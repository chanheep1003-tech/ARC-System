#!/usr/bin/env python3
"""Project-local external tools. This adapter never grants ARC content approval."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
LOCK = Path(__file__).with_name('tools.lock.json')
PROJECT = 'ARC-System'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_new(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as f:
        f.write(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def runtime(root=ROOT):
    return Path(root) / '.arc-tools'


def environment(root=ROOT):
    rt = runtime(root)
    env = os.environ.copy()
    env.update({
        'DEEPTUTOR_HOME': str(rt / 'deeptutor-home'),
        'CLAUDE_MEM_DATA_DIR': str(rt / 'memory'),
        'CLAUDE_MEM_PROVIDER': 'host',
        'CLAUDE_MEM_WORKER_HOST': '127.0.0.1',
        'CLAUDE_MEM_WORKER_PORT': '37891',
        'CLAUDE_MEM_ONLINE_OPTIN': 'false',
        'CLAUDE_MEM_TELEMETRY': '0',
        'DO_NOT_TRACK': '1',
        'IMPECCABLE_HOME': str(rt / 'impeccable-home'),
        'IMPECCABLE_LIVE_COPY_AGENT': 'chat',
    })
    return env


def execute(argv, root=ROOT, timeout=180, cwd=None):
    return subprocess.run([str(x) for x in argv], cwd=cwd or root,
                          env=environment(root), text=True, capture_output=True, timeout=timeout)


def checked(argv, root=ROOT, timeout=180, cwd=None):
    r = execute(argv, root, timeout, cwd)
    if r.returncode:
        raise RuntimeError(f'{Path(str(argv[0])).name} exited {r.returncode}: {(r.stderr or r.stdout)[-1800:]}')
    return r


def pybin(name, root=ROOT):
    return runtime(root) / 'venvs' / name / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')


def appbin(name, root=ROOT):
    return runtime(root) / 'node/node_modules/.bin' / (name + '.cmd' if os.name == 'nt' else name)


def _bun_runs(path):
    """True only when this binary can execute on the host (the musl build cannot on glibc and vice versa)."""
    try:
        return subprocess.run([str(path), '--version'], capture_output=True, timeout=15).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def bunbin(root=ROOT):
    base = runtime(root) / 'node/node_modules'
    candidates = list(base.glob('@oven/bun-*/bin/bun')) + list(base.glob('@oven/bun-*/bin/bun.exe'))
    # npm installs both libc variants; try the non-musl package first, then keep only a binary that really runs.
    for path in sorted(candidates, key=lambda c: ('musl' in str(c), str(c))):
        if path.is_file() and _bun_runs(path):
            return path
    ordinary = appbin('bun', root)
    if ordinary.exists():
        return ordinary
    raise RuntimeError('Bun runtime missing; run install claude-mem')


def source(tool, root=ROOT):
    return runtime(root) / 'src' / tool


def fetch(tool, root=ROOT, lock=None):
    spec = (lock or read(LOCK))['tools'][tool]
    dst = source(tool, root)
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        checked(['git', 'init', str(dst)], root)
        checked(['git', 'remote', 'add', 'origin', 'https://github.com/' + spec['repository'] + '.git'], root, cwd=dst)
        checked(['git', 'fetch', '--depth', '1', 'origin', spec['commit']], root, cwd=dst)
        checked(['git', 'checkout', '--detach', 'FETCH_HEAD'], root, cwd=dst)
    actual = checked(['git', 'rev-parse', 'HEAD'], root, cwd=dst).stdout.strip()
    if actual != spec['commit']:
        raise RuntimeError(f'{tool}: checkout differs from locked commit; preserve it and resolve explicitly')
    if not (dst / 'LICENSE').is_file():
        raise RuntimeError(f'{tool}: upstream LICENSE missing')
    return dst


def install(tool, root=ROOT):
    spec = read(LOCK)['tools'][tool]
    src = fetch(tool, root)
    if tool in ('superpowers', 'mattpocock'):
        # Deliberately expose the bundle through ARC's router, not global hooks.
        paths = skill_paths(tool, root)
        index = runtime(root) / (tool + '-skills.json')
        index.write_text(json.dumps([str(p.relative_to(root)) for p in paths], indent=2) + '\n')
        return {'tool': tool, 'installed_skills': len(paths), 'activation': 'ARC_ROUTE_ON_DEMAND'}
    if tool in ('markitdown', 'deeptutor', 'heretic'):
        name = 'documents' if tool == 'markitdown' else tool
        python = pybin(name, root)
        python.parent.parent.parent.mkdir(parents=True, exist_ok=True)
        if not python.exists():
            checked([sys.executable, '-m', 'venv', str(python.parent.parent)], root)
        package = str(src / 'packages/markitdown') + '[pdf,docx,pptx,xlsx,xls]' if tool == 'markitdown' else str(src)
        checked([python, '-m', 'ensurepip', '--upgrade'], root)
        checked([python, '-m', 'pip', 'install', package], root, timeout=1800)
        if tool == 'deeptutor':
            checked([python, '-m', 'deeptutor_cli.main', 'init', '--non-interactive'], root)
        return {'tool': tool, 'installed': True, 'model_execution': 'NOT_RUN'}
    if tool == 'orkas':
        checked(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], root, timeout=900, cwd=src)
        return {'tool': tool, 'installed': 'JAVASCRIPT_DEPENDENCIES', 'native_gui': 'NOT_VERIFIED'}
    node = runtime(root) / 'node'
    node.mkdir(parents=True, exist_ok=True)
    for filename in ('package.json', 'package-lock.json'):
        target = node / filename
        expected = (Path(__file__).parent / 'node' / filename).read_bytes()
        if target.exists() and target.read_bytes() != expected:
            # Refuse to replace another user's runtime manifest silently.
            raise RuntimeError(f'local node {filename} differs; preserve it and reconcile with tooling/external/node first')
        target.write_bytes(expected)
    checked(['npm', 'ci', '--prefix', str(node), '--ignore-scripts', '--no-audit', '--no-fund'], root, timeout=900)
    if tool == 'impeccable':
        # Link known local skill assets; do not enable permission-bypass hooks.
        link = Path(root) / '.agents/skills/impeccable'
        expected = src / '.agents/skills/impeccable'
        if link.is_symlink() and link.resolve() == expected.resolve():
            pass
        elif link.exists() or link.is_symlink():
            raise RuntimeError('existing project Impeccable installation differs; preserve it and reconcile explicitly')
        else:
            checked([appbin(tool, root), 'link', '--source=' + str(src), '--providers=codex', '--yes'], root)
    return {'tool': tool, 'installed': True, 'global_hooks': False}


def skill_paths(tool, root=ROOT):
    src = source(tool, root)
    if tool == 'superpowers':
        return sorted((src / 'skills').glob('*/SKILL.md'))
    if tool == 'mattpocock':
        return sorted((src / 'skills/engineering').glob('*/SKILL.md')) + sorted((src / 'skills/productivity').glob('*/SKILL.md'))
    if tool == 'impeccable':
        return [src / '.agents/skills/impeccable/SKILL.md']
    raise ValueError('not a skill bundle')


def route(task):
    routes = {
        'source': ['markitdown'],
        'tutor': ['deeptutor'],
        'maintenance': ['superpowers', 'mattpocock'],
        'design': ['impeccable'],
        'memory': ['claude-mem'],
        'team': ['orkas'],
        'model-lab': ['heretic'],
    }
    return {'task': task, 'tools': routes[task], 'authority': 'SYSTEM_MANIFEST.yaml',
            'scope_expansion': False, 'content_approval': False,
            'execution': 'ON_DEMAND', 'personal_weakness_tracking': False}


def convert(input_path, output, source_ref, root=ROOT):
    original, output = Path(input_path).resolve(), Path(output).resolve()
    receipt = Path(str(output) + '.receipt.json')
    if not original.is_file():
        raise ValueError('input must be an existing local file downloaded via an authorized connector')
    if output == original or output.exists() or receipt.exists():
        raise ValueError('output and receipt must be new paths distinct from the input')
    if not source_ref.strip():
        raise ValueError('source reference required')
    python = pybin('documents', root)
    code = 'from markitdown import MarkItDown; import sys; print(MarkItDown(enable_plugins=False).convert(sys.argv[1]).markdown)'
    result = checked([python, '-c', code, str(original)], root)
    if not result.stdout.strip():
        raise ValueError('empty extraction; scan/OCR review required')
    data = {
        'schema': 'ARC-EXTRACTION-RECEIPT-V1', 'source_ref': source_ref,
        'input_sha256': hashlib.sha256(original.read_bytes()).hexdigest(),
        'output_sha256': hashlib.sha256(result.stdout.encode()).hexdigest(),
        'converter': 'markitdown', 'scope_status': 'UNKNOWN',
        'review_status': 'UNVERIFIED', 'location_status': 'UNVERIFIED',
        'visual_marks_status': 'NOT_CHECKED', 'ocr_status': 'NOT_RUN',
        'active_bank_eligible': False,
    }
    write_new(output, result.stdout)
    write_new(receipt, data)
    return data


def memory_request(endpoint, payload=None, root=ROOT):
    # Fixed loopback endpoint, fixed ARC project: no remote memory upload.
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request('http://127.0.0.1:37891' + endpoint, data=body,
                                 headers={'Content-Type': 'application/json'})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(req, timeout=10) as response:
        return json.load(response)


def memory_service(command, root=ROOT):
    worker = runtime(root) / 'node/node_modules/claude-mem/plugin/scripts/worker-service.cjs'
    return checked([bunbin(root), worker, command], root, timeout=90).stdout


def doctor(root=ROOT):
    rows = {}
    for tool, spec in read(LOCK)['tools'].items():
        src = source(tool, root)
        row = {'source_present': src.is_dir(), 'commit_match': False, 'runtime': 'NOT_INSTALLED', 'functional': 'NOT_TESTED'}
        if src.is_dir():
            row['commit_match'] = execute(['git', 'rev-parse', 'HEAD'], root, cwd=src).stdout.strip() == spec['commit']
        try:
            if tool in ('superpowers', 'mattpocock'):
                row.update(runtime='INSTALLED', skill_count=len(skill_paths(tool, root)), functional='ON_DEMAND_FILES')
                if not row['commit_match'] or not row['skill_count']:
                    row.update(runtime='INVALID', functional='BLOCKED')
            elif tool == 'deeptutor':
                p = pybin(tool, root)
                r = execute([p, '-m', 'deeptutor_cli.main', 'doctor', '--format', 'json'], root, timeout=30)
                report = json.loads(r.stdout)
                row.update(runtime='INSTALLED', functional='READY' if report.get('ok') else 'MODEL_SETUP_REQUIRED', checks=report.get('checks'))
            elif tool in ('markitdown', 'heretic'):
                name = 'documents' if tool == 'markitdown' else tool
                code = 'import ' + tool + '; import importlib.metadata as m; print(m.version(' + repr('heretic-llm' if tool == 'heretic' else 'markitdown') + '))'
                r = checked([pybin(name, root), '-c', code], root, timeout=45)
                row.update(runtime='INSTALLED', version=r.stdout.strip(), functional='IMPORT_OK')
                if tool == 'heretic':
                    gpu = checked([pybin(name, root), '-c', 'import torch; print(torch.cuda.is_available())'], root, timeout=45).stdout.strip()
                    row.update(cuda_available=gpu == 'True', functional='MODEL_AND_HARDWARE_SETUP_REQUIRED', automatic_model_modification=False)
            elif tool == 'orkas':
                ok = (src / 'node_modules/typescript').is_dir()
                row.update(runtime='JS_DEPENDENCIES_INSTALLED' if ok else 'NOT_INSTALLED', functional='NATIVE_GUI_SETUP_REQUIRED')
            elif tool == 'impeccable':
                r = checked([appbin(tool, root), '--version'], root)
                row.update(runtime='INSTALLED', version=r.stdout.strip(), functional='CLI_OK')
            elif tool == 'claude-mem':
                r = checked([appbin(tool, root), '--version'], root)
                row.update(runtime='SDK_INSTALLED', version=r.stdout.strip(), functional='WORKER_NOT_RUNNING', global_hooks=False)
                try:
                    health = memory_request('/api/health', root=root)
                    row.update(functional='LOCAL_WORKER_READY', health=health)
                except Exception:
                    pass
        except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
            row['error'] = str(exc)[:800]
        rows[tool] = row
    return {'schema': 'ARC-EXTERNAL-DOCTOR-V1', 'tools': rows, 'model_quality_regression_executed': False,
            'production_enabled': False, 'global_agent_hooks_installed': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('fetch', 'install'):
        p = sub.add_parser(name); p.add_argument('tool', choices=[*read(LOCK)['tools'], 'all'])
    p = sub.add_parser('doctor'); p.add_argument('--output')
    p = sub.add_parser('route'); p.add_argument('task', choices=['source','tutor','maintenance','design','memory','team','model-lab'])
    p = sub.add_parser('skills'); p.add_argument('tool', choices=['superpowers','mattpocock','impeccable'])
    p = sub.add_parser('convert'); p.add_argument('input'); p.add_argument('--output', required=True); p.add_argument('--source-ref', required=True)
    p = sub.add_parser('memory-service'); p.add_argument('action', choices=['start','stop','status'])
    p = sub.add_parser('memory-save'); p.add_argument('--input', required=True); p.add_argument('--title', required=True)
    p = sub.add_parser('memory-search'); p.add_argument('query')
    p = sub.add_parser('tutor'); p.add_argument('--prompt-file', required=True); p.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command in ('fetch', 'install'):
            ids = list(read(LOCK)['tools']) if args.tool == 'all' else [args.tool]
            results = []
            for tool in ids:
                try:
                    result = install(tool) if args.command == 'install' else {'tool':tool,'source':str(fetch(tool))}
                    results.append(result)
                except Exception as exc:
                    results.append({'tool':tool,'status':'BLOCKED','error':str(exc)[:1800]})
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return int(any(x.get('status')=='BLOCKED' for x in results))
        if args.command == 'route': result = route(args.task)
        elif args.command == 'skills': result = [str(p.relative_to(ROOT)) for p in skill_paths(args.tool)]
        elif args.command == 'doctor':
            result = doctor()
            if args.output: write_new(args.output, result)
        elif args.command == 'convert': result = convert(args.input, args.output, args.source_ref)
        elif args.command == 'memory-service': result = memory_service(args.action)
        elif args.command == 'memory-save':
            result = memory_request('/api/memory/save', {'text':Path(args.input).read_text(), 'title':args.title, 'project':PROJECT, 'cwd':str(ROOT)})
        elif args.command == 'memory-search':
            from urllib.parse import urlencode
            result = memory_request('/api/search/observations?' + urlencode({'query':args.query,'project':PROJECT}))
        elif args.command == 'tutor':
            if Path(args.output).exists(): raise ValueError('choose a new output path')
            state = doctor()['tools']['deeptutor']
            if state['functional'] != 'READY': raise ValueError('DeepTutor model/credentials not configured; run its config setup first')
            prompt = Path(args.prompt_file).read_text()
            p = pybin('deeptutor').parent / ('deeptutor.exe' if os.name == 'nt' else 'deeptutor')
            r = checked([p,'run','chat',prompt,'--format','json','--language','ko'], timeout=600)
            write_new(args.output, r.stdout)
            result = {'output':args.output,'status':'DRAFT_REVIEW_PENDING','active_bank_eligible':False}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({'status':'BLOCKED','error':str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
