#!/usr/bin/env python3
"""ARC run ledger: one request, resumable stages and reference-only worker handoffs.

This program never calls a model, uploads a file, or proves a review is truthful.
The host supplies actual worker results and verified storage receipts.
"""
import argparse
import copy
import fcntl
import json
import os
import re
import sys
from contextlib import contextmanager
from pathlib import Path

STAGES = ['request', 'source', 'draft', 'review', 'publish']
EXCLUDED = {'answer_key', 'author_solution', 'author_history', 'target_difficulty'}
REQUIRED_GATES = {'exam_scope', 'generation_source', 'similarity', 'product_quality'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def save(path, state):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temp, path)

@contextmanager
def lock(path):
    p = Path(str(path) + '.lock')
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield

def counts(state):
    items = state.get('draft', {}).get('items', [])
    reviews = {i['id']: i for i in state.get('review', {}).get('items', [])}
    checked = sum(i['id'] in reviews and reviews[i['id']]['sha256'] == i['sha256'] for i in items)
    passed = sum(i['id'] in reviews and reviews[i['id']]['sha256'] == i['sha256']
                 and reviews[i['id']]['pass'] for i in items)
    active = passed if state.get('publish', {}).get('mode') == 'verified' else 0
    return {'target': state['request']['count'], 'drafted': len(items), 'checked': checked,
            'eligible': passed, 'active': active}

def create(request, owner, manifest=None):
    for key in ['batch_id', 'subject', 'scope', 'product', 'ruleset_commit', 'count']:
        require(request.get(key) is not None, 'missing request field: ' + key)
    require(isinstance(request['count'], int) and not isinstance(request['count'], bool)
            and request['count'] > 0, 'count must be a positive integer')
    require(re.fullmatch(r'[0-9a-f]{40}', request['ruleset_commit']), 'pin a full ruleset commit SHA')
    require(bool(owner.strip()), 'owner required')
    return {'schema': 'ARC-RUN-V1', 'version': 1, 'owner': owner, 'stage': 'request',
            'status': 'READY', 'blockers': [], 'request': request,
            'manifest_paths': manifest or {}, 'events': [{'stage': 'request', 'actor': owner}]}

def unique(items):
    require(isinstance(items, list), 'items must be a list')
    ids = [i.get('id') for i in items]
    require(all(isinstance(i, str) and i.strip() for i in ids), 'non-empty item IDs required')
    require(len(ids) == len(set(ids)), 'duplicate item IDs')

# Explicit transition table: (current stage, event) -> stage after the event.
# This is the single source of truth for "what may happen next"; `machine` prints it
# for agents and `status` lists the events whose guards currently pass.
#   publish_draft  saves a review copy; the run stays open (stage unchanged, active=0).
#   publish        verified release; terminal (status DONE).
#   revise         post-review fix; the blind round is spent, so the run can only draft-publish.
TRANSITIONS = {
    ('request', 'source'): 'source',
    ('source', 'draft'): 'draft',
    ('draft', 'draft'): 'draft',
    ('draft', 'review'): 'review',
    ('draft', 'publish_draft'): 'draft',
    ('review', 'publish_draft'): 'review',
    ('review', 'revise'): 'draft',
    ('review', 'publish'): 'publish',
}
STATUSES = {
    'READY': 'next event may be recorded',
    'BLOCKED': 'last record failed its gate; fix the input and record again',
    'ON_HOLD': 'stopped by an explicit block; only unblock or transfer',
    'DONE': 'verified publication recorded; terminal',
}

def event_for(stage, payload):
    if stage == 'publish' and isinstance(payload, dict) and payload.get('mode') == 'draft':
        return 'publish_draft'
    return stage

def guard_failures(state, event):
    """Cheap preconditions that do not depend on the payload (payload checks live in validators)."""
    c = counts(state)
    if state.get('status') == 'ON_HOLD':
        return ['batch is ON_HOLD: ' + '; '.join(state.get('blockers', [])) + ' (run unblock first)']
    if state.get('status') == 'DONE':
        return ['batch is DONE']
    if (state['stage'], event) not in TRANSITIONS:
        return ['stage order violation: ' + event + ' not allowed after ' + state['stage']]
    if event == 'draft' and state['stage'] == 'draft' and c['drafted'] >= c['target']:
        return ['draft already complete (' + str(c['drafted']) + '/' + str(c['target']) + ')']
    if event == 'review':
        if c['drafted'] != c['target']:
            return ['complete draft before bundle review']
        if state.get('previous_review'):
            return ['blind round already used; post-review revision stays draft']
    if event == 'publish' and c['eligible'] != c['target']:
        return ['required content gates not passed']
    return []

def allowed_events(state):
    return [e for (s, e) in TRANSITIONS if s == state['stage'] and not guard_failures(state, e)]

def validate_source(state, payload):
    refs = payload.get('refs', [])
    require(refs and all(r.get('file_ref') and r.get('location') and r.get('verified') is True
                         for r in refs), 'verified source file and location required')
    return payload

def validate_draft(state, payload, append):
    if append:
        payload = dict(payload, items=state['draft']['items'] + payload.get('items', []))
    items = payload.get('items', [])
    unique(items)
    require(0 < len(items) <= state['request']['count'], 'draft count exceeds request or is empty')
    for item in items:
        require(item.get('student_ref') and re.fullmatch(r'[0-9a-f]{64}', item.get('sha256', '')),
                'student reference and manuscript SHA256 required')
        require(type(item.get('author_answer')) is int and item['author_answer'] in [1, 2, 3, 4, 5], 'five-choice author key required')
    return payload

def validate_review(state, payload):
    require(payload.get('rounds') == 1, 'one blind round required')
    require(payload.get('fresh_context') is True and EXCLUDED <= set(payload.get('excluded_inputs', [])),
            'blind isolation evidence incomplete')
    items = payload.get('items', [])
    unique(items)
    drafts = {i['id']: i for i in state['draft']['items']}
    require(set(drafts) == {i['id'] for i in items}, 'review IDs must match draft exactly')
    for item in items:
        draft = drafts[item['id']]
        require(item.get('sha256') == draft['sha256'], 'stale reviewed manuscript: ' + item['id'])
        require(type(item.get('answer')) is int and item['answer'] in [1, 2, 3, 4, 5], 'review answer required')
        verdicts = item.get('option_verdicts', [])
        require(len(verdicts) == 5 and all(type(v) is bool for v in verdicts)
                and sum(verdicts) == 1 and verdicts[item['answer'] - 1] and item.get('evidence_refs'),
                'all-option judgments and evidence required')
        item['pass'] = (item['answer'] == draft['author_answer']
                        and item.get('fact_pass') is True and item.get('scope_pass') is True
                        and item.get('quality_pass') is True)
    return payload

def validate_artifacts(payload):
    refs = payload.get('artifacts', [])
    require(refs and all(r.get('file_ref') and r.get('readback_verified') is True for r in refs),
            'actual persisted artifact and readback receipt required')

def validate_publish(state, payload):
    require(payload.get('mode') == 'verified', 'publish mode required')
    validate_artifacts(payload)
    receipts = payload.get('gate_receipts', {})
    require(all(receipts.get(g, {}).get('pass') is True and receipts[g].get('evidence_ref')
                for g in REQUIRED_GATES), 'scope/source/similarity/product gate receipts required')
    return payload

def apply(state, event, payload):
    """Run one event through the transition table; raises ValueError on any failed guard."""
    state = copy.deepcopy(state)
    require(isinstance(payload, dict), 'payload must be a JSON object')
    failures = guard_failures(state, event)
    require(not failures, failures[0] if failures else '')
    target = TRANSITIONS[(state['stage'], event)]
    if event == 'source':
        state['source'] = validate_source(state, payload)
    elif event == 'draft':
        state['draft'] = validate_draft(state, payload, append=state['stage'] == 'draft')
    elif event == 'review':
        state['review'] = validate_review(state, payload)
    elif event == 'revise':
        revised = validate_draft(state, payload, append=False)
        require([i['id'] for i in revised['items']] == [i['id'] for i in state['draft']['items']],
                'revision must preserve item IDs')
        state['draft'] = revised
        state['previous_review'] = state.pop('review')
    elif event == 'publish_draft':
        require(payload.get('mode') == 'draft', 'publish mode required')
        validate_artifacts(payload)
        c = counts(state)
        state.setdefault('draft_publications', []).append(
            dict(payload, drafted=c['drafted'], target=c['target']))
    elif event == 'publish':
        state['publish'] = validate_publish(state, payload)
    state['stage'] = target
    state['status'] = 'DONE' if event == 'publish' else 'READY'
    state['blockers'] = []
    return state

def advance(state, stage, payload):
    """Backward-compatible entry point: `stage` is the CLI --stage value."""
    require(stage in STAGES[1:], 'unknown stage')
    return apply(state, event_for(stage, payload), payload)

def machine():
    return {'stages': STAGES, 'statuses': STATUSES,
            'transitions': [{'from': s, 'event': e, 'to': t} for (s, e), t in TRANSITIONS.items()],
            'commands': {'record': 'source|draft|review|publish (publish mode=draft -> publish_draft)',
                         'revise': 'revise', 'block': 'any open status -> ON_HOLD',
                         'unblock': 'ON_HOLD -> READY', 'transfer': 'owner change, stage unchanged'}}

def handoff(state):
    stage = state['stage']
    nxt = STAGES[STAGES.index(stage) + 1] if stage != 'publish' else None
    if stage == 'draft' and counts(state)['drafted'] < state['request']['count']:
        nxt = 'draft'
    packet = {'batch_id': state['request']['batch_id'], 'to_stage': nxt,
              'ruleset_commit': state['request']['ruleset_commit'], 'scope': state['request']['scope'],
              'subject': state['request']['subject'], 'state_version': state['version'],
              'allowed_events': allowed_events(state)}
    if nxt == 'review':
        packet['items'] = [{k: i[k] for k in ['id', 'sha256', 'student_ref']} for i in state['draft']['items']]
        packet['source_refs'] = state['source']['refs']
        packet['excluded_inputs'] = sorted(EXCLUDED)
    else:
        packet['input_refs'] = state.get(stage, {})
    return packet

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['init', 'status', 'handoff', 'machine', 'record', 'revise', 'transfer', 'block', 'unblock'])
    p.add_argument('--state')
    p.add_argument('--input')
    p.add_argument('--manifest')
    p.add_argument('--actor')
    p.add_argument('--expected-version', type=int)
    p.add_argument('--stage', choices=STAGES[1:])
    p.add_argument('--new-owner')
    p.add_argument('--reason')
    args = p.parse_args(argv)
    if args.command == 'machine':
        print(json.dumps(machine(), ensure_ascii=False, indent=2))
        return 0
    if not args.state:
        p.error('--state is required')
    try:
        with lock(args.state):
            if args.command == 'init':
                require(not Path(args.state).exists(), 'existing batch state cannot be overwritten')
                require(args.input and args.actor, 'input and actor required')
                manifest = {}
                if args.manifest:
                    import yaml
                    m = yaml.safe_load(Path(args.manifest).read_text(encoding='utf-8'))
                    manifest = {'active': m.get('active', {}), 'runtime': m.get('runtime', {})}
                state = create(read(args.input), args.actor, manifest)
                save(args.state, state)
            else:
                state = read(args.state)
                if args.command == 'status':
                    print(json.dumps({'stage': state['stage'], 'status': state['status'],
                                      'owner': state['owner'], 'version': state['version'],
                                      'counts': counts(state), 'blockers': state['blockers'],
                                      'allowed_events': allowed_events(state),
                                      'draft_publications': len(state.get('draft_publications', []))},
                                     ensure_ascii=False))
                    return 0
                if args.command == 'handoff':
                    print(json.dumps(handoff(state), ensure_ascii=False, indent=2))
                    return 0
                require(args.actor == state['owner'], 'batch belongs to another worker')
                require(args.expected_version == state['version'], 'stale state version; reload before retry')
                if args.command == 'record':
                    require(args.stage and args.input, 'stage and input required')
                    require(state['status'] != 'ON_HOLD',
                            'batch is ON_HOLD: ' + '; '.join(state['blockers']) + ' (run unblock first)')
                    try:
                        state = advance(state, args.stage, read(args.input))
                    except ValueError as exc:
                        state['status'] = 'BLOCKED'
                        state['blockers'] = [str(exc)]
                        state['version'] += 1
                        state['events'].append({'actor': args.actor, 'failed_stage': args.stage, 'reason': str(exc)})
                        save(args.state, state)
                        raise
                elif args.command == 'revise':
                    require(state['stage'] == 'review' and args.input and args.reason,
                            'revise requires a reviewed draft, input and change reason')
                    state = apply(state, 'revise', read(args.input))
                    state['post_blind_edits'] = args.reason
                elif args.command == 'transfer':
                    require(args.new_owner and args.reason, 'explicit new owner and reason required')
                    state['owner'] = args.new_owner
                elif args.command == 'unblock':
                    require(state['status'] == 'ON_HOLD', 'only an ON_HOLD batch can be unblocked')
                    require(args.reason, 'unblock reason required')
                    state['status'], state['blockers'] = 'READY', []
                else:
                    require(args.reason, 'blocking reason required')
                    require(state['status'] != 'DONE', 'a DONE batch cannot be put on hold')
                    state['status'], state['blockers'] = 'ON_HOLD', [args.reason]
                state['version'] += 1
                state['events'].append({'actor': args.actor, 'command': args.command, 'stage': args.stage,
                                        'reason': args.reason})
                save(args.state, state)
            print(json.dumps({'state': args.state, 'version': state['version'], 'counts': counts(state)}))
            return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('ARC WORKFLOW BLOCKED: ' + str(exc), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
