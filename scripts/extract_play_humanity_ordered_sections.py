#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path

PATH=Path('temp/《玩转人性》.md')
OUT=Path('temp/.play-humanity-ordered-sections.json')
text=PATH.read_text(encoding='utf-8-sig')
MAJOR=re.compile(r'(?m)^#{2,6}\s+(玩转[^\n]+?)\s*$')
majors=list(MAJOR.finditer(text))
results=[]
for idx,m in enumerate(majors):
    name=m.group(1).strip()
    start=m.end(); end=majors[idx+1].start() if idx+1<len(majors) else len(text)
    chunk=text[start:end]
    cursor=0; seq=[]
    # Follow the earliest monotonic 1,2,3... marker in this major chunk.
    for n in range(1,31):
        pat=re.compile(rf'(?<!\d){n}\s*[．.]\s*')
        hit=pat.search(chunk,cursor)
        if not hit:
            break
        abspos=start+hit.start()
        before=text[max(start,abspos-120):abspos].replace('\n',' ')
        after=text[start+hit.end():min(end,start+hit.end()+320)].replace('\n',' ')
        seq.append({'no':n,'char_offset':abspos,'before':before,'after':after})
        cursor=hit.end()
    results.append({'major':name,'heading_line':text.count('\n',0,m.start())+1,'sequence_length':len(seq),'sequence':seq})
OUT.write_text(json.dumps({'major_count':len(results),'majors':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'major_count':len(results),'sequence_lengths':{x['major']:x['sequence_length'] for x in results}},ensure_ascii=False,indent=2))
