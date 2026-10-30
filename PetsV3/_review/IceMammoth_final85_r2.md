# Ice Mammoth - FINAL 8.5 GATE, ROUND 2 (2026-10-28, fresh reviewer) - FIX

**Model: 8.0/10 - FIX. Clips: 8.3/10 - FIX.**

Both are below the 8.5 floor. Round 1 was 7.5 model and 8.0 clips. The round-1 MUSTs were carried out and most of them now show in the renders. Three things remain: the leg cuffs read as dark patches, the eye slit fills its socket, and the roar mouth is still hidden from the side. The MUST list below has three items.

## What I looked at
- **Read:** `_review/GLACIER_REVIEWER_BRIEF.md`; `_review/IceMammoth_final85.md` (round 1); `IceMammoth/MODEL_NOTES.md` and `CLIP_NOTES.md` (final85 sections); `IceMammoth/ANIM_REFS.md`; `_scratch/verify.json`; `_scratch/export_result_f85.txt`; `_review/IceMammoth_plan.md`; `pets/IceMammoth.py` (palette L17-27, eye L188-198, cuff() L83-105 and its call L329, legs L314-330, mouth L206-211, roar keys L511-536). Vault: `06 Modelling and Art/Creature Style.md` and `Model Review Checklist.md`.
- **Model images (`IceMammoth/renders/`):** `_model_sheet.png` (tq, front, side, back, game, under), `_close_sheet.png` (close_tq, close_front, close_side), `_flat_sheet.png`, `_roar_mouth.png` (pclose_below/front/side at idle, roar 34 and roar 50), `_icons_strip_128.png`, `_icons_strip_64.png`, `IceMammoth_icon.png`. Comparison: `PetsV3/_ALL_FIERCE_progress.png`.
- **Clip images:** `_beats_f85_irw_side.png` and `_irw_tq.png` (idle, roar, walk); `_beats_f85_act_side.png` and `_act_tq.png` (dust-over); single frames `beat_f85_act_side_act_dustover_020.png`, `_066.png` and `beat_f85_act_tq_act_dustover_080.png`.
- **Limits:** I could not zoom or upscale the sheets (no image library is available to a reviewer), so the judgments are from the native-size images. Numbers come from `verify.json` and the export result.
- All images loaded.

## MODEL: 8.0 / 10

**Strong:** the species reads at 64 px and at 128 px. The dome, the pale tusks with mint caps, the ridged trunk and the dark mane are clear. The stud skin is consistent. The pale belly shows from below (`under`, `_model_sheet`). The brows read as a scowl (`_close_sheet`). The icon is the only aqua body in the strip (`_icons_strip_128`). It is clearly its own pet next to the navy Raiju and ThunderBull, the grey Bramble Badger, the olive Tortoise and the lavender Yeti. Tris 14,272 (cap 15k).

## CLIPS: 8.3 / 10

**Strong:** the idle now moves visibly (the trunk tip is in a different place at f0, f20, f60 and f100 in `_irw_side` and `_irw_tq`). The dust-over reads as a sequence: the trunk reaches down, lifts over the head at f44, and flicks back over the brow at f56 (`_act_side`). At f80 the trunk tip sits on the snow in `_act_tq`. The numbers are within limits.

---

## Round-1 MUST check

| round-1 item | result | evidence |
|---|---|---|
| **M1** body colour (80,150,176), L17 | **PASS on the lead's terms** | The colour changed as asked. In `_icons_strip_128` it reads as its own pet (only aqua body). Fierce read is PARTIAL: the light sky-blue is friendlier than the dark rich body the style asks for, and the fierce read rests on the brows, tusks and mane. Not counted, per the lead ruling. The in-game colour is the lead's Studio check. |
| **M2** eyes: black socket + dark-mint slit | **PARTIAL** | `close_front` shows a black frame and a teal slit, and the white block is gone. But the slit (L195, 0.070 long) fills most of the socket (L193, 0.084), so the black shows only as a thin rim. The bright teal bar with its dark notch reads a little like a visor. See MM2. |
| **M3** shaggy wool cuffs on all four legs | **PARTIAL** | `_model_sheet` `model_side` and `model_tq` show a dark square at each knee, not a band. The cause is in `cuff()` (L83-105, called at L329): the loft runs from -0.10 to 0.25 of the knee-to-ankle length, which is about a third of the shin. The rest of each shin is one aqua column. See MM1. |
| **C1** idle: trunk ±16, ear flap f40, feet planted | **PASS on numbers, PARTIAL on the ear** | Numbers: ground_min_z 0.018, drift 0, collision_free true (`verify.json`). Visible trunk swing in `_irw_side` and `_irw_tq`. The f40 ear flap and the 1.2° breath are not readable at this distance (see TO 9+). |
| **C2** scoops: hold 4 frames each, snow spray <= 0.012, max swing < 60 | **PASS** | `verify.json` track: FX_SnowSpray z 0.010 on f18/20/22, 0.0111 on f64/66/68 and f78/80/82. Act ground_min_z -0.016. Max swing 53.7 at f76. `_act_tq` f80 shows the tip on the snow. The holds read as contact. |

## Round-1 TO 9+ check

| item | result | note |
|---|---|---|
| 1. Scowl brow (-22, -28, z 1.410) | PASS | The brow shelves overhang the slits in `close_front` and `close_tq`. |
| 2. Visible breath (chest 0.5 to 1.2 deg) | PARTIAL | The number changed (`verify.json` chest_vs_spine idle 1.2). It is not visible in the sheets. |
| 3. Open jaw at the roar peak | **FAIL from the side** | `pclose_front_roar_34` shows a thin dark slit under the trunk root. `pclose_side_roar_34` and `_irw_side` roar f34 show the trunk root covering the mouth. See CM1. |
| 4. Colour fallback | Lead's call | Not my decision. |

## Owner decision (not scored)
The ANIM_REFS rule. The idle now cites the `/tags/elephants` clip, which the 2026-10-28 round could read. The roar and act cite the site refs #3, #5 and #9 (`ANIM_REFERENCES_1014.md`, source animationreference.org) and the W0 wolf tag. The walk is a Muybridge plate (733, Wikimedia), not a site clip. Round 1 and round 2 both leave this for the owner to confirm.

---

## MUST (to 8.5 on both)

**Model**
- **MM1. Leg cuffs read as a band.** In `cuff()` (`pets/IceMammoth.py` L91, the ring tuple) change the last ring `(0.25, 0.034, 0.07)` to `(0.50, 0.040, 0.07)`, and the ring `(0.16, 0.026, 0.0)` to `(0.30, 0.030, 0.0)`. The cuff then covers about half of each shin, not a third, with the same jagged hem. Check: `_model_sheet` `model_side` and `model_tq` show a continuous dark band across all four legs, and step-1 `collision_free` stays true.
- **MM2. Eye slit: black frame on both ends.** L195 `(0.070, 0.008, 0.012)` becomes `(0.056, 0.008, 0.009)`. Keep the socket L193 `(0.084, 0.012, 0.028)`. Check: `close_front` shows black at both ends of the slit and above and below it, and the slit no longer fills the socket.

**Clips**
- **CM1. Roar mouth visible from the side at the peak (f26-50).** The Trunk1 root covers the mouth in `pclose_side_roar_34`. Fix: in the roar keys (L536, `Trunk1` loc) add a Trunk1 pitch key of about -10 deg at f30 and hold it to f50, so the root clears the chin. Raise the jaw at f34 (L517) from 18 to 20 deg. Keep the trunk curling to the sky at f22-34. Check: `pclose_side_roar_34` and `_roar_mouth` show the dark mouth interior from the side, `head_pitch_up` stays at 16, `jaw_max` stays at or under 22, and `collision_free` stays true.

## TO 9+ (polish, in order of impact)
1. **Eye.** After MM2, check the slit still reads at 5 studs. The EYE_MINT slit is the brightest spot on the head.
2. **Breath and ears (idle).** The chest breath (1.2 deg, L468) and the f40 ear flap (`8 * bell(f, 40, 6)`) do not read at 5 studs. Raise the chest breath to about 2.0 deg, and the f40 ear amplitude to about 10.
3. **Body colour (lead's Studio check).** The sky-blue body still reads light and cheerful in the strip. If the Studio capture at 5 studs reads toy-like, the brief's fallback (72,140,164) applies. This is the lead's call.
4. **Walk cuffs.** After MM1, check the cuffs at walk f10 to f30 in `_irw_side` so they do not clip the stepping shins.
5. **Roar hold.** The trunk tremble at f26-50 is subtle. A small extra tremble amplitude (±2 to ±3 deg) would make the hold read.

## Pass / fail checklist (round 2)

| check | result | note |
|---|---|---|
| **MODEL** | | |
| Tris <= 15k | PASS | 14,272 (`tris_body`) |
| HEIGHT 9.0 | PASS | builder number |
| Species reads at 64 px and 128 px | PASS | `_icons_strip_64` / `_128` |
| Studded body, head, legs, trunk | PASS | `_model_sheet`, `_close_sheet` |
| No glow / no Neon | PASS | `tris_glow` empty |
| Body reads as its own pet next to the others | PASS | `_icons_strip_128` |
| Body reads dark rich, fierce | PARTIAL | lead's colour call |
| Eyes: narrow slit in a black socket | PARTIAL | MM2 |
| Brow reads as a scowl | PASS | `_close_sheet` |
| Legs: a second-colour band on each leg | **FAIL** | MM1 |
| Pale underside visible | PASS | `under`, `_model_sheet` |
| Tusks and mint caps read at 64 px | PASS | `_icons_strip_64` |
| Floating, poking or intersecting parts | PASS | 6 views plus `under` |
| **CLIPS** | | |
| collision_free, all 4 clips | PASS | `verify.json` |
| ground_min_z >= -0.02 | PASS | act -0.016 |
| Loops closed, walk slide 0 | PASS | `verify.json` audit |
| Roar and act end at rest | PASS | 0.0 both |
| Neck <= 8, chest vs spine <= 5 | PASS | neck 3.0 max, chest 1.68 max |
| Head + neck pitch-up <= 30 | PASS | roar 16, act 17 |
| Max adjacent swing <= 60 | PASS | 53.7 (act f76) |
| Scoops read as contact | PASS | C2 numbers and `_act_tq` f80 |
| Idle readable at 5 studs | PARTIAL | trunk yes; ear and breath no (TO 9+ 2) |
| Roar open mouth readable from the side | **FAIL** | CM1 |
| Acts in place, no spins | PASS | |
| ANIM_REFS rule | OWNER DECISION | see above |
