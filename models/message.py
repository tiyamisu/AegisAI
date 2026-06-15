"""
AegisAI — ChatMessage Model
============================
Defines the data structures for chat conversation messages.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


class MessageRole(Enum):
    """Identifies who sent a message in the conversation."""
    USER   = "user"
    BOT    = "bot"
    SYSTEM = "system"


@dataclass
class ChatMessage:
    """
    Represents a single message in the AegisAI conversation.

    Attributes:
        role        : Who sent this message (USER | BOT | SYSTEM)
        text        : The message content
        timestamp   : When the message was created
        is_emergency: True when the message contains emergency guidance
        suggestions : List of follow-up quick-action suggestions to show
        intent      : The classified intent that produced this message
    """
    role: MessageRole
    text: str
    timestamp: datetime        = field(default_factory=datetime.now)
    is_emergency: bool         = False
    suggestions: List[str]     = field(default_factory=list)
    intent: str                = ""

    # ------------------------------------------------------------------
    def formatted_time(self) -> str:
        """Return timestamp as HH:MM string for display."""
        return self.timestamp.strftime("%H:%M")

    @classmethod
    def bot(cls, text: str, *, is_emergency: bool = False,
            suggestions: List[str] | None = None, intent: str = "") -> "ChatMessage":
        """Factory: create a bot message."""
        return cls(
            role=MessageRole.BOT,
            text=text,
            is_emergency=is_emergency,
            suggestions=suggestions or [],
            intent=intent,
        )

    @classmethod
    def user(cls, text: str) -> "ChatMessage":
        """Factory: create a user message."""
        return cls(role=MessageRole.USER, text=text)

    @classmethod
    def system(cls, text: str) -> "ChatMessage":
        """Factory: create a system notification message."""
        return cls(role=MessageRole.SYSTEM, text=text)
