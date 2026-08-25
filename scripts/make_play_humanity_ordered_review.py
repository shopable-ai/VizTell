#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
src=Path('temp/.play-humanity-ordered-sections.json')
out=Path('temp/.play-humanity-ordered-review.tsv')
data=json.loads(src.read_text(encoding='utf-8'))
rows=['major\tno\tafter_prefix']
for major in data.get('majors',[]):
    for item in major.get('sequence',[]):
        after=' '.join(str(item.get('after','')).split())
        rows.append(f"{major.get('major','')}\t{item.get('no')}\t{after[:280]}")
out.write_text('\n'.join(rows)+'\n',encoding='utf-8')
print(f'rows={len(rows)-1}')
