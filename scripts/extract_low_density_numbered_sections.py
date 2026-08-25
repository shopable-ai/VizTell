#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

TARGETS = [
    Path('temp/《零距离人性》/index.md'),
    Path('temp/《玩转人性》.md'),
    Path('temp/布局锦囊5.0/index.md'),
]
OUT = Path('temp/.low-density-numbered-section-candidates.json')
PATTERNS = [
    re.compile(r'^\s*(\d{1,3})\s*[．.、]\s*(.{1,220})$'),
    re.compile(r'^\s*第\s*([一二三四五六七八九十百千万0-9]+)\s*[章节部分篇讲课]\s*(.{0,180})$'),
]


def candidates(path: Path) -> dict:
    text = path.read_text(encoding='utf-8-sig')
    rows = []
    for i, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith(('#', '![', '|', '```', '<!--')):
            continue
        for pat in PATTERNS:
            m = pat.match(s)
            if m:
                rows.append({
                    'line': i,
                    'length': len(s),
                    'text': s[:500],
                    'next_120': '',
                })
                break
    lines = text.splitlines()
    for row in rows:
        j = row['line']
        k = j
        while k < len(lines):
            nxt = lines[k].strip()
            k += 1
            if nxt and not nxt.startswith('!['):
                row['next_120'] = nxt[:120]
                break
    return {
        'path': str(path),
        'existing_headings': [x.strip() for x in text.splitlines() if re.match(r'^#{1,4}\s+', x)],
        'candidate_count': len(rows),
        'candidates': rows,
    }


def main() -> int:
    payload = {'documents': [candidates(p) for p in TARGETS]}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({d['path']: d['candidate_count'] for d in payload['documents']}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
