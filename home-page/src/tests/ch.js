const {chromium}=require('/opt/npm-tools/node_modules/playwright');const fs=require('fs');
const block=fs.readFileSync('/home/claude/whatatrip-donor-wall/home-page/home-block.html','utf8');
(async()=>{const b=await chromium.launch();for(const W of [1440,390]){const p=await b.newPage({viewport:{width:W,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(String(e).slice(0,200)));
await p.route('**/*',r=>{const u=r.request().url();if(u==='http://test.local/')return r.fulfill({contentType:'text/html',body:'<!DOCTYPE html><html><head><meta charset=utf-8><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style=margin:0>'+block+'</body></html>'});if(u.includes('master-donors.json'))return r.fulfill({contentType:'application/json',body:fs.readFileSync('/home/claude/whatatrip-donor-wall/master-donors.json','utf8')});if(u.includes('/macros/'))return r.fulfill({contentType:'application/json',body:'{"raised":140000}'});return r.abort()});
await p.goto('http://test.local/');await p.waitForTimeout(2000);
await p.click('[data-chx="thor"]');await p.waitForTimeout(200);
const el=p.locator('#wath-challenges');await el.scrollIntoViewIfNeeded();await el.screenshot({path:'/tmp/ch-'+W+'.png'});
console.log(W,await p.locator('#wath .chw').count(),await p.locator('.mh').first().textContent(),errs)}await b.close()})();
