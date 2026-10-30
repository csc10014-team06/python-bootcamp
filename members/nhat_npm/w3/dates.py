"""Parse simple due date expressions relative to a supplied date."""

import re
from datetime import date, timedelta

_IN_DAYS = re.compile(r"in\s+(\d+)\s+days?", re.IGNORECASE)
_WEEKDAYS = {
    name.lower(): day
    for day, names in enumerate(
        (
            ("Mon", "Monday"),
            ("Tue", "Tuesday"),
            ("Wed", "Wednesday"),
            ("Thu", "Thursday"),
            ("Fri", "Friday"),
            ("Sat", "Saturday"),
            ("Sun", "Sunday"),
        )
    )
    for name in names
}


def parse_due(text: str, today: date) -> date:
    """Return the date described by ISO, relative-day, or weekday text.

    Weekday names refer to the next occurrence after ``today``; using today's
    weekday therefore means seven days later.
    """
    value = text.strip()
    lowered = value.lower()

    if lowered == "tomorrow":
        return today + timedelta(days=1)

    match = _IN_DAYS.fullmatch(value)
    if match:
        return today + timedelta(days=int(match.group(1)))

    weekday = _WEEKDAYS.get(lowered)
    if weekday is not None:
        days_ahead = (weekday - today.weekday()) % 7 or 7
        return today + timedelta(days=days_ahead)

    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Unknown due date: {text!r}") from exc
