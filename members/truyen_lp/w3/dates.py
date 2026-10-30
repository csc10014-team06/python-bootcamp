"""W3-1: Parse due dates from ISO format, relative text, or weekday names."""

from __future__ import annotations

import re
from datetime import date, timedelta

_WEEKDAYS: dict[str, int] = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tues": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thur": 3,
    "thurs": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}


def parse_due(text: str, today: date) -> date:
    """Parse a date string relative to `today`.

    Accepts:
    - ISO 8601 date: e.g. "2026-10-30"
    - "today" -> today
    - "tomorrow" -> today + 1 day
    - "in N days" / "in N day" -> today + N days
    - Weekday name (e.g. "Fri", "Tue", "Monday") -> next occurrence (> today)

    Raises:
        TypeError: If text is not a string.
        ValueError: If text is empty or format cannot be parsed.
    """
    if not isinstance(text, str):
        raise TypeError("Due date must be a string")

    clean = text.strip()
    if not clean:
        raise ValueError("Due date cannot be empty")

    lower = clean.lower()

    if lower == "today":
        return today

    if lower == "tomorrow":
        return today + timedelta(days=1)

    rel_match = re.match(r"^in\s+(\d+)\s+days?$", lower)
    if rel_match:
        days = int(rel_match.group(1))
        return today + timedelta(days=days)

    if lower in _WEEKDAYS:
        target_wd = _WEEKDAYS[lower]
        days_ahead = (target_wd - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)

    try:
        return date.fromisoformat(clean)
    except ValueError as exc:
        raise ValueError(f"Unknown due date format: {text!r}") from exc
