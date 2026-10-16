
def by_day(items: list[tuple[str, str]]) -> dict[str, list[str]]:
    timetable = {}

    for course, day in items:
        timetable.setdefault(day, []).append(course)

    for day in timetable:
        timetable[day].sort()

    return timetable
