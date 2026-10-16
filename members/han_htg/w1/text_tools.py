def word_count(text: str) -> dict[str, int]:
    text = text.lower()
    for c in ".,!?;:":
        text = text.replace(c, "")

    counts: dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    counts = word_count(text)
    sorted_item = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return sorted_item[:k]