> **Current revision: 0.2.0-intermediate.1 — incomplete production scope.** Read [v3 verification](docs/v3-verification.md), [full requirement audit](docs/v3-coverage.md), and [visual comparison](docs/v3-comparison.md). Older verification documents describe the previous release and are historical.

# Tank Flags · 0.2.0-intermediate.1

An editable Three.js/TypeScript browser prerelease for Kids Hug. Two humans race to shared flags; there are no bases and no return-to-base scoring. **This is not a finished production game or a verified native Kids Hug integration.** See [verification](docs/verification.md) and [coverage](docs/coverage.md).

## Run

Prerequisites: Node 24 (validated: 24.22.1), npm 11, Python 3.12 with Pillow, Blender 4.3.2 for asset regeneration. Existing runtime assets are included; Blender is not needed for normal development.

```sh
npm ci
npm run dev
```

Open the local Vite server in your browser. Same-keyboard development mode: player one WASD/arrows and Space; player two IJKL and Enter. This is explicitly development testing. Touch controls operate player one. On portrait screens the entire arena remains visible; landscape is recommended.

For two separate browser clients on a trusted LAN:

```sh
npm run relay
npm run dev
```

Open the Vite server from each device, using the server computer's LAN address. Create an invitation on one browser, enter its six-character code on the other, and both press Ready. Allow TCP 5173 and 8787 on your local firewall where appropriate. The relay URL defaults to the current hostname on port 8787; `?relay=wss%3A%2F%2Fyour-approved-relay` overrides it. HTTPS pages require WSS. Do not expose the development relay to the public internet. It is a separate development host with bearer reconnect seats, not native authenticated Kids Hug networking. The second player must use a separate browser page/device, never a synthetic timeout peer.

The creator can change the theme in the lobby; this clears both readiness flags. A disconnected seat can reconnect using the same browser session and room within 20 seconds. A disconnected match pauses; resume explicitly after reconnection. Refresh recovery is not yet supported. Reconnect grace expiry ends as interrupted with no winner.

## Build, validate, inspect, package

```sh
npm run typecheck
npm test
npm run assets:build
node scripts/asset-check.mjs
npm run build
npm run preview
npm run package
```

The asset build regenerates original Blender sources, GLBs, textures, PCM WAVs, artwork icons, and three map JSON files. It does not download assets. Generated art uses fixed seeds. Blender export timestamps make source files not byte-identical between runs; archive contents have a separately verified hash manifest.

`npm run preview` serves the compiled build; `viewer.html` is a development asset viewer with orbit controls and sound audition. The separate relay still requires `npm run relay`. Production HTML/assets use relative URLs and no runtime CDN. Serve HTTP rather than opening HTML via `file:`. Browser audio starts after a user gesture.

The package command creates:

- `artifacts/tank-flags-0.2.0-intermediate.1-source.zip` — one editable project root, includes authoring sources and generation scripts.
- `artifacts/tank-flags-0.2.0-intermediate.1-web.zip` — one compiled web root.
- `artifacts/tank-flags-0.2.0-intermediate.1.khgame` — ZIP-compatible package with manifest and SHA-256 integrity.
- `artifacts/SHA256.json` — final archive sizes and hashes.

No dependency on absolute workspace paths exists in these outputs. The relay is excluded from the game package. Source ZIP excludes node_modules, distribution and other ZIPs. `integrity.json` hashes all package files except itself. Hashes are integrity checks, not publisher signatures.

Additional automated checks (Chromium must be installed):

```sh
# Start npm run preview -- --port 4173 and npm run relay first.
node scripts/browser-check.mjs
node scripts/browser-lan.mjs
node scripts/relay-check.mjs
```

## Project layout

- `src/simulation.ts`: 30 Hz authority, independently testable without WebGL.
- `src/collision.ts`: circle/box movement and swept projectile intersections.
- `src/render.ts`: GLB loading, static geometry merging, instanced wall states, camera, shadows and cosmetic effects.
- `src/input.ts`: keyboard and independent touch pointer capture.
- `src/audio.ts`: local decoded WAVs, loop lifecycle and capped master gain.
- `src/relay.ts`, `protocol.ts`: standalone development rooms and validated intent protocol.
- `src/host.ts`: proposed typed host API and isolated mock; no supplied native implementation.
- `public/config`, `public/maps`: versioned settings and three concrete maps.
- `authoring`: editable `.blend` models and original procedural generation.
- `public/assets`: actual runtime GLBs, texture, audio, metadata and provenance.

## Trial balance and units

All balance fields are read at runtime. Distances are meters; speeds m/s; accelerations m/s²; angular speed radians/s; timer and interval values seconds; gains linear 0–1; rates Hz. Positions are XZ with +Y up and +Z tank forward. `turnSpeed` is 300 degrees/s expressed as radians. Collision uses a conservative circular hull (radius .76 m), not the exact 1.2×1.5 m oriented rectangle requested; this is a documented mechanical deviation.

Balance defaults: 180 or 300 seconds, three-second countdown, 60-second sudden death; 100 health, 25 damage; two-hit walls, ten-second safe rebuild, 2.5-second ghost; .16-second tap cap, .43-second hold and auto intervals; projectile 17 m/s, three-second lifetime. Shield absorbs two shots or lasts five seconds; rapid divides firing intervals by 1.15 for eight seconds; rockets affect the next two shots or eight seconds; auto lasts eight seconds. Helper has 50 health, no automatic respawn and no lifetime limit. Main buffs replace one another; helper is independent. Trial defaults are adjustable, not owner-approved final balance.

Map cell units are 2 m on a 27×17 grid. The three themes share geometry, spawn cells and candidates. Wall occupancy is 45.1% of interior cells; paths remain connected. Flag candidates are ranked by both players' path costs, with breakable-wall cost and a previous-location penalty, then authority-seeded tie variation. Exact simultaneous entry timing is not yet tracked; same-tick collection uses proximity then seeded tie breaking.

Visual/camera/audio settings drive the runtime, but not every target quality mode is implemented. JSON schemas cover numeric settings; map/manifest schema coverage is still partial. Compatibility hashes a source-build fingerprint, balance, map and the complete resource inventory. Ready verifies resource bytes, including models, audio, textures, font and configuration. SHA-256 has a local JavaScript fallback for HTTP LAN origins.

## Original assets and licenses

Project code and original generated asset sources are provided under the MIT license in `LICENSE`. Geometry is authored by `authoring/build.py`; audio, texture and icon generation by `authoring/audio.py`. No supplied catalog image is used as a runtime sprite, background or texture. Each runtime model has an editable Blender file and manifest entry. Runtime effects are principally code-driven; several generic shared effect GLBs are catalog placeholders and must be replaced before production acceptance. Third-party npm packages retain their upstream licenses; see lockfile and installed package license files. No national or religious emblem appears on the golden flag.

## Missing source material

The referenced `TankFlags-Codex-Complete-Prompt-v2.md` and Kids Hug native application source were not supplied. The pasted implementation brief and four embedded reference images were available. Exact audio catalog IDs and native API compatibility cannot be verified without the missing material.

Low quality mode (`?quality=low`) uses authored decimated wall LODs, reduced pixel ratio and no shadow maps. Font assets include the bundled DejaVu license. Restart the relay after rebuilding public assets/configuration because its inventory is loaded at process startup.
