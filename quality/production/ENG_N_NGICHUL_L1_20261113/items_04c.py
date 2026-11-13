# Mini 모의고사 04회 ③ 3-4-11 ~ 3-4-12  (generate_items.py가 exec)

# ───────── 3-4-11 선천적 시각 장애인의 꿈 ─────────
c = "3-4-11"
mcq(c, "RDG-01", "D3", "다음 글의 요지로 가장 적절한 것은?", text(c),
    ["People blind from birth dream as vividly as others, using non-visual senses.",
     "People blind from birth cannot dream because they lack visual memories.",
     "Sighted people remember their friends better than blind people do.",
     "Dreams consist mostly of pictures, no matter who the dreamer is.",
     "Non-visual senses grow weaker in those who are born without sight."],
    1, 2,
    [("vivid_nonvisual", S, "시각 경험 없이도 다른 감각의 경험·기억으로 똑같이 생생한 꿈을 꾼다는 것이 요지이다."),
     ("cannot_dream", S, "그림으로 꿈꾸지 않을 뿐 꿈을 꾼다고 했으므로 반대이다."),
     ("remember_better", M, "친구를 기억하는 방식이 다를 뿐 우열은 없다."),
     ("pictures", M, "그림으로 꿈꾸지 않아도 비슷한 꿈 경험을 한다고 했다."),
     ("weaker_senses", W, "오히려 다른 감각으로 세상을 이해하는 놀라운 능력이 발달한다.")])

under(c, "GRM-01", "D3", (1, 3), [("develop an amazing", "develop"), ("that come", "come"), ("who has been", "has been"),
                                  ("those of", "those"), "constructed"],
      (4, "constructing"), 4,
      [("plural_develop", W, "주어 people의 동사이다."),
       ("rel_plural_come", M, "선행사 experiences and memories(복수)에 맞춘 come이다."),
       ("perfect_since", M, "since birth와 함께 쓰는 현재완료이다."),
       ("pronoun_those", S, "앞의 The dreams(복수)를 받으므로 those가 맞다."),
       ("passive_constructed", S, "꿈이 경험과 기억으로 '구성되는' 것이므로 수동 are constructed여야 한다.")])

under(c, "RDG-03", "D4", (2, 6), ["vivid", ("are unique", "unique"), "familiar", "associate", ("have similar overall", "similar")],
      (4, "duller"), 2,
      [("vivid_ok", M, "정상 시력인의 꿈만큼 '생생할' 수 있다."),
       ("unique_ok", S, "however로 '독특한' 점(비시각적 재료)을 대조한다."),
       ("familiar_ok", W, "'친숙한' 친구를 꿈꾸는 예시이다."),
       ("associate_ok", S, "같은 친구를 비시각적 감각 경험과 '연결한다'."),
       ("similar_swap", S, "시각 장애인도 생생한 꿈을 꾼다는 글의 취지와 맞지 않는다. 전체적인 꿈 경험은 '비슷하다(similar)'여야 하므로 duller는 틀리다.")],
      steps=3)

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("have similar overall dreaming experiences", "________________________")),
    ["dream as richly as sighted people do", "hardly ever have dreams during their sleep",
     "dream only about the people they have touched", "cannot recognize their friends in their dreams",
     "dream mainly about sounds rather than people"],
    1, 3,
    [("rich_dreams", S, "원문 'similar overall dreaming experiences'를 바꿔 쓴 것이다."),
     ("rarely_dream", M, "꿈을 꾸지 않는다는 내용은 없다."),
     ("only_touched", S, "촉각 등 비시각 감각을 쓴다는 점에 끌린 오답으로, '만지는 사람만' 꿈꾼다는 것은 과장이다."),
     ("cannot_recognize", M, "같은 친구를 다른 감각으로 떠올린다고 했다."),
     ("sounds_only", W, "소리만으로 꿈꾼다는 내용은 없다.")])

mcq(c, "RDG-07", "D3", None,
    slots(c, [0, 1, 2, 3, 4, 6], marks={1: "( ① )", 2: "( ② )", 3: "( ③ )", 4: "( ④ )", 6: "( ⑤ )"}),
    NUMS, 5, 4,
    [("after_s1", W, "the same friend가 가리킬 친구가 아직 나오지 않았다."),
     ("after_s2", W, "친구 예시 전이다."), ("after_s3", M, "친구 예시 전이라 the same friend가 성립하지 않는다."),
     ("after_s4", S, "친구가 나오기 직전이라 끌리지만, ④ 뒤 문장이 바로 정상 시력인의 친구 예시이다."),
     ("after_s5", S, "정상 시력인이 친구를 시각 기억으로 꿈꾼다는 문장 뒤에 But으로 시각 장애인의 경우를 대조한다.")], steps=2,
    view=["But, a blind person will associate the same friend with a unique combination of experiences from their "
          "non-visual senses that act to represent that friend."])

# ───────── 3-4-12 실수를 용납하지 않는 비행 ─────────
c = "3-4-12"
mcq(c, "RDG-01", "D3", "다음 글의 제목으로 가장 적절한 것은?", text(c),
    ["Why Driving Is More Dangerous Than Flying", "Business Decisions: Lessons from the Cockpit",
     "How Physics Makes Flying Easy and Natural", "The Role of Technology in Modern Airports",
     "Flying: A System That Forgives No Mistakes"],
    5, 2,
    [("driving_danger", M, "자동차와의 비교는 비행의 위험을 보여 주기 위한 것이고 운전이 더 위험하다는 것은 반대이다."),
     ("business_lessons", S, "비즈니스는 대조 사례일 뿐 교훈의 출처가 아니다."),
     ("physics_easy", M, "비행은 물리 법칙과의 끊임없는 싸움이라고 했다."),
     ("airports", W, "공항 기술은 다루지 않는다."),
     ("forgives_none", S, "단 한 사람의 실수도 재앙이 되는, 용납 없는(unforgiving) 환경이라는 것이 글 전체이다.")])

under(c, "GRM-01", "D3", (2, 7), [("meaning the default", "meaning"), ("typically results", "results"),
                                  ("when encountered", "encountered"), ("everyone working", "working"), "forgetting"],
      (0, "meant"), 3,
      [("participle_meaning", S, "앞 절 전체를 받아 '즉 ~라는 뜻이다'를 나타내는 분사구문이므로 meaning이어야 한다."),
       ("singular_results", M, "주어 a loss of power(단수)의 동사이다."),
       ("elliptic_encountered", S, "when (they are) encountered에서 주어·be동사가 생략된 수동 분사이다."),
       ("gerund_subject", M, "relies on의 목적어 동명사 working, everyone은 의미상 주어이다."),
       ("gerund_forgetting", W, "a single person을 의미상 주어로 하는 동명사구가 주어 자리에 왔다.")])

under(c, "RDG-03", "D3", (0, 4), ["struggle", "naturally", ("default is to crash", "crash"), "unforgiving", "disastrous"],
      (3, "forgiving"), 5,
      [("struggle_ok", M, "비행은 물리 법칙과의 '싸움'이다."), ("naturally_ok", M, "그 속도와 고도는 '자연스럽게' 일어나는 일이 아니다."),
       ("crash_ok", W, "기본값이 '추락'이라는 것이 fail-safe가 아니라는 뜻이다."),
       ("unforgiving_swap", S, "작은 실수도 재앙으로 이어지는 환경이므로 '용납하지 않는(unforgiving)'이어야 한다."),
       ("disastrous_ok", S, "자동차와 대조해 공중의 동력 상실은 '재앙적'이다.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("relies on everyone working at an optimum level", "relies on ________________________")),
    ["every single person doing their job at their best", "a few experts making all the important decisions",
     "machines that can correct any human error", "the pilot's skill in flying through bad weather",
     "rules borrowed from the world of business"],
    1, 2,
    [("everyone_best", S, "원문 'everyone working at an optimum level'을 바꿔 쓴 것이다."),
     ("few_experts", S, "비즈니스에서는 일부만 결정에 참여한다는 대조 문장에 끌린 오답이다."),
     ("machines", M, "단 한 사람의 실수도 재앙이 된다고 했으므로 기계가 보완한다는 것은 맞지 않는다."),
     ("pilot_weather", W, "조종사 한 명이 아니라 모두가 중요하다."), ("business_rules", W, "비즈니스는 대조 대상이다.")])

s12 = sents(c)
mcq(c, "RDG-05", "D3", None,
    " ".join(s12[:2] + ["① Airline tickets have become much cheaper in recent decades, allowing more people to travel by air.",
                        "②", s12[2], "③", s12[3], "④", s12[4], "⑤", s12[5], s12[6], s12[7]]),
    NUMS, 1, 4,
    [("cheap_tickets", S, "항공 여행을 다루지만 비행의 '용납 없는' 위험이라는 논점과 무관하다."),
     ("fail_safe", M, "자연스럽지 않다는 앞 문장을 '기본값이 추락'으로 이어 간다."),
     ("unforgiving", M, "비행 환경의 특성을 정리한다."),
     ("car_vs_air", S, "자동차와 비교해 공중의 위험을 보여 준다."),
     ("business_contrast", S, "however로 이어질 비즈니스 대조 사례이다.")])
