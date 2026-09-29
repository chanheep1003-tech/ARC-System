# -*- coding: utf-8 -*-
"""ARC FINAL N°02 — 공통국어2 (지문은 N°01과 동일, 표기(㉠~) 위치만 문항에 맞게 재설정)."""
import sys, pathlib, copy
LIB = pathlib.Path(__file__).resolve().parents[4] / "sources" / "KOR" / "공통국어2"
sys.path.insert(0, str(LIB))
import unit1 as U, unit2 as V, supplement4 as S

def put(seq, old, new):
    out, hit = [], 0
    for x in seq:
        if old in x and not hit:
            x = x.replace(old, new, 1); hit = 1
        out.append(x)
    assert hit, old
    return out
def put_st(st, old, new):
    hit = 0
    for k, s in enumerate(st):
        for j, ln in enumerate(s):
            if old in ln and not hit:
                st[k][j] = ln.replace(old, new, 1); hit = 1
    assert hit, old
def wrap_st(st, start, label):
    for k, s in enumerate(st):
        for j, ln in enumerate(s):
            if ln.startswith(start):
                st[k][j] = "{%s|%s}" % (label, ln); return
    raise AssertionError(start)
def wrap_l(lines, start, label):
    lines = list(lines)
    for j, ln in enumerate(lines):
        if ln.startswith(start):
            lines[j] = "{%s|%s}" % (label, ln); return lines
    raise AssertionError(start)

# A. 제망매가·속미인곡
JMG = put(list(U.JMG), "이에 저에 떨어질 잎처럼,", "이에 저에 떨어질 잎처럼,")
JMG = put(JMG, "어느 가을 이른 바람에", "어느 가을 {㉠|이른 바람}에")
JMG = put(JMG, "한 가지에 나고", "{㉡|한 가지}에 나고")
JMG = put(JMG, "가는 곳 모르온저.", "{㉢|가는 곳 모르온저}.")
SMI = copy.deepcopy(U.SMI)
wrap_st(SMI, "구롬은", "㉣")
put_st(SMI, "어엿븐 그림재", "{㉤|어엿븐 그림재}")

# B. 춘향전
CHH = list(U.CHH)
CHH = put(CHH, "어사의 마음이 심란하구나.", "{㉠|어사의 마음이 심란하구나.}")
CHH = put(CHH, "어찌 아니 명관(名官)인가.", "{㉡|어찌 아니 명관(名官)인가.}")
CHH = put(CHH, "초목금수(草木禽獸)인들 아니 떨랴.", "{㉢|초목금수(草木禽獸)인들 아니 떨랴.}")
CHH = put(CHH, "이 글 뜻은,", "{㉣|이 글 뜻은,}")
CHH = put(CHH, "문짝을 이고 내달으니", "{㉤|문짝을 이고 내달으니}")

# E. 탄궁가
TAN = list(S.TAN_LINES)
TAN = wrap_l(TAN, "삼십 일에 아홉 끼니", "㉠")
TAN = wrap_l(TAN, "안표(顔瓢)가 자주 빈들", "㉡")
TAN = wrap_l(TAN, "웅얼웅얼 불평하며", "㉢")
TAN = wrap_l(TAN, "빈천도 내 분수니", "㉣")

# H. 협상
NEGO = [[st, sp, tx] for st, sp, tx, nt in V.NEGO]
def put_n(old, new):
    hit = 0
    for r in NEGO:
        if old in r[2] and not hit:
            r[2] = r[2].replace(old, new, 1); hit = 1
    assert hit, old
for lab, txt in [
    ("㉠", "경제적 가치만 생각하기에는 사람과 자연이 입을 피해가 큽니다."),
    ("㉡", "지역 이기주의로 비칠 수 있지 않을까요?"),
    ("㉢", "철도 이용객이 연간 170만 명 이상 증가하여 도로의 차량이 감소하면 매년 미세 먼지 204톤, 일산화 탄소, 질소 산화물, 휘발성 유기 화합물도 각각 6,781톤, 3,657톤, 536톤 이상 줄어들 것으로 예상됩니다."),
    ("㉣", "비용과 시간이 더 들더라도 수목산 국립 공원을 피해 동측 농경지를 지나는 노선으로 변경하겠습니다. 대신 학교와 주거지의 지하 터널 구간은 유지하게 해 주십시오."),
    ("㉤", "발파 진동에 관한 민원이 많을 것으로 예상이 되는데 그대로 진행하는 것이 더 큰 문제가 되지 않겠습니까?")]:
    put_n(txt, "{%s|%s}" % (lab, txt))
NEGO_PRE = ("<b>글의 상황</b> 수목구와 수목산 국립 공원 지하를 통과하는 고속 철도 공사 계획이 발표되자, 수목구 주민들과 환경 단체가 ‘고속 철도 공사 반대 위원회’(이하 반대 위원회)를 결성하여 "
            "‘고속 철도 공사 추진 위원회’(이하 추진 위원회)에 협상을 요구했다. 공사 계획에 따르면 수목산 국립 공원 일부 지하와 수목 고등학교 운동장·주거지 일부 지하에 화약을 이용한 발파 방식으로 터널을 뚫고, "
            "전 구간에서 300km/h로 운행할 예정이다.")
NEGO_NOTES = ["발파(發破): 바위나 대상물 속에 구멍을 뚫어 폭약을 재어 넣고 폭파함.", "철새 도래지: 철새 따위가 다른 곳에서 들어와 머무르는 곳."]

SETS = [
    dict(rng=(1, 3), kind="multi", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 1~3번, 서·논술형 1번)", parts=[
        dict(label="(가)", kind="poem", lines=JMG, src="월명사, 「제망매가」 (김완진 해독)", notes=[]),
        dict(label="(나)", kind="stanzas", stanzas=SMI, src="정철, 「속미인곡」", notes=U.SMI_NOTES)]),
    dict(rng=(4, 5), kind="prose", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 4~5번, 서·논술형 2번)", pre=U.CHH_PRE, paras=CHH, src="작자 미상, 「춘향전」", notes=U.CHH_NOTES),
    dict(rng=(6, 7), kind="stanzas", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 6~7번)", stanzas=U.SURA, src="백석, 「수라」", notes=U.SURA_NOTES),
    dict(rng=(8, 10), kind="prose", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 8~10번)", pre=U.GU_PRE, paras=U.GU, src="윤흥길, 「아홉 켤레의 구두로 남은 사내」 (일부 발췌)", notes=U.GU_NOTES),
    dict(rng=(11, 14), kind="multi", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 11~14번)", parts=[
        dict(label="(가)", kind="poem", lines=TAN, src="정훈, 「탄궁가」", notes=S.TAN_NOTES),
        dict(label="(나)", kind="poem", lines=S.PAL_LINES, src="백석, 「팔원(八院) — 서행시초(西行詩抄) 3」", notes=S.PAL_NOTES),
        dict(label="(다)", kind="stanzas", stanzas=S.MEM_STANZAS, src="기형도, 「기억할 만한 지나침」", notes=S.MEM_NOTES)]),
    dict(rng=(15, 17), kind="prose", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 15~17번, 서·논술형 3번)", paras=S.KANT_PARAS, src="이행남, 「칸트의 도덕적 자율성으로부터 헤겔의 인륜적 자율성으로」", notes=[]),
    dict(rng=(18, 19), kind="essay", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 18~19번)",
         pre="<b>글의 상황</b> 소민이는 유기견이 계속 증가하는 사회적 문제를 해결하기 위해, 우리 지역 주민들을 독자로 하여 사회 관계망 서비스(SNS)에 올릴 논증하는 글을 썼다.",
         head=V.ESSAY_TITLE, paras=V.ESSAY, src="소민이의 글", notes=[]),
    dict(rng=(20, 22), kind="dialog", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 20~22번, 서·논술형 4번)", pre=NEGO_PRE, head="우리 학교 아래로 고속 철도가 지나간다고?", turns=NEGO,
         deal=V.NEGO_DEAL, src="협상 대화", notes=NEGO_NOTES),
]
