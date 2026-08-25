#!/usr/bin/env python3
"""Repair semantic Markdown residuals that syntax/date based checks cannot catch.

This pass is deliberately evidence-driven:
1. A known OCR title sequence in 《穷人的底层逻辑》 is restored from exact
   title prefixes already present in the source text.
2. The textual TOC in 《人性背后隐藏的邪恶密码》 is removed using the
   unambiguous numbering reset after the preserved page-008 image.
3. Explicit `□...` section markers are promoted when a short title/body
   boundary can be proven from punctuation or a conservative body-starter set.

All Markdown image references are preserved exactly as a multiset. The script
never uses Git modification time or a historical "format" commit as proof of
completion; current content is the authority.
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

POVERTY_PATH = Path("temp/《穷人的底层逻辑》/index.md")
EVIL_PATH = Path("temp/《人性背后隐藏的邪恶密码》/index.md")

# These are not invented labels: each exact string is visibly glued to the
# first sentence of a section in the current OCR-derived source, before the
# first already-correct `## 穷人混在穷人圈` section.
POVERTY_TITLES = [
    "穷人的饥饿思维",
    "穷人只有一个鸡蛋",
    "穷人占据不利地形",
    "穷人是永远的弱者",
    "穷人是社会的基础",
    "穷人是一种资源",
    "穷人被支配",
    "穷人不安全",
    "穷人容易上当",
    "穷人劳动不止",
    "穷人恩重如山",
    "穷人是颗螺丝钉",
    "穷人没法不志短",
    "穷人为富人输血",
    "穷人后富起来",
    "穷人不要感恩戴德",
    "穷人幻想现代化",
    "穷人要奋斗",
    "素养创造财富",
    "靠人推是走不远的",
    "穷人要有思想",
    "穷人要有激情",
    "你是穷人你怕什么",
    "穷人重视手艺",
    "穷人最有革命性",
    "把幻想变成理想",
    "始终保持斗志",
    "发财是件苦差事",
]

# OCR body starts commonly found immediately after a boxed section label.
# Matching is allowed only after at least 4 title characters and only if a
# substantial body remains, so ordinary short phrases are not promoted.
BODY_STARTERS = [
    "所谓", "现实生活中", "在现实生活中", "心理学", "心理学家",
    "通常", "一般来说", "长期以来", "人们常说", "人们", "一个人",
    "有的人", "有人", "社会", "生活中", "人生", "其实", "对于",
    "任何人", "大量的", "研究表明", "研究发现", "怎样", "要培养",
    "要想", "要使", "首先", "当一个", "当人", "如果一个", "如果你",
    "成功型", "软弱", "最佳的", "我们", "许多人", "很多人", "古人",
    "现代", "现实中", "面对", "所谓的", "每个人", "人的", "孩子",
]
BODY_STARTERS = sorted(set(BODY_STARTERS), key=len, reverse=True)


def image_refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def normalize_blanks(lines: list[str]) -> list[str]:
    out: list[str] = []
    for raw in lines:
        x = raw.rstrip()
        if not x:
            if out and out[-1] != "":
                out.append("")
        else:
            out.append(x)
    while out and out[-1] == "":
        out.pop()
    return out


def verify(path: Path, before: str, after: str) -> None:
    if image_refs(before) != image_refs(after):
        raise RuntimeError(f"{path}: Markdown image references changed")
    if len(re.findall(r"^#\s+", after, flags=re.M)) != 1:
        raise RuntimeError(f"{path}: expected exactly one H1 after repair")


def repair_poverty(text: str) -> tuple[str, dict]:
    lines = text.splitlines()
    title_set = set(POVERTY_TITLES)
    found = set()
    splits = []
    out: list[str] = []
    before_first_existing = True

    # Longest first protects titles sharing prefixes.
    titles = sorted(POVERTY_TITLES, key=len, reverse=True)
    for idx, raw in enumerate(lines, 1):
        s = raw.strip()
        if s == "## 穷人混在穷人圈":
            before_first_existing = False
        if before_first_existing and not H.match(s) and s:
            matched = None
            for title in titles:
                if s.startswith(title) and len(s) > len(title):
                    remainder = s[len(title):].lstrip(" ：:，,。；;、")
                    if len(remainder) >= 4:
                        matched = (title, remainder)
                        break
            if matched:
                title, remainder = matched
                out.append(f"## {title}")
                out.append("")
                out.append(remainder)
                found.add(title)
                splits.append({"line": idx, "title": title})
                continue

        # This is an OCR-corrupted pseudo-heading, not a semantic title. Keep
        # its text to avoid deleting source material, but remove heading syntax.
        if s.startswith("## 种种困难，领导一个团饮创乐奖功警"):
            out.append(s[3:].strip())
            continue
        out.append(raw.rstrip())

    after = "\n".join(normalize_blanks(out)) + "\n"
    unresolved = [t for t in POVERTY_TITLES if t not in found and f"## {t}" not in after]
    return after, {
        "titles_expected": len(POVERTY_TITLES),
        "titles_split": len(splits),
        "splits": splits,
        "unresolved_titles": unresolved,
    }


def repair_evil_toc(text: str) -> tuple[str, dict]:
    lines = text.splitlines()
    page8 = None
    body = None
    for i, raw in enumerate(lines):
        if "assets/page-008.png" in raw and IMAGE.search(raw):
            page8 = i
            break
    if page8 is not None:
        for i in range(page8 + 1, min(len(lines), page8 + 80)):
            if re.match(r"^\s*1\s*[.．、]\s*为什么", lines[i]):
                body = i
                break
    if page8 is None or body is None:
        return text, {"changed": False, "reason": "page8/body reset anchor not proven"}

    out: list[str] = []
    removed = 0
    for i, raw in enumerate(lines):
        if i >= body:
            out.append(raw.rstrip())
            continue
        s = raw.strip()
        if H.match(s) and len(H.match(s).group(1)) == 1:
            out.append(raw.rstrip())
        elif IMAGE.search(raw):
            # Preserve all original page images from the visual TOC.
            out.append(raw.rstrip())
        elif not s:
            out.append("")
        else:
            # Everything else before the numbering reset is extracted TOC text.
            removed += 1
    after = "\n".join(normalize_blanks(out)) + "\n"
    return after, {
        "changed": after != text.replace("\r\n", "\n"),
        "page8_line": page8 + 1,
        "body_reset_line": body + 1,
        "toc_text_lines_removed": removed,
    }


def split_box_payload(payload: str) -> tuple[str, str] | None:
    payload = payload.strip()
    if not payload:
        return None
    # If the source already contains an explicit question mark, it is the
    # strongest possible title boundary.
    qm_positions = [p for p in (payload.find("？"), payload.find("?")) if 0 <= p <= 80]
    if qm_positions:
        p = min(qm_positions)
        title = payload[: p + 1].strip()
        body = payload[p + 1 :].strip()
        if 3 <= len(title) <= 80 and len(body) >= 12:
            return title, body

    # Otherwise, use a conservative lexical boundary.
    best = None
    for starter in BODY_STARTERS:
        pos = payload.find(starter, 4)
        if pos < 0 or pos > 60:
            continue
        title = payload[:pos].strip(" ：:，,。；;、")
        body = payload[pos:].strip()
        if not (4 <= len(title) <= 55 and len(body) >= 18):
            continue
        if best is None or pos < best[0]:
            best = (pos, title, body, starter)
    if best:
        _, title, body, _ = best
        return title, body
    return None


def repair_box_markers(text: str) -> tuple[str, dict]:
    out: list[str] = []
    promoted = []
    unresolved = []
    for idx, raw in enumerate(text.splitlines(), 1):
        m = BOX.match(raw)
        if not m:
            out.append(raw.rstrip())
            continue
        split = split_box_payload(m.group(1))
        if not split:
            unresolved.append({"line": idx, "excerpt": m.group(1)[:140]})
            out.append(raw.rstrip())
            continue
        title, body = split
        out.append(f"## {title}")
        out.append("")
        out.append(body)
        promoted.append({"line": idx, "title": title})
    after = "\n".join(normalize_blanks(out)) + "\n"
    return after, {
        "box_headings_promoted": len(promoted),
        "box_promoted": promoted,
        "box_markers_unresolved": unresolved,
    }


def process(path: Path, apply: bool) -> dict:
    original = path.read_text(encoding="utf-8-sig")
    text = original
    details: dict = {}

    if path == POVERTY_PATH:
        text, details["poverty_semantic_titles"] = repair_poverty(text)
    if path == EVIL_PATH:
        text, details["leading_toc"] = repair_evil_toc(text)

    # Explicit boxed section markers are independently strong evidence and can
    # occur in more than one book.
    if BOX.search(text):
        text, details["boxed_sections"] = repair_box_markers(text)

    verify(path, original, text)
    changed = text != original.replace("\r\n", "\n")
    if changed and apply:
        path.write_text(text, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "applied": bool(changed and apply),
        "image_refs": sum(image_refs(original).values()),
        "details": details,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="temp")
    p.add_argument("--report", default="temp/.semantic-residual-repair.json")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    root = Path(args.root)
    targets = sorted(x for x in root.rglob("*.md") if x.is_file() and not x.name.startswith("."))
    results = []
    errors = []
    for path in targets:
        try:
            results.append(process(path, args.apply))
        except Exception as exc:
            errors.append({"path": str(path), "error": str(exc)})

    unresolved_boxes = []
    for item in results:
        for x in item.get("details", {}).get("boxed_sections", {}).get("box_markers_unresolved", []):
            unresolved_boxes.append({"path": item["path"], **x})
    poverty_unresolved = []
    for item in results:
        poverty_unresolved.extend(item.get("details", {}).get("poverty_semantic_titles", {}).get("unresolved_titles", []))

    payload = {
        "policy": {
            "completion_basis": "current semantic/structural content, not file modified date or historical commit message",
            "image_invariant": "exact Markdown image reference multiset preserved",
        },
        "summary": {
            "markdown_files_scanned": len(targets),
            "files_changed": sum(bool(x["applied"]) for x in results),
            "box_headings_promoted": sum(x.get("details", {}).get("boxed_sections", {}).get("box_headings_promoted", 0) for x in results),
            "box_markers_unresolved": len(unresolved_boxes),
            "poverty_titles_unresolved": len(poverty_unresolved),
            "image_refs_checked": sum(x["image_refs"] for x in results),
            "errors": len(errors),
        },
        "results": [x for x in results if x["changed"] or x.get("details")],
        "unresolved_box_markers": unresolved_boxes,
        "errors": errors,
    }
    Path(args.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
