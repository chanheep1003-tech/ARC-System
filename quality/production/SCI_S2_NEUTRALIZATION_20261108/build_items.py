#!/usr/bin/env python3
"""SCI S2 20-item bundle (통합과학2 산·염기와 중화 반응). Every numeric claim is verified by sim() below."""
import yaml, pathlib

ROOT = pathlib.Path('/home/user/ARC-System')
OUT = ROOT / 'quality/production/SCI_S2_NEUTRALIZATION_20261108'
OUT.mkdir(parents=True, exist_ok=True)

# ---- chemistry model (통합과학 수준: 이온 수 모형). a mL of HCl at p H+ per mL; b mL of NaOH at q OH- per mL.
def sim(a, b, p=1, q=1):
    H0, OH0 = a * p, b * q
    w = min(H0, OH0)
    r = dict(Na=OH0, Cl=H0, H=H0 - w, OH=OH0 - w, water=w)
    r['total'] = r['Na'] + r['Cl'] + r['H'] + r['OH']
    r['kind'] = 'acid' if r['H'] > 0 else ('base' if r['OH'] > 0 else 'neutral')
    return r

TARGET_POS = [3, 5, 2, 4, 1, 3, 2, 4, 5, 2, 3, 1, 3, 4, 5, 4, 1, 5, 2, 1]
DIFF = {1: 'D2', 2: 'D2', 3: 'D2', 4: 'D2'}
for n in range(5, 15): DIFF[n] = 'D3'
for n in range(15, 21): DIFF[n] = 'D4'
ITEMS = []


def D(text, claim, c, why, v=False, ev='CONCEPT'):
    return dict(text=text, claim=claim, c=c, why=why, v=v, ev=[ev])


def item(no, fam, cov, stem, correct, distractors, second, steps, elim, view=None, table=None, key_v=True):
    base = [correct] + distractors
    pos = TARGET_POS[no - 1]
    final = list(range(1, 5))[: pos - 1] + [0] + list(range(1, 5))[pos - 1:]
    judg = []
    for i in final:
        b = base[i]
        judg.append(dict(v=(b['v'] if i else key_v), c='CORRECT' if i == 0 else b['c'], axis='application', claim=b['claim'],
                         ev=b['ev'], why=b['why']))
    it = dict(item_id=f'SCI-S2-{no:03d}', format='MCQ', family=fam, coverage=cov, difficulty=DIFF[no],
              balance='ADVANCED_DISCRIMINATION' if DIFF[no] == 'D4' else 'CORE_EXAM_POINT', stem=stem,
              options=[base[i]['text'] for i in final], answer=pos, second_best=final.index(second + 1) + 1,
              judgments=judg, reasoning_steps=steps, immediate_elimination=elim)
    if view: it['view'] = view
    if table: it['table'] = table
    ITEMS.append(it)


# ---------------------------------------------------------------- D2 (4)
item(1, 'KEY_WORD_FUNCTION', 'ACID_PROPERTIES', "염산(HCl) 수용액에 대한 설명으로 옳은 것은?",
     D("푸른색 리트머스 종이를 붉게 변화시킨다.", "litmus", '', "산성 수용액은 푸른색 리트머스 종이를 붉게 변화시킨다.", True),
     [D("BTB 용액을 떨어뜨리면 파란색이 된다.", "btb_blue", 'MEDIUM', "산성에서 BTB 용액은 노란색이다."),
      D("페놀프탈레인 용액을 붉게 변화시킨다.", "pp_red", 'MEDIUM', "산성에서 페놀프탈레인 용액은 색이 변하지 않는다."),
      D("마그네슘 리본을 넣으면 산소 기체가 발생한다.", "mg_o2", 'STRONG', "산과 마그네슘이 반응하면 수소 기체가 발생한다."),
      D("수용액에서 수산화 이온(OH⁻)을 내놓는다.", "oh_out", 'WEAK', "산은 수소 이온(H⁺)을 내놓는다.")],
     second=2, steps=1, elim=2)

item(2, 'KEY_WORD_FUNCTION', 'NET_IONS', "염산(HCl)과 수산화 나트륨(NaOH) 수용액이 중화 반응하여 물이 생성될 때, 실제로 반응하는 이온(알짜 이온)만을 모두 고른 것은?",
     D("H⁺, OH⁻", "h_oh", '', "물이 생성되는 반응은 H⁺ + OH⁻ → H₂O 이다.", True),
     [D("Na⁺, Cl⁻", "na_cl", 'STRONG', "Na⁺과 Cl⁻은 반응에 참여하지 않는 구경꾼 이온이다."),
      D("H⁺, Cl⁻", "h_cl", 'MEDIUM', "Cl⁻은 구경꾼 이온이다."),
      D("Na⁺, OH⁻", "na_oh", 'MEDIUM', "Na⁺은 구경꾼 이온이다."),
      D("H⁺, Na⁺, OH⁻", "h_na_oh", 'WEAK', "Na⁺은 구경꾼 이온이다.")],
     second=0, steps=1, elim=2)

item(3, 'MULTI_JUDGMENT', 'NEUTRALIZATION_DAILY', "중화 반응을 이용한 사례로 옳은 것만을 <보기>에서 있는 대로 고른 것은?",
     D("ㄱ, ㄴ", "gn", '', "ㄱ(제산제)과 ㄴ(염기성 물질을 바르는 것)은 중화 반응의 이용이다.", True),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 중화 반응의 이용이다."),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 중화 반응의 이용이다."),
      D("ㄷ", "only_d", 'MEDIUM', "산성 토양에는 염기성 물질을 뿌려야 하므로 ㄷ은 틀리다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ이 틀리다.")],
     second=0, steps=1, elim=2,
     view=["ㄱ. 속쓰림이 있을 때 염기성 물질이 든 제산제를 먹어 위산을 중화한다.",
           "ㄴ. 산성 물질에 쏘인 곳에 염기성 물질이 든 약을 발라 산을 중화한다.",
           "ㄷ. 산성화된 토양에 묽은 염산을 뿌려 토양의 산성을 중화한다."])

item(4, 'SEQUENCE_ORDER', 'BTB_COLOR_SEQUENCE', "묽은 염산(HCl)에 BTB 용액을 떨어뜨린 뒤 NaOH 수용액을 조금씩 넣어 완전히 중화시키고 계속 넣을 때, 용액의 색 변화를 순서대로 옳게 나타낸 것은?",
     D("노란색 → 초록색 → 파란색", "y_g_b", '', "산성은 노란색, 중성은 초록색, 염기성은 파란색이다.", True),
     [D("파란색 → 초록색 → 노란색", "b_g_y", 'STRONG', "산과 염기의 색이 반대로 되었다."),
      D("노란색 → 파란색 → 초록색", "y_b_g", 'MEDIUM', "중성은 파란색과 노란색 사이의 초록색이다."),
      D("초록색 → 노란색 → 파란색", "g_y_b", 'MEDIUM', "처음 산성 용액은 노란색이다."),
      D("붉은색 → 무색 → 파란색", "r_c_b", 'WEAK', "BTB 용액의 색 변화가 아니다.")],
     second=0, steps=1, elim=2)

# ---------------------------------------------------------------- D3 (10)
t5 = [(6, 4), (5, 5), (3, 7)]
s5 = [sim(*x) for x in t5]
assert [x['kind'] for x in s5] == ['acid', 'neutral', 'base'] and [x['water'] for x in s5] == [4, 5, 3]
item(5, 'MULTI_JUDGMENT', 'MIX_SAME_CONC_LIQUID', "표는 농도가 같은 HCl 수용액과 NaOH 수용액의 부피를 달리하여 혼합한 용액 (가)~(다)에 대한 자료이다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은? (단, 혼합 전 수용액의 온도는 모두 같다.)",
     D("ㄱ, ㄴ", "gn", '', "(가)는 산성이라 BTB가 노란색이고, (다)는 염기성이라 BTB가 파란색이다.", True),
     [D("ㄱ", "only_g", 'STRONG', "(다)가 염기성이므로 ㄴ도 옳다."),
      D("ㄴ", "only_n", 'STRONG', "(가)가 산성이므로 ㄱ도 옳다."),
      D("ㄷ", "only_d", 'MEDIUM', "(가)에서 생성된 물이 (다)보다 많아 최고 온도가 (가)에서 더 높다."),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "ㄷ이 틀리다.")],
     second=0, steps=2, elim=1,
     table=dict(header=["혼합 용액", "(가)", "(나)", "(다)"], rows=[["HCl 수용액 부피(mL)", "6", "5", "3"], ["NaOH 수용액 부피(mL)", "4", "5", "7"]]),
     view=["ㄱ. (가)에 BTB 용액을 떨어뜨리면 노란색이 된다.", "ㄴ. (다)에 BTB 용액을 떨어뜨리면 파란색이 된다.", "ㄷ. 혼합 후 최고 온도는 (가)와 (다)에서 같다."])

t6 = [(2, 8), (5, 5), (8, 2), (6, 4)]
w6 = [sim(*x)['water'] for x in t6]
assert w6 == [2, 5, 2, 4]
item(6, 'COMPARISON_MATRIX', 'WATER_COUNT_COMPARE', "표는 농도가 같은 HCl 수용액과 NaOH 수용액을 부피를 달리하여 혼합한 용액 (가)~(라)이다. 생성된 물 분자 수가 가장 많은 용액과, (가)와 생성된 물 분자 수가 같은 용액을 옳게 짝지은 것은?",
     D("(나), (다)", "nb_c", '', "생성된 물 분자 수는 (가)2, (나)5, (다)2, (라)4이므로 가장 많은 것은 (나), (가)와 같은 것은 (다)이다.", True),
     [D("(나), (라)", "nb_d", 'STRONG', "(라)의 물 분자 수는 4로 (가)의 2와 다르다."),
      D("(라), (다)", "d_c", 'MEDIUM', "가장 많은 것은 (나)이다."),
      D("(다), (나)", "c_nb", 'MEDIUM', "가장 많은 것은 (나)이다."),
      D("(나), (가)", "nb_a", 'WEAK', "(가) 자신과 비교할 수 없다.")],
     second=0, steps=2, elim=1,
     table=dict(header=["혼합 용액", "(가)", "(나)", "(다)", "(라)"], rows=[["HCl 수용액 부피(mL)", "2", "5", "8", "6"], ["NaOH 수용액 부피(mL)", "8", "5", "2", "4"]]))

t7 = [(1, 9), (3, 7), (5, 5), (7, 3), (9, 1)]
w7 = [sim(*x)['water'] for x in t7]
assert w7 == [1, 3, 5, 3, 1]
item(7, 'MULTI_JUDGMENT', 'PEAK_TEMPERATURE', "농도가 같은 HCl 수용액과 NaOH 수용액을 부피의 합이 10 mL가 되도록 표와 같이 혼합하였다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은? (단, 혼합 전 수용액의 온도는 모두 같다.)",
     D("ㄱ, ㄴ", "gn", '', "생성된 물 분자 수가 (다)에서 가장 많아 최고 온도가 가장 높고, (나)와 (라)는 물 분자 수가 3으로 같다.", True),
     [D("ㄱ", "only_g", 'STRONG', "(나)와 (라)의 물 분자 수가 같으므로 ㄴ도 옳다."),
      D("ㄴ", "only_n", 'STRONG', "(다)에서 가장 높으므로 ㄱ도 옳다."),
      D("ㄷ", "only_d", 'MEDIUM', "(가)는 염기성이고 (마)는 산성이다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ이 틀리다.")],
     second=0, steps=2, elim=1,
     table=dict(header=["혼합 용액", "(가)", "(나)", "(다)", "(라)", "(마)"], rows=[["HCl 수용액 부피(mL)", "1", "3", "5", "7", "9"], ["NaOH 수용액 부피(mL)", "9", "7", "5", "3", "1"]]),
     view=["ㄱ. 혼합 후 최고 온도가 가장 높은 것은 (다)이다.", "ㄴ. (나)와 (라)의 혼합 후 최고 온도는 같다.", "ㄷ. (가)와 (마)는 모두 염기성이다."])

t8 = [(4, 8), (6, 6), (10, 2)]
s8 = [sim(*x) for x in t8]
assert [x['total'] for x in s8] == [16, 12, 20]
item(8, 'MULTI_JUDGMENT', 'TOTAL_IONS_COMPARE', "표는 농도가 같은 HCl 수용액과 NaOH 수용액을 혼합한 용액 (가)~(다)에 대한 자료이다. 혼합 전 각 수용액 1 mL에 들어 있는 양이온과 음이온의 수는 각각 1개씩이라고 할 때, 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은?",
     D("ㄴ, ㄷ", "nd", '', "전체 이온 수는 (가)16, (나)12, (다)20이므로 (다)가 가장 많고 (나)는 (가)의 3/4이다.", True),
     [D("ㄱ, ㄴ", "gn", 'STRONG', "(가)는 (나)보다 전체 이온 수가 많다."),
      D("ㄱ, ㄷ", "gd", 'STRONG', "ㄱ이 틀리다."),
      D("ㄴ", "only_n", 'MEDIUM', "ㄷ도 옳다."),
      D("ㄱ, ㄴ, ㄷ", "gnd", 'MEDIUM', "ㄱ이 틀리다.")],
     second=0, steps=3, elim=1,
     table=dict(header=["혼합 용액", "(가)", "(나)", "(다)"], rows=[["HCl 수용액 부피(mL)", "4", "6", "10"], ["NaOH 수용액 부피(mL)", "8", "6", "2"]]),
     view=["ㄱ. 전체 이온 수는 (가)가 (나)보다 적다.", "ㄴ. 전체 이온 수는 (다)가 가장 많다.", "ㄷ. (나)의 전체 이온 수는 (가)의 전체 이온 수의 3/4배이다."])

# Q9: Na+ model: NaOH 10 mL has 8 Na+ 8 OH-; each 10 mL of HNO3 adds 4 H+ 4 NO3-
naoh = 8; per = 4
st = []
for n in (1, 2, 3):
    h = n * per; w = min(h, naoh)
    st.append(dict(Na=naoh, A=h, H=h - w, OH=naoh - w))
assert [x['H'] for x in st] == [0, 0, 4] and [x['Na'] + x['A'] + x['H'] + x['OH'] for x in st] == [16, 16, 24]
item(9, 'MULTI_JUDGMENT', 'CATION_MODEL', "표는 수산화 나트륨(NaOH) 수용액 10 mL에 묽은 질산(HNO₃) 10 mL씩을 차례로 넣었을 때 수용액 (가)~(다)에 들어 있는 양이온의 모형 수를 나타낸 것이다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은?",
     D("ㄱ, ㄷ", "gd", '', "■는 H⁺이고, 전체 이온 수는 (나)16, (다)24로 (다)가 (나)의 1.5배이다.", True),
     [D("ㄱ, ㄴ", "gn", 'STRONG', "(나)는 중성이므로 ㄴ(염기성)이 틀리다."),
      D("ㄱ", "only_g", 'STRONG', "ㄷ도 옳다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄴ이 틀리다."),
      D("ㄴ", "only_n", 'WEAK', "ㄴ은 틀리다.")],
     second=1, steps=3, elim=1,
     table=dict(header=["수용액", "(가)", "(나)", "(다)"], rows=[["● (Na⁺)의 수", "8", "8", "8"], ["■의 수", "0", "0", "4"]]),
     view=["ㄱ. ■는 H⁺이다.", "ㄴ. (나)는 염기성이다.", "ㄷ. 수용액에 들어 있는 전체 이온 수는 (다)가 (나)의 1.5배이다."])

t10 = [(2, 8), (5, 5), (8, 2)]
r10 = [(sim(*x)['Na'], sim(*x)['Cl']) for x in t10]
assert r10 == [(8, 2), (5, 5), (2, 8)]
item(10, 'MULTI_JUDGMENT', 'SPECTATOR_ION_RATIO', "표는 농도가 같은 HCl 수용액과 NaOH 수용액을 부피를 달리하여 혼합한 용액 A~C에 대한 자료이다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은?",
     D("ㄱ, ㄴ", "gn", '', "A는 Na⁺ 8, Cl⁻ 2이므로 4배, B는 5와 5로 같다. C는 1/4이다.", True),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다."),
      D("ㄱ, ㄷ", "gd", 'STRONG', "ㄷ에서 C는 1/4이므로 틀리다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ이 틀리다."),
      D("ㄷ", "only_d", 'MEDIUM', "ㄷ은 틀리다.")],
     second=1, steps=2, elim=1,
     table=dict(header=["혼합 용액", "A", "B", "C"], rows=[["HCl 수용액 부피(mL)", "2", "5", "8"], ["NaOH 수용액 부피(mL)", "8", "5", "2"]]),
     view=["ㄱ. A에서 Na⁺의 수는 Cl⁻의 수의 4배이다.", "ㄴ. B에서 Na⁺의 수와 Cl⁻의 수는 같다.", "ㄷ. C에서 (Na⁺의 수 / Cl⁻의 수)는 4이다."])

# Q11 evaporation
assert sim(6, 6)['kind'] == 'neutral' and sim(4, 6)['OH'] == 2 and sim(4, 6)['water'] == 4 and sim(6, 6)['water'] == 6
item(11, 'MULTI_JUDGMENT', 'SALT_AFTER_EVAPORATION', "농도가 같은 HCl 수용액과 NaOH 수용액을 (가) HCl 6 mL + NaOH 6 mL, (나) HCl 4 mL + NaOH 6 mL로 혼합하였다. 두 혼합 용액의 물을 완전히 증발시켜 고체를 얻었을 때, 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은? (단, 증발 과정에서 NaOH은 변하지 않는다.)",
     D("ㄱ, ㄴ", "gn", '', "(가)는 완전 중화되어 NaCl만, (나)는 NaOH이 남아 NaCl과 NaOH이 남는다.", True),
     [D("ㄱ", "only_g", 'STRONG', "(나)에는 NaCl과 NaOH이 모두 남으므로 ㄴ도 옳다."),
      D("ㄴ", "only_n", 'STRONG', "(가)에는 NaCl만 남으므로 ㄱ도 옳다."),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "ㄷ은 생성된 물 분자 수가 (가)가 더 많으므로 틀리다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ이 틀리다.")],
     second=0, steps=2, elim=1,
     view=["ㄱ. (가)에서는 염화 나트륨(NaCl)만 얻는다.", "ㄴ. (나)에서는 염화 나트륨(NaCl)과 수산화 나트륨(NaOH)이 얻어진다.",
           "ㄷ. 생성된 물 분자 수는 (나)가 (가)보다 많다."])

item(12, 'MULTI_JUDGMENT', 'ELECTROPHORESIS', "다음은 이온의 이동을 알아보는 실험이다. 유리판 위에 질산 칼륨(KNO₃) 수용액과 BTB 용액을 적셔 초록색이 된 거름종이를 올려놓고, 수용액 ㉠을 적신 실을 가운데에 놓은 뒤 전류를 흘려 주었더니 거름종이가 실에서부터 B극 쪽으로 노랗게 변했다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은?",
     D("ㄱ, ㄷ", "gd", '', "노랗게 변한 것은 H⁺이 (−)극인 B극 쪽으로 이동했기 때문이고, 이동한 이온은 H⁺이다.", True),
     [D("ㄱ", "only_g", 'STRONG', "ㄷ도 옳다."),
      D("ㄷ", "only_d", 'STRONG', "ㄱ도 옳다."),
      D("ㄱ, ㄴ", "gn", 'MEDIUM', "수산화 나트륨 수용액을 쓰면 OH⁻이 (+)극으로 이동해 파랗게 변하므로 ㄴ이 틀리다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄴ이 틀리다.")],
     second=0, steps=2, elim=1,
     view=["ㄱ. B극은 (−)극이다.", "ㄴ. ㉠으로 수산화 나트륨 수용액을 쓰면 같은 결과가 나타난다.", "ㄷ. 거름종이에서 노랗게 변한 부분으로 이동한 이온은 H⁺이다."])

item(13, 'COMPARISON_MATRIX', 'INDICATOR_TABLE', "표는 용액 A~D에 마그네슘 리본, BTB 용액, 페놀프탈레인 용액을 각각 넣었을 때의 결과이다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은?",
     D("ㄱ, ㄴ", "gn", '', "A와 D는 산성이고 B는 중성이다.", True),
     [D("ㄱ", "only_g", 'STRONG', "B가 중성이므로 ㄴ도 옳다."),
      D("ㄴ", "only_n", 'STRONG', "A와 D가 산성이므로 ㄱ도 옳다."),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "B와 C를 섞어도 중성이 되는 것은 아니며, ㄷ은 B(중성)이므로 중화 반응이 일어나지 않아 틀리다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ이 틀리다.")],
     second=0, steps=2, elim=1,
     table=dict(header=["용액", "마그네슘 리본", "BTB 용액", "페놀프탈레인 용액"],
                rows=[["A", "기체 발생", "노란색", "무색"], ["B", "변화 없음", "초록색", "무색"], ["C", "변화 없음", "파란색", "붉은색"], ["D", "기체 발생", "노란색", "무색"]]),
     view=["ㄱ. A와 D는 모두 산성이다.", "ㄴ. B는 중성이다.", "ㄷ. B와 C를 섞으면 중화 반응이 일어난다."])

# Q14: HCl 10 mL (conc c) + NaOH (2c) 4/5/6 mL
t14 = [sim(10, v, 1, 2) for v in (4, 5, 6)]
assert [x['kind'] for x in t14] == ['acid', 'neutral', 'base'] and [x['water'] for x in t14] == [8, 10, 10]
item(14, 'MULTI_JUDGMENT', 'DIFFERENT_CONC_BASIC', "농도가 c인 HCl 수용액 10 mL에 농도가 2c인 NaOH 수용액을 (가) 4 mL, (나) 5 mL, (다) 6 mL 넣어 혼합하였다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은?",
     D("ㄱ, ㄷ", "gd", '', "(가)는 H⁺이 남아 산성이고, (나)와 (다)에서 생성된 물 분자 수는 모두 10으로 같다.", True),
     [D("ㄱ", "only_g", 'STRONG', "ㄷ도 옳다."),
      D("ㄷ", "only_d", 'STRONG', "ㄱ도 옳다."),
      D("ㄱ, ㄴ", "gn", 'MEDIUM', "(다)는 염기성이라 BTB가 파란색이므로 ㄴ이 틀리다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄴ이 틀리다.")],
     second=0, steps=3, elim=1,
     view=["ㄱ. (가)는 산성이다.", "ㄴ. (다)에 BTB 용액을 떨어뜨리면 노란색이 된다.", "ㄷ. 생성된 물 분자 수는 (나)와 (다)에서 같다."])

# ---------------------------------------------------------------- D4 (6)
# Q15: (가) neutral given; HCl 5/NaOH 10 => p*5 = 10 => p = 2 (per mL), q = 1
a15 = [(5, 10), (5, 15), (10, 10)]
s15 = [sim(a, b, 2, 1) for a, b in a15]
assert [x['kind'] for x in s15] == ['neutral', 'base', 'acid'] and [x['water'] for x in s15] == [10, 10, 10] and [x['total'] for x in s15] == [20, 30, 40]
item(15, 'MULTI_JUDGMENT', 'UNKNOWN_CONC_RATIO', "표는 HCl 수용액과 NaOH 수용액의 부피를 달리하여 혼합한 용액 (가)~(다)에 대한 자료이다. (가)는 중성이다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은? (단, 혼합 전 수용액 1 mL에 들어 있는 양이온과 음이온의 수는 각 수용액에서 일정하다.)",
     D("ㄱ, ㄷ", "gd", '', "(가)가 중성이므로 HCl 농도가 NaOH의 2배이고, 전체 이온 수는 20:30:40 = 2:3:4이다.", True),
     [D("ㄱ, ㄴ", "gn", 'STRONG', "생성된 물 분자 수는 (가)~(다)에서 모두 10으로 같다. ㄴ이 틀리다."),
      D("ㄱ", "only_g", 'STRONG', "ㄷ도 옳다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄴ이 틀리다."),
      D("ㄷ", "only_d", 'MEDIUM', "ㄱ도 옳다.")],
     second=1, steps=4, elim=1,
     table=dict(header=["혼합 용액", "(가)", "(나)", "(다)"], rows=[["HCl 수용액 부피(mL)", "5", "5", "10"], ["NaOH 수용액 부피(mL)", "10", "15", "10"]]),
     view=["ㄱ. HCl 수용액의 농도는 NaOH 수용액 농도의 2배이다.", "ㄴ. 생성된 물 분자 수는 (나)가 (가)보다 많다.", "ㄷ. 혼합 용액 속 전체 이온 수는 (가) : (나) : (다) = 2 : 3 : 4 이다."])

# Q16: NaOH 10 mL fixed, HCl 5/15/30 (same conc). Unknown ions: ㉠ = Cl-, ㉡ = OH-
a16 = [5, 15, 30]
s16 = [sim(a, 10) for a in a16]
assert [x['Cl'] for x in s16] == [5, 15, 30] and [x['OH'] for x in s16] == [5, 0, 0] and [x['water'] for x in s16] == [5, 10, 10] and s16[1]['kind'] == 'acid'
item(16, 'MULTI_JUDGMENT', 'UNKNOWN_ION_ID', "표는 NaOH 수용액 10 mL에 HCl 수용액의 부피를 달리하여 넣어 만든 혼합 용액 (가)~(다)에 들어 있는 이온 ㉠과 ㉡의 수를 나타낸 것이다. ㉠과 ㉡은 각각 H⁺, Na⁺, Cl⁻, OH⁻ 중 하나이며, Na⁺의 수는 일정하다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은? (단, 혼합 전 수용액 1 mL에 들어 있는 이온 수는 각 수용액에서 일정하고, 두 수용액의 농도는 같다.)",
     D("ㄱ, ㄷ", "gd", '', "㉠은 늘어나는 Cl⁻, ㉡은 줄어드는 OH⁻이고, 생성된 물 분자 수는 (가)5, (다)10으로 (다)가 2배이다.", True),
     [D("ㄱ, ㄴ", "gn", 'STRONG', "(나)에는 H⁺이 남아 산성이므로 ㄴ이 틀리다."),
      D("ㄱ", "only_g", 'STRONG', "ㄷ도 옳다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄴ이 틀리다."),
      D("ㄷ", "only_d", 'MEDIUM', "ㄱ도 옳다.")],
     second=1, steps=4, elim=1,
     table=dict(header=["혼합 용액", "(가)", "(나)", "(다)"], rows=[["HCl 수용액 부피(mL)", "5", "15", "30"], ["㉠의 수", "5", "15", "30"], ["㉡의 수", "5", "0", "0"]]),
     view=["ㄱ. ㉠은 Cl⁻이다.", "ㄴ. (나)는 염기성이다.", "ㄷ. 생성된 물 분자 수는 (다)에서가 (가)에서의 2배이다."])

# Q17: BTB colours, ratio inferred from (가) green: HCl 3 / NaOH 6 neutral => p=2,q=1
a17 = [(6, 6), (4, 10), (5, 8)]
s17 = [sim(a, b, 2, 1) for a, b in a17]
assert [x['kind'] for x in s17] == ['acid', 'base', 'acid']
item(17, 'MULTI_JUDGMENT', 'INDICATOR_PREDICTION', "표는 HCl 수용액과 NaOH 수용액의 부피를 달리하여 혼합한 용액 (가)~(라)에 BTB 용액을 떨어뜨린 결과이다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은? (단, 혼합 전 수용액 1 mL에 들어 있는 양이온과 음이온의 수는 각 수용액에서 일정하다.)",
     D("ㄱ, ㄴ", "gn", '', "(가)가 초록색(중성)이므로 HCl 농도가 NaOH의 2배이다. (나)는 H⁺이 남아 노란색, (다)는 OH⁻이 남아 파란색이다.", True),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다."),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 옳다."),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "(라)는 H⁺이 남아 노란색이므로 ㄷ은 틀리다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ이 틀리다.")],
     second=1, steps=4, elim=1,
     table=dict(header=["혼합 용액", "(가)", "(나)", "(다)", "(라)"], rows=[["HCl 수용액 부피(mL)", "3", "6", "4", "5"], ["NaOH 수용액 부피(mL)", "6", "6", "10", "8"], ["BTB 용액의 색", "초록색", "?", "?", "?"]]),
     view=["ㄱ. (나)는 노란색이다.", "ㄴ. (다)는 파란색이다.", "ㄷ. (라)는 초록색이다."])

# Q18: temperature rise proportional to water count; p = 1.5 per mL HCl; total 20 mL
a18 = [(4, 16), (8, 12), (12, 8)]
s18 = [sim(a, b, 1.5, 1) for a, b in a18]
assert [x['water'] for x in s18] == [6, 12, 8] and [x['kind'] for x in s18] == ['base', 'neutral', 'acid']
item(18, 'MULTI_JUDGMENT', 'TEMPERATURE_TO_CONC', "HCl 수용액과 NaOH 수용액을 부피의 합이 20 mL가 되도록 혼합했을 때의 최고 온도는 표와 같다. 혼합 전 수용액의 온도는 모두 20.0 ℃이고, 최고 온도의 상승 폭은 생성된 물 분자 수에 비례한다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은? (단, 혼합 전 수용액 1 mL에 들어 있는 양이온과 음이온의 수는 각 수용액에서 일정하다.)",
     D("ㄱ, ㄴ", "gn", '', "(4 mL, 16 mL)에서 물 분자 6개를 만든 비로 HCl 농도가 NaOH의 1.5배임을 알 수 있고, (8, 12)에서 중성이다.", True),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다."),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 옳다."),
      D("ㄱ, ㄷ", "gd", 'MEDIUM', "(12, 8)은 H⁺이 남아 산성이므로 ㄷ은 틀리다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ이 틀리다.")],
     second=1, steps=4, elim=1,
     table=dict(header=["혼합 용액", "(가)", "(나)", "(다)"], rows=[["HCl 수용액 부피(mL)", "4", "8", "12"], ["NaOH 수용액 부피(mL)", "16", "12", "8"], ["최고 온도(℃)", "23.0", "26.0", "24.0"]]),
     view=["ㄱ. HCl 수용액의 농도는 NaOH 수용액 농도의 1.5배이다.", "ㄴ. (나)는 중성이다.", "ㄷ. (다)는 염기성이다."])

# Q19: p=2: ratio Na/Cl at (가) HCl 5 = 1 ; (나) HCl 10 -> 1/2 ; (다) HCl 20 -> 1/4 ; NaOH 10 mL fixed
a19 = [5, 10, 20]
s19 = [sim(a, 10, 2, 1) for a in a19]
assert [x['Na'] / x['Cl'] for x in s19] == [1.0, 0.5, 0.25] and s19[0]['kind'] == 'neutral' and s19[1]['water'] == s19[2]['water'] == 10
item(19, 'MULTI_JUDGMENT', 'RATIO_TO_CONC', "표는 NaOH 수용액 10 mL에 HCl 수용액의 부피를 달리하여 넣은 혼합 용액 (가)~(다)에서 Na⁺의 수와 Cl⁻의 수의 비를 나타낸 것이다. 이에 대한 설명으로 옳은 것만을 <보기>에서 있는 대로 고른 것은? (단, 혼합 전 수용액 1 mL에 들어 있는 양이온과 음이온의 수는 각 수용액에서 일정하다.)",
     D("ㄱ, ㄴ", "gn", '', "(가)에서 Na⁺과 Cl⁻ 수가 같으므로 중성이고 HCl 농도는 NaOH의 2배이다. (나)와 (다)의 생성된 물 분자 수는 모두 10이다.", True),
     [D("ㄱ", "only_g", 'STRONG', "ㄴ도 옳다."),
      D("ㄴ", "only_n", 'STRONG', "ㄱ도 옳다."),
      D("ㄴ, ㄷ", "nd", 'MEDIUM', "ㄷ에서 두 수용액의 농도는 같지 않으므로 틀리다."),
      D("ㄷ", "only_d", 'MEDIUM', "ㄷ이 틀리다.")],
     second=1, steps=4, elim=1,
     table=dict(header=["혼합 용액", "(가)", "(나)", "(다)"], rows=[["HCl 수용액 부피(mL)", "5", "10", "20"], ["Na⁺의 수 / Cl⁻의 수", "1", "1/2", "1/4"]]),
     view=["ㄱ. (가)는 중성이다.", "ㄴ. 생성된 물 분자 수는 (나)와 (다)에서 같다.", "ㄷ. 혼합 전 HCl 수용액과 NaOH 수용액의 농도는 같다."])

# Q20: NaOH 20 mL + HCl 10/20/30 mL, same conc.  x=Cl at 10, y=OH at 10, z=H at 30
s20 = [sim(a, 20) for a in (10, 20, 30)]
assert (s20[0]['Cl'], s20[0]['OH'], s20[2]['H']) == (10, 10, 10) and s20[1]['kind'] == 'neutral'
item(20, 'CASE_APPLICATION', 'TABLE_FILL_IN', "표는 NaOH 수용액 20 mL에 HCl 수용액을 넣어 만든 혼합 용액 (가)~(다)에 들어 있는 이온의 수를 나타낸 것이다. (나)는 중성이고, 혼합 전 수용액 1 mL에 들어 있는 양이온과 음이온의 수는 각 수용액에서 일정하다. x + y + z는? (단, 두 수용액의 농도는 같다.)",
     D("30", "n30", '', "(나)가 중성이므로 두 수용액 농도가 같아 (가)에서 Cl⁻ x = 10, OH⁻ y = 10, (다)에서 H⁺ z = 10이다.", True),
     [D("20", "n20", 'STRONG', "세 값을 모두 더하면 30이다."),
      D("40", "n40", 'STRONG', "세 값을 모두 더하면 30이다."),
      D("50", "n50", 'MEDIUM', "세 값을 모두 더하면 30이다."),
      D("60", "n60", 'WEAK', "세 값을 모두 더하면 30이다.")],
     second=0, steps=4, elim=1,
     table=dict(header=["혼합 용액", "(가)", "(나)", "(다)"],
                rows=[["HCl 수용액 부피(mL)", "10", "20", "30"], ["Na⁺의 수", "20", "20", "20"], ["Cl⁻의 수", "x", "20", "30"],
                      ["OH⁻의 수", "y", "0", "0"], ["H⁺의 수", "0", "0", "z"]]))

ITEMS.sort(key=lambda x: x['item_id'])
# option numbers for Q20 must be ascending numerals: reorder so options read 20,30,40,50,60 with key 30
it20 = ITEMS[19]
opts = ['20', '30', '40', '50', '60']
key_text = '30'
j = it20['options']
# rebuild judgments keyed by text
by_text = {o: jd for o, jd in zip(j, it20['judgments'])}
it20['options'] = opts
it20['judgments'] = [by_text[o] for o in opts]
it20['answer'] = opts.index(key_text) + 1
it20['second_best'] = opts.index('20') + 1
TARGET_POS[19] = it20['answer']

bundle = dict(
    batch_id='SCI-S2-NEUTRALIZATION-20261108', product_mode='ARC_N', subject='SCI', generator='CLAUDE', set_label='ARC N°',
    course='통합과학2', cover_subtitle='산·염기와 중화 반응 20문항', school_line='동북고등학교 1학년 · 2026',
    created_at='2026-11-08T14:00:00+09:00',
    scope='2026 동북고 1학년 2학기 기말 임시 범위(사용자 지정): 통합과학2 산·염기와 중화 반응',
    request_spec=dict(decided_by='USER', stage='S2', item_count=20, difficulty_targets={'D2': 0.2, 'D3': 0.5, 'D45': 0.3}),
    source_composition=dict(policy_version='ARC-SOURCE-MIX-V1.0', profile='PAST_70_AI_30', mode='ORIGINAL_TRIAL',
                            authorized_by='STANDING_USER_RULE_20261108',
                            shortage_reason='현재 범위의 CONTENT_VERIFIED 문제은행 B=0 < R=14; 학교 교과서·학습지 미확인'),
    school_source_status='NOT_READ',
    calibration_reference='quality/anchors/SCI_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0.yaml (난도·형식 참고만, 문항·수치 미사용)',
    items=ITEMS)
for it in ITEMS:
    it['provenance'] = dict(mode='AI_ORIGINAL', school_scope_refs=['SCI-SCOPE-USER-20261108'],
                            design_purpose='S2 자료 해석·적용: 이온 수 모형과 혼합 부피 자료로 중화 반응을 추론')
yaml.safe_dump(bundle, open(OUT / 'items.yaml', 'w', encoding='utf-8'), allow_unicode=True, sort_keys=False, width=1000)
print('items', len(ITEMS), 'answers', [i['answer'] for i in ITEMS])
import collections
print('diff', dict(collections.Counter(i['difficulty'] for i in ITEMS)), 'pos', dict(collections.Counter(i['answer'] for i in ITEMS)))
