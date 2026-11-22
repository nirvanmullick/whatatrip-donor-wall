# What a Trip website: status
Last updated Nov 21, 2026 (written from the claude.ai session notes of Nov 15–18).
Claude Code updates this file at the end of each session.

## Live builds
- whatatrip.com/home-dev (`VERSION-DEV`) serves `a7bda0ade8648167b01652e638fb4b6b8a20880d` (Nov 21: level colours, badges, honeycombs, hover cards, three-way sort).
- /home-test (`VERSION`) still serves `210cca4cc14a26ee9f4797ff6c559141f88428e0`. Move it only when Nirvan says so.

## Built so far (on /home-dev)
- Kickstarter-style home page: zoom-poster hero with the trailer playing in place, the Rough Cut figure and the
  $135K matching card, a level list with Give and Details buttons, a perks carousel, 10 supporters with
  "Show 10 more", budget milestones under the supporters, and FAQs, Updates and Comments as tabs.
- Real sign-in through Supabase (Google and email link, with an optional password), a Member Dashboard with a
  sidebar (Dashboard, My profile, My impact, My perks, Inbox, Updates, More ways to help, Settings), and
  inline profile editing.
- Referrals (`?ref=username`, a 90-day credit window, a welcome pop-up), the post-gift thank-you screen, and 12 starting testimonials.
- Site Management: Members (add, edit, two-step delete), Team & roles, Profile changes, Member messages,
  Forum moderation, Site Analytics, email/text blast (sketch), and perks inventory.
- Member-to-team messaging (non-supporters are limited to 3 a day). Forum beta, team only for now
  (`site_content settings.forum_open`).

## Waiting on Nirvan
1. Level colours and badges: BUILT on /home-dev Nov 21 (his answers: icon only; colour by the giver's overall level;
   pastel rainbow, not saturated). `LVCOL`, `LVICON`, `lvBadge()`, `av()` and `avHex()` in app.js. Not yet done from the
   mockup: badge in the Details pop-up and on member profiles, referral cluster lines, Top/Recent/List tabs, a colour key.
   Nov 21 later: challenge gifts are an interlocking honeycomb (`chHive`, `chHiveLay`) on the page and in the profile
   pop-up (all gifts, order given, sort arrow); hexagons darken on hover; hovering a hexagon or name shows a small
   profile card (`.wath-hc`) that opens the full profile. One sort button steps through largest / most recent /
   order given (`CHORD`); hexagons grow in after a re-sort. "N people gave" is now computed (`chDonors`: each named
   person once, each anonymous gift as one donor), no longer the fixed 76. Waiting on his reaction.
   Done Nov 21: the staff-only note for the two Oct 15 manual gifts is stored in the members database
   (`gift_private.staff_note`, Owner/Admin only; migration `gift_private_staff_note`). The two gifts were added to
   `gifts` as real, unlinked records (source `event_cost`; migrations `gifts_source_allow_private` and `gifts_source_allow_event_cost` added those types).
   The same note is on both contacts in Nirvana as a history note (Nirvan allowed that one write). Never put staff notes in manual-gifts.csv: this repo is public.
2. Level and perk mismatches between the donor wall and the home page: Inner Circle at $2.5K or $25K; extra
   features at $1K or $500; Contributing Producer or Co-Producer at $100K; Road Trippers at $100 or $50; and the
   wall still lists "Get High with Rick".
3. In-house member fundraisers (members never leave for Pledge), and perks option A or B for fundraisers.
4. Whether and when to move off Squarespace (and whether Cloudflare is acceptable).
5. Real bios for Juli Crockett, Micah Van Hove and Jeffrey Reeser.

## Open technical items
- Cloudflare Turnstile check on non-supporter messages (needs a free Cloudflare account; Nirvan pastes the secret into Supabase).
- Email alerts for new messages (needs `RESEND_API_KEY` as a function secret).
- The separate /budget page still shows the old Final Cut lines (the new Final Cut is $915K).
- Mac setup done Nov 21: repo cloned, tests made portable, tools installed in `home-page/src/tests` (`npm install`).
  hm, mem, adm, fit, cols, unread, hover and tabs pass. Two tests are out of date with the page (not a Mac problem):
  `acct.js` looks for the referral field on the dashboard home (`.mov [data-f=ref]`), and `live.js` is blocked by the
  newer "Position your photo" pop-up before Save changes. README also lists `tests/perk.js`, which is not in the repo.
  Fix or retire these before the next behaviour change.
- Sample values that still need real ones: Instagram follower count and goal, limited perk counts, filmmaker Instagram handles.

## Next step
Get Nirvan's reaction to the level colours on /home-dev, then finish the remaining mockup pieces in item 1.
Once the setup commit is pushed, delete the "First-time setup" section from CLAUDE.md.
