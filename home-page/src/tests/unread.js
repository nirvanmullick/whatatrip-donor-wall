// Unread updates count beside "Updates" in the dashboard menu. Run: node unread.js
const {chromium}=require('playwright');const fs=require('fs');
const block=fs.readFileSync((process.env.REPO||require('path').resolve(__dirname,'../../..'))+'/home-page/home-block.html','utf8');
(async()=>{const b=await chromium.launch();for(const W of [1300,390]){const ctx=await b.newContext({viewport:{width:W,height:860}});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(String(e).slice(0,200)));
await ctx.route('**/*',r=>{const u=r.request().url();if(u.includes('/macros/'))return r.fulfill({contentType:'application/json',body:'{"raised":114509}'});if(u.startsWith('about:'))return r.continue();return r.abort()});
await p.setContent('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0"><header id="header"><div class="header-nav-list"><div class="header-nav-item"><a href="/about">About</a></div></div></header><div style="max-width:1100px;margin:0 auto;padding:60px 30px 0">'+block+'</div></body></html>');await p.waitForTimeout(1200);
await p.click('[data-wath-login]');await p.waitForTimeout(300);await p.click('.mov [data-m=login]');await p.waitForTimeout(200);await p.click('.mov [data-m=obskip]');await p.waitForTimeout(200);
const bd=()=>p.evaluate(()=>{const x=document.querySelector('.mov .msnav [data-t=updates] .mbdg');return x?x.textContent:'none'});const L=['start:'+await bd()];await p.screenshot({path:'unread-'+W+'.png',clip:{x:0,y:0,width:Math.min(W,700),height:420}});
await p.evaluate(()=>document.querySelector('.mov .msnav [data-t=updates]').click());await p.waitForTimeout(300);await p.evaluate(()=>document.querySelector('.mov .mup:not(.lk):not(.rd)').click());await p.waitForTimeout(300);L.push('after reading one:'+await bd());
await p.evaluate(()=>{const x=document.querySelector('.mov .mup:not(.lk):not(.rd)');if(x)x.click()});await p.waitForTimeout(300);L.push('after reading all:'+await bd());
console.log(W,L.join(' | '),errs);await ctx.close()}await b.close()})();
