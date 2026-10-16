

def summary(score: list[float]) -> dict:
    if (score == []):
        raise ValueError()

    cnt = len(score)

    scores = sorted(score)

    if (cnt % 2 == 0):
        median = (scores[cnt//2 - 1] + scores[cnt//2])/2
    else:
        median = scores[cnt//2]
    
    result = {
        "min": min(score),
        "max": max(score),
        "mean": round(sum(score) / len(score), 2),
        "median": round(median, 2)
    }
    return result