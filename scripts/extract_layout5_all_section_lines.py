#!/usr/bin/env python3
import json,re
from pathlib import Path
p=Path('temp/布局锦囊5.0/index.md')
lines=p.read_text(encoding='utf-8-sig').splitlines()
rows=[]
for i in range(2290,min(len(lines),2485)):
    s=lines[i].strip()
    if '节' in s or re.match(r'^#{1,6}\s+',s):
        rows.append({'line':i+1,'text':s[:500]})
Path('temp/.layout5-all-section-lines.json').write_text(json.dumps({'count':len(rows),'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'count':len(rows)},ensure_ascii=False))
