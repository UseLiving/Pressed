import os
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_markets.py')).read().split("with sync_playwright() as p:")[0]
exec(src)
from playwright.sync_api import sync_playwright
import json
Q=F2=0
def ok2(n,c,d=None):
    global Q,F2
    if c:Q+=1;print('PASS',n)
    else:F2+=1;print('FAIL',n,'|',json.dumps(d,default=str)[:240])
with sync_playwright() as p:
    br=p.chromium.launch();srv=Srv();reqs=[]
    c,pg,errs=new(br,srv,go=False);pg.on('request',lambda r:reqs.append(r.url));pg.wait_for_timeout(600)
    g=pg.evaluate("()=>{var x=document.getElementById('xBtn'),j=[].filter.call(document.querySelectorAll('nav a.btn'),function(a){return /Join the beta/.test(a.textContent)})[0],xr=x.getBoundingClientRect(),jr=j.getBoundingClientRect();return {href:x.href,target:x.target,rel:x.rel,name:x.getAttribute('aria-label'),right:xr.left>=jr.right-1,row:Math.abs((xr.top+xr.bottom)/2-(jr.top+jr.bottom)/2)<6,w:xr.width,h:xr.height,svg:!!x.querySelector('svg'),tag:x.tagName,gap:xr.left-jr.right}}")
    ok2('THE X LINK: an X button sits directly to the RIGHT of "Join the beta" in the header on the same row, and goes to https://x.com/TradePressed in a new tab with noopener',g['href']=='https://x.com/TradePressed' and g['target']=='_blank' and 'noopener' in g['rel'] and g['right'] and g['row'] and g['svg'],g)
    ok2('...it is a real link with the X logo, named for screen readers ("Pressed on X (opens in a new tab)"), at least 40px square',g['tag']=='A' and 'Pressed on X' in g['name'] and 'new tab' in g['name'] and g['h']>=40 and g['w']>=40,g)
    pg.keyboard.press('Tab')
    order=pg.evaluate("()=>{var els=[].slice.call(document.querySelectorAll('a,button,summary,input')).filter(function(e){var r=e.getBoundingClientRect();return r.width>0&&r.height>0});var i=els.indexOf(document.getElementById('xBtn')),j=els.findIndex(function(e){return /Join the beta/.test(e.textContent)&&e.closest('nav')});return j>=0&&i===j+1}")
    ok2('in keyboard order the X link comes straight after "Join the beta"',order)
    ok2('the page makes no request to X (it is only a link)',not any('x.com' in u for u in reqs),[u for u in reqs if 'x.com' in u]);c.close()
    bad=[]
    for w,h,m in ((1360,900,False),(768,1024,True),(560,900,True),(414,896,True),(390,844,True),(360,740,True),(320,640,True)):
        c,pg,errs=new(br,Srv(),vp=(w,h),mobile=m,go=False);pg.wait_for_timeout(300)
        for state in ('disconnected','connected'):
            if state=='connected':
                pg.click('#wSum');pg.wait_for_function("()=>document.getElementById('wSum').textContent.indexOf('7Wkg')>-1",timeout=4000);pg.wait_for_timeout(200)
            g=pg.evaluate("()=>{var x=document.getElementById('xBtn').getBoundingClientRect(),vw=innerWidth,s=document.getElementById('wSum').getBoundingClientRect(),b=document.querySelector('.brand').getBoundingClientRect();return {vis:x.width>0,h:x.height,w:x.width,out:x.right>vw||x.left<0,sw:document.documentElement.scrollWidth,vw:vw,afterWallet:x.left>=s.right-1,overlap:b.right>s.left-2}}")
            if not(g['vis'] and g['h']>=40 and g['w']>=40 and not g['out'] and g['sw']<=w and g['afterWallet'] and not g['overlap']):bad.append((w,state,g))
        c.close()
    ok2('THE X LINK ON EVERY SCREEN (7 widths from 1360 down to 320px, with the wallet disconnected and connected): visible, at least 40px, fully on screen, no sideways scroll, after the wallet button, and never overlapping the logo',not bad,bad[:2])
    c,pg,errs=new(br,Srv(),vp=(320,640),mobile=True,go=False);t=pg.evaluate("()=>document.getElementById('wSum').innerText");ok2('on the narrowest phones the wallet button reads just "Connect" to make room, and the full label is still read out to screen readers',t.strip()=='Connect' and 'wallet' in pg.evaluate("()=>document.getElementById('wSum').textContent"),t);c.close()
    br.close()
print('XSUMMARY: %d/%d passed'%(Q,Q+F2))
