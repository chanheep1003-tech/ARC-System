#!/usr/bin/env python3
"""ARC REFERENCE 문항은행 레지스트리 빌더 (Phase 1: 메타데이터 단계).

입력(수집 CSV)은 저장소에 두지 않고 인자로 받는다. 표준 라이브러리만 사용한다.
  python3 bank/tools/build_register.py --judge J.csv --gaya G.csv --sources S1.csv S2.csv

문항 본문·선지는 입력에도 없고 출력에도 쓰지 않는다. 정답·난도는 입력에 있는 값만 옮기고 추정하지 않는다.
"""
import argparse
import csv
import hashlib
import os
import re
import sys
from collections import Counter, defaultdict

BANK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CIRCLED = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5'}

ITEM_COLUMNS = [
    'item_id', 'legacy_item_id', 'subject', 'phase', 'concept_id', 'concept_secondary', 'mapping_basis', 'scope_codes',
    'scope_status', 'range_confirmed', 'origin_level', 'source_id', 'source_type', 'provider', 'source_title',
    'exam_year', 'grade', 'origin_subject', 'source_locator', 'question_url', 'explanation_url', 'body_access',
    'body_reviewed', 'question_form', 'asset_type', 'asset_type_basis', 'visual_required', 'answer', 'answer_source',
    'answer_check', 'difficulty', 'difficulty_score', 'difficulty_method', 'solvable_with_current_knowledge', 'blocked_knowledge_tag',
    'cluster_id', 'dup_role', 'reuse_mode', 'status', 'review_flags', 'review_pass', 'notes',
]
CLUSTER_COLUMNS = ['cluster_id', 'subject', 'concept_id', 'basis', 'size', 'canonical_item_id', 'member_item_ids', 'key_sample']

# 2026-10-04 세션에서 HEAD 요청으로 확인한 도메인별 접근 결과 (재확인 필요)
DOMAIN_ACCESS = {
    'wdown.ebsi.co.kr': 'EXTERNAL_PDF_REACHABLE',
    'www.suneung.re.kr': 'EXTERNAL_PDF_REACHABLE',
    'www.kcue.or.kr': 'EXTERNAL_PDF_REACHABLE',
    'textbook.gimmyoung.com': 'EXTERNAL_PDF_REACHABLE',
    'files-scs.pstatic.net': 'EXTERNAL_PDF_UNREACHABLE',
    'www.goe.go.kr': 'EXTERNAL_PDF_UNREACHABLE',
}

KNOWN_INPUTS = {
    '1FfJDPEbaUvS3vUOnzQxoa6L2f3IohsT9': 'ARC_추가분_전체판정.csv',
    '1xmPdU_z5Q-ztnIMluFJC4H5y7Utl4NIF': 'ARC_학교기출_정답교정.csv',
    '1FYY-CZlLjOeLcAUpIEeDQhV_C-ri126N': 'SCI_COLLECTOR_20261003_BATCH02/SOURCES.csv',
    '1gLbtopR32yaKLvv6WRPq6_IXcTN8kHEh': 'SOC_COLLECTOR_20261003_BATCH02/SOURCES.csv',
}


def read_csv(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    return [{(k or '').strip(): (v or '').strip() for k, v in r.items()} for r in rows]


def write_csv(path, columns, rows):
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction='raise', lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, '') for c in columns})


class Knowledge:
    """bank/ 의 데이터 파일(개념표·매핑·규칙·보류 키워드)을 로드한다."""

    def __init__(self, bank):
        self.concepts = {r['concept_id']: r for r in read_csv(os.path.join(bank, 'concepts.csv'))}
        self.crosswalk = {(r['key_type'], r['key']): r for r in read_csv(os.path.join(bank, 'scope_crosswalk.csv'))}
        self.rules = defaultdict(list)
        for r in read_csv(os.path.join(bank, 'concept_rules.csv')):
            rx = re.compile(r['regex']) if r['regex'] else None
            self.rules[r['group']].append((int(r['order']), r['concept_id'], rx))
        for g in self.rules:
            self.rules[g].sort(key=lambda x: x[0])
        self.blocked = [(r['tag'], r['subject'], re.compile(r['regex'])) for r in read_csv(os.path.join(bank, 'blocked_knowledge.csv'))]
        self.topics = {(r['source_id'], r['topic']): r for r in read_csv(os.path.join(bank, 'manual_topic_map.csv'))}
        for (key, ktype) in [(k, v) for k, v in self.crosswalk.items()]:
            tgt = ktype['target']
            if tgt.startswith('GROUP:'):
                assert tgt[6:] in self.rules, 'rule group missing: ' + tgt
            else:
                assert tgt in self.concepts, 'concept missing: ' + tgt
        for g, lst in self.rules.items():
            for _, cid, _ in lst:
                assert cid in self.concepts, 'rule concept missing: ' + cid

    def resolve_group(self, group, *texts):
        """텍스트를 점점 넓혀가며 키워드에 걸리는 개념을 순서대로 반환. 없으면 default."""
        rules = self.rules[group]
        default = [cid for _, cid, rx in rules if rx is None][0]
        acc = ''
        for t in texts:
            acc = (acc + ' ' + t).strip()
            hits = [cid for _, cid, rx in rules if rx is not None and rx.search(acc)]
            if hits:
                return hits
        return [default]

    def resolve_scope(self, scope_str, text_primary, text_wide):
        out, unit1, unknown = [], False, []
        for key in re.split(r'[;,]', scope_str):
            key = key.strip()
            if not key:
                continue
            if re.match(r'^10통(과|사)1-', key):
                unit1 = True
                continue
            m = re.match(r'^(?:SCI|SOC)-C-(10통[과사]2-\d\d-\d\d)$', key)
            if m:
                ktype, k = 'CODE', m.group(1)
            elif re.match(r'^10통[과사]2-\d\d-\d\d$', key):
                ktype, k = 'CODE', key
            elif re.match(r'^(?:SCI|SOC)-[MS]\d\d$', key):
                ktype, k = 'SCOPE', key
            else:
                unknown.append(key)
                continue
            entry = self.crosswalk.get((ktype, k))
            if not entry:
                unknown.append(key)
                continue
            tgt = entry['target']
            if tgt.startswith('GROUP:'):
                cids = self.resolve_group(tgt[6:], text_primary, text_wide)
                basis = 'CODE_UNIT_KEYWORD_CONCEPT' if ktype == 'CODE' else 'KEYWORD_COLLECTOR_UNIT'
            else:
                cids = [tgt]
                basis = 'CODE_DIRECT' if ktype == 'CODE' else 'KEYWORD_COLLECTOR_UNIT'
            for cid in cids:
                out.append((cid, basis, entry['needs_scope_check'] == 'Y'))
        seen, uniq = set(), []
        for c in out:
            if c[0] not in seen:
                seen.add(c[0])
                uniq.append(c)
        return uniq, unit1, unknown


def norm_answer(v):
    v = (v or '').strip()
    if v in CIRCLED:
        return CIRCLED[v]
    return v if re.fullmatch(r'[1-5]', v) else ''


def norm_form(v):
    if re.search(r'서술|논술|서답', v) and not v.startswith('UNKNOWN'):
        return '서술형'
    if v.startswith('객관식') or v == '선택형':
        return '선택형'
    return 'UNKNOWN'


def origin_level_of(gs):
    if gs.startswith('상위학년'):
        return 'UPPER'
    if gs.startswith('고1 통합 교과'):
        return 'LEGACY_G1'
    if gs.startswith('고1 통합'):
        return 'CURRENT'
    return 'UNKNOWN'


def origin_subject_of(row, level):
    m = re.search(r"원본 과목 '([^']+)'", row.get('extra_prerequisite', ''))
    if m:
        return m.group(1)
    if level in ('CURRENT', 'LEGACY_G1'):
        return '통합과학' if row['subject'] == 'SCI' else '통합사회'
    return ''


ASSET_RX = [
    ('graph', re.compile('그래프')),
    ('particle_model', re.compile('입자')),
    ('experiment_diagram', re.compile('실험')),
    ('map', re.compile('지도')),
    ('table', re.compile('도표|(?<![가-힣])표(?![가-힣])')),
]


def asset_of(visual, text):
    if visual == 'NO':
        return 'none', 'VISUAL_REQUIRED_FIELD'
    for name, rx in ASSET_RX:
        if rx.search(text):
            return name, 'KEYWORD_GUESS'
    if visual in ('YES', 'YES_LIKELY'):
        return 'unknown', 'VISUAL_REQUIRED_FIELD'
    return 'unknown', 'NONE'


def domain_of(url):
    m = re.match(r'^https?://([^/]+)', url or '')
    return m.group(1) if m else ''


def body_access_of(asset_status, url):
    if asset_status == 'EXISTING_DRIVE_ORIGINAL':
        return 'DRIVE_ORIGINAL'
    return DOMAIN_ACCESS.get(domain_of(url), 'EXTERNAL_PDF_UNVERIFIED' if url else 'NONE')


def decide(item, concepts, unit1, unknown, needs_check, leak_tags, origin_ii, record_ok):
    """scope_status / status 를 규칙대로 결정한다. 반환: (scope_status, status, extra_notes)"""
    notes = []
    if not record_ok:
        return 'OUT_OF_SCOPE', 'EXCLUDED', ['비문항 참고자료']
    if not concepts:
        if unit1:
            return 'OUT_OF_SCOPE', 'EXCLUDED', ['통합과학1/통합사회1 성취기준 코드만 해당']
        if unknown:
            return 'NEEDS_SCOPE_CHECK', 'HOLD', ['매핑표에 없는 범위 키: ' + ';'.join(unknown)]
        return 'OUT_OF_SCOPE', 'EXCLUDED', ['트랙 개념에 매핑되지 않음']
    level = item['origin_level']
    if unit1:
        notes.append('통합1 성취기준 코드가 함께 걸림 — 통합1 지식 필요 여부 본문 확인 필요')
    if needs_check or unit1:
        scope = 'NEEDS_SCOPE_CHECK'
    elif level == 'UPPER':
        scope = 'ADVANCED_BLOCKED' if (leak_tags or origin_ii) else 'EXTENDED_CANDIDATE'
    else:
        scope = 'IN_SCOPE'
    if scope == 'ADVANCED_BLOCKED':
        notes.append('키워드 근거 보류(' + ','.join(leak_tags + (['ORIGIN_II'] if origin_ii else [])) + ') — 본문 확인 시 해제 가능')
    if scope in ('NEEDS_SCOPE_CHECK', 'ADVANCED_BLOCKED'):
        status = 'HOLD'
    elif item['answer']:
        status = 'NEEDS_BODY_REVIEW'
    else:
        status = 'NEEDS_ANSWER'
    return scope, status, notes


def build_judge_items(rows, src_by_id, K):
    items = []
    for r in rows:
        subj = r['subject']
        level = origin_level_of(r['grade_suitability'])
        text1 = r['concept_keywords'] + ' ' + r['testable_point']
        concepts, unit1, unknown = K.resolve_scope(r['scope_id'], text1, r['item_summary'])
        primary = concepts[0] if concepts else None
        pc = K.concepts[primary[0]] if primary else None
        src = src_by_id.get(r['source_id'], {})
        origin_sub = origin_subject_of(r, level)
        origin_ii = bool(re.search(r'(Ⅱ|II)$', origin_sub))
        text_all = text1 + ' ' + r['item_summary']
        leak = []
        if subj == 'SCI' and level == 'UPPER':
            leak = [t for t, s, rx in K.blocked if s == subj and rx.search(text_all)]
        asset, asset_basis = asset_of(r['visual_required'], text_all)
        ans = norm_answer(r['official_answer'])
        provider = src.get('provider', '')
        role = src.get('role', '')
        if role in ('OFFICIAL_REFERENCE', 'OFFICIAL_GUIDE'):
            stype, reuse = 'OFFICIAL_ASSESS', 'DIRECT_OK'
        elif provider == 'EBSi':
            stype, reuse = 'EXAM_NATIONAL', 'ADAPT_ONLY'
        else:
            stype, reuse = 'UNKNOWN', 'ADAPT_ONLY'
        item = {
            'legacy_item_id': r['item_id'], 'subject': subj,
            'phase': pc['phase'] if pc else '',
            'concept_id': primary[0] if primary else '',
            'concept_secondary': ';'.join(c[0] for c in concepts[1:]),
            'mapping_basis': primary[1] if primary else 'NONE',
            'scope_codes': r['scope_id'], 'range_confirmed': pc['range_confirmed'] if pc else '',
            'origin_level': level, 'source_id': r['source_id'], 'source_type': stype, 'provider': provider,
            'source_title': r['source_title'], 'exam_year': r['year'], 'grade': r['grade'], 'origin_subject': origin_sub,
            'source_locator': 'PDF p.%s / Q%s' % (r['pdf_page'], r['question_number']),
            'question_url': r['question_url'], 'explanation_url': r['explanation_url'],
            'body_access': body_access_of(r['asset_status'], r['question_url'] or src.get('download_url', '')),
            'body_reviewed': 'N', 'question_form': norm_form(r['question_form']),
            'asset_type': asset, 'asset_type_basis': asset_basis, 'visual_required': r['visual_required'],
            'answer': ans, 'answer_source': 'OFFICIAL_KEY' if ans and r['answer_verification'].startswith('OFFICIAL') else 'NONE',
            'answer_check': r['answer_verification'], 'difficulty': 'UNRATED', 'difficulty_method': 'UNRATED',
            'blocked_knowledge_tag': ';'.join(leak + (['ORIGIN_II'] if origin_ii else [])),
            'reuse_mode': reuse,
        }
        if ans and item['answer_source'] == 'NONE':
            item['answer'] = ''
            item['notes'] = '정답 값은 있으나 검증 등급이 OFFICIAL이 아니어서 미채택'
        scope, status, notes = decide(item, concepts, unit1, unknown,
                                      any(c[2] and c[0] == (primary[0] if primary else None) for c in concepts) if primary else False,
                                      leak, origin_ii, r['record_type'] == 'QUESTION')
        if r['status'] == 'EXCLUDED_SUBJECT1_OR_ADVANCED' and scope in ('IN_SCOPE', 'EXTENDED_CANDIDATE'):
            # 수집 단계의 제외 판정(통합1 영역 또는 상위학년 지식)을 승계한다. 키워드 매핑이 이를 되살리면 안 된다.
            scope, status = ('ADVANCED_BLOCKED' if level == 'UPPER' else 'NEEDS_SCOPE_CHECK'), 'HOLD'
            if level == 'UPPER':
                item['blocked_knowledge_tag'] = ';'.join(t for t in [item['blocked_knowledge_tag'], 'COLLECTOR_ADVANCED'] if t)
            notes.append('수집 단계 판정 EXCLUDED_SUBJECT1_OR_ADVANCED 승계 — 본문 확인 시 해제 가능')
        item['scope_status'], item['status'] = scope, status
        if (r['record_type'] == 'QUESTION' and primary and K.concepts[primary[0]]['subject'] == subj
                and re.match(r'^SOC-C-', primary[0]) and pc['phase'] == 'MIDTERM'):
            notes.append('C 학습지 X 표시 영역과 겹치는지 시각 확인 필요(SOCIAL_MASTER §2-1)')
        prev = r['duplicate_previous_item']
        if prev:
            item['dup_role'], item['cluster_id'] = 'DUPLICATE', 'XREF-' + prev
            notes.append('이전 수집 색인 %s와 중복(원 색인은 본 레지스트리에 없음)' % prev)
            if item['status'] not in ('EXCLUDED', 'HOLD'):
                item['status'] = 'HOLD'
        else:
            item['dup_role'] = 'UNCLUSTERED'
        if item['status'] == 'EXCLUDED':
            item['dup_role'], item['cluster_id'] = 'UNCLUSTERED', ''
        item['notes'] = ' | '.join([n for n in [item.get('notes', '')] + notes if n])
        item['_tp'] = r['testable_point']
        items.append(item)
    return items


def build_gaya_items(rows, K):
    items = []
    for r in rows:
        subj = r['subject']
        topic_row = K.topics.get((r['source_id'], r['topic']))
        notes = []
        if not topic_row:
            raise SystemExit('manual_topic_map.csv에 없는 주제: %s %s' % (r['source_id'], r['topic']))
        ans = norm_answer(r['official_answer'])
        prov = norm_answer(r['provided_answer'])
        if ans and prov and ans != prov:
            notes.append('원 제공 정답 %s → 교정 %s(%s)' % (prov, ans, r['answer_check']))
        out = topic_row['out_of_scope'] == 'Y'
        cid = topic_row['concept_id']
        concept = K.concepts.get(cid) if cid else None
        # 원 CSV 내부 불일치 기록
        if '1' == r['unit'][-1:] and '2' in r['mapping'] and not out:
            notes.append('원 CSV unit=%s이나 mapping="%s" — 불일치. 성취기준 코드 매핑표 기준으로 판정' % (r['unit'], r['mapping']))
        if out and r['unit'][-1:] == '2' and '1 참고' in r['mapping']:
            notes.append('원 CSV unit=%s이나 mapping="%s" — 불일치. mapping 기준 제외' % (r['unit'], r['mapping']))
        if out:
            scope, status = 'OUT_OF_SCOPE', 'EXCLUDED'
            notes.append(topic_row['note'])
        else:
            scope = 'IN_SCOPE'
            status = 'NEEDS_BODY_REVIEW' if ans else 'NEEDS_ANSWER'
        if r['form'] == '서술형':
            notes.append('서술형 정답·채점기준 미확보')
        if concept and re.match(r'^SOC-C-', cid):
            notes.append('C 학습지 X 표시 영역 시각 확인 필요')
        items.append({
            'legacy_item_id': 'GAYA_%s_%s' % (subj, r['number'].replace(' ', '')), 'subject': subj,
            'phase': concept['phase'] if concept else '', 'concept_id': cid, 'concept_secondary': topic_row['concept_secondary'],
            'mapping_basis': 'TOPIC_MANUAL' if concept else 'NONE', 'scope_codes': '',
            'range_confirmed': concept['range_confirmed'] if concept else '', 'origin_level': 'SCHOOL',
            'scope_status': scope, 'source_id': r['source_id'], 'source_type': 'SCHOOL_FINAL', 'provider': '가야고등학교',
            'source_title': '가야고 2024 기말 ' + ('통합과학' if subj == 'SCI' else '통합사회'), 'exam_year': '2024', 'grade': '',
            'origin_subject': '통합과학' if subj == 'SCI' else '통합사회',
            'source_locator': '%s / 문항 %s' % (r['question_locator'], r['number']), 'question_url': '', 'explanation_url': '',
            'body_access': 'SCHOOL_SEPARATED_PDF', 'body_reviewed': 'N', 'question_form': norm_form(r['form']),
            'asset_type': 'unknown', 'asset_type_basis': 'NONE', 'visual_required': 'UNKNOWN',
            'answer': ans, 'answer_source': 'OFFICIAL_KEY' if ans else 'NONE', 'answer_check': r['answer_check'],
            'difficulty': 'UNRATED', 'difficulty_method': 'UNRATED', 'blocked_knowledge_tag': '', 'cluster_id': '',
            'dup_role': 'UNCLUSTERED', 'reuse_mode': 'CALIBRATION_ONLY', 'status': status,
            'notes': ' | '.join(n for n in notes if n), '_tp': r['topic'],
        })
    return items


def cluster_items(items):
    """같은 (과목, 주 개념, 정규화한 평가목표 문구) 를 한 묶음으로 본다. 문구 일치 기준이라 보수적이며,
    구조 수준 묶음은 본문 확보 후 Phase 2에서 확장한다."""
    def norm(s):
        return re.sub(r'[\s\.\,·ㆍ\-\(\)\[\]]', '', s)

    def rank(it):
        return (0 if it['status'].startswith('READY') else 1, 0 if it['reuse_mode'] == 'DIRECT_OK' else 1, 0 if it['answer'] else 1,
                0 if it['body_access'] == 'DRIVE_ORIGINAL' else 1, -int(it['exam_year'] or 0), it['legacy_item_id'])

    groups = defaultdict(list)
    for it in items:
        if it['dup_role'] == 'UNCLUSTERED' and it['status'] != 'EXCLUDED' and it['concept_id'] and it['_tp'].strip():
            groups[(it['subject'], it['concept_id'], norm(it['_tp']))].append(it)
    clusters, n = [], defaultdict(int)
    for key in sorted(groups):
        members = sorted(groups[key], key=rank)
        n[key[0]] += 1
        cid = 'CL-%s-%04d' % (key[0], n[key[0]])
        for i, it in enumerate(members):
            it['cluster_id'] = cid
            it['dup_role'] = 'CANONICAL' if i == 0 else 'VARIANT'
        clusters.append({'cluster_id': cid, 'subject': key[0], 'concept_id': key[1], 'basis': 'TESTABLE_POINT_EXACT',
                         'size': len(members), 'canonical_item_id': members[0]['item_id'],
                         'member_item_ids': ';'.join(m['item_id'] for m in members), 'key_sample': members[0]['_tp'][:60]})
    return clusters


def assign_ids(items):
    items.sort(key=lambda it: (it['subject'], natural(it['legacy_item_id'])))
    per = Counter()
    for it in items:
        per[it['subject']] += 1
        it['item_id'] = 'BREF-%s-%06d' % (it['subject'], per[it['subject']])


def natural(s):
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def write_manifest(paths, counts):
    lines = ['# SOURCES_MANIFEST', '', '`build_register.py` 입력 파일(저장소에 포함하지 않음). 입력은 Drive `N제 시스템` 수집 결과이며 파일 이름은 Drive 파일 ID다.', '',
             '|파일(Drive ID)|원래 이름|행 수(헤더 제외)|바이트|sha256|', '|---|---|---:|---:|---|']
    for p in paths:
        fid = os.path.splitext(os.path.basename(p))[0]
        lines.append('|%s|%s|%d|%d|%s|' % (fid, KNOWN_INPUTS.get(fid, '?'), counts[p], os.path.getsize(p), sha256(p)))
    lines += ['', '레지스트리 재생성: `python3 bank/tools/build_register.py --judge <전체판정.csv> --gaya <정답교정.csv> --sources <SOURCES.csv ...>`', '']
    with open(os.path.join(BANK, 'SOURCES_MANIFEST.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--judge', required=True)
    ap.add_argument('--gaya', required=True)
    ap.add_argument('--sources', nargs='+', required=True)
    ap.add_argument('--bank-dir', default=BANK)
    a = ap.parse_args()
    K = Knowledge(a.bank_dir)
    judge, gaya = read_csv(a.judge), read_csv(a.gaya)
    src = {}
    src_rows = 0
    counts = {a.judge: len(judge), a.gaya: len(gaya)}
    for p in a.sources:
        rows = read_csv(p)
        counts[p] = len(rows)
        for r in rows:
            src.setdefault(r['source_id'], r)
    items = build_judge_items(judge, src, K) + build_gaya_items(gaya, K)
    assign_ids(items)
    review_dir = os.path.join(a.bank_dir, 'review')
    if os.path.isdir(review_dir):
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import apply_review
        print('review applied', apply_review.apply(items, review_dir, K.concepts))
    clusters = cluster_items(items)
    for subj in ('SCI', 'SOC'):
        write_csv(os.path.join(a.bank_dir, 'items_%s.csv' % subj), ITEM_COLUMNS, [i for i in items if i['subject'] == subj])
        write_csv(os.path.join(a.bank_dir, 'clusters_%s.csv' % subj), CLUSTER_COLUMNS, [c for c in clusters if c['subject'] == subj])
    write_manifest([a.judge, a.gaya] + a.sources, counts)
    print('items', len(items), Counter(i['subject'] for i in items))
    print('status', Counter(i['status'] for i in items).most_common())
    print('scope_status', Counter(i['scope_status'] for i in items).most_common())
    print('clusters', len(clusters), 'size>1', sum(1 for c in clusters if c['size'] > 1))


if __name__ == '__main__':
    sys.exit(main())
