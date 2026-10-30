# Frostfang Lynx - FINAL 8.5 GATE, round 3 (clips) - 2026-10-28

## Verdict
- **Clips: 8.0 / 10 - FIX** (one MUST, C2: the idle is still too quiet at game distance)
- **Model: not re-scored this round** (PASS at 8.5 in round 2, as the coordinator states).
- Clip-by-clip: act 8.5 (C1 done), roar 8.5, walk 8.0, idle 7.5 (C2 open).

Round 2 was clips 8.0 with C1 (claw fan at game distance) and C2 (idle life) open. C1 is now clearly closed. C2 is only partly closed.

## What I looked at
- Round-3 renders (01:34-01:38): `renders/pclose_game_act_clawflex_50.png`, `pclose_game_idle_26.png`, `pclose_game_idle_62.png`, `pclose_side_act_clawflex_50.png`, `pclose_side_idle_26.png`, `pclose_side_idle_62.png`, `pclose_tq_act_clawflex_50.png`, `_game_r2.png` (three game-camera frames), `_pose_tq_sheet.png`.
- Gates: `_scratch/fullcheck.json` and `gate6.log` (01:37): collision_free true, no collisions, linear 0 in all clips, idle and walk loops 0.0, idle foot drift 0.0, act ground_min_z -0.002 (the worst clip), roar and idle ground minimum -0.0.
- `_scratch/clipmetrics.json`: act neck max 7.36 (limit 8), act chest vs spine 3.35 (limit 5), act head pitch 0.32 (limit 30), act end vs frame 0 = 0.0 (f95 and f96), idle f120 vs f0 = 0.0.
- Source `pets/FrostfangLynx.py`: claws `0.095 x 0.017` (line 273), claw base `CLAWZ 0.042` (line 44), breath `loc z = -0.02 * H_U * rb` (line 439), idle tail sway `sway = 14.0 * sin(2π f / n)` (line 447), act drop 0.10 H (line ~513), claw open -55 (lines ~524-525), toe roll -20 (line ~539), claw events claw1 f48 and claw2 f60 exported (line ~543).
- Convention check: Raiju and ShadePanther drive the head yaw on the Y slot too, so Y is the yaw axis in this kit. The tail sway is therefore a real lateral swing, not a twist.
- Not checked: the spark VFX in Studio (coordinator's pipeline), per-frame PNGs beyond the sheets, the .blend.

---------------------------------------------------------------------------------------------------------------------
## 1. Act: 8.5 (C1 closed)
- **Crouch.** Clearly lower than idle in `pclose_side_act_clawflex_50.png`: the chest drops, the front reads low, the stare is held.
- **Claw fan at game distance.** In `pclose_game_act_clawflex_50.png` the forepaw claws now stand out as separate cyan wedges on both front paws, not just dashes. In `pclose_tq_act_clawflex_50.png` the four claws per paw open into a fan. The round-2 MUST is met at the game camera.
- **Stare.** The 18 deg lock with the tufts flat at -12 deg reads as a hunter's stare.
- **Pose limits.** Neck 7.36, chest vs spine 3.35, head pitch 0.32 (all inside the limits). Paws planted. Ends at rest (f95 and f96 vs frame 0 = 0.0).
- **Still to confirm (not a gate):** the claw1 f48 and claw2 f60 sparks. The events are exported, but the spark VFX is the coordinator's job and is not in the files I can see. Check in Studio that the sparks fire on those frames.

## 2. Roar: 8.5 (unchanged, still the best beat)
Ruff flare, jaw open to the frost fangs, the neck pushes forward. Neck 4.0, chest 2.0, no pitch problems. No change needed.

## 3. Walk: 8.0 (unchanged)
Clean lateral-sequence cat walk, planted feet, slide 0.0, loop closed. Generic rather than a signature (see T1). No change needed for the gate.

## 4. Idle: 7.5 (C2 open)
- **Head look.** Visible in the side frames: the head height and angle differ clearly between f26 and f62 (the +14 / -8 deg look-around). This is the main motion and it reads.
- **Tail sway.** The sway is correct on the yaw axis (14 deg on Tail1, plus 0.6x on Tail2, so the tip reaches about 0.4 studs peak each side). But from the side camera it is hidden by design. In the game-camera frames `pclose_game_idle_26.png` and `_62.png` the tail tip moves only a few pixels between the two frames, even though f26 is near the sway peak and f62 is near zero. At game distance the tail reads as static.
- **Breath.** 0.02H (about 0.14 studs) dipping below rest. It is correct, but it is too small to see from the game camera. The planted feet hold (idle foot drift 0.0).
- **Net:** the idle reads as a look-around and nothing else.

---------------------------------------------------------------------------------------------------------------------
## 5. MUST list (clips: to reach 8.5)

### C2 (idle life visible at game distance)
- Line ~447, the tail sway: `sway=14.0 * math.sin(2 * math.pi * f / n)` becomes `sway=22.0 * math.sin(2 * math.pi * f / n)`. The tip then reaches about 0.6 studs peak, which is visible from the game camera. Keep one cycle per 120 f (it reads as calm). The loop stays closed (sin is 0 at f=0 and f=120).
- Line ~439, the breath: `-0.02 * H_U * rb` becomes `-0.03 * H_U * rb` (about 0.2 studs). Keep the dip below rest so the feet do not drift.
- Re-check: idle foot drift 0.0, collision_free true, loop seam 0.0.
- Pass: `pclose_game_idle_26.png` and `_62.png` differ visibly in the tail tip (a 15-20 px shift at the game-camera scale), and the breath dip is visible on the back line between two idle frames.

**Re-send list for C2:** `pets/FrostfangLynx.py` diff; `renders/pclose_game_idle_26.png`, `pclose_game_idle_62.png`; `renders/pose_tq_idle_26.png`, `idle_62.png`; the new `_scratch/fullcheck.json`.

---------------------------------------------------------------------------------------------------------------------
## 6. TO 9+ list (higher is better; not needed for 8.5)
- **T1 Walk counter-sway.** Make the walk tail counter-swing the hips: the tail sways at about 6 deg (up from 4), opposite phase to the hips. The walk then reads as a cat rather than a generic quad. Line ~468.
- **T2 Idle ear life.** The ear twitch at f70 is 3 deg (line ~TW). Raise it to 8 deg so the ears read as alert, not only the head.
- **T3 Spark check (confirm, not a builder change).** Check in Studio that the ICE sparks fire on claw1 (f48) and claw2 (f60). If they do, the act sells its signature at game distance.

---------------------------------------------------------------------------------------------------------------------
## 7. Pass / fail checklist (clips)

| # | item | result |
|---|---|---|
| 1 | collision_free true | PASS |
| 2 | Linear 0 in every clip | PASS |
| 3 | Loops closed (idle, walk) | PASS (0.0 / 0.0) |
| 4 | ground_min_z >= -0.02 | PASS (act -0.002, others -0.0) |
| 5 | Pose limits: neck <= 8, chest vs spine <= 5, head pitch <= 30 | PASS (7.36 / 3.35 / 0.32) |
| 6 | No head shake, no airborne frames | PASS |
| 7 | Acts in place, end at rest | PASS (f95 and f96 vs f0 = 0.0) |
| 8 | Signature beat readable at game distance (crouch, claw fan) | PASS (C1 closed) |
| 9 | Idle has visible life at game distance | FAIL (C2: tail tip and breath too small) |
| 10 | Walk reads as a cat walk | PASS (generic, T1) |
| 11 | Roar reads as a threat | PASS |
| 12 | ANIM_REFS rule | PASS as recorded in review 4 (not re-verified here) |
| 13 | Claw sparks on claw1 and claw2 | NOT VERIFIED (events exported; VFX is the coordinator's) |

**Scores:** clips 8.0 (FIX: C2). Model not re-scored (PASS at 8.5 from round 2).
