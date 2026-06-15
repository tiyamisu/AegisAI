"""
AegisAI — Modern Tkinter GUI
==============================
Provides a polished, dark-themed chat interface for the AegisAI chatbot.
Uses only Python standard library (tkinter) — no external dependencies.

Features:
  - Dark professional theme
  - Left navigation sidebar
  - Scrollable chat message area with styled bubbles
  - Risk level status indicator (colour-coded)
  - Emergency banner (flashes when critical)
  - Job offer paste dialog
  - Responsive layout

Author  : AegisAI Team
Version : 1.0
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import threading
import time
import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from chatbot import ChatBot, ChatResponse, Intent


# ===========================================================================
# COLOUR PALETTE
# ===========================================================================

class Palette:
    # Backgrounds
    BG_DARK     = "#0d1117"     # main window background
    BG_SIDEBAR  = "#161b22"     # sidebar background
    BG_HEADER   = "#0d1117"     # header bar
    BG_INPUT    = "#21262d"     # input area background
    BG_BUBBLE_BOT  = "#1f2937"  # bot message bubble
    BG_BUBBLE_USER = "#1a4731"  # user message bubble
    BG_BUTTON   = "#21262d"     # sidebar button default
    BG_BTN_HOV  = "#30363d"     # sidebar button hover
    BG_BTN_ACT  = "#238636"     # sidebar button active (green)

    # Text
    TEXT_PRIMARY   = "#e6edf3"
    TEXT_SECONDARY = "#8b949e"
    TEXT_ACCENT    = "#58a6ff"
    TEXT_SUCCESS   = "#3fb950"
    TEXT_WARNING   = "#d29922"
    TEXT_DANGER    = "#f85149"
    TEXT_BOT_NAME  = "#58a6ff"
    TEXT_USER_NAME = "#3fb950"

    # Risk level colours
    RISK_UNKNOWN   = "#8b949e"
    RISK_LOW       = "#3fb950"
    RISK_MEDIUM    = "#d29922"
    RISK_HIGH      = "#f85149"
    RISK_CRITICAL  = "#ff0000"

    # Other
    BORDER         = "#30363d"
    SEPARATOR      = "#21262d"
    SEND_BTN       = "#238636"
    SEND_BTN_HOV   = "#2ea043"
    SCROLLBAR      = "#30363d"


# ===========================================================================
# RISK COLOURS (for status indicator)
# ===========================================================================

_RISK_COLORS = {
    "UNKNOWN":  (Palette.RISK_UNKNOWN,  "⚪ Not Assessed"),
    "LOW":      (Palette.RISK_LOW,      "🟢 Low Risk"),
    "MEDIUM":   (Palette.RISK_MEDIUM,   "🟡 Medium Risk"),
    "HIGH":     (Palette.RISK_HIGH,     "🔴 High Risk"),
    "CRITICAL": (Palette.RISK_CRITICAL, "🚨 Critical"),
}


# ===========================================================================
# SIDEBAR BUTTONS CONFIG
# ===========================================================================

_SIDEBAR_BUTTONS = [
    ("🏠  Home / Menu",          "menu"),
    ("📚  Trafficking Basics",   "what is human trafficking"),
    ("⚠️   Warning Signs",        "warning signs"),
    ("👶  Child Trafficking",    "child trafficking"),
    ("🏗️   Forced Labour",        "forced labour"),
    ("💻  Online Grooming",      "online grooming"),
    ("❤️   Victim Support",       "victim support"),
    ("📋  Legal Rights",         "legal rights"),
    ("🔐  Safety Tips",          "safety tips"),
    ("🏢  NGO Support",          "ngo support"),
    ("───────────────────────", None),  # separator
    ("🔍  Risk Assessment",      "risk assessment"),
    ("💼  Check Job Offer",      "check job offer"),
    ("📞  Emergency Helplines",  "helplines"),
    ("───────────────────────", None),  # separator
    ("🔄  Reset Session",        "__reset__"),
]


# ===========================================================================
# TYPING ANIMATION
# ===========================================================================

class TypingIndicator:
    """Shows an animated 'AegisAI is typing...' indicator."""

    def __init__(self, chat_area, palette: Palette):
        self._chat_area = chat_area
        self._palette   = palette
        self._active    = False
        self._tag_id    = None

    def show(self):
        if self._active:
            return
        self._active = True
        self._chat_area.config(state=tk.NORMAL)
        self._chat_area.insert(tk.END, "\n🛡️ AegisAI  ·  ·  ·\n", "typing")
        self._chat_area.see(tk.END)
        self._chat_area.config(state=tk.DISABLED)

    def hide(self):
        if not self._active:
            return
        self._active = False
        self._chat_area.config(state=tk.NORMAL)
        content = self._chat_area.get("1.0", tk.END)
        lines   = content.split("\n")
        # Remove last typing line
        final   = "\n".join(
            l for l in lines if "·  ·  ·" not in l
        )
        self._chat_area.delete("1.0", tk.END)
        self._chat_area.insert("1.0", final)
        self._chat_area.see(tk.END)
        self._chat_area.config(state=tk.DISABLED)


# ===========================================================================
# MAIN APPLICATION CLASS
# ===========================================================================

class AegisAIApp:
    """
    Main Tkinter application for AegisAI.

    Builds the GUI layout, connects the ChatBot engine,
    and handles all UI events.
    """

    APP_TITLE   = "AegisAI — AI-Powered Human Trafficking Prevention"
    APP_VERSION = "v1.0"
    WIN_WIDTH   = 1020
    WIN_HEIGHT  = 700
    MIN_WIDTH   = 800
    MIN_HEIGHT  = 550

    def __init__(self, root: tk.Tk):
        """
        Initialise the application.

        Args:
            root: Tkinter root window
        """
        self._root     = root
        self._bot      = ChatBot()
        self._palette  = Palette()
        self._emergency_flash_active = False
        self._emergency_flash_state  = False

        self._setup_window()
        self._build_layout()
        self._apply_theme()
        self._show_welcome()

    # ------------------------------------------------------------------
    # WINDOW SETUP
    # ------------------------------------------------------------------

    def _setup_window(self):
        """Configure the root window."""
        self._root.title(self.APP_TITLE)
        self._root.configure(bg=Palette.BG_DARK)
        self._root.resizable(True, True)
        self._root.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)

        # Centre on screen
        sw = self._root.winfo_screenwidth()
        sh = self._root.winfo_screenheight()
        x  = (sw - self.WIN_WIDTH)  // 2
        y  = (sh - self.WIN_HEIGHT) // 2
        self._root.geometry(f"{self.WIN_WIDTH}x{self.WIN_HEIGHT}+{x}+{y}")

        # Handle close
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------------
    # LAYOUT CONSTRUCTION
    # ------------------------------------------------------------------

    def _build_layout(self):
        """Build the entire GUI layout."""
        self._build_header()
        self._build_main_area()
        self._build_input_area()
        self._build_status_bar()

    def _build_header(self):
        """Build the top header bar."""
        self._header = tk.Frame(
            self._root, bg=Palette.BG_HEADER,
            height=60, bd=0, highlightthickness=0
        )
        self._header.pack(side=tk.TOP, fill=tk.X)
        self._header.pack_propagate(False)

        # Shield icon + title
        tk.Label(
            self._header, text="🛡️",
            font=("Segoe UI Emoji", 22),
            bg=Palette.BG_HEADER, fg=Palette.TEXT_ACCENT,
        ).pack(side=tk.LEFT, padx=(16, 4), pady=10)

        # Title block
        title_frame = tk.Frame(self._header, bg=Palette.BG_HEADER)
        title_frame.pack(side=tk.LEFT, padx=4, pady=10)

        tk.Label(
            title_frame, text="AegisAI",
            font=("Segoe UI", 16, "bold"),
            bg=Palette.BG_HEADER, fg=Palette.TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="AI-Powered Human Trafficking Prevention & Victim Assistance",
            font=("Segoe UI", 8),
            bg=Palette.BG_HEADER, fg=Palette.TEXT_SECONDARY,
        ).pack(anchor="w")

        # Emergency button (right side)
        self._emergency_btn = tk.Button(
            self._header, text="🆘 EMERGENCY",
            font=("Segoe UI", 10, "bold"),
            bg="#8b0000", fg="white",
            activebackground="#a00000", activeforeground="white",
            bd=0, padx=12, pady=6, cursor="hand2",
            command=self._on_emergency,
        )
        self._emergency_btn.pack(side=tk.RIGHT, padx=16, pady=12)

        # Risk level badge
        risk_frame = tk.Frame(self._header, bg=Palette.BG_HEADER)
        risk_frame.pack(side=tk.RIGHT, padx=8, pady=10)

        tk.Label(
            risk_frame, text="RISK LEVEL",
            font=("Segoe UI", 7, "bold"),
            bg=Palette.BG_HEADER, fg=Palette.TEXT_SECONDARY,
        ).pack()

        self._risk_label = tk.Label(
            risk_frame, text="⚪ Not Assessed",
            font=("Segoe UI", 9, "bold"),
            bg=Palette.BG_HEADER, fg=Palette.RISK_UNKNOWN,
        )
        self._risk_label.pack()

        # Separator line
        tk.Frame(
            self._root, bg=Palette.BORDER, height=1
        ).pack(side=tk.TOP, fill=tk.X)

    def _build_main_area(self):
        """Build the sidebar + chat area."""
        main_frame = tk.Frame(self._root, bg=Palette.BG_DARK)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._build_sidebar(main_frame)
        self._build_chat_area(main_frame)

    def _build_sidebar(self, parent):
        """Build the left navigation sidebar."""
        sidebar_outer = tk.Frame(
            parent, bg=Palette.BG_SIDEBAR,
            width=210, bd=0,
            highlightthickness=1,
            highlightbackground=Palette.BORDER,
        )
        sidebar_outer.pack(side=tk.LEFT, fill=tk.Y)
        sidebar_outer.pack_propagate(False)

        # Sidebar title
        tk.Label(
            sidebar_outer, text="NAVIGATION",
            font=("Segoe UI", 8, "bold"),
            bg=Palette.BG_SIDEBAR, fg=Palette.TEXT_SECONDARY,
            anchor="w",
        ).pack(fill=tk.X, padx=12, pady=(12, 4))

        # Scrollable sidebar buttons
        sidebar_canvas = tk.Canvas(
            sidebar_outer, bg=Palette.BG_SIDEBAR,
            highlightthickness=0, bd=0,
        )
        sidebar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sb_scroll = ttk.Scrollbar(
            sidebar_outer, orient=tk.VERTICAL, command=sidebar_canvas.yview
        )
        sidebar_canvas.configure(yscrollcommand=sb_scroll.set)

        btn_frame = tk.Frame(sidebar_canvas, bg=Palette.BG_SIDEBAR)
        sidebar_canvas.create_window((0, 0), window=btn_frame, anchor="nw")

        self._sidebar_buttons_refs = []
        for label, command in _SIDEBAR_BUTTONS:
            if command is None:
                # Separator
                sep = tk.Frame(btn_frame, bg=Palette.BORDER, height=1)
                sep.pack(fill=tk.X, padx=8, pady=4)
                tk.Label(
                    btn_frame, text="",
                    bg=Palette.BG_SIDEBAR, height=0,
                ).pack()
                continue

            btn = tk.Button(
                btn_frame,
                text=label,
                font=("Segoe UI", 9),
                bg=Palette.BG_BUTTON, fg=Palette.TEXT_PRIMARY,
                activebackground=Palette.BG_BTN_HOV,
                activeforeground=Palette.TEXT_PRIMARY,
                bd=0, relief=tk.FLAT,
                padx=12, pady=7,
                anchor="w",
                cursor="hand2",
                command=lambda c=command: self._on_sidebar_click(c),
            )
            btn.pack(fill=tk.X, padx=4, pady=1)

            # Hover effects
            btn.bind("<Enter>",
                     lambda e, b=btn: b.configure(bg=Palette.BG_BTN_HOV))
            btn.bind("<Leave>",
                     lambda e, b=btn: b.configure(bg=Palette.BG_BUTTON))

            self._sidebar_buttons_refs.append(btn)

        # Update scroll region
        btn_frame.update_idletasks()
        sidebar_canvas.config(scrollregion=sidebar_canvas.bbox("all"))

    def _build_chat_area(self, parent):
        """Build the main chat message display area."""
        chat_outer = tk.Frame(parent, bg=Palette.BG_DARK)
        chat_outer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Chat text widget with scrollbar
        chat_frame = tk.Frame(chat_outer, bg=Palette.BG_DARK)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Custom scrollbar
        scrollbar = ttk.Scrollbar(chat_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._chat_area = tk.Text(
            chat_frame,
            bg=Palette.BG_DARK,
            fg=Palette.TEXT_PRIMARY,
            font=("Consolas", 10),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bd=0,
            padx=12,
            pady=8,
            yscrollcommand=scrollbar.set,
            cursor="arrow",
            highlightthickness=0,
            selectbackground=Palette.BG_BTN_HOV,
        )
        self._chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.configure(command=self._chat_area.yview)

        # Text tags for styled messages
        self._chat_area.tag_configure(
            "bot_name",
            font=("Segoe UI", 9, "bold"),
            foreground=Palette.TEXT_BOT_NAME,
        )
        self._chat_area.tag_configure(
            "user_name",
            font=("Segoe UI", 9, "bold"),
            foreground=Palette.TEXT_USER_NAME,
        )
        self._chat_area.tag_configure(
            "bot_msg",
            font=("Segoe UI", 10),
            foreground=Palette.TEXT_PRIMARY,
            lmargin1=16,
            lmargin2=16,
        )
        self._chat_area.tag_configure(
            "user_msg",
            font=("Segoe UI", 10),
            foreground="#c8e6c9",
            lmargin1=16,
            lmargin2=16,
        )
        self._chat_area.tag_configure(
            "emergency_msg",
            font=("Segoe UI", 10, "bold"),
            foreground=Palette.TEXT_DANGER,
            lmargin1=16,
            lmargin2=16,
        )
        self._chat_area.tag_configure(
            "typing",
            font=("Segoe UI", 9, "italic"),
            foreground=Palette.TEXT_SECONDARY,
            lmargin1=16,
        )
        self._chat_area.tag_configure(
            "separator",
            foreground=Palette.BORDER,
        )
        self._chat_area.tag_configure(
            "timestamp",
            font=("Segoe UI", 7),
            foreground=Palette.TEXT_SECONDARY,
        )
        self._chat_area.tag_configure(
            "risk_badge_low",
            font=("Segoe UI", 8, "bold"),
            foreground=Palette.RISK_LOW,
        )
        self._chat_area.tag_configure(
            "risk_badge_medium",
            font=("Segoe UI", 8, "bold"),
            foreground=Palette.RISK_MEDIUM,
        )
        self._chat_area.tag_configure(
            "risk_badge_high",
            font=("Segoe UI", 8, "bold"),
            foreground=Palette.RISK_HIGH,
        )
        self._chat_area.tag_configure(
            "risk_badge_critical",
            font=("Segoe UI", 8, "bold"),
            foreground=Palette.RISK_CRITICAL,
        )

        self._typing = TypingIndicator(self._chat_area, self._palette)

    def _build_input_area(self):
        """Build the message input area at the bottom."""
        # Separator
        tk.Frame(
            self._root, bg=Palette.BORDER, height=1
        ).pack(side=tk.BOTTOM, fill=tk.X)

        input_outer = tk.Frame(
            self._root, bg=Palette.BG_INPUT, pady=10
        )
        input_outer.pack(side=tk.BOTTOM, fill=tk.X)

        # Current state label
        self._state_label = tk.Label(
            input_outer,
            text="💬 Chat",
            font=("Segoe UI", 8),
            bg=Palette.BG_INPUT, fg=Palette.TEXT_SECONDARY,
            anchor="w",
        )
        self._state_label.pack(side=tk.TOP, fill=tk.X, padx=16, pady=(0, 4))

        # Input row
        input_row = tk.Frame(input_outer, bg=Palette.BG_INPUT)
        input_row.pack(fill=tk.X, padx=12)

        # Text input field
        self._input_var = tk.StringVar()
        self._input_field = tk.Entry(
            input_row,
            textvariable=self._input_var,
            font=("Segoe UI", 11),
            bg="#21262d",
            fg=Palette.TEXT_PRIMARY,
            insertbackground=Palette.TEXT_ACCENT,
            bd=0,
            highlightthickness=1,
            highlightbackground=Palette.BORDER,
            highlightcolor=Palette.TEXT_ACCENT,
            relief=tk.FLAT,
        )
        self._input_field.pack(
            side=tk.LEFT, fill=tk.X, expand=True,
            ipady=10, padx=(0, 8),
        )
        self._input_field.bind("<Return>", self._on_send)
        self._input_field.bind("<KP_Enter>", self._on_send)

        # Send button
        self._send_btn = tk.Button(
            input_row,
            text="  ▶  Send  ",
            font=("Segoe UI", 10, "bold"),
            bg=Palette.SEND_BTN,
            fg="white",
            activebackground=Palette.SEND_BTN_HOV,
            activeforeground="white",
            bd=0, relief=tk.FLAT,
            padx=16, pady=9,
            cursor="hand2",
            command=self._on_send,
        )
        self._send_btn.pack(side=tk.RIGHT)

        # Bind hover effects to send button
        self._send_btn.bind(
            "<Enter>", lambda e: self._send_btn.config(bg=Palette.SEND_BTN_HOV))
        self._send_btn.bind(
            "<Leave>", lambda e: self._send_btn.config(bg=Palette.SEND_BTN))

        # Focus input on startup
        self._input_field.focus()

    def _build_status_bar(self):
        """Build the bottom status bar."""
        tk.Frame(
            self._root, bg=Palette.BORDER, height=1
        ).pack(side=tk.BOTTOM, fill=tk.X)

        status_bar = tk.Frame(
            self._root, bg="#0a0e14", height=22
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        status_bar.pack_propagate(False)

        tk.Label(
            status_bar,
            text=f"AegisAI {self.APP_VERSION}  |  All conversations are private & anonymous  |  "
                 f"Emergency: 100 / 1098 / 112",
            font=("Segoe UI", 7),
            bg="#0a0e14", fg="#484f58",
        ).pack(side=tk.LEFT, padx=10, pady=3)

    # ------------------------------------------------------------------
    # THEME
    # ------------------------------------------------------------------

    def _apply_theme(self):
        """Apply ttk theme overrides."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Vertical.TScrollbar",
            background=Palette.BG_DARK,
            troughcolor=Palette.BG_DARK,
            bordercolor=Palette.BG_DARK,
            arrowcolor=Palette.TEXT_SECONDARY,
            width=8,
        )

    # ------------------------------------------------------------------
    # WELCOME
    # ------------------------------------------------------------------

    def _show_welcome(self):
        """Display the welcome message when the app opens."""
        welcome = self._bot.get_welcome_message()
        self._append_bot_message(welcome)
        self._update_state_label("💬 Type a message or choose from the menu")

    # ------------------------------------------------------------------
    # MESSAGE DISPLAY
    # ------------------------------------------------------------------

    def _append_bot_message(self, text: str, is_emergency: bool = False):
        """
        Append a bot message bubble to the chat area.

        Args:
            text:         Message text
            is_emergency: If True, use danger colours
        """
        self._chat_area.config(state=tk.NORMAL)
        ts = time.strftime("%H:%M")

        # Bot name header
        self._chat_area.insert(tk.END, "\n")
        self._chat_area.insert(tk.END, f"🛡️ AegisAI  ", "bot_name")
        self._chat_area.insert(tk.END, f"{ts}\n", "timestamp")

        # Message body
        msg_tag = "emergency_msg" if is_emergency else "bot_msg"
        self._chat_area.insert(tk.END, f"{text}\n", msg_tag)

        # Separator
        self._chat_area.insert(
            tk.END,
            "  " + "─" * 70 + "\n",
            "separator"
        )

        self._chat_area.see(tk.END)
        self._chat_area.config(state=tk.DISABLED)

    def _append_user_message(self, text: str):
        """Append a user message bubble to the chat area."""
        self._chat_area.config(state=tk.NORMAL)
        ts = time.strftime("%H:%M")

        self._chat_area.insert(tk.END, "\n")
        self._chat_area.insert(tk.END, f"👤 You  ", "user_name")
        self._chat_area.insert(tk.END, f"{ts}\n", "timestamp")
        self._chat_area.insert(tk.END, f"{text}\n", "user_msg")
        self._chat_area.insert(
            tk.END,
            "  " + "─" * 70 + "\n",
            "separator"
        )

        self._chat_area.see(tk.END)
        self._chat_area.config(state=tk.DISABLED)

    def _update_risk_indicator(self, risk_level: str):
        """Update the risk level badge in the header."""
        color, label = _RISK_COLORS.get(
            risk_level, _RISK_COLORS["UNKNOWN"]
        )
        self._risk_label.config(text=label, fg=color)

        if risk_level == "CRITICAL":
            self._start_emergency_flash()

    def _update_state_label(self, text: str):
        """Update the state label above the input field."""
        self._state_label.config(text=text)

    # ------------------------------------------------------------------
    # EMERGENCY FLASH
    # ------------------------------------------------------------------

    def _start_emergency_flash(self):
        """Start the emergency banner flash animation."""
        if not self._emergency_flash_active:
            self._emergency_flash_active = True
            self._flash_cycle()

    def _flash_cycle(self):
        """Toggle emergency button colour repeatedly."""
        if not self._emergency_flash_active:
            return
        if self._emergency_flash_state:
            self._emergency_btn.config(bg="#8b0000")
        else:
            self._emergency_btn.config(bg="#ff0000")
        self._emergency_flash_state = not self._emergency_flash_state
        self._root.after(600, self._flash_cycle)

    def _stop_emergency_flash(self):
        self._emergency_flash_active = False
        self._emergency_btn.config(bg="#8b0000")

    # ------------------------------------------------------------------
    # EVENT HANDLERS
    # ------------------------------------------------------------------

    def _on_send(self, event=None):
        """Handle Send button click or Enter key press."""
        user_text = self._input_var.get().strip()
        if not user_text:
            return

        self._input_var.set("")
        self._input_field.config(state=tk.DISABLED)
        self._send_btn.config(state=tk.DISABLED)

        # Show user message immediately
        self._append_user_message(user_text)

        # Process in background thread to avoid freezing UI
        thread = threading.Thread(
            target=self._process_in_thread,
            args=(user_text,),
            daemon=True,
        )
        thread.start()

    def _process_in_thread(self, user_text: str):
        """Run chatbot processing in background thread."""
        # Show typing indicator
        self._root.after(0, self._typing.show)

        # Simulate minimal thinking delay for UX
        time.sleep(0.4)

        try:
            response = self._bot.process(user_text)
        except Exception as e:
            response = type("R", (), {
                "text": f"An error occurred: {e}\nPlease try again.",
                "intent": Intent.UNCLEAR,
                "risk_level": "UNKNOWN",
                "is_emergency": False,
            })()

        # Update UI from main thread
        self._root.after(0, lambda: self._handle_response(response))

    def _handle_response(self, response: ChatResponse):
        """Display the bot's response in the UI (must run on main thread)."""
        self._typing.hide()

        # Display message
        self._append_bot_message(
            response.text,
            is_emergency=response.is_emergency
        )

        # Update risk indicator
        if hasattr(response, "risk_level") and response.risk_level:
            self._update_risk_indicator(response.risk_level)

        # Update state label based on active mode
        if self._bot.get_session_state().pending_job_text:
            self._update_state_label(
                "📋 Paste job description text and press Send"
            )
        elif self._bot._risk.is_active():
            self._update_state_label(
                "🔍 Risk Assessment active — answer YES or NO"
            )
        else:
            self._update_state_label("💬 Type a message or choose from the menu")

        # Re-enable input
        self._input_field.config(state=tk.NORMAL)
        self._send_btn.config(state=tk.NORMAL)
        self._input_field.focus()

    def _on_sidebar_click(self, command: str):
        """Handle sidebar button clicks."""
        if command == "__reset__":
            self._on_reset_session()
            return

        # Inject the command as if the user typed it
        self._input_var.set(command)
        self._on_send()

    def _on_emergency(self):
        """Handle Emergency button click."""
        self._input_var.set("emergency")
        self._on_send()
        self._start_emergency_flash()

    def _on_reset_session(self):
        """Reset the entire session after confirmation."""
        if messagebox.askyesno(
            "Reset Session",
            "This will clear the conversation and reset your session.\n"
            "Continue?",
            icon="warning",
        ):
            self._bot.reset_session()
            self._stop_emergency_flash()

            # Clear chat area
            self._chat_area.config(state=tk.NORMAL)
            self._chat_area.delete("1.0", tk.END)
            self._chat_area.config(state=tk.DISABLED)

            # Reset risk indicator
            self._update_risk_indicator("UNKNOWN")
            self._update_state_label("💬 Session reset. Start fresh!")

            # Show welcome again
            self._show_welcome()

    def _on_close(self):
        """Handle window close event."""
        if messagebox.askokcancel(
            "Exit AegisAI",
            "Are you sure you want to exit?\n\n"
            "Remember:\n"
            "  • Police: 100\n"
            "  • Childline: 1098\n"
            "  • Emergency: 112",
        ):
            self._root.destroy()

    # ------------------------------------------------------------------
    # KEYBOARD SHORTCUTS
    # ------------------------------------------------------------------

    def setup_shortcuts(self):
        """Bind global keyboard shortcuts."""
        self._root.bind("<Control-r>", lambda e: self._on_reset_session())
        self._root.bind("<Control-e>", lambda e: self._on_emergency())
        self._root.bind("<Escape>",    lambda e: self._input_field.focus())


# ===========================================================================
# STANDALONE RUNNER
# ===========================================================================

def run_app():
    """Launch the AegisAI GUI application."""
    root = tk.Tk()

    # Set app icon (Unicode shield character in title)
    try:
        root.wm_iconbitmap()
    except Exception:
        pass

    app = AegisAIApp(root)
    app.setup_shortcuts()

    root.mainloop()


if __name__ == "__main__":
    run_app()
