
from collections.abc import Callable
from types import ModuleType


def test_w1_1_summary_edge_case(load: Callable[[str, str], ModuleType]) -> None:
    """Check that equal grades produce the expected summary."""
    g = load("w1", "grades")

    # EDGE CASE: All scores are identical.
    assert g.summary([4, 4, 4, 4]) == {
        "min": 4,
        "max": 4,
        "mean": 4,
        "median": 4,
    }


def test_w1_2_word_count_edge_case(load: Callable[[str, str], ModuleType]) -> None:
    """Check that punctuation-only text contains no words."""
    t = load("w1", "text_tools")

    # EDGE CASE: Punctuation-only input contains no words.
    assert t.word_count("... !!! , ; ?") == {}
    assert t.top_k("... !!! , ; ?", 3) == []


def test_w1_3_thesis_edge_case(load: Callable[[str, str], ModuleType]) -> None:
    """Check that a low GPA prevents thesis registration."""
    r = load("w1", "rules")

    # EDGE CASE: Enough credits, but GPA is below the threshold.
    credits = 120
    gpa = 1.99

    assert not r.can_register_thesis(credits, gpa)
    assert r.missing(credits, gpa) == [
        f"GPA {gpa:.2f} is below 2.0"
    ]


def test_w1_4_bubble_sort(load: Callable[[str, str], ModuleType]) -> None:
    """Check bubble sort on ordinary, empty, and repeated-value inputs."""
    tr = load("w1", "translate")

    assert tr.bubble_sort([3, 1, 2]) == [1, 2, 3]
    assert tr.bubble_sort([1, 2, 3]) == [1, 2, 3]
    assert tr.bubble_sort([3, 2, 1]) == [1, 2, 3]

    # EDGE CASE: Empty input.
    assert tr.bubble_sort([]) == []

    # EDGE CASE: A single element needs no swaps.
    assert tr.bubble_sort([42]) == [42]

    assert tr.bubble_sort([5, 5, 2, 2, 1]) == [1, 2, 2, 5, 5]

    # EDGE CASE: Sorting must not lose or duplicate repeated values.
    values = [4, 1, 4, 2, 1]
    result = tr.bubble_sort(values)
    assert result == [1, 1, 2, 4, 4]
    assert sorted(result) == sorted(values)


def test_w1_5_timetable_edge_case(load: Callable[[str, str], ModuleType]) -> None:
    """Check grouping when a course appears on more than one day."""
    tt = load("w1", "timetable")

    # EDGE CASE: The same course appears on different days.
    assert tt.by_day([
        ("CSC10014", "Tue"),
        ("CSC10014", "Mon"),
        ("CSC10001", "Tue"),
    ]) == {
        "Tue": ["CSC10001", "CSC10014"],
        "Mon": ["CSC10014"],
    }
