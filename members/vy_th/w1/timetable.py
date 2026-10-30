def by_day(courses: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group courses by weekday and sort each group."""
    result = {}

    for course, day in courses:
        result.setdefault(day, []).append(course)

    for day_courses in result.values():
        day_courses.sort()

    return result
