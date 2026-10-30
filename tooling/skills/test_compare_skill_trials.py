import unittest
from compare_skill_trials import compare


class CompareTests(unittest.TestCase):
    def test_pairs_missing_and_pending(self):
        base = [{"id": "a", "status": "FAIL"}, {"id": "b", "status": "NOT_RUN"},
                {"id": "old", "status": "PASS"}]
        candidate = [{"id": "a", "status": "PASS"}, {"id": "b", "status": "PASS"},
                     {"id": "new", "status": "PASS"}]
        result = compare(base, candidate)
        self.assertEqual(result["paired_evaluated_count"], 1)
        self.assertEqual(result["unevaluated"], ["b"])
        self.assertEqual(result["baseline_only"], ["old"])
        self.assertEqual(result["candidate_only"], ["new"])
        self.assertEqual(result["changes"], [{"id": "a", "baseline": "FAIL", "candidate": "PASS"}])

    def test_rejects_duplicates_and_invalid_status(self):
        with self.assertRaises(ValueError):
            compare([{"id": "x", "status": "PASS"}, {"id": "x", "status": "PASS"}], [])
        with self.assertRaises(ValueError):
            compare([{"id": "x", "status": "MAYBE"}], [])
        with self.assertRaises(ValueError):
            compare([{"id": "", "status": "PASS"}], [])


if __name__ == "__main__":
    unittest.main()
