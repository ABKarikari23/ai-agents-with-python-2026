"""User-scoped persistent memory backed by SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "agent_memory.db"
MAX_MEMORY_LENGTH = 300


def initialize_memory() -> None:
    """Create the memory database and table when needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_memory(user_id: str, content: str) -> None:
    """Persist one explicitly selected memory for a user."""
    if not isinstance(user_id, str) or not user_id.strip():
        raise ValueError("User ID cannot be empty.")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Memory content cannot be empty.")
    if len(content) > MAX_MEMORY_LENGTH:
        raise ValueError(f"Memory content cannot exceed {MAX_MEMORY_LENGTH} characters.")

    initialize_memory()
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            "INSERT INTO memories (user_id, content) VALUES (?, ?)",
            (user_id, content.strip()),
        )


def get_memories(user_id: str, limit: int = 20) -> list[str]:
    """Return the most recent memories belonging only to the requested user."""
    if not isinstance(user_id, str) or not user_id.strip():
        raise ValueError("User ID cannot be empty.")
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("Memory limit must be a positive integer.")

    initialize_memory()
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute(
            """
            SELECT content FROM memories
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
    return [str(row[0]) for row in reversed(rows)]
