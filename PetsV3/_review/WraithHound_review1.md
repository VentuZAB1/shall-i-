# Wraith Hound - model gate review 1 (2026-10-27) - REVISE (model)

**Score: 6/10 for a 10 % medium-high** (the plan review was also 6/10). Ship bar is 8/10.

The bones of this model are good: a lean, long-wedged hound, studs on the whole surface, narrow slit eyes under heavy brows, no glow, 6,820 tris. It is also clearly not a sibling copy: the lavender hide and blue-tipped mane are their own read.

It fails the thing the plan was built around, the **ghost**. The soot is not a saddle on top of a pale body. It covers most of the torso, so the body reads as a dark-backed wolf with pale legs. The game camera confirms it: the pet is 58 % soot in game, against a plan of 26 %. The mane also reads as Raiju-style back spines, not smoke.

Four MUSTs fix it, all as code changes to `pets/WraithHound.py`. None changes a bone name or a joint, so the clip work is not affected. One MUST (M0) is a waiver the lead needs to decide.

## What I looked at
- Rules: `Creature Style.md`, `Model Review Checklist.md`, `FIERCE_GUIDE.md`; the owner decisions in `GLACIER_CONCEPTS.md`; the plan `_review/WraithHound_plan.md` (v2) and `GLACIER_PLAN_REVIEW.md` section 2.11 with rulings 5 and 9; the format of `VenomBasilisk_review2.md`.
- Builder files: `pets/WraithHound.py`, `WraithHound/MODEL_NOTES.md`, `renders/_shares.json`.
- Wraith renders: `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `flat_side.png`, `flat_game.png`, `flat_tq.png`, `model_tq.png`.
- Comparisons: the `_model_sheet.png` of ShadePanther, BlackDragon, NightmareStallion, Raiju and Cerberus, and the lineup `_ALL_FIERCE_progress.png`. PharaohAsparuh and AbyssWeaver are judged from the icon strips only, not their sheets.
- My own read-only checks (no Blender, no Studio):
  - a palette-ID pixel count on `flat_side.png` (flat render, no lighting);
  - hue angles computed from the RGB values in each pet file.

## Measured
**Flat side render, palette-ID pixels (non-background):**

| region | SOOT | ASH_LAV | MIST | reading |
|---|---|---|---|---|
| torso band (x150-240, y172-208) | **84 %** | 16 % | 0 | the body is dark |
| legs (x130-300, y215-290) | 3 % | **75 %** | 22 % | the ghost lives here |
| tail (x290-400, y150-300) | **85 %** | 15 % | 0 | a dark plank |
| neck + head (x60-150, y120-175) | 59 % | 35 % | 2 | the mane root bleeds in |

**Builder's whole-view shares (`_shares.json`) against the plan:**

| | side | tq | game | plan side |
|---|---|---|---|---|
| SOOT | **48.7** | 40.2 | **57.8** | 26 |
| ASH_LAV | 32.3 | 35.2 | **24.8** | 40 |
| MIST | 9.8 | 16.0 | 5.6 | 12 |

**Why the torso is dark (`pets/WraithHound.py` L127-129):** `upper()` cuts the soot slab at a z of -0.092 (rib, waist) and -0.094 (waist) and -0.092 (hips). That leaves the soot on the top portion of each torso block:
- chest 71 %;
- waist 90 %;
- hips 81 %.

That is not a top layer, it is the flank. MODEL_NOTES says "the body still reads lavender: head, neck, lower flanks and legs". The lower flank is only the 9 % sliver below the MIST cut at L131.

**Hue (H, degrees; HSV from the RGB in each file):**

| colour | H | distance from WH INDIGO (H 231) |
|---|---|---|
| WH INDIGO (100,120,240) | 231 | - |
| Raiju FUR (80,102,182) | 227 | **4** |
| BlackDragon INK (78,68,158) | 247 | 16 (the v2 note said 9) |
| BlackDragon MANE (146,84,236) | 265 | 33 |
| ShadePanther VIOLET (170,80,255) | 271 | 40 |

**Heights (studs):** Wraith 8.0. For comparison: ShadePanther 7.0, Raiju 8.0, Cerberus 8.5, BlackDragon 9.0, NightmareStallion 9.0.

---------------------------------------------------------------------------------------------------------------------
## 1. Your five questions

1. **64 px ghost-hound read: species YES, ghost NO.** The strip shows a canid: long wedge head, tall pinned ears, a row of dorsal spines, a long tail. It reads as a pale wolf with a black back. It does not read as a ghost. **Fail (M1).**
2. **Distinct from Raiju, Cerberus, ShadePanther: partly.**
   - Cerberus (three heads) and ShadePanther (crystal cat) are clearly different. The Void-egg dark pets (Panther, Stallion, Dragon) are dark violet or charcoal; the Wraith is lilac-ash.
   - **Raiju is not clear.** Raiju is a blue wolf with a row of dark dorsal spines and tall ears. The Wraith uses the same recipe (canid, spines, ears), and its blue spike tips sit 4 degrees from Raiju's body hue. The only thing that separates them is the mane, and at present the mane reads as Raiju's spines (M3). **Fail (M3, M4).**
3. **Is the soot share too high, is the ghost lightness lost?** **Yes, both.** 48.7 % whole-view soot (plan 26), 84 % of the torso band is soot, and the pet is 58 % soot in game. The light parts are the legs, the head and the neck; the torso is a dark box. **Fail (M1, M2).**
4. **Does the indigo read next to the Void violets?** **Yes.** It reads as cornflower blue, not violet, in `game_view.png` and the 128 px strip. It sits 40 degrees from ShadePanther VIOLET and 33 degrees from BlackDragon MANE. The plan's separation holds. The new clash is Raiju (4 degrees). **Fix M4.**
5. **Plan review ruling 5 allowed the ash body only "tinted, with a dark saddle".** The tint passes: ASH_LAV is H 253, S 0.22, a lilac ash, and it is not plain grey. The dark saddle does not pass: the dark area is the torso itself, not a saddle on top of it. **Exception not met.**

## 2. Deviations, ruled
- **Soot as the "top layer" of each torso block:** the mechanism is accepted, the coverage is rejected. A top layer of about 40 % of each torso block is a saddle. 71-90 % is a dark body. **M1.**
- **Mane as three rows of swept soot wisps with indigo points:** accepted over the plan's round blocks (round puffs read as fingers, as the builder said). The angle is rejected: the centre wisp rises at about 73 degrees (`d0 = (0, 0.30, 1.0)`, L79) and the back wisp at about 63 degrees (L80), so the rows read as dorsal spines. **M3.**
- **Mist socks and paws:** the paws are accepted (the mist at the feet ghosts well). The front sock climbs the lower 36 % of the shin (L194) and reads as a white boot. **NICE 1.**
- **Soot leg caps (`_scratch/WraithHound_legcaps.py`), rejected:** I agree they stay rejected, since they read as dark pauldrons in front. I did not open the scratch file.
- **Undisclosed deviation: the tail.** Plan section 5 says a lavender-root tail with a SOOT tuft at the tip. Built: lavender on segment 1 only, soot on segments 2 to 4 (L209), plus a soot tuft (L211). The tail is 85 % soot in side view. **Reject, M2.**
- **Elbow at 0.33H (plan 0.42H), withers 0.72H:** accepted. The builder's reasoning holds, and the lean hound still reads.

---------------------------------------------------------------------------------------------------------------------
## 3. MUST (priority order)

**M0 - decision for the lead, not a code change.** The plan's "saddle at least 18 % of side" (review 2.11 MUST 2) cannot hold with a pale torso. The builder met 18.8 % only by covering the torso. Recommend the minimum becomes **10-14 %** (the dark top third of the torso plus the mane roots). Record the waiver in the plan.

**M1 - torso soot cut (pets/WraithHound.py L127-129).** The soot should cover the top ~40 % of each torso block, not 71-90 %.
- L127 `upper(B, rib, -0.092, sad)` becomes `upper(B, rib, 0.043, sad)`.
- L128 `upper(B, waist, -0.094, sad)` becomes `upper(B, waist, 0.024, sad)`.
- L129 `upper(B, hips, -0.092, sad)` becomes `upper(B, hips, 0.030, sad)`.

Leave the MIST cut at L131 as it is. Expect the saddle to fall to about 10 % and SOOT to about 40 % total. Re-measure. The lavender flank then reads from mid-body down.

**M2 - tail to the plan (L209).** `ASH_LAV if i == 0 else SOOT` becomes `ASH_LAV if i < 2 else SOOT`: Tail1 and Tail2 lavender, Tail3 soot. Keep the soot tuft at Tail4 (L211). This takes roughly 3-4 points off the SOOT share and makes the tail read as a pale plume with a dark tip.

**M3 - the mane must lean back (L79, L80, and the side wisps at L84).** The steep `d0` vectors make the wisps stand up like spines, the Raiju read. Change:
- L79 centre wisp `(0, 0.30, 1.0)` becomes `(0, 0.85, 0.55)`, about 33 degrees above horizontal;
- L80 back wisp `(0, 0.50, 1.0)` becomes `(0, 0.95, 0.42)`;
- L84 side wisp `(s_ * 0.40, 0.40, 1.0)` becomes `(s_ * 0.55, 0.85, 0.60)`.

Leave the tail vectors (`d1`) alone. The target is a streaming plume, not stacked blades. Check it at 64 and 128 px next to Raiju.

**M4 - indigo hue off Raiju's body (L19-20).**
- INDIGO `(100, 120, 240)` becomes **`(112, 120, 240)` #7078F0** (H 236).
- INDIGO_L `(160, 176, 255)` becomes **`(176, 184, 255)` #B0B8FF** (H 234).

Keep the value at 240. The brightness (V 240 against Raiju's V 182) is what separates the accent from Raiju's body. The new hue is 9 degrees from Raiju, 10 from BlackDragon INK, 28 from BlackDragon MANE and 35 from ShadePanther VIOLET.

## 4. NICE
1. **Front sock (L194):** `A + (K - A) * 0.36` becomes `* 0.18`. The white reads as boots at the current length. Keep the rear paw socks at L201.
2. **Chest plate (L133):** the half-width `0.122` becomes `0.090`. From the front the white plate reads as a slab across the chest, not a throat.
3. **Muzzle:** the upper muzzle MIST seg in the head block (about L136-140) reads as a white husky muzzle. Make the upper muzzle ASH_LAV and keep MIST on the lower jaw only. Lengthen the ivory fangs from 0.062 to about 0.075 (L145-149) so the mouth reads fierce in close-up.
4. **Eyes at 64 px:** the indigo slit (L162, 0.033 x 0.0095) vanishes at 64 px. Enlarge it to about 0.038 x 0.012 and the rim (L160) to about 0.043 x 0.014. Keep the black socket.
5. **Underline:** the side-view belly reads nearly level from chest to hips, by my eye about 8 px of rise in a 400 px frame. Raise the waist block centre from z 0.755 to about 0.775 (L121) so the underline rises toward the flank.
6. **Height:** 8.0 is shorter than NightmareStallion (9.0), but the plan said the Wraith should look bigger than the Stallion. Once M3 lifts the mane, consider 8.5 with a `HEIGHT` change only. Optional.
7. **Under-view:** no belly or underside render was supplied. Send one with the next sheet (belly, mist socks, tail underside).

---------------------------------------------------------------------------------------------------------------------
## 5. Pass / fail checklist

| check | result |
|---|---|
| 64 px: species reads (canid, wedge head, ears, spines) | PASS |
| 64 px: ghost reads | **FAIL** (M1) |
| 128 px: mane reads as streaming smoke, not spines | **FAIL** (M3) |
| Fierce face: slit eyes under heavy brow, no googly eyes, no smile | PASS (eyes need NICE 4 at 64 px) |
| Whole surface studded, details smooth, no Neon or glow | PASS |
| Tris <= 15k (6,820) | PASS |
| Dark body + pale underside + one accent (ghost exception) | **FAIL** (M1, with M0 waiver) |
| SOOT <= 38 % side (plan 26 %) | **FAIL** (48.7 %) - re-measure after M1 + M2 |
| Saddle >= 18 % (plan) | met (18.8 %) only by covering the torso - see M0 |
| Accent distinct from Void violets | PASS (33-40 degrees) |
| Accent distinct from Raiju | **FAIL** (4 degrees) - M4 |
| Tail per plan (pale root, soot tip) | **FAIL** (M2) |
| No box belly, no plastic-toy slabs | PARTIAL (chest plate NICE 2, flat underline NICE 5) |
| Rarity: bigger and stranger than the Stallion (plan 2) | soft FAIL (8.0 vs 9.0) - NICE 6 |
| Floating or poking parts (four views) | PASS (ears, chest plate and paws attached); under-view not checked (NICE 7) |
| Rarity fit (10 %, no hero piece) | PASS if M1-M4 land |

**Estimates, not measured:** after M1 and M2 I expect SOOT ~36-40 %, the saddle ~10 %, and ASH_LAV + MIST ~48-53 %. Re-measure with the same palette-ID method. Gate: SOOT <= 38 %, ASH_LAV + MIST >= 48 %.

**Round 2 packet:** `_model_sheet`, `_close_sheet`, the 64 and 128 px strips (Wraith first, next to Raiju, ShadePanther and BlackDragon), `flat_side`, `game_view`, the under-view, and the value shares in `_shares.json`.
