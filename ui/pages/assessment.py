"""
AegisAI — Risk Assessment Page
=================================
6-step guided wizard with progress bar, question cards,
live risk gauge, and final professional report.
"""
from __future__ import annotations

import threading
import logging
from typing import Optional

import customtkinter as ctk
from ui.theme import Theme
from ui.components.risk_badge import RiskBadge
from models.assessment import RiskLevel, AssessmentResult
from services.assessment_service import TOTAL_QUESTIONS, TOTAL_STEPS

log = logging.getLogger(__name__)


class AssessmentPage(ctk.CTkFrame):
    """
    Risk assessment wizard page.

    Parameters
    ----------
    parent             : Parent widget
    assessment_service : AssessmentService instance
    session_service    : SessionService instance
    """

    def __init__(self, parent, assessment_service, session_service) -> None:
        super().__init__(parent, fg_color=Theme.BG_DARK, corner_radius=0)
        self._svc  = assessment_service
        self._sess = session_service
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

        # Hero icon
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
                "Your answers are private and not stored anywhere."
            ),
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_SECONDARY,
            justify="center",
        ).pack(pady=(8, 28))

        # Info chips row
        chips_row = ctk.CTkFrame(center, fg_color="transparent")
        chips_row.pack(pady=(0, 24))
        for info in ["15 Questions", "6 Steps", "~3 Minutes", "Confidential"]:
            ctk.CTkLabel(
                chips_row,
                text=f"  {info}  ",
                font=Theme.FONT_TINY,
                text_color=Theme.TEXT_ACCENT,
                fg_color=Theme.BG_CARD,
                corner_radius=Theme.RADIUS_SM,
            ).pack(side="left", padx=4, ipady=4)

        ctk.CTkButton(
            center,
            text="▶   Start Assessment",
            font=("Segoe UI", 13, "bold"),
            width=210,
            height=44,
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
        inner.grid(row=0, column=0, padx=Theme.PAD_LG, pady=(Theme.PAD, Theme.PAD_SM), sticky="ew")
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
            prog_frame,
            width=0, height=4,
            fg_color=Theme.BG_INPUT,
            progress_color=Theme.ACCENT,
            corner_radius=2,
        )
        self._prog_bar.grid(row=1, column=0, sticky="ew")
        self._prog_bar.set(0)

        # ── Two-column layout: question left, live gauge right ─────────
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=2, column=0, padx=Theme.PAD_LG, pady=Theme.PAD_LG, sticky="nsew")
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
        ).grid(row=0, column=0, padx=Theme.CARD_PAD, pady=(Theme.CARD_PAD, 4), sticky="w")

        self._q_text = ctk.CTkLabel(
            left, text="",
            font=("Segoe UI", 14),
            text_color=Theme.TEXT_PRIMARY,
            wraplength=520, justify="left", anchor="nw",
        )
        self._q_text.grid(row=1, column=0, padx=Theme.CARD_PAD, pady=(0, Theme.PAD), sticky="nw")

        # Answer buttons row
        btn_frame = ctk.CTkFrame(left, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=Theme.CARD_PAD, pady=Theme.CARD_PAD, sticky="ew")

        answer_options = [
            ("✅  Yes",      "yes",  Theme.SUCCESS),
            ("❌  No",       "no",   Theme.DANGER),
            ("❓  Not Sure", "no",   Theme.WARNING),
        ]
        for label, value, color in answer_options:
            ctk.CTkButton(
                btn_frame,
                text=label,
                font=Theme.FONT_SMALL,
                width=110,
                height=38,
                fg_color=Theme.BG_INPUT,
                hover_color=color,
                text_color=color,
                border_color=color,
                border_width=1,
                corner_radius=Theme.RADIUS,
                command=lambda v=value: self._answer(v),
            ).pack(side="left", padx=(0, 8))

        # Abort button
        ctk.CTkButton(
            left, text="✖  Abort",
            font=Theme.FONT_TINY, width=72, height=26,
            fg_color="transparent", hover_color=Theme.BG_HOVER,
            text_color=Theme.TEXT_MUTED, border_width=0,
            command=self._build_idle,
        ).grid(row=3, column=0, padx=Theme.CARD_PAD, pady=(0, Theme.PAD_SM), sticky="e")

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
            font=("Segoe UI", 34, "bold"), text_color=Theme.SUCCESS,
        )
        self._gauge_pct_lbl.grid(row=1, column=0, padx=Theme.PAD, pady=6)

        self._gauge_bar = ctk.CTkProgressBar(
            right, width=24, height=120,
            fg_color=Theme.BG_INPUT, progress_color=Theme.SUCCESS,
            corner_radius=6, orientation="vertical",
        )
        self._gauge_bar.grid(row=2, column=0, padx=Theme.PAD, pady=6)
        self._gauge_bar.set(0)

        self._gauge_badge = RiskBadge(right, RiskLevel.UNKNOWN)
        self._gauge_badge.grid(row=3, column=0, padx=Theme.PAD, pady=(4, Theme.PAD_SM))

        self._answers_lbl = ctk.CTkLabel(
            right, text="0 / 15",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        )
        self._answers_lbl.grid(row=4, column=0, padx=Theme.PAD, pady=(0, Theme.PAD))

        # Load first question
        self._refresh_ui()

    def _build_result(self, result: AssessmentResult) -> None:
        """Show the final assessment report."""
        self._clear()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        scroll = ctk.CTkScrollableFrame(
            self, fg_color=Theme.BG_DARK, corner_radius=0,
            scrollbar_button_color=Theme.BG_INPUT,
            scrollbar_button_hover_color=Theme.ACCENT,
        )
        scroll.grid(row=0, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        # Result header card
        header = ctk.CTkFrame(
            scroll, fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_LG,
            border_width=2, border_color=result.risk_level.color,
        )
        header.grid(row=0, column=0, padx=Theme.PAD_LG,
                    pady=(Theme.PAD_LG, Theme.PAD), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text="ASSESSMENT COMPLETE",
            font=("Segoe UI", 9, "bold"), text_color=Theme.TEXT_MUTED,
        ).grid(row=0, column=0, padx=Theme.CARD_PAD, pady=(Theme.CARD_PAD, 4), sticky="w")

        ctk.CTkLabel(
            header, text=f"{result.risk_level.emoji}  {result.risk_level.label}",
            font=("Segoe UI", 28, "bold"), text_color=result.risk_level.color,
        ).grid(row=1, column=0, padx=Theme.CARD_PAD, pady=0, sticky="w")

        ctk.CTkLabel(
            header,
            text=f"Risk Score: {result.risk_score}  ·  Suspicion: {result.risk_pct:.1f}%",
            font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY,
        ).grid(row=2, column=0, padx=Theme.CARD_PAD, pady=(2, 6), sticky="w")

        score_bar = ctk.CTkProgressBar(
            header, height=8, fg_color=Theme.BG_INPUT,
            progress_color=result.risk_level.color, corner_radius=4,
        )
        score_bar.grid(row=3, column=0, padx=Theme.CARD_PAD,
                       pady=(0, Theme.CARD_PAD), sticky="ew")
        score_bar.set(min(result.risk_pct / 100, 1.0))

        # Summary
        ctk.CTkLabel(
            scroll, text=result.summary,
            font=Theme.FONT_BODY, text_color=Theme.TEXT_PRIMARY,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, padx=Theme.PAD_LG, pady=(0, Theme.PAD), sticky="w")

        # Recommendations card
        rec_card = ctk.CTkFrame(
            scroll, fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_LG,
            border_width=1, border_color=Theme.BORDER,
        )
        rec_card.grid(row=2, column=0, padx=Theme.PAD_LG, pady=(0, Theme.PAD), sticky="ew")
        rec_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            rec_card, text="📋  Recommendations",
            font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=Theme.CARD_PAD,
               pady=(Theme.CARD_PAD, 8), sticky="w")

        for i, rec in enumerate(result.recommendations):
            row_frame = ctk.CTkFrame(rec_card, fg_color="transparent")
            row_frame.grid(row=i + 1, column=0, padx=Theme.CARD_PAD, pady=2, sticky="ew")
            row_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                row_frame, text="›",
                font=("Segoe UI", 14, "bold"), text_color=Theme.ACCENT, width=16,
            ).grid(row=0, column=0, padx=(0, 6), sticky="w")

            ctk.CTkLabel(
                row_frame, text=rec,
                font=Theme.FONT_BODY, text_color=Theme.TEXT_PRIMARY,
                anchor="w", justify="left", wraplength=660,
            ).grid(row=0, column=1, sticky="w")

        ctk.CTkFrame(rec_card, height=1, fg_color=Theme.BORDER).grid(
            row=100, column=0, padx=Theme.CARD_PAD, pady=Theme.PAD_SM, sticky="ew"
        )

        # Restart button
        ctk.CTkButton(
            scroll, text="↺  Take Assessment Again",
            font=Theme.FONT_SMALL, width=210, height=40,
            fg_color=Theme.BG_CARD, hover_color=Theme.BG_HOVER,
            text_color=Theme.ACCENT, border_color=Theme.BORDER_ACCENT,
            border_width=1, corner_radius=Theme.RADIUS,
            command=self._build_idle,
        ).grid(row=3, column=0, padx=Theme.PAD_LG, pady=Theme.PAD_LG)

    # ------------------------------------------------------------------

    def _start(self) -> None:
        self._svc.start()
        self._sess.start_assessment()
        self._build_wizard()

    def _answer(self, response: str) -> None:
        result = self._svc.answer(response)
        if isinstance(result, AssessmentResult):
            self._sess.complete_assessment(result)
            self._build_result(result)
        else:
            self._refresh_ui()
            partial = self._svc.get_partial_result()
            if partial:
                self._update_gauge(partial)

    def _refresh_ui(self) -> None:
        q_num, total_q, step, pct = self._svc.get_progress()
        q = self._svc.current_question
        if not q:
            return
        step_name = q.step_name
        self._step_lbl.configure(text=f"Step {step} of {TOTAL_STEPS}  —  {step_name}")
        self._q_lbl.configure(text=f"Q {q_num} of {total_q}")
        self._q_text.configure(text=q.text)
        self._prog_bar.set(pct / 100)
        self._answers_lbl.configure(text=f"{q_num - 1} / {total_q}")

    def _update_gauge(self, result: AssessmentResult) -> None:
        pct   = result.risk_pct
        level = result.risk_level
        color = level.color
        self._gauge_pct_lbl.configure(text=f"{pct:.0f}%", text_color=color)
        self._gauge_bar.configure(progress_color=color)
        self._gauge_bar.set(pct / 100)
        self._gauge_badge.update(level)

    def _clear(self) -> None:
        for w in self.winfo_children():
            w.destroy()
