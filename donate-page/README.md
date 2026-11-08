# /donate — Film Budget + Donations block

Since 2026-11-08 the big budget + donor-wall code for whatatrip.com/donate lives here instead of
inside the Squarespace Code Block.

- `donate-block.html` — the full block (HTML + CSS + JS). Edit THIS, never the Squarespace block.
- `VERSION` — the commit SHA the site loads. The site fetches VERSION (GitHub raw, ~5 min cache), then
  loads `donate-block.html` at that exact commit from jsDelivr (fast CDN, cached by browsers).
- `squarespace-loader-block.html` — the small block that sits in Squarespace. It waits for the Pledge
  form to load first, then inserts this code. Only needs re-pasting if the loader itself changes.

## Publishing a change
1. Commit the new `donate-block.html` and push.
2. Write that commit's full SHA into `VERSION`, commit, push. Live within ~5 minutes.
   (Two commits because VERSION has to name the commit that holds the new file.)
3. Roll back = put an older SHA in VERSION.

The source of truth on Nirvan's computer stays `whatatrip-donate-CURRENT-MASTER.txt` (same content).
