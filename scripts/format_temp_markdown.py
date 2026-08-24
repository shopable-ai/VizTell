#!/usr/bin/env python3
"""Conservative formatter for converted/OCR Markdown books under temp/.

Aligned with .prompt/Markdown文档整理与修复通用提示词.md.
The script processes ONE file per invocation. It is designed for temp/**/index.md
and refuses the write if image references are lost/changed, page markers remain,
or body retention falls below the safety threshold.

Important image rule: full-page source screenshots may intentionally move after
searchable OCR text. Therefore image *order* may change, but the multiset of
Markdown image references (exact strings, paths and counts) must remain identical.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from opencc import OpenCC
    CC = OpenCC("t2s")
except Exception:
    CC = None

PAGE_COMMENT = re.compile(r"^\s*<!--\s*page\s*:\s*(\d+)\s*-->\s*$", re.I)
PAGE_HEADING = re.compile(r"^\s*#{1,6}\s*第\s*\d+\s*页\s*$")
IMAGE_COMMENT = re.compile(r"^\s*<!--\s*Image\s*\([^>]*\)\s*-->\s*$", re.I)
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
PAGE_IMAGE = re.compile(r"!\[[^\]]*(?:第\s*\d+\s*页)?原始页面图[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\([^\n)]*assets/page[-_]?\d+[^\n)]*\)", re.I)
TABLE = re.compile(r"^\s*\|.*\|\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
LIST = re.compile(r"^\s*(?:[-*+]\s+|[-*+]\s*[•·]\s*|\d+[.)、：:]\s*|[（(]?[一二三四五六七八九十百]+[)）、.]\s*)")
CHAPTER = re.compile(r"^第\s*[一二三四五六七八九十百零〇两0-9]+\s*章(?:\s+|：|:)?\s*.*$")
PART = re.compile(r"^(?:第\s*[一二三四五六七八九十百零〇两0-9]+\s*[篇部卷]|Part\s+\d+)\b.*$", re.I)
TOC_LEADER = re.compile(r"^(.*?)(?:\.{4,}|…{3,}|·{4,}|﹒{4,})\s*[.·… ]*\d+\s*$")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
URL = re.compile(r"https?\s*:\s*//\S+", re.I)
SCAN_FOOT = re.compile(r"^\s*\d*\s*籍\s*:\s*.*(?:SS\s*Q|SOS).*$", re.I)
PUNCT_END = tuple("。！？；：!?;”’）》】…")


@dataclass
class Stats:
    source: str
    destination: str
    title: str
    source_bytes: int = 0
    output_bytes: int = 0
    pages_detected: int = 0
    toc_pages_removed: int = 0
    page_comments_removed: int = 0
    page_headings_removed: int = 0
    conversion_image_comments_removed: int = 0
    repeated_furniture_removed: int = 0
    end_page_numbers_removed: int = 0
    heading_fixes: int = 0
    duplicate_title_lines_removed: int = 0
    list_marker_fixes: int = 0
    paragraph_blocks_reflowed: int = 0
    table_blocks_preserved: int = 0
    page_images_moved_after_text: int = 0
    ordinary_images_preserved_in_place: int = 0
    traditional_to_simplified: bool = False
    traditional_character_changes: int = 0
    image_refs_before: int = 0
    image_refs_after: int = 0
    image_refs_changed: bool = False
    image_reference_order_changed: bool = False
    visible_body_chars: int = 0
    meaningful_body_retention: float = 1.0


def strip_heading(s: str) -> str:
    s = s.strip()
    m = HEADING.match(s)
    return m.group(2).strip() if m else s


def norm(s: str) -> str:
    s = strip_heading(s).replace("　", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s.translate(str.maketrans({"﹕": "：", ":": "：", "—": "-", "－": "-"}))


def compact_key(s: str) -> str:
    return re.sub(r"\s+", "", norm(s))


def simplify(text: str, stats: Stats) -> str:
    if not CC or not text:
        return text
    protected: list[str] = []
    token = "__KEEP_%d__"

    def hold(m: re.Match[str]) -> str:
        protected.append(m.group(0))
        return token % (len(protected) - 1)

    tmp = IMAGE.sub(hold, text)
    tmp = URL.sub(hold, tmp)
    converted = CC.convert(tmp)
    for i, value in enumerate(protected):
        converted = converted.replace(token % i, value)
    stats.traditional_character_changes += sum(1 for a, b in zip(text, converted) if a != b) + abs(len(text) - len(converted))
    return converted


def split_pages(lines: list[str]) -> list[tuple[int, list[str]]]:
    pages: list[tuple[int, list[str]]] = []
    page = 0
    buf: list[str] = []
    saw = False
    for line in lines:
        m = PAGE_COMMENT.match(line)
        if m:
            saw = True
            if page or buf:
                pages.append((page, buf))
            page = int(m.group(1))
            buf = []
        else:
            buf.append(line)
    if page or buf:
        pages.append((page, buf))
    if not saw:
        return [(0, lines[:])]
    return pages


def page_text(block: list[str]) -> list[str]:
    out = []
    for line in block:
        s = line.strip()
        if not s or IMAGE.fullmatch(s) or IMAGE_COMMENT.match(s) or PAGE_HEADING.match(s):
            continue
        out.append(strip_heading(s))
    return out


def toc_score(block: list[str]) -> tuple[int, int, int, int]:
    texts = page_text(block)
    leaders = sum(bool(TOC_LEADER.match(x)) for x in texts)
    chapters = sum(bool(CHAPTER.match(norm(x))) for x in texts)
    directory = sum("目录" in re.sub(r"\s+", "", x) for x in texts[:4])
    chars = sum(len(x) for x in texts)
    return leaders, chapters, directory, chars


def detect_toc_pages(pages: list[tuple[int, list[str]]]) -> set[int]:
    if not pages or pages[0][0] == 0:
        return set()
    scan = pages[: min(30, len(pages))]
    start_i: int | None = None
    for i, (_, block) in enumerate(scan):
        leaders, chapters, directory, chars = toc_score(block)
        if directory or leaders >= 3 or (chapters >= 3 and chars < 5000):
            start_i = i
            break
    if start_i is None:
        return set()
    chosen: list[int] = []
    for i in range(start_i, len(scan)):
        pno, block = scan[i]
        leaders, chapters, directory, chars = toc_score(block)
        if i == start_i:
            chosen.append(pno)
            continue
        likely = leaders >= 2 or chapters >= 2 or directory or (chars < 1800 and (leaders + chapters) >= 1)
        if likely:
            chosen.append(pno)
            continue
        break
    return set(chosen)


def parse_toc_titles(pages: list[tuple[int, list[str]]], toc_pages: set[int], stats: Stats) -> dict[str, tuple[int, str]]:
    titles: dict[str, tuple[int, str]] = {}
    for pno, block in pages:
        if pno not in toc_pages:
            continue
        for raw in block:
            if IMAGE.fullmatch(raw.strip()) or IMAGE_COMMENT.match(raw) or PAGE_HEADING.match(raw):
                continue
            text = simplify(strip_heading(raw), stats)
            if not text:
                continue
            candidates: list[str] = []
            m = TOC_LEADER.match(text)
            if m:
                candidates.append(m.group(1).strip())
            elif HEADING.match(raw.strip()) or CHAPTER.match(norm(text)) or PART.match(norm(text)):
                candidates.append(text.strip())
            for candidate in candidates:
                candidate = norm(candidate)
                candidate = re.sub(r"^目录\s*", "", candidate).strip()
                if len(candidate) < 2 or len(candidate) > 140:
                    continue
                level = 2 if CHAPTER.match(candidate) or PART.match(candidate) else 3
                titles[compact_key(candidate)] = (level, candidate)
    return titles


def infer_title(source: Path, lines: list[str]) -> str:
    parent = source.parent.name.strip()
    parent = re.sub(r"^\d+[._、\-\s]*", "", parent)
    parent = re.sub(r"PDF版$", "", parent, flags=re.I).strip()
    if parent.startswith("《") and parent.endswith("》"):
        parent = parent[1:-1].strip()
    for raw in lines[:120]:
        m = HEADING.match(raw.strip())
        if not m or len(m.group(1)) != 1:
            continue
        t = norm(m.group(2))
        if not t or "目录" in t or CHAPTER.match(t) or len(t) > 60:
            continue
        t = re.sub(r"[°·•]+$", "", t).strip()
        if t:
            if parent and compact_key(parent) in compact_key(t):
                return parent
            if parent:
                return parent
            return t
    return parent or "未命名文档"


def image_refs(text: str) -> list[str]:
    return IMAGE.findall(text)


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


def repeated_furniture(pages: list[tuple[int, list[str]]], title: str) -> set[str]:
    counts: Counter[str] = Counter()
    page_count = max(1, len(pages))
    for _, block in pages:
        seen: set[str] = set()
        for raw in block:
            s = norm(raw)
            if not s or len(s) > 120 or IMAGE.fullmatch(raw.strip()) or HEADING.match(raw.strip()):
                continue
            seen.add(s)
        counts.update(seen)
    threshold = max(3, int(page_count * 0.08))
    result: set[str] = set()
    title_key = compact_key(title)
    for text, count in counts.items():
        if count < threshold:
            continue
        k = compact_key(text)
        promo = any(x in text for x in ("微信", "公众号", "内部资料", "课程网址", "电子版", "版权所有", "更多绝密", "朋友圈每日更新"))
        titleish = bool(title_key and (title_key in k or k in title_key) and len(k) <= len(title_key) + 12)
        if promo or titleish:
            result.add(text)
    return result


def fix_list_marker(line: str, stats: Stats) -> str:
    fixed = re.sub(r"^\s*[-*+]\s*[•·]\s*", "- ", line)
    if fixed != line:
        stats.list_marker_fixes += 1
    return fixed


def reflow_plain(lines: list[str], stats: Stats) -> list[str]:
    out: list[str] = []
    pending: list[str] = []

    def flush() -> None:
        nonlocal pending
        if not pending:
            return
        if len(pending) > 1:
            stats.paragraph_blocks_reflowed += 1
        text = ""
        for frag in pending:
            frag = frag.strip()
            if not text:
                text = frag
            elif re.search(r"[A-Za-z0-9]$", text) and re.match(r"^[A-Za-z0-9]", frag):
                text += " " + frag
            else:
                text += frag
        if text:
            out.append(text)
        pending = []

    for line in lines:
        s = line.strip()
        if not s:
            if pending and pending[-1].rstrip().endswith(PUNCT_END):
                flush()
            continue
        if HEADING.match(s) or LIST.match(s) or TABLE.match(s) or FENCE.match(s) or IMAGE.fullmatch(s) or s.startswith("> "):
            flush()
            out.append(line.rstrip())
            continue
        pending.append(line.rstrip())
        if s.endswith(PUNCT_END):
            flush()
    flush()
    return out


def clean_page(pno: int, block: list[str], title: str, toc_titles: dict[str, tuple[int, str]], furniture: set[str], stats: Stats) -> tuple[list[str], list[str]]:
    text_lines: list[str] = []
    page_images: list[str] = []
    meaningful = [x for x in block if x.strip() and not IMAGE.fullmatch(x.strip()) and not IMAGE_COMMENT.match(x)]

    for raw in block:
        s = raw.rstrip("\r\n")
        stripped = s.strip()
        if PAGE_HEADING.match(s):
            stats.page_headings_removed += 1
            continue
        if IMAGE_COMMENT.match(s):
            stats.conversion_image_comments_removed += 1
            continue
        im = IMAGE.fullmatch(stripped)
        if im:
            if PAGE_IMAGE.fullmatch(stripped):
                page_images.append(im.group(0))
            else:
                text_lines.append(im.group(0))
                stats.ordinary_images_preserved_in_place += 1
            continue
        if SCAN_FOOT.match(stripped):
            stats.repeated_furniture_removed += 1
            continue
        plain_original = strip_heading(stripped)
        if norm(plain_original) in furniture:
            stats.repeated_furniture_removed += 1
            continue
        if meaningful and stripped == meaningful[-1].strip():
            if re.fullmatch(r"\d{1,4}", stripped) and (not pno or int(stripped) in {pno, pno - 1, pno + 1}):
                stats.end_page_numbers_removed += 1
                continue
        if not stripped:
            text_lines.append("")
            continue

        hm = HEADING.match(stripped)
        plain = hm.group(2).strip() if hm else stripped
        plain = simplify(plain, stats)
        k = compact_key(plain)

        if compact_key(plain) == compact_key(title):
            stats.duplicate_title_lines_removed += 1
            continue
        evidence = toc_titles.get(k)
        if evidence:
            level, canonical = evidence
            new = f"{'#' * level} {canonical}"
            if stripped != new:
                stats.heading_fixes += 1
            text_lines.append(new)
            continue
        if CHAPTER.match(norm(plain)) or PART.match(norm(plain)):
            text_lines.append("## " + norm(plain))
            if not (hm and len(hm.group(1)) == 2):
                stats.heading_fixes += 1
            continue
        if hm:
            text_lines.append("### " + norm(plain))
            if len(hm.group(1)) != 3:
                stats.heading_fixes += 1
            continue

        line = simplify(s, stats)
        line = fix_list_marker(line, stats)
        text_lines.append(line)

    cleaned = reflow_plain(text_lines, stats)
    if page_images:
        stats.page_images_moved_after_text += len(page_images)
    return cleaned, page_images


def normalize_blank_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        if not line.strip():
            if out and out[-1] != "":
                out.append("")
        else:
            out.append(line.rstrip())
    while out and out[-1] == "":
        out.pop()
    return out


def run(source: Path, destination: Path | None = None, title: str | None = None) -> Stats:
    original = source.read_text(encoding="utf-8")
    lines = original.splitlines()
    pages = split_pages(lines)
    title = title or infer_title(source, lines)
    destination = destination or source.with_name(f"{title}.md")
    stats = Stats(str(source), str(destination), title, source_bytes=len(original.encode("utf-8")))
    stats.pages_detected = len(pages) if pages and pages[0][0] else 0
    before_images = image_refs(original)
    stats.image_refs_before = len(before_images)

    toc_pages = detect_toc_pages(pages)
    stats.toc_pages_removed = len(toc_pages)
    toc_titles = parse_toc_titles(pages, toc_pages, stats)
    furniture = repeated_furniture(pages, title)

    output: list[str] = [f"# {title}", ""]
    toc_page_images: list[str] = []
    body_source_parts: list[str] = []

    for pno, block in pages:
        if pno:
            stats.page_comments_removed += 1
        if pno in toc_pages:
            for raw in block:
                if IMAGE_COMMENT.match(raw):
                    stats.conversion_image_comments_removed += 1
                    continue
                im = IMAGE.fullmatch(raw.strip())
                if im:
                    toc_page_images.append(im.group(0))
            continue

        body_source_parts.extend(block)
        cleaned, page_imgs = clean_page(pno, block, title, toc_titles, furniture, stats)
        if cleaned:
            if output and output[-1] != "":
                output.append("")
            output.extend(cleaned)
        if page_imgs:
            if output and output[-1] != "":
                output.append("")
            output.extend(page_imgs)

    if toc_page_images:
        output[2:2] = ["**目录**", ""] + toc_page_images + [""]
        stats.page_images_moved_after_text += len(toc_page_images)

    output = normalize_blank_lines(output)
    final = "\n".join(output).strip() + "\n"

    after_images = image_refs(final)
    stats.image_refs_after = len(after_images)
    stats.image_reference_order_changed = before_images != after_images
    stats.image_refs_changed = Counter(before_images) != Counter(after_images)
    stats.traditional_to_simplified = stats.traditional_character_changes > 0

    if stats.image_refs_changed:
        raise RuntimeError("Markdown image references were added, removed, duplicated, or path-modified; refusing write")
    if re.search(r"^\s*<!--\s*page\s*:", final, re.M | re.I):
        raise RuntimeError("page comments remain")
    if IMAGE_COMMENT.search(final):
        raise RuntimeError("image conversion comments remain")
    if len(re.findall(r"^#\s+", final, re.M)) != 1:
        raise RuntimeError("output must contain exactly one H1")

    before_len = max(1, meaningful_len("\n".join(body_source_parts)))
    after_len = meaningful_len(final)
    stats.meaningful_body_retention = min(1.0, after_len / before_len)
    if stats.meaningful_body_retention < 0.90:
        raise RuntimeError(f"meaningful body retention too low: {stats.meaningful_body_retention:.4f}")

    stats.visible_body_chars = visible_chars(final)
    stats.output_bytes = len(final.encode("utf-8"))
    destination.write_text(final, encoding="utf-8")
    if source.resolve() != destination.resolve():
        source.unlink()
    return stats


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--destination")
    p.add_argument("--title")
    p.add_argument("--report")
    a = p.parse_args()
    source = Path(a.source)
    if not source.is_file():
        raise SystemExit(f"source not found: {source}")
    destination = Path(a.destination) if a.destination else None
    stats = run(source, destination, a.title)
    payload = json.dumps(asdict(stats), ensure_ascii=False, indent=2)
    print(payload)
    if a.report:
        Path(a.report).write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
