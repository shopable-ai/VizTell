#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

REPORT=Path('temp/.explicit-promo-cleanup-report.json')
IMAGE=re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')
ACCOUNT=r'(?:[A-Za-z][A-Za-z0-9_-]{4,}|[1-9]\d{5,})'
CONTACT=re.compile(
    rf'(?i)(?:[（(]\s*)?(?:(?:更多[^。！？\n]{{0,24}}[,，]?\s*)?(?:添加(?:作者)?|加作者)\s*)?(?:拼课\s*)?(?:我的\s*)?(?:微信|微信号|微芯|薇芯|薇信|V信|VX|WX)\s*[:：号]?\s*{ACCOUNT}(?:\s*[）)])?'
)
PUBLIC_NAMES=['营销书刊','知识藏经阁','文字变现艺术家','顶层思维供应社','文字变现']
PUBLIC=re.compile(r'(?:[（(]\s*)?(?:公号|公众号)\s*[:：]\s*(?:'+'|'.join(map(re.escape,PUBLIC_NAMES))+r')(?:\s*[）)])?')
MORE=re.compile(r'更多资料加\s*信\s*[A-Za-z0-9_-]{4,}', re.I)
EMPTY_BRACKETS=re.compile(r'[（(]\s*[）)]')


def refs(text:str)->Counter[str]:
    return Counter(IMAGE.findall(text))


def clean_text(text:str)->tuple[str,dict]:
    counts={'contact':0,'public_watermark':0,'more_materials':0,'empty_brackets':0}
    out=[]
    for raw in text.splitlines():
        if IMAGE.fullmatch(raw.strip()):
            out.append(raw)
            continue
        line,n=CONTACT.subn('',raw); counts['contact']+=n
        line,n=PUBLIC.subn('',line); counts['public_watermark']+=n
        line,n=MORE.subn('',line); counts['more_materials']+=n
        line,n=EMPTY_BRACKETS.subn('',line); counts['empty_brackets']+=n
        out.append(line)
    return '\n'.join(out)+('\n' if text.endswith(('\n','\r\n')) else ''),counts


def main()->int:
    changed=[]; errors=[]; totals=Counter()
    for path in sorted(Path('temp').rglob('*.md')):
        if path.name.startswith('.'): continue
        try:
            before=path.read_text(encoding='utf-8-sig')
            before_refs=refs(before)
            after,counts=clean_text(before)
            if refs(after)!=before_refs:
                raise RuntimeError('Markdown image references changed')
            if len(re.findall(r'^#\s+',after,re.M))!=1:
                raise RuntimeError('expected exactly one H1')
            if after!=before.replace('\r\n','\n'):
                path.write_text(after,encoding='utf-8')
                item={'path':str(path),**counts,'image_refs':sum(before_refs.values())}
                changed.append(item)
                totals.update(counts)
        except Exception as exc:
            errors.append({'path':str(path),'error':str(exc)})
    # A successful run must leave no exact account credential or known watermark.
    remaining=[]
    for path in sorted(Path('temp').rglob('*.md')):
        if path.name.startswith('.'): continue
        text=path.read_text(encoding='utf-8-sig')
        if CONTACT.search(text) or PUBLIC.search(text) or MORE.search(text):
            remaining.append(str(path))
    if remaining:
        errors.append({'remaining_explicit_promo_files':remaining})
    payload={'summary':{'files_changed':len(changed),'totals':dict(totals),'errors':len(errors)},'changed':changed,'errors':errors}
    REPORT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload['summary'],ensure_ascii=False,indent=2))
    return 0 if not errors else 2

if __name__=='__main__':
    raise SystemExit(main())
