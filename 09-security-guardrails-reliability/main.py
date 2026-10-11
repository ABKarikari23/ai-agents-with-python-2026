"""
Security, Guardrails and Reliability in AI Agents
Part of: AI Agents with Python 2026

This teaching demo keeps tool execution behind application-enforced policies.
The approval Boolean is only for the local demonstration; production approval
must be verified by the application and bound to the exact proposed action.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping

logger = logging.getLogger("agent_security")

ToolHandler = Callable[..., Any]
ArgumentValidator = Callable[[Mapping[str, Any]], dict[str, Any]]

_SERVICE_STATES = {
    "nginx": "degraded",
    "redis": "healthy",
}


class GuardrailError(Exception):
    """Base exception for a tool call rejected by a guardrail."""


class UnknownToolError(GuardrailError):
    """Raised when a proposed tool is not registered."""


class UnauthorizedToolError(GuardrailError):
    """Raised when an agent role cannot use a registered tool."""


class InvalidArgumentsError(GuardrailError):
    """Raised when tool arguments fail application validation."""


class ApprovalRequired(GuardrailError):
    """Raised when a tool requires approval that has not been provided."""


class ToolCallLimitExceeded(GuardrailError):
    """Raised when a workflow exceeds its configured tool-call budget."""


def _copy_arguments(arguments: Mapping[str, Any]) -> dict[str, Any]:
    return dict(arguments)


@dataclass(frozen=True)
class ToolPolicy:
    handler: ToolHandler
    allowed_roles: frozenset[str]
    requires_approval: bool = False
    validator: ArgumentValidator = _copy_arguments


class AgentGuardrails:
    """Authorize and validate every proposed tool call before execution."""

    def __init__(
        self,
        policies: Mapping[str, ToolPolicy],
        max_tool_calls: int = 10,
    ) -> None:
        if (
            isinstance(max_tool_calls, bool)
            or not isinstance(max_tool_calls, int)
            or max_tool_calls < 1
        ):
            raise ValueError("max_tool_calls must be a positive integer.")

        self._policies = MappingProxyType(dict(policies))
        self.max_tool_calls = max_tool_calls
        self.tool_calls = 0

    def execute(
        self,
        tool_name: str,
        role: str,
        arguments: Mapping[str, Any],
        *,
        approved: bool = False,
    ) -> Any:
        """Run a registered tool only after its policy checks pass.

        Every proposal consumes one call from the workflow budget, including
        rejected proposals, so repeated unauthorized attempts are bounded too.
        """
        if self.tool_calls >= self.max_tool_calls:
            raise ToolCallLimitExceeded(
                "Agent stopped: maximum tool-call count reached."
            )
        self.tool_calls += 1

        logger.info("Tool proposed: tool=%s role=%s", tool_name, role)
        policy = self._policies.get(tool_name)
        if policy is None:
            raise UnknownToolError(f"Unknown tool: {tool_name}")
        if role not in policy.allowed_roles:
            raise UnauthorizedToolError(
                f"Role {role!r} is not authorized to use {tool_name!r}."
            )
        if not isinstance(arguments, Mapping):
            raise InvalidArgumentsError("Tool arguments must be a mapping.")

        validated_arguments = policy.validator(arguments)
        if policy.requires_approval and not approved:
            raise ApprovalRequired(
                f"Tool {tool_name!r} requires human approval."
            )

        logger.info("Tool authorization passed: tool=%s role=%s", tool_name, role)
        return policy.handler(**validated_arguments)


def _validate_server_arguments(arguments: Mapping[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"server"}:
        raise InvalidArgumentsError("Expected exactly one 'server' argument.")
    server = arguments["server"]
    if not isinstance(server, str) or server not in {"server-01", "server-02"}:
        raise InvalidArgumentsError("Server is not in the approved server list.")
    return {"server": server}


def _validate_service_arguments(arguments: Mapping[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"service"}:
        raise InvalidArgumentsError("Expected exactly one 'service' argument.")
    service = arguments["service"]
    if not isinstance(service, str) or service not in _SERVICE_STATES:
        raise InvalidArgumentsError("Service is not in the approved service list.")
    return {"service": service}


def get_server_metrics(server: str) -> dict[str, Any]:
    """Return deterministic sample metrics without contacting an external API."""
    cpu_usage = {"server-01": 74, "server-02": 35}[server]
    return {
        "server": server,
        "cpu_usage": cpu_usage,
        "status": "online",
    }


def restart_service(service: str) -> dict[str, Any]:
    """Simulate restarting an approved service in local demo state."""
    _SERVICE_STATES[service] = "healthy"
    return {"service": service, "restarted": True, "status": "healthy"}


def build_policies() -> dict[str, ToolPolicy]:
    return {
        "get_server_metrics": ToolPolicy(
            handler=get_server_metrics,
            allowed_roles=frozenset({"monitoring_agent", "it_agent"}),
            validator=_validate_server_arguments,
        ),
        "restart_service": ToolPolicy(
            handler=restart_service,
            allowed_roles=frozenset({"infrastructure_agent"}),
            requires_approval=True,
            validator=_validate_service_arguments,
        ),
    }


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    print("Part 9: Security, Guardrails and Reliability in AI Agents")

    guardrails = AgentGuardrails(build_policies(), max_tool_calls=5)
    metrics = guardrails.execute(
        tool_name="get_server_metrics",
        role="monitoring_agent",
        arguments={"server": "server-01"},
    )
    print("\nAuthorized read-only tool:")
    print(metrics)

    print("\nUnauthorized tool attempt:")
    try:
        guardrails.execute(
            tool_name="restart_service",
            role="monitoring_agent",
            arguments={"service": "nginx"},
        )
    except GuardrailError as error:
        print(f"Blocked: {error}")

    print("\nApproval-gated action:")
    try:
        guardrails.execute(
            tool_name="restart_service",
            role="infrastructure_agent",
            arguments={"service": "nginx"},
        )
    except ApprovalRequired as error:
        print(f"Blocked: {error}")

    print("Simulated engineer approval received.")
    result = guardrails.execute(
        tool_name="restart_service",
        role="infrastructure_agent",
        arguments={"service": "nginx"},
        approved=True,
    )
    print(result)
    print(f"\nTool proposals used: {guardrails.tool_calls}/5")


if __name__ == "__main__":
    main()
