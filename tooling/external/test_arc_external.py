import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('arc_external', Path(__file__).with_name('arc_external.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class ExternalToolTests(unittest.TestCase):
    def test_routes_do_not_enable_generation_or_profiling(self):
        for task in ['source','tutor','maintenance','design','memory','team','model-lab']:
            r = a.route(task)
            self.assertFalse(r['content_approval'])
            self.assertFalse(r['scope_expansion'])
            self.assertFalse(r['personal_weakness_tracking'])
        self.assertNotIn('heretic', a.route('source')['tools'])
        self.assertEqual(a.route('maintenance')['tools'], ['superpowers','mattpocock'])

    def test_conversion_receipt_does_not_grant_qa(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); original=p/'source.txt'; original.write_text('H+ + OH- -> H2O')
            out=p/'out.md'
            with patch.object(a,'checked',return_value=subprocess.CompletedProcess([],0,'converted\n','')):
                r=a.convert(original,out,'Drive:file-id#page=1',p)
            self.assertEqual(out.read_text(),'converted\n')
            self.assertEqual(r['input_sha256'],hashlib.sha256(original.read_bytes()).hexdigest())
            self.assertEqual(r['review_status'],'UNVERIFIED')
            self.assertEqual(r['visual_marks_status'],'NOT_CHECKED')
            self.assertFalse(r['active_bank_eligible'])
            self.assertEqual(json.loads(Path(str(out)+'.receipt.json').read_text()),r)

    def test_refuses_input_overwrite_and_existing_output(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source.txt';p.write_text('keep')
            with self.assertRaises(ValueError): a.convert(p,p,'ref',d)
            self.assertEqual(p.read_text(),'keep')

    def test_converter_failure_does_not_create_fake_artifacts(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); original=p/'source.txt';original.write_text('content')
            with patch.object(a,'checked',side_effect=RuntimeError('converter failed')):
                with self.assertRaises(RuntimeError):a.convert(original,p/'out.md','ref',p)
            self.assertFalse((p/'out.md').exists())
            self.assertFalse((p/'out.md.receipt.json').exists())

    def test_empty_extraction_blocks_scan_approval(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); original=p/'scan.pdf';original.write_bytes(b'%PDF')
            with patch.object(a,'checked',return_value=subprocess.CompletedProcess([],0,'  ','')):
                with self.assertRaises(ValueError):a.convert(original,p/'out.md','ref',p)
            self.assertFalse((p/'out.md').exists())

    def test_local_memory_does_not_use_http_proxy(self):
        class Response:
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self):return b'{"success":true}'
        class Opener:
            def open(self,req,timeout):
                self.req=req
                self.timeout=timeout
                return Response()
        opener=Opener()
        with patch.object(a.urllib.request,'build_opener',return_value=opener):
            r=a.memory_request('/api/memory/save',{'project':'ARC-System','text':'test'})
        self.assertTrue(r['success'])
        self.assertEqual(opener.req.full_url,'http://127.0.0.1:37891/api/memory/save')
        self.assertEqual(json.loads(opener.req.data)['project'],'ARC-System')

    def test_environment_is_scoped_and_does_not_mutate_parent(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.dict(a.os.environ,{'IMPECCABLE_LIVE_COPY_AGENT':'auto','CLAUDE_MEM_DATA_DIR':'elsewhere'}):
                env=a.environment(Path(d))
                self.assertEqual(env['IMPECCABLE_LIVE_COPY_AGENT'],'chat')
                self.assertEqual(env['CLAUDE_MEM_DATA_DIR'],str(Path(d)/'.arc-tools/memory'))
                self.assertEqual(a.os.environ['CLAUDE_MEM_DATA_DIR'],'elsewhere')

    def test_fetch_mismatch_does_not_checkout_over_user_changes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);src=a.source('example',root);src.mkdir(parents=True);(src/'LICENSE').write_text('MIT')
            lock={'tools':{'example':{'repository':'owner/repo','commit':'a'*40}}}
            with patch.object(a,'checked',return_value=subprocess.CompletedProcess([],0,'b'*40+'\n','')) as run:
                with self.assertRaises(RuntimeError):a.fetch('example',root,lock)
            self.assertEqual(run.call_count,1)
            self.assertEqual(run.call_args.args[0],['git','rev-parse','HEAD'])

    def test_all_upstream_commits_are_pinned(self):
        lock=a.read(a.LOCK)
        self.assertEqual(len(lock['tools']),8)
        for t in lock['tools'].values():
            self.assertRegex(t['commit'],r'^[0-9a-f]{40}$')
            self.assertFalse(t['automatic_activation'])


if __name__=='__main__':unittest.main()
