"""
AegisAI — Scam Service
========================
Provides job-offer scam detection using the AegisAI indicator engine.
Logs all submitted checks and analysis results to SQLite database.
"""
from __future__ import annotations

import logging
import sys
import os
from typing import List

from models.scam import DetectionResult, SuspicionLevel
from services.database_service import DatabaseService
from services.session_service import SessionService

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

log = logging.getLogger(__name__)

# Level thresholds (must match scam_analyzer calibration)
_THRESHOLDS = [
    (76.0, SuspicionLevel.VERY_HIGH),
    (56.0, SuspicionLevel.HIGH_RISK),
    (36.0, SuspicionLevel.MODERATE),
    (16.0, SuspicionLevel.LOW_RISK),
    (0.0,  SuspicionLevel.SAFE),
]


class ScamService:
    """
    Coordinates job-offer scam detection and logs results to SQLite database.
    """

    def __init__(self) -> None:
        self._db = DatabaseService()
        self._session = SessionService.instance()
        try:
            from scam_detector import ScamDetector as _SD
            self._detector = _SD()
            log.info("ScamService ready.")
        except Exception as exc:
            log.error("ScamService init failed: %s", exc)
            self._detector = None

    def analyze(self, text: str) -> DetectionResult:
        """Analyse a job offer text, return a typed DetectionResult, and log it to SQLite."""
        if not self._detector:
            return self._empty_result()

        try:
            raw = self._detector.analyze(text)
            pct   = float(getattr(raw, "suspicion_pct", 0.0))
            score = int(getattr(raw, "raw_score", 0))
            flags: List[str] = list(getattr(raw, "top_flags", []))
            raw_level = getattr(raw, "level", "SAFE")
            rec   = getattr(raw, "recommendation", "")

            level = SuspicionLevel.from_string(raw_level)
            if level == SuspicionLevel.SAFE and pct > 0:
                # Re-derive level from pct in case raw level string differs
                for threshold, lvl in _THRESHOLDS:
                    if pct >= threshold:
                        level = lvl
                        break

            report = self._format_report_text(level, pct, score, flags, rec)

            # Category scores (optional)
            cat_scores = {}
            if hasattr(raw, "category_scores"):
                cat_scores = dict(raw.category_scores)

            result = DetectionResult(
                level           = level,
                suspicion_pct   = pct,
                raw_score       = score,
                top_flags       = flags[:10],
                category_scores = cat_scores,
                recommendation  = rec or level.advice,
                detailed_report = report,
            )

            # Log this scam check in the database
            self._db.save_scam_log(
                self._session.session_id,
                text,
                pct,
                level.name,
                flags[:10]
            )

            return result

        except Exception as exc:
            log.error("Scam analysis error: %s", exc)
            return self._empty_result()

    def get_scam_history(self) -> List[dict]:
        """Load past scam scan records from the database."""
        return self._db.get_scam_logs(self._session.session_id)

    # ------------------------------------------------------------------

    @staticmethod
    def _format_report_text(level: SuspicionLevel, pct: float,
                            score: int, flags: List[str], rec: str) -> str:
        lines = [
            f"{'='*50}",
            f"  SCAM ANALYSIS REPORT",
            f"{'='*50}",
            f"  Risk Level   :  {level.icon}  {level.label}",
            f"  Suspicion    :  {pct:.1f}%",
            f"  Raw Score    :  {score}",
            f"{'─'*50}",
        ]
        if flags:
            lines.append("  Red Flags Detected:")
            for flag in flags[:10]:
                lines.append(f"    ⚠  {flag}")
        else:
            lines.append("  No significant red flags detected.")
        lines += [
            f"{'─'*50}",
            f"  Recommendation:",
            f"    {rec or level.advice}",
            f"{'='*50}",
        ]
        return "\n".join(lines)

    @staticmethod
    def _empty_result() -> DetectionResult:
        return DetectionResult(
            level           = SuspicionLevel.SAFE,
            suspicion_pct   = 0.0,
            raw_score       = 0,
            top_flags       = [],
            recommendation  = "Analyzer unavailable. Use caution.",
        )
