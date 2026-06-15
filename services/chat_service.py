"""
AegisAI — Chat Service
========================
Manages the conversation: routing user input to the correct handler,
building ChatMessage responses, maintaining conversation history, and saving to SQLite.
"""
from __future__ import annotations

import logging
from typing import Callable, List, Optional

from models.message import ChatMessage, MessageRole
from models.assessment import RiskLevel
from services.database_service import DatabaseService
from .intent_service import Intent, IntentService
from .session_service import SessionService

log = logging.getLogger(__name__)

# Typing-indicator delay in ms (used by UI layer)
TYPING_DELAY_MS = 800


class ChatService:
    """
    Core conversation engine with SQLite integration.

    Responsibilities:
    - Receive raw user text
    - Classify intent via IntentService
    - Route to the appropriate knowledge / module handler
    - Build and return typed ChatMessage responses
    - Maintain and load conversation history from SQLite
    - Expose navigate_callback so chat can trigger page navigation
    """

    # Welcome message shown at session start
    WELCOME = (
        "👋  Hello! I'm AegisAI — your AI-powered guide to human trafficking "
        "prevention and victim support.\n\n"
        "I can help you:\n"
        "  🛡️  Learn about human trafficking\n"
        "  📊  Assess your risk situation\n"
        "  🔍  Analyze suspicious job offers\n"
        "  🆘  Access emergency help & helplines\n"
        "  ⚖️  Understand your legal rights\n\n"
        "How can I help you today?"
    )

    def __init__(
        self,
        kb,
        rule_engine,
        session: SessionService,
        navigate_cb: Optional[Callable[[str], None]] = None,
    ) -> None:
        self._kb          = kb
        self._engine      = rule_engine
        self._session     = session
        self._navigate_cb = navigate_cb
        self._db          = DatabaseService()
        self._intent_svc  = IntentService(kb_manager=kb)
        self._history: List[ChatMessage] = []
        log.info("ChatService ready.")

    # ------------------------------------------------------------------

    @property
    def history(self) -> List[ChatMessage]:
        return self._history

    def get_welcome(self) -> ChatMessage:
        """Return the initial welcome message, or load history if it exists."""
        db_messages = self._db.get_messages(self._session.session_id)
        if db_messages:
            self._history = db_messages
            # Return the last message in history or a standard message to not duplicate
            log.info("Loaded %d chat messages from database.", len(db_messages))
            return db_messages[-1]

        msg = ChatMessage.bot(
            self.WELCOME,
            suggestions=self._kb.get_suggestions("default"),
        )
        self._history.append(msg)
        # Save welcome message to database
        self._db.save_message(
            self._session.session_id,
            "bot",
            msg.text,
            is_emergency=msg.is_emergency,
            suggestions=msg.suggestions,
            intent="WELCOME"
        )
        return msg

    def send(self, text: str) -> ChatMessage:
        """
        Process user input and return a bot ChatMessage.

        This is called from a background thread by the UI layer.
        It is synchronous — the threading is managed by the caller.
        """
        # 1. Classify intent
        intent = self._intent_svc.classify(text)
        log.debug("Intent: %s  |  text: %.40s…", intent.name, text)

        # 2. Save user message to database
        user_msg = ChatMessage.user(text)
        user_msg.intent = intent.name
        self._history.append(user_msg)
        self._session.increment_messages()
        self._db.save_message(
            self._session.session_id,
            "user",
            text,
            is_emergency=False,
            intent=intent.name
        )

        # 3. Dispatch to handler
        response = self._dispatch(intent, text)

        # 4. Save response to database
        self._history.append(response)
        self._db.save_message(
            self._session.session_id,
            "bot",
            response.text,
            is_emergency=response.is_emergency,
            suggestions=response.suggestions,
            intent=intent.name
        )

        return response

    # ------------------------------------------------------------------
    # Intent dispatcher — one handler per intent family

    def _dispatch(self, intent: Intent, text: str) -> ChatMessage:
        handlers = {
            Intent.GREETING:          self._handle_greeting,
            Intent.MENU:              self._handle_menu,
            Intent.EMERGENCY:         self._handle_emergency,
            Intent.RISK_ASSESSMENT:   self._handle_risk_assessment,
            Intent.JOB_ANALYSIS:      self._handle_job_analysis,
            Intent.WARNING_SIGNS:     self._handle_kb_query,
            Intent.CHILD_TRAFFICKING: self._handle_kb_query,
            Intent.FORCED_LABOUR:     self._handle_kb_query,
            Intent.ONLINE_GROOMING:   self._handle_kb_query,
            Intent.REPORTING:         self._handle_kb_query,
            Intent.LEGAL_RIGHTS:      self._handle_kb_query,
            Intent.NGO_SUPPORT:       self._handle_kb_query,
            Intent.SAFETY_TIPS:       self._handle_kb_query,
            Intent.LEARN_BASICS:      self._handle_kb_query,
            Intent.UNCLEAR:           self._handle_unclear,
        }
        handler = handlers.get(intent, self._handle_unclear)
        return handler(text, intent)

    # ------------------------------------------------------------------
    # Handlers

    def _handle_greeting(self, text: str, intent: Intent) -> ChatMessage:
        return ChatMessage.bot(
            "Hello! 👋 I'm AegisAI, your anti-trafficking assistant.\n\n"
            "I'm here to help with awareness, risk assessment, job offer analysis, "
            "and emergency guidance. What would you like to know?",
            suggestions=self._kb.get_suggestions("default"),
            intent=intent.name,
        )

    def _handle_menu(self, text: str, intent: Intent) -> ChatMessage:
        return ChatMessage.bot(
            "📋  Here's what I can help you with:\n\n"
            "  1️⃣  Learn about human trafficking\n"
            "  2️⃣  Understand warning signs\n"
            "  3️⃣  Start a risk assessment\n"
            "  4️⃣  Analyze a job offer for scams\n"
            "  5️⃣  Get emergency help\n"
            "  6️⃣  Know your legal rights\n"
            "  7️⃣  Find NGO support\n\n"
            "You can also use the sidebar on the left to navigate directly.",
            suggestions=self._kb.get_suggestions("default"),
            intent=intent.name,
        )

    def _handle_emergency(self, text: str, intent: Intent) -> ChatMessage:
        info = self._kb.get_emergency_info()
        if self._navigate_cb:
            self._navigate_cb("emergency")
        return ChatMessage.bot(
            text=info,
            is_emergency=True,
            suggestions=["What is the escape plan?", "Find nearby shelter", "Report to police"],
            intent=intent.name,
        )

    def _handle_risk_assessment(self, text: str, intent: Intent) -> ChatMessage:
        if self._navigate_cb:
            self._navigate_cb("assessment")
        return ChatMessage.bot(
            "🛡️  I'm opening the Risk Assessment wizard for you.\n\n"
            "You'll answer 15 simple yes/no questions. Based on your answers, "
            "our expert system will classify your risk level and provide "
            "personalised guidance.\n\n"
            "Please use the Risk Assessment page that just opened in the sidebar.",
            suggestions=["What is risk assessment?", "Is it confidential?"],
            intent=intent.name,
        )

    def _handle_job_analysis(self, text: str, intent: Intent) -> ChatMessage:
        if self._navigate_cb:
            self._navigate_cb("scam_analyzer")
        return ChatMessage.bot(
            "🔍  I'm opening the Scam Analyzer for you.\n\n"
            "Paste the full job offer text into the Scam Analyzer page and "
            "I'll check it against 110 trafficking red-flag indicators.\n\n"
            "The analyzer will show you:\n"
            "  • Suspicion score\n"
            "  • Detected red flags\n"
            "  • Risk level\n"
            "  • Recommendations",
            suggestions=["Red flags in job offers", "How to verify a job?"],
            intent=intent.name,
        )

    def _handle_kb_query(self, text: str, intent: Intent) -> ChatMessage:
        response = self._kb.get_best_response(text)
        suggestions = self._kb.get_suggestions(intent.suggestion_family)
        return ChatMessage.bot(response, suggestions=suggestions, intent=intent.name)

    def _handle_unclear(self, text: str, intent: Intent) -> ChatMessage:
        return ChatMessage.bot(
            "I'm not sure I understood that. Here are some things I can help with:",
            suggestions=self._kb.get_suggestions("default"),
            intent=intent.name,
        )
