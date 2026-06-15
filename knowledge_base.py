"""
AegisAI — Knowledge Base Manager
=================================
Provides a clean, query-driven interface over the AegisAI knowledge base.
Supports keyword search, intent matching, category browsing, and fuzzy lookup.

Author  : AegisAI Team
Version : 1.0
"""

import re
import sys
import os
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Resolve import path for the data package
# ---------------------------------------------------------------------------
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

try:
    from data.knowledge_base import (
        KNOWLEDGE_BASE,
        KEYWORD_INDEX,
        CATEGORY_INDEX,
        EMERGENCY_ENTRY_IDS,
    )
    _KB_LOADED = True
except ImportError:
    _KB_LOADED = False
    KNOWLEDGE_BASE   = {}
    KEYWORD_INDEX    = {}
    CATEGORY_INDEX   = {}
    EMERGENCY_ENTRY_IDS = []


# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------
CATEGORIES = [
    "human_trafficking_basics",
    "warning_signs",
    "recruitment_scams",
    "child_trafficking",
    "forced_labour",
    "online_grooming",
    "victim_support",
    "emergency_assistance",
    "reporting_procedures",
    "legal_rights",
    "safety_measures",
    "ngo_support",
    "faqs",
]

CATEGORY_DISPLAY_NAMES = {
    "human_trafficking_basics": "Human Trafficking Basics",
    "warning_signs":            "Warning Signs",
    "recruitment_scams":        "Recruitment Scams",
    "child_trafficking":        "Child Trafficking",
    "forced_labour":            "Forced Labour",
    "online_grooming":          "Online Grooming",
    "victim_support":           "Victim Support",
    "emergency_assistance":     "Emergency Assistance",
    "reporting_procedures":     "Reporting Procedures",
    "legal_rights":             "Legal Rights",
    "safety_measures":          "Safety Measures",
    "ngo_support":              "NGO Support",
    "faqs":                     "FAQs",
}

# Fallback responses when no KB entry is found
_FALLBACK_RESPONSE = (
    "I'm not sure I understood that. "
    "You can ask me about:\n\n"
    "  • Human trafficking (types, signs, statistics)\n"
    "  • Warning signs and red flags\n"
    "  • Job offer safety check\n"
    "  • Risk assessment\n"
    "  • Emergency help and reporting\n"
    "  • Legal rights and NGO support\n\n"
    "Or type a number from the main menu to navigate.\n"
    "In an emergency, call 100 or 1098 immediately."
)

_EMERGENCY_RESPONSE = (
    "🆘 EMERGENCY — CALL THESE NUMBERS RIGHT NOW 🆘\n\n"
    "  🔴 Police Emergency  :  100  (24/7, Free)\n"
    "  🔴 Childline India   :  1098 (24/7, Free)\n"
    "  🔴 Women's Helpline  :  1091 (24/7, Free)\n"
    "  🔴 National Emergency:  112  (24/7, Free)\n\n"
    "If you cannot call: text your location to a trusted person, "
    "use the hand signal (palm up, tuck thumb, fold fingers), "
    "or go to the nearest public place and ask for help.\n\n"
    "YOU ARE NOT ALONE. HELP IS COMING."
)


# ===========================================================================
# QUERY RESULT DATACLASS
# ===========================================================================

class KBResult:
    """Encapsulates a single knowledge base query result."""

    def __init__(self,
                 entry_id:   str,
                 category:   str,
                 intent:     str,
                 response:   str,
                 confidence: float = 1.0):
        self.entry_id   = entry_id
        self.category   = category
        self.intent     = intent
        self.response   = response
        self.confidence = confidence        # 0.0–1.0 match score

    def __repr__(self) -> str:
        return (
            f"KBResult(id={self.entry_id!r}, category={self.category!r}, "
            f"intent={self.intent!r}, confidence={self.confidence:.2f})"
        )


# ===========================================================================
# KNOWLEDGE BASE MANAGER
# ===========================================================================

class KnowledgeBaseManager:
    """
    Central manager for the AegisAI knowledge base.

    Responsibilities:
      - Load and validate the knowledge base on startup
      - Provide keyword, intent, and category-based search
      - Return structured KBResult objects
      - Offer emergency-specific lookup
      - Track query statistics for reporting
    """

    def __init__(self):
        """Initialise the manager and validate the loaded KB."""
        self._kb:            Dict = KNOWLEDGE_BASE
        self._keyword_index: Dict = KEYWORD_INDEX
        self._category_index: Dict = CATEGORY_INDEX
        self._emergency_ids: List  = EMERGENCY_ENTRY_IDS
        self._query_count:   int   = 0
        self._miss_count:    int   = 0

        # Pre-compile intent keyword sets for O(1) lookup
        self._intent_map: Dict[str, List[str]] = self._build_intent_map()

        if not _KB_LOADED:
            print("[KBManager] WARNING: data/knowledge_base.py not found. "
                  "Using empty KB — responses will be limited.")

    # ------------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------------

    def _build_intent_map(self) -> Dict[str, List[str]]:
        """Build a map: intent_name → [entry_ids]."""
        intent_map: Dict[str, List[str]] = {}
        for eid, entry in self._kb.items():
            intent = entry.get("intent", "")
            if intent not in intent_map:
                intent_map[intent] = []
            intent_map[intent].append(eid)
        return intent_map

    def _tokenise(self, text: str) -> List[str]:
        """Lowercase and split text into tokens, removing punctuation."""
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return text.split()

    def _score_entry(self, tokens: List[str], entry: Dict) -> float:
        """
        Score an entry against a token list.
        Score = number of matching keywords / total keywords in entry.
        """
        keywords = [kw.lower() for kw in entry.get("keywords", [])]
        if not keywords:
            return 0.0
        matches = sum(1 for kw in keywords if any(kw in t or t in kw for t in tokens))
        return matches / len(keywords)

    # ------------------------------------------------------------------
    # PUBLIC QUERY METHODS
    # ------------------------------------------------------------------

    def query(self, user_input: str, top_n: int = 1) -> List[KBResult]:
        """
        Main query method. Returns the top_n best-matching KB results
        for a given user input string.

        Args:
            user_input: Raw text from the user
            top_n:      How many results to return

        Returns:
            List of KBResult sorted by confidence (highest first)
        """
        self._query_count += 1
        tokens = self._tokenise(user_input)
        scores: List[Tuple[float, str]] = []

        for eid, entry in self._kb.items():
            # Score against keywords
            score = self._score_entry(tokens, entry)

            # Boost score if any user query matches literally
            for uq in entry.get("user_queries", []):
                if uq.lower() in user_input.lower():
                    score = max(score, 0.85)
                    break

            if score > 0:
                scores.append((score, eid))

        # Sort by score descending
        scores.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, eid in scores[:top_n]:
            entry = self._kb[eid]
            results.append(KBResult(
                entry_id=eid,
                category=entry.get("category", ""),
                intent=entry.get("intent", ""),
                response=entry.get("response", ""),
                confidence=score,
            ))

        if not results:
            self._miss_count += 1

        return results

    def query_by_category(self, category: str) -> List[KBResult]:
        """
        Retrieve all entries for a given category.

        Args:
            category: One of the CATEGORIES constants

        Returns:
            List of KBResult for that category
        """
        ids = self._category_index.get(category, [])
        results = []
        for eid in ids:
            entry = self._kb.get(eid, {})
            results.append(KBResult(
                entry_id=eid,
                category=entry.get("category", category),
                intent=entry.get("intent", ""),
                response=entry.get("response", ""),
                confidence=1.0,
            ))
        return results

    def query_by_intent(self, intent: str) -> Optional[KBResult]:
        """
        Retrieve the first entry matching a specific intent name.

        Args:
            intent: Exact intent string e.g. 'define_trafficking'

        Returns:
            KBResult or None
        """
        ids = self._intent_map.get(intent, [])
        if not ids:
            return None
        eid   = ids[0]
        entry = self._kb.get(eid, {})
        return KBResult(
            entry_id=eid,
            category=entry.get("category", ""),
            intent=intent,
            response=entry.get("response", ""),
            confidence=1.0,
        )

    def get_emergency_response(self) -> str:
        """
        Return the highest-priority emergency response.
        Falls back to the built-in constant if KB is empty.
        """
        for eid in self._emergency_ids:
            entry = self._kb.get(eid)
            if entry:
                return entry.get("response", _EMERGENCY_RESPONSE)
        return _EMERGENCY_RESPONSE

    def get_fallback(self) -> str:
        """Return the standard fallback message for unrecognised input."""
        return _FALLBACK_RESPONSE

    def get_best_response(self, user_input: str) -> str:
        """
        Convenience method: query and return just the response string.
        Returns fallback if no match found.

        Args:
            user_input: User's raw text

        Returns:
            Response string
        """
        # Check for emergency keywords first
        emergency_kw = ["help me", "emergency", "in danger", "trapped",
                        "scared", "hurt", "held", "forced", "i need help now"]
        lower_input = user_input.lower()
        if any(kw in lower_input for kw in emergency_kw):
            return self.get_emergency_response()

        results = self.query(user_input, top_n=1)
        if results and results[0].confidence >= 0.1:
            return results[0].response
        return self.get_fallback()

    def get_category_overview(self, category: str) -> str:
        """
        Return a formatted overview of a category's content.

        Args:
            category: Category name

        Returns:
            Multi-line summary string
        """
        display = CATEGORY_DISPLAY_NAMES.get(category, category.replace("_", " ").title())
        results = self.query_by_category(category)
        if not results:
            return f"No content found for category: {display}"

        lines = [f"📚 {display} — {len(results)} topics available:\n"]
        for i, r in enumerate(results[:5], 1):
            intent_display = r.intent.replace("_", " ").title()
            lines.append(f"  {i}. {intent_display}")
        if len(results) > 5:
            lines.append(f"  ... and {len(results) - 5} more topics.")
        lines.append("\nType a question or topic to learn more.")
        return "\n".join(lines)

    def list_categories(self) -> str:
        """Return a formatted list of all available categories."""
        lines = ["Available knowledge categories:\n"]
        for i, cat in enumerate(CATEGORIES, 1):
            display = CATEGORY_DISPLAY_NAMES.get(cat, cat)
            count   = len(self._category_index.get(cat, []))
            lines.append(f"  [{i:02d}] {display} ({count} topics)")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # STATISTICS
    # ------------------------------------------------------------------

    def get_stats(self) -> Dict:
        """Return KB usage statistics."""
        return {
            "total_entries":  len(self._kb),
            "total_queries":  self._query_count,
            "missed_queries": self._miss_count,
            "hit_rate": (
                f"{((self._query_count - self._miss_count) / max(1, self._query_count)) * 100:.1f}%"
            ),
            "categories": {
                cat: len(ids)
                for cat, ids in self._category_index.items()
            },
        }

    def total_entries(self) -> int:
        """Return total number of KB entries."""
        return len(self._kb)


# ===========================================================================
# MODULE SELF-TEST
# ===========================================================================

if __name__ == "__main__":
    print("AegisAI Knowledge Base Manager — Self Test")
    print("=" * 50)
    mgr = KnowledgeBaseManager()
    print(f"KB loaded: {mgr.total_entries()} entries")

    # Test 1: keyword query
    print("\nTest 1: Query — 'what is human trafficking'")
    res = mgr.query("what is human trafficking", top_n=1)
    for r in res:
        print(f"  Match: {r.entry_id} | conf={r.confidence:.2f} | intent={r.intent}")

    # Test 2: category query
    print("\nTest 2: Category — emergency_assistance")
    cat_res = mgr.query_by_category("emergency_assistance")
    print(f"  Found {len(cat_res)} entries")

    # Test 3: emergency response
    print("\nTest 3: Emergency response snippet")
    emg = mgr.get_emergency_response()
    print(f"  {emg[:80]}...")

    # Test 4: statistics
    print("\nTest 4: Stats")
    for k, v in mgr.get_stats().items():
        if not isinstance(v, dict):
            print(f"  {k}: {v}")
