"""
AegisAI — Header Component
============================
Top application header bar showing current page title,
risk level badge, and SOS emergency button.
"""
from __future__ import annotations
import customtkinter as ctk
from ui.theme import Theme
from models.assessment import RiskLevel
from typing import Callable


class Header(ctk.CTkFrame):
    """
    Fixed top header bar.

    Parameters
    ----------
    parent      : Parent widget
    on_sos      : Callback() triggered when SOS button is clicked
    """

    def __init__(self, parent, on_sos: Callable[[], None]) -> None:
        super().__init__(
            parent,
            height=Theme.HEADER_H,
            fg_color=Theme.BG_HEADER,
            corner_radius=0,
        )
        self._on_sos = on_sos
        self._build()

    def _build(self) -> None:
        self.grid_propagate(False)
        self.grid_columnconfigure(1, weight=1)

        # Left: App brand + page breadcrumb
        left = ctk.CTkFrame(self, fg_color="transparent")
        left.grid(row=0, column=0, padx=(Theme.PAD_LG, 0), pady=0, sticky="w")

        ctk.CTkLabel(
            left,
            text="🛡️  AegisAI",
            font=("Segoe UI", 13, "bold"),
            text_color=Theme.ACCENT,
        ).pack(side="left", padx=(0, 8))

        # Separator character
        ctk.CTkLabel(
            left,
            text="›",
            font=("Segoe UI", 13),
            text_color=Theme.TEXT_MUTED,
        ).pack(side="left", padx=(0, 8))

        # Current page title
        self._title_lbl = ctk.CTkLabel(
            left,
            text="Dashboard",
            font=("Segoe UI", 13, "bold"),
            text_color=Theme.TEXT_PRIMARY,
        )
        self._title_lbl.pack(side="left")

        # Right: Risk badge + SOS button
        right = ctk.CTkFrame(self, fg_color="transparent")
        right.grid(row=0, column=2, padx=Theme.PAD, pady=0, sticky="e")

        # Risk level badge
        self._risk_badge = ctk.CTkLabel(
            right,
            text=f"  {RiskLevel.UNKNOWN.emoji}  {RiskLevel.UNKNOWN.label}  ",
            font=Theme.FONT_TINY,
            text_color=Theme.TEXT_SECONDARY,
            fg_color=Theme.BG_INPUT,
            corner_radius=Theme.RADIUS_SM,
        )
        self._risk_badge.pack(side="left", padx=(0, 10), ipady=3)

        # SOS button (always visible)
        self._sos_btn = ctk.CTkButton(
            right,
            text="🆘  SOS",
            font=("Segoe UI", 11, "bold"),
            width=76,
            height=30,
            fg_color=Theme.DANGER,
            hover_color="#B91C1C",
            corner_radius=Theme.RADIUS_SM,
            command=self._on_sos,
        )
        self._sos_btn.pack(side="left")

        # Bottom border
        ctk.CTkFrame(self, height=1, fg_color=Theme.BORDER).grid(
            row=1, column=0, columnspan=3, sticky="ew"
        )
        self.grid_rowconfigure(0, weight=1)

    # ------------------------------------------------------------------

    def set_title(self, title: str) -> None:
        """Update the page title text in the header breadcrumb."""
        self._title_lbl.configure(text=title)

    def set_risk(self, level: RiskLevel) -> None:
        """Update the risk level badge colour and text with semantic tints."""
        bg_colors = {
            RiskLevel.UNKNOWN:  Theme.BG_INPUT,
            RiskLevel.LOW:      Theme.SUCCESS_BG,
            RiskLevel.MEDIUM:   Theme.WARNING_BG,
            RiskLevel.HIGH:     Theme.DANGER_BG,
            RiskLevel.CRITICAL: Theme.CRITICAL_BG,
        }
        fg_colors = {
            RiskLevel.UNKNOWN:  Theme.TEXT_SECONDARY,
            RiskLevel.LOW:      Theme.SUCCESS,
            RiskLevel.MEDIUM:   Theme.WARNING,
            RiskLevel.HIGH:     Theme.DANGER,
            RiskLevel.CRITICAL: Theme.CRITICAL,
        }

        bg_color = bg_colors.get(level, Theme.BG_INPUT)
        fg_color = fg_colors.get(level, Theme.TEXT_SECONDARY)

        self._risk_badge.configure(
            text=f"  {level.emoji}  {level.label}  ",
            text_color=fg_color,
            fg_color=bg_color,
        )

    def flash_sos(self) -> None:
        """Briefly animate the SOS button to draw attention."""
        original = Theme.DANGER
        self._sos_btn.configure(fg_color=Theme.CRITICAL)
        self.after(300, lambda: self._sos_btn.configure(fg_color=original))
