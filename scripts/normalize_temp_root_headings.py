#!/usr/bin/env python3
"""Conservatively normalize Markdown heading hierarchy in temp/**/*.md.

Two safe phases are applied:
1. Lift clearly shifted numbered chapters (### 第X章 -> ## 第X章, descendants
   move up one level in the same chapter).
2. Repair obvious structural jumps using semantic cues:
   - front-matter headings such as 前言/序言 are exempt from body hierarchy;
   - long prose/OCR/recommendation noise accidentally marked as headings is
     restored to plain text;
   - short structural headings that skip a level are promoted only to the
     missing parent level.

Visible text and Markdown image references must remain unchanged.
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
FRONTMATTER = re.compile(
    r"^(?:前言|序言|序[一二三四五六七八九十0-9]*[：:]?|推荐序|推荐语|出版说明|版权信息|作者简介|内容简介|导读|引言|后记|致谢)(?:\s|$|[：:])"
)
META_NOISE = re.compile(
    r"(?i)(?:学习中心推荐|社群$|赚钱有道社群|电子书$|THE\s+WORLD\s+OF\s+MORTALS|^[!！\s._-]*[A-Z]{1,6}[!！\s._-]*$)"
)
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
    """Ignore only ATX markers so heading-only edits must preserve visible text."""
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


def analyze_numbered(lines: list[str], display_name: str) -> dict:
    rows = list(iter_heading_rows(lines))
    chapters = [(i, level, title) for i, level, title in rows if CHAPTER.match(title)]
    levels = Counter(level for _, level, _ in chapters)
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
    all_h3 = bool(chapters) and set(levels) == {3}
    target = display_name.endswith(TARGET)
    eligible = all_h3 and (len(chapters) >= 2 or target) and (direct_h4 >= 2 or deep_descendants >= 3 or target)
    return {
        "chapter_count": len(chapters), "chapter_levels": dict(sorted(levels.items())),
        "h4_descendants": direct_h4, "deep_descendants": deep_descendants,
        "eligible_numbered_shift": eligible,
    }


def normalize_numbered(lines: list[str]) -> tuple[list[str], dict]:
    out: list[str] = []
    in_fence = False
    fence_token = ""
    in_lifted_chapter = False
    changes: list[dict] = []
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
        level, title = len(hm.group(1)), hm.group(3).strip()
        new_level = level
        reason = ""
        if level == 3 and CHAPTER.match(title):
            new_level, in_lifted_chapter, reason = 2, True, "numbered-chapter"
        elif in_lifted_chapter and level <= 2:
            in_lifted_chapter = False
        elif in_lifted_chapter and level >= 4:
            new_level, reason = level - 1, "chapter-descendant"
        if new_level != level:
            changes.append({"title": title[:180], "from": level, "to": new_level, "reason": reason})
            out.append("#" * new_level + " " + title + ending)
        else:
            out.append(raw)
    return out, {"changes": changes}


def looks_like_prose_or_noise(title: str) -> bool:
    t = title.strip()
    if META_NOISE.search(t):
        return True
    if len(t) >= 70:
        return True
    if len(t) >= 45 and re.search(r"[，,。！？!?；;]", t):
        return True
    # OCR sentence fragments often contain several commas and no structural prefix.
    if len(t) >= 32 and len(re.findall(r"[，,]", t)) >= 2 and not re.match(r"^(?:第.+[章节篇卷]|[一二三四五六七八九十]+、|\d+[、.．])", t):
        return True
    return False


def repair_obvious_jumps(lines: list[str]) -> tuple[list[str], dict]:
    out: list[str] = []
    in_fence = False
    fence_token = ""
    prev_structural: int | None = None
    changes: list[dict] = []
    exemptions: list[dict] = []

    for line_no, raw in enumerate(lines, 1):
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
        if level == 1:
            prev_structural = 1
            out.append(raw)
            continue

        # Front matter deliberately stays below the body-chapter level and does
        # not become the structural parent of later正文 headings.
        if prev_structural == 1 and FRONTMATTER.match(title):
            exemptions.append({"line": line_no, "title": title[:180], "level": level, "reason": "front-matter"})
            out.append(raw)
            continue

        if prev_structural is not None and level > prev_structural + 1:
            if looks_like_prose_or_noise(title):
                # Restore visible text to a normal paragraph; do not let it act
                # as a parent heading for following structure.
                changes.append({"line": line_no, "title": title[:180], "from": level, "to": 0, "reason": "prose-or-metadata-misheading"})
                out.append(title + ending)
                continue
            new_level = prev_structural + 1
            changes.append({"line": line_no, "title": title[:180], "from": level, "to": new_level, "reason": "fill-missing-heading-level"})
            out.append("#" * new_level + " " + title + ending)
            prev_structural = new_level
            continue

        out.append(raw)
        prev_structural = level

    return out, {"changes": changes, "exemptions": exemptions}


def unresolved_jumps(text: str) -> list[dict]:
    lines = text.splitlines(keepends=True)
    out: list[dict] = []
    in_fence = False
    fence_token = ""
    prev_structural: int | None = None
    for line_no, raw in enumerate(lines, 1):
        stripped = raw.rstrip("\r\n")
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
        if not hm:
            continue
        level, title = len(hm.group(1)), hm.group(3).strip()
        if level == 1:
            prev_structural = 1
            continue
        if prev_structural == 1 and FRONTMATTER.match(title):
            continue
        if prev_structural is not None and level > prev_structural + 1:
            out.append({"line": line_no, "previous": prev_structural, "level": level, "title": title[:180]})
        prev_structural = level
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="temp")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", default="temp/.root-heading-normalization.json")
    args = ap.parse_args()
    root = Path(args.root)
    paths = sorted((p for p in root.rglob("*.md") if p.is_file() and not p.name.startswith(".") and p.name not in SKIP_NAMES), key=lambda p: str(p))
    report = {
        "rule": "# book -> ## body chapter/top section -> ### subsection; front matter exempt; prose misheadings demoted",
        "scope": "temp/**/*.md recursively; semantic conservative repair",
        "changed_files": [], "audited_files": [], "unresolved_files": [],
    }

    for path in paths:
        before = path.read_text(encoding="utf-8")
        info = analyze_numbered(before.splitlines(keepends=True), str(path.relative_to(root)))
        work_lines = before.splitlines(keepends=True)
        numbered = {"changes": []}
        if info["eligible_numbered_shift"]:
            work_lines, numbered = normalize_numbered(work_lines)
        work_lines, jumps = repair_obvious_jumps(work_lines)
        after = "".join(work_lines)

        if semantic_body(before) != semantic_body(after):
            raise SystemExit(f"SAFETY: visible text changed in {path}")
        if Counter(image_refs(before)) != Counter(image_refs(after)):
            raise SystemExit(f"SAFETY: image references changed in {path}")
        h1_before = len(re.findall(r"^#\s+", before, re.M))
        h1_after = len(re.findall(r"^#\s+", after, re.M))
        if h1_before != h1_after:
            raise SystemExit(f"SAFETY: H1 count changed in {path}: {h1_before}->{h1_after}")

        all_changes = numbered["changes"] + jumps["changes"]
        row = {
            "file": str(path), **info,
            "heading_changes": len(all_changes),
            "numbered_changes": numbered["changes"][:12],
            "jump_changes": jumps["changes"][:20],
            "frontmatter_exemptions": jumps["exemptions"][:12],
        }
        if all_changes:
            if args.apply:
                path.write_text(after, encoding="utf-8")
            report["changed_files"].append(row)
        report["audited_files"].append(row)
        unresolved = unresolved_jumps(after)
        if unresolved:
            report["unresolved_files"].append({"file": str(path), "examples": unresolved[:12]})

    report["summary"] = {
        "files_audited": len(report["audited_files"]),
        "files_changed": len(report["changed_files"]),
        "heading_changes": sum(x["heading_changes"] for x in report["changed_files"]),
        "unresolved_jump_files": len(report["unresolved_files"]),
        "frontmatter_exemptions": sum(len(x["frontmatter_exemptions"]) for x in report["audited_files"]),
    }
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
