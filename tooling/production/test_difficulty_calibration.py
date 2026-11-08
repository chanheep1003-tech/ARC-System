import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("difficulty_calibration_t", ROOT / "tooling/production/difficulty_calibration.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
REG = c.load_registry()


def blind(pairs):
    return [{"item_id": k, "difficulty": v} for k, v in pairs]


class CalibrationTests(unittest.TestCase):
    def test_registry_has_no_item_text_and_known_labels(self):
        for a in REG["anchors"]:
            self.assertIn(a["label"], REG["label_to_level"])
            self.assertNotIn("text", a)
            self.assertTrue(a["drive_id"])

    def test_insufficient_anchors_does_not_adjust(self):
        rep = c.calibrate(blind([("ANCHOR-MEGA3-08", "D3"), ("SOC-1", "D2")]), REG)
        self.assertEqual(rep["status"], "INSUFFICIENT_ANCHORS")
        self.assertFalse(rep["applied"])
        self.assertEqual(c.adjusted_level("D2", rep), 2.0)

    def test_lenient_solver_gets_offset(self):
        pairs = [("ANCHOR-MEGA3-08", "D3"), ("ANCHOR-MEGA4-13", "D3"), ("ANCHOR-MEGA3-25", "D3"), ("ANCHOR-MEGA3-14", "D3"),
                 ("ANCHOR-MEGA3-01", "D2"), ("ANCHOR-MEGA4-01", "D2"), ("S-1", "D2"), ("S-2", "D3")]
        rep = c.calibrate(blind(pairs), REG)
        self.assertEqual(rep["status"], "SOLVER_LENIENT")
        self.assertTrue(rep["applied"])
        self.assertGreater(rep["offset"], 0.5)
        self.assertGreater(c.adjusted_level("D3", rep), 3.0)
        dist = c.calibrated_distribution(blind(pairs), rep)
        self.assertEqual(dist["basis"], "CALIBRATED")

    def test_calibrated_solver_keeps_labels(self):
        pairs = [("ANCHOR-MEGA3-08", "D4"), ("ANCHOR-MEGA4-13", "D4"), ("ANCHOR-MEGA3-25", "D4"), ("ANCHOR-MEGA3-14", "D4"),
                 ("ANCHOR-MEGA3-01", "D2"), ("ANCHOR-MEGA4-01", "D2")]
        rep = c.calibrate(blind(pairs), REG)
        self.assertEqual(rep["status"], "CALIBRATED")

    def test_structure_solver_mismatch(self):
        rows = [{"item_id": "A", "band": "D4", "label": "D4"}, {"item_id": "B", "band": "D3", "label": "D3"}]
        out = c.structure_solver_mismatch(rows, blind([("A", "D3"), ("B", "D3")]))
        self.assertEqual([m["item_id"] for m in out], ["A"])


if __name__ == "__main__":
    unittest.main()
