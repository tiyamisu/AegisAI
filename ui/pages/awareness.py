"""
AegisAI — Awareness Center Page
==================================
Browse 13 KB topic categories in a compact card grid.
Click any card to read the full content in the right panel.
"""
from __future__ import annotations
import customtkinter as ctk
from ui.theme import Theme
from typing import List

# Topic metadata: (key, icon, title, description)
TOPICS = [
    ("human_trafficking_basics", "📖", "Trafficking Basics",   "Definition, types & global statistics"),
    ("warning_signs",            "⚠️", "Warning Signs",        "Red flags to recognise trafficking"),
    ("recruitment_scams",        "💼", "Recruitment Scams",    "Fake job offers and fraud tactics"),
    ("child_trafficking",        "👶", "Child Trafficking",    "POCSO, Childline & protection laws"),
    ("forced_labour",            "⛓️", "Forced Labour",        "Bonded labour, debt bondage & rights"),
    ("online_grooming",          "💻", "Online Grooming",      "Social media dangers & catfishing"),
    ("victim_support",           "🤝", "Victim Support",       "Counselling, rehab & survivor stories"),
    ("emergency_assistance",     "🆘", "Emergency Assistance", "Escape plans & shelter access"),
    ("reporting_procedures",     "📝", "Reporting Procedures", "FIR, NHRC & cybercrime filing"),
    ("legal_rights",             "⚖️", "Legal Rights",         "ITPA, POCSO & victim compensation"),
    ("safety_measures",          "🔒", "Safety Measures",      "Travel, online & job safety tips"),
    ("ngo_support",              "🏥", "NGO Support",          "IJM, Prerana & support organisations"),
    ("faqs",                     "❓", "FAQs",                 "Common questions & misconceptions"),
]


class AwarenessPage(ctk.CTkFrame):
    """Topic browser with compact grid of cards and detail panel."""

    def __init__(self, parent, kb_manager) -> None:
        super().__init__(parent, fg_color=Theme.BG_DARK, corner_radius=0)
        self._kb = kb_manager
        self._cards: List[dict] = []
        self._build()

    def _build(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ── Title bar ─────────────────────────────────────────────────
        title_bar = ctk.CTkFrame(self, fg_color="transparent")
        title_bar.grid(row=0, column=0, columnspan=2, padx=Theme.PAD_LG,
                       pady=(Theme.PAD, Theme.PAD_SM), sticky="ew")
        title_bar.grid_columnconfigure(0, weight=1)

        left_title = ctk.CTkFrame(title_bar, fg_color="transparent")
        left_title.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            left_title, text="📚  Awareness Center",
            font=Theme.FONT_TITLE, text_color=Theme.TEXT_PRIMARY,
        ).pack(anchor="w")
        ctk.CTkLabel(
            left_title, text=f"Browse {len(TOPICS)} topics on human trafficking prevention",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 0))

        # Topic count badge
        ctk.CTkLabel(
            title_bar,
            text=f"  {len(TOPICS)} Topics  ",
            font=Theme.FONT_TINY,
            text_color=Theme.ACCENT,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_SM,
        ).grid(row=0, column=1, sticky="e", padx=(0, 0), ipady=4)

        # ── Left: topic grid (2-column, scrollable) ───────────────────
        left = ctk.CTkScrollableFrame(
            self, fg_color="transparent", width=330,
            scrollbar_button_color=Theme.BG_INPUT,
            scrollbar_button_hover_color=Theme.ACCENT,
        )
        left.grid(row=1, column=0, padx=(Theme.PAD_LG, Theme.PAD_SM),
                  pady=(0, Theme.PAD_LG), sticky="nsew")
        left.grid_columnconfigure((0, 1), weight=1)

        self._cards = []
        for idx, (key, icon, title, desc) in enumerate(TOPICS):
            col = idx % 2
            row = idx // 2
            self._make_topic_card(left, key, icon, title, desc, row, col)

        # ── Right: detail panel ───────────────────────────────────────
        self._detail = ctk.CTkScrollableFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_LG,
            border_width=1,
            border_color=Theme.BORDER,
            scrollbar_button_color=Theme.BG_INPUT,
            scrollbar_button_hover_color=Theme.ACCENT,
        )
        self._detail.grid(row=1, column=1, padx=(0, Theme.PAD_LG),
                          pady=(0, Theme.PAD_LG), sticky="nsew")
        self._detail.grid_columnconfigure(0, weight=1)

        # Placeholder
        placeholder = ctk.CTkFrame(self._detail, fg_color="transparent")
        placeholder.grid(row=0, column=0, padx=Theme.PAD_LG, pady=60)

        ctk.CTkLabel(
            placeholder,
            text="📖",
            font=("Segoe UI", 40),
        ).pack(pady=(0, 12))
        ctk.CTkLabel(
            placeholder,
            text="Select a topic on the left",
            font=Theme.FONT_SUBTITLE,
            text_color=Theme.TEXT_SECONDARY,
        ).pack()
        ctk.CTkLabel(
            placeholder,
            text="Click any card to read detailed information",
            font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED,
        ).pack(pady=(4, 0))

    def _make_topic_card(self, parent, key, icon, title, desc, row, col):
        card_data = {}
        card = ctk.CTkFrame(
            parent,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS,
            border_width=1,
            border_color=Theme.BORDER,
            cursor="hand2",
        )
        card.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        card_data["frame"] = card

        # Icon
        ctk.CTkLabel(
            card, text=icon, font=("Segoe UI", 20),
        ).pack(anchor="w", padx=Theme.PAD_SM, pady=(Theme.PAD_SM, 2))

        # Title
        ctk.CTkLabel(
            card, text=title,
            font=("Segoe UI", 11, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            wraplength=130, justify="left",
        ).pack(anchor="w", padx=Theme.PAD_SM)

        # Description
        ctk.CTkLabel(
            card, text=desc,
            font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED,
            wraplength=130, justify="left",
        ).pack(anchor="w", padx=Theme.PAD_SM, pady=(1, Theme.PAD_SM))

        self._cards.append(card_data)

        def _click(e, k=key, t=title, i=icon, c=card):
            # Deselect all cards
            for cd in self._cards:
                cd["frame"].configure(border_color=Theme.BORDER, fg_color=Theme.BG_CARD)
            # Highlight selected
            c.configure(border_color=Theme.ACCENT, fg_color=Theme.BG_ACTIVE)
            self._show_detail(k, t, i)

        card.bind("<Button-1>", _click)
        for w in card.winfo_children():
            w.bind("<Button-1>", _click)

    def _show_detail(self, key: str, title: str, icon: str) -> None:
        """Load and display topic content in the detail panel."""
        for w in self._detail.winfo_children():
            w.destroy()

        # Detail header
        header = ctk.CTkFrame(self._detail, fg_color="transparent")
        header.grid(row=0, column=0, padx=Theme.PAD_LG, pady=(Theme.PAD_LG, 0), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text=f"{icon}  {title}",
            font=Theme.FONT_TITLE, text_color=Theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkFrame(self._detail, height=1, fg_color=Theme.BORDER_ACCENT).grid(
            row=1, column=0, padx=Theme.PAD_LG, pady=(Theme.PAD_SM, Theme.PAD), sticky="ew"
        )

        # Fetch content from KB
        results = self._kb.get_by_category(key)
        if results:
            for ridx, r in enumerate(results[:6]):
                content_card = ctk.CTkFrame(
                    self._detail,
                    fg_color=Theme.BG_DARK,
                    corner_radius=Theme.RADIUS_SM,
                    border_width=0,
                )
                content_card.grid(row=ridx + 2, column=0, padx=Theme.PAD_LG,
                                  pady=(0, 8), sticky="ew")
                content_card.grid_columnconfigure(0, weight=1)

                # Accent left border via a colored strip
                accent_strip = ctk.CTkFrame(
                    content_card, width=3, fg_color=Theme.ACCENT_MUTED, corner_radius=2,
                )
                accent_strip.grid(row=0, column=0, padx=(0, 0), pady=8, sticky="ns")
                accent_strip.grid_propagate(False)

                ctk.CTkLabel(
                    content_card,
                    text=r.response,
                    font=Theme.FONT_BODY,
                    text_color=Theme.TEXT_PRIMARY,
                    wraplength=480,
                    justify="left",
                    anchor="w",
                ).grid(row=0, column=1, padx=(8, Theme.PAD_SM), pady=Theme.PAD_SM, sticky="w")
        else:
            ctk.CTkLabel(
                self._detail,
                text="📭  Content not available yet.\nPlease check back later.",
                font=Theme.FONT_BODY,
                text_color=Theme.TEXT_MUTED,
                justify="center",
            ).grid(row=2, column=0, padx=Theme.PAD_LG, pady=Theme.PAD_LG * 3)
