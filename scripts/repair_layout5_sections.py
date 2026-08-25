#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PATH = Path('temp/布局锦囊5.0/index.md')
REPORT = Path('temp/.layout5-section-repair.json')
IMAGE = re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')

# Current-content reviewed section sequence.  Titles are normalized only for
# OCR whitespace/punctuation; no missing section is invented.
REVIEWED = [
    ('第一节 时间：如何让你的时间投资卓有成效？', r'第一\s*节\s*时间[：:]\s*如何让你的时间投资卓有成效[？?]'),
    ('第二节 状态：如何成为一个更在状态的狠人？', r'第二\s*节\s*状态[：:]\s*如何成为一个更在状态的狠人[？?]'),
    ('第三节 情商：如何既取悦自己又让别人舒服？', r'第三\s*节\s*情商[：:]\s*如何既取悦自己又让别人舒服[？?]'),
    ('第四节 学霸：如何加速成为某个领域的高手？', r'第四\s*节\s*学霸[：:]\s*如何加速成为某个领域的高手[？?]'),
    ('第五节 读书：如何将读过的书转化为生产力？', r'第五\s*节\s*读书[：:]\s*如何将读过的书转化为生产力[？?]'),
    ('第六节 写作：如何通过写作让自己更有优势？', r'第六\s*节\s*写作[；;：:]\s*如何通过写作让自己更有优势[？?]'),
    ('第七节 讲课：如何让你讲出去的话很有价值？', r'第七\s*节\s*讲课[：:]\s*如何让你讲出去的话很有价值[？?]'),
    ('第八节 牛人：如何通过持续见牛人突破自己？', r'第八\s*节\s*牛人[：:]\s*如何通过持续见牛人突破自己[？?]'),
    ('第一节 贵人：如何让自己拥有超好的贵人运？', r'第一\s*节\s*贵人[：:]\s*如何让自[已己]拥有超好的贵人运[？?]'),
    ('第二节 团队：如何打造极有战斗力的小团队？', r'第二\s*节\s*团队\s*[：:]\s*(?:然后|如何)?\s*打造极有战斗力的小\s*团\s*队\s*[？?]'),
    ('第三节 销售：如何让你的销售能力大幅提升？', r'第三\s*节\s*销售[：:]\s*如\s*何让你\s*的\s*销\s*售\s*能\s*力大幅提升[？?]'),
    ('第四节 个人品牌：如何让你的个人品牌越来越贵？', r'第四\s*节\s*(?:个人品牌[：:]\s*)?如何让你的个人品牌越来越贵[？?]'),
    ('第五节 冠军：如何运用冠军战略吸引好机会？', r'第五\s*节\s*冠军[：:]\s*如何运用冠军战略吸引好机会[？?]'),
    ('第六节 赚钱：如何有效提高自己的赚钱水平？', r'第六\s*节\s*赚钱\s*[：:]\s*如何有效提高\s*自\s*己的\s*赚钱水\s*平[？?]'),
    ('第七节 写书：如何让写书这件事变得更容易？', r'第七\s*节\s*写书\s*[：:]\s*如何让写\s*书这\s*件事\s*变\s*得更\s*容\s*易[？?]'),
]
COMPILED = [(title, re.compile(pattern)) for title, pattern in REVIEWED]


def refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def main() -> int:
    before = PATH.read_text(encoding='utf-8-sig')
    before_refs = refs(before)
    lines = before.splitlines()
    out: list[str] = []
    restored: list[dict] = []

    for lineno, raw in enumerate(lines, 1):
        line = raw
        if line.strip() == '### 第一部分：打基础':
            out.append('## 第一部分：打基础')
            continue

        matched = False
        for title, pat in COMPILED:
            m = pat.search(line)
            if not m:
                continue
            prefix = line[:m.start()].rstrip()
            suffix = line[m.end():].lstrip()
            # These reviewed markers are section boundaries; preserve any
            # preceding/succeeding OCR text as prose instead of discarding it.
            if prefix:
                out.append(prefix)
                out.append('')
            out.append(f'### {title}')
            if suffix:
                out.extend(['', suffix])
            restored.append({
                'source_line': lineno,
                'title': title,
                'had_prefix': bool(prefix),
                'prefix_tail': prefix[-120:] if prefix else '',
                'had_suffix': bool(suffix),
                'suffix_prefix': suffix[:120] if suffix else '',
            })
            matched = True
            break
        if not matched:
            out.append(line)

    after = '\n'.join(out) + ('\n' if before.endswith(('\n', '\r\n')) else '')
    if refs(after) != before_refs:
        raise RuntimeError('Markdown image references changed')
    if len(re.findall(r'^#\s+', after, re.M)) != 1:
        raise RuntimeError('expected exactly one H1')
    if len(restored) != len(REVIEWED):
        got = {x['title'] for x in restored}
        missing = [title for title, _ in REVIEWED if title not in got]
        raise RuntimeError(f'expected {len(REVIEWED)} reviewed sections, restored {len(restored)}; missing={missing}')
    # All reviewed section titles must appear exactly once as H3.
    bad = [title for title, _ in REVIEWED if after.count(f'### {title}') != 1]
    if bad:
        raise RuntimeError(f'reviewed H3 count invariant failed: {bad}')
    if '### 第一部分：打基础' in after or after.count('## 第一部分：打基础') != 1:
        raise RuntimeError('first major-part hierarchy not repaired')

    PATH.write_text(after, encoding='utf-8')
    payload = {
        'status': 'applied',
        'path': str(PATH),
        'major_part_upgraded_to_h2': True,
        'reviewed_sections_restored': len(restored),
        'embedded_sections_split_from_prose': sum(x['had_prefix'] for x in restored),
        'image_refs_preserved': sum(before_refs.values()),
        'restored': restored,
        'errors': [],
    }
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in payload.items() if k != 'restored'}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
