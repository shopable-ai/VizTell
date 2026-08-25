#!/usr/bin/env python3
from __future__ import annotations
import json,re
from collections import Counter
from pathlib import Path
PATH=Path('temp/《人性心法》/index.md')
REPORT=Path('temp/.human-mind-section15-repair.json')
IMAGE=re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')
SOURCE='第15 节投机是对人性最大的亵渎071很多人以为投机很容易，以为跟对老大，加入一个创业公司待几年上市很容易。这是对人性最大的亵渎。'
TITLE='### 第15节 投机是对人性最大的亵渎'
BODY='很多人以为投机很容易，以为跟对老大，加入一个创业公司待几年上市很容易。这是对人性最大的亵渎。'
FALSE_H3='### 给他工资？谁给他五险一金？'

def refs(t): return Counter(IMAGE.findall(t))

def main():
    before=PATH.read_text(encoding='utf-8-sig'); r=refs(before)
    if before.count(SOURCE)!=1: raise RuntimeError(f'section15 source count={before.count(SOURCE)}')
    if before.count(FALSE_H3)!=1: raise RuntimeError(f'false H3 count={before.count(FALSE_H3)}')
    after=before.replace(SOURCE,TITLE+'\n\n'+BODY,1).replace(FALSE_H3,'给他工资？谁给他五险一金？',1)
    if refs(after)!=r: raise RuntimeError('image refs changed')
    if '第15 节投机是对人性最大的亵渎071' in after: raise RuntimeError('old glued section remains')
    PATH.write_text(after,encoding='utf-8')
    payload={'status':'applied','path':str(PATH),'section15_restored':True,'page_marker_071_removed':True,'false_h3_demoted':1,'image_refs_preserved':sum(r.values()),'errors':[]}
    REPORT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload,ensure_ascii=False))
    return 0
if __name__=='__main__': raise SystemExit(main())
