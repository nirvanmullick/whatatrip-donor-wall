const {chromium}=require('/opt/npm-tools/node_modules/playwright');const fs=require('fs');
const block=fs.readFileSync('/home/claude/whatatrip-donor-wall/home-page/home-block.html','utf8');
const R='/home/claude/whatatrip-donor-wall/';
(async()=>{const b=await chromium.launch();for(const W of [1300,1100,390]){const p=await b.newPage({viewport:{width:W,height:900}});const errs=[];p.on('pageerror',e=>errs.push(String(e)));
await p.route('**/*',r=>{const u=r.request().url();if(u.includes('/macros/'))return r.fulfill({contentType:'application/json',body:'{"raised":114509}'});if(u.includes('master-donors.json'))return r.fulfill({contentType:'application/json',body:fs.readFileSync(R+'master-donors.json','utf8')});if(u.includes('manual.json'))return r.fulfill({contentType:'application/json',body:fs.readFileSync(R+'manual.json','utf8')});return u.startsWith('about:')?r.continue():r.abort()});
await p.setContent('<!DOCTYPE html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><body style=margin:0><div style="max-width:1100px;margin:0 auto;padding:60px 30px 0">'+block+'</div>');await p.waitForTimeout(2500);
const m=()=>p.evaluate(()=>{const a=document.querySelector('#wath-recent [data-supmore]'),c=document.querySelector('#wath-levels [data-chart]');return a&&c?[Math.round(a.getBoundingClientRect().top+scrollY),Math.round(c.getBoundingClientRect().top+scrollY),document.querySelectorAll('#wath-recent .suplist>*').length]:[!!a,!!c]});
const r1=await m();await p.click('#wath-recent [data-suptab=recent], #wath-recent .tabs button:nth-child(2)').catch(()=>{});await p.waitForTimeout(400);const r2=await m();console.log(W,r1,r2,errs);
if(W===1300){const s=await p.$('.wrap.cols');await p.evaluate(()=>{const a=document.querySelector('#wath-levels [data-chart]');window.scrollTo(0,a.getBoundingClientRect().top+scrollY-700)});await p.waitForTimeout(300);await p.screenshot({path:'fit.png'})}}
await b.close()})();
