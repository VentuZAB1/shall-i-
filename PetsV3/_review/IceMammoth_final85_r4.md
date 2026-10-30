# Ice Mammoth - FINAL 8.5 GATE, ROUND 4 (2026-10-28, fresh reviewer)

**Model: 8.6/10 - PASS. Clips: 8.6/10 - PASS.**

Both clear the 8.5 floor, but only by a little. Nothing blocks the bar. The items below are for 9+.

## What I looked at
- **Read:** `_review/GLACIER_REVIEWER_BRIEF.md`; `_review/IceMammoth_final85_r3.md` (round 3); `IceMammoth/MODEL_NOTES.md` and `CLIP_NOTES.md` ("Final gate round 3" sections); `_scratch/verify.json`, `_scratch/full_step1.txt`, `_scratch/export_result_f85r3.txt`.
- **Timestamps:** the newest set is the one the brief names. `pclose_side_roar_34.png`, `pclose_front/tq/below_roar_34.png` at 04:40; `_model_sheet.png`, `_close_sheet.png`, `_roar_mouth.png` at 04:41; `_beats_f85r3_act_tq/side.png` at 04:41; icon strips at 04:43. The FBX export is at 04:42. Pet file ~04:38 per the title bars. I did not use `_scratch/idle_mouth.png` (04:44), which is not in the gate set.
- **Images read (all loaded):** `pclose_side_roar_34` (420 px native); `_roar_mouth` (side, front, below, tq at f34 and f50); `_model_sheet` (tq, front, side, back, game, under); `_close_sheet` (close_tq, close_front, close_side); `_beats_f85r3_act_tq` and `_act_side` (f10 to f100, every hold frame); `_icons_strip_64` and `_128`; `_ALL_FIERCE_progress` for distinctness.
- **Limits:** no zoom or upscale tool was available, and PIL is not installed, so I could not count the dark mouth pixels. The CM1b ratio (0.55) is the builder's measurement. I checked it by eye only and it looks consistent with that. Judgments are from native-size images. The breath, the f40 ear flap and the roar tremble are not visible at sheet scale, and I say so below.

## MODEL: 8.6 / 10 - PASS

**Strong:** the mammoth reads at 64 px and 128 px. It is the only aqua body in the strip, next to the Yeti, Raiju, Bramble Badger, Frostfang Lynx and Mossback. The dome, the pale tusks with mint caps and the ridged trunk are clear. The eyes are narrow teal slits in black sockets under dark brows, which reads fierce, not cute. Both legs have a dark cuff band with a jagged hem. The soles are dark. The pale underside shows in `under`. Tris 14,688 (cap 15k), no glow meshes.

**Held back from 9:** the body is still a light sky-blue (lead's call, not scored). The flanks read as a regular repeat of the lock rows. The belly fringe reads a little like a row of teeth from the side. The pale belly plate is still a plate, only broken at its lower edge.

## CLIPS: 8.6 / 10 - PASS

**Strong:** the roar mouth now shows from the side. In `pclose_side_roar_34` a dark band sits between the cheek block and the dropped chin block. It is clearly visible, not a sliver. The `_roar_mouth` panels show a dark interior from front, below and 3/4. The act flick now passes over the head: in `_beats_f85r3_act_side` the trunk arcs above the dome line at f44 to f58, and the tip peaks at about the top of the dome at f56. The scoops reach the snow at f20 and f64 to f82, with the tip on the ground in `_act_tq`.

**Held back from 9:** from a pure side camera, the near tusk root and the cheek still cover part of the mouth, so the opening reads as a gap rather than a clear open mouth. The breath and f40 ear flap are not visible at sheet scale. The roar tremble does not show in stills. The act's max swing of 53.7 deg is still close to the 60 cap.

## Round-3 check

| round-3 item | result | evidence |
|---|---|---|
| **CM1b** roar mouth from the side, f30-50 | **PASS** | `pclose_side_roar_34` shows a clear dark band between the cheek and the chin. `_roar_mouth` side panels at f34 and f50 agree. Builder measures the band at 0.55 of the chin height (target >= 0.25). I could not count pixels (no PIL), but the band reads at about that scale by eye. Jaw max 22.0 @ f34 (within 22). Head pitch-up 16.0 (within 30). `collision_free: true`. |
| **9+ 1** pupil removed | **PASS** | `_close_sheet` (tq, front, side): the teal slit is one line in a black socket. No pupil block. |
| **9+ 2** belly lip / slab | **PARTIAL** | `_model_sheet` `model_side`: five short WOOL_D locks per side hang off the belly edge and break the plate's bottom line. The pale band is still a flat plate. Better than round 3, but not fully a wool edge. |
| **9+ 3** brows darker | **PASS** | `_close_sheet` shows the brows in a darker blue-grey (BROW_D 64,84,96) that reads as a scowl. |
| **9+ 4** mid lock row variation | **PARTIAL** | Variation was raised to 0.12 per notes. In `model_side` the middle row still reads as a regular repeat. Not a visible change at this scale. |
| **9+ 5** cuff hems jagged | **PARTIAL** | The hems read as a dark band with a broken edge at sheet scale. Not checkable at 5 studs. |
| **Clip 1** act flick over the brow | **PASS** | `_beats_f85r3_act_side` f44 to f58: the trunk crests above the dome line. Head pitch-up 17.0, max swing 53.7, both within limits. |
| **Clip 2** ear and breath at 5 studs | **PARTIAL** | Numbers only: ear flap f40 = 10, idle breath chest 2.0. Not visible at sheet scale. Needs a Studio check at game distance. |
| **Clip 3** roar tremble | **PARTIAL** | ±3 deg in the notes. Not visible in stills. Check at game speed. |
| **Clip 4** one-frame swing | **PASS** | Max 53.7 (f76, FX_SnowSpray), under 60. Builder re-checked in step-1 JSON. |

## Numbers (from `verify.json` and `full_step1.txt`)
- Collision-free: true (`collisions: {}`, hinge-free crossings 0 with the throat hinge).
- ground_min_z: idle 0.018, walk 0.015, roar 0.018, act -0.016. All >= -0.02.
- Loops closed, walk slide 0.0. Roar and act end at rest 0.0.
- Neck max 0.6 / 0.8 / 2.0 / 3.0. Chest vs spine 2.0 / 1.68 / 1.0 / 0. Head pitch-up roar 16.0, act 17.0. Jaw max roar 22.0 (f34), act 2.0.
- Scoop holds: FX_SnowSpray 0.010 (f18-22) and 0.0111 (f64-68, f78-82). Min 0.0087 at f23.
- Tris 14,688 (cap 15k). HEIGHT 9.0.

## MUST (blocking 8.5)
None. Both scores clear 8.5 on the evidence above.

## TO 9+ (in order of impact)
**Model**
1. **Belly pale plate.** The BELLY_PALE band still reads as a flat plate in `model_side`. Break its top edge with 2 stud-rows of WOOL_D or raise the lower-edge fringe to 7 locks per side. Round 3 found the top strip was hidden under the lowest lock row. Check the cost in tris (14,688 now, cap 15k).
2. **Flank rows.** The middle lock row still repeats regularly. Vary its height as well as its length (about ±0.02 units), so the row has no rhythm.
3. **Brow shade.** The brows are right, but in `close_front` they still read a light grey-blue at the outer ends. Darken the outer 30% of each brow slab a further step (about 56,72,84).
4. **Light body.** Not scored (lead's call). If the owner asks for a darker body later, the fallback (72,140,164) still applies.

**Clips**
1. **Mouth from a pure side.** The near tusk root covers the front of the dark opening. Move the MOUTH_IN interior about 0.01 further back, so the opening shows past the tusk root from a straight side view.
2. **Ear and breath at 5 studs.** Check in Studio at game distance. If invisible, raise the f40 ear flap from 10 to about 12, as round 3 asked.
3. **Roar tremble.** Keep the ±3 deg tremble, but check it at game speed.
4. **Act swing.** 53.7 is near the 60 cap. Check in the game clip for any snap on f76.

## Pass / fail checklist (round 4)

| check | result | note |
|---|---|---|
| **MODEL** | | |
| Tris <= 15k | PASS | 14,688 |
| HEIGHT 9.0 | PASS | export `height: 9.0` |
| Species reads at 64 px and 128 px | PASS | `_icons_strip_64` / `_128` |
| Studded body, head, legs, trunk | PASS | `_model_sheet`, `_close_sheet` |
| No glow / no Neon | PASS | `tris_glow` empty |
| Distinct next to the other pets | PASS | `_icons_strip_128`, `_ALL_FIERCE_progress` |
| Eyes: narrow slit in a black socket, one line | PASS | `_close_sheet` |
| Brow reads as a scowl | PASS | `_close_sheet` |
| Legs: second-colour cuff on each leg | PASS | `_model_sheet` |
| Pale underside visible | PASS | `under` |
| Tusks and mint caps read at 64 px | PASS | `_icons_strip_64` |
| Floating, poking or intersecting parts | PASS | 6 views plus `under` |
| **CLIPS** | | |
| collision_free, all 4 clips | PASS | `verify.json` / step 1 |
| ground_min_z >= -0.02 | PASS | act -0.016 |
| Loops closed, walk slide 0 | PASS | step 1 audit |
| Roar and act end at rest | PASS | 0.0 both |
| Neck <= 8, chest vs spine <= 5 | PASS | see numbers |
| Head + neck pitch-up <= 30 | PASS | roar 16.0, act 17.0 |
| Jaw max <= 22 | PASS | 22.0 @ f34 |
| Max adjacent swing <= 60 | PASS | 53.7, near the cap |
| Scoop holds: FX_SnowSpray <= 0.012 | PASS | 0.010 / 0.0111 |
| Scoops read as contact | PASS | `_act_tq` f80 |
| Roar open mouth readable from the side | PASS | CM1b (`pclose_side_roar_34`) |
| Act flick passes over the head | PASS | `_beats_f85r3_act_side` f44-58 |
| Idle readable at 5 studs | PARTIAL | trunk yes; ear and breath not at sheet scale |
| Acts in place, no spins | PASS | |
| ANIM_REFS rule | OWNER DECISION | not scored |

## Summary
- **Model: 8.6/10, PASS.** Pupil gone, brows darker, belly fringe added. The pale belly plate is still a plate.
- **Clips: 8.6/10, PASS.** Side mouth reads, and the act flick passes over the brow.
- **Result:** both clear the 8.5 floor with no MUST items. The 9+ list is the next step.
- **Unverified at sheet scale:** ear and breath at 5 studs, the roar tremble, and the mouth pixel ratio (I could not count pixels).
