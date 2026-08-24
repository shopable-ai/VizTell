#!/usr/bin/env python3
"""Final cleanup/validation pass for temp Markdown.

- Merge OCR-wrapped continuation lines inside numbered list items in the 12 raw
  converted documents already identified by .raw-format-report.json.
- Patch the common Markdown prompt with repeated numbered-title families.
- Validate child-directory index.md naming, page-marker/page-number cleanup,
  blank headings, high-confidence contact ads, and Markdown image preservation.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
H = re.compile(r"^#{1,6}\s+\S")
LIST = re.compile(r"^\s*\d+\s*[.．、)]\s+\S")
PUNCT = tuple("。！？；：!?;”’）》】…")
PAGE_MARK = re.compile(r"<!--\s*page\s*:", re.I)
PAGE_TOKEN = re.compile(r"第\s*\d{1,4}\s*页")
BLANK_HEADING = re.compile(r"^#{1,6}\s*$", re.M)
CONTACT = re.compile(r"(?i)(?:加|添加|联系|客服|获取请添加)?\s*(?:微信|微\s*信|V信|VX)\s*[：:=]?\s*[A-Za-z][A-Za-z0-9_%\-]{2,}")


def join_fragments(a: str, b: str) -> str:
    a = a.rstrip()
    b = b.strip()
    if not a:
        return b
    if re.search(r"[A-Za-z0-9]$", a) and re.match(r"^[A-Za-z0-9]", b):
        return a + " " + b
    return a + b


def merge_list_continuations(path: Path) -> dict:
    before = path.read_text(encoding="utf-8")
    imgs = Counter(IMAGE.findall(before))
    lines = before.splitlines()
    out: list[str] = []
    merged = 0
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        s = line.strip()
        if LIST.match(s) and not s.endswith(PUNCT):
            combined = line
            j = i + 1
            while j < len(lines):
                nxt = lines[j].strip()
                if not nxt:
                    break
                if H.match(nxt) or LIST.match(nxt) or nxt == "***" or nxt.startswith("|") or nxt.startswith(">"):
                    break
                combined = join_fragments(combined, nxt)
                merged += 1
                j += 1
                if combined.rstrip().endswith(PUNCT):
                    break
            out.append(combined)
            i = j
            continue
        out.append(line)
        i += 1
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    if Counter(IMAGE.findall(text)) != imgs:
        raise RuntimeError(f"{path}: image references changed")
    if len(re.findall(r"^#\s+", text, re.M)) != 1:
        raise RuntimeError(f"{path}: H1 count changed")
    if text != before:
        path.write_text(text, encoding="utf-8")
    return {"path": str(path), "changed": text != before, "continuation_lines_merged": merged}


def patch_prompt(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    before = text
    needle = "- `第一节……`、`第 1 节……` 等节级编号行；"
    extra = "\n- `第十七诀……`、`第一套……`、`第一招……`、`第一计……` 等在同一文件中稳定重复出现的编号主题；"
    if needle in text and extra.strip() not in text:
        text = text.replace(needle, needle + extra, 1)
    validation_needle = "5. 是否还有可能已经丢失 Markdown `#` 的纯文字标题没有被识别；"
    validation_extra = "\n6. `第 X 诀 / 第 X 套 / 第 X 招 / 第 X 计` 等稳定重复编号标题是否已按语义恢复；"
    if validation_needle in text and validation_extra.strip() not in text:
        text = text.replace(validation_needle, validation_needle + validation_extra, 1)
        # Renumber following validation items to keep the list monotonic.
        block_start = text.find("# 八、完成前的最终校验")
        block_end = text.find("\n---\n\n# 九、", block_start)
        if block_start >= 0 and block_end > block_start:
            block = text[block_start:block_end]
            lines = block.splitlines()
            new_lines = []
            seq = 0
            for line in lines:
                if re.match(r"^\d+\. ", line):
                    seq += 1
                    line = re.sub(r"^\d+\.", f"{seq}.", line)
                new_lines.append(line)
            text = text[:block_start] + "\n".join(new_lines) + text[block_end:]
    if text != before:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def validate(root: Path) -> dict:
    child_naming = []
    issues = []
    files = sorted(p for p in root.rglob("*.md") if p.is_file() and not p.name.startswith("."))
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        mds = sorted(p.name for p in d.glob("*.md") if not p.name.startswith("."))
        if mds and mds != ["index.md"]:
            child_naming.append({"directory": str(d), "markdown_files": mds})
    for p in files:
        text = p.read_text(encoding="utf-8-sig")
        found = []
        if PAGE_MARK.search(text): found.append("page-marker")
        if BLANK_HEADING.search(text): found.append("blank-heading")
        if CONTACT.search(text): found.append("contact-ad")
        if p.parent == root and PAGE_TOKEN.search(text): found.append("inline-page-token")
        h1 = len(re.findall(r"^#\s+", text, re.M))
        if h1 != 1: found.append(f"h1-count:{h1}")
        if found:
            issues.append({"path": str(p), "issues": found})
    return {
        "markdown_files_scanned": len(files),
        "child_directory_naming_issues": child_naming,
        "content_issues": issues,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="temp")
    ap.add_argument("--raw-report", default="temp/.raw-format-report.json")
    ap.add_argument("--prompt", default=".prompt/Markdown文档整理与修复通用提示词.md")
    ap.add_argument("--report", default="temp/.final-markdown-validation.json")
    args = ap.parse_args()

    raw = json.loads(Path(args.raw_report).read_text(encoding="utf-8"))
    targets = [Path(x["path"]) for x in raw.get("formatted", []) if x.get("formatted")]
    merge_results = []
    errors = []
    for p in targets:
        try:
            merge_results.append(merge_list_continuations(p))
        except Exception as exc:
            errors.append({"path": str(p), "error": str(exc)})

    prompt_changed = patch_prompt(Path(args.prompt))
    validation = validate(Path(args.root))
    payload = {
        "list_continuation_cleanup": [x for x in merge_results if x.get("changed")],
        "prompt_numbered_title_rule_added": prompt_changed,
        "validation": validation,
        "errors": errors,
        "summary": {
            "raw_files_with_list_wrap_changes": sum(bool(x.get("changed")) for x in merge_results),
            "list_continuation_lines_merged": sum(x.get("continuation_lines_merged", 0) for x in merge_results),
            "markdown_files_scanned": validation["markdown_files_scanned"],
            "child_directory_naming_issues": len(validation["child_directory_naming_issues"]),
            "content_issue_files": len(validation["content_issues"]),
            "errors": len(errors),
        },
    }
    Path(args.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
