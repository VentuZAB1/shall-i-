## ROUND 2 (2026-10-27, after `_review/CinderOverlord_review1.md`, REVISE 5/10) - every MUST + NICE applied

Numbers now: **11,124 tris**; H_MODEL 2.210 BU (the crown blades grew 12 %), HEIGHT 10.5 studs (unchanged), stud pitch
0.0472. Gold at 64 px: **portrait 28** (kit counter; brief counter 50), **game camera 19** (r1 16). Gate >= 25: PASS.
Crown + neck pose test (`pose_try`, 8 poses: alternating lifts A/B, all blades 35 deg up, all 35 deg forward, neck bow +
blades, look yaw, look-up + blades): **0 collisions in every pose**, ground_min_z -0.006 (Tail3, at rest).
Sheet: `renders/_pose_crown_sheet.png` (rest / all up / all forward / bow / look-up).

Strict value shares (`PermafrostTitan/_scratch/shares.py`: background AND anti-aliased edge / speckle pixels excluded):

| colour | side | tq | game | plan / review target |
|---|---|---|---|---|
| PLUM_OBS (body) | 45.9 | 39.6 | 28.0 | 44 |
| OBS_D (obsidian) | 30.0 | 31.6 | 53.5 | 16 (review: "deeper obsidian-dominant" fallback, see M1) |
| PALE_S | 7.7 (+ IVORY-matched shade 1.9) | 9.5 (+2.0) | **0.6** | 10 / game >= 4 (see M7) |
| ROSE + ROSE_H | 6.6 | 5.6 | 7.0 | ~6 (review ruling) |
| LAVA | 1.7 | 1.1 | 1.1 | < 2 |
| GOLD + GOLD_D | 2.2 | 6.5 | 5.4 | 3 |

| # | item | done |
|---|---|---|
| M1 | body off the Leviathan magenta | PLUM_OBS first set to the review's (150,84,110); the 64 px portrait **still read pink**, so per the review's own fallback ("deeper obsidian-dominant, not lighter") it went to **(144,80,96)** (H 345 oxblood, S 0.44, luma 101 >= 95; 45 deg off the Leviathan's H 300) AND an **obsidian dorsal saddle** (OBS_D band over the top of every body/tail segment and the back of the neck, rings drop from it down the flanks) + an **obsidian skull cap** brow-to-crown. Game view is now dark obsidian back + wine flanks + lava vents. |
| M2 | crown not a tiara | gold only on the two upper edges of every blade + the two sides of the centre blade (outer side frames on blades 1/2/4/5 gone). To hold the >= 25 px gate the remaining gold edges are wider (half 0.016 -> 0.025) and the blades 12 % taller (0.17 / 0.215 / 0.28); rose inner lines moved in (0.66) so the wider gold does not cover them. |
| M3 | Fire read | `LAVA = (255,128,24)`: the hot core line of all 24 vent slits + the tail ember tip. ROSE_H stays only on the centre crown gem. |
| M4 | rose ~6 % | slits `w = 0.060*sc + 0.014`, `L = 0.22*sc + 0.04` exactly as ruled; the pair spacing now scales with the slit width (gap ~0.25 w) so the doubled slits stay two slits; raised to 24 deg on the flank (clear of the wider pale band). No stripes. Rose 6.6 % side / 7.0 % game. |
| M5 | head not a brick | the literal numbers (front half-size 0.115, rnd 0.50) would not have changed the read: blockkit caps rounding at 0.45 x the smallest half-size, so the box only got smaller. The skull is now a **lofted wedge** (8 superellipse stations, n 2.8): widest at the cheeks (0.40 wide), tapering + dropping to a **squared muzzle** (side view = a crocodile / dragon wedge). Jaw lofted too (tapers with the snout), jaw-muscle boxes -> smooth ellipsoid bulges, the boxy OBS_D cheek plates removed, nostrils sit on top of the muzzle (no pig-snout read from the front). Close-ups: `renders/_close_sheet.png`. |
| M6 | bulk | `RAD[0..4] = 0.265, 0.250, 0.230, 0.205, 0.180` (+15 %), tail radii unchanged; the rearing neck thickened with it (`FRAD` +~10 %: 0.268 ... 0.180) and the forearms moved out/forward with the thicker chest. Vents, rings, scutes, spikes follow the radii. |
| M7 | pale underside in game | arc widened to **188-352 deg** on Spine..Body4 (200-340 on Tail1), `PALE_S = (245,236,240)`. Side 7.7 %, tq 9.5 %, **game 0.6 %**. The game camera sits behind and ~38 deg above a serpent lying on its belly: geometrically it only sees the lower flank down to ~-27 deg on the side facing it and nothing below the equator on the other side. Reaching 4 % in game would need the pale band at/above the equator on both flanks (a pale lateral stripe, which would also run into the vents = candy stripes). I stopped at 188-352 and ask the reviewer to judge the 3-band read from `gamelook_game.png` (dark back / wine flanks / lava vents / gold crown) instead of a game pale share. |
| M8 | BlackDragon in the strips | BlackDragon is first after the Cinder in `_icons_strip_64/128.png` and `_icons2_strip_64/128.png` (then Boar, Golem, Cerberus, Ivonrath, Phoenix, Rex, Leviathan). |
| N1 | tail rings | Tail1-4 ring band 0.60-0.80 (body keeps 0.52-0.86). |
| N2 | beams | nasal ridge now a thin 0.02-wide OBS_D ridge on the muzzle tip only; the crown mount is two tapered halves (0.068 high at the centre -> 0.04 at the ends), side blocks smaller. |
| N3 | brow points | each brow has an OBS_D forward point at its inner-front end (angry V). |
| N4 | eye slits | rose slit 0.074 -> 0.085, socket 0.088 -> 0.098. |
| N5 | molt check | done above: 35 deg lifts at the fatter body = 0 collisions. |

Deliverables: `renders/_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64/128.png`, `_icons2_strip_64/128.png`,
`flat_side/tq/game.png`, `gamelook_game.png`, `gamelook_tq.png`, `_pose_crown_sheet.png`; numbers in
`_scratch/shares_strict.json`, `_scratch/game_icon.json`, `_scratch/model_result.txt`.

---- (round 1 notes below, kept for history) ----

