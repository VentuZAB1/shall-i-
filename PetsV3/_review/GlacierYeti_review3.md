# Glacier Yeti - clip gate review 3 (2026-10-27) - REVISE (clips)

**Score: 6/10.** Ship at 8/10 or better.

The clip set is in good shape. The numbers are clean (collision-free, ground contact, loops, in-place acts, no head shakes), and the skid and roar beats read. Two things block the gate. The walk is not the diagonal gait the notes describe: the phase offsets give a lateral sequence. And the crust icicles still read as two white teeth in profile, right over the muzzle, so the round-2 fix did not land in the side view. Fix these, plus four smaller items below, then send the walk pose sheet, the side view and the limit numbers. No full re-review is needed.

## What I looked at

- Notes: `GlacierYeti/ANIM_REFS.md`, `GlacierYeti/CLIP_NOTES.md`, `GlacierYeti/MODEL_NOTES.md`, `GlacierYeti/_scratch/full_step1.txt`.
- Clip data: `GlacierYeti/GlacierYeti.json` (per-bone quaternions, event fractions). I decomposed the Head, Spine, Chest and Jaw rotations myself. I did not run Blender or Studio.
- Code: `GlacierYeti/_scratch/anim_block.py` (walk L72), `pets/GlacierYeti.py` (crust icicles around L197-201, shelf 2 around L210-213, leg widths L219, `check_pairs` L261-265, `joints` L272-274).
- Renders: `renders/_beats_rw_side.png`, `_beats_rw_tq.png`, `_beats_act_side.png`, `_beats_act_tq.png`, `_model_sheet.png` (side panel and the full sheet), `model_side.png`, `_icons_strip_64.png`, `_icons_strip_128.png`.
- Refs: `_review/ANIM_REFERENCES_1014.md` (sections 1-5, Thornblade Mantis, Leviathan), `BrambleBadger/ANIM_REFS.md`, `IceMammoth/ANIM_REFS.md` (for format), the animation-reference site note and the owner rule.

## Measured numbers (from the JSON)

Angles are degrees from each clip's frame 0. Pitch is about X, yaw about Y. My decomposition uses the quaternion order (x, y, z, w) that the JSON uses.

| clip | bone | pitch range | yaw range | max frame-to-frame | note |
|---|---|---|---|---|---|
| idle | Head | -6.5 .. 0 | ±1.5 | 0.9 | head drop 6.5, no shake |
| idle | Spine | 0 | ±4 | 0.2 | hip yaw, as planned |
| idle | Plate_L/R | max dev 3.6 | | 1.4 | lift is small (NICE 4) |
| walk | Spine | -9 .. -7 | ±2 | 0.5 | hunch about 8 |
| walk | Chest | max dev 4.6 | ±4 | 0.6 | within 5 |
| walk | Head | 4 .. 6 | ±3 | 0.4 | counter-level, no shake |
| roar | Head | -2 .. 17 | ±5 (one turn) | 4.6 | builder says 15.1; within 30 |
| roar | Jaw | -26 .. -2 | 0 | 3.1 | jaw opens 24 |
| roar | Chest | max dev 4.1 | ±4 | 2.4 | within 5 |
| act_skid | Spine | -22.5 .. 0 | ±5.8 | 3.7 | torso drop |
| act_skid | Chest | max dev 4.4 | ±3 | 1.7 | within 5 |
| act_skid | Head | 0 .. 16 | -3.6 .. 2.8 | 2.0 | within 30; no shake |
| act_skid | Jaw | -18 .. -2 | 0 | 6.0 | opens 16 (NICE 1) |

- Loops: idle plates end-vs-start 0.00; walk end-vs-start is one frame step (for example Shin_L 3.5 against a max swing of 4.2). Closed.
- Acts end on rest: roar and skid end-vs-start 0.00 on every bone.
- Root travel: linear 0 (builder audit, not re-measured).
- Ground: ground_min_z 0.002 in all four clips. collision_free true at step 1.

Reconciliation with the brief's numbers:
- "neck ≤ 6": I cannot reproduce it. The rig has no Neck bone, and the Head joint peaks at 16-17 degrees (roar and skid). See MUST 4.
- "head up 15": the builder's 15.1 is close to my 17.0 (method difference). Both are within the 30 limit.
- "chest vs spine ≤ 5": confirmed, 4.1 to 4.6 across clips.

## Checklist (clip gate)

| Check | Result |
|---|---|
| Collision-free, ground ≥ -0.02, linear 0, loops closed, walk slide 0 | PASS |
| Chest vs spine ≤ 5 | PASS (max 4.6) |
| Head + neck pitch-up ≤ 30 | PASS (max 17) |
| Neck ≤ 8 (Head joint is the neck, no Neck bone) | FAIL as measured (17); decision needed (MUST 4) |
| No head shakes | PASS (roar yaw has one turn; walk and idle yaw ≤ 3) |
| No airborne spins | PASS (no flight; spine roll ≤ 2) |
| Acts in place (root net 0) | PASS |
| Acts end exactly at rest | PASS (0.00) |
| Walk is the reference's gait (diagonal LH, RF, RH, LF) | FAIL (lateral in code, MUST 1) |
| Readable beats: skid (drop, sled, slide, dig, rise), roar (lift, jaw open) | PASS, with notes (NICE 3) |
| Collision of crust icicles with the open jaw | NOT CHECKED (no Plate-Jaw pair, MUST 6) |
| Crust icicles and shelf read clean in profile | FAIL (MUST 2, MUST 3) |
| ANIM_REFS rule: 1-3 animationreference.org clips, cited | PARTIAL (roar and skid cited; walk cites only Muybridge, MUST 5) |
| Loop and rest pose consistent across clips (jaw rest) | PARTIAL (jaw rest -3 vs -2, NICE 2) |

## MUST (in priority order)

1. **The walk is a lateral gait, not the diagonal the notes describe.** `GlacierYeti/_scratch/anim_block.py` L72 has `legs = [("Leg_L", 0.0), ("Arm_L", 0.25), ("Leg_R", 0.5), ("Arm_R", 0.75)]`. The arms and legs on the same side are on the same side of the body (both `s = +1` for L, see `pets/GlacierYeti.py` shoulder S and hip LEG). So the sequence is LH, LF, RH, RF: each same-side pair steps in a row. The docstring, the CLIP_NOTES and the Muybridge plate 747 read (Q1) all say diagonal LH, RF, RH, LF.
   - Fix: `legs = [("Leg_L", 0.0), ("Arm_R", 0.25), ("Leg_R", 0.5), ("Arm_L", 0.75)]`.
   - Re-run headless step 1 and check collision-free, ground, slide 0 and the loop.
   - Re-render the walk pose sheet (f0, f12, f24, f36) and check the fists plant on the diagonal.
   - Relabel the stomp: f24 is the Leg_R (RH) contact after the fix, not Leg_L as the notes say (or move the stomp event to f0).

2. **The crust icicles still read as two white teeth in profile.** This is the same misread as round 2. In `model_side.png` and `_model_sheet.png` (side panel) two white spikes hang straight down from the crust's front-bottom edge, right in front of the muzzle. The round-3 direction `(s * 0.65, 0, -1)` is mostly down, so "points straight out" holds only from the front (`pets/GlacierYeti.py` L198-199). The back icicle `(s * 0.45, 0.15, -1)` also hangs down.
   - Delete the front icicle (`ly = -0.03`) and keep the back one, or point it out and back: about `(s * 1.0, 0.30, -0.15)`, so in profile it sweeps back, not down.
   - Target: no white point below the crust's front half in the side view, at rest and in the skid beats f16-28 (`_beats_act_side.png`).

3. **Shelf 2 still reads as a pale pocket on the chest in profile.** Moving it back 0.08 and down to 0.50 helped (round 2 was a bib). In `model_side.png` it is still a pale patch with a green bottom edge at about x 280-360, y 230-295, in the front half of the body.
   - Move it another +0.06 in y (`pets/GlacierYeti.py` L210: `Ua` y +0.08 becomes about +0.14), or shorten its front half so its front edge sits behind the chest line.
   - Target: no pale patch on the chest front in profile.

4. **The neck limit (≤ 8) is unresolved.** The Yeti has no Neck bone; the Head joint carries the neck through the sleeve (`joints()` L273). The Head joint pitches to 16-17 degrees in the roar and the skid. If the Head joint is the neck, this fails the ≤ 8 limit. The brief's "neck ≤ 6" does not match any joint I can measure.
   - Option A (recommended): add a Neck bone and split the lift (neck about 8, head about 9 in the roar), so the limit is met on both joints.
   - Option B: keep one Head joint and record in CLIP_NOTES that a rig without a Neck bone uses the head + neck ≤ 30 rule only. This needs the lead's decision.
   - Either way, state in CLIP_NOTES which joint is measured as the neck, with the real number.

5. **ANIM_REFS rule: the walk cites no animationreference.org clip.** The owner rule (2026-10-10) is 1-3 clips from animationreference.org, cited in the plan. The walk cites only Muybridge plate 747, which is not from that site.
   - The matching clip is already in our notes: `_review/ANIM_REFERENCES_1014.md` #4, "Dragon Walk Cycle" (Sophocleous), a diagonal-pair walk, 45 f cycle, with the head dipping on each front-foot contact. Cite #4 for the walk timing. Keep Muybridge as the frame study.
   - Label the skid refs correctly. "#5 Attack" and "#6 Monsters University" are in the Thornblade Mantis section (combat study set), not the top table (top #5 is the Bird Flight tutorial). Write "Mantis section #5 / #6" in ANIM_REFS.md and CLIP_NOTES.md.

6. **No collision check between the crust and the Jaw.** `check_pairs` (L264) has Plate vs Head but not Plate vs Jaw. The jaw opens 24 degrees in the roar and 16 in the skid, and the crust icicles hang over it.
   - Add `("Plate_L", "Jaw"), ("Plate_R", "Jaw")` to `check_pairs`. Re-run step 1 and report the result for the roar peak (f28-30) and the skid f22-28.

## NICE

1. **Jaw in the skid.** The jaw opens to about 16 degrees, and a red mouth shows at f22 and f58 (`_beats_act_tq.png`). That is not in the plan. If it is a gasp at the brake, keep it and name it in CLIP_NOTES. Otherwise cap the jaw at 8 degrees so the roar stays the only open-mouth beat.
2. **Jaw rest.** The jaw rests at -3 in idle and walk and at -2 in roar and skid. Unify to one value (the "exact rest" rule).
3. **Roar read.** Head lift 17 and jaw 24 are modest for a roar at 5-stud distance. Consider a head lift of about 22 (still within 30 with the neck) and a jaw peak of about 26 at f28-30.
4. **Idle is almost still.** The plates lift 3.6 degrees, which is too small to see at phone size. Raise to about 6, or add a chest breath (the idle is otherwise only a hip yaw and a head drop).
5. **Idle to walk rest.** The idle spine rests at 0 and the walk at -8.6, so the switch needs a cross-fade (about 0.2 s) to avoid a pop. Check in the runtime.
6. **Fist knuckle plates.** From the front (`model_front.png`) the three white plates on each fist top read as a row of teeth. Two plates, or a lower profile, would help.
7. **Icon strip.** At 64 px the Yeti reads as a lilac hulk with a pale shoulder slab. The silhouette passes. The accent does not show at 64 px, which is fine at this size.

## Notes for the next round

- Send: the walk pose sheet after MUST 1 (f0, f12, f24, f36, side and tq); `model_side.png` after MUST 2 and 3; the step-1 output with the Plate-Jaw pairs (MUST 6); the joint decision for MUST 4 (which joint is the neck, and the real number).
- The clip numbers are otherwise clean. Once MUST 1-6 land, I expect the clip gate to clear at about 8/10.
