def by_day(timetable: list[tuple[str, str]]) -> dict[str, list[str]]:

    result = {}
    
    for course, day in timetable:
        result.setdefault(day, []).append(course)

   
    for day in result:
        result[day].sort()

    return result