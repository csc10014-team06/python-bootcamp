"""W1-3: Thesis registration eligibility."""

MIN_CREDITS = 120
MIN_GPA = 2.0


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Return True if credits >= 120 and gpa >= 2.0."""
    return credits >= MIN_CREDITS and gpa >= MIN_GPA


def missing(credits: int, gpa: float) -> list[str]:
    """Return readable reasons the student cannot register (empty if eligible)."""
    reasons: list[str] = []
    if credits < MIN_CREDITS:
        reasons.append(f"need {MIN_CREDITS - credits} more credits")
    if gpa < MIN_GPA:
        reasons.append(f"GPA {gpa} is below {MIN_GPA}")
    return reasons
