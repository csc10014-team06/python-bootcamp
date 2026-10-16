def by_day(timetable: list[tuple[str, str]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for course, day in timetable:
        result.setdefault(day, []).append(course)
    for courses in result.values():
        courses.sort()
    return result
