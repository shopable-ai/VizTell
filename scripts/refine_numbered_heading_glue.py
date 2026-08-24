#!/usr/bin/env python3
"""Refine repeated numbered heading families after the conservative first pass.

Focuses on concrete syntax defects observed after OCR conversion:
- a next `第X套：...` title glued to the previous paragraph;
- explanation text glued into a `第X套` heading;
- leftover top-of-document TOC entries (`第X个思想病毒`) before the real
  `第一套` body structure.

Only files identified in temp/.numbered-heading-normalization.json are eligible.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
NUM = r"[一二三四五六七八九十百千零〇两0-9]+"
SET_TOKEN = re.compile(rf"第\s*{NUM}\s*套\s*[：:]")
SET_LINE = re.compile(rf"^(?:##\s+)?(第\s*{NUM}\s*套\s*[：:]\s*)(.+)$")
VIRUS_HEADING = re.compile(rf"^##\s+第\s*{NUM}\s*个思想病毒[：:].+$")
TITLE_END = re.compile(r"^(.{1,32}?(?:术|法|模式|系统|策略|技巧|思维|原理|逻辑|公式|模型|法则|效应|原则|机制|方法))(?=\S)")


def split_embedded_sets(lines: list[str]) -> tuple[list[str], int]:
    out: list[str] = []
    count = 0
    for line in lines:
        # Find `第X套：` occurrences that start after body text. Iterate because
        # a single OCR line can contain more than one glued title.
        pending = line
        while True:
            matches = list(SET_TOKEN.finditer(pending))
            later = next((m for m in matches if m.start() > 0), None)
            if not later:
                break
            prefix = pending[:later.start()].rstrip()
            suffix = pending[later.start():].lstrip()
            if prefix:
                out.append(prefix)
                out.append("")
            pending = suffix
            count += 1
        out.append(pending)
    return out, count


def split_set_heading_description(lines: list[str]) -> tuple[list[str], int]:
    out: list[str] = []
    count = 0
    for line in lines:
        s = line.strip()
        m = SET_LINE.match(s)
        if not m:
            out.append(line.rstrip())
            continue
        lead, rest = m.groups()
        # Prefer the shortest plausible technique-name suffix. This book's
        # primary units are short named techniques such as 感官洗脑术/让步操纵术.
        tm = TITLE_END.match(rest)
        if tm and len(rest) > len(tm.group(1)):
            title = tm.group(1).strip()
            desc = rest[len(tm.group(1)):].lstrip(" ：:，,。")
            if desc:
                if out and out[-1] != "":
                    out.append("")
                out.append(f"## {lead}{title}".replace("：:", "："))
                out.append("")
                out.append(desc)
                count += 1
                continue
        # Ensure it is an H2 even when there is no safe description split.
        canonical = f"## {lead}{rest}".replace("：:", "：")
        if out and out[-1] != "":
            out.append("")
        out.append(canonical)
        out.append("")
    return out, count


def remove_leading_virus_toc(lines: list[str]) -> tuple[list[str], int]:
    first_set = next((i for i, line in enumerate(lines) if re.match(r"^##\s+第\s*(?:一|1)\s*套\s*[：:]", line.strip())), None)
    if first_set is None:
        return lines, 0
    before = lines[:first_set]
    # Only treat these as residual TOC entries when there are multiple virus
    # headings immediately before a large numbered-set body.
    idxs = [i for i, line in enumerate(before) if VIRUS_HEADING.match(line.strip())]
    if len(idxs) < 2:
        return lines, 0
    keep = [line for i, line in enumerate(before) if i not in set(idxs)]
    # Drop excess blanks left by removal.
    text = "\n".join(keep + lines[first_set:])
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.splitlines(), len(idxs)


def normalize_spacing(lines: list[str]) -> str:
    out: list[str] = []
    for line in lines:
        s = line.rstrip()
        if re.match(r"^#{1,6}\s+", s.strip()):
            if out and out[-1] != "":
                out.append("")
            out.append(s)
            out.append("")
        else:
            out.append(s)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-report", default="temp/.numbered-heading-normalization.json")
    ap.add_argument("--report", default="temp/.numbered-heading-refinement.json")
    args = ap.parse_args()

    report = json.loads(Path(args.source_report).read_text(encoding="utf-8"))
    candidates = [x for x in report.get("changed", []) if "套" in x.get("active_units", [])]
    changed = []
    errors = []
    for item in candidates:
        path = Path(item["path"])
        before = path.read_text(encoding="utf-8")
        imgs = Counter(IMAGE.findall(before))
        lines, embedded = split_embedded_sets(before.splitlines())
        lines, desc = split_set_heading_description(lines)
        lines, toc = remove_leading_virus_toc(lines)
        after = normalize_spacing(lines)
        if Counter(IMAGE.findall(after)) != imgs:
            errors.append({"path": str(path), "error": "image references changed"})
            continue
        if len(re.findall(r"^#\s+", after, re.M)) != 1:
            errors.append({"path": str(path), "error": "H1 count is not 1"})
            continue
        if after != before:
            path.write_text(after, encoding="utf-8")
            changed.append({
                "path": str(path),
                "embedded_set_titles_separated": embedded,
                "heading_descriptions_separated": desc,
                "residual_toc_headings_removed": toc,
            })

    payload = {
        "changed": changed,
        "errors": errors,
        "summary": {
            "files_changed": len(changed),
            "embedded_set_titles_separated": sum(x["embedded_set_titles_separated"] for x in changed),
            "heading_descriptions_separated": sum(x["heading_descriptions_separated"] for x in changed),
            "residual_toc_headings_removed": sum(x["residual_toc_headings_removed"] for x in changed),
            "errors": len(errors),
        },
    }
    Path(args.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
