const {chromium}=require('/opt/npm-tools/node_modules/playwright');const fs=require('fs');
const block=fs.readFileSync('/home/claude/whatatrip-donor-wall/home-page/home-block.html','utf8');const ph=fs.readFileSync('/tmp/ph.png');
const html='<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0"><header id="header"><div class="header-nav-list"><div class="header-nav-item"><a href="/about">About</a></div></div></header><div>'+block+'</div></body></html>';
(async()=>{const b=await chromium.launch();for(const W of [1440,390]){const ctx=await b.newContext({viewport:{width:W,height:900}});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(String(e).slice(0,200)));
await ctx.route('**/*',r=>{const u=r.request().url();if(u==='http://test.local/')return r.fulfill({contentType:'text/html',body:html});if(/squarespace-cdn/.test(u))return r.fulfill({contentType:'image/png',body:ph});return r.abort()});
await p.goto('http://test.local/');await p.waitForTimeout(1500);
console.log(W,'list',await p.evaluate(()=>[...document.querySelectorAll('#wath-levels .mwr b')].map(x=>x.textContent).join(' | ')));
await p.evaluate(()=>document.querySelector('#wath-levels [data-arc]').click());await p.waitForTimeout(400);await p.screenshot({path:'/tmp/arcA-'+W+'.png'});
for(let k=0;k<4;k++){await p.evaluate(()=>document.querySelector('.arcov .arcn').click());await p.waitForTimeout(150)}
console.log(W,'last slide iframe',await p.evaluate(()=>{const f=document.querySelector('.arcov iframe');return f&&f.src}));await p.screenshot({path:'/tmp/arcB-'+W+'.png'});
await p.keyboard.press('Escape');await p.waitForTimeout(150);
await p.evaluate(()=>document.querySelector('#wath-levels [data-invite]').click());await p.waitForTimeout(300);console.log(W,'invite logged-out:',await p.evaluate(()=>document.querySelector('.invov').innerText.slice(0,160)));await p.screenshot({path:'/tmp/inv-'+W+'.png'});
await p.evaluate(()=>document.querySelector('.invov [data-invj]').click());await p.waitForTimeout(400);console.log(W,'login opened',await p.evaluate(()=>!!document.querySelector('.mov')&&!document.querySelector('.invov')));
if(await p.$('.mov [data-m=login]'))await p.click('.mov [data-m=login]');await p.waitForTimeout(300);if(await p.$('.mov [data-m=obskip]'))await p.click('.mov [data-m=obskip]');await p.waitForTimeout(300);
await p.evaluate(()=>{var b=document.querySelector('.mov [data-m=tab][data-t=home]');if(b)b.click()});await p.waitForTimeout(300);const lv=await p.$('.mov .mlv');if(lv){await lv.screenshot({path:'/tmp/lv-'+W+'.png'})}
await p.evaluate(()=>{var x=document.querySelector('.mov [data-m=close]');if(x)x.click()});await p.waitForTimeout(300);
await p.evaluate(()=>document.querySelector('#wath-levels [data-invite]').click());await p.waitForTimeout(300);console.log(W,'invite logged-in:',await p.evaluate(()=>{var o=document.querySelector('.invov');return o&&o.innerText.slice(0,160)}));
console.log(W,'errors',JSON.stringify(errs));await ctx.close()}await b.close()})();
