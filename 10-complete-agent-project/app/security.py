"""Application-enforced tool authorization and argument validation."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.tools import TOOL_REGISTRY


class ToolAuthorizationError(Exception):
    """Base exception for rejected tool proposals."""


class UnknownToolError(ToolAuthorizationError):
    """Raised when a proposed tool is not registered."""


class UnauthorizedToolError(ToolAuthorizationError):
    """Raised when a role cannot use a registered tool."""


class InvalidToolArgumentsError(ToolAuthorizationError):
    """Raised when tool arguments do not match the tool schema."""


class _StrictArguments(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class KnowledgeSearchArguments(_StrictArguments):
    query: str = Field(min_length=1, max_length=500)


class MetricsArguments(_StrictArguments):
    server: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[a-zA-Z0-9][a-zA-Z0-9.-]*$",
    )


class TicketDraftArguments(_StrictArguments):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=2000)


ARGUMENT_SCHEMAS: dict[str, type[_StrictArguments]] = {
    "search_knowledge": KnowledgeSearchArguments,
    "get_server_metrics": MetricsArguments,
    "draft_support_ticket": TicketDraftArguments,
}


def execute_authorized_tool(
    tool_name: str,
    role: str,
    arguments: dict[str, Any],
) -> Any:
    """Validate a proposal and execute only its registered handler."""
    tool = TOOL_REGISTRY.get(tool_name)
    if tool is None:
        raise UnknownToolError(f"Unknown tool: {tool_name}")
    if role not in tool.allowed_roles:
        raise UnauthorizedToolError(
            f"Role {role!r} is not authorized to use {tool_name!r}."
        )
    if not isinstance(arguments, dict):
        raise InvalidToolArgumentsError("Tool arguments must be an object.")

    schema = ARGUMENT_SCHEMAS[tool_name]
    try:
        validated_arguments = schema.model_validate(arguments).model_dump()
    except ValidationError as error:
        raise InvalidToolArgumentsError(
            f"Invalid arguments for tool {tool_name!r}."
        ) from error

    return tool.handler(**validated_arguments)
