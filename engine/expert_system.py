"""
AegisAI Expert System
=====================
Rule-Based Expert System with Forward Chaining Inference Engine
Contains:
  - Working Memory (Facts)
  - Rule Base (50+ IF-THEN rules)
  - Risk Classification Logic (Low / Medium / High / Critical)
  - Inference Engine
  - Conflict Resolution Strategy
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from enum import Enum
import copy


# ===========================================================================
# ENUMERATIONS
# ===========================================================================

class RiskLevel(Enum):
    UNKNOWN  = "UNKNOWN"
    LOW      = "LOW"
    MEDIUM   = "MEDIUM"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"


class TraffickingType(Enum):
    LABOUR        = "LABOUR_TRAFFICKING"
    SEX           = "SEX_TRAFFICKING"
    DOMESTIC      = "DOMESTIC_SERVITUDE"
    CHILD         = "CHILD_TRAFFICKING"
    ORGAN         = "ORGAN_TRAFFICKING"
    ONLINE        = "ONLINE_EXPLOITATION"
    BONDED_LABOUR = "BONDED_LABOUR"
    RECRUITMENT   = "RECRUITMENT_SCAM"
    UNKNOWN       = "UNKNOWN"


class Urgency(Enum):
    ROUTINE   = 1
    ADVISORY  = 2
    ALERT     = 3
    URGENT    = 4
    EMERGENCY = 5


# ===========================================================================
# FACTS — The Working Memory
# These represent what the inference engine "knows" about the current session
# ===========================================================================

@dataclass
class Fact:
    """A single fact stored in working memory."""
    name:  str
    value: Any
    source: str = "USER_INPUT"          # USER_INPUT | INFERRED | SYSTEM
    confidence: float = 1.0             # 0.0 – 1.0
    timestamp: int = 0                  # set by WorkingMemory


@dataclass
class WorkingMemory:
    """
    The working memory holds all known facts for the current session.
    Facts are stored as {name: Fact} for fast lookup.
    """
    _facts: Dict[str, Fact] = field(default_factory=dict)
    _clock: int = 0

    # ------------------------------------------------------------------
    # Core Operations
    # ------------------------------------------------------------------

    def assert_fact(self, name: str, value: Any,
                    source: str = "USER_INPUT", confidence: float = 1.0):
        """Add or overwrite a fact in working memory."""
        self._clock += 1
        self._facts[name] = Fact(
            name=name, value=value, source=source,
            confidence=confidence, timestamp=self._clock
        )

    def retract_fact(self, name: str):
        """Remove a fact from working memory."""
        self._facts.pop(name, None)

    def get(self, name: str, default: Any = None) -> Any:
        """Retrieve a fact's value, or default if absent."""
        fact = self._facts.get(name)
        return fact.value if fact is not None else default

    def has(self, name: str) -> bool:
        """Check if a fact exists."""
        return name in self._facts

    def all_facts(self) -> Dict[str, Any]:
        """Return all facts as a simple name→value dictionary."""
        return {n: f.value for n, f in self._facts.items()}

    def snapshot(self) -> Dict[str, Fact]:
        """Return a deep copy of the current working memory."""
        return copy.deepcopy(self._facts)

    def clear(self):
        """Reset working memory."""
        self._facts.clear()
        self._clock = 0

    def __repr__(self):
        facts_str = "\n  ".join(
            f"{n}: {f.value} (src={f.source}, conf={f.confidence:.2f})"
            for n, f in sorted(self._facts.items(), key=lambda x: x[1].timestamp)
        )
        return f"WorkingMemory[\n  {facts_str}\n]"


# ===========================================================================
# INITIAL FACTS — Pre-loaded at session start
# ===========================================================================

INITIAL_FACTS = {
    # Session defaults
    "session_active":            True,
    "risk_score":                0,
    "risk_level":                RiskLevel.UNKNOWN.value,
    "trafficking_type_suspected": TraffickingType.UNKNOWN.value,
    "urgency":                   Urgency.ROUTINE.value,

    # User flags — set by questionnaire / NLP
    "user_is_minor":             False,
    "user_is_female":            None,    # None = unknown
    "user_seeking_job":          False,
    "user_received_job_offer":   False,
    "user_in_immediate_danger":  False,
    "user_has_escaped":          False,
    "user_reporting_for_other":  False,

    # Situation flags
    "documents_confiscated":     False,
    "freedom_restricted":        False,
    "wages_withheld":            False,
    "physical_abuse_present":    False,
    "threats_received":          False,
    "isolated_from_family":      False,
    "debt_bondage_present":      False,
    "online_contact_suspicious": False,
    "job_offer_suspicious":      False,
    "sexual_exploitation":       False,
    "labour_exploitation":       False,
    "child_involved":            False,
    "contact_with_authority_ok": True,
    "transportation_involved":   False,
    "cross_border_movement":     False,
    "deception_used":            False,
    "coercion_used":             False,
    "multiple_victims":          False,
    "organized_crime_suspected": False,

    # Assessment tracking
    "risk_assessment_complete":  False,
    "job_analysis_complete":     False,
    "emergency_module_shown":    False,
    "resource_module_shown":     False,
    "questions_answered":        0,
}


def initialise_working_memory() -> WorkingMemory:
    """Create a fresh working memory pre-loaded with initial facts."""
    wm = WorkingMemory()
    for name, value in INITIAL_FACTS.items():
        wm.assert_fact(name, value, source="SYSTEM")
    return wm


# ===========================================================================
# RULES — The Rule Base
# Each rule: condition function + action function + metadata
# ===========================================================================

@dataclass
class Rule:
    """
    Represents a single IF-THEN production rule.

    condition(wm) -> bool   : evaluates conditions against working memory
    action(wm)    -> None   : fires when condition is True (modifies wm)
    """
    rule_id:     str
    name:        str
    description: str
    priority:    int          # lower number = higher priority
    category:    str
    condition:   object       # Callable[[WorkingMemory], bool]
    action:      object       # Callable[[WorkingMemory], None]
    fired:       bool = False


# ---------------------------------------------------------------------------
# Helper score updater
# ---------------------------------------------------------------------------

def _add_score(wm: WorkingMemory, points: int, reason: str = ""):
    current = wm.get("risk_score", 0)
    wm.assert_fact("risk_score", current + points, source="INFERRED")
    # Log reason chain
    chain = wm.get("score_reason_chain", [])
    if reason:
        chain.append(f"+{points}: {reason}")
    wm.assert_fact("score_reason_chain", chain, source="INFERRED")


def _set_urgency(wm: WorkingMemory, urgency: Urgency):
    current = wm.get("urgency", Urgency.ROUTINE.value)
    if urgency.value > current:
        wm.assert_fact("urgency", urgency.value, source="INFERRED")


def _flag_type(wm: WorkingMemory, t: TraffickingType):
    wm.assert_fact("trafficking_type_suspected", t.value, source="INFERRED")


# ===========================================================================
# RULE DEFINITIONS — 52 IF-THEN rules
# ===========================================================================

RULE_BASE: List[Rule] = [

    # -----------------------------------------------------------------------
    # SECTION A: EMERGENCY DETECTION RULES (Priority 1-5)
    # -----------------------------------------------------------------------

    Rule(
        rule_id="R001",
        name="Immediate Physical Danger",
        description="IF user is in immediate danger THEN set CRITICAL risk and EMERGENCY urgency",
        priority=1,
        category="emergency",
        condition=lambda wm: wm.get("user_in_immediate_danger") is True,
        action=lambda wm: (
            wm.assert_fact("risk_level", RiskLevel.CRITICAL.value, source="INFERRED"),
            _set_urgency(wm, Urgency.EMERGENCY),
            _add_score(wm, 100, "User in immediate physical danger"),
            wm.assert_fact("show_emergency_contacts", True, source="INFERRED"),
            wm.assert_fact("show_escape_plan", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R002",
        name="Physical Abuse Detected",
        description="IF physical abuse is present THEN add score and alert urgency",
        priority=2,
        category="emergency",
        condition=lambda wm: wm.get("physical_abuse_present") is True,
        action=lambda wm: (
            _add_score(wm, 25, "Physical abuse present"),
            _set_urgency(wm, Urgency.ALERT),
            wm.assert_fact("recommend_medical_help", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R003",
        name="Child in Danger",
        description="IF a child is involved THEN elevate urgency to URGENT and add score",
        priority=2,
        category="emergency",
        condition=lambda wm: (
            wm.get("child_involved") is True or wm.get("user_is_minor") is True
        ),
        action=lambda wm: (
            _add_score(wm, 20, "Child involved — elevated vulnerability"),
            _set_urgency(wm, Urgency.URGENT),
            wm.assert_fact("activate_child_protection_module", True, source="INFERRED"),
            _flag_type(wm, TraffickingType.CHILD),
        ),
    ),

    Rule(
        rule_id="R004",
        name="User Has Escaped Trafficking",
        description="IF user has escaped THEN show post-escape guidance immediately",
        priority=3,
        category="emergency",
        condition=lambda wm: wm.get("user_has_escaped") is True,
        action=lambda wm: (
            wm.assert_fact("show_post_escape_guidance", True, source="INFERRED"),
            wm.assert_fact("show_medical_guidance", True, source="INFERRED"),
            wm.assert_fact("show_legal_aid_info", True, source="INFERRED"),
            _set_urgency(wm, Urgency.URGENT),
        ),
    ),

    Rule(
        rule_id="R005",
        name="Reporting for Someone Else",
        description="IF user is reporting for someone else THEN activate third-party guidance",
        priority=4,
        category="emergency",
        condition=lambda wm: wm.get("user_reporting_for_other") is True,
        action=lambda wm: (
            wm.assert_fact("show_bystander_guidance", True, source="INFERRED"),
            wm.assert_fact("show_reporting_procedures", True, source="INFERRED"),
        ),
    ),

    # -----------------------------------------------------------------------
    # SECTION B: CONTROL AND COERCION RULES (Priority 6-15)
    # -----------------------------------------------------------------------

    Rule(
        rule_id="R006",
        name="Freedom of Movement Restricted",
        description="IF freedom is restricted THEN add score 15",
        priority=6,
        category="control",
        condition=lambda wm: wm.get("freedom_restricted") is True,
        action=lambda wm: (
            _add_score(wm, 15, "Freedom of movement restricted"),
            _set_urgency(wm, Urgency.ADVISORY),
        ),
    ),

    Rule(
        rule_id="R007",
        name="Threats Received",
        description="IF threats are received THEN add score 18",
        priority=6,
        category="control",
        condition=lambda wm: wm.get("threats_received") is True,
        action=lambda wm: (
            _add_score(wm, 18, "Threats received against user or family"),
            _set_urgency(wm, Urgency.ALERT),
        ),
    ),

    Rule(
        rule_id="R008",
        name="Documents Confiscated",
        description="IF documents are confiscated THEN add score 20 — a major indicator",
        priority=6,
        category="control",
        condition=lambda wm: wm.get("documents_confiscated") is True,
        action=lambda wm: (
            _add_score(wm, 20, "Identity documents confiscated by third party"),
            wm.assert_fact("show_document_recovery_info", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R009",
        name="Isolation from Family",
        description="IF isolated from family THEN add score 12",
        priority=7,
        category="control",
        condition=lambda wm: wm.get("isolated_from_family") is True,
        action=lambda wm: _add_score(wm, 12, "Isolated from family and support network"),
    ),

    Rule(
        rule_id="R010",
        name="Debt Bondage",
        description="IF debt bondage is present THEN add score 20 and flag as bonded labour",
        priority=7,
        category="control",
        condition=lambda wm: wm.get("debt_bondage_present") is True,
        action=lambda wm: (
            _add_score(wm, 20, "Debt bondage — bonded labour indicator"),
            _flag_type(wm, TraffickingType.BONDED_LABOUR),
            wm.assert_fact("show_bonded_labour_rights", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R011",
        name="Coercion Used",
        description="IF coercion was used THEN add score 15",
        priority=7,
        category="control",
        condition=lambda wm: wm.get("coercion_used") is True,
        action=lambda wm: _add_score(wm, 15, "Coercion used to control victim"),
    ),

    Rule(
        rule_id="R012",
        name="Deception Used in Recruitment",
        description="IF deception was used THEN add score 12",
        priority=8,
        category="control",
        condition=lambda wm: wm.get("deception_used") is True,
        action=lambda wm: (
            _add_score(wm, 12, "Deception used in recruitment process"),
            wm.assert_fact("show_victim_rights", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R013",
        name="Wages Withheld",
        description="IF wages are being withheld THEN add score 15",
        priority=8,
        category="exploitation",
        condition=lambda wm: wm.get("wages_withheld") is True,
        action=lambda wm: (
            _add_score(wm, 15, "Wages withheld — labour exploitation indicator"),
            _flag_type(wm, TraffickingType.LABOUR),
        ),
    ),

    Rule(
        rule_id="R014",
        name="Sexual Exploitation Confirmed",
        description="IF sexual exploitation is occurring THEN add score 30 and classify",
        priority=5,
        category="exploitation",
        condition=lambda wm: wm.get("sexual_exploitation") is True,
        action=lambda wm: (
            _add_score(wm, 30, "Sexual exploitation confirmed"),
            _flag_type(wm, TraffickingType.SEX),
            _set_urgency(wm, Urgency.URGENT),
            wm.assert_fact("show_sexual_assault_resources", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R015",
        name="Labour Exploitation Confirmed",
        description="IF labour exploitation is occurring THEN add score 20 and classify",
        priority=8,
        category="exploitation",
        condition=lambda wm: wm.get("labour_exploitation") is True,
        action=lambda wm: (
            _add_score(wm, 20, "Labour exploitation confirmed"),
            _flag_type(wm, TraffickingType.LABOUR),
        ),
    ),

    # -----------------------------------------------------------------------
    # SECTION C: RECRUITMENT SCAM RULES (Priority 10-20)
    # -----------------------------------------------------------------------

    Rule(
        rule_id="R016",
        name="Suspicious Job Offer Received",
        description="IF user received a suspicious job offer THEN add score 10",
        priority=10,
        category="recruitment",
        condition=lambda wm: wm.get("job_offer_suspicious") is True,
        action=lambda wm: (
            _add_score(wm, 10, "Suspicious job offer received"),
            wm.assert_fact("activate_job_analyzer", True, source="INFERRED"),
            _flag_type(wm, TraffickingType.RECRUITMENT),
        ),
    ),

    Rule(
        rule_id="R017",
        name="Overseas Job With Document Surrender",
        description="IF overseas job AND documents confiscated THEN HIGH risk recruitment scam",
        priority=9,
        category="recruitment",
        condition=lambda wm: (
            wm.get("cross_border_movement") is True and
            wm.get("documents_confiscated") is True
        ),
        action=lambda wm: (
            _add_score(wm, 30, "Overseas job + document confiscation — very high trafficking risk"),
            wm.assert_fact("show_overseas_job_warning", True, source="INFERRED"),
            wm.assert_fact("show_embassy_contacts", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R018",
        name="Online Contact Suspicious",
        description="IF online contact is suspicious THEN add score 10 and flag for grooming check",
        priority=10,
        category="recruitment",
        condition=lambda wm: wm.get("online_contact_suspicious") is True,
        action=lambda wm: (
            _add_score(wm, 10, "Suspicious online contact — possible grooming"),
            wm.assert_fact("show_online_safety_tips", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R019",
        name="Transportation Involved with Deception",
        description="IF transported AND deception was used THEN add score 15",
        priority=9,
        category="recruitment",
        condition=lambda wm: (
            wm.get("transportation_involved") is True and
            wm.get("deception_used") is True
        ),
        action=lambda wm: _add_score(
            wm, 15, "Transportation used with deception — trafficking pattern"
        ),
    ),

    Rule(
        rule_id="R020",
        name="Multiple Victims Situation",
        description="IF multiple victims are involved THEN add score 10 and flag organized crime",
        priority=9,
        category="exploitation",
        condition=lambda wm: wm.get("multiple_victims") is True,
        action=lambda wm: (
            _add_score(wm, 10, "Multiple victims present"),
            wm.assert_fact("organized_crime_suspected", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R021",
        name="Organized Crime Suspected",
        description="IF organized crime suspected THEN add score 15 and alert authorities module",
        priority=8,
        category="exploitation",
        condition=lambda wm: wm.get("organized_crime_suspected") is True,
        action=lambda wm: (
            _add_score(wm, 15, "Organized crime network suspected"),
            wm.assert_fact("show_ahtu_contacts", True, source="INFERRED"),
        ),
    ),

    # -----------------------------------------------------------------------
    # SECTION D: RISK CLASSIFICATION RULES (Priority 20-30)
    # Applied AFTER scoring is complete
    # -----------------------------------------------------------------------

    Rule(
        rule_id="R022",
        name="Classify as LOW Risk",
        description="IF score 0–20 THEN risk level = LOW",
        priority=20,
        category="classification",
        condition=lambda wm: (
            wm.get("risk_assessment_complete") is True and
            0 <= wm.get("risk_score", 0) <= 20
        ),
        action=lambda wm: (
            wm.assert_fact("risk_level", RiskLevel.LOW.value, source="INFERRED"),
            wm.assert_fact("show_educational_resources", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R023",
        name="Classify as MEDIUM Risk",
        description="IF score 21–50 THEN risk level = MEDIUM",
        priority=20,
        category="classification",
        condition=lambda wm: (
            wm.get("risk_assessment_complete") is True and
            21 <= wm.get("risk_score", 0) <= 50
        ),
        action=lambda wm: (
            wm.assert_fact("risk_level", RiskLevel.MEDIUM.value, source="INFERRED"),
            wm.assert_fact("show_caution_advice", True, source="INFERRED"),
            wm.assert_fact("show_helplines", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R024",
        name="Classify as HIGH Risk",
        description="IF score 51–99 THEN risk level = HIGH",
        priority=20,
        category="classification",
        condition=lambda wm: (
            wm.get("risk_assessment_complete") is True and
            51 <= wm.get("risk_score", 0) <= 99
        ),
        action=lambda wm: (
            wm.assert_fact("risk_level", RiskLevel.HIGH.value, source="INFERRED"),
            wm.assert_fact("show_emergency_guidance", True, source="INFERRED"),
            wm.assert_fact("show_helplines", True, source="INFERRED"),
            _set_urgency(wm, Urgency.URGENT),
        ),
    ),

    Rule(
        rule_id="R025",
        name="Classify as CRITICAL Risk",
        description="IF score >= 100 THEN risk level = CRITICAL",
        priority=20,
        category="classification",
        condition=lambda wm: (
            wm.get("risk_assessment_complete") is True and
            wm.get("risk_score", 0) >= 100
        ),
        action=lambda wm: (
            wm.assert_fact("risk_level", RiskLevel.CRITICAL.value, source="INFERRED"),
            wm.assert_fact("show_emergency_guidance", True, source="INFERRED"),
            wm.assert_fact("show_emergency_contacts", True, source="INFERRED"),
            wm.assert_fact("show_escape_plan", True, source="INFERRED"),
            _set_urgency(wm, Urgency.EMERGENCY),
        ),
    ),

    # -----------------------------------------------------------------------
    # SECTION E: LOW RISK RULES (Advisory)
    # -----------------------------------------------------------------------

    Rule(
        rule_id="R026",
        name="LOW: Seeking Employment",
        description="IF user is seeking a job THEN provide job safety awareness",
        priority=25,
        category="low_risk",
        condition=lambda wm: (
            wm.get("user_seeking_job") is True and
            wm.get("risk_level") == RiskLevel.LOW.value
        ),
        action=lambda wm: (
            wm.assert_fact("show_job_safety_tips", True, source="INFERRED"),
            wm.assert_fact("recommend_job_analyzer", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R027",
        name="LOW: Online Safety Education",
        description="IF online contact is suspicious AND risk is LOW THEN show online safety",
        priority=25,
        category="low_risk",
        condition=lambda wm: (
            wm.get("online_contact_suspicious") is True and
            wm.get("risk_level") == RiskLevel.LOW.value
        ),
        action=lambda wm: wm.assert_fact("show_online_safety_education", True, source="INFERRED"),
    ),

    Rule(
        rule_id="R028",
        name="LOW: Minor User — Extra Education",
        description="IF user is a minor AND risk is low THEN provide age-appropriate education",
        priority=25,
        category="low_risk",
        condition=lambda wm: (
            wm.get("user_is_minor") is True and
            wm.get("risk_level") == RiskLevel.LOW.value
        ),
        action=lambda wm: (
            wm.assert_fact("show_child_safety_education", True, source="INFERRED"),
            wm.assert_fact("recommend_trusted_adult_conversation", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R029",
        name="LOW: Student Awareness Path",
        description="IF user is student AND risk is low THEN show awareness module",
        priority=26,
        category="low_risk",
        condition=lambda wm: (
            wm.get("user_is_student") is True and
            wm.get("risk_level") == RiskLevel.LOW.value
        ),
        action=lambda wm: wm.assert_fact("show_student_awareness_module", True, source="INFERRED"),
    ),

    Rule(
        rule_id="R030",
        name="LOW: NGO Worker Information",
        description="IF user is NGO worker AND risk is low THEN show resource directory",
        priority=26,
        category="low_risk",
        condition=lambda wm: (
            wm.get("user_is_ngo_worker") is True and
            wm.get("risk_level") == RiskLevel.LOW.value
        ),
        action=lambda wm: (
            wm.assert_fact("show_ngo_resource_directory", True, source="INFERRED"),
            wm.assert_fact("show_reporting_procedures", True, source="INFERRED"),
        ),
    ),

    # -----------------------------------------------------------------------
    # SECTION F: MEDIUM RISK RULES (Caution + Advisory)
    # -----------------------------------------------------------------------

    Rule(
        rule_id="R031",
        name="MEDIUM: Show Helplines",
        description="IF risk is MEDIUM THEN always show helplines",
        priority=22,
        category="medium_risk",
        condition=lambda wm: wm.get("risk_level") == RiskLevel.MEDIUM.value,
        action=lambda wm: (
            wm.assert_fact("show_helplines", True, source="INFERRED"),
            wm.assert_fact("show_warning_signs_education", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R032",
        name="MEDIUM: Suspicious Job — Detailed Analysis",
        description="IF risk is MEDIUM AND job offer suspicious THEN force job analysis",
        priority=22,
        category="medium_risk",
        condition=lambda wm: (
            wm.get("risk_level") == RiskLevel.MEDIUM.value and
            wm.get("job_offer_suspicious") is True
        ),
        action=lambda wm: (
            wm.assert_fact("force_job_analysis", True, source="INFERRED"),
            wm.assert_fact("show_job_red_flag_list", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R033",
        name="MEDIUM: Deception Without Freedom Restriction",
        description="IF deception BUT no restriction THEN caution — watch situation",
        priority=23,
        category="medium_risk",
        condition=lambda wm: (
            wm.get("deception_used") is True and
            wm.get("freedom_restricted") is False and
            wm.get("risk_level") == RiskLevel.MEDIUM.value
        ),
        action=lambda wm: (
            wm.assert_fact("show_deception_warning", True, source="INFERRED"),
            wm.assert_fact("recommend_safety_plan", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R034",
        name="MEDIUM: Online Grooming Suspicion",
        description="IF suspicious online contact AND deception AND risk is MEDIUM",
        priority=22,
        category="medium_risk",
        condition=lambda wm: (
            wm.get("online_contact_suspicious") is True and
            wm.get("deception_used") is True and
            wm.get("risk_level") == RiskLevel.MEDIUM.value
        ),
        action=lambda wm: (
            wm.assert_fact("show_grooming_warning", True, source="INFERRED"),
            wm.assert_fact("show_block_report_guide", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R035",
        name="MEDIUM: Isolated With Financial Dependency",
        description="IF isolated AND wages withheld AND risk is MEDIUM",
        priority=22,
        category="medium_risk",
        condition=lambda wm: (
            wm.get("isolated_from_family") is True and
            wm.get("wages_withheld") is True and
            wm.get("risk_level") == RiskLevel.MEDIUM.value
        ),
        action=lambda wm: (
            _add_score(wm, 10, "Isolation + wage withholding — escalating risk"),
            wm.assert_fact("show_labour_rights", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R036",
        name="MEDIUM: Migrant Worker Vulnerability",
        description="IF user is migrant AND freedom restricted AND risk is MEDIUM",
        priority=23,
        category="medium_risk",
        condition=lambda wm: (
            wm.get("user_is_migrant") is True and
            wm.get("freedom_restricted") is True and
            wm.get("risk_level") == RiskLevel.MEDIUM.value
        ),
        action=lambda wm: (
            wm.assert_fact("show_migrant_worker_rights", True, source="INFERRED"),
            wm.assert_fact("show_embassy_contacts", True, source="INFERRED"),
        ),
    ),

    # -----------------------------------------------------------------------
    # SECTION G: HIGH RISK RULES (Urgent Response)
    # -----------------------------------------------------------------------

    Rule(
        rule_id="R037",
        name="HIGH: Show Emergency Contacts and Guidance",
        description="IF risk is HIGH THEN always show emergency contacts",
        priority=18,
        category="high_risk",
        condition=lambda wm: wm.get("risk_level") == RiskLevel.HIGH.value,
        action=lambda wm: (
            wm.assert_fact("show_emergency_contacts", True, source="INFERRED"),
            wm.assert_fact("show_emergency_guidance", True, source="INFERRED"),
            wm.assert_fact("show_legal_aid_info", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R038",
        name="HIGH: Documents Taken + Freedom Restricted",
        description="IF docs confiscated AND freedom restricted AND risk HIGH",
        priority=17,
        category="high_risk",
        condition=lambda wm: (
            wm.get("documents_confiscated") is True and
            wm.get("freedom_restricted") is True and
            wm.get("risk_level") == RiskLevel.HIGH.value
        ),
        action=lambda wm: (
            _add_score(wm, 20, "Docs confiscated + freedom restricted = classic trafficking"),
            wm.assert_fact("show_document_recovery_info", True, source="INFERRED"),
            wm.assert_fact("show_escape_plan", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R039",
        name="HIGH: Debt Bondage with Threats",
        description="IF debt bondage AND threats AND risk HIGH",
        priority=17,
        category="high_risk",
        condition=lambda wm: (
            wm.get("debt_bondage_present") is True and
            wm.get("threats_received") is True and
            wm.get("risk_level") == RiskLevel.HIGH.value
        ),
        action=lambda wm: (
            _add_score(wm, 15, "Debt bondage + threats — bonded labour trafficking"),
            wm.assert_fact("show_bonded_labour_rights", True, source="INFERRED"),
            wm.assert_fact("show_nhrc_contact", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R040",
        name="HIGH: Female Minor — Maximum Protection",
        description="IF female AND minor AND risk HIGH",
        priority=16,
        category="high_risk",
        condition=lambda wm: (
            wm.get("user_is_female") is True and
            wm.get("user_is_minor") is True and
            wm.get("risk_level") == RiskLevel.HIGH.value
        ),
        action=lambda wm: (
            _add_score(wm, 10, "Female minor — maximum vulnerability"),
            wm.assert_fact("show_childline_priority", True, source="INFERRED"),
            wm.assert_fact("show_pocso_protection", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R041",
        name="HIGH: Cross-Border Movement + Exploitation",
        description="IF cross border + exploitation AND risk HIGH",
        priority=17,
        category="high_risk",
        condition=lambda wm: (
            wm.get("cross_border_movement") is True and
            (wm.get("sexual_exploitation") is True or
             wm.get("labour_exploitation") is True) and
            wm.get("risk_level") == RiskLevel.HIGH.value
        ),
        action=lambda wm: (
            _add_score(wm, 15, "Cross-border movement with exploitation = international trafficking"),
            wm.assert_fact("show_international_support", True, source="INFERRED"),
            wm.assert_fact("show_embassy_contacts", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R042",
        name="HIGH: Recommend Safety Plan",
        description="IF risk is HIGH AND no immediate danger THEN recommend safety plan",
        priority=18,
        category="high_risk",
        condition=lambda wm: (
            wm.get("risk_level") == RiskLevel.HIGH.value and
            wm.get("user_in_immediate_danger") is False
        ),
        action=lambda wm: wm.assert_fact("recommend_safety_plan", True, source="INFERRED"),
    ),

    # -----------------------------------------------------------------------
    # SECTION H: CRITICAL RISK RULES (Emergency Response Only)
    # -----------------------------------------------------------------------

    Rule(
        rule_id="R043",
        name="CRITICAL: Immediate Danger + Child",
        description="IF critical + child + immediate danger THEN activate full child protection",
        priority=1,
        category="critical_risk",
        condition=lambda wm: (
            wm.get("risk_level") == RiskLevel.CRITICAL.value and
            (wm.get("child_involved") is True or wm.get("user_is_minor") is True) and
            wm.get("user_in_immediate_danger") is True
        ),
        action=lambda wm: (
            wm.assert_fact("show_childline_priority", True, source="INFERRED"),
            wm.assert_fact("show_escape_plan", True, source="INFERRED"),
            wm.assert_fact("activate_full_emergency_mode", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R044",
        name="CRITICAL: Sexual + Physical Abuse",
        description="IF critical + sexual AND physical abuse THEN medical + emergency",
        priority=2,
        category="critical_risk",
        condition=lambda wm: (
            wm.get("risk_level") == RiskLevel.CRITICAL.value and
            wm.get("sexual_exploitation") is True and
            wm.get("physical_abuse_present") is True
        ),
        action=lambda wm: (
            wm.assert_fact("show_medical_emergency_info", True, source="INFERRED"),
            wm.assert_fact("show_sexual_assault_resources", True, source="INFERRED"),
            wm.assert_fact("show_witness_protection_info", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R045",
        name="CRITICAL: No Ability to Contact Authorities",
        description="IF critical + cannot contact authority THEN show silent help methods",
        priority=2,
        category="critical_risk",
        condition=lambda wm: (
            wm.get("risk_level") == RiskLevel.CRITICAL.value and
            wm.get("contact_with_authority_ok") is False
        ),
        action=lambda wm: (
            wm.assert_fact("show_silent_help_signals", True, source="INFERRED"),
            wm.assert_fact("show_coded_escape_methods", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R046",
        name="CRITICAL: Organized Crime — Full Alert",
        description="IF critical + organized crime THEN alert AHTU and show full emergency",
        priority=3,
        category="critical_risk",
        condition=lambda wm: (
            wm.get("risk_level") == RiskLevel.CRITICAL.value and
            wm.get("organized_crime_suspected") is True
        ),
        action=lambda wm: (
            wm.assert_fact("show_ahtu_contacts", True, source="INFERRED"),
            wm.assert_fact("show_witness_protection_info", True, source="INFERRED"),
            wm.assert_fact("show_nhrc_contact", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R047",
        name="CRITICAL: International Trafficking",
        description="IF critical + cross border + organized crime",
        priority=3,
        category="critical_risk",
        condition=lambda wm: (
            wm.get("risk_level") == RiskLevel.CRITICAL.value and
            wm.get("cross_border_movement") is True and
            wm.get("organized_crime_suspected") is True
        ),
        action=lambda wm: (
            wm.assert_fact("show_embassy_contacts", True, source="INFERRED"),
            wm.assert_fact("show_international_support", True, source="INFERRED"),
            wm.assert_fact("show_mea_helpline", True, source="INFERRED"),
        ),
    ),

    # -----------------------------------------------------------------------
    # SECTION I: RESOURCE RECOMMENDATION RULES (Priority 30-40)
    # -----------------------------------------------------------------------

    Rule(
        rule_id="R048",
        name="Show Compensation Information",
        description="IF user has escaped AND risk is HIGH or CRITICAL THEN show compensation",
        priority=30,
        category="resources",
        condition=lambda wm: (
            wm.get("user_has_escaped") is True and
            wm.get("risk_level") in [RiskLevel.HIGH.value, RiskLevel.CRITICAL.value]
        ),
        action=lambda wm: (
            wm.assert_fact("show_compensation_rights", True, source="INFERRED"),
            wm.assert_fact("show_nalsa_info", True, source="INFERRED"),
        ),
    ),

    Rule(
        rule_id="R049",
        name="Show Rehabilitation Information",
        description="IF user has escaped THEN show rehabilitation programs",
        priority=30,
        category="resources",
        condition=lambda wm: wm.get("user_has_escaped") is True,
        action=lambda wm: wm.assert_fact("show_rehabilitation_programs", True, source="INFERRED"),
    ),

    Rule(
        rule_id="R050",
        name="Show Trauma Support",
        description="IF sexual exploitation OR physical abuse THEN show trauma support",
        priority=30,
        category="resources",
        condition=lambda wm: (
            wm.get("sexual_exploitation") is True or
            wm.get("physical_abuse_present") is True
        ),
        action=lambda wm: wm.assert_fact("show_trauma_support", True, source="INFERRED"),
    ),

    Rule(
        rule_id="R051",
        name="Show Reporting Procedures",
        description="IF user is reporting for other OR risk is MEDIUM+ THEN show reporting info",
        priority=30,
        category="resources",
        condition=lambda wm: (
            wm.get("user_reporting_for_other") is True or
            wm.get("risk_score", 0) > 20
        ),
        action=lambda wm: wm.assert_fact("show_reporting_procedures", True, source="INFERRED"),
    ),

    Rule(
        rule_id="R052",
        name="Show Legal Aid Information",
        description="IF risk is HIGH or CRITICAL THEN always show legal aid info",
        priority=29,
        category="resources",
        condition=lambda wm: wm.get("risk_level") in [
            RiskLevel.HIGH.value, RiskLevel.CRITICAL.value
        ],
        action=lambda wm: (
            wm.assert_fact("show_legal_aid_info", True, source="INFERRED"),
            wm.assert_fact("show_victim_rights", True, source="INFERRED"),
        ),
    ),
]

# Sort rule base by priority (ascending = higher priority first)
RULE_BASE.sort(key=lambda r: r.priority)


# ===========================================================================
# INFERENCE ENGINE — Forward Chaining
# ===========================================================================

class InferenceEngine:
    """
    Forward-Chaining Inference Engine.

    Algorithm:
      1. Start with facts in Working Memory
      2. Evaluate all rules whose conditions are True
      3. Add newly inferred facts to Working Memory
      4. Repeat until no new rules fire (fixed point)
      5. Return enriched Working Memory with all conclusions

    Conflict Resolution: Priority-based (lowest priority number fires first)
    """

    def __init__(self, rule_base: List[Rule]):
        self.rule_base = sorted(rule_base, key=lambda r: r.priority)
        self.inference_log: List[str] = []

    def run(self, wm: WorkingMemory, max_cycles: int = 20) -> WorkingMemory:
        """
        Execute forward chaining inference until fixpoint or max_cycles.

        Returns the enriched WorkingMemory.
        """
        self.inference_log = []

        for cycle in range(max_cycles):
            fired_any = False

            for rule in self.rule_base:
                if rule.fired:
                    continue  # Each rule fires at most once per session

                try:
                    condition_met = rule.condition(wm)
                except Exception as e:
                    self.inference_log.append(
                        f"[CYCLE {cycle+1}] ERROR evaluating {rule.rule_id}: {e}"
                    )
                    continue

                if condition_met:
                    # Record pre-fire snapshot to detect changes
                    pre_snap = wm.snapshot()

                    try:
                        rule.action(wm)
                        rule.fired = True
                        fired_any = True
                        self.inference_log.append(
                            f"[CYCLE {cycle+1}] FIRED: {rule.rule_id} — {rule.name}"
                        )
                    except Exception as e:
                        self.inference_log.append(
                            f"[CYCLE {cycle+1}] ACTION ERROR in {rule.rule_id}: {e}"
                        )

            if not fired_any:
                self.inference_log.append(
                    f"[CYCLE {cycle+1}] FIXPOINT reached — no new rules fired."
                )
                break

        return wm

    def reset_fired_flags(self):
        """Reset all rules so they can fire again (for new sessions)."""
        for rule in self.rule_base:
            rule.fired = False

    def get_log(self) -> List[str]:
        return self.inference_log

    def get_fired_rules(self) -> List[str]:
        return [r.rule_id for r in self.rule_base if r.fired]


# ===========================================================================
# RISK CLASSIFICATION LOGIC
# ===========================================================================

class RiskClassifier:
    """
    Maps a risk score to a risk level with full explanation.
    Used as post-processing step after inference engine run.
    """

    THRESHOLDS = {
        RiskLevel.CRITICAL: 100,
        RiskLevel.HIGH:      51,
        RiskLevel.MEDIUM:    21,
        RiskLevel.LOW:        0,
    }

    RESPONSES = {
        RiskLevel.LOW: {
            "label":   "🟢 LOW RISK",
            "colour":  "green",
            "summary": (
                "Based on your responses, you appear to be in a safe situation.\n"
                "However, it is always good to stay informed about the warning signs\n"
                "of human trafficking. Explore the educational resources below."
            ),
            "actions": [
                "Browse our educational resources",
                "Learn about warning signs",
                "Take the job offer safety check",
            ],
            "helplines": ["Childline: 1098", "Police: 100"],
        },
        RiskLevel.MEDIUM: {
            "label":   "🟡 MEDIUM RISK",
            "colour":  "yellow",
            "summary": (
                "Some warning signs are present in your situation.\n"
                "We recommend you take precautionary steps and reach out\n"
                "to a trusted adult or one of the helplines below."
            ),
            "actions": [
                "Review warning signs relevant to your situation",
                "Contact a trusted adult or NGO",
                "Consider calling a helpline for confidential advice",
                "Read about your legal rights",
            ],
            "helplines": [
                "Childline: 1098 (24/7, Free)",
                "Police: 100",
                "Women's Helpline: 1091",
            ],
        },
        RiskLevel.HIGH: {
            "label":   "🔴 HIGH RISK",
            "colour":  "red",
            "summary": (
                "⚠️  WARNING: Significant risk indicators have been detected.\n"
                "You may be in or approaching a dangerous situation.\n"
                "Please reach out to authorities or a support organization immediately."
            ),
            "actions": [
                "Contact police (100) or Childline (1098) NOW",
                "Reach out to a trusted adult",
                "Read the emergency guidance",
                "Consider a safe exit plan",
                "Request free legal aid from DLSA",
            ],
            "helplines": [
                "🆘 Police: 100",
                "🆘 Childline: 1098",
                "🆘 Women's Helpline: 1091",
                "🆘 NHRC: 14433",
            ],
        },
        RiskLevel.CRITICAL: {
            "label":   "🚨 CRITICAL RISK",
            "colour":  "red_bold",
            "summary": (
                "🚨 CRITICAL: You are in a VERY DANGEROUS SITUATION.\n"
                "Please seek help IMMEDIATELY.\n"
                "Call 100 (Police) or 1098 (Childline) right now.\n"
                "If you cannot call, use the Silent Help Signal or approach\n"
                "any person in a public space."
            ),
            "actions": [
                "Call Police: 100 IMMEDIATELY",
                "Call Childline: 1098 IMMEDIATELY",
                "Use Silent Help Signal if you cannot speak",
                "Go to the nearest public space",
                "Get to safety before anything else",
            ],
            "helplines": [
                "🆘 EMERGENCY Police: 100",
                "🆘 EMERGENCY Childline: 1098",
                "🆘 EMERGENCY National: 112",
                "🆘 Women's Helpline: 1091",
                "🆘 Ambulance: 108",
            ],
        },
    }

    @classmethod
    def classify(cls, score: int) -> RiskLevel:
        if score >= cls.THRESHOLDS[RiskLevel.CRITICAL]:
            return RiskLevel.CRITICAL
        elif score >= cls.THRESHOLDS[RiskLevel.HIGH]:
            return RiskLevel.HIGH
        elif score >= cls.THRESHOLDS[RiskLevel.MEDIUM]:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

    @classmethod
    def get_response(cls, score: int) -> dict:
        level = cls.classify(score)
        response = dict(cls.RESPONSES[level])
        response["score"] = score
        response["level"] = level.value
        response["level_enum"] = level
        return response

    @classmethod
    def explain_score(cls, wm: WorkingMemory) -> str:
        """Return a human-readable breakdown of how the score was reached."""
        chain = wm.get("score_reason_chain", [])
        score = wm.get("risk_score", 0)
        level = cls.classify(score)

        lines = [
            "RISK ASSESSMENT BREAKDOWN",
            "=" * 40,
        ]
        for item in chain:
            lines.append(f"  {item}")
        lines.append("-" * 40)
        lines.append(f"  TOTAL SCORE : {score}")
        lines.append(f"  RISK LEVEL  : {level.value}")
        return "\n".join(lines)


# ===========================================================================
# RISK QUESTION BANK — for the guided questionnaire
# ===========================================================================

RISK_QUESTIONS = [
    {
        "qid":       "RQ01",
        "domain":    "control_coercion",
        "question":  "Is someone controlling where you go or who you can speak to?",
        "yes_fact":  "freedom_restricted",
        "yes_value": True,
        "yes_score": 15,
        "follow_up": "RQ01a",
    },
    {
        "qid":       "RQ01a",
        "domain":    "control_coercion",
        "question":  "Does that person use threats or physical force to control you?",
        "yes_fact":  "threats_received",
        "yes_value": True,
        "yes_score": 18,
        "follow_up": None,
        "parent":    "RQ01",
    },
    {
        "qid":       "RQ02",
        "domain":    "deception",
        "question":  "Were you given false promises about a job, relationship, or opportunity that turned out to be untrue?",
        "yes_fact":  "deception_used",
        "yes_value": True,
        "yes_score": 12,
        "follow_up": "RQ02a",
    },
    {
        "qid":       "RQ02a",
        "domain":    "deception",
        "question":  "Are your actual situation and working conditions very different from what was promised?",
        "yes_fact":  "coercion_used",
        "yes_value": True,
        "yes_score": 13,
        "follow_up": None,
        "parent":    "RQ02",
    },
    {
        "qid":       "RQ03",
        "domain":    "documents",
        "question":  "Has someone taken away your ID, passport, or Aadhaar and is holding it?",
        "yes_fact":  "documents_confiscated",
        "yes_value": True,
        "yes_score": 20,
        "follow_up": None,
    },
    {
        "qid":       "RQ04",
        "domain":    "labour",
        "question":  "Are you working without being paid, or are your wages being taken by someone else?",
        "yes_fact":  "wages_withheld",
        "yes_value": True,
        "yes_score": 15,
        "follow_up": "RQ04a",
    },
    {
        "qid":       "RQ04a",
        "domain":    "labour",
        "question":  "Do you owe a 'debt' to your employer or recruiter that seems impossible to repay?",
        "yes_fact":  "debt_bondage_present",
        "yes_value": True,
        "yes_score": 20,
        "follow_up": None,
        "parent":    "RQ04",
    },
    {
        "qid":       "RQ05",
        "domain":    "physical_safety",
        "question":  "Have you been physically hurt or threatened with violence?",
        "yes_fact":  "physical_abuse_present",
        "yes_value": True,
        "yes_score": 25,
        "follow_up": None,
    },
    {
        "qid":       "RQ06",
        "domain":    "isolation",
        "question":  "Are you prevented from contacting your family or friends?",
        "yes_fact":  "isolated_from_family",
        "yes_value": True,
        "yes_score": 12,
        "follow_up": None,
    },
    {
        "qid":       "RQ07",
        "domain":    "sexual_exploitation",
        "question":  "Are you being forced to do anything of a sexual nature against your will?",
        "yes_fact":  "sexual_exploitation",
        "yes_value": True,
        "yes_score": 30,
        "follow_up": None,
    },
    {
        "qid":       "RQ08",
        "domain":    "immediate_safety",
        "question":  "Are you in immediate danger right now?",
        "yes_fact":  "user_in_immediate_danger",
        "yes_value": True,
        "yes_score": 50,
        "follow_up": None,
    },
    {
        "qid":       "RQ09",
        "domain":    "transport",
        "question":  "Were you transported to your current location by someone else without full understanding of where you were going?",
        "yes_fact":  "transportation_involved",
        "yes_value": True,
        "yes_score": 10,
        "follow_up": "RQ09a",
    },
    {
        "qid":       "RQ09a",
        "domain":    "transport",
        "question":  "Did this involve crossing a state or international border?",
        "yes_fact":  "cross_border_movement",
        "yes_value": True,
        "yes_score": 10,
        "follow_up": None,
        "parent":    "RQ09",
    },
    {
        "qid":       "RQ10",
        "domain":    "online",
        "question":  "Did you meet someone online who made you a job or opportunity offer that led to your current situation?",
        "yes_fact":  "online_contact_suspicious",
        "yes_value": True,
        "yes_score": 10,
        "follow_up": None,
    },
    {
        "qid":       "RQ11",
        "domain":    "children",
        "question":  "Are there children in the same situation as you?",
        "yes_fact":  "child_involved",
        "yes_value": True,
        "yes_score": 20,
        "follow_up": None,
    },
]


# ===========================================================================
# EXPERT SYSTEM SESSION — Orchestrates WM + Inference Engine + Classifier
# ===========================================================================

class ExpertSystemSession:
    """
    Top-level orchestrator for a single user session.

    Usage:
        session = ExpertSystemSession()
        session.assert_user_fact("user_in_immediate_danger", True)
        session.run_inference()
        result = session.get_result()
    """

    def __init__(self):
        self.wm = initialise_working_memory()
        self.engine = InferenceEngine(RULE_BASE)
        self.classifier = RiskClassifier()
        self._completed = False

    def assert_user_fact(self, name: str, value: Any, confidence: float = 1.0):
        """Assert a fact about the user directly."""
        self.wm.assert_fact(name, value, source="USER_INPUT", confidence=confidence)

    def process_risk_answer(self, question: dict, answer: bool):
        """
        Process a single risk questionnaire answer.
        Sets the relevant fact and adds score to working memory.
        """
        if answer:
            self.wm.assert_fact(
                question["yes_fact"], question["yes_value"], source="USER_INPUT"
            )
            _add_score(self.wm, question["yes_score"], question["question"])

    def complete_assessment(self):
        """Mark the risk assessment as complete and trigger classification."""
        self.wm.assert_fact("risk_assessment_complete", True, source="SYSTEM")

    def run_inference(self):
        """Run the forward-chaining inference engine on the current facts."""
        self.engine.reset_fired_flags()
        self.wm = self.engine.run(self.wm)

        # Ensure risk level is set based on score (in case R022-R025 haven't fired)
        score = self.wm.get("risk_score", 0)
        level = self.classifier.classify(score)
        if self.wm.get("risk_level") == RiskLevel.UNKNOWN.value:
            self.wm.assert_fact("risk_level", level.value, source="INFERRED")

        self._completed = True

    def get_result(self) -> dict:
        """Return the full result of the inference run."""
        score = self.wm.get("risk_score", 0)
        response = self.classifier.get_response(score)
        response["score_breakdown"] = self.classifier.explain_score(self.wm)
        response["fired_rules"] = self.engine.get_fired_rules()
        response["inference_log"] = self.engine.get_log()
        response["all_facts"] = self.wm.all_facts()
        response["show_flags"] = {
            k: v for k, v in self.wm.all_facts().items()
            if k.startswith("show_") and v is True
        }
        return response

    def get_urgency_level(self) -> Urgency:
        return Urgency(self.wm.get("urgency", Urgency.ROUTINE.value))

    def is_emergency(self) -> bool:
        return self.get_urgency_level() in [Urgency.URGENT, Urgency.EMERGENCY]


# ===========================================================================
# DEMO / TEST
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  AegisAI Expert System — Demonstration")
    print("=" * 60)

    # --- Test 1: Critical Risk Scenario ---
    print("\n[SCENARIO 1] Critical Risk — User in immediate danger")
    session = ExpertSystemSession()
    session.assert_user_fact("user_in_immediate_danger", True)
    session.assert_user_fact("documents_confiscated", True)
    session.assert_user_fact("freedom_restricted", True)
    session.assert_user_fact("sexual_exploitation", True)
    session.assert_user_fact("physical_abuse_present", True)
    session.complete_assessment()
    session.run_inference()
    result = session.get_result()
    print(result["score_breakdown"])
    print(f"Risk Level  : {result['level']}")
    print(f"Urgency     : {session.get_urgency_level().name}")
    print(f"Rules Fired : {result['fired_rules']}")
    print(f"Show Flags  : {list(result['show_flags'].keys())}")

    print("\n" + "-" * 60)

    # --- Test 2: Medium Risk Scenario ---
    print("\n[SCENARIO 2] Medium Risk — Suspicious job offer, online contact")
    session2 = ExpertSystemSession()
    session2.assert_user_fact("job_offer_suspicious", True)
    session2.assert_user_fact("online_contact_suspicious", True)
    session2.assert_user_fact("deception_used", True)
    session2.complete_assessment()
    session2.run_inference()
    result2 = session2.get_result()
    print(result2["score_breakdown"])
    print(f"Risk Level  : {result2['level']}")

    print("\n" + "-" * 60)

    # --- Test 3: Low Risk Scenario ---
    print("\n[SCENARIO 3] Low Risk — Student seeking awareness")
    session3 = ExpertSystemSession()
    session3.assert_user_fact("user_is_student", True)
    session3.assert_user_fact("user_seeking_job", True)
    session3.complete_assessment()
    session3.run_inference()
    result3 = session3.get_result()
    print(result3["score_breakdown"])
    print(f"Risk Level  : {result3['level']}")

    print("\n" + "=" * 60)
    print(f"  Total Rules in Rule Base: {len(RULE_BASE)}")
    print(f"  Total Risk Questions    : {len(RISK_QUESTIONS)}")
    print("=" * 60)
