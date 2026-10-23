import pytest


def tests_for_han_htg_summary(load):
    g = load("w1", "grades")
    assert g.summary([7.521, 9.32, 6.12, 8.45]) == {"min": 6.12, "max": 9.32, "mean": 7.84, "median": 7.99}
    assert g.summary([5.678, 5.942, 5.401]) == {"min": 5.401, "max": 5.942, "mean": 5.673, "median": 5.678}
    assert g.summary([6.421]) == {"min": 6.421, "max": 6.421, "mean": 6.421, "median": 6.421}
    with pytest.raises(ValueError):
        g.summary([])


def tests_for_han_htg_word_count(load):
    t = load("w1", "text_tools")
    assert t.word_count("Data science is a interdisciplinary field.") == {"data": 1, "science": 1, "is": 1, "a": 1, "interdisciplinary": 1, "field": 1}
    assert t.top_k("Data science is a interdisciplinary field.", 2) == [("data", 1), ("science", 1)]
    assert t.top_k("Python is fun and Python is powerful.", 1) == [("python", 2)]
    assert t.top_k("Artificial intelligence AI is transforming the world.", 3) == [("ai", 2), ("artificial", 1), ("intelligence", 1)]
    assert t.top_k("AI is cool, AI is everywhere. AI is the future.", 3) == [("ai", 3), ("is", 3), ("cool", 1)]
    assert t.top_k("python python python Java Java JavaScript", 3) == [("python", 3), ("java", 2), ("javascript", 1)]
    assert t.top_k("", 3) == []

def tests_for_han_htg_thesis(load):
    r = load("w1", "rules")
    assert r.can_register_thesis(120, 2.0)
    assert r.can_register_thesis(119, 3.0)
    assert r.can_register_thesis(118, 3.1)
    assert not r.can_register_thesis(120, 1.5)
    assert not r.can_register_thesis(119, 2.0)
    assert not r.can_register_thesis(100, 1.5)
    assert r.missing(118, 3.1) == ["need 2 more credits"]
    assert r.missing(120, 2.0) == []
    assert len(r.missing(100, 1.5)) == 2

def tests_for_han_htg_translate(load, variant):
    tr = load("w1", "translate")
    if variant == 1:
        assert tr.binary_search([10, 20, 30, 40, 50], 30) == 2
        assert tr.binary_search([10, 20, 30, 40, 50], 45) == -1
        assert tr.binary_search([], 10) == -1
    elif variant == 2:
        assert tr.insertion_sort([12, 11, 13, 5, 6]) == [5, 6, 11, 12, 13]
        assert tr.insertion_sort([]) == []
    elif variant == 3:
        assert tr.transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
        assert tr.transpose([]) == []
    elif variant == 4:
        assert tr.primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        assert tr.primes_up_to(1) == []
    elif variant == 5:
        assert tr.gcd(99, 121) == 11
        assert tr.gcd(48, 18) == 6
        assert tr.gcd(7, 5) == 1
        assert tr.gcd(0, 7) == 7

def tests_for_han_htg_timetable(load):
    tt = load("w1", "timetable")
    assert tt.by_day([("ENG10001", "Wed"), ("CSC10022", "Thu"), ("CSC10022", "Mon"), ("CSC10018", "Mon")]) == {
    'Mon': ['CSC10018', 'CSC10022'],
    'Tue': [],
    'Wed': ['ENG10001'],
    'Thu': ['CSC10022'],
    'Fri': []
}
    assert tt.by_day([]) == {}