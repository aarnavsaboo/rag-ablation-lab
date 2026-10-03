# Experiment methodology

The repository is organized around paired, reproducible RAG experiments rather than one-off demos.

## Experimental unit

A run is defined by a dataset revision and a concrete pipeline specification. The specification captures chunking, lexical and dense retrieval, fusion, query expansion, candidate depth, diversity selection, reranking, final top-k and evidence-budget choices.

The planner expands a configuration grid into explicit run records before execution. This keeps the experiment surface inspectable and makes it possible to rerun or split a matrix without changing the implementation.

## Artifact flow

```text
dataset + grid
      |
      v
concrete run specs
      |
      v
pipeline execution
      |
      +--> ranked document IDs
      +--> per-query metrics
      +--> stage timings
      |
      v
raw JSONL
      |
      +--> aggregate report
      +--> paired comparison
      +--> query-level regressions
```

Raw results are treated as the source of truth. Reports should be regenerated from those records instead of mutating the experiment output.

## Comparison rules

Pipeline variants are compared on the same query IDs. Aggregate changes are useful, but they are not sufficient: the report also keeps wins, ties, losses and the largest per-query regressions.

When changing more than one retrieval stage, create an intermediate experiment where possible. This keeps attribution clearer than comparing two configurations that differ everywhere.

## Reproducibility

For meaningful comparisons, keep constant:

- corpus and labelled query set
- experiment seed
- final evaluation cutoffs
- model revisions
- embedding/reranker versions
- runtime configuration

Local model and embedding results are machine-dependent. System metadata should stay attached to the run artifacts when results leave the original workstation.

## Extension points

New retrieval stages should expose deterministic inputs and outputs and should not write directly into reporting code. New metrics should operate on stored rankings so they can be recalculated without rerunning retrieval.
