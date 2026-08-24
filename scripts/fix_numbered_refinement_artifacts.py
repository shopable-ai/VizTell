#!/usr/bin/env python3
"""Repair artifacts from the numbered-heading refinement pass and patch its bug.

Observed artifact class:
- existing `## 第X套...` was re-split as if `##` were prose, leaving an empty
  `##` line;
- a compound technique title could be cut too early, e.g.
  `第五套：限定思维` + `操控术原理：`.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
SET_H = re.compile(r"^##\s+(第\s*[一二三四五六七八九十百千零〇两0-9]+\s*套\s*[：:]\s*)(.+)$")
CONT = re.compile(r"^([^\s，。；：:]{1,16}(?:术|法|模式|系统|策略|技巧|机制|方法))(.*)$")
TERMINALS = ("术", "法", "模式", "系统", "策略", "技巧", "机制", "方法", "模型", "法则", "原则")


def repair_file(path: Path) -> dict:
    before = path.read_text(encoding="utf-8")
    imgs = Counter(IMAGE.findall(before))
    lines = before.splitlines()
    out: list[str] = []
    blank_h2_removed = 0
    compound_titles_rejoined = 0
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s == "##":
            blank_h2_removed += 1
            i += 1
            continue
        m = SET_H.match(s)
        if m:
            lead, title = m.groups()
            if not title.endswith(TERMINALS):
                # Look ahead over blank lines for a continuation beginning with
                # a compact technique-name suffix such as 操控术.
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    cm = CONT.match(lines[j].strip())
                    if cm:
                        suffix, rest = cm.groups()
                        out.append(f"## {lead}{title}{suffix}")
                        out.append("")
                        if rest.strip(" ：:，,。"):
                            out.append(rest.lstrip(" ：:，,。"))
                        compound_titles_rejoined += 1
                        i = j + 1
                        continue
        out.append(lines[i].rstrip())
        i += 1

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    if Counter(IMAGE.findall(text)) != imgs:
        raise RuntimeError("image references changed")
    if len(re.findall(r"^#\s+", text, re.M)) != 1:
        raise RuntimeError("H1 count is not 1")
    if re.search(r"^##\s*$", text, re.M):
        raise RuntimeError("blank H2 remains")
    if text != before:
        path.write_text(text, encoding="utf-8")
    return {
        "path": str(path),
        "changed": text != before,
        "blank_h2_removed": blank_h2_removed,
        "compound_titles_rejoined": compound_titles_rejoined,
    }


def patch_refiner(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    before = text
    # Do not split a SET_TOKEN inside an already-valid Markdown heading line.
    text = text.replace(
        '        pending = line\n        while True:',
        '        if re.match(r"^#{1,6}\\s+", line.strip()):\n            out.append(line)\n            continue\n        pending = line\n        while True:',
        1,
    )
    path.write_text(text, encoding="utf-8")
    return text != before


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="temp/《洗脑的最高境界》.md")
    ap.add_argument("--refiner", default="scripts/refine_numbered_heading_glue.py")
    ap.add_argument("--report", default="temp/.numbered-refinement-artifact-fix.json")
    args = ap.parse_args()

    result = repair_file(Path(args.target))
    patched = patch_refiner(Path(args.refiner))
    payload = {
        "file": result,
        "refiner_bug_patched": patched,
        "errors": [],
    }
    Path(args.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
