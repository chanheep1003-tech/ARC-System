"""Merge the A/B/C chapter sources into one ARC CORE book bundle (core_content.yaml)."""
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
PROD = HERE.parent


def unit_from_bundle(path: Path) -> dict:
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    u = d["units"][0]
    for i, s in enumerate(u["sections"], 1):
        no = s.pop("no", None) if "no" in s else s.pop(False, None)
        s["no"] = str(no or f"{i:02d}")
    return u


units = [
    unit_from_bundle(PROD / "SOC_CORE_A1_JUSTICE_20261123/core_content.yaml"),
    unit_from_bundle(PROD / "SOC_CORE_A2_INEQUALITY_20261123/core_content.yaml"),
]
for name in ["A3_peace", "B1_energy_future", "C1_minority_labor", "C2_market"]:
    units.append(yaml.safe_load((HERE / "parts" / f"{name}.yaml").read_text(encoding="utf-8")))

book = {
    "batch_id": "SOC_CORE_ABC_FINAL_20261123",
    "product_mode": "ARC_CORE",
    "subject": "SOC",
    "set_label": "ARC CORE",
    "course": "통합사회2",
    "cover_subtitle": "2학기 기말 A·B·C파트 전범위 개념서 (교과서 범위)",
    "school_line": "동북고등학교",
    "scope": "A: 44~61, 108~123쪽 / B: 134~151쪽 / C: 25~26, 64~83쪽 (학습지 제외)",
    "created_at": "2026-11-23T00:00:00+09:00",
    "status": "DRAFT_PREVIEW_NOT_RELEASABLE",
    "internal": {
        "exam_id": "DONGBUK_2026_2_FINAL",
        "user_directive": "A·B·C 한 권으로 묶기, 교과서 범위 중심, 학습지 제외, 심화·선지 분석·구조화, 1장 축소판 분량 기준",
        "sources_read": {
            "2과": ["19kx_qVzPh9WocFtsV6PZlnsmwh8mXxLJ", "1xoykPY1JnX0GwbCspEERHnPErcASGZnc"],
            "4과": ["1ATCS6zsYUfKjcvmEKSLAD8nFkz4KiBT3", "1W4j0t64sGgneWkR2TrjehjmyrEZF_HwS"],
            "5과": ["15ndRu8AYYhOeWIihqJm3KRZrEyt4r-v3", "1eP5YEvvG0NqJTxMz8sUmYnbgJELod70g"],
            "3과": ["1jmbFTvCu9z-1udSBMlIXQq8XjS5fBbFU", "1Ra8HTzm1pt383dWazRa1j_j9wImRJq1M"],
            "1과": ["1EluRfTGwEiW1flizdNHaji_RrdC4NYvS"],
        },
        "worksheet_used": False,
        "chapter_A1_status": "USER_APPROVED_DRIVE_SAVED_1R29jpxBxAPzEYjQ_u2pIxrMjz6M2jJan",
    },
    "units": units,
}
(HERE / "core_content.yaml").write_text(yaml.safe_dump(book, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
print("units", len(units), "sections", sum(len(u["sections"]) for u in units))
