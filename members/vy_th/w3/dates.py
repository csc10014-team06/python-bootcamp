from datetime import date, timedelta


def parse_due(text: str, today: date) -> date:
    """Parse an ISO date or a relative due-date expression."""
    text = text.strip().lower()

    if text == "tomorrow":
        return today + timedelta(days=1)

    if text.startswith("in ") and text.endswith((" days", " day")):
        parts = text.split()
        n = int(parts[1])

        return today + timedelta(days=n)

    weekdays = {
        "mon": 0,
        "tue": 1,
        "wed": 2,
        "thu": 3,
        "fri": 4,
        "sat": 5,
        "sun": 6,
    }

    if text in weekdays:
        target = weekdays[text]
        days_ahead = (target - today.weekday()) % 7

        if days_ahead == 0:
            days_ahead = 7

        return today + timedelta(days=days_ahead)

    return date.fromisoformat(text)
