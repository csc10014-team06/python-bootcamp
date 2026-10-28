"""W3-2: Chat log analysis for route latency statistics."""

from collections import Counter, defaultdict
import math
from typing import Any, Sequence


def analyse(pairs: Sequence[tuple[str, float | int]]) -> dict[str, Any]:
    """Analyze request counts and p95 latency per route from (route, latency_ms) pairs.

    Args:
        pairs: A sequence of (route, latency_ms) tuples.

    Returns:
        dict containing:
        - "counts": Counter of requests per route
        - "p95": dict mapping route to its 95th percentile latency
        - "slowest": the route with the highest p95 latency (or None if empty)
    """
    counts: Counter[str] = Counter()
    grouped: dict[str, list[float | int]] = defaultdict(list)

    for route, latency in pairs:
        counts[route] += 1
        grouped[route].append(latency)

    p95: dict[str, float | int] = {}
    for route, latencies in grouped.items():
        sorted_lats = sorted(latencies)
        idx = max(0, math.ceil(0.95 * len(sorted_lats)) - 1)
        p95[route] = sorted_lats[idx]

    slowest = max(p95, key=lambda k: p95[k]) if p95 else None

    return {
        "counts": counts,
        "p95": p95,
        "slowest": slowest,
    }
