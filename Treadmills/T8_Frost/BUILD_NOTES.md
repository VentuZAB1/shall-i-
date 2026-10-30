# Tier 8 `Tier8_x14` (x14, 700K/s): FROST: BUILD NOTES (Phase B, 2026-10-12)

Built in `ServerStorage.Assets.Treadmills.Tier8_x14` only, with `T.refresh(8)` after each step. Nothing else was
touched: no scripts, no other templates or bays, and Play was never started.

Theme attribute: `Frost`. Name, Tier 8, TierName x14, SpeedPerSecond 700000 and LabelHeight 10.6 are unchanged.

## Final validator (`T.validate(8)`)
```
== Tier8 Frost: 0 FAIL, 0 WARN
ok   label screen = Part 6.1x3.1 colour (16,40,92) lum 0.15, 3 tilted parts
ok   88 visible parts (62 decor), 7 accent-material parts, 3 lights; animation hooks: sparkle_ x9, chevron_ x4, screen_gem x1, rune_ x13
```

## What was built: the approved PLAN.md plus every PLAN_REVIEW x14 change

### Chassis (26 parts)
Recoloured exactly as in the plan. Parts were matched by size, and the belt strips by x.

| Role | Colour | Variant | Parts |
|---|---|---|---|
| FRAME (24,40,82) | navy | Studs | side frames, both console bars, handles, handle caps |
| FRAME (24,40,82) | navy | Inlet | belt strips at x 0 and ±2.59 |
| SNOW (238,247,255) | white | Inlet | belt strips at ±1.30 and ±3.89 |
| SNOW | white | Studs | screen frame, bracket |
| SNOW | white | Weld | feet |
| ICE (168,214,244) | pale blue | Weld | base plate, console posts, console panel |
| GLACIER (120,185,240) | blue | Weld | grips |
| MIDNIGHT (16,40,92) | dark navy | Universal | screen face (luminance 0.15, opaque) |

### Decor (62 parts)
Sub-models: `Decor/Arch`, `Decor/Rails`, `Decor/Front` and `Decor/Belt`.

**Arch (33 parts):**
- **Structure:**
  - `ArchPlinth_L/_R` (FRAME) sit on the console bar ends.
  - Each pillar is `ArchPillarLow` (SNOW), `ArchPillarIce` (Glass, T 0.3, with `PillarLight`) and `ArchPillarHigh`
    (SNOW), at x ±6.4365. Their inner faces are flush on the handles.
  - `ArchLintel` (FRAME, y 9.9-11.1) with `ArchSnowCap` on top (SNOW, y 11.1-11.5, overhanging 0.2).
  - `ArchCorner_L/_R`: WedgePart braces in the inner corners.
- **Icicles:** 4.
- **Crown (review change 2):**
  - `CrownCrystal_L2/_R2`: 0.7 x 1.2 x 0.7, lean 20°, x ±6.2.
  - `CrownCrystal_L1/_R1`: 0.8 x 1.2 x 0.8, lean 12°, moved to x ±3.0.
  - NEW `CrownCrystal_C`: 0.9 x 1.3 x 0.9, upright, y 11.18-12.48, with `CrownLight`.
  - All 5 crystals are Glass, T 0.3.
  - `sparkle_crown_1..4` are 0.4 cubes; `sparkle_crown_5` is a 0.45 cube.
- **`rune_4..10`:** 0.6 x 0.6 x 1.6 through-inlays on the pillars and the lintel.

**Rails (18 parts):**
- `SideSnow_L/_R`: a snow layer on the side frames.
- `RailPost_L1..3/_R1..3` (FRAME).
- `RailBar_L/_R`: CLEAR ICE, **T 0.22** (review change 5). They run from the grip's back face to z 7.6.
- `rune_1..3` / `rune_11..13`: GLACIER bands.
- `sparkle_rail_L/_R`.

**Front (7 parts):**
- `ConsoleSnow`: the snow lip.
- `GemFrost`: a white diamond plate, with `screen_gem` (GLACIER diamond) on it.
- `FootCrystal_L/_R`: CLEAR ICE, T 0.22, leaning 15°.
- `sparkle_foot_L/_R`.

**Belt (4 parts, review change 4):**
- `chevron_1..4` "ice skids": SNOW, 0.6 x 0.12 x 1.4.
- They lie on the navy strips (y 0.266-0.386) at (-2.594, -3.0), (0, -1.2), (2.594, 0.6), (0, 2.4).

**Removed (review change 1):** `halo`, `HaloCradle_L/_R`.

**Lights (review change 3):** `CrownLight` in `CrownCrystal_C`, plus `PillarLight_L/_R`. 3 in total, all with Shadows
off.

## Small changes made during the build
1. **Icicles are now inverted `CornerWedgePart` spikes, not flat WedgeParts.**
   - Why: in `T8_eye_v1` and `T8_close_v1` the right-triangle wedges read as glass panes or sails.
   - Now each icicle is a 3D pyramid with its point at the front corner, so it reads as an icicle from every preset
     (`T8_eye_v3`, `T8_hub34_v3`).
   - The part count didn't change, and no extra bricks were needed (the 88-part budget had no room for 2-brick
     sticks).
   - Tips:
     - The long icicles hang to y 8.10 at abs(x) 3.40-4.10, outside the screen frame (abs(x) 3.24).
     - The short icicles end at y 9.10 at abs(x) 1.50-2.10.
     - Every icicle has ToOrientation rx = 0, so none can be mistaken for the label screen.
2. **Translucency:** every CLEAR ICE part uses T 0.22, including the foot crystals, so they look consistent. The review
   only required this for the icicles and rails.
3. **GLACIER is (120,185,240) from the start, as the review recommended.**
   - The rune numbering is the chase order: the client sorts by number.

## Checks
- **Static peak:** 12.798, `sparkle_crown_5` (limit 12.8).
  - The highest non-sparkle part is `CrownCrystal_C` at 12.48. The snow cap top is 11.5.
- **Sparkles at 110 % (R2):** the peak is 12.83 (limit 12.9).
  - The foot sparkles reach max abs(x) 7.14 (limit 7.4).
  - The rail sparkles top out at 4.42, under the corridor's 4.5.
  - None enters the Zone, the corridor, the over-head box or the exit walkway.
- **Chevrons:** swept over the full wrap range (z -4.5..4.1). No limit box is hit, and they stay under the Zone (top
  0.386 < 0.6).
- **Max abs(x):** 7.300 (`ArchSnowCap`).
- **Exit walkway R1** (abs(x) <= 4.1, z >= 7, y 0.3-6.6): empty. The validator rule passes.
- **Rune order** in the bay clone, sorted by number:
  ```
  1(-5.2,3.8,4.9) 2(-5.2,3.8,0.4) 3(-5.2,3.8,-3.5) 4(-6.4,3.7,-8.5) 5(-6.4,8.6,-8.5) 6(-3.6,10.5,-8.5)
  7(0,10.5,-8.5) 8(3.6,10.5,-8.5) 9(6.4,8.6,-8.5) 10(6.4,3.7,-8.5) 11(5.2,3.8,-3.5) 12(5.2,3.8,0.4) 13(5.2,3.8,4.9)
  ```
  That is left rail back→front, up the left pillar, across the lintel, down the right pillar, then right rail
  front→back.
- **Label in `runner` with the lights on (R3):** the face stays dark navy, and "+700K / sec" reads crisply inside a white
  border. No light dims or tints it, so the brightness is unchanged.
- **Glass:** it reads as pale translucent ice in `hub34`, `spawn` and `lineup`, so the Glass look was kept and the
  plastic fallback wasn't needed.
- **Accent materials:** 7 of 88 (cap 13).

## Captures
All were taken under the camera lock (`lock("T8")`), one at a time, then unlocked.

| Capture ids | State |
|---|---|
| `T8_spawn_v3`, `T8_hub34_v3`, `T8_eye_v3`, `T8_side_v3`, `T8_sideHi_v3`, `T8_runner_v3b`, `T8_rear34_v3`, `T8_close_v3`, `T8_lineup_v3` | **Final** |
| `T8_spawn_v2`, `T8_hub34_v2`, `T8_eye_v2`, `T8_side_v2`, `T8_sideHi_v2`, `T8_runner_v2`, `T8_rear34_v2`, `T8_close_v2`, `T8_lineup_v2` | Full build with the flat wedge icicles |
| `T8_hub34_v1`, `T8_runner_v1b`, `T8_close_v1`, `T8_eye_v1` | Chassis plus arch only |

What the final captures show:
- **`lineup_v3`:** x16 Galaxy (left) is clearly bigger: planet plus a filled monolith. x14 Frost (centre) is a white and
  ice gate with a crown. x12 Emerald (right) is clearly smaller: no gate.
- **`rear34_v3`:** the gate, the handrails and the snow lines read well from the base side. The upgrade sign is
  unobstructed.

## Unsure / notes for the reviewer
- **The mock label can be missing on the first capture after a refresh.** It happened in `T8_runner_v1` and
  `T8_runner_v3`: the label was missing on the first capture and was there on the immediate retake (`_v1b`, `_v3b`).
  This is a render-timing effect of the freshly made SurfaceGui, not a model problem.
- **The `side` preset sits only 11 studs from the belt centre,** so it shows a close, oblique profile rather than a full
  side elevation.
- **The camera lock was taken over once** by another builder after its 60 s age limit.
  - That happened between `T8_eye_v2` and `T8_side_v2`.
  - `T8_eye_v2` matches the v1 and v3 eye shots, so I don't think it was swapped.
  - From then on I re-locked every 2 captures.
- **The workspace attribute `TestFreshSave` is false.** I never started Play, so it didn't matter for this job. Check
  it before any Play test.

## Phase C (polish, 2026-10-12)
REVIEW.md verdict: **PASS**, with no MUST items. I applied all 6 NICE items in the template only, using property and
CFrame edits. The part count is unchanged.

| # | Item | What I did |
|---|---|---|
| 1 | Plinth overhang | `ArchPlinth_L/_R` are now `Size.X` 1.4935 at x ±6.3868. They span abs(x) 5.6400-7.1335, flush with the console bar ends. The inner face is still flush with the end of `ConsoleSnow`, and the pillars (5.84-7.04) still sit on the plinth |
| 2 | Long-icicle sliver | **Butted flush**: `Icicle_L1/_R1` centre ±3.8865, so x 3.5365-4.2365, which is the exact inner tip of `ArchCorner`. y 8.10-9.90 is unchanged. Why flush (see `T8_eye_C1`, `T8_hub34_C1`): the brace and the icicle now read as one hanging ice fang at each gate corner. The other option (±3.60) would hang the icicle right against the label frame's edge (3.24) in the runner view and still leave a narrow slot |
| 3 | Rune and crystal columns | `rune_6` / `rune_8` moved to x ±3.0, under `CrownCrystal_L1/_R1`. The beam now has 5 aligned light-and-crystal columns. The chase numbering is unchanged |
| 4 | Glass | All 7 Glass parts (the 2 pillar ice blocks and the 5 crown crystals) are now Transparency **0.16** and a slightly deeper ice tint, **(170, 216, 248)**. All are still Glass |
| 5 | Screen back | Only the chassis bracket (2.16x2.85x0.99, tilted) changed: it is now **ICE (168,214,244) / Weld**. It reads as an ice panel on the plaza side and continues the ICE/Weld console core below it. The screen frame stays SNOW, so the runner's label border stays white. Size and tilt are untouched, so there are still 3 tilted parts and the label stays on the face |
| 6 | Ice skids | `chevron_1..4` are now **CLEAR ICE (196,232,255), Transparency 0.2**, Plastic/Universal. Size and positions are unchanged |

### Validator after Phase C
```
== Tier8 Frost: 0 FAIL, 0 WARN
ok   label screen = Part 6.1x3.1 colour (16,40,92) lum 0.15, 3 tilted parts
ok   88 visible parts (62 decor), 7 accent-material parts, 3 lights; animation hooks: sparkle_ x9, chevron_ x4, screen_gem x1, rune_ x13
```
- The static peak is still 12.798 (`sparkle_crown_5`, limit 12.8), and max abs(x) is still 7.300.
- The crown, sparkle and skid geometry didn't change, so the earlier 110 % and sweep checks still hold.

### Phase C captures
These were taken with the Studio camera at FOV 70, under lock "T8", one at a time, then unlocked:
- `T8_eye_C1`
- `T8_hub34_C1`
- `T8_spawn_C1`
- `T8_runner_C1`
- `T8_close_C1`
- `T8_farfront_C1`: far front view, camera [644, 8, -150] looking at [644, 5.6, -100], 50 studs at near-eye height,
  with x18 / x16 / x14 / x12 in frame.

What they show:
- **Runner (`T8_runner_C1`):** "+700K / sec" is crisp. The long icicles stay clear of the label.
- **Pillars (`T8_close_C1`):** the glass ice blocks now read as solid pale-blue ice instead of a gap in the pillar.
- **Far front (`T8_farfront_C1`):** the crown reads as a row of ice spikes at 50 studs. The ladder holds: x16 is bigger,
  x12 is smaller.

### Unsure
- At Transparency 0.16, the Glass pillar blocks still let a little sky through at the closest camera (`T8_close_C1`).
  That's intended, so they still read as glass and ice.
- If the owner wants them fully solid, the next step is Transparency 0.1 on all 7 Glass parts together, so the look
  stays uniform.
