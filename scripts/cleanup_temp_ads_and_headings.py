#!/usr/bin/env python3
"""Surgically remove high-confidence book-external ads from temp Markdown.

The repository contains OCR/PDF conversions where ad strings may be standalone,
embedded in prose, glued to the beginning of a sentence, or formatted as a
Markdown heading. This pass follows .prompt/Markdown文档整理与修复通用提示词.md:

- recurse through every temp/**/*.md;
- preserve正文 and every Markdown image reference;
- remove only high-confidence third-party promo/contact spans;
- if an ad heading is removed, repair only the hierarchy damage caused by that
  false parent heading;
- keep normal discussion/examples about WeChat, public accounts, QR codes, etc.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

IMG = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
CRED = r"[A-Za-z0-9][A-Za-z0-9_%\-. ]{2,22}"
WX = r"(?:微\s*信|威\s*信|V\s*信|V\s*X|VX|weixin|wechat)"
ADD_AUTHOR = r"(?:可\s*)?(?:添\s*加|加|联\s*系|扫\s*码\s*添\s*加)\s*(?:本\s*书\s*)?(?:作\s*者|客\s*服|老\s*师|讲\s*师|助\s*理|小\s*编|Mona\s*老\s*师)?\s*"

# Exact recurring watermark/promo token glued into正文 in some books.
GLUED_PREFIX = re.compile(
    rf"(?i)(?:更\s*多\s*精\s*品\s*(?:课\s*程|资\s*料|资\s*源|电\s*子\s*书))\s*"
    rf"(?:加|添\s*加)\s*{WX}\s*[：:=]?\s*{CRED}"
)
INLINE_RESOURCE_TOKEN = re.compile(
    rf"(?i)更\s*多\s*资\s*料\s*(?:加|添\s*加)\s*{WX}\s*[：:=]?\s*{CRED}\s*[，,]?\s*"
)

# Parenthetical contact/promo ads. Keep the surrounding正文.
PAREN_AD = re.compile(
    rf"[（(]\s*[^（）()\n]{{0,120}}(?:{ADD_AUTHOR}{WX}|(?:作\s*者|客\s*服|老\s*师|Mona\s*老\s*师)\s*{WX})"
    rf"[^（）()\n]{{0,120}}[）)]",
    re.I,
)
PAREN_RESOURCE_AD = re.compile(
    rf"[（(]\s*[^（）()\n]{{0,100}}(?:更\s*多|内\s*部|模\s*板|课\s*程|资\s*料|资\s*源)"
    rf"[^（）()\n]{{0,80}}(?:{ADD_AUTHOR}{WX}|{WX}\s*[：:=]?\s*{CRED})[^（）()\n]{{0,100}}[）)]",
    re.I,
)

# Explicit resource/author CTA phrase. The prefix is intentionally specific so
# ordinary sentences such as “加客户微信”“老师的微信” are not removed.
AUTHOR_CTA = re.compile(
    rf"(?i)(?:(?:具\s*体\s*)?(?:更\s*多\s*)?(?:落\s*地\s*(?:细\s*节|模\s*型|增\s*长[^，。；;]{{0,18}})|"
    rf"更\s*多\s*(?:内\s*部|精\s*品|实\s*用)?\s*(?:资\s*料|资\s*源|课\s*程|电\s*子\s*书|细\s*节)|"
    rf"如\s*有\s*疑\s*惑|内\s*部\s*课\s*程\s*分\s*享|割\s*韭\s*菜\s*模\s*板|"
    rf"也\s*可\s*以|可\s*以|可)\s*[，,:：；;、\-—]*\s*)"
    rf"(?:见[^，。；;]{{0,30}}[，,]\s*)?{ADD_AUTHOR}{WX}\s*[：:=．.]*\s*{CRED}"
    rf"(?:\s*(?:获\s*取|索\s*取|领\s*取|内\s*部\s*悄\s*悄\s*分\s*享|购\s*正\s*版\s*书\s*籍)[^。！？!?；;\n]{{0,90}})?"
    rf"[。；;]?[，,]?\s*"
)

# Shorter explicit “添加作者微信 + credential” span, used inside prose when
# no promo lead survives OCR. It does not match generic “加微信” examples.
AUTHOR_CONTACT_SPAN = re.compile(
    rf"(?i)(?:也\s*可\s*以\s*)?{ADD_AUTHOR}{WX}\s*[：:=．.]*\s*{CRED}"
    rf"(?:\s*(?:获\s*取|索\s*取|领\s*取)[^。！？!?；;，,\n]{{0,60}})?"
)

# Public-account/book-external promo fragments embedded between正文 clauses.
PUBLIC_RESOURCE_SPAN = re.compile(
    r"(?i)更\s*多\s*内\s*部\s*绝\s*密\s*资\s*料\s*关\s*注\s*公\s*众\s*号\s*[：:]?\s*[^，,。；;]{1,30}[，,]?\s*"
)
AUDIO_PROMO_SPAN = re.compile(
    r"(?i)完\s*整\s*的?\s*音\s*频[^。！？!?]{0,100}(?:关\s*注|微\s*信\s*公\s*众\s*平\s*台)[^。！？!?]{0,80}[。！？!?]?"
)
PERSONAL_ACCOUNT_TAIL = re.compile(
    r"(?i)更\s*多\s*实\s*用\s*干\s*货\s*和\s*活\s*动\s*通\s*知[^。！？!?]{0,30}"
    r"(?:关\s*注|添\s*加)[^。！？!?]{0,20}(?:个\s*人\s*)?微\s*信\s*号[^。！？!?]{0,80}[。！？!?]?"
)

# Lines that are themselves promotional headings/noise. These can legitimately
# be deleted as a whole, after which direct child headings may need to move up.
AD_HEADING = re.compile(
    r"(?i)(?:购\s*正\s*版\s*书\s*籍|更\s*多\s*(?:隐\s*秘|内\s*部|精\s*品)?\s*(?:内\s*容|资\s*料|课\s*程|资\s*源)|"
    r"内\s*部\s*配\s*套\s*分\s*享).{0,100}(?:添\s*加|加|联\s*系).{0,20}(?:作\s*者|客\s*服|老\s*师)?.{0,10}微\s*信"
)

# High-confidence standalone ad-only lines. Long prose is NEVER deleted solely
# because it contains a contact phrase; it is handled by span removal above.
STANDALONE_AD = re.compile(
    rf"(?i)^(?:[—\-–~·•\s]*)?(?:(?:具\s*体\s*)?(?:更\s*多\s*)?(?:落\s*地\s*细\s*节|"
    rf"更\s*多\s*(?:精\s*品|内\s*部)?\s*(?:课\s*程|资\s*料|资\s*源|电\s*子\s*书))[^。！？!?\n]{{0,80}})?"
    rf"{ADD_AUTHOR}{WX}\s*[：:=．.]*\s*{CRED}[^。！？!?\n]{{0,120}}[。！？!?]?$"
)
PURE_CONTACT = re.compile(
    rf"(?i)^\s*(?:(?:微\s*信\s*号|微\s*信\s*ID|客\s*服\s*微\s*信|作\s*者\s*微\s*信|老\s*师\s*微\s*信|VX|V\s*信|威\s*信)\s*[：:=．.]?\s*)?{CRED}(?:\s*电\s*\d[\d ]{{5,}})?\s*$"
)

# Residual audit only. These are candidates, not auto-deletion rules.
BROAD_REVIEW = re.compile(
    r"(?i)(?:添\s*加\s*作\s*者\s*微\s*信|作\s*者\s*微\s*信|客\s*服\s*微\s*信|老\s*师\s*微\s*信|"
    r"更\s*多\s*资\s*料\s*加\s*威\s*信|更\s*多\s*精\s*品\s*课\s*程\s*加\s*威\s*信|关\s*注\s*本\s*公\s*众\s*号|"
    r"更\s*多\s*内\s*部\s*绝\s*密\s*资\s*料\s*关\s*注\s*公\s*众\s*号)"
)


def unwrap(line: str) -> str:
    s = line.strip()
    s = re.sub(r"^#{1,6}\s*", "", s)
    s = re.sub(r"^>+\s*", "", s)
    s = re.sub(r"^[-*+]\s+", "", s)
    s = re.sub(r"^\d+\s*[.．、)]\s+", "", s)
    s = re.sub(r"^\*\*(.*?)\*\*$", r"\1", s)
    return s.strip()


def normalize_punctuation(s: str) -> str:
    s = re.sub(r"[，,]\s*[，,]", "，", s)
    s = re.sub(r"；\s*；", "；", s)
    s = re.sub(r"。\s*。", "。", s)
    s = re.sub(r"\s{2,}", " ", s) if len(s) < 240 else s
    return s.strip()


def strip_special_spans(content: str) -> tuple[str, list[str]]:
    """Remove only proven ad spans; never discard surrounding正文."""
    s = content
    kinds: list[str] = []
    rules = [
        (GLUED_PREFIX, "glued-prefix"),
        (INLINE_RESOURCE_TOKEN, "inline-resource-token"),
        (PAREN_AD, "parenthetical-contact"),
        (PAREN_RESOURCE_AD, "parenthetical-resource"),
        (AUDIO_PROMO_SPAN, "audio-resource-promo"),
        (PUBLIC_RESOURCE_SPAN, "public-account-resource"),
        (PERSONAL_ACCOUNT_TAIL, "personal-account-tail"),
        (AUTHOR_CTA, "author-cta"),
        (AUTHOR_CONTACT_SPAN, "author-contact-span"),
    ]
    for rx, kind in rules:
        new, count = rx.subn("", s)
        if count:
            kinds.extend([kind] * count)
            s = new

    # Known OCR pattern: a promo prefix is followed by the actual next section
    # in the same physical line. Keep the next-section words.
    m = re.match(
        r"(?i)^\s*更\s*多\s*落\s*地\s*细\s*节.{0,120}?"
        r"(?:添\s*加|加)\s*作\s*者\s*微\s*信.{0,120}?"
        r"(?=(?:圈\s*子\s*比\s*努\s*力|收\s*钱\s*之\s*术|如\s*果\s*你\s*现\s*在))",
        s,
    )
    if m:
        s = s[m.end():]
        kinds.append("ocr-promo-prefix")

    return normalize_punctuation(s), kinds


def line_parts(line: str) -> tuple[str, str]:
    m = HEAD.match(line)
    if not m:
        return "", line
    return m.group(1) + " ", m.group(2)


def is_ad_heading(content: str) -> bool:
    return bool(AD_HEADING.search(content) or STANDALONE_AD.match(content))


def is_standalone_ad(content: str) -> bool:
    s = content.strip()
    if not s:
        return False
    if len(s) > 240:
        return False
    return bool(STANDALONE_AD.match(s) or (PURE_CONTACT.match(s) and re.search(r"(?:VX|V\s*信|威\s*信|微\s*信)", s, re.I)))


def clean_text(text: str) -> tuple[str, dict]:
    images = Counter(IMG.findall(text))
    out: list[str] = []
    actions: list[dict] = []
    heading_shifts: list[dict] = []
    fenced = False
    removed_heading_level: int | None = None

    for n, raw in enumerate(text.splitlines(), 1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fenced = not fenced
            out.append(raw)
            removed_heading_level = None
            continue
        if fenced or IMG.search(raw):
            out.append(raw)
            continue

        prefix, content = line_parts(raw)
        heading_level = len(prefix.strip()) if prefix else None

        # Remove a false promotional heading as a structural unit.
        if heading_level and is_ad_heading(content):
            actions.append({"line": n, "kind": "ad-heading", "before": content[:240], "after": ""})
            removed_heading_level = heading_level
            continue

        cleaned, kinds = strip_special_spans(content)

        # A line may become an ad-only residue after span removal.
        if is_standalone_ad(cleaned):
            kinds.append("standalone-ad")
            cleaned = ""

        if kinds:
            actions.append({
                "line": n,
                "kind": "+".join(sorted(set(kinds))),
                "before": content[:300],
                "after": cleaned[:300],
            })

        if not cleaned.strip():
            # Only set heading parent if the removed original line was a heading.
            if heading_level:
                removed_heading_level = heading_level
            continue

        # Repair only a child level that was made too deep by the immediately
        # preceding removed advertising heading.
        if heading_level and removed_heading_level is not None:
            if heading_level > removed_heading_level:
                new_level = max(1, heading_level - 1)
                heading_shifts.append({
                    "line": n,
                    "title": cleaned[:180],
                    "from": heading_level,
                    "to": new_level,
                    "removed_ad_parent": removed_heading_level,
                })
                prefix = "#" * new_level + " "
            else:
                removed_heading_level = None

        out.append(prefix + cleaned if prefix else cleaned)

    if not actions and not heading_shifts:
        return text, {"actions": [], "heading_shifts": []}

    result = "\n".join(out)
    if text.endswith("\n"):
        result += "\n"
    if Counter(IMG.findall(result)) != images:
        raise RuntimeError("Markdown image references changed")
    return result, {"actions": actions, "heading_shifts": heading_shifts}


def heading_jumps(text: str) -> list[dict]:
    out: list[dict] = []
    prev: int | None = None
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fenced = not fenced
            continue
        if not fenced and (m := HEAD.match(line)):
            level = len(m.group(1))
            if prev is not None and level > prev + 1:
                out.append({"line": n, "previous": prev, "level": level, "title": m.group(2)[:160]})
            prev = level
    return out


def h1_count(text: str) -> int:
    return len(re.findall(r"^#\s+", text, re.M))


def process(path: Path) -> dict:
    before = path.read_text(encoding="utf-8-sig")
    after, info = clean_text(before)
    if h1_count(after) != h1_count(before):
        raise RuntimeError(f"H1 count would change from {h1_count(before)} to {h1_count(after)}")
    if len(heading_jumps(after)) > len(heading_jumps(before)):
        raise RuntimeError("cleanup would introduce a new heading-level jump")
    changed = before != after
    if changed:
        path.write_text(after, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "ad_spans_removed": len(info["actions"]),
        "heading_changes": len(info["heading_shifts"]),
        "examples": info["actions"][:12],
        "heading_examples": info["heading_shifts"][:8],
    }


def patch_prompt(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    marker = "- 不得因为清理广告而删除整段有价值正文。"
    extra = """
- 广告可能被错误包装成 `#` / `##` / `###` 等标题、列表项、引用块或粗体短句；识别时应先去掉 Markdown 外壳再判断；
- **广告清理的默认单位是“广告片段”，不是“整行”。** 一行中只要仍包含正常正文，就必须保留正文，只删除广告前缀、广告尾巴、括号联系方式或嵌入式引流片段；
- 广告可能直接粘在正文前后，例如“更多资料加威信xxxx，正文……”或“正文……添加作者微信xxxx获取资料”；必须只剥离广告串，不能删除整句正文；
- **不能因为正文出现“微信、朋友圈、公众号、扫码、微信群、微信号、电子书、资源”等词就删除。** 正文讨论微信获客、朋友圈运营、扫码案例、公众号营销、联系人微信等，都属于正文；
- 高置信广告通常同时包含“书外引流目的 + 行动指令 + 联系方式/资源领取”中的两项以上，例如“添加作者微信获取资料”“扫码添加老师私人微信”“关注本公众号领取模板”；单纯叙述“老师的微信”“客户加微信”不是广告；
- 广告若被错误识别成标题，应删除该广告标题，并只修复由这个伪标题直接造成的子标题下沉；不得借广告清理之名批量重排与广告无关的标题；
- 删除广告后若留下残缺括号、孤立标点、空标题或标题跳级，应同步修复；
- 批量处理目录时必须递归检查目标目录下全部 `.md` 正文文件，而不是只扫描根层；完成后必须再次扫描高置信广告残留和标题跳级，并保留审计报告。
""".rstrip()
    if marker not in text:
        raise RuntimeError("prompt marker not found")
    if "广告清理的默认单位是“广告片段”，不是“整行”" in text:
        return False
    path.write_text(text.replace(marker, marker + "\n" + extra, 1), encoding="utf-8")
    return True


def high_confidence_residuals(text: str) -> list[dict]:
    out: list[dict] = []
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced or IMG.search(line):
            continue
        plain = unwrap(line)
        # Use only the rules that are safe enough to require zero leftovers.
        if (
            GLUED_PREFIX.search(plain)
            or INLINE_RESOURCE_TOKEN.search(plain)
            or PAREN_AD.search(plain)
            or PAREN_RESOURCE_AD.search(plain)
            or PUBLIC_RESOURCE_SPAN.search(plain)
            or PERSONAL_ACCOUNT_TAIL.search(plain)
            or AD_HEADING.search(plain)
        ):
            out.append({"line": n, "text": plain[:300]})
            if len(out) >= 12:
                break
    return out


def review_candidates(text: str) -> list[dict]:
    out: list[dict] = []
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced or IMG.search(line):
            continue
        plain = unwrap(line)
        if len(plain) <= 450 and BROAD_REVIEW.search(plain):
            out.append({"line": n, "text": plain[:350]})
            if len(out) >= 12:
                break
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="temp")
    ap.add_argument("--prompt", default=".prompt/Markdown文档整理与修复通用提示词.md")
    ap.add_argument("--report", default="temp/.ad-heading-cleanup-report.json")
    args = ap.parse_args()

    root = Path(args.root)
    files = sorted(p for p in root.rglob("*.md") if p.is_file() and not p.name.startswith("."))
    prompt_changed = patch_prompt(Path(args.prompt))
    results: list[dict] = []
    errors: list[dict] = []
    for p in files:
        try:
            results.append(process(p))
        except Exception as exc:
            errors.append({"path": str(p), "error": str(exc)})

    residuals: list[dict] = []
    review: list[dict] = []
    jump_files: list[dict] = []
    for p in files:
        text = p.read_text(encoding="utf-8-sig")
        r = high_confidence_residuals(text)
        if r:
            residuals.append({"path": str(p), "examples": r})
        c = review_candidates(text)
        if c:
            review.append({"path": str(p), "examples": c})
        j = heading_jumps(text)
        if j:
            jump_files.append({"path": str(p), "examples": j[:10]})

    changed = [x for x in results if x["changed"]]
    report = {
        "prompt_strengthened": prompt_changed,
        "changed_files": changed,
        "high_confidence_residuals": residuals,
        "review_candidates": review,
        "heading_jump_files": jump_files,
        "errors": errors,
        "summary": {
            "markdown_files_scanned": len(files),
            "markdown_files_changed": len(changed),
            "ad_spans_removed": sum(x["ad_spans_removed"] for x in results),
            "heading_changes": sum(x["heading_changes"] for x in results),
            "high_confidence_residual_files": len(residuals),
            "review_candidate_files": len(review),
            "heading_jump_files": len(jump_files),
            "errors": len(errors),
        },
    }
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors or residuals else 0


if __name__ == "__main__":
    raise SystemExit(main())
