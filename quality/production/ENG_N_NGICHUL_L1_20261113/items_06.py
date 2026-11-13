# Mini 모의고사 06회 3-6-1 ~ 3-6-4  (generate_items.py가 exec)

# ───────── 3-6-1 고객은 항상 옳은가 ─────────
c = "3-6-1"
mcq(c, "RDG-01", "D3", "다음 글의 요지로 가장 적절한 것은?", text(c),
    ["Companies should replace every product that customers return.",
     "Businesses sometimes need to say no to unreasonable customers.",
     "Customers who complain are the real reason for a company's success.",
     "E-commerce companies have more difficult customers than others.",
     "Warranty experts should decide which customers a company keeps."],
    2, 1,
    [("replace_all", S, "대부분 교환해 주지만 거절해야 할 때도 있다는 것이 글의 반전이다."),
     ("say_no", S, "손상되지 않았거나 남용된 제품, 무엇을 해도 만족하지 않는 고객에게는 '아니오'라고 해야 한다는 것이 요지이다."),
     ("complainers_success", S, "성공의 이유는 '나머지' 고객들이라고 했다."),
     ("ecommerce_hard", W, "업종 비교는 없다."), ("warranty_decide", M, "보증 전문가는 한 사례의 화자일 뿐이다.")])

under(c, "GRM-01", "D4", (1, 4), [("which makes", "makes"), ("to maintain", "maintain"), ("has been abused", "abused"),
                                  ("who owns", "owns"), ("she says are", "are")],
      (4, "is"), 3,
      [("singular_makes", S, "선행사 a famous company(단수)이므로 makes이다."),
       ("to_purpose", M, "'~하기 위해'를 나타내는 to부정사이다."),
       ("passive_abused", S, "제품이 '남용된' 것이므로 has been abused이다."),
       ("singular_owns", M, "선행사 Lauren Thorp의 동사이다."),
       ("inserted_clause_are", S, "who (she says) are에서 she says는 삽입절이고 who는 the rest of her customers(복수)를 받으므로 are여야 한다.")],
      steps=3)

under(c, "RDG-03", "D4", (1, 4), ["broken", "replacement", "undamaged", "dissatisfied", "success"],
      (2, "damaged"), 4,
      [("broken_ok", M, "'고장 난' 제품을 반품한다."), ("replacement_ok", S, "관계 유지를 위해 '교환품'을 준다."),
       ("undamaged_swap", S, "'아니오'라고 해야 하는 경우이므로 제품이 '손상되지 않았거나' 남용된 때여야 한다. damaged라면 교환 대상이다."),
       ("dissatisfied_ok", S, "무엇을 해도 '불만족할' 고객이다."), ("success_ok", W, "나머지 고객이 '성공'의 이유이다.")],
      steps=3)

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("sometimes you just have to fire a customer", "sometimes you just have to ________________________")),
    ["let go of a customer nobody can please", "give the customer a full refund right away",
     "ask the customer to write a good review", "hire more staff to handle complaints",
     "lower your prices for loyal customers"],
    1, 2,
    [("stop_serving", S, "원문 'fire a customer'(고객을 내보내다)를 바꿔 쓴 것으로 다음 문장과 이어진다."),
     ("full_refund", S, "'고객은 항상 옳다'는 앞부분에 끌린 오답으로 While의 양보와 맞지 않는다."),
     ("good_review", W, "후기는 언급되지 않는다."), ("hire_staff", M, "직원 충원은 다루지 않는다."),
     ("lower_prices", W, "가격은 무관하다.")])

mcq(c, "RDG-09", "D3", None, text(c),
    ["reward …… unsatisfied", "refuse …… unsatisfied", "refuse …… loyal", "reward …… loyal", "ignore …… grateful"],
    2, 3,
    [("reward_unsat", M, "(B)는 맞지만 그런 고객에게는 거절해야 한다."),
     ("refuse_unsat", S, "제품을 남용하거나 무엇을 해도 만족하지 않는 고객은 거절해야 할 때가 있다."),
     ("refuse_loyal", S, "(A)는 맞지만 충성 고객은 오히려 성공의 이유이다."),
     ("reward_loyal", W, "글의 논점과 맞지 않는다."), ("ignore_grateful", W, "두 빈칸 모두 맞지 않는다.")],
    view=["Although companies usually try to keep customers happy, they may have to (A) ________ customers who abuse "
          "products or remain (B) ________ no matter what."])

# ───────── 3-6-2 가상 환경과 고통 ─────────
c = "3-6-2"
mcq(c, "RDG-01", "D4", "다음 글의 주제로 가장 적절한 것은?", text(c),
    ["why virtual worlds should always be free of pain", "the dangers of video games for young players",
     "the history of training programs for soldiers", "how touch makes virtual objects seem more real",
     "when pain can be useful in virtual worlds"],
    5, 1,
    [("pain_free", S, "'고통 없는 편이 낫지 않을까'라는 의문 뒤에 그렇지 않은 상황이 있다고 반박한다."),
     ("game_danger", W, "게임의 위험은 다루지 않는다."),
     ("soldier_history", M, "군인 훈련은 사례일 뿐이다."),
     ("touch_real", S, "촉각 재현이라는 출발점에 끌린 오답으로, 초점은 '고통'이다."),
     ("pain_useful", S, "드물지만 가상 환경에서 고통을 전달하는 능력이 쓸모 있는 경우가 있다는 것이 주제이다.")], steps=3)

under(c, "GRM-01", "D4", (0, 4), [("lies in", "lies"), ("can never be", "be"), ("whether reproducing", "whether"),
                                  ("would ever be", "would"), ("comes in handy", "comes")],
      (0, "lie"), 5,
      [("singular_lies", S, "주어는 긴 수식어(related to ... environments)가 붙은 One important point(단수)이므로 lies여야 한다."),
       ("can_be", W, "조동사 can + be이다."),
       ("whether_clause", S, "wonder의 목적어 명사절을 이끄는 whether이다."),
       ("would_ever", M, "가정적 의문의 would이다."),
       ("singular_comes", S, "선행사 situations가 아니라 절의 주어 the ability(단수)에 맞춘 comes이다.")], steps=3)

under(c, "RDG-03", "D3", (1, 6), [("entirely believable", "believable"), ("\"better\"", "better"), "small", "realism",
                                  "hazard"],
      (1, "worse"), 4,
      [("believable_ok", M, "고통이 없으면 완전히 '믿을 만할' 수 없다."),
       ("better_swap", S, "'가상 세계는 고통이 없는 편이 더 낫지 않나?'라는 반문이어야 하므로 worse는 반대이다."),
       ("small_ok", M, "그런 상황은 인정하건대 '적다'."),
       ("realism_ok", S, "게임에서는 시뮬레이션의 '현실감'을 높인다."),
       ("hazard_ok", W, "군인에게 고통은 직업상 '위험'이다.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("the ability to deliver painful stimulation comes in handy", "________________________")),
    ["pain must be removed for the safety of users", "the ability to deliver pain turns out to be useful",
     "touch cannot be reproduced at all", "soldiers prefer games without any pain",
     "users forget that they are in a game"],
    2, 1,
    [("remove_pain", S, "Even if not immediately intuitive 뒤에는 직관과 반대인 '고통이 유용한' 상황이 와야 한다."),
     ("pain_useful", S, "원문 'comes in handy'를 바꿔 쓴 것이다."),
     ("no_touch", M, "촉각 재현은 가능성을 전제로 한다."), ("soldiers_prefer", W, "군인의 선호는 언급되지 않는다."),
     ("forget_game", W, "무관하다.")])

mcq(c, "RDG-07", "D3", None,
    slots(c, [0, 1, 3, 4, 5, 6], marks={1: "( ① )", 3: "( ② )", 4: "( ③ )", 5: "( ④ )", 6: "( ⑤ )"}),
    NUMS, 2, 3,
    [("after_s1", M, "such kinds of stimulation이 가리킬 painful stimulation이 아직 없다."),
     ("after_s2", S, "고통 없이는 믿을 수 없다는 문장 뒤에 However로 의문을 제기하고, '고통 없는 편이 낫지 않나?'로 이어진다."),
     ("after_s4", S, "반문 뒤에 다시 의문을 제기하면 흐름이 반복된다."),
     ("after_s5", M, "이미 유용한 상황이 있다고 답한 뒤이다."), ("after_s6", W, "사례 제시 직전이다.")],
    view=["However, one might wonder whether reproducing such kinds of stimulation would ever be of any use within "
          "virtual or mediated interactions."])

# ───────── 3-6-3 나눌수록 커지는 지식 ─────────
c = "3-6-3"
mcq(c, "RDG-01", "D3", "다음 글의 제목으로 가장 적절한 것은?", text(c),
    ["Physical Resources: The Key to National Wealth", "Why Wheels Break Faster Than Ideas Spread",
     "Sharing Knowledge Means Losing Your Advantage", "The Hidden Costs of Creating New Ideas",
     "Knowledge: A Resource That Grows When Shared"],
    5, 3,
    [("physical_key", M, "물리적 자원과 대조되는 지식이 중심이다."), ("wheels", M, "바퀴는 비유적 예시이다."),
     ("lose_advantage", S, "한 사람의 이득이 다른 사람의 손실일 필요가 없다고 했으므로 반대이다."),
     ("hidden_costs", W, "비용은 다루지 않는다."),
     ("grows_shared", S, "공유해도 줄지 않고 모두를 이롭게 하는, 본질적으로 풍부한 자원이라는 것이 중심이다.")])

under(c, "GRM-01", "D3", (3, 9), [("are depleted", "depleted"), ("keep on working", "working"), ("all of whom", "whom"),
                                  ("have to be", "have"), ("while impoverishing", "impoverishing")],
      (1, "to work"), 3,
      [("passive_depleted", M, "자원이 '고갈되는' 것이므로 수동이다."),
       ("keep_on_ing", S, "keep on -ing(계속 ~하다)이므로 working이어야 한다."),
       ("all_of_whom", S, "콤마 뒤 접속사 없이 절을 잇는 관계대명사 whom이다(them은 불가)."),
       ("doesnt_have", M, "doesn't have to: ~일 필요는 없다."),
       ("while_ing", W, "접속사 while + 분사이다.")])

under(c, "RDG-03", "D3", (3, 10), ["depleted", "infinite", "loss", "enrich", "abundant"],
      (4, "scarce"), 1,
      [("depleted_ok", S, "물리적 자원은 쓰면 '고갈된다'."), ("infinite_ok", M, "설계도는 '무한한' 사람과 공유할 수 있다."),
       ("loss_ok", M, "한쪽의 이득이 다른 쪽의 '손실'일 필요가 없다."),
       ("enrich_ok", W, "새 아이디어로 모두를 '풍요롭게' 한다."),
       ("abundant_swap", S, "누구도 가난하게 하지 않는 지식의 규칙은 지식을 본질적으로 '풍부하게' 만든다. scarce는 반대이다.")])

mcq(c, "RDG-04", "D4", None,
    edit(text(c), ("but the design for a wheel can be shared with an infinite number of people, all of whom can benefit "
                   "from it", "but the design for a wheel ________________________")),
    ["can be shared by countless people at the same time", "wears out as quickly as the wheel itself",
     "belongs only to the person who made it", "becomes less useful the more it is shared",
     "can only be used in one place at a time"],
    1, 5,
    [("countless_share", S, "원문(무한한 사람과 공유해 모두가 이득을 본다)을 바꿔 쓴 것이다."),
     ("wears_out", M, "바퀴는 닳아도 바퀴의 아이디어는 계속 작동한다고 했다."),
     ("belongs_one", M, "공유를 강조하는 글과 반대이다."),
     ("less_useful", S, "물리적 자원의 성질(나누면 줄어든다)을 지식에 적용한 오답이다."),
     ("one_place", S, "but 앞의 '바퀴'에 해당하는 성질로, 설계도와 대조된다.")], steps=3)

mcq(c, "RDG-09", "D3", None, text(c),
    ["increased …… harming", "reduced …… helping", "reduced …… harming", "protected …… informing", "increased …… helping"],
    3, 2,
    [("increased_harm", M, "(B)는 맞지만 물리적 자원은 쓰면 줄어든다."),
     ("reduced_help", S, "(A)는 맞지만 '누구도 돕지 않고'는 모두를 이롭게 한다는 글과 반대이다."),
     ("reduced_harm", S, "물리적 자원은 쓰고 나누면 줄지만, 지식은 누구도 해치지(가난하게 하지) 않고 모두에게 이롭다."),
     ("protected_inform", W, "글과 무관하다."), ("increased_help", W, "두 빈칸 모두 맞지 않는다.")],
    view=["Unlike physical resources, which are (A) ________ when used or shared, knowledge can benefit everyone "
          "without (B) ________ anyone."])

# ───────── 3-6-4 위대한 작곡가와 독창성 ─────────
c = "3-6-4"
mcq(c, "RDG-01", "D3", "다음 글의 요지로 가장 적절한 것은?", text(c),
    ["Salieri was a poor composer who simply copied Mozart's music.",
     "Music that sounds familiar is easier for people to remember.",
     "Great composers were great largely because their works were original.",
     "Most people today understand Beethoven's works perfectly.",
     "Movies are the best way to learn about classical composers."],
    3, 1,
    [("salieri_poor", S, "Salieri는 아주 좋은 작곡가였다고 했다."),
     ("familiar_easy", M, "익숙함은 비교적 주변적인 진술이다."),
     ("original_great", S, "당대에 이해받지 못한 생소함, 즉 독창성이 위대함의 조건이라는 것이 요지이다."),
     ("understand_now", W, "오늘날의 이해는 다루지 않는다."), ("movies", M, "영화는 예시를 끌어오는 도구일 뿐이다.")])

under(c, "GRM-01", "D4", (0, 4), [("were misunderstood", "misunderstood"), ("could understand", "understand"),
                                  ("is unfamiliarity", "is"), ("expressed within", "expressed"), ("so great", "great")],
      (3, "expressing"), 3,
      [("passive_misunderstood", M, "작곡가들이 '오해받은' 것이므로 수동이다."),
       ("could_understand", W, "조동사 + 동사원형이다."),
       ("singular_is", S, "주어 The reason(단수)의 동사이다(for this initial lack of acceptance에 끌리지 않는다)."),
       ("pp_expressed", S, "ideas가 형식 안에서 '표현된' 것이므로 과거분사 expressed여야 한다."),
       ("adj_great", S, "make + 목적어 + 형용사 보어이므로 great가 맞다.")], steps=3)

under(c, "RDG-03", "D4", (5, 10), [("their own ideas", "own"), ("most famous", "famous"), ("a bad composer", "bad"),
                                   ("wasn't original", "original"), ("just like", "like")],
      (3, "popular"), 3,
      [("own_ok", S, "훌륭한 작곡가는 '자신만의' 생각을 갖는다."),
       ("famous_ok", W, "가장 '유명한' 비(非)위대 작곡가로 그려진다."),
       ("bad_ok", S, "Salieri는 '나쁜' 작곡가가 아니었다는 양보이다."),
       ("original_swap", S, "다음 문장(남들이 쓰는 것과 똑같이 들렸다)이 이유를 설명하므로 '독창적이지' 않았기 때문이어야 한다. popular는 이와 무관하다."),
       ("like_ok", M, "당시 다른 작곡가들의 곡과 '똑같이' 들렸다.")], steps=3)

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("The reason for this initial lack of acceptance is unfamiliarity.",
                   "The reason for this initial lack of acceptance is ________________________.")),
    ["that the composers did not have enough talent", "that their works were too short to enjoy",
     "that their music was too new for people to be used to", "that people preferred to hear Salieri's music",
     "that concerts were too expensive at the time"],
    3, 1,
    [("no_talent", S, "위대한 작곡가들이므로 재능 부족은 맞지 않는다."), ("too_short", W, "곡의 길이는 무관하다."),
     ("too_new", S, "원문 'unfamiliarity'를 바꿔 쓴 것으로 다음 문장(형식과 생각이 완전히 새로웠다)과 이어진다."),
     ("salieri_pref", M, "Salieri는 뒤에 나오는 대조 사례이다."), ("expensive", W, "무관하다.")])

ordering(c, "D3", (0, 1), [(2, 5), (6, 7), (8, 10)], ["A", "C", "B"], 1, 4,
         [("acb", S, "이해받지 못한 이유는 생소함, 그것이 위대함의 조건 (A) → 영화 Amadeus와 Salieri (C) → Salieri는 독창적이지 않아 위대하지 못했다 (B)."),
          ("bac", W, "(B)의 Now, Salieri는 Salieri가 소개된 (C) 뒤에 와야 한다."),
          ("bca", W, "(B)가 맨 앞에 올 수 없다."),
          ("cab", S, "(A)의 this initial lack of acceptance는 주어진 글(오해받았다)을 바로 받아야 한다."),
          ("cba", M, "(A)가 맨 뒤면 this initial lack of acceptance가 가리킬 내용과 멀어진다.")])
