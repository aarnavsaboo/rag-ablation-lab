# rag-ablation-lab

A config-driven experiment harness for measuring which parts of a RAG pipeline actually help on a particular dataset.

The lab treats chunking, lexical retrieval, embeddings, rank fusion, query rewriting, candidate depth, diversity selection and reranking as independent variables. Each run produces per-query rankings and metrics, not just one aggregate score, so a more complicated configuration can be inspected for both wins and regressions.

The repository is built around ablation rather than demos: establish a baseline, change one factor, measure the delta, keep the queries where the change helped and the queries where it hurt.

## Experiment dimensions

- fixed-size vs sentence-aware chunking
- chunk size and overlap
- BM25 parameters
- embedding model
- lexical / dense / hybrid retrieval
- reciprocal-rank fusion weighting
- query expansion count
- HyDE-style generated search text
- candidate depth
- MMR selection
- cross-encoder reranking
- final top-k
- evidence budget

## Workflow

```text
corpus + labelled queries
          |
          v
     experiment grid
          |
          v
   concrete run specs
          |
          v
      pipeline runner
          |
          +--> rankings
          +--> per-query metrics
          +--> stage timings
          |
          v
       raw JSONL
          |
      +---+----------------+
      |                    |
      v                    v
aggregate metrics      paired deltas
                           |
                           v
                    win/loss queries
```

## Example

```bash
python -m rag_ablation_lab grid configs/grid.example.json > runs/plan.jsonl
python -m rag_ablation_lab run runs/plan.jsonl --dataset examples/dataset.json --out runs/results.jsonl
python -m rag_ablation_lab summarize runs/results.jsonl
python -m rag_ablation_lab compare runs/results.jsonl baseline-id experiment-id
```

## Paired comparison

Averages can hide where a pipeline regressed. The comparison layer pairs two experiments on query ID and reports:

- mean Recall@k delta
- mean MRR delta
- mean nDCG delta
- number of query wins/ties/losses
- bootstrap interval for the mean delta
- worst regressions by query ID
- largest improvements by query ID
- stage-time delta

The bootstrap implementation is intentionally small and deterministic from a seed.

## Failed experiments are first-class results

The lab does not assume query expansion, reranking or larger chunks are improvements. If a complex configuration loses to BM25, that result remains visible.

Useful RAG engineering often means removing a stage after measuring it.

## Repository layout

- `dataset.py` — labelled corpus/query format
- `grid.py` — experiment matrix expansion
- `retrievers.py` — small lexical baseline and pluggable interfaces
- `metrics.py` — Recall/MRR/nDCG
- `runner.py` — experiment execution
- `stats.py` — paired deltas and bootstrap intervals
- `report.py` — per-experiment summaries
- `configs/` — experiment grids
- `examples/` — tiny reproducible fixtures
- `tests/` — deterministic tests

Maintained by **Aarnav Saboo**.
