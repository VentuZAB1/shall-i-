# Bramble Badger - FINAL 8.5 GATE, ROUND 3 (2026-10-28) - FIX (clips)

**Model: 8.5/10 (PASS, at the floor). Clips: 8.3/10 (FIX, under the floor). Overall: FIX.**

Owner rule: 8.5 is the floor and higher is better. The clip MUSTs below lift the clips to 8.5+. The TO 9+ items are the next step.

## What I looked at

- Round 2 gate: `_review/BrambleBadger_final85_r2.md`. Builder notes: `BrambleBadger/MODEL_NOTES.md` (round 4) and `CLIP_NOTES.md` (round 2).
- Code, read directly: `pets/BrambleBadger.py` (torso and `body_hull` lines 96-137, THORNS 36-38, mantle line 135, thigh line 216, idle 325-336, sniff Spine line 329, Chest line 330).
- Model renders: `_body_r2.png`, `_model_sheet.png`, `low_below.png`, `game_view.png`, `_icons_strip_64.png`, `_icons_strip_128.png`.
- Clip renders: `_flick_2x.png`, `_pclose_side_sheet.png`, `pclose_side_idle_00` and `_act_burrow_99` (rest match), `_pose_tq_sheet.png` (not re-viewed; unchanged except the flicks and sniff roll).
- Numbers: `_scratch/fullcheck.json`, `_scratch/clipmetrics.json`, `_scratch/export.log` (01:30 export).

## Round 2 items: status

| Item | Status | Evidence |
|---|---|---|
| MM1 hind thigh corner | MET | Half-width 0.048 (line 216). No point at the hip in the side sheet. |
| MM2 back step | MET | The spine, rear block and arch are one lofted body (`body_hull`). No seam in `_body_r2` or the side sheet. |
| MM3 underside evidence | MET | `low_below.png` now shows the belly, skirt, legs and claws from the low front-left. Nothing floats. |
| T1 flank band | MET | Curved strip, half-height 0.024. Visible as a lower step in `_body_r2`. Subtle at 2.8 % game (see TO 9+). |
| T2 one tapered torso | MET | The top is level (0.540 to 0.553 to 0.535). The thorns sit on it. |
| MC1 flicks | MET | 12 frames, peaks at f46 and f102. In `_flick_2x` the ear turns and the tail moves visibly at 2x. |
| MC2 sniff roll | MET on numbers | Spine rolls 1.5 deg with the sweeps (line 329). It is subtle at game size. See MC2. |
| MC3 evidence | MET | Numbers below; chest vs spine quoted as 2.92 (walk, from the JSON). |

## Numbers (all pass)

- `collision_free` true, collisions {}. `ground_min_z` -0.002 in every clip.
- Loops closed (idle f120 vs f0 0.0). Linear 0 in every clip. Walk slide 0.0, foot_z_var 0.0.
- Neck max 7.87 (idle, limit 8).
- Chest vs spine max 2.92 (walk), 2.2 (idle), 1.5 (roar), 1.25 (act). Limit 5.
- Head pitch-up 6.25 (act). Head yaw 2.99 deg per frame (act). Quaternion flips 0 (keys and sampled).
- Limb swing max 14.2 (armature) and 17.85 (local, Foot_FL scoop). Limit 60.
- Act f99 and f100 vs f0: 0.0. `pclose_side_act_burrow_99` matches `pclose_side_idle_00`. Roar f59 vs f0: 0.21 deg.
- Tris 6,832 (cap 15k; the plan said 5-8k, so this is inside it).

---

## Model: 8.5/10 (PASS)

**Gains since round 2:** the body is one form, which removes the stacked-block read. The rump rounds off cleanly. The hind thigh no longer has a spike. The crest sits on a smooth top and reads as a bold amber ridge at 64 px, 128 px and in the game view. The underside is now checked and shows nothing floating. The white head with its black bands still gives the strongest badger read in the Grass set.

**Why it is at the floor, not above it:** the back is a plain capsule. Its only features are the crest, the mantle front, the flank band and the stud skin. The shoulders do not stand up over the back line, so the front is not as heavy as a real badger's. That is the main thing between 8.5 and 9 (TO 9+ T1).

## Clips: 8.3/10 (FIX)

**Gains since round 2:** the flicks are now a visible beat (12 frames, 16 deg ear, 14 deg tail). The sniff now moves the body with the head. Breathing runs all loop. The dig, the growl and the walk all still read, and every gate passes.

**Still holding it at 8.3:** the idle is still a small-motion clip at phone size.
1. Breathing: 0.010 units on the Spine (0.11 studs) and 1.2 deg on the Chest. That is about 3 to 4 pixels on a phone.
2. The sniff roll: 1.5 deg on the Spine. The head moves 15 to 20 deg, but the body only moves a fraction of that.
3. The crest bristle at f70 is 3 deg. It is hard to see.
4. The ear twitch is the one visible idle beat. The rest of the idle reads as a head bob with a tiny body.

---

## MUST (lifts the clips to 8.5+)

**MC1. Breathing you can see (line 329 and line 330).**
- Line 329: the Spine loc `-0.010 * d + 0.010 * b` becomes `-0.010 * d + 0.014 * b` (0.16 studs at HEIGHT 6.5).
- Line 330: the Chest rot `1.0 * d + 1.2 * b` becomes `1.0 * d + 1.8 * b`.
- Check: the chest top rises on `pclose_side_idle_00` against `_40`, with the neck at or below 8 deg.

**MC2. Sniff body roll (line 329).** `rot=(4.0 * d, 0, 1.5 * yw / 8.0)` becomes `rot=(4.0 * d, 0, 2.5 * yw / 8.0)`. The body now leans 2.5 deg into each nose sweep. Check: chest vs spine stays at or below 5, and quaternion flips stay at 0.

**MC3. Crest bristle (line 336).** `thorns(k, f, 3.0 * br)` becomes `thorns(k, f, 5.0 * br)`. The crest lifts 5 deg at f70 and settles. Check: the thorn bases stay buried in the hull at f70 (no gaps at the rear thorns), and the idle loop still closes.

**MC4. Evidence after MC1-MC3.** Re-run `headless_full` and `clipmetrics`. Required: `collision_free` true, `ground_min_z` at or above -0.02, linear 0, loops closed, neck at or below 8, chest vs spine at or below 5, head yaw at or below 3 deg per frame, quaternion flips 0. Send a 2x crop of idle f0 and f40 (breathing and sniff roll), and of f70 (the crest).

---

## TO 9+ (highest impact, after the MUSTs)

**T1. Shoulder hump (model).** Raise the front of the back so the shoulders stand over the line, as a real badger's do. Changes:
- Line 135, the mantle block: centre z 0.42 becomes 0.44, and half z 0.12 becomes 0.135. The top then sits at 0.575 (0.035 above the hull at the shoulders).
- THORNS, the first two entries (lines 36-37): z 0.515 becomes 0.550 and z 0.535 becomes 0.570, so the front thorns still sit on the top.
- Check: a side close-up of the shoulders and neck. The neck block must not step up, and the front thorns must stay seated.

**T2. Ear twitch at each sniff sweep (clip).** Add a 6-deg ear flick, 6 frames long, at each yaw peak (f36, f52, f68). That gives the idle a visible beat on every nose sweep, not just once. The ears are already keyed in `ears(...)` on line 335.

---

## Pass / fail checklist

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Reads as a badger at 64 px | PASS | The crest and the white head read |
| 2 | Reads at 128 px | PASS | |
| 3 | Distinct from the Grass set | PASS | |
| 4 | Fierce face | PASS | |
| 5 | No stuck-on parts | PASS | The thigh and rump are clean |
| 6 | Torso reads as one form | PASS | `body_hull` |
| 7 | Palette and accent | PASS | Game AMBER 16.4 %, GREY 48.6 % |
| 8 | Flank band / toy risk | PASS | Subtle; TO 9+ T1 for the shoulders |
| 9 | Underside checked | PASS | `low_below.png` |
| 10 | Tris | PASS | 6,832 (cap 15k) |
| 11 | Clip: loops, ground, pose limits | PASS | |
| 12 | Clip: no head shakes | PASS | Head yaw 2.99 deg per frame |
| 13 | Clip: flicks read | PASS | `_flick_2x` |
| 14 | Clip: idle body life | FAIL | MC1-MC3 |
| 15 | Clip: walk | PASS | |
| 16 | Clip: roar readable | PASS | |
| 17 | Clip: act readable | PASS | |
| 18 | Animation refs cited | PASS | Carried over from round 1 |

## Next step

1. Builder applies MC1 to MC3 and sends the MC4 evidence.
2. Builder adds T1 and T2 if time allows.
3. The clip gate closes at 8.5+ when MC1 to MC4 are in. The model is at the floor and passes now. The TO 9+ list is the goal for the next pass.
