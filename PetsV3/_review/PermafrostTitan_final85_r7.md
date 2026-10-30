# Permafrost Titan - FINAL 8.5 GATE, ROUND 7 (model + clips, renders 2026-10-28 09:17-09:18) - FIX

**Model: 8.6/10 - PASS. Clips: 8.1/10 - FIX.**

Per clip: idle 8.5, walk 8.5, roar 8.5, act (kneel) 8.1. The clips score is the lowest, so it is **8.1 (act)**.

Summary: round 7 closes the two model items (MD-A seam, MD-B evidence) and the three numeric clip items (IDLE-1, WALK-1, ROAR-1). The kneel is still the weak clip. The 30 deg yaw clearly improves the shin, and the sole and heel plate now face the game camera. But from the game camera the kneel still reads as one thigh column that ends in a sideways foot. The forward standing leg is hidden behind the body, and the knee cap on the snow is not visible.

## What I looked at

- Brief `GLACIER_REVIEWER_BRIEF.md`; round 6 review `PermafrostTitan_final85_r6.md`; builder notes `PermafrostTitan\MODEL_NOTES.md` (ROUND 6 section) and `CLIP_NOTES.md` (ROUND 6 section).
- Renders, all opened and all loaded (all are the round 6 set, 09:17-09:18, none stale): `renders\_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `_icons2_strip_64.png`, `_icons2_strip_128.png`, `_kneel_2x_f40_f50.png`, `_kneel_views.png`, `_beats2x_kneel.png`, `_beats2x_idle.png`, `_beats2x_roar.png`, `_walk_sheet.png`, `_roar_front_sheet.png`, `_roar_jaw_close.png`, `_pose_tq_sheet.png`; plus `PermafrostTitan\_scratch\yaw_cmp_zoom.png` and `yaw_cmp_f40.png`.
- My own crops, outside the project (saved to `%TEMP%`): game f40 and tq f40 lower body from `_kneel_2x_f40_f50.png`; game walk row f12-f30 from `_walk_sheet.png`.
- Logs (`PermafrostTitan\_scratch\`): `clipgate_r6.txt` (HEADLESS_RESULT), `ang_r6.txt`, `arm_r6.txt`, `export_r6.txt`, `game_icon_r6.txt`, `pack_post_r6.json`.
- `ANIM_REFS.md` was not re-opened this round. No new references were added in round 6.

## Numbers (from the logs)

- Tris body **7,820** (cap 15k). PASS.
- `collision_free` true, `collisions` {}. Linear 0 on all clips. Loops 0 / 0 (idle, walk). Walk slide 0.0. Idle foot drift 0.0. PASS.
- `ground_min_z`: idle 0.000, walk 0.000, roar 0.000, act **-0.017** (f20). PASS, at the edge of -0.02.
- Chest vs spine (max): idle 4.85 (f30), walk 4.03 (f36), roar 3.0, act 4.68 (f57). All <= 5. PASS.
- Head pitch (no Neck bone, head + neck <= 30): roar 15.0, act 14.1. Idle head yaw 13.5 (one slow look). Walk 1.4. PASS.
- Fists (ARMPROBE): idle cycle range **L 0.142, R 0.137** (>= 0.12). Idle f0-f30 travel L 0.133, R 0.033. Closest fist-to-thigh idle 0.067 (L) / 0.066 (R) (>= 0.04). Walk range 0.215 both sides, closest gap 0.057 (>= 0.03).
- Gold at 64 px (kit counter): portrait **49**, game **27** (gates >= 25 / >= 20). PASS.
- Shares, game view (`pack_post_r6.json`): MAUVE 57.8, PLUM 16.6, ICE_W 15.0, JOINT_D 6.7, GOLD 1.9.

## Per-clip scores

| clip | score | one line why | evidence |
|---|---|---|---|
| idle | 8.5 | IDLE-1 numbers all pass (cycle range 0.142 / 0.137, gap 0.066, foot drift 0). The weight shift and the one head look read at 2x. Arm sway is still small at phone size and the breath barely shows. Clears the floor, not by much. | `renders\_beats2x_idle.png`; `_scratch\arm_r6.txt` |
| walk | 8.5 | WALK-1 applied and passes (pelvis 0.035, chest roll 3.5, chest vs spine 4.03, slide 0). In the game row the feet separate and one lifts (f24, f30), and the torso rolls. Still soft at phone size. | `renders\_walk_sheet.png` (game row); `_scratch\ang_r6.txt` |
| roar | 8.5 | ROAR-1 passes on the front sheet: at f27 both fists are at z 1.052 and the out angles mirror. Head 15, jaw open at f27. The mouth is dark grey in the kit render (lead: Studio). The 3/4 tq view still looks uneven at f22, which is perspective. | `renders\_roar_front_sheet.png`; `_roar_jaw_close.png`; `_beats2x_roar.png` |
| act (kneel) | **8.1** | Yaw 30 works: the shin runs off to the side, the sole and heel plate face the game camera, ground -0.017, no collisions. But from the game camera the kneel reads as one thigh column ending in a sideways foot. The forward standing leg is hidden behind the body, and the knee cap on the snow is not visible. Not yet a kneel from behind. | `renders\_kneel_2x_f40_f50.png` (game f40, f50); `_scratch\yaw_cmp_zoom.png`; my crop `%TEMP%\r7_game_f40_low.png` |

## Model score: 8.6 (PASS)

The silhouette and face read well at 1x and in the close sheet. The round 6 blockers are closed. The remaining open items are Studio judgements (mouth darkness, body colour) and small polish points in the TO 9+ list.

## Round 6 items

| item | status | evidence |
|---|---|---|
| **MD-A** chest/waist seam mauve | **PASS** | Side view: one dark seam above the hips (the belt). Front view: chest and waist read as one mass. A light ICE_W belly band still sits under the gold ring (see TO 9+). `_model_sheet.png` (front, side); `_roar_front_sheet.png` f0. |
| **MD-B** icons and close sheet re-made | **PASS** | Strips and close sheet are 09:18, from this build. Gold 49 / 27. The 128 px strip shows two crust masses on each shoulder. The 64 px icon is small, but the gold and the shoulder masses are readable. |
| **ACT-1** kneel yaw 30 | **PARTIAL** | Numbers pass (yaw 30, ground -0.017, collisions none, chest 4.68, ends at rest). Visual: from the game camera the shin is its own limb and the sole faces the camera, but the knee cap on the snow is hidden and the standing leg is not visible. See MUST 1. |
| **IDLE-1** arm sway 7 | **PASS** | Cycle range L 0.142 / R 0.137 (>= 0.12); gap 0.066 (>= 0.04); foot drift 0; chest vs spine 4.85. |
| **WALK-1** pelvis / chest roll | **PASS** | Pelvis 0.035, chest roll 3.5. Chest vs spine 4.03 (target <= 4.5). Slide 0. Game row shows the feet and the torso roll step to step. |
| **ROAR-1** arm asymmetry | **PASS** | Front sheet f27: both fists at z 1.052, out angles equal, symmetric at f22 and f50. Perspective explains the 3/4 unevenness. |
| MC4' roar mouth | Open, Studio (lead ruling) | Kit luma ~81. Not scored. |
| Kneel snow puff | Studio (VFX) | Not scored. |
| ANIM_REFS rule | Not re-checked this round | No new references in round 6; the round 5 PASS carries. |

## New MUSTs (only what blocks 8.5 on a clip)

**MUST 1 (act, ACT-2). Make the kneel legible from the game camera. Blocks act 8.5.**

- What is wrong: in `_kneel_2x_f40_f50` (game f40 and f50) the kneeling leg is one column from the hip to the snow, and the shin and sole run off to the side. The forward standing leg is behind the body from this camera, so no second leg shows. The knee cap on the snow sits behind the thigh and cannot be seen.
- Fix (IK targets only, no new bones):
  1. In the act's standing-foot key (the forward foot that steps 0.30 BU in f0-9 per CLIP_NOTES), add a lateral offset of **0.10 BU** to its planted target, pointing away from the kneeling side. Hold it from f12 to f52 and ease it back with the rest by f62. Keep its z at 0.0 and its yaw as it is.
  2. Only if the knee cap is still hidden in the acceptance render: move the kneeling-knee target **0.06 BU** outward (away from the centreline), then re-run the ground probe.
- Acceptance:
  - Model: at f40 the standing heel plate is at least **0.10 BU** clear of the kneeling thigh's outer face, with no collision.
  - Render: game f40 and f50 at 2x show two separate lower legs, with background visible between them, and a dark knee cap on the snow.
  - Gates unchanged: `ground_min_z` >= -0.02 (act), `collide_where` 0 pairs, chest vs spine <= 5, head + neck <= 30. Idle and walk untouched.

## TO 9+ (not blocking)

- **Model, belly band:** the light ICE_W belly band under the gold ring still divides chest and waist at 1x. Shorten its half-height from 0.036 to about 0.028 BU, or key it to a MAUVE tone, so the chest reads as one mass.
- **Model, eye slits:** the white highlights in the slits read as glints in `_close_sheet`. Darken them toward (200, 220, 236), as round 3 suggested. Still open.
- **Model, lip:** in the side close (`_close_sheet` middle) the mouth lip sits slightly proud of the face front. Pull it from 0.012 to about 0.008 BU so it does not read as poking out.
- **Idle:** a second, smaller head look later in the cycle, and a little more breath at phone size (round 6 TO 9+, still open).
- **Walk:** a larger step lift in the game view. The feet separate now but stay small at phone size.
- **Roar:** judge the mouth in Studio. Check the roar from the game camera before ship, since the 3/4 view still makes the arms look uneven at f22.
- **Act:** after MUST 1, a settle of about 0.04 BU on the knee so the knee cap reads on the snow.

## Notes (not scored)

- `CLIP_NOTES.md` round 4 says "the left foot steps forward 0.30 BU", but round 2 says the RIGHT foot steps forward and the kneel is on the LEFT knee (`Knee_L` anchor). Correct the round 4 line so the next edit moves the right foot.
- The act's ground minimum (-0.017) is at the -0.02 limit. Any offset for MUST 1 must re-run the ground probe.

## Pass / fail checklist

- Silhouette and species at phone size: PASS.
- Face (brows, slits, closed mouth): PASS.
- Gold hero at 64 px (49 portrait / 27 game): PASS.
- Stacked torso bands (MD-A): PASS (belly band in TO 9+).
- Crust at 64 px (MD-B): PASS.
- Tris 7,820 (cap 15k): PASS.
- Collision-free, linear 0, loops closed, idle drift 0, walk slide 0: PASS.
- Ground minimum -0.017 (act): PASS (edge).
- Chest vs spine <= 5 (all clips): PASS.
- Head + neck pitch <= 30: PASS.
- Idle fist range >= 0.12 both sides, gap >= 0.04: PASS.
- Walk readable from behind: PASS.
- Roar arms symmetric at f27 (front): PASS.
- Kneel legible from the game camera: **FAIL** (MUST 1).
- Mouth opening, snow puff, body colour: Studio, not scored.
- ANIM_REFS rule: not re-checked; round 6 PASS carries.
