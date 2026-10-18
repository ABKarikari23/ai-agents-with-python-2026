"""Small, local lexical search over approved troubleshooting documents."""

from __future__ import annotations

import re
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "data" / "knowledge"


def tokenize(text: str) -> set[str]:
    """Return normalized alphanumeric terms from text."""
    return set(re.findall(r"\b[a-zA-Z0-9]+\b", text.lower()))


def load_documents() -> list[dict[str, str]]:
    """Load local text documents; an absent directory is an empty knowledge base."""
    if not KNOWLEDGE_DIR.exists():
        return []

    documents = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.txt")):
        documents.append(
            {
                "source": path.name,
                "content": path.read_text(encoding="utf-8"),
            }
        )
    return documents


def search_knowledge(query: str, limit: int = 3) -> list[dict[str, str | int]]:
    """Rank documents by simple query-term overlap."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Knowledge search query cannot be empty.")
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("Search limit must be a positive integer.")

    query_terms = tokenize(query)
    matches = []
    for document in load_documents():
        score = len(query_terms & tokenize(document["content"]))
        if score:
            matches.append({**document, "score": score})

    return sorted(
        matches,
        key=lambda item: (-int(item["score"]), str(item["source"])),
    )[:limit]
