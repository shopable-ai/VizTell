#!/usr/bin/env python3
from __future__ import annotations
import json, re
from collections import Counter, defaultdict
from pathlib import Path

OUT=Path('temp/.explicit-promo-token-summary.json')
CONTACT=re.compile(r'(?i)(?:微信|微信号|微芯|薇芯|薇信|V信|VX|WX)\s*[:：号]?\s*(?:[A-Za-z][A-Za-z0-9_-]{4,}|[1-9]\d{5,})')
# Known watermark/account names are extracted only when separated by an account marker.
PUBLIC_NAMES=['营销书刊','知识藏经阁','文字变现艺术家','顶层思维供应社','文字变现','知识藏经阁']
PUBLIC=re.compile(r'(?:公号|公众号)\s*[:：]\s*('+'|'.join(map(re.escape,PUBLIC_NAMES))+r')')
MORE=re.compile(r'更多资料加\s*信\s*[A-Za-z0-9_-]{4,}', re.I)
DIRECT=re.compile(r'(?:添加作者|加作者|扫码添加|扫码关注)\s*(?:微信|微芯|薇芯|薇信|V信|VX|WX)?\s*[:：号]?\s*(?:[A-Za-z][A-Za-z0-9_-]{4,}|[1-9]\d{5,})?', re.I)
patterns={'contact':CONTACT,'public_watermark':PUBLIC,'more_materials':MORE,'direct_cta':DIRECT}
counts=Counter(); files=defaultdict(set); samples=defaultdict(list)
for path in sorted(Path('temp').rglob('*.md')):
    if path.name.startswith('.'): continue
    text=path.read_text(encoding='utf-8-sig')
    for kind,pat in patterns.items():
        for m in pat.finditer(text):
            token=m.group(0)
            counts[(kind,token)]+=1
            files[(kind,token)].add(str(path))
            if len(samples[(kind,token)])<5:
                line=text.count('\n',0,m.start())+1
                samples[(kind,token)].append({'path':str(path),'line':line,'context':text[max(0,m.start()-70):m.end()+90].replace('\n',' ')})
rows=[]
for key,count in sorted(counts.items(),key=lambda kv:(kv[0][0],-kv[1],kv[0][1])):
    kind,token=key
    rows.append({'kind':kind,'token':token,'count':count,'files':sorted(files[key]),'samples':samples[key]})
payload={'summary':{'unique_tokens':len(rows),'occurrences':sum(counts.values()),'files':len(set(p for s in files.values() for p in s))},'tokens':rows}
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(payload['summary'],ensure_ascii=False))
