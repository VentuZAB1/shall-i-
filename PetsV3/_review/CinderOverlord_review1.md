# Cinder Overlord - MODEL GATE review 1 (2026-10-27) - REVISE

**Verdict: REVISE. Score 5/10** for an ultra-rare 0.5 %. Target to ship: 8/10 or better.

The build is sound where it is measurable: 10,896 tris, a rig that lifts the five crown blades with zero collisions (builder's test), and a clean wedge-free lying S. The problems are in the read. At 64 px it is a thin pink serpent with a yellow tiara. It shares its family with CosmicLeviathan (1 %), it does not read as Fire, and it does not outclass the Phoenix (2 %) or Ivonrath (4 %) in impact. Do NOT send it to the clip gate yet. The fixes below are model-only and must land before the molt act is authored.

## 0. What I looked at

- Style and gates: `Creature Style.md`, `Model Review Checklist.md`, `FIERCE_GUIDE.md`, the plan `_review/CinderOverlord_plan.md` (v2), the plan review section 2.10 and gates section 6 of `_review/GLACIER_PLAN_REVIEW.md`, the owner decisions in `_review/GLACIER_CONCEPTS.md`, and the format of `VenomBasilisk_review2.md`.
- Builder's notes `CinderOverlord/MODEL_NOTES.md` (deviations 1-7, value table).
- Renders in `CinderOverlord/renders/`:
  - `_model_sheet.png` (4 views), `_close_sheet.png` (head, crown, face);
  - `_icons_strip_64.png` / `_128.png` (8 items: Cinder first, then MoltenBoar, LavaGolem, Cerberus, Ivonrath, InfernoPhoenix, ThunderRex, CosmicLeviathan);
  - `_icons2_strip_64.png` / `_128.png` (portrait + game-camera icon + the same 7 comparisons);
  - `flat_side.png`, `flat_tq.png`, `flat_game.png`, `gamelook_game.png`, `gamelook_tq.png`.
- Comparison renders: `BlackDragon/renders/_model_sheet.png`, `ThunderRex/renders/_model_sheet.png`, `CosmicLeviathan/renders/_model_sheet.png`, `_ALL_FIERCE_progress.png` (lineup).
- Source: `pets/CinderOverlord.py` (line references below) and the palettes of CosmicLeviathan, ThunderRex, BlackDragon, Ivonrath, InfernoPhoenix.
- Colour: I converted the RGB values to hue (H) and saturation (S) myself and measured the hue distance to each comparison.

No clip work was reviewed (no clips exist yet; the clip gate is for the next round).

## 1. Numbers

| Item | Built | Target / rule | Result |
|---|---|---|---|
| Tris | 10,896 | <= 15k | PASS |
| Height | 10.5 | above Rex and Leviathan (10.0) | PASS on the number; the body is thin, so it does not read taller |
| Gold px at 64 px | 39 (builder's counter says 52) | >= 25 | PASS |
| Body PLUM_OBS side / game | 56.6 % / 51.7 % | dark rich body | PASS (plan was 44 %) |
| Obsidian OBS_D side / game | 24.7 % / 32.7 % | 16 % (plan) | over the plan; game shows it as a second dark band |
| Pale underside PALE_S side / game | 6.4 % / **0.7 %** | 10 % (plan); visible 3-band | **FAIL in game**: the pale band is effectively gone from the player's view |
| Rose ROSE + ROSE_H side / game | 3.6 % / 3.7 % | 8 % (plan), accent strong in game | **FAIL** (about half the plan) |
| Gold GOLD side / game | 2.3 % / 4.4 % | 3 % (plan) | PASS |
| Body colour | (160,90,136), H ~321, S 0.44, luminance ~116 | brightest channel >= 170 OR luminance >= 95 | PASS on the luminance clause (brightest channel is 160; note it) |
| Hue distance to CosmicLeviathan HIDE (170,54,170, H 300, S 0.68) | ~21 deg, the body reads as the same magenta family | a sibling must not copy the family | **FAIL** (MUST 1) |

## 2. Builder's deviations, ruled

1. **Colours (body deepened to (160,90,136), OBS_D to (62,50,64)).** The darkening is right: it removes the candy-pink of the plan value. The hue is wrong for a 0.5 % pet: it sits 21 deg from the CosmicLeviathan's magenta. **Partly accepted.** OBS_D stays. The body moves (MUST 1).
2. **Obsidian rings instead of top plates.** **Accepted.** The rings give the banded serpent and the dark band. The read is a segmented worm on the tail, so it is thinned there (NICE 1).
3. **Gold frames on all four edges of each blade.** **Rejected in part.** The four-edge gold makes the crown a yellow tiara. That is the cute read, and it copies the gold-crown language of CosmicLeviathan, Ivonrath, Phoenix and ThunderRex. Keep the gold, but on fewer edges (MUST 2).
4. **Crown mount, five blades side by side.** **Accepted.** The five-point crown reads from the front, and the lift test is clean.
5. **Head x1.2 and cheek spikes.** **Accepted** for the size and the spikes. The head is still a brick (MUST 5).
6. **Vents as double slits.** **Accepted.** The doubling reads. The rose is still too little (MUST 4).
7. **Forearms on Neck1.** **Accepted.** They read as arms.

## 3. Builder's open question: widen the vents into lava stripes to reach 8 % rose?

**Ruling: YES, widen the vents to about 6 % rose. NO to full-length stripes.**

- Widen the vent slits (`pets/CinderOverlord.py` lines 242-243): width `0.042*sc+0.010` to `0.060*sc+0.014`, length `0.18*sc+0.035` to `0.22*sc+0.04`. That multiplies the rose area by about 1.7, so about 6 %.
- Do not go to continuous lava stripes. Stripes running the length of the body read as candy stripes, which is the toy look the owner rejected. Keep them as flush slits at the six pairs.
- The 8 % target is not required if MUST 3 lands (the lava hot cores carry the Fire read).

## 4. Fierce or cute?

**Borderline. Cute risk is high at icon size, fierce in the close-ups.**

- Fierce: the brow bar over the rose slit eyes, the cheek spikes, the fangs, the dark crown mass, and the forearm claws all read as predator at close range.
- Cute: the portrait reads lavender-pink, not plum; the five gold blades are a royal tiara, not a crest; the pale ladder on the throat and the boxy head read as a toy. At 64 px the face does not resolve at all, so the pet reads as "pink worm with a yellow crown".
- Fixes are MUST 1, MUST 2 and MUST 5.

## 5. Does the Fire-egg identity read?

**No.** At 64 px and in the game view the Cinder reads as a magenta-plum serpent with a gold crown. Nothing in the icon is orange, red or ember. It reads Celestial (the CosmicLeviathan family) before it reads Fire.

The concept's rule was "rose instead of fire colours". The rose does not carry the Fire read on its own at 3.6 %. The fix is in MUST 3: the vent hot cores and the tail ember tip become LAVA orange. The Fire egg is all orange, so two hot cores in LAVA are a family signal, and they stay under 2 % of the surface, so the Cinder is not a copy of the Boar or the Golem.

## 6. Is it the most impressive pet of the Fire egg?

**No, not yet.** At 64 px the InfernoPhoenix (flame crest, ember wings) and the Ivonrath (winged red wyrm with a gold flame crown) both read more striking and more "fire". The Cinder is the thinnest silhouette of the three. It is the top of the egg by odds (0.5 %), so it has to be the most imposing. It is not yet: the body is thin (MUST 6) and the crown is a tiara (MUST 2).

The comparison to the 1 % secrets is also a loss today:
- ThunderRex: a heavier silhouette, a clear three-band navy / cyan / gold, a readable crown.
- CosmicLeviathan: more mass, fins and an ivory belly. The Cinder reads as a thinner echo of it (MUST 1 and 2).

## 7. MUST list (prioritized, all in `pets/CinderOverlord.py` unless noted)

**MUST 1 - Move the body off the CosmicLeviathan's magenta (distinctness).**
- Leviathan HIDE (170,54,170) is H 300, S 0.68. The Cinder PLUM_OBS (160,90,136) is H ~321, S 0.44: 21 deg apart, and at icon size both read "magenta serpent, gold crown, pale belly".
- Change line 17 `PLUM_OBS = (160, 90, 136)` to **(150, 84, 110)** (H ~336, S 0.44, luminance ~107). That is about 36 deg from the Leviathan, and it reads a cooler oxblood-mauve, not candy pink. Keep OBS_D (62,50,64).
- If the portrait still reads pink after this, go to a deeper obsidian-dominant body (more OBS_D share), not a lighter one.

**MUST 2 - The crown reads as a tiara; cut the gold to the edges that matter.**
- The gold frame loop at lines 170-176 runs on all four edges of every blade. Keep the gold on the two upper edges of each blade, and on the two sides of the centre blade only. Drop the outer side frames on blades 1, 2, 4 and 5.
- Gold px at 64 px should land at about 28-32. Re-measure: the gate is >= 25.
- Keep the gold itself (house gold is the hero rule for rare tiers). The change is the amount, not the colour.

**MUST 3 - Make it read Fire: lava hot cores.**
- Line 155 (the vent hot centre) and the tail ember tip (line 213, the second `ROSE_H` spike) change from ROSE_H (255,190,214) to **LAVA (255,128,24)**. The rose body stays the accent, and the orange sits only in the hot cores.
- Keep the vent body ROSE (255,96,150). Two orange cores plus one tail tip are under 2 % of the surface.

**MUST 4 - Rose accent area (the builder's open question, ruled in section 3).**
- Lines 242-243: vent width `0.042*sc+0.010` to `0.060*sc+0.014`; length `0.18*sc+0.035` to `0.22*sc+0.04`. Expect rose at about 6 % (side). Do not stripe the body.

**MUST 5 - The head is a brick.**
- The skull is `B.seg((0,-0.50,1.69),(0,-1.04,1.625), 0.195, 0.150, PLUM_OBS, "Head", top=(0.56,0.56), ext=0.05, rnd=0.36)` at lines 260-261. In the close-ups it reads as a rounded box with a flat top.
- Narrow the front radius `0.150` to **0.115**, and raise `rnd` `0.36` to **0.50**, so the cross-section is an oval wedge and the snout tapers to a point.
- The black crown mount at line 301 and the nasal ridge at line 262 also read as a beam across the skull. Thin the nasal ridge to 0.02 wide (see NICE 2).

**MUST 6 - The body is too thin for a 0.5 % pet.**
- The chest radius is `RAD[0] = 0.230` (line 37), so the chest is about 0.21 H thick. The Leviathan and Rex are visibly bulkier.
- Raise `RAD[0..4]` by about 15 %: `[0.265, 0.250, 0.230, 0.205, 0.180, ...]`. Leave the tail radii, so the taper stays. The vents and rings follow the radii automatically.
- Re-check the vents and ring bands after the change (lines 196-206 and 235-243).

**MUST 7 - The pale underside is invisible in game (0.7 % in game).**
- The belly scutes run on the arc 212-328 deg (line 207, `scutes(..., 212, 328, ts=((0.04,0.44),(0.52,0.94)))`). From the game camera (5 studs up) the belly is hidden, so the pale band disappears.
- Widen the arc to 190-340 deg on Body1-4, so the pale band wraps the flank as well as the belly.
- Raise `PALE_S` (line 20) from (226,210,214) to **(245,236,240)**. In game (x0.6) that is a light grey band, not plum. Target game pale >= 4 %.

**MUST 8 - Icon gate: BlackDragon is missing from the 64 / 128 strips.**
- The icon strips show seven comparisons. BlackDragon (the other serpent, named in the brief) is not in them. Add it to `_icons2_strip_64.png` and `_icons2_strip_128.png` next to the Cinder, since it is the pet most likely to be compared for the serpent kit.

## 8. NICE list

1. **Rings read as a segmented worm on the tail.** The ring band (lines 196-206, 0.52-0.86 of each segment) on Tail1-4 reads as "caterpillar" from the side. Thin it to 0.60-0.80 on the tail segments only. Keep the full ring band on Spine to Body4.
2. **The nasal ridge and the crown mount read as beams** (lines 262 and 301). Make the ridge 0.02 wide, and taper the crown mount's ends to 0.04 high.
3. **The brows are flat bars** (line 297, `0.108 x 0.036 x 0.030`). Give each brow a forward point (a small spike) so the eyes read fierce from 64 px.
4. **Rose eye slits are too small at 64 px** (line 292, 0.074 wide). Widen to about 0.085 so the eye reads at distance.
5. **Clip-gate watch (for the next round):** the molt act is 35 deg per plate with 0 collisions at rest; check the same at 35 deg with the fatter body from MUST 6.

## 9. Pass / fail checklist (model gate)

| # | Check | Result |
|---|---|---|
| 1 | Tris <= 15k | PASS (10,896) |
| 2 | Silhouette at 64 px: the species reads (serpent, crown) | PASS |
| 3 | Face reads at 64 px | FAIL (eyes do not resolve) |
| 4 | Face reads in close-up (narrow slits, brow, fangs) | PASS |
| 5 | Fierce, not cute (icon) | FAIL (borderline: pink portrait, tiara) |
| 6 | Dark rich body (game) | PASS (plum in game) |
| 7 | Pale underside visible in game (3 bands) | FAIL (0.7 %) |
| 8 | One bright accent (rose) strong enough in game | FAIL (3.7 %, target ~6-8 %) |
| 9 | Gold hero readable at 64 px, >= 25 px | PASS (39 px; re-measure after MUST 2) |
| 10 | Fire-egg identity reads | FAIL (no orange or ember) |
| 11 | Distinct from CosmicLeviathan (1 %) | FAIL (same magenta and gold family) |
| 12 | Outclasses ThunderRex (1 %) at icon size | FAIL |
| 13 | Outclasses CosmicLeviathan (1 %) at icon size | FAIL (thinner, same family) |
| 14 | Outclasses InfernoPhoenix (2 %) and Ivonrath (4 %) | FAIL (not the most impressive Fire pet yet) |
| 15 | Parts floating, poking, or visible wrong from below | PASS (visual; the crown and claws sit on their bones) |
| 16 | Crown is hero: gold rim, obsidian blades, one big signature | PASS in concept; FAIL on the tiara read (MUST 2) |
| 17 | Icon gate: 64 / 128 px next to the nearest pets incl. BlackDragon | FAIL (BlackDragon missing) |
| 18 | Clip gate (pose limits, collisions, acts) | NOT REVIEWED (no clips yet) |

## 10. Next round

Send, with the fixes applied:
- `_model_sheet.png` and `_close_sheet.png` (head and crown);
- `_icons2_strip_64.png` and `_128.png` with BlackDragon added;
- `flat_side.png`, `flat_tq.png`, `flat_game.png` with the new value shares (game pale, rose, gold);
- `gamelook_game.png` (the 5-stud view that the player sees).

The clip gate starts after this model gate passes at 8/10.
