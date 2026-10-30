# Permafrost Titan - model gate review 2 (2026-10-27) - APPROVED WITH FIXES (model)

**Score: 7/10 for a 2.5 % SECRET** (round 1 was 6/10). Ship at 8/10 or better.

Round 1 landed well. The back now carries gold, the brows are stone slabs, the fists lost the grille, the core reads as ice
rather than a star, and the feet are wedges. The front is strong. From behind, though, the Titan does NOT yet clearly
outclass the Yeti: the Yeti's back has about twice the pale mass, and the Titan's only rarity cue there is a small gold ring.
Two code-level MUSTs fix that (back gold size, back pale mass). They are small, so this is a short round 3 on the back views
and game-camera icons, not a full model round.

## What I looked at

- Code: not re-read this round. Judged from the renders and the builder's ROUND 2 notes in `PermafrostTitan/MODEL_NOTES.md`.
- Titan renders (round 2, 17:25): `_model_sheet.png`, `_close_sheet.png`, `close_back.png`, `model_back.png`, `model_side.png`,
  `_under_sheet.png` (belly-up, low front, low back), `_icons_strip_64/128.png`, `_icons2_strip_64/128.png` (game camera),
  `flat_side.png`, `flat_game.png`, `gamelook_game.png`.
- Comparison, Yeti (CURRENT, 17:31 render): `GlacierYeti/renders/model_back.png`, `_model_sheet.png`, `_icons_strip_64/128.png`.
  The Yeti is at round 2 and `_review/GlacierYeti_review2.md` gave it APPROVED WITH FIXES 7/10 (its own side-profile MUSTs
  are still open). So the bar to clear is 7/10, not the round-1 5/10 I used last time.
- Roc: `_review/BlizzardRoc_review2.md` exists; not re-read here, it is a 7.4 % high tier and not the question this round.

## Measured facts

- Gold at 64 px, portrait cell: **32 px** by my hue count (builder's kit count 36). Gate 25. PASS.
- Gold at 64 px, game-camera cell: **14 px** by my count (builder 16). Gate 8. PASS, but small.
- Gold at 128 px, game-camera cell: 71 px in the ring region. The ring reads as a yellow ring on the hump.
- Back ring solid, not a hole: the ring centre is (175,201,230). It matches the ice caps in the same close-up
  ((174-176, 200-202, 230)). The sky is (197,214,235). So the ice disc is solid ice in shade. PASS.
- Back-view colour share, same crude mask on the same back camera (`model_back.png`, about +/-3 points):

| | pale ICE | gold | mint (Yeti accent) |
|---|---|---|---|
| Titan | **8.1 %** | 1.2 % | - |
| Yeti | **16.3 %** | - | 2.2 % |

- Flat palette: MAUVE is now (146,101,178) in `flat_side.png` and `flat_game.png`. Brightest channel 178, which passes the
  170 rule. The builder's strict value shares were not re-counted this round. In-game preview: the dominant purple bucket is
  still about (72,64,104), so the lift barely shows in game.
- Tris 7,168 (builder's count, not re-measured). Cap 15k. PASS.
- Height 10.0 (unchanged). Above the Yeti (9.0) and the Roc (9.0). PASS.

## Round-1 MUST check

| # | Item | Result |
|---|---|---|
| M1 | Gold on the back | Built: 0.21 BU ring, 14 px in the game-cam 64 cell (gate 8). PASS as a gate; the outclass margin is thin (MUST 1). |
| M2 | Brows: flat slabs, 28 deg | PASS. No tube ends. They still read as a dark visor band at 64 px, which is acceptable. |
| M3a | Fists: no grille band | PASS. Four finger nubs with white knuckle crusts read as fingers from the front. |
| M3b | Pauldron cap smaller | PASS. The cap now reads as crust, not a shelf. But it also cut the back's pale mass (MUST 2). |
| M3c | Feet: wedge | PASS in `model_side.png` and `_under_sheet.png`: the toes narrow, the claws are black. |
| M3d | Knee caps rounder | PASS. |
| N1 | Colour (146,101,178) | PASS in the palette (brightest 178). Game-preview dominant unchanged (NICE 3). |
| N2 | Gold margin (chest 0.240) | PASS. 32 px portrait. |
| N3 | Core: octagon disc, no star | PASS. The close-up reads as a faceted ice gem. |
| N4 | Neck collar | Builder says done. Not re-checked here. |
| N5 | Ankle band | Builder says done. One thin band is visible at the ankle in `model_side.png`. PASS. |
| - | Belly-up / from below | PASS. `_under_sheet.png`: no floating, poking or open parts; soles are studded; toe claws black. |

## The outclass question: the Yeti from behind

**Not yet clearly.** The Titan's back is still a purple giant with a small gold ring and white shoulder caps. The Yeti's back
is a navy ape with big pale shoulder plates, mint seams and a pale hump plate. Measured:

- **Gold vs mint.** The Titan wins on colour code. Gold is the hero colour, and the Yeti's back has no gold at all. This is
  the real separation, and the ring is visible at 128 px from behind.
- **Pale mass.** The Yeti wins clearly. Its back is about twice as pale (16 % vs 8 %). Its shoulder plates read as big
  silhouette. The Titan's caps were shrunk in round 1 for the box read, and that left the back quiet.
- **Height.** The Titan wins: 10.0 vs 9.0. It is not visible from behind in these views, though.

So from behind the Titan is a tie on presence and a win on colour, and the gold is too small to carry a clear outclass. Two fixes
make it clear: a bigger back gold ring (MUST 1), and pale back mass restored (MUST 2). Neither needs a bone, joint or clip change.

## MUST (in priority order)

1. **Back gold ring is too small to outclass the Yeti from behind.** Currently 0.21 BU outer diameter (about 0.10 H, 44 % of the chest
   ring's 0.48 BU), 14 px from the game camera at 64 px.
   - Enlarge the back echo ring to **0.25 BU outer diameter** (about 0.12 H, 52 % of the chest ring). Same construction (12 GOLD
     facets, GOLD_D lining, octagon ice disc, no settings), tilt 8 deg, centre z about 1.69. Keep it a ring. No spikes, no crown.
   - The chest ring stays the bigger hero (0.48 BU), so the front is still the signature and the back is the echo.
   - Check collisions with the back slabs (L114-119) and the top crust chunks (L124-127); run the collision locator.
   - Target: at least **20 gold px** in the game-camera 64 cell by my hue count (14 now). The ring must read clearly in the 128
     game-camera cell.

2. **Back pale mass: the Titan's back is about half as pale as the Yeti's.** Pale share from behind: 8 % vs 16 % (same mask,
   same camera). The round-1 pauldron cap cut (0.148 x 0.165 x 0.036 to 0.120 x 0.140 x 0.030) was right for the box read, but it
   left the back quiet.
   - Restore some pale volume on the shoulder caps: **0.130 x 0.150 x 0.033**, keeping `rnd` 0.30 and the three chunks. Do not
     restore the flat slab.
   - Do NOT add spikes or crown-like points on the hump to add pale mass. Keep the hump chunks blunt and flat-topped, as now.
   - Target: back pale share at least **11 %** on the same camera and mask.

## NICE (do these too)

1. **Legs still stack three plates each from the side** (thigh plate L239-240, knee cap L243, shin guard L245). Thin the shin guard
   depth from 0.034 to about 0.028. Keep the knee cap as is. This is the last of the stacked-box read in `model_side.png`.
2. **Chest and pelvis read as stacked blocks in side view.** The ribcage and waist taper (L103-108) is fine. Only the front face
   reads flat. A small extra taper (bot 0.70 to 0.66) on the chest block would soften the box read. Optional.
3. **In-game colour does not show the lift.** The flat palette is (146,101,178) but the game-preview dominant bucket is still
   about (72,64,104). Check the lift in the Studio game view at the clip gate. If it still reads dusky, lift MAUVE once more, to
   about (156,108,188). Keep the hue.
4. **Brows at 64 px** read as a dark visor band rather than two brows. Optional: a touch more slant (28 to 30 deg).
5. **Pet-facing claim (round 1, NICE 7)** is still unverified. Keep the back gold as the main rarity cue until Studio confirms
   the idle turn-to-player.

## Pass / fail checklist (model gate, round 2)

| Check | Result |
|---|---|
| 64 px silhouette: upright armoured giant reads at a glance | PASS |
| Gold hero readable at 64 px, front portrait cell (32 px, gate 25) | PASS |
| Gold visible from behind, game-camera 64 cell (14 px, gate 8) | PASS as a gate |
| Gold back ring big enough to outclass the Yeti from behind (target 20 px) | FAIL (MUST 1) |
| Back pale mass comparable to the Yeti (target 11 %, now 8 %) | FAIL (MUST 2) |
| Back ring is solid ice, not a see-through hole | PASS (centre matches the ice caps) |
| No crown, no spikes, no cyan, no glow, no Neon | PASS |
| Face: slits under a flat stone brow, no round eyes, no glint, no smile | PASS |
| Brows read as stone, not cartoon tubes | PASS (round 1 MUST 2 landed) |
| Fists and feet not boxes or grilles | PASS (wedge feet, no finger grille) |
| Legs read as tapered limbs from the side | PARTIAL (three stacked plates per leg, NICE 1) |
| Chest and pelvis: no box belly, belly line rises in side view | PARTIAL (front face flat, NICE 2) |
| Body colour: brightest channel 170 or more (flat palette 178) | PASS |
| In-game colour shows the lift | PARTIAL (NICE 3) |
| 3-band colour blocking (mid body, dark plum, pale ice) plus gold | PASS |
| Tier fit: above the Yeti (14 %) on presence | PARTIAL (front yes; back not yet, MUST 1 and 2) |
| Tier fit: above the Roc (7.4 %) | PASS |
| Distinct from Thunder Rex and Cosmic Leviathan | PASS |
| Floating, poking or intersecting parts (visible views and belly-up) | PASS (`_under_sheet.png`) |
| Tris 15k or under | PASS (7,168, builder's count) |
| Height in line with tier (10.0) | PASS |
| Clip gate | not judged this round |

## Next round (a short round 3, back views and icons only)

- `model_back.png` and `close_back.png` with the enlarged back ring, and the pale back share (same mask, same camera).
- `_icons2_strip_64.png` and `_icons2_strip_128.png` (game camera) next to GlacierYeti.
- The collision-locator result for the back ring and the shoulder caps.
- The full model gate is not needed again. Clips start after the back is at 8/10 or better.
