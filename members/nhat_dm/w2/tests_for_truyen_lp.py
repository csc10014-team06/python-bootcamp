"""W2-4: Pytest suite testing a teammate's Week 1 functions (including edge cases)."""

import pytest

from members.truyen_lp.w1.grades import summary
from members.truyen_lp.w1.rules import can_register_thesis, missing
from members.truyen_lp.w1.text_tools import top_k, word_count
from members.truyen_lp.w1.timetable import by_day


def test_summary_even_and_rounding() -> None:
    """Test W1-1 summary with decimals requiring rounding to 2 decimal places."""
    result = summary([7.5, 9.0, 6.0, 8.0])
    assert result == {"min": 6.0, "max": 9.0, "mean": 7.62, "median": 7.75}


def test_summary_empty_raises() -> None:
    """Test W1-1 summary raises ValueError on empty input."""
    with pytest.raises(ValueError):
        summary([])


def test_top_k_tie_breaking_and_punctuation_only() -> None:
    """Edge case for W1-2: ties broken alphabetically & string with only punctuation."""
    # Khi số lần xuất hiện bằng nhau, phải sắp xếp theo thứ tự bảng chữ cái
    text = "beta! alpha? beta, alpha."
    assert top_k(text, 2) == [("alpha", 2), ("beta", 2)]
    # Edge case: chuỗi chỉ toàn dấu câu, không có từ nào
    assert word_count("...,,,!?;:") == {}
    assert top_k("...,,,!?;:", 3) == []


def test_thesis_eligibility_exact_boundary() -> None:
    """Edge case for W1-3: exact boundary values credits=120 and gpa=2.0."""
    assert can_register_thesis(120, 2.0) is True
    assert missing(120, 2.0) == []
    assert can_register_thesis(119, 1.99) is False
    reasons = missing(119, 1.99)
    assert len(reasons) == 2


def test_timetable_grouped_and_sorted() -> None:
    """Test W1-5 by_day sorts courses alphabetically per day."""
    schedule = [
        ("CSC10014", "Mon"),
        ("MTH00003", "Tue"),
        ("CSC10001", "Mon"),
    ]
    assert by_day(schedule) == {
        "Mon": ["CSC10001", "CSC10014"],
        "Tue": ["MTH00003"],
    }