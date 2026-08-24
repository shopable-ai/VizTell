#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

SRC = Path('temp/007《布局锦囊1.0》/index.md')
DST = Path('temp/007《布局锦囊1.0》/布局锦囊1.0.md')
REPORT = Path('temp/.format-progress.json')
PAGE = re.compile(r'^\s*<!--\s*page\s*:\s*(\d+)\s*-->\s*$', re.I)
PAGE_H = re.compile(r'^\s*#{1,6}\s*第\s*\d+\s*页\s*$')
IMG = re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')
H = re.compile(r'^(#{1,6})\s+(.*)$')
PROMO = re.compile(r'\s*\d*【朋友圈每日更新最新电子版书籍[^\n]*$')


def split_pages(raw: str):
    pages, current_no, current = [], None, []
    for line in raw.splitlines():
        m = PAGE.match(line)
        if m:
            if current_no is not None:
                pages.append((current_no, current))
            current_no, current = int(m.group(1)), []
        else:
            current.append(line)
    if current_no is not None:
        pages.append((current_no, current))
    return pages


def clean_page(page_no: int, block: list[str]):
    cleaned, imgs, first_h1_seen = [], [], False
    for line in block:
        if PAGE_H.match(line):
            continue
        exact_img = IMG.fullmatch(line.strip())
        if exact_img:
            imgs.append(exact_img.group(0)); continue
        new = PROMO.sub('', line).rstrip()
        if not new.strip():
            cleaned.append(''); continue
        hm = H.match(new.strip())
        if hm:
            level, title = len(hm.group(1)), hm.group(2).strip()
            if page_no == 1 and title == '布局锦囊':
                continue
            if level == 1:
                cleaned.append('## ' + title); first_h1_seen = True
            elif level == 2 and first_h1_seen:
                cleaned.append('### ' + title)
            else:
                cleaned.append(new.strip())
        else:
            cleaned.append(new.strip() if new.startswith(' ') else new)
    norm = []
    for x in cleaned:
        if not x.strip():
            if norm and norm[-1] != '': norm.append('')
        else: norm.append(x.rstrip())
    while norm and norm[-1] == '': norm.pop()
    return norm, imgs


def main():
    raw = SRC.read_text(encoding='utf-8')
    images_before = IMG.findall(raw)
    pages = split_pages(raw)
    assert pages and pages[0][0] == 1
    assert any(p == 18 for p, _ in pages) and any(p == 19 for p, _ in pages)
    front, body, toc_images = ['# 布局锦囊1.0', ''], [], []
    moved = 0
    for page_no, block in pages:
        text_lines, imgs = clean_page(page_no, block)
        if 5 <= page_no <= 17:
            toc_images.extend(imgs); continue
        target = front if page_no <= 4 else body
        if text_lines:
            if target and target[-1] != '': target.append('')
            target.extend(text_lines)
        if imgs:
            if target and target[-1] != '': target.append('')
            target.extend(imgs); moved += len(imgs)
    final = front
    if toc_images:
        if final and final[-1] != '': final.append('')
        final.extend(['## 目录', '']); final.extend(toc_images); moved += len(toc_images)
    if body:
        if final and final[-1] != '': final.append('')
        final.extend(body)
    normalized = []
    for x in final:
        if not x.strip():
            if normalized and normalized[-1] != '': normalized.append('')
        else: normalized.append(x.rstrip())
    output = '\n'.join(normalized).strip() + '\n'
    images_after = IMG.findall(output)
    assert images_after == images_before, 'image reference order/path changed'
    assert len(re.findall(r'^#\s+', output, re.M)) == 1
    assert not re.search(r'^\s*<!--\s*page\s*:', output, re.M | re.I)
    assert not re.search(r'^\s*#{1,6}\s*第\s*\d+\s*页\s*$', output, re.M)
    assert '朋友圈每日更新最新电子版书籍' not in output
    DST.write_text(output, encoding='utf-8'); SRC.unlink()
    visible = IMG.sub('', output)
    visible = re.sub(r'^#{1,6}\s*', '', visible, flags=re.M)
    report = {
      'file': str(DST), 'source_bytes': len(raw.encode()), 'output_bytes': len(output.encode()),
      'pages_detected': len(pages), 'toc_ocr_pages_removed': 13, 'page_markers_removed': len(pages),
      'repeated_promo_fragments_removed': len(re.findall(r'【朋友圈每日更新最新电子版书籍', raw)),
      'page_images_moved_after_text': moved, 'image_refs_before': len(images_before),
      'image_refs_after': len(images_after), 'image_refs_changed': images_before != images_after,
      'visible_body_chars': len(re.sub(r'\s+', '', visible)), 'traditional_to_simplified': False,
      'notes': 'Pages 5-17 OCR directory text removed; all original page screenshots preserved in source order under 目录.'}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__': main()
