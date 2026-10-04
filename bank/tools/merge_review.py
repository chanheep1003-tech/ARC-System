#!/usr/bin/env python3
"""검토 에이전트 결과(jsonl)와 해설지 정답표 파싱 결과를 bank/review/ 에 병합한다.

- p1.jsonl: 배치 결과를 합친 것. 본문·선지는 없고 판정값(정답 풀이, 범위, 난도 점수, 개념 적합성)만 있다.
  rubric 의 허용 키만 남기고 note/range_reason 은 80자로 자른다.
- official_answers.csv: 해설지 정답표에서 읽은 공식 정답(item_id, answer, source).
  이미 레지스트리에 정답이 있는 문항은 apply_review 가 건드리지 않는다.
  python3 bank/tools/merge_review.py --results <results 디렉터리> --parsed <parsed_answers.json>
"""
import argparse
import csv
import glob
import json
import os

BANK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
KEEP = ['item_id', 'body_ok', 'form', 'answer_blind', 'answer_conf', 'knowledge_needed', 'range_judgement', 'range_reason',
        'concept_fit', 'suggested_concept', 'asset_type', 'structure', 'scores', 'flags', 'note']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results')
    ap.add_argument('--parsed')
    a = ap.parse_args()
    out = os.path.join(BANK, 'review')
    os.makedirs(out, exist_ok=True)
    if a.results:
        merged = {}
        for path in sorted(glob.glob(os.path.join(a.results, '*.jsonl'))):
            for line in open(path, encoding='utf-8'):
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                row = {k: d.get(k) for k in KEEP}
                for k in ('note', 'range_reason', 'structure'):
                    if isinstance(row.get(k), str):
                        row[k] = row[k][:80]
                merged[d['item_id']] = row
        with open(os.path.join(out, 'p1.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
            for iid in sorted(merged):
                f.write(json.dumps(merged[iid], ensure_ascii=False) + '\n')
        print('p1.jsonl', len(merged))
    if a.parsed:
        ans = json.load(open(a.parsed, encoding='utf-8'))['answers']
        with open(os.path.join(out, 'official_answers.csv'), 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(['item_id', 'answer', 'source'])
            for iid in sorted(ans):
                w.writerow([iid, ans[iid], 'EBSi 해설지 정답표(자동 파싱, 기존 공식 정답 364건과 전수 일치로 보정)'])
        print('official_answers.csv', len(ans))


if __name__ == '__main__':
    main()
