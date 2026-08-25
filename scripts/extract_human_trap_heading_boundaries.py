#!/usr/bin/env python3
from __future__ import annotations
import json, re
from pathlib import Path

PATH = Path('temp/《人性陷阱》/index.md')
OUT = Path('temp/.human-trap-heading-boundaries.json')
INLINE = re.compile(r'(?<!\d)(\d{1,3})陷阱\s*(\d+)\s*[：:]\s*')
rows=[]
inline=[]
for i, raw in enumerate(PATH.read_text(encoding='utf-8-sig').splitlines(),1):
    if raw.startswith('## 陷阱'):
        text=raw[3:].strip()
        rows.append({'line':i,'length':len(text),'text':text[:600]})
    for m in INLINE.finditer(raw):
        inline.append({
            'line': i,
            'page_prefix': m.group(1),
            'trap_no': m.group(2),
            'before': raw[max(0,m.start()-100):m.start()],
            'after': raw[m.end():m.end()+400],
        })
payload={
    'count':len(rows),
    'overlong':[r for r in rows if r['length']>80],
    'inline_page_prefixed_traps': inline,
    'all':[{'line':r['line'],'length':r['length'],'text':r['text'][:180]} for r in rows]
}
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'count':len(rows),'overlong':sum(r['length']>80 for r in rows),'inline_page_prefixed_traps':len(inline)},ensure_ascii=False))
