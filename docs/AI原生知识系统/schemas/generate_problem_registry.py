#!/usr/bin/env python3
"""Generate the machine-auditable canonical P-L2 problem registry.

Source-of-truth discipline:
- Human semantics come from ../01_需求宇宙.md.
- SUP primary/related mappings come from ../01B_标准用户问题与专业问题映射.md.
- Synthetic case references come from ../22_遗漏、反例与回归测试.md.
- This script materializes a derived JSONL asset; generated JSONL is never the human-editing fact source.

Usage:
  python schemas/generate_problem_registry.py
  python schemas/generate_problem_registry.py --check
  python schemas/generate_problem_registry.py --output schemas/problem-registry.generated.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
PROBLEM_MD = ROOT / "01_需求宇宙.md"
SUP_MD = ROOT / "01B_标准用户问题与专业问题映射.md"
TEST_MD = ROOT / "22_遗漏、反例与回归测试.md"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "problem-registry.generated.jsonl"

PROBLEM_ID_RE = re.compile(r"P-L2-(\d{2})-(\d{2})")
SHORT_ID_RE = re.compile(r"(?<![0-9])((?:0[1-9]|1[0-7])-[0-9]{2})(?![0-9])")
P_L1_RE = re.compile(r"P-L1-(\d{2})")
JOURNEY_RE = re.compile(r"J(?:0[1-9]|1[0-8])")
SUP_RE = re.compile(r"SUP-[0-9]{3}")
SYN_RE = re.compile(r"SYN-[A-Z]+[0-9]{2}")

SCALE_TAGS = {
    "单书",
    "单本书",
    "多书",
    "百本",
    "海量",
    "海量知识",
    "领域",
    "长期",
    "长期积累",
    "长期研究",
}


def clean_cell(value: str) -> str:
    value = value.strip()
    value = value.replace("`", "")
    value = value.replace("<br>", "；").replace("<br/>", "；")
    return value.strip()


def split_md_row(line: str) -> list[str]:
    """Split the simple Markdown tables used by the formal files.

    The current problem tables intentionally avoid literal pipes inside cells.
    If that convention changes, this parser should be upgraded before generation.
    """
    line = line.strip()
    if not (line.startswith("|") and line.endswith("|")):
        return []
    return [clean_cell(x) for x in line[1:-1].split("|")]


def short_to_problem_id(short_id: str) -> str:
    return f"P-L2-{short_id}"


def canonical_ids_in_text(text: str) -> set[str]:
    ids = set(PROBLEM_ID_RE.findall(text))
    out = {f"P-L2-{a}-{b}" for a, b in ids}
    for short in SHORT_ID_RE.findall(text):
        out.add(short_to_problem_id(short))
    return out


def parse_problem_rows(text: str) -> tuple[list[dict], dict[str, str]]:
    lines = text.splitlines()
    records: list[dict] = []
    aliases: dict[str, str] = {}
    current_p_l1: str | None = None
    in_human_table = False
    in_alias_table = False
    previous_semantics: dict[str, dict[str, str]] = defaultdict(dict)

    for i, line in enumerate(lines):
        heading = re.match(r"^###\s+P-L1-(\d{2})\b", line)
        if heading:
            current_p_l1 = f"P-L1-{heading.group(1)}"
            in_human_table = False

        if line.startswith("## 五、旧 P-L2"):
            in_alias_table = True
            in_human_table = False
        elif in_alias_table and line.startswith("## ") and not line.startswith("## 五、"):
            in_alias_table = False

        cells = split_md_row(line)
        if not cells:
            continue

        if cells and cells[0] == "人话问题":
            in_human_table = True
            continue
        if cells and all(set(c) <= {"-", ":"} for c in cells if c):
            continue

        if in_human_table and current_p_l1 and len(cells) >= 10:
            raw_id = cells[9]
            match = PROBLEM_ID_RE.search(raw_id)
            if not match:
                continue
            problem_id = f"P-L2-{match.group(1)}-{match.group(2)}"
            primary_p_l1 = f"P-L1-{match.group(1)}"
            if primary_p_l1 != current_p_l1:
                raise ValueError(f"P-L1 heading mismatch for {problem_id}: {current_p_l1}")

            human, example, consequence, need, outcome, related, stages, tags, audit, _ = cells[:10]

            inherited = previous_semantics[current_p_l1]
            if consequence == "同上":
                consequence = inherited.get("user_consequence", "")
            if need == "同上":
                need = inherited.get("user_need", "")
            if outcome == "同上":
                outcome = inherited.get("desired_outcome", "")

            if consequence:
                inherited["user_consequence"] = consequence
            if need:
                inherited["user_need"] = need
            if outcome:
                inherited["desired_outcome"] = outcome

            related_l1 = sorted({f"P-L1-{x}" for x in re.findall(r"(?<!\d)(0[1-9]|1[0-7])(?!\d)", related)})
            related_l1 = [x for x in related_l1 if x != primary_p_l1]

            journey_stages = sorted(set(JOURNEY_RE.findall(stages)))
            raw_tags = [x.strip() for x in re.split(r"[；;,，]", tags) if x.strip()]
            scale_tags = sorted({x for x in raw_tags if x in SCALE_TAGS})
            scenario_tags = [x for x in raw_tags if x not in SCALE_TAGS]

            if "PARTIAL" in audit:
                audit_status = "PARTIAL"
            elif "REWRITE" in audit:
                audit_status = "REWRITE"
            else:
                audit_status = "KEEP"

            records.append(
                {
                    "schema_version": "0.1",
                    "problem_id": problem_id,
                    "canonical_human_problem": human,
                    "user_consequence": consequence,
                    "user_need": need,
                    "desired_outcome": outcome,
                    "primary_p_l1": primary_p_l1,
                    "related_p_l1": related_l1,
                    "journey_stages": journey_stages,
                    "scenario_tags": scenario_tags,
                    "scale_tags": scale_tags,
                    "primary_sup": [],
                    "related_sup": [],
                    "confusable_neighbors": [],
                    "boundary_rule": None,
                    "problem_relations": [],
                    "synthetic_cases": [],
                    "audit_status": audit_status,
                    "legacy_aliases": [],
                    "source_file": "../01_需求宇宙.md",
                    "generated_at": None,
                }
            )

        if in_alias_table and len(cells) >= 2:
            old_match = PROBLEM_ID_RE.search(cells[0])
            new_match = PROBLEM_ID_RE.search(cells[1])
            if old_match and new_match:
                old_id = f"P-L2-{old_match.group(1)}-{old_match.group(2)}"
                new_id = f"P-L2-{new_match.group(1)}-{new_match.group(2)}"
                if old_id == new_id:
                    raise ValueError(f"Self alias is invalid: {old_id}")
                aliases[old_id] = new_id

    return records, aliases


def parse_sup_reverse_mapping(text: str) -> tuple[dict[str, set[str]], dict[str, set[str]], int]:
    primary: dict[str, set[str]] = defaultdict(set)
    related: dict[str, set[str]] = defaultdict(set)
    sup_rows = 0

    for line in text.splitlines():
        cells = split_md_row(line)
        if len(cells) < 5 or not SUP_RE.fullmatch(cells[0]):
            continue
        sup_rows += 1
        sup_id = cells[0]
        primary_ids = canonical_ids_in_text(cells[2])
        related_ids = canonical_ids_in_text(cells[3])
        for pid in primary_ids:
            primary[pid].add(sup_id)
        for pid in related_ids - primary_ids:
            related[pid].add(sup_id)

    return primary, related, sup_rows


def parse_synthetic_reverse_mapping(text: str) -> dict[str, set[str]]:
    reverse: dict[str, set[str]] = defaultdict(set)
    current_case: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        if not current_case:
            buffer = []
            return
        block = "\n".join(buffer)
        for pid in canonical_ids_in_text(block):
            reverse[pid].add(current_case)
        buffer = []

    for line in text.splitlines():
        heading = re.match(r"^###\s+(SYN-[A-Z]+[0-9]{2})\b", line)
        if heading:
            flush()
            current_case = heading.group(1)
            buffer = [line]
        elif current_case:
            buffer.append(line)
    flush()
    return reverse


def enrich(records: list[dict], aliases: dict[str, str], sup_text: str, test_text: str) -> list[dict]:
    by_id = {r["problem_id"]: r for r in records}
    primary_sup, related_sup, sup_rows = parse_sup_reverse_mapping(sup_text)
    synthetic = parse_synthetic_reverse_mapping(test_text)

    if sup_rows != 94:
        raise ValueError(f"Expected 94 SUP rows, found {sup_rows}")

    for old_id, canonical_id in aliases.items():
        if canonical_id not in by_id:
            raise ValueError(f"Alias target is not canonical: {old_id} -> {canonical_id}")
        by_id[canonical_id]["legacy_aliases"].append(old_id)

    for pid, record in by_id.items():
        record["primary_sup"] = sorted(primary_sup.get(pid, set()))
        record["related_sup"] = sorted(related_sup.get(pid, set()) - set(record["primary_sup"]))
        record["synthetic_cases"] = sorted(synthetic.get(pid, set()))
        record["legacy_aliases"] = sorted(record["legacy_aliases"])

    return sorted(records, key=lambda r: r["problem_id"])


def validate(records: list[dict], aliases: dict[str, str]) -> None:
    ids = [r["problem_id"] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate canonical problem_id detected")
    if len(records) != 151:
        raise ValueError(f"Expected 151 canonical P-L2 records, found {len(records)}")
    if len(aliases) != 32:
        raise ValueError(f"Expected 32 legacy alias/degraded entries, found {len(aliases)}")
    overlap = set(ids) & set(aliases)
    if overlap:
        raise ValueError(f"Legacy aliases still present as canonical records: {sorted(overlap)}")

    for record in records:
        pid = record["problem_id"]
        match = PROBLEM_ID_RE.fullmatch(pid)
        if not match:
            raise ValueError(f"Invalid problem_id: {pid}")
        expected_l1 = f"P-L1-{match.group(1)}"
        if record["primary_p_l1"] != expected_l1:
            raise ValueError(f"primary_p_l1 mismatch: {pid}")
        for field in ("canonical_human_problem", "user_consequence", "user_need", "desired_outcome"):
            if not str(record[field]).strip():
                raise ValueError(f"Missing {field} in {pid}")


def materialize(output: Path) -> tuple[list[dict], dict[str, str]]:
    problem_text = PROBLEM_MD.read_text(encoding="utf-8")
    sup_text = SUP_MD.read_text(encoding="utf-8")
    test_text = TEST_MD.read_text(encoding="utf-8")

    records, aliases = parse_problem_rows(problem_text)
    records = enrich(records, aliases, sup_text, test_text)
    validate(records, aliases)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return records, aliases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the formal Markdown sources and derived registry contract without keeping output.",
    )
    args = parser.parse_args()

    if args.check:
        problem_text = PROBLEM_MD.read_text(encoding="utf-8")
        sup_text = SUP_MD.read_text(encoding="utf-8")
        test_text = TEST_MD.read_text(encoding="utf-8")
        records, aliases = parse_problem_rows(problem_text)
        records = enrich(records, aliases, sup_text, test_text)
        validate(records, aliases)
        print(f"OK: {len(records)} canonical P-L2; {len(aliases)} legacy aliases/degraded entries; 94 SUP rows")
        return 0

    records, aliases = materialize(args.output)
    print(f"Wrote {args.output}: {len(records)} canonical P-L2; {len(aliases)} aliases/degraded entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
