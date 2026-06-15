"""
AegisAI — Scam Detection Models
=================================
Data structures for the scam analyzer output.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class SuspicionLevel(Enum):
    """
    Risk classification for a job offer analysis.

    Attributes:
        label  : Display name
        color  : Hex badge colour
        advice : Short advice string shown in the report
        icon   : Icon emoji for the badge
    """
    SAFE      = ("Safe",             "#4ade80", "This appears to be a legitimate opportunity.",          "✅")
    LOW_RISK  = ("Low Risk",         "#86efac", "Minor concerns. Verify before accepting.",              "🔍")
    MODERATE  = ("Moderate Risk",    "#fbbf24", "Several red flags. Investigate thoroughly.",            "⚠️")
    HIGH_RISK = ("High Risk",        "#f87171", "Significant trafficking indicators detected!",          "🚨")
    VERY_HIGH = ("Very High Risk",   "#ef4444", "CRITICAL: Multiple trafficking red flags found!",       "🆘")

    def __init__(self, label: str, color: str, advice: str, icon: str) -> None:
        self.label = label
        self.color = color
        self.advice = advice
        self.icon   = icon

    @classmethod
    def from_string(cls, s: str) -> "SuspicionLevel":
        mapping = {
            "SAFE":      cls.SAFE,
            "LOW_RISK":  cls.LOW_RISK,
            "MODERATE":  cls.MODERATE,
            "HIGH_RISK": cls.HIGH_RISK,
            "VERY_HIGH": cls.VERY_HIGH,
        }
        return mapping.get(s.upper(), cls.SAFE)


@dataclass
class DetectionResult:
    """
    Output from the ScamService for a single job offer text analysis.

    Attributes:
        level           : Classified suspicion level
        suspicion_pct   : Percentage suspicion score (0.0–100.0)
        raw_score       : Raw accumulated indicator score
        top_flags       : List of most significant red flag descriptions
        category_scores : Score breakdown per indicator category
        recommendation  : Single-sentence actionable recommendation
        detailed_report : Full formatted report text
    """
    level:            SuspicionLevel
    suspicion_pct:    float
    raw_score:        int
    top_flags:        List[str]      = field(default_factory=list)
    category_scores:  Dict[str, int] = field(default_factory=dict)
    recommendation:   str           = ""
    detailed_report:  str           = ""

    @property
    def is_dangerous(self) -> bool:
        """True when the level is HIGH_RISK or VERY_HIGH."""
        return self.level in (SuspicionLevel.HIGH_RISK, SuspicionLevel.VERY_HIGH)
