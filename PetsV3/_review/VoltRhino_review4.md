# Volt Rhino - clip gate review 4 (2026-10-27) - APPROVED WITH FIXES (clips)

**Score: 8/10 for the clips** (review 3 was 7/10). The motion is now a credible heavy quadruped: the charge reads as a braced
strike, the walk is a true lateral sequence, the bellow opens the jaw with the head held up, and every pose limit and the
end-at-rest checks pass. What is left is paperwork and stale renders, not the animation.

**Verdict: APPROVED WITH FIXES.** Clip geometry and data are approved. The three MUST items below must land before the final
export and the clip sign-off. None of them changes a bone, a joint or a timing.

## Rulings the lead asked for

- **MUST 4, event convention: PASS.** `ThunderRex/ThunderRex.lua` line 108 exports `roar = {peak = 0.381, ...}`, and
  `ROBLOX PLAYBOOK/.../CreatureAnimator.lua` `_events` (line 213) fires at `t = frac * len`. Fractions of clip length are the
  live convention. The Volt Rhino events (`stamp` 0.383, `bellow1` 0.333, `tap1` 0.3) are consistent with it.
- **MUST 2, the brace: PASS.** Judged from `_beats_act_side` f30 / f42 / f54 and `_beats_act_tq`:
  - the spine stays level (Spine pitch +1.5 only), so it reads as a charge, not a bow. The bow read would need the back to round;
  - the forelegs fold and the chest drops (the chest's lowest point 0.591 to 0.528). The strike reads as weight going forward;
  - the feet stay on the ground in every beat;
  - the horn tip sits on the snow at each tap (Horn_Tip z 0.013 / 0.024 / 0.013; mesh bottoms -0.002 / 0.008 / -0.002).
  The deviation is accepted: a 29.8 deg knee fold plus a 0.06 chest drop does what the 4-8 deg plus 0.1 request was for.
  One caveat: report Foot_FL / Foot_FR z at f30 / f42 / f54 (expect about 0) so "planted" is a number, not a judgement (NICE 3).

## What I looked at
- `VoltRhino/CLIP_NOTES.md` (Round 3 and the References round), `VoltRhino/ANIM_REFS.md` ("Central references" section)
- `_review/ANIM_REFERENCES_1027.md` (the central pull and the per-pet citation list)
- `_scratch/verify.json`, `_scratch/full_step1.txt`
- Renders: `_beats_act_side.png`, `_beats_act_tq.png` (f16-f100, incl. f30 / f42 / f54), `_jaw_roar_sheet.png`,
  `pclose_side_roar_00/28.png`, `pclose_tq_roar_28.png`, `_beats_rw_side/tq.png` (roar, idle, walk; see MUST 1)
- Source comparison: `pets/Raiju.py`, `pets/ThunderRex.py`, `pets/ThunderBull.py` (`joints()`)

## MUST (before the final export and clip sign-off)

### MUST 1. Stale renders: re-render the beats from the final rig
- The final files are `VoltRhino.lua` and `VoltRhino_rigged.blend` at 21:57:50, and `verify.json` at 21:58.
- The beat renders are older: `_beats_act_*.png` 17:43, `_jaw_roar_sheet.png` and `pclose_*` 17:45, `_beats_rw_*.png` 17:33.
  The walk changed at about 21:57 (own lateral offsets BL 0, FL 0.75, BR 0.5, FR 0.25). The walk beats still show the old
  diagonal sequence, and the roar beats predate the 14 deg jaw and the f10 onset.
- The numbers were re-run, so the data is current. The pictures are not. Re-render from `VoltRhino_rigged.blend` (21:57):
  - walk side and tq at f0, 10, 20, 30 (the lateral touch-downs);
  - roar side at f6, 16, 20, 28, 36, 50, plus the jaw close-up at f28;
  - act side and tq at f16, 22, 27, 30, 39, 42, 46, 54, 58, 62, 86, 100.
- Put the render time in the sheet title or the file name, so the reviewer knows the pictures match the export.

### MUST 2. Animation references: the owner rule is per animation, and two of three are not met yet
The rule: pull 1-3 clips from animationreference.org for each animation, note the key frames, and cite them.

a. **Walk: no site clip.** The central file names `walk-cycle` as a useful tag for quadrupeds (367 clips). Volt Rhino's
   "Site tags searched" list is `elephants`, `animals`, `muybridge`, `wolfs-rain`, `kaiju-no-8`; `walk-cycle` is not in it.
   - Open one `/tags/walk-cycle` (or `/tags/animals`) clip, step it, and cite the touch-down frames, or write the no-fit result.
   - Also give the photo numbers from Muybridge "Walking bison" for the touch-down order (BL, FL, BR, FR) and the duty.
     The current text cites "B1-B6" without the photo numbers.
b. **Act (horn strike): the search result is not written.** `kaiju-no-8` is listed as searched, but no result is recorded.
   - Write one line: how many candidates, and why none fits. Only then is the Wikimedia fallback (Plate 700) the right source.
   - Plate 700 itself is well cited (frames 9-16, what is taken, and the match to the brace). Keep it as the brace source.
   - There are 22 site opens left today, so there is budget for one act clip if one fits.
c. **W0 (bellow onset): give the source frames.** The file says "~0.66 s (~20 f at 30 fps)" and the central file says "about 15 f".
   Both are right at different frame rates, but neither gives the source frame range. Write the 24 fps source frames
   (mouth starts, peak, hold), then the 30 fps conversion (x1.25). The bellow's f10 start, f16 mid and f20 peak should match.

### MUST 3. Plan section 10 still says "TBD by builder"
- `_review/VoltRhino_plan.md` section 10 still reads "TBD by builder. Suggested tags: rhino charge..." The owner's rule says to
  cite the clips in the plan. Put the reference table, or a pointer to ANIM_REFS "Central references", into section 10.

## NICE (do these too)

1. **Open-jaw look (`pclose_side_roar_28`, `_jaw_roar_sheet` panels 2 and 4).** The pale lower jaw reads as a flat plank under a
   flat maroon box, not a mouth. At phone size it is small, so this is not a blocker. Taper the pale jaw back into the skull
   line, and make the mouth interior taper inward instead of a box.
2. **Throat exemption.** Raw collisions in the act are 51-62 frames (Head|Chest, Jaw|Chest) and are exempted by the 0.26
   throat hinge. Raiju, ThunderRex and ThunderBull use the same `joints()` pattern, so I accept it. Add one throat close-up
   from below at f42, to confirm there is no skin poke-through at 70 deg of pitch.
3. **Planted feet as a number.** Report Foot_FL and Foot_FR z at f30, f42 and f54 (expect about 0).
4. **Tap variety.** Tap 2 is shallower and drags the horn (NICE 2 of round 3, in the notes). Keep it. If the three taps still
   look too alike at speed, make tap 3 a little deeper than tap 1.

## Pass / fail checklist

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Collision-free step 1 (4 clips) | PASS | `collision_free: true`, `collisions: {}`; raw counts explained by the throat hinge |
| 2 | ground_min_z >= -0.02 | PASS | idle 0.0, walk -0.002, roar 0.0, act -0.002 |
| 3 | Linear 0, loops closed, walk slide 0 | PASS | audit in `full_step1.txt` |
| 4 | Neck <= 8 deg | PASS | act 6.0, walk 2.48, roar 3.5, idle 2.06 |
| 5 | Chest vs spine <= 5 deg | PASS | act 3.8 (the brace), walk 2.09, roar 1.0, idle 0.68. The 4.4 figure was the Yeti's act, not the rhino |
| 6 | Head + neck pitch-up <= 30 deg | PASS | roar 16.0, act 16.0 |
| 7 | Max swing per frame <= 60 deg | PASS | act 23.1 (the snap), idle 15.1 (tail flick, spread over 82-107) |
| 8 | No head shakes | PASS | Idle yaw is one slow cycle |
| 9 | No airborne spins; acts in place | PASS | Feet planted in the act beats (confirm with NICE 3) |
| 10 | Ends at rest | PASS | end vs start 0.0, end vs rest 0.0 (roar and act) |
| 11 | Brace reads as a charge, not a bow | PASS | Level spine, folded forelegs, horn on the snow (MUST 2 ruling) |
| 12 | Readable roar (horn up, snout forward) | PASS on old beats | Re-check after MUST 1 |
| 13 | Jaw within its limit | PASS | roar 14.0 (limit 14), act 8.0, idle 2.0, walk 1.5. The limit is the builder's own (kit has none); it is enforced in the rig |
| 14 | Events as fractions | PASS | MUST 4 ruling; matches ThunderRex and `CreatureAnimator._events` |
| 15 | Walk: lateral sequence | PASS on numbers | BL f0, FL f10, BR f20, FR f30 (LH, LF, RH, RF). Picture stale (MUST 1) |
| 16 | Animation references (owner rule) | PARTIAL | W0 cited (needs source frames); Plate 700 and Walking bison cited; walk and act have no site clip (MUST 2) |
| 17 | Plan section 10 cites the refs | FAIL | Still "TBD" (MUST 3) |
| 18 | Renders match the final export | FAIL | Beats are older than the 21:57 export (MUST 1) |

## Summary
- Approved: the motion, the limits, the events, the brace and the bellow timing.
- Must land before the final export: re-rendered beats from the final rig (MUST 1), per-animation references for the walk and
  the act with source frames for W0 (MUST 2), and plan section 10 updated (MUST 3).
- Score: 8/10. Verdict: APPROVED WITH FIXES.
