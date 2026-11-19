#!/usr/bin/env python3
"""Deterministic completeness gate for ARC independent-solve QA evidence.

This runner cannot decide whether a literary interpretation or factual claim is
true. It makes the evidence-producing review auditable and blocks CONTENT_LOCK
when the required blind solve, option map, source trace, or difficulty evidence
is absent or internally inconsistent.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
SUBJECTS = {"KOR", "ENG", "SOC", "SCI", "HIS", "AI"}
VERDICTS = {"TRUE", "FALSE", "HALF_TRUE", "UNSUPPORTED"}
COMPETITIVENESS = {"STRONG", "MEDIUM", "WEAK", "CORRECT"}
DIFFICULTIES = {"D1", "D2", "D3", "D4", "D5"}
CONFIDENCE_LEVELS = {"HIGH", "MEDIUM", "LOW"}
SECOND_BEST_RISKS = {"HIGH", "MEDIUM", "LOW", "NONE"}
REQUIRED_EXCLUDED_INPUTS = {"ANSWER_KEY", "PASS_A", "AUTHOR_INTENT", "TARGET_DIFFICULTY"}
ITEM_GATES = {
    "FACTUAL_ACCURACY_REVIEW",
    "OPTION_SEMANTIC_DUPLICATION_REVIEW",
    "ANSWER_EVIDENCE_TRACE",
    "SCOPE_EVIDENCE_TRACE",
    "ALL_OPTION_AUDIT",
    "UNIQUE_ANSWER",
    "DIFFICULTY_MATCH",
}
SET_GATES = {
    "STRUCTURE",
    "ANSWER_COUNT_MATCH",
    "MANUSCRIPT_CONTAMINATION",
    "TOO_EASY",
    "MID_GAP",
    "STRUCTURE_BIAS",
    "D4_SHORT",
    "PASSAGE_TRUNCATION",
}
KOR_ALLOWED_ORIGINS = {
    "USER_UPLOAD",
    "USER_PROVIDED_SCHOOL_SUPPLEMENT",
    "USER_PROVIDED_TEXTBOOK",
    "CONNECTED_DRIVE_RAW_SCHOOL_SOURCE",
}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def load_payload(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("QA evidence root must be a mapping")
    return data


def finding(code: str, message: str, item_id: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"severity": "FAIL", "code": code, "message": message}
    if item_id:
        result["item_id"] = item_id
    return result


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0 and all(str(v).strip() for v in value)


def gate_failures(gates: Any, required: set[str], prefix: str, item_id: str | None = None) -> list[dict[str, Any]]:
    if not isinstance(gates, dict):
        return [finding(f"{prefix}_GATES_MISSING", f"{prefix} gates must be a mapping", item_id)]
    failures = []
    for name in sorted(required):
        if str(gates.get(name, "")).upper() != "PASS":
            failures.append(finding(f"{prefix}_{name}_NOT_PASS", f"{name} must equal PASS", item_id))
    return failures


def analyze_item(item: Any, item_format: str, subject: str = "") -> list[dict[str, Any]]:
    if not isinstance(item, dict):
        return [finding("ITEM_NOT_MAPPING", "Each item must be a mapping")]
    item_id = str(item.get("item_id", "")).strip() or "<missing>"
    findings: list[dict[str, Any]] = []
    pass_a = item.get("pass_a")
    pass_b = item.get("pass_b")
    if not isinstance(pass_a, dict) or not isinstance(pass_b, dict):
        return [finding("PASS_AB_MISSING", "pass_a and pass_b mappings are required", item_id)]

    answer_a = str(pass_a.get("answer", "")).strip()
    answer_b = str(pass_b.get("answer", "")).strip()
    if not answer_a or answer_a != answer_b:
        findings.append(finding("ANSWER_AB_MISMATCH", "PASS A and blind PASS B answers must match", item_id))
    if not nonempty_list(pass_a.get("answer_evidence")):
        findings.append(finding("PASS_A_EVIDENCE_MISSING", "PASS A answer_evidence is required", item_id))

    if pass_b.get("blind") is not True:
        findings.append(finding("PASS_B_NOT_BLIND", "PASS B must declare blind=true", item_id))
    excluded = {str(v).upper() for v in pass_b.get("excluded_inputs", []) if str(v).strip()}
    if not REQUIRED_EXCLUDED_INPUTS <= excluded:
        missing = sorted(REQUIRED_EXCLUDED_INPUTS - excluded)
        findings.append(finding("BLIND_INPUT_LEAK", f"PASS B excluded_inputs missing: {missing}", item_id))
    if not nonempty_list(pass_b.get("answer_evidence")):
        findings.append(finding("ANSWER_EVIDENCE_MISSING", "PASS B answer_evidence is required", item_id))
    if str(pass_b.get("confidence", "")).upper() not in CONFIDENCE_LEVELS:
        findings.append(finding("CONFIDENCE_INVALID", "PASS B confidence must be HIGH/MEDIUM/LOW", item_id))
    if not isinstance(pass_b.get("transfer_required"), bool):
        findings.append(finding("TRANSFER_FLAG_INVALID", "transfer_required must be boolean", item_id))

    scope = pass_b.get("scope_trace")
    if not isinstance(scope, dict) or str(scope.get("status", "")).upper() != "IN_SCOPE":
        findings.append(finding("SCOPE_TRACE_INVALID", "scope_trace.status must equal IN_SCOPE", item_id))
    elif not nonempty_list(scope.get("source_refs")):
        findings.append(finding("SCOPE_SOURCE_REFS_MISSING", "scope_trace.source_refs is required", item_id))

    option_judgments = pass_b.get("option_judgments")
    if item_format == "MCQ5" and (not isinstance(option_judgments, list) or len(option_judgments) != 5):
        findings.append(finding("OPTION_JUDGMENT_COUNT", "MCQ5 requires exactly five option judgments", item_id))
        option_judgments = option_judgments if isinstance(option_judgments, list) else []

    polarity = str(item.get("stem_polarity", "")).upper()
    if polarity not in {"POSITIVE", "NEGATIVE"} and subject == "KOR":
        findings.append(finding("STEM_POLARITY_MISSING", "KOR normative items require explicit POSITIVE/NEGATIVE polarity", item_id))
    if not polarity:
        polarity = "POSITIVE"  # legacy fixtures remain compatible; Korean reviewer must specify polarity
    if polarity not in {"POSITIVE", "NEGATIVE"}:
        findings.append(finding("STEM_POLARITY_INVALID", "stem_polarity must be POSITIVE/NEGATIVE", item_id))
    option_ids: list[str] = []
    true_ids: list[str] = []
    false_ids: list[str] = []
    uncertain_ids: list[str] = []
    semantic_keys: list[str] = []
    strong_distractors = 0
    for option in option_judgments or []:
        if not isinstance(option, dict):
            findings.append(finding("OPTION_JUDGMENT_INVALID", "Every option judgment must be a mapping", item_id))
            continue
        option_id = str(option.get("option_id", "")).strip()
        verdict = str(option.get("verdict", "")).upper()
        axis = str(option.get("axis", "")).strip().casefold()
        claim_key = str(option.get("claim_key", "")).strip().casefold()
        competitiveness = str(option.get("competitiveness", "")).upper()
        option_ids.append(option_id)
        if verdict == "TRUE":
            true_ids.append(option_id)
        elif verdict == "FALSE":
            false_ids.append(option_id)
        elif verdict in {"HALF_TRUE", "UNSUPPORTED"}:
            uncertain_ids.append(option_id)
        if verdict not in VERDICTS:
            findings.append(finding("OPTION_VERDICT_INVALID", f"Invalid verdict for option {option_id}", item_id))
        if competitiveness not in COMPETITIVENESS:
            findings.append(finding("OPTION_COMPETITIVENESS_INVALID", f"Invalid competitiveness for option {option_id}", item_id))
        elif option_id != answer_b and competitiveness == "STRONG":
            strong_distractors += 1
        if not axis or not claim_key:
            findings.append(finding("OPTION_SEMANTIC_KEY_MISSING", f"axis and claim_key required for option {option_id}", item_id))
        else:
            semantic_keys.append(f"{axis}::{claim_key}")
        if not nonempty_list(option.get("evidence_refs")):
            findings.append(finding("OPTION_EVIDENCE_MISSING", f"evidence_refs required for option {option_id}", item_id))

    if len(option_ids) != len(set(option_ids)):
        findings.append(finding("OPTION_ID_DUPLICATE", "Option IDs must be unique", item_id))
    if polarity == "NEGATIVE":
        if len(false_ids) != 1 or false_ids[0] != answer_b or len(true_ids) != 4:
            findings.append(finding("UNIQUE_ANSWER_INVALID", "Negative stem requires exactly one FALSE answer and four TRUE choices", item_id))
    elif len(true_ids) != 1 or (true_ids and true_ids[0] != answer_b):
        findings.append(finding("UNIQUE_ANSWER_INVALID", "Positive stem requires exactly one TRUE answer", item_id))
    if subject == "KOR" and uncertain_ids:
        findings.append(finding("KOR_OPTION_UNSUPPORTED", "KOR normative release cannot contain HALF_TRUE/UNSUPPORTED judgments", item_id))
    if len(semantic_keys) != len(set(semantic_keys)):
        findings.append(finding("OPTION_SEMANTIC_DUPLICATION", "Duplicate AXIS + CLAIM_KEY detected", item_id))

    second_best = str(pass_b.get("second_best_option", "")).strip()
    if not second_best or second_best == answer_b or second_best not in option_ids:
        findings.append(finding("SECOND_BEST_INVALID", "second_best_option must be a non-answer option", item_id))
    if str(pass_b.get("second_best_risk", "")).upper() not in SECOND_BEST_RISKS:
        findings.append(finding("SECOND_BEST_RISK_INVALID", "second_best_risk must be HIGH/MEDIUM/LOW/NONE", item_id))

    target = str(item.get("target_difficulty", "")).upper()
    actual = str(pass_b.get("actual_difficulty", "")).upper()
    if target not in DIFFICULTIES or actual not in DIFFICULTIES:
        findings.append(finding("DIFFICULTY_INVALID", "target and actual difficulty must be D1-D5", item_id))
    elif target != actual:
        findings.append(finding("DIFFICULTY_MISMATCH", f"target {target} != actual {actual}", item_id))

    reasoning_steps = pass_b.get("reasoning_steps")
    evidence_count = pass_b.get("evidence_count")
    immediate = pass_b.get("immediate_elimination_count")
    for field, value in (("reasoning_steps", reasoning_steps), ("evidence_count", evidence_count), ("immediate_elimination_count", immediate)):
        if not isinstance(value, int) or value < 0:
            findings.append(finding("DIFFICULTY_METRIC_INVALID", f"{field} must be a non-negative integer", item_id))

    if actual == "D3" and isinstance(reasoning_steps, int) and isinstance(immediate, int):
        if reasoning_steps < 1 or strong_distractors < 1 or immediate > 2:
            findings.append(finding("D3_SHORT", "D3 requires >=1 step, >=1 strong distractor, and <=2 immediate eliminations", item_id))
    if actual == "D4" and isinstance(reasoning_steps, int) and isinstance(immediate, int):
        if reasoning_steps < 2 or strong_distractors < 2 or immediate > 2:
            findings.append(finding("D4_SHORT", "D4 requires >=2 steps, >=2 strong distractors, and <=2 immediate eliminations", item_id))
    if actual == "D5" and all(isinstance(v, int) for v in (reasoning_steps, evidence_count, immediate)):
        if reasoning_steps < 3 or strong_distractors < 2 or evidence_count < 2 or immediate > 1:
            findings.append(finding("D5_MINIMUM_FAIL", "D5 minimum reasoning/evidence/distractor gate failed", item_id))

    findings.extend(gate_failures(item.get("gates"), ITEM_GATES, "ITEM", item_id))
    return findings


def analyze_korean_source_locks(data: dict[str, Any], item_ids: set[str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if data.get("uses_source_text") is not True:
        return findings
    locks = data.get("source_text_locks")
    if not isinstance(locks, list) or not locks:
        return [finding("KOR_SOURCE_LOCK_MISSING", "Korean source text requires source_text_locks")]
    for lock in locks:
        if not isinstance(lock, dict):
            findings.append(finding("KOR_SOURCE_LOCK_INVALID", "Each source lock must be a mapping"))
            continue
        source_id = str(lock.get("source_text_id", "<missing>"))
        if str(lock.get("source_origin", "")).upper() not in KOR_ALLOWED_ORIGINS:
            findings.append(finding("KOR_SOURCE_ORIGIN_FORBIDDEN", f"Forbidden source origin for {source_id}"))
        if str(lock.get("source_role", "")).upper() != "RAW_SCHOOL_SOURCE":
            findings.append(finding("KOR_SOURCE_ROLE_INVALID", f"{source_id} must use RAW_SCHOOL_SOURCE"))
        if str(lock.get("text_fidelity", "")).upper() != "EXACT":
            findings.append(finding("KOR_SOURCE_NOT_EXACT", f"{source_id} must use TEXT_FIDELITY=EXACT"))
        if not str(lock.get("source_file_id", "")).strip() or not str(lock.get("source_location", "")).strip():
            findings.append(finding("KOR_SOURCE_PROVENANCE_INCOMPLETE", f"{source_id} requires file ID and location"))
        if not SHA256_RE.fullmatch(str(lock.get("source_text_sha256", ""))):
            findings.append(finding("KOR_SOURCE_CHECKSUM_INVALID", f"{source_id} requires a SHA-256 checksum"))
        linked = lock.get("linked_item_ids")
        if not nonempty_list(linked) or not set(map(str, linked)) <= item_ids:
            findings.append(finding("KOR_SOURCE_LINKAGE_INVALID", f"{source_id} requires valid linked_item_ids"))
        for field in ("wording_lock", "punctuation_lock", "line_break_lock", "boundary_lock"):
            if lock.get(field) is not True:
                findings.append(finding("KOR_SOURCE_BOUNDARY_UNLOCKED", f"{source_id}.{field} must be true"))
    return findings


# ---------------------------------------------------------------------------
# Print-exam integrity lint (2026-11-19). Runs on the authored bundle text
# (items.yaml), not on QA evidence. Static PASS never replaces human review.
#   quality/ARC_VIEW_EVIDENCE_POLICY_V1.0.md
#   quality/ARC_SET_CROSS_ITEM_LEAK_GATE_V1.0.md
# ---------------------------------------------------------------------------
NORMATIVE_AXES = {"orthography", "spacing", "grammar", "pronunciation", "morphology", "phonology", "norm",
                  "word_formation", "standard_pronunciation", "loanword", "romanization"}
# Labels a normative <보기> may carry: official clause text or objective data only.
VIEW_ALLOWED_LABEL = re.compile(
    r"^\s*(?:\[(?:조항 원문|규정 원문|한글 맞춤법|표준어 규정|표준 발음법|외래어 표기법|로마자 표기법|발음 자료|사전 뜻풀이|"
    r"사전 자료|짜임 자료|형태소 자료|자료|예문|학생의 글|탐구 대화|대화)\]|제\s*\d+\s*항|<?(?:한글 맞춤법|표준 발음법|표준어 규정)|"
    r"[㉠-㉯ⓐ-ⓩⒶ-Ⓩㄱ-ㅎ]\s*[.:)]?\s|\(?[가-하]\)\s)")
VIEW_FORBIDDEN_LABEL = re.compile(r"\[(?:해설 ?자료|해설|풀이|풀이 ?자료|판별 ?기준|판단 ?기준|힌트|정리|요령|공식|팁)\]")
# A derived decision rule: condition + orthographic outcome.
VIEW_FORMULA = re.compile(
    r"(?:이면|라면|일 ?때|인 ?경우|하면|으면|는 경우)[^.。\n]{0,40}?"
    r"(?:탈락|줄어|줄여|붙여 ?(?:쓴|적)|띄어 ?(?:쓴|적)|(?:으로|로) ?적|소리 ?(?:나|난)|된소리|거센소리|사이시옷)")
QUOTED_PAIR = re.compile(r"[‘'“\"]([^‘’'“”\"]{1,30})[’'”\"]\s*(?:을|를)\s*[‘'“\"]([^‘’'“”\"]{1,30})[’'”\"]\s*(?:으로|로)")
ARROW_PAIR = re.compile(r"([가-힣A-Za-z]{1,20})\s*(?:→|->|⇒)\s*([가-힣A-Za-z]{1,20})")
DUP_WORD = re.compile(r"(?<![가-힣])([가-힣]{2,})\s+\1(?![가-힣])")
HANGUL = re.compile(r"[가-힣]")


def _final_jong(ch: str) -> int:
    code = ord(ch) - 0xAC00
    return code % 28 if 0 <= code < 11172 else -1


def spacing_anomalies(text: str) -> list[str]:
    """High-precision unintended-spacing patterns (dependent nouns written attached)."""
    hits: list[str] = []
    for m in re.finditer(r"([가-힣])(게|수|것)(\s*)(남|있|없|많|아니|뭐|같)", text):
        pre, noun, gap, nxt = m.groups()
        jong = _final_jong(pre)
        if noun in {"게", "수"} and jong == 8:          # ㄹ-final: 할게 남아 / 할수 있다
            hits.append(m.group(0))
        elif noun == "것" and jong in {4, 8}:           # ㄴ/ㄹ-final: 한것 같다 / 할것 없다
            hits.append(m.group(0))
    for m in re.finditer(r"([가-힣])(수)(있|없)", text):   # 할수있다
        if _final_jong(m.group(1)) == 8 and m.group(0) not in hits:
            hits.append(m.group(0))
    return hits


def _norm(text: str) -> str:
    return re.sub(r"[^가-힣A-Za-z0-9]", "", str(text))


def _texts(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        out: list[str] = []
        for v in value:
            out.extend(_texts(v))
        return out
    if isinstance(value, dict):
        out = []
        for v in value.values():
            out.extend(_texts(v))
        return out
    return [str(value)]


def is_normative(item: dict[str, Any], bundle: dict[str, Any]) -> bool:
    if item.get("normative") is not None:
        return bool(item["normative"])
    if bundle.get("v6") or item.get("v6_area") or str(item.get("domain", "")).upper() in {"GRAMMAR", "NORM"}:
        return True
    axes = {str(j.get("axis", "")).casefold() for j in item.get("judgments") or [] if isinstance(j, dict)}
    return bool(axes & NORMATIVE_AXES)


def _edit1(a: str, b: str) -> bool:
    return len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1


def lint_bundle_text(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    """Static print-exam integrity lint over an items.yaml bundle.

    Returns findings with severity FAIL/WARN and codes:
      VIEW_SOLUTION_LABEL, VIEW_SOLUTION_FORMULA (no-hint view, normative items)
      OPTION_SELF_IDENTICAL_CORRECTION, UNINTENDED_SPACING_ERROR, DUPLICATE_WORD, WHITESPACE_ANOMALY
      HEADWORD_MISSING (declared `headwords` absent; near-miss spelling reported)
      CROSS_ITEM_ANSWER_LEAK, CROSS_ITEM_EXAMPLE_REUSE (set-level)
    """
    findings: list[dict[str, Any]] = []
    items = [it for it in bundle.get("items") or [] if isinstance(it, dict)]

    def add(code: str, severity: str, message: str, item_id: str | None = None, **extra: Any) -> None:
        findings.append({"code": code, "severity": severity, "message": message, **({"item_id": item_id} if item_id else {}), **extra})

    for it in items:
        iid = str(it.get("item_id", ""))
        normative = is_normative(it, bundle)
        options = [str(o) for o in it.get("options") or []]
        authored = {"stem": _texts(it.get("stem")), "view": _texts(it.get("view")), "options": options,
                    "conditions": _texts(it.get("conditions")), "model_answer": _texts(it.get("model_answer"))}

        # 1. No-hint view (normative items only; literature views may carry interpretive context).
        if normative:
            for line in authored["view"]:
                for raw in str(line).splitlines():
                    if VIEW_FORBIDDEN_LABEL.search(raw):
                        add("VIEW_SOLUTION_LABEL", "FAIL", f"<보기>에 해설·판별 공식 자료 표지: {raw[:40]}", iid)
                    elif VIEW_FORMULA.search(raw) and not VIEW_ALLOWED_LABEL.match(raw):
                        # A view that restates official clauses must cite them (`view_clause_refs`);
                        # the reviewer then confirms the wording is clause text, not a derived shortcut.
                        sev = "WARN" if it.get("view_clause_refs") else "FAIL"
                        add("VIEW_SOLUTION_FORMULA", sev, f"<보기>에 조항 원문이 아닌 판별 공식 의심: {raw[:50]}", iid)

        # 2. Self-identical corrections anywhere in student text.
        for field, texts in authored.items():
            for text in texts:
                for a, b in QUOTED_PAIR.findall(text) + ARROW_PAIR.findall(text):
                    if a.strip() == b.strip():
                        add("OPTION_SELF_IDENTICAL_CORRECTION", "FAIL", f"{field}: '{a}'를 '{b}'로 — 고치기 전후가 같음", iid)

        # 3. Unintended spacing errors. In normative items a deliberate error is acknowledged when
        #    (a) it sits right after a target mark (㉠, ⓐ, [ ...) in the view/options, or
        #    (b) a judgment names the fragment or its corrected form, or (c) `intended_errors` lists it.
        judgments = [j for j in it.get("judgments") or [] if isinstance(j, dict)]
        declared = [str(x) for x in it.get("intended_errors") or []]
        judgment_text = _norm(" ".join(_texts([j.get("why") for j in judgments] + [j.get("claim") for j in judgments])))
        for field, texts in authored.items():
            for idx, text in enumerate(texts):
                for hit in spacing_anomalies(text):
                    core = _norm(hit[:2])
                    pos = text.find(hit)
                    near_mark = pos >= 0 and re.search(r"[㉠-㉯ⓐ-ⓩⒶ-Ⓩ\[][^㉠-㉯ⓐ-ⓩⒶ-Ⓩ\[\]]{0,14}$", text[max(0, pos - 15):pos + 1]) is not None
                    acknowledged = normative and field in {"options", "view"} and (
                        near_mark or core in judgment_text
                        or any(_norm(hit) in _norm(d) or _norm(d) in _norm(hit) for d in declared))
                    if not acknowledged:
                        loc = f"{field}[{idx + 1}]" if field == "options" else field
                        add("UNINTENDED_SPACING_ERROR", "FAIL", f"{loc}: 의도하지 않은 붙여쓰기 의심 '{hit}'", iid)
                for m in DUP_WORD.finditer(text):
                    add("DUPLICATE_WORD", "WARN", f"{field}: 같은 단어 연속 '{m.group(0)}'", iid)
                if re.search(r"[가-힣]  +[가-힣]|\s+[.,?!](?!\.)", text):
                    add("WHITESPACE_ANOMALY", "WARN", f"{field}: 이중 공백 또는 문장부호 앞 공백", iid)

        # 4. Declared headwords must appear; report near-miss spellings (곗날 → 옛날).
        student = " ".join(t for texts in authored.values() for t in texts)
        tokens = set(re.findall(r"[가-힣]+", student))
        for hw in it.get("headwords") or []:
            hw = str(hw).strip()
            if hw and hw not in student:
                near = sorted(t for t in tokens if any(_edit1(hw, t[i:i + len(hw)]) for i in range(0, max(1, len(t) - len(hw) + 1))))
                add("HEADWORD_MISSING", "FAIL", f"계획 표제어 '{hw}'가 학생 텍스트에 없음" + (f" (유사 표기: {', '.join(near[:3])})" if near else ""), iid)

    # 5. Set-level cross-item leak: a constructed-response answer printed in another item.
    def student_text(it: dict[str, Any]) -> str:
        return " ".join(_texts(it.get("stem")) + _texts(it.get("view")) + [str(o) for o in it.get("options") or []])

    for cr in items:
        if str(cr.get("format", "")).upper() not in {"CR", "CONSTRUCTED", "SHORT_ANSWER"}:
            continue
        explicit = [str(x) for x in cr.get("answer_targets") or []]
        auto: list[str] = []
        for text in _texts(cr.get("model_answer")):
            auto += re.findall(r"[‘'“\"]([^‘’'“”\"]{2,40})[’'”\"]", text)
        for text in _texts(cr.get("accepted_variants")):
            auto += [re.sub(r"^[ⓐ-ⓩ㉠-㉯A-Za-z0-9.)\s]+", "", part).strip() for part in re.split(r"[/,]", text)]
        targets = [(t, True) for t in explicit if _norm(t)] + [(t, False) for t in auto if len(_norm(t)) >= 3]
        normative = is_normative(cr, bundle) or bool(bundle.get("v6"))
        for other in items:
            if other is cr:
                continue
            other_text = _norm(student_text(other))
            for target, is_explicit in targets:
                if _norm(target) and _norm(target) in other_text:
                    sev = "FAIL" if (normative or is_explicit) else "WARN"
                    add("CROSS_ITEM_ANSWER_LEAK", sev, f"서답형 {cr.get('item_id')}의 답 '{target}'이 {other.get('item_id')}에 그대로 실림", str(cr.get("item_id")),
                        leaked_in=other.get("item_id"))
        if normative:
            cr_text = _norm(" ".join(_texts(cr.get("stem")) + _texts(cr.get("view")) + _texts(cr.get("conditions"))))
            for other in items:
                if other is cr or str(other.get("format", "")).upper() in {"CR", "CONSTRUCTED", "SHORT_ANSWER"}:
                    continue
                for option in [str(o) for o in other.get("options") or []] + _texts(other.get("view")):
                    o = _norm(re.sub(r"[\[\]]", "", option))
                    if len(o) >= 6 and any(o[i:i + 6] in cr_text for i in range(0, len(o) - 5)):
                        add("CROSS_ITEM_EXAMPLE_REUSE", "FAIL", f"서답형 {cr.get('item_id')}가 {other.get('item_id')}의 예문을 다시 씀: {option[:30]}",
                            str(cr.get("item_id")), reused_from=other.get("item_id"))
                        break
    return findings


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    subject = str(data.get("subject", "")).upper()
    item_format = str(data.get("item_format", "")).upper()
    items = data.get("items")
    item_count = data.get("item_count")

    if data.get("schema_version") != "ARC-QA-EVIDENCE-V1.0":
        findings.append(finding("SCHEMA_VERSION_INVALID", "schema_version must be ARC-QA-EVIDENCE-V1.0"))
    if subject not in SUBJECTS:
        findings.append(finding("SUBJECT_INVALID", "subject must be KOR/SOC/HIS/SCI/AI"))
    if item_format != "MCQ5":
        findings.append(finding("ITEM_FORMAT_UNSUPPORTED", "V1.0 executable gate supports MCQ5"))
    if not isinstance(items, list) or not isinstance(item_count, int) or item_count != len(items):
        findings.append(finding("ITEM_COUNT_MISMATCH", "item_count must equal the number of items"))
        items = items if isinstance(items, list) else []

    item_ids = [str(item.get("item_id", "")).strip() for item in items if isinstance(item, dict)]
    if any(not item_id for item_id in item_ids) or len(item_ids) != len(set(item_ids)):
        findings.append(finding("ITEM_ID_INVALID", "Every item_id must be non-empty and unique"))
    for item in items:
        findings.extend(analyze_item(item, item_format, subject))

    findings.extend(gate_failures(data.get("set_gates"), SET_GATES, "SET"))
    if subject == "KOR":
        findings.extend(analyze_korean_source_locks(data, set(item_ids)))
    if data.get("content_lock") is not True:
        findings.append(finding("CONTENT_LOCK_NOT_REQUESTED", "Final QA evidence must request content_lock=true"))

    status = "FAIL" if findings else "PASS"
    return {
        "tool": "ARC_CONTENT_QA_GATE_V1.0",
        "status": status,
        "subject": subject or None,
        "item_count": len(items),
        "fail_count": len(findings),
        "content_lock_allowed": status == "PASS",
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(load_payload(args.evidence))
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
