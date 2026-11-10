# QA Report — Deployment Build

## Result

**Passed for static prototype deployment.** The `dist/` build contains the app, five runtime data files, manifests, and the optimized assets used by the game. Original prompt packs, high-resolution source images, and working documents are not copied to the deployment folder.

## Checks performed

- Asset validator: 50 raster images readable and in expected formats/dimensions; 30 character sprites retain alpha; 7 SVGs parse; all active asset references resolve.
- Data/runtime checks: all five JSON data files parse; app JavaScript passes Node module syntax validation.
- Browser review: checked mobile-width and desktop-width layouts; dialogue text center matches the dialogue frame center in both axes; full 16:9 CG stays visible in the stage, with blurred side fill on wide screens; character sprites are placed by scene position metadata.
- Game flow: chapter navigation, dialogue advance, choice feedback, final quiz (10 questions), scored result, and restart.
- Static build: `python scripts/deploy/build_static.py` completed; output includes 57 runtime art files plus two manifests and is approximately 69.4 MB. Windows `desktop.ini` and source-only README files are excluded.

## Known product notes

- The user approved using all supplied pictures as-is. Scene 06 has people painted into the background, and the four CG outfits do not exactly match the sprite sheets; these were kept in the prototype per that instruction.
- Progress and scores are stored in local browser storage; there is no account sync or server-side save.
- A live public deploy has not been made because no hosting destination or domain was specified. The contents of `dist/` are ready for static hosting.
