import sys; sys.path.insert(0, "/home/user/ARC-System/works")
import arc_build as ab
import os
base = "/home/user/ARC-System/works/C"; out_dir = "/home/user/ARC-System/output"
m1 = dict(no="11", title="C파트 · 인권 · 헌법 · 제도 FINAL 50", school="동북고등학교 1학년",
          range="인권의 의미와 확장 · 헌법과 기본권 · 인권 보장을 위한 제도적 장치와 시민 참여",
          head_right="통합사회2 · C파트 FINAL 50", answer_sub="ARC N°11 · C파트 FINAL 50 · 정답표",
          concept_sub="각 개념 상자 오른쪽 아래의 번호는 그 개념을 다룬 문항입니다.")
m2 = dict(no="12", title="C파트 SPECIAL 20 · 기본권 제한과 권력 견제", school="동북고등학교 1학년",
          range="기본권 제한의 한계(제37조 제2항) · 권력 분립의 실질적 기능 · 헌법재판소와 권리 구제",
          head_right="통합사회2 · C파트 SPECIAL 20", answer_sub="ARC N°12 · C파트 SPECIAL 20 · 정답표",
          concept_sub="문항 번호(S)는 해당 개념을 다룬 스페셜 문항입니다.")
parts = [open(f"{base}/_parts/p{i}.txt", encoding="utf-8").read() for i in (1, 2, 3)]
open(f"{base}/main.txt", "w", encoding="utf-8").write("\n".join(parts))
cf1 = [x for x in ("C_C", "C_C2", "C_C3") if os.path.exists(f"{base}/fig/{x}.svg")] or None
cf2 = ["C_CS"] if os.path.exists(base + "/fig/C_CS.svg") else None
p1, n1 = ab.build_all(base, "ARC_N11_통합사회2_C파트_FINAL50_V1.0.pdf", m1, "main.txt", out_dir, concept_fig=cf1)
p2, n2 = ab.build_all(base, "ARC_N12_통합사회2_C파트_SPECIAL20_V1.0.pdf", m2, "special.txt", out_dir, concept_fig=cf2)
print(p1, n1); print(p2, n2)
