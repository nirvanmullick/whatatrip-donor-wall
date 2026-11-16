const {chromium}=require('/opt/npm-tools/node_modules/playwright');const fs=require('fs');
const block=fs.readFileSync('/home/claude/whatatrip-donor-wall/home-page/home-block.html','utf8');
const R='/home/claude/whatatrip-donor-wall/';
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
 const txt=await p.evaluate(()=>({hero:document.querySelector('#wath [data-hero]').innerText.replace(/\n+/g,' | '),match:document.querySelector('#wath [data-matchline]').innerText,sup:document.querySelector('#wath [data-supcount]').innerText,top:[...document.querySelectorAll('#wath-recent .dn')].slice(0,10).map(d=>d.innerText.replace(/\n+/g,' ')),ch:[...document.querySelectorAll('#wath [data-challenges] .ch')].map(d=>d.innerText.replace(/\n+/g,' ').slice(0,90)),bud:document.querySelector('#wath [data-budget]').innerText.replace(/\n+/g,' | ').slice(0,420),hs:document.documentElement.scrollWidth-innerWidth}));
 await p.screenshot({path:'hm-'+W+'.png',fullPage:true});
 await p.click('#wath-recent [data-sup=recent]'); const rec=await p.evaluate(()=>[...document.querySelectorAll('#wath-recent .dn')].slice(0,4).map(d=>d.innerText.replace(/\n+/g,' ')));
 const com=await p.evaluate(()=>[...document.querySelectorAll('#wath-comments .dn .when')].slice(0,4).map(d=>d.innerText));
 await p.click('#wath [data-chart]'); await p.waitForTimeout(200); await p.screenshot({path:'hm-'+W+'-chart.png'}); await p.keyboard.press('Escape');
 if(W===1300)console.log(JSON.stringify({txt,rec,com},null,1)); console.log(W,'hscroll',txt.hs,errs); await ctx.close(); } await b.close(); })();
