#!/usr/bin/env python3
"""Repository-wide conservative repair for Markdown books under temp/.

Responsibilities:
1. First-level temp child directories use index.md for the main Markdown file.
2. Remove high-confidence third-party promo/contact advertisements.
3. For still-raw PDF/OCR Markdown containing <!-- page:N --> markers, remove
   leading TOC pages, page markers/page numbers, restore common semantic heading
   levels, and conservatively reflow broken OCR paragraphs.
4. Preserve every Markdown image reference exactly.
5. Patch the repository formatting prompt so future runs follow the same naming
   and advertising rules.

The formatter intentionally skips full body reformatting for files that no
longer contain page markers; those files only receive safe naming/ad cleanup.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter
from pathlib import Path

PAGE = re.compile(r"^\s*<!--\s*page\s*:\s*\d+\s*-->\s*$", re.I | re.M)
H = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
IMG_COMMENT = re.compile(r"^\s*<!--\s*Image\s*\([^>]*\)\s*-->\s*$", re.I)
LEADER = re.compile(r"(.{2,100}?)(?:\.{4,}|…{3,}|·{4,}|﹒{4,})\s*[.·… ]*(\d{1,4})(?=\D|$)")
CHAPTER = re.compile(r"^第\s*[一二三四五六七八九十百零〇两0-9]+\s*章\b.*$")
SECTION = re.compile(r"^第\s*[一二三四五六七八九十百零〇两0-9]+\s*节\b.*$")
PART = re.compile(r"^(?:第\s*[一二三四五六七八九十百零〇两0-9]+\s*(?:部分|篇|部|卷|册)|上篇|中篇|下篇|Part\s+\d+)\b.*$", re.I)
BAD_GENE = re.compile(r"^【\s*坏人基因\s*\d+\s*】.*$")
STORY = re.compile(r"^【\s*故事\s*\d+[^】]*】.*$")
VIRUS = re.compile(r"^第[一二三四五六七八九十百零〇两0-9]+个思想病毒[：:].*$")
LIST = re.compile(r"^\s*(?:[-*+]\s+|\d+\s*[.．、)]\s+|[（(]?[一二三四五六七八九十百]+[)）、.]\s*)")
TABLE = re.compile(r"^\s*\|.*\|\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
PUNCT_END = tuple("。！？；：!?;”’）》】…")

CONTACT = re.compile(
    r"(?i)(?:加|添加|联系|获取请添加|咨询|客服)?\s*"
    r"(?:微信|微\s*信|V信|VX|V\s*X)\s*[：:=]?\s*"
    r"[A-Za-z][A-Za-z0-9_%\-]{2,}(?:\s*(?:或|/|、)\s*[A-Za-z][A-Za-z0-9_%\-]{2,})?"
)
PROMO_WORDS = ("朋友圈每日更新", "更多精品优质电子版书籍", "获取电子版", "获取请添加", "客服微信", "加微信", "添加微信")
PROMO_SUFFIX = re.compile(
    r"(?i)(?:感谢您的阅读[，,。\s]*)?(?:如需|如需要|需要)?[^\n]{0,80}?"
    r"(?:更多精品优质电子版书籍|电子版书籍|精品电子版|获取电子版|朋友圈每日更新)[^\n]{0,120}?"
    r"(?:微信|V信|VX)[：:=]?\s*[A-Za-z][A-Za-z0-9_%\-]{2,}(?:\s*(?:或|/|、)\s*[A-Za-z][A-Za-z0-9_%\-]{2,})?[^\n]*$"
)


def nkey(s: str) -> str:
    s = re.sub(r"^\d+[._、\-\s]*", "", s.strip())
    s = re.sub(r"[《》【】\[\]（）()\s_\-—·:：]", "", s)
    return s.lower()


def title_for(path: Path) -> str:
    name = path.parent.name if path.name.lower() == "index.md" else path.stem
    m = re.match(r"^《(.+?)》(.*)$", name.strip())
    if m:
        name = (m.group(1) + m.group(2)).strip()
    return name.strip() or "未命名文档"


def image_refs(text: str) -> list[str]:
    return IMAGE.findall(text)


def strip_format_chars(text: str) -> int:
    x = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    x = IMAGE.sub("", x)
    x = re.sub(r"^#{1,6}\s*", "", x, flags=re.M)
    x = re.sub(r"[#*_>`~\s]", "", x)
    return len(x)


def rename_child_markdowns(root: Path) -> tuple[list[dict], list[dict]]:
    changed: list[dict] = []
    ambiguous: list[dict] = []
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        mds = sorted(p for p in d.glob("*.md") if p.is_file() and not p.name.startswith("."))
        if not mds:
            continue
        index = d / "index.md"
        non_index = [p for p in mds if p.name.lower() != "index.md"]
        if index.exists():
            for p in list(non_index):
                if p.read_bytes() == index.read_bytes():
                    p.unlink()
                    changed.append({"action": "delete-identical-duplicate", "from": str(p), "to": str(index)})
            remaining = [p for p in d.glob("*.md") if p.name.lower() != "index.md" and not p.name.startswith(".")]
            if remaining:
                ambiguous.append({"directory": str(d), "reason": "index.md already exists with additional non-identical Markdown files", "files": [p.name for p in remaining]})
            continue

        if len(mds) == 1:
            src = mds[0]
            src.rename(index)
            changed.append({"action": "rename", "from": str(src), "to": str(index)})
            continue

        parent_key = nkey(d.name)
        matches = [p for p in mds if nkey(p.stem) == parent_key]
        if len(matches) == 1:
            src = matches[0]
            src.rename(index)
            changed.append({"action": "rename-main", "from": str(src), "to": str(index)})
        else:
            ambiguous.append({"directory": str(d), "reason": "multiple Markdown files and main file is ambiguous", "files": [p.name for p in mds]})
    return changed, ambiguous


def clean_ads_text(text: str) -> tuple[str, int]:
    removed = 0
    out: list[str] = []
    for raw in text.splitlines():
        line = raw
        stripped = line.strip()
        if not stripped:
            out.append(line)
            continue
        # High-confidence standalone contact/promotional lines.
        if CONTACT.search(stripped) and (len(stripped) <= 500 or any(w in stripped for w in PROMO_WORDS)):
            removed += 1
            continue
        if any(w in stripped for w in PROMO_WORDS) and len(stripped) <= 220:
            # Remove only obvious promotional lines; a normal paragraph that
            # merely mentions 微信 without contact details is preserved.
            removed += 1
            continue
        # Remove a promotional suffix appended to legitimate body text.
        new = PROMO_SUFFIX.sub("", line).rstrip()
        if new != line.rstrip():
            removed += 1
            if new.strip():
                out.append(new)
            continue
        # Common inline pattern such as “……，加微信：Sm99%10。”
        m = CONTACT.search(line)
        if m and any(k in line[max(0, m.start()-25):m.start()+1] for k in ("加", "添加", "客服", "联系", "获取")):
            prefix = line[: max(line.rfind("。", 0, m.start()), line.rfind("！", 0, m.start()), line.rfind("？", 0, m.start())) + 1].rstrip()
            removed += 1
            if prefix:
                out.append(prefix)
            continue
        out.append(line)
    return "\n".join(out).rstrip() + "\n", removed


def split_blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    buf: list[str] = []
    for line in lines:
        if PAGE.match(line):
            blocks.append(buf)
            buf = []
        else:
            buf.append(line)
    blocks.append(buf)
    return blocks


def content_lines(block: list[str]) -> list[str]:
    out = []
    for x in block:
        s = x.strip()
        if not s or H.match(s) or IMG_COMMENT.match(s) or IMAGE.fullmatch(s):
            continue
        out.append(s)
    return out


def toc_likeness(block: list[str], continuation: bool) -> bool:
    xs = content_lines(block)
    if not xs:
        return continuation
    joined = "".join(xs)
    if "目录" in joined[:120] or "目 录" in joined[:120]:
        return True
    leaders = sum(len(LEADER.findall(x)) for x in xs)
    long_body = sum(len(x) >= 150 and not LEADER.search(x) for x in xs)
    structural = sum(bool(CHAPTER.match(x) or SECTION.match(x) or PART.match(x) or BAD_GENE.match(x) or VIRUS.match(x)) for x in xs)
    if leaders >= 3 and long_body == 0:
        return True
    if continuation and long_body == 0 and (leaders >= 1 or structural >= 4 or (len(xs) >= 8 and max(map(len, xs)) < 110)):
        return True
    return False


def detect_toc_prefix(blocks: list[list[str]]) -> set[int]:
    chosen: set[int] = set()
    started = False
    for i, block in enumerate(blocks[:20]):
        yes = toc_likeness(block, started)
        if yes:
            started = True
            chosen.add(i)
            continue
        if started:
            break
        # Only a leading TOC is removed; do not start detection deep in body.
        if i > 2:
            break
    return chosen


def clean_candidate(s: str) -> str:
    s = H.sub(lambda m: m.group(2), s.strip())
    s = re.sub(r"^(?:目录|目\s*录)\s*", "", s).strip()
    s = re.sub(r"\s+", " ", s)
    return s.strip(" .·…\t")


def toc_candidates(blocks: list[list[str]], toc_ids: set[int]) -> set[str]:
    found: set[str] = set()
    for i in toc_ids:
        block = blocks[i]
        for raw in block:
            s = clean_candidate(raw)
            if not s:
                continue
            for m in LEADER.finditer(s):
                c = clean_candidate(m.group(1))
                # In concatenated TOCs the previous page number may precede
                # the next title; remove that numeric residue.
                c = re.sub(r"^\d{1,4}\s*", "", c).strip()
                if 2 <= len(c) <= 100:
                    found.add(c)
            if BAD_GENE.match(s) or STORY.match(s) or VIRUS.match(s) or CHAPTER.match(s) or SECTION.match(s) or PART.match(s):
                found.add(s)
    return found


def semantic_level(text: str, current: int = 1, from_toc: bool = False) -> int | None:
    t = clean_candidate(text)
    if CHAPTER.match(t):
        return 2
    if PART.match(t):
        return 2
    if BAD_GENE.match(t) or VIRUS.match(t):
        return 2
    if SECTION.match(t):
        return 3
    if STORY.match(t):
        return 3
    if from_toc:
        return min(4, max(2, current + 1))
    return None


def normalize_list(line: str) -> str:
    return re.sub(r"^\s*(\d+)\s*[．、)]\s*", lambda m: f"{m.group(1)}. ", line)


def reflow(lines: list[str]) -> list[str]:
    out: list[str] = []
    pending: list[str] = []

    def flush() -> None:
        nonlocal pending
        if not pending:
            return
        text = ""
        for frag in pending:
            frag = frag.strip()
            if not frag:
                continue
            if not text:
                text = frag
            elif re.search(r"[A-Za-z0-9]$", text) and re.match(r"^[A-Za-z0-9]", frag):
                text += " " + frag
            else:
                text += frag
        if text:
            out.append(text)
        pending = []

    for line in lines:
        s = line.strip()
        if not s:
            if pending and pending[-1].rstrip().endswith(PUNCT_END):
                flush()
            continue
        special = bool(H.match(s) or LIST.match(s) or TABLE.match(s) or FENCE.match(s) or IMAGE.fullmatch(s) or s.startswith(">"))
        if special:
            flush()
            out.append(line.rstrip())
            continue
        pending.append(line.rstrip())
        if s.endswith(PUNCT_END):
            flush()
    flush()
    # Normalize blank lines around structural blocks.
    final: list[str] = []
    for x in out:
        if final and (H.match(x.strip()) or H.match(final[-1].strip())):
            if final[-1] != "":
                final.append("")
        final.append(x)
    return final


def format_raw_document(path: Path) -> dict:
    original = path.read_text(encoding="utf-8-sig")
    if not PAGE.search(original):
        return {"path": str(path), "formatted": False, "reason": "no-page-markers"}
    before_images = image_refs(original)
    lines = original.splitlines()
    blocks = split_blocks(lines)
    toc_ids = detect_toc_prefix(blocks)
    candidates = toc_candidates(blocks, toc_ids)

    # Baseline excludes detected TOC so intentional TOC deletion does not trip
    # the body-retention safety check.
    baseline_text = "\n".join("\n".join(b) for i, b in enumerate(blocks) if i not in toc_ids)
    baseline_len = max(1, strip_format_chars(baseline_text))

    title = title_for(path)
    first_h1 = next((H.match(x.strip()).group(2).strip() for x in lines[:20] if H.match(x.strip()) and len(H.match(x.strip()).group(1)) == 1), None)
    if first_h1 and not CHAPTER.match(first_h1) and not SECTION.match(first_h1):
        title = first_h1

    body: list[str] = [f"# {title}", ""]
    current_level = 1
    heading_changes = 0
    page_numbers_removed = 0
    conversion_comments_removed = 0

    for bi, block in enumerate(blocks):
        if bi in toc_ids:
            continue
        # Remove first/last standalone numeric page numbers in each block.
        nonblank = [j for j, x in enumerate(block) if x.strip() and not IMG_COMMENT.match(x)]
        edge = set(nonblank[:1] + nonblank[-1:])
        for j, raw in enumerate(block):
            s = raw.strip()
            if not s:
                body.append("")
                continue
            if IMG_COMMENT.match(s):
                conversion_comments_removed += 1
                continue
            if j in edge and re.fullmatch(r"\d{1,4}", s):
                page_numbers_removed += 1
                continue
            if IMAGE.fullmatch(s):
                body.append(s)
                continue
            hm = H.match(s)
            plain = clean_candidate(s)
            if not plain:
                continue
            # Drop duplicate book-title occurrences after the canonical H1.
            if nkey(plain) == nkey(title):
                if hm or len(plain) <= 80:
                    continue
            level = semantic_level(plain, current_level, plain in candidates)
            if level is not None:
                body.append(f"{'#' * level} {plain}")
                current_level = level
                if not (hm and len(hm.group(1)) == level):
                    heading_changes += 1
                continue
            # Existing non-H1 Markdown heading without stronger semantics is
            # kept as a subsection, never allowed to create a second H1.
            if hm:
                level = min(4, max(2, current_level + (0 if current_level >= 3 else 1)))
                body.append(f"{'#' * level} {plain}")
                current_level = level
                if len(hm.group(1)) != level:
                    heading_changes += 1
                continue
            # Split a high-confidence TOC title glued to the start of a body line.
            prefix = next((c for c in sorted(candidates, key=len, reverse=True) if len(c) >= 3 and s.startswith(c) and len(s) - len(c) >= 25), None)
            if prefix:
                level = semantic_level(prefix, current_level, True) or min(4, current_level + 1)
                body.append(f"{'#' * level} {prefix}")
                body.append(s[len(prefix):].lstrip(" ：:，,。"))
                current_level = level
                heading_changes += 1
                continue
            body.append(normalize_list(raw.rstrip()))

    body = reflow(body)
    # Exactly one H1 and no conversion page markers.
    final = "\n".join(body)
    final = re.sub(r"\n{3,}", "\n\n", final).strip() + "\n"
    if len(re.findall(r"^#\s+", final, re.M)) != 1:
        raise RuntimeError(f"{path}: output must contain exactly one H1")
    if PAGE.search(final):
        raise RuntimeError(f"{path}: page markers remain")
    if Counter(before_images) != Counter(image_refs(final)):
        raise RuntimeError(f"{path}: Markdown image references changed")
    retention = strip_format_chars(final) / baseline_len
    if retention < 0.88:
        raise RuntimeError(f"{path}: body retention too low: {retention:.4f}")
    path.write_text(final, encoding="utf-8")
    return {
        "path": str(path),
        "formatted": True,
        "toc_blocks_removed": len(toc_ids),
        "heading_changes": heading_changes,
        "page_numbers_removed": page_numbers_removed,
        "conversion_comments_removed": conversion_comments_removed,
        "body_retention": round(min(1.0, retention), 4),
        "images_preserved": len(before_images),
    }


def patch_prompt(path: Path) -> dict:
    if not path.exists():
        return {"changed": False, "reason": "prompt-not-found"}
    text = path.read_text(encoding="utf-8")
    original = text

    ad_rule = """\n## 9.1 删除明显广告、联系方式和资源引流信息\n\n如果原始电子书或转换稿中混入第三方广告，应删除，例如：\n\n- `加微信：Sm99%10`；\n- `添加客服微信：xxxx`；\n- `朋友圈每日更新，获取请添加微信……`；\n- `感谢您的阅读，如需要更多精品优质电子版书籍……`；\n- 与正文无关的公众号、微信号、VX / V信、资源群、电子版获取方式等。\n\n执行边界：\n\n- 只有能够高置信判断为广告、联系方式或资源引流时才删除；\n- 正文正常讨论“微信”“朋友圈”“公众号”等概念时必须保留；\n- 如果广告被错误拼接在正文句尾，只删除广告片段，保留前面的正常正文；\n- 不得因为清理广告而删除整段有价值正文。\n\n"""
    if "## 9.1 删除明显广告、联系方式和资源引流信息" not in text:
        marker = "# 五、图片处理"
        if marker in text:
            text = text.replace(marker, ad_rule + "---\n\n" + marker, 1)

    # Replace the old absolute 'never index.md' naming rule with repository-aware naming.
    pattern = re.compile(r"## 12\. 文件名直接使用真实书名.*?(?=\n---\n\n# 八、完成前的最终校验)", re.S)
    replacement = """## 12. 根据仓库位置确定文件名\n\n先识别真实书名，再根据文件所在位置确定 Markdown 文件名：\n\n### `temp/` 根目录中的独立 Markdown\n\n如果文件直接位于 `temp/` 根目录，文件名使用真实书名，例如：\n\n```text\ntemp/博弈论.md\n```\n\n不要附加 `-修正版`、`-clean`、`-最终版` 等后缀。\n\n### `temp/<书名目录>/` 中的主 Markdown\n\n如果一本书已经有独立子目录，则该目录中的**主 Markdown 文件固定命名为 `index.md`**，例如：\n\n```text\ntemp/《人性要诀》/index.md\n```\n\n不要保留：\n\n```text\ntemp/《人性要诀》/人性要诀.md\ntemp/《人性要诀》/《人性要诀》.md\n```\n\n这样目录名负责表达书名，`index.md` 作为统一内容入口，便于脚本、工作流和后续知识库处理。\n\n如果子目录中存在多个 Markdown 文件，必须先判断哪一个是主文档；不能在无法确定时把多个不同文件互相覆盖。\n"""
    if pattern.search(text):
        text = pattern.sub(replacement, text, count=1)

    changed = text != original
    if changed:
        path.write_text(text, encoding="utf-8")
    return {"changed": changed}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="temp")
    ap.add_argument("--prompt", default=".prompt/Markdown文档整理与修复通用提示词.md")
    ap.add_argument("--report", default="temp/.semantic-cleanup-report.json")
    args = ap.parse_args()

    root = Path(args.root)
    renamed, ambiguous = rename_child_markdowns(root)

    ad_results: list[dict] = []
    format_results: list[dict] = []
    errors: list[dict] = []

    targets = sorted(p for p in root.rglob("*.md") if p.is_file() and not p.name.startswith("."))
    for p in targets:
        original = p.read_text(encoding="utf-8-sig")
        before_imgs = Counter(image_refs(original))
        cleaned, removed = clean_ads_text(original)
        if Counter(image_refs(cleaned)) != before_imgs:
            errors.append({"path": str(p), "stage": "ads", "error": "image reference safety check failed"})
            continue
        if removed:
            p.write_text(cleaned, encoding="utf-8")
            ad_results.append({"path": str(p), "ad_fragments_removed": removed})

    # Full structural formatting only for raw converted files still carrying page markers.
    targets = sorted(p for p in root.rglob("*.md") if p.is_file() and not p.name.startswith("."))
    for p in targets:
        try:
            if PAGE.search(p.read_text(encoding="utf-8-sig")):
                format_results.append(format_raw_document(p))
        except Exception as e:
            errors.append({"path": str(p), "stage": "format", "error": str(e)})

    prompt_result = patch_prompt(Path(args.prompt))
    payload = {
        "renamed_to_index": renamed,
        "ambiguous_child_directories": ambiguous,
        "ads_cleaned": ad_results,
        "formatted_raw_documents": format_results,
        "prompt": prompt_result,
        "errors": errors,
        "summary": {
            "renamed_count": len(renamed),
            "ambiguous_directory_count": len(ambiguous),
            "files_with_ads_cleaned": len(ad_results),
            "ad_fragments_removed": sum(x["ad_fragments_removed"] for x in ad_results),
            "raw_documents_formatted": sum(bool(x.get("formatted")) for x in format_results),
            "format_heading_changes": sum(x.get("heading_changes", 0) for x in format_results),
            "errors": len(errors),
        },
    }
    report = Path(args.report)
    report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
