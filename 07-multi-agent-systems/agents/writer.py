"""Writer agent for the Part 7 multi-agent workflow."""

from __future__ import annotations

from agents.base import BaseAgent
from state import AgentState


class WriterAgent(BaseAgent):
    """Turns research output into a draft answer."""

    def run(self, state: AgentState) -> AgentState:
        if not state.research:
            state.errors.append("Writer requires research before drafting.")
            state.status = "failed"
            return state

        summary = state.research.get("summary", "")
        key_points = state.research.get("key_points", [])
        key_points_text = "\n".join(f"- {point}" for point in key_points)

        state.draft = (
            f"Draft for: {state.task}\n\n"
            f"{summary}\n\n"
            "Key findings:\n"
            f"{key_points_text}\n\n"
            "This draft is structured to explain the goal, summarize the evidence, "
            "and present a clear final recommendation."
        )
        state.status = "draft_complete"
        return state
