#!/usr/bin/env python3
"""Validate the structural contracts of docs/通用链路宇宙."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_ROOT = REPO_ROOT / "docs" / "通用链路宇宙"
CORE_FILE = DOC_ROOT / "02_通用基础链路库.md"
INDEX_FILE = DOC_ROOT / "12_术语、边界与编号索引.md"
SCENARIO_FILE = DOC_ROOT / "13_场景验证与覆盖矩阵.md"
OVERVIEW_FILE = DOC_ROOT / "00_总览与核心结论.md"
REQUIRED_FIELDS = (
    "核心步骤",
    "解决",
    "输入",
    "输出",
    "完成标准",
    "返回",
    "可调用",
    "应用",
)


def github_slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"\s+", "-", text)


def headings(text: str) -> list[tuple[int, str]]:
    in_fence = False
    result: list[tuple[int, str]] = []
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            result.append((len(match.group(1)), match.group(2)))
    return result


def anchor_set(text: str) -> set[str]:
    counts: dict[str, int] = {}
    anchors: set[str] = set()
    for _, title in headings(text):
        base = github_slug(title)
        count = counts.get(base, 0)
        anchor = base if count == 0 else f"{base}-{count}"
        counts[base] = count + 1
        anchors.add(anchor)
    return anchors


def markdown_links(text: str) -> list[str]:
    in_fence = False
    links: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            links.extend(re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", line))
    return links


def add_error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(REPO_ROOT)}: {message}")


def validate_markdown(errors: list[str], path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    hs = headings(text)
    if sum(level == 1 for level, _ in hs) != 1:
        add_error(errors, path, "must contain exactly one H1")
    for (previous, _), (current, title) in zip(hs, hs[1:]):
        if current > previous + 1:
            add_error(errors, path, f"heading level jumps before '{title}'")

    for raw_link in markdown_links(text):
        link = raw_link.strip().strip("<>")
        if re.match(r"^(?:https?://|mailto:)", link):
            continue
        target_text, _, fragment = link.partition("#")
        target = path if not target_text else (path.parent / unquote(target_text)).resolve()
        if not target.exists():
            add_error(errors, path, f"broken relative link '{raw_link}'")
            continue
        if fragment and target.suffix.lower() == ".md":
            target_anchors = anchor_set(target.read_text(encoding="utf-8"))
            if unquote(fragment).lower() not in target_anchors:
                add_error(errors, path, f"missing anchor in link '{raw_link}'")


def validate_core_chains(errors: list[str]) -> None:
    text = CORE_FILE.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^###\s+(C\d{2})\s+(.+?)\s*$", text, re.MULTILINE))
    ids = [match.group(1) for match in matches]
    expected = [f"C{number:02d}" for number in range(1, 31)]
    if ids != expected:
        add_error(errors, CORE_FILE, f"core IDs are not exactly C01-C30: {ids}")
    if len(set(ids)) != len(ids):
        add_error(errors, CORE_FILE, "core IDs are duplicated")

    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else text.find("\n## 四、", match.end())
        if end == -1:
            end = len(text)
        block = text[match.end() : end]
        missing = [field for field in REQUIRED_FIELDS if field not in block]
        if missing:
            add_error(errors, CORE_FILE, f"{match.group(1)} missing fields: {', '.join(missing)}")

    index_text = INDEX_FILE.read_text(encoding="utf-8")
    index_ids = re.findall(r"^\|\s*(C\d{2})\s*\|", index_text, re.MULTILINE)
    if index_ids != expected:
        add_error(errors, INDEX_FILE, "number index is not exactly C01-C30 in order")


def validate_overview(errors: list[str], documents: list[Path]) -> None:
    overview = OVERVIEW_FILE.read_text(encoding="utf-8")
    linked_names = {
        unquote(link.partition("#")[0])
        for link in markdown_links(overview)
        if link.partition("#")[0].endswith(".md")
    }
    for path in documents:
        if path == OVERVIEW_FILE:
            continue
        if path.name not in linked_names:
            add_error(errors, OVERVIEW_FILE, f"navigation does not link '{path.name}'")
        local_links = {
            unquote(link.partition("#")[0])
            for link in markdown_links(path.read_text(encoding="utf-8"))
        }
        if OVERVIEW_FILE.name not in local_links:
            add_error(errors, path, "does not provide a return link to the overview")


def validate_scenarios(errors: list[str]) -> None:
    text = SCENARIO_FILE.read_text(encoding="utf-8")
    expected = (
        "个人一周计划与健康维护",
        "普通工作任务从接收到验收",
        "软件需求从用户问题到上线运营",
        "AI 重度软件 OPC 从机会到现金回收",
        "项目经验转成公司流程并被采用",
        "生产故障的止损、恢复和防复发",
        "产品或流程的暂停、交接、淘汰和重启",
    )
    for scenario in expected:
        if scenario not in text:
            add_error(errors, SCENARIO_FILE, f"missing benchmark scenario '{scenario}'")


def main() -> int:
    errors: list[str] = []
    documents = sorted(DOC_ROOT.rglob("*.md"))
    if not documents:
        print(f"ERROR: no Markdown files found under {DOC_ROOT}")
        return 1

    for path in [REPO_ROOT / "README.md", *documents]:
        validate_markdown(errors, path)
    validate_core_chains(errors)
    validate_overview(errors, documents)
    validate_scenarios(errors)

    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS: "
        f"{len(documents)} docs; one H1 each; no heading jumps; "
        "relative links and anchors valid; C01-C30 unique and complete; "
        "bidirectional overview navigation and seven benchmark scenarios present."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
