from pathlib import Path
import json
brief=Path('docs/production-brief-v3.txt').read_text()
rows=[]
for line in brief.splitlines():
 s=line.strip()
 if not s or s.startswith('=') or s in ['ROLE','ATTACHED REFERENCES (keep filenames, map to IDs; inspect every image; if one is missing, say exactly which)']:continue
 if s.startswith('PART ') or (s[:1].isdigit() and len(s)<100):continue
 status='unverified';note='Some supporting implementation exists; the complete requirement is not verified. See the explicit gaps below.'
 if 'native source' in s or s.startswith('This is a draft') or s.startswith('Implement typed interface'):
  status='blocked' if 'native source' in s else 'unverified';note='src/host-v1.ts supplies a typed proposed interface and injection adapter; actual host source and connected native path absent.'
 rows.append('| '+status+' | '+s.replace('|',' / ')+' | '+note+' |')
Path('docs/v3-coverage.md').write_text('''# Production brief v3 coverage — intermediate, not final acceptance

The supplied brief is preserved verbatim in production-brief-v3.txt. Status applies to the WHOLE listed requirement, not just the presence of a similarly named function. Unverified includes partial implementation; it must not be read as complete.

## Verified in this revision

- TypeScript compilation, production build, headless simulation tests and primary GLB/WAV existence checks. Individual runtime and browser checks are recorded in v3-verification.md.
- Previous revision browser/network results are historical and are not automatically claimed for this revision.

## Explicit outstanding requirements

- Exact reference fidelity remains unverified: named reference PNGs and closer framing file are not present as workspace attachments; only the four earlier conversation images were seen.
- Native host source/SDK/loader/discovery is absent. New typed host contract is not yet connected to the game controller or the development relay through one common adapter.
- Authority still resides in the development relay, not in the room creator as v3 explicitly requires. The exact new protocol envelope, aggregate rate limiting and full invitation lifecycle are not implemented.
- Conservative circular hull remains, rather than required rectangular hull. Exact swept flag entry-time ties remain unimplemented. Map safe pockets are clipped at the interior edge, not a full 3x3 interior region.
- Art is procedural intermediate work. Not every detailed prop matches its reference. Dedicated boundary straight/corner/end suffix files, shared damage/disable/shadow models and every requested specialized FX are not complete. Houses, tiled roofs, porcelain patterns, arched bridge and scenic groups need more authoring. Several animation requirements remain missing despite new ambient clips.
- Audio files are original procedural WAVs; final perceptual quality, exact S-/A-/M- catalog names, compressed variants, speed layering, limiter/ducking and all sound priorities are incomplete or unverified. Manual listening was not performed.
- Config naming/migrations/full schema constraints and every tunable default do not yet match v3. Flag fallback and repeat exclusion history, exact helper avoidance and respawn fallback region remain incomplete.
- Native package manifest schema/min_host_api/age_range need reconciliation with the absent loader. The intermediate package still declares development LAN permission rather than the requested final permissions []. It must not be treated as a native-approved package.
- No physical phone, two native devices, measured mobile FPS, phone/headphone listening or owner visual approval.

## Requirement-by-requirement audit

| Status | Supplied requirement | Evidence / limitation |
|---|---|---|
'''+ '\n'.join(rows)+'\n')
