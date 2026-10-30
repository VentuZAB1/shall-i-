# Permafrost Titan - FINAL 8.5 GATE, ROUND 11 (model + clips, renders 2026-10-28 14:23-14:24) - APPROVED AT THE FLOOR (8.5), conditional on the Knee_L snow puff

**Verdict: APPROVED. Score 8.5/10 (act, idle, walk, roar). Model 8.6 PASS.**
The clips score is the LOWEST per-clip score: **8.5 (idle, walk, roar, act all 8.5).** This meets the 8.5 floor with no margin.

One condition for the act score: the Knee_L snow puff at f18 (`icecrack`, 0.18) must be in Studio. Without it the knee contact cannot be read from the game camera, and I would score act 8.4 again (the r10 read).

Per clip: idle 8.5, walk 8.5, roar 8.5, act_kneelrise 8.5. (No fly / takeoff / land clips.)

Summary: round 11 fixes the thing r10 was missing. The kneeling thigh is now clear of the hanging upper arm: Leg_L screen share at f40 is **0.759** (r10 0.636, r8 0.591), and only 12 px of Arm_L cover it (r10 362 px). Every number that the brief set as a gate passes, except MUST 1(b), which the lead has waived. The motion is unchanged and clean: a heavy drop, touch-down at f18 with no bounce, a hold with no slide, and a forward-leaning rise. The new arm pose reads as bracing, not as an odd reach.

## Answer to the owner's question (game camera, phone size)
- **Motion: yes.** The body drops (pelvis 0.380) and turns 30 deg. The knee touches down at f18 on `icecrack`, the hold has no bounce and no slide (knee -0.0030 to -0.0001, drift 0.010), and the rise leans forward at f50-58 and lifts at f60. Heavy and clean at phone size (`_kneel_game_strip_f0_f64.png`, `_beats2x_kneel.png`).
- **Thigh: yes now.** 0.759 screen share at f40 (0.761 at f50), 0.637 vertex share. The thigh now reads as a leg, not a folded block.
- **One knee on the snow: partly, and it needs the puff.** From the game camera the shin plate sits in front of the thigh with no background between them (waived, see below). The drop, the bent leg and the foot claws carry the read. The puff at Knee_L marks the contact.
- **Arm pose: natural.** Both fists brace forward over the raised right knee. The left arm is straight and the right elbow is bent 32 deg, a deliberate asymmetry that fits the mirrored kneel. At phone size it reads as bracing, not as a stiff reach (`_scratch/r11/_arm_cmp_f40.png`, `_kneel_views.png`).

## What I looked at
- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; previous round `_review/PermafrostTitan_final85_r10.md`; builder notes `PermafrostTitan/CLIP_NOTES.md` (section "FINAL 8.5 ROUND 11"); `ANIM_REFS.md` (Plate 356 K2, K3, K8a).
- Code: `pets/PermafrostTitan.py` `act_kneelrise` (lines 532-619): DROP 521 (0.380), STAND_OUT 79 (0.10), KNEE_OUT 80 (0.06), ARM_L 560 (f18 (1,24,12); f30-46 (4,32,0); f53 (4,28,10)), KNEEL_ANKLE 593, L/R tables 596-600, events 619. Only the ARM_L table changed. The file matches the notes.
- Renders, all opened: `_kneel_2x_f30_f40_f50.png`, `_kneel_2x_f40_f50.png`, `_kneel_3x_game_f30_f40_f50.png`, `_kneel_close_f30_f40_f50.png`, `_beats2x_kneel.png`, `_kneel_game_strip_f0_f64.png`, `_kneel_views.png`, `_pose_tq_sheet.png` (all 24 beats: idle, walk, roar, act), `_scratch/r11/_arm_cmp_f40.png`, `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `flat_tq.png`, `flat_game.png`, `flat_side.png`, `_ALL_FIERCE_progress.png`.
  - The model and icon sheets are the round-8 renders (09:53-09:54). The geometry has not changed since round 8 (see the model section).
  - The idle, walk and roar beats are judged from `_pose_tq_sheet.png` and the JSON compare. The older `_walk_sheet.png`, `_roar_front_sheet.png` and `_beats2x_idle.png` were not reopened: their clip data is byte-identical to the r10 and r8 exports.
- Data (read only):
  - `_scratch/thigh_probe_r11_f40.json`: Leg_L 0.759 screen / 0.637 vert at f40; occluders Shin_L 1,884 px, Spine 1,240 px, Arm_L 12 px; arm gap 0.326; fist z 0.52; `gap_px` 0 (no background in the hip-knee-ankle triangle).
  - `_scratch/kneel_vis_r11.json`: Leg_L 0.637 / 0.637 / 0.600 at f30 / f40 / f50; Shin_L 0.625 / 0.618 / 0.610; Foot_L 0.487 / 0.487 / 0.463; arm-leg overlap L [] and R []; Chest 4.68 (f57); Head 14.11 (f20).
  - `_scratch/knee_frames_r11.json`: knee band f18-52 -0.0030 to -0.0001; touch-down f18; toes -0.0172 (f18-52); rise to -0.014 at f57, lift at f60.
  - `_scratch/export_r11.txt`: collision_free true, collisions {}; loops 0 / 0; walk slide 0; linear 0; act ground -0.017; idle, walk, roar ground 0.0; tris 7,820; events icecrack 0.18, core1 0.30, core2 0.44 (unchanged).
  - `_scratch/r11_arm.txt`, `r11_arm2.txt`, `r11_pole.txt`, `r11_ko.txt`, `r11_yaw_armfwd.txt`: the sweeps behind the chosen hold and the rejected pole and ankle options.
- My own checks:
  - **JSON diff r10 vs r11:** only `act_kneelrise` `rot/Arm_L` and `rot/Fore_L` changed. Idle, walk, roar and all events are identical.
  - **JSON diff r8 vs r11:** the act clip only, as expected.
  - **Lua diff r10 vs r11:** lines 74-75 only, the act Arm_L and Fore_L rows.
  - **Per-frame rotation (60 deg rule):** idle 1.23 deg, walk 14.09 deg (Shin_R f24), roar 3.22 deg, act 22.09 deg (Shin_R f8). Quaternion sign flips: 0 in every clip.
  - **Thigh-metric sweep (r11_arm2.txt):** a straight arm at 32 deg forward is the smallest hold that clears the thigh to >= 0.75. Fwd 14 or less gives 0.69 at best, so the choice is sound.
  - **Knee-pole sweep (r11_pole.txt):** the pole moves the knee 6-8 cm per 20 deg; the best thigh (+20 deg, 0.679) lifts the knee off the snow. Rejection accepted.
  - **Ankle sweep (r11_ko.txt):** KNEE_OUT 0.06 is the only value that keeps the knee on the band (-0.003 to -0.0001); 0.00 digs the knee 5 cm in, 0.12 floats it 5 cm. Accepted.
- Not done: no Studio, no Blender runs. The screen-share and occlusion figures are the builder's pixel probes, which I checked against the stored JSON and the images, not re-ran.

## Per-clip table

| clip | score | one line why | evidence file |
|---|---|---|---|
| idle | 8.5 | Clip data identical to r10 and r8 (JSON). Weight shift, fist sway and slow head read; the sway is thin at phone size; chest vs spine 4.85 at f30 (limit 5). | `renders/pose_tq_sheet.png` (idle beats), `_scratch/export_r11.txt` |
| walk | 8.5 | Clip data identical to r10 and r8. Feet separate, one lifts, the torso rolls; soft at phone size; slide 0, loop 0 / 0. | `renders/pose_tq_sheet.png` (walk beats) |
| roar | 8.5 | Clip data identical to r10 and r8. Both arms level at f27, head lifts, jaw open. Mouth colour is a Studio check (lead ruling). | `renders/pose_tq_sheet.png` (roar beats) |
| act_kneelrise | **8.5** | Motion clean: drop, f18 touch-down, no bounce, no slide, forward-lean rise. Thigh 0.759 (was 0.636): the arm no longer hides it. Shin 0.638 and foot claws hold. The one-knee read is inferred from the drop and the foot, and needs the puff. Background between shin and thigh is waived. | `_kneel_2x_f40_f50.png`, `_kneel_3x_game_f30_f40_f50.png`, `_beats2x_kneel.png`, `_kneel_game_strip_f0_f64.png`, `thigh_probe_r11_f40.json` |

Lowest per-clip score: **8.5** (idle, walk, roar, act tie). Clips score = 8.5.

## Model: 8.6 (PASS, unchanged)
- Geometry is unchanged from round 8. Tris 7,820 (cap 15,000). The model lua differs from round 10 only in the act Arm_L and Fore_L rows.
- The silhouette, species, fierce brows and slit eyes, closed mouth, and the gold chest ring all read at 64 px (`_icons_strip_64.png`, first icon). The palette matches the plan (`flat_tq.png`, `flat_game.png`).
- Round 9 TO 9+ items are still open (see the r10 table). They carry the 8.6.

## r10 item table

| r10 item | r11 status | evidence |
|---|---|---|
| Act MUST 1 (a): Leg_L screen >= 0.70 at game f40 | **PASS** | 0.759 at f40, 0.761 at f50 (`thigh_probe_r11_f40.json`, `r11_arm2.txt`) |
| Act MUST 1 (b): background between Shin_L and Leg_L along >= 1/3 of the shin | **WAIVED (lead ruling)** | 0 background px in the hip-knee-ankle triangle (`gap_px` 0). Yaw 45 gives 24 px but Leg_L vert falls to 0.487 and the arm covers the thigh again (`r11_yaw_armfwd.txt`). Judge on what the camera can show, as the lead ruled. |
| Act MUST 1 (c): Shin_L screen >= 0.62 and foot claws visible | **PASS** | Shin_L 0.638 screen (0.618 vert); claws visible in the 2x and 3x crops |
| Act MUST 1 (d): fist gap >= 0.05, fist centre z < 0.80, collide 0 for Fore/Fist/Hand vs Leg over f18-62 | **PASS** | gap 0.326, fist z 0.52, `arm_leg_overlap_frames` L [] R []; collisions {} |
| Act MUST 1 lever A (knee pole) | **Rejected, accepted** | knee moves 6-8 cm per 20 deg; the best thigh (0.679) lifts the knee off the snow (`r11_pole.txt`) |
| Act MUST 1 lever B (left arm, thigh metric) | **DONE** | sweep `r11_arm.txt`, `r11_arm2.txt`; chosen hold (4, 32, 0) |
| Act MUST 2: knee f18-52 in -0.003 to +0.001, touch-down f18, no bounce | **PASS** | -0.0030 to -0.0001; touch-down f18 (`icecrack`); xy drift 0.010 |
| Act MUST 2: toes >= -0.02, collision-free, linear 0, loops 0 / 0, walk slide 0, standing foot drift 0, chest <= 5, head + neck <= 30 | **PASS** | toes -0.017; collision_free true; linear 0; loops 0 / 0; slide 0; Foot_R drift 0.0; chest 4.68; head 14.11 |
| NICE 1: fist rests on the thigh (gap 0.05-0.08) | **Superseded** | The gap is now 0.326 because the fist braces forward over the raised knee. The builder documents the conflict with MUST 1; accepted. |
| NICE 2: standing right shin stub in 3/4 (STAND_OUT 0.10, line 79) | **OPEN** | Not changed in r11 (`pets/PermafrostTitan.py` line 79) |
| NICE 3: model belly band under the gold ring | **OPEN** | Still visible in the front model sheet |
| NICE 4: white highlights inside the eye slits | **OPEN** | Still visible in `_close_sheet.png` |
| NICE 5: lip slightly proud | **OPEN** | Still visible in `_close_sheet.png` (side) |
| NICE 6: idle fist sway +10-20 % | **OPEN** | Idle data unchanged |
| NICE 7: walk step lift at f24-30 | **OPEN** | Walk data unchanged |
| NICE 8: idle chest vs spine (4.85, limit 5) | **OPEN (in range)** | Idle data unchanged |
| NICE 9: next-round render set with 3x crop and thigh table | **DONE** | `_kneel_3x_game_f30_f40_f50.png`, thigh table below |

Thigh and shin table (game camera, f40; r8 / r10 / r11):

| part | r8 | r10 | r11 |
|---|---|---|---|
| Leg_L thigh, screen / vert | 0.591 / 0.487 | 0.636 / 0.487 | **0.759 / 0.637** |
| Shin_L, screen / vert | 0.585 / 0.478 | 0.638 / 0.618 | 0.638 / 0.618 |
| Foot_L, screen / vert | 0.706 / 0.500 | 0.773 / 0.487 | 0.773 / 0.487 |
| Arm_L px over the thigh (f40) | 1,450 | 362 | **12** |

## MUST (before ship; none on the model or clips)
The model and clip gates pass. Two Studio items remain and are required before ship:

1. **Studio: the Knee_L snow puff at f18** (`icecrack`, 0.18). Lead ruling: committed. The act score of 8.5 assumes the puff is there, as the brief asks. Without it, act is 8.4.
2. **Studio: colour check** of the whole pet (lead ruling, not scored here) and the roar mouth colour.

## NICE (optional for 9+; each is buildable)
1. **Model, belly band:** shorten the light ICE_W band under the gold ring from half-height 0.036 to about 0.028 BU, or key it to a mauve tone. Model 8.6 to about 9.
2. **Model, eye slits:** darken the white highlights inside the slits to about RGB (200, 220, 236).
3. **Model, lip:** pull the lip from 0.012 to about 0.008 BU.
4. **Standing right shin stub (3/4):** move Foot_R / Shin_R about 0.03-0.05 BU further out in the body frame (`STAND_OUT`, line 79), then re-check the foot gates.
5. **Idle and walk:** raise the idle fist sway 10-20 % (gap 0.067 gives room); lift the walk step at f24-30 in the game view. Re-log chest vs spine (idle 4.85, limit 5) after any idle change.
6. **Knee read without the puff:** if the owner wants the knee visible without the puff, the next lever is a shin-plate tone change (a lighter or mauve shin plate), not more arm or leg moves. Only if the puff is not enough.

## Pass / fail checklist
- Silhouette and species at phone size: **PASS**.
- Face (brows, slits, closed mouth): **PASS** (white slit highlights still open, NICE 2).
- Gold hero at 64 px: **PASS** (`_icons_strip_64.png`).
- Tris 7,820 (cap 15k): **PASS**.
- Model 8.6: **PASS** (geometry unchanged).
- Idle, walk, roar clip data identical to round 10 and round 8 (JSON diff): **PASS**.
- Only the act Arm_L and Fore_L changed (r10 to r11 JSON and lua diffs): **PASS**.
- Collision-free; linear 0; idle and walk loops 0 / 0; walk slide 0; standing foot drift 0 (`export_r11.txt`, `kneel_vis_r11.json`): **PASS**.
- Act ground >= -0.02 (toes -0.017): **PASS**.
- Per-frame limb swing <= 60 deg and no quaternion sign flips, all clips (act 22.09 deg, walk 14.09 deg): **PASS**.
- Chest vs spine <= 5 (act 4.68; idle 4.85): **PASS** (idle is thin).
- Head + neck pitch <= 30 (act 14.11): **PASS**.
- Knee lands on the snow at f18 with `icecrack`, no bounce, no slide: **PASS**.
- Knee on the snow during the hold, no float (-0.0030 to -0.0001): **PASS**.
- Body drop and 30 deg turn read from the game camera: **PASS**.
- Foot claws visible from the game camera at f40: **PASS**.
- 3/4 kneel read: **PASS**.
- Kneeling thigh >= 0.70 screen share from the game camera (0.759): **PASS**.
- Shin separates from thigh with background at game f40: **WAIVED** (lead ruling; 0 px is geometrically impossible at yaw 30).
- Knee contact readable from the game camera without the puff: **CONDITIONAL** (the puff is a Studio item; judged with it).
- New arm pose reads as a natural titan kneel, not an odd pose: **PASS**.
- ANIM_REFS rule (Plate 356 K3 forward-lean rise, K8a settle): **PASS** (spine pitch 10 at f58 with a forward lean; settle 0.005 at f20).
- Mouth colour, colour, and the snow-puff VFX: Studio, not scored.
