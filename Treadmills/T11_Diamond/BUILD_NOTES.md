# T11 `Tier11_x20` (x20, 1M/s): DIAMOND RAINBOW. BUILD NOTES (Phase B)

- Built in `game.ServerStorage.Assets.Treadmills.Tier11_x20` and refreshed with `T.refresh(11)` after each step.
- Changed nothing else: no Play, no scripts, no other tiers or bays.
- `Theme = "Diamond Rainbow"`. Tier / TierName / SpeedPerSecond / LabelHeight unchanged.

## Final validator (`T.validate(11)`)
```
== Tier11 Diamond Rainbow: 0 FAIL, 0 WARN
ok   label screen = Part 6.1x3.1 colour (30,26,64) lum 0.12, 3 tilted parts
ok   106 visible parts (80 decor), 13 accent-material parts, 3 lights; animation hooks: wing_L x2, wing_root_L x1,
     sparkle_ x12, screen_gem x1, chevron_ x6, hood_emblem x1, wing_root_R x1, wing_R x2, screen_bar_ x7, rune_ x7, halo x1
```
- Rule R1 (exit walkway |x| ≤ 4.1, z ≥ 7, y 0.3–6.6): empty. No spoiler. The rails sit at |x| ≥ 4.79 and the pylons
  at |x| ≥ 5.2.
- **Parts:** 106 visible, 39 animated (counted on the refreshed bay):
  - 7 runes, 1 halo, 4 wing parts, 12 sparkles, 7 EQ bars, screen_gem, hood_emblem, 6 chevrons.
- **Accent:** 13 Glass parts (the halo + 12 sparkles), under the limit floor(106 × 0.15) = 15.
- **Ladder:**

| Measure | Value |
|---|---|
| Solid top | **14.55** (crown points) |
| Static peak | **15.75** (halo) |
| Animated max | **15.93** (halo at the top of its float); wings ≤ 15.58 at full flap; crown sparkles 15.28 at 110 % |

## What was built (all decor Anchored, CanCollide / CanTouch / CanQuery false)
### Chassis recolour (size, position and collision unchanged)
- **Belt strips:** red → violet from −x to +x, Inlet (red on the runner's left).
- **White, Studs:** side frames, console bars, handles, handle caps.
- **Obsidian (26, 24, 40):**
  - base plate, bracket, **screen frame**: Studs
  - console and centre posts, front feet: Weld
  - grips: Inlet
- **Screen face:** midnight (30, 26, 64), Universal.

### Grand rainbow arch (z_a = −10.135)
- Centre (0, 5.7), R = 6.55, thickness 1.2.
- **Base pieces:**
  - `ArchPlinth_L/R`: O Weld, y −0.6 to 0.2.
  - `ArchLeg_L/R`: W Studs, y 0.2 to 5.1.
  - `ArchCapital_L/R`: O Studs, **1.6 wide**, y 5.1 to 5.83.
- **`ArchStone_1..7`:** STATIC rainbow voussoirs, Studs, alternating depths 1.1 / 1.3, red on the left.
- **`rune_1..7`:** white Universal diamond inlays.
  - Size 0.7 × 0.7 × (stone depth + 0.2), turned 45° in the stone plane, proud 0.1 on both faces.
  - Numbered red → violet, so the chase sweeps left → right as the runner sees it. Order checked on the refreshed
    bay: x = −6.39 … +6.39.
- **Seating:** the end stones' outer bottom corners sit at (±7.303, 5.834), flush with the capital top. Their inner
  corners sink 0.27 into the opaque capitals. No stone corner sticks out past a capital (capitals reach x 7.35).
- **`sparkle_leg_L/R`:** 0.5 Glass gems, 45° about Z, centred on the leg front faces at y 2.6.
- **Lights:** `CapitalLight` PointLights, warm (255, 150, 170) left and cool (185, 160, 255) right, Brightness 1.0,
  Range 9, Shadows off.

### Crown, diamond and wings
| Part | Spec |
|---|---|
| `CrownBand` | O, 3.2 × 0.8 × 1.7, y 12.85–13.65 |
| `CrownPoint_1..4` | W Weld 0.5 × 0.9 × 0.5 at (±1.3, z_a ± 0.6) |
| `sparkle_crown_1..4` | 0.4 Glass cubes on their vertex, y 14.55–15.24 |
| `halo` | 1.1 Glass cube on its vertex (rx = 35.3°), y 13.85–15.75, holds `DiamondLight` (255, 250, 240), Brightness 2, Range 12 |
| `wing_root_L/R` | W, 0.4 × 0.8 × 0.8, flush with the band ends |
| `wing_L/R` (main feather) | W Weld WedgePart, 3.0 span × 1.3, flat leading edge, swept up 10° (rx = 10°, so it doesn't count as screen-tilted) |
| `wing_L/R` (second feather) | crystal WedgePart, 2.2 × 0.9, swept −5°, 0.25 behind toward the runner side. It shows below the main feather |

### Tall console (equalizer)
| Part | Spec |
|---|---|
| `ConsoleTower_L/R` | crystal, 0.6 × 4.345 × 1.0 at x ±3.6, y 4.505–8.85, standing on the upper console bar |
| `MarqueeBody` | W, 7.8 × 1.3 × 1.0, **y 8.85–10.15** |
| `MarqueeDisplay` | O, on the runner face |
| `screen_bar_1..7` | rainbow, 0.55 × 0.8, y 9.1–9.9, z −7.9 |
| `screen_gem` | blue diamond on the plaza face, y 9.5 |

### Rails
- `RailPost_L/R1..3`: crystal, z −4.0 / 1.6 / 7.2, y 0.875–2.1.
- `RailBar_L/R`: W, y 2.1–2.6, z −4.4 to 7.95, butting into the pylons.
- Sparkles: `sparkle_rail_L/R` at the front (z −4.0) and `sparkle_rail_L2/R2` over the middle posts (z 1.6), all on
  the bar top.

### Rear pylons (no spoiler)
| Part | Spec |
|---|---|
| `PylonBody_L/R` | W, 1.0 × 6.0 × 1.2 at x ±5.75, z 7.95–9.15, y −0.6 to 5.4 |
| `PylonBand_L/R` | collars, red left / violet right, Inlet, y 3.0–3.8 |
| `PylonShaft_L/R` | crystal, 0.8 × 3.6 × 0.8, y 5.4–9.0 |
| `PylonCap_L/R` | W Weld, 1.0 × 0.4 × 1.0, y 9.0–9.4 |
| `sparkle_pylon_L/R` | 0.7 Glass cube on its vertex, centred at 9.4, top 10.0 |

### Badge and belt
- `HoodSetting` (O) and `hood_emblem` (violet): a diamond on the console front.
- `chevron_1..6`: white diamond tiles (0.8 × 0.12 × 0.8, 45° about Y) on the orange and indigo strips, at
  z −2.6 / −0.2 / 2.2.

### Palette as built
| Role | RGB / setting |
|---|---|
| W | (248, 248, 250): the reviewer's neutral white, not Frost's snow |
| C | (220, 236, 255), Transparency 0.25, Weld |
| O | (26, 24, 40) |
| Glass gems | (240, 248, 255), Transparency 0.1–0.15, Reflectance 0.2 |
| R | 255,58,58 |
| O | 255,140,26 |
| Y | 255,214,32 |
| G | 46,204,96 |
| B | 30,144,255 |
| I | 88,86,232 |
| V | 178,76,240 |

## Review changes applied (`PLAN_REVIEW.md`, x20)
1. **Arch chase on inlays:** the stones are static `ArchStone_1..7`; `rune_1..7` are white inlays. The rainbow keeps
   full colour while running.
2. **`RearSpoiler` deleted.** The walkway is empty (R1).
3. **Taller pylons:** crystal shafts to 9.0, white caps, gems topping out at 10.0, 1.0 wide, at |x| ≤ 6.3.
4. **Crown clearance:** points and sparkles at (±1.3, z_a ± 0.6) and the band widened to 3.2 × 1.7. Computed
   horizontal clearance to the spinning halo (radius 0.898):
   - crown points: 0.209
   - crown sparkles at 110 %: 0.174
5. **Marquee at y 8.85–10.15.** The EQ bars and the gem moved up with it. The towers grew to 8.85.
6. **Richness:**
   - a second crystal feather per wing, also named `wing_L` / `wing_R`;
   - `sparkle_rail_L2/R2`;
   - `sparkle_leg_L/R`.
   - Result: 106 parts and 39 animated.
7. **Arch seating:** capitals widened to 1.6 and raised to 5.83, so the stones sit flush. Checked in `close`.
- **Recommended items also done:** W is the neutral (248, 248, 250), and the wing sweeps are 10° / −5°, so the tilted
  count stays 3.

## R2: every hook checked at its extreme (computed in Studio)
| Hook | Extreme |
|---|---|
| Wings at ±0.28 rad | main: x 1.72–5.25, y 12.86–15.58; second: x 1.82–4.20, y 12.88–14.26 |
| Wings vs the arch | at the full down-flap, the lowest point (root bottom, x ≈ 2.1, y 12.86) is ≈ 0.33 above the arch's outer surface |
| Halo with float ±0.18 | y 13.67–15.93: clears the band (13.65) and stays under 16. Spinning never changes rx |
| Sparkles at 110 % | crown y ≤ 15.28; pylon x 5.14–6.36 (outside the corridor, and under 6.4 for the sign keep-out); rail sparkles y ≤ 3.33 (under the corridor) |
| Chevrons | wrap at y 0.26–0.38, below the Zone (0.6) |

Nothing crosses y 16 or |x| 7.4, or enters the Zone, the head box, the corridor or the walkway.

## Deviation from the approved plan (small improvement)
- **Screen frame (chassis) is Obsidian, not white.**
  - In `hub34_v1`, `eye_v1` and `close_v1` the screen back, marquee and console merged into one flat white mass.
  - With a dark screen back, the front reads in clear bands: white console, violet badge, dark screen, white marquee
    with the blue gem, rainbow arch.
  - In `runner_v3` the label still reads crisply. The white towers and marquee frame the dark screen.

## Captures (all taken one at a time under `T.lock("T11")`)
### v1 (before the frame change)
`T11_hub34_v1`, `T11_spawn_v1`, `T11_runner_v1`, `T11_lineup_v1`, `T11_sideHi_v1`, `T11_side_v1`,
`T11_rear34_v1`, `T11_close_v1`, `T11_eye_v1`

### v2/v3 (final)
`T11_eye_v2`, `T11_runner_v3`, `T11_hub34_v2`, `T11_lineup_v2`, `T11_spawn_v2`, `T11_close_v2`, `T11_side_v2`,
`T11_sideHi_v2`, `T11_rear34_v2`

### Notes on the captures
- **`T11_runner_v2`:** taken right after a refresh, before the mock label rendered (blank face). `runner_v3` is the
  same view with the label.
- **Camera FOV:** the lab camera FOV was about 50° in the v1 shots and 70° in the later ones (someone else changed
  it), so v1 and v2 framings differ.
- **What the captures show:**
  - `runner_v3`: the arch frames the view. The whole winged crown and diamond are visible above it at FOV 70, the
    "+1M / sec" label is crisp on the midnight face, and the rainbow road is underfoot.
  - `lineup_v2` / `spawn_v2`: x20 is clearly the tallest and most distinct next to x18.
  - `rear34`: the crystal pylons rise above x18's fins.
  - `side`: the pylon shaft, cap and gem read well.

## Things I'm unsure about (for the visual reviewer)
- **Sky sliver:** from the plaza there is a thin strip of sky between the screen's top edge (8.38) and the marquee
  (8.85, set by the review). It reads as a separation line. I left it rather than add a tilted filler.
- **Arch joints:** small inner V-notches between the stones are visible up close. That is the brick-arch look, and
  the alternating depths prevent z-fighting.
- **`side` / `sideHi` presets:** they sit only 11–12.5 studs from the belt centre. The arch and crown are mostly out of
  frame there; `spawn`, `hub34` and `lineup` show the full silhouette.

---

# Phase C: fixes from REVIEW.md (verdict FIX). All items 1-9 done; the obsidian screen frame is kept (item 10)

## Final validator (`T.refresh(11)` + `T.validate(11)`)
```
== Tier11 Diamond Rainbow: 0 FAIL, 0 WARN
ok   label screen = Part 6.1x3.1 colour (30,26,64) lum 0.12, 3 tilted parts
ok   109 visible parts (83 decor), 13 accent-material parts, 3 lights; animation hooks: wing_L x2, wing_root_L x1,
     sparkle_ x12, wing_R x2, chevron_ x8, hood_emblem x1, wing_root_R x1, screen_gem x1, screen_bar_ x7, rune_ x7, halo x1
```
- **Visible parts:** 109 (≤ 110; x18 has 106).
- **Animated parts:** 41 (x18 has 40):
  - 7 runes, 1 halo, 4 wing parts, 12 sparkles, 7 EQ bars, `screen_gem`, `hood_emblem`, 8 chevrons.
- **Glass:** 13 parts, under the limit floor(109 × 0.15) = 16.
- **Heights:**

| Measure | Value |
|---|---|
| Opaque top at rest | **15.00** (taller crown points); wing tips 14.80 |
| Static peak | **15.77** (diamond) |
| Animated max | **15.95** (diamond at the top of its float); wing tips **15.90** (up-flap); crown sparkles 15.57 at 110 % |

## Item by item
1. **MUST, motion:** added `chevron_7` and `chevron_8`, white diamond tiles on the GREEN centre strip at (0, 0.32, −1.4)
   and (0, 0.32, +1.0). Same tile as the others. Animated count 39 → **41**.
2. **MUST, king silhouette:**
   - **Main feathers:** now 4.1 span × 1.6 × 0.35, W Weld.
     - The flat leading edge sweeps 3.5°, so rx = 3.5° and they aren't counted as screen-tilted.
     - The root edge is flush on the hinge's outer face: x ∓2.05 from y 12.95 to 14.55 (it leans in 0.1 at the top).
     - The tip at rest is (∓6.04, 14.80).
   - **Hinges:** `wing_root_L/R` moved to x ∓1.85 (x 1.65-2.05), to sit on the ends of the widened 3.3 band.
   - **Under-feathers:** 2.9 × 1.1 × 0.25 crystal.
     - Flat bottom at y 12.95. The sloping top runs from the root (y 14.05) down to the tip (∓4.95, 12.95).
     - They sit 0.31 behind the main feather (a 0.01 gap), so from the plaza they show as a second feather under the main
       one.
   - **The optional step was needed:** the first far view (`T11_C_front55_b10b11`) still put x20's opaque top level with
     x18's flames. So `CrownPoint_1..4` are now **1.35** tall (y 13.65-15.0) and the crown sparkles are centred at 15.19.
   - In `T11_C_front55_b10b11_v2` the crown points, the 12-wide white wings and the diamond now clearly top x18.
3. **MUST, gap:** `MarqueeSkirt`, O Studs, 6.48 × 0.32 × 0.22 at (0, 8.69, −9.18), axis-aligned.
   - It sits exactly on the frame's top edge, measured at (y 8.527, z −9.292), and butts the marquee's bottom.
   - In `T11_C_close` the dark screen now runs straight up to the white marquee.
   - The `screen_gem` bottom (8.93) clears it.
4. **MUST, floating gems:** the sparkles were lowered so they still touch their support at 55 %.

| Sparkles | Centre | Bottom at 55 % | Top at 110 % |
|---|---|---|---|
| `sparkle_crown_1..4` (taller points) | 15.19 | 15.00 | 15.57 |
| `sparkle_rail_L/R/L2/R2` | 2.79 | 2.60 | 3.17 |

5. **Diamond:** `halo` is a 1.05 cube centred at y 14.86. It spans 13.95-15.77 at rest and 13.77-15.95 while floating,
   so it stays 0.12 above the band. Horizontal radius 0.857. `DiamondLight` is still inside.
6. **Rim notches:**
   - `ArchStone_1..7` are now 3.26 long, so the outer rim is closed.
   - The end stones' outer-bottom corners sit at (±7.333, 5.702), inside the capitals (x ≤ 7.35, top 5.83). The inner
     corners are at (±6.164, 5.435), also inside.
   - The keystone spans ±1.63, so `CrownBand` was widened to **3.3** × 0.8 × 1.7.
7. **Feather hinges:** done as part of item 2. The root edge now touches the hinge face from 12.95 to 13.65.
8. **Arch slit:**
   - `ArchLeg_L/R` are now 1.45 deep, centred at z −10.06 (front −10.785, back −9.335, flush with the console bar).
   - `ArchCapital_L/R` are 1.55 deep, centred at z −10.11 (back −9.335), which closes their 0.047 gap too.
   - `sparkle_leg` didn't move.
9. **Ghost crystal:** `PylonShaft_L/R` and both under-feathers are now Transparency **0.12**. The console towers and rail
   posts stay at 0.25.

## R2 re-check (computed in Studio)
**Wings at ±0.28 rad about the hinges (∓1.85, 13.25):**

| Feather | x range | y range | Lowest clearance above the arch's outer surface |
|---|---|---|---|
| Main | 1.59-6.31 | 12.91-15.90 | 0.214 at the down-flap (0.30 at rest, 0.40 at the up-flap) |
| Under-feather | 1.82-4.95 | 12.10-14.07 | 0.214 |

- The clearance was sampled along every edge against the real stone faces. ≥ 0.15 holds everywhere.
- The feathers stay clear of the crown points in z: the main feather is within ±0.175 of the arch plane, the
  under-feather from +0.185 to +0.435, and the points start at ±0.35 only from x 1.55 inward.

**Diamond vs the crown:**
- Horizontal clearance to the points: 0.249.
- Horizontal clearance to the crown sparkles at 110 %: 0.215.

**Overall:** nothing passes y 16 or |x| 7.4 (the widest part is the stone corner at 7.333), and nothing enters the Zone,
the head box, the corridor or the exit walkway. The validator gives no WARN.

## Phase C captures (`T.lock("T11")` before EVERY capture, one at a time, unlocked afterwards; FOV 70)
- `T11_C_front55_b10b11`: camera (699, 7, −152) looking at (699, 7, −100), wings only.
- `T11_C_front55_b10b11_v2`: the same view after the taller crown points. **This is the final far front view.**
- `T11_C_close`, `T11_C_hub34`, `T11_C_spawn`, `T11_C_eye`, `T11_C_runner`, `T11_C_rear34`, `T11_C_lineup`.

## What the captures show
| View | Result |
|---|---|
| `runner` | "+1M / sec" is crisp. The bigger wings and crown are a top-of-frame accent, well clear of the label. The new centre diamonds stream under the runner |
| `close` | the skirt closes the screen-to-marquee gap; the arch joints are closed at the rim |
| `spawn` / `hub34` | the 12-wide winged crown spreads over the arch and reads solid white instead of grey shards. The taller points give a proper crown outline |
| `front55` / `lineup` | x20 is the tallest silhouette in the line |
| `rear34` | the pylons are less ghostly at Transparency 0.12 |

The "SCOPE / LOOP WARNING" hook messages during this pass came from repeating the same `T.lock("T11")` call before each
capture, as instructed. That's intentional, not a stuck loop.
