#!/usr/bin/env python3
"""Repository-wide semantic completeness audit for temp Markdown.

This audit intentionally catches false passes that syntax-only validators miss.
It is diagnostic: it does not rewrite book content.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

H = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
BOX = re.compile(r"^\s*[□▢▫]\s*.+")
# High-risk plain chapter markers are deliberately limited to explicit chapter-
# like units.  `第X部分/第X部` is common inside prose (e.g. `第三部分，下部...`)
# and is therefore left to lower-confidence/manual review rather than promoted.
CHAPTER_PLAIN = re.compile(r"^\s*(第\s*[一二三四五六七八九十百零〇两0-9]+\s*(?:章|节|课|讲|篇|卷|册)(?![，,。；;：:])\s*.{0,90})\s*$")
QA = re.compile(r"^\s*\d{1,4}\s*[.．、]\s*[^？?\n]{2,110}[？?]\s*$")
ANSWER = re.compile(r"^\s*答\s*[:：]")
TOC_LEADER = re.compile(r"(?:\.{4,}|…{3,}|·{4,}|﹒{4,})\s*[.·… ]*\d{1,4}\s*$")
CONVERSION = re.compile(r"(?:<!--\s*page\s*:\s*\d+\s*-->|<!--\s*Image\s*\(|^\s*(?:视觉补充|页面视觉补充|OCR文字补充|原始页面文字补充)\s*$)", re.I | re.M)
AD_PATTERNS = [
    re.compile(r"加\s*(?:我|本人)?\s*微信"),
    re.compile(r"微信(?:号|联系|咨询|购买|获取|扫码)"),
    re.compile(r"(?:VX|V信|薇信)\s*[:：号]?", re.I),
    re.compile(r"一手电子书"),
]
BODY_STARTERS = [
    "据说", "有一个", "很多", "一般", "我们", "当", "如果", "因为", "对于",
    "人们", "一个", "其实", "大家", "想要", "假如", "从前", "曾经", "首先",
    "所谓", "现代", "古代", "街头", "从道理", "煤矿", "穷人", "富人", "中国",
]


def visible_chars(text: str) -> int:
    x = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    x = IMAGE.sub("", x)
    x = re.sub(r"^#{1,6}\s*", "", x, flags=re.M)
    x = re.sub(r"[#*_>`~\s]", "", x)
    return len(x)


def git_meta(path: Path) -> dict:
    p = subprocess.run(["git","log","-1","--format=%H%x09%cI%x09%s","--",str(path)], text=True, capture_output=True)
    raw=p.stdout.strip()
    if not raw: return {}
    a=raw.split("\t",2)
    return {"sha":a[0],"date":a[1] if len(a)>1 else None,"message":a[2] if len(a)>2 else None}


def next_nonblank(lines, start):
    for j in range(start, min(len(lines), start+8)):
        s=lines[j].strip()
        if s and not IMAGE.fullmatch(s) and not s.startswith("<!--"):
            return j,s
    return None,None


def common_heading_stems(headings: list[str]) -> set[str]:
    c=Counter()
    for title in headings:
        plain=re.sub(r"^\d+[.、．]\s*", "", title.strip())
        plain=re.sub(r"^[第上中下].{0,8}?[章节篇部卷课讲]\s*", "", plain)
        han="".join(re.findall(r"[\u4e00-\u9fff]", plain))
        if len(han)>=2:
            c[han[:2]] += 1
    return {k for k,v in c.items() if v>=4}


def possible_glue(lines: list[str], stems:set[str], limit=30):
    hits=[]
    for i,raw in enumerate(lines,1):
        s=raw.strip()
        if not s or H.match(s) or IMAGE.search(s) or s.startswith(("|","```","~~~","<!--")):
            continue
        if len(s)<26: continue
        if stems and not any(s.startswith(stem) for stem in stems):
            continue
        for starter in BODY_STARTERS:
            p=s.find(starter,4,36)
            if 4<=p<=35:
                prefix=s[:p].strip(" ：:，,。；;、")
                if 4<=len(prefix)<=30 and not prefix.endswith(("的","和","与","或","是","在")):
                    hits.append({"line":i,"prefix":prefix,"body_starter":starter,"excerpt":s[:180]})
                    break
        if len(hits)>=limit: break
    return hits


def audit(path: Path) -> dict:
    text=path.read_text(encoding="utf-8-sig")
    lines=text.splitlines()
    hs=[]
    for i,raw in enumerate(lines,1):
        m=H.match(raw.strip())
        if m: hs.append((i,len(m.group(1)),m.group(2).strip()))
    h1=sum(level==1 for _,level,_ in hs)
    hbody=[title for _,level,title in hs if 2<=level<=4]
    vis=visible_chars(text)
    issues=[]

    if h1!=1: issues.append({"code":"h1_count","severity":"high","detail":f"H1={h1}"})
    if vis>=30000 and not hbody:
        issues.append({"code":"large_document_without_structure","severity":"high","detail":f"visible_chars={vis}"})
    elif vis>=80000 and len(hbody)<5:
        issues.append({"code":"very_low_heading_density","severity":"high","detail":f"visible_chars={vis}, headings_2_4={len(hbody)}"})
    elif vis>=80000 and vis/max(1,len(hbody))>12000:
        issues.append({"code":"low_heading_density","severity":"medium","detail":f"chars_per_heading={round(vis/max(1,len(hbody)))}"})

    box=[i for i,x in enumerate(lines,1) if BOX.match(x)]
    if box: issues.append({"code":"explicit_box_heading_residue","severity":"high","detail":f"count={len(box)}, lines={box[:20]}"})

    plain_ch=[(i,x.strip()[:120]) for i,x in enumerate(lines,1) if not H.match(x.strip()) and CHAPTER_PLAIN.match(x.strip())]
    if plain_ch: issues.append({"code":"plain_chapter_markers","severity":"high","detail":f"count={len(plain_ch)}, examples={plain_ch[:12]}"})

    qa=[]
    for i,x in enumerate(lines):
        if H.match(x.strip()) or not QA.match(x.strip()): continue
        _,nxt=next_nonblank(lines,i+1)
        if nxt and ANSWER.match(nxt): qa.append(i+1)
    if qa: issues.append({"code":"numbered_qa_heading_residue","severity":"high","detail":f"count={len(qa)}, lines={qa[:20]}"})

    toc=[i for i,x in enumerate(lines[:500],1) if TOC_LEADER.search(x.strip())]
    if toc: issues.append({"code":"leading_toc_leader_residue","severity":"high","detail":f"count={len(toc)}, lines={toc[:20]}"})
    if CONVERSION.search(text): issues.append({"code":"conversion_residue","severity":"high","detail":"page/conversion marker remains"})

    ad=[]
    for pat in AD_PATTERNS:
        for m in pat.finditer(text):
            line=text.count("\n",0,m.start())+1
            ad.append({"line":line,"match":m.group(0)[:60]})
            if len(ad)>=30: break
        if len(ad)>=30: break
    if ad: issues.append({"code":"possible_ad_residue","severity":"medium","detail":f"count_sample={len(ad)}, examples={ad[:20]}"})

    giant=[i for i,x in enumerate(lines,1) if len(x)>2500 and not IMAGE.search(x) and not x.lstrip().startswith("|")]
    if giant: issues.append({"code":"giant_ocr_lines","severity":"medium","detail":f"count={len(giant)}, lines={giant[:20]}"})

    stems=common_heading_stems(hbody)
    glue=possible_glue(lines,stems)
    if len(glue)>=3:
        issues.append({"code":"possible_heading_body_glue","severity":"medium","detail":f"count_sample={len(glue)}, stems={sorted(stems)}, examples={glue[:12]}"})

    huge_head=[{"line":i,"level":l,"length":len(t),"text":t[:160]} for i,l,t in hs if l>1 and len(t)>180]
    if huge_head: issues.append({"code":"oversized_heading","severity":"high","detail":f"count={len(huge_head)}, examples={huge_head[:12]}"})

    sev={x['severity'] for x in issues}
    status='needs_review_high' if 'high' in sev else ('needs_review_medium' if 'medium' in sev else 'pass')
    history=git_meta(path)
    if issues and re.search(r"format|cleanup|finalize|repair", history.get('message') or '', re.I):
        issues.append({"code":"history_processed_but_content_fails","severity":"info","detail":history.get('message')})
    return {"path":str(path),"status":status,"metrics":{"bytes":len(text.encode('utf-8')),"visible_chars":vis,"h1":h1,"headings_2_4":len(hbody),"image_refs":len(IMAGE.findall(text)),"lines":len(lines)},"issues":issues,"history":history}


def main():
    p=argparse.ArgumentParser(); p.add_argument('--root',default='temp'); p.add_argument('--report',default='temp/.semantic-completeness-audit.json'); a=p.parse_args()
    targets=sorted(x for x in Path(a.root).rglob('*.md') if x.is_file() and not x.name.startswith('.'))
    items=[audit(x) for x in targets]
    counts=defaultdict(int)
    for item in items:
        for issue in item['issues']: counts[issue['code']]+=1
    review=[x for x in items if x['status']!='pass']
    payload={'summary':{'markdown_files_scanned':len(items),'pass':sum(x['status']=='pass' for x in items),'needs_review_high':sum(x['status']=='needs_review_high' for x in items),'needs_review_medium':sum(x['status']=='needs_review_medium' for x in items),'review_total':len(review),'image_refs_total':sum(x['metrics']['image_refs'] for x in items)},'issue_counts':dict(sorted(counts.items())), 'review':review}
    Path(a.report).write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload['summary'],ensure_ascii=False,indent=2)); print(json.dumps(payload['issue_counts'],ensure_ascii=False,indent=2))

if __name__=='__main__': main()
