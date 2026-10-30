PASS

# Round 5 polish (delta check, independent reviewer, 2026-10-14)

**Verdict: PASS.** NICE 1-4 are applied, and nothing regressed. Cleared for the hub rollout. Crops are in
`review_crops\round5p\`.

| Check | Result |
|---|---|
| 1. Tongue tips and lean | **Pass.** The tops are blunt 3-lump heads (no spires), and the two tongues in each tile lean in opposite directions (`chain_EndL_A.png`, `chain_B_EndR.png`). |
| 2. Box-hedge masses | **Mostly pass.** B's flat lacy block is gone, the shoulders slope, and the tops are broken. One leftover is noted below (optional). |
| 3. Cap fade and seams | **Pass.** No straight diagonal: the bottom corner wobbles (EndL x 59 → 40, EndR 196 → 215 over the last 1.4 studs). The joins are invisible at 3x (`joins_x3.png`), and all 8 pairings have identical join deltas. |
| 4. Dying patches | **Pass.** Soft yellow-olive, with no orange freckles in `wall_close8_day`. The W_Crack_C notch moss matches the strips. |
| 5. No regressions | **Pass.** Wall-moss saturation is 0.60 day / 0.72 night (slime 0.80 / 0.90). Edge margins hold on all 17, the hidden bands are intact, and there are 0 floating clumps. The W_Crack_C slots are ≤ about 1.05 stud (90th percentile) over A 7-10 and B 12.5-15.5. |
| 6. Height vs "mushier" | **Pass.** My measured median is 1.95 (A) / 1.64 (B), with max about 4.4. `game_tp_day` still reads as a thick, overgrown, damp wall foot: the continuous mat, the climbing lumps and the dark wet band are all kept, and it is far from the round-3 thin fringe. |

**Optional nits (not blocking):**
- A's first mass (u about 2-6) still has a near-vertical left flank of about 1.9 studs next to a gap in the mat, and a
  flat slab-like top lump (`A_mass1_x3.png`). It only shows within about 8 studs. A low shoulder cushion in the gap
  would fix it.
- EndR's outer fade keeps faint vertical streaks at 2x.

---

# Round 5 (archived, 2026-10-14): PASS

**Verdict: PASS.** Both round-4 MUST items and all 4 NICE items are fixed. I verified them myself in the renders, the
sheets and the PNGs, and nothing regressed. Cleared to show the owner the re-built test patch and, after their OK, to
roll out.

The owner-facing read in `game_tp_day/night` is right:
- a thick, clearly green moss mat along the wall foot, under a dark wet band;
- a few climbing tongues;
- the wall moss tied to the floor moss and a wet puddle;
- the cracks unchanged.

It reads as "overgrown, damp, abandoned Halloween square", not a hedge, not neon and not gloomy. The slime is the
brightest green again.

Crops are in `review_crops\round5\`.

## Verified
| Item | Result |
|---|---|
| MUST 1 hedge of bushes | **Fixed.** A continuous mat plus 2 ragged tongues per tile. No round crowns, and no cut-out bushes in `wall_oblique20_day`. Median height A 2.37 / B 2.19. |
| MUST 2 neon | **Fixed.** My own measurement on the moss pixels: day median saturation 0.60 (mean (44,112,52)), night 0.72, against the slime's 0.80 / 0.90. It is still clearly green on the shaded wall (value 0.45). |
| N1 W_Crack_C notch moss | **Fixed.** It matches the strip palette in `wall_close8_day`. |
| N2 G_Stain_A flecks | **Fixed.** 14 faint streaks read as a wet sheen, not glitter. |
| N3 end-cap fade | **Fixed** at the top of the fade. There is a small leftover at the bottom corner (N3 below). |
| Seams / caps | All 8 pairings have identical join deltas. At 3x zoom the joins are invisible: a 0.5-level column step. The caps' inner columns are within 2/255 of the strips'. |
| Edges / bands / floating | All OK. Every free edge has a ≥ 4 px alpha-0 margin, every hidden band is intact, and there is 0 floating moss. |
| Test patch | `Crack_Diag` at y 5.25-15.25 is 2.1 studs clear of the moss. |

## MUST
None.

## NICE (polish; can be done during the hub rollout)
1. **Tongue tips.**
   - At third-person distance the 4 tongues in the bay read as pointed spires, a little like cypress trees or flames
     (`round5\game_tp_day_tongues_x4.png`).
   - In `mossbase_seams.png` every tongue leans the same way, so long runs show a repeated row of "fins".
   - Fix: blunt or break the tips (2-3 lumps across the top rather than one point), and lean the two tongues in each
     tile in opposite directions.
2. **Box-shaped masses.**
   - A at about u 1.5-4 and B at about u 16-20 have a near-vertical side and a flat, lacy top. They read as a clipped
     box hedge or crate (`round5\A_u0-8_x3.png`, `B_u14-24_x3.png`, and the left block in `wall_close8_day`).
   - Fix: round the shoulders (sides at about 45-60°) and break the top line with 1-2 lumps.
3. **End caps.**
   - The bottom outer corner of the fade is still a near-straight slant over the last ~1.4 studs (EndL rows 210-260:
     x 59 → 34; EndR: 192 → 224).
   - The fade top has vertical comb streaks that read as a misty pine-forest silhouette at 2x
     (`round5\comp_W_MossBase_End*_x2.png`).
   - Fix: wobble the last stud too, and soften or shorten the vertical streaking in the caps.
4. **Dying patches.** These are small orange-brown round spots that read as rust freckles up close (`wall_close8_day`,
   the B mass). Make them fewer and larger, softer and more yellow-olive, and put them on mound tops and edges.
5. **Rollout.**
   - Back-wall bays alternate A/B, so every A bay repeats the same tongues at the same spots.
   - Vary `OffsetStudsU` per bay, by 6, 12 or 18 studs, except in bays that carry a `W_Crack_C`, which need offset 0
     for the low-moss slot.
   - Keep 2-3 bays bare.

---

# Round 4 (archived, 2026-10-14): FIX

**Verdict: FIX** (two narrow MUST items). The direction is right, and the re-calibration is trustworthy:
- `ingame_vs_mock.png` shows the re-lit mock reproducing the game's thin dark fringe with the round-3 decals, so the
  `game_*` frames can be judged as in-game.
- The owner's complaint was the **value and mass** (a near-black fringe in shade), and both are now fixed: the moss is
  thick, visible and green, and the damp band does the "wet" work.

It overshoots on two things the brief rules out:
- the wall moss now reads as a **row of bushes/hedge** painted on the wall;
- the moss **chroma** is neon-lime, more saturated than the slime.

**Don't go back to round 3.** Keep the brightness, the continuous thick base and the dark wet band; trim the
silhouettes and the chroma only.

Crops are in `review_crops\round4\` (plus `review_crops\round4_*_game_vs_mock.png`).

## Still clean (re-measured)
- **Files.** All 17 are RGBA, ≤ 1024 px, multiples of 4.
- **Margins.** Every non-contact edge has a ≥ 4 px alpha-0 margin.
- **Hidden bands.** All intact (4 px alpha 0, then a 3 px ramp, then content at full strength).
- **MossBase seams.** All 8 pairings have identical seam deltas (max 54/255 vs the strips' median column delta of 65),
  and `seamless_ok` is true.
- **Floating moss.** 0 in all 9 wall textures.
- **Fringes.** None.
- **`Crack_Diag`.** Now at y 5.75-15.75: 2.1 studs clear of the moss and below the garland swag. OK.

## MUST
1. **MossBase A/B read as a hedge of round shrubs, not moss creeping up a wall.**
   - **Where:** `game_tp_day`, `wall_eye25_day`, `wall_tp_day`, and `mossbase_seams.png`, where the chain is an evenly
     spaced row of domes.
   - **What makes it a hedge:**
     - tree-crown domes 3.5-5.3 studs tall (A is > 3.5 studs over about 55 % of its width; both A and B peak at 5.3);
     - full spherical dome shading on the big masses.
   - **Why it matters on a decal:** a painted 3D bush on a flat decal also turns into a cut-out sticker at an angle
     (`wall_oblique20_day`).
   - **Fix:**
     - (a) Cap the broad masses at about 3 studs, and keep the continuous 1-2 stud base mat.
     - (b) Replace the round crowns with 1-2 **ragged climbing tongues** per tile: narrower toward the top, a broken
       or lumpy top, at most about 4.5 studs, offset at irregular spacing.
     - (c) Flatten the macro dome shading: keep the per-clump lumps, drop the one big sphere light per mound.
     - (d) Make the seam mound lower (≤ 1.5 studs) so the chain doesn't pulse every 24 studs.
   - **Targets:** median moss height about 2-2.3 studs (A is 2.7 today). Keep the W_Crack_C low slots.
   - **Caps:** EndL/EndR follow.
2. **The moss chroma is neon and has stolen the slime's role.**
   - **Measured (moss pixels in the game frames):**

| Frame | Median saturation |
|---|---|
| day, round 4 | 0.79 (hue 108) |
| night, round 4 | **0.91**, mean RGB (48,116,13) |
| day, round 3 | 0.66 |
| the W_Drip_B slime in the same frame | 0.80 |

   - At night the lime glows against the dark blue (`game_tp_night`). The Moonlit saturation boost will push it
     further in game, because the mock night is the conservative one.
   - Close up, the bright tips everywhere turn G_Moss_A/B and the MossBase into lime sponge/foam (`game_close_day`,
     `wall_close8_day`, `wall_tp4_day`).
   - **Fix:**
     - Keep the value (brightness), and lower the body chroma by about 20 % toward olive, e.g. MM2 about (72,108,34)
       and MM3 about (112,150,46).
     - Keep the lime only on a minority of lit tips (`tip_amt` about 0.55-0.6 instead of 1.0).
     - Add a few olive/yellow-brown (dying) patches per tile for variation.
     - Apply the same change to G_Moss_A/B.
   - **Gate:**
     - moss median saturation ≤ about 0.68 day and ≤ about 0.75 night in `game_tp_*`;
     - the slime is still the most saturated green in frame;
     - it still reads clearly green, not dark, on the shaded wall.

## NICE
1. **W_Crack_C notch moss (the coordinator's question): NICE, not MUST.**
   - Within about 8 studs, the round-3 notch moss is a dull olive plug next to the lime (`round4\close8_notch.png`).
   - From the third-person camera it reads as shadow inside the notch (`round4\game_tp_notch.png`).
   - Retint the notch moss and the 2 ledge tufts to the **final** MossBase palette, in the same pass as MUST 2. Leave
     the crack pixels untouched.
2. **G_Stain_A.** It now reads clearly as wet ground (dark rim, sheen, reflection line), not as a shadow. Pass.
   - Its 36 white flecks read as glitter/stars up close (`game_close_day`). Cut them to about 12-15, make them
     longer and fainter, and keep the rim reflection line.
   - G_Stain_B: fine.
3. **End-cap damp regression.**
   - The outer bottom corner of EndL/EndR fades along a straight diagonal again: EndL rows 195-240, alpha-40 edge
     x 69 → 41, linear (`round4\comp_W_MossBase_EndL_x2.png`).
   - Restore the round-3 sine/noise fade.
4. **After MUST 1,** re-check `mossbase_seams.png` for an even "bush every N studs" rhythm, and `wall_oblique20_day` for
   the sticker read.

---

# Round 2 (archived, 2026-10-14): PASS

**Verdict: PASS.** Cleared for the owner test patch. All 6 round-1 MUST items and 6 NICE items are fixed, or fixed well enough that what's left only shows within about 8 studs. The NICE items below are polish. Do N1 before rolling out across the hub; it is about a 10-minute change.

Crops are in `review_crops\round2\`.

## What I checked myself
- **Files.** All 17 are RGBA, ≤ 1024 px, multiples of 4. Every non-contact edge has a ≥ 4 px alpha-0 margin.
- **Hidden bands.** W_Crack_C bottom, W_Drip_A/B top and MossBase bottom each have 4 px of alpha 0, a 3 px ramp, then content at full strength.
- **MossBase seams.** The seam delta is 35/255 against a median column delta of 51 inside the strip, the same in all 8 pairings, and the caps match the strips.
- **Fringes.** None over black, white or magenta.
- **Test patch.** I re-rasterized the floor patch from the PNG alpha in world space, in all 4 possible Top-face orientations:
  - the only content overlap is a stain under moss (allowed);
  - the wall-foot moss ends 0.1-0.35 stud from z 104;
  - the plaza-rim crack and slime don't touch.
- **Wall bay.** The math is consistent:
  - faces at 41.05 / 65.15;
  - W_Crack_C at 56.65, on the low-moss slot (it sits in low moss in the render);
  - W_Crack_B content at x 44.0-49.9;
  - W_Drip_A content at x 59.1-63.0, 2.2 studs from the pillar, with ≥ 5 studs to any crack;
  - clear of Base2 and Base3 with their margins.

## Round-1 items, re-verified
| Item | Result |
|---|---|
| MUST 1 W_Crack_C tree | **Fixed.** It reads as a crack in `gate_W_Crack_C_vs_A`, the thumbs, `wall_eye25_day` and `wall_tp_day`. |
| MUST 2 stains / shadow | **Fixed.** G_Stain_A reads as a wet olive puddle with a rim and no longer matches the dummy's shadow. G_Stain_B reads as a mud skid. |
| MUST 3 floating moss | **Fixed.** The confetti is gone in every wall view, and `floating_moss` reports 0. |
| MUST 4 Drip_B band | **Fixed.** The left end tapers and the right end is a lobe. |
| MUST 5 glass chips | **Partly fixed.** The chips are darker and attached, but they still read as translucent flat panes up close (N1). |
| MUST 6 test patch | **Fixed** (see above). |
| NICE 1-6 | **Done.** Wedge roots, micro-jag, the tide line, slime, drops, the G_Crack_C ladder and the JSON are all addressed. Two small leftovers are in N2 and N3. |

## Owner-facing impression
- **Third-person wall view** (`wall_tp_day/night`): this is the strongest view, and it is tasteful.
  - What it shows: zigzag cracks with moss tufts, a mossy wall foot, wall moss joined to the floor moss, a damp puddle, and one lime slime drip as the fun accent.
  - It reads as an overgrown, abandoned Halloween town square, not dirty, gloomy or photographic.
- **Night** keeps everything readable.
- **Floor third-person view** (`floor_tp_day`): the clusters with clean space between them work, and the slime pops on cream.
- **Eye height:** the walls carry the look and the floor grime is faint, as designed.
- **Possible owner question:** at 25 studs, MossBase A's 2.5-stud mounds read a little like low shrubs along the wall. That is fine for an "overgrown" read. If the owner asks for "creepier/flatter", use B on more bays.

## MUST
None.

## NICE (polish; N1 before hub-wide rollout)
1. **Glassy chips and lips.**
   - **Where they show:**
     - the W_Crack_C kink chip and the W_Crack_B chip beside its open section read as flat translucent panes with straight edges and a pale rim (`round2\close8_crackC_chip.png`, `tp4_crackC_chip.png`, `oblique_crackB_chip.png`);
     - G_Crack_C's tilted chunk reads as a pale glass sheet (`comp_G_Crack_C_x1.png`);
     - pale "✓" ticks: one at the G_Crack_B crater top and one at the W_Crack_C notch apex;
     - G_Crack_A's open section has a continuous white lip (visible in `wall_tp_day`).
   - **Fix:**
     - Drop the separate recess polygons on W_Crack_A/B/C and G_Crack_A (keep only the open-section bevels).
     - Use a darker W4 tint for the tilt on G_Crack_C instead of the W5 pale gradient.
     - Gate-break the lips to ≤ 50 % with irregular gaps.
     - Remove the two tick highlights.
2. **G_Crack_B still has a slight spider read on cream** (`close6_crackB_cream.png`): a round body with 8 evenly spaced, curved, bent legs.
   - Make 2 rays long and straight-kinked, and the rest short.
   - Remove the "knee" bends.
   - Make 2 of the ring arcs a bit bolder so it reads as a spider-web *fracture*.
3. **Small leftovers:**
   - **MossBase_B:** the damp wicks end in sharp flame-like spikes, and the broken tide line leaves curved "eyebrow" ticks in A and B. Soften the spike tips and shorten or remove isolated tick fragments.
   - **EndL:** the outer damp edge still shows 2 pointed peaks, and a single dark pill-shaped satellite sits about 0.4 stud above the moss. Remove the pill.
   - **W_Crack_C:** the damp glaze behind the notch has a peaked "mountain" outline. Use a soft rounded fan instead. A pink sliver (the grass sprig) in the notch moss reads as a worm; make it straw-coloured or drop it.
   - **G_Stain_A:** its rim is a uniform continuous outline on a cloud/teddy-head silhouette, which looks a little clip-art. Break the rim in 2-3 places, vary its width, and make one lobe less round.
   - **W_Drip_B:** the left taper of the goo band is a straight bevel. Give it a sagging curve.

---

# Round 1 (archived, 2026-10-14): FIX

## MUST (blocking)
1. **`W_Crack_C` read as a painted dead tree.** It had a trunk with a root flare, Y-forks of upward twigs and a moss bush. Redraw: an angular zigzag, a notch recess at the base, moss in the notch and on ledges; gate at 1/8 next to W_Crack_A.
2. **The stains read as cast shadows, and G_Stain_B as a slug.** Fix: a saturated olive/umber hue, a watermark ring structure, and a splashy drag shape with elongated splatter.
3. **Free-floating moss bits on the walls** (about 20 in MossBase_A, plus B, the caps and W_Crack_C). Cut about 70 % and attach the rest; regenerate the seam set.
4. **The visible part of W_Drip_B's goo band was a hard rectangle.** Taper and round both ends.
5. **The chips rendered as glass shards.** Use a lit-side edge only and a dark recess fill, and drop chips that don't touch a crack core.
6. **The test patch sat on Base2.** Also, W_Drip_A ran into W_Crack_B, and the floor moss stopped 2.3-2.7 studs short of the wall. Move to the bay at x 39.8-66.4 and recompute.

## NICE
1. Crack line quality (wedge roots, micro-jag, a 1.8-stud crater).
2. The MossBase damp band drew a "mountain range".
3. G_Slime_A looked like a stamped icon.
4. The drops were round.
5. G_Crack_C read as a ladder.
6. The test_patch.json `verify` list, ModuleScript cleanup, and the third-person view for the owner.
