#!/usr/bin/env python3
"""Conservative one-file-at-a-time Markdown formatter for temp/ books.

Rules are aligned with .prompt/Markdown文档整理与修复通用提示词.md.
The script intentionally processes exactly ONE file per invocation and refuses
writes if Markdown image references change or meaningful body retention drops.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

PAGE_COMMENT = re.compile(r"^\s*<!--\s*page\s*:\s*(\d+)\s*-->\s*$", re.I)
PAGE_HEADING = re.compile(r"^\s*#{1,6}\s*第\s*\d+\s*页\s*$")
IMAGE_COMMENT = re.compile(r"^\s*<!--\s*Image\s*\([^>]*\)\s*-->\s*$", re.I)
TOC_LEADER = re.compile(r"^(?P<prefix>.*?)(?:\.{5,}|…{3,}|·{5,})\s*\d+\s*$")
CHAPTER = re.compile(r"^第[一二三四五六七八九十百零〇两0-9]+章(?:\s+|：|:)?(?P<title>.*)$")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
LIST = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)、]\s*|[（(]?[一二三四五六七八九十]+[)）、.]\s*)")
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
TABLE = re.compile(r"^\s*\|.*\|\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
SEPARATOR = re.compile(r"^\s*(?:---+|\*\*\*+|___+)\s*$")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


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
    heading_fixes: int = 0
    paragraph_blocks_reflowed: int = 0
    list_blocks_preserved: int = 0
    table_blocks_preserved: int = 0
    image_refs_before: int = 0
    image_refs_after: int = 0
    image_refs_changed: bool = False
    visible_body_chars: int = 0
    meaningful_body_retention: float = 1.0


def strip_heading(s: str) -> str:
    s = s.strip()
    m = HEADING.match(s)
    return m.group(2).strip() if m else s


def key(s: str) -> str:
    s = strip_heading(s).replace("　", " ")
    s = re.sub(r"\s+", "", s)
    return s.translate(str.maketrans({"﹕": "：", ":": "：", "—": "-", "－": "-"}))


def chunks(lines: list[str]) -> list[tuple[int, list[str]]]:
    out: list[tuple[int, list[str]]] = []
    page = 0
    buf: list[str] = []
    for line in lines:
        m = PAGE_COMMENT.match(line)
        if m:
            if page or buf:
                out.append((page, buf))
            page = int(m.group(1))
            buf = []
        else:
            buf.append(line)
    if page or buf:
        out.append((page, buf))
    return out


def find_body_page(lines: list[str]) -> int | None:
    saw_toc = False
    last_toc = None
    for page, block in chunks(lines):
        nonblank = [x for x in block if x.strip() and not PAGE_HEADING.match(x)]
        leaders = sum(bool(TOC_LEADER.match(strip_heading(x))) for x in nonblank)
        is_toc = leaders >= 3 or (leaders >= 1 and len(nonblank) <= 12)
        if is_toc:
            saw_toc = True
            last_toc = page
            continue
        if saw_toc and last_toc is not None and page > last_toc:
            prose = sum(len(x.strip()) for x in nonblank)
            if prose >= 120:
                return page
    return None


def split_toc(lines: list[str], body_page: int | None) -> tuple[list[str], list[str], int]:
    if body_page is None:
        return [], lines[:], 0
    for i, line in enumerate(lines):
        m = PAGE_COMMENT.match(line)
        if m and int(m.group(1)) == body_page:
            return lines[:i], lines[i:], max(0, body_page - 1)
    return [], lines[:], 0


def toc_hierarchy(toc: list[str]) -> dict[str, tuple[int, str]]:
    entries: list[tuple[int, str]] = []
    for raw in toc:
        if PAGE_COMMENT.match(raw) or PAGE_HEADING.match(raw):
            continue
        plain = strip_heading(raw)
        m = TOC_LEADER.match(plain)
        if not m:
            continue
        prefix = m.group("prefix")
        title = re.sub(r"\s+", " ", prefix.strip())
        if title:
            indent = len(prefix) - len(prefix.lstrip(" \t"))
            entries.append((indent, title))
    if not entries:
        return {}
    chapter_indents = [i for i, t in entries if CHAPTER.match(t)]
    chapter_indent = min(chapter_indents) if chapter_indents else 4
    out: dict[str, tuple[int, str]] = {}
    for indent, title in entries:
        if CHAPTER.match(title):
            level = 3
        elif indent < chapter_indent:
            level = 2
        else:
            level = 4
        out[key(title)] = (level, title)
    return out


def image_refs(text: str) -> list[str]:
    return IMAGE.findall(text)


def join_wrapped(parts: list[str]) -> str:
    out = ""
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if not out:
            out = part
        elif re.search(r"[A-Za-z0-9]$", out) and re.match(r"^[A-Za-z0-9]", part):
            out += " " + part
        else:
            out += part
    return out


def structural(line: str) -> bool:
    s = line.strip()
    return bool(not s or HEADING.match(s) or LIST.match(s) or TABLE.match(s) or FENCE.match(s)
                or SEPARATOR.match(s) or IMAGE.search(s) or s.startswith("> "))


def clean_body(body: list[str], hierarchy: dict[str, tuple[int, str]], stats: Stats) -> list[str]:
    stage: list[str] = []
    for raw in body:
        line = raw.rstrip("\r\n")
        if PAGE_COMMENT.match(line):
            stats.page_comments_removed += 1
            stage.append("@@PAGE_BREAK@@")
            continue
        if PAGE_HEADING.match(line):
            stats.page_headings_removed += 1
            continue
        if IMAGE_COMMENT.match(line):
            stats.conversion_image_comments_removed += 1
            continue
        plain = strip_heading(line)
        evidence = hierarchy.get(key(plain)) if plain else None
        if evidence:
            level, canonical = evidence
            new = f"{'#' * level} {canonical}"
            if line.strip() != new:
                stats.heading_fixes += 1
            stage.extend(["", new, ""])
            continue
        # Do NOT delete isolated numbers here: without page-adjacent evidence,
        # a standalone number may be real content. Explicit page headings above
        # are the only page-number text removed automatically.
        stage.append(line)

    # A PDF page boundary is not automatically a paragraph boundary. Remove
    # blanks adjacent to explicit page markers so sentences split across pages
    # reconnect; preserve all other blank lines.
    compact: list[str] = []
    i = 0
    while i < len(stage):
        if stage[i] != "@@PAGE_BREAK@@":
            compact.append(stage[i])
            i += 1
            continue
        while compact and compact[-1] == "":
            compact.pop()
        i += 1
        while i < len(stage) and stage[i] == "":
            i += 1

    out: list[str] = []
    i = 0
    in_fence = False
    while i < len(compact):
        s = compact[i].strip()
        if FENCE.match(s):
            in_fence = not in_fence
            out.append(compact[i].rstrip())
            i += 1
            continue
        if in_fence:
            out.append(compact[i].rstrip())
            i += 1
            continue
        if not s:
            if out and out[-1] != "":
                out.append("")
            i += 1
            continue
        if HEADING.match(s) or IMAGE.search(s) or s.startswith("> ") or SEPARATOR.match(s):
            out.append(s)
            i += 1
            continue
        if TABLE.match(s):
            stats.table_blocks_preserved += 1
            while i < len(compact) and TABLE.match(compact[i].strip()):
                out.append(compact[i].strip())
                i += 1
            continue
        if LIST.match(s):
            stats.list_blocks_preserved += 1
            parts = [s]
            i += 1
            while i < len(compact):
                nxt = compact[i].strip()
                if not nxt or LIST.match(nxt) or structural(compact[i]):
                    break
                parts.append(nxt)
                i += 1
            out.append(join_wrapped(parts))
            continue
        parts = [s]
        i += 1
        while i < len(compact):
            nxt = compact[i].strip()
            if not nxt or structural(compact[i]):
                break
            parts.append(nxt)
            i += 1
        if len(parts) > 1:
            stats.paragraph_blocks_reflowed += 1
        out.append(join_wrapped(parts))

    normalized: list[str] = []
    for line in out:
        if not line.strip():
            if normalized and normalized[-1] != "":
                normalized.append("")
        else:
            normalized.append(line.rstrip())
    while normalized and normalized[-1] == "":
        normalized.pop()
    return normalized


def visible_chars(text: str) -> int:
    x = HTML_COMMENT.sub("", text)
    x = IMAGE.sub("", x)
    x = re.sub(r"^\s*#{1,6}\s*", "", x, flags=re.M)
    x = re.sub(r"[`*_>\[\](){}|~-]", "", x)
    return len(re.sub(r"\s+", "", x))


def meaningful_len(text: str) -> int:
    x = HTML_COMMENT.sub("", text)
    x = IMAGE.sub("", x)
    x = re.sub(r"^\s*#{1,6}\s*第\s*\d+\s*页\s*$", "", x, flags=re.M)
    x = re.sub(r"[#\s]", "", x)
    return len(x)


def infer_title(path: Path) -> str:
    stem = re.sub(r"^\d+[._、\-\s]*", "", path.stem.strip())
    if stem.startswith("《") and stem.endswith("》"):
        stem = stem[1:-1].strip()
    return stem or path.stem


def run(source: Path, destination: Path, title: str) -> Stats:
    original = source.read_text(encoding="utf-8")
    lines = original.splitlines()
    stats = Stats(str(source), str(destination), source_bytes=len(original.encode("utf-8")))
    before_images = image_refs(original)
    stats.image_refs_before = len(before_images)

    body_page = find_body_page(lines)
    toc, body, stats.toc_pages_removed = split_toc(lines, body_page)
    hierarchy = toc_hierarchy(toc)
    if toc and not hierarchy:
        raise RuntimeError("TOC detected but hierarchy could not be inferred; refusing unsafe rewrite")

    cleaned = clean_body(body, hierarchy, stats)
    # Demote any surviving accidental H1 before adding the real book title.
    cleaned = [re.sub(r"^#\s+", "## ", x) if re.match(r"^#\s+", x) else x for x in cleaned]
    output = "\n".join([f"# {title}", ""] + cleaned).strip() + "\n"

    after_images = image_refs(output)
    stats.image_refs_after = len(after_images)
    stats.image_refs_changed = before_images != after_images
    if stats.image_refs_changed:
        raise RuntimeError("Markdown image references changed; refusing write")
    if re.search(r"^\s*<!--\s*page\s*:", output, re.M | re.I):
        raise RuntimeError("page comments remain")
    if re.search(r"^\s*#{1,6}\s*第\s*\d+\s*页\s*$", output, re.M):
        raise RuntimeError("page headings remain")
    if len(re.findall(r"^#\s+", output, re.M)) != 1:
        raise RuntimeError("output must contain exactly one H1")

    before_len = max(1, meaningful_len("\n".join(body)))
    after_len = meaningful_len(output)
    stats.meaningful_body_retention = min(1.0, after_len / before_len)
    if stats.meaningful_body_retention < 0.985:
        raise RuntimeError(f"body retention too low: {stats.meaningful_body_retention:.4f}")

    stats.visible_body_chars = visible_chars(output)
    stats.output_bytes = len(output.encode("utf-8"))
    destination.write_text(output, encoding="utf-8")
    if source.resolve() != destination.resolve():
        source.unlink()
    return stats


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--destination", required=True)
    p.add_argument("--title")
    p.add_argument("--report")
    a = p.parse_args()
    source = Path(a.source)
    destination = Path(a.destination)
    title = a.title or infer_title(source)
    if not source.is_file():
        raise SystemExit(f"source not found: {source}")
    stats = run(source, destination, title)
    payload = json.dumps(asdict(stats), ensure_ascii=False, indent=2)
    print(payload)
    if a.report:
        Path(a.report).write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
