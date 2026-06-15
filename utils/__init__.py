"""AegisAI — Utils Package."""
from .logger import setup_logging
from .threading_utils import run_in_thread

__all__ = ["setup_logging", "run_in_thread"]
