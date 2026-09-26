# 공통국어2 지문 라이브러리

출제용 원문 텍스트를 한 번 확정해 두는 곳. **새 N제/CORE 작업 시 Drive에서 재추출하지 말고 여기서 import.**

| 모듈 | 변수 | 작품 | 형태 |
|---|---|---|---|
| `unit1.py` | `JMG` | 월명사, 「제망매가」(김완진 해독) | 행 list |
| | `SMI`, `SMI_NOTES` | 정철, 「속미인곡」 | 연 list[list] (48행) |
| | `CHH_PRE`, `CHH`, `CHH_NOTES` | 「춘향전」(교과서 수록 전체) | 앞 줄거리 + 문단 list |
| | `SURA`, `SURA_NOTES` | 백석, 「수라」 | 연 list[list] (12행) |
| | `GU_PRE`, `GU`, `GU_NOTES` | 윤흥길, 「아홉 켤레의 구두로 남은 사내」 | (가)~(라) 발췌 + 중략 줄거리 |
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
- 보충자료 4편: ARC N°06~09에서 사용한 확정본(N°09 기준).
