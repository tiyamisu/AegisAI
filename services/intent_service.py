"""
AegisAI — Intent Service
==========================
Classifies user input into a typed Intent enum.
Uses a priority-ordered pattern dictionary — no if-else chains.
"""
from __future__ import annotations

import logging
from enum import Enum, auto
from typing import Dict, List

log = logging.getLogger(__name__)


class Intent(Enum):
    """All supported user intents."""
    GREETING        = auto()
    LEARN_BASICS    = auto()
    WARNING_SIGNS   = auto()
    CHILD_TRAFFICKING = auto()
    FORCED_LABOUR   = auto()
    ONLINE_GROOMING = auto()
    RISK_ASSESSMENT = auto()
    JOB_ANALYSIS    = auto()
    EMERGENCY       = auto()
    REPORTING       = auto()
    LEGAL_RIGHTS    = auto()
    NGO_SUPPORT     = auto()
    SAFETY_TIPS     = auto()
    MENU            = auto()
    UNCLEAR         = auto()

    @property
    def suggestion_family(self) -> str:
        """Map intent to a KB suggestion family key."""
        families = {
            Intent.EMERGENCY:       "emergency",
            Intent.REPORTING:       "report",
            Intent.RISK_ASSESSMENT: "risk",
            Intent.JOB_ANALYSIS:    "scam",
            Intent.LEARN_BASICS:    "learn",
            Intent.WARNING_SIGNS:   "learn",
        }
        return families.get(self, "default")


# ---------------------------------------------------------------------------
# Pattern dictionary — checked in order (most specific first)
# ---------------------------------------------------------------------------
_PATTERNS: Dict[Intent, List[str]] = {
    Intent.EMERGENCY: [
        "emergency", "danger", "help me", "trapped", "need help now",
        "sos", "scared", "call police", "unsafe", "run away",
        "escape", "in danger", "being held", "kidnap",
    ],
    Intent.RISK_ASSESSMENT: [
        "risk assessment", "assess my risk", "check my risk",
        "am i safe", "how safe am i", "are you safe", "danger check",
        "start assessment", "take assessment",
    ],
    Intent.JOB_ANALYSIS: [
        "check job", "job offer", "analyze job", "analyse job",
        "scam check", "is this job", "suspicious job", "job scam",
        "job advertisement", "work offer", "employment offer",
    ],
    Intent.WARNING_SIGNS: [
        "warning signs", "red flags", "signs of trafficking",
        "how to identify", "indicators of", "spot trafficking",
    ],
    Intent.CHILD_TRAFFICKING: [
        "child trafficking", "child abuse", "pocso", "childline",
        "child exploitation", "minor trafficking", "children",
    ],
    Intent.FORCED_LABOUR: [
        "forced labour", "bonded labour", "debt bondage",
        "forced to work", "unpaid work", "slave labour",
    ],
    Intent.ONLINE_GROOMING: [
        "online grooming", "grooming", "catfish", "social media",
        "sextortion", "online predator", "messaging apps",
    ],
    Intent.REPORTING: [
        "report", "how to report", "file complaint", "fir",
        "cybercrime", "nhrc", "report trafficking", "make complaint",
    ],
    Intent.LEGAL_RIGHTS: [
        "legal rights", "my rights", "victim rights",
        "law", "itpa", "ipc 370", "legal protection",
    ],
    Intent.NGO_SUPPORT: [
        "ngo", "organisation", "organization", "ijm", "prerana",
        "shakti vahini", "support group", "contact ngo",
    ],
    Intent.SAFETY_TIPS: [
        "stay safe", "safety tips", "how to stay safe",
        "protect myself", "be safe online", "travel safety",
    ],
    Intent.LEARN_BASICS: [
        "what is trafficking", "human trafficking", "what is",
        "define", "explain", "tell me about", "information",
    ],
    Intent.GREETING: [
        "hello", "hi", "hey", "namaste", "good morning",
        "good evening", "start", "begin",
    ],
    Intent.MENU: [
        "menu", "home", "main menu", "options",
        "what can you do", "help", "commands",
    ],
}


class IntentService:
    """
    Classifies raw user text into an Intent.

    Strategy (in priority order):
    1. Exact single-word commands (menu, home, start)
    2. Pattern matching via _PATTERNS dict
    3. KB similarity fallback (returns LEARN_BASICS if confident)
    4. UNCLEAR
    """

    _EXACT_MAP: Dict[str, Intent] = {
        "menu":      Intent.MENU,
        "home":      Intent.MENU,
        "back":      Intent.MENU,
        "start":     Intent.GREETING,
        "help":      Intent.MENU,
        "sos":       Intent.EMERGENCY,
        "emergency": Intent.EMERGENCY,
    }

    def __init__(self, kb_manager=None) -> None:
        self._kb = kb_manager

    def classify(self, text: str) -> Intent:
        """Classify user input text to the most appropriate Intent."""
        lower = text.lower().strip()

        if not lower:
            return Intent.UNCLEAR

        # 1. Exact single-word match
        if lower in self._EXACT_MAP:
            return self._EXACT_MAP[lower]

        # 2. Pattern matching (first match wins — patterns are priority-ordered)
        for intent, patterns in _PATTERNS.items():
            for pattern in patterns:
                if pattern in lower:
                    log.debug("Intent: %s (pattern: '%s')", intent.name, pattern)
                    return intent

        # 3. KB similarity fallback
        if self._kb:
            try:
                results = self._kb.query(text, top_n=1)
                if results and results[0].confidence >= 0.15:
                    return Intent.LEARN_BASICS
            except Exception:
                pass

        return Intent.UNCLEAR
