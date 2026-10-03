from __future__ import annotations

from random import Random


def bootstrap_mean_interval(
    values: list[float],
    *,
    samples: int = 2000,
    confidence: float = .95,
    seed: int = 17,
) -> tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    rng = Random(seed)
    means = []
    n = len(values)
    for _ in range(samples):
        draw = [values[rng.randrange(n)] for _ in range(n)]
        means.append(sum(draw) / n)
    means.sort()
    alpha = (1 - confidence) / 2
    lo = means[min(len(means)-1, int(alpha * len(means)))]
    hi = means[min(len(means)-1, int((1-alpha) * len(means)))]
    return lo, hi


def paired_records(left: list[dict], right: list[dict], metric: str) -> dict:
    l = {x["query_id"]: x for x in left}
    r = {x["query_id"]: x for x in right}
    keys = sorted(set(l) & set(r))
    deltas = [float(r[k]["metrics"][metric]) - float(l[k]["metrics"][metric]) for k in keys]
    interval = bootstrap_mean_interval(deltas)
    ranked = sorted(zip(keys, deltas), key=lambda x:x[1])
    return {
        "pairs": len(keys),
        "mean_delta": 0.0 if not deltas else sum(deltas)/len(deltas),
        "bootstrap_95": interval,
        "wins": sum(x > 0 for x in deltas),
        "ties": sum(x == 0 for x in deltas),
        "losses": sum(x < 0 for x in deltas),
        "largest_regressions": ranked[:5],
        "largest_improvements": list(reversed(ranked[-5:])),
    }
