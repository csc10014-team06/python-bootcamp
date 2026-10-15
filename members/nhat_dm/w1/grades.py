import statistics
def summary(score:list[float]) -> dict:
    if not score: 
        raise ValueError("the list of scores cannot be empty")
    else:
        return {
            "min":min(score),
            "max":max(score),
            "mean":round(statistics.mean(score),2),
            "median":round(statistics.median(score),2),
        }