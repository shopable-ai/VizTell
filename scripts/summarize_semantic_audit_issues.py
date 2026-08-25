#!/usr/bin/env python3
import json
from collections import defaultdict
from pathlib import Path

src = Path('temp/.semantic-completeness-audit.json')
out = Path('temp/.semantic-audit-issue-index.tsv')
summary_out = Path('temp/.semantic-audit-issue-summary.json')
data = json.loads(src.read_text(encoding='utf-8'))
rows = []
by_code = defaultdict(list)
for item in data.get('review', []):
    path = item.get('path')
    for issue in item.get('issues', []):
        if issue.get('severity') == 'info':
            continue
        code = issue.get('code')
        detail = str(issue.get('detail', '')).replace('\t', ' ').replace('\n', ' ')
        rows.append(f"{code}\t{path}\t{detail[:500]}")
        by_code[code].append(path)
out.write_text('\n'.join(rows) + '\n', encoding='utf-8')
compact = {
    'audit_summary': data.get('summary', {}),
    'issue_types': {
        code: {
            'count': len(paths),
            'paths': sorted(set(paths)),
        }
        for code, paths in sorted(by_code.items())
    },
}
summary_out.write_text(json.dumps(compact, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({code: len(paths) for code, paths in sorted(by_code.items())}, ensure_ascii=False))
