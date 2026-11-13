import re,io
R='/home/claude/whatatrip-donor-wall/'
old=io.open(R+'donate-page/squarespace-loader-block.html',encoding='utf-8').read()
gate=old[old.index('/* Gate:'):old.index('/* Loader')]; gate=gate[:gate.rindex('})();')+5]+'\n'   # the Pledge-form gate, unchanged

CSS='''
  #%(m)s.wat-ld-wait { min-height: %(h)spx; }
  #%(m)s .watld { font-family: "Source Sans 3", "Source Sans Pro", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; color: #1f2430; -webkit-font-smoothing: antialiased; }
  #%(m)s .watld * { box-sizing: border-box; }
  #%(m)s .watld-card { background: #fff; border-radius: 18px; box-shadow: 0 14px 40px rgba(20,30,55,.18); padding: 22px 24px 20px; margin: 0 auto 18px; max-width: %(w)spx; }
  #%(m)s .watld-h { font-size: 24px; font-weight: 700; margin: 0 0 12px; }
  #%(m)s .watld-tabs { display: flex; gap: 6px; border-bottom: 1px solid #e2e5ea; margin-bottom: 16px; }
  #%(m)s .watld-tabs span { padding: 7px 11px; font-size: 16px; font-weight: 600; color: #6e7488; border-radius: 8px 8px 0 0; }
  #%(m)s .watld-tabs span.on { background: #e8e2f7; color: #1f2430; box-shadow: inset 0 -2px 0 #33697f; }
  #%(m)s .watld-sh { display: block; border-radius: 8px; background: linear-gradient(90deg, #e9edf2 0%%, #f5f7fa 45%%, #e9edf2 90%%); background-size: 220%% 100%%; animation: watLdSh 1.3s ease-in-out infinite; }
  #%(m)s .watld-sh.pu { background-image: linear-gradient(90deg, #e3defa 0%%, #f1eefc 45%%, #e3defa 90%%); }
  #%(m)s .watld-row { display: flex; align-items: center; gap: 12px; padding: 11px 0; border-top: 1px solid #eef0f4; }
  #%(m)s .watld-dot { flex: 0 0 auto; width: 34px; height: 34px; border-radius: 50%%; }
  #%(m)s .watld-cap { text-align: center; font-size: 14px; font-weight: 600; color: #5a6b78; margin: 14px 0 2px; min-height: 20px; transition: opacity .22s ease; }
  #%(m)s .watld-cap::before { content: ""; display: inline-block; width: 8px; height: 8px; margin-right: 8px; border-radius: 50%%; background: #6b5cc4; vertical-align: 1px; animation: watLdPulse 1s ease-in-out infinite; }
  @keyframes watLdSh { 0%% { background-position: 110%% 0 } 100%% { background-position: -110%% 0 } }
  @keyframes watLdPulse { 0%%, 100%% { opacity: .25; transform: scale(.8) } 50%% { opacity: 1; transform: scale(1.15) } }
  @media (prefers-reduced-motion: reduce) { #%(m)s .watld-sh, #%(m)s .watld-cap::before { animation: none; } }
'''
def sh(w,h,extra='',cls=''): return '<span class="watld-sh %s" style="width:%s;height:%spx;%s"></span>'%(cls,w,h,extra)
BUDCARD=lambda cap: ('<div class="watld-card"><div class="watld-h">Our Film Budget</div>'
  '<div class="watld-tabs"><span>Total Budget</span><span class="on">Rough Cut</span><span>Final Cut</span></div>'
  + sh('62%',34,'margin:0 auto 14px') + sh('100%',26,'border-radius:6px;margin-bottom:26px','pu') + sh('100%',128,'border-radius:12px')
  + '<div class="watld-cap" aria-live="polite">'+cap+'</div></div>')
def rows(n,dot=True): return ''.join('<div class="watld-row">'+(sh('34px',34,'','')[:-7].replace('watld-sh ','watld-sh watld-dot ')+'</span>' if dot else '')+'<span style="flex:1">'+sh(str(70-(i*9)%30)+'%',14,'margin-bottom:7px')+sh(str(38+(i*7)%20)+'%',11)+'</span>'+sh('64px',14)+'</div>' for i in range(n))
LISTCARD=lambda title,n: '<div class="watld-card"><div class="watld-h" style="font-size:19px">'+title+'</div>'+rows(n,False)+'</div>'
SKEL={
 'budget': BUDCARD('Loading the budget&hellip;')+LISTCARD('$700K Rough Cut Budget',6)+LISTCARD('$900K Final Cut Budget',4),
 'donate': BUDCARD('Loading the budget&hellip;')+'<div class="watld-card"><div class="watld-h">Donations</div><div class="watld-tabs"><span>Top Donations</span><span class="on">Recent Donations</span><span>Challenges</span></div>'+rows(5)+'</div>',
}
PERKS=[('Add Your Name','Join our donor wall with everyone helping make this film.','$5+','76b2e2e5-27bc-454e-9bc1-db04bae5638e/WAT+5+add+your+name+pic.png'),
       ('Get a Film Credit','Get a Special Thanks or more in our film and on IMDb.','$5k+','b9c48c42-1e1d-4d74-9c65-e533da7e89b3/WAT_theater_pre_visual.png'),
       ('Stay in Arcturus','A week in the house Rick built at 21 for psychedelic journeys.','$25k+','1175374f-153d-4c3f-a06c-693efe0c820a/Arcturus_Exterior.png'),
       ('Guided Therapy w Rick','Guided session w Rick in home he built for psychedelic therapy','$250k+','2cd821c0-6504-4f70-829a-280be526ee4b/Arcturus_Therapy_blurred.png')]
IMG='https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/'
# 2026-11-12 (Nirvan): the picture-of-the-page placeholder for the donor wall "does not match what the actual donor
# wall is ... looks like a mistake going from one page to the other". A stand-in layout can never match a page that
# measures and arranges itself, so the wall's placeholder is now deliberately NOT a layout: the wall's own pale canvas
# with one quiet line in the middle. The wall then appears on the same canvas.
SKEL['donors']=('<div class="watld-dw"><div class="watld-dw-mid">'
 '<div class="watld-cap" aria-live="polite">Loading the donor wall&hellip;</div>'
 + sh('220px',6,'border-radius:4px;margin:14px auto 0','pu')
 + '</div></div>')
DWCSS='''
  #%(m)s .watld-dw { background: #ece7f7; box-shadow: 0 0 0 100vmax #ece7f7; clip-path: inset(0 -100vmax); min-height: 100vh; display: flex; justify-content: center; }
  #%(m)s .watld-dw-mid { margin-top: 30vh; text-align: center; }
  #%(m)s .watld-dw .watld-cap { font-size: 15px; color: #5a4a9a; margin: 0; }
'''
JS='''
/* Loader v2 (11/12/2026). VERSION names the commit to load; jsDelivr serves that exact commit from a fast CDN and
   browsers keep it. NEW: the last version this browser loaded is remembered, and its code is asked for straight away
   (it comes out of the browser's own cache), while VERSION is checked alongside -- so a returning visitor is not kept
   waiting on two round trips. A newer version, if VERSION answers within 0.6s, is used instead. */
(function () {
  var REPO = 'nirvanmullick/whatatrip-donor-wall', DIR = '%(dir)s', FILE = DIR + '%(file)s', KEY = 'wat-ver:' + DIR;
  var mount = document.getElementById('%(m)s'); if (!mount || mount.__watStarted) return;
  mount.__watStarted = 1; mount.classList.add('wat-ld-wait');
  var caps = %(caps)s, ci = 0, capEl = mount.querySelector('.watld-cap');
  var capT = setInterval(function () { if (!capEl || !document.body.contains(capEl)) { clearInterval(capT); return; }
    ci = (ci + 1) %% caps.length; capEl.style.opacity = '0'; setTimeout(function () { capEl.textContent = caps[ci]; capEl.style.opacity = '1'; }, 230); }, 1700);
  function get(u, opt) { return fetch(u, opt).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); }); }
  function ok(v) { return /^[0-9a-f]{7,40}$/.test(v || ''); }
  function file(v) { return get('https://cdn.jsdelivr.net/gh/' + REPO + '@' + v + '/' + FILE).catch(function () { return get('https://raw.githubusercontent.com/' + REPO + '/' + v + '/' + FILE); }); }
  function save(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  var known = null; try { known = localStorage.getItem(KEY); } catch (e) {}
  if (!ok(known)) known = null;
  var ver = get('https://raw.githubusercontent.com/' + REPO + '/main/' + DIR + 'VERSION', { cache: 'no-store' }).then(function (v) { v = (v || '').trim(); if (!ok(v)) throw new Error('version'); return v; });
  var fresh = function () { return ver.then(function (v) { save(v); return file(v); }).catch(function () { return get('https://raw.githubusercontent.com/' + REPO + '/main/' + FILE, { cache: 'no-store' }); }); };
  var html;
  if (known) {
    var mine = file(known);
    html = Promise.race([ver.catch(function () { return null; }), new Promise(function (res) { setTimeout(function () { res(null); }, 600); })])
      .then(function (v) { if (v && v !== known) { save(v); return file(v).catch(function () { return mine; }); } return mine; })
      .catch(fresh);
    ver.then(save, function () {});
  } else html = fresh();
  function inject(s) {
    clearInterval(capT);
    var tpl = document.createElement('template'); tpl.innerHTML = s;
    var scripts = [].slice.call(tpl.content.querySelectorAll('script'));
    var marks = scripts.map(function (sc) { var c = document.createComment('wat'); sc.parentNode.replaceChild(c, sc); return c; });
    mount.innerHTML = ''; mount.className = ''; mount.appendChild(tpl.content);
    var i = 0;
    (function next() {
      if (i >= scripts.length) return;
      var old = scripts[i], m = marks[i]; i++;
      var n = document.createElement('script');
      [].forEach.call(old.attributes, function (a) { n.setAttribute(a.name, a.value); });
      n.text = old.text; m.parentNode.replaceChild(n, m);
      setTimeout(next, 0);
    })();
  }
  var after = %(after)s;
  after(function () {
    html.then(inject, function () {
      clearInterval(capT); mount.className = '';
      mount.innerHTML = '<div class="watld"><div class="watld-card"><div class="watld-h">%(failh)s</div><div class="watld-cap" style="animation:none">%(failt)s</div></div></div>';
    });
  });
})();
'''
PAGES={
 'budget': dict(m='wat-budget-mount',h=1500,w=860,dir='budget-page/',file='budget-block.html',after='function (fn) { fn(); }',failh='Our Film Budget',failt='The budget could not load. Please refresh the page.',
    caps='["Loading the budget\\u2026", "Adding up the latest donations\\u2026", "Checking the matching challenge\\u2026", "Almost there\\u2026"]',
    head='''<!-- WHAT A TRIP - /budget page LOADER v2 (11/12/2026).
     Paste this ENTIRE small block into the ONE Code Block on /budget (replacing the earlier loader).
     The real code lives on GitHub: nirvanmullick/whatatrip-donor-wall -> budget-page/budget-block.html
     Shows a picture of the page (and "Loading the budget...") while the real one arrives. -->'''),
 'donors': dict(m='wat-donors-mount',h=600,w=860,dir='donors-page/',file='donors-block.html',after='function (fn) { fn(); }',failh='Our Film Donors',failt='The donor wall could not load. Please refresh the page.',
    caps='["Loading the donor wall\\u2026"]',
    head='''<!-- WHAT A TRIP - /donors (donor wall) LOADER v2 (11/12/2026).
     Paste this ENTIRE small block into the ONE Code Block on /donors (replacing the earlier loader).
     The real code lives on GitHub: nirvanmullick/whatatrip-donor-wall -> donors-page/donors-block.html
     Shows the wall's own pale background and a quiet "Loading the donor wall..." until the wall is ready. -->'''),
 'donate': dict(m='wat-donate-mount',h=1100,w=480,dir='donate-page/',file='donate-block.html',after='window.WAT_AFTER_FORM || function (fn) { fn(); }',failh='Our Film Budget',failt='<a href="/budget">See the film budget &rarr;</a>',
    caps='["Loading the budget\\u2026", "Adding up the latest donations\\u2026", "Loading our donors\\u2026", "Almost there\\u2026"]',
    head='''<!-- WHAT A TRIP - /donate Film Budget + Donations LOADER v2 (11/12/2026).
     Paste this ENTIRE small block over the earlier loader (the block UNDER the Pledge form).
     The real code lives on GitHub: nirvanmullick/whatatrip-donor-wall -> donate-page/donate-block.html
     The donation form still loads first; a picture of the budget + donations shows meanwhile. -->'''),
}
OUT={'budget':'budget-page/squarespace-loader-block.html','donors':'donors-page/squarespace-loader-block.html','donate':'donate-page/squarespace-loader-block.html'}
for k,P in PAGES.items():
    css=CSS%P+(DWCSS%P if k=='donors' else '')
    html=(P['head']+'\n<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>\n<link rel="preconnect" href="https://raw.githubusercontent.com" crossorigin>\n'
      '<div id="%s" class="wat-ld-wait">\n  <div class="watld">%s</div>\n</div>\n<style>%s</style>\n<script>\n%s%s</script>\n'%(P['m'],SKEL[k],css,(gate if k=='donate' else ''),JS%P))
    io.open(R+OUT[k],'w',encoding='utf-8').write(html); print(k,len(html))
