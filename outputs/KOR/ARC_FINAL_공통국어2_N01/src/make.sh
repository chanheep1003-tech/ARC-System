#!/bin/sh
# 빌드 → 문제지·정답 및 채점 기준 PDF → 합본(문제지+답지). 규칙: quality/ARC_PAIRED_DELIVERY_V1.0.md
set -e
cd "$(dirname "$0")"
V=V1.2
O=..
python3 build_final.py
NODE_PATH="${NODE_PATH:-$(npm root -g)}" node pdf.js "$O/ARC_FINAL_공통국어2_N01_${V}.pdf" "$O/ARC_FINAL_공통국어2_N01_정답및채점기준.pdf"
python3 ../../../../quality/tools/bundle_pdf.py "$O/ARC_FINAL_공통국어2_N01_${V}_문제지+답지.pdf" "$O/ARC_FINAL_공통국어2_N01_${V}.pdf" "$O/ARC_FINAL_공통국어2_N01_정답및채점기준.pdf"
