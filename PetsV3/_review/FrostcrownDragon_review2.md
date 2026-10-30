# Frostcrown Dragon - model gate review 2 (2026-10-27) - REVISE

**Score: 7/10 for a 0.1 % mythic (ship at 8+).** Round 1 was 6/10. The fins, the frost core, the tail tip and the gold
are all clearly better, and the builder fixed each one as written. But the rarest pet does NOT yet clearly outclass Thunder
Rex or Cosmic Leviathan. It wins on gold and ice. It is level with both on value. From the front the crown still reads as
a V of horns with its five-point band hidden. Three short MUST items finish it. The fins, the core and the tail do not need
another review round.

## Judgement: does it clearly outclass Thunder Rex and Cosmic Leviathan?
| Test (128 px icon, 64 px gold) | Frostcrown | Thunder Rex | Cosmic Leviathan | Verdict |
|---|---|---|---|---|
| Gold share (builder 128 px) | **4.0 %** | 1.0 % | 2.3 % | clearly ahead |
| Gold px at 64 px (strict) | **23** (builder, game camera) / 33 (my count, 64 strip cell 1) | ~4 (my count, 64 strip cell 2) | ~11 (my count, 64 strip cell 3) | ahead, but near the gate of 25 |
| Ice-white share (builder) | **8.9 %** | 3.7 % | 4.2 % | ahead |
| Ice-white share (my count, portrait) | **8.8 %** | 5.3 % | 4.3 % | ahead |
| Fins / crystal row readable at 64 px | 7 white blades, read from side, back and game camera | dense cyan spine row | pink / blue fins | ahead on the fin row, not on density |
| Mean luminance (builder) | 118 | 107 | 116 | **not ahead**: Frost is the lightest of the three |
| Mean luminance (my count, portrait) | 114 | 118 | 108 | **not clear**: my numbers reverse the ranking |
| Dark share (builder) | 22 % | 18 % | 12 % | ahead of both, below the 30 % target |
| Dark share (my count, portrait) | 24 % | 11 % | 22 % | ahead of Rex, level with Leviathan |
| Crown read from the front | V of horns, five-point band hidden | gold crown + cyan gems | gold spiked crown | **not ahead** |

The two measurements disagree on the Rex / Leviathan value ranking. They are different crops, so I do not treat the value
gap as proven either way. The conclusion that holds under both methods: **the Frostcrown is not clearly darker or richer
than the 1 % secrets.** The rare-tier rule asks for a clear win, and value is the one place it is still level.

## What the builder changed (round 1 MUST status)
- **MUST 1 seven fins: DONE, reads.** Seven ICE_W blades stand on the neck, the withers and the back, and the tail base. They
  show from the side and the back and in the game-camera model. `FIN_PARENTS` and the assert close the rig gap I flagged.
- **MUST 2 frost core: DONE, mostly.** The ICE_W hex crystal sits recessed in a DARK setting. It is the clean chest focal point
  the round asked for (`core_front`). **Remaining:** the chest front still reads as two pale plates with DARK bars (see M2).
- **MUST 3 crown: PARTIAL.** Side and tq read as a proper gold crown: a swept gold horn with a band and a point. **From the
  front it fails:** the horns rise as a yellow V, and only the centre point of the five-point band shows. Measured gold at 64
  px is 23 on the game camera (target 40, gate 25). See M1.
- **MUST 4 colours: APPLIED, value not yet at target.** Builder 118 vs target 115; my count 114. R1 (the wider dark band) did
  not separate the dark top from the flanks in the game views (`model_game`). See M3.
- **MUST 5 tail tip: DONE.** The 0.44 BU white crystal reads at the back of the game view.
- **NICE N1-N4: DONE.** Skull, upper arm, and the kept face read as fierce (slit eyes, brows, fangs).
- **R1 deviation: ACCEPT the dark-limb and membrane changes**, which help the silhouette. The membrane darkening (100,130,196)
  reads well. The wider neck saddle and the dark socks are fine. Lower saddle shells were reverted; that is fine.

## MUST (round 3, in priority order)

### M1 - Crown from the front (the gold hero, and the gold px at 64 px)
- Problem: in `crown_front` and `close_front` the horn roots (L272-275; `P[0]` = (s*0.09, -0.06, 0.12), base width 0.080) sit
  at the same depth as the diadem band (y -0.152), so they cover the band's outer points. Only the centre point shows. The
  horns rise from `P[1]` (z 0.27) to `P[2]` (z 0.36) with a wide V, which reads as ears.
- Fix:
  - move the horn roots BACK so they rise from behind the band: `P[0]` y -0.06 -> **+0.04**, `P[1]` y 0.11 -> **0.16**;
  - lean the horns back, not up: `P[2]` z 0.36 -> **0.30** (keep `P[3]` at (s*0.31, 0.74, 0.40));
  - widen the diadem band (L278): (0.15, 0.030, 0.040) -> **(0.20, 0.040, 0.050)**, so its ends stand out past the horn roots;
  - five points (L285-289, now 0.06 / 0.09 / 0.13 / 0.09 / 0.06): inner pair x ±0.05 h **0.10**, outer pair x ±0.10 h **0.07**,
    centre x 0 h **0.15**.
- Target: all five points visible in `crown_front`; gold px at 64 px game camera **>= 40** (builder count); the front
  silhouette reads as a crown with horns, not ears.

### M2 - The chest front must not read as a grille
- Problem: `close_front` shows pale plates on the chest front with DARK bars across them. The bars come from the belly rungs
  (the `for t, w in ((0.40, 0.10), (0.80, 0.09))` loop, L206-209). The neck-throat scute bars were already removed in round 2.
  From the front the chest reads as a ladder. The hex core is the one feature that should stand there.
- Fix: remove the belly rung loop (L206-209) so the belly strip (L204-205) stays a plain ICE_BELLY plate. Keep the hex core
  (L210-224) as the only chest feature.
- Target: no DARK bars on the chest front in `close_front`.

### M3 - Value: a clear dark body, not a mid-blue sheet
- Problem: the portrait is level with the secrets (builder 118, my 114). In `model_game` and `model_side` the back and flanks
  read as one mid-blue; the DEEP_STEEL top band does not show between the fins.
- Fix: `STEEL_BLUE` (70,118,190) -> **(62,104,176)** (brightest channel 176 keeps the >= 170 rule). Keep `DEEP_STEEL`
  (38,64,130) and `MEMBRANE` (100,130,196). Keep the fins ICE_W.
- Target: mean luminance of pet px in the 128 portrait **<= 110** (both methods), dark share **>= 28 %**. Below 110 the
  Frostcrown is as dark as Leviathan on my count and darker than Rex on the builder's.

## NICE
- **N1** If M3 is not enough, lift the DEEP_STEEL saddle shell pad 0.022 -> 0.030 so the top band shows past the fins.
- **N2** Check the Fin_6 / Fin_7 bases against the tail after M1 (the back of the tail is in the game view).
- **N3** The chest core setting: its dark rim is slightly "bolt-like" in `core_front`. Leave it, unless M2 changes the
  chest read.
- **N4** Keep the placeholder idle (ground fold). The clip gate is next.

## Pass / fail checklist
| # | Item | Result | Note |
|---|---|---|---|
| 1 | Species reads at 64 px | PASS | Winged 4-legged dragon, gold head read, white fin row |
| 2 | Fins read in silhouette (7) | PASS | Side, back and game view |
| 3 | Frost core = focal point | PASS | Recessed ICE_W hex crystal |
| 4 | No grille on the chest | FAIL | Two pale plates with DARK bars (M2) |
| 5 | Crown reads as a crown from the front | FAIL | V of horns, five-point band hidden (M1) |
| 6 | Crown reads from the side / game view | PASS | Swept gold horn + band + point |
| 7 | Gold hero >= 25 px at 64 px | MARGINAL | 23 px builder count, game camera |
| 8 | Gold hero >= 40 px at 64 px (round-1 target) | FAIL | 23 px (M1 fixes it) |
| 9 | Gold share >= 2.5 % | PASS | 4.0 % |
| 10 | Value <= 115 (portrait) | MARGINAL | 118 builder / 114 mine (M3 target 110) |
| 11 | Dark share >= 30 % | FAIL | 22 % builder / 24 % mine (M3 target 28) |
| 12 | Ice-white >= 9 % | MARGINAL | 8.9 % builder / 8.8 % mine |
| 13 | Clearly outclasses Thunder Rex | PARTIAL | Ahead on gold and fins; level on value; not ahead on the crown front |
| 14 | Clearly outclasses Cosmic Leviathan | PARTIAL | Ahead on gold and ice; Leviathan is darker and more saturated on my count |
| 15 | 3-band colour blocking reads | PARTIAL | DEEP_STEEL top band not visible in the game views (M3) |
| 16 | Stud skin on hide, smooth detail | PASS | Studs on body, neck, legs; fins, horns, core, claws smooth |
| 17 | Tris within gate (13k) | PASS | 8,236 builder-reported (not re-measured here) |
| 18 | No glow / no Neon | PASS | |
| 19 | Name is two words | PASS | Frostcrown Dragon |
| 20 | collision_free at fold | PASS (builder) | ground_min_z -0.005, reported by the builder; clip gate re-checks |

## Next round
Send only: `crown_front` and `close_front` (after M1, M2), `flat_game` with the value share, the 64 and 128 px strips
(portrait and game camera) next to Thunder Rex and Cosmic Leviathan on the same camera, and the step-1 tri count. If those
pass, this is the mythic, and I expect 8/10 at that point.

Verdict: **REVISE, 7/10.** Do M1-M3 and send the next round. Fins, core, tail and gold are the hero read; do not touch them.
