import unittest
from rag_ablation_lab.metrics import recall_at_k, reciprocal_rank, ndcg_at_k
from rag_ablation_lab.grid import expand_grid


class Tests(unittest.TestCase):
    def test_metrics(self):
        ranked = ["b", "a", "c"]
        relevant = {"a", "c"}
        self.assertEqual(recall_at_k(ranked, relevant, 2), 0.5)
        self.assertEqual(reciprocal_rank(ranked, relevant, 3), 0.5)
        self.assertGreater(ndcg_at_k(ranked, relevant, 3), 0)

    def test_grid(self):
        cfg = dict(retriever=["bm25","dense"], chunk_size=512, overlap=64, top_k=5,
                   fusion_alpha=0.5, query_mode="raw", reranker="none")
        self.assertEqual(len(expand_grid(cfg)), 2)


if __name__ == "__main__":
    unittest.main()
