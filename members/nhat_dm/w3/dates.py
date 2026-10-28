"""W3-1: Parse due dates from relative strings, ISO format, or weekday names."""

from datetime import date, timedelta
import re

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
    """Parse a date string into a date object relative to `today`.

    Accepts:
    - ISO format dates: e.g. '2026-10-30'
    - 'tomorrow' -> today + 1 day
    - 'today' -> today
    - 'in N days' / 'in N day' -> today + N days
    - Weekday names (e.g. 'Fri', 'Tue', 'Monday') -> next occurrence (> today)

    Raises:
        ValueError: If text cannot be parsed or format is unknown.
    """
    if not isinstance(text, str):
        raise ValueError("Date text must be a string")

    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Date text cannot be empty")

    lower = cleaned.lower()

    if lower == "tomorrow":
        return today + timedelta(days=1)

    if lower == "today":
        return today

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
        return date.fromisoformat(cleaned)
    except ValueError as exc:
        raise ValueError(f"Unknown date expression: {text!r}") from exc
