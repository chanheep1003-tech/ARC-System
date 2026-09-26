# -*- coding: utf-8 -*-
# ARC N°08 간단 해설 — (정답 근거, 주요 오답 짚기)
import sys, pathlib, importlib.util
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("c", HERE / "content.py"); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
CIRC = "①②③④⑤"
ANS = [(q["t"] if q["t"] is not None else q["c"]) for q in c.Q]

EX = [
 ("10~11행: 올벼 씨는 반 넘게 쥐가 먹었고, 기장·피·조·팥은 서너 되를 부쳤다(뿌렸다).", "씨앗은 ‘집 안에 들어가’ 마련 → 이웃에게 빌린 것은 쟁기·호미뿐. 환곡·세금은 둘 다 마련 못 함."),
 ("41~42행은 하늘을 부르는 말이 아니라, 하늘이 만든 가난을 어찌하겠느냐는 체념의 설의이다.", "1~12행은 독백, 13행 아이들, 29~31행 가난 귀신, 37행 ‘네 말’ = 귀신의 말 → 모두 적절."),
 ("ㄱ(반복·운율), ㄴ(대구), ㄹ(형편이 나아질 상황의 가정 → 절망 강조)이 적절.", "ㄷ 잡초에게 원망을 돌리는 것 ×(자조) / ㅁ 설의는 벗어날 방법이 없다는 체념 ×."),
 ("‘온가지로’는 ‘온갖 방법으로’라는 뜻이다(가까스로 ×).", "일정 = 틀림없이, 상전 = 주인인 화자, 장만 = 갖춤, 여읠 줄 없다 = 떨어질 일이 없다."),
 ("생활을 사실적으로 나열하면서 결말에서 하늘이 정한 분수로 받아들이므로 (다) 현실 수용형.", "환곡·세금은 언급될 뿐 제도를 비판하지 않음 → (나) ×. 안회·원헌은 비교 기준이지 즐기는 삶 × → (가) ×."),
 ("‘이른 말이’(32행) 뒤 33~35행이 귀신의 말, 36행 ‘우는 듯 꾸짖는 듯’은 화자의 묘사.", "37~39행은 ‘돌이켜 생각하니’로 시작하는 화자의 생각 → ‘신의’도 화자의 말."),
 ("‘설마한들 어이하리’ = 설마 해도(아무리 바라도) 어찌하겠는가 → 끝나리라는 기대 ×, 체념.", "40행 ‘잔꾀로 여읠려냐’ = 떼어 낼 수 없다는 인정 → 적절."),
 ("&lt;보기&gt;는 자연(강산풍월)을 지키려고 가난을 지니지만, 윗글은 가난을 분수로 체념할 뿐 자연 속에서 즐기지 않는다.", "두 작품 모두 가난을 벗어나려는 시도(전송 / 팔려 함)가 있음 → 적절."),
 ("1~28행은 화자의 탄식 나열, 29행 이후 가난 귀신의 말이 끼어드는 대화 구성.", "40~42행(여읠려냐, 어이하리, 무엇하리)에도 설의법 → ‘설의 없음’ ×. 해결책 제시 ×."),
 ("ㄱ(격식 갖춘 전송), ㄴ(생사를 함께함), ㄹ(버린 세상 ↔ 버리지 않은 가난)이 적절.", "ㄷ ‘뉘 말 듣고’는 누구인지 몰라 따지는 반문 / ㅁ 40행은 떼어 낼 수 없다는 뜻."),
 ("차는 묘향산행(150리)인데 자성은 350리 → 차에서 내린 뒤에도 더 가야 한다고 짐작할 수 있다.", "삼촌은 ‘묘향산 어디메’에 산다 → ‘삼촌이 사는 자성’ ×. 차는 ‘텅 비어’ 승객이 거의 없다."),
 ("새 저고리가 넉넉한 대우를 뜻한다는 근거는 없다. 오히려 터진 손잔등과 대비된다.", "‘옛말속같이’(옛이야기 속처럼), 색채 대비, 길 떠나는 날의 차림 → 모두 적절한 감상."),
 ("ㄱ(12행 ‘차 안’), ㄴ(11행 관찰), ㅁ(어느 한 사람 = 화자가 눈을 씻음)만 알 수 있다.", "ㄷ 누구에게 들었는지 불명 / ㄹ ‘주재소장 같은’ = 짐작일 뿐 알고 있었다 ×."),
 ("13행에서 ‘같은’이 빠져도 16행 ‘-었을 것이다’로 끝나므로 13~16행 전체가 추측이다.", "신분을 직접 확인했다는 근거 없음. ‘어린아이 둘’이 동생이라는 근거도 없음."),
 ("현재 장면은 차 안팎에 한정되고, 과거(주재소장 집)는 화자의 짐작으로만 제시된다.", "우는 까닭을 밝히지 않음(역순 배열 ×), 인물과의 대화 없음."),
 ("「팔원」의 화자는 계집아이와 같은 차 안(한구석)에 있다 → ‘같은 공간에 있지 않다’ ×.", "&lt;보기&gt;는 지난 삶을 직접 본 적이 있고, 「팔원」은 짐작 → 적절한 대비."),
 ("‘쳤다’로 단정하면 짐작이 확인된 사실처럼 읽혀 추측의 여운이 약해진다.", "과거형이므로 ‘지금도 걸레를 친다’ ×, 13~15행과의 연결은 유지된다."),
 ("시는 지난 생활의 짐작으로 끝날 뿐, 아이의 앞날에 대한 판단을 제시하지 않는다.", "지명 제목·‘서쪽 지방을 다니며 쓴 시’라는 부제 → 여행자·관찰자 화자라는 감상은 적절."),
 ("「기억할 만한 지나침」의 화자는 ‘고통스러웠다’, ‘떠나지 못했다’일 뿐 눈물을 흘리지 않는다.", "눈을 씻는 것은 「팔원」의 ‘어느 한 사람’뿐."),
 ("‘옛말속같이’ = 옛이야기 속처럼(약속의 말 ×).", "텅 하니(휑하게), 예서(여기서), 어디메서(어디에서), 쌔하얗게(매우 하얗게)."),
 ("화자는 울음이 그칠 때까지 창밖에 머물렀고, 사내가 화자를 보았는지는 시에 없다.", "8행 ‘아무도 없었다’는 도움 요청 실패의 이유가 아님. 2연에서 우는 까닭은 끝내 밝혀지지 않음."),
 ("ㄱ(경직된 건물), ㄴ(개입할 수 없는 무력함), ㄹ(건물과 화자 모두 붙들린 모습)이 적절.", "ㄷ 눈보라로 길이 막혔다는 근거 없음 / ㅁ 붙잡아 두려 한 것은 사내가 아니라 ‘침묵’."),
 ("‘서류 뭉치’(건물 은유)와 문서를 다루는 ‘서기’가 이어져 차갑고 사무적인 분위기를 만든다.", "사내가 우는 까닭(업무)은 시에 드러나지 않는다."),
 ("윗글 2연은 사내를 어리석지 않다고 이해할 뿐, 사내의 슬픔이 끝났는지 확인하지 않는다.", "&lt;보기&gt;의 반복·일반화, 윗글의 특정 장면 → 대비 모두 적절."),
 ("사내를 발견한 직후 ‘눈은 퍼부었고’를 다시 쓰며, 지켜보는 이가 화자 혼자뿐인 상황으로 초점을 옮긴다.", "‘도와줄 사람이 없어서 못 멈췄다’는 시에 없는 인과."),
 ("떠올린 것도 ‘우연히’ → 오래 애써 왔다는 것은 반대 의미.", "‘지금’으로 시간 층위 변화, 텅 빈 사무실의 쓸쓸함, 현재형 판단 → 적절."),
 ("누군가 창을 두드렸다는 내용은 없다. 화자는 ‘중지시킬 수 없었’고 창밖에서 지켜보기만 했다.", "눈 오는 밤, 불빛, 춥고 큰 방, 혼자 울음 → 원문과 일치."),
 ("「팔원」은 지난 생활의 짐작으로 끝나며 앞날에 대한 희망을 드러내지 않는다.", "「탄궁가」 = 귀신의 말을 직접 들음, 윗글 = 창밖에서 관찰 → 적절."),
 ("‘그 춥고 큰 방’의 ‘그’는 앞에서 말한(유리창 너머 보이는) 방을 가리킬 뿐, 들어가 본 경험 ×.", "‘무슨 관공서였는데’ → 잘 모르는 행인 / 희미한 불빛이 시선을 이끎 → 적절."),
 ("‘못했다’(능력·상황 부정) → ‘않았다’(의지 부정)로 바꾸면 스스로 머문 것처럼 읽혀, 붙들린 느낌이 약해진다.", "시제·사실(떠났다/울음이 그쳤다)은 달라지지 않는다."),
 ("준칙은 모든 이성적 존재자에게 적용해도 모순 없이 실현되는 보편성을 갖추어야 도덕 법칙이 된다.", "① 예지계는 이성으로 ‘사유’될 뿐 경험적으로 ‘인식’되지 않는다(인식/사유 뒤바꿈). 시민 사회는 조정 ×, 충돌로 불안정."),
 ("ㄴ(이성이 원인 + 실천)과 ㄹ(괴로움 회피 = 이성 아닌 것이 원인 → 타율)이 적절.", "ㄱ 보편성 확인만 하고 행위하지 않음 → 자유 의식 × / ㄷ 원인이 이익·감정이면 (나)와 다르다."),
 ("자유는 예지계에 속해 경험적으로 인식되지 않으므로, 이성에 따른 행위를 실천할 때 ‘의식’된다.", "현상계의 인과 관찰로 확인 × / 욕구 충족의 만족감 ×."),
 ("국가의 법·제도를 통한 조정은 자유가 가장 구체화된 모습 → ‘자유의 후퇴’, ‘외적 강제’ ×.", "형의 사랑(가족), 규칙 없음(제도적 보장 약함), 앱 규칙(제도 수립), 그럼에도 분쟁(충돌) → 적절."),
 ("선택 가능성‘으로만’ 이해하고 법·제도를 구속으로 보는 것 = 추상적 자유.", "헤겔은 선택 가능성이 자유와 무관하다고 보지 않음(‘-으로만’이 핵심). 법은 희생이 아니라 조건."),
 ("ㄱ, ㄴ, ㄹ이 적절.", "ㄷ 관계·제도 속 구현은 헤겔만 / ㅁ 헤겔에게 법·제도는 자유의 조건."),
 ("‘한편’은 칸트의 견해에서 다른 관점인 헤겔의 견해로 화제를 옮긴다.", "윗글은 헤겔이 칸트를 반박하는 논쟁을 서술하지 않는다."),
 ("홉스는 법을 자유의 ‘제한’으로 보므로, 법에 따르는 것을 ‘조화를 이룬 완성된 자유’로 보는 것은 헤겔뿐이다.", "홉스(혼란 방지)와 헤겔(이해관계 조정) 모두 충돌을 다루는 법의 역할 인정 → 적절."),
 ("‘성향을 띠다’ = 어떤 성질을 가지다 → ‘정치적 성격을 띠다’.", "빛깔을 띠다(⑤), 미소를 띠다(④), 임무를 띠다(③), 띠를 두르다(①)는 다른 뜻."),
 ("ㄱ(벌이 싫어서 = 불쾌 회피 → 타율), ㄴ(가족 단계의 제도적 보장 약함), ㄷ(보편성 + 스스로 부과 + 실천), ㅁ(선택 가능성으로만)이 적절.", "ㄹ D는 법을 자유의 바탕(조건)으로 보므로 헤겔의 구체적 자유에 가깝다."),
]
assert len(EX) == 40

CSS = """
@page { size: A4; margin: 20mm 16.5mm 16mm;
  @top-left { content: "ARC N°08 · 해설"; font-family: Inter,'Noto Sans CJK KR',sans-serif; font-weight:700; font-size:7pt; letter-spacing:.06em; color:#1F2A44; vertical-align:bottom; padding-bottom:2.5mm; border-bottom:.45pt solid #d9dbde; }
  @top-right { content: "공통국어2 · 보충자료 4편"; font-family:'Noto Sans CJK KR',sans-serif; font-size:6.9pt; color:#666c74; vertical-align:bottom; padding-bottom:2.5mm; border-bottom:.45pt solid #d9dbde; }
  @bottom-center { content: counter(page, decimal-leading-zero); font-family: Inter,sans-serif; font-size:7pt; color:#687078; } }
*{box-sizing:border-box} body{margin:0;font-family:'Noto Sans CJK KR',sans-serif;color:#17191d;-webkit-print-color-adjust:exact;print-color-adjust:exact}
h1{font-size:15pt;margin:0 0 1mm;letter-spacing:-.03em} .sub{font-size:8pt;color:#666c74;margin-bottom:4mm}
.key{display:grid;grid-template-columns:repeat(10,1fr);border:.5pt solid #c9ccd0;margin-bottom:6mm;font-size:8pt}
.key div{text-align:center;padding:1.3mm 0;border-right:.4pt solid #e1e3e6;border-bottom:.4pt solid #e1e3e6}.key b{font-family:Inter,sans-serif;color:#1F2A44;font-size:7pt;margin-right:1mm}
.cols{column-count:2;column-gap:8mm;column-rule:.35pt solid #e4e5e7}
.set{font-size:8.2pt;font-weight:700;color:#fff;background:#1F2A44;padding:1.4mm 2.6mm;margin:0 0 3mm;break-after:avoid;break-inside:avoid}
.e{break-inside:avoid;margin-bottom:4mm;font-size:8.3pt;line-height:1.62;letter-spacing:-.02em}
.eh{display:flex;align-items:baseline;gap:2mm;margin-bottom:.8mm}
.no{font-family:Inter,sans-serif;font-weight:700;color:#1F2A44;font-size:9pt}
.ans{font-weight:700;color:#7A2E35}
.why{color:#23272c}.trap{color:#555a60}.trap:before{content:"오답 ";font-weight:700;color:#7A2E35;font-size:7.4pt}
"""
SETS = [(1, "[01~10] 정훈, 「탄궁가」"), (11, "[11~20] 백석, 「팔원」"), (21, "[21~30] 기형도, 「기억할 만한 지나침」"), (31, "[31~40] 칸트와 헤겔의 자유")]

def build():
    key = "".join(f"<div><b>{i:02d}</b>{CIRC[a]}</div>" for i, a in enumerate(ANS, 1))
    body = []
    for i, (why, trap) in enumerate(EX, 1):
        for s, title in SETS:
            if i == s: body.append(f'<div class="set">{title}</div>')
        body.append(f'<div class="e"><div class="eh"><span class="no">{i:02d}</span><span class="ans">정답 {CIRC[ANS[i-1]]}</span></div><div class="why">{why}</div><div class="trap">{trap}</div></div>')
    return (f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>ARC N°08 해설</title><style>{CSS}</style></head><body>"
            f"<h1>ARC N°08 공통국어2 — 정답과 해설</h1><div class='sub'>동북고등학교 2학기 중간고사 대비 · 보충자료 4편 40문항 · 간단 해설</div>"
            f"<div class='key'>{key}</div><div class='cols'>{''.join(body)}</div></body></html>")

(HERE / "explain.html").write_text(build(), encoding="utf-8")
print("".join(CIRC[a] for a in ANS))
