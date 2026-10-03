// ============================================================================
//  What a Trip — MASTER DONOR LIST builder                        (2026-09-30)
//
//  Runs in GitHub Actions right after scrape.js (every 15 min), and whenever
//  someone edits manual-gifts.csv or name-fixes.csv on GitHub.
//
//  READS
//    donors.json        every Pledge gift -- written by scrape.js, never by hand
//    manual-gifts.csv   every gift NOT on Pledge (GoFundMe, Network for Good,
//                       cheques, wires, private gifts) -- edited BY HAND
//    name-fixes.csv     how a Pledge name should be shown -- edited BY HAND
//
//  WRITES
//    manual.json        what the donate page and donor wall load (the two CSVs,
//                       checked and cleaned). Only written if both CSVs are valid,
//                       so a typo can never blank the site: the last good copy stays.
//    master-donors.csv  THE MASTER LIST: every gift from every source, one row per
//    master-donors.json gift, newest first, names as the site shows them. Open the
//                       .csv on GitHub to read or search it, or download it into a
//                       spreadsheet or a CRM.
//
//  A problem in a CSV fails the run (red in the Actions tab) and the summary of
//  that run lists the row and what is wrong with it.
// ============================================================================
import { readFileSync, writeFileSync, existsSync, appendFileSync } from 'fs';

const SOURCES = ['gofundme', 'networkforgood', 'private', 'check', 'wire', 'stock', 'daf', 'paypal', 'venmo', 'zelle', 'cash', 'nft', 'art', 'other'];
const SOURCE_LABEL = { pledge: 'Pledge', gofundme: 'GoFundMe', networkforgood: 'Network for Good', nft: 'NFT sale', art: 'Art sale',
  private: 'Private', check: 'Check', wire: 'Wire', stock: 'Stock', daf: 'DAF', paypal: 'PayPal', venmo: 'Venmo', zelle: 'Zelle', cash: 'Cash', other: 'Other' };
const errors = [], warnings = [];

/* ---------- CSV ---------- */
function parseCSV(text) {
  text = text.replace(/^﻿/, '');
  const rows = []; let row = [], cell = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; }
      else cell += c;
    } else if (c === '"') q = true;
    else if (c === ',') { row.push(cell); cell = ''; }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(cell); rows.push(row); row = []; cell = '';
    } else cell += c;
  }
  if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
  const head = (rows.shift() || []).map((h) => h.trim().toLowerCase());
  return rows
    .map((r, i) => ({ line: i + 2, cells: r }))
    .filter(({ cells }) => cells.some((c) => c.trim() !== ''))       // blank lines are fine
    .map(({ line, cells }) => { const o = { _line: line }; head.forEach((h, j) => { o[h] = (cells[j] || '').trim(); }); return o; });
}
const csvCell = (v) => { v = v == null ? '' : String(v); return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
const yes = (v) => /^(y|yes|true|1|x)$/i.test(String(v || '').trim());
const no  = (v) => /^(n|no|false|0)$/i.test(String(v || '').trim());

/* ---------- manual-gifts.csv ---------- */
const gifts = [];
if (!existsSync('manual-gifts.csv')) errors.push('manual-gifts.csv is missing');
else {
  const rows = parseCSV(readFileSync('manual-gifts.csv', 'utf8'));
  const seen = new Map();
  for (const r of rows) {
    const where = `manual-gifts.csv line ${r._line}`;
    // date: 2026-06-15, 2026-06-15 12:05, or 6/15/2026
    let ds = r.date || '', m, ts = null;
    if ((m = ds.match(/^(\d{4})-(\d{1,2})-(\d{1,2})(?:[ T](\d{1,2}):(\d{2}))?/)))
      ts = `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}T${(m[4] || '12').padStart(2, '0')}:${m[5] || '00'}:00`;
    else if ((m = ds.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/)))
      ts = `${m[3]}-${m[1].padStart(2, '0')}-${m[2].padStart(2, '0')}T12:00:00`;
    if (!ts || isNaN(new Date(ts).getTime())) { errors.push(`${where}: the date "${ds}" isn't a date. Use 2026-06-15 (or 2026-06-15 14:30).`); continue; }
    if (new Date(ts).getTime() > Date.now() + 2 * 864e5) warnings.push(`${where}: the date ${ds} is in the future.`);
    const amount = Number(String(r.amount || '').replace(/[$,\s]/g, ''));
    if (!(amount > 0)) { errors.push(`${where}: the amount "${r.amount}" isn't a number above zero.`); continue; }
    const anonymous = yes(r.anonymous);
    if (!anonymous && !r.name) { errors.push(`${where}: no name. Put the donor's name, or "yes" in the anonymous column.`); continue; }
    const source = (r.source || '').toLowerCase().replace(/[\s_-]/g, '');
    if (source === 'pledge') { errors.push(`${where}: Pledge gifts come in by themselves -- don't add them here (to fix how a Pledge name shows, use name-fixes.csv).`); continue; }
    if (!SOURCES.includes(source)) { errors.push(`${where}: the source "${r.source}" isn't one of: ${SOURCES.join(', ')}.`); continue; }
    if (r.recent_feed && !yes(r.recent_feed) && !no(r.recent_feed)) { errors.push(`${where}: recent_feed should be yes, no, or empty.`); continue; }
    const g = { ts, amount, source };
    if (anonymous) g.anonymous = true; else g.name = r.name.replace(/\s+/g, ' ');
    if (r.comment) g.comment = r.comment;
    // optional: how it came in, in your own words ("via ..."), a link for those words, and a video to show
    if (r.via) g.via = r.via.replace(/^via\s+/i, '');
    if (r.link) { if (!/^https?:\/\//.test(r.link)) { errors.push(`${where}: the link "${r.link}" should start with https://`); continue; } g.viaUrl = r.link; }
    if (/^(nft|art)$/.test(source)) g.art = true;   // a gift of art: the wall marks it with an easel
    if (r.video) { if (!/^https:\/\//.test(r.video)) { errors.push(`${where}: the video "${r.video}" should start with https://`); continue; } g.video = r.video; }
    if (no(r.recent_feed)) g.legacy = true;                        // listed on the wall, left out of Recent Donations
    const key = [(g.name || 'anon').toLowerCase(), amount, ts.slice(0, 10), source].join('|');
    if (seen.has(key)) warnings.push(`${where}: looks the same as line ${seen.get(key)} (same name, amount, day and source). If it's really two gifts, fine.`);
    else seen.set(key, r._line);
    gifts.push(g);
  }
}

/* ---------- name-fixes.csv ---------- */
const renames = {};
if (existsSync('name-fixes.csv')) {
  for (const r of parseCSV(readFileSync('name-fixes.csv', 'utf8'))) {
    const from = (r.name_on_pledge || '').trim(), to = (r.show_as || '').trim();
    if (!from || !to) { errors.push(`name-fixes.csv line ${r._line}: needs both name_on_pledge and show_as.`); continue; }
    const k = from.toLowerCase();
    if (renames[k] && renames[k] !== to) errors.push(`name-fixes.csv line ${r._line}: "${from}" is already renamed to "${renames[k]}".`);
    renames[k] = to;
  }
}

/* ---------- pledge-via.csv: a Pledge gift that really came from somewhere else ---------- */
const pledgeVia = {};
if (existsSync('pledge-via.csv')) {
  for (const r of parseCSV(readFileSync('pledge-via.csv', 'utf8'))) {
    const id = String(r.pledge_id || '').trim(), via = String(r.via || '').trim().replace(/^via\s+/i, '');
    if (!/^\d+$/.test(id) || !via) { errors.push(`pledge-via.csv line ${r._line}: needs a pledge_id (a number) and via.`); continue; }
    pledgeVia[id] = via;
  }
}

/* ---------- report ---------- */
function summary(md) { if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, md + '\n'); }
if (errors.length) {
  console.error('NOT UPDATED -- fix these first:\n  ' + errors.join('\n  '));
  summary('## Master donor list NOT updated\nThe site keeps using the last good version until these are fixed:\n\n' + errors.map((e) => '- ' + e).join('\n'));
  if (warnings.length) summary('\n**Also worth a look:**\n' + warnings.map((w) => '- ' + w).join('\n'));
  process.exit(1);
}

/* ---------- manual.json (what the pages load) ---------- */
gifts.sort((a, b) => (a.ts < b.ts ? 1 : a.ts > b.ts ? -1 : 0));
const manual = { updated: new Date().toISOString(), count: gifts.length, gifts, renames, pledgeVia };
const prevManual = existsSync('manual.json') ? readFileSync('manual.json', 'utf8') : '';
const strip = (s) => { try { const o = JSON.parse(s); delete o.updated; return JSON.stringify(o); } catch (e) { return ''; } };
if (strip(prevManual) !== strip(JSON.stringify(manual))) writeFileSync('manual.json', JSON.stringify(manual, null, 1) + '\n');

/* ---------- the master list ---------- */
let pledge = [];
if (existsSync('donors.json')) {
  try { pledge = JSON.parse(readFileSync('donors.json', 'utf8')).donors || []; }
  catch (e) { warnings.push('donors.json could not be read: ' + e.message); }
}
const shown = (n) => (n && renames[n.trim().toLowerCase()]) || n;
const all = [
  ...pledge.map((d) => ({ date: d.ts, name: d.anonymous ? '' : shown(d.name), name_on_record: d.anonymous ? '' : d.name,
    amount: d.amount, source: 'pledge', anonymous: !!d.anonymous, matched: !!d.matched, pledge_id: d.id, via: pledgeVia[d.id] || '',
    // a donor who typed their preferred name into Pledge's comment box: once renamed, that comment is just the name again
    comment: (d.comment && shown(d.name) && d.comment.trim().toLowerCase() === shown(d.name).toLowerCase()) ? '' : (d.comment || ''),
    added_by: 'automatic (Pledge)' })),
  ...gifts.map((g) => ({ date: g.ts, name: g.anonymous ? '' : g.name, name_on_record: g.anonymous ? '' : g.name,
    amount: g.amount, source: g.source, anonymous: !!g.anonymous, matched: false, pledge_id: '',
    comment: g.comment || '', via: g.via || '', added_by: 'by hand (manual-gifts.csv)' + (g.legacy ? ', not in Recent feed' : '') }))
].sort((a, b) => new Date(b.date) - new Date(a.date));

const cols = ['date', 'name', 'amount', 'source', 'via', 'anonymous', 'matched_on_pledge', 'comment', 'name_on_record', 'pledge_id', 'added_by'];
const csv = [cols.join(',')].concat(all.map((g) => [
  String(g.date).replace('T', ' ').slice(0, 16), g.anonymous ? 'Anonymous' : g.name, g.amount, SOURCE_LABEL[g.source] || g.source, g.via || '',
  g.anonymous ? 'yes' : '', g.matched ? 'yes' : '', g.comment, g.name_on_record, g.pledge_id, g.added_by
].map(csvCell).join(','))).join('\n') + '\n';
const prevCsv = existsSync('master-donors.csv') ? readFileSync('master-donors.csv', 'utf8') : '';
if (prevCsv !== csv) {
  writeFileSync('master-donors.csv', csv);
  writeFileSync('master-donors.json', JSON.stringify({ updated: new Date().toISOString(), count: all.length, gifts: all }, null, 1) + '\n');
}

/* ---------- totals, for the run summary ---------- */
const bySource = {};
let total = 0;
all.forEach((g) => { total += g.amount; const s = SOURCE_LABEL[g.source] || g.source; bySource[s] = bySource[s] || { n: 0, amt: 0 }; bySource[s].n++; bySource[s].amt += g.amount; });
const people = new Set(all.filter((g) => !g.anonymous).map((g) => g.name.toLowerCase())).size;
const money = (n) => '$' + Math.round(n).toLocaleString('en-US');
console.log(`Master list: ${all.length} gifts, ${money(total)}, ${people} named supporters + ${all.filter((g) => g.anonymous).length} anonymous gifts.`);
Object.entries(bySource).forEach(([s, v]) => console.log(`  ${s}: ${v.n} gifts, ${money(v.amt)}`));
summary(`## Master donor list: ${all.length} gifts, ${money(total)}\n\n| Source | Gifts | Amount |\n|---|---:|---:|\n` +
  Object.entries(bySource).map(([s, v]) => `| ${s} | ${v.n} | ${money(v.amt)} |`).join('\n') +
  `\n\n${people} named supporters. Challenge matches (money a sponsor gives to match others) are not rows here.`);
if (warnings.length) { console.warn('Warnings:\n  ' + warnings.join('\n  ')); summary('\n**Worth a look (not errors):**\n' + warnings.map((w) => '- ' + w).join('\n')); }
