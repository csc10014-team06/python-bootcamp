

def summary(score: list[float]) -> dict:
    if (score == []):
        raise ValueError()

    median = 0
    cnt = len(score)

    score.sort()

    if (len(score) % 2 == 0):
        median = (score[cnt//2 - 1] + score[cnt//2])/2
    else:
        median = score[cnt//2]
    
    result = {
        "min": min(score),
        "max": max(score),
        "mean": round(sum(score) / len(score), 2),
        "median": median
    }
    return result

my_dict = summary([7.5, 9, 6, 8])

print(my_dict["mean"])