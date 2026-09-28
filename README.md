# What a Trip donor feed (v2)

`scrape.js` reads Pledge's own JSON donation feed for https://www.pledge.to/whatatrip. That's the
same data Pledge's page loads when you scroll its list. It writes `donors.json`, and both the
donate page and the donor wall read that file.

- Every run reads at least 20 gifts, then keeps going until it reaches a gift already in
  donors.json. The daily run at 09:17 UTC reads the whole list.
- Gifts are merged by Pledge's gift id. Nothing already in the file is ever removed.
- The "Match" rows are folded into the gift they match, so each gift has one row with `matched: true`.
- If a donor chose Anonymous on Pledge, no name is written for them.
- If Pledge can't be read, the run fails (it shows red in Actions) and donors.json is left as it was.
- No browser and no npm packages are needed. A run takes about 10 seconds.

## To install (one time)
1. In the GitHub repo `nirvanmullick/whatatrip-donor-wall`, replace `scrape.js`, `package.json`
   and `.github/workflows/scrape.yml` with the files in this folder. You can drag them onto
   "Add file → Upload files". For the workflow, open the existing file and paste over it.
2. Go to Actions → "Scrape donor wall" → Run workflow. Leave "full sync" ticked.
3. Check that donors.json now has about 27 gifts, each with an `id` and a `ts`.
