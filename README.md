# What a Trip — donor feed and MASTER DONOR LIST (v3)

This repo is the one place our donor records live. The donate page and the donor wall
both read from it, so a donor added here shows up on both.

| File | What it is | Who edits it |
|---|---|---|
| `master-donors.csv` | **The master list.** Every gift from every source, newest first, with names as the site shows them. Click it on GitHub to read or search it, or use the download button to open it in Excel or Google Sheets. | Nobody. It is rebuilt automatically. |
| `manual-gifts.csv` | Every gift that did **not** come through Pledge: GoFundMe, Network for Good, checks, wires, private gifts. | **You**, by hand. |
| `name-fixes.csv` | How a Pledge donor's name should be shown, e.g. "Peter Kennedy" → "Peter & Brooke Kennedy". | **You**, by hand. |
| `donors.json` | Every Pledge gift, read from Pledge every 15 minutes. | Nobody. `scrape.js` writes it. |
| `manual.json`, `master-donors.json` | The two CSVs checked and converted for the website. | Nobody. `build-master.js` writes them. |

## To add a donor who gave outside Pledge

1. Open `manual-gifts.csv` on GitHub and click the pencil (Edit).
2. Add one line anywhere (order doesn't matter), for example:

   ```
   2026-06-15,Elise Fried,5000,,networkforgood,,,,,,given at Rachel & Jade's online event
   ```

   The columns are:
   - **date**: `2026-06-15`, or `2026-06-15 14:30` if you know the time.
   - **name**: as it should appear on the site.
   - **amount**: a number. `$` and commas are fine.
   - **anonymous**: `yes`, or leave it empty.
   - **source**: one of `gofundme`, `networkforgood`, `private`, `check`, `wire`, `stock`, `daf`, `paypal`, `venmo`, `zelle`, `cash`, `nft`, `art`, `other`.
   - **recent_feed**: leave it empty. Put `no` only for an old major gift that should be listed but kept out of Recent Donations.
   - **comment**: shown on the site as the donor's quote. Put it in "double quotes" if it has a comma.
   - **via** (optional): how the gift came in, in your own words. It shows on the wall as "via ...",
     for example `David Choe’s NFT “Fist Hugger” sold at Christie’s auction`. Leave it empty to show the source name.
   - **link** (optional): a web address that the "via" words link to.
   - **video** (optional): an embeddable video player address. It plays small under the person's history when their name is opened.
   - **notes**: for us only. Never shown on the site.
3. Click **Commit changes**.

Within a minute or two GitHub checks the file and rebuilds the master list. Both web pages
pick up the change within about 5 minutes.

**If you make a mistake** (a bad date, a missing name, an unknown source), nothing breaks. The
website keeps the last good version, the run shows a red ✗ in the **Actions** tab, and clicking
the run shows which line is wrong and why. Fix the line and commit again.

## To say where a Pledge gift really came from

`pledge-via.csv` lets a Pledge gift say "via ..." on the site, e.g. Sarena Snider's $4,000 shows as
"via Another Light Foundation Grant". One line per gift: the Pledge gift id (in `master-donors.csv`,
column `pledge_id`), the words, and a note for us.

## Credit links that say whose credit it is

Every credit on the donor wall has its own small page at **credits.whatatrip.com**, e.g.
`https://credits.whatatrip.com/david-choe`. Texted or posted, that link previews as
**"David Choe — Donor to What a Trip"** with a card image showing the name, and opening it goes
straight to David's credit on whatatrip.com/donors. The copy-link icon on the wall hands out these
addresses by itself once credits.whatatrip.com answers.

- `build-credits.js` makes the pages (in `site/`) on every run, so new donors get theirs
  automatically, and the workflow publishes them with GitHub Pages. Nobody edits `site/`.
- A page is never deleted, so a link that has been sent keeps working.
- `site/credits-index.json` lists every address ever handed out and where it goes. If the profiles
  ever move to another system, point `credits.whatatrip.com` at it and have it answer the same
  addresses (or redirect them), and every link already sent keeps working.
- `credits-seed.json` is everyone on the wall on Oct 2, 2026. `fonts/` is the card images' typeface.

**One DNS record makes it live** (in Squarespace → Domains → whatatrip.com → DNS):
`CNAME` · host `credits` · value `nirvanmullick.github.io`

**A gift made on Pledge never goes in `manual-gifts.csv`**, because it comes in by itself. To change how a Pledge name is shown, add a line to `name-fixes.csv` instead.

**Matching challenges.** A gift in `manual-gifts.csv` is never counted toward a matching
challenge. The Osters' challenge only matches Pledge gifts made after it started, and
Rachel's challenge list is kept in the page code.

## What runs when (`.github/workflows/scrape.yml`)
- **Every 15 minutes:** read new Pledge gifts into `donors.json`, then rebuild the master list.
- **Once a day:** read Pledge's whole list.
- **Whenever `manual-gifts.csv` or `name-fixes.csv` is edited:** rebuild the master list straight away.
- If Pledge can't be read, the master list is still rebuilt from what we already have, and the run shows red.

## To install v4 (one time)
1. Upload `build-master.js`, `build-credits.js`, `credits-seed.json`, `pledge-via.csv`,
   `manual-gifts.csv`, `name-fixes.csv`, `package.json`, `.gitignore`, this `README.md`, and the
   whole `fonts` folder (drag the folder onto the upload page).
2. Replace `.github/workflows/scrape.yml` with the new one, as below.
3. Settings → Pages → Source: **GitHub Actions**; Custom domain: `credits.whatatrip.com`.
4. Add the DNS record above. Actions → Scrape donor wall → Run workflow. Then open
   `https://credits.whatatrip.com/david-choe` -- it should land on David's credit.

## (Earlier) To install v3 (one time)
1. In `nirvanmullick/whatatrip-donor-wall`, use **Add file → Upload files** to upload
   `build-master.js`, `manual-gifts.csv`, `name-fixes.csv`, `package.json` and this `README.md`.
   `scrape.js` is unchanged.
2. Open `.github/workflows/scrape.yml`, click the pencil, paste in the new `scrape.yml` from this
   folder, and commit.
3. Go to **Actions → Scrape donor wall → Run workflow**. When it finishes (green ✓), the repo
   has `manual.json` and `master-donors.csv`.
4. Paste the new donate page and donor wall code into Squarespace.

   Until step 3 is done, the pages use the copy of the list built into their code, so nothing
   breaks if the code goes up first.
