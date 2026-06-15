"""
AegisAI — Risk Assessment Page  (v2.1 — Fixed & Enhanced)
===========================================================
Changes from v2.0:
  - BUG FIX: "Not Sure" now correctly submits "not_sure" (was "no")
  - BUG FIX: Removed duplicate complete_assessment() call
  - BUG FIX: Q15 completion guaranteed — answer() always returns result
  - NEW: Professional modal popup with circular progress ring
  - NEW: Personalised recommendations per risk category
  - NEW: Emergency contacts always shown in popup
  - NEW: Detailed Report window with export capability
  - NEW: Smooth fade-in animation on popup
"""
from __future__ import annotations

import math
import os
import logging
import threading
from datetime import datetime
from typing import Optional, Callable

import customtkinter as ctk
from ui.theme import Theme
from ui.components.risk_badge import RiskBadge
from models.assessment import RiskLevel, AssessmentResult
from services.assessment_service import TOTAL_QUESTIONS, TOTAL_STEPS, MAX_SIMPLE_SCORE

log = logging.getLogger(__name__)


# ── Color mapping for each risk level ────────────────────────────────────────
_LEVEL_COLORS = {
    RiskLevel.LOW:      "#10B981",   # Emerald green
    RiskLevel.MEDIUM:   "#FBBF24",   # Amber yellow
    RiskLevel.HIGH:     "#F97316",   # Orange
    RiskLevel.CRITICAL: "#EF4444",   # Red
    RiskLevel.UNKNOWN:  "#64748B",   # Slate
}

_LEVEL_BG = {
    RiskLevel.LOW:      "#0D2D1E",
    RiskLevel.MEDIUM:   "#2D2010",
    RiskLevel.HIGH:     "#2D1A05",
    RiskLevel.CRITICAL: "#2D0A0A",
    RiskLevel.UNKNOWN:  "#1A2030",
}

_LEVEL_LABELS = {
    RiskLevel.LOW:      "🟢  LOW RISK",
    RiskLevel.MEDIUM:   "🟡  MODERATE RISK",
    RiskLevel.HIGH:     "🟠  HIGH RISK",
    RiskLevel.CRITICAL: "🔴  CRITICAL RISK",
    RiskLevel.UNKNOWN:  "❔  NOT ASSESSED",
}


# ── Circular progress ring (canvas-drawn) ─────────────────────────────────────

class _RingProgress(ctk.CTkCanvas):
    """
    Canvas widget that draws a circular progress arc with
    the percentage displayed in the centre.
    """

    SIZE = 160  # diameter in pixels

    def __init__(self, parent, pct: float, color: str) -> None:
        super().__init__(
            parent,
            width=self.SIZE, height=self.SIZE,
            bg=Theme.BG_CARD,
            highlightthickness=0,
        )
        self._pct   = pct
        self._color = color
        self._draw(pct)

    def _draw(self, pct: float) -> None:
        self.delete("all")
        pad   = 14
        x0, y0 = pad, pad
        x1, y1 = self.SIZE - pad, self.SIZE - pad

        # Background circle
        self.create_oval(x0, y0, x1, y1, outline="#253354", width=14, fill="")

        # Progress arc (start at top = -90°)
        extent = (pct / 100) * 360
        if extent > 0:
            self.create_arc(
                x0, y0, x1, y1,
                start=90,
                extent=-extent,
                style="arc",
                outline=self._color,
                width=14,
            )

        # Centre text
        cx, cy = self.SIZE / 2, self.SIZE / 2
        self.create_text(
            cx, cy - 10,
            text=f"{pct:.0f}%",
            font=("Segoe UI", 26, "bold"),
            fill=self._color,
        )
        self.create_text(
            cx, cy + 16,
            text="risk score",
            font=("Segoe UI", 9),
            fill=Theme.TEXT_MUTED,
        )

    def animate_to(self, target_pct: float, steps: int = 40) -> None:
        """Animate the ring from 0 to target_pct."""
        step_size = target_pct / max(steps, 1)

        def _tick(current: float) -> None:
            current = min(current, target_pct)
            self._draw(current)
            if current < target_pct:
                self.after(20, _tick, current + step_size)

        self.after(60, _tick, 0.0)


# ── Result popup modal ────────────────────────────────────────────────────────

class ResultPopup(ctk.CTkToplevel):
    """
    Modal popup displayed after the assessment completes.

    Features:
    - Centered over parent, grabs focus (modal behaviour)
    - Semi-transparent dimmed background overlay
    - Animated circular progress ring
    - Risk badge with colored background
    - Personalised recommendations
    - Emergency contacts (always visible)
    - Action buttons: View Report | Retake | Resources | Close
    """

    WIDTH  = 680
    HEIGHT = 720

    def __init__(
        self,
        parent,
        result: AssessmentResult,
        on_retake:    Callable,
        on_resources: Callable,
        on_close:     Callable,
    ) -> None:
        super().__init__(parent)
        self._result      = result
        self._on_retake    = on_retake
        self._on_resources = on_resources
        self._on_close     = on_close

        self._configure_window(parent)
        self._build()
        self._animate_in()

    # ------------------------------------------------------------------

    def _configure_window(self, parent) -> None:
        self.title("Risk Assessment Complete — AegisAI")
        self.resizable(False, False)
        self.grab_set()           # modal — block interaction with parent
        self.lift()
        self.focus_force()

        # Center on parent
        self.update_idletasks()
        px = parent.winfo_rootx() + (parent.winfo_width()  - self.WIDTH)  // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - self.HEIGHT) // 2
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{px}+{py}")

        self.configure(fg_color=Theme.BG_DARK)
        self.protocol("WM_DELETE_WINDOW", self._close)

    def _build(self) -> None:
        result = self._result
        level  = result.risk_level
        color  = _LEVEL_COLORS.get(level, Theme.ACCENT)
        bg     = _LEVEL_BG.get(level, Theme.BG_CARD)

        # Root scrollable content
        scroll = ctk.CTkScrollableFrame(
            self, fg_color=Theme.BG_DARK, corner_radius=0,
            scrollbar_button_color=Theme.BG_INPUT,
            scrollbar_button_hover_color=color,
        )
        scroll.pack(fill="both", expand=True)
        scroll.grid_columnconfigure(0, weight=1)

        # ── 1. Header banner ──────────────────────────────────────────
        banner = ctk.CTkFrame(
            scroll, fg_color=bg,
            corner_radius=Theme.RADIUS_LG,
            border_width=2, border_color=color,
        )
        banner.grid(row=0, column=0, padx=Theme.PAD_LG,
                    pady=(Theme.PAD_LG, Theme.PAD_SM), sticky="ew")
        banner.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            banner,
            text="RISK ASSESSMENT COMPLETE",
            font=("Segoe UI", 9, "bold"),
            text_color=color,
        ).grid(row=0, column=0, padx=Theme.CARD_PAD,
               pady=(Theme.CARD_PAD, 2), sticky="w")

        ctk.CTkLabel(
            banner,
            text="🛡️  AegisAI has analysed your responses",
            font=("Segoe UI", 16, "bold"),
            text_color=Theme.TEXT_PRIMARY,
        ).grid(row=1, column=0, padx=Theme.CARD_PAD, pady=(0, 4), sticky="w")

        ctk.CTkLabel(
            banner,
            text=f"Assessed on {result.assessed_at}  ·  {TOTAL_QUESTIONS} questions answered",
            font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED,
        ).grid(row=2, column=0, padx=Theme.CARD_PAD,
               pady=(0, Theme.CARD_PAD), sticky="w")

        # ── 2. Score section (ring + badge side by side) ──────────────
        score_frame = ctk.CTkFrame(
            scroll, fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_LG,
            border_width=1, border_color=Theme.BORDER,
        )
        score_frame.grid(row=1, column=0, padx=Theme.PAD_LG,
                         pady=Theme.PAD_SM, sticky="ew")
        score_frame.grid_columnconfigure(0, weight=1)
        score_frame.grid_columnconfigure(1, weight=1)

        # Left: ring
        ring_frame = ctk.CTkFrame(score_frame, fg_color="transparent")
        ring_frame.grid(row=0, column=0, padx=Theme.CARD_PAD,
                        pady=Theme.CARD_PAD, sticky="nsew")

        self._ring = _RingProgress(ring_frame, 0.0, color)
        self._ring.pack(pady=(0, 8))

        ctk.CTkLabel(
            ring_frame,
            text=f"Score: {result.simple_score} / {MAX_SIMPLE_SCORE}",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        ).pack()

        # Right: risk category pill + answer breakdown
        right_frame = ctk.CTkFrame(score_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, padx=Theme.CARD_PAD,
                         pady=Theme.CARD_PAD, sticky="nsew")

        ctk.CTkLabel(
            right_frame,
            text="RISK CATEGORY",
            font=("Segoe UI", 9, "bold"),
            text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", pady=(0, 6))

        # Risk level pill
        pill = ctk.CTkFrame(
            right_frame, fg_color=bg,
            corner_radius=Theme.RADIUS,
            border_width=2, border_color=color,
        )
        pill.pack(anchor="w", pady=(0, 12))
        ctk.CTkLabel(
            pill,
            text=_LEVEL_LABELS.get(level, level.label),
            font=("Segoe UI", 17, "bold"),
            text_color=color,
        ).pack(padx=16, pady=8)

        # Score progress bar
        ctk.CTkLabel(
            right_frame, text="Risk Percentage",
            font=("Segoe UI", 10), text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", pady=(0, 3))

        pct_bar = ctk.CTkProgressBar(
            right_frame, height=10,
            fg_color=Theme.BG_INPUT, progress_color=color,
            corner_radius=5,
        )
        pct_bar.pack(fill="x", pady=(0, 12))
        pct_bar.set(min(result.simple_pct / 100, 1.0))

        # Answer breakdown chips
        breakdown_row = ctk.CTkFrame(right_frame, fg_color="transparent")
        breakdown_row.pack(anchor="w")

        for label, count, fg in [
            (f"✅ Yes: {result.yes_count}",       result.yes_count,      Theme.SUCCESS),
            (f"❌ No: {result.no_count}",          result.no_count,       Theme.DANGER),
            (f"❓ Not Sure: {result.not_sure_count}", result.not_sure_count, Theme.WARNING),
        ]:
            ctk.CTkLabel(
                breakdown_row,
                text=f"  {label}  ",
                font=Theme.FONT_TINY,
                text_color=fg,
                fg_color=Theme.BG_INPUT,
                corner_radius=4,
            ).pack(side="left", padx=(0, 6), ipady=3)

        # ── 3. Recommendations ────────────────────────────────────────
        rec_card = ctk.CTkFrame(
            scroll, fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_LG,
            border_width=1, border_color=Theme.BORDER,
        )
        rec_card.grid(row=2, column=0, padx=Theme.PAD_LG,
                      pady=Theme.PAD_SM, sticky="ew")
        rec_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            rec_card,
            text="📋  Personalised Recommendations",
            font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=Theme.CARD_PAD,
               pady=(Theme.CARD_PAD, 6), sticky="w")

        for ridx, rec in enumerate(result.recommendations):
            row_f = ctk.CTkFrame(rec_card, fg_color="transparent")
            row_f.grid(row=ridx + 1, column=0,
                       padx=Theme.CARD_PAD, pady=2, sticky="ew")
            row_f.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                row_f, text="›",
                font=("Segoe UI", 13, "bold"),
                text_color=color, width=14,
            ).grid(row=0, column=0, padx=(0, 6), sticky="nw", pady=1)

            ctk.CTkLabel(
                row_f, text=rec,
                font=Theme.FONT_BODY,
                text_color=Theme.TEXT_PRIMARY,
                anchor="w", justify="left",
                wraplength=540,
            ).grid(row=0, column=1, sticky="w")

        ctk.CTkFrame(rec_card, height=Theme.PAD_SM,
                     fg_color="transparent").grid(row=200, column=0)

        # ── 4. Emergency contacts (always shown) ──────────────────────
        sos_card = ctk.CTkFrame(
            scroll, fg_color="#2D0A0A",
            corner_radius=Theme.RADIUS_LG,
            border_width=2, border_color=Theme.DANGER,
        )
        sos_card.grid(row=3, column=0, padx=Theme.PAD_LG,
                      pady=Theme.PAD_SM, sticky="ew")
        sos_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            sos_card,
            text="🚨  Emergency Contacts  —  Available 24/7",
            font=("Segoe UI", 11, "bold"),
            text_color=Theme.DANGER,
        ).grid(row=0, column=0, padx=Theme.CARD_PAD,
               pady=(Theme.CARD_PAD, 6), sticky="w")

        contacts = [
            ("📞  112", "National Emergency Services",   "#EF4444"),
            ("📞  181", "Women's Helpline",               "#F97316"),
            ("📞  1098","Childline India",                "#FBBF24"),
            ("📞  100", "Police",                         "#EF4444"),
        ]
        contacts_row = ctk.CTkFrame(sos_card, fg_color="transparent")
        contacts_row.grid(row=1, column=0, padx=Theme.CARD_PAD,
                          pady=(0, Theme.CARD_PAD), sticky="ew")

        for cidx, (num, name, c_color) in enumerate(contacts):
            chip = ctk.CTkFrame(
                contacts_row, fg_color=Theme.BG_DARK,
                corner_radius=Theme.RADIUS_SM,
                border_width=1, border_color=c_color,
            )
            chip.grid(row=0, column=cidx, padx=(0 if cidx == 0 else 6, 0))

            ctk.CTkLabel(
                chip, text=num,
                font=("Segoe UI", 13, "bold"),
                text_color=c_color,
            ).pack(padx=10, pady=(6, 1))

            ctk.CTkLabel(
                chip, text=name,
                font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
            ).pack(padx=10, pady=(0, 6))

        # ── 5. Action buttons ─────────────────────────────────────────
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.grid(row=4, column=0, padx=Theme.PAD_LG,
                       pady=(Theme.PAD_SM, Theme.PAD_LG), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        btn_cfg = [
            ("📄  View Detailed Report", color,        "#1A1A2E",        self._open_report),
            ("↺  Retake Assessment",     Theme.BG_CARD, Theme.ACCENT,     self._retake),
            ("📁  Go To Resources",      Theme.BG_CARD, Theme.TEXT_ACCENT, self._go_resources),
            ("✖  Close",                 Theme.BG_CARD, Theme.TEXT_MUTED,  self._close),
        ]
        for col, (text, fg, tc, cmd) in enumerate(btn_cfg):
            ctk.CTkButton(
                btn_frame, text=text,
                font=("Segoe UI", 10, "bold"),
                height=38,
                fg_color=fg,
                hover_color=_LEVEL_COLORS.get(level, Theme.ACCENT_HOVER),
                text_color=tc,
                border_color=color if col > 0 else fg,
                border_width=1 if col > 0 else 0,
                corner_radius=Theme.RADIUS,
                command=cmd,
            ).grid(row=0, column=col, padx=(0 if col == 0 else 4, 0), sticky="ew")

    def _animate_in(self) -> None:
        """Start the ring animation after the window is shown."""
        self.after(200, lambda: self._ring.animate_to(self._result.simple_pct))

    # ------------------------------------------------------------------

    def _open_report(self) -> None:
        self.grab_release()
        DetailedReportWindow(self, self._result)

    def _retake(self) -> None:
        self._close()
        self._on_retake()

    def _go_resources(self) -> None:
        self._close()
        self._on_resources()

    def _close(self) -> None:
        self.grab_release()
        self._on_close()
        self.destroy()


# ── Detailed Report Window ────────────────────────────────────────────────────

class DetailedReportWindow(ctk.CTkToplevel):
    """
    Secondary window with the full detailed assessment report.
    Includes export-to-text functionality.
    """

    def __init__(self, parent, result: AssessmentResult) -> None:
        super().__init__(parent)
        self._result = result
        self.title("Detailed Assessment Report — AegisAI")
        self.geometry("700x640")
        self.minsize(600, 500)
        self.configure(fg_color=Theme.BG_DARK)
        self.grab_set()
        self.lift()
        self._build()

    def _build(self) -> None:
        result  = self._result
        level   = result.risk_level
        color   = _LEVEL_COLORS.get(level, Theme.ACCENT)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        scroll = ctk.CTkScrollableFrame(
            self, fg_color=Theme.BG_DARK, corner_radius=0,
            scrollbar_button_color=Theme.BG_INPUT,
            scrollbar_button_hover_color=color,
        )
        scroll.grid(row=0, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        # Header
        ctk.CTkLabel(
            scroll,
            text="📄  Detailed Assessment Report",
            font=Theme.FONT_TITLE, text_color=Theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=Theme.PAD_LG,
               pady=(Theme.PAD_LG, Theme.PAD_SM), sticky="w")

        # Meta card
        meta = self._card(scroll, row=1)
        rows = [
            ("📅  Assessment Date",    result.assessed_at),
            ("❓  Questions Answered", str(TOTAL_QUESTIONS)),
            ("✅  Yes Answers",        str(result.yes_count)),
            ("❌  No Answers",         str(result.no_count)),
            ("🤷  Not Sure Answers",   str(result.not_sure_count)),
            ("📊  Final Score",        f"{result.simple_score} / {MAX_SIMPLE_SCORE} points"),
            ("📈  Risk Percentage",    f"{result.simple_pct:.1f}%"),
            ("🏷️  Risk Category",      _LEVEL_LABELS.get(level, level.label)),
        ]
        for ridx, (lbl, val) in enumerate(rows):
            row_f = ctk.CTkFrame(meta, fg_color="transparent")
            row_f.grid(row=ridx, column=0, padx=Theme.CARD_PAD,
                       pady=3, sticky="ew")
            row_f.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                row_f, text=lbl,
                font=("Segoe UI", 10, "bold"),
                text_color=Theme.TEXT_MUTED, width=180, anchor="w",
            ).grid(row=0, column=0, sticky="w")

            ctk.CTkLabel(
                row_f, text=val,
                font=Theme.FONT_BODY, text_color=Theme.TEXT_PRIMARY, anchor="w",
            ).grid(row=0, column=1, sticky="w")

        ctk.CTkFrame(meta, height=Theme.PAD_SM, fg_color="transparent").grid(row=100, column=0)

        # Summary
        ctk.CTkLabel(
            scroll, text="📝  Summary",
            font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_PRIMARY,
        ).grid(row=2, column=0, padx=Theme.PAD_LG,
               pady=(Theme.PAD, Theme.PAD_SM), sticky="w")

        ctk.CTkLabel(
            scroll, text=result.summary,
            font=Theme.FONT_BODY, text_color=Theme.TEXT_SECONDARY,
            wraplength=620, justify="left",
        ).grid(row=3, column=0, padx=Theme.PAD_LG, pady=(0, Theme.PAD), sticky="w")

        # Recommendations
        ctk.CTkLabel(
            scroll, text="📋  Recommendations",
            font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_PRIMARY,
        ).grid(row=4, column=0, padx=Theme.PAD_LG,
               pady=(0, Theme.PAD_SM), sticky="w")

        rec_card = self._card(scroll, row=5)
        for ridx, rec in enumerate(result.recommendations):
            row_f = ctk.CTkFrame(rec_card, fg_color="transparent")
            row_f.grid(row=ridx, column=0, padx=Theme.CARD_PAD,
                       pady=2, sticky="ew")
            row_f.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                row_f, text="›",
                font=("Segoe UI", 13, "bold"),
                text_color=color, width=14,
            ).grid(row=0, column=0, padx=(0, 6), sticky="nw")

            ctk.CTkLabel(
                row_f, text=rec,
                font=Theme.FONT_BODY, text_color=Theme.TEXT_PRIMARY,
                anchor="w", justify="left", wraplength=560,
            ).grid(row=0, column=1, sticky="w")

        ctk.CTkFrame(rec_card, height=Theme.PAD_SM, fg_color="transparent").grid(row=100, column=0)

        # Emergency contacts
        ctk.CTkLabel(
            scroll, text="🚨  Emergency Contacts",
            font=Theme.FONT_SUBTITLE, text_color=Theme.DANGER,
        ).grid(row=6, column=0, padx=Theme.PAD_LG,
               pady=(Theme.PAD, Theme.PAD_SM), sticky="w")

        sos_card = ctk.CTkFrame(
            scroll, fg_color="#2D0A0A",
            corner_radius=Theme.RADIUS_LG,
            border_width=1, border_color=Theme.DANGER,
        )
        sos_card.grid(row=7, column=0, padx=Theme.PAD_LG,
                      pady=(0, Theme.PAD), sticky="ew")
        sos_card.grid_columnconfigure(0, weight=1)

        for num, name in [("112", "Emergency Services"), ("181", "Women's Helpline"),
                           ("1098", "Childline India"), ("100", "Police")]:
            r_f = ctk.CTkFrame(sos_card, fg_color="transparent")
            r_f.grid(sticky="ew", padx=Theme.CARD_PAD, pady=2)
            r_f.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(r_f, text=num, font=("Segoe UI", 12, "bold"),
                         text_color=Theme.DANGER, width=50).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(r_f, text=name, font=Theme.FONT_BODY,
                         text_color=Theme.TEXT_SECONDARY, anchor="w").grid(row=0, column=1, sticky="w")

        ctk.CTkFrame(sos_card, height=Theme.PAD_SM, fg_color="transparent").grid(sticky="ew")

        # Export button row
        btn_row = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_row.grid(row=8, column=0, padx=Theme.PAD_LG,
                     pady=(0, Theme.PAD_LG), sticky="ew")

        ctk.CTkButton(
            btn_row,
            text="💾  Export Report (.txt)",
            font=Theme.FONT_SMALL, width=170, height=36,
            fg_color=color, hover_color=Theme.ACCENT_HOVER,
            text_color="#1A1A2E",
            corner_radius=Theme.RADIUS,
            command=self._export,
        ).pack(side="left")

        ctk.CTkButton(
            btn_row, text="✖  Close",
            font=Theme.FONT_SMALL, width=80, height=36,
            fg_color="transparent", hover_color=Theme.BG_HOVER,
            text_color=Theme.TEXT_MUTED, border_width=0,
            command=self._do_close,
        ).pack(side="left", padx=(8, 0))

    def _card(self, parent, row: int) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            parent, fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_LG,
            border_width=1, border_color=Theme.BORDER,
        )
        card.grid(row=row, column=0, padx=Theme.PAD_LG,
                  pady=(0, Theme.PAD_SM), sticky="ew")
        card.grid_columnconfigure(0, weight=1)
        return card

    def _export(self) -> None:
        """Export report as a plain text file to the Desktop."""
        lines = [
            "=" * 60,
            "AegisAI — Risk Assessment Report",
            "=" * 60,
            "",
        ] + self._result.report_lines + [
            "",
            "EMERGENCY CONTACTS:",
            "  112  — Emergency Services",
            "  181  — Women's Helpline",
            "  1098 — Childline India",
            "  100  — Police",
            "",
            "Generated by AegisAI",
        ]

        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        path    = os.path.join(desktop, "AegisAI_Report.txt")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            self._show_toast(f"✅  Saved to Desktop: AegisAI_Report.txt")
        except Exception as exc:
            self._show_toast(f"❌  Export failed: {exc}")

    def _show_toast(self, msg: str) -> None:
        toast = ctk.CTkLabel(
            self, text=msg,
            font=Theme.FONT_SMALL,
            fg_color=Theme.BG_CARD,
            text_color=Theme.TEXT_PRIMARY,
            corner_radius=Theme.RADIUS,
        )
        toast.place(relx=0.5, rely=0.95, anchor="s")
        self.after(3000, toast.destroy)

    def _do_close(self) -> None:
        self.grab_release()
        self.destroy()


# ── Main Assessment Page ──────────────────────────────────────────────────────

class AssessmentPage(ctk.CTkFrame):
    """
    Risk assessment wizard page.

    Parameters
    ----------
    parent             : Parent widget (the app content area)
    assessment_service : AssessmentService instance
    session_service    : SessionService instance
    navigate_cb        : Optional callback(page_name: str) for navigation buttons
    """

    def __init__(self, parent, assessment_service,
                 session_service, navigate_cb: Optional[Callable] = None) -> None:
        super().__init__(parent, fg_color=Theme.BG_DARK, corner_radius=0)
        self._svc         = assessment_service
        self._sess        = session_service
        self._navigate_cb = navigate_cb   # for "Go to Resources" button
        self._result: Optional[AssessmentResult] = None
        self._build_idle()

    # ------------------------------------------------------------------

    def _build_idle(self) -> None:
        """Show the start screen."""
        self._clear()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center = ctk.CTkFrame(self, fg_color="transparent")
        center.grid(row=0, column=0)

        ctk.CTkLabel(
            center, text="🛡️", font=("Segoe UI", 56),
        ).pack(pady=(0, 12))

        ctk.CTkLabel(
            center, text="Risk Assessment",
            font=Theme.FONT_HERO, text_color=Theme.TEXT_PRIMARY,
        ).pack()

        ctk.CTkLabel(
            center,
            text=(
                "Answer 15 questions to receive a personalised risk assessment.\n"
                "All responses are completely private and stored only on your device."
            ),
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_SECONDARY,
            justify="center",
        ).pack(pady=(8, 28))

        # Info chips
        chips_row = ctk.CTkFrame(center, fg_color="transparent")
        chips_row.pack(pady=(0, 24))
        for info in ["15 Questions", "6 Steps", "~3 Minutes", "Private & Confidential"]:
            ctk.CTkLabel(
                chips_row,
                text=f"  {info}  ",
                font=Theme.FONT_TINY,
                text_color=Theme.TEXT_ACCENT,
                fg_color=Theme.BG_CARD,
                corner_radius=Theme.RADIUS_SM,
            ).pack(side="left", padx=4, ipady=4)

        # Scoring legend
        legend = ctk.CTkFrame(center, fg_color=Theme.BG_CARD,
                              corner_radius=Theme.RADIUS, border_width=1,
                              border_color=Theme.BORDER)
        legend.pack(pady=(0, 20))

        ctk.CTkLabel(
            legend, text="Scoring System",
            font=("Segoe UI", 10, "bold"), text_color=Theme.TEXT_MUTED,
        ).pack(padx=20, pady=(10, 4))

        leg_row = ctk.CTkFrame(legend, fg_color="transparent")
        leg_row.pack(padx=20, pady=(0, 10))
        for txt, pts, clr in [
            ("Yes = 2 pts",      "2", Theme.SUCCESS),
            ("Not Sure = 1 pt",  "1", Theme.WARNING),
            ("No = 0 pts",       "0", Theme.DANGER),
        ]:
            ctk.CTkLabel(
                leg_row, text=f"  {txt}  ",
                font=Theme.FONT_TINY, text_color=clr,
                fg_color=Theme.BG_INPUT, corner_radius=4,
            ).pack(side="left", padx=4, ipady=3)

        ctk.CTkButton(
            center,
            text="▶   Start Assessment",
            font=("Segoe UI", 13, "bold"),
            width=220, height=44,
            fg_color=Theme.ACCENT,
            hover_color=Theme.ACCENT_HOVER,
            text_color="#1A1A2E",
            corner_radius=Theme.RADIUS,
            command=self._start,
        ).pack()

    def _build_wizard(self) -> None:
        """Show the active questionnaire UI."""
        self._clear()
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Progress header ───────────────────────────────────────────
        prog_frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD,
                                   border_width=0, corner_radius=0)
        prog_frame.grid(row=0, column=0, sticky="ew")
        prog_frame.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(prog_frame, fg_color="transparent")
        inner.grid(row=0, column=0, padx=Theme.PAD_LG,
                   pady=(Theme.PAD, Theme.PAD_SM), sticky="ew")
        inner.grid_columnconfigure(0, weight=1)

        self._step_lbl = ctk.CTkLabel(
            inner, text="Step 1 of 6",
            font=Theme.FONT_SUBTITLE, text_color=Theme.ACCENT,
        )
        self._step_lbl.grid(row=0, column=0, sticky="w")

        self._q_lbl = ctk.CTkLabel(
            inner, text="Question 1 of 15",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        )
        self._q_lbl.grid(row=0, column=1, sticky="e")

        self._prog_bar = ctk.CTkProgressBar(
            prog_frame, width=0, height=4,
            fg_color=Theme.BG_INPUT, progress_color=Theme.ACCENT,
            corner_radius=2,
        )
        self._prog_bar.grid(row=1, column=0, sticky="ew")
        self._prog_bar.set(0)

        # ── Two-column layout: question left, live gauge right ────────
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=2, column=0, padx=Theme.PAD_LG,
                  pady=Theme.PAD_LG, sticky="nsew")
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # Left: question card
        left = ctk.CTkFrame(body, fg_color=Theme.BG_CARD,
                             corner_radius=Theme.RADIUS_LG,
                             border_width=1, border_color=Theme.BORDER)
        left.grid(row=0, column=0, padx=(0, Theme.PAD_SM), sticky="nsew")
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            left, text="QUESTION",
            font=("Segoe UI", 9, "bold"),
            text_color=Theme.TEXT_MUTED,
        ).grid(row=0, column=0, padx=Theme.CARD_PAD,
               pady=(Theme.CARD_PAD, 4), sticky="w")

        self._q_text = ctk.CTkLabel(
            left, text="",
            font=("Segoe UI", 14),
            text_color=Theme.TEXT_PRIMARY,
            wraplength=520, justify="left", anchor="nw",
        )
        self._q_text.grid(row=1, column=0, padx=Theme.CARD_PAD,
                          pady=(0, Theme.PAD), sticky="nw")

        # ── Answer buttons (3: Yes / Not Sure / No) ───────────────────
        # NOTE: "Not Sure" value is "not_sure" — this is the critical bug fix
        btn_frame = ctk.CTkFrame(left, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=Theme.CARD_PAD,
                       pady=Theme.CARD_PAD, sticky="ew")

        answer_options = [
            ("✅  Yes",      "yes",      Theme.SUCCESS, "Yes (2 pts)"),
            ("❓  Not Sure", "not_sure", Theme.WARNING, "Not Sure (1 pt)"),
            ("❌  No",       "no",       Theme.DANGER,  "No (0 pts)"),
        ]
        self._answer_buttons = []
        for label, value, color, tooltip in answer_options:
            btn = ctk.CTkButton(
                btn_frame,
                text=label,
                font=Theme.FONT_SMALL,
                width=118, height=42,
                fg_color=Theme.BG_INPUT,
                hover_color=color,
                text_color=color,
                border_color=color,
                border_width=1,
                corner_radius=Theme.RADIUS,
                command=lambda v=value: self._answer(v),
            )
            btn.pack(side="left", padx=(0, 8))
            self._answer_buttons.append(btn)

        # Abort button
        ctk.CTkButton(
            left, text="✖  Abort",
            font=Theme.FONT_TINY, width=72, height=26,
            fg_color="transparent", hover_color=Theme.BG_HOVER,
            text_color=Theme.TEXT_MUTED, border_width=0,
            command=self._build_idle,
        ).grid(row=3, column=0, padx=Theme.CARD_PAD,
               pady=(0, Theme.PAD_SM), sticky="e")

        # Right: live gauge panel
        right = ctk.CTkFrame(body, fg_color=Theme.BG_CARD,
                              corner_radius=Theme.RADIUS_LG,
                              border_width=1, border_color=Theme.BORDER)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            right, text="LIVE RISK",
            font=("Segoe UI", 9, "bold"), text_color=Theme.TEXT_MUTED,
        ).grid(row=0, column=0, padx=Theme.PAD, pady=(Theme.PAD, 4))

        self._gauge_pct_lbl = ctk.CTkLabel(
            right, text="0%",
            font=("Segoe UI", 32, "bold"), text_color=Theme.SUCCESS,
        )
        self._gauge_pct_lbl.grid(row=1, column=0, padx=Theme.PAD, pady=6)

        self._gauge_bar = ctk.CTkProgressBar(
            right, width=24, height=100,
            fg_color=Theme.BG_INPUT, progress_color=Theme.SUCCESS,
            corner_radius=6, orientation="vertical",
        )
        self._gauge_bar.grid(row=2, column=0, padx=Theme.PAD, pady=6)
        self._gauge_bar.set(0)

        self._gauge_badge = RiskBadge(right, RiskLevel.UNKNOWN)
        self._gauge_badge.grid(row=3, column=0, padx=Theme.PAD,
                                pady=(4, Theme.PAD_SM))

        self._answers_lbl = ctk.CTkLabel(
            right, text="0 / 15",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        )
        self._answers_lbl.grid(row=4, column=0, padx=Theme.PAD,
                                pady=(0, Theme.PAD))

        # Scoring breakdown labels (live)
        self._score_breakdown = ctk.CTkLabel(
            right,
            text="✅ 0  ❓ 0  ❌ 0",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
            justify="center",
        )
        self._score_breakdown.grid(row=5, column=0, padx=Theme.PAD,
                                    pady=(0, Theme.PAD))

        self._refresh_ui()

    # ------------------------------------------------------------------

    def _start(self) -> None:
        self._svc.start()
        self._sess.start_assessment()
        self._build_wizard()

    def _answer(self, response: str) -> None:
        """
        Process an answer button click.
        Disables buttons during processing to prevent double-submit.
        """
        # Disable all answer buttons immediately to prevent double clicks
        if hasattr(self, "_answer_buttons"):
            for btn in self._answer_buttons:
                btn.configure(state="disabled")

        # Re-enable after brief delay (unless page changes)
        self.after(300, self._re_enable_buttons)

        # Submit to service
        try:
            result = self._svc.answer(response)
        except Exception as exc:
            log.error("Assessment answer error: %s", exc)
            self._re_enable_buttons()
            return

        if isinstance(result, AssessmentResult):
            # ── CRITICAL FIX: only call complete_assessment ONCE ──────
            # The service's _finish() does NOT call it anymore,
            # so we do it here exactly once.
            self._sess.complete_assessment(result)
            self._result = result
            # Show the popup (don't rebuild the wizard page underneath)
            self.after(150, lambda r=result: self._show_result_popup(r))
        else:
            # More questions remain
            self._refresh_ui()
            partial = self._svc.get_partial_result()
            if partial:
                self._update_gauge(partial)

    def _re_enable_buttons(self) -> None:
        if hasattr(self, "_answer_buttons"):
            for btn in self._answer_buttons:
                try:
                    btn.configure(state="normal")
                except Exception:
                    pass

    def _show_result_popup(self, result: AssessmentResult) -> None:
        """Launch the result modal popup centered on the parent window."""
        # Find the root window
        root = self.winfo_toplevel()

        def _go_resources():
            if self._navigate_cb:
                self._navigate_cb("resources")

        ResultPopup(
            parent       = root,
            result       = result,
            on_retake    = self._build_idle,
            on_resources = _go_resources,
            on_close     = self._build_idle,
        )

    def _refresh_ui(self) -> None:
        q_num, total_q, step, pct = self._svc.get_progress()
        q = self._svc.current_question
        if not q:
            return

        self._step_lbl.configure(
            text=f"Step {step} of {TOTAL_STEPS}  —  {q.step_name}"
        )
        self._q_lbl.configure(text=f"Q {q_num} of {total_q}")
        self._q_text.configure(text=q.text)
        self._prog_bar.set(pct / 100)
        self._answers_lbl.configure(text=f"{q_num - 1} / {total_q}")

        # Update live scoring breakdown
        y, n, ns = self._svc.get_answer_counts()
        if hasattr(self, "_score_breakdown"):
            self._score_breakdown.configure(
                text=f"✅ {y}  ❓ {ns}  ❌ {n}"
            )

    def _update_gauge(self, result: AssessmentResult) -> None:
        pct   = result.simple_pct if result.simple_pct > 0 else result.risk_pct
        level = result.risk_level
        color = _LEVEL_COLORS.get(level, Theme.ACCENT)
        self._gauge_pct_lbl.configure(text=f"{pct:.0f}%", text_color=color)
        self._gauge_bar.configure(progress_color=color)
        self._gauge_bar.set(min(pct / 100, 1.0))
        self._gauge_badge.update(level)

    def _clear(self) -> None:
        self._answer_buttons = []
        for w in self.winfo_children():
            w.destroy()
