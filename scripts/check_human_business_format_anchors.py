#!/usr/bin/env python3
from pathlib import Path
import json

path=Path('temp/《人性商战(线下3天2夜全文字版)》.md')
out=Path('temp/.human-business-anchor-check.json')
text=path.read_text(encoding='utf-8-sig')
anchors=[
('三大核心：搞人、搞钱、搞地盘','三大核心搞人搞钱搞地盘'),
('上午课程：人性获取','上午首先为大家分享的叫人性获取'),
('下午课程：人性营销','今天下午的主题跟大家分享人性营销'),
('商业模式落地','接下来主题商业模式落地'),
('战略破局','我接下来其实这个部分就给大家讲的是战略破局'),
('团队破局：合伙人与股权','第二个我们来看一下合伙人初期在一起的时候，我们该如何分股权'),
]
rows=[]
for heading,anchor in anchors:
    p=text.find(anchor)
    rows.append({'heading':heading,'anchor':anchor,'count':text.count(anchor),'first_pos':p,'context':text[max(0,p-100):p+len(anchor)+180] if p>=0 else None})
payload={'rows':rows}
out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(payload,ensure_ascii=False,indent=2))
