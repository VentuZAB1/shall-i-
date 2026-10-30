# Permafrost Titan - FINAL 8.5 GATE, ROUND 5 (model + clips, export 2026-10-28 05:11) - FIX

**Model: 8.4/10 - FIX. Clips: 7.7/10 - FIX.**

Per clip: idle 7.6, walk 7.6, roar 8.0, act (kneel) 7.5.

Owner bar: 8.5 is the floor for the model and for every clip. Nothing under 8.5 ships.

Round 4 did what it said on the waist (MM1 PASS). The model is now a clear, fierce titan with a strong gold hero. It still reads as a stack of bands with a small head, and the crust clusters are noisy at 64 px. The clips did not move much: the kneel is still not legible from the game camera, the idle and walk arm motion is too small to read, and the roar mouth is still a grey slab in the kit render.

## What I looked at

- Brief (`GLACIER_REVIEWER_BRIEF.md`), round 4 review (`PermafrostTitan_final85_r4.md`), builder notes `MODEL_NOTES.md` and `CLIP_NOTES.md` (both "FINAL 8.5 ROUND 4" sections), `_scratch/fist_r4.txt`, `_scratch/clipgate_r4.txt`, `_scratch/export_r4.txt`, `_scratch/joints_r4_f40.txt`.
- Renders, newest set (title bars 05:05, pose sheet 05:11). Opened and loaded: `_model_sheet.png`, `_kneel_2x_f40_f50.png` (tq and game), `_kneel_views.png` (front, tq, back, game at f18, f40, f58), `_beats2x_kneel.png`, `_beats2x_idle.png`, `_beats2x_roar.png`, `_walk_sheet.png`, `_roar_jaw_close.png`, `_pose_tq_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `hx_game_act_kneelrise_40.png`, `hx_tq_act_kneelrise_40.png`, `_scratch/zoom_game_kneel_r4.png`.
- My own crops (outside the review folder, in the temp dir): the tq f40 left fist and kneeling thigh at 3x; the game f40 left leg at 3x; the idle left arm across f0, f30, f60, f90 at 2x. I also cropped the walk sheet, but the panel coordinates were wrong, so I did not use it.
- Not opened: `_icons_strip_128`, `_icons2_*`, `flat_*`, `gamelook_*`, `_cv_kneel_*`. No image failed to load.
- Note: the game camera sits behind the Titan. The face is hidden in the game view, so game-camera items are judged from behind.

## Numbers (logs, not re-run)

- Tris 7,664 (under 15k). PASS.
- collision_free true. Loops 0 / 0. Linear 0. Walk slide 0. Idle foot drift 0. PASS.
- ground_min_z: idle 0.000, walk 0.000, roar 0.000, act -0.017 at f20 (limit -0.02). PASS, but at the edge.
- Chest vs spine: idle 4.85, walk 2.5, roar 3.0, act 4.68 (limit 5). PASS.
- Head pitch: roar 15, act 14.1 (head + neck <= 30, per the lead's ruling). PASS.
- Gold at 64 px: kit counter portrait 54 / game 27; render window portrait 47 / game 20. Both pass the gate (>= 25 portrait, >= 20 game). The game-camera figure is at the gate edge.
- Fist probe (`fist_r4.txt`, f30 / f40 / f46): surface gap 0.092, fist centre to thigh surface 0.372, fist centre z 0.502, chest line z 0.824.

## Round-4 items

**Model**

- **MM1 waist: PASS.** In `_model_sheet` (front, side) the waist steps in under the chest and out to the hips, with the belt seam tucked as a step. The side view reads as a waist now, not a straight column. The torso still reads as stacked bands, which is the 8.4 reason below, not this item.

**Clips**

- **MC1 kneel L from the game camera: FAIL.**
  - From the tq (`_kneel_2x` tq f40 and f50, and my crop of the L fist): PASS. The left fist sits on the front of the kneeling thigh, at knee height, and reads as a hand on the knee.
  - From the game camera (`_kneel_2x` game f40 and f50, `hx_game_act_kneelrise_40`, my 3x crop `game_f40_legL`): the kneeling leg reads as a vertical thigh and shin block, with a foot block and a dark heel plate toward the camera. The knee on the snow is not legible, and the shin's backward lean is lost. A viewer would read it as one leg stepping back, not a kneel. The builder's foreshortening warning is correct.
  - The angle change (31.4 to 21.5 deg) is too small to change the silhouette. The fix below is a larger geometry change.
- **MC2 idle arm sway: PARTIAL.**
  - Numerically the sway is in place (+/-5). Visually, in `_beats2x_idle` and my 2x crop of the left arm across f0 / f30 / f60 / f90, the fist and bracer move only a few pixels. The pauldrons barely move. The builder did not log the f0-to-f30 fist displacement, so the 0.05 BU acceptance is unverified.
- **MC3 walk swing: PARTIAL.** `_walk_sheet` tq shows the arms swinging, but the travel is modest. The closest fist-to-thigh distance of 0.065 leaves no room to swing more at the shoulder.
- **MC4 jaw cavity: PARTIAL.** `_roar_jaw_close` f27 (front and tq) shows the cavity as a flat grey slab, about (85, 88, 95) in the render. It reads as a grey panel, not a dark opening. The builder says Studio will be darker. That is not verified here, and the lead ruled that colour is judged in Studio.
- **Fist re-measure: visual PASS, numeric test needs restating.** The tq read holds (fist on knee). But the round-3 test asked for the fist centre within 0.03 of the thigh surface, and the round-4 centre is 0.372 away. The builder changed the metric to a surface gap of 0.092. The lead should restate the test in the next notes (see ruling below).

**Other rows**

- Chest vs spine, head pitch, collision, ground, tris: PASS (above).
- Gold at 64: PASS (27 kit / 20 render).
- Fierce face (`_close_sheet`): PASS. Heavy brows, slit eyes, closed mouth line, no glints.
- Blunt ice, no spikes, no glow: PASS.

## New MUSTs (only what blocks 8.5)

**Model (8.4 -> 8.5)**

- **MD1. Head is small (the stack reads as blocks).** `pets/PermafrostTitan.py` L206, skull half-width 0.160 -> 0.172 (+7.5 %), height unchanged. Scale the brow, slit and jaw X offsets by the same 1.075 so the face stays put on the skull.
  - Acceptance: `_model_sheet` front shows a head at least 0.34 BU wide (was 0.32). `collide_where` head vs neck and shoulders 0 pairs. Head pitch unchanged.
- **MD2. Crust clusters read as white noise at 64 px.** Each pauldron top and each fist knuckle crust: reduce the three flat-topped chunks to two, each at least 0.06 BU in its smallest half-size.
  - Acceptance: `_icons_strip_64` (first icon) shows the shoulder crust as two clear masses, not a white fringe. Tris within 200 of 7,664. `collide_where` 0 pairs at the pauldron and fist.

**Clips (7.7 -> 8.5)**

- **MC1'. Game-camera kneel L (blocks act 7.5).** In the kneel hold (f18-52), move the `Shin_L` ankle hold from (0, 0.365, 0.101) to (0, 0.41, 0.06), with the toe curl kept at 16. The knee stays pinned (`Knee_L` z <= 0.00).
  - This lays the shin back at about 12 deg above horizontal, with the toes on the snow.
  - Acceptance: from the game camera (behind) at 2x, f40 and f50 show the shin lying back with the toe and sole toward the camera, and the knee reads on the snow. `ground_min_z` >= -0.02. `collide_where` 0 pairs. Chest vs spine <= 5.
  - If this alone fails, one alternative: a body yaw of 15-20 deg toward the L side during f18-52 (Root only, no chest change), so the shin is seen side-on. Use one of the two, not both.
- **MC2'. Idle reads too small (blocks idle 7.6).** Keep the arm sway at +/-5 and add a forearm bend of +/-4 deg on `Fore_L` and `Fore_R`, opposite to the arm sway.
  - Acceptance: fist travel f0 to f30 is at least 0.05 BU (log it in CLIP_NOTES). `collide_where` fist vs thigh 0 pairs at the swing extremes. Idle foot drift 0.
- **MC3'. Walk arm travel (blocks walk 7.6).** Keep the shoulder swing at 9 deg. Add a forearm bend of +/-6 deg on `Fore_L` and `Fore_R`, in the opposite phase to the arm.
  - Acceptance: fist travel f0 to f42 at tq is visibly larger than now. `collide_where` fist vs thigh at least 0.03 BU at the extremes. Walk slide 0.
- **MC4'. Roar mouth (blocks roar 8.0).** The jaw cavity colour at L225 goes from (24, 26, 34) to (10, 10, 14). Add a 0.012 BU upper-lip overhang over the cavity, so the cavity sits in the lip's shadow.
  - Acceptance: `_roar_jaw_close` f27 (front and tq) shows a dark opening, with the cavity measurably darker than the current (85, 88, 95). If the kit render cannot get the cavity below about 60 luma, the Studio check is required and this item stays open until it is seen there.

## TO 9+ (not blocking)

- Torso: the chest and waist bands still read as stacked slabs from the front. A 0.02 BU bevel on the belt lip would soften the step.
- Eye slits: bright white bars in `_close_sheet`. The round-3 suggestion of a darker ice tone (about 200, 220, 236) is still open.
- Walk and idle: the lowest clip scores. MC2' and MC3' are the largest lift for the least risk.
- Kneel: a small snow puff at the knee contact (`icecrack`) would sell the kneel from the game camera.
- Roar: the head pitch of 15 leaves room for a slightly deeper bellow, if the lead wants more drama.

## Ruling needed (not scored)

- **Neck rule:** the lead's ruling (head + neck <= 30) is applied. Head pitch is 15 (roar) and 14.1 (act). PASS.
- **Fist test:** round 3 asked for the fist centre within 0.03 of the thigh surface. The round-4 centre is 0.372 away, so the test as written would fail. The visual read passes. The lead should restate the test as "fist surface gap >= 0.09 and no collision, and the tq reads as a hand on the knee", and say so in the notes.
- **Gold:** the game-camera gold is 27 on the kit counter and 20 on the render window. Both pass, but the render window is on the gate edge. State which counter the ship bar uses.
- **Colour:** not scored, per the lead ruling. The MC4' Studio check depends on it.

## Summary

- Model 8.4 (FIX). Clips 7.7 (FIX): idle 7.6, walk 7.6, roar 8.0, act 7.5.
- Round-4 items: MM1 PASS. MC1 FAIL (game-camera kneel). MC2 PARTIAL. MC3 PARTIAL. MC4 PARTIAL.
- New MUSTs: MD1 head +7.5 %; MD2 crust chunks 3 to 2; MC1' shin ankle back and low; MC2' forearm bend +/-4; MC3' forearm bend +/-6; MC4' cavity (10, 10, 14) with a 0.012 lip.
