def summary(scores: list[float]) -> dict:
    if len(scores) == 0:
        raise ValueError("scores is not valid")
    ordered = sorted(scores)
    n = len(ordered)

    mn = ordered[0]
    mx = ordered[n-1]
    mean = round(sum(ordered) / n, 2)

    mid = n // 2

    if n % 2 == 1:
        med = ordered[mid]
    else:
        med = (ordered[mid-1] + ordered[mid]) / 2

    med = round(med, 2)

    return {
        "min": mn,
        "max": mx,
        "mean": mean,
        "median": med
    }
