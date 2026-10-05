"""
AI Agents for Automation — Building Useful Agentic Workflows
Part of: AI Agents with Python 2026

This example demonstrates the automation pattern from the Part 8 article:
- an event triggers the workflow instead of a human starting it manually
- agents analyze the event, gather evidence with tools, and diagnose the issue
- guardrails decide which tools the agent may use
- high-risk actions require human approval (human-in-the-loop)
- the workflow verifies the result instead of assuming success
- every step is recorded in an observability trace
"""

from __future__ import annotations

import logging
from datetime import datetime

from workflows.incident_workflow import Event, IncidentWorkflow


def simulated_engineer_approval(action: str, context: dict) -> bool:
    """Simulated human-in-the-loop approval (article section 17)."""
    print(f"\n[human-in-the-loop] Approval requested for high-risk action: {action}")
    print("[human-in-the-loop] Diagnosis:", context["diagnosis"]["diagnosis"])
    print("[human-in-the-loop] Approved (simulated engineer)\n")
    return True


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    print("Part 8: AI Agents for Automation — Building Useful Agentic Workflows")

    alert = Event(
        event_type="system_alert",
        source="monitoring",
        message="Server server-01 CPU usage is 95%",
        timestamp=datetime.now(),
    )

    workflow = IncidentWorkflow(approval_callback=simulated_engineer_approval)
    result = workflow.run(alert)

    print("\n--- Workflow trace ---")
    for entry in result.trace:
        print(entry)

    print("\nStatus:", result.status)
    if result.diagnosis:
        print("Diagnosis:", result.diagnosis["diagnosis"])
    print("Verified:", result.verified)
    print("Report:", result.report)

    # A low-severity event takes the deterministic path: no incident, no escalation.
    quiet_event = Event(
        event_type="system_alert",
        source="monitoring",
        message="Server server-02 CPU usage is 35%",
        timestamp=datetime.now(),
    )
    quiet_result = IncidentWorkflow().run(quiet_event)
    print("\n--- Low-severity event ---")
    print("Status:", quiet_result.status)
    print("Report:", quiet_result.report)


if __name__ == "__main__":
    main()
