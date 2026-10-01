import sys; sys.path.insert(0, "/home/user/ARC-System/works")
import arc_build as ab
base = "/home/user/ARC-System/works/A"
out_dir = "/home/user/ARC-System/output"
m1 = dict(no="07", title="A파트 · 정의와 사고방식 FINAL 50", school="동북고등학교 1학년",
          range="정의의 의미와 필요성 · 정의의 실질적 기준 · 『생각의 지도』 p.156~233",
          head_right="통합사회2 · A파트 FINAL 50",
          answer_sub="ARC N°07 · A파트 FINAL 50 · 정답표",
          concept_sub="각 개념 상자 오른쪽 아래의 번호는 그 개념을 다룬 문항입니다.")
p1, n1 = ab.build_all(base, "ARC_N07_통합사회2_A파트_FINAL50_V1.0.pdf", m1, "main.txt", out_dir, concept_fig=["C_A", "C_A2"])
m2 = dict(no="08", title="A파트 SPECIAL 20 · 칸트와 베카리아의 사형 논쟁", school="동북고등학교 1학년",
          range="정의의 실질적 기준 · 교정적 정의: 사형제도 탐구 (칸트·베카리아)",
          head_right="통합사회2 · A파트 SPECIAL 20",
          answer_sub="ARC N°08 · A파트 SPECIAL 20 · 정답표",
          concept_sub="문항 번호는 해당 개념을 다룬 문항입니다.")
p2, n2 = ab.build_all(base, "ARC_N08_통합사회2_A파트_SPECIAL20_V1.0.pdf", m2, "special.txt", out_dir, concept_fig=["C_S"])
print(p1, n1); print(p2, n2)
