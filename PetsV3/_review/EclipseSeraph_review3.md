# Eclipse Seraph - model gate review 3 (2026-10-27) - REVISE (one short round)

**Score: 7.5/10 for a 0.1 % MYTHIC** (round 1: 5, round 2: 7; ship at 8+).

Round 3 is clearly better. The pegasus white is gone, the body and wings are a clean lilac, the dark mane frames the face, the halo reads as an eclipse, and a red accent now shows from the game camera. The Seraph is not yet the top of the Celestial egg. Against Cosmic Leviathan (1 %) it wins on the gold hero and the red accent, but it loses on chroma and dark mass. Against Solar Lion (common, 54.9 %) it is more distinct but less punchy. Three small numeric fixes (MUST 1 to 3) decide it. No concept change.

Keep: six wings (11,252 tris, builder's count), HEIGHT 11.5, the 40-degree halo with the 0.050 gold lip, the red slit eyes, the lilac face and underside, the white hand coverts as the single wing highlight.

---

## Answers to the brief's questions

- **Lion-angel, not pegasus?** At 128 px, yes: a dark mane ruff around a white muzzle with red eyes, under a gold eclipse and six lilac wings. At 64 px, borderline: it reads as a lilac winged cat with a dark ruff. The mane is still less striking than the Solar Lion's gold-spiked ruff.
- **Outclasses Cosmic Leviathan at 64 px?** Partly. It wins the gold hero (90 gold px against 20) and it has a red accent the Leviathan lacks. It loses on chroma (mean saturation 0.32 against 0.35; saturated pixels 35 % against 41 %) and dark mass (20 % against 35 %). Not yet.
- **Outclasses Solar Lion at 64 px?** No, on punch. The Solar Lion's tawny body and gold spiked mane (267 gold px, saturation 0.42) catch the eye first. The Seraph is more distinct (lilac, halo, eclipse) but less striking. A mythic has to read richer than the common, so this is the main gap.
- **Red accent visible from the game camera?** Yes. 12 red px at 64 px (builder: 15), 51 px at 128 px. The tail brush shows as a red block at the back in the game renders. It is small, but it is there.

---

## Measured (my counter; builder's counter in brackets)

### 64 px, 7-cell strip (portrait)
| item | round 2 | round 3 | target | status |
|---|---|---|---|---|
| near-white (lum > 200) | 32 % | **27 %** [22.1 icon] | <= 25 | BORDERLINE PASS (within +/-3 of the method) |
| mean saturation | 0.27 | **0.32** [0.33] | >= 0.33 | BORDERLINE (Leviathan 0.35 [0.37]) |
| saturated px (sat > 0.35) | 30 % | **35 %** | >= 41 (Leviathan) | FAIL vs Leviathan |
| dark (lum < 90) | 20 % | **20 %** [16.5] | >= 22 | FAIL (no change from round 2) |
| gold px, portrait | 82 | **90** (8.7 %) [69 / 90] | >= 20 | PASS (Leviathan 20, Frostcrown 108) |
| red px, portrait | 12 | **20** (1.9 %) [29] | >= 10 | PASS |

### 64 px, 4-cell game-camera icon
| item | round 2 | round 3 | target | status |
|---|---|---|---|---|
| gold px | 13 | **18** (2.7 %) [22 / 22] | >= 20 | BORDERLINE FAIL on my counter |
| red px | 0 | **12** (1.8 %) [15 / 14] | >= 10 | PASS |

### Flat IDs (display pose, game camera, round 3 palette)
WING_LILAC 32.6 %, BODY_MID 25.6 %, OBSID 17.8 %, MOON_IVORY 4.9 %, GOLD 3.8 %, BLACK 3.8 %, BLOOD 2.2 % (was 0.1 % in round 2), WING_IN 0.8 %.

The lilac is now the whole silhouette: about 58 % of it is lilac, and the white is 5.7 % (face plus the three hand coverts). The red brush took the BLOOD share from 0.1 % to 2.2 %.

---

## Round 2 MUST status

| # | round 2 item | result |
|---|---|---|
| M1 | upper primaries lilac, white only on the hand coverts | DONE. Near-white 27 % (mine), 22-23 % (builder). Borderline pass. |
| M2 | red element on the back (tail brush) | DONE. 12 red px game (mine), 15 (builder). Pass. |
| M3 | outer mane ring larger, dark mass to 22 % | PARTIAL. Ring grown (0.31, 0.36, 26 tufts), but the dark count did not move (20 % on my counter). FAIL. |
| M4 | body richer, saturation at least 0.33 | PARTIAL. Body is a clean lilac (190,120,226), but saturation is 0.32 (mine) against Leviathan's 0.35. Below the outclass line. FAIL. |
| NICE 2 | rim lip 0.050 to restore game gold | DONE. Game gold 18 (mine), 22 (builder). Borderline. |

---

## MUST (round 4; model only, one short round)

**MUST 1 - Chroma: outclass the Leviathan's colour (the gate that matters most).**
- Target: mean saturation at least 0.36 on my 64 px portrait (now 0.32), and saturated share at least 40 % (now 35 %).
- Lever A, body: `BODY_MID` (line 21) (190,120,226) goes to (196,112,234). Saturation 0.47 to 0.52, the same luminance (about 151 against 153), hue 281.
- Lever B, wings: `WING_LILAC` (line 22) (200,146,232) goes to (206,130,240). Saturation 0.37 to 0.46, luminance about the same.
- Lever C, if still short: widen the BLOOD corona band (line 232, `cor_o - 0.07`) to 0.09. Red is the most saturated colour on the pet, so more red lifts the mean and the saturated share, and it strengthens the accent.
- Hue stays about 280. That is 9 deg from the Shade Panther's VIOLET accent (271). No violet anywhere; accents stay BLOOD and GOLD.

**MUST 2 - Dark mass to 22 % (the lion frame at 64 px).**
- M3 grew the mane ring but the dark count stayed at 20 %. The enlarged ring's lit tufts sit above luminance 90, so the new area did not register as dark.
- Lever: `OBSID` (line 24) (46,46,70) goes to (34,34,56) for the mane tufts and the halo disc. Hue 240 is kept. The mane stays the darkest mass around the face.
- Target: dark (luminance < 90) at least 22 % on my 64 px portrait. The builder should measure on the same counter, since the reviewer's counter is the gate.

**MUST 3 - Game-camera gold at 20 px on my counter.**
- The rim band is `rim_i = HALO_R - 0.075` (line 213). Widen it to `- 0.085` (+13 %). The corona follows the rim inward (`cor_o = rim_i`), and the radial change leaves the head and mane clearance and the top height unchanged.
- Target: at least 20 gold px in the 64 px game-camera icon on my counter (now 18).

**MUST 4 - Keep the halo clearance at 0.05 or more.** Head clearance is 0.050 BU, exactly at the minimum. No change needed this round, but any edit to tilt, centre or rim must re-check it.

## NICE
1. **Tail brush shape.** In the side and game renders the BLOOD brush reads as a red block or ball rather than a brush (block `(0.12, 0.13, 0.11)` at line 329, tufts 0.07 wide at line 332). Shrink the block to about (0.10, 0.11, 0.095) and lengthen the tufts by about 0.03, so it reads as a brush from behind.
2. **Halo margin.** Add 0.01 BU of head clearance if it costs nothing else.
3. **Lower pair and display pose.** Good. No change.

---

## Pass / fail checklist (round 3)

| item | result |
|---|---|
| 64 px species reads as lion-angel (not pegasus) | BORDERLINE (lilac winged cat with a dark ruff) |
| 128 px: halo, mane, face, six wings | PASS |
| Fierce, not cute | PASS |
| Face red eyes at 64 px | PASS (portrait red 20 px) |
| No box belly, rising belly line | PASS |
| Smooth gold, red, feather tips; no Neon, no glow | PASS |
| Palette follows the plan | PARTIAL (lilac body is a planner-approved deviation; ivory down from the plan's 40 %) |
| Dark rich body + pale underside + one bright accent | PASS (dark rich lilac body, ivory face and underside, red and gold accents) |
| 3-band colour blocking | PASS (dark mane and halo / lilac / gold and red) |
| Accent visible from the game camera | PASS (12 red px, red tail brush) |
| Gold hero at 64 px, portrait | PASS (90 px) |
| Gold hero at 64 px, game camera | BORDERLINE (18 on my counter, 22 on the builder's) |
| Dark mass (lion frame) at least 22 % | FAIL (20 %) |
| Chroma at least the 1 % Leviathan | FAIL (0.32 against 0.35) |
| Outclasses Cosmic Leviathan at 64 px | PARTIAL (gold and red win; chroma and dark lose) |
| Outclasses Solar Lion at 64 px | FAIL on punch (more distinct, less striking) |
| Distinct from Shade Panther (violet) | PASS (hue 280 body, no violet accent) |
| Six wings: tris <= 15k, countable | PASS (11,252 tris, builder's count) |
| Floating, poking or intersecting parts | PASS (builder's cut-through 0; halo head clearance 0.050, at the minimum) |
| Name is two words | PASS |

---

## Next round: send with
- `_icons_strip_64.png` (7 cells) and `_icons2_strip_64.png` / `_128.png` (4 cells), with the raw and strip counts for near-white, saturation, saturated share, dark, gold and red.
- `flat_game.png` and `flat_side.png` with the value shares.
- `_idle_sheet.png` and `_close_sheet.png`.
- A game-camera render from behind and above (the view that must show the red brush).
- The tri count and the halo clearance numbers.

**Bottom line:** REVISE at 7.5/10. The Seraph now reads as a lion-angel at 128 px and carries a red accent the game camera can see. It does not yet outclass the Cosmic Leviathan on colour richness or the Solar Lion on punch. MUST 1 (chroma), MUST 2 (dark mass) and MUST 3 (game gold) are small numeric edits. Ship at 8 or above only after round 4 meets all three.
