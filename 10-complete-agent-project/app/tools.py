"""Explicitly registered, limited-capability demo tools."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping

from app.knowledge import search_knowledge

ToolHandler = Callable[..., Any]


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    allowed_roles: frozenset[str]
    handler: ToolHandler


def get_server_metrics(server: str) -> dict[str, str | int]:
    """Return sample metrics without connecting to a real server."""
    return {
        "server": server,
        "status": "online",
        "cpu_usage_percent": 42,
        "memory_usage_percent": 68,
        "source": "demonstration data; not live monitoring",
    }


def draft_support_ticket(title: str, description: str) -> dict[str, str]:
    """Prepare a local ticket draft without submitting it externally."""
    return {"status": "draft", "title": title, "description": description}


TOOL_REGISTRY: Mapping[str, ToolDefinition] = MappingProxyType(
    {
        "search_knowledge": ToolDefinition(
            name="search_knowledge",
            description="Search approved local troubleshooting documents.",
            allowed_roles=frozenset({"it_assistant"}),
            handler=search_knowledge,
        ),
        "get_server_metrics": ToolDefinition(
            name="get_server_metrics",
            description="Read demonstration metrics for an approved server name.",
            allowed_roles=frozenset({"it_assistant"}),
            handler=get_server_metrics,
        ),
        "draft_support_ticket": ToolDefinition(
            name="draft_support_ticket",
            description="Prepare a support ticket draft without submitting it.",
            allowed_roles=frozenset({"it_assistant"}),
            handler=draft_support_ticket,
        ),
    }
)
