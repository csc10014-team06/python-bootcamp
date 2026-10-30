
def can_register_thesis(credits: int, gpa: float) -> bool:
    """Return whether the credit and GPA requirements are both met."""
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """Describe the thesis registration requirements that are not met."""
    reasons = []

    if credits < 120:
        reasons.append(f"need {120 - credits} more credits")

    if gpa < 2.0:
        reasons.append("need GPA of at least 2.0")

    return reasons
