"""Simulated monitoring tools (article section 11).

In production these would call a real monitoring API. Here an in-memory
store keeps the example self-contained and lets the workflow verify that a
remediation action actually worked instead of assuming success.
"""

_SERVERS = {
    "server-01": {"cpu": 95, "memory": 72, "disk": 64},
    "server-02": {"cpu": 35, "memory": 40, "disk": 55},
}


def get_server_metrics(server: str) -> dict:
    """Return the current metrics for a server."""
    return dict(_SERVERS.get(server, {"cpu": 0, "memory": 0, "disk": 0}))


def restart_service(server: str) -> dict:
    """Simulated remediation: restart the service and bring CPU back to normal."""
    if server in _SERVERS:
        _SERVERS[server]["cpu"] = 35
    return {"server": server, "restarted": True}


def _reset_demo_state() -> None:
    """Restore the demo servers (used by the tests)."""
    _SERVERS["server-01"]["cpu"] = 95
    _SERVERS["server-02"]["cpu"] = 35
