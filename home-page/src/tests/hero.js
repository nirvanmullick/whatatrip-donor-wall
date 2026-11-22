const {chromium}=require('playwright');const fs=require('fs');
const block=fs.readFileSync((process.env.REPO||require('path').resolve(__dirname,'../../..'))+'/home-page/home-block.html','utf8');
(async()=>{const b=await chromium.launch();for(const W of [1300,390]){const ctx=await b.newContext({viewport:{width:W,height:900}});const p=await ctx.newPage();
await ctx.route('**/*',r=>{const u=r.request().url();if(u.includes('/macros/'))return r.fulfill({contentType:'application/json',body:'{"raised":114509}'});if(u.includes('wat-donor-count'))return r.fulfill({contentType:'application/json',body:'{"donors":281}'});if(u.startsWith('about:'))return r.continue();return r.abort()});
await p.setContent('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0"><div style="max-width:1100px;margin:0 auto;padding:60px 30px 0">'+block+'</div></body></html>');await p.waitForTimeout(6500);
await p.screenshot({path:'hero-'+W+'.png'});await ctx.close()}await b.close()})();
