#!/usr/bin/env python3
"""Recursively clean high-confidence ads from temp Markdown and repair headings.

Rules are a deterministic subset of
.prompt/Markdown文档整理与修复通用提示词.md. The script never changes a
Markdown image reference and avoids deleting ordinary prose that merely mentions
WeChat/公众号.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

IMG = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
CN = r"[一二三四五六七八九十百千万〇零两0-9]+"
CHAPTER = re.compile(rf"^第\s*{CN}\s*章(?:\s|[：:、.．-]|$)")
SECTION = re.compile(rf"^第\s*{CN}\s*节(?:\s|[：:、.．-]|$)")
SUBNO = re.compile(rf"^第\s*{CN}\s*(?:诀|套|招|计|式|法|步|关|课|讲)(?:\s|[：:、.．-]|$)")

CONTACT_ID = re.compile(
    r"(?i)(?:微信|微\s*信|V\s*信|V\s*X|VX|weixin|wechat)\s*"
    r"(?:号|ID|账号|：|:|=)?\s*[A-Za-z][A-Za-z0-9_%\-.]{2,}"
)
MARKER = re.compile(
    r"(?i)(?:加我?微信|添加(?:我|客服|老师|助理|小编|作者)?微信|客服微信|联系微信|"
    r"微信号|微信ID|V信|VX|扫码添加|扫码关注|获取资料请|领取资料请|"
    r"更多电子书|更多资料|更多资源)"
)
PROMO_CONTACT = re.compile(
    r"(?i)(?:加|添加|扫码(?:添加)?|联系|客服|咨询|私信|获取(?:请)?|领取(?:请)?)"
    r".{0,10}(?:微信|微\s*信|V\s*信|V\s*X|VX|weixin|wechat)"
)
RESOURCE_PROMO = re.compile(
    r"(?i)(?:更多|海量|精品|完整|全套|免费|领取|获取|购买|需要|想要)"
    r".{0,24}(?:电子书|电子版|书籍|资料|资源|课程|教程|合集)"
    r".{0,30}(?:微信|V信|VX|扫码|二维码|公众号|联系|添加)"
)
SOCIAL_PROMO = re.compile(
    r"(?i)(?:朋友圈.{0,28}(?:每日|持续|更新|资料|资源|电子书|课程|领取|获取)|"
    r"(?:关注|搜索|扫码关注).{0,12}(?:公众号|订阅号).{0,24}(?:领取|获取|资料|资源|电子书|课程|更多)?|"
    r"(?:资源群|读者群|交流群|福利群).{0,24}(?:微信|扫码|二维码|加入|添加|VX|V信))"
)
THANKS_PROMO = re.compile(
    r"(?i)感谢(?:您|你)?(?:的)?阅读.{0,36}(?:微信|电子版|电子书|资料|资源|公众号|更多|领取|获取)"
)
PURE_CONTACT = re.compile(
    r"(?i)^\s*(?:微信|微\s*信|V\s*信|VX|微信号|微信ID|ID|客服)?\s*"
    r"[：:=]?\s*[A-Za-z][A-Za-z0-9_%\-.]{2,}\s*$"
)
AD_NEIGHBOR = re.compile(
    r"(?i)^(?:微信号|微信ID|客服微信|扫码|扫描二维码|长按识别|二维码|添加好友|"
    r"关注公众号|公众号|获取更多|领取更多|更多资源|更多电子书|资源群|交流群).{0,50}$"
)
BROAD = re.compile(
    r"(?i)(?:加.{0,5}微信|添加.{0,8}微信|微信号|微信ID|客服微信|V信|VX|"
    r"扫码.{0,8}(?:微信|二维码|公众号)|公众号.{0,12}(?:资源|资料|电子书|领取|获取)|"
    r"(?:更多|领取|获取).{0,18}(?:电子书|资料|资源).{0,18}(?:微信|扫码|公众号))"
)


def unwrap(line: str) -> str:
    s = line.strip()
    s = re.sub(r"^#{1,6}\s*", "", s)
    s = re.sub(r"^>+\s*", "", s)
    s = re.sub(r"^[-*+]\s+", "", s)
    s = re.sub(r"^\d+\s*[.．、)]\s+", "", s)
    s = re.sub(r"^\*\*(.*?)\*\*$", r"\1", s)
    return s.strip()


def strong_ad(line: str) -> bool:
    if not line or IMG.search(line):
        return False
    raw, s = line.strip(), unwrap(line)
    if not s:
        return False
    wrapped = bool(re.match(r"^(?:#{1,6}\s*|>+\s*|[-*+]\s+|\d+\s*[.．、)]\s+)", raw))
    context = bool(re.search(
        r"(?:电子书|电子版|资料|资源|课程|教程|合集|领取|获取|客服|作者|老师|助理|小编|扫码|二维码|咨询|私信)", s, re.I
    ))
    marker = MARKER.search(s)
    mixed = bool(marker and marker.start() > 0 and re.search(r"[。！？；;：:,，、|｜—-]\s*$", s[:marker.start()]))
    if CONTACT_ID.search(s) and len(s) <= 140 and not mixed:
        if marker or wrapped or context or PURE_CONTACT.match(s):
            return True
    if len(s) <= 180 and (RESOURCE_PROMO.search(s) or SOCIAL_PROMO.search(s) or THANKS_PROMO.search(s)):
        return True
    return bool(len(s) <= 120 and PROMO_CONTACT.search(s) and context)


def neighbor(line: str) -> bool:
    s = unwrap(line)
    return bool(s and not IMG.search(s) and (PURE_CONTACT.match(s) or (len(s) <= 70 and AD_NEIGHBOR.match(s))))


def strip_ad_tail(line: str) -> tuple[str, bool]:
    if IMG.search(line) or len(line) < 6:
        return line, False
    for m in MARKER.finditer(line):
        pos = m.start()
        if pos < 2:
            continue
        prefix, tail = line[:pos].rstrip(), line[pos:].strip()
        if len(tail) > 180:
            continue
        if prefix[-1:] not in "。！？；;：:，,、|｜—- ）)]】》" and not line[pos - 1].isspace():
            continue
        if strong_ad(tail) or CONTACT_ID.search(tail) or RESOURCE_PROMO.search(tail):
            return prefix.rstrip(" |｜—-"), True
    return line, False


def clean_ads(text: str) -> tuple[str, dict]:
    imgs = Counter(IMG.findall(text))
    out, removed, tails, shifts = [], [], [], []
    budget = 0
    removed_level = None
    fenced = False
    for n, raw in enumerate(text.splitlines(), 1):
        line, s = raw.rstrip(), raw.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fenced = not fenced
            out.append(line)
            budget, removed_level = 0, None
            continue
        if fenced:
            out.append(line)
            continue
        hm = HEAD.match(line)
        if strong_ad(line):
            level = len(hm.group(1)) if hm else None
            removed.append({"line": n, "text": unwrap(line)[:180], "heading_level": level})
            if level is not None:
                removed_level = level
            budget = 2
            continue
        if budget and neighbor(line):
            removed.append({"line": n, "text": unwrap(line)[:180], "adjacent": True})
            budget -= 1
            continue
        if removed_level is not None and hm:
            level = len(hm.group(1))
            if level > removed_level:
                new = max(1, level - 1)
                title = hm.group(2).strip()
                shifts.append({"line": n, "title": title[:150], "from": level, "to": new, "ad_parent": removed_level})
                line = "#" * new + " " + title
            else:
                removed_level = None
        new_line, changed = strip_ad_tail(line)
        if changed:
            tails.append({"line": n, "before": line[:200], "after": new_line[:200]})
            line, budget = new_line, 2
        elif line.strip():
            budget = 0
        out.append(line)
    result = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    if Counter(IMG.findall(result)) != imgs:
        raise RuntimeError("Markdown image references changed while removing ads")
    return result, {"removed": removed, "tails": tails, "ad_heading_shifts": shifts}


def identity(path: Path, root: Path) -> str:
    raw = path.parent.name if path.name.lower() == "index.md" and path.parent != root else path.stem
    return re.sub(r"(?i)(?:[-_ ]?PDF版?|[-_ ]?纯文字版|[-_ ]?全文字版)$", "", raw)


def norm(s: str) -> str:
    s = unwrap(s)
    s = re.sub(r"[《》〈〉【】\[\]（）()\s·•—_\-:：,.，。'\"“”‘’]", "", s)
    return re.sub(r"(?i)PDF版?|纯文字版|全文字版", "", s).lower()


def same_title(a: str, b: str) -> bool:
    a, b = norm(a), norm(b)
    return bool(a and b and (a == b or (len(a) >= 4 and len(b) >= 4 and (a in b or b in a))))


def repair_headings(text: str, path: Path, root: Path) -> tuple[str, list[dict]]:
    lines = text.splitlines()
    heads, fenced = [], False
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fenced = not fenced
            continue
        if not fenced and (m := HEAD.match(line)):
            heads.append((i, len(m.group(1)), m.group(2).strip()))
    if not heads:
        raise RuntimeError("no Markdown heading remains")

    title_i = next((i for i, _l, t in heads if same_title(t, identity(path, root))), None)
    if title_i is None:
        title_i = next((i for i, l, _t in heads if l == 1), None)
    if title_i is None:
        first_chapter = next((i for i, _l, t in heads if CHAPTER.match(t)), None)
        title_i = next((i for i, _l, _t in heads if first_chapter is None or i < first_chapter), heads[0][0])

    changes, prev, chapter_seen, fenced = [], 0, False, False
    for i, raw in enumerate(lines):
        s = raw.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced or not (m := HEAD.match(raw)):
            continue
        old, title = len(m.group(1)), m.group(2).strip()
        level = old
        if i == title_i:
            level = 1
        elif CHAPTER.match(title):
            level, chapter_seen = 2, True
        elif SECTION.match(title):
            level = 3 if chapter_seen else 2
        elif SUBNO.match(title):
            level = 3 if chapter_seen else min(max(level, 2), 3)
        elif level == 1:
            level = 3 if chapter_seen else 2
        if i != title_i and prev and level > prev + 1:
            level = prev + 1
        if level != old:
            changes.append({"line": i + 1, "title": title[:150], "from": old, "to": level})
            lines[i] = "#" * level + " " + title
        prev = level
    result = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"
    h1 = len(re.findall(r"^#\s+", result, re.M))
    if h1 != 1:
        raise RuntimeError(f"expected exactly one H1, got {h1}")
    return result, changes


def patch_prompt(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    marker = "- 不得因为清理广告而删除整段有价值正文。"
    extra = """
- 广告可能被错误包装成 `#` / `##` / `###` 等标题、列表项、引用块或粗体短句；识别时应先去掉这些 Markdown 外壳，不能因为它像标题就保留；
- 广告常被拆成连续多行，例如“获取更多资料请加微信”下一行才是微信号 / ID；高置信时应按**广告块**清理，但不得跨过正常正文继续删除；
- 对“正文句子 + 广告尾巴”的混合行，只删除后半段高置信广告尾巴，保留前面的正常正文；
- 删除广告标题、联系方式标题或噪声标题后，必须重新校验其前后标题层级，修复由广告造成的章节整体下沉、`##` 后直接 `####` 等结构损伤；
- 批量处理目录时必须递归检查目标目录下全部 `.md` 正文文件，而不是只扫描根层；
- 最终广告校验应覆盖“加微信 / 添加微信 / 客服微信 / 微信号 / 微信ID / V信 / VX / 扫码添加 / 资源领取 / 公众号引流”等变体，同时通过语义和上下文保留正文中正常讨论微信、公众号等词的内容。
""".rstrip()
    if marker not in text or "广告可能被错误包装成 `#` / `##` / `###`" in text:
        return False
    path.write_text(text.replace(marker, marker + "\n" + extra, 1), encoding="utf-8")
    return True


def residual(text: str) -> list[dict]:
    out, fenced = [], False
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fenced = not fenced
            continue
        plain = unwrap(line)
        if not fenced and not IMG.search(line) and len(plain) <= 220 and BROAD.search(plain):
            out.append({"line": n, "text": plain[:220]})
            if len(out) == 12:
                break
    return out


def jumps(text: str) -> list[dict]:
    out, prev, fenced = [], None, False
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fenced = not fenced
            continue
        if not fenced and (m := HEAD.match(line)):
            level = len(m.group(1))
            if prev is not None and level > prev + 1:
                out.append({"line": n, "previous": prev, "level": level, "title": m.group(2)[:120]})
            prev = level
    return out[:12]


def process(path: Path, root: Path) -> dict:
    before = path.read_text(encoding="utf-8-sig")
    imgs = Counter(IMG.findall(before))
    no_ads, ad = clean_ads(before)
    after, heading = repair_headings(no_ads, path, root)
    if Counter(IMG.findall(after)) != imgs:
        raise RuntimeError("Markdown image references changed")
    changed = before != after
    if changed:
        path.write_text(after, encoding="utf-8")
    return {
        "path": str(path), "changed": changed,
        "ad_lines_removed": len(ad["removed"]),
        "inline_ad_tails_removed": len(ad["tails"]),
        "heading_changes": len(ad["ad_heading_shifts"]) + len(heading),
        "ad_examples": ad["removed"][:5],
        "heading_examples": (ad["ad_heading_shifts"] + heading)[:6],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="temp")
    ap.add_argument("--prompt", default=".prompt/Markdown文档整理与修复通用提示词.md")
    ap.add_argument("--report", default="temp/.ad-heading-cleanup-report.json")
    args = ap.parse_args()
    root = Path(args.root)
    files = sorted(p for p in root.rglob("*.md") if p.is_file() and not p.name.startswith("."))
    results, errors = [], []
    prompt_changed = patch_prompt(Path(args.prompt))
    for p in files:
        try:
            results.append(process(p, root))
        except Exception as exc:
            errors.append({"path": str(p), "error": str(exc)})

    validation = []
    for p in files:
        text = p.read_text(encoding="utf-8-sig")
        r, j = residual(text), jumps(text)
        h1 = len(re.findall(r"^#\s+", text, re.M))
        if r or j or h1 != 1:
            validation.append({"path": str(p), "residual_ad_candidates": r, "heading_jumps": j, "h1_count": h1})

    changed = [x for x in results if x["changed"]]
    report = {
        "prompt_strengthened": prompt_changed,
        "changed_files": changed,
        "validation_issues": validation,
        "errors": errors,
        "summary": {
            "markdown_files_scanned": len(files),
            "markdown_files_changed": len(changed),
            "ad_lines_removed": sum(x["ad_lines_removed"] for x in results),
            "inline_ad_tails_removed": sum(x["inline_ad_tails_removed"] for x in results),
            "heading_changes": sum(x["heading_changes"] for x in results),
            "validation_issue_files": len(validation),
            "errors": len(errors),
        },
    }
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
