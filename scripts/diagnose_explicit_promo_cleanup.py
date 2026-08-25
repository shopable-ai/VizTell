#!/usr/bin/env python3
from __future__ import annotations
import json,re
from collections import Counter
from pathlib import Path
from clean_explicit_promo_credentials import CONTACT,PUBLIC,MORE,IMAGE,clean_text,refs

OUT=Path('temp/.explicit-promo-cleanup-diagnostic.json')
problems=[]; would_change=[]; remaining=[]
for path in sorted(Path('temp').rglob('*.md')):
    if path.name.startswith('.'): continue
    before=path.read_text(encoding='utf-8-sig')
    after,counts=clean_text(before)
    if refs(after)!=refs(before):
        problems.append({'path':str(path),'kind':'image_refs_changed'})
    h1=len(re.findall(r'^#\s+',after,re.M))
    if h1!=1:
        problems.append({'path':str(path),'kind':'h1_count','count':h1})
    if after!=before.replace('\r\n','\n'):
        would_change.append({'path':str(path),'counts':counts})
    for kind,pat in [('contact',CONTACT),('public',PUBLIC),('more',MORE)]:
        m=pat.search(after)
        if m:
            remaining.append({'path':str(path),'kind':kind,'match':m.group(0),'context':after[max(0,m.start()-80):m.end()+120].replace('\n',' ')})
payload={'summary':{'would_change_files':len(would_change),'problems':len(problems),'remaining_after_clean':len(remaining)},'problems':problems,'remaining':remaining,'would_change':would_change}
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(payload['summary'],ensure_ascii=False))
