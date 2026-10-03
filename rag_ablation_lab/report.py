from collections import defaultdict
from statistics import median


def summarize(rows: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        groups[row["experiment_id"]].append(row)

    output = []
    for experiment_id, group in sorted(groups.items()):
        output.append({
            "experiment_id": experiment_id,
            "queries": len(group),
            "recall": sum(x["metrics"]["recall"] for x in group) / len(group),
            "mrr": sum(x["metrics"]["mrr"] for x in group) / len(group),
            "ndcg": sum(x["metrics"]["ndcg"] for x in group) / len(group),
            "median_retrieval_ms": median(x["timing_ms"]["retrieval"] for x in group),
            "config": group[0]["config"],
        })
    return output
