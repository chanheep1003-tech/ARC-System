#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
SKILLS=ROOT/'skills'
errors=[]
names=[]
for p in sorted(SKILLS.glob('*/SKILL.md')):
    text=p.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        errors.append(f'{p}: missing frontmatter')
        continue
    m=re.search(r'^name:\s*([^\n]+)', text, re.M)
    d=re.search(r'^description:\s*[\'\"](.+?)[\'\"]$', text, re.M)
    if not m: errors.append(f'{p}: missing name'); continue
    name=m.group(1).strip()
    names.append(name)
    if name != p.parent.name: errors.append(f'{p}: name/folder mismatch')
    if not re.fullmatch(r'[a-z0-9-]{1,64}',name): errors.append(f'{p}: invalid name')
    if not d: errors.append(f'{p}: missing quoted description')
    lines=len(text.splitlines())
    if lines>500: errors.append(f'{p}: >500 lines ({lines})')
if len(names)!=len(set(names)): errors.append('duplicate skill names')
registry=(SKILLS/'SKILL_REGISTRY.yaml').read_text(encoding='utf-8')
for name in names:
    if f'  {name}:' not in registry: errors.append(f'{name}: missing registry entry')
# Ensure removed learner-adaptive feature is not accidentally enabled.
for bad in ['learner_adaptive_retry: enabled','personal_weakness_tracking: enabled']:
    if bad in registry: errors.append(f'forbidden feature enabled: {bad}')
print(f'skills={len(names)}')
if errors:
    print('FAIL')
    for e in errors: print('-',e)
    sys.exit(1)
print('PASS')
