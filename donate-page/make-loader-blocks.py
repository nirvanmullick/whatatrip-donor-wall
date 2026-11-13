import re,io
R='/home/claude/whatatrip-donor-wall/'
old=io.open(R+'donate-page/squarespace-loader-block.html',encoding='utf-8').read()
# v3 (11/13/2026): the Pledge-form gate is gone. It held this block back until the form's iframe had finished loading
# (about a second, up to 3.5s). The form loads in its own frame and is not slowed by this; Nirvan: "The donate page is
# especially important to load fast." WAT_AFTER_FORM stays defined (the block calls it) but runs straight away.
gate='''/* v3: no waiting on the Pledge form -- it loads in its own frame. The block still calls WAT_AFTER_FORM. */
(function () {
  if (window.WAT_AFTER_FORM) return;
  var q = [], going = false;
  function runNext() { var fn = q.shift(); if (!fn) { going = false; return; } try { fn(); } catch (e) { if (window.console) console.error(e); } setTimeout(runNext, 0); }
  window.WAT_AFTER_FORM = function (fn) { q.push(fn); if (!going) { going = true; setTimeout(runNext, 0); } };
})();
'''
PLEDGE='https://script.google.com/macros/s/AKfycby307o55LbT03mbFsh5_bqyxWB9zpLrxXFlDQ0ggTlPn_mV9QaBk3t4DmAqQk9WxRCt/exec'
FEED='https://script.google.com/macros/s/AKfycbzh1TcLYntIy9tf7Nj8jJfnl5k7ILrkrF1yJ1xTJ2vR4JyEQZHMgp3XMw3dtH7-4ajHzQ/exec'
RAW='https://raw.githubusercontent.com/nirvanmullick/whatatrip-donor-wall/main/'
ALLPRE={'pledge':PLEDGE+'?t=','list':RAW+'donors.json?t=','manual':RAW+'manual.json?t=','live':FEED+'?type=donors&t=','recent':FEED+'?type=recent&t=','count':'https://nanavjvwnmkujuxllsir.supabase.co/functions/v1/wat-donor-count'}
def pre(keys):
    items=', '.join("%s: '%s'"%(k,ALLPRE[k]) for k in keys)
    return '''/* v3: ask for the live numbers NOW, at the top of the page, instead of after the code below has arrived and
   started. The block picks these answers up (window.WAT_PRE); if one fails it simply asks again itself. */
(function () {
  if (window.WAT_PRE) return;
  var U = { '''+items+''' }, P = window.WAT_PRE = { t: Date.now() };
  Object.keys(U).forEach(function (k) {
    var u = U[k]; if (/[?&]t=$/.test(u)) u += Date.now();
    try { P[k] = fetch(u, /t=\\d+$/.test(u) ? { cache: 'no-store' } : undefined).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); } catch (e) {}
  });
})();
'''


CSS='''
  #%(m)s.wat-ld-wait { min-height: %(h)spx; }
  @media (max-width: 767px) { #wat-donate-mount { margin-top: 30px; } }
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
  + sh('62%',34,'margin:0 auto 14px') + sh('100%',26,'border-radius:6px;margin-bottom:26px','pu') + sh('100%',170,'border-radius:12px') + sh('132px',34,'border-radius:8px;margin:22px auto 0','pu')   # v3b: the real card is ~518px tall; the stand-in was 398, so everything under it dropped 120px when it loaded
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
SKEL['donors']='<div class="watld-dw"><div class="watld-dw-mid" role="status" aria-label="Loading the donor wall"><div class="watld-rk"><i class="watld-ring"></i><img alt="" width="124" height="124" src="https://pledgeling-res.cloudinary.com/image/upload/c_thumb,g_face,z_0.7,f_auto,h_440,w_440,q_80/v1/prod-media/images/fundraiser_landing_pages/Gi3SsICSnaakROU6zCbf_1WHAT_A_TRIP_Deck_5_25_2026.001.jpeg"></div><div class="watld-tx"><div class="watld-big">Loading<span class="watld-dots" aria-hidden="true"><i></i><i></i><i></i></span></div><div class="watld-sub"><span><b class="watld-n">282</b> donors,</span> <span>credit levels,</span> <span>and donor perks</span></div></div></div></div>'
DWCSS='\n  /* v5 (11/13/2026) -- Nirvan: "start it up in the left where it\'s going to land, while the circle is loading around\n     it." Rick\'s portrait sits where the wall\'s own portrait will be, at its size; "Loading" is set in the headline\'s\n     place and size. The turning ring is the loading circle. Positions come from the script (--rk-*). */\n  #%(m)s .watld-dw { position: relative; z-index: 0; min-height: 100vh; }\n  #%(m)s .watld-dw::before { content: ""; position: absolute; z-index: -1; top: 0; bottom: 0; left: 50%%; width: 100vw; margin-left: -50vw; background: #ece7f7; }\n  #%(m)s .watld-dw-mid { position: absolute; left: var(--rk-l, 118px); top: var(--rk-t, 131px); right: 12px; display: flex; align-items: center; gap: var(--rk-g, 38px); text-align: left; }\n  #%(m)s .watld-rk { position: relative; flex: 0 0 auto; width: var(--rk-s, 150px); height: var(--rk-s, 150px); }\n  #%(m)s .watld-rk::before { content: ""; position: absolute; inset: -9px; border-radius: 50%%; border: 4px solid #dcd4f2; }\n  #%(m)s .watld-rk img { display: block; width: 100%%; height: 100%%; border-radius: 50%%; object-fit: cover; background: #d9d1ef; }\n  #%(m)s .watld-ring { position: absolute; inset: -9px; border-radius: 50%%; background: conic-gradient(from 0deg, rgba(107,92,196,0) 0deg, #b9aee6 150deg, #6b5cc4 330deg, rgba(107,92,196,0) 360deg); -webkit-mask: radial-gradient(farthest-side, transparent calc(100%% - 4px), #000 calc(100%% - 3.5px)); mask: radial-gradient(farthest-side, transparent calc(100%% - 4px), #000 calc(100%% - 3.5px)); animation: watLdSpin 1.15s linear infinite; }\n  #%(m)s .watld-tx { min-width: 0; }\n  #%(m)s .watld-big { font-family: "Source Sans Pro", "Source Sans 3", system-ui, -apple-system, "Segoe UI", sans-serif; font-size: var(--rk-f, 44px); font-weight: 700; line-height: 1.06; letter-spacing: -.02em; color: #1b1526; }\n  #%(m)s .watld-dots i { display: inline-block; width: .13em; height: .13em; min-width: 4px; min-height: 4px; margin-left: .12em; border-radius: 50%%; background: #6b5cc4; animation: watLdDot 1.2s ease-in-out infinite; }\n  #%(m)s .watld-dots i:nth-child(2) { animation-delay: .16s; } #%(m)s .watld-dots i:nth-child(3) { animation-delay: .32s; }\n  #%(m)s .watld-sub { margin-top: .5em; font-size: clamp(15px, calc(var(--rk-f, 44px) * .5), 21px); font-weight: 600; line-height: 1.3; color: #5a4a9a; }\n  #%(m)s .watld-sub span { display: inline-block; opacity: 0; transform: translateY(7px); animation: watLdIn .5s cubic-bezier(.2,.7,.2,1) forwards; animation-delay: .15s; }\n  #%(m)s .watld-sub span:nth-child(2) { animation-delay: .55s; } #%(m)s .watld-sub span:nth-child(3) { animation-delay: .95s; }\n  #%(m)s .watld-sub b { font-weight: 700; color: #2c2456; }\n  #%(m)s .watld-in .watld-sub span { animation: none; opacity: 1; transform: none; }\n  @keyframes watLdSpin { to { transform: rotate(360deg); } }\n  @keyframes watLdDot { 0%%, 100%% { opacity: .25; transform: translateY(0); } 40%% { opacity: 1; transform: translateY(-3px); } }\n  @keyframes watLdIn { to { opacity: 1; transform: none; } }\n  @media (prefers-reduced-motion: reduce) { #%(m)s .watld-ring { animation-duration: 3s; } #%(m)s .watld-dots i { animation: none; opacity: .7; } #%(m)s .watld-sub span { animation: none; opacity: 1; transform: none; } }\n'
JS='''
/* Loader v3 (11/13/2026; the code-loading part is as in v2). VERSION names the commit to load; jsDelivr serves that exact commit from a fast CDN and
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
 'budget': dict(pre=['pledge'],m='wat-budget-mount',h=1500,w=860,dir='budget-page/',file='budget-block.html',after='function (fn) { fn(); }',failh='Our Film Budget',failt='The budget could not load. Please refresh the page.',
    caps='["Loading the budget\\u2026", "Adding up the latest donations\\u2026", "Checking the matching challenge\\u2026", "Almost there\\u2026"]',
    head='''<!-- WHAT A TRIP - /budget page LOADER v3 (11/13/2026).
     Paste this ENTIRE small block into the ONE Code Block on /budget (replacing the earlier loader).
     The real code lives on GitHub: nirvanmullick/whatatrip-donor-wall -> budget-page/budget-block.html
     Shows a picture of the page (and "Loading the budget...") while the real one arrives. -->'''),
 'donors': dict(pre=['pledge','manual','list','live'],m='wat-donors-mount',h=600,w=860,dir='donors-page/',file='donors-block.html',after='function (fn) { fn(); }',failh='Our Film Donors',failt='The donor wall could not load. Please refresh the page.',
    caps='(function () { var n = 0; try { n = +localStorage.getItem("wat-donor-count") || 0; } catch (e) {} if (n < 20) n = 282; window.WAT_DW_CAP = "shown"; var m = document.getElementById("wat-donors-mount"); var c = m.querySelector(".watld-n"); if (c) c.textContent = n; try { (function (root) {\n  /* where Rick\'s portrait will be on the wall: [window width, left, top, size, headline left, headline size], all\n     measured from the top-left of this block. This browser\'s own last measurement if the window is the same width,\n     else the nearest of a table measured on the live page 11/13/2026. */\n  var W = window.innerWidth, g = null, T = [[360,12,151,92,119,18.9],[390,11,154,92,118,20.3],[430,8,152,104,127,22.4],[600,-1,133,104,118,24],[700,-4,133,104,115,24],[800,58,224,112,196,33.6],[900,74,235,112,212,37.8],[1024,84,237,124,238,43],[1150,94,135,124,248,44],[1280,105,131,150,293,44],[1440,118,131,150,306,44],[1700,138,131,150,326,44]];\n  try { var k = JSON.parse(localStorage.getItem(\'wat-dw-rk\') || \'null\'); if (k && k.length === 6 && Math.abs(k[0] - W) <= 2) g = k; } catch (e) {}\n  if (!g) { g = T[0]; for (var i = 1; i < T.length; i++) if (Math.abs(T[i][0] - W) < Math.abs(g[0] - W)) g = T[i]; }\n  var s = root.style;\n  s.setProperty(\'--rk-l\', g[1] + \'px\'); s.setProperty(\'--rk-t\', g[2] + \'px\'); s.setProperty(\'--rk-s\', g[3] + \'px\');\n  s.setProperty(\'--rk-g\', Math.max(14, g[4] - g[1] - g[3]) + \'px\'); s.setProperty(\'--rk-f\', g[5] + \'px\');\n})(m); } catch (e) {} return [""]; })()',
    head='''<!-- WHAT A TRIP - /donors (donor wall) LOADER v5 (11/13/2026).
     Paste this ENTIRE small block into the ONE Code Block on /donors (replacing the earlier loader).
     The real code lives on GitHub: nirvanmullick/whatatrip-donor-wall -> donors-page/donors-block.html
     Shows the wall's own pale background and a quiet "Loading the donor wall..." until the wall is ready. -->'''),
 'donate': dict(pre=['pledge','list','manual','live','recent','count'],m='wat-donate-mount',h=1100,w=480,dir='donate-page/',file='donate-block.html',after='window.WAT_AFTER_FORM || function (fn) { fn(); }',failh='Our Film Budget',failt='<a href="/budget">See the film budget &rarr;</a>',
    caps='["Loading the budget\\u2026", "Adding up the latest donations\\u2026", "Loading our donors\\u2026", "Almost there\\u2026"]',
    head='''<!-- WHAT A TRIP - /donate Film Budget + Donations LOADER v3 (11/13/2026).
     Paste this ENTIRE small block over the earlier loader (the block UNDER the Pledge form).
     The real code lives on GitHub: nirvanmullick/whatatrip-donor-wall -> donate-page/donate-block.html
     A picture of the budget + donations shows while the real one arrives (v3: no longer waits for the form). -->'''),
}
OUT={'budget':'budget-page/squarespace-loader-block.html','donors':'donors-page/squarespace-loader-block.html','donate':'donate-page/squarespace-loader-block.html'}
for k,P in PAGES.items():
    css=CSS%P+(DWCSS%P if k=='donors' else '')
    html=(P['head']+'\n<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>\n<link rel="preconnect" href="https://raw.githubusercontent.com" crossorigin>\n<link rel="preconnect" href="https://script.google.com" crossorigin>\n<link rel="preconnect" href="https://script.googleusercontent.com" crossorigin>\n'
      '<div id="%s" class="wat-ld-wait">\n  <div class="watld">%s</div>\n</div>\n<style>%s</style>\n<script>\n%s%s</script>\n'%(P['m'],SKEL[k],css,pre(P['pre'])+(gate if k=='donate' else ''),JS%P))
    io.open(R+OUT[k],'w',encoding='utf-8').write(html); print(k,len(html))
