"""
AegisAI — Assessment Service
==============================
Stateful wizard guiding user through 15 risk questions.
Persists answers in SQLite and triggers RuleEngine evaluation.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

from models.assessment import AssessmentQuestion, AssessmentResult, RiskLevel
from services.database_service import DatabaseService
from services.session_service import SessionService

log = logging.getLogger(__name__)


class WizardState(Enum):
    IDLE       = auto()
    IN_PROGRESS = auto()
    COMPLETE   = auto()


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

TOTAL_STEPS = 6
TOTAL_QUESTIONS = len(QUESTIONS)


class AssessmentService:
    """
    Manages the risk assessment wizard lifecycle.
    Saves answers in SQLite as they are provided.
    """

    def __init__(self, rule_engine) -> None:
        self._engine  = rule_engine
        self._state   = WizardState.IDLE
        self._index   = 0                    # current question index
        self._facts: Dict[str, bool] = {}   # accumulated facts
        self._db      = DatabaseService()
        self._session = SessionService.instance()

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

    # ------------------------------------------------------------------

    def start(self) -> AssessmentQuestion:
        """Reset and start a new assessment session."""
        self._index = 0
        self._facts = {}
        self._state = WizardState.IN_PROGRESS

        # Clear previous records for this session in the database
        self._db.clear_assessment_answers(self._session.session_id)
        log.info("Assessment started. Database cleared for new answers.")
        return QUESTIONS[0]

    def answer(self, response: str) -> "AssessmentQuestion | AssessmentResult":
        """
        Submit an answer for the current question and persist it to SQLite.
        """
        if not self.is_active:
            raise RuntimeError("Assessment is not active. Call start() first.")

        q   = QUESTIONS[self._index]
        yes = response.strip().lower() in ("yes", "y", "true", "1")

        self._facts[q.fact_key] = yes
        log.debug("Q%02d [%s] = %s", self._index + 1, q.fact_key, yes)

        # Persist answer to SQLite DB
        self._db.save_assessment_answer(self._session.session_id, q.qid, yes)

        self._index += 1

        if self._index >= TOTAL_QUESTIONS:
            return self._finish()
        else:
            return QUESTIONS[self._index]

    def abort(self) -> None:
        """Cancel the current assessment without producing a result."""
        self._state = WizardState.IDLE
        self._facts = {}
        self._index = 0
        self._db.clear_assessment_answers(self._session.session_id)
        log.info("Assessment aborted and database entries cleared.")

    def get_partial_result(self) -> Optional[AssessmentResult]:
        """Return a preliminary result mid-assessment (for live gauge)."""
        if not self._facts:
            return None
        return self._engine.assess(self._facts)

    # ------------------------------------------------------------------

    def _finish(self) -> AssessmentResult:
        self._state = WizardState.COMPLETE
        result = self._engine.assess(self._facts)
        log.info(
            "Assessment complete. Risk: %s  Score: %d",
            result.risk_level.name,
            result.risk_score
        )

        # Notify global session to save risk and update UI header/observers
        self._session.complete_assessment(result)
        return result
