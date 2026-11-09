import yaml,glob,re,collections,json
SRC={'A':'KOR_CONFUSION_RAW_A_KILLER_SETS_20261109.yaml','B':'KOR_CONFUSION_RAW_B_FREQUENT_SETS_20261109.yaml','C':'KOR_CONFUSION_RAW_C_SCHOOL_MATERIALS_20261109.yaml','D':'KOR_CONFUSION_RAW_D_MOCK_GRAMMAR_20261109.yaml'}
D='/home/user/ARC-System/quality/exam_style/'
ents=[]
for k,f in SRC.items():
    d=yaml.safe_load(open(D+f))
    for e in d['entries']:
        e['_src']=k; ents.append(e)
CL=[
('M-JU','중세국어','주격 조사 이/ㅣ/영형태',['주격 조사 이/','주격 조사 ‘ㅇ','주격 조사: ','보조사 ‘ㅇ/은’','반모음 ㅣ 말음']),
('M-DONGHYUNG','중세국어','동형 어절 판별(이/에: 주격·비교 부사격·관형격·서술격)',['비교 부사격','동형','형태가 같은 ‘이’','관형격 ㅣ(제','부사격 조사','서술격','부사격 조사: 비교','‘이셔’']),
('M-GWAN','중세국어','관형격 조사 ㅅ/ᄋᆡ/의',['관형격 조사','관형격 ㅅ','중세 국어 관형격']),
('M-MOK','중세국어','목적격 조사 형태 선택',['목적격']),
('M-HGEUK','중세국어','ㅎ종성·ㄱ덧생김 체언',['ㅎ 종성','ㅎ종성','ㄱ덧생김','ㄱ종성','ㄱ 곡용','ㅎ 흔적','ㅎ 흔적처럼','ㄱ 곡용 체언']),
('M-MOEUM','중세국어','모음 조화',['모음 조화','모음조화']),
('M-SIGI','중세국어','음운 변화의 시기·적용 판정(원순모음화·구개음화·두음 법칙·모음 변화)',['원순모음화','구개음화 적용','구개음화 정밀','구개음화 미적용','구개음화의 통시','구개음화: ','두음 법칙의 시기','두음 법칙 미적용','두음 법칙·구개음화의 시기','시기 판정','시기·범위','모음 축약 현상','단모음 7개','아래아(ㆍ) 소실','아래아, ㅿ']),
('M-OLDLETTER','중세국어','옛 글자 식별·소실(ㅸ ㆁ ㆆ ㅿ ㆍ)',['옛 글자','사라진 글자','현대에 쓰이지','옛 글자 식별']),
('M-JONGSEONG','중세국어','8종성법·이어적기/끊어적기·표기 변천',['8종성','이어적기','끊어적기','이어 적','연철']),
('M-BYEONGSEO','중세국어','병서·어두 자음군·ㅅ계 합용병서',['병서','어두 자음군','각자병서','ㅅ계']),
('M-JEJA','중세국어','훈민정음 제자 원리·창제 정신',['제자','초성 17자','초성 제자','창제 정신','중성:','종성: 초성','훈민정음 모음','자음 체계와 모음 체계']),
('M-BANGJEOM','중세국어','방점·성조',['방점','성조']),
('M-DONGGUK','중세국어','동국정운식 한자음',['동국정운']),
('M-HONOR','중세국어','주체 높임 선어말 어미',['높임']),
('M-MEANING','중세국어','어휘 의미 변화(확대·축소·이동)',['의미 변화','어엿비','여름(열매)','놈의','어휘 의미','단어 의미']),
('M-MORPH','중세국어','명사형 어미/파생 접미사·용언 활용·향찰·접두사 이형태',['명사형 어미','용언 활용','향찰','접두사의 통시','어절 형태소 분석','기본형이 같은 용언','보조사와 격조사의 결합','합성어 분류',"'-기'","'-하다' 파생"]),
('M-SYNTH','중세국어','중세→현대 종합·감상·해석·출제 구성',['중세→현대','종합 오설명','현대어 풀이','용비어천가','중세 국어 특징 종합','시험 출제 구성','국어의 역사성','교과서보다 나아간','교과서 밖']),
('O-CHIK','맞춤법','총칙(소리대로/어법)·단어 수',['총칙','제1항','소리대로','1·2항','표음','표의','단어 수','제2항','혼동 어휘']),
('O-DOEN','맞춤법','된소리(제5항)·형태소 경계 된소리',['제5항','된소리: ','된소리 표기','형태소 경계의 된소리','된소리를 음운']),
('O-GUGAE','맞춤법','구개음화·ㄷ 소리 받침(제6~7항)',['제6항','제7항','닫히다']),
('O-DUEUM','맞춤법','두음 법칙·렬/률(제10~12항)',['렬·률','률/렬','두음 법칙 본음','두음법칙','제10~12']),
('O-WONHYUNG','맞춤법','원형 밝히기·-이/-히·부사·명사 파생(제19~25·51·54~57항)',['제19','-이/-히','명사 파생','제25','제51','반듯이','제15항','제27항','제53','제57','어미·접미사','제19~25','동음이의','조리다','굳이','제6항·제7항·제28항']),
('O-SAISIOT','맞춤법','사이시옷(제30항)',['사이시옷','한자어+한자어 합성어']),
('O-JUNMAL','맞춤법','준말·되/돼·불규칙 표기(제34~40항·제18항)',['준말','제40항','되/돼','제34','제36','불규칙 활용','‘하’ 준말']),
('O-SPACE','맞춤법','띄어쓰기(조사·의존 명사·보조 용언·단위)',['띄어쓰기','데/지','만큼, 대로','안되다','단위를 나타내는','단위 명사']),
('O-DEON','맞춤법','-던/-든·-던지/-든지 등 혼동 어미',['-던/-든','제56항','던 vs']),
('O-PHON','음운·표준 발음','음운 변동·표준 발음법',['비음화','음운 변동','발음','된소리되기','겹받침','ㄹ 관련','동화','모음 탈락','축약','음성 인식','자음군 단순화','변동','음운 규칙의 적용 순서']),
('O-META','공통','복합 규정 판단·문항 형식 메타·서술형',['복합','규정 조항','문항 형식','신어','순화','종합: 선지','판단 2건','보기에서 비음화','보기에 제시','음운 개수','문제 형식']),
]
def cluster(e):
    c=str(e['concept'])
    for cid,unit,name,keys in CL:
        if any(k in c for k in keys): return cid
    return None
G=collections.defaultdict(list); un=[]
for e in ents:
    cid=cluster(e)
    (G[cid] if cid else un).append(e)

assert not un, [(e['_src'],e['id'],e['concept']) for e in un]
KM={'SURFACE_SIMILARITY':['KM15','KM01','KM11'],'EXCEPTION_RULE':['KM09'],'TIME_SCOPE':['KM03'],'CATEGORY_SWAP':['KM04'],'COUNTING':['KM12'],'RULE_DIRECTION':['KM08'],'MULTI_CONDITION':['KM07'],'TERM_CONFUSION':['KM04'],'OTHER':[]}
def lvl(e):
    k=e.get('killer_level')
    return int(k) if isinstance(k,(int,float,str)) and str(k).isdigit() else 0
out=[]
for cid,unit,name,keys in CL:
    es=G.get(cid,[])
    bysrc=collections.Counter(e['_src'] for e in es)
    k3=sum(1 for e in es if lvl(e)==3)
    kmax=max([lvl(e) for e in es] or [0])
    bfreq=collections.Counter(str(e.get('frequency')) for e in es if e['_src']=='B')
    cemp=collections.Counter(str(e.get('school_emphasis')) for e in es if e['_src']=='C')
    causes=collections.Counter(str(e.get('cause')) for e in es if e.get('cause'))
    morph=sum(1 for e in es if e.get('morpheme_analysis_needed') in (True,'true','True'))
    score=k3+bfreq.get('HIGH',0)+2*cemp.get('HIGH',0)
    def pick(field,n=3,order=None):
        seen=[];
        for e in sorted(es,key=lambda x:(-lvl(x),x['_src'])):
            v=e.get(field)
            if v and str(v) not in seen and str(v)!='NONE': seen.append(str(v))
            if len(seen)>=n: break
        return seen
    mis=[]
    for c,_ in causes.most_common(3):
        for m in KM.get(c,[]):
            if m not in mis: mis.append(m)
    if cid in ('M-MORPH','M-DONGHYUNG','O-WONHYUNG') or morph>=len(es)/2:
        for m in ('KM13','KM15'):
            if m not in mis: mis.append(m)
    if 'O-SAISIOT'==cid and 'KM07' not in mis: mis.append('KM07')
    scope='AUXILIARY' if cid=='O-PHON' else 'CORE'
    oos=sum(1 for e in es if e.get('out_of_scope') in (True,'true','True'))
    out.append({'cluster':cid,'unit':unit,'scope':scope,'out_of_scope_entries':oos,'name':name,'entries':len(es),'by_source':dict(bysrc),
      'killer3_entries':k3,'killer_max':kmax,'frequency_B':dict(bfreq),'school_emphasis_C':dict(cemp),
      'priority_score':score,'dominant_causes':[c for c,_ in causes.most_common(3)],
      'morpheme_analysis_share':f"{morph}/{len(es)}",
      'top_confusions':pick('confusion',4),'distractor_patterns':pick('distractor_pattern',3) or pick('killer_structure',2),
      'outside_textbook_variation':pick('outside_textbook_variation',2),'confusing_expression':pick('confusing_expression',2),
      'design_hints':(pick('design_hint',3)+pick('downscale_hint',2))[:4],'suggested_misconception_codes':mis,
      'raw_ids':[e['id'] for e in es]})
out.sort(key=lambda r:(r['scope']!='CORE',-r['priority_score'],-r['killer3_entries']))
def md(out,meta):
    L=['# 국어 헷갈림·킬러 지도 (공통국어2 3단원 중세 국어 + 한글 맞춤법)','','기계 판독본: `quality/exam_style/KOR_CONFUSION_AND_KILLER_MAP_V1.0.yaml`. 원본 분석 4개: `KOR_CONFUSION_RAW_{A,B,C,D}_*_20261109.yaml` (문항·해설 원문 없음, 구조와 이유만 기록).','','자료: A 킬러 세트 125문항 · B 빈출 세트 100문항 · C 학교 보충자료·국립국어원 해설 · D 모의고사급 문법(블랙라벨 일부). 총 원본 항목 '+str(meta['total_raw_entries'])+'개를 개념 28개 묶음으로 병합했다.','','한계: 학생 정답률 자료가 없어 킬러 정도는 문항 구조와 해설에서 추정한 값이다. A 는 킬러 세트라 높게 몰려 있다. 사이시옷·두음 법칙은 모의고사급(D)에서 검증하지 못했다.','','## 우선순위 (핵심 범위, 점수 = 킬러3 항목 수 + 빈출 HIGH 수 + 2×학교 강조 HIGH 수)','','| 순위 | 묶음 | 단원 | 점수 | 킬러3 | 출처(A/B/C/D) | 형태소 분석 필요 |','|---|---|---|---|---|---|---|']
    core=[r for r in out if r['scope']=='CORE']
    for i,r in enumerate(core,1):
        bs=r['by_source']; L.append(f"| {i} | {r['name']} | {r['unit']} | {r['priority_score']} | {r['killer3_entries']} | {bs.get('A',0)}/{bs.get('B',0)}/{bs.get('C',0)}/{bs.get('D',0)} | {r['morpheme_analysis_share']} |")
    L+=['','## 상위 묶음의 헷갈림 지점과 오답 설계','']
    for r in core[:10]:
        L.append(f"### {r['name']} ({r['cluster']}, 점수 {r['priority_score']})")
        L.append('- 헷갈림: '+' / '.join(r['top_confusions'][:3]))
        L.append('- 오답 설계: '+' / '.join(r['distractor_patterns'][:2]))
        L.append('- 낯선 단어·예문 변형: '+' / '.join(r['outside_textbook_variation'][:2]))
        L.append('- 설계 힌트: '+' / '.join(r['design_hints'][:3]))
        L.append('- 착각 코드 후보: '+', '.join(r['suggested_misconception_codes'])+' · 원인: '+', '.join(r['dominant_causes']))
        L.append('')
    aux=[r for r in out if r['scope']!='CORE']
    L+=['## 보조 범위(모의고사급, 3단원 직접 범위 아님)','']+[f"- {r['name']} ({r['cluster']}): 항목 {r['entries']}개, 킬러3 {r['killer3_entries']}개, 범위 밖 표시 {r['out_of_scope_entries']}개" for r in aux]
    L+=['','## 국어 v5 설계에 쓰는 법','','1. D4 후보는 점수가 높은 묶음에서 고른다(사이시옷, 띄어쓰기 품사 판별, 형태소 경계, 동형 어절 판별, ㅎ종성·ㄱ덧생김, 시기 판정).','2. 오답은 각 묶음의 헷갈림 지점과 착각 코드로 만든다(문항 judgment 의 mis 필드).','3. 교과서 밖 단어·예문은 묶음의 "낯선 단어·예문 변형" 방식으로 구성하고 novel_examples 에 기록한다.','4. 형태소 경계 분석이 필요한 묶음(형태소 분석 필요 비율이 높은 것)은 D4 의 morpheme_analysis 근거로 쓴다.','']
    open(D+'KOR_CONFUSION_AND_KILLER_MAP_V1.0.md','w',encoding='utf-8').write('\n'.join(L))
meta={'map_id':'ARC_KOR_CONFUSION_AND_KILLER_MAP_V1.0','version':1.0,'date':'2026-11-09','status':'ACTIVE_DEV','decision':'D-25/D-26',
 'unit':'공통국어2 3단원 국어의 어제와 오늘 (중세 국어 + 한글 맞춤법) + 표준 발음/음운 보조',
 'sources':{'A':'족보닷컴 최다오답공략 4세트 + 최상위공략 3세트 (7세트 125문항, 인라인 해설)','B':'족보닷컴 최다빈출공략 5세트 (100문항, 해설)','C':'동북고 보충자료(스캔 9쪽)·시범 10쪽(제3자 노트)·직전대비 안내·국립국어원 해설(일부)','D':'블랙라벨 문법 초고난도(앞부분 약 17만 자 OCR)'},
 'limits':['학생 정답률 자료가 없다. killer_level 은 문항 구조·해설에서 추정한 값이다.','A 의 killer_level 은 킬러 세트 자체 특성 때문에 높게 몰려 있어 B·C 와 상대 비교해야 한다.','옛한글·방점·선지 번호 소실로 중세 어형 분석 일부는 추정이다.','사이시옷·두음 법칙은 A·B·C 에서 확인, D(모의고사급)에서는 검증 못 했다.','2027 바탕 언어와 매체 PDF 는 텍스트가 없어 분석하지 못했다.'],
 'priority_score_def':'killer_level 3 항목 수 + 빈출 HIGH 항목 수 + 2×학교 강조 HIGH 항목 수','raw_files':list(SRC.values()),'total_raw_entries':len(ents)}
yaml.safe_dump({'meta':meta,'clusters':out},open(D+'KOR_CONFUSION_AND_KILLER_MAP_V1.0.yaml','w',encoding='utf-8'),allow_unicode=True,sort_keys=False,width=200)
print(len(out)); md(out,meta)

for r in out[:12]: print(r['priority_score'],r['cluster'],r['name'],r['by_source'],r['killer3_entries'])
