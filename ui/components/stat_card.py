"""
AegisAI — Stat Card Component
================================
A compact metric display card showing an icon, large number, and label.
Used on the dashboard for KB entries, rules, indicators, etc.
"""
from __future__ import annotations
import customtkinter as ctk
from ui.theme import Theme


class StatCard(ctk.CTkFrame):
    """
    A compact info card displaying a single metric.

    Parameters
    ----------
    parent : Parent widget
    icon   : Emoji icon (e.g. "📚")
    value  : Metric value string (e.g. "105")
    label  : Description label (e.g. "KB Entries")
    color  : Accent color for the icon and value (defaults to ACCENT)
    """

    def __init__(
        self,
        parent,
        icon: str,
        value: str,
        label: str,
        color: str = Theme.ACCENT,
    ) -> None:
        super().__init__(
            parent,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS,
            border_width=1,
            border_color=Theme.BORDER,
        )
        self._build(icon, value, label, color)

    def _build(self, icon: str, value: str, label: str, color: str) -> None:
        self.grid_columnconfigure(0, weight=1)

        # Top row: icon + value side-by-side for compactness
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, padx=Theme.CARD_PAD, pady=(Theme.CARD_PAD, 2), sticky="w")

        ctk.CTkLabel(
            top,
            text=icon,
            font=("Segoe UI", 20),
            text_color=color,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            top,
            text=value,
            font=("Segoe UI", 20, "bold"),
            text_color=color,
        ).pack(side="left")

        # Label below
        ctk.CTkLabel(
            self,
            text=label,
            font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED,
        ).grid(row=1, column=0, padx=Theme.CARD_PAD, pady=(0, Theme.CARD_PAD - 4), sticky="w")

        # Bottom accent stripe
        ctk.CTkFrame(
            self, height=2, fg_color=color, corner_radius=0,
        ).grid(row=2, column=0, padx=0, pady=0, sticky="ew")
