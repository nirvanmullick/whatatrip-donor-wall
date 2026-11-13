# /donors — the donor wall

Since 2026-11-12 the donor wall code lives here (same set-up as `donate-page/` and `budget-page/`).

- `donors-block.html` — the BUILT wall (do not edit by hand). It is built from the source in
  `whatatrip-donorwall-SOURCE.zip` in Nirvan's project folder: `python3 build_full.py` writes
  `whatatrip-donorwall-FULLWIDTH-MASTER.txt`, which is copied here.
- `VERSION` — the commit SHA the site loads. `squarespace-loader-block.html` — the small block in Squarespace.

Publish: commit `donors-block.html`, push, write that commit's SHA into `VERSION`, commit, push.
