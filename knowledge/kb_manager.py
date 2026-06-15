"""
AegisAI — Knowledge Base Manager
===================================
Thin adapter that wraps data/knowledge_base.py providing a clean,
typed interface to the rest of the application.

The underlying KB data is kept 100% unchanged — this layer only
changes how we access it.
"""
from __future__ import annotations

import logging
import sys
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional

# Ensure project root is importable
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

log = logging.getLogger(__name__)


@dataclass
class KBResult:
    """Single knowledge base query result."""
    entry_id:   str
    category:   str
    intent:     str
    response:   str
    confidence: float   # 0.0 – 1.0
    priority:   int


class KBManager:
    """
    Provides a clean interface to the AegisAI knowledge base.

    Public methods
    --------------
    query(text, top_n)     -> list[KBResult]
    get_best_response(text)-> str
    get_emergency_info()   -> str
    get_by_category(cat)   -> list[KBResult]
    get_categories()       -> list[str]
    get_suggestions(intent)-> list[str]
    stats()                -> dict
    """

    # Quick-action suggestions mapped by broad intent family
    _SUGGESTIONS: dict[str, List[str]] = {
        "emergency": [
            "What is the escape plan?",
            "Call emergency helplines",
            "How to reach a shelter?",
        ],
        "learn": [
            "What are warning signs?",
            "How does recruitment scam work?",
            "Child trafficking facts",
        ],
        "risk": [
            "Start risk assessment",
            "What is forced labour?",
            "Online grooming signs",
        ],
        "scam": [
            "Red flags in job offers",
            "How to verify a job?",
            "Report a suspicious offer",
        ],
        "report": [
            "How to file an FIR?",
            "NHRC complaint process",
            "Online reporting portal",
        ],
        "default": [
            "What is human trafficking?",
            "Check my risk level",
            "Analyze job offer",
            "Emergency help",
        ],
    }

    # ------------------------------------------------------------------

    def __init__(self) -> None:
        """Load the knowledge base from data/knowledge_base.py."""
        try:
            from knowledge_base import KnowledgeBaseManager as _KBM
            self._kb = _KBM()
            log.info("KBManager ready. Entries: %d", self._kb.total_entries())
        except Exception as exc:
            log.error("KBManager failed to load: %s", exc)
            self._kb = None

    # ------------------------------------------------------------------

    def query(self, text: str, top_n: int = 3) -> List[KBResult]:
        """
        Search the knowledge base for text.

        Returns up to top_n results sorted by confidence descending.
        Returns empty list if no match or KB unavailable.
        """
        if not self._kb or not text.strip():
            return []
        try:
            raw = self._kb.query(text, top_n=top_n)
            results = []
            for r in raw:
                results.append(KBResult(
                    entry_id   = getattr(r, "entry_id", ""),
                    category   = getattr(r, "category", ""),
                    intent     = getattr(r, "intent", ""),
                    response   = getattr(r, "response", ""),
                    confidence = getattr(r, "confidence", 0.0),
                    priority   = getattr(r, "priority", 3),
                ))
            return results
        except Exception as exc:
            log.warning("KB query error: %s", exc)
            return []

    def get_best_response(self, text: str) -> str:
        """Return the best single response string for a query."""
        if not self._kb:
            return self._fallback()
        try:
            return self._kb.get_best_response(text) or self._fallback()
        except Exception:
            return self._fallback()

    def get_emergency_info(self) -> str:
        """Return the emergency assistance knowledge entry."""
        if not self._kb:
            return (
                "EMERGENCY CONTACTS:\n"
                "• Police: 100\n"
                "• Childline: 1098\n"
                "• National Emergency: 112\n"
                "• Women's Helpline: 1091"
            )
        try:
            return self._kb.get_emergency_response()
        except Exception:
            return "Call 100 (Police) or 1098 (Childline) immediately."

    def get_by_category(self, category: str) -> List[KBResult]:
        """Return all entries in a specific category."""
        if not self._kb:
            return []
        try:
            raw = self._kb.query_by_category(category)
            return [
                KBResult(
                    entry_id   = getattr(r, "entry_id", ""),
                    category   = category,
                    intent     = getattr(r, "intent", ""),
                    response   = getattr(r, "response", ""),
                    confidence = 1.0,
                    priority   = getattr(r, "priority", 3),
                )
                for r in raw
            ]
        except Exception:
            return []

    @lru_cache(maxsize=1)
    def get_categories(self) -> List[str]:
        """Return the list of all available KB categories."""
        if not self._kb:
            return []
        try:
            cats = self._kb.list_categories()
            # list_categories returns a formatted string; split it
            lines = [ln.strip().lstrip("•-").strip() for ln in cats.splitlines() if ln.strip()]
            return [ln for ln in lines if ln]
        except Exception:
            return []

    def get_suggestions(self, intent_family: str = "default") -> List[str]:
        """Return context-aware quick-action suggestion labels."""
        return self._SUGGESTIONS.get(intent_family, self._SUGGESTIONS["default"])

    def stats(self) -> dict:
        """Return KB statistics dictionary."""
        if not self._kb:
            return {"total_entries": 0, "total_queries": 0}
        try:
            return self._kb.get_stats()
        except Exception:
            return {}

    # ------------------------------------------------------------------

    def _fallback(self) -> str:
        return (
            "I'm here to help. You can ask me about:\n"
            "• Human trafficking awareness\n"
            "• Risk assessment\n"
            "• Job offer analysis\n"
            "• Emergency help and helplines\n"
            "• Legal rights and reporting"
        )
