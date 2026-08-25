#!/usr/bin/env python3
"""Content-level audit and conservative repair for Markdown books under temp/.

This is intentionally different from a timestamp/commit based progress check.
Git history is recorded as weak evidence only. A file passes only when its
current contents satisfy structural invariants derived from
.prompt/Markdown文档整理与修复通用提示词.md.

Safe automatic repairs in this script are limited to high-confidence cases:
- textual leading TOCs with page-number leaders, even when <!-- page:N --> markers
  have already disappeared;
- headings recovered from those TOC titles, including titles glued to the first
  sentence of their body section;
- duplicate H1 book-title lines;
- conversion-only labels/comments and high-confidence OCR page numbers;
- exact preservation of every Markdown image reference.

Anything that cannot be repaired conservatively is reported as needs_review
rather than being force-edited.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path

HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMAGE = re.compile(r"!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]")
PAGE_IMAGE = re.compile(r"!\[[^\]]*第\s*(\d+)\s*页原始页面图[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\([^\n)]*assets/page[-_]?(\d+)[^\n)]*\)", re.I)
PAGE_COMMENT = re.compile(r"^\s*<!--\s*page\s*:\s*\d+\s*-->\s*$", re.I)
IMAGE_COMMENT = re.compile(r"^\s*<!--\s*Image\s*\([^>]*\)\s*-->\s*$", re.I)
TOC_LEADER = re.compile(r"(.{2,160}?)(?:\.{4,}|…{3,}|·{4,}|﹒{4,})\s*[.·… ]*(\d{1,4})(?=\D|$)")
CHAPTER = re.compile(r"^第\s*[一二三四五六七八九十百零〇两0-9]+\s*章\b.*$")
SECTION = re.compile(r"^第\s*[一二三四五六七八九十百零〇两0-9]+\s*节\b.*$")
PART = re.compile(r"^(?:第\s*[一二三四五六七八九十百零〇两0-9]+\s*(?:部分|篇|部|卷|册)|上篇|中篇|下篇|Part\s+\d+)\b.*$", re.I)
PURE_NUMBER = re.compile(r"^\s*(\d{1,4})\s*$")
CONVERSION_LABELS = {
    "视觉补充",
    "视觉说明",
    "ocr补充",
    "ocr文字补充",
    "页面视觉补充",
    "原始页面文字补充",
    "ai补充说明",
}


def strip_md_shell(s: str) -> str:
    s = s.strip()
    m = HEADING.match(s)
    if m:
        s = m.group(2).strip()
    s = re.sub(r"^\*\*(.*?)\*\*$", r"\1", s).strip()
    s = re.sub(r"^__(.*?)__$", r"\1", s).strip()
    return s


def compact(s: str) -> str:
    s = strip_md_shell(s)
    s = re.sub(r"\s+", "", s)
    s = s.translate(str.maketrans({"：": ":", "－": "-", "—": "-", "·": ""}))
    return s.lower()


def title_for(path: Path, lines: list[str]) -> str:
    for raw in lines[:60]:
        m = HEADING.match(raw.strip())
        if m and len(m.group(1)) == 1:
            t = strip_md_shell(raw)
            if t and t != "目录" and not CHAPTER.match(t):
                return t
    name = path.parent.name if path.name.lower() == "index.md" else path.stem
    m = re.match(r"^《(.+?)》(.*)$", name.strip())
    if m:
        name = (m.group(1) + m.group(2)).strip()
    return name.strip() or "未命名文档"


def image_refs(text: str) -> list[str]:
    return IMAGE.findall(text)


def visible_chars(text: str) -> int:
    x = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    x = IMAGE.sub("", x)
    x = re.sub(r"^#{1,6}\s*", "", x, flags=re.M)
    x = re.sub(r"[#*_>`~\s]", "", x)
    return len(x)


def git_meta(path: Path) -> dict:
    try:
        p = subprocess.run(
            ["git", "log", "-1", "--format=%H%x09%cI%x09%s", "--", str(path)],
            text=True,
            capture_output=True,
            check=False,
        )
        raw = p.stdout.strip()
        if not raw:
            return {}
        parts = raw.split("\t", 2)
        return {
            "last_commit_sha": parts[0] if len(parts) > 0 else None,
            "last_commit_date": parts[1] if len(parts) > 1 else None,
            "last_commit_message": parts[2] if len(parts) > 2 else None,
        }
    except Exception:
        return {}


def page_image_max(lines: list[str]) -> tuple[int, int]:
    nums: list[int] = []
    count = 0
    for raw in lines:
        for m in PAGE_IMAGE.finditer(raw):
            count += 1
            token = m.group(1) or m.group(2)
            if token:
                nums.append(int(token))
    return count, (max(nums) if nums else 0)


def clean_toc_candidate(s: str) -> str:
    s = strip_md_shell(s)
    s = re.sub(r"^\d{1,4}\s*", "", s).strip()
    s = re.sub(r"\s+", " ", s).strip(" .·…\t")
    return s


def looks_like_toc_marker(raw: str) -> bool:
    return compact(raw) in {"目录", "contents", "content"}


def nearby_leader(lines: list[str], idx: int, distance: int = 5) -> bool:
    for j in range(idx + 1, min(len(lines), idx + distance + 1)):
        if TOC_LEADER.search(strip_md_shell(lines[j])):
            return True
    return False


def discover_leading_toc(lines: list[str], title: str) -> dict:
    """Find textual TOC residue without requiring page comments.

    Only leader-based TOCs are auto-removed. Structural-only TOCs are audited
    but left untouched unless there is stronger evidence elsewhere.
    """
    scan_limit = min(len(lines), 500)
    marker: int | None = None
    for i in range(scan_limit):
        if looks_like_toc_marker(lines[i]):
            marker = i
            break

    leader_start: int | None = None
    start = marker + 1 if marker is not None else 0
    for i in range(start, scan_limit):
        if TOC_LEADER.search(strip_md_shell(lines[i])):
            leader_start = i
            break
        if marker is None and i > 120:
            break
        if marker is not None and i > marker + 40:
            break
    if leader_start is None:
        return {
            "marker": marker,
            "remove": set(),
            "candidates": [],
            "body_start": None,
            "leader_lines": 0,
        }

    remove: set[int] = set()
    candidates: list[str] = []
    leader_lines = 0
    if marker is not None:
        remove.add(marker)

    body_start: int | None = None
    seen_leader = False
    for i in range(leader_start, min(len(lines), leader_start + 420)):
        raw = lines[i]
        s = strip_md_shell(raw)
        if not s:
            continue
        if IMAGE.fullmatch(raw.strip()) or IMAGE_COMMENT.match(raw.strip()):
            continue
        matches = list(TOC_LEADER.finditer(s))
        if matches:
            seen_leader = True
            leader_lines += 1
            remove.add(i)
            for m in matches:
                c = clean_toc_candidate(m.group(1))
                if 2 <= len(c) <= 120 and compact(c) not in {compact(title), "目录"}:
                    candidates.append(c)
            continue
        if seen_leader and (CHAPTER.match(s) or SECTION.match(s) or PART.match(s)) and len(s) <= 140:
            remove.add(i)
            candidates.append(clean_toc_candidate(s))
            continue
        if seen_leader and len(s) <= 8 and nearby_leader(lines, i):
            # Typical OCR residue between concatenated TOC pages, e.g. a
            # one-character running footer. Do not use it as a title.
            remove.add(i)
            continue
        if seen_leader:
            # The first real prose line marks body start. A body heading may be
            # glued to this line; it is intentionally preserved for splitting.
            body_start = i
            break

    # Deduplicate while retaining TOC order.
    seen: set[str] = set()
    ordered: list[str] = []
    for c in candidates:
        k = compact(c)
        if not k or k in seen:
            continue
        seen.add(k)
        ordered.append(c)
    return {
        "marker": marker,
        "remove": remove,
        "candidates": ordered,
        "body_start": body_start,
        "leader_lines": leader_lines,
    }


def candidate_levels(candidates: list[str]) -> dict[str, tuple[int, str]]:
    has_chapter = any(CHAPTER.match(c) or PART.match(c) for c in candidates)
    result: dict[str, tuple[int, str]] = {}
    for c in candidates:
        if CHAPTER.match(c) or PART.match(c):
            level = 2
        elif SECTION.match(c):
            level = 3
        else:
            level = 3 if has_chapter else 2
        result[compact(c)] = (level, c)
    return result


def plausible_page_number_indices(lines: list[str]) -> set[int]:
    image_count, max_page = page_image_max(lines)
    if image_count < 3 or max_page < 3:
        return set()
    found: list[tuple[int, int]] = []
    for i, raw in enumerate(lines):
        m = PURE_NUMBER.match(raw)
        if m:
            found.append((i, int(m.group(1))))
    plausible = [(i, n) for i, n in found if 0 < n <= max_page + 5]
    if len(plausible) < 3:
        return set()
    if len(plausible) / max(1, len(found)) < 0.75:
        return set()
    # A page-number sequence need not be perfectly consecutive after OCR, but
    # most values should be non-decreasing in file order.
    nondecreasing = sum(plausible[j][1] >= plausible[j - 1][1] for j in range(1, len(plausible)))
    if len(plausible) > 1 and nondecreasing / (len(plausible) - 1) < 0.65:
        return set()
    return {i for i, _ in plausible}


def remove_trailing_page_no_before_visual(lines: list[str], idx: int, max_page: int) -> None:
    if idx <= 0 or max_page <= 0:
        return
    prev = lines[idx - 1]
    m = re.search(r"(?<!\d)(\d{1,3})\s*$", prev)
    if not m:
        return
    n = int(m.group(1))
    if not (0 < n <= max_page + 5):
        return
    # Restrict this repair to the converter-only visual label anchor.
    if len(prev.strip()) < 12 or prev.rstrip().endswith(("。", "！", "？", ".", "!", "?")):
        return
    lines[idx - 1] = prev[: m.start()].rstrip()


def repair_file(path: Path, apply: bool) -> dict:
    original = path.read_text(encoding="utf-8-sig")
    before_images = Counter(image_refs(original))
    lines = original.splitlines()
    title = title_for(path, lines)
    toc = discover_leading_toc(lines, title)
    levels = candidate_levels(toc["candidates"])
    page_no_indices = plausible_page_number_indices(lines)
    _, max_page = page_image_max(lines)

    work = lines[:]
    # Inline page number immediately before an explicit conversion-only label.
    for i, raw in enumerate(work):
        if compact(raw) in CONVERSION_LABELS:
            remove_trailing_page_no_before_visual(work, i, max_page)

    changed = False
    removed_toc_lines = 0
    page_numbers_removed = 0
    conversion_labels_removed = 0
    conversion_comments_removed = 0
    recovered_headings = 0
    glued_headings_split = 0
    duplicate_h1_removed = 0
    seen_candidate: set[str] = set()
    output: list[str] = []

    # Choose longest titles first when matching a glued body prefix.
    prefix_candidates = sorted(
        ((k, level, canonical) for k, (level, canonical) in levels.items() if len(canonical) >= 3),
        key=lambda x: len(x[2]),
        reverse=True,
    )

    for i, raw in enumerate(work):
        stripped = raw.strip()
        if i in toc["remove"] and not IMAGE.fullmatch(stripped):
            removed_toc_lines += 1
            changed = True
            continue
        if PAGE_COMMENT.match(stripped) or IMAGE_COMMENT.match(stripped):
            conversion_comments_removed += 1
            changed = True
            continue
        if i in page_no_indices:
            page_numbers_removed += 1
            changed = True
            continue
        plain = strip_md_shell(stripped)
        if compact(plain) in CONVERSION_LABELS:
            conversion_labels_removed += 1
            changed = True
            continue

        hm = HEADING.match(stripped)
        if hm and len(hm.group(1)) == 1:
            if compact(hm.group(2)) == compact(title):
                if any(HEADING.match(x.strip()) and len(HEADING.match(x.strip()).group(1)) == 1 for x in output):
                    duplicate_h1_removed += 1
                    changed = True
                    continue
            elif output:
                # The prompt requires a single H1. A later unrelated H1 is a
                # structural heading, never another book title.
                raw = "## " + hm.group(2).strip()
                stripped = raw.strip()
                plain = hm.group(2).strip()
                hm = HEADING.match(stripped)
                changed = True

        key = compact(plain)
        evidence = levels.get(key)
        if evidence and key not in seen_candidate:
            level, canonical = evidence
            new = f"{'#' * level} {canonical}"
            if stripped != new:
                changed = True
                recovered_headings += 1
            output.append(new)
            seen_candidate.add(key)
            continue

        if not hm and stripped:
            matched = None
            for key2, level, canonical in prefix_candidates:
                if key2 in seen_candidate:
                    continue
                if stripped.startswith(canonical) and len(stripped) - len(canonical) >= 24:
                    matched = (key2, level, canonical)
                    break
            if matched:
                key2, level, canonical = matched
                remainder = stripped[len(canonical):].lstrip(" ：:，,。")
                output.append(f"{'#' * level} {canonical}")
                output.append("")
                output.append(remainder)
                seen_candidate.add(key2)
                recovered_headings += 1
                glued_headings_split += 1
                changed = True
                continue
        output.append(raw.rstrip())

    # Ensure canonical book H1 exists and is the first substantive text line.
    h1_positions = [i for i, x in enumerate(output) if HEADING.match(x.strip()) and len(HEADING.match(x.strip()).group(1)) == 1]
    if not h1_positions:
        output.insert(0, f"# {title}")
        output.insert(1, "")
        changed = True
    elif compact(strip_md_shell(output[h1_positions[0]])) != compact(title):
        output[h1_positions[0]] = f"# {title}"
        changed = True

    # Normalize excessive blank lines only; do not globally reflow prose here.
    final_lines: list[str] = []
    for x in output:
        if not x.strip():
            if final_lines and final_lines[-1] != "":
                final_lines.append("")
        else:
            final_lines.append(x.rstrip())
    while final_lines and final_lines[-1] == "":
        final_lines.pop()
    final = "\n".join(final_lines).strip() + "\n"

    after_images = Counter(image_refs(final))
    if before_images != after_images:
        raise RuntimeError(f"{path}: Markdown image references changed; refusing write")
    if len(re.findall(r"^#\s+", final, re.M)) != 1:
        raise RuntimeError(f"{path}: output must contain exactly one H1")

    # The only non-duplicate body removals are TOC text, page numbers and
    # conversion labels/comments. Retention remains a broad safety guard.
    retention = visible_chars(final) / max(1, visible_chars(original))
    if retention < 0.72:
        raise RuntimeError(f"{path}: visible-content retention too low: {retention:.4f}")

    if changed and apply:
        path.write_text(final, encoding="utf-8")

    result = {
        "path": str(path),
        "title": title,
        "changed": changed,
        "applied": bool(changed and apply),
        "toc_marker_found": toc["marker"] is not None,
        "toc_leader_lines": toc["leader_lines"],
        "toc_titles_detected": len(toc["candidates"]),
        "toc_text_lines_removed": removed_toc_lines,
        "headings_recovered_from_toc": recovered_headings,
        "glued_headings_split": glued_headings_split,
        "candidate_headings_not_found": len(levels) - len(seen_candidate),
        "page_numbers_removed": page_numbers_removed,
        "conversion_labels_removed": conversion_labels_removed,
        "conversion_comments_removed": conversion_comments_removed,
        "duplicate_h1_removed": duplicate_h1_removed,
        "image_refs_preserved": sum(before_images.values()),
        "visible_retention": round(min(1.0, retention), 4),
    }
    result.update(git_meta(path))
    return result


def audit_text(path: Path, text: str, repair_info: dict | None = None) -> list[dict]:
    issues: list[dict] = []
    lines = text.splitlines()
    title = title_for(path, lines)
    hlevels = [len(m.group(1)) for x in lines if (m := HEADING.match(x.strip()))]
    h1 = sum(x == 1 for x in hlevels)
    h2plus = sum(2 <= x <= 4 for x in hlevels)
    vis = visible_chars(text)

    if h1 != 1:
        issues.append({"code": "h1_count", "severity": "high", "detail": f"H1={h1}, expected 1"})
    first_nonblank = next((strip_md_shell(x) for x in lines if x.strip() and not IMAGE.fullmatch(x.strip())), "")
    if first_nonblank and compact(first_nonblank) != compact(title):
        issues.append({"code": "book_title_not_first", "severity": "medium", "detail": first_nonblank[:100]})
    if PAGE_COMMENT.search(text):
        issues.append({"code": "page_comment_residue", "severity": "high", "detail": "<!-- page:N --> remains"})
    if IMAGE_COMMENT.search(text):
        issues.append({"code": "conversion_comment_residue", "severity": "medium", "detail": "<!-- Image (...) --> remains"})

    conversion_hits = []
    for i, x in enumerate(lines, start=1):
        if compact(x) in CONVERSION_LABELS:
            conversion_hits.append(i)
    if conversion_hits:
        issues.append({"code": "conversion_label_residue", "severity": "high", "detail": f"lines={conversion_hits[:12]}"})

    # Leading TOC residue is content evidence, independent of Git dates.
    toc = discover_leading_toc(lines, title)
    if toc["leader_lines"] > 0:
        issues.append({"code": "leading_toc_text_residue", "severity": "high", "detail": f"leader_lines={toc['leader_lines']}, titles={len(toc['candidates'])}"})
    elif toc["marker"] is not None:
        issues.append({"code": "toc_marker_needs_review", "severity": "low", "detail": "目录 marker remains but no leader-based TOC was proven"})

    # Long OCR/PDF books with only a book title are almost certainly not fully
    # semantically formatted. This is an audit flag, not an auto-edit rule.
    if vis >= 30000 and h2plus == 0:
        issues.append({"code": "large_document_without_structure", "severity": "high", "detail": f"visible_chars={vis}, headings_2_4={h2plus}"})
    elif vis >= 80000 and h2plus < 3:
        issues.append({"code": "very_low_heading_density", "severity": "medium", "detail": f"visible_chars={vis}, headings_2_4={h2plus}"})

    # Suspicious giant OCR lines are strong evidence that page text was never
    # semantically reflowed. Avoid flagging tables, URLs and image-only lines.
    giant = [i for i, x in enumerate(lines, start=1) if len(x) > 2500 and not IMAGE.search(x) and not x.lstrip().startswith("|")]
    if giant:
        issues.append({"code": "giant_ocr_lines", "severity": "medium", "detail": f"lines={giant[:12]}, count={len(giant)}"})

    # Obvious heading jumps.
    jumps = 0
    prev = None
    for level in hlevels:
        if prev is not None and level > prev + 1:
            jumps += 1
        prev = level
    if jumps:
        issues.append({"code": "heading_level_jumps", "severity": "medium", "detail": f"count={jumps}"})

    if repair_info and repair_info.get("candidate_headings_not_found", 0) > max(3, int(repair_info.get("toc_titles_detected", 0) * 0.35)):
        issues.append({"code": "toc_body_heading_coverage_low", "severity": "medium", "detail": f"missing={repair_info['candidate_headings_not_found']}/{repair_info.get('toc_titles_detected', 0)}"})

    # Surface the important false-positive condition explicitly.
    msg = (repair_info or {}).get("last_commit_message") or ""
    if issues and re.search(r"format|cleanup|repair|normalize|final", msg, re.I):
        issues.append({"code": "history_says_processed_but_content_fails", "severity": "info", "detail": msg[:180]})
    return issues


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="temp")
    p.add_argument("--report", default="temp/.content-format-audit.json")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    root = Path(args.root)
    targets = sorted(x for x in root.rglob("*.md") if x.is_file() and not x.name.startswith("."))
    repairs: list[dict] = []
    errors: list[dict] = []

    for path in targets:
        try:
            repairs.append(repair_file(path, args.apply))
        except Exception as exc:
            errors.append({"path": str(path), "stage": "repair", "error": str(exc)})
            repairs.append({"path": str(path), "changed": False, "applied": False, **git_meta(path)})

    repair_by_path = {x["path"]: x for x in repairs}
    audits: list[dict] = []
    issue_counts: dict[str, int] = defaultdict(int)
    high_files = 0
    medium_files = 0
    clean_files = 0

    for path in targets:
        text = path.read_text(encoding="utf-8-sig")
        info = repair_by_path.get(str(path), {})
        issues = audit_text(path, text, info)
        for issue in issues:
            issue_counts[issue["code"]] += 1
        severities = {x["severity"] for x in issues}
        if "high" in severities:
            status = "needs_review_high"
            high_files += 1
        elif "medium" in severities:
            status = "needs_review_medium"
            medium_files += 1
        else:
            status = "pass"
            clean_files += 1
        audits.append({
            "path": str(path),
            "status": status,
            "issues": issues,
            "metrics": {
                "bytes": len(text.encode("utf-8")),
                "visible_chars": visible_chars(text),
                "h1": len(re.findall(r"^#\s+", text, re.M)),
                "h2": len(re.findall(r"^##\s+", text, re.M)),
                "h3": len(re.findall(r"^###\s+", text, re.M)),
                "h4": len(re.findall(r"^####\s+", text, re.M)),
                "image_refs": len(image_refs(text)),
            },
            "history": {k: v for k, v in info.items() if k.startswith("last_commit_")},
        })

    payload = {
        "policy": {
            "completion_basis": "current content invariants; Git modified/commit date is weak evidence only",
            "prompt": ".prompt/Markdown文档整理与修复通用提示词.md",
            "image_rule": "exact Markdown image-reference multiset must be preserved",
        },
        "summary": {
            "markdown_files_scanned": len(targets),
            "files_changed": sum(bool(x.get("applied")) for x in repairs),
            "files_pass": clean_files,
            "files_needing_review_high": high_files,
            "files_needing_review_medium": medium_files,
            "repair_errors": len(errors),
            "toc_text_lines_removed": sum(x.get("toc_text_lines_removed", 0) for x in repairs),
            "headings_recovered_from_toc": sum(x.get("headings_recovered_from_toc", 0) for x in repairs),
            "glued_headings_split": sum(x.get("glued_headings_split", 0) for x in repairs),
            "page_numbers_removed": sum(x.get("page_numbers_removed", 0) for x in repairs),
            "conversion_labels_removed": sum(x.get("conversion_labels_removed", 0) for x in repairs),
            "image_refs_preserved_total": sum(x.get("image_refs_preserved", 0) for x in repairs),
        },
        "issue_counts": dict(sorted(issue_counts.items())),
        "repairs": repairs,
        "audit": audits,
        "errors": errors,
    }
    Path(args.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    print(json.dumps({"issue_counts": payload["issue_counts"]}, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
