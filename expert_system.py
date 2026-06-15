"""
AegisAI — Expert System Engine
================================
Rule-based forward-chaining expert system for risk classification
and response guidance. Wraps engine/expert_system.py and exposes
a clean session-oriented API for the chatbot.

Author  : AegisAI Team
Version : 1.0
"""

import sys
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Resolve import path
# ---------------------------------------------------------------------------
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

try:
    from engine.expert_system import (
        ExpertSystemSession as _CoreSession,
        RiskClassifier      as _CoreClassifier,
        RiskLevel,
        Urgency,
        TraffickingType,
        RISK_QUESTIONS,
        RULE_BASE,
    )
    _ENGINE_LOADED = True
except ImportError:
    _ENGINE_LOADED = False
    # Minimal stubs so the rest of the module still runs
    class RiskLevel:            # type: ignore
        UNKNOWN  = "UNKNOWN"
        LOW      = "LOW"
        MEDIUM   = "MEDIUM"
        HIGH     = "HIGH"
        CRITICAL = "CRITICAL"
    class Urgency:              # type: ignore
        ROUTINE   = 1
        ADVISORY  = 2
        ALERT     = 3
        URGENT    = 4
        EMERGENCY = 5
    class TraffickingType:      # type: ignore
        UNKNOWN = "UNKNOWN"
    RISK_QUESTIONS = []
    RULE_BASE      = []


# ===========================================================================
# RISK LEVEL METADATA — human-readable decorations
# ===========================================================================

RISK_METADATA: Dict[str, Dict] = {
    "LOW": {
        "emoji":   "🟢",
        "label":   "LOW RISK",
        "color":   "#28a745",
        "summary": (
            "You appear to be in a safe situation. Stay informed about "
            "trafficking warning signs and contact us if your situation changes."
        ),
        "actions": [
            "Browse educational resources",
            "Learn about warning signs",
            "Take the job offer safety check",
        ],
    },
    "MEDIUM": {
        "emoji":   "🟡",
        "label":   "MEDIUM RISK",
        "color":   "#ffc107",
        "summary": (
            "Some warning signs are present. We recommend reaching out to "
            "a trusted adult or one of the helplines listed below."
        ),
        "actions": [
            "Review warning signs for your situation",
            "Contact a trusted adult or NGO",
            "Consider calling a helpline for confidential advice",
            "Read about your legal rights",
        ],
    },
    "HIGH": {
        "emoji":   "🔴",
        "label":   "HIGH RISK",
        "color":   "#dc3545",
        "summary": (
            "⚠️ Significant risk indicators detected. You may be in or "
            "approaching a dangerous situation. Please contact authorities "
            "or a support organisation immediately."
        ),
        "actions": [
            "Contact police (100) or Childline (1098) NOW",
            "Reach out to a trusted adult",
            "Read the emergency guidance",
            "Consider a safe exit plan",
        ],
    },
    "CRITICAL": {
        "emoji":   "🚨",
        "label":   "CRITICAL RISK",
        "color":   "#8b0000",
        "summary": (
            "🚨 CRITICAL: You are in a VERY DANGEROUS SITUATION. "
            "Please seek help IMMEDIATELY.\n"
            "Call 100 (Police) or 1098 (Childline) right now."
        ),
        "actions": [
            "Call Police: 100 IMMEDIATELY",
            "Call Childline: 1098 IMMEDIATELY",
            "Use Silent Help Signal if you cannot speak",
            "Go to the nearest public place",
        ],
    },
    "UNKNOWN": {
        "emoji":   "⚪",
        "label":   "NOT ASSESSED",
        "color":   "#6c757d",
        "summary": "Risk level not yet assessed. Take the risk assessment to find out.",
        "actions": [],
    },
}


# ===========================================================================
# ASSESSMENT RESULT
# ===========================================================================

@dataclass
class AssessmentResult:
    """Structured result returned after a complete expert system session."""
    risk_level:       str          = "UNKNOWN"
    risk_score:       int          = 0
    urgency:          int          = 1
    trafficking_type: str          = "UNKNOWN"
    fired_rules:      List[str]    = field(default_factory=list)
    show_flags:       List[str]    = field(default_factory=list)
    score_breakdown:  str          = ""
    summary:          str          = ""
    actions:          List[str]    = field(default_factory=list)
    emoji:            str          = "⚪"
    color:            str          = "#6c757d"
    is_emergency:     bool         = False
    raw_facts:        Dict         = field(default_factory=dict)

    @property
    def label(self) -> str:
        return RISK_METADATA.get(self.risk_level, {}).get("label", self.risk_level)


# ===========================================================================
# EXPERT SYSTEM ENGINE
# ===========================================================================

class ExpertSystemEngine:
    """
    Public API for the AegisAI Expert System.

    Manages a single inference session at a time and provides
    methods to assert facts, run inference, and retrieve results.

    Usage:
        engine = ExpertSystemEngine()
        engine.new_session()
        engine.assert_fact("user_in_immediate_danger", True)
        engine.assert_fact("documents_confiscated", True)
        result = engine.conclude()
        print(result.risk_level, result.summary)
    """

    def __init__(self):
        """Initialise the engine and log KB availability."""
        self._session: Optional[Any] = None
        self._result:  Optional[AssessmentResult] = None
        self._facts_asserted: Dict[str, Any] = {}

        if _ENGINE_LOADED:
            print("[ExpertSystem] Engine loaded successfully. "
                  f"Rules: {len(RULE_BASE)}, Questions: {len(RISK_QUESTIONS)}")
        else:
            print("[ExpertSystem] WARNING: engine/expert_system.py not found. "
                  "Running in fallback mode.")

    # ------------------------------------------------------------------
    # SESSION MANAGEMENT
    # ------------------------------------------------------------------

    def new_session(self):
        """
        Start a fresh inference session.
        Clears all previously asserted facts.
        """
        self._facts_asserted = {}
        self._result         = None

        if _ENGINE_LOADED:
            self._session = _CoreSession()
        else:
            self._session = None

    def assert_fact(self, name: str, value: Any, confidence: float = 1.0):
        """
        Assert a user fact into the working memory.

        Args:
            name:       Fact name (must match a known fact key)
            value:      Fact value (bool, str, int, etc.)
            confidence: 0.0–1.0 confidence level
        """
        self._facts_asserted[name] = value

        if self._session is not None and _ENGINE_LOADED:
            try:
                self._session.assert_user_fact(name, value, confidence)
            except Exception as e:
                print(f"[ExpertSystem] Warning: could not assert fact {name!r}: {e}")

    def complete_assessment(self):
        """
        Mark the risk assessment as complete and trigger classification rules.
        Call this after all facts from the questionnaire have been asserted.
        """
        if self._session is not None and _ENGINE_LOADED:
            self._session.complete_assessment()

    # ------------------------------------------------------------------
    # INFERENCE
    # ------------------------------------------------------------------

    def run_inference(self) -> AssessmentResult:
        """
        Execute the forward-chaining inference engine.

        Returns:
            AssessmentResult with risk level, score, and recommended actions
        """
        if not _ENGINE_LOADED or self._session is None:
            return self._fallback_result()

        try:
            self._session.complete_assessment()
            self._session.run_inference()
            raw = self._session.get_result()
        except Exception as e:
            print(f"[ExpertSystem] Inference error: {e}")
            return self._fallback_result()

        risk_level  = raw.get("level", "UNKNOWN")
        meta        = RISK_METADATA.get(risk_level, RISK_METADATA["UNKNOWN"])

        result = AssessmentResult(
            risk_level       = risk_level,
            risk_score       = raw.get("score", 0),
            urgency          = raw.get("all_facts", {}).get("urgency", 1),
            trafficking_type = raw.get("all_facts", {}).get(
                                  "trafficking_type_suspected", "UNKNOWN"),
            fired_rules      = raw.get("fired_rules", []),
            show_flags       = list(raw.get("show_flags", {}).keys()),
            score_breakdown  = raw.get("score_breakdown", ""),
            summary          = meta["summary"],
            actions          = meta["actions"],
            emoji            = meta["emoji"],
            color            = meta["color"],
            is_emergency     = self._session.is_emergency(),
            raw_facts        = raw.get("all_facts", {}),
        )
        self._result = result
        return result

    def _fallback_result(self) -> AssessmentResult:
        """
        Create a fallback result when the core engine is unavailable.
        Uses a simple heuristic based on directly asserted facts.
        """
        score = 0
        if self._facts_asserted.get("user_in_immediate_danger"):
            score += 100
        if self._facts_asserted.get("physical_abuse_present"):
            score += 25
        if self._facts_asserted.get("sexual_exploitation"):
            score += 30
        if self._facts_asserted.get("documents_confiscated"):
            score += 20
        if self._facts_asserted.get("freedom_restricted"):
            score += 15
        if self._facts_asserted.get("threats_received"):
            score += 18
        if self._facts_asserted.get("wages_withheld"):
            score += 15
        if self._facts_asserted.get("debt_bondage_present"):
            score += 20
        if self._facts_asserted.get("isolated_from_family"):
            score += 12

        if score >= 100:
            level = "CRITICAL"
        elif score >= 51:
            level = "HIGH"
        elif score >= 21:
            level = "MEDIUM"
        else:
            level = "LOW"

        meta   = RISK_METADATA[level]
        return AssessmentResult(
            risk_level  = level,
            risk_score  = score,
            summary     = meta["summary"],
            actions     = meta["actions"],
            emoji       = meta["emoji"],
            color       = meta["color"],
            is_emergency= score >= 51,
        )

    # ------------------------------------------------------------------
    # DIRECT SCORING (for quick single-question evaluation)
    # ------------------------------------------------------------------

    def quick_assess(self, situation_flags: Dict[str, bool]) -> AssessmentResult:
        """
        Convenience method: assert multiple flags, run inference, return result.

        Args:
            situation_flags: e.g. {"user_in_immediate_danger": True, ...}

        Returns:
            AssessmentResult
        """
        self.new_session()
        for name, value in situation_flags.items():
            self.assert_fact(name, value)
        return self.run_inference()

    # ------------------------------------------------------------------
    # QUESTIONNAIRE
    # ------------------------------------------------------------------

    def get_questions(self) -> List[Dict]:
        """
        Return the list of risk assessment questions.

        Returns:
            List of question dicts with keys: qid, question, domain, yes_fact, yes_score
        """
        return RISK_QUESTIONS if _ENGINE_LOADED else []

    def get_question_count(self) -> int:
        """Return total number of root-level questions (no follow-ups)."""
        return sum(
            1 for q in RISK_QUESTIONS
            if not q.get("parent")
        ) if _ENGINE_LOADED else 0

    def process_question_answer(self, question: Dict, answer: bool):
        """
        Process a single questionnaire answer.

        Args:
            question: Question dict from get_questions()
            answer:   True for Yes, False for No
        """
        if answer and self._session is not None and _ENGINE_LOADED:
            try:
                self._session.process_risk_answer(question, answer)
            except Exception as e:
                print(f"[ExpertSystem] Error processing answer: {e}")
        elif answer:
            # Fallback: assert the fact and score manually
            fact  = question.get("yes_fact")
            value = question.get("yes_value", True)
            if fact:
                self._facts_asserted[fact] = value

    # ------------------------------------------------------------------
    # RESULTS
    # ------------------------------------------------------------------

    def get_last_result(self) -> Optional[AssessmentResult]:
        """Return the result from the most recent inference run."""
        return self._result

    def format_result_banner(self, result: AssessmentResult) -> str:
        """
        Format a human-readable assessment result banner.

        Args:
            result: AssessmentResult from run_inference()

        Returns:
            Formatted multi-line string
        """
        lines = [
            "=" * 55,
            f"  {result.emoji}  RISK ASSESSMENT COMPLETE  {result.emoji}",
            "=" * 55,
            f"  Risk Level : {result.label}",
            f"  Score      : {result.risk_score} points",
            "",
            "  Summary:",
            f"  {result.summary}",
            "",
        ]

        if result.actions:
            lines.append("  Recommended Actions:")
            for action in result.actions:
                lines.append(f"    ✓ {action}")
            lines.append("")

        if result.show_flags:
            lines.append("  Additional Resources:")
            for flag in result.show_flags[:4]:
                display = flag.replace("show_", "").replace("_", " ").title()
                lines.append(f"    → {display}")

        lines.append("=" * 55)
        return "\n".join(lines)

    def is_emergency_active(self) -> bool:
        """Return True if the current session is at URGENT or EMERGENCY level."""
        if self._session is not None and _ENGINE_LOADED:
            try:
                return self._session.is_emergency()
            except Exception:
                pass
        return self._facts_asserted.get("user_in_immediate_danger", False)


# ===========================================================================
# MODULE SELF-TEST
# ===========================================================================

if __name__ == "__main__":
    print("AegisAI Expert System Engine — Self Test")
    print("=" * 55)

    engine = ExpertSystemEngine()

    # --- Test 1: Critical risk ---
    print("\n[TEST 1] Critical Risk Scenario")
    result = engine.quick_assess({
        "user_in_immediate_danger": True,
        "documents_confiscated":    True,
        "physical_abuse_present":   True,
        "freedom_restricted":       True,
        "sexual_exploitation":      True,
    })
    print(engine.format_result_banner(result))

    # --- Test 2: Low risk ---
    print("\n[TEST 2] Low Risk Scenario")
    result = engine.quick_assess({
        "user_seeking_job":      True,
        "job_offer_suspicious":  False,
        "online_contact_suspicious": False,
    })
    print(f"  Risk: {result.emoji} {result.label} | Score: {result.risk_score}")

    # --- Test 3: Questions ---
    print(f"\n[TEST 3] Questions available: {engine.get_question_count()}")
