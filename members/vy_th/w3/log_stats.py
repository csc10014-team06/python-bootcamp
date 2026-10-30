from collections import Counter, defaultdict
from math import ceil

def analyse(pairs: list[tuple[str, float]]) -> dict:
    """Analyse request counts and p95 latency for each route."""
    counts = Counter()
    latencies = defaultdict(list)

    for route, latency_ms in pairs:
        counts[route] += 1
        latencies[route].append(latency_ms)

    p95 = {}

    for route, values in latencies.items():
        values.sort()
        index = ceil(0.95 * len(values)) - 1
        p95[route] = values[index]

    slowest = max(p95, key=lambda route: p95[route]) if p95 else None

    return {
        "counts": dict(counts),
        "p95": p95,
        "slowest": slowest,
    }
