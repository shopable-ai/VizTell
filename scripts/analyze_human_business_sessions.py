#!/usr/bin/env python3
"""Dry-run boundary analysis for the 3-day/2-night human-business transcript.

The source is a speech-to-text transcript with 400k+ visible characters and no
body headings. This script extracts only explicit course/session transition
language and nearby context. It never edits the book.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

PATH = Path("temp/《人性商战(线下3天2夜全文字版)》.md")
OUT = Path("temp/.human-business-session-analysis.json")

PHRASES = [
    "上午的课程到此结束", "上午课程到此结束", "下午的课程到此结束", "下午课程到此结束",
    "今天上午", "今天下午", "今天晚上", "今晚", "明天上午", "明天下午", "明天晚上",
    "第二天", "第三天", "第一天", "三天两晚", "三天两夜",
    "下午的主题", "上午的主题", "晚上的主题", "今天的主题", "接下来的主题",
    "上午首先为大家分享", "下午首先为大家分享", "接下来为大家分享",
    "继续接着昨天", "接着昨天", "昨天上午", "昨天下午", "昨天晚上",
    "上午好", "下午好", "晚上好", "早上好",
    "中午休息", "下午上课时间", "明天上课时间", "今天课程到此结束",
]
PATTERN = re.compile("|".join(re.escape(x) for x in sorted(PHRASES, key=len, reverse=True)))


def excerpt(s: str, n: int = 560) -> str:
    return re.sub(r"\s+", " ", s.strip())[:n]


def main() -> None:
    text = PATH.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    matches = []
    for i, raw in enumerate(lines):
        for m in PATTERN.finditer(raw):
            before = raw[max(0, m.start()-220):m.start()]
            after = raw[m.end():m.end()+420]
            matches.append({
                "line": i + 1,
                "phrase": m.group(0),
                "char_in_line": m.start(),
                "before": excerpt(before, 260),
                "after": excerpt(after, 460),
                "line_prefix": excerpt(raw, 820),
            })
    # Nearby sequential duplicates are useful evidence but collapse exact repeats.
    seen = set()
    dedup = []
    for x in matches:
        key = (x["line"], x["phrase"], x["char_in_line"])
        if key not in seen:
            seen.add(key)
            dedup.append(x)
    payload = {
        "policy": "dry-run only; explicit course/session transition language is evidence, current content is authoritative",
        "summary": {"matches": len(dedup), "lines": len(lines)},
        "matches": dedup,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
