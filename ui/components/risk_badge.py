"""
AegisAI — Risk Badge Component
================================
Coloured pill badge displaying the current risk level.
"""
from __future__ import annotations
import customtkinter as ctk
from ui.theme import Theme
from models.assessment import RiskLevel


class RiskBadge(ctk.CTkLabel):
    """
    Coloured pill label showing risk level emoji + text.

    Call update(level) to change the displayed level.
    """

    def __init__(self, parent, level: RiskLevel = RiskLevel.UNKNOWN) -> None:
        super().__init__(
            parent,
            text="",
            font=Theme.FONT_SMALL,
            corner_radius=Theme.RADIUS_SM,
            padx=12,
            pady=4,
        )
        self.update(level)

    def update(self, level: RiskLevel) -> None:
        """Refresh the badge to reflect a new risk level."""
        bg_map = {
            RiskLevel.UNKNOWN:  Theme.BG_INPUT,
            RiskLevel.LOW:      Theme.SUCCESS_BG,
            RiskLevel.MEDIUM:   Theme.WARNING_BG,
            RiskLevel.HIGH:     Theme.DANGER_BG,
            RiskLevel.CRITICAL: Theme.CRITICAL_BG,
        }
        self.configure(
            text=f" {level.emoji}  {level.label} ",
            text_color=level.color,
            fg_color=bg_map.get(level, Theme.BG_INPUT),
        )
