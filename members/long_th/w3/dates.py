"""W3-1: Date parsing for the study planner.

Parses human-friendly date strings into ``datetime.date`` objects.
"""

import re
from datetime import date, timedelta


# Monday=0 … Sunday=6 — matching date.weekday()
_WEEKDAYS: dict[str, int] = {
    "mon": 0, "tue": 1, "wed": 2, "thu": 3,
    "fri": 4, "sat": 5, "sun": 6,
}


def parse_due(text: str, today: date) -> date:
    """Convert a human-readable due-date string to a ``date``.

    Supported formats:
    - ISO date: ``"2026-10-30"``
    - ``"tomorrow"``
    - ``"in N days"``  (e.g. ``"in 3 days"``)
    - Three-letter weekday name (e.g. ``"Fri"``), meaning the *next*
      occurrence (never today).

    Raises ``ValueError`` for anything else.
    """
    cleaned = text.strip().lower()

    # ISO date  (e.g. "2026-10-30")
    try:
        return date.fromisoformat(text.strip())
    except ValueError:
        pass

    # "tomorrow"
    if cleaned == "tomorrow":
        return today + timedelta(days=1)

    # "in N days"
    m = re.fullmatch(r"in\s+(\d+)\s+days?", cleaned)
    if m:
        return today + timedelta(days=int(m.group(1)))

    # Three-letter weekday name (next occurrence, not today)
    abbr = cleaned[:3]
    if abbr in _WEEKDAYS:
        target_wd = _WEEKDAYS[abbr]
        diff = (target_wd - today.weekday()) % 7
        if diff == 0:
            diff = 7  # next occurrence, not today
        return today + timedelta(days=diff)

    raise ValueError(f"Unknown date format: {text!r}")

