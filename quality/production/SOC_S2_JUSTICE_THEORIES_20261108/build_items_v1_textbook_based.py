#!/usr/bin/env python3
"""SOC S2 20-item bundle (천재 통합사회2 II-2 자유주의와 공동체주의 정의관, pp.44-49).
Thinker positions are limited to what the textbook pages state (claim-fidelity gate): no extreme corollaries."""
import yaml, pathlib, collections

ROOT = pathlib.Path('/home/user/ARC-System')
OUT = ROOT / 'quality/production/SOC_S2_JUSTICE_THEORIES_20261108'
OUT.mkdir(parents=True, exist_ok=True)
SRC = 'SOC-TB-CHUNJAE-2-P44-49'
TARGET_POS = [3, 5, 2, 4, 1, 3, 2, 4, 5, 2, 3, 1, 3, 4, 5, 4, 1, 5, 2, 1]
DIFF = {n: 'D2' for n in range(1, 5)}
DIFF.update({n: 'D3' for n in range(5, 15)})
DIFF.update({n: 'D4' for n in range(15, 21)})
ITEMS = []


def D(text, claim, c, why, v=False, page='p.45'):
    return dict(text=text, claim=claim, c=c, why=why, v=v, ev=[f'{SRC}:{page}'])


def item(no, fam, cov, stem, correct, distractors, second, steps, elim, view=None, table=None, key_v=True):
    base = [correct] + distractors
    pos = TARGET_POS[no - 1]
    final = list(range(1, 5))[: pos - 1] + [0] + list(range(1, 5))[pos - 1:]
    judg = []
    for i in final:
        b = base[i]
        judg.append(dict(v=(b['v'] if i else key_v), c='CORRECT' if i == 0 else b['c'], axis='application', claim=b['claim'],
                         ev=b['ev'], why=b['why']))
    it = dict(item_id=f'SOC-S2-{no:03d}', format='MCQ', family=fam, coverage=cov, difficulty=DIFF[no],
              balance='ADVANCED_DISCRIMINATION' if DIFF[no] == 'D4' else 'CORE_EXAM_POINT', stem=stem,
              options=[base[i]['text'] for i in final], answer=pos, second_best=final.index(second + 1) + 1,
              judgments=judg, reasoning_steps=steps, immediate_elimination=elim)
    if view: it['view'] = view
    if table: it['table'] = table
    ITEMS.append(it)


def item_rows(no, fam, cov, stem, header, rows, wrong, why, pages, strengths, steps, elim, second):
    labels = ['㉠', '㉡', '㉢', '㉣', '㉤']
    assert TARGET_POS[no - 1] == wrong + 1, (no, wrong)
    judg = [dict(v=(i != wrong), c='CORRECT' if i == wrong else strengths[i], axis='application', claim=f'row_{labels[i]}',
                 ev=[f'{SRC}:{pages[i]}'], why=why[i]) for i in range(5)]
    ITEMS.append(dict(item_id=f'SOC-S2-{no:03d}', format='MCQ', family=fam, coverage=cov, difficulty=DIFF[no],
                      balance='ADVANCED_DISCRIMINATION' if DIFF[no] == 'D4' else 'CORE_EXAM_POINT', stem=stem, options=labels,
                      answer=wrong + 1, second_best=second + 1, judgments=judg, reasoning_steps=steps, immediate_elimination=elim,
                      table=dict(header=['구분'] + header, rows=[[labels[i]] + rows[i] for i in range(5)])))


# ============================================================ D2 (4)
item(1, 'KEY_WORD_FUNCTION', 'LIBERAL_FEATURES', "자유주의적 정의관에 대한 설명으로 옳은 것은?",
     D("자유와 권리를 최대한 누리며 개인선을 실현하는 것을 정의롭다고 본다.", "liberal_def", '', "자유주의는 개인의 자유와 권리를 최대한 누리며 개인선을 실현하는 것을 정의롭다고 여긴다.", True, 'p.45'),
     [D("공동체의 공동선이 개인선보다 먼저 추구되어야 한다고 본다.", "common_first", 'STRONG', "공동선 우선은 공동체주의의 입장이다.", False, 'p.46'),
      D("인간은 공동체에서 부여한 역할로 자아 정체성을 형성한다고 본다.", "role_identity", 'MEDIUM', "역할로 정체성을 형성한다는 것은 공동체주의의 입장이다.", False, 'p.46'),
      D("공동체의 덕목을 실천하며 공동선을 실현하는 것을 정의롭다고 본다.", "virtue_common", 'MEDIUM', "공동체주의의 정의 개념이다.", False, 'p.46'),
      D("개인의 권리보다 공동체에 대한 의무를 우선한다고 본다.", "duty_first", 'WEAK', "자유주의는 개인의 권리를 중시한다.", False, 'p.45')],
     second=0, steps=1, elim=2)

item(2, 'KEY_WORD_FUNCTION', 'COMMUNITARIAN_FEATURES', "공동체주의적 정의관에 대한 설명으로 옳은 것은?",
     D("공동체와 분리되어 독립적으로 존재하는 개인은 있을 수 없다고 본다.", "no_independent", '', "공동체주의는 공동체와 분리되어 독립적으로 존재하는 개인은 있을 수 없다고 본다.", True, 'p.46'),
     [D("국가는 중립적 입장에서 개인의 자유로운 삶을 최대한 허용해야 한다고 본다.", "neutral_state", 'STRONG', "국가의 중립성은 자유주의의 입장이다.", False, 'p.45'),
      D("개인선이 공동선보다 우선한다고 본다.", "individual_first", 'MEDIUM', "개인선 우선은 자유주의의 입장이다.", False, 'p.45'),
      D("인간은 합리적 이성에 따라 선택한 삶의 목적을 향해 살아가는 독립적 존재라고 본다.", "rational_independent", 'MEDIUM', "독립적 존재라는 인간관은 자유주의의 입장이다.", False, 'p.45'),
      D("자아 정체성은 공동체가 부여한 역할보다 개인의 선택으로 이루어진다고 본다.", "choice_identity", 'WEAK', "선택으로 이루어지는 정체성은 자유주의의 입장이다.", False, 'p.45')],
     second=0, steps=1, elim=2)

item(3, 'COMPARISON_MATRIX', 'THEORY_MATCHING', "<보기>의 (가), (나)에 해당하는 정의관을 옳게 짝지은 것은?",
     D("(가) 자유주의적 정의관, (나) 공동체주의적 정의관", "lib_com", '', "(가)는 개인선과 개인의 권리를, (나)는 공동선과 구성원의 역할·의무를 강조한다.", True, 'p.45'),
     [D("(가) 공동체주의적 정의관, (나) 자유주의적 정의관", "com_lib", 'STRONG', "두 정의관이 서로 바뀌었다.", False, 'p.45'),
      D("(가) 자유주의적 정의관, (나) 자유주의적 정의관", "lib_lib", 'WEAK', "(나)는 공동체주의이다.", False, 'p.46'),
      D("(가) 공동체주의적 정의관, (나) 공동체주의적 정의관", "com_com", 'WEAK', "(가)는 자유주의이다.", False, 'p.45'),
      D("(가) 공동체주의적 정의관, (나) 정의관을 판단할 수 없음", "unknown", 'WEAK', "두 설명 모두 정의관을 판단할 수 있다.", False, 'p.45')],
     second=0, steps=1, elim=2,
     view=["(가) 개인의 자유와 권리를 보호하는 것이 우선이며, 개인선이 공동선보다 앞선다.",
           "(나) 구성원이 유대감을 바탕으로 역할과 의무를 다하며 공동선을 실현해야 한다."])

item(4, 'KEY_WORD_FUNCTION', 'RAWLS_PRINCIPLES', "롤스가 제시한 정의의 원칙 (가)~(다)를 이름과 옳게 연결한 것은?",
     D("(가) 평등한 자유의 원칙, (나) 차등의 원칙, (다) 기회균등의 원칙", "eq_diff_opp", '', "(가)는 평등한 자유, (나)는 최소 수혜자에게 최대 이익이 되는 차등, (다)는 직책과 지위의 개방인 기회균등이다.", True, 'p.47'),
     [D("(가) 차등의 원칙, (나) 평등한 자유의 원칙, (다) 기회균등의 원칙", "diff_eq_opp", 'STRONG', "(가)와 (나)의 이름이 바뀌었다.", False, 'p.47'),
      D("(가) 평등한 자유의 원칙, (나) 기회균등의 원칙, (다) 차등의 원칙", "eq_opp_diff", 'STRONG', "(나)와 (다)의 이름이 바뀌었다.", False, 'p.47'),
      D("(가) 기회균등의 원칙, (나) 차등의 원칙, (다) 평등한 자유의 원칙", "opp_diff_eq", 'MEDIUM', "(가)와 (다)의 이름이 바뀌었다.", False, 'p.47'),
      D("(가) 차등의 원칙, (나) 기회균등의 원칙, (다) 평등한 자유의 원칙", "diff_opp_eq", 'WEAK', "세 원칙 모두 잘못 연결했다.", False, 'p.47')],
     second=0, steps=1, elim=2,
     view=["(가) 모든 사람은 동등한 기본적 자유를 최대한 누려야 한다.",
           "(나) 사회적·경제적 불평등은 사회에서 가장 불리한 처지에 있는 최소 수혜자에게 최대의 이익이 되어야 한다.",
           "(다) 불평등의 계기가 되는 직책이나 지위는 모든 사람에게 개방되어야 한다."])

# ============================================================ D3 (10)
item(5, 'STUDENT_RESPONSE_EVALUATION', 'ANCESTOR_RESPONSIBILITY', "조상이 노예를 소유했던 잘못에 대해 후손이 사과하거나 배상할 책임이 있는지를 두고, <보기>의 학생 A~C가 두 정의관의 입장을 설명하였다. 적절한 것만을 고른 것은?",
     D("A, B", "ab", '', "자유주의는 조상의 행위와 후손은 무관하다고 보고, 공동체주의는 후손이 공동체의 역사와 책무를 물려받는다고 본다.", True, 'p.45'),
     [D("A", "only_a", 'STRONG', "B의 설명도 적절하다.", False, 'p.46'),
      D("B", "only_b", 'STRONG', "A의 설명도 적절하다.", False, 'p.45'),
      D("A, C", "ac", 'MEDIUM', "C는 자유주의의 입장을 반대로 설명했다.", False, 'p.45'),
      D("B, C", "bc", 'MEDIUM', "C가 부적절하다.", False, 'p.45')],
     second=0, steps=2, elim=1,
     view=["학생 A: 자유주의적 정의관은 조상이 한 행위와 후손은 무관하므로 후손에게 사과나 배상의 책임이 없다고 볼 거야.",
           "학생 B: 공동체주의적 정의관은 후손의 정체성이 공동체와 분리될 수 없고 사회적 책무를 공동체의 역사에서 물려받는다고 볼 거야.",
           "학생 C: 자유주의적 정의관은 후손이 같은 공동체의 구성원이므로 조상의 책임을 물려받는다고 볼 거야."])

item(6, 'MULTI_JUDGMENT', 'RAWLS_NOZICK_COMPARE', "롤스와 노직의 정의관을 비교한 <보기>의 설명 중 옳은 것만을 있는 대로 고른 것은?",
     D("ㄱ, ㄴ", "gn", '', "두 사람 모두 개인의 자유와 권리를 보호하는 것을 정의로 보며, 노직은 최소 수혜자에게 최대 이익을 보장해야 한다는 말에 동의하기 어렵다고 본다.", True, 'p.47'),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다.", False, 'p.47'),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 옳다.", False, 'p.47'),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "노직은 정당한 취득과 양도가 지켜지면 빈부 격차가 문제 되지 않는다고 보므로 ㄷ이 틀리다.", False, 'p.47'),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ이 틀리다.", False, 'p.47')],
     second=0, steps=2, elim=1,
     view=["ㄱ. 롤스와 노직은 모두 개인의 자유와 권리를 보호하고 존중하는 것을 정의와 연결한다.",
           "ㄴ. 롤스는 최소 수혜자에게 최대 이익을 보장해야 한다고 보지만, 노직은 이에 동의하기 어렵다고 본다.",
           "ㄷ. 노직은 정당한 취득과 양도의 결과로 빈부 격차가 생기면 그 격차를 반드시 해소해야 한다고 본다."])

item(7, 'MULTI_JUDGMENT', 'NOZICK_CASE', "다음 사례에 대해 노직의 입장에서 판단한 <보기>의 내용 중 옳은 것만을 있는 대로 고른 것은?\n갑은 타인에게 피해를 주지 않고 정당하게 땅을 취득한 뒤, 이를 자신의 뜻에 따라 을에게 팔았다. 이후 갑과 을 사이의 재산 차이가 크게 벌어졌다.",
     D("ㄱ, ㄴ", "gn", '', "정당한 취득과 양도가 지켜졌으므로 소유 권리가 인정되고, 그 결과로 생긴 빈부 격차는 문제가 되지 않는다.", True, 'p.47'),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다.", False, 'p.47'),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 옳다.", False, 'p.47'),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "ㄷ은 노직의 입장과 어긋나므로 틀리다.", False, 'p.47'),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ이 틀리다.", False, 'p.47')],
     second=0, steps=2, elim=1,
     view=["ㄱ. 갑이 땅을 정당하게 취득했으므로 그 땅에 대한 소유 권리를 가진다.",
           "ㄴ. 취득의 원칙과 양도의 원칙이 지켜졌다면 재산 차이가 커졌다는 점만으로는 문제가 되지 않는다.",
           "ㄷ. 재산 차이가 크므로 갑의 소유물 일부를 거두어 최소 수혜자에게 주는 것이 정의의 요구이다."])

item(8, 'MULTI_JUDGMENT', 'RAWLS_POLICY_CASE', "롤스의 정의의 원칙에 비추어 <보기>의 정책 (가)~(다)에 대해 판단한 내용으로 옳은 것만을 있는 대로 고른 것은?",
     D("ㄱ, ㄴ", "gn", '', "(가)는 최소 수혜자의 처지가 가장 크게 개선되어 차등의 원칙에 부합하고, (나)는 최소 수혜자의 처지가 나빠져 차등의 원칙에 어긋난다.", True, 'p.47'),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다.", False, 'p.47'),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 옳다.", False, 'p.47'),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "(다)는 직책의 개방을 막아 기회균등의 원칙에 어긋나므로 ㄷ(부합한다)이 틀리다.", False, 'p.47'),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "ㄷ이 틀리다.", False, 'p.47')],
     second=0, steps=2, elim=1,
     view=["(가) 높은 보상을 받는 직업을 두되, 그 제도로 사회에서 가장 불리한 처지에 있는 사람들의 처지가 가장 크게 개선된다.",
           "(나) 사회 전체의 평균 소득은 오르지만 가장 불리한 처지에 있는 사람들의 처지는 나빠진다.",
           "(다) 높은 지위의 직책 지원 자격을 특정 집단의 사람에게만 준다.",
           "ㄱ. (가)는 차등의 원칙에 부합한다.  ㄴ. (나)는 차등의 원칙에 어긋난다.  ㄷ. (다)는 기회균등의 원칙에 부합한다."])

item(9, 'MULTI_JUDGMENT', 'MILL_FREEDOM_CASE', "밀의 입장에서 <보기>의 사례를 설명한 내용으로 옳은 것만을 있는 대로 고른 것은?",
     D("ㄱ, ㄷ", "gd", '', "밀은 타인에게 영향을 미치지 않는 행위에 대해서는 개인의 절대적 자유를 주장하므로, (가)는 간섭할 영역이 아니고 이 기준은 (나)에는 그대로 적용되지 않는다.", True, 'p.45'),
     [D("ㄱ", "only_g", 'STRONG', "ㄷ도 옳다.", False, 'p.45'),
      D("ㄷ", "only_d", 'STRONG', "ㄱ도 옳다.", False, 'p.45'),
      D("ㄱ, ㄴ", "gn", 'MEDIUM', "ㄴ은 타인에게 영향을 주는 (나)에까지 절대적 자유를 인정하므로 틀리다.", False, 'p.45'),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄴ이 틀리다.", False, 'p.45')],
     second=0, steps=2, elim=1,
     view=["(가) 혼자 있는 집에서 자신의 취향에 맞는 방식으로 하루를 보내는 행위",
           "(나) 늦은 밤 이웃에게 큰 소음 피해를 주는 방식으로 노래를 부르는 행위",
           "ㄱ. 밀은 (가)에 대해 타인이나 사회가 간섭하지 않아야 한다고 볼 것이다.",
           "ㄴ. 밀은 (나)에 대해서도 (가)와 같이 개인의 절대적 자유가 인정된다고 볼 것이다.",
           "ㄷ. 밀이 말한 절대적 자유는 타인에게 영향을 미치지 않는 행위를 기준으로 한다."])

item(10, 'MULTI_JUDGMENT', 'MACINTYRE_VIEW', "매킨타이어의 입장에서 <보기>를 설명한 내용으로 옳은 것만을 있는 대로 고른 것은?\n나는 가족, 도시, 민족, 국가 등 다양한 공동체의 구성원이다. 나는 그 공동체들로부터 다양한 빚과 유산, 적절한 기대와 의무를 물려받는다.",
     D("ㄱ, ㄴ", "gn", '', "인간은 공동체와 분리된 존재가 아니며 공동체로부터 의무를 물려받는 것이 도덕의 출발점이다.", True, 'p.47'),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다.", False, 'p.47'),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 옳다.", False, 'p.47'),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "자유롭고 독립적인 인간관을 따르는 것은 자유주의이므로 ㄷ이 틀리다.", False, 'p.46'),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "ㄷ이 틀리다.", False, 'p.46')],
     second=0, steps=2, elim=1,
     view=["ㄱ. 인간은 공동체와 분리되어 존재하는 것이 아니라 공동체의 구성원으로 살아간다.",
           "ㄴ. 공동체로부터 물려받은 빚과 의무는 도덕의 출발점이 된다.",
           "ㄷ. 현대 사회의 분열은 인간을 공동체에 뿌리를 둔 존재로 보는 데서 비롯한다."])

item(11, 'MULTI_JUDGMENT', 'GREENBELT_CASE', "다음 사례에 대한 <보기>의 설명 중 옳은 것만을 있는 대로 고른 것은?\nA시는 도심의 녹지를 보존하기 위해 일부 사유지의 개발을 제한하기로 하였다. 다수의 시민은 녹지의 혜택을 누리지만, 해당 토지 소유자는 재산권 행사에 제약을 받게 되었다.",
     D("ㄱ, ㄴ", "gn", '', "자유주의는 소유자의 권리와 사익 침해를, 공동체주의는 환경을 보호할 구성원의 의무를 근거로 든다.", True, 'p.48'),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다.", False, 'p.48'),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 옳다.", False, 'p.48'),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "ㄷ은 두 정의관이 반드시 양립할 수 없다고 하므로 틀리다.", False, 'p.48'),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ이 틀리다.", False, 'p.48')],
     second=0, steps=2, elim=1,
     view=["ㄱ. 자유주의적 정의관은 이 정책이 토지 소유자의 권리와 사익을 부당하게 침해할 수 있다고 볼 것이다.",
           "ㄴ. 공동체주의적 정의관은 구성원이 공동체의 환경을 보호할 의무가 있으므로 정책이 필요하다고 볼 것이다.",
           "ㄷ. 두 정의관은 서로 대립하므로 어떤 경우에도 함께 고려할 수 없다."])

item(12, 'MULTI_JUDGMENT', 'NIMBY_CASE', "쓰레기 소각장 신설에 대해 주민들이 건강권과 재산권 침해를 이유로 반대하는 님비(NIMBY) 현상을 두고, <보기>의 설명 중 옳은 것만을 있는 대로 고른 것은?",
     D("ㄱ, ㄴ", "gn", '', "님비는 자신이 사는 지역에 혐오 시설이 들어서는 것을 강하게 반대하는 현상이고, 공동체주의는 공동선과 구성원의 책임을 강조한다.", True, 'p.46'),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다.", False, 'p.46'),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 옳다.", False, 'p.46'),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "ㄷ은 공동체주의가 사익만 인정한다는 뜻이라 틀리다.", False, 'p.46'),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ이 틀리다.", False, 'p.46')],
     second=0, steps=2, elim=1,
     view=["ㄱ. 님비 현상은 위험 시설이나 혐오 시설이 자신이 사는 지역에 들어서는 것을 강하게 반대하는 현상이다.",
           "ㄴ. 공동체주의적 정의관은 공동선을 앞세워 구성원이 공동체에 대한 책임을 나누어야 한다고 볼 것이다.",
           "ㄷ. 공동체주의적 정의관은 공동체 구성원의 사익을 어떤 경우에도 인정하지 않는다고 볼 것이다."])

item(13, 'MULTI_JUDGMENT', 'RIGHTS_DUTIES_HARMONY', "권리와 의무, 사익과 공익의 관계에 대한 <보기>의 설명 중 옳은 것만을 있는 대로 고른 것은?",
     D("ㄱ, ㄴ", "gn", '', "자신의 권리만 내세우며 의무를 회피하면 누구도 권리를 누리지 못하고, 공익을 고려하지 않고 사익만 내세우면 공동체가 파괴된다.", True, 'p.48'),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다.", False, 'p.48'),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 옳다.", False, 'p.48'),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ은 공익만 강조하면 개인의 권리를 침해한다고 한 내용과 어긋나므로 틀리다.", False, 'p.48'),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "ㄷ이 틀리다.", False, 'p.48')],
     second=0, steps=2, elim=1,
     view=["ㄱ. 자신의 권리만 내세우고 책임이나 의무를 회피하면 누구도 자신의 권리조차 누릴 수 없다.",
           "ㄴ. 공익을 고려하지 않고 사익만 내세우면 공동체가 파괴되어 개인의 이익마저 보장받지 못한다.",
           "ㄷ. 개인의 권리와 사익은 공익을 위해서라면 언제나 제한해야 한다."])

item_rows(14, 'COMPARISON_MATRIX', 'THEORY_TABLE', "<보기>의 표에서 ㉠~㉤ 중 옳지 않은 것은?",
          ["항목", "자유주의적 정의관", "공동체주의적 정의관"],
          [["인간관", "합리적 이성에 따라 스스로 선택한 삶의 목적을 향해 살아가는 독립적 존재", "특정 공동체의 구성원으로서 공동체의 덕목을 실천하며 살아가는 존재"],
           ["우선하는 가치", "개인선", "공동선"],
           ["공동체·국가의 의미", "개인의 자유와 권리를 보호하고 증진하는 수단", "좋은 삶을 살아가는 데 중요한 기반"],
           ["자아 정체성", "공동체가 부여한 역할로 형성된다고 봄", "개인의 선택으로 형성된다고 봄"],
           ["정의로운 상태", "개인이 자유와 권리를 최대한 누리며 개인선을 실현하는 것", "구성원이 유대감을 바탕으로 역할과 의무를 다하며 공동선을 실현하는 것"]],
          wrong=3,
          why=["자유주의의 독립적 인간관과 공동체주의의 구성원 인간관이 맞다.", "자유주의는 개인선, 공동체주의는 공동선을 우선한다.",
               "자유주의는 공동체를 수단으로, 공동체주의는 기반으로 본다.", "자유주의는 선택으로, 공동체주의는 사회적 역할로 정체성이 형성된다고 보므로 서술이 서로 바뀌었다.",
               "각 정의관이 정의롭다고 여기는 상태가 맞다."],
          pages=['p.45', 'p.45', 'p.46', 'p.45', 'p.45'], strengths=['MEDIUM', 'WEAK', 'STRONG', '', 'MEDIUM'], steps=2, elim=2, second=2)

# ============================================================ D4 (6)
item(15, 'COMPARISON_MATRIX', 'CROSS_THINKER_CASE', "A시가 시립 도서관 건립 비용을 마련하는 방법을 두고 주민 갑~병이 <보기>와 같이 말하였다. 갑~병의 발언과 가장 가까운 사상가를 옳게 짝지은 것은?",
     D("갑: 노직, 을: 롤스, 병: 매킨타이어", "no_ro_ma", '', "갑은 정당한 소유물의 사용을 개인의 선택에 맡기는 노직, 을은 최소 수혜자의 이익을 기준으로 삼는 롤스, 병은 공동체 구성원의 책무를 말하는 매킨타이어와 가깝다.", True, 'p.47'),
     [D("갑: 밀, 을: 롤스, 병: 매킨타이어", "mi_ro_ma", 'STRONG', "갑의 발언은 정당하게 얻은 소유물의 사용에 관한 것이라 밀의 타인에게 영향 없는 행위의 자유보다 노직의 소유 권리에 가깝다.", False, 'p.47'),
      D("갑: 노직, 을: 매킨타이어, 병: 롤스", "no_ma_ro", 'STRONG', "을은 최소 수혜자 이익을 기준으로 하므로 롤스이고, 병은 공동체의 책무를 말하므로 매킨타이어이다.", False, 'p.47'),
      D("갑: 롤스, 을: 노직, 병: 매킨타이어", "ro_no_ma", 'MEDIUM', "갑과 을이 서로 바뀌었다.", False, 'p.47'),
      D("갑: 노직, 을: 롤스, 병: 밀", "no_ro_mi", 'MEDIUM', "병의 발언은 공동체 구성원의 책무를 말하므로 밀이 아니라 매킨타이어와 가깝다.", False, 'p.45')],
     second=0, steps=4, elim=1,
     view=["갑: 내가 정당하게 번 소득을 도서관 건립에 쓸지는 내가 정할 일입니다. 강제로 걷는 것은 옳지 않습니다.",
           "을: 사회에서 가장 불리한 처지에 있는 주민이 도서관에서 가장 큰 이익을 얻는 방식이라면 부담에 차이를 두어도 됩니다.",
           "병: 우리는 같은 도시의 구성원으로서 물려받은 공동체의 터전을 가꿀 책임을 서로 나누어야 합니다."])

item(16, 'COMPARISON_MATRIX', 'ONE_CASE_FOUR_VOICES', "하천 정비 비용 분담에 대한 주민 (가)~(라)의 발언 <보기>에 대한 설명으로 옳은 것은?",
     D("(가)는 소유 권리를, (다)는 최소 수혜자의 이익을 근거로 든다.", "g_no_d_ro", '', "(가)는 정당하게 얻은 재산의 사용은 자신이 정한다는 소유 권리를, (다)는 가장 어려운 사람이 가장 큰 도움을 받도록 한다는 차등의 원칙을 근거로 든다.", True, 'p.47'),
     [D("(나)는 공동체주의, (다)는 노직처럼 소유 권리를 근거로 든다.", "n_com_d_no", 'STRONG', "(다)는 소유 권리가 아니라 최소 수혜자 이익을 근거로 든다.", False, 'p.47'),
      D("(가)와 (라)는 모두 개인선이 공동선보다 우선한다는 입장이다.", "g_r_individual", 'STRONG', "(라)는 모두에게 이익이 되는 공동체의 선을 근거로 든다.", False, 'p.45'),
      D("(나)와 (다)는 모두 공동체주의적 정의관의 입장이다.", "n_d_com", 'MEDIUM', "(다)는 롤스처럼 자유주의적 정의관에 속한다.", False, 'p.47'),
      D("(가)와 (다)는 모두 소유 권리를 근거로 한 노직의 입장과 같다.", "g_d_no", 'MEDIUM', "(다)는 노직이 동의하기 어렵다고 한 최소 수혜자 이익 기준을 따른다.", False, 'p.47')],
     second=0, steps=4, elim=1,
     view=["(가) 토지 소유 주민: 정비로 이익을 보지 않는 내게 비용을 매기는 것은 재산권 침해입니다. 정당하게 얻은 내 재산의 사용은 내가 정합니다.",
           "(나) 이장: 우리는 이 마을의 구성원으로서 물려받은 터전을 가꿀 책임이 있습니다. 모두가 함께 부담하는 것이 도리입니다.",
           "(다) 청년: 자신의 형편을 모른다고 가정하고 정합시다. 가장 어려운 주민이 가장 큰 도움을 받도록 부담에 차이를 둡시다.",
           "(라) 상점 주인: 모두에게 이익이 되는 일이니 모두가 같은 금액을 내는 것이 공동체의 선을 위한 길입니다."])

item(17, 'STUDENT_RESPONSE_EVALUATION', 'HALF_TRUE_STUDENTS', "자유주의와 공동체주의에 대한 학생 A~D의 발언 중 옳은 것만을 고른 것은?",
     D("A, C", "ac", '', "A와 C는 두 정의관을 정확히 설명했고, B와 D는 각각 한 부분이 틀렸다.", True, 'p.45'),
     [D("A", "only_a", 'STRONG', "C의 설명도 옳다.", False, 'p.46'),
      D("C", "only_c", 'STRONG', "A의 설명도 옳다.", False, 'p.45'),
      D("A, B", "ab", 'MEDIUM', "B는 공동체주의가 공동체를 수단으로만 본다고 하여 틀렸다.", False, 'p.46'),
      D("C, D", "cd", 'MEDIUM', "D는 공동체주의가 정체성을 선택으로만 형성된다고 본다고 하여 틀렸다.", False, 'p.46')],
     second=0, steps=4, elim=1,
     view=["학생 A: 자유주의는 개인선이 공동선보다 앞선다고 보고, 국가가 중립적 입장에서 개인의 자유로운 삶을 최대한 허용해야 한다고 봐.",
           "학생 B: 공동체주의는 공동체를 개인의 자유와 권리를 보호하는 수단으로만 보고, 개인선보다 공동선을 앞세워.",
           "학생 C: 조상의 잘못에 대해 자유주의는 후손의 배상 책임을 인정하지 않고, 공동체주의는 후손이 공동체의 역사와 책무를 물려받는다고 봐.",
           "학생 D: 공동체주의는 자아 정체성이 사회적 역할과 무관하게 개인의 선택으로만 이루어진다고 봐."])

# Q18: Rawls table with a policy that violates exactly one principle (fixed ㉠~㉤ options)
item_rows(18, 'COMPARISON_MATRIX', 'RAWLS_POLICY_TABLE', "<보기>의 표에서 ㉠~㉤ 중 롤스의 정의의 원칙에 비추어 판단이 옳지 않은 것은?",
          ["정책 내용", "판단"],
          [["모든 시민에게 동등한 투표권을 보장한다.", "평등한 자유의 원칙에 부합한다."],
           ["일부 집단의 투표권을 제한하는 대신 사회 전체의 복지를 높인다.", "평등한 자유의 원칙에 어긋난다."],
           ["불평등한 보상을 허용하되 최소 수혜자의 처지가 가장 크게 개선된다.", "차등의 원칙에 부합한다."],
           ["높은 지위의 직책을 지원할 자격을 모든 사람에게 개방한다.", "기회균등의 원칙에 부합한다."],
           ["평균 소득을 높이지만 최소 수혜자의 처지가 나빠진다.", "차등의 원칙에 부합한다."]],
          wrong=4,
          why=["동등한 기본적 자유를 보장하므로 평등한 자유의 원칙에 부합한다.", "사회 전체의 복지를 이유로도 기본적 권리는 침해될 수 없다는 롤스의 입장에서 어긋난다.",
               "최소 수혜자에게 최대 이익이 되는 불평등이므로 차등의 원칙에 부합한다.", "직책과 지위가 모든 사람에게 개방되므로 기회균등의 원칙에 부합한다.",
               "최소 수혜자의 처지가 나빠지므로 차등의 원칙에 어긋난다."],
          pages=['p.47'] * 5, strengths=['MEDIUM', 'STRONG', 'STRONG', 'MEDIUM', ''], steps=4, elim=2, second=1)
ITEMS[-1]['family'] = 'COMPARISON_MATRIX'

item(19, 'MULTI_JUDGMENT', 'COMPLEMENTARY_SOLUTION', "개발 제한 구역 지정으로 토지 소유자가 재산권 행사에 제약을 받는 갈등에 대해 <보기>의 해결 방안 (가)~(다)를 평가한 내용으로 옳은 것만을 있는 대로 고른 것은?",
     D("ㄱ, ㄴ", "gn", '', "(가)는 소유자의 권리를 인정하면서 공동체의 환경도 지키는 보완적 방안이고, (나)는 공동선만 강조해 개인의 권리를 침해한다.", True, 'p.48'),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다.", False, 'p.48'),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 옳다.", False, 'p.48'),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ은 개인선만 강조해 공동체의 환경을 해치므로 보완적이라는 평가가 틀리다.", False, 'p.48'),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "ㄷ이 틀리다.", False, 'p.48')],
     second=0, steps=4, elim=1,
     view=["(가) 개발을 제한하되 토지 소유자에게 적절한 보상을 한다.",
           "(나) 토지 소유자에게 아무 보상 없이 개발을 금지하고 환경 보호만을 우선한다.",
           "(다) 토지 소유자의 뜻에 따라 개발을 자유롭게 허용하고 환경은 고려하지 않는다.",
           "ㄱ. (가)는 개인선을 실현하면서 공동선을 훼손하지 않는 대안을 모색한 것이다.",
           "ㄴ. (나)는 공익만을 강조하여 개인의 권리와 이익을 침해할 수 있다.",
           "ㄷ. (다)는 개인의 권리와 공동체의 환경을 모두 고려한 보완적 방안이다."])

item(20, 'MULTI_JUDGMENT', 'CONDITION_CHANGE', "다음 사례에서 상황 (가)와 (나)에 대한 노직과 롤스의 판단을 비교한 <보기>의 설명 중 옳은 것만을 있는 대로 고른 것은?\n을은 갑이 정당하게 취득한 소유물을 갑의 뜻에 따라 양도받았다. (가) 이 양도로 사회에서 가장 불리한 처지에 있는 사람의 처지가 나빠진다. (나) 이 양도로 가장 불리한 처지에 있는 사람의 처지가 가장 크게 개선된다.",
     D("ㄱ, ㄷ", "gd", '', "노직은 정당한 양도라는 이유로 (가)와 (나)를 모두 정당하게 보지만, 롤스는 (가)에서 차등의 원칙에 어긋난다고 보고 (나)에서는 부합한다고 본다.", True, 'p.47'),
     [D("ㄱ", "only_g", 'STRONG', "ㄷ도 옳다.", False, 'p.47'),
      D("ㄷ", "only_d", 'STRONG', "ㄱ도 옳다.", False, 'p.47'),
      D("ㄱ, ㄴ", "gn", 'MEDIUM', "ㄴ은 노직이 (가)에서 양도를 부정한다는 뜻이라 틀리다.", False, 'p.47'),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄴ이 틀리다.", False, 'p.47')],
     second=0, steps=5, elim=1,
     view=["ㄱ. 노직은 취득과 양도가 정당하다면 (가)와 (나)에서 모두 소유 권리가 인정된다고 볼 것이다.",
           "ㄴ. 노직은 (가)에서는 최소 수혜자의 처지가 나빠지므로 양도가 정당하지 않다고 볼 것이다.",
           "ㄷ. 롤스는 (가)에서는 차등의 원칙에 어긋나고 (나)에서는 부합한다고 볼 것이다."])

ITEMS.sort(key=lambda x: x['item_id'])
assert len(ITEMS) == 20
bundle = dict(
    batch_id='SOC-S2-JUSTICE-THEORIES-20261108', product_mode='ARC_N', subject='SOC', generator='CLAUDE', set_label='ARC N°',
    course='통합사회2', cover_subtitle='Ⅱ-2 자유주의와 공동체주의 정의관 20문항', school_line='동북고등학교 1학년 · 2026',
    created_at='2026-11-08T16:00:00+09:00',
    scope='2026 동북고 1학년 2학기 기말 임시 범위(사용자 지정, 소단원 선택은 임시 판단): 천재 통합사회2 Ⅱ-2 자유주의와 공동체주의 정의관 pp.44-49',
    request_spec=dict(decided_by='USER', stage='S2', item_count=20, difficulty_targets={'D2': 0.2, 'D3': 0.5, 'D45': 0.3}),
    source_composition=dict(policy_version='ARC-SOURCE-MIX-V1.0', profile='PAST_70_AI_30', mode='ORIGINAL_TRIAL',
                            authorized_by='STANDING_USER_RULE_20261108',
                            shortage_reason='현재 범위의 CONTENT_VERIFIED 문제은행 B=0 < R=14'),
    school_source_status='TEXTBOOK_TEXT_READ_PP34_61_VISUALS_NOT_CHECKED',
    school_source_ref=SRC,
    items=ITEMS)
for it in ITEMS:
    it['provenance'] = dict(mode='AI_ORIGINAL', school_scope_refs=[SRC],
                            design_purpose='S2 자료 해석·적용: 교과서 pp.44-49의 두 정의관과 사상가 입장을 새 사례에 적용')
yaml.safe_dump(bundle, open(OUT / 'items_v1_textbook_based_REJECTED.yaml', 'w', encoding='utf-8'), allow_unicode=True, sort_keys=False, width=1000)
print('items', len(ITEMS), 'answers', [i['answer'] for i in ITEMS])
print('diff', dict(collections.Counter(i['difficulty'] for i in ITEMS)), 'pos', dict(collections.Counter(i['answer'] for i in ITEMS)))
