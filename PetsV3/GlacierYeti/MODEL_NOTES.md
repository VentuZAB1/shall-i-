# Glacier Yeti - model notes (model gate, 2026-10-27)

File: `pets/GlacierYeti.py` (model + biped rig with arm IK + check_pairs / joints, no clips yet).
Tris: 5,076. Size (Blender units) 1.58 x 1.17 x 1.65. HEIGHT 9.0 studs = bbox top (head). PITCH 0.0411
(same world stud size as the Raiju).

## What I built
- Torso: a hunched navy snow beast. One curved `curveloft` torso runs from a narrow pelvis up and forward
  (~32 deg) to a barrel chest, with a trapezius hump that sinks the head between broad shoulders.
- Legs: short and thick, knees forward, broad dark feet with 3 dark toes + black claws.
- Arms: long, with a rounded deltoid, a bulging upper arm and a thick forearm tapering to the wrist. The heavy
  DARK fists hang just above the snow (bottom ~0.13), with black claws and 3 jagged ice knuckle plates.
- Ice plates (PLATE_ICE, smooth, flat-shaded, AURORA seam lines on the plate edges only):
  - a crust over each deltoid, its outer end tilted up 20 deg, with 2 broken shards on top and 3 irregular
    icicle shards on the rim;
  - a jagged slab on the outer upper arm, tilted up 20 deg;
  - 2 broken ice sheets frozen onto the hump. They carry the read for the game camera, which sits behind.
- Head:
  - a wide flat skull and a heavy dark BROW V (25 deg, inner ends low, overhanging);
  - deep-set PLATE_ICE slit eyes in black sockets with black slit pupils, tilted 20 deg (on navy, not on snow);
  - a snow muzzle and a broad flat black nose;
  - a jutting underbite jaw with 2 ivory fangs rising past the lip corners;
  - small low pointed ears and swept-back cheek tufts.
- Bones for VFX anchors: `Hand_L/R` (shard burst), `Chest` (snow puff), `Mouth` (breath), `Plate_L/R` (aurora dust).

## Value shares (flat palette IDs, %)
| | POLAR_NAVY | PLATE_ICE | SNOW | AURORA | BROW | BLACK | IVORY |
|---|---|---|---|---|---|---|---|
| side | 61.0 | 18.6 | 0.8 | 1.1 | 15.0 | 3.0 | 0.5 |
| tq | 60.6 | 17.2 | 1.2 | 0.5 | 16.4 | 3.3 | 0.8 |
| game | 56.5 | 31.0 | - | 1.3 | 9.4 | 1.6 | 0.1 |

## Deviations from the plan (and why)
- **No snow chest V.** I tried 4 versions on the hunched, forward-leaning chest:
  - a loft band (twice): it read as a white bib / "smile" crescent;
  - two bars: they read as collarbones / a mustache;
  - a mosaic of patches: it read as a grinning mouth of teeth.
  - All 4 failed in the front view, so SNOW is only the muzzle (0.8-1.2 %, plan 10 %).
  - The pale read comes from the ice plates instead (PLATE_ICE 17-19 %, plan 12 %).
- **POLAR_NAVY (120,128,200) -> (108,116,196).** The plan value rendered pale lavender next to LavaGolem / Kappa.
  Same hue (H 233), brightest channel 196.
- **BROW share 15 %** (plan 6 %). The fists and feet are BROW (dark extremities, like the Raiju's dark paws). That
  gives value contrast against the pale knuckle plates.
- **2 extra ice sheets on the hump** (not in the plan). Without them, the back (what the game camera sees) was a
  plain navy dome. They are flat sheets, not spikes, so they don't copy Thunder Rex's crystal ridge.
- **Elbow height**: 0.50H (plan 0.38H). The plan's numbers would give a 0.70 upper arm and a 0.25 forearm.
  I used ape proportions (upper arm ~ forearm) with the knuckles near the snow.
- **Tris 5.1k** (plan 8-11k): there's room if the reviewer wants more detail.

## Self-critique
- The silhouette (hunch + pale shoulder crust + dark head) reads at 64 px and is distinct from LavaGolem by colour
  and plates.
- The front of the torso is a plain navy barrel, and the limbs are still fairly blocky.
- If the reviewer wants more, I'd add pectoral/abdominal muscle masses in navy (form only, no colour) rather than
  another pale patch.

## Round 2 (review 1 fixes, 2026-10-27)
Tris 5,832. Height 1.63 units = 9.0 studs.

**MUST fixes**
- M1: the 3 ice knuckle plates sit on the TOP edge of the fist, with no seam on them. The fist front is smooth BROW.
  The fist is also rounder (rnd 0.50).
- M2: upper arm 0.17 -> 0.14, forearm 0.15 -> 0.10 (rnd 0.50).
- M3: thigh 0.19 -> 0.15; shin 0.14 -> 0.10 with a calf bulge; wedge feet (heel -> toe taper) with 3 rounded toe
  blocks + black claws.
- M4: 2 pectoral masses (exactly mirrored) + 1 abdominal mass, laid flush-ish on the chest loft, studded, navy
  form only.
- M5: the muzzle is POLAR_NAVY; fangs are 0.10.
- M6: AURORA seams are 0.040 wide.
  - A full seam runs round each shoulder crust's lower rim (front, outer, back).
  - The upper-arm slab has 3 seam edges; the hump sheets keep theirs.
  - AURORA is 3.4 % side, 4.4 % game.
- M7: the upper hump sheet moved to z 1.25 and tilts 20 deg, so it never shows over the skull.

**NICE fixes**
- Brow wings narrowed to 0.095.
- Skull 0.22 wide.
- NAVY_D (92,100,178) on the pelvis/belly tube, abdominal mass, shins and calves.
- Crust spikes trimmed to the 2 rim icicles.

**Value shares (%)**

| view | POLAR_NAVY | NAVY_D | PLATE_ICE | AURORA | BROW | BLACK | IVORY |
|---|---|---|---|---|---|---|---|
| side | 50.3 | 13.3 | 16.1 | 3.4 | 13.5 | 3.1 | 0.3 |
| game | 41.8 | 16.2 | 28.1 | 4.4 | 7.8 | 1.7 | 0.1 |

**Deliverables:** `_model_sheet.png` (incl. `model_lowfront`), `_close_sheet.png`, `_chest_sheet.png` (low-angle
chest views), `under.png` (belly-up), `flat_*`, and the `_icons_strip_64/128.png` strips (vs IceMammoth,
BrambleBadger, LavaGolem, Kappa, SeaTurtleWarrior, Treant).

## Round 3 (2026-10-27, after the round-2 verdict)
All round-2 MUST and NICE fixes are applied, plus the small mesh changes the clips needed. The list is in `CLIP_NOTES.md` under "Changes made for the clips". Fresh sheets: `renders/_model_sheet.png`, `renders/_close_sheet.png`, `renders/_icons_strip_64.png` / `_128.png`.

## Final 8.5 gate round (2026-10-28, `_review/GlacierYeti_final85.md`)
Pet file: `pets/GlacierYeti.py` 01:12. Backup of the pre-round file: `_scratch/GlacierYeti_r4_export.py`.
- **M1 fangs:** base y -0.818 -> -0.77, length 0.10 -> 0.07, IVORY -> (200, 196, 184). The tips sit at the mouth corners
  behind the snout face (`renders/_final_mouth.png`, `close_side.png`).
- **M2 mouth:** MOUTH -> (40, 8, 14) on the lip inlay and the interior; the interior block bevel 0.012 -> 0.030, z half
  0.042 -> 0.036. Open roar = a dark cavity; closed = hidden (`_final_mouth.png`).
- **M3 fist plates:** centre z 0.100 -> 0.092, slab thickness 0.032 -> 0.018.
- **M4 crust lip:** a PLATE_ICE_D (184, 206, 222) lip under each crust. Deviation from the review's single front block:
  that block would have covered the front aurora seam (the seam sits on the cap's lower 0.06). Instead the lip runs
  along the front, outer and back rim JUST BELOW the seam, in two stepped pieces per edge (heights 0.072 / 0.058), flared
  out and down so its face catches less light. Bands top to bottom: pale cap, green seam, mid-ice lip, navy
  (`renders/_crust_sheet.png`). Flat shares: PLATE_ICE_D 5.1 % side, 3.9 % game.
- **M5 limbs:** the asked rnd 0.50 -> 0.66 is a no-op: `blockkit._resolve` caps the edge rounding at 0.45 x the smallest
  half size, and rnd 0.50 is already at that cap. So the upper arm, forearm, thigh and shin are now studded superellipse
  lofts (`mtube`, n 2.2, 20 segments) with the same extents as the old blocks, domed ends buried in the neighbours, a
  bicep belly (upper arm) and a calf belly (shin). The separate bicep and calf blocks are gone.
- **T2 signature:** three short flat-topped PLATE_ICE frost blades in a row down the hump's rear slope (heights 0.07 /
  0.10 / 0.09, raked back and up, nostud). First placed on the ridge: they poked over the head as a 'horn' in the front
  view and one crossed the neck sleeve, so they moved down the slope. Tips stay at or below z 1.62: nothing shows over
  the head from the front; the side view shows a 3-blade crest.
- **T3 colour:** the lit game view still read lilac, so POLAR_NAVY (108, 116, 196) -> (96, 106, 186) and NAVY_D
  (92, 100, 178) -> (80, 90, 170) to keep the one-step-darker belly/shins. Brightest channels 186 / 170.
- **T4:** crust rim seam 0.040 -> 0.055.
- **T1 (rig):** a Neck bone (see CLIP_NOTES); the neck sleeve mesh moved from Chest to Neck.
- **Numbers:** tris 7,640 (was 6,036; the limb lofts). Size 1.62 x 1.18 x 1.63. Flat shares side / game: POLAR_NAVY
  52.7 / 38.3, NAVY_D 11.1 / 14.3, PLATE_ICE 11.7 / 29.0, PLATE_ICE_D 5.1 / 3.9, AURORA 3.3 / 4.8, BROW 12.7 / 7.8.
- **Renders (re-rendered 03:23-03:24 from the final 01:12:59 file; the first set at 01:12 was 40 s older than the last spine change, so it was redone; title bars carry the times; flat / icon / strips 01:13):** `renders/_model_sheet.png` (tq, front,
  side, back, game, under), `_close_sheet.png`, `_crust_sheet.png`, `_final_mouth.png`, `flat_side/tq/game.png`,
  `_icons_strip_64/128.png` (vs IceMammoth, Raiju, BrambleBadger, LavaGolem, Kappa, SeaTurtleWarrior, Treant),
  `GlacierYeti_icon.png`.
- **Not done:** a Studio game-camera capture. Builders may not touch Studio; `model_game.png` is the kit's game-camera
  view in Blender.

## Final gate round 2 (2026-10-28, `_review/GlacierYeti_final85_r2.md`)
Pet file 03:55; backup of round 1 `_scratch/GlacierYeti_f85r1.py`. Renders 03:56-03:58 (title bars carry the times),
export 03:59.
- **MN1 fangs:** IVORY (150, 146, 140) dim bone grey; base y -0.745, length 0.05. Dim grey points at the mouth corners,
  nothing pale ahead of the lower lip (`renders/_final_mouth.png`: `pclose_front_idle_00`, `pclose_side_idle_00`,
  `pclose_front_roar_30`, `pclose_side_roar_30`).
- **MN2 fist plates:** centre z 0.092 -> 0.080; `slab()` takes a colour and the fist plates are PLATE_ICE_D. No white
  strip on the fists in `model_front` / `model_tq` or the walk / skid tq frames (`_beats_f85r2_ws_tq.png`).
- **P1 crust:** the cap is two plates (inner + outer halves, 0.01 gap); the outer one sits 0.012 higher and tilts 4 deg
  outer-edge-up, so the crust reads as broken ice from the front and the back (`renders/_crust_sheet.png`, incl. a back
  view).
- **P2:** crust rim seam 0.055 -> 0.070 (AURORA 3.6 % side, 5.2 % game).
- Tris 7,728. `_icons_strip_64/128.png` and `GlacierYeti_icon.png` re-made from the final portrait.

## Final gate round 3 (2026-10-28 05:19, exported 05:22)
All values are measured with PIL on the 05:21-05:24 re-renders. lum = Rec.601 luma.

- MN1, fangs: IVORY is now (100,96,90), the lead's first try. It passed, so (72,70,68) was not needed.
  - `pclose_front_idle_00`: the fang (bone-coloured) pixels peak at lum 154 on the left (103 px) and 155 on the right (105 px). None reach 170.
  - The reviewer's literal left box (x 118-130, y 200-218) has 15 px at lum 170 or more. They are all the blue fur highlight (163,182,255) at its right edge (x 130), not fang.
  - `pclose_side_idle_00`, box x 160-192 / y 200-226: max lum 169, 0 px at 200 or more.
  - The fangs read as dull bone points, not holes (`_final_mouth`).
- MN2, fist plates:
  - The plate plane is now v = (0,0.6,1), normal (0,-1,0.6), facing forward. `slab()` builds the plane from u and v, so changing only the n argument would not have moved it.
  - The plates sit on the front-top bevel: c = Fv + (gx, -0.105, 0.080).
  - The new colour is KNUCKLE_ICE (88,104,128). The lead's (120,140,168) peaked at lum 209 in `model_front`; the next try, (104,122,150), peaked at about 230 in `model_tq`, where the near fist faces the key light.
  - Fist boxes now: `model_front` L 165 / R 185, `model_tq` L 185 (plate interior) / R 175.
  - The only pixels at lum 200 or more are 6 anti-aliased silhouette pixels on the tq near fist against the white ground (peak 210).
  - No white top shows in `beat_f85r3_ws_tq_walk_000` or `beat_f85r3_ws_tq_act_skid_007`.
- Tris 7,728, collision_free true, ground 0.002 on all clips. The gates and verify numbers are unchanged: neck 7.69, pitch-up 24.08, chest vs spine 4.61 or less.

## Per-clip round 4, model 9+ (2026-10-28 06:13)
- The shoulder-cap plates now use `CAP_ICE = (182, 200, 214)`, 12 % under PLATE_ICE. The lip, icicle, slabs, eyes and spines keep their colours.
- Measured on the lit 06:2x model renders, with the cap pixels masked from the flat ID renders resized to match: the share of cap pixels at lum 250 or more is 14 % (tq), 6 % (side) and 2 % (game). The cap median lum is 237 / 221 / 211, so it still reads as pale ice.
- Tris 7,728, collision_free true.
