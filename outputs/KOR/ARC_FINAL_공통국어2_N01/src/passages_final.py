# -*- coding: utf-8 -*-
"""ARC FINAL N°01 — 공통국어2 2026-2학기 중간고사 대비. 지문은 sources/KOR/공통국어2 라이브러리에서 import."""
import sys, pathlib, copy
LIB = pathlib.Path(__file__).resolve().parents[4] / "sources" / "KOR" / "공통국어2"
sys.path.insert(0, str(LIB))
import unit1 as U, unit2 as V, supplement4 as S

def put(seq, old, new):
    """seq(list[str]) 안의 old를 new로 1회 치환(못 찾으면 오류)."""
    out, hit = [], 0
    for x in seq:
        if old in x and not hit:
            x = x.replace(old, new, 1); hit = 1
        out.append(x)
    assert hit, old
    return out

# (가) 제망매가 / (나) 속미인곡 (교과서 1단원)
JMG = put(put(list(U.JMG), "이에 저에 떨어질 잎처럼,", "이에 저에 {㉠|떨어질 잎}처럼,"), "아아, 미타찰(彌陀刹)에서 만날 나", "아아, {㉡|미타찰(彌陀刹)}에서 만날 나")
SMI = copy.deepcopy(U.SMI)
def put_st(st, old, new):
    hit = 0
    for k, s in enumerate(st):
        for j, ln in enumerate(s):
            if old in ln and not hit:
                st[k][j] = ln.replace(old, new, 1); hit = 1
    assert hit, old
put_st(SMI, "낙월(落月)", "{㉢|낙월(落月)}")

# 춘향전 (1단원)
CHH = list(U.CHH)
CHH = put(CHH, "‘마는’ 하는 끝말을 내뱉고는 입맛이 사납겠다.", "{㉠|‘마는’ 하는 끝말을 내뱉고는 입맛이 사납겠다.}")
CHH = put(CHH, "‘오냐, 도적질은 내가 하마. 오라는 네가 받아라.’", "{㉡|‘오냐, 도적질은 내가 하마. 오라는 네가 받아라.’}")
CHH = put(CHH, "@@VERSE@@금준미주(金樽美酒) 천인혈(千人血)이요", "@@VERSE@@{㉢|금준미주(金樽美酒) 천인혈(千人血)이요}")
CHH = put(CHH, "인궤 잃고 강정 들고, 병부 잃고 송편 들고,", "{㉣|인궤 잃고 강정 들고, 병부 잃고 송편 들고,}")
CHH = put(CHH, "“내려오는 관장마다 모두 명관(名官)이로구나.", "{㉤|“내려오는 관장마다 모두 명관(名官)이로구나.}")

# 협상 (2단원): (단계, 화자, 발언) → 본문. 마크 삽입
NEGO = []
for st, sp, tx, nt in V.NEGO:
    NEGO.append([st, sp, tx])
def put_n(old, new):
    hit = 0
    for r in NEGO:
        if old in r[2] and not hit:
            r[2] = r[2].replace(old, new, 1); hit = 1
    assert hit, old
put_n("학교 운동장의 지하를 지나는 터널 공사가 걱정되는 점 이해합니다.", "{㉠|학교 운동장의 지하를 지나는 터널 공사가 걱정되는 점 이해합니다.}")
put_n("또 터널 내부로 토사와 지하수가 유입되어 땅 꺼짐 현상과 같은 심각한 위험을 초래할 수도 있다고 하던데……. 정말 이런 사고가 나면 책임질 수 있으십니까?", "{㉡|또 터널 내부로 토사와 지하수가 유입되어 땅 꺼짐 현상과 같은 심각한 위험을 초래할 수도 있다고 하던데……. 정말 이런 사고가 나면 책임질 수 있으십니까?}")
put_n("대다수 국민의 생활 여건을 개선하려는 철도 사업을 이렇게 반대하는 것은 지역 이기주의로 비칠 수 있지 않을까요?", "{㉢|대다수 국민의 생활 여건을 개선하려는 철도 사업을 이렇게 반대하는 것은 지역 이기주의로 비칠 수 있지 않을까요?}")
put_n("그렇다면 지하 터널 전체 구간이 아니라 학교와 주거지 아래 일부 공사 구간만 공법을 변경하는 것은 어떠신지요?", "{㉣|그렇다면 지하 터널 전체 구간이 아니라 학교와 주거지 아래 일부 공사 구간만 공법을 변경하는 것은 어떠신지요?}")
put_n("학교와 주거지 아래 지하 터널 구간에서는 고속 철도 운행을 일반 열차의 평균 속력 120km/h로 낮춰서 운행해 주시기 바랍니다.", "{㉤|학교와 주거지 아래 지하 터널 구간에서는 고속 철도 운행을 일반 열차의 평균 속력 120km/h로 낮춰서 운행해 주시기 바랍니다.}")
NEGO_PRE = ("<b>글의 상황</b> 수목구와 수목산 국립 공원 지하를 통과하는 고속 철도 공사 계획이 발표되자, 수목구 주민들과 환경 단체가 ‘고속 철도 공사 반대 위원회’(이하 반대 위원회)를 결성하여 "
            "‘고속 철도 공사 추진 위원회’(이하 추진 위원회)에 협상을 요구했다. 공사 계획에 따르면 수목산 국립 공원 일부 지하와 수목 고등학교 운동장·주거지 일부 지하에 화약을 이용한 발파 방식으로 터널을 뚫고, "
            "전 구간에서 300km/h로 운행할 예정이다.")
NEGO_NOTES = ["발파(發破): 바위나 대상물 속에 구멍을 뚫어 폭약을 재어 넣고 폭파함.", "철새 도래지: 철새 따위가 다른 곳에서 들어와 머무르는 곳."]

SETS = [
    dict(rng=(1, 3), kind="multi", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 1~3번, 서·논술형 1번)", parts=[
        dict(label="(가)", kind="poem", lines=JMG, src="월명사, 「제망매가」 (김완진 해독)", notes=[]),
        dict(label="(나)", kind="stanzas", stanzas=SMI, src="정철, 「속미인곡」", notes=U.SMI_NOTES)]),
    dict(rng=(4, 5), kind="prose", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 4~5번)", pre=U.CHH_PRE, paras=CHH, src="작자 미상, 「춘향전」", notes=U.CHH_NOTES),
    dict(rng=(6, 7), kind="stanzas", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 6~7번)", stanzas=U.SURA, src="백석, 「수라」", notes=U.SURA_NOTES),
    dict(rng=(8, 10), kind="prose", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 8~10번, 서·논술형 2번)", pre=U.GU_PRE, paras=U.GU, src="윤흥길, 「아홉 켤레의 구두로 남은 사내」 (일부 발췌)", notes=U.GU_NOTES),
    dict(rng=(11, 14), kind="multi", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 11~14번)", parts=[
        dict(label="(가)", kind="poem", lines=S.TAN_LINES, src="정훈, 「탄궁가」", notes=S.TAN_NOTES),
        dict(label="(나)", kind="poem", lines=S.PAL_LINES, src="백석, 「팔원(八院) — 서행시초(西行詩抄) 3」", notes=S.PAL_NOTES),
        dict(label="(다)", kind="stanzas", stanzas=S.MEM_STANZAS, src="기형도, 「기억할 만한 지나침」", notes=S.MEM_NOTES)]),
    dict(rng=(15, 17), kind="prose", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 15~17번)", paras=S.KANT_PARAS, src="이행남, 「칸트의 도덕적 자율성으로부터 헤겔의 인륜적 자율성으로」", notes=[]),
    dict(rng=(18, 19), kind="essay", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 18~19번, 서·논술형 3번)",
         pre="<b>글의 상황</b> 소민이는 유기견이 계속 증가하는 사회적 문제를 해결하기 위해, 우리 지역 주민들을 독자로 하여 사회 관계망 서비스(SNS)에 올릴 논증하는 글을 썼다.",
         head=V.ESSAY_TITLE, paras=V.ESSAY, src="소민이의 글", notes=[]),
    dict(rng=(20, 22), kind="dialog", title="※ 다음 글을 읽고 물음에 답하시오. (선택형 20~22번, 서·논술형 4번)", pre=NEGO_PRE, head="우리 학교 아래로 고속 철도가 지나간다고?", turns=NEGO,
         deal=V.NEGO_DEAL, src="협상 대화", notes=NEGO_NOTES),
]
