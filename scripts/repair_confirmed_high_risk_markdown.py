#!/usr/bin/env python3
"""Repair confirmed high-risk semantic false passes without guessing.

Cases are evidence-backed by current-content diagnostics:
- 008《布局锦囊3.0》: remove the extracted textual TOC from item 934 through
  item 1052 / 后记 while preserving any page images inside that range.
- 《百发百中攻心术》: repair the repeated page-header artifact
  `第20章让孩子听话的攻心术` when it has been glued into body text.
- Clean only clearly orphaned promotional CTA fragments left after removal of
  direct contact credentials, and repair one proven `B端消费者` OCR boundary.

Markdown image references must remain exactly unchanged. Untouched lines are
preserved byte-for-byte except for the repository-standard LF newline encoding;
this script must never perform global whitespace normalization.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")

LAYOUT3 = Path("temp/008《布局锦囊3.0》/index.md")
GONGXIN = Path("temp/《百发百中攻心术》/index.md")

ORPHAN_PROMO_SENTENCES = [
    re.compile(r"(?:更多落地细节|更多布局秘密)[，,]?\s*添加作者(?:获取内部分享|内部悄悄分享|获取[^。！？]{0,30})[。！？]?"),
    re.compile(r"要是想不出来可以添加来问我[。！？]?"),
    re.compile(r"可以添加作者获取经济风向标小模板[。！？]?"),
    re.compile(r"大家添加保证不会\d*[。！？]?"),
]


def refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def join_lines(lines: list[str], final_newline: bool = True) -> str:
    text = "\n".join(lines)
    if final_newline and not text.endswith("\n"):
        text += "\n"
    return text


def repair_layout3(text: str) -> tuple[str, dict]:
    lines = text.splitlines()
    start = end = None
    for i, raw in enumerate(lines):
        if start is None and "934个布局锦囊" in raw.replace(" ", ""):
            start = i
        if start is not None and "1052个布局锦囊" in raw.replace(" ", "") and "后记" in raw:
            end = i
            break
    if start is None or end is None or end < start or end - start > 120:
        return text, {"changed": False, "reason": "TOC anchors not proven"}

    out: list[str] = []
    removed: list[int] = []
    preserved_images = 0
    for i, raw in enumerate(lines):
        if start <= i <= end:
            if IMAGE.search(raw):
                out.append(raw)
                preserved_images += len(IMAGE.findall(raw))
            elif raw.strip():
                removed.append(i + 1)
            continue
        out.append(raw)

    after = join_lines(out, text.endswith("\n"))
    return after, {
        "changed": after != text,
        "toc_start_line": start + 1,
        "toc_end_line": end + 1,
        "toc_text_lines_removed": len(removed),
        "page_images_preserved_inside_toc": preserved_images,
    }


def repair_gongxin(text: str) -> tuple[str, dict]:
    lines = text.splitlines()
    out: list[str] = []
    first_ch20_seen = False
    first_upgraded = False
    glued_stripped: list[dict] = []
    exact = re.compile(r"^##\s+第\s*20\s*章\s*$")
    glued = re.compile(r"^##\s+第\s*20\s*章\s*让孩子听话的攻心术(.*)$")

    for i, raw in enumerate(lines, 1):
        s = raw.strip()
        if exact.match(s):
            if not first_ch20_seen:
                out.append("## 第20章 让孩子听话的攻心术")
                first_ch20_seen = True
                first_upgraded = True
            else:
                # Repeated exact chapter labels are page-header residue.
                continue
            continue

        m = glued.match(s)
        if m:
            remainder = m.group(1).lstrip(" ：:，,。；;")
            if remainder:
                out.append(remainder)
                glued_stripped.append({"line": i, "body_prefix": remainder[:120]})
            continue

        out.append(raw)

    after = join_lines(out, text.endswith("\n"))
    return after, {
        "changed": after != text,
        "chapter20_heading_upgraded": first_upgraded,
        "chapter20_glued_headers_stripped": len(glued_stripped),
        "samples": glued_stripped[:12],
    }


def cleanup_orphan_promos(text: str) -> tuple[str, dict]:
    """Edit only lines with an actual evidence-backed substitution.

    Crucially, ordinary lines, Markdown tables, code, spacing and indentation are
    left untouched. This prevents a cleanup pass from becoming a formatting
    pass of its own.
    """
    lines = text.splitlines()
    out: list[str] = []
    removed = 0
    fixed_b_endpoint = 0
    in_fence = False
    fence_token: str | None = None

    for raw in lines:
        stripped = raw.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            token = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = None
            out.append(raw)
            continue

        if in_fence or IMAGE.search(raw) or raw.lstrip().startswith("|"):
            out.append(raw)
            continue

        line = raw
        line_changed = False

        # One current-content sequence proves the contact token sat between
        # `C端消费者` and an OCR `8端消费者` (= B端消费者). Repair only that
        # exact known sequence; do not touch other numeric text.
        if "C端消费者休闲 醇味 端消费者" in line:
            line = line.replace("C端消费者休闲 醇味 端消费者", "C端消费者休闲 醇味 B端消费者")
            fixed_b_endpoint += 1
            line_changed = True

        for pat in ORPHAN_PROMO_SENTENCES:
            line, n = pat.subn("", line)
            if n:
                removed += n
                line_changed = True

        if line_changed:
            # Clean only the immediate whitespace/punctuation made awkward by
            # the removed fragment, without changing unrelated indentation.
            leading = re.match(r"^\s*", raw).group(0)
            body = line[len(leading):] if line.startswith(leading) else line.lstrip()
            body = re.sub(r"[ \t]{2,}", " ", body)
            body = re.sub(r"^[，,；;]+", "", body)
            line = leading + body

        out.append(line)

    after = join_lines(out, text.endswith("\n"))
    return after, {
        "orphan_promo_sentences_removed": removed,
        "ocr_b_endpoint_repaired": fixed_b_endpoint,
        "changed": after != text,
    }


def process(path: Path, apply: bool) -> dict:
    before = path.read_text(encoding="utf-8-sig")
    before_refs = refs(before)
    text = before
    details: dict = {}

    if path == LAYOUT3:
        text, details["layout3_toc"] = repair_layout3(text)
    if path == GONGXIN:
        text, details["gongxin_chapter20"] = repair_gongxin(text)

    text, details["promo_cleanup"] = cleanup_orphan_promos(text)

    if before_refs != refs(text):
        raise RuntimeError(f"{path}: Markdown image references changed")
    if len(re.findall(r"^#\s+", text, re.M)) != 1:
        raise RuntimeError(f"{path}: expected exactly one H1")

    changed = text != before.replace("\r\n", "\n")
    if changed and apply:
        path.write_text(text, encoding="utf-8")

    return {
        "path": str(path),
        "changed": changed,
        "applied": bool(changed and apply),
        "image_refs": sum(before_refs.values()),
        "details": details,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="temp")
    p.add_argument("--report", default="temp/.confirmed-high-risk-repair.json")
    p.add_argument("--apply", action="store_true")
    a = p.parse_args()

    targets = sorted(x for x in Path(a.root).rglob("*.md") if x.is_file() and not x.name.startswith("."))
    results, errors = [], []
    for path in targets:
        try:
            item = process(path, a.apply)
            if item["changed"]:
                results.append(item)
        except Exception as exc:
            errors.append({"path": str(path), "error": str(exc)})

    payload = {
        "summary": {
            "markdown_files_scanned": len(targets),
            "files_changed": len(results),
            "image_refs_checked_on_changed_files": sum(x["image_refs"] for x in results),
            "errors": len(errors),
        },
        "results": results,
        "errors": errors,
    }
    Path(a.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
