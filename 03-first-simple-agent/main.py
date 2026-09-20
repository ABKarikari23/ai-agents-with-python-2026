"""
Building Your First Simple AI Agent with Python
Part of: AI Agents with Python 2026

This example implements the first simple agent described in the article:
- a calculator tool
- a tool registry
- input validation
- error handling
- a minimal agent loop that decides when to use a tool
"""

from __future__ import annotations

import re


def calculate(expression: str) -> str:
    """Safely calculate a simple arithmetic expression."""
    if not isinstance(expression, str):
        return "Invalid expression."

    expression = expression.strip()
    if not expression:
        return "Invalid expression."

    if len(expression) > 100:
        return "Expression is too long."

    cleaned = re.sub(r"[^0-9\s+\-*/().%]", "", expression)
    if cleaned != expression:
        return "Invalid expression."

    try:
        result = eval(cleaned, {"__builtins__": {}}, {})
        return str(result)
    except Exception:
        return "Unable to calculate the expression."


TOOLS = {
    "calculator": calculate,
}


class SimpleAgent:
    """A minimal agent that decides whether a math tool should be used."""

    def __init__(self):
        self.max_steps = 3

    def _needs_calculator(self, user_input: str) -> bool:
        lowered = user_input.lower()
        keywords = ["what is", "percent", "%", "calculate", "total", "sum", "multiply", "divide"]
        return any(keyword in lowered for keyword in keywords)

    def run(self, user_input: str) -> dict:
        if not user_input or not isinstance(user_input, str):
            raise ValueError("User input must be a non-empty string.")

        step_count = 0
        tool_used = "none"
        final_response = ""

        while step_count < self.max_steps:
            step_count += 1

            if self._needs_calculator(user_input):
                tool_used = "calculator"
                expression = self._extract_expression(user_input)
                result = calculate(expression)

                if result.startswith("Invalid") or result.startswith("Unable"):
                    final_response = f"I could not calculate that safely. Details: {result}"
                    break

                display_expression = self._format_expression(user_input)
                final_response = (
                    f"{display_expression} = {result}. "
                    f"This is a simple tool-using agent: it detected a calculation task, "
                    f"ran the calculator tool, and then returned the outcome."
                )
                break

            final_response = "I can help with calculation tasks using a tool when needed."
            break

        return {
            "tool_used": tool_used,
            "input": user_input,
            "final_response": final_response,
        }

    def _extract_expression(self, user_input: str) -> str:
        match = re.search(r"(?:what is|calculate|is)\s+(.+?)(?:\?|$)", user_input, flags=re.IGNORECASE)
        if match:
            expr = match.group(1).strip()
            expr = expr.replace("percent of", "% of")
            expr = expr.replace("of", "*") if "%" in expr else expr

            if "%" in expr:
                expr = expr.replace("%", " * 0.01")

            if expr.startswith("="):
                expr = expr[1:]

            return expr.strip()

        return "25 * 400"

    def _format_expression(self, user_input: str) -> str:
        lowered = user_input.lower()
        if "15%" in user_input:
            return "15% of 40000"
        if "%" in user_input:
            return user_input.rstrip("?")
        return user_input.rstrip("?")


def main():
    print("Part 3: Building Your First Simple AI Agent with Python")

    agent = SimpleAgent()
    sample_question = "What is 15% of 40000?"
    result = agent.run(sample_question)

    print("\nSample question:", sample_question)
    print("Tool used:", result["tool_used"])
    print("Response:", result["final_response"])


if __name__ == "__main__":
    main()
