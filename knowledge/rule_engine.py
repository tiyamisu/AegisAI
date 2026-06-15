"""
AegisAI — Rule Engine
=======================
Wraps engine/expert_system.py with a clean typed interface.
Provides forward-chaining inference for risk classification.
"""
from __future__ import annotations

import logging
import sys
import os
from typing import Dict

from models.assessment import RiskLevel, AssessmentResult

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

log = logging.getLogger(__name__)


class RuleEngine:
    """
    Adapter over the AegisAI forward-chaining expert system.

    Public methods
    --------------
    assess(facts: dict) -> AssessmentResult
    """

    def __init__(self) -> None:
        try:
            from expert_system import ExpertSystemEngine
            self._engine = ExpertSystemEngine()
            log.info("RuleEngine ready. 52 rules loaded.")
        except Exception as exc:
            log.error("RuleEngine init failed: %s", exc)
            self._engine = None

    # ------------------------------------------------------------------

    def assess(self, facts: Dict[str, bool]) -> AssessmentResult:
        """
        Run forward-chaining inference on the provided facts dict.

        Parameters
        ----------
        facts : Dict[str, bool]
            Mapping of fact_key -> bool (True = indicator present)

        Returns
        -------
        AssessmentResult with risk_level, score, summary, actions
        """
        if not self._engine:
            return self._fallback_result(facts)

        try:
            raw = self._engine.quick_assess(facts)
            level = RiskLevel.from_string(getattr(raw, "risk_level", "UNKNOWN"))
            score = int(getattr(raw, "risk_score", 0))

            # Clamp pct to 0–100
            pct = min(score / 1.2, 100.0)

            summary = getattr(raw, "summary", self._make_summary(level))
            actions = list(getattr(raw, "actions", []))

            recs = self._make_recommendations(level, facts)

            report_lines = [
                f"Risk Level : {level.emoji}  {level.label}",
                f"Risk Score : {score} / 120",
                f"Suspicion  : {pct:.1f}%",
                "",
                "Indicators Found:",
            ] + [f"  ✓ {k.replace('_', ' ').title()}" for k, v in facts.items() if v]

            return AssessmentResult(
                risk_level      = level,
                risk_score      = score,
                risk_pct        = pct,
                summary         = summary,
                recommendations = recs,
                actions         = actions,
                facts           = facts,
                report_lines    = report_lines,
            )

        except Exception as exc:
            log.error("Assessment inference error: %s", exc)
            return self._fallback_result(facts)

    # ------------------------------------------------------------------

    @staticmethod
    def _make_summary(level: RiskLevel) -> str:
        summaries = {
            RiskLevel.LOW:      "Your responses suggest a low risk situation. Stay informed and alert.",
            RiskLevel.MEDIUM:   "Some risk indicators are present. Exercise caution and verify your situation.",
            RiskLevel.HIGH:     "Significant risk factors detected. Please seek assistance as soon as possible.",
            RiskLevel.CRITICAL: "CRITICAL RISK DETECTED. Your safety may be in immediate danger. Act now.",
            RiskLevel.UNKNOWN:  "Assessment could not be completed. Please try again.",
        }
        return summaries.get(level, "Assessment complete.")

    @staticmethod
    def _make_recommendations(level: RiskLevel, facts: dict) -> list:
        base = {
            RiskLevel.LOW: [
                "Continue learning about trafficking warning signs.",
                "Share awareness with friends and family.",
                "Know your emergency helpline numbers.",
            ],
            RiskLevel.MEDIUM: [
                "Contact a trusted person about your concerns.",
                "Verify any job offers through official channels.",
                "Keep the NHRC helpline (14433) saved.",
                "Document any suspicious interactions.",
            ],
            RiskLevel.HIGH: [
                "Call the Anti-Trafficking Helpline: 14433",
                "Contact Police: 100 or Emergency: 112",
                "Reach out to Childline if a minor is involved: 1098",
                "Do not sign any documents under pressure.",
                "Try to contact a family member or trusted friend.",
            ],
            RiskLevel.CRITICAL: [
                "CALL POLICE IMMEDIATELY: 100",
                "CALL NATIONAL EMERGENCY: 112",
                "CALL CHILDLINE (if minor involved): 1098",
                "Try to leave the situation safely if possible.",
                "If unsafe, signal for help silently.",
                "Do NOT hand over any documents.",
            ],
        }
        return base.get(level, ["Seek guidance from a trusted source."])

    @staticmethod
    def _fallback_result(facts: dict) -> AssessmentResult:
        yes_count = sum(1 for v in facts.values() if v)
        if yes_count == 0:
            level = RiskLevel.LOW
        elif yes_count <= 2:
            level = RiskLevel.MEDIUM
        elif yes_count <= 5:
            level = RiskLevel.HIGH
        else:
            level = RiskLevel.CRITICAL

        score = yes_count * 10
        return AssessmentResult(
            risk_level      = level,
            risk_score      = score,
            risk_pct        = min(score / 1.2, 100.0),
            summary         = RuleEngine._make_summary(level),
            recommendations = RuleEngine._make_recommendations(level, facts),
            actions         = [],
            facts           = facts,
        )
