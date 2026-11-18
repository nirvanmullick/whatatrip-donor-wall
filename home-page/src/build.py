import re,json,io,base64,os
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
P=open('proto/index.html').read()
css=P[P.index('<style>')+7:P.index('</style>')]
# ---------- scope CSS ----------
PFX=':is(#wath,#wath-top)'
def scope_sel(sel):
    out=[]
    for s in re.split(r',(?![^(]*\))',sel):
        s=s.strip()
        if not s: continue
        if s in('html','body') or s.startswith('html') : 
            if s=='body': out.append('#wath'); 
            continue
        if s.startswith('header') or s.startswith('nav') or s.startswith('footer') or s.startswith('.proto') or s.startswith('.hv') or s.startswith('.pv') or s.startswith('.logo'): continue
        if s=='*': out.append(PFX+' *'); continue
        out.append(PFX+' '+s)
    return ','.join(out)
def scope(css):
    out=[];i=0;n=len(css)
    while i<n:
        j=css.find('{',i)
        if j<0: break
        sel=css[i:j].strip()
        # find matching }
        d=0;k=j
        while k<n:
            if css[k]=='{':d+=1
            elif css[k]=='}':
                d-=1
                if d==0:break
            k+=1
        body=css[j+1:k]
        sel=re.sub(r'/\*.*?\*/','',sel,flags=re.S).strip()
        if sel.startswith('@media'):
            out.append(sel+'{'+scope(body)+'}')
        else:
            ss=scope_sel(sel)
            if ss: out.append(ss+'{'+body+'}')
        i=k+1
    return '\n'.join(out)
css=re.sub(r'url\(data:[^)]*\)','none',css)
scoped=scope(css)
scoped=scoped.replace('#wath{margin:0;','#wath{').replace('background:#f5f3fa;line-height:1.45}','background:#f5f3fa;line-height:1.45;width:100vw;margin-left:calc(50% - 50vw);overflow-x:clip;text-align:left;-webkit-font-smoothing:antialiased}',1)
extra='''
/* test page only: the short main menu (About, Donor Wall, Impact, Donate). The logo already goes home. */
.header-nav-item:has(> a[href="/trailer"]),.header-nav-item:has(> a[href="/budget"]),
.header-menu-nav-item:has(a[href="/trailer"]),.header-menu-nav-item:has(a[href="/budget"]){display:none!important}

#wath-top{font-family:'Source Sans 3',system-ui,sans-serif;color:#1f2430;line-height:1.45;text-align:left}
:is(#wath,#wath-top) :where(h1,h2,h3,p,ul,ol,li,a,button,b,span,table,th,td,summary){font-family:inherit;letter-spacing:normal;text-transform:none}
:is(#wath,#wath-top) :where(h1,h2,h3){font-weight:800;color:#1f2430;margin:0;line-height:1.15}
:is(#wath,#wath-top) :where(h3){font-size:18px}
:is(#wath,#wath-top) :where(p){margin:0;font-size:inherit;line-height:inherit}
:is(#wath,#wath-top) :where(button){appearance:none;-webkit-appearance:none;border-radius:0;box-shadow:none;text-shadow:none;margin:0;line-height:1.3;color:inherit;width:auto;height:auto;min-width:0}
:is(#wath,#wath-top) :where(a){text-decoration:underline;background:none;border:0}
:is(#wath,#wath-top) :where(ul){list-style:disc}
:is(#wath,#wath-top) :where(li){margin:0;padding:0}
:is(#wath,#wath-top) :where(img){max-width:none;border:0}
:is(#wath,#wath-top) .video{background:#1b1526 center 30%/cover;min-height:0;aspect-ratio:16/9;text-decoration:none;display:block;align-self:start}
:is(#wath,#wath-top) .video iframe{position:absolute;inset:0;width:100%;height:100%;border:0;display:block}
:is(#wath,#wath-top) .video.playing{background-image:none!important;cursor:default}
:is(#wath,#wath-top) .subnav{position:sticky;top:0;z-index:20}
:is(#wath,#wath-top) .subnav .wrap{overflow:visible;align-items:center;gap:16px}
:is(#wath,#wath-top) .subnav .snl{display:flex;gap:26px;overflow-x:auto;flex:1;min-width:0;scrollbar-width:none}
:is(#wath,#wath-top) .subnav .snl::-webkit-scrollbar{display:none}
:is(#wath,#wath-top) .subnav .btn{flex:none;min-height:38px;padding:0 18px;margin:6px 0}
:is(#wath,#wath-top) .sec{scroll-margin-top:70px}
:is(#wath,#wath-top) .band{scroll-margin-top:56px}
:is(#wath,#wath-top) aside{top:110px}
:is(#wath,#wath-top) .av{background-size:cover;background-position:center;overflow:hidden;position:relative}
:is(#wath,#wath-top) .av img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
:is(#wath,#wath-top) .ft.ph{background-size:cover;background-position:center}
:is(#wath,#wath-top) .ft.ph:after{inset:25% 0 0;background:linear-gradient(180deg,transparent,rgba(20,14,50,.86))}

:is(#wath,#wath-top) .lv ul{padding:0 0 0 17px;margin:4px 0 0}
:is(#wath,#wath-top) .msd ul{padding:0 0 0 18px;margin:0 0 12px 30px}
:is(#wath,#wath-top) .ft.ph .fl{background:rgba(20,14,50,.55);padding:3px 8px;border-radius:999px;text-shadow:none}
:is(#wath,#wath-top) .cbtn{padding:0;display:inline-flex;align-items:center;justify-content:center;background:#fff;color:#6152a0}
:is(#wath,#wath-top) table{border:0}
:is(#wath,#wath-top) .lv .gorb{margin-top:10px;min-height:38px}
:is(#wath,#wath-top) .gor{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
:is(#wath,#wath-top) .gor .btn{min-height:38px;padding:0 14px;font-size:14px;display:inline-flex;align-items:center;text-decoration:none}
:is(#wath,#wath-top) .fb .gor{margin-top:0}
:is(#wath,#wath-top) .btn.lite{background:rgba(255,255,255,.92);border-color:rgba(255,255,255,.92);color:#2c2208}
:is(#wath,#wath-top) .fq{border-top:1px solid #e9e6f1}
:is(#wath,#wath-top) .fq:first-child{border-top:0}
:is(#wath,#wath-top) .fq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:15px 0;font-weight:700;font-size:17px;color:#1f2430}
:is(#wath,#wath-top) .fq summary::-webkit-details-marker{display:none}
:is(#wath,#wath-top) .fq[open] .chev{transform:rotate(180deg)}
:is(#wath,#wath-top) .fq p{margin:0 0 16px;color:#3a4051;font-size:16px;line-height:1.55;max-width:680px}
:is(#wath,#wath-top) .card.tndd{background:#1b1e2b;border-color:#1b1e2b;color:#fff;gap:28px;padding:28px}
:is(#wath,#wath-top) .tndl{flex:0 0 auto;width:min(300px,100%);height:auto;display:block}
:is(#wath,#wath-top) .tndt{flex:1;min-width:260px}
:is(#wath,#wath-top) .tndt .tag{color:#9db7ff}
:is(#wath,#wath-top) .tndt h2{color:#fff;font-size:24px;margin:6px 0 8px;line-height:1.2}
:is(#wath,#wath-top) .tndt p{color:#d6d9e6;margin:0 0 16px;font-size:16px;line-height:1.5}
:is(#wath,#wath-top) .tndq{border-left:3px solid #e5302e;padding:2px 0 2px 16px;margin:14px 0 18px}
:is(#wath,#wath-top) .tndq p{color:#fff;font-size:18px;line-height:1.45;margin:0 0 10px;font-style:italic}
:is(#wath,#wath-top) .tndby{display:flex;align-items:center;gap:10px;font-size:13.5px;color:#d6d9e6;line-height:1.35}
:is(#wath,#wath-top) .tndby img{width:44px;height:44px;border-radius:50%;object-fit:cover;flex:none}
:is(#wath,#wath-top) .tndby b{color:#fff;font-size:15px}
:is(#wath,#wath-top) .btn.tf{background:transparent;border-color:#fff;color:#fff;display:inline-flex;align-items:center;text-decoration:none;padding:0 22px}
:is(#wath,#wath-top) .tndb{display:flex;gap:12px 14px;align-items:center;flex-wrap:wrap}
:is(#wath,#wath-top) .btn.tj{background:#2f8cff;border-color:#2f8cff;color:#fff;display:inline-flex;align-items:center;text-decoration:none;padding:0 26px}
:is(#wath,#wath-top) .tm{color:#fff;font-weight:700}
@media(max-width:700px){:is(#wath,#wath-top) .card.tndd{justify-content:center}:is(#wath,#wath-top) .tndl{margin:0 auto}}
:is(#wath,#wath-top) .tm5{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
:is(#wath,#wath-top) .tmc{background:#fff;border:1px solid #e3dfee;border-radius:14px;padding:14px 16px;display:flex;flex-direction:column;gap:2px}
:is(#wath,#wath-top) .tmc b{font-size:17px}
:is(#wath,#wath-top) .tmc span{font-size:14px;color:#5b6478}

/* ---- Nov 15: look of the donor wall page (/donors): periwinkle site header, lavender page, pinned menu bar ---- */
#header{background:#6f74aa!important}
.page-section:has(#wat-home-mount),.page-section:has(#wat-home-mount) .section-background{background-color:#ece7f7!important}
.page-section:has(#wat-home-mount) .content-wrapper{padding-top:0!important;padding-bottom:0!important}
.page-section:has(#wat-home-mount){padding-top:59px!important;min-height:0!important}
#header .header-nav-item a,#header .header-title-text a,#header .header-title a,#header .header-menu-nav-item a{color:#fff!important}
#header .header-actions .icon svg,#header .header-actions svg{fill:#fff!important}
#header .burger-inner .top-bun,#header .burger-inner .patty,#header .burger-inner .bottom-bun{background-color:#fff!important}
#wath{background:#ece7f7;color:#1b1526;font-family:'Source Sans 3','Source Sans Pro',-apple-system,system-ui,sans-serif}
:is(#wath,#wath-top) .hero{background:transparent;border-bottom:0;padding-top:34px}
:is(#wath,#wath-top) h1{font-weight:900;color:#1b1526;letter-spacing:-.01em}
:is(#wath,#wath-top) :where(h2){color:#1b1526}
:is(#wath,#wath-top) .card{background:#f6f3fc;border-color:#d9d3ec}
:is(#wath,#wath-top) .tmc,:is(#wath,#wath-top) .ch,:is(#wath,#wath-top) .tile,:is(#wath,#wath-top) .raise{background:#f6f3fc;border-color:#d9d3ec}
:is(#wath,#wath-top) .ch.live{background:#fbf5e6;border-color:#ecd9a8}
:is(#wath,#wath-top) .ch.done{background:#e6eef6;border-color:#bcd0e2}
:is(#wath,#wath-top) .band{background:#dedaf0;border-color:#d0cae6}
:is(#wath,#wath-top) .nm{background:#f6f3fc}
:is(#wath,#wath-top) .hour{background:#f6f3fc;border-color:#d9d3ec;color:#3a3350}
:is(#wath,#wath-top) .seg{border-color:#d0cae6}
:is(#wath,#wath-top) .seg button{background:#e3def2}
:is(#wath,#wath-top) .seg button.on{background:#f6f3fc}
:is(#wath,#wath-top) .bar,:is(#wath,#wath-top) .total{background:#dcd6ee}
:is(#wath,#wath-top) .btn{border-radius:8px;border-color:#1b1526;color:#1b1526;background:transparent}
:is(#wath,#wath-top) .btn.pri{background:#6152a0;border-color:#6152a0;color:#fff}
:is(#wath,#wath-top) .btn.gold{background:#f1d28a;border-color:#f1d28a;color:#2c2208}
:is(#wath,#wath-top) .btn.lite{background:rgba(255,255,255,.92);border-color:rgba(255,255,255,.92);color:#2c2208}
:is(#wath,#wath-top) .btn.tj{background:#2f8cff;border-color:#2f8cff;color:#fff}
:is(#wath,#wath-top) .btn.tf{background:transparent;border-color:#fff;color:#fff}
:is(#wath,#wath-top) .subnav{background:#ece7f7;border-bottom:0}
:is(#wath,#wath-top) .subnav .wrap{border-bottom:1px solid rgba(27,21,38,.16);padding-top:5px;padding-bottom:6px}
:is(#wath,#wath-top) .subnav .snl{gap:22px}
:is(#wath,#wath-top) .subnav .snl a{color:#1b1526;font-weight:800;font-size:13.5px;letter-spacing:.12em;text-transform:uppercase;padding:13px 0}
:is(#wath,#wath-top) .subnav .snl a:hover{color:#6152a0}
:is(#wath,#wath-top) .subnav .btn{min-width:120px}
@media(min-width:901px){:is(#wath,#wath-top) .subnav .snl a{letter-spacing:.08em;padding:13px 10px;font-size:13px}:is(#wath,#wath-top) .subnav .snl{margin-left:-10px;padding-right:0}}
@media(min-width:901px) and (max-width:1240px){:is(#wath,#wath-top) .subnav .snl a{letter-spacing:.05em;padding:13px 7px;font-size:12.5px}:is(#wath,#wath-top) .subnav .snl{margin-left:-7px}}
@media(max-width:700px){:is(#wath,#wath-top) .hsub{display:none}}
:is(#wath,#wath-top) .hero-grid>div{gap:12px!important}
:is(#wath,#wath-top) .hero .match{padding:9px 14px;font-size:14.5px;line-height:1.4}
:is(#wath,#wath-top) .hero .fine{font-size:12.5px;margin-top:-2px}
:is(#wath,#wath-top) [data-hero] b,:is(#wath,#wath-top) [data-hero] .nms,:is(#wath,#wath-top) [data-hero] .hsub,:is(#wath,#wath-top) .kstats b,:is(#wath,#wath-top) [data-mneed]{font-variant-numeric:tabular-nums}
:is(#wath,#wath-top) .video{container-type:inline-size}
:is(#wath,#wath-top) .video:not(.playing):before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(27,21,38,.5) 0%,rgba(27,21,38,.12) 38%,rgba(27,21,38,0) 60%)}
:is(#wath,#wath-top) .vt{position:absolute;left:0;right:0;top:9%;display:flex;flex-direction:column;align-items:center;gap:1.4cqw;text-align:center;color:#fff;padding:0 4%;text-shadow:0 2px 18px rgba(27,21,38,.45)}
:is(#wath,#wath-top) .vt b{font-size:10.5cqw;line-height:.95;font-weight:900;letter-spacing:.01em;white-space:nowrap}
:is(#wath,#wath-top) .vt i{font-style:normal;font-size:3.5cqw;line-height:1.1;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#d9e2ff;white-space:nowrap}
:is(#wath,#wath-top) .play{top:60%}
:is(#wath,#wath-top) .video:not(.playing):before{background:linear-gradient(180deg,rgba(27,21,38,.55) 0%,rgba(27,21,38,.14) 40%,rgba(27,21,38,0) 62%,rgba(27,21,38,.5) 100%)}
:is(#wath,#wath-top) .vt{top:6%}
:is(#wath,#wath-top) .vt em,:is(#wath,#wath-top) .vb{font-style:normal;font-size:2.35cqw;line-height:1.2;font-weight:500;letter-spacing:.2em;text-transform:uppercase;color:#e6ebff;white-space:nowrap}
:is(#wath,#wath-top) .vt em{margin-bottom:.6cqw}
:is(#wath,#wath-top) .vt strong,:is(#wath,#wath-top) .vb strong{font-weight:800;color:#fff}
:is(#wath,#wath-top) .vb{margin-top:.5cqw}
:is(#wath,#wath-top) .vt{top:5%;gap:1.2cqw}
:is(#wath,#wath-top) .video .play{top:auto;bottom:6%;left:50%;transform:translateX(-50%);width:auto;height:auto;border-radius:999px;padding:.6em 1.25em .6em 1em;gap:.5em;font-size:max(13.5px,2.5cqw);font-weight:800;color:#1b1526;white-space:nowrap;box-shadow:0 6px 22px rgba(27,21,38,.35);transition:transform .15s}
:is(#wath,#wath-top) .video .play svg{width:1.05em;height:1.05em;flex:none}
:is(#wath,#wath-top) .video:hover .play{transform:translateX(-50%) scale(1.04)}
@media(max-width:700px){:is(#wath,#wath-top) .vt em,:is(#wath,#wath-top) .vb{font-size:2.9cqw;letter-spacing:.14em}}
:is(#wath,#wath-top) .card.tndd{padding:40px 40px 38px;gap:28px 40px;align-items:flex-start}
:is(#wath,#wath-top) .tndl{width:min(250px,100%);margin:4px auto 0}
:is(#wath,#wath-top) .tndt{min-width:min(100%,340px)}
:is(#wath,#wath-top) .tndt h2{font-size:27px;margin:8px 0 14px}
:is(#wath,#wath-top) .tndt .tndi{font-size:17px;line-height:1.6;margin:0 0 12px;color:#d6d9e6}
:is(#wath,#wath-top) .tndt .tndk{font-size:18px;font-weight:700;color:#fff;margin:0 0 4px;line-height:1.4}
:is(#wath,#wath-top) .tndq{margin:22px 0 26px;padding-left:18px}
@media(max-width:700px){:is(#wath,#wath-top) .card.tndd{padding:28px 22px 26px}:is(#wath,#wath-top) .tndt h2{font-size:23px}}
:is(#wath,#wath-top) .video:not(.playing){background-size:170% auto;background-position:50% 66%}
:is(#wath,#wath-top) .video .play{bottom:4.5%}
:is(#wath,#wath-top) .tmc{align-items:center;text-align:center;padding:18px 12px 16px;gap:3px}
:is(#wath,#wath-top) .tmp{width:84px;height:84px;border-radius:50%;object-fit:cover;background:#d9d3ec;margin-bottom:8px;display:block}
:is(#wath,#wath-top) .tm5{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
@media(max-width:700px){:is(#wath,#wath-top) .tm5{grid-template-columns:1fr 1fr}}
:is(#wath,#wath-top) .car{padding-left:28px;padding-right:28px;scroll-padding-left:28px}
:is(#wath,#wath-top) .car .ft{scroll-margin-left:0}
:is(#wath,#wath-top) .band .bandh{max-width:none;padding-left:28px;padding-right:28px}
:is(#wath,#wath-top) .band .carwrap>.wrap:last-child{max-width:none;padding-left:28px;padding-right:28px}
@media(max-width:700px){:is(#wath,#wath-top) .car,:is(#wath,#wath-top) .band .bandh,:is(#wath,#wath-top) .band .carwrap>.wrap:last-child{padding-left:18px;padding-right:18px}:is(#wath,#wath-top) .car{scroll-padding-left:18px}}
:is(#wath,#wath-top) .fa{position:absolute;left:0;right:0;top:54px;bottom:47%;display:flex;align-items:center;justify-content:center;padding:0 22px;z-index:0}
:is(#wath,#wath-top) .fa-win{width:100%;max-width:236px;background:#14101f;border-radius:12px;padding:8px;box-shadow:0 10px 26px rgba(20,14,50,.45);display:grid;gap:6px}
:is(#wath,#wath-top) .fa-win.g2{grid-template-columns:1fr 1fr}
:is(#wath,#wath-top) .fa-win.g31{grid-template-columns:2.1fr 1fr}
:is(#wath,#wath-top) .fa-t{border-radius:7px;background:#3a3350 center/cover;aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#d9d3ec;letter-spacing:.04em}
:is(#wath,#wath-top) .fa-t.you{outline:2px solid #f1d28a;color:#f1d28a;background:#2a2340}
:is(#wath,#wath-top) .fa-col{display:grid;gap:6px}
:is(#wath,#wath-top) .fa-cr{width:100%;max-width:236px;aspect-ratio:16/9;background:#0b0910;border-radius:8px;box-shadow:0 10px 26px rgba(20,14,50,.45);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px}
:is(#wath,#wath-top) .fa-cr small{font-size:8.5px;letter-spacing:.3em;color:#9a93ad;font-weight:700}
:is(#wath,#wath-top) .fa-cr i{display:block;height:5px;border-radius:3px;background:#3a3350}
:is(#wath,#wath-top) .fa-cr b{font-size:15px;color:#f1d28a;letter-spacing:.04em;font-weight:700}
:is(#wath,#wath-top) .fa-fs{display:flex;gap:6px;background:#14101f;padding:14px 8px;border-radius:6px;box-shadow:0 10px 26px rgba(20,14,50,.45);background-image:radial-gradient(circle,#d9d3ec 2px,transparent 2.6px),radial-gradient(circle,#d9d3ec 2px,transparent 2.6px);background-size:14px 8px,14px 8px;background-position:3px 3px,3px calc(100% - 3px);background-repeat:repeat-x;background-color:#14101f}
:is(#wath,#wath-top) .fa-fs span{width:66px;aspect-ratio:4/3;border-radius:3px;background:#3a3350 center/cover}
:is(#wath,#wath-top) .fa-dw{display:grid;grid-template-columns:repeat(4,44px);gap:8px}
:is(#wath,#wath-top) .fa-dw .av{width:44px;height:44px;border:2px solid rgba(255,255,255,.85);font-size:13px}
:is(#wath,#wath-top) .fa-dw .you{width:44px;height:44px;border-radius:50%;border:2px dashed #f1d28a;color:#f1d28a;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800}
:is(#wath,#wath-top) .fa svg{filter:drop-shadow(0 10px 18px rgba(20,14,50,.45))}
:is(#wath,#wath-top) .ups{padding-left:0;display:flex;flex-direction:column;gap:0;max-width:760px}
:is(#wath,#wath-top) .ups:before{display:none}
:is(#wath,#wath-top) .up{padding:0 0 34px}
:is(#wath,#wath-top) .up:before{display:none}
:is(#wath,#wath-top) .up:not(:last-child):after{content:"";position:absolute;left:50%;bottom:4px;width:2px;height:26px;background:#cfc8e6;border-radius:2px}
:is(#wath,#wath-top) .upc{background:#fff;border:1px solid #d9d3ec;border-radius:16px;padding:26px 30px 24px;box-shadow:0 2px 10px rgba(27,21,38,.05)}
:is(#wath,#wath-top) .upm{margin-bottom:10px}
:is(#wath,#wath-top) .upn{color:#6152a0}
:is(#wath,#wath-top) .upc h3{font-size:27px;margin:0 0 14px;letter-spacing:-.01em}
:is(#wath,#wath-top) .upa{margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid #ebe7f5}
:is(#wath,#wath-top) .upa em{font-style:normal;display:inline-block;margin-left:8px;font-size:11.5px;font-weight:800;letter-spacing:.04em;background:#ece7f7;color:#6152a0;border-radius:999px;padding:2px 9px;vertical-align:1px}
:is(#wath,#wath-top) .upa .upd{margin-left:auto;font-size:14px;color:#5b6478;text-align:right}
:is(#wath,#wath-top) .upk{background:#1b1526}
:is(#wath,#wath-top) .uplk{position:relative;max-height:4.9em;overflow:hidden;-webkit-mask-image:linear-gradient(180deg,#000 25%,transparent 100%);mask-image:linear-gradient(180deg,#000 25%,transparent 100%);user-select:none}
:is(#wath,#wath-top) .upgate{display:flex;gap:14px;align-items:center;flex-wrap:wrap;background:#f6f3fc;border:1px dashed #b9aee6;border-radius:12px;padding:14px 16px;margin-top:6px}
:is(#wath,#wath-top) .upgate>div{flex:1;min-width:200px;display:flex;flex-direction:column;gap:2px}
:is(#wath,#wath-top) .upgate b{font-size:15.5px;color:#1b1526}
:is(#wath,#wath-top) .upgate span{font-size:14px;color:#5b6478;line-height:1.4}
:is(#wath,#wath-top) .upgi{flex:none;width:38px;height:38px;border-radius:50%;background:#1b1526;color:#fff;display:flex;align-items:center;justify-content:center}
:is(#wath,#wath-top) .upgate .btn{min-height:40px;padding:0 16px;font-size:14.5px}
@media(max-width:600px){:is(#wath,#wath-top) .upc{padding:20px 18px}:is(#wath,#wath-top) .upc h3{font-size:22px}:is(#wath,#wath-top) .upa{flex-wrap:wrap}:is(#wath,#wath-top) .upa .upd{margin-left:0;width:100%;text-align:left}}
:is(#wath,#wath-top) .video:not(.playing):before{background:linear-gradient(180deg,rgba(27,21,38,.26) 0%,rgba(27,21,38,.04) 36%,rgba(27,21,38,0) 70%,rgba(27,21,38,.22) 100%);-webkit-backdrop-filter:brightness(1.3) saturate(1.12);backdrop-filter:brightness(1.3) saturate(1.12)}
:is(#wath,#wath-top) .vt{text-shadow:0 2px 14px rgba(27,21,38,.6),0 0 2px rgba(27,21,38,.35)}
:is(#wath,#wath-top) .video:not(.playing){background-image:none;background-color:#55507e}
:is(#wath,#wath-top) .vk{position:absolute;inset:0;overflow:hidden;z-index:0}
:is(#wath,#wath-top) .vk i{position:absolute;inset:0;background:var(--ph) center 30%/cover no-repeat;will-change:transform,opacity}
:is(#wath,#wath-top) .vk .k1{transform-origin:50% 68%;transform:scale(1.7);animation:wathK1 26s linear infinite}
:is(#wath,#wath-top) .vk .k2{transform-origin:50% 62%;opacity:0;animation:wathK2 26s linear infinite}
:is(#wath,#wath-top) .vk .k3{transform-origin:14% 62%;opacity:0;animation:wathK3 26s linear infinite}
@keyframes wathK1{0%{transform:scale(1.12)}40%{transform:scale(1.75)}95%{transform:scale(1.75)}95.01%{transform:scale(1.12)}100%{transform:scale(1.12)}}
@keyframes wathK2{0%,37%{opacity:0;transform:scale(2.35)}40%{opacity:1}66%{opacity:1}69%,100%{opacity:0;transform:scale(2.65)}}
@keyframes wathK3{0%,66%{opacity:0;transform:scale(1.75) translateX(0)}69%{opacity:1}96%{opacity:1}100%{opacity:0;transform:scale(1.75) translateX(-5%)}}
:is(#wath,#wath-top) .video:not(.playing):before{z-index:1}
:is(#wath,#wath-top) .video .vt,:is(#wath,#wath-top) .video .play{z-index:2}
:is(#wath,#wath-top) .vt>*{opacity:0;animation:wathUp .9s cubic-bezier(.2,.7,.2,1) forwards}
:is(#wath,#wath-top) .vt>*:nth-child(1){animation-delay:.3s}:is(#wath,#wath-top) .vt>*:nth-child(2){animation-delay:.7s}:is(#wath,#wath-top) .vt>*:nth-child(3){animation-delay:1.2s}:is(#wath,#wath-top) .vt>*:nth-child(4){animation-delay:1.6s}
:is(#wath,#wath-top) .vt{animation:wathFloat 9s ease-in-out 2.6s infinite}
@keyframes wathUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes wathFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
@media(prefers-reduced-motion:reduce){:is(#wath,#wath-top) .vk i,:is(#wath,#wath-top) .vt,:is(#wath,#wath-top) .vt>*{animation:none!important}:is(#wath,#wath-top) .vt>*{opacity:1}:is(#wath,#wath-top) .vk .k2,:is(#wath,#wath-top) .vk .k3{opacity:0}}
:is(#wath,#wath-top) .tov{position:fixed;inset:0;z-index:100000;background:rgba(14,10,24,.9);display:flex;align-items:center;justify-content:center;padding:56px 24px 24px;animation:wathFade .25s ease}
:is(#wath,#wath-top) .tovf{position:relative;width:min(100%,calc((100vh - 96px)*16/9));aspect-ratio:16/9;background:#000;border-radius:10px;overflow:hidden;box-shadow:0 24px 80px rgba(0,0,0,.6)}
:is(#wath,#wath-top) .tovf iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
:is(#wath,#wath-top) .tovx{position:absolute;top:10px;right:14px;width:44px;height:44px;border-radius:50%;border:0;background:rgba(255,255,255,.14);color:#fff;font-size:28px;line-height:1;cursor:pointer}
:is(#wath,#wath-top) .tovx:hover{background:rgba(255,255,255,.28)}
@keyframes wathFade{from{opacity:0}to{opacity:1}}
html.wath-noscroll{overflow:hidden}
@media(max-width:700px){:is(#wath,#wath-top) .tov{padding:56px 0 24px}:is(#wath,#wath-top) .tovf{border-radius:0}}
:is(#wath,#wath-top) .fa{bottom:50%}
:is(#wath,#wath-top) .fa-win.g2{max-width:176px}
:is(#wath,#wath-top) .fa-win.g2 .fa-t{aspect-ratio:16/10}
:is(#wath,#wath-top) .fa svg{height:96px;width:auto}
:is(#wath,#wath-top) .ups{max-width:none}
:is(#wath,#wath-top) .match .mh{display:block;color:#2c2208;font-size:16.5px;font-weight:800;margin-bottom:2px}
:is(#wath,#wath-top) .match b{color:#2c2208}
:is(#wath,#wath-top) .shr{display:flex;align-items:center;gap:10px 22px;flex-wrap:wrap;margin-top:26px;padding:14px 2px;border-top:1px solid rgba(27,21,38,.14);border-bottom:1px solid rgba(27,21,38,.14)}
:is(#wath,#wath-top) .shl{font-size:12.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#5b6478}
:is(#wath,#wath-top) .shb{display:flex;gap:6px 8px;flex-wrap:wrap}
:is(#wath,#wath-top) .sh1{display:inline-flex;align-items:center;gap:7px;min-height:36px;padding:0 13px;border-radius:999px;border:1px solid rgba(27,21,38,.18);background:transparent;color:#1b1526;font:inherit;font-size:14px;font-weight:700;text-decoration:none;cursor:pointer;transition:background .15s,border-color .15s}
:is(#wath,#wath-top) .sh1:hover{background:#fff;border-color:#6152a0;color:#6152a0}
:is(#wath,#wath-top) .shc{margin-left:auto;font-size:14.5px;font-weight:700;color:#6152a0;text-decoration:none}
:is(#wath,#wath-top) .shc:hover{text-decoration:underline}
:is(#wath,#wath-top) .hero{padding-bottom:0}
@media(max-width:700px){:is(#wath,#wath-top) .shr{margin-top:18px;padding:12px 0}:is(#wath,#wath-top) .shl{width:100%}:is(#wath,#wath-top) .shc{margin-left:0}}
:is(#wath,#wath-top) .cnt{display:inline-block;vertical-align:.55em;margin-left:5px;font-size:10.5px;font-weight:800;letter-spacing:0;line-height:1;background:rgba(97,82,160,.16);color:#6152a0;border-radius:999px;padding:3px 6px;font-variant-numeric:tabular-nums}
:is(#wath,#wath-top) .cnt:empty{display:none}
:is(#wath,#wath-top) h2 .cnt{font-size:13px;padding:4px 8px;vertical-align:.5em;margin-left:8px}
:is(#wath,#wath-top) .subnav .snl a.on .cnt{background:rgba(255,255,255,.25);color:#fff}
@media(min-width:1241px){:is(#wath,#wath-top) .subnav .snl a{letter-spacing:.06em;padding:13px 8px;font-size:12.5px}:is(#wath,#wath-top) .subnav .snl{margin-left:-8px}}
@media(min-width:901px) and (max-width:1240px){:is(#wath,#wath-top) .subnav .snl a{letter-spacing:.03em;padding:13px 5px;font-size:12px}:is(#wath,#wath-top) .subnav .snl{margin-left:-5px}:is(#wath,#wath-top) .subnav .btn{min-width:96px}}
:is(#wath,#wath-top) .taxn{display:flex;gap:9px;align-items:flex-start;color:#33697f}
:is(#wath,#wath-top) .taxn svg{flex:none;margin-top:1px}
:is(#wath,#wath-top) .taxn b{display:block;font-size:15.5px;color:#1b1526;line-height:1.25}
:is(#wath,#wath-top) .taxn span{display:block;font-size:13px;color:#5b6478;line-height:1.4;margin-top:2px}
:is(#wath,#wath-top) .subnav .snl a{display:inline-flex;align-items:center;flex:none}
:is(#wath,#wath-top) .subnav .snl .cnt{vertical-align:0;align-self:flex-start;margin-top:-3px;line-height:1}
:is(#wath,#wath-top) .hero-grid{grid-template-rows:auto 1fr;row-gap:0}
:is(#wath,#wath-top) .hero-grid>.video{grid-column:1;grid-row:1}
:is(#wath,#wath-top) .hero-grid>div:not(.shr){grid-column:2;grid-row:1/span 2}
:is(#wath,#wath-top) .hero-grid>.shr{grid-column:1;grid-row:2;align-self:start;margin-top:14px;padding:10px 2px;gap:8px 14px}
:is(#wath,#wath-top) .hero-grid>.shr{flex-direction:row!important}
:is(#wath,#wath-top) .sh1{width:38px;height:38px;min-height:0;padding:0;justify-content:center;border-radius:50%;border-color:rgba(27,21,38,.16);color:#3a3350}
:is(#wath,#wath-top) .sh1:hover{background:#6152a0;border-color:#6152a0;color:#fff}
:is(#wath,#wath-top) .hero{padding-bottom:26px}
@media(max-width:700px){:is(#wath,#wath-top) .shr{margin-top:16px}:is(#wath,#wath-top) .shl{width:auto}:is(#wath,#wath-top) .shc{margin-left:auto}}
:is(#wath,#wath-top) .upgate .upga{flex:none;display:flex;flex-direction:row;align-items:center;gap:10px}
:is(#wath,#wath-top) .upgate .upgo{font-size:13.5px;color:#5b6478}
:is(#wath,#wath-top) .hero-grid>.shr{align-self:end;margin-top:22px}
:is(#wath,#wath-top) .hero .match{padding:0;overflow:hidden}
:is(#wath,#wath-top) .mx{display:flex;align-items:center;gap:12px;width:100%;text-align:left;background:none;border:0;padding:12px 14px;font:inherit;font-size:14.5px;line-height:1.4;color:#5a4a1c;cursor:pointer}
:is(#wath,#wath-top) .mx:hover{background:rgba(201,154,62,.1)}
:is(#wath,#wath-top) .mxi{position:relative;flex:none;width:44px;height:44px;border-radius:50%;background:#f1d28a;color:#2c2208;display:flex;align-items:center;justify-content:center}
:is(#wath,#wath-top) .mxi em{position:absolute;right:-5px;top:-4px;font-style:normal;font-size:11px;font-weight:800;background:#2c2208;color:#f1d28a;border-radius:999px;padding:2px 5px;line-height:1}
:is(#wath,#wath-top) .mxt{flex:1;min-width:0}
:is(#wath,#wath-top) .mx .chev{flex:none;color:#7a5c14;transition:transform .2s}
:is(#wath,#wath-top) .mx[aria-expanded=true] .chev{transform:rotate(180deg)}
:is(#wath,#wath-top) .mxd{padding:2px 14px 14px;border-top:1px solid rgba(201,154,62,.35);display:flex;flex-direction:column;gap:10px}
:is(#wath,#wath-top) .mxd[hidden]{display:none}
:is(#wath,#wath-top) .mxd p{margin:10px 0 0;font-size:14px;line-height:1.45;color:#5a4a1c}
:is(#wath,#wath-top) .mxr{display:grid;grid-template-columns:1fr auto;gap:1px 10px;font-size:14px;color:#5a4a1c}
:is(#wath,#wath-top) .mxr .mxs{grid-column:1/-1;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8a7a4a}
:is(#wath,#wath-top) .mxr.live .mxs{color:#7a5c14}
:is(#wath,#wath-top) .mxr.done .mxs{color:#33697f}
:is(#wath,#wath-top) .mxr b{color:#2c2208;font-size:15px}
:is(#wath,#wath-top) .mxr .mxa{text-align:right;white-space:nowrap}
:is(#wath,#wath-top) .mxr .bar{grid-column:1/-1;height:7px;margin-top:4px;background:rgba(201,154,62,.25)}
:is(#wath,#wath-top) .mxr .bar i{background:#c99a3e}
:is(#wath,#wath-top) .mxd a{font-weight:700;font-size:14.5px;color:#7a5c14}
@media(max-width:420px){:is(#wath,#wath-top) .mxr{grid-template-columns:1fr}:is(#wath,#wath-top) .mxr .mxa{text-align:left}}
:is(#wath,#wath-top) .mxb{display:block;height:8px;margin:8px 0 6px;background:rgba(201,154,62,.25)}
:is(#wath,#wath-top) .mxb i{background:#c99a3e}
:is(#wath,#wath-top) .mxl{display:block;font-size:13.5px;color:#5a4a1c;font-variant-numeric:tabular-nums}
:is(#wath,#wath-top) .mxl b{font-size:15px}
:is(#wath,#wath-top) .mx{align-items:flex-start}
:is(#wath,#wath-top) .mx .chev{margin-top:4px}
:is(#wath,#wath-top) .mx{position:relative}
:is(#wath,#wath-top) .mx .chev{position:absolute;right:13px;top:13px;margin:0}
:is(#wath,#wath-top) .mx .mh{padding-right:22px}
#wath-top .mov{position:fixed;inset:0;z-index:100000;background:#ece7f7;display:flex;flex-direction:column;animation:wathFade .2s ease;color:#1b1526}
#wath-top .minner{width:100%;max-width:980px;margin:0 auto;padding:0 24px}
#wath-top .mtop{background:#6f74aa;color:#fff;flex:none}
#wath-top .mtop .minner:first-child{display:flex;align-items:center;gap:14px;padding-top:12px;padding-bottom:8px}
#wath-top .mlogo{font-size:18px;font-weight:900;letter-spacing:.02em}
#wath-top .mlogo span{font-weight:600;opacity:.85;letter-spacing:0;margin-left:6px}
#wath-top .msamp{margin-left:auto;background:#f1d28a;color:#2c2208;border-radius:999px;padding:4px 12px;font-size:12.5px;font-weight:800}
#wath-top .mx2{flex:none;width:38px;height:38px;border-radius:50%;border:0;background:rgba(255,255,255,.18);color:#fff;font-size:24px;line-height:1;cursor:pointer}
#wath-top .mtabs{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;padding-bottom:0}
#wath-top .mtabs::-webkit-scrollbar{display:none}
#wath-top .mt{flex:none;background:none;border:0;border-bottom:3px solid transparent;color:rgba(255,255,255,.82);font:inherit;font-size:14.5px;font-weight:700;padding:10px 12px;cursor:pointer;white-space:nowrap}
#wath-top .mt.on{color:#fff;border-bottom-color:#fff}
#wath-top .mbody{flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch}
#wath-top .mmain{padding-top:26px;padding-bottom:60px;display:flex;flex-direction:column;gap:14px}
#wath-top .mmain h2{font-size:26px;margin:0 0 4px;color:#1b1526}
#wath-top .mcard{background:#fff;border:1px solid #d9d3ec;border-radius:16px;padding:20px 22px;text-align:left;font:inherit;color:inherit;display:block;width:100%}
#wath-top .mrow{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
#wath-top .mtag{display:block;font-size:11.5px;font-weight:800;letter-spacing:.12em;color:#6152a0;margin-bottom:4px}
#wath-top .mbig{display:block;font-size:28px;line-height:1.1}
#wath-top .mh3{display:block;font-size:19px;line-height:1.2;margin-bottom:4px}
#wath-top .msub{display:block;font-size:14.5px;color:#5b6478;line-height:1.45;margin:4px 0 0}
#wath-top .mgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
#wath-top .mgrid.two{grid-template-columns:repeat(2,1fr)}
#wath-top .mact{cursor:pointer;display:flex;flex-direction:column;gap:4px;color:#6152a0;transition:border-color .15s,transform .15s}
#wath-top .mact:hover{border-color:#6152a0;transform:translateY(-1px)}
#wath-top .mact b{font-size:17px;color:#1b1526;margin-top:6px}
#wath-top .mact span{font-size:14px;color:#5b6478;line-height:1.4}
#wath-top .mchips{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
#wath-top .mchip{border:1px solid #cfc8e6;background:#f6f3fc;border-radius:999px;padding:8px 14px;font:inherit;font-size:14.5px;font-weight:700;color:#1b1526;cursor:pointer}
#wath-top .mchip.on{background:#6152a0;border-color:#6152a0;color:#fff}
#wath-top .mlink{background:none;border:0;padding:0;font:inherit;font-size:14.5px;font-weight:700;color:#6152a0;cursor:pointer;text-decoration:underline;align-self:flex-start}
#wath-top .mtab{width:100%;border-collapse:collapse;margin:6px 0 10px;font-size:15px}
#wath-top .mtab td{padding:11px 4px;border-top:1px solid #ebe7f5;vertical-align:top}
#wath-top .mtab td:first-child{color:#5b6478;white-space:nowrap;width:1%;padding-right:18px}
#wath-top .mtab td:last-child{text-align:right;width:1%}
#wath-top .mtab td span{display:block;font-size:13px;color:#7a5c14}
#wath-top .mtot td{border-top:2px solid #d9d3ec;font-weight:700}
#wath-top .mprof{display:flex;gap:14px;align-items:center;margin-bottom:8px}
#wath-top .mav{width:64px;height:64px;border-radius:50%;background:#d9d3ec;color:#6152a0;font-weight:800;font-size:20px;display:flex;align-items:center;justify-content:center;flex:none}
#wath-top .mf{display:block;margin:14px 0;position:relative}
#wath-top .mf>span{display:block;font-size:13.5px;font-weight:700;margin-bottom:5px}
#wath-top .mf input,#wath-top .mf textarea{width:100%;box-sizing:border-box;border:1px solid #cfc8e6;border-radius:10px;padding:10px 12px;font:inherit;font-size:15.5px;background:#fff;color:#1b1526}
#wath-top .mf input:disabled{background:#f3f0f9;color:#8a84a0}
#wath-top .mf em{font-style:normal;display:inline-flex;gap:5px;align-items:center;font-size:13px;color:#6152a0;font-weight:700;margin-top:5px}
#wath-top .mck{display:flex;gap:8px;align-items:center;font-size:15px;margin:4px 0 16px}
#wath-top .mup{display:flex;gap:12px;align-items:flex-start;cursor:pointer}
#wath-top .mup:hover{border-color:#6152a0}
#wath-top .mdot{flex:none;width:10px;height:10px;border-radius:50%;background:#6152a0;margin-top:7px}
#wath-top .mup.rd .mdot{background:transparent;border:2px solid #cfc8e6;box-sizing:border-box}
#wath-top .mup.lk .mdot{background:#cfc8e6}
#wath-top .mupt{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}
#wath-top .mupt b{font-size:17.5px}
#wath-top .mup.rd .mupt b{font-weight:600}
#wath-top .mupt>span{font-size:13.5px;color:#5b6478;display:inline-flex;gap:5px;align-items:center;flex-wrap:wrap}
#wath-top .mupt em{font-style:normal;font-size:14.5px;color:#3a4051;line-height:1.45}
#wath-top .mup.lk .mupt em{filter:blur(3.5px);user-select:none}
#wath-top .mst{flex:none;font-size:12px;font-weight:800;border-radius:999px;padding:3px 10px;background:#6152a0;color:#fff}
#wath-top .mup.rd .mst{background:#ece7f7;color:#5b6478}
#wath-top .mup.lk .mst{background:#1b1526}
#wath-top .mcode{font-family:ui-monospace,Menlo,monospace;letter-spacing:.06em;background:#f6f3fc;border:1px dashed #b9aee6;border-radius:8px;padding:8px 10px;display:inline-block;margin:4px 0}
#wath-top .mcard .btn{margin-top:12px}
#wath-top .mrow .btn{margin-top:0}
#wath-top .lkc{background:#f6f3fc}
#wath-top .mlk{display:inline-flex;gap:6px;align-items:center;font-size:13.5px;font-weight:800;color:#6152a0;margin-top:10px}
#wath-top .lkc .btn{display:block}
#wath-top .mpk{display:flex;gap:10px;align-items:center;padding:9px 0;border-top:1px solid #ebe7f5;font-size:15px;color:#8a84a0}
#wath-top .mpk.ok{color:#1b1526}
#wath-top .mpi{flex:none;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#ece7f7;color:#8a84a0;font-size:12px;font-weight:800}
#wath-top .mpk.ok .mpi{background:#33697f;color:#fff}
#wath-top .mpn{flex:1}
#wath-top .mpl{font-size:13px;font-weight:700}
#wath-top .msw{display:flex;gap:12px;align-items:flex-start;padding:12px 0;border-top:1px solid #ebe7f5;cursor:pointer}
#wath-top .msw input{position:absolute;opacity:0}
#wath-top .msw i{flex:none;width:40px;height:22px;border-radius:999px;background:#cfc8e6;position:relative;transition:background .15s;margin-top:2px}
#wath-top .msw i:after{content:"";position:absolute;left:2px;top:2px;width:18px;height:18px;border-radius:50%;background:#fff;transition:transform .15s}
#wath-top .msw input:checked+i{background:#6152a0}
#wath-top .msw input:checked+i:after{transform:translateX(18px)}
#wath-top .msw input:focus-visible+i{outline:2px solid #1b1526;outline-offset:2px}
#wath-top .msw span{font-size:14px;color:#5b6478;line-height:1.4}
#wath-top .msw span b{display:block;font-size:15.5px;color:#1b1526}
#wath-top .mov .soon{display:inline-block}
#wath-top #wath-toast{z-index:100002}
@media(max-width:700px){#wath-top .minner{padding:0 16px}#wath-top .mgrid,#wath-top .mgrid.two{grid-template-columns:1fr}#wath-top .msamp{font-size:11px;padding:3px 9px;margin-left:auto;max-width:150px;text-align:center}#wath-top .mlogo span{display:none}#wath-top .mcard{padding:16px}#wath-top .mmain h2{font-size:23px}}
@media(max-width:700px){#wath-top .msamp{font-size:0;max-width:none;padding:4px 10px}#wath-top .msamp:after{content:"Sample preview";font-size:12px}}
#wath-top .mlinks{display:grid;grid-template-columns:1fr 1fr;gap:8px 12px}
#wath-top .mlinks label{display:flex;align-items:center;border:1px solid #cfc8e6;border-radius:10px;background:#fff;overflow:hidden}
#wath-top .mlinks i{font-style:normal;flex:none;width:86px;padding:0 0 0 12px;font-size:13.5px;font-weight:700;color:#6152a0}
#wath-top .mlinks input{border:0;border-radius:0;padding:10px 12px 10px 0;min-width:0;flex:1}
#wath-top .mlinks input:focus{outline:none}
#wath-top .mlinks label:focus-within{border-color:#6152a0;box-shadow:0 0 0 2px rgba(97,82,160,.2)}
#wath-top .mf>em{color:#5b6478;font-weight:400}
@media(max-width:700px){#wath-top .mlinks{grid-template-columns:1fr}}
#wath-top .maddr{display:grid;grid-template-columns:1fr 1fr;gap:8px 12px}
#wath-top .maddr .w2{grid-column:1/-1}
#wath-top .mpriv{display:inline-block;margin-left:6px;font-size:11px;font-weight:800;letter-spacing:.04em;background:#1b1526;color:#fff;border-radius:999px;padding:2px 8px;vertical-align:1px}
@media(max-width:700px){#wath-top .maddr{grid-template-columns:1fr}}
:is(#wath,#wath-top) button.tmc{font:inherit;color:inherit;cursor:pointer;transition:border-color .15s,transform .15s}
:is(#wath,#wath-top) button.tmc:hover{border-color:#6152a0;transform:translateY(-2px)}
:is(#wath,#wath-top) .tmc em{font-style:normal;font-size:13px;font-weight:700;color:#6152a0;margin-top:6px}
:is(#wath,#wath-top) .bov{position:fixed;inset:0;z-index:100000;background:rgba(14,10,24,.72);display:flex;align-items:center;justify-content:center;padding:20px;animation:wathFade .2s ease}
:is(#wath,#wath-top) .bovc{position:relative;background:#fff;border-radius:18px;max-width:560px;width:100%;max-height:calc(100vh - 40px);overflow:auto;padding:30px 30px 26px;color:#1b1526;box-shadow:0 24px 80px rgba(0,0,0,.4)}
:is(#wath,#wath-top) .bovh{display:flex;gap:16px;align-items:center;margin-bottom:16px;padding-right:30px}
:is(#wath,#wath-top) .bovh img{width:96px;height:96px;border-radius:50%;object-fit:cover;flex:none;background:#d9d3ec}
:is(#wath,#wath-top) .bovh b{display:block;font-size:24px;line-height:1.15}
:is(#wath,#wath-top) .bovh span{display:block;font-size:14px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#6152a0;margin-top:4px}
:is(#wath,#wath-top) .bovc p{font-size:16.5px;line-height:1.6;color:#3a4051;margin:0}
:is(#wath,#wath-top) .bovx{position:absolute;top:12px;right:12px;width:38px;height:38px;border-radius:50%;border:0;background:#ece7f7;color:#1b1526;font-size:24px;line-height:1;cursor:pointer}
:is(#wath,#wath-top) .chf{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}
:is(#wath,#wath-top) .chf .btn{display:inline-flex;align-items:center;text-decoration:none}
:is(#wath,#wath-top) .cha{display:flex;gap:8px 12px;flex-wrap:wrap;align-items:center;margin-top:2px}
:is(#wath,#wath-top) .cha .btn{min-height:36px;font-size:13.5px;padding:0 13px}
:is(#wath,#wath-top) .cha .chl{background:none;border:0;padding:0;font:inherit;font-size:13.5px;font-weight:700;color:#6152a0;cursor:pointer;text-decoration:underline}
:is(#wath,#wath-top) .chn{font-size:13px;color:#5b6478;line-height:1.4}
@media(max-width:700px){:is(#wath,#wath-top) .bovc{padding:24px 20px 20px}:is(#wath,#wath-top) .bovh img{width:76px;height:76px}:is(#wath,#wath-top) .bovh b{font-size:21px}}
#wath-top .mtop.adm{background:#1b1526}
#wath-top .mswap{flex:none;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.35);color:#fff;border-radius:999px;padding:6px 13px;font:inherit;font-size:13px;font-weight:700;cursor:pointer}
#wath-top .mswap:hover{background:rgba(255,255,255,.3)}
#wath-top .mgrid.four{grid-template-columns:repeat(4,1fr)}
#wath-top .astat b{display:block;font-size:27px;line-height:1.15;font-variant-numeric:tabular-nums}
#wath-top .astat span:last-child{display:block;font-size:13.5px;color:#5b6478;margin-top:3px;line-height:1.35}
#wath-top .asmp{display:inline-block;background:#f1d28a;color:#2c2208;border-radius:999px;padding:1px 8px;font-size:10.5px;font-weight:800;letter-spacing:.02em;vertical-align:1px;margin-left:4px}
#wath-top .abar{display:grid;grid-template-columns:minmax(120px,42%) 1fr 48px;gap:10px;align-items:center;font-size:14px;padding:6px 0;color:#3a4051}
#wath-top .abar .bar{height:8px}
#wath-top .abar b{text-align:right;font-variant-numeric:tabular-nums;color:#1b1526}
#wath-top .asearch{flex:1;min-width:180px;border:1px solid #cfc8e6;border-radius:10px;padding:10px 12px;font:inherit;font-size:15px}
#wath-top .mtab th{text-align:left;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#5b6478;padding:10px 4px 8px}
#wath-top .asup td,#wath-top .asup td:first-child,#wath-top .asup td:last-child{width:auto;text-align:left;white-space:normal;color:#1b1526;padding-right:10px}
#wath-top .apill{display:inline-block;border-radius:999px;padding:2px 10px;font-size:12px;font-weight:800;background:#ece7f7;color:#5b6478;white-space:nowrap}
#wath-top .apill.on{background:#33697f;color:#fff}
#wath-top .mav.sm{width:40px;height:40px;font-size:14px}
#wath-top .ainv{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;padding-top:14px;border-top:1px solid #ebe7f5}
#wath-top .ainv input{flex:1;min-width:180px;border:1px solid #cfc8e6;border-radius:10px;padding:10px 12px;font:inherit;font-size:15px}
#wath-top .ainv select{border:1px solid #cfc8e6;border-radius:10px;padding:0 10px;font:inherit;font-size:15px;background:#fff;min-height:44px}
#wath-top .ainv .btn{margin-top:0}
#wath-top .aperm{overflow-x:auto}
#wath-top .aperm table{min-width:520px}
#wath-top .aperm td,#wath-top .aperm td:first-child,#wath-top .aperm td:last-child{width:auto;text-align:center;white-space:normal;color:#1b1526}
#wath-top .aperm td:first-child{text-align:left}
#wath-top .aperm th:not(:first-child){text-align:center}
#wath-top .ayes{color:#33697f;font-weight:800}
#wath-top .ano{color:#b9b3cc}
#wath-top .mpk .mlink{align-self:center}
@media(max-width:900px){#wath-top .mgrid.four{grid-template-columns:1fr 1fr}}
@media(max-width:700px){#wath-top .mswap{padding:5px 9px;font-size:12px}#wath-top .abar{grid-template-columns:minmax(96px,44%) 1fr 40px}}
#wath-top .mav{overflow:hidden;position:relative}
#wath-top .mav img{width:100%;height:100%;object-fit:cover;display:block}
#wath-top .mav.lkd img{filter:grayscale(1) opacity(.55)}
#wath-top .mfile{display:inline-flex;align-items:center;cursor:pointer;position:relative;margin-top:0}
#wath-top .mfile input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%}
#wath-top .mprof .mlink{margin-left:10px}
#wath-top .mpub{background:#f6f3fc}
#wath-top .mvis{display:flex;flex-direction:column;gap:9px;margin-top:6px;font-size:14.5px;color:#3a4051}
#wath-top .mvis>div{display:flex;gap:10px;align-items:flex-start;line-height:1.4}
#wath-top .mvis .apill{flex:none;min-width:92px;text-align:center;display:inline-flex;gap:4px;align-items:center;justify-content:center}
#wath-top .apill.dk{background:#1b1526;color:#fff}
#wath-top .mov input[type=checkbox]{width:auto!important;flex:none;margin:0}
#wath-top .mck{justify-content:flex-start}
#wath-top .mlogo,#wath-top .msamp,#wath-top .mswap{white-space:nowrap}
@media(max-width:700px){#wath-top .mtop .minner:first-child{gap:8px}#wath-top .mlogo{font-size:15px}#wath-top .msamp:after{content:"Sample";font-size:11.5px}#wath-top .msamp{padding:3px 8px}#wath-top .mx2{width:34px;height:34px}}
:is(#wath,#wath-top) .vk .k2,:is(#wath,#wath-top) .vk .k3{display:none}
:is(#wath,#wath-top) .vk .k1{transform-origin:50% 74%;animation:wathZoom 30s linear infinite}
@keyframes wathZoom{0%{transform:scale(1.1);opacity:0}3%{opacity:1}82%{transform:scale(2.6);opacity:1}95%{transform:scale(2.6);opacity:1}100%{transform:scale(2.6);opacity:0}}
@media(prefers-reduced-motion:reduce){:is(#wath,#wath-top) .vk .k1{transform:scale(1.7)}}
#wath-top .mob{max-width:640px;margin:0 auto;width:100%;display:flex;flex-direction:column;gap:16px}
#wath-top .mobs{display:flex;gap:8px 18px;flex-wrap:wrap;font-size:13.5px;font-weight:700;color:#8a84a0}
#wath-top .mobs span{display:inline-flex;align-items:center;gap:7px}
#wath-top .mobs i{font-style:normal;width:24px;height:24px;border-radius:50%;background:#d9d3ec;color:#5b6478;display:inline-flex;align-items:center;justify-content:center;font-size:12.5px}
#wath-top .mobs .on{color:#1b1526}
#wath-top .mobs .on i{background:#6152a0;color:#fff}
#wath-top .mobs .dn i{background:#33697f;color:#fff}
#wath-top .mobn{display:flex;gap:12px;align-items:center;margin-top:20px;flex-wrap:wrap}
#wath-top .mobn .btn{margin-top:0}
#wath-top .mobn .btn.pri{margin-left:auto}
#wath-top .mobn .mlink{align-self:center}
#wath-top .mnl{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:6px 0 14px}
#wath-top .mnl b{display:block;font-size:24px;line-height:1.15;font-variant-numeric:tabular-nums}
#wath-top .mnl span{display:block;font-size:13.5px;color:#5b6478;line-height:1.35;margin-top:2px}
#wath-top .mkn{display:flex;flex-direction:column;border-top:1px solid #ebe7f5}
#wath-top .mknr{display:flex;gap:10px;align-items:center;text-align:left;background:none;border:0;border-bottom:1px solid #ebe7f5;padding:11px 2px;font:inherit;font-size:15px;color:#1b1526;cursor:pointer}
#wath-top .mknr:last-child{border-bottom:0}
#wath-top .mknr:hover{color:#6152a0}
#wath-top .mknr i{flex:none;width:8px;height:8px;border-radius:50%;background:#6152a0}
#wath-top .mfeed{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:10px;margin:12px 0 4px}
#wath-top .mfi{display:block;aspect-ratio:1/1;border-radius:12px;background:#3a3350 center/cover;border:0;padding:0;position:relative;overflow:hidden}
#wath-top .mfi.vid{aspect-ratio:auto;cursor:pointer}
#wath-top .mfi.vid span{position:absolute;left:12px;bottom:12px;background:rgba(255,255,255,.94);color:#1b1526;border-radius:999px;padding:7px 13px;font:inherit;font-size:13.5px;font-weight:800}
@media(max-width:700px){#wath-top .mnl{grid-template-columns:1fr}#wath-top .mfeed{grid-template-columns:1fr 1fr}#wath-top .mfi.vid{grid-column:1/-1;aspect-ratio:16/9}#wath-top .mfeed .mfi:last-child{display:none}}
:is(#wath,#wath-top) .flim{font-size:12px;font-weight:800;background:rgba(255,255,255,.94);color:#1b1526;border-radius:999px;padding:3px 9px;white-space:nowrap}
:is(#wath,#wath-top) .flim.low{background:#f1d28a;color:#2c2208}
:is(#wath,#wath-top) .flim.out{background:#1b1526;color:#fff}
:is(#wath,#wath-top) .ft.out{filter:saturate(.55)}
:is(#wath,#wath-top) .ft.out .fb .btn{background:rgba(255,255,255,.92);color:#1b1526;border-color:transparent}
#wath-top .asw{flex:none;width:40px;height:22px;border-radius:999px;background:#cfc8e6;border:0;position:relative;cursor:pointer;padding:0;transition:background .15s}
#wath-top .asw i{position:absolute;left:2px;top:2px;width:18px;height:18px;border-radius:50%;background:#fff;transition:transform .15s}
#wath-top .asw.on{background:#6152a0}
#wath-top .asw.on i{transform:translateX(18px)}
#wath-top .ainvt td,#wath-top .ainvt td:first-child,#wath-top .ainvt td:last-child{width:auto;text-align:left;white-space:normal;color:#1b1526;vertical-align:middle;padding-right:10px}
#wath-top .ainvt td:first-child span{color:#5b6478}
#wath-top .ainvt tr.off td:first-child{opacity:.5}
#wath-top .anum{width:74px;border:1px solid #cfc8e6;border-radius:8px;padding:7px 8px;font:inherit;font-size:15px}
#wath-top .astep{display:inline-flex;align-items:center;gap:8px}
#wath-top .astep button{width:28px;height:28px;border-radius:50%;border:1px solid #cfc8e6;background:#fff;font:inherit;font-size:16px;line-height:1;cursor:pointer;color:#1b1526}
#wath-top .astep b{min-width:22px;text-align:center;font-variant-numeric:tabular-nums}
#wath-top .apill.warn{background:#f1d28a;color:#2c2208}
#wath-top .aperm .ainvt{min-width:640px}
.wath-chip{display:inline-flex;align-items:center;gap:7px;vertical-align:middle}
.wath-chip-arr{display:inline-flex;align-items:center;align-self:stretch;padding:6px 0 6px 4px;margin:-6px 0;cursor:pointer}
.wath-chip-av{width:28px;height:28px;border-radius:50%;background:#fff;color:#6152a0;font-size:11px;font-weight:800;display:inline-flex;align-items:center;justify-content:center;overflow:hidden;letter-spacing:0}
.wath-chip-av img{width:100%;height:100%;object-fit:cover;display:block}
#wath-top .acm{position:fixed;z-index:99990;width:264px;background:#fff;border:1px solid #d9d3ec;border-radius:14px;box-shadow:0 18px 50px rgba(27,21,38,.25);padding:8px;display:flex;flex-direction:column;animation:wathFade .15s ease;color:#1b1526}
#wath-top .acmh{display:flex;gap:10px;align-items:center;padding:8px 8px 12px;border-bottom:1px solid #ebe7f5;margin-bottom:6px}
#wath-top .acmh .mav{width:42px;height:42px;font-size:14px}
#wath-top .acmh b{display:block;font-size:15.5px}
#wath-top .acmh span{display:block;font-size:13px;color:#5b6478}
#wath-top .acm button{background:none;border:0;text-align:left;font:inherit;font-size:15px;padding:9px 10px;border-radius:8px;cursor:pointer;color:#1b1526}
#wath-top .acm button:hover{background:#f1edf9;color:#6152a0}
#wath-top .acm .adm{border-top:1px solid #ebe7f5;border-radius:0 0 8px 8px;margin-top:6px;padding-top:12px}
#wath-top .acm .out{color:#8a2b2b}
#wath-top .acms{font-size:11.5px;color:#8a84a0;padding:6px 10px 2px}
:is(#wath,#wath-top) .upk.un{background:#33697f}
#wath-top .mref{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:4px 0 6px}
#wath-top .mrefu{flex:1;min-width:200px;font-family:ui-monospace,Menlo,monospace;font-size:15.5px;background:#f6f3fc;border:1px dashed #b9aee6;border-radius:10px;padding:11px 12px;overflow-wrap:anywhere}
#wath-top .mref .btn{margin-top:0}
#wath-top .mrefe{display:flex;align-items:center;border:1px solid #cfc8e6;border-radius:10px;background:#fff;overflow:hidden}
#wath-top .mrefe i{font-style:normal;flex:none;padding:0 0 0 12px;color:#5b6478;font-size:15px}
#wath-top .mrefe input{border:0;border-radius:0;padding-left:2px;min-width:0;flex:1}
#wath-top a.mchip{text-decoration:none;display:inline-block}
#wath-top .astat .mtag .asmp{display:inline-block;margin:0 0 0 4px;font-size:10.5px;color:#2c2208}
:is(#wath,#wath-top) .ft.hl .fa{top:88px;bottom:44%}
:is(#wath,#wath-top) .ft.hl .fa-cr{max-width:200px}
#wath-top .mtsep{flex:none;width:1px;background:rgba(255,255,255,.35);margin:8px 8px}
#wath-top .mt.ext{text-decoration:none;display:inline-flex;align-items:center;gap:5px;color:rgba(255,255,255,.82)}
#wath-top .mt.ext:after{content:"↗";font-size:12px;opacity:.8}
#wath-top .mt.ext:hover{color:#fff}
#wath-top .mbp{margin:12px 0}
#wath-top .mbp .mrow{font-size:15px;margin-bottom:6px}
#wath-top .mbp .mrow span{color:#5b6478;font-variant-numeric:tabular-nums}
#wath-top .msg{display:flex;gap:10px;align-items:center;padding:9px 0;border-top:1px solid #ebe7f5;flex-wrap:wrap}
#wath-top .msg>input{flex:1;min-width:200px;border:1px solid #cfc8e6;border-radius:8px;padding:8px 10px;font:inherit;font-size:15px}
#wath-top .msga{display:inline-flex;align-items:center;gap:4px;color:#5b6478}
#wath-top .msga input{width:110px;border:1px solid #cfc8e6;border-radius:8px;padding:8px 8px;font:inherit;font-size:15px}
#wath-top .msg .mlink{align-self:center}
#wath-top .acm a{display:block;text-decoration:none;font-size:15px;padding:9px 10px;border-radius:8px;color:#1b1526}
#wath-top .acm a:hover{background:#f1edf9;color:#6152a0}
#wath-top .acm a:after{content:" ↗";font-size:12px;color:#8a84a0}
#wath-top .mbp .bar{display:block;height:8px}
#wath-top .mextt{display:inline-flex;gap:14px;flex:none}
#wath-top .mxl{background:none;border:0;padding:0;font:inherit;font-size:13.5px;font-weight:700;color:#fff;text-decoration:underline;text-underline-offset:3px;cursor:pointer;white-space:nowrap}
#wath-top .mxl:hover{opacity:.8}
#wath-top .mtabs .mtsep,#wath-top .mtabs .mt.ext{display:none}
#wath-top .msamp{margin-left:auto}
@media(max-width:1000px){#wath-top .mextt{display:none}#wath-top .mtabs .mtsep{display:block}#wath-top .mtabs .mt.ext{display:inline-flex}}
@media(min-width:1001px){#wath-top .msamp{font-size:12px;padding:4px 10px}}
#header .wath-htitle{display:inline-flex!important;align-items:center;gap:12px;line-height:1}
#header .wath-hlogo{width:42px;height:42px;border-radius:50%;object-fit:cover;flex:none;border:2px solid rgba(255,255,255,.85);display:block}
@media(max-width:767px){#header .wath-hlogo{width:34px;height:34px}#header .wath-htitle{gap:9px}}
#wath-top .mlogo{display:inline-flex;align-items:center;gap:9px}
#wath-top .mlogo img{width:32px;height:32px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,.85)}
#wath-top .mlogo span{margin-left:0}
#wath-top .mimt b{display:block;font-size:34px;line-height:1.1;font-variant-numeric:tabular-nums}
#wath-top .mimt span{display:block;font-size:15px;color:#5b6478;margin-top:4px}
#wath-top .mimr{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:16px 0 12px}
#wath-top .mimr>div{position:relative;padding-left:16px}
#wath-top .mimr i{position:absolute;left:0;top:6px;width:9px;height:9px;border-radius:50%}
#wath-top .mimr b{display:block;font-size:21px;font-variant-numeric:tabular-nums}
#wath-top .mimr span{display:block;font-size:13.5px;color:#5b6478;line-height:1.4}
#wath-top .mimr em{font-style:normal}
#wath-top .mimb{display:flex;height:10px;overflow:hidden}
#wath-top .mimb i{display:block;height:100%;border-radius:0}
@media(max-width:700px){#wath-top .mimr{grid-template-columns:1fr}#wath-top .mlogo img{width:28px;height:28px}}
:is(#wath,#wath-top) .tndb .btn.tj,:is(#wath,#wath-top) .tndb .btn.tf{background:linear-gradient(90deg,#2f9bff 0%,#a46ef2 25%,#e5311f 50%,#a46ef2 75%,#2f9bff 100%);background-size:200% 100%;animation:wathTnd 7s linear infinite;border:0;border-radius:3px;color:#fff;text-transform:uppercase;letter-spacing:.04em;font-weight:600;font-size:15px;min-height:50px;padding:0 26px;box-shadow:0 5px 21px rgba(144,98,135,.44),0 0 0 1px rgba(164,110,242,.08);display:inline-flex;align-items:center;text-decoration:none;transition:transform .15s,box-shadow .15s}
:is(#wath,#wath-top) .tndb .btn.tf{animation-delay:-3.5s}
:is(#wath,#wath-top) .tndb .btn.tj:hover,:is(#wath,#wath-top) .tndb .btn.tf:hover{transform:translateY(-1px);box-shadow:0 8px 26px rgba(164,110,242,.55);color:#fff}
@keyframes wathTnd{from{background-position:0% 0}to{background-position:200% 0}}
@media(prefers-reduced-motion:reduce){:is(#wath,#wath-top) .tndb .btn.tj,:is(#wath,#wath-top) .tndb .btn.tf{animation:none}}
#header .wath-hlogo{margin:-9px 0}
#wath-top .mcard>.mtag+.msw{border-top:0}
#wath-top .msw.dis{opacity:.45;cursor:default}
#wath-top .mfr{display:flex;gap:14px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:12px 0;border-top:1px solid #ebe7f5}
#wath-top .mfr>span:first-child{font-size:14px;color:#5b6478;line-height:1.4;flex:1;min-width:200px}
#wath-top .mfr b{display:block;font-size:15.5px;color:#1b1526}
#wath-top .mfr select{border:1px solid #cfc8e6;border-radius:10px;padding:0 10px;font:inherit;font-size:15px;background:#fff;min-height:42px;color:#1b1526}
#wath-top .mfr .btn{margin-top:0}
#wath-top .mfrb{display:inline-flex;gap:8px;flex-wrap:wrap}
#wath-top .mgrp{display:flex;gap:14px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:12px 0;border-top:1px solid #ebe7f5}
#wath-top .mcard>.mtag+.mgrp{border-top:0;padding-top:4px}
#wath-top .mgrp>div{flex:1;min-width:220px}
#wath-top .mgrp b{display:block;font-size:15.5px}
#wath-top .mgrp>div span{font-size:14px;color:#5b6478;line-height:1.4}
#wath-top .mgrp .mlk{margin:0;flex:none;color:#6152a0;font-size:13.5px}
#wath-top .mgrp .mlk em{font-style:normal;font-weight:600;color:#5b6478;margin-left:6px}
#wath-top .mgrp .btn{margin-top:0}
#wath-top .mgrp.lk b{color:#5b6478}
#wath-top .mpv{background:#f6f3fc;border:1px solid #d9d3ec;border-radius:14px;padding:16px 18px 18px;margin:18px 0}
#wath-top .mpvh{display:flex;gap:12px;align-items:flex-start;color:#1b1526;padding-bottom:4px}
#wath-top .mpvh>svg{flex:none;width:34px;height:34px;padding:9px;border-radius:50%;background:#1b1526;color:#fff;box-sizing:border-box}
#wath-top .mpvh b{display:block;font-size:16.5px}
#wath-top .mpvh span{display:block;font-size:14px;color:#3a4051;line-height:1.5;margin-top:2px}
#wath-top .mcr .mcrn{display:inline-flex;gap:5px;align-items:center;font-size:13px;color:#6152a0;font-weight:700;margin-top:5px}
#wath-top .mcru{margin:8px 0 0;padding-left:18px;font-size:13.5px;color:#5b6478;line-height:1.5}
#wath-top .mcru li{margin:2px 0}
:is(#wath,#wath-top) .lall{font-weight:700;color:#6152a0}
:is(#wath,#wath-top) .hero h1,:is(#wath,#wath-top) .hero h1+p{text-align:center;margin-left:auto;margin-right:auto}
:is(#wath,#wath-top) #wath-levels{position:static!important}
:is(#wath,#wath-top) [data-levels]{background:none!important;border:0!important;padding:0!important;box-shadow:none!important}
:is(#wath,#wath-top) .lv,:is(#wath,#wath-top) .lv:first-child,:is(#wath,#wath-top) .div.blue+.lv{display:flex;align-items:flex-start;gap:12px;border:1px solid rgba(27,21,38,.08);border-left:6px solid var(--lc);background:var(--lb);border-radius:14px;padding:14px 16px 16px 14px;margin:9px 0}
:is(#wath,#wath-top) .lv .amt,:is(#wath,#wath-top) .lv.gold .amt{color:var(--lc)}
:is(#wath,#wath-top) .lv .t b{color:#1b1526}
:is(#wath,#wath-top) .lv ul{color:#2f3445}
:is(#wath,#wath-top) .lv .lall{display:inline-block;color:var(--lc);font-weight:700}
:is(#wath,#wath-top) .lv .gorb{background:#fff}
:is(#wath,#wath-top) .lim{display:inline-flex;align-items:center;gap:5px;background:#f1d28a;color:#2c2208;border-radius:999px;padding:2px 9px;font-size:11.5px;font-weight:800;letter-spacing:.03em;white-space:nowrap;vertical-align:1px;box-shadow:0 0 0 1px rgba(122,92,20,.35)}
:is(#wath,#wath-top) .lim.out{background:#1b1526;color:#fff;box-shadow:none}
:is(#wath,#wath-top) .flim{background:#f1d28a;color:#2c2208;box-shadow:0 0 0 1px rgba(122,92,20,.35)}
:is(#wath,#wath-top) .lv.k7{--lb:#241d38;--lc:#f1d28a;border-color:#241d38;border-left-color:#f1d28a}
:is(#wath,#wath-top) .lv.k7 .t b{color:#fff}
:is(#wath,#wath-top) .lv.k7 ul{color:#e6e2f2}
:is(#wath,#wath-top) .lv.k7 .gorb{background:#f1d28a;border-color:#f1d28a;color:#2c2208}
:is(#wath,#wath-top) .lv.k7 .gor .btn{background:#f1d28a;border-color:#f1d28a;color:#2c2208}
:is(#wath,#wath-top) #wath-levels .div{margin:14px 2px 2px}
:is(#wath,#wath-top) .lv.k0{--lb:#e8f3f6;--lc:#33697f}
:is(#wath,#wath-top) .lv.k1{--lb:#e6eef9;--lc:#3b6fb3}
:is(#wath,#wath-top) .lv.k2{--lb:#ece7f9;--lc:#6152a0}
:is(#wath,#wath-top) .lv.k3{--lb:#f3e6f6;--lc:#8a4fa3}
:is(#wath,#wath-top) .lv.k4{--lb:#fbe9ec;--lc:#b04a66}
:is(#wath,#wath-top) .lv.k5{--lb:#fdf1dc;--lc:#b07a1c}
:is(#wath,#wath-top) .lv.k6{--lb:#fbe7c2;--lc:#8f6312}
:is(#wath,#wath-top) .bovig{display:inline-flex;align-items:center;gap:6px;margin-top:8px;font-size:14px;font-weight:700;color:#6152a0;text-decoration:none;border:1px solid #d9d3ec;border-radius:999px;padding:5px 12px 5px 9px}
:is(#wath,#wath-top) .bovig:hover{background:#6152a0;border-color:#6152a0;color:#fff}
:is(#wath,#wath-top) .lv.k7 .lall{color:#f1d28a}
:is(#wath,#wath-top) #wath-updates .ups,:is(#wath,#wath-top) #wath-updates .up,:is(#wath,#wath-top) #wath-updates .upc{max-width:none;width:auto;margin-left:0;margin-right:0}
:is(#wath,#wath-top) #wath-updates .up{padding-left:0}
:is(#wath,#wath-top) #wath-updates .ups{padding-left:0!important}
:is(#wath,#wath-top) #wath-levels.vA [data-levels]{border:1px solid rgba(27,21,38,.16)!important;border-radius:0!important;overflow:hidden}
:is(#wath,#wath-top) #wath-levels.vA .lv{border-radius:0!important;margin:0!important;border:0!important;border-bottom:1px solid rgba(27,21,38,.13)!important;padding:16px 16px 18px!important}
:is(#wath,#wath-top) #wath-levels.vA .lv:last-child{border-bottom:0!important}
:is(#wath,#wath-top) #wath-levels.vA .lv .t b{color:#1b1526!important}
:is(#wath,#wath-top) #wath-levels.vA .lv ul{color:#2f3445!important}
:is(#wath,#wath-top) #wath-levels.vA .lv .gorb{background:#fff!important;border-color:#1b1526!important;color:#1b1526!important}
:is(#wath,#wath-top) #wath-levels.vA .lv .gor .btn.pri{background:#6152a0!important;border-color:#6152a0!important;color:#fff!important}
:is(#wath,#wath-top) #wath-levels.vA .lv .gor a.btn{background:#fff!important;border-color:#1b1526!important;color:#1b1526!important}
:is(#wath,#wath-top) #wath-levels.vA .div{margin:0!important;padding:9px 16px;color:#fff!important;font-size:11.5px;letter-spacing:.09em;gap:0;justify-content:flex-start;text-align:left}
:is(#wath,#wath-top) #wath-levels.vA .div:before,:is(#wath,#wath-top) #wath-levels.vA .div:after{display:none}
:is(#wath,#wath-top) #wath-levels.vA .div.blue{background:#1b1526}
:is(#wath,#wath-top) #wath-levels.vA .div:not(.blue){background:#1b1526}
:is(#wath,#wath-top) #wath-levels.vA .lv.k0,:is(#wath,#wath-top) #wath-levels.vA .lv.k1,:is(#wath,#wath-top) #wath-levels.vA .lv.k2,:is(#wath,#wath-top) #wath-levels.vA .lv.k3,:is(#wath,#wath-top) #wath-levels.vA .lv.k4,:is(#wath,#wath-top) #wath-levels.vA .lv.k5,:is(#wath,#wath-top) #wath-levels.vA .lv.k6,:is(#wath,#wath-top) #wath-levels.vA .lv.k7{background:#fff!important}
:is(#wath,#wath-top) #wath-levels.vA .lv.k0 .amt,:is(#wath,#wath-top) #wath-levels.vA .lv.k1 .amt,:is(#wath,#wath-top) #wath-levels.vA .lv.k2 .amt,:is(#wath,#wath-top) #wath-levels.vA .lv.k3 .amt,:is(#wath,#wath-top) #wath-levels.vA .lv.k4 .amt,:is(#wath,#wath-top) #wath-levels.vA .lv.k5 .amt,:is(#wath,#wath-top) #wath-levels.vA .lv.k6 .amt,:is(#wath,#wath-top) #wath-levels.vA .lv.k7 .amt,:is(#wath,#wath-top) #wath-levels.vA .lv.k0 .lall,:is(#wath,#wath-top) #wath-levels.vA .lv.k1 .lall,:is(#wath,#wath-top) #wath-levels.vA .lv.k2 .lall,:is(#wath,#wath-top) #wath-levels.vA .lv.k3 .lall,:is(#wath,#wath-top) #wath-levels.vA .lv.k4 .lall,:is(#wath,#wath-top) #wath-levels.vA .lv.k5 .lall,:is(#wath,#wath-top) #wath-levels.vA .lv.k6 .lall,:is(#wath,#wath-top) #wath-levels.vA .lv.k7 .lall{color:#6152a0!important}
:is(#wath,#wath-top) #wath-levels.vB [data-levels]{border:1px solid rgba(27,21,38,.16)!important;border-radius:0!important;overflow:hidden}
:is(#wath,#wath-top) #wath-levels.vB .lv{border-radius:0!important;margin:0!important;border:0!important;border-bottom:1px solid rgba(27,21,38,.13)!important;padding:16px 16px 18px!important}
:is(#wath,#wath-top) #wath-levels.vB .lv:last-child{border-bottom:0!important}
:is(#wath,#wath-top) #wath-levels.vB .lv .t b{color:#1b1526!important}
:is(#wath,#wath-top) #wath-levels.vB .lv ul{color:#2f3445!important}
:is(#wath,#wath-top) #wath-levels.vB .lv .gorb{background:#fff!important;border-color:#1b1526!important;color:#1b1526!important}
:is(#wath,#wath-top) #wath-levels.vB .lv .gor .btn.pri{background:#6152a0!important;border-color:#6152a0!important;color:#fff!important}
:is(#wath,#wath-top) #wath-levels.vB .lv .gor a.btn{background:#fff!important;border-color:#1b1526!important;color:#1b1526!important}
:is(#wath,#wath-top) #wath-levels.vB .div{margin:0!important;padding:9px 16px;color:#fff!important;font-size:11.5px;letter-spacing:.09em;gap:0;justify-content:flex-start;text-align:left}
:is(#wath,#wath-top) #wath-levels.vB .div:before,:is(#wath,#wath-top) #wath-levels.vB .div:after{display:none}
:is(#wath,#wath-top) #wath-levels.vB .div.blue{background:#6152a0}
:is(#wath,#wath-top) #wath-levels.vB .div:not(.blue){background:#6152a0}
:is(#wath,#wath-top) #wath-levels.vB .lv.k0,:is(#wath,#wath-top) #wath-levels.vB .lv.k1{background:#e8ecf8!important}
:is(#wath,#wath-top) #wath-levels.vB .lv.k0 .amt,:is(#wath,#wath-top) #wath-levels.vB .lv.k1 .amt,:is(#wath,#wath-top) #wath-levels.vB .lv.k0 .lall,:is(#wath,#wath-top) #wath-levels.vB .lv.k1 .lall{color:#6152a0!important}
:is(#wath,#wath-top) #wath-levels.vB .lv.k2,:is(#wath,#wath-top) #wath-levels.vB .lv.k3,:is(#wath,#wath-top) #wath-levels.vB .lv.k4,:is(#wath,#wath-top) #wath-levels.vB .lv.k5,:is(#wath,#wath-top) #wath-levels.vB .lv.k6,:is(#wath,#wath-top) #wath-levels.vB .lv.k7{background:#eee9f8!important}
:is(#wath,#wath-top) #wath-levels.vB .lv.k2 .amt,:is(#wath,#wath-top) #wath-levels.vB .lv.k3 .amt,:is(#wath,#wath-top) #wath-levels.vB .lv.k4 .amt,:is(#wath,#wath-top) #wath-levels.vB .lv.k5 .amt,:is(#wath,#wath-top) #wath-levels.vB .lv.k6 .amt,:is(#wath,#wath-top) #wath-levels.vB .lv.k7 .amt,:is(#wath,#wath-top) #wath-levels.vB .lv.k2 .lall,:is(#wath,#wath-top) #wath-levels.vB .lv.k3 .lall,:is(#wath,#wath-top) #wath-levels.vB .lv.k4 .lall,:is(#wath,#wath-top) #wath-levels.vB .lv.k5 .lall,:is(#wath,#wath-top) #wath-levels.vB .lv.k6 .lall,:is(#wath,#wath-top) #wath-levels.vB .lv.k7 .lall{color:#6152a0!important}
:is(#wath,#wath-top) #wath-levels.vB .lv.k0,:is(#wath,#wath-top) #wath-levels.vB .lv.k2,:is(#wath,#wath-top) #wath-levels.vB .lv.k4,:is(#wath,#wath-top) #wath-levels.vB .lv.k6{background:#f8f6fd!important}
:is(#wath,#wath-top) #wath-levels.vB .lv.k1,:is(#wath,#wath-top) #wath-levels.vB .lv.k3,:is(#wath,#wath-top) #wath-levels.vB .lv.k5,:is(#wath,#wath-top) #wath-levels.vB .lv.k7{background:#e9e3f6!important}
:is(#wath,#wath-top) #wath-levels.vC [data-levels]{border:1px solid rgba(27,21,38,.16)!important;border-radius:0!important;overflow:hidden}
:is(#wath,#wath-top) #wath-levels.vC .lv{border-radius:0!important;margin:0!important;border:0!important;border-bottom:1px solid rgba(27,21,38,.13)!important;padding:16px 16px 18px!important}
:is(#wath,#wath-top) #wath-levels.vC .lv:last-child{border-bottom:0!important}
:is(#wath,#wath-top) #wath-levels.vC .lv .t b{color:#1b1526!important}
:is(#wath,#wath-top) #wath-levels.vC .lv ul{color:#2f3445!important}
:is(#wath,#wath-top) #wath-levels.vC .lv .gorb{background:#fff!important;border-color:#1b1526!important;color:#1b1526!important}
:is(#wath,#wath-top) #wath-levels.vC .lv .gor .btn.pri{background:#6152a0!important;border-color:#6152a0!important;color:#fff!important}
:is(#wath,#wath-top) #wath-levels.vC .lv .gor a.btn{background:#fff!important;border-color:#1b1526!important;color:#1b1526!important}
:is(#wath,#wath-top) #wath-levels.vC .div{margin:0!important;padding:9px 16px;color:#fff!important;font-size:11.5px;letter-spacing:.09em;gap:0;justify-content:flex-start;text-align:left}
:is(#wath,#wath-top) #wath-levels.vC .div:before,:is(#wath,#wath-top) #wath-levels.vC .div:after{display:none}
:is(#wath,#wath-top) #wath-levels.vC .div.blue{background:#33697f}
:is(#wath,#wath-top) #wath-levels.vC .div:not(.blue){background:#8f6312}
:is(#wath,#wath-top) #wath-levels.vC .lv.k0,:is(#wath,#wath-top) #wath-levels.vC .lv.k1{background:#fff!important}
:is(#wath,#wath-top) #wath-levels.vC .lv.k0 .amt,:is(#wath,#wath-top) #wath-levels.vC .lv.k1 .amt,:is(#wath,#wath-top) #wath-levels.vC .lv.k0 .lall,:is(#wath,#wath-top) #wath-levels.vC .lv.k1 .lall{color:#33697f!important}
:is(#wath,#wath-top) #wath-levels.vC .lv.k2,:is(#wath,#wath-top) #wath-levels.vC .lv.k3,:is(#wath,#wath-top) #wath-levels.vC .lv.k4,:is(#wath,#wath-top) #wath-levels.vC .lv.k5,:is(#wath,#wath-top) #wath-levels.vC .lv.k6,:is(#wath,#wath-top) #wath-levels.vC .lv.k7{background:#fff!important}
:is(#wath,#wath-top) #wath-levels.vC .lv.k2 .amt,:is(#wath,#wath-top) #wath-levels.vC .lv.k3 .amt,:is(#wath,#wath-top) #wath-levels.vC .lv.k4 .amt,:is(#wath,#wath-top) #wath-levels.vC .lv.k5 .amt,:is(#wath,#wath-top) #wath-levels.vC .lv.k6 .amt,:is(#wath,#wath-top) #wath-levels.vC .lv.k7 .amt,:is(#wath,#wath-top) #wath-levels.vC .lv.k2 .lall,:is(#wath,#wath-top) #wath-levels.vC .lv.k3 .lall,:is(#wath,#wath-top) #wath-levels.vC .lv.k4 .lall,:is(#wath,#wath-top) #wath-levels.vC .lv.k5 .lall,:is(#wath,#wath-top) #wath-levels.vC .lv.k6 .lall,:is(#wath,#wath-top) #wath-levels.vC .lv.k7 .lall{color:#8f6312!important}
:is(#wath,#wath-top) #wath-levels.vC .lv.k0,:is(#wath,#wath-top) #wath-levels.vC .lv.k1{border-left:6px solid #33697f!important}
:is(#wath,#wath-top) #wath-levels.vC .lv.k2,:is(#wath,#wath-top) #wath-levels.vC .lv.k3,:is(#wath,#wath-top) #wath-levels.vC .lv.k4,:is(#wath,#wath-top) #wath-levels.vC .lv.k5,:is(#wath,#wath-top) #wath-levels.vC .lv.k6,:is(#wath,#wath-top) #wath-levels.vC .lv.k7{border-left:6px solid #8f6312!important}
:is(#wath,#wath-top) .lim{background:#fff;color:#1b1526;box-shadow:0 0 0 1px rgba(27,21,38,.55);font-weight:700}
:is(#wath,#wath-top) .lim.out{background:#1b1526;color:#fff}
:is(#wath,#wath-top) .car{gap:18px;align-items:stretch}
:is(#wath,#wath-top) .pc{flex:0 0 min(300px,78vw);scroll-snap-align:start;background:#fff;border:1px solid #d9d3ec;border-radius:10px;overflow:hidden;display:flex;flex-direction:column;color:#1b1526}
:is(#wath,#wath-top) .pci{aspect-ratio:16/10;background:#e3ddf2 center/cover no-repeat;position:relative;display:flex;align-items:center;justify-content:center;overflow:hidden}
:is(#wath,#wath-top) .pci.offer{color:#6152a0;background:#f3f0fa;border-bottom:1px dashed #b9aee6}
:is(#wath,#wath-top) .pci .fa{position:static;padding:0 22px;width:100%;inset:auto}
:is(#wath,#wath-top) .pci .fa svg{height:104px}
:is(#wath,#wath-top) .pcb{padding:16px 18px 18px;display:flex;flex-direction:column;gap:6px;flex:1}
:is(#wath,#wath-top) .pcl{font-size:11.5px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#5b6478}
:is(#wath,#wath-top) .pcb b{font-size:19.5px;line-height:1.2;color:#1b1526}
:is(#wath,#wath-top) .pcb b .soon{vertical-align:2px}
:is(#wath,#wath-top) .pcb p{margin:0;font-size:14.5px;line-height:1.45;color:#5b6478}
:is(#wath,#wath-top) .pclim{display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:700;color:#1b1526;margin-top:4px}
:is(#wath,#wath-top) .pclim:before{content:"";width:7px;height:7px;border-radius:50%;background:#6152a0;flex:none}
:is(#wath,#wath-top) .pclim.out:before{background:#8a84a0}
:is(#wath,#wath-top) .pcf{margin-top:auto;padding-top:12px}
:is(#wath,#wath-top) .pcf>.btn{width:100%;min-height:42px;font-size:14.5px;background:#fff}
:is(#wath,#wath-top) .pcf .gor{display:flex;gap:8px}
:is(#wath,#wath-top) .pcf .gor .btn{flex:1;justify-content:center;min-height:42px;font-size:14.5px;display:inline-flex;align-items:center;text-decoration:none}
:is(#wath,#wath-top) .pc.out .pci{filter:grayscale(.7) opacity(.8)}
@media(min-width:901px) and (max-width:1099px){:is(#wath,#wath-top) .hero-grid{grid-template-columns:minmax(0,1.55fr) minmax(300px,1fr)}}
@media(min-width:901px){:is(#wath,#wath-top) .hero-grid{grid-template-rows:1fr auto!important}
:is(#wath,#wath-top) .hero-grid>.video{aspect-ratio:auto!important;align-self:stretch!important;height:auto;min-height:320px}}
:is(#wath,#wath-top) .lim,:is(#wath,#wath-top) .lim.out{display:block;background:none!important;box-shadow:none!important;border-radius:0;padding:0;margin-top:1px;font-size:12.5px;font-weight:600;letter-spacing:0;color:#6152a0!important;white-space:normal;vertical-align:baseline}
:is(#wath,#wath-top) .lim.out{color:#5b6478!important}
:is(#wath,#wath-top) .lim svg{display:none}
:is(#wath,#wath-top) .pclim{font-weight:600;color:#6152a0}
:is(#wath,#wath-top) .pclim:before{display:none}
:is(#wath,#wath-top) .pclim.out{color:#5b6478}
:is(#wath,#wath-top) .pci.art:not(.offer){background:#14101f}
:is(#wath,#wath-top) .pci .fa{position:absolute!important;inset:0!important;padding:0!important;width:auto;display:flex;align-items:center;justify-content:center}
:is(#wath,#wath-top) .pci .fa svg{height:66%;filter:none}
:is(#wath,#wath-top) .pci .fa-cr{max-width:none;width:100%;height:100%;aspect-ratio:auto;border-radius:0;box-shadow:none;background:#0b0910;gap:8px}
:is(#wath,#wath-top) .pci .fa-cr small{font-size:10.5px}
:is(#wath,#wath-top) .pci .fa-cr b{font-size:24px!important;color:#fff}
:is(#wath,#wath-top) .pci .fa-cr i{height:6px}
:is(#wath,#wath-top) .pci .fa-win,:is(#wath,#wath-top) .pci .fa-win.g2{max-width:none;width:100%;height:100%;border-radius:0;box-shadow:none;padding:10px;gap:8px;box-sizing:border-box}
:is(#wath,#wath-top) .pci .fa-win .fa-t,:is(#wath,#wath-top) .pci .fa-win.g2 .fa-t{aspect-ratio:auto;height:100%;min-height:0}
:is(#wath,#wath-top) .pci .fa-win.g2{grid-template-rows:1fr 1fr}
:is(#wath,#wath-top) .pci .fa-col{gap:8px;grid-template-rows:1fr 1fr;min-height:0}
:is(#wath,#wath-top) .pci .fa-t.you{outline:2px solid #b9aee6;outline-offset:-2px;color:#d9d3ec}
:is(#wath,#wath-top) .pci .fa-fs{width:100%;height:100%;box-sizing:border-box;border-radius:0;box-shadow:none;padding:22px 10px;gap:8px;align-items:stretch}
:is(#wath,#wath-top) .pci .fa-fs span{width:auto;flex:1;aspect-ratio:auto}
:is(#wath,#wath-top) .pci .fa-dw{grid-template-columns:repeat(4,52px);gap:12px}
:is(#wath,#wath-top) .pci .fa-dw .av,:is(#wath,#wath-top) .pci .fa-dw .you{width:52px;height:52px}
:is(#wath,#wath-top) .pci .fa-dw .you{border-color:#b9aee6;color:#d9d3ec}
:is(#wath,#wath-top) #wath-levels .lv .t b{font-size:15px!important;letter-spacing:.07em!important;line-height:1.25;display:block;margin-bottom:3px}
:is(#wath,#wath-top) #wath-levels.vB .lv{display:block!important;padding:0!important;background:#f8f6fd!important;border-bottom:0!important}
:is(#wath,#wath-top) #wath-levels.vB .lv .lh{display:flex;align-items:baseline;gap:10px;background:#1b1526;padding:9px 16px}
:is(#wath,#wath-top) #wath-levels.vB .lv .lh .amt{flex:none!important;padding:0!important;font-size:15px!important;font-weight:800;color:#fff!important;letter-spacing:.04em}
:is(#wath,#wath-top) #wath-levels.vB .lv .lh b{font-size:15px!important;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:#cfc6f0!important;line-height:1.25;margin:0!important}
:is(#wath,#wath-top) #wath-levels.vB .lv .t{display:block;padding:12px 16px 16px}
:is(#wath,#wath-top) #wath-levels.vB .lv ul{list-style:none!important;padding:0!important;margin:0!important}
:is(#wath,#wath-top) #wath-levels.vB .lv li{position:relative;padding-left:14px;margin:3px 0}
:is(#wath,#wath-top) #wath-levels.vB .lv li:before{content:"";position:absolute;left:1px;top:.62em;width:5px;height:5px;border-radius:50%;background:#8a84a0}
:is(#wath,#wath-top) #wath-levels.vB .lv li.hl{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
:is(#wath,#wath-top) #wath-levels.vB .lv li.hl .lim{flex:none;display:inline!important;margin:0;font-size:12.5px;white-space:nowrap;text-align:right}
:is(#wath,#wath-top) #wath-levels.vB .lv li.hl>span:first-child{color:inherit!important;font-size:inherit!important}
:is(#wath,#wath-top) #wath-levels.vB .lv .gorb{width:100%;margin-top:12px;min-height:42px}
:is(#wath,#wath-top) #wath-levels.vB .lv .gor{display:flex;gap:8px;margin-top:12px}
:is(#wath,#wath-top) #wath-levels.vB .lv .gor .btn{flex:1;justify-content:center;min-height:42px}
:is(#wath,#wath-top) #wath-levels.vB .lv.k0,:is(#wath,#wath-top) #wath-levels.vB .lv.k1,:is(#wath,#wath-top) #wath-levels.vB .lv.k2,:is(#wath,#wath-top) #wath-levels.vB .lv.k3,:is(#wath,#wath-top) #wath-levels.vB .lv.k4,:is(#wath,#wath-top) #wath-levels.vB .lv.k5,:is(#wath,#wath-top) #wath-levels.vB .lv.k6,:is(#wath,#wath-top) #wath-levels.vB .lv.k7{background:#f8f6fd!important}
:is(#wath,#wath-top) #wath-levels.vB .lv .lh{background:#e2dbf3}
:is(#wath,#wath-top) #wath-levels.vB .lv .lh .amt{color:#6152a0!important}
:is(#wath,#wath-top) #wath-levels.vB .lv .lh b{color:#1b1526!important}
#wath-top .minner{max-width:1100px}
#wath-top .mtop .minner:first-child{padding-top:10px;padding-bottom:10px;gap:16px}
#wath-top button.mlogo{background:none;border:0;color:#fff;font:inherit;font-size:20px;font-weight:900;letter-spacing:.02em;cursor:pointer;padding:0;flex:none}
#wath-top .mlogo img{width:36px;height:36px}
#wath-top .mnav{display:flex;gap:22px;margin-left:auto;flex:none}
#wath-top .mnav a{color:#fff;text-decoration:none;font-size:15px;font-weight:500;white-space:nowrap}
#wath-top .mnav a:hover{text-decoration:underline;text-underline-offset:4px}
#wath-top .msamp{margin-left:6px!important;background:rgba(255,255,255,.2);color:#fff;font-weight:700}
#wath-top .mme{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:700;white-space:nowrap;flex:none}
#wath-top .mme .mav{width:30px;height:30px;font-size:11.5px;box-shadow:0 0 0 2px rgba(255,255,255,.85)}
#wath-top .msub2{background:#f8f6fd;border-bottom:1px solid #d9d3ec;flex:none}
#wath-top .msub2 .mtabs{align-items:center;gap:4px;padding-top:8px;padding-bottom:8px}
#wath-top .msub2 .mlab{flex:none;font-size:11.5px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#6152a0;margin-right:10px;white-space:nowrap}
#wath-top .msub2 .mt{color:#1b1526;border:0;border-radius:999px;padding:7px 13px;font-size:14px}
#wath-top .msub2 .mt:hover{background:#ece7f7}
#wath-top .msub2 .mt.on{background:#6152a0;color:#fff}
#wath-top .msub2 .mt.ext{color:#5b6478}
#wath-top .msub2 .mtsep{background:#d9d3ec}
@media(max-width:1000px){#wath-top .mnav,#wath-top .mme>span{display:none}
#wath-top .msamp{margin-left:auto!important}}
@media(max-width:700px){#wath-top .msub2 .mlab{display:none}
#wath-top button.mlogo{font-size:15px}
#wath-top .mlogo img{width:28px;height:28px}
#wath-top .msamp:after{content:none}
#wath-top .msamp{font-size:11.5px!important}}
#wath-top .mmw{position:relative;flex:none;display:inline-flex}
#wath-top button.mme{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.35);border-radius:999px;color:#fff;font:inherit;font-size:14px;font-weight:700;padding:4px 12px 4px 5px;cursor:pointer}
#wath-top button.mme:hover{background:rgba(255,255,255,.26)}
#wath-top .mmenu{display:none;position:absolute;right:0;top:calc(100% + 8px);z-index:5;width:232px;background:#fff;border:1px solid #d9d3ec;border-radius:14px;box-shadow:0 18px 50px rgba(27,21,38,.25);padding:8px;flex-direction:column}
#wath-top .mmw.open .mmenu{display:flex}
#wath-top .mmenu button{background:none;border:0;border-radius:8px;text-align:left;font:inherit;font-size:15px;font-weight:500;padding:9px 10px;color:#1b1526;cursor:pointer;white-space:nowrap}
#wath-top .mmenu button:hover{background:#f1edf9;color:#6152a0}
#wath-top .mmenu button.on{font-weight:800;color:#6152a0}
#wath-top .mmenu .adm{border-top:1px solid #ebe7f5;border-radius:0 0 8px 8px;margin-top:6px;padding-top:12px}
#wath-top .mmenu .out{color:#8a2b2b}
#wath-top .mtop{position:relative;z-index:3}
#wath-top .msec+.msec{margin-top:34px;padding-top:26px;border-top:1px solid #d9d3ec}
#wath-top .mh3{font-size:19px;margin:22px 0 12px;color:#1b1526}
#wath-top .mgoal{display:flex;flex-direction:column;gap:2px}
#wath-top .mgoal .mgt{font-size:17px;line-height:1.25}
#wath-top .mgoal .btn{margin-top:12px;align-self:flex-start;min-height:40px;padding:0 16px;font-size:14px;display:inline-flex;align-items:center;text-decoration:none}
@media(max-width:800px){#wath-top .mgoals{grid-template-columns:1fr}}
@media(max-width:1000px){#wath-top button.mme{padding:4px 9px 4px 5px}}
#wath-top button.msamp{border:1px dashed rgba(255,255,255,.6);font:inherit;font-size:12px;font-weight:700;cursor:pointer;white-space:nowrap}
#wath-top button.msamp:hover{background:rgba(255,255,255,.32)}
#wath-top .msec{display:flex;flex-direction:column;gap:16px}
#wath-top .msec>h2,#wath-top .msec>h3,#wath-top .msec>p{margin-top:0;margin-bottom:0}
#wath-top .msec>.mh3{margin-top:10px}
@media(max-width:1000px){#wath-top .mme>span.mav{display:flex}}
@media(max-width:700px){#wath-top .mmain{padding-top:18px}}
#wath-top .mside{display:grid;grid-template-columns:220px minmax(0,1fr);gap:28px;align-items:start}
#wath-top .msnav{display:flex;flex-direction:column;gap:2px;position:sticky;top:8px;background:#fff;border:1px solid #d9d3ec;border-radius:14px;padding:8px}
#wath-top .msn{background:none;border:0;border-radius:8px;text-align:left;font:inherit;font-size:15px;font-weight:500;padding:9px 11px;color:#1b1526;cursor:pointer}
#wath-top .msn:hover{background:#f1edf9;color:#6152a0}
#wath-top .msn.on{background:#ece7f7;color:#6152a0;font-weight:800}
#wath-top .msn.out{color:#8a2b2b;border-top:1px solid #ebe7f5;border-radius:0 0 8px 8px;margin-top:6px;padding-top:12px}
#wath-top .msmain .msec>h2{font-size:19px}
@media(max-width:800px){#wath-top .mside{grid-template-columns:1fr;gap:14px}
#wath-top .msnav{flex-direction:row;position:static;overflow-x:auto;scrollbar-width:none;padding:6px}
#wath-top .msn{flex:none;white-space:nowrap}
#wath-top .msn.out{border-top:0;margin-top:0;padding-top:9px;border-radius:8px}}
@media(max-width:700px){#wath-top button.msamp{font-size:0!important;padding:4px 9px}
#wath-top button.msamp:after{content:"Sample"!important;font-size:11.5px}}
#wath-top .mnm{display:grid;grid-template-columns:1fr 1fr;gap:0 14px}
#wath-top .mcr .mck{margin:12px 0 0}
#wath-top .mcr input:disabled{background:#f1edf9;color:#8a84a0}
@media(max-width:560px){#wath-top .mnm{grid-template-columns:1fr}}
#wath-top .mov select[data-arole]{border:1px solid #cfc8e6;border-radius:10px;padding:0 10px;font:inherit;font-size:15px;background:#fff;min-height:42px;color:#1b1526;flex:none;max-width:100%}
#wath-top .amng{border-color:#6152a0;box-shadow:0 0 0 3px rgba(97,82,160,.12)}
#wath-top .amg{display:grid;grid-template-columns:minmax(0,280px) 1fr;gap:18px;align-items:start;margin-top:6px}
#wath-top .amb{display:flex;flex-wrap:wrap;gap:8px;padding-top:28px}
#wath-top .amb .btn{min-height:42px;padding:0 14px;font-size:14px}
#wath-top .asup tr.sel td{background:#f1edf9}
#wath-top .asup td:last-child{text-align:right}
@media(max-width:700px){#wath-top .amg{grid-template-columns:1fr;gap:4px}
#wath-top .amb{padding-top:6px}}
@media(max-width:700px){#wath-top .asup th:nth-child(2),#wath-top .asup td:nth-child(2){display:none}
#wath-top .asup td,#wath-top .asup th{padding-left:4px;padding-right:4px;font-size:14px}}
#wath-top .asup td .apill{display:inline-block!important;width:auto}
#wath-top .mlogin{max-width:440px;margin:26px auto 0;padding:28px 28px 24px}
#wath-top .mlogin h2{font-size:23px;margin:0 0 6px}
#wath-top .mlb{width:100%;min-height:46px;display:flex;align-items:center;justify-content:center;gap:10px;margin-top:12px;font-size:15px}
#wath-top .mlb:not(.pri){background:#fff}
#wath-top .mlor{display:flex;align-items:center;gap:12px;margin:18px 0 12px;color:#5b6478;font-size:13px}
#wath-top .mlor:before,#wath-top .mlor:after{content:"";flex:1;height:1px;background:#d9d3ec}
#wath-top .mlogin .msub{margin-top:12px}
:is(#wath,#wath-top) #wath-levels.vB [data-levels]{border:0!important;overflow:visible!important;background:none!important}
:is(#wath,#wath-top) #wath-levels.vB .lv{border:1px solid #cfc7e6!important;margin:0 0 16px!important}
:is(#wath,#wath-top) #wath-levels.vB .lv:last-child{border-bottom:1px solid #cfc7e6!important;margin-bottom:0!important}
:is(#wath,#wath-top) #wath-levels.vB .lv .lh{padding:13px 18px}
:is(#wath,#wath-top) #wath-levels.vB .lv .t{padding:18px 18px 20px}
:is(#wath,#wath-top) #wath-levels.vB .lv li{margin:5px 0}
:is(#wath,#wath-top) #wath-levels.vB .lv .gorb,:is(#wath,#wath-top) #wath-levels.vB .lv .gor{margin-top:20px}
:is(#wath,#wath-top) #wath-levels.vB .div{margin:6px 0 16px!important}
:is(#wath,#wath-top) #wath-levels.vB [data-levels]+*{margin-top:16px}
:is(#wath,#wath-top) #wath-levels .lv .gor .btn{flex:1 1 0;min-width:0;justify-content:center;min-height:42px;padding:0 8px;white-space:nowrap}
:is(#wath,#wath-top) .pcr{display:block;text-align:center;margin-top:9px;font-size:13.5px;font-weight:600;color:#6152a0;text-decoration:underline;text-underline-offset:2px}
:is(#wath,#wath-top) .pcr:hover{color:#1b1526}
:is(#wath,#wath-top) .pkd .pkdi{height:190px;border-radius:12px;background:#d9d3ec center/cover no-repeat;margin:0 44px 16px 0}
:is(#wath,#wath-top) .pkd .pkdl{display:block;font-size:13px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#6152a0;padding-right:40px}
:is(#wath,#wath-top) .pkd .pkdt{display:block;font-size:24px;line-height:1.2;margin:4px 0 8px;padding-right:40px}
:is(#wath,#wath-top) .pkd .pkdm{font-size:14.5px;font-weight:700;color:#6152a0;margin-top:8px}
:is(#wath,#wath-top) .pkd .pkdh{display:block;font-size:14px;font-weight:800;margin:18px 0 6px;color:#1b1526}
:is(#wath,#wath-top) .pkd .pkdu{margin:0;padding-left:20px;font-size:15.5px;line-height:1.55;color:#3a4051}
:is(#wath,#wath-top) .pkd .pkdn{font-size:14px;color:#5b6478;margin-top:14px}
:is(#wath,#wath-top) .pkd .pkdb{margin-top:16px}
:is(#wath,#wath-top) .pkd .pkdb .btn{width:100%;min-height:46px}
:is(#wath,#wath-top) .pkd .pkdq{font-size:13px;font-weight:700;color:#6152a0;white-space:nowrap;margin-left:6px}
:is(#wath,#wath-top) .pkd .pkdw{font-size:14px;color:#1b1526;margin:10px 0 2px}
:is(#wath,#wath-top) #wath-levels .lv .pcr{margin-top:10px}
:is(#wath,#wath-top) #wath-levels.vB .lv .gor button.btn:not(.pri){background:#fff!important;border-color:#1b1526!important;color:#1b1526!important}
:is(#wath,#wath-top) .pkd .pkcta{display:flex;align-items:center;justify-content:center;width:100%;min-height:46px;text-decoration:none}
:is(#wath,#wath-top) .pkd .bovh b em{font-style:italic}
/* breathing room: more space between sections, with a hairline between them */
#wath .stack{gap:40px}
#wath .stack>.sec+.sec{border-top:1px solid #d5cfe9;padding-top:44px}
#wath .cols{padding-top:56px;padding-bottom:84px}
#wath .cols.second{padding-top:60px}
#wath .band{padding:58px 0 62px}
#wath .sec{gap:16px}
@media(max-width:700px){#wath .stack{gap:30px}#wath .stack>.sec+.sec{padding-top:32px}#wath .cols{padding-top:34px;padding-bottom:52px}#wath .cols.second{padding-top:40px}#wath .band{padding:40px 0 44px}}
#wath-top .mbdg{display:inline-flex;align-items:center;justify-content:center;min-width:20px;height:20px;padding:0 6px;margin-left:6px;border-radius:999px;background:#6152a0;color:#fff;font-size:11.5px;font-weight:800;line-height:1;vertical-align:1px}
.acm .mbdg{display:inline-flex;align-items:center;justify-content:center;min-width:20px;height:20px;padding:0 6px;margin-left:6px;border-radius:999px;background:#6152a0;color:#fff;font-size:11.5px;font-weight:800;line-height:1}
#wath-top .msn .mbug{color:#9488cf;vertical-align:-3px;margin-right:7px;flex:none}
#wath-top .msn.on .mbug{color:#6152a0}
#wath-top .msmain2{min-width:0}
#wath-top select[data-lrole],#wath-top select[data-rstatus],#wath-top select[data-blv]{font:inherit;font-size:15px;padding:8px 10px;border:1px solid #cfc7e8;border-radius:10px;background:#fff;color:#1b1526;flex:none;max-width:100%}
#wath-top .mslab{display:block;font-size:11px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#6152a0;padding:8px 11px 4px}
#wath-top .mslab.tm{border-top:1px solid #ebe7f5;margin-top:6px;padding-top:14px}
#wath-top .msn.msw{display:none}
@media(max-width:1000px){#wath-top .mme>span.marr{display:inline-flex}}
#wath-top .marr{display:inline-flex;align-items:center;align-self:stretch;padding:0 2px 0 6px;margin:-4px 0 -4px 0}
@media(max-width:800px){#wath-top .mslab{display:none}#wath-top .msn.msw{display:block;border:1px solid #cfc7e8;color:#6152a0;font-weight:700;border-radius:999px;margin-right:4px}#wath-top .msnav[data-grp=me] .g-team,#wath-top .msnav[data-grp=team] .g-me{display:none}}
#wath-top .msn.par{font-weight:800;color:#6152a0}
#wath-top .msn.sub{padding-left:24px;font-size:14px}
@media(max-width:800px){#wath-top .msn.sub{padding-left:11px}}
#wath-top .mbtns{display:flex;gap:8px;flex-wrap:wrap}
#wath-top .mfr{display:inline-block;margin-left:8px;font-size:13.5px;font-weight:600;color:#6152a0}
#wath-top .mdelp h3{margin:6px 0 2px}
#wath-top .mdelp .mdele{margin:0 0 12px;color:#5b6478;word-break:break-all}
#wath-top .mdelp p{margin:12px 0 4px}
#wath-top .mdelp ul{margin:0 0 4px;padding-left:20px}
#wath-top .mdelp li{margin:3px 0;color:#3a3350}
#wath-top .mdelp .mdelw{font-weight:700;color:#1b1526}
#wath-top .mdelp .mf input{max-width:220px;letter-spacing:.08em}
#wath-top .mdelb{display:flex;gap:10px;align-items:center;margin-top:16px;flex-wrap:wrap;justify-content:space-between}
#wath-top .mdelp .mdelgo{background:#4a3f7a;border-color:#4a3f7a;color:#fff}
#wath-top .mdelp .mdelgo[disabled]{background:#e4dff0;border-color:#e4dff0;color:#8d86a3;cursor:not-allowed}
:is(#wath,#wath-top) .video .vt .play{position:static;transform:none;margin-top:1.6cqw;display:inline-flex;align-items:center;text-shadow:none}
:is(#wath,#wath-top) .video:hover .vt .play{transform:scale(1.04)}
:is(#wath,#wath-top) .video>.vb{position:absolute;left:0;right:0;bottom:5%;margin:0;text-align:center;z-index:2;text-shadow:0 2px 14px rgba(27,21,38,.6),0 0 2px rgba(27,21,38,.35)}
:is(#wath,#wath-top) .upx{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;font-size:14.5px;color:#3a3350;background:#f6f3fc;border:1px solid #d9d3ec;border-radius:12px;padding:10px 14px}
:is(#wath,#wath-top) .upx b{color:#6152a0}
:is(#wath,#wath-top) .ups{position:relative;margin:6px 0 0;padding-left:34px}
:is(#wath,#wath-top) .ups:before{content:"";position:absolute;left:9px;top:10px;bottom:10px;width:2px;background:#cfc8e6}
:is(#wath,#wath-top) .up{position:relative;display:block;padding:0 0 30px;color:inherit;text-decoration:none}
:is(#wath,#wath-top) .up:last-child{padding-bottom:4px}
:is(#wath,#wath-top) .up:before{content:"";position:absolute;left:-31px;top:5px;width:14px;height:14px;border-radius:50%;background:#6152a0;border:3px solid #ece7f7;box-shadow:0 0 0 2px #6152a0}
:is(#wath,#wath-top) .up.locked:before{background:#ece7f7}
:is(#wath,#wath-top) .upm{display:flex;gap:8px 12px;flex-wrap:wrap;align-items:center;font-size:12.5px;font-weight:800;letter-spacing:.1em;color:#5b6478;text-transform:uppercase;margin-bottom:6px}
:is(#wath,#wath-top) .upm .upd{font-weight:600;letter-spacing:0;text-transform:none;font-size:14px}
:is(#wath,#wath-top) .upc{background:#f6f3fc;border:1px solid #d9d3ec;border-radius:16px;padding:20px 22px}
:is(#wath,#wath-top) .upc h3{font-size:24px;line-height:1.2;margin:0 0 10px}
:is(#wath,#wath-top) .upa{display:flex;align-items:center;gap:10px;font-size:14px;color:#5b6478;margin-bottom:12px}
:is(#wath,#wath-top) .upa b{color:#1b1526;font-size:15px}
:is(#wath,#wath-top) .upt p{color:#3a4051;font-size:16.5px;line-height:1.6;margin:0 0 12px}
:is(#wath,#wath-top) .upt.clampd{display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
:is(#wath,#wath-top) .upt.clampd p{display:inline}
:is(#wath,#wath-top) .upl{font-weight:700;color:#6152a0;font-size:15px;background:none;border:0;padding:0;margin-top:8px;display:inline-block;cursor:pointer;text-decoration:none}
:is(#wath,#wath-top) .upk{display:inline-flex;align-items:center;gap:5px;background:#1b1526;color:#fff;border-radius:999px;padding:2px 9px;font-size:11.5px;font-weight:800;letter-spacing:.04em;text-transform:none}
:is(#wath,#wath-top) .ups2{display:inline-flex;background:#f1d28a;color:#2c2208;border-radius:999px;padding:2px 9px;font-size:11.5px;font-weight:800;letter-spacing:.04em;text-transform:none}
@media(max-width:600px){:is(#wath,#wath-top) .ups{padding-left:26px}:is(#wath,#wath-top) .ups:before{left:6px}:is(#wath,#wath-top) .up:before{left:-26px}:is(#wath,#wath-top) .upc{padding:16px}:is(#wath,#wath-top) .upc h3{font-size:21px}}

/* ---- Nov 15: phone layout borrowing from Kickstarter (video first, three stats, reward cards, a Donate bar that stays on screen) ---- */
:is(#wath,#wath-top) .kstats{display:none}
:is(#wath,#wath-top) .mcta{display:none}
@media(max-width:700px){
:is(#wath,#wath-top) .wrap{padding-left:18px;padding-right:18px}
:is(#wath,#wath-top) .hero{padding:0 0 22px}
:is(#wath,#wath-top) .hero>.wrap{display:flex;flex-direction:column}
:is(#wath,#wath-top) .hero-grid{display:contents}
:is(#wath,#wath-top) .video{order:-1;margin:0 -18px 16px;border-radius:0;width:auto;align-self:stretch}
:is(#wath,#wath-top) .hero h1{font-size:26px;line-height:1.12}
:is(#wath,#wath-top) .hero>.wrap>.sub{font-size:15.5px!important;margin-bottom:14px}
:is(#wath,#wath-top) .kstats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;border-top:1px solid rgba(27,21,38,.14);border-bottom:1px solid rgba(27,21,38,.14);padding:12px 0}
:is(#wath,#wath-top) .kstats b{display:block;font-size:20px;line-height:1.1;color:#1b1526}
:is(#wath,#wath-top) .kstats span{font-size:12.5px;color:#5b6478}
:is(#wath,#wath-top) .subnav .btn{display:none}
:is(#wath,#wath-top) .subnav .wrap{padding-right:0}
:is(#wath,#wath-top) .subnav .snl{gap:20px;padding-right:18px}
:is(#wath,#wath-top) .cols{padding:28px 18px 40px;gap:32px}
:is(#wath,#wath-top) .stack{gap:34px}
:is(#wath,#wath-top) aside>.card{padding:0;background:transparent;border:0}
:is(#wath,#wath-top) .lv{display:block;background:#f6f3fc;border:1px solid #d9d3ec;border-radius:14px;padding:16px;margin:10px 0}
:is(#wath,#wath-top) .lv .amt{display:block;font-size:26px;margin-bottom:2px}
:is(#wath,#wath-top) .lv .t b{font-size:13px}
:is(#wath,#wath-top) .lv ul{font-size:15.5px}
:is(#wath,#wath-top) .lv .gorb,:is(#wath,#wath-top) .lv .gor .btn{min-height:46px;font-size:16px}
:is(#wath,#wath-top) .lv .gorb{width:100%;background:#6152a0;border-color:#6152a0;color:#fff}
:is(#wath,#wath-top) .lv .gor .btn{flex:1;justify-content:center}
:is(#wath,#wath-top) .div{margin:18px 0 4px}
:is(#wath,#wath-top) .car{padding-left:18px;padding-right:18px}
:is(#wath,#wath-top) .car .ft{scroll-margin-left:18px}
:is(#wath,#wath-top) .band{padding:28px 0 30px}
:is(#wath,#wath-top) .bandh .cbtn{display:none}
#wath{padding-bottom:76px}
:is(#wath,#wath-top) .mcta{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:45;background:#ece7f7;border-top:1px solid rgba(27,21,38,.16);padding:10px 16px calc(10px + env(safe-area-inset-bottom));align-items:center;gap:14px;box-shadow:0 -6px 18px rgba(27,21,38,.08)}
:is(#wath,#wath-top) .mctat{display:flex;flex-direction:column;line-height:1.15}
:is(#wath,#wath-top) .mctat b{font-size:18px;color:#33697f}
:is(#wath,#wath-top) .mctat span{font-size:12px;color:#5b6478}
:is(#wath,#wath-top) .mcta .btn{flex:1;min-height:48px;font-size:17px}
:is(#wath,#wath-top) .toast{bottom:88px}
}
/* test page only: look at the phone layout from a computer */
:is(#wath,#wath-top) .pvb{position:fixed;left:16px;bottom:16px;z-index:44;display:inline-flex;align-items:center;gap:7px;background:#1b1526;color:#fff;border:0;border-radius:999px;padding:10px 16px;font-size:14px;font-weight:700;box-shadow:0 6px 18px rgba(27,21,38,.25);cursor:pointer}
:is(#wath,#wath-top) .pvo{display:none;position:fixed;inset:0;z-index:99990;background:rgba(27,21,38,.82);flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:14px}
:is(#wath,#wath-top) .pvo.on{display:flex}
:is(#wath,#wath-top) .pvh{display:flex;align-items:center;gap:16px;color:#fff;font-size:16px}
:is(#wath,#wath-top) .pvh .btn{background:#fff;border-color:#fff;color:#1b1526;min-height:38px}
:is(#wath,#wath-top) .pvf{width:390px;max-width:100%;height:min(820px,calc(100vh - 90px));border-radius:34px;border:10px solid #0f0c16;background:#fff;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.5)}
:is(#wath,#wath-top) .pvf iframe{width:100%;height:100%;border:0;display:block}
@media(max-width:700px){:is(#wath,#wath-top) .pvb{display:none}}
html.wath-framed :is(#wath,#wath-top) .pvb{display:none}
:is(#wath,#wath-top) .msd>summary{margin:0 -12px;padding:10px 12px;border-radius:10px;border-top:0;transition:background .15s}
:is(#wath,#wath-top) .msd{border-top:1px solid #e3dfee}
:is(#wath,#wath-top) .msd>summary:hover,:is(#wath,#wath-top) .msd>summary:focus-visible{background:#e3def2}
:is(#wath,#wath-top) .msd[open]>summary{background:#ebe6f6}
:is(#wath,#wath-top) .msd[open]>summary:hover{background:#e3def2}
:is(#wath,#wath-top) .fq>summary{margin:0 -12px;padding:15px 12px;border-radius:10px;transition:background .15s}
:is(#wath,#wath-top) .fq>summary:hover,:is(#wath,#wath-top) .fq>summary:focus-visible{background:#e3def2}
:is(#wath,#wath-top) .subnav .snl{position:relative;gap:2px}
:is(#wath,#wath-top) .subnav .snl a{position:relative;z-index:1;padding:13px 12px;transition:color .2s}
:is(#wath,#wath-top) .subnav .snl a.on,:is(#wath,#wath-top) .subnav .snl a.on:hover{color:#fff}
:is(#wath,#wath-top) .snp{position:absolute;left:0;top:50%;width:0;height:30px;margin-top:-15px;border-radius:999px;background:#6152a0;opacity:0;transition:left .28s cubic-bezier(.3,.7,.3,1),width .28s cubic-bezier(.3,.7,.3,1),opacity .2s;z-index:0;pointer-events:none}
@media(prefers-reduced-motion:reduce){:is(#wath,#wath-top) .snp{transition:none}}
@media(max-width:700px){:is(#wath,#wath-top) .subnav .snl{gap:0;padding-right:18px}:is(#wath,#wath-top) .subnav .wrap{padding-left:8px}}
@media(min-width:701px){:is(#wath,#wath-top) .subnav .snl{margin-left:-12px}}
:is(#wath,#wath-top) .skel{color:transparent!important;background:linear-gradient(90deg,#e9e6f1,#f5f3fa,#e9e6f1);border-radius:8px}
'''
# ---------- markup ----------
home=P[P.index('<main id="v-home">')+len('<main id="v-home">'):P.index('</main>')]
# hero video -> link to trailer with real photo
a=home.index('<div class="video">'); b=home.index('</div>',home.index('</button>',a))+6
home=home[:a]+'<a class="video" href="/trailer" data-trailer aria-label="Play the trailer" style="--ph:url(https://cdn.jsdelivr.net/gh/nirvanmullick/whatatrip-donor-wall@a16e9d9153ce12938211d08a74ccbc5c0c4cc9f5/home-page/img/rick-desert-plate.jpg)"><span class="vk" aria-hidden="true"><i class="k1"></i><i class="k2"></i><i class="k3"></i><i class="k4" style="background-image:url(https://cdn.jsdelivr.net/gh/nirvanmullick/whatatrip-donor-wall@1b7a0244740bb8ca34c9a99ff14fb69e89d86c3b/home-page/img/rick-desert-fg-2x-sharp.webp)"></i></span><span class="vt" aria-hidden="true"><b>WHAT A TRIP</b><span class="play pq"><svg aria-hidden="true" width="26" height="26" viewBox="0 0 24 24"><path d="M8 5l12 7-12 7z" fill="#fff"/></svg></span></span><span class="vc vcl" aria-hidden="true">From Executive Producer<strong>Darren Aronofsky</strong></span><span class="vc vcr" aria-hidden="true">A film by<strong>Nirvan Mullick</strong></span></a>'+home[b:]
# remove hero stats block
a=home.index('<div data-hero-stats'); b=home.index('</div></div>',a)+12
home=home[:a]+home[b:]
home=home.replace('<div class="match"><strong style="color:#2c2208">Every gift is doubled right now.</strong> $135K in matching challenges through Dec 31.</div>','<div class="match" data-matchline></div>')
home=home.replace('<h2>280 supporters and counting</h2>','<h2 data-supcount>Supporters</h2>')
home=home.replace('href="https://whatatrip.com/','href="/')
for i in ['story','recent','budget','perks','challenges','store','access','levels']:
    home=home.replace('id="%s"'%i,'id="wath-%s"'%i).replace('href="#%s"'%i,'href="#wath-%s"'%i)
home=home.replace('<button class="btn pri" data-toast="Preview only: this would start your own fundraiser page, e.g. whatatrip.com/yourname.">Start a fundraiser</button><span class="soon">Coming soon</span>','<a class="btn pri" data-fund="0" style="display:inline-flex;align-items:center;text-decoration:none" target="_blank" rel="noopener" href="https://www.pledge.to/peer-fundraisers/d33779b9d0a280bb7c145ae18e822ada/a255ae06d98c43581c2553685138d9a4/new">Start a fundraiser</a>')
home=home.replace('data-toast="Preview only: this would open the shirt in the store."','data-toast="The store is coming soon."').replace('data-toast="Preview only: this would open the store."','data-toast="The store is coming soon."')
home=home.replace('<a href="#wath-levels" data-chart','<a href="#wath-levels" data-chart')

# ---- submenu (Nov 15) ----
a=home.index('<div class="subnav">'); e=home.index('</div></div>',a)+12
home=home[:a]+'<div class="subnav"><div class="wrap"><div class="snl"><a href="#wath" data-top>Campaign</a><a href="#wath-story">Story</a><a href="#wath-recent">Community</a><a href="#wath-perks">Perks</a><a href="#wath-team">Filmmakers</a><a href="#wath-budget">Budget</a><a href="#wath-impact">Impact</a><a href="#wath-faq">FAQs</a><a href="#wath-comments">Comments<sup class="cnt" data-cnt="com"></sup></a><a href="#wath-levels" class="snm">Perks</a><a href="#wath-updates">Updates<sup class="cnt" data-cnt="upd"></sup></a></div><button class="btn pri" data-give>Donate</button></div></div>'+home[e:]
stub=lambda i,t,x:'<section class="sec" id="wath-%s"><h2>%s <span class="soon">Coming soon</span></h2><p class="sub">%s</p></section>'%(i,t,x)
a=home.index('<section class="sec" id="wath-recent">')
home=home[:a]+'<section class="sec" id="wath-team"><h2>Filmmakers</h2><div class="tm5"><button class="tmc" data-bio="darren" aria-haspopup="dialog"><img class="tmp" loading="lazy" alt="" width="84" height="84" style="object-position:50% 30%" src="https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/9b0e790b-0826-45ce-b5e3-2b2b28f01dbf/darren_aronofsky.jpeg?format=300w"><b>Darren Aronofsky</b><span>Executive Producer</span></button><button class="tmc" data-bio="nirvan" aria-haspopup="dialog"><img class="tmp" loading="lazy" alt="" width="84" height="84" style="object-position:50% 30%" src="https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/1555433778223-YF44T2R77O4M3UTN9J4O/nirvan_bw.jpg?format=300w"><b>Nirvan Mullick</b><span>Director, Producer</span></button><button class="tmc" data-bio="dream" aria-haspopup="dialog"><img class="tmp" loading="lazy" alt="" width="84" height="84" style="object-position:50% 25%" src="https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/1555431858411-Z2NV78ZE78PGR5BTJ8GZ/Dream_Mullick.jpg?format=300w"><b>Dream Mullick</b><span>Producer</span></button><button class="tmc" data-bio="jeffrey" aria-haspopup="dialog"><img class="tmp" loading="lazy" alt="" width="84" height="84" style="object-position:50% 30%" src="https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/1555431789123-2KB2SGD4YE7YE4AD0JE5/IMG_20181217_162143.jpg?format=300w"><b>Jeffrey Schneider</b><span>Cinematographer</span></button><button class="tmc" data-bio="vickie" aria-haspopup="dialog"><img class="tmp" loading="lazy" alt="" width="84" height="84" style="object-position:50% 25%" src="https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/93eff408-ea57-4c5f-b815-a4908353c04b/Vickie_BW.png?format=300w"><b>Vickie Curtis</b><span>Story Consultant</span></button><div class="tmc tmn"><span class="tmp tmi" aria-hidden="true">JC</span><b>Juli Crockett</b><span>Assistant to the Director</span></div></div><details class="crew"><summary>See the full crew<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><div class="tm5 crew5"><button class="tmc tmn" data-bio="micah" aria-haspopup="dialog"><span class="tmp tmi" aria-hidden="true">MV</span><b>Micah Van Hove</b><span>Rough Cut Editor</span></button><button class="tmc tmn" data-bio="jreeser" aria-haspopup="dialog"><span class="tmp tmi" aria-hidden="true">JR</span><b>Jeffrey Reeser</b><span>Rough Cut Editor</span></button></div></details></section>'+home[a:]
a=home.index('<section class="sec"><div class="card tnd" data-tnd>')
home=home[:a]+'<section class="sec" id="wath-faq"><h2>FAQs</h2><div class="card" style="padding:6px 20px"><details class="fq"><summary>What is the film about?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p><em>What a Trip</em> follows Rick Doblin and MAPS, the organization he founded, across a 40+ year effort to bring psychedelic therapy back into culture.</p></details><details class="fq"><summary>Who is making it?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>The film is directed by Nirvan Mullick, produced by Dream Mullick, and executive produced by Darren Aronofsky.</p></details><details class="fq"><summary>How long has it been in the works?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>Twelve years. We have been filming with Rick since 2014.</p></details><details class="fq"><summary>Where is the film now?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>Filming is largely done and we are editing the rough cut, one act at a time. The <a href="#wath-budget">budget section</a> shows which milestone we are funding right now.</p></details><details class="fq"><summary>When will it be finished?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>We are aiming for late 2027. The exact timing depends on how quickly the edit is funded.</p></details><details class="fq"><summary>How is the film funded?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>By donations, together with years of unpaid work and investment from the filmmakers. The total budget is $3.4M: $1.8M already raised and invested since 2014, $700K for the rough cut, and $900K for the final cut.</p></details><details class="fq"><summary>What does my donation pay for?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>Right now, editing. Every $50 covers about one hour of an editor&rsquo;s time. The budget section lists what each milestone pays for.</p></details><details class="fq"><summary>Is my donation tax-deductible?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>Yes. Donations go through Creative Visions Foundation, our nonprofit fiscal sponsor, and are tax-deductible, less the fair market value of any perk you receive.</p></details><details class="fq"><summary>How do I get perks?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>Each gift level comes with perks (see <a href="#wath-levels">Perks</a>). When you give, you choose which perks you want. Some perks are limited, so they are first come, first served. Perks with a market value, like a stay or a dinner, reduce the tax-deductible part of your gift, so you can say no thanks to keep your whole gift deductible. Gifts raised through your own fundraiser count toward your level too.</p></details><details class="fq"><summary>How do I manage my perks?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>Log in and open <b>Your perks</b> in your Member Dashboard. Once your gift clears, each perk you chose shows up there with its status and the next step: either we need something from you, like a shirt size, dates that work or how to spell your name, or our team is arranging it. You can message us about any perk from there, or email <a href="mailto:info@whatatrip.com">info@whatatrip.com</a>.</p></details><details class="fq"><summary>What is TRUTH Not DARE?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>It is the film&rsquo;s impact campaign, launching alongside the film. It offers honest education about the real risks and benefits of psychedelics. <a href="/impact">Read more</a>.</p></details></div></section>'+home[a:].replace('<section class="sec"><div class="card tnd" data-tnd>','<section class="sec" id="wath-impact"><div class="card tnd" data-tnd>',1)
a=home.index('<section class="sec" id="wath-store">')
home=home[:a]+'<section class="sec" id="wath-updates"><h2>Updates<sup class="cnt" data-cnt="upd"></sup></h2><p class="sub">Some updates are for members only.</p><div data-updates></div></section>'+home[a:]
old='A documentary about Rick Doblin, MAPS and the fight to legalize psychedelic therapy.'
assert old in home
home=home.replace(old,'A documentary following Rick&rsquo;s 40+ year journey with MAPS to bring psychedelics back into culture.')

# ---- page order follows the submenu (Nov 15): Story, Community | Perks | Filmmakers, Budget, (Matching), Impact, FAQs, Updates, Comments, Store, Access ----
def cut(i):
    global home
    a=home.index('<section class="sec" id="wath-%s"'%i); e=home.index('</section>',a)+10
    s=home[a:e]; home=home[:a]+home[e:]; return s
S={i:cut(i) for i in ['team','budget','challenges','impact','faq','updates','store','access']}
S['comments']='<section class="sec" id="wath-comments"><h2>Comments<sup class="cnt" data-cnt="com"></sup></h2><div class="card" style="padding:10px 20px 16px" data-comments></div></section>'
mark='<div class="wrap cols second"><div class="stack">'
assert mark in home
home=home.replace(mark,mark+''.join(S[i] for i in ['team','budget','challenges','impact','faq','comments','updates']),1)
home=home.replace('<div class="match" data-matchline></div>','<div class="kstats" data-kstats></div><div class="match" data-matchline></div>',1)
assert 'data-kstats' in home
chart=P[P.index('<div class="ov" id="ov-chart">'):P.index('<div class="toast"')]
top='<div class="mcta"><span class="mctat"><b data-mneed></b><span>still needed</span></span><button class="btn pri" data-give>Donate now</button></div><button class="bgp" data-bugpill aria-label="Report a bug or idea"><svg aria-hidden="true" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 8a4 4 0 0 1 8 0v1H8z"/><rect x="7" y="9" width="10" height="11" rx="5"/><path d="M12 13v7M3 13h4M17 13h4M4 19l3-2M20 19l-3-2M4 7l3 2M20 7l-3 2"/></svg>Report a bug</button><button class="pvb" data-pv aria-label="Preview this page as it looks on a phone"><svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="2" width="10" height="20" rx="2.5"/><path d="M11 18h2"/></svg>Phone preview</button><div class="pvo" data-pvo><div class="pvh"><b>Phone preview</b><button class="btn" data-pvx>Back to desktop</button></div><div class="pvf" data-pvf></div></div><a id="wath-plg" data-plg-action="donate" data-widget-id="6GNakp1GtmAa92RH" href="/donate" hidden>Donate</a>'+chart+'<div class="toast" id="wath-toast" role="status"></div>'
# ---------- data ----------
photos=json.load(open('photos.json'))
photos['rachel hamilton']={'src':'https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/b4f47436-f528-4275-9249-ee476b67d384/rachel-hamilton_1.jpg?format=500w'}
photos['meg & david roth']={'src':'https://cdn.jsdelivr.net/gh/nirvanmullick/whatatrip-donor-wall@main/home-page/img/roth.jpg'}
a=P.index('var COMMENTS=');b=P.index(';\nvar supTab',a)
handq=[[c[0],c[3]] for c in json.loads(P[a+13:b]) if c[2]=='']
def grab(name,end):
    a=P.index(name); b=P.index(end,a); return P[a:b]
LEVELS=grab('var LEVELS=[','var PERKS=').replace(' <span class="soon">Coming soon</span>',' <span class="soon">Coming soon</span>')
PERKS=grab('var PERKS=','var STAGES=')
BUL=grab('var BUL=','function msRow(')
bud=json.load(open('bud.json'))
js=open('app.js').read()
js=js.replace('/*LEVELS*/',LEVELS).replace('/*PERKS*/',PERKS).replace('/*BUL*/',BUL).replace('/*PHOTOS*/','var PHOTOS='+json.dumps(photos,ensure_ascii=False)+';').replace('/*HANDQ*/','var HANDQ='+json.dumps(handq,ensure_ascii=False)+';')

# ---- Nov 15: share row under the video; clearer tax note under Donate ----
import re as _re
_m=_re.search(r'<div style="display:flex;gap:10px"><button class="btn" style="flex:1" data-copy="https://whatatrip.com">Share</button>.*?</div>\n?',home,_re.S)
assert _m
home=home[:_m.start()]+home[_m.end():]
_end='<p class="fine">Tax-deductible, less the fair market value of any perk you receive.</p></div></div>'
assert home.count(_end)==1
_ic=lambda d:'<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">'+d+'</svg>'
_u='https%3A%2F%2Fwhatatrip.com'
_t='Help%20bring%20Rick%20Doblin%E2%80%99s%20story%20to%20the%20screen.%20WHAT%20A%20TRIP%2C%20executive%20produced%20by%20Darren%20Aronofsky.'
_shr=('<div class="shr"><button type="button" class="remb" data-remind title="Sign up for updates and to join the journey" aria-label="Sign up for updates and to join the journey"><svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9a6 6 0 0 1 12 0c0 6 2.5 7.5 2.5 7.5h-17S6 15 6 9z"/><path d="M10 20a2.2 2.2 0 0 0 4 0"/></svg><span class="remu">Sign up</span><span class="remi">Signed up</span></button><span class="shl2">Share:</span><div class="shb">'
 +'<a class="sh1" aria-label="Share on Facebook" title="Facebook" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u='+_u+'">'+_ic('<path d="M13.6 21v-7.6h2.55l.4-3H13.6V8.5c0-.87.25-1.46 1.5-1.46h1.6V4.36c-.28-.04-1.23-.12-2.33-.12-2.3 0-3.87 1.4-3.87 3.98v2.2H7.9v3h2.6V21z"/>')+'</a>'+'<button type="button" class="sh1" data-embed aria-label="Embed or copy a short link" title="Embed or short link"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/></svg></button>'
 +'<a class="sh1" aria-label="Share on X" title="X" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?url='+_u+'&text='+_t+'">'+_ic('<path d="M17.75 3h3.07l-6.7 7.66L22 21h-6.17l-4.83-6.32L5.47 21H2.4l7.17-8.2L2 3h6.33l4.37 5.78zm-1.08 16.17h1.7L7.4 4.74H5.58z"/>')+'</a>'
 +'<a class="sh1" aria-label="Share on Bluesky" title="Bluesky" target="_blank" rel="noopener" href="https://bsky.app/intent/compose?text='+_t+'%20'+_u+'">'+_ic('<path d="M6.3 4.4c2.3 1.7 4.7 5.2 5.7 7 1-1.8 3.4-5.3 5.7-7 1.6-1.2 4.3-2.2 4.3.9 0 .6-.4 5.2-.6 5.9-.7 2.6-3.4 3.2-5.7 2.8 4.1.7 5.1 3 2.9 5.3-4.3 4.4-6.1-1.1-6.6-2.5-.1-.3-.1-.4 0-.3 0-.1 0 0-.1.3-.5 1.4-2.3 6.9-6.6 2.5-2.2-2.3-1.2-4.6 2.9-5.3-2.3.4-5-.3-5.7-2.8-.2-.7-.6-5.3-.6-5.9 0-3.1 2.7-2.1 4.4-.9z"/>')+'</a>'
 +'<a class="sh1" aria-label="Share by email" title="Email" href="mailto:?subject=WHAT%20A%20TRIP%3A%20The%20Rick%20Doblin%20Story&body='+_t+'%0A%0A'+_u+'">'+_ic('<path d="M3 6.6A1.6 1.6 0 0 1 4.6 5h14.8A1.6 1.6 0 0 1 21 6.6v.25l-9 5.6-9-5.6zm0 2.6v8.2A1.6 1.6 0 0 0 4.6 19h14.8a1.6 1.6 0 0 0 1.6-1.6V9.2l-9 5.6z"/>')+'</a>'
 +''
 +'</div></div>')
_tax='<div class="taxn"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.5"/><path d="M7.5 12.5l3 3 6-6.5"/></svg><div><b>Donations are tax-deductible</b><span>Less the fair market value of any perk you receive.</span></div></div>'
home=home.replace(_end,'</div>'+_shr+'</div>',1)  # Nov 17 later: share row sits under the video, Donate lines up with the video bottom  # Nov 17: tax note dropped (the kband says it); share row sits under Donate now

_c='<div class="chs" data-challenges></div>'
assert home.count(_c)==1
home=home.replace(_c,_c)  # Nov 17: Start a challenge now lives inside the list (renderChallenges)

# Budget / "Where the money goes" sits under the supporters in the first (left) column, beside the level list.
def _section(html,start):
    i=html.index(start);d=0;k=i
    while True:
        o=html.find('<section',k+1);c=html.find('</section>',k+1)
        if o!=-1 and o<c: d+=1;k=o
        else:
            if d==0: return i,c+len('</section>')
            d-=1;k=c
_a,_b=_section(home,'<section class="sec" id="wath-budget"')
_bud=home[_a:_b];home=home[:_a]+home[_b:]
_a,_b=_section(home,'<section class="sec" id="wath-recent"')
home=home[:_b]+_bud+home[_b:]
_n1='<a href="#wath-perks">Perks</a><a href="#wath-team">Filmmakers</a><a href="#wath-budget">Budget</a>'
assert home.count(_n1)==1
home=home.replace(_n1,'<a href="#wath-budget">Budget</a><a href="#wath-perks">Perks</a><a href="#wath-team">Filmmakers</a>')

# Tabs: FAQs, Comments and Updates each open in place of the campaign scroll (Story to Impact stays one scroll).
_t1='<a href="#wath-faq">FAQs</a>'
assert home.count(_t1)==1
home=home.replace(_t1,'<i class="snd" aria-hidden="true"></i>'+_t1)
# Nov 16 (Nirvan): perks carousel folded into Choose your level; Filmmakers becomes the full-width band in its place; FAQs move up under the supporters
_ps=home.find('<section class="band" id="wath-perks">');_pe=home.find('<div class="wrap cols second">',_ps)
assert _ps>0 and _pe>_ps
_ts=home.find('<section class="sec" id="wath-team">');_te=home.find('</section>',_ts)+len('</section>')
_team=home[_ts:_te];home=home[:_ts]+home[_te:]
_inner=_team[len('<section class="sec" id="wath-team">'):-len('</section>')]
_ps=home.find('<section class="band" id="wath-perks">');_pe=home.find('<div class="wrap cols second">',_ps)
home=home[:_ps]+'<section class="band tband" id="wath-team"><div class="wrap">'+_inner+'</div></section>\n'+home[_pe:]
_fs=home.find('<section class="sec" id="wath-faq">');_fe=home.find('</section>',_fs)+len('</section>')
_faq=home[_fs:_fe];home=home[:_fs]+home[_fe:]
_rs=home.find('<section class="sec" id="wath-recent">');_re=home.find('</section>',_rs)+len('</section>')
assert _rs>0
home=home[:_re]+_faq+home[_re:]
home=home.replace('<a href="#wath-perks">Perks</a>','<a href="#wath-levels">Perks</a>')
# Nov 17 (Nirvan): a clear "Impact" heading above the T.R.U.T.H. Not D.A.R.E. card
_ia='<section class="sec" id="wath-impact"><div class="card tnd" data-tnd>'
assert home.count(_ia)==1
home=home.replace(_ia,'<section class="sec" id="wath-impact"><h2 class="imph">Impact Campaign</h2><div class="card tnd" data-tnd>')

# Nov 17 (Nirvan): a second photo band (Rick in coloured light), moved to the very bottom under Updates, just above the footer
_im=len(home)
home=home[:_im]+'<section class="rband fband" aria-label="Rick Doblin"><div class="rbimg" role="img" aria-label="Close-up of Rick Doblin lit in red and blue" style="background-image:url(https://cdn.jsdelivr.net/gh/nirvanmullick/whatatrip-donor-wall@4bea9baf0ec58ab40213efe8896f314c05fa861e/home-page/img/rick-face-light.jpg)"></div><div class="wrap rbw"><div class="rbt"><p class="rbk">Fifty years. One mission.</p><h2>Bring psychedelics from the underground back into the culture.</h2><div class="rbb"><button class="btn pri" data-give>Help tell this story</button></div></div></div></section>\n'+home[_im:]
# Nov 17 (Nirvan): trailer card - play button sits lower and centred, between the desert plate and Rick (so Rick grows in front of it);
# "The Rick Doblin Story" with a short white line under WHAT A TRIP; credits move up under it.
_play='<span class="play pq"><svg aria-hidden="true" width="26" height="26" viewBox="0 0 24 24"><path d="M8 5l12 7-12 7z" fill="#fff"/></svg></span>'
assert home.count('<b>WHAT A TRIP</b>'+_play+'</span>')==1
home=home.replace('<b>WHAT A TRIP</b>'+_play+'</span>','<b>WHAT A TRIP</b><em class="vsub"><svg class="vorn" viewBox="0 0 240 24" aria-hidden="true" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path pathLength="1" d="M120 12 C108 12 100 4 90 6 C82 8 82 17 89 17 C95 17 95 10 90 10 M120 12 C104 12 70 12 52 12 C40 12 34 6 26 8 C20 10 22 16 27 15 M52 12 C40 12 30 18 18 16"/><path pathLength="1" d="M120 12 C132 12 140 4 150 6 C158 8 158 17 151 17 C145 17 145 10 150 10 M120 12 C136 12 170 12 188 12 C200 12 206 6 214 8 C220 10 218 16 213 15 M188 12 C200 12 210 18 222 16"/><path d="M120 7 L124 12 L120 17 L116 12 Z" fill="#fff" stroke="none"/></svg><span>The Rick Doblin Story</span></em></span>')
assert home.count('<i class="k4"')==1
home=home.replace('<i class="k4"','<span class="play pq kplay">'+_play[len('<span class="play pq">'):-len('</span>')]+'</span><i class="k4"')

# Nov 17 (Nirvan): Kickstarter-style light band under the hero; Perks out of the menu (the column is beside it)
home=home.replace('<a href="#wath-levels">Perks</a>','',1)
_sn=home.find('<div class="subnav">')
_ic=lambda d:'<svg aria-hidden="true" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+d+'</svg>'
_bi=lambda d:'<svg aria-hidden="true" width="33" height="33" viewBox="0 0 24 24" fill="none" stroke="#1b1526" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'+d+'</svg>'
_HX='M30 3l23.4 13.5v27L30 57 6.6 43.5v-27z'
def _blob(c,dk,deco):
    return '<svg class="kbb" aria-hidden="true" viewBox="-8 -8 76 76"><path fill="'+c+'" d="'+_HX+'"/><g fill="none" stroke="'+dk+'" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'+deco+'</g></svg>'
# four different molecule touches: an echo outline, a fused five-ring with two oxygens, a zig-zag side chain, inner benzene bonds
_decos=[('#f3c9b9','#e3a48c','<path d="M53.4 16.5l7.4-4.3"/><circle cx="62.5" cy="11" r="2.4" fill="#e3a48c" stroke="none"/>'),
 ('#cfe3c2','#9fc68c','<path d="M30 57v7.5"/><circle cx="30" cy="66.5" r="2.4" fill="#9fc68c" stroke="none"/>'),
 ('#f5dc8a','#dcb94c','<path d="M6.6 43.5l-7.4 4.3"/><circle cx="-2.9" cy="49" r="2.4" fill="#dcb94c" stroke="none"/>'),
 ('#d9cdf3','#a995da','<path d="M30 3v-7.5"/><circle cx="30" cy="-6.5" r="2.4" fill="#a995da" stroke="none"/>')]
_items=[(_bi('<g fill="#1b1526" stroke="none"><circle cx="6.6" cy="6.4" r="3.6"/><circle cx="14.6" cy="5.6" r="4.4"/><rect x="2.2" y="10.6" width="14.8" height="9.4" rx="1.6"/><path d="M17.6 13.6l4.6-2.6v8.6l-4.6-2.6z"/></g><g fill="#fff" stroke="none"><circle cx="6.6" cy="6.4" r="1.1"/><circle cx="14.6" cy="5.6" r="1.3"/></g>'),'12 years in the making.','Filmed since 2014, with rare access to Rick and MAPS.'),
 (_bi('<circle cx="6.5" cy="6.5" r="2.8"/><circle cx="6.5" cy="17.5" r="2.8"/><path d="M8.6 8.4L20 18M8.6 15.6L20 6"/>'),'$50 = one hour of editing.','Every gift goes straight into finishing the film.'),
 (_bi('<path d="M8.5 7.5a3.5 3.5 0 0 0-6 2.5c0 3.5 6 7 6 7s6-3.5 6-7a3.5 3.5 0 0 0-6-2.5z"/><path d="M15.5 7.2a3.5 3.5 0 0 1 6 2.6c0 3.4-5.2 6.6-6 7.1"/>'),'Every gift doubled.','A <span data-poolall>$190K</span> matching challenge pool doubles gifts through <span data-matchend>Dec 31</span>.'),
 (_bi('<g fill="#1b1526" stroke="none"><path d="M10 2.5c.6 4.4 2.6 6.4 7 7-4.4.6-6.4 2.6-7 7-.6-4.4-2.6-6.4-7-7 4.4-.6 6.4-2.6 7-7z"/><path d="M18.5 13c.35 2.4 1.4 3.45 3.8 3.8-2.4.35-3.45 1.4-3.8 3.8-.35-2.4-1.4-3.45-3.8-3.8 2.4-.35 3.45-1.4 3.8-3.8z"/><path d="M18.6 1.8c.22 1.5.88 2.16 2.4 2.4-1.52.24-2.18.9-2.4 2.4-.22-1.5-.88-2.16-2.4-2.4 1.52-.24 2.18-.9 2.4-2.4z"/><circle cx="5" cy="19.6" r="1.2"/></g>'),'Tax-deductible','minus the fair market value of any perks you receive.')]
home=home[:_sn]+'<div class="kband" role="list"><div class="wrap kbw">'+''.join('<div class="kbi" role="listitem"><span class="kbic">'+_blob(*_decos[n])+it[0]+'</span><p><b>'+it[1]+'</b> '+it[2]+'</p></div>' for n,it in enumerate(_items))+'</div></div>\n'+home[_sn:]

# Nov 17 1pm (Nirvan): order after the perks is the Rick banner, then More ways to help (heading + buttons), then Arcturus.
#   More ways to help leaves the sidebar and gets its own section right after the banner. On phones a script moves the banner
#   and this section up to sit right after the perks (see placeRband in app.js).
_mw='<div class="mwh" data-mwh></div>'
assert home.count(_mw)==1
home=home.replace(_mw,'',1)
# Nov 17 (Nirvan): the close-up of Rick breaks up the page, between the columns and the Filmmakers band
_tb=home.find('<section class="band tband" id="wath-team">')
assert _tb>0
home=home[:_tb]+'<section class="rband" aria-label="About Rick Doblin"><div class="rbimg" role="img" aria-label="Rick Doblin on the phone in the desert at dusk" style="background-image:url(https://cdn.jsdelivr.net/gh/nirvanmullick/whatatrip-donor-wall@20759526d18f6ccd6ec0c0754a4b07b556a0a469/home-page/img/rick-closeup.jpg)"></div><div class="wrap rbw"><div class="rbt"><p class="rbk">The Rick Doblin Story</p><h2>When he was 18, Rick Doblin dropped out to become a psychedelic therapist.</h2><p class="rbs">But first, he would need to change the world.</p><div class="rbb"><button class="btn pri" data-give>Donate now</button><button class="btn rbtr" data-trailer>Watch the trailer</button></div></div></div></section>\n'+home[_tb:]
_rb=home.find('<section class="rband" aria-label="About Rick Doblin">');_rbe=home.find('</section>',_rb)+len('</section>')
assert _rb>0

# Nov 17 (Nirvan): one scroll, menu in the same order as the page, no tabs
_ns=home.find('<div class="snl">');_ne=home.find('</div>',_ns)+len('</div>')
assert _ns>0
home=home[:_ns]+'<div class="snl"><a href="#wath" data-top>Campaign</a><a href="#wath-levels" class="snm">Perks</a><a href="#wath-story">Story</a><a href="#wath-recent">Community</a><a href="#wath-faq">FAQs<sup class="cnt" data-cnt="faq"></sup></a><a href="#wath-budget">Budget</a><a href="#wath-impact">Impact</a><a href="#wath-team">Filmmakers</a><a href="#wath-comments">Comments<sup class="cnt" data-cnt="com"></sup></a><a href="#wath-updates">Updates<sup class="cnt" data-cnt="upd"></sup></a></div>'+home[_ne:]

# Nov 16 11pm (Nirvan): on desktop the share icons sit at the right end of the menu bar, under the big Donate button; the small Donate takes their place once you scroll
_ss=home.find('<div class="shr">');_se=home.find('</div></div>',_ss)+len('</div></div>')
assert _ss>0
_shr=home[_ss:_se].replace('<div class="shr">','<div class="shr snshr">',1)
_db='<button class="btn pri" data-give>Donate</button></div></div>'
assert home.count(_db)==1
home=home.replace(_db,'<span class="snr">'+_shr+'<button class="btn pri" data-give>Donate now</button></span></div></div>',1)

# Nov 16 11pm (Nirvan): Matching challenges, then Comments, move to the left column under the budget
def _cut(h,sid):
    s=h.find('<section class="sec" id="'+sid+'">');e=h.find('</section>',s)+len('</section>')
    assert s>0
    return h[:s]+h[e:],h[s:e]
home,_chal=_cut(home,'wath-challenges')
home,_coms=_cut(home,'wath-comments')
_bs=home.find('<section class="sec" id="wath-budget">');_be=home.find('</section>',_bs)+len('</section>')
assert _bs>0
home=home[:_be]+_chal+_coms+home[_be:]



# Nov 17 1:09pm (Nirvan): after the perks: Rick banner, Filmmakers, Impact, Comments, Updates, then More ways to help + Arcturus, then the closing banner
_cs=home.find('<section class="sec" id="wath-comments">');_ce=home.find('</section>',_cs)+len('</section>')
assert _cs>0
_com=home[_cs:_ce];home=home[:_cs]+home[_ce:]
_us=home.find('<section class="sec" id="wath-updates">');assert _us>0
home=home[:_us]+_com+home[_us:]
# Nov 17 1:20pm (Nirvan): Impact moves into the left column under Matching challenges, filling the space beside the perks
_is,_ie=_section(home,'<section class="sec" id="wath-impact"')
_imp=home[_is:_ie];home=home[:_is]+home[_ie:]
# Nov 17 2:47pm (Nirvan): Budget, then the Rick banner as soon as the perks end, Filmmakers, Matching challenges,
#   Impact as a full-width band, then Comments + Updates. Challenges (and Impact) wait in their own sections after
#   Filmmakers; on a computer a script lifts them into the left column only when that fills the space beside the perks.
_ch,_che=_section(home,'<section class="sec" id="wath-challenges"')
_chal2=home[_ch:_che];home=home[:_ch]+home[_che:]
_tm=home.find('<section class="band tband" id="wath-team">');_tme=home.find('</section>',_tm)+len('</section>')
assert _tm>0
# Nov 17 4:05pm (Nirvan): Impact comes before Filmmakers, to match the menu
home=home[:_tm]+'<section class="impband" data-imphome><div class="wrap">'+_imp+'</div></section>'+home[_tm:_tme]+'<div class="wrap chwrap" data-chhome>'+_chal2+'</div>'+home[_tme:]
_fb=home.find('<section class="rband fband"');assert _fb>0
# Nov 17 1:21pm (Nirvan): More ways to help + Arcturus sit in a right sidebar beside Comments and Updates
_c2=home.find('<div class="wrap cols second"><div class="stack">');assert _c2>0
_c2e=home.find('</div>',home.find('</section>',home.find('<section class="sec" id="wath-updates">')))  # end of .stack
assert home[_c2e:_c2e+6]=='</div>'
home=home[:_c2e+6]+'<aside class="mwside" id="wath-help"><div class="mwh" data-mwh></div></aside>'+home[_c2e+6:]

extra+="""
#wath[data-tabv]>:not(.hero):not(.subnav):not(.cols.second){display:none}
#wath:is([data-tabv="faq"],[data-tabv="comments"])>.cols:not(.second){display:block!important;min-height:100vh;padding-top:44px}
#wath:is([data-tabv="faq"],[data-tabv="comments"])>.cols:not(.second)>aside,#wath[data-tabv="faq"]>.cols:not(.second) .stack>.sec:not(#wath-faq),#wath[data-tabv="comments"]>.cols:not(.second) .stack>.sec:not(#wath-comments){display:none!important}
#wath:is([data-tabv="faq"],[data-tabv="comments"])>.cols:not(.second) :is(#wath-faq,#wath-comments){border-top:0;padding-top:0}
#wath:is([data-tabv="faq"],[data-tabv="comments"])>.cols.second{display:none}
#wath[data-tabv] .cols.second .stack>.sec{display:none}
#wath[data-tabv="faq"] .cols.second .stack>#wath-faq,#wath[data-tabv="comments"] .cols.second .stack>#wath-comments,#wath[data-tabv="updates"] .cols.second .stack>#wath-updates{display:block;border-top:0;padding-top:0}
#wath[data-tabv] .cols.second{min-height:100vh;padding-top:44px}
#wath .soc{margin-top:16px;padding-top:14px;border-top:1px solid #ece8f4}
#wath .socr{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
#wath .rxb{display:inline-flex;flex-wrap:wrap;gap:6px}
#wath .rx{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:4px;min-width:30px;height:30px;padding:0 7px;border-radius:8px;border:1px solid #e3def0;background:#fff;font-family:inherit;font-size:12.5px;font-weight:700;line-height:1;color:#4a4560;transition:background .15s,border-color .15s}
#wath .rx .rxe{font-size:14px;line-height:1}
#wath .rx:hover{background:#f4f1fb;border-color:#d4cce9}
#wath .rx.on{background:#ece7fa;border-color:#8f7fd0;color:#3d3175}
#wath .rx:focus-visible,#wath .cml button:focus-visible{outline:2px solid #5d4fa6;outline-offset:2px}
#wath .rxb.sm .rx{min-width:26px;height:26px;padding:0 5px;border-radius:7px}
#wath .rxb.sm .rx .rxe{font-size:12.5px}
#wath .dncm{padding:4px 0 14px 46px;border-bottom:1px solid #ece8f4}
@media(max-width:520px){#wath .dncm{padding-left:0}}
#wath .socn{all:unset;cursor:pointer;font-family:inherit;font-size:14px;font-weight:600;line-height:1.2;color:#5d4fa6;padding:6px 2px}
#wath .socn:hover{text-decoration:underline}
#wath .socl{margin-top:14px;display:flex;flex-direction:column;gap:14px}
#wath .cm{display:flex;gap:12px;align-items:flex-start}
#wath .cm .av{flex:none}
#wath .cm.hid{opacity:.55}
#wath .cmb{flex:1;min-width:0;background:#fff;border:1px solid #ebe7f3;border-radius:12px;padding:10px 14px}
#wath .cmh{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;font-size:14px}
#wath .cmh span{color:#7a7f90;font-size:13px}
#wath .cmb p{margin:4px 0 0;font-size:15px;line-height:1.5;color:#1f2430;overflow-wrap:anywhere}
#wath .cml{display:flex;gap:14px;margin-top:6px}
#wath .cml button{all:unset;cursor:pointer;font-family:inherit;font-size:13px;font-weight:600;color:#5d4fa6}
#wath .cml button:hover{text-decoration:underline}
#wath .cml button[data-arm]{color:#8a3b3b}
#wath .cm0{margin:0;color:#7a7f90;font-size:14px}
#wath .cmf{display:flex;gap:10px;align-items:flex-end;margin-top:14px}
#wath .cmf textarea,#wath .cmb textarea{flex:1;width:100%;box-sizing:border-box;min-height:44px;border:1px solid #d9d3ea;border-radius:10px;padding:10px 12px;font-family:inherit;font-size:15px;line-height:1.45;color:#1f2430;background:#fff;resize:vertical}
#wath .cmf .btn{flex:none}
#wath .cma{display:flex;gap:8px;margin-top:8px}
#wath .cmn{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:14px;font-size:14px;color:#5b6478}
#wath .dn .wn{display:flex;flex-wrap:wrap;align-items:center;column-gap:10px;row-gap:4px;min-width:0}
#wath .dn .wn .rxb{gap:4px}
#wath .dn .amtc{flex:none}
#wath .dn .amtc .when{white-space:nowrap}
#wath .dn .who{min-width:0}
@media(max-width:520px){#wath .cmf{flex-direction:column;align-items:stretch}}
@media(min-width:901px){#wath .subnav .btn[data-give]{opacity:0;visibility:hidden;transform:translateY(14px);transition:opacity .28s ease,transform .28s ease,visibility 0s linear .28s}
#wath.sngive .subnav .btn[data-give]{opacity:1;visibility:visible;transform:none;transition:opacity .28s ease,transform .28s ease,visibility 0s}}
@media(prefers-reduced-motion:reduce){#wath .subnav .btn[data-give]{transition:none!important;transform:none!important}}
#wath .mx.mxg{display:grid!important;grid-template-columns:58px minmax(0,1fr);column-gap:12px;row-gap:0;align-items:center;padding:14px 16px 14px 14px;position:relative}
#wath .mx.mxg>*{grid-column:2}
#wath .mx.mxg .mh{grid-column:1/-1;font-size:18px;line-height:1.25;margin:0;padding:0 26px;text-align:center}
@media(max-width:520px){#wath .mx.mxg .mh{font-size:16px;padding:0 22px}}
#wath .mx.mxg .mxs2{display:block;grid-row:2;margin-top:8px}
#wath .mx.mxg .mxrow{display:contents}
#wath .mx.mxg .mxi2{grid-column:1;grid-row:3;align-self:center;position:relative;width:58px;height:34px;margin-top:4px;z-index:1}
#wath .mx.mxg .mxi2 .mxi{position:absolute;top:0;width:34px;height:34px;margin:0;box-shadow:0 0 0 3px #fbf3df}
#wath .mx.mxg .mxi2 .g1{left:0}
#wath .mx.mxg .mxi2 .g2{left:24px}
#wath .mx.mxg .mxrow .mxb{grid-column:2;grid-row:3;align-self:center;height:10px;margin:4px 0 0 -16px;border-radius:0 999px 999px 0}
#wath .mx.mxg .mxrow .mxb i{border-radius:0 999px 999px 0}
#wath .mx.mxg .mxl{grid-row:4;margin-top:6px}
#wath .mx.mxg .chev{position:absolute;top:16px;right:14px}
#wath #wath-levels .lv .lvi{aspect-ratio:16/9;display:flex}
#wath #wath-levels .lv .lvi .fa-cr b{font-size:20px!important}
#wath #wath-levels .lvlim{margin-top:16px;padding:10px 12px;border-radius:10px;background:#efeaf9;display:flex;flex-direction:column;gap:2px}
#wath #wath-levels .lvlt{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#6152a0}
#wath #wath-levels .lvla{font-size:14px;font-weight:600;color:#1b1526}
#wath #wath-levels .lvla.out{color:#8a3b3b}
#wath .tband{padding:56px 0}
#wath .tband h2{margin-top:0}
#wath .card.tndd{align-items:flex-start}
#wath .tndside{flex:0 0 auto;width:min(320px,100%);display:flex;flex-direction:column;align-items:flex-start;gap:20px}
#wath .tndside .tndl{width:100%;margin:0}
#wath .tndside .tndb .btn.tj{min-width:150px;justify-content:center}
#wath .tndt{flex:1 1 0;max-width:600px}
/* Trailer card (Nov 16): title + play button up top; credits sit low in the desert either side of Rick */
:is(#wath,#wath-top) .video .vt{top:3.5%!important}
:is(#wath,#wath-top) .video .vc{position:absolute;bottom:7%;z-index:2;display:flex;flex-direction:column;align-items:center;text-align:center;gap:.6cqw;white-space:nowrap;transform:translateX(-50%);font-size:1.9cqw;line-height:1.2;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:#e6ebff;text-shadow:0 2px 14px rgba(27,21,38,.7),0 0 2px rgba(27,21,38,.4);opacity:0;animation:wathUpX .9s cubic-bezier(.2,.7,.2,1) 1.9s forwards}
@keyframes wathUpX{from{opacity:0;transform:translate(-50%,14px)}to{opacity:1;transform:translate(-50%,0)}}
:is(#wath,#wath-top) .video .vc strong{display:block;font-size:2.6cqw;font-weight:800;letter-spacing:.08em;color:#fff}
:is(#wath,#wath-top) .video .vcl{left:18.5%}
:is(#wath,#wath-top) .video .vcr{left:81.5%}
:is(#wath,#wath-top) .video.playing .vc{display:none}
@media(prefers-reduced-motion:reduce){:is(#wath,#wath-top) .video .vc{animation:none;opacity:1;transform:translateX(-50%)}}
@media(max-width:700px){:is(#wath,#wath-top) .video .vc{font-size:2.3cqw;bottom:6%;letter-spacing:.08em}:is(#wath,#wath-top) .video .vc strong{font-size:2.9cqw;letter-spacing:.04em}:is(#wath,#wath-top) .video .vcl{left:19.5%}:is(#wath,#wath-top) .video .vcr{left:80.5%}}
#wath .subnav .snr{display:grid;flex:none;align-items:center;justify-items:end}
#wath .subnav .snr>*{grid-area:1/1}
#wath .subnav .snshr{display:flex;flex-wrap:nowrap;align-items:center;gap:10px;margin:0!important;padding:0!important;border:0!important;transition:opacity .25s ease,visibility 0s linear 0s}
#wath .subnav .snshr .shl{width:auto;font-size:11.5px}
#wath .subnav .snshr .shb{flex-wrap:nowrap;gap:6px}
#wath .subnav .snshr .sh1{width:34px;height:34px}
#wath.sngive .subnav .snshr{opacity:0;visibility:hidden;transition:opacity .2s ease,visibility 0s linear .2s}
@media(min-width:1240px){#wath .hero-grid>.shr{display:none!important}}
@media(max-width:1239px){#wath .subnav .snshr{display:none}}
:is(#wath,#wath-top) .video .vt .play.pq{width:clamp(56px,9cqw,84px);height:clamp(56px,9cqw,84px);padding:0;border-radius:14px;background:#6152a0;justify-content:center;gap:0;margin-top:2.4cqw;box-shadow:0 10px 28px rgba(27,21,38,.35)}
:is(#wath,#wath-top) .video .vt .play.pq svg{width:50%;height:50%;margin-left:6%}
:is(#wath,#wath-top) .video:hover .vt .play.pq{background:#54479a}
#wath .mwh{margin-top:18px;display:flex;flex-direction:column;gap:14px}
#wath .mwh .mwt{font-size:22px;margin:10px 0 0}
#wath .mwa{all:unset;box-sizing:border-box;cursor:pointer;display:flex;flex-direction:column;border-radius:14px;overflow:hidden;background:#1b1526;color:#fff;box-shadow:0 8px 24px rgba(27,21,38,.18);transition:transform .2s ease}
#wath .mwa:hover{transform:translateY(-2px)}
#wath .mwa:focus-visible{outline:3px solid #6152a0;outline-offset:3px}
#wath .mwai{display:block;aspect-ratio:16/9;background:#3a3350 center/cover}
#wath .mwab{display:flex;flex-direction:column;gap:4px;padding:14px 16px 16px}
#wath .mwak{font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#c9bff0}
#wath .mwab b{font-size:20px;line-height:1.15}
#wath .mwab span{font-size:14px;line-height:1.4;color:#e4dff5}
#wath .mwab .mwago{margin-top:6px;font-weight:700;color:#fff}
#wath .mwl{display:flex;flex-direction:column;background:#fff;border:1px solid rgba(27,21,38,.1);border-radius:14px;overflow:hidden}
#wath .mwr{all:unset;box-sizing:border-box;cursor:pointer;display:flex;gap:12px;align-items:flex-start;padding:13px 14px;border-top:1px solid rgba(27,21,38,.08);color:#1b1526;text-decoration:none}
#wath .mwr:first-child{border-top:0}
#wath .mwr:hover{background:#f6f3fc}
#wath .mwr:focus-visible{outline:2px solid #6152a0;outline-offset:-2px}
#wath .mwic{flex:none;width:36px;height:36px;border-radius:10px;background:#ece7fa;color:#5d4fa6;display:inline-flex;align-items:center;justify-content:center}
#wath .mwtx{display:flex;flex-direction:column;gap:2px;min-width:0}
#wath .mwtx b{font-size:15px}
#wath .mwtx span{font-size:13.5px;line-height:1.4;color:#5b6478}
.arcov{padding:2vh 2vw!important}
.arcov .arcc{position:relative;width:min(1200px,96vw);max-height:96vh;overflow:auto;background:#fff;border-radius:16px;box-shadow:0 30px 80px rgba(0,0,0,.45)}
.arcov .arcs{position:relative;background:#120e1a;aspect-ratio:16/9;max-height:72vh;width:100%}
.arcov .arcs img,.arcov .arcs iframe{display:block;width:100%;height:100%;border:0}
.arcov .arcp,.arcov .arcn{position:absolute;top:50%;transform:translateY(-50%);width:48px!important;height:48px!important;padding:0!important;display:flex;align-items:center;justify-content:center;border-radius:50%!important;border:0;background:rgba(255,255,255,.92);color:#1b1526;font-size:30px;line-height:1;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.3)}
.arcov .arcp{left:14px}.arcov .arcn{right:14px}
.arcov .arcbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 20px;border-bottom:1px solid #ece8f4}
.arcov .arcbar p{margin:0;font-size:15px;color:#3a3350}
.arcov .arcdots{display:flex;gap:8px;flex:none}
.arcov .arcdots button{width:10px!important;height:10px!important;padding:0!important;border-radius:50%!important;border:0;background:#d6cfe9;cursor:pointer}
.arcov .arcdots button.on{background:#6152a0}
.arcov .arct{padding:16px 20px 20px}
.arcov .arct>b{font-size:22px}
.arcov .arct>p{margin:6px 0 12px;color:#3a3350;line-height:1.5}
.arcov .arcl{display:flex;flex-direction:column;gap:6px}
.arcov .arcl a{color:#5d4fa6;text-decoration:none;font-size:14.5px}
.arcov .arcl a:hover{text-decoration:underline}
.arcov .bovx{position:absolute;top:12px;right:12px;z-index:3;width:40px!important;height:40px!important;border-radius:50%!important;background:rgba(255,255,255,.95)!important}
@media(max-width:700px){.arcov .arcbar{flex-direction:column;align-items:flex-start}.arcov .arcp,.arcov .arcn{width:38px!important;height:38px!important;font-size:24px}}
.invov .invh{display:block;font-size:22px;margin-bottom:8px}
.invov .invl{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:12px;padding:10px 12px;border:1px solid #e3def0;border-radius:10px}
.invov .invl span{flex:1;min-width:0;overflow-wrap:anywhere;font-weight:600}
.invov .invb{margin-top:14px}
.invov .invs{margin:10px 0 0;color:#7a7f90;font-size:14px}
#wath .socc{font-size:14px;font-weight:700;color:#4a4560}
.mov .mnot{margin-top:12px;padding:12px 14px;border-radius:10px;background:#fff4dc;border:1px solid #f0d9a6;display:flex;flex-direction:column;gap:4px;font-size:14.5px;line-height:1.45;color:#3a2f12}
.mov .mnot b{font-size:15.5px;color:#1b1526}
.mov .mwhere{margin:12px 0 0}
.mov .mlad{position:relative;margin:22px 8px 6px;padding-bottom:40px}
.mov .mladt{height:8px;border-radius:999px;background:#e4dff2;overflow:hidden}
.mov .mladt i{display:block;height:100%;background:#6152a0;border-radius:999px}
.mov .mladd{position:absolute;left:0;right:0;top:-3px}
.mov .mladd span{position:absolute;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:2px;font-size:11.5px;color:#7a7f90;white-space:nowrap}
.mov .mladd span::before{content:'';width:14px;height:14px;border-radius:50%;background:#fff;border:2px solid #cfc7e6;box-sizing:border-box;margin-bottom:4px}
.mov .mladd span.on::before{background:#6152a0;border-color:#6152a0}
.mov .mladd span.nx::before{border-color:#6152a0}
.mov .mladd span b{color:#1b1526;font-size:12px}
.mov .mladd span em{display:none;font-style:normal}
.mov .mladd span.nx em{display:block;color:#6152a0;font-weight:700}
.mov .mladd span:first-child{transform:none;align-items:flex-start}
.mov .mladd span:last-child{transform:translateX(-100%);align-items:flex-end}
.mov .mladd span:first-child::before,.mov .mladd span:last-child::before{margin-left:-7px;margin-right:-7px}
.mov .mnext{margin-top:4px}
@media(max-width:560px){.mov .mladd span b{font-size:10.5px}.mov .mladd span:nth-child(even):not(.nx) b{display:none}}
#wath .upbar{margin:14px 0 16px;padding:12px 14px;border-radius:12px;background:#fff;border:1px solid #ebe7f3}
#wath .upbh{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:8px;font-size:14px}
#wath .upbh span{color:#5b6478}
#wath .upbar .bar{height:10px}
#wath .upbar .bar i{background:#6152a0}
#wath .upbar.live .bar i{background:#c99a3e}
#wath .upbar.done .bar i{background:#33697f}
#wath .upt a{color:#5d4fa6;font-weight:600}
#wath .rband{position:relative;overflow:hidden;background:#8d93c6;min-height:clamp(420px,42vw,620px);display:flex;align-items:center}
#wath .rband .rbimg{position:absolute;inset:0;background:center right/cover no-repeat}
#wath .rband .rbimg::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,rgba(35,28,70,.55) 0%,rgba(35,28,70,.25) 38%,rgba(35,28,70,0) 60%)}
#wath .rband .rbw{position:relative;z-index:1;width:100%}
#wath .rband .rbt{max-width:520px;color:#fff;text-shadow:0 2px 18px rgba(27,21,38,.35)}
#wath .rband .rbk{margin:0 0 10px;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#e6e2ff}
#wath .rband h2{margin:0;color:#fff;font-size:clamp(26px,3vw,40px);line-height:1.15}
#wath .rband .rbs{margin:14px 0 0;font-size:clamp(17px,1.6vw,21px);color:#f2f0ff}
#wath .rband .rbb{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px;text-shadow:none}
#wath .rband .rbtr{background:rgba(255,255,255,.92);color:#1b1526;border-color:transparent}
@media(max-width:760px){#wath .rband{display:block;min-height:0;background:#2b2450}#wath .rband .rbimg{position:relative;inset:auto;aspect-ratio:16/10;background-position:72% center}#wath .rband .rbimg::after{display:none}#wath .rband .rbw{padding-top:22px;padding-bottom:28px}#wath .rband .rbt{text-shadow:none}}
#wath .upimg{margin:4px 0 16px}
#wath .upimg img{display:block;max-width:100%;max-height:560px;width:auto;margin:0 auto;border-radius:12px}
#wath .upimg figcaption{margin-top:8px;text-align:center;font-size:13.5px;color:#5b6478}
#wath .upsh{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:5px;margin-left:12px;padding:5px 10px;border-radius:999px;border:1px solid #e3def0;font-size:13px;font-weight:700;color:#5d4fa6}
#wath .upsh:hover{background:#f4f1fb}
#wath .upsh:focus-visible{outline:2px solid #6152a0;outline-offset:2px}
#wath .up{scroll-margin-top:80px}
#wath #wath-levels .lv .lvi.lvshirt{aspect-ratio:3/4;background-size:cover;background-position:50% 0}
#wath .kband{background:#f6f3ec;border-top:1px solid rgba(27,21,38,.06);border-bottom:1px solid rgba(27,21,38,.06);margin:26px 0 0}
#wath .kband .kbw{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px;padding-top:22px;padding-bottom:22px}
#wath .kbi{display:flex;gap:12px;align-items:flex-start}
#wath .kbic{flex:none;color:#6152a0;margin-top:2px}
#wath .kbi b{display:block;font-size:15.5px;color:#1b1526}
#wath .kbi span span{display:block;font-size:14px;line-height:1.4;color:#5b6478;margin-top:2px}
@media(max-width:900px){#wath .kband .kbw{grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}
@media(max-width:520px){#wath .kband .kbw{grid-template-columns:1fr;gap:14px}}
#wath h2 .h2s{font-weight:500;color:#5b6478;font-size:.62em;letter-spacing:0}
@media(min-width:1100px){#wath .hero>.wrap>h1,#wath .hero>.wrap>h1+.sub{margin-right:calc(clamp(300px,32vw,390px) + 34px);margin-left:0;max-width:none}}
@media(min-width:901px) and (max-width:1099px){#wath .hero>.wrap>h1,#wath .hero>.wrap>h1+.sub{margin-right:calc(39.2% + 13px);margin-left:0;max-width:none}}
#wath .cmtz{all:unset;box-sizing:border-box;cursor:pointer;display:inline-flex;align-items:center;gap:12px;max-width:min(100%,560px);padding:10px 16px 10px 12px;border-radius:999px;background:#fff;border:1px solid #e3def0;box-shadow:0 2px 10px rgba(27,21,38,.05);transition:border-color .15s,box-shadow .15s}
#wath .cmtz:hover{border-color:#c9bff0;box-shadow:0 6px 18px rgba(27,21,38,.09)}
#wath .cmtz:focus-visible{outline:2px solid #6152a0;outline-offset:3px}
#wath .cmta{display:inline-flex;flex:none}
#wath .cmta .av{width:30px;height:30px;font-size:11px;border:2px solid #fff;margin-left:-9px}
#wath .cmta .av:first-child{margin-left:0}
#wath .cmtt{display:flex;flex-direction:column;min-width:0}
#wath .cmtt b{font-size:14px;color:#1b1526}
#wath .cmtt span{font-size:13.5px;color:#5b6478;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#wath .cmtgo{flex:none;color:#6152a0;font-weight:800}
#wath .socx{max-width:680px}
#wath .socr .socn{margin-left:auto}
:is(#wath,#wath-top) .vk .k1{animation-name:wathZoomBg}
:is(#wath,#wath-top) .vk .k4{background-position:center 30%;background-size:cover;background-repeat:no-repeat;transform-origin:50% 74%;animation:wathZoomFg 30s linear infinite}
@keyframes wathZoomBg{0%{transform:scale(1.1);opacity:0}3%{opacity:1}82%{transform:scale(1.9);opacity:1}95%{transform:scale(1.9);opacity:1}100%{transform:scale(1.9);opacity:0}}
@keyframes wathZoomFg{0%{transform:scale(1.1) translateY(0);opacity:0}3%{opacity:1}82%{transform:scale(2.45) translateY(-2.2%);opacity:1}95%{transform:scale(2.45) translateY(-2.2%);opacity:1}100%{transform:scale(2.45) translateY(-2.2%);opacity:0}}
@media(prefers-reduced-motion:reduce){:is(#wath,#wath-top) .vk .k1,:is(#wath,#wath-top) .vk .k4{animation:none!important;transform:scale(1.7)}}
#wath .rband.fband{background:#07060c}
#wath .rband.fband .rbimg{background-position:62% center}
#wath .rband.fband .rbimg::after{background:linear-gradient(90deg,rgba(7,6,12,.85) 0%,rgba(7,6,12,.45) 30%,rgba(7,6,12,0) 50%)}
#wath .rband.fband .rbt{max-width:440px}
@media(max-width:760px){#wath .rband.fband{background:#07060c}#wath .rband.fband .rbimg{background-position:62% center}}
#wath .tndside{align-items:center!important}
#wath .tndside .tndb{display:flex;justify-content:center;width:100%}
@media(min-width:901px){#wath .card.tndd{gap:28px 72px!important;padding:48px 52px 46px!important}#wath .tndt{padding-left:8px}}
#wath .imph{margin:0 0 18px}
.wath-nbdg{display:inline-flex;align-items:center;justify-content:center;min-width:18px;height:18px;padding:0 5px;margin-left:4px;border-radius:999px;background:#6152a0;color:#fff;font-size:11px;font-weight:800;line-height:1;vertical-align:middle}
#wath .upimg.lk{position:relative;overflow:hidden;border-radius:12px;max-width:520px;margin-left:auto;margin-right:auto}
#wath .upimg.lk img{filter:blur(16px) brightness(.75) saturate(.9);transform:scale(1.08);max-height:420px;width:100%;object-fit:cover;border-radius:0}
#wath .upimg.lk .lkv{position:absolute;inset:0;margin:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:#fff;text-align:center;padding:20px;font-size:15px}
#wath .upimg.lk .lkv b{display:inline-flex;align-items:center;gap:6px;font-size:18px}
#wath .upt.uplk:has(.upimg.lk){max-height:none!important;-webkit-mask-image:none!important;mask-image:none!important;overflow:visible!important}
#wath .upt.uplk:has(.upimg.lk)::after{display:none!important}
#wath .upimg.lk img{max-height:320px}
#wath .tmc .tmi{width:84px;height:84px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;background:#e4dff2;color:#5a4f8f;font-size:24px;font-weight:800;margin-bottom:8px;flex:none}
#wath .msd ul{background:#efeaf9;border-radius:10px;padding:10px 14px 10px 30px!important;margin:6px 0 12px 30px!important}
#wath .msd.ms-now{border:2px solid #6152a0!important;border-radius:14px;background:#f6f3fd;padding:10px 14px 6px;margin:12px 0}
#wath .msd.ms-now>summary{margin:0 -6px}
#wath .msd.ms-now ul{background:#e7e0f8}
#wath .msd.ms-next{border:1.5px dashed #b9addf!important;border-radius:14px;padding:10px 14px 6px;margin:12px 0}
#wath .msd.ms-next>summary{margin:0 -6px}
#wath .mstag{display:inline-block;margin:2px 0 2px;padding:3px 9px;border-radius:999px;background:#6152a0;color:#fff;font-size:11px;font-weight:800;letter-spacing:.1em}
#wath .mstag.nx{background:#ece7fa;color:#5d4fa6}
#wath .msbar{margin:4px 0 8px 30px}
#wath .msbar .bar{display:block;height:10px}
#wath .msbar .bar i{background:#6152a0}
#wath .msbl{display:block;margin-top:5px;font-size:13.5px;color:#5b6478}
#wath .msd.msflash{animation:wathMsFlash 1.6s ease}
@keyframes wathMsFlash{0%,100%{box-shadow:0 0 0 0 rgba(97,82,160,0)}25%{box-shadow:0 0 0 6px rgba(97,82,160,.25)}}
@media(max-width:520px){#wath .msbar,#wath .msd ul{margin-left:0!important}}
#wath .msd.ms-now>summary,#wath .msd.ms-next>summary{flex-wrap:wrap;row-gap:4px}
#wath .msd>summary .mstagw{flex:0 0 100%;display:block;line-height:1}
#wath .msd>summary .msbar{flex-basis:100%;margin:4px 0 2px 30px}
#wath .msd.ms-now>summary{background:transparent!important}
.pfd{border:1px solid #e3def0;border-radius:12px;margin:10px 0;background:#fff}.pfd>summary .apill{flex:none;white-space:nowrap}.pfd>summary{list-style:none;display:flex;align-items:center;gap:12px;padding:14px 16px;cursor:pointer}.pfd>summary::-webkit-details-marker{display:none}.pfd[open]>summary{border-bottom:1px solid #eee9f7}.pft{flex:1;min-width:0}.pft b{display:block;font-size:15px;color:#1b1526}.pft span{display:block;font-size:13px;color:#5b6478;margin-top:2px}.pfb{padding:14px 16px 16px;background:#faf8fe;border-radius:0 0 12px 12px}.pfg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 14px;margin:6px 0}.pfg{align-items:end}#wath-top .pfg .mf{margin:0}#wath-top .pfg .mf select{width:100%;box-sizing:border-box;border:1px solid #cfc8e6;border-radius:10px;padding:10px 12px;font-family:inherit;font-size:15.5px;background:#fff;color:#1b1526;height:44px}.pfg .mf input,.pfg .mf select,.pfg .mf textarea{width:100%;box-sizing:border-box}.pfh{display:block;font-size:13px;color:#1b1526;margin:10px 0 2px}.pfn{display:block;font-size:12.5px;color:#5b6478;margin:8px 0 0;font-style:normal}.pfbar{margin-top:12px}.pfat{font-size:12.5px;color:#4a7a3a;margin:0 0 8px}.pfaddr{margin-top:6px}.pfpv{font-size:12px;color:#5b6478;display:flex;gap:8px;flex-wrap:wrap;align-items:center}.pfpv .mlink.on{font-weight:800;text-decoration:underline}.pfauto{margin-top:12px}@media(max-width:560px){.pfg{grid-template-columns:1fr}.pfg .mf[style*=span]{grid-column:auto!important}}:is(#wath,#wath-top) .hero-grid>div .shr{display:flex!important;border:0;margin-top:16px;padding:0;gap:8px 14px;justify-content:center;flex-wrap:wrap}:is(#wath,#wath-top) .hero-grid>div .shr .shl{width:auto}#wath .subnav .snshr{display:none!important}:is(#wath,#wath-top) .subnav .wrap{border-bottom:0}:is(#wath,#wath-top) .subnav{border-bottom:1px solid rgba(27,21,38,.16)}#wath .kband{margin-bottom:22px}#wath .subnav .snr{overflow:hidden;align-self:stretch;display:flex;align-items:center;margin:-5px 0 -6px;padding:5px 0 6px}#wath .subnav .snr .btn[data-give]{opacity:1;visibility:hidden;transform:translateY(160%);transition:transform .3s ease-in,visibility 0s linear .3s}#wath.sngive .subnav .snr .btn[data-give]{opacity:1;visibility:visible;transform:none;transition:transform .45s cubic-bezier(.2,.9,.3,1.2),visibility 0s}#wath .chs{display:block!important}#wath .chsum{margin:0 0 12px;color:#5b6478;font-size:14.5px}#wath .chsum b{color:#1b1526}#wath .chw{border:1px solid #e3def0;border-radius:14px;background:#fff;margin:0 0 12px;overflow:hidden}#wath .chw.live{background:#fffaf0;border-color:#ecd9a8}#wath .chx{display:block;width:100%;text-align:left;background:none;border:0;padding:14px 16px 13px;cursor:pointer;font-family:inherit;color:inherit}#wath .chtop{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}#wath .chtop .tag{font-size:11.5px;font-weight:800;letter-spacing:.1em;flex:0 0 100%;margin-bottom:2px}#wath .chn2{font-size:17px;color:#1b1526;flex:1;min-width:0}#wath .chn2 span{font-weight:600;color:#5b6478;font-size:14.5px;margin-left:6px}#wath .chtop .chev{flex:none;color:#6152a0;transition:transform .2s;align-self:center}#wath .chx[aria-expanded=true] .chev{transform:rotate(180deg)}#wath .chrow{display:flex;align-items:center;gap:10px;margin:10px 0 6px}#wath .chi{width:30px;height:30px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;flex:none}#wath .chb{flex:1;height:10px;margin:0}#wath .chb i{display:block;height:100%;border-radius:inherit}#wath .chl2{display:block;font-size:14px;color:#5b6478;padding-left:40px}#wath .chl2 b{color:#1b1526}#wath .chd{padding:0 16px 14px 56px}#wath .chdh{display:block;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#5b6478;margin:2px 0 6px}#wath .chp{list-style:none;margin:0;padding:0;max-height:260px;overflow:auto}#wath .chp li{display:grid;grid-template-columns:1fr auto 110px;gap:10px;padding:7px 0;border-top:1px solid #f0edf6;font-size:14px}#wath .chp li b{color:#1b1526}#wath .chp li em{font-style:normal;color:#8a84a0;text-align:right;font-size:13px}#wath .chno{font-size:14px;color:#5b6478;margin:0}#wath .chd .cha{display:flex;gap:14px;align-items:center;margin-top:12px}#wath .chstart{display:flex;gap:16px;align-items:center;justify-content:space-between;border:1px dashed #b9b0d6;border-radius:14px;padding:14px 16px;background:#f6f3fd}#wath .chstart b{display:block;font-size:16px;color:#1b1526}#wath .chstart span{display:block;font-size:13.5px;color:#5b6478;margin-top:3px}#wath .chstart .btn{flex:none}@media(max-width:560px){#wath .chstart{flex-direction:column;align-items:stretch}#wath .chd{padding-left:16px}#wath .chp li{grid-template-columns:1fr auto}#wath .chp li em{display:none}}@media(min-width:761px){#wath .rband .rbimg{inset:-14% 0;will-change:transform}}#wath a.btn{text-decoration:none!important}:is(#wath,#wath-top) .bgp{position:fixed;left:16px;bottom:16px;z-index:44;display:inline-flex;align-items:center;gap:6px;background:#1b1526;color:#fff;border:0;border-radius:999px;padding:7px 13px;font-size:12.5px;font-weight:700;font-family:inherit;box-shadow:0 6px 18px rgba(27,21,38,.25);cursor:pointer;opacity:.9}:is(#wath,#wath-top) .bgp:hover{opacity:1}:is(#wath,#wath-top) .pvb{bottom:58px}@media(max-width:900px){:is(#wath,#wath-top) .bgp{bottom:88px;left:10px;padding:6px 11px;font-size:12px}}html.wath-framed :is(#wath,#wath-top) .bgp,html.wath-noscroll :is(#wath,#wath-top) .bgp{display:none}#wath .crew{margin:14px 0 10px}#wath .crew>summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:6px;font-weight:700;color:#6152a0}#wath .crew>summary::-webkit-details-marker{display:none}#wath .crew[open]>summary .chev{transform:rotate(180deg)}#wath .crew5{margin-top:12px;grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}@media(min-width:901px){#wath .crew5{grid-template-columns:repeat(6,minmax(0,1fr))}}#wath-top .mbeta{display:inline-block;margin-left:8px;font-size:10.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;background:#f3c64e;color:#2c2208;border-radius:999px;padding:3px 8px;vertical-align:middle}#wath-top .mslab.ms2{border-top:1px solid #ebe7f5;margin-top:8px;padding-top:14px}#wath .mxd .mxgh{display:block;font-size:11.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#7a5c14;margin:14px 0 4px}#wath .mxd .mxr{display:block;padding:0;border:0;margin:0 0 6px;background:rgba(255,255,255,.7);border-radius:10px}#wath .mxd .mxrb{display:block;width:100%;text-align:left;background:none;border:0;padding:10px 12px;cursor:pointer;font-family:inherit;color:inherit}#wath .mxd .mxrt{display:flex;align-items:center;gap:8px}#wath .mxd .mxrt b{flex:1;min-width:0;font-size:15px;color:#2c2208}#wath .mxd .mxrt .mxa{font-weight:700;color:#5b4a1e;font-size:14px}#wath .mxd .mxrt .chev{flex:none;color:#7a5c14;transition:transform .2s}#wath .mxd .mxrb[aria-expanded=true] .chev{transform:rotate(180deg)}#wath .mxd .mxr .bar{display:block;height:7px;margin:7px 0 5px}#wath .mxd .mxr .bar i{display:block;height:100%;border-radius:inherit}#wath .mxd .mxa2{display:block;font-size:13px;color:#6b5a2e}#wath .mxd .mxp{padding:0 12px 10px}#wath .mxd .mxp ul{list-style:none;margin:0;padding:0;max-height:220px;overflow:auto}#wath .mxd .mxp li{display:grid;grid-template-columns:1fr auto 86px;gap:8px;font-size:13px;padding:5px 0;border-top:1px solid rgba(122,92,20,.15)}#wath .mxd .mxp li em{font-style:normal;color:#8a7a50;text-align:right;font-size:12px}#wath .mxd .mxp p{font-size:13px;margin:6px 0 0;color:#6b5a2e}#wath .lvshirt{position:relative}#wath .lvshirt .lvcap{position:absolute;left:0;right:0;bottom:0;padding:26px 14px 12px;background:linear-gradient(180deg,rgba(17,14,24,0) 0%,rgba(17,14,24,.78) 70%);color:#fff;font-weight:800;font-size:17px;line-height:1.2;text-align:center;letter-spacing:.01em}#wath .chsec{margin:0 0 6px}#wath .chsh{display:block;font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#5b6478;margin:16px 0 8px}#wath .chsec.a .chsh{color:#7a5c14}#wath .chsec.n .chsh{color:#6152a0}#wath .chsec.d{border-top:2px solid #d9d3ec;margin-top:18px;padding-top:4px}#wath .chsec.d .chsh{color:#33697f}#wath .chw.next{background:#f8f6fe}#wath .chw.done{background:#fff}#wath .chn2{font-size:18.5px!important;font-weight:800;line-height:1.25}#wath .chrow{gap:0!important;position:relative}#wath .chi2{position:relative;width:58px;height:34px;flex:none;z-index:1}#wath .chi2 .chi{position:absolute;top:0;width:34px!important;height:34px!important;border-radius:50%;display:flex;align-items:center;justify-content:center;background:color-mix(in srgb,var(--cc) 28%,#fff);color:color-mix(in srgb,var(--cc) 75%,#000);box-shadow:0 0 0 3px #fff}#wath .chi2 .g1{left:0}#wath .chi2 .g2{left:24px}#wath .chw.live .chi2 .chi{box-shadow:0 0 0 3px #fffaf0}#wath .chw.next .chi2 .chi{box-shadow:0 0 0 3px #f8f6fe}#wath .chrow .chb{margin-left:-8px!important;height:10px;background:color-mix(in srgb,var(--cc) 16%,#fff)}#wath .chrow .chb i{background:var(--cc)!important}#wath .chl2{padding-left:58px!important}#wath .chd{padding-left:74px!important}@media(max-width:560px){#wath .chd{padding-left:16px!important}#wath .chl2{padding-left:0!important}}#wath a.chbig{display:flex;width:100%;box-sizing:border-box;justify-content:center;align-items:center;min-height:58px;font-size:18px;margin-top:16px;border-radius:12px}#wath .chbn{text-align:center;font-size:13px;color:#5b6478;margin:8px 0 0}#wath .subnav .snr .btn[data-give]{min-width:190px!important;padding:0 26px;font-size:15.5px}@media(min-width:901px) and (max-width:1240px){#wath .subnav .snr .btn[data-give]{min-width:150px!important;padding:0 18px}}@media(min-width:701px){:is(#wath,#wath-top) .pvb{bottom:16px;width:156px;justify-content:center;box-sizing:border-box}:is(#wath,#wath-top) .bgp{bottom:64px;width:156px;justify-content:center;box-sizing:border-box;padding:10px 16px;font-size:14px}}#wath-top .bovi,#wath .bovi,.bov .bovi{width:76px;height:76px;border-radius:50%;background:#d9d3ec;color:#6152a0;font-weight:800;font-size:28px;display:flex;align-items:center;justify-content:center;flex:none}:is(#wath,#wath-top) .bovh .bovi{display:flex!important;align-items:center;justify-content:center;width:76px;height:76px;border-radius:50%;background:#d9d3ec;color:#6152a0!important;font-weight:800;font-size:26px!important;letter-spacing:0!important;text-transform:none!important;flex:none;margin:0!important}#wath .chp li b small,#wath .mxp li b small{display:block;font-weight:500;font-size:11.5px;color:#8a84a0}:is(#wath,#wath-top) .gco{position:fixed;inset:0;z-index:2147483000;background:rgba(27,21,38,.55);overflow:auto;padding:24px 12px;display:flex;justify-content:center;align-items:flex-start}:is(#wath,#wath-top) .gcoc{position:relative;background:#fff;border-radius:16px;max-width:620px;width:100%;padding:0 24px 22px;box-shadow:0 20px 60px rgba(27,21,38,.35);color:#1b1526;font-size:15px}:is(#wath,#wath-top) .gcob{margin:0 -24px 16px;padding:12px 56px 12px 24px;background:#f3c64e;color:#2c2208;border-radius:16px 16px 0 0;font-size:14px;line-height:1.35}:is(#wath,#wath-top) .gcob b{letter-spacing:.08em;margin-right:6px}:is(#wath,#wath-top) .gcox{position:absolute;right:12px;top:8px;background:none;border:0;font-size:28px;line-height:1;color:#2c2208;cursor:pointer}:is(#wath,#wath-top) .gcos{display:flex;gap:14px;font-size:12.5px;font-weight:700;color:#9a93b3;margin-bottom:10px}:is(#wath,#wath-top) .gcos .on{color:#6152a0}:is(#wath,#wath-top) .gcos .dn{color:#33697f}:is(#wath,#wath-top) .gcoc h3{margin:4px 0 10px;font-size:22px}:is(#wath,#wath-top) .gcon{color:#4a4560;line-height:1.5;margin:10px 0}:is(#wath,#wath-top) .gcoa{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}:is(#wath,#wath-top) .gcoa button{border:1px solid #cfc8e6;background:#fff;border-radius:10px;padding:12px;font-weight:800;font-size:16px;cursor:pointer;font-family:inherit}:is(#wath,#wath-top) .gcoa button.on{background:#6152a0;color:#fff;border-color:#6152a0}:is(#wath,#wath-top) .gcol{display:block;margin-top:12px;font-weight:700;font-size:13.5px}:is(#wath,#wath-top) .gcoi{display:flex;align-items:center;gap:6px;border:1px solid #cfc8e6;border-radius:10px;padding:0 12px;margin-top:6px;font-size:18px}:is(#wath,#wath-top) .gcoi input{border:0;outline:0;font-size:18px;padding:10px 0;width:100%;font-family:inherit}:is(#wath,#wath-top) .gcof{display:flex;justify-content:space-between;gap:10px;margin-top:18px}:is(#wath,#wath-top) .gcof .btn[disabled]{opacity:.45;cursor:not-allowed}:is(#wath,#wath-top) .gcop{border:1px solid #e3def0;border-radius:12px;padding:14px 16px;margin:12px 0}:is(#wath,#wath-top) .gcop.y{border-color:#6152a0;background:#f8f6fe}:is(#wath,#wath-top) .gcoph b{display:block;font-size:17px}:is(#wath,#wath-top) .gcoph span{display:block;font-size:13px;color:#6152a0;font-weight:700;margin-top:2px}:is(#wath,#wath-top) .gcop p{margin:8px 0;color:#4a4560;line-height:1.45}:is(#wath,#wath-top) .gcop ul{margin:6px 0 8px;padding-left:18px;color:#4a4560;font-size:14px;line-height:1.45}:is(#wath,#wath-top) .gcoq{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:8px}:is(#wath,#wath-top) .gcoq span{font-weight:800;margin-right:4px}:is(#wath,#wath-top) .gcoq button{border:1px solid #cfc8e6;background:#fff;border-radius:999px;padding:8px 14px;font-weight:700;cursor:pointer;font-family:inherit}:is(#wath,#wath-top) .gcoq button.on{background:#6152a0;color:#fff;border-color:#6152a0}:is(#wath,#wath-top) .gcock{display:flex;gap:10px;align-items:flex-start;margin-top:10px;font-size:14px;line-height:1.4}:is(#wath,#wath-top) .gcock input{margin-top:3px;width:18px;height:18px;flex:none}:is(#wath,#wath-top) .gcoout{color:#8a3b2a!important}:is(#wath,#wath-top) .gcor>div{display:flex;justify-content:space-between;gap:16px;padding:9px 0;border-bottom:1px solid #eee9f7}:is(#wath,#wath-top) .gcor span{color:#5b6478}:is(#wath,#wath-top) .gcor b{text-align:right}:is(#wath,#wath-top) .gcor .tot b{font-size:19px;color:#33697f}@media(max-width:560px){:is(#wath,#wath-top) .gcoc{padding:0 16px 18px}:is(#wath,#wath-top) .gcob{margin:0 -16px 14px;padding-left:16px}:is(#wath,#wath-top) .gcoa{grid-template-columns:repeat(2,1fr)}}@media(min-width:761px){#wath .rband.fband .rbt{margin-left:auto}#wath .rband.fband .rbimg{background-position:22% center}#wath .rband.fband .rbimg::after{background:linear-gradient(270deg,rgba(7,6,12,.88) 0%,rgba(7,6,12,.5) 32%,rgba(7,6,12,0) 55%)}}:is(#wath,#wath-top) .gcos span{display:inline-block!important;border:0!important;padding:0!important;margin:0!important;line-height:1.3!important;font-size:12.5px!important}:is(#wath,#wath-top) .gcoinc{background:#f6f3fd;border-radius:12px;padding:12px 16px;margin:12px 0;font-size:14px}:is(#wath,#wath-top) .gcoinc ul{margin:6px 0 0;padding-left:18px;color:#4a4560;line-height:1.45}:is(#wath,#wath-top) .video .vt .play.pq{width:clamp(84px,13.5cqw,128px)!important;height:clamp(52px,8.4cqw,80px)!important;border-radius:12px}:is(#wath,#wath-top) .video .vt .play.pq svg{width:30%!important;height:auto!important;margin-left:4%;transform:scale(1.35)}#wath #wath-levels .crh{display:block;border-radius:12px;padding:12px 16px;margin:4px 0 10px}#wath #wath-levels .crh b{display:block;font-size:13px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}#wath #wath-levels .crh span{display:block;font-size:13.5px;margin-top:2px;opacity:.9}#wath #wath-levels .crh.on{background:#e9e4f7;color:#3d3270}#wath #wath-levels .crh.film{background:#1b1526;color:#fff}#wath #wath-levels .crh.film span{color:#e6e2ff}#wath #wath-levels .crline{display:block;margin:30px 0 18px;text-align:center}#wath #wath-levels .crline .up,#wath #wath-levels .crline .dn{display:block;font-size:12.5px;font-weight:700;color:#6152a0}#wath #wath-levels .crline .ln{display:flex;align-items:center;gap:12px;margin:10px 0}#wath #wath-levels .crline .ln:before,#wath #wath-levels .crline .ln:after{content:'';flex:1;height:3px;background:#1b1526;border-radius:2px}#wath #wath-levels .crline em{font-style:normal;font-size:12px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;color:#1b1526;border:2px solid #1b1526;border-radius:999px;padding:5px 12px;white-space:nowrap}#wath .supn{font-size:15px;font-weight:700;color:#5b6478;margin-left:10px;letter-spacing:0;white-space:nowrap}#wath .hero-grid>.shr.shr{display:flex!important;border:0;padding:0;margin-top:14px;gap:8px 14px;align-self:start;justify-content:center;flex-wrap:wrap}@media(min-width:901px){#wath .hero-grid>div:not(.shr){grid-row:1!important}#wath .hero-grid>.shr.shr{grid-column:2;grid-row:2;justify-content:center}#wath .hero-grid>div:not(.shr)>.btn.big[data-give]{margin-top:auto}#wath .hm{display:none}}@media(max-width:900px){#wath .hd{display:none}#wath .hero-grid>.shr.shr{justify-content:center;margin-top:16px}}#wath .hd .hraise{display:block;font-size:42px;color:#33697f;line-height:1;font-weight:800}#wath .hd .hsub2{display:block;font-size:16px;color:#1f2430;font-weight:600;margin:4px 0 12px}#wath .hd .bar{margin:0}#wath .hd .hsub3{display:block;font-size:13.5px;color:#5b6478;margin-top:6px}#wath .hd .hst{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0 6px}#wath .hd .hst b{display:block;font-size:34px;line-height:1;font-weight:800;color:#1b1526}#wath .hd .hst span{display:block;font-size:14px;color:#5b6478;margin-top:4px}#wath .kband{background:#f1e9ec!important;border-color:rgba(120,96,128,.16)!important}#wath .kband .kbic{color:#7d6a8a}#wath .btn.cmt0{min-height:38px;padding:0 18px;font-size:14.5px}#wath .cmn.cmm{display:block;background:#f6f3fd;border-radius:12px;padding:14px 16px}#wath .cmn.cmm b{display:block;font-size:15.5px;color:#1b1526}#wath .cmn.cmm span{display:block;font-size:14px;color:#4a4560;margin-top:4px;line-height:1.45}#wath .cmmb{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}#wath .cmmb .btn{min-height:40px;text-decoration:none}#wath .socr{display:flex!important;justify-content:space-between;align-items:center;width:100%}#wath .cmn.cmm{padding:18px 20px;margin-top:12px;max-width:680px;box-sizing:border-box}#wath .cmmb .btn{display:inline-flex;align-items:center;justify-content:center;padding:0 18px;font-size:14.5px;line-height:1}:is(#wath,#wath-top) .bovf{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px;padding-top:14px;border-top:1px solid #eee9f7}:is(#wath,#wath-top) .bovf a{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-weight:700;font-size:14px;border-radius:999px;padding:9px 16px;border:1px solid #cfc8e6;color:#1b1526;background:#fff}:is(#wath,#wath-top) .bovf a.pri{background:#6152a0;border-color:#6152a0;color:#fff}:is(#wath,#wath-top) .bovf a:hover{filter:brightness(.97)}:is(#wath,#wath-top) .video .vk .kplay{position:absolute;left:50%;top:43%;transform:translate(-50%,-50%);display:flex;align-items:center;justify-content:center;width:clamp(84px,13.5cqw,128px);height:clamp(52px,8.4cqw,80px);border-radius:12px;background:#6152a0;box-shadow:0 10px 28px rgba(27,21,38,.35);transition:transform .15s,background .15s;opacity:0;animation:wathFade .8s ease 1.1s forwards}:is(#wath,#wath-top) .video .vk .kplay svg{width:30%;height:auto;margin-left:4%;transform:scale(1.35)}:is(#wath,#wath-top) .video:hover .vk .kplay{background:#54479a;transform:translate(-50%,-50%) scale(1.04)}:is(#wath,#wath-top) .video .vk .k4{z-index:2!important}:is(#wath,#wath-top) .video .vk .kplay{z-index:1!important}:is(#wath,#wath-top) .video .vt .vsub{display:flex;flex-direction:column;align-items:center;gap:1.1cqw;font-style:normal;font-size:2.3cqw;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#fff;margin:.4cqw 0 0}:is(#wath,#wath-top) .video .vt .vsub .vln{display:block;width:0;height:2px;background:#fff;border-radius:2px;opacity:.9;animation:wathLn .7s cubic-bezier(.2,.7,.2,1) 1s forwards}@keyframes wathLn{to{width:6cqw}}:is(#wath,#wath-top) .video .vt .vcrow{display:flex;gap:7cqw;justify-content:center;margin-top:1.6cqw}:is(#wath,#wath-top) .video .vt .vc2{display:flex;flex-direction:column;align-items:center;gap:.4cqw;font-size:1.55cqw;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:#e6ebff;white-space:nowrap}:is(#wath,#wath-top) .video .vt .vc2 strong{font-size:2.1cqw;font-weight:800;letter-spacing:.08em;color:#fff}@media(max-width:700px){:is(#wath,#wath-top) .video .vt .vc2{font-size:2.1cqw}:is(#wath,#wath-top) .video .vt .vc2 strong{font-size:2.7cqw}:is(#wath,#wath-top) .video .vt .vsub{font-size:2.8cqw}}@media(prefers-reduced-motion:reduce){:is(#wath,#wath-top) .video .vk .kplay{animation:none;opacity:1}:is(#wath,#wath-top) .video .vt .vsub .vln{animation:none;width:6cqw}}@media(max-width:700px){:is(#wath,#wath-top) .video .vk .kplay{top:46%;width:62px;height:40px;border-radius:10px}:is(#wath,#wath-top) .video .vt .vcrow{margin-top:1cqw}}/*spacing pass Nov 17*/#wath :is(.sec,.tband,#wath-team,#wath-impact,#wath-levels,#wath-updates,#wath-comments,#wath-challenges,#wath-budget,#wath-faq,#wath-recent,#wath-story)>h2:not(.rbt h2){margin-top:0!important;margin-bottom:0!important}#wath :is(.sec,.tband,#wath-team,#wath-impact,#wath-levels,#wath-updates,#wath-comments,#wath-challenges,#wath-budget,#wath-faq,#wath-recent,#wath-story)>h2+:not(.sub){margin-top:2px!important}#wath :is(.sec,.tband,#wath-team,#wath-impact,#wath-levels,#wath-updates,#wath-comments,#wath-challenges,#wath-budget,#wath-faq,#wath-recent,#wath-story)>h2+.sub{margin-top:-8px!important;margin-bottom:0!important}#wath :is(.sec,.tband,#wath-team,#wath-impact,#wath-levels,#wath-updates,#wath-comments,#wath-challenges,#wath-budget,#wath-faq,#wath-recent,#wath-story)>h2+.sub+*{margin-top:2px!important}#wath #wath-team h2+.tm5{margin-top:18px!important}#wath h2+.mwa{margin-top:2px!important}#wath .hero h1+p,#wath .hero .lede{text-wrap:balance}#wath .upimg.lk{max-width:640px!important;min-height:320px;background:#eee}#wath .upimg.lk img{filter:blur(10px) saturate(.9)!important;max-height:380px!important;min-height:320px}#wath .upimg.lk .lkv{background:rgba(250,248,255,.74);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);color:#1b1526!important;gap:10px!important;padding:24px!important}#wath .upimg.lk .lkv .lkb{width:72px;height:72px;border-radius:50%;background:#1b1526;color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(27,21,38,.25);margin-bottom:4px}#wath .upimg.lk .lkv b{font-size:22px!important;color:#1b1526}#wath .upimg.lk .lkv>span:not(.lkb):not(.lka){font-size:15px;color:#4a4560;max-width:360px;line-height:1.45}#wath .upimg.lk .lkv .lka{display:flex;gap:8px;margin-top:6px}#wath .upimg.lk .lkv .lka .btn{min-height:42px;padding:0 20px}#wath :is(article,.upd,.upc,li,div):has(> .upt .upimg.lk) > .upgate,#wath :has(> .upt .upimg.lk) .upgate{display:none!important}#wath .upimg.lk .lkpeek{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:blur(5px) saturate(1.05)!important;transform:scale(1.03)!important;max-height:none!important;min-height:0!important;opacity:0;-webkit-mask-image:radial-gradient(circle 90px at var(--mx,50%) var(--my,50%),#000 0,rgba(0,0,0,.6) 45%,transparent 100%);mask-image:radial-gradient(circle 90px at var(--mx,50%) var(--my,50%),#000 0,rgba(0,0,0,.6) 45%,transparent 100%);transition:opacity .35s;animation:wathPeek 2.4s ease-in-out infinite;pointer-events:none}@keyframes wathPeek{0%,100%{filter:blur(5px) saturate(1.05)}50%{filter:blur(7px) saturate(1.1) brightness(1.05)}}#wath .upimg.lk.peeking .lkpeek{opacity:1}#wath .upimg.lk .lkv{background:none!important}#wath .upimg.lk .lkv::before{content:'';position:absolute;inset:0;z-index:-1;background:rgba(250,248,255,.74);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);transition:-webkit-mask-size .3s}#wath .upimg.lk.peeking .lkv::before{-webkit-mask-image:radial-gradient(circle 100px at var(--mx,50%) var(--my,50%),rgba(0,0,0,.25) 0,rgba(0,0,0,.6) 55%,#000 100%);mask-image:radial-gradient(circle 100px at var(--mx,50%) var(--my,50%),rgba(0,0,0,.25) 0,rgba(0,0,0,.6) 55%,#000 100%)}#wath .upimg.lk .lkv{z-index:1;isolation:isolate}#wath .upimg.lk .lkv>*{position:relative}@media(prefers-reduced-motion:reduce){#wath .upimg.lk .lkpeek{animation:none}}#wath .upimg.lk.touch .lkpeek{filter:blur(2.5px)!important;animation:none;-webkit-mask-image:radial-gradient(circle 140px at var(--mx,50%) var(--my,50%),#000 0,rgba(0,0,0,.75) 55%,transparent 100%);mask-image:radial-gradient(circle 140px at var(--mx,50%) var(--my,50%),#000 0,rgba(0,0,0,.75) 55%,transparent 100%)}#wath .upimg.lk.touch.peeking .lkv::before{-webkit-mask-image:radial-gradient(circle 150px at var(--mx,50%) var(--my,50%),rgba(0,0,0,.1) 0,rgba(0,0,0,.5) 55%,#000 100%);mask-image:radial-gradient(circle 150px at var(--mx,50%) var(--my,50%),rgba(0,0,0,.1) 0,rgba(0,0,0,.5) 55%,#000 100%)}:is(#wath,#wath-top) .video .vk .kplay{border:3px solid #fff;box-sizing:border-box}@media(max-width:700px){:is(#wath,#wath-top) .video .vk .kplay{border-width:2px}}:is(#wath,#wath-top) .vk .k1,:is(#wath,#wath-top) .vk .k4{will-change:auto!important}:is(#wath,#wath-top) .video .vk .kplay{top:28cqw!important}@media(max-width:700px){:is(#wath,#wath-top) .video .vk .kplay{top:26cqw!important}}@media(min-width:901px){#wath .hero-grid>.video{max-height:min(660px,70vw)}}:is(#wath,#wath-top) .tovx{border-radius:10px!important;background:#e6e0f7!important;color:#4a3d8f!important;width:46px!important;height:46px!important;font-size:30px!important;font-weight:400;box-shadow:0 6px 18px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;padding:0 0 3px}:is(#wath,#wath-top) .tovx:hover{background:#d6ccf2!important}@font-face{font-family:'WathCinzel';src:url(https://cdn.jsdelivr.net/gh/nirvanmullick/whatatrip-donor-wall@4e04806e3b5654f217362eac77019828d754d7d7/fonts/cinzel-latin-600-normal.woff2) format('woff2');font-weight:600;font-display:swap}:is(#wath,#wath-top) .video .vt .vsub span{font-family:'WathCinzel',Georgia,serif!important;font-weight:600!important;text-transform:none!important;letter-spacing:.08em!important;font-size:2.9cqw!important}@media(max-width:700px){:is(#wath,#wath-top) .video .vt .vsub span{font-size:3.4cqw!important}}@font-face{font-family:'WathCinzelDeco';src:url(https://cdn.jsdelivr.net/gh/nirvanmullick/whatatrip-donor-wall@c95d972216525d2673bbb969d52d7de81214a7d8/fonts/cinzel-decorative-latin-400-normal.woff2) format('woff2');font-weight:400;font-display:swap}@font-face{font-family:'WathCinzelDeco';src:url(https://cdn.jsdelivr.net/gh/nirvanmullick/whatatrip-donor-wall@c95d972216525d2673bbb969d52d7de81214a7d8/fonts/cinzel-decorative-latin-700-normal.woff2) format('woff2');font-weight:700;font-display:swap}:is(#wath,#wath-top) .video .vt .vsub span{font-family:'WathCinzelDeco','WathCinzel',Georgia,serif!important;font-weight:700!important;letter-spacing:.04em!important;font-size:3.3cqw!important}@media(max-width:700px){:is(#wath,#wath-top) .video .vt .vsub span{font-size:3.8cqw!important}}:is(#wath,#wath-top).wdeco .video .vt b{font-family:'WathCinzelDeco',Georgia,serif!important;font-weight:700!important;font-size:8.6cqw!important;letter-spacing:.02em!important;line-height:1!important}@font-face{font-family:'WathRye';src:url(https://cdn.jsdelivr.net/gh/nirvanmullick/whatatrip-donor-wall@8951059a044e3028e0d25cece4682ae989c9c156/fonts/rye-latin-400-normal.woff2) format('woff2');font-display:swap}@font-face{font-family:'WathBevan';src:url(https://cdn.jsdelivr.net/gh/nirvanmullick/whatatrip-donor-wall@8951059a044e3028e0d25cece4682ae989c9c156/fonts/bevan-latin-400-normal.woff2) format('woff2');font-display:swap}:is(#wath,#wath-top).wdeco2 .video .vt b{font-family:'WathRye',Georgia,serif!important;font-weight:400!important;font-size:9.4cqw!important;letter-spacing:.02em!important}@font-face{font-family:'WathGrenze';src:url(https://cdn.jsdelivr.net/gh/nirvanmullick/whatatrip-donor-wall@2dc942b70e1366834f3da1693683cf0c4bca786b/fonts/grenze-latin-800-normal.woff2) format('woff2');font-display:swap}:is(#wath,#wath-top):is(.wdeco4,.wdeco5) .video .vt b{font-family:'WathGrenze',Georgia,serif!important;font-weight:800!important;font-size:11.2cqw!important;letter-spacing:.015em!important;line-height:1!important}:is(#wath,#wath-top).wdeco5 .video .vt b{color:#f4d76a!important;text-shadow:0 2px 0 #3a1f12,0 0 2px #3a1f12,0 6px 22px rgba(27,21,38,.55)!important}:is(#wath,#wath-top).wdeco3 .video .vt b{font-family:'WathBevan',Georgia,serif!important;font-weight:400!important;font-size:9.6cqw!important;letter-spacing:.01em!important}:is(#wath,#wath-top) .video .vt .vsub .vorn{width:34cqw;height:auto;display:block;overflow:visible;filter:drop-shadow(0 1px 6px rgba(27,21,38,.45))}:is(#wath,#wath-top) .video .vt .vsub .vorn path[pathLength]{stroke-dasharray:1;stroke-dashoffset:1;animation:wathOrn 1.4s cubic-bezier(.3,.6,.2,1) 1s forwards}:is(#wath,#wath-top) .video .vt .vsub .vorn path:not([pathLength]){opacity:0;transform-origin:120px 12px;animation:wathFade .6s ease 1s forwards}@keyframes wathOrn{to{stroke-dashoffset:0}}@media(prefers-reduced-motion:reduce){:is(#wath,#wath-top) .video .vt .vsub .vorn path{animation:none!important;stroke-dashoffset:0;opacity:1}}@media(max-width:700px){:is(#wath,#wath-top) .video .vt .vsub .vorn{width:30cqw}}#wath .upimg.lk img.lkpeek{filter:none!important;animation:none!important;transform:none!important;-webkit-mask-image:radial-gradient(circle 85px at var(--mx,50%) var(--my,50%),#000 0,#000 60%,transparent 100%)!important;mask-image:radial-gradient(circle 85px at var(--mx,50%) var(--my,50%),#000 0,#000 60%,transparent 100%)!important}#wath .upimg.lk.touch .lkpeek{-webkit-mask-image:radial-gradient(circle 130px at var(--mx,50%) var(--my,50%),#000 0,#000 65%,transparent 100%)!important;mask-image:radial-gradient(circle 130px at var(--mx,50%) var(--my,50%),#000 0,#000 65%,transparent 100%)!important}#wath .upimg.lk.peeking .lkv::before{-webkit-mask-image:radial-gradient(circle 90px at var(--mx,50%) var(--my,50%),transparent 0,transparent 60%,#000 100%)!important;mask-image:radial-gradient(circle 90px at var(--mx,50%) var(--my,50%),transparent 0,transparent 60%,#000 100%)!important}#wath .upimg.lk.touch.peeking .lkv::before{-webkit-mask-image:radial-gradient(circle 140px at var(--mx,50%) var(--my,50%),transparent 0,transparent 65%,#000 100%)!important;mask-image:radial-gradient(circle 140px at var(--mx,50%) var(--my,50%),transparent 0,transparent 65%,#000 100%)!important}#wath .upimg.lk .lkv{-webkit-backdrop-filter:none!important;backdrop-filter:none!important}#wath .upimg.lk .lkink{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:3}#wath .upimg.lk img.lkpeek{filter:url(#wathInk)!important}#wath .upimg.lk .lkv{z-index:2!important}@media(min-width:901px){#wath .subnav .snl a.snm{display:none!important}}:is(#wath,#wath-top).mpre .mcta .mctat{display:none}:is(#wath,#wath-top).mpre .mcta{background:transparent!important;border-top-color:transparent!important;box-shadow:none!important}:is(#wath,#wath-top).min .mcta{transform:translateY(110%);opacity:0;pointer-events:none}:is(#wath,#wath-top).mrise .mcta{animation:wmrise .45s cubic-bezier(.2,.8,.2,1) both}@keyframes wmrise{from{transform:translateY(100%)}to{transform:none}}#wath .upimg img[src*="rick-arcturus-1970s"]{object-position:50% 18%!important}html.wath-hmerge #header{transition:background-color .2s;z-index:60!important;pointer-events:none}html.wath-hmerge #header a,html.wath-hmerge #header button,html.wath-hmerge #header .header-burger,html.wath-hmerge #header .header-menu{pointer-events:auto}html.wath-hmerge.wath-htop #header{background:transparent!important;box-shadow:none!important;border:0!important}html.wath-hmerge.wath-htop body:not(.header--menu-open) #header .header-title{visibility:hidden}html.wath-hmerge #wath:not(.wdeco):not(.wdeco2):not(.wdeco3):not(.wdeco4):not(.wdeco5) .hero .video .vt b{font-size:8.6cqw!important}html.wath-hmerge #wath:is(.wdeco4,.wdeco5) .hero .video .vt b{font-size:10cqw!important}#wath .upflw{display:flow-root}#wath .upflw .upclr{display:block;clear:both}#wath .upflw>.upimg.upfl{float:right;width:36%;max-width:280px;margin:4px 0 14px 28px}#wath .upa.upam{display:none}#wath .upflw>.upimg.upfl img{width:100%;max-height:none;border-radius:10px}#wath .upflw>.upimg.upfl figcaption{text-align:left;font-size:12.5px;line-height:1.4;margin-top:6px}#wath .upflw>h3{margin-top:0}#wath .upflw .upt{display:block}@media(max-width:600px){#wath .upa.upam{display:flex}#wath .upflw>.upa{display:none}#wath .upflw>.upimg.upfl{width:44%;margin:2px 0 10px 14px}#wath .upflw>.upimg.upfl figcaption{font-size:11.5px}}@media(max-width:900px){#wath .hero div:has(>.kstats){display:flex;flex-direction:column}#wath .hero div:has(>.kstats)>div:has(>.hm){display:contents!important}#wath .hero .hm{order:1}#wath .hero .kstats{order:2}#wath .hero .nm{order:3}#wath .hero div:has(>.kstats)>.match{order:4}#wath .hero div:has(>.kstats)>.btn.big{order:5}#wath .cols:not(.second)>.stack{display:contents}#wath .cols:not(.second)>.stack>*{order:3}#wath .cols:not(.second)>.stack>#wath-story{order:1}#wath .cols:not(.second)>#wath-levels{order:2}}#wath .video:not(.playing) .vk .kplay{filter:brightness(.793) saturate(.9)}@media(max-width:767px){#wath-top .bgp[data-bugpill]{display:none!important}}#header .wath-hlog{display:none}@media(max-width:767px){#header .header-display-mobile .wath-hlog{display:inline-flex;align-items:center;align-self:center;margin:0 10px 0 auto;padding:7px 12px;border:1.5px solid rgba(255,255,255,.75);border-radius:999px;color:#fff;font:600 15px/1 'Source Sans 3','Source Sans Pro',system-ui,sans-serif;text-decoration:none;white-space:nowrap}#header .wath-hlog .wath-chip{gap:0}#header .wath-hlog .wath-chip>span:not(.wath-chip-av){display:none}#header .wath-hlog:has(.wath-chip){padding:0;border:0}#header .wath-hlog .wath-chip-av{width:34px;height:34px;border:2px solid rgba(255,255,255,.85)}}#wath .kband .kbw{gap:28px 40px}#wath .kband .kbi{display:flex;align-items:flex-start;gap:16px;max-width:270px}#wath .kband .kbi p{margin:0;font-size:16.5px;line-height:1.45;color:#3a3245}#wath .kband .kbi p b{color:#1b1526;font-weight:700;display:inline!important;font-size:inherit}#wath .kband .kbic{position:relative;flex:none;width:60px;height:60px;display:flex;align-items:center;justify-content:center;background:none!important;color:#1b1526}#wath .kband .kbic .kbb{position:absolute;inset:-6px;width:calc(100% + 12px);height:calc(100% + 12px)}#wath .kband .kbic>svg:not(.kbb){position:relative;transform:translate(3px,-2px)}:is(#wath,#wath-top) .shr .shl{display:none}#wath .remb{display:inline-flex;align-items:center;justify-content:center;gap:6px;width:auto;margin:0;height:38px;padding:0 14px;border-radius:999px;font-size:14px!important;white-space:nowrap;flex:none;border:1.5px solid #d9d1ec;background:#fff;color:#1b1526;font:700 15.5px/1 inherit;cursor:pointer}#wath .remb:hover{border-color:#6152a0;color:#6152a0}#wath .remb svg{flex:none}:is(#wath,#wath-top) .embx textarea{width:100%;min-height:110px;font:12.5px/1.45 ui-monospace,Menlo,monospace;border:1px solid #ddd6ee;border-radius:10px;padding:10px;resize:vertical;box-sizing:border-box}:is(#wath,#wath-top) .embx .embl{display:flex;gap:8px;align-items:center}:is(#wath,#wath-top) .embx .embl input{flex:1;min-width:0;font:15px inherit;border:1px solid #ddd6ee;border-radius:10px;padding:10px 12px}:is(#wath,#wath-top) .embx h4{margin:18px 0 8px;font-size:15px}:is(#wath,#wath-top) .embx .invh{display:block;font-size:20px}:is(#wath,#wath-top) .embx .embp a{width:100%}:is(#wath,#wath-top) .embx .embp{margin:14px 0 4px;border:1px dashed #d9d1ec;border-radius:12px;padding:12px;display:flex;justify-content:center}:is(#wath,#wath-top) .shr{flex-wrap:wrap}:is(#wath,#wath-top) .snshr .remb{display:none!important}#wath .remb .remi,#wath.wmin .remb .remu{display:none}#wath.wmin .remb .remi{display:inline}#wath.wmin .remb svg path:first-child{fill:currentColor}.mov .mnot .mnb{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}#wath .hero .shr{gap:10px;align-items:center;justify-content:center}#wath .hero .shr .shb{gap:6px}#wath .hero .shr{flex-wrap:nowrap}#wath .hero .shr .sh1{width:36px;height:36px}#wath .hero .shr .remb{height:36px}@media(max-width:480px){#wath .hero .shr .sh1{width:33px;height:33px}#wath .hero .shr .remb{height:33px;padding:0 10px;font-size:13px!important}#wath .hero .shr{gap:6px}#wath .hero .shr .shb{gap:4px}}#wath .kband .kbic .kbb{overflow:visible}#wath .kband .kbic>svg:not(.kbb){transform:none}#header .wath-hlogo,.wath-chip-av,#wath-top .mav,#wath-top .mlogo img,:is(#wath,#wath-top) .av,:is(#wath,#wath-top) .bovh img,:is(#wath,#wath-top) .tmp,#wath .tmc .tmi,:is(#wath,#wath-top) .tndby img{border-radius:0!important;clip-path:polygon(50% 0,93.3% 25%,93.3% 75%,50% 100%,6.7% 75%,6.7% 25%)}#header .wath-hlogo,.wath-chip-av,#wath-top .mlogo img{border:0!important;padding:0!important;object-fit:cover}#header .wath-hlogo{width:42px;height:46px}:is(#wath,#wath-top) .av:not(:has(img)),.wath-chip-in:not(:has(img)){background:#cfc3ea!important;color:#3f3478!important}#wath .suplist{position:relative}#wath .suplist>.dn{position:relative;z-index:1}#wath .suplist>svg.bonds{position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible;pointer-events:none;z-index:0}#wath .suplist>svg.bonds path{fill:none;stroke:#dcd3f0;stroke-width:1.4;stroke-linecap:round;stroke-linejoin:round}#wath .suplist>svg.bonds circle{fill:#f6f3fb;stroke:#dcd3f0;stroke-width:1.4}#wath .suplist>svg.bonds circle.f{fill:#dcd3f0;stroke:none}#wath .hero .shr{justify-content:space-between!important;width:100%}#wath .hero .shr .remb{flex:1 1 auto;border-radius:12px;justify-content:center;max-width:none}#wath .chbig.chgold{display:flex;align-items:center;justify-content:center;gap:10px;background:#f0cf6a!important;border:1px solid #d4a63c!important;color:#3b2c08!important}#wath .chbig.chgold:hover{background:#e8c254!important}#wath .chgold .chgi{display:inline-flex}#wath .chgold .chgi svg+svg{margin-left:-8px}#wath .chd{position:relative}#wath .chd .chso{position:absolute;right:0;top:-8px;display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border:0;border-radius:10px;background:none;color:#6152a0;cursor:pointer}#wath .chd .chso:hover{background:rgba(97,82,160,.1)}#wath .chp small.chpart{display:block;font-weight:500;color:#9a93a8;font-size:12px}#wath-top .hxc .bovc{max-width:340px}#wath-top .hxc .hxs{position:relative;margin:0 auto;overflow:hidden;border-radius:12px;background:#ddd;touch-action:none;cursor:grab;user-select:none}#wath-top .hxc .hxs:active{cursor:grabbing}#wath-top .hxc .hxs img{position:absolute;left:0;top:0;max-width:none;transform-origin:0 0;pointer-events:none}#wath-top .hxc .hxs svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}#wath-top .hxc .hxs svg path:first-child{fill:rgba(27,21,38,.55)}#wath-top .hxc .hxs svg .hxl{fill:none;stroke:#fff;stroke-width:.8;vector-effect:non-scaling-stroke}#wath-top .hxc .hxz{display:flex;align-items:center;gap:10px;margin:14px auto 0;max-width:260px;font-size:14px;font-weight:700}#wath-top .hxc .hxz input{flex:1}#wath-top .hxc .hxb{display:flex;gap:10px;justify-content:flex-end;margin-top:16px}#wath .suplist>.dn{padding-top:12px!important;padding-bottom:12px!important}#wath .suplist .dn .av{width:42px!important;height:42px!important;font-size:12.5px}:is(#wath,#wath-top) .cnt:not(.cntn){background:none!important;padding-left:0!important;padding-right:0!important;margin-left:4px;color:#6152a0}:is(#wath,#wath-top) .subnav .snl a.on .cnt:not(.cntn){color:#fff}#wath .chgold .chgi svg+svg{margin-left:-3px!important}#wath .suplist>svg.bonds path.hxo{fill:#fff;stroke:#b9abe0;stroke-width:1}#wath .mwsec>.wrap{padding:44px 28px 52px}#wath .mwsec .mwh{margin:0}@media(min-width:901px){#wath .mwsec .mwh{display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:16px 44px;align-items:start}#wath .mwsec .mwt{grid-column:1/-1}#wath .mwsec .mwl{display:grid;grid-template-columns:1fr 1fr}#wath .mwsec .mwl .mwr{border-bottom:1px solid rgba(27,21,38,.08)}}@media(max-width:900px){#wath .cols:not(.second)>.rband{order:3;margin:8px calc(50% - 50vw);width:auto}#wath .cols:not(.second)>.stack>*{order:5}}@media(max-width:900px){#wath .mwsec>.wrap{padding:32px 18px 40px}}.mov input.manon{background:#f3f0f9!important;color:#6b6380!important;cursor:pointer}.mov .manp{position:fixed;inset:0;z-index:20;background:rgba(27,21,38,.45);display:flex;align-items:center;justify-content:center;padding:20px}.mov .manpc{background:#fff;border-radius:16px;padding:22px 22px 18px;max-width:380px;box-shadow:0 20px 50px rgba(27,21,38,.3)}.mov .manpc b{font-size:18px;color:#1b1526}.mov .manpc p{margin:8px 0 16px;color:#5b5368;line-height:1.45}.mov .manpb{display:flex;gap:10px;justify-content:flex-end;flex-wrap:wrap}@media(min-width:901px){#wath .cols.second{grid-template-columns:minmax(0,1fr) 400px!important;max-width:none}#wath .cols.second>.mwside{position:sticky;top:110px}}#wath .mwside .mwh{margin-top:0}#wath .mwside .mwt{margin-top:0}/* Nov 17 2pm (Nirvan): a 2px white hexagon outline around Rick's logo and the member's photo in the header */#header .wath-hlw{display:inline-flex;flex:none;width:42px;height:46px;padding:2px;box-sizing:border-box;background:#fff;clip-path:polygon(50% 0,93.3% 25%,93.3% 75%,50% 100%,6.7% 75%,6.7% 25%);margin:-9px 0}#header .wath-hlw .wath-hlogo{width:100%!important;height:100%!important;margin:0!important;border:0!important}.wath-chip-av{background:#fff!important;padding:2px!important;box-sizing:border-box;border:0!important}.wath-chip-in{display:flex;align-items:center;justify-content:center;width:100%;height:100%;overflow:hidden;clip-path:polygon(50% 0,93.3% 25%,93.3% 75%,50% 100%,6.7% 75%,6.7% 25%);background:#fff;color:#6152a0}.wath-chip-in img{width:100%;height:100%;object-fit:cover;display:block}#header .wath-hlog .wath-chip-av{width:36px!important;height:40px!important}.wath-chip .wath-chip-av{width:30px;height:33px}#wath .kband .kbi:nth-child(4) .kbic>svg:not(.kbb){width:36px;height:36px}#wath .shr .shl2{display:none;font-weight:700;font-size:15px;color:#3a3245}#wath.wmin .hero .shr .remb{display:none!important}#wath.wmin .hero .shr .shl2{display:inline}#wath.wmin .hero .shr{justify-content:center!important}:is(#wath,#wath-top) .snshr .shl2{display:none!important}/* Nov 17 2:26pm (Nirvan): milestones as targets: the current one pulses, upcoming ones are light gray targets, done ones are crossed off */:is(#wath,#wath-top) .ms .dot{position:relative}:is(#wath,#wath-top) .ms .dot:not(.done):not(.now){background:radial-gradient(circle,#cdc8da 0 22%,#f4f2f8 23% 42%,#cdc8da 43% 60%,#f4f2f8 61% 100%)!important;box-shadow:inset 0 0 0 1.5px #cdc8da}:is(#wath,#wath-top) .ms .dot.now{background:radial-gradient(circle,#6152a0 0 22%,#fff 23% 42%,#6152a0 43% 60%,#fff 61% 100%)!important;box-shadow:inset 0 0 0 1.5px #6152a0}:is(#wath,#wath-top) .ms .dot.now:after{content:"";position:absolute;inset:-1px;border-radius:50%;border:2px solid #6152a0;animation:wathTgt 1.8s ease-out infinite;pointer-events:none}@keyframes wathTgt{0%{transform:scale(1);opacity:.75}100%{transform:scale(2.3);opacity:0}}@media(prefers-reduced-motion:reduce){:is(#wath,#wath-top) .ms .dot.now:after{animation:none;opacity:0}}:is(#wath,#wath-top) .ms:has(.dot.done) .n,:is(#wath,#wath-top) .ms:has(.dot.done) .a{text-decoration:line-through;text-decoration-thickness:1.5px;text-decoration-color:rgba(27,21,38,.45);color:#7a7388}#wath .suplist>svg.bonds path.hxb{stroke:#b9abe0;stroke-width:1}#wath .chwrap{padding:44px 28px 8px}#wath .chwrap>.sec{border-top:0;padding-top:0}#wath .impband{background:#1e1f2c;margin-top:32px}#wath .impband>.wrap{padding:52px 28px}#wath .impband #wath-impact{border-top:0;padding-top:0}#wath .impband #wath-impact>h2.imph{color:#fff}#wath .impband [data-tnd]{max-width:none}@media(max-width:900px){#wath .chwrap{padding:28px 18px 0}#wath .impband>.wrap{padding:36px 18px}}/* Rick's quote framed like on truthnotdare.org: a rounded box with a blue-purple-red gradient outline */:is(#wath,#wath-top) .tndq{border:1.5px solid transparent!important;border-radius:18px;background:linear-gradient(#1b1e2b,#1b1e2b) padding-box,linear-gradient(90deg,#2f9bff,#a46ef2,#e5311f,#a46ef2,#2f9bff) border-box;padding:24px 28px 22px!important;text-align:center}:is(#wath,#wath-top) .tndq .tndby{justify-content:center;text-align:left}#wath .card.tndd.tfill{align-content:space-evenly}/* Nov 17 3:19pm (Nirvan): budget and milestones layout */#wath .msd>summary .mstagw{margin:0 0 10px}#wath .msd.ms-now,#wath .msd.ms-next{padding-top:14px}:is(#wath,#wath-top) .ms .dot.now:after{animation:wathTgt 2.6s ease-out infinite!important}@keyframes wathTgt{0%{transform:scale(1);opacity:.45}100%{transform:scale(1.6);opacity:0}}#wath .msd .ms .msr{margin-left:auto;font-size:13.5px;color:#5b6478;font-weight:600;white-space:nowrap}#wath .msd .ms .msr b{color:#1b1526}#wath .msbl2{display:flex;justify-content:space-between;gap:10px;margin-top:6px;font-size:13.5px;color:#5b6478}#wath .msbl2 b{color:#6152a0}:is(#wath,#wath-top) .ms .dot.todo:not(.done):not(.now){background:#fff!important;box-shadow:inset 0 0 0 1.5px #cfc9dc!important}#wath .bstill{margin-top:26px;font-size:13px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#6b6380}#wath .bsec .bh2{display:flex;align-items:baseline;gap:10px;margin-bottom:4px}#wath .bsec .bh2 b{font-size:19px}#wath .bsec .bh2 .bamt{font-size:19px;font-weight:800;color:#6152a0}#wath .bsec .bh2 .bamt.done{color:#33697f}#wath .bsec .bh2 .bsub{margin-left:auto;font-size:13px;color:#6b6380;font-weight:600}#wath .suplist>.dn.bgrow{opacity:0}#wath .suplist>.dn.bgrow .av{transform:scale(.4)}#wath .suplist>.dn.bgrow.bgin{opacity:1;transition:opacity .25s}#wath .suplist>.dn.bgrow.bgin .av{transform:none;transition:transform .3s cubic-bezier(.2,1.4,.4,1)}#wath .suplist>svg.bonds path.hxo.bgrow{opacity:0;transform-box:fill-box;transform-origin:center;transform:scale(.4)}#wath .suplist>svg.bonds path.hxo.bgrow.bgin{opacity:1;transform:none;transition:opacity .25s,transform .3s cubic-bezier(.2,1.4,.4,1)}.mov .pftr{display:flex;margin:2px 0 12px;padding:0}
.mov .pftr .pfs{display:block!important;flex:1 1 0!important;border:0!important;padding:0!important;margin:0!important;min-width:0;position:relative;text-align:center;font-size:12px;line-height:1.3;color:#8a849a}
.mov .pftr .pfo{display:block;width:14px;height:14px;margin:0 auto 6px;border-radius:50%;border:2px solid #cfc8e6;background:#fff;position:relative;z-index:1;box-sizing:border-box}
.mov .pftr .pfs+.pfs::before{content:"";position:absolute;top:6px;right:50%;width:100%;height:2px;background:#e3def0}
.mov .pftr .pfs.dn::before,.mov .pftr .pfs.now::before{background:#6152a0}
.mov .pftr .pfs.dn .pfo{background:#6152a0;border-color:#6152a0}
.mov .pftr .pfs.now .pfo{border-color:#6152a0;box-shadow:0 0 0 4px rgba(97,82,160,.15)}
.mov .pftr .pfs.now .pfl{color:#1b1526;font-weight:700}
.mov .pfnx{margin:0 0 14px;padding:10px 12px;border-radius:10px;background:#f4f1fb;font-size:14px;line-height:1.45;color:#3a3245}
.mov .pfnx.you{background:#fff6e0}
.mov .pfmsg{display:inline-block;margin-top:12px;font-size:14px}
.mov .tgc .tgamt{margin:10px 0 4px;font-size:15px;color:#5b6478}.mov .tgc .tgamt b{font-size:24px;color:#1b1526;margin-right:6px}
.mov .tgc .pfbar{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.mov .mcard.pfnext{display:flex;flex-direction:column;align-items:flex-start;width:100%;margin-bottom:12px;border-color:#e8c766;background:#fffaf0}
@media(max-width:520px){.mov .pftr .pfl{font-size:11px}}
#wath #wath-levels .lv .lvi.lvfull{aspect-ratio:auto!important;display:block;background:#1b1526}
#wath #wath-levels .lv .lvi.lvfull img{display:block;width:100%;height:auto;max-height:520px;object-fit:cover}
:is(#wath,#wath-top) .gcopl{display:flex;flex-direction:column;gap:10px;margin:14px 0}
:is(#wath,#wath-top) .gcp{display:flex;align-items:stretch;border:1.5px solid #e3def0;border-radius:14px;background:#fff;transition:border-color .15s,background .15s,box-shadow .15s}
:is(#wath,#wath-top) .gcp:hover{border-color:#c9bff0}
:is(#wath,#wath-top) .gcp.on{border-color:#6152a0;background:#f8f6fe;box-shadow:0 4px 14px rgba(97,82,160,.12)}
:is(#wath,#wath-top) .gcp.out .gcpt b{color:#8a849a}
:is(#wath,#wath-top) .gcps{all:unset;box-sizing:border-box;flex:1;min-width:0;display:flex;gap:14px;align-items:flex-start;padding:14px 8px 14px 16px;cursor:pointer;border-radius:14px 0 0 14px}
:is(#wath,#wath-top) .gcps:focus-visible{outline:2px solid #6152a0;outline-offset:2px}
:is(#wath,#wath-top) .gcpb{flex:none;width:24px;height:24px;border-radius:7px;border:2px solid #b9b0dc;display:flex;align-items:center;justify-content:center;color:#fff;font-size:15px;font-weight:900;margin-top:1px;transition:background .15s,border-color .15s;box-sizing:border-box}
:is(#wath,#wath-top) .gcp.on .gcpb,:is(#wath,#wath-top) .gcpb.bell{background:#6152a0;border-color:#6152a0}
:is(#wath,#wath-top) .gcpt{display:flex;flex-direction:column;gap:3px;min-width:0}
:is(#wath,#wath-top) .gcpt b{font-size:16.5px;color:#1b1526;line-height:1.3}
:is(#wath,#wath-top) .gcpm{font-size:13.5px;font-weight:700;color:#6152a0}
:is(#wath,#wath-top) .gcpn{font-size:13.5px;color:#5b6478;line-height:1.4}
:is(#wath,#wath-top) .gcpd{all:unset;box-sizing:border-box;flex:none;align-self:center;margin-right:12px;padding:7px 12px;border-radius:999px;border:1px solid #e3def0;font-size:13px;font-weight:700;color:#5d4fa6;cursor:pointer;background:#fff}
:is(#wath,#wath-top) .gcpd:hover{background:#f4f1fb}
:is(#wath,#wath-top) .gcpd:focus-visible{outline:2px solid #6152a0;outline-offset:2px}
:is(#wath,#wath-top) .gcsum{background:#f6f3fd;border-radius:14px;padding:6px 16px;margin:14px 0}
:is(#wath,#wath-top) .gcsum>div{display:flex;justify-content:space-between;gap:16px;padding:9px 0;font-size:15px}
:is(#wath,#wath-top) .gcsum>div+div{border-top:1px solid #e6e0f4}
:is(#wath,#wath-top) .gcsum span{color:#5b6478}
:is(#wath,#wath-top) .gcsum .tot b{font-size:19px;color:#33697f}
:is(#wath,#wath-top) .gcdl{position:fixed;inset:0;z-index:2147483001;background:rgba(27,21,38,.45);display:flex;align-items:center;justify-content:center;padding:16px}
:is(#wath,#wath-top) .gcdc{position:relative;background:#fff;border-radius:16px;max-width:480px;width:100%;max-height:85vh;overflow:auto;padding:22px 22px 18px;box-shadow:0 20px 60px rgba(27,21,38,.35);color:#1b1526;font-size:15px}
:is(#wath,#wath-top) .gcdc .gcox{color:#5b6478;top:10px}
:is(#wath,#wath-top) .gcdh{display:block;font-size:20px;margin:0 30px 4px 0}
:is(#wath,#wath-top) .gcdc p{color:#4a4560;line-height:1.5;margin:10px 0}
:is(#wath,#wath-top) .gcdc ul{margin:6px 0 8px;padding-left:18px;color:#4a4560;font-size:14.5px;line-height:1.5}
:is(#wath,#wath-top) .gcdc .gcpm2{font-size:14px;color:#33697f;font-weight:700}
@media(max-width:560px){:is(#wath,#wath-top) .gcps{padding:12px 6px 12px 12px;gap:10px}:is(#wath,#wath-top) .gcpd{margin-right:8px;padding:6px 10px}}
#wath .tmc .tmw{display:inline-flex;flex:none;width:90px;height:90px;padding:3px;box-sizing:border-box;margin-bottom:8px;background:#7d6bc6;clip-path:polygon(50% 0,93.3% 25%,93.3% 75%,50% 100%,6.7% 75%,6.7% 25%)}
#wath .tmc .tmw>.tmp,#wath .tmc .tmw>.tmi{width:100%!important;height:100%!important;margin:0!important}
#wath .crewt{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:6px;font-weight:700;color:#6152a0;margin-top:2px}
#wath .crewt:focus-visible{outline:2px solid #6152a0;outline-offset:3px;border-radius:4px}
#wath .crewt .crc,#wath .crewt[aria-expanded=true] .crs{display:none}
#wath .crewt[aria-expanded=true] .crc{display:inline}
#wath .crewt[aria-expanded=true] .chev{transform:rotate(180deg)}
#wath .crewb .crew5{margin:0 0 14px}
#wath .suplist>.dn.sp{cursor:pointer;border-radius:12px;transition:background .15s}
#wath .suplist>.dn.sp:hover,#wath .suplist>.dn.sp:focus-visible{background:rgba(97,82,160,.08);outline:0}
#wath .suplist>.dn.sp:focus-visible{box-shadow:0 0 0 2px #6152a0}
#wath .spcm{display:inline-flex;align-items:center;color:#8a7cc8;margin-left:6px;vertical-align:-2px}
#wath-top .spov .spvh .av{text-transform:none;width:64px;height:64px;font-size:20px;flex:none;display:inline-flex;align-items:center;justify-content:center;background:#cfc3ea;color:#3f3478;font-weight:800;overflow:hidden}
#wath-top .spov .spvh .av img{width:100%;height:100%;object-fit:cover}
#wath-top .spst{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}
#wath-top .spst>div{flex:1 1 120px;background:#f6f3fd;border-radius:12px;padding:10px 12px}
#wath-top .spst b{display:block;font-size:17px;color:#1b1526}
#wath-top .spst span{font-size:13px;color:#5b6478}
#wath-top .spq blockquote{margin:0 0 10px;padding:10px 14px;border-left:3px solid #8a7cc8;background:#faf9fd;border-radius:0 10px 10px 0;color:#3a3245;font-size:15px;line-height:1.5}
#wath-top .spnq{color:#5b6478;font-size:14.5px}
#wath-top .mslab.mshd{all:unset;box-sizing:border-box;display:flex;align-items:center;gap:6px;width:100%;font-size:11px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#6152a0;padding:8px 11px 4px;cursor:pointer}
#wath-top .mslab.mshd .mbeta{letter-spacing:.04em}
#wath-top .mslab.mshd .chev{margin-left:auto;transition:transform .15s;flex:none}
#wath-top .mslab.mshd[aria-expanded=false] .chev{transform:rotate(-90deg)}
#wath-top .mslab.mshd:focus-visible{outline:2px solid #6152a0;outline-offset:-2px;border-radius:8px}
#wath-top .msgb.cl{display:none}
#wath-top .mslab.tm.tmtop{border-top:0;margin-top:0;padding-top:8px}
#wath-top .msgb[data-g=team]+.mslab{border-top:1px solid #ebe7f5;margin-top:6px;padding-top:14px}
@media(max-width:800px){#wath-top .mslab.mshd{display:none}#wath-top .msgb.cl{display:contents}#wath-top .msgb{display:contents}}
@media(min-width:801px){#wath-top .msgb{display:flex;flex-direction:column;align-items:stretch}#wath-top .msgb>.msn{text-align:left}#wath-top .msgb.cl{display:none}}
/* Nov 17 4:19pm (Nirvan): the member's hexagon matches Rick's hexagon (42x46, white outline) in both top bars */
#header .wath-chip-av,#header .wath-hlog .wath-chip-av,#wath-top .wath-chip .wath-chip-av,.wath-chip .wath-chip-av{width:42px!important;height:46px!important;font-size:13px!important}
#wath-top .mme .wath-chip-av{width:42px!important;height:46px!important;font-size:13px;font-weight:800;display:inline-flex;flex:none}
#wath-top .mlogo img{width:42px!important;height:46px!important;padding:2px!important;background:#fff!important;box-sizing:border-box}
:is(#wath,#wath-top) .hxw{display:inline-flex;flex:none;align-self:center;padding:2px;background:#9d8fd8;line-height:0;vertical-align:middle;clip-path:polygon(50% 0,93.3% 25%,93.3% 75%,50% 100%,6.7% 75%,6.7% 25%)}
:is(#wath,#wath-top) .hxw>*{margin:0!important;box-shadow:none!important;border:0!important}
#wath-top .mme .hxw,#wath-top .mme .hxw.hxm{padding:2px;background:#fff}
#wath-top .sphx{margin:0 0 14px;border:1px solid #e3def0;border-radius:12px}
#wath-top .sphb{all:unset;box-sizing:border-box;display:flex;align-items:center;gap:8px;width:100%;padding:11px 14px;font-weight:700;font-size:14.5px;color:#5d4fa6;cursor:pointer}
#wath-top .sphb .chev{margin-left:auto;transition:transform .15s}
#wath-top .sphb[aria-expanded=true] .chev{transform:rotate(180deg)}
#wath-top .sphb:focus-visible{outline:2px solid #6152a0;border-radius:12px}
#wath-top .sphl{padding:0 14px 8px}
#wath-top .sphl>div{display:flex;justify-content:space-between;padding:7px 0;border-top:1px solid #f0edf7;font-size:14.5px}
#wath-top .sphl span{color:#5b6478}
#wath-top .spch{margin:0 0 14px}
#wath-top .spl{display:block;font-size:11px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#6152a0;margin-bottom:6px}
#wath-top .spch>div{display:flex;justify-content:space-between;gap:10px;padding:9px 12px;background:#fff8e8;border-radius:10px;margin-bottom:6px;font-size:14.5px}
#wath-top .spch>div span{color:#7a6230}
#wath-top .spbio p{margin:0 0 10px;color:#3a3245;line-height:1.5;font-size:15px}
#wath-top .spbio .sprole{font-weight:700;color:#5d4fa6;font-size:14px}
#wath-top .splk{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px}
#wath-top .splk a{padding:6px 12px;border-radius:999px;border:1px solid #e3def0;font-size:13.5px;font-weight:700;color:#5d4fa6;text-decoration:none}
#wath-top .splk a:hover{background:#f4f1fb}
#wath-top .spf{display:flex;flex-wrap:wrap;gap:10px}
#wath-top .spf .btn{display:inline-flex;align-items:center;gap:7px}
#wath-top .spq:empty{display:none}
:is(#wath,#wath-top) .gcgets{margin:16px 0 4px;background:#f6f3fd;border-radius:14px;padding:14px 18px}
:is(#wath,#wath-top) .gcgl{display:block;font-size:11.5px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#6152a0;margin-bottom:6px}
:is(#wath,#wath-top) .gcgets ul{margin:0;padding-left:20px;color:#3a3245;line-height:1.5;font-size:15px}
:is(#wath,#wath-top) .gcgets li{margin:4px 0}
:is(#wath,#wath-top) .gcgets li::marker{color:#8a7cc8}
:is(#wath,#wath-top) .gclim{margin:12px 0 0;padding-top:12px;border-top:1px solid #e6e0f4}
:is(#wath,#wath-top) .gclq{display:inline-block;margin-left:6px;font-size:12.5px;font-weight:700;color:#7a6230;background:#fff3d6;border-radius:999px;padding:1px 8px}
:is(#wath,#wath-top) .gclq.out{color:#8a3b2a;background:#fbe5df}
@keyframes gnew{0%{opacity:0;transform:translateY(8px) scale(.97);background:rgba(97,82,160,.18)}60%{opacity:1;transform:none;background:rgba(97,82,160,.12)}100%{background:transparent}}
:is(#wath,#wath-top) .gcgets li{border-radius:6px;padding:0 4px;margin-left:-4px}
:is(#wath,#wath-top) .gcgets li.gout{pointer-events:none}
@media(prefers-reduced-motion:reduce){:is(#wath,#wath-top) .gcgets li.gnew{animation:none}}
#wath #wath-levels .crh.crh1 span{margin-top:0;font-size:15px;font-weight:700;opacity:1;line-height:1.4}
:is(#wath,#wath-top) .pki{display:inline-block;vertical-align:-3px;margin-left:6px;flex:none}
:is(#wath,#wath-top) .gcos{align-items:center;gap:6px!important;flex-wrap:nowrap;white-space:nowrap;overflow:hidden}
:is(#wath,#wath-top) .gcos .gca{display:inline-flex;color:#b9b0dc;flex:none}
:is(#wath,#wath-top) .gcos .gcmw{display:inline-flex;align-items:center;gap:6px;flex:none}
:is(#wath,#wath-top) .gcos .gcst.on{color:#6152a0}
:is(#wath,#wath-top) .gcos .gcst.dn{color:#33697f}
@media(max-width:560px){:is(#wath,#wath-top) .gcos{font-size:12px!important;gap:4px!important}}
:is(#wath,#wath-top) .gcos .gcmw .gcst{margin-left:6px!important;margin-right:0!important}
:is(#wath,#wath-top) .gcos>.gca{margin:0 9px!important}
:is(#wath,#wath-top) .gcos .gcmw>.gca{margin:0 3px 0 9px!important}
:is(#wath,#wath-top) .gclv{padding:6px 0 2px;text-align:left}
:is(#wath,#wath-top) .gclvi{font-size:30px;line-height:1;margin:6px 0 8px}
:is(#wath,#wath-top) .gci{all:unset;box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:#6152a0;color:#fff;font:italic 700 12px/1 Georgia,serif;cursor:pointer;vertical-align:1px;margin-left:4px}
:is(#wath,#wath-top) .gci:focus-visible{outline:2px solid #1b1526;outline-offset:2px}
:is(#wath,#wath-top) .gcix{display:block;margin-top:6px;font-size:13.5px;color:#5b6478;line-height:1.45}
:is(#wath,#wath-top) .gcpi{flex:none;width:72px;height:72px;border-radius:10px;object-fit:cover;background:#e9e4f7}
:is(#wath,#wath-top) .gcp .gcpm{font-size:14px;color:#1b1526}
:is(#wath,#wath-top) .gcpa{font-size:12.5px;font-weight:700;color:#7a6230;background:#fff3d6;border-radius:999px;padding:1px 8px;align-self:flex-start}
@media(max-width:560px){:is(#wath,#wath-top) .gcpi{width:56px;height:56px}}
#wath-top .mdisc .mdh{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:6px 0 2px}
#wath-top .mdisc .mdh .mh3{margin:0;font-size:24px}
#wath-top .mdisc .mcode{font-weight:800;letter-spacing:.06em;background:#f4f1fb;border:1px dashed #b9b0dc;border-radius:8px;padding:4px 10px;color:#3f3478}
#wath-top .mdl{list-style:none;margin:10px 0 12px;padding:0}
#wath-top .mdl li{display:flex;align-items:center;gap:10px;padding:7px 0;border-top:1px solid #f0edf7;font-size:14.5px}
#wath-top .mdl li>span:nth-child(2){flex:1}
#wath-top .mdl em{font-style:normal;font-weight:700;color:#8a849a;font-size:13px}
#wath-top .mdl li.ok em{color:#33697f}
#wath-top .mdk{flex:none;width:20px;height:20px;border-radius:6px;border:2px solid #cfc8e6;display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px;font-weight:900;box-sizing:border-box}
#wath-top .mdl li.ok .mdk{background:#33697f;border-color:#33697f}
.mov .pfd.pfpend{opacity:.62;background:#faf9fc}
.mov .pfd.pfpend .pfsum{display:flex;align-items:center;gap:12px;padding:14px 16px}
.mov .pfd.pfpend .pft span{display:block;font-size:13.5px;color:#5b6478}
.mov .pfd.pfpend .apill{flex:none;white-space:nowrap}
.mov .pfint{all:unset;box-sizing:border-box;display:flex;gap:12px;align-items:flex-start;width:100%;padding:12px 14px;border:1.5px solid #e3def0;border-radius:12px;cursor:pointer;background:#fff;margin:0 0 10px}
.mov .pfint.on{border-color:#6152a0;background:#f8f6fe}
.mov .pfint:focus-visible{outline:2px solid #6152a0;outline-offset:2px}
.mov .pfint b{display:block;font-size:15px;color:#1b1526}
.mov .pfint em{display:block;font-style:normal;font-size:13.5px;color:#5b6478;margin-top:2px}
.mov .pfib{flex:none;width:22px;height:22px;border-radius:7px;border:2px solid #b9b0dc;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:13px;box-sizing:border-box;margin-top:1px}
.mov .pfint.on .pfib{background:#6152a0;border-color:#6152a0}
.mov .pfn2{font-size:14px;color:#3a3245;line-height:1.5;margin:0 0 8px}
.mov .pfn2 .soon{margin-left:4px}
.mov .pfsv{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 10px}
#wath-top .mov .pfsv button{all:unset;box-sizing:border-box;cursor:pointer;padding:6px 12px;border-radius:999px;border:1px solid #e3def0;font-size:13.5px;font-weight:700;color:#5d4fa6;background:#fff}
#wath-top .mov .pfsv button.on{background:#6152a0;border-color:#6152a0;color:#fff}
#wath-top .mov .pfsv button span{opacity:.75;margin-left:3px}
.mov .pfsk{display:inline-flex;align-items:center;gap:8px;font-size:13.5px;font-weight:700;color:#5b6478;margin-bottom:8px}
.mov .pfsk select,.mov .pfdt{border:1px solid #cfc8e6;border-radius:8px;padding:4px 8px;font:inherit;font-size:13.5px;background:#fff}
:is(#wath,#wath-top) .gcos{position:relative;padding:5px 0 5px 8px;isolation:isolate;overflow:visible!important}
:is(#wath,#wath-top) .gcos .gcpill{position:absolute!important;left:0;top:calc(50% - 13px)!important;height:26px;margin:0!important;padding:0!important;border-radius:999px;background:#ece7fb;border:1px solid #cdbff3;z-index:-1;pointer-events:none;box-sizing:border-box}
:is(#wath,#wath-top) .gcos .gcst.on{color:#4a3d8f}
:is(#wath,#wath-top) .gcdcar{position:relative;margin:-22px -22px 14px;border-radius:16px 16px 0 0;overflow:hidden;background:#1b1526;aspect-ratio:16/10}
:is(#wath,#wath-top) .gcdtr{display:flex;height:100%;transition:transform .45s cubic-bezier(.3,.8,.3,1)}
:is(#wath,#wath-top) .gcdtr img{flex:0 0 100%;width:100%;height:100%;object-fit:cover;display:block}
:is(#wath,#wath-top) .gcdar{all:unset;position:absolute;top:50%;margin-top:-18px;width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.92);color:#1b1526;font-size:24px;line-height:34px;text-align:center;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.25)}
:is(#wath,#wath-top) .gcdar.l{left:10px}:is(#wath,#wath-top) .gcdar.r{right:10px}
:is(#wath,#wath-top) .gcddots{position:absolute;left:0;right:0;bottom:10px;display:flex;justify-content:center;gap:6px}
:is(#wath,#wath-top) .gcddots button{all:unset;width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.55);cursor:pointer}
:is(#wath,#wath-top) .gcddots button.on{background:#fff}
:is(#wath,#wath-top) .gcdc .gcox{z-index:3;background:rgba(255,255,255,.9)!important;border-radius:50%;width:34px;height:34px;line-height:32px;text-align:center;font-size:24px}
:is(#wath,#wath-top) .gcdc{max-width:560px!important}
:is(#wath,#wath-top) .gcp{flex-wrap:wrap}
:is(#wath,#wath-top) .gcph{flex:1 1 100%;display:block;margin:0 16px 14px 54px;font-size:13.5px;font-weight:700;color:#3a3245}
:is(#wath,#wath-top) .gcph input{display:block;width:100%;max-width:320px;margin-top:6px;border:1px solid #cfc8e6;border-radius:10px;padding:9px 12px;font:inherit;font-weight:400;font-size:15px;box-sizing:border-box}
:is(#wath,#wath-top) .gcph em{display:block;font-style:normal;font-weight:400;color:#5b6478;margin-top:5px}
:is(#wath,#wath-top) .gcmng{font-size:14px;color:#5d4fa6!important;font-weight:600}
@media(max-width:560px){:is(#wath,#wath-top) .gcph{margin-left:46px}}
#wath-top .mbdg.mbdot{position:relative;padding-left:16px}
#wath-top .mbdg.mbdot::before{content:"";position:absolute;left:6px;top:50%;margin-top:-3px;width:6px;height:6px;border-radius:50%;background:#f3c64e}
#wath-top .inbl{padding:4px 0}
#wath-top .inbm{border-top:1px solid #f0edf7}
#wath-top .inbm:first-child{border-top:0}
#wath-top .inbh{all:unset;box-sizing:border-box;display:flex;gap:12px;align-items:center;width:100%;padding:13px 18px;cursor:pointer}
#wath-top .inbh:hover{background:#faf9fd}
#wath-top .inbh:focus-visible{outline:2px solid #6152a0;outline-offset:-2px}
#wath-top .inbd{flex:none;width:9px;height:9px;border-radius:50%;background:transparent}
#wath-top .inbm.un .inbd{background:#6152a0;box-shadow:0 0 0 3px rgba(97,82,160,.18)}
#wath-top .inbw{display:flex;flex-direction:column;min-width:0}
#wath-top .inbw b{font-size:15px;font-weight:600;color:#3a3245}
#wath-top .inbm.un .inbw b{font-weight:800;color:#1b1526}
#wath-top .inbw span{font-size:13px;color:#8a849a}
#wath-top .inbb{padding:0 18px 14px 39px;font-size:15px;line-height:1.55;color:#3a3245}
#wath-top .inbb ul{padding-left:18px;margin:6px 0}
#wath-top .pfm2{display:grid;grid-template-columns:200px 1fr;gap:8px;margin-top:8px}
#wath-top .pfm2 textarea{grid-column:1/-1}
#wath-top .pfm2 .btn{justify-self:start}
#wath-top .inbc select,#wath-top .pfm2 select,#wath-top .pfm2 input,#wath-top .pfm2 textarea{border:1px solid #cfc8e6;border-radius:8px;padding:8px 10px;font:inherit;font-size:14px}
@media(max-width:600px){#wath-top .pfm2{grid-template-columns:1fr}}
:is(#wath,#wath-top) .hz{background:none!important;border-radius:0!important;box-shadow:none!important;overflow:visible}
:is(#wath,#wath-top) .hz .hrt{position:absolute;inset:-3px -4px -4px;width:calc(100% + 8px);height:calc(100% + 7px);overflow:visible;z-index:0}
:is(#wath,#wath-top) .hz>svg:not(.hrt){position:relative;z-index:1;margin-top:-3px}
#wath .chi2 .hz .hrt path{fill:color-mix(in srgb,var(--cc) 45%,#fff);stroke:#fffaf0;stroke-width:2.6;stroke-linejoin:round}
#wath .chw.next .chi2 .hz .hrt path{stroke:#f8f6fe}
#wath .chi2 .g2{z-index:2}
:is(#wath,#wath-top) .mxi2 .hz .hrt path,:is(#wath,#wath-top) .mxi.hz .hrt path{fill:#f1d28a;stroke:#fbf3df;stroke-width:2.6;stroke-linejoin:round}
#wath .chrow .chb{margin-left:-12px!important}
:is(#wath,#wath-top) .gctot{margin:0 0 12px;padding:0 0 12px;border-bottom:1px solid #e6e0f4;font-size:15px;line-height:1.5;color:#3a3245}
:is(#wath,#wath-top) .gcnew{display:inline-block;margin-left:6px;font-size:11px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:#6152a0;border-radius:999px;padding:1px 7px;vertical-align:1px}
#wath #wath-recent .suplist>.dn.dnm{padding-top:2px;padding-bottom:2px;margin:-12px 0}
#wath #wath-recent .dnm .wn{display:flex!important;flex-direction:column;align-items:flex-start;min-width:0}
#wath #wath-recent .dnm .wn b{white-space:normal;line-height:1.25}
#wath #wath-recent .dnm .av.avm{background:#f7ecc9!important;color:#9a8550!important;font-size:11px}
#wath #wath-recent .x2{display:inline-block;margin-top:3px;font-size:11px;font-weight:800;color:#6b5210;background:#f8e08e;border-radius:999px;padding:0 7px;line-height:16px;align-self:flex-end}
#wath .suplist svg.bonds .hxo.m{stroke:#ecdcae}
#wath .suplist svg.bonds .bs.bm path{stroke:#ecdcae}
#wath .suplist svg.bonds .bs.bm circle{stroke:#ecdcae;fill:#fffaf0}
#wath .suplist>.dn{padding-left:14px!important;padding-right:18px!important;border-radius:14px}
#wath .suplist>.dn.hv{border-radius:14px;transition:background .15s}
#wath .suplist>.dn.hv:hover{background:rgba(97,82,160,.08)}
#wath #wath-recent .suplist>.dn.rc>.who{padding-left:28px}
#wath #wath-recent .suplist>.dn:is(.rc,.dnm)>.who .wn{display:flex!important;flex-direction:column;align-items:flex-start;row-gap:0;min-width:0}
#wath #wath-recent .wn .wn1{display:flex;flex-wrap:wrap;align-items:center;column-gap:10px;row-gap:4px;min-width:0}
#wath #wath-recent .wn .dnms{display:flex;align-items:center;gap:4px;font-size:12.5px;font-weight:500;color:#8a849a;margin-top:2px;line-height:1.3}
#wath #wath-recent .dnm .dnms{color:#a7a1b4}
#wath #wath-recent .dnm .wn b{font-weight:600;font-size:13.5px;color:#8a849a}
#wath #wath-recent .dn:is(.rc,.dnm) .amtc{display:flex;flex-direction:column;align-items:flex-end}
#wath #wath-recent .dnm .amtc .a{font-weight:700;color:#a9925a}
#wath #wath-recent .suplist>.dn.dnm>.who{padding-left:56px}
#wath #wath-recent .suplist>.dn.dnm{cursor:pointer;background:none!important}
#wath #wath-recent .suplist>.dn.dnm::before{content:"";position:absolute;left:108px;right:0;top:9px;bottom:9px;border-radius:12px;background:transparent;transition:background .15s;z-index:-1}
#wath #wath-recent .suplist>.dn.dnm:hover::before,#wath #wath-recent .suplist>.dn.dnm.on::before{background:rgba(201,154,62,.11)}
#wath #wath-recent .suplist>.dn.dnm:focus-visible{outline:0}
#wath #wath-recent .suplist>.dn.dnm:focus-visible::before{box-shadow:0 0 0 2px #c99a3e}
#wath #wath-recent .dnm .dnms{display:block}#wath #wath-recent .dnm .chev{display:inline-block;vertical-align:-2px;margin-left:4px;transition:transform .25s;opacity:.8}
#wath #wath-recent .dnm.on .chev{transform:rotate(180deg)}
#wath #wath-recent .dnm:hover .dnms,#wath #wath-recent .dnm.on .dnms{color:#9a8550}
#wath #wath-recent .dnm .av.avp{opacity:.82}
#wath #wath-recent .dnx{position:relative;z-index:2;margin:14px 0 18px 108px;padding:16px 18px 16px;background:#fffaf0;border:1px solid #f0e3bf;border-radius:16px;box-shadow:0 6px 18px rgba(154,133,80,.10)}
#wath #wath-recent .dnxh{display:flex;align-items:center;gap:12px}
#wath #wath-recent .dnxh .chi2{flex:none}
#wath #wath-recent .dnxt{display:flex;flex-direction:column;min-width:0}
#wath #wath-recent .dnxt b{font-size:14.5px;font-weight:700;color:#3a3245;line-height:1.3}
#wath #wath-recent .dnxt span{font-size:13px;color:#6b6478;margin-top:2px}
#wath #wath-recent .dnxt span b{font-size:13px;color:#3a3245}
#wath #wath-recent .dnxb{display:block;height:8px;margin:12px 0 4px;border-radius:999px;background:#f1e7cd;overflow:hidden}
#wath #wath-recent .dnxb i{display:block;height:100%;border-radius:999px;background:var(--cc)}
#wath #wath-recent .dnxl{display:block;margin:12px 0 6px;font-size:11.5px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:#a9925a}
#wath #wath-recent p.dnxl{text-transform:none;letter-spacing:0;font-weight:500;font-size:13px;color:#6b6478}
#wath #wath-recent ul.dnxp{list-style:none!important;margin:0!important;padding:0!important;display:flex;flex-direction:column;gap:2px}
#wath #wath-recent ul.dnxp li{display:flex!important;align-items:center;gap:10px;margin:0!important;padding:5px 8px!important;border-radius:10px;font-size:13.5px;color:#3a3245}
#wath #wath-recent ul.dnxp li::before{display:none!important}
#wath #wath-recent ul.dnxp li.me{background:#f8e9bd}
#wath #wath-recent ul.dnxp li .av{width:26px!important;height:26px!important;font-size:9.5px!important;flex:none}
#wath #wath-recent ul.dnxp .dnxn{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#wath #wath-recent ul.dnxp .dnxn em{font-style:normal;font-size:11px;font-weight:800;color:#6b5210;background:#f8e08e;border-radius:999px;padding:0 6px;margin-left:4px}
#wath #wath-recent ul.dnxp b{font-weight:700;color:#a9925a}
#wath #wath-recent .dnxa{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:14px}
#wath #wath-challenges .chw.chflash{animation:chfl 1.8s ease}
@keyframes chfl{0%,100%{box-shadow:0 0 0 0 rgba(201,154,62,0)}20%,60%{box-shadow:0 0 0 4px rgba(201,154,62,.45)}}
@media (max-width:600px){#wath .suplist>.dn{padding-left:8px!important;padding-right:10px!important}#wath #wath-recent .suplist>.dn.dnm>.who{padding-left:44px}#wath #wath-recent .suplist>.dn.dnm::before{left:92px}#wath #wath-recent .dnx{margin-left:28px;padding:14px}}
#wath .suplist>svg.bonds .gseal.soft{opacity:.45}
#wath .suplist>svg.bonds path.hxo.g{stroke:#d4a23a;stroke-width:1.6}
#wath .suplist>svg.bonds .gseal{filter:drop-shadow(0 1px 2px rgba(150,110,30,.25))}
#wath #wath-recent .lvb{position:relative;display:inline;margin:0;padding:0;border:0;background:none;font:inherit;color:inherit;cursor:default;text-decoration:none}
#wath #wath-recent .lvb:hover{color:#6b6390}
#wath #wath-recent .lvb .tip{display:none;position:absolute;left:0;top:calc(100% + 8px);background:#4b3f8c;color:#fff!important;font-weight:500;font-size:12.5px;line-height:1.45;padding:9px 12px;border-radius:11px;width:max-content;max-width:260px;z-index:60;text-align:left;white-space:normal;box-shadow:0 10px 28px rgba(45,32,100,.32),0 2px 6px rgba(45,32,100,.18)}
#wath #wath-recent .lvb:hover .tip,#wath #wath-recent .lvb:focus-visible .tip{display:block}
@media (hover:none){#wath #wath-recent .lvb .tip{display:none!important}}
#wath-top .spov .spsl{position:relative;display:inline-flex;flex:none;margin:4px 6px 4px 4px}
#wath-top .spov .spsl .spseal{position:absolute;left:50%;top:50%;width:92px;height:92px;transform:translate(-50%,-50%);pointer-events:none;filter:drop-shadow(0 1px 3px rgba(150,110,30,.3))}
#wath-top .spov .spsl>.hxw,#wath-top .spov .spsl>.av{position:relative;z-index:1}
#wath-top .spov .spsl .hxw{background:#d4a23a!important}
:is(#wath,#wath-top) .pkt{position:relative;display:inline-flex;vertical-align:-3px;cursor:help;border-radius:6px;outline:0}
:is(#wath,#wath-top) .pkt .pki{vertical-align:0}
:is(#wath,#wath-top) .pkt:focus-visible{box-shadow:0 0 0 2px #6152a0}
:is(#wath,#wath-top) .pkt .pktip{display:none;position:absolute;left:50%;bottom:calc(100% + 8px);transform:translateX(-50%);opacity:1!important;letter-spacing:0;text-transform:none;background:#4b3f8c;color:#fff!important;font-weight:500;font-size:12.5px;line-height:1.45;padding:9px 12px;border-radius:11px;width:max-content;max-width:260px;z-index:60;text-align:left;white-space:normal;box-shadow:0 10px 28px rgba(45,32,100,.32),0 2px 6px rgba(45,32,100,.18)}
:is(#wath,#wath-top) .pkt .pktip::after{content:"";position:absolute;left:50%;top:100%;margin-left:-6px;border:6px solid transparent;border-top-color:#4b3f8c}
@media (hover:hover){:is(#wath,#wath-top) .pkt:hover .pktip{display:block}}
:is(#wath,#wath-top) .pkt:focus-visible .pktip,:is(#wath,#wath-top) .pkt.on .pktip{display:block}
#wath .pkedb{display:inline-flex;align-items:center;gap:5px;margin:0 0 0 6px;padding:3px 6px;border:1px dashed #b9abe0;border-radius:7px;background:#fff;color:#6152a0;font:600 12px/1 inherit;cursor:pointer;vertical-align:1px;opacity:.55;transition:opacity .15s,background .15s}
#wath li:hover>.pkedb,#wath .pkedb:focus-visible{opacity:1}
#wath .pkedb:hover{background:#efeafb;opacity:1}
#wath .lh .pkedb.pkedh{margin-left:auto;opacity:.85;padding:5px 9px}
.mov .pke .pkelv{display:flex;gap:8px;overflow-x:auto;padding:2px 2px 10px;margin:0 0 6px;scrollbar-width:thin}
.mov .pke .pkelv button{flex:none;display:flex;flex-direction:column;align-items:flex-start;gap:2px;padding:9px 13px;border:1px solid #ddd5f0;border-radius:12px;background:#fff;color:#3a3245;cursor:pointer;text-align:left}
.mov .pke .pkelv button b{font-size:14px;font-weight:800;color:#6152a0}
.mov .pke .pkelv button span{font-size:12px;color:#6b6478;white-space:nowrap}
.mov .pke .pkelv button.on{background:#6152a0;border-color:#6152a0}
.mov .pke .pkelv button.on b,.mov .pke .pkelv button.on span{color:#fff}
.mov .pke .pkeg{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:22px;align-items:start}
@media (max-width:860px){.mov .pke .pkeg{grid-template-columns:1fr}.mov .pke .pkep{order:-1;position:static!important}}
.mov .pke .pkei{border:1px solid #e6e0f4;border-radius:14px;padding:12px 14px;margin:0 0 12px;background:#fdfcff}
.mov .pke .pkei.fl{border-color:#6152a0;box-shadow:0 0 0 3px rgba(97,82,160,.15)}
.mov .pke .pkei1{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.mov .pke .pken{flex:none;width:22px;height:22px;border-radius:50%;background:#efeafb;color:#6152a0;font-size:12px;font-weight:800;display:inline-flex;align-items:center;justify-content:center}
.mov .pke input.pket{flex:1 1 calc(100% - 40px);min-width:0;font-size:15px;font-weight:600;padding:9px 11px;border:1px solid #d9d1ee;border-radius:10px;background:#fff}
.mov .pke .pkeo{display:flex;gap:4px;flex:none;margin-left:30px}
.mov .pke .pkeo button{height:36px;min-width:34px;padding:0 8px;border:1px solid #e0d9f2;border-radius:9px;background:#fff;color:#3a3245;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:4px;font-size:14px}
.mov .pke .pkeo button:disabled{opacity:.35;cursor:default}
.mov .pke .pkeo button.pkedel:hover{background:#fbecef;color:#8a1f3d;border-color:#f0c9d3}
.mov .pke .pkeo .pkeib{min-width:52px}
.mov .pke .pkeni{font-size:11px;color:#8a849a;white-space:nowrap}
.mov .pke .pkeic{display:grid;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:6px;margin:10px 0 2px;padding:10px;border-radius:12px;background:#f5f2fc}
.mov .pke .pkeic button{display:flex;align-items:center;gap:8px;padding:7px 9px;border:1px solid transparent;border-radius:9px;background:#fff;cursor:pointer;font-size:12.5px;color:#3a3245;text-align:left}
.mov .pke .pkeic button.on{border-color:#6152a0;background:#efeafb;font-weight:700}
.mov .pke .pkeic button:hover{border-color:#b9abe0}
.mov .pke .pkef{display:flex;flex-direction:column;gap:5px;margin:12px 0 0;font-size:13px;font-weight:700;color:#3a3245}
.mov .pke .pkef em{font-style:normal;font-weight:500;color:#8a849a;margin-left:6px}
.mov .pke .pkef textarea,.mov .pke .pkef input{font:inherit;font-weight:500;font-size:14px;padding:8px 11px;border:1px solid #d9d1ee;border-radius:10px;background:#fff;resize:vertical;width:100%;box-sizing:border-box}
.mov .pke .pkemo{display:inline-flex;align-items:center;gap:6px;font-weight:600}
.mov .pke .pkemo input{width:140px}
.mov .pke .pkec{display:inline-flex;align-items:center;gap:8px;margin:10px 0 0;font-size:13px;color:#3a3245;cursor:pointer}
.mov .pke details.pked{margin:12px 0 0;border-top:1px dashed #e0d9f2;padding-top:10px}
.mov .pke details.pked summary{cursor:pointer;font-size:13px;font-weight:700;color:#6152a0}
.mov .pke .pkeadd{width:100%;border-style:dashed}
.mov .pke .pketip{margin:10px 0 0;font-size:12.5px}
.mov .pke .pkep{position:sticky;top:12px;padding:14px;border-radius:16px;background:#f5f2fc}
.mov .pke .pkepv{margin:8px 0 0;background:#fff;border-radius:14px;overflow:visible;box-shadow:0 1px 4px rgba(27,21,38,.08)}
.mov .pke .pkepv .pkph{display:flex;align-items:baseline;gap:10px;padding:12px 16px;background:#e7e1f7;border-radius:14px 14px 0 0}
.mov .pke .pkepv .pkph .amt{font-weight:800;color:#6152a0}
.mov .pke .pkepv .pkph b{font-weight:800;letter-spacing:.04em;text-transform:uppercase;font-size:14px}
.mov .pke .pkepv .pkpt{padding:12px 16px 14px}
.mov .pke .pkepv ul{margin:0;padding:0 0 0 18px}
.mov .pke .pkepv li{margin:0 0 6px;font-size:14px;line-height:1.5}
.mov .pke .pkepv .soon{font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.05em;color:#6152a0;background:#efeafb;border-radius:999px;padding:1px 7px}
.mov .pke .pkepv .lall{color:#6b6478;font-style:italic}
.mov .pke .pkebar{position:sticky;bottom:0;z-index:3;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;margin:16px -4px -4px;padding:12px 4px 4px;background:linear-gradient(rgba(255,255,255,0),#fff 30%)}
.mov .pke .pkebb{display:flex;flex-wrap:wrap;align-items:center;gap:10px}
.mov .pke .pkest{font-size:13px;color:#6b6478}
.mov .pke .pkeerr{color:#8a1f3d;font-weight:600}
.mov .tmctl{display:flex;flex-wrap:wrap;align-items:center;justify-content:flex-end;gap:8px;flex:none}
.mov .tmpp{display:inline-flex;align-items:center;gap:7px;font-size:12px;font-weight:700;color:#6152a0;background:#f5f2fc;border:1px solid #e0d9f2;border-radius:999px;padding:5px 11px 5px 6px;cursor:pointer;white-space:nowrap}
.mov .tmpp.inc{cursor:default;padding:5px 11px;color:#6b6478}
.mov .tmpp i{width:26px;height:15px;border-radius:999px;background:#d6cfe8;position:relative;transition:background .2s}
.mov .tmpp i::after{content:"";position:absolute;left:2px;top:2px;width:11px;height:11px;border-radius:50%;background:#fff;transition:left .2s}
.mov .tmpp.on i{background:#6152a0}
.mov .tmpp.on i::after{left:13px}
#wath-top .spov .sphm{display:block;font-style:normal;font-size:12px;font-weight:600;color:#a9925a;margin-top:1px}
#wath .suplist>.dn:hover,#wath .suplist>.dn:focus-within{z-index:8}
#wath li:has(>.pkt:hover),#wath li:has(>.pkt.on),#wath li:has(>.pkt:focus-visible){position:relative;z-index:8}
#wath .mi .tip,#wath .srtb .tip{background:#4b3f8c!important;color:#fff!important;border-radius:11px!important;padding:9px 12px!important;z-index:60!important;box-shadow:0 10px 28px rgba(45,32,100,.32),0 2px 6px rgba(45,32,100,.18)}
#wath #wath-recent .suplist>.dn{padding-right:48px!important}
#wath #wath-recent .dn .amtc{position:relative}
#wath #wath-recent .dn .amtc .x2{position:absolute;left:calc(100% + 8px);top:50%;transform:translateY(-50%);margin:0!important}
@media (max-width:600px){#wath #wath-recent .suplist>.dn{padding-right:40px!important}#wath #wath-recent .dn .amtc .x2{left:calc(100% + 5px)}}
.mov .bde .bdr{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 8px}
.mov .bde input.bdn{flex:1 1 220px;min-width:0;font-size:14.5px;font-weight:600;padding:9px 11px;border:1px solid #d9d1ee;border-radius:10px;background:#fff}
.mov .bde .bdn.bdfix{flex:1 1 220px;font-size:14.5px;font-weight:600;color:#3a3245}
.mov .bde .bdmo{display:inline-flex;align-items:center;gap:4px;font-weight:700;color:#6b6478}
.mov .bde .bdmo input{width:130px;font-size:14.5px;font-weight:600;padding:9px 11px;border:1px solid #d9d1ee;border-radius:10px;background:#fff;text-align:right}
.mov .bde .pkeo{display:flex;gap:4px;flex:none}
.mov .bde .pkeo button{height:36px;min-width:34px;padding:0 8px;border:1px solid #e0d9f2;border-radius:9px;background:#fff;color:#3a3245;cursor:pointer}
.mov .bde .pkeo button:disabled{opacity:.35;cursor:default}
.mov .bde .pkeo button.pkedel:hover{background:#fbecef;color:#8a1f3d;border-color:#f0c9d3}
.mov .bde .pkeadd{width:100%;border-style:dashed;margin-top:4px}
.mov .bde .bdtot{font-size:13px;color:#6b6478}.mov .bde .bdtot b{color:#1b1526;font-size:15px}
.mov .bde .pkei{border:1px solid #e6e0f4;border-radius:14px;padding:12px 14px;margin:0 0 12px;background:#fdfcff}
.mov .bde .pkei.off{opacity:.6}
.mov .bde .pkef{display:flex;flex-direction:column;gap:5px;margin:10px 0 0;font-size:13px;font-weight:700;color:#3a3245}
.mov .bde .pkef em{font-style:normal;font-weight:500;color:#8a849a;margin-left:6px}
.mov .bde .pkef textarea,.mov .bde .pkef input{font:inherit;font-weight:500;font-size:14px;padding:8px 11px;border:1px solid #d9d1ee;border-radius:10px;background:#fff;width:100%;box-sizing:border-box}
.mov .bdsum{display:flex;flex-wrap:wrap;gap:12px;margin-top:14px}
.mov .bdsum>div{flex:1 1 200px;padding:12px 14px;border-radius:12px;background:#f5f2fc;display:flex;flex-direction:column;gap:2px}
.mov .bdsum span{font-size:12.5px;color:#6b6478}.mov .bdsum b{font-size:20px;color:#1b1526}
.mov .tmname{border:0;background:none;padding:0;margin:0;font:inherit;color:inherit;cursor:pointer;text-align:left}.mov .tmname:hover b{color:#6152a0;text-decoration:underline;text-underline-offset:3px}
.mov .mgv{border:0;background:none;padding:3px 6px;margin:-3px -6px;border-radius:7px;font:inherit;font-weight:700;color:#33697f;cursor:pointer;text-decoration:underline dotted rgba(51,105,127,.45);text-underline-offset:3px}
.mov .mgv:hover{background:#e6f0f3}
.mov .mact{display:inline-block;margin:2px 4px 2px 0;border:0;border-radius:999px;padding:3px 9px;font:600 12px/1.3 inherit;background:#fbf0d4;color:#7a5f1c;cursor:pointer;white-space:nowrap}
.mov .mact:hover{background:#f6e3ae}
.mov .mseen{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:#3a3245;white-space:nowrap}
.mov .mseen i{width:8px;height:8px;border-radius:50%;background:#b9b3c6}
.mov .mseen.rec i{background:#2fa36b;box-shadow:0 0 0 3px rgba(47,163,107,.16)}
.mov .mseen.no{color:#8a849a}
.mov .gtab td{vertical-align:middle}
.mov .gtab .gact{white-space:nowrap;text-align:right}
.mov .gtab .gact .mlink{margin-left:10px}
.mov .gtab .gdel{color:#8a1f3d}
.mov .gtab input{font:inherit;font-size:14px;padding:7px 9px;border:1px solid #d9d1ee;border-radius:9px;background:#fff;max-width:170px}
.mov .gtab .bdmo input{width:100px}
.mov .bdmo{display:inline-flex;align-items:center;gap:4px;font-weight:700;color:#6b6478}
.mov .gaddf{margin-top:14px;padding:14px;border-radius:14px;background:#f5f2fc}
.mov .gaddr{display:flex;flex-wrap:wrap;gap:12px}
.mov .gaddr .mf{margin:0}
.mov .gaddr input{font:inherit;font-size:14px;padding:8px 10px;border:1px solid #d9d1ee;border-radius:9px;background:#fff}
.mov .gaddr .bdmo input{width:120px}
.mov ul.hlist{list-style:none;margin:12px 0 8px;padding:0}
.mov ul.hlist li{display:grid;grid-template-columns:150px 1fr auto;gap:12px;align-items:start;padding:9px 0;border-top:1px solid #eee9f7;font-size:13.5px;color:#3a3245}
.mov ul.hlist li::before{display:none}
.mov ul.hlist .hwhen{color:#6b6478;font-size:12.5px}
.mov ul.hlist .hch{display:block;margin-top:3px;font-size:12.5px;color:#6b6478}
.mov ul.hlist .hby{font-size:12.5px;color:#6152a0;font-weight:600;white-space:nowrap}
@media (max-width:640px){.mov ul.hlist li{grid-template-columns:1fr}.mov ul.hlist .hby{white-space:normal}}
#wath .msd .msnote{margin:10px 0 4px 28px;padding:10px 13px;border-radius:12px;background:#fbf3dc;border:1px solid #f0e0b0;color:#5c4a1e;font-size:14px;line-height:1.5}
#wath .msd .msnote a{color:#6152a0;font-weight:600}
#wath .suplist.scr{max-height:var(--suph);overflow-y:auto;overflow-x:hidden;overscroll-behavior-y:auto;scrollbar-width:thin;scrollbar-color:#cfc6ea transparent;-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 14px,#000 calc(100% - 28px),transparent 100%);mask-image:linear-gradient(to bottom,transparent 0,#000 14px,#000 calc(100% - 28px),transparent 100%);padding-top:6px;padding-bottom:22px}
#wath .suplist.scr::-webkit-scrollbar{width:6px}#wath .suplist.scr::-webkit-scrollbar-thumb{background:#cfc6ea;border-radius:6px}
#wath .suplist>.dn.bgrow.bgin .av{transition:transform .26s cubic-bezier(.2,1.6,.4,1)!important}
.mov .blg{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;align-items:start}
@media (max-width:860px){.mov .blg{grid-template-columns:1fr}}
.mov .blpv{padding:12px;border-radius:14px;background:#f5f2fc}
.mov .blem{border-radius:12px;overflow:hidden;border:1px solid #e3ddf3;background:#fff;margin-top:8px}
.mov .blemh{display:flex;flex-direction:column;gap:2px;padding:10px 14px;border-bottom:1px solid #ece7f7;font-size:12.5px;color:#6b6478}
.mov .blemh .blsub{font-size:14px;font-weight:700;color:#1b1526}
.mov .blph{margin:8px auto 0;max-width:300px;padding:18px 14px 14px;border-radius:26px;background:#fff;border:1px solid #e3ddf3}
.mov .blbub{display:inline-block;max-width:85%;padding:10px 13px;border-radius:18px 18px 18px 6px;background:#ece9f3;color:#1b1526;font-size:14px;line-height:1.4}
.mov .blphf{display:block;margin-top:8px;font-size:11.5px;color:#8a849a}
#wath-top .spov .sppv{max-width:380px}
#wath-top .spov .sppl{display:flex;flex-direction:column;align-items:center;text-align:center;gap:8px;padding:26px 10px 18px}
#wath-top .spov .spplk{width:76px;height:76px;display:flex;align-items:center;justify-content:center;background:#ece7f7;color:#6152a0;clip-path:polygon(50% 0,93.3% 25%,93.3% 75%,50% 100%,6.7% 75%,6.7% 25%)}
#wath-top .spov .sppl b{font-size:20px;color:#1b1526}#wath-top .spov .sppl>span:last-child{color:#6b6478;font-size:14px}
.mov .acln{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.mov .acln .aclp{font-size:13px;color:#6b6478;word-break:break-all}
.mov .acln input{flex:1 1 180px;min-width:0;font:inherit;font-size:15px;font-weight:600;padding:9px 11px;border:1px solid #d9d1ee;border-radius:10px;background:#fff}
.mov .acms{margin-top:6px}.mov .acms.ok{color:#2f7d55;font-weight:600}
.mov .aclk{display:flex;flex-direction:column;gap:3px;padding:10px 12px;border-radius:10px;background:#f5f2fc}.mov .aclk b{word-break:break-all}.mov .aclk span{font-size:13px;color:#6b6478}
.mov .acna{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px}
.mov .acna input{flex:1 1 220px;font:inherit;font-size:14px;padding:9px 11px;border:1px solid #d9d1ee;border-radius:10px}
:is(#wath,#wath-top) .cmpend{color:#a9925a;font-weight:700}
.mov tr.cmwait td{background:#fffaf0}
.mov .mchip:disabled{opacity:.55;cursor:default}
.mov .mfbar{display:flex;flex-direction:column;gap:8px;margin:12px 0 14px;padding:12px;border-radius:12px;background:#f7f5fc}
.mov .mfbar>div{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.mov .mfbar>div>span{font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#8a849a;min-width:92px}
.mov .mfbar select{font:inherit;font-size:13.5px;padding:6px 9px;border:1px solid #d9d1ee;border-radius:9px;background:#fff}
.mov .mchip.sm{padding:5px 11px;font-size:13px}
@media(min-width:801px){#wath-top .msgb{margin:0 0 4px 12px;padding-left:8px;border-left:2px solid #efeafb}#wath-top .msgb .msn{padding-left:10px}}
.mov .inbtabs{display:flex;gap:6px;margin:0 0 10px}
.mov .inbtabs button{display:inline-flex!important;align-items:center;gap:7px;border:1px solid #ddd5f0!important;background:#fff;border-radius:999px!important;padding:7px 16px!important;font:inherit;font-size:14.5px;font-weight:700;color:#3a3245;cursor:pointer}
.mov .inbtabs button.on{background:#6152a0!important;border-color:#6152a0!important;color:#fff!important}
.mov .inbtabs .inbn{font-size:12px;font-weight:700;opacity:.7}
#wath-top .spov .spq1:not(:has(blockquote)){display:none}
#wath-top .spov .spq1{margin:14px 0 4px;padding:16px 18px;border-radius:16px;background:#4b3f8c;color:#fff}
#wath-top .spov .spq1 .spql{display:block;font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#d9d1ee;margin-bottom:6px}
#wath-top .spov .spq1 blockquote{margin:0;padding:0;border:0;background:none;color:#fff;font-size:16px;line-height:1.5;font-weight:600;font-style:normal}
#wath-top .spov .spq1 blockquote+blockquote{margin-top:10px}
#wath-top .spov .spmi{margin:16px 0 8px;font-size:18px;font-weight:800;color:#1b1526}
#wath-top .spov .cnhive{position:relative;margin:8px 0 4px;max-width:100%}
#wath-top .spov .cnhx{position:absolute;padding:0;border:0;background:#b9abe0;cursor:pointer;clip-path:polygon(50% 0,93.3% 25%,93.3% 75%,50% 100%,6.7% 75%,6.7% 25%);display:flex;align-items:center;justify-content:center}
#wath-top .spov .cnhx .av,#wath-top .spov .cnhx .hxw{width:calc(100% - 4px)!important;height:calc(100% - 4px)!important;font-size:12px;clip-path:polygon(50% 0,93.3% 25%,93.3% 75%,50% 100%,6.7% 75%,6.7% 25%);padding:0!important;background:#cfc3ea}
#wath-top .spov .cnhx .hxw .av{width:100%!important;height:100%!important}
#wath-top .spov .cnhx:hover{background:#6152a0}
#wath-top .spov .cnby{margin:4px 0 6px;font-size:14.5px;color:#5b5368}
#wath-top .spov .cnsum{margin:6px 0 0;font-size:13.5px;color:#5b5368}
#wath-top .spov .cnvf{position:relative;width:100%;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background:#1b1526;margin-top:8px}
#wath-top .spov .cnvf iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
#wath-top .spov .cnvt{margin:6px 0 0;font-size:13.5px;color:#5b5368}
.mov .cnadd{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 14px}
.mov .cnadd input{flex:1 1 180px;min-width:0;font:inherit;font-size:14px;padding:9px 11px;border:1px solid #d9d1ee;border-radius:10px;background:#fff}
.mov .cnadd>span{font-size:14px;color:#6b6478}
.mov .cngrp{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;padding:10px 0;border-top:1px solid #eee9f7}
.mov .cngrp>b{min-width:180px}
.mov .cnchips{display:flex;flex-wrap:wrap;gap:6px}
.mov .cnchip{display:inline-flex;align-items:center;gap:6px;padding:4px 6px 4px 11px;border-radius:999px;background:#efeafb;font-size:13.5px;font-weight:600;color:#3f3478}
.mov .cnchip button{border:0;background:#fff;border-radius:50%;width:22px;height:22px;font-size:11px;cursor:pointer;color:#8a1f3d}
.mov .cnform{margin:0 0 14px;padding:14px;border-radius:14px;background:#f5f2fc}
.mov .cnrow{display:flex;flex-wrap:wrap;gap:12px}
.mov .cnrow .mf{margin:0 0 10px}
.mov .cnform input,.mov .cnform select{font:inherit;font-size:14px;padding:8px 10px;border:1px solid #d9d1ee;border-radius:9px;background:#fff}
.mov .cnform .bdmo input{width:120px}
#wath-top .spov .spq1 blockquote{display:-webkit-box;-webkit-line-clamp:6;-webkit-box-orient:vertical;overflow:hidden;cursor:pointer}
#wath-top .spov .spq1.open blockquote{display:block;-webkit-line-clamp:unset}
#wath-top .spov .spchi{margin:2px 0 8px;font-size:14.5px;line-height:1.5;color:#5b5368}
.mov .cnform .mf .bdmo{display:inline-flex!important;flex-direction:row}
#wath-top .spov details.spchd{background:#fffaf0;border:1px solid #f0e3bf;border-radius:12px;margin:0 0 8px;padding:0}
#wath-top .spov details.spchd summary{list-style:none;cursor:pointer;display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;padding:11px 14px}
#wath-top .spov details.spchd summary::-webkit-details-marker{display:none}
#wath-top .spov details.spchd summary>span:not(.spchn){margin-left:auto;font-size:14px;color:#8a6d2a}
#wath-top .spov .spchn{flex-basis:100%;font-size:14px;font-weight:700;color:#6152a0;text-decoration:underline dotted rgba(97,82,160,.4);text-underline-offset:3px}
#wath-top .spov .spchn .chev{vertical-align:-1px;transition:transform .2s}
#wath-top .spov details.spchd[open] .spchn .chev{transform:rotate(180deg)}
#wath-top .spov ul.spchl{list-style:none;margin:0;padding:0 14px 10px;max-height:260px;overflow:auto}
#wath-top .spov ul.spchl li{display:flex;justify-content:space-between;gap:10px;padding:6px 0;border-top:1px solid #f3ead2;font-size:14px}
#wath-top .spov ul.spchl li::before{display:none}
#wath-top .spov ul.spchl b{color:#a9925a}
#wath-top .spov .spchx{margin:0;padding:0 14px 10px;font-size:13px;color:#8a849a}
#wath-top .cngrid,.mov .cngrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:6px;margin-top:8px}
.mov .cngrid.sm{grid-template-columns:repeat(auto-fill,minmax(84px,1fr))}
#wath-top .cnph,.mov .cnph{position:relative;display:block;padding:0;border:0;border-radius:10px;overflow:hidden;aspect-ratio:1;background:#ece7f7;cursor:pointer}
#wath-top .cnph img,.mov .cnph img{width:100%;height:100%;object-fit:cover;display:block}
.mov .cnpx{position:absolute;top:4px;right:4px;width:26px;height:26px;border-radius:50%;border:0;background:rgba(255,255,255,.92);color:#8a1f3d;cursor:pointer;font-size:12px}
#wath-top .galov{background:rgba(15,10,25,.88)}
#wath-top .galov .galw{position:relative;max-width:92vw;max-height:88vh;display:flex;flex-direction:column;align-items:center;margin:auto}
#wath-top .galov .galw img{max-width:92vw;max-height:80vh;border-radius:12px;object-fit:contain;cursor:zoom-out}
#wath-top .galov .galw p{color:#fff;margin:10px 0 0;font-size:15px}
#wath-top .galov .bovx{position:absolute;top:-14px;right:-14px}
.spmt{background:linear-gradient(135deg,#fff8e6,#fdf0cf);border:1px solid #ecd9a3;border-radius:14px;padding:14px 16px;margin:12px 0 4px;display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px}.spmt p{margin:0;flex:1 1 220px;font-size:15px;line-height:1.45;color:#3a3048}.spmt b{color:#1b1526}.spmt .btn{flex:0 0 auto}
.spchh{padding:10px 14px 2px;overflow-x:auto}.spchh .cnhive{margin:0}
.mpgrid{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:18px;align-items:start}.mpside .mcard{margin-bottom:18px}.mpprev{position:sticky;top:12px}.mpprev .spin{margin-top:12px}.mpprev .spin .bovh{margin-top:0}.mpnote{background:#f4f1fa;border-radius:10px;padding:10px 12px;font-size:14px;margin:10px 0 0;color:#3a3048}
.mpck{display:flex!important;align-items:center;gap:8px;margin:6px 0!important}.mpact{display:grid;gap:14px}.mpact>div{display:grid;gap:4px;padding-bottom:14px;border-bottom:1px solid #eee8f5}.mpact>div:last-child{border:0;padding-bottom:0}.mpact b{color:#1b1526;font-size:16px}.mpact span{font-size:14px;color:#5b5368;line-height:1.45}.mpact .btn{justify-self:start;margin-top:6px}
@media(max-width:820px){.mpgrid{grid-template-columns:1fr}.mpprev{position:static}}
.spin .bovc{max-width:none!important;max-height:none!important;box-shadow:none!important;padding:0!important;overflow:visible!important;border-radius:0;animation:none}.mpprev .spin{margin-top:14px}
.crsub{display:block;margin-top:4px}.crsub .mlink,.msub .mlink[data-crg]{font:inherit;padding:0}
:is(#wath,#wath-top) .crgov{z-index:2147483000}.crg{max-width:560px!important}.crg h3{margin:4px 0 8px;font-size:22px;color:#1b1526}.crg ol{margin:12px 0;padding-left:20px;display:grid;gap:9px}.crg li{font-size:15px;line-height:1.5;color:#3a3048}.crg li b{color:#1b1526}.crg .crgq{font-size:14px!important;color:#6b6478!important}
.pch{border-top:1px solid #eee8f5;padding:12px 0}.pch.new{background:#faf7ff;margin:0 -12px;padding:12px;border-radius:10px}.pchh{display:flex;flex-wrap:wrap;gap:4px 8px;align-items:baseline;font-size:15px}.pchh span{margin-left:auto;font-size:13px;color:#6b6478}.pch ul{margin:6px 0 4px;padding-left:18px;font-size:14px;line-height:1.5;color:#3a3048}.pch li i{color:#8a8296}
.mov .adots{position:relative;display:inline-flex}
.mov .amng button.adotb{width:36px!important;height:36px!important;min-width:36px;box-sizing:border-box;flex:none;border-radius:50%;border:1px solid rgba(27,21,38,.16);background:#fff;color:#1b1526;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;padding:0}
.mov .amng button.adotb:hover{background:#f1eef8}
.mov .amng .mbtns{display:inline-flex;align-items:center;gap:14px}
.mov .amng .mbtns>.mlink{margin:0;padding:0;line-height:36px}
.mov .amng button.adotb{border-radius:50%!important;border:1px solid rgba(27,21,38,.16)!important;background:#fff!important}
.mov .adotm{position:absolute;right:0;top:42px;z-index:20;min-width:240px;background:#fff;border:1px solid rgba(27,21,38,.14);border-radius:10px;box-shadow:0 10px 30px rgba(27,21,38,.14);padding:6px;display:flex;flex-direction:column}
.mov .adotm button{all:unset;cursor:pointer;padding:10px 12px;border-radius:8px;font-size:15px;color:#1b1526}
.mov .adotm button:hover,.mov .adotm button:focus-visible{background:#f1eef8}
.mov .aphr{display:flex;align-items:center;gap:16px;margin:4px 0 12px}
.mov .aphv{width:72px;height:72px;border-radius:50%;background:#e4dff2;color:#5a4f8f;font-weight:700;font-size:22px;display:inline-flex;align-items:center;justify-content:center;overflow:hidden;flex:none}
.mov .aphv img{width:100%;height:100%;object-fit:cover}
.mov .aphb{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.mov .aphb label.btn{cursor:pointer;display:inline-flex;align-items:center;justify-content:center;line-height:1.2;padding:10px 18px;min-height:0;height:auto;width:auto}
.mov .aflag{border-color:#c9b8ee;background:#f6f2fd}
.mov .aflag .mrow{gap:12px;margin-top:6px}
.mov .mdd{margin-top:10px;max-width:420px;border:1px solid rgba(27,21,38,.16);border-radius:10px;background:#fff}
.mov .mdd>summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 14px;font-size:15px;color:#1b1526}
.mov .mdd>summary::-webkit-details-marker{display:none}
.mov .mdd[open]>summary svg{transform:rotate(180deg)}
.mov .mdd .mddl{padding:2px 14px 10px;border-top:1px solid rgba(27,21,38,.08)}
.mov .mdd .mddl .mck{display:flex;margin:8px 0}
:is(#wath,#wath-top) .subnav .snl .snd{flex:none;align-self:center;width:1px;height:18px;margin:0 8px;background:rgba(27,21,38,.24)}
@media(max-width:700px){#wath[data-tabv] .cols.second{padding-top:28px}}
"""

# Nov 17 4:06pm (Nirvan): a purple hexagon outline around the filmmaker photos so they read as molecules
import re as _re
# Nov 17 4:07pm (Nirvan): the crew opens above the toggle, which then reads Collapse
_c0=home.find('<details class="crew"><summary>');_c1=home.find('</summary>',_c0)+len('</summary>');_c2=home.find('</details>',_c1)
assert _c0>0 and _c2>_c1
_chv=home[_c0:_c1][home[_c0:_c1].find('<svg'):home[_c0:_c1].find('</svg>')+6]
home=home[:_c0]+'<div class="crew"><div class="crewb" hidden>'+home[_c1:_c2]+'</div><button type="button" class="crewt" aria-expanded="false"><span class="crs">See the full crew</span><span class="crc">Collapse</span>'+_chv+'</button></div>'+home[_c2+len('</details>'):]
home=home.replace('<div class="tmc tmn"><span class="tmp tmi" aria-hidden="true">JC</span><b>Juli Crockett</b><span>Assistant to the Director</span></div>','<button class="tmc tmn" data-bio="juli" aria-haspopup="dialog"><span class="tmp tmi" aria-hidden="true">JC</span><b>Juli Crockett</b><span>Assistant to the Director</span></button>')
home=_re.sub(r'(<img class="tmp"[^>]*>|<(span|i) class="tmp tmi"[^>]*>[^<]*</\2>)',r'<span class="tmw">\1</span>',home)
out='<!-- WHAT A TRIP home page (test build). Source: nirvanmullick/whatatrip-donor-wall home-page/home-block.html -->\n<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800&display=swap" rel="stylesheet">\n<style>\n'+scoped+extra+'</style>\n<div id="wath">'+home+'</div>\n<div id="wath-top">'+top+'</div>\n<script>\n'+js+'\n</script>\n'
os.makedirs('../img',exist_ok=True)
# Nov 17 3pm (Nirvan): the 'Start a Matching Challenge' pop-up from the /matching page (same bundle the donate page carries)
out+='\n'+open('mc-bundle.html').read()+'\n'
open('../home-block.html','w').write(out)
print(len(out))
