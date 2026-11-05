# Actual render comparison against the earlier embedded reference boards

The four prior conversation images were visually inspected. Named PNG originals and the closer framing file were not attached to v3, so no pixel-difference or side-by-side source-image composite is claimed. All captures in evidence-v3 are actual runtime renders, not generated concepts.

| Area | Concrete change | Remaining difference from reference |
|---|---|---|
| Tank | Five wheels, storage, two team emblems, softer paint, lower turret | Still less sculpted; lacks reference panel complexity and fine painted material treatment |
| Walls | Two courses, chunky irregular blocks, individually varied tint, jagged crack markings | Less organic wear and richer ambient occlusion than the reference; top faces still overly regular |
| Date palms | Separate pointed leaflets, diamond trunk scales, dates, animated fronds | Foliage remains sparser and less layered than the reference |
| Houses | Parapet edges, raised corners, triangular vents, rafter ends, planked doors | Door lacks a true arched opening; Japanese layered tiles and Classic canopy house still need refinement |
| Perimeter | Repeated houses north/south, side palms, Najdi farm/rest group, Japanese pond/bridge | Repetition too obvious; some edge scenery clips outside the view and needs composition passes |
| HUD | Navy score pill/pause, orange fire, blue-grey joystick, rising true damage | Font/control proportions and emblem readability need physical-phone review |
| Motion | Actual ambient GLB clips loaded through animation mixers | Full watering, eating, fish paths/tails, cat stretch and all nuanced motions remain incomplete |
| Materials | Per-brick color variation and softer tank roughness | Full PBR texture atlases, grain normal detail, painted edge work and final soft contact lighting incomplete |

Mesh measurements: canonical tank 8524 triangles; Najdi palm 4752; intact wall 704. Helper currently reuses canonical mesh complexity and exceeds its 3–6k budget; this is outstanding. Per-asset measurements are in v3-asset-metrics.json.
