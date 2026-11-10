#!/usr/bin/env python3
"""Fault-injection tests for provenance and the actual 70/30 counts."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("arc_source_mix", ROOT / "tooling/sources/generation_source_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def bundle(n=20):
    past, _ = gate.targets(n)
    items = []
    for i in range(n):
        p = {"mode": "AI_ORIGINAL", "school_scope_refs": ["SCHOOL:p46"], "design_purpose": "current-scope application"}
        if i < past:
            p = {"mode": "VERIFIED_VARIANT", "source_kind": "SCHOOL_EXAM", "source_id": "EXAM-1",
                 "source_item_number": str(i+1), "source_locator": f"PDF:p{i+1}", "source_answer_ref": "EXAM-KEY:p1",
                 "origin_family_id": f"EXAM-1-Q{i+1}", "source_review_status": "CONTENT_VERIFIED",
                 "core_preserved": "essential conditions and reasoning", "modification_log": ["changed case"]}
        items.append({"item_id": f"Q{i+1}", "provenance": p})
    return {"source_composition": {"policy_version": gate.POLICY_VERSION}, "item_count": n, "items": items}


class Tests(unittest.TestCase):
    def codes(self, b):
        return {f["code"] for f in gate.analyze(b)["findings"]}

    def test_rounding_all_sizes(self):
        for n in range(1,101):
            p,c=gate.targets(n)
            self.assertEqual(p+c,n)
            self.assertLessEqual(abs(p-n*0.7),0.5000001)
        self.assertEqual(gate.targets(20),(14,6))
        self.assertEqual(gate.targets(25),(18,7))
        self.assertEqual(gate.targets(40),(28,12))

    def test_valid_five_subjects(self):
        for subject in ('SCI','SOC','KOR','HIS','AI'):
            b=bundle();b['subject']=subject
            self.assertEqual(gate.analyze(b)['status'],'PASS')

    def test_old_90_10_rejected(self):
        b=bundle();b['items'][14:18]=copy.deepcopy(b['items'][:4])
        for i,r in enumerate(b['items'][14:18],14):
            r['item_id']=f'Q{i+1}';r['provenance']['origin_family_id']=f'EXAM-OTHER-Q{i}'
        self.assertIn('SOURCE_MIX_MISMATCH',self.codes(b))

    def test_missing_original(self):
        b=bundle();b['items'][0]['provenance'].pop('source_id')
        self.assertIn('SOURCE_REFERENCE_MISSING',self.codes(b))

    def test_unreviewed_candidate(self):
        b=bundle();b['items'][0]['provenance']['source_review_status']='HEADER_REVIEWED'
        self.assertIn('SOURCE_UNVERIFIED',self.codes(b))

    def test_publisher_is_not_past_exam(self):
        b=bundle();b['items'][0]['provenance']['source_kind']='PUBLISHER_ITEM'
        self.assertIn('NOT_ACTUAL_PAST_EXAM',self.codes(b))

    def test_same_original_family(self):
        b=bundle();b['items'][1]['provenance']['origin_family_id']=b['items'][0]['provenance']['origin_family_id']
        self.assertIn('ORIGINAL_FAMILY_REPEATED',self.codes(b))

    def test_creative_needs_scope(self):
        b=bundle();b['items'][-1]['provenance'].pop('school_scope_refs')
        self.assertIn('CREATIVE_SCOPE_EVIDENCE_MISSING',self.codes(b))

    def test_blank_creative_scope_rejected(self):
        b=bundle();b['items'][-1]['provenance']['school_scope_refs']=[' ']
        self.assertIn('CREATIVE_SCOPE_EVIDENCE_MISSING',self.codes(b))

    def test_malformed_nested_items_fail_closed(self):
        b=bundle();b.pop('items');b['sets']=[{'items':None}]
        self.assertIn('SOURCE_ITEMS_EMPTY',self.codes(b))

    def test_missing_policy(self):
        b=bundle();b.pop('source_composition')
        self.assertIn('SOURCE_POLICY_MISSING',self.codes(b))

    def test_edits_need_change_log(self):
        b=bundle();b['items'][0]['provenance'].pop('modification_log')
        self.assertIn('SOURCE_CHANGE_LOG_MISSING',self.codes(b))

    def test_constructed_response_and_multiple_sets(self):
        b=bundle();rows=b.pop('items');rows[-1]['format']='CR'
        b['sets']=[{'items':rows[:10]},{'items':rows[10:]}]
        self.assertEqual(gate.analyze(b)['status'],'PASS')

    def test_empty_bundle(self):
        b=bundle();b['items']=[];b['item_count']=0
        self.assertIn('SOURCE_ITEMS_EMPTY',self.codes(b))

    def test_shared_works_do_not_hide_flat_items(self):
        b=bundle();b['sets']=[{'works':[{'source_text_id':'RAW-1'}]}]
        self.assertEqual(gate.analyze(b)['item_count'],20)
        self.assertEqual(gate.analyze(b)['status'],'PASS')

    def test_bad_count_and_duplicate_id(self):
        b=bundle();b['item_count']=19;b['items'][1]['item_id']='Q1'
        self.assertTrue({'SOURCE_ITEM_COUNT_MISMATCH','SOURCE_ITEM_ID_INVALID'} <= self.codes(b))


if __name__=='__main__':
    unittest.main()
