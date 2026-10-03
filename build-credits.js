// build-credits.js -- ONE SMALL PAGE PER CREDIT, so a texted link says whose credit it is.
//
// Nirvan, 2026-10-02: "when you text it, it says the name and says 'donor to What a Trip' ...
// not so generic as just 'What a Trip' with the picture of Rick Doblin".
//
// A text message (or Slack, WhatsApp, Facebook...) builds its preview from the tags at the top of
// the page a link points to. whatatrip.com/donors#donor-david-choe is, to them, just /donors --
// the part after # is never sent -- so every credit got the same "What a Trip" preview.
// This script writes site/<name>.html for every credit, served by GitHub Pages at
//   https://credits.whatatrip.com/<name>
// Each one carries that person's own preview ("David Choe -- Donor to What a Trip" plus a card
// image with their name) and sends a reader straight on to their credit on whatatrip.com/donors.
//
// Who gets a page: everyone in credits-seed.json (every credit on the wall when it was made), plus
// every name and anonymous gift in master-donors.json (so new donors get theirs automatically).
// Card images (site/img/<name>.png) are only drawn when new or changed.
//
// Run: node build-credits.js   (needs @resvg/resvg-js for the images; without it the pages still
// build and use img/_wall.png)

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';

const SITE = 'https://whatatrip.com/donors';
// OUR OWN ADDRESS, so a link sent today keeps working if the pages ever move off GitHub: point
// credits.whatatrip.com at the new home and every /<name> address still answers.
const BASE = 'https://credits.whatatrip.com/';
const OUT = 'site';   // GitHub Pages publishes this folder (the deploy step in scrape.yml)
const FILM_LINE = 'A documentary about Rick Doblin and the fight to legalize psychedelic therapy';

// the donor wall's own address rules (donorSlug(keyOf(name)) in the page code) -- must match
const keyOf = (n) => String(n == null ? '' : n).trim().toLowerCase();
const slugOf = (id) => String(id || '').toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const caDate = (ts) => new Date(ts).toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/* ---------- who has a credit ---------- */
const credits = new Map();   // slug -> { name, kind: 'donor' | 'supporter' | 'anon' | 'community' }
function add(slug, name, kind) {
  if (!slug) return;
  const had = credits.get(slug);
  if (had && !(had.kind === 'supporter' && kind === 'donor')) return;
  credits.set(slug, { name, kind });
}
add('unnamed-community-credit', 'Unnamed Community Credit', 'community');
if (existsSync('credits-seed.json')) {
  for (const c of JSON.parse(readFileSync('credits-seed.json', 'utf8'))) {
    if (c.slug === 'unnamed-community-credit') continue;
    if (/^anon-/.test(c.slug)) add(c.slug, null, 'anon');
    else add(c.slug, c.name, c.gave ? 'donor' : 'supporter');
  }
}
if (existsSync('master-donors.json')) {
  const anonSeen = {};
  const gifts = (JSON.parse(readFileSync('master-donors.json', 'utf8')).gifts || []).slice()
    .sort((a, b) => new Date(a.date) - new Date(b.date));
  for (const g of gifts) {
    if (g.anonymous || !g.name) {
      if (!g.date) continue;
      let id = 'anon-' + (g.amount || 0) + '-' + caDate(g.date);
      anonSeen[id] = (anonSeen[id] || 0) + 1;
      if (anonSeen[id] > 1) id += '-' + anonSeen[id];
      add(id, null, 'anon');
    } else add(slugOf(keyOf(g.name)), g.name, 'donor');
  }
}

/* ---------- the words ---------- */
function words(c) {
  if (c.kind === 'community') return {
    big: 'Unnamed Community Credit', sub: 'Supporters of What a Trip',
    title: 'The Unnamed Community Credit — What a Trip',
    desc: 'Everyone who gave to What a Trip without a named credit, thanked together on the donor wall. ' + FILM_LINE + '.' };
  if (c.kind === 'anon') return {
    big: 'Anonymous', sub: 'Donor to What a Trip',
    title: 'An anonymous donor to What a Trip',
    desc: 'An anonymous gift on the What a Trip donor wall. ' + FILM_LINE + '.' };
  const role = c.kind === 'supporter' ? 'Supporter of What a Trip' : 'Donor to What a Trip';
  return { big: c.name, sub: role, title: c.name + ' — ' + role,
    desc: c.name + '’s credit on the What a Trip donor wall. ' + FILM_LINE + '.' };
}

/* ---------- the card image (1200 x 630, the size every preview uses) ---------- */
function cardSVG(w) {
  // Source Sans Bold is about 0.5em a letter; shrink a long name to fit 1040px, then wrap if still huge
  let size = Math.min(104, Math.floor(1040 / (Math.max(w.big.length, 6) * 0.57)));
  let lines = [w.big];
  if (size < 64 && w.big.includes(' ')) {
    const parts = w.big.split(' '); let best = null;
    for (let i = 1; i < parts.length; i++) {
      const a = parts.slice(0, i).join(' '), b = parts.slice(i).join(' ');
      const m = Math.max(a.length, b.length); if (!best || m < best.m) best = { a, b, m };
    }
    lines = [best.a, best.b]; size = Math.min(96, Math.floor(1040 / (Math.max(best.m, 6) * 0.57)));
  }
  const nameY = lines.length === 1 ? 330 : 270;
  const nameSVG = lines.map((t, i) => `<text x="80" y="${nameY + i * size * 1.05}" font-family="Source Sans 3" font-weight="700" font-size="${size}" fill="#1f2430">${esc(t)}</text>`).join('');
  const subY = nameY + (lines.length - 1) * size * 1.05 + 78;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#6f74aa"/><stop offset="0.55" stop-color="#5a93af"/><stop offset="1" stop-color="#d9a441"/></linearGradient></defs>
  <rect width="1200" height="630" fill="#fbf9f5"/>
  <rect width="1200" height="14" fill="url(#g)"/>
  <text x="80" y="112" font-family="Source Sans 3" font-weight="700" font-size="30" letter-spacing="7" fill="#33414f">WHAT A TRIP</text>
  <text x="80" y="150" font-family="Source Sans 3" font-weight="600" font-size="24" letter-spacing="4" fill="#7d8794">DONOR WALL</text>
  ${nameSVG}
  <text x="80" y="${subY}" font-family="Source Sans 3" font-weight="600" font-size="46" fill="#5a93af">${esc(w.sub)}</text>
  <rect x="80" y="520" width="1040" height="2" fill="#e9ecf1"/>
  <text x="80" y="570" font-family="Source Sans 3" font-weight="400" font-size="27" fill="#45525f">${esc(FILM_LINE)}</text>
</svg>`;
}

let Resvg = null;
try { ({ Resvg } = await import('@resvg/resvg-js')); } catch (e) { console.log('(no @resvg/resvg-js -- pages build without new images)'); }
function png(svg) {
  return new Resvg(svg, { font: { loadSystemFonts: false, defaultFontFamily: 'Source Sans 3',
    fontFiles: ['fonts/SourceSans3-Regular.ttf', 'fonts/SourceSans3-Semibold.ttf', 'fonts/SourceSans3-Bold.ttf'] } }).render().asPng();
}

/* ---------- the page ---------- */
function page(slug, w, img) {
  const to = SITE + '#donor-' + slug;
  return `<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(w.title)}</title>
<meta name="description" content="${esc(w.desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="What a Trip">
<meta property="og:title" content="${esc(w.title)}">
<meta property="og:description" content="${esc(w.desc)}">
<meta property="og:url" content="${BASE + slug}">
<meta property="og:image" content="${BASE + img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="${esc(w.title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(w.title)}">
<meta name="twitter:description" content="${esc(w.desc)}">
<meta name="twitter:image" content="${BASE + img}">
<meta name="robots" content="noindex">
<script>
  /* a person goes straight on to the credit; a link-preview reader stays and reads the tags above */
  if (!/bot|crawl|spider|facebookexternalhit|facebot|twitterbot|slack|whatsapp|telegram|discord|linkedin|embedly|preview|pinterest|skype|google-structured/i.test(navigator.userAgent))
    location.replace(${JSON.stringify(to)});
</script>
<style>body{font-family:"Source Sans 3","Source Sans Pro",-apple-system,Helvetica,Arial,sans-serif;background:#fbf9f5;color:#1f2430;display:flex;min-height:90vh;align-items:center;justify-content:center;text-align:center;padding:16px}a{color:#5a93af;font-weight:600}</style>
</head><body><p>${esc(w.big)} &middot; ${esc(w.sub)}<br><br><a href="${esc(to)}">See the credit on whatatrip.com &rarr;</a></p></body></html>
`;
}

/* ---------- write ---------- */
mkdirSync(OUT + '/img', { recursive: true });
const manifestPath = OUT + '/img/manifest.json';
const manifest = existsSync(manifestPath) ? JSON.parse(readFileSync(manifestPath, 'utf8')) : {};
const wallW = { big: 'Donor Wall', sub: 'Thank you to everyone who made What a Trip possible' };
if (Resvg && manifest._wall !== JSON.stringify(wallW)) { writeFileSync(OUT + '/img/_wall.png', png(cardSVG(wallW))); manifest._wall = JSON.stringify(wallW); }

let pages = 0, drawn = 0;
for (const [slug, c] of credits) {
  const w = words(c);
  const sig = JSON.stringify([w.big, w.sub, 3]);
  // anonymous gifts all share one picture
  const imgName = c.kind === 'anon' ? '_anonymous.png' : slug + '.png';
  if (Resvg && manifest[imgName] !== sig) { writeFileSync(OUT + '/img/' + imgName, png(cardSVG(w))); manifest[imgName] = sig; drawn++; }
  const img = existsSync(OUT + '/img/' + imgName) ? 'img/' + imgName : 'img/_wall.png';
  const html = page(slug, w, img);
  const f = OUT + '/' + slug + '.html';
  if (!existsSync(f) || readFileSync(f, 'utf8') !== html) { writeFileSync(f, html); pages++; }
}
writeFileSync(manifestPath, JSON.stringify(manifest, null, 1) + '\n');
writeFileSync(OUT + '/ok.txt', 'ok\n');   // the donor wall checks for this before handing out these links

// any address without a page yet (a gift newer than the last run) still lands on the wall
writeFileSync(OUT + '/404.html', `<!doctype html><html><head><meta charset="utf-8"><title>What a Trip — Donor Wall</title>
<meta property="og:title" content="What a Trip — Donor Wall"><meta property="og:image" content="${BASE}img/_wall.png">
<script>var m=location.pathname.match(/\\/([a-z0-9-]+?)(?:\\.html)?\\/?$/);location.replace(${JSON.stringify(SITE)}+(m?'#donor-'+m[1]:''));</script>
</head><body><a href="${SITE}">What a Trip donor wall</a></body></html>
`);
writeFileSync(OUT + '/.nojekyll', '');
writeFileSync(OUT + '/CNAME', 'credits.whatatrip.com\n');
// every address ever handed out, so any future system can keep answering the same links
// (an address is never dropped: a renamed credit's old page stays, and stays in this list)
const idxPath = OUT + '/credits-index.json';
const idx = {};
try { for (const e of JSON.parse(readFileSync(idxPath, 'utf8'))) idx[e.slug] = e; } catch (e) {}
for (const [slug, c] of credits) idx[slug] = { slug, name: c.name, kind: c.kind, url: BASE + slug, goes_to: SITE + '#donor-' + slug };
writeFileSync(idxPath, JSON.stringify(Object.values(idx).sort((a, b) => a.slug < b.slug ? -1 : 1), null, 1) + '\n');
console.log(`${credits.size} credits: ${pages} pages written, ${drawn} images drawn`);
