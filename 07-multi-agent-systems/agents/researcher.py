"""Research agent for the Part 7 multi-agent workflow."""

from __future__ import annotations

from agents.base import BaseAgent
from state import AgentState


class ResearchAgent(BaseAgent):
    """Collects the required reasoning context for a task."""

    def run(self, state: AgentState) -> AgentState:
        task = (state.task or "").strip()

        if not task:
            state.errors.append("Research requires a task description.")
            state.status = "failed"
            return state

        state.research = {
            "task": task,
            "summary": (
                f"Research completed for '{task}'. The task is clear, relevant sources "
                "have been identified, and the next step is to organize the findings "
                "into a draft response."
            ),
            "key_points": [
                "Define the objective clearly.",
                "Gather facts from trusted sources.",
                "Organize the findings into a usable structure.",
                "Prepare a final recommendation or answer.",
            ],
            "confidence": 0.92,
        }
        state.status = "research_complete"
        return state
