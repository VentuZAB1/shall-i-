# Volt Rhino - clip gate review 3 (2026-10-27) - REVISE (clips, small)

**Score: 7/10 for the clips.** The motion is sound: four clips, collision-free, ground-clean, loops closed, no pose-limit
breaches, and the round-2 model fixes landed (flush horn rings, brow sunk, one fold wedge per leg, StormWyvern in the strips).
The gate fails on three small items, not on the animation: the animationreference.org rule was not followed for this pet,
two checks are not verified (end-at-rest numbers, the tap-2 and tap-3 contacts), and one decision on the horn tap needs a
written ruling (below).

**Verdict: REVISE (small).** No re-animation is needed unless the new references change the act or the walk. Fix the MUST
list, then send the updated beat sheets and numbers. The lead can keep building the Studio clip data in parallel.

## DECISION: the act_horntap head-down pitch

**Ruling: ACCEPT the head-down strike, with one condition (MUST 2).** Reasons:

1. **The geometry needs it.** At rest the horn tip sits 1.23 units from the throat pivot, 25 deg above horizontal, and the
   throat is 0.86 units above the ground. The tip reaches the snow only when the head points about 44 deg further down, so
   about 69-70 deg of total pitch-down. This matches the builder's 2 + 6 + 62. It is the horn's shape, not a choice.
2. **A crouch cannot remove it in any useful amount.** Each 0.1 units (about 0.5 studs) that the throat drops saves only
   about 6 deg. Getting the head under 45 deg would need the throat about 0.44 units lower (about 2.4 studs, over a quarter of
   the height). That is a kneel, not a strike.
3. **It is a natural rhino pose.** Rhinos and bulls drop the head to 60-80 deg to graze and to charge. It reads as an armed
   charge, not a bow, when the forelegs carry weight (MUST 2).
4. **It is inside the written limits.** The brief limits pitch-UP (head + neck <= 30 deg). Neck 6 deg is under 8. No rule
   covers pitch-down.

The one risk is that the head reads as bowing or pecking. Condition: MUST 2 (brace) and NICE 2 (vary the taps).

## What I looked at
- `VoltRhino/CLIP_NOTES.md`, `VoltRhino/ANIM_REFS.md`, `_scratch/full_step1.txt`, `renders/_beats_act.json`, `renders/_beats_rw.json`
- Beat sheets: `_beats_act_side.png`, `_beats_act_tq.png` (f8-f100, 12 beats); `_beats_rw_side.png`, `_beats_rw_tq.png`
  (roar f6-50, idle f0-90, walk f0-30)
- `_model_sheet.png`, `_close_sheet.png`, `flat_side.png`, `_icons_strip_128.png`
- Rules: `_review/GLACIER_REVIEWER_BRIEF.md`; Obsidian `Creature Animation.md`; the owner's animation-reference rule
  (`feedback-animation-references`); `animation-reference-site.md` (tag URLs)
- Prior round: `_review/VoltRhino_review2.md`

## 1. Model fixes from round 2 (quick check)

| Fix | Status | Evidence |
|---|---|---|
| Horn rings flush, root collar kept | DONE | `_close_sheet` panel 2: faint banding, no steps |
| Brow sunk 0.010 | DONE | Reads as an overhang, not a pipe |
| One fold wedge per leg, no front gaiter | DONE | `_model_sheet`: clean legs |
| Saddle rear edge f 0.06 | DONE | `flat_side`: the light flank panel is gone |
| StormWyvern in the strips | DONE | `_icons_strip_128.png`, 6th icon |
| Lime tip band on the horn | DONE | `_close_sheet` panel 1, reads from the front |

## 2. Clip gate, item by item

| Check (brief + Creature Animation) | Result | Notes |
|---|---|---|
| Collision-free at step 1 (all 4 clips) | PASS | `collision_free: true`, `collisions: {}` |
| ground_min_z >= -0.02 | PASS | idle 0.0, walk -0.002, roar 0.0, act -0.002 (tip at tap 1) |
| Linear 0, loops closed, walk slide 0 | PASS | audit in `full_step1.txt` |
| Neck <= 8 deg | PASS | act 6.0 (max), walk 2.5, roar 3.5, idle 2.1 |
| Chest vs spine <= 5 deg | PASS | notes table: act 2.0, walk 2.1. See MUST 3c (the 4.4 in the brief message does not match) |
| Head + neck pitch-up <= 30 deg | PASS | roar 16.0, act 16.0 |
| No head shakes | PASS | Idle yaw is one slow ±6 cycle. Roar and act have no shake |
| No airborne spins, legs planted in acts | PASS | Feet planted in the act beats; the horn tip is the only contact |
| Acts in place | PASS | Beat sheets: the body does not travel |
| No limb swing > 60 deg per adjacent frame | PASS | Act snap 23.2 deg; idle tail flick 27.5 deg (NICE 1) |
| Readable beats: roar (horn up, snout forward) | PASS | `_beats_rw_side` f16-f36: the horn reaches the sky, the snout stays level |
| Readable beats: act (tap, snap, charge) | PASS with gaps | f22-f30 strike reads. Tap 2 (f42) and tap 3 (f54) are not in the beat sheets (MUST 3a) |
| Ends exactly at rest | NOT VERIFIED | No end-minus-rest numbers for roar or act (MUST 3b) |
| Walk reads as a heavy quad walk | PASS | Duty 0.70, stride 0.343, low head, planted rear. Plate refs B1-B6 match the notes |
| Idle reads as the plan (horn tilt, stamp) | PASS | Left-fore stamp at f46, tail flick at f90, no shake |
| ANIM_REFS rule (animationreference.org, per animation) | FAIL | No clip pulled for this pet (MUST 1) |
| Event times in the export | NOT VERIFIED | `full_step1` stores events as fractions of clip length (MUST 4) |
| Jaw opening within its limit | NOT VERIFIED | Bellow opens the jaw 19 deg; the joint limit is not reported (MUST 3d) |

## 3. MUST (prioritised)

### MUST 1. animationreference.org rule: pull clips for THIS animation
- The owner's rule is "before ANY animation, pull 1-3 clips from animationreference.org, note the frames, and cite them in the
  plan". It is per animation ("get references each time").
- `ANIM_REFS.md` could not play any site clip. The Claude Browser pane was hidden and Chrome froze. It cites Muybridge
  Wikimedia plates (not animationreference.org) and four clips from `_review/ANIM_REFERENCES_1014.md`. Those were pulled
  for other pets (Sea Beasts, Dragon Walk Cycle, Children of the Sea). Reusing them does not meet "each time".
- **Do this:** retry through the Claude-in-Chrome tools, not the hidden pane. If the chrome tools say "No group with id",
  call `switch_browser` (the user clicks Connect). Budget: none of the 25 daily opens has been used.
  - Heavy quadruped charge or walk: `/tags/animals` (532). Lateral walk: `/tags/walk-cycle`.
  - Horn strike and snap: `/tags/combat` or `/tags/impact-frames`. Not `quadruped`, `birds` or `idle` (those 404).
- Pull 1-3 clips, step them frame by frame, and convert 24 fps to our 30 fps (frames x 1.25). Put a short Reference table in
  plan section 10 (still "TBD") and in `ANIM_REFS.md`, with the clip titles, tags, frames and what you take from each.
- If the site has nothing usable, the owner decides a waiver. The builder and the reviewer cannot grant one.

### MUST 2. act_horntap: brace the strike so it reads as a charge, not a bow
- The 70 deg head-down pitch is accepted (ruling above). In the 30 f beat (`_beats_act_side` f30) the forelegs look straight.
  With straight legs a head-down dip reads as bowing or grazing.
- Add a **front-leg knee fold of 4-8 deg** at each tap (the elbow/knee fold already exists) and a **chest drop of about
  0.1 units** at the strike (f22-f30, f34-f42, f46-f54). The throat drop saves about 6 deg, so the head pitch at each tap
  becomes about 63-64 deg. The horn tip must still touch the snow at each tap, with ground_min_z between -0.02 and 0.
- Feet stay planted. Re-run the headless step 1 and report ground_min_z, collision_free and the knee angles.

### MUST 3. Verification gaps (numbers and beats, no re-animation)
a. **Beat sheets for tap 2 (f42) and tap 3 (f54)**, side and tq, with the horn tip height above the snow at each tap. Add them
   to `_beats_act`. Right now only tap 1 (f30) is shown.
b. **End-at-rest numbers** for the roar and the act: the maximum per-bone rotation between the last frame and frame 0. Target
   at or under 1 deg. The notes say "back to rest" but report no numbers.
c. **Reconcile chest vs spine.** The brief message quoted 4.4 deg; `CLIP_NOTES.md` reports 2.0 for act_horntap and 2.1 for
   walk. Both pass the 5 deg limit, but the two figures must match before sign-off. Name the measurement.
d. **Jaw limit.** Report the Jaw joint's maximum rotation in the rig. The bellow opens the jaw 19 deg. Confirm it is within the
   limit and that the jaw is never keyed past it (Model Review Checklist).

### MUST 4. Event time convention
- `full_step1.txt` stores events as fractions of the clip length: `stamp` 0.383 = frame 46 of 120; `bellow1` 0.333 = frame 20
  of 60; `tap1` 0.3 = frame 30 of 100. The clip data is internally consistent.
- Confirm the Lua export and `CreatureAnimator` expect the same unit as the approved pets (for example the Raiju export). If
  the consumer expects frames or seconds, every VFX event fires at the wrong time. Check one approved pet's export first.

## 4. NICE (do these too)
1. **Tail flick smoothing.** The idle flick (f90) swings Tail3 27.5 deg in one frame. Spread it over 3 frames with an ease,
   so it reads as a flick, not a jerk.
2. **Vary the taps.** Three identical dips at f30, f42, f54 can read as pecking, which is bird-like. Make tap 2 a little
   shallower (about 66 deg) or give it a small lateral horn drag, so the three taps read as strikes.
3. **Bolts on the ground.** Let the `FX_BoltTrail` start on the tap frame (f30, f42, f54), not on the snap. The event list
   already has the three taps.
4. **Roar jaw.** Keep the jaw lag (f14). It is already in the plan. Confirm the chin reads pale at the bellow peak (f28).

## 5. Pass / fail summary
- PASS: collisions, ground, audit, neck, chest vs spine (pending MUST 3c), pitch-up, no shakes, no spins, acts in place,
  swing limit per frame, readable roar and act strike, walk and idle reads.
- FAIL: ANIM_REFS rule (MUST 1).
- NOT VERIFIED: end-at-rest, tap 2 and tap 3 contacts, jaw limit, event convention (MUST 2-4).
- Score: 7/10. Verdict: REVISE (small). Next: MUST 1-4, then send the sheets:
  `_beats_act_side`, `_beats_act_tq` (with f42, f54), the new end-pose numbers, the jaw limit and the export check.
