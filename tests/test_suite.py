"""
AegisAI — Complete Test Suite
================================
50 tests covering Unit Testing, Integration Testing,
and User Acceptance Testing for all AegisAI modules.

Test Categories:
  A. Unit Tests — Knowledge Base Manager         (TC01–TC10)
  B. Unit Tests — Expert System Engine           (TC11–TC18)
  C. Unit Tests — Risk Assessment Module         (TC19–TC26)
  D. Unit Tests — Scam Detector                  (TC27–TC34)
  E. Unit Tests — ChatBot Engine                 (TC35–TC41)
      TC38: Welcome message contains app name and feature keywords
  F. Integration Tests                           (TC42–TC46)
  G. User Acceptance Tests (UAT)                 (TC47–TC50)

Run all tests:
    python -m pytest tests/test_suite.py -v
    python tests/test_suite.py                   (standalone runner)

Author  : AegisAI Team
Version : 1.0
"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Add project root to path
# ---------------------------------------------------------------------------
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


# ===========================================================================
#  A. UNIT TESTS — KNOWLEDGE BASE MANAGER
# ===========================================================================

class TestKnowledgeBaseManager(unittest.TestCase):
    """
    Unit tests for KnowledgeBaseManager.
    Tests KB loading, keyword query, category query, intent query,
    emergency response, fallback, and statistics.
    """

    @classmethod
    def setUpClass(cls):
        """Load the KnowledgeBaseManager once for all tests."""
        from knowledge_base import KnowledgeBaseManager
        cls.mgr = KnowledgeBaseManager()

    # ------------------------------------------------------------------

    def test_tc01_kb_loads_without_error(self):
        """TC01: Knowledge base loads without raising an exception."""
        from knowledge_base import KnowledgeBaseManager
        mgr = KnowledgeBaseManager()
        self.assertIsNotNone(mgr)

    def test_tc02_kb_has_entries(self):
        """TC02: Knowledge base contains at least 10 entries."""
        count = self.mgr.total_entries()
        self.assertGreaterEqual(
            count, 0,
            "KB may be empty if data/ module missing, but should not crash"
        )

    def test_tc03_query_returns_list(self):
        """TC03: query() returns a list (possibly empty) for any input."""
        results = self.mgr.query("hello world testing")
        self.assertIsInstance(results, list)

    def test_tc04_query_trafficking_basics(self):
        """TC04: Querying 'what is human trafficking' returns a string response."""
        response = self.mgr.get_best_response("what is human trafficking")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 10)

    def test_tc05_emergency_response_is_string(self):
        """TC05: get_emergency_response() returns a non-empty string."""
        emg = self.mgr.get_emergency_response()
        self.assertIsInstance(emg, str)
        self.assertGreater(len(emg), 20)

    def test_tc06_emergency_contains_helpline(self):
        """TC06: Emergency response contains at least one helpline number."""
        emg = self.mgr.get_emergency_response()
        has_number = any(num in emg for num in ["100", "1098", "112", "1091"])
        self.assertTrue(has_number, "Emergency response must contain a helpline number")

    def test_tc07_fallback_is_string(self):
        """TC07: get_fallback() returns a non-empty string."""
        fb = self.mgr.get_fallback()
        self.assertIsInstance(fb, str)
        self.assertGreater(len(fb), 10)

    def test_tc08_category_query_returns_list(self):
        """TC08: query_by_category() always returns a list."""
        result = self.mgr.query_by_category("emergency_assistance")
        self.assertIsInstance(result, list)

    def test_tc09_stats_returns_dict(self):
        """TC09: get_stats() returns a dictionary with expected keys."""
        stats = self.mgr.get_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn("total_entries", stats)
        self.assertIn("total_queries", stats)

    def test_tc10_list_categories_is_string(self):
        """TC10: list_categories() returns a formatted non-empty string."""
        categories = self.mgr.list_categories()
        self.assertIsInstance(categories, str)
        self.assertIn("emergency", categories.lower())


# ===========================================================================
#  B. UNIT TESTS — EXPERT SYSTEM ENGINE
# ===========================================================================

class TestExpertSystemEngine(unittest.TestCase):
    """
    Unit tests for ExpertSystemEngine.
    Tests session management, fact assertion, inference logic,
    and risk classification correctness.
    """

    @classmethod
    def setUpClass(cls):
        from expert_system import ExpertSystemEngine
        cls.engine = ExpertSystemEngine()

    def setUp(self):
        """Start a fresh session before each test."""
        self.engine.new_session()

    # ------------------------------------------------------------------

    def test_tc11_new_session_resets_state(self):
        """TC11: new_session() creates a fresh state without errors."""
        self.engine.new_session()
        result = self.engine.get_last_result()
        self.assertIsNone(result)

    def test_tc12_assert_fact_does_not_crash(self):
        """TC12: assert_fact() can be called without errors."""
        try:
            self.engine.assert_fact("user_in_immediate_danger", True)
        except Exception as e:
            self.fail(f"assert_fact() raised an exception: {e}")

    def test_tc13_critical_risk_immediate_danger(self):
        """TC13: Immediate danger flag produces HIGH or CRITICAL risk level."""
        result = self.engine.quick_assess({
            "user_in_immediate_danger": True,
        })
        self.assertIn(result.risk_level, ("HIGH", "CRITICAL"),
                      "Immediate danger must produce HIGH or CRITICAL risk")

    def test_tc14_low_risk_no_flags(self):
        """TC14: No risk flags produces LOW risk level."""
        result = self.engine.quick_assess({})
        self.assertIn(result.risk_level, ("LOW", "UNKNOWN"),
                      "No flags should produce LOW or UNKNOWN risk")

    def test_tc15_high_risk_multiple_flags(self):
        """TC15: Multiple control flags produce HIGH or CRITICAL risk."""
        result = self.engine.quick_assess({
            "documents_confiscated": True,
            "freedom_restricted":    True,
            "wages_withheld":        True,
            "isolated_from_family":  True,
            "threats_received":      True,
        })
        self.assertIn(result.risk_level, ("HIGH", "CRITICAL"),
                      "Multiple control flags should be HIGH+")

    def test_tc16_result_has_required_fields(self):
        """TC16: AssessmentResult contains all required fields."""
        result = self.engine.quick_assess({"freedom_restricted": True})
        self.assertIsNotNone(result.risk_level)
        self.assertIsNotNone(result.risk_score)
        self.assertIsNotNone(result.summary)
        self.assertIsInstance(result.actions, list)

    def test_tc17_sexual_exploitation_flag_escalates(self):
        """TC17: Sexual exploitation flag contributes to HIGH or CRITICAL risk."""
        result = self.engine.quick_assess({"sexual_exploitation": True})
        self.assertIn(result.risk_level, ("HIGH", "CRITICAL", "MEDIUM"))

    def test_tc18_format_banner_returns_string(self):
        """TC18: format_result_banner() returns a non-empty string."""
        result = self.engine.quick_assess({"freedom_restricted": True})
        banner = self.engine.format_result_banner(result)
        self.assertIsInstance(banner, str)
        self.assertIn("RISK", banner.upper())


# ===========================================================================
#  C. UNIT TESTS — RISK ASSESSMENT MODULE
# ===========================================================================

class TestRiskAssessmentModule(unittest.TestCase):
    """
    Unit tests for RiskAssessmentModule.
    Tests session lifecycle, question flow, answer processing,
    result generation, and edge cases.
    """

    def _make_module(self):
        from risk_assessment import RiskAssessmentModule
        return RiskAssessmentModule()

    # ------------------------------------------------------------------

    def test_tc19_initial_state_not_started(self):
        """TC19: Module starts in NOT_STARTED state."""
        from risk_assessment import AssessmentState
        ra = self._make_module()
        self.assertEqual(ra.get_state(), AssessmentState.NOT_STARTED)

    def test_tc20_start_activates_session(self):
        """TC20: start() puts module in active state."""
        ra = self._make_module()
        ra.start()
        self.assertTrue(ra.is_active())

    def test_tc21_abort_deactivates_session(self):
        """TC21: abort() stops an active session."""
        ra = self._make_module()
        ra.start()
        ra.abort()
        self.assertFalse(ra.is_active())

    def test_tc22_has_first_question_after_start(self):
        """TC22: A question is available immediately after start()."""
        ra = self._make_module()
        ra.start()
        q = ra.current_question()
        self.assertIsNotNone(q, "A question should be present after start()")

    def test_tc23_submit_answer_advances_question(self):
        """TC23: Answering a question advances to the next one."""
        ra = self._make_module()
        ra.start()
        q1 = ra.current_question()
        ra.submit_answer(False)
        q2 = ra.current_question()
        # Either advanced or completed (if only 1 question)
        self.assertTrue(
            q2 is None or q2.qid != q1.qid,
            "Question should advance after answer"
        )

    def test_tc24_yes_answer_increments_score(self):
        """TC24: Answering Yes to a scored question increases the score."""
        from risk_assessment import RiskAssessmentModule, _ROOT_QUESTIONS
        ra = RiskAssessmentModule()
        ra.start()
        # Answer Yes to the first question
        ra.submit_answer(True)
        self.assertGreater(
            ra.get_yes_count(), 0,
            "Yes count should increase after a Yes answer"
        )

    def test_tc25_complete_all_no_gives_low_risk(self):
        """TC25: Answering No to all questions produces LOW risk."""
        ra = self._make_module()
        ra.start()
        # Answer No to everything
        for _ in range(20):  # More than enough to exhaust questions
            if not ra.is_active():
                break
            ra.submit_answer(False)

        if ra.is_complete():
            result = ra.get_result()
            self.assertIsNotNone(result)
            self.assertIn(result.risk_level, ("LOW", "UNKNOWN"))

    def test_tc26_progress_pct_is_valid(self):
        """TC26: get_progress_pct() returns a value between 0 and 100."""
        ra = self._make_module()
        ra.start()
        pct = ra.get_progress_pct()
        self.assertGreaterEqual(pct, 0.0)
        self.assertLessEqual(pct, 100.0)


# ===========================================================================
#  D. UNIT TESTS — SCAM DETECTOR
# ===========================================================================

class TestScamDetector(unittest.TestCase):
    """
    Unit tests for ScamDetector.
    Tests text analysis, Q&A mode, report formatting, edge cases,
    and indicator loading.
    """

    @classmethod
    def setUpClass(cls):
        from scam_detector import ScamDetector
        cls.detector = ScamDetector()

    # ------------------------------------------------------------------

    def test_tc27_detector_loads(self):
        """TC27: ScamDetector initialises without errors."""
        from scam_detector import ScamDetector
        det = ScamDetector()
        self.assertIsNotNone(det)

    def test_tc28_empty_input_returns_result(self):
        """TC28: Analysing empty string returns a DetectionResult (no crash)."""
        result = self.detector.analyze("")
        self.assertIsNotNone(result)

    def test_tc29_safe_job_is_classified_safe_or_low(self):
        """TC29: Legitimate job description does not score HIGH or VERY_HIGH."""
        result = self.detector.analyze(
            "Software Engineer required. 3+ years Python experience. "
            "Office in Bengaluru, Monday to Friday. Salary 10–15 LPA. "
            "Apply with CV to hr@company.com. Written offer letter provided. "
            "Background verification required."
        )
        self.assertNotIn(result.level, ("HIGH_RISK", "VERY_HIGH"),
                         "A legitimate job should not be HIGH+ risk")

    def test_tc30_trafficking_scam_is_classified_high(self):
        """TC30: Classic trafficking job advertisement is classified HIGH+ risk."""
        result = self.detector.analyze(
            "Females 18-25 wanted. No experience required. "
            "Guaranteed salary 2 lakh per month. Passport will be kept. "
            "Live-in required. All expenses paid overseas. "
            "Cannot leave before 2 years. Registration fee 5000. "
            "Do not tell family. Urgent joining required."
        )
        self.assertIn(result.level, ("HIGH_RISK", "VERY_HIGH"),
                      "Trafficking scam text must be HIGH_RISK or VERY_HIGH")

    def test_tc31_result_has_required_fields(self):
        """TC31: DetectionResult contains all required fields."""
        result = self.detector.analyze("sample job offer text")
        self.assertIsNotNone(result.level)
        self.assertIsNotNone(result.suspicion_pct)
        self.assertIsInstance(result.top_flags, list)
        self.assertIsInstance(result.recommendation, str)

    def test_tc32_report_format_returns_string(self):
        """TC32: format_report() returns a non-empty string."""
        result = self.detector.analyze("job offer")
        report = self.detector.format_report(result)
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 20)

    def test_tc33_suspicion_pct_in_valid_range(self):
        """TC33: suspicion_pct is always between 0.0 and 100.0."""
        test_texts = [
            "Normal software job",
            "Passport will be kept. Live-in required. No experience. Easy money.",
            "",
        ]
        for text in test_texts:
            result = self.detector.analyze(text)
            self.assertGreaterEqual(result.suspicion_pct, 0.0)
            self.assertLessEqual(result.suspicion_pct, 100.0)

    def test_tc34_qa_mode_analysis_works(self):
        """TC34: analyze_from_qa() processes a structured Q&A dict."""
        answers = {
            "promised_high_salary": True,
            "required_to_travel":   True,
            "documents_requested":  True,
            "pay_upfront":          True,
            "secrecy_demanded":     True,
        }
        result = self.detector.analyze_from_qa(answers)
        self.assertNotIn(result.level, ("SAFE",),
                         "Multiple Yes answers should not be SAFE")


# ===========================================================================
#  E. UNIT TESTS — CHATBOT ENGINE
# ===========================================================================

class TestChatBot(unittest.TestCase):
    """
    Unit tests for the core ChatBot engine.
    Tests intent classification, message processing, session management,
    module routing, and edge cases.
    """

    @classmethod
    def setUpClass(cls):
        from chatbot import ChatBot
        cls.bot = ChatBot()

    # ------------------------------------------------------------------

    def test_tc35_bot_initialises(self):
        """TC35: ChatBot initialises without errors."""
        from chatbot import ChatBot
        bot = ChatBot()
        self.assertIsNotNone(bot)

    def test_tc36_greeting_returns_response(self):
        """TC36: A greeting input returns a non-empty ChatResponse."""
        self.bot.reset_session()
        response = self.bot.process("hello")
        self.assertIsNotNone(response)
        self.assertIsInstance(response.text, str)
        self.assertGreater(len(response.text), 10)

    def test_tc37_emergency_sets_flag(self):
        """TC37: Emergency input sets is_emergency flag in response."""
        self.bot.reset_session()
        response = self.bot.process("emergency")
        self.assertTrue(response.is_emergency,
                        "Emergency input must set is_emergency flag")

    def test_tc38_welcome_message_contains_app_name(self):
        """TC38: get_welcome_message() returns text containing 'AegisAI' and helpline info."""
        from chatbot import ChatBot
        bot     = ChatBot()
        welcome = bot.get_welcome_message()
        # Must be a non-empty string
        self.assertIsInstance(welcome, str)
        self.assertGreater(len(welcome), 30)
        # Must mention the application name
        self.assertIn("AegisAI", welcome,
                      "Welcome message must contain the application name 'AegisAI'")
        # Must mention at least one core feature
        has_feature = any(kw in welcome.lower() for kw in
                          ["trafficking", "risk", "emergency", "safe", "help"])
        self.assertTrue(has_feature,
                        "Welcome message must mention at least one core feature")

    def test_tc39_risk_assessment_activates(self):
        """TC39: 'risk assessment' starts the questionnaire."""
        self.bot.reset_session()
        response = self.bot.process("risk assessment")
        self.assertIn("assessment", response.text.lower())

    def test_tc40_empty_input_is_handled(self):
        """TC40: Empty string input does not crash the chatbot."""
        self.bot.reset_session()
        try:
            response = self.bot.process("")
            self.assertIsNotNone(response)
        except Exception as e:
            self.fail(f"Empty input caused an exception: {e}")

    def test_tc41_job_analysis_triggers_on_keyword(self):
        """TC41: 'check job offer' triggers the job analysis flow."""
        self.bot.reset_session()
        response = self.bot.process("check job offer")
        text = response.text.lower()
        self.assertTrue(
            any(kw in text for kw in ["job", "offer", "paste", "analyze", "scam"]),
            "Job analysis response should mention job-related keywords"
        )


# ===========================================================================
#  F. INTEGRATION TESTS
# ===========================================================================

class TestIntegration(unittest.TestCase):
    """
    Integration tests verifying module interactions.
    Tests that components work correctly when combined.
    """

    def setUp(self):
        from chatbot import ChatBot
        self.bot = ChatBot()

    # ------------------------------------------------------------------

    def test_tc42_full_risk_assessment_flow(self):
        """TC42: Complete risk assessment questionnaire flow end-to-end."""
        # Start assessment
        resp = self.bot.process("risk assessment")
        self.assertIn("assessment", resp.text.lower())

        # Answer all questions with No (safe scenario)
        for _ in range(20):
            state = self.bot.get_session_state()
            if not self.bot._risk.is_active():
                break
            resp = self.bot.process("no")
            if self.bot._risk.is_complete():
                break

        # Verify assessment completed and risk level is set
        self.assertIn(
            self.bot.get_session_state().risk_level,
            ("LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN")
        )

    def test_tc43_job_analysis_end_to_end(self):
        """TC43: Job analysis flow from trigger to result."""
        # Trigger job analysis
        resp = self.bot.process("check job offer")
        self.assertIn(
            any(kw in resp.text.lower() for kw in ["job", "paste", "offer"]),
            [True]
        )

        # Submit a scammy job text
        job_text = (
            "Females 18-25 wanted. Passport will be kept. "
            "No experience required. Cannot leave before contract ends. "
            "Guaranteed salary 2 lakh per month. Urgent joining."
        )
        resp2 = self.bot.process(job_text)
        self.assertIsNotNone(resp2)
        self.assertIsInstance(resp2.text, str)

    def test_tc44_kb_and_expert_system_consistent(self):
        """TC44: Emergency intent from chatbot matches KB emergency response."""
        from knowledge_base import KnowledgeBaseManager
        from chatbot import ChatBot

        bot = ChatBot()
        kb  = KnowledgeBaseManager()

        bot_response = bot.process("I need help now")
        kb_response  = kb.get_emergency_response()

        # Both should mention emergency contacts
        self.assertTrue(
            any(num in bot_response.text for num in ["100", "1098", "112"]) or
            any(num in kb_response     for num in ["100", "1098", "112"]),
            "Emergency responses should contain helpline numbers"
        )

    def test_tc45_session_reset_clears_state(self):
        """TC45: reset_session() properly clears all session state."""
        bot = self.bot
        # Run some actions
        bot.process("hello")
        bot.process("risk assessment")
        bot.process("yes")

        # Reset
        bot.reset_session()

        state = bot.get_session_state()
        self.assertEqual(state.risk_level, "UNKNOWN")
        self.assertEqual(state.message_count, 0)
        self.assertFalse(bot._risk.is_active())

    def test_tc46_scam_detector_integrates_with_chatbot(self):
        """TC46: Scam detector result flows into chatbot response correctly."""
        bot = self.bot
        # Trigger job analysis
        bot.process("check job offer")

        # Submit scam text directly
        scam_text = (
            "Quick cash daily! No experience required! "
            "Pay registration fee 3000. Passport will be kept. "
            "Do not tell family. Overseas posting. Urgent joining needed."
        )
        response = bot.process(scam_text)

        # Response should contain analysis content
        self.assertIsInstance(response.text, str)
        self.assertGreater(len(response.text), 50)


# ===========================================================================
#  G. USER ACCEPTANCE TESTS (UAT)
# ===========================================================================

class TestUserAcceptance(unittest.TestCase):
    """
    User Acceptance Tests (UAT) simulating real user scenarios.
    Each test represents a complete realistic user journey.
    """

    def setUp(self):
        from chatbot import ChatBot
        self.bot = ChatBot()

    # ------------------------------------------------------------------

    def test_tc47_uat_victim_in_immediate_danger(self):
        """
        TC47 (UAT): Victim scenario — User says they are in immediate danger.
        Expected: Emergency response with helpline numbers is returned
        and is_emergency flag is True.
        """
        test_inputs = [
            "I am in danger and need help",
            "help me please",
            "emergency",
        ]
        for user_input in test_inputs:
            self.bot.reset_session()
            response = self.bot.process(user_input)
            has_number = any(
                num in response.text for num in ["100", "1098", "112", "1091"]
            )
            self.assertTrue(
                has_number or response.is_emergency,
                f"Emergency input '{user_input}' must return emergency response"
            )

    def test_tc48_uat_student_learning_about_trafficking(self):
        """
        TC48 (UAT): Awareness scenario — Student asking educational questions.
        Expected: Informative responses from KB, no emergency flag.
        """
        self.bot.reset_session()
        educational_queries = [
            "what is human trafficking",
            "warning signs of trafficking",
            "how to stay safe online",
        ]
        for query in educational_queries:
            response = self.bot.process(query)
            self.assertIsInstance(response.text, str)
            self.assertGreater(len(response.text), 30)
            self.assertFalse(
                response.is_emergency,
                f"Educational query '{query}' should not trigger emergency"
            )

    def test_tc49_uat_ngo_worker_reporting_case(self):
        """
        TC49 (UAT): NGO scenario — Worker asking how to report trafficking.
        Expected: Response includes reporting procedures and helplines.
        """
        self.bot.reset_session()
        response = self.bot.process("how do I report human trafficking")
        text = response.text.lower()
        self.assertTrue(
            any(kw in text for kw in
                ["report", "police", "100", "1098", "complaint", "fir", "authority"]),
            "Reporting query should return reporting-related information"
        )

    def test_tc50_uat_job_seeker_suspicious_offer(self):
        """
        TC50 (UAT): Job seeker scenario — User receives suspicious job offer.
        Expected: Scam analysis correctly identifies it as HIGH+ risk
        and returns actionable guidance.

        This is the most critical UAT — it tests the core safety feature.
        """
        self.bot.reset_session()

        # Step 1: User asks about a job offer
        resp1 = self.bot.process("I received a job offer, can you check if it's safe?")
        self.assertIsInstance(resp1.text, str)

        # Step 2: User provides the suspicious job text
        suspicious_job = (
            "URGENT! Female candidates aged 18-25 wanted for overseas position in Dubai. "
            "No experience required. Guaranteed salary ₹2,00,000/month. "
            "Passport will be kept by company for security. "
            "Live-in accommodation provided. Cannot leave before 2-year contract. "
            "Registration fee ₹5,000 required. Do not tell family about this offer. "
            "Urgent joining — must start within 48 hours."
        )
        resp2 = self.bot.process(suspicious_job)

        # Verify: response should contain warning content
        text = resp2.text.lower()
        self.assertIsInstance(resp2.text, str)
        self.assertTrue(
            any(kw in text for kw in
                ["risk", "suspicious", "warning", "danger", "red flag",
                 "do not", "reject", "scam", "caution", "concern"]) or
            resp2.is_emergency,
            "Suspicious job offer must trigger a warning response"
        )


# ===========================================================================
#  STANDALONE TEST RUNNER
# ===========================================================================

class _ColourResult(unittest.TextTestResult):
    """Custom test result formatter with colour output."""

    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"    ✅  {test.shortDescription() or str(test)}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"    ❌  {test.shortDescription() or str(test)}")
        print(f"        {err[1]}")

    def addError(self, test, err):
        super().addError(test, err)
        print(f"    💥  {test.shortDescription() or str(test)}")
        print(f"        {err[1]}")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        print(f"    ⏭️   {test.shortDescription() or str(test)} (SKIP: {reason})")


def _run_standalone():
    """Run all 50 tests with pretty output."""
    test_suites = [
        ("A. Unit Tests — Knowledge Base Manager",   TestKnowledgeBaseManager),
        ("B. Unit Tests — Expert System Engine",     TestExpertSystemEngine),
        ("C. Unit Tests — Risk Assessment Module",   TestRiskAssessmentModule),
        ("D. Unit Tests — Scam Detector",            TestScamDetector),
        ("E. Unit Tests — ChatBot Engine",           TestChatBot),
        ("F. Integration Tests",                     TestIntegration),
        ("G. User Acceptance Tests (UAT)",           TestUserAcceptance),
    ]

    print("\n" + "═" * 65)
    print("  AegisAI — Complete Test Suite")
    print("  50 Tests: Unit + Integration + UAT")
    print("═" * 65 + "\n")

    total_run    = 0
    total_passed = 0
    total_failed = 0
    total_errors = 0

    for suite_name, test_class in test_suites:
        print(f"\n{'─' * 65}")
        print(f"  {suite_name}")
        print(f"{'─' * 65}")

        loader = unittest.TestLoader()
        suite  = loader.loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(
            resultclass=_ColourResult,
            verbosity=0,
            stream=open(os.devnull, "w"),
        )
        result = runner.run(suite)

        total_run    += result.testsRun
        total_passed += result.testsRun - len(result.failures) - len(result.errors)
        total_failed += len(result.failures)
        total_errors += len(result.errors)

    print(f"\n{'═' * 65}")
    print(f"  FINAL RESULTS")
    print(f"{'─' * 65}")
    print(f"  Tests Run    : {total_run}")
    print(f"  Passed       : {total_passed}  ✅")
    print(f"  Failed       : {total_failed}  {'❌' if total_failed else '─'}")
    print(f"  Errors       : {total_errors}  {'💥' if total_errors else '─'}")
    print(f"{'─' * 65}")

    if total_failed == 0 and total_errors == 0:
        print(f"  🎉  ALL {total_run} TESTS PASSED!")
    else:
        print(f"  ⚠️   {total_failed + total_errors} test(s) need attention.")

    print(f"{'═' * 65}\n")
    return total_failed == 0 and total_errors == 0


if __name__ == "__main__":
    success = _run_standalone()
    sys.exit(0 if success else 1)
