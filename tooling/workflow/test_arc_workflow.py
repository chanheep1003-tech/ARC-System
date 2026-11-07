import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from arc_workflow import advance, counts, create, handoff, main, read

REQUEST = {'batch_id': 'trial', 'subject': 'SCI', 'scope': 'neutralization',
           'product': 'ARC_N', 'count': 1, 'ruleset_commit': 'a' * 40}
SOURCE = {'refs': [{'file_ref': 'drive:source', 'location': 'p.1', 'verified': True}]}
DRAFT = {'items': [{'id': 'SCI-001', 'sha256': 'b' * 64, 'student_ref': 'student.md', 'author_answer': 3}]}
REVIEW = {'rounds': 1, 'fresh_context': True,
          'excluded_inputs': ['answer_key', 'author_solution', 'author_history', 'target_difficulty'],
          'items': [{'id': 'SCI-001', 'sha256': 'b' * 64, 'answer': 3, 'option_verdicts': [False, False, True, False, False],
                     'evidence_refs': ['drive:source#p1'], 'fact_pass': True, 'scope_pass': True, 'quality_pass': True}]}
PUBLISH = {'mode': 'verified', 'artifacts': [{'file_ref': 'drive:output', 'readback_verified': True}],
           'gate_receipts': {g: {'pass': True, 'evidence_ref': 'gate-report.json#' + g}
                             for g in ['exam_scope', 'generation_source', 'similarity', 'product_quality']}}

def draft():
    return advance(advance(create(REQUEST, 'GPT'), 'source', SOURCE), 'draft', DRAFT)

class WorkflowTests(unittest.TestCase):
    def test_full_flow_and_counts(self):
        s = advance(advance(draft(), 'review', REVIEW), 'publish', PUBLISH)
        self.assertEqual(counts(s), {'target': 1, 'drafted': 1, 'checked': 1, 'eligible': 1, 'active': 1})

    def test_cannot_skip_source_or_publish_verified_without_review(self):
        with self.assertRaises(ValueError):
            advance(create(REQUEST, 'GPT'), 'draft', DRAFT)
        with self.assertRaises(ValueError):
            advance(draft(), 'publish', PUBLISH)

    def test_blind_handoff_excludes_key_and_history(self):
        packet = handoff(draft())
        self.assertEqual(packet['items'][0], {k: DRAFT['items'][0][k] for k in ['id', 'sha256', 'student_ref']})
        self.assertNotIn('author_answer', json.dumps(packet))

    def test_stale_review_and_duplicate_ids_rejected(self):
        r = json.loads(json.dumps(REVIEW)); r['items'][0]['sha256'] = 'c' * 64
        with self.assertRaises(ValueError):
            advance(draft(), 'review', r)
        d = {'items': DRAFT['items'] * 2}
        with self.assertRaises(ValueError):
            advance(advance(create(REQUEST, 'GPT'), 'source', SOURCE), 'draft', d)

    def test_matching_answers_do_not_override_failed_quality(self):
        r = json.loads(json.dumps(REVIEW)); r['items'][0]['quality_pass'] = False
        s = advance(draft(), 'review', r)
        self.assertEqual(counts(s)['eligible'], 0)
        with self.assertRaises(ValueError):
            advance(s, 'publish', PUBLISH)

    def test_multiple_accepted_options_rejected(self):
        r = json.loads(json.dumps(REVIEW)); r['items'][0]['option_verdicts'] = [True, False, True, False, False]
        with self.assertRaises(ValueError): advance(draft(), 'review', r)

    def test_verified_publish_needs_ancillary_gate_receipts(self):
        s = advance(draft(), 'review', REVIEW)
        with self.assertRaises(ValueError): advance(s, 'publish', dict(PUBLISH, gate_receipts={}))

    def test_draft_can_be_saved_without_independent_review(self):
        p = dict(PUBLISH, mode='draft')
        s = advance(draft(), 'publish', p)
        self.assertEqual(counts(s)['active'], 0)
        self.assertEqual(counts(s)['checked'], 0)

    def test_chunk_checkpoint_then_resume(self):
        request = dict(REQUEST, count=2)
        s = advance(advance(create(request, 'GPT'), 'source', SOURCE), 'draft', DRAFT)
        self.assertEqual(counts(s)['drafted'], 1)
        with self.assertRaises(ValueError): advance(s, 'review', REVIEW)
        next_item = dict(DRAFT['items'][0], id='SCI-002')
        s = advance(s, 'draft', {'items': [next_item]})
        self.assertEqual(counts(s)['drafted'], 2)

    def test_cli_resume_owner_stale_state_and_revision_invalidation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); state = root/'state.json'; payload = root/'input.json'
            def call(cmd, **extra):
                args = [cmd, '--state', str(state)]
                for k,v in extra.items(): args += ['--'+k.replace('_','-'), str(v)]
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    return main(args)
            payload.write_text(json.dumps(REQUEST))
            self.assertEqual(call('init', input=payload, actor='GPT'), 0)
            self.assertEqual(call('init', input=payload, actor='GPT'), 2)
            payload.write_text(json.dumps(SOURCE))
            self.assertEqual(call('record', stage='source', input=payload, actor='GEMINI', expected_version=1), 2)
            self.assertEqual(call('record', stage='source', input=payload, actor='GPT', expected_version=0), 2)
            self.assertEqual(call('record', stage='source', input=payload, actor='GPT', expected_version=1), 0)
            payload.write_text(json.dumps(DRAFT))
            self.assertEqual(call('record', stage='draft', input=payload, actor='GPT', expected_version=2), 0)
            payload.write_text(json.dumps(REVIEW))
            self.assertEqual(call('record', stage='review', input=payload, actor='GPT', expected_version=3), 0)
            revised = json.loads(json.dumps(DRAFT)); revised['items'][0]['sha256'] = 'c' * 64
            payload.write_text(json.dumps(revised))
            self.assertEqual(call('revise', input=payload, actor='GPT', expected_version=4, reason='fix option'), 0)
            self.assertEqual(counts(read(state))['checked'], 0)
            self.assertIn('previous_review', read(state))

    def test_failed_gate_records_blocker_and_can_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); state = root/'state.json'; payload = root/'input.json'
            state.write_text(json.dumps(create(REQUEST, 'GPT')))
            payload.write_text(json.dumps({'refs': []}))
            args = ['record', '--state', str(state), '--actor', 'GPT', '--expected-version', '1',
                    '--stage', 'source', '--input', str(payload)]
            with contextlib.redirect_stderr(io.StringIO()): self.assertEqual(main(args), 2)
            self.assertEqual(read(state)['status'], 'BLOCKED')
            self.assertEqual(read(state)['stage'], 'request')
            payload.write_text(json.dumps(SOURCE)); args[args.index('1')] = '2'
            with contextlib.redirect_stdout(io.StringIO()): self.assertEqual(main(args), 0)
            self.assertEqual(read(state)['status'], 'READY')

    def test_init_with_manifest_yaml_dates(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            request, manifest, state = root / 'request.json', root / 'manifest.yaml', root / 'state.json'
            request.write_text(json.dumps(REQUEST))
            manifest.write_text('runtime:\n  deadline: 2026-11-07\n  nested:\n    - 2026-11-08\nactive: {}\n')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['init', '--state', str(state), '--input', str(request), '--actor', 'GPT', '--manifest', str(manifest)]), 0)
            self.assertEqual(read(state)['manifest_paths']['runtime']['deadline'], '2026-11-07')
            self.assertEqual(read(state)['manifest_paths']['runtime']['nested'], ['2026-11-08'])

if __name__ == '__main__':
    unittest.main()
