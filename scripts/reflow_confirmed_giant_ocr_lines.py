#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

TARGETS = [
    Path('temp/《开窍开智开悟5》.md'),
    Path('temp/《玩转人性》.md'),
    Path('temp/做局大师-人间博弈之术.md'),
]
REPORT = Path('temp/.giant-ocr-reflow-report.json')
IMAGE = re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')


def refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def lexical(text: str) -> str:
    return re.sub(r'\s+', '', text)


def split_line(raw: str, target: int = 650, hard: int = 1100) -> list[str]:
    if len(raw) <= hard:
        return [raw]
    stripped = raw.lstrip()
    if stripped.startswith(('#', '|', '```', '~~~', '<!--')) or IMAGE.search(raw):
        return [raw]
    out = []
    start = 0
    last_break = None
    for i, ch in enumerate(raw):
        if ch in '。！？；.!?;':
            last_break = i + 1
        if i - start >= target and last_break and last_break > start:
            out.append(raw[start:last_break])
            start = last_break
            last_break = None
        elif i - start >= hard and last_break and last_break > start:
            out.append(raw[start:last_break])
            start = last_break
            last_break = None
    out.append(raw[start:])
    return [x for x in out if x != '']


def process(path: Path) -> dict:
    before = path.read_text(encoding='utf-8-sig')
    before_refs = refs(before)
    before_lex = lexical(before)
    lines = before.splitlines()
    giant_before = [i + 1 for i, line in enumerate(lines) if len(line) > 2500]
    out = []
    new_lines = 0
    changed_lines = []
    for i, line in enumerate(lines, 1):
        chunks = split_line(line)
        if len(chunks) > 1:
            changed_lines.append({'line': i, 'length': len(line), 'chunks': len(chunks)})
            new_lines += len(chunks) - 1
        out.extend(chunks)
    after = '\n'.join(out) + ('\n' if before.endswith(('\n', '\r\n')) else '')
    if lexical(after) != before_lex:
        raise RuntimeError(f'{path}: lexical content changed')
    if refs(after) != before_refs:
        raise RuntimeError(f'{path}: image references changed')
    if after != before.replace('\r\n', '\n'):
        path.write_text(after, encoding='utf-8')
    giant_after = [i + 1 for i, line in enumerate(after.splitlines()) if len(line) > 2500]
    return {
        'path': str(path),
        'giant_lines_before': giant_before,
        'changed_lines': changed_lines,
        'new_prose_lines_created': new_lines,
        'giant_lines_after': giant_after,
        'lexical_content_preserved_modulo_whitespace': True,
        'image_refs_preserved': sum(before_refs.values()),
    }


def main() -> int:
    results = []
    errors = []
    for path in TARGETS:
        try:
            results.append(process(path))
        except Exception as exc:
            errors.append({'path': str(path), 'error': str(exc)})
    payload = {'results': results, 'errors': errors}
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == '__main__':
    raise SystemExit(main())
