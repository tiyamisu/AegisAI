"""
AegisAI — Core Chatbot Engine
==============================
Central orchestrator for the AegisAI anti-trafficking assistant.
Handles intent classification, session management, module routing,
and response generation.

Architecture:
  ChatBot
    ├── KnowledgeBaseManager   — KB lookup and response retrieval
    ├── ExpertSystemEngine     — Inference and risk classification
    ├── RiskAssessmentModule   — Interactive questionnaire
    └── ScamDetector           — Job offer analysis

Author  : AegisAI Team
Version : 1.0
"""

import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

from knowledge_base  import KnowledgeBaseManager, CATEGORIES, CATEGORY_DISPLAY_NAMES
from expert_system   import ExpertSystemEngine, AssessmentResult
from risk_assessment import RiskAssessmentModule, AssessmentState
from scam_detector   import ScamDetector, DetectionResult


# ===========================================================================
# INTENT CONSTANTS
# ===========================================================================

class Intent(Enum):
    """All recognised user intents."""
    # Navigation
    MENU            = "menu"
    HELP            = "help"
    GREETING        = "greeting"
    GOODBYE         = "goodbye"
    UNCLEAR         = "unclear"

    # Knowledge base
    LEARN_BASICS    = "learn_basics"
    LEARN_SIGNS     = "learn_signs"
    LEARN_SCAMS     = "learn_scams"
    LEARN_CHILD     = "learn_child"
    LEARN_LABOUR    = "learn_labour"
    LEARN_GROOMING  = "learn_grooming"
    LEARN_SUPPORT   = "learn_support"
    LEARN_REPORTING = "learn_reporting"
    LEARN_LEGAL     = "learn_legal"
    LEARN_SAFETY    = "learn_safety"
    LEARN_NGOS      = "learn_ngos"
    LEARN_FAQS      = "learn_faqs"

    # Actions
    RISK_ASSESSMENT = "risk_assessment"
    JOB_ANALYZE     = "job_analyze"
    EMERGENCY       = "emergency"
    REPORT_CRIME    = "report_crime"
    HELPLINES       = "helplines"

    # Assessment flow
    ANSWER_YES      = "answer_yes"
    ANSWER_NO       = "answer_no"
    STOP_ASSESSMENT = "stop_assessment"


# ===========================================================================
# INTENT PATTERNS
# ===========================================================================

_INTENT_PATTERNS: List[Tuple[Intent, List[str]]] = [
    # Emergency — highest priority
    (Intent.EMERGENCY, [
        "help me", "emergency", "in danger", "hurt me", "trapped",
        "scared", "i am in danger", "abuse", "violence", "threatening",
        "kidnapped", "forced", "i need help now", "please help",
        "cannot leave", "held against",
    ]),
    # Greeting
    (Intent.GREETING, [
        "hello", "hi", "hey", "good morning", "good evening",
        "namaste", "good afternoon", "howdy", "greetings",
    ]),
    # Goodbye
    (Intent.GOODBYE, [
        "bye", "goodbye", "exit", "quit", "close", "later",
        "see you", "thanks bye", "ok bye",
    ]),
    # Risk assessment
    (Intent.RISK_ASSESSMENT, [
        "risk assessment", "assess my risk", "check my risk",
        "am i safe", "is my situation safe", "risk check",
        "how at risk am i", "assess situation",
    ]),
    # Job analysis
    (Intent.JOB_ANALYZE, [
        "analyze job", "check job", "job offer", "is this job safe",
        "job scam", "analyze offer", "verify job", "job safe",
        "is this a scam", "check this offer", "job description",
        "suspicious job", "red flags job",
    ]),
    # Helplines
    (Intent.HELPLINES, [
        "helpline", "phone number", "contact", "call", "hotline",
        "who to call", "emergency number", "police number",
        "childline", "ngos number", "support line",
    ]),
    # Reporting
    (Intent.REPORT_CRIME, [
        "report", "how to report", "file complaint", "police complaint",
        "report trafficking", "report abuse", "file fir",
        "where to report", "how do i report",
    ]),
    # Learning — Knowledge base categories
    (Intent.LEARN_BASICS, [
        "what is human trafficking", "define trafficking",
        "explain trafficking", "what is trafficking",
        "trafficking basics", "trafficking meaning",
        "types of trafficking", "what are the types",
    ]),
    (Intent.LEARN_SIGNS, [
        "warning signs", "red flags", "signs of trafficking",
        "how to identify", "indicators", "recognize trafficking",
        "suspicious signs", "warning",
    ]),
    (Intent.LEARN_SCAMS, [
        "recruitment scam", "fake job", "job scam", "scam recruitment",
        "fake offer", "job fraud", "fraudulent job",
    ]),
    (Intent.LEARN_CHILD, [
        "child trafficking", "children trafficking", "minor trafficking",
        "child abuse", "child safety", "protect child", "child rights",
    ]),
    (Intent.LEARN_LABOUR, [
        "forced labour", "bonded labour", "labour trafficking",
        "debt bondage", "forced work", "labour exploitation",
    ]),
    (Intent.LEARN_GROOMING, [
        "online grooming", "grooming", "online predator",
        "internet safety", "social media safety", "online abuse",
        "cyber grooming", "catfishing",
    ]),
    (Intent.LEARN_SUPPORT, [
        "victim support", "support for victims", "help for victims",
        "counselling", "rehabilitation", "survivor support",
    ]),
    (Intent.LEARN_REPORTING, [
        "how to report", "reporting procedure", "file complaint",
        "report to police", "report a case",
    ]),
    (Intent.LEARN_LEGAL, [
        "legal rights", "my rights", "law against trafficking",
        "itpa", "pocso", "legal protection", "constitution rights",
        "victim rights", "legal aid",
    ]),
    (Intent.LEARN_SAFETY, [
        "safety tips", "stay safe", "how to stay safe",
        "personal safety", "safety measures", "how to be safe",
        "safety precautions",
    ]),
    (Intent.LEARN_NGOS, [
        "ngo", "organisation", "organization", "support groups",
        "who can help", "which ngo", "anti trafficking ngo",
    ]),
    (Intent.LEARN_FAQS, [
        "faq", "frequently asked", "common questions",
        "basic questions", "general questions",
    ]),
    # Assessment answers
    (Intent.ANSWER_YES, ["yes", "y", "yeah", "yep", "correct", "true",
                          "absolutely", "definitely", "sure", "affirmative"]),
    (Intent.ANSWER_NO,  ["no", "n", "nope", "incorrect", "false",
                          "not really", "negative", "nah"]),
    (Intent.STOP_ASSESSMENT, ["stop", "cancel", "abort", "exit assessment",
                               "quit assessment", "go back", "leave"]),
    # Menu / help
    (Intent.MENU, ["menu", "main menu", "home", "back", "start",
                   "begin", "options", "what can you do", "features"]),
    (Intent.HELP, ["help", "how to use", "guide", "instructions",
                   "what can you do", "usage"]),
]


# ===========================================================================
# CHAT RESPONSE
# ===========================================================================

@dataclass
class ChatResponse:
    """
    A single structured response from the chatbot.

    Attributes:
        text         : Main response text to display
        intent       : Classified intent of the user input
        risk_level   : Current session risk level (if assessed)
        is_emergency : True if emergency protocol should activate
        show_menu    : True if main menu should be displayed after response
        module_data  : Optional structured data (for GUI to use)
        timestamp    : Time of response generation
    """
    text:         str
    intent:       Intent = Intent.UNCLEAR
    risk_level:   str    = "UNKNOWN"
    is_emergency: bool   = False
    show_menu:    bool   = False
    module_data:  Any    = None
    timestamp:    float  = field(default_factory=time.time)


# ===========================================================================
# SESSION STATE
# ===========================================================================

@dataclass
class SessionState:
    """Tracks state for the current chat session."""
    risk_level:        str   = "UNKNOWN"
    risk_score:        int   = 0
    is_emergency:      bool  = False
    assessment_done:   bool  = False
    job_analysis_done: bool  = False
    message_count:     int   = 0
    user_type:         str   = "unknown"   # victim, family, ngo, student, citizen
    last_intent:       Optional[Intent] = None
    pending_job_text:  bool  = False       # True when waiting for job text input


# ===========================================================================
# MAIN CHATBOT CLASS
# ===========================================================================

class ChatBot:
    """
    AegisAI Core Chatbot Engine.

    Orchestrates all AI modules and manages the conversation flow.
    Provides a single public method — process() — that accepts raw
    user input and returns a ChatResponse.

    Example:
        bot = ChatBot()
        print(bot.process("hello").text)
        print(bot.process("start risk assessment").text)
        print(bot.process("yes").text)
    """

    # ------------------------------------------------------------------
    # MAIN MENU TEXT
    # ------------------------------------------------------------------
    _MAIN_MENU = (
        "━" * 50 + "\n"
        "  🛡️  AegisAI — Main Menu\n"
        "━" * 50 + "\n\n"
        "  📚 Knowledge Base:\n"
        "    1. Human Trafficking Basics\n"
        "    2. Warning Signs\n"
        "    3. Recruitment Scams\n"
        "    4. Child Trafficking\n"
        "    5. Forced Labour\n"
        "    6. Online Grooming\n\n"
        "  🤝 Support:\n"
        "    7. Victim Support\n"
        "    8. Emergency Assistance\n"
        "    9. Reporting Procedures\n"
        "   10. Legal Rights\n"
        "   11. Safety Measures\n"
        "   12. NGO Support\n\n"
        "  🔍 AI Tools:\n"
        "   13. Risk Assessment\n"
        "   14. Job Offer Safety Check\n\n"
        "  📞 Helplines:\n"
        "   15. Emergency Contacts\n\n"
        "  Type a number (1-15), ask a question, or type HELP.\n"
        "━" * 50
    )

    # Map menu numbers to intents
    _MENU_MAP: Dict[str, Intent] = {
        "1":  Intent.LEARN_BASICS,
        "2":  Intent.LEARN_SIGNS,
        "3":  Intent.LEARN_SCAMS,
        "4":  Intent.LEARN_CHILD,
        "5":  Intent.LEARN_LABOUR,
        "6":  Intent.LEARN_GROOMING,
        "7":  Intent.LEARN_SUPPORT,
        "8":  Intent.EMERGENCY,
        "9":  Intent.LEARN_REPORTING,
        "10": Intent.LEARN_LEGAL,
        "11": Intent.LEARN_SAFETY,
        "12": Intent.LEARN_NGOS,
        "13": Intent.RISK_ASSESSMENT,
        "14": Intent.JOB_ANALYZE,
        "15": Intent.HELPLINES,
    }

    # Map intent → KB category
    _INTENT_TO_CATEGORY: Dict[Intent, str] = {
        Intent.LEARN_BASICS:    "human_trafficking_basics",
        Intent.LEARN_SIGNS:     "warning_signs",
        Intent.LEARN_SCAMS:     "recruitment_scams",
        Intent.LEARN_CHILD:     "child_trafficking",
        Intent.LEARN_LABOUR:    "forced_labour",
        Intent.LEARN_GROOMING:  "online_grooming",
        Intent.LEARN_SUPPORT:   "victim_support",
        Intent.EMERGENCY:       "emergency_assistance",
        Intent.LEARN_REPORTING: "reporting_procedures",
        Intent.LEARN_LEGAL:     "legal_rights",
        Intent.LEARN_SAFETY:    "safety_measures",
        Intent.LEARN_NGOS:      "ngo_support",
        Intent.LEARN_FAQS:      "faqs",
    }

    # ------------------------------------------------------------------
    # INITIALISATION
    # ------------------------------------------------------------------

    def __init__(self):
        """
        Initialise the chatbot and all AI modules.
        """
        print("[ChatBot] Initialising AegisAI...")

        # Load all AI modules
        self._kb      = KnowledgeBaseManager()
        self._expert  = ExpertSystemEngine()
        self._risk    = RiskAssessmentModule(self._expert)
        self._scam    = ScamDetector()

        # Session state
        self._session = SessionState()

        print(f"[ChatBot] Ready. KB entries: {self._kb.total_entries()}, "
              f"Scam indicators: {self._scam.get_indicator_count()}")

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def process(self, user_input: str) -> ChatResponse:
        """
        Process a single user message and return a ChatResponse.

        Args:
            user_input: Raw text entered by the user

        Returns:
            ChatResponse with the bot's reply and metadata
        """
        self._session.message_count += 1
        clean = user_input.strip()

        if not clean:
            return self._respond(
                "Please type a message. For the main menu, type MENU.",
                Intent.UNCLEAR
            )

        # --- Route based on active module state ---
        if self._risk.is_active():
            return self._handle_assessment_input(clean)

        if self._session.pending_job_text:
            return self._handle_job_text(clean)

        # --- Classify intent ---
        intent = self._classify_intent(clean)
        self._session.last_intent = intent

        # --- Dispatch ---
        return self._dispatch(intent, clean)

    def get_welcome_message(self) -> str:
        """Return the initial welcome message for a new session."""
        return (
            "━" * 50 + "\n"
            "  🛡️  Welcome to AegisAI\n"
            "  AI-Powered Human Trafficking Prevention\n"
            "━" * 50 + "\n\n"
            "I am your confidential AI assistant.\n\n"
            "I can help you:\n"
            "  📚 Learn about human trafficking\n"
            "  🔍 Assess your current risk level\n"
            "  💼 Check if a job offer is safe\n"
            "  🆘 Find emergency help and contacts\n"
            "  ⚖️  Understand your legal rights\n\n"
            "All conversations are PRIVATE and ANONYMOUS.\n\n"
            "━" * 50 + "\n"
            "Type MENU for all options, or just start talking!\n"
            "━" * 50
        )

    def get_main_menu(self) -> str:
        """Return the main menu text."""
        return self._MAIN_MENU

    def get_session_state(self) -> SessionState:
        """Return the current session state."""
        return self._session

    def reset_session(self):
        """Reset the session state and all module states."""
        self._session = SessionState()
        self._risk.abort()
        self._expert.new_session()
        print("[ChatBot] Session reset.")

    # ------------------------------------------------------------------
    # INTENT CLASSIFICATION
    # ------------------------------------------------------------------

    def _classify_intent(self, text: str) -> Intent:
        """
        Classify user input into an Intent using keyword matching.

        Algorithm:
          1. Check if input is a menu number
          2. Check for exact menu/home commands
          3. Match against all intent pattern lists
          4. Return the first matching intent (patterns are priority-ordered)
          5. Fall back to KB query if no pattern matches

        Args:
            text: Cleaned user input

        Returns:
            Classified Intent
        """
        lower = text.lower().strip()

        # Menu number shortcut
        if lower in self._MENU_MAP:
            return self._MENU_MAP[lower]

        # Exact single-word menu/home commands always route to MENU
        if lower in ("menu", "home", "start", "main menu", "back"):
            return Intent.MENU

        # Pattern matching
        for intent, patterns in _INTENT_PATTERNS:
            for pattern in patterns:
                if pattern in lower:
                    return intent

        # Check KB for a reasonable match
        results = self._kb.query(text, top_n=1)
        if results and results[0].confidence >= 0.2:
            return Intent.LEARN_BASICS  # Generic KB intent

        return Intent.UNCLEAR

    # ------------------------------------------------------------------
    # DISPATCH
    # ------------------------------------------------------------------

    def _dispatch(self, intent: Intent, raw_input: str) -> ChatResponse:
        """Route a classified intent to the appropriate handler."""
        handlers = {
            Intent.GREETING:        self._handle_greeting,
            Intent.GOODBYE:         self._handle_goodbye,
            Intent.MENU:            self._handle_menu,
            Intent.HELP:            self._handle_help,
            Intent.EMERGENCY:       self._handle_emergency,
            Intent.HELPLINES:       self._handle_helplines,
            Intent.RISK_ASSESSMENT: self._handle_start_assessment,
            Intent.JOB_ANALYZE:     self._handle_start_job_analyze,
            Intent.REPORT_CRIME:    self._handle_report_crime,
            Intent.UNCLEAR:         self._handle_unclear,
        }

        # Knowledge base category handlers
        kb_intents = {
            Intent.LEARN_BASICS, Intent.LEARN_SIGNS, Intent.LEARN_SCAMS,
            Intent.LEARN_CHILD, Intent.LEARN_LABOUR, Intent.LEARN_GROOMING,
            Intent.LEARN_SUPPORT, Intent.LEARN_REPORTING, Intent.LEARN_LEGAL,
            Intent.LEARN_SAFETY, Intent.LEARN_NGOS, Intent.LEARN_FAQS,
        }

        if intent in kb_intents:
            return self._handle_kb_query(intent, raw_input)

        handler = handlers.get(intent, self._handle_unclear)
        return handler(raw_input)

    # ------------------------------------------------------------------
    # HANDLERS — Navigation
    # ------------------------------------------------------------------

    def _handle_greeting(self, _: str) -> ChatResponse:
        greetings = [
            "Hello! I'm AegisAI, your confidential anti-trafficking assistant.\n\n"
            "I can help you learn about trafficking, assess risks, or get emergency help.\n"
            "Type MENU to see all options.",
        ]
        return self._respond(greetings[0], Intent.GREETING)

    def _handle_goodbye(self, _: str) -> ChatResponse:
        return self._respond(
            "Stay safe! Remember:\n"
            "  • Police: 100\n"
            "  • Childline: 1098\n"
            "  • Emergency: 112\n\n"
            "You can return to AegisAI anytime. Goodbye! 🛡️",
            Intent.GOODBYE
        )

    def _handle_menu(self, _: str) -> ChatResponse:
        return ChatResponse(
            text=self._MAIN_MENU,
            intent=Intent.MENU,
            risk_level=self._session.risk_level,
            show_menu=True,
        )

    def _handle_help(self, _: str) -> ChatResponse:
        help_text = (
            "AegisAI — How to Use\n\n"
            "━ Chat naturally — just ask your question\n"
            "━ Type a number (1-15) from the main menu\n"
            "━ Say MENU to see all options\n"
            "━ Say RISK ASSESSMENT to start risk check\n"
            "━ Say CHECK JOB to analyze a job offer\n"
            "━ Say EMERGENCY for immediate help\n\n"
            "All conversations are CONFIDENTIAL.\n"
            "No data is stored or shared."
        )
        return self._respond(help_text, Intent.HELP)

    # ------------------------------------------------------------------
    # HANDLERS — Emergency
    # ------------------------------------------------------------------

    def _handle_emergency(self, _: str) -> ChatResponse:
        self._session.is_emergency = True
        response = self._kb.get_emergency_response()
        return ChatResponse(
            text=response,
            intent=Intent.EMERGENCY,
            risk_level="CRITICAL",
            is_emergency=True,
        )

    def _handle_helplines(self, _: str) -> ChatResponse:
        text = (
            "📞 AegisAI Emergency Helplines\n\n"
            "  🆘 EMERGENCY              : 112 (24/7, Free)\n"
            "  🚔 Police                 : 100 (24/7, Free)\n"
            "  🧒 Childline India        : 1098 (24/7, Free)\n"
            "  👩 Women's Helpline       : 1091 (24/7, Free)\n"
            "  🏥 Ambulance              : 108 (24/7, Free)\n"
            "  ⚖️  NHRC                   : 14433\n"
            "  📋 Labour Helpline        : 1800-425-1013\n"
            "  💻 Cyber Crime Helpline   : 1930\n"
            "  ✈️  MEA Overseas Helpline  : 1800-11-3090\n\n"
            "For overseas: contact the nearest Indian Embassy or Consulate."
        )
        return self._respond(text, Intent.HELPLINES)

    # ------------------------------------------------------------------
    # HANDLERS — Knowledge Base
    # ------------------------------------------------------------------

    def _handle_kb_query(self, intent: Intent, raw_input: str) -> ChatResponse:
        """
        Handle a knowledge base category or keyword query.
        """
        category = self._INTENT_TO_CATEGORY.get(intent)

        if category:
            # Try to find a specific entry within the category
            results = self._kb.query(raw_input, top_n=1)
            if results and results[0].confidence >= 0.15 and results[0].category == category:
                return self._respond(results[0].response, intent)
            else:
                # Return category overview
                cat_results = self._kb.query_by_category(category)
                if cat_results:
                    return self._respond(cat_results[0].response, intent)

        # General KB query
        response = self._kb.get_best_response(raw_input)
        return self._respond(response, intent)

    # ------------------------------------------------------------------
    # HANDLERS — Risk Assessment
    # ------------------------------------------------------------------

    def _handle_start_assessment(self, _: str) -> ChatResponse:
        """Begin a new risk assessment session."""
        self._risk.start()
        intro = RiskAssessmentModule.intro_text()
        first_q = self._risk.current_question_text()
        return ChatResponse(
            text=f"{intro}\n{first_q}",
            intent=Intent.RISK_ASSESSMENT,
            risk_level=self._session.risk_level,
        )

    def _handle_assessment_input(self, text: str) -> ChatResponse:
        """Handle user input during an active risk assessment."""
        lower = text.lower().strip()

        # Check for abort
        if any(kw in lower for kw in ["stop", "cancel", "abort", "quit", "exit"]):
            self._risk.abort()
            return self._respond(
                "Risk assessment stopped.\n\n"
                "You can restart anytime by saying 'Risk Assessment'.\n"
                "Type MENU for other options.",
                Intent.STOP_ASSESSMENT
            )

        # Parse Yes/No
        is_yes = any(kw in lower for kw in
                     ["yes", "y", "yeah", "yep", "correct", "true", "sure", "absolutely"])
        is_no  = any(kw in lower for kw in
                     ["no", "n", "nope", "false", "not", "never", "nah"])

        if not is_yes and not is_no:
            q = self._risk.current_question()
            return self._respond(
                f"Please answer YES or NO.\n\n{self._risk.current_question_text()}",
                Intent.UNCLEAR
            )

        # Submit answer
        answer = is_yes
        next_q = self._risk.submit_answer(answer)

        # Check if assessment is complete
        if self._risk.is_complete():
            result = self._risk.get_result()
            if result:
                self._session.risk_level      = result.risk_level
                self._session.risk_score      = result.risk_score
                self._session.is_emergency    = result.is_emergency
                self._session.assessment_done = True

                response_text = (
                    self._risk.get_formatted_result() + "\n\n" +
                    RiskAssessmentModule.outro_text(result)
                )

                return ChatResponse(
                    text=response_text,
                    intent=Intent.RISK_ASSESSMENT,
                    risk_level=result.risk_level,
                    is_emergency=result.is_emergency,
                    module_data=result,
                )

        # Still in progress — return next question
        if next_q:
            return self._respond(next_q, Intent.RISK_ASSESSMENT)

        return self._respond(
            "Processing your answers...",
            Intent.RISK_ASSESSMENT
        )

    # ------------------------------------------------------------------
    # HANDLERS — Job Analysis
    # ------------------------------------------------------------------

    def _handle_start_job_analyze(self, raw_input: str) -> ChatResponse:
        """
        Initiate a job offer analysis.
        If the user already included text, analyse immediately.
        Otherwise ask for the job text.
        """
        # Check if text was provided inline
        stripped = raw_input.lower().replace("check job", "").replace(
            "analyze job", "").replace("job offer", "").replace(
            "is this a scam", "").strip()

        if len(stripped) > 30:
            # User provided job text inline
            return self._handle_job_text(stripped)

        # Ask for job text
        self._session.pending_job_text = True
        return self._respond(
            "📋 JOB OFFER SAFETY CHECK\n\n"
            "Please paste the full job advertisement, description, or offer "
            "message below. Include as much text as possible for accurate analysis.\n\n"
            "(Type CANCEL to go back.)",
            Intent.JOB_ANALYZE
        )

    def _handle_job_text(self, text: str) -> ChatResponse:
        """Analyse job description text submitted by the user."""
        self._session.pending_job_text = False

        if text.lower().strip() in ["cancel", "back", "stop"]:
            return self._respond("Job analysis cancelled. Type MENU for options.", Intent.MENU)

        if len(text) < 20:
            return self._respond(
                "Please provide more text — at least a sentence from the job offer "
                "for accurate analysis.",
                Intent.JOB_ANALYZE
            )

        result   = self._scam.analyze(text)
        report   = self._scam.format_report(result)
        self._session.job_analysis_done = True

        return ChatResponse(
            text=report,
            intent=Intent.JOB_ANALYZE,
            risk_level=self._session.risk_level,
            is_emergency=result.is_dangerous,
            module_data=result,
        )

    # ------------------------------------------------------------------
    # HANDLERS — Reporting
    # ------------------------------------------------------------------

    def _handle_report_crime(self, raw_input: str) -> ChatResponse:
        response = self._kb.get_best_response("how to report human trafficking")
        return self._respond(response, Intent.REPORT_CRIME)

    # ------------------------------------------------------------------
    # HANDLERS — Fallback
    # ------------------------------------------------------------------

    def _handle_unclear(self, raw_input: str) -> ChatResponse:
        """
        Handle unrecognised inputs by trying the KB.
        If KB finds nothing, return the fallback menu.
        """
        results = self._kb.query(raw_input, top_n=1)
        if results and results[0].confidence >= 0.1:
            return self._respond(results[0].response, Intent.UNCLEAR)
        return self._respond(self._kb.get_fallback(), Intent.UNCLEAR, show_menu=True)

    # ------------------------------------------------------------------
    # HELPER METHODS
    # ------------------------------------------------------------------

    def _respond(self, text: str, intent: Intent,
                 show_menu: bool = False) -> ChatResponse:
        """Create a ChatResponse with current session context."""
        return ChatResponse(
            text=text,
            intent=intent,
            risk_level=self._session.risk_level,
            is_emergency=self._session.is_emergency,
            show_menu=show_menu,
        )


# ===========================================================================
# MODULE SELF-TEST
# ===========================================================================

if __name__ == "__main__":
    print("AegisAI ChatBot — Self Test")
    print("=" * 55)

    bot = ChatBot()

    test_inputs = [
        "hello",
        "what is human trafficking",
        "warning signs",
        "risk assessment",
        "yes",
        "no",
        "yes",
        "no",
        "no",
        "no",
        "no",
        "no",
        "stop",
        "check job offer",
        "Earn 2 lakh per month, no experience. Send photo. Urgent joining. "
        "Registration fee 5000. Passport will be kept.",
        "helplines",
        "bye",
    ]

    for msg in test_inputs:
        print(f"\n{'─' * 50}")
        print(f"  User : {msg[:60]!r}")
        response = bot.process(msg)
        print(f"  Bot  [{response.intent.value}]: {response.text[:120]}...")
        if response.is_emergency:
            print("  *** EMERGENCY FLAG ACTIVE ***")
