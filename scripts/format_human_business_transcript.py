#!/usr/bin/env python3
"""Structure 《人性商战(线下3天2夜全文字版)》 from explicit source anchors.

This is not a topic-model guess. Each inserted heading is tied to an exact
phrase spoken in the transcript. The body text is preserved character-for-
character modulo whitespace/newlines, and giant speech-to-text lines are
reflowed only at sentence punctuation for Markdown readability.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PATH = Path('temp/《人性商战(线下3天2夜全文字版)》.md')
REPORT = Path('temp/.human-business-format-repair.json')
IMAGE = re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')

# heading, exact body anchor. The heading wording is taken directly from the
# same anchor or from the course overview that explicitly defines the module.
ANCHORS = [
    ('三大核心：搞人、搞钱、搞地盘', '三大核心搞人搞钱搞地盘'),
    ('上午课程：人性导航图', '上午我重点为大家分享的是人性导航图'),
    ('下午课程：人性营销', '今天下午的主题跟大家分享人性营销'),
    ('商业模式落地', '接下来主题商业模式落地'),
    ('战略破局', '我接下来其实这个部分就给大家讲的是战略破局'),
    ('团队破局：合伙人与股权', '第二个我们来看一下合伙人初期在一起的时候，我们该如何分股权'),
]


def refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def body_fingerprint(text: str) -> str:
    # Ignore whitespace only. All original lexical content must survive.
    return re.sub(r'\s+', '', text)


def insert_headings(text: str) -> tuple[str, list[dict]]:
    work = text
    inserted = []
    errors = []
    positions = []
    for heading, anchor in ANCHORS:
        count = work.count(anchor)
        if count != 1:
            errors.append(f'anchor {anchor!r} occurs {count} times, expected 1')
        else:
            positions.append((work.find(anchor), heading, anchor))
    if errors:
        raise RuntimeError('; '.join(errors))

    for pos, heading, anchor in sorted(positions, reverse=True):
        prefix = work[:pos].rstrip()
        suffix = work[pos:].lstrip()
        work = prefix + f'\n\n## {heading}\n\n' + suffix
        inserted.append({'heading': heading, 'anchor': anchor, 'original_char_offset': pos})
    inserted.sort(key=lambda x: x['original_char_offset'])
    return work, inserted


def split_giant_line(raw: str, target: int = 650, hard: int = 1100) -> list[str]:
    """Split a prose line only after sentence punctuation.

    The function never edits, normalizes or deletes characters. If a stretch
    has no suitable punctuation, it is left intact rather than hard-cutting a
    word or number.
    """
    if len(raw) <= hard or raw.lstrip().startswith(('#', '|', '```', '~~~', '<!--')) or IMAGE.search(raw):
        return [raw]

    chunks = []
    start = 0
    last_sentence = None
    for i, ch in enumerate(raw):
        if ch in '。！？!?':
            last_sentence = i + 1
            current_len = last_sentence - start
            if current_len >= target:
                chunks.append(raw[start:last_sentence])
                start = last_sentence
                last_sentence = None
    if start < len(raw):
        tail = raw[start:]
        if chunks and len(tail) < 120:
            chunks[-1] += tail
        else:
            chunks.append(tail)
    return chunks if chunks else [raw]


def reflow(text: str) -> tuple[str, dict]:
    out = []
    giant_before = 0
    lines_created = 0
    for raw in text.splitlines():
        if len(raw) > 1100 and not raw.lstrip().startswith(('#', '|', '```', '~~~', '<!--')) and not IMAGE.search(raw):
            giant_before += 1
        pieces = split_giant_line(raw)
        if len(pieces) == 1:
            out.append(raw.rstrip())
        else:
            for j, piece in enumerate(pieces):
                if j:
                    out.append('')
                out.append(piece.rstrip())
            lines_created += len(pieces) - 1
    result = '\n'.join(out).rstrip() + '\n'
    giant_after = sum(1 for x in result.splitlines() if len(x) > 2500 and not IMAGE.search(x))
    return result, {
        'giant_lines_over_1100_before': giant_before,
        'new_prose_lines_created': lines_created,
        'lines_over_2500_after': giant_after,
    }


def main() -> int:
    before = PATH.read_text(encoding='utf-8-sig')
    before_refs = refs(before)
    errors = []
    try:
        with_headings, inserted = insert_headings(before)
        after, reflow_stats = reflow(with_headings)
    except Exception as exc:
        REPORT.write_text(json.dumps({'status':'blocked','errors':[str(exc)]}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(str(exc))
        return 2

    stripped_after_lines = []
    inserted_lines = {f'## {h}' for h, _ in ANCHORS}
    for raw in after.splitlines():
        if raw.strip() in inserted_lines:
            continue
        stripped_after_lines.append(raw)
    after_body = '\n'.join(stripped_after_lines)
    if body_fingerprint(before) != body_fingerprint(after_body):
        errors.append('original transcript body changed beyond whitespace/newlines')
    if before_refs != refs(after):
        errors.append('Markdown image references changed')
    if len(re.findall(r'^#\s+', after, re.M)) != 1:
        errors.append('H1 invariant failed')
    for heading, anchor in ANCHORS:
        if after.count(f'## {heading}') != 1:
            errors.append(f'heading count invalid: {heading}')
        if after.count(anchor) != 1:
            errors.append(f'body anchor count invalid after repair: {anchor}')
    if errors:
        REPORT.write_text(json.dumps({'status':'blocked','errors':errors}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({'status':'blocked','errors':errors}, ensure_ascii=False, indent=2))
        return 2

    PATH.write_text(after, encoding='utf-8')
    payload = {
        'status':'applied',
        'path':str(PATH),
        'headings_inserted':len(inserted),
        'inserted':inserted,
        **reflow_stats,
        'original_body_preserved_modulo_whitespace':True,
        'image_refs_preserved':sum(before_refs.values()),
        'errors':[],
    }
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
