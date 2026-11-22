const {chromium}=require('playwright');const fs=require('fs');
const block=fs.readFileSync((process.env.REPO||require('path').resolve(__dirname,'../../..'))+'/home-page/home-block.html','utf8');
(async()=>{const b=await chromium.launch();for(const W of [1300,390]){const ctx=await b.newContext({viewport:{width:W,height:900}});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(String(e).slice(0,200)));
await ctx.route('**/*',r=>{const u=r.request().url();if(u==='http://test.local/')return r.fulfill({contentType:'text/html',body:'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">'+block+'</body></html>'});if(u.includes('/macros/'))return r.fulfill({contentType:'application/json',body:'{"raised":114509}'});return r.abort()});
await p.goto('http://test.local/');await p.waitForTimeout(1200);
await p.click('[data-wath-login]');await p.waitForTimeout(400);await p.click('.mov [data-m=login]');await p.waitForTimeout(200);await p.click('.mov [data-m=obskip]');await p.waitForTimeout(200);
await p.evaluate(()=>{document.querySelector('.mov [data-m=tab][data-t=perks],.mov [data-t=perks]').click()});await p.waitForTimeout(300);
await p.click('.mov [data-m=pfpv][data-t="25000"]');await p.waitForTimeout(300);
// shirt: fill size + address and save
const sh=p.locator('.mov details.pfd',{hasText:'Legalize Rick'});await sh.locator('summary').click();
await sh.locator('select').first().selectOption('L');for(const [k,v] of [['name','Test Person'],['l1','1 Main St'],['city','Ojai'],['reg','CA'],['zip','93023']])await sh.locator('[data-pfa='+k+']').fill(v);
await sh.locator('[data-m=pfsave]').click();await p.waitForTimeout(300);
const st=await p.locator('.mov details.pfd',{hasText:'Legalize Rick'}).locator('summary .apill').textContent();
const ar=p.locator('.mov details.pfd',{hasText:'Arcturus'});await ar.locator('summary').click();await p.waitForTimeout(200);
await ar.screenshot({path:require('os').tmpdir()+'/pf-stay-'+W+'.png'});
await p.locator('.mov .mbody').evaluate(e=>e.scrollTop=0);await p.screenshot({path:require('os').tmpdir()+'/pf-'+W+'.png'});
console.log(W,'shirt status:',st,'rows',await p.locator('.mov details.pfd').count(),'errors',errs)}await b.close()})();
