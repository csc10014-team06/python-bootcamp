"""W1-5: Group a timetable by day."""


def by_day(pairs: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group (course, day) pairs into {day: sorted list of courses}."""
    days: dict[str, list[str]] = {}
    for course, day in pairs:
        days.setdefault(day, []).append(course)
    return {day: sorted(courses) for day, courses in days.items()}
