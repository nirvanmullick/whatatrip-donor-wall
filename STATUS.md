# What a Trip website: status
Last updated Nov 22, 2026 (written from the claude.ai session notes of Nov 15–18).
Claude Code updates this file at the end of each session.

## Live builds
- whatatrip.com/home-dev (`VERSION-DEV`) serves `b6848be2d6cfcb722a091e5da27264c8b9929603` (Nov 22: honeycomb grid of supporters, roomier preview card, full-page profile).
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
   DONE Nov 22 (late): Supporters heading reads "Our N supporters" (live count, in `renderHero`); the link under the
   grid reads "See all N supporters" and is right-aligned. Connections on a profile page are a linked two-row chain
   (`data-zig` on the hive; the zigzag branch at the top of `chHiveLay`), wrapping into more bands when wide.
   Filmmakers v3 (Nov 22, replaces the honeycomb + list): honeycomb on the left, ONE featured filmmaker panel on the
   right (`teamPanel`), no list. Hover or tap a face to swap the panel (`teamPick`); the featured face is crisp, the
   rest soft. Owners/Admins get "Edit order" (`TEAMEDIT`): drag faces or Move earlier/later; order saved as `team` in
   the `settings` row of `site_content` (`teamSave`), first = featured. No films list yet (BIOS has no films data).
   Supporters search (Nov 22, final shape): the magnifying glass sits inline after "Our N supporters" (`.suphd` wraps
   the h2 and the controls); the field slides open/shut (`.sopen`, `supOpenSet`); "See all N" is on the heading line,
   not under the grid. While searching the preview stays at four rows, shows names whose first or last name STARTS
   with the query, in the current tab's order, and the hexagons glide to their new spots (`supRelay`). The full grid
   on profile pages keeps everyone in place and dims non-matches (unchanged).
   Challenges (Nov 22): the submenu has "Challenges" + count (`data-cnt="chal"`, = LEGS + PAST) after Supporters.
   Completed challenges are sorted largest first, with a button for most recent first (`CHDSORT`, `chDoneTs`). Open
   by default: any active challenge and the first completed one (`CHDEF`); the rest start folded. The fit script can
   still fold the top one at tight tablet widths. This supersedes "all challenges start open".
   ASKED, not built: an "Import contacts" option in the Invite a friend pop-up. Contact import is not built at all yet
   (needs the privacy decisions and backend discussed Nov 22).
   Nov 22: anonymous hexagons read "AN" (`avHex`). The home supporters honeycomb ends with a "?" hexagon
   (`[data-join]`, placed in the last showing slot by `chHiveLay`); its card says "Will you join us?" with a
   "Join us" button that calls `give(5)`.
   COORDINATION: the Stripe session was told it may edit `app.js`/`build.py` to put its test checkout on /home-dev
   after this session's push; pull before editing here again.
   ASKED, not built: "Offer a perk" form under More ways to help (first version can post to the team inbox).
   Nov 22, crew profiles round:
   - Crew profile pages: `openBio(k)` now opens `openProfilePage(name,k)` (same page as supporters) with `crewMain`/`crewSide`.
     Films and links live in `CREWX` (Darren's ten films link to IMDb; tiles are text only, no poster art yet). `?crew=rick` deep link.
   - Team list: Rick Doblin (Featured Talent, photo `home-page/img/rick-suit-hex.jpg`, bio is a DRAFT), Eric Watson and Interconnected
     (both with placeholder one-line bios, no photo). Supporters with $100K+ are added automatically (`teamSupp`, skips private profiles);
     their hexagon opens their supporter profile. Heading is "Our Filmmaking Team"; honeycomb rows are 5 / 4 / 5 (`teamLay`).
   - New perk at $100K: "A place on our filmmaking team" (level box bullet in the `LEVELS.forEach` near the top, `GPK` id `team`,
     checkout bullet in `gcoPerkB`). If the level wording has been edited in Site Management, check it still shows.
   - Everyone's Connections card starts with Rick (`sppgHex(names,1)`); Rick's page says everyone is connected to him.
   - Grid photos: fainter at rest (.14), one-colour picture in the level's colour on hover; the full-colour photo is in the card.
   - Preview card: sits just below or above a honeycomb instead of on it, opens out of the hexagon, stronger shadow.
   - Join hexagon: blue, card says "Want to join us?" with a purple "Donate now" button; an empty search keeps it on its own row.
   Later Nov 22: the supporter search has an X (`[data-supclr]`) and also filters the Top / Recent list as you type
   (`supV`/`supHit` in `renderDonations`; ranks keep their real number). Profile pages have a faint hexagon wallpaper
   (background of `.bov.sppg`). The Stripe test checkout was NOT added: Nirvan told the Stripe session not to put it on the
   site at all (it must be unsearchable, maybe password-protected). The older gco test checkout is still on /home-dev.
   FAQs have an Expand all / Collapse all control on the heading (`faqAllSet`, added in `faqCnt`). The profile wallpaper has a second
   tile with a few softly filled hexagons.
   Event hosts (anyone with a row in `activities`): `isHost` adds class `eh` (darker outline); in the grid they are placed by the
   level they raised to (`supAllHex`), and the profile reads "Hosted an event that raised $25K+". The wallpaper's filled hexagons
   use the level colours. Not checked against live data (the test data has no event for Alex Enchin).
   The join hexagon (`JOINHX`) is also the last hexagon of the full community grid on profile pages (bottom row of the last column).
   Count check Nov 22: /home-dev and /donors both read 293 when loaded fresh (Nirvan saw 294 on /donors once; not reproduced).
   Honeycombs (`chHiveLay`, all except the zigzag connection chains) now fill along the diagonal: each cell is scored
   col/cols + row/rows and people take cells in that order, so colours run upper-left to lower-right. The join hexagon is a deeper
   lavender and holds the lower-right corner; a short last row is right-aligned up to it.
   Database: Alex Enchin's existing event row (Oct 15 2019, $30,000) was retitled "Fundraising event in Toronto".
   OPEN: Nirvan sees 294 on /donors; fresh loads here show 293 on both pages. Waiting on a screenshot of where he sees it.
   Team honeycomb: hover switches after 220ms (`TEAMHT`), the unselected faces are fainter and the selected one is slightly larger,
   clicking any face opens its profile on hover devices, and the button reads "View my crew profile".
   Crew profile editor: Owners and Admins get "Edit profile" on a crew page (`crewForm`, `crewEdClick`, `crewSave`). Edits are saved
   in the site settings under `crew` (no database change) and applied over the built-in text by `crewApply`. Photo upload goes to the
   editor's own folder in the `profile-photos` bucket; NOT tested with a real login yet. Team photos are black and white in the team section.
   Not built: crew members editing their own page (needs their member account linked to the crew page: a database change).
   Profile wallpaper: `sppgLife` lights one hexagon in the side margins every 10 to 30 seconds (max nine, off for reduced motion,
   narrow screens and hidden tabs). Team honeycomb now switches only after the pointer has rested on a face for 260ms (mousemove).
   Levels now match the donor wall (Nirvan, relayed by the Stripe session): Road Trippers start at $100 (was $50; LVCOL and LVICON keys
   moved to 100), $100K is "Contributing Producer", top level is "Presented by". Source: `home-page/src/proto/index.html` LEVELS/PERKS,
   `app.js`, `mc-bundle.html`. NOT ruled on by Nirvan: home page still lists "Smoke a joint with Rick" (donor wall removed it) and hides
   Wayfinders/Trailblazers (donor wall shows them).
   THE THREE COUNTS (Nov 22): /donors loading screen shows the number this browser remembered from its last visit (it counts name chips
   on screen, so it can read 294-296); the wall itself and /home-dev compute 293 = 252 named givers + 36 anonymous gifts + 5 credited
   non-givers; /donate shows 286 from the Nirvana CRM count service (266 known donors + 20 anonymous gifts it could not match to anyone).
   Nirvan wants one accurate number and the word "supporters" instead of "donors". Proposal pending his OK (touches the live /donors
   and /donate pages).
   Profile pages: `openProfilePage` scrolls the window to the top, opens the page just below the site header and restores the scroll
   on close (`sppgLeave`); `sppgNav` renames the header's /donors link to "Supporters" on this page and marks it while a profile is open
   (the real menu rename has to be done in Squarespace). Wallpaper is the `.sppgfx::before` layer (`--sppgwp`), fades in on arrival and
   out through a `.sppgout` ghost; filled hexagons stay (max 80), fainter, anywhere on the wallpaper. Join card says "You? Join us! :-)".
   ASKED, not started: dev versions of the other pages (matching, supporters wall, donate, about, impact) so the dev menu stays in the
   dev world. Conflict to raise: he told the Stripe session the new checkout must not go on the site, even for development.
   Supporters list: Top supporters / Recent donations are now tabs on a line (`.seg.suptabs`), and switching glides rows that appear in
   both lists to their new place and fades in the rest (in the `data-sup` click handler). Phone widths: the name side shrinks and the
   level label under the amount may wrap, so nothing overlaps. Built-in team order (`TEAMORD`) now equals the order Nirvan saved.
   NOTED from Nirvan: the Fiscal Sponsor role (Creative Visions) may edit only its own profile, nothing else on the site.
   CORRECTION (Nirvan, relayed by the Stripe session): Road Trippers stays at $50 on the home page; reverted (LVCOL/LVICON keys back
   to 50). "Contributing Producer" and "Presented by" stay. The donor wall still says $100 for Road Trippers; nobody has changed it.
   Team honeycomb now switches 80ms after the pointer stops on a face.
   Join hexagon: a click opens giving (`give(5)`); on touch the first tap shows the card and the second opens giving. The card title is
   "You? Join us!" with a waving-hand emoji that waves once every ten seconds (`.hcwave`).
   Stripe checkout on /home-dev: Nirvan told this session it may go on the dev site only; the Stripe session is confirming with him
   first-hand before doing anything (he had told it not to put it on the site at all). Nothing added yet.
   Rick's crew page: the Connections card reads "<count> Connections" and shows the supporters honeycomb, four rows, with a
   "See all" button that opens the rest (`[data-crall]` in the profile page click handler).
   Crew pages: Links card comes first, each link with a small icon (`crewLinkIco`); film tiles are a poster on top (hotlinked from
   Wikipedia; 4th field of a film in `CREWX`, editable in the form) with the title and year under it. Nirvan has Caine's Arcade and
   The 1 Second Film. To confirm with Nirvan: Instagram handles (@rickdoblin, @mapsnews, @darrenaronofsky), poster rights, what "Box"
   meant in his dictated note, and logo files for MAPS and Protozoa (none added). Menu: Supporters is marked with a soft tint, no underline.
   NOT built: a "Connect with me" card with the crew member's referral link (needs their member account linked to the crew page).
   Nirvan's crew page: seven films linking to YouTube with the video stills as posters (Caine's Arcade 1 and 2, The Box Man, The Three
   of Us, #EarthToParis, #EarthToMarrakech, The 1 Second Film trailer) and three links (interconnected.is, nirvan.com, imagination.org).
   He dictated "interconnectedmedia"; interconnected.is was used because it is the company's working site. To confirm.
   BUG FIXED (Nov 22): the saved site settings (`site_content` key `settings`: team order, crew profile edits, voices pins and hides,
   comment approval) were never read back on the live site, because the loader near "var CSET=" ran before `LIVE` is set further
   down the file. It now runs in a `setTimeout(...,0)`. Proven with a test that loads the page as whatatrip.com (scratch t68.js):
   before, zero settings requests; after, the saved order and a saved crew edit both show. Built-in team order updated to his latest.
   The same early-run problem was noted before in `seedLoad()` and has not been looked at again.
   Supporter list tabs: the connector lines (`bondsDraw`) were measured while rows were gliding and stayed wrong. They now hide during
   the glide (`.suplist.shuf`) and are redrawn 560ms later; scratch test t69.js compares the lines before and after Top/Recent/Top.
   A separate session, "Interactive fundraising progress bar" (name `progress-bar`), is building a standalone mockup at
   `whatatrip-site/mockups/progress-bar.html`; it must not edit the home page files and will hand over for integration.
   $100K perk reworded (Nirvan, relayed by the Stripe session): "Get listed as part of the filmmaking team on our website", with a small
   three-hexagon icon in the level box (`PKI.team`) and a drawn team-grid picture with "YOU" in it (`featArt('tm')`, a new `FEAT` card).
   The home page has no perk-card carousel at the moment, so that picture only shows where perk cards are rendered (perk details).
   SECTION ORDER (Nirvan, via the NIRVANA session, Nov 22): page and submenu are both Story, Perks, Filmmakers, Supporters, Challenges,
   Impact, Budget, FAQs, Voices, Updates. Done in the last build step of `build.py` (works on `out`): Budget and FAQs leave the left
   column and wait in `[data-bfhome]` after the Impact band; the Challenges home now comes before the Impact home; the submenu links
   are reordered there too. The fit script in app.js lifts Challenges, Impact, Budget, FAQs beside the perks in that order while they
   fit (at 1300: the first three). Scratch test t73.js compares menu order with scroll order at five widths.
   Honeycomb shuffle: while a honeycomb re-sorts or is filtered, `hvLift` adds `.shuf` to the hive so every hexagon casts a soft
   drop shadow and gets a varied z-index (they pass over and under each other); both are removed when the move ends.
   Submenu pill (`spy` in app.js): stays on Campaign until the bar is pinned and the page has scrolled 30px into Story, then slides
   to Story. Clicking Story holds it there (`HELD`) while the bar is pinned; scrolling back to the hero returns it to Campaign.
   Scratch test t76.js steps the scroll around the pin point and reads the active item.
   Team: built-in order is Nirvan first (as he saved it) and `TEAMFIRST='darren'` is the face highlighted on load.
   Crew films that link to YouTube open in an on-site player (`crewVideo`, youtube-nocookie embed, Esc closes, link out to YouTube for
   views). Nirvan's stills use the widescreen `mqdefault.jpg` (no black bars); added "A Love Letter from #EarthToParis". His links now
   include YouTube, X and Instagram (handles taken from nirvan.com), and any crew page with an Instagram name shows "Follow on Instagram".
   Live view counts are not shown (would need a YouTube API key held server-side).
   Join card: the hand now waves as the card opens, then again every ten seconds.
   Join hexagon: the level colours travel slowly around its edge (conic gradient on the ring, `@property --wja`) and it breathes a faint
   glow; both off for reduced motion. FAQs are never lifted beside the perks any more: below the Rick banner the order is always
   FAQs, Voices, Updates (checked on the live dev page: FAQs start 44px under the banner).
   Perk lists shortened (Nirvan, Nov 22): $5 reads "Your own supporter profile, with your photo and social links"; $50 and $250 list
   only their editing line plus "Plus everything in..."; the $25K perk is "Your photo featured in our supporter grids".
   BEHAVIOUR: in honeycomb grids a photo now shows only from the $25K level by giving or raising (`av()` adds class `lo` below that;
   CSS hides the image inside `.chhive`). Profiles, lists and preview cards still show everyone's photo. He said "maybe" to this rule,
   so it is flagged for him to confirm.
   Shirt counter: `shirtN(a)` = one Legalize Rick Inception shirt per $500, shown in the giving flow bullets ("Access to buy N
   shirts ... one for every $500"). The same note was passed to the Stripe checkout session.
   Trailer: `openTrailer(from)` now zooms. The Vimeo player is created at once (it starts loading within about 50ms of the click),
   covered by a copy of the preview card (`.tovp`) that grows from the card's position to the full player in 620ms while the page
   dims, then fades to the playing video. From the "Watch the trailer" button it grows out of the button. No zoom for reduced motion.
   Scratch test t82.js checks the start, middle and end positions.
   Trailer auto-close: a `message` listener trusts only https://player.vimeo.com messages from the trailer's own iframe; on "ready"
   it asks for the "ended" event, and on "ended" the overlay fades out and closes. Tested with a stand-in player (scratch t83.js),
   NOT yet with the real Vimeo player playing to the end.
   Trailer: confirmed against the REAL Vimeo player (scratch t84.js, Chrome): it reports "finish" and the window closes itself.
   `closeTrailer` now shrinks the player back into the preview card (or fades if the card is off screen).
   Join hexagon: first click shows the preview card; its button says "Join us" and opens `openJoin` (class `.jov`): Donate $5 or more,
   Start a fundraiser and raise $5 or more, Donate a perk (links to /contact for now). BUG FIXED in the hover card: clicking a
   hexagon focused it, and pressing the mouse on the card closed the card (focusout) before its button got the click.
   IDEA from Nirvan, not built: joining is free, but a profile is only activated and listed once the member has helped (gave,
   raised, offered a perk that raised money, or invited friends who gave). Needs a membership rule and database work.
   FAQs moved into the lower two-column block (first in `.cols.second>.stack`), so "More ways to help" sits beside them; then Voices,
   then Updates. FAQs got a two-line heading like Voices ("FAQs 11" label over "Questions and answers") so the two boxes start level
   (measured equal at 1024/1300/1440). `[data-bfhome]` now holds only Budget.
   Voices rows: new right column `.vside` with the editor menu or, for everyone else including guests, a flag (guests are asked to log
   in), and the reactions stacked under it. Nothing sits under the quote any more.
   MOCKUPS waiting on Nirvan (in `whatatrip-site/mockups/`, not in the repo, nothing built):
   - `after-trailer-hero.html`: what the trailer spot becomes after the trailer has been watched. Three versions: wide shot with
     supporter hexagons around Rick; close-up with hexagons beside him; close-up built out of supporter hexagons. Copy options:
     "Join us to help bring Rick's story to the screen." / "Be part of sharing Rick Doblin's legacy." Button becomes "Join us".
   - `join-us-popup.html`: three layouts for the Join us pop-up with four ways to help (Donate $5+, Start a fundraiser, Donate a
     perk, Start a matching challenge of $25K+). He decided against a "join for free" option.
   NOTE: on Nov 22 one test (scratch t84.js) launched the installed Google Chrome in the background to play the real Vimeo trailer.
   Nirvan saw a macOS permission prompt and asked to be told before any installed app is opened; use the bundled test browser only,
   and tell him first if an installed app is ever needed.
   AFTER THE TRAILER (Nov 22, Nirvan picked mockup 3 and refined it): when the trailer closes, the trailer spot becomes a photo
   mosaic of Rick's close-up made of supporter profile tiles (one hexagon each, initials, level colour). Sky and desert tiles keep
   much of their own colour; tiles over Rick take on his. Headline "Be part of sharing Rick Doblin's legacy." sits up in the sky;
   the purple "Join Us" button sits where the play button was and opens the Join us pop-up; "Watch the trailer again" bottom left.
   Hovering a tile turns it into a clear profile tile and shows the usual preview card; clicking opens the profile.
   Code: trailerAfter / vjDraw / vjRick in app.js, `.video .vj*` CSS. Shows after ANY close of the trailer, for that page view only.
   Also fixed: moving from one hexagon to the next no longer cancels the next preview card (site-wide).
   Join us pop-up redesign (layouts A/B/C in mockups/join-us-popup.html) still waits on his pick.
   COMMUNITY CREDIT (Nov 22, Nirvan): "Yet to be Named" community credit, brought over from the live /donors wall. It is the sum of
   every gift under $5,000 (named people by their total given, plus each anonymous gift), always added up from the gifts (commData).
   - A hexagon with the animated multicolour outline sits in the home Supporters grid, placed by its total; it is not counted as a supporter.
   - Its page (openComm -> openProfilePage(...,'community'); commMain/commSide/commHive/commList): total and count, a bar to $250K with
     the $100K mark, "At $100,000 Contributing Producer / At $250,000 Executive Producer", About, The name, and "Everyone in this
     credit" as a honeycomb with a Grid view / List view switch (search works on both; names open profiles).
   NOT built, waiting on Nirvan: (1) the "submit a name" form and later the vote: needs a new database table, ask before migrating;
   (2) the drawing for a trip to Arcturus (at $250K, and maybe at the $5 level): NOT on the site until a lawyer and Creative Visions
   sign off. Summary given to him: a paid-entry drawing is a raffle (California bans selling raffle tickets online); the workable
   route is a sweepstakes with a clearly disclosed free way to enter at equal odds (mail-in is the usual one; it cannot be hidden in
   the terms), official rules, and NY/FL registration if the prize is worth over $5,000. (3) No hover card on the credit's hexagon yet.
   Nov 22 evening, mosaic refinements from Nirvan (all built): the mosaic is already in place as the trailer shrinks back and eases
   out from a slight zoom (no tile-by-tile arrival); Rick's cut-out comes from the photo itself (VJM mask in app.js, made by scratch
   mkmask.js), so tiles over Rick are nearly clear with almost no initials and background initials are very faint; gaps between tiles
   show the photo with a violet wash (no dark lines); headline is now "Policy change needs science. / Culture change needs stories."
   centred above the purple Join Us button in the middle of the frame, with a small white "Watch the trailer again" button (play
   arrow) under it; all three sit above the tiles. Tiles radiate from the button, largest donors first, and within a level people with
   a testimonial come first; anonymous gifts are not tiles; tiles ignore the pointer until about a second after the picture settles.
   COMMUNITY CREDIT name ideas: form is live on the credit's page (idea + optional name). Migration `credit_name_ideas` applied
   Nov 22 with Nirvan's yes: anyone can insert, only Owner/Admin/Manager can read, Owner/Admin can edit or delete. There is no
   staff screen for the entries yet (read them with SQL), and the vote is not built.
   Nov 22 (Nirvan, relayed by the Stripe session): the shirt line in the giving pop-up is shortened to one line:
   "Access to buy N Legalize Rick Inception shirt(s) in our store" (the "one for every $500" detail is removed; the count is unchanged).
   Nov 22 late (Nirvan, relayed by the parent session): after-trailer copy and layout changed. The headline, Join Us and the rewatch
   button now sit in the open space left of Rick (wrapper `.vjw`), not in the centre. Copy writes on line by line after the image
   returns: "Changing psychedelic policy needs science. / Changing culture needs stories. / This story needs you."
   TO CONFIRM with Nirvan: his dictation began "Changing policy needs changing. Psychedelic policy needs science." which I read as
   a restart, so line 1 is my reading. The button is now "Rewatch the trailer", bottom of that left space (icon only when the hero
   is very small). Tiles radiate from wherever the Join Us button sits.
   Level colours (Nirvan): MAPS Makers ($500) is now an aqua blue (#d2eef2 / #7cc7d3 / #1d5d6b) so it no longer looks like Mile
   Markers ($250); the levels step red, orange, yellow, green, aqua, blue, indigo, purple from highest to lowest.
   Nov 22 late, from Nirvan (all on /home-dev):
   - Community credit page: grid on top with the list always under it (both follow the Largest/Recent sort; anonymous gifts are rows
     too). The credit's name sits in a field with a "Suggest a name" button; pressing it makes the field editable and shows Submit
     (with a lock when logged out). Logged out, Submit shows "You must log in to submit your name. This is for our members only.",
     a Log in button, "If you're not yet a member, you can join us for as little as $5." and "Donate $5 to join". The "your name"
     field is gone (the member's id is saved instead). About text rewritten to his wording with the live count and total in bold.
     OPEN: the database still accepts ideas from visitors who are not logged in (the page blocks it, the table does not). Ask Nirvan
     before the migration that limits inserts to signed-in members.
   - Larger filmmaker photos (home bio preview, hover card, crew page) have a 3px hexagon outline: white on the page, lavender on white cards.
   - TRY-OUT: in the hero the Matching Challenge Fund now sits above the Current Milestone (four `[data-hero]` order rules at the end
     of the CSS in build.py; delete them to undo).
   - He asked for mockups of the matching-fund icons (two linked hexagons with bold gift boxes; hexagon with two hearts): see
     whatatrip-site/mockups/matching-icons.html.
   Nov 22 late (Nirvan, relayed by the parent session), all on /home-dev:
   - The trailer starts closing about one second before it ends, measured from the video's own length (Vimeo timeupdate /
     playProgress events), so the suggested-videos screen is not seen. NOT verified against real playback: the bundled test browser
     cannot play the Vimeo video. Nirvan plans a shorter cut; nothing to change when he uploads it.
   - After-trailer headline is bigger and now reads "Changing policy needs science. / Changing culture needs stories. / This story
     needs you." (his later self-correction; still to confirm with him).
   - Preview cards on the hero mosaic choose a spot that never covers the headline, Join Us or the rewatch button (tested 56 hovers
     at 768, 1024, 1300, 1440).
   ASKED, not built yet: members posting updates on their profile with public/members/only-me visibility (needs a migration);
   Rick managing his own page and having an invite link (needs a member account linked to the crew page).
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
