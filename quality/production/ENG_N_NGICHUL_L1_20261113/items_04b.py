# Mini 모의고사 04회 ② 3-4-6 ~ 3-4-10  (generate_items.py가 exec)

# ───────── 3-4-6 언어로 동물을 깎아내리기 ─────────
c = "3-4-6"
mcq(c, "RDG-02", "D4", '밑줄 친 "linguistic castration"이 다음 글에서 의미하는 바로 가장 적절한 것은?',
    edit(text(c), ('"linguistic castration."', U('"linguistic castration."'))),
    ["teaching animals to understand basic human words",
     "using language to deny animals the abilities we claim for ourselves",
     "avoiding technical terms when describing animal behavior",
     "admitting that some animals are smarter than humans",
     "replacing scientific words with everyday expressions"],
    2, 3,
    [("teach_words", W, "동물에게 말을 가르치는 내용은 없다."),
     ("deny_abilities", S, "kissing을 mouth-to-mouth contact로 부르는 등 말로 동물의 능력을 깎아내려 인간의 우위를 지키는 것이다."),
     ("avoid_technical", S, "과학자들은 오히려 전문 용어를 써서 동물과 거리를 둔다고 했으므로 반대이다."),
     ("admit_smarter", S, "동물이 인간을 이겨도 본능으로 치부한다고 했으므로 반대이다."),
     ("everyday_words", M, "일상어를 전문어로 바꾸는 것이 문제라고 했으므로 방향이 반대이다.")], steps=2)

under(c, "GRM-01", "D3", (0, 3), ["downplay", "employing", "showing", "said", ("write it off", "write")],
      (3, "saying"), 3,
      [("verb_downplay", W, "명사절 주어 humans의 동사이다."),
       ("participle_employing", M, "앞 절을 보충하는 분사구문으로 Scientists가 '사용하는' 능동이다."),
       ("participle_showing", S, "evidence가 ~을 '보여 주는' 능동 관계이므로 showing이 맞다."),
       ("passive_said", S, "toolmaking이 인간을 정의한다고 '말해지는' 것이므로 수동 said(to define)여야 한다."),
       ("phrasal_write_off", W, "they write it off as ~: ~로 치부하다(대명사는 동사와 off 사이).")])

under(c, "RDG-03", "D4", (0, 5), ["downplay", ("to distance", "distance"), ("qualitatively different", "different"),
                                  "instinct", "disempower"],
      (0, "exaggerate"), 4,
      [("downplay_swap", S, "인간이 사다리 꼭대기를 지키려 동물과의 유사성을 '축소한다(downplay)'는 것이 글 전체이므로 exaggerate는 반대이다."),
       ("distance_ok", S, "전문 용어로 동물을 우리와 '멀어지게' 한다."),
       ("different_ok", M, "도구 제작을 인간의 것과 질적으로 '다른' 것으로 해석한다."),
       ("instinct_ok", S, "동물이 이겨도 지능이 아닌 '본능'으로 치부한다."),
       ("disempower_ok", W, "말로 동물의 힘을 '빼앗는다'는 결론이다.")], steps=3)

ordering(c, "D3", (0, 0), [(1, 2), (3, 3), (4, 5)], ["A", "C", "B"], 1, 4,
         [("acb", S, "과학자들의 전문 용어 사례 (A) → 동물의 우월한 능력도 본능으로 치부 (C) → 이를 linguistic castration이라 부른다 (B)."),
          ("bac", W, "(B)의 This and so many more tricks는 앞의 사례들 뒤에 와야 한다."),
          ("bca", W, "(B)가 맨 앞에 올 수 없다."),
          ("cab", S, "(C)의 they가 가리킬 Scientists가 (A)에서 먼저 나와야 한다."),
          ("cba", M, "(C)가 맨 앞이면 they의 지시 대상이 없다.")])

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("employing technical language to distance the other animals from us",
                   "employing technical language to ________________________")),
    ["make their findings easier for the public to read", "keep other animals at a distance from humans",
     "show how closely animals resemble humans", "prove that animals have no instincts at all",
     "describe animal behavior in a more emotional way"],
    2, 3,
    [("easier_public", M, "전문 용어는 오히려 일반인에게 어렵다."),
     ("keep_distance", S, "kissing → mouth-to-mouth contact처럼 말로 동물을 인간과 떼어 놓는다."),
     ("resemble", S, "유사성을 축소한다는 글의 요지와 반대이다."),
     ("no_instinct", W, "동물의 능력을 오히려 본능으로 치부한다고 했다."),
     ("emotional", W, "감정적 서술은 반대 방향이다.")])

# ───────── 3-4-7 자동화 시대의 중산층 ─────────
c = "3-4-7"
mcq(c, "RDG-01", "D3", "다음 글의 요지로 가장 적절한 것은?", text(c),
    ["Technological progress has always raised the incomes of the middle class.",
     "Workers should go to college so that machines cannot replace them.",
     "Automation, like early industrialization, has cut many workers off from progress.",
     "Early factories treated their workers more harshly than modern firms do.",
     "Men adjust to new technology more slowly than women usually do."],
    3, 2,
    [("progress_raises", M, "진보의 혜택을 누리지 못한다는 첫 문장과 반대이다."),
     ("go_college", S, "대학 없이도 중산층이 될 수 있던 길이 닫혔다는 언급을 대학 진학 권고로 비튼 오답이다."),
     ("automation_cutoff", S, "초기 산업화처럼 자동화가 중산층의 기회와 상향 이동을 막았다는 것이 요지이다."),
     ("harsh_factories", W, "두 시대의 대우를 비교하지 않는다."),
     ("men_slow", M, "패자가 주로 남성이라는 사실을 적응 속도의 성별 차이로 바꾼 오답이다.")])

under(c, "GRM-01", "D3", (2, 6), [("dried up", "dried"), "diminishing", "shifting", "dropped", "to attain"],
      (4, "attaining"), 3,
      [("verb_dried", W, "opportunity가 주어인 동사 dried up이다."),
       ("participle_diminishing", M, "opportunities를 꾸미는 '줄어드는' 현재분사이다."),
       ("by_gerund", M, "전치사 by의 목적어 자리의 동명사이다."),
       ("parallel_dropped", S, "have failed와 and로 병렬된 (have) dropped out이다."),
       ("allow_to", S, "allow + 목적어 + to-v 구조이므로 to attain이어야 한다.")])

under(c, "RDG-03", "D4", (1, 6), ["backwaters", "diminishing", "unwillingly", "primarily", "receded"],
      (2, "eagerly"), 5,
      [("backwaters_ok", M, "진보에서 '뒤처진 곳'에 남겨졌다는 비유이다."),
       ("diminishing_ok", W, "중산층의 기회가 '줄어들었다'."),
       ("unwillingly_swap", S, "어쩔 수 없이 더 낮은 임금의 일자리로 옮겨 간 피해자들이므로 eagerly(열심히)는 맞지 않는다."),
       ("primarily_ok", S, "패자는 '주로' 한창때의 남성이었다."),
       ("receded_ok", S, "제조업 일자리가 '줄어들자' 상향 이동의 길이 닫혔다는 인과이다.")], steps=2)

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("a path of upward mobility was closed", "________________________ was closed")),
    ["the chance to avoid going to college", "the door to automated factory work",
     "a way of reducing their working hours", "an opportunity to retire early",
     "a route to a higher social position"],
    5, 1,
    [("avoid_college", S, "대학 없이 중산층이 될 수 있었다는 앞 문장의 표면만 가져온 오답이다."),
     ("automated_work", M, "자동화된 일자리로 가는 문이 아니라 상향 이동의 길이 닫혔다."),
     ("reduce_hours", W, "근무 시간은 다루지 않는다."), ("retire_early", W, "조기 은퇴는 다루지 않는다."),
     ("upward_route", S, "원문 'a path of upward mobility'를 바꿔 쓴 것이다.")])

s7 = sents(c)
mcq(c, "RDG-05", "D3", None,
    " ".join(s7[:2] + ["①", s7[2], "②", s7[3],
                       "③ Some automated factories have become popular tourist sites that attract visitors from around the world.",
                       "④", s7[4], "⑤", s7[5], s7[6]]),
    NUMS, 3, 5,
    [("artisans", M, "초기 산업화와 자동화를 나란히 비교한다."), ("adjusted", M, "피해자들의 적응 방식을 설명한다."),
     ("tourist_drift", S, "automated를 쓰지만 중산층의 기회 상실이라는 논점과 무관하다."),
     ("men_losers", W, "패자의 특징으로 비교를 이어간다."),
     ("manufacturing", S, "상향 이동의 길이 닫힌 이유를 설명하는 배경이다.")])

# ───────── 3-4-8 포식자의 보수적 선택 ─────────
c = "3-4-8"
mcq(c, "RDG-01", "D3", "다음 글의 제목으로 가장 적절한 것은?", text(c),
    ["How Hawks Became the Fastest Hunters in the Sky", "Coral Snakes and King Snakes: Natural Enemies",
     "Eating Wild Mushrooms: A Tasty but Safe Choice", "Why Imperfect Mimics Survive: Predators Play It Safe",
     "Speed Matters More Than Caution in the Wild"],
    4, 5,
    [("fast_hawk", W, "매는 상상 속 예시일 뿐이다."), ("snake_enemies", M, "두 뱀의 관계가 아니라 포식자의 선택이 논점이다."),
     ("mushroom_safe", M, "버섯은 같은 논리의 예시이고, 확실하지 않으면 먹지 말라고 했다."),
     ("imperfect_mimic", S, "포식자가 안전한 쪽을 택하므로 킹스네이크가 완벽히 흉내 내지 않아도 된다."),
     ("speed_over_caution", S, "빨리 행동해야 한다는 앞부분만 보면 끌리지만, 결론은 생존을 위한 신중함이다.")])

under(c, "GRM-01", "D3", (2, 8), ["hesitate", ("might be gone", "gone"), "mistake", "to favor", ("to be a perfect", "to be")],
      (4, "being"), 2,
      [("if_present", W, "조건절의 현재 시제이다."),
       ("be_gone", S, "be gone(사라지다)의 과거분사 형용사이다."),
       ("if_present2", M, "조건절에서는 미래를 현재 시제로 쓴다."),
       ("shape_to", M, "shape A to-v: A가 ~하도록 만들다."),
       ("need_for_to", S, "there is no need for A to-v 구조이므로 to be여야 한다.")])

under(c, "RDG-03", "D4", (2, 8), ["quickly", ("a venomous", "venomous"), "obvious", "conservative", ("a perfect", "perfect")],
      (3, "risky"), 5,
      [("quickly_ok", M, "주저하면 먹이를 놓치므로 '빨리' 행동해야 한다."),
       ("venomous_ok", W, "목숨을 잃게 하는 것은 '독이 있는' 산호뱀이다."),
       ("obvious_ok", S, "먹이와 목숨 사이의 선택은 '분명하다'."),
       ("conservative_swap", S, "한 끼보다 장기적 생존을 택하는 '보수적인(신중한)' 선택이므로 risky는 반대이다."),
       ("perfect_ok", S, "포식자가 신중하므로 '완벽한' 모방자가 될 필요가 없다는 결론이다.")], steps=3)

mcq(c, "RDG-04", "D4", None,
    edit(text(c), ("there is no need for the king snake to be a perfect mimic of the coral snake's colors",
                   "the king snake ________________________")),
    ["must copy every detail of the coral snake's colors", "does not have to look exactly like the coral snake",
     "needs to become more venomous than the coral snake", "should hide from predators during the daytime",
     "has to move faster than any hawk can fly"],
    2, 1,
    [("copy_every", S, "포식자가 의심만 들어도 피하므로 완벽히 닮을 필요가 없다는 결론과 반대이다."),
     ("not_exact", S, "원문 'no need ... to be a perfect mimic'을 바꿔 쓴 것이다."),
     ("more_venom", S, "킹스네이크는 독이 없는 뱀이다."), ("hide_daytime", W, "숨는 행동은 언급되지 않는다."),
     ("faster", W, "속도 경쟁은 다루지 않는다.")], steps=3)

mcq(c, "RDG-09", "D3", None, text(c),
    ["hasty …… imperfect", "cautious …… flawless", "cautious …… imperfect", "hasty …… flawless", "random …… colorful"],
    3, 2,
    [("hasty_imperfect", M, "(B)는 맞지만 포식자는 생존을 위해 신중하게 고른다."),
     ("cautious_flawless", S, "(A)는 맞지만 완벽한 모방은 필요 없다고 했다."),
     ("cautious_imperfect", S, "실수 한 번이 목숨을 앗아 가므로 포식자는 신중하고, 그래서 불완전한 모방도 먹이를 지켜 준다."),
     ("hasty_flawless", W, "두 빈칸 모두 반대이다."), ("random_colorful", W, "두 빈칸 모두 글과 무관하다.")],
    view=["Because a single mistake can cost its life, a predator tends to make (A) ________ choices, which allows "
          "even a(n) (B) ________ imitation to protect its prey."])

# ───────── 3-4-9 문학 작품의 함축 ─────────
c = "3-4-9"
mcq(c, "RDG-01", "D3", "다음 글의 주제로 가장 적절한 것은?", text(c),
    ["the danger of reading too much into literary works", "why modern literature prefers direct statements",
     "the history of direct telling in literary works", "ways to write literary works that state ideas clearly",
     "the value of asking what a literary text implies"],
    5, 1,
    [("over_reading", S, "함축을 찾는 일을 경계하는 것이 아니라 권장한다."),
     ("modern_direct", M, "시대에 따라 직접 진술의 양이 다르다는 언급뿐이다."),
     ("history_telling", M, "직접 진술의 역사는 다루지 않는다."), ("write_clearly", W, "글쓰기 방법은 다루지 않는다."),
     ("ask_implication", S, "'텍스트가 무엇을 암시하는가'를 묻는 것이 해석의 출발이자 분석력을 기른다는 것이 주제이다.")])

under(c, "GRM-01", "D3", (1, 7), [("does not mean", "mean"), "Depending", "whatever", ("What a text implies", "What"),
                                  ("tests our", "tests")],
      (3, "That"), 5,
      [("does_mean", W, "does not + 동사원형이다."),
       ("participle_depending", M, "depending on: ~에 따라(관용적 분사구문)."),
       ("whatever_np", M, "whatever + 명사: 어떤 ~이든."),
       ("what_clause", S, "implies의 목적어가 빠진 불완전한 절이 주어이므로 선행사를 포함한 What이어야 한다."),
       ("singular_tests", S, "주어가 our work(단수)이므로 tests가 맞다(implications에 끌리지 않는다).")])

under(c, "RDG-03", "D4", (0, 4), ["imply", ("include direct statements", "direct"), "lesser", "always", "approach"],
      (1, "indirect"), 4,
      [("imply_ok", W, "문학은 '암시한다'는 일반화이다."),
       ("direct_swap", S, "however로 '그렇다고 문학에 직접적 진술이 없다는 뜻은 아니다'라고 해야 다음 문장(직접 진술이 많을 수도 있다)과 이어진다."),
       ("lesser_ok", S, "직접 진술이 많으면 암시는 '더 적다'."),
       ("always_ok", S, "어떤 비율이든 해석할 것이 '항상' 있다."),
       ("approach_ok", M, "해석에 '접근하는' 방법이다.")], steps=3)

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ("there is always something for readers to interpret", "________________________")),
    ["the writer's message is always stated directly", "the reader should focus on the direct statements",
     "readers always find something left to interpret", "older works contain more suggestion than newer ones",
     "the text can be understood without any analysis"],
    3, 2,
    [("stated_directly", M, "But으로 앞의 '직접 진술이 많을 수 있다'를 뒤집어야 한다."),
     ("focus_direct", S, "직접 진술을 언급한 앞 문장에 끌린 오답이다."),
     ("something_left", S, "원문을 바꿔 쓴 것으로 바로 뒤 'What does the text suggest?'와 이어진다."),
     ("older_more", M, "시대별 비교는 하지 않는다."), ("no_analysis", W, "분석력을 시험한다고 했으므로 반대이다.")])

mcq(c, "RDG-07", "D3", None,
    slots(c, [0, 2, 3, 4, 5, 6, 7], marks={2: "( ① )", 3: "( ② )", 4: "( ③ )", 5: "( ④ )", 6: "( ⑤ )"}),
    NUMS, 1, 2,
    [("after_s1", S, "This broad generalization이 첫 문장(문학은 암시한다)을 가리키고, 다음 문장(직접 진술이 많을 수도)으로 이어진다."),
     ("after_s3", S, "② 앞에서 이미 직접 진술의 양을 말했으므로 '그렇다고 직접 진술이 없다는 뜻은 아니다'는 늦다."),
     ("after_s4", M, "Thus 문장과 이어지지 않는다."), ("after_s5", W, "함축의 가치를 말하는 부분과 무관하다."),
     ("after_s6", W, "분석력 이야기 뒤에 일반화를 받는 문장이 올 수 없다.")], steps=2,
    view=["This broad generalization, however, does not mean that works of literature do not include direct statements."])

# ───────── 3-4-10 감각과 온도 ─────────
c = "3-4-10"
mcq(c, "RDG-08", "D3", None, text(c),
    ["우리는 흔히 온도를 물체를 만졌을 때의 느낌과 연관 짓는다.",
     "카펫은 타일보다 열에 의한 에너지 전달 속도가 더 빠르다.",
     "같은 온도의 타일과 카펫 중 타일이 더 차갑게 느껴진다.",
     "감각은 온도에 대한 정성적인 정보를 제공한다.",
     "온도계는 정량적인 측정을 위해 개발되었다."],
    2, 3,
    [("touch_temp", W, "첫 문장과 일치한다."),
     ("carpet_faster", S, "타일이 카펫보다 더 빠른 속도로 에너지를 전달한다고 했으므로 일치하지 않는다."),
     ("tile_colder", S, "예시와 일치한다."), ("qualitative", M, "2문장과 일치한다."),
     ("thermometer", M, "마지막 문장과 일치한다.")])

under(c, "GRM-01", "D3", (2, 6), ["mislead", "feels", "even though", ("than carpet does", "does"), ("What we need", "What")],
      (3, "is"), 5,
      [("verb_mislead", W, "are와 and로 병렬된 동사이다."),
       ("singular_feels", M, "주어 the tile(단수)의 동사이다."),
       ("conj_even_though", M, "절을 이끄는 접속사이다."),
       ("pro_verb_does", S, "앞의 일반동사 transfers를 대신하므로 does여야 한다."),
       ("what_clause", S, "need의 목적어가 빠진 불완전한 절을 이끄는 What이 맞다.")])

under(c, "RDG-03", "D4", (1, 6), ["qualitative", "unreliable", "colder", "higher", "actual"],
      (2, "warmer"), 4,
      [("qualitative_ok", M, "느낌은 '정성적' 지표이다."), ("unreliable_ok", S, "감각은 '믿을 수 없고' 우리를 속인다."),
       ("colder_swap", S, "타일이 에너지를 더 빨리 빼앗아 가므로 '더 차갑게' 느껴져야 한다."),
       ("higher_ok", S, "타일이 '더 높은' 비율로 에너지를 전달한다."),
       ("actual_ok", W, "피부는 '실제' 온도가 아니라 전달률을 잰다.")], steps=3)

mcq(c, "RDG-04", "D3", None,
    edit(text(c), ('Your skin "measures" the rate of energy transfer by heat rather than the actual temperature.',
                   'Your skin "measures" ________________________ rather than the actual temperature.')),
    ["how fast energy is transferred by heat", "how long an object has been touched", "how much an object weighs",
     "the color and texture of the surface", "the average temperature of the room"],
    1, 5,
    [("transfer_rate", S, "원문 'the rate of energy transfer by heat'를 바꿔 쓴 것이다."),
     ("touch_time", M, "접촉 시간은 다루지 않는다."), ("weight", W, "무게는 무관하다."),
     ("texture", M, "타일과 카펫의 재질 차이에 끌린 오답으로, 피부가 재는 것은 재질이 아니다."),
     ("room_temp", S, "온도라는 표면어에 끌린 오답이다.")])

ordering(c, "D3", (0, 1), [(2, 3), (4, 5), (6, 7)], ["B", "A", "C"], 2, 3,
         [("acb", W, "(A)의 The two objects는 타일과 카펫이 소개된 (B) 뒤에 와야 한다."),
          ("bac", S, "감각은 믿을 수 없다·타일 예시 (B) → 두 물체가 다르게 느껴지는 이유 (A) → 그래서 믿을 만한 측정법(온도계) (C)."),
          ("bca", S, "(A)의 설명 없이 (C)의 'rather than the rate of energy transfer'가 먼저 나올 수 없다."),
          ("cab", M, "(C)가 맨 앞이면 '전달률'이 설명 없이 나온다."), ("cba", W, "흐름이 거꾸로이다.")])
