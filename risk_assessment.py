"""
AegisAI — Risk Assessment Module
==================================
Manages the interactive, multi-step risk assessment questionnaire.
Drives the conversation with the user, collects answers, and
delegates scoring/inference to the ExpertSystemEngine.

Author  : AegisAI Team
Version : 1.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from expert_system import ExpertSystemEngine, AssessmentResult, RISK_METADATA


# ===========================================================================
# ENUMERATIONS & STATE
# ===========================================================================

class AssessmentState(Enum):
    """Finite states of a risk assessment session."""
    NOT_STARTED   = "NOT_STARTED"
    IN_PROGRESS   = "IN_PROGRESS"
    WAITING_INPUT = "WAITING_INPUT"
    COMPLETED     = "COMPLETED"
    ABORTED       = "ABORTED"


# ===========================================================================
# QUESTION MODEL
# ===========================================================================

@dataclass
class Question:
    """Represents a single risk assessment question."""
    qid:        str
    domain:     str
    text:       str
    yes_fact:   str
    yes_value:  Any  = True
    yes_score:  int  = 0
    follow_up:  Optional[str] = None   # qid of follow-up if answered Yes
    parent:     Optional[str] = None   # qid of parent question (if follow-up)

    def is_follow_up(self) -> bool:
        """Return True if this is a follow-up (conditional) question."""
        return self.parent is not None

    def to_dict(self) -> Dict:
        """Serialise to dictionary (compatible with engine.process_question_answer)."""
        return {
            "qid":       self.qid,
            "domain":    self.domain,
            "question":  self.text,
            "yes_fact":  self.yes_fact,
            "yes_value": self.yes_value,
            "yes_score": self.yes_score,
            "follow_up": self.follow_up,
        }


# ===========================================================================
# BUILT-IN QUESTION BANK
# (mirrors RISK_QUESTIONS from engine/expert_system.py for standalone use)
# ===========================================================================

_BUILTIN_QUESTIONS: List[Question] = [
    Question("RQ01",  "control",   "Is someone controlling where you go or who you can speak to?",
             "freedom_restricted", True, 15, follow_up="RQ01a"),
    Question("RQ01a", "control",   "Does that person use threats or physical force to control you?",
             "threats_received", True, 18, parent="RQ01"),
    Question("RQ02",  "deception", "Were you given false promises about a job, relationship, or opportunity?",
             "deception_used", True, 12, follow_up="RQ02a"),
    Question("RQ02a", "deception", "Are your actual conditions very different from what was promised?",
             "coercion_used", True, 13, parent="RQ02"),
    Question("RQ03",  "documents", "Has someone taken away your ID, passport, or Aadhaar?",
             "documents_confiscated", True, 20),
    Question("RQ04",  "labour",    "Are you working without being paid, or are your wages taken?",
             "wages_withheld", True, 15, follow_up="RQ04a"),
    Question("RQ04a", "labour",    "Do you owe a 'debt' to your employer that seems impossible to repay?",
             "debt_bondage_present", True, 20, parent="RQ04"),
    Question("RQ05",  "safety",    "Have you been physically hurt or threatened with violence?",
             "physical_abuse_present", True, 25),
    Question("RQ06",  "isolation", "Are you prevented from contacting your family or friends?",
             "isolated_from_family", True, 12),
    Question("RQ07",  "sexual",    "Are you being forced to do anything of a sexual nature against your will?",
             "sexual_exploitation", True, 30),
    Question("RQ08",  "safety",    "Are you in immediate danger right now?",
             "user_in_immediate_danger", True, 50),
    Question("RQ09",  "transport", "Were you transported to your current location without fully understanding where you were going?",
             "transportation_involved", True, 10, follow_up="RQ09a"),
    Question("RQ09a", "transport", "Did this involve crossing a state or international border?",
             "cross_border_movement", True, 10, parent="RQ09"),
    Question("RQ10",  "online",    "Did you meet someone online whose offer led to your current situation?",
             "online_contact_suspicious", True, 10),
    Question("RQ11",  "children",  "Are there children in the same situation as you?",
             "child_involved", True, 20),
]

# Map qid → Question for fast lookup
_Q_MAP: Dict[str, Question] = {q.qid: q for q in _BUILTIN_QUESTIONS}

# Root-level questions (not follow-ups), in order
_ROOT_QUESTIONS: List[Question] = [
    q for q in _BUILTIN_QUESTIONS if not q.is_follow_up()
]


# ===========================================================================
# DOMAIN LABELS
# ===========================================================================

_DOMAIN_LABELS = {
    "control":    "Control & Coercion",
    "deception":  "Deception & False Promises",
    "documents":  "Document Control",
    "labour":     "Labour Exploitation",
    "safety":     "Physical Safety",
    "isolation":  "Isolation",
    "sexual":     "Sexual Exploitation",
    "transport":  "Transportation",
    "online":     "Online Recruitment",
    "children":   "Child Involvement",
}


# ===========================================================================
# RISK ASSESSMENT MODULE
# ===========================================================================

class RiskAssessmentModule:
    """
    Manages the interactive risk assessment questionnaire.

    The assessment proceeds as a series of Yes/No questions.
    Certain Yes answers trigger immediate follow-up questions.
    After all questions are answered, the expert system computes
    the risk level via forward-chaining inference.

    Typical usage (from chatbot):
        ra = RiskAssessmentModule()
        ra.start()

        while not ra.is_complete():
            q = ra.current_question()
            answer = get_yes_no_from_user(q.text)
            ra.submit_answer(answer)

        result = ra.get_result()
    """

    def __init__(self, engine: Optional[ExpertSystemEngine] = None):
        """
        Args:
            engine: Optional ExpertSystemEngine instance.
                    If None, a new one is created internally.
        """
        self._engine:   ExpertSystemEngine = engine or ExpertSystemEngine()
        self._state:    AssessmentState    = AssessmentState.NOT_STARTED
        self._result:   Optional[AssessmentResult] = None

        # Questionnaire tracking
        self._queue:     List[Question] = []   # upcoming questions
        self._answered:  List[Dict]    = []    # history of answered questions
        self._current:   Optional[Question] = None
        self._q_index:   int = 0               # root question index

    # ------------------------------------------------------------------
    # SESSION CONTROL
    # ------------------------------------------------------------------

    def start(self):
        """
        Initialise a new risk assessment session.
        Resets all state and starts fresh.
        """
        self._engine.new_session()
        self._state    = AssessmentState.IN_PROGRESS
        self._result   = None
        self._answered = []
        self._q_index  = 0

        # Prime the queue with all root-level questions
        self._queue    = list(_ROOT_QUESTIONS)
        self._current  = None
        self._advance()

    def abort(self):
        """Abort the current assessment session."""
        self._state = AssessmentState.ABORTED
        self._current = None
        self._queue.clear()

    def is_complete(self) -> bool:
        """Return True if the assessment has finished."""
        return self._state == AssessmentState.COMPLETED

    def is_active(self) -> bool:
        """Return True if the assessment is currently in progress."""
        return self._state in (
            AssessmentState.IN_PROGRESS,
            AssessmentState.WAITING_INPUT,
        )

    def get_state(self) -> AssessmentState:
        """Return the current state of the assessment."""
        return self._state

    # ------------------------------------------------------------------
    # QUESTION FLOW
    # ------------------------------------------------------------------

    def current_question(self) -> Optional[Question]:
        """
        Return the question currently awaiting an answer.
        Returns None if there is no active question.
        """
        return self._current

    def current_question_text(self) -> str:
        """
        Return the text of the current question with formatting.
        Includes domain label and progress indicator.
        """
        if self._current is None:
            return ""

        domain = _DOMAIN_LABELS.get(self._current.domain, self._current.domain)
        answered = len([a for a in self._answered if not _Q_MAP.get(
            a.get("qid", ""), Question("", "", "", "")).is_follow_up()])
        total    = len(_ROOT_QUESTIONS)
        progress = f"[Question {min(answered + 1, total)} of {total}]"

        follow_note = " (follow-up)" if self._current.is_follow_up() else ""

        return (
            f"{progress} {domain}{follow_note}\n\n"
            f"  {self._current.text}\n\n"
            "  Answer: Yes (Y) / No (N)"
        )

    def submit_answer(self, answer: bool) -> Optional[str]:
        """
        Submit the user's answer to the current question.

        Args:
            answer: True for Yes, False for No

        Returns:
            Optional follow-up question text if a follow-up was triggered,
            None otherwise.
        """
        if self._current is None or not self.is_active():
            return None

        q = self._current

        # Record the answer
        self._answered.append({
            "qid":      q.qid,
            "question": q.text,
            "domain":   q.domain,
            "answer":   answer,
            "score":    q.yes_score if answer else 0,
        })

        # Delegate to expert system engine
        self._engine.process_question_answer(q.to_dict(), answer)

        # If Yes and there is a follow-up, insert it next in the queue
        if answer and q.follow_up:
            follow_q = _Q_MAP.get(q.follow_up)
            if follow_q:
                self._queue.insert(0, follow_q)

        # Advance to next question
        self._advance()

        return self.current_question_text() if self._current else None

    def _advance(self):
        """
        Move to the next question in the queue.
        If the queue is exhausted, complete the assessment.
        """
        if self._queue:
            self._current = self._queue.pop(0)
            self._state   = AssessmentState.WAITING_INPUT
        else:
            self._current = None
            self._complete()

    def _complete(self):
        """Finalise the assessment and compute the result."""
        self._state  = AssessmentState.COMPLETED
        self._result = self._engine.run_inference()

    # ------------------------------------------------------------------
    # RESULTS
    # ------------------------------------------------------------------

    def get_result(self) -> Optional[AssessmentResult]:
        """
        Return the final AssessmentResult.
        Returns None if assessment is not yet complete.
        """
        return self._result

    def get_formatted_result(self) -> str:
        """
        Return a human-readable formatted result string.
        """
        if self._result is None:
            return "Assessment not yet complete."
        return self._engine.format_result_banner(self._result)

    def get_score_breakdown(self) -> str:
        """
        Return a detailed breakdown of how the score was computed.
        """
        if not self._answered:
            return "No questions have been answered."

        lines = ["SCORE BREAKDOWN", "-" * 40]
        total = 0
        for record in self._answered:
            if record["answer"] and record["score"] > 0:
                domain = _DOMAIN_LABELS.get(record["domain"], record["domain"])
                lines.append(f"  +{record['score']:3d}  [{domain}] {record['question'][:55]}")
                total += record["score"]
        lines.append("-" * 40)
        lines.append(f"  TOTAL: {total} points")
        return "\n".join(lines)

    def get_answered_count(self) -> int:
        """Return how many questions have been answered."""
        return len(self._answered)

    def get_yes_count(self) -> int:
        """Return how many questions were answered Yes."""
        return sum(1 for a in self._answered if a["answer"])

    def get_progress_pct(self) -> float:
        """Return assessment progress as a percentage (0.0–100.0)."""
        total_root = len(_ROOT_QUESTIONS)
        answered_root = sum(
            1 for a in self._answered
            if not _Q_MAP.get(a.get("qid", ""),
                              Question("", "", "", "")).is_follow_up()
        )
        return (answered_root / max(1, total_root)) * 100

    def get_domain_scores(self) -> Dict[str, int]:
        """Return the accumulated score per domain."""
        domain_scores: Dict[str, int] = {}
        for record in self._answered:
            if record["answer"]:
                d = record["domain"]
                domain_scores[d] = domain_scores.get(d, 0) + record["score"]
        return domain_scores

    # ------------------------------------------------------------------
    # INTRO / OUTRO TEXT
    # ------------------------------------------------------------------

    @staticmethod
    def intro_text() -> str:
        """Return the assessment introduction message."""
        return (
            "━" * 55 + "\n"
            "  🔍  AegisAI RISK ASSESSMENT\n"
            "━" * 55 + "\n\n"
            "This assessment is completely CONFIDENTIAL.\n"
            "No personal data is stored or shared.\n\n"
            f"You will be asked up to {len(_ROOT_QUESTIONS)} questions.\n"
            "Answer YES (Y) or NO (N) to each.\n"
            "Type STOP at any time to exit the assessment.\n\n"
            "━" * 55 + "\n"
            "Ready? Let's begin.\n"
        )

    @staticmethod
    def outro_text(result: AssessmentResult) -> str:
        """Return a closing message appropriate to the risk level."""
        closings = {
            "LOW": (
                "✅ You appear to be in a safe situation.\n"
                "Stay informed — knowledge is your best protection.\n"
                "Remember: Childline (1098) and Police (100) are always available."
            ),
            "MEDIUM": (
                "⚠️  Some warning signs are present in your situation.\n"
                "Please consider reaching out to a trusted adult or one of our helplines.\n"
                "Childline: 1098 | Police: 100 | Women's Helpline: 1091"
            ),
            "HIGH": (
                "🔴 You may be in a dangerous situation.\n"
                "Please contact authorities or a support organisation immediately.\n"
                "Police: 100 | Childline: 1098 | NHRC: 14433"
            ),
            "CRITICAL": (
                "🚨 PLEASE SEEK HELP IMMEDIATELY.\n"
                "Call Police: 100  or  Childline: 1098  RIGHT NOW.\n"
                "If you cannot call, go to the nearest public place and ask for help."
            ),
        }
        return closings.get(result.risk_level, "Assessment complete. Stay safe.")


# ===========================================================================
# MODULE SELF-TEST
# ===========================================================================

if __name__ == "__main__":
    print("AegisAI Risk Assessment Module — Self Test")
    print("=" * 55)

    ra = RiskAssessmentModule()
    print(ra.intro_text())
    ra.start()

    # Simulate a High Risk scenario
    _answers = {
        "RQ01": True,   # freedom restricted
        "RQ01a": True,  # threats
        "RQ02": True,   # deception
        "RQ02a": True,  # coercion
        "RQ03": True,   # docs confiscated
        "RQ04": True,   # wages withheld
        "RQ04a": True,  # debt bondage
        "RQ05": False,  # no physical abuse
        "RQ06": True,   # isolated
        "RQ07": False,  # no sexual exploitation
        "RQ08": False,  # not immediate danger
        "RQ09": False,
        "RQ10": False,
        "RQ11": False,
    }

    while ra.is_active():
        q = ra.current_question()
        if q is None:
            break
        answer = _answers.get(q.qid, False)
        print(f"  Q: {q.text[:60]!r} → {'Yes' if answer else 'No'}")
        ra.submit_answer(answer)

    print("\n" + ra.get_score_breakdown())
    print("\n" + ra.get_formatted_result())
    print(f"\nProgress: {ra.get_progress_pct():.0f}%")
    print(f"Answered: {ra.get_answered_count()} | Yes: {ra.get_yes_count()}")
