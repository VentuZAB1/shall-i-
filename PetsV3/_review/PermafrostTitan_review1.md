# Permafrost Titan - model gate review 1 (2026-10-27) - REVISE (model)

**Score: 6/10 for a 2.5 % SECRET.** Ship at 8/10 or better. The concept is right and the chest bezel works from the front.
It is not yet a clear outclass of the Yeti (14 %) or the Roc (7.4 %): from behind it has no gold, the brows read as cartoon
tubes, and the limbs are the same stacked-box robot build that got the Yeti 5/10. All MUST items are code-level
(no bone, joint or clip change), so this is a short round 2 on renders, not a new full gate.

## What I looked at

- Code: `pets/PermafrostTitan.py` (palette L17-27, back hump and slabs L111-127, bezel L128-159, pecs L166-170, head
  L171-191, arms and pauldrons L192-231, legs and feet L232-252).
- Builder and plan: `PermafrostTitan/MODEL_NOTES.md`, `_review/PermafrostTitan_plan.md` (v2), `_review/GLACIER_PLAN_REVIEW.md`
  section 2.5 and rulings, `_review/GLACIER_CONCEPTS.md` (owner decisions), `FIERCE_GUIDE.md`, the vault notes
  `06 Modelling and Art/Creature Style.md` and `Model Review Checklist.md`.
- Titan renders: `_model_sheet.png`, `_close_sheet.png`, `close_low.png`, `model_back.png`, `flat_side.png`, `flat_tq.png`,
  `flat_game.png`, `gamelook_tq.png`, `gamelook_game.png`, `_icons_strip_64.png`, `_icons_strip_128.png`,
  `_icons2_strip_64.png`, `_icons2_strip_128.png`. Not supplied: a belly-up render (see NICE / next round).
- Comparisons: ThunderRex and LavaGolem `_model_sheet.png`, GlacierYeti and BlizzardRoc `_model_sheet.png` and
  `_icons_strip_128.png`, CosmicLeviathan `_model_sheet.png`, `_ALL_FIERCE_progress.png`.
- Calibration from this round: `GlacierYeti_review1.md` (5/10, REVISE, "blocky robot ape") and `BlizzardRoc_review1.md`
  (7/10, APPROVED WITH FIXES).

## Measured facts

- Height: HEIGHT 10.0 (L15). Equal to Thunder Rex, above the Yeti (9.0) and the Roc (9.0). PASS.
- Tris: 7,000 per the builder (cap 15k). Not re-measured. PASS.
- Gold at 64 px, portrait cell: 26 px by my hue count (builder's kit count 31). Gate is 25, so it passes with a thin margin.
- Gold at 64 px, game-camera icon (`_icons2_strip_64`, second cell): 0 px. The gold ring is not visible from behind.
- Body MAUVE (136,94,166): H 275, S 0.43, V 0.65. Brightest channel 166 (rule 170, misses by 4). Luminance 115 (alt rule 95, passes).
  The FIERCE guide accepts either test, so this is a NICE, not a MUST.
- In-game body (`gamelook_game.png`, the most common purple tones): about (72,64,104) dusky slate-violet. Builder's estimate (82,56,100).
- Value shares: the builder's table (MAUVE 65.3, PLUM 11.8, ICE 11.3, JOINT 7.8, GOLD 1.2, BLACK 2.4 side) holds.
  My flat-palette pixel check agrees within about 4 points (body family about 65 %, ICE about 8 %, gold 0.9 % side, 3.2 % tq).
- The builder's claim "pets turn to face the player when idle" is UNVERIFIED. A search of the Studio scripts found no
  pet-facing code and the memory notes have none either. Do not rely on the front ring until Studio confirms it.

## What works

- **The hero works from the front.** A 12-facet house-gold bezel (outer dia 0.45 BU = 0.22 H, tilt 10 deg, four settings,
  GOLD_D lining) around an ice-white core. It is the one big signature and it reads at 64 px in the portrait. The plan's
  gold spec is met, and the band (0.037 H vs 0.03 H) is an accepted deviation (it adds the margin).
- **Colour blocking is three bands plus gold.** Mid MAUVE body, dark PLUM back slabs, hip plates and armour, pale ICE_W
  caps and knuckles, gold hero. Blocking passes, and the gold is smooth while the body is studded.
- **Distinct from Rex and the Roc.** No spikes, no crown, no cyan, and no white bird build. The ice is white, not the Lynx cyan.
- **Hard rules pass.** No glow, no Neon, studs everywhere, and the ice caps, gold and slits are smooth.
- **The upper face is fierce in part.** Narrow ICE_W slits in dark sockets, black slit pupils with no glint, a flat closed
  mouth, and no smile. Keep the slit design.
- **Floating and intersection:** none seen in the visible views (front, side, back, tq, low close-up).

## Deviations (builder's list) - verdict

| # | Deviation | Verdict |
|---|---|---|
| 1 | MAUVE deepened from (184,150,200) to (136,94,166), same hue | ACCEPT. The plan value read pastel. Lift a little more (NICE 1). |
| 2 | Added PLUM armour plates for 3-band blocking | ACCEPT. This is the right fix for a secret. |
| 3 | Extra blunt ice on the back hump and forearms | ACCEPT the ice (blunt, no spikes). It does NOT replace gold on the back (MUST 1). |
| 4 | Proportions (the plan's numbers did not add up) | ACCEPT. The builder's numbers are consistent. |
| 5 | Bezel band 0.037 H (plan 0.03 H) plus 4 settings, for the gold gate | ACCEPT. The margin is needed (NICE 2). |
| 6 | Head group translated +0.035 up, +0.03 forward; neck knuckle | ACCEPT. Collision-tested by the builder; neutral to the look. |

## Answers to the builder's flags

**1. Zero gold from the game camera (behind): NOT acceptable as built for a 2.5 % secret.** The brief asks for a gold hero
readable at 64 px from the player's camera. The front works, but the game-camera icon is a purple giant with white shoulder
caps, and from behind it looks much like the Yeti (also a dark giant with pale shoulder plates). The player sees the back
while the pet walks and follows, and the front-facing claim is unverified. The fix is a small gold element on the back that
echoes the chest ring. It is not a crown and it does not copy Rex (MUST 1).

**2. Colour deepening: ACCEPT.** The pastel is gone and the hue (H 275) stays out of the Glacier blue-violet cluster. The value
is a little dark (in-game about (72,64,104)). Lift it slightly to keep presence in game (NICE 1).

**3. Does it clearly outclass the Yeti and the Roc? Not yet.**
- Roc (7.4 %): yes on tier signal (gold ring, 10 vs 9 studs, three bands, bulk). The Roc is a different animal.
- Yeti (14 %): only from the front. From behind the two are close. The Yeti will improve after its own REVISE, so the Titan's
  margin has to come from MUST 1 and MUST 3, not from the colour.

## MUST (in priority order)

1. **Give the back a gold element (game camera, L111-127).** Build a small echo of the chest ring on the back hump, the same
   construction as the bezel (L139-150: 12 GOLD segments, GOLD_D lining, no settings).
   - Outer diameter 0.20 BU (about 0.10 H, about 44 % of the chest ring's 0.45 BU).
   - Band 0.030 BU radial, depth 0.06, tilt 0-10 deg up.
   - Centre on the hump back face at about z 1.66-1.70, between the back slabs (L114-119, z 1.20-1.58) and the top crust
     chunks (L124-127). Check collisions with the collision locator.
   - Fallback if the owner wants one ring only: 3-4 gold blunt tiles along the top of the back slabs (no spikes, no crown).
   - Test: the game-camera icon shows at least 8 gold px at 64 px (today 0).

2. **The brows are rounded tubes that read as cartoon eyebrows (L180-183).** Build them as flat stone slabs:
   - `rnd=0.14` becomes `rnd=0.06` (square ends, not tubes).
   - Shorten each half by about 10 % (half-size x 0.084 becomes about 0.076), with the inner ends still over the nose.
   - Tilt 22 deg becomes 28 deg inner-down, and drop them 0.005 so they overhang the slit sockets (ice_eye, L186-188).
   - Test: `close_low.png` and `close_front.png` show square slate lids over the slits, with no tube ends.

3. **Robot-box read on fists, pauldrons, feet and knee caps.** These read as stacked boxes and a grille.
   - **Fists (L208):** delete the JOINT_D finger-gap band. It reads as a grille across the knuckles from the front. Round the
     four curled fingers (L210-211) from `rnd` 0.45 to 0.55, and the fist (L207) from 0.36 to 0.46.
   - **Pauldron cap (L219-220):** the ICE_W slab (0.148 x 0.165 x 0.036) reads as a white shelf on a box, and it is the same
     pale-plate read as the Yeti. Reduce it to 0.12 x 0.14 x 0.030, `rnd` 0.30. Keep its three chunks (L221-223). Round the
     pauldron body (L217-218) from `rnd` 0.45 to 0.55 with a bottom taper of 0.80.
   - **Feet (L248-249):** the foot is a 0.178 x 0.222 x 0.08 box. Make it a wedge that narrows to about 0.7 width at the
     toes (-y), `rnd` 0.36 to 0.45, height 0.07. Keep the three toe blocks (L250-251).
   - **Knee cap (L243):** `rnd` 0.44 to 0.55, half-depth 0.05 to 0.04.
   - Test: front and side sheets show rounded fists, pauldrons and feet, with no stacked box edges. From above, the foot is a wedge.

## NICE (do these too)

1. **Colour lift (L18):** MAUVE (136,94,166) becomes **(146,101,178)**. Hue stays 275, saturation 0.43, brightest channel 178
   (passes 170). In game about (88,61,107). Keep PLUM (L21).
2. **Gold margin (L135):** outer radius 0.225 becomes 0.240 (or band 0.075 becomes 0.085). Target at least 32 gold px at 64 px
   by my count (today 26; gate 25).
3. **The white core reads as a star badge (L162):** the octagon at 0 deg plus the octagon at 45 deg form an 8-point star at
   close range. Drop the 0 deg square, keep the 45 deg disc and the raised diamond, so it reads as ice.
4. **Neck collar (L172):** the JOINT_D neck joint reads as a black box collar in `close_low.png`. Set `rnd` 0.45 to 0.50
   and height 0.09 to 0.07.
5. **Three dark bands per leg (L242, L245, L247):** keep the knee joint and the shin guard, and cut the ankle band (L247) to
   about 0.02 tall (`A + (0,0,0.045)` becomes `A + (0,0,0.015)`).
6. **Distinctness, colour:** ShadePanther's indigo fur (92,80,148, H 250) is about 25 deg from the Titan's hue, and the
   Cosmic Leviathan's plum (170,54,170, H 300) is about 25 deg the other way. Keep the Titan violet and do not go bluer. Note
   for the lineup. The Titan's shoulder caps and the Yeti's plates are both pale slabs, which MUST 3b reduces.
7. **Pet-facing claim:** confirm in Studio (idle pets turning to the player) before the front ring is relied on as the main view.
   If it is false, MUST 1 is a must, not a nice-to-have.
8. **Lineup check:** the LavaGolem is the same stocky golem build family (box shoulders, box fists, stubby legs). The Titan
   avoids LavaGolem's spikes and its magma-trim language, so it is a cousin, not a copy. The gold ring keeps them apart.

## Pass / fail checklist (model gate)

| Check | Result |
|---|---|
| 64 px silhouette: upright armoured giant reads at a glance | PASS |
| 128 px strip: gold ring and white ice read as the hero | PASS (front) |
| Game-camera read (behind): hero or gold visible | FAIL (0 gold, MUST 1) |
| Face: slits under a heavy brow, no round eyes, no glint, no smile | PASS (slits and pupils) |
| Face: brow reads as stone, not cartoon | FAIL (MUST 2) |
| Not cute, not a toy: no box-stack read on fists, feet, pauldrons, legs | FAIL (MUST 3) |
| Real anatomy, tapered limbs | PARTIAL (torso and ribcage taper; limbs and feet are boxes, MUST 3) |
| No box belly, belly line rises in side view | PASS (ribcage and waist taper) |
| Body colour: brightest channel 170 or more, or luminance 95 or more | PASS (luminance 115); brightest 166 (NICE 1) |
| 3-band blocking (mid body, dark plum, pale ice) plus gold | PASS |
| One big signature feature (the chest bezel) | PASS |
| Gold hero readable at 64 px (front, portrait cell) | PASS (26 px by my count, 31 by builder; thin, NICE 2) |
| Gold hero visible from behind (game camera) | FAIL (MUST 1) |
| Pale underside (FIERCE rule) or accepted exception | PARTIAL (no pale underside; ICE caps and the gold carry it; accept only if the back gold lands) |
| Value shares printed against the plan | PASS (builder's table; my check agrees within about 4 points) |
| Tier fit: above the Yeti and Roc on presence | PARTIAL (clear vs Roc; vs Yeti only from the front) |
| Distinct from Rex and Leviathan | PASS (no spikes, no crown, no cyan; violet is 25 deg from Leviathan) |
| Distinct from the Yeti | PARTIAL (both pale shoulder slabs on a dark giant; MUST 3b) |
| Floating, poking or intersecting parts (visible views) | PASS (none seen) |
| Parts visible from below | NOT CHECKED (no belly-up render; `close_low.png` is front-low only) |
| Tris 15k or under | PASS (7,000, builder's count) |
| No glow, no Neon | PASS |
| Studs everywhere, details smooth | PASS |
| Height in line with tier (10.0, equal to Rex) | PASS |
| Clip gate | not judged this round |

## Next round (send all at once)

- `_model_sheet.png` and `_close_sheet.png` (front, side, tq), plus `close_low.png` and a close-up of the brows.
- `_icons_strip_64.png` and `_icons_strip_128.png` next to ThunderRex, LavaGolem, CosmicLeviathan and GlacierYeti.
- The game-camera icon (`_icons2_strip_64.png` and `_icons2_strip_128.png`) next to BlizzardRoc and GlacierYeti.
- A belly-up render (the visible-from-below check) and a back close-up showing the new back ring.
- Flat palette shares for side, tq and game, with the new MAUVE value.
- The clip gate starts after the model is at 8/10 or better.
