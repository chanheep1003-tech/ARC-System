# Mini 모의고사 05회 ② 3-5-5 ~ 3-5-10  (generate_items.py가 exec)

# ───────── 3-5-5 빠른 판단 ─────────
c = "3-5-5"
mcq(c, "RDG-01", "D3", "다음 글의 요지로 가장 적절한 것은?", text(c),
    ["Careful thinking always leads to better decisions than quick thinking.",
     "Parents should teach their children to make judgments quickly.",
     "In urgent, critical moments, quick judgments can work better than long thought.",
     "Gathering information is a waste of time in most situations.",
     "First impressions are usually misleading and should be ignored."],
    3, 4,
    [("careful_always", S, "But 이전의 통념으로, 글은 이를 반박한다."),
     ("teach_children", M, "아이들에게 하는 말은 통념의 예시일 뿐이다."),
     ("snap_better", S, "시간에 쫓기는 위급한 상황에서는 순간적 판단이 더 나을 수 있다는 것이 요지이다."),
     ("info_waste", S, "'특정 순간'의 이야기를 '대부분의 상황'으로 과장한 오답이다."),
     ("impressions_wrong", M, "첫인상이 더 나은 수단일 수 있다고 했으므로 반대이다.")])

under(c, "GRM-01", "D4", (1, 4), [("is directly", "is"), ("went into", "went"), ("off gathering", "gathering"),
                                  ("when haste", "when"), ("can offer", "offer")],
      (2, "gather"), 4,
      [("singular_is", M, "주어 the quality(단수)의 동사이다."),
       ("rel_went", S, "선행사 the time and effort를 받는 that절의 과거 동사이다(결정에 '들어간')."),
       ("better_off_ing", S, "be better off -ing(~하는 편이 더 낫다)이므로 동명사 gathering이어야 한다."),
       ("rel_adverb_when", S, "선행사 moments 뒤에 완전한 절이 오므로 관계부사 when이 맞다."),
       ("can_offer", W, "조동사 can + 동사원형이다.")])

under(c, "RDG-03", "D3", (0, 5), ["suspicious", "directly", "careful", "critical", "sharpened"],
      (3, "relaxed"), 1,
      [("suspicious_ok", S, "대부분 빠른 판단을 '의심한다'는 통념의 출발이다."),
       ("directly_ok", M, "결정의 질이 들인 시간에 '정비례한다'고 믿는다."),
       ("careful_ok", M, "신중한 숙고에 시간을 쓰는 편이 낫다는 믿음이다."),
       ("critical_swap", S, "time-driven과 나란히 '위급한(critical)' 상황이어야 순간 판단이 빛난다. relaxed는 반대이다."),
       ("sharpened_ok", W, "생존자들은 빠른 판단 능력을 '연마했다'.")])

mcq(c, "RDG-04", "D4", None,
    edit(text(c), ("can offer better means of making sense of the world", "________________________")),
    ["lead us to make more careless mistakes", "should be checked against more information",
     "can be a better way of understanding the world", "are less useful than careful analysis",
     "depend on how much time we have spent"],
    3, 2,
    [("careless", M, "haste does not make waste와 반대이다."),
     ("check_more", S, "But 이전의 통념(정보를 최대한 모은다)으로 되돌아간 오답이다."),
     ("better_way", S, "원문 'better means of making sense of the world'를 바꿔 쓴 것이다."),
     ("less_useful", S, "But 뒤의 반전을 놓친 오답이다."), ("time_spent", W, "시간을 쏟을수록 좋다는 통념이다.")], steps=3)

mcq(c, "RDG-07", "D3", None,
    slots(c, [0, 1, 2, 3, 5], marks={1: "( ① )", 2: "( ② )", 3: "( ③ )", 5: "( ④ )"}) + " ( ⑤ )",
    NUMS, 4, 3,
    [("after_s1", W, "통념이 다 소개되기 전이다."), ("after_s2", M, "아이들에게 하는 말 예시 앞이다."),
     ("after_s3", S, "③ 뒤 문장도 통념(정보를 최대한 모은다)이라 But의 반전이 너무 이르다."),
     ("after_s4", S, "통념을 모두 제시한 뒤 But으로 반전하고, 생존자들이 '이 교훈'을 배웠다는 문장으로 이어진다."),
     ("end", M, "this lesson이 가리킬 내용이 생존자 문장보다 먼저 나와야 한다.")],
    view=["But there are moments, particularly in time-driven, critical situations, when haste does not make waste, "
          "when our snap judgments and first impressions can offer better means of making sense of the world."])

# ───────── 3-5-6 평범한 유명인 ─────────
c = "3-5-6"
mcq(c, "RDG-01", "D4", "다음 글의 주제로 가장 적절한 것은?", text(c),
    ["why social media stars should learn to act or sing", "the barriers that keep ordinary people from becoming famous",
     "the decline of traditional stars in the age of social media", "how ordinary celebrity changes what it means to be famous",
     "the reasons reality TV stars are criticized by the public"],
    4, 2,
    [("learn_skills", M, "기술 부족 비판은 언급되지만 배우라는 주장은 없다."),
     ("barriers", S, "엘리트 영역으로 넘어가기 어렵다는 언급에 끌린 오답으로, 글은 그 비판이 요점을 놓친다고 했다."),
     ("star_decline", M, "전통 스타의 쇠퇴는 다루지 않는다."),
     ("redefine_fame", S, "평범한 유명인 현상이 명성의 의미를 재구성한다는 것이 주제이다."),
     ("reality_tv", S, "리얼리티 TV 스타는 비교 대상일 뿐이다.")], steps=3)

under(c, "GRM-01", "D3", (0, 3), [("to achieve", "achieve"), ("not having", "having"), ("associated with traditional",
                                  "associated"), "highlights", "misses"],
      (2, "associating"), 2,
      [("to_achieve", W, "an instrument를 꾸미는 to부정사이다."),
       ("for_not_having", S, "전치사 for 뒤의 동명사 부정 not having이다."),
       ("pp_associated", S, "skills and talents가 전통 스타와 '연관된' 것이므로 수동 associated여야 한다."),
       ("singular_highlights", M, "주어 This criticism(단수)의 동사이다."),
       ("singular_misses", M, "주어 the criticism(단수)의 동사이다.")])

under(c, "RDG-03", "D4", (1, 5), ["criticized", "barriers", "reconstructs", ("hierarchical distance", "distance"), "regular"],
      (3, "closeness"), 3,
      [("criticized_ok", M, "기술이 없다고 '비판받는다'."),
       ("barriers_ok", M, "엘리트 영역으로 넘어가는 데 실제 '장벽'이 있다."),
       ("reconstructs_ok", S, "However로 비판이 놓친 점, 즉 명성의 의미를 '재구성한다'는 것이다."),
       ("distance_swap", S, "신비감과 함께 위계적 '거리감'이 별(star)의 특징이어야 일상적 상호작용과 대조된다."),
       ("regular_ok", S, "평범한 사람들과의 '규칙적이고' 잦은 상호작용이다.")], steps=3)

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("relatively high scores on attention scales", "________________________")),
    ["the talent to act or sing in front of others", "a mysterious distance from ordinary fans",
     "relatively high numbers on measures of attention", "the approval of traditional celebrities",
     "a reward given only to hardworking creators"],
    3, 2,
    [("talent", S, "엘리트 유명인의 특징으로 대조 대상이다."), ("mystery", S, "별(star)의 신비감과 거리감은 엘리트 유명인의 특징이다."),
     ("attention_numbers", S, "구독자·팔로워·좋아요 같은 지표, 즉 관심 척도의 높은 수치이다."),
     ("approval", W, "전통 스타의 인정은 무관하다."), ("hardworking", M, "노력에 대한 보상이라는 말은 없다.")])

mcq(c, "RDG-09", "D3", None, text(c),
    ["talent …… competition", "mystery …… competition", "openness …… interaction", "mystery …… interaction",
     "openness …… isolation"],
    4, 2,
    [("talent_comp", M, "(A)는 일부 맞지만 평범한 유명인은 경쟁이 아니라 상호작용으로 관심을 얻는다."),
     ("mystery_comp", S, "(A)는 맞지만 (B)가 틀리다."),
     ("open_interaction", S, "(B)는 맞지만 엘리트 유명인은 신비감으로 상징된다."),
     ("mystery_interaction", S, "엘리트 유명인은 신비감과 거리감, 평범한 유명인은 잦은 상호작용이다."),
     ("open_isolation", W, "두 빈칸 모두 반대이다.")],
    view=["Unlike elite celebrity, which depends on (A) ________ and distance, ordinary celebrity is gained through "
          "frequent (B) ________ with ordinary people."])

# ───────── 3-5-7 능력과 자기 가치 ─────────
c = "3-5-7"
mcq(c, "RDG-02", "D3", "밑줄 친 Period.가 다음 글에서 의미하는 바로 가장 적절한 것은?",
    edit(text(c), ("Period.", U("Period."))),
    ["A person's ability changes over a long period of time.", "Performance should be measured at regular intervals.",
     "That one result is the final word on the person.",
     "People need some rest after an outstanding performance.", "Average people can become outstanding with time."],
    3, 1,
    [("period_time", S, "period의 다른 뜻(기간)에 끌린 오답이다."),
     ("intervals", M, "측정 주기는 다루지 않는다."),
     ("final_judgment", S, "수행이 곧 그 사람이라는 판단에 다른 어떤 것도 고려되지 않는다는 단정이다."),
     ("rest", W, "휴식은 무관하다."), ("become_outstanding", M, "성장 가능성은 다루지 않는다.")])

under(c, "GRM-01", "D3", (0, 3), [("refers to", "refers"), ("reflect how", "how"), ("writing a brilliant", "writing"),
                                  ("how well one plays", "well"), ("However ability", "However")],
      (3, "good"), 5,
      [("singular_refers", W, "주어 ability(단수)의 동사이다."),
       ("how_adj", S, "how smart they are: how + 형용사 + 주어 + 동사이다."),
       ("gerund_list", M, "how smart they are를 보여 주는 동명사구 예시이다."),
       ("adverb_well", S, "동사 plays를 꾸미므로 부사 well이어야 한다."),
       ("however_concession", S, "However + 주어 + may be p.p.: 아무리 ~하게 정의되든(양보).")])

under(c, "RDG-03", "D3", (2, 5), ["attractive", "latest", "sole", ("the only measure", "only"), ("an average person", "average")],
      (2, "minor"), 4,
      [("attractive_ok", W, "매력 있는 것도 능력으로 볼 수 있다."),
       ("latest_ok", M, "'최신' 유행에 밝은 것이다."),
       ("sole_swap", S, "능력이 자기 가치의 '유일한' 결정 요인일 때 문제가 생긴다. minor(사소한)는 뒤 문장(유일한 척도)과 맞지 않는다."),
       ("only_ok", S, "수행이 그 사람의 '유일한' 척도가 된다."),
       ("average_ok", S, "평범한 수행은 '평범한' 사람을 뜻한다.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("the sole determinant of one's self-worth", "________________________")),
    ["the only thing that decides how much a person is worth", "too difficult for most people to develop",
     "measured by teachers rather than by oneself", "shared with others in conversation",
     "defined in terms of intellectual competence alone"],
    1, 5,
    [("sole_worth", S, "원문 'the sole determinant of one's self-worth'를 바꿔 쓴 것이다."),
     ("too_difficult", M, "능력 개발의 어려움은 다루지 않는다."), ("teachers", W, "누가 재는지는 다루지 않는다."),
     ("conversation", W, "대화는 예시일 뿐이다."),
     ("intellectual_only", S, "However ability may be defined(어떻게 정의되든)라고 했으므로 정의 방식이 문제가 아니다.")])

mcq(c, "RDG-07", "D3", None,
    slots(c, [0, 1, 2, 4, 5, 6], marks={1: "( ① )", 2: "( ② )", 4: "( ③ )", 5: "( ④ )", 6: "( ⑤ )"}),
    NUMS, 3, 2,
    [("after_s1", M, "능력의 정의가 아직 다 나오지 않았다."),
     ("after_s2", S, "② 뒤에 매력·유행 등 또 다른 능력의 정의가 이어지므로 이르다."),
     ("after_s3", S, "능력의 여러 정의 뒤에 '어떻게 정의되든'으로 묶고, 수행이 유일한 척도가 된다는 문장으로 이어진다."),
     ("after_s4", M, "The performance becomes the only measure가 주어진 문장보다 먼저 나올 수 없다."),
     ("after_s5", W, "결론 Period. 직전이다.")],
    view=["However ability may be defined, a problem occurs when it is the sole determinant of one's self-worth."])

# ───────── 3-5-8 돈에 대한 청사진 ─────────
c = "3-5-8"
mcq(c, "RDG-01", "D3", "다음 글의 요지로 가장 적절한 것은?", text(c),
    ["Parents should give children money to teach them its value.",
     "Parents' casual words about money can shape children's lifelong beliefs.",
     "Children ask many questions because their parents know everything.",
     "Overspending in adulthood is mainly caused by a lack of income.",
     "Children should always be told the truth about family finances."],
    2, 5,
    [("give_money", M, "용돈 교육은 다루지 않는다."),
     ("casual_words", S, "부모의 무심한 말이 돈에 대한 청사진에 새겨져 평생의 신념이 된다는 것이 요지이다."),
     ("know_all", M, "아이들이 부모를 그렇게 '본다'는 것은 질문이 많은 이유일 뿐이다."),
     ("income_lack", M, "과소비는 결핍감을 피하려는 신념 때문이라고 했다."),
     ("tell_truth", S, "We can't afford that의 해석을 다루지만 재정을 다 알려야 한다는 주장은 없다.")])

under(c, "GRM-01", "D3", (1, 5), [("as soon as", "soon"), ("a way that", "that"), ("get written", "written"),
                                  ("can have", "have"), ("used by parents", "used")],
      (2, "writing"), 5,
      [("as_soon_as", W, "as soon as: ~하자마자."), ("rel_that", M, "a way를 꾸미는 관계사절이다."),
       ("get_pp", S, "답이 청사진에 '새겨지는' 것이므로 get + 과거분사(수동) written이어야 한다."),
       ("can_have", M, "조동사 can + 동사원형이다."),
       ("pp_used", S, "a common phrase가 부모에 의해 '사용되는' 것이므로 과거분사이다.")])

under(c, "RDG-03", "D4", (4, 9), ["passing", "lasting", ("can't afford", "afford"), "deprived", ("to avoid", "avoid")],
      (3, "satisfied"), 2,
      [("passing_ok", M, "'지나가는' 말 한마디도 영향을 준다."),
       ("lasting_ok", S, "Even worse와 이어지는 '지속적인' 영향이다."),
       ("afford_ok", S, "'그걸 살 여유가 없어'라는 흔한 말이다."),
       ("deprived_swap", S, "결핍감을 피하려 과소비한다고 했으므로 '박탈감을 느끼는(deprived)' 것이어야 한다. satisfied는 반대이다."),
       ("avoid_ok", W, "결핍감을 '피하기' 위해 과소비한다.")], steps=3)

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("get written into a money blueprint", "________________________")),
    ["are soon forgotten as we grow up", "shape our core beliefs about money",
     "make us ask even more questions", "are usually too hard for us to understand",
     "teach us how to earn money on our own"],
    2, 1,
    [("forgotten", S, "Even worse와 lasting effect로 이어지므로 잊힌다는 것은 반대이다."),
     ("blueprint_beliefs", S, "원문 'get written into a money blueprint'를 바꿔 쓴 것이다."),
     ("more_questions", M, "질문의 양은 논점이 아니다."),
     ("too_hard", M, "부모는 어린아이가 이해할 수 있게 답한다고 했다."), ("earn_money", W, "돈 버는 법은 다루지 않는다.")])

s58 = sents(c)
mcq(c, "RDG-05", "D3", None,
    " ".join(s58[:5] + ["①", s58[5], "②", s58[6],
                        "③ Many banks now offer special savings accounts that are designed for young children.",
                        "④", s58[7], "⑤", s58[8], s58[9]]),
    NUMS, 3, 5,
    [("afford_example", M, "부모의 흔한 말 예시이다."), ("interpret", M, "아이가 어떻게 해석할지 생각해 보게 한다."),
     ("bank_accounts", S, "아이와 돈을 다루지만 부모의 말이 신념이 된다는 논점에서 벗어난다."),
     ("message", S, "앞 문장의 '해석'을 구체적으로 보여 준다."), ("beliefs_lead", S, "그 신념이 낳는 결과로 이어진다.")])

# ───────── 3-5-9 전자 상거래와 책 ─────────
c = "3-5-9"
mcq(c, "RDG-01", "D3", "다음 글의 제목으로 가장 적절한 것은?", text(c),
    ["Why Physical Bookstores Will Never Disappear", "Books: Where the Online Shopping Boom Began",
     "How Online Shopping Lowered the Quality of Books", "Cars: The Most Popular Online Products",
     "Shelf Space: The Secret of Successful Bookstores"],
    2, 5,
    [("never_disappear", M, "오프라인 매장이 전자 상거래에 자리를 내주었다고 했다."),
     ("books_began", S, "책 판매에서 시작된 온라인 쇼핑이 거대 산업이 된 과정이다."),
     ("quality_lower", W, "책의 질은 다루지 않는다."), ("cars_popular", M, "자동차는 확장의 예시일 뿐이다."),
     ("shelf_secret", S, "선반 공간은 오프라인 매장의 '한계'로 제시되었다.")])

under(c, "GRM-01", "D3", (1, 6), [("fundamentally changed", "changed"), ("was the shift", "was"), ("which is how", "which"),
                                  ("as many titles", "many"), ("led to", "led")],
      (4, "leading"), 2,
      [("verb_changed", W, "주어 the shift의 동사이다."),
       ("inversion_was", S, "부정어 Nowhere가 문두에 나와 be동사와 주어가 도치되었다."),
       ("rel_which", S, "앞 절 전체를 받는 계속적 용법의 which이다."),
       ("many_titles", M, "셀 수 있는 복수명사 titles이므로 many이다."),
       ("main_verb_led", S, "주어 The combination의 정동사 자리이므로 led여야 한다.")])

under(c, "RDG-03", "D4", (2, 8), ["obvious", "space", "aggressive", ("lower prices", "lower"), "expanded"],
      (3, "higher"), 3,
      [("obvious_ok", M, "책 판매에서 변화가 가장 '분명했다'."),
       ("space_ok", S, "선반 '공간'의 한계로 많은 책을 둘 수 없다."),
       ("aggressive_ok", S, "낮은 운영비 덕분에 '공격적인' 할인을 했다."),
       ("lower_swap", S, "앞 문장의 할인과 이어지는 '더 낮은' 가격과 더 많은 선택이 성장을 이끌었다."),
       ("expanded_ok", W, "다른 품목으로 '확장되었다'.")], steps=3)

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("stock as many titles as a virtual bookstore could", "________________________")),
    ["compete with the huge selection of online stores", "sell their books at the same price every day",
     "hire enough workers to help their customers", "offer comfortable spaces for readers",
     "order books from foreign publishers"],
    1, 4,
    [("selection", S, "원문(온라인 서점만큼 많은 종류를 갖출 수 없다)을 바꿔 쓴 것으로 다음 문장(선반 공간의 한계)과 이어진다."),
     ("same_price", M, "가격은 그 뒤에 따로 나온다."), ("workers", W, "직원은 무관하다."),
     ("spaces", S, "space라는 표면어에 끌린 오답이다."), ("foreign", W, "해외 주문은 무관하다.")])

ordering(c, "D3", (0, 1), [(2, 4), (5, 6), (7, 8)], ["C", "A", "B"], 4, 1,
         [("acb", S, "(A)의 In addition to greater variety는 다양성이 언급된 (C) 뒤에 와야 한다."),
          ("bac", W, "(B)의 Before long은 온라인 서점이 성장한 뒤의 일이다."),
          ("bca", W, "(B)가 맨 앞에 올 수 없다."),
          ("cab", S, "책 판매와 선반 한계 (C) → 할인까지 더해져 성장 (A) → 곧 다른 품목으로 확장 (B)."),
          ("cba", M, "(B)의 확장이 (A)의 성장보다 먼저 올 수 없다.")])

# ───────── 3-5-10 마그마와 광물 결정 ─────────
c = "3-5-10"
mcq(c, "RDG-08", "D3", None, text(c),
    ["마그마는 지표에 도달하거나 지하에 갇혀서도 식을 수 있다.",
     "마그마가 식으면 원자들이 가까워지며 화합물을 이루기 시작한다.",
     "마그마 속 원소의 종류는 어떤 광물이 형성될지와 관계가 없다.",
     "마그마가 천천히 식으면 맨눈으로 볼 수 있을 만큼 큰 결정이 생긴다.",
     "마그마가 빨리 식으면 개별 광물 결정을 쉽게 볼 수 없다."],
    3, 5,
    [("cool_surface", W, "2문장과 일치한다."), ("atoms_combine", M, "3문장과 일치한다."),
     ("elements_irrelevant", S, "원소의 종류와 양이 어떤 광물이 생길지를 부분적으로 결정한다고 했다."),
     ("slow_large", M, "7문장과 일치한다."), ("fast_small", S, "마지막 문장과 일치한다.")])

under(c, "GRM-01", "D4", (1, 5), [("called magma", "called"), ("move closer", "move"), ("arrange themselves", "themselves"),
                                  ("partly determine", "determine"), ("depends partly", "depends")],
      (3, "determines"), 5,
      [("pp_called", W, "magma라고 '불리는' 과거분사이다."),
       ("parallel_move", M, "lose, move, begin이 병렬된 동사이다."),
       ("reflexive", S, "주어 atoms와 목적어가 같으므로 재귀대명사 themselves이다."),
       ("plural_determine", S, "주어가 The type and amount(두 가지)이므로 복수동사 determine이어야 한다."),
       ("singular_depends", S, "주어 the size(단수)의 동사이다(of the crystals에 끌리지 않는다).")])

under(c, "RDG-03", "D3", (5, 9), [("how rapidly", "rapidly"), ("cools slowly", "slowly"), ("generally large", "large"), ("enough time", "time"), ("will be small", "small")],
      (2, "tiny"), 5,
      [("rapidly_ok", W, "얼마나 '빨리' 식는지에 달려 있다."), ("slowly_ok", M, "'천천히' 식는 경우이다."),
       ("large_swap", S, "맨눈으로 볼 수 있을 만큼 '큰' 결정이어야 다음 문장(더 큰 결정)과 이어진다."),
       ("time_ok", M, "원자들이 모일 '시간'이 충분하다."), ("small_ok", S, "빨리 식으면 결정이 '작다'.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("This is because the atoms have enough time to move together", "This is because the atoms "
                   "________________________")),
    ["lose all of their heat energy at once", "are pushed apart by the hot magma", "combine with atoms from the air",
     "stop moving as soon as they cool", "are given plenty of time to gather"],
    5, 4,
    [("lose_at_once", M, "한꺼번에 열을 잃는 것은 빨리 식는 경우이다."), ("pushed_apart", W, "원자들은 가까워진다."),
     ("air_atoms", W, "공기 중 원자는 언급되지 않는다."),
     ("stop_moving", S, "식으면 움직임을 멈춘다는 것은 '천천히 모일 시간이 있다'는 설명과 반대이다."),
     ("plenty_time", S, "원문 'have enough time to move together'를 바꿔 쓴 것이다.")])

mcq(c, "RDG-09", "D4", None, text(c),
    ["speed …… faster", "location …… slower", "pressure …… faster", "speed …… slower", "location …… faster"],
    4, 1,
    [("speed_faster", S, "(A)는 맞지만 빨리 식으면 결정이 작아진다."),
     ("location_slower", S, "(B)는 맞지만 결정 크기를 좌우하는 것은 식는 속도이다(지표·지하 모두 식을 수 있다)."),
     ("pressure_faster", W, "압력은 언급되지 않는다."),
     ("speed_slower", S, "결정 크기는 식는 속도에 달려 있고, 천천히 식을수록 결정이 커진다."),
     ("location_faster", W, "두 빈칸 모두 맞지 않는다.")], steps=3,
    view=["The size of the mineral crystals that form from magma depends on its cooling (A) ________: the (B) ________ "
          "it cools, the larger the crystals become."])
