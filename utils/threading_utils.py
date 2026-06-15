"""AegisAI — Threading Utilities"""
import threading
import logging
from typing import Callable, Any

log = logging.getLogger(__name__)


def run_in_thread(
    target: Callable[[], Any],
    on_done: Callable[[Any], None] | None = None,
    on_error: Callable[[Exception], None] | None = None,
    daemon: bool = True,
) -> threading.Thread:
    """
    Run *target* in a background daemon thread.

    Parameters
    ----------
    target   : Callable that does the background work; its return value
               is passed to on_done.
    on_done  : Callback(result) scheduled on the calling thread when done.
               **Must** be scheduled via root.after() by the caller if UI
               updates are needed.
    on_error : Callback(exc) if target raises an exception.
    daemon   : Whether the thread is a daemon (default True).

    Returns
    -------
    The started Thread object.
    """
    def _run():
        try:
            result = target()
            if on_done:
                on_done(result)
        except Exception as exc:
            log.error("Background thread error: %s", exc)
            if on_error:
                on_error(exc)

    t = threading.Thread(target=_run, daemon=daemon)
    t.start()
    return t
