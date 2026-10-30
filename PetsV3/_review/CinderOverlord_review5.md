# Cinder Overlord - model round 5 review (2026-10-27) - REVISE

**Verdict: REVISE. Score 7/10** (round 4 was 7/10). Target to ship: 8/10 or better.

The palette change clears the Fire egg: no Fire-egg colour sits within 40 degrees of the new accent, and the Phoenix's ember and lava copies are gone. But the sulfur-blue family is already taken by other pets, and the blue core copies a Glacier and a 1 % secret colour. At game distance the blue vents also read as ice rather than fire. One MUST blocks the pass: sibling clearance for the blue colours. Everything else in round 5 is fixed or acceptable.

## 0. What I looked at

- Round-5 notes (`CinderOverlord/MODEL_NOTES.md`, "ROUND 5"), `_scratch/gate_r5.json` (the only gate file; `gate_r4.json` is renamed `STALE_r4_gate_r4.json`), `_scratch/gold_windows_r5.txt`, `_scratch/accent_cmp.png`.
- Renders, all dated 22:53-22:54 and newer than the source `pets/CinderOverlord.py` (22:52): `_model_sheet.png`, `close_front.png` and `_close_sheet.png`, `_icons_strip_64.png` / `_128.png`, `_icons2_strip_64.png` / `_128.png`, `_molt_r4_front|side|tq.png`, `gamelook_game.png`, `gamelook_tq.png`.
- Source colours (`pets/CinderOverlord.py` lines 18-27) and every sibling's RGB in `pets/*.py`, including the Glacier pets and the 1 % secrets. Hue distances computed from the RGB values.

Not verified:
- The rendered gold hue window (H 48-60) and the blade-height change come from the builder's counter; I did not re-measure pixels.
- The clip numbers are unchanged from the round-4 pass (the clip gate is at 8/10 and was not re-opened).

## 1. Round-4 MUSTs

| # | Round-4 MUST | Round-5 result | Verdict |
|---|---|---|---|
| 1 | Accent off the Phoenix EMBER (3.4 deg) | Accent is now (40,160,255), H 207. The Phoenix's nearest colour is now 40 deg away (BlackDragon INK, H 247). But the accent is 2.8 deg from **Kraken EYE / RING (40,150,255)**, a near-identical RGB. | **PARTIAL** (MUST 1) |
| 2 | Cores off the Phoenix LAVA | Cores are (140,220,255), H 198. They are no longer a Phoenix copy, but they sit **5.7 deg from ThunderRex CYAN (60,214,255)** and **7.4 deg from FrostfangLynx ICE (150,236,255)**. | **PARTIAL** (MUST 1) |
| 3 | Gold: one counter, tight window, blends excluded | Team counter (H 29-58, s>0.5, v>0.45): **portrait 27** (gate 25), **game 19**. None of the 27 pixels lie in the H 29-38 blend band. Tight window H 38-48 gives 7 / 8 (the builder's reported counts; reproduced by the gold-window file). | **PASS** on the team counter; the tight window cannot gate any pet (see section 4) |
| 4 | All renders from the current model | Renders 22:53-22:54 are newer than the source (22:52) and the gate file (22:54). `_molt_r4_*` and `close_front` are current. | **PASS** |

## 2. Colour: sibling clearance (the blocking item)

The builder's rule was 15 degrees from every Fire-egg colour. The Fire egg is clear: the nearest Fire-egg colour is 40 deg away. But the lineup rule is "never copy a sibling's accent", and the blue zone is crowded. Hue distances (degrees), from `pets/*.py`:

| Colour | RGB | Hue | Distance to accent (207) | Distance to core (198) |
|---|---|---|---|---|
| **Kraken EYE / RING** | (40,150,255) | 209 | **2.8** | 11.0 |
| **Kraken EYE_HOT** | (176,216,255) | 210 | **3.1** | 11.3 |
| **ThunderRex CYAN** (1 %) | (60,214,255) | 193 | 13.9 | **5.7** |
| **FrostfangLynx ICE** (Glacier, 50 %) | (150,236,255) | 191 | 15.6 | **7.4** |
| **Thunderbird TEAL** (Storm) | (36,138,160) | 191 | 15.9 | **7.7** |
| **IceMammoth CHAR_TEAL** (Glacier) | (96,168,184) | 191 | 15.6 | 7.4 |
| **ThunderRex DEEP** (1 %) | (34,110,230) | 217 | **10.2** | 18.4 |
| **Thunderbird STORM** | (26,80,100) | 196 | 10.3 | 2.1 |
| **CosmicLeviathan AZURE** (1 %) | (90,148,255) | 219 | **12.4** | 20.6 |
| **FrostcrownDragon STEEL_BLUE** (Glacier, 0.1 %) | (62,104,176) | 218 | 11.4 | 19.6 |

What this means:
- The accent is a near copy of Kraken's eye and ring blue. Kraken is a live pet, so this is the same copy the rule forbids.
- The core is inside 8 degrees of the ThunderRex CYAN, the Frostfang ICE and the Thunderbird TEAL. Two of those are other rare or Glacier pets.
- The accent is 10-12 degrees from both 1 % secrets (ThunderRex DEEP, Leviathan AZURE) and from the Frostcrown. Those are the pets the Cinder must outclass.
- The whole band from H 187 to 222 is occupied by at least ten pets, so no blue can clear 15 degrees of all of them.

**Ruling: the blue family is not separable by hue.** Keep the sulfur concept only if the Cinder can be distinct in value and saturation, which the current accent is not (its value 255 and saturation 0.84 match Kraken's eye).

## 3. Fire read

- At 128 px the ember body with the blue slits reads as a red serpent with cold crystal points, and the crown is gold. The blue reads distinct from the Phoenix and Ivonrath. Accept.
- At game distance (`gamelook_game.png`) the blue vents read as **ice crystal**, not fire. The body is a dark ember and the vents are the only fire signal, so the identity is weakened where the player sees it. The "blue-hot" rationale (complement of the orange body) is right for contrast, but the read is cold.
- The core (140,220,255) is pale cyan. Pale cyan is the Glacier egg's colour (FrostfangLynx ICE, Permafrost ICE), so the Fire-egg pet is borrowing the new area's signature. That is a copy problem as well as a read problem.

## 4. Gold

- The team counter gives 27 on the portrait and 19 on the game camera. The round-4 blend inflation is gone: none of the 27 pixels lie in H 29-38. Pass.
- The tight window (H 38-48, s >= 0.6) gives 7 on the portrait. The builder's reason is correct: the rendered gold highlights sit above H 48. So a tight window cannot gate the pet, and the team counter is the only usable gate.
- Rendered window (H 40-62, s >= 0.6, v >= 0.55), from `gold_windows_r5.txt`: **21** on the portrait, 8 on the game camera. The team counter and the rendered window both put the portrait above 20, so the gold read is real.
- **Hero at 64 px:** yes. The yellow five-blade crest is the tallest and brightest mass in `_icons_strip_64.png` and in `_icons_strip_128.png`. It reads as the hero of the pet.

## 5. Shares (game view, `gate_r5.json`)

- Body **40.4 %** (floor 40): passes, with 0.4 points of margin. The taller crown and the blue points took share from the body. Accept, but it is borderline (NICE 2).
- Obsidian **35.1 %** (ceiling 40): passes.
- Blue accent 6.8, blue cores 3.5, gold 5.1 + 0.9, pale 2.2: consistent with the render.
- Side and tq: body 47.7 / 39.7, obsidian 23.4 / 26.8, pale 10.8 / 12.2. Pass.

## 6. Distinct from the Phoenix, Ivonrath, and every sibling

- **Phoenix (2 %):** accent and cores distinct (no ember or lava copy is left; the nearest Fire-egg accent colour is 40 deg away). The body is 5.5 deg in hue from the Phoenix's EMBER body, separated by value (166 against 232) and silhouette: partial, accepted with the same reasoning as Ivonrath.
- **Ivonrath (4 %):** partly. The body (166,66,50) is 7.5 deg from Ivonrath RED (H 1). Separated by value (166 against 198), saturation (0.70 against 0.80) and silhouette (a wingless serpent against a winged wyrm). Accept, as in round 4.
- **Every other sibling:** not yet. See section 2.

## 7. Rarest Fire pet, and outclassing

- **Rarest:** yes by odds (0.5 %, against the Phoenix's 2 %). The rarity is visible: the crown is the tallest mass in the egg and the blue points are the only cold colour in the egg.
- **Outclass on impact:** partly. At 128 px the Cinder is a thin red serpent, and the Phoenix's flame and ThunderRex's blue are more striking. The blue points help at 64 px. This is a judgement for the owner once the colour clearance is fixed.

## 8. MUST list (prioritized)

**MUST 1 - Sibling clearance for the blue colours (blocks the pass).**
- The accent (40,160,255) is 2.8 deg from Kraken EYE / RING (40,150,255) and 3.1 deg from Kraken EYE_HOT. The accent is 10-12 deg from ThunderRex DEEP, CosmicLeviathan AZURE and Frostcrown STEEL_BLUE. The core (140,220,255) is 5.7 deg from ThunderRex CYAN, 7.4 from Frostfang ICE and 7.7 from Thunderbird TEAL.
- Rule to apply: every Cinder colour at least 15 deg from every pet's colour in `pets/*.py` (the 1 % secrets and the Glacier pets included), with an owner exception for any that cannot clear.
- The blue zone H 187-222 cannot clear all of them. So the builder must either (a) find a hue outside it that clears the 15-degree rule against the full lineup (run the table over every pet, not only the Fire egg), or (b) keep blue and separate it by value and saturation from Kraken's eye and ThunderRex's cyan (for example a deeper, less saturated blue on the slits), and show that in the 64 and 128 px strips.
- Deliver the table with the chosen hues.

**MUST 2 - Fire read at game distance (lead's decision).**
- At 5 studs the blue vents read as ice crystal (`gamelook_game.png`). If the lead keeps blue, the fire signal must come from the vents' hot centres: a warm centre inside the blue rim, with the centre itself clear of 15 degrees from every Fire-egg colour and from the Glacier pets' ICE.
- If the lead does not want a warm centre, accept the cold read and say so to the owner.

## 9. NICE list

1. **Ivonrath proximity.** The body is 7.5 deg from Ivonrath's crimson. Keep the saturation at or below 0.70 and luminance at or below 94 (do not lift it).
2. **Body share margin.** Body 40.4 % against a floor of 40. Give it about 2 points of margin, for example by thinning the crown's blue inner lines (CROWN_IN) or the blue vent slits, so the next change cannot push it under the floor.
3. **Report the rendered gold window** (21 on the portrait) next to the team counter (27), so the gate reads as two agreeing numbers.
4. **Molt readability.** The blade lift is visible in `_molt_r4_side.png` (the centre blade rises and the outer blades drop back). The blue crown lines read well in the front view. No change needed.

## 10. Pass / fail checklist (round 5)

| # | Check | Result |
|---|---|---|
| 1 | Tris <= 15k | PASS (10,852) |
| 2 | Height 10.5, tallest of the Fire egg and of the secrets | PASS |
| 3 | Collision free, ground >= -0.02, loops closed | PASS (builder's, clip gate unchanged) |
| 4 | Renders current (newer than the source and the gate file) | PASS |
| 5 | Gold >= 25 at 64 px (team counter) | PASS (27 portrait; 19 game) |
| 6 | Gold reads as the hero at 64 px | PASS (yellow five-blade crest) |
| 7 | Game shares: body >= 40 %, obsidian <= 40 % | PASS (40.4 / 35.1), margin 0.4 |
| 8 | Accent distinct from every Fire-egg colour | PASS (nearest 40 deg) |
| 9 | Accent distinct from every sibling (15 deg) | **FAIL** (Kraken 2.8, ThunderRex 10.2, Leviathan 12.4) |
| 10 | Core distinct from every sibling (15 deg) | **FAIL** (ThunderRex CYAN 5.7, Frostfang ICE 7.4, Thunderbird TEAL 7.7) |
| 11 | Body distinct from Phoenix | PARTIAL (body is 5.5 deg in hue from the Phoenix's EMBER body; separated by value (166 against 232) and silhouette; accent and cores are clear) |
| 12 | Body distinct from Ivonrath | PARTIAL (7.5 deg; value and silhouette separate them) |
| 13 | Reads as FIRE at 128 px | PASS |
| 14 | Reads as FIRE at game distance | **PARTIAL** (blue vents read as ice; MUST 2) |
| 15 | Fierce, not cute | PASS |
| 16 | Outclasses the Fire egg at 64/128 px | PARTIAL (rarest by odds; not the most impressive yet) |

## 11. Next round

Send with the fixes applied:
- the colour table (every Cinder colour against every pet, 15-degree rule) with the chosen accent and core hues (MUST 1);
- a 64 and 128 px strip with the new colours, next to Kraken, ThunderRex, Leviathan, Frostfang, Phoenix and Ivonrath (MUST 1);
- the game-camera look with the lead's decision on the warm centre (MUST 2);
- the body share with its margin (NICE 2).

The model goes to the owner at 8/10, after MUST 1 and 2 pass.
