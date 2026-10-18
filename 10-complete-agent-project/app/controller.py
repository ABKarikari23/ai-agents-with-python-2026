"""Task state shared by the agent controller and its integrations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    task_id: str
    user_id: str
    request: str
    step_count: int = 0
    tool_call_count: int = 0
    completed: bool = False
    needs_human: bool = False
    observations: list[str] = field(default_factory=list)
    result: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
