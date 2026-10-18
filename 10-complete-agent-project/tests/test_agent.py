import pytest

from app.agent import AgentError, run_agent
from app.model_adapter import DemoModelAdapter, ModelDecision


def test_demo_agent_returns_grounded_troubleshooting_guidance(tmp_path, monkeypatch):
    import app.memory as memory

    database_path = tmp_path / "agent.db"
    monkeypatch.setattr(memory, "DB_PATH", database_path)

    response = run_agent(
        DemoModelAdapter(),
        "test-user",
        "What should I check if my application is unavailable and the server is online?",
    )

    assert "application service is running" in response
    assert "not a confirmed diagnosis" in response
    assert "Sources:" in response
    assert database_path.exists()


def test_metrics_request_uses_an_approved_tool(tmp_path, monkeypatch):
    import app.memory as memory

    monkeypatch.setattr(memory, "DB_PATH", tmp_path / "agent.db")
    response = run_agent(
        DemoModelAdapter(),
        "test-user",
        "Show the CPU metrics for the server.",
    )

    assert "cpu_usage_percent" in response
    assert "not a live system check" in response


def test_ticket_request_only_prepares_a_draft(tmp_path, monkeypatch):
    import app.memory as memory

    monkeypatch.setattr(memory, "DB_PATH", tmp_path / "agent.db")
    response = run_agent(
        DemoModelAdapter(),
        "test-user",
        "Please draft a support ticket for the application issue.",
    )

    assert "has not been submitted" in response


def test_empty_request_is_rejected():
    with pytest.raises(ValueError, match="cannot be empty"):
        run_agent(DemoModelAdapter(), "test-user", "  ")


def test_malformed_model_decision_is_rejected(tmp_path, monkeypatch):
    import app.memory as memory

    monkeypatch.setattr(memory, "DB_PATH", tmp_path / "agent.db")

    class MalformedAdapter:
        def decide(self, messages, available_tools):
            return ModelDecision(kind="tool_call")

    with pytest.raises(AgentError, match="malformed tool call"):
        run_agent(MalformedAdapter(), "test-user", "Check the server metrics.")


def test_repeated_tool_calls_are_bounded(tmp_path, monkeypatch):
    import app.memory as memory

    monkeypatch.setattr(memory, "DB_PATH", tmp_path / "agent.db")

    class RepeatingToolAdapter:
        def decide(self, messages, available_tools):
            return ModelDecision(
                kind="tool_call",
                tool_name="get_server_metrics",
                arguments={"server": "server-01"},
            )

    with pytest.raises(AgentError, match="maximum tool-call count"):
        run_agent(RepeatingToolAdapter(), "test-user", "Check server metrics.")
