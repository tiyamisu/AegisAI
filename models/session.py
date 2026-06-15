"""
AegisAI — App Session Model
=============================
Global application session state shared across all modules.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from .assessment import RiskLevel


@dataclass
class AppSession:
    """
    Holds transient application-wide state for a single user session.

    This object is managed by SessionService and shared (read-only) by
    UI components that need to react to state changes.

    Attributes:
        current_page        : Name of the currently visible page
        risk_level          : Most recent risk assessment result
        risk_score          : The numeric score computed by the expert rules
        is_emergency        : Whether the situation is flagged as emergency
        assessment_active   : True while assessment wizard is running
        assessment_complete : True after wizard finishes
        scam_mode           : True while scam analyzer is waiting for text input
        message_count       : Total messages exchanged in this session
    """
    current_page:         str       = "dashboard"
    risk_level:           RiskLevel = RiskLevel.UNKNOWN
    risk_score:           int       = 0
    is_emergency:         bool      = False
    assessment_active:    bool      = False
    assessment_complete:  bool      = False
    scam_mode:            bool      = False
    message_count:        int       = 0

    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Reset session to initial state (keeps current_page)."""
        self.risk_level          = RiskLevel.UNKNOWN
        self.risk_score          = 0
        self.is_emergency         = False
        self.assessment_active   = False
        self.assessment_complete = False
        self.scam_mode           = False
        self.message_count       = 0
