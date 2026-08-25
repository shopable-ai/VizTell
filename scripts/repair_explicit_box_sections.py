#!/usr/bin/env python3
"""Recover explicit `□...` section headings from OCR-derived Markdown.

Unlike semantic guessing, the box glyph is source evidence that a new topic
starts here. We still split the title/body only when a conservative boundary is
provable. Unresolved markers remain untouched and are reported.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

H = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
BOX = re.compile(r"^\s*[□▢▫]\s*(.+?)\s*$")

# Strong body openers observed across reference/handbook prose. Earlier match
# wins; matching begins only after >=4 title chars.
STARTERS = sorted({
    "所谓", "所谓的", "现实生活中", "在现实生活中", "现实中", "生活中",
    "心理学已经", "心理学家", "心理学", "通常", "一般来说", "长期以来",
    "人们常说", "人们往往", "人们", "一个人", "有的人", "有人", "许多人",
    "很多人", "大量的", "研究表明", "研究发现", "社会", "人生", "其实",
    "对于", "任何人", "怎样", "要培养", "要想", "要使", "首先", "其次",
    "当一个", "当人", "如果一个", "如果你", "我们", "面对", "现代",
    "古人", "每个人", "人的", "孩子", "最佳的", "软弱", "成功型",
    "人格障碍", "家庭", "父母", "婚姻", "工作", "竞争", "嫉妒", "猜疑",
}, key=len, reverse=True)


def image_refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def normalize(lines: list[str]) -> str:
    out = []
    for raw in lines:
        x = raw.rstrip()
        if x:
            out.append(x)
        elif out and out[-1] != "":
            out.append("")
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) + "\n"


def split_payload(payload: str):
    payload = payload.strip()
    # Explicit punctuation is strongest.
    q = [i for i in (payload.find("？"), payload.find("?")) if 3 <= i <= 80]
    if q:
        p = min(q)
        title, body = payload[:p+1].strip(), payload[p+1:].strip()
        if len(body) >= 12:
            return title, body, "question_mark"

    # An em dash/colon after a compact title can also be explicit source syntax.
    for token in ("——", "：", ":"):
        p = payload.find(token, 4, 70)
        if p >= 4:
            title, body = payload[:p].strip(), payload[p+len(token):].strip()
            if 4 <= len(title) <= 60 and len(body) >= 18:
                return title, body, f"delimiter:{token}"

    best = None
    for starter in STARTERS:
        p = payload.find(starter, 4)
        if p < 0 or p > 60:
            continue
        title = payload[:p].strip(" ：:，,。；;、")
        body = payload[p:].strip()
        if not (4 <= len(title) <= 55 and len(body) >= 18):
            continue
        # Avoid splitting a grammatical title immediately after generic words.
        if title.endswith(("的", "和", "与", "或", "及", "在", "对", "把", "让")):
            continue
        candidate = (p, title, body, starter)
        if best is None or p < best[0]:
            best = candidate
    if best:
        _, title, body, starter = best
        return title, body, f"starter:{starter}"
    return None


def process(path: Path, apply: bool):
    before = path.read_text(encoding="utf-8-sig")
    before_images = image_refs(before)
    out = []
    promoted = []
    unresolved = []
    markers = 0
    for i, raw in enumerate(before.splitlines(), 1):
        m = BOX.match(raw)
        if not m:
            out.append(raw.rstrip())
            continue
        markers += 1
        split = split_payload(m.group(1))
        if not split:
            unresolved.append({"line": i, "excerpt": m.group(1)[:180]})
            out.append(raw.rstrip())
            continue
        title, body, evidence = split
        out.extend([f"## {title}", "", body])
        promoted.append({"line": i, "title": title, "evidence": evidence})

    after = normalize(out)
    if before_images != image_refs(after):
        raise RuntimeError(f"{path}: image references changed")
    if len(re.findall(r"^#\s+", after, re.M)) != 1:
        raise RuntimeError(f"{path}: expected exactly one H1")
    changed = after != before.replace("\r\n", "\n")
    if changed and apply:
        path.write_text(after, encoding="utf-8")
    return {
        "path": str(path), "markers": markers, "changed": changed,
        "applied": bool(changed and apply), "promoted": promoted,
        "unresolved": unresolved, "image_refs": sum(before_images.values()),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="temp")
    p.add_argument("--report", default="temp/.boxed-section-repair.json")
    p.add_argument("--apply", action="store_true")
    a = p.parse_args()
    targets = sorted(x for x in Path(a.root).rglob("*.md") if x.is_file() and not x.name.startswith("."))
    results, errors = [], []
    for path in targets:
        try:
            item = process(path, a.apply)
            if item["markers"]:
                results.append(item)
        except Exception as exc:
            errors.append({"path": str(path), "error": str(exc)})
    unresolved = [{"path": x["path"], **u} for x in results for u in x["unresolved"]]
    payload = {
        "summary": {
            "markdown_files_scanned": len(targets),
            "files_with_box_markers": len(results),
            "files_changed": sum(x["applied"] for x in results),
            "markers_found": sum(x["markers"] for x in results),
            "headings_promoted": sum(len(x["promoted"]) for x in results),
            "markers_unresolved": len(unresolved),
            "errors": len(errors),
        },
        "results": results,
        "unresolved": unresolved,
        "errors": errors,
    }
    Path(a.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
