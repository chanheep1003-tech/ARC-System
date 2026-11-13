"""영어 ARC N° — N기출 고난도 독해 Level 1 (3-4-1~3-6-4) 지문당 5문항 변형. 저장소 루트에서 실행.

지문마다 5개 슬롯(대의·어법·어휘·구조/추론·서답형)을 두고, 유형은 quality/english/ARC_ENG_EXAM_TYPES_V1.0.yaml
코드에서만 고른다. 본문은 passages.yaml(Drive 마스터 DB 정제본)에서 읽고, 밑줄·빈칸·삽입 변형은 find/replace로만
만든다(찾는 문자열이 정확히 한 번 나와야 한다). ⟦…⟧ = 밑줄.
"""
from pathlib import Path
import re
import yaml

HERE = Path(__file__).resolve().parent
PASS = {p["code"]: p for p in yaml.safe_load((HERE / "passages.yaml").read_text(encoding="utf-8"))["passages"]}
S, M, W = "STRONG", "MEDIUM", "WEAK"
U = lambda s: f"⟦{s}⟧"
CIRC = "①②③④⑤"
FAMILY = {"RDG-01": "MAIN_IDEA", "RDG-02": "IMPLIED_MEANING", "RDG-03": "VOCAB_IN_CONTEXT", "RDG-04": "BLANK_INFERENCE",
          "RDG-05": "IRRELEVANT_SENTENCE", "RDG-06": "SEQUENCE_ORDER", "RDG-07": "SENTENCE_INSERTION",
          "RDG-08": "CONTENT_UNDERSTANDING", "RDG-09": "SUMMARY_COMPLETION", "GRM-01": "GRAMMAR_ERROR",
          "GRM-02": "GRAMMAR_CORRECT_SET", "VOC-03": "VOCAB_DEFINITION", "VOC-04": "VOCAB_SYNONYM",
          "CRQ-01": "SUMMARY_COMPLETION", "CRQ-02": "VOCAB_DEFINITION", "CRQ-03": "STRUCTURE_RELATION"}
CRQ01_COND = ["본문에 있는 단어만을 사용하되 필요한 경우 어형을 변화시킬 것", "요약문에 이미 언급된 단어는 사용하지 말 것",
              "각 빈칸에 한 단어씩만 넣을 것"]
items: list[dict] = []
counter: dict[str, int] = {}


def text(code: str) -> str:
    return PASS[code]["text"]


def sents(code: str) -> list[str]:
    return re.split(r"(?<=[.?!\"])\s+(?=[A-Z])", text(code))


def edit(src: str, *pairs: tuple[str, str]) -> str:
    for find, repl in pairs:
        if src.count(find) != 1:
            raise SystemExit(f"EDIT_NOT_UNIQUE: {find!r} x{src.count(find)}")
        src = src.replace(find, repl, 1)
    return src


def ulist(src: str, *finds: str) -> str:
    """Underline finds in order as ①⟦…⟧ … ⑤⟦…⟧. A (context, word) pair underlines word inside a unique context."""
    pairs = []
    for i, f in enumerate(finds):
        ctx, w = f if isinstance(f, tuple) else (f, f)
        pairs.append((ctx, ctx.replace(w, f"{CIRC[i]}{U(w)}", 1)))
    return edit(src, *pairs)


def _id(code: str) -> str:
    counter[code] = counter.get(code, 0) + 1
    return f"ENG-NG-{code}-{counter[code]}"


def mcq(code, t, d, stem, passage, opts, ans, sb, judg, steps=2, elim=1, view=None, view_label=None):
    neg = bool(re.search(r"틀린 것|않은 것|않는 것|관계 없는", stem))  # negative stem: key is the one FALSE option
    js = []
    for i, (claim, c, why) in enumerate(judg, 1):
        js.append({"axis": "reading", "c": "CORRECT" if i == ans else c, "claim": claim,
                   "ev": ["PASSAGE", f"OPTION{i}", f"SCOPE:NGICHUL-L1-{code}"], "v": (i != ans) if neg else (i == ans),
                   "why": why})
    it = {"item_id": _id(code), "set": None, "eng_type": f"ARC-ENG-{t}", "source_code": code,
          "scope_refs": [f"NGICHUL-L1-{code}"], "stem": stem, "passage": passage if isinstance(passage, list) else [passage],
          "options": opts, "answer": ans, "second_best": sb, "difficulty": d, "family": FAMILY[t],
          "balance": "ADVANCED_DISCRIMINATION" if d in ("D4", "D5") else "CORE_EXAM_POINT",
          "reasoning_steps": steps, "immediate_elimination": elim, "transfer": True,
          "stem_polarity": "NEGATIVE" if neg else "POSITIVE", "judgments": js}
    if view:
        it["view"] = view
        it["view_label"] = view_label if view_label is not None else ""
    items.append(it)
    return it


def crq(code, t, d, stem, passage, conditions, model, rubric, points, accepted=None, view=None, view_label=None):
    it = {"item_id": _id(code), "set": None, "format": "CR", "eng_type": f"ARC-ENG-{t}", "source_code": code,
          "scope_refs": [f"NGICHUL-L1-{code}"], "stem": stem, "passage": passage if isinstance(passage, list) else [passage],
          "conditions": conditions, "model_answer": model, "rubric": rubric, "points": points, "difficulty": d,
          "family": FAMILY[t]}
    if accepted:
        it["accepted_variants"] = accepted
    if view:
        it["view"] = view
        it["view_label"] = view_label if view_label is not None else ""
    items.append(it)
    return it


# ───────────────────────── 지문 01 · 3-4-1 고객 만족과 수익성의 균형 ─────────────────────────
c = "3-4-1"
mcq(c, "RDG-02", "D3", "밑줄 친 not 'give away the house'가 다음 글에서 의미하는 바로 가장 적절한 것은?",
    edit(text(c), ("not 'give away the house'", U("not 'give away the house'"))),
    ["not sacrifice the firm's profits just to make customers happier",
     "not let competitors copy the firm's customer-centered culture",
     "not stop investing in luxurious facilities for loyal guests",
     "not let customer satisfaction fall below that of competitors",
     "not reveal the company's credo to the general public"],
    1, 4,
    [("profit_kept", S, "가격 인하·서비스 확대로 만족도를 올리면 이익이 줄 수 있으므로, 이익을 내주지 않는다는 뜻이다."),
     ("copy_culture", W, "경쟁사의 모방은 글에서 다루지 않는다."),
     ("luxury_invest", M, "Pazano의 고급 호텔은 예시일 뿐, 시설 투자 중단과는 무관하다."),
     ("relative_level", S, "'경쟁사 대비 높은 만족'은 추구하는 바이고, 밑줄은 그 만족을 '이익을 버리면서까지' 올리지 않는다는 것이다."),
     ("credo_secret", W, "credo는 고객 만족 열정을 요약한 것이지 비밀이 아니다.")])

mcq(c, "GRM-01", "D3", "다음 글의 밑줄 친 부분 중, 어법상 틀린 것은?",
    edit(ulist(text(c), "interested", "become", "promises", "lowering", "profitably"),
         (U("promises"), U("promise"))),
    ["①", "②", "③", "④", "⑤"], 3, 2,
    [("pp_postmodifier", M, "companies를 뒤에서 꾸미는 과거분사(관심을 가진)이므로 맞다."),
     ("plural_subject", S, "주어가 value and service로 복수이므로 become이 맞다."),
     ("rel_agreement", S, "선행사 its credo가 단수이므로 promises로 고쳐야 한다."),
     ("by_gerund", W, "전치사 by의 목적어 자리이므로 동명사 lowering이 맞다."),
     ("adverb_mod", M, "동사 generate를 꾸미는 부사이므로 profitably가 맞다.")])

mcq(c, "RDG-03", "D3", "다음 글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?",
    edit(ulist(text(c), "exceptional", "passion", "maximize", ("in lower profits", "lower"), "delicate"),
         (U("delicate"), U("effortless"))),
    ["①", "②", "③", "④", "⑤"], 5, 3,
    [("exceptional_ok", W, "고객을 기쁘게 하려는 기업에서 '탁월한' 가치·서비스는 문맥에 맞다."),
     ("passion_ok", W, "고객 만족에 대한 '열정'이 credo에 요약된다는 흐름에 맞다."),
     ("maximize_ok", S, "앞의 does not attempt와 함께 '극대화하려 하지는 않는다'는 핵심 대조를 이룬다."),
     ("lower_ok", M, "가격 인하·서비스 확대가 '더 낮은' 이익을 낳을 수 있다는 흐름이다."),
     ("delicate_swap", S, "가치 창출과 이익 유지 사이의 '미묘한(delicate)' 균형이어야 하므로 effortless는 반대이다.")])

mcq(c, "RDG-04", "D4", "다음 빈칸에 들어갈 말로 가장 적절한 것은?",
    edit(text(c), ("Thus, the purpose of marketing is to generate customer value profitably.",
                   "Thus, what marketing ultimately aims at is to ________________________.")),
    ["maximize customer satisfaction regardless of the cost involved",
     "create value for customers while keeping the business profitable",
     "rank at the top of the industry in customer satisfaction",
     "lower prices so as to win customers away from competitors",
     "build a company culture centered on its employees' passion"],
    2, 1,
    [("maximize_trap", S, "글은 고객 만족을 극대화하려 하지 않는다고 했으므로 반대이다."),
     ("value_profit", S, "원문 'generate customer value profitably'를 바꿔 쓴 것으로 바로 뒤 delicate balance와 이어진다."),
     ("rank_top", M, "Pazano의 순위는 예시일 뿐 마케팅의 목적이 아니다."),
     ("lower_price", S, "가격 인하는 이익 감소로 이어질 수 있는 수단으로 제시되었다."),
     ("employee_passion", W, "열정은 고객 만족에 대한 것이고 직원 중심 문화는 다루지 않는다.")], steps=3)

crq(c, "CRQ-01", "D4", "다음 글의 내용을 한 문장으로 요약하고자 한다. <조건>에 맞게 빈칸 (A), (B)에 들어갈 말을 쓰시오.",
    [text(c), "",
     "→ A customer-centered firm seeks high customer satisfaction but avoids its (A)________, because the goal of "
     "marketing is the (B)________ creation of customer value."],
    CRQ01_COND, "(A) maximization  (B) profitable",
    ["(A) maximize → maximization: 소유격 its 뒤 명사 자리 (2점)", "(B) profitably → profitable: 명사 creation을 꾸미는 형용사 자리 (2점)",
     "단어는 맞고 어형이 틀리면 해당 빈칸 1점"], 4)

# ───────────────────────── 지문 02 · 3-4-2 외상 후 성장 ─────────────────────────
c = "3-4-2"
mcq(c, "RDG-01", "D2", "다음 글의 요지로 가장 적절한 것은?", text(c),
    ["Experts should pay more attention to post-traumatic stress syndrome.",
     "A single bad event usually has less impact on us than a good one.",
     "외상을 겪은 사람 대부분은 전문적인 심리 치료를 받아야 한다.",
     "외상 경험 뒤에는 부정적 영향보다 성장이 더 흔하게 나타난다.",
     "People who avoid terrifying events tend to become more mature."],
    4, 1,
    [("more_attention_pts", S, "Seligman은 PTSS에 관심이 쏠리는 것을 한탄했으므로 반대 진술이다."),
     ("bad_weaker", M, "글은 나쁜 사건 하나가 좋은 사건보다 더 강력하다고 했다."),
     ("therapy_needed", M, "80% 이상이 PTSS를 겪지 않는다고 했으므로 맞지 않는다."),
     ("growth_common", S, "외상 후 성장이 훨씬 널리 퍼져 있고 결국 더 강해진다는 것이 요지이다."),
     ("avoid_events", W, "끔찍한 사건을 피하는 사람에 대한 내용은 없다.")], steps=1)

mcq(c, "GRM-02", "D4", "다음 글의 밑줄 친 부분 중, 어법상 올바른 것끼리 짝지은 것은?",
    edit(text(c),
         ("which is actually far more widespread", "(a)" + U("which is actually far more widespread")),
         ("the experience has made them stronger", "(b)" + U("the experience has made them stronger")),
         ("so much attention is lavished on post-traumatic stress syndrome",
          "(c)" + U("so much attention is lavishing on post-traumatic stress syndrome")),
         ("After being exposed to a terrifying event", "(d)" + U("After exposing to a terrifying event")),
         ("they typically emerge more capable than ever", "(e)" + U("they typically emerge more capably than ever")),
         ("Bad can make us stronger in the end.", "(f)" + U("Bad can make us stronger in the end."))),
    ["(a), (c), (f)", "(a), (b), (f)", "(b), (d), (e)", "(a), (b), (e)", "(c), (d), (f)"],
    2, 4,
    [("set_acf", S, "(c)는 attention이 '쏟아지는' 것이므로 수동 is lavished여야 한다."),
     ("set_abf", S, "(a) 선행사 the concept → is, (b) make+O+비교급 형용사, (f) make+O+형용사 보어로 모두 맞다."),
     ("set_bde", W, "(d)는 '노출되는' 것이므로 being exposed to, (e)는 emerge의 보어 형용사 capable이어야 한다."),
     ("set_abe", S, "(e) emerge 뒤는 주격 보어 형용사 자리이므로 capably는 틀리다."),
     ("set_cdf", W, "(c), (d) 모두 능동·수동 오류이다.")], steps=3)
items[-1]["grm02_correct"] = ["a", "b", "f"]

mcq(c, "VOC-03", "D3", "다음 밑줄 친 단어의 의미에 대한 설명으로 가장 적절한 것은?",
    edit(sents(c)[2], ("is lavished on", "is " + U("lavished") + " on")),
    ["taken away slowly over a long period of time", "divided equally among several different people",
     "given generously or in very large amounts", "hidden carefully so that others cannot find it",
     "wasted on something that has no real value"],
    3, 5,
    [("taken_away", W, "반의 방향의 뜻풀이이다."), ("divided", M, "'나누다'는 lavish의 뜻이 아니다."),
     ("given_generously", S, "be lavished on: ~에 아낌없이(넘치도록) 쏟아지다."),
     ("hidden", W, "문맥(관심이 PTSS에 쏠림)과 반대이다."),
     ("wasted", S, "lavish의 '헤픈' 어감에 끌린 오답으로, 이 문장은 '많이 쏟아진다'는 뜻이다.")], steps=1)

mcq(c, "RDG-07", "D4", "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?",
    [s for s in [" ".join([sents(c)[0], "( ① )", sents(c)[1], "( ② )", sents(c)[2], "( ③ )", sents(c)[4], "( ④ )",
                          sents(c)[5], "( ⑤ )"])]],
    ["①", "②", "③", "④", "⑤"], 3, 2,
    [("after_s1", S, "①의 앞 문장은 PTG로 끝나 it이 PTG를 가리키게 되어 'PTG를 겪지 않는다'는 모순이 된다."),
     ("after_s2", S, "②는 성장 사례 뒤라 it이 가리킬 PTSS가 없고 Seligman 문장으로 이어지는 흐름도 끊긴다."),
     ("after_s3", S, "PTSS에 과도한 관심이 쏠려 나쁜 사건의 부정적 효과를 기대한다는 오해 뒤에, In fact로 반박 수치를 제시한다."),
     ("after_s5", M, "④ 앞은 life's challenges로 끝나 it이 가리킬 대상이 맞지 않는다."),
     ("after_s6", W, "결론 문장 뒤에 근거 수치가 올 수 없다.")], steps=3,
    view=["In fact, at least 80 percent of people who are exposed to a terrifying event do not experience it."])

crq(c, "CRQ-03", "D3", "다음 글의 빈칸에 들어갈 말을 <보기>의 어구를 모두 배열하여 완성하시오.",
    edit(text(c), ("respond in so many constructive ways that they typically emerge more capable than ever",
                   "________________________________________")),
    ["<보기>의 어구를 모두 한 번씩만 사용할 것", "어구의 형태를 바꾸지 말 것"],
    "respond in so many constructive ways that they typically emerge more capable than ever",
    ["so ~ that 구조(so many constructive ways that)와 emerge + 형용사 보어 어순이 모두 맞으면 5점",
     "so ~ that 구조는 맞으나 typically 위치 또는 more capable than ever 어순 오류 1개 3점", "그 외 0점"], 5,
    view=["typically / that / respond in / emerge / they / so many / constructive ways / more capable than ever"],
    view_label="<보 기>")

# ───────────────────────── 지문 03 · 3-4-3 아이들의 이사 스트레스 ─────────────────────────
c = "3-4-3"
mcq(c, "RDG-08", "D3", "다음 글의 내용과 일치하지 않는 것은?", text(c),
    ["이사는 모든 사람에게 어렵지만 아이들에게 특히 스트레스가 된다.",
     "일상이 깨지면 아이들은 안정감을 잃고 혼란을 느낄 수 있다.",
     "3~6세 아이들은 새집과 새 방을 미리 상상하는 것을 어려워한다.",
     "아이들의 과거 경험보다 새 환경 적응을 돕는 데 집중해야 한다.",
     "자신의 배경을 나눌 기회는 공동체 의식 형성에 도움이 된다."],
    4, 3,
    [("stress_children", W, "1문장과 일치한다."), ("lose_security", M, "2문장과 일치한다."),
     ("literal_age", S, "4문장(이해가 문자 그대로라 미리 상상하기 어렵다)과 일치한다."),
     ("balance_flip", S, "과거 경험 인정과 적응 지원 사이의 '균형'이 중요하다고 했으므로 일치하지 않는다."),
     ("community", M, "마지막 문장과 일치한다.")])

mcq(c, "GRM-01", "D3", "다음 글의 밑줄 친 부분 중, 어법상 틀린 것은?",
    edit(ulist(text(c), "disoriented", "is taken away", "affected", "to imagine", "which is essential"),
         (U("which is essential"), U("what is essential"))),
    ["①", "②", "③", "④", "⑤"], 5, 2,
    [("feel_pp", M, "feel의 보어로 '혼란스러운' 상태를 나타내는 과거분사이다."),
     ("all_that_singular", S, "all that is familiar(익숙한 모든 것)는 단수 취급하므로 is가 맞다."),
     ("passive_affected", M, "아이들이 '영향을 받는' 것이므로 수동이 맞다."),
     ("it_for_to", W, "가주어 it - 진주어 to부정사 구조이다."),
     ("what_vs_which", S, "앞 절의 a sense of community를 받는 계속적 용법이므로 which여야 한다. what은 선행사를 포함한다.")])

mcq(c, "VOC-04", "D3", "주어진 문장에서 밑줄 친 단어와 가장 비슷한 뜻을 가진 단어를 고르시오.",
    edit(sents(c)[5], ("validating", U("validating"))),
    ["evaluating", "acknowledging", "overlooking", "questioning", "abandoning"],
    2, 1,
    [("evaluating", S, "철자(val-)가 비슷한 혼동어로, '평가하다'는 '인정하다'와 다르다."),
     ("acknowledging", S, "validate: (가치·타당성을) 인정하다 = acknowledge."),
     ("overlooking", W, "반의어(못 본 체하다)이다."), ("questioning", M, "타당성을 의심한다는 뜻으로 반대 방향이다."),
     ("abandoning", W, "과거를 버린다는 뜻이 되어 균형과 맞지 않는다.")], steps=1)

s3 = sents(c)
mcq(c, "RDG-05", "D3", "다음 글에서 전체 흐름과 관계 없는 문장은?",
    " ".join(s3[:3] + ["①", s3[3], "②", s3[4], "③", s3[5],
                       "④ Many families find that a new place with a bigger yard gives their children more room to play outside.",
                       "⑤", s3[6], s3[7]]),
    ["①", "②", "③", "④", "⑤"], 4, 2,
    [("literal", W, "어린아이의 문자 그대로의 이해를 설명한다."), ("worries", S, "그 이해에서 나오는 걱정의 예시로 이어진다."),
     ("balance", M, "걱정에 대한 대응 원칙(균형)을 제시한다."),
     ("yard_drift", S, "new place를 그대로 쓰지만 아이의 심리적 적응이 아니라 집의 물리적 장점으로 논점이 벗어난다."),
     ("share_background", M, "균형의 한 축(과거 존중)을 구체화한다.")])

crq(c, "CRQ-02", "D3", "다음 글의 빈칸 (A)~(C)에 주어진 철자로 시작하는 단어를 영영풀이에 맞게 쓰시오. (단, 빈칸의 문법 자리에 맞게 어형을 바꿀 것)",
    edit(text(c), ("feel disoriented", "feel (A) d__________"),
         ("validating children's", "(B) v__________ children's"),
         ("those in transition", "those in (C) t__________")),
    ["영영풀이는 원형(기본형)을 기준으로 주어졌다", "빈칸의 문법 자리에 맞게 어형을 바꾸어 쓸 것"],
    "(A) disoriented  (B) validating  (C) transition",
    ["각 2점", "(A) disorient, (B) validate처럼 원형 그대로 쓰면 해당 빈칸 1점", "철자 오류는 0점"], 6,
    view=["(A) to make someone lose their sense of direction or feel confused",
          "(B) to recognize or confirm that something is worthy, true, or important",
          "(C) the process of changing from one state, place, or condition to another"],
    view_label="<영영풀이>")

# ───────────────────────── 지문 04 · 3-4-4 피부 전도도로 감정 측정 ─────────────────────────
c = "3-4-4"
mcq(c, "RDG-01", "D3", "다음 글의 제목으로 가장 적절한 것은?", text(c),
    ["How to Control Your Emotions by Reducing Sweat", "The Conscious Mind: Master of the Body's Reactions",
     "Skin as a Meter: Turning Feelings into Numbers", "Why Electricity Is Harmful to Human Skin",
     "Subjective Feelings: Something Science Can Never Measure"],
    3, 1,
    [("control_sweat", S, "땀을 줄여 감정을 조절하는 방법은 다루지 않는다(땀은 무의식적으로 나온다)."),
     ("conscious_master", M, "의식은 이 변화에 거의 관여하지 않는다고 했으므로 반대이다."),
     ("skin_numbers", S, "피부 전도도로 주관적 감정 상태를 객관적 수치로 바꾼다는 글 전체를 담는다."),
     ("electric_harm", W, "전류의 해로움은 다루지 않는다."), ("never_measure", M, "측정할 수 있다는 글의 주장과 반대이다.")],
    steps=1)

mcq(c, "GRM-01", "D3", "다음 글의 밑줄 친 부분 중, 어법상 틀린 것은?",
    edit(ulist(text(c), "efficiently", ("electrically conductive", "conductive"), "having", "to put", "transferring"),
         (U("efficiently"), U("efficient"))),
    ["①", "②", "③", "④", "⑤"], 1, 3,
    [("adverb_verb", S, "동사 conducts를 꾸미므로 부사 efficiently여야 한다(more or less는 정도 표현)."),
     ("gets_adj", S, "gets의 보어 형용사이고 electrically가 그것을 꾸민다."),
     ("gerund_subject", S, "전치사 without의 목적어인 동명사 having, your conscious mind는 그 의미상 주어이다."),
     ("allow_to", W, "allow + O + to-v 구조이다."), ("at_gerund", W, "전치사 at의 목적어인 동명사이다.")], steps=2)

mcq(c, "RDG-03", "D4", "다음 글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?",
    edit(ulist(text(c), ("any intense", "intense"), ("electrically conductive", "conductive"), ("your conscious", "conscious"), ("an objective value", "objective"), "subconsciously"),
         (U("subconsciously"), U("consciously"))),
    ["①", "②", "③", "④", "⑤"], 5, 3,
    [("intense_ok", W, "stressed, sad처럼 '강렬한' 감정의 예시와 맞다."),
     ("conductive_ok", M, "땀이 나면 피부가 전기를 더 잘 통하게 된다."),
     ("conscious_ok", S, "변화가 의식의 관여 '없이' 일어난다는 문장이므로 conscious가 맞다(without과 함께 읽어야 한다)."),
     ("objective_ok", S, "주관적 상태에 '객관적' 값을 매긴다는 대조이다."),
     ("subconscious_swap", S, "앞에서 땀샘 활동은 의식 없이 일어난다고 했으므로 몸이 '무의식적으로' 땀을 흘리는 것을 추적해야 한다.")],
    steps=3)

mcq(c, "RDG-09", "D3", "다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?",
    text(c),
    ["deliberately …… subjective", "involuntarily …… collective", "gradually …… temporary",
     "involuntarily …… subjective", "deliberately …… shared"],
    4, 1,
    [("deliberate_subj", S, "(B)는 맞지만 땀샘 활동은 의식의 관여 없이 일어나므로 (A)가 틀리다."),
     ("invol_collective", M, "(A)는 맞지만 측정 대상은 한 개인의 주관적 상태이다."),
     ("gradual_temp", W, "변화 속도나 일시성은 글의 논점이 아니다."),
     ("invol_subj", S, "의식과 무관하게(involuntarily) 일어나는 땀 변화로 주관적(subjective) 감정을 수치화한다."),
     ("deliberate_shared", W, "두 빈칸 모두 글과 맞지 않는다.")], steps=2,
    view=["Because sweat gland activity changes (A) ________ with our emotions, measuring how well our skin "
          "conducts electricity lets scientists express a (B) ________ feeling as an objective number."])

crq(c, "CRQ-01", "D4", "다음 글의 내용을 한 문장으로 요약하고자 한다. <조건>에 맞게 빈칸 (A), (B)에 들어갈 말을 쓰시오.",
    [text(c), "",
     "→ Since emotional stimulation makes us sweat without our awareness and thus raises our skin's electrical "
     "(A)________, scientists can achieve the (B)________ of a subjective state as an objective number."],
    CRQ01_COND, "(A) conductivity  (B) measurement",
    ["(A) conducts/conductive → conductivity: 소유격 skin's electrical 뒤 명사 자리 (2점)",
     "(B) measure → measurement: 관사 the 뒤 명사 자리 (2점)", "단어는 맞고 어형이 틀리면 해당 빈칸 1점"], 4,
    accepted=["(A) conductance"])

bundle = {
    "batch_id": "ENG-N-NGICHUL-L1-20261113", "product_mode": "ARC_N", "subject": "ENG", "generator": "CLAUDE",
    "set_label": "ARC N° 영어", "course": "공통영어2",
    "cover_subtitle": "N기출 고난도 독해 Level 1 · 3-4-1~3-6-4 · 지문당 5문항", "school_line": "동북고등학교 1학년 · 2026 2학기 기말",
    "created_at": "2026-11-13T21:00:00+09:00",
    "scope": "N기출 고난도 독해 Level 1 p78~91 (Mini 모의고사 04~06회, 28지문)",
    "scope_refs": ["NGICHUL-L1-3-4-1~3-6-4"], "workbook_profile": "PASSAGE_5",
    "exam_context_id": "DONGBUK_2026_2_FINAL",
    "sets": [], "items": items,
}
(HERE / "items.yaml").write_text(yaml.safe_dump(bundle, allow_unicode=True, sort_keys=False, width=4000), encoding="utf-8")
print(len(items), "items")
