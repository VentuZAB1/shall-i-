# Frostcrown Dragon - scores review 5 (2026-10-28) - REVISE

**Model: 8.0 / 10. Clips: 8.0 / 10.** Both are below the new 8.5 minimum, so the verdict is REVISE for both. The build is
clean and the act now has a real peak, which was the main round-4 gap. What keeps it from 8.5 is the outclass read: the
front horns still read as gold blocks, the in-game gold is marginal, and the body has less spectacle detail than Rex. The
clip gate is close: physics and reference rules now pass, and one unverified handoff could still pop.

## Model - 8.0 / 10
### What is strong (verified)
- **Gold hero at 64 px, portrait:** 44 px (my strict count), against Rex 4 and Leviathan 11. The gold read is clearly ahead.
- **Ice-white:** 9.4 % on my 128 px count, 8.1 % on the builder's. The two counts differ by 1.3 points, so the 9 % target is
  borderline on the builder's count (see MUST 3).
- **Luminance:** 107 (128 px) / 100 (64 px) mine; 105 / 105 / 109 builder. Under 110.
- **Dark share:** 29 % (my 128 px count), the most of the three. Target 28 %, met on my count.
- **Five crown points** read from the front (`crown_front.png`). The back-view crown ring with spikes reads from the game camera
  (`crown_game.png`). The back-to-flank gap in `model_game` is clear.
- **Crystal fins (7), frost core, white tail crystal:** all read at icon size.
- **Tris 8,440** (builder), gate 13k. Step-1 collision-free.

### What holds it below 8.5
1. **Front horns read as gold blocks, not horns (the coordinator's question: yes, they do).** In `crown_front.png` the two
   upper horn segments are wide flat slabs with square faces. `horn()` builds each segment with `side=(1, 0, 0)`
   (L150, L153), so its flat width runs along x, the front view's horizontal. Each horn shows its full ~0.18 BU width from
   the front. This is the "toy slab" look the owner rejected before. The root taper (review 4 N3) helps the root only.
2. **In-game gold is marginal.** My strict count on the 64 px game icon (`FrostcrownDragon_icon_game.png`) is **13**, and
   **26-27** on a looser gold rule. The builder reports 28. The gate is 25, so it passes only on the looser rule. The
   shaded horn sides fall below the strict red threshold after lighting. The back band is 0.15 wide and 0.022 tall, so
   little gold faces the game camera.
3. **Outclass detail vs Rex.** Rex has a dense spine row, cyan trim bands on every armour segment and seams. Frostcrown's
   body is a plain studded blue from the side and the back, with only the fins and the tail breaking it. At 64 px the
   silhouette wins, but close up Rex has more spectacle.
4. **Ice-white margin.** 9.4 % (mine) vs 8.1 % (builder). If the builder's count is right, it misses 9 %.

## Clips - 8.0 / 10
### What is strong (verified)
- **Physics and limits:** step-1 collision-free, all loops closed, linear 0, walk slide 0. `ground_min_z` -0.005 to -0.008
  (fly +0.098). Neck max 7.0 (margin 1 deg), chest vs spine 3.0, head + neck pitch-up 15, largest step **24.6 deg** (was 42.4).
- **End-of-clip rest:** the end frames are in the sheets. Roar f66, act f110 and land f28 match the rest pose visually and
  the builder's delta is 0.00 deg. This closes review 4 MUST 3.
- **Act peak:** the wings flare to SPREAD at f44 and hold through the frost burst at f50 (`_pose_tq_act_stillfreeze_sheet.png`,
  f44 / f50 / f58). The fins rise to 30 and the head presses low at the same time. This closes review 4 MUST 2. The act
  reads as a single moment.
- **Readable beats:** takeoff (crouch f0-10, wings up, the f12-14 downstroke, airborne f19-22), land (glide, flare f7-12,
  touch f16), roar (head lifts, jaw lags and opens, hold, close) all read.
- **ANIM_REFS:** every primary reference is now from a site tag: #236985 (Earthsea dragons: takeoff, flare), #260630 (heron:
  land, head press), #174482 (Maid Dragon S: fly body), #256671 (walk-cycle, lateral sequence), plus #174333, banshee #8 and
  Sea Beasts #3. Method and frames are written out. The lead's rule is met.

### What holds it below 8.5
1. **Takeoff-to-fly handoff is unverified.** The takeoff ends in the flight cycle (fly phase 0.2) and the fly clip sits at
   +0.098 above the ground. In the f27-28 frames the feet look low, close to the rest height. If the takeoff's last foot
   height is not +0.098, the switch into fly will pop. The notes do not report it.
2. **The act has no finish beat.** After the mist at f50 the wings hold, then settle at f70-80. The climax is good, but
   nothing closes the moment, and the frost burst itself is VFX (not in the clip).
3. **Dragon-specific flight reference is thin.** The dragon flight references are the Earthsea dragon (takeoff, flare) and
   a black western dragon (fly body). The HTTYD dragon-rider clip the lead named was not read (the site froze). That is
   acceptable under the rule, but it is the weakest link for a mythic flyer.
4. **Fin tick is small.** The idle fins tick 2 deg together. At gameplay distance that is not readable.

## MUST - to reach 8.5 (in priority order)

### Model
- **M1 Horn blocks (fix the slab read).** In `horn()` (L150 and L153) change `side=(1, 0, 0)` to a diagonal, e.g.
  `side=(0.707, 0, 0.707)`, so the front-view x-width drops by about 30 % while the side view keeps the horn's depth. Keep
  the root taper and the tip points. Check the kit's `side` semantics on one segment first. Target: `crown_front.png` shows
  two horns that read as curved horns, not flat blocks, and the five points stay visible.
- **M2 In-game gold (raise the strict count to 25+).**
  - back points (L288): `GOLD_D` -> `GOLD`, so they keep the house gold after lighting;
  - back band (L285): (0.15, 0.022, 0.05) -> **(0.20, 0.035, 0.05)**, so more gold faces the game camera;
  - add one brighter upper ridge on each horn (`GOLD_D` band at L156) only if M1 still leaves the strict count under 25.
  Target: strict gold px at 64 px on `FrostcrownDragon_icon_game.png` **>= 25** (state the resize filter and the threshold
  with the number, so the count can be reproduced).
- **M3 Ice-white over 9 % on both counts.** Add one ICE_THROAT facet bar along each neck-top fin base (or two more facets on
  the fins) so both counts reach 9 %. Report both counts.
- **M4 Crystal seams for the outclass read (Rex has trim bands; we use ice, not cyan).** Add 2 ICE_THROAT trim bands on each
  torso block and 2 on the tail (flush bars, 0.018 wide, on the flank). This gives the flanks the banding Rex gets from its
  cyan trims, in our own colour. Keep the studs on the hide. Target: the side and the tq views show banded flanks at 300 px.

### Clips
- **C1 Verify the takeoff-to-fly handoff.** Report the takeoff's lowest foot z at f27 and f28, and the fly clip's start
  height (+0.098). If the difference is more than 0.02, blend the last 4 takeoff frames to the fly base height. No pop.

## TO 9+ (after the 8.5 items)
- **Model:** a lighter gold edge on the horns' upper faces so the crown catches light in the game view; a faint ICE_W
  frost edge on the wing arm (catches light at distance); a second small facet on each fin for tq readability.
- **Act:** a finish beat at f58-66, two small wing snaps (3-4 deg) as the frost lands, so the act ends with a flourish, not
  a settle.
- **Idle:** fin tick 2 -> 3 deg, so it reads at gameplay distance.
- **Refs:** read one dragon-rider clip (HTTYD, from the site's `how-to-train-your-dragon` tag) for the takeoff downbeat and
  the act's wing flare, and cite its frames. It is the best dragon-specific reference we have not used.
- **Takeoff:** a slightly stronger downbeat (the wings sweep through a wider arc at f12-14) so the launch reads from the
  game camera.

## Pass / fail checklist
| # | Item | Result | Note |
|---|---|---|---|
| 1 | Five crown points from the front | PASS | |
| 2 | Horns read as horns, not slabs | FAIL | Flat x-width (M1) |
| 3 | Back crown ring from the game camera | PASS | |
| 4 | Dark top separate from flanks | PASS | |
| 5 | Luminance <= 110 | PASS | 107 mine; 105 builder |
| 6 | Dark share >= 28 % | PASS (mine) | 29 %; builder 24 % |
| 7 | Ice-white >= 9 % on both counts | MARGINAL | 9.4 mine / 8.1 builder (M3) |
| 8 | Gold hero, portrait 64 px >= 25 | PASS | 44 |
| 9 | Gold hero, game 64 px >= 25 (strict) | FAIL on strict | 13 strict / 26-27 loose (M2) |
| 10 | Gold hero clearly ahead of Rex and Leviathan | PASS | 44 vs 4 / 11 |
| 11 | Outclass detail vs Rex (banding / seams) | FAIL | Plain body (M4) |
| 12 | Tris <= 13k | PASS | 8,440 builder |
| 13 | Step-1 collision-free, loops, linear 0 | PASS | |
| 14 | Ground >= -0.02 | PASS | -0.008 worst |
| 15 | Neck <= 8 | PASS | 7.0 |
| 16 | Chest vs spine <= 5 | PASS | 3.0 |
| 17 | Head + neck pitch-up <= 30 | PASS | 15 |
| 18 | Largest step < 60 | PASS | 24.6 |
| 19 | End frames at rest (roar, act, land) | PASS | Visual + builder 0.00 deg |
| 20 | Takeoff-to-fly handoff | NOT VERIFIED | (C1) |
| 21 | Act peak reads | PASS | f44-58 |
| 22 | Act finish beat | FAIL | TO 9+ |
| 23 | ANIM_REFS: site tags for every primary clip | PASS | Frames and method cited |
| 24 | Events match the clip table | PASS | Fraction-stored times reconcile |
| 25 | Name, no glow, studs | PASS | |

## Next round (short)
Send: the horn front crown at 600 px after M1; the 64 px game icon with the strict gold count and the resize filter (M2);
both ice-white counts (M3); a side and tq view showing the flank banding (M4); the takeoff's last foot z and the fly start
height (C1).

Verdict: **REVISE. Model 8.0, clips 8.0.** Do M1-M4 and C1 to reach 8.5; the TO 9+ list is the path past it.
