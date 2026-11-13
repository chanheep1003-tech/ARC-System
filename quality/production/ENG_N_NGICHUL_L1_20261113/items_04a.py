# Mini 모의고사 04회 ① 3-4-1 ~ 3-4-5  (generate_items.py가 exec)

# ───────── 3-4-1 고객 만족과 수익성의 균형 ─────────
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
     ("relative_level", S, "경쟁사 대비 높은 만족은 추구하는 바이고, 밑줄은 그 만족을 이익을 버리면서까지 올리지 않는다는 것이다."),
     ("credo_secret", W, "credo는 고객 만족 열정을 요약한 것이지 비밀이 아니다.")])

under(c, "GRM-01", "D3", (2, 6), ["is summed up", "promises", ("seeks to deliver", "to deliver"), "lowering", "profitably"],
      (1, "promise"), 1,
      [("passive_summed", S, "passion이 '요약되는' 것이므로 수동태가 맞다."),
       ("rel_agreement", S, "선행사 its credo가 단수이므로 promises로 고쳐야 한다."),
       ("seek_to", M, "seek은 to부정사를 목적어로 취한다."),
       ("by_gerund", W, "전치사 by의 목적어 자리이므로 동명사 lowering이 맞다."),
       ("adverb_mod", M, "동사 generate를 꾸미는 부사이므로 profitably가 맞다.")])

under(c, "RDG-03", "D3", (3, 7), ["maximize", ("always increase", "increase"), ("in lower profits", "lower"),
                                  ("value profitably", "profitably"), "delicate"],
      (4, "effortless"), 1,
      [("maximize_ok", S, "앞의 does not attempt와 함께 '극대화하려 하지는 않는다'는 핵심 대조를 이룬다."),
       ("increase_ok", M, "가격 인하·서비스 확대로 만족도를 '높일' 수 있다는 흐름이다."),
       ("lower_ok", M, "그 결과 이익이 '더 낮아질' 수 있다."),
       ("profitably_ok", W, "이익을 내며 고객 가치를 창출한다는 결론이다."),
       ("delicate_swap", S, "가치 창출과 이익 유지 사이의 '미묘한(delicate)' 균형이어야 하므로 effortless는 반대이다.")])

mcq(c, "RDG-04", "D4", None,
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

mcq(c, "RDG-09", "D3", None, text(c),
    ["low …… profitably", "high …… generously", "high …… profitably", "stable …… freely", "low …… cheaply"],
    3, 2,
    [("low_profit", M, "(B)는 맞지만 고객 중심 기업은 경쟁사보다 높은 만족을 추구한다."),
     ("high_generous", S, "(A)는 맞지만 'give away the house' 하지 않는다는 결론과 반대이다."),
     ("high_profit", S, "높은 만족은 유지하되 극대화하지 않고, 이익을 내며 가치를 창출한다."),
     ("stable_free", W, "두 빈칸 모두 글과 맞지 않는다."), ("low_cheap", W, "두 빈칸 모두 글과 맞지 않는다.")],
    view=["A customer-centered firm keeps customer satisfaction (A) ________ rather than maximizing it, because "
          "marketing aims to create customer value (B) ________."])

# ───────── 3-4-2 외상 후 성장 ─────────
c = "3-4-2"
mcq(c, "RDG-01", "D2", "다음 글의 요지로 가장 적절한 것은?", text(c),
    ["Experts should pay more attention to post-traumatic stress syndrome.",
     "A single bad event usually has less impact on us than a good one.",
     "Most people who experience trauma need professional treatment.",
     "Growth after trauma is far more common than lasting harm.",
     "Avoiding terrifying events is the key to becoming more mature."],
    4, 1,
    [("more_attention_pts", S, "Seligman은 PTSS에 관심이 쏠리는 것을 한탄했으므로 반대 진술이다."),
     ("bad_weaker", M, "글은 나쁜 사건 하나가 좋은 사건보다 더 강력하다고 했다."),
     ("therapy_needed", M, "80% 이상이 PTSS를 겪지 않는다고 했으므로 맞지 않는다."),
     ("growth_common", S, "외상 후 성장이 훨씬 널리 퍼져 있고 결국 더 강해진다는 것이 요지이다."),
     ("avoid_events", W, "끔찍한 사건을 피하는 것에 대한 내용은 없다.")], steps=1)

mcq(c, "GRM-02", "D4", None,
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

under(c, "RDG-03", "D3", (1, 3), [("made them stronger", "stronger"), "lamented", "lavished", "mistakenly", "terrifying"],
      (3, "correctly"), 5,
      [("stronger_ok", M, "외상 경험이 사람을 '더 강하게' 만들었다는 성장의 예시이다."),
       ("lamented_ok", M, "PTSS에만 관심이 쏠리는 것을 '한탄했다'는 흐름이다."),
       ("lavished_ok", W, "관심이 PTSS에 '아낌없이 쏟아진다'는 뜻이다."),
       ("mistakenly_swap", S, "Seligman이 한탄한 이유는 사람들이 나쁜 사건의 효과를 '잘못' 기대하게 되기 때문이므로 correctly는 반대이다."),
       ("terrifying_ok", S, "외상을 일으키는 '끔찍한' 사건이다.")])

mcq(c, "RDG-07", "D4", None,
    slots(c, [0, 1, 2, 4, 5, "( ⑤ )"], marks={1: "( ① )", 2: "( ② )", 4: "( ③ )", 5: "( ④ )"}),
    NUMS, 3, 2,
    [("after_s1", S, "① 앞 문장은 PTG로 끝나 it이 PTG를 가리키게 되어 'PTG를 겪지 않는다'는 모순이 된다."),
     ("after_s2", S, "②는 성장 사례 뒤라 it이 가리킬 PTSS가 없고 Seligman 문장으로 이어지는 흐름도 끊긴다."),
     ("after_s3", S, "PTSS에 관심이 쏠려 나쁜 사건의 부정적 효과를 기대한다는 오해 뒤에, In fact로 반박 수치를 제시한다."),
     ("after_s5", M, "④ 앞은 life's challenges로 끝나 it이 가리킬 대상이 맞지 않는다."),
     ("after_s6", W, "결론 문장 뒤에 근거 수치가 올 수 없다.")], steps=3,
    view=["In fact, at least 80 percent of people who are exposed to a terrifying event do not develop post-traumatic stress syndrome."])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("people respond in so many constructive ways that they typically emerge more capable than ever of "
                   "confronting life's challenges", "people ________________________")),
    ["become so fearful of bad events that they avoid any challenge",
     "respond so constructively that they end up better able to face hardships",
     "forget their trauma completely and return to their former selves",
     "remain stuck in the negative effects that the event produced",
     "rely on experts in order to recover from the stress syndrome"],
    2, 3,
    [("fearful_avoid", M, "결국 더 강해진다는 마지막 문장과 반대이다."),
     ("constructive_capable", S, "원문(건설적으로 반응해 삶의 도전에 맞설 능력이 더 커진다)을 바꿔 쓴 것이다."),
     ("forget_return", S, "회복에 그치지 않고 이전보다 더 강해진다는 점에서 맞지 않는다."),
     ("stuck_negative", M, "Even though가 이끄는 앞 절의 내용(나쁜 사건이 더 강력함)과만 이어지는 오답이다."),
     ("rely_experts", W, "전문가 의존은 언급되지 않는다.")])

# ───────── 3-4-3 아이들의 이사 스트레스 ─────────
c = "3-4-3"
mcq(c, "RDG-08", "D3", None, text(c),
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

under(c, "GRM-01", "D3", (1, 7), ["disoriented", "is taken away", "affected", "to imagine", "which is essential"],
      (4, "what is essential"), 2,
      [("feel_pp", M, "feel의 보어로 '혼란스러운' 상태를 나타내는 과거분사이다."),
       ("all_that_singular", S, "all that is familiar(익숙한 모든 것)는 단수 취급하므로 is가 맞다."),
       ("passive_affected", M, "아이들이 '영향을 받는' 것이므로 수동이 맞다."),
       ("it_for_to", W, "가주어 it - 진주어 to부정사 구조이다."),
       ("what_vs_which", S, "앞의 a sense of community를 받는 계속적 용법이므로 which여야 한다. what은 선행사를 포함한다.")])

under(c, "RDG-03", "D3", (3, 6), ["literal", "worries", "balance", ("adjust to", "adjust"), "respects"],
      (3, "object"), 3,
      [("literal_ok", M, "새집을 미리 상상하지 못하는 이유로 '문자 그대로의' 이해가 맞다."),
       ("worries_ok", W, "뒤의 질문들은 아이들의 '걱정'의 예시이다."),
       ("balance_ok", S, "과거 인정과 적응 지원 사이의 '균형'이 글의 핵심이다."),
       ("adjust_swap", S, "새 환경에 '적응하도록(adjust to)' 돕는 것이어야 하며, object to(반대하다)는 흐름과 반대이다."),
       ("respects_ok", M, "과거를 정체성의 일부로 '존중하는' 방식이다.")])

s3 = sents(c)
mcq(c, "RDG-05", "D3", None,
    " ".join(s3[:3] + ["①", s3[3], "②", s3[4], "③", s3[5],
                       "④ Many families find that a new place with a bigger yard gives their children more room to play outside.",
                       "⑤", s3[6], s3[7]]),
    NUMS, 4, 2,
    [("literal", W, "어린아이의 문자 그대로의 이해를 설명한다."), ("worries", S, "그 이해에서 나오는 걱정의 예시로 이어진다."),
     ("balance", M, "걱정에 대한 대응 원칙(균형)을 제시한다."),
     ("yard_drift", S, "new place를 그대로 쓰지만 아이의 심리적 적응이 아니라 집의 물리적 장점으로 논점이 벗어난다."),
     ("share_background", M, "균형의 한 축(과거 존중)을 구체화한다.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("validating children's past experiences", "________________________")),
    ["making children forget their old homes quickly",
     "teaching children how to pack their own belongings",
     "choosing a house that looks like the old one",
     "keeping children away from their new classmates",
     "acknowledging what children have been through before"],
    5, 1,
    [("forget_old", S, "균형의 다른 한 축이 새 환경 적응이므로, 과거를 잊게 하는 것은 균형이 아니라 한쪽 치우침이다."),
     ("pack_belongings", W, "짐 싸기는 다루지 않는다."), ("same_house", M, "집의 외형은 논점이 아니다."),
     ("away_classmates", W, "공동체 의식 형성과 반대이다."),
     ("acknowledge_past", S, "뒤 문장(과거를 존중하며 배경을 나눌 기회)과 이어지는 '과거 경험 인정'이다.")])

# ───────── 3-4-4 피부 전도도로 감정 측정 ─────────
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

under(c, "GRM-01", "D3", (2, 7), [("electrically conductive", "conductive"), "having", "to put", ("by tracking", "tracking"),
                                  "transferring"],
      (1, "has"), 1,
      [("gets_adj", S, "gets의 보어 형용사이고 electrically가 그것을 꾸민다."),
       ("gerund_subject", S, "전치사 without 뒤에는 동명사 having이 와야 하고 your conscious mind는 그 의미상 주어이다."),
       ("allow_to", W, "allow + O + to-v 구조이다."), ("by_gerund", M, "전치사 by의 목적어인 동명사이다."),
       ("at_gerund", W, "전치사 at의 목적어인 동명사이다.")])

under(c, "RDG-03", "D4", (1, 6), [("any intense", "intense"), ("electrically conductive", "conductive"),
                                  ("your conscious", "conscious"), ("an objective value", "objective"), "subconsciously"],
      (4, "consciously"), 3,
      [("intense_ok", W, "stressed, sad처럼 '강렬한' 감정의 예시와 맞다."),
       ("conductive_ok", M, "땀이 나면 피부가 전기를 더 잘 통하게 된다."),
       ("conscious_ok", S, "변화가 의식의 관여 '없이' 일어난다는 문장이므로 conscious가 맞다(without과 함께 읽어야 한다)."),
       ("objective_ok", S, "주관적 상태에 '객관적' 값을 매긴다는 대조이다."),
       ("subconscious_swap", S, "땀샘 활동은 의식 없이 일어난다고 했으므로 몸이 '무의식적으로' 땀을 흘리는 것을 추적해야 한다.")],
      steps=3)

mcq(c, "RDG-09", "D3", None, text(c),
    ["deliberately …… subjective", "involuntarily …… collective", "gradually …… temporary",
     "involuntarily …… subjective", "deliberately …… shared"],
    4, 1,
    [("deliberate_subj", S, "(B)는 맞지만 땀샘 활동은 의식의 관여 없이 일어나므로 (A)가 틀리다."),
     ("invol_collective", M, "(A)는 맞지만 측정 대상은 한 개인의 주관적 상태이다."),
     ("gradual_temp", W, "변화 속도나 일시성은 글의 논점이 아니다."),
     ("invol_subj", S, "의식과 무관하게(involuntarily) 일어나는 땀 변화로 주관적(subjective) 감정을 수치화한다."),
     ("deliberate_shared", W, "두 빈칸 모두 글과 맞지 않는다.")],
    view=["Because sweat gland activity changes (A) ________ with our emotions, measuring how well our skin "
          "conducts electricity lets scientists express a (B) ________ feeling as an objective number."])

ordering(c, "D3", (0, 0), [(1, 2), (3, 4), (5, 7)], ["B", "C", "A"], 3, 4,
         [("acb", W, "(A)의 This는 측정 가능성을 가리키므로 땀 변화가 무의식적이라는 (C)보다 앞설 수 없다."),
          ("bac", M, "(C)가 (A)보다 먼저 와야 '무의식적 변화 → 그래서 객관적 측정에 유용' 흐름이 된다."),
          ("bca", S, "땀과 전도도 (B) → 그 변화는 무의식적 (C) → 그래서 과학적으로 유용하다 (A)."),
          ("cab", S, "(C)의 This change in sweat gland activity는 땀이 언급된 (B) 뒤에 와야 한다."),
          ("cba", M, "(C)가 맨 앞이면 This change가 가리킬 대상이 없다.")])

# ───────── 3-4-5 음악 선택의 부담 ─────────
c = "3-4-5"
mcq(c, "RDG-01", "D3", "다음 글의 주제로 가장 적절한 것은?", text(c),
    ["the growing popularity of radio as a guide to new music",
     "the burden of choosing music that comes with unlimited access",
     "the decline of physical music collections in the digital age",
     "how music distributors decide which songs become hits",
     "the role of technology in improving the quality of sound"],
    2, 3,
    [("radio_popular", W, "라디오의 '선별자' 역할이 사라졌다고 했으므로 반대이다."),
     ("burden_choice", S, "음악을 마음껏 접할 수 있게 되었지만 스스로 골라야 하는 노력이 커졌다는 것이 주제이다."),
     ("physical_decline", S, "디지털 라이브러리를 실물 음반처럼 정리한다는 비교는 있지만 실물 음반의 쇠퇴가 주제는 아니다."),
     ("distributor_hits", M, "유통사의 제한된 목록에서 벗어났다는 언급뿐이다."),
     ("sound_quality", W, "음질은 다루지 않는다.")])

under(c, "GRM-01", "D3", (1, 5), ["given", "confronted", "in which", "organizing", ("actively has to choose", "has")],
      (4, "have"), 3,
      [("perfect_given", W, "has given + 간접목적어 + 직접목적어 구조이다."),
       ("perfect_confronted", M, "has also confronted them with ~: ~에 직면하게 하다."),
       ("prep_relative", S, "orient themselves in genres이므로 전치사 in + which가 맞다."),
       ("parallel_organizing", M, "filtering out과 병렬인 동명사로 start의 목적어이다."),
       ("subject_verb", S, "주어 the individual(단수)이므로 has to choose가 맞다. 앞의 긴 수식어구에 끌려 복수로 쓰지 않는다.")],
      steps=2)

under(c, "RDG-03", "D3", (1, 6), ["control", ("countless genres", "countless"), "physical", "restricted", "considerable"],
      (1, "few"), 5,
      [("control_ok", M, "대중적 이용 가능성이 소리 환경에 대한 '통제권'을 주었다."),
       ("countless_swap", S, "However로 이어지며 '수많은' 장르 속에서 길을 찾아야 하는 부담을 말하므로 few는 반대이다."),
       ("physical_ok", W, "디지털 라이브러리와 대비되는 '실물' 음반이다."),
       ("restricted_ok", M, "유통사의 제한된 목록에 '제한되지' 않는다."),
       ("considerable_ok", S, "스스로 골라야 하므로 '상당한' 노력이 든다는 결론이다.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("The search for the right song is thus associated with considerable effort.",
                   "The search for the right song is thus ________________________.")),
    ["left entirely to the local radio stations", "a matter of chance rather than of choice",
     "easier than it was in the days of records", "a task that demands a lot of work from the listener",
     "no longer necessary for most music lovers"],
    4, 3,
    [("radio_left", M, "라디오의 선별 없이 개인이 골라야 한다고 했으므로 반대이다."),
     ("chance", M, "개인이 '능동적으로' 선택해야 한다고 했다."),
     ("easier", S, "통제권이 커져 쉬워졌다고 착각하게 만드는 오답으로, 선택의 부담이 커졌다는 결론과 반대이다."),
     ("demanding_task", S, "원문 'associated with considerable effort'를 바꿔 쓴 것이다."),
     ("unnecessary", W, "검색이 필요 없다는 내용은 없다.")])

mcq(c, "RDG-07", "D4", None,
    slots(c, [0, 1, 2, 3, 5, 6, "( ⑤ )"], marks={1: "( ① )", 2: "( ② )", 3: "( ③ )", 5: "( ④ )"}),
    NUMS, 4, 3,
    [("after_s1", M, "아직 실물 음반과의 비교가 나오지 않아 the difference가 가리킬 대상이 없다."),
     ("after_s2", S, "However가 연달아 나오고 difference의 비교 대상도 없다."),
     ("after_s3", S, "② 뒤 문장(수많은 장르) 다음에 오면 '차이점'의 비교 대상(실물 음반)이 아직 없다."),
     ("after_s4", S, "디지털 라이브러리를 실물 음반처럼 정리한다는 문장 뒤에, However로 '선택이 개인의 손에 있다'는 차이를 말한다."),
     ("end", W, "결론 뒤에는 올 수 없다.")], steps=3,
    view=["However, there is the difference that the choice lies in their own hands."])
