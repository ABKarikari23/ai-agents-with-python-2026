"""Simulated log retrieval tool (article section 11)."""

_LOGS = {
    "server-01": [
        "Application started",
        "Database connection slow",
        "High CPU detected",
    ],
    "server-02": [
        "Application started",
        "Health check passed",
    ],
}


def get_recent_logs(server: str) -> list:
    """Return the most recent log lines for a server."""
    return list(_LOGS.get(server, []))
