const {chromium}=require('/opt/npm-tools/node_modules/playwright');const fs=require('fs');
const block=fs.readFileSync('/home/claude/whatatrip-donor-wall/home-page/home-block.html','utf8');const RP='/home/claude/whatatrip-donor-wall/';
const html='<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0"><header id="header"><div class="header-nav-list"><div class="header-nav-item"><a href="/about">About</a></div></div></header><div>'+block+'</div></body></html>';
(async()=>{const b=await chromium.launch();for(const W of [1300,390]){const ctx=await b.newContext({viewport:{width:W,height:900}});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(String(e).slice(0,200)));
await ctx.route('**/*',r=>{const u=r.request().url();if(u==='http://test.local/')return r.fulfill({contentType:'text/html',body:html});if(u.includes('/macros/'))return r.fulfill({contentType:'application/json',body:'{"raised":114509}'});if(u.includes('master-donors.json'))return r.fulfill({contentType:'application/json',body:fs.readFileSync(RP+'master-donors.json','utf8')});if(u.includes('manual.json'))return r.fulfill({contentType:'application/json',body:fs.readFileSync(RP+'manual.json','utf8')});return r.abort()});
await p.goto('http://test.local/');await p.waitForTimeout(1500);
const st=()=>p.evaluate(()=>({upBars:document.querySelectorAll('#wath-updates .soc').length,giftBars:document.querySelectorAll('#wath .dn .wn').length,mov:!!document.querySelector('.mov')}));
console.log(W,'start',JSON.stringify(await st()));
// logged out react -> login opens
await p.evaluate(()=>document.querySelector('#wath-updates .rx').click());await p.waitForTimeout(500);console.log(W,'logged-out react opens login:',(await st()).mov);
await p.evaluate(()=>{var x=document.querySelector('.mov [data-m=close]');if(x)x.click()});await p.waitForTimeout(300);
// sample log in
await p.click('[data-wath-login]');await p.waitForTimeout(300);await p.click('.mov [data-m=login]');await p.waitForTimeout(200);if(await p.$('.mov [data-m=obskip]'))await p.click('.mov [data-m=obskip]');await p.evaluate(()=>{var x=document.querySelector('.mov [data-m=close]');if(x)x.click()});await p.waitForTimeout(400);
await p.evaluate(()=>document.querySelector('#wath-updates .rx[data-e="❤️"]').click());await p.waitForTimeout(200);
console.log(W,'heart on:',await p.evaluate(()=>{var b=document.querySelector('#wath-updates .rx[data-e="❤️"]');return b.className+' '+b.textContent}));
await p.evaluate(()=>document.querySelector('#wath-updates [data-cmt]').click());await p.waitForTimeout(300);
await p.evaluate(()=>document.querySelector('#wath-updates [data-cbox]').scrollIntoView({block:'center'}));
await p.fill('#wath-updates [data-cbox]','So glad to see this coming together!');await p.evaluate(()=>document.querySelector('#wath-updates [data-cm=post]').click());await p.waitForTimeout(300);
console.log(W,'comment:',await p.evaluate(()=>[...document.querySelectorAll('#wath-updates .cm p')].map(x=>x.textContent).join('|')),'count btn:',await p.evaluate(()=>document.querySelector('#wath-updates [data-cmt]').textContent));
await p.screenshot({path:'/tmp/soc-up-'+W+'.png'});
await p.evaluate(()=>document.querySelector('#wath-updates .cml [data-cm=edit]').click());await p.waitForTimeout(150);await p.fill('#wath-updates [data-cedit]','Edited text');await p.evaluate(()=>document.querySelector('#wath-updates [data-cm=save]').click());await p.waitForTimeout(200);
console.log(W,'edited:',await p.evaluate(()=>document.querySelector('#wath-updates .cm p').textContent+' / '+document.querySelector('#wath-updates .cmh span').textContent));
const del=async()=>p.evaluate(()=>document.querySelector('#wath-updates .cml [data-cm=delete]').click());await del();await p.waitForTimeout(100);console.log(W,'armed:',await p.evaluate(()=>document.querySelector('#wath-updates .cml [data-cm=delete]').textContent));await del();await p.waitForTimeout(200);
console.log(W,'after delete:',await p.evaluate(()=>document.querySelectorAll('#wath-updates .cm').length));
// gift reaction
await p.evaluate(()=>{var b=document.querySelector('#wath [data-sup=recent]');if(b)b.click()});await p.waitForTimeout(300);
const gb=await p.evaluate(()=>document.querySelectorAll('#wath .dn .wn').length);await p.evaluate(()=>{var b=document.querySelector('#wath .dn .wn .rx');if(b){b.scrollIntoView({block:'center'});b.click()}});await p.waitForTimeout(200);
console.log(W,'gift bars',gb,'gift heart:',await p.evaluate(()=>{var b=document.querySelector('#wath .dn .wn .rx');return b&&b.className}));
await p.screenshot({path:'/tmp/soc-gift-'+W+'.png'});
const ov=await p.evaluate(()=>{const els=[...document.querySelectorAll('#wath .soc *, #wath .dn *')].filter(e=>e.children.length===0&&e.textContent.trim()&&e.offsetParent);const bx=els.map(e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom,e.textContent.trim().slice(0,20)]});let o=[];for(let i=0;i<bx.length;i++)for(let j=i+1;j<bx.length;j++){const a=bx[i],c=bx[j];const x=Math.min(a[2],c[2])-Math.max(a[0],c[0]),y=Math.min(a[3],c[3])-Math.max(a[1],c[1]);if(x>2&&y>2)o.push(a[4]+' / '+c[4])}return o.slice(0,6)});
console.log(W,'overlaps',JSON.stringify(ov),'hscroll',await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth),'errors',JSON.stringify(errs));await ctx.close()}await b.close()})();
