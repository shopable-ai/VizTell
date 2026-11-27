import json
from playwright.sync_api import sync_playwright

# Source-derived mechanisms, not the complete installed OpenDesk extension.
# A: preserve the right-edge clearance policy (28px capped at 10% of width).
# G: reproduce candidate selection based on event.target and ancestor traversal.
results={"scope":"isolated Chromium page, source-derived minimal mechanisms; not installed extension or native OS pointer test"}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':800,'height':600})
    page.set_content('''<style>body{height:3000px;margin:0}#track{position:fixed;right:0;top:0;width:24px;height:100%;background:#aaa}#knob{position:absolute;top:80px;right:0;width:24px;height:180px;background:#444}#toc{position:fixed;right:0;top:140px;width:38px;height:46px;z-index:100;background:#ccc;pointer-events:auto}</style><div id="track"><div id="knob"></div></div><button id="toc">TOC</button><script>window.trace=[];let k=document.querySelector('#knob');document.addEventListener('pointerdown',e=>trace.push(['down',e.target.id,e.isTrusted]));k.addEventListener('pointerdown',e=>k.setPointerCapture(e.pointerId));k.addEventListener('pointermove',e=>{if(k.hasPointerCapture(e.pointerId)){window.scrollTo(0,Math.max(0,e.clientY-150)*5);}});</script>''')
    a=[]
    # Custom scrollbar fixture: intentional 24px or 32px occupied region.
    # Test criterion: same pointer starting inside fixture thumb at x=innerWidth-width+2, y=155,
    # trusted pointerdown delivered to thumb, and scroll position increases after drag.
    for strip in [24,32]:
        for mode in ['overlap','safe28','noninteractive']:
            page.evaluate('''([strip,mode])=>{scrollTo(0,0);trace.length=0;let t=document.querySelector('#toc');document.querySelector('#track').style.width=strip+'px';document.querySelector('#knob').style.width=strip+'px';t.style.right=mode==='safe28'?'28px':'0px';t.style.pointerEvents=mode==='noninteractive'?'none':'auto';}''',[strip,mode])
            x=800-strip+2
            page.mouse.move(x,155);page.mouse.down();page.mouse.move(x,290,steps=8);page.mouse.up()
            row=page.evaluate('''()=>({trace:trace.slice(),scrollY:window.scrollY})''');row.update({'strip_px':strip,'mode':mode,'start_x':x,'pass':row['trace'][0][1]=='knob' and row['scrollY']>0});a.append(row)
    results['A']=a
    assert [r['pass'] for r in a]==[False,True,True,False,False,True],a
    # G: fixed scenario. Child has visible content but is not necessarily hit target.
    page.set_content('''<style>body{margin:0}#parent{margin:30px;padding:20px;width:300px;height:100px;background:#eee}#tiny{display:inline-block;background:#ff0;font-size:14px}</style><article id="parent"><span id="tiny">短文本</span><p>Other answer text</p></article><script>window.trace=[];document.addEventListener('pointerdown',e=>{let node=e.target;let ids=[];while(node&&node!==document.body&&node!==document.documentElement){let r=node.getBoundingClientRect();if(r.width>0&&r.height>0&&node.textContent.trim())ids.push(node.id);node=node.parentElement;}trace.push({target:e.target.id,candidates:ids,trusted:e.isTrusted})});</script>''')
    g=[]
    for pe in ['auto','none','auto']:
        page.locator('#tiny').evaluate('(e,v)=>e.style.pointerEvents=v',pe)
        rect=page.locator('#tiny').bounding_box();x=rect['x']+rect['width']/2;y=rect['y']+rect['height']/2
        hit=page.evaluate('([x,y])=>document.elementFromPoint(x,y).id',[x,y]);page.mouse.click(x,y)
        r=page.evaluate('()=>trace[trace.length-1]');r.update({'pointer_events':pe,'element_from_point':hit,'x':x,'y':y});g.append(r)
    results['G']=g
    assert [r['target'] for r in g]==['tiny','parent','tiny'],g
    assert [r['candidates'][0] for r in g]==['tiny','parent','tiny'],g
    assert all(r['trusted'] for r in g)
    results['chromium_version']=browser.version
    browser.close()
print(json.dumps(results,ensure_ascii=False,indent=2))
