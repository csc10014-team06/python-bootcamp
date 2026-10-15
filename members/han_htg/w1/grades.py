def summary(scores: list[float]) -> dict:
    if not scores:
        raise ValueError("Scores list is empty!")
    s = sorted(scores)
    n = len(s)

    minVal = s[0]
    maxVal = s[n - 1]
    meanVal = sum(s) / n

    if n % 2 == 0:
        medianVal = (s[n//2 - 1] +s[n//2]) / 2
    else:
        medianVal = s[n//2]

    return {
        "min": minVal,
        "max": maxVal,
        "mean": round(meanVal, 2),
        "median": round(medianVal, 2)
    }

print(summary([1.4, 2, 5, 2.5]))