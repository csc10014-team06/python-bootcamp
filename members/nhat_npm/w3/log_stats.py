"""Summarize request counts and latency percentiles from a chat log."""

from collections import Counter, defaultdict
from math import ceil
from typing import Iterable


def analyse(pairs: Iterable[tuple[str, float]]) -> dict[str, object]:
    """Return request counts, per-route p95 latency, and the slowest route.

    The p95 uses the nearest-rank method. If there are no requests, the counts
    and p95 mappings are empty and ``slowest`` is ``None``.
    """
    latencies: dict[str, list[float]] = defaultdict(list)
    counts: Counter[str] = Counter()

    for route, latency_ms in pairs:
        counts[route] += 1
        latencies[route].append(latency_ms)

    p95 = {
        route: sorted(route_latencies)[ceil(0.95 * len(route_latencies)) - 1]
        for route, route_latencies in latencies.items()
    }
    slowest = max(p95, key=p95.__getitem__) if p95 else None

    return {"counts": dict(counts), "p95": p95, "slowest": slowest}
