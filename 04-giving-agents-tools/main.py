"""
Giving AI Agents Tools — APIs, Functions and External Services
Part of: AI Agents with Python 2026

This example demonstrates the Part 4 concept of a tool-enabled AI agent:
- a weather tool that behaves like an external API call
- tool metadata / registry
- a simple decision layer
- validation, safety, and clear boundaries around tool execution
"""

from __future__ import annotations


def get_weather(city: str) -> dict:
    """Simulate a weather API response for a city."""
    city = str(city).strip()
    if not city:
        raise ValueError("City name is required.")

    sample_data = {
        "Accra": {"city": "Accra", "temperature": 28, "condition": "Partly Cloudy", "humidity": 75},
        "Kumasi": {"city": "Kumasi", "temperature": 26, "condition": "Sunny", "humidity": 68},
        "Takoradi": {"city": "Takoradi", "temperature": 29, "condition": "Humid", "humidity": 80},
    }

    data = sample_data.get(city.title())
    if data is None:
        return {
            "city": city.title(),
            "temperature": "unknown",
            "condition": "data unavailable",
            "humidity": "unknown",
            "note": "Demo data only; replace with a real API in production.",
        }

    return data


TOOLS = {
    "get_weather": {
        "description": "Get the current weather conditions for a city.",
        "function": get_weather,
        "parameters": ["city"],
    }
}


class ToolAwareAgent:
    """A simple agent that decides when to use a weather tool."""

    def __init__(self):
        self.tools = TOOLS

    def _needs_weather(self, user_input: str) -> bool:
        lowered = user_input.lower()
        return any(keyword in lowered for keyword in ["weather", "temperature", "rain", "cloudy", "sunny"])

    def run(self, user_input: str) -> dict:
        if not user_input:
            raise ValueError("User input is required.")

        if self._needs_weather(user_input):
            city = self._extract_city(user_input)
            tool_result = get_weather(city)
            return {
                "tool_used": "get_weather",
                "city": tool_result.get("city", city.title()),
                "final_response": (
                    f"The weather in {tool_result.get('city', city.title())} is "
                    f"{tool_result.get('condition', 'unknown')} with a temperature of "
                    f"{tool_result.get('temperature', 'unknown')}°C."
                ),
            }

        return {
            "tool_used": "none",
            "final_response": "I can help with weather, data, or other tool-based tasks.",
        }

    def _extract_city(self, user_input: str) -> str:
        for city in ["Accra", "Kumasi", "Takoradi"]:
            if city.lower() in user_input.lower():
                return city
        return "Accra"


def main():
    print("Part 4: Giving AI Agents Tools — APIs, Functions and External Services")

    agent = ToolAwareAgent()
    question = "What is the weather in Accra?"
    result = agent.run(question)

    print("\nQuestion:", question)
    print("Tool used:", result["tool_used"])
    print("Response:", result["final_response"])


if __name__ == "__main__":
    main()
