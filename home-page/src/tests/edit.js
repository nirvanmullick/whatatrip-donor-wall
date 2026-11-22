const {chromium}=require('playwright');const fs=require('fs');
const block=fs.readFileSync((process.env.REPO||require('path').resolve(__dirname,'../../..'))+'/home-page/home-block.html','utf8');
const R=(process.env.REPO||require('path').resolve(__dirname,'../../..'))+'/';
const pledge=+(process.argv[2]||114509);
const page=`<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{margin:0;font-family:Georgia,serif;font-size:19px;line-height:1.9;color:#333;background:#fff}
h1,h2,h3{font-family:Georgia,serif;text-transform:uppercase;letter-spacing:.2em;font-size:58px;margin:40px 0;line-height:2}
p{margin:0 0 30px;font-size:22px}a{color:red;text-decoration:underline wavy}
button{font-family:Georgia;text-transform:uppercase;letter-spacing:.3em;border-radius:40px;padding:30px;background:#000;color:#fff}
ul{list-style:square;margin:30px;padding:30px}li{margin:20px 0}table{border:3px solid red}th,td{padding:30px;font-size:30px}
header.sq{position:fixed;top:0;left:0;right:0;height:80px;background:rgba(255,255,255,.9);z-index:10;border-bottom:1px solid #ccc}
.col{max-width:1100px;margin:0 auto;padding:100px 40px 40px}
</style></head><body><header class="sq">SQUARESPACE HEADER</header><div class="col"><div class="code-block">${block}</div></div></body></html>`;
(async()=>{ const b=await chromium.launch(); for(const W of [1300,390]){ const ctx=await b.newContext({viewport:{width:W,height:900}}); const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e).slice(0,300)));
 await ctx.route('**/*',r=>{const u=r.request().url();
  if(u.includes('/macros/'))return r.fulfill({contentType:'application/json',body:JSON.stringify({raised:pledge,goal:500000})});
  if(u.includes('master-donors.json'))return r.fulfill({contentType:'application/json',body:fs.readFileSync(R+'master-donors.json','utf8')});
  if(u.includes('manual.json'))return r.fulfill({contentType:'application/json',body:fs.readFileSync(R+'manual.json','utf8')});
  if(u.includes('wat-donor-count'))return r.fulfill({contentType:'application/json',body:JSON.stringify({donors:281})});
  if(u.startsWith('http://wat.test/'))return r.fulfill({contentType:'text/html',body:page});
  if(u.startsWith('about:')||u.startsWith('data:'))return r.continue(); return r.abort()});
 await p.goto('http://wat.test/?edit=1'); await p.waitForTimeout(900);
 const bar=await p.evaluate(()=>!!window.__watEditBar&&document.querySelector('#wath').isContentEditable);
 // 1 edit a level perk line
 const li=p.locator('#wath-levels .lv li').first(); await li.click(); await p.keyboard.press('End'); await p.keyboard.type(' forever');
 // 2 edit a button label; the click must not open the give panel
 const btn=p.locator('#wath-levels .gorb').first(); await btn.click(); await p.keyboard.press('End'); await p.keyboard.type(' today');
 const opened=await btn.getAttribute('aria-expanded');
 // 3 edit a heading
 const h=p.locator('#wath h2').first(); await h.click(); await p.keyboard.press('End'); await p.keyboard.type('!');
 await p.evaluate(()=>window.__watEditBar.querySelector('[data-show]').click());
 const log=await p.evaluate(()=>JSON.parse(localStorage.getItem('wat-copy-edits-v1')));
 await p.screenshot({path:'edit-'+W+'.png'});
 // editing off: buttons work again
 await p.evaluate(()=>{window.__watEditBar.querySelector('[data-show]').click();window.__watEditBar.querySelector('[data-tog]').click();document.querySelector('#wath-levels .gorb').scrollIntoView({block:'center'})}); await btn.click({timeout:8000}); const opened2=await p.evaluate(()=>document.querySelectorAll('#wath-levels .gor').length+'/'+document.querySelector('#wath-levels .gorb').getAttribute('aria-expanded'));
 const hs=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
 console.log(W,JSON.stringify({bar,opened,opened2,hs,log},null,1),errs); await ctx.close(); } await b.close(); })();
