"""Prepare embeddable static fonts for the ARC CORE build.
- Pretendard: TrueType-outline static weights (400/500/600/700) so Chromium embeds them as TrueType, not Type3.
- Noto Sans KR (Hanja/Hangul fallback): files are static wght=400 but their name table still says 'Thin';
  rewrite the name table to 'Noto Sans KR' / 'Regular' so the embedded font name matches the real weight.
"""
import glob, os, shutil, sys
from fontTools.ttLib import TTFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = sys.argv[1]  # node_modules/pretendard
pre = os.path.join(ROOT, 'fonts', 'pretendard')
for f in glob.glob(pre + '/*.otf'): os.remove(f)
for w in ['Regular', 'Medium', 'SemiBold', 'Bold']:
    shutil.copy(f'{PKG}/dist/public/static/alternative/Pretendard-{w}.ttf', pre)
noto = os.path.join(ROOT, 'fonts', 'notosanskr', 'files')
n_fixed = 0
for f in glob.glob(noto + '/*.woff2'):
    t = TTFont(f)
    assert t['OS/2'].usWeightClass == 400, f
    for rec in t['name'].names:
        if rec.nameID in (1, 16): rec.string = 'Noto Sans KR'
        elif rec.nameID in (2, 17): rec.string = 'Regular'
        elif rec.nameID == 4: rec.string = 'Noto Sans KR Regular'
        elif rec.nameID == 6: rec.string = 'NotoSansKR-Regular'
        elif rec.nameID == 3: rec.string = 'NotoSansKR-Regular-ARC'
    t.flavor = 'woff2'
    t.save(f); n_fixed += 1
print('pretendard:', sorted(os.listdir(pre)), '| noto renamed:', n_fixed)
