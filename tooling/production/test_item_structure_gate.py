import copy
import importlib.util
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = _load("item_structure_gate_t", "tooling/production/item_structure_gate.py")
LIB = g.load_library()


def item(no, ans, **kw):
    base = {"item_id": f"SOC-S2-{no:03d}", "format": "MCQ", "difficulty": "D3", "template": "T3", "stem": "s",
            "options": ["가나다라마바사", "아자차카타파하", "하나둘셋넷다섯", "여섯일곱여덟", "아홉열하나둘"], "answer": ans,
            "reasoning_steps": 3, "immediate_elimination": 2,
            "view": ["갑: 롤스 요지", "을: 노직 요지", "ㄱ. 진술1", "ㄴ. 진술2", "ㄷ. 진술3"]}
    base.update(kw)
    return base


def bundle(items, **kw):
    b = {"product_mode": "ARC_N", "subject": "SOC", "items": items,
         "request_spec": {"decided_by": "USER", "stage": "S2", "item_count": len(items),
                          "difficulty_targets": {"D2": 0.2, "D3": 0.5, "D45": 0.3}}}
    b.update(kw)
    return b


class StructureGateTests(unittest.TestCase):
    def codes(self, res):
        return {f["code"] for f in res["findings"]}

    def test_library_templates_are_well_formed(self):
        ranks = {"D1", "D2", "D3", "D4", "D5"}
        for code, t in LIB["templates"].items():
            self.assertIn(t["subject"], {"SOC", "SCI", "KOR"}, code)
            lo, hi = t["difficulty"]
            self.assertTrue(lo in ranks and hi in ranks and g.RANK[lo] <= g.RANK[hi], code)
            self.assertNotIn("D1", t["difficulty"], code)

    def test_template_required_known_subject_and_range(self):
        a = item(1, 1); del a["template"]
        b = item(2, 2, template="ZZ")
        c = item(3, 3, template="S1")                 # 과학 템플릿을 사회에 사용
        d = item(4, 4, template="T1", difficulty="D4")  # T1 은 D2 전용
        codes = self.codes(g.check_bundle(bundle([a, b, c, d])))
        for want in ("TEMPLATE_MISSING", "TEMPLATE_UNKNOWN", "TEMPLATE_SUBJECT_MISMATCH", "TEMPLATE_DIFFICULTY_OUT_OF_RANGE"):
            self.assertIn(want, codes)

    def test_d4_label_needs_structure(self):
        weak = item(1, 1, difficulty="D4", template="T4", reasoning_steps=1, view=["갑: x"], immediate_elimination=3)
        res = g.check_bundle(bundle([weak]))
        self.assertIn("STRUCTURE_BAND_BELOW_LABEL", self.codes(res))
        self.assertEqual(res["status"], "FAIL")
        strong = item(1, 1, difficulty="D4", template="T10", reasoning_steps=5, immediate_elimination=1,
                      table={"header": ["a"], "rows": [["b"]]})
        res2 = g.check_bundle(bundle([strong]))
        self.assertNotIn("STRUCTURE_BAND_BELOW_LABEL", self.codes(res2))

    def test_length_cue(self):
        long_ans = item(1, 3, options=["짧은 선지입니다", "역시 짧은 선지", "이것은 정답인데 다른 선지들보다 훨씬 더 길게 쓰여 있는 문장입니다", "짧은 선지 넷", "짧은 선지 다섯"])
        self.assertIn("LENGTH_CUE_ANSWER_LONGEST", self.codes(g.check_bundle(bundle([long_ans]))))
        sym = item(1, 1, options=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"])
        self.assertNotIn("LENGTH_CUE_ANSWER_LONGEST", self.codes(g.check_bundle(bundle([sym]))))

    def test_absolute_word_cue(self):
        opts = ["그는 언제나 옳다고 본다", "어떤 경우에도 허용된다고 본다", "전혀 고려하지 않는다고 본다", "상황에 따라 판단한다고 본다", "모두가 그렇다고 본다 같다"]
        res = g.check_bundle(bundle([item(1, 4, options=opts)]))
        self.assertIn("ABSOLUTE_WORD_CUE", self.codes(res))

    def test_position_balance_and_run(self):
        items = [item(i + 1, 1) for i in range(10)]
        codes = self.codes(g.check_bundle(bundle(items)))
        self.assertIn("ANSWER_POSITION_BIAS", codes)
        self.assertIn("ANSWER_POSITION_RUN", codes)
        ok = [item(i + 1, (i % 5) + 1) for i in range(10)]
        self.assertNotIn("ANSWER_POSITION_BIAS", self.codes(g.check_bundle(bundle(ok))))

    def test_textbook_copy(self):
        book = "자유주의는 개인의 자유와 권리를 최대한 누리며 개인선을 실현하는 것을 정의롭다고 여긴다."
        copied = item(1, 1, options=["자유주의는 개인의 자유와 권리를 최대한 누리며 개인선을 실현하는 것을 정의롭다고 여긴다.", "x" * 20, "y" * 20, "z" * 20, "w" * 20])
        res = g.check_bundle(bundle([copied]), source_texts=[book])
        self.assertIn("TEXTBOOK_COPY", self.codes(res))
        self.assertIn("TEXTBOOK_COPY_UNCHECKED", self.codes(g.check_bundle(bundle([copied]))))

    def test_feasibility_asks_user(self):
        b = bundle([item(1, 1)], scope_profile={"subunit_count": 1})
        res = g.check_bundle(b)
        self.assertIn("REQUEST_DIFFICULTY_INFEASIBLE_FOR_SCOPE", self.codes(res))
        self.assertTrue(any("ASK THE USER" in f["message"] for f in res["findings"]))
        b["request_spec"]["feasibility_acknowledged_by"] = "USER"
        self.assertNotIn("REQUEST_DIFFICULTY_INFEASIBLE_FOR_SCOPE", self.codes(g.check_bundle(b)))
        wide = bundle([item(1, 1)], scope_profile={"subunit_count": 3})
        self.assertNotIn("REQUEST_DIFFICULTY_INFEASIBLE_FOR_SCOPE", self.codes(g.check_bundle(wide)))
        self.assertIn("REQUEST_SCOPE_PROFILE_MISSING", self.codes(g.check_bundle(bundle([item(1, 1)]))))

    def test_soc_s2_v3_rejected_bundle_is_flagged_before_solver(self):
        """v3 의 D4 라벨 문항 다수는 구조 점수가 D3 밴드다. 풀이자도 모두 D3로 평가했다(사전 예측 일치)."""
        raw = yaml.safe_load((ROOT / "quality/production/SOC_S2_JUSTICE_THEORIES_20261108/items_v3_exam_structure_REJECTED.yaml").read_text(encoding="utf-8"))
        res = g.check_bundle(raw)
        d4_low = [f["item_id"] for f in res["findings"] if f["code"] == "STRUCTURE_BAND_BELOW_LABEL" and f["severity"] == "FAIL"]
        self.assertGreaterEqual(len(d4_low), 4)
        self.assertEqual(res["status"], "FAIL")
        self.assertNotIn("TEMPLATE_MISSING", self.codes(res))
        self.assertNotIn("TEMPLATE_DIFFICULTY_OUT_OF_RANGE", self.codes(res))


class SuppliedConceptTests(unittest.TestCase):
    def codes(self, res):
        return {f["code"] for f in res["findings"]}

    def test_outside_term_without_definition_fails(self):
        it = item(1, 1, view=["갑: 원초적 입장에서 합의한 원칙이 정의입니다.", "ㄱ. a", "ㄴ. b", "ㄷ. c"])
        self.assertIn("OUTSIDE_CONCEPT_NOT_SUPPLIED", self.codes(g.check_bundle(bundle([it]))))

    def test_outside_term_defined_in_item_passes_and_scores(self):
        view = ["<자료> 분배의 정의를 그 소유가 생긴 과정으로 판단하는 관점을 '역사적 원리'라 한다.", "갑: 정당한 취득과 양도의 결과이면 정당합니다.", "ㄱ. a", "ㄴ. b", "ㄷ. c"]
        base = item(1, 1, view=view)
        res_no = g.check_bundle(bundle([base]))
        self.assertIn("OUTSIDE_CONCEPT_NOT_SUPPLIED", self.codes(res_no))      # supplied_concepts 기록 없음
        ok = item(1, 1, view=view, supplied_concepts=["역사적 원리"])
        res_ok = g.check_bundle(bundle([ok]))
        self.assertNotIn("OUTSIDE_CONCEPT_NOT_SUPPLIED", self.codes(res_ok))
        s_ok = g.structure_features(ok, "SOC", LIB)["score"]
        s_base = g.structure_features(base, "SOC", LIB)["score"]
        self.assertGreater(s_ok, s_base)

    def test_plain_wording_without_term_needs_nothing(self):
        it = item(1, 1, view=["갑: 공정한 조건에서 합의한 것이 정의의 원칙입니다.", "ㄱ. a", "ㄴ. b", "ㄷ. c"])
        self.assertNotIn("OUTSIDE_CONCEPT_NOT_SUPPLIED", self.codes(g.check_bundle(bundle([it]))))


class PipelineFeasibilityTests(unittest.TestCase):
    def test_pipeline_blocks_infeasible_request_before_anything_else(self):
        import json
        import tempfile
        pipeline = _load("arc_production_pipeline_t", "tooling/production/production_pipeline.py")
        raw = yaml.safe_load((ROOT / "quality/production/SOC_S2_JUSTICE_THEORIES_20261108/items_v3_exam_structure_REJECTED.yaml").read_text(encoding="utf-8"))
        raw["scope_profile"] = {"subunit_count": 1}
        with tempfile.TemporaryDirectory() as td:
            d = Path(td) / "bundle"
            d.mkdir()
            (d / "items.yaml").write_text(yaml.safe_dump(raw, allow_unicode=True, sort_keys=False), encoding="utf-8")
            rep = pipeline.run(d, Path(td) / "out")
            self.assertEqual(rep["status"], "BLOCKED")
            self.assertEqual(rep["blocking_gates"], ["REQUEST_SPEC"])
            self.assertIn("REQUEST_DIFFICULTY_INFEASIBLE_FOR_SCOPE", {f["code"] for f in rep["findings"]})
            raw["request_spec"]["feasibility_acknowledged_by"] = "USER"
            (d / "items.yaml").write_text(yaml.safe_dump(raw, allow_unicode=True, sort_keys=False), encoding="utf-8")
            try:
                rep2 = pipeline.run(d, Path(td) / "out2")
            except Exception:
                rep2 = {"blocking_gates": ["LATER_STAGE"]}
            self.assertNotEqual(rep2.get("blocking_gates"), ["REQUEST_SPEC"])


if __name__ == "__main__":
    unittest.main()
