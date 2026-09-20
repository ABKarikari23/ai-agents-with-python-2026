"""
How AI Agents Work — Models, Tools, State, Memory and Agent Loops
Part of: AI Agents with Python 2026

This example demonstrates the agent architecture described in the article:
- a goal
- a model-like decision step
- a tool call
- observation of results
- memory/state tracking
- a final response
"""

from __future__ import annotations


class Memory:
    """Stores short-term user context and preferences."""

    def __init__(self):
        self._data = {}

    def add(self, key: str, value: str) -> None:
        self._data[key] = value

    def get(self, key: str):
        return self._data.get(key)

    def items(self):
        return self._data.items()


class ResearchTool:
    """A simple tool that returns relevant information for a research question."""

    def run(self, query: str) -> str:
        query_lower = query.lower()

        if "solar" in query_lower and "ghana" in query_lower:
            return (
                "Solar energy can reduce electricity costs for businesses, improve "
                "energy resilience, and support cleaner operations. In Ghana, solar "
                "systems are increasingly relevant for stable power supply and lower "
                "operating expenses."
            )

        if "ai" in query_lower and "education" in query_lower:
            return (
                "AI can personalize learning, support academic research, and help "
                "students practice skills more efficiently."
            )

        return "Relevant research findings were collected from an approved knowledge source."


class SimpleAgent:
    """A minimal goal-driven agent demonstrating planning, tool use, memory, and result handling."""

    def __init__(self):
        self.memory = Memory()
        self.tool = ResearchTool()

    def decide(self, goal: str) -> dict:
        if "solar" in goal.lower() or "research" in goal.lower():
            return {
                "tool": "research",
                "arguments": {"query": goal},
                "note": "Tool selected: research. Need a grounded fact set to answer the user's question."
            }

        return {
            "tool": "none",
            "arguments": {},
            "note": "Tool selected: none. No external tool required for this request."
        }

    def run(self, goal: str) -> dict:
        self.memory.add("last_goal", goal)

        decision = self.decide(goal)
        if decision["tool"] == "research":
            observation = self.tool.run(decision["arguments"]["query"])
        else:
            observation = "No tool result needed."

        final_response = (
            f"Summary for: {goal}. The agent used a planned tool call to gather "
            f"relevant information and then reasoned about the findings. Observation: "
            f"{observation}"
        )

        return {
            "goal": goal,
            "decision": decision["note"],
            "observation": observation,
            "final_response": final_response,
        }


def main():
    print("Part 2: How AI Agents Work — Models, Tools, State, Memory and Agent Loops")

    memory = Memory()
    memory.add("preferred_language", "Python")
    memory.add("budget", "GHS 5000")

    agent = SimpleAgent()
    result = agent.run("Research the benefits of solar energy for small businesses in Ghana")

    print("\nMemory state:")
    for key, value in memory.items():
        print(f"  - {key}: {value}")

    print("\nAgent workflow:")
    print(f"Goal: {result['goal']}")
    print(f"Decision: {result['decision']}")
    print(f"Observation: {result['observation']}")
    print(f"Final response: {result['final_response']}")


if __name__ == "__main__":
    main()
