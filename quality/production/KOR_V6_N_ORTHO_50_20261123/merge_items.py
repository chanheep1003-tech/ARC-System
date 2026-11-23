"""ARC N° V6 한글 맞춤법 50문항(객관식) 한 세트 묶음 — 세트 1~4 원본 번들을 순서대로 합쳐 1~50번으로 다시 번호를 매긴다.
원본: KOR_V6_N_ORTHO_SET1~4_20261123/items.yaml (각 generate 스크립트로 생성). 저장소 루트에서 실행."""
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
items = []
for n in range(1, 5):
    src = yaml.safe_load((ROOT / f"KOR_V6_N_ORTHO_SET{n}_20261123" / "items.yaml").read_text(encoding="utf-8"))
    for it in src["items"]:
        it = dict(it)
        it["source_item_id"] = it["item_id"]
        it["item_id"] = f"KOR-V6N-{len(items) + 1:03d}"
        it["family"] = {"A2_STUDENT_TEXT_ERRORS": "ERROR_CORRECTION",
                        "A6_RULE_CASE_EXPLANATION": "CASE_APPLICATION"}.get(it["archetype"], it["family"])
        items.append(it)
assert len(items) == 50
bundle = {
    "batch_id": "KOR-V6-N-ORTHO-50-20261123", "product_mode": "ARC_N", "subject": "KOR", "generator": "CLAUDE",
    "set_label": "ARC N° V6", "course": "공통국어2",
    "cover_subtitle": "한글 맞춤법 50문항 (전 문항 객관식)",
    "cover_lines": ["1~12 조사·보조사 / 의존 명사 / 어미",
                    "13~24 접미사·어미 vs 의존 명사, 단위·수·열거·호칭",
                    "25~36 형태 밝혀 적기·된소리·사이시옷·준말·구별 표기",
                    "37~50 생활 문장 종합"],
    "school_line": "동북고등학교 1학년 · 2026", "created_at": "2026-11-23T16:00:00+09:00",
    "scope": "미래엔 공통국어2 3단원 한글 맞춤법 (2026 2학기 기말 범위, 학교 공지 2026-11-13)",
    "scope_refs": ["TEXTBOOK:미래엔 공통국어2 3-(2) 한글 맞춤법과 오늘날의 국어생활, 한글 맞춤법 제1·2·5·15·19·30·35·39~46·48·57항"],
    "archetype_library": "quality/korean/ARC_KOR_GRAMMAR_ARCHETYPES_V1.0.yaml",
    "v6": {"policy": "quality/korean/ARC_KOR_V6_UNFAMILIAR_EXPRESSION_ORTHOGRAPHY_V1.0.md",
           "set": "단일 50문항 (사용자 지시 2026-11-23: 한 세트로 묶음)",
           "user_override": "전 50문항 객관식(서답형 0), 단원 세트 분할 대신 한 세트", "blind_review": "NOT_RUN"},
    "sets": [], "items": items}
out = Path(__file__).with_name("items.yaml")
out.write_text(yaml.safe_dump(bundle, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
print(f"wrote {out} ({len(items)} items)")
