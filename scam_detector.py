"""
AegisAI — Scam Detector Module
================================
Clean public interface for analysing job offer texts for human
trafficking recruitment scam indicators.
Wraps modules/scam_analyzer.py and provides structured results
and formatted reports for the chatbot and GUI.

Author  : AegisAI Team
Version : 1.0
"""

import sys
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Resolve import path
# ---------------------------------------------------------------------------
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

try:
    from modules.scam_analyzer import (
        ScamAnalyzer   as _CoreAnalyzer,
        SuspicionLevel,
        ALL_INDICATORS,
        AnalysisResult as _CoreResult,
    )
    _ANALYZER_LOADED = True
except ImportError:
    _ANALYZER_LOADED = False
    class SuspicionLevel:           # type: ignore
        SAFE          = "SAFE"
        LOW_RISK      = "LOW_RISK"
        MODERATE_RISK = "MODERATE_RISK"
        HIGH_RISK     = "HIGH_RISK"
        VERY_HIGH     = "VERY_HIGH"
    ALL_INDICATORS = []


# ===========================================================================
# DETECTION RESULT
# ===========================================================================

@dataclass
class DetectionResult:
    """
    Structured result returned from ScamDetector.analyze().

    Attributes:
        raw_text        : Original job description text
        total_score     : Raw score from matched indicators
        suspicion_pct   : Percentage (0–100) of suspicion
        level           : SuspicionLevel enum value
        level_label     : Human-readable risk label
        level_emoji     : Emoji for the risk level
        level_color     : Hex color for GUI display
        match_count     : Number of indicators matched
        top_flags       : Top 5 most concerning matches
        category_scores : Score breakdown by indicator category
        recommendation  : Assessment summary text
        action_required : What the user should do
        is_dangerous    : True if HIGH_RISK or VERY_HIGH
    """
    raw_text:        str          = ""
    total_score:     int          = 0
    suspicion_pct:   float        = 0.0
    level:           str          = "SAFE"
    level_label:     str          = "Safe"
    level_emoji:     str          = "🟢"
    level_color:     str          = "#28a745"
    match_count:     int          = 0
    top_flags:       List[str]    = field(default_factory=list)
    category_scores: Dict[str, int] = field(default_factory=dict)
    recommendation:  str          = ""
    action_required: str          = ""
    is_dangerous:    bool         = False


# ===========================================================================
# SUSPICION LEVEL METADATA
# ===========================================================================

_LEVEL_METADATA = {
    "SAFE": {
        "label": "✅ Safe",
        "emoji": "🟢",
        "color": "#28a745",
    },
    "LOW_RISK": {
        "label": "⚠️ Low Risk",
        "emoji": "🟡",
        "color": "#ffc107",
    },
    "MODERATE_RISK": {
        "label": "⚠️ Moderate Risk",
        "emoji": "🟠",
        "color": "#fd7e14",
    },
    "HIGH_RISK": {
        "label": "🔴 High Risk",
        "emoji": "🔴",
        "color": "#dc3545",
    },
    "VERY_HIGH": {
        "label": "🚨 Very High Risk",
        "emoji": "🚨",
        "color": "#8b0000",
    },
}


# ===========================================================================
# SCAM DETECTOR
# ===========================================================================

class ScamDetector:
    """
    Public API for the AegisAI job offer scam detection system.

    Analyses free-text job descriptions for indicators of human trafficking
    recruitment using pattern matching and weighted scoring.

    Usage:
        detector = ScamDetector()
        result   = detector.analyze("Earn 2 lakhs per month, no experience...")
        print(result.level_label)
        print(result.recommendation)
    """

    def __init__(self):
        """Initialise the detector and create the core analyzer."""
        self._analyzer: Optional[object] = None
        self._analysis_count: int = 0

        if _ANALYZER_LOADED:
            self._analyzer = _CoreAnalyzer()
            print(f"[ScamDetector] Loaded. Indicators: {len(ALL_INDICATORS)}")
        else:
            print("[ScamDetector] WARNING: modules/scam_analyzer.py not found. "
                  "Using fallback keyword detection.")

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def analyze(self, job_text: str) -> DetectionResult:
        """
        Analyse a job description text for scam/trafficking indicators.

        Args:
            job_text: Full text of the job advertisement or offer

        Returns:
            DetectionResult with complete analysis
        """
        if not job_text or not job_text.strip():
            return DetectionResult(
                raw_text=job_text,
                recommendation="No text provided to analyse.",
            )

        self._analysis_count += 1

        if _ANALYZER_LOADED and self._analyzer:
            return self._analyze_with_core(job_text)
        else:
            return self._fallback_analyze(job_text)

    def analyze_from_qa(self, answers: Dict[str, bool]) -> DetectionResult:
        """
        Analyse based on a structured Q&A about a job offer
        (alternative to full text analysis).

        Args:
            answers: Dict mapping question keys to bool answers

        Returns:
            DetectionResult
        """
        score = 0
        flags = []

        mappings = {
            "promised_high_salary":   ("Unrealistic salary promised",           8),
            "required_to_travel":     ("Travel/relocation required",            5),
            "documents_requested":    ("Documents demanded before starting",     9),
            "pay_upfront":            ("Upfront fee demanded",                   9),
            "no_written_contract":    ("No written contract offered",            7),
            "secrecy_demanded":       ("Secrecy from family demanded",          10),
            "overseas_posting":       ("Overseas posting with no verification",  6),
            "recruited_via_social":   ("Recruited via social media/WhatsApp",    5),
            "urgent_joining":         ("Urgency to join immediately",            5),
            "live_in_required":       ("Live-in arrangement required",           6),
            "vague_job_description":  ("Job description is vague/unclear",       4),
            "advance_payment_given":  ("Advance payment (debt trap setup)",      8),
        }

        for key, (desc, weight) in mappings.items():
            if answers.get(key, False):
                score  += weight
                flags.append(desc)

        # Map score to level
        ref_cap = 60
        pct = min(100.0, (score / max(1, ref_cap)) * 100)
        level = self._pct_to_level(pct)
        meta  = _LEVEL_METADATA.get(level, _LEVEL_METADATA["SAFE"])

        rec, action = self._get_recommendation(level)

        return DetectionResult(
            raw_text=str(answers),
            total_score=score,
            suspicion_pct=round(pct, 1),
            level=level,
            level_label=meta["label"],
            level_emoji=meta["emoji"],
            level_color=meta["color"],
            match_count=len(flags),
            top_flags=flags[:5],
            recommendation=rec,
            action_required=action,
            is_dangerous=level in ("HIGH_RISK", "VERY_HIGH"),
        )

    def format_report(self, result: DetectionResult, compact: bool = False) -> str:
        """
        Format a human-readable analysis report.

        Args:
            result:  DetectionResult from analyze()
            compact: If True, return a short summary

        Returns:
            Formatted string
        """
        if compact:
            return (
                f"{result.level_emoji} {result.level_label} "
                f"({result.suspicion_pct:.0f}% suspicious, "
                f"{result.match_count} flags)\n"
                f"{result.recommendation}"
            )

        lines = [
            "=" * 60,
            "  🔍  AegisAI JOB OFFER SCAM ANALYSIS",
            "=" * 60,
            f"  Suspicion Level  :  {result.level_emoji} {result.level_label}",
            f"  Suspicion Score  :  {result.suspicion_pct:.1f}%",
            f"  Indicators Found :  {result.match_count}",
            "",
        ]

        if result.top_flags:
            lines.append("  Top Red Flags Detected:")
            lines.append("  " + "─" * 40)
            for flag in result.top_flags:
                lines.append(f"    ⚠️  {flag}")
            lines.append("")

        if result.category_scores:
            lines.append("  Score by Category:")
            lines.append("  " + "─" * 40)
            sorted_cats = sorted(
                result.category_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )
            for cat, score in sorted_cats[:5]:
                display = cat.replace("_", " ").title()
                bar = "█" * min(score, 20)
                lines.append(f"    {display:<22} {bar} ({score})")
            lines.append("")

        lines += [
            "  Assessment:",
            "  " + "─" * 40,
            f"  {result.recommendation}",
            "",
            "  What to Do:",
            "  " + "─" * 40,
            f"{result.action_required}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def get_indicator_count(self) -> int:
        """Return the total number of loaded scam indicators."""
        return len(ALL_INDICATORS)

    def get_analysis_count(self) -> int:
        """Return how many analyses have been performed in this session."""
        return self._analysis_count

    # ------------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------------

    def _analyze_with_core(self, job_text: str) -> DetectionResult:
        """Delegate to the core ScamAnalyzer."""
        try:
            core_result: _CoreResult = self._analyzer.analyze(job_text)
            level = core_result.suspicion_level.value
            meta  = _LEVEL_METADATA.get(level, _LEVEL_METADATA["SAFE"])
            return DetectionResult(
                raw_text        = job_text,
                total_score     = core_result.total_score,
                suspicion_pct   = core_result.suspicion_pct,
                level           = level,
                level_label     = meta["label"],
                level_emoji     = meta["emoji"],
                level_color     = meta["color"],
                match_count     = len(core_result.matches),
                top_flags       = core_result.top_flags,
                category_scores = core_result.category_scores,
                recommendation  = core_result.recommendation,
                action_required = core_result.action_required,
                is_dangerous    = level in ("HIGH_RISK", "VERY_HIGH"),
            )
        except Exception as e:
            print(f"[ScamDetector] Core analysis error: {e}")
            return self._fallback_analyze(job_text)

    def _fallback_analyze(self, job_text: str) -> DetectionResult:
        """
        Simple keyword-based fallback when core analyzer is unavailable.
        Uses a curated set of the most important scam keywords.
        """
        text  = job_text.lower()
        score = 0
        flags = []

        _FALLBACK_INDICATORS = [
            ("passport will be kept",          10, "Document confiscation"),
            ("id will be held",                10, "Document confiscation"),
            ("cannot leave",                   10, "Forced contract"),
            ("work off debt",                  10, "Debt bondage"),
            ("no experience required",          4, "Vague requirements"),
            ("guaranteed salary",               5, "Unrealistic salary"),
            ("easy money",                      5, "Deceptive compensation"),
            ("send your photo",                 5, "Appearance targeting"),
            ("all expenses paid",               4, "Financial dependency"),
            ("overseas posting",                5, "Geographic isolation"),
            ("live-in required",                6, "Residential control"),
            ("registration fee",                8, "Fee extraction"),
            ("pay upfront",                     8, "Fee extraction"),
            ("no written contract",             7, "Contract avoidance"),
            ("do not tell family",              9, "Secrecy demand"),
            ("myanmar",                         8, "High-risk destination"),
            ("cambodia",                        8, "High-risk destination"),
            ("webcam job",                      9, "Online exploitation"),
            ("adult entertainment",             9, "Sexual exploitation"),
            ("penalty for leaving",             8, "Coercive control"),
            ("no phone allowed",                8, "Communication control"),
            ("urgent joining",                  4, "Urgency pressure"),
            ("flexible work",                   2, "Vague description"),
            ("hired on the spot",               5, "Irregular recruitment"),
            ("dm to apply",                     4, "Informal recruitment"),
        ]

        for keyword, weight, description in _FALLBACK_INDICATORS:
            if keyword in text:
                score  += weight
                flags.append(description)

        ref_cap = 60
        pct     = min(100.0, (score / ref_cap) * 100)
        level   = self._pct_to_level(pct)
        meta    = _LEVEL_METADATA.get(level, _LEVEL_METADATA["SAFE"])
        rec, action = self._get_recommendation(level)

        return DetectionResult(
            raw_text=job_text,
            total_score=score,
            suspicion_pct=round(pct, 1),
            level=level,
            level_label=meta["label"],
            level_emoji=meta["emoji"],
            level_color=meta["color"],
            match_count=len(flags),
            top_flags=list(set(flags))[:5],
            recommendation=rec,
            action_required=action,
            is_dangerous=level in ("HIGH_RISK", "VERY_HIGH"),
        )

    @staticmethod
    def _pct_to_level(pct: float) -> str:
        """Map a suspicion percentage to a SuspicionLevel string."""
        if pct <= 15:
            return "SAFE"
        elif pct <= 35:
            return "LOW_RISK"
        elif pct <= 55:
            return "MODERATE_RISK"
        elif pct <= 75:
            return "HIGH_RISK"
        else:
            return "VERY_HIGH"

    @staticmethod
    def _get_recommendation(level: str) -> Tuple[str, str]:
        """Return (recommendation, action_required) for a given level."""
        _RECS = {
            "SAFE": (
                "No significant scam indicators detected. Proceed with "
                "normal caution — always verify the employer independently.",
                "  ✓ Verify company registration independently\n"
                "  ✓ Do not pay any fees before joining\n"
                "  ✓ Get all terms in writing",
            ),
            "LOW_RISK": (
                "Minor concerns found. The offer may be legitimate "
                "but warrants closer examination.",
                "  ✓ Research the company online independently\n"
                "  ✓ Ask for a written contract before committing\n"
                "  ✓ Never pay any upfront fee",
            ),
            "MODERATE_RISK": (
                "CAUTION: Multiple suspicious patterns detected. "
                "We strongly advise not accepting this offer without thorough verification.",
                "  ⚠️  Do NOT pay any fee or deposit\n"
                "  ⚠️  Do NOT surrender any documents\n"
                "  ✓  Verify on emigrate.gov.in (for overseas jobs)\n"
                "  ✓  Contact Labour Helpline: 1800-425-1013",
            ),
            "HIGH_RISK": (
                "⚠️ HIGH SUSPICION: This offer contains serious red flags "
                "commonly associated with human trafficking recruitment.",
                "  🛑  Do NOT accept this job\n"
                "  🛑  Do NOT travel to the stated location\n"
                "  ✓  Report to: cybercrime.gov.in\n"
                "  ✓  Childline if minor involved: 1098",
            ),
            "VERY_HIGH": (
                "🚨 VERY HIGH SUSPICION: This offer strongly matches a "
                "human trafficking recruitment profile. DO NOT engage.",
                "  🚨  REJECT this offer immediately\n"
                "  🚨  REPORT to Police: 100\n"
                "  🚨  REPORT to Cyber Crime: 1930\n"
                "  ✓  Save all evidence (screenshots, messages)",
            ),
        }
        default = ("No assessment available.", "Contact helpline: 1098")
        return _RECS.get(level, default)


# ===========================================================================
# MODULE SELF-TEST
# ===========================================================================

if __name__ == "__main__":
    print("AegisAI Scam Detector — Self Test")
    print("=" * 60)

    detector = ScamDetector()
    print(f"Indicators loaded: {detector.get_indicator_count()}\n")

    test_cases = [
        (
            "VERY HIGH: Gulf Job Scam",
            "Females 18-25 wanted for Gulf posting. No experience required. "
            "Guaranteed ₹1.5 lakh/month. Passport will be kept for security. "
            "No phone allowed. Do not tell family. Registration fee ₹5000. "
            "Live-in required. Urgent joining needed. Cannot leave before 2 years.",
        ),
        (
            "SAFE: Legitimate Software Job",
            "Software Engineer needed. 3+ years Python experience. "
            "Office in Bengaluru. Salary 10-15 LPA. Apply with CV. "
            "Interview process: technical + HR round. Offer letter provided.",
        ),
    ]

    for label, text in test_cases:
        print(f"[{label}]")
        result  = detector.analyze(text)
        report  = detector.format_report(result)
        print(report)
