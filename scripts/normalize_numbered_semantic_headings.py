#!/usr/bin/env python3
"""Normalize high-confidence repeated numbered semantic headings in temp Markdown.

This pass is intentionally conservative. It targets title families that are
strongly book-structural when repeated at line starts (e.g. 第十七诀, 第一套),
and only activates a family when a file contains at least three occurrences.
It also splits OCR-glued consecutive title tokens such as
“第三十诀 ... 第三十一诀 ...”.

Markdown image references are preserved exactly.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
H = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NUM = r"[一二三四五六七八九十百千零〇两0-9]+"
TOKEN = re.compile(rf"第\s*{NUM}\s*(诀|招|计|套|法|术|课|讲)(?=[\s：:、，,.．]|[^\w])")
START = re.compile(rf"^第\s*{NUM}\s*(诀|招|计|套|法|术|课|讲)(?=[\s：:、，,.．]|[^\w])")

# Families that are safe enough to promote as top-level content units when
# repeated throughout a document.
PRIMARY_UNITS = {"诀", "招", "计", "套", "课", "讲"}
SECONDARY_UNITS = {"法", "术"}

TITLE_END_WORDS = (
    "术", "法", "模式", "系统", "策略", "技巧", "思维", "原理", "逻辑",
    "公式", "模型", "法则", "效应", "原则", "机制", "方法", "能力",
)
DESC_STARTS = (
    "用", "利用", "在", "根据", "通过", "把", "让", "原理", "公式",
    "因为", "如果", "可以", "能够", "就是", "是", "指", "主要", "核心",
)


def image_refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def strip_heading(line: str) -> str:
    m = H.match(line.strip())
    return m.group(2).strip() if m else line.strip()


def split_glued_tokens(line: str, active_units: set[str]) -> tuple[list[str], int]:
    """Split multiple active serial-title tokens that were OCR-glued together."""
    plain = strip_heading(line)
    matches = [m for m in TOKEN.finditer(plain) if m.group(1) in active_units]
    if len(matches) <= 1:
        return [line], 0
    # Only split when first token starts at the beginning and every resulting
    # chunk has useful text. This prevents splitting incidental inline mentions.
    if matches[0].start() != 0:
        return [line], 0
    chunks: list[str] = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(plain)
        chunk = plain[m.start():end].strip()
        if len(chunk) < 4:
            return [line], 0
        chunks.append(chunk)
    return chunks, len(chunks) - 1


def extract_titled_prefix(text: str, unit: str) -> tuple[str, str]:
    """For '第一套：感官洗脑术用...' split title from description safely."""
    if unit != "套":
        return text.strip(), ""
    m = re.match(rf"^(第\s*{NUM}\s*套\s*[：:]\s*)(.+)$", text.strip())
    if not m:
        return text.strip(), ""
    lead, rest = m.groups()
    # Choose the earliest plausible title-ending word followed by a known
    # description starter. Keep the whole line if evidence is insufficient.
    candidates: list[tuple[int, str, str]] = []
    for end_word in TITLE_END_WORDS:
        pos = rest.find(end_word)
        while pos >= 0:
            cut = pos + len(end_word)
            title_body = rest[:cut].strip()
            desc = rest[cut:].lstrip(" ：:，,。")
            if 1 <= len(title_body) <= 36 and desc and any(desc.startswith(x) for x in DESC_STARTS):
                candidates.append((cut, title_body, desc))
            pos = rest.find(end_word, pos + 1)
    if not candidates:
        return text.strip(), ""
    _, title_body, desc = min(candidates, key=lambda x: x[0])
    return (lead + title_body).strip(), desc


def choose_level(unit: str, existing_level: int | None) -> int:
    if unit in PRIMARY_UNITS:
        # Numbered formula/lesson units are usually parallel principal sections.
        return 2
    if existing_level and existing_level >= 2:
        return min(existing_level, 3)
    return 3


def normalize_file(path: Path) -> dict:
    before = path.read_text(encoding="utf-8-sig")
    before_images = image_refs(before)
    lines = before.splitlines()

    counts: Counter[str] = Counter()
    for line in lines:
        plain = strip_heading(line)
        m = START.match(plain)
        if m:
            counts[m.group(1)] += 1

    # Require repetition. Primary title families need 3+, weaker 法/术 need 5+.
    active_units = {
        unit for unit, count in counts.items()
        if (unit in PRIMARY_UNITS and count >= 3) or (unit in SECONDARY_UNITS and count >= 5)
    }
    if not active_units:
        return {"path": str(path), "changed": False, "counts": dict(counts)}

    stage: list[str] = []
    glued_splits = 0
    for line in lines:
        chunks, n = split_glued_tokens(line, active_units)
        glued_splits += n
        stage.extend(chunks)

    out: list[str] = []
    heading_changes = 0
    description_splits = 0
    unit_changes: Counter[str] = Counter()

    for raw in stage:
        stripped = raw.strip()
        plain = strip_heading(raw)
        m = START.match(plain)
        if not m or m.group(1) not in active_units:
            out.append(raw.rstrip())
            continue
        unit = m.group(1)
        hm = H.match(stripped)
        existing_level = len(hm.group(1)) if hm else None
        level = choose_level(unit, existing_level)
        heading_text, desc = extract_titled_prefix(plain, unit)

        if out and out[-1] != "":
            out.append("")
        new_heading = f"{'#' * level} {heading_text}"
        out.append(new_heading)
        out.append("")
        if desc:
            out.append(desc)
            description_splits += 1
        if stripped != new_heading or desc:
            heading_changes += 1
            unit_changes[unit] += 1

    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    if image_refs(text) != before_images:
        raise RuntimeError(f"{path}: image references changed")
    if len(re.findall(r"^#\s+", text, re.M)) != 1:
        raise RuntimeError(f"{path}: H1 count changed")

    changed = text != before
    if changed:
        path.write_text(text, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "counts": dict(counts),
        "active_units": sorted(active_units),
        "heading_changes": heading_changes,
        "glued_title_splits": glued_splits,
        "description_splits": description_splits,
        "unit_changes": dict(unit_changes),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="temp")
    ap.add_argument("--report", default="temp/.numbered-heading-normalization.json")
    args = ap.parse_args()

    root = Path(args.root)
    results = []
    errors = []
    for path in sorted(p for p in root.rglob("*.md") if p.is_file() and not p.name.startswith(".")):
        try:
            results.append(normalize_file(path))
        except Exception as exc:
            errors.append({"path": str(path), "error": str(exc)})

    changed = [x for x in results if x.get("changed")]
    payload = {
        "changed": changed,
        "errors": errors,
        "summary": {
            "files_scanned": len(results) + len(errors),
            "files_changed": len(changed),
            "heading_changes": sum(x.get("heading_changes", 0) for x in changed),
            "glued_title_splits": sum(x.get("glued_title_splits", 0) for x in changed),
            "description_splits": sum(x.get("description_splits", 0) for x in changed),
            "errors": len(errors),
        },
    }
    Path(args.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
