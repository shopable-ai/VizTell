#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PATH = Path('temp/《零距离人性》/index.md')
REPORT = Path('temp/.zero-distance-structure-repair.json')
IMAGE = re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')
PAGE_V = re.compile(r'\s*\d{1,3}\s*V\s*$')

SECTIONS = {
    '第二章 细察行为，了解性情': [
        (1,'触摸'),(2,'涂鸦'),(3,'点菜'),(4,'拿烟'),(5,'握手'),(6,'亲吻'),(7,'喝水'),
        (8,'习惯性行为'),(9,'男人的小动作'),(10,'吃东西的方式'),(11,'握电话筒的方式'),
        (12,'挤公车'),(13,'开车方式'),(14,'下车方式'),
    ],
    '第三章 穿着打扮，暴露内心': [
        (1,'着装'),(2,'穿衣风格'),(3,'鞋'),(4,'背包'),(5,'眼镜'),(6,'香水'),(7,'颜色'),
        (8,'领带'),(9,'发型'),(10,'帽子'),(11,'妆容'),(12,'戒指'),(13,'首饰'),(14,'T 恤'),
        (15,'手表'),(16,'衬衫'),(17,'内衣'),
    ],
}

BAD_H3_PREFIXES = (
    '### 第二部分是中部，也就是人们所谓的“中庭”',
    '### 第三部分，下部，也就是人们经常说的下庭',
)
PROMO = re.compile(r'[,，]?\s*更多资料加\s*信ipip885\s*[,，]?')


def refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def main() -> int:
    before = PATH.read_text(encoding='utf-8-sig')
    before_refs = refs(before)
    lines = before.splitlines()
    current_h2 = None
    expected = {chapter: {no:title for no,title in items} for chapter,items in SECTIONS.items()}
    restored = []
    page_removed = 0
    promo_removed = 0
    demoted = 0
    out = []

    for i, raw in enumerate(lines, 1):
        line = raw
        if line.startswith('## '):
            current_h2 = line[3:].strip()

        if any(line.startswith(prefix) for prefix in BAD_H3_PREFIXES):
            line = line[4:]
            demoted += 1

        # Remove only the exact intrusive credential phrase, not narrative mentions.
        line, n = PROMO.subn('', line)
        promo_removed += n

        # OCR page marker like `38 V` occurs at the physical page boundary.
        if not IMAGE.search(line):
            new_line, n = PAGE_V.subn('', line)
            if n:
                page_removed += n
                line = new_line.rstrip()

        if current_h2 in expected and not line.lstrip().startswith('#'):
            for no, title in expected[current_h2].items():
                m = re.match(rf'^\s*{no}\s*[．.、]\s*{re.escape(title)}(.*)$', line)
                if not m:
                    continue
                remainder = m.group(1)
                out.append(f'### {no}. {title}')
                if remainder.strip():
                    out.extend(['', remainder.lstrip()])
                restored.append({'source_line': i, 'chapter': current_h2, 'no': no, 'title': title})
                line = None
                break
            if line is None:
                continue

        out.append(line)

    after = '\n'.join(out) + ('\n' if before.endswith(('\n','\r\n')) else '')
    if refs(after) != before_refs:
        raise RuntimeError('Markdown image references changed')
    if len(re.findall(r'^#\s+', after, re.M)) != 1:
        raise RuntimeError('expected exactly one H1')
    if len(restored) != 31:
        raise RuntimeError(f'expected 31 reviewed section headings, restored {len(restored)}')
    if PROMO.search(after):
        raise RuntimeError('direct promo credential remains')
    if any(x.startswith(BAD_H3_PREFIXES) for x in after.splitlines()):
        raise RuntimeError('known false H3 remains')
    PATH.write_text(after, encoding='utf-8')
    payload = {
        'status':'applied','path':str(PATH),'section_headings_restored':len(restored),
        'page_v_markers_removed':page_removed,'direct_promo_phrases_removed':promo_removed,
        'false_h3_demoted':demoted,'image_refs_preserved':sum(before_refs.values()),
        'restored':restored,'errors':[]
    }
    REPORT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in payload.items() if k not in ('restored',)},ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
