#!/usr/bin/env python3
"""Dry-run semantic boundary analysis for `□...` headings.

No book content is changed. A split is proposed only when the source box marker
proves a section start and a strong sentence-level body opener proves where the
short title ends. This avoids the earlier unsafe generic lexical splitter.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

TARGET = Path("temp/《人性难题宝典1-9》.md")
OUT = Path("temp/.box-heading-boundary-analysis.json")
BOX = re.compile(r"^\s*[□▢▫]\s*(.+?)\s*$")

TITLE_START = re.compile(r"^(?:如何|为什么|怎样|怎么|为何|什么|哪些|哪种|是否|别让|不可|不要|学会|用什么)")
STARTERS = sorted({
    "在现实生活中", "现实生活中", "在实际交往中", "实际交往中",
    "心理学已经", "心理学家", "心理学", "没有人", "生活中常", "生活中",
    "古往今来", "大千世界", "随着年龄", "随着社会", "随着",
    "英国哲学家", "英国", "美国", "法国", "德国", "日本",
    "研究表明", "研究发现", "研究", "所谓", "人们常说", "人们往往", "人们",
    "有的人", "有人", "这种类型的人", "这种类型", "这是个", "这是一个",
    "拒绝别人的要求", "拒绝别人", "对于爱", "对于那些", "对于这种", "对于",
    "最可怕的人", "最可怕", "尖酸刻薄型的人", "成功者", "成功的人",
    "通常情况下", "通常", "一般来说", "一般而言",
    "要避免", "要培养", "要想", "要使", "只要你", "只要",
    "如果不幸", "如果一个", "如果你", "如果", "当一个", "当你",
    "猜疑产生", "嫉妒是", "嫉妒", "古人", "俗话说", "俗话",
    "一位", "有位", "一个故事", "有一个故事", "一天", "一次",
    "父母", "老师", "社会上", "在社会上", "在人际交往中", "人际交往中",
    "从心理学", "从社会学", "从某种意义上", "事实上", "其实",
}, key=len, reverse=True)


def propose(payload: str):
    payload = payload.strip()
    # Explicit punctuation boundary is strongest.
    for q in ("？", "?"):
        p = payload.find(q)
        if 3 <= p <= 70:
            title = payload[:p+1].strip()
            body = payload[p+1:].strip()
            if len(body) >= 15:
                return title, body, f"punctuation:{q}"

    if not TITLE_START.match(payload):
        return None

    best = None
    for starter in STARTERS:
        p = payload.find(starter, 5)
        if p < 0 or p > 60:
            continue
        title = payload[:p].strip(" ：:，,。；;、")
        body = payload[p:].strip()
        if not (4 <= len(title) <= 48 and len(body) >= 18):
            continue
        if title.endswith(("的", "和", "与", "或", "及", "在", "把", "让", "对", "向")):
            continue
        candidate = (p, title, body, starter)
        if best is None or p < best[0]:
            best = candidate
    if best:
        _, title, body, starter = best
        return title, body, f"starter:{starter}"
    return None


def main() -> None:
    text = TARGET.read_text(encoding="utf-8-sig")
    candidates = []
    unresolved = []
    markers = 0
    for i, raw in enumerate(text.splitlines(), 1):
        m = BOX.match(raw)
        if not m:
            continue
        markers += 1
        payload = m.group(1).strip()
        split = propose(payload)
        if split:
            title, body, evidence = split
            candidates.append({
                "line": i,
                "title": title,
                "evidence": evidence,
                "body_prefix": body[:220],
                "source_prefix": payload[:320],
            })
        else:
            unresolved.append({"line": i, "source_prefix": payload[:320]})
    payload = {
        "policy": "dry-run only; no Markdown content changed",
        "summary": {
            "box_markers": markers,
            "high_confidence_candidates": len(candidates),
            "unresolved": len(unresolved),
        },
        "candidates": candidates,
        "unresolved": unresolved,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
