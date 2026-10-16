def can_register_thesis(credits: int, gpa: float) -> bool:
    if credits >= 120 and gpa >= 2.0:
        return True

    return False

def missing(credits, gpa) -> list[str]:
    result = []

    if credits < 120:
        result.append(f"need {120 - credits} more credits")

    if gpa < 2.0:
        result.append("GPA must be at least 2.0")

    return result
