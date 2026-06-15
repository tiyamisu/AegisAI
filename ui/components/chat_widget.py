"""
AegisAI — Chat Widget
=======================
Full chat interface: scrollable message history, typing animation,
quick-action suggestion chips, and message input bar.

All bot processing runs in a background thread; UI updates are
rescheduled on the main thread via root.after() — the UI never blocks.
"""
from __future__ import annotations

import threading
import time
import logging
from datetime import datetime
from typing import Callable, List, Optional

import customtkinter as ctk
from ui.theme import Theme
from models.message import ChatMessage, MessageRole

log = logging.getLogger(__name__)


# ── Individual message bubble ────────────────────────────────────────────────

class _MessageBubble(ctk.CTkFrame):
    """Single chat message row with bubble card + timestamp."""

    MAX_WIDTH = 500  # max bubble width in px

    def __init__(self, parent, message: ChatMessage) -> None:
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self._build(message)

    def _build(self, msg: ChatMessage) -> None:
        is_user = msg.role == MessageRole.USER

        # ── Bubble card colors ────────────────────────────────────────
        if msg.is_emergency:
            bg     = Theme.DANGER_BG
            border = Theme.DANGER
            bw     = 1
            tc     = Theme.TEXT_PRIMARY
        elif is_user:
            bg     = Theme.ACCENT_MUTED
            border = Theme.ACCENT_MUTED
            bw     = 0
            tc     = "#ffffff"
        else:
            bg     = Theme.BG_CARD
            border = Theme.BORDER
            bw     = 1
            tc     = Theme.TEXT_PRIMARY

        bubble = ctk.CTkFrame(
            self,
            fg_color=bg,
            border_color=border,
            border_width=bw,
            corner_radius=Theme.RADIUS,
        )

        if is_user:
            bubble.grid(row=0, column=0, padx=(100, 0), pady=(2, 0), sticky="e")
        else:
            bubble.grid(row=0, column=0, padx=(0, 100), pady=(2, 0), sticky="w")

        # Role prefix for bot messages
        if not is_user:
            prefix = "🚨  AegisAI" if msg.is_emergency else "🤖  AegisAI"
            prefix_color = Theme.DANGER if msg.is_emergency else Theme.ACCENT
            ctk.CTkLabel(
                bubble,
                text=prefix,
                font=("Segoe UI", 9, "bold"),
                text_color=prefix_color,
            ).pack(anchor="w", padx=Theme.PAD_SM, pady=(Theme.PAD_SM, 0))

        # Message text
        ctk.CTkLabel(
            bubble,
            text=msg.text,
            font=Theme.FONT_CHAT_MSG,
            text_color=tc,
            wraplength=self.MAX_WIDTH,
            justify="left",
            anchor="w",
        ).pack(anchor="w", padx=Theme.PAD_SM, pady=(3, Theme.PAD_SM))

        # ── Timestamp ─────────────────────────────────────────────────
        ts = ctk.CTkLabel(
            self,
            text=msg.formatted_time(),
            font=Theme.FONT_CHAT_TIME,
            text_color=Theme.TEXT_MUTED,
        )
        if is_user:
            ts.grid(row=1, column=0, padx=(0, 4), pady=(0, 4), sticky="e")
        else:
            ts.grid(row=1, column=0, padx=(4, 0), pady=(0, 4), sticky="w")


# ── Typing indicator ─────────────────────────────────────────────────────────

class _TypingIndicator(ctk.CTkFrame):
    """Animated three-dot typing indicator shown while bot processes."""

    _FRAMES = ["●  ·  ·", "·  ●  ·", "·  ·  ●"]

    def __init__(self, parent) -> None:
        super().__init__(parent, fg_color="transparent")
        self._alive = True
        self._step  = 0

        bubble = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS,
            border_width=1,
            border_color=Theme.BORDER,
        )
        bubble.pack(anchor="w", pady=(2, 4))

        self._lbl = ctk.CTkLabel(
            bubble,
            text=self._FRAMES[0],
            font=("Segoe UI", 12),
            text_color=Theme.ACCENT,
        )
        self._lbl.pack(padx=14, pady=8)

        self._animate()

    def _animate(self) -> None:
        if not self._alive:
            return
        self._lbl.configure(text=self._FRAMES[self._step % 3])
        self._step += 1
        try:
            self.after(380, self._animate)
        except Exception:
            pass

    def stop(self) -> None:
        self._alive = False


# ── Full chat widget ─────────────────────────────────────────────────────────

class ChatWidget(ctk.CTkFrame):
    """
    Complete chat interface panel.

    Parameters
    ----------
    parent      : Parent widget
    send_cb     : Callback(text: str) -> ChatMessage  (called on background thread)
    welcome_msg : Initial ChatMessage to display
    """

    # Quick-action chip definitions (label, query_text)
    _DEFAULT_CHIPS = [
        ("What is trafficking?",  "what is human trafficking"),
        ("Check my risk",          "start risk assessment"),
        ("Analyze job offer",      "check job offer"),
        ("Emergency help",         "emergency help"),
    ]

    def __init__(
        self,
        parent,
        send_cb: Callable[[str], ChatMessage],
        welcome_msg: Optional[ChatMessage] = None,
    ) -> None:
        super().__init__(
            parent,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS_LG,
            border_width=1,
            border_color=Theme.BORDER,
        )
        self._send_cb      = send_cb
        self._typing_widget: Optional[_TypingIndicator] = None
        self._chips: list   = []
        self._build()
        if welcome_msg:
            self.add_message(welcome_msg)

    # ------------------------------------------------------------------

    def _build(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Chat header bar ───────────────────────────────────────────
        chat_header = ctk.CTkFrame(self, fg_color=Theme.BG_INPUT, corner_radius=0, height=36)
        chat_header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        chat_header.grid_propagate(False)
        chat_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            chat_header,
            text="🤖  AI Chat  —  Ask anything about trafficking, risks, or safety",
            font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED,
            anchor="w",
        ).grid(row=0, column=0, padx=Theme.PAD, pady=0, sticky="w")

        # Thin accent line under header
        ctk.CTkFrame(self, height=1, fg_color=Theme.BORDER).grid(
            row=1, column=0, sticky="ew", padx=0, pady=0
        )

        # ── Message scroll area ───────────────────────────────────────
        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=Theme.BG_DARK,
            corner_radius=0,
            scrollbar_button_color=Theme.BG_INPUT,
            scrollbar_button_hover_color=Theme.ACCENT,
        )
        self._scroll.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        self._scroll.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ── Suggestion chips bar ──────────────────────────────────────
        self._chips_frame = ctk.CTkFrame(
            self, fg_color=Theme.BG_CARD, height=46, corner_radius=0,
            border_width=0,
        )
        self._chips_frame.grid(row=3, column=0, sticky="ew", padx=0, pady=0)
        self._render_chips(self._DEFAULT_CHIPS)

        # ── Divider ───────────────────────────────────────────────────
        ctk.CTkFrame(self, height=1, fg_color=Theme.BORDER).grid(
            row=4, column=0, sticky="ew", padx=0, pady=0
        )

        # ── Input bar ────────────────────────────────────────────────
        input_bar = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, height=56, corner_radius=0)
        input_bar.grid(row=5, column=0, sticky="ew", padx=0, pady=0)
        input_bar.grid_columnconfigure(0, weight=1)
        input_bar.grid_propagate(False)

        self._entry = ctk.CTkEntry(
            input_bar,
            placeholder_text="Type your message… (Enter to send)",
            font=Theme.FONT_BODY,
            fg_color=Theme.BG_INPUT,
            border_color=Theme.BORDER,
            text_color=Theme.TEXT_PRIMARY,
            placeholder_text_color=Theme.TEXT_MUTED,
            corner_radius=Theme.RADIUS,
            height=36,
        )
        self._entry.grid(row=0, column=0, padx=(Theme.PAD, 8), pady=10, sticky="ew")
        self._entry.bind("<Return>", lambda e: self._on_send())

        self._send_btn = ctk.CTkButton(
            input_bar,
            text="Send  ➤",
            font=("Segoe UI", 11, "bold"),
            width=86,
            height=36,
            fg_color=Theme.ACCENT,
            hover_color=Theme.ACCENT_HOVER,
            text_color="#1A1A2E",
            corner_radius=Theme.RADIUS,
            command=self._on_send,
        )
        self._send_btn.grid(row=0, column=1, padx=(0, Theme.PAD), pady=10)

    # ------------------------------------------------------------------

    def add_message(self, message: ChatMessage) -> None:
        """Add a ChatMessage bubble to the scroll area (main thread only)."""
        row = len(self._scroll.winfo_children())
        bubble = _MessageBubble(self._scroll, message)
        bubble.grid(row=row, column=0, padx=Theme.PAD, pady=2, sticky="ew")

        # Update suggestion chips
        if message.suggestions:
            chip_data = [(s, s) for s in message.suggestions[:4]]
            self._render_chips(chip_data)

        # Scroll to bottom after a brief delay
        self.after(80, self._scroll_to_bottom)

    def set_typing(self, visible: bool) -> None:
        """Show or hide the typing indicator."""
        if visible and self._typing_widget is None:
            row = len(self._scroll.winfo_children())
            self._typing_widget = _TypingIndicator(self._scroll)
            self._typing_widget.grid(row=row, column=0, padx=Theme.PAD, pady=2, sticky="w")
            self.after(80, self._scroll_to_bottom)

        elif not visible and self._typing_widget is not None:
            self._typing_widget.stop()
            self._typing_widget.destroy()
            self._typing_widget = None

    def set_input_enabled(self, enabled: bool) -> None:
        """Enable or disable the input field and send button."""
        state = "normal" if enabled else "disabled"
        self._entry.configure(state=state)
        self._send_btn.configure(state=state)

    # ------------------------------------------------------------------

    def _on_send(self) -> None:
        text = self._entry.get().strip()
        if not text:
            return

        self._entry.delete(0, "end")
        self.set_input_enabled(False)

        from models.message import ChatMessage
        self.add_message(ChatMessage.user(text))
        self.set_typing(True)

        def _process():
            try:
                time.sleep(0.5)
                return self._send_cb(text)
            except Exception as exc:
                log.error("Chat send error: %s", exc)
                return ChatMessage.bot("Sorry, I encountered an error. Please try again.")

        def _on_done(response: ChatMessage):
            self.after(0, lambda: self._show_response(response))

        threading.Thread(target=lambda: _on_done(_process()), daemon=True).start()

    def _show_response(self, response: ChatMessage) -> None:
        self.set_typing(False)
        self.add_message(response)
        self.set_input_enabled(True)
        self._entry.focus()

    def _render_chips(self, chips: list) -> None:
        """Render quick-action chip buttons."""
        for w in self._chips_frame.winfo_children():
            w.destroy()
        self._chips = []

        for idx, (label, query) in enumerate(chips[:5]):
            btn = ctk.CTkButton(
                self._chips_frame,
                text=label,
                font=Theme.FONT_CHIP,
                width=0,
                height=28,
                fg_color=Theme.BG_INPUT,
                hover_color=Theme.BG_HOVER,
                text_color=Theme.TEXT_SECONDARY,
                border_color=Theme.BORDER,
                border_width=1,
                corner_radius=Theme.RADIUS_SM,
                command=lambda q=query: self._chip_clicked(q),
            )
            btn.pack(side="left", padx=(Theme.PAD if idx == 0 else 4, 0), pady=9)
            self._chips.append(btn)

    def _chip_clicked(self, query: str) -> None:
        """Insert a chip query into the entry and send it."""
        self._entry.delete(0, "end")
        self._entry.insert(0, query)
        self._on_send()

    def _scroll_to_bottom(self) -> None:
        """Scroll the message area to the latest message."""
        try:
            self._scroll._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    def inject_message(self, text: str) -> None:
        """Programmatically send a message (e.g., from sidebar navigation)."""
        self._entry.delete(0, "end")
        self._entry.insert(0, text)
        self._on_send()
