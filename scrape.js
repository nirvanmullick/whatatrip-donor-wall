// ============================================================================
//  What a Trip — Pledge donor feed  ->  donors.json            (v2, 2026-09-28)
//
//  WHY THIS REPLACES THE OLD SCRAPER
//  The old script opened pledge.to/whatatrip in a headless browser and read the
//  rows on screen. Pledge only renders ~10 rows until you scroll, and with a
//  matching challenge running every gift takes TWO rows (the gift + its
//  "Match" row) -- so the site only ever saw the 5 newest gifts. On 2026-09-27
//  that dropped Thomas Aarts, Vincent Nance, Juli Crockett and Anthony Greenberg.
//
//  WHAT THIS DOES
//  * Reads the same JSON feed Pledge's own page uses when you scroll its list
//    (GET https://www.pledge.to/whatatrip?last_id=<id>, Accept: application/json).
//    No browser, no scrolling, no guessing at page markup. Public, no login.
//  * Walks page by page (about 25 rows each) until BOTH are true:
//      - it has read at least MIN_GIFTS real gifts (default 20), and
//      - it has reached a gift already in donors.json.
//    FULL_SYNC=1 (daily run, or tick the box on a manual run) walks the whole list.
//  * Match rows are folded into the gift they match: one row per real gift, with
//    `matched: true` when a sponsor matched it. No more doubled rows.
//  * Respects each donor's privacy choice: if Pledge shows them as Anonymous, the
//    file has no name for them -- ever.
//  * MERGES into the existing donors.json by Pledge's gift id. Nothing captured is
//    ever dropped. A failed or empty read changes nothing and fails the run, so a
//    broken scrape shows up red in GitHub Actions instead of blanking the site.
//
//  Output rows: { id, ts, name?, anonymous, amount, time, comment?, matched }
//  (name/anonymous/amount/time/comment/matched are the same fields the widgets
//   already read; id + ts are new, and ts is the exact time of the gift.)
// ============================================================================
import { readFileSync, writeFileSync, existsSync } from 'fs';

const PAGE       = process.env.PLEDGE_URL || 'https://www.pledge.to/whatatrip';
const FULL_SYNC  = process.env.FULL_SYNC === '1';
const MIN_GIFTS  = +(process.env.MIN_GIFTS || 20);   // always read at least this many real gifts
const MAX_PAGES  = 200;                              // hard stop (~5,000 rows)
const OUT        = 'donors.json';

/* ---------- what we already have ---------- */
let previous = { donors: [] };
if (existsSync(OUT)) {
  try { previous = JSON.parse(readFileSync(OUT, 'utf8')) || { donors: [] }; }
  catch (e) { console.warn('Could not parse existing donors.json:', e.message); }
}
const prevRows  = Array.isArray(previous.donors) ? previous.donors : [];
const knownIds  = new Set(prevRows.filter((d) => d.id).map((d) => d.id));
// Rows without an id came from the old screen-reading scraper. They can't be matched
// to Pledge's ids, so the first run of this version walks the whole list and rebuilds.
const legacy    = prevRows.some((d) => !d.id);
const walkAll   = FULL_SYNC || legacy || knownIds.size === 0;
console.log(`Have ${prevRows.length} rows (${knownIds.size} with ids). ${walkAll ? 'Walking the whole list.' : 'Reading new gifts.'}`);

/* ---------- fetch ---------- */
async function getPage(lastId) {
  const url = PAGE + (lastId ? '?last_id=' + lastId : '');
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const r = await fetch(url, { headers: { Accept: 'application/json', 'User-Agent': 'whatatrip-donor-wall/2.0 (+https://whatatrip.film)' } });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const j = await r.json();
      if (!j || !Array.isArray(j.orders)) throw new Error('no orders[] in response');
      return j;
    } catch (e) {
      console.warn(`  page ${lastId || 'first'} attempt ${attempt} failed: ${e.message}`);
      if (attempt === 3) throw e;
      await new Promise((res) => setTimeout(res, 2000 * attempt));
    }
  }
}

const orders = [];
let totals = null, lastId = null, gifts = 0, hitKnown = false, pages = 0;
while (pages < MAX_PAGES) {
  const j = await getPage(lastId);
  pages++;
  if (!totals && j.fundraiser_landing_page) totals = j.fundraiser_landing_page;
  if (!j.orders.length) break;                               // end of the list
  for (const o of j.orders) {
    orders.push(o);
    if (!o.is_match) { gifts++; if (knownIds.has(o.id)) hitKnown = true; }
  }
  lastId = j.orders[j.orders.length - 1].id;
  if (!walkAll && gifts >= MIN_GIFTS && hitKnown) break;     // we've overlapped what we have
}
console.log(`Read ${pages} page(s): ${orders.length} rows, ${gifts} real gifts.`);
if (!gifts) { console.error('No gifts read -- leaving donors.json untouched.'); process.exit(1); }

/* ---------- fold match rows into the gifts they match ---------- */
const t = (o) => new Date(o.created_at).getTime();
const matchRows = orders.filter((o) => o.is_match);
const used = new Set();
function hasMatch(g) {
  const m = matchRows.find((o) => !used.has(o.id) && o.amount === g.amount &&
    o.donor_name === g.donor_name && Math.abs(t(o) - t(g)) < 10 * 60 * 1000);
  if (m) { used.add(m.id); return true; }
  return false;
}

function ago(ts) {
  const s = (Date.now() - new Date(ts).getTime()) / 1000;
  const u = (n, w) => { n = Math.max(1, Math.round(n)); return `${n} ${w}${n === 1 ? '' : 's'} ago`; };
  const d = s / 86400;
  if (d >= 365.25) return u(d / 365.25, 'year');
  if (d >= 30.44)  return u(d / 30.44, 'month');
  if (d >= 7)      return u(d / 7, 'week');
  if (d >= 1)      return u(d, 'day');
  if (s >= 3600)   return u(s / 3600, 'hour');
  if (s >= 60)     return u(s / 60, 'minute');
  return 'just now';
}

const fresh = orders
  .filter((o) => !o.is_match && !o.is_pending_pledge)   // pending pledges aren't money yet
  .map((o) => {
    const anonymous = !!o.anonymized || !o.donor_name || /^anonymous$/i.test(o.donor_name.trim());
    const comment = (o.comments || []).filter((c) => c.from_donor !== false)
      .map((c) => String(c.body || '').trim()).filter(Boolean).join(' / ');
    const row = { id: o.id, ts: o.created_at };
    if (!anonymous) row.name = o.donor_name.trim();
    row.anonymous = anonymous;
    row.amount = Math.round(Number(o.usd_amount || o.amount) * 100) / 100;
    row.time = ago(o.created_at);
    if (comment) row.comment = comment;
    row.matched = hasMatch(o);
    return row;
  });

/* ---------- merge: by id, newest first, never drop ---------- */
const byId = new Map();
prevRows.filter((d) => d.id).forEach((d) => byId.set(d.id, { ...d, time: ago(d.ts) }));
fresh.forEach((d) => byId.set(d.id, d));                      // Pledge's current view wins for a gift it still lists
if (walkAll && legacy) {
  // Rebuilding from the old format: only do it if Pledge gave us at least as many gifts
  // as the old file held, so a short read can never shrink the wall.
  const oldGifts = prevRows.length;
  if (byId.size < Math.ceil(oldGifts / 2)) { console.error(`Only ${byId.size} gifts vs ${oldGifts} before -- refusing to rebuild.`); process.exit(1); }
  console.log(`Rebuilt from Pledge: ${oldGifts} old-format rows replaced by ${byId.size} gifts with ids.`);
}
const donors = [...byId.values()].sort((a, b) => new Date(b.ts) - new Date(a.ts));

const out = {
  updated: new Date().toISOString(),
  count: donors.length,
  source: 'pledge-json-v2',
  totals: totals ? {
    raised: Number(totals.total_raised),                          // gifts only (what Pledge calls "raised")
    raised_with_matching: Number(totals.total_raised_with_matching),
    goal: Number(totals.goal),
    donors: totals.total_donors
  } : null,
  donors
};
// Only rewrite the file when a gift changed, or every few hours to refresh the "x ago"
// labels -- otherwise every 15-minute run would make a commit.
const sig = (rows) => JSON.stringify((rows || []).map(({ time, ...rest }) => rest)) + JSON.stringify(out.totals);
const stale = !previous.updated || (Date.now() - new Date(previous.updated).getTime()) > 3 * 3600 * 1000;
if (!legacy && sig(prevRows) + '' === sig(donors) && JSON.stringify(previous.totals) === JSON.stringify(out.totals) && !stale) {
  console.log('No change since last run -- donors.json left as is.');
  process.exit(0);
}
writeFileSync(OUT, JSON.stringify(out, null, 2) + '\n');
console.log(`Wrote ${donors.length} gifts (${fresh.filter((d) => !knownIds.has(d.id)).length} new this run).`);
