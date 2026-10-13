def can_register_thesis(credits: int, gpa: float) -> bool:
    return credits >= 120 and gpa >= 2.0

def missing(credits: int, gpa: float) -> list[str]:
    verdict: list[str] = []
    if (credits < 120):
        verdict.append(f"need {120 - credits} more credits")
    if (gpa < 2.0):
        verdict.append(f"need {2.0 - gpa:.2f} more points")
    return verdict

    