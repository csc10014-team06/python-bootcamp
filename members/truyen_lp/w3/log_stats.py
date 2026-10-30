"""W3-2: Chat log analysis for request counts and p95 latency."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from collections.abc import Sequence
from typing import Any


def analyse(pairs: Sequence[tuple[str, float | int]]) -> dict[str, Any]:
    """Calculate request counts, p95 latency per route, and the slowest route.

    Args:
        pairs: Sequence of (route, latency_ms) tuples.

    Returns:
        dict containing:
        - "counts": Counter of requests per route
        - "p95": dict mapping route to its 95th percentile latency
        - "slowest": the route name with the highest p95 latency
    """
    if not pairs:
        return {
            "counts": Counter(),
            "p95": {},
            "slowest": None,
        }

    counts: Counter[str] = Counter()
    by_route: dict[str, list[float | int]] = defaultdict(list)

    for route, latency in pairs:
        counts[route] += 1
        by_route[route].append(latency)

    p95: dict[str, float | int] = {}
    for route, latencies in by_route.items():
        sorted_lats = sorted(latencies)
        idx = max(0, math.ceil(0.95 * len(sorted_lats)) - 1)
        p95[route] = sorted_lats[idx]

    slowest = max(p95, key=lambda r: p95[r]) if p95 else None

    return {
        "counts": counts,
        "p95": p95,
        "slowest": slowest,
    }
