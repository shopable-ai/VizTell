#!/usr/bin/env python3
"""Fix PAGE multiline detection and execute the raw OCR/PDF formatting pass.

This helper also patches repair_temp_markdown_structure.py in-place so future
repository-wide runs keep the correction.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path


def patch_main_script(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    old = 'PAGE = re.compile(r"^\\s*<!--\\s*page\\s*:\\s*\\d+\\s*-->\\s*$", re.I)'
    new = 'PAGE = re.compile(r"^\\s*<!--\\s*page\\s*:\\s*\\d+\\s*-->\\s*$", re.I | re.M)'
    if old not in text:
        return False
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("repair_temp_markdown_structure", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load repair module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="temp")
    ap.add_argument("--report", default="temp/.raw-format-report.json")
    args = ap.parse_args()

    main_script = Path(__file__).with_name("repair_temp_markdown_structure.py")
    patched = patch_main_script(main_script)
    mod = load_module(main_script)
    root = Path(args.root)

    formatted = []
    errors = []
    scanned = 0
    for path in sorted(p for p in root.rglob("*.md") if p.is_file() and not p.name.startswith(".")):
        text = path.read_text(encoding="utf-8-sig")
        if not mod.PAGE.search(text):
            continue
        scanned += 1
        try:
            formatted.append(mod.format_raw_document(path))
        except Exception as exc:
            errors.append({"path": str(path), "error": str(exc)})

    payload = {
        "main_script_multiline_fix_applied": patched,
        "raw_documents_detected": scanned,
        "formatted": formatted,
        "errors": errors,
        "summary": {
            "raw_documents_detected": scanned,
            "raw_documents_formatted": sum(bool(x.get("formatted")) for x in formatted),
            "toc_blocks_removed": sum(x.get("toc_blocks_removed", 0) for x in formatted),
            "heading_changes": sum(x.get("heading_changes", 0) for x in formatted),
            "page_numbers_removed": sum(x.get("page_numbers_removed", 0) for x in formatted),
            "errors": len(errors),
        },
    }
    Path(args.report).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
