"""Reviewer agent for the Part 7 multi-agent workflow."""

from __future__ import annotations

from agents.base import BaseAgent
from state import AgentState


class ReviewerAgent(BaseAgent):
    """Checks the draft for completeness and quality issues."""

    def run(self, state: AgentState) -> AgentState:
        if not state.draft:
            state.errors.append("Reviewer requires a draft before review.")
            state.status = "failed"
            return state

        issues = []
        if len(state.draft) < 50:
            issues.append("Draft appears too short.")
        if "key findings" not in state.draft.lower():
            issues.append("Draft lacks a clear findings section.")

        if issues:
            state.review = {
                "approved": False,
                "issues": issues,
                "message": "The draft requires revision before approval.",
            }
            state.status = "needs_revision"
        else:
            state.review = {
                "approved": True,
                "issues": [],
                "message": "The draft meets the expected quality checks.",
            }
            state.status = "review_complete"

        return state
