"""W1-2: Text processing tools for word counting and ranking."""


def word_count(text: str) -> dict[str, int]:
    """Count occurrences of each word in text, case-insensitive, ignoring punctuation."""
    text = text.lower()
    punctuations = ".,!?;:"
    for p in punctuations:
        text = text.replace(p, "")

    words = text.split()
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1

    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return top k words sorted by frequency (descending) and alphabetically."""
    counts = word_count(text)
    sorted_words = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return sorted_words[:k]
