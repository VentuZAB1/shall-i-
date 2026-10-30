# Permafrost Titan - FINAL 8.5 GATE, ROUND 9 (model + clips, renders 2026-10-28 09:53-09:54) - FIX

**Model: 8.6/10 - PASS. Clips: 8.2/10 - FIX.**

Per clip: idle 8.5, walk 8.5, roar 8.5, act (kneel) 8.2. The clips score is the lowest, so it is **8.2 (act)**.

Summary: the round 9 build changed only the act (KNEE_OUT 0.06, pelvis drop 0.348, left arm -6). From the judged game camera the kneel is still not an L. The kneeling shin and foot sit behind the left forearm and fist, so the shin is not a separate limb and the claws do not show. The 0.06 gain is about 4 % on screen (builder's own numbers: 75.8 px to 79.1 px), which is not visible at phone size. The 3/4 view reads fully (thigh, dark knee plate, flat foot with claws). MUST 1 is the arm, not another leg tweak.

## What I looked at

- Brief `GLACIER_REVIEWER_BRIEF.md`; round 8 review `PermafrostTitan_final85_r8.md`; builder notes `PermafrostTitan\CLIP_NOTES.md` (ROUND 8 section).
- Renders, all opened and all loaded (09:53-09:54 set): `_kneel_2x_f40_f50.png`, `_kneel_2x_f30_f40_f50.png`, `_kneel_views.png`, `_beats2x_kneel.png`, `_beats2x_idle.png`, `_beats2x_roar.png`, `_roar_jaw_close.png`, `_walk_sheet.png`, `_roar_front_sheet.png`, `_pose_tq_sheet.png`, `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`.
- My own zoomed crops of the current 09:53 game and 3/4 f40 panels, in `%TEMP%` (not in the project): `C:\Users\ventu\AppData\Local\Temp\r9_game_f40_legs_x3.png` (3x) and `r9_tq_f40_legs_x25.png` (2.5x). The builder's `r8_*` crops in `%TEMP%` are from the 09:47 build, so I did not use them.
- Gate log `PermafrostTitan\_scratch\export_r8.txt` (HEADLESS_RESULT): collision_free true, collisions {}, ground_min_z act -0.016 (f20), linear 0, idle and walk loops 0 / 0, walk slide 0.0, tris_body 7,820.
- Not re-measured this round: act chest vs spine and head peak (4.68 / 14.1 are the round 6 numbers). The gate log has no angle probe.
- ANIM_REFS: Plate 356 (K3) and the K8a-c cuts are present. The ANIM_REFS rule passes.
- The builder's round 7 visibility table (`leg_px`) gave Shin_L 0.49 visible at f40. The current render does not match that. The projected-box share does not account for the forearm and fist in front of the shin, so do not use it as the pass test. Judge the render.

## Per-clip table

| clip | score | one line why | evidence file |
|---|---|---|---|
| idle | 8.5 | Unchanged. Hip weight shift, fist sway and the slow head look read at 2x. The sway and breath are still small at phone size, so the margin is thin. Feet stay planted. | `renders\_beats2x_idle.png` (f0/f30/f60/f90) |
| walk | 8.5 | Unchanged. Feet separate and one lifts; the torso rolls in the game row. Still soft at phone size. | `renders\_walk_sheet.png` (game row) |
| roar | 8.5 | Unchanged. Both arms out and level at f27 on the front sheet; head lifts; jaw open with a dark gap at f27. Mouth colour is the Studio check (lead ruling). | `renders\_roar_front_sheet.png`; `_beats2x_roar.png`; `_roar_jaw_close.png` |
| act (kneel) | **8.2** | Game camera: the kneeling shin and foot are hidden under the left forearm, fist and bracer (my 3x crop). Only the thigh and the dark knee plate show, so the L and the knee on the snow are not readable. The body drop and the 30 deg turn read. The 3/4 view reads fully (thigh, knee plate, flat foot with claws on the ground). The 0.06 ankle gain is not visible. | `renders\_kneel_2x_f40_f50.png` (game f40 panel); my crops `%TEMP%\r9_game_f40_legs_x3.png`, `r9_tq_f40_legs_x25.png`; `_kneel_2x_f30_f40_f50.png`; `_kneel_views.png`; `_beats2x_kneel.png` |

## Model (8.6 PASS)

Geometry is unchanged from round 8 (the round 9 build only changed the act). The model sheet, close sheet and icon strips were re-checked:

- Silhouette and species read at phone size. The fierce brows and slit eyes read in the close sheet. Mouth closed.
- The gold chest ring reads at 64 px (icon strip, first slot) and in the game view. The crust shoulders read at 128 px.
- Studded skin, mauve body and the ICE_W crust give the approved style. Tris 7,820 (cap 15k).
- The round 8 TO 9+ items are still visible: the light ICE_W band under the gold ring splits the chest (`_model_sheet.png`, front); white highlights still sit in the eye slits (`_close_sheet.png`); the mouth lip is slightly proud in the side close.

Model stays 8.6. Nothing new blocks it.

## New MUSTs (only what blocks 8.5 on the act)

**MUST 1 (act, blocks act 8.5). From the game camera the kneeling shin and foot must be visible, not hidden under the left arm.**

- What is wrong: at game f40 (`_kneel_2x_f40_f50` top-right, and my 3x crop) the left forearm, fist and bracer sit in front of Shin_L and Foot_L. The kneeling leg reads as a thigh that ends in the fist. The claws of the kneeling foot are not visible. Rounds 7 and 8 only moved the arm to clear collisions, so the arm hold has not been tuned for the shin's visibility.
- Fix (left arm hold only; keep KNEE_OUT 0.06, pelvis drop 0.348, yaw 30, standing foot 0.10, the knee band and the ground numbers as they are):
  1. In the probe, re-solve the left arm keys for f18-62 over these ranges: out -11 to +4 (round 8 used -6), fwd -6 to 14 (round 8 used 14), elbow bend 0 to 30 (round 8 used 14). Look for the first combination that meets every condition below. Start with the smallest change from the round 8 hold.
  2. Acceptance, all measured:
     a. Game f40 (2x render, plus a 3x crop of the lower body): the top edge of Shin_L breaks away from Leg_L with background between them, along at least one third of the shin length, and the Foot_L claws are visible.
     b. `collide_where`: 0 pairs for `Fore_L | Leg_L`, `Fist_L | Leg_L` and `Hand_L | Leg_L` over f18-62.
     c. Fist-to-thigh surface gap at least 0.05 (`fist_probe`), with the fist centre under the chest line (z below 0.80).
     d. Knee band and ground unchanged: knee lowest point over f18-52 in [-0.017, -0.005]; `ground_min_z` act at least -0.02; collision_free true; linear 0; idle and walk loops 0 / 0.
     e. The 3/4 f40 read stays as it is.
  3. If no arm hold passes (a) to (d), stop and report to the lead. Do not add another leg tweak; KNEE_OUT 0.06/0.08, the standing foot 0.10-0.25 and yaw 18-30 are already tried.
- The hidden standing leg is not a MUST (lead ruling). The snow puff at the knee is the lead's Studio VFX and is not scored.

## TO 9+ (not blocking)

- **Act, knee contact:** the knee is on the snow at -0.005 to -0.017 (numerically good). The contact will only read with the Studio snow puff. Do NOT add a further knee settle; it would sink the knee past the -0.02 gate.
- **Act, 3/4 standing leg:** the standing shin is still a stub behind the right fist (`r9_tq_f40_legs_x25.png`). Lateral only, 0.03-0.05 BU more, as a clearance check (round 8 TO 9+).
- **Act, re-measure:** re-run `ang_probe` for the act. Chest vs spine 4.68 and head 14.1 are round 6 values. The arm change may move the head and chest, so log the numbers this round (pose limits: chest vs spine at most 5, head + neck at most 30).
- **Model, belly band:** shorten the light ICE_W band under the gold ring from half-height 0.036 to about 0.028 BU, or key it to a MAUVE tone, so the chest reads as one mass.
- **Model, eye slits:** darken the white highlights inside the slits toward (200, 220, 236).
- **Model, lip:** pull the lip from 0.012 to about 0.008 BU so it does not read as poking out in the side close.
- **Idle:** the fist sway is still small at phone size. A small increase in arm sway is allowed; the closest fist-to-thigh gap logged for the idle is 0.067, so there is room.
- **Walk:** a larger step lift at f24-30 in the game view (round 8 TO 9+).
- **Roar:** mouth colour in Studio (lead ruling).

## Pass / fail checklist

- Silhouette and species at phone size: PASS.
- Face (brows, slits, closed mouth): PASS (white slit highlights still open, TO 9+).
- Gold hero at 64 px: PASS (icon strip, first slot).
- Tris 7,820 (cap 15k): PASS (export_r8.txt; geometry unchanged).
- Collision-free, linear 0, idle and walk loops 0 / 0, walk slide 0.0, ground act -0.016 (export_r8.txt): PASS.
- Chest vs spine and head + neck (act and roar): NOT RE-MEASURED this round; round 6 values 4.68 / 14.1 (TO 9+ re-log). Roar head peak 15 from round 6 notes.
- Neck at most 8: not applicable (no Neck bone; head + neck at most 30 applies).
- Knee on the snow, act hold (f18-52): numerically PASS (-0.005 to -0.017).
- Kneeling L from the game camera (shin and foot visible): **FAIL** (MUST 1).
- Knee contact readable from the game camera: **FAIL** (same cause as MUST 1; the snow puff VFX is added in Studio).
- 3/4 kneel read: PASS (`r9_tq_f40_legs_x25.png`).
- Body drop and 30 deg turn from the game camera: PASS.
- Idle, walk, roar readable at phone size: PASS at 8.5 each (margins thin on idle and walk).
- ANIM_REFS rule (Plate 356 K3, K8a-c): PASS.
- Mouth colour, snow puff VFX: Studio, not scored.
