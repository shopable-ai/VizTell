#!/usr/bin/env python3
"""Remove one confirmed duplicate OCR block in 《穷人的底层逻辑》.

The repair is intentionally narrow and aborts unless all safeguards prove the
second block is a duplicate immediately before page-006 while earlier source
copies of all three paragraphs already exist. Markdown image references are an
exact invariant.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PATH = Path('temp/《穷人的底层逻辑》/index.md')
REPORT = Path('temp/.poverty-duplicate-ocr-repair.json')
IMAGE = re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')

A = '穷人缺钱，很容易陷入恶性循环。'
B = '查《说文解字》，穷人的“穷”字'
C = '我曾经看到过一个拾荒者改变命运的报道'
PAGE6 = 'assets/page-006.png'


def refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def starts(lines: list[str], prefix: str) -> list[int]:
    return [i for i, x in enumerate(lines) if x.strip().startswith(prefix)]


def main() -> int:
    before = PATH.read_text(encoding='utf-8-sig')
    before_refs = refs(before)
    lines = before.splitlines()
    errors: list[str] = []

    page6 = next((i for i, x in enumerate(lines) if PAGE6 in x and IMAGE.search(x)), None)
    a = starts(lines, A)
    b = starts(lines, B)
    c = starts(lines, C)

    if page6 is None:
        errors.append('page-006 image anchor not found')
    if len(a) < 2:
        errors.append(f'expected at least 2 A-prefix occurrences, found {len(a)}')
    if len(b) < 2:
        errors.append(f'expected at least 2 B-prefix occurrences, found {len(b)}')
    if len(c) < 2:
        errors.append(f'expected at least 2 C-prefix occurrences, found {len(c)}')

    if errors:
        REPORT.write_text(json.dumps({'status':'blocked','errors':errors,'A':a,'B':b,'C':c,'page6':page6}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({'status':'blocked','errors':errors}, ensure_ascii=False, indent=2))
        return 2

    # Only the final occurrence before page-006 may be removed.
    second_a = max(i for i in a if i < page6)
    second_b = max(i for i in b if i < page6)
    second_c = max(i for i in c if i < page6)

    if not (second_a < second_b < second_c < page6):
        errors.append(f'duplicate block order invalid: A={second_a+1}, B={second_b+1}, C={second_c+1}, page6={page6+1}')
    if page6 - second_c > 4:
        errors.append(f'C duplicate is not immediately before page-006: distance={page6-second_c}')
    if second_c - second_a > 8:
        errors.append(f'duplicate block is unexpectedly wide: span={second_c-second_a+1}')
    if not any(i < second_a for i in a):
        errors.append('no earlier A source copy exists')
    if not any(i < second_a for i in b):
        errors.append('no earlier B source copy exists')
    if not any(i < second_a for i in c):
        errors.append('no earlier C source copy exists')
    # The candidate block must contain no image references or headings.
    for i in range(second_a, second_c + 1):
        s = lines[i].strip()
        if IMAGE.search(lines[i]):
            errors.append(f'image found inside candidate duplicate block at line {i+1}')
        if re.match(r'^#{1,6}\s+', s):
            errors.append(f'heading found inside candidate duplicate block at line {i+1}')

    if errors:
        REPORT.write_text(json.dumps({'status':'blocked','errors':errors,'A':a,'B':b,'C':c,'page6':page6}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({'status':'blocked','errors':errors}, ensure_ascii=False, indent=2))
        return 2

    # Remove only substantive lines from A through C, plus blank lines within
    # that span. Everything before/after is byte-preserved line-for-line.
    out = lines[:second_a] + lines[second_c + 1:]
    after = '\n'.join(out).rstrip() + '\n'

    if before_refs != refs(after):
        errors.append('Markdown image references changed')
    if len(re.findall(r'^#\s+', after, re.M)) != 1:
        errors.append('H1 invariant failed')
    if len(starts(after.splitlines(), A)) >= len(a):
        errors.append('duplicate A occurrence was not reduced')
    if errors:
        REPORT.write_text(json.dumps({'status':'blocked','errors':errors}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        return 2

    PATH.write_text(after, encoding='utf-8')
    payload = {
        'status':'applied',
        'path':str(PATH),
        'removed_line_range':[second_a+1, second_c+1],
        'removed_lines': second_c-second_a+1,
        'page6_line_before': page6+1,
        'earlier_source_copies': {
            'A':[i+1 for i in a if i < second_a],
            'B':[i+1 for i in b if i < second_a],
            'C':[i+1 for i in c if i < second_a],
        },
        'image_refs_preserved':sum(before_refs.values()),
        'errors':[],
    }
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
