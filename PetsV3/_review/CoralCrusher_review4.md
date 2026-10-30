# Coral Crusher - clip gate review 4 (2026-10-27) - APPROVED, 8/10

**Verdict: APPROVED. Score 8/10 (ship bar 8). No MUST left.** Both round-3 MUSTs are answered:
- **M1 (animation references):** the walk and wave now cite two site clips, with post IDs, frame ranges and observations.
- **M2 (wave timing):** the act is three slow display arcs with holds, a 120 f length, and the peaks and events where the
  round-3 spec put them.

Three small NICE items remain. They are optional and do not block the export.

## What I looked at
- `CoralCrusher/ANIM_REFS.md` (round 4 section, S1 and S2, and the C1/C2 Wikimedia notes)
- `CoralCrusher/CLIP_NOTES.md` (round 4 section, and the clip table)
- `pets/CoralCrusher.py` `act_semaphore` (L538-576, keys for `lift_r`, `spread_r`, `fore_r`, `wrist_r`, `tap_l`, events)
- `renders/_wave_strip.png` (tq and game, every 2 f, f18-78, peaks and troughs labelled)
- `renders/_pose_tq_sheet.png` (rebuilt; roar and act beats, including act f18, 28, 38, 50, 60, 72, 80, 84, 90, 104)
- Not re-run: the headless gate. I used the numbers the notes report (collision_free true, ground -0.013, loops 0, slide 0.002).
- Not opened: the Sakugabooru posts. My role is read-only, so I judged the cited observations for internal consistency
  with the build, and for whether they are real site clips with IDs and frames.

## M1 - animation references (PASS)
- **S1 (walk):** Sakugabooru #270689, the Ohmu run in *Nausicaa*, `/tags/creature-animation`. Observations O1-O3 (two
  alternating leg sets; a level shell; the arch is run-specific) give frame ranges. The notes say the walk does not change
  because the clip agrees on alternation and level shell. That is a fair read.
  - **Caveat (NICE):** S1 is a *run*, so it supports the alternation pattern, not the walk timing. The 30 f walk cycle is
    still set by the Wikimedia walk (C1). Say so in the walk line of `CLIP_NOTES.md`, so nobody later takes the Ohmu's 10 f
    cycle as the target.
- **S2 (wave):** Sakugabooru #170480, James Baxter's dancing horse, `/tags/creature-animation`. H1 (up, f34-42), H2
  (hold, f42-90 while the other foreleg works), H3 (drop, f90-92/94) give frame ranges and the rise/hold/drop rhythm. Good.
- The rejected clips and the tags tried are in the log. That is the honest version of the owner's rule.
- **Owner rule:** "pull 1-3 clips from animationreference.org, note key poses/frames, cite them" is met. Two site clips are
  cited with IDs and frames. The Wikimedia clips stay as study notes, which is fine.

## M2 - the wave (PASS)
Checked against `_wave_strip.png` and the code:
- **Three peaks**, labelled `wave1` f28, `wave2` f50, `wave3` f72. Troughs at f38 and f60 (labelled). Period about 22 f
  (about 0.73 s) per arc, inside the 20-24 f I asked for.
- **Holds:** keys hold each top for 4 f (f26-30, f48-52, f70-74). In the strip the four frames at each top look alike, so the
  top reads as a pause.
- **Rotation top to trough** (world, from the builder's probe): merus 36.7 deg, carpus 42.1 deg, claw 36.7 deg. All >= 30.
  The strip shows the claw rising to the top and dropping forward in front at each trough, so the arcs read in tq and game.
- **Up and down timing:** up 10 f (trough to top), down 8 f (top to trough). Slow up, quicker down, as F3 asks.
- **After the waves:** the claw holds out at f74-80, the cutter taps at f84 and f90, the claw swings in and folds f90-104,
  and the pet is exactly at rest from f104 to f120. The pose sheet agrees (f90 lower, f104 at rest).
- **Legs:** planted (foot drift 0.0 per the notes). The stand is now 0.10 BU and pitch -5 (N2), and the feet stay put.
- **Pose limits (Spine as analogue):** pitch -5 and roll -2 in the act, and the roar pitch is unchanged. Under the limits.

## NICE (optional; none blocks export)
- **N1 hold length:** the tops hold 4 f (about 0.13 s). The references hold far longer: the Ohmu-style display (C2, about
  1.5 s per pose) and the horse's raised foreleg (H2, about 2 s). The 4 f is what I specified in round 3, so it passes. A
  6-8 f hold would read more clearly as a *display* at game distance.
- **N2 return length:** the build's down-stroke is 8 f. The cited H3 drop is 2-4 f at 24 fps, about 3-5 f at 30 fps. So
  "quick drop" is only partly supported. Either shorten the return to about 5-6 f (check `collision_free` after, since a
  faster fold can meet the rim), or add a line in `ANIM_REFS.md` saying why 8 f is kept.
- **N3 walk citation:** see the S1 caveat above. Add the Wikimedia C1 cycle timing to the walk line, so the 30 f cycle has one
  owner.

## Pass / fail checklist

| # | check | result |
|---|---|---|
| 1 | M1: site clips cited with IDs, frames and observations | **PASS** |
| 2 | M1: walk agrees with cited alternation (no walk change needed) | **PASS** (N3 caveat) |
| 3 | M2: three arcs, period 20-24 f | **PASS** (about 22 f) |
| 4 | M2: holds at each top | **PASS** (4 f; N1) |
| 5 | M2: top-to-trough >= 30 deg | **PASS** (36.7 / 42.1 / 36.7) |
| 6 | M2: events on the peaks, taps, fold, rest | **PASS** |
| 7 | N2 (stand taller) and N3 (roar 30 deg) | **PASS** |
| 8 | Gate numbers (as reported): collision_free, ground, loops, slide | **PASS** (not re-run) |
| 9 | Pose limits (Spine analogue), no head shakes, no airborne spins | **PASS** |
| 10 | Acts in place and end at rest | **PASS** (f104-120) |
| 11 | Holds and return timing match the cited refs | **PASS**, with N1 and N2 optional |

**APPROVED, 8/10.** Clip gate passes. Clips can be exported. N1-N3 are optional.
