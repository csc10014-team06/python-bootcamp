import pytest


def test_grades_summary(load):
    g = load("w1", "grades")
    res = g.summary([-2.5, 4.0, 8.5])
    assert res == {"min": -2.5, "max": 8.5, "mean": 3.33, "median": 4.0}

    same = g.summary([7.0, 7.0, 7.0, 7.0])
    assert same == {"min": 7.0, "max": 7.0, "mean": 7.0, "median": 7.0}

    scale = g.summary([0.0, 10.0])
    assert scale == {"min": 0.0, "max": 10.0, "mean": 5.0, "median": 5.0}

    with pytest.raises(ValueError):
        g.summary([])


def test_word_count(load):
    t = load("w1", "text_tools")
    assert t.word_count("     ") == {}
    assert t.word_count("... !? :; ,. ---") == {}

    assert t.word_count("Hello, hello! HELLO?") == {"hello": 3}

    sample = "apple banana apple orange apple banana"
    assert t.top_k(sample, 0) == []
    assert t.top_k(sample, 10) == [("apple", 3), ("banana", 2), ("orange", 1)]

    ties = "cat bat bat cat ant"
    assert t.top_k(ties, 2) == [("bat", 2), ("cat", 2)]


def test_thesis(load):
    r = load("w1", "rules")
    assert r.can_register_thesis(120, 2.0)
    assert r.missing(120, 2.0) == []

    assert not r.can_register_thesis(119, 3.8)
    reasons_credit = " ".join(r.missing(119, 3.8)).lower()
    assert "1 more" in reasons_credit

    assert not r.can_register_thesis(130, 1.99)
    assert len(r.missing(130, 1.99)) == 1

    assert not r.can_register_thesis(80, 1.4)
    assert len(r.missing(80, 1.4)) == 2


def test_translate(load, variant):
    tr = load("w1", "translate")
    if variant == 1:
        arr = [-10, -5, 0, 7, 20]
        assert tr.binary_search(arr, -10) == 0
        assert tr.binary_search(arr, 20) == 4
        assert tr.binary_search(arr, 15) == -1
        assert tr.binary_search([], 0) == -1
    elif variant == 2:
        assert tr.insertion_sort([1, 2, 3]) == [1, 2, 3]
        assert tr.insertion_sort([9, 7, 5, 3]) == [3, 5, 7, 9]
        assert tr.insertion_sort([4, 2, 4, 1]) == [1, 2, 4, 4]
    elif variant == 3:
        assert tr.transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
        assert tr.transpose([[1, 2, 3]]) == [[1], [2], [3]]
        assert tr.transpose([[1], [2]]) == [[1, 2]]
    elif variant == 4:
        assert tr.primes_up_to(-10) == []
        assert tr.primes_up_to(0) == []
        assert tr.primes_up_to(1) == []
        assert tr.primes_up_to(2) == [2]
        assert tr.primes_up_to(3) == [2, 3]
        assert tr.primes_up_to(13) == [2, 3, 5, 7, 11, 13]
        assert tr.primes_up_to(25)[-1] == 23
    elif variant == 5:
        assert tr.gcd(35, 14) == 7
        assert tr.gcd(17, 19) == 1
        assert tr.gcd(0, 25) == 25
        assert tr.gcd(100, 100) == 100


def test_timetable(load):
    tt = load("w1", "timetable")
    raw_schedule = [
        ("Z999", "Fri"),
        ("A001", "Fri"),
        ("CSC10014", "Wed"),
        ("MTH00003", "Fri"),
    ]
    got = tt.by_day(raw_schedule)
    assert got.get("Fri") == ["A001", "MTH00003", "Z999"]
    assert got.get("Wed") == ["CSC10014"]
    assert tt.by_day([]) == {}