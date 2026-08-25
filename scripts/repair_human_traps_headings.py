#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PATH = Path('temp/《人性陷阱》/index.md')
REPORT = Path('temp/.human-traps-heading-repair.json')
IMAGE = re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')
TRAP = re.compile(r'^(?!##\s)(陷阱\s*\d+\s*[：:]\s*.+?)\s*$')


def refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def main() -> int:
    before = PATH.read_text(encoding='utf-8-sig')
    before_refs = refs(before)
    out = []
    repaired = []
    for i, raw in enumerate(before.splitlines(), 1):
        m = TRAP.match(raw.strip())
        if m:
            title = re.sub(r'\s+', ' ', m.group(1)).strip()
            out.append(f'## {title}')
            repaired.append({'source_line': i, 'title': title})
        else:
            out.append(raw)
    after = '\n'.join(out) + ('\n' if before.endswith(('\n', '\r\n')) else '')
    if refs(after) != before_refs:
        raise RuntimeError('Markdown image references changed')
    if len(re.findall(r'^#\s+', after, re.M)) != 1:
        raise RuntimeError('expected exactly one H1')
    remaining = [x for x in after.splitlines() if re.match(r'^陷阱\s*\d+\s*[：:]', x.strip())]
    if not repaired:
        raise RuntimeError('no explicit trap headings found')
    if remaining:
        raise RuntimeError(f'{len(remaining)} explicit trap headings remain')
    PATH.write_text(after, encoding='utf-8')
    payload = {
        'status': 'applied',
        'path': str(PATH),
        'headings_restored': len(repaired),
        'image_refs_preserved': sum(before_refs.values()),
        'headings': repaired,
        'errors': [],
    }
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
