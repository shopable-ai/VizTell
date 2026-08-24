#!/usr/bin/env python3
"""Normalize only the beginning of book Markdown files under temp/.

Scope is intentionally narrow:
- keep repository paths unchanged;
- make the physical first line `# <book title>`;
- remove leading PDF/OCR page marker comments before the title;
- otherwise preserve the document body as-is.

This is a header-only repair pass, not a replacement for the full Markdown
semantic formatter.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PAGE = re.compile(r"^\s*<!--\s*page\s*:\s*\d+\s*-->\s*$", re.I)
H1 = re.compile(r"^#\s+(.+?)\s*$")


def title_from_path(path: Path) -> str:
    name = path.stem.strip()
    if name.lower() == "index":
        name = path.parent.name.strip()

    # Book-title marks are removed only for the H1 text. Paths are untouched.
    # Keep any suffix outside the marks (e.g. 上册 / 下册 / PDF版) so this
    # narrow pass does not guess beyond filename evidence.
    m = re.match(r"^《(.+?)》(.*)$", name)
    if m:
        name = (m.group(1) + m.group(2)).strip()
    elif name.startswith("《") and name.endswith("》"):
        name = name[1:-1].strip()

    return name or path.stem


def key(s: str) -> str:
    return re.sub(r"[\s《》【】\[\]（）()\-—_·:：]", "", s).lower()


def normalize_one(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8-sig")
    original = raw
    lines = raw.splitlines()
    title = title_from_path(path)

    # Remove only leading whitespace/page-marker conversion artifacts.
    removed_leading_page_markers = 0
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and PAGE.match(lines[0]):
        lines.pop(0)
        removed_leading_page_markers += 1
        while lines and not lines[0].strip():
            lines.pop(0)

    moved_existing_h1 = False
    inserted_h1 = False

    if lines and H1.match(lines[0]):
        # Existing first-line H1 wins; do not rewrite a title that was already
        # semantically established by an earlier formatting pass.
        pass
    else:
        # If there is exactly one existing H1 and it clearly matches the
        # filename-derived book title, move it to line 1 instead of duplicating.
        h1_positions = [(i, H1.match(line)) for i, line in enumerate(lines) if H1.match(line)]
        matching = [(i, m) for i, m in h1_positions if key(m.group(1)) == key(title)]
        if len(matching) == 1:
            i, m = matching[0]
            h1_line = lines.pop(i)
            # Collapse blank space left where the H1 was removed, without
            # touching nonblank body text.
            if i < len(lines) and i > 0 and not lines[i - 1].strip() and not lines[i].strip():
                lines.pop(i)
            lines = [h1_line, ""] + lines
            moved_existing_h1 = True
        else:
            lines = [f"# {title}", ""] + lines
            inserted_h1 = True

    # Physical line 1 must be H1; normalize only excess blank lines immediately
    # after it. Body text remains otherwise unchanged.
    while len(lines) > 2 and not lines[1].strip() and not lines[2].strip():
        lines.pop(2)

    output = "\n".join(lines).rstrip() + "\n"
    changed = output != original
    if changed:
        path.write_text(output, encoding="utf-8")

    first = output.splitlines()[0] if output else ""
    if not H1.match(first):
        raise RuntimeError(f"first line is not H1 after repair: {path}")

    return {
        "path": str(path),
        "changed": changed,
        "title": H1.match(first).group(1),
        "inserted_h1": inserted_h1,
        "moved_existing_h1": moved_existing_h1,
        "removed_leading_page_markers": removed_leading_page_markers,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="temp")
    ap.add_argument("--report")
    args = ap.parse_args()

    root = Path(args.root)
    targets = sorted(
        p for p in root.rglob("*.md")
        if p.is_file() and not p.name.startswith(".")
    )
    results = [normalize_one(p) for p in targets]
    payload = {
        "scanned": len(results),
        "changed": sum(r["changed"] for r in results),
        "inserted_h1": sum(r["inserted_h1"] for r in results),
        "moved_existing_h1": sum(r["moved_existing_h1"] for r in results),
        "removed_leading_page_markers": sum(r["removed_leading_page_markers"] for r in results),
        "changed_files": [r for r in results if r["changed"]],
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    print(text, end="")
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
