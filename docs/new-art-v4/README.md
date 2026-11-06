# New Najdi desktop asset set — v0.4

This revision uses 27 newly authored GLBs from authoring/najdi-v4.py, with editable .blend files under authoring/najdi-v4. The reference archive Tank.rar contains 13 image boards, not 3D model files. No images are presented as runtime models. Every matching old/new GLB hash was compared before the old files were removed; all differ. The legacy public/assets/models folder, legacy authoring generator and root-level legacy .blend sources have been removed from the current checkout. Git history preserves older revisions.

The renderer has a single exclusive model path: assets/najdi-v4. Its camera is now angled across the arena. New masonry, tracked tanks, date palms, buildings, canopy fabric, crops, pots, seated characters, golden flag and power badges replace the former model set. Sand has a newly generated 1024px ripple texture. Wall direction and crossing meshes follow grid adjacency instead of displaying isolated horizontal fragments.

Desktop distribution contains PLAY.bat, start.mjs, bundled relay.cjs and compiled web files. Node 24+ is the only external prerequisite. There is no npm install/build step for the recipient. On Windows the launcher opens the default browser and keeps the local server running. The BAT file has not been executed on Windows; the same Node entrypoint was run from a clean extracted archive on Linux, and index + new GLBs returned HTTP 200. Archive hashes and the absence of legacy model paths were checked.

Production build and 16 headless tests passed. Actual browser asset-viewer and simultaneous emulated touch movement/fire passed. Actual Najdi active-match run reported no page errors. Physical Windows double-click, phone performance, native Kids Hug integration and manual audio listening are unverified. No owner approval or exact visual match is claimed. Images copied here are actual runtime captures; low quality software rendering disables shadows and does not demonstrate final hardware performance.

The simulation is still the flag race with keyboard movement/fire, collision, destructible walls and pickups. Core mechanics were retained; no unsupported claim of an entirely new ruleset is made.

Final post-junction-fix active match check: PASS, phase playing at tick 108, no page errors. Final ZIP re-read verification: all internal hashes match, 27 GLBs, PLAY.bat present, no legacy assets/models directory. No source runtime npm modules are required in the exported package.
