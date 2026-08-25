#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
p=Path('temp/《玩转人性》.md')
lines=p.read_text(encoding='utf-8-sig').splitlines()
heads=[]
for i,s in enumerate(lines,1):
    if re.match(r'^#{1,6}\s+',s.strip()):
        prev=next((lines[j].strip()[:180] for j in range(i-2,max(-1,i-6),-1) if lines[j].strip()),'') if i>=2 else ''
        nxt=next((lines[j].strip()[:180] for j in range(i,min(len(lines),i+5)) if lines[j].strip()),'') if i<len(lines) else ''
        heads.append({'line':i,'heading':s.strip(),'previous':prev,'next':nxt})
# Capture numbered section markers anywhere in prose, not ordinary list items that are already separated.
pat=re.compile(r'(?<!\d)(\d{1,2})\s*[．.]\s*([^\n]{4,90})')
inline=[]
for i,s in enumerate(lines,1):
    if s.lstrip().startswith(('#','![')): continue
    for m in pat.finditer(s):
        inline.append({'line':i,'no':m.group(1),'after':m.group(2)[:120],'before':s[max(0,m.start()-120):m.start()]})
Path('temp/.play-humanity-structure.json').write_text(json.dumps({'headings':heads,'inline_numbered':inline},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'headings':len(heads),'inline_numbered':len(inline)},ensure_ascii=False))
