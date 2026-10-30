
def by_day(items: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group course names by day and sort each day's courses."""
    timetable = {}

    for course, day in items:
        timetable.setdefault(day, []).append(course)

    for courses in timetable.values():
        courses.sort()

    return timetable
