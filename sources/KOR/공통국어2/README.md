# 공통국어2 지문 라이브러리

출제용 원문 텍스트를 한 번 확정해 두는 곳. **새 N제/CORE 작업 시 Drive에서 재추출하지 말고 여기서 import.**

| 모듈 | 변수 | 작품 | 형태 |
|---|---|---|---|
| `unit1.py` | `JMG` | 월명사, 「제망매가」(김완진 해독) | 행 list |
| | `SMI`, `SMI_NOTES` | 정철, 「속미인곡」 | 연 list[list] (48행) |
| | `CHH_PRE`, `CHH`, `CHH_NOTES` | 「춘향전」(교과서 수록 전체) | 앞 줄거리 + 문단 list |
| | `SURA`, `SURA_NOTES` | 백석, 「수라」 | 연 list[list] (12행) |
| | `GU_PRE`, `GU`, `GU_NOTES` | 윤흥길, 「아홉 켤레의 구두로 남은 사내」 | (가)~(라) 발췌 + 중략 줄거리 |
| `unit2.py` | `ESSAY`(+`ESSAY_*`) | 소민이의 논증하는 글 「반려견 보호자 자격시험을 의무화하자」(교과서 2단원 01) | 문단 list + 개념·계획·자료·개요·주석 |
| | `NEGO`(+`NEGO_*`) | 고속 철도 공사 협상 대화 「우리 학교 아래로 고속 철도가 지나간다고?」(2단원 02) | (단계, 화자, 발언, 여백주석) list + 입장·합의안·쟁점 |
| `supplement4.py` | `TAN_*` | 정훈, 「탄궁가」 | 행 list |
| | `PAL_*` | 백석, 「팔원」 | 행 list |
| | `MEM_*` | 기형도, 「기억할 만한 지나침」 | 연 list[list] |
| | `KANT_*`, `EXTRA_MATERIAL` | 이행남, 칸트·헤겔 자유 + 보충 해설문 | 문단 list |

문단 표기: `@@LAB@@(가)` 라벨 · `@@SUM@@` 줄거리 박스 · `@@VERSE@@a|b` 삽입 운문. HTML 태그(`<b>`) 포함 가능.

## 사용
```python
import sys; sys.path.insert(0, "sources/KOR/공통국어2")   # 저장소 루트 기준
from unit1 import SMI, SMI_NOTES
```
사람이 읽는 판본: `md/` (작품별 + `_ALL_…md` 통합본). 모듈 수정 후 `python3 export_md.py`로 재생성.

## 출처·주의
- 교과서 PDF(Drive `17bdR-sY3W1Rl770yp1Q2cCZrNAmMNjFo`, 교사용)는 본문 텍스트층이 없어 추출 불가.
- 1단원 원문: Drive `ARC_공통국어2_1단원_N제50_학생용.md`(`1jNYWqJ0VZXrB5NPo3DxWI6CbjPrFmRBN`) + 2025 기출(`1bNw6j5elzsIqWjaR3hG9dRmCEJtMoIK5`).
- 속미인곡 아래아 일부(ᄌᆞᆷ결의, ᄎᆞᆯ하리, ᄉᆡᆼ각, ᄇᆞᆰ앗ᄂᆞᆫ고, ᄒᆞ돗ᄯᅥᆫ디)는 원자료 깨짐으로 복원한 것 — 교과서 대조 전까지 [미검증].
- 2단원(`unit2.py`): 교과서 PDF 본문 글꼴이 깨져 **페이지 이미지 시각 전사**함 → 전 항목 [미검증], 교과서 대조 시 수정. 학습활동(p79~83, p94~99)·개념 영상 등은 미수록.
- 보충자료 4편: ARC N°06~09에서 사용한 확정본(N°09 기준).

## Drive 사본 (폴더 `ARC_지문라이브러리_공통국어2` · `1n5ZBALgxepDFrwXFS5yRiSCIsb3HQz6y`)
업로드 시 로컬 md와 바이트 크기 일치 확인 완료(2026-09-26).

| 파일 | Drive ID |
|---|---|
| 1단원_01_제망매가.md | `13aDdyppI70swNYroiVwO3iIjSKD7CfNr` |
| 1단원_02_속미인곡.md | `134BxAdmA09CH-m7fvauAQxtlhLyZSH3j` |
| 1단원_03_춘향전.md | `1AlO7AGHLIbgdJNr5p-hWQi-QLjGXzpbq` |
| 1단원_04_수라.md | `1mUxoZQ4CgwxPwUfVPMrJqkNb30pKUAzG` |
| 1단원_05_아홉켤레의구두로남은사내.md | `1tTY6xKXHo2Y74WO2b8qRfA0UCnJ6xvLc` |
| 2단원_01_논증하는글쓰기_반려견자격시험.md | `1RXHjf9cwZ5wHFwd5qQZnGTXkQeucS-ck` |
| 2단원_02_지혜롭게협상하기_고속철도.md | `1a7ccnKY4BNWRuhWoduT6sh0KFn14Lo7q` |
| 보충_01_탄궁가.md | `1uBEsT4vgkWyh-OzD-z7d1JoiZnLd54C3` |
| 보충_02_팔원.md | `1p-Ji4U8zJrrBQYxMe9Sy_i6Qkvdb3QeU` |
| 보충_03_기억할만한지나침.md | `1E6-HZ6bGhbzG44vm0uLTlrLyAAuoLKl9` |
| 보충_04_칸트헤겔자유.md | `1byOHoB3DiIlM3LWrV6THPTn1LGeaaKSL` |

원문 수정 시: 모듈 수정 → `export_md.py` → 해당 Drive 파일 갱신(update_file) → 이 표 유지.
