#!/bin/sh
# 빌드 → PDF 3종 → 합본(문제지+정답표). 해설은 별도 PDF (ARC 규칙: 문제지와 답지는 항상 함께, 해설은 따로)
set -e
cd "$(dirname "$0")"
V=V1.2
O=..
python3 build_n11.py
NODE_PATH="${NODE_PATH:-$(npm root -g)}" node pdf.js "$O/ARC_N11_공통국어2_시험범위11편_110Q_${V}.pdf" "$O/ARC_N11_공통국어2_정답표.pdf" "$O/ARC_N11_공통국어2_간단해설.pdf"
python3 ../../../../quality/tools/bundle_pdf.py "$O/ARC_N11_공통국어2_시험범위11편_110Q_${V}_문제지+답지.pdf" "$O/ARC_N11_공통국어2_시험범위11편_110Q_${V}.pdf" "$O/ARC_N11_공통국어2_정답표.pdf"
