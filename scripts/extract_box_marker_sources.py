#!/usr/bin/env python3
from pathlib import Path
import re

src = Path('temp/《人性难题宝典1-9》.md')
out = Path('temp/.box-marker-sources.tsv')
rx = re.compile(r'^\s*[□▢▫]\s*(.+?)\s*$')
rows = []
for i, raw in enumerate(src.read_text(encoding='utf-8-sig').splitlines(), 1):
    m = rx.match(raw)
    if not m:
        continue
    payload = re.sub(r'\s+', ' ', m.group(1).strip())
    rows.append(f'{i}\t{payload[:260]}')
out.write_text('\n'.join(rows) + '\n', encoding='utf-8')
print(f'box_markers={len(rows)}')
