# Blizzard Roc - model gate notes (builder D, 2026-10-27)

File: `pets/BlizzardRoc.py` (Thunderbird / Inferno Phoenix wing-biped kit). Plan: `_review/BlizzardRoc_plan.md` v2.



## ROUND 8 (review 7: model 8.6) - 9+ M3b + M4b
- **M3b, mantle band:** the middle shingle row on the Chest and the upper row on the Spine are CHAR. The wing arm bar
  and wrist (the leading edge) are CHAR too: the shingle rows alone left STORM + MANTLE at 45.8 percent.
  Game-camera shares: STORM_GREY 22.4 + MANTLE 14.3 = **36.7 %** (target <= 40); CHAR **29.8 %**
  (target >= 20); SNOW 16.5; FROST_V 9.2.
- **M4b, eye:** the FROST_H hot-spot bar is gone (and so is the FROST_H colour). The eye is a FROST_V slit with a
  BLACK slit pupil in the black socket, with no pale dash (`renders/_head2x_sheet.png`).
- Tris 12,940. Re-rendered: `_model_sheet.png`, `model_*.png`, `_head2x_sheet.png`, `BlizzardRoc_icon.png` + strips.

## ROUND 7 (review 6: model 8.5 PASS; model TO 9+)
- **M1 tail blade:** the outer tail pair's feather faces are tilted 40 deg about the tail axis (edges up and out), so the
  side view shows a blade. The inner pair stays flat.
  - Tilting the other way, edges toward the legs, cut the trailing shins in fly, takeoff and land at 14-40 deg.
  - `renders/model_side.png` shows the blade; `model_game.png` still shows the fan.
- **M3 mantle:** a new MANTLE (158,160,170) on the two dorsal saddles and the back shingles. On the game camera:
  STORM_GREY **31.7 %** (was 47 %) + MANTLE 16.0 %, CHAR 18.8 %, SNOW 16.4 %.
- **M4 eye:** `renders/_head2x_sheet.png` (2x head, front + game). The eye reads as a FROST_V slit in the black
  socket, and the small hot spot no longer reads as a glint.
- **M2 wing twist: not done.** The model views render the bind pose. +16 deg on the bind feathers would shift every
  clip's wing twist by 16 deg, including the FOLD / LIFT keys of an approved clip set. In play the wings are always
  posed.
- Tris 12,964. Re-rendered after the last change: `_model_sheet.png`, `model_*.png`, `BlizzardRoc_icon.png`, the
  strips, `_head2x_sheet.png`.

## ROUND 6 (review 5: model 8.5 APPROVED; MUST 4 + model TO 9+)
- **MUST 4 (stale evidence):** re-rendered after the tail change, with the code final:
  - `renders/_model_sheet.png` (tq / front / side / back / game / top, 600 px);
  - `renders/model_game.png`, `model_side.png`;
  - `BlizzardRoc_icon.png` + `_icons_strip_64|128.png`, `_icons2_strip_64|128.png`.
- **TO 9+ tail from behind:** the outer pair is fanned **+-14** (was +-12) and tapered harder (taper 0.45 -> 0.58), so
  the outer two read as feather blades, not rods. On the game camera (`model_game.png`, `_pose_game_walk_sheet.png`)
  the tail shows as a spread wedge with four violet tips behind the folded primaries.
- **TO 9+ eye hot spot:** the FROST_H bar is 0.010 x 0.002 (was 0.014 x 0.003).
- **Not changed:** the trouser block. A deeper coil is blocked by the flank skirt, not the trouser (`CLIP_NOTES.md`).
- Tris 12,964 (unchanged).

## REVIEW 2 FIXES (APPROVED WITH FIXES 8/10)
- M1 eye = a violet slit under a black lid: socket (0.046*sc, 0.008, 0.011*sc) at z +0.004*sc, hot spot
  0.014*sc x 0.003*sc (slit 0.045*sc x 0.0085*sc kept). `renders/head_front.png`, `renders/_eye_sheet.png`.
- M2 one strip, no duplicate angle: `renders/_icons_strip_64.png` / `_128.png` = Roc, Frostfang Lynx, Ice Mammoth,
  Glacier Yeti, Thunderbird, Griffin, Inferno Phoenix, Frostcrown Dragon.
- M3 `renders/model_tq.png` 600 x 600 (all model views 600; `model_under.png` 600, ground hidden).
- M4 printed by `model()`: `"tris": 12964, "size": [4.0, 2.01, 2.03], "H": 1.996, "lowest": -0.031,
  "crest_tip": [0.0, -0.378, 1.99], "span": 3.999}` -> span 3.999 / H 1.996 = **2.00 H** (bind pose).
- M5 root lift: every ground clip plants the feet FOOT_LIFT (0.014) up; step 1 with the clips: ground_min_z idle
  -0.017, walk -0.018, takeoff / land / roar / act_bow -0.017 (>= -0.02); collision_free true.
- Value shares after M1 (flat IDs, fold idle): side SNOW 18.9 / STORM 38.4 / CHAR 25.8 / FROST_V 8.5; game SNOW 16.1 /
  STORM 47.5 / CHAR 19.2 / FROST_V 9.5.

## ROUND 2 (review 1, APPROVED WITH FIXES 7/10) - all MUST 1-6 + NICE 1, 2 applied; supersedes the sections below
- Tris 12,964. HEIGHT 9.0 studs = crest top (model top 1.996 BU).
- **Span (bind pose) 3.999 BU = 2.00 H** (MUST 1: tip `_raise((2.11 + WDX, 0.30, 1.40))`, ELEV kept 14).
- Ground fold re-searched for the new span: 45 / 81 collision-free, FOLD = (86, 10, -80, 10); `fold_pairs` clean;
  step 1 (`headless_full ... - 1`, placeholder idle) collision_free true. ground_min_z -0.031 (talon hooks in the bind
  pose): fixed with the clips (root lift), gate >= -0.02.
- MUST 2 covert bars FROST_V (straight, one per covert). MUST 3 crest fracs (0.40, 0.60), widths 0.115 / 0.105.
  MUST 5 Neck2 top cape row SNOW. MUST 6 tail feathers 0.22 wide, taper 0.45. NICE 1 middle breast chevron FROST_V.
  NICE 2 belly strip 0.13.
- MUST 4 mask: the socket plate is gone; ONE CHAR stripe starts AT the eye and runs back along the skull side into the
  nape; slim V brow (0.072, 0.020, 0.018); the FROST_V slit thinner (half-height 0.0125 -> 0.0085) and set low under
  the black lid (slit, FROST_H spot and pupil kept, D3). From the front the eyes no longer sit in a frame.
- Value targets needed more than MUST 2 / 5 (CHAR side only 36.7 -> 35.2, SNOW game 10.7 -> 12.9), so (R = round-2
  deviations, please judge):
  - R1 Primaries: STORM_GREY root (40 % of the length), then a CHAR band, the FROST_V bar and a CHAR point
    (`PBARS = [(CHAR, .11), (FROST_V, .17), (CHAR, .32)]`). The wing tips stay dark; the side-view flank slab breaks up
    (NICE 3).
  - R2 The white nape collar continues down the whole neck back (Neck2 row 0.50 + Neck row 0.85 SNOW): white head and
    neck from behind, grey from the mantle.
  - R3 White rump + uppertail coverts + tail base (seen by the game camera); the four tail feathers keep STORM bases.
  - R4 Inner 3 of 7 coverts SNOW (snowy shoulder); secondary CHAR trailing edge 0.30 -> 0.18 of the length.

| colour (flat IDs, fold pose) | plan | side | tq | game | review target |
|---|---|---|---|---|---|
| SNOW | 36 | 19.0 | 32.7 | **15.9** | game >= 15 |
| STORM_GREY | 25 | 38.3 | 27.5 | 47.4 | |
| CHAR | 16 | **25.7** | 19.7 | **19.2** | side <= 28, game <= 22 |
| PALE_G | 6 | 1.9 | 4.5 | 2.0 | (NICE 2 applied; the folded wing covers the belly from the side) |
| FROST_V | 5 | 8.5 | 6.3 | 9.5 | <= 12 |
| BEAK / BLACK | 3 / 3 | 2.7 / 3.5 | 4.2 / 4.6 | 2.2 / 3.6 | |

- Renders (round 2): `renders/_model_sheet.png` (bind, 600 px, incl. `model_under.png` = under view, ground hidden),
  `renders/_close_sheet.png` (head front / game / tq + crest side / back), `renders/_idle_sheet.png` (ground fold),
  `renders/_icons_strip_64.png` / `_128.png` (vs Thunderbird, Griffin, Glacier Yeti, Ice Mammoth, Inferno Phoenix),
  `renders/flat_side|tq|game.png`.

## Round-1 notes

## Numbers
- Tris 12,284 (plan 9-13k). HEIGHT 9.0 studs = crest top; model top 1.996 BU (crest), stud pitch 0.0505.
- Bind-pose span 3.78 BU = 1.9 H (wings raised 14 deg in the bind pose; open flight span ~2.1 H).

## What I built
- Snowy raptor leaning 35 deg: SNOW keeled breast + lower body, STORM_GREY dorsal saddles, rump and mantle shingles
  (each shingle has a CHAR barred tip), PALE_G shading strip + lowest breast-shingle row along the belly slope.
- 2-bone S-neck: SNOW front, STORM_GREY nape cape (2 shingle rows per segment) running into the mantle.
- Head: rounded SNOW skull, osprey CHAR eye mask (a plate round each socket + a stripe back along the skull to the
  nape), heavy CHAR V brow, BLACK lid-heavy socket with a FROST_V slit, FROST_H hot spot on the outer half and a BLACK
  slit pupil (no glint). CHAR cere, BEAK dark-steel hook bill with a BLACK hook point, BEAK mandible, MOUTH gape.
- ERECT crest: 3 flat plumes rising ~68 deg (centre) / ~60 deg (sides, splayed 22 deg) from the crown, SNOW with
  FROST_V points (45 % of the length), own `Crest` bone.
- Breast: three CHAR chevron bars (snowy-owl barring) lying flush on the keel front.
- Wings (wing3, per side): SNOW shoulder, STORM_GREY arm bar + wrist, CHAR hand bar; 7 coverts (STORM_GREY, CHAR barred
  tips, SNOW at the shoulder), 8 STORM_GREY secondaries with a CHAR trailing edge, 3 + 5 CHAR primaries each with a
  FROST_V bar and a CHAR point, 4 grey hand coverts.
- Legs: SNOW feathered trousers with a ragged SNOW / PALE_G cuff, CHAR scaled tarsus (BEAK scale bands), 3 CHAR toes +
  hallux, BLACK hooked talons.
- Tail: STORM_GREY base + coverts, FOUR plain feathers (spread +-2.5 / +-8 deg, no fan): STORM_GREY, FROST_V bar,
  CHAR point.
- Rig + VFX anchors already in `rig()`: FX_FrostTrail_L/R [WingTip_L/R], FX_CrestSparkle [Crest], FX_BreathCloud [Head],
  FX_FrostDust [Tail2], FX_SnowPuff_LandL/R [Foot_L/R]. check_pairs() / joints() written.
- Ground FOLD searched on this body (`fold_search`, cloak grid): 36 / 54 collision-free; FOLD = (86, 6, -80, 10).

## Deviations from the plan (+ why)
- D1 Wing root moved out 0.05 (WDX, the Thunderbird recipe): with the root on the flank every cloak fold cut the
  lower body (0 / 54 free); with WDX 0.05, 36 / 54 free.
- D2 Crest plumes 0.12-0.15 H long (plan 0.10 H) and 0.09-0.10 BU wide: at 0.10 H the crest vanished at 64 px.
- D3 Eye has a small FROST_H (228,216,255) hot spot (the creature-style eye recipe: socket + bright slit + hot centre).
- D4 CHAR barred tips on the mantle shingles + coverts (snowy-owl / gyrfalcon barring): with plain STORM_GREY the back
  read as a flat pale slab ("grey plastic"); this keeps the plan colour and puts the dark tones on the back.
- D5 Placeholder `anim()` = an idle held at the FOLD, only so the portrait / 64 px icon / value shares show the ground
  pose players see. It is replaced by the real clips after this gate.

## Value shares (flat ID renders of the ground fold pose; plan = side estimate)
| colour | plan | side | tq | game |
|---|---|---|---|---|
| SNOW | 36 | 19.6 | 34.4 | 10.7 |
| STORM_GREY | 25 | 28.2 | 21.0 | 46.9 |
| CHAR | 16 | 35.9 | 25.1 | 27.6 |
| PALE_G | 6 | 2.1 | 4.7 | 1.4 |
| FROST_V | 5 | 7.6 | 4.8 | 7.6 |
| BEAK / BLACK | 3 / 3 | 2.8 / 3.6 | 4.6 / 4.9 | 2.2 / 3.4 |
The folded wing covers the flank in the side view (CHAR primaries); the tq view matches the plan. The game camera
(behind, high) sees the grey back as the largest zone and no white fan (plan gate 2).

## Renders
`renders/_model_sheet.png` (bind pose), `renders/_idle_sheet.png` (ground fold pose), `renders/_close_sheet.png`,
`renders/_icons_strip_64.png` / `_128.png` (vs Lynx, Mammoth, Yeti, Frostcrown Dragon, Thunderbird, Griffin, Phoenix).
