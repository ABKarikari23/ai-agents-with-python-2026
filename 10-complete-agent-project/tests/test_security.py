import pytest
from pydantic import ValidationError

from app.security import (
    InvalidToolArgumentsError,
    UnauthorizedToolError,
    UnknownToolError,
    execute_authorized_tool,
)


def test_unknown_tool_is_rejected():
    with pytest.raises(UnknownToolError):
        execute_authorized_tool("delete_everything", "it_assistant", {})


def test_invalid_server_name_is_rejected():
    with pytest.raises(InvalidToolArgumentsError) as error:
        execute_authorized_tool(
            "get_server_metrics",
            "it_assistant",
            {"server": "../../etc/passwd"},
        )

    assert isinstance(error.value.__cause__, ValidationError)


def test_unknown_arguments_are_rejected():
    with pytest.raises(InvalidToolArgumentsError):
        execute_authorized_tool(
            "get_server_metrics",
            "it_assistant",
            {"server": "server-01", "execute": "unexpected"},
        )


def test_unauthorized_role_is_rejected():
    with pytest.raises(UnauthorizedToolError):
        execute_authorized_tool(
            "get_server_metrics",
            "guest",
            {"server": "server-01"},
        )


def test_ticket_tool_only_creates_a_draft():
    result = execute_authorized_tool(
        "draft_support_ticket",
        "it_assistant",
        {"title": "Application issue", "description": "Users cannot connect."},
    )

    assert result["status"] == "draft"
