"""
AegisAI — Assessment Service
==============================
Stateful wizard guiding user through 15 risk questions.
Tracks Yes / No / Not Sure answers and computes a simple 30-point score
(Yes=2, NotSure=1, No=0) alongside the expert-system inference score.

Bug Fixes in v2.1:
  - "Not Sure" now correctly contributes 1 point (not 0)
  - Removed duplicate complete_assessment() call (was called twice)
  - Q15 completion now reliably returns AssessmentResult
"""
from __future__ import annotations

import logging
from datetime import datetime
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

from models.assessment import AssessmentQuestion, AssessmentResult, RiskLevel
from services.database_service import DatabaseService
from services.session_service import SessionService

log = logging.getLogger(__name__)

# Maximum simple score: 15 questions × 2 points each
MAX_SIMPLE_SCORE = 30


class WizardState(Enum):
    IDLE        = auto()
    IN_PROGRESS = auto()
    COMPLETE    = auto()


# Answer weight constants
_WEIGHT_YES       = 2
_WEIGHT_NOT_SURE  = 1
_WEIGHT_NO        = 0


# ---------------------------------------------------------------------------
# Question bank — 15 questions in 6 themed steps
# ---------------------------------------------------------------------------
QUESTIONS: List[AssessmentQuestion] = [
    # ── Step 1: Your Current Situation ──────────────────────────────────────
    AssessmentQuestion("q01", "Is your freedom to leave your job or home being restricted by someone?",
                       "freedom_restricted",     15, 1, "Your Current Situation", "control"),
    AssessmentQuestion("q02", "Were you promised different conditions (pay, location, job type) than what you actually got?",
                       "deception_used",         12, 1, "Your Current Situation", "deception"),
    AssessmentQuestion("q03", "Are you cut off from your family, friends, or support network?",
                       "isolated_from_family",   10, 1, "Your Current Situation", "isolation"),

    # ── Step 2: Freedom & Movement ──────────────────────────────────────────
    AssessmentQuestion("q04", "Has someone confiscated your passport, ID card, or travel documents?",
                       "documents_confiscated",  20, 2, "Freedom & Movement", "control"),
    AssessmentQuestion("q05", "Are you being watched or escorted — unable to move freely on your own?",
                       "movement_monitored",     12, 2, "Freedom & Movement", "control"),

    # ── Step 3: Control & Coercion ──────────────────────────────────────────
    AssessmentQuestion("q06", "Have you received threats of harm (to you or your family) if you try to leave?",
                       "threats_received",       18, 3, "Control & Coercion", "threats"),
    AssessmentQuestion("q07", "Are you being forced to do things against your will through fear or violence?",
                       "physical_abuse_present", 18, 3, "Control & Coercion", "abuse"),

    # ── Step 4: Work & Compensation ─────────────────────────────────────────
    AssessmentQuestion("q08", "Are your wages being withheld, taken, or not paid as promised?",
                       "wages_withheld",         15, 4, "Work & Compensation", "labour"),
    AssessmentQuestion("q09", "Have you been told you owe a debt that keeps growing (debt bondage)?",
                       "debt_bondage_present",   15, 4, "Work & Compensation", "labour"),
    AssessmentQuestion("q10", "Are you being forced to work longer hours or in different conditions than agreed?",
                       "labour_exploitation",    10, 4, "Work & Compensation", "labour"),

    # ── Step 5: Safety & Exploitation ───────────────────────────────────────
    AssessmentQuestion("q11", "Have you been pressured or forced into any sexual activity?",
                       "sexual_exploitation",    25, 5, "Safety & Exploitation", "exploitation"),
    AssessmentQuestion("q12", "Are you in immediate danger right now?",
                       "user_in_immediate_danger", 30, 5, "Safety & Exploitation", "emergency"),

    # ── Step 6: Background & Context ────────────────────────────────────────
    AssessmentQuestion("q13", "Were you transported to your current location by someone who made promises to you?",
                       "cross_border_movement",  10, 6, "Background & Context", "movement"),
    AssessmentQuestion("q14", "Are there children in a similar situation around you?",
                       "user_is_minor",           8, 6, "Background & Context", "child"),
    AssessmentQuestion("q15", "Did an online contact (social media, messaging app) lead you to this situation?",
                       "online_contact_suspicious", 8, 6, "Background & Context", "online"),
]

TOTAL_STEPS     = 6
TOTAL_QUESTIONS = len(QUESTIONS)


def _simple_risk_level(pct: float) -> RiskLevel:
    """Map a simple-score percentage to a RiskLevel using the 4-band system."""
    if pct <= 25.0:
        return RiskLevel.LOW
    elif pct <= 50.0:
        return RiskLevel.MEDIUM
    elif pct <= 75.0:
        return RiskLevel.HIGH
    else:
        return RiskLevel.CRITICAL


class AssessmentService:
    """
    Manages the risk assessment wizard lifecycle.
    Saves answers in SQLite as they are provided.

    Answer values accepted by answer():
        "yes"       — contributes 2 simple points, asserts fact as True
        "not_sure"  — contributes 1 simple point,  asserts fact as False
        "no"        — contributes 0 simple points,  asserts fact as False
    """

    def __init__(self, rule_engine) -> None:
        self._engine        = rule_engine
        self._state         = WizardState.IDLE
        self._index         = 0
        self._facts:        Dict[str, bool] = {}
        self._yes_count:    int = 0
        self._no_count:     int = 0
        self._not_sure_count: int = 0
        self._simple_score: int = 0
        self._db            = DatabaseService()
        self._session       = SessionService.instance()

    # ------------------------------------------------------------------

    @property
    def is_active(self) -> bool:
        return self._state == WizardState.IN_PROGRESS

    @property
    def is_complete(self) -> bool:
        return self._state == WizardState.COMPLETE

    @property
    def current_question(self) -> Optional[AssessmentQuestion]:
        if self._state == WizardState.IN_PROGRESS and self._index < TOTAL_QUESTIONS:
            return QUESTIONS[self._index]
        return None

    def get_progress(self) -> Tuple[int, int, int, float]:
        """Returns (current_q_num, total_questions, current_step, pct_complete)."""
        q_num = self._index + 1
        step  = QUESTIONS[min(self._index, TOTAL_QUESTIONS - 1)].step
        pct   = (self._index / TOTAL_QUESTIONS) * 100
        return q_num, TOTAL_QUESTIONS, step, pct

    def get_answer_counts(self) -> Tuple[int, int, int]:
        """Returns (yes_count, no_count, not_sure_count)."""
        return self._yes_count, self._no_count, self._not_sure_count

    # ------------------------------------------------------------------

    def start(self) -> AssessmentQuestion:
        """Reset and start a new assessment session."""
        self._index          = 0
        self._facts          = {}
        self._yes_count      = 0
        self._no_count       = 0
        self._not_sure_count = 0
        self._simple_score   = 0
        self._state          = WizardState.IN_PROGRESS

        self._db.clear_assessment_answers(self._session.session_id)
        log.info("Assessment started. Total questions: %d", TOTAL_QUESTIONS)
        return QUESTIONS[0]

    def answer(self, response: str) -> "AssessmentQuestion | AssessmentResult":
        """
        Submit an answer for the current question.

        Parameters
        ----------
        response : str
            One of "yes", "not_sure", or "no"

        Returns
        -------
        AssessmentQuestion  — if more questions remain
        AssessmentResult    — when the final question (Q15) has been answered
        """
        if not self.is_active:
            raise RuntimeError("Assessment is not active. Call start() first.")

        if self._index >= TOTAL_QUESTIONS:
            # Safety guard: already exhausted — force finish
            return self._finish()

        q        = QUESTIONS[self._index]
        response = response.strip().lower()

        # Classify the response into one of three buckets
        if response in ("yes", "y", "true", "1"):
            fact_value           = True
            self._yes_count     += 1
            self._simple_score  += _WEIGHT_YES
        elif response in ("not_sure", "unsure", "maybe", "2"):
            fact_value            = False          # don't assert as a positive fact
            self._not_sure_count += 1
            self._simple_score   += _WEIGHT_NOT_SURE
        else:
            # "no", "n", "false", "0", or anything else
            fact_value          = False
            self._no_count     += 1
            self._simple_score += _WEIGHT_NO

        self._facts[q.fact_key] = fact_value
        log.debug("Q%02d [%s] response=%s  simple_score=%d",
                  self._index + 1, q.fact_key, response, self._simple_score)

        # Persist to DB
        self._db.save_assessment_answer(self._session.session_id, q.qid, fact_value)

        self._index += 1  # advance AFTER storing

        # ── KEY FIX: check completion BEFORE returning next question ──
        if self._index >= TOTAL_QUESTIONS:
            return self._finish()

        return QUESTIONS[self._index]

    def abort(self) -> None:
        """Cancel the current assessment without producing a result."""
        self._state          = WizardState.IDLE
        self._facts          = {}
        self._index          = 0
        self._yes_count      = 0
        self._no_count       = 0
        self._not_sure_count = 0
        self._simple_score   = 0
        self._db.clear_assessment_answers(self._session.session_id)
        log.info("Assessment aborted.")

    def get_partial_result(self) -> Optional[AssessmentResult]:
        """Return a preliminary result mid-assessment (for live gauge)."""
        if not self._facts:
            return None
        answered = self._index
        if answered == 0:
            return None
        # Compute partial simple score/pct
        partial_pct   = (self._simple_score / MAX_SIMPLE_SCORE) * 100
        partial_level = _simple_risk_level(partial_pct)
        result        = self._engine.assess(self._facts)
        # Override pct and level with simple system for gauge consistency
        result.simple_pct    = partial_pct
        result.simple_score  = self._simple_score
        result.risk_pct      = partial_pct
        result.risk_level    = partial_level
        return result

    # ------------------------------------------------------------------

    def _finish(self) -> AssessmentResult:
        """
        Called when all 15 questions have been answered.
        Computes final scores, builds the result, notifies session.
        NOTE: does NOT call session.complete_assessment() here —
        the UI layer does that to avoid double-calling observers.
        """
        self._state = WizardState.COMPLETE

        # ── Simple 30-point scoring (primary display system) ──────────
        simple_pct   = (self._simple_score / MAX_SIMPLE_SCORE) * 100
        simple_level = _simple_risk_level(simple_pct)

        # ── Expert system inference (secondary — for detailed report) ──
        try:
            expert_result = self._engine.assess(self._facts)
        except Exception as exc:
            log.warning("Expert engine failed, using simple scoring only: %s", exc)
            expert_result = None

        # ── Build recommendations based on simple risk level ──────────
        recs = _RECOMMENDATIONS.get(simple_level, [])

        # ── Summary ───────────────────────────────────────────────────
        summary = _SUMMARIES.get(simple_level, "Assessment complete.")

        # ── Emergency flag ────────────────────────────────────────────
        is_emergency = (simple_level == RiskLevel.CRITICAL or
                        self._facts.get("user_in_immediate_danger", False))

        # ── Assemble final result ─────────────────────────────────────
        report_lines = [
            f"Assessment Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"Risk Category   : {simple_level.emoji}  {simple_level.label}",
            f"Simple Score    : {self._simple_score} / {MAX_SIMPLE_SCORE}",
            f"Risk Percentage : {simple_pct:.1f}%",
            "",
            f"Answers:  ✅ Yes={self._yes_count}  ❌ No={self._no_count}  "
            f"❓ Not Sure={self._not_sure_count}",
            "",
            "Indicators Asserted:",
        ] + [f"  ✓ {k.replace('_', ' ').title()}"
             for k, v in self._facts.items() if v]

        result = AssessmentResult(
            risk_level      = simple_level,
            risk_score      = self._simple_score,
            risk_pct        = simple_pct,
            summary         = summary,
            recommendations = recs,
            actions         = list(getattr(expert_result, "actions", [])),
            facts           = dict(self._facts),
            report_lines    = report_lines,
            simple_score    = self._simple_score,
            simple_pct      = simple_pct,
            yes_count       = self._yes_count,
            no_count        = self._no_count,
            not_sure_count  = self._not_sure_count,
            is_emergency    = is_emergency,
            assessed_at     = datetime.now().strftime("%d %B %Y, %I:%M %p"),
        )

        log.info(
            "Assessment complete. Level=%s  Score=%d/%d (%.1f%%)"
            "  Yes=%d  No=%d  NotSure=%d",
            simple_level.name, self._simple_score, MAX_SIMPLE_SCORE, simple_pct,
            self._yes_count, self._no_count, self._not_sure_count,
        )
        return result


# ---------------------------------------------------------------------------
# Static content: recommendations and summaries per risk level
# ---------------------------------------------------------------------------

_RECOMMENDATIONS = {
    RiskLevel.LOW: [
        "Stay informed about the warning signs of human trafficking.",
        "Verify all employment opportunities through official channels.",
        "Keep trusted contacts and family members updated on your whereabouts.",
        "Save emergency helpline numbers: 112, 181, 1098.",
        "Learn how to safely report suspicious activity.",
    ],
    RiskLevel.MEDIUM: [
        "Exercise caution with anyone who contacted you with unsolicited offers.",
        "Verify the identity and registration of any recruiters before proceeding.",
        "Avoid sharing sensitive documents (ID, passport) with unverified parties.",
        "Document suspicious interactions with dates and details.",
        "Contact a trusted person about your concerns immediately.",
        "Keep the NHRC helpline (14433) and Women's Helpline (181) saved.",
    ],
    RiskLevel.HIGH: [
        "Seek assistance from trusted authorities or family members immediately.",
        "Contact the Anti-Trafficking Helpline: 14433 (NHRC).",
        "Call Police (100) or Emergency Services (112) if you feel unsafe.",
        "Avoid travelling with the recruiter or signing any documents under pressure.",
        "If a child is involved, contact Childline: 1098 (free, 24/7).",
        "Do not hand over your identity documents to anyone.",
        "Try to reach a public place, police station, or NGO shelter.",
    ],
    RiskLevel.CRITICAL: [
        "🚨 CALL EMERGENCY SERVICES NOW: 112",
        "🚨 CALL POLICE: 100",
        "🚨 CALL WOMEN'S HELPLINE: 181",
        "🚨 CALL CHILDLINE (if a minor is involved): 1098",
        "Seek immediate assistance — do not remain alone.",
        "If unsafe to call, send a silent SOS text or signal for help.",
        "Reach the nearest police station, hospital, or public place.",
        "Contact a trusted family member or friend immediately.",
        "Do NOT hand over any identity documents.",
        "Reach out to NGOs: IJM India, Prerana, Shakti Vahini.",
    ],
}

_SUMMARIES = {
    RiskLevel.LOW:
        "Your responses suggest a low-risk situation. "
        "While no immediate danger is indicated, staying informed and prepared is always wise.",
    RiskLevel.MEDIUM:
        "Some risk indicators are present in your responses. "
        "Exercise caution, verify the people around you, and reach out to a trusted person.",
    RiskLevel.HIGH:
        "Significant trafficking risk factors have been detected. "
        "Please seek assistance from trusted authorities or support services as soon as possible.",
    RiskLevel.CRITICAL:
        "CRITICAL RISK DETECTED. Your responses indicate you may be in immediate danger. "
        "Please contact emergency services or a trusted person RIGHT NOW.",
}
