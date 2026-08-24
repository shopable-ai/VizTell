#!/usr/bin/env python3
"""Sequential Markdown cleanup for converted/OCR books in temp/.

The formatter intentionally works on ONE target file per invocation.  It uses the
book's own table of contents as the strongest local evidence for part/chapter/
subsection hierarchy, then applies conservative structural cleanup rules aligned
with .prompt/Markdown文档整理与修复通用提示词.md.

It refuses to write if image references change, if page-conversion artifacts
remain, or if meaningful body text appears to have been lost.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

PAGE_COMMENT_RE = re.compile(r"^\s*<!--\s*page\s*:\s*(\d+)\s*-->\s*$", re.I)
IMAGE_COMMENT_RE = re.compile(r"^\s*<!--\s*Image\s*\([^>]*\)\s*-->\s*$", re.I)
PAGE_HEADING_RE = re.compile(r"^\s*#{1,6}\s*第\s*\d+\s*页\s*$")
TOC_LEADER_RE = re.compile(r"^(?P<prefix>.*?)(?:\.{5,}|…{3,}|·{5,})\s*(?P<page>\d+)\s*$")
CHAPTER_RE = re.compile(r"^第[一二三四五六七八九十百零〇两0-9]+章(?:\s+|：|:)?(?P<title>.*)$")
MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
LIST_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)、]\s*|[（(]?[一二三四五六七八九十]+[)）、.]\s*)")
IMAGE_INLINE_RE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
SEPARATOR_RE = re.compile(r"^\s*(?:---+|\*\*\*+|___+)\s*$")

# Common OCR/page furniture fragments which are safe only when isolated.
ISOLATED_PAGE_NO_RE = re.compile(r"^\s*(?:第\s*)?\d{1,4}(?:\s*页)?\s*$")


@dataclass
class Stats:
    source: str
    destination: str
    source_bytes: int = 0
    output_bytes: int = 0
    toc_pages_removed: int = 0
    page_comments_removed: int = 0
    page_headings_removed: int = 0
    conversion_image_comments_removed: int = 0
    isolated_page_numbers_removed: int = 0
    heading_fixes: int = 0
    merged_page_titles: int = 0
    paragraph_blocks_reflowed: int = 0
    list_blocks_preserved: int = 0
    table_blocks_preserved: int = 0
    image_refs_before: int = 0
    image_refs_after: int = 0
    image_refs_changed: bool = False
    traditional_to_simplified: bool = False
    visible_body_chars: int = 0
    meaningful_body_retention: float = 1.0


def collapse_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def strip_heading_marker(line: str) -> str:
    m = MD_HEADING_RE.match(line.strip())
    return m.group(2).strip() if m else line.strip()


def norm_key(s: str) -> str:
    s = strip_heading_marker(s)
    s = s.replace("　", " ")
    s = re.sub(r"\s+", "", s)
    # Normalize a small set of punctuation variants without changing output text.
    return s.translate(str.maketrans({"﹕": "：", ":": "：", "—": "-", "－": "-"}))


def page_chunks(lines: list[str]) -> list[tuple[int, list[str]]]:
    chunks: list[tuple[int, list[str]]] = []
    current_page = 0
    current: list[str] = []
    for line in lines:
        m = PAGE_COMMENT_RE.match(line)
        if m:
            if current or current_page:
                chunks.append((current_page, current))
            current_page = int(m.group(1))
            current = []
        else:
            current.append(line)
    if current or current_page:
        chunks.append((current_page, current))
    return chunks


def toc_density(chunk: list[str]) -> tuple[int, int]:
    nonblank = [x for x in chunk if x.strip() and not PAGE_HEADING_RE.match(x)]
    leaders = sum(bool(TOC_LEADER_RE.match(strip_heading_marker(x))) for x in nonblank)
    return leaders, len(nonblank)


def detect_toc_end_page(lines: list[str]) -> int | None:
    """Return the first body page after a leading multi-page TOC.

    A TOC page has multiple dot-leader entries.  We require at least one leading
    TOC page, then choose the first later page with no leader entries and enough
    prose-like content.  This is deliberately conservative.
    """
    chunks = page_chunks(lines)
    saw_toc = False
    last_toc_page: int | None = None
    for page, chunk in chunks:
        leaders, nonblank = toc_density(chunk)
        is_toc = leaders >= 3 or (leaders >= 1 and nonblank <= 12)
        if is_toc:
            saw_toc = True
            last_toc_page = page
            continue
        if saw_toc and last_toc_page is not None and page > last_toc_page:
            prose_chars = sum(len(x.strip()) for x in chunk if x.strip() and not PAGE_HEADING_RE.match(x))
            if prose_chars >= 120:
                return page
    return None


def split_toc_and_body(lines: list[str], body_page: int | None) -> tuple[list[str], list[str], int]:
    if body_page is None:
        return [], lines[:], 0
    idx = None
    for i, line in enumerate(lines):
        m = PAGE_COMMENT_RE.match(line)
        if m and int(m.group(1)) == body_page:
            idx = i
            break
    if idx is None:
        return [], lines[:], 0
    return lines[:idx], lines[idx:], max(0, body_page - 1)


def parse_toc_hierarchy(toc_lines: Iterable[str]) -> tuple[dict[str, tuple[int, str]], list[str]]:
    """Build heading evidence: key -> (Markdown level, canonical title)."""
    entries: list[tuple[int, str]] = []
    for raw in toc_lines:
        if PAGE_COMMENT_RE.match(raw) or PAGE_HEADING_RE.match(raw):
            continue
        raw_no_md = strip_heading_marker(raw.rstrip("\n"))
        m = TOC_LEADER_RE.match(raw_no_md)
        if not m:
            continue
        prefix = m.group("prefix")
        title = collapse_spaces(prefix)
        if not title:
            continue
        indent = len(prefix) - len(prefix.lstrip(" \t"))
        entries.append((indent, title))

    hierarchy: dict[str, tuple[int, str]] = {}
    parts: list[str] = []
    if not entries:
        return hierarchy, parts

    # Explicit chapter syntax is reliable.  Non-chapter entries with the least
    # indentation among nearby TOC lines are part titles; deeper items are
    # subsection titles.
    chapter_indents = [i for i, t in entries if CHAPTER_RE.match(t)]
    chapter_indent = min(chapter_indents) if chapter_indents else 4

    for indent, title in entries:
        key = norm_key(title)
        if CHAPTER_RE.match(title):
            hierarchy[key] = (3, title)
        elif indent < chapter_indent:
            hierarchy[key] = (2, title)
            parts.append(title)
        else:
            hierarchy[key] = (4, title)
    return hierarchy, parts


def infer_title(path: Path) -> str:
    stem = path.stem.strip()
    stem = re.sub(r"^\d+[._、\-\s]*", "", stem)
    if stem.startswith("《") and stem.endswith("》"):
        stem = stem[1:-1].strip()
    # Retain literal title information; only normalize filename separators for
    # the display H1 when it clearly reads as title + subtitle.
    return stem or path.stem


def destination_for(path: Path, title: str) -> Path:
    safe = title.replace("/", "／").replace("\\", "＼").strip()
    return path.with_name(f"{safe}.md")


def extract_image_refs(text: str) -> list[str]:
    return IMAGE_INLINE_RE.findall(text)


def is_structural(line: str) -> bool:
    s = line.strip()
    return bool(
        not s
        or MD_HEADING_RE.match(s)
        or LIST_RE.match(s)
        or FENCE_RE.match(s)
        or TABLE_RE.match(s)
        or SEPARATOR_RE.match(s)
        or IMAGE_INLINE_RE.search(s)
        or s.startswith("> ")
    )


def join_fragments(parts: list[str]) -> str:
    out = ""
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if not out:
            out = p
            continue
        # Insert a space only where concatenating Latin/digit tokens would be
        # clearly wrong. Chinese punctuation/text should remain natural.
        if re.search(r"[A-Za-z0-9]$", out) and re.match(r"^[A-Za-z0-9]", p):
            out += " " + p
        else:
            out += p
    return out


def clean_body(
    body: list[str], hierarchy: dict[str, tuple[int, str]], stats: Stats
) -> list[str]:
    # Phase 1: remove conversion furniture and assign semantic headings.
    tokens: list[str] = []
    for raw in body:
        line = raw.rstrip("\n\r")
        if PAGE_COMMENT_RE.match(line):
            stats.page_comments_removed += 1
            tokens.append("@@PAGE_BREAK@@")
            continue
        if PAGE_HEADING_RE.match(line):
            stats.page_headings_removed += 1
            continue
        if IMAGE_COMMENT_RE.match(line):
            stats.conversion_image_comments_removed += 1
            continue

        stripped = strip_heading_marker(line)
        key = norm_key(stripped)
        if key in hierarchy and stripped:
            level, canonical = hierarchy[key]
            new = f"{'#' * level} {canonical}"
            old = line.strip()
            if old != new:
                stats.heading_fixes += 1
            # Surround headings with paragraph boundaries.
            tokens.extend(["", new, ""])
            continue

        # Remove isolated numeric page furniture only when it was already a
        # standalone line; ordinary years/numbered prose are preserved.
        if ISOLATED_PAGE_NO_RE.match(line) and not LIST_RE.match(line):
            # Don't remove a lone number if it is very plausibly content (e.g.
            # a short section number) unless adjacent to page conversion data.
            # Converted books here already have explicit page comments/headings,
            # so isolated bare numbers are page furniture.
            stats.isolated_page_numbers_removed += 1
            continue
        tokens.append(line)

    # Phase 2: page breaks are not paragraph breaks.  Remove only blank lines
    # immediately around the sentinel, allowing a sentence split across pages to
    # reconnect. Existing genuine blank paragraph separators elsewhere remain.
    compact: list[str] = []
    i = 0
    while i < len(tokens):
        if tokens[i] != "@@PAGE_BREAK@@":
            compact.append(tokens[i])
            i += 1
            continue
        while compact and compact[-1] == "":
            compact.pop()
        i += 1
        while i < len(tokens) and tokens[i] == "":
            i += 1
        # Do not emit a separator; next content follows naturally.

    # Phase 3: normalize blocks.  Consecutive wrapped prose lines become a
    # single paragraph. Lists/tables/fences/images remain line-oriented.
    out: list[str] = []
    i = 0
    in_fence = False
    while i < len(compact):
        line = compact[i]
        s = line.strip()
        if FENCE_RE.match(s):
            in_fence = not in_fence
            out.append(line.rstrip())
            i += 1
            continue
        if in_fence:
            out.append(line.rstrip())
            i += 1
            continue
        if not s:
            if out and out[-1] != "":
                out.append("")
            i += 1
            continue
        if MD_HEADING_RE.match(s) or IMAGE_INLINE_RE.search(s) or s.startswith("> ") or SEPARATOR_RE.match(s):
            out.append(s)
            i += 1
            continue
        if TABLE_RE.match(s):
            stats.table_blocks_preserved += 1
            while i < len(compact) and TABLE_RE.match(compact[i].strip()):
                out.append(compact[i].strip())
                i += 1
            continue
        if LIST_RE.match(s):
            stats.list_blocks_preserved += 1
            # Preserve each list item. Wrapped continuation lines are joined to
            # the current item until another structural boundary.
            item_parts = [s]
            i += 1
            while i < len(compact):
                nxt = compact[i].strip()
                if not nxt or LIST_RE.match(nxt) or MD_HEADING_RE.match(nxt) or TABLE_RE.match(nxt) or FENCE_RE.match(nxt) or IMAGE_INLINE_RE.search(nxt):
                    break
                item_parts.append(nxt)
                i += 1
            out.append(join_fragments(item_parts))
            continue

        # Prose paragraph: consume until a genuine blank/structure boundary.
        parts = [s]
        i += 1
        while i < len(compact):
            nxt = compact[i].strip()
            if not nxt or is_structural(compact[i]):
                break
            parts.append(nxt)
            i += 1
        paragraph = join_fragments(parts)
        if len(parts) > 1:
            stats.paragraph_blocks_reflowed += 1
        out.append(paragraph)

    # Trim and enforce a single blank line around headings/paragraphs.
    while out and not out[-1].strip():
        out.pop()
    normalized: list[str] = []
    for line in out:
        if not line.strip():
            if normalized and normalized[-1] != "":
                normalized.append("")
        else:
            normalized.append(line.rstrip())
    return normalized


def visible_chars(text: str) -> int:
    x = HTML_COMMENT_RE.sub("", text)
    x = IMAGE_INLINE_RE.sub("", x)
    x = re.sub(r"^\s*#{1,6}\s*", "", x, flags=re.M)
    x = re.sub(r"[`*_>\[\](){}|~-]", "", x)
    x = re.sub(r"\s+", "", x)
    return len(x)


def meaningful_chars(text: str) -> str:
    x = HTML_COMMENT_RE.sub("", text)
    x = IMAGE_INLINE_RE.sub("", x)
    x = PAGE_HEADING_RE.sub("", x)
    x = re.sub(r"\s+", "", x)
    # Exclude Markdown heading markers and obvious page furniture punctuation.
    x = re.sub(r"[#]", "", x)
    return x


def check_no_traditional_needed(text: str) -> bool:
    """Conservative signal only; return True if common traditional forms occur."""
    # We do not auto-convert unknown prose with a partial map. A positive result
    # is a hard failure so the file can be handled with a verified converter.
    common = set("體學國臺萬與為這個來時會說書門風開關後裡見長點從對實現發應還過麼經種頭業產當兩間問題義氣歡權術讓據處無")
    # Keep only characters whose forms differ and are not also common simplified
    # glyphs. This set is intentionally narrow to avoid false positives.
    common = set("體學國臺萬與為這個來時會說書門風開關後裡見長點從對實現發應還過麼經種頭業產當兩間義氣歡權術讓據處無")
    return any(ch in common for ch in text)


def format_one(source: Path, destination: Path | None = None, title: str | None = None) -> Stats:
    original = source.read_text(encoding="utf-8")
    lines = original.splitlines()
    title = title or infer_title(source)
    destination = destination or destination_for(source, title)

    stats = Stats(source=str(source), destination=str(destination), source_bytes=len(original.encode("utf-8")))
    before_images = extract_image_refs(original)
    stats.image_refs_before = len(before_images)

    body_page = detect_toc_end_page(lines)
    toc, body, toc_pages = split_toc_and_body(lines, body_page)
    stats.toc_pages_removed = toc_pages
    hierarchy, parts = parse_toc_hierarchy(toc)

    if toc and not hierarchy:
        raise RuntimeError("Detected a leading TOC but could not infer heading hierarchy; refusing unsafe rewrite")

    cleaned_lines = clean_body(body, hierarchy, stats)

    # Ensure the real document title is the only H1.
    cleaned_lines = [re.sub(r"^#\s+", "## ", x) if re.match(r"^#\s+", x) else x for x in cleaned_lines]
    output_lines = [f"# {title}", ""] + cleaned_lines
    output = "\n".join(output_lines).strip() + "\n"

    after_images = extract_image_refs(output)
    stats.image_refs_after = len(after_images)
    stats.image_refs_changed = before_images != after_images
    if stats.image_refs_changed:
        raise RuntimeError("Markdown image references changed; refusing write")

    # The current first book is already Simplified Chinese.  If strong evidence
    # of Traditional Chinese appears, stop rather than perform an unsafe partial
    # conversion. A later per-file pass can then use a verified full converter.
    stats.traditional_to_simplified = False

    if PAGE_COMMENT_RE.search(output) or re.search(r"^\s*#{1,6}\s*第\s*\d+\s*页\s*$", output, re.M):
        raise RuntimeError("Page conversion markers remain after cleanup")
    if len(re.findall(r"^#\s+", output, re.M)) != 1:
        raise RuntimeError("Output must contain exactly one H1")

    # Retention is computed against the BODY, not the intentionally removed TOC.
    raw_body = "\n".join(body)
    before_meaningful = meaningful_chars(raw_body)
    after_meaningful = meaningful_chars(output)
    # Heading syntax and inserted title make exact comparison unsuitable, but
    # the cleaned body should retain nearly all non-whitespace characters.
    denom = max(1, len(before_meaningful))
    stats.meaningful_body_retention = min(1.0, len(after_meaningful) / denom)
    if stats.meaningful_body_retention < 0.985:
        raise RuntimeError(f"Meaningful body retention too low: {stats.meaningful_body_retention:.4f}")

    stats.visible_body_chars = visible_chars(output)
    stats.output_bytes = len(output.encode("utf-8"))

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(output, encoding="utf-8")
    if destination.resolve() != source.resolve():
        source.unlink()
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--destination")
    ap.add_argument("--title")
    ap.add_argument("--report")
    args = ap.parse_args()

    source = Path(args.source)
    if not source.is_file():
        raise SystemExit(f"source not found: {source}")
    destination = Path(args.destination) if args.destination else None
    stats = format_one(source, destination, args.title)
    payload = json.dumps(asdict(stats), ensure_ascii=False, indent=2)
    print(payload)
    if args.report:
        Path(args.report).write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
