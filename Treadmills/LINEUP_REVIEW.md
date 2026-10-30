# LINEUP REVIEW: treadmills x12-x20, final gate (2026-10-12)

Reviewer: the final lineup reviewer. This was a READ-ONLY pass: I made no template or lab edits and did not call
`T.refresh` or `T.reset`.

**What I did:**
- Read `TREADMILL_BRIEF.md`, `PLAN_REVIEW.md`, and the `REVIEW.md` and Phase C notes for all five tiers.
- Dumped every bay in belt space and checked that each lab copy matches its template. They match: the only
  differences are rounding at 0.005.
- Ran a coplanar-face and floating-part scan on bays 7-11.
- Re-computed the animated extremes using the current `TreadmillClient` code.
- Took 25 captures. Each one was preceded by its own `T.lock("Final")` (true every time), was taken alone, and the
  lock was released with `T.unlock("Final")` at the end. Studio FOV was 70.

## OVERALL VERDICT: **SHIP**
All five tiers pass, and nothing is a MUST. The ladder reads as a clean staircase from every hub angle:
- Height, width of the crown and amount of motion grow at every step.
- Every tier has its own silhouette and palette and is distinct from x1-x10.
- Every Phase C fix landed exactly as written.

The 4 NICE items below are optional polish for the owner to decide on. None of them blocks shipping.

---

## 1. Validator (`T.validate`, run just now)
| Tier | Result | Visible parts (decor) | Accent parts | Lights | Label face |
|---|---|---|---|---|---|
| x12 Emerald | **0 FAIL / 0 WARN** | 68 (42) | 0 | 3 | (0,78,50), lum 0.23 |
| x14 Frost | **0 FAIL / 0 WARN** | 88 (62) | 7 Glass | 3 | (16,40,92), lum 0.15 |
| x16 Galaxy | **0 FAIL / 0 WARN** | 93 (67) | 0 | 2 | (16,10,36), lum 0.05 |
| x18 Inferno | **0 FAIL / 0 WARN** | 106 (80) | 2 Metal | 3 | (30,22,24), lum 0.09 |
| x20 Diamond Rainbow | **0 FAIL / 0 WARN** | 109 (83) | 13 Glass | 3 | (30,26,64), lum 0.12 |

**Scan results:**
- **Coplanar faces:** one known hit, `StarRayH`/`StarRayV` back faces at z -10.75 on x16. It is buried inside
  `ScreenDisplayFront` and can't be seen, as the x16 review already found. There is no other decor z-fighting.
- **Floating parts:** only the intended ones: x20's `halo` diamond and x16's `orb_shard_0` moon.
- **Extremes** (flames ×1.46, sparkles 110 %, halo and orb bob and spin, wings ±0.28 rad): every model stays under
  y 16 and within |x| 7.4 and z -11.8.

## 2. The ladder (measured in the lab, belt space)
| Tier | Solid top | Static peak | Anim max | Max \|x\| | Visible parts | Animated parts | Signature feature |
|---|---|---|---|---|---|---|---|
| x1 to x8 (T1-T5) | 6.44 → 8.53 | same | - | 4.5 → 7.1 | 14-26 | 0 | brick chassis, one colour each |
| x10 (T6) | 8.53 | 8.53 | - | 7.13 | 26 | 0 | gold/black chassis |
| **x12 Emerald** | 9.98 | 9.98 (crest gem) | 9.98 | 7.13 | **68** | **22** | jewel-green slab, emerald crest, low gem rails with a 12-rune chase |
| **x14 Frost** | 12.48 | 12.80 (crown gem) | 12.83 | 7.30 | **88** | **27** | snow-capped ice gate on the console, glass crystal crown, icicles, sliding ice skids |
| **x16 Galaxy** | 12.70 | 14.40 (planet) | 14.63 | 7.24 | **93** | **40** | violet star gate filled by a starfield monolith; ringed planet with orbiting moons; EQ |
| **x18 Inferno** | 13.40 | 14.90 (flame) | 15.64 | 7.14 | **106** | **40** | basalt floor gate, stepped volcano, 14 flickering flames, flexing swept fins, molten belt |
| **x20 Diamond Rainbow** | **15.00** | **15.77** (diamond) | **15.95** | **7.35** | **109** | **41** | 7-stone rainbow arch, winged crown, floating spinning diamond, rainbow road, white pylons |

- **Height:** every step goes up. The static peak rises 8.53 → 9.98 → 12.80 → 14.40 → 14.90 → 15.77. The solid top
  rises 8.53 → 9.98 → 12.48 → 12.70 → 13.40 → 15.00.
- **Parts:** visible parts rise at every step: 26 → 68 → 88 → 93 → 106 → 109. Animated parts go 0 → 22 → 27 → 40 →
  40 → 41. x16 and x18 tie on count; see NICE 2.
- **Width of the top:**
  - x12 has a crest only.
  - x14 has a full-width crown line.
  - x16's crown line is full width, plus the planet.
  - x18's volcano is full width.
  - x20 has a full-width round arch, with a winged crown about 12 studs wide on top.

### How it reads in the captures
- **Front, far** (`FL_front_all_122`: all 11 at about 120 studs; `FL_front_b6to11_70`; `FL_front_b1to7_70`):
  - x1 to x10 form one low band.
  - From x12 the models climb steadily to x20 on the left: x12's crest, x14's gate, x16's planet over its gate,
    x18's volcano and flames, then x20's arch with its crown.
  - No two models share an outline.
- **Rear / base side** (`FL_rear_all_118`, `FL_rear_b6to11_70`, `FL_rear45_b11to7`, `FL_rear_b9to11_eye`):
  - The clearest staircase of all.
  - The runner-side labels step +600K, +700K, +800K, +900K, +1M from left to right.
  - Each belt is a different road: emerald stripes, navy/white ice, violet runway, molten river, rainbow road.
- **Hub ±45°** (`FL_hub_plus45_b9_75`, `FL_hub_minus45_b9_75`):
  - From +45° the row recedes from x20 down to x1. It reads like a shop ladder: the best showcase shot.
  - From -45° the four gated tiers rise behind x12.
- **Pairs at 45-50 studs:** `FL_pair_6v7_45` / `FL_pair_6v7_hub34`, `FL_pair_7v8_45`, `FL_pair_8v9_48`,
  `FL_pair_9v10_50`, `FL_pair_10v11_48`.

| Step | How it reads |
|---|---|
| x10 → x12 | colour and richness (emerald jewel, crest, gem rails, chase). Same footprint; see NICE 1 |
| x12 → x14 | the big jump: first gate, crown line and icicles |
| x14 → x16 | heavier, filled monolith and a darker cosmic palette, with the planet on top |
| x16 → x18 | taller stepped peak, flames, fins, and the darkest, heaviest mass |
| x18 → x20 | the tallest and widest model, the only round silhouette, the only rainbow, a winged crown and a floating diamond |

**Distinctness** (checked against `FL_front_b1to7_70` and `FL_rear_all_118`):

| New tier | Compared with | Why it stays distinct |
|---|---|---|
| x12 jewel green with onyx | T4 grass green | T4 is matte grass green |
| x14 navy / snow / ice | T1 toy cyan | T1 is toy cyan |
| x16 violet / indigo with magenta accents | T3 pastel pink | T3 is pastel pink |
| x18 basalt, lava orange and crimson | T5 plain red/black | T5 is plain red/black |
| x20 white, spectrum and obsidian | T6 gold, and x14's white | it has nothing in common with T6's gold, and its rainbow arch separates it from x14 |

## 3. Phase C items: every one verified on the lab copy (part data)
| Tier | Item | Found |
|---|---|---|
| x12 | Screen bracket → EMERALD DEEP | (0,100,60) Plastic/Studs, CFrame unchanged ✓ |
| x12 | Crest gem → gem plastic | `screen_gem` Plastic/Weld (60,230,140), T 0.10, `CrestLight` inside ✓ |
| x14 | 1 Plinths | `ArchPlinth_L/_R` 1.493 wide at ±6.387 ✓ |
| x14 | 2 Icicles | `Icicle_L1/_R1` at ±3.886, butted flush ✓ |
| x14 | 3 Runes | `rune_6/_8` at x ±3.0, under the crystals ✓ |
| x14 | 4 Glass | all 7 Glass parts T 0.16, (170,216,248) ✓ |
| x14 | 5 Bracket | ICE (168,214,244) Weld ✓ |
| x14 | 6 Skids | `chevron_1..4` clear ice (196,232,255), T 0.20, Universal ✓ |
| x16 | Starfield light | `StarfieldWash` is gone (2 lights: PlanetGlow, RunnerGlow) ✓ |
| x16 | Planet ring | `orb_ring_a` 0.14×3.6×3.6, rot Z 110°, T 0.15, STARLIGHT ✓ |
| x16 | Moons | at r 2.35: (2.35, 13.95, -9.125), (-1.175, 13.45, -11.16), (-1.175, 13.75, -7.09) ✓ |
| x16 | EQ colours | magenta / violet (165,95,255) / lavender / violet / magenta ✓ |
| x16 | Runes | 12, including the lintel plates at (±1.3, 11.55, -7.56) ✓ |
| x16 | Arch caps | `ArchCap_L/_R` 1.5×0.5×1.93 at y 12.45 ✓ |
| x18 | Flames | crown C 0.9×1.1 at y 13.85, core C 0.5×1.6 at 14.1. Sides 0.7×0.8 / 0.35×1.3 at ±1.4. Torches 0.7×0.8 / 0.35×1.3 ✓ |
| x18 | Lava flow | `skull_eyes` 1.0 wide ✓ |
| x18 | Console slopes | `ConsoleSlope_L/_R` LAVA Inlet; `ConsoleStep` stays crimson ✓ |
| x18 | Bracket | BASALT (30,22,24) Studs ✓ |
| x18 | Exhausts | `flame_exhaust` 0.5×0.6×0.5 ✓ |
| x18 | Screen gem | `screen_gem` 0.85 ✓ |
| x18 | Runes | at y 2.955 ✓ |
| x20 | Chevrons | `chevron_7/_8` at (0, 0.32, -1.4) and (0, 0.32, 1.0) ✓ |
| x20 | Main feathers | 4.1 × 1.6 × 0.35 W Weld ✓ |
| x20 | Under-feathers | 2.9 × 1.1, T 0.12 ✓ |
| x20 | Hinges | at ∓1.85 ✓ |
| x20 | Crown points | `CrownPoint_1..4` 1.35 tall, top 15.0 ✓ |
| x20 | Marquee skirt | `MarqueeSkirt` 6.48×0.32×0.22 at (0, 8.69, -9.18), axis-aligned ✓ |
| x20 | Sparkle centres | crown 15.19, rail 2.79 ✓ |
| x20 | Diamond | `halo` 1.05 at y 14.86 ✓ |
| x20 | Arch stones | `ArchStone_1..7` 3.26 long ✓ |
| x20 | Crown band | `CrownBand` 3.3 ✓ |
| x20 | Arch legs | `ArchLeg` 1.45 deep at z -10.06 ✓ |
| x20 | Capitals | `ArchCapital` 1.55 deep ✓ |
| x20 | Crystal transparency | `PylonShaft` and under-feathers T 0.12 ✓ |

## 4. Runner views and broken-part check
**Runner views:** `FL_runner_7` … `FL_runner_11`, the preset camera, FOV 70.

| Tier | Label | What frames it |
|---|---|---|
| x12 | crisp | the crest sits above it; the gem rails converge |
| x14 | crisp, with a white border | the icicles hang clear at the gate corners; the skids show as ice inlays |
| x16 | crisp | the EQ sits above it; the 4 lintel runes are evenly spaced; the ringed planet is in frame |
| x18 | crisp, with a crimson border | the tapered two-tone flames sit on top; the fins frame the view like a cockpit |
| x20 | crisp | the rainbow EQ marquee is above it; the crown and wings are a top-of-frame accent |

- Nothing crosses or crowds the label in any of them.

**Broken-part check (far and pair views):**
- No floating bricks, no visible z-fighting, no clipping.
- The x20 rim notches, the screen-to-marquee gap and the leg slit are all closed (`FL_x20_hub_front_26`).
- The x14 plinths and icicles are flush.
- The mock labels rendered in every capture where they should.

---

## 5. Per-tier verdicts
### x12 Emerald: **PASS**
- **NICE 1 (owner's call, no action recommended):** x12 has the smallest silhouette step on the ladder.
  - It keeps T6's footprint and adds 1.45 of crest (`FL_pair_6v7_45`, `FL_front_all_122`). The step reads through
    colour and richness: 26 → 68 parts and the first motion.
  - From the ±45° bases and the rear the gem rails show clearly (`FL_pair_6v7_hub34`, `FL_rear_all_118`).
  - This is the "restrained first step" agreed in PLAN_REVIEW.
  - **Only if the owner wants more front pop:** enlarge the crest (gem and prongs) so the peak is about 10.6-10.8. That
    still leaves x14's crown (12.8) clearly above.

### x14 Frost: **PASS**
No items.

### x16 Galaxy: **PASS**
- **NICE 2 (no action):** the animated parts now tie x18 at 40, because the Phase C lintel runes added 2.
  - Accept it. x18's motion is bigger and runs at idle: 14 flames at up to ×1.46 and fins flexing ±16°. x16's runes
    only flash while running.
  - Changing x18 would cascade into x20's ≥ x18 rule.
- The planet is small beyond about 60 studs (`FL_front_b6to11_70`) but reads as a ringed planet at hub distance
  (`FL_pair_8v9_48`, `FL_runner_9`). No action.

### x18 Inferno: **PASS**
- **NICE 3 (optional, 2 property edits):** from the base side at eye level, `flame_exhaust_L/_R` (MAGMA Inlet) read
  as two small yellow nubs on the floor (`FL_rear_b9to11_eye`).
  - Fix: recolour them LAVA (255,100,0). This was the builder's own open option.
  - Cosmetic only.

### x20 Diamond Rainbow: **PASS**
- **NICE 4 (optional, 2 property edits):** at 45-55 studs the Weld X-pattern on the two white main feathers reads a
  little like "X" lattice marks beside the crown (`FL_pair_10v11_48`, `FL_pair_9v10_50`). Up close they read as
  feathers (`FL_x20_hub_front_26`).
  - Fix: try MaterialVariant Universal on the two 4.1-span main `wing_L/_R` only, and keep the crystal
    under-feathers on Weld.
  - Keep it only if the wings read as cleaner solid white in a 50-stud front capture.

---

## 6. Notes for the orchestrator (not model items)
1. **`TreadmillClient` chevrons now ride with the belt arrows** (lines 554-562), idle too. That fixes the lag the x14
   review reported.
   - Idle they move at 2.5 st/s. Running they move at 9 × (1 + 0.15 × (Tier − 1)): 18.45 st/s on x14 and 22.5 st/s
     on x20.
   - At 22.5 st/s each x20 tile wraps its 7.2-stud lane about 3 times a second.
   - Check once in a Play test that this reads as a stream, not a strobe, and that tiles and arrows move the same way.
2. **The lab ships if it stays where it is.** `workspace._TreadmillLab` (Archivable = true, x 490-710, z -100) and
   `ServerStorage._TreadLabTools` are still in the place.
   - Move the lab out of Workspace (or delete it) before the owner publishes.
3. **The templates live in `ServerStorage.Assets.Treadmills.Tier7_x12 … Tier11_x20`.**
   - The owner still has to Save, Publish and Migrate.
   - The ShopConfig prices are the orchestrator's to wire.

## 7. Captures (all `FL_*`, lock "Final")
| Group | Capture ids |
|---|---|
| Full lineup, front | `FL_front_all_122` (all 11), `FL_front_b6to11_70`, `FL_front_b1to7_70`. `FL_front_all_105` cuts off x20; don't use it |
| Rear / base side | `FL_rear_all_118`, `FL_rear_b6to11_70`, `FL_rear45_b11to7`, `FL_rear_b9to11_eye` |
| Hub ±45° | `FL_hub_plus45_b9_75`, `FL_hub_minus45_b9_75` |
| Pairs | `FL_pair_6v7_45`, `FL_pair_6v7_hub34`, `FL_pair_7v8_45`, `FL_pair_8v9_48`, `FL_pair_9v10_50`, `FL_pair_10v11_48` |
| x20 detail | `FL_x20_hub_front_26`, `FL_x20_hub34_40` |
| Runner | `FL_runner_7`, `FL_runner_8`, `FL_runner_9`, `FL_runner_10`, `FL_runner_11` |

### Showcase for the owner (best 6)
1. `FL_hub_plus45_b9_75`: the whole ladder receding from x20 down to x1, as seen from a ±45° base.
2. `FL_front_all_122`: all 11 tiers from the plaza side, with the new five climbing on the left.
3. `FL_rear_b6to11_70`: x10 → x20 from the base side, labels +600K … +1M, five different belts.
4. `FL_pair_9v10_50`: x14 / x16 / x18 / x20 side by side at hub distance.
5. `FL_runner_11`: the owner's view on x20 (rainbow road, EQ marquee, winged crown, "+1M / sec").
6. `FL_rear45_b11to7`: the rear 3/4 staircase with x20's pylons and rainbow road in front.
