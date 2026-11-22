# What a Trip website: status
Last updated Nov 22, 2026 (written from the claude.ai session notes of Nov 15–18).
Claude Code updates this file at the end of each session.

## Live builds
- whatatrip.com/home-dev (`VERSION-DEV`) serves `8b4a68b13c979dbd5d8a5b64d192d78144905ea7` (Nov 22: honeycomb grid of supporters, roomier preview card, full-page profile).
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
   Nov 22: Nirvan calls it the "honeycomb grid of supporters". Now: two orders only (largest first, most recent first;
   `CHORD`), filled column by column so colour runs left to right (`chHiveLay`), grows in as a wave when a challenge
   opens (script animation, `grow` class), and on a re-sort hexagons and list rows glide to their new places
   (`chResort`, no re-render). Lists show a small profile hexagon by each name. Anonymous gifts take the colour of the
   level of that gift and have their own card (Anonymous, level, amount, their comment) via `anonAt`. The preview card
   is bigger with a white "View full profile" button and previews a quote (`seedOf`). Challenge makers get a quiet
   second outline in grids and lists (`isMaker`, `.av.mk`). Waiting on his reaction.
   Nov 22 later: a profile now opens as a full page, not a pop-up (`openProfilePage`, `sppgSide`, `.sppg` CSS; `openSupp(n)`
   with no target calls it, and the old pop-up code is gone). Main column = the same profile body (`openSupp(n,into)` with
   `into._page`). Side column by view: visitor (Join the trip, Connections, active match, ways to help), member
   (Connections, invite link, next level, match), own (Finish your profile, Connections, invite, next level).
   "Connections" today = referral links both ways (`CONN.ref`), with a grey "will be shown here" when empty. Below: the
   honeycomb grid of all supporters (`TOPL`) with search and the two-order sort. Photos in grids get a wash of the level
   colour, full photo on hover. Preview card no longer vanishes while the pointer travels to it.
   Nov 22: the home page Comments tab is now "Voices" with the heading "Why this film matters" (ids and code names
   still say comments). Later the same day the section heading became "Voices" + count with the subtitle
   "Why this film matters", so the menu link lands on a matching title. `renderComments` ends with an "Add your voice" block: non-members get Donate $5 / Start a
   fundraiser / Log in; members get a button that opens their own profile page. Member testimonials do NOT yet appear
   in that list (it shows pinned quotes and gift comments only).
   Nov 22: matching challenges start open (`CHOPEN[slug]!==false`), so their honeycombs show without a click; hovering
   a hexagon highlights that gift's row in the list under it (`li.hl`). Members' own quotes are wired into the Voices
   list (`MVOICE`, `voiceLoad`, merged in `comments()` for $5+ members) but need the `member_voices()` database function:
   SQL is in `home-page/supabase/member_voices.sql`, APPLIED Nov 22 with his OK (read-only, 3 quotes today).
   Note: `seedLoad()` runs before `LIVE` is set (line order), so team-made seed quotes never load from the database;
   left alone, ask Nirvan before changing since it would change which quotes show.
   Profile page side cards for a logged-in member now speak to them: "My referral link" / "Share my link" and
   "Level up" (works out what they need for the next level; the button opens giving with that amount filled in).
   Nov 22 late: "Add your voice" is one button under the Voices list; non-members get a small pop-up (`voiceAsk`:
   Donate $5 to join, quiet links to log in or start a fundraiser), members go to their own profile. Preview cards also
   show on the Our supporters list, and every card waits 0.6s. Photos in grids are a soft one-colour image in the level
   colour with initials on top (`data-i` on `.av`), real photo on hover; challenge makers too. PUBLIC NAME: never say
   "honeycomb grid of supporters" on the site (internal name only); the profile page section is headed "Our community".
   Asked, not designed yet: how a member connects their Pledge fundraiser so it fills their profile, and what a
   member's own fundraising page (whatatrip.com/username) looks like.
   Nov 22 night: tools on each voice (`renderComments`, `voiceId`, `voiceSet`, `voiceSave`, `voiceFlag`, `VMENU`).
   Everyone sees two reactions and a reply button (the existing reactions/comments tables, target `voice:<slug>:<hash>`).
   Members get a flag (sends a team inbox message). Owners and Admins get a three-dot menu: pin, hide, flag, remove;
   saved under `voices` in the `settings` row of `site_content` (no migration). Managers cannot use the menu yet because
   `save_site_content` only lets owner/admin write `settings`; widening that needs a migration and Nirvan's OK.
   There is no screen yet to restore a removed voice (edit `settings.voices.rem`).
   SUPPORTER COUNT (decided Nov 22: match /donors): the page now counts it itself (`suppCount`): every named person
   once (donors in `TOTALS`, challenge makers in `LEGS`/`PAST`, people in `CONN.act` credited for raising without a gift)
   plus every anonymous gift. That is the /donors rule (its people list minus the "Unnamed Community Credit" row).
   The Nirvana count is only a stand-in until gifts load. Confirmed live Nov 22: both pages read 293. Older note follows.
   SUPPORTER COUNT (old): /home-dev showed 286 from the Nirvana `wat-donor-count` function (266 known people + 20 anonymous
   gifts it cannot tie to a known person). whatatrip.com/donors shows 293-294 because it counts every anonymous gift
   (36) as its own supporter and adds a few names credited without a gift. Waiting on Nirvan: which rule to use.
   Asked for next: hero mockups (supporter hexagons filling the hero after the zoom / after the trailer, and Rick's
   portrait made of supporter hexagons).
   Layout fix: opening every challenge made the section too tall to sit beside the perks, so the page's own fit
   script dropped it below (Nirvan noticed). Now `fit()` folds the lowest challenges (`CHAUTO`) until the section fits;
   anything the visitor toggles (`CHOPEN`) is kept. Phones and tablets show all open.
   Add your voice for a logged-in $5+ member is now an inline box under the list (`VBOX`, saves via `spSave` to the
   profile testimonial; prefilled with a note if they already have one). Non-members still get the join pop-up.
   Singular level names for one person (`lvOne(level, name)`, built on `LVONE`): "MAPS Maker" on cards, profiles,
   lists, the dashboard and Level up; the plural stays for the level itself and for couples ("A & B").
   Nov 22 last round: the Voices section is headed by a small purple label "Voices" + count (`.eyb`) over the h2
   "Why this film matters"; "More ways to help" has a matching label ("Get involved", my wording) so both boxes start
   level (sticky top 93px). Voice ids are now `page:voice-<slug>-<hash>` because the reactions/comments tables only
   accept update:/gift:/page:/comment: targets (the first version, `voice:`, failed with WAT-RXN). Reactions show on
   hover on desktop (always on touch, and always once someone has reacted). A logged-out reaction or reply opens the
   small join-or-log-in pop-up (`voiceAsk('react')`, used by `socNeedLogin` everywhere). Names and icons in the list
   open the preview card. Hexagons are top-aligned with the quote.
   Asked, not built: the log-in screen itself as a small pop-up (today it is the full-screen dashboard overlay);
   a "Members" page replacing the donor wall, one grid of supporters and filmmakers, with filmmaker profile pages
   (bio, films, testimonial) and per-field privacy (public / connections only).
   Submenu (Nov 22): Campaign, Story, Filmmakers, Supporters + count (`data-cnt="sup"`, set in `renderHero`), FAQs,
   Budget, Impact, Voices, Updates. Only the FINAL menu string in build.py (the `_ne` replacement) was changed; the
   first copy is rewritten by later build steps and must stay as it is. Menu order no longer matches scroll order
   (the Filmmakers section is still lower on the page), so the highlight jumps; moving the section is a layout change
   to offer Nirvan.
   DONE Nov 22: (1) log-in as a pop-up. `.mov[data-tab="login"|"pw"]` is now a dimmed layover with the `.mlogin`
   card centred (CSS only, plus a close button `.mlx` in the card and click-outside-to-close). The sign-in logic is
   untouched; after logging in the full dashboard opens as before. Not verified against real Google/email sign-in.
   DONE Nov 22: each challenge card has a share button (`.chsh`, `data-chshare`; copies `chLink(slug)` = this page +
   `#wat-challenge-<slug>`, or the phone share sheet). Arriving on such a link scrolls to and opens that challenge
   (`chGo`). Card titles lead with the amount: "$60,000 matching challenge by NAME" (`chTitleCard`; the name shows the
   preview card when the person has gifts).
   DONE Nov 22: supporters honeycomb at the top of the Supporters section (`supHive`, container `.suphv` inserted
   before `[data-donations]`; `data-rows="4"` caps a hive in `chHiveLay`; "See all supporters" links to /donors until
   the Members page exists). It re-sorts with the Top/Recent tabs via `chResort` and hovering a hexagon highlights the
   whole list row (`.dn.hl`). Also fixed an older bug: at phone widths the Supporters section was ~28px wider than
   the screen because the two tabs could not shrink (amounts were cut off at the right).
   Both supporter honeycombs (home page `supHive`, profile page `openProfilePage`) now draw from `supAllHex(mode)`:
   named supporters + people credited without a gift + one hexagon per anonymous gift, so their totals equal
   `suppCount()` (293 live). Arcturus card moved into the perks column (`[data-arcbox]`, appended to `#wath-levels`).
   Filmmakers: mockup only in `../mockups/filmmakers-ideas.html` (ideas A/B/C + a filmmaker profile page); waiting on
   Nirvan's pick, then move the section up under Story.
   Stripe checkout + Fiscal Sponsor role for Creative Visions runs in its own session ("Stripe checkout for Creative
   Visions"); do not build it here.
   DONE Nov 22: Filmmakers is compact and sits in the left column right after Story. The last step of build.py
   removes the old full-width band and inserts `<section id="wath-team">` with `[data-team]`; `renderTeam()` draws a
   two-row zigzag honeycomb (`teamLay`, wraps into more bands as the crew grows) and a list of names and roles (first
   five, then "Show N more"). Order and membership: `TEAMORD` + `BIOS`. Hovering a face or name shows the preview card
   (role + first line of the bio); clicking opens the existing bio pop-up. Filmmaker PROFILE PAGES are still only a
   mockup (`../mockups/filmmakers-ideas.html`).
   DONE Nov 22: on a profile page the community honeycomb sits in the left column under the profile (`.sppgL`).
   DONE Nov 22: a search button above the home-page supporters honeycomb (`SUPF`, `supFilter`, `[data-supsearch]`);
   typing narrows the grid (class `xq`, skipped by `chHiveLay`) and lifts the four-row cap while searching.
   STILL TO DO from that list and later messages: move "Learn about Arcturus" up under the perk levels with a divider;
   hexagon doubling-icon mockup; Filmmakers section redesign (compact, left column, right after Story, honeycomb of
   filmmakers highlighting Darren Aronofsky) + filmmaker/crew profile mockups (other films with thumbnails, IMDb link,
   their own referral link and network); admins adding referrals by hand so they show in a person's connections
   (`staff_set_referral` already exists in the database).
   ALSO ASKED Nov 22 (older list): supporters honeycomb grid (4 rows + "See all") above the Top/Recent tabs in the
   Supporters section, shuffling when the tab changes and highlighting the matching list row on hover; move the
   "Learn about Arcturus" block up under the perk levels with a divider; mock up the doubling icon as two overlapping
   hexagons instead of hearts; Creative Visions/Stripe admin idea (discussion only).
   QUEUE he asked for, in his words "build these next": (1) log-in as a small pop-up [done], (2) Members page replacing the
   donor wall with supporters + filmmakers in one grid, filmmaker profiles, per-field privacy (needs a migration: ask),
   (3) hero mockups, (4) four-row community grid on the home page, (5) donor wall mockup, (6) Connect button (migration).
   NOT built, needs a database change he must OK first: a "Connect" button and member-to-member connections.
   Asked for next (Nov 22): a four-row honeycomb grid at the top of the home page community section with Top donors /
   Recent buttons that shuffle it and a "View all" to a donors page; and a new donor wall (mock up first): full
   honeycomb at the top, clicking a hexagon scrolls to that person in the list, hovering opens the preview card.
   Stale tests: `pf.js` also fails (perks form), alongside `acct.js` and `live.js`.
2a. NEW REQUESTS Nov 22, not built (mock up first, then ask before any database change):
   - Full profile as a page, not a pop-up, laid out like the dashboard profile. Three views: your own (logged in),
     a visitor (right column markets "Become a member"), and a logged-in member viewing someone else. Columns hold a
     honeycomb grid of all members/donors you can hover, and a member search bar.
   - Member connections: each member chooses who may connect (people I already know via a contacts upload and match,
     only members at chosen levels, or nobody) and how to be told (site inbox, email, text). Needs schema, privacy
     review (contacts upload is sensitive) and Nirvan's OK on migrations.
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
