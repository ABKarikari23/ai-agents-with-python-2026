"""Analysis agent: diagnoses the incident from gathered evidence.

The agent makes its decision using current evidence (metrics and logs)
rather than assumptions — article section 11.
"""

from __future__ import annotations


class AnalysisAgent:
    """Combines metrics and logs into a diagnosis and a recommended action."""

    def diagnose(self, event, metrics: dict, logs: list) -> dict:
        findings = []

        cpu = metrics.get("cpu", 0)
        if cpu >= 90:
            findings.append(f"CPU is critically high at {cpu}%")
        if any("slow" in line.lower() for line in logs):
            findings.append("logs show slow database connections")
        if any("high cpu" in line.lower() for line in logs):
            findings.append("high CPU was also recorded in the logs")

        diagnosis = "; ".join(findings) or "no clear cause found in the gathered evidence"
        action = "restart_service" if cpu >= 90 else "create_ticket"

        return {
            "diagnosis": diagnosis,
            "recommended_action": action,
            "evidence": {"metrics": metrics, "logs": logs},
        }
