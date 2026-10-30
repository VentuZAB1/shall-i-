**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.**

# Coral Crusher - FINAL GATE round 4 (9+ polish check), 2026-10-28

Both scores hold at the 8.5 floor. The polish landed on the measurable clip items (roll, breath, wave trough) and on N1 (dome clusters). The eye item is still not shown to follow the claw at phone size, so 9+ is not reached yet. Nothing blocks ship at 8.5.

## What I looked at
All seven images opened; none failed to load. All are the newest set (file times):
- `renders/_model_sheet.png` (04:40): tq, front, side, back.
- `renders/close_domeclusters.png` (04:40): dome cluster close-up.
- `renders/_beats2x_idle.png` (04:40): idle f0 / 20 / 45 / 62 / 80 / 110.
- `renders/_act_eyes_roll.png` (04:44): act f0 / 30 / 41 / 53, game and side cameras.
- `renders/_pose_tq_sheet.png` (04:44): 26 beats.
- `renders/_wave_strip.png` (04:44): tq and game, f18-82.
- `CoralCrusher_portrait_alt.png` (04:44): game-camera icon. The face is not in frame here, so the portrait is not scored for the face.

Also opened for the eyes at native size: `renders/pose_tq_act_semaphore_30.png` and `_41.png` (300 px), and `renders/close_front.png` (rest-pose face close-up).

Numbers (read only, no Blender run):
- `_scratch/export_r3.txt` (export 04:43): `tris_body` 12452; `collision_free` true; `ground_min_z` -0.013 in all four clips; linear 0; idle and walk loops 0 / 0; idle foot drift 0; walk slide 0.002, foot_z_var 0.001; events wave1 30, wave2 53, wave3 76, tap1 90, tap2 96 (seconds x 120 match).
- `_scratch/eye_r3.txt` (eye probe, read as data).
- `pets/CoralCrusher.py` source: idle breath line 484; act keys and eye tracks lines 556-599; `check_pairs` lines 371-372 include Claw vs Eye_L / Eye_R, so the claw-to-eye clearance is inside the collision gate.
- `C:\cdimp\CoralCrusher.fbx` is dated 04:43, matching the export.

## Round 3 TO 9+ items

1. **Act eyes readable at phone size: PARTIAL.**
   - Left: tip-angle swing 64.1 (f41) to 44.0 (f30) = **20.1 deg**, which meets the literal target by a hair. Heading swing 72.7 to 34.5 = **38.2 deg**. The left eye turns toward the claw but is still 44 deg off it at the tops, so it never looks at the claw.
   - Right: the literal metric (tip-angle swing >= 20) now reads **0.5 deg** (3.5 to 3.0), because the right eye is locked on the tip at rest (4.6), at the tops (3.0) and at the troughs (3.5). Heading swing 23.7 to 39.3 = **15.6 deg**. That is the same amplitude round 3 had (16.3 deg by the old metric), which round 3 said could not be seen.
   - Verdict on the re-scope: a locked right eye keeps looking at the claw, and I accept that as the design goal. It does not move more, though, so it adds nothing to 9+ on its own. The right eye also lags the drop by 2 f (tip angle 23.4 at f36), as designed.
   - Visible follow: **not shown**. No render resolves the stalks. At 300 px and in the 500 px panels the eyes are a few pixels under the slate brow plates. My estimate from the round-2 stalk length (about 0.43 studs), 5.8 studs per BU and a crab about 14 studs wide: the right tip moves about 0.12 studs (about 1 px on a phone) and the left about 0.28 studs (about 2-3 px). These are estimates, not measurements.
   - So the numbers are real, but the motion is too small to read at phone size. Clip tuning is capped at a few pixels. A readable eye needs a geometry change (stalk or bulb), which is a model item.

2. **Shell roll +/-4: LANDED.** Source line 595: roll = -2u minus 4 per beat (+/-4 with the beat). Shoulder swing (zR minus zL): -0.0625 at the tops, +0.0209 at the troughs = **0.083 BU** (target >= 0.08). Idle foot drift 0, collision_free true. Visibility in stills is not provable (about 0.5 studs of shoulder travel by estimate), the same as round 3.

3. **Idle breath +/-6: LANDED.** Source line 484: breath -6 / +6 / -6 at f45 / f62 / f80 on the same 35 f arc. In `_beats2x_idle` the claw at f62 is clearly higher than at f45 and f80.

4. **Act trough depth: LANDED.** Source: merus trough 16 to 2, wrist trough -40 to 2, tops unchanged (merus 40, wrist -6), trough spread 6. collision_free true, ground -0.013. Tip drop **0.36 BU** (round 3: 0.18, so about 2.1 studs vs 1.0). In `_wave_strip` the troughs at f39 and f62 drop visibly, and in `_act_eyes_roll` f41 the crusher sits low and forward.
   - Caveat: the builder's world-angle numbers (merus 22.6 deg and carpus 19.2 deg above horizontal at f41) are not the same metric as round 3's "about 40 deg above horizontal", so the "toward horizontal" target cannot be checked like-for-like. The tip drop is the number I can verify.

5. **N1 dome clusters taper: LANDED.** `close_domeclusters.png`: the rose spikes are pointed cones on wider dark ROSE_D bases (base 0.060 x scale, was 0.045). They no longer read as straight tubes. Minor: one front-left spike in that close-up reads as a flat fin. Not a must.

## Regressions
**None confirmed.**
- Tris 12,452 (cap 15k). collision_free, ground, loops, slide, idle drift and events all match the stated values.
- Pale underside and walk timing are pending owner sign-off and are not counted.

**Risk to verify (not a confirmed regression):** at the act troughs the crusher is brought in (spread 6) and lowered, so its tip sits almost on the right eye's gaze line (3.5 deg). At 300 px the claw sits beside the crusher-side stalk, not over it, but I could not check pixel overlap.
- Check: a game-camera render with a zoomed crop of the eye box at f38-44 and f60-66.
- If the claw covers the right stalk, test a trough spread step outward (6 to 10) and re-run the gate. Keep it only if `collision_free` stays true and `collide_where` stays 0. If the claw does not cover the stalk, drop this note.

## What is still between this pet and 9+
- **Eye follow visibility (the one remaining point).** Clip-only tuning cannot make a 0.43-stud stalk readable at phone size. It needs a model change to the eye (stalk length or bulb size), then a phone-size check: game camera at 390 px wide, f30 vs f41, with the eye box cropped. A 9+ pass needs the stalk tips to differ by a few visible pixels there. Today they differ by about 1 to 3 px by estimate.
- **Rose fin (model, small).** Replace the flat front-left spike in `close_domeclusters.png` with a cone, the same as the others.
- **Trough angle (verification only).** If the lead wants the "toward horizontal" target checked, the builder should report the merus and palm angle at f39 in round 3's metric.

**Model 8.5 PASS. Clips 8.5 PASS.** Nothing blocks ship at the 8.5 floor. 9+ is the eye follow, which needs geometry.

## Pass / fail checklist (round 4)
| # | check | result |
|---|---|---|
| 1 | N1 dome cluster taper | LANDED |
| 2 | Tris <= 15k | PASS (12,452) |
| 3 | Left eye tip-angle swing >= 20 | PASS (20.1, barely) |
| 4 | Right eye tip-angle swing >= 20 | NOT MET by design (0.5 deg, locked on the tip) |
| 5 | Eyes visibly follow the claw at phone size | NOT SHOWN (about 1-3 px by estimate) |
| 6 | Shell roll shoulder swing >= 0.08 BU | PASS (0.083) |
| 7 | Idle breath +/-6 | PASS (source and beats) |
| 8 | Act trough lower, collision-free | PASS (drop 0.36 BU, collision_free true) |
| 9 | Gate numbers (collision, ground, loops, slide, drift) | PASS |
| 10 | Rest exact f110-120 (eyes 50.9 / 4.6, shoulder 0.0) | PASS |
| 11 | Claw vs eye collision | PASS (in check_pairs) |
| 12 | Walk timing, pale underside | PENDING owner (not counted) |
