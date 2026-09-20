"""
What Are AI Agents? — From Chatbots to Goal-Driven Systems
Part of: AI Agents with Python 2026

This example introduces the key difference between a chatbot and a true
agent-driven system: a chatbot answers a prompt, while an agent works toward a
clear goal using a plan, tools, and feedback.
"""

from __future__ import annotations


class Chatbot:
    """A simple rule-based chatbot that responds to a prompt."""

    def respond(self, prompt: str) -> str:
        prompt_lower = prompt.lower()

        if "ai agent" in prompt_lower:
            return (
                "An AI agent is a goal-driven system that can observe context, "
                "decide on actions, and use tools to complete a task. A chatbot "
                "mostly responds to a prompt."
            )

        return (
            "I can explain the difference between a chatbot and an AI agent. "
            "A chatbot responds to a question, while an AI agent works toward a goal."
        )


class SimpleAgent:
    """A minimal goal-driven agent inspired by the Part 1 article."""

    def run(self, goal: str) -> dict:
        plan = [
            "Understand the task and identify the information needed.",
            "Gather relevant facts from approved sources or knowledge.",
            "Organize the findings into a clear summary or recommendation.",
            "Deliver the final answer with the key conclusions and next steps.",
        ]

        summary = (
            f"Goal: {goal}. This is a goal-driven agent because it follows a plan, "
            "collects information, and produces a structured output rather than only "
            "answering a single prompt. The project focuses on the impact of AI on "
            "education in Ghana, so the agent would evaluate research findings, "
            "organize relevant themes, and explain the practical benefits and risks."
        )

        return {
            "goal": goal,
            "plan": plan,
            "summary": summary,
        }


def main():
    print("Part 1: What Are AI Agents? — From Chatbots to Goal-Driven Systems")
    print("\nChatbot example:")
    chatbot = Chatbot()
    print(chatbot.respond("What is an AI agent?"))

    print("\nGoal-driven agent example:")
    agent = SimpleAgent()
    result = agent.run("Research the impact of AI on education in Ghana")
    print(f"Goal: {result['goal']}")
    print("Plan:")
    for index, step in enumerate(result["plan"], start=1):
        print(f"  {index}. {step}")
    print(f"\nSummary: {result['summary']}")


if __name__ == "__main__":
    main()
