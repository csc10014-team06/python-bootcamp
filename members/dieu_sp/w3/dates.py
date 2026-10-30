"""W3-1: Parse a due date written as an ISO date, a relative day or a weekday."""

import re
from datetime import date, timedelta

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
IN_N_DAYS = re.compile(r"in (\d+) days?")


def parse_due(text: str, today: date) -> date:
    """Return the date that text refers to, counted from today.

    Accepts "YYYY-MM-DD", "today", "tomorrow", "in N days" and weekday names
    such as "Fri" or "friday". A weekday means its next occurrence, so the same
    weekday as today is one week later. Anything else raises ValueError.
    """
    s = text.strip().lower()
    if s == "today":
        return today
    if s == "tomorrow":
        return today + timedelta(days=1)

    m = IN_N_DAYS.fullmatch(s)
    if m:
        return today + timedelta(days=int(m.group(1)))

    for i, name in enumerate(WEEKDAYS):
        if s in (name, name[:3]):
            return today + timedelta(days=(i - today.weekday() - 1) % 7 + 1)

    try:
        return date.fromisoformat(s)
    except ValueError:
        raise ValueError(f"Unrecognised due date: {text!r}") from None
