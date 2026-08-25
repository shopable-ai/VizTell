#!/usr/bin/env python3
"""Normalize clearly over-deep numbered chapter hierarchies in temp/**/*.md.

This is intentionally conservative. It edits only documents whose numbered
chapter structure is clearly shifted one level too deep, for example:

    ### 第二章 ...
    #### 向对方摆明利害关系

becomes:

    ## 第二章 ...
    ### 向对方摆明利害关系

It never rewrites visible text or Markdown image references. Ambiguous headings
remain audit findings rather than being mechanically promoted/demoted.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

HEADING = re.compile(r"^(#{1,6})([ \t]+)(.*?)([ \t]*)$")
CHAPTER = re.compile(r"^第\s*[一二三四五六七八九十百千万零〇两0-9]+\s*章(?:\s+|[：:]|$).*")
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
FENCE = re.compile(r"^\s*(```|~~~)")
TARGET = "做局大师-人间博弈之术.md"
SKIP_NAMES = {
    ".format-subdirs-summary.md", ".root-heading-normalization.md",
    ".root-heading-normalization.json", ".ad-heading-cleanup-report.json",
}


def iter_heading_rows(lines: list[str]):
    in_fence = False
    fence_token = ""
    for i, line in enumerate(lines):
        stripped = line.rstrip("\r\n")
        fm = FENCE.match(stripped)
        if fm:
            token = fm.group(1)
            if not in_fence:
                in_fence, fence_token = True, token
            elif token == fence_token:
                in_fence, fence_token = False, ""
            continue
        if in_fence:
            continue
        hm = HEADING.match(stripped)
        if hm:
            yield i, len(hm.group(1)), hm.group(3).strip()


def image_refs(text: str) -> list[str]:
    return IMAGE.findall(text)


def semantic_body(text: str) -> str:
    out: list[str] = []
    in_fence = False
    fence_token = ""
    for raw in text.splitlines(keepends=True):
        line = raw.rstrip("\r\n")
        ending = raw[len(line):]
        fm = FENCE.match(line)
        if fm:
            token = fm.group(1)
            if not in_fence:
                in_fence, fence_token = True, token
            elif token == fence_token:
                in_fence, fence_token = False, ""
            out.append(raw)
            continue
        if not in_fence:
            hm = HEADING.match(line)
            if hm:
                out.append(hm.group(3).strip() + ending)
                continue
        out.append(raw)
    return "".join(out)


def analyze(lines: list[str], display_name: str) -> dict:
    rows = list(iter_heading_rows(lines))
    chapters = [(i, level, title) for i, level, title in rows if CHAPTER.match(title)]
    chapter_levels = Counter(level for _, level, _ in chapters)
    deep_descendants = 0
    direct_h4 = 0
    for pos, (idx, level, _title) in enumerate(chapters):
        if level != 3:
            continue
        next_idx = chapters[pos + 1][0] if pos + 1 < len(chapters) else len(lines)
        for hidx, hlevel, _htitle in rows:
            if hidx <= idx or hidx >= next_idx:
                continue
            if hlevel <= 2:
                break
            if hlevel >= 4:
                deep_descendants += 1
                if hlevel == 4:
                    direct_h4 += 1

    all_chapters_are_h3 = bool(chapters) and set(chapter_levels) == {3}
    target = display_name.endswith(TARGET)
    eligible = (
        all_chapters_are_h3
        and (len(chapters) >= 2 or target)
        and (direct_h4 >= 2 or deep_descendants >= 3 or target)
    )
    return {
        "chapter_count": len(chapters),
        "chapter_levels": dict(sorted(chapter_levels.items())),
        "h4_descendants": direct_h4,
        "deep_descendants": deep_descendants,
        "eligible": eligible,
    }


def normalize(lines: list[str]) -> tuple[list[str], dict]:
    out: list[str] = []
    in_fence = False
    fence_token = ""
    in_lifted_chapter = False
    changed = chapter_changes = descendant_changes = 0
    samples: list[dict] = []

    for raw in lines:
        stripped = raw.rstrip("\r\n")
        ending = raw[len(stripped):]
        fm = FENCE.match(stripped)
        if fm:
            token = fm.group(1)
            if not in_fence:
                in_fence, fence_token = True, token
            elif token == fence_token:
                in_fence, fence_token = False, ""
            out.append(raw)
            continue
        if in_fence:
            out.append(raw)
            continue

        hm = HEADING.match(stripped)
        if not hm:
            out.append(raw)
            continue
        level = len(hm.group(1))
        title = hm.group(3).strip()
        new_level = level
        if level == 3 and CHAPTER.match(title):
            new_level = 2
            in_lifted_chapter = True
            chapter_changes += 1
        elif in_lifted_chapter and level <= 2:
            in_lifted_chapter = False
        elif in_lifted_chapter and level >= 4:
            new_level = level - 1
            descendant_changes += 1

        if new_level != level:
            changed += 1
            new_line = "#" * new_level + " " + title + ending
            if len(samples) < 16:
                samples.append({"before": "#" * level + " " + title, "after": "#" * new_level + " " + title})
            out.append(new_line)
        else:
            out.append(raw)

    return out, {
        "heading_changes": changed,
        "chapter_changes": chapter_changes,
        "descendant_changes": descendant_changes,
        "samples": samples,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="temp")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", default="temp/.root-heading-normalization.json")
    args = ap.parse_args()
    root = Path(args.root)
    report = {
        "rule": "# book -> ## numbered chapter -> ### chapter subsection -> #### true subsection child",
        "scope": "temp/**/*.md recursively; high-confidence numbered chapter shifts only",
        "changed_files": [], "audited_files": [], "ambiguous_files": [],
    }

    paths = sorted(
        (p for p in root.rglob("*.md") if p.is_file() and not p.name.startswith(".") and p.name not in SKIP_NAMES),
        key=lambda p: str(p),
    )
    for path in paths:
        before = path.read_text(encoding="utf-8")
        lines = before.splitlines(keepends=True)
        display_name = str(path.relative_to(root))
        info = analyze(lines, display_name)
        row = {"file": str(path), **info}
        if not info["eligible"]:
            if info["chapter_count"] and any(int(k) >= 3 for k in info["chapter_levels"]):
                report["ambiguous_files"].append(row)
            report["audited_files"].append(row)
            continue

        new_lines, changes = normalize(lines)
        after = "".join(new_lines)
        row.update(changes)
        if semantic_body(before) != semantic_body(after):
            raise SystemExit(f"SAFETY: visible text changed in {path}")
        if Counter(image_refs(before)) != Counter(image_refs(after)):
            raise SystemExit(f"SAFETY: image references changed in {path}")
        if changes["heading_changes"] and args.apply:
            path.write_text(after, encoding="utf-8")
        if changes["heading_changes"]:
            report["changed_files"].append(row)
        report["audited_files"].append(row)

    report["summary"] = {
        "files_audited": len(report["audited_files"]),
        "files_changed": len(report["changed_files"]),
        "heading_changes": sum(x.get("heading_changes", 0) for x in report["changed_files"]),
        "chapter_changes": sum(x.get("chapter_changes", 0) for x in report["changed_files"]),
        "descendant_changes": sum(x.get("descendant_changes", 0) for x in report["changed_files"]),
        "ambiguous_files": len(report["ambiguous_files"]),
    }
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
