const {chromium}=require('/opt/npm-tools/node_modules/playwright');const fs=require('fs');
const block=fs.readFileSync('/home/claude/whatatrip-donor-wall/home-page/home-block.html','utf8');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});const errs=[];p.on('pageerror',e=>errs.push(String(e)));
await p.setContent('<!DOCTYPE html><html><head><meta charset="utf-8"></head><body style="margin:0">'+block+'</body></html>');await p.waitForTimeout(800);
const st=()=>p.evaluate(()=>{const b=document.querySelector('#wath .subnav .btn[data-give]');return document.getElementById('wath').classList.contains('sngive')+' op='+getComputedStyle(b).opacity});
console.log('top',await st());await p.mouse.wheel(0,500);await p.waitForTimeout(600);console.log('500',await st());await p.mouse.wheel(0,1500);await p.waitForTimeout(600);console.log('2000',await st());await p.screenshot({path:'/tmp/sng.png'});await p.mouse.wheel(0,-2000);await p.waitForTimeout(600);console.log('back',await st());console.log(errs);await b.close()})();
