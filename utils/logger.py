"""AegisAI — Logging Setup"""
import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logger with a clean, coloured format."""
    fmt = "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s"
    logging.basicConfig(
        level=level,
        format=fmt,
        datefmt="%H:%M:%S",
        stream=sys.stdout,
        encoding="utf-8",
        errors="replace",
    )
    # Quieten noisy third-party loggers
    for noisy in ("PIL", "customtkinter", "darkdetect"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
