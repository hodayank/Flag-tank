# Verification and remaining work

Version: 0.1.0-alpha.1. Environment: Linux cloud workspace; Node 24.22.1, Python 3.12.14, Blender 4.3.2, installed Chromium with SwiftShader. No physical Android or Kids Hug devices were available. No manual audio listening is claimed.

## Verified capabilities

- A real TypeScript/Three.js project and lockfile; clean `npm ci` completed.
- TypeScript checks and production build pass after correcting a viewer top-level-await compatibility issue.
- Fifteen simulation tests pass. They exercise all three map layouts (symmetry, connectivity, wall density, spawn pockets), deterministic fixed-step state, vector-normalized acceleration, collision sliding, projectile sweeps, two-hit persistent wall damage, occupied rebuild postponement, tap/hold distinction, expiring auto/rapid, friendly pass-through, health/respawn/protection, rocket charges, persistent/no-respawn helpers, flag scoring and sudden death, pause/stale input, and packet shapes.
- 74 runtime GLB files and corresponding editable Blender sources pass existence, glTF header/length/mesh checks. Canonical tank node hierarchy is checked. 65 real PCM WAV files pass format/existence checks. These checks do not establish visual fidelity or pleasant audio.
- Development relay protocol checks pass with two independent WebSocket clients: atomic remaining seat, room-full response, hash mismatch rejection, matching initial state, stale-match rejection, coordinated pause/resume, disconnect pause, rematch reset. Invalid packet shape checks are separate simulation tests.
- Runtime screenshots come from the actual game, not generated concept art or catalog crops. See final browser results below; earlier iterations were disrupted by hot reload and were not counted as passing runs.

## Production limitations

This is a functional prerelease, not the complete premium game requested. Outstanding independent production work includes:

- Reference-quality sculpting, grain and material refinement; richer decorative perimeter; accurate Najdi boys, farmer, calico cat, tiled roofs, shelter and botanical silhouettes. Generated geometry is dimensional but several props are still simplified, and some shared effects use generic catalog meshes.
- Wall corner/T-junction files now have dedicated modular silhouettes; they still need reference-quality refinement. Logical maze rendering currently uses the aligned intact/cracked/rubble cell variants.
- Complete animation data and glTF clips; current motion is code-driven. Track wheels, recoil, flag motion, sway and particles exist, but full tread animation, suspension, koi paths/tails, watering, seated gestures, cat breathing/stretching, nuanced cloth and water animation are incomplete.
- Circular conservative hull collision rather than oriented rectangular dimensions; helper avoidance/aim quality and long-match fairness need human playtesting; exact sub-tick flag entry timing is not implemented.
- Several configured pickup parameters remain fixed in the simulation rather than independently tunable fields. Main sound catalog has complete local files but several effects share procedural character; original music loops are 48 seconds, not professionally mixed/listened-to final music. Five audio buses exist. Motor load/tread layering and priority ducking are incomplete.
- Native Kids Hug handshake, discovery, invitations outside the game, authenticated native transport, save/load and full invitation error-state UX require the actual host. The proposed contract and isolated mock are provided, not verified against an APK.
- Relay reconnect token survives only the current game controller session. Full refresh/rejoin persistence, explicit invitation expiry/cancel/decline/busy policy and comprehensive abuse/rate limiting are not production-ready. No internet multiplayer is advertised.
- Handshake hashes build/balance/map and the full resource inventory; Ready verifies each resource. This gate was added after the first protocol/browser run and is checked separately in the final validation. Package integrity also covers every distributable file independently.
- All numeric config files have schemas and runtime settings checks; full map/manifest JSON schema validation is incomplete.
- Resource cleanup is implemented at page exit and clears match scene membership, audio loops, labels and input on restart. Exhaustive heap/GPU leak testing over many restarts remains unrun; owned geometry, instance buffers, ground textures, ghost materials and loop gain nodes are explicitly released; exhaustive heap/GPU accounting still needs a further audit.

## External prerequisites and untested acceptance

Missing attachment: `TankFlags-Codex-Complete-Prompt-v2.md`. Missing native Kids Hug source, loader and transport. No native discovery acceptance, two physical device LAN acceptance, physical multi-touch verification, phone FPS or WebView compatibility claim. Browser screenshots and protocol tests are not substitutes. The available browser uses CPU software rendering; high-quality shadows are very slow here. `?quality=low` reduces pixel ratio and disables shadow maps for constrained rendering; hardware performance targets are unverified.

No public preview was published. Use README commands to serve compiled output locally. Environment draft persistence/publication and fresh-task snapshot restoration must be reported separately.

## Final browser and relay results

- Production three-theme browser run: PASS, no page errors. Active Najdi flag state and keyboard fire exercised; Classic and Japanese scenes loaded and captured.
- Final two-browser production run: PASS, no page errors. Create/join/ready with complete resource verification, same match ID, active play, shared pause/resume.
- Final relay protocol recheck: PASS with matching rebuilt resource inventory. A prior retry correctly failed while the relay retained an older inventory; restarting it after the build resolved that setup mismatch.
- Browser captures used installed Chromium/SwiftShader and reduced quality. They are real runtime evidence, not evidence of final visual approval or mobile frame rate.
- Fifteen simulation tests pass; no skipped or expected-failure tests.
- Full clean lockfile installation was performed. Final source-archive extraction/build and archive integrity results are recorded below after execution.

Environment `install_script` and `start_skill` were saved successfully as a draft. Publication and fresh-task restoration have not been performed or verified.

## Final delivery checks

- Source ZIP clean extraction: PASS. `npm ci --offline`, production build, all 15 tests and asset checks completed from the extracted project using the existing npm cache.
- Rebuilt compiled files byte-match the prepared distribution.
- Final `.khgame` and compiled web ZIP contents were re-read and every `integrity.json` SHA-256 entry verified. Archive hashes are in `artifacts/SHA256.json`; they change if documentation/evidence is repackaged.
- Asset viewer captured the real canonical tank and intact/cracked/rubble models. Automated emulated multi-touch successfully moved and fired simultaneously. Physical touch remains untested.
- `rebuild-ghost-fixture.png` uses an explicitly labeled injected development simulation state at 8.5 seconds after destruction; it demonstrates the actual runtime telegraph, not a recorded natural match sequence.

- Final restart check: PASS, three actual UI match restarts held renderer counts at 132 geometries and one texture on each measured iteration. This is bounded-resource evidence for that sequence, not an exhaustive leak proof.
