# Production brief v3 — intermediate revision

Build 0.2.0-intermediate.1. This document supersedes previous verification claims for changed assets and code. The full requested production scope is NOT complete. See v3-coverage.md for every supplied requirement and explicit outstanding work.

Implemented changes: redesigned two-course masonry with individual tint and corner variation; 704-triangle intact wall; five-wheel tank with storage, separate insignia and paint edge accents; pointed multi-leaflet date palms; improved houses, character face/clothing details and watering-can prop; recognizable shield/bullet/rocket/auto/helper badges; ambient GLB animation clips and runtime mixers; much denser themed perimeter; navy HUD, orange fire control, floating applied damage; ice-blue pulsing rebuild; opposite-side camera and input mapping for guest; helper 0.85 speed and 0.15 m rebuild clearance; WAV source generation at 48 kHz; proposed typed v1 host interface and guarded injection adapter.

Initial checks: production build, TypeScript and 16 tests passed; 74 primary GLBs and 65 WAVs passed existence/format checks. The new SDK test verifies missing methods are rejected; it is not native integration acceptance. All WAV sample rates were inspected as 48000 Hz. No manual listening claimed.

Visual observations from actual browser captures: tank storage, hub count and silhouette improved, but paint/material and sculpt detail still fall short of the reference. Perimeter now populated north/south and sides, but remains more repetitive and less organic than the reference. Low-detail decimation visibly damaged masonry edges, so it was removed from runtime selection; low quality now preserves the full model. Phone framing/readability and richer scenic groups still need refinement. Newly authored ambient clips are not substitutes for all requested character actions.

No named reference PNG files or closer 01 WIDE file were attached with v3. Earlier embedded images were inspected; reference files are not falsely claimed as present in the repository. Native source, real host SDK and physical devices were not supplied. Phone performance, physical touch, native discovery and audio listening remain untested. Two-client browser networking was verified on the older revision; it needs rechecking for the opposite-side camera changes. Native production support remains false.

Final command results and captures are appended only after they complete. Package inventories and archive hashes are generated after the last build. Historical downloads remain separate from this intermediate revision. No owner approval is implied.

Final mesh measurements: canonical tank 8524 triangles (within 4–10k); date palm 4752 (within 2–6k); intact wall 704 (within 100–800). Helper still shares canonical complexity and exceeds its requested budget. See v3-asset-metrics.json.

The final production build and all 16 tests passed. All 74 primary GLBs and 65 WAV files passed the existing structural checks. An actual browser run loaded all three themes with no page errors and emulated simultaneous movement/fire passed. Final opposite-camera two-browser results are appended after completion, not inferred from prior versions.

Final v3 two-browser check: PASS, no page errors. Create/join/ready, identical match ID, shared pause/resume and opposite camera positions were asserted. Final asset viewer/touch-emulation check: PASS, no claim of physical touch. The separate test relay used port 8788; ordinary launch defaults remain documented on 8787.
