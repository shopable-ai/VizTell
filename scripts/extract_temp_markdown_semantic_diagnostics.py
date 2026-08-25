#!/usr/bin/env python3
"""Extract compact semantic-format diagnostics for Markdown files that may false-pass.

The script does not modify book content. It exists because modification dates,
commit messages, syntax checks and heading counts cannot prove that OCR-derived
semantic headings were actually recovered.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

TARGETS = [
    "temp/《穷人的底层逻辑》/index.md",
    "temp/《人性商战(线下3天2夜全文字版)》.md",
    "temp/《人性难题宝典1-9》.md",
    "temp/《揭秘人性密码1》/index.md",
    "temp/《缠论108课详解彩色修订典藏版》/index.md",
    "temp/《语言的魔力》/index.md",
    "temp/直播复盘录.md",
]

H = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
STRUCT = re.compile(
    r"第\s*[一二三四五六七八九十百零〇两0-9]+\s*(?:章|节|课|讲|天|篇|部分|部|卷)"
    r"|(?:上篇|中篇|下篇|序言|前言|后记|附录|目录|开篇|第一天|第二天|第三天|上午|下午|晚上)"
    r"|\b(?:Chapter|Part)\s+[0-9IVXLC]+\b",
    re.I,
)
PROSE_STARTERS = (
    "据说", "有一个", "很多", "一般", "我们", "你", "当", "在", "如果", "因为",
    "为什么", "对于", "所谓", "人们", "一个", "今天", "那么", "其实", "可以", "这",
    "大家", "想要", "假如", "从前", "曾经", "有人", "首先", "其次", "现代", "古代",
)


def compact_excerpt(s: str, n: int = 260) -> str:
    s = re.sub(r"\s+", " ", s.strip())
    return s[:n]


def first_text_snippets(lines: list[str], limit: int = 45) -> list[dict]:
    out = []
    for i, raw in enumerate(lines, 1):
        s = raw.strip()
        if not s or IMAGE.fullmatch(s) or s.startswith("<!--"):
            continue
        out.append({"line": i, "text": compact_excerpt(s)})
        if len(out) >= limit:
            break
    return out


def structure_hits(text: str, limit: int = 160) -> list[dict]:
    out = []
    for m in STRUCT.finditer(text):
        a = max(0, m.start() - 90)
        b = min(len(text), m.end() + 180)
        out.append({"match": m.group(0), "context": compact_excerpt(text[a:b], 330)})
        if len(out) >= limit:
            break
    return out


def glued_prefix_candidates(lines: list[str], limit: int = 120) -> list[dict]:
    """Diagnose short title-like prefixes glued to an ordinary prose starter.

    This is deliberately diagnostic only. It does not promote candidates.
    """
    out = []
    seen = set()
    starters = "|".join(map(re.escape, sorted(PROSE_STARTERS, key=len, reverse=True)))
    rx = re.compile(rf"^([^#|!<>]{{2,32}}?)(?=({starters}))")
    for i, raw in enumerate(lines, 1):
        s = raw.strip()
        if not s or len(s) < 28 or H.match(s) or IMAGE.search(s) or s.startswith(("|", "```", "~~~")):
            continue
        m = rx.match(s)
        if not m:
            continue
        prefix = m.group(1).strip(" ：:，,。；;!?！？、.-—")
        if not (2 <= len(prefix) <= 28):
            continue
        # Filter ordinary grammatical fragments aggressively.
        if prefix.endswith(("，", "。", "的", "了", "是", "和", "与", "或", "但", "而")):
            continue
        key = prefix.replace(" ", "")
        if key in seen:
            continue
        seen.add(key)
        out.append({"line": i, "prefix": prefix, "starter": m.group(2), "context": compact_excerpt(s, 360)})
        if len(out) >= limit:
            break
    return out


def keyword_contexts(text: str, terms: list[str], limit_each: int = 50) -> dict[str, list[str]]:
    result = {}
    for term in terms:
        vals = []
        start = 0
        while len(vals) < limit_each:
            pos = text.find(term, start)
            if pos < 0:
                break
            vals.append(compact_excerpt(text[max(0, pos - 40):pos + 260], 330))
            start = pos + len(term)
        if vals:
            result[term] = vals
    return result


def diagnose(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    headings = []
    for i, raw in enumerate(lines, 1):
        m = H.match(raw.strip())
        if m:
            headings.append({"line": i, "level": len(m.group(1)), "text": m.group(2).strip()})
            if len(headings) >= 240:
                break

    line_lengths = sorted(((len(x), i + 1) for i, x in enumerate(lines)), reverse=True)[:20]
    nonblank = [x.strip() for x in lines if x.strip()]
    return {
        "path": str(path),
        "metrics": {
            "bytes": len(text.encode("utf-8")),
            "characters": len(text),
            "lines": len(lines),
            "nonblank_lines": len(nonblank),
            "paragraphish_lines": sum(1 for x in nonblank if not H.match(x) and not IMAGE.fullmatch(x)),
            "headings": len(headings),
            "images": len(IMAGE.findall(text)),
            "max_line_length": max((len(x) for x in lines), default=0),
        },
        "first_text_snippets": first_text_snippets(lines),
        "headings": headings,
        "structure_hits": structure_hits(text),
        "glued_prefix_candidates": glued_prefix_candidates(lines),
        "longest_lines": [{"line": i, "length": n, "excerpt": compact_excerpt(lines[i-1], 420)} for n, i in line_lengths],
        "focused_contexts": keyword_contexts(
            text,
            [
                "穷人的", "富人的", "穷人只有", "穷人思维", "富人思维",
                "第一天", "第二天", "第三天", "上午", "下午", "晚上",
                "第一章", "第二章", "第三章", "第一课", "第二课", "第三课",
                "语言的魔力", "前言", "序言", "后记", "附录",
            ],
        ),
    }


def main() -> None:
    docs = []
    for raw in TARGETS:
        p = Path(raw)
        if p.exists():
            docs.append(diagnose(p))
    payload = {
        "purpose": "semantic residual inspection; content is not modified",
        "rule": "Git dates/format commits are supporting metadata only; current content decides completion",
        "documents": docs,
    }
    out = Path("temp/.semantic-format-diagnostics.json")
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"documents": len(docs), "output": str(out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
