# ARC VISUAL RENDERER POLICY V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV

## PURPOSE
정확도가 필요한 평가용 시각자료를 LLM의 자유형 그림 생성에서 분리한다.
기본 파이프라인은 `VISUAL_SPEC → deterministic renderer → PASS A → independent PASS B`다.

## RENDERER ROUTING
- SCI-GRAPH: matplotlib 또는 동등한 수치 기반 SVG/PDF renderer
- SCI-PARTICLE: ARC deterministic SVG particle renderer
- SCI-EXPERIMENT: explicit element/connection spec → draw.io/structured SVG
- SCI-PROCESS: draw.io/structured SVG
- chemical structure: ChemCP/검증된 chemistry renderer
- timeline: timeline renderer/structured SVG
- SOC-DATA / SOC-STAT: matplotlib/table renderer
- SOC-FLOW / SOC-INSTITUTION / SOC-COMPARE / SOC-CASEBOX: structured SVG/draw.io
- SOC-MAP: verified vector base + explicit region overlay only
- HIS-TIMELINE: timeline renderer
- HIS-MAP / HIS-ORG: verified vector base or draw.io/structured SVG

## GENERATIVE IMAGE RULE
생성형 이미지 모델은 축·수치·입자 개수·지도 경계·실험 연결·연표 순서 등 정답에 영향을 주는 자료의 기본 renderer로 사용하지 않는다.
장식성 이미지가 정말 필요한 경우에만 비핵심 자산으로 허용하며, 학생의 정답 추론 근거가 되어서는 안 된다.

## REQUIRED OUTPUT
모든 deterministic render는:
- source VISUAL_SPEC
- rendered asset
- RENDER_MANIFEST
- renderer name/version
- spec hash
- semantic element counts/data
를 남긴다.

## FALLBACK
전용 renderer가 없으면 임의로 그림을 생성하지 않는다.
1) draw.io/structured SVG로 표현 가능하면 전환
2) 표로 바꿔도 평가 의도가 유지되는 경우에만 DATA_TABLE로 재설계
3) 아니면 ASSET_RENDER_BLOCKED

## RELEASE
필수 TRUE_VISUAL은 ARC_VISUAL_PASS_AB_V1.0의 PASS A/B와 QUESTION_VISUAL_CROSSCHECK가 모두 PASS여야 BANK/FINAL 후보가 된다.

END ARC VISUAL RENDERER POLICY V1.0
