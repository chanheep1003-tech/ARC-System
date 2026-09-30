# -*- coding: utf-8 -*-
import sys, pathlib, copy
LIB = pathlib.Path(__file__).resolve().parents[4] / "sources" / "KOR" / "공통국어2"
sys.path.insert(0, str(LIB))
import unit1 as U, unit2 as V, supplement4 as S

def put(seq, old, new, all_=False):
    out, hit = [], 0
    for x in seq:
        if old in x and (all_ or not hit):
            x = x.replace(old, new, None if False else (-1 if all_ else 1)); hit += 1
        out.append(x)
    assert hit, old
    return out
def put_st(st, old, new, all_=False):
    hit = 0
    for k, s in enumerate(st):
        for j, ln in enumerate(s):
            if old in ln and (all_ or not hit):
                st[k][j] = ln.replace(old, new); hit += 1
    assert hit, old
    return st

# 01 제망매가
JMG = put(list(U.JMG), "이른 바람", "{㉠|이른 바람}")
JMG = put(JMG, "떨어질 잎", "{㉡|떨어질 잎}")
JMG = put(JMG, "한 가지", "{㉢|한 가지}")
JMG = put(JMG, "가는 곳 모르온저", "{㉣|가는 곳 모르온저}")
JMG = put(JMG, "미타찰(彌陀刹)", "{㉤|미타찰(彌陀刹)}")
# 02 속미인곡
SMI = copy.deepcopy(U.SMI)
for lab, txt in (("㉠", "반벽(半壁) 쳥등(靑燈)"), ("㉡", "오뎐된 계셩(鷄聲)"), ("㉢", "어엿븐 그림재"), ("㉣", "낙월(落月)"), ("㉤", "구ᄌᆞᆫ 비")):
    put_st(SMI, txt, "{%s|%s}" % (lab, txt))
# 03 춘향전
CHH = list(U.CHH)
CHH = put(CHH, "‘마는’ 하는 끝말을 내뱉고는 입맛이 사납겠다.", "{㉠|‘마는’ 하는 끝말을 내뱉고는 입맛이 사납겠다.}")
CHH = put(CHH, "‘오냐, 도적질은 내가 하마. 오라는 네가 받아라.’", "{㉡|‘오냐, 도적질은 내가 하마. 오라는 네가 받아라.’}")
CHH = put(CHH, "@@VERSE@@금준미주(金樽美酒) 천인혈(千人血)이요", "@@VERSE@@{㉢|금준미주(金樽美酒) 천인혈(千人血)이요}")
CHH = put(CHH, "인궤 잃고 강정 들고, 병부 잃고 송편 들고,", "{㉣|인궤 잃고 강정 들고, 병부 잃고 송편 들고,}")
CHH = put(CHH, "“내려오는 관장마다 모두 명관(名官)이로구나.", "{㉤|“내려오는 관장마다 모두 명관(名官)이로구나.}")
# 04 수라
SURA = copy.deepcopy(U.SURA)
put_st(SURA, "문밖으로 쓸어 버린다", "{㉠|문밖}으로 쓸어 버린다")
put_st(SURA, "차디찬 밤이다", "{㉡|차디찬 밤}이다")
put_st(SURA, "찬 밖이라도", "{㉢|찬 밖}이라도")
put_st(SURA, "고이 보드라운 종이에 받어", "{㉣|고이 보드라운 종이에 받어}")
put_st(SURA, "쉬이 만나기나 했으면 좋으련만", "{㉤|쉬이 만나기나 했으면 좋으련만}")
# 05 아홉 켤레
GU = list(U.GU)
GU = put(GU, "그의 구두는 놀랄 만큼 반짝거렸다.", "{㉠|그의 구두는 놀랄 만큼 반짝거렸다.}")
GU = put(GU, "그는 오른발을 들어 왼쪽 바짓가랑이 뒤에다 두어 번 문질렀다.", "{㉡|그는 오른발을 들어 왼쪽 바짓가랑이 뒤에다 두어 번 문질렀다.}")
GU = put(GU, "“오 선생, 이래 봬도 나 대학 나온 사람이오.”", "{㉢|“오 선생, 이래 봬도 나 대학 나온 사람이오.”}")
GU = put(GU, "아버지 노릇 하는 것도 아마 여러 질일 겁니다.", "{㉣|아버지 노릇 하는 것도 아마 여러 질일 겁니다.}")
# 06 논증
ESSAY = list(V.ESSAY)
ESSAY = put(ESSAY, "그러나 독일의 한 지역에서는 2013년부터 반려견 보호자 자격시험을 실시하면서 개 물림 사고가 현저히 감소했다고 합니다.", "{㉠|그러나 독일의 한 지역에서는 2013년부터 반려견 보호자 자격시험을 실시하면서 개 물림 사고가 현저히 감소했다고 합니다.}")
# 07 협상
NEGO = [[st, sp, tx] for st, sp, tx, nt in V.NEGO]
def put_n(old, new):
    hit = 0
    for r in NEGO:
        if old in r[2] and not hit:
            r[2] = r[2].replace(old, new, 1); hit = 1
    assert hit, old
for lab, txt in (("㉠", "경제적 가치만 생각하기에는 사람과 자연이 입을 피해가 큽니다."),
                 ("㉡", "학교 운동장의 지하를 지나는 터널 공사가 걱정되는 점 이해합니다."),
                 ("㉢", "또 터널 내부로 토사와 지하수가 유입되어 땅 꺼짐 현상과 같은 심각한 위험을 초래할 수도 있다고 하던데……. 정말 이런 사고가 나면 책임질 수 있으십니까?"),
                 ("㉣", "지역 이기주의로 비칠 수 있지 않을까요?"),
                 ("㉤", "비용과 시간이 더 들더라도 수목산 국립 공원을 피해 동측 농경지를 지나는 노선으로 변경하겠습니다. 대신 학교와 주거지의 지하 터널 구간은 유지하게 해 주십시오.")):
    put_n(txt, "{%s|%s}" % (lab, txt))
NEGO_PRE = ("<b>글의 상황</b> 수목구와 수목산 국립 공원 지하를 통과하는 고속 철도 공사 계획이 발표되자, 수목구 주민들과 환경 단체가 ‘고속 철도 공사 반대 위원회’(이하 반대 위원회)를 결성하여 "
            "‘고속 철도 공사 추진 위원회’(이하 추진 위원회)에 협상을 요구했다. 공사 계획에 따르면 수목산 국립 공원 일부 지하와 수목 고등학교 운동장·주거지 일부 지하에 화약을 이용한 발파 방식으로 터널을 뚫고, "
            "전 구간에서 300km/h로 운행할 예정이다.")
NEGO_NOTES = ["발파(發破): 바위나 대상물 속에 구멍을 뚫어 폭약을 재어 넣고 폭파함.", "철새 도래지: 철새 따위가 다른 곳에서 들어와 머무르는 곳."]
# 08 탄궁가
TAN = list(S.TAN_LINES)
TAN = put(TAN, "삼십 일에 아홉 끼니 얻거나 못 얻거나", "{㉠|삼십 일에 아홉 끼니 얻거나 못 얻거나}")
TAN = put(TAN, "안표(顔瓢)가 자주 빈들 나같이 비었으며", "{㉡|안표(顔瓢)가 자주 빈들 나같이 비었으며}")
TAN = put(TAN, "환곡(還穀) 장리(長利)는 무엇으로 장만하며", "{㉢|환곡(還穀) 장리(長利)는 무엇으로 장만하며}")
TAN = put(TAN, "빈천도 내 분수니 서러워해 무엇하리", "{㉣|빈천도 내 분수니 서러워해 무엇하리}")
# 09 팔원
PAL = list(S.PAL_LINES)
PAL = put(PAL, "옛말속같이 진진초록 새 저고리를 입고", "{㉠|옛말속같이 진진초록 새 저고리를 입고}")
PAL = put(PAL, "손잔등이 밭고랑처럼 몹시도 터졌다", "{㉡|손잔등이 밭고랑처럼 몹시도 터졌다}")
PAL = put(PAL, "쌔하얗게 얼은 자동차 유리창 밖에", "{㉢|쌔하얗게 얼은 자동차 유리창 밖에}")
PAL = put(PAL, "어느 한 사람도 눈을 씻는다", "{㉣|어느 한 사람도 눈을 씻는다}")
PAL = put(PAL, "찬물에 걸레를 쳤을 것이다", "{㉤|찬물에 걸레를 쳤을 것이다}")
# 10 기억할 만한 지나침
MEM = copy.deepcopy(S.MEM_STANZAS)
put_st(MEM, "그리고 나는 우연히", "{㉠|그리고 나는 우연히}", all_=True)
put_st(MEM, "희고 거대한 서류 뭉치로 변해갔다", "{㉡|희고 거대한 서류 뭉치로 변해갔다}")
put_st(MEM, "서기(書記)는 혼자 울고 있었다", "{㉢|서기(書記)는 혼자 울고 있었다}")
put_st(MEM, "침묵을 달아나지 못하게 하느라 나는 거의 고통스러웠다", "{㉣|침묵을 달아나지 못하게 하느라 나는 거의 고통스러웠다}")
put_st(MEM, "나는 그 사내를 어리석은 자라고 생각하지 않는다", "{㉤|나는 그 사내를 어리석은 자라고 생각하지 않는다}")

T = "※ 다음 글을 읽고 물음에 답하시오."
SETS = [
    dict(rng=(1, 10), name="제망매가", kind="poem", lines=JMG, src="월명사, 「제망매가」 (김완진 해독)", notes=[]),
    dict(rng=(11, 20), name="속미인곡", kind="stanzas", stanzas=SMI, src="정철, 「속미인곡」", notes=U.SMI_NOTES),
    dict(rng=(21, 30), name="춘향전", kind="prose", pre=U.CHH_PRE, paras=CHH, src="작자 미상, 「춘향전」", notes=U.CHH_NOTES),
    dict(rng=(31, 40), name="수라", kind="stanzas", stanzas=SURA, src="백석, 「수라」", notes=U.SURA_NOTES),
    dict(rng=(41, 50), name="아홉 켤레의 구두로 남은 사내", kind="prose", pre=U.GU_PRE, paras=GU, src="윤흥길, 「아홉 켤레의 구두로 남은 사내」 (일부 발췌)", notes=U.GU_NOTES),
    dict(rng=(51, 60), name="논증하는 글 쓰기", kind="essay", pre="<b>글의 상황</b> 소민이는 유기견이 계속 증가하는 사회적 문제를 해결하기 위해, 우리 지역 주민들을 독자로 하여 사회 관계망 서비스(SNS)에 올릴 논증하는 글을 썼다.",
         head=V.ESSAY_TITLE, paras=ESSAY, src="소민이의 글", notes=[]),
    dict(rng=(61, 70), name="지혜롭게 협상하기", kind="dialog", pre=NEGO_PRE, head="우리 학교 아래로 고속 철도가 지나간다고?", turns=NEGO, deal=V.NEGO_DEAL, src="협상 대화", notes=NEGO_NOTES),
    dict(rng=(71, 80), name="탄궁가", kind="poem", lines=TAN, src="정훈, 「탄궁가」", notes=S.TAN_NOTES),
    dict(rng=(81, 90), name="팔원", kind="poem", lines=PAL, src="백석, 「팔원(八院) — 서행시초(西行詩抄) 3」", notes=S.PAL_NOTES),
    dict(rng=(91, 100), name="기억할 만한 지나침", kind="stanzas", stanzas=MEM, src="기형도, 「기억할 만한 지나침」", notes=S.MEM_NOTES),
    dict(rng=(101, 110), name="칸트와 헤겔의 자유", kind="prose", paras=S.KANT_PARAS, src="이행남, 「칸트의 도덕적 자율성으로부터 헤겔의 인륜적 자율성으로」", notes=[]),
]
