# Bramble Badger - FINAL 8.5 GATE, ROUND 2 (2026-10-28) - FIX

**Model: 8.0/10. Clips: 8.0/10. Verdict: FIX (both under the 8.5 floor).**

Owner rule: 8.5 is the floor and higher is better. The MUSTs below lift the pet to 8.5+. The TO 9+ items are the next step.

## What I looked at

- Round 1 gate: `_review/BrambleBadger_final85.md`. Builder notes: `BrambleBadger/MODEL_NOTES.md` (round 3) and `CLIP_NOTES.md` (final 8.5 gate).
- Code, read directly: `pets/BrambleBadger.py` (torso lines 74-86, thigh and haunch 156-159, THORNS 36-38, idle 262-276, walk 288-290, roar 315, burrow 357).
- Model renders: `_model_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `crop_side_body.png`, `_body_f85.png`, `low_below.png`.
- Clip renders: `_pose_tq_sheet.png`, `_pclose_tq_sheet.png`, `_pclose_side_sheet.png`, `pclose_side_idle_00`, `_40`, `_43`, `pclose_side_roar_30`, `pclose_side_walk_00`, `_08`.
- Numbers: `_scratch/fullcheck.json`, `_scratch/clipmetrics.json`, `_scratch/export.log`.

## Round 1 items: status

| Item | Status | Evidence |
|---|---|---|
| M1 hind thigh fin | PARTIAL | Narrower (0.072 to 0.060) and lower. A pointed top corner remains at the hip, visible in `pclose_side_walk_08` and `crop_side_body`. See MM1. |
| M2 rump knob | MET | The knob is gone. The rump is flush in `_model_sheet` and the side sheet. |
| M3 back seams | PARTIAL | The back now reads as one line from crest to tail stub in the side sheet. The arch and rear block still show as stacked blocks in `crop_side_body`. See MM2. |
| T1 flank band | MET, subtle | Visible in the side close-up as a faint lower step. At 2.1 % of the game view it is too quiet to read from 5 studs. See TO 9+ T1. |
| T2 crest | MET | The crest is the new signature. It reads at 64 px and 128 px and in `game_view`. |
| C1 idle breathing | MET on numbers | Spine +/-0.010 and Chest 1.2 deg over the whole loop. Not visible at the sheet scale. |
| C2 ear and tail flicks | MET on numbers, too brief | The window is 6 frames (f40 to f46, 0.2 s). See MC1. |
| C3 walk weight | MET | Bob 0.020 and roll 4 deg. The stride reads in `pclose_side_walk_00` and `_08`. |
| T3 growl | MET | `pclose_side_roar_30` against `_idle_00`: the body sits lower, the thorns lie flat, the head drops. |
| T4 dig scoops | MET | The front paws reach further forward and the hind kicks read in the act frames of the side sheet. |
| Underside evidence | NOT MET | `low_below.png` is blank: ground and four grey slivers, no body. See MM3. |

## Numbers (all pass)

- `collision_free` true, collisions {}.
- `ground_min_z` -0.002 in every clip.
- Loops closed (idle f120 vs f0 0.0, walk f30 vs f0 0.0). Linear 0 in every clip. Walk slide 0.0.
- Neck max 7.87 (idle, limit 8).
- Chest vs spine max 2.92 (walk), 2.2 (idle), 1.5 (roar), 1.25 (act). Limit 5.
- Head pitch-up 6.25 (act). Head yaw 2.99 deg per frame (act). Quaternion flips 0.
- Limb swing max 14.2 (armature) and 17.9 (local, Foot_FL scoop). Limit 60.
- Act f99 and f100 vs f0: 0.0. Roar f59 vs f0: 0.21 deg.
- Tris 5,004 (cap 15k).

**Discrepancy to fix:** the round message says chest vs spine 3.35 deg. The JSON says 2.92 (walk) and 2.2 (idle). Quote 2.92. It still passes.

**Shares:** side GREY 32.8 (target 35-40, down from 37.8 because of the new band), MANTLE 13.1, BELLY_D 24.7 (target 15-22, accepted in review 2), GREY_D 4.1, FACE 9.4, AMBER 7.3. Game: GREY 50.4, BELLY_D 15.4, AMBER 14.7. Pass.

---

## Model: 8.0/10

**Gains since round 1:** the crest is now the pet's signature. It reads as a bold amber ridge at 64 px (`_icons_strip_64`), 128 px and in the game view. The rump knob is gone, so the rear profile is clean. The back reads as one line in the side sheet. The white face with its black bands is still the strongest read in the Grass set.

**Still holding it at 8.0:**
1. A pointed top corner remains at the hind thigh. It sticks out about 0.010 units beyond the rear block (the thigh's outer face is at about 0.222; the rear block is at 0.212).
2. The torso reads as stacked blocks. The arch (line 78) and the rear block (line 77) make a visible step on the top, and the grey shoulder seam (line 75) sits under the mantle.
3. The flank band reads as a faint shelf. It does not yet work as a second tone from the game camera.
4. The underside has no valid evidence yet.

## Clips: 8.0/10

**Gains:** the growl hunker reads now. The dig is wider and the kicks read. The walk weight is visible in stride. Breathing runs the full loop. The numbers are clean.

**Still holding it at 8.0:**
1. The ear and tail flicks are 6 frames long (0.2 s at 30 fps). At game distance they are a blip, not a beat.
2. The sniff (f20 to f80) moves only the head and neck. The body is still during the signature beat. The chest breath (1.2 deg) is too small to read.

---

## MUST (lifts the pet to 8.5+)

### Model

**MM1. Hind thigh corner (line 156).** `B.seg(H + Vector((0, 0.0, -0.045)), K, 0.060, 0.080, BELLY_D, leg, ...)`. Change the half-width `0.060` to `0.048`, so the outer face sits at about 0.211 to 0.213, flush with the rear block (0.212). Keep the depth and the start point. Check: a side close-up (`pclose_side_walk_08`) with no point above the grey flank at the hip.

**MM2. Back step on top (lines 77-78).** The arch (line 78, centre y 0.08, half y 0.27) and the rear block (line 77) make a visible step on top. Change the arch to centre y 0.10 and half y 0.20, so it spans y -0.10 to 0.30 and its ends sit inside the spine and rear blocks. Keep its top at z 0.553 (the thorns sit on it). Check: `crop_side_body` shows one continuous back line with no seam at the rear block.

**MM3. Underside evidence.** `renders/low_below.png` is blank. Re-render from below: the camera at about z 0.20 (below the belly, about 0.3 units above the ground), front-left, about 3/4, aimed at the belly, the skirt and the legs. The frame must show the body. Send it with the result. Without it, "nothing floats from below" stays unverified.

### Clips

**MC1. Ear and tail flicks: make them readable (line 264 and lines 274-276).**
- Replace `FLICK` with `[(0, 0.0), (40, 0.0), (46, 1.0), (52, 0.0), (96, 0.0), (102, 1.0), (108, 0.0), (120, 0.0)]`. That is a 12-frame flick with its peak at f46 and f102.
- Ear amplitude on line 274: `10.0 * fk` becomes `16.0 * fk`.
- Tail on line 276: keep `14.0 * fk`.
- Check: frames 40, 46 and 52 in `pclose_side_idle`. The loop stays closed, since f120 ends at 0.

**MC2. Body life in the sniff (line 268).** `rot=(4.0 * d, 0, 0)` on Spine becomes `rot=(4.0 * d, 0, 1.5 * yw / 8.0)`. The spine rolls 1.5 deg with each nose sweep, so the body moves with the head. Check: chest vs spine stays at or below 5, and quaternion flips stay at 0.

**MC3. Evidence after MC1 and MC2.** Re-run `headless_full` and `clipmetrics`. Required: `collision_free` true, `ground_min_z` at or above -0.02, linear 0, loops closed, neck at or below 8, chest vs spine at or below 5, head yaw at or below 3 deg per frame, quaternion flips 0. Send 2x crops of idle f40 and f46 (ears) and f99 and f102 (tail). Quote chest vs spine as 2.92 (walk).

---

## TO 9+ (highest impact, after the MUSTs)

**T1. Flank band readable (model).** Line 85: the band half-height `0.0175` becomes `0.024`, so the band spans z 0.309 to 0.357. Keep GREY_D (150, 146, 156). Check: `game_view` shows two tones on the flank.

**T2. One tapered torso (model).** Replace the stacked blocks on lines 76-78 with one tapered grey seg from y -0.26 to 0.36. Use `top=(0.95, 0.90)`, `rnd=0.45`, and keep the top z at 0.553, so the thorn bases still sit on it. This removes the step read that remains after MM2. Check: `crop_side_body` shows a single back. Only do this if MM2 does not fully clear the seam.

---

## Pass / fail checklist

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Reads as a badger at 64 px | PASS | Crest and face read clearly |
| 2 | Reads at 128 px | PASS | |
| 3 | Distinct from the Grass set | PASS | |
| 4 | Fierce face | PASS | |
| 5 | No stuck-on parts | FAIL | MM1 (hip corner) |
| 6 | Torso reads as one form | FAIL | MM2, T2 |
| 7 | Palette and accent | PASS | Crest is the brightest Grass accent |
| 8 | Flank band / toy risk | PARTIAL | T1 |
| 9 | Tris | PASS | 5,004 |
| 10 | Underside checked | FAIL | MM3 |
| 11 | Clip: loops, ground, pose limits | PASS | |
| 12 | Clip: no head shakes | PASS | |
| 13 | Clip: idle reads alive | PARTIAL | MC1, MC2 |
| 14 | Clip: walk weight | PASS | |
| 15 | Clip: roar readable | PASS | |
| 16 | Clip: act readable | PASS | |
| 17 | Animation refs cited | PASS | Carried over from round 1 |

## Next step

1. Builder applies MM1 to MM3 and MC1 to MC3, and sends the listed frames and the corrected chest-vs-spine number.
2. Builder adds T1 and T2 if time allows. T2 is only needed if MM2 does not clear the seam.
3. The gate closes at 8.5+ when the MUSTs are in. The TO 9+ list is the goal for the next pass.
