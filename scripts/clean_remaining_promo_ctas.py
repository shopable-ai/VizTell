#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

REPORT=Path('temp/.remaining-promo-cta-cleanup-report.json')
IMAGE=re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')

# Exact recurring promotional units confirmed by current-content review.
PATTERNS=[
    ('human_mind_private_wechat', re.compile(r'扫码添加王老师私人微信号或搜索【wanglaoshikefu】，回复[“"]突破[”"]')),
    ('human_mind_resume_course', re.compile(r'(?:###\s*)?扫码关注[，,]?\s*回复[“"]简历[”"]二字\s*送你一份由王老师亲自编写的超实用简历模板帮你的职场更顺利仅需\s*1\s*元[，,]?即可试听王老师精彩千聊课程《[^》]{1,80}》')),
    ('author_internal_share', re.compile(r'(?:具体(?:更多)?落地细节\s*[：:,，]?\s*|更多落地细节\s*[，,]?\s*|具体更多落地细节\s*[，,]?\s*)?(?:可以|可)?\s*添加作者(?:获取内部分享|内部分享|内部|获取内部营销密码)[。！？]?')),
    ('layout5_author_wechat', re.compile(r'[（(]\s*(?:具体落地细节\s*[，,]?\s*)?(?:割韭菜\s*模板可)?\s*添加作者微信\s*[；;:：]?\s*1\s*3\s*6\s*1\s*3\s*8\s*2\s*6\s*5\s*1\s*4\s*获取内部分享\s*[）)]')),
    ('layout5_orphan_author_share', re.compile(r'因为书籍页码\s*有\s*限[，,]?\s*可以添加作者侬信\s*[：:]?\s*获取\s*内\s*部分享[。！？]?')),
]

def refs(t:str)->Counter[str]: return Counter(IMAGE.findall(t))

def main()->int:
    changed=[]; totals=Counter(); errors=[]
    for path in sorted(Path('temp').rglob('*.md')):
        if path.name.startswith('.'): continue
        try:
            before=path.read_text(encoding='utf-8-sig'); r=refs(before); after=before; counts={}
            for kind,pat in PATTERNS:
                after,n=pat.subn('',after); counts[kind]=n; totals[kind]+=n
            if refs(after)!=r: raise RuntimeError('image refs changed')
            if len(re.findall(r'^#\s+',after,re.M))!=1: raise RuntimeError('H1 invariant failed')
            if after!=before.replace('\r\n','\n'):
                path.write_text(after,encoding='utf-8')
                changed.append({'path':str(path),'counts':counts,'image_refs':sum(r.values())})
        except Exception as exc:
            errors.append({'path':str(path),'error':str(exc)})
    remaining=[]
    for path in sorted(Path('temp').rglob('*.md')):
        if path.name.startswith('.'): continue
        text=path.read_text(encoding='utf-8-sig')
        for kind,pat in PATTERNS:
            m=pat.search(text)
            if m: remaining.append({'path':str(path),'kind':kind,'match':m.group(0)[:180]})
    if remaining: errors.append({'remaining':remaining})
    payload={'summary':{'files_changed':len(changed),'removed':dict(totals),'errors':len(errors)},'changed':changed,'errors':errors}
    REPORT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload['summary'],ensure_ascii=False,indent=2))
    return 0 if not errors else 2
if __name__=='__main__': raise SystemExit(main())
