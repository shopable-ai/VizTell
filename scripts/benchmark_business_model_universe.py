#!/usr/bin/env python3
"""Deterministic integrity + routing/retrieval harness for 商业模式宇宙.

This is NOT an A-E answer-quality judge. It verifies ontology preservation,
task routing, minimum-context assembly and a deterministic V0 retrieval baseline.
V0 uses task/flag retrieval concepts and benchmark-only semantic anchors so a
high routing score cannot hide an obviously bad Atom/Pattern retriever.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

BM_ROOT = Path("docs/商业模式宇宙")
ROUTER_PATH = Path("08_机器数据与Schema/task_router_v1.json")
BENCH_PATH = Path("08_机器数据与Schema/benchmark_manifest_v1.json")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL {path}:{line_no}: {exc}") from exc
            if not isinstance(obj, dict):
                raise ValueError(f"Expected object in {path}:{line_no}")
            rows.append(obj)
    return rows


def atoms_from_registry(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for key, value in obj.items():
        if not isinstance(value, dict):
            continue
        atoms = value.get("atoms")
        if not isinstance(atoms, list):
            continue
        category_name = value.get("category_name")
        for atom in atoms:
            if isinstance(atom, dict):
                item = dict(atom)
                item.setdefault("category_id", key)
                if category_name:
                    item.setdefault("category_name", category_name)
                rows.append(item)
    return rows


def roles_from_registry(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for family in obj.get("role_families", []):
        if not isinstance(family, dict):
            continue
        for role in family.get("roles", []):
            if isinstance(role, dict):
                item = dict(role)
                item.setdefault("family_id", family.get("id"))
                rows.append(item)
    return rows


def ensure_unique_ids(records: Sequence[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    seen = set()
    dup = []
    for record in records:
        rid = record.get("id")
        if not rid:
            dup.append("<missing-id>")
            continue
        if rid in seen:
            dup.append(str(rid))
        seen.add(rid)
    return (not dup, sorted(set(dup)))


def normalize(text: str) -> str:
    return re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "", text.lower())


def ngrams(text: str, n: int = 2) -> set[str]:
    text = normalize(text)
    if not text:
        return set()
    if len(text) < n:
        return {text}
    return {text[i : i + n] for i in range(len(text) - n + 1)}


def lexical_similarity(query: str, candidate: str) -> float:
    """Deterministic similarity with two-way substring + char-bigram coverage."""
    qn = normalize(query)
    cn = normalize(candidate)
    if not qn or not cn:
        return 0.0
    direct = 0.0
    if cn in qn:
        direct = 1.0
    elif qn in cn:
        direct = min(1.0, len(qn) / max(1.0, len(cn)))
    qg = ngrams(qn)
    cg = ngrams(cn)
    candidate_coverage = len(qg & cg) / max(1, len(cg))
    query_coverage = len(qg & cg) / max(1, len(qg))
    return direct * 2.0 + candidate_coverage + query_coverage * 0.25


def retrieval_score(query: str, concepts: Sequence[str], candidate: str) -> float:
    base = lexical_similarity(query, candidate)
    concept_scores = sorted(
        (lexical_similarity(str(concept), candidate) for concept in concepts if str(concept).strip()),
        reverse=True,
    )
    best = concept_scores[0] if concept_scores else 0.0
    supporting = sum(concept_scores[1:4]) if len(concept_scores) > 1 else 0.0
    return base + best * 2.0 + supporting * 0.35


def trigger_score(query: str, triggers: Sequence[str]) -> float:
    text = query.lower()
    score = 0.0
    for trigger in triggers:
        term = str(trigger).lower().strip()
        if term and term in text:
            score += 2.0 + min(3.0, len(normalize(term)) / 3.0)
    return score


def unique_text(items: Sequence[str]) -> List[str]:
    out: List[str] = []
    seen = set()
    for item in items:
        text = str(item).strip()
        key = text.lower()
        if text and key not in seen:
            out.append(text)
            seen.add(key)
    return out


def route_task(query: str, router: Dict[str, Any]) -> Dict[str, Any]:
    family_scores: List[Tuple[float, str, Dict[str, Any]]] = []
    for family in router.get("families", []):
        score = trigger_score(query, family.get("triggers", []))
        family_scores.append((score, str(family.get("id")), family))
    family_scores.sort(key=lambda x: (-x[0], x[1]))
    if not family_scores:
        raise ValueError("Router has no task families")

    best_score, best_id, best_family = family_scores[0]
    if best_score <= 0:
        best_family = next(
            (f for f in router.get("families", []) if f.get("id") == "design_new_business_model"),
            best_family,
        )
        best_id = str(best_family.get("id"))

    flags: List[Dict[str, Any]] = []
    flag_scores: Dict[str, float] = {}
    for flag in router.get("flags", []):
        score = trigger_score(query, flag.get("triggers", []))
        if score > 0:
            flags.append(flag)
            flag_scores[str(flag.get("id"))] = score

    domains: List[str] = []
    assets: List[str] = []
    concepts: List[str] = list(best_family.get("retrieval_concepts", []))
    for domain in best_family.get("primary_domains", []):
        if domain not in domains:
            domains.append(domain)
    for asset in best_family.get("knowledge_assets", []):
        if asset not in assets:
            assets.append(asset)
    for flag in flags:
        concepts.extend(flag.get("retrieval_concepts", []))
        for domain in flag.get("domains_add", []):
            if domain not in domains:
                domains.append(domain)
        for asset in flag.get("assets_add", []):
            if asset not in assets:
                assets.append(asset)

    concepts = unique_text(concepts)
    return {
        "family": best_id,
        "family_score": best_score,
        "alternate_routes": [
            {"family": family_id, "score": score}
            for score, family_id, _ in family_scores[1:4]
            if score > 0
        ],
        "flags": [str(f.get("id")) for f in flags],
        "flag_scores": flag_scores,
        "domains": domains,
        "assets": assets,
        "retrieval_concepts": concepts,
    }


def retrieve_top(
    query: str,
    concepts: Sequence[str],
    records: Sequence[Dict[str, Any]],
    allowed_domains: set[str] | None,
    k: int,
    text_fields: Sequence[str],
) -> List[Dict[str, Any]]:
    scored = []
    for item in records:
        domain = item.get("category_id")
        if allowed_domains is not None and domain and domain not in allowed_domains:
            continue
        text = " ".join(str(item.get(field, "")) for field in text_fields)
        score = retrieval_score(query, concepts, text)
        scored.append((score, str(item.get("id", "")), item))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [dict(item, _retrieval_score=round(score, 6)) for score, _, item in scored[:k]]


def pct(hit: int, total: int) -> float:
    return 100.0 if total == 0 else round(hit * 100.0 / total, 2)


def ratio(hit: int, total: int) -> float:
    return 1.0 if total == 0 else round(hit / total, 6)


def mean_top_score(records: Sequence[Dict[str, Any]], n: int = 3) -> float:
    values = [float(x.get("_retrieval_score", 0.0)) for x in records[:n]]
    return round(sum(values) / len(values), 6) if values else 0.0


def preservation_report(root: Path, router: Dict[str, Any]) -> Dict[str, Any]:
    machine = root / "08_机器数据与Schema"
    base_atoms = load_jsonl(machine / "atoms.jsonl")
    v3_atoms = atoms_from_registry(load_json(machine / "atoms_v3_registry.json"))
    v4_atoms = atoms_from_registry(load_json(machine / "atoms_v4_registry.json"))
    base_patterns = load_jsonl(machine / "patterns.jsonl")
    v3_patterns = load_jsonl(machine / "patterns_v3_extension_P131-P170.jsonl")
    v4_patterns = load_jsonl(machine / "patterns_v4_extension_P171-P200.jsonl")
    roles = roles_from_registry(load_json(machine / "product_roles_v4.json"))

    all_atoms = base_atoms + v3_atoms + v4_atoms
    all_patterns = base_patterns + v3_patterns + v4_patterns
    atom_unique, atom_dups = ensure_unique_ids(all_atoms)
    pattern_unique, pattern_dups = ensure_unique_ids(all_patterns)
    role_unique, role_dups = ensure_unique_ids(roles)

    checks = {
        "base_atoms_500": len(base_atoms) == 500,
        "v3_atoms_149": len(v3_atoms) == 149,
        "v4_atoms_27": len(v4_atoms) == 27,
        "total_atoms_676": len(all_atoms) == 676,
        "base_patterns_130": len(base_patterns) == 130,
        "v3_patterns_40": len(v3_patterns) == 40,
        "v4_patterns_30": len(v4_patterns) == 30,
        "total_patterns_200": len(all_patterns) == 200,
        "product_roles_40": len(roles) == 40,
        "atom_ids_unique": atom_unique,
        "pattern_ids_unique": pattern_unique,
        "role_ids_unique": role_unique,
        "u19_preserved": any(a.get("category_id") == "U19" for a in all_atoms),
        "no_u28_plus": not any(
            re.match(r"U(2[8-9]|[3-9][0-9]+)-", str(a.get("id", ""))) for a in all_atoms
        ),
        "p001_present": any(p.get("id") == "P001" for p in all_patterns),
        "p200_present": any(p.get("id") == "P200" for p in all_patterns),
        "pr01_present": any(r.get("id") == "PR01" for r in roles),
        "pr40_present": any(r.get("id") == "PR40" for r in roles),
    }

    router_assets: List[str] = []
    for family in router.get("families", []):
        router_assets.extend(family.get("knowledge_assets", []))
    for flag in router.get("flags", []):
        router_assets.extend(flag.get("assets_add", []))
    missing_router_assets = sorted({a for a in router_assets if not (root / a).exists()})
    checks["router_assets_exist"] = not missing_router_assets

    return {
        "pass": all(checks.values()),
        "checks": checks,
        "counts": {
            "base_atoms": len(base_atoms), "v3_atoms": len(v3_atoms), "v4_atoms": len(v4_atoms),
            "total_atoms": len(all_atoms), "base_patterns": len(base_patterns),
            "v3_patterns": len(v3_patterns), "v4_patterns": len(v4_patterns),
            "total_patterns": len(all_patterns), "product_roles": len(roles)
        },
        "duplicates": {"atoms": atom_dups, "patterns": pattern_dups, "roles": role_dups},
        "missing_router_assets": missing_router_assets,
        "atoms": all_atoms,
        "patterns": all_patterns,
    }


def ablation_asset_groups(assets: Sequence[str]) -> Dict[str, set[str]]:
    assets_set = set(assets)
    groups = {
        "product_roles_offer": {a for a in assets_set if "商品角色" in a or "Offer" in a or "Skill机器加载" in a},
        "opportunity_lens": {a for a in assets_set if "机会来源" in a},
        "value_chain_ecosystem": {a for a in assets_set if a.startswith("02_") or a.startswith("03_")},
        "conditional_real_economics": {a for a in assets_set if a.startswith("06_")},
        "topic_case": {a for a in assets_set if a.startswith("09_") or a.startswith("04_")},
        "failure_counterargument": {a for a in assets_set if a.startswith("05_")},
    }
    return {key: value for key, value in groups.items() if value}


def benchmark_case(
    case: Dict[str, Any], router: Dict[str, Any], root: Path,
    atoms: Sequence[Dict[str, Any]], patterns: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
    query = str(case.get("query", ""))
    route = route_task(query, router)
    required_assets = list(case.get("required_assets", []))
    required_domains = list(case.get("required_domains", []))
    expected_flags = list(case.get("expected_flags", []))

    missing_assets_on_disk = [a for a in required_assets if not (root / a).exists()]
    asset_hits = [a for a in required_assets if a in route["assets"]]
    domain_hits = [d for d in required_domains if d in route["domains"]]
    flag_hits = [f for f in expected_flags if f in route["flags"]]
    asset_recall = pct(len(asset_hits), len(required_assets))
    domain_recall = pct(len(domain_hits), len(required_domains))
    flag_recall = pct(len(flag_hits), len(expected_flags))
    route_correct = route["family"] == case.get("expected_family")

    cfg = router.get("retrieval", {})
    max_assets = int(cfg.get("default_max_knowledge_assets", 12))
    budget_ok = len(route["assets"]) <= max_assets
    top_atoms = retrieve_top(
        query, route["retrieval_concepts"], atoms, set(route["domains"]),
        int(cfg.get("default_top_atoms", 24)), ("name", "essence", "definition", "category_name"),
    )
    top_patterns = retrieve_top(
        query, route["retrieval_concepts"], patterns, None,
        int(cfg.get("default_top_patterns", 12)), ("name", "formula", "definition", "description"),
    )

    anchors = case.get("retrieval_anchors", {})
    expected_atom_ids = list(anchors.get("atom_ids", []))
    expected_pattern_ids = list(anchors.get("pattern_ids", []))
    got_atom_ids = {str(x.get("id")) for x in top_atoms}
    got_pattern_ids = {str(x.get("id")) for x in top_patterns}
    atom_anchor_hits = [x for x in expected_atom_ids if x in got_atom_ids]
    pattern_anchor_hits = [x for x in expected_pattern_ids if x in got_pattern_ids]
    atom_anchor_recall = ratio(len(atom_anchor_hits), len(expected_atom_ids))
    pattern_anchor_recall = ratio(len(pattern_anchor_hits), len(expected_pattern_ids))

    atom_top3_mean = mean_top_score(top_atoms)
    pattern_top3_mean = mean_top_score(top_patterns)
    signal_threshold = float(cfg.get("v0_min_top3_mean_score", 0.08))
    anchor_threshold = float(cfg.get("v0_required_anchor_recall", 1.0))
    signal_pass = atom_top3_mean >= signal_threshold and pattern_top3_mean >= signal_threshold
    anchor_pass = atom_anchor_recall >= anchor_threshold and pattern_anchor_recall >= anchor_threshold

    score = round(min(100.0,
        (35.0 if route_correct else 0.0) + asset_recall * 0.30 + domain_recall * 0.20
        + flag_recall * 0.10 + (5.0 if budget_ok else 0.0)
    ), 2)

    ablations = {}
    for group, removed in ablation_asset_groups(route["assets"]).items():
        remaining = [a for a in route["assets"] if a not in removed]
        remaining_hits = [a for a in required_assets if a in remaining]
        new_recall = pct(len(remaining_hits), len(required_assets))
        ablations[group] = {
            "removed_assets": sorted(removed),
            "required_asset_recall_after": new_recall,
            "coverage_drop_points": round(asset_recall - new_recall, 2),
        }

    return {
        "case_id": case.get("id"), "name": case.get("name"), "query": query,
        "route": {
            "family": route["family"], "expected_family": case.get("expected_family"),
            "correct": route_correct, "flags": route["flags"], "expected_flags": expected_flags,
            "alternate_routes": route["alternate_routes"],
        },
        "coverage": {
            "required_asset_recall": asset_recall, "required_domain_recall": domain_recall,
            "expected_flag_recall": flag_recall, "missing_assets_on_disk": missing_assets_on_disk,
            "missing_assets_in_context": sorted(set(required_assets) - set(asset_hits)),
            "missing_domains": sorted(set(required_domains) - set(domain_hits)),
            "knowledge_asset_count": len(route["assets"]), "knowledge_asset_budget": max_assets,
            "budget_ok": budget_ok,
        },
        "retrieval_preview": {
            "strategy": "task/flag concept weighted deterministic V0",
            "retrieval_concepts": route["retrieval_concepts"],
            "top_atoms": [{"id": a.get("id"), "name": a.get("name"), "score": a.get("_retrieval_score")} for a in top_atoms[:10]],
            "top_patterns": [{"id": p.get("id"), "name": p.get("name"), "score": p.get("_retrieval_score")} for p in top_patterns[:10]],
        },
        "retrieval_quality": {
            "v0_min_top3_mean_score": signal_threshold,
            "atom_top3_mean_score": atom_top3_mean,
            "pattern_top3_mean_score": pattern_top3_mean,
            "signal_pass": signal_pass,
            "required_anchor_recall": anchor_threshold,
            "atom_anchor_ids": expected_atom_ids,
            "atom_anchor_hits": atom_anchor_hits,
            "atom_anchor_recall": atom_anchor_recall,
            "pattern_anchor_ids": expected_pattern_ids,
            "pattern_anchor_hits": pattern_anchor_hits,
            "pattern_anchor_recall": pattern_anchor_recall,
            "anchor_pass": anchor_pass,
            "semantics": "V0 retrieval regression guard; benchmark anchors never modify the retrieval query",
        },
        "retrieval_ablation": ablations,
        "runtime_harness_score": score,
        "score_semantics": "routing/context harness only; NOT A-E business answer quality",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--strict", action="store_true", help="exit non-zero on regression")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    args = parser.parse_args()

    root = Path(args.root).resolve() / BM_ROOT
    router = load_json(root / ROUTER_PATH)
    bench = load_json(root / BENCH_PATH)
    preservation = preservation_report(root, router)
    atoms = preservation.pop("atoms")
    patterns = preservation.pop("patterns")
    cases = [benchmark_case(c, router, root, atoms, patterns) for c in bench.get("active_cases", [])]

    min_score = float(bench.get("regression_policy", {}).get("minimum_runtime_harness_score", 90))
    failures: List[str] = []
    if not preservation["pass"]:
        failures.append("preservation")
    for case in cases:
        cov = case["coverage"]
        rq = case["retrieval_quality"]
        if case["runtime_harness_score"] < min_score: failures.append(f"{case['case_id']}:score")
        if cov["required_asset_recall"] < 100: failures.append(f"{case['case_id']}:asset_recall")
        if cov["required_domain_recall"] < 100: failures.append(f"{case['case_id']}:domain_recall")
        if cov["expected_flag_recall"] < 100: failures.append(f"{case['case_id']}:flag_recall")
        if not cov["budget_ok"]: failures.append(f"{case['case_id']}:context_budget")
        if cov["missing_assets_on_disk"]: failures.append(f"{case['case_id']}:missing_files")
        if not rq["signal_pass"]: failures.append(f"{case['case_id']}:retrieval_signal")
        if not rq["anchor_pass"]: failures.append(f"{case['case_id']}:retrieval_anchor")

    report = {
        "harness": "business-model-universe-runtime-v1",
        "ontology_base": "v4",
        "note": "Validates structure + routing + minimum-context + V0 retrieval anchors; does not estimate A-E business-answer uplift.",
        "preservation": preservation,
        "cases": cases,
        "regression": {"minimum_runtime_harness_score": min_score, "pass": not failures, "failures": sorted(set(failures))},
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 1 if args.strict and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
