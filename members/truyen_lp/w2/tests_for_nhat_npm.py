import pytest

from members.nhat_npm.w1.grades import summary
from members.nhat_npm.w1.rules import can_register_thesis, missing
from members.nhat_npm.w1.text_tools import top_k, word_count
from members.nhat_npm.w1.timetable import by_day
from members.nhat_npm.w1.translate import binary_search


def test_nhat_summary_even_length_and_empty() -> None:
    res = summary([7.5, 9.0, 6.0, 8.0])
    assert res == {"min": 6.0, "max": 9.0, "mean": 7.62, "median": 7.75}

    single = summary([8.5])
    assert single == {"min": 8.5, "max": 8.5, "mean": 8.5, "median": 8.5}

    with pytest.raises(ValueError):
        summary([])


def test_nhat_word_count_and_top_k_ties() -> None:
    text = "Banana, apple! Banana: apple? Orange."
    counts = word_count(text)
    assert counts == {"banana": 2, "apple": 2, "orange": 1}

    ranked = top_k(text, 2)
    assert ranked == [("apple", 2), ("banana", 2)]
    assert top_k(text, 0) == []


def test_nhat_thesis_boundary_cases() -> None:
    assert can_register_thesis(120, 2.0) is True
    assert missing(120, 2.0) == []

    assert can_register_thesis(119, 2.0) is False
    assert missing(119, 2.0) == ["need 1 more credits"]

    assert can_register_thesis(120, 1.99) is False
    assert missing(120, 1.99) == ["need GPA of at least 2.0"]


def test_nhat_binary_search_edge_cases() -> None:
    assert binary_search([], 10) == -1
    assert binary_search([42], 42) == 0
    assert binary_search([42], 10) == -1

    arr = [10, 20, 30, 40, 50]
    assert binary_search(arr, 5) == -1
    assert binary_search(arr, 55) == -1
    assert binary_search(arr, 10) == 0
    assert binary_search(arr, 30) == 2
    assert binary_search(arr, 50) == 4


def test_nhat_by_day_sorting_and_multiple_days() -> None:
    assert by_day([]) == {}

    entries = [
        ("MATH101", "Mon"),
        ("COMP202", "Tue"),
        ("COMP101", "Mon"),
        ("PHYS101", "Tue"),
    ]
    result = by_day(entries)
    assert result == {
        "Mon": ["COMP101", "MATH101"],
        "Tue": ["COMP202", "PHYS101"],
    }
