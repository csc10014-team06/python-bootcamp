
def word_count(text: str) -> dict[str, int]:
    """Count words after lowercasing text and removing basic punctuation."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", ".,!?;:"))
    words = text.split()

    cnt = {}

    for word in words:
        if word in cnt:
            cnt[word] += 1
        else:
            cnt[word] = 1

    return cnt


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return up to ``k`` words ordered by count and then alphabetically."""
    if k <= 0:
        return []

    cnt = word_count(text)
    items = sorted(cnt.items(), key=lambda item: (-item[1], item[0]))

    return items[:k]
