# Permafrost Titan - FINAL 8.5 GATE, ROUND 8 (model + clips, renders 2026-10-28 09:41-09:43) - FIX

**Model: 8.6/10 - PASS. Clips: 8.2/10 - FIX.**

Per clip: idle 8.5, walk 8.5, roar 8.5, act (kneel) 8.2. The clips score is the lowest, so it is **8.2 (act)**.

Summary: the standing-foot step (0.10) has no visible effect. From the game camera the kneel still reads as one thigh column that runs into a foot block. The shin is not a separate limb and the knee contact is not readable. The body drop and the 30 deg turn do read, and the 3/4 view reads better. Per the lead ruling, the hidden standing leg is not counted. The act needs one fix (MUST 1) before it can reach 8.5.

## What I looked at

- Brief `GLACIER_REVIEWER_BRIEF.md`; round 7 review `PermafrostTitan_final85_r7.md`; builder notes `PermafrostTitan\CLIP_NOTES.md` (ROUND 7 section).
- Renders, all opened and all loaded (09:41-09:43 set): `_kneel_2x_f40_f50.png`, `_kneel_2x_f30_f40_f50.png`, `_kneel_views.png`, `_beats2x_kneel.png`, `_beats2x_idle.png`, `_beats2x_roar.png`, `_walk_sheet.png`, `_roar_front_sheet.png`, `_roar_jaw_close.png`, `_pose_tq_sheet.png`, `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `flat_game.png`, `flat_tq.png`.
- My own crops, outside the project (saved to `%TEMP%`): `r8_game_f40_legs.png` (game f40 lower body) and `r8_tq_f40_legs.png` (3/4 f40 legs).
- Gate log `PermafrostTitan\_scratch\export_r7.txt` (HEADLESS_RESULT): collision_free true, collisions {}, ground_min_z act -0.017 (f20), linear 0, idle and walk loops 0 / 0, walk slide 0.0 (audit), tris_body 7,820.
- `ANIM_REFS.md`: Muybridge Plate 356 (kneel and rise, K3) and the K8a-c cuts are present. The ANIM_REFS rule passes.
- Not re-measured this round: act chest vs spine and head peak (4.68 / 14.1) are the round 6 numbers (see NICE).

## Per-clip table

| clip | score | one line why | evidence file |
|---|---|---|---|
| idle | 8.5 | Unchanged since round 7. Weight shift, one slow head look and the fist sway read at 2x; the sway is still small at phone size. Feet stay planted. Margin is thin. | `renders\_beats2x_idle.png` (f0/f30/f60/f90) |
| walk | 8.5 | Unchanged. Feet separate and one lifts; the torso rolls in the game row. Readable from behind, still soft at phone size. | `renders\_walk_sheet.png` (game row) |
| roar | 8.5 | Unchanged. Both fists are out and level at f27 on the front sheet; head lifts; the jaw opens with a dark gap at f27 (front and 3/4 close). Judge mouth colour in Studio. | `renders\_roar_front_sheet.png`; `_beats2x_roar.png`; `_roar_jaw_close.png` |
| act (kneel) | **8.2** | Body drop and the 30 deg turn read from the game camera; the 3/4 view reads as a kneel (dark knee plate, shin back to a clawed foot). But from the game camera the thigh runs straight into a foot block, the shin is not a separate limb, and the knee contact is not visible. The standing-foot change (0.10) is invisible at f40. | `renders\_kneel_2x_f40_f50.png` (game + 3/4 f40/f50); `_kneel_2x_f30_f40_f50.png`; `_kneel_views.png`; `_beats2x_kneel.png`; my crops `%TEMP%\r8_game_f40_legs.png`, `r8_tq_f40_legs.png` |

## Model (8.6 PASS)

Geometry is unchanged this round (the round 7 build only changed the act). The model sheet, close sheet and icon strips were re-made and checked:

- Silhouette and species read at phone size. The fierce brows and slit eyes read in the close sheet. Mouth closed.
- The gold chest ring reads at 64 px in the first icon slot and in the game view. The crust shoulders read at 128 px.
- Studded skin, mauve body and the ICE_W crust give the approved style. Tris 7,820 (cap 15k).
- The round 7 TO 9+ items are still open in the renders: the light ICE_W belly band under the gold ring still splits the chest and waist; white highlights still sit in the eye slits in the close sheet; the mouth lip is still slightly proud in the side close.

Model stays 8.6. Nothing new blocks it.

## New MUSTs (only what blocks 8.5 on the act)

**MUST 1 (act, blocks act 8.5). From the game camera the kneeling shin must read as its own limb.**

- What is wrong: in `_kneel_2x_f40_f50` (game f40 and f50), and in my crop `r8_game_f40_legs.png`, the kneeling thigh is a column from the hip that ends in a flat foot block with a heel plate. The shin is foreshortened into that block, and the knee contact is not visible. From the high game camera the L shape is weak.
- Fix (IK targets only; no new bones; yaw stays at 30, the lead's cap):
  1. Kneeling knee out: `KNEE_OUT = 0.06` BU (away from the centreline). Round 7 tested this and dropped it for two faults: the knee lifted off the snow, and the left forearm went into the thigh (`Fore_L | Leg_L`, f21-30). Re-solve both in the probe, not by hand:
     a. Raise the pelvis drop in steps of about 0.002 BU, re-running the ground probe, until the lowest knee point over f18-52 is between **-0.005 and -0.017**.
     b. Lower the left elbow bend, or nudge the left out angle, until `collide_where` reports **0 pairs** for `Fore_L | Leg_L` over f18-62. Keep the left fist at least **0.05 BU** clear of `Leg_L`.
  2. Fallback, only if step 1 cannot reach 0 collision pairs with the knee on the snow: move the kneeling ankle target **0.08 BU** laterally (away from the centreline) for f18-52, eased in and out with the rest, and re-run the ground probe with the same knee band.
- Acceptance:
  - Model/gate: knee lowest point over f18-52 in **[-0.017, -0.005]**; `ground_min_z` act **>= -0.02**; `collide_where` **0 pairs** (all clips); chest vs spine **<= 5** and head + neck **<= 30** (act and roar); idle and walk untouched.
  - Render: at 2x, game f40 lower body shows the thigh and the shin as two shapes. The shin's top edge breaks away from the thigh's lower end, with a visible knee corner and background at the join, along at least one third of the shin length. The 3/4 f40 read stays as it is.
- The hidden standing leg is NOT a MUST (lead ruling). The snow puff at the knee is the lead's Studio VFX and is not scored.

## TO 9+ (not blocking)

- **Act, knee settle: do NOT add the round 7 "0.04 BU knee settle".** The knee already rests on the snow at -0.005 to -0.017. A further 0.04 would sink it past the -0.02 gate. Leave the knee where it is.
- **Act, 3/4 standing leg:** the standing shin ends as a stub under the right fist in `r8_tq_f40_legs.png`. If the lead wants more of it, lateral only, not forward: 0.03-0.05 BU more stand-out on `Foot_R` in the hold (a clearance check, not a MUST).
- **Act, re-measure:** re-run `ang_probe` for the act. Chest vs spine 4.68 and head 14.1 are round 6 values; the standing-foot change should not move them, but they are not re-logged.
- **Model, belly band:** shorten the light ICE_W band under the gold ring from half-height 0.036 to about 0.028 BU, or key it to a MAUVE tone, so the chest reads as one mass.
- **Model, eye slits:** darken the white highlights inside the slits toward (200, 220, 236), as round 3 suggested. Still visible in `_close_sheet.png`.
- **Model, lip:** pull the lip from 0.012 to about 0.008 BU so it does not read as poking out in the side close.
- **Idle:** one smaller second head look later in the cycle, and a little more breath at phone size.
- **Walk:** a larger step lift (f24-30) in the game view. The feet separate now but stay small at phone size.
- **Roar:** judge the mouth colour in Studio, as the lead ruled. Check the roar from the game camera before ship.

## Pass / fail checklist

- Silhouette and species at phone size: PASS.
- Face (brows, slits, closed mouth): PASS (glints still open, TO 9+).
- Gold hero at 64 px: PASS (icon strip, first slot).
- Tris 7,820 (cap 15k): PASS.
- Collision-free, linear 0, idle and walk loops 0 / 0, walk slide 0.0 (export_r7.txt): PASS.
- Ground minimum -0.017 (act, f20): PASS (edge of -0.02).
- Knee on the snow, act hold (f18-52): numerically PASS (-0.005 to -0.017); not visible from the game camera (MUST 1).
- Chest vs spine <= 5, head + neck <= 30 (act and roar; no Neck bone, so the neck <= 8 rule does not apply): PASS (round 6 numbers).
- Idle fist range and gap, walk gap: PASS (round 6 numbers, unchanged).
- Roar arms symmetric at f27 (front): PASS.
- Kneeling L from the game camera (thigh down, shin back): **FAIL** (MUST 1).
- 3/4 kneel read: PASS (tq f40).
- Body drop and 30 deg turn from the game camera: PASS.
- ANIM_REFS rule (Plate 356, K3, K8a-c): PASS.
- Mouth colour, snow puff VFX: Studio, not scored.
