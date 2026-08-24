#!/usr/bin/env python3
"""Remove OCR page-number tokens such as '第 12 页' from raw books already formatted.

Targets are read from temp/.raw-format-report.json so normal Markdown documents
are not touched. Markdown image references must remain byte-for-byte identical.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
PAGE_TOKEN = re.compile(r"第\s*\d{1,4}\s*页")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-report", default="temp/.raw-format-report.json")
    ap.add_argument("--report", default="temp/.inline-page-number-cleanup.json")
    args = ap.parse_args()

    source_report = Path(args.source_report)
    data = json.loads(source_report.read_text(encoding="utf-8"))
    targets = [Path(x["path"]) for x in data.get("formatted", []) if x.get("formatted")]

    changed = []
    errors = []
    for path in targets:
        if not path.exists():
            errors.append({"path": str(path), "error": "missing"})
            continue
        before = path.read_text(encoding="utf-8")
        before_images = Counter(IMAGE.findall(before))
        count = len(PAGE_TOKEN.findall(before))
        if not count:
            continue
        after = PAGE_TOKEN.sub("", before)
        # Remove spaces left between Chinese punctuation/text by the deleted token.
        after = re.sub(r"([，。！？；：、])\s{2,}", r"\1", after)
        after = re.sub(r"\n{3,}", "\n\n", after)
        if Counter(IMAGE.findall(after)) != before_images:
            errors.append({"path": str(path), "error": "image references changed"})
            continue
        path.write_text(after, encoding="utf-8")
        changed.append({"path": str(path), "page_tokens_removed": count})

    payload = {
        "changed": changed,
        "errors": errors,
        "summary": {
            "files_changed": len(changed),
            "page_tokens_removed": sum(x["page_tokens_removed"] for x in changed),
            "errors": len(errors),
        },
    }
    Path(args.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
