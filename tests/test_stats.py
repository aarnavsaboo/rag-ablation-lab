import unittest

from rag_ablation_lab.stats import bootstrap_mean_interval, paired_records


class Tests(unittest.TestCase):
    def test_bootstrap_is_ordered(self):
        lo, hi = bootstrap_mean_interval([1,2,3], samples=200, seed=1)
        self.assertLessEqual(lo, hi)

    def test_paired(self):
        left = [{"query_id":"q1","metrics":{"ndcg":.2}}]
        right = [{"query_id":"q1","metrics":{"ndcg":.7}}]
        out = paired_records(left,right,"ndcg")
        self.assertAlmostEqual(out["mean_delta"], .5)


if __name__ == "__main__":
    unittest.main()
