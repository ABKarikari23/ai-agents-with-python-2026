import importlib.util
from pathlib import Path
import sys
import unittest

MODULE_PATH = Path(__file__).with_name("main.py")
SPEC = importlib.util.spec_from_file_location("part9_main", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Could not load Part 9 module from {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class Part9GuardrailsTest(unittest.TestCase):
    def setUp(self):
        MODULE._SERVICE_STATES.update({"nginx": "degraded", "redis": "healthy"})
        self.guardrails = MODULE.AgentGuardrails(MODULE.build_policies())

    def test_authorized_role_can_call_registered_tool(self):
        result = self.guardrails.execute(
            "get_server_metrics",
            "monitoring_agent",
            {"server": "server-01"},
        )

        self.assertEqual(result["cpu_usage"], 74)
        self.assertEqual(result["status"], "online")

    def test_unknown_tool_is_rejected(self):
        with self.assertRaises(MODULE.UnknownToolError):
            self.guardrails.execute("delete_data", "it_agent", {})

    def test_role_without_permission_is_rejected(self):
        with self.assertRaises(MODULE.UnauthorizedToolError):
            self.guardrails.execute(
                "get_server_metrics",
                "content_agent",
                {"server": "server-01"},
            )

    def test_invalid_server_is_rejected_before_handler_runs(self):
        with self.assertRaises(MODULE.InvalidArgumentsError):
            self.guardrails.execute(
                "get_server_metrics",
                "monitoring_agent",
                {"server": "../../etc/passwd"},
            )

    def test_sensitive_action_requires_approval(self):
        with self.assertRaises(MODULE.ApprovalRequired):
            self.guardrails.execute(
                "restart_service",
                "infrastructure_agent",
                {"service": "nginx"},
            )

        self.assertEqual(MODULE._SERVICE_STATES["nginx"], "degraded")

    def test_approved_sensitive_action_runs(self):
        result = self.guardrails.execute(
            "restart_service",
            "infrastructure_agent",
            {"service": "nginx"},
            approved=True,
        )

        self.assertTrue(result["restarted"])
        self.assertEqual(MODULE._SERVICE_STATES["nginx"], "healthy")

    def test_rejected_proposals_also_consume_call_budget(self):
        guardrails = MODULE.AgentGuardrails(MODULE.build_policies(), max_tool_calls=1)
        with self.assertRaises(MODULE.UnknownToolError):
            guardrails.execute("unknown", "it_agent", {})

        with self.assertRaises(MODULE.ToolCallLimitExceeded):
            guardrails.execute(
                "get_server_metrics",
                "monitoring_agent",
                {"server": "server-01"},
            )

    def test_tool_call_limit_must_be_positive(self):
        with self.assertRaises(ValueError):
            MODULE.AgentGuardrails(MODULE.build_policies(), max_tool_calls=0)


if __name__ == "__main__":
    unittest.main()
