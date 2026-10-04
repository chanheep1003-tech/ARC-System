#!/usr/bin/env python3
"""bank/ 레지스트리 검증. 하드 규칙 위반이 하나라도 있으면 종료코드 1.

열거값은 schema.yaml 의 items_columns 에서 읽는다(스키마가 단일 기준).
  python3 bank/tools/validate.py
"""
import csv
import os
import re
import sys
from collections import Counter, defaultdict

BANK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def read_csv(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def load_schema():
    enums, columns, in_items = {}, [], False
    with open(os.path.join(BANK, 'schema.yaml'), encoding='utf-8') as f:
        for line in f:
            if re.match(r'^items_columns:', line):
                in_items = True
                continue
            if in_items and re.match(r'^\S', line):
                break
            m = re.match(r'^  (\w+):\s+(.*)$', line)
            if in_items and m:
                columns.append(m.group(1))
                e = re.match(r'^\[(.+?)\]', m.group(2))
                if e:
                    enums[m.group(1)] = {x.strip() for x in e.group(1).split(',')}
    return columns, enums


def main():
    columns, enums = load_schema()
    concepts = {r['concept_id']: r for r in read_csv(os.path.join(BANK, 'concepts.csv'))}
    errors = []

    def err(msg):
        if len(errors) < 60:
            errors.append(msg)

    all_items = []
    for subj in ('SCI', 'SOC'):
        path = os.path.join(BANK, 'items_%s.csv' % subj)
        with open(path, encoding='utf-8-sig', newline='') as f:
            header = next(csv.reader(f))
        if header != columns:
            err('%s: 컬럼이 schema.yaml 과 다름: %s' % (path, [c for c in header if c not in columns] + [c for c in columns if c not in header]))
        for r in read_csv(path):
            r['_file'] = subj
            all_items.append(r)

    ids = Counter(i['item_id'] for i in all_items)
    legacy = Counter(i['legacy_item_id'] for i in all_items)
    for k, v in ids.items():
        if v > 1:
            err('item_id 중복: ' + k)
    for k, v in legacy.items():
        if v > 1:
            err('legacy_item_id 중복: ' + k)

    for i in all_items:
        iid = i['item_id']
        if i['subject'] != i['_file']:
            err('%s: subject와 파일 불일치' % iid)
        if not re.fullmatch(r'BREF-%s-\d{6}' % i['subject'], iid):
            err('%s: item_id 형식' % iid)
        for col, allowed in enums.items():
            if col in i and i[col] != '' and i[col] not in allowed:
                err('%s: %s=%r 는 허용값 아님' % (iid, col, i[col]))
        cid = i['concept_id']
        if cid:
            c = concepts.get(cid)
            if not c:
                err('%s: concept_id %s 가 concepts.csv에 없음' % (iid, cid))
            else:
                if c['subject'] != i['subject']:
                    err('%s: 개념 과목 불일치' % iid)
                if i['phase'] != c['phase'] or i['range_confirmed'] != c['range_confirmed']:
                    err('%s: phase/range_confirmed 가 개념표와 다름' % iid)
        for s in filter(None, i['concept_secondary'].split(';')):
            if s not in concepts:
                err('%s: concept_secondary %s 미등록' % (iid, s))
        # 정답
        if i['question_form'] == '선택형' and i['answer'] and not re.fullmatch(r'[1-5]', i['answer']):
            err('%s: 선택형 정답 형식 %r' % (iid, i['answer']))
        if i['question_form'] == '서술형' and i['answer']:
            err('%s: 서술형인데 정답 값이 있음' % iid)
        if bool(i['answer']) != (i['answer_source'] in ('OFFICIAL_KEY', 'SOLVED_2PASS')):
            err('%s: answer 와 answer_source 불일치' % iid)
        # 하드 규칙
        st, sc = i['status'], i['scope_status']
        if st == 'READY':
            need = [i['body_reviewed'] == 'Y', i['answer_source'] in ('OFFICIAL_KEY', 'SOLVED_2PASS'),
                    sc in ('IN_SCOPE', 'EXTENDED_SOLVABLE'), i['range_confirmed'] == 'Y', i['difficulty'] != 'UNRATED']
            if not all(need):
                err('%s: READY 조건 미충족 %s' % (iid, need))
        if sc in ('OUT_OF_SCOPE', 'BLOCKED_USER_X') and st != 'EXCLUDED':
            err('%s: %s 인데 status=%s' % (iid, sc, st))
        if sc in ('ADVANCED_BLOCKED', 'NEEDS_SCOPE_CHECK') and st not in ('HOLD', 'EXCLUDED'):
            err('%s: %s 인데 status=%s' % (iid, sc, st))
        if i['difficulty_method'] == 'UNRATED' and i['difficulty'] != 'UNRATED':
            err('%s: 난도가 근거 없이 채워짐' % iid)
        if i['dup_role'] == 'DUPLICATE' and st not in ('HOLD', 'EXCLUDED'):
            err('%s: DUPLICATE 인데 status=%s' % (iid, st))
        if st == 'EXCLUDED' and i['dup_role'] in ('CANONICAL', 'VARIANT'):
            err('%s: EXCLUDED 가 묶음 구성원' % iid)
        if i['body_reviewed'] == 'Y' and i['answer_source'] == 'NONE' and st == 'READY':
            err('%s: 정답 없이 READY' % iid)
        if sc == 'IN_SCOPE' and not cid:
            err('%s: IN_SCOPE 인데 개념 없음' % iid)

    # 묶음
    members = defaultdict(list)
    for i in all_items:
        if i['cluster_id'] and not i['cluster_id'].startswith('XREF-'):
            members[i['cluster_id']].append(i)
    cl_rows = []
    for subj in ('SCI', 'SOC'):
        cl_rows += read_csv(os.path.join(BANK, 'clusters_%s.csv' % subj))
    cl_ids = {c['cluster_id'] for c in cl_rows}
    if len(cl_ids) != len(cl_rows):
        err('cluster_id 중복')
    for c in cl_rows:
        m = members.get(c['cluster_id'], [])
        canon = [x for x in m if x['dup_role'] == 'CANONICAL']
        if len(canon) != 1:
            err('%s: CANONICAL 이 %d건' % (c['cluster_id'], len(canon)))
        elif canon[0]['item_id'] != c['canonical_item_id']:
            err('%s: canonical_item_id 불일치' % c['cluster_id'])
        if int(c['size']) != len(m):
            err('%s: size 불일치' % c['cluster_id'])
    for cid in members:
        if cid not in cl_ids:
            err('%s: clusters 파일에 없는 cluster_id' % cid)

    print('items', len(all_items), dict(Counter(i['subject'] for i in all_items)))
    print('READY', sum(1 for i in all_items if i['status'] == 'READY'), '| clusters', len(cl_rows))
    if errors:
        print('FAIL', len(errors), '건 (최대 60건 표시)')
        for e in errors:
            print(' -', e)
        return 1
    print('PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
