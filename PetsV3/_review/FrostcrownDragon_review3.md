# Frostcrown Dragon - model gate review 3 (2026-10-27) - APPROVED WITH FIXES

**Score: 8/10 (ship at 8).** The crown is now the hero. It reads as a gold crown from the side, from behind and in the
tq view: five points stand on the band in tq, the horns sweep back from the skull edge, and the V of ears is gone. Gold is
clearly ahead of both 1 % secrets. Fins and the frost core read well. Two small MUST items remain. The outer two front
crown points are hidden, and the dark top band does not separate from the flanks in `model_game`. Both are small, specific
code changes. Verify them with one re-render. No new full review round is needed.

## Answers to the lead's questions
1. **Crowned ice-dragon mythic?** Yes. Gold crown in three views, seven white crystal fins, a chest crystal core, and a
   white crystal tail. At 64 px the gold crown and the white fin row read at once.
2. **Outclasses everything below it?** Partly. Gold and crystal are clearly ahead of Thunder Rex and Cosmic Leviathan.
   Value is not: the portrait sits between the two secrets (see the table). The fix is M2.
3. **Is the dark top separate from the flanks in `model_game`?** No, not clearly. Sampled on the spine, the back and neck read
   about (67-73, 89-94, 155-159). The flank reads about (70-74, 103-109, 170-175). The gap is roughly 10-15 luminance points.
   The dark is now carried by the legs, not the back. The target is 20 or more.

## Round 2 MUST status
- **M1 crown front: PARTIAL.** Five points show in `crown_tq` and the back ring shows in `crown_game`. From the front I count
  three points: the centre and the inner pair. The outer pair at the band ends is hidden. The cause is the horn roots:
  `P[0]` = (s*0.17, 0.05, 0.10) with base radius 0.092 puts the root's inner face at about |x| 0.08, over the outer points at
  x +/-0.10. **Still a MUST (M1 below).**
- **M2 belly rungs: DONE.** No DARK bars on the chest. The hex core is the only chest feature (`_core_sheet.png`).
- **M3 value: PARTIAL.** Portrait mean luminance is 111 on my count and 114 on the builder's, against a target of 110. Dark
  share is 24 % (mine) and 22 % (builder), against 28 %. Rex and Leviathan swap order between our two counts, so value is
  level, not outclassed. **Still a MUST (M2 below).**
- **DEEP_STEEL on the whole legs (deviation R2): ACCEPT.** It is the Rex-style dark-socks recipe, and it adds value contrast on
  the lower body. The side view now shows dark legs under a mid-blue torso. That is acceptable, but the back must be the
  darkest part of the torso (M2).
- **N1 shell pad 0.030: REVERTED by the builder.** Correct; it cut into the folded wings.

## Measurements (128 px and 64 px strips, same method; my counts are approximate)
| Icon | Frost r3 (mine / builder) | Thunder Rex (mine / builder) | Cosmic Leviathan (mine / builder) | Verdict |
|---|---|---|---|---|
| Mean luminance, 128 px portrait | 111 / 114 | 118 / 107 | 108 / 116 | level, between the two (target <= 110) |
| Dark share (lum < 70), 128 px portrait | 24 % / 22 % | 11 % / 18 % | 22 % / 12 % | most dark mass (target 28 %) |
| Ice-white share, 128 px | 8.4 % / 8.4 % | 5.3 % / 3.7 % | 4.3 % / 4.2 % | ahead (target 9 %, a miss) |
| Gold share, 128 px | 2.8 % / n.a. | 0.6 % / 1.0 % | 1.2 % / 2.3 % | ahead |
| Gold px at 64 px, portrait (strict) | **41** / 85 | 4 / n.a. | 11 / n.a. | clearly ahead |
| Gold px at 64 px, game camera | n.a. / **27** | n.a. | n.a. | 27 passes the gate of 25; 40 waived by the lead |

The game-camera icon measures about lum 83-90 and dark share 42-47 % on my count. Rex and Leviathan have no same-camera game
icon in the strips, so I cannot compare game icons directly.

## What is strong (keep these)
- Gold crown read in three views. From the side the swept gold horns and band read as a crown. From behind the gold ring with
  its spikes reads as a crown, not as ears.
- Seven white crystal fins: visible from the side, the back and the game view.
- The hex frost core is a clean, single chest focal point.
- The white tail crystal reads at the back of the game view.
- Gold share is ahead of both secrets, which satisfies the hero-piece rule.

## MUST (round 4, in priority order)

### M1 - Front crown: all five points clear of the horn roots
- Cause: `P[0]` = (s*0.17, 0.05, 0.10) in `pets/FrostcrownDragon.py` (L269-270). Its base radius (0.092) covers |x| 0.08-0.26
  in front view, over the outer points at x +/-0.10 (L283-284).
- Fix: move the root out and keep the sweep:
  - `P[0]` x: 0.17 -> **0.21** (`HC + Vector((s * 0.21, 0.05, 0.10))`);
  - `P[1]` x: 0.22 -> **0.24** (keep y 0.17, z 0.24);
  - keep the base width at 0.092 and the other points as they are.
  This puts the root's inner face at about |x| 0.12, clear of the points at x +/-0.10.
- Target: all five points visible in `crown_front`. Re-check the gold px at 64 px on the game camera (the lead's gate is
  25); the move may trim a few gold px, so re-measure.

### M2 - The back must read darker than the flanks in `model_game`
- Cause: the top band is DEEP_STEEL (38,64,130) on the saddle shells (`sh_rib`, `sh_waist`, `sh_hips`, L200-202) and the neck
  saddle (L231). The body beneath is STEEL_BLUE (62,104,176), and the gap between them is about 10-15 luminance points.
- Fix: darken the dark accent only. `DEEP_STEEL` (38,64,130) -> **(30,50,110)** (L24). Keep `STEEL_BLUE` (62,104,176) for the
  flanks. The brightest channel of the dark accent falls below 170, which is allowed for an accent band, not the body.
  Legs and wing arms also darken, which is accepted (see R2).
- Target: back-to-flank luminance gap of **20 or more** in `model_game` (sample the spine between the fins against the flank),
  and portrait mean luminance **<= 110** on my count (the builder's count should also land at or below 110).

## NICE
- **N1** Membranes (100,130,196) are the largest blue mass in the game view. (90,118,184) would let the body and the fins lead.
  Optional.
- **N2** The horn roots show as flat gold blocks at the skull sides in `model_game` (lower left of the game view). The M1 move
  should soften this. If not, taper the root.
- **N3** The chest core setting's dark rim reads slightly bolt-like in `core_front`. Leave it.

## Pass / fail checklist
| # | Item | Result | Note |
|---|---|---|---|
| 1 | Species reads at 64 px | PASS | Dragon, gold crown and white fin row read together |
| 2 | Crown reads as a crown from the side and tq | PASS | Five points in tq |
| 3 | Crown reads from the front (five points) | FAIL | Three points visible; outer pair hidden (M1) |
| 4 | Crown reads from behind (game camera) | PASS | Gold back ring with spikes |
| 5 | Fins read (7) in silhouette | PASS | Side, back, game |
| 6 | Frost core = chest focal point, no grille | PASS | Hex core only (M2 of round 2 done) |
| 7 | Gold hero >= 25 px at 64 px (game camera) | PASS | 27 (lead ruling); 41 on the portrait strip |
| 8 | Gold hero >= 40 px at 64 px (round 2 target) | WAIVED | Lead ruling |
| 9 | Gold share ahead of both secrets | PASS | 2.8 % vs 0.6 % / 1.2 % |
| 10 | Ice-white >= 9 % | MARGINAL | 8.4 % on both counts |
| 11 | Dark share >= 28 % | FAIL | 24 % / 22 % (M2) |
| 12 | Mean luminance <= 110 | FAIL | 111 / 114 (M2) |
| 13 | Dark top separate from flanks in `model_game` | FAIL | About 10-15 points; target 20 (M2) |
| 14 | Outclasses Thunder Rex overall | PARTIAL | Ahead on gold, crown and crystal; level on value |
| 15 | Outclasses Cosmic Leviathan overall | PARTIAL | Ahead on gold and ice; Leviathan's magenta is more striking on the portrait |
| 16 | Stud skin on hide, smooth detail | PASS | Studs on body and legs; fins, horns, core, claws smooth |
| 17 | Tris within gate (13k) | PASS | 8,440 builder-reported (not re-measured here) |
| 18 | No glow / no Neon | PASS | |
| 19 | Name is two words | PASS | Frostcrown Dragon |
| 20 | `collision_free` at fold | PASS (builder) | ground_min_z -0.005, builder-reported |

## Next round (short check, not a full review)
Send: `crown_front.png` (must show five points), `model_game.png` (back vs flank), the 64 and 128 px strips with Rex and
Leviathan on the same camera, and the step-1 tri count. If M1 and M2 pass, the model ships at 8/10.

Verdict: **APPROVED WITH FIXES, 8/10.** Do M1 and M2 (both are one-line numeric changes), re-render, and send the short check.
