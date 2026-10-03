from math import log2


def recall_at_k(ranked: list[str], relevant: set[str], k: int) -> float:
    if not relevant:
        return 0.0
    return len(set(ranked[:k]) & relevant) / len(relevant)


def reciprocal_rank(ranked: list[str], relevant: set[str], k: int) -> float:
    for i, item in enumerate(ranked[:k], 1):
        if item in relevant:
            return 1.0 / i
    return 0.0


def ndcg_at_k(ranked: list[str], relevant: set[str], k: int) -> float:
    dcg = sum((1.0 / log2(i + 1)) for i, x in enumerate(ranked[:k], 1) if x in relevant)
    ideal_hits = min(k, len(relevant))
    idcg = sum(1.0 / log2(i + 1) for i in range(1, ideal_hits + 1))
    return 0.0 if idcg == 0 else dcg / idcg


def aggregate(rows: list[tuple[list[str], set[str]]], k: int = 10) -> dict[str, float]:
    if not rows:
        return {"recall": 0.0, "mrr": 0.0, "ndcg": 0.0}
    values = [
        (recall_at_k(r, rel, k), reciprocal_rank(r, rel, k), ndcg_at_k(r, rel, k))
        for r, rel in rows
    ]
    n = len(values)
    return {
        "recall": sum(x[0] for x in values) / n,
        "mrr": sum(x[1] for x in values) / n,
        "ndcg": sum(x[2] for x in values) / n,
    }
