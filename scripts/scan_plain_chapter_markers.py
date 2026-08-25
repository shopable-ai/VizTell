#!/usr/bin/env python3
import json,re
from pathlib import Path
PAT=re.compile(r'^\s*(第\s*[一二三四五六七八九十百零〇两0-9]+\s*(?:章|节|课|讲|篇|卷|册)(?![，,。；;：:])\s*.{0,90})\s*$')
rows=[]
for p in sorted(Path('temp').rglob('*.md')):
    if p.name.startswith('.'): continue
    for i,x in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
        if x.lstrip().startswith('#'): continue
        if PAT.match(x.strip()): rows.append({'path':str(p),'line':i,'text':x.strip()[:140]})
Path('temp/.plain-chapter-marker-review.json').write_text(json.dumps({'count':len(rows),'matches':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'count':len(rows)},ensure_ascii=False))
