#!/usr/bin/env python3
"""Extract compact, reviewable anchors from the human-business transcript.

No book content is modified. The output is intentionally small enough to review
before adding any headings to a 400k-character transcript.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

PATH = Path('temp/《人性商战(线下3天2夜全文字版)》.md')
OUT = Path('temp/.human-business-semantic-anchors.json')

TOPICS = [
    '人性破局','人性获取','模式破局','营销破局','爆品破局','爆品颇具','战略破局','团队破局','团队过去',
    '商业模式','人性营销','战略布局','团队获取','股权','合伙人','六大系统','六大破题系统','三大核心',
]
TRANSITIONS = [
    '上午首先为大家分享','上午的课程到此结束','上午课程到此结束','今天上午',
    '下午的课程到此结束','下午课程到此结束','今天下午的主题','下午的主题','下午首先为大家分享',
    '今天晚上','今晚','晚上的主题','明天上午','明天下午','明天晚上','今天课程到此结束',
    '接下来其实这个部分就给大家讲的是','接下来就是后面的课程','接下来为大家分享',
    '第一天','第二天','第三天','三天两晚','三天两夜',
]
CONTACT = re.compile(r'(?i)(?:加\s*我\s*微信|加\s*微信|微信号|wx\s*[:：=]|vx\s*[:：=]|薇芯\s*[:：=]|薇信\s*[:：=]|公号\s*[:：])')


def snippet(text: str, pos: int, needle_len: int, radius: int = 220) -> str:
    a=max(0,pos-radius); b=min(len(text),pos+needle_len+radius)
    return re.sub(r'\s+',' ',text[a:b].strip())


def line_col(text: str, pos: int) -> tuple[int,int]:
    line=text.count('\n',0,pos)+1
    prev=text.rfind('\n',0,pos)
    col=pos-(prev+1)
    return line,col


def hits(text: str, terms: list[str], max_each: int=20):
    out=[]
    for term in terms:
        start=0; n=0
        while n<max_each:
            p=text.find(term,start)
            if p<0: break
            line,col=line_col(text,p)
            out.append({'term':term,'line':line,'col':col,'context':snippet(text,p,len(term))})
            start=p+len(term); n+=1
    return sorted(out,key=lambda x:(x['line'],x['col'],x['term']))


def main():
    text=PATH.read_text(encoding='utf-8-sig')
    contacts=[]
    for m in CONTACT.finditer(text):
        line,col=line_col(text,m.start())
        contacts.append({'match':m.group(0),'line':line,'col':col,'context':snippet(text,m.start(),len(m.group(0)),300)})
        if len(contacts)>=30: break
    payload={
        'policy':'diagnostic only; headings must be based on explicit source transitions/topics, not mtime or heuristic density',
        'metrics':{'characters':len(text),'lines':text.count('\n')+1},
        'topic_hits':hits(text,TOPICS,25),
        'transition_hits':hits(text,TRANSITIONS,25),
        'contact_hits':contacts,
    }
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'topic_hits':len(payload['topic_hits']),'transition_hits':len(payload['transition_hits']),'contact_hits':len(contacts)},ensure_ascii=False))

if __name__=='__main__': main()
