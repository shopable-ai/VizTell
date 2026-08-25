#!/usr/bin/env python3
"""Recover high-confidence numbered Q&A headings.

A plain line such as `12.为什么……？` is promoted only when the next
substantive line begins with `答：` (or the answer begins on the same line).
That answer adjacency distinguishes body sections from textual TOC entries.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

H = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
QA = re.compile(r"^\s*(\d{1,4})\s*[.．、]\s*([^？?\n]{2,100}[？?])\s*(.*)$")
ANSWER = re.compile(r"^\s*答\s*[:：]")


def refs(text: str):
    return Counter(IMAGE.findall(text))


def next_nonblank(lines, start):
    for i in range(start, min(len(lines), start + 8)):
        s = lines[i].strip()
        if s and not IMAGE.fullmatch(s) and not s.startswith("<!--"):
            return i, s
    return None, None


def normalize(lines):
    out=[]
    for raw in lines:
        x=raw.rstrip()
        if x:
            out.append(x)
        elif out and out[-1] != "":
            out.append("")
    while out and out[-1] == "": out.pop()
    return "\n".join(out)+"\n"


def process(path: Path, apply: bool):
    before=path.read_text(encoding="utf-8-sig")
    before_refs=refs(before)
    lines=before.splitlines()
    out=[]; promoted=[]
    for i, raw in enumerate(lines):
        s=raw.strip()
        if H.match(s):
            out.append(raw.rstrip()); continue
        m=QA.match(s)
        if not m:
            out.append(raw.rstrip()); continue
        number, question, remainder=m.groups()
        same_answer=bool(ANSWER.match(remainder))
        j, nxt=next_nonblank(lines, i+1)
        adjacent_answer=bool(nxt and ANSWER.match(nxt))
        if not (same_answer or adjacent_answer):
            out.append(raw.rstrip()); continue
        out.append(f"## {number}. {question.strip()}")
        if remainder.strip():
            out.extend(["", remainder.strip()])
        promoted.append({"line": i+1, "number": int(number), "question": question.strip(), "answer_evidence": "same_line" if same_answer else f"next_line:{j+1}"})
    after=normalize(out)
    if before_refs != refs(after):
        raise RuntimeError(f"{path}: image references changed")
    if len(re.findall(r"^#\s+", after, re.M)) != 1:
        raise RuntimeError(f"{path}: expected exactly one H1")
    changed=after != before.replace("\r\n","\n")
    if changed and apply: path.write_text(after,encoding="utf-8")
    return {"path":str(path),"changed":changed,"applied":bool(changed and apply),"promoted":promoted,"image_refs":sum(before_refs.values())}


def main():
    p=argparse.ArgumentParser(); p.add_argument('--root',default='temp'); p.add_argument('--report',default='temp/.numbered-qa-repair.json'); p.add_argument('--apply',action='store_true'); a=p.parse_args()
    targets=sorted(x for x in Path(a.root).rglob('*.md') if x.is_file() and not x.name.startswith('.'))
    results=[]; errors=[]
    for path in targets:
        try:
            item=process(path,a.apply)
            if item['promoted']: results.append(item)
        except Exception as exc: errors.append({'path':str(path),'error':str(exc)})
    payload={'summary':{'markdown_files_scanned':len(targets),'files_changed':sum(x['applied'] for x in results),'headings_promoted':sum(len(x['promoted']) for x in results),'errors':len(errors)},'results':results,'errors':errors}
    Path(a.report).write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload['summary'],ensure_ascii=False,indent=2))
    return 0 if not errors else 2

if __name__=='__main__': raise SystemExit(main())
