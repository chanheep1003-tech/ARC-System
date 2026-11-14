"""ARC N° 국어 V3·V6 혼합 번들 공용 도우미 (맞춤법·중세국어 번들이 함께 쓴다).

- old(): '{SS.A}'처럼 적은 옛한글 음절을 첫가끝(L V T) 조합형 자모로 바꾼다.
- mcq(): 선지별 판정을 'K:/S:/M:/W:' 접두어로 받아 번들 판정 필드를 만든다.
- balance_keys(): 진술형·분류형 선지의 정답 위치를 재배치해 정답 번호 분포를 맞춘다.
"""
import re
from collections import Counter

L = {"g": 0x1100, "gg": 0x1101, "n": 0x1102, "d": 0x1103, "r": 0x1105, "m": 0x1106, "b": 0x1107, "s": 0x1109,
     "SS": 0x110A, "'": 0x110B, "j": 0x110C, "JJ": 0x110D, "c": 0x110E, "k": 0x110F, "t": 0x1110, "p": 0x1111,
     "h": 0x1112, "BD": 0x1120, "BS": 0x1121, "BSG": 0x1122, "BSD": 0x1123, "SG": 0x112D, "SD": 0x112F, "SB": 0x1132,
     "BW": 0x112B, "Z": 0x1140, "OO": 0x1147, "NG": 0x114C, "Q": 0x1159}
V = {"a": 0x1161, "ae": 0x1162, "ya": 0x1163, "eo": 0x1165, "e": 0x1166, "yeo": 0x1167, "ye": 0x1168, "o": 0x1169,
     "wa": 0x116A, "oe": 0x116C, "yo": 0x116D, "u": 0x116E, "wo": 0x116F, "wi": 0x1171, "yu": 0x1172, "eu": 0x1173,
     "ui": 0x1174, "i": 0x1175, "A": 0x119E, "AI": 0x11A1}
T = {"g": 0x11A8, "n": 0x11AB, "d": 0x11AE, "l": 0x11AF, "lg": 0x11B0, "m": 0x11B7, "b": 0x11B8, "s": 0x11BA,
     "ng": 0x11BC, "j": 0x11BD, "h": 0x11C2, "NG": 0x11F0, "LQ": 0x11D9, "Z": 0x11EB, "lh": 0x11B6, "lb": 0x11B2}


def _syl(code: str) -> str:
    parts = code.split(".")
    if len(parts) not in (2, 3):
        raise ValueError(f"bad old-hangul syllable code: {code}")
    out = chr(L[parts[0]]) + chr(V[parts[1]])
    if len(parts) == 3:
        out += chr(T[parts[2]])
    return out


def old(text: str) -> str:
    return re.sub(r"\{([^{}]+)\}", lambda m: _syl(m.group(1)), text)


def deep_old(obj):
    if isinstance(obj, str):
        return old(obj)
    if isinstance(obj, list):
        return [deep_old(x) for x in obj]
    if isinstance(obj, dict):
        return {k: deep_old(v) for k, v in obj.items()}
    return obj


DEFAULT_TRAP = {"A1_GENERAL_RULE_MAPPING": "T1_RIGHT_CONCEPT_WRONG_CASE", "A2_STUDENT_TEXT_ERRORS": "T6_PARTIAL_SET",
                "A3_CONDITION_CLASSIFICATION": "T4_SAME_FORM_OTHER_FUNCTION",
                "A4_INQUIRY_DIALOGUE_CHECK": "T2_EXCEPTION_CONDITION", "A5_EXAMPLE_MULTI_JUDGMENT": "T6_PARTIAL_SET",
                "A6_RULE_CASE_EXPLANATION": "T1_RIGHT_CONCEPT_WRONG_CASE"}
C = {"S": "STRONG", "M": "MEDIUM", "W": "WEAK"}


class Bank:
    def __init__(self, prefix: str, axis: str):
        self.prefix, self.axis, self.items = prefix, axis, []

    def mcq(self, arch, d, fam, level, stem, view, opts, judg, neg=False, fixed=False, source=None):
        """judg: 5 strings 'K:근거'(정답) / 'S:'·'M:'·'W:'(오답 경쟁도) + 근거. 'S:...|T3' 처럼 함정 코드를 덧붙일 수 있다."""
        assert len(opts) == 5 and len(judg) == 5
        keys = [i for i, j in enumerate(judg, 1) if j.startswith("K:")]
        assert len(keys) == 1, (stem, keys)
        ans = keys[0]
        js, sb = [], None
        n = len(self.items) + 1
        for i, raw in enumerate(judg, 1):
            tag, body = raw.split(":", 1)
            trap = None
            if "|T" in body:
                body, trap = body.rsplit("|", 1)
                trap = {"T1": "T1_RIGHT_CONCEPT_WRONG_CASE", "T2": "T2_EXCEPTION_CONDITION", "T3": "T3_ONE_OF_TWO_WRONG",
                        "T4": "T4_SAME_FORM_OTHER_FUNCTION", "T5": "T5_RULE_JURISDICTION", "T6": "T6_PARTIAL_SET"}[trap]
            j = {"axis": self.axis, "c": "CORRECT" if i == ans else C[tag], "claim": f"{self.prefix.lower()}{n:02d}_o{i}",
                 "ev": ["VIEW", f"OPTION{i}"], "v": (i != ans) if neg else (i == ans), "why": body.strip()}
            if i != ans:
                j["trap"] = trap or DEFAULT_TRAP[arch]
                if sb is None and tag == "S":
                    sb = i
            js.append(j)
        if sb is None:
            sb = next(i for i in range(1, 6) if i != ans and judg[i - 1].startswith("M:"))
        it = {"item_id": f"KOR-{self.prefix}-{n:03d}", "archetype": arch, "level": level, "stem": stem, "view": view,
              "options": opts, "answer": ans, "second_best": sb, "difficulty": d, "family": "EXCEPT_INCORRECT" if neg else fam,
              "balance": "ADVANCED_DISCRIMINATION" if d in ("D4", "D5") else "CORE_EXAM_POINT",
              "reasoning_steps": 3 if d == "D4" else 2, "immediate_elimination": 0 if d == "D4" else 1,
              "transfer": level == "V3", "stem_polarity": "NEGATIVE" if neg else "POSITIVE", "judgments": js,
              "_fixed": fixed}
        if source:
            it["source_note"] = source
        self.items.append(it)

    def cr(self, d, level, stem, view, conditions, model, rubric, source=None):
        n = len(self.items) + 1
        it = {"item_id": f"KOR-{self.prefix}-{n:03d}", "archetype": "C1_CONSTRUCTED_BLANK_SENTENCE", "format": "CR",
              "level": level, "points": 5, "stem": stem, "view": view, "conditions": conditions,
              "model_answer": model, "rubric": rubric, "ev": ["VIEW"], "difficulty": d}
        if source:
            it["source_note"] = source
        self.items.append(it)


def _move(it, target):
    """Move the key of a non-fixed item to position `target`, keeping judgments aligned."""
    cur = it["answer"]
    if cur == target:
        return
    order = list(range(1, 6))
    order[cur - 1], order[target - 1] = order[target - 1], order[cur - 1]
    it["options"] = [it["options"][i - 1] for i in order]
    it["judgments"] = [it["judgments"][i - 1] for i in order]
    for k, j in enumerate(it["judgments"], 1):
        j["ev"] = ["VIEW", f"OPTION{k}"] if j["ev"][-1].startswith("OPTION") else j["ev"]
    pos = {old: new for new, old in enumerate(order, 1)}
    it["answer"], it["second_best"] = pos[it["answer"]], pos[it["second_best"]]


def balance_keys(items):
    mcqs = [it for it in items if it.get("format") != "CR"]
    cnt = Counter(it["answer"] for it in mcqs if it["_fixed"])
    seq = []
    for it in mcqs:
        if not it["_fixed"]:
            prev2 = seq[-2:]
            choices = sorted(range(1, 6), key=lambda p: (cnt[p], p))
            for p in choices:
                if not (len(prev2) == 2 and prev2[0] == prev2[1] == p):
                    _move(it, p)
                    break
            cnt[it["answer"]] += 1
        seq.append(it["answer"])
    for it in items:
        it.pop("_fixed", None)
    return Counter(seq)


def report(items):
    mcqs = [it for it in items if it.get("format") != "CR"]
    n = len(mcqs)
    endings = [re.sub(r"\s", "", it["stem"])[-8:] for it in mcqs]
    run = best = 1
    for a, b in zip(endings, endings[1:]):
        run = run + 1 if a == b else 1
        best = max(best, run)
    seq = [it["answer"] for it in mcqs]
    krun = k = 1
    for a, b in zip(seq, seq[1:]):
        k = k + 1 if a == b else 1
        krun = max(krun, k)
    sb = sum(re.sub(r"\s", "", it["stem"]).endswith("가장적절한것은?") for it in mcqs)
    ex = sum("적절하지않은" in re.sub(r"\s", "", it["stem"]) for it in mcqs)
    print("MCQ", n, "CR", len(items) - n, "keys", dict(sorted(Counter(seq).items())), "key_run", krun,
          "single_best", sb, "/", round(n * .4), "except", ex, "/", round(n * .2), "stem_run", best,
          "diff", dict(Counter(it["difficulty"] for it in items)), "level", dict(Counter(it["level"] for it in items)))
