## ROUND 2 (2026-10-27, after `_review/PermafrostTitan_review1.md`, REVISE 6/10) - every MUST + NICE applied

Numbers now: **7,168 tris**; H_MODEL 2.029 BU, HEIGHT 10.0, PITCH 0.0455 (unchanged). Gold at 64 px: **portrait 36**
(kit counter; brief counter 55; r1 31), **game camera (behind) 16** (r1 0; review test >= 8). Head pose test
(`pose_try`: bow 12, lift -10, yaw +/-25, bow + yaw + jaw, chest bow + head bow): **0 collisions**, ground 0.0.

Strict value shares (background AND edge / speckle pixels excluded):

| colour | side | tq | game |
|---|---|---|---|
| MAUVE | 66.0 | 63.2 | 59.9 |
| PLUM | 12.3 | 14.8 | 19.0 |
| ICE_W | 10.2 | 8.7 | 10.4 |
| JOINT_D | 7.6 | 7.4 | 7.8 |
| GOLD + GOLD_D | 1.8 | 4.3 | 1.4 (r1 0) |
| BLACK | 2.2 | 1.6 | 1.6 |

| # | item | done |
|---|---|---|
| M1 | gold on the back | a **back echo bezel** on the hump's back face (centre z 1.69, tilted 8 deg up): 12 GOLD facets, outer dia **0.21 BU (~0.10 H, 44 % of the chest ring)**, band 0.035 radial, depth 0.06, GOLD_D lining, a small octagon ice disc inside; no settings, no crown, nothing pointed. On Chest; anchor `BACK` (model() info) for a glint VFX. Game-cam icon 16 gold px. Close-up `renders/close_back.png`. |
| M2 | brows | flat slate slabs: rnd 0.14 -> 0.06, half-length 0.084 -> 0.076, tilt 28 deg inner-down, dropped 0.005 onto the sockets. `close_brows.png`, `close_browtq.png`. |
| M3a | fists | the JOINT_D finger-gap band is gone; fist rnd 0.46, fingers rnd 0.55 (note: blockkit caps rounding at 0.45 x the smallest half-size, so 0.46 / 0.55 land at that cap). |
| M3b | pauldron | ice cap 0.148 x 0.165 x 0.036 -> **0.120 x 0.140 x 0.030**, rnd 0.30; pauldron body rnd 0.55 (capped) with a **bottom taper 0.80**; the three chunks kept. |
| M3c | feet | the foot is a **wedge**: a seg from heel to toes narrowing to 0.70 width at the toes, height 0.14 (half 0.07), rnd 0.45; three toe blocks kept. |
| M3d | knee caps | rnd 0.55 (capped), half-depth 0.05 -> 0.04. |
| N1 | colour | MAUVE (146,101,178): brightest channel 178 (passes 170). |
| N2 | gold margin | chest bezel R_OUT 0.225 -> 0.240: portrait 36 px. |
| N3 | core | the 0-deg square is gone: the core is now a flat **octagon ice disc** (radius 0.119, inside the gold-dark lining so the lining no longer cuts it into a star) + the 45-deg raised diamond + a small 45-deg top facet. |
| N4 | neck collar | JOINT_D neck knuckle half-height 0.090 -> 0.070, rnd 0.50. Head poses still 0 collisions. |
| N5 | ankle band | `A + (0,0,0.045)` -> `A + (0,0,0.015)`. |
| N7 | pet-facing | not verifiable from Blender (I do not touch Studio); the back ring now carries the gold from behind either way. |

Belly-up / from-below check: `PermafrostTitan/_scratch/view_under.py` (ground hidden) -> `renders/_under_sheet.png`
(belly, low front, low back): no floating, poking or open parts; soles are studded stone, toe claws black.

Deliverables: `renders/_model_sheet.png`, `_close_sheet.png` (back ring, brows front + 3/4, chest front / low / tq),
`close_low.png`, `_under_sheet.png`, `_icons_strip_64/128.png` and `_icons2_strip_64/128.png` (next to ThunderRex,
LavaGolem, CosmicLeviathan, GlacierYeti, BlizzardRoc), `flat_*.png`, `gamelook_*.png`; numbers in
`_scratch/shares_strict.json`, `_scratch/game_icon.json`, `_scratch/model_result.txt`.

---- (round 1 notes below, kept for history) ----

