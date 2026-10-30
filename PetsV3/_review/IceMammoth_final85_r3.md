# Ice Mammoth - FINAL 8.5 GATE, ROUND 3 (2026-10-28, fresh reviewer)

**Model: 8.5/10 - PASS. Clips: 8.4/10 - FIX.**

Model is at the 8.5 floor, with no margin. Clips stay under the bar because the roar's open mouth still does not read from the side (CM1), and it does not read at game distance from any angle. Everything else in the clip gate passes on the numbers.

## What I looked at
- **Read:** `_review/GLACIER_REVIEWER_BRIEF.md`; `_review/IceMammoth_final85_r2.md` (round 2); `IceMammoth/MODEL_NOTES.md` and `CLIP_NOTES.md` ("Final gate round 2" sections); `_scratch/verify.json`; `_scratch/export_result_f85r2.txt`.
- **Model (newest set, rendered 03:47-03:51):** `renders/_model_sheet.png` (tq, front, side, back, game, under); `renders/_close_sheet.png` (close_tq, close_front, close_side); `renders/_flat_sheet.png`; `renders/_icons_strip_64.png` and `_128.png`; comparison `PetsV3/_ALL_FIERCE_progress.png`.
- **Mouth:** `renders/_roar_mouth.png` (pclose_side idle/roar 34/roar 50, pclose_tq roar 34, pclose_front idle/roar 34, pclose_below idle/roar 34) and `renders/pclose_side_roar_34.png` (420 px, native).
- **Clips:** `renders/_beats_f85r2_irw_side.png` and `_irw_tq.png` (idle, roar f0-66, walk f0-30); `renders/_beats_f85r2_act_side.png` and `_act_tq.png` (f10-100, every scoop hold).
- **Limits:** I could not zoom or upscale. Judgments are from native-size sheets. The cuff hems, the ear flap at f40 and the breath are only checkable at this scale, so they are marked as such. The throat hinge is from the 10-27 round and was not part of this round's changes. I did not re-judge it beyond the step-1 `collision_free: true`.
- **All images loaded.**

## MODEL: 8.5 / 10 - PASS (at the floor)

**Strong:** the species reads at 64 px and 128 px (the only aqua body in the strip, next to the Yeti, Raiju, Bramble Badger, Frostfang Lynx and Mossback). The dome, pale tusks with mint caps, the ridged trunk and the dark mane are clear. The stud skin is even. The brow shelves overhang the eyes and read as a scowl (`_close_sheet`). Both legs now show a dark second-colour band (`_model_sheet`). The pale underside shows in `under`. The feet have dark soles. Tris 14,272 (cap 15k). No glow meshes (`tris_glow` is empty).

**Held back from 9:** the body is still a light sky-blue with a uniform stud grid, so the fierce read rests on the brows, tusks and mane. The lead ruled the colour is not scored. The eye slit is split into two teal blocks by the black pupil, so from the front it reads a little like a visor. The pale belly reads as a flat slab in `model_side`. Details are in the TO 9+ list.

## CLIPS: 8.4 / 10 - FIX

**Strong:** the idle trunk swing is visible across f0, f20, f40, f60 and f80 in both views. The roar reads as a trumpet: the trunk rises to the sky by f16, the head is up 16 deg, and the trunk holds f22-50 (`_beats_f85r2_irw_side`). The act reads as a sequence: a scoop, the trunk lifting over the head at f44, a flick back at f56, and the tip on the snow at f80 (`_beats_f85r2_act_tq`). Every number in `verify.json` is inside its limit (see the checklist). The walk f10-30 shows no visible clipping at sheet scale.

**Held back from 9:** the roar mouth (CM1, below). The act flick peaks at head height (f44-56) and never goes over the back, which the act name implies. The breath and the f40 ear flap are not visible at sheet scale.

## Round-2 MUST check

| round-2 item | result | evidence |
|---|---|---|
| **MM1** leg cuffs as a band | **PASS** | `_model_sheet` `model_side` and `model_tq` show a dark band on the upper half of all visible legs, with a jagged hem. WOOL_D side share 30.1 %. Walk f10-30 in `_irw_side`: no clipping at sheet scale. Step 1 `collision_free: true`. The band reads more as a dark sleeve than a stripe; it is clear, though. |
| **MM2** eye: black frame on both ends | **PASS** | `close_front`: black at both ends of the teal slit and above and below it. The slit no longer fills the socket. `close_tq` and `close_side` show the same. Note: the pupil splits the slit into two blocks (TO 9+). |
| **CM1** roar mouth from the side, f26-50 | **FAIL from the side; PARTIAL in 3/4 and front** | `pclose_side_roar_34`: a dark gap a few pixels tall between the tusk root and the chin block. `_roar_mouth` side roar 34 and 50 show the same. `pclose_tq_roar_34` shows a clear dark cavity under the tusk root. `pclose_front_roar_34` shows a dark opening under the trunk root. From the below view it is a small dark wedge. Jaw max 20.0 (within 22), head pitch-up 16.0 (within 30), both PASS. |

## Round-2 TO 9+ check

| item | result | note |
|---|---|---|
| 1. Eye after MM2 | PASS | The bright slit still reads at `model_tq` and `model_front`. The split by the pupil is a TO 9+ below. |
| 2. Breath and ears | PARTIAL | Numbers: idle chest vs spine 2.0 (`verify.json`). Ear flap f40 = 10 (builder). Neither is visible at sheet scale. Needs a 5-stud check in Studio. |
| 3. Body colour | Lead's call | Not scored. Still reads light in the strip. |
| 4. Walk cuffs f10-30 | PASS | `_irw_side` walk f10/15/20/25/30: no visible shin clipping at sheet scale. |
| 5. Roar tremble | PARTIAL | ±3 deg (builder). Stills do not show it; the trunk hold reads as a trumpet anyway. |

## Pass / fail checklist (round 3)

| check | result | note |
|---|---|---|
| **MODEL** | | |
| Tris <= 15k | PASS | 14,272 (`tris_body`) |
| HEIGHT 9.0 | PASS | export `height: 9.0` |
| Species reads at 64 px and 128 px | PASS | `_icons_strip_64` / `_128` |
| Studded body, head, legs, trunk | PASS | `_model_sheet`, `_close_sheet` |
| No glow / no Neon | PASS | `tris_glow` empty |
| Body reads as its own pet next to the others | PASS | `_icons_strip_128`, `_ALL_FIERCE_progress` |
| Body reads dark rich, fierce | PARTIAL | lead's colour call; not scored |
| Eyes: narrow slit in a black socket | PASS | MM2 |
| Brow reads as a scowl | PASS | `_close_sheet` |
| Legs: second-colour band on each leg | PASS | MM1 |
| Pale underside visible | PASS | `under`, `_model_sheet` |
| Tusks and mint caps read at 64 px | PASS | `_icons_strip_64` |
| Floating, poking or intersecting parts | PASS | 6 views plus `under`; throat hinge from earlier round, step-1 clean |
| **CLIPS** | | |
| collision_free, all 4 clips | PASS | `verify.json` / export: `collision_free: true`, `collisions: {}` |
| ground_min_z >= -0.02 | PASS | act -0.016 (f24) |
| Loops closed, walk slide 0 | PASS | export audit: loop_pos 0, loop_rot 0, slide 0.0 |
| Roar and act end at rest | PASS | 0.0 both |
| Neck <= 8, chest vs spine <= 5 | PASS | neck 0.6 / 0.8 / 2.0 / 3.0; chest 2.0 / 1.68 / 1.0 / 0 |
| Head + neck pitch-up <= 30 | PASS | roar 16.0, act 17.0 |
| Jaw max <= 22 | PASS | roar 20.0 (f34) |
| Max adjacent swing <= 60 | PASS | 53.7 (act f76), near the cap |
| Scoop holds: FX_SnowSpray <= 0.012 | PASS | 0.010 (f18-22), 0.0111 (f64-68, f78-82); min 0.0087 at f23 |
| Scoops read as contact | PASS | `_act_tq` f80, the tip on the snow |
| Idle readable at 5 studs | PARTIAL | trunk yes; ear and breath not at sheet scale |
| Roar open mouth readable from the side | **FAIL** | CM1b |
| Acts in place, no spins | PASS | |
| ANIM_REFS rule | OWNER DECISION | not scored, as in round 2 |

## New MUSTs (blocking 8.5 on clips)

**Model:** none. The model clears the 8.5 floor.

**Clips**
- **CM1b. The roar mouth must show from the side at the peak (f30-50).** Current: `pclose_side_roar_34` shows only a sliver of dark between the tusk root and the chin block, a few pixels tall at 420 px. Direction: (a) in the roar keys, drop the jaw at f34 from 20 to 22 deg (the 22 deg cap); (b) move the dark MOUTH_IN interior about 0.03 units forward (toward the front of the chin) so its front edge clears the underside of the tusk root. Target: in `pclose_side_roar_34` the dark opening is at least a quarter of the chin block's height. Check: `pclose_side_roar_34` and `_roar_mouth` side panels show the dark opening from the side; jaw max <= 22; head pitch-up 16.0; `collision_free` stays true.
- If the mouth cannot show from the side without moving the trunk root, the lead may decide the roar reads through the trunk and the head and that the mouth is not needed. That is the lead's call. Under this brief the item stays FAIL.

## TO 9+ (in order of impact)

**Model**
1. **Eye pupil.** The black pupil (0.008 x 0.004 x 0.011) splits the teal slit into two blocks, so it reads like a visor. Narrow the pupil to 0.004 wide or remove it, so the slit reads as one line of teal.
2. **Pale belly.** In `model_side` the BELLY_PALE band reads as a flat plate between the legs. Give its lower edge a 0.02-unit wool lip, or break its top edge with 2 stud-rows of WOOL_D, so it reads as wool, not a slab.
3. **Brows.** The brow slabs read a light grey-blue in `model_tq`. Shade them to WOOL_D (64,84,96 family) so the scowl is darker and the body reads more fierce.
4. **Flank rows.** The middle lock row is still regular in `model_side`. Raise its length variation from 0.08 to about 0.12.
5. **Cuff hems.** Confirm at 5 studs that the hem reads as a jagged edge, not a flat top. (The hem is only visible at native size.)

**Clips**
1. **Act flick.** The flick crests at head height (f44-56). Either raise the crest by about 5 deg so it passes over the brow, or rename the act to match what it does.
2. **Ear and breath at 5 studs.** The f40 ear flap (10) and the idle breath (2.0) are not visible at sheet scale. Check in Studio at game distance; if invisible, raise the ear amplitude to about 12.
3. **Roar tremble.** The ±3 deg tremble does not show in stills. Keep it, but check the hold at game speed.
4. **One-frame swing.** The act's max swing of 53.7 deg is near the 60 cap. Re-check in the game clip for a snap.

**Lead's items (not scored)**
- Body colour (80,150,176) reads light in the strip. Decision in Studio at 5 studs; the brief's fallback (72,140,164) still applies.
