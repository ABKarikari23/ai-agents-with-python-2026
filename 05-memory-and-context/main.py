"""
Adding Memory and Context to AI Agents
Part of: AI Agents with Python 2026

This example demonstrates the core memory ideas from the article:
- short-term context and conversation history
- long-term preferences stored in memory
- a simple agent that uses stored information when answering
"""

from __future__ import annotations


class Memory:
    """A simple in-memory storage system for user preferences and context."""

    def __init__(self):
        self._store = {}

    def add(self, key: str, value: str) -> None:
        self._store[key] = value

    def get(self, key: str):
        return self._store.get(key)

    def get_all(self):
        return dict(self._store)


class AgentWithMemory:
    """A simple agent that uses memory to personalize responses."""

    def __init__(self):
        self.memory = Memory()
        self.conversation_history = []

    def remember(self, key: str, value: str) -> None:
        self.memory.add(key, value)
        self.conversation_history.append({"key": key, "value": value})

    def respond(self, user_prompt: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_prompt})

        name = self.memory.get("name") or "friend"
        preferred_language = self.memory.get("preferred_language") or "Python"

        response = (
            f"Hi {name}! Based on your previous preferences, I recommend a project using "
            f"{preferred_language}. This is a good fit for your interests and matches your "
            f"needs."
        )

        self.conversation_history.append({"role": "assistant", "content": response})
        return response


def main():
    print("Part 5: Adding Memory and Context to AI Agents")

    memory = Memory()
    memory.add("name", "Abraham")
    memory.add("preferred_language", "Python")

    agent = AgentWithMemory()
    agent.memory = memory

    print("\nStored preferences:")
    for key, value in memory.get_all().items():
        print(f"  - {key}: {value}")

    print("\nAgent response:")
    print(agent.respond("Recommend a project for me"))


if __name__ == "__main__":
    main()
