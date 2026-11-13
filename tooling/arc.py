#!/usr/bin/env python3
"""ARC 단일 진입 CLI — 실사용에 필요한 반복 작업을 한 곳에 모은다.

    python tooling/arc.py doctor                 실행 환경 점검 (의존성·폰트)
    python tooling/arc.py status                 국어·사회·과학 × CORE/N/FINAL 준비 상태
    python tooling/arc.py plan   --subject KOR --scope "한글 맞춤법"      제작 계획(버전·문항 수·난도·원형)
    python tooling/arc.py start  --subject SCI --product ARC_N --count 20 --scope "산화·환원"
    python tooling/arc.py scope  --subject SCI --status CONFIRMED_UNITS_ONLY --units ... --sources ... --evidence ...
    python tooling/arc.py log    --run-id ... --product ARC_N --subject SCI --range "..." --items 20
    python tooling/arc.py checksums [--check]    CHECKSUMS.sha256 재생성 / 검증
    python tooling/arc.py ci                     GitHub Actions 단계 로컬 실행

이 도구는 모델을 호출하지 않고, Drive를 읽지 않으며, 범위를 추정하지 않는다.
범위·근거는 사용자가 준 값만 기록한다. 판정 권한은 기존 게이트
(exam_scope_gate, production_pipeline, validate_system)에 그대로 있다.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SYSTEM_MANIFEST.yaml"
CHECKSUMS = ROOT / "CHECKSUMS.sha256"
RUN_LOG_JSONL = ROOT / "ops" / "RUN_LOG.jsonl"
RUN_LOG_CSV = ROOT / "ops" / "RUN_LOG.csv"
EPHEMERAL = {"CHECKSUMS.sha256", "ops/RUN_LOG.csv", "ops/RUN_LOG.jsonl"}
KST = dt.timezone(dt.timedelta(hours=9))

SUBJECTS = {"KOR": "korean", "ENG": "english", "SOC": "social", "SCI": "science", "HIS": "history", "AI": "ai"}
SUBJECT_KO = {"KOR": "국어", "ENG": "영어", "SOC": "사회", "SCI": "과학", "HIS": "한국사", "AI": "AI"}
PRODUCTS = ("ARC_CORE", "ARC_N", "ARC_FINAL")
PRODUCT_SHORT = {"ARC_CORE": "CORE", "ARC_N": "N", "ARC_FINAL": "FINAL"}
CANARY_RUNNER = {
    "ARC_CORE": "tooling/canary/nightly_canary.py",
    "ARC_N": "tooling/canary/kor_n_canary.py",
    "ARC_FINAL": "tooling/canary/kor_final_canary.py",
}
SCOPE_STATES = ("PROVISIONAL_REMAINDER", "CONFIRMED_UNITS_ONLY", "CONFIRMED")


# ---------- shared helpers ----------

def load_manifest() -> dict:
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def tracked_files() -> list[str]:
    out = git("ls-files", "--cached", "--others", "--exclude-standard")
    return sorted(p.strip().replace("\\", "/") for p in out.splitlines() if p.strip() and (ROOT / p.strip()).is_file())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exam_registry(manifest: dict) -> tuple[Path, dict, str]:
    runtime = manifest["runtime"]
    path = ROOT / runtime["exam_context_registry"]
    return path, yaml.safe_load(path.read_text(encoding="utf-8")), runtime["active_exam_id"]


def load_scope_gate():
    spec = importlib.util.spec_from_file_location("arc_exam_scope_gate", ROOT / "tooling/exams/exam_scope_gate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canary_fixture(subject: str, product: str) -> Path:
    return ROOT / "quality" / "canary" / f"{subject}_{PRODUCT_SHORT[product]}_CANARY_V1.yaml"


# ---------- doctor ----------

def cmd_doctor(_args) -> int:
    problems = []
    for module, package in (("yaml", "PyYAML"), ("fitz", "PyMuPDF"), ("cv2", "opencv-python-headless")):
        try:
            __import__(module)
            print(f"[OK]   python: {package}")
        except Exception:
            print(f"[MISS] python: {package}")
            problems.append(f"python -m pip install -r tooling/requirements-smoke.txt")
    font_dirs = [Path("/usr/share/fonts/truetype/nanum"), Path.home() / ".local/share/fonts/nanum"]
    font_names = ("NanumMyeongjo.ttf", "NanumMyeongjoBold.ttf", "NanumGothic.ttf", "NanumGothicBold.ttf")
    missing_fonts = [name for name in font_names if not any((d / name).is_file() for d in font_dirs)]
    if missing_fonts:
        print(f"[MISS] fonts: {', '.join(missing_fonts)}")
        problems.append("bash tooling/ci/install_fonts.sh   (없으면 PDF 조판·카나리 실패)")
    else:
        print("[OK]   fonts: Nanum Myeongjo/Gothic")
    try:
        print(f"[OK]   git: {git('rev-parse', '--abbrev-ref', 'HEAD')} @ {git('rev-parse', '--short', 'HEAD')}")
    except Exception:
        print("[MISS] git repository")
        problems.append("저장소 루트에서 실행")
    if problems:
        print("\n필요한 조치:")
        for line in dict.fromkeys(problems):
            print("  " + line)
        return 1
    print("\n환경 준비 완료. 다음: python tooling/arc.py status")
    return 0


# ---------- status ----------

def cell_status(subject: str, product: str, entry: dict, manifest: dict) -> tuple[str, list[str]]:
    """Return (label, blockers) for one subject/product cell using the registered gate rules."""
    blockers: list[str] = []
    if not canary_fixture(subject, product).is_file():
        blockers.append("E2E 카나리 없음")
    if product == "ARC_CORE":
        # exam_scope_gate only admits products listed for the subject; CORE is maintenance-mode.
        if "ARC_CORE" not in (entry.get("products") or []):
            blockers.append("시험 설정 products에 ARC_CORE 미등록 (등록: arc.py scope --products)")
    elif product not in (entry.get("products") or []):
        blockers.append(f"시험 설정에서 {product} 비활성")
    state = entry.get("scope_status")
    if state not in {"CONFIRMED", "CONFIRMED_UNITS_ONLY"}:
        blockers.append(f"범위 미확정({state})")
    elif product == "ARC_FINAL" and state != "CONFIRMED":
        blockers.append("FINAL은 전체 범위 CONFIRMED 필요")
    if state in {"CONFIRMED", "CONFIRMED_UNITS_ONLY"}:
        if not entry.get("scope_evidence_refs"):
            blockers.append("범위 근거(scope_evidence_refs) 없음")
        if not entry.get("unit_ids"):
            blockers.append("unit_ids 없음")
        if not entry.get("source_ids"):
            blockers.append("source_ids 없음")
    if product == "ARC_FINAL" and not isinstance(entry.get("difficulty_anchor"), dict):
        blockers.append("기말 난도 anchor 미등록")
    return ("READY" if not blockers else "BLOCKED"), blockers


def cmd_status(args) -> int:
    manifest = load_manifest()
    _, registry, exam_id = exam_registry(manifest)
    exam = registry["exams"][exam_id]
    active = exam.get("active_subjects", [])
    print(f"ARC {manifest['system']['version']}  |  branch {git('rev-parse', '--abbrev-ref', 'HEAD')}"
          f"  |  exam {exam_id} ({exam.get('status')}, date={exam.get('exam_date')})")
    print(f"활성 과목: {', '.join(active)}\n")
    rows = []
    for subject in active:
        entry = exam["subjects"][subject]
        for product in PRODUCTS:
            label, blockers = cell_status(subject, product, entry, manifest)
            rows.append((subject, product, label, blockers))
    width = max(len(PRODUCT_SHORT[p]) for p in PRODUCTS) + 2
    print("과목   " + "".join(PRODUCT_SHORT[p].ljust(width + 6) for p in PRODUCTS))
    for subject in active:
        line = f"{SUBJECT_KO[subject]:<4} "
        for product in PRODUCTS:
            label = next(r[2] for r in rows if r[0] == subject and r[1] == product)
            line += label.ljust(width + 6)
        print(line)
    blocked = [r for r in rows if r[3]]
    if blocked:
        print("\n막힌 이유:")
        for subject, product, _, blockers in blocked:
            print(f"  {SUBJECT_KO[subject]} {PRODUCT_SHORT[product]}: " + " / ".join(blockers))
        print("\n범위가 확정되면:  python tooling/arc.py scope --subject <과목> --status CONFIRMED "
              "--units ... --sources ... --evidence ...")
    if args.json:
        print(json.dumps([{"subject": s, "product": p, "status": l, "blockers": b} for s, p, l, b in rows],
                         ensure_ascii=False, indent=2))
    # Status is a report; a blocked matrix is not a tool failure.
    return 0


# ---------- start ----------

def files_to_load(manifest: dict, subject: str, product: str) -> list[tuple[str, str]]:
    runtime, active = manifest["runtime"], manifest["active"]
    quality, layout = active["quality"], active["layout"]
    out: list[tuple[str, str]] = [
        ("runbook", runtime["unified_runbook"]),
        ("공통 엔진", active["common_generation_engine"]["path"]),
        ("과목 MASTER", active["subjects"][SUBJECTS[subject]]["path"]),
        ("생성 계약", runtime["generator_contract"]),
        ("콘텐츠 번들 계약", runtime["content_bundle_contract"]),
        ("범위 장부", quality["scope_ledger"]),
        ("오류 DB", quality["error_database"]),
        ("문항 품질", quality["item_quality"]),
        ("가짜 난도 게이트", quality.get("false_difficulty_gate", "")),
        ("독립 재풀이", quality["universal_independent_solve"]),
        ("GOLD 앵커", quality["gold_anchor_packs"].get(SUBJECTS[subject], "")),
        ("시험 설정", runtime["exam_context_registry"]),
    ]
    if subject == "KOR":
        out += [("국어 문항 엔진", active["korean_item_engine"]["path"]),
                ("국어 문항 QA", quality["korean_item_qa"]),
                ("국어 V1~V6 정책", runtime["korean_learning_level_policy"]),
                ("국어 실전성 게이트", quality["korean_exam_realism_gate"]),
                ("중세국어 모듈(해당 범위 요청 시에만)", runtime.get("korean_middle_korean_policy", ""))]
    if subject == "ENG":
        out += [("영어 문항 유형 라이브러리", runtime["english_exam_type_library"]),
                ("범위 공지", runtime["exam_scope_notice"])]
    if subject == "SOC":
        out += [("사회 C X표시 제외 색인", quality["social_c_xmark_exclusion_index"]),
                ("사회 학교자료 목록", quality["social_school_source_inventory"]),
                ("사회 시각자료 명세", quality["social_visual_spec"])]
    if product == "ARC_CORE":
        out += [("CORE 내용 엔진", active["core_content_engine"]["path"]),
                ("CORE 편집 구조", active["core_editorial_architecture"]["path"]),
                ("CORE 심화 엔진", active["core_depth_engine"]["path"]),
                ("CORE QA 벤치", quality["core_qa_bench"]),
                ("CORE 조판 패치", layout["core_patch"])]
    else:
        out += [("난도 엔진", quality["difficulty_engine"]),
                ("세트 편집", quality["set_editorial"]),
                ("유사도 가드", quality["similarity_guard"]),
                ("출처 비율 정책", runtime["generation_source_policy"])]
    if product == "ARC_N":
        out += [("N 균형 게이트", quality["n_balance_gate"]),
                ("N 레이아웃", layout["arc_n_layout_override"])]
    if product == "ARC_FINAL":
        anchor_key = {"KOR": "final_difficulty_anchor_kor", "SOC": "final_difficulty_anchor_soc",
                      "SCI": "final_difficulty_anchor_sci_redox"}.get(subject)
        out += [("FINAL 품질 게이트", quality["final_quality_gate"])]
        if anchor_key:
            out += [("FINAL 난도 앵커", quality[anchor_key])]
    out += [("조판 계약", runtime["typesetter_contract"]), ("PDF 조판 MASTER", layout["pdf_master"])]
    return [(label, path) for label, path in out if path]


def cmd_start(args) -> int:
    manifest = load_manifest()
    subject, product = args.subject, args.product
    _, registry, exam_id = exam_registry(manifest)
    exam = registry["exams"][exam_id]
    entry = exam["subjects"][subject]
    today = dt.datetime.now(KST).strftime("%Y%m%d")
    runs = ROOT / "runs"
    serial = 1
    while (runs / f"{subject}-{PRODUCT_SHORT[product]}-{today}-{serial:02d}").exists():
        serial += 1
    batch_id = args.batch_id or f"{subject}-{PRODUCT_SHORT[product]}-{today}-{serial:02d}"
    run_dir = runs / batch_id
    commit = git("rev-parse", "HEAD")
    dirty = bool(git("status", "--porcelain", "--untracked-files=no"))
    request = {
        "batch_id": batch_id, "subject": subject, "scope": args.scope, "product": product,
        "count": args.count, "ruleset_commit": commit,
        "outputs": ["student.pdf"] if product == "ARC_CORE" else ["student.pdf", "answer_key.pdf"],
        "source_mix_mode": args.source_mix_mode,
        "exam_id": exam_id,
    }
    label, blockers = cell_status(subject, product, entry, manifest)
    gate = load_scope_gate()
    exam_context = {
        "exam_id": exam_id,
        "profile_sha256": gate.digest(exam),
        "unit_ids": args.units or [],
        "source_ids": args.sources or [],
    }
    if not args.dry_run:
        run_dir.mkdir(parents=True, exist_ok=False)
        (run_dir / "request.json").write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (run_dir / "exam_context.yaml").write_text(
            yaml.safe_dump({"exam_context": exam_context}, allow_unicode=True, sort_keys=False), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, "tooling/workflow/arc_workflow.py", "init", "--state", str(run_dir / "state.json"),
             "--input", str(run_dir / "request.json"), "--actor", args.actor, "--manifest", "SYSTEM_MANIFEST.yaml"],
            cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr.strip() or result.stdout.strip())
            return result.returncode
    print(f"BATCH    {batch_id}{'  (dry-run, 파일 미생성)' if args.dry_run else ''}")
    print(f"REQUEST  {SUBJECT_KO[subject]} {PRODUCT_SHORT[product]} {args.count}{'개념' if product == 'ARC_CORE' else '문항'} / {args.scope}")
    print(f"RULESET  {commit[:12]}{'  (경고: 커밋되지 않은 변경 있음)' if dirty else ''}")
    if not args.dry_run:
        print(f"STATE    {run_dir.relative_to(ROOT)}/state.json")
    print(f"EXAM     {exam_id}  scope={entry.get('scope_status')}  →  {label}")
    for blocker in blockers:
        print(f"         BLOCKER: {blocker}")
    if blockers:
        print("         초안(draft) 작성과 자료 수집은 가능. 검증본(verified) 출판은 위 항목 해결 후.")
    print("\n읽을 파일 (manifest 기준, 이 순서):")
    for index, (label_, path) in enumerate(files_to_load(manifest, subject, product), 1):
        print(f"  {index:>2}. {path}    # {label_}")
    print("\n다음 단계:")
    print("  1) Drive에서 해당 범위 학교자료·교과서를 실제로 열람 → source.json 기록")
    print(f"  2) python tooling/workflow/arc_workflow.py status --state runs/{batch_id}/state.json")
    print("  3) 생성 → 독립 재풀이 → 조판. 끝나면 python tooling/arc.py log ... 로 RUN_LOG 기록")
    return 0


# ---------- plan ----------

PLAN_DEFAULTS = ROOT / "ops" / "planning" / "ARC_PLAN_DEFAULTS_V1.yaml"
GRAMMAR_WORDS = ("맞춤법", "띄어쓰기", "문법", "사이시옷", "표기")


def apportion(total: int, shares: dict[str, float]) -> dict[str, int]:
    """Largest-remainder split so the counts always add up to total."""
    raw = {k: total * v for k, v in shares.items()}
    out = {k: int(v) for k, v in raw.items()}
    for k in sorted(raw, key=lambda k: raw[k] - out[k], reverse=True)[: total - sum(out.values())]:
        out[k] += 1
    return out


def previous_kor_version(scope: str) -> str | None:
    if not RUN_LOG_JSONL.is_file():
        return None
    found = None
    for line in RUN_LOG_JSONL.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("product") != "ARC_N" or rec.get("subject") != "KOR":
            continue
        text = f"{rec.get('run_id', '')} {rec.get('target_range', '')}"
        if not any(word and word in text for word in scope.split()):
            continue
        match = re.search(r"V([1-4])(?!\d)", text)
        if match:
            found = f"V{match.group(1)}"
    return found


def build_plan(subject: str, product: str, scope: str, count: int | None, version: str | None) -> dict:
    defaults = yaml.safe_load(PLAN_DEFAULTS.read_text(encoding="utf-8"))
    manifest = load_manifest()
    _, registry, exam_id = exam_registry(manifest)
    entry = registry["exams"][exam_id]["subjects"][subject]
    reasons = []
    grammar = subject == "KOR" and any(w in scope for w in GRAMMAR_WORDS)
    if count is None and product == "ARC_FINAL" and subject in defaults.get("final_count_default", {}):
        count = defaults["final_count_default"][subject]
        reasons.append(f"FINAL 문항 수 미지정 → 시험과 같은 {count}")
    if count is None:
        count = defaults["count_default"].get(subject, 20)
        reasons.append(f"문항 수 미지정 → 기본 {count}")
    profile, version_name = None, None
    if subject == "KOR" and product == "ARC_N":
        if version:
            reasons.append(f"버전 지정 {version}")
        elif grammar:
            version = "V6"
            reasons.append("맞춤법·띄어쓰기 요청 → V6")
        else:
            prev = previous_kor_version(scope)
            version = "V1" if prev is None else f"V{min(4, int(prev[1]) + 1)}"
            reasons.append("같은 범위 기록 없음 → V1" if prev is None else f"직전 {prev} → {version}")
        if version not in defaults["kor_versions"]:
            raise SystemExit(f"국어 ARC N° 버전은 {', '.join(defaults['kor_versions'])} 중 하나여야 합니다 (V5는 ARC FINAL).")
        profile = defaults["kor_versions"][version]
        version_name = profile["name"]
    elif subject == "KOR":
        version = "V5" if product == "ARC_FINAL" else None
        profile = {"difficulty": None, "advanced": None}
    else:
        version = None
        profile = defaults["other_subjects"][subject]
    plan = {"subject": subject, "product": product, "scope": scope, "version": version, "version_name": version_name,
            "count": count, "reasons": reasons, "exam_id": exam_id, "scope_status": entry.get("scope_status")}
    if product == "ARC_N" and profile.get("difficulty"):
        split = defaults["set_split"][subject]
        per_unit = split["unit_selected"] + split["unit_constructed"]
        units = max(1, round(count / per_unit))
        constructed = units * split["unit_constructed"]
        selected = count - constructed
        diff = apportion(selected, profile["difficulty"])
        lo, hi = defaults["hard_limits"]["advanced_share"]
        # Keep the count inside the gate band even after rounding.
        advanced = min(int(selected * hi + 1e-9), max(-(-selected * lo // 1).__int__(), round(selected * profile["advanced"])))
        if not lo - 1e-9 <= advanced / selected <= hi + 1e-9:
            raise SystemExit("계획의 심화 비율이 게이트 범위(20~30%)를 벗어납니다.")
        plan.update({"units": units, "selected": selected, "constructed": constructed,
                     "difficulty": {k: v for k, v in diff.items() if v}, "advanced": advanced, "core": selected - advanced})
        if grammar:
            library = yaml.safe_load((ROOT / defaults["archetype_library"]["KOR_GRAMMAR"]).read_text(encoding="utf-8"))
            mcq_types = [k for k, v in library["archetypes"].items() if v["format"] == "MCQ"]
            plan["archetype_library"] = defaults["archetype_library"]["KOR_GRAMMAR"]
            plan["archetype_mix"] = apportion(selected, {k: 1 / len(mcq_types) for k in mcq_types})
            plan["archetype_mix"]["C1_CONSTRUCTED_BLANK_SENTENCE"] = constructed
    if subject == "ENG":
        library = yaml.safe_load((ROOT / defaults["archetype_library"]["ENG"]).read_text(encoding="utf-8"))
        plan["archetype_library"] = defaults["archetype_library"]["ENG"]
        if product == "ARC_N" and plan.get("units"):
            parts = library["arc_n_set"]["parts"]
            plan["archetype_mix"] = {k: v * plan["units"] for k, v in parts.items()}
        elif product == "ARC_FINAL":
            totals = library["arc_final_totals"]
            plan["final_blueprint"] = (f"선택형 {totals['selected_items']}({totals['selected_points']:g}점, 1~10번 단어 각 1점) + "
                                       f"서답형 {totals['constructed_items']}({totals['constructed_points']:g}점), 23번 교과서 다중 어법·34번 요약문 고정")
    _, blockers = cell_status(subject, product, entry, manifest)
    plan["blockers"] = blockers
    plan["read_order"] = [path for _, path in files_to_load(manifest, subject, product)]
    return plan


def print_plan(plan: dict) -> None:
    subject, product = plan["subject"], plan["product"]
    title = f"{SUBJECT_KO[subject]} {PRODUCT_SHORT[product]}"
    if plan.get("version"):
        title += f" {plan['version']}" + (f" ({plan['version_name']})" if plan.get("version_name") else "")
    print("ARC 제작 계획")
    print(f"  제품      {title}")
    print(f"  범위      {plan['scope']}")
    if plan.get("units"):
        print(f"  분량      총 {plan['count']}문항 = 선택형 {plan['selected']} + 서답형 {plan['constructed']}, 단원 세트 {plan['units']}개")
        print("  난도      " + " / ".join(f"{k} {v}" for k, v in plan["difficulty"].items()) + "  (선택형 기준)")
        print(f"  구성      핵심 {plan['core']} / 심화 {plan['advanced']}")
    else:
        print(f"  분량      {plan['count']}문항")
    if plan.get("final_blueprint"):
        print(f"  배치      {plan['final_blueprint']}")
    if plan.get("archetype_mix"):
        print("  문항 원형 " + ", ".join(f"{k if plan['subject'] == 'ENG' else k.split('_')[0]} {v}" for k, v in plan["archetype_mix"].items()))
        print(f"            ({plan['archetype_library']})")
    for reason in plan["reasons"]:
        print(f"  기본값    {reason}")
    print(f"  시험      {plan['exam_id']}  범위 상태 {plan['scope_status']}")
    for blocker in plan["blockers"]:
        print(f"  막힘      {blocker}")
    print("  절차      계획 확인 → 자료 열람 → 단원 세트 1개 초안 → 자체 점검·조판 미리보기 → 독립 재풀이 → 다음 세트")


def cmd_plan(args) -> int:
    plan = build_plan(args.subject, args.product, args.scope, args.count, args.version)
    print_plan(plan)
    if args.save:
        path = Path(args.save)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(f"\n저장: {path}")
    return 0


# ---------- scope ----------

def cmd_scope(args) -> int:
    manifest = load_manifest()
    path, registry, exam_id = exam_registry(manifest)
    exam = registry["exams"][exam_id]
    entry = exam["subjects"][args.subject]
    if args.show:
        print(yaml.safe_dump({args.subject: entry, "exam_date": exam.get("exam_date")}, allow_unicode=True, sort_keys=False))
        return 0
    changed = []
    if args.status:
        if args.status in {"CONFIRMED", "CONFIRMED_UNITS_ONLY"}:
            units = args.units if args.units is not None else entry.get("unit_ids")
            sources = args.sources if args.sources is not None else entry.get("source_ids")
            evidence = args.evidence if args.evidence is not None else entry.get("scope_evidence_refs")
            missing = [name for name, value in (("--units", units), ("--sources", sources), ("--evidence", evidence)) if not value]
            if missing:
                print("범위를 확정 처리하려면 다음 값이 필요합니다: " + ", ".join(missing))
                print("근거(학교 공지·학습지 위치) 없이 확정 상태로 바꾸지 않습니다.")
                return 2
        entry["scope_status"] = args.status
        changed.append(f"scope_status={args.status}")
    for field, value in (("unit_ids", args.units), ("source_ids", args.sources),
                         ("scope_evidence_refs", args.evidence), ("excluded_unit_ids", args.exclude_units),
                         ("excluded_source_ids", args.exclude_sources), ("products", args.products)):
        if value is not None:
            if len(set(value)) != len(value):
                print(f"{field}: 중복 값이 있습니다.")
                return 2
            entry[field] = list(value)
            changed.append(f"{field}={value}")
    if args.final_anchor:
        anchor_path = ROOT / args.final_anchor
        if not anchor_path.is_file():
            print(f"anchor 파일이 없습니다: {args.final_anchor}")
            return 2
        payload = yaml.safe_load(anchor_path.read_text(encoding="utf-8"))
        gate = load_scope_gate()
        if not isinstance(payload, dict) or gate.subject_code(payload.get("subject")) != args.subject:
            print("anchor 파일의 subject가 이 과목과 일치하지 않습니다.")
            return 2
        anchor_units = args.anchor_units or entry.get("unit_ids") or []
        if not anchor_units:
            print("anchor가 적용될 단원(--anchor-units 또는 등록된 unit_ids)이 필요합니다.")
            return 2
        entry["difficulty_anchor"] = {"subject": args.subject, "unit_ids": list(anchor_units),
                                      "path": args.final_anchor, "sha256": sha256(anchor_path)}
        changed.append(f"difficulty_anchor={args.final_anchor}")
    if args.exam_date:
        dt.date.fromisoformat(args.exam_date)
        exam["exam_date"] = args.exam_date
        changed.append(f"exam_date={args.exam_date}")
    if not changed:
        print("변경할 값이 없습니다. --show 로 현재 값을 확인하세요.")
        return 2
    path.write_text(yaml.safe_dump(registry, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
    print(f"{path.relative_to(ROOT)} 갱신 ({exam_id} / {args.subject})")
    for line in changed:
        print("  " + line)
    print("\n시험 설정 해시가 바뀌었으므로 기존 원고는 EXAM_PROFILE_STALE로 보류됩니다(정상).")
    print("다음: python tooling/arc.py checksums && python tooling/arc.py status")
    return 0


# ---------- log ----------

CSV_FIELDS = ["run_id", "timestamp", "product", "subject", "target_range", "item_count", "manifest_version",
              "git_branch", "git_commit", "engine_version", "subject_master_version", "bank_pass", "discarded",
              "avg_item_quality", "avg_commercial_grade", "set_editorial_score", "hard_fail_count", "notes"]


def version_of(path: str) -> str:
    match = re.search(r"_V(\d+(?:\.\d+)*)", path)
    return match.group(1) if match else "UNKNOWN"


def cmd_log(args) -> int:
    manifest = load_manifest()
    existing = set()
    if RUN_LOG_JSONL.is_file():
        for line in RUN_LOG_JSONL.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing.add(json.loads(line).get("run_id"))
    if args.run_id in existing:
        print(f"run_id가 이미 있습니다: {args.run_id}")
        return 2
    difficulty = None
    if args.difficulty:
        difficulty = {}
        for part in args.difficulty.split(","):
            key, _, value = part.partition("=")
            difficulty[key.strip()] = int(value)
        if args.items is not None and sum(difficulty.values()) != args.items:
            print(f"난도 분포 합({sum(difficulty.values())})이 문항 수({args.items})와 다릅니다.")
            return 2
    subject_master = manifest["active"]["subjects"].get(SUBJECTS.get(args.subject, ""), {}).get("path", "")
    record = {
        "run_id": args.run_id,
        "timestamp": dt.datetime.now(KST).replace(microsecond=0).isoformat(),
        "product": args.product, "subject": args.subject, "target_range": args.range,
        "item_count": args.items, "manifest_version": manifest["system"]["version"],
        "git_branch": git("rev-parse", "--abbrev-ref", "HEAD"), "git_commit": git("rev-parse", "HEAD"),
        "engine_version": str(manifest["active"]["common_generation_engine"]["version"]),
        "subject_master_version": version_of(subject_master) if subject_master else "UNCHANGED",
        "bank_pass": args.bank_pass, "discarded": args.discarded,
        "avg_item_quality": args.avg_item_quality, "avg_commercial_grade": args.avg_commercial_grade,
        "set_editorial_score": args.set_editorial_score, "difficulty_distribution": difficulty,
        "hard_fail_count": args.hard_fail, "output_refs": args.output or [], "notes": args.notes or "",
    }
    with RUN_LOG_JSONL.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    with RUN_LOG_CSV.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=CSV_FIELDS, extrasaction="ignore").writerow(
            {k: ("" if v is None else v) for k, v in record.items()})
    count = f"{args.items}문항" if args.items is not None else "문항 수 없음"
    print(f"RUN_LOG 기록: {args.run_id} ({args.product}/{args.subject}, {count}, hard_fail={args.hard_fail})")
    return 0


# ---------- checksums ----------

def cmd_checksums(args) -> int:
    files = [p for p in tracked_files() if p not in EPHEMERAL]
    current = {}
    if CHECKSUMS.is_file():
        for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                digest, path = line.split(maxsplit=1)
                current[path.strip()] = digest
    fresh = {p: sha256(ROOT / p) for p in files}
    added = sorted(set(fresh) - set(current))
    removed = sorted(set(current) - set(fresh))
    changed = sorted(p for p in fresh if p in current and fresh[p] != current[p])
    for label, items in (("추가", added), ("삭제", removed), ("변경", changed)):
        for item in items:
            print(f"  {label}: {item}")
    if args.check:
        if added or removed or changed:
            print(f"CHECKSUMS 불일치: 추가 {len(added)} / 삭제 {len(removed)} / 변경 {len(changed)}")
            print("고치려면: python tooling/arc.py checksums")
            return 1
        print(f"CHECKSUMS 일치 ({len(fresh)} files)")
        return 0
    CHECKSUMS.write_text("".join(f"{fresh[p]}  {p}\n" for p in sorted(fresh)), encoding="utf-8")
    print(f"CHECKSUMS.sha256 갱신: {len(fresh)} files (추가 {len(added)} / 삭제 {len(removed)} / 변경 {len(changed)})")
    return 0


# ---------- scaffold ----------

def cmd_scaffold(args) -> int:
    """Create a canonical bundle skeleton (items.yaml) so Gemini, Claude, and ChatGPT produce identical structure."""
    now = dt.datetime.now(KST).strftime("%Y-%m-%d")
    batch_id = args.batch_id or f"ARC-{args.actor}-{now.replace('-', '')}-{args.subject}-01"
    out_dir = Path(args.out) if args.out else ROOT / "runs" / batch_id
    out_dir.mkdir(parents=True, exist_ok=True)
    course_map = {"KOR": "공통국어2", "SOC": "통합사회2", "SCI": "통합과학2", "HIS": "한국사2", "AI": "인공지능기초"}
    set_label = "ARC FINAL" if args.product == "ARC_FINAL" else f"ARC N° {args.version or 'V1'}"
    skel = {
        "batch_id": batch_id,
        "generator": args.actor,
        "product_mode": args.product,
        "subject": args.subject,
        "course": course_map.get(args.subject, args.subject),
        "set_label": set_label,
        "cover_subtitle": f"{args.scope} 집중 훈련",
        "school_line": "동북고등학교",
        "scope": args.scope,
        "created_at": now,
        "scope_refs": [f"SCOPE:{args.subject}_CONFIRMED_UNIT"],
        "archetype_library": "quality/korean/ARC_KOR_GRAMMAR_ARCHETYPES_V1.0.yaml" if args.subject == "KOR" else None,
        "items": [
            {
                "item_id": f"{args.subject}-01",
                "format": "MCQ",
                "archetype": "KOR-G-RULE-MATCH" if args.subject == "KOR" else None,
                "family": "VIEW_APPLICATION",
                "balance": "CORE_EXAM_POINT",
                "difficulty": "D3",
                "reasoning_steps": 2,
                "immediate_elimination": 1,
                "stem": "<보기>를 바탕으로 탐구한 내용으로 가장 적절한 것은?",
                "view": ["ㄱ. 첫 번째 탐구 조건이나 예문을 여기에 작성한다.", "ㄴ. 두 번째 탐구 조건이나 예문을 여기에 작성한다."],
                "options": ["선지 1", "선지 2", "선지 3", "선지 4", "선지 5"],
                "answer": 1,
                "second_best": 2,
                "judgments": [
                    {"v": "TRUE", "c": "KEY", "axis": "핵심 판단축", "claim": "선지 1 핵심 명제", "ev": ["VIEW"], "why": "정답인 구체적 이유"},
                    {"v": "FALSE", "c": "STRONG", "trap": "POS_CONFUSION", "axis": "핵심 판단축", "claim": "선지 2 핵심 명제", "ev": ["VIEW"], "why": "매력적 오답(2순위)인 구체적 이유"},
                    {"v": "FALSE", "c": "PLAUSIBLE", "trap": "CLAUSE_MISMATCH", "axis": "보조 판단축", "claim": "선지 3 핵심 명제", "ev": ["VIEW"], "why": "오답인 구체적 이유"},
                    {"v": "FALSE", "c": "PLAUSIBLE", "trap": "EXCEPTION_IGNORED", "axis": "보조 판단축", "claim": "선지 4 핵심 명제", "ev": ["VIEW"], "why": "오답인 구체적 이유"},
                    {"v": "FALSE", "c": "WEAK", "trap": "SURFACE_FORM_BIAS", "axis": "기초 판단축", "claim": "선지 5 핵심 명제", "ev": ["VIEW"], "why": "오답인 구체적 이유"},
                ],
            }
        ],
    }
    if skel["archetype_library"] is None:
        skel.pop("archetype_library")
        skel["items"][0].pop("archetype")
    target = out_dir / "items.yaml"
    target.write_text(yaml.safe_dump(skel, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"표준 번들 스켈레톤 생성 완료: {target}")
    print(f"다음 단계: {target} 작성 후 python tooling/production/draft_preview.py {out_dir} --output-dir {out_dir}/out")
    return 0


# ---------- ci ----------

def cmd_ci(args) -> int:
    command = [sys.executable, "tooling/run_ci_local.py"]
    if args.fail_fast:
        command.append("--fail-fast")
    if args.only:
        command += ["--only", args.only]
    return subprocess.run(command, cwd=ROOT).returncode


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="실행 환경 점검").set_defaults(func=cmd_doctor)

    p = sub.add_parser("status", help="과목×제품 준비 상태")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("plan", help="요청을 제작 계획(버전·문항 수·난도·문항 원형)으로 바꿔 보여 준다")
    p.add_argument("--subject", required=True, choices=sorted(SUBJECTS))
    p.add_argument("--product", default="ARC_N", choices=PRODUCTS)
    p.add_argument("--scope", required=True)
    p.add_argument("--count", type=int)
    p.add_argument("--version", help="국어 ARC N°: V1~V4, V6")
    p.add_argument("--save", help="계획을 YAML로 저장할 경로")
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("scaffold", help="Gemini·Claude·ChatGPT 공통 items.yaml 표준 스켈레톤 생성")
    p.add_argument("--subject", required=True, choices=sorted(SUBJECTS))
    p.add_argument("--product", default="ARC_N", choices=PRODUCTS)
    p.add_argument("--scope", required=True)
    p.add_argument("--version", help="국어 ARC N° 버전 (예: V6)")
    p.add_argument("--actor", default="CLAUDE", help="생성 모델 식별자 (GEMINI / CLAUDE / GPT)")
    p.add_argument("--batch-id")
    p.add_argument("--out", help="번들 생성 폴더 경로")
    p.set_defaults(func=cmd_scaffold)

    p = sub.add_parser("start", help="요청 1건을 request.json + state.json으로 시작")
    p.add_argument("--subject", required=True, choices=sorted(SUBJECTS))
    p.add_argument("--product", required=True, choices=PRODUCTS)
    p.add_argument("--count", required=True, type=int, help="문항 수 (CORE는 개념 수)")
    p.add_argument("--scope", required=True, help="요청 범위 (사용자 표현 그대로)")
    p.add_argument("--units", nargs="*", help="exam_context unit_ids")
    p.add_argument("--sources", nargs="*", help="exam_context source_ids")
    p.add_argument("--actor", default="CLAUDE")
    p.add_argument("--batch-id")
    p.add_argument("--source-mix-mode", default="original_trial")
    p.add_argument("--dry-run", action="store_true", help="파일을 만들지 않고 안내만 출력")
    p.set_defaults(func=cmd_start)

    p = sub.add_parser("scope", help="현재 시험의 과목별 범위 등록 (사용자 제공 근거만 기록)")
    p.add_argument("--subject", required=True, choices=sorted(SUBJECTS))
    p.add_argument("--show", action="store_true")
    p.add_argument("--status", choices=SCOPE_STATES)
    p.add_argument("--units", nargs="*")
    p.add_argument("--sources", nargs="*")
    p.add_argument("--evidence", nargs="*", help="학교 공지·학습지 위치 등 범위 근거")
    p.add_argument("--exclude-units", nargs="*")
    p.add_argument("--exclude-sources", nargs="*")
    p.add_argument("--products", nargs="*", choices=PRODUCTS)
    p.add_argument("--final-anchor", help="FINAL 난도 anchor YAML 경로 (sha256 자동 고정)")
    p.add_argument("--anchor-units", nargs="*")
    p.add_argument("--exam-date", help="YYYY-MM-DD")
    p.set_defaults(func=cmd_scope)

    p = sub.add_parser("log", help="RUN_LOG.jsonl + RUN_LOG.csv에 실행 1건 기록")
    p.add_argument("--run-id", required=True)
    p.add_argument("--product", required=True, choices=PRODUCTS + ("QA",))
    p.add_argument("--subject", required=True)
    p.add_argument("--range", required=True)
    p.add_argument("--items", type=int)
    p.add_argument("--bank-pass", type=int)
    p.add_argument("--discarded", type=int)
    p.add_argument("--avg-item-quality", type=float)
    p.add_argument("--avg-commercial-grade", type=float)
    p.add_argument("--set-editorial-score", type=float)
    p.add_argument("--difficulty", help="예: D1=1,D2=7,D3=7,D4=4,D5=1")
    p.add_argument("--hard-fail", type=int, default=0)
    p.add_argument("--output", nargs="*", help="산출물 참조 (Drive 파일 ID/경로)")
    p.add_argument("--notes")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("checksums", help="CHECKSUMS.sha256 재생성 또는 검증")
    p.add_argument("--check", action="store_true")
    p.set_defaults(func=cmd_checksums)

    p = sub.add_parser("ci", help="CI 단계 로컬 실행")
    p.add_argument("--fail-fast", action="store_true")
    p.add_argument("--only")
    p.set_defaults(func=cmd_ci)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
