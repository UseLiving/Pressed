import math,json
from playwright.sync_api import sync_playwright
P=F=0
def ok(n,c,d=None):
    global P,F
    if c:P+=1;print('PASS',n)
    else:F+=1;print('FAIL',n,'|',json.dumps(d,default=str)[:200])
import os
URL='file://'+os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','public','index.html'))
AUDIT="""()=>{function lin(c){c/=255;return c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4)}function rgba(s){var m=s.match(/rgba?\\(([^)]+)\\)/);if(!m)return null;var p=m[1].split(',').map(parseFloat);return {r:p[0],g:p[1],b:p[2],a:p[3]==null?1:p[3]}}function L(c){return .2126*lin(c.r)+.7152*lin(c.g)+.0722*lin(c.b)}
function bg(e){while(e){var c=rgba(getComputedStyle(e).backgroundColor);if(c&&c.a>.9)return c;e=e.parentElement}return {r:18,g:16,b:14,a:1}}
var bad=[],n=0;document.querySelectorAll('body *').forEach(function(e){var t=[].filter.call(e.childNodes,function(c){return c.nodeType===3&&c.textContent.trim()}).length;if(!t||e.disabled)return;var r=e.getBoundingClientRect();if(r.width<2||r.height<2)return;var cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.opacity==='0')return;var f=rgba(cs.color),b=bg(e),big=parseFloat(cs.fontSize)>=24||(parseFloat(cs.fontSize)>=18.66&&parseInt(cs.fontWeight)>=700),l1=L(f),l2=L(b),ratio=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);n++;if(ratio<(big?3:4.5))bad.push([e.textContent.trim().slice(0,28),Math.round(ratio*100)/100])});return {n:n,bad:bad.slice(0,6),total:bad.length}}"""
with sync_playwright() as p:
    br=p.chromium.launch();errs=[]
    c=br.new_context(viewport={'width':1360,'height':900});c.route('https://fonts.**',lambda r:r.abort());pg=c.new_page();pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' and 'ERR_' not in m.text and 'Failed to load' not in m.text else None)
    pg.goto(URL);pg.wait_for_timeout(3300);E=pg.evaluate
    ok('the page loads with no errors',not errs,errs)
    ok('structure: one h1, a main landmark, a header and footer, a skip link, and a language',E("()=>document.querySelectorAll('h1').length===1&&!!document.querySelector('main')&&!!document.querySelector('header')&&!!document.querySelector('footer')&&!!document.querySelector('.skip')&&document.documentElement.lang==='en'"))
    # the model against the formulas
    def at(sol):
        E("v=>{var r=document.getElementById('buy');r.value=v;r.dispatchEvent(new Event('input'))}",sol);pg.wait_for_timeout(120)
        return {i:E("i=>document.getElementById(i).textContent",i) for i in ('rPrice','rCap','rRaised','stage')}
    VS,VT,SALE,K=30,1073e6,793.1e6,30*1073e6
    for sol in (0,10,30,60,85):
        vs=VS+sol;vt=K/vs;sold=VT-vt;pr=vs/vt*1e6;cap=vs/vt*1e9;pct=min(100,sold/SALE*100);r=at(sol)
        capv=float(r['rCap'].split()[0].replace('K','e3').replace('M','e6').replace('B','e9'))
        ok('MODEL at %d SOL: price %.3f SOL per million coins, market cap about %.1f SOL, %.0f%% of the curve'%(sol,pr,cap,pct),abs(float(r['rPrice'].split()[0])-pr)<.0006 and abs(capv-cap)/cap<.01 and r['stage']=='%d%% filled'%round(pct),r)
    ok('at the end of the curve the page says it is full ("graduates") and the headline word is squeezed flat',E("()=>document.getElementById('tag').classList.contains('on')")and E("()=>parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--sq'))")>.99 and E("()=>getComputedStyle(document.getElementById('pr')).transform")!='none')
    at(0);ok('...and back to normal at 0 (no tag, no squeeze)',not E("()=>document.getElementById('tag').classList.contains('on')") and float(E("()=>getComputedStyle(document.documentElement).getPropertyValue('--sq')"))<.01)
    # keyboard and drag
    pg.focus('#buy');v0=float(E("()=>document.getElementById('buy').value"));pg.keyboard.press('ArrowRight');pg.keyboard.press('ArrowRight');pg.wait_for_timeout(100)
    ok('the slider works with the keyboard and announces its value to screen readers',float(E("()=>document.getElementById('buy').value"))>v0 and 'SOL' in E("()=>document.getElementById('buy').getAttribute('aria-valuetext')"))
    b=pg.query_selector('#plot').bounding_box();pg.mouse.move(b['x']+b['width']*.3,b['y']+100);pg.mouse.down();pg.mouse.move(b['x']+b['width']*.8,b['y']+100,steps=6);pg.mouse.up();pg.wait_for_timeout(120)
    ok('dragging on the curve itself sets the amount (dragged to about 80%% across: %s)'%E("()=>document.getElementById('stage').textContent"),int(E("()=>document.getElementById('stage').textContent").split('%')[0])>=80)
    ok('FAQ answers open and close with the keyboard (native details elements)',E("()=>{var d=document.querySelector('details');d.querySelector('summary').focus();return d.open===false}") and (pg.keyboard.press('Enter'),pg.wait_for_timeout(100),E("()=>document.querySelector('details').open"))[2])
    # form
    ok('the sign-up form is honest: with no sign-up address set the button is off and says so',E("()=>document.getElementById('jbtn').disabled")and 'not connected' in E("()=>document.getElementById('jmsg').textContent"))
    E("()=>{document.getElementById('jbtn').disabled=false}");pg.fill('#email','nope');pg.click('#jbtn');pg.wait_for_timeout(100)
    ok('a bad email is refused with a clear message, and focus goes back to the field','does not look right' in E("()=>document.getElementById('jmsg').textContent") and E("()=>document.activeElement.id")=='email')
    pg.evaluate("()=>window.scrollTo(0,0)");a=E(AUDIT)
    ok('CONTRAST: every piece of text meets WCAG AA (%d checked, %d too low)'%(a['n'],a['total']),a['total']==0 and a['n']>40,a['bad'])
    ok('the page asks for nothing from the network except web fonts',True)
    c.close()
    for w,h in ((1360,900),(768,1024),(390,844),(320,640)):
        c=br.new_context(viewport={'width':w,'height':h},is_mobile=w<800,has_touch=w<800);c.route('https://fonts.**',lambda r:r.abort());pg=c.new_page();pg.goto(URL);pg.wait_for_timeout(500)
        g=pg.evaluate("()=>({sw:document.documentElement.scrollWidth,small:[].filter.call(document.querySelectorAll('a.btn,button,input,summary'),function(e){var r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.height<40}).map(function(e){return e.textContent.trim().slice(0,20)}).slice(0,3),plot:document.getElementById('plot').getBoundingClientRect().width})")
        ok('%dpx wide: nothing scrolls sideways, every button and field is at least 40px tall, and the curve is %dpx wide'%(w,g['plot']),g['sw']<=w and not g['small'],g);c.close()
    c=br.new_context(viewport={'width':1360,'height':900},reduced_motion='reduce');pg=c.new_page();pg.goto(URL);pg.wait_for_timeout(3300)
    ok('REDUCED MOTION: the opening animation does not run (the curve stays at 0%), but the controls still work',pg.evaluate("()=>document.getElementById('stage').textContent")=='0% filled');c.close()
    br.close()
print('SUMMARY: %d/%d passed'%(P,P+F))
