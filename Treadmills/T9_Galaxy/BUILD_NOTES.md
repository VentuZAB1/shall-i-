# Tier9_x16 GALAXY "Star Gate": BUILD NOTES (Phase B, 2026-10-12)

## What was built
Template: `ServerStorage.Assets.Treadmills.Tier9_x16`, built exactly to PLAN.md plus the binding x16 changes in
`../PLAN_REVIEW.md`. The bay copy (`Bay9.Treadmill`) was refreshed with `T.refresh(9)`.

The build is reproducible: `build_t9.luau` in this folder is idempotent. It recolours the chassis, clears and rebuilds
`Decor` from a spec, adds the lights, refreshes Bay9 and prints the validator report plus the rune order.

- **Attributes:** Theme = "Galaxy". Name, Tier 9, TierName x16, SpeedPerSecond 800000 and LabelHeight 10.6 are
  unchanged.
- **Chassis (26 parts):** only Color and MaterialVariant changed, as in the PLAN recolour map.
  - The label FACE is VOID (16,10,36), lum 0.05.
  - The label FRAME is the violet bezel; the bracket is magenta.
  - The belt reads violet edge | dark | dark | magenta centre | dark | dark | violet edge.
- **Decor (63 parts):**

| Group | Parts | Count |
|---|---|---|
| A. Star Gate on the front console bar ends | plinths, posts (y 2.06-10.9), lintel (10.9-12.2), 2 corner wedges, `rune_1..10` | 17 |
| B. Raised screen tower | tower (8.55-12.2, z -10.64..-9.34) | 18 total |
| | runner display (8.85-10.75) with `screen_bar_1..5` (bottom 9.05, heights 0.9/1.15/1.4/1.15/0.9) and `sparkle_scr_1/2` | |
| | hub display (8.85-11.9) with `screen_gem`, StarRayH/V and `sparkle_scr_3..7` | |
| C. Topper | TopperBase 0.3 (12.2-12.5), PlanetDish 0.2 (12.5-12.7), `orb_core` Ø1.4 at y 13.7, `orb_ring_a` Ø3.0 tilted 25° about Z (T 0.3), `orb_shard_0..2` Ø0.45 at orbit radius 2.0 (y 13.95 / 13.45 / 13.75) | 7 |
| D. Rails | 2 rail bars from the grips to z 7.6 (y 3.2-3.85), 6 posts, `sparkle_rail_L1..3/R1..3`, 2 magenta caps | 16 |
| E. Front console bar | magenta FrontStripe, `sparkle_front_1..4` | 5 |

- **Lights (3, Shadows off):**
  - PlanetGlow: PointLight in `orb_core`, (255,90,225), Brightness 2, Range 10.
  - StarfieldWash: SurfaceLight on `ScreenDisplayFront`, Face Front (-Z), (170,120,255), Brightness 1.5, Range 12,
    Angle 110.
  - RunnerGlow: PointLight in `ScreenDisplayRunner`, (200,130,255), Brightness 0.8, Range 7.
  - R3: in the `runner` capture the label face stays dark and the text is crisp, so RunnerGlow stays (it is already
    ≤ 1.0).

## Final validator output (`T.refresh(9)`)
```
== Tier9 Galaxy: 0 FAIL, 0 WARN
ok   label screen = Part 6.1x3.1 colour (16,10,36) lum 0.05, 3 tilted parts
ok   89 visible parts (63 decor), 0 accent-material parts, 3 lights; animation hooks: orb_shard_0 x1, sparkle_ x17,
     orb_shard_2 x1, orb_core x1, rune_ x10, screen_gem x1, orb_ring_a x1, screen_bar_ x5, orb_shard_1 x1
```
- The tilted count is still 3 (chassis bracket, face and frame only). No decor part is X-tilted.
- The new rear-walkway rule (R1) passes: the rails sit at |x| >= 4.685 and nothing is behind the belt.

## Rune order, printed from the refreshed bay (numbering = chase order)
`1(6.5,2.5) > 2(6.5,5.7) > 3(6.5,7.5) > 4(6.5,9.2) > 5(3.9,11.6) > 6(-3.9,11.6) > 7(-6.5,9.2) > 8(-6.5,7.5) >
9(-6.5,5.7) > 10(-6.5,2.5)`

The flash runs up the +X post, across the lintel and down the -X post.

## R2: animated extremes (computed on the template)
| Hook | Extreme | Range | Clearance |
|---|---|---|---|
| `orb_core` | bob ±0.15, pulse ×1.12 | y 12.77-14.63 | dish top 12.70; anim max ≤ 14.7 ✓ |
| `orb_ring_a` | every spin angle, with bob | rim y 12.85-14.55 | clears the topper by more than 0.35 |
| `orb_shard_0..2` | orbit r 2.00 | ring rim r 1.50 | moon gap 0.27; z sweep -11.43..-6.88, y ≥ 13.07 |
| Sparkles | 110 % | rail star top 4.239 | runner corridor starts at 4.5 |

- The equalizer bars only shrink (bottom-anchored). The runes and `screen_gem` change colour only.
- Over all hooks at their extremes: x -5.57..5.57, y 0.65..14.63, z -11.43..6.88.
- No hook enters the Zone, the RUN corridor, the HEAD box or the EXIT walkway, and none leaves the envelope.

## Ladder check (PLAN_REVIEW §1, x16 row)
- **Solid top:** 12.7 (dish), target ≤ 12.7 ✓.
- **Static peak:** 14.4 (planet top; the ring top is about 14.40), target ≤ 14.4 ✓.
- **Anim max:** 14.63, target ≤ 14.7 ✓.
- **Visible parts:** 89 (88-96) ✓.
- **Animated parts:** 38 (10 runes, 5 bars, 17 sparkles, 5 orb parts, 1 gem) ✓.

## Captures (taken one at a time under camera lock "T9")
| Preset | Capture ids |
|---|---|
| hub34 | `T9_hub34_v1` |
| runner | `T9_runner_v1b` (label not yet rendered, a Studio render hiccup), `T9_runner_v1c` (label OK) |
| spawn | `T9_spawn_v1` |
| side | `T9_side_v1` |
| sideHi | `T9_sideHi_v1` |
| close | `T9_close_v1` |
| eye | `T9_eye_v1` |
| rear34 | `T9_rear34_v1` |
| lineup | `T9_lineup_v1` (x18 to its left, x14 to its right) |

Phase A study captures: `T9_A_*`. Final captures after the last tweak: see the "Final" section below.

## What I looked at, critically
- **runner:**
  - The gate frames the view, with magenta bands up both posts and two on the lintel.
  - The raised screen sits right above the label: dark display, 5-bar equalizer and 2 stars.
  - The label "+800K / sec" reads crisp on the VOID face inside the violet bezel.
  - Starlit violet rails run along both sides, over the magenta centre runway.
  - Nothing is over the head or in the corridor.
  - The planet is clipped at the top edge in this preset only because the Studio camera FOV is 50. The game client's
    default is 70, which shows the whole planet with room to spare.
- **rear34:** the strongest view. The ringed planet with moons on the gate, the equalizer, the label and the starred
  rails with magenta caps. It is clearly above x14's white ice gate next door.
- **lineup:** reads instantly as the purple tier with a planet. The gate is filled by the dark starfield monolith (the
  magenta gem and white stars read at 60 studs). It sits between x14 (lower, white) and x18.
- **spawn / hub34:** the tower stands 1.3 in front of the gate plane, so from oblique angles it overlaps part of one
  post. It reads as "screen mounted on the front of the gate". I kept it there; reasons are under "Anything unsure".
  The planet is cut at the top of these presets by their low look-at point.
- **eye / close:** the posts with bands frame the console. The violet label-frame back carries the magenta bracket,
  and the front bar's magenta stripe plus 4 stars give the plaza a galaxy face at eye height.
- **side / sideHi:** the rails, posts, stars and caps read cleanly. No sky sliver shows at the screen seam, so the
  optional filler wedge was not added.

## Small changes vs the plan (all inside the review's numbers)
- `sparkle_scr_1/2` moved to (±2.65, 10.2) so their tops are at 10.45, matching the review's "y ≤ 10.45". They stay
  clear of the outer bars at 110 %.
- All other coordinates are exactly as in PLAN.md with the review's x16 changes:
  - post runes at 2.45 / 5.65 / 7.45 / 9.25;
  - wedges at 9.6-10.9;
  - starfield re-spread inside 8.85-11.9.

## Anything unsure
- **Tower depth:** the tower sits 1.3 in front of the arch plane, as approved, to keep the label safe from high
  cameras: its runner face (-9.34) is behind the label's top edge (-9.16). Pulling it back about 0.4 would tighten the
  oblique look in `hub34`, but it would then sit slightly in front of the label edge. I left it as approved; tell me
  if you prefer the tighter look.
- **Starfield lighting:** the starfield SurfaceLight hardly shows in the daylight lab. It is meant for the plaza at
  dusk.

## Final (after the sparkle_scr_1/2 tweak)
- `T.refresh(9)` / `T.validate(9)`: **0 FAIL, 0 WARN**. 89 visible parts, 3 tilted parts, 3 lights, same hook list as
  above.
- Final captures (lock "T9"):
  - `T9_runner_v2`: label crisp; the two stars now sit at the display's upper corners.
  - `T9_hub34_v2`: unchanged from v1.
- Earlier v1 captures of the other presets still apply; nothing else changed.
- **Camera lock:** `T.lock` was refused for several minutes while Rev7, T8, T10 and T11 held the camera. I never
  forced a takeover. Every capture was taken one at a time under my own lock, and the lock was released afterwards.

---

# Phase C: fixes from REVIEW.md (2026-10-12)
I rebuilt from the updated `build_t9.luau`, which now holds all the Phase C values (`STARFIELD_WASH = false`). Then I
ran `T.refresh(9)`.

| # | Item | What I did |
|---|---|---|
| 1 | MUST: starfield wash | **Cause confirmed: the `StarfieldWash` SurfaceLight. It is now deleted.** |
| 2 | MUST: planet reads as a marble | `orb_ring_a` is 0.14 × 3.6 × 3.6, rotated Z 110° (20° tilt), Transparency 0.15, **STARLIGHT (255,240,178)**. Moons at orbit radius 2.35: `orb_shard_0` (2.35, 13.95, -9.125), `orb_shard_1` (-1.175, 13.45, -11.160), `orb_shard_2` (-1.175, 13.75, -7.090). The planet stays Ø1.4 at y 13.7; the dish stays. |
| 3 | NICE: equalizer colours | `screen_bar_1/5` MAGENTA, `screen_bar_2/4` bright violet (165,95,255), `screen_bar_3` LAVENDER. No cream bar over the yellow label any more. |
| 4 | NICE: rune chase | 2 runner-face rune plates, 0.45 × 1.4 × 0.1, at (±1.3, 11.55, -7.56), MAGENTA Universal. Renumbered to 12 runes in chase order. |
| 5 | NICE: gate corners | `ArchCap_L/_R`: 1.5 × 0.5 × 1.93, FRAME Studs, at (±6.4875, 12.45, -8.475), y 12.2-12.7. |
| 6 | Raised screen | Kept at z -10.64..-9.34, as the review answered. |
| 7 | Rail-to-grip joint | Left as it was. |

**Item 1 in detail:**
- With the light disabled, both head-on captures show the display as deep VOID with crisp stars, rays and gem:
  `T9C_front24_lightoff` (camera 666,7.6,-124) and `T9C_front46_lightoff` (666,8,-146).
- I then tried the allowed fallback (Brightness 0.6, Range 8):
  - `T9C_front24_light06`: a nice soft core glow at 24 studs.
  - `T9C_front46_light06`: at 46 studs the whole panel lifts to a medium purple again, which fails the "outer half
    near VOID" test.
- So the light is removed. Lights are now 2: PlanetGlow and RunnerGlow.

**Item 2, ring colour:** STARLIGHT was kept. In `T9C_lineup_starring`, `T9C_rear34` and `T9C_runner` the warm gold
ring reads as a real Saturn ring against the blue sky, around the magenta ball. LAVENDER was the colour that vanished
against the sky before.

**Item 4, rune order (printed from the bay):**
`1(6.5,2.5) > 2(6.5,5.7) > 3(6.5,7.5) > 4(6.5,9.2) > 5(3.9,11.6) > 6(1.3,11.6,z-7.56) > 7(-1.3,11.6,z-7.56) >
8(-3.9,11.6) > 9(-6.5,9.2) > 10(-6.5,7.5) > 11(-6.5,5.7) > 12(-6.5,2.5)`

The lintel steps are now 2.6 studs instead of one 7.8 jump.

## Validator after Phase C (`T.refresh(9)` / `T.validate(9)`)
```
== Tier9 Galaxy: 0 FAIL, 0 WARN
ok   label screen = Part 6.1x3.1 colour (16,10,36) lum 0.05, 3 tilted parts
ok   93 visible parts (67 decor), 0 accent-material parts, 2 lights; animation hooks: orb_shard_0 x1, sparkle_ x17,
     orb_shard_2 x1, orb_core x1, rune_ x12, screen_gem x1, orb_ring_a x1, screen_bar_ x5, orb_shard_1 x1
```

## Ladder and R2 after Phase C (computed on the template)
| Check | Value | Limit |
|---|---|---|
| Solid top | **12.70** (ArchCaps and dish) | ≤ 12.7 |
| Static peak | **14.40** (planet; ring top 14.38) | ≤ 14.4 |
| Anim max | **14.63** (`orb_core` bob + pulse) | ≤ 14.7 |
| Ring rim, every spin + bob | 12.87 to 14.53 | TopperBase 12.50; never passes over the dish (rim horizontal radius ≥ 1.69 > 1.0) |
| Moon gap to ring rim | 0.325 | - |
| Moon z sweep | -11.70..-6.55 | envelope ≥ -11.8 |
| Rail sparkle top at 110 % | 4.239 | corridor starts at 4.5 |
| Hits on Zone / RUN / HEAD / EXIT / envelope | none | - |

- **Visible parts:** **93** (88-96). **Animated parts:** **40** (12 runes, 5 bars, 17 sparkles, 5 orb parts, 1 gem).
  That is ≤ 40 and under x18's.

## Phase C captures (lock "T9", one at a time, Studio FOV 70)
| Group | Capture ids |
|---|---|
| Head-on checks | `T9C_front24_lightoff`, `T9C_front46_lightoff`, `T9C_front24_light06`, `T9C_front46_light06`, `T9C_front46_final` (the final head-on far view) |
| Presets | `T9C_lineup_starring`, `T9C_rear34`, `T9C_runner`, `T9C_spawn`, `T9C_hub34`, `T9C_eye` |

What the captures show:
- **Head-on (24 / 46 studs):** the starfield stays deep space with crisp stars and gem. The planet reads as a ringed
  Saturn above the gate.
- **runner (FOV 70):** the whole ringed planet is in frame. The 4 lintel runes are evenly spaced. The equalizer is
  magenta / violet / lavender. The label is crisp.
- **rear34 / lineup:** the gold-ringed planet is the clear top feature of bays 7-9.
- **hub34 / spawn / eye:** the ArchCaps give the gate stepped corners.
