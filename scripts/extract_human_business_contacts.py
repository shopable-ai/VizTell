#!/usr/bin/env python3
from pathlib import Path
import re

src=Path('temp/《人性商战(线下3天2夜全文字版)》.md')
out=Path('temp/.human-business-contact-contexts.tsv')
text=src.read_text(encoding='utf-8-sig')
rx=re.compile(r'(?i)(?:加\s*我\s*微信|加\s*微信|微信号|wx\s*[:：=]|vx\s*[:：=]|薇芯\s*[:：=]|薇信\s*[:：=]|公号\s*[:：])')
rows=[]
for m in rx.finditer(text):
    line=text.count('\n',0,m.start())+1
    a=max(0,m.start()-180); b=min(len(text),m.end()+300)
    ctx=re.sub(r'\s+',' ',text[a:b].strip())
    rows.append(f'{line}\t{m.group(0)}\t{ctx}')
out.write_text('\n'.join(rows)+'\n',encoding='utf-8')
print(f'contacts={len(rows)}')
