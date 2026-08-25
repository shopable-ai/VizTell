#!/usr/bin/env python3
"""Conservatively remove third-party promo/contact ads from temp Markdown.

This is a deterministic safety pass for the repository's Markdown cleanup prompt.
It recursively scans temp/**/*.md, preserves all Markdown image references and
ordinary prose, and only repairs heading depth when a removed ad heading was a
false structural parent.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

IMG = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
CRED = r"[A-Za-z0-9][A-Za-z0-9_%\-.]{3,}"
ROLE = r"(?:作者|本书作者|客服|老师|讲师|助理|小编|班主任|顾问|私人|官方)"
CHANNEL = r"(?:微信|微\s*信|威信|V\s*信|V\s*X|VX|weixin|wechat)"

ROLE_CONTACT = re.compile(
    rf"(?i)(?:添加|加|联系|扫码添加|搜索|私信|咨询)?"
    rf".{{0,8}}{ROLE}.{{0,10}}{CHANNEL}(?:号|ID|账号)?"
)
CRED_CONTACT = re.compile(
    rf"(?i)(?:微信号|微信ID|客服微信|作者微信|老师微信|私人微信|V信|VX|威信)"
    rf"\s*[：:=]?\s*{CRED}"
)
DIRECT_RESOURCE = re.compile(
    r"(?i)(?:更多|具体更多|内部|精品|完整|全套).{0,24}"
    r"(?:落地细节|电子书|电子版|资料|资源|课程|模板|干货|分享).{0,32}"
    r"(?:添加|加|联系|扫码|关注|搜索).{0,18}(?:微信|威信|V信|VX|公众号|订阅号)"
)
DIRECT_PUBLIC = re.compile(
    r"(?i)(?:(?:立刻|马上|现在)?扫码)?(?:关注|搜索)本公众号|"
    r"扫码关注.{0,10}本公众号|"
    r"回复[“\"『「]?[^”\"』」]{1,12}[”\"』」]?(?:二字|即可)?.{0,18}(?:送|领取|获取).{0,18}(?:资料|模板|课程|电子书|资源)"
)
THANKS_PROMO = re.compile(
    r"(?i)感谢(?:您|你)?(?:的)?阅读.{0,40}(?:更多|领取|获取|添加|联系).{0,28}(?:微信|公众号|电子版|电子书|资料|资源)"
)
SEARCH_CREDENTIAL = re.compile(
    rf"(?i)(?:扫码添加|添加|加).{{0,12}}{ROLE}.{{0,12}}(?:微信|威信)"
    rf".{{0,30}}(?:搜索|微信号|ID|账号|回复).{{0,12}}(?:【)?{CRED}(?:】)?"
)
TAIL_MARKER = re.compile(
    r"(?i)(?:具体更多落地细节|更多落地细节|具体落地细节|添加作者微信|"
    r"添加客服微信|添加老师微信|扫码添加.{0,8}(?:老师|作者|客服)|"
    r"更多精品(?:课程|资料|资源|电子书)|关注本公众号|扫码关注本公众号|"
    r"感谢(?:您|你)?(?:的)?阅读.{0,12}(?:如需|需要|获取|领取))"
)
PURE_ID = re.compile(rf"(?i)^\s*(?:(?:微信|威信|V信|VX|ID|账号|客服)\s*[：:=]?\s*)?{CRED}\s*$")
AD_NEIGHBOR = re.compile(r"(?i)^(?:微信号|微信ID|客服微信|作者微信|老师微信|私人微信|扫码|扫描二维码|长按识别|关注本公众号|回复.{0,12}(?:领取|获取)).{0,60}$")
BROAD_REVIEW = re.compile(
    r"(?i)(?:作者微信|客服微信|老师微信|私人微信|微信号|微信ID|加.{0,5}微信|添加.{0,8}微信|"
    r"威信[A-Za-z0-9]|V信|VX|扫码关注|关注本公众号|更多.{0,18}(?:资料|资源|电子书).{0,18}(?:微信|公众号|扫码))"
)


def unwrap(line: str) -> str:
    s = line.strip()
    s = re.sub(r"^#{1,6}\s*", "", s)
    s = re.sub(r"^>+\s*", "", s)
    s = re.sub(r"^[-*+]\s+", "", s)
    s = re.sub(r"^\d+\s*[.．、)]\s+", "", s)
    s = re.sub(r"^\*\*(.*?)\*\*$", r"\1", s)
    return s.strip()


def direct_ad(line: str) -> bool:
    if not line or IMG.search(line):
        return False
    s = unwrap(line)
    if not s:
        return False
    return bool(
        ROLE_CONTACT.search(s)
        or CRED_CONTACT.search(s)
        or DIRECT_RESOURCE.search(s)
        or DIRECT_PUBLIC.search(s)
        or THANKS_PROMO.search(s)
        or SEARCH_CREDENTIAL.search(s)
    )


def mixed_prefix(line: str) -> bool:
    """True when a direct ad begins after a plausible正文 sentence."""
    for m in TAIL_MARKER.finditer(line):
        if m.start() < 2:
            continue
        prefix = line[:m.start()].rstrip()
        if prefix and (prefix[-1] in "。！？；;：:，,、|｜—-）)]】》" or line[m.start()-1].isspace()):
            return True
    return False


def whole_line_ad(line: str) -> bool:
    return direct_ad(line) and not mixed_prefix(line)


def strip_tail(line: str) -> tuple[str, bool]:
    if IMG.search(line):
        return line, False
    for m in TAIL_MARKER.finditer(line):
        if m.start() < 2:
            continue
        prefix, tail = line[:m.start()].rstrip(), line[m.start():].strip()
        if not prefix or len(tail) > 260:
            continue
        if prefix[-1] not in "。！？；;：:，,、|｜—-）)]】》" and not line[m.start()-1].isspace():
            continue
        if direct_ad(tail):
            return prefix.rstrip(" |｜—-"), True
    return line, False


def neighbor(line: str) -> bool:
    s = unwrap(line)
    return bool(s and not IMG.search(line) and (PURE_ID.fullmatch(s) or AD_NEIGHBOR.match(s)))


def clean_text(text: str) -> tuple[str, dict]:
    images = Counter(IMG.findall(text))
    out: list[str] = []
    removed: list[dict] = []
    tails: list[dict] = []
    shifts: list[dict] = []
    fenced = False
    neighbor_budget = 0
    removed_heading_level: int | None = None

    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fenced = not fenced
            out.append(line)
            neighbor_budget = 0
            removed_heading_level = None
            continue
        if fenced:
            out.append(line)
            continue

        hm = HEAD.match(line)
        if whole_line_ad(line):
            level = len(hm.group(1)) if hm else None
            removed.append({"line": n, "text": unwrap(line)[:220], "heading_level": level})
            if level is not None:
                removed_heading_level = level
            neighbor_budget = 2
            continue

        if neighbor_budget and neighbor(line):
            removed.append({"line": n, "text": unwrap(line)[:220], "adjacent": True})
            neighbor_budget -= 1
            continue

        # Only repair hierarchy that can be causally attributed to an ad heading.
        if removed_heading_level is not None and hm:
            level = len(hm.group(1))
            if level > removed_heading_level:
                new_level = level - 1
                title = hm.group(2).strip()
                shifts.append({"line": n, "title": title[:180], "from": level, "to": new_level, "ad_parent": removed_heading_level})
                line = "#" * new_level + " " + title
            else:
                removed_heading_level = None

        new_line, changed = strip_tail(line)
        if changed:
            tails.append({"line": n, "before": line[:260], "after": new_line[:220]})
            line = new_line
            neighbor_budget = 2
        elif line.strip():
            neighbor_budget = 0
        out.append(line)

    result = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    if Counter(IMG.findall(result)) != images:
        raise RuntimeError("Markdown image references changed")
    return result, {"removed": removed, "tails": tails, "heading_shifts": shifts}


def h1_count(text: str) -> int:
    return len(re.findall(r"^#\s+", text, re.M))


def jumps(text: str) -> list[tuple[int, int, int]]:
    out, prev, fenced = [], None, False
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fenced = not fenced
            continue
        if not fenced and (m := HEAD.match(line)):
            level = len(m.group(1))
            if prev is not None and level > prev + 1:
                out.append((n, prev, level))
            prev = level
    return out


def process(path: Path) -> dict:
    before = path.read_text(encoding="utf-8-sig")
    after, info = clean_text(before)
    # Existing files were already validated as one-H1 documents. Never make this worse.
    if h1_count(after) != h1_count(before):
        raise RuntimeError(f"H1 count would change from {h1_count(before)} to {h1_count(after)}")
    if len(jumps(after)) > len(jumps(before)):
        raise RuntimeError("heading cleanup would introduce a new level jump")
    changed = before != after
    if changed:
        path.write_text(after, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "ad_lines_removed": len(info["removed"]),
        "inline_ad_tails_removed": len(info["tails"]),
        "heading_changes": len(info["heading_shifts"]),
        "ad_examples": info["removed"][:8],
        "tail_examples": info["tails"][:5],
        "heading_examples": info["heading_shifts"][:8],
    }


def patch_prompt(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    marker = "- 不得因为清理广告而删除整段有价值正文。"
    extra = """
- 广告可能被错误包装成 `#` / `##` / `###` 等标题、列表项、引用块或粗体短句；识别时应先去掉 Markdown 外壳再判断；
- 广告常被拆成连续多行，例如引流句下一行才是微信号 / ID；仅在上下文能够高置信确认属于同一广告块时连续清理；
- 对“正文句子 + 广告尾巴”的混合行，只删除后半段明确的第三方引流尾巴，前面的正文必须保留；
- **不能因为正文出现“微信、朋友圈、公众号、扫码、电子书、资源”等词就删除。** 例如正文讨论微信获客、朋友圈运营、扫码案例、公众号营销时都属于正文，应完整保留；
- 优先删除的高置信广告包括：作者 / 客服 / 老师私人微信号、明确联系方式、领取更多资料 / 课程 / 电子书的第三方引流、关注“本公众号”的书外宣传等；
- 删除广告标题后，才对其直接造成的子标题下沉进行层级上移；不得借广告清理之名批量重排与广告无关的标题；
- 批量处理目录时必须递归检查目标目录下全部 `.md` 正文文件，而不是只扫描根层。
""".rstrip()
    if marker not in text or "不能因为正文出现“微信、朋友圈、公众号、扫码、电子书、资源”等词就删除" in text:
        return False
    path.write_text(text.replace(marker, marker + "\n" + extra, 1), encoding="utf-8")
    return True


def review_candidates(text: str) -> list[dict]:
    out, fenced = [], False
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fenced = not fenced
            continue
        plain = unwrap(line)
        if not fenced and not IMG.search(line) and len(plain) <= 280 and BROAD_REVIEW.search(plain):
            out.append({"line": n, "text": plain[:280], "direct_ad": direct_ad(line)})
            if len(out) >= 15:
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
    results, errors = [], []
    prompt_changed = patch_prompt(Path(args.prompt))
    for p in files:
        try:
            results.append(process(p))
        except Exception as exc:
            errors.append({"path": str(p), "error": str(exc)})

    residual_direct, review = [], []
    for p in files:
        text = p.read_text(encoding="utf-8-sig")
        direct = []
        for n, line in enumerate(text.splitlines(), 1):
            if direct_ad(line) and not mixed_prefix(line) and not IMG.search(line):
                direct.append({"line": n, "text": unwrap(line)[:260]})
                if len(direct) >= 8:
                    break
        if direct:
            residual_direct.append({"path": str(p), "examples": direct})
        candidates = review_candidates(text)
        if candidates:
            review.append({"path": str(p), "examples": candidates})

    changed = [x for x in results if x["changed"]]
    report = {
        "prompt_strengthened": prompt_changed,
        "changed_files": changed,
        "residual_direct_ads": residual_direct,
        "review_candidates": review,
        "errors": errors,
        "summary": {
            "markdown_files_scanned": len(files),
            "markdown_files_changed": len(changed),
            "ad_lines_removed": sum(x["ad_lines_removed"] for x in results),
            "inline_ad_tails_removed": sum(x["inline_ad_tails_removed"] for x in results),
            "heading_changes": sum(x["heading_changes"] for x in results),
            "residual_direct_ad_files": len(residual_direct),
            "review_candidate_files": len(review),
            "errors": len(errors),
        },
    }
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
