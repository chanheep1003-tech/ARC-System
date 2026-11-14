"""Old Hangul (conjoining jamo clusters) support for the Korean renderer.

PyMuPDF draws code points one by one and cannot shape conjoining jamo. This module shapes every
old-Hangul cluster that occurs in a bundle with HarfBuzz (Noto Sans CJK KR), copies the composed glyph
outline into a small generated TrueType font and maps the cluster to a private-use code point.
runs() in kor_renderer swaps clusters for those code points and draws them with font key "O".
"""
from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

NOTO = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
KR_INDEX = 1
PUA0 = 0xF0000  # supplementary private use area A
CLUSTER = re.compile("[ᄀ-ᅟꥠ-ꥼ]+[ᅠ-ᆧힰ-ퟆ]+[ᆨ-ᇿퟋ-ퟻ]*"
                     "|[ᅠ-ᆧ]+[ᆨ-ᇿ]*")
_MAP: dict[str, str] = {}
_FONT_PATH: Path | None = None


def _is_modern(c: str) -> bool:
    import unicodedata
    return len(unicodedata.normalize("NFC", c)) == 1 and 0xAC00 <= ord(unicodedata.normalize("NFC", c)) <= 0xD7A3


def clusters(text: str) -> set[str]:
    return {m for m in CLUSTER.findall(text) if not _is_modern(m)}


def encode(text: str) -> str:
    if not _MAP:
        return text
    return CLUSTER.sub(lambda m: _MAP.get(m.group(), m.group()), text)


def is_old_char(ch: str) -> bool:
    return PUA0 <= ord(ch) < PUA0 + 0x4000


def prepare(obj) -> Path | None:
    """Scan any JSON-able bundle, build the font once for all clusters found."""
    global _FONT_PATH
    found = clusters(json.dumps(obj, ensure_ascii=False))
    if not found:
        return _FONT_PATH
    if set(_MAP) >= found and _FONT_PATH:
        return _FONT_PATH
    import uharfbuzz as hb
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.ttLib import TTCollection

    allc = sorted(found | set(_MAP))
    tt = TTCollection(str(NOTO)).fonts[KR_INDEX]
    gs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    face = hb.Face(hb.Blob.from_file_path(str(NOTO)), KR_INDEX)
    hbf = hb.Font(face)
    names, glyphs, metrics, cmap = [".notdef"], {}, {".notdef": (1000, 0)}, {}
    pen = TTGlyphPen(None)
    glyphs[".notdef"] = pen.glyph()
    for i, c in enumerate(allc):
        cp = PUA0 + i
        _MAP[c] = chr(cp)
        buf = hb.Buffer()
        buf.add_str(c)
        buf.guess_segment_properties()
        hb.shape(hbf, buf)
        pen = TTGlyphPen(gs)
        x = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            tp = TransformPen(Cu2QuPen(pen, 1.0, reverse_direction=True), (1, 0, 0, 1, x + pos.x_offset, pos.y_offset))
            gs[order[info.codepoint]].draw(tp)
            x += pos.x_advance
        gname = f"uni{cp:X}"
        names.append(gname)
        glyphs[gname] = pen.glyph()
        metrics[gname] = (x, 0)
        cmap[cp] = gname
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=880, descent=-120)
    fb.setupNameTable({"familyName": "ArcOldHangul", "styleName": "Regular"})
    fb.setupOS2(sTypoAscender=880, sTypoDescender=-120, usWinAscent=880, usWinDescent=120)
    fb.setupPost()
    out = Path(tempfile.gettempdir()) / f"ArcOldHangul_{abs(hash(tuple(allc))) % 10**8}.ttf"
    fb.save(str(out))
    _FONT_PATH = out
    return out


def font_path() -> Path | None:
    return _FONT_PATH
