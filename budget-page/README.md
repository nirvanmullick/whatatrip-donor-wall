# /budget — Film Budget page block

Since 2026-11-12 the /budget page code lives here (same set-up as `donate-page/`).

- `budget-block.html` — the full block (budget bar + Rough Cut and Final Cut budgets). Edit THIS.
- `VERSION` — the commit SHA the site loads (GitHub raw, ~5 min cache; file served from jsDelivr).
- `squarespace-loader-block.html` — the small block pasted into the /budget Code Block.

Publish: commit `budget-block.html`, push, write that commit's SHA into `VERSION`, commit, push.
Roll back: put an older SHA in `VERSION`.

Direct links: `/budget#rough-cut`, `/budget#final-cut`, and one per goal — `#editing-act-1`,
`#production-filming`, `#editing-act-2`, `#editing-act-3`, `#animation`, `#interviews-b-roll`,
`#music-archival`, `#admin-fees`, `#final-cut-editing`, `#color-grading`, `#sound-design-mix`,
`#score-music`, `#titles-vfx`, `#delivery-distribution`. The matching-pool settings in the bar are a
copy of `donate-page/donate-block.html`'s LIVE_MATCH — change both together.
