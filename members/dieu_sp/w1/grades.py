"""W1-1: Grade summary."""

from statistics import median


def summary(scores: list[float]) -> dict:
    """Return min, max, mean and median of scores.

    Mean and median are rounded to 2 decimals. An empty list raises ValueError.
    """
    if not scores:
        raise ValueError("scores must not be empty")
    return {
        "min": min(scores),
        "max": max(scores),
        "mean": round(sum(scores) / len(scores), 2),
        "median": round(median(scores), 2),
    }
