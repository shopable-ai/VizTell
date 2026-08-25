#!/usr/bin/env python3
"""Restore all boxed section headings in 《人性难题宝典1-9》 exactly.

The 235 titles below were reviewed against temp/.box-marker-sources.tsv. The
script never guesses a boundary: it requires the Nth `□` source payload to
start with the Nth reviewed title. Any mismatch aborts the write.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PATH = Path('temp/《人性难题宝典1-9》.md')
REPORT = Path('temp/.human-questions-exact-heading-repair.json')
BOX = re.compile(r'^\s*[□▢▫]\s*(.+?)\s*$')
IMAGE = re.compile(r'!\[[^\]]*\]\([^\n)]*\)|!\[[^\]]*\]\[[^\]\n]*\]')

TITLES = [
'如何消除人格障碍','如何克服软弱的性格','如何解读成功型与失败型','如何避免“不成功人生”的 6 大错误','为什么人生本无“注定”的说法','如何从“小”字到“大”字','如何掌握处理困难的诀窍','如何掌握突破困境的方法','如何对自己的自卑心理进行分析','为什么不要活在别人的价值观里','如何培养助于成功的精神特质和习惯','如何正确认识你自己','如何找到自己的正确位置','如何走自己的路让别人去说吧','如何学会推销自己','如何主动性地创造生活','如何宠辱不惊把握自我','如何别让感情蒙蔽理智','如何保持冷静客观态度','如何开诚布公信任别人','如何开阔心胸自我解脱','如何树立正确的竞争观念','为什么自我期望值不要过高','如何自我控制保持心理上的平衡','如何少追求物质多追求理想',
'为什么不要嫉妒别人的成功','如何同命运决一死战','如何掌握自我尊重法','如何树立“我为人人，人人为我”的观念','如何淡泊名利不求奢华','为什么要知足者常乐','如何运用理性克制贪欲','战胜人性弱点有哪 5 大绝招','如何克服自身弱点的 12 个“不要”','如何将弱点转化为优点','如何掌握战胜自卑的 5 大法宝','如何迈向成功的心理修备','如何培养成就大业者的心理品质','如何不打没把握的人生之仗','如何了解自己和了解别人','如何巧妙掌握“控制法”','如何留意批评','如何学会与别人合作','如何防止与人争斗','为什么君子之交淡如水','哪些形象最不受欺侮','为什么一见如故要适度远之','为什么借朋友钱不如给钱','为什么友情突然升温要小心','如何用一缕温情征服人心',
'如何用委婉拒绝征服人心','如何征服猛烈型的人','如何征服情绪型的人','如何征服慎重型的人','如何征服浪漫型的人','如何征服现实型的人','如何征服乐天派的人','如何征服无魄力型的人','如何征服形式主义的人','如何征服口密腹剑的人','如何征服吹牛拍马的人','如何征服尖酸刻薄的人','如何征服挑拨离间的人','如何征服笑里藏刀的人','如何征服翻脸无情的人','如何征服戴着面具的“好人”','为什么将心比心服人心','如何制服傲慢对手 3 法','如何掌握对付坏人的 4 大杀手锏','为什么认错使人伟大','如何及时摆脱尴尬境地','在顾客面前被上司指责时该怎么办','如何平静对付冷遇','如何轻松化解言语失误','错怪了别人怎么办',
'如何诱使对方主动说出难于启齿的事情','发现别人嘲讽你时该怎么办','为什么逢人只说三分话','如何多说对方爱听的话','如何说些鼓舞人心的话','如何寻找话题激发共同兴奋点','如何看对方的性格说话','为什么话说的不要太绝','如何掌握开玩笑的“规则”','为什么要有能伸能屈的本领','为什么不属于自己的切莫强求','如何克服因失利而实施报复','如何在争论时尽量保持冷静','如何学会不怕挨批评','如何消除误会','如何主动“拥抱”机会','如何做事半功倍的事','如何掌握办事“二分法”：计划＋习惯','如何找到“第一位”','如何与压力和平共处','为什么冥想可缓解压力','为什么在你痛苦时流泪也能缓解压力','为什么体育锻炼是减轻压力的灵丹妙药','逐步适应处理人生的过度压力','为什么溜之大吉能处理人生过度压力',
'为什么处惊不变是处理人生过度的压力','为什么忘却悲痛是处理人生过度的压力','为什么面对逆境要采取积极态度','为什么逆境会变成好运的台阶','如何面对压力冲破自我樊篱','如何面对压力摆脱墨守成规','如何面对压力不要自我否定','摆脱精神压力有哪些方法','如何疏解工作压力','如何借助人际关系降压','如何以营养降压','如何以运动降压','如何寻找医疗渠道降压','如何疏解压力有哪些好方法','如何建立健康积极的人生观','如何博得异性的喜爱','如何掌握追求爱情的好时机','如何借题发挥地追求恋人','如何单刀直入地追求恋人','初恋有何对策','令女人心里暖洋洋有哪些妙法','如何适度做爱情的“小动作”','如何变单相思为双相思','如何使爱情没有第三者','理想妻子有哪 10 条标准',
'坏妻子有哪些表现','理想丈夫有哪些标准','坏丈夫有哪些表现','如何掌握失恋兵法','如何掌握最佳的婚育年龄','如何推算最佳受孕时间','什么决定胎儿的性别','如何预知生男还是生女','如何做一个好丈夫的方法','如何做一个好妻子的方法','为什么夫妻间要用甜言蜜语','如何快乐度过成家立业后的日子','为什么千万不要后院“起火”','如何学会改善夫妻关系','如何增添婚姻生活的情趣','如何让配偶保持好心情','为什么家和才能万事兴','为什么家庭是爱的调色盘','为什么情感需要精心培养','有了孩子后出现家庭危机怎么办','如何起诉和离婚','如何掌握家庭问题的处理方法','为什么小事是组合家人感情的细胞','为什么积极赞赏会使相互间再多一点爱','如何掌握夫妻间问题的处理方法',
'如何掌握对方嗜赌的处理方法','如何掌握对方有怪癖的处理方法','如何掌握夫妻吵架的处理方法','如何掌握分家难分的处理办法','如何掌握发生遗产纠纷的处理办法','如何掌握婆媳间问题的处理方法','假如你是婆婆如何处理好婆媳关系','假如你是媳妇如何处理好婆媳关系','如何做好孩子的人生规划','如何教给孩子竞争的意识','如何让孩子自己独立自主','如何增强孩子的记忆力','如何重视孩子的想像力','如何提高孩子的思维能力','如何激发孩子的学习智慧','为什么动手动脑对于学习同样重要','如何实现学习与实践的结合','如何对孩子的学习智慧给予肯定','如何锻炼孩子的毅力','为什么吃苦受难是孩子的必修课','如何增强孩子的承受力','为什么对孩子不可溺爱与失爱','为什么尽量让孩子学会自理','如何培养孩子专心致志的习惯','如何培养孩子敏捷灵巧的习惯',
'如何培养孩子精益求精的习惯','如何让孩子学会合作','为什么孩子交友不可不慎','为什么在父母的眼里孩子不论长多大都是孩子','如何定位打工族','如何自己做老板','如何选择创业方向','为什么创业前必须清楚 3 个问题','如何掌握开创事业的基本步骤','什么是经营者有利可图的买卖','如何利用人们爱方便的心理赚钱','如何利用父母“望子成龙”的心理赚钱','为什么经营高档商品或廉价商品都能赚钱','为什么受女性欢迎的产品一定畅销','如何利用众人感到困扰的事情做生意','如何为公司招兵买马','如何学会借别人的钱发财','如何寻找创业搭档','如何协调合作获取成功','经营者为什么要追求最大的利润','怎样与爱挑剔的领导相处','怎样与顽劣贪婪的上司相处','怎样与自私的领导相处','怎样与阴险的上司相处','怎样与傲慢的领导相处',
'如何防止同事小人','如何学会与有棱角的同事打交道','如何对付各种打小报告的同事','如何应付排挤你的同事','如何妥善处理同事和你争功劳','如何对付爱唠叨的下属','如何对付自作聪明的下属','如何对付自私自利的下属','如何对付阴险狡诈的下属','如何防止性骚扰','如何防止朋友中的小人','如何防止生意场中的小人','如何防止情场小人','如何用适当的理由拒绝男友的性要求','如何用超负荷条件拒绝性要求','为什么用诚恳的态度拒绝男友的性要求','如何从失败中摸索事业的目标','如何挣脱失败','如何打败心理上的 7 个敌人','如何不要为失败寻找借口','为什么失败的经验越丰富而成功的几率越大','为什么失败是对一个人人格的试验','为什么苦难往往是经过化妆了的幸福','为什么成功属于打不垮的人','为什么跌倒了要勇敢地站起来',
'为什么多灾多难是一笔珍贵的财富','如何钻研自己的领域','如何激发人本来的潜能','如何打好内心竞赛','如何培养永不言败的心理','为什么面临绝路心里要喊“前进，前进！”','如何在逆境中点燃追求的热情','如何东山再起','如何重新登录成功','如何掌握通向辉煌人生必备的 6 种能力'
]


def refs(text: str) -> Counter[str]:
    return Counter(IMAGE.findall(text))


def main() -> int:
    before = PATH.read_text(encoding='utf-8-sig')
    before_refs = refs(before)
    lines = before.splitlines()
    marker_payloads = [BOX.match(x).group(1).strip() for x in lines if BOX.match(x)]
    errors = []
    if len(TITLES) != 235:
        errors.append(f'reviewed title count={len(TITLES)}, expected=235')
    if len(marker_payloads) != len(TITLES):
        errors.append(f'box marker count={len(marker_payloads)}, title count={len(TITLES)}')
    for i, (payload, title) in enumerate(zip(marker_payloads, TITLES), 1):
        if not payload.startswith(title):
            errors.append(f'#{i}: expected prefix {title!r}, got {payload[:90]!r}')
            if len(errors) >= 20:
                break
    if errors:
        REPORT.write_text(json.dumps({'status':'blocked','errors':errors}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({'status':'blocked','errors':errors}, ensure_ascii=False, indent=2))
        return 2

    out = []
    idx = 0
    splits = []
    for line_no, raw in enumerate(lines, 1):
        m = BOX.match(raw)
        if not m:
            out.append(raw.rstrip())
            continue
        title = TITLES[idx]
        payload = m.group(1).strip()
        body = payload[len(title):].lstrip(' ：:，,。；;、')
        out.append(f'## {title}')
        if body:
            out.extend(['', body])
        splits.append({'source_line':line_no,'title':title,'body_chars_on_marker_line':len(body)})
        idx += 1

    after = '\n'.join(out).rstrip() + '\n'
    if before_refs != refs(after):
        errors.append('Markdown image references changed')
    if len(re.findall(r'^#\s+', after, re.M)) != 1:
        errors.append('H1 invariant failed')
    if BOX.search(after):
        errors.append('boxed section marker remains after exact repair')
    if errors:
        REPORT.write_text(json.dumps({'status':'blocked','errors':errors}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        return 2

    PATH.write_text(after, encoding='utf-8')
    payload = {
        'status':'applied',
        'path':str(PATH),
        'reviewed_titles':len(TITLES),
        'headings_restored':idx,
        'image_refs_preserved':sum(before_refs.values()),
        'splits':splits,
        'errors':[],
    }
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:payload[k] for k in ('status','reviewed_titles','headings_restored','image_refs_preserved')}, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
