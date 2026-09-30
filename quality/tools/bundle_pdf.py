#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""문제지 + 정답표 + 해설(채점기준)을 한 PDF로 묶는다. (ARC 규칙: 문제지와 답지는 항상 함께 조판·제공)
usage: bundle_pdf.py OUT.pdf 문제지.pdf 정답표.pdf [해설.pdf ...]
- 각 파일 시작 페이지에 PDF 책갈피(목차)를 넣는다.
- 문제지가 홀수 쪽이면 정답표가 새 낱장에서 시작하도록 백지 1쪽을 넣는다."""
import sys, pymupdf

def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    out, srcs = sys.argv[1], sys.argv[2:]
    labels = ["문제지", "정답표", "해설"]
    doc = pymupdf.open(); toc = []
    for i, p in enumerate(srcs):
        s = pymupdf.open(p)
        if i > 0 and doc.page_count % 2 == 1:
            doc.new_page(width=s[0].rect.width, height=s[0].rect.height)
        toc.append([1, labels[i] if i < len(labels) else f"부록{i}", doc.page_count + 1])
        doc.insert_pdf(s)
    doc.set_toc(toc)
    doc.save(out, garbage=3, deflate=True)
    print(f"bundled {len(srcs)} files -> {out} ({doc.page_count} pages)")

if __name__ == "__main__":
    main()
