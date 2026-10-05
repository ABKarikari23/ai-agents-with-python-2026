import importlib.util
from datetime import datetime
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).with_name("main.py")
SPEC = importlib.util.spec_from_file_location("part8_main", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

import config
from tools import monitoring as monitoring_tool
from tools import notifications as notifications_tool
from workflows.incident_workflow import Event, IncidentWorkflow, retry


def make_event(message, source="monitoring"):
    return Event(
        event_type="system_alert",
        source=source,
        message=message,
        timestamp=datetime(2026, 1, 1, 10, 0, 0),
    )


class Part8AutomationTest(unittest.TestCase):
    def setUp(self):
        monitoring_tool._reset_demo_state()
        notifications_tool._reset_demo_state()

    def test_high_cpu_event_runs_full_workflow(self):
        workflow = IncidentWorkflow(
            approval_callback=lambda action, context: True, sleep=lambda _: None
        )
        result = workflow.run(make_event("Server server-01 CPU usage is 95%"))

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.analysis["severity"], "high")
        self.assertIsNotNone(result.diagnosis)
        self.assertTrue(result.action_result["restarted"])
        self.assertTrue(result.verified)
        self.assertTrue(result.trace)

    def test_low_cpu_event_requires_no_action(self):
        result = IncidentWorkflow().run(make_event("Server server-02 CPU usage is 35%"))

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.analysis["severity"], "low")
        self.assertEqual(result.report, "No action required")
        self.assertIsNone(result.action_result)

    def test_high_risk_action_needs_approval(self):
        workflow = IncidentWorkflow(
            approval_callback=lambda action, context: False, sleep=lambda _: None
        )
        result = workflow.run(make_event("Server server-01 CPU usage is 95%"))

        self.assertEqual(result.status, "escalated")
        self.assertIn("requires human approval", result.report)
        # The high-risk restart must NOT have happened.
        self.assertEqual(monitoring_tool.get_server_metrics("server-01")["cpu"], 95)
        # Instead, an escalation ticket was created for a human engineer.
        self.assertEqual(result.action_result["status"], "open")

    def test_guardrail_blocks_unauthorized_tools(self):
        self.assertTrue(config.is_allowed("get_metrics"))
        self.assertFalse(config.is_allowed("delete_data"))
        self.assertEqual(config.risk_level("restart_service"), "high")
        self.assertEqual(config.risk_level("unknown_tool"), "critical")

    def test_stop_rule_limits_tool_calls(self):
        original = config.MAX_STEPS
        config.MAX_STEPS = 1
        try:
            workflow = IncidentWorkflow(sleep=lambda _: None)
            result = workflow.run(make_event("Server server-01 CPU usage is 95%"))
        finally:
            config.MAX_STEPS = original

        self.assertEqual(result.status, "failed")
        self.assertIn("Stop rule", result.report)

    def test_retry_succeeds_after_temporary_failures(self):
        attempts = []

        def flaky():
            attempts.append(1)
            if len(attempts) < 3:
                raise ConnectionError("temporary failure")
            return "ok"

        self.assertEqual(retry(flaky, sleep=lambda _: None), "ok")
        self.assertEqual(len(attempts), 3)

    def test_retry_raises_after_final_attempt(self):
        def always_fails():
            raise TimeoutError("still down")

        with self.assertRaises(TimeoutError):
            retry(always_fails, sleep=lambda _: None)

    def test_ticket_creation_is_idempotent(self):
        first = notifications_tool.create_ticket("Investigate CPU", "INC-1")
        second = notifications_tool.create_ticket("Investigate CPU", "INC-1")

        self.assertFalse(first["duplicate"])
        self.assertTrue(second["duplicate"])
        self.assertEqual(first["id"], second["id"])


if __name__ == "__main__":
    unittest.main()
