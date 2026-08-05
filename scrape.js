// Renders the public Pledge fundraiser wall in a headless browser and writes
// donors.json. Pledge has already applied each donor's anonymity choice, so we
// simply mirror what the wall shows — "Anonymous" stays anonymous, names stay names.
import { chromium } from 'playwright';
import { writeFileSync } from 'fs';

const URL = 'https://www.pledge.to/whatatrip';   // <-- your fundraiser's public page

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });

// wait for the donor rows to render
await page.waitForSelector('div.h6.mb-0', { timeout: 40000 }).catch(() => {});

// click any "load more / show more" a few times to pull in older gifts
for (let i = 0; i < 10; i++) {
  const more = await page.$(
    'button:has-text("Load more"), button:has-text("Show more"), a:has-text("Load more"), a:has-text("Show more"), button:has-text("See all")'
  );
  if (!more) break;
  await more.click().catch(() => {});
  await page.waitForTimeout(1200);
}

const donors = await page.evaluate(() => {
  const rows = [...document.querySelectorAll('div.h6.mb-0')].filter((el) =>
    /donated/i.test(el.textContent || '')
  );
  const seen = new Set();
  const list = [];
  rows.forEach((el) => {
    // name = the first <b>; amount = the <b> inside the amount span
    const nameEl = el.querySelector('b');
    const amtEl = el.querySelector('span.text-nowrap b') ||
                  [...el.querySelectorAll('b')].find((b) => /\$/.test(b.textContent || ''));
    const name = nameEl ? nameEl.textContent.trim() : '';
    const amountStr = amtEl ? amtEl.textContent.replace(/[^\d.]/g, '') : '';
    const amount = amountStr ? Number(amountStr) : null;
    if (amount == null) return;

    // time = the <small> text, minus the "Match 🎉" badge
    let time = '';
    const small = el.querySelector('small');
    if (small) {
      const clone = small.cloneNode(true);
      const badge = clone.querySelector('.text-primary');
      if (badge) badge.remove();
      time = (clone.textContent || '').replace(/\s+/g, ' ').trim();
    }

    // comment = the "shadow-primary" bubble inside the same <li>, if present
    let comment = '';
    const li = el.closest('li');
    if (li) {
      const cEl = li.querySelector('[class*="shadow-primary"]');
      if (cEl) comment = (cEl.textContent || '').replace(/\s+/g, ' ').trim();
    }

    const anonymous = /^anonymous$/i.test(name);
    // de-dupe (the wall repeats donors across Recent/Top tabs)
    const key = name + '|' + amount + '|' + time + '|' + comment;
    if (seen.has(key)) return;
    seen.add(key);

    list.push({
      name: anonymous ? '' : name,   // never store a name Pledge is hiding
      anonymous,
      amount,
      time,
      comment,
      matched: /Match/i.test(el.textContent || ''),
    });
  });
  return list;
});

writeFileSync(
  'donors.json',
  JSON.stringify({ updated: new Date().toISOString(), count: donors.length, donors }, null, 2)
);
await browser.close();
console.log('Wrote donors.json with', donors.length, 'donors');
