from collections import Counter, defaultdict
import math
from typing import Any


def analyse(pairs: list[tuple[str, float | int]]) -> dict[str, Any]:
    """Calculate request counts, p95 latency, and the slowest route."""
    if not pairs:
        return {"counts": Counter(), "p95": {}, "slowest": None}

    counts: Counter[str] = Counter()
    by_route: dict[str, list[float]] = defaultdict(list)

    for route, latency in pairs:
        counts[route] += 1
        by_route[route].append(float(latency))

    p95: dict[str, float] = {}
    for route, latencies in by_route.items():
        sorted_lats = sorted(latencies)
        idx = max(0, math.ceil(0.95 * len(sorted_lats)) - 1)
        p95[route] = sorted_lats[idx]

    slowest = max(p95, key=lambda r: p95[r])

    return {
        "counts": counts,
        "p95": p95,
        "slowest": slowest,
    }