#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PATH = Path('temp/《玩转人性》.md')
REPORT = Path('temp/.play-humanity-safe-section-repair.json')
IMAGE = re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')
MAJOR = re.compile(r'^#{2,6}\s+(玩转[^\n]+?)\s*$')

# Reviewed line-start subsection titles. These are distinct from inline numeric
# enumerations inside prose and therefore safe to promote.
SECTIONS = {
    ('玩转生活',2): '试验 80 人，79 人用身体“说话"',
    ('玩转生活',4): '有趣的狗打架',
    ('玩转生活',7): '校长误解了一位女学生的眼神',
    ('玩转职场',1): '瞒不过丁老板的三角眼',
    ('玩转职场',8): '他寡言少语，怎么也当上了头头',
    ('玩转职场',9): '老板驾驭部下的“体语软件”',
    ('玩转职场',10): '由走路来了解你的职员',
    ('玩转生意场',4): '石膏点豆腐，一物降一物',
    ('玩转生意场',5): '正确运用“假眠效果”',
    ('玩转办公室',2): '“看他那样。官气十足"',
    ('玩转会议',7): '会场上的“四个怎么样"',
    ('玩转路途',1): '怎样“就坐"或“就站"',
    ('玩转路途',2): '人到底需要多大的私人空间',
    ('玩转路途',5): '研究证明，鼻子也会“说话"',
    ('玩转会客',2): '口蜜腹剑与推心置腹',
    ('玩转会客',9): '恋恋不舍——绝妙的告别',
    ('玩转家庭',1): '家庭探秘',
    ('玩转家庭',7): '在家里，男女平等难',
    ('玩转舞会',2): '被冷落的漂亮妞',
    ('玩转舞会',6): '眼神及其在舞场上的运用',
    ('玩转舞会',7): '千万莫“盯"人',
    ('玩转情场',1): '从女人胸脯捕捉“性"信号',
    ('玩转情场',6): '姑娘火了，她要叫警察',
}


def refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def main() -> int:
    before = PATH.read_text(encoding='utf-8-sig')
    before_refs = refs(before)
    lines = before.splitlines()
    current_major = None
    out = []
    major_fixed = []
    restored = []

    for lineno, raw in enumerate(lines, 1):
        s = raw.strip()
        m = MAJOR.match(s)
        if m:
            current_major = m.group(1).strip()
            out.append(f'## {current_major}')
            major_fixed.append({'line': lineno, 'major': current_major, 'old': s})
            continue

        matched = False
        if current_major:
            for (major, no), title in SECTIONS.items():
                if major != current_major:
                    continue
                pat = re.compile(rf'^\s*{no}\s*[．.]\s*{re.escape(title)}')
                hit = pat.match(raw)
                if not hit:
                    continue
                body = raw[hit.end():]
                out.append(f'### {no}. {title}')
                if body.strip():
                    out.extend(['', body.lstrip()])
                restored.append({'source_line': lineno, 'major': major, 'no': no, 'title': title, 'body_prefix': body.lstrip()[:120]})
                matched = True
                break
        if not matched:
            out.append(raw)

    after = '\n'.join(out) + ('\n' if before.endswith(('\n','\r\n')) else '')
    if refs(after) != before_refs:
        raise RuntimeError('Markdown image references changed')
    if len(re.findall(r'^#\s+', after, re.M)) != 1:
        raise RuntimeError('expected exactly one H1')
    majors = [m.group(1).strip() for m in map(MAJOR.match, after.splitlines()) if m]
    if len(majors) != 11 or any(not line.startswith('## ') for line in after.splitlines() if MAJOR.match(line.strip())):
        raise RuntimeError(f'expected 11 H2 major sections, got {len(majors)}')
    if len(restored) != len(SECTIONS):
        got={(x['major'],x['no']) for x in restored}
        missing=[key for key in SECTIONS if key not in got]
        raise RuntimeError(f'expected {len(SECTIONS)} reviewed line-start sections, restored {len(restored)}; missing={missing}')

    PATH.write_text(after, encoding='utf-8')
    payload = {
        'status':'applied','path':str(PATH),
        'major_sections_normalized_to_h2':len(major_fixed),
        'reviewed_line_start_sections_restored':len(restored),
        'image_refs_preserved':sum(before_refs.values()),
        'majors':major_fixed,'sections':restored,'errors':[]
    }
    REPORT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in payload.items() if k not in ('majors','sections')},ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
