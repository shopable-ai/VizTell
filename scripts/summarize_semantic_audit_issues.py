#!/usr/bin/env python3
import json
from pathlib import Path

src=Path('temp/.semantic-completeness-audit.json')
out=Path('temp/.semantic-audit-issue-index.tsv')
data=json.loads(src.read_text(encoding='utf-8'))
rows=[]
for item in data.get('review',[]):
    for issue in item.get('issues',[]):
        if issue.get('severity')=='info':
            continue
        detail=str(issue.get('detail','')).replace('\t',' ').replace('\n',' ')
        rows.append(f"{issue.get('code')}\t{item.get('path')}\t{detail[:500]}")
out.write_text('\n'.join(rows)+'\n',encoding='utf-8')
print(f'issues={len(rows)}')
