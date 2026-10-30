# Tier9_x16 GALAXY: VISUAL REVIEW (Phase C, 2026-10-12)

Reviewer: independent visual reviewer. Read-only: no edits to the template, the lab, or anything else. No `T.refresh` or
`T.reset`. I read the brief, PLAN_REVIEW, PLAN and BUILD_NOTES, dumped every part of `Bay9.Treadmill` in belt space,
read `TreadmillClient` (orb, bars, sparkles, runes, findScreen), ran `T.validate(9)`, and ran a coplanar-face
(z-fighting) scan. All captures were taken one at a time under camera lock `Rev9` at FOV 70.

## VERDICT: **FIX** (2 MUST, 4 NICE, 1 answer)

The build is clean, accurate and on-ladder. Two things hold it back from "on point":
- the hub-side starfield turns into a flat pale-lilac panel when seen head-on from the plaza;
- the signature planet is too small to carry the "bigger difference" over x14.

Both fixes are cheap and stay inside the agreed ladder numbers.

### Validator and facts checked
- `T.validate(9)`: **0 FAIL, 0 WARN**. 89 visible parts (63 decor), 3 tilted parts (chassis only), 3 lights with
  Shadows off, 0 accent materials, Theme = Galaxy. Name, Tier, TierName, SpeedPerSecond and LabelHeight (10.6) are
  correct.
- **Plan-review x16 changes: all done, to the number.**
  - Posts y 2.06-10.9, lintel 10.9-12.2, wedges 9.6-10.9.
  - Runes at 2.45 / 5.65 / 7.45 / 9.25.
  - Tower 8.55-12.2. Runner display 8.85-10.75. Bars bottom 9.05, heights 0.9 / 1.15 / 1.4 / 1.15 / 0.9.
  - Hub display 8.85-11.9. TopperBase 12.2-12.5. Dish 12.5-12.7.
  - `orb_core` Ø1.4 at 13.7. Ring Ø3.0 at a 25° tilt. Moons Ø0.45 at r 2.0, y 13.45-13.95.
- **Ladder:**

  | | x14 (bay 8) | **x16** | x18 (bay 10) |
  |---|---|---|---|
  | Solid top | 12.48 | **12.7** | 13.4 |
  | Static peak | 12.8 | **14.4** | 14.9 |
  | Visible parts | 88 | **89** | 106 |
  | Animated parts | 27 | **38** | 42 |

- **R2 extremes (from the client code):**
  - `orb_core`: bob ±0.15 and pulse ×1.12 give y 12.77-14.63. It clears the dish by 0.07.
  - Ring rim: ≥ 12.85.
  - Moons: z -11.35..-6.90, y ≥ 13.07. Horizontal gap to the ring rim ≥ 0.24.
  - Bars only shrink (55-100 %).
  - Sparkles at 110 %:
    - rail stars: top 4.24 (< 4.5);
    - `sparkle_scr_2`: x 2.92 (display edge 2.94), and it clears bar_5;
    - front stars: stay off the stripe.
  - Nothing reaches the Zone, the over-head box, the runner corridor, the R1 walkway or the envelope.
- **Coplanar-face scan:** no decor z-fighting. The only decor pair, the back faces of `StarRayH` and `StarRayV` at
  z -10.75, is buried inside `ScreenDisplayFront`. The remaining hits are T6 chassis bottoms on the floor, the same as
  tier 6.

---

## Numbered items

### 1. MUST: the hub starfield washes out to pale lilac when seen head-on
**Evidence:** `Rev9_front30`, `Rev9_bays8to10_front`, `Rev9_lineup`, `Rev9_front24_spawnline`,
`Rev9_front_starfield_near`. Compare `Rev9_hub34`, `Rev9_eye` and `Rev9_far_m45`, where the same face is dark.

**What happens:**
- Seen straight on, `ScreenDisplayFront` (VOID 16,10,36) renders with a violet radial hotspot at 24 studs.
- At 30-60 studs the whole panel goes flat pale lilac (about 170,120,230). The white stars and the lavender rays lose
  most of their contrast.
- From oblique angles the same face is deep navy. The effect depends on the view angle and has the tint of
  `StarfieldWash` (170,120,255). It is almost certainly that SurfaceLight's specular on its own face.
- Bay 9 is the only lab tier with a SurfaceLight.

**Why it matters:**
- Spawn is straight in front of the middle base, so this head-on view is the most common plaza view.
- The tier's hero face then reads pastel instead of "deep space".

**Fix:**
1. Set `StarfieldWash.Enabled = false` and recapture head-on at about 24 and 46 studs, e.g. camera (666, 7.6, -124)
   and (666, 8, -146), both looking at (666, 7, -100).
2. If the wash is gone, either delete the light or bring it back at **Brightness ≤ 0.6, Range ≤ 8**.
3. A soft violet core glow around `screen_gem` up close is welcome (it looked good in `Rev9_front_starfield_near`).
4. If the wash stays with the light off, report it. The cause is then something else, so don't recolour blindly.

**Accept when:** in both head-on captures the display's outer half stays near VOID, and the 5 stars plus the gem read
crisp.

### 2. MUST: the planet is too small to carry the step over x14; widen it within the ladder
**Evidence:** `Rev9_lineup`, `Rev9_runner_zoomout` (x14 | x16 | x18 side by side), `Rev9_rear34`, `Rev9_front30`.

**What happens:**
- At 40-60 studs the Ø1.4 planet with its Ø3.0, T 0.3 lavender ring is a marble-sized dot. The pale ring vanishes
  against the sky.
- x14's five-crystal crown spans the full gate width. So from behind and from the lineup, x16's top line reads as
  "flat lintel plus a dot". It looks no richer than x14's crown, even though it is 1.6 higher.
- The planet is x16's signature motif. It has to read.

**Fix (keeps static peak ≤ 14.4, anim max ≤ 14.7, envelope z ≥ -11.8):**
- **`orb_ring_a`:**
  - Size 0.14 × 3.0 × 3.0 → **0.14 × 3.6 × 3.6**.
  - Rotation Z 115° → **110°** (tilt 25° → 20°).
  - Transparency 0.3 → **0.15**.
  - Results:
    - ring top 14.38 static and 14.53 with bob;
    - rim low point 12.87 (TopperBase 12.5);
    - over the dish edge ≥ 13.11 (dish 12.7).
  - Colour: try **STARLIGHT (255,240,178)**, a gold "Saturn" ring that pops on blue sky and against the magenta ball.
    If you keep LAVENDER, use T ≤ 0.15. Choose the one that reads better in a lineup capture.
- **Moons:** push the orbit radius 2.0 → **2.35** (gap to the ring rim 0.30; z sweep -11.70..-6.55; y unchanged).
  New static centres:
  - `orb_shard_0` (2.35, 13.95, -9.125)
  - `orb_shard_1` (-1.175, 13.45, -11.160)
  - `orb_shard_2` (-1.175, 13.75, -7.090)
- **Keep** the planet Ø1.4 at y 13.7 and the dish. A bigger ball only fits if the dish is removed, and it would gain
  just 0.2.
- Re-run the R2 numbers and record them in BUILD_NOTES.

**Accept when:** in a `lineup`-type capture the ring reads as a ring (not a smudge) and the planet system is clearly
the top feature of bays 7-9.

### 3. NICE: the equalizer colours read pale, and the cream bar echoes the label
**Evidence:** `Rev9_runner_screen_zoom`, `Rev9_side`, `Rev9_runner`.

**What happens:**
- The display sits in the lintel's shade. There, `screen_bar_2/_4` LAVENDER and `screen_bar_3` STARLIGHT read
  grey-lilac and khaki rather than lit.
- The cream centre bar sits right above the yellow "+800K", so it competes with the label.

**Suggestion:** a ramp from saturated at the edges to light in the middle, with no yellow:
- bar_1/_5 MAGENTA (keep);
- bar_2/_4 bright violet (165,95,255);
- bar_3 LAVENDER (196,168,255).

The two STARLIGHT `sparkle_scr_1/_2` stars stay.

### 4. NICE: smooth the rune chase across the lintel
**What happens:**
- Up the posts the white flash steps 3.2 / 1.8 / 1.8, then 3.5 onto the lintel.
- It then jumps **7.8 studs** from `rune_5` (x 3.9) to `rune_6` (x -3.9) in one sixth of a second.
- The runner sees the whole lintel (`Rev9_runner`), so the chase stutters right where the owner looks.

**Suggestion:**
- Add two runner-face rune plates on the lintel at x ±1.3:
  - 0.45 × 1.4 × 0.1;
  - centre (±1.3, 11.55, -7.56): on the lintel's runner face (-7.61), proud 0.05 top and bottom like the other bands;
  - MAGENTA, Universal.
- Renumber the runes to 12 in this order: +X post up (1-4), +3.9, +1.3, -1.3, -3.9, -X post down (9-12).
- Totals: visible parts 91, animated parts 40. That stays under x18's 42 and x20's 41, so the ladder order holds.

### 5. NICE: cap the gate corners to match the plinths
**Suggestion:**
- Add `ArchCap_L/_R`: 1.5 × 0.5 × 1.93, FRAME Studs, at (±6.4875, 12.45, -8.475), so y 12.2-12.7.
- They repeat the plinth (base and capital), overhang the lintel ends by 0.10 like the plinths, and give the flat top
  line two stepped corners.
- They stay within the limits: solid top 12.7 is still the target, |x| 7.24, lamp clearance 0.46.
- With item 4 the total is 93 visible parts, inside 88-96.

### 6. ANSWER (no change): keep the raised screen where it is; do not pull it back 0.4
**What the captures show:**
- At the hub's oblique angles the tower covers the far post's INNER side face (`Rev9_spawn`, `Rev9_hub34`,
  `Rev9_far_m45`, `Rev9_far_p45`).
- It reads as "screen mounted on the front of the gate". That is coherent.

**Why not pull it back:**
- Pulling it back 0.4 would cut that overlap by only about a third, because the post's inner face is exposed at any
  oblique angle.
- It would put the runner face at z -8.94, 0.21 in FRONT of the label's top edge (-9.152), so the runner display and
  bars would overhang the label bezel as a ledge.
- It would also break the flush tower/lintel joint.

Keep it at -10.64..-9.34.

### 7. NICE: rail-to-grip joint (optional)
**What happens:**
- `RailBar_L/_R` (y 3.2-3.85) meets the 1.21-square grips (y 3.163-4.374) nearly bottom-aligned, with a 0.04 step.
- It attaches below the grip centre (`Rev9_side`). It reads fine as a bigger grip knob, so this is low priority.

**Suggestion:** don't raise the rail. With the stars on top it would come within 0.02 of the 4.5 runner-corridor line.

---

## What is good: keep it
- **Craft:**
  - Every joint is flush. Plinth on the bar end, post on the plinth (outer face = bar end, 7.1345 / 7.1335), inner
    face flush with the handle ends (5.84).
  - Wedges seat against the post and the lintel. The tower is flush on the lintel's front face. TopperBase caps the
    lintel and tower exactly (z -10.64..-7.61, x ±3.24).
  - Rail posts sit on the side frames. Rail caps enclose the rail ends.
  - Bands are proud 0.05 all round. Stars are centred on their surfaces, so they never detach while they twinkle.
  - No z-fighting, no sky sliver at the tower/frame seam (`Rev9_side`, `Rev9_sideHi`, `Rev9_seam_side_low`), and
    perfect symmetry.
  - 100 % Plastic + Studs / Inlet / Universal / Weld: true to tiers 1-6.
- **Theme:**
  - Deep indigo, violet and magenta, with starlight accents. It reads instantly as the purple cosmic tier.
  - Nothing like T3's pastel pink (magenta is used only as small energy bands), and clearly apart from x12, x14, x18
    and x20 (`Rev9_lineup`, `Rev9_bays8to10_front`).
- **Runner view (`Rev9_runner`, `Rev9_runner_zoomout`):**
  - The best of the new tiers to run on: the gate frames the view, and the starred violet rails converge on the
    magenta centre runway.
  - The label "+800K / sec" is crisp on the VOID face. Neither RunnerGlow nor PlanetGlow lifts it.
  - The raised display sits ABOVE the label (bars start at 9.05, the label top is at 8.39) and cannot cover it from
    any camera in front of the console.
  - The planet is fully in frame at FOV 70.
- **The starfield face itself:** the gem, the 4-point lens flare and the scattered stars are a great hub-side hero.
  Up close (`Rev9_front_starfield_near`, `Rev9_close`) it looks premium. Item 1 is only about the distance and
  head-on wash.
- **Clearances:**
  - Upgrade signs untouched (`Rev9_rear34`, `Rev9_runner_zoomout`). Nothing at |x| > 6.4 for z 4-8.6.
  - Lamp clearance 0.46. R1 walkway empty: the rails' inner faces are at ±4.735.
- **Motion:** 38 animated parts.
  - The rune chase is numbered correctly.
  - The equalizer is bottom-anchored and only shrinks.
  - The planet, ring and moons are all mathematically clear at their extremes.
  - The x14 → x16 jump in life (27 → 38 animated parts) is a big, visible step. Keep all of it.

## Capture ids (lock `Rev9`, FOV 70)
| Group | Capture ids |
|---|---|
| Presets | `Rev9_runner`, `Rev9_spawn`, `Rev9_hub34`, `Rev9_eye`, `Rev9_side`, `Rev9_sideHi`, `Rev9_rear34`, `Rev9_close`, `Rev9_lineup` |
| Hub distance / angles | `Rev9_far_m45`, `Rev9_far_p45`, `Rev9_bays8to10_front` (46 studs), `Rev9_front30`, `Rev9_front24_spawnline` |
| Detail | `Rev9_runner_screen_zoom`, `Rev9_front_starfield_near`, `Rev9_seam_side_low`, `Rev9_runner_zoomout` |

## After the fixes, recapture
- `runner`, `hub34`, `lineup` and `rear34`.
- The two head-on checks from item 1.
- `T.validate(9)` (0 FAIL / 0 WARN).
- The R2 numbers for the new ring and moons.
