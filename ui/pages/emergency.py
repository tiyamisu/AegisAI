"""
AegisAI — Emergency Help Page
================================
High-visibility emergency helplines, escape guidance,
and silent distress signal information.
"""
from __future__ import annotations
import customtkinter as ctk
from ui.theme import Theme


HELPLINES = [
    ("🚔", "Police",            "100",   "Immediate police response",               Theme.DANGER),
    ("🆘", "National Emergency","112",   "All emergencies — police/fire/medical",   Theme.DANGER),
    ("👶", "Childline",         "1098",  "Child trafficking & abuse (24/7)",        Theme.WARNING),
    ("👩", "Women's Helpline",  "1091",  "Women in distress (24/7)",                Theme.WARNING),
    ("📞", "Anti-Trafficking",  "14433", "NHRC trafficking helpline",               Theme.ACCENT),
    ("💻", "Cybercrime",        "1930",  "Online crimes & fraud",                   Theme.ACCENT),
    ("🏥", "Ambulance",         "108",   "Medical emergencies",                     Theme.SUCCESS),
    ("🌐", "Missing Persons",   "1094",  "Track missing persons",                   Theme.SUCCESS),
]

ESCAPE_STEPS = [
    ("Stay calm",                "Take a slow breath. Panic makes escape harder. Think clearly."),
    ("Memorise the exits",       "Identify all possible ways out — doors, windows, vehicles."),
    ("Signal for help",          "If someone trustworthy is nearby, use the thumbs-down signal or mouth 'HELP'."),
    ("Contact a helper",         "If you have a phone, call 100 (Police) or 112. Even a short call helps."),
    ("Leave without confrontation", "Do not argue. Pick a moment when your captor is distracted."),
    ("Reach a safe place",       "Police station, hospital, NGO shelter, or a crowd of people."),
    ("Report immediately",       "Tell the police everything — describe your captors and location."),
]


class EmergencyPage(ctk.CTkFrame):
    """Emergency help page with helplines and escape guidance."""

    def __init__(self, parent) -> None:
        super().__init__(parent, fg_color=Theme.BG_DARK, corner_radius=0)
        self._build()

    def _build(self) -> None:
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Emergency banner ──────────────────────────────────────────
        banner = ctk.CTkFrame(
            self,
            fg_color=Theme.CRITICAL_BG,
            corner_radius=0,
            border_width=0,
        )
        banner.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        banner.grid_columnconfigure(0, weight=1)

        # Banner inner layout
        banner_inner = ctk.CTkFrame(banner, fg_color="transparent")
        banner_inner.grid(row=0, column=0, padx=Theme.PAD_LG, pady=(Theme.PAD, Theme.PAD), sticky="ew")
        banner_inner.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            banner_inner,
            text="🚨   EMERGENCY ASSISTANCE   🚨",
            font=("Segoe UI", 18, "bold"),
            text_color=Theme.CRITICAL,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            banner_inner,
            text="If you are in immediate danger — CALL 100 (Police) or 112 (Emergency) RIGHT NOW",
            font=("Segoe UI", 12),
            text_color=Theme.TEXT_PRIMARY,
        ).grid(row=1, column=0, pady=(2, 0), sticky="w")

        # Accent bottom border
        ctk.CTkFrame(self, height=2, fg_color=Theme.CRITICAL).grid(
            row=1, column=0, sticky="ew", padx=0, pady=0
        )

        # ── Scroll content ────────────────────────────────────────────
        scroll = ctk.CTkScrollableFrame(
            self, fg_color=Theme.BG_DARK, corner_radius=0,
            scrollbar_button_color=Theme.BG_INPUT,
            scrollbar_button_hover_color=Theme.ACCENT,
        )
        scroll.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        scroll.grid_columnconfigure(0, weight=1)
        scroll.grid_columnconfigure(1, weight=1)

        # Helplines heading
        ctk.CTkLabel(
            scroll, text="📞  Emergency Helplines",
            font=Theme.FONT_TITLE, text_color=Theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, columnspan=2, padx=Theme.PAD_LG,
               pady=(Theme.PAD_LG, Theme.PAD_SM), sticky="w")

        ctk.CTkLabel(
            scroll,
            text="Click any card to copy the number to clipboard",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        ).grid(row=1, column=0, columnspan=2, padx=Theme.PAD_LG, pady=(0, Theme.PAD), sticky="w")

        # Helpline cards grid
        for idx, (icon, name, number, desc, color) in enumerate(HELPLINES):
            col = idx % 2
            row = idx // 2 + 2
            self._make_helpline_card(scroll, icon, name, number, desc, color, row, col)

        # Escape plan heading
        ctk.CTkLabel(
            scroll, text="🏃  Safe Escape Plan",
            font=Theme.FONT_TITLE, text_color=Theme.TEXT_PRIMARY,
        ).grid(row=7, column=0, columnspan=2, padx=Theme.PAD_LG,
               pady=(Theme.PAD_LG, Theme.PAD_SM), sticky="w")

        for step_idx, (step_title, step_desc) in enumerate(ESCAPE_STEPS):
            self._make_step_card(scroll, step_idx + 1, step_title, step_desc,
                                 row=8 + step_idx)

        # Footer padding
        ctk.CTkFrame(scroll, height=Theme.PAD_LG, fg_color="transparent").grid(
            row=20, column=0, columnspan=2)

    def _make_helpline_card(self, parent, icon, name, number, desc, color, row, col):
        card = ctk.CTkFrame(
            parent,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS,
            border_width=1,
            border_color=color,
            cursor="hand2",
        )
        padx_left  = (Theme.PAD_LG, Theme.PAD_SM) if col == 0 else (Theme.PAD_SM, Theme.PAD_LG)
        card.grid(row=row, column=col, padx=padx_left, pady=4, sticky="nsew")
        card.grid_columnconfigure(1, weight=1)

        # Icon
        ctk.CTkLabel(
            card, text=icon, font=("Segoe UI", 24),
        ).grid(row=0, column=0, rowspan=2, padx=Theme.PAD, pady=Theme.PAD)

        # Name
        ctk.CTkLabel(
            card, text=name,
            font=("Segoe UI", 11, "bold"), text_color=Theme.TEXT_PRIMARY,
        ).grid(row=0, column=1, padx=(0, Theme.PAD), pady=(Theme.PAD, 0), sticky="w")

        # Number (large, colored)
        ctk.CTkLabel(
            card, text=number,
            font=("Segoe UI", 20, "bold"), text_color=color,
        ).grid(row=1, column=1, padx=(0, Theme.PAD), pady=0, sticky="w")

        # Description
        ctk.CTkLabel(
            card, text=desc,
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        ).grid(row=2, column=0, columnspan=2,
               padx=Theme.PAD, pady=(0, Theme.PAD_SM), sticky="w")

        # Copy on click
        def _copy(n=number):
            try:
                card.clipboard_clear()
                card.clipboard_append(n)
            except Exception:
                pass

        card.bind("<Button-1>", lambda e: _copy())
        for w in card.winfo_children():
            w.bind("<Button-1>", lambda e: _copy())

        # Hover effect
        def _enter(e, c=card, col=color):
            c.configure(fg_color=Theme.BG_ACTIVE)

        def _leave(e, c=card):
            c.configure(fg_color=Theme.BG_CARD)

        card.bind("<Enter>", _enter)
        card.bind("<Leave>", _leave)
        for w in card.winfo_children():
            w.bind("<Enter>", _enter)
            w.bind("<Leave>", _leave)

    def _make_step_card(self, parent, num, title, desc, row):
        card = ctk.CTkFrame(
            parent, fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS,
            border_width=0,
        )
        card.grid(row=row, column=0, columnspan=2,
                  padx=Theme.PAD_LG, pady=3, sticky="ew")
        card.grid_columnconfigure(1, weight=1)

        # Step number badge
        num_badge = ctk.CTkFrame(
            card, fg_color=Theme.ACCENT_MUTED,
            corner_radius=6, width=32, height=32,
        )
        num_badge.grid(row=0, column=0, rowspan=2, padx=Theme.PAD, pady=Theme.PAD)
        num_badge.grid_propagate(False)

        ctk.CTkLabel(
            num_badge, text=str(num),
            font=("Segoe UI", 11, "bold"), text_color="#ffffff",
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(
            card, text=title,
            font=("Segoe UI", 11, "bold"), text_color=Theme.TEXT_PRIMARY,
        ).grid(row=0, column=1, padx=(0, Theme.PAD), pady=(Theme.PAD_SM, 0), sticky="w")

        # Description
        ctk.CTkLabel(
            card, text=desc,
            font=Theme.FONT_BODY, text_color=Theme.TEXT_SECONDARY,
            wraplength=640, justify="left",
        ).grid(row=1, column=1, padx=(0, Theme.PAD), pady=(0, Theme.PAD_SM), sticky="w")
