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
.wath-chip-arr{display:inline-flex;align-items:center;align-self:stretch;padding:6px 0 6px 8px;margin:-6px 0;border-left:1px solid rgba(255,255,255,.45);cursor:pointer}
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
#wath-top .msmain2{min-width:0}
#wath-top select[data-lrole],#wath-top select[data-rstatus]{font:inherit;font-size:15px;padding:8px 10px;border:1px solid #cfc7e8;border-radius:10px;background:#fff;color:#1b1526;flex:none;max-width:100%}
#wath-top .mslab{display:block;font-size:11px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#6152a0;padding:8px 11px 4px}
#wath-top .mslab.tm{border-top:1px solid #ebe7f5;margin-top:6px;padding-top:14px}
#wath-top .msn.msw{display:none}
@media(max-width:1000px){#wath-top .mme>span.marr{display:inline-flex}}
#wath-top .marr{display:inline-flex;align-items:center;align-self:stretch;padding:0 2px 0 9px;margin:-4px 0 -4px 2px;border-left:1px solid rgba(255,255,255,.4)}
@media(max-width:800px){#wath-top .mslab{display:none}#wath-top .msn.msw{display:block;border:1px solid #cfc7e8;color:#6152a0;font-weight:700;border-radius:999px;margin-right:4px}#wath-top .msnav[data-grp=me] .g-team,#wath-top .msnav[data-grp=team] .g-me{display:none}}
#wath-top .msn.par{font-weight:800;color:#6152a0}
#wath-top .msn.sub{padding-left:24px;font-size:14px}
@media(max-width:800px){#wath-top .msn.sub{padding-left:11px}}
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
home=home[:a]+'<a class="video" href="/trailer" data-trailer aria-label="Play the trailer" style="--ph:url(https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/876eaca8-ad5c-42e5-8c35-3a37a50f8e00/rick_doblin_+purple.jpg?format=2500w)"><span class="vk" aria-hidden="true"><i class="k1"></i><i class="k2"></i><i class="k3"></i></span><span class="vt" aria-hidden="true"><em>From Executive Producer <strong>Darren Aronofsky</strong></em><b>WHAT A TRIP</b><i>The Rick Doblin Story</i><span class="vb">A film by <strong>Nirvan Mullick</strong></span></span><span class="play"><svg aria-hidden="true" width="26" height="26" viewBox="0 0 24 24"><path d="M7 4l14 8-14 8z" fill="#6152a0"/></svg><span>Watch the trailer</span></span></a>'+home[b:]
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
home=home[:a]+'<div class="subnav"><div class="wrap"><div class="snl"><a href="#wath" data-top>Campaign</a><a href="#wath-story">Story</a><a href="#wath-recent">Community</a><a href="#wath-perks">Perks</a><a href="#wath-team">Filmmakers</a><a href="#wath-budget">Budget</a><a href="#wath-impact">Impact</a><a href="#wath-faq">FAQs</a><a href="#wath-comments">Comments<sup class="cnt" data-cnt="com"></sup></a><a href="#wath-updates">Updates<sup class="cnt" data-cnt="upd"></sup></a></div><button class="btn pri" data-give>Donate</button></div></div>'+home[e:]
stub=lambda i,t,x:'<section class="sec" id="wath-%s"><h2>%s <span class="soon">Coming soon</span></h2><p class="sub">%s</p></section>'%(i,t,x)
a=home.index('<section class="sec" id="wath-recent">')
home=home[:a]+'<section class="sec" id="wath-team"><h2>Filmmakers</h2><div class="tm5"><button class="tmc" data-bio="nirvan" aria-haspopup="dialog"><img class="tmp" loading="lazy" alt="" width="84" height="84" style="object-position:50% 30%" src="https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/1555433778223-YF44T2R77O4M3UTN9J4O/nirvan_bw.jpg?format=300w"><b>Nirvan Mullick</b><span>Director, Producer</span></button><button class="tmc" data-bio="dream" aria-haspopup="dialog"><img class="tmp" loading="lazy" alt="" width="84" height="84" style="object-position:50% 25%" src="https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/1555431858411-Z2NV78ZE78PGR5BTJ8GZ/Dream_Mullick.jpg?format=300w"><b>Dream Mullick</b><span>Producer</span></button><button class="tmc" data-bio="darren" aria-haspopup="dialog"><img class="tmp" loading="lazy" alt="" width="84" height="84" style="object-position:50% 30%" src="https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/9b0e790b-0826-45ce-b5e3-2b2b28f01dbf/darren_aronofsky.jpeg?format=300w"><b>Darren Aronofsky</b><span>Executive Producer</span></button><button class="tmc" data-bio="jeffrey" aria-haspopup="dialog"><img class="tmp" loading="lazy" alt="" width="84" height="84" style="object-position:50% 30%" src="https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/1555431789123-2KB2SGD4YE7YE4AD0JE5/IMG_20181217_162143.jpg?format=300w"><b>Jeffrey Schneider</b><span>Cinematographer</span></button><button class="tmc" data-bio="vickie" aria-haspopup="dialog"><img class="tmp" loading="lazy" alt="" width="84" height="84" style="object-position:50% 25%" src="https://images.squarespace-cdn.com/content/v1/5cb1600577b90384f9245e9e/93eff408-ea57-4c5f-b815-a4908353c04b/Vickie_BW.png?format=300w"><b>Vickie Curtis</b><span>Story Consultant</span></button></div><a href="/about" style="font-weight:700">Read about the team</a></section>'+home[a:]
a=home.index('<section class="sec"><div class="card tnd" data-tnd>')
home=home[:a]+'<section class="sec" id="wath-faq"><h2>FAQs</h2><div class="card" style="padding:6px 20px"><details class="fq"><summary>What is the film about?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p><em>What a Trip</em> follows Rick Doblin and MAPS, the organization he founded, across a 40+ year effort to bring psychedelic therapy back into culture.</p></details><details class="fq"><summary>Who is making it?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>The film is directed by Nirvan Mullick, produced by Dream Mullick, and executive produced by Darren Aronofsky.</p></details><details class="fq"><summary>How long has it been in the works?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>Twelve years. We have been filming with Rick since 2014.</p></details><details class="fq"><summary>Where is the film now?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>Filming is largely done and we are editing the rough cut, one act at a time. The <a href="#wath-budget">budget section</a> shows which milestone we are funding right now.</p></details><details class="fq"><summary>When will it be finished?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>We are aiming for late 2027. The exact timing depends on how quickly the edit is funded.</p></details><details class="fq"><summary>How is the film funded?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>By donations, together with years of unpaid work and investment from the filmmakers. The total budget is $3.4M: $1.8M already raised and invested since 2014, $700K for the rough cut, and $900K for the final cut.</p></details><details class="fq"><summary>What does my donation pay for?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>Right now, editing. Every $50 covers about one hour of an editor&rsquo;s time. The budget section lists what each milestone pays for.</p></details><details class="fq"><summary>Is my donation tax-deductible?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>Yes. Donations go through Creative Visions Foundation, our nonprofit fiscal sponsor, and are tax-deductible, less the fair market value of any perk you receive.</p></details><details class="fq"><summary>What is TRUTH Not DARE?<svg class="chev" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg></summary><p>It is the film&rsquo;s impact campaign, launching alongside the film. It offers honest education about the real risks and benefits of psychedelics. <a href="/impact">Read more</a>.</p></details></div></section>'+home[a:].replace('<section class="sec"><div class="card tnd" data-tnd>','<section class="sec" id="wath-impact"><div class="card tnd" data-tnd>',1)
a=home.index('<section class="sec" id="wath-store">')
home=home[:a]+'<section class="sec" id="wath-updates"><h2>Updates<sup class="cnt" data-cnt="upd"></sup></h2><p class="sub">News from the filmmakers as the film takes shape. Some updates are for supporters at certain levels.</p><div class="upx"><span><b>$500+</b> Private teaser and edit-room updates</span><span><b>$5K+</b> Zoom with the filmmakers</span><span><b>$25K+</b> Zoom with Rick Doblin</span><span class="soon">Member sign-in coming soon</span></div><div data-updates></div></section>'+home[a:]
old='A documentary about Rick Doblin, MAPS and the fight to legalize psychedelic therapy.'
assert old in home
home=home.replace(old,'A documentary following Rick&rsquo;s 40+ year journey with MAPS to bring psychedelics back into culture.')

# ---- page order follows the submenu (Nov 15): Story, Community | Perks | Filmmakers, Budget, (Matching), Impact, FAQs, Updates, Comments, Store, Access ----
def cut(i):
    global home
    a=home.index('<section class="sec" id="wath-%s"'%i); e=home.index('</section>',a)+10
    s=home[a:e]; home=home[:a]+home[e:]; return s
S={i:cut(i) for i in ['team','budget','challenges','impact','faq','updates','store','access']}
S['comments']='<section class="sec" id="wath-comments"><h2>Comments<sup class="cnt" data-cnt="com"></sup></h2><p class="sub">What supporters are saying.</p><div class="card" style="padding:10px 20px 16px" data-comments></div></section>'
mark='<div class="wrap cols second"><div class="stack">'
assert mark in home
home=home.replace(mark,mark+''.join(S[i] for i in ['team','budget','challenges','impact','faq','comments','updates']),1)
home=home.replace('<div class="match" data-matchline></div>','<div class="kstats" data-kstats></div><div class="match" data-matchline></div>',1)
assert 'data-kstats' in home
chart=P[P.index('<div class="ov" id="ov-chart">'):P.index('<div class="toast"')]
top='<div class="mcta"><span class="mctat"><b data-mneed></b><span>still needed</span></span><button class="btn pri" data-give>Donate</button></div><button class="pvb" data-pv aria-label="Preview this page as it looks on a phone"><svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="2" width="10" height="20" rx="2.5"/><path d="M11 18h2"/></svg>Phone preview</button><div class="pvo" data-pvo><div class="pvh"><b>Phone preview</b><button class="btn" data-pvx>Back to desktop</button></div><div class="pvf" data-pvf></div></div><a id="wath-plg" data-plg-action="donate" data-widget-id="6GNakp1GtmAa92RH" href="/donate" hidden>Donate</a>'+chart+'<div class="toast" id="wath-toast" role="status"></div>'
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
_shr=('<div class="shr"><span class="shl">Share our campaign</span><div class="shb">'
 +'<a class="sh1" aria-label="Share on Facebook" title="Facebook" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u='+_u+'">'+_ic('<path d="M13.6 21v-7.6h2.55l.4-3H13.6V8.5c0-.87.25-1.46 1.5-1.46h1.6V4.36c-.28-.04-1.23-.12-2.33-.12-2.3 0-3.87 1.4-3.87 3.98v2.2H7.9v3h2.6V21z"/>')+'</a>'
 +'<a class="sh1" aria-label="Share on X" title="X" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?url='+_u+'&text='+_t+'">'+_ic('<path d="M17.75 3h3.07l-6.7 7.66L22 21h-6.17l-4.83-6.32L5.47 21H2.4l7.17-8.2L2 3h6.33l4.37 5.78zm-1.08 16.17h1.7L7.4 4.74H5.58z"/>')+'</a>'
 +'<a class="sh1" aria-label="Share by email" title="Email" href="mailto:?subject=WHAT%20A%20TRIP%3A%20The%20Rick%20Doblin%20Story&body='+_t+'%0A%0A'+_u+'">'+_ic('<path d="M3 6.6A1.6 1.6 0 0 1 4.6 5h14.8A1.6 1.6 0 0 1 21 6.6v.25l-9 5.6-9-5.6zm0 2.6v8.2A1.6 1.6 0 0 0 4.6 19h14.8a1.6 1.6 0 0 0 1.6-1.6V9.2l-9 5.6z"/>')+'</a>'
 +'<button class="sh1" aria-label="Copy the link" title="Copy link" data-copy="https://whatatrip.com"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg></button>'
 +'</div><a class="shc" href="/matching">Start a matching challenge &rarr;</a></div>')
_tax='<div class="taxn"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.5"/><path d="M7.5 12.5l3 3 6-6.5"/></svg><div><b>Donations are tax-deductible</b><span>Made through Creative Visions, our nonprofit fiscal sponsor. Deductible less the fair market value of any perk you receive.</span></div></div>'
home=home.replace(_end,_tax+'</div>'+_shr+'</div>',1)

_c='<div class="chs" data-challenges></div>'
assert home.count(_c)==1
home=home.replace(_c,_c+'<div class="chf"><a class="btn" href="/matching">See all challenges</a><a class="btn pri" href="/contact">Start a challenge</a></div>')

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

out='<!-- WHAT A TRIP home page (test build). Source: nirvanmullick/whatatrip-donor-wall home-page/home-block.html -->\n<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800&display=swap" rel="stylesheet">\n<style>\n'+scoped+extra+'</style>\n<div id="wath">'+home+'</div>\n<div id="wath-top">'+top+'</div>\n<script>\n'+js+'\n</script>\n'
os.makedirs('../img',exist_ok=True)
open('../home-block.html','w').write(out)
print(len(out))
