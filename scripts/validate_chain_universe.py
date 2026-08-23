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
PROJECT_SCENE_FILE = DOC_ROOT / "15_项目与复杂任务链路宇宙.md"
KNOWLEDGE_SCENE_FILE = DOC_ROOT / "16_阅读学习与知识研究链路宇宙.md"
SCENE_ENTRY_FILE = DOC_ROOT / "17_现实场景分类与入口地图.md"
SCENE_EXPLANATION_FILE = DOC_ROOT / "18_场景分类说明与组合示例.md"
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
        "复杂项目从模糊目标到交付",
        "文章／单书从筛选到掌握迁移",
        "大量资料去重并形成知识差额",
    )
    for scenario in expected:
        if scenario not in text:
            add_error(errors, SCENARIO_FILE, f"missing benchmark scenario '{scenario}'")


def validate_scene_universes(errors: list[str]) -> None:
    requirements = {
        PROJECT_SCENE_FILE: (
            "目标建立组合链",
            "目标拆解链",
            "问题拆解链",
            "已有解法搜索链",
            "多方案生成链",
            "失败预演与反例链",
            "方案评估链",
            "执行控制链",
            "按根因返回最近的有效层",
        ),
        KNOWLEDGE_SCENE_FILE: (
            "文章进入链",
            "单本书 T0—T7 阶段链",
            "多资料去重与知识增量链",
            "资料状态与掌握状态分开",
            "语义相似只适合召回候选",
            "知识差额",
        ),
    }
    for path, phrases in requirements.items():
        if not path.exists():
            add_error(errors, path, "required L3 scene universe is missing")
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                add_error(errors, path, f"missing required scene concept '{phrase}'")


def validate_real_world_scene_map(errors: list[str]) -> None:
    if not SCENE_ENTRY_FILE.exists():
        add_error(errors, SCENE_ENTRY_FILE, "real-world scene entry map is missing")
        return
    if not SCENE_EXPLANATION_FILE.exists():
        add_error(errors, SCENE_EXPLANATION_FILE, "scene explanation file is missing")
        return

    entry_text = SCENE_ENTRY_FILE.read_text(encoding="utf-8")
    expected_scene_ids = [f"S{number:02d}" for number in range(1, 16)]
    scene_ids = re.findall(r"^\|\s*(S\d{2})\s*\|", entry_text, re.MULTILINE)
    if scene_ids != expected_scene_ids:
        add_error(errors, SCENE_ENTRY_FILE, f"scene IDs are not exactly S01-S15 in order: {scene_ids}")
    if len(set(scene_ids)) != len(scene_ids):
        add_error(errors, SCENE_ENTRY_FILE, "scene IDs are duplicated")

    expected_domain_ids = [f"D{number:02d}" for number in range(1, 9)]
    domain_ids = re.findall(r"^\|\s*(D\d{2})\s*\|", entry_text, re.MULTILINE)
    if domain_ids != expected_domain_ids:
        add_error(errors, SCENE_ENTRY_FILE, f"domain IDs are not exactly D01-D08 in order: {domain_ids}")

    required_entry_phrases = (
        "现实场景 = 主场景类型 × 发生领域 × 主体规模 × 复杂度／风险 × 生命周期阶段",
        "场景代码 `S01—S15` 只是导航编号",
        "一个现实事件可以同时具有多个场景标签，但只选一个主入口",
        "AI／Agent 通常是技术模式或工具维度，而不是新的现实领域",
        "第三维：主体规模",
        "第四维：复杂度与风险",
        "第五维：生命周期阶段",
    )
    for phrase in required_entry_phrases:
        if phrase not in entry_text:
            add_error(errors, SCENE_ENTRY_FILE, f"missing scene taxonomy rule '{phrase}'")

    explanation_text = SCENE_EXPLANATION_FILE.read_text(encoding="utf-8")
    required_explanation_phrases = (
        "本文件只负责解释，不承担稳定分类结论",
        "S07 信息／研究 vs S08 学习／能力",
        "S09 任务／执行 vs S10 项目／复杂任务",
        "S12 监测／反馈／偏差／改进 vs S13 风险／异常／恢复",
        "S14 验证／验收／价值评估 vs S15 生命周期",
        "场景分类不是互斥标签体系",
        "什么时候才值得建立新的独立场景宇宙",
    )
    for phrase in required_explanation_phrases:
        if phrase not in explanation_text:
            add_error(errors, SCENE_EXPLANATION_FILE, f"missing scene explanation boundary '{phrase}'")


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
    validate_scene_universes(errors)
    validate_real_world_scene_map(errors)

    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS: "
        f"{len(documents)} docs; one H1 each; no heading jumps; "
        "relative links and anchors valid; C01-C30 unique and complete; "
        "ten benchmark scenarios; project/complex-task and reading/knowledge L3 universes; "
        "S01-S15 real-world scene entry map, five-dimensional scene coordinates, "
        "and separated scene explanation file present."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
