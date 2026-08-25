#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path

TARGETS = [
    Path('temp/《零距离人性》/index.md'),
    Path('temp/《玩转人性》.md'),
]
OUT = Path('temp/.numbered-section-review.tsv')
PAT = re.compile(r'^\s*(\d{1,3})\s*[．.、]\s*(.+)$')
H2 = re.compile(r'^##\s+(.+)$')

rows=['path\tline\tchapter\tno\ttext']
for path in TARGETS:
    chapter='（H1之后/未识别章节）'
    for i, raw in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1):
        h=H2.match(raw.strip())
        if h:
            chapter=h.group(1)
            continue
        m=PAT.match(raw.strip())
        if not m:
            continue
        text=m.group(2).replace('\t',' ')[:180]
        rows.append(f'{path}\t{i}\t{chapter}\t{m.group(1)}\t{text}')
OUT.write_text('\n'.join(rows)+'\n',encoding='utf-8')
print(f'rows={len(rows)-1}')
