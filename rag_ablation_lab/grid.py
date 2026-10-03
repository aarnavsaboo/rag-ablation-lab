from dataclasses import dataclass, asdict
from hashlib import sha1
from itertools import product
import json


@dataclass(frozen=True)
class Experiment:
    retriever: str
    chunk_size: int
    overlap: int
    top_k: int
    fusion_alpha: float
    query_mode: str
    reranker: str

    @property
    def id(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True).encode()
        return sha1(payload).hexdigest()[:12]


def expand_grid(config: dict) -> list[Experiment]:
    keys = ["retriever", "chunk_size", "overlap", "top_k", "fusion_alpha", "query_mode", "reranker"]
    values = [config[k] if isinstance(config[k], list) else [config[k]] for k in keys]
    return [Experiment(**dict(zip(keys, combo))) for combo in product(*values)]


def paired_delta(left: list[float], right: list[float]) -> dict[str, float]:
    if len(left) != len(right) or not left:
        raise ValueError("paired runs must have the same non-zero length")
    deltas = [b - a for a, b in zip(left, right)]
    ordered = sorted(deltas)
    return {
        "mean_delta": sum(deltas) / len(deltas),
        "median_delta": ordered[len(ordered) // 2],
        "wins": sum(x > 0 for x in deltas),
        "ties": sum(x == 0 for x in deltas),
        "losses": sum(x < 0 for x in deltas),
    }
