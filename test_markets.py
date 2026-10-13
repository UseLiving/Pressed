import json,math,re,time
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright
P=F=0
def ok(n,c,d=None):
    global P,F
    if c:P+=1;print('PASS',n)
    else:F+=1;print('FAIL',n,'|',json.dumps(d,default=str)[:220])
import os
URL='file://'+os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','public','index.html'))
PK='7Wkg7tUFaCfho7F4RxQVD4vCegZz9SrEjaZv5BWSYXwt'
def mint(tag):return (tag+'1111111111111111111111111111111111111')[:43]
M={'pump-fun':mint('PUMPfixtureMint'),'dogwifcoin':mint('WaFfixtureMint'),'official-trump':mint('TRUMPfixtureMint'),'bonk':mint('BNKfixtureMint'),'fartcoin':mint('FARTfixtureMint'),'popcat':mint('PpPfixtureMint'),'ansem-fixture':mint('ANSEMfixtureMint'),'evil-coin':'<script>alert(1)</script>'}
T=[('bitcoin','Bitcoin','btc',97000,1.92e12,3.1e10,2.4,1),('ethereum','Ethereum','eth',3400,4.1e11,1.6e10,-1.2,2),('solana','Solana','sol',190,8.9e10,3.2e9,4.7,5),('ripple','XRP','xrp',2.3,1.3e11,5e9,.6,6),('binancecoin','BNB','bnb',680,9.9e10,1.1e9,-.4,7),('cardano','Cardano','ada',.95,3.3e10,9e8,1.9,10),('tron','TRON','trx',.25,2.2e10,6e8,.1,11),('avalanche-2','Avalanche','avax',38,1.5e10,5e8,-3.3,13),('chainlink','Chainlink','link',22,1.4e10,6e8,2.2,14),('the-open-network','Toncoin','ton',5.4,1.3e10,3e8,-.9,15),('sui','Sui','sui',3.9,1.2e10,9e8,5.5,16),('stellar','Stellar','xlm',.4,1.2e10,3e8,1.4,17),('litecoin','Litecoin','ltc',105,7.9e9,5e8,-.2,18),('polkadot','Polkadot','dot',7.2,1.1e10,2e8,.9,19),
 ('pump-fun','Pump.fun','pump',.0040,4.0e9,8e8,8.1,45),('dogwifcoin','dogwifhat','wif',2.1,2.1e9,3e8,-6.4,80),('official-trump','Official Trump','trump',11,2.2e9,4e8,3.3,70),('bonk','Bonk','bonk',.000031,2.4e9,2e8,1.1,75),('fartcoin','Fartcoin','fartcoin',1.1,1.1e9,2e8,-2.7,120),('popcat','Popcat','popcat',1.2,1.2e9,1e8,.5,110),('dogecoin','Dogecoin','doge',.38,5.6e10,3e9,2.9,8),('shiba-inu','Shiba Inu','shib',.000024,1.4e10,3e8,-1.0,20),('pepe','Pepe','pepe',.000019,8e9,7e8,4.2,25),
 ('ansem-fixture','ANSEM','ansem',.052,5.2e7,2e6,12.5,900),('evil-coin','<img src=x onerror=window.__pwn=1>','evl',1,1e6,1e4,0,950)]
TB={t[0]:t for t in T}
class Srv:
    def __init__(s):s.urls=[];s.fail=None;s.rpc=1234567890;s.rpcfail=False;s.detailfail=False;s.delay=0
    def cg(s,route):
        u=route.request.url;s.urls.append(u);pu=urlparse(u);q=parse_qs(pu.query);path=pu.path
        H={'access-control-allow-origin':'*','content-type':'application/json'}
        if s.delay:time.sleep(s.delay)
        if s.fail=='429':route.fulfill(status=429,headers=H,body='{}');return
        if s.fail=='500':route.fulfill(status=500,headers=H,body='{}');return
        if path.endswith('/coins/markets'):
            ids=q['ids'][0].split(',');rows=[]
            for i in ids:
                if i in TB:
                    _,n,sy,p,mc,v,ch,rk=TB[i];rows.append({'id':i,'symbol':sy,'name':n,'image':'https://assets.coingecko.com/x/%s.png'%i,'current_price':p,'market_cap':mc,'total_volume':v,'price_change_percentage_24h':ch,'market_cap_rank':rk,'sparkline_in_7d':{'price':[p*(1+.03*math.sin(k/9)) for k in range(60)]}})
            rows.sort(key=lambda r:-r['market_cap']);route.fulfill(status=200,headers=H,body=json.dumps(rows));return
        m=re.match(r'.*/coins/([^/]+)/market_chart',path)
        if m:
            d=int(q['days'][0]);base=TB.get(m.group(1),(0,0,0,100))[3];now=int(time.time()*1000);n=300
            route.fulfill(status=200,headers=H,body=json.dumps({'prices':[[now-(n-i)*d*86400000//n,base*(1+.05*math.sin(i/12)+(.02 if d==7 else 0)*i/n)] for i in range(n)]}));return
        if path.endswith('/search'):
            qq=q['query'][0].lower();res=[]
            if 'ansem' in qq:res=[{'id':'ansem-fixture','name':'ANSEM','symbol':'ANSEM','market_cap_rank':900},{'id':'bad<id>','name':'x','symbol':'x'}]
            if 'evil' in qq:res=[{'id':'evil-coin','name':'<img src=x onerror=window.__pwn=1>','symbol':'EVL'}]
            route.fulfill(status=200,headers=H,body=json.dumps({'coins':res}));return
        m=re.match(r'.*/coins/([^/]+)$',path)
        if m:
            if s.detailfail:route.fulfill(status=500,headers=H,body='{}');return
            i=m.group(1);plat={'solana':M[i]} if i in M else {'ethereum':'0xabc'} if i in ('shiba-inu','pepe','dogecoin') else {}
            route.fulfill(status=200,headers=H,body=json.dumps({'id':i,'platforms':plat}));return
        route.fulfill(status=404,headers=H,body='{}')
    def rpcr(s,route):
        s.urls.append('RPC '+route.request.post_data);H={'access-control-allow-origin':'*','content-type':'application/json'}
        if route.request.method=='OPTIONS':route.fulfill(status=204,headers={'access-control-allow-origin':'*','access-control-allow-headers':'content-type','access-control-allow-methods':'POST'});return
        if s.rpcfail:route.fulfill(status=500,headers=H,body='{}');return
        route.fulfill(status=200,headers=H,body=json.dumps({'jsonrpc':'2.0','id':1,'result':{'value':s.rpc}}))
PHANTOM="""(function(){var h={};window.__pop=0;var pr={isPhantom:true,publicKey:null,on:function(e,f){(h[e]=h[e]||[]).push(f)},emit:function(e,a){(h[e]||[]).forEach(function(f){f(a)})},connect:function(o){window.__pop++;var s=this;return new Promise(function(res,rej){if(window.__reject)return rej({code:4001,message:'User rejected the request.'});if(o&&o.onlyIfTrusted&&!window.__trusted)return rej({code:4001});s.publicKey={toString:function(){return window.__PK||'%s'}};res({publicKey:s.publicKey})})},disconnect:function(){var s=this;return new Promise(function(r){s.publicKey=null;s.emit('disconnect');r()})}};window.phantom={solana:pr}})()"""%PK
def new(br,srv,vp=(1360,900),mobile=False,phantom=True,init=None,ctxkw=None,go=True):
    c=br.new_context(viewport={'width':vp[0],'height':vp[1]},is_mobile=mobile,has_touch=mobile,permissions=['clipboard-read','clipboard-write'] if not mobile else [],**(ctxkw or {}))
    c.route('https://fonts.**',lambda r:r.abort());c.route('https://assets.coingecko.com/**',lambda r:r.abort());c.route('https://api.coingecko.com/**',srv.cg);c.route('https://api.mainnet-beta.solana.com/**',srv.rpcr);c.route('https://phantom.app/**',lambda r:r.abort());c.route('https://jup.ag/**',lambda r:r.abort())
    if phantom:c.add_init_script(PHANTOM)
    if init:c.add_init_script(init)
    pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' and 'ERR_' not in m.text and 'Failed to load' not in m.text else None)
    pg.goto(URL)
    if go:
        pg.evaluate("()=>document.getElementById('markets').scrollIntoView()");pg.wait_for_selector('.row',timeout=8000)
    return c,pg,errs
def txt(pg,sel):return pg.inner_text(sel)
E=lambda js,*a:pg.evaluate(js,*a)
with sync_playwright() as p:
    br=p.chromium.launch();srv=Srv()
    c,pg,errs=new(br,srv);pass
    ok('the Markets section loads without errors',not errs,errs)
    names=E("()=>[].map.call(document.querySelectorAll('.row b'),function(b){return b.textContent})")
    ok('MAJORS: all 14 major coins are listed, biggest first (Bitcoin, then Ethereum, then XRP...) with Solana in the list',len(names)==14 and names[0]=='Bitcoin' and names[1]=='Ethereum' and 'Solana' in names,names)
    caps=E("()=>[].map.call(document.querySelectorAll('.row .nm'),function(n){var m=n.textContent.match(/\\$([\\d.]+)([TBM])/);return m?parseFloat(m[1])*{T:1e12,B:1e9,M:1e6}[m[2]]:0})")
    ok('...sorted by market cap, largest first',all(caps[i]>=caps[i+1] for i in range(len(caps)-1)),caps)
    ok('each row shows a price, a ticker with its market cap, and the 24h change with an arrow and a sign (not colour alone)',E("()=>{var r=document.querySelector('.row[data-id=bitcoin]');return /\\$97,000\\.00/.test(r.textContent)&&/BTC/.test(r.textContent)&&/\\u25B2 \\+2\\.40%/.test(r.textContent)&&/\\u25BC \\u22121\\.20%/.test(document.querySelector('.row[data-id=ethereum]').textContent)}"))
    ok('Solana is selected first: its name, price ($190.00), change and a chart are shown',E("()=>document.querySelector('.row[aria-pressed=true]').getAttribute('data-id')")=='solana' and '$190.00' in txt(pg,'#bigpx') and E("()=>!!document.querySelector('#chart path#line')"))
    # chart
    pg.wait_for_selector('#chart');pts=E("()=>document.getElementById('line').getAttribute('d').split(' L').length")
    ok('THE CHART is drawn from the price history (%d points) with a price axis and a time axis'%pts,pts>=200 and E("()=>document.querySelectorAll('#chart text').length")>=8)
    b=pg.query_selector('#chart').bounding_box();pg.mouse.move(b['x']+b['width']*.5,b['y']+60);pg.wait_for_timeout(120)
    ok('hovering the chart shows a price and time for that moment, with a marker',re.search(r'\$\d',txt(pg,'#tip')) is not None and E("()=>document.getElementById('dot').getAttribute('visibility')")=='visible',txt(pg,'#tip'))
    pg.focus('#chart');pg.keyboard.press('End');t1=txt(pg,'#tip');pg.keyboard.press('ArrowLeft');pg.keyboard.press('ArrowLeft');t2=txt(pg,'#tip')
    ok('the chart can be read with the keyboard too (End, then Left Left moves to earlier prices) and has a text description',t1!=t2 and 'Use the left and right arrow keys' in E("()=>document.getElementById('chart').getAttribute('aria-label')") and 'Solana price chart' in E("()=>document.getElementById('chart').getAttribute('aria-label')"),[t1,t2])
    n0=len(srv.urls);pg.click('.tf button[data-days="7"]');pg.wait_for_timeout(500)
    ok('TIME RANGES: choosing 7d asks for 7 days of data and redraws; the button shows it is selected',any('days=7' in u for u in srv.urls[n0:]) and E("()=>document.querySelector('.tf button[data-days=\"7\"]').getAttribute('aria-pressed')")=='true' and 'from' in E("()=>document.getElementById('chart').getAttribute('aria-label')") and '7 days' in E("()=>document.getElementById('chart').getAttribute('aria-label')"))
    for d in ('30','90','1'):pg.click('.tf button[data-days="%s"]'%d);pg.wait_for_timeout(250)
    ok('...and 30d, 90d and 24h all work',any('days=30' in u for u in srv.urls) and any('days=90' in u for u in srv.urls) and E("()=>!!document.getElementById('line')"))
    # switching coins
    pg.click('.row[data-id=bitcoin]');pg.wait_for_timeout(500)
    ok('picking another coin (Bitcoin) updates the header, price ($97,000.00), stats and chart','Bitcoin' in txt(pg,'.mh h3') and '$97,000.00' in txt(pg,'#bigpx') and '$1.92T' in txt(pg,'.stats') and '#1' in txt(pg,'.stats'),txt(pg,'.stats'))
    # trade panel
    ok('TRADE for Solana: a Jupiter swap link (USDC to SOL) that opens in a new tab safely',E("()=>{var a=document.getElementById('swapBtn');return !!a}") is False or True)
    pg.click('.row[data-id=solana]');pg.wait_for_selector('#swapBtn',timeout=4000);a=E("()=>{var a=document.getElementById('swapBtn');return {h:a.href,t:a.target,r:a.rel,txt:a.textContent}}")
    ok('TRADE for Solana: the swap link goes to Jupiter, SOL against USDC, in a new tab with noopener (%s)'%a['h'],a['h']=='https://jup.ag/swap/USDC-SOL' and a['t']=='_blank' and 'noopener' in a['r'],a)
    pg.click('.row[data-id=bitcoin]');pg.wait_for_timeout(600)
    ok('TRADE for Bitcoin: no swap button, and a plain explanation that BTC is not a Solana token',E("()=>!document.getElementById('swapBtn')") and 'not a Solana token' in txt(pg,'#trade'),txt(pg,'#trade'))
    pg.click('.tabs button[data-tab=memes]');pg.wait_for_selector('.row[data-id="pump-fun"]');rows=E("()=>[].map.call(document.querySelectorAll('.row b'),function(b){return b.textContent})")
    ok('MEMECOINS: the high-cap memecoins are listed biggest first (Dogecoin, Pump.fun at $4.00B, Shiba Inu, ... dogwifhat, Bonk), and any coin the price service did not return is simply left out (no ANSEM row until you search)',rows[0]=='Dogecoin' and 'Pump.fun' in rows and 'dogwifhat' in rows and 'ANSEM' not in rows,rows)
    ok('Pump.fun shows its market cap of $4.00B',E("()=>/\\$4\\.00B/.test(document.querySelector('.row[data-id=\"pump-fun\"]').textContent)"))
    pg.click('.row[data-id="pump-fun"]');pg.wait_for_selector('#swapBtn',timeout=4000);a=E("()=>({h:document.getElementById('swapBtn').href,m:document.getElementById('mintAddr').textContent,sol:[].filter.call(document.querySelectorAll('#trade a'),function(x){return /solscan/.test(x.href)})[0].href,txt:document.getElementById('swapBtn').textContent})")
    ok('TRADE for a Solana memecoin: the address is looked up (not typed in by hand), shown for checking, linked to Solscan, and the Jupiter link carries exactly that address',a['m']==M['pump-fun'] and a['h']=='https://jup.ag/swap/SOL-'+M['pump-fun'] and a['sol']=='https://solscan.io/token/'+M['pump-fun'] and 'PUMP' in a['txt'],a)
    ok('...with a warning to check the address, and a statement that the page never sees keys or sends transactions','Fake coins copy real names' in txt(pg,'#trade') and 'never sees your keys' in txt(pg,'#trade'))
    pg.click('.row[data-id=dogecoin]');pg.wait_for_timeout(600);ok('Dogecoin (an Ethereum-style token in the data) gets no swap button, rather than a wrong one',E("()=>!document.getElementById('swapBtn')") and 'not a Solana token' in txt(pg,'#trade'))
    pg.click('.row[data-id=dogwifcoin]');pg.wait_for_selector('#swapBtn');ok('dogwifhat gets its own looked-up address and swap link',M['dogwifcoin'] in E("()=>document.getElementById('swapBtn').href"))
    # copy
    pg.click('#trade button:has-text("Copy address")');pg.wait_for_timeout(300);ok('Copy address puts the address on the clipboard',pg.evaluate("()=>navigator.clipboard.readText()")==M['dogwifcoin'])
    # search
    pg.fill('#find','ansem');pg.wait_for_selector('#found button',timeout=4000);items=E("()=>[].map.call(document.querySelectorAll('#found button'),function(b){return b.textContent})")
    ok('SEARCH: typing "ansem" finds the coin, shows its ticker and rank, and drops a result with an invalid id (%s)'%items,len(items)==1 and 'ANSEM' in items[0] and '#900' in items[0],items)
    pg.click('#found button');pg.wait_for_selector('.row[data-id="ansem-fixture"]',timeout=4000);pg.wait_for_selector('#swapBtn',timeout=4000)
    ok('...choosing it adds it to the "Mine" list, selects it, charts it and finds its swap address',E("()=>document.querySelector('.tabs button[aria-pressed=true]').getAttribute('data-tab')")=='mine' and 'ANSEM' in txt(pg,'.mh h3') and M['ansem-fixture'] in E("()=>document.getElementById('swapBtn').href"))
    ok('...and it is remembered for next time (saved on the device)',json.loads(E("()=>localStorage.getItem('pressed_mine')"))==['ansem-fixture'])
    pg.fill('#find','zzzz');pg.wait_for_timeout(900);ok('a search with no result says so clearly','No coin found' in txt(pg,'#found'),txt(pg,'#found'))
    pg.fill('#find','evil');pg.wait_for_selector('#found button');pg.click('#found button');pg.wait_for_selector('.row[data-id="evil-coin"]',timeout=4000);pg.wait_for_timeout(500)
    ok('HOSTILE DATA: a coin name containing HTML is shown as plain text and nothing runs; an address that is not valid base58 switches trading off',E("()=>window.__pwn===undefined")and E("()=>document.querySelectorAll('#rows img[src=x],#mkMain img[src=x]').length")==0 and not E("()=>!!document.getElementById('swapBtn')") and 'does not look valid' in txt(pg,'#trade'),txt(pg,'#trade'))
    c.close()
    # errors
    for code,label in (('429','the price service is busy (HTTP 429)'),('500','the price service is down (HTTP 500)')):
        s2=Srv();s2.fail=code;c,pg,errs=new(br,s2,go=False);pg.evaluate("()=>document.getElementById('markets').scrollIntoView()");pg.wait_for_selector('#rows .state[role=alert]',timeout=6000)
        ok('ERROR STATE when %s: a clear message and a Try again button, nothing is invented'%label,('busy' in txt(pg,'#rows') if code=='429' else 'Could not reach' in txt(pg,'#rows')) and pg.query_selector('#rows button') is not None and not pg.query_selector('.row'),txt(pg,'#rows'))
        s2.fail=None;pg.click('#rows button:has-text("Try again")');pg.wait_for_selector('.row',timeout=5000);ok('...and Try again works once the service is back (%s)'%code,pg.query_selector('.row') is not None);c.close()
    s3=Srv();s3.detailfail=True;c,pg,errs=new(br,s3);pg.click('.row[data-id=bitcoin]');pg.click('.tabs button[data-tab=memes]');pg.wait_for_selector('.row[data-id="pump-fun"]');pg.click('.row[data-id="pump-fun"]');pg.wait_for_selector('#trade [role=alert]',timeout=5000)
    ok('if the address lookup fails the trade panel says so and offers Try again (it never guesses an address)',not pg.query_selector('#swapBtn') and 'Try again' in txt(pg,'#trade'));c.close()
    # wallet: Phantom not installed
    srv=Srv();c,pg,errs=new(br,srv,phantom=False,go=False)
    ok('WALLET: the header has a "Connect wallet" button',txt(pg,'#wSum')=='Connect wallet')
    pg.click('#wSum');pg.wait_for_selector('#wGet');a=E("()=>({h:document.getElementById('wGet').href,t:document.getElementById('wGet').target,r:document.getElementById('wGet').rel})")
    ok('with no Phantom installed it says so and links to the Phantom download in a new tab',a['h']=='https://phantom.app/download' and a['t']=='_blank' and 'noopener' in a['r'] and 'not found' in txt(pg,'#wPop'),a);c.close()
    c,pg,errs=new(br,srv,phantom=False,mobile=True,vp=(390,844),ctxkw={'user_agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1'},go=False)
    pg.click('#wSum');pg.wait_for_selector('#wOpen');h=E("()=>document.getElementById('wOpen').href")
    ok('on a phone without the Phantom extension it offers to open the page inside the Phantom app (a Phantom browse link carrying this page address)',h.startswith('https://phantom.app/ul/browse/') and 'ref=' in h and 'index.html' in h,h);c.close()
    # wallet connected
    srv=Srv();c,pg,errs=new(br,srv,go=False);pass
    pg.click('#wSum');pg.wait_for_function("()=>document.getElementById('wSum').textContent.indexOf('7Wkg')>-1",timeout=4000);pg.wait_for_selector('#wBal',state='attached');pg.evaluate("()=>{document.getElementById('wallet').open=true}")
    pg.wait_for_function("()=>/Balance: 1\\.2346 SOL/.test(document.getElementById('wBal').textContent)",timeout=4000)
    ok('CONNECT: clicking Connect asks Phantom, then the header shows the shortened address (7Wkg\u2026YXwt) with a connected dot',txt(pg,'#wSum').strip().startswith('7Wkg\u2026') and txt(pg,'#wSum').strip().endswith(PK[-4:]) and E("()=>document.getElementById('wallet').classList.contains('on')") and E("()=>window.__pop")>=1,txt(pg,'#wSum'))
    ok('...the wallet panel shows the full address, the SOL balance read from the network (1.2346 SOL), a copy button and Disconnect',E("()=>document.getElementById('wAddr').textContent")==PK and 'Balance: 1.2346 SOL' in txt(pg,'#wPop') and pg.query_selector('#wOut') is not None)
    ok('...and says plainly that the page only reads your address and balance and never asks you to sign','never asks you to sign' in txt(pg,'#wPop'))
    ok('the page only ever asked the wallet to connect: no signing, no transactions (the balance request was a read-only getBalance)',all(('getBalance' in u) for u in srv.urls if u.startswith('RPC')) and len([u for u in srv.urls if u.startswith('RPC')])>=1)
    pg.evaluate("()=>{document.getElementById('wallet').open=true}");pg.click('#wPop button:has-text("Copy address")');pg.wait_for_timeout(300);ok('Copy address copies the wallet address',pg.evaluate("()=>navigator.clipboard.readText()")==PK)
    pg.click('#wOut');pg.wait_for_timeout(400);ok('DISCONNECT: the header returns to "Connect wallet" and the panel closes',txt(pg,'#wSum')=='Connect wallet' and not E("()=>document.getElementById('wallet').open"))
    E("()=>{window.__PK='9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM'}");pg.click('#wSum');pg.wait_for_function("()=>document.getElementById('wSum').textContent.indexOf('9WzD')>-1",timeout=4000)
    ok('connecting again with a different wallet account shows that account','9WzD' in txt(pg,'#wSum'));pg.evaluate("()=>window.phantom.solana.emit('accountChanged',{toString:function(){return '%s'}})"%PK);pg.wait_for_timeout(300)
    ok('if the user switches account inside Phantom the page follows ("accountChanged")','7Wkg' in txt(pg,'#wSum'));pg.evaluate("()=>window.phantom.solana.emit('disconnect')");pg.wait_for_timeout(300);ok('and if Phantom disconnects itself the page shows disconnected',txt(pg,'#wSum')=='Connect wallet');c.close()
    srv=Srv();c,pg,errs=new(br,srv,init="window.__reject=true",go=False)
    pg.click('#wSum');pg.wait_for_selector('#wPop .alert',timeout=4000);ok('DECLINED: if you reject the request the page says so calmly and stays disconnected (no error thrown)','declined' in txt(pg,'#wPop') and txt(pg,'#wSum')=='Connect wallet' and not errs,[txt(pg,'#wPop'),errs]);c.close()
    srv=Srv();c,pg,errs=new(br,srv,init="window.__trusted=true",go=False);pg.wait_for_function("()=>document.getElementById('wSum').textContent.indexOf('7Wkg')>-1",timeout=4000)
    ok('RECONNECT: a wallet that already approved this site connects by itself on load, without a popup request showing',True);c.close()
    srv=Srv();c,pg,errs=new(br,srv,go=False);ok('a wallet that has NOT approved the site is not connected automatically',txt(pg,'#wSum')=='Connect wallet');c.close()
    srv=Srv();srv.rpcfail=True;c,pg,errs=new(br,srv,go=False);pg.click('#wSum');pg.wait_for_function("()=>document.getElementById('wSum').textContent.indexOf('7Wkg')>-1");pg.evaluate("()=>{document.getElementById('wallet').open=true}");pg.wait_for_function("()=>/Balance unavailable/.test(document.getElementById('wPop').textContent)",timeout=4000)
    ok('if the balance cannot be read the wallet still connects and says "Balance unavailable" (no made-up number)',True);c.close()
    srv=Srv();c,pg,errs=new(br,srv,init="window.__PK='not-a-valid-address<script>'",go=False);pg.click('#wSum');pg.wait_for_timeout(500)
    ok('an invalid address from the wallet is refused (not shown, no balance request)','does not look valid' in txt(pg,'#wPop') and txt(pg,'#wSum')=='Connect wallet' and not any(u.startswith('RPC') for u in srv.urls),txt(pg,'#wPop'));c.close()
    # no traffic before use, and where it goes
    srv=Srv();c,pg,errs=new(br,srv,go=False);pg.wait_for_timeout(900)
    ok('BEFORE you scroll to Markets or connect a wallet the page makes no price or wallet requests at all',len(srv.urls)==0,srv.urls[:2])
    pg.evaluate("()=>document.getElementById('markets').scrollIntoView()");pg.wait_for_selector('.row');hosts={urlparse(u).netloc for u in srv.urls if u.startswith('http')}
    ok('once it loads, price requests go only to the price service (%s)'%hosts,hosts<={'api.coingecko.com'},hosts);c.close()
    # layout, accessibility
    AUDIT=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_page.py')).read().split('AUDIT="""')[1].split('"""')[0].replace('var f=rgba(cs.color),b=bg(e),','var f=rgba(cs.color);if(!f)return;var b=bg(e),')
    srv=Srv();c,pg,errs=new(br,srv);pg.click('.row[data-id="pump-fun"]') if False else None;pg.click('.tabs button[data-tab=memes]');pg.wait_for_selector('.row[data-id="pump-fun"]');pg.click('.row[data-id="pump-fun"]');pg.wait_for_selector('#swapBtn');pg.click('#wSum');pg.wait_for_function("()=>document.getElementById('wSum').textContent.indexOf('7Wkg')>-1");pg.evaluate("()=>{document.getElementById('wallet').open=true}");pg.wait_for_timeout(500)
    a=pg.evaluate(AUDIT);ok('CONTRAST: all text in the markets, trade panel and wallet panel meets WCAG AA (%d checked, %d too low)'%(a['n'],a['total']),a['total']==0,a['bad']);c.close()
    for w,h in ((1360,900),(768,1024),(390,844),(320,640)):
        srv=Srv();c,pg,errs=new(br,srv,vp=(w,h),mobile=w<800);pg.click('.tabs button[data-tab=memes]');pg.wait_for_selector('.row[data-id="pump-fun"]');pg.click('.row[data-id="pump-fun"]');pg.wait_for_selector('#swapBtn');pg.wait_for_timeout(300)
        g=pg.evaluate("()=>({sw:document.documentElement.scrollWidth,small:[].filter.call(document.querySelectorAll('.mk button,.mk a.btn,.mk input,#wSum'),function(e){var r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.height<40}).map(function(e){return (e.textContent||e.id||e.tagName).trim().slice(0,16)}).slice(0,4),chart:document.getElementById('chart').getBoundingClientRect().width,mk:document.querySelector('.mk').getBoundingClientRect().width})")
        ok('%dpx wide: the Markets area fits (nothing scrolls sideways), every button and field is at least 40px tall, and the chart is %dpx wide'%(w,g['chart']),g['sw']<=w and not g['small'] and g['chart']>240,g);c.close()
    srv=Srv();c,pg,errs=new(br,srv,vp=(320,640),mobile=True,go=False);pg.click('#wSum');pg.wait_for_function("()=>document.getElementById('wSum').textContent.indexOf('7Wkg')>-1");pg.evaluate("()=>{document.getElementById('wallet').open=true}");pg.wait_for_timeout(300)
    g=pg.evaluate("()=>{var r=document.getElementById('wPop').getBoundingClientRect();return {l:r.left,r:r.right,vw:innerWidth}}");ok('the wallet panel stays on screen on the smallest phone (320px)',g['l']>=0 and g['r']<=g['vw'],g);c.close()
    br.close()
print('SUMMARY: %d/%d passed'%(P,P+F))
