#!/usr/bin/env python3
"""Second-pass invariant repairs for temp Markdown.

Only repairs structure that is objectively invalid under the repository prompt:
- a top TOC label that now fronts only preserved page images;
- heading-level jumps such as H1 -> H3 or H2 -> H4;
- duplicate H1 titles.

The pass never invents new semantic headings from ordinary prose. Markdown image
references must remain byte-identical as a multiset.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

H = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
FENCE = re.compile(r"^\s*(```|~~~)")


def compact(s: str) -> str:
    m = H.match(s.strip())
    if m:
        s = m.group(2)
    s = re.sub(r"^\*\*(.*?)\*\*$", r"\1", s.strip())
    return re.sub(r"\s+", "", s).lower()


def images(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def title_of(lines: list[str], path: Path) -> str:
    for x in lines[:60]:
        m = H.match(x.strip())
        if m and len(m.group(1)) == 1:
            return m.group(2).strip()
    name = path.parent.name if path.name == "index.md" else path.stem
    m = re.match(r"^《(.+?)》(.*)$", name)
    return ((m.group(1) + m.group(2)).strip() if m else name).strip()


def removable_image_only_toc_label(lines: list[str], idx: int) -> bool:
    """True only when a top `目录` label is followed by preserved page images
    and no textual TOC entries before the body resumes."""
    saw_image = False
    for j in range(idx + 1, min(len(lines), idx + 120)):
        s = lines[j].strip()
        if not s:
            continue
        if IMAGE.fullmatch(s):
            saw_image = True
            continue
        # Another conversion comment around a page image is harmless here.
        if s.startswith("<!--") and s.endswith("-->"):
            continue
        # First real text: remove the label only if at least one image was seen.
        return saw_image
    return saw_image


def process(path: Path, apply: bool) -> dict:
    original = path.read_text(encoding="utf-8-sig")
    before_imgs = images(original)
    lines = original.splitlines()
    title = title_of(lines, path)

    toc_labels_removed = 0
    duplicate_h1_removed = 0
    heading_jumps_fixed = 0
    out: list[str] = []
    in_fence = False
    fence_token = None
    prev_level: int | None = None
    seen_h1 = False

    for i, raw in enumerate(lines):
        s = raw.strip()
        fm = FENCE.match(s)
        if fm:
            token = fm.group(1)
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = None
            out.append(raw.rstrip())
            continue
        if in_fence:
            out.append(raw.rstrip())
            continue

        if i < 500 and compact(raw) == "目录" and removable_image_only_toc_label(lines, i):
            toc_labels_removed += 1
            continue

        m = H.match(s)
        if not m:
            out.append(raw.rstrip())
            continue
        level = len(m.group(1))
        text = m.group(2).strip()

        if level == 1:
            if seen_h1:
                if compact(text) == compact(title):
                    duplicate_h1_removed += 1
                    continue
                level = 2
                heading_jumps_fixed += 1
            else:
                seen_h1 = True
                prev_level = 1
                out.append(f"# {text}")
                continue

        if prev_level is None:
            prev_level = 1 if seen_h1 else level
        if level > prev_level + 1:
            level = prev_level + 1
            heading_jumps_fixed += 1
        out.append(f"{'#' * level} {text}")
        prev_level = level

    final: list[str] = []
    for x in out:
        if not x.strip():
            if final and final[-1] != "":
                final.append("")
        else:
            final.append(x.rstrip())
    while final and final[-1] == "":
        final.pop()
    text = "\n".join(final).strip() + "\n"

    if before_imgs != images(text):
        raise RuntimeError(f"{path}: Markdown image references changed")
    if len(re.findall(r"^#\s+", text, re.M)) != 1:
        raise RuntimeError(f"{path}: expected exactly one H1")

    changed = text != original.replace("\r\n", "\n")
    if changed and apply:
        path.write_text(text, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "applied": bool(changed and apply),
        "toc_labels_removed": toc_labels_removed,
        "duplicate_h1_removed": duplicate_h1_removed,
        "heading_jumps_fixed": heading_jumps_fixed,
        "image_refs": sum(before_imgs.values()),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="temp")
    p.add_argument("--report", default="temp/.format-invariant-repair.json")
    p.add_argument("--apply", action="store_true")
    a = p.parse_args()
    root = Path(a.root)
    targets = sorted(x for x in root.rglob("*.md") if x.is_file() and not x.name.startswith("."))
    results = []
    errors = []
    for path in targets:
        try:
            results.append(process(path, a.apply))
        except Exception as exc:
            errors.append({"path": str(path), "error": str(exc)})
    payload = {
        "summary": {
            "markdown_files_scanned": len(targets),
            "files_changed": sum(bool(x.get("applied")) for x in results),
            "toc_labels_removed": sum(x["toc_labels_removed"] for x in results),
            "duplicate_h1_removed": sum(x["duplicate_h1_removed"] for x in results),
            "heading_jumps_fixed": sum(x["heading_jumps_fixed"] for x in results),
            "image_refs_checked": sum(x["image_refs"] for x in results),
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
