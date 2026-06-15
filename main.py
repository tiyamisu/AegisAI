"""
AegisAI — Application Entry Point
=====================================
Usage:
    python main.py          Launch the GUI (default)
    python main.py --test   Run backend self-tests
"""
import argparse
import logging
import sys
import os

# Ensure project root is on path
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from utils.logger import setup_logging


def run_gui() -> None:
    """Launch the AegisAI CustomTkinter GUI application."""
    from ui.app_window import AegisAIApp
    app = AegisAIApp()
    app.run()


def run_tests() -> None:
    """Run the test suite (unittest)."""
    import unittest
    from tests.test_suite import (
        TestKnowledgeBaseManager, TestExpertSystemEngine,
        TestRiskAssessmentModule, TestScamDetector,
        TestChatBot, TestIntegration, TestUserAcceptance,
    )
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()
    for cls in [
        TestKnowledgeBaseManager, TestExpertSystemEngine,
        TestRiskAssessmentModule, TestScamDetector,
        TestChatBot, TestIntegration, TestUserAcceptance,
    ]:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AegisAI — Anti-Trafficking AI Platform"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the automated test suite and exit",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable DEBUG-level logging",
    )
    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(log_level)

    log = logging.getLogger("main")
    log.info("AegisAI starting… (Python %s)", sys.version.split()[0])

    if args.test:
        run_tests()
    else:
        run_gui()


if __name__ == "__main__":
    main()
