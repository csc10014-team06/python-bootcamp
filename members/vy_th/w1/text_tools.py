def word_count(text: str) -> dict[str, int]:
    text = text.lower()
    for c in ".,!?;:":
        text = text.replace(c, " ")

    words = text.split()
    
    counts = {}
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    counts = word_count(text)
    items = list(counts.items())

    items.sort(key=lambda x: (-x[1], x[0]))

    return items[:k]
