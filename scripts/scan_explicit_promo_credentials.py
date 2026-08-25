#!/usr/bin/env python3
from __future__ import annotations
import json, re
from pathlib import Path

OUT=Path('temp/.explicit-promo-credential-review.json')
PATTERNS={
  'contact_account': re.compile(r'(?i)(?:微信|微信号|微芯|薇芯|薇信|V信|VX|WX)\s*[:：号]?\s*([A-Za-z][A-Za-z0-9_-]{4,}|\d{6,})'),
  'more_materials': re.compile(r'更多(?:资料|内容|落地细节|布局秘密)[^。！？\n]{0,40}(?:加|添加|关注|联系)[^。！？\n]{0,35}'),
  'public_account': re.compile(r'(?:公号|公众号)\s*[:：]\s*[^，。；！？\s]{2,40}'),
  'direct_cta': re.compile(r'(?:添加作者|加作者|扫码添加|扫码关注)[^。！？\n]{0,45}'),
}
rows=[]
for path in sorted(Path('temp').rglob('*.md')):
    if path.name.startswith('.'):
        continue
    text=path.read_text(encoding='utf-8-sig')
    lines=text.splitlines()
    for i,line in enumerate(lines,1):
        for kind,pat in PATTERNS.items():
            for m in pat.finditer(line):
                rows.append({
                    'path':str(path),'line':i,'kind':kind,'match':m.group(0),
                    'context':line[max(0,m.start()-100):m.end()+140]
                })
OUT.write_text(json.dumps({'count':len(rows),'matches':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'count':len(rows),'files':len(set(x['path'] for x in rows))},ensure_ascii=False))
