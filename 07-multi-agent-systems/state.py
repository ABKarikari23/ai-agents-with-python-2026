"""Shared workflow state for the multi-agent demo."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    """Tracks the task, outputs, and review status across agents."""

    task: str
    research: dict[str, Any] | None = None
    draft: str | None = None
    review: dict[str, Any] | None = None
    errors: list[str] = field(default_factory=list)
    status: str = "pending"

    def is_successful(self) -> bool:
        return not self.errors and self.status in {"review_complete", "completed"}
