"""Notification and ticketing tools.

Ticket creation is idempotent (article section 22): repeating a request with
the same request_id returns the existing ticket instead of creating a
duplicate. This matters whenever an automated agent retries an action after
a timeout and cannot know whether the first attempt succeeded.
"""

_SENT_NOTIFICATIONS = []
_TICKETS = {}


def send_notification(channel: str, message: str) -> dict:
    """Send a notification to a channel (simulated)."""
    notification = {"channel": channel, "message": message}
    _SENT_NOTIFICATIONS.append(notification)
    return {"sent": True, "channel": channel, "message": message}


def create_ticket(title: str, request_id: str) -> dict:
    """Create a support ticket idempotently."""
    if request_id in _TICKETS:
        return {**_TICKETS[request_id], "duplicate": True}

    ticket = {"id": request_id, "title": title, "status": "open"}
    _TICKETS[request_id] = ticket
    return {**ticket, "duplicate": False}


def _reset_demo_state() -> None:
    """Clear notifications and tickets (used by the tests)."""
    _SENT_NOTIFICATIONS.clear()
    _TICKETS.clear()
