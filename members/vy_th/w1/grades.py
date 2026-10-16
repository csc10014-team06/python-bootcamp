def mean(scores: list[float]):
    total = 0;
    for i in range(len(scores)):
        total += scores[i]

    return round(total / len(scores), 2)

def median(scores: list[float]):
    scores = sorted(scores)
    if len(scores) % 2 == 1:
        result = scores[len(scores) // 2]
    else:
        result = (scores[len(scores) // 2 - 1] + scores[len(scores) // 2]) / 2

    return round(result, 2)

def summary(scores: list[float]) -> dict:
    if scores:
        return{"min": min(scores), "max": max(scores), "mean": mean(scores), "median": median(scores)}
    else:
        raise ValueError("Scores cannot be empty")
