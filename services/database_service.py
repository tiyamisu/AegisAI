"""
AegisAI — Database Service
============================
Handles thread-safe persistence using SQLite.
Stores session statistics, chat histories, facts, and scam logs.
"""
from __future__ import annotations

import json
import os
import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Optional
from models.message import ChatMessage, MessageRole

log = logging.getLogger(__name__)

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "aegis_ai.db")


class DatabaseService:
    """
    Manages SQLite database transactions.
    Creates connection per request to ensure thread safety across GUI & background tasks.
    """

    def __init__(self) -> None:
        self.db_path = DB_PATH
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Create and return a new SQLite database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self) -> None:
        """Create tables if they do not exist."""
        os.makedirs(DB_DIR, exist_ok=True)
        log.info("Initializing database at: %s", self.db_path)

        with self._get_connection() as conn:
            # 1. Sessions table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    risk_level TEXT DEFAULT 'UNKNOWN',
                    risk_score INTEGER DEFAULT 0,
                    is_emergency INTEGER DEFAULT 0
                );
            """)

            # 2. Chat history table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT CHECK(role IN ('user', 'bot')),
                    text TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_emergency INTEGER DEFAULT 0,
                    suggestions TEXT, -- JSON array
                    intent TEXT DEFAULT '',
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
                );
            """)

            # 3. Assessment answers table (Facts)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS assessment_answers (
                    session_id TEXT,
                    question_id TEXT,
                    answer INTEGER CHECK(answer IN (0, 1)),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY(session_id, question_id),
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
                );
            """)

            # 4. Scam scanner logs table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scam_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    job_text TEXT NOT NULL,
                    suspicion_pct REAL NOT NULL,
                    risk_level TEXT NOT NULL,
                    red_flags TEXT, -- JSON array
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
                );
            """)
            conn.commit()
        log.info("Database tables initialized successfully.")

    # ------------------------------------------------------------------
    # Session Persistence Operations
    # ------------------------------------------------------------------

    def create_session(self, session_id: str) -> None:
        """Create a new session entry if it does not exist."""
        try:
            with self._get_connection() as conn:
                conn.execute(
                    "INSERT OR IGNORE INTO sessions (session_id) VALUES (?);",
                    (session_id,)
                )
                conn.commit()
        except sqlite3.Error as exc:
            log.error("Failed to create session in database: %s", exc)

    def update_session_risk(self, session_id: str, risk_level: str, risk_score: int, is_emergency: bool) -> None:
        """Update the risk parameters of an active session."""
        try:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    UPDATE sessions
                    SET risk_level = ?, risk_score = ?, is_emergency = ?
                    WHERE session_id = ?;
                    """,
                    (risk_level, risk_score, 1 if is_emergency else 0, session_id)
                )
                conn.commit()
        except sqlite3.Error as exc:
            log.error("Failed to update session risk in database: %s", exc)

    def get_session(self, session_id: str) -> Optional[dict]:
        """Fetch details of a single session."""
        try:
            with self._get_connection() as conn:
                cur = conn.execute("SELECT * FROM sessions WHERE session_id = ?;", (session_id,))
                row = cur.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as exc:
            log.error("Failed to fetch session from database: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Message History Operations
    # ------------------------------------------------------------------

    def save_message(self, session_id: str, role: str, text: str,
                     is_emergency: bool = False, suggestions: List[str] | None = None,
                     intent: str = "") -> None:
        """Save a new chat message to the history."""
        self.create_session(session_id)
        sugg_str = json.dumps(suggestions or [])
        try:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO messages (session_id, role, text, is_emergency, suggestions, intent)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """,
                    (session_id, role, text, 1 if is_emergency else 0, sugg_str, intent)
                )
                conn.commit()
        except sqlite3.Error as exc:
            log.error("Failed to save message to database: %s", exc)

    def get_messages(self, session_id: str) -> List[ChatMessage]:
        """Load chat history for a session."""
        messages: List[ChatMessage] = []
        try:
            with self._get_connection() as conn:
                cur = conn.execute(
                    "SELECT role, text, timestamp, is_emergency, suggestions, intent FROM messages WHERE session_id = ? ORDER BY timestamp ASC;",
                    (session_id,)
                )
                for row in cur.fetchall():
                    # Parse timestamp format (SQLite returns string usually)
                    try:
                        ts = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                    except Exception:
                        ts = datetime.now()

                    suggestions = []
                    if row["suggestions"]:
                        try:
                            suggestions = json.loads(row["suggestions"])
                        except Exception:
                            pass

                    role = MessageRole.USER if row["role"] == "user" else MessageRole.BOT
                    msg = ChatMessage(
                        role=role,
                        text=row["text"],
                        timestamp=ts,
                        is_emergency=bool(row["is_emergency"]),
                        suggestions=suggestions,
                        intent=row["intent"] or "",
                    )
                    messages.append(msg)
        except sqlite3.Error as exc:
            log.error("Failed to load messages from database: %s", exc)
        return messages

    # ------------------------------------------------------------------
    # Assessment Facts Operations
    # ------------------------------------------------------------------

    def save_assessment_answer(self, session_id: str, question_id: str, answer: bool) -> None:
        """Save a user's answer to a risk assessment question."""
        self.create_session(session_id)
        try:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO assessment_answers (session_id, question_id, answer)
                    VALUES (?, ?, ?);
                    """,
                    (session_id, question_id, 1 if answer else 0)
                )
                conn.commit()
        except sqlite3.Error as exc:
            log.error("Failed to save assessment answer: %s", exc)

    def get_assessment_answers(self, session_id: str) -> Dict[str, bool]:
        """Retrieve all answered questions and their boolean values."""
        answers = {}
        try:
            with self._get_connection() as conn:
                cur = conn.execute(
                    "SELECT question_id, answer FROM assessment_answers WHERE session_id = ?;",
                    (session_id,)
                )
                for row in cur.fetchall():
                    answers[row["question_id"]] = bool(row["answer"])
        except sqlite3.Error as exc:
            log.error("Failed to load assessment answers: %s", exc)
        return answers

    def clear_assessment_answers(self, session_id: str) -> None:
        """Clear all risk assessment answers for the session."""
        try:
            with self._get_connection() as conn:
                conn.execute("DELETE FROM assessment_answers WHERE session_id = ?;", (session_id,))
                conn.commit()
        except sqlite3.Error as exc:
            log.error("Failed to clear assessment answers: %s", exc)

    # ------------------------------------------------------------------
    # Scam Logs Operations
    # ------------------------------------------------------------------

    def save_scam_log(self, session_id: str, job_text: str, suspicion_pct: float,
                      risk_level: str, red_flags: List[str]) -> None:
        """Log a job offer text scan result."""
        self.create_session(session_id)
        flags_str = json.dumps(red_flags)
        try:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO scam_logs (session_id, job_text, suspicion_pct, risk_level, red_flags)
                    VALUES (?, ?, ?, ?, ?);
                    """,
                    (session_id, job_text, suspicion_pct, risk_level, flags_str)
                )
                conn.commit()
        except sqlite3.Error as exc:
            log.error("Failed to save scam log: %s", exc)

    def get_scam_logs(self, session_id: str) -> List[dict]:
        """Fetch all scam analyzer scans recorded for this session."""
        logs = []
        try:
            with self._get_connection() as conn:
                cur = conn.execute(
                    "SELECT * FROM scam_logs WHERE session_id = ? ORDER BY timestamp DESC;",
                    (session_id,)
                )
                for row in cur.fetchall():
                    r = dict(row)
                    try:
                        r["red_flags"] = json.loads(row["red_flags"])
                    except Exception:
                        r["red_flags"] = []
                    logs.append(r)
        except sqlite3.Error as exc:
            log.error("Failed to load scam logs: %s", exc)
        return logs

    def delete_session(self, session_id: str) -> None:
        """Delete all database logs associated with a session (due to cascade delete)."""
        try:
            with self._get_connection() as conn:
                conn.execute("DELETE FROM sessions WHERE session_id = ?;", (session_id,))
                conn.commit()
        except sqlite3.Error as exc:
            log.error("Failed to delete session: %s", exc)
