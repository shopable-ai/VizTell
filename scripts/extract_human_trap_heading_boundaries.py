#!/usr/bin/env python3
from __future__ import annotations
import json, re
from pathlib import Path

PATH = Path('temp/《人性陷阱》/index.md')
OUT = Path('temp/.human-trap-heading-boundaries.json')
rows=[]
for i, raw in enumerate(PATH.read_text(encoding='utf-8-sig').splitlines(),1):
    if raw.startswith('## 陷阱'):
        text=raw[3:].strip()
        rows.append({'line':i,'length':len(text),'text':text[:500]})
OUT.write_text(json.dumps({'count':len(rows),'overlong':[r for r in rows if r['length']>80],'all':[{'line':r['line'],'length':r['length'],'text':r['text'][:180]} for r in rows]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'count':len(rows),'overlong':sum(r['length']>80 for r in rows)},ensure_ascii=False))
