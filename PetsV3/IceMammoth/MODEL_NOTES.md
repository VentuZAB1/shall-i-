# Ice Mammoth - model notes (model gate, 2026-10-27)

File: `pets/IceMammoth.py` (model + rig + check_pairs, no clips yet). `MAMMOTH_PROTO=1` env builds only
head + trunk + tusks (the trunk gate).
Tris: 11,216. Size (Blender units) 1.11 x 2.77 x 1.83. HEIGHT 9.0 studs = bbox top (head-dome wool). PITCH 0.0456
(same world stud size as the Raiju).

## Trunk build gate (plan MUST 3) - PASS
- Prototype: `_scratch/trunk_proto_sheet.png` (head + trunk + tusks only) and `_scratch/trunk_proto_64.png`
  (front / side / tq at 64 px).
- How the trunk is built: 4 bones (Trunk1-4). Each segment is 2-3 stacked "accordion" bands, and each band narrows
  toward its lower end, so the joints show ridges. It tapers 0.118 -> 0.060 half-width.
- It has a pale inner strip, a flared dark tip with 2 finger lips, and the tip curls forward.
- At 64 px it reads as a ridged trunk (taper, ridges, curled dark tip), not a hose. Same read in the full-body
  icon strip.

## What I built
- Body: woolly mammoth on a smooth `curveloft` barrel (split Chest | Spine). The back slopes from the shoulder hump
  (z 1.60) down to a low rump (1.20). The belly line rises 0.60 -> 0.69.
- Mane: dark wool over the back, plus 7 laid-back mane tufts on the hump ridge.
- Wool: 3 shingled rows of pointed wool-lock blocks down each flank. The top row is dark (the mane fringe), the
  lengths and flare vary, and the bottom row ends at ~0.35H as per the plan. A dark wool bib hangs at the chest.
- Head: a tall domed head (scaled 1.12 about the throat), with a dark wool cap + 4 tufts on the dome.
- Face: a heavy dark brow V (inner ends low); small deep-set slanted mint slits with black slit pupils; cheek
  bulges.
- Ears: small rounded flaps with a dark hair fringe.
- Tusks: 2 smooth curved ice tubes (socket -> down-out -> forward -> up-in tip, ~0.75 units long). Each has a
  teal sheath and a dark root ring, and 2 mint zigzag cracks on the outer third.
- Legs: thick columns, flat round pads with a dark sole rim and 4 dark toenails.
- Tail: thin, with a dark tuft.
- Bones for VFX anchors: `Trunk_Tip`, `Tusk_L/R` (tips), `Back`, `Breath`, `Foot_FL`.

## Value shares (flat palette IDs, %)
| | CHAR_TEAL | WOOL_D | BELLY_PALE | TUSK_ICE | MINT | DARK | BLACK |
|---|---|---|---|---|---|---|---|
| side | 56.7 | 31.9 | 1.2 | 4.3 | 0.2 | 3.7 | 2.0 |
| tq | 58.0 | 26.5 | 0.7 | 6.7 | 0.6 | 5.8 | 1.7 |
| game | 42.6 | 51.0 | 0.2 | 1.5 | 0.0 | 3.0 | 1.6 |

## Deviations from the plan (and why)
- **Body colours darkened**: CHAR_TEAL (150,184,188) -> (112,152,162) and WOOL_D (96,118,124) -> (64,84,96).
  - Next to ThunderBull / MoltenBoar / Badger in the 64 px strip, the plan values rendered almost white-cyan
    ("baby blue").
  - The new values keep the hue (H 191-201) and give the "dark teal-grey brute" read the plan asks for.
  - Brightest channel is 162: slightly under the 170 guide. That's intended, the same as the lineup's grey pets
    (Golem / Boar at 112).
- **WOOL_D share**: 32 % side (plan 18 %). The mane + dark top lock row carry the dark-back read.
- **BELLY_PALE share**: 1.2 % (plan 10 %). The wool skirt hides the belly; the pale strip shows from low angles
  and on the trunk's inner side.
- **MINT share**: 0.2-0.6 % (plan 4 %). The cracks + eyes are small at the full-body scale. I can widen the cracks
  if the reviewer wants more mint.
- **HEIGHT**: the head dome is the top (the plan says "top of the wool hump"). The shoulder hump is 0.87 of the
  height, the rump 0.66.
- **Tusks**: one smooth tube per tusk instead of 3 block segments (a curved tusk from blocks looked kinked). The 2
  mint cracks are on the outer third.
- **Head group scaled 1.12** about the throat in code (head, trunk, tusks, ears; joints use the same `HX()`), so
  the head reads mammoth-big.

## Self-critique
- The silhouette at 64 px is clear: dome head, 2 pale tusks, trunk, dark maned hump.
- The flank lock rows are a bit regular up close.
- The lower legs are plain columns.

## Round 2 (review 1 fixes, 2026-10-27)
Tris 13,676 (cap 15k; the plan's 8-11k is exceeded by the tusk tubes + 54 wool locks). Height 1.76 units = 9.0
studs, PITCH 0.0439.

**MUST fixes**
- M1 mint:
  - 3 cracks per tusk (t 0.55 / 0.68 / 0.79), bars 0.035 x 0.012.
  - A MINT ice cap over the last 40 % of each tusk tube. 16 % was not enough for the game view.
  - Eye slit half (0.074, 0.008, 0.018) in a bigger DARK socket.
  - MINT is 2.3 % side, 1.0 % game.
- M2: CHAR_TEAL (96,168,184), WOOL_D (80,110,124).
- M3: lock rows shortened. Row 1 is 0.19, row 2 0.20 (variation 0.08), row 3 0.11.
  - The belly band goes up to zhi -0.18 and now runs to the rump, so it also shows from behind.
  - BELLY_PALE is 3.3 % side, 0.9 % game.
- M4: rounded wool clumps (top 0.6-0.7, rnd 0.45) replace the head spikes and spine spikes, so the top is a dome.
- Also: the dorsal wool band is narrower (zlo 0.66 / 0.74). WOOL_D in game 44.5 %; CHAR_TEAL in game 47.9 %.

**NICE fixes**
- WOOL_D tusk socket rings.
- TUSK_ICE (226,240,246).
- Skull rnd 0.55.
- Trunk lowered: tip z 0.30 in build space (0.21 in world), below the knee line.
- 2 transverse teal seams across the wool dome.
- Brows 0.01 into the skull.
- Accordion step 0.94.

**Value shares (%)**

| view | CHAR_TEAL | WOOL_D | BELLY_PALE | TUSK_ICE | MINT | DARK |
|---|---|---|---|---|---|---|
| side | 60.4 | 25.4 | 3.3 | 2.9 | 2.3 | 3.7 |
| game | 47.9 | 44.5 | 0.9 | 0.9 | 1.0 | 3.2 |

**Deliverables:** `_model_sheet.png`, `_close_sheet.png`, `under.png`, `trunk_icon_64_x4.png`, `flat_*`, and the
`_icons_strip_64/128.png` strips (vs ThunderBull, MoltenBoar, Mossback, BrambleBadger, GlacierYeti).

## Round 3 (2026-10-27, after the round-2 verdict)
All round-2 MUST and NICE fixes are applied, plus the small mesh changes the clips needed. The list is in `CLIP_NOTES.md` under "Changes made for the clips". Fresh sheets: `renders/_model_sheet.png`, `renders/_close_sheet.png`, `renders/_icons_strip_64.png` / `_128.png`.

## Final 8.5 gate round (2026-10-28, `_review/IceMammoth_final85.md`)
Pet file: `pets/IceMammoth.py` 03:18. Pre-round backup: `_scratch/IceMammoth_r4_export.py`.
- **M1 colour:** CHAR_TEAL (96, 168, 184) -> (80, 150, 176), exactly as asked. Icon body median (my measure:
  `_scratch/iconv.py`, the 128 px icon, hue 170-215, s > 0.2): **V 0.77, H 200, S 0.53**. The V <= 0.70 target is not
  reachable while the brightest channel stays >= 170: the icon renderer lifts V about 1.12x, so 170 already gives ~0.76.
  I also tried (64, 132, 172) (darker in luminance, still >= 170): V 0.76, no visible gain (`_scratch/_colour_compare.png`),
  so it was reverted. The T4 fallback (72, 140, 164) breaks the 170 rule; that is the lead's / owner's call. The Studio
  game-camera capture (C1, open since review 2) is still not done: builders may not touch Studio.
- **M2 eyes:** the socket is BLACK (0.084, 0.012, 0.028); the slit is EYE_MINT (56, 196, 168), same size. Close-ups show a
  teal slit in a black frame, no pale window (`renders/_close_sheet.png`).
- **M3 legs:** a WOOL_D cuff on every leg: a studded superellipse loft from just above the knee down the top quarter of
  the shin, 0.022 proud (0.034 at the hem), with a jagged hem (alternate points 0.07 of the shin lower). A dark band on
  all four legs in the side, tq and back views (`_model_sheet.png`).
- **TO9 1 brow:** rot (-22, -s*28, 0), z 1.410: the brow overhangs the slit.
- **TO9 3 mouth:** a dark mouth interior (MOUTH_IN (40, 8, 14)) rides the jaw, hidden when closed; at the roar peak
  (jaw 18) a dark slit shows under the raised trunk root from the front (`renders/_roar_mouth.png`, camera on the Jaw).
- **Numbers:** tris 14,272 (was 13,716; cap 15k). Flat shares side / tq / game: CHAR_TEAL 57.8 / 58.9 / 47.0, WOOL_D
  27.8 / 25.1 / 45.3, BELLY_PALE 3.3 / 0.6 / 0.9, MINT 2.3 / 3.1 / 1.0, EYE_MINT 0.0 / 0.3 / 0.
- **Renders (03:19-03:21, from the 03:18 file; title bars carry the times):** `renders/_model_sheet.png` (tq, front, side,
  back, game 600 px, under), `_close_sheet.png`, `_flat_sheet.png`, `_roar_mouth.png`, `_icons_strip_64/128.png` (vs
  GlacierYeti, ThunderBull, Raiju, BrambleBadger, FrostfangLynx, MossbackTortoise), `IceMammoth_icon.png`.

## Final gate round 2 (2026-10-28, `_review/IceMammoth_final85_r2.md`)
Pet file 03:47; backup of round 1 `_scratch/IceMammoth_f85r1.py`. Renders 03:49-03:51 (title bars carry the times).
- **MM1 cuffs:** rings (0.16, 0.026, 0) -> (0.30, 0.030, 0) and (0.25, 0.034, 0.07) -> (0.50, 0.040, 0.07): the cuff covers
  the top half of each shin, same jagged hem. A dark band on all four legs in `model_side` / `model_tq`
  (`renders/_model_sheet.png`). Walk f10-30 in `_beats_f85r2_irw_side.png`: no clipping; step 1 collision-free. WOOL_D side
  share 27.8 -> 30.1 %.
- **MM2 eye:** slit (0.056, 0.008, 0.009) in the unchanged socket (0.084, 0.012, 0.028): black at both ends and above /
  below (`renders/_close_sheet.png`).
- **Mouth (for CM1):** the jaw hinge moved from mid-chin (y -1.08) to the back of the chin (0, -0.97, 0.99), so the open
  jaw drops the chin front ~0.07 instead of barely moving; the dark interior is longer and wider (0.092 x 0.085 x 0.030,
  inside the chin width), hidden when closed.
- Tris 14,272 (unchanged). Colour unchanged (80, 150, 176) per the lead. `renders/_icons_strip_64/128.png` and
  `IceMammoth_icon.png` re-made from the final portrait.

## Final gate round 3 (2026-10-28 04:38, exported 04:42)
- 9+ 1 pupil: the black pupil block is removed, so the EYE_MINT slit (0.056 x 0.009) reads as one teal line in the black socket (`_close_sheet`).
- 9+ 2 belly: a 2-stud-row WOOL_D strip on the pale band's top edge was tried first. It was hidden under the lowest lock row and cost 1,268 tris (15,540, over the 15k cap), so it was removed. It was replaced by a WOOL_D hem fringe on the band's lower edge: 5 short locks per side at `zang(-0.84)`, y -0.22..0.22 between the legs, 0.085-0.105 long. They hang just below the belly line in `model_side`. They cost +416 tris.
- 9+ 3 brows: new `BROW_D = (64, 84, 96)` on the brow slabs (WOOL_D stays on the mane).
- 9+ 4 flank: the middle lock row length variation goes from 0.08 to 0.12.
- CM1b mouth: MOUTH_IN interior moved +0.03 forward (centre y -1.07 -> -1.10). Still hidden when the jaw is closed (`pclose_*_idle_0` unchanged).
- Tris 14,688 (cap 15k), collision_free true, ground idle 0.018 / walk 0.015 / roar 0.018 / act -0.016.
