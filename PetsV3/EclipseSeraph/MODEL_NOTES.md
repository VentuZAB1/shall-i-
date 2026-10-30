# Eclipse Seraph - model gate notes (builder D, 2026-10-27)

File: `pets/EclipseSeraph.py` (Solar Lion anatomy x1.18 + three wing3 feather-wing pairs). Plan:
`_review/EclipseSeraph_plan.md` v2.



## ROUND 9 (review 8: model 8.5 PASS) - cheap 9+ (colours still ON HOLD, unchanged)
- **Muzzle pads +17 %:** (0.085, 0.095, 0.066) -> (0.099, 0.110, 0.077), same MUZZLE colour, a broader lion muzzle.
- **Lower pair root out:** C root x 0.26 -> 0.29 (BB 0.245 -> 0.275), for a wider front lower beat. The far lower tip
  reach holds (-0.171 screen x, 17 visible verts). Cut-through at rest 0; every clip collision-free.
- Icon / strips / portrait / model views re-rendered: saturation 0.406, share 64.8 % (Solar Lion 0.391 / 56.5 %).
  Rest halo clearance Head 0.055 / Mane 0.078. Tris 11,336.

## ROUND 8 (review 7: model 8.0, clips 8.5) - MUST far lower reach + cheap 9+ (colours ON HOLD, unchanged)
- **MUST, far lower wing reach:** the lower pair (C) is now longer and reaches further outward:
  - wrist 0.04 further out: W (0.47 -> 0.51), H2 (0.44 -> 0.47);
  - tip 12 % further: T (0.76, 1.12) -> (0.835, 1.228).
  - The root stays on the flank and the rest pose is unchanged, so nothing new is pushed forward.
  - Visibility test (`_scratch/vis_cands.py`, tq camera, the far wing's visible verts): leftmost screen x -0.155 ->
    **-0.171**. The face / mane edge is at -0.128.
  - The visible reach outside the mane grows about 60 % (0.027 -> 0.043 screen units). On your 0.09-0.11 H reading,
    that is roughly 0.15-0.17 H.
  - Both sides grow; the near lower wing still balances the near middle wing on the card (`EclipseSeraph_icon.png`).
  - Cut-through at rest 0 hits; every clip collision-free.
- **9+, lion read:** the cheek ruff tufts are 0.03 longer (0.20 / 0.19), a heavier dark frame round the face.
  OBSID only, no colour change.
- **Colours:** untouched. MOON_IVORY / BODY_MID / WING_LILAC stay as in round 7 until the owner rules.
- Counts after the change (my 64 px strip, cell 0): saturation 0.406, share 64.9 %. Icon: near-white 11.9 %, gold 75,
  red 61; game gold 34, red 18. Halo clearance: rest Head 0.055 / Mane 0.078, roar f30 Mane 0.055. Tris 11,336.

## ROUND 7 (review 6: model 8.0, clips 8.5) - MUST 1 + TO 9+ + evidence
- **MUST 1, the sixth wing on the Index card:** the lower pair at rest is now **C (-12, fwd +70, twist 0, tip -45)**:
  it reaches down and FORWARD with the hands spread, "with two he covered his feet" (was -2 / +40 / 0 / -18).
  - `EclipseSeraph_icon.png` (512) shows six shapes:
    - far side: the upper fan, the middle tips left of the halo, and the lower tips left of the face;
    - near side: the upper blade, the level middle wing, and the lower wing reaching past the forelegs.
  - The front view (`renders/idle_front.png`, `_pose_front_*` f0) reads as a six-point star, three tiers per side.
  - Acceptance gap: the far lower tips clear the face edge by about **0.09 H**, not 0.15 H.
    - The visibility search (`_scratch/vis_cands.py`, a camera ray test on the far wing's verts, 40+ poses) found the
      far lower wing fully hidden at every pose with fwd <= 52, including "tip out -8 / up +4" (0 verts visible) and
      up 30 / 46.
    - Only a forward reach shows it. fwd 70-80 with the hand spread 45-60 is the maximum (12-20 verts, screen x
      -0.155 against the face / mane edge at -0.128); the wing length caps the reach.
  - fwd stays far above -4, so the walk is clear. All seven clips are at 0 hits (step 1).
- **TO 9+, face:** the muzzle pads are a warm lilac grey MUZZLE (186,170,190), was white WING_IN. Only the chin stays
  pale, so the OBSID brow and cheek ruff carry the face.
- **TO 9+, saturation (my 7-cell 64 px strip, cell 0):**

  | measure | r6 | **r7** |
  |---|---|---|
  | mean saturation | 0.395 | **0.410** |
  | saturated share | 62.5 % | **65.9 %** |

  - Solar Lion 0.391 / 56.5 %, Frostcrown 0.388 / 59.0 % on the same count.
  - New colours:

    | colour | was | now |
    |---|---|---|
    | MOON_IVORY | (222,176,248) | (210,150,246) |
    | BODY_MID | (188,96,230) | (184,86,228) |
    | WING_LILAC | (204,120,248) | (202,112,248) |
    | IVORY_D | (190,184,206) | (178,164,204) |

  - The wing stays ~22 lum over the body (r6: 21). +0.021 was possible with wing (200,104,248), but the split falls to
    17, so I stopped at +0.015.
  - Raw: saturation 0.45, near-white 18.8 %, dark 22.7 %. Gold 77 / 104 / 124 (icon / raw / brief), game 34, red
    60 / 18.
- **7-cell strip restored:** `renders/_icons_strip_64|128.png` = Seraph, Solar Lion, Frostcrown, Griffin, Celestial
  Dragon, Cvetibara, Cosmic Leviathan.
- Halo clearance: rest Head 0.055 / Mane 0.078; roar f30 Mane 0.055. Tris 11,336.

## ROUND 6 (review 5: model 8 / clips 8.5 / overall 8 -> REVISE) - MUST 1-3 + TO 9+
Counts below are mine (64 px). In round 5 you read about +0.018 saturation and +11 points of saturated share over my
strip count.

- **MUST 1 six wings at rest (Index card + front):** new `DISPLAY_POSE` (the ground rest pose of every clip):
  A (40, +4, 22, -8), B (20, +16, 20, -14), C (-2, +40, 0, -18). Was A (44, -4, 22, 0), B (4, -8, 20, 0),
  C (10, -4, 0, -6).
  - Raising C to 16 as suggested put it on top of B (both flat behind the flank, `_scratch/cand7.png`). So the tiers are
    now separated by angle and sweep: B is a diagonal swept forward, and C lies level and sweeps forward along the flank
    ("two cover the feet").
  - `EclipseSeraph_icon.png` (512): on the near side the upper, middle and lower wings are three separate shapes. On
    the far side the upper fan shows above the halo and the middle fan now shows past the halo's left edge. Only the
    far lower wing stays hidden under the head. That is 5 of 6 on the card (was 3).
  - Front view (`renders/idle_front.png`, `model_front.png`): three tiers per side.
  - Cut-through and walk: 0 hits at rest (`_scratch/pose_cands.py`) and in every clip at step 1. The cascade needed one
    path change: B sweeps back as it rises, so it never meets the chest.
- **MUST 2 punch (my 7-cell 64 px strip, cell 0 vs Solar Lion cell 1):**

  | measure | Seraph r5 | **Seraph r6** | Solar Lion |
  |---|---|---|---|
  | mean saturation | 0.352 | **0.395** | 0.391 |
  | saturated share (s > 0.35) | 44.1 % | **62.5 %** | 56.5 % |

  - Other counts (raw portrait at 64 px): saturation 0.43, near-white 21.6 % (was 34.4), dark (< 90) 22.0 % (was 23.1).
    On the 64 px icon: saturation 0.42, near-white 13.7 %.
  - Lever A (corona 0.10 -> 0.12) alone gave +0.000 / +0.1 points. The gain came from the colours:

    | colour | was | now |
    |---|---|---|
    | WING_LILAC | (214,150,246) | (204,120,248), S 0.52, hue 281 |
    | BODY_MID | (196,112,234) | (188,96,230), S 0.58, hue 281 |
    | MOON_IVORY | (230,196,244) | (222,176,248) |
    | OBSID | (26,26,66) | (30,22,78) |

    The wings stay ~21 lum over the body, so the wing / body split holds. The hue is 281 (Shade Panther accent 271).
    Variant runs: `_scratch/var7.py` with `r6v1-6.json`.
- **TO 9+ (model):**
  - **Lion ruff:** two OBSID cheek tufts per side frame the face (`Head` bone). They give +0.8 points of raw dark and
    clear every clip.
  - **Hero gold:** the halo's gold rim is 0.085 -> 0.10 wide. Portrait gold is 77 icon / 104 raw / 124 brief counter
    (was 69 / 89 / 108-ish). Game-camera gold is 34 (was 26).
  - The corona band is 0.12. Red is 47 on the portrait icon and 15 on the game camera (gate 12).
- **Halo clearance:** at rest, Head 0.055 / Mane 0.078 / Wing_A 0.078. At the roar hold (f30, tilt 18), Mane 0.055.
- Tris **11,336** (gate 15k). Step 1 collision-free.
- Re-rendered after the last change: `EclipseSeraph_icon.png`, `_icons_strip_64|128.png`, `_icons2_strip_64|128.png`,
  `renders/_model_sheet.png`, `renders/idle_game|front|tq.png`.

## ROUND 5 (review 4: model 8/10, clips 6/10 - the one bounded six-wing round)
- **MUST 1 value split:** WING_LILAC (204,120,242) -> **(214,150,246)**, as given. Feather luminance ~180 against the
  body's 151 (gap ~29).
  - Saturation (mine): icon 0.37 (Leviathan 0.37 on the same counter), raw 0.38, strip cell 0.352. Your round-4 count
    was 0.39 when mine was icon 0.39, so it should land at ~0.37 (>= 0.36, margin ~0.01).
  - Side effect: the lighter feathers raise near-white (lum > 200) to 22.9 % icon and 34.4 % raw (was 16.8 / 23.6).
    That is above the round-3 <= 25 on the raw count. I kept your colour; tell me if near-white still counts.
- **MUST 2 game red:**
  - The brush sits 0.03 lower and 0.03 further back. The block is (0.13, 0.14, 0.11); the tufts are 0.085 wide, with
    the up-back tuft at 0.26 plus two side up-back tufts (0.20).
  - Moving the brush alone left my count at 14, which you read as 9, so it needed more. Game red is now **17** on my
    count (portrait 52), so about 12 on yours. Variant runs are in `_scratch/var7.py`.
- **MUST 3 (model part):** Wing_B root moved back 0.10, up 0.04 and out 0.02, and re-parented to the Spine
  (`make_wing("B", ...)`, `rig()`). The clip side is in `CLIP_NOTES.md`.
- Tris 11,288, H 2.234 (halo top 2.231). Halo clearance Head 0.055, Mane 0.080.
- Game gold 26 strict / 26 brief (keep > 20 on yours: NICE 4). Dark (lum < 90) raw 23.1 %.
- Flat shares, game view: WING_LILAC 31.5 %, BODY_MID 29.0 %, OBSID 19.3 %, GOLD 4.6 %, BLOOD 2.8 %.
- Renders (LAST, 600 px): `renders/_model_sheet.png`, `renders/_icons_strip_64|128.png`,
  `renders/_icons2_strip_64|128.png`, `renders/_idle_sheet.png`.

## ROUND 4 (review 3, REVISE 7.5/10) - MUST 1-4 + NICE 1-2 applied, plus clip-round model changes
- **MUST 1 chroma:** BODY_MID (196,112,234) and WING_LILAC (206,130,240) as the review gave them, then the corona
  band 0.07 -> 0.10 (lever C). After those, the reviewer-like strip-cell counter still read 0.340 (Leviathan 0.351), so
  I pushed one step further on three colours, keeping hue: WING_LILAC -> **(204,120,242)**, OBSID (34,34,56) ->
  **(26,26,66)** (hue 240, richer and darker), MOON_IVORY (232,208,240) -> **(230,196,244)**. Variant runs are in
  `_scratch/var4.py`.
- **MUST 2 dark mass:** OBSID darker (above). **MUST 3 game gold:** rim band `HALO_R - 0.085`.
- **MUST 4 / NICE 2 clearance:** halo tilt 40, centre HC + (0, 0.22, 0.614), top 2.231. HALO_LIP 0.060 -> 0.066: game
  gold had fallen to 24 after the brush change, and the game camera sees the rim's outer edge, so a wider radial band
  did not help (0.095 / 0.100 tested: no change). Head clearance 0.055, Mane 0.080.
- **NICE 1 tail brush:** tufts +0.03 longer, plus a sixth tuft up and back so it reads as a brush from behind. The
  block goes to (0.11, 0.12, 0.10), not the review's (0.10, 0.11, 0.095): at the review size the game camera dropped
  to 12 red px (the block is most of the red from that camera). With 0.11 it is 14. Variants are in `_scratch/var5.py`.
- **Clip fix for the brush:** the takeoff crouch lifts the tail (+8), so the longer tufts clear the floor.
- **Clip-round model changes:** (a) the outer mane ring's low + side tufts (d.z < 0.6) are weighted to Neck instead of
  Mane. They sat in the chest cape and the foreleg tops at rest, and any head turn cut them through. The top arc stays
  on Mane, which flares in the roar. (b) DISPLAY_POSE lower pair C fwd -10 -> -4: the root rows cleared the thigh on
  the walk. The look is the same at icon size.

All counts are mine at 64 px. The margin is over the review-3 target. The reviewer's counter ran 1-5 points worse
than mine in round 3 (white +5 vs my icon, saturation -0.01, game gold -4), so I aimed past each target.
| item | round 3 (mine) | **round 4 (mine)** | target | margin |
|---|---|---|---|---|
| mean saturation: raw / icon / strip cell (with outline) | 0.33 / 0.33 / - | **0.40 / 0.39 / 0.370** | >= 0.36 | +0.04 / +0.03 / +0.010 (Leviathan cell 0.351, icon 0.37) |
| saturated share (s > 0.35): raw / strip cell | - | **76 % / 57 %** | >= 40 % | +36 / +17 |
| near-white (lum > 200): raw / icon / strip cell | 32.6 / 22.1 / 23.1 % | **23.6 / 16.8 / 14.7 %** | <= 25 % | +1.4 / +8.2 / +10.3 |
| dark (lum < 90), raw | 16.5 % | **22.7 %** | >= 22 % | +0.7 (in round 3 the reviewer's dark read HIGHER than mine: 20 vs 16.5) |
| gold px GAME camera (strict / brief counter) | 22 / 22 | **27 / 25** | >= 20 | +7 / +5 |
| gold px portrait (strict / brief) | 69 / 90 | **70 / 108** | >= 20 | +50 / +88 |
| red px portrait / GAME camera | 29 / 15 | **49 / 14** | >= 10 | +39 / +4 |
| halo clearance Head / Mane (BU) | 0.050 / 0.082 | **0.055 / 0.080** | >= 0.050 | +0.005 |
| tris | 11,252 | **11,264** | <= 15k | |
- H 2.234 BU (top = halo top 2.231), bind span 3.83. Step 1 with the clips: collision_free true, ground_min_z >= -0.010.
- Flat shares, game view: WING_LILAC 30.6 %, BODY_MID 30.2 %, OBSID 19.6 %, MOON_IVORY 4.9 %, GOLD 4.6 %, BLOOD 2.2 %.
- Renders (rendered LAST, 600 px, final model + display pose): `renders/_model_sheet.png` (incl. `model_under.png`),
  `renders/_icons_strip_64|128.png` (7 cells: Seraph, Solar Lion, Griffin, Celestial Dragon, Cvetibara, Cosmic
  Leviathan, Frostcrown), `renders/_icons2_strip_64|128.png` (portrait, game icon, Leviathan, Frostcrown),
  `renders/_idle_sheet.png`.

## ROUND 3 (review 2, REVISE 7/10) - M1-M4 + NICE 2 applied (renders only)
- Tris 11,252. H 2.173, top = halo top 2.170. Step 1: collision_free true, ground_min_z -0.003. Halo clearance
  (display pose): Head 0.050 BU, Mane 0.082 BU.
- M1 upper primaries WING_LILAC; WING_IN only on the 3 upper hand coverts (the one pale highlight).
- M2 tail brush BLOOD (block + 5 tufts), and 1.2x bigger (block (0.12, 0.13, 0.11), tufts +0.03 long, 0.07 wide):
  at the review size the game camera saw 9 red px.
- M3 outer mane ring (0.31, 0.36, 0.10, 26 tufts).
- M4 BODY_MID (190,120,226). Margin for the saturation target: WING_LILAC (190,150,226) -> (200,146,232) (hue 278, the
  body family; not the 271 violet). No violet anywhere; accents BLOOD + GOLD only.
- NICE 2 rim lip 0.045 -> 0.050 (HALO_C z 0.578 keeps the top), after M1-M4 the game gold had dropped to 21 / 19.

| 64 px | round 2 | **round 3** | target |
|---|---|---|---|
| near-white, portrait icon (alpha) | 25.6 % | **22.1 %** | <= 25 |
| near-white, strip cell without outline | 26.6 % | **23.1 %** | |
| near-white, raw render (no outline) | 36.1 % | 32.6 % | |
| mean saturation, portrait (icon / raw) | 0.28 / 0.28 | **0.33 / 0.33** | >= 0.33 (Leviathan 0.37 on the same count) |
| dark (lum < 90), raw | 16.9 % | 16.5 % | >= 22 on the reviewer's count |
| gold px portrait (strict / brief counter) | 59 / 87 | **69 / 90** | |
| gold px GAME camera (strict / brief counter) | 22 / 20 | **22 / 22** | >= 20 |
| red px portrait | 16 | **29** | >= 10 |
| red px GAME camera (icon / raw) | 0 | **15 / 14** | >= 10 |
- Counter used: "strict" = `_tools/game_icon.py` gold_px_*_64; "brief" = its gold_px_brief_counter.
- Renders: `renders/_icons_strip_64|128.png` (vs Solar Lion, Griffin, Celestial Dragon, Cvetibara, Cosmic Leviathan,
  Frostcrown), `renders/_icons2_strip_64|128.png` (portrait, game icon, Leviathan, Frostcrown), `renders/_idle_sheet.png`,
  `renders/_model_sheet.png` (600 px, incl. under view).

## ROUND 2 (review 1, REVISE 5/10; six wings kept) - MUST 1-7 + NICE applied; supersedes the sections below
- Tris 11,228. H 2.173 BU; model top 2.170 = halo top 2.170 (HEIGHT 11.5 studs = halo rim top). Bind span 3.83 BU.
- Step 1 (`headless_full ... - 1`, placeholder display idle): collision_free true, ground_min_z -0.003.
- MUST 1 body split: BODY_MID on chest / tuck / waist / hips / legs / paws / tail, MOON_IVORY kept on face, cranium,
  muzzle, neck, shoulders, wing arms; B + C flight feathers lilac. Pushed one step (R1 below).
- MUST 2 mane: tuft lean (0, 0.9 + 0.12 * ring, 0), counts 22 / 22 / 24, widths 0.07 / 0.085 / 0.10, bib 5 tufts,
  cape extended to the chest. No gold on the mane.
- MUST 3: skull 0.20, muzzle 0.12, nose 0.066, forelegs 0.13 / 0.165, paws 0.12 x 0.13, tail end (0, 1.66, 0.26),
  end tuft 0.10 / 0.11 / 0.095.
- MUST 4 halo: HALO_TILT 40; HALO_C z 0.582 (0.60 put the thicker rim above 11.5 studs; 0.582 keeps the top);
  `halo_top` formula updated for the rim lip. Clearance (display pose): halo to Head 0.056 BU, to Mane 0.105 BU (>= 0.05).
- MUST 5: gold rim `rim_i = R - 0.075`, corona 0.07 wide, eyes sc 1.6. The gold rim now also stands 0.045 proud of each
  disc face (HALO_LIP; was 0.022) - the game camera sees the halo edge-on (below), so the rim edge band is its gold.
- MUST 6: C root z 1.05, C geometry raised (W z 1.04, hinge z 1.07, tip z 1.05); display C (10, -10, 0, -6):
  wing-vs-wing / wing-vs-body cut-throughs **0** (`_scratch/pose_cands.py`, c10); C up 18 (NICE 1) cut into B (83-99
  pairs), so up stays 10 with the raised C.
- MUST 7: tipf 0.12 (secondaries) / 0.15 (primaries).
- R1 (deviation, please judge): MUST 1's colours alone moved the lit portrait little (Blender's portrait key light puts
  lit #CEA0E8 over lum 200), so BODY_MID (206,160,232) -> **(184,128,214)** (same hue 278, S 0.40, V 0.84) and
  WING_LILAC (214,186,236) -> **(190,150,226)**; the upper pair's coverts, hand coverts and secondaries are WING_LILAC
  (its WING_IN primaries stay the one pale highlight); B + C coverts BODY_MID; OBSID (60,60,84) -> **(46,46,70)** so
  the mane counts as dark mass.
- R2 HALO_LIP 0.045 (see MUST 5).

| 64 px portrait (pet px) | round 1 model | round 2 | target |
|---|---|---|---|
| near-white (lum > 200), raw render no outline | 48.4 % | **36.1 %** | <= 25 (reviewer 42 -> scaled ~31) |
| near-white, strip cell without the outline | 34.7 % | 26.6 % | |
| mean saturation (raw) | 0.19 | **0.28** | >= 0.28 |
| dark (lum < 90), raw | 9.3 % | **16.9 %** | >= 22 (reviewer 15 -> scaled ~27) |
| gold px, portrait (strict / brief counter) | 41 | **59 / 87** | >= 20 |
| red px, portrait | 1-3 | **16** | >= 10 |
| gold px, GAME camera | 9 | **22 / 20** | >= 20 |
| red px, GAME camera | 0 | **0** | >= 10 - see below |
(round-1 model re-rendered with the same tools: `_scratch/pre_r1_icon.png`; scripts `_scratch/raw_stats.py`,
`_scratch/calib.py`, `_scratch/seraph_stats.py`.)

- **Open: red from the game camera.** The game camera is high behind (~38 deg); a disc tilted 40 deg forward-up is
  exactly edge-on to it (cos 0.006), so neither face (corona) shows. Measured red at tilt 40 / 30 / 20: 0 / 0 / 0 (thin
  ellipse, partly behind the raised upper wings). Red >= 10 from behind needs the halo tilted back toward the camera,
  which makes it edge-on in the portrait. Kept tilt 40 (MUST 4); lead's call.
- Option not applied: upper primaries lilac too -> near-white raw 31.1 % / strip 22.1 %, sat 0.32
  (`_scratch/var_apri_icon.png`); MUST 1 keeps them WING_IN.
- NICE 2: display span 3.06 BU = 1.41 H, set by the middle pair B (A at up 26 / 34 / 44 gives the same span); 2.0 H
  would need the upper pair near level, which drops the V. A kept at 44. NICE 3 not needed (game gold 22).
  NICE 4: `renders/_icons2_strip_64.png` / `_128.png` = [portrait, game-camera icon, Cosmic Leviathan, Frostcrown].

| colour (flat IDs, display pose) | side | tq | game |
|---|---|---|---|
| MOON_IVORY | 7.0 | 8.0 | 5.4 |
| BODY_MID | 28.5 | 20.6 | 29.0 |
| WING_LILAC | 14.8 | 9.2 | 25.5 |
| WING_IN | 14.2 | 12.8 | 7.9 |
| IVORY_D | 1.1 | 2.1 | 1.3 |
| OBSID | 26.2 | 30.2 | 22.1 |
| GOLD / GOLD_D | 3.3 / 0.3 | 8.8 / 0.5 | 3.7 / 0.4 |
| BLOOD | 0.0 | 3.2 | 0.1 |
| BLACK | 4.2 | 4.1 | 4.2 |

- Renders (round 2): `renders/_model_sheet.png` (bind, 600 px, incl. under view), `renders/_close_sheet.png` (face
  front / side / tq, halo front / side / game, rim + corona close-ups), `renders/_idle_sheet.png` (display pose),
  `renders/_icons_strip_64.png` / `_128.png`, `renders/_icons2_strip_64.png` / `_128.png`, `renders/flat_*.png`.

## Round-1 notes

## SIX-WING STEP-1 GATE: PASS -> six wings kept (no four-wing fallback)
- Tris 10,484 (target 13k, ceiling 15k). Feathers of the middle / lower pairs are unbevelled 12-tri blades; only the
  upper main pair is bevelled.
- 64 px: not a blob. The portrait icon reads as halo + dark mane + pale lion + raised upper V + the middle pair; the
  three tiers (raised upper V, level middle pair, tucked lower pair) read clearly from the back / game camera
  (`renders/_idle_sheet.png`). From the front 3/4 portrait the lower pair is mostly hidden by the body (plan NICE: "two
  big pairs plus a tuck"). Reviewer: please judge the 64 px strip; if it fails, the fallback needs the owner.

## Numbers
- HEIGHT 11.5 studs = top of the halo rim (model top 2.168 BU = halo top in the bind pose), stud pitch 0.0423.
- Bind pose span 3.83 BU (1.8 H); the display pose raises the upper pair above the halo (idle top 2.94 BU).

## What I built
- Lion body (Solar Lion x1.18): deep ribcage, shoulders, sloped tuck, waist, hips (chest 19 % wider than hips),
  IVORY_D underside strip following the rising belly line; heavy forelegs, digitigrade hind legs, big paws with an
  IVORY_D pad line and 4 BLACK claws; a long 4-bone tail with an OBSID tuft (Tail_Tip).
- Head: broad MOON_IVORY cranium, nose bridge with an IVORY_D stripe, WING_IN muzzle pads + chin, a BLACK triangular
  nose, IVORY fangs, MOUTH; BLOOD slit eyes (20 deg, inner end low) in BLACK sockets with BLACK slit pupils under heavy
  OBSID brows (no glint); small OBSID ears.
- Mane: THREE OBSID rings of radiating tufts framing the face (inner 0.13 BU, middle 0.25, outer 0.33 on the Mane
  bone), a mane bulk + crest over the neck, a shoulder cape with swept tufts, a chest bib.
- HERO halo: a SOLID OBSID disc (filled, 0.92 BU across, 0.08 thick) tilted 20 deg forward-up, floating above the head
  on the Halo bone, a GOLD rim band on the outer edge and a BLOOD corona ring just inside the rim on BOTH faces (smooth
  lofted tubes, no studs). Gold at 64 px: 41 px on the portrait icon (gate >= 20).
- SIX feathered wings (bones Wing_A/B/C_L/R + WingTip_A/B/C_L/R): A upper main pair = 3 rows (MOON_IVORY studded arm +
  coverts, IVORY_D secondaries, WING_IN primaries, MOON_IVORY hand coverts); B middle pair and C lower pair = 2 rows
  (WING_IN coverts + flight feathers); every flight feather tipped OBSID.
- Display pose (the ground pose; placeholder idle): A raised V (44 up, 22 twist), B level and spread back (4 up, 20
  twist), C tucked low at the flank. Wing-vs-wing / body cut-throughs in this pose: 0 except C vs the hind thigh
  (4-5 tri pairs), to be cleared with the clips.
- Rig + VFX anchors in `rig()`: Halo + FX_CoronaSparkle, Mouth + FX_CoronaRing, Mane_Top + FX_HaloDust,
  FX_FeatherSparkle_A/B/C_L/R on the WingTip bones, Tail_Tip + FX_StarSparkle. check_pairs() / joints() written.

## Deviations from the plan (+ why)
- D1 Halo 0.92 BU across = 0.45 H (plan 0.50 H) and 0.22 back / 0.74 above the skull centre: at 0.50 H and over the
  face it covered the mane and read as a cap brim from the side; slightly smaller and set back it floats as a halo.
- D2 Wing lengths: upper pair ~1.85 BU per side (plan 1.3 H = 2.8 BU), middle ~1.4, lower ~1.1. The bind pose must
  stay under the halo top (Studio scales the model by the bind-pose height) and a 2.6 H span made the 64 px icon tiny.
  The display pose still gives the tallest silhouette in the game.
- D3 OBSID share ~29-38 % (plan 14 %): the plan's own halo size + three mane rings + 36 feather tips; tips already
  trimmed once. The lilac-ivory body still reads light; the dark parts frame it (mane, halo, wing edges).
- D4 Muzzle pads / chin use WING_IN (the palette's near-white) so the face has a lighter muzzle than the lilac skull.
- D5 Placeholder `anim()` = the held display pose, only for the portrait / icons / value shares (real clips after).

## Value shares (flat ID renders of the display pose)
| colour | plan | side | tq | game |
|---|---|---|---|---|
| MOON_IVORY | 40 | 30.6 | 26.9 | 27.7 |
| IVORY_D | 10 | 13.0 | 6.9 | 9.1 |
| OBSID | 14 | 30.8 | 37.5 | 28.7 |
| WING_IN | 8 | 18.4 | 17.0 | 26.5 |
| BLOOD | 4 | 0.4 | 1.8 | 0.6 |
| GOLD | 2 | 1.9 | 4.9 | 2.4 |
| BLACK | 3 | 4.5 | 4.4 | 4.6 |

## Renders
`renders/_model_sheet.png` (bind pose), `renders/_idle_sheet.png` (display pose), `renders/_close_sheet.png` (head),
`renders/_icons_strip_64.png` / `_128.png` (vs Solar Lion, Griffin, Celestial Dragon, Cvetibara, Cosmic Leviathan,
Frostcrown Dragon), `renders/_icons2_strip_128.png` (portrait + game-camera icon).
