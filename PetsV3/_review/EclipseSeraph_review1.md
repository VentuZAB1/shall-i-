# Eclipse Seraph - model gate review 1 (2026-10-27) - REVISE

**Score: 5/10 for a 0.1 % MYTHIC** (ship at 8+).

The craft is sound: a clean studded mesh, a fierce face, no box belly, tris inside budget, gold on the hero piece only. It fails the job of the top of the Celestial egg. At icon size it reads as a pale white winged horse with a halo, and it is the palest and least saturated pet in the set. Every fail below is codeable in `pets/EclipseSeraph.py` without a new concept.

Keep: the six-wing count, HEIGHT 11.5, the solid eclipse disc with a gold rim, the red slit eyes, the lilac-ivory head.

**Six-wing gate: PASS (keep six).** See section 2.

---

## What I looked at
- Read first: `_review/EclipseSeraph_plan.md` (v2), `_review/GLACIER_CONCEPTS.md` (OWNER DECISIONS), `_review/GLACIER_PLAN_REVIEW.md` section 2.12, `FIERCE_GUIDE.md`, the vault notes Creature Style and Model Review Checklist, and the format of `VenomBasilisk_review2.md` and `ThornbladeMantis_review2.md`.
- Builder: `pets/EclipseSeraph.py` (425 lines), `EclipseSeraph/MODEL_NOTES.md`.
- Seraph renders: `_model_sheet`, `_close_sheet`, `_idle_sheet`, `_icons_strip_64`, `_icons_strip_128`, `_icons2_strip_64`, `_icons2_strip_128` (upscaled 2-4x to check details), `flat_game`, `flat_side`, `model_side`, `model_back`, `idle_front`.
- Comparison sheets: SolarLion, Griffin, CelestialDragon, Cvetibara, CosmicLeviathan, ThunderRex, FrostcrownDragon `_model_sheet.png`, and `_ALL_FIERCE_progress.png`.
- Clip gate: not part of this round.

Method: object-pixel counts on the renders (background removed, nearest palette match, about +/-3 points). The same method was used for every pet. I did not run Blender. The tri count (10,484) is the builder's figure.

## Measured

### 64 px icon strip (portrait cell, same method for all)
| pet | mean luminance | near-white px (lum > 200) | mean saturation | gold px | red px |
|---|---|---|---|---|---|
| **Eclipse Seraph** | **168** | **42 %** | **0.18** | 42 (4.2 %) | 0 |
| Solar Lion | 133 | 9 % | 0.42 | 267 (21 %) | 1 |
| Griffin | 123 | 4 % | 0.35 | 108 (11 %) | 0 |
| Celestial Dragon | 102 | 6 % | 0.43 | 0 | 0 |
| Cvetibara | 118 | 3 % | 0.31 | 5 (0.4 %) | 1 |
| Cosmic Leviathan (1 %) | 109 | 4 % | 0.35 | 20 (1.9 %) | 0 |
| Frostcrown Dragon (0.1 %) | 159 | 15 % | 0.41 | 73 (4.4 %) | 0 |

- **Game-camera icon** (second cell of `_icons2_strip_64.png`): **8 gold px (1.2 %), 0 red px.** The builder's gate (41 gold px) was measured on the portrait only.
- **Flat game silhouette** (`flat_game.png`, background removed): MOON_IVORY 27.7 %, WING_IN 26.5 % (near-white 54 %), OBSID 25.5 %, IVORY_D 6.6 %, BLACK 4.1 %, GOLD 2.0 %, BLOOD 0.2 %. The builder's table agrees within the method's error.
- **Halo geometry:** the disc is built flat (normal = Z, line 201 `Rt = Rotation(HALO_TILT, X)` on a disc in the XY plane). So it is a plate 20 deg from horizontal, not a disc facing forward. From a level front it is an ellipse of ratio 0.34. From the side it is a diagonal bar (`model_side`, `model_back`). In the game-camera icon it is a thin gold ring.

---

## 1. The lead's concerns, answered

**Pegasus, not lion: confirmed.** Three things make the horse read:
1. The body is a slim, long-legged quadruped with a long bare tail ending in a small black pom (`TAILP` line 34, tail loop line 311). The lion's mass is missing.
2. The head is small against the chest: skull half-width 0.177 (line 237) against chest 0.26 (line 226). The muzzle is 0.10 wide (line 238) and the nose 0.052 (line 242). At icon size the face reads as a small white cat head.
3. The mane is three rings of radial spikes (the `for ring, (r0, L, w, n, ...)` loop, 14/14/16 tufts, 0.05-0.08 wide). At 64 px it is a black sunburst / hedgehog ruff. It is the same radial silhouette the Solar Lion's mane gives, and it is not a lion's mane mass.

Colour adds to it: the whole animal and both wing sets are white, so the pegasus read comes from the colour as much as from the shape.

**Paler and plainer than the Solar Lion: confirmed, and this is the fail.** 42 % near-white pixels against 9 %. Mean saturation 0.18 against 0.42. Saturated pixels (sat > 0.35) 9 % against 68 %. It is the least chromatic pet in the set.

**Body value (the lilac may wash out): both risks are real, in opposite directions.**
- In the icon pipeline the body is near-white (luminance about 171).
- The palette value (232,208,240) has luminance 219, so it passes the 0.6x rule (brightest channel >= 170). At the 0.6x in-game factor it becomes about (139,125,144): a grey-mauve. Low saturation (S 0.13) is why it goes grey and not lilac.
- So the body is white in the icon and grey in game. The fix is a richer mid-lilac on the body, with the ivory kept for the face and underside (MUST 1).

**Red corona and gold amount: too small.**
- Red: 0 px at 64 px in both icons; 0.2 % of the game silhouette. The eyes are small (`eye(..., sc=1.25)`, line 257). The corona band is 0.032 wide (line 217).
- Gold: 42 px in the portrait (passes the >= 20 gate). **8 px in the game camera (fails).** The rim is 0.045 wide (line 207) on a near-flat plate, so it reads as a thin gold line.

**Wing colour blocking: none.** All six wings are WING_IN / MOON_IVORY white with thin OBSID tips (lines 144, 150, 157). That is one white mass with black dashes. There is no mid band. The brief wants three bands: dark (mane, halo, tips) / lilac mid / gold + red. Measured in the flat game render: near-white 54 %, dark 25 %, gold 2 %, no mid band.

**What makes it the jackpot: not yet.**
- It does not outclass Cosmic Leviathan (1 %). The Leviathan is saturated (41 % saturated pixels, purple, blue, gold crown). The Seraph is pale.
- It does not clearly outclass Frostcrown (0.1 %). Both are pale with gold. The Seraph's gold is thinner in game and it is less saturated.
- It does not carry the premium feel of the Solar Lion (common, 54.9 %).

The jackpot needs three hero reads that each land at 64 px in the game camera:
- **gold halo rim:** at least 20 gold px in the game-camera icon (now 8);
- **dark mane mass framing the face:** at least 22 % dark px in the portrait (Solar Lion 22 %, Seraph 15 %);
- **red corona and eyes:** at least 10 red px in the game-camera icon (now 0).

Plus the body split (MUST 1), so the pale is not 54 % of the silhouette.

---

## 2. Six-wing gate: PASS (keep six)

- **Tris:** 10,484 per the builder (target 13k, ceiling 15k). Not re-measured, because reviewers do not run Blender. Within limit.
- **Not a blob:** the three tiers are countable from the back (`model_back`), and the raised upper V and the spread middle pair are countable from the front (`idle_front`).
- **Fallback not triggered:** the written trigger is tris over 15k, or a blob where the six cannot be counted. Neither is met, so the four-wing fallback does not apply and does not need the owner.
- **Caveat (not a fail):** the lower pair is hidden from the front, so it reads only from the back and the game view. At 64 px the icon count is three to four blades. Fix its colour (MUST 1) and let its tips show past the flank (NICE 1). If it is still invisible in round 2, the four-wing question goes back to the owner.

---

## 3. MUST (before clips; in priority order)

**MUST 1 - Body value: split the pale (the main colour fix).**
- Add `BODY_MID = (206,160,232)` #CEA0E8 (H 278, S 0.31, V 0.91; about (124,96,139) in game). Use it for: the chest ribcage (line 226), the tuck (228), hips (229-230), all four legs and shins (296-302), the paws (303), and the tail segments (311).
- Keep MOON_IVORY (232,208,240) for: shoulders (227), neck (235), cranium (237), the muzzle block and nose bridge (238), and the wing arms (135-137). The face and the underside stay the approved colour.
- Wings: the flight feathers of pairs B and C change from WING_IN to lilac (214,186,236) #D6BAEC (line 144 `else WING_IN`, line 157 for B and C). The upper pair's primaries keep WING_IN as the single pale highlight.
- Targets (64 px portrait): near-white (lum > 200) at most 25 % (now 42); mean saturation at least 0.28 (now 0.18).
- **Plan change:** this moves MOON_IVORY from the plan's 40 % to about 25 % of the body. The concept lists one body colour, so the planner must approve it. I recommend yes.

**MUST 2 - Lion read: a mane mass, not a sunburst.**
- Mane tufts (the tuft call in the ring loop, `tuft(B, root, d + Vector((0, 0.42 + 0.12 * ring, 0)), ...)`): lean the tufts back instead of out. Change the lean to `(0, 0.9 + 0.12 * ring, 0)` so the locks sweep back like a lion's mane (+y is back; the face is at -y).
- Tuft counts 14/14/16 to 22/22/24. Widths 0.05/0.065/0.08 to 0.07/0.085/0.10, so the gaps close.
- Chest bib (`# chest bib` loop): 3 tufts to 5. Shoulder cape (`# cape` block): extend it so the dark mass runs down to the chest.
- Keep the mane OBSID. Keep gold OFF the mane: gold stays on the halo only. That is the distinction from the Solar Lion's gold-tipped sun mane.
- Target: dark px (lum < 90) at least 22 % of the 64 px portrait (now 15 %).

**MUST 3 - Head, muzzle, legs and tail: a lion's mass.**
- Skull half-width 0.177 to 0.20 (line 237). Muzzle seg half-width 0.10 to 0.12 (line 238). Nose 0.052 to 0.066 (line 242). A square lion muzzle, not a cat's.
- Forelegs: half-widths 0.112 / 0.148 to 0.13 / 0.165 (line 296). Paws 0.106 x 0.118 to 0.12 x 0.13 (line 303).
- Tail: end point `(0, 1.72, 0.22)` to `(0, 1.66, 0.26)` (line 34, about 8 % shorter). End tuft 0.075 / 0.085 / 0.075 to 0.10 / 0.11 / 0.095 (line 314). A horse's tail is long and bare; a lion's ends in a brush.

**MUST 4 - Halo: stand it up so the hero reads.**
- `HALO_TILT` (line 38): 20 to 40. The face and rim then show from the front and the game camera. Front ratio goes from 0.34 to 0.64.
- `HALO_C` z offset (line 35): 0.74 to 0.60. This keeps the rim top at the same height (11.5 studs). The `halo_top` value in the bounds (line 329) is the check.
- **Clearance:** the front lower edge must clear the crown and the outer mane tufts by at least 0.05 BU. If it touches, move the `HALO_C` y offset from 0.22 to 0.32. Check with the close sheet.

**MUST 5 - Gold and red at icon size.**
- Gold rim: `rim_i = HALO_R - 0.045` (line 207) to `- 0.075` (about 0.035 H). Target: at least 20 gold px in the game-camera icon (now 8); at least 3 % of the 64 px object pixels (portrait already 4.2 %).
- Corona: `rim_i - 0.032` (line 217) to `- 0.07`, so the BLOOD band reads as a band on the disc face. Target: at least 10 red px in the game-camera icon (now 0).
- Eyes: `eye(B, ..., sc=1.25)` (line 257) to `sc=1.6`, so the slits are about 30 % larger. Target: at least 10 red px in the 64 px portrait.

**MUST 6 - Clear the lower-pair clash.**
- The builder's own note: the lower pair (C) cuts 4-5 tri pairs into the hind thigh in the display pose. Raise the C root z from 1.02 to 1.05 (line 92), or lift C up from 10 to 14 (`DISPLAY_POSE`, line 374). Re-run the cut-through check. Target: 0.

**MUST 7 - Wing tips: fewer black dashes.**
- Tip fraction: `tipf=0.19` (secondaries, line 145) to 0.12. `tipf=0.25` (primaries, line 158) to 0.15. At 64-128 px the black dashes read as noise. Keep a dark trailing hem, shorter.

---

## 4. NICE
1. **Lower pair (C):** lift the display pose from up 10 to 18 (line 374), so its tips show past the flank in the front 3/4. The tucked read stays.
2. **Upper pair span:** check the game-camera span is about 2.0 H. If the wings look short, widen the upper pair's display angle (line 374, A from 44 to 50).
3. **Gold inner band:** only if the game-camera gold is still under 20 px after MUST 5, add a darker gold inner band to the rim. No gold on any other part.
4. **Round 2 outclass test:** a game-camera 64 px strip next to Cosmic Leviathan and Frostcrown Dragon.

## 5. Deviations ruling (MODEL_NOTES)

| # | deviation | ruling | why |
|---|---|---|---|
| D1 | halo 0.45 H, set back | ACCEPT | it floats clear of the mane. MUST 4 changes only the tilt and height |
| D2 | wings shorter (bind span about 1.8 H, plan 2.6 H) | ACCEPT | the bind pose must stay under the halo for the height scale. Check the display span (NICE 2) |
| D3 | OBSID 29-38 % (plan 14 %) | REJECT as built | the surplus is 36 feather tips and the spiky mane. Move the dark into one mane mass (MUST 2) and shorten the tips (MUST 7) |
| D4 | muzzle pads WING_IN | ACCEPT | a pale lion muzzle is right. Enlarge the muzzle (MUST 3) |
| D5 | placeholder display-pose idle | N/A | the real clips come after this gate |

## 6. Pass / fail checklist

| item | result |
|---|---|
| 64 px: species reads instantly (lion) | FAIL (reads as a winged horse / pegasus with a halo) |
| 128 px: species reads | FAIL (the lion read is weak) |
| Fierce, not cute (slit eyes, heavy brow, fangs, no glint, no smile) | PASS |
| Face reads from the game camera | PARTIAL (red eyes invisible at 64 px) |
| No box belly; belly line rises to the hips | PASS |
| Studs on hide; details smooth; no Neon, no glow | PASS (no emission in code; gold, red and feather tips smooth) |
| Palette follows the plan | PARTIAL (near-white 54 % against the plan's 40 % body; OBSID over plan) |
| Dark rich body + pale underside + one bright accent | FAIL (body pale; accent invisible) |
| Accent strong in game colours | FAIL (0 red px at 64 px) |
| Gold hero: at least 20 px at 64 px | PASS portrait (42); FAIL game camera (8) |
| 3-band colour blocking | FAIL (no mid band) |
| Six wings: tris <= 15k, not a blob, tiers countable | PASS |
| Six wings: all visible from the front icon | PARTIAL (lower pair hidden) |
| Floating, poking or intersecting parts | FAIL (lower pair into the hind thigh, the builder's own note; halo clearance unverified) |
| Distinct from Solar Lion (radial mane, sun colours) | PARTIAL (the radial mane is close to the Solar Lion's ruff at 64 px) |
| Beats Cosmic Leviathan (1 %) and Frostcrown Dragon (0.1 %) | FAIL (paler, less saturated, thinner gold) |
| Name is two words | PASS |

## 7. Next round: send with
- `_model_sheet.png`, `_close_sheet.png` (face at 3 angles), `_icons_strip_64.png`, `_icons2_strip_128.png` (portrait and game-camera).
- A 64 px game-camera strip with the Seraph beside Cosmic Leviathan and Frostcrown Dragon.
- `flat_game.png` with the value shares.
- Front and side renders of the halo after MUST 4, and a close-up of the rim and corona.
- The lower-pair cut-through check output (MUST 6).
- A re-run tri count.

**Bottom line:** REVISE. The body colour split, the lion mane and head, and the halo tilt with gold and red sizes decide whether this beats the Leviathan and the Frostcrown. Do not ship the current mesh.
