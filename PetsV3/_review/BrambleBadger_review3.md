# Bramble Badger - clip gate review 3 (2026-10-27) - APPROVED WITH FIXES (clips)

**Score: 7/10** for a 40 % starter (ship target 8/10).

The numeric gates are clean: collision-free, no linear drift, closed loops, zero walk slide, and the lowest point sits
at -0.012 (limit -0.02). The pose limits hold, and the four references are cited. Two beats do not yet read at game
distance. The roar's hunker is too small, and the act's opening repeats the idle sniff. One head sweep is quick enough to
read as a shake. Three edits, plus a few numbers, will fix all of it. The builder then sends the changed frames, and I sign
off without another full round.

## What I looked at

- `BrambleBadger/CLIP_NOTES.md`, `BrambleBadger/ANIM_REFS.md`, `BrambleBadger/_scratch/fullcheck.json`.
- Sheets: `renders/_pose_tq_sheet.png` (18 frames), `_pclose_side_sheet.png` (14), `_pclose_tq_sheet.png` (14).
- Single frames: `pclose_side_idle_00`, `pclose_side_idle_36`, `pclose_side_roar_12`, `pclose_side_roar_30`,
  `pclose_side_act_burrow_25`, `pclose_side_act_burrow_54`, and `_scratch/roar_vs_idle.png`.
- Code: `pets/BrambleBadger.py` (`idle`, `walk`, `roar`, `burrow`), read directly.
- Rules: `_review/GLACIER_REVIEWER_BRIEF.md` (clip gate), `Creature Animation.md`, and `_review/ANIM_REFERENCES_1014.md`
  (for the precedent on a missing animationreference.org subject).

## Numeric gates (fullcheck.json)

| Gate | Result | Status |
|---|---|---|
| collision_free | true, collisions {} | PASS |
| linear (all clips) | 0 | PASS |
| Loops (idle, walk) | loop_pos 0, loop_rot 0 | PASS |
| Walk slide and foot_z_var | 0.0 | PASS |
| Idle foot drift | 0.0 | PASS |
| ground_min_z | idle -0.002, walk -0.002, roar -0.002, act -0.012 (f54) | PASS (limit -0.02) |
| Tris | 4,956 (cap 15k) | PASS |
| Events | growl f30; dig1 26, dig2 36, dig3 46, kick1 54, kick2 60 | PASS (prefixes ok, no `end`) |
| Pose: neck | at most 8 deg (idle and act 8 x d) | PASS, at the limit |
| Pose: head + neck pitch-up | code gives about 6.3 (head -4.25, neck -2.0 at DN -0.25); message says 8, notes say limit 6 | PASS, numbers to reconcile |
| Pose: chest vs spine | code gives about 3 in idle and act (Spine 4 d vs Chest 1 d), more in f50-62; notes say 1.5, message says 2 | PASS, numbers to reconcile |
| No airborne spins | none | PASS |
| Act in place | act_burrow linear 0 | PASS |
| Haunch (review 2 N-3) | moved to Spine (line 154) | PASS |
| Brow and socket (review 2 M-1) | seated in the band (lines 95, 105) | PASS |

## Animation references (the owner rule)

Four references are cited: A (The Pointer, idle), B (Pluto and the Gopher, roar), C (Once Upon a Forest, act), and D
(Dragon Walk Cycle, walk, from animationreference.org per `ANIM_REFERENCES_1014.md`). The builder searched
animationreference.org first, found no sniff, dig or quadruped tags, and used Sakugabooru for A to C. The spider
precedent (2026-10-14) accepted the same route, with the search documented. **PASS with note.**

## Beats at game distance

**Idle, nose-down sniff: PASS.** `pclose_side_idle_36` shows the snout at the grass, and the body stays still. The yaw
sweeps are +8, -8, +5 over 15-20 f each, which is not a shake.

**Walk: PASS on numbers.** Slide 0, foot_z_var 0, stride 0.30. The walk sheet shows a diagonal-pair trot.

**Roar, hunker growl: FAIL on readability (see M-1).** The head is level and forward with the jaw open (`roar_vs_idle`,
panel 2). That is the accepted deviation and it does differ from the idle. But the hunker is not there. The body line in
`pclose_side_roar_12` and `_30` is the same as in `pclose_side_idle_00`. The code sets the drop to `0.05 * H_U`, about
0.029 units (5 % of HEIGHT), and that is too small to read at game distance.

**Act, dig the burrow: FAIL on the opening (see M-2).** The first 14 f drop the head 17 deg (`DN` 0 to 1), with a 6 deg
yaw sweep at f12. The idle drop is 15 deg with the same sweep. The act's opening is the idle sniff again, so the act
does not read as its own beat until the scoops start. The scoop lift (0.026, 4.5 % of HEIGHT) is within the 5 % limit.
The nose reaches the spot, and the dig reads from the VFX.

**Act, kicks: NICE.** The hind kick is 0.045 back and 0.030 up. In `pclose_side_act_burrow_54` the hind feet are close
to planted, so the kick is small at this distance (see N-3).

---

## MUST

**M-1. Roar: the hunker must read at game distance.** (`pets/BrambleBadger.py`, `roar()`)
- Built: `drop = 0.05 * H_U` (about 0.029 units, 5 % of HEIGHT). The thorns flatten `-15 * TH` and the ears go back
  `-22 * TH`. The body line at f12 and f30 is indistinguishable from the idle.
- Direction: set `drop = 0.10 * H_U` (about 0.058 units, 10 %), keeping the rump lag of 3 f. Flatten the thorns `-22` and
  the ears `-28` at the hold. Keep the head level, the jaw at 24 deg, and the timing.
- Check: `pclose_side_roar_30` against `pclose_side_idle_00`. The body top must drop visibly at the hold.

**M-2. Act: the opening repeats the idle sniff.** (`burrow()`, the `DN` and `YW` keys and the `paw()` start times)
- Built: `DN` ramps to 1.0 by f14 (head 17 deg down, neck 8). `YW` has a 6 deg sweep at f12. The forepaw scoops start at
  f18 (`paw(f, 18, SC)`). The first 18 f therefore read as the idle sniff.
- Direction: reduce the opening to a quick nose-tap. `DN` peaks at 0.45 (head about 8 deg, neck about 4), and the tap
  lasts f0-8. Remove the f12 yaw. Start the first scoop at f8 (`paw(f, 8, SC)`, not f18), so the act opens with the paw. The
  idle keeps the long sniff.
- The dig events (26, 36, 46) and the kick events (54, 60) must move with the scoops. Keep each event on its backward
  sweep (ref C). Send the new frames at f10, f21 and f25.

**M-3. Act: the head look-around is a shake.** (`burrow()`, `YW` keys at f64-78)
- Built: `YW` goes +14 at f68-72, then -14 at f75-78. That is a 28 deg reversal in 3 f, about 0.1 s. The head takes 0.6 of
  it and the neck 0.4. It reads as a shake, and the rule forbids head shakes.
- Direction: spread the reversal over at least 10 f (for example `(72, +14)` to `(80, -14)`). Keep the look-around hold within
  f64-78, so the head yaw changes by 3 deg per frame or less.

**M-4. Evidence and numbers.** Send these with the fixes.
- **Rest pose at the end.** The pose sheets stop at act f74 and roar f52. Send act f99 and roar f59 (side and tq), and report
  each clip's maximum joint delta from frame 0. The rule is "ends exactly in the rest pose", so the delta must be about 0.
- **Per-frame limits.** Report the headless maximum per-frame limb swing for each clip (rule: 60 deg or less), and the
  quaternion sign-flip count (must be 0). Neither is in `fullcheck.json`.
- **Chest vs spine.** `CLIP_NOTES` says 1.5 deg, but the code (idle and act) gives about 3 deg, and more in f50-62 where the
  Spine adds 1.5 for the dig. The limit is 5, so this passes, but the notes are wrong. Correct the notes and report the
  measured maximum.
- **Head + neck pitch-up.** The notes say the limit is 6 and the message says 8. The code gives about 6.3 at the act's
  look-up. Report one measured value in world space.

---

## NICE

**N-1. The kick toe dips into the floor.** The lowest point (-0.012, f54) is the back left foot's toe on the first kick. It
passes the -0.02 rule, but it reads as pushing into the grass. Tilt the foot 6-8 deg toe-up during f51-55, or raise the toe
by 0.010, so the minimum is -0.002 or higher.

**N-2. Kick lift is marginally above 5 % of HEIGHT.** `KICK` (3, (0.045, 0.030)): 0.030 is 5.2 % of 0.58 units. Trim to 0.028.

**N-3. Hind kicks read small at game distance.** The 0.045 back slide is about 8 % of HEIGHT. Push it to about 0.06 so the
dirt kick reads from the camera distance. Keep the lift within N-2.

**N-4. No side walk frame.** The walk is covered by numbers and the trot sheet, but there is no side-view walk frame in
the close-ups. Send one walk frame (side, mid-stride) with the next round.

---

## Pass / fail checklist (clip gate)

| # | Check | Result | Note |
|---|---|---|---|
| 1 | collision_free | PASS | true |
| 2 | Ground contact (≥ -0.02) | PASS | lowest -0.012 (act f54), see N-1 |
| 3 | linear = 0 | PASS | all clips |
| 4 | Loops closed (idle, walk) | PASS | |
| 5 | Walk slide ≈ 0 | PASS | 0.0 |
| 6 | Neck ≤ 8 deg | PASS | at the limit |
| 7 | Chest vs spine ≤ 5 deg | PASS | notes wrong, M-4 |
| 8 | Head + neck pitch-up ≤ 30 deg | PASS | about 6-8, M-4 |
| 9 | No head shakes | FAIL | act look-around, M-3 |
| 10 | No airborne spins | PASS | |
| 11 | Acts in place | PASS | linear 0 |
| 12 | Acts end at rest | NOT VERIFIED | no frame past act f74 or roar f52, M-4 |
| 13 | Readable beats: idle | PASS | |
| 14 | Readable beats: walk | PASS on numbers | N-4 |
| 15 | Readable beats: roar | FAIL | M-1 |
| 16 | Readable beats: act opening | FAIL | M-2 |
| 17 | Readable beats: act kicks | NICE | N-3 |
| 18 | Max limb swing ≤ 60 deg per frame | NOT VERIFIED | not in fullcheck, M-4 |
| 19 | Quaternion sign continuity | NOT VERIFIED | not in fullcheck, M-4 |
| 20 | Events named and timed | PASS | prefixes ok, no `end` |
| 21 | Animation references cited | PASS | four cited, with the precedent route |
| 22 | Tris | PASS | 4,956 |
| 23 | Model items from review 2 | PASS | brow seated, haunch on Spine |

## Next step

1. The builder applies M-1, M-2 and M-3, and the N items if they are quick.
2. The builder sends: `pclose_side_roar_30` next to `pclose_side_idle_00`; new act frames at f10, f21 and f25 (side and
   tq); act f99 and roar f59 with their deltas; the per-frame limb and quaternion numbers; and the corrected limit numbers.
3. On those, I sign off the clip gate at 8/10. No full round is needed.
