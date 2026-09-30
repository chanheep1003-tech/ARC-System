# -*- coding: utf-8 -*-
import sys, pathlib, copy
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / "sources" / "KOR" / "공통국어2"))
import supplement4 as S

def put(seq, old, new):
    out, hit = [], 0
    for x in seq:
        if old in x and not hit:
            x = x.replace(old, new, 1); hit = 1
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

TAN = list(S.TAN_LINES)
for lab, txt in (("㉠", "장초(萇楚)의 무지(無知)를 부러워하나 어찌하리"), ("㉡", "베틀 북도 쓸데없어 빈 벽에 남겨 두고"), ("㉢", "솥 시루도 버려두니 붉은빛이 다 되었다"),
                 ("㉣", "세시 삭망 명일 기제는 무엇으로 제사하며"), ("㉤", "네 혼자 신의 있어 나를 아니 버리거든")):
    TAN = put(TAN, txt, "{%s|%s}" % (lab, txt))
PAL = list(S.PAL_LINES)
for lab, txt in (("㉠", "차디찬 아침인데"), ("㉡", "묘향산행 승합자동차는 텅 하니 비어서"), ("㉢", "계집아이는 운다 느끼며 운다"),
                 ("㉣", "텅 비인 차 안 한구석에서"), ("㉤", "이렇게 추운 아침에도 손이 꽁꽁 얼어서")):
    PAL = put(PAL, txt, "{%s|%s}" % (lab, txt))
MEM = copy.deepcopy(S.MEM_STANZAS)
for lab, txt in (("㉠", "움직이지 못하는 건물들은 눈을 뒤집어쓰고"), ("㉡", "그 춥고 큰 방"), ("㉢", "어떻게 해야 할까, 나는 중지시킬 수 없었다"),
                 ("㉣", "그리고 나는 우연히 지금 그를 떠올리게 되었다"), ("㉤", "밤은 깊고 텅 빈 사무실 창밖으로 눈이 퍼붓는다")):
    put_st(MEM, txt, "{%s|%s}" % (lab, txt))

SETS = [
    dict(rng=(1, 10), name="탄궁가", kind="poem", lines=TAN, src="정훈, 「탄궁가」", notes=S.TAN_NOTES),
    dict(rng=(11, 20), name="팔원", kind="poem", lines=PAL, src="백석, 「팔원(八院) — 서행시초(西行詩抄) 3」", notes=S.PAL_NOTES),
    dict(rng=(21, 30), name="기억할 만한 지나침", kind="stanzas", stanzas=MEM, src="기형도, 「기억할 만한 지나침」", notes=S.MEM_NOTES),
    dict(rng=(31, 40), name="칸트와 헤겔의 자유", kind="prose", paras=S.KANT_PARAS, src="이행남, 「칸트의 도덕적 자율성으로부터 헤겔의 인륜적 자율성으로」", notes=[]),
]
