# Experiment discipline

Large grids are useful for exploration, but a final claim should usually come from a smaller paired comparison.

A practical sequence is:

1. freeze the corpus and labels;
2. record a lexical baseline;
3. add dense retrieval without changing chunking;
4. compare hybrid fusion against both components;
5. add reranking only after candidate retrieval is stable;
6. inspect query-level losses;
7. repeat the final comparison on a held-out query split.

If an expensive stage improves the mean while creating large regressions on a small query family, the raw per-query rows make that visible.
