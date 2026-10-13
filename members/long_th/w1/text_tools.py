import re


def word_count(text: str) -> dict[str, int]:
    result: dict[str, int] = {}
    words = [word for word in re.split(r'\W+', text) if word]
    for word in words:
        word = word.lower()
        if (word in result):
            result[word] += 1
        else:
            result[word] = 1
    return result

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    word_dict = word_count(text)
    sorted_dict = sorted(word_dict.items(), key = lambda x: x[1], reverse = True)
    return sorted_dict[:k]



