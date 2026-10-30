# Frostcrown Dragon - model gate notes (builder D, 2026-10-27)

File: `pets/FrostcrownDragon.py` (wing-quad: CelestialDragon / Ivonrath membrane wing, ThunderRex helpers).
Plan: `_review/FrostcrownDragon_plan.md` v2 (written as "Absolute Zero Dragon").



## ROUND 9 (review 8: model 8.4, clips all >= 8.6) - seam coverage + cheap 9+
- **Seam coverage:** every flank seam now runs on down to the lowest flank point the hide reaches. The bands use the
  tuck block as well as their torso block, so the line continues over the tuck.

  | band (y) | lower end (BU) | was |
  |---|---|---|
  | rib -0.24 | **0.60** | 0.70 |
  | rib -0.10 (moved from -0.06: there the rib's tapered bottom ends at 0.68) | **0.61** | 0.70 |
  | waist 0.08 | **0.64** | 0.75 |
  | waist 0.24 | **0.69** | 0.75 |
  | hips 0.33 | **0.70** | 0.77 |
  | hips 0.68 | 0.77 (no hide lower; the thigh is below) | 0.77 |

  - The tops still start under the saddle at 0.92-0.97.
  - `renders/model_side.png` (600 px; 6x zoom `_scratch/seam_zoom4.png`): each seam is an unbroken 3-4 px line from the
    saddle edge to the belly edge, about 90 % of the visible flank.
- **Ice-white (same mask as round 8):** portrait rule **9.8 %**, loose **10.7 %**, mean luma 107.
- **Gold, brief rule:** 28 / 29 / 30 (LANCZOS / BOX / NEAREST).
- Tris **10,460**.

## ROUND 8 (review 7: model 8.4, clips 8.6) - MUST 1 ice-white, MUST 2 seams, close sheet, diadem edge
- **MUST 1, ice-white, counted with your mask** (`_scratch/white_mask.py`):
  - image `renders/_icons_strip_128.png`, first cell, crop x 6-133 / y 6-133, no resize, no filter;
  - pet px = max(|R-52|, |G-62|, |B-74|) > 6; luma = 0.299 R + 0.587 G + 0.114 B; s = HSV saturation.
  - The mask reproduced your round-7 numbers exactly on the old strip (8.8 % / 9.6 %).

  | rule | r7 | **r8** | target |
  |---|---|---|---|
  | portrait (luma > 215, s < 0.15) | 8.8 % | **9.6 %** | >= 9.2 % |
  | loose (luma > 200, s < 0.20) | 9.6 % | **10.5 %** | >= 9.5 % |
  | mean luma | 105 | **106** | <= 110 |

  - ICE_W (236,246,252) -> **(244,250,255)**, also on the second fin facet. The palette alone gave 9.0 %, so the
    wing-arm frost edge (ICE_W) is 0.045 -> 0.065 deep: +0.5 pt. ICE_BELLY tests did nothing (the belly is not
    visible in the portrait).
  - The fin widths and ICE_THROAT are unchanged.
- **MUST 2, flank seams:** `trim_band()` bars are 0.018 thick and sit 0.016 off the hide.
  - There is now a ray hit at every mid-height, and each bar runs 0.005 past both ends, so neighbouring bars overlap
    by 0.01: one unbroken line.
  - Each line reaches further down the flank: rib 0.97 -> 0.70, waist 0.95 -> 0.75, hips 0.92 -> 0.77 (was 0.95-0.76 /
    0.93-0.80 / 0.90-0.77).
  - `renders/model_side.png` (600 px): each seam is a continuous 3-4 px wide line over about 80 % of the visible
    flank, with no gaps (6x zoom: `_scratch/seam_zoom3.png`).
- **Process:** `renders/_close_sheet.png` is re-rendered from the final build (tq / side / front / back, head at game
  distance).
- **9+, diadem edge:** a thin GOLD_HI lit edge runs along the diadem's front top, so the horns read apart from the band.
- **Gold, brief rule (64 px game icon):** 28 LANCZOS / 29 BOX / 30 NEAREST (gate 25). Strict 10 / 11 / 17, logged
  only.
- Tris **10,220** (gate 13k). Step 1 collision-free.

## ROUND 7 (review 6: model 8.2, clips 8.4) - model 1-3 + clips 4-5
Lead rulings: the gold is scored on the brief rule (strict is logged only); gold stays on the crown; the horns do not
grow.
- **1. Horns read as rounded, tapering horns.** `horn()` is no longer three boxes: it lofts one smooth tube
  (`B.tube`). The rings are octagonal and follow a Catmull-Rom curve through the same four horn points, so length and
  sweep are unchanged.
  - `rnd` caps at 0.45 in the kit, so rounding by `rnd` was not possible.
  - Root radius 0.84 w0, tapering hard as (1 - t)^0.85 to a 0.06 w0 point.
  - The side radius is 0.80 x the up radius, so the outer edge is pulled in.
  - GOLD body to t 0.80, then a GOLD_D point; two GOLD_D collars (t 0.30 / 0.58, 6 % proud); a thin GOLD_HI crest on
    the upper face.
  - `renders/_crown_sheet.png` (600 px, front / game / tq): two rounded horns curving back to sharp points, the five
    diadem points clear.
- **Gold, 64 px game-camera icon (alpha > 128):** brief rule (h .09-.17, s > .45, v > .55) **27 LANCZOS / 28 BOX / 29
  NEAREST** (gate 25). Tool rule 24 / 28 / 27. Strict, logged only: 10 / 11 / 16. Portrait 64: tool 57, brief 86 (the
  slimmer horns cost about 20 portrait px; gate 25).
- **2. Flank bands:** `trim_band()` bars are 0.030 wide (tail 0.027), 0.012 half-thick, sitting 0.010 off the hide
  (were 0.018 / 0.005 / 0.003). They read as bands in `renders/model_side.png` at 300 px.
- **3. Ice-white:** the second ICE_W fin facet is wider (lerp 0.30 -> 0.45).

  | count | r6 | r7 |
  |---|---|---|
  | stricter rule (lum > 215, s < 0.15, 128 px icon) | 9.0 % | **9.4 %** |
  | strip rule (lum > 200, s < 0.2) | 9.3 % | **9.6 %** |

  Luminance 105 / 109, dark 25 %.
- Tris **9,632** (gate 13k). Step 1 collision-free.

## ROUND 6 (review 5: model 8.0 -> REVISE) - M1-M4 + the model TO 9+ items
- **M1 horns (front):** the horn cross-section now runs on the diagonal (`HORN_SIDE = (0.707, 0, 0.707)`), so the faces
  are bevel facets, not a flat slab facing the camera. On the diagonal the projected front width is
  2 x 0.707 x (hw + hd), so I also slimmed the sections:
  - upper segments: hw 0.45 w, hd 0.55 w -> front width **1.41 w** (round 5: 2.0 w, a box on x) = **-29 %**;
  - root segment: 0.55 w / 0.58 w -> 1.60 w (round 5 root: 1.56 w; my first diagonal try had widened it to 2.26 w).
  - `renders/crown_front.png` (600 px): two slim, segmented horns rising to points; all five diadem points stay clear.
    Variant renders: `_scratch/hv/hv_cmp.png`, `hv_cmp2.png` (script `_scratch/horn_var.py`).
- **M2 game-camera gold** (`FrostcrownDragon_icon_game.png` -> 64 px, alpha > 128; script `_scratch/goldcount.py`):
  | rule | LANCZOS | BOX | NEAREST |
  |---|---|---|---|
  | tool: h .08-.16, s > .50, v > .45 | **27** | 29 | 30 |
  | brief: h .09-.17, s > .45, v > .55 | **28** | 30 | 32 |
  | strict: h .10-.15, s > .60, v > .70 | **18** | 16 | 17 |
  | rgb: R >= 200, G >= 140, B <= 110 | 16 | 17 | 16 |
  - Done: back points GOLD (5, taller: 0.10 / 0.14 / 0.18 / 0.14 / 0.10); back band (0.21, 0.04, 0.08), was
    (0.15, 0.022, 0.05); GOLD_HI lit upper edge on each horn segment; GOLD_D (214,150,30) -> (232,162,18) and
    GOLD_HI -> (255,204,24), more saturated, because lit gold renders pale.
  - **Strict 25 is not reached (18).** At 512 px most gold that fails the strict rule fails on saturation only
    (lit house gold renders at s 0.5-0.6). Tests (`_scratch/var_gold.py`, `gv1-5.json`):
    - ridge bands / tips to GOLD, a wider lit edge, a bigger diadem: +1 to +3 each;
    - a more saturated house GOLD (255,192,26) gave +4 (to 21), but GOLD is the shared house colour, so I kept it;
    - gold fin sockets / tail mount / wrist knuckles reach 36-41 on the loose rules, but the plan says "gold = the
      crown only (owner's rule)", so none of them are in.
    - Growing the horns is the only other route (lead ruling: no). **Needs a ruling:** keep 27 / 28 on the tool / brief
      rule, or allow one of the above.
- **M3 ice-white (both counts >= 9 %):** 128 px strip **9.3 %** (was 8.1), 128 px portrait icon (L > 215, s < 0.15)
  9.1 %, 64 px strip 8.4 %. Luminance 105 / 104 / 109 (128 / 64 / alpha), dark share 24 %.
  - Changes: ICE_THROAT (210,226,246) -> (224,236,252), now also on the lips, the jaw underside and the small tail
    crystal; a second ICE_W facet on each fin (toward the tip) and an ICE_THROAT bar along each fin base (not Fin_2:
    there it cut the Chest in the takeoff crouch); MEMBRANE -> (78,102,174) and DARK -> (46,52,84) to hold the
    luminance; foot claws 0.08 -> 0.09 long.
- **M4 crystal seams:** `trim_band()` lays 2 flush ICE_THROAT bars (0.018 wide, ray-hit on the flank surface) on each
  torso block (rib / waist / hips) and 2 on the tail (Tail1 / Tail2, 0.016). The side and tq views show banded flanks
  (`renders/model_side.png`, `_scratch/side_game_look.png`).
- **TO 9+ (model):** the GOLD_HI horn edge; an ICE_W frost edge along each wing arm; a second fin facet.
- Tris **9,288** (gate 13k). Step 1 collision-free. Re-rendered after the last change: `renders/_crown_sheet.png`,
  `_model_sheet.png`, `_icons_strip_64|128.png`, `_icons2_strip_64|128.png`, `idle_game.png`, `idle_side.png`.

## ROUND 5 (review 4: model APPROVED 8/10) - MUST 4 + NICE N3
- **MUST 4 ice-white:** a new ICE_THROAT (210,226,246) on the throat scutes and the frost-core facet, as asked. That
  alone moved my 128 px count only 6.7 -> 7.0 %, so I also put ICE_THROAT on the fins' inner facets (the fins carry the
  ice read). ICE_BELLY (196,214,240) stays on the belly strip, chest plate, lips, jaw underside and tail crystal.
  - My counts: ice-white 8.1 % on the 128 px strip (was 6.7; you read +1.1 over me in round 4, i.e. ~9.2 on your
    count), 7.0 % at 64 px.
  - Luminance 105 / 105 / 109 (128 / 64 / alpha), unchanged. Back-flank gap 26.4.
  - Gold: portrait 76 / 107, game 27 / 28 (strict / brief).
- **N3:** the horn root segment starts at 0.78 x the old width and widens to the next segment, at the same x 0.21 /
  0.24 positions. From the front the upper horn segments still read as wide gold blocks, because they are seen
  end-on as they sweep back.
- Tris 8,440, H 2.212. Re-rendered (600 px): `renders/crown_front.png`, `renders/_model_sheet.png`,
  `renders/_icons_strip_64|128.png`, `renders/_icons2_strip_64|128.png`.

## ROUND 4 (review 3, APPROVED WITH FIXES 8/10) - M1 + M2 applied, plus clip-round model changes
- Lead ruling: game-camera gold 27-28 passes (gate 25), the 40 target is waived, and the horns did not grow.
- **M1 front crown:** horn roots `P[0]` x s*0.17 -> s*0.21, `P[1]` x s*0.22 -> s*0.24 (the Horn_L/R joint follows at
  s*0.21). `renders/crown_front.png` shows all five diadem points clear of the horn roots.
- **M2 value:** DEEP_STEEL (38,64,130) -> (30,50,110) -> **(24,42,96)**. The review's step left the portrait at 113 on
  my counter, so I went one step further. To get past 110 I also darkened three non-hero colours: DARK (66,72,108) ->
  (54,60,94), MEMBRANE (100,130,196) -> (86,112,184), ICE_BELLY (210,226,246) -> (196,214,240). STEEL_BLUE (62,104,176)
  is kept. Variant runs are in `_scratch/val_var.py`.
- **Clip-round model changes (no visible change at icon size):** Fin_2 now sits on the neck root top (parent Neck,
  base (0, -0.56, 1.27), h 0.46), and the Neck saddle starts at 40 % of the bone, so the head press does not cut the
  neck. Fin capsules: Fin_1 / Fin_2 r 0.09 over 0.16. Wing capsules: S -> BB + 30 % (r 0.17) plus an arm root
  (r 0.13). Horn root capsule r 0.09. check_pairs adds Fin_2 | Neck2.

| measure | DEEP_STEEL step only (gap: review 3) | **round 4 final** | target |
|---|---|---|---|
| mean luminance, 128 px strip cell | 110 | **105** | <= 110 (aim a few points past) |
| mean luminance, 64 px strip cell | 109 | **105** | <= 110 |
| mean luminance, portrait icon (alpha, `_scratch/iconstats.py`) | 114 | **109** | <= 110 (builder count) |
| dark share (lum < 70), strip 128 / 64 | 24 / 26 % | **24 / 26 %** | |
| back-vs-flank gap, lit game view (DEEP 80.0 vs STEEL 106.3) | 10-15 (review) | **26.3** | >= 20 |
| gold px portrait 64 (strict / brief counter) | 95 / 122 | **76 / 114** | >= 20 |
| gold px GAME camera 64 (strict / brief counter) | 28 / 30 | **28 / 31** | 25 (ruling) |
| tris | 8,440 | **8,440** | |
- H 2.212 BU, bind span 4.836. Step 1 with the clips: collision_free true, ground_min_z >= -0.008 (`CLIP_NOTES.md`).
- Renders (600 px, re-rendered after the last change): `renders/crown_front.png` / `crown_game.png` / `crown_tq.png`
  (`_crown_sheet.png`), `renders/model_game.png` (`_model_sheet.png`), `renders/_icons_strip_64|128.png` (vs Thunder Rex,
  Cosmic Leviathan, Celestial Dragon, Black Dragon, Ivonrath), `renders/_icons2_strip_64|128.png`.

## ROUND 3 (review 2, REVISE 7/10) - M1-M3 applied (renders only)
- Tris 8,440. Step 1: collision_free true, ground_min_z -0.005; fold (32, -6, 0, 120) `fold_pairs` clean.
- M1 crown front: horn roots moved back AND out to the skull edge so they rise behind the band ends
  (P = (s*.17, .05, .10), (s*.22, .17, .24), (s*.27, .36, .30), (s*.31, .74, .40); the review's (s*.09, .04) roots still
  stood behind the outer points, gold on gold); horn base 0.080 -> 0.092; diadem band (0.20, 0.040, 0.050), sides
  0.028 / 0.050; points 0.07 / 0.10 / 0.15 / 0.10 / 0.07 set on the band top; NEW: a GOLD back band with three
  GOLD_D back points (a crown ring the game camera sees). `renders/crown_front.png`: all five points read between the
  horns.
- M2 belly rung loop removed (plain ICE_BELLY strip; the hex core is the only chest feature).
- M3 STEEL_BLUE (62,104,176). R2 (deviation): DEEP_STEEL on the whole legs (shoulder blocks, upper arms, thighs) - M3
  alone moved the portrait 118 -> 116. N1 (shell pad 0.030) cut the folded wings into the Spine: reverted.

| icon measure | Frostcrown r2 | **Frostcrown r3** | Thunder Rex | Cosmic Leviathan | target |
|---|---|---|---|---|---|
| mean lum, 128 strip (my method) | 118 | **114** | 107 | 116 | <= 110 on the reviewer's count (it read 114 when mine read 118) |
| mean lum, 64 strip | 117 | **113** | 105 | 113 | |
| dark (lum < 70), 128 strip | 22 % | **22 %** | 18 % | 12 % | >= 28 % |
| ice-white | 8.9 % | 8.4 % | 3.7 % | 4.2 % | |
| gold px 64 px portrait (strict / brief) | 76 / 108 | **85 / 124** | | | |
| gold px 64 px GAME camera | 23 / 25 | **27 / 28** | | | >= 40 |
- Game-camera gold: the game icon is fit to the whole 4.3 BU body seen from high behind, so the head is ~8 px wide
  and the crown faces away. The back band + points and the thicker horns took it 23 -> 27; 40 would need horns about
  twice the area, which brings back the V. Lead's call.
- Renders: `renders/_crown_sheet.png` (front / game / tq), `renders/_core_sheet.png`, `renders/_model_sheet.png`
  (600 px), `renders/_icons_strip_64|128.png` and `renders/_icons2_strip_64|128.png` (portrait + game icon) next to
  Thunder Rex and Cosmic Leviathan.

## ROUND 2 (review 1, REVISE 6/10) - MUST 1-5 + NICE N1-N4 applied; supersedes the sections below
- Tris 8,236 (gate 13k). H 2.233 BU; model top 2.228 = the gold horn (hero), stud pitch 0.0436. Bind span 4.84 BU
  (2.17 H), length 4.30 BU.
- Ground fold (32, -6, 0, 120): `fold_pairs` clean; step 1 (`headless_full ... - 1`, placeholder idle):
  **collision_free true**, ground_min_z -0.005.
- MUST 1 seven ICE_W fins, thickness 0.085, `FIN_PARENTS` (Neck2, Neck, Chest, Spine, Spine, Tail1, Tail2) + an
  assert, FX_FinSpark_1..7. Visible heights / chords 0.40 / 0.26, 0.50 / 0.31 (Fin_2 is 0.55 from a base 0.05 inside the
  neck), 0.60 / 0.38, 0.52 / 0.35, 0.42 / 0.29, 0.30 / 0.20, 0.24 / 0.17. Bases re-spaced so the swept blades never
  overlap (neck bases explicit points, body bases ray hits on the saddle shells, tail bases on the dorsal band). The
  body ridge spikes stood where fins 3-7 stand: removed (Tail3 / Tail4 keep theirs, the DARK stripe stays).
- MUST 2 frost core: ICE_W hex crystal 0.20 x 0.26 in a DARK setting with an ICE_BELLY inner facet + facet edges,
  ANCH Core at its face; keel plate + grille removed; belly rungs 4 -> 2 (t 0.40, 0.80). Round-2 fix: the setting was
  in front of the crystal (only the small facet showed), now recessed; the crystal stands 0.011 proud of it.
- MUST 3 crown: horn base 0.080, tip (s*0.31, 0.74, 0.40); diadem band (0.15, 0.030, 0.040), sides 0.022 / 0.040,
  back 0.04 tall; five points h 0.06 / 0.09 / 0.13 / 0.09 / 0.06.
- MUST 4 STEEL_BLUE (70,118,190), DEEP_STEEL (38,64,130), MEMBRANE (116,146,206) - then R1.
- MUST 5 tail tip spike 0.44 x 0.085, side blades 0.26 x 0.05, FX_IceDust at 0.42.
- NICE N1 skull (0.17, 0.175, 0.135); N2 upper arm 0.12 / 0.14; N3 / N4 kept.
- R1 (deviation, please judge) - value: MUST 4's colours took the icon lum only 140 -> 131 in my measure, so the
  3-band dark top band was widened: DEEP_STEEL on the wing arms + wrists, the shins + hind feet + paws ("dark socks",
  Rex's armour recipe), a 1.5x wider neck saddle; MEMBRANE one step further (116,146,206) -> **(100,130,196)**; DARK
  fingers +0.01 wide, outer trailing trim 0.042 -> 0.06 (inner trim stays 0.042: wider cut the Spine in the fold).
  Lower saddle shells were tried and reverted (no gain, fold collision).

| icon measure (128 px strip cell, pet px vs the cell bg, same method per cell) | Frostcrown | Thunder Rex | Cosmic Leviathan | target |
|---|---|---|---|---|
| mean luminance | **118** | 107 | 116 | <= 115 on the reviewer's scale (round 1: 130 vs 95 / 94) |
| dark (lum < 70) | **22 %** | 18 % | 12 % | >= 30 % on the reviewer's scale (round 1: 24 vs 45 / 37) |
| ice-white (lum > 200, s < 0.2) | **8.9 %** | 3.7 % | 4.2 % | >= 9 % |
| gold share | **4.0 %** | 1.0 % | 2.3 % | >= 2.5 % |
| gold px at 64 px, portrait (strict / brief counter) | **76 / 108** | | | >= 40 |
| gold px at 64 px, game camera | 23 / 25 | | | |
My measure does not reproduce the reviewer's absolute numbers (it reads Rex 107, not 95), so compare the gaps: round 1
the Frostcrown was +35 over both secrets on the reviewer's scale; now +11 over Rex and +2 over the Leviathan, with the
highest dark and ice-white shares of the three. Script: `_scratch/stripstats.py`.

| colour (flat IDs, fold pose) | side | tq | game |
|---|---|---|---|
| STEEL_BLUE | 19.8 | 19.3 | 13.4 |
| DEEP_STEEL | 11.5 | 20.4 | 16.6 |
| MEMBRANE | 29.6 | 18.9 | 28.5 |
| DARK | 23.1 | 16.6 | 19.5 |
| ICE_W / ICE_BELLY | 3.1 / 3.6 | 5.7 / 6.9 | 8.2 / 3.8 |
| GOLD / GOLD_D | 2.2 / 1.9 | 5.6 / 2.2 | 1.6 / 2.5 |
| MOUTH / BLACK | 2.1 / 3.2 | 1.8 / 2.5 | 2.3 / 3.6 |

- Renders (round 2): `renders/_model_sheet.png` (bind, 600 px), `renders/_close_sheet.png` (crown front / side / tq,
  frost core front / tq, fins side / back / game), `renders/_idle_sheet.png` (fold), `renders/_icons_strip_64.png` /
  `_128.png` (vs Thunder Rex, Cosmic Leviathan, Celestial Dragon, Black Dragon, Ivonrath), `renders/_icons2_strip_*`
  (portrait + game-camera icon), `renders/flat_*.png`.

## Round-1 notes

## Numbers
- Tris 8,140 (step-1 gate 13k, cap 15k). HEIGHT 11.5 studs = the gold horn tips (model top 2.20 BU, H 2.207 BU incl.
  the claws), stud pitch 0.043.
- Bind-pose span 4.82 BU = 2.2 H (plan 2.3 H), length 4.19 BU.

## What I built
- Torso: deep keeled ribcage (front raised 6 deg), DEEP_STEEL shoulder hump, sloped tuck to a narrow waist, hips (chest
  28 % wider than hips; the belly line rises chest -> hind legs). ICE_BELLY brisket plate, belly strip up the tuck and
  a keel plate on the chest front, all with DARK scute gaps.
- 3-band colour blocking: DEEP_STEEL saddle shells over ribcage / waist / hips, a DEEP_STEEL neck saddle, skull cap
  and tail top; a DARK dorsal stripe along the neck back, body top and tail top (the back line) under the fins;
  STEEL_BLUE sides; ICE_BELLY throat / belly / jaw underside.
- S-neck (Neck + Neck2) with an ICE_BELLY scute throat.
- Head (throat pivot): wedge skull, jaw muscles, snout with a DARK nose ridge + BLACK nostril slits, ICE_BELLY upper
  lip, ICE_W fangs + teeth, STEEL jaw with ICE_BELLY underside and a cold-violet MOUTH, long EYE_HOT slit eyes (20 deg,
  inner corner low) in BLACK sockets with BLACK slit pupils under heavy DARK brows, DARK brow spines + cheek blades.
- HERO gold horn crown: two long back-swept GOLD horns (3 segments, base 0.13 BU thick, GOLD_D ridge bands, GOLD_D
  points) on their own bones Horn_L / Horn_R; a slim GOLD diadem (front + side bands, GOLD_D back) with three points.
  Gold at 64 px: 60 px on the portrait icon (gate >= 25).
- FIVE flat ICE_W frost fins on Fin_1..Fin_5 (Neck2, Neck, Chest withers = tallest 0.48 BU, Spine, Spine): hard-edged
  crystal pentagon blades (thin across x, swept back), an ICE_BELLY inner facet on both faces, a DARK root socket.
  DARK laid-back ridge scales between them and down the tail.
- Wings: bat wing on 4 fingers (wing3 rules: inner panel on Wing_*, 3 outer panels on WingTip_*), STEEL_BLUE arm +
  wrist, ICE_W thumb claw, DARK fingers + scalloped DARK trailing-edge trim, MEMBRANE panels.
- Legs: muscular shoulder blocks + upper arms, elbow spurs, digitigrade hind legs with hock spurs, paws with 4 ICE_W
  claws on DARK bases. Tail (Tail1-4) ending in an ICE_W crystal spike cluster (main spike 0.32 BU + 2 side spikes + an
  ICE_BELLY spike) on Tail_Tip.
- Rig + VFX anchors in `rig()`: Mouth + FX_FrostBreath, Horn_L/R + FX_IceTrail_L/R, Fin_1..5 + FX_FinSpark_1..5,
  WingTip_L/R + FX_FrostTrail_L/R, Tail_Tip + FX_IceDust, Core + FX_ColdLight. check_pairs() / joints() written.
- Ground fold (placeholder, collision-free with fold_pairs / pose_try): (32, -6, 0, 120), the CelestialDragon raised
  fold. Re-searched with the clips.

## Deviations from the plan (+ why) - please judge D1 first
- D1 Colours: STEEL_BLUE (124,160,216) -> (88,136,210) (same hue 216, S 0.58, in game ~(53,82,126)); MEMBRANE
  (190,206,236) -> (150,178,228); new DEEP_STEEL (58,86,156) for the top band. With the plan values the dragon rendered
  as a pastel-blue toy and was the palest pet in the mythic / secret icon strip next to Thunder Rex and Cosmic Leviathan
  (test icons: `_scratch/var/icon_a.png` = plan palette, `icon_b/c.png` = richer variants). The mythic must outclass
  them; a richer steel-blue + a dark top band gives the 3-band blocking the rare-tier rule asks for. Still steel-blue
  (not indigo like Celestial Dragon, H 237), 6 deg from the plan hue. If the owner wants the plan value back it is a
  one-line change.
- D2 DARK share is ~14-19 % (plan 6 %): DARK wing fingers + trailing trim and the dorsal stripe frame the pale membranes
  and the white fins (white on dark reads at 64 px).
- D3 Fin spacing 0.35-0.45 BU (plan 0.30 H = 0.66 BU): five fins over the neck + back (plan "down the neck and back");
  0.66 spacing would put fins on the tail. Fin_3 sits on the withers in front of the wing root so three fins read in the
  side view of the folded pose (the folded wing covers the back fins from the side; the tq / back / game views show all
  five).
- D4 Wing root at y -0.18 (a little behind the shoulder) so the withers fin stands in front of the folded wing.
- D5 Claws ICE_W on DARK bases (the plan lists claws under both ICE_W and BLACK; ice claws on dark bases read as frost).
- D6 Placeholder `anim()` = an idle held at the ground fold, only for the portrait / 64 px icon / value shares.

## Value shares (flat ID renders of the ground fold pose)
| colour | plan | side | tq | game |
|---|---|---|---|---|
| STEEL_BLUE | 40 | 30.0 | 35.4 | 23.5 |
| ICE_BELLY | 14 | 2.9 | 5.5 | 2.0 |
| ICE_W | 10 | 1.8 | 3.6 | 3.9 |
| MEMBRANE | 8 | 32.8 | 23.5 | 30.9 |
| DEEP_STEEL | - | 5.4 | 7.7 | 13.6 |
| DARK | 6 | 18.9 | 14.1 | 17.7 |
| GOLD / GOLD_D | 4 / 1 | 1.7 / 1.4 | 4.6 / 1.6 | 1.3 / 1.7 |
The raised folded wings cover the flank and belly from the side (MEMBRANE high, ICE low); front 3/4 matches better.

## Renders
`renders/_model_sheet.png` (bind pose), `renders/_idle_sheet.png` (ground fold), `renders/_close_sheet.png` (head),
`renders/_icons_strip_64.png` / `_128.png` (vs Glacier siblings, Celestial Dragon, Black Dragon, Thunder Rex, Cosmic
Leviathan, Ivonrath), `renders/_icons2_strip_128.png` (portrait + game-camera icon vs the secrets).
