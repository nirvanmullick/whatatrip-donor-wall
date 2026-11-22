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
  if(u.startsWith('about:')||u.startsWith('data:'))return r.continue(); return r.abort()});
 await p.setContent(page); await p.waitForTimeout(900);
 const el=await p.$('#wath-levels'); const info=await p.evaluate(()=>{const L=document.querySelector('#wath-levels');return {cls:L.className,n:L.querySelectorAll('.lv').length,hs:document.documentElement.scrollWidth-innerWidth}});
 await el.screenshot({path:'lv-'+W+'.png'}); console.log(W,JSON.stringify(info),errs); await ctx.close(); } await b.close(); })();
