#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path('temp')
AUDIT = ROOT / '.semantic-completeness-audit.json'
PROMO = ROOT / '.explicit-promo-token-summary.json'
REPORT = ROOT / '.final-markdown-corpus-validation.json'
PROMPT = Path('.prompt/Markdown文档整理与修复通用提示词.md')
IMAGE = re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')
PROMPT_MARKER = '### 5. “确定缺陷”与“复核候选”必须分开统计'


def git_head() -> str:
    p = subprocess.run(['git','rev-parse','HEAD'], text=True, capture_output=True, check=True)
    return p.stdout.strip()


def main() -> int:
    audit = json.loads(AUDIT.read_text(encoding='utf-8'))
    promo = json.loads(PROMO.read_text(encoding='utf-8'))
    prompt_text = PROMPT.read_text(encoding='utf-8-sig')
    md_files = sorted(p for p in ROOT.rglob('*.md') if p.is_file() and not p.name.startswith('.'))

    h1_bad = []
    image_total = 0
    for path in md_files:
        text = path.read_text(encoding='utf-8-sig')
        h1 = len(re.findall(r'^#\s+', text, flags=re.M))
        if h1 != 1:
            h1_bad.append({'path': str(path), 'h1': h1})
        image_total += len(IMAGE.findall(text))

    summary = audit.get('summary', {})
    issue_counts = audit.get('issue_counts', {})
    candidate_counts = audit.get('review_candidate_counts', {})
    promo_summary = promo.get('summary', {})

    checks = {
        'markdown_file_count_matches_audit': len(md_files) == summary.get('markdown_files_scanned'),
        'all_files_objectively_pass': summary.get('pass') == len(md_files),
        'actionable_high_defects_zero': summary.get('needs_review_high') == 0,
        'actionable_medium_defects_zero': summary.get('needs_review_medium') == 0,
        'actionable_issue_types_zero': not issue_counts,
        'explicit_promo_tokens_zero': promo_summary.get('occurrences') == 0 and promo_summary.get('files') == 0,
        'all_files_exactly_one_h1': not h1_bad,
        'image_total_matches_audit': image_total == summary.get('image_refs_total'),
        'prompt_completion_rules_present': PROMPT_MARKER in prompt_text,
    }
    ok = all(checks.values())
    payload = {
        'status': 'pass' if ok else 'fail',
        'head_commit_at_validation': git_head(),
        'summary': {
            'markdown_files': len(md_files),
            'objective_pass': summary.get('pass'),
            'actionable_high_defects': summary.get('needs_review_high'),
            'actionable_medium_defects': summary.get('needs_review_medium'),
            'explicit_promo_occurrences': promo_summary.get('occurrences'),
            'explicit_promo_files': promo_summary.get('files'),
            'markdown_image_refs_total': image_total,
            'review_candidate_docs': summary.get('review_candidate_docs'),
            'review_candidate_counts': candidate_counts,
        },
        'checks': checks,
        'h1_failures': h1_bad,
        'note': 'Review candidates are high-recall observations only and are intentionally not counted as actionable defects.',
    }
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if ok else 2


if __name__ == '__main__':
    raise SystemExit(main())
