"""Monitoring agent: classifies incoming events (article section 10).

A production system would let an AI model determine severity, likely cause,
required tools, and whether human approval is needed. This example uses
transparent rules so it runs without external services — the interface the
workflow depends on stays the same.
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

HIGH_CPU_THRESHOLD = 90
HIGH_SEVERITY_KEYWORDS = ("signal lost", "outage", "offline", "down")


class MonitoringAgent:
    """Analyzes monitoring events and decides whether to investigate."""

    def analyze(self, event) -> dict:
        logger.info("Analyzing event: %s", event.message)
        message = event.message.lower()

        cpu = self._extract_cpu(message)
        if cpu is not None:
            if cpu >= HIGH_CPU_THRESHOLD:
                return {"severity": "high", "requires_investigation": True}
            return {"severity": "low", "requires_investigation": False}

        if any(keyword in message for keyword in HIGH_SEVERITY_KEYWORDS):
            return {"severity": "high", "requires_investigation": True}

        return {"severity": "low", "requires_investigation": False}

    @staticmethod
    def _extract_cpu(message: str):
        """Pull a CPU percentage out of messages like 'CPU usage is 95%'."""
        match = re.search(r"cpu(?:\s+usage)?\s*(?:is|=|:)?\s*(\d{1,3})", message)
        return int(match.group(1)) if match else None
