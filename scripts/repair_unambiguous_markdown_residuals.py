#!/usr/bin/env python3
"""Repair only high-confidence Markdown residuals across temp/**/*.md.

Current-content evidence is authoritative; file mtimes / previous format commits
are not used as completion signals.

Repairs are deliberately narrow:
- remove standalone OCR page-footer lines and inline `第N页共M页` suffixes;
- remove direct obfuscated contact credentials such as `wx:abc123` / `薇芯:123456`;
- remove the known embedded promo token `公号：文字变现艺术家`;
- split oversized numbered `第N招` headings only when the title/body boundary is
  explicit (full stop after a compact title, or `...法，` construction).

Every Markdown image reference must remain byte-identical as a multiset.
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
STANDALONE_PAGE = re.compile(
    r"^\s*(?:第\s*)?\d{1,4}\s*页(?:\s*[,，;；]?\s*共\s*\d{1,4}\s*页)?\s*$"
)
INLINE_PAGE_SUFFIX = re.compile(
    r"\s*第\s*\d{1,4}\s*页\s*共\s*\d{1,4}\s*页\s*$"
)
DIRECT_CONTACT = re.compile(
    r"(?i)(?<![A-Za-z0-9])(?:wx|vx|v\s*信|薇芯|薇信|威信)\s*[:：=]\s*[A-Za-z0-9_-]{5,24}\s*[，,]?"
)
KNOWN_PROMO = re.compile(r"公号\s*[:：]\s*文字变现艺术家\s*[，,]?")

# `## 第1招.用拖延法消耗他的时间。这个方法...`
NUMBERED_FULLSTOP = re.compile(
    r"^(第\s*\d{1,3}\s*招\s*[.．、]\s*[^。！？!?]{2,80})[。！？!?]\s*(.{20,})$"
)
# `## 第2招，叫做赞同回击法，这就好比...`
NUMBERED_METHOD = re.compile(
    r"^(第\s*\d{1,3}\s*招\s*[，,]\s*(?:(?:就是|叫做)\s*)?[^，,。！？!?]{2,45}?法)[，,]\s*(.{20,})$"
)


def refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def normalize(lines: list[str]) -> str:
    out: list[str] = []
    for raw in lines:
        x = raw.rstrip()
        if x:
            out.append(x)
        elif out and out[-1] != "":
            out.append("")
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) + "\n"


def process(path: Path, apply: bool) -> dict:
    before = path.read_text(encoding="utf-8-sig")
    before_refs = refs(before)
    out: list[str] = []
    in_fence = False
    fence = None
    counts = {
        "standalone_page_footers_removed": 0,
        "inline_page_suffixes_removed": 0,
        "direct_contact_tokens_removed": 0,
        "known_promo_tokens_removed": 0,
        "oversized_numbered_headings_split": 0,
    }
    samples: list[dict] = []

    for lineno, raw in enumerate(before.splitlines(), 1):
        s = raw.strip()
        fm = FENCE.match(s)
        if fm:
            token = fm.group(1)
            if not in_fence:
                in_fence, fence = True, token
            elif token == fence:
                in_fence, fence = False, None
            out.append(raw.rstrip())
            continue
        if in_fence or IMAGE.search(raw):
            out.append(raw.rstrip())
            continue

        if STANDALONE_PAGE.fullmatch(s):
            counts["standalone_page_footers_removed"] += 1
            if len(samples) < 40:
                samples.append({"line": lineno, "kind": "standalone_page_footer", "before": s})
            continue

        line = raw.rstrip()
        new = INLINE_PAGE_SUFFIX.sub("", line).rstrip()
        if new != line:
            counts["inline_page_suffixes_removed"] += 1
            if len(samples) < 40:
                samples.append({"line": lineno, "kind": "inline_page_suffix", "before": line[-100:], "after": new[-100:]})
            line = new

        new, n = DIRECT_CONTACT.subn("", line)
        if n:
            counts["direct_contact_tokens_removed"] += n
            if len(samples) < 40:
                samples.append({"line": lineno, "kind": "direct_contact", "before": line[:220], "after": new[:220]})
            line = re.sub(r"\s{2,}", " ", new).strip()

        new, n = KNOWN_PROMO.subn("", line)
        if n:
            counts["known_promo_tokens_removed"] += n
            if len(samples) < 40:
                samples.append({"line": lineno, "kind": "known_promo", "before": line[:220], "after": new[:220]})
            line = re.sub(r"\s{2,}", " ", new).strip()

        hm = H.match(line.strip())
        if hm and len(hm.group(2)) >= 100:
            level = len(hm.group(1))
            content = hm.group(2).strip()
            split = NUMBERED_FULLSTOP.match(content) or NUMBERED_METHOD.match(content)
            if split:
                title, body = split.group(1).strip(), split.group(2).strip()
                if 4 <= len(title) <= 90 and len(body) >= 20:
                    out.append(f"{'#' * level} {title}")
                    out.append("")
                    out.append(body)
                    counts["oversized_numbered_headings_split"] += 1
                    if len(samples) < 40:
                        samples.append({"line": lineno, "kind": "split_numbered_heading", "title": title, "body_prefix": body[:140]})
                    continue

        out.append(line)

    after = normalize(out)
    if before_refs != refs(after):
        raise RuntimeError(f"{path}: Markdown image references changed")
    if len(re.findall(r"^#\s+", after, re.M)) != 1:
        raise RuntimeError(f"{path}: expected exactly one H1")

    changed = after != before.replace("\r\n", "\n")
    if changed and apply:
        path.write_text(after, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "applied": bool(changed and apply),
        **counts,
        "image_refs": sum(before_refs.values()),
        "samples": samples,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="temp")
    p.add_argument("--report", default="temp/.unambiguous-residual-repair.json")
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

    keys = [
        "standalone_page_footers_removed",
        "inline_page_suffixes_removed",
        "direct_contact_tokens_removed",
        "known_promo_tokens_removed",
        "oversized_numbered_headings_split",
    ]
    payload = {
        "policy": "Only current-content, high-confidence residuals are auto-repaired; image references are invariant.",
        "summary": {
            "markdown_files_scanned": len(targets),
            "files_changed": len(results),
            **{k: sum(x[k] for x in results) for k in keys},
            "image_refs_checked": sum(x.get("image_refs", 0) for x in results),
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
