def can_register_thesis(credits: int, gpa: float) -> bool:
    """Check whether a student meets thesis registration requirements."""
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """List the requirements missing for thesis registration."""
    result = []

    if credits < 120:
        result.append(f"need {120 - credits} more credits")

    if gpa < 2.0:
        result.append("GPA must be at least 2.0")

    return result
