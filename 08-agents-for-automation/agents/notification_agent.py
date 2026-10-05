"""Notification agent: composes the report for a workflow outcome.

The agent only *decides what to say*; the workflow executes the actual
send_notification tool call through the guardrail layer (article section 19).
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class NotificationAgent:
    """Builds the human-readable incident report."""

    def compose_report(self, event, diagnosis: dict, status: str, verified: bool) -> str:
        verification = "verified" if verified else "not verified"
        report = (
            f"Incident {status}: {event.message} | "
            f"Diagnosis: {diagnosis['diagnosis']} | "
            f"Action: {diagnosis['recommended_action']} ({verification})"
        )
        logger.info("Report composed: %s", report)
        return report
