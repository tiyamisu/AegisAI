"""
AegisAI — Session Service
===========================
Singleton that holds global application state and persists it to SQLite.
All pages read from this and dispatch mutations through it.
"""
from __future__ import annotations

import logging
from models.session import AppSession
from models.assessment import RiskLevel, AssessmentResult
from services.database_service import DatabaseService

log = logging.getLogger(__name__)


class SessionService:
    """
    Application-wide state singleton integrated with SQLite persistence.

    Usage
    -----
    session = SessionService.instance()
    session.set_risk_level(RiskLevel.HIGH, 65, False)
    current = session.state.risk_level
    """

    _instance: "SessionService | None" = None
    _session_id = "user_session_001"  # Default session for single-user desktop app

    def __init__(self) -> None:
        self._db = DatabaseService()
        self._state = AppSession()
        self._on_risk_change_callbacks: list = []
        self._on_navigate_callbacks:    list = []
        self._load_or_create_session()

    @classmethod
    def instance(cls) -> "SessionService":
        """Return the singleton instance, creating it if necessary."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # ------------------------------------------------------------------

    @property
    def session_id(self) -> str:
        """Get the active session identifier."""
        return self._session_id

    @property
    def state(self) -> AppSession:
        """Read-only access to current session state."""
        return self._state

    def _load_or_create_session(self) -> None:
        """Load session properties from the database if they exist, else create new."""
        self._db.create_session(self._session_id)
        data = self._db.get_session(self._session_id)
        if data:
            self._state.risk_level = RiskLevel.from_string(data["risk_level"])
            self._state.risk_score = data["risk_score"]
            self._state.is_emergency = bool(data["is_emergency"])
            log.info(
                "Restored session state from database: Risk=%s, Score=%d",
                self._state.risk_level.name,
                self._state.risk_score
            )
        else:
            log.info("Initialized fresh session in database.")

    def set_risk_level(self, level: RiskLevel, score: int = 0, is_emergency: bool = False) -> None:
        """Update the session risk level, save to SQLite, and notify listeners."""
        old_level = self._state.risk_level
        self._state.risk_level = level
        self._state.risk_score = score
        self._state.is_emergency = is_emergency

        # Persist changes to database
        self._db.update_session_risk(self._session_id, level.name, score, is_emergency)

        if old_level != level:
            for cb in self._on_risk_change_callbacks:
                try:
                    cb(level)
                except Exception as exc:
                    log.warning("Risk callback error: %s", exc)

    def set_page(self, page: str) -> None:
        self._state.current_page = page
        for cb in self._on_navigate_callbacks:
            try:
                cb(page)
            except Exception as exc:
                log.warning("Nav callback error: %s", exc)

    def increment_messages(self) -> None:
        self._state.message_count += 1

    def start_assessment(self) -> None:
        self._state.assessment_active = True
        self._state.assessment_complete = False

    def complete_assessment(self, result: AssessmentResult) -> None:
        self._state.assessment_active = False
        self._state.assessment_complete = True
        self.set_risk_level(result.risk_level, result.risk_score, result.is_emergency)

    def start_scam_mode(self) -> None:
        self._state.scam_mode = True

    def end_scam_mode(self) -> None:
        self._state.scam_mode = False

    def reset(self) -> None:
        """Reset all session state and clear logs in database."""
        self._state.reset()
        self._db.delete_session(self._session_id)
        self._db.create_session(self._session_id)
        log.info("Session reset and database records cleared.")

        # Notify observers
        for cb in self._on_risk_change_callbacks:
            try:
                cb(RiskLevel.UNKNOWN)
            except Exception as exc:
                log.warning("Risk callback error during reset: %s", exc)

    # ------------------------------------------------------------------
    # Observer registration

    def on_risk_change(self, callback) -> None:
        """Register a callback(RiskLevel) for risk level changes."""
        self._on_risk_change_callbacks.append(callback)

    def on_navigate(self, callback) -> None:
        """Register a callback(str) for page navigation changes."""
        self._on_navigate_callbacks.append(callback)
