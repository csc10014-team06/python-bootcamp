"""W1-2: Word counter."""

from collections import Counter

PUNCTUATION = ".,!?;:"


def word_count(text: str) -> dict[str, int]:
    """Count words in text, ignoring case and the punctuation .,!?;:"""
    cleaned = text.lower().translate(str.maketrans("", "", PUNCTUATION))
    return dict(Counter(cleaned.split()))


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return the k most common words, by count (descending) then alphabetically."""
    pairs = sorted(word_count(text).items(), key=lambda p: (-p[1], p[0]))
    return pairs[:k]
