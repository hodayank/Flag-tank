# Requirements coverage

This is a prerelease implementation, not owner-approved final production art.

| Brief section | Coverage / limits |
|---|---|
| 1. PROJECT IDENTITY AND REQUIRED OUTCOME | Browser project and packages; native acceptance pending |
| 1. A playable standalone browser version. | Browser project and packages; native acceptance pending |
| 2. The complete editable TypeScript project. | Four embedded images inspected; Complete-Prompt-v2 missing |
| 3. Actual 3D models, textures, animations, effects, and audio. | TypeScript, Three.js, fixed-step simulation, relative production build |
| 4. All three fully implemented visual themes. | Procedural dimensional art implemented; substantial reference-quality refinement remains |
| 5. Functional game rules and multiplayer architecture. | Editable Blender files and GLBs; several shared FX IDs remain generic meshes |
| 6. A .khgame package for Kids Hug integration. | All catalog file IDs generated; specialized prop/character fidelity incomplete |
| 7. Full source and authoring assets in a clearly organized ZIP. | Three concrete symmetric connected JSON maps; camera fit |
| 8. Build, test, packaging, and integration instructions. | Countdown, score, fair path-cost placement, sudden death |
| 9. An honest verification and remaining-work report. | Keyboard, analog touch, independent pointers; physical touch untested |
| 2. REFERENCE IMAGES AND PRIORITY | Four embedded images inspected; Complete-Prompt-v2 missing |
| 1. My latest explicit instructions. | Browser project and packages; native acceptance pending |
| 2. This implementation brief and its explicit updates. | Four embedded images inspected; Complete-Prompt-v2 missing |
| 3. The attached complete production specification. | TypeScript, Three.js, fixed-step simulation, relative production build |
| 4. Images for appearance, materials, silhouettes, lighting, framing, and environmental detail. | Procedural dimensional art implemented; substantial reference-quality refinement remains |
| 5. Older prototypes only as potentially reusable mechanics references. | Editable Blender files and GLBs; several shared FX IDs remain generic meshes |
| 3. TECHNICAL IMPLEMENTATION | TypeScript, Three.js, fixed-step simulation, relative production build |
| 4. VISUAL QUALITY TARGET | Procedural dimensional art implemented; substantial reference-quality refinement remains |
| 5. CREATE ACTUAL 3D ASSETS | Editable Blender files and GLBs; several shared FX IDs remain generic meshes |
| 6. ASSET IDS AND THE THREE THEMES | All catalog file IDs generated; specialized prop/character fidelity incomplete |
| 7. CAMERA AND MAP DESIGN | Three concrete symmetric connected JSON maps; camera fit |
| 8. MATCH RULES | Countdown, score, fair path-cost placement, sudden death |
| 9. MOVEMENT AND INPUT | Keyboard, analog touch, independent pointers; physical touch untested |
| 10. FIRING AND PROJECTILES | Tap/hold/auto, swept collision; simulation tests |
| 1. Tap: | Browser project and packages; native acceptance pending |
| 2. Held fire: | Four embedded images inspected; Complete-Prompt-v2 missing |
| 3. Temporary auto-fire pickup: | TypeScript, Three.js, fixed-step simulation, relative production build |
| 11. HEALTH, DISABLE AND RESPAWN | Health, disable, safe respawn, protection |
| 12. WALL DAMAGE AND REBUILD | Two-hit walls, permanent cracks, occupied rebuild postponement |
| 13. POWERUPS AND HELPER | Five pickups and persistent helper; AI needs playtesting |
| 14. ANIMATION AND EFFECTS | Recoil, cloth motion, particles, environmental sway; character/track/water animations incomplete |
| 15. AUDIO: ACTUAL FILES, MODERN QUALITY | Original WAV catalog and three loops; timbre quality and manual listening not verified |
| 16. INVITATION, LOBBY AND MATCH FLOW | Development create/join/ready flow; native invitation delivery absent |
| 1. A child or parent opens Games → Tank Flags. | Browser project and packages; native acceptance pending |
| 2. Create invitation / Join invitation entry. | Four embedded images inspected; Complete-Prompt-v2 missing |
| 3. Creator requests a two-player room. | TypeScript, Three.js, fixed-step simulation, relative production build |
| 4. Host sends invitation to eligible Kids Hug devices on the LAN, including parents and children according to host policy. | Procedural dimensional art implemented; substantial reference-quality refinement remains |
| 5. Receiver sees: | Editable Blender files and GLBs; several shared FX IDs remain generic meshes |
| 6. Invitation can arrive while the receiver is outside the game. | All catalog file IDs generated; specialized prop/character fidelity incomplete |
| 7. First valid acceptance claims the remaining seat atomically. | Three concrete symmetric connected JSON maps; camera fit |
| 8. Later simultaneous acceptances receive room-full. | Countdown, score, fair path-cost placement, sudden death |
| 9. Both players enter the same lobby. | Keyboard, analog touch, independent pointers; physical touch untested |
| 10. Show both player slots, connection state, selected theme, duration, and readiness. | Tap/hold/auto, swept collision; simulation tests |
| 11. Creator proposes Najdi, Basic, or Japanese. | Health, disable, safe respawn, protection |
| 12. Guest sees the selection and explicitly readies. | Two-hit walls, permanent cracks, occupied rebuild postponement |
| 13. A setup change clears both readiness states. | Five pickups and persistent helper; AI needs playtesting |
| 14. Both clients load the selected assets. | Recoil, cloth motion, particles, environmental sway; character/track/water animations incomplete |
| 15. Both verify matching build, config, and map versions/hashes. | Original WAV catalog and three loops; timbre quality and manual listening not verified |
| 16. Ready is blocked on load or compatibility failure. | Development create/join/ready flow; native invitation delivery absent |
| 17. Exactly two confirmed ready players trigger a shared three-second countdown. | Typed proposed host contract and isolated mock; real adapter absent |
| 18. Match begins from the same authoritative state/tick. | Server authority, authenticated connection seats, sequences, reconnect pause; browser relay only |
| 19. Match ends with the same scores and result. | Balance used; visual/camera/audio settings are integrated; full schema coverage is incomplete |
| 20. Offer Rematch / Change theme / Exit. | ZIP-compatible package, SHA-256 integrity; native capabilities explicitly false |
| 21. Rematch uses a new match ID and seed and clears old state. | Implementation and actual-browser checks; visual acceptance not claimed |
| 17. KIDS HUG CONTRACT AND STANDALONE DEVELOPMENT | Typed proposed host contract and isolated mock; real adapter absent |
| 18. AUTHORITATIVE NETWORKING | Server authority, authenticated connection seats, sequences, reconnect pause; browser relay only |
| 1. Validate/accept inputs. | Browser project and packages; native acceptance pending |
| 2. Rotate/move with collision. | Four embedded images inspected; Complete-Prompt-v2 missing |
| 3. Accept legal shots. | TypeScript, Three.js, fixed-step simulation, relative production build |
| 4. Sweep projectiles. | Procedural dimensional art implemented; substantial reference-quality refinement remains |
| 5. Apply damage/disable. | Editable Blender files and GLBs; several shared FX IDs remain generic meshes |
| 6. Resolve flag and pickup collection. | All catalog file IDs generated; specialized prop/character fidelity incomplete |
| 7. Update timers and safe wall rebuild. | Three concrete symmetric connected JSON maps; camera fit |
| 8. Check match end. | Countdown, score, fair path-cost placement, sudden death |
| 9. Emit events and snapshots. | Keyboard, analog touch, independent pointers; physical touch untested |
| 19. EXTERNAL CONFIGURATION | Balance used; visual/camera/audio settings are integrated; full schema coverage is incomplete |
| 20. .KHGAME PACKAGE | ZIP-compatible package, SHA-256 integrity; native capabilities explicitly false |
| 21. IMPLEMENTATION PROCESS | Implementation and actual-browser checks; visual acceptance not claimed |
| 1. Inspect references and available source. | Browser project and packages; native acceptance pending |
| 2. Create a concise requirements coverage matrix. | Four embedded images inspected; Complete-Prompt-v2 missing |
| 3. Set up reproducible source/build/configuration. | TypeScript, Three.js, fixed-step simulation, relative production build |
| 4. Implement a small Najdi scene at the intended final quality: | Procedural dimensional art implemented; substantial reference-quality refinement remains |
| 5. Inspect the running result against the reference. | Editable Blender files and GLBs; several shared FX IDs remain generic meshes |
| 6. Improve observed visual deficiencies. | All catalog file IDs generated; specialized prop/character fidelity incomplete |
| 7. Continue full simulation, all powerups/helper, all three maps and environment assets. | Three concrete symmetric connected JSON maps; camera fit |
| 8. Implement full invitation/lobby flow and networking adapters. | Countdown, score, fair path-cost placement, sudden death |
| 9. Test and repair. | Keyboard, analog touch, independent pointers; physical touch untested |
| 10. Build and verify all delivery packages. | Tap/hold/auto, swept collision; simulation tests |
| 22. REQUIRED VERIFICATION | See verification report; native devices and phone performance untested |
| 23. FINAL DELIVERY | See artifacts directory and README |
| 1. Full editable TypeScript source ZIP. | Browser project and packages; native acceptance pending |
| 2. Separate compiled playable web ZIP. | Four embedded images inspected; Complete-Prompt-v2 missing |
| 3. .khgame package. | TypeScript, Three.js, fixed-step simulation, relative production build |
| 4. Actual runtime GLB models/textures/audio. | Procedural dimensional art implemented; substantial reference-quality refinement remains |
| 5. Editable authoring sources and generation/export scripts. | Editable Blender files and GLBs; several shared FX IDs remain generic meshes |
| 6. All configuration/map files and schemas. | All catalog file IDs generated; specialized prop/character fidelity incomplete |
| 7. Typed SDK contract and adapters. | Three concrete symmetric connected JSON maps; camera fit |
| 8. Isolated development mock. | Countdown, score, fair path-cost placement, sudden death |
| 9. Separate development host/relay if implemented. | Keyboard, analog touch, independent pointers; physical touch untested |
| 10. Asset/audio manifests and licenses. | Tap/hold/auto, swept collision; simulation tests |
| 11. Integration guide. | Health, disable, safe respawn, protection |
| 12. Build/test/preview/package instructions. | Two-hit walls, permanent cracks, occupied rebuild postponement |
| 13. Actual-game comparison screenshots. | Five pickups and persistent helper; AI needs playtesting |
| 14. Verification report. | Recoil, cloth motion, particles, environmental sway; character/track/water animations incomplete |
| 15. Known issues and exact blockers. | Original WAV catalog and three loops; timbre quality and manual listening not verified |
| 16. Build/package hashes and version information. | Development create/join/ready flow; native invitation delivery absent |
| 24. COMPLETION STANDARD | Not claimed complete; known production gaps documented |
