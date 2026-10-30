"""W3-2: Chat log analysis.

Analyses ``(route, latency_ms)`` pairs and returns counts, p95 latency per
route, and the route with the highest p95.
"""

import math
from collections import Counter, defaultdict


def analyse(pairs: list[tuple[str, int]]) -> dict:
    """Analyse a list of ``(route, latency_ms)`` pairs.

    Returns a dict with three keys:

    - ``"counts"``: ``dict[str, int]`` — number of requests per route
      (a ``Counter``).
    - ``"p95"``: ``dict[str, int | float]`` — 95th-percentile latency for
      each route.
    - ``"slowest"``: ``str`` — the route with the highest p95 latency.
    """
    counts: Counter[str] = Counter()
    latencies: dict[str, list[int]] = defaultdict(list)

    for route, latency_ms in pairs:
        counts[route] += 1
        latencies[route].append(latency_ms)

    p95: dict[str, int | float] = {}
    for route, values in latencies.items():
        values_sorted = sorted(values)
        n = len(values_sorted)
        idx = math.ceil(0.95 * n) - 1  # 0-based index
        p95[route] = values_sorted[idx]

    slowest = max(p95, key=lambda r: p95[r])

    return {
        "counts": dict(counts),
        "p95": p95,
        "slowest": slowest,
    }

