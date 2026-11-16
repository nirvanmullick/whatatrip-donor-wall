# Home page source (how to rebuild `home-block.html`)

`../home-block.html` is generated. Never edit it by hand. Edit the source here, rebuild, test, publish.

## Files
- `build.py`: builds the page. Holds the markup and all CSS. Reads `proto/index.html` (levels, perks, comments),
  `bud.json` (budget), `photos.json`, and `app.js`. Run from anywhere: `python3 home-page/src/build.py`.
- `app.js`: all behaviour, including the sample Member Dashboard and admin area.
- `proto/`: the earlier prototype that `build.py` pulls data blocks from.
- `tests/`: Playwright checks. They expect the repo at `/home/claude/whatatrip-donor-wall` and Playwright at
  `/opt/npm-tools/node_modules/playwright`.

## Real sign-in ("live" mode)
On whatatrip.com the Log in button is real: `app.js` (block starting `LIVE sign-in`) loads supabase-js from jsdelivr and talks to
the members database at `https://auth.whatatrip.com` with the public (publishable) key. Google and email-link sign-in, the
member's own profile and gifts, profile edits (saved at once; public fields through `save_my_profile()`, no approval step),
an optional password (asked once after a first email-link log in; `PROV=email node tests/live.js` covers it), the member
sidebar menu, and the admin Members list. Anywhere else, or with `?sample=1`, the old sample preview runs, which is what the other
tests use. `node tests/live.js` exercises live mode against a mocked database (needs supabase-js at
`/tmp/sbjs`: `mkdir -p /tmp/sbjs && cd /tmp/sbjs && npm i @supabase/supabase-js@2.119.0`). Never put a secret key in this file.

Team invitations are emailed by the Supabase Edge Function `invite-email` (source kept in `../supabase/functions/invite-email/index.ts`;
deploy it to the What a Trip project when it changes). It needs the function secret `RESEND_API_KEY`. Without the secret the
role is still given and the page says the email could not be sent.

## Adding CSS
In `build.py`, insert new rules before the LAST occurrence of `:is(#wath,#wath-top) .upx{display:flex;`
(`i=b.rindex(k)`). Scope selectors by hand: `:is(#wath,#wath-top) ...` for the page, `#wath-top ...` for the
member/admin overlay, `#header ...` for the Squarespace header. Later rules win, so this file has many overrides;
check for an existing rule before adding another.

## After every build
1. Extract the last `<script>` of `home-block.html` and run `node --check` on it.
2. `node tests/hm.js` should end with `1300 hscroll 0 []` and `390 hscroll 0 []`.
3. `node tests/mem.js` (member screens, 16 lines ending `0 ]`), `node tests/adm.js` (admin, 14 lines `0, 0 ]`),
   `node tests/acct.js` (login, account menu, referral link), `node tests/fit.js` (older check from when "Show more" lined up with "Compare all perks"; now informational), `node tests/cols.js` (15 supporters on desktop, budget under the supporters beside the level list), `node tests/perk.js` (Give / Details buttons and pop-ups).
4. Look at screenshots at 1300 and 390 wide. The sandbox cannot load squarespace-cdn images, so photos are blank
   there; check real photos on the live test page.

## Publish
1. Commit `home-block.html` (and the source), push to `main`.
2. Write that commit's id into `home-page/VERSION`, commit, push.
3. Verify with `git show origin/main:home-page/VERSION`. raw.githubusercontent caches for about 5 minutes.

The page is loaded only by the hidden test page whatatrip.com/home-test.
