#!/usr/bin/env python3
"""Current-exam admission, replay isolation, and anchor misuse regression."""
import copy
from datetime import date
import hashlib
import shutil
import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("arc_exam_gate", ROOT / "tooling/exams/exam_scope_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class ScopeTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {"runtime": {"active_exam_id": "FINAL"}}
        self.profile = {"status": "PREPARING", "inherit_midterm_scope": False, "subjects": {
            "KOR": {"scope_status": "CONFIRMED_UNITS_ONLY", "scope_evidence_refs": ["SCHOOL:RANGE:1"],
                    "unit_ids": ["U2"], "source_ids": ["RAW2"], "excluded_unit_ids": [],
                    "excluded_source_ids": [], "products": ["ARC_N", "ARC_FINAL"], "difficulty_anchor": None}}}
        self.bundle = {"subject": "KOR", "product_mode": "ARC_N", "exam_context": {
            "exam_id": "FINAL", "profile_sha256": gate.digest(self.profile), "unit_ids": ["U2"], "source_ids": ["RAW2"]},
            "passages": [{"source_text_id": "RAW2"}]}

    def result(self, bundle=None, profile=None, replay=False):
        return gate.analyze(bundle or self.bundle, self.manifest, {"exams": {"FINAL": profile or self.profile}}, archived_replay=replay)

    def codes(self, result):
        return {x["code"] for x in result["findings"]}

    def test_confirmed_unit_practice(self):
        self.assertEqual(self.result()["status"], "PASS")

    def test_yaml_date_hash_matches_iso_date(self):
        p=copy.deepcopy(self.profile);p['exam_date']=date(2026,12,1)
        q=copy.deepcopy(p);q['exam_date']='2026-12-01'
        self.assertEqual(gate.digest(p),gate.digest(q))

    def test_missing_context(self):
        b=copy.deepcopy(self.bundle); b.pop("exam_context")
        self.assertIn("EXAM_CONTEXT_MISSING", self.codes(self.result(b)))

    def test_midterm_id(self):
        b=copy.deepcopy(self.bundle); b["exam_context"]["exam_id"]="MID"
        self.assertIn("EXAM_ID_NOT_ACTIVE", self.codes(self.result(b)))

    def test_stale_profile(self):
        p=copy.deepcopy(self.profile); p["subjects"]["KOR"]["source_ids"].append("NEW")
        self.assertIn("EXAM_PROFILE_STALE", self.codes(self.result(profile=p)))

    def test_pending(self):
        p=copy.deepcopy(self.profile); p["subjects"]["KOR"]["scope_status"]="PENDING"
        self.assertIn("EXAM_SCOPE_PENDING", self.codes(self.result(profile=p)))

    def test_old_unit(self):
        b=copy.deepcopy(self.bundle); b["exam_context"]["unit_ids"]=["U1"]
        self.assertIn("EXAM_UNIT_OUT_OF_SCOPE", self.codes(self.result(b)))

    def test_old_source(self):
        b=copy.deepcopy(self.bundle); b["exam_context"]["source_ids"]=["RAW1"]
        self.assertIn("EXAM_SOURCE_OUT_OF_SCOPE", self.codes(self.result(b)))

    def test_actual_source_binding(self):
        b=copy.deepcopy(self.bundle); b["passages"][0]["source_text_id"]="RAW1"
        self.assertIn("EXAM_SOURCE_BINDING_MISMATCH", self.codes(self.result(b)))

    def test_final_partial_scope(self):
        b=copy.deepcopy(self.bundle); b["product_mode"]="ARC_FINAL"
        self.assertIn("FINAL_SCOPE_NOT_CONFIRMED", self.codes(self.result(b)))

    def test_exclusion(self):
        p=copy.deepcopy(self.profile); p["subjects"]["KOR"]["excluded_source_ids"]=["RAW2"]
        self.assertIn("EXAM_SOURCE_OUT_OF_SCOPE", self.codes(self.result(profile=p)))

    def test_active_replay_forbidden(self):
        self.assertIn("ACTIVE_EXAM_REPLAY_FORBIDDEN", self.codes(self.result(replay=True)))

    def test_legacy_replay_never_release(self):
        b=copy.deepcopy(self.bundle); b.pop("exam_context")
        r=self.result(b,replay=True)
        self.assertEqual(r["status"],"ARCHIVED_REPLAY"); self.assertFalse(r["release_allowed"])

    def test_no_scope_evidence(self):
        p=copy.deepcopy(self.profile); p["subjects"]["KOR"]["scope_evidence_refs"]=[]
        self.assertIn("EXAM_SCOPE_EVIDENCE_MISSING", self.codes(self.result(profile=p)))

    def test_anchor_units_and_hash(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'anchor.yaml').write_text('subject: SCI_REDOX\n')
            p=copy.deepcopy(self.profile); p["subjects"]["SCI"]=p["subjects"].pop("KOR")
            p["subjects"]["SCI"]["scope_status"]="CONFIRMED"
            p["subjects"]["SCI"]["difficulty_anchor"]={"subject":"SCI_REDOX","unit_ids":["REDOX"],"path":"anchor.yaml","sha256":"0"*64}
            b=copy.deepcopy(self.bundle); b["subject"]="SCI"; b["product_mode"]="ARC_FINAL"; b["exam_context"]["profile_sha256"]=gate.digest(p)
            r=gate.analyze(b,self.manifest,{"exams":{"FINAL":p}},root=root)
            self.assertIn("FINAL_ANCHOR_UNIT_MISMATCH",self.codes(r))
            self.assertIn("FINAL_ANCHOR_CHECKSUM_MISMATCH",self.codes(r))

    def test_registry_path_escape(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(gate.ExamContextError): gate.repo_file(Path(d),'../outside.yaml')

    def test_pending_production_stops_before_blind_or_render(self):
        spec=importlib.util.spec_from_file_location('arc_prod_exam_test',ROOT/'tooling/production/production_pipeline.py')
        prod=importlib.util.module_from_spec(spec);spec.loader.exec_module(prod)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'items.yaml').write_text(yaml.safe_dump({'batch_id':'CURRENT','subject':'KOR','product_mode':'ARC_N'}))
            result=prod.run(root,root/'out')
            self.assertEqual(result['blocking_gates'],['EXAM_SCOPE'])
            self.assertIsNone(result['pdf']); self.assertFalse(list((root/'out').glob('*.pdf')))

    def test_malformed_subjects_fails(self):
        p=copy.deepcopy(self.profile);p['subjects']=[]
        self.assertIn('EXAM_SUBJECT_NOT_REGISTERED',self.codes(self.result(profile=p)))

    def test_malformed_products_fails(self):
        p=copy.deepcopy(self.profile);p['subjects']['KOR']['products']=None
        self.assertIn('EXAM_PRODUCT_NOT_ACTIVE',self.codes(self.result(profile=p)))

    def test_current_final_pipeline_and_handoff_binding(self):
        spec=importlib.util.spec_from_file_location('arc_prod_current_test',ROOT/'tooling/production/production_pipeline.py')
        prod=importlib.util.module_from_spec(spec);spec.loader.exec_module(prod)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            manifest=yaml.safe_load((ROOT/'SYSTEM_MANIFEST.yaml').read_text())
            manifest['runtime']['exam_context_registry']='test_exam.yaml'
            p=copy.deepcopy(self.profile)
            fixture=ROOT/'quality/production/KOR_SEMIFINAL_FINAL_20260925'
            bundle=yaml.safe_load((fixture/'items.yaml').read_text())
            source_ids=sorted(gate.actual_source_ids(bundle))
            p['subjects']['KOR']['source_ids']=source_ids
            p['subjects']['KOR']['scope_status']='CONFIRMED'
            raw_anchor=(ROOT/'quality/anchors/KOR_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0.yaml').read_bytes()
            (root/'test_anchor.yaml').write_bytes(raw_anchor)
            p['subjects']['KOR']['difficulty_anchor']={'subject':'KOR','unit_ids':['U2'],
                'path':'test_anchor.yaml','sha256':hashlib.sha256(raw_anchor).hexdigest()}
            manifest['runtime']['active_exam_id']='FINAL'
            (root/'test_exam.yaml').write_text(yaml.safe_dump({'schema_version':'ARC-EXAM-CONTEXT-V1','exams':{'FINAL':p}}))
            (root/'SYSTEM_MANIFEST.yaml').write_text(yaml.safe_dump(manifest))
            for name in ['templates','tooling','quality']:
                shutil.copytree(ROOT/name,root/name,ignore=shutil.ignore_patterns('__pycache__'))
            bundle['exam_context']={'exam_id':'FINAL','profile_sha256':gate.digest(p),'unit_ids':['U2'],'source_ids':source_ids}
            (root/'items.yaml').write_text(yaml.safe_dump(bundle,allow_unicode=True))
            (root/'blind_review.yaml').write_bytes((fixture/'blind_review.yaml').read_bytes())
            r=prod.run(root,root/'out',manifest_path=root/'SYSTEM_MANIFEST.yaml')
            self.assertEqual(r['gates']['EXAM_SCOPE'],'PASS')
            self.assertEqual(r['gates']['TYPESETTER_ADMISSION'],'PASS')
            self.assertTrue(Path(r['pdf']).is_file())
            handoff=next((root/'out').glob('*_READY.md'))
            metadata,text=prod.handoff_gate.parse_handoff(handoff)
            self.assertEqual(metadata['EXAM_CONTEXT'],bundle['exam_context'])
            proof_path=root/'out'/metadata['QA_EVIDENCE_FILENAME']
            proof=yaml.safe_load(proof_path.read_text());proof['exam_context']['source_ids']=['OTHER']
            proof_path.write_text(yaml.safe_dump(proof))
            with self.assertRaisesRegex(prod.typesetter.TypesetterAdmissionError,'QA_EXAM_CONTEXT_BINDING_MISMATCH'):
                prod.typesetter.resolve_job(handoff,root/'SYSTEM_MANIFEST.yaml')


if __name__ == '__main__':
    unittest.main()
