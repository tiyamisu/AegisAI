"""
AegisAI — Dashboard Page
==========================
Home page with compact hero section, metric stat cards, and the main chat interface.
The chat area takes the majority of the vertical space.
"""
from __future__ import annotations
import customtkinter as ctk
from ui.theme import Theme
from ui.components.stat_card import StatCard
from ui.components.chat_widget import ChatWidget
from models.message import ChatMessage
from typing import Callable


class DashboardPage(ctk.CTkFrame):
    """
    Main dashboard — compact hero banner + stats row + embedded AI chat.

    Parameters
    ----------
    parent       : Parent widget
    chat_service : ChatService instance for sending messages
    kb_stats     : dict from KBManager.stats()
    """

    def __init__(self, parent, chat_service, kb_stats: dict) -> None:
        super().__init__(parent, fg_color=Theme.BG_DARK, corner_radius=0)
        self._chat_svc = chat_service
        self._kb_stats = kb_stats
        self._build()

    def _build(self) -> None:
        # Row 0: hero (fixed) | Row 1: stats (fixed) | Row 2: chat (expands)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Hero Section (compact) ────────────────────────────────────
        hero = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_LG,
            border_width=1,
            border_color=Theme.BORDER_ACCENT,
        )
        hero.grid(row=0, column=0, padx=Theme.PAD_LG, pady=(Theme.PAD, 0), sticky="ew")
        hero.grid_columnconfigure(0, weight=1)

        # Left content
        hero_left = ctk.CTkFrame(hero, fg_color="transparent")
        hero_left.grid(row=0, column=0, padx=Theme.PAD_LG, pady=Theme.PAD, sticky="w")

        ctk.CTkLabel(
            hero_left,
            text="🛡️  Welcome to AegisAI",
            font=Theme.FONT_HERO,
            text_color=Theme.TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            hero_left,
            text=(
                "AI-Powered Human Trafficking Prevention & Victim Assistance Platform  —  "
                "Ask me anything below."
            ),
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_SECONDARY,
            justify="left",
            wraplength=680,
        ).pack(anchor="w", pady=(3, 0))

        # Right badge
        badge_frame = ctk.CTkFrame(
            hero,
            fg_color=Theme.ACCENT_MUTED,
            corner_radius=Theme.RADIUS_SM,
        )
        badge_frame.grid(row=0, column=1, padx=Theme.PAD_LG, pady=Theme.PAD)

        ctk.CTkLabel(
            badge_frame,
            text="AI\nActive",
            font=("Segoe UI", 10, "bold"),
            text_color="#ffffff",
            justify="center",
        ).pack(padx=12, pady=8)

        # ── Stat Cards Row ────────────────────────────────────────────
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.grid(row=1, column=0, padx=Theme.PAD_LG, pady=(Theme.PAD_SM, 0), sticky="ew")

        total_kb  = self._kb_stats.get("total_entries", 105)
        cards_cfg = [
            ("📚", str(total_kb), "KB Entries",      Theme.ACCENT),
            ("⚙️", "52",          "Expert Rules",    Theme.SUCCESS),
            ("🔍", "110",         "Scam Indicators", Theme.DANGER),
            ("📋", "15",          "Risk Questions",  Theme.TEXT_ACCENT),
        ]
        for idx, (icon, val, lbl, color) in enumerate(cards_cfg):
            card = StatCard(stats_frame, icon, val, lbl, color)
            card.grid(row=0, column=idx, padx=(0 if idx == 0 else 10, 0), pady=0, sticky="nsew")
            stats_frame.grid_columnconfigure(idx, weight=1)

        # ── Chat Widget (main focus — takes remaining space) ──────────
        welcome = self._chat_svc.get_welcome()
        self._chat = ChatWidget(
            self,
            send_cb=self._chat_svc.send,
            welcome_msg=welcome,
        )
        self._chat.grid(
            row=2, column=0,
            padx=Theme.PAD_LG, pady=(Theme.PAD_SM, Theme.PAD_LG),
            sticky="nsew",
        )

    def inject_query(self, query: str) -> None:
        """Programmatically send a query into the chat (e.g., from sidebar)."""
        self._chat.inject_message(query)
