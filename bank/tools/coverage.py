#!/usr/bin/env python3
"""bank/ 레지스트리에서 트랙·개념별 부족 분석(COVERAGE_GAP_*.md)을 생성한다. 재실행하면 같은 결과가 나온다.

'후보 풀'은 status 가 NEEDS_BODY_REVIEW 또는 NEEDS_ANSWER 인 문항이다(HOLD·EXCLUDED 제외).
본문 검토(body_reviewed=Y)가 끝난 READY 문항만 '출제 가능'으로 센다. 기준 숫자는 가정이며 아래 상수로 조정한다.
판정은 두 가지를 나란히 낸다.
  - 엄격: 고2·3 선택과목(UPPER) 문항을 뺀 풀. 현재 교육과정 문항·학교 시험지만 센다.
  - 확장: UPPER 를 포함한 풀. 현재 지식으로 풀리는지 아직 검증하지 않은 문항이 섞여 있어 낙관적이다.
  python3 bank/tools/coverage.py
"""
import csv
import os
import sys
from collections import Counter

BANK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
TARGET_PROTOTYPES = 6      # 개념당 후보 원형(묶음) 수 — 두 세트 이상을 중복 없이 구성할 수 있다는 가정
LOW_PROTOTYPES = 3         # 이 미만이면 CRITICAL
POOL_STATUS = ('READY', 'READY_PENDING_RANGE', 'NEEDS_BODY_REVIEW', 'NEEDS_ANSWER')
ACCESSIBLE = ('DRIVE_ORIGINAL', 'EXTERNAL_PDF_REACHABLE', 'SCHOOL_SEPARATED_PDF')


def read_csv(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def prototypes(items):
    """묶음 수. 묶음이 없는 문항은 1건당 1개로 센다."""
    seen, n = set(), 0
    for i in items:
        c = i['cluster_id']
        if c and not c.startswith('XREF-'):
            if c not in seen:
                seen.add(c)
                n += 1
        else:
            n += 1
    return n


def level(protos):
    if protos < LOW_PROTOTYPES:
        return 'CRITICAL'
    if protos < TARGET_PROTOTYPES:
        return 'LOW'
    return 'OK'


def render(subj, items, concepts):
    title = {'SCI': '통합과학2', 'SOC': '통합사회2'}[subj]
    ready = [i for i in items if i['status'] == 'READY']
    pool = [i for i in items if i['status'] in POOL_STATUS]
    L = ['# COVERAGE_GAP_%s — %s 기출 후보 부족 분석 (잠정)' % (subj, title), '',
         '> `bank/tools/coverage.py` 가 생성한 파일이다. 직접 고치지 말고 레지스트리를 고친 뒤 재생성한다.', '',
         '**읽는 법.** 본문 검토가 끝난 문항(READY)은 현재 **%d건**이다. 아래 숫자는 모두 "후보 풀"(본문·정답 미검토, HOLD·EXCLUDED 제외) 기준의 **잠정치**다. '
         '판정 기준(가정): 개념당 후보 원형 ≥ %d이면 OK, %d~%d이면 LOW, < %d이면 CRITICAL.' % (len(ready), TARGET_PROTOTYPES, LOW_PROTOTYPES, TARGET_PROTOTYPES - 1, LOW_PROTOTYPES),
         '**엄격**은 고2·3 선택과목 문항을 뺀 풀(현재 교육과정 문항·학교 시험지), **확장**은 그 문항을 포함한 풀이다. 확장은 "현재 지식으로 풀리는가"를 아직 검증하지 못해 낙관적이다.', '']
    L += ['## 1. 전체 현황', '', '|구분|건수|', '|---|---:|']
    L.append('|레지스트리 전체|%d|' % len(items))
    for st in ('READY', 'READY_PENDING_RANGE', 'NEEDS_BODY_REVIEW', 'NEEDS_ANSWER', 'HOLD', 'EXCLUDED'):
        L.append('|status=%s|%d|' % (st, sum(1 for i in items if i['status'] == st)))
    L += ['', '후보 풀 %d건 중 본문을 지금 도구로 열 수 있는 것: **%d건** (`DRIVE_ORIGINAL`·`EXTERNAL_PDF_REACHABLE`·`SCHOOL_SEPARATED_PDF`).' %
          (len(pool), sum(1 for i in pool if i['body_access'] in ACCESSIBLE)), '']
    for phase, label in (('MIDTERM', '중간 트랙 (SCOPE_LEDGER, 범위 확정)'), ('FINAL_REMAINDER', '기말 후보 트랙 (중간 제외 나머지, 범위 미확정 — READY 불가)')):
        L += ['## 2. %s' % label, '',
              '|개념|우선순위|전체|후보 풀|원형(엄격)|원형(확장)|풀 중 정답 보유|HOLD|판정(엄격)|판정(확장)|', '|---|---|---:|---:|---:|---:|---:|---:|---|---|']
        strict_gaps, hidden = [], []
        for cid, c in concepts.items():
            if c['subject'] != subj or c['phase'] != phase:
                continue
            allm = [i for i in items if i['concept_id'] == cid]
            pl = [i for i in allm if i['status'] in POOL_STATUS]
            strict = [i for i in pl if i['origin_level'] != 'UPPER']
            p_s, p_e = prototypes(strict), prototypes(pl)
            l_s, l_e = level(p_s), level(p_e)
            if l_s != 'OK':
                strict_gaps.append((p_s, cid, l_s))
            if l_s != l_e:
                hidden.append('%s(%s→%s)' % (cid, l_s, l_e))
            L.append('|%s|%s|%d|%d|%d|%d|%d|%d|%s|%s|' % (
                cid, c['priority'], len(allm), len(pl), p_s, p_e, sum(1 for i in pl if i['answer']),
                sum(1 for i in allm if i['status'] == 'HOLD'), l_s, l_e))
        L.append('')
        if strict_gaps:
            L.append('부족 개념(엄격 기준, 적은 순): ' + ', '.join('%s(%d, %s)' % (c, p, lv) for p, c, lv in sorted(strict_gaps)))
            L.append('')
        if hidden:
            L.append('확장 기준에서만 부족이 가려지는 개념(고2·3 문항 풀이 가능성 검증이 해결의 열쇠): ' + ', '.join(hidden))
            L.append('')
    L += ['## 3. 후보 풀 구성', '', '|origin_level|건수|', '|---|---:|']
    for k, v in Counter(i['origin_level'] for i in pool).most_common():
        L.append('|%s|%d|' % (k, v))
    L += ['', '|reuse_mode|건수|', '|---|---:|']
    for k, v in Counter(i['reuse_mode'] for i in pool).most_common():
        L.append('|%s|%d|' % (k, v))
    L += ['', '|asset_type (기준)|건수|', '|---|---:|']
    for k, v in Counter('%s (%s)' % (i['asset_type'], i['asset_type_basis']) for i in pool).most_common():
        L.append('|%s|%d|' % (k, v))
    L += ['', '|question_form|건수|', '|---|---:|']
    for k, v in Counter(i['question_form'] for i in pool).most_common():
        L.append('|%s|%d|' % (k, v))
    L += ['', '난도(D1~D5) 분포는 **산출 불가**: 후보 풀 %d건 모두 `UNRATED`다. 본문 검토(Phase 2) 후에 채운다.' % len(pool), '']
    L += ['## 4. 해석상 한계', '',
          '- 개념 배정은 대부분 수집 단계의 키워드 범위(`KEYWORD_COLLECTOR_UNIT`)에서 나왔다. 성취기준 코드 기반(`CODE_*`)·수동(`TOPIC_MANUAL`) 배정은 소수다. '
          '고2·3 선택과목 문항(`UPPER`)은 요지·출제의도 텍스트만 본 판정이라 실제로 현재 지식으로 풀리는지는 본문을 봐야 안다.',
          '- 중간 트랙의 후보가 적은 것은 수집 지시가 "중간 제외 나머지"였기 때문이다. 중간 트랙 보강은 학교 시험지·교재(Drive에 있으나 아직 문항 단위로 색인되지 않은 자료)가 필요하다.',
          '- 후보 원형은 평가목표 문구가 같은 것끼리 묶은 값이다. 구조 수준 묶음은 본문 확보 후 다시 한다.',
          '- 자료형(그래프·입자모형 등)은 대부분 `unknown`이라 자료형별 부족은 아직 판단할 수 없다.', '']
    return '\n'.join(L)


def main():
    concepts = {r['concept_id']: r for r in read_csv(os.path.join(BANK, 'concepts.csv'))}
    for subj in ('SCI', 'SOC'):
        items = read_csv(os.path.join(BANK, 'items_%s.csv' % subj))
        with open(os.path.join(BANK, 'COVERAGE_GAP_%s.md' % subj), 'w', encoding='utf-8', newline='\n') as f:
            f.write(render(subj, items, concepts))
        print('wrote COVERAGE_GAP_%s.md' % subj)


if __name__ == '__main__':
    sys.exit(main())
