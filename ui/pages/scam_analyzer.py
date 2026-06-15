"""
AegisAI — Scam Analyzer Page
==============================
Paste a job offer text → get instant risk analysis with
suspicion gauge, red-flag chips, category breakdown, and recommendations.
Includes a persistent local scan history log list at the bottom left.
"""
from __future__ import annotations

import threading
import logging
from typing import Optional, List

import customtkinter as ctk
from ui.theme import Theme
from models.scam import DetectionResult, SuspicionLevel

log = logging.getLogger(__name__)


class ScamAnalyzerPage(ctk.CTkFrame):
    """Dedicated scam detection page with input, results, and scan history panels."""

    def __init__(self, parent, scam_service) -> None:
        super().__init__(parent, fg_color=Theme.BG_DARK, corner_radius=0)
        self._svc = scam_service
        self._result: Optional[DetectionResult] = None
        self._history_items: List[ctk.CTkFrame] = []
        self._build()
        self._load_history()

    def _build(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ── Title bar ─────────────────────────────────────────────────
        title_bar = ctk.CTkFrame(self, fg_color="transparent")
        title_bar.grid(row=0, column=0, columnspan=2, padx=Theme.PAD_LG,
                       pady=(Theme.PAD, Theme.PAD_SM), sticky="ew")
        title_bar.grid_columnconfigure(0, weight=1)

        left_title = ctk.CTkFrame(title_bar, fg_color="transparent")
        left_title.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            left_title, text="🔍  Scam Analyzer",
            font=Theme.FONT_TITLE, text_color=Theme.TEXT_PRIMARY,
        ).pack(anchor="w")
        ctk.CTkLabel(
            left_title,
            text="Paste a job offer, recruitment message, or suspicious ad below",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 0))

        # Status badge
        ctk.CTkLabel(
            title_bar,
            text="  AI-Powered  ",
            font=Theme.FONT_TINY,
            text_color=Theme.ACCENT,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_SM,
        ).grid(row=0, column=1, sticky="e", ipady=4)

        # ── Left: Input & History panel ───────────────────────────────
        left = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_LG,
            border_width=1,
            border_color=Theme.BORDER,
        )
        left.grid(row=1, column=0, padx=(Theme.PAD_LG, Theme.PAD_SM),
                  pady=(0, Theme.PAD_LG), sticky="nsew")
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            left, text="📋  Job Offer / Message Text",
            font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=Theme.CARD_PAD,
               pady=(Theme.CARD_PAD, 6), sticky="w")

        self._textbox = ctk.CTkTextbox(
            left,
            font=Theme.FONT_BODY,
            fg_color=Theme.BG_INPUT,
            text_color=Theme.TEXT_PRIMARY,
            border_color=Theme.BORDER,
            border_width=1,
            corner_radius=Theme.RADIUS,
            scrollbar_button_color=Theme.BG_INPUT,
            height=170,
            wrap="word",
        )
        self._textbox.grid(row=1, column=0, padx=Theme.CARD_PAD,
                           pady=(0, Theme.PAD_SM), sticky="ew")
        self._textbox.insert("1.0", "Paste the job offer text here…")
        self._textbox.bind("<FocusIn>", self._on_text_focus)

        # Action buttons row
        btn_row = ctk.CTkFrame(left, fg_color="transparent")
        btn_row.grid(row=2, column=0, padx=Theme.CARD_PAD, pady=(0, 8), sticky="ew")

        self._analyze_btn = ctk.CTkButton(
            btn_row,
            text="🔍  Analyze for Scam",
            font=("Segoe UI", 11, "bold"),
            width=148, height=34,
            fg_color=Theme.ACCENT,
            hover_color=Theme.ACCENT_HOVER,
            text_color="#1A1A2E",
            corner_radius=Theme.RADIUS,
            command=self._run_analysis,
        )
        self._analyze_btn.pack(side="left")

        ctk.CTkButton(
            btn_row,
            text="Clear",
            font=Theme.FONT_TINY,
            width=58, height=34,
            fg_color="transparent",
            hover_color=Theme.BG_HOVER,
            text_color=Theme.TEXT_MUTED,
            border_width=0,
            command=self._clear_input,
        ).pack(side="left", padx=(6, 0))

        # History divider
        ctk.CTkFrame(left, height=1, fg_color=Theme.BORDER).grid(
            row=3, column=0, padx=Theme.CARD_PAD, pady=(4, 6), sticky="ew"
        )

        # History title
        ctk.CTkLabel(
            left, text="🕒  Recent Scans",
            font=("Segoe UI", 11, "bold"), text_color=Theme.TEXT_SECONDARY,
        ).grid(row=4, column=0, padx=Theme.CARD_PAD, pady=(0, 3), sticky="w")

        # History scroll
        self._history_scroll = ctk.CTkScrollableFrame(
            left, fg_color="transparent",
            scrollbar_button_color=Theme.BG_INPUT,
            height=110,
        )
        self._history_scroll.grid(row=5, column=0, padx=Theme.CARD_PAD - 4,
                                   pady=(0, Theme.CARD_PAD), sticky="nsew")
        self._history_scroll.grid_columnconfigure(0, weight=1)

        # ── Right: Results panel ──────────────────────────────────────
        self._results_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_LG,
            border_width=1,
            border_color=Theme.BORDER,
            scrollbar_button_color=Theme.BG_INPUT,
            scrollbar_button_hover_color=Theme.ACCENT,
        )
        self._results_scroll.grid(row=1, column=1, padx=(Theme.PAD_SM, Theme.PAD_LG),
                                   pady=(0, Theme.PAD_LG), sticky="nsew")
        self._results_scroll.grid_columnconfigure(0, weight=1)
        self._show_results_placeholder()

    # ------------------------------------------------------------------

    def _run_analysis(self) -> None:
        text = self._textbox.get("1.0", "end").strip()
        if not text or text == "Paste the job offer text here…":
            self._show_error("Please paste a job offer text first.")
            return

        self._analyze_btn.configure(state="disabled", text="⏳  Analyzing…")
        self._clear_results()
        self._show_loading()

        def _process():
            return self._svc.analyze(text)

        def _done(result: DetectionResult):
            self.after(0, lambda r=result: self._finish_analysis(r))

        threading.Thread(
            target=lambda: _done(_process()), daemon=True
        ).start()

    def _finish_analysis(self, result: DetectionResult) -> None:
        self._analyze_btn.configure(state="normal", text="🔍  Analyze for Scam")
        self._show_results(result)
        self._load_history()

    def _show_results(self, result: DetectionResult) -> None:
        self._clear_results()

        # ── Suspicion gauge card ──────────────────────────────────────
        gauge_card = ctk.CTkFrame(
            self._results_scroll,
            fg_color=Theme.BG_DARK,
            corner_radius=Theme.RADIUS,
            border_width=2,
            border_color=result.level.color,
        )
        gauge_card.grid(row=0, column=0, padx=Theme.PAD,
                        pady=(Theme.PAD, Theme.PAD_SM), sticky="ew")
        gauge_card.grid_columnconfigure(0, weight=1)

        # Level label
        ctk.CTkLabel(
            gauge_card,
            text=f"{result.level.icon}  {result.level.label}",
            font=("Segoe UI", 20, "bold"),
            text_color=result.level.color,
        ).grid(row=0, column=0, padx=Theme.PAD, pady=(Theme.PAD, 2), sticky="w")

        ctk.CTkLabel(
            gauge_card,
            text=f"Suspicion Score: {result.suspicion_pct:.1f}%",
            font=Theme.FONT_BODY, text_color=Theme.TEXT_SECONDARY,
        ).grid(row=1, column=0, padx=Theme.PAD, pady=0, sticky="w")

        bar = ctk.CTkProgressBar(
            gauge_card, height=10, fg_color=Theme.BG_INPUT,
            progress_color=result.level.color, corner_radius=5,
        )
        bar.grid(row=2, column=0, padx=Theme.PAD, pady=(6, Theme.PAD), sticky="ew")
        bar.set(result.suspicion_pct / 100)

        # ── Recommendation card ───────────────────────────────────────
        rec_card = ctk.CTkFrame(
            self._results_scroll, fg_color=Theme.BG_DARK,
            corner_radius=Theme.RADIUS, border_width=1, border_color=Theme.BORDER,
        )
        rec_card.grid(row=1, column=0, padx=Theme.PAD, pady=Theme.PAD_SM, sticky="ew")
        rec_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            rec_card, text="💡  Recommendation",
            font=("Segoe UI", 10, "bold"), text_color=Theme.TEXT_MUTED,
        ).grid(row=0, column=0, padx=Theme.PAD, pady=(Theme.PAD_SM, 3), sticky="w")

        ctk.CTkLabel(
            rec_card, text=result.recommendation,
            font=Theme.FONT_BODY, text_color=Theme.TEXT_PRIMARY,
            wraplength=360, justify="left",
        ).grid(row=1, column=0, padx=Theme.PAD, pady=(0, Theme.PAD_SM), sticky="w")

        # ── Red flags card ────────────────────────────────────────────
        if result.top_flags:
            flags_card = ctk.CTkFrame(
                self._results_scroll, fg_color=Theme.BG_DARK,
                corner_radius=Theme.RADIUS, border_width=1, border_color=Theme.BORDER,
            )
            flags_card.grid(row=2, column=0, padx=Theme.PAD, pady=Theme.PAD_SM, sticky="ew")
            flags_card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                flags_card,
                text=f"⚠️  Detected Red Flags ({len(result.top_flags)})",
                font=("Segoe UI", 10, "bold"), text_color=Theme.WARNING,
            ).grid(row=0, column=0, padx=Theme.PAD, pady=(Theme.PAD_SM, 4), sticky="w")

            flags_inner = ctk.CTkFrame(flags_card, fg_color="transparent")
            flags_inner.grid(row=1, column=0, padx=Theme.PAD, pady=(0, Theme.PAD_SM), sticky="ew")

            for flag in result.top_flags[:10]:
                chip = ctk.CTkLabel(
                    flags_inner,
                    text=f"  ⚠ {flag[:60]}  ",
                    font=Theme.FONT_TINY,
                    fg_color=Theme.WARNING_BG,
                    text_color=Theme.WARNING,
                    corner_radius=4,
                )
                chip.pack(anchor="w", padx=0, pady=2)

    def _load_history(self) -> None:
        """Fetch past scam scan logs from service and render list items."""
        for w in self._history_scroll.winfo_children():
            w.destroy()
        self._history_items.clear()

        logs = self._svc.get_scam_history()
        if not logs:
            ctk.CTkLabel(
                self._history_scroll,
                text="No recent scans logged",
                font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
            ).pack(anchor="w", padx=8, pady=8)
            return

        for idx, entry in enumerate(logs[:6]):
            self._create_history_row(entry, idx)

    def _create_history_row(self, entry: dict, index: int) -> None:
        item = ctk.CTkFrame(
            self._history_scroll,
            fg_color=Theme.BG_INPUT,
            corner_radius=Theme.RADIUS_SM,
            cursor="hand2",
            height=34,
        )
        item.pack(fill="x", pady=2)
        item.pack_propagate(False)

        raw_level = entry["risk_level"]
        level = SuspicionLevel.from_string(raw_level)

        lbl_status = ctk.CTkLabel(
            item,
            text=f" {level.icon} {entry['suspicion_pct']:.0f}%",
            font=("Segoe UI", 9, "bold"),
            text_color=level.color,
            width=52,
        )
        lbl_status.pack(side="left", padx=(5, 4))

        preview = entry["job_text"].replace("\n", " ").strip()
        if len(preview) > 40:
            preview = preview[:37] + "…"

        lbl_preview = ctk.CTkLabel(
            item,
            text=preview,
            font=Theme.FONT_TINY,
            text_color=Theme.TEXT_PRIMARY,
            anchor="w",
        )
        lbl_preview.pack(side="left", fill="x", expand=True)

        def _click(e, ent=entry):
            self._textbox.delete("1.0", "end")
            self._textbox.insert("1.0", ent["job_text"])

            lvl = SuspicionLevel.from_string(ent["risk_level"])
            result = DetectionResult(
                level=lvl,
                suspicion_pct=ent["suspicion_pct"],
                raw_score=int(ent["suspicion_pct"] * 0.6),
                top_flags=ent["red_flags"],
                recommendation=lvl.advice,
            )
            self._show_results(result)

        def _enter(e, itm=item):
            itm.configure(fg_color=Theme.BG_HOVER)

        def _leave(e, itm=item):
            itm.configure(fg_color=Theme.BG_INPUT)

        for w in (item, lbl_status, lbl_preview):
            w.bind("<Button-1>", _click)
            w.bind("<Enter>", _enter)
            w.bind("<Leave>", _leave)

        self._history_items.append(item)

    def _show_loading(self) -> None:
        ctk.CTkLabel(
            self._results_scroll,
            text="⏳  Analyzing job offer…\nThis may take a few seconds.",
            font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED,
            justify="center",
        ).grid(row=0, column=0, padx=Theme.PAD, pady=Theme.PAD_LG * 3)

    def _show_results_placeholder(self) -> None:
        placeholder = ctk.CTkFrame(self._results_scroll, fg_color="transparent")
        placeholder.grid(row=0, column=0, padx=Theme.PAD, pady=60)

        ctk.CTkLabel(
            placeholder, text="🔍",
            font=("Segoe UI", 40),
        ).pack(pady=(0, 12))
        ctk.CTkLabel(
            placeholder,
            text="Paste a job offer and click Analyze",
            font=Theme.FONT_SUBTITLE,
            text_color=Theme.TEXT_SECONDARY,
        ).pack()
        ctk.CTkLabel(
            placeholder,
            text="AI will detect red flags, suspicion level & recommendations",
            font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED,
            justify="center",
        ).pack(pady=(4, 0))

    def _show_error(self, msg: str) -> None:
        self._clear_results()
        ctk.CTkLabel(
            self._results_scroll,
            text=f"⚠  {msg}",
            font=Theme.FONT_BODY, text_color=Theme.DANGER,
        ).grid(row=0, column=0, padx=Theme.PAD, pady=Theme.PAD_LG)

    def _clear_results(self) -> None:
        for w in self._results_scroll.winfo_children():
            w.destroy()

    def _clear_input(self) -> None:
        self._textbox.delete("1.0", "end")

    def _on_text_focus(self, e) -> None:
        if self._textbox.get("1.0", "end").strip() == "Paste the job offer text here…":
            self._textbox.delete("1.0", "end")
