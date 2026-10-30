# Frostfang Lynx - FINAL 8.5 GATE, round 4 (model + clips) - 2026-10-28

**Model: 8.5/10 - PASS. Clips: 8.0/10 - FIX.**

Clips score = the floor of the four clip scores (owner rule: a floor, not an average). Idle 8.5, act 8.5, roar 8.5, walk 8.0. The walk is the one clip below the bar, and its one fix is a visible walk tail counter-sway (MUST W1).

## What I looked at
- Brief: `_review/GLACIER_REVIEWER_BRIEF.md`. Round 3: `_review/FrostfangLynx_final85_r3.md`. Builder notes: `FrostfangLynx/CLIP_NOTES.md` (round 3 section).
- Numbers: `_scratch/fullcheck.json`, `_scratch/clipmetrics.json`, `_scratch/fc_r3.txt`, `_scratch/gate6.log`, `_scratch/export.log`.
- Source: diff of `_scratch/FrostfangLynx_f85r2c.py` (round 2) vs `_scratch/FrostfangLynx_f85r3.py` (round 3). Only 4 animation lines changed (breath, ear twitch, idle tail sway, walk tail sway). The model section (everything before the animation marker, line 374) has 0 changed lines.
- Helper: `pk.wave` in `_tools/petkit_backup_20261008.py` = `sin(2*pi*(cycles*f/n + phase))`, so the walk tail phase 0.5 is exactly `-sin`, opposite the hip yaw.
- Images opened (`FrostfangLynx/renders/` unless noted):
  - `_idle_game_r3.png` (game camera, f0 / f26 / f62 / f70; top 1x, bottom 2x)
  - `pclose_game_idle_26.png`, `pclose_game_idle_62.png` (2x)
  - `_scratch/r3/game1x_62.png`, `game1x_70.png` (1x single frames)
  - `pose_tq_idle_26.png`, `pose_tq_idle_62.png`
  - `_breath_side_r3.png` (fixed side camera, red line = f0 back)
  - `_walk_tail_r3.png` (game camera f0 / f6 / f12 / f18)
  - `pclose_game_walk_06.png`, `pclose_game_walk_18.png` (2x)
  - `_model_sheet.png` (4 views)
- Not re-opened this round: `_close_sheet.png`, icon strips, flat palette renders. The model geometry is unchanged from round 2 (diff above), so the model score is carried from round 2 after a check of the sheet.
- Tail and ear distances are estimated by eye on the displayed images (about +/- 10 px at 2x). I did not run any measurement tool.
- Not verified here: the ICE sparks on claw1 f48 / claw2 f60 (lead's Studio check, not counted). ANIM_REFS rule (recorded in review 4, not re-verified).

## Round-3 items
| Item | Result | Evidence |
|---|---|---|
| C2 idle tail visible at game distance | PASS | `pclose_game_idle_26` vs `_62` (2x): the black tip moves about 50-60 px (centre about (530,480) to (480,512)). `_idle_game_r3` top row (1x): about 20 px. Reads calm, one slow 120 f cycle, not busy. Round-3 target 15-20 px at 1x is met. |
| C2 breath visible on back line | PASS (side camera) | `_breath_side_r3.png`: at f60 the back sits visibly below the red f0 line (16 px of 800, builder number confirmed by eye). Feet stay planted (idle foot drift 0.0). At game camera the breath is nearly invisible: see polish P2. |
| C2 numbers (collision, loop seam, foot drift) | PASS | `fullcheck.json`: collision_free true, idle loop 0.0 / 0.0, idle foot drift 0.0, linear 0 in all clips, ground idle -0.0, walk -0.0, roar -0.0, act -0.002. |
| T1 walk tail counter-sway (6 deg, opposite hips) | FAIL (visible), data PASS | Data: `6*wave(f,n,0.5)` = exact opposite of the hip yaw `1.8*wave(f,n)`. Visible: `pclose_game_walk_06` vs `_18` (2x) show the black tail tip at essentially the same screen spot (under about 5 px by eye). `_walk_tail_r3` shows the same. The CLIP_NOTES claim of 23 px f6-f18 is not reproduced. See MUST W1. |
| T2 ear twitch 8 deg at f70 | PARTIAL (data PASS) | Data: Ear_L +8, Ear_R -4.8 at f70, rebound -4 at f72 (correct). Visible: `game1x_62` vs `game1x_70` ears look alike at 1x. Not legible at game distance. See polish P1. |
| T3 spark check | Not counted | Lead's Studio job. Events unchanged (claw1 f48, claw2 f60, snow_flick f77). |
| Act / roar (no change this round) | PASS (8.5 each) | Unchanged source. Act neck 7.36 (limit 8), chest vs spine 3.35 (limit 5), head pitch 0.32 (limit 30). Roar neck 4.0, chest 2.0. Claw fan and crouch still read in `pclose_game_act_clawflex_50`. |

## Clip scores (round 4)
- **Idle: 8.5.** The head look-around, the 22 deg tail sway and the breath all read. The one weak spot is the ear twitch (P1) and the breath at game distance (P2).
- **Act: 8.5.** Unchanged, and the round-3 review already passed it.
- **Roar: 8.5.** Unchanged.
- **Walk: 8.0.** A clean lateral-sequence cat walk with planted feet, loop closed (0.0 / 0.0), slide 0.0. Its only signature is the tail counter-sway, and that does not show from the game camera. Walk stays at 8.0 until W1 is met.

Pose limits and sanity (all from `clipmetrics.json`): neck max idle 5.63, walk 2.03, roar 4.0, act 7.36 (all <= 8). Chest vs spine idle 1.44, walk 2.68, roar 2.0, act 3.35 (all <= 5). Head pitch-up max 1.32 idle, 0.55 walk, 0.0 roar, 0.32 act (all <= 30). Head yaw rate max 1.83 deg/f (idle), 3.26 (act), no head shakes. Quaternion flips 0 in every clip. Tris 8,396 (<= 15k). No airborne frames (ground min >= -0.002).

## Model: 8.5/10 - PASS (unchanged from round 2)
- Round 3 changed no model geometry (source diff: 0 changed lines before the animation marker).
- `_model_sheet.png` still shows the fierce read: narrow ice-cyan slit eyes under dark brows, frost fangs, snow-white muzzle and cheek ruff, dark rosette spots on a pale-silver body, studded blocks, ice-tipped ears.
- Frost-silver coat colour is a lead ruling and is not counted against the score.

## MUST (blocks 8.5)

**W1. Walk tail counter-sway must read at game camera (clips floor = walk 8.0).**
- Evidence: `renders/pclose_game_walk_06.png` and `_18.png` (2x) and `_walk_tail_r3.png` show the tail tip at essentially the same screen spot, under about 5 px by eye. CLIP_NOTES claims 23 px; I could not reproduce that.
- Cause: the hip yaw runs in opposite phase to the tail (Spine yaw +1.8 at f6 and -1.8 at f18, tail -6 and +6). The tail's world yaw therefore swings only about -4.2 to +4.2 (8.4 deg in total). The idle's world swing is about 24 deg (f26 +21.5 to f62 -2.3), which gave about 26 px at 1x.
- Fix: in `walk()` (the `bobtail(...)` line, about line 468 of `FrostfangLynx_f85r3.py`, i.e. the `pets/FrostfangLynx.py` walk section), change `sway=6.0 * pk.wave(f, n, 0.5)` to `sway=12.0 * pk.wave(f, n, 0.5)`. Keep phase 0.5 (opposite the hips) and keep the Spine yaw at 1.8. Expected world swing about 20 deg, close to the idle's 24 deg.
- If 12 deg still shows under 15 px, the swing is mostly toward and away from the rear camera. Then add a Z-roll counter-sway (+/-6 deg on Tail1, +/-3.6 deg on Tail2, phase 0.5). That needs a roll argument on `bobtail()`.
- Pass: the tail tip moves at least 15 px between f6 and f18 at 1x game camera (at least 30 px in the 2x `pclose_game_walk` pair), as a visible sideways swing. Re-run the gate: collision_free true, walk loop 0.0 / 0.0, walk slide 0.0, linear 0, quaternion flips 0. Correct the CLIP_NOTES 23 px claim to the measured value.
- Re-send list: `pets/FrostfangLynx.py` diff, `renders/pclose_game_walk_06.png` and `_18.png`, `_walk_tail_r3.png` (new), new `_scratch/fullcheck.json`.

No other MUST. Idle, act and roar pass.

## TO 9+ (not needed for 8.5)
- **P1. Ear twitch legibility (T2).** At 1x, f62 and f70 ears look alike. Raise the twitch from 8 deg to 12 deg at the idle `tw = 8.0 * tab(TW, f)` line (about line 444), keep `pr = -0.6 * tw`. Pass: the ear tips visibly differ between f62 and f70 at 2x.
- **P2. Breath at game distance.** The 16 px dip is clear from the side camera but nearly invisible from the game camera. Option: raise the Spine breath from 0.03H to 0.04H (`-0.04 * H_U * rb`, about 0.28 studs at 5.9 studs per unit). Keep idle foot drift at 0.0. Optional, since the side camera already passes.
- **P3. Stale comment (housekeeping).** Line 438 of `FrostfangLynx_f85r3.py` still says "breathing rise 0..0.01H". The code is a 0.03H dip. Update the comment.
- **P4. Walk signature.** After W1, the walk's only signature is the tail counter-sway. If a 9+ walk is wanted, a second readable beat (for example a slight head bob that lines up with the foot contacts) would help. Not required for 8.5.

## Pass / fail checklist (round 4)
| # | Item | Result |
|---|---|---|
| 1 | collision_free true | PASS |
| 2 | Linear 0 in every clip | PASS |
| 3 | Loops closed (idle, walk) | PASS (0.0 / 0.0) |
| 4 | ground_min_z >= -0.02 | PASS (act -0.002, others -0.0) |
| 5 | Pose limits (neck <= 8, chest vs spine <= 5, head pitch <= 30) | PASS |
| 6 | No head shake, no airborne frames | PASS |
| 7 | Acts in place, end at rest | PASS (f95 and f96 vs f0 = 0.0) |
| 8 | Signature beat readable at game distance (act crouch, claw fan) | PASS |
| 9 | Idle has visible life at game distance (tail, breath, head) | PASS |
| 10 | Walk reads as a cat walk | PASS (generic) |
| 11 | Walk counter-sway visible at game distance | FAIL (W1) |
| 12 | Roar reads as a threat | PASS |
| 13 | Ear twitch legible at game distance | PARTIAL (P1) |
| 14 | Model unchanged and still fierce | PASS (8.5) |
| 15 | Claw sparks on claw1 f48 / claw2 f60 | NOT COUNTED (lead's Studio check) |
