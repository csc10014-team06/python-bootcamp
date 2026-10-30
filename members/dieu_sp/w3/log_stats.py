"""W3-2: Request counts and p95 latency per route from (route, ms) pairs."""

import math
from collections import Counter, defaultdict


def p95(values: list[float]) -> float:
    """Return the 95th percentile of values using the nearest-rank method."""
    ordered = sorted(values)
    return ordered[math.ceil(0.95 * len(ordered)) - 1]


def analyse(pairs: list[tuple[str, float]]) -> dict:
    """Summarise (route, latency_ms) pairs.

    Returns {"counts": requests per route, "p95": 95th percentile latency per
    route, "slowest": the route with the highest p95}. Empty input raises ValueError.
    """
    if not pairs:
        raise ValueError("pairs must not be empty")

    latencies: dict[str, list[float]] = defaultdict(list)
    for route, ms in pairs:
        latencies[route].append(ms)

    p95s = {route: p95(ms) for route, ms in latencies.items()}
    return {
        "counts": dict(Counter(route for route, _ in pairs)),
        "p95": p95s,
        "slowest": max(p95s, key=lambda route: p95s[route]),
    }
