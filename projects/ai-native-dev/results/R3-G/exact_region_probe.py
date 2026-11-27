"""Verify exact read-only module bytes and run isolated Chromium browser cases.
Usage: python exact_region_probe.py /path/to/region-picker.js
No extension install, no external site/network, fake extraction returns only ID/text.
"""
import base64, hashlib, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
src=Path(sys.argv[1]).read_bytes()
sha=hashlib.sha1(b'blob '+str(len(src)).encode()+b'\0'+src).hexdigest()
assert sha=='45f09fae8c948bfd748b66c01d3066282e550b1c',sha
candidate='--candidate' in sys.argv
if candidate:
    # Scratch-only candidate: validate eligibility immediately before extraction;
    # retain explicit ancestor selection only when it remains eligible.
    old=b'    if(!node||!node.isConnected)return;\n    // Conversion is synchronous'
    new=b"    if(!node||!node.isConnected)return;\n    if(!regionCandidates(lastTarget||target,doc,win).includes(node)){cancel('region eligibility changed');return;}\n    // Conversion is synchronous"
    assert src.count(old)==1
    src=src.replace(old,new,1)
uri='data:text/javascript;base64,'+base64.b64encode(src).decode()
html='''<style>body{margin:0}article{margin:30px;padding:20px;width:300px;height:180px;background:#eee}#tiny,#token{display:inline-block;background:#ff0}</style><article id="parent"><span id="tiny">Tiny text</span><p>Other text</p><pre id="code"><span id="token">let x=1</span></pre></article><input id="secret" type="password" value="fixture">'''
rows=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':800,'height':600})
    def reset():
        page.goto('about:blank');page.set_content(html)
        page.evaluate('async uri=>{window.picker=await import(uri)}',uri)
        page.evaluate("""()=>{window.events=[];window.extracted=[];document.addEventListener('click',e=>events.push({target:e.target.id,trusted:e.isTrusted}),true);window.start=()=>{window.session=picker.beginRegionPick({extract:n=>{extracted.push(n.id);return n.id+':'+n.textContent},timeoutMs:1500});window.outcome=null;session.promise.then(x=>outcome={ok:true,...x},e=>outcome={ok:false,error:e.message})}}""")
    def coords(sel):
        r=page.locator(sel).bounding_box();return r['x']+r['width']/2,r['y']+r['height']/2
    def finish(case,expected):
        page.wait_for_function('outcome!==null',timeout=3000)
        row=page.evaluate('()=>({outcome,events,extracted,overlay_remains:!!document.querySelector("[data-opendesk-clip-root]")})');row.update(case=case,expected=expected)
        actual=row['extracted'][0] if row['extracted'] else None
        row['matches_expected']=(actual==expected and not row['overlay_remains']);rows.append(row)
    for pe in ['auto','none','auto']:
        reset();page.locator('#tiny').evaluate('(e,v)=>e.style.pointerEvents=v',pe);x,y=coords('#tiny');page.evaluate('start()');page.mouse.move(x,y);page.mouse.click(x,y);finish('tiny_'+pe,'parent' if pe=='none' else 'tiny')
    reset();x,y=coords('#token');page.evaluate('start()');page.mouse.move(x,y);page.mouse.click(x,y);finish('pre_atomic','code')
    reset();x,y=coords('#tiny');page.evaluate('start()');page.keyboard.down('Control');page.mouse.move(x,y);page.mouse.click(x,y);page.keyboard.up('Control');finish('ctrl_append','tiny');assert rows[-1]['outcome']['append'] is True
    reset();x,y=coords('#secret');page.evaluate('start()');page.mouse.move(x,y);page.mouse.click(x,y);page.keyboard.press('Escape');finish('password_blocked',None)
    reset();x,y=coords('#tiny');page.evaluate('start()');page.mouse.move(x,y);page.evaluate("location.hash='changed'");page.mouse.click(x,y);finish('route_changed',None)
    reset();x,y=coords('#tiny');page.evaluate('start()');page.mouse.move(x,y);page.keyboard.press('ArrowUp');page.mouse.click(x,y);finish('intentional_parent','parent')
    reset();x,y=coords('#tiny');page.evaluate('start()');page.mouse.move(x,y);page.keyboard.press('ArrowUp');page.keyboard.press('ArrowDown');page.keyboard.press('Enter');finish('keyboard_return_to_child','tiny')
    # Counterexample: eligibility changes after hover, element remains connected & hit target unchanged.
    reset();x,y=coords('#tiny');page.evaluate('start()');page.mouse.move(x,y);page.evaluate("document.querySelector('#tiny').setAttribute('aria-hidden','true')");fresh=page.evaluate("picker.regionCandidates(document.querySelector('#tiny'),document,window).map(e=>e.id)");assert fresh==[],fresh;page.mouse.click(x,y);finish('stale_aria_hidden',None);rows[-1]['fresh_candidates']=fresh
    reset();x,y=coords('#tiny');page.evaluate('start()');page.mouse.move(x,y);page.evaluate("document.querySelector('#parent').setAttribute('contenteditable','true')");fresh=page.evaluate("picker.regionCandidates(document.querySelector('#tiny'),document,window).map(e=>e.id)");assert fresh==[],fresh;page.mouse.click(x,y);finish('stale_editable_ancestor',None);rows[-1]['fresh_candidates']=fresh
    version=browser.version;browser.close()
assert all(r['matches_expected'] for r in rows[:-2]),rows
assert [r['extracted'] for r in rows[-2:]]==([[],[]] if candidate else [['tiny'],['tiny']]),rows
print(json.dumps({'scope':'exact Git blob module in isolated Chromium, fake extraction; no installed extension / production site','git_blob_sha':sha,'scratch_candidate':candidate,'chromium':version,'cases':rows},ensure_ascii=False,indent=2))
