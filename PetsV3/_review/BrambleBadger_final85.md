# Bramble Badger - FINAL 8.5 GATE (2026-10-28) - FIX

**Model: 7.5/10. Clips: 7.5/10. Verdict: FIX (both under the 8.5 floor).**

Owner rule (2026-10-28): 8.5 is the floor and higher is better. The MUST list lifts the pet to 8.5+. The TO 9+ list is the next step.

## What I looked at

- Plan `_review/BrambleBadger_plan.md` (v2). Brief `_review/GLACIER_REVIEWER_BRIEF.md`.
- Earlier reviews: `BrambleBadger_review1.md` to `review4.md`. Review 4 signed off the clips at 8/10 on numbers. This gate judges what the eye sees.
- Builder notes: `BrambleBadger/MODEL_NOTES.md`, `CLIP_NOTES.md`, `ANIM_REFS.md`.
- Code, read directly: `pets/BrambleBadger.py` (model lines 71-154, `idle` 249, `walk` 275, `roar` 294, `burrow` 322).
- Renders: `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `flat_side.png`, `flat_game.png`, `game_view.png`, `pclose_side_idle_00`, `pclose_side_walk_08`, `pclose_side_act_burrow_44`, `_pose_tq_sheet.png` (18 frames), `_pclose_side_sheet.png` (14), `_pclose_tq_sheet.png` (14), `_roar_vs_idle_side.png`.
- Numbers: `BrambleBadger/_scratch/fullcheck.json`, `_scratch/clipmetrics.json`.
- Comparisons: `_ALL_FIERCE_progress.png`.

Units: HEIGHT 6.5 studs = 0.58 model units, so 1 unit = 11.2 studs. 0.010 units = 0.11 studs.

## Model: 7.5/10

**Strengths (kept):**
- The badger reads at 64 px and 128 px. It is the clearest animal in the Grass strip, and it is distinct from Stag, Mossback, Treant, Basilisk and Mantis.
- The white wedge face with two black bands and amber slits is fierce and reads grumpy at game distance.
- The amber crest is the only warm accent in Grass, and the in-game palette holds (`flat_game.png`).
- Tris 4,956 against the 15k cap.

**Drags (why it is not 8.5 yet):**
1. The rump has a stuck-on box. The haunch block (lines 153-154) sits 0.043 units proud of the rear block at the rump, about 7 % of HEIGHT. Every side frame shows it.
2. The hind thigh (line 151) ends in a pointed dark fin above the rear leg. It reads as a spike, not a thigh.
3. The torso reads as stacked blocks. The side view shows seams at the rear block (line 76) and a step down to the rump.
4. The back is one light grey tone over 38 % of the side view. From the game camera it reads as a flat grey toy, which is the owner's past rejection.
5. The crest is small: 0.056-0.058 units, about 10 % of HEIGHT. It is correct for the plan, but it is not the Raiju-level silhouette the owner loved.

## Clips: 7.5/10

**Passes:** every clip is in place, closed, and at rest at the end. The head stays within the pose limits (neck max 7.87 deg, chest vs spine max 2.92, head pitch-up 6.25, head yaw 2.99 deg per frame, no quaternion flips). Ground minimum is -0.002. The roar reads in `_roar_vs_idle_side.png`: the body drops, the thorns lie flat, the ears go back and the jaw opens. The act reads as a tap, three scoops and two kicks, and the look-around is no longer a shake.

**Drags:**
1. The idle is nearly still apart from the head. Breathing is 0.002 units (0.02 studs), which is invisible. Breathing is also gated off while the head is down, so the 60-frame sniff is dead still in the body. The ears only follow the head (line 267). The tail is 4 deg and static.
2. The walk weight shift is small: the body bob is 0.010 units (0.11 studs) and the roll is 3 deg. In `pclose_side_walk_08` the body barely moves between steps.
3. The dig scoops are small at game distance: forward reach is 0.040-0.048 units (about 0.5 studs). The dig depends on the VFX to read.
4. Animation refs: 1 of 4 cited clips is from animationreference.org (the walk). The other three are Sakugabooru, after the site had no matching tags. The builder recorded the search. This follows the 2026-10-14 spider precedent, so it passes with a note.

---

## MUST (lifts the pet to 8.5+)

### Model (7.5 to 8.5+)

**M1. Hind thigh fin (line 151).** `B.seg(H + Vector((0, 0.02, -0.012)), K, 0.072, 0.088, BELLY_D, leg, bot=(0.9, 1), top=(0.80, 0.74), ext=0.0, ext1=0.03)` (the `fb == "B"` branch). The taper narrows the top into a point above the skirt. Direction: change to `top=(0.95, 0.95)` and add `rnd=0.45`. Check: the side close-up (`pclose_side_idle_00`) shows a rounded thigh, with nothing peaking above the skirt line.

**M2. Rump box knob (lines 153-154).** `B.add(H + Vector((s * 0.022, 0.025, -0.035)), (0.068, 0.110, 0.075), GREY, "Spine", ...)`. H.x is s x 0.165, so the block centre is at s x 0.187 and its outer face at s x 0.255. The rear block (line 76) is at 0.212, so the knob sits 0.043 units proud. Direction: drop the x offset (`s * 0.022` becomes `0`) and change the half x from 0.068 to 0.050. The outer face then sits at 0.215, flush with the rear block within 0.003. Keep y and z. Check: the side frame shows no box at the rump.

**M3. Back seams (lines 75-77).** The back is three blocks: the spine seg (line 75, top (0.95, 0.97)), the rear block (line 76, top (0.78, 0.70), rnd 0.42) and the arch (line 77). The rear block steps down toward the rump. Direction: on line 76 change `top=(0.78, 0.70)` to `top=(0.95, 0.95)` and `rnd=0.42` to `rnd=0.50`, so its top runs level with line 75. Check: one back line runs from the crest to the tail stub in the side close-up.

### Clips (7.5 to 8.5+)

**C1. Idle breathing (lines 261-263).** Line 261: `b = pk.wave(f, n, 0, 3) * (1 - d)` becomes `b = pk.wave(f, n, 0, 3)`, so breathing continues during the sniff. Line 262: `+ 0.002 * b` becomes `+ 0.010 * b` (0.11 studs). Line 263: Chest `rot=(1.0 * d, 0, 0)` becomes `rot=(1.0 * d + 1.2 * b, 0, 0)`. Check: the chest top visibly rises at f0 and f40 in the side frames, and the neck stays at or below 8 deg.

**C2. Idle ear and tail life (lines 267-269).** Line 267 sets the ears from the head only. Add a flick: `ears(k, f, -4.0 * d + 3.0 * lf + 10.0 * flick(f))`, where `flick` is a `tab` through `[(40, 0), (43, 1), (46, 0), (96, 0), (99, 1), (102, 0)]`. On line 269, add a 14 deg flick to the Tail1 pitch on the same frames. Check: the ears and tail move at f43 and f99 in `pclose_side_idle` frames, and the idle loop still closes.

**C3. Walk weight shift (lines 282-283).** `loc=(0, 0, -0.010 * bob)` becomes `-0.020 * bob` (0.22 studs, 3.4 % of HEIGHT). On line 282, the roll `3.0 * pk.wave(f, n)` becomes `4.0 * pk.wave(f, n)`. Check: `pose_tq_walk` frames 0, 8, 15 and 23 show the bob, and the walk loop stays at 0.

**C4. Evidence after C1-C3.** Re-run `headless_full` and `clipmetrics`. Required: `collision_free` true, `ground_min_z` at or above -0.02, linear 0, idle and walk loops closed, neck at or below 8, chest vs spine at or below 5, head yaw at or below 3 deg per frame. Send: side frames of idle f0, f40 and f100, and walk f0 and f8. For the model, send one side close-up after M1-M3. No full model round is needed if these render clean.

---

## TO 9+ (highest impact, after the MUSTs)

**T1. Break the flat grey back (model).** Add a GREY_D (150, 146, 156) flank band on both sides, 0.035 units tall at z 0.315 to 0.350, y -0.26 to 0.27. Use the `edge_band` style with 0.003 proud. This gives the body a second read in the game camera and removes the "grey plastic toy" risk.

**T2. Bigger crest signature (model).** In `THORNS` (lines 35-37), change the five middle thorns from 0.056-0.058 to 0.072 and the two shoulder thorns to 0.064. On line 126 (the `B.spike` call in the thorn loop), change the thorn width from 0.056 to 0.064. The crest then reads at 64 px from the game camera. This ends at about 12 % of HEIGHT, above the plan's 8-10 %. The owner must approve the plan change.

**T3. Stronger growl (clip).** In `roar()`, line 308, raise the tremble `tr` from 1.5 to 2.5 deg. Its window (f24 to f42) stays the same. This makes the growl read as a snarl at 5 studs. Check that the head yaw rate stays at or below 3 deg per frame.

**T4. Wider dig scoops (clip).** On line 350, change the `SC` reach from `-0.040` and `-0.048` to `-0.056` and `-0.064`, so each paw sweep is about 0.7 studs. Keep the lift at 0.026 (under 0.05H). Re-check `collision_free` and `ground_min_z` at or above -0.02.

---

## Pass / fail checklist

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Reads as a badger at 64 px | PASS | Strongest Grass icon |
| 2 | Distinct from the Grass set | PASS | |
| 3 | Fierce face | PASS | Bands and slits read grumpy |
| 4 | No stuck-on parts | FAIL | M2 rump knob, M1 thigh fin |
| 5 | Torso reads as one form | FAIL | M3 seams |
| 6 | Palette in game colours | PASS | Accent reads strong |
| 7 | Accent strength | PASS | Amber is the only warm Grass accent |
| 8 | Flat back / toy risk | FAIL | T1 for 9+ |
| 9 | Tris | PASS | 4,956 against 15k |
| 10 | Clip: loops, ground, pose limits | PASS | Numbers from review 4 hold |
| 11 | Clip: no head shakes | PASS | Look-around is 3.0 deg per frame |
| 12 | Clip: idle reads alive | FAIL | C1, C2 |
| 13 | Clip: walk weight | FAIL (minor) | C3 |
| 14 | Clip: roar readable | PASS | T3 for 9+ |
| 15 | Clip: act readable | PASS | T4 for 9+ |
| 16 | Animation refs cited | PASS | With note on the Sakugabooru route |

## Next step

1. Builder applies M1-M3 and C1-C3, then sends the evidence in C4.
2. Builder adds T1-T4 if time allows. T2 needs the owner's plan approval first.
3. The gate closes at 8.5+ on the MUST list. The 9+ list is the goal for the next pass.
