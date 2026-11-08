#!/usr/bin/env python3
"""ARC_N layout decisions of 2026-11-08: difficulty strip, fixed slots, B/W logo release blocker."""
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pre = load("arc_pdf_preflight_n", "tooling/pdf_qc/pdf_preflight.py")
gw = load("arc_gateway_n", "tooling/typeset/typesetter_gateway.py")
rend = load("arc_kor_renderer_n", "tooling/typeset/kor_renderer.py")


def make_pdf(path, problem_lines, answer_lines):
    doc = fitz.open()
    cover = doc.new_page(width=595, height=842); cover.insert_text((72, 100), "ARC N cover")
    doc.new_page(width=595, height=842)  # blank verso
    prob = doc.new_page(width=595, height=842)
    y = 90
    for line in problem_lines:
        prob.insert_text((60, y), line, fontsize=10, fontname="korea"); y += 24
    doc.new_page(width=595, height=842)  # blank separator
    ans = doc.new_page(width=595, height=842)
    y = 90
    for line in answer_lines:
        ans.insert_text((60, y), line, fontsize=10, fontname="korea"); y += 16
    doc.save(path)


def codes(result):
    return {f["type"] for p in result["pages"] for f in p["flags"]}


class PreflightRules(unittest.TestCase):
    def run_pre(self, problem, answer, **kw):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "n.pdf"
            make_pdf(path, problem, answer)
            return pre.analyze_pdf(path, "ARC_N", **kw)

    ANSWER = ["ANSWER KEY", "1. 3", "2. 2"]

    def test_strip_required_and_present(self):
        problem = ["난이도 D2", "QUESTION 1", "난이도 D3", "QUESTION 2"]
        ok = self.run_pre(problem, self.ANSWER, require_difficulty_strip=True)
        self.assertNotIn("ARC_N_DIFFICULTY_STRIP_MISSING", codes(ok))

    def test_strip_missing_fails(self):
        r = self.run_pre(["QUESTION 1", "QUESTION 2"], self.ANSWER, require_difficulty_strip=True)
        self.assertIn("ARC_N_DIFFICULTY_STRIP_MISSING", codes(r))
        self.assertEqual(r["status"], "FAIL")

    def test_strip_not_required_by_default(self):
        r = self.run_pre(["QUESTION 1", "QUESTION 2"], self.ANSWER)
        self.assertNotIn("ARC_N_DIFFICULTY_STRIP_MISSING", codes(r))

    def test_slot_overfill_warns(self):
        r = self.run_pre([f"QUESTION {i}" for i in range(1, 6)], self.ANSWER, max_questions_per_page=4)
        self.assertIn("ARC_N_SLOT_OVERFILL", codes(r))
        self.assertNotEqual(r["status"], "PASS")
        four = self.run_pre([f"QUESTION {i}" for i in range(1, 5)], self.ANSWER, max_questions_per_page=4)
        self.assertNotIn("ARC_N_SLOT_OVERFILL", codes(four))

    def test_difficulty_on_answer_page_fails(self):
        r = self.run_pre(["QUESTION 1"], ["ANSWER KEY", "1. 3  난이도 D2"])
        self.assertIn("ARC_N_DIFFICULTY_IN_ANSWER_PAGE", codes(r))
        self.assertEqual(r["status"], "FAIL")


class RendererStrip(unittest.TestCase):
    ITEM = {"stem": "문항", "options": ["a", "b", "c", "d", "e"], "difficulty": "D3"}

    def texts(self, product, item):
        block = rend.question_block(rend.Layout(), item, "1", product)
        return [op[3] for op in block.ops if op[0] == "text"]

    def test_n_shows_exact_grade_in_strip_only(self):
        t = self.texts("ARC_N", self.ITEM)
        self.assertIn("난이도 D3", t)
        self.assertEqual(sum("D3" in s for s in t), 1)

    def test_final_never_shows_difficulty(self):
        self.assertFalse(any("D3" in s for s in self.texts("ARC_FINAL", self.ITEM)))

    def test_missing_or_invalid_grade_is_not_invented(self):
        for item in (dict(self.ITEM, difficulty=None), dict(self.ITEM, difficulty="hard"), {k: v for k, v in self.ITEM.items() if k != "difficulty"}):
            self.assertFalse(any("난이도" in s for s in self.texts("ARC_N", item)))


class GatewayProfile(unittest.TestCase):
    def test_profiles(self):
        n, f = gw.PRODUCT_PROFILES["ARC_N"], gw.PRODUCT_PROFILES["ARC_FINAL"]
        self.assertEqual((n["slots_per_page"], n["metadata_strip_difficulty"], n["passage_set_slot_release"]), (4, "D1_D5", True))
        self.assertEqual(f["metadata_strip_difficulty"], "NONE")
        self.assertEqual(gw.preflight_args(n), ["--max-questions-per-page", "4", "--require-difficulty-strip"])
        self.assertEqual(gw.preflight_args(f), [])

    def make_root(self, d, registry_row="", asset=None):
        root = Path(d)
        (root / "templates/brand/assets").mkdir(parents=True)
        (root / "templates/brand/ARC_BRAND_ASSET_REGISTRY_V1.0.md").write_text("| table |\n" + registry_row + "\n", encoding="utf-8")
        if asset is not None:
            (root / "templates/brand/assets" / gw.BW_LOGO).write_bytes(asset)
        return root

    MANIFEST = {"runtime": {"arc_n_cover_logo_variant": "BW_REGISTERED_ASSET_REQUIRED"}}

    def test_unregistered_logo_blocks_release(self):
        with tempfile.TemporaryDirectory() as d:
            b = gw.brand_release_blockers(self.make_root(d), self.MANIFEST, "ARC_N")
        self.assertTrue(b and b[0].startswith("BRAND_ASSET_MISSING"))

    def test_registered_matching_logo_clears_blocker(self):
        data = b"bw-logo-bytes"
        h = hashlib.sha256(data).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            root = self.make_root(d, f"| ARC N B/W | {gw.BW_LOGO} | id | 1 | {h} |", data)
            self.assertEqual(gw.brand_release_blockers(root, self.MANIFEST, "ARC_N"), [])

    def test_hash_mismatch_and_absent_copy(self):
        h = hashlib.sha256(b"x").hexdigest()
        with tempfile.TemporaryDirectory() as d:
            root = self.make_root(d, f"| {gw.BW_LOGO} | {h} |", b"other")
            self.assertTrue(gw.brand_release_blockers(root, self.MANIFEST, "ARC_N")[0].startswith("BRAND_HASH_MISMATCH"))
        with tempfile.TemporaryDirectory() as d:
            root = self.make_root(d, f"| {gw.BW_LOGO} | {h} |")
            self.assertIn("repository copy is absent", gw.brand_release_blockers(root, self.MANIFEST, "ARC_N")[0])

    def test_other_products_unaffected(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(gw.brand_release_blockers(self.make_root(d), self.MANIFEST, "ARC_FINAL"), [])

    def test_repo_registry_row_is_pending_not_a_hash(self):
        b = gw.brand_release_blockers(ROOT, yaml_manifest(), "ARC_N")
        self.assertTrue(b and b[0].startswith("BRAND_ASSET_MISSING"))


def yaml_manifest():
    import yaml
    return yaml.safe_load((ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
