# Mini 모의고사 05회 ① 3-5-1 ~ 3-5-4  (generate_items.py가 exec)

# ───────── 3-5-1 설계자 없는 설계 ─────────
c = "3-5-1"
mcq(c, "RDG-02", "D4", "밑줄 친 design without a designer가 다음 글에서 의미하는 바로 가장 적절한 것은?",
    edit(text(c), ("design without a designer", U("design without a designer"))),
    ["the careful planning that animals do for their survival", "the selective breeding of dogs and cows by humans",
     "a theory proving that nature must have a creator", "an organism designed to serve several purposes at once",
     "an appearance of purpose produced by a process with no intention"],
    5, 2,
    [("animal_planning", M, "의식적 의도는 아무 역할도 하지 않는다고 했다."),
     ("selective_breeding", S, "인간의 선택 교배는 글에서 말하는 '유일한 진짜 지적 설계'로, 밑줄과 반대 개념이다."),
     ("creator_theory", S, "다윈이 바로 그 가설을 무너뜨렸다고 했다."),
     ("multi_purpose", M, "여러 목적의 설계는 언급되지 않는다."),
     ("purpose_no_intention", S, "자연선택이 무의식적인 우연의 축적으로 '설계된 듯한 겉모습'을 만든다는 뜻이다.")], steps=3)

under(c, "GRM-01", "D3", (1, 6), [("is that natural", "is"), ("as if they were", "were"), ("comes not", "comes"),
                                  ("which we've", "which"), "perpetrated"],
      (0, "are"), 4,
      [("singular_is", S, "주어 the most important thing(단수)의 동사이므로 is여야 한다(about natural selection에 끌리지 않는다)."),
       ("as_if_were", M, "as if + 과거형(사실과 반대되는 가정)이다."),
       ("singular_comes", M, "주어 The design(단수)의 동사이다."),
       ("rel_which", S, "선행사 organisms를 받는 목적격 관계대명사이다."),
       ("pp_perpetrated", W, "a forgery를 뒤에서 꾸미는 수동 분사이다.")])

under(c, "RDG-03", "D3", (2, 7), [("conscious agent", "conscious"), "mindless", "favorable", "deliberately", ("no role", "no")],
      (4, "a central"), 2,
      [("conscious_ok", M, "적응이 '의식적인' 행위자가 만든 것처럼 보인다는 착시이다."),
       ("mindless_ok", S, "설계는 '생각 없는' 우연의 축적에서 나온다."),
       ("favorable_ok", M, "'유리한' 우연이 쌓인다."),
       ("deliberately_ok", S, "인간은 선택 교배로 '의도적으로' 바꾸었다."),
       ("no_role_swap", S, "자연의 설계는 위조품이며 의식적 의도는 '아무 역할도 하지 않는다'가 결론이다.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("the mindless accumulation of favorable accidents over vast periods of time", "________________________")),
    ["the slow piling up of lucky accidents over a very long time", "the careful plans of a conscious creator",
     "the selective breeding carried out by humans", "the sudden changes caused by natural disasters",
     "the intelligence that animals show in their daily lives"],
    1, 3,
    [("lucky_accidents", S, "원문을 바꿔 쓴 것이다."), ("conscious_creator", S, "not from a designer와 정면으로 어긋난다."),
     ("selective_breeding", S, "인간의 의도적 설계로 자연의 설계와 대조된다."),
     ("sudden_disasters", M, "아주 긴 시간에 걸친 축적과 반대된다."), ("animal_intelligence", W, "동물의 지능은 다루지 않는다.")])

ordering(c, "D4", (0, 1), [(2, 3), (4, 5), (6, 7)], ["C", "B", "A"], 5, 2,
         [("acb", M, "(A)의 Beyond that이 가리킬 인간의 선택 교배가 (B)에서 먼저 나와야 한다."),
          ("bac", S, "(B)의 '자연의 설계는 설계자가 아니라 우연에서 나온다'는 (C)의 '그렇지 않다(But they weren't)' 다음에 와야 한다."),
          ("bca", M, "(A)가 마지막이 되지만 (B)가 (C)보다 앞서 논리가 거꾸로이다."),
          ("cab", S, "(A)의 Beyond that은 (B)의 선택 교배를 받으므로 (B) 뒤에 와야 한다."),
          ("cba", S, "의도적 설계처럼 보이지만 아니다 (C) → 설계는 우연의 축적, 진짜 설계는 인간의 교배뿐 (B) → 그 밖은 위조품 (A).")])

# ───────── 3-5-2 눈 맞춤과 문화 차이 ─────────
c = "3-5-2"
mcq(c, "RDG-08", "D3", None, text(c),
    ["가정과 학교의 신념이 다르면 학생에게 어려움이 생길 수 있다.",
     "서구 앵글로 문화에서 눈을 맞추는 것은 존중의 표시이다.",
     "일부 원주민·아시아 문화에서는 눈 맞춤이 무례함의 표시일 수 있다.",
     "교사는 눈을 맞추지 않는 학생을 수업에 관심이 없다고 오해할 수 있다.",
     "교사가 눈 맞춤을 요구하면 학부모는 그 의미를 바로 이해하게 된다."],
    5, 3,
    [("home_school", W, "첫 문장과 일치한다."), ("western_respect", M, "4문장과 일치한다."),
     ("aboriginal_disrespect", S, "5문장과 일치한다."), ("teacher_misread", S, "6문장과 일치한다."),
     ("parents_understand", S, "설명 없이 눈 맞춤을 요구하면 학부모가 오히려 교사가 존중받기를 원하지 않는다고 오해할 수 있다고 했다.")])

under(c, "GRM-01", "D3", (1, 5), [("is interpreted", "interpreted"), ("that is different", "that"), ("in which", "which"),
                                  "attending", ("not listening", "listening")],
      (0, "interpreting"), 3,
      [("passive_interpreted", S, "행동이 '해석되는' 것이므로 수동 is interpreted여야 한다."),
       ("rel_that", M, "선행사 a cultural perspective를 받는 주격 관계대명사이다."),
       ("prep_which", S, "ways in which: 전치사 + 관계대명사로 완전한 절이 뒤따른다."),
       ("prog_attending", M, "are attending to: ~에 주의를 기울이고 있다."),
       ("prog_listening", W, "are not listening의 진행형이다.")])

under(c, "RDG-03", "D3", (3, 6), [("mark of respect", "respect"), ("mark of disrespect", "disrespect"), "authority",
                                  "favour", ("to be respected", "respected")],
      (1, "respect"), 4,
      [("respect_ok", M, "서구 앵글로 문화에서 눈 맞춤은 '존중'의 표시이다."),
       ("disrespect_swap", S, "However로 다른 문화를 대조하므로 '무례함(disrespect)'의 표시여야 한다."),
       ("authority_ok", W, "어린 사람이 '권위' 있는 사람에게 보일 때 특히 그렇다."),
       ("favour_ok", S, "눈 맞춤을 '선호하지' 않는 문화이다."),
       ("respected_ok", M, "학생과 학부모는 교사가 '존중받기'를 원하지 않는다고 오해할 수 있다.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("are not listening or are not interested", "________________________")),
    ["are not paying attention to the lesson", "are showing respect to their teachers",
     "need more time to answer the questions", "prefer to work in groups with friends",
     "come from families that value education"],
    1, 2,
    [("not_attentive", S, "원문 'are not listening or are not interested'를 바꿔 쓴 것이다."),
     ("showing_respect", S, "학생들의 실제 의도이지만, 이 이해가 '없는' 교사의 오해를 묻는 빈칸이므로 맞지 않는다."),
     ("more_time", M, "응답 시간은 다루지 않는다."), ("group_work", W, "모둠 활동은 무관하다."),
     ("value_education", W, "가정의 교육관은 무관하다.")])

mcq(c, "RDG-09", "D3", None, text(c),
    ["varies …… praise", "varies …… misinterpret", "remains …… misinterpret", "remains …… ignore", "disappears …… correct"],
    2, 3,
    [("varies_praise", M, "(A)는 맞지만 이해가 없으면 칭찬이 아니라 오해한다."),
     ("varies_misinterpret", S, "눈 맞춤의 의미는 문화마다 달라서, 이를 모르면 학생의 행동을 오해한다."),
     ("remains_misinterpret", S, "(B)는 맞지만 의미가 같다면 오해가 생기지 않는다."),
     ("remains_ignore", W, "두 빈칸 모두 맞지 않는다."), ("disappears_correct", W, "두 빈칸 모두 맞지 않는다.")],
    view=["Because the meaning of eye contact (A) ________ across cultures, teachers who fail to understand this may "
          "(B) ________ students' behaviour."])

# ───────── 3-5-3 유명세와 진짜 우정 ─────────
c = "3-5-3"
mcq(c, "RDG-01", "D3", "다음 글의 요지로 가장 적절한 것은?", text(c),
    ["Becoming famous is the quickest way to make true friends.", "Anxious people need public attention to feel safe.",
     "Being forgotten by the world is a sign of personal failure.", "Kindness from the public can replace close friendships.",
     "Real safety comes from a few close bonds, not from fame."],
    5, 2,
    [("fame_shortcut", M, "유명세는 우정의 지름길을 찾는 것이지만 진짜 친절은 공적 영역에 없다고 했다."),
     ("anxious_need", S, "불안한 사람일수록 명성을 갈망하지만 바로 그들이 경계해야 한다고 했다."),
     ("forgotten_failure", M, "잊히는 것은 저주나 실패가 아니라고 했다."),
     ("public_kindness", W, "진짜 친절은 공적 영역에서 얻을 수 없다."),
     ("bonds_not_fame", S, "모르는 이들에게 알려지려 하지 말고 진정한 유대를 쌓으라는 것이 요지이다.")])

under(c, "GRM-01", "D3", (2, 6), [("It is the fruit", "is"), ("be won", "won"), ("that can survive", "that"), "feel",
                                  ("Being entirely", "Being")],
      (4, "Be"), 4,
      [("singular_is", W, "real kindness를 받는 It의 동사이다."),
       ("passive_won", M, "친절은 '얻어지는' 것이므로 cannot be won이 맞다."),
       ("rel_that", M, "선행사 genuine bonds를 받는 주격 관계대명사이다."),
       ("plural_feel", S, "주어는 the very anxious(불안한 사람들, 복수)이므로 feel이 맞다."),
       ("gerund_subject", S, "동사 is의 주어 자리이므로 동명사 Being이어야 한다.")])

under(c, "RDG-03", "D3", (0, 4), ["shortcut", ("never", "never"), "intimate", "one-sidedly", "genuine"],
      (0, "detour"), 3,
      [("shortcut_swap", S, "유명세는 우정에 이르는 '지름길'을 찾는 일이라는 진단이다. detour(돌아가는 길)는 반대이다."),
       ("never_ok", M, "Yet으로 진짜 친절은 공적 영역에서 '결코' 얻을 수 없다고 반박한다."),
       ("intimate_ok", S, "소수의 '친밀하고' 상호적인 관계의 열매이다."),
       ("one_sided_ok", M, "멀리서 또는 '일방적으로' 얻을 수 없다."),
       ("genuine_ok", W, "실수를 견디는 '진정한' 유대이다.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("is no curse or sign of failure", "is ________________________")),
    ["nothing to be ashamed of or afraid of", "the worst punishment a person can receive",
     "a natural result of having few friends", "the price anxious people pay for fame",
     "a goal that only famous people can reach"],
    1, 3,
    [("nothing_shameful", S, "원문 'no curse or sign of failure'를 바꿔 쓴 것으로 뒤의 '만족스럽고 안전한 삶의 기초'와 이어진다."),
     ("worst_punishment", M, "세미콜론 뒤 긍정적 평가와 반대이다."),
     ("few_friends", S, "잊힌 삶에서도 진짜 친구를 얻는다고 했으므로 친구가 적은 결과가 아니다."),
     ("price_fame", M, "명성의 대가로 잊힌다는 내용은 없다."), ("only_famous", W, "유명인은 잊힐 수 없다.")])

s53 = sents(c)
mcq(c, "RDG-05", "D3", None,
    " ".join(s53[:1] + ["①", s53[1], "②", s53[2],
                        "③ Many celebrities hire assistants to answer the large number of letters they receive from fans.",
                        "④", s53[3], "⑤", s53[4], s53[5], s53[6]]),
    NUMS, 3, 5,
    [("never_public", M, "유명세에 대한 반박을 시작한다."), ("fruit", M, "진짜 친절의 출처를 설명한다."),
     ("celebrity_letters", S, "유명인을 다루지만 '진짜 우정은 공적 영역에서 얻을 수 없다'는 논점에서 벗어난다."),
     ("one_sided", S, "It(진짜 친절)을 이어 받는다."), ("safety_bonds", S, "결론적 조언으로 이어진다.")])

# ───────── 3-5-4 과학자들의 데이터 공개 ─────────
c = "3-5-4"
mcq(c, "RDG-01", "D3", "다음 글의 주제로 가장 적절한 것은?", text(c),
    ["why scientists share their findings openly with others", "how scientists protect their data from being stolen",
     "the reasons scientific conclusions are often wrong", "the difficulty of testing a hypothesis by experiment",
     "the competition among scientists for new discoveries"],
    1, 3,
    [("share_openly", S, "발견을 공개해 검증과 새 가설에 쓰이게 하는 이유가 주제이다."),
     ("protect_data", M, "독점하지 않는다고 했으므로 반대이다."),
     ("often_wrong", S, "다른 과학자가 결론을 반박할 수 있다는 언급에 끌린 오답이다."),
     ("hard_testing", W, "실험의 어려움은 다루지 않는다."), ("competition", M, "경쟁이 아니라 상호 의존을 말한다.")])

under(c, "GRM-01", "D3", (0, 4), ["prove", ("keep that information", "keep"), "derive", ("makes it possible for other "
                                  "scientists to reconsider", "possible"), ("being limited", "limited")],
      (4, "limiting"), 2,
      [("parallel_prove", W, "make와 or로 병렬된 동사원형이다."),
       ("do_not_keep", M, "do not + 동사원형이다."),
       ("parallel_derive", S, "consider와 and로 병렬된 동사원형이다(alone can consider ... and derive)."),
       ("make_it_possible", M, "make + 가목적어 it + 형용사 + for 의미상 주어 + to-v 구조이다."),
       ("passive_limited", S, "정보가 소수에게 '한정되는' 것이므로 수동 being limited여야 한다.")])

under(c, "RDG-03", "D3", (0, 5), [("to themselves", "themselves"), "available", "refute", ("as widely as", "widely"),
                                  "depends"],
      (3, "narrowly"), 2,
      [("themselves_ok", M, "정보를 '자기들끼리만' 간직하지 않는다."),
       ("available_ok", S, "데이터를 검토할 수 있게 '공개한다'."),
       ("refute_ok", S, "다른 과학자들이 결론을 '반박할' 수도 있다."),
       ("widely_swap", S, "rather than being limited to a few people과 대조되려면 '가능한 한 널리' 퍼져야 한다."),
       ("depends_ok", W, "모든 과학자는 다른 과학자의 연구에 '의존한다'.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("spread as widely as possible, rather than being limited to a few people",
                   "________________________")),
    ["kept within a small group of experts", "shared as broadly as possible",
     "checked by the government first", "published only after it is proven",
     "used to make a profit for scientists"],
    2, 4,
    [("small_group", S, "소수에게 한정하지 않는다는 원문과 반대이다."),
     ("shared_broadly", S, "원문 'spread as widely as possible'을 바꿔 쓴 것이다."),
     ("government", W, "정부 검토는 언급되지 않는다."),
     ("only_proven", S, "다른 과학자들이 검증·반박하도록 공개한다고 했으므로 '증명된 뒤에만'은 맞지 않는다."),
     ("profit", W, "이익은 다루지 않는다.")])

mcq(c, "RDG-09", "D3", None, text(c),
    ["publish …… grows", "hide …… grows", "publish …… shrinks", "sell …… spreads", "hide …… shrinks"],
    1, 3,
    [("publish_grows", S, "과학자들은 데이터를 공개하고, 지식은 널리 공유될 때 늘어난다."),
     ("hide_grows", M, "(B)는 맞지만 과학자들은 정보를 숨기지 않는다."),
     ("publish_shrinks", S, "(A)는 맞지만 사회 전체가 더 많이 알게 된다고 했다."),
     ("sell_spreads", W, "판매는 언급되지 않는다."), ("hide_shrinks", W, "두 빈칸 모두 반대이다.")],
    view=["Scientists (A) ________ their data instead of keeping it to themselves, because knowledge (B) ________ "
          "when it is shared by many."])
