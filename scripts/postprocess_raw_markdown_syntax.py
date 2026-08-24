#!/usr/bin/env python3
"""Post-process the raw-document formatting pass for Markdown syntax integrity.

Only files listed as successfully formatted in temp/.raw-format-report.json are
touched. The pass separates headings and OCR scene separators that may have
been glued to neighboring prose during paragraph reflow.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
H1 = re.compile(r"^#\s+", re.M)
PAGE = re.compile(r"<!--\s*page\s*:", re.I)
PAGE_TOKEN = re.compile(r"第\s*\d{1,4}\s*页")
# A Markdown heading marker embedded after ordinary prose/punctuation.
EMBEDDED_HEADING = re.compile(r"(?P<prefix>[^\n`#])(?P<h>#{2,4})\s+(?=[^#\s])")


def separate_scene_markers(text: str) -> tuple[str, int]:
    changed = 0
    out = []
    for line in text.splitlines():
        # A single *** glued to prose is overwhelmingly an OCR scene separator.
        # Lines with paired *** are left alone to avoid damaging bold-italic text.
        if line.count("***") == 1 and line.strip() != "***":
            before, after = line.split("***", 1)
            if before.strip() or after.strip():
                if before.rstrip():
                    out.append(before.rstrip())
                out.extend(["", "***", ""])
                if after.lstrip():
                    out.append(after.lstrip())
                changed += 1
                continue
        out.append(line)
    return "\n".join(out), changed


def separate_embedded_headings(text: str) -> tuple[str, int]:
    total = 0
    while True:
        def repl(m: re.Match[str]) -> str:
            nonlocal total
            total += 1
            return m.group("prefix") + "\n\n" + m.group("h") + " "
        new = EMBEDDED_HEADING.sub(repl, text)
        if new == text:
            return text, total
        text = new


def normalize_heading_spacing(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    for line in lines:
        is_heading = bool(re.match(r"^#{1,6}\s+", line.strip()))
        if is_heading and out and out[-1] != "":
            out.append("")
        out.append(line.rstrip())
        if is_heading:
            out.append("")
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-report", default="temp/.raw-format-report.json")
    ap.add_argument("--report", default="temp/.raw-syntax-postprocess.json")
    args = ap.parse_args()

    raw = json.loads(Path(args.source_report).read_text(encoding="utf-8"))
    targets = [Path(x["path"]) for x in raw.get("formatted", []) if x.get("formatted")]
    changed = []
    errors = []

    for path in targets:
        if not path.exists():
            errors.append({"path": str(path), "error": "missing"})
            continue
        before = path.read_text(encoding="utf-8")
        images = Counter(IMAGE.findall(before))
        text, scene_count = separate_scene_markers(before)
        text, heading_count = separate_embedded_headings(text)
        text = normalize_heading_spacing(text)

        if Counter(IMAGE.findall(text)) != images:
            errors.append({"path": str(path), "error": "image references changed"})
            continue
        if len(H1.findall(text)) != 1:
            errors.append({"path": str(path), "error": "H1 count is not 1"})
            continue
        if PAGE.search(text):
            errors.append({"path": str(path), "error": "page marker remains"})
            continue
        if PAGE_TOKEN.search(text):
            errors.append({"path": str(path), "error": "inline page token remains"})
            continue
        if EMBEDDED_HEADING.search(text):
            errors.append({"path": str(path), "error": "embedded heading remains"})
            continue

        if text != before:
            path.write_text(text, encoding="utf-8")
            changed.append({
                "path": str(path),
                "embedded_headings_separated": heading_count,
                "scene_markers_separated": scene_count,
            })

    payload = {
        "changed": changed,
        "errors": errors,
        "summary": {
            "files_changed": len(changed),
            "embedded_headings_separated": sum(x["embedded_headings_separated"] for x in changed),
            "scene_markers_separated": sum(x["scene_markers_separated"] for x in changed),
            "errors": len(errors),
        },
    }
    Path(args.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
