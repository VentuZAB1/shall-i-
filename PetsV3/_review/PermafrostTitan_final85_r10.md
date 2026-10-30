# Permafrost Titan - FINAL 8.5 GATE, ROUND 10 (model + clips, renders 2026-10-28 14:01-14:02) - REVISE (act only)

**Verdict: REVISE. Score 8.4/10 (act). Not shippable (floor 8.5). Model 8.6 PASS.**

Per clip: idle 8.5, walk 8.5, roar 8.5, **act (kneel) 8.4**. The clips score is the lowest, so it is **8.4 (act)**.

Summary: round 10 is a real gain. The shin's visible share from the game camera went from 47.8 % to 61.8 % (vertex), the kneeling foot's claws now show at game f40, and the knee lands on the snow at f18 with no bounce and no slide. But the kneeling thigh is still hidden (36 % of it is covered, and its vertex share is 48.7 %, the same as round 8). From the game camera the leg still reads as a bent leg folded back, not as one knee on the snow. The contact is fine; the readability of the leg is not there yet. MUST 1 is the thigh.

## Answer to the owner's question (game camera, phone size)
- **Motion: yes.** Heavy drop (pelvis 0.380), clean touch-down at f18 on `icecrack`, a hold with no bounce and no slide (knee drift 0.010), and a rise that presses into the snow at f57 and lifts at f60.
- **Readability: not yet.** At game f40 the thigh is covered by the left fist, forearm and spine. The shin plate sits on the thigh with no background between them, so "one knee on the snow" does not read. The knee itself is hidden behind the plate and foot from this camera. The puff will mark the contact, but it cannot make the leg read by itself.

## What I looked at
- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round 9 review `_review/PermafrostTitan_final85_r9.md`; builder notes `PermafrostTitan/CLIP_NOTES.md` (FINAL 8.5 ROUND 10 and ROUND 10 sections, plus the round 9 camera-bug note); `_review/VenomBasilisk_review2.md` (format); Obsidian `Creature Animation.md` and `Model Review Checklist.md`; `_review/GLACIER_CONCEPTS.md` OWNER DECISIONS (Permafrost gold chest bezel).
- Renders, all opened: `_kneel_2x_f30_f40_f50.png`, `_kneel_2x_f40_f50.png`, `_kneel_close_f30_f40_f50.png`, `_beats2x_kneel.png`, `_kneel_game_strip_f0_f64.png`, `_kneel_views.png`, `_pose_tq_sheet.png`, `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`. Also the highest-res game frames `hx_game_act_kneelrise_40.png`, `kv_game_act_kneelrise_18.png`, `kv_game_act_kneelrise_58.png`.
- Data (read only): `_scratch/kneel_vis_r10b.json`, `kneel_pix_r10b.json`, `knee_frames_r8.json`, `knee_frames_r10b.json`, `export_r10.txt`, `arm_search_r10b_fixedcam.txt`, `arm_search_r10_fixedcam_r8.txt`, `arm_search_r10_fullgrid.txt`, `cam_check.py`.
- My own checks:
  - JSON compare against the round 8 export (`_scratch/r8_export_files/PermafrostTitan_r8.json`): idle, walk and roar clip data are identical; only `act_kneelrise` changed. Confirmed.
  - Per-frame limb swing: act max 22.1 deg (Shin_R, f7), walk max 14.1 deg. Quaternion sign flips: 0 in all clips. Both pass the 60 deg rule.
  - Gate numbers in `export_r10.txt` and `kneel_vis_r10b.json` match the builder's notes.
- Not done: no pixel tooling (PIL is not installed), so the shin/thigh separation is judged by eye on the 2x and 3x frames. No Studio.

## Per-clip table

| clip | score | one line why | evidence file |
|---|---|---|---|
| idle | 8.5 | Clip data identical to round 8. Weight shift, fist sway and slow head read; the sway is still thin at phone size; chest vs spine 4.85 at f30 is close to the 5 limit. | `renders\pose_tq_idle_*` (14:01), `_beats2x_idle.png` (09:53) |
| walk | 8.5 | Clip data identical to round 8. Feet separate, one lifts, the torso rolls in the game row; soft at phone size; slide 0.0. | `renders\pose_tq_walk_*` (14:01), `wk_game_walk_*` (09:53) |
| roar | 8.5 | Clip data identical to round 8. Both arms level at f27, head lifts, jaw open. Mouth colour is a Studio check (lead ruling). | `renders\pose_tq_roar_*` (14:01), `_roar_front_sheet.png` (09:54) |
| act_kneelrise | **8.4** | Motion clean (f18 touch-down, no bounce, no slide, clean rise). Readability short of the bar: thigh 36 % hidden by the fist, forearm and spine; shin does not separate from the thigh; the knee contact sits behind the plate and foot from the game camera. The 3/4 read is good. | `renders\hx_game_act_kneelrise_40.png`, `kv_game_act_kneelrise_18.png`, `_kneel_2x_f40_f50.png`, `_scratch\kneel_pix_r10b.json` |

## Model: 8.6 (PASS, unchanged)
- Geometry is unchanged from round 8 (act-only change; tris 7,820). The model score carries.
- The silhouette, species, fierce brows and slit eyes, closed mouth, and the gold chest ring at 64 px all read (`_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`).
- The round 9 TO 9+ items are still open (see the table): the light ICE_W band under the gold ring splits the chest; white highlights sit in the eye slits; the lip is slightly proud.

## Round 9 item table

| r9 item | r10 status | evidence |
|---|---|---|
| Act MUST 1 (a): game f40, Shin_L top edge breaks away from Leg_L with background along at least 1/3 of the shin | **FAIL** | No background is visible between the dark shin plate and the thigh block at game f40 (`hx_game_act_kneelrise_40.png`). `kneel_pix_r10b.json`: Shin_L occludes 471 px of Leg_L. |
| Act MUST 1 (a): Foot_L claws visible at game f40 | **PASS** | Dark claws clear at lower right (`hx_game_act_kneelrise_40.png`). Foot_L screen share 77.3 % (`kneel_pix_r10b.json`). |
| Act MUST 1 (b): collide_where 0 for Fore_L/Leg_L, Fist_L/Leg_L, Hand_L/Leg_L over f18-62 | **PASS** | `kneel_vis_r10b.json` `arm_leg_overlap_frames` L [] and R []; `export_r10.txt` collision_free true, collisions {}. |
| Act MUST 1 (c): fist-to-thigh gap >= 0.05, fist centre z < 0.80 | **PASS** | gap 0.137, fist_z 0.459 (`arm_search_r10b_fixedcam.txt`). Note: the fist floats 0.137 BU off the thigh top (see NICE 1). |
| Act MUST 1 (d): knee lowest f18-52 in [-0.017, -0.005]; ground act >= -0.02; collision_free; linear 0; loops 0/0 | **PASS (by lead ruling)** | Knee f18-52 is -0.0030 to -0.0001 (`knee_frames_r10b.json`): on the surface, never above it, no float. The r9 band top (-0.005) is no longer hit, because the knee now touches rather than presses (r8: -0.006 to -0.016). Toes -0.017 (>= -0.02). collision_free true; linear 0; loops 0/0. |
| Act MUST 1 (e): 3/4 f40 read stays | **PASS** | `_kneel_2x_f40_f50.png` (tq f40): kneeling plate and foot, standing claw foot, fist. |
| Act MUST 1 step 3: stop and report if (a) to (d) fail | **Applies** | (a) failed, so see MUST 1 below. The round 10 change was the leg, not the arm; the arm hold was not re-searched with the thigh metric. |
| Act: shin "28.7 %" in r9 notes | **CORRECTED** | The r9 number came from a camera bug (camera at the world origin). The true round 8 value is 47.8 % (`arm_search_r10_fixedcam_r8.txt`, ARMCAM [1.596, 3.495, 4.044] = the game camera). Confirmed. |
| Act: "zero arm parts occlude" (r9 notes) | **INVALID** | Same camera bug. The fixed-camera grid shows arm parts do occlude the shin in some holds (Fore_L 16 px, Hand_L 11 px at out -11 / fwd -6 / bend 0). |
| Act: do not add a further knee settle | **PASS** | No settle added. Knee lands f18 on `icecrack` (0.18), no bounce. |
| Act: Chest vs spine and head (r9 TO 9+ re-measure) | **PASS** | Chest 4.68 (f57) and head 14.11 (f20) from `export_r10.txt`. Limits 5 and 30. |
| Act: standing right shin stub in 3/4 (r9 TO 9+) | **OPEN** | STAND_OUT still 0.10 (pets/PermafrostTitan.py line 79); not re-measured this round. |
| Act: knee sinks / contact reads from the game camera | **FAIL** | The knee sits behind the plate and the foot from this camera, so the contact is not readable without the puff. Judge with the puff (lead ruling), but the leg itself is still not readable (MUST 1). |
| Idle, walk, roar: readable at phone size | **PASS at 8.5 each** | Clip data identical to round 8 (JSON compare). Margins still thin (idle sway, walk step). |
| Idle fist sway (r9 TO 9+) | **OPEN** | Unchanged. |
| Walk step lift at f24-30 (r9 TO 9+) | **OPEN** | Unchanged. |
| Roar mouth colour | **Studio** | Not scored. |
| Model: belly band under the gold ring splits the chest (r9 TO 9+) | **OPEN** | Still visible in `_model_sheet.png` (front). Geometry unchanged. |
| Model: white highlights in the eye slits (r9 TO 9+) | **OPEN** | Still visible in `_close_sheet.png`. |
| Model: lip slightly proud (r9 TO 9+) | **OPEN** | Still visible in `_close_sheet.png` (side). |

## Measured numbers behind the verdict (fixed game camera, f40 unless noted)

| part | vertex share | screen share | occluders (px) |
|---|---|---|---|
| Shin_L | 61.8 (f30 62.5, f50 61.0) | 63.8 | Leg_L 411, Foot_L 331 |
| Foot_L | 48.7 (f50 46.3) | 77.3 | Shin_L 504 |
| Leg_L (thigh) | **48.7 (unchanged from r8)** | **63.6** (alone 13,004 px, visible 8,276) | Shin_L 471, Arm_L 362, Spine 299 |

- The thigh is the part that did not move. Its vertex share is the same as round 8 (48.7 %), and 36 % of it is still covered.
- The shin is in front of the thigh over 471 px, so the knee bends toward the camera and the two overlap; nothing separates them.
- The knee pole is the default `(0, -1, 0)` (blockkit.py line 832), so the bend plane is not chosen for visibility.

## MUST (prioritized, all buildable)

**MUST 1 (act, blocks 8.5). From the game camera at f40, the kneeling thigh must be at least 70 % visible on screen and the shin must separate from it.**
- Lever A, knee pole (act only): in `act_kneelrise` (pets/PermafrostTitan.py lines 532-614), before the Leg_L loop (lines 606-612), set `k.legs2["Leg_L"]["knee"]` (set in blockkit.py line 835; `solve_leg` reads it each call at blockkit.py lines 851-870) to a vector with a sideways component for frames 18-52. Ease it in over f12-18 and out over f52-62. Try x = +0.4 to +0.8 and x = -0.4 to -0.8 (body frame); the probe picks the sign. Restore the default after the loop, so idle and walk are untouched. ankle_to (line 611) pins the ankle, so the contact does not move; re-check the knee band.
- Lever B, left arm (ARM_L, line 555; the hold f30-46 is (-6, 14, 14)): re-run the sweep with the THIGH metric, not only the shin. Try out -6 to +4, fwd 4 to 14, bend 14 to 30. Round 10 only measured the shin.
- Acceptance, measured with the kneel_pix method on the game camera after a depsgraph update, and then checked on 2x and 3x crops:
  a. Leg_L screen share >= 0.70 (now 0.636) and vertex share >= 0.60 (now 0.487).
  b. Shin_L shows background between its top edge and Leg_L along at least 1/3 of its length (2x and 3x crops, f40).
  c. Shin_L screen share stays >= 0.62 and the Foot_L claws stay visible.
  d. Fist-to-thigh gap >= 0.05, fist centre z < 0.80, and collide_where 0 for Fore_L|Leg_L, Fist_L|Leg_L and Hand_L|Leg_L over f18-62.
- If no combination passes (a) to (d), stop and report to the lead. Do not add a knee settle or another DROP change.

**MUST 2 (act, keep the contact as it is). Every trial must keep the knee and the ground numbers.**
- Knee lowest f18-52 stays within -0.003 to +0.001 (now -0.0030 to -0.0001); the knee still lands at f18 (`icecrack` 0.18); no bounce.
- Toes ground >= -0.02; collision_free true; linear 0; idle and walk loops 0/0; walk slide 0; standing foot drift 0; chest vs spine <= 5; head + neck <= 30.
- Re-export and re-run every gate after each trial. Export only if all gates are green.

## NICE (do these too)
1. **Fist rests on the thigh.** The fist sits 0.137 BU off the thigh top (`arm_search_r10b_fixedcam.txt`, gap 0.137). The ARM_L docstring says "on the left thigh". Bring the gap to 0.05-0.08 if MUST 1 allows, so the fist reads as resting, not hanging.
2. **Standing right shin stub (3/4).** Open since round 9. Move Foot_R / Shin_R 0.03-0.05 BU further out in the body frame (STAND_OUT, line 79) and re-check the foot gates.
3. **Model: belly band.** Shorten the light ICE_W band under the gold ring from half-height 0.036 to about 0.028 BU, or key it to a mauve tone (model 8.6 to 9).
4. **Model: eye slits.** Darken the white highlights inside the slits toward RGB (200, 220, 236).
5. **Model: lip.** Pull the lip from 0.012 to about 0.008 BU.
6. **Idle sway.** Raise the fist sway about 10-20 %. The closest fist-to-thigh gap is 0.067, so there is room.
7. **Walk step lift.** A larger lift at f24-30 in the game view.
8. **Idle chest vs spine (4.85 at f30, limit 5).** Keep any idle change within range and re-log.
9. **Next round.** Send the same render set plus a 3x crop of the lower body at game f40 and a thigh-share table. Use the same camera method.

## Pass / fail checklist
- Silhouette and species at phone size: **PASS**.
- Face (brows, slits, closed mouth): **PASS** (white slit highlights still open, NICE 4).
- Gold hero at 64 px: **PASS** (`_icons_strip_64.png`).
- Tris 7,820 (cap 15k): **PASS**.
- Model 8.6: **PASS** (geometry unchanged).
- Idle, walk, roar clip data identical to round 8 (JSON compare): **PASS**.
- Collision-free; linear 0; idle and walk loops 0/0; walk slide 0; foot drift 0 (`export_r10.txt`, `kneel_vis_r10b.json`): **PASS**.
- Act ground >= -0.02 (toes -0.017): **PASS**.
- Per-frame limb swing <= 60 deg and no quaternion sign flips, all clips (act max 22.1 deg, walk max 14.1 deg): **PASS**.
- Chest vs spine <= 5 (act 4.68; idle 4.85, r9 log): **PASS** (idle is thin).
- Head + neck pitch <= 30 (act 14.11): **PASS**.
- Knee lands on the snow at f18 with icecrack, no bounce, no slide: **PASS**.
- Knee on the snow during the hold, no float: **PASS** (lead ruling; -0.0030 to -0.0001).
- Body drop and 30 deg turn read from the game camera: **PASS**.
- Foot claws visible from the game camera at f40: **PASS**.
- 3/4 kneel read: **PASS**.
- Kneeling thigh >= 0.70 screen share from the game camera: **FAIL** (0.636; MUST 1).
- Shin separates from thigh with background at game f40: **FAIL** (MUST 1).
- Knee contact readable from the game camera without the puff: **FAIL** (MUST 1; the puff is a Studio item and is judged with it, per lead ruling).
- ANIM_REFS rule (Plate 356 K3, K8a-c): **PASS** (carried from round 9; `ANIM_REFS.md` not re-opened this round, file time 03:30).
- Mouth colour and the snow-puff VFX: Studio, not scored.
