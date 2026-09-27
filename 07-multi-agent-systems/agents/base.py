"""Base classes for the multi-agent workflow."""

from __future__ import annotations

from abc import ABC, abstractmethod

from state import AgentState


class BaseAgent(ABC):
    """All agents in the workflow must implement a run method."""

    @abstractmethod
    def run(self, state: AgentState) -> AgentState:
        """Process the current task state and return the updated state."""
        raise NotImplementedError
