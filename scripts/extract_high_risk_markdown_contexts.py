#!/usr/bin/env python3
"""Create a compact semantic context file for high-risk Markdown review.

Reads temp/.semantic-completeness-audit.json and extracts only evidence useful
for repairing `needs_review_high` documents. Does not modify book content.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

AUDIT = Path("temp/.semantic-completeness-audit.json")
OUT = Path("temp/.semantic-high-risk-contexts.json")
H = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
STRUCT = re.compile(
    r"(?:第\s*[一二三四五六七八九十百零〇两0-9]+\s*(?:天|章|节|课|讲|篇|部分|部|卷)|"
    r"(?:第一|第二|第三|第四|第五|第六|第七|第八|第九|第十)\s*(?:天|晚|上午|下午)|"
    r"上午|下午|晚上|夜场|开场|复盘|总结|课程|模块|主题|环节|阶段|Part\s+\d+)"
    r"|^\s*[□▢▫]"
    r"|^\s*\d{1,4}\s*[.．、:：]",
    re.I,
)
CONTACT = re.compile(r"(?i)(?:加\s*我\s*微信|微信号|wx\s*[:：=]|vx\s*[:：=]|薇芯\s*[:：=]|薇信\s*[:：=]|公号\s*[:：])")


def excerpt(s: str, n: int = 300) -> str:
    return re.sub(r"\s+", " ", s.strip())[:n]


def context(lines: list[str], idx: int, radius: int = 2) -> dict:
    a = max(0, idx - radius)
    b = min(len(lines), idx + radius + 1)
    return {
        "line": idx + 1,
        "context": [{"line": j + 1, "text": excerpt(lines[j], 260)} for j in range(a, b) if lines[j].strip() and not IMAGE.fullmatch(lines[j].strip())],
    }


def extract(path: Path, audit_item: dict) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    first = []
    headings = []
    structural = []
    oversized = []
    contact = []
    giant = []

    for i, raw in enumerate(lines):
        s = raw.strip()
        if not s or IMAGE.fullmatch(s) or s.startswith("<!--"):
            continue
        if len(first) < 100:
            first.append({"line": i + 1, "text": excerpt(s, 320)})
        hm = H.match(s)
        if hm:
            item = {"line": i + 1, "level": len(hm.group(1)), "text": excerpt(hm.group(2), 500), "length": len(hm.group(2))}
            if len(headings) < 250:
                headings.append(item)
            if len(hm.group(2)) > 180 and len(oversized) < 80:
                oversized.append(item)
        if len(s) <= 220 and STRUCT.search(s) and len(structural) < 300:
            structural.append({"line": i + 1, "text": excerpt(s, 360)})
        if CONTACT.search(s) and len(contact) < 80:
            contact.append(context(lines, i, 1))
        if len(raw) > 2500 and len(giant) < 20:
            giant.append({"line": i + 1, "length": len(raw), "prefix": excerpt(raw, 700)})

    return {
        "path": str(path),
        "audit_status": audit_item.get("status"),
        "audit_metrics": audit_item.get("metrics", {}),
        "audit_issues": audit_item.get("issues", []),
        "first_text_lines": first,
        "headings": headings,
        "structural_candidates": structural,
        "oversized_headings": oversized,
        "contact_contexts": contact,
        "giant_lines": giant,
    }


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    high = [x for x in audit.get("review", []) if x.get("status") == "needs_review_high"]
    docs = []
    for item in high:
        p = Path(item["path"])
        if p.exists():
            docs.append(extract(p, item))
    payload = {
        "summary": {"high_risk_documents": len(docs)},
        "documents": docs,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
