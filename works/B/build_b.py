import sys; sys.path.insert(0, "/home/user/ARC-System/works")
import arc_build as ab
base = "/home/user/ARC-System/works/B"; out_dir = "/home/user/ARC-System/output"
m1 = dict(no="09", title="B파트 · 세계화와 인구 FINAL 50", school="동북고등학교 1학년",
          range="세계화의 다양한 양상과 문제 해결 · 인구 문제와 미래 사회",
          head_right="통합사회2 · B파트 FINAL 50", answer_sub="ARC N°09 · B파트 FINAL 50 · 정답표",
          concept_sub="각 개념 상자 오른쪽 아래의 번호는 그 개념을 다룬 문항입니다.")
m2 = dict(no="10", title="B파트 SPECIAL 20 · 인구 구조와 인구 변천", school="동북고등학교 1학년",
          range="인구 구조 · 인구 변천 모형 · 인구 지표(부양비·고령화 지수·합계 출산율)",
          head_right="통합사회2 · B파트 SPECIAL 20", answer_sub="ARC N°10 · B파트 SPECIAL 20 · 정답표",
          concept_sub="문항 번호는 해당 개념을 다룬 문항입니다.")
import os
cf1 = ["C_B", "C_B2"] if os.path.exists(base + "/fig/C_B.svg") else None
cf2 = ["C_BS"] if os.path.exists(base + "/fig/C_BS.svg") else None
p1, n1 = ab.build_all(base, "ARC_N09_통합사회2_B파트_FINAL50_V1.0.pdf", m1, "main.txt", out_dir, concept_fig=cf1)
p2, n2 = ab.build_all(base, "ARC_N10_통합사회2_B파트_SPECIAL20_V1.0.pdf", m2, "special.txt", out_dir, concept_fig=cf2)
print(p1, n1); print(p2, n2)
