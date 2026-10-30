# Coral Crusher - FINAL GATE round 3 (8.5 bar), 2026-10-28

**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.**

Both sides are at the bar. All three round-2 clip MUSTs are met (CM-R2-1, CM-R2-2 on the numbers, CM-R2-3), and the model
did not change. No MUST blocks 8.5. The walk timing (CM-R2-4) and the pale underside (MM2) stay pending owner calls, which the
brief says are not counted. The TO 9+ list below is where the remaining points are.

## What I looked at
All images opened; none failed to load.
- **Newest clip set (03:47-03:48):** `renders/_walk_sway_claw.png`, `_walk_sway_strip.png`, `_wave_strip.png` (tq and game,
  f18-82), `_pose_tq_sheet.png` (26 beats), `pose_tq_idle_45 / 62 / 80.png`, `pose_tq_act_semaphore_30 / 41.png`,
  `wv_game_act_semaphore_30 / 36 / 40 / 42.png`, `ws_game_walk_*` (walk f0-27).
- **Portrait:** `CoralCrusher_portrait_alt.png` (03:48, game-camera render). Reads well: crusher up, fierce face, studded shell.
- **Model:** `renders/_model_sheet.png` (01:43). The geometry is unchanged since the round 2 model (tris 12,644 in
  `_scratch/gate_f85.json` and the r2 export; no model change in MODEL_NOTES r2).
- **Stale file:** `renders/_act_eyes_roll.png` is dated 01:46, before the round 2 eye change (see process flags). I used it only
  for the face look, not as round 2 evidence.
- **Numbers:** `_scratch/gate_f85.json` (03:49), `_scratch/eye_r2.txt`, `_scratch/export_r2.txt`, CLIP_NOTES round 2 section,
  ANIM_REFS and the lead ruling on CM3. The FBX `C:\cdimp\CoralCrusher.fbx` is dated 03:48:15, after the 03:47 clip renders,
  so it matches the round 2 state. Timestamp check only; I did not open the FBX.
- **My own silhouette checks** (read-only, nothing written): each frame was thresholded (orange or near-black pixels) and
  the masks were compared by IoU. Results are cited under the items below.

## Round 2 items

| # | item | verdict | evidence |
|---|---|---|---|
| CM-R2-1 | Idle breath readable (guard was ±3 deg, now ±5) | **PASS** | Troughs f45 / f80, peak f62, same 35 f arc. Silhouette at 300 px: f45 to f62 IoU 0.80, f62 to f80 0.81, f45 to f80 0.97 (returns to the same pose). For scale, the guard lift from rest (f20 to f45) is IoU 0.87, so the breath is about the size of the lift. In `pose_tq_idle_62` the claw tip sits visibly higher than in `_45` and `_80`. |
| CM-R2-2 | Act secondary motion reads (both eyes track, shell roll) | **PASS on the numbers; visibility PARTIAL** | Eyes (`eye_r2.txt`): right eye tip-angle 21.5 deg at the troughs (f41 / f64) to 5.2 deg at the tops (f30 / f53 / f76) = **16.3 deg**; left 71.8 to 56.8 = **15.0 deg**. Both >= 10. Yaw is right 20, left -12. Roll: shoulder dip (zR minus zL) -0.052 at the tops, +0.010 at the troughs, so +/-3 deg about -2. Rest exact: f110 eyes 50.9 / 4.6, shoulder 0.0, `pose_tq_act_semaphore_110` = rest. collision_free true. Idle foot drift 0. I could not see the eye or roll change in the 300 px stills. In motion they should show: the eye stalk (about 0.43 studs) moves about 0.12 studs over 16 deg, and the 0.062 BU shoulder swing is about 0.36 studs. Not provable from stills, so it goes in the TO 9+ list. |
| CM-R2-3 | Walk claw sway visible (6 deg) | **PASS** | `_walk_sway_claw.png` (crusher crop, fixed reference line): the tip moves about 20 px in the crop from f0 to f9 and back by f12-18. Visible against the line. Walk slide 0.002, unchanged. |
| CM-R2-4 | Walk timing: owner sign-off or a site clip | **PENDING OWNER** (not counted, per lead ruling) | ANIM_REFS: animationreference.org has no crab tag; timing comes from the Wikimedia C1 footage by lead ruling. |

**Act wave (new check, game camera):** the signature beat reads from the game camera. Silhouette top (f30) to trough (f40 /
f42) IoU 0.65 (about 2,900 px changed of about 6,600); top to top (f30 to f50) IoU 0.98. My first look at the 220 px frames
suggested a smaller change. The masks say the wave is clear.

**Gate numbers (as reported, consistent with the r2 notes):** collision_free true; ground_min_z -0.013 in all four clips;
linear 0; idle and walk loops 0 / 0; idle foot drift 0; walk slide 0.002, foot_z_var 0.001. Events: wave1 30, wave2 53,
wave3 76, tap1 90, tap2 96; roar clacks 22 / 30 / 38. Roar unchanged (`pose_tq_roar_14 / 22 / 38`), reads fine. No head
shakes and no airborne moves.

## Model: 8.5/10 - PASS (no regression, no gain)
- **MM2, pale underside:** accepted by lead ruling (1.6 % side, 2.2 % game, 5.6 % back). The cream lip shows at the rear in
  `_model_sheet` (side and back). Not counted. Owner written sign-off still pending.
- **N1 (round 2 NICE, not applied):** the dome rose clusters still read as straight pink tubes in `_model_sheet` (tq) and in
  the tq close-up. Taper them (see TO 9+ 5).
- **Face:** slit eyes under heavy brow plates, fanged W mouth, no smile, no googly eyes. Reads fierce.
- **Tris 12,644** (cap 15k). PASS.

## MUST list (blocking 8.5)
None. Both scores are at the bar.

## TO 9+ (polish, measurable)
1. **Act eyes readable at phone size.** Raise the eye track so each eye's tip-angle swing is >= 20 deg (now R 16.3, L 15.0):
   right yaw 20 to 26, left -12 to -16 in `act_semaphore`. Re-probe with `_scratch/eye_probe.py`. Keep rest exact at f110
   (eyes 50.9 / 4.6).
2. **Shell roll.** Raise the roll from +/-3 to +/-4 deg so the shoulder swing (zR minus zL) goes from 0.062 BU to at least
   0.08 BU (tops about -0.07). Keep collision_free true and idle foot drift 0.
3. **Idle breath at 64 px.** Raise the guard breath from +/-5 to +/-6 deg (same 35 f arc, troughs f45 / f80, peak f62). The
   f70 tap stays.
4. **Act trough depth.** The tq trough (f41 / f62) still holds the claw about 40 deg above horizontal. Lower it toward
   horizontal-forward only if `collide_where` stays 0 (CLIP_NOTES: at a merus below ~16 deg the carpus cut into the front rim).
5. **Model N1 (carry-over).** Taper the two dome rose clusters (scale 1.30 / 1.20 at (0.075, 0.075) and (-0.085, 0.02)): wider
   ROSE_D base, pointed ROSE tip, as in round 2 N1.

## Process flags (not scored)
- `renders/_act_eyes_roll.png` is stale (01:46, before round 2). Re-render the act eye and roll sheet at the r2 state (game
  camera, f0 / f30 / f41 / f53) so the eye and roll evidence matches the export.
- Owner written sign-off still needed: walk timing (CM-R2-4) and the pale underside (MM2).
- The FBX (`C:\cdimp\CoralCrusher.fbx`, 03:48:15) matches the r2 state by timestamp. Re-export only if clip keys change.

## Pass / fail checklist (round 3)
| # | check | result |
|---|---|---|
| 1 | CM-R2-1 idle breath +/-5 readable | PASS |
| 2 | CM-R2-2 eye track >= 10 deg, both eyes | PASS (16.3 R / 15.0 L) |
| 3 | CM-R2-2 shell roll +/-3 | PASS on numbers; PARTIAL visibility in stills |
| 4 | CM-R2-3 walk claw sway visible | PASS |
| 5 | CM-R2-4 walk timing | PENDING OWNER (not counted) |
| 6 | Act rest exact f110-120 | PASS |
| 7 | Gate numbers (collision_free, ground, loops, slide) | PASS |
| 8 | Wave readable from the game camera | PASS (top to trough IoU 0.65) |
| 9 | Model regression | none (geometry unchanged, tris 12,644) |
| 10 | MM2 pale underside | ACCEPTED by lead ruling (not counted); owner sign-off pending |
| 11 | Tris <= 15k | PASS |

**Model 8.5/10 - PASS. Clips 8.5/10 - PASS.** Send to the owner with: the walk-timing and pale-underside sign-offs, and the
TO 9+ items if the owner wants 9+ before shipping.
