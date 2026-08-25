#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
p=Path('temp/《玩转人性》.md')
lines=p.read_text(encoding='utf-8-sig').splitlines()
heads=[]
current='（书首）'
rows=['line\tmajor\tno\ttext']
major_pat=re.compile(r'^#{2,6}\s+(玩转.+?)\s*$')
number_pat=re.compile(r'^\s*(\d{1,2})\s*[．.]\s*(.+)$')
inline_pat=re.compile(r'(?<!\d)(\d{1,2})\s*[．.]\s*([^\n]{4,120})')
inline=[]
for i,s in enumerate(lines,1):
    stripped=s.strip()
    m=major_pat.match(stripped)
    if m:
        current=m.group(1)
        heads.append({'line':i,'heading':stripped,'major':current})
        continue
    m=number_pat.match(stripped)
    if m and not stripped.startswith('#'):
        rows.append(f'{i}\t{current}\t{m.group(1)}\t{m.group(2).replace(chr(9)," ")[:220]}')
    if stripped.startswith(('#','![')): continue
    for x in inline_pat.finditer(s):
        if x.start()==0: continue
        inline.append({'line':i,'major':current,'no':x.group(1),'before':s[max(0,x.start()-120):x.start()],'after':x.group(2)[:180]})
Path('temp/.play-humanity-structure.json').write_text(json.dumps({'headings':heads,'inline_numbered':inline},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
Path('temp/.play-humanity-numbered-review.tsv').write_text('\n'.join(rows)+'\n',encoding='utf-8')
print(json.dumps({'major_headings':len(heads),'line_start_numbered':len(rows)-1,'inline_numbered':len(inline)},ensure_ascii=False))
