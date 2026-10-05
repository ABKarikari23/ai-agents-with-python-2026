"""Configuration and guardrails for the Part 8 automation example.

The agents can recommend actions, but the application decides whether those
actions are permitted — article sections 18-20.
"""

# Stop rule: maximum number of tool executions per workflow run (section 20).
MAX_STEPS = 8

# Retry policy for flaky tools and APIs (section 21).
MAX_RETRIES = 3

# Guardrail: only these tools may be executed by the agent (section 19).
ALLOWED_TOOLS = {
    "get_metrics",
    "get_logs",
    "restart_service",
    "create_ticket",
    "send_notification",
}

# Guardrail: the automation only operates in these environments (section 19).
ALLOWED_ENVIRONMENTS = {
    "development",
    "staging",
}

# Risk-based autonomy policy (section 18).
RISK_POLICY = {
    "get_metrics": "low",
    "get_logs": "low",
    "send_notification": "medium",
    "create_ticket": "medium",
    "restart_service": "high",
    "delete_data": "critical",
}

# Risk levels that require human approval before execution.
HIGH_RISK_LEVELS = {"high", "critical"}


def is_allowed(tool_name: str) -> bool:
    """Return True only when the tool is explicitly permitted."""
    return tool_name in ALLOWED_TOOLS


def risk_level(tool_name: str) -> str:
    """Return the risk level for a tool; unknown tools default to critical."""
    return RISK_POLICY.get(tool_name, "critical")
