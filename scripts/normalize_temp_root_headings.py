#!/usr/bin/env python3
"""Conservatively normalize Markdown heading hierarchy in temp/**/*.md.

Phases:
1. Lift clearly shifted numbered chapters.
2. Repair obvious heading-level jumps.
3. Re-audit headings promoted by the previous pass and undo promotions when the
   title is actually OCR prose, cover metadata, a promotional tagline, or a
   garbled repeat of the book title.

Only Markdown heading markers may change; visible text and image references are
required to remain identical.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
from collections import Counter
from pathlib import Path

HEADING = re.compile(r"^(#{1,6})([ \t]+)(.*?)([ \t]*)$")
CHAPTER = re.compile(r"^第\s*[一二三四五六七八九十百千万零〇两0-9]+\s*章(?:\s+|[：:]|$).*")
STRUCTURAL_PREFIX = re.compile(
    r"^(?:第\s*[一二三四五六七八九十百千万零〇两0-9]+\s*[章节篇卷部]|"
    r"第\s*[一二三四五六七八九十百千万零〇两0-9]+\s*(?:诀|套|招|计|式|法|步|关|课|讲)|"
    r"[一二三四五六七八九十百千万]+[、.]|\d+\s*[、.．]|(?:第一|第二|第三|第四|第五|第六|第七|第八|第九|第十)部分)"
)
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
FENCE = re.compile(r"^\s*(```|~~~)")
FRONTMATTER = re.compile(
    r"^(?:前言|序言|序[一二三四五六七八九十0-9]*[：:]?|推荐序|推荐语|出版说明|版权信息|作者简介|内容简介|导读|引言|后记|致谢)(?:\s|$|[：:])"
)
META_NOISE = re.compile(
    r"(?i)(?:学习中心推荐|赚钱有道社群|提升财富思维|简体版|亚洲第一心灵能量书|"
    r"THE\s+WORLD\s+OF\s+MORTALS|^[!！\s._-]*[A-Z]{1,6}[!！\s._-]*$)"
)
TARGET = "做局大师-人间博弈之术.md"
SKIP_NAMES = {
    ".format-subdirs-summary.md", ".root-heading-normalization.md",
    ".root-heading-normalization.json", ".ad-heading-cleanup-report.json",
}


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
        if not in_fence and (hm := HEADING.match(line)):
            out.append(hm.group(3).strip() + ending)
        else:
            out.append(raw)
    return "".join(out)


def heading_rows(lines: list[str]):
    in_fence = False
    fence_token = ""
    for i, raw in enumerate(lines):
        line = raw.rstrip("\r\n")
        fm = FENCE.match(line)
        if fm:
            token = fm.group(1)
            if not in_fence:
                in_fence, fence_token = True, token
            elif token == fence_token:
                in_fence, fence_token = False, ""
            continue
        if not in_fence and (hm := HEADING.match(line)):
            yield i, len(hm.group(1)), hm.group(3).strip()


def analyze_numbered(lines: list[str], display_name: str) -> dict:
    rows = list(heading_rows(lines))
    chapters = [(i, level, title) for i, level, title in rows if CHAPTER.match(title)]
    levels = Counter(level for _, level, _ in chapters)
    deep_descendants = direct_h4 = 0
    for pos, (idx, level, _title) in enumerate(chapters):
        if level != 3:
            continue
        next_idx = chapters[pos + 1][0] if pos + 1 < len(chapters) else len(lines)
        for hidx, hlevel, _ in rows:
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


def normalize_numbered(lines: list[str]) -> tuple[list[str], list[dict]]:
    out: list[str] = []
    in_fence = False
    fence_token = ""
    in_chapter = False
    changes: list[dict] = []
    for line_no, raw in enumerate(lines, 1):
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
        if in_fence or not (hm := HEADING.match(line)):
            out.append(raw)
            continue
        level, title = len(hm.group(1)), hm.group(3).strip()
        new = level
        reason = ""
        if level == 3 and CHAPTER.match(title):
            new, in_chapter, reason = 2, True, "numbered-chapter"
        elif in_chapter and level <= 2:
            in_chapter = False
        elif in_chapter and level >= 4:
            new, reason = level - 1, "chapter-descendant"
        if new != level:
            changes.append({"line": line_no, "title": title[:180], "from": level, "to": new, "reason": reason})
            out.append("#" * new + " " + title + ending)
        else:
            out.append(raw)
    return out, changes


def normalized_identity(s: str) -> str:
    s = Path(s).parent.name if Path(s).name.lower() == "index.md" else Path(s).stem
    s = re.sub(r"PDF版|纯文字版|全文字版", "", s, flags=re.I)
    return re.sub(r"[《》〈〉【】\[\]（）()\s·•—_\-:：,.，。'\"“”‘’]", "", s).lower()


def repeated_cover_title(title: str, display_name: str, line_no: int) -> bool:
    if line_no > 15:
        return False
    a = re.sub(r"[《》〈〉【】\[\]（）()\s·•—_\-:：,.，。'\"“”‘’]", "", title).lower()
    b = normalized_identity(display_name)
    if len(a) < 4 or len(b) < 4:
        return False
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    match = difflib.SequenceMatcher(None, a, b).find_longest_match(0, len(a), 0, len(b)).size
    return ratio >= 0.68 or (match >= 5 and match / min(len(a), len(b)) >= 0.65)


def looks_like_prose_or_noise(title: str, display_name: str = "", line_no: int = 9999) -> bool:
    t = title.strip()
    if META_NOISE.search(t):
        return True
    if display_name and repeated_cover_title(t, display_name, line_no):
        return True
    if t.startswith(("：", ":")):
        return True
    if STRUCTURAL_PREFIX.match(t):
        return False
    if re.search(r"[？！!?](?:\s*\d+)?$", t):
        return False
    if len(t) >= 70:
        return True
    if len(t) >= 20 and "。" in t:
        return True
    if len(t) >= 22 and "，" in t:
        return True
    if len(re.findall(r"[，,]", t)) >= 2:
        return True
    if re.match(r"^(?:的|是|那么|下来|颚|条大路|我认为|核心的目的)", t) and len(t) >= 12:
        return True
    return False


def previous_promotions(report_path: Path) -> dict[str, set[str]]:
    if not report_path.exists():
        return {}
    try:
        data = json.loads(report_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    out: dict[str, set[str]] = {}
    for row in data.get("changed_files", []):
        file = row.get("file")
        if not file:
            continue
        for ch in row.get("jump_changes", []):
            if ch.get("from") == 3 and ch.get("to") == 2 and ch.get("reason") == "fill-missing-heading-level":
                title = ch.get("title")
                if title:
                    out.setdefault(file, set()).add(title)
    return out


def reaudit_prior_promotions(lines: list[str], display_name: str, prior_titles: set[str]) -> tuple[list[str], list[dict]]:
    if not prior_titles:
        return lines, []
    out: list[str] = []
    changes: list[dict] = []
    in_fence = False
    fence_token = ""
    for line_no, raw in enumerate(lines, 1):
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
        if not in_fence and (hm := HEADING.match(line)):
            level, title = len(hm.group(1)), hm.group(3).strip()
            if level == 2 and title in prior_titles and looks_like_prose_or_noise(title, display_name, line_no):
                changes.append({"line": line_no, "title": title[:180], "from": 2, "to": 0, "reason": "reverse-false-promotion"})
                out.append(title + ending)
                continue
        out.append(raw)
    return out, changes


def repair_jumps(lines: list[str], display_name: str) -> tuple[list[str], list[dict], list[dict]]:
    out: list[str] = []
    changes: list[dict] = []
    exemptions: list[dict] = []
    in_fence = False
    fence_token = ""
    prev: int | None = None
    for line_no, raw in enumerate(lines, 1):
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
        if in_fence or not (hm := HEADING.match(line)):
            out.append(raw)
            continue
        level, title = len(hm.group(1)), hm.group(3).strip()
        if level == 1:
            prev = 1
            out.append(raw)
            continue
        if prev == 1 and FRONTMATTER.match(title):
            exemptions.append({"line": line_no, "title": title[:180], "level": level, "reason": "front-matter"})
            out.append(raw)
            continue
        if prev is not None and level > prev + 1:
            if looks_like_prose_or_noise(title, display_name, line_no):
                changes.append({"line": line_no, "title": title[:180], "from": level, "to": 0, "reason": "prose-or-metadata-misheading"})
                out.append(title + ending)
                continue
            new = prev + 1
            changes.append({"line": line_no, "title": title[:180], "from": level, "to": new, "reason": "fill-missing-heading-level"})
            out.append("#" * new + " " + title + ending)
            prev = new
            continue
        out.append(raw)
        prev = level
    return out, changes, exemptions


def unresolved_jumps(text: str) -> list[dict]:
    out: list[dict] = []
    prev: int | None = None
    in_fence = False
    fence_token = ""
    for line_no, raw in enumerate(text.splitlines(), 1):
        fm = FENCE.match(raw)
        if fm:
            token = fm.group(1)
            if not in_fence:
                in_fence, fence_token = True, token
            elif token == fence_token:
                in_fence, fence_token = False, ""
            continue
        if in_fence or not (hm := HEADING.match(raw)):
            continue
        level, title = len(hm.group(1)), hm.group(3).strip()
        if level == 1:
            prev = 1
            continue
        if prev == 1 and FRONTMATTER.match(title):
            continue
        if prev is not None and level > prev + 1:
            out.append({"line": line_no, "previous": prev, "level": level, "title": title[:180]})
        prev = level
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="temp")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", default="temp/.root-heading-normalization.json")
    args = ap.parse_args()
    root = Path(args.root)
    report_path = Path(args.report)
    prior = previous_promotions(report_path)
    paths = sorted((p for p in root.rglob("*.md") if p.is_file() and not p.name.startswith(".") and p.name not in SKIP_NAMES), key=lambda p: str(p))
    report = {
        "rule": "# book -> ## body chapter/top section -> ### subsection; front matter exempt; prose/metadata misheadings demoted",
        "scope": "temp/**/*.md recursively; conservative semantic repair + reverse audit",
        "changed_files": [], "audited_files": [], "unresolved_files": [],
    }
    for path in paths:
        before = path.read_text(encoding="utf-8")
        display = str(path.relative_to(root))
        info = analyze_numbered(before.splitlines(keepends=True), display)
        lines = before.splitlines(keepends=True)
        numbered: list[dict] = []
        if info["eligible_numbered_shift"]:
            lines, numbered = normalize_numbered(lines)
        lines, reversed_changes = reaudit_prior_promotions(lines, display, prior.get(str(path), set()))
        lines, jump_changes, exemptions = repair_jumps(lines, display)
        after = "".join(lines)
        if semantic_body(before) != semantic_body(after):
            raise SystemExit(f"SAFETY: visible text changed in {path}")
        if Counter(image_refs(before)) != Counter(image_refs(after)):
            raise SystemExit(f"SAFETY: image references changed in {path}")
        if len(re.findall(r"^#\s+", before, re.M)) != len(re.findall(r"^#\s+", after, re.M)):
            raise SystemExit(f"SAFETY: H1 count changed in {path}")
        all_changes = numbered + reversed_changes + jump_changes
        row = {
            "file": str(path), **info, "heading_changes": len(all_changes),
            "numbered_changes": numbered[:12], "reverse_audit_changes": reversed_changes[:20],
            "jump_changes": jump_changes[:20], "frontmatter_exemptions": exemptions[:12],
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
        "reverse_audit_changes": sum(len(x["reverse_audit_changes"]) for x in report["changed_files"]),
        "unresolved_jump_files": len(report["unresolved_files"]),
        "frontmatter_exemptions": sum(len(x["frontmatter_exemptions"]) for x in report["audited_files"]),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
