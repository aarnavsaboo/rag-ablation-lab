# rag-ablation-lab

An experiment harness for asking a simple question: which parts of a RAG pipeline actually improve retrieval on a given corpus?

The runner treats chunking, retrieval, fusion, query expansion and reranking as independent factors. Experiments are written to JSONL with enough configuration to reproduce each run, then compared with Recall@k, MRR and nDCG rather than a single hand-picked example.

## Experiments

- lexical vs dense vs hybrid retrieval
- reciprocal-rank fusion weight sweeps
- fixed-size vs sentence-aware chunking
- query expansion and HyDE-style synthetic queries
- MMR diversity after retrieval
- optional cross-encoder reranking
- chunk-size and overlap grids
- bootstrap deltas between two runs

```bash
python -m rag_ablation_lab grid configs/grid.example.json
python -m rag_ablation_lab compare results/baseline.jsonl results/hybrid.jsonl
```

The repository is intentionally comfortable with null results. A more complicated pipeline that loses to BM25 on the labelled queries should be recorded as a loss, not tuned away.

Maintained by **Aarnav Saboo**.
