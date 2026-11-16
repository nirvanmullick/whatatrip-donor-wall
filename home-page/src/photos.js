const fs=require('fs');const s=fs.readFileSync('/home/claude/whatatrip-donor-wall/donors-page/donors-block.html','utf8');
const a=s.indexOf('var PHOTOS = {');let i=s.indexOf('{',a),d=0,j=i;
for(;j<s.length;j++){const c=s[j];if(c==='{')d++;else if(c==='}'){d--;if(d===0)break}}
const obj=(new Function('return '+s.slice(i,j+1)))();const out={};
for(const k in obj){const v=obj[k];out[k]=typeof v==='string'?{src:v}:v}
// rachel + roth
const m=s.match(/rachel-hamilton_1\.jpg[^'"]*/);
fs.writeFileSync('photos.json',JSON.stringify(out,null,1));console.log(Object.keys(out).length,Object.keys(out).join(' | '));
const q=s.slice(s.indexOf('var QUOTES_BY_HAND = {'));let qi=q.indexOf('{'),qd=0,qj=qi;for(;qj<q.length;qj++){const c=q[qj];if(c==='{')qd++;else if(c==='}'){qd--;if(qd===0)break}}
const Q=(new Function('return '+q.slice(qi,qj+1)))();fs.writeFileSync('quotes.json',JSON.stringify(Q,null,1));console.log(Object.keys(Q));
