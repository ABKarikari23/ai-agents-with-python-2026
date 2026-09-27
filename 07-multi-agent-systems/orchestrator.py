"""Orchestrator for the Part 7 example."""

from __future__ import annotations

from agents.researcher import ResearchAgent
from agents.reviewer import ReviewerAgent
from agents.writer import WriterAgent
from state import AgentState


class Orchestrator:
    """Runs a simple sequential multi-agent workflow."""

    def __init__(self):
        self.researcher = ResearchAgent()
        self.writer = WriterAgent()
        self.reviewer = ReviewerAgent()

    def run(self, task: str) -> AgentState:
        state = AgentState(task=task)

        state = self.researcher.run(state)
        if state.errors:
            state.status = "failed"
            return state

        state = self.writer.run(state)
        if state.errors:
            state.status = "failed"
            return state

        state = self.reviewer.run(state)
        if state.errors:
            state.status = "failed"
            return state

        if state.review and state.review.get("approved"):
            state.status = "completed"
        else:
            state.status = "needs_revision"

        return state
