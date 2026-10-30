# Ice Mammoth - clip gate review 3 (2026-10-27) - APPROVED WITH FIXES (clips)

**Score: 7.5/10 for a MEDIUM 26 %.** The walk, the idle and the roar read well and pass the pose and collision limits. The
dust-over act has one real fault: the trunk tip never reaches the snow, so the scoop and its snow spray hang in the air.
That fix is a key change on three frames. The remaining MUSTs are numeric reports and one owner decision about the
animationreference.org rule. The bone names and the rig do not change, so the fixes do not reopen the model gate.

## Round-2 NICE items (from the coordinator's list)
- Tusk-cap edge (pale ICE_MINT ring, t 0.52-0.60): **done**, the step reads as ice, not a dipped sleeve (close sheet, middle panel).
- Two large head clumps: **done**, they read as a wool crown (close sheet).
- Eye socket (0.078, 0.012, 0.024): **done**, but see NICE 1.
- Skull and dome 0.04 shorter at the back: **done**. In the act and roar side sheets the dome clears the shoulder hump at the
  head-lift frames (f44-f56 act, f16-f40 roar). No visible contact.

## What I looked at
- `IceMammoth/ANIM_REFS.md`, `CLIP_NOTES.md`, `MODEL_NOTES.md` (round 2), `_scratch/full_step1.txt` (the 17:12 run),
  `_scratch/limits.py`, `pets/IceMammoth.py` (rig L319-353, `joints()` L368-370, `neck_lift` L416-420)
- `_review/ANIMATION_REFERENCES_1014.md` (refs #3, #5, #9 are animationreference.org clips with cited timing)
- Beat sheets, all viewed:
  - `_beats_act_side.png` and `_beats_act_tq.png` (f10, 20, 32, 44, 52, 56, 66, 74, 80, 86, 95, 100)
  - `_beats_rw_side.png` and `_beats_rw_tq.png` (roar f8, 16, 22, 40, 58; idle f0, 30, 80; walk f0, 10, 20, 30)
- Strips: `_icons_strip_64.png` (4x zoom), `_close_sheet.png`
- Flat palette counts on `flat_side.png` and `flat_game.png`

## Verified numbers
| clip | collision_free | ground_min_z | loop / rest | max adjacent swing | head pitch-up | neck (saved) | chest (saved) |
|---|---|---|---|---|---|---|---|
| idle 120 | true | 0.018 | loop closed, foot drift 0 | 4.0 | 1.1 | 0.6 | 0.5 |
| walk 40 | true | 0.015 | loop closed, slide 0.0 | 6.1 | 0.2 | 0.8 | 1.7 |
| roar 66 | true | 0.018 | linear 0 (rest not measured, M4) | 20.8 | 16 | 2.0 | 1.0 |
| act 100 | true | 0.018 | linear 0 (rest not measured, M4) | 43.6 (Trunk4) | 17 | 2.0 | 0 |

- Max adjacent-frame swing 43.6 on the trunk is under the 60 deg rule. No airborne spins. No head shakes (roar tremble ±2, walk head ±1).
- Head pitch-up 16 and 17 deg are under 30. Event names (stomp, exhale, trumpet, scoop1-3, dust1-3) have no `end`.
- Event timings match the plan: act dust1 56, dust2 74, dust3 86; roar trumpet at 26; idle exhale at 80; walk stomp at 30.
- **The numbers in the message do not match the saved table.** The message gives neck ≤6 deg and chest vs spine ≤4.4 deg.
  CLIP_NOTES gives neck max 2.0 and chest max 1.7. Both pass, but there is no saved LIMITS_RESULT file to show the source (MUST 3).

## Clip judgement
- **walk (40 f): PASS.** The gait follows Muybridge plate 733 as the notes say: the lateral sequence LH, LF, RH, RF (BL 0,
  FL 0.25, BR 0.5, FR 0.75), duty 0.72, the fore legs fold with a low lift, and the head is nearly still. Frames 0, 10, 20 and
  30 show planted, heavy feet and a readable stride. Good.
- **idle (120 f): PASS.** A small, lagged trunk swing with the tusks still. The exhale at f80 lifts the trunk tip, which reads.
- **roar (66 f): PASS.** Tuck at f8, the head lifts and the trunk rises through a forward pose at f16 to near-vertical at f40
  (the trumpet). Trunk lowers with a slower return at f58. The jaw opens after the lift, as ref #3 says.
- **act_dustover (100 f): FAIL on contact.** See MUST 1. Everything else in the act is readable: the lift in front of the
  face at f32-f44, the snap over the brow at f56 and f86, the two smaller scoops, and the return to rest.

---------------------------------------------------------------------------------------------------------------------
## MUST (in priority order)

**M1. The act scoop must reach the snow.** (Clip fix, act only.)
- The side and tq panels show the trunk tip about one stud above the snow at its lowest, at scoop1 f20, scoop2 f66 and
  scoop3 f80 (my estimate from the panels; not measured). The plan says the trunk "drops and curls
  into the snow (tip down, scoop open)". The FX_SnowSpray anchor sits on Trunk_Tip, so today the spray would hang in the
  air about a stud above the ground.
- The idle, roar and act all show ground_min_z 0.018. That is the same value, so it is almost certainly the foot soles at
  rest, and the trunk tip's lowest point has never been measured.
- Fix: at f20, f66 and f80, lower the tip (Trunk1-4 pitch, plus Trunk_Tip if needed) until Trunk_Tip world z is at most 0.04 units
  above the ground. The tip may touch at about 0.01. ground_min_z must stay at or above -0.02 for the whole clip.
- The scoop frames must keep the head pitch at or under 20 deg, and the chest and neck limits stay as they are.
- Report: the world Trunk_Tip z at f20, f66 and f80, and the minimum Trunk_Tip z over the act.

**M2. OWNER DECISION: the animationreference.org rule is not met as written.** (Not a builder fix; the owner must accept or reject.)
- The owner rule (feedback-animation-references) says to pull 1-3 clips from animationreference.org before any animation.
  The builder could not play the only elephant clip, so the rule was not met for this pet.
- Substitutes: the walk uses Muybridge plate 733 (a real frame-by-frame still, not animationreference.org). The roar and the act
  use refs #3 (Sea Beasts heavy-head roar), #5 (combat "Attack" snap) and #9 (Children of the Sea humpback mass), which are real
  animationreference.org clips already logged in `_review/ANIMATION_REFERENCES_1014.md`. None is an elephant or a trunk.
- The substitution is documented, and it is reasonable. But I cannot approve a rule exception as a reviewer. Options for the
  owner: accept the substitute, or pull one elephant or trunk clip for the act and the roar when animationreference.org is
  reachable again.

**M3. Reconcile the limit numbers and save the run.**
- The message says neck ≤6 deg and chest vs spine ≤4.4 deg. CLIP_NOTES says neck max 2.0 and chest max 1.7.
- `limits.py` measures the Chest's own local angle, not chest relative to spine. Say which one 4.4 came from, and save the
  `LIMITS_RESULT` line to a file next to CLIP_NOTES.

**M4. Measure the rest pose for the two non-looping clips.**
- roar and act both end at rest, but the audit measures only the root (linear 0). Report the maximum bone rotation difference
  between frame 0 and the last frame, for both clips. Target at most 0.5 deg.

**M5. Report the throat-hinge exemption before counting it as collision-free.**
- `joints()` (L368-370) is a capsule at y -0.88, z 1.03, x ±0.24, radius 0.09 on the Head. `overlap_report` ignores any Head or
  Chest (or Jaw or Chest) crossing whose points all sit inside it. The count of ignored crossings is not in the output, so
  `collision_free: true` is partly the exemption.
- Report, per clip: the raw crossing count before the exemption, and the count the exemption removed. Then add one throat
  close-up (side, tq) at roar f22 and act f48, where the head pitch is at its largest.
- If the raw crossings are only in the capsule and no skull or dome geometry passes through the chest bib, the exemption is
  fine as written. If any crossings sit outside it, fix the geometry before the exemption counts.

---------------------------------------------------------------------------------------------------------------------
## NICE
1. **Eye at close range.** The eye reads as a small white-rimmed square window with a black dash, not a slit (close sheet,
   front panel). Make the MINT slit a bit darker, or cut the white rim so it reads as a narrow slanted slit. Keep the black socket.
2. **Act: the tip height and the spray together.** Once M1 lands, check that FX_SnowSpray at scoop1, scoop2 and scoop3 lands on
   the snow in the tq sheet.
3. **C1 is still open.** The body colour in game (the Studio capture at the 5-stud camera from the round-2 gate) is still
   not done. The lit preview is aqua. Apply the round-2 NICE 3 hue shift only if the capture says aqua.
4. **Walk frames.** The walk beat set is 10-frame steps. Add one frame at f5 and f35 (the mid-contact) so the lateral sequence
   can be checked against the plate's frame 6-8 swing.

## Pass / fail checklist
| check | result | note |
|---|---|---|
| collision_free, all 4 clips | PASS (with M5) | exemption not yet reported |
| ground_min_z ≥ -0.02 | PASS | 0.015-0.018 |
| Trunk tip above ground during the scoops | **FAIL** | M1 |
| Loops closed (idle, walk) | PASS | loop_pos 0, loop_rot 0 |
| Roar and act end at rest | NOT MEASURED | M4 |
| Walk slide ~0 | PASS | 0.0 |
| Idle feet still | PASS | drift 0 |
| Linear root motion 0 (all clips) | PASS | |
| Neck ≤ 8 deg | PASS | 2.0 saved (6 in message: M3) |
| Chest vs spine ≤ 5 deg | PASS | 1.7 saved (4.4 in message: M3) |
| Head + neck pitch-up ≤ 30 deg | PASS | 16 roar, 17 act |
| Max adjacent-frame swing ≤ 60 deg | PASS | 43.6 trunk, act |
| No head shakes | PASS | |
| No airborne spins | PASS | |
| Acts in place | PASS | linear 0 |
| Readable beats (walk, idle, roar) | PASS | beat sheets |
| Readable beats (act) | PASS except scoop | M1 |
| Event names (no `end`) | PASS | |
| Event timings match the plan | PASS | |
| ANIM_REFS rule | **OWNER DECISION** | M2 |

## Not done in this review
- No Blender run and no game run. I did not measure the trunk tip height; the estimate in M1 is from the panels.
- The f0 rest frame was not in the beat sheets, so the rest check is numeric only (M4).
- The raw collision count was not in any file I could read (M5).
