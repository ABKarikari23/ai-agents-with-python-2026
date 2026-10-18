"""Provider-independent model contract and an offline teaching adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Protocol


@dataclass(frozen=True)
class ModelDecision:
    kind: Literal["tool_call", "final"]
    content: str = ""
    tool_name: str | None = None
    arguments: dict[str, Any] | None = None


class ModelAdapter(Protocol):
    def decide(
        self,
        messages: list[dict[str, str]],
        available_tools: list[dict[str, str]],
    ) -> ModelDecision:
        """Return a structured final response or propose one registered tool."""
        ...


class DemoModelAdapter:
    """Deterministic offline adapter; replace it with a provider integration."""

    def decide(
        self,
        messages: list[dict[str, str]],
        available_tools: list[dict[str, str]],
    ) -> ModelDecision:
        request = next(
            message["content"]
            for message in messages
            if message["role"] == "user"
        )
        tool_results = [
            message["content"]
            for message in messages
            if message["role"] == "tool"
        ]
        lowered_request = request.lower()

        if (
            not tool_results
            and "draft" in lowered_request
            and "ticket" in lowered_request
        ):
            return ModelDecision(
                kind="tool_call",
                tool_name="draft_support_ticket",
                arguments={
                    "title": "Application access issue",
                    "description": request,
                },
            )
        if (
            not tool_results
            and any(
                term in lowered_request
                for term in ("metric", "cpu", "memory usage")
            )
        ):
            return ModelDecision(
                kind="tool_call",
                tool_name="get_server_metrics",
                arguments={"server": "server-01"},
            )

        if tool_results:
            if tool_results[-1].startswith("draft_support_ticket:"):
                return ModelDecision(
                    kind="final",
                    content=(
                        "A local support-ticket draft is ready; it has not been "
                        f"submitted. Draft details: {tool_results[-1]}"
                    ),
                )
            return ModelDecision(
                kind="final",
                content=(
                    "The approved demonstration tool returned: "
                    f"{tool_results[-1]}\n"
                    "This is sample data, not a live system check."
                ),
            )

        knowledge = next(
            (
                message["content"]
                for message in messages
                if message["role"] == "system"
                and "Retrieved knowledge:" in message["content"]
            ),
            "",
        )
        sources = [
            line.removeprefix("Source: ")
            for line in knowledge.splitlines()
            if line.startswith("Source: ")
        ]
        if sources and (
            "application" in lowered_request or "server" in lowered_request
        ):
            return ModelDecision(
                kind="final",
                content=(
                    "Start by confirming that the application service is running "
                    "and its expected port is listening. Then check DNS resolution, "
                    "firewall rules, proxy configuration, recent deployments, "
                    "application logs, and upstream dependencies. Do not restart "
                    "production services without authorization. These are "
                    "troubleshooting recommendations, not a confirmed diagnosis.\n"
                    f"Sources: {', '.join(sources)}."
                ),
            )
        if sources:
            return ModelDecision(
                kind="final",
                content=(
                    "I found relevant information in the local knowledge base. "
                    "Review the retrieved documents below:\n"
                    f"{knowledge}\nSources: {', '.join(sources)}."
                ),
            )
        return ModelDecision(
            kind="final",
            content="I could not find relevant local guidance. Please provide more context.",
        )
