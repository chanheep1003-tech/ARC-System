"""Phase 2 검토 결과를 레지스트리 항목에 반영한다. build_register.py 가 군집화 전에 호출한다.

입력(bank/review/, 저장소에 포함 — 판정값만 있고 문항 본문은 없다):
  p1.jsonl                  1차 독립 풀이·범위·난도·개념 판정 (rubric 형식)
  p2.jsonl                  2차 독립 풀이(검증용, 일부 문항만)
  official_answers.csv      해설지 정답표에서 읽은 공식 정답 (item_id, answer, source)

원칙: 공식 정답은 있으면 쓰고, 없으면 독립 풀이 2회가 일치할 때만 SOLVED_2PASS 로 인정한다.
READY 는 본문 검토·정답 검증·난도 평가·범위 판정이 모두 끝난 문항뿐이다. 범위 미확정(range_confirmed=N)이면 READY_PENDING_RANGE.
"""
import csv
import json
import os

BANDS = [(24, 'D1'), (44, 'D2'), (64, 'D3'), (79, 'D4'), (100, 'D5')]
LIM = {'A': 20, 'B': 25, 'C': 20, 'D': 15, 'E': 10, 'F': 10}
ASSETS = {'none', 'passage', 'table', 'graph', 'particle_model', 'experiment_diagram', 'map', 'flowchart', 'composite'}


def read_jsonl(path):
    out = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                d = json.loads(line)
                out[d['item_id']] = d
    return out


def band(score):
    for hi, name in BANDS:
        if score <= hi:
            return name
    return 'D5'


def valid_scores(sc):
    return isinstance(sc, dict) and all(isinstance(sc.get(k), int) and 0 <= sc[k] <= v for k, v in LIM.items())


def apply(items, review_dir, concepts):
    p1 = read_jsonl(os.path.join(review_dir, 'p1.jsonl'))
    p2 = read_jsonl(os.path.join(review_dir, 'p2.jsonl'))
    official = {}
    path = os.path.join(review_dir, 'official_answers.csv')
    if os.path.exists(path):
        with open(path, encoding='utf-8-sig', newline='') as f:
            official = {r['item_id']: r['answer'] for r in csv.DictReader(f)}
    stats = {'reviewed': 0}
    for it in items:
        iid = it['item_id']
        # 공식 정답 보강(해설지 정답표). 레지스트리에 이미 정답이 있으면 건드리지 않는다.
        if not it['answer'] and iid in official:
            it['answer'], it['answer_source'], it['answer_check'] = official[iid], 'OFFICIAL_KEY', 'OFFICIAL_ANSWER_TABLE_PARSED_P2'
            if it['status'] == 'NEEDS_ANSWER':
                it['status'] = 'NEEDS_BODY_REVIEW'
        r1 = p1.get(iid)
        if not r1:
            continue
        stats['reviewed'] += 1
        r2 = p2.get(iid)
        flags = set(r1.get('flags') or [])
        notes = []
        body_y = r1.get('body_ok') == 'Y'
        it['body_reviewed'] = 'Y' if body_y else 'N'
        it['review_pass'] = 'P1+P2' if r2 else 'P1'
        if r2:
            flags |= set(r2.get('flags') or [])
        if not body_y:
            notes.append('본문 검토 %s(%s)' % (r1.get('body_ok', '?'), ','.join(sorted(flags)) or '사유 없음'))

        # 개념 재배정
        cid = it['concept_id']
        if r1.get('concept_fit') == 'MISFIT' or (r1.get('concept_fit') == 'PARTIAL' and r1.get('suggested_concept') not in ('', None)):
            sug = r1.get('suggested_concept') or ''
            if r1.get('concept_fit') == 'MISFIT' and sug == 'OUT':
                it['scope_status'], it['status'] = 'OUT_OF_SCOPE', 'EXCLUDED'
                notes.append('검토: 배정 개념 %s와 무관, 트랙 개념 없음' % cid)
            elif sug in concepts and concepts[sug]['subject'] == it['subject'] and sug != cid:
                if r1.get('concept_fit') == 'MISFIT':
                    notes.append('검토: 개념 %s→%s 재배정' % (cid, sug))
                    it['concept_id'], it['mapping_basis'] = sug, 'REVIEW_REASSIGNED'
                    it['phase'], it['range_confirmed'] = concepts[sug]['phase'], concepts[sug]['range_confirmed']
                    sec = [s for s in it['concept_secondary'].split(';') if s and s != sug]
                    it['concept_secondary'] = ';'.join(sec)
                else:
                    sec = [s for s in it['concept_secondary'].split(';') if s]
                    if sug not in sec:
                        sec.append(sug)
                    it['concept_secondary'] = ';'.join(sec)

        # 형태·자료형
        if body_y:
            if r1.get('form') in ('선택형', '서술형'):
                it['question_form'] = r1['form']
            if r1.get('asset_type') in ASSETS:
                it['asset_type'], it['asset_type_basis'] = r1['asset_type'], 'REVIEW'

        # 풀이 가능성·범위
        rj = r1.get('range_judgement')
        it['solvable_with_current_knowledge'] = {'WITHIN': 'Y', 'BEYOND': 'N'}.get(rj, 'UNSURE')
        if it['scope_status'] not in ('OUT_OF_SCOPE', 'NEEDS_SCOPE_CHECK', 'BLOCKED_USER_X'):
            if rj == 'BEYOND':
                it['scope_status'] = 'ADVANCED_BLOCKED'
                it['blocked_knowledge_tag'] = ';'.join(t for t in [it['blocked_knowledge_tag'], 'REVIEW_BEYOND'] if t)
                notes.append('검토: 범위 초과 지식 필요(%s)' % ','.join(r1.get('knowledge_needed') or []))
            elif rj == 'WITHIN' and it['origin_level'] == 'UPPER' and it['scope_status'] == 'EXTENDED_CANDIDATE':
                it['scope_status'] = 'EXTENDED_SOLVABLE'

        # 정답 검증
        blinds = [d.get('answer_blind', '') for d in (r1, r2) if d and d.get('answer_blind')]
        verified, key_problem = False, False
        if it['answer_source'] == 'OFFICIAL_KEY' and it['answer']:
            agree = sum(1 for b in blinds if b == it['answer'])
            disagree = sum(1 for b in blinds if b != it['answer'])
            if agree and not disagree:
                verified = True
            elif agree and disagree:
                key_problem = True
                flags.add('ANSWER_SPLIT')
            elif disagree:
                key_problem = True
                flags.add('KEY_DISPUTE')
        elif not it['answer'] and r2 and r1.get('answer_blind') and r1.get('answer_blind') == r2.get('answer_blind') \
                and r1.get('answer_conf') != 'L' and r2.get('answer_conf') != 'L':
            it['answer'], it['answer_source'], it['answer_check'] = r1['answer_blind'], 'SOLVED_2PASS', 'INDEPENDENT_2PASS_AGREE'
            verified = True
        if flags & {'ANSWER_AMBIGUOUS', 'NO_VALID_ANSWER', 'CONDITION_MISSING'}:
            key_problem = True

        # 난도
        sc = r1.get('scores')
        if body_y and valid_scores(sc):
            total = sum(sc[k] for k in LIM)
            it['difficulty'], it['difficulty_score'], it['difficulty_method'] = band(total), str(total), 'STRUCTURAL'

        # 상태
        if it['scope_status'] == 'OUT_OF_SCOPE':
            it['status'] = 'EXCLUDED'
        elif it['scope_status'] in ('ADVANCED_BLOCKED', 'NEEDS_SCOPE_CHECK') or it['dup_role'] == 'DUPLICATE' or key_problem:
            it['status'] = 'HOLD'
        elif (body_y and verified and it['difficulty'] != 'UNRATED' and it['scope_status'] in ('IN_SCOPE', 'EXTENDED_SOLVABLE')
              and it['solvable_with_current_knowledge'] == 'Y'):
            it['status'] = 'READY' if it['range_confirmed'] == 'Y' else 'READY_PENDING_RANGE'
        else:
            it['status'] = 'NEEDS_BODY_REVIEW' if it['answer'] else 'NEEDS_ANSWER'
        it['review_flags'] = ';'.join(sorted(flags))
        if r1.get('note'):
            notes.append('검토: ' + r1['note'])
        it['notes'] = ' | '.join(n for n in [it['notes']] + notes if n)
    return stats
