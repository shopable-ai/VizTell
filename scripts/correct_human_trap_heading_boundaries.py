#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PATH = Path('temp/《人性陷阱》/index.md')
REPORT = Path('temp/.human-trap-heading-boundary-repair.json')
IMAGE = re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')

# Proven non-question title endings from current-content review.
NONQUESTION_ENDINGS = [
    '职场男女相处的九大陷阱',
    '破解对方强势行为下的“纸老虎“心理',
    '与客户建立私交的 N 个陷阱',
    '温柔地杀你：老板炒你就鱼的 N 个陷阱',
    '小心“温柔“外表下的暴力倾向',
    '外遇的 N 个征兆',
]
INLINE_TRAP = re.compile(r'(?<!\d)(\d{1,3})陷阱\s*(\d+)\s*[：:]\s*')


def refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def boundary(text: str) -> int | None:
    # `text` excludes leading `## ` and starts with 陷阱.
    q = [p for p in (text.find('？'), text.find('?')) if p >= 0]
    if q:
        return min(q) + 1
    for ending in NONQUESTION_ENDINGS:
        p = text.find(ending)
        if p >= 0:
            return p + len(ending)
    return None


def split_overlong_heading(raw: str) -> tuple[list[str], dict | None]:
    if not raw.startswith('## 陷阱'):
        return [raw], None
    text = raw[3:]
    if len(text) <= 80:
        return [raw], None
    cut = boundary(text)
    if not cut:
        raise RuntimeError(f'overlong trap heading has no reviewed boundary: {text[:180]}')
    title = text[:cut].rstrip()
    body = text[cut:].lstrip()
    if not body:
        raise RuntimeError(f'overlong trap heading has empty body: {title}')
    return [f'## {title}', '', body], {'title': title, 'body_prefix': body[:120]}


def split_inline_trap(raw: str) -> tuple[list[str], dict | None]:
    # Recover a page-number-prefixed trap marker glued at the end of a prose line,
    # e.g. `...更有帮助 8陷阱 7 ：为你持家理财，还是...？`.
    m = INLINE_TRAP.search(raw)
    if not m:
        return [raw], None
    before = raw[:m.start()].rstrip()
    page_number = m.group(1)
    trap_no = m.group(2)
    rest = f'陷阱 {trap_no} ：' + raw[m.end():]
    cut = boundary(rest)
    if not cut:
        raise RuntimeError(f'inline trap has no reviewed boundary: {rest[:180]}')
    title = rest[:cut].rstrip()
    body = rest[cut:].lstrip()
    out = []
    if before:
        out.append(before)
        out.append('')
    out.append(f'## {title}')
    if body:
        out.extend(['', body])
    return out, {'removed_page_number': page_number, 'title': title, 'body_prefix': body[:120]}


def main() -> int:
    before = PATH.read_text(encoding='utf-8-sig')
    before_refs = refs(before)
    out: list[str] = []
    heading_splits = []
    inline_splits = []
    for i, raw in enumerate(before.splitlines(), 1):
        pieces, info = split_overlong_heading(raw)
        if info:
            info['source_line'] = i
            heading_splits.append(info)
            out.extend(pieces)
            continue
        pieces, info = split_inline_trap(raw)
        if info:
            info['source_line'] = i
            inline_splits.append(info)
        out.extend(pieces)
    after = '\n'.join(out) + ('\n' if before.endswith(('\n', '\r\n')) else '')
    if refs(after) != before_refs:
        raise RuntimeError('Markdown image references changed')
    remaining_overlong = [
        {'line': i, 'length': len(x[3:]), 'text': x[3:][:180]}
        for i, x in enumerate(after.splitlines(), 1)
        if x.startswith('## 陷阱') and len(x[3:]) > 80
    ]
    remaining_inline = [
        {'line': i, 'text': x[:180]}
        for i, x in enumerate(after.splitlines(), 1)
        if INLINE_TRAP.search(x)
    ]
    if remaining_overlong:
        raise RuntimeError(f'overlong trap headings remain: {remaining_overlong[:5]}')
    if remaining_inline:
        raise RuntimeError(f'inline page-prefixed trap markers remain: {remaining_inline[:5]}')
    PATH.write_text(after, encoding='utf-8')
    payload = {
        'status': 'applied',
        'path': str(PATH),
        'overlong_headings_split': len(heading_splits),
        'inline_page_prefixed_headings_recovered': len(inline_splits),
        'heading_splits': heading_splits,
        'inline_splits': inline_splits,
        'image_refs_preserved': sum(before_refs.values()),
        'errors': [],
    }
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
