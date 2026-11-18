"""한글 맞춤법 내신형 시범 5문항 (선택형 4 + 서답형 1). 저장소 루트에서 실행.
사용자 피드백(2026-11-18): 암기형 금지, <보기> 조항·새 예문·새 지문 탐구형 선호."""
import yaml
from pathlib import Path
S, M, W = "STRONG", "MEDIUM", "WEAK"
items = []
DEFAULT_TRAP = {"A1_GENERAL_RULE_MAPPING": "T1_RIGHT_CONCEPT_WRONG_CASE", "A2_STUDENT_TEXT_ERRORS": "T6_PARTIAL_SET",
                "A3_CONDITION_CLASSIFICATION": "T2_EXCEPTION_CONDITION", "A4_INQUIRY_DIALOGUE_CHECK": "T4_SAME_FORM_OTHER_FUNCTION"}

def mcq(arch, d, fam, steps, elim, stem, opts, ans, sb, judg, view, neg=False):
    n = len(items) + 1
    js = []
    for i, (cl, c, ev, why, *trap) in enumerate(judg, 1):
        j = {"axis": "orthography", "c": "CORRECT" if i == ans else c, "claim": cl, "ev": ev,
             "v": (i != ans) if neg else (i == ans), "why": why}
        if i != ans:
            j["trap"] = trap[0] if trap else DEFAULT_TRAP[arch]
        js.append(j)
    items.append({"item_id": f"KOR-ONP-{n:03d}", "archetype": arch, "stem": stem, "view": view, "options": opts, "answer": ans,
                  "second_best": sb, "difficulty": d, "family": fam,
                  "balance": "ADVANCED_DISCRIMINATION" if d in ("D4", "D5") else "CORE_EXAM_POINT",
                  "reasoning_steps": steps, "immediate_elimination": elim, "transfer": True,
                  "stem_polarity": "NEGATIVE" if neg else "POSITIVE", "judgments": js})

# 1. 제30항 사이시옷 조항 + 새 단어 적용 (A1)
mcq("A1_GENERAL_RULE_MAPPING", "D3", "VIEW_APPLICATION", 2, 1,
    "<보기>의 한글 맞춤법 조항을 바탕으로 탐구한 내용으로 가장 적절한 것은?",
    ["'전셋집'은 한자어와 순우리말의 합성어로 뒷말이 된소리로 나므로 ㉡에 따라 사이시옷을 적는다.",
     "'횟수'는 한자어끼리 결합한 말이어서 ㉠의 조건을 충족하지 못하므로 '회수'로 적는다.",
     "'뒷일'은 앞말이 모음으로 끝나고 뒷말이 된소리로 나므로 ㉡에 따라 사이시옷을 적는다.",
     "'머릿말'은 순우리말끼리의 합성어이고 앞말이 모음으로 끝나므로 바른 표기이다.",
     "'제삿날'은 한자어끼리 결합한 말이므로 ㉠에 따라 사이시옷을 적을 수 없다."],
    1, 2,
    [("sai30_jeonse", S, ["VIEW", "OPTION1"], "'전세(傳貰)'는 한자어, '집'은 순우리말이고 [전세찝/전섿찝]으로 뒷말이 된소리로 나며 앞말이 모음으로 끝나므로 사이시옷을 적는다."),
     ("sai30_hoetsu", S, ["VIEW", "OPTION2"], "'횟수'는 <보기>의 '다만'에서 예외로 사이시옷을 적는다고 밝힌 여섯 단어 중 하나이다.", "T2_EXCEPTION_CONDITION"),
     ("sai30_dwit_il", M, ["VIEW", "OPTION3"], "'뒷일'은 [뒨닐]로 뒷말의 첫소리 모음 앞에서 'ㄴㄴ' 소리가 덧나는 경우(㉣)이지 된소리(㉡)의 경우가 아니다."),
     ("sai30_meorimal", S, ["VIEW", "OPTION4"], "'머리말'은 [머리말]로 발음되어 된소리나 'ㄴ' 소리가 덧나지 않으므로 사이시옷을 적지 않는다. 앞말이 모음으로 끝나는 것만으로는 조건이 충족되지 않는다.", "T2_EXCEPTION_CONDITION"),
     ("sai30_jesa", W, ["VIEW", "OPTION5"], "'날'은 순우리말이므로 '제사(祭祀)+날'은 한자어와 순우리말의 합성어이며 [제산날]로 'ㄴ' 소리가 덧나 '제삿날'로 적는다.")],
    ["제30항 사이시옷은 다음과 같은 경우에 받치어 적는다.",
     "㉠순우리말로 된 합성어 또는 순우리말과 한자어로 된 합성어로서 앞말이 모음으로 끝난 경우",
     "  (1) ㉡뒷말의 첫소리가 된소리로 나는 것",
     "  (2) ㉢뒷말의 첫소리 'ㄴ, ㅁ' 앞에서 'ㄴ' 소리가 덧나는 것",
     "  (3) ㉣뒷말의 첫소리 모음 앞에서 'ㄴㄴ' 소리가 덧나는 것",
     "다만, 두 음절로 된 한자어 '곳간(庫間), 셋방(貰房), 숫자(數字), 찻간(車間), 툇간(退間), 횟수(回數)'는 사이시옷을 받치어 적는다."])

# 2. 학급 안내문(새 지문)에서 맞춤법에 어긋난 곳 3개 (A2)
mcq("A2_STUDENT_TEXT_ERRORS", "D4", "STUDENT_RESPONSE_EVALUATION", 3, 1, "<보기>의 [A]에 들어갈 말로 적절한 것은?",
    ["㉠, ㉢, ㉣", "㉠, ㉢, ㉥", "㉠, ㉤, ㉥", "㉡, ㉢, ㉥", "㉢, ㉣, ㉤"],
    2, 1,
    [("notice_acd", S, ["VIEW"], "㉣ '등굣길'은 한자어 '등교'와 순우리말 '길'의 합성어로 [등교낄/등굗낄]처럼 된소리가 나므로 사이시옷을 적은 바른 표기이다."),
     ("notice_acf", S, ["VIEW"], "㉠ '몇일'은 '며칠', ㉢ '뒷풀이'는 '뒤풀이'(뒷말 첫소리가 거센소리 'ㅍ'이므로 사이시옷을 적지 않음), ㉥ '줄께요'는 '줄게요'로 고쳐야 한다."),
     ("notice_aef", S, ["VIEW"], "㉤ '참석률'은 'ㄱ' 받침 뒤이므로 '률'로 적는 것이 바르다. 모음이나 'ㄴ' 받침 뒤에서만 '율'로 적는다.", "T2_EXCEPTION_CONDITION"),
     ("notice_bcf", M, ["VIEW"], "㉡ '깨끗이'는 'ㅅ' 받침 뒤에서 '-이'로 적는 바른 표기이다."),
     ("notice_cde", W, ["VIEW"], "㉣ '등굣길', ㉤ '참석률'은 바른 표기이다.")],
    ["학생: 선생님, 제가 쓴 학급 축제 안내문인데 게시하기 전에 맞춤법을 점검해 주세요.",
     "<학생이 쓴 안내문> ㉠몇일 동안 준비한 학급 축제가 드디어 열립니다. 행사가 끝나면 교실을 ㉡깨끗이 정리해 주세요. 정리가 끝난 뒤에는 운동장에서 ㉢뒷풀이를 합니다. 자세한 일정은 ㉣등굣길에 나누어 드린 안내지를 참고하세요. 지난 행사의 ㉤참석률이 낮았던 만큼 이번에는 모두 함께해요. 궁금한 점은 반장에게 물어보면 바로 답해 ㉥줄께요.",
     "선생님: 안내문에서 맞춤법에 어긋난 표기는 [A]란다. 고쳐서 게시하렴."])

# 3. '렬/률'·두음 법칙 조건 분류 (A3)
mcq("A3_CONDITION_CLASSIFICATION", "D3", "COMPARISON_MATRIX", 2, 1,
    "<보기 1>을 바탕으로 <보기 2>의 ㉠~㉤을 분류한 것으로 가장 적절한 것은?",
    ["Ⓐ ㉠, ㉡, ㉣   Ⓑ ㉤   Ⓒ ㉢", "Ⓐ ㉠, ㉣, ㉤   Ⓑ ㉡   Ⓒ ㉢", "Ⓐ ㉣   Ⓑ ㉠, ㉡, ㉤   Ⓒ ㉢",
     "Ⓐ ㉠, ㉣   Ⓑ ㉡   Ⓒ ㉢, ㉤", "Ⓐ ㉠, ㉣   Ⓑ ㉡, ㉤   Ⓒ ㉢"],
    5, 1,
    [("ryul_ng_as_n", S, ["VIEW"], "㉡ '성공률'의 앞 음절 받침은 'ㅇ'이다. 'ㄴ' 받침이 아니므로 Ⓑ에 해당한다.", "T2_EXCEPTION_CONDITION"),
     ("ryul_ng_e", S, ["VIEW"], "㉤ '명중률'도 'ㅇ' 받침 뒤이므로 '률'로 적는 Ⓑ이다.", "T2_EXCEPTION_CONDITION"),
     ("ryul_n_as_other", M, ["VIEW"], "㉠ '백분율'은 'ㄴ' 받침 뒤이므로 Ⓐ이다."),
     ("ryul_e_as_dueum", W, ["VIEW"], "㉤ '명중률'은 단어 첫머리가 아니므로 두음 법칙(Ⓒ)과 관계가 없다.", "T5_RULE_JURISDICTION"),
     ("ryul_correct", S, ["VIEW", "OPTION5"], "㉠ 백분율(ㄴ 받침 뒤)·㉣ 운율(ㄴ 받침 뒤)은 Ⓐ, ㉡ 성공률·㉤ 명중률(ㅇ 받침 뒤)은 Ⓑ, ㉢ 연세(年歲, 단어 첫머리 '년'→'연')는 Ⓒ이다.")],
    ["<보기 1> 한자음 '렬, 률'과 '녀, 뇨, 뉴, 니'의 표기는 놓이는 자리에 따라 달라진다. Ⓐ모음이나 'ㄴ' 받침 뒤에 이어지는 '렬, 률'은 '열, 율'로 적고, Ⓑ그 밖의 받침 뒤에서는 본음대로 '렬, 률'로 적는다. 한편 Ⓒ한자음 '녀, 뇨, 뉴, 니'가 단어의 첫머리에 올 적에는 두음 법칙에 따라 '여, 요, 유, 이'로 적는다.",
     "<보기 2> ㉠ 백분율   ㉡ 성공률   ㉢ 연세(年歲)   ㉣ 운율   ㉤ 명중률"])

# 4. 새 지문(도서관 일기) 띄어쓰기 탐구 대화 (A4)
mcq("A4_INQUIRY_DIALOGUE_CHECK", "D3", "STUDENT_RESPONSE_EVALUATION", 2, 1,
    "<보기>의 ㉠~㉤ 중 학생의 설명으로 적절하지 않은 것은?",
    ["㉠", "㉡", "㉢", "㉣", "㉤"], 4, 1,
    [("lib_de_noun", M, ["VIEW"], "'가는 데'의 '데'는 '일'의 뜻을 나타내는 의존 명사이므로 띄어 쓴다는 설명은 옳다."),
     ("lib_neunde_ending", S, ["VIEW"], "'빌리려는데'의 '-는데'는 뒤 절의 배경을 제시하는 연결 어미의 일부이므로 붙여 쓴다는 설명은 옳다."),
     ("lib_su_bakke", M, ["VIEW"], "'수'는 의존 명사로 띄어 쓰고 '밖에'는 조사로 '수'에 붙여 쓴다는 설명은 옳다."),
     ("lib_ppun_noun_wrong", S, ["VIEW"], "'사람뿐'의 '뿐'은 체언 '사람' 뒤에 붙은 조사이다. 관형사형 뒤에 왔다는 설명은 앞말의 품사를 잘못 판단한 것이다."),
     ("lib_ppun_adn", S, ["VIEW"], "'올 뿐'의 '뿐'은 관형사형 '올' 뒤의 의존 명사이므로 띄어 쓴다는 설명은 옳다.")],
    ["<학생의 일기> 도서관에 가는 데 삼십 분이 걸렸다. 책을 빌리려는데 대출 카드가 없었다. 할 수 없이 친구 카드를 빌릴 수밖에 없었다. 열람실에는 공부하는 사람뿐이었다. 다음에는 일찍 올 뿐 아니라 카드도 꼭 챙겨야겠다.",
     "선생님: 일기에서 앞말과의 띄어쓰기가 서로 다른 부분을 찾아 그 이유를 설명해 볼까요?",
     "학생: ㉠'가는 데'의 '데'는 '일'의 뜻을 나타내는 의존 명사여서 띄어 썼어요. ㉡'빌리려는데'의 '-는데'는 뒤 내용의 배경을 보여 주는 어미의 일부라서 붙여 썼어요. ㉢'빌릴 수밖에'에서 '수'는 의존 명사라서 띄어 쓰고, '밖에'는 조사라서 '수'에 붙여 썼어요. ㉣'사람뿐이었다'의 '뿐'은 관형사형 뒤에 쓰였으므로 의존 명사이지만 예외적으로 붙여 썼어요. ㉤'올 뿐 아니라'의 '뿐'은 관형사형 '올' 뒤에 쓰인 의존 명사라서 띄어 썼어요.",
     "선생님: 한 군데만 빼고 잘 설명했어요."], neg=True)

# 5. 서답형 — 사이시옷을 적지 않는 이유 탐구 (C1)
items.append({
    "item_id": "KOR-ONP-005", "archetype": "C1_CONSTRUCTED_BLANK_SENTENCE", "format": "CR", "points": 5,
    "stem": "<보기>의 탐구 과정을 읽고, ㉠~㉣에 들어갈 말을 <조건>에 따라 서술하시오.",
    "view": ["학생 A: '위층, 피자집, 해님, 개수'는 모두 앞말이 모음으로 끝나는데 왜 사이시옷을 적지 않을까?",
             "학생 B: 사이시옷 조건을 하나씩 따져 보면 돼. '위층'은 뒷말의 첫소리가 이미 ( ㉠ )여서 사이시옷을 적을 필요가 없어. '피자집'은 앞말이 ( ㉡ )라서 조건에 맞지 않아. '해님'은 '해'에 ( ㉢ )가 붙은 파생어여서 합성어가 아니고, '개수(個數)'는 ( ㉣ )끼리 결합했는데 예외로 정한 여섯 단어에도 들지 않기 때문이야."],
    "conditions": ["1. '㉠은 ~, ㉡은 ~, ㉢은 ~, ㉣은 ~이다.'의 완결된 문장으로 쓸 것.",
                   "2. ㉠~㉣은 '된소리, 거센소리, 외래어, 고유어, 한자어, 접두사, 접미사' 중에서 골라 쓸 것.",
                   "3. 문제에서 요구한 내용 외에 문법적 오개념은 내용당 1점씩 감점."],
    "model_answer": "㉠은 거센소리, ㉡은 외래어, ㉢은 접미사, ㉣은 한자어이다.",
    "rubric": ["㉠, ㉡, ㉢, ㉣ 각 1점씩 4점", "문장 형식 1점"],
    "ev": ["VIEW"], "difficulty": "D3"})

bundle = {"batch_id": "KOR-ORTHO-NAESIN-PILOT-20261118", "product_mode": "ARC_N", "subject": "KOR", "generator": "CLAUDE",
          "set_label": "ARC N° 맞춤법 내신형 시범", "course": "공통국어2",
          "cover_subtitle": "한글 맞춤법 · 내신형 시범 5문항 (선택형 4 + 서답형 1)",
          "cover_lines": ["<보기> 조항·새 예문·새 지문을 근거로 판단하는 탐구형"],
          "school_line": "동북고등학교 1학년 · 2026", "created_at": "2026-11-18T12:00:00+09:00",
          "scope": "미래엔 공통국어2 3-(2) 한글 맞춤법과 오늘날의 국어생활 116~127쪽 (2026-2 기말 범위)",
          "scope_refs": ["TEXTBOOK:미래엔 공통국어2 3-(2) 116~127쪽", "NOTICE:DONGBUK_2026_2_FINAL_SCOPE_NOTICE"],
          "archetype_library": "quality/korean/ARC_KOR_GRAMMAR_ARCHETYPES_V1.0.yaml", "sets": [], "items": items}
Path(__file__).with_name("items.yaml").write_text(yaml.safe_dump(bundle, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
print(len(items))
