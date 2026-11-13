# Mini 모의고사 05회 ③ 3-5-11 ~ 3-5-12  (generate_items.py가 exec)

# ───────── 3-5-11 밤하늘과 인류 ─────────
c = "3-5-11"
mcq(c, "RDG-01", "D3", "다음 글의 주제로 가장 적절한 것은?", text(c),
    ["the scientific study of the stars in ancient times", "the cultural and practical roles the night sky has played",
     "why people in remote areas still lack calendars", "the dangers of sailing without a navigation tool",
     "how myths about the stars were proven false"],
    2, 1,
    [("ancient_science", S, "달력·항해 같은 실용적 쓰임은 있지만 과학 연구가 주제는 아니다."),
     ("cultural_practical", S, "신화·문화적 정체성(문화)과 시간 기록·항해(실용) 두 측면의 역할이 주제이다."),
     ("lack_calendars", M, "외딴 지역 사람들은 실용적 목적으로 밤하늘을 관찰한다고 했다."),
     ("sailing_danger", W, "항해 도구라는 언급만 있다."), ("myths_false", M, "신화가 거짓으로 밝혀졌다는 내용은 없다.")])

under(c, "GRM-01", "D3", (1, 5), [("people to wonder", "to wonder"), ("ancestors created", "created"),
                                  ("became embedded", "embedded"), ("to keep track", "to keep"), ("vital for", "vital")],
      (0, "wondering"), 4,
      [("inspire_to", S, "inspire + 목적어 + to-v 구조이고 to imagine과 병렬이므로 to wonder여야 한다."),
       ("past_created", M, "과거 사실을 나타내는 과거 동사이다."),
       ("pp_embedded", M, "요소들이 정체성에 '새겨진' 상태를 나타내는 과거분사 보어이다."),
       ("help_to", S, "help + 목적어 + (to) v 구조이므로 to keep도 맞다."),
       ("adj_vital", W, "a useful navigation tool을 뒤에서 보충하는 형용사구이다.")])

under(c, "RDG-03", "D3", (2, 6), ["legendary", "embedded", "essential", "useful", "remote"],
      (3, "useless"), 2,
      [("legendary_ok", M, "밤하늘에 대한 '전설적인' 이야기이다."),
       ("embedded_ok", S, "이야기의 요소들이 문화적 정체성에 '깊이 새겨졌다'."),
       ("essential_ok", M, "농경과 채집을 돕는 '필수적인' 수단이다."),
       ("useful_swap", S, "vital for commerce and exploring과 이어지려면 '유용한' 항해 도구여야 한다."),
       ("remote_ok", W, "오늘날에도 '외딴' 지역 사람들은 실용적 목적으로 하늘을 본다.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("became embedded in the social and cultural identities of many generations", "________________________")),
    ["became part of who many generations were", "were soon forgotten by the next generation",
     "were used only by farmers and sailors", "were replaced by scientific facts", "were written down only by kings"],
    1, 2,
    [("identity", S, "원문(여러 세대의 사회·문화적 정체성에 새겨졌다)을 바꿔 쓴 것이다."),
     ("forgotten", S, "여러 세대에 걸쳐 이어졌다는 흐름과 반대이다."),
     ("farmers_only", M, "농경·항해는 다음 문장의 실용적 쓰임이다."), ("science", M, "과학적 사실은 언급되지 않는다."),
     ("kings", W, "왕은 무관하다.")])

ordering(c, "D3", (0, 1), [(2, 3), (4, 4), (5, 6)], ["B", "A", "C"], 2, 4,
         [("acb", M, "(C)의 also는 실용적 쓰임이 처음 나온 (A) 뒤에 와야 한다."),
          ("bac", S, "신화와 문화적 정체성 (B) → On a practical level 달력 (A) → 또한(also) 항해 도구 (C)."),
          ("bca", M, "(C)의 also가 (A)보다 앞서면 실용적 쓰임의 첫 언급이 없다."),
          ("cab", S, "(C)의 it also provided는 앞선 쓰임의 언급 뒤에 와야 한다."),
          ("cba", W, "흐름이 거꾸로이다.")])

# ───────── 3-5-12 눈 색깔 실험 ─────────
c = "3-5-12"
mcq(c, "RDG-01", "D3", "다음 글의 요지로 가장 적절한 것은?", text(c),
    ["Children with blue eyes learn faster than other children.", "Teachers should never run experiments on students.",
     "Eye color has a strong effect on learning ability.", "Uncertified information is quickly forgotten by students.",
     "What children believe about their ability affects how they learn."],
    5, 3,
    [("blue_faster", S, "첫 번째 정보는 검증되지 않은 것이었고 뒤에서 뒤집힌다."),
     ("no_experiments", M, "실험의 윤리는 다루지 않는다."),
     ("eye_color", S, "결과가 눈 색이 아니라 '들은 말'에 따라 뒤바뀌었으므로 반대이다."),
     ("forgotten", W, "정보가 학습 동기를 크게 바꾸었다."),
     ("belief_matters", S, "자신의 능력에 대한 믿음이 학습 동기와 성적을 좌우한다는 것이 요지이다.")])

under(c, "GRM-01", "D3", (0, 4), [("was conducted", "conducted"), ("who participated", "participated"),
                                  ("have a higher", "have"), ("children write", "write"), ("were monitored", "monitored")],
      (0, "conducting"), 4,
      [("passive_conducted", S, "실험이 '실시된' 것이므로 수동 was conducted여야 한다."),
       ("rel_participated", M, "선행사 The teacher를 받는 관계사절 동사이다."),
       ("plural_have", M, "주어 children의 동사이다."),
       ("causative_had", S, "사역동사 had + 목적어 + 동사원형이므로 write가 맞다."),
       ("passive_monitored", W, "아이들이 '관찰된' 것이다.")])

under(c, "RDG-03", "D3", (2, 8), ["uncertified", "monitored", "dropped", "wrong", ("eyes decreased", "decreased")],
      (4, "increased"), 3,
      [("uncertified_ok", M, "'검증되지 않은' 정보였다."), ("monitored_ok", W, "일주일간 '관찰되었다'."),
       ("dropped_ok", S, "갈색 눈 아이들의 동기는 '떨어졌다'."),
       ("wrong_ok", S, "실험 결과가 '틀렸다'는 보고였다."),
       ("decreased_swap", S, "while로 대조되므로 이번에는 파란 눈 아이들의 동기가 '떨어져야' 한다.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("This time the children with brown eyes excelled in class", "This time ________________________")),
    ["the brown-eyed children did much better in class", "all of the children lost interest in their lessons",
     "the blue-eyed children refused to wear their cards", "the teacher stopped telling students about studies",
     "the children with brown eyes felt confused"],
    1, 2,
    [("brown_better", S, "원문 'the children with brown eyes excelled in class'를 바꿔 쓴 것이다."),
     ("all_lost", S, "while 뒤에 파란 눈 아이들만 동기가 줄었다고 대조하므로 '모두'는 맞지 않는다."),
     ("refuse_cards", W, "카드 거부는 언급되지 않는다."), ("teacher_stop", M, "교사의 행동 변화는 다루지 않는다."),
     ("confused", M, "혼란은 언급되지 않는다.")])

mcq(c, "RDG-07", "D3", None,
    slots(c, [0, 1, 2, 3, 5, 6, 7, 8], marks={1: "( ① )", 2: "( ② )", 3: "( ③ )", 5: "( ④ )", 7: "( ⑤ )"}),
    NUMS, 4, 5,
    [("after_s1", W, "실험 소개 직후라 결과가 나올 수 없다."), ("after_s2", W, "교사의 말 전이다."),
     ("after_s3", M, "카드를 거는 절차 전이다."),
     ("after_s4", S, "'결과는 다음과 같았다' 뒤에 첫 번째 결과가 오고, Then으로 두 번째 말이 이어진다."),
     ("after_s6", S, "두 번째 말 뒤의 결과 자리이지만, 이 자리에는 갈색 눈 아이들이 뛰어나게 된 두 번째 결과가 와야 한다.")],
    view=["Learning motivation for children with brown eyes dropped, and the blue-eyed children became drastically "
          "better in class."])
