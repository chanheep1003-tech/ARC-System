#!/usr/bin/env python3
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('arc_collection',ROOT/'tooling/sources/source_collection_gate.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.row={'source_id':'ONE','title':'기말 자료 후보','provider':'EBS','url':'https://example.org/a?utm_source=search',
                  'collected_at':'2026-10-03','reviewed_at':'2026-10-03','curriculum':'UNKNOWN','role':'OFFICIAL_REFERENCE',
                  'review_status':'LINK_REVIEWED','exam_scope_status':'PENDING','eligible_for_current_exam':False}

    def codes(self,rows): return {f['code'] for f in gate.analyze({'sources':rows})['findings']}

    def test_candidate_is_not_eligible(self):
        r=gate.analyze({'sources':[self.row]});self.assertEqual(r['status'],'PASS');self.assertEqual(r['eligible_for_current_exam_count'],0)

    def test_deferred_subject_cannot_be_promoted_but_can_be_preserved(self):
        for subject in ("HIS", "AI"):
            with self.subTest(subject=subject):
                row=copy.deepcopy(self.row)
                row.update(role='RAW_SCHOOL_SOURCE',eligible_for_current_exam=True,exam_scope_status='CONFIRMED',review_status='CONTENT_REVIEWED',curriculum='2022_REVISED',scope_evidence_refs=['RANGE'],subject=subject,unit_ids=['U2'],sha256='a'*64,content_verification_ref='CHECK')
                ledger={'collection_scope':{'active_subjects':['SCI','SOC','KOR']},'sources':[row]}
                result=gate.analyze(ledger)
                self.assertIn('COLLECTION_SUBJECT_NOT_ACTIVE',{f['code'] for f in result['findings']})
                self.assertEqual(result['eligible_for_current_exam_count'],0)
                row.update(eligible_for_current_exam=False,collection_action='PARKED_BY_USER')
                self.assertEqual(gate.analyze(ledger)['status'],'PASS')

    def test_active_subject_can_be_promoted_after_full_review(self):
        row=copy.deepcopy(self.row)
        row.update(role='RAW_SCHOOL_SOURCE',eligible_for_current_exam=True,exam_scope_status='CONFIRMED',review_status='CONTENT_REVIEWED',curriculum='2022_REVISED',scope_evidence_refs=['RANGE'],subject='SCI',unit_ids=['U2'],sha256='a'*64,content_verification_ref='CHECK')
        result=gate.analyze({'collection_scope':{'active_subjects':['SCI','SOC','KOR']},'sources':[row]})
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['eligible_for_current_exam_count'],1)

    def test_reference_cannot_be_promoted(self):
        row=copy.deepcopy(self.row);row['eligible_for_current_exam']=True
        self.assertIn('COLLECTION_UNCONFIRMED_PROMOTION',self.codes([row]))
        self.assertIn('COLLECTION_REFERENCE_AS_SCHOOL_SOURCE',self.codes([row]))

    def test_alias_url_duplicate(self):
        row=copy.deepcopy(self.row);row['source_id']='TWO';row['url']='https://example.org/a#section'
        self.assertIn('COLLECTION_IDENTITY_DUPLICATE',self.codes([self.row,row]))

    def test_same_title_size_is_only_candidate_duplicate(self):
        a=copy.deepcopy(self.row);a['size_bytes']=10
        b=copy.deepcopy(a);b['source_id']='TWO';b['url']='https://example.org/b'
        r=gate.analyze({'sources':[a,b]});self.assertEqual(r['status'],'PASS');self.assertEqual(len(r['possible_duplicates_not_content_verified']),1)

    def test_malformed_entry(self):
        self.assertIn('COLLECTION_ENTRY_INVALID',self.codes([None]))

    def test_generated_practice_is_not_raw(self):
        row=copy.deepcopy(self.row);row.update(role='GENERATED_PRACTICE',eligible_for_current_exam=True,exam_scope_status='CONFIRMED',review_status='CONTENT_REVIEWED',curriculum='2022_REVISED',scope_evidence_refs=['RANGE'],subject='KOR',unit_ids=['U2'],sha256='a'*64,content_verification_ref='CHECK')
        self.assertIn('COLLECTION_REFERENCE_AS_SCHOOL_SOURCE',self.codes([row]))


if __name__=='__main__': unittest.main()
