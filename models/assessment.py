"""
AegisAI — Assessment Models
=============================
Data structures for the risk assessment wizard.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List


class RiskLevel(Enum):
    """
    Risk classification levels produced by the expert system.

    Attributes:
        label    : Human-readable name shown in the UI
        color    : Hex colour for the risk badge
        severity : Numeric severity 0–4 for comparisons
        emoji    : Visual indicator emoji
    """
    UNKNOWN  = ("Not Assessed",  "#64748b", 0, "❔")
    LOW      = ("Low Risk",      "#4ade80", 1, "🟢")
    MEDIUM   = ("Medium Risk",   "#fbbf24", 2, "🟡")
    HIGH     = ("High Risk",     "#f87171", 3, "🔴")
    CRITICAL = ("Critical Risk", "#ef4444", 4, "🚨")

    def __init__(self, label: str, color: str, severity: int, emoji: str) -> None:
        self.label    = label
        self.color    = color
        self.severity = severity
        self.emoji    = emoji

    @classmethod
    def from_string(cls, s: str) -> "RiskLevel":
        """Convert a string like 'HIGH' or 'CRITICAL' to the enum member."""
        mapping = {
            "LOW":      cls.LOW,
            "MEDIUM":   cls.MEDIUM,
            "HIGH":     cls.HIGH,
            "CRITICAL": cls.CRITICAL,
        }
        return mapping.get(s.upper(), cls.UNKNOWN)


@dataclass
class AssessmentQuestion:
    """
    A single question in the risk assessment questionnaire.

    Attributes:
        qid      : Unique question ID (e.g. "q01")
        text     : The question text shown to the user
        fact_key : Fact key asserted in Working Memory when answered Yes
        weight   : Score contribution when answered Yes (positive = risk factor)
        step     : Which wizard step (1–6) this question belongs to
        step_name: Display name for the wizard step
        category : Thematic category for reporting
    """
    qid:       str
    text:      str
    fact_key:  str
    weight:    int
    step:      int
    step_name: str
    category:  str = ""


@dataclass
class AssessmentResult:
    """
    The final output of a completed risk assessment.

    Attributes:
        risk_level      : Classified risk level enum
        risk_score      : Raw accumulated score (0–200+)
        risk_pct        : Percentage (0.0–100.0) for gauge display
        summary         : One-paragraph human-readable summary
        recommendations : List of specific advice strings
        actions         : Immediate action items
        facts           : Dict of asserted facts used for inference
        report_lines    : Formatted lines for the full report card
    """
    risk_level:      RiskLevel
    risk_score:      int
    risk_pct:        float
    summary:         str
    recommendations: List[str]      = field(default_factory=list)
    actions:         List[str]      = field(default_factory=list)
    facts:           dict           = field(default_factory=dict)
    report_lines:    List[str]      = field(default_factory=list)
