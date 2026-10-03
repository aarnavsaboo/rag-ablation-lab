# Experiment notes

Ablations are most useful when only one factor moves at a time. Large Cartesian grids are convenient for exploration but poor explanations by themselves.

Recommended workflow:

1. freeze a labelled query set before tuning;
2. establish lexical and dense baselines;
3. change one retrieval component;
4. keep raw per-query rankings;
5. inspect wins and losses, not only the mean;
6. run the final configuration on a held-out query set.

Query expansion, reranking and larger chunks can all reduce quality. The project treats those outcomes as useful observations rather than implementation failures.
