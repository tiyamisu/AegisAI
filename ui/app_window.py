"""
AegisAI — Main Application Window
====================================
Root CustomTkinter window. Manages layout, page switching,
and wires all services to all pages.

Layout:
    ┌─────────────────────────────────────┐
    │           HEADER (56px)             │
    ├──────────┬──────────────────────────┤
    │ SIDEBAR  │       CONTENT AREA       │
    │ (210px)  │    (dynamic page frame)  │
    └──────────┴──────────────────────────┘
"""
from __future__ import annotations

import logging
import sys
import os

import customtkinter as ctk

# ── Project path ──────────────────────────────────────────────────────────
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from ui.theme import Theme
from ui.components.sidebar import Sidebar
from ui.components.header import Header

from services.session_service import SessionService
from services.chat_service import ChatService
from services.assessment_service import AssessmentService
from services.scam_service import ScamService
from knowledge.kb_manager import KBManager
from knowledge.rule_engine import RuleEngine

from ui.pages.dashboard import DashboardPage
from ui.pages.awareness import AwarenessPage
from ui.pages.assessment import AssessmentPage
from ui.pages.scam_analyzer import ScamAnalyzerPage
from ui.pages.emergency import EmergencyPage
from ui.pages.resources import ResourcesPage

log = logging.getLogger(__name__)

# Page title map
PAGE_TITLES = {
    "dashboard":    "Dashboard",
    "awareness":    "Awareness Center",
    "assessment":   "Risk Assessment",
    "scam_analyzer": "Scam Analyzer",
    "emergency":    "Emergency Help",
    "resources":    "Resources & Guidance",
}


class AegisAIApp:
    """
    Root application controller.

    Responsibilities:
    - Create and configure the CTk root window
    - Instantiate all services (dependency injection)
    - Build the layout: header, sidebar, content area
    - Manage page navigation (show/hide frames)
    - Wire SOS events to emergency page + sidebar flash
    """

    WINDOW_TITLE  = "AegisAI — AI-Powered Anti-Trafficking Platform"
    WINDOW_SIZE   = "1280x780"
    WINDOW_MIN_W  = 960
    WINDOW_MIN_H  = 640

    def __init__(self) -> None:
        # ── CustomTkinter global config ──────────────────────────────
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ── Root window ───────────────────────────────────────────────
        self._root = ctk.CTk()
        self._root.title(self.WINDOW_TITLE)
        self._root.geometry(self.WINDOW_SIZE)
        self._root.minsize(self.WINDOW_MIN_W, self.WINDOW_MIN_H)
        self._root.configure(fg_color=Theme.BG_DARK)

        # ── Services ──────────────────────────────────────────────────
        self._session = SessionService.instance()
        self._kb      = KBManager()
        self._engine  = RuleEngine()

        self._chat_svc  = ChatService(
            kb=self._kb,
            rule_engine=self._engine,
            session=self._session,
            navigate_cb=self._navigate_to,
        )
        self._assess_svc = AssessmentService(rule_engine=self._engine)
        self._scam_svc   = ScamService()

        # Subscribe to risk changes → update header badge
        self._session.on_risk_change(self._on_risk_change)

        # ── Build layout ──────────────────────────────────────────────
        self._build_layout()

        # ── Create pages (lazy-instantiated once, cached) ─────────────
        self._pages: dict[str, ctk.CTkFrame] = {}
        self._current_page: str = ""

        self._init_pages()

        # ── Show initial page ─────────────────────────────────────────
        self._navigate_to("dashboard")

        log.info("AegisAI window ready.")

    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the Tkinter event loop."""
        self._root.mainloop()

    # ------------------------------------------------------------------

    def _build_layout(self) -> None:
        """Create the 3-zone layout: header / sidebar / content."""
        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_columnconfigure(1, weight=1)

        # Header (full width, top)
        self._header = Header(self._root, on_sos=self._on_sos)
        self._header.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Sidebar (left, below header)
        self._sidebar = Sidebar(self._root, navigate_cb=self._navigate_to)
        self._sidebar.grid(row=1, column=0, sticky="nsew")

        # Vertical divider
        ctk.CTkFrame(self._root, width=1, fg_color=Theme.BORDER).grid(
            row=1, column=0, sticky="nse", padx=(Theme.SIDEBAR_W, 0)
        )

        # Content frame (right, below header)
        self._content = ctk.CTkFrame(self._root, fg_color=Theme.BG_DARK, corner_radius=0)
        self._content.grid(row=1, column=1, sticky="nsew")
        self._content.grid_rowconfigure(0, weight=1)
        self._content.grid_columnconfigure(0, weight=1)

    def _init_pages(self) -> None:
        """Instantiate all pages and place them in the content area."""
        kb_stats = self._kb.stats()

        pages_config = {
            "dashboard":    lambda: DashboardPage(
                self._content, self._chat_svc, kb_stats
            ),
            "awareness":    lambda: AwarenessPage(self._content, self._kb),
            "assessment":   lambda: AssessmentPage(
                self._content, self._assess_svc, self._session,
                navigate_cb=self._navigate_to,
            ),
            "scam_analyzer": lambda: ScamAnalyzerPage(self._content, self._scam_svc),
            "emergency":    lambda: EmergencyPage(self._content),
            "resources":    lambda: ResourcesPage(self._content),
        }

        for name, factory in pages_config.items():
            frame = factory()
            frame.grid(row=0, column=0, sticky="nsew")
            self._pages[name] = frame

        # Initially hide all
        for frame in self._pages.values():
            frame.grid_remove()

    # ------------------------------------------------------------------

    def _navigate_to(self, page: str) -> None:
        """Switch to the specified page (thread-safe via after())."""
        # If called from a background thread, reschedule on main thread
        if not self._is_main_thread():
            self._root.after(0, lambda: self._navigate_to(page))
            return

        if page not in self._pages:
            log.warning("Unknown page: %s", page)
            return

        # Hide current
        if self._current_page and self._current_page in self._pages:
            self._pages[self._current_page].grid_remove()

        # Show new
        self._pages[page].grid(row=0, column=0, sticky="nsew")
        self._current_page = page

        # Update header + sidebar
        self._header.set_title(PAGE_TITLES.get(page, page.title()))
        self._sidebar.set_active(page)
        self._session.set_page(page)

        log.debug("Navigated to: %s", page)

    def _on_sos(self) -> None:
        """Handle SOS button click — navigate to emergency and flash."""
        self._navigate_to("emergency")
        self._sidebar.flash_emergency()
        self._header.flash_sos()
        log.warning("SOS triggered by user.")

    def _on_risk_change(self, level) -> None:
        """Called when session risk level changes — update header badge."""
        self._root.after(0, lambda: self._header.set_risk(level))

    @staticmethod
    def _is_main_thread() -> bool:
        import threading
        return threading.current_thread() is threading.main_thread()
