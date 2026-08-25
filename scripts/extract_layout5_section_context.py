#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
PATH=Path('temp/布局锦囊5.0/index.md')
OUT=Path('temp/.layout5-section-context.json')
lines=PATH.read_text(encoding='utf-8-sig').splitlines()
pat=re.compile(r'^\s*(第\s*[一二三四五六七八九十0-9]+\s*节[^\n]{0,120})$')
rows=[]
for i,line in enumerate(lines,1):
    if pat.match(line.strip()) and not line.lstrip().startswith('#'):
        prev=[]; nxt=[]
        for j in range(max(0,i-6),i-1):
            s=lines[j].strip()
            if s: prev.append({'line':j+1,'text':s[:220]})
        for j in range(i,min(len(lines),i+6)):
            s=lines[j].strip()
            if s: nxt.append({'line':j+1,'text':s[:220]})
        rows.append({'line':i,'text':line.strip(),'previous':prev[-4:],'next':nxt[:4]})
# Also capture all existing headings in the surrounding 2200-2480 region.
headings=[{'line':i,'text':line.strip()} for i,line in enumerate(lines,1) if 2200<=i<=2480 and re.match(r'^#{1,6}\s+',line.strip())]
OUT.write_text(json.dumps({'markers':rows,'surrounding_headings':headings},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'markers':len(rows),'surrounding_headings':len(headings)},ensure_ascii=False))
