def by_day(timetable: list[tuple[str, str]]) -> dict[str, list[str]]:
    res: dict[str, list[str]] = {}
    for course, day in timetable:
        res.setdefault(day, []).append(course)
    for day in res:
        res[day].sort()
    return res