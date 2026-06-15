"""
AegisAI — Sidebar Component
=============================
Left navigation sidebar with AegisAI logo and compact page nav buttons.
Width: 190px (reduced 20% from previous 210px for a sleeker look).
"""
from __future__ import annotations
import customtkinter as ctk
from ui.theme import Theme
from typing import Callable


class Sidebar(ctk.CTkFrame):
    """
    Left sidebar with branding and navigation buttons.

    Parameters
    ----------
    parent      : Parent widget
    navigate_cb : Callback(page_name: str) triggered on nav item click
    """

    def __init__(self, parent, navigate_cb: Callable[[str], None]) -> None:
        super().__init__(
            parent,
            width=Theme.SIDEBAR_W,
            fg_color=Theme.BG_SIDEBAR,
            corner_radius=0,
        )
        self._navigate_cb  = navigate_cb
        self._active_page  = "dashboard"
        self._nav_buttons: dict[str, dict] = {}
        self._build()

    # ------------------------------------------------------------------

    def _build(self) -> None:
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        # ── Logo Area ─────────────────────────────────────────────────
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=12, pady=(20, 6), sticky="ew")

        # Shield icon + brand name row
        logo_inner = ctk.CTkFrame(logo_frame, fg_color="transparent")
        logo_inner.pack(anchor="w")

        ctk.CTkLabel(
            logo_inner,
            text="🛡️",
            font=("Segoe UI", 22),
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            logo_inner,
            text="AegisAI",
            font=("Segoe UI", 17, "bold"),
            text_color=Theme.ACCENT,
        ).pack(side="left")

        ctk.CTkLabel(
            logo_frame,
            text="Anti-Trafficking Platform",
            font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 0))

        # Divider
        ctk.CTkFrame(self, height=1, fg_color=Theme.BORDER).grid(
            row=1, column=0, padx=12, pady=(6, 8), sticky="ew"
        )

        # ── Navigation Items ─────────────────────────────────────────
        nav_section_lbl = ctk.CTkLabel(
            self,
            text="NAVIGATION",
            font=("Segoe UI", 9, "bold"),
            text_color=Theme.TEXT_MUTED,
        )
        nav_section_lbl.grid(row=2, column=0, padx=14, pady=(0, 4), sticky="w")

        for idx, page in enumerate(Theme.NAV_ORDER):
            self._create_nav_item(page, row=idx + 3)

        # ── Version label at bottom ───────────────────────────────────
        self.grid_rowconfigure(20, weight=1)

        # Bottom divider
        ctk.CTkFrame(self, height=1, fg_color=Theme.BORDER).grid(
            row=21, column=0, padx=12, pady=(0, 8), sticky="ew"
        )

        ctk.CTkLabel(
            self,
            text="v2.0  ·  Academic Project",
            font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED,
        ).grid(row=22, column=0, padx=12, pady=(0, 14), sticky="sw")

    def _create_nav_item(self, page: str, row: int) -> None:
        """Create a single navigation row (indicator bar + icon + label)."""
        icon  = Theme.NAV_ICONS.get(page, "•")
        label = Theme.NAV_LABELS.get(page, page.title())

        # Container frame for the nav item
        item_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=Theme.RADIUS_SM,
            cursor="hand2",
        )
        item_frame.grid(row=row, column=0, padx=6, pady=1, sticky="ew")
        item_frame.grid_columnconfigure(2, weight=1)

        # Active indicator bar (3px left bar)
        indicator = ctk.CTkFrame(
            item_frame,
            width=3,
            height=28,
            fg_color="transparent",
            corner_radius=2,
        )
        indicator.grid(row=0, column=0, padx=(0, 0), pady=5, sticky="ns")
        indicator.grid_propagate(False)

        # Icon label
        icon_lbl = ctk.CTkLabel(
            item_frame,
            text=icon,
            font=("Segoe UI", 14),
            width=24,
            text_color=Theme.TEXT_SECONDARY,
        )
        icon_lbl.grid(row=0, column=1, padx=(6, 4), pady=7)

        # Text label
        text_lbl = ctk.CTkLabel(
            item_frame,
            text=label,
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_SECONDARY,
            anchor="w",
        )
        text_lbl.grid(row=0, column=2, padx=(0, 6), pady=7, sticky="w")

        # Click and hover bindings
        def _click(e, p=page):
            self.set_active(p)
            self._navigate_cb(p)

        def _enter(e, f=item_frame):
            if self._active_page != page:
                f.configure(fg_color=Theme.BG_HOVER)

        def _leave(e, f=item_frame):
            if self._active_page != page:
                f.configure(fg_color="transparent")

        for widget in (item_frame, icon_lbl, text_lbl, indicator):
            widget.bind("<Button-1>", _click)
            widget.bind("<Enter>", _enter)
            widget.bind("<Leave>", _leave)

        # Store references for active-state management
        self._nav_buttons[page] = {
            "frame":     item_frame,
            "indicator": indicator,
            "text_lbl":  text_lbl,
            "icon_lbl":  icon_lbl,
        }

    # ------------------------------------------------------------------

    def set_active(self, page: str) -> None:
        """Highlight the active nav item and un-highlight others."""
        for p, widgets in self._nav_buttons.items():
            is_active = (p == page)
            widgets["frame"].configure(
                fg_color=Theme.BG_ACTIVE if is_active else "transparent"
            )
            widgets["indicator"].configure(
                fg_color=Theme.ACCENT_MUTED if is_active else "transparent"
            )
            widgets["text_lbl"].configure(
                text_color=Theme.TEXT_ACCENT if is_active else Theme.TEXT_SECONDARY,
                font=("Segoe UI", 11, "bold") if is_active else Theme.FONT_SMALL,
            )
            widgets["icon_lbl"].configure(
                text_color=Theme.ACCENT if is_active else Theme.TEXT_SECONDARY,
            )
        self._active_page = page

    def flash_emergency(self) -> None:
        """Highlight emergency nav item in red for SOS events."""
        if "emergency" in self._nav_buttons:
            widgets = self._nav_buttons["emergency"]
            widgets["frame"].configure(fg_color=Theme.DANGER_BG)
            widgets["indicator"].configure(fg_color=Theme.DANGER)
            widgets["text_lbl"].configure(text_color=Theme.DANGER)
            widgets["icon_lbl"].configure(text_color=Theme.DANGER)
