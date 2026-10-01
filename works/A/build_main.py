import sys; sys.path.insert(0, "/home/user/ARC-System/works")
import arc_build as ab
meta = dict(no="07", title="A파트 · 정의와 사고방식 FINAL 50", school="동북고등학교 1학년",
            range="정의의 의미와 필요성 · 정의의 실질적 기준 · 『생각의 지도』 p.156~233",
            head_right="통합사회2 · A파트 FINAL 50",
            answer_sub="ARC N°07 · A파트 FINAL 50 · 정답표",
            concept_sub="문항 번호는 해당 개념을 다룬 문항입니다.")
out, n = ab.build_all("/home/user/ARC-System/works/A", "ARC_N07_통합사회2_A파트_FINAL50_V1.0.pdf", meta, "main.txt", "/home/user/ARC-System/output", concept_fig=None)
print(out, n)
