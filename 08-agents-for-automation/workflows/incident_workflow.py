"""Incident workflow: the automated agent loop from the Part 8 article.

    Event → Analyze → Gather Evidence → Reason → Select Action
          → (Human approval for high-risk) → Execute → Verify → Report

The critical addition over a fixed pipeline is verification: the agent does
not perform an action and assume it worked — it checks the outcome.
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime

import config
from agents.analysis_agent import AnalysisAgent
from agents.monitoring_agent import MonitoringAgent
from agents.notification_agent import NotificationAgent
from tools import logs as logs_tool
from tools import monitoring as monitoring_tool
from tools import notifications as notifications_tool

logger = logging.getLogger(__name__)


@dataclass
class Event:
    """A structured trigger for the automation (article section 9)."""

    event_type: str
    source: str
    message: str
    timestamp: datetime


@dataclass
class WorkflowResult:
    """The outcome of a workflow run, including its observability trace."""

    status: str
    trace: list = field(default_factory=list)
    analysis: dict | None = None
    diagnosis: dict | None = None
    action_result: dict | None = None
    verified: bool = False
    report: str = ""


def retry(operation, retries: int = config.MAX_RETRIES, sleep=time.sleep):
    """Run an operation with exponential backoff (article section 21).

    Attempt 1 → immediate, attempt 2 → after 2s, attempt 3 → after 4s.
    The final exception is re-raised so the caller can escalate.
    """
    for attempt in range(retries):
        try:
            return operation()
        except Exception as error:
            if attempt == retries - 1:
                raise
            logger.warning("Tool attempt %d failed (%s) — retrying", attempt + 1, error)
            sleep(2 ** attempt)


class IncidentWorkflow:
    """Runs the incident-response automation with guardrails and stop rules."""

    def __init__(self, approval_callback=None, sleep=time.sleep):
        self.monitoring_agent = MonitoringAgent()
        self.analysis_agent = AnalysisAgent()
        self.notification_agent = NotificationAgent()
        # Human-in-the-loop (section 17): high-risk actions are denied unless
        # the approval callback explicitly approves them.
        self.approval_callback = approval_callback or (lambda action, context: False)
        self.sleep = sleep
        self._steps = 0

    def run(self, event: Event) -> WorkflowResult:
        self._steps = 0
        result = WorkflowResult(status="started")
        trace = result.trace

        try:
            self._trace(trace, f"Event received from {event.source}: {event.message}")

            # 1. Analyze the event
            result.analysis = self.monitoring_agent.analyze(event)
            self._trace(trace, f"Agent classified event as {result.analysis['severity'].upper()}")

            if not result.analysis["requires_investigation"]:
                result.status = "completed"
                result.report = "No action required"
                self._trace(trace, result.report)
                return result

            server = self._extract_server(event.message)

            # 2. Gather evidence with tools
            metrics = self._run_tool("get_metrics", trace, server=server)
            self._trace(trace, "Metrics received")
            log_lines = self._run_tool("get_logs", trace, server=server)
            self._trace(trace, "Logs received")

            # 3. Reason over the evidence
            result.diagnosis = self.analysis_agent.diagnose(event, metrics, log_lines)
            self._trace(trace, f"Diagnosis: {result.diagnosis['diagnosis']}")

            # 4. Select an action and check its risk level (section 18)
            action = result.diagnosis["recommended_action"]
            risk = config.risk_level(action)
            self._trace(trace, f"Recommended action '{action}' (risk: {risk})")

            if risk in config.HIGH_RISK_LEVELS:
                self._trace(trace, "Human approval required")
                context = {"event": event, "diagnosis": result.diagnosis}
                if not self.approval_callback(action, context):
                    return self._escalate(event, result, action)
                self._trace(trace, "Approval granted")

            # 5. Execute the approved action
            result.action_result = self._execute(action, server, event, trace)
            self._trace(trace, f"Action '{action}' executed")

            # 6. Verify the outcome instead of assuming success (section 4)
            result.verified = self._verify(action, server, result.action_result, trace)

            # 7. Report
            result.status = "completed" if result.verified else "escalated"
            result.report = self.notification_agent.compose_report(
                event, result.diagnosis, result.status, result.verified
            )
            self._run_tool(
                "send_notification", trace, channel="operations", message=result.report
            )
            self._trace(trace, "Workflow completed")

        except Exception as error:
            result.status = "failed"
            result.report = str(error)
            self._trace(trace, f"Workflow failed: {error}")

        return result

    def _execute(self, action: str, server: str, event: Event, trace: list) -> dict:
        if action == "restart_service":
            return self._run_tool("restart_service", trace, server=server)

        # Idempotent request id: retrying the same event never duplicates the ticket.
        request_id = f"INC-{event.timestamp:%Y%m%d%H%M%S}"
        title = f"{event.event_type}: {event.message}"
        return self._run_tool("create_ticket", trace, title=title, request_id=request_id)

    def _verify(self, action: str, server: str, action_result: dict, trace: list) -> bool:
        if action == "restart_service":
            metrics = self._run_tool("get_metrics", trace, server=server)
            healthy = metrics.get("cpu", 100) < 90
            self._trace(
                trace,
                "Verification: system healthy" if healthy else "Verification: issue persists",
            )
            return healthy

        verified = bool(action_result and action_result.get("id"))
        self._trace(
            trace,
            "Verification: ticket recorded" if verified else "Verification: result missing",
        )
        return verified

    def _escalate(self, event: Event, result: WorkflowResult, action: str) -> WorkflowResult:
        """High-risk action without approval → hand over to a human (section 17)."""
        trace = result.trace
        self._trace(trace, f"High-risk action '{action}' was not approved — escalating")

        request_id = f"INC-{event.timestamp:%Y%m%d%H%M%S}"
        ticket = self._run_tool(
            "create_ticket",
            trace,
            title=f"ESCALATION — {event.message}",
            request_id=request_id,
        )
        result.action_result = ticket
        result.status = "escalated"
        result.report = (
            f"High-risk action '{action}' requires human approval. "
            f"Escalated to an engineer (ticket {ticket['id']})."
        )
        self._run_tool(
            "send_notification", trace, channel="operations", message=result.report
        )
        return result

    def _run_tool(self, tool_name: str, trace: list, **kwargs):
        # Guardrail (section 19): the application decides what is permitted.
        if not config.is_allowed(tool_name):
            raise PermissionError(f"Tool '{tool_name}' is not in ALLOWED_TOOLS")

        # Stop rule (section 20): the agent must know when to stop.
        self._steps += 1
        if self._steps > config.MAX_STEPS:
            raise RuntimeError(f"Stop rule triggered: exceeded MAX_STEPS={config.MAX_STEPS}")

        self._trace(trace, f"Tool call: {tool_name}")

        operations = {
            "get_metrics": lambda: monitoring_tool.get_server_metrics(kwargs["server"]),
            "get_logs": lambda: logs_tool.get_recent_logs(kwargs["server"]),
            "restart_service": lambda: monitoring_tool.restart_service(kwargs["server"]),
            "create_ticket": lambda: notifications_tool.create_ticket(
                kwargs["title"], kwargs["request_id"]
            ),
            "send_notification": lambda: notifications_tool.send_notification(
                kwargs["channel"], kwargs["message"]
            ),
        }
        return retry(operations[tool_name], sleep=self.sleep)

    @staticmethod
    def _trace(trace: list, message: str) -> None:
        """Append a timestamped entry to the observability trace (section 23)."""
        stamp = datetime.now().strftime("%H:%M:%S")
        trace.append(f"[{stamp}] {message}")
        logger.info(message)

    @staticmethod
    def _extract_server(message: str) -> str:
        match = re.search(r"server-\d+", message.lower())
        return match.group(0) if match else "server-01"
