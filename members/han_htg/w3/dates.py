from datetime import date, timedelta
import re

WEEKDAYS: dict[str, int] = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}


def parse_due(text: str, today: date) -> date:
    """Parse a human-readable due date string relative to a base date."""
    clean = text.strip().lower()
    if not clean:
        raise ValueError("Due date cannot be empty")

    if clean == "tomorrow":
        return today + timedelta(days=1)

    match = re.match(r"^in\s+(\d+)\s+days?$", clean)
    if match:
        return today + timedelta(days=int(match.group(1)))

    if clean in WEEKDAYS:
        target_wd = WEEKDAYS[clean]
        days_ahead = (target_wd - today.weekday()) % 7
        return today + timedelta(days=7 if days_ahead == 0 else days_ahead)

    try:
        return date.fromisoformat(text.strip())
    except ValueError as err:
        raise ValueError(f"Unknown due date format: {text!r}") from err