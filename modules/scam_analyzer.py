"""
AegisAI — Recruitment Scam Analyzer
=====================================
NLP-based job offer analyzer for detecting human trafficking recruitment scams.

Contains:
  - 100+ Scam Indicators (grouped into 12 categories)
  - Weighted Risk Scoring Formula
  - NLP Preprocessing Pipeline
  - Detection Logic with Confidence Levels
  - Example Test Cases
"""

import re
import string
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


# ===========================================================================
# ENUMERATIONS
# ===========================================================================

class SuspicionLevel(Enum):
    SAFE          = "SAFE"
    LOW_RISK      = "LOW_RISK"
    MODERATE_RISK = "MODERATE_RISK"
    HIGH_RISK     = "HIGH_RISK"
    VERY_HIGH     = "VERY_HIGH"


# ===========================================================================
# SCAM INDICATOR DEFINITIONS — 100+ indicators across 12 categories
# ===========================================================================

@dataclass
class Indicator:
    """A single scam indicator entry."""
    indicator_id:  str
    category:      str
    keyword:       str                  # phrase or keyword to match
    is_regex:      bool                 # True if keyword is a regex pattern
    weight:        int                  # severity score contribution
    description:   str                  # explanation of why this is a red flag
    example:       str = ""             # example phrase that triggers this


# ---------------------------------------------------------------------------
# Category 1: VAGUE JOB DESCRIPTIONS (weight 2-3)
# ---------------------------------------------------------------------------
CAT_VAGUE = [
    Indicator("I001", "vague_description", "flexible work", False, 2,
              "Real jobs specify schedules; 'flexible' often hides unpaid or unregulated work.",
              "'Flexible work available, no fixed hours required'"),
    Indicator("I002", "vague_description", "no experience required", False, 3,
              "High-paying jobs never require zero experience — a deception tactic.",
              "'High pay, no experience needed, anyone can apply'"),
    Indicator("I003", "vague_description", "easy money", False, 4,
              "Promises of easy money are classic trafficking lures.",
              "'Easy money from home — no hard work needed'"),
    Indicator("I004", "vague_description", "quick cash", False, 4,
              "Traffickers attract desperate victims with urgent cash promises.",
              "'Quick cash, get paid same day'"),
    Indicator("I005", "vague_description", "miscellaneous work", False, 2,
              "Vague role descriptions hide the true nature of exploitative work.",
              "'Miscellaneous duties, more info on joining'"),
    Indicator("I006", "vague_description", "entertainment industry", False, 3,
              "'Entertainment' is a common cover for sexual exploitation.",
              "'Work in the entertainment industry, good pay, females preferred'"),
    Indicator("I007", "vague_description", "service industry", False, 2,
              "Ambiguous 'service' roles mask domestic servitude.",
              "'Service industry job, must be willing to travel'"),
    Indicator("I008", "vague_description", "personal assistant", False, 2,
              "Personal assistant roles can mask domestic servitude or sexual exploitation.",
              "'Personal assistant to wealthy client, live-in required'"),
    Indicator("I009", "vague_description", "hospitality job", False, 2,
              "Hospitality is commonly used for trafficking in luxury sectors.",
              "'Female hospitality staff wanted, international placement'"),
    Indicator("I010", "vague_description", "helper", False, 2,
              "Ambiguous 'helper' role hides exploitative domestic work.",
              "'Urgently required: female helper, age 18-25'"),
]

# ---------------------------------------------------------------------------
# Category 2: UNREALISTIC COMPENSATION (weight 4-6)
# ---------------------------------------------------------------------------
CAT_COMPENSATION = [
    Indicator("I011", "unrealistic_compensation",
              r"earn.{0,30}(lakh|lakhs|1,00,000|100000).{0,20}(per|a|every).{0,10}(month|week)",
              True, 6,
              "Monthly earnings in lakhs for unskilled work is implausible — classic bait.",
              "'Earn 2 lakhs per month working from home'"),
    Indicator("I012", "unrealistic_compensation", "guaranteed salary", False, 4,
              "Legitimate jobs don't guarantee salary before knowing your performance.",
              "'Guaranteed salary of ₹80,000/month from day one'"),
    Indicator("I013", "unrealistic_compensation", "unlimited earning", False, 5,
              "Promises of unlimited income with no ceiling are deceptive lures.",
              "'Unlimited earning potential, no cap on income'"),
    Indicator("I014", "unrealistic_compensation", "double your income", False, 4,
              "Income-doubling promises exploit financial desperation.",
              "'Double your current income in 3 months'"),
    Indicator("I015", "unrealistic_compensation", "best salary in industry", False, 3,
              "Superlative salary claims without evidence are red flags.",
              "'Best salary in the industry, cash payment daily'"),
    Indicator("I016", "unrealistic_compensation", "cash daily", False, 4,
              "Daily cash payments avoid paper trails — used in illegal operations.",
              "'Get paid in cash daily, no deductions'"),
    Indicator("I017", "unrealistic_compensation", "high commission", False, 3,
              "Extremely high commission structures often indicate illegal MLM or trafficking.",
              "'High commission of 80% on every sale'"),
    Indicator("I018", "unrealistic_compensation", r"\d{5,}.{0,10}per day", True, 5,
              "Absurdly high daily pay for unspecified work.",
              "'₹5000 per day for simple online task'"),
    Indicator("I019", "unrealistic_compensation", "paid weekly in cash", False, 3,
              "Cash payments bypass banking and worker protections.",
              "'Paid weekly in cash, no questions asked'"),
    Indicator("I020", "unrealistic_compensation", "no deductions", False, 3,
              "Real employers deduct PF, tax etc. — no deductions hides illegal employment.",
              "'Full salary, no deductions, take home everything'"),
]

# ---------------------------------------------------------------------------
# Category 3: GEOGRAPHIC ISOLATION / TRAVEL REQUIREMENTS (weight 3-5)
# ---------------------------------------------------------------------------
CAT_GEOGRAPHY = [
    Indicator("I021", "geographic_isolation", "live-in required", False, 5,
              "Mandatory live-in arrangements facilitate total control over victim.",
              "'This is a live-in position, accommodation provided by employer'"),
    Indicator("I022", "geographic_isolation", "remote location", False, 4,
              "Remote locations isolate victims from help.",
              "'Position based at a remote resort, transportation provided'"),
    Indicator("I023", "geographic_isolation", "travel required", False, 3,
              "Unexplained travel requirements often mean transportation for trafficking.",
              "'Must be willing to travel at short notice'"),
    Indicator("I024", "geographic_isolation", "relocate immediately", False, 4,
              "Urgency to relocate prevents victims from making informed decisions.",
              "'Must be willing to relocate immediately, everything arranged'"),
    Indicator("I025", "geographic_isolation", "overseas posting", False, 4,
              "Overseas jobs with no verifiable employer are classic trafficking vectors.",
              "'Overseas posting in Dubai, all expenses paid'"),
    Indicator("I026", "geographic_isolation", "gulf job", False, 3,
              "Gulf country jobs are frequently used in trafficking operations from India.",
              "'Gulf job available for female candidates immediately'"),
    Indicator("I027", "geographic_isolation", "abroad opportunity", False, 3,
              "Unverified 'abroad' opportunities frequently lead to trafficking.",
              "'Exciting abroad opportunity for young women, apply today'"),
    Indicator("I028", "geographic_isolation", "accommodation provided", False, 2,
              "Employer-controlled accommodation enables isolation and control.",
              "'Accommodation and meals fully provided by employer'"),
    Indicator("I029", "geographic_isolation", "all expenses paid", False, 3,
              "When employer pays everything, victim becomes financially dependent.",
              "'All expenses paid — visa, flight, food, accommodation'"),
    Indicator("I030", "geographic_isolation", "myanmar", False, 8,
              "Myanmar is a known destination for tech scam centre trafficking.",
              "'Online data entry job in Myanmar, excellent package'"),
    Indicator("I031", "geographic_isolation", "cambodia", False, 8,
              "Cambodia is a known tech scam centre trafficking destination.",
              "'Customer service job in Cambodia, high pay, immediate joining'"),
    Indicator("I032", "geographic_isolation", "laos", False, 7,
              "Laos is a known tech scam centre trafficking destination.",
              "'Job in Laos for IT graduates, all visa arranged'"),
    Indicator("I033", "geographic_isolation", "thailand border", False, 6,
              "Thailand border areas host known scam centres.",
              "'Position on Thai-Myanmar border, special incentives'"),
]

# ---------------------------------------------------------------------------
# Category 4: DOCUMENT CONFISCATION (weight 7-10)
# ---------------------------------------------------------------------------
CAT_DOCUMENTS = [
    Indicator("I034", "document_confiscation", "passport will be kept", False, 10,
              "Passport confiscation is the clearest indicator of trafficking.",
              "'Company will keep your passport for security'"),
    Indicator("I035", "document_confiscation", "id will be held", False, 10,
              "ID holding is illegal and enables control over victim.",
              "'Your ID will be held by the manager during employment'"),
    Indicator("I036", "document_confiscation", "submit original documents", False, 8,
              "No legitimate employer requires original document surrender.",
              "'Submit original Aadhaar and passport at time of joining'"),
    Indicator("I037", "document_confiscation", "documents surrendered", False, 9,
              "Document surrender enables trafficker control.",
              "'All documents surrendered to employer for the duration of contract'"),
    Indicator("I038", "document_confiscation", "visa held by company", False, 9,
              "Visa confiscation is common in overseas trafficking.",
              "'Your work visa will be held by the company representative'"),
    Indicator("I039", "document_confiscation", "aadhaar required upfront", False, 7,
              "Aadhaar collection before employment is a trafficking method.",
              "'Send your Aadhaar and photo for immediate verification'"),
    Indicator("I040", "document_confiscation", "proof of identity to be deposited", False, 8,
              "Depositing identity proof with employer is a control mechanism.",
              "'Deposit your identity proof with HR on day one'"),
]

# ---------------------------------------------------------------------------
# Category 5: COERCIVE CONTROL LANGUAGE (weight 8-10)
# ---------------------------------------------------------------------------
CAT_COERCION = [
    Indicator("I041", "coercive_control", "cannot leave before contract ends", False, 10,
              "Contracts preventing resignation are bonded labour — illegal in India.",
              "'No resignation allowed before 2-year contract is complete'"),
    Indicator("I042", "coercive_control", "work off debt", False, 10,
              "Debt bondage is the classic forced labour mechanism.",
              "'You will work off the advance we give you before receiving salary'"),
    Indicator("I043", "coercive_control", "penalty for leaving", False, 8,
              "Financial penalties for leaving are coercive control tools.",
              "'A penalty of ₹50,000 will be charged if you leave before 1 year'"),
    Indicator("I044", "coercive_control", "must repay advance", False, 9,
              "Advances with repayment conditions create debt bondage.",
              "'You must repay the joining advance before leaving'"),
    Indicator("I045", "coercive_control", "no resignation allowed", False, 9,
              "Preventing resignation is a violation of labour rights.",
              "'No resignation will be accepted during the contract period'"),
    Indicator("I046", "coercive_control", "sign agreement before joining", False, 5,
              "Pressuring to sign agreements before employment start is coercive.",
              "'Must sign the bond agreement before your start date'"),
    Indicator("I047", "coercive_control", "forfeit salary if leave", False, 9,
              "Salary forfeiture for leaving is financial coercion.",
              "'You will forfeit all salary if you leave without notice'"),
    Indicator("I048", "coercive_control", "bond of", False, 6,
              "Employment bonds are frequently used in exploitative contracts.",
              "'3-year bond of ₹1,00,000 required on joining'"),
    Indicator("I049", "coercive_control", "cannot quit", False, 9,
              "Explicit prohibition on quitting is coercion.",
              "'This is a mandatory contract — you cannot quit mid-term'"),
    Indicator("I050", "coercive_control", "strict discipline", False, 4,
              "Vague 'strict discipline' clauses enable abuse.",
              "'Strict discipline policy enforced — any breach means deduction'"),
]

# ---------------------------------------------------------------------------
# Category 6: COMMUNICATION RESTRICTIONS (weight 5-8)
# ---------------------------------------------------------------------------
CAT_COMMUNICATION = [
    Indicator("I051", "communication_restriction", "no phone allowed", False, 8,
              "Phone bans isolate victims from getting help.",
              "'Personal phones are not allowed during working hours'"),
    Indicator("I052", "communication_restriction", "no personal calls", False, 7,
              "Banning personal calls prevents victims from reaching support.",
              "'No personal calls permitted inside the facility'"),
    Indicator("I053", "communication_restriction", "limited contact with family", False, 8,
              "Family contact restrictions enable isolation — trafficking indicator.",
              "'Limited contact with outside family for security reasons'"),
    Indicator("I054", "communication_restriction", "mobile surrender on joining", False, 9,
              "Phone surrender is a known trafficking control mechanism.",
              "'You will surrender your mobile phone upon arrival at the facility'"),
    Indicator("I055", "communication_restriction", "no internet access", False, 6,
              "Internet restriction prevents victims from seeking help online.",
              "'No personal internet access allowed at the facility'"),
    Indicator("I056", "communication_restriction", "social media restricted", False, 5,
              "Social media bans prevent victims from raising alarm.",
              "'Social media use is strictly prohibited during employment period'"),
    Indicator("I057", "communication_restriction", "all communications monitored", False, 6,
              "Surveillance of communications is a control mechanism.",
              "'All your communications may be monitored by management'"),
]

# ---------------------------------------------------------------------------
# Category 7: UNUSUAL RECRUITMENT PROCESS (weight 3-6)
# ---------------------------------------------------------------------------
CAT_RECRUITMENT = [
    Indicator("I058", "unusual_recruitment", "no interview required", False, 5,
              "Legitimate employers conduct interviews to assess candidates.",
              "'No interview required — selected on application, join immediately'"),
    Indicator("I059", "unusual_recruitment", "hired on the spot", False, 5,
              "Instant hiring without vetting is a trafficking recruitment method.",
              "'Hired on the spot — no documents needed to start'"),
    Indicator("I060", "unusual_recruitment", "recruited via whatsapp", False, 4,
              "WhatsApp-only recruitment bypasses formal verification.",
              "'Send your photo on WhatsApp to apply — interview via WhatsApp'"),
    Indicator("I061", "unusual_recruitment", "dm to apply", False, 4,
              "DM-based applications are used by fake recruiters.",
              "'DM to apply, no CV required, urgent requirement'"),
    Indicator("I062", "unusual_recruitment", "no cv required", False, 4,
              "Requiring no CV prevents proper screening — a red flag.",
              "'No CV or experience required — just send your photo'"),
    Indicator("I063", "unusual_recruitment", "send your photo to apply", False, 5,
              "Requesting photo upfront (not normal) suggests exploitation.",
              "'Send your full-length photo to apply for this position'"),
    Indicator("I064", "unusual_recruitment", "urgent joining", False, 4,
              "Urgency prevents victims from doing due diligence.",
              "'Urgent: 5 positions, must join within 48 hours'"),
    Indicator("I065", "unusual_recruitment", "no registration number", False, 3,
              "Lack of company registration details hides illegitimate operations.",
              "'Apply now — no company details shared until interview'"),
    Indicator("I066", "unusual_recruitment", "talent scout", False, 4,
              "'Talent scouts' are commonly used in modeling/entertainment scams.",
              "'Our talent scout noticed you on Instagram — you have a great look'"),
    Indicator("I067", "unusual_recruitment", "approached on street", False, 5,
              "Street recruitment is a classic trafficking tactic.",
              "'One of our scouts approached you — we liked your personality'"),
    Indicator("I068", "unusual_recruitment", "casting agent", False, 4,
              "Fake casting agents are used to recruit trafficking victims.",
              "'Our casting agent will arrange your audition and expenses'"),
]

# ---------------------------------------------------------------------------
# Category 8: FINANCIAL EXPLOITATION (weight 5-8)
# ---------------------------------------------------------------------------
CAT_FINANCIAL = [
    Indicator("I069", "financial_exploitation", "registration fee required", False, 8,
              "Legitimate jobs never require registration fees from applicants.",
              "'Pay ₹2,000 registration fee to secure your position'"),
    Indicator("I070", "financial_exploitation", "pay upfront", False, 8,
              "Requiring upfront payment is a scam indicator.",
              "'Pay ₹5,000 upfront for your uniform and training kit'"),
    Indicator("I071", "financial_exploitation", "security deposit", False, 6,
              "Employee security deposits are used to trap victims financially.",
              "'A refundable security deposit of ₹10,000 is required'"),
    Indicator("I072", "financial_exploitation", "training fee", False, 7,
              "Training fees extracted from employees are financial exploitation.",
              "'Training fee of ₹3,000 will be deducted from first salary'"),
    Indicator("I073", "financial_exploitation", "processing fee", False, 7,
              "Processing fees for jobs are always scams.",
              "'A processing fee of ₹1,500 is required to complete your application'"),
    Indicator("I074", "financial_exploitation", "visa fee", False, 6,
              "Demanding visa fees from job seekers is a scam.",
              "'Visa processing fee of ₹15,000 — refundable after 6 months'"),
    Indicator("I075", "financial_exploitation", "pay to get job", False, 9,
              "Paying to get a job is always a scam.",
              "'Confirm your slot by paying ₹500 — first come, first served'"),
    Indicator("I076", "financial_exploitation", "advance taken from salary", False, 6,
              "Salary advance deductions create debt traps.",
              "'An advance of ₹20,000 will be given and recovered over 6 months'"),
    Indicator("I077", "financial_exploitation", "refundable after", False, 5,
              "False refund promises keep victims paying.",
              "'Deposit is fully refundable after 1 year of service'"),
    Indicator("I078", "financial_exploitation", "loan for joining", False, 8,
              "Encouraging loans to join is a debt bondage setup.",
              "'We can arrange a loan for your joining fee — repay from salary'"),
]

# ---------------------------------------------------------------------------
# Category 9: GENDER/AGE TARGETING (weight 3-5)
# ---------------------------------------------------------------------------
CAT_TARGETING = [
    Indicator("I079", "targeting_vulnerable", "females only", False, 5,
              "Female-only posts without justification are red flags.",
              "'Only female candidates between 18-25 years, fair complexion'"),
    Indicator("I080", "targeting_vulnerable", "age 18 to 25", False, 3,
              "Strict age-targeting of young adults is a vulnerability exploitation tactic.",
              "'Only candidates aged 18-25 will be considered'"),
    Indicator("I081", "targeting_vulnerable", "good looking", False, 5,
              "Appearance requirements for non-appearance-based jobs indicate exploitation.",
              "'Must be good looking and presentable, photos required'"),
    Indicator("I082", "targeting_vulnerable", "fair complexion", False, 5,
              "Skin tone requirements have no job relevance and target for exploitation.",
              "'Fair complexion preferred, full-length photo mandatory'"),
    Indicator("I083", "targeting_vulnerable", "single women", False, 5,
              "Targeting single women indicates vulnerability exploitation.",
              "'Single women preferred for this residential position'"),
    Indicator("I084", "targeting_vulnerable", "freshers welcome", False, 2,
              "Targeting fresh graduates with no work knowledge indicates exploitation.",
              "'Freshers welcome, high salary from day 1, no experience needed'"),
    Indicator("I085", "targeting_vulnerable", "poor background", False, 6,
              "Explicitly targeting poor applicants exploits financial vulnerability.",
              "'Opportunity for candidates from poor or rural backgrounds'"),
    Indicator("I086", "targeting_vulnerable", "from village", False, 4,
              "Rural targeting exploits lack of urban awareness.",
              "'Preference for candidates from rural or small-town backgrounds'"),
    Indicator("I087", "targeting_vulnerable", "willing to do anything", False, 7,
              "Vague 'willing to do anything' clause enables exploitation.",
              "'Must be flexible and willing to do anything asked'"),
    Indicator("I088", "targeting_vulnerable", "desperate for work", False, 6,
              "Targeting financially desperate individuals is exploitation.",
              "'For those who are desperate for work and need immediate income'"),
]

# ---------------------------------------------------------------------------
# Category 10: PRIVACY/SECRECY DEMANDS (weight 5-7)
# ---------------------------------------------------------------------------
CAT_SECRECY = [
    Indicator("I089", "secrecy_demand", "do not tell family", False, 9,
              "Demands for secrecy from family are a grooming and control tactic.",
              "'Keep this opportunity confidential — do not tell family yet'"),
    Indicator("I090", "secrecy_demand", "keep confidential", False, 6,
              "Confidentiality demands prevent victims from getting advice.",
              "'This is a confidential opportunity — do not post publicly'"),
    Indicator("I091", "secrecy_demand", "do not share details", False, 5,
              "Suppressing information sharing is a control tactic.",
              "'Do not share these details with anyone until you join'"),
    Indicator("I092", "secrecy_demand", "secret job", False, 7,
              "Secret job offers are always suspicious.",
              "'This is a discreet opportunity — total confidentiality required'"),
    Indicator("I093", "secrecy_demand", "for your eyes only", False, 6,
              "Exclusive secrecy demands isolate victim from support.",
              "'This message is for your eyes only — apply directly'"),
    Indicator("I094", "secrecy_demand", "do not discuss with anyone", False, 8,
              "Isolating victims from others' opinions is grooming behavior.",
              "'Do not discuss this opportunity with your friends or relatives'"),
]

# ---------------------------------------------------------------------------
# Category 11: ONLINE EXPLOITATION PATTERNS (weight 5-9)
# ---------------------------------------------------------------------------
CAT_ONLINE = [
    Indicator("I095", "online_exploitation", "send intimate photos", False, 10,
              "Requesting intimate photos is sexual exploitation.",
              "'For modeling, send intimate photos to this number'"),
    Indicator("I096", "online_exploitation", "adult entertainment", False, 9,
              "Adult entertainment jobs often mask sex trafficking.",
              "'Work in adult entertainment — high pay, immediate joining'"),
    Indicator("I097", "online_exploitation", "online friendship job", False, 7,
              "Paid 'friendship' or 'companionship' jobs are exploitation fronts.",
              "'Earn by making online friends — companionship services'"),
    Indicator("I098", "online_exploitation", "webcam job", False, 9,
              "Webcam jobs are frequently sex trafficking fronts.",
              "'Webcam job from home — ₹50,000/month, flexible hours'"),
    Indicator("I099", "online_exploitation", "chat with foreigners", False, 6,
              "Paid chatting with foreigners is often exploitation.",
              "'Earn ₹1,000/hour just chatting with foreign clients'"),
    Indicator("I100", "online_exploitation", "crypto job online", False, 7,
              "Crypto/online jobs from Myanmar/Cambodia are tech scam trafficking.",
              "'Online crypto trading job, work from home, high pay, apply now'"),
    Indicator("I101", "online_exploitation", "dating app job", False, 8,
              "Dating app recruitment is a common grooming-to-trafficking path.",
              "'Earn by creating profiles on dating apps — easy income'"),
    Indicator("I102", "online_exploitation", "social media influencer job", False, 4,
              "Fake influencer jobs can lead to exploitation.",
              "'Become a social media influencer — we manage your profile'"),
]

# ---------------------------------------------------------------------------
# Category 12: LEGAL/CONTRACT RED FLAGS (weight 5-8)
# ---------------------------------------------------------------------------
CAT_LEGAL = [
    Indicator("I103", "legal_red_flags", "no written contract", False, 7,
              "Verbal-only arrangements prevent victims from asserting rights.",
              "'Everything is verbal — no written contract required'"),
    Indicator("I104", "legal_red_flags", "sign now decide later", False, 7,
              "Pressuring signatures before reading is coercive.",
              "'Sign the contract first, we'll explain terms when you arrive'"),
    Indicator("I105", "legal_red_flags", "contract in foreign language", False, 6,
              "Foreign-language contracts that victims can't read enable deception.",
              "'Contract is in English/Arabic — sign here, we'll translate later'"),
    Indicator("I106", "legal_red_flags", "unregistered company", False, 5,
              "Unregistered companies have no legal accountability.",
              "'We are a startup — not yet officially registered'"),
    Indicator("I107", "legal_red_flags", "no gst number", False, 4,
              "Legitimate businesses operating at scale have GST registration.",
              "'We do not have a GST number yet — we are new'"),
    Indicator("I108", "legal_red_flags", "no company address", False, 6,
              "Companies with no verifiable address are illegitimate.",
              "'Company address will be shared after you confirm'"),
    Indicator("I109", "legal_red_flags", "terms will be shared later", False, 7,
              "Withholding terms prevents informed consent.",
              "'Full terms will be shared once you arrive at the location'"),
    Indicator("I110", "legal_red_flags", "not responsible for", False, 5,
              "Pre-emptive disclaimers of responsibility signal intent to exploit.",
              "'Company is not responsible for any personal situation after joining'"),
]

# Compile master list
ALL_INDICATORS: List[Indicator] = (
    CAT_VAGUE + CAT_COMPENSATION + CAT_GEOGRAPHY + CAT_DOCUMENTS +
    CAT_COERCION + CAT_COMMUNICATION + CAT_RECRUITMENT + CAT_FINANCIAL +
    CAT_TARGETING + CAT_SECRECY + CAT_ONLINE + CAT_LEGAL
)

# Maximum possible score (for percentage calculation)
MAX_POSSIBLE_SCORE = sum(ind.weight for ind in ALL_INDICATORS)


# ===========================================================================
# NLP PREPROCESSOR — Lightweight, NLTK-optional
# ===========================================================================

# Common English stopwords (lightweight, no NLTK needed)
_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "was", "are", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "this", "that",
    "these", "those", "it", "its", "i", "you", "he", "she", "we", "they",
    "their", "our", "your", "his", "her", "not", "no", "so", "as", "if",
    "then", "than", "there", "where", "who", "which", "what", "when",
    "how", "all", "any", "both", "each", "few", "more", "most", "other",
    "into", "through", "during", "before", "after", "above", "below",
    "up", "down", "out", "off", "over", "under", "again", "further",
}

def preprocess_text(raw_text: str) -> Tuple[str, List[str]]:
    """
    Preprocess raw job description text.

    Returns:
        (processed_string, list_of_tokens)
    """
    # Lowercase
    text = raw_text.lower()

    # Remove special characters except spaces and basic punctuation
    text = re.sub(r"[^\w\s₹\-\/]", " ", text)

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenize
    tokens = text.split()

    # Remove stopwords (keep for keyword matching but remove from token list)
    content_tokens = [t for t in tokens if t not in _STOPWORDS and len(t) > 2]

    return text, content_tokens


# ===========================================================================
# DETECTION RESULT
# ===========================================================================

@dataclass
class MatchResult:
    """A single matched indicator result."""
    indicator:    Indicator
    matched_text: str
    position:     int              # character position in input


@dataclass
class AnalysisResult:
    """Full result of scanning a job description."""
    raw_text:          str
    processed_text:    str
    total_score:       int
    max_score:         int
    suspicion_pct:     float
    suspicion_level:   SuspicionLevel
    matches:           List[MatchResult]
    category_scores:   Dict[str, int]
    category_counts:   Dict[str, int]
    recommendation:    str
    action_required:   str
    top_flags:         List[str]


# ===========================================================================
# SCORING FORMULA
# ===========================================================================

# Realistic reference cap: a job description matching ~8 moderate indicators
# (avg weight 7) hits ~56 points — we scale against 60 so results are meaningful.
_SCORE_REFERENCE_CAP = 60

def compute_suspicion_score(total_raw_score: int,
                             max_possible:   int,
                             match_count:    int) -> Tuple[float, SuspicionLevel]:
    """
    Risk Scoring Formula:

    Suspicion % = min((raw_score / REFERENCE_CAP) * 100, 100)

    REFERENCE_CAP = 60  (equivalent to ~8 moderate-weight red flags)

    Thresholds:
      0–15%  → SAFE
      16–35% → LOW_RISK
      36–55% → MODERATE_RISK
      56–75% → HIGH_RISK
      76%+   → VERY_HIGH

    This uses a realistic cap rather than the theoretical maximum of all
    indicators so that real-world suspicious texts produce meaningful scores.
    """
    if total_raw_score == 0:
        return 0.0, SuspicionLevel.SAFE

    pct = min(100.0, (total_raw_score / _SCORE_REFERENCE_CAP) * 100)

    if pct <= 15:
        level = SuspicionLevel.SAFE
    elif pct <= 35:
        level = SuspicionLevel.LOW_RISK
    elif pct <= 55:
        level = SuspicionLevel.MODERATE_RISK
    elif pct <= 75:
        level = SuspicionLevel.HIGH_RISK
    else:
        level = SuspicionLevel.VERY_HIGH

    return round(pct, 2), level


# ===========================================================================
# RECOMMENDATION ENGINE
# ===========================================================================

_RECOMMENDATIONS = {
    SuspicionLevel.SAFE: {
        "recommendation": (
            "No significant trafficking or scam indicators detected in this job offer. "
            "It appears relatively safe based on the text provided. "
            "However, always verify the employer independently before accepting."
        ),
        "action_required": (
            "Proceed with normal caution:\n"
            "  ✓ Verify the company's registration and address\n"
            "  ✓ Do not pay any fees before joining\n"
            "  ✓ Get all terms in writing\n"
            "  ✓ Share details with a trusted family member"
        ),
    },
    SuspicionLevel.LOW_RISK: {
        "recommendation": (
            "A few minor concerns were found in this job offer. "
            "The offer may be legitimate but warrants closer examination. "
            "Do not proceed without verifying these specific concerns."
        ),
        "action_required": (
            "Caution — verify before proceeding:\n"
            "  ✓ Research the company online independently\n"
            "  ✓ Ask for a written contract before committing\n"
            "  ✓ Visit the company office in person\n"
            "  ✓ Never pay any upfront fee\n"
            "  ✓ Discuss with a trusted adult first"
        ),
    },
    SuspicionLevel.MODERATE_RISK: {
        "recommendation": (
            "CAUTION: Multiple suspicious patterns detected in this job offer. "
            "These are known tactics used in trafficking and labor exploitation scams. "
            "We strongly recommend you do NOT accept or travel for this offer without thorough verification."
        ),
        "action_required": (
            "Action required — do not proceed without verification:\n"
            "  ⚠️  Do NOT pay any fee or deposit\n"
            "  ⚠️  Do NOT surrender any documents\n"
            "  ⚠️  Do NOT travel to an unknown location alone\n"
            "  ✓  Verify company on: emigrate.gov.in (for overseas jobs)\n"
            "  ✓  Consult a trusted adult or NGO before any decision\n"
            "  ✓  Contact Labour Helpline: 1800-425-1013 if unsure"
        ),
    },
    SuspicionLevel.HIGH_RISK: {
        "recommendation": (
            "⚠️  HIGH SUSPICION: This job offer contains multiple serious red flags "
            "commonly associated with human trafficking recruitment. "
            "This offer is likely FRAUDULENT and potentially dangerous."
        ),
        "action_required": (
            "STOP — Do not proceed with this offer:\n"
            "  🛑  Do NOT accept this job\n"
            "  🛑  Do NOT travel to the stated location\n"
            "  🛑  Do NOT pay any amount\n"
            "  🛑  Do NOT share your documents\n"
            "  ✓  Report this offer to: cybercrime.gov.in\n"
            "  ✓  Report to Labour Department: 1800-425-1013\n"
            "  ✓  Contact Childline if a minor is involved: 1098\n"
            "  ✓  Share this offer with police if you were approached in person"
        ),
    },
    SuspicionLevel.VERY_HIGH: {
        "recommendation": (
            "🚨 VERY HIGH SUSPICION: This job offer matches the profile of HUMAN TRAFFICKING "
            "recruitment. The combination of indicators found in this text strongly suggests "
            "this is a trafficking recruitment operation. DO NOT engage with this offer."
        ),
        "action_required": (
            "DANGER — Treat this as a trafficking attempt:\n"
            "  🚨  REJECT this offer immediately\n"
            "  🚨  Do NOT contact the recruiter again\n"
            "  🚨  REPORT to Police: 100\n"
            "  🚨  REPORT to Cyber Crime: 1930 / cybercrime.gov.in\n"
            "  🚨  REPORT to Childline: 1098 (if any minor was targeted)\n"
            "  🚨  REPORT to NHRC: 14433\n"
            "  ✓  Save all evidence (screenshots, messages, numbers)\n"
            "  ✓  Warn others who may have seen this offer"
        ),
    },
}


# ===========================================================================
# SCAM ANALYZER — Main Class
# ===========================================================================

class ScamAnalyzer:
    """
    Main class for analyzing job descriptions for trafficking scam indicators.
    """

    def __init__(self, indicators: Optional[List[Indicator]] = None):
        self.indicators = indicators or ALL_INDICATORS

    def analyze(self, raw_job_text: str) -> AnalysisResult:
        """
        Analyze a job description text for scam and trafficking indicators.

        Args:
            raw_job_text: The full text of the job description

        Returns:
            AnalysisResult with complete analysis
        """
        processed_text, tokens = preprocess_text(raw_job_text)

        matches: List[MatchResult] = []
        matched_ids: set = set()   # prevent double-counting same indicator

        for indicator in self.indicators:
            if indicator.indicator_id in matched_ids:
                continue

            # Build search text: both processed and original lower for pattern matching
            search_text = processed_text

            if indicator.is_regex:
                pattern = indicator.keyword
                found = re.search(pattern, search_text, re.IGNORECASE)
                if found:
                    matches.append(MatchResult(
                        indicator=indicator,
                        matched_text=found.group(0),
                        position=found.start(),
                    ))
                    matched_ids.add(indicator.indicator_id)
            else:
                keyword = indicator.keyword.lower()
                pos = search_text.find(keyword)
                if pos != -1:
                    matches.append(MatchResult(
                        indicator=indicator,
                        matched_text=keyword,
                        position=pos,
                    ))
                    matched_ids.add(indicator.indicator_id)

        # Aggregate scores
        total_score = sum(m.indicator.weight for m in matches)
        category_scores: Dict[str, int] = {}
        category_counts: Dict[str, int] = {}

        for m in matches:
            cat = m.indicator.category
            category_scores[cat] = category_scores.get(cat, 0) + m.indicator.weight
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # Compute suspicion level
        suspicion_pct, suspicion_level = compute_suspicion_score(
            total_score, MAX_POSSIBLE_SCORE, len(matches)
        )

        # Build top flags (top 5 by weight)
        top_matches = sorted(matches, key=lambda x: x.indicator.weight, reverse=True)[:5]
        top_flags = [
            f"[{m.indicator.indicator_id}] {m.indicator.description}"
            for m in top_matches
        ]

        # Get recommendation
        rec = _RECOMMENDATIONS[suspicion_level]

        return AnalysisResult(
            raw_text=raw_job_text,
            processed_text=processed_text,
            total_score=total_score,
            max_score=MAX_POSSIBLE_SCORE,
            suspicion_pct=suspicion_pct,
            suspicion_level=suspicion_level,
            matches=matches,
            category_scores=category_scores,
            category_counts=category_counts,
            recommendation=rec["recommendation"],
            action_required=rec["action_required"],
            top_flags=top_flags,
        )

    def format_report(self, result: AnalysisResult) -> str:
        """Format a human-readable analysis report."""
        lines = [
            "=" * 65,
            "  AegisAI JOB OFFER SCAM ANALYSIS REPORT",
            "=" * 65,
            f"  Suspicion Score  : {result.total_score} / {result.max_score}",
            f"  Suspicion %      : {result.suspicion_pct:.1f}%",
            f"  Risk Level       : {result.suspicion_level.value}",
            f"  Indicators Found : {len(result.matches)}",
            "",
            "CATEGORY BREAKDOWN:",
            "-" * 65,
        ]

        for cat, score in sorted(
            result.category_scores.items(), key=lambda x: x[1], reverse=True
        ):
            count = result.category_counts.get(cat, 0)
            bar = "█" * min(score, 30)
            lines.append(f"  {cat:<30} | {bar:<30} ({count} flags, score={score})")

        lines += [
            "",
            "TOP RED FLAGS DETECTED:",
            "-" * 65,
        ]
        for flag in result.top_flags:
            lines.append(f"  ⚠️  {flag}")

        lines += [
            "",
            "ASSESSMENT:",
            "-" * 65,
            f"  {result.recommendation}",
            "",
            "WHAT TO DO:",
            "-" * 65,
            f"{result.action_required}",
            "",
            "=" * 65,
        ]

        return "\n".join(lines)


# ===========================================================================
# EXAMPLE TEST CASES
# ===========================================================================

EXAMPLE_CASES = [

    {
        "label": "EXAMPLE 1 — Classic Gulf Job Trafficking Scam",
        "expected_level": SuspicionLevel.HIGH_RISK,
        "text": (
            "URGENT REQUIREMENT! Females between 18-25 required for Gulf job in Dubai. "
            "No experience required. Guaranteed salary of ₹1,50,000 per month. "
            "All expenses paid — visa, flight, accommodation. Live-in required. "
            "Company will keep your passport for security during employment. "
            "No written contract needed — everything verbal. "
            "Limited contact with family allowed. No personal phones allowed. "
            "Joining must happen within 48 hours. Send full-length photo to apply. "
            "Do not share this offer with anyone. Registration fee ₹5,000 required. "
            "Fair complexion preferred. Cannot leave before 2-year contract ends."
        ),
    },

    {
        "label": "EXAMPLE 2 — Tech Scam Centre (Myanmar)",
        "expected_level": SuspicionLevel.VERY_HIGH,
        "text": (
            "Online data entry job available in Myanmar. High salary — earn ₹2 lakhs per month "
            "working on computers. No experience needed. Company arranges visa, flight, and "
            "accommodation. Hired on the spot — no interview required. Send your Aadhaar to apply. "
            "No personal calls allowed during work hours. Mobile surrender on joining. "
            "Sign agreement before joining. Terms will be shared later. Urgent joining required."
        ),
    },

    {
        "label": "EXAMPLE 3 — Modeling Scam",
        "expected_level": SuspicionLevel.HIGH_RISK,
        "text": (
            "Talent scout is looking for young girls for the entertainment industry. "
            "Good looking females aged 18-25 with fair complexion can earn ₹80,000 per month. "
            "No experience needed. Photoshoot required before joining. "
            "Send intimate photos for portfolio. Keep this confidential. "
            "Do not discuss with family yet. Immediate joining. Pay processing fee of ₹2,000."
        ),
    },

    {
        "label": "EXAMPLE 4 — Bonded Labour Farm Job",
        "expected_level": SuspicionLevel.HIGH_RISK,
        "text": (
            "Agricultural worker required on sugar farm. Advance of ₹20,000 given immediately. "
            "Must repay advance through work. Cannot quit before contract ends. "
            "Accommodation provided at the farm. Limited contact with outside. "
            "Strict discipline policy — penalty for leaving ₹30,000. "
            "Work 12 hours per day, paid weekly in cash."
        ),
    },

    {
        "label": "EXAMPLE 5 — Legitimate Job Offer (Control Case)",
        "expected_level": SuspicionLevel.SAFE,
        "text": (
            "Software Engineer — 3+ years experience required. "
            "Salary: ₹8–12 LPA based on interview. Work from office in Bengaluru. "
            "Monday to Friday, 9 AM to 6 PM. Benefits: PF, ESI, health insurance, "
            "21 days paid leave. Apply with CV to hr@techfirm.co.in. "
            "All candidates must appear for technical interview and HR round. "
            "Offer letter provided before joining. Background verification done."
        ),
    },

    {
        "label": "EXAMPLE 6 — Online Sextortion/Exploitation",
        "expected_level": SuspicionLevel.VERY_HIGH,
        "text": (
            "Work from home webcam job. Earn ₹50,000 per month. No experience required. "
            "Adult entertainment position available. Send intimate photos to apply. "
            "Chat with foreigners online. Dating app job. "
            "All communications monitored. Do not tell family about this job. "
            "Unlimited earning potential. Paid daily in cash."
        ),
    },

    {
        "label": "EXAMPLE 7 — Domestic Worker Trap",
        "expected_level": SuspicionLevel.LOW_RISK,
        "text": (
            "Urgently required: helper for household in Delhi. Female candidates only. "
            "Live-in required. Accommodation and food provided. ₹15,000 per month. "
            "No phone allowed inside the house. Submit Aadhaar and photo on joining. "
            "Immediate joining required. Approached on street or WhatsApp apply."
        ),
    },

    {
        "label": "EXAMPLE 8 — Suspicious But Less Extreme",
        "expected_level": SuspicionLevel.LOW_RISK,
        "text": (
            "Sales executive needed. Flexible work timings. Easy work, high commission. "
            "No experience needed. Salary + unlimited earning potential. "
            "Travel required to meet clients. Immediate joining preferred."
        ),
    },
]


# ===========================================================================
# MAIN — Run test cases
# ===========================================================================

if __name__ == "__main__":
    analyzer = ScamAnalyzer()

    print("=" * 65)
    print("  AegisAI Scam Analyzer — Test Run")
    print(f"  Total Indicators Loaded: {len(ALL_INDICATORS)}")
    print(f"  Maximum Possible Score : {MAX_POSSIBLE_SCORE}")
    print("=" * 65)

    for case in EXAMPLE_CASES:
        print(f"\n{'─' * 65}")
        print(f"  {case['label']}")
        print(f"{'─' * 65}")
        result = analyzer.analyze(case["text"])
        report = analyzer.format_report(result)
        print(report)
        expected = case["expected_level"].value
        actual = result.suspicion_level.value
        status = "✅ PASS" if actual == expected else f"⚠️ EXPECTED {expected}"
        print(f"  Test: {status}")
        print()

    print("\n" + "=" * 65)
    print("  Indicator Summary by Category:")
    print("=" * 65)

    cat_summary: Dict[str, int] = {}
    for ind in ALL_INDICATORS:
        cat_summary[ind.category] = cat_summary.get(ind.category, 0) + 1

    for cat, count in sorted(cat_summary.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:<35}: {count} indicators")

    print(f"\n  TOTAL INDICATORS: {len(ALL_INDICATORS)}")
    print("=" * 65)
