import pytest


def test_summary(load):
    g = load("w1", "grades")
    assert g.summary([1, 2, 2]) == {"min": 1, "max": 2, "mean": 1.67, "median": 2}
    assert g.summary([3, 1, 4, 2])["median"] == 2.5
    with pytest.raises(ValueError):
        g.summary([])


def test_word_count(load):
    t = load("w1", "text_tools")
    assert t.word_count("Hi, hi! HI?") == {"hi": 3}
    assert t.word_count("... !!! ;") == {}  # edge case: only punctuation
    assert t.top_k("b a b", 10) == [("b", 2), ("a", 1)]


def test_thesis(load):
    r = load("w1", "rules")
    assert not r.can_register_thesis(130, 1.9)
    assert not r.can_register_thesis(119, 4.0)
    assert r.missing(119, 4.0) == ["need 1 more credits"]


def test_binary_search(load):
    tr = load("w1", "translate")
    assert tr.binary_search([1, 3, 5, 7, 9], 1) == 0
    assert tr.binary_search([1, 3, 5, 7, 9], 9) == 4
    assert tr.binary_search([1, 3, 5, 7, 9], 10) == -1  # edge case: key bigger than all
    assert tr.binary_search([4], 4) == 0


def test_by_day(load):
    tt = load("w1", "timetable")
    got = tt.by_day([("MTH00003", "Wed"), ("CSC10014", "Mon"), ("CSC10014", "Wed")])
    assert got == {"Wed": ["CSC10014", "MTH00003"], "Mon": ["CSC10014"]}
