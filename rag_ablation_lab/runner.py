from __future__ import annotations

from time import perf_counter

from .dataset import Dataset
from .grid import Experiment
from .metrics import recall_at_k, reciprocal_rank, ndcg_at_k
from .retrievers import BM25Retriever


def run_experiment(dataset: Dataset, experiment: Experiment) -> list[dict]:
    # The built-in executable baseline is lexical. Other strategy names remain
    # explicit experiment dimensions so optional adapters can be added without
    # changing the result format.
    if experiment.retriever not in {"bm25", "lexical"}:
        raise NotImplementedError(
            f"{experiment.retriever} requires an external adapter; use bm25 for the built-in baseline"
        )

    retriever = BM25Retriever(dataset.documents)
    rows = []
    for query in dataset.queries:
        started = perf_counter()
        ranking = retriever.search(query.text, experiment.top_k)
        elapsed = (perf_counter() - started) * 1000
        relevant = set(query.relevant)
        rows.append({
            "experiment_id": experiment.id,
            "query_id": query.id,
            "ranking": ranking,
            "metrics": {
                "recall": recall_at_k(ranking, relevant, experiment.top_k),
                "mrr": reciprocal_rank(ranking, relevant, experiment.top_k),
                "ndcg": ndcg_at_k(ranking, relevant, experiment.top_k),
            },
            "timing_ms": {"retrieval": elapsed},
            "config": experiment.__dict__,
        })
    return rows
