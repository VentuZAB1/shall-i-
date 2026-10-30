# Coral Crusher - model round-3 check + CLIP GATE review 3 (2026-10-27) - APPROVED WITH FIXES

**Score: 8/10 for a 15 % Medium (ship bar 8).**
- **Model: APPROVED.** The round-2 MUSTs landed. The claws are smooth, the plastic cream is gone, the walk-blend skate is
  fixed, and the game-camera portrait reads as a crab.
- **Clips: APPROVED WITH FIXES.** Every numeric gate passes (collision-free, planted feet, closed loops, slide 0.002, pose
  limits on the rig's analogues). Two items need fixing before the clips are exported: **M1** (the owner's animationreference
  rule) and **M2** (the wave timing, which is the signature act).

## What I looked at
- Model: `renders/_model_sheet.png` (tq, front, side, back), `_close_sheet.png` (claw tq and side, face front and high),
  `_under_sheet.png`, `_crossfade_sheet.png` (9 frames, 0.3 s), `model_front.png`, `gamelook_game.png`,
  `CoralCrusher_portrait_alt.png` (512 px game-camera idle f0)
- Clips: `renders/_pose_tq_sheet.png` (21 beats: idle, walk, roar, act), `CLIP_NOTES.md`, `ANIM_REFS.md`,
  `_scratch/clipgate.txt` (headless numbers), `_scratch/shares_strict.json`
- Code: `pets/CoralCrusher.py` clip section (idle L:~457, walk L:~480, roar L:~513, `act_semaphore` L:538-563, `YAW_WALK` /
  `BASE_YAW` = 45, L:397-398)
- Rules: the owner's animation-references rule (memory `feedback-animation-references`), the site guide
  (`animation-reference-site`), `_review/CoralCrusher_review2.md`

## 1. Model round-3 check (review-2 MUSTs and NICE)

| item | result |
|---|---|
| M1 claws: cream dropped, palm / fingers / knuckles smooth | **PASS.** `close_sheet` claw panels: bronze palms and fingers with no stud dots; the cream is gone. Studs stay on the merus and carpus (allowed). |
| M1 pale share 0.9 % side (lead ruling: ACCEPT as built) | **ACCEPT.** The claw cream was the mitten read. Note: from below (`_under_sheet`) the underside is a flat pale octagon. Never seen from the game camera, but see N1. |
| M2 base pose at 45 deg, ankle travel 0.077 BU (was 0.79) | **PASS.** `_crossfade_sheet` shows the feet staying put through the blend. |
| M3 portrait = game-camera icon | **PASS.** `CoralCrusher_portrait_alt.png` reads as a crab with claws up, shell seams, and legs. |
| N1 second plate row on the dome | **PASS.** Two dome arcs are visible in the tq and game views. |
| N3 rear ledge lower | **PASS** by eye (not measured). |
| N4 margin spines alternate large / small | **PASS.** Visible in `model_front` and `gamelook_game`. |
| N5 walk claws 10 deg lower | **PASS.** Walk frames show the claws folded low. |
| Shares (builder's strict file) | side: bronze 49.6, bronze_d 12.1, shell_d 19.2, rose+rose_d 11.1, pale 0.9, black 5.4. Game: shell_d 16.2, rose 11.3. Accepted. |
| Tris | 11,900 (cap 15k). **PASS.** |

Visual read in game (`gamelook_game`): the crab reads as a crab at game distance. The spines carry the accent, the claws
are bronze with pink tips, and the shell is a copper dome with seams. No plastic read.

## 2. Clip gate (numbers from `_scratch/clipgate.txt`, pose sheet checked)

| gate | result |
|---|---|
| collision_free | **PASS** (true, all clips, every frame) |
| ground_min_z | **PASS** (-0.013, never lower; legs at rest) |
| linear / loops | **PASS.** linear 0 everywhere; idle loop pos 0 / rot 0; walk loop pos 0 / rot 0; idle foot drift 0 |
| walk slide / foot_z_var | **PASS.** 0.002 / 0.001 |
| events match the beats | **PASS.** Walk sand 13.8 / 28.8 (the tripod touch-downs in the code); roar clacks 22 / 30 / 38; act waves 26 / 40 / 54, taps 66 / 70; idle tap 70 |
| Pose limits (no neck or chest bone; I used the Spine as the analogue) | **PASS.** Spine pitch max -4 (roar, nose up) and -3 (act); roll -2 at most. Claw lifts of 20 to 60 deg are limb poses, not head pitch. |
| No head shakes | **PASS.** The idle eyes swivel one at a time (left +10 at f18-44, right -10 at f60-80), with a freeze between. No alternating L/R shake. |
| No airborne spins | **PASS.** Feet stay on the ground in every frame. |
| Acts in place, end at rest | **PASS.** The act returns to exact rest by f90-100; the roar and idle zero out by f60 and f120. |
| Walk gait | **PASS.** Tripods L1/R5/L3 vs R4/L2/R6, duty 0.55, body at 45 deg, claws held low. |
| Idle claw guard | **PASS.** The crusher lifts 20 deg from f28 and holds to f98; the cutter taps at f70. |
| Roar clacks | **PASS** in the sheet and code. Cocked open, snap shut, hard stop, three times. |
| Wave: readable as the signature | **FAIL as timed** (M2). |
| Reference rule | **FAIL** (M1). |

## 3. MUST (before the clips are exported)

### M1 - The owner's animationreference rule (process, not a clip change)
- The owner's rule (memory `feedback-animation-references`) asks for 1 to 3 clips from **animationreference.org** before any
  animation, with the key poses and frames cited.
- `ANIM_REFS.md` shows a search with no crab / insect / multi-leg tag, and then Wikimedia footage (C1 walk, C2 wave). The
  Wikimedia clips are useful study, but they are **not** the site clips the rule asks for. The site clips it reuses (#5,
  #6, #7) come from the 2026-10-14 Abyss Weaver session, not this pet.
- Fix, using the site tags the guide lists (no quadruped tag exists; `/tags/quadruped` is a 404):
  - **walk:** `/resources/locomotion-animation-reference` (its quadruped-gait section) or `/tags/walk-cycle` (367). Pick a
    clip with a multi-leg or tripod-like gait and cite the frames. The tripod timing is the point.
  - **wave / display:** `/tags/creature-animation` or `/tags/body-mechanics` (76). Pick a clip with a raise, hold and return
    of one limb (any creature), and cite the frames for the up, hold and down.
  - Add both citations to `ANIM_REFS.md` with the frame numbers. Keep the Wikimedia clips as study notes.
- If the site clips contradict the Wikimedia read (for example, a walk that holds the body square), the walk changes; say so.
- If the owner accepts Wikimedia for this pet, the lead must log that ruling in writing.

### M2 - The wave is a flutter, not a display (signature act)
- Current keys (`act_semaphore`, `fore_r`): the carpus swings 8 to 42 deg with **no hold** at the top. The period is 14 frames
  (about 0.47 s per arc). The plan asked for "slow arcs", and the reference (C2 F3) holds each pose about 1.5 s. Right now the
  three waves read as a quick flutter.
- **Direction:** arcs about **20 to 24 frames** per wave, with a **4-frame hold at each top** (the display). For example:
  - waves in the window f18 to f78, with peaks at about f28, f50, f72, troughs about 10 frames apart;
  - taps at f84 and f90 (the cutter), fold f90 to f104, rest f104 to f120 (act length **120**, not 100).
  - Move the events to the new peaks (`wave1..3`) and taps (`tap1..2`).
- "Stands tall": the body rises 0.05 BU (about 0.3 stud) with pitch -3. That is barely visible. See N2.
- **Check when re-rendered:** a wave strip (tq and game, every 2 frames across f18 to f78). It must show three peaks of at
  least 30 deg, each with a visible hold. Legs stay planted (`collision_free` true, slide 0).

---------------------------------------------------------------------------------------------------------------------
## 4. NICE

- **N1 Underside:** from below the belly is one flat pale octagon. Give it a slight taper or dome (about 0.02 BU) so it reads
  as a belly, not a plate. The game camera never sees it, so this is low priority.
- **N2 Stand tall:** raise the act's body rise from 0.05 BU to about **0.10 BU** and pitch to -5, so "stands tall" reads
  (about 0.6 stud at this scale).
- **N3 Roar:** the crouch reads well in the sheet. Consider a slightly higher peak on the clacks (cocked open to 30 deg, now
  25 deg lift) so the three clacks look distinct at game distance.
- **N4 Idle eye swivel:** the swivel is about 10 deg. Fine as a look-around. Keep it.

---------------------------------------------------------------------------------------------------------------------
## 5. Deviations (round 3)
1. **Pale share 0.9 % (lead ruling):** **ACCEPT.** The claw cream was the mitten read. The underside shows from low angles
   only, and the game camera does not see it.
2. **Walk / idle base at yaw 45 (review-2 M2 option A):** **ACCEPT.** The skate is fixed (0.077 BU).
3. **Wikimedia references instead of the site (M1):** **NOT ACCEPTED as built.** The owner's rule asks for the site clips.

---------------------------------------------------------------------------------------------------------------------
## 6. Pass / fail checklist

| # | check | result |
|---|---|---|
| 1 | Model: claws smooth, no plastic cream | **PASS** |
| 2 | Model: portrait = game-camera icon | **PASS** |
| 3 | Model: pale share (accepted by lead ruling) | **ACCEPT** |
| 4 | Model: tris <= 15k | **PASS** (11,900) |
| 5 | Crossfade: feet planted through idle to walk | **PASS** (0.077 BU) |
| 6 | Clips: collision_free, ground, linear 0, loops, slide | **PASS** |
| 7 | Pose limits (Spine analogue), no head shakes, no airborne spins | **PASS** |
| 8 | Acts in place, end at rest | **PASS** |
| 9 | Walk tripods and claw pose | **PASS** |
| 10 | Roar clacks readable | **PASS** |
| 11 | Wave readable as the signature (holds, arc period) | **FAIL** (M2) |
| 12 | Animation-reference rule (owner) | **FAIL** (M1) |

Re-check (round 4, small): the site citations for walk and wave (M1), and the re-timed wave strip (M2). No model round.

**APPROVED WITH FIXES, 8/10.** Model approved. Clips: M1 and M2 must land before the export.
