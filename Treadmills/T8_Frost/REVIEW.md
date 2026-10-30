# Tier 8 `Tier8_x14` (x14, 700K/s): FROST: VISUAL REVIEW (Phase C, 2026-10-12)

Reviewer: independent visual reviewer. **Read-only:** nothing in the game was edited (no `T.refresh` / `T.reset`, no
template or lab edits). Camera lock `Rev8`; captures were taken one at a time, then unlocked.

## VERDICT: PASS

There are no MUST items. The build is clean, on theme, and sits exactly on the agreed ladder. All six PLAN_REVIEW
changes are done. The 6 NICE items below are cheap polish (about 10 property edits, part count unchanged). Please do
them in Phase C so the build is "on point perfect", then re-run `T.validate(8)` and recapture.

## Evidence
- **Validator:** `T.validate(8)` = **0 FAIL, 0 WARN**. 88 visible parts (62 decor), 7 accent parts, 3 lights. Hooks:
  `sparkle_` x9, `chevron_` x4, `screen_gem` x1, `rune_` x13.
- **Template vs lab:** the lab copy in Bay8 is identical to the template (all 67 named parts: position, size, colour,
  material). The template holds only parts and the 3 PointLights, with no leftover GUI.
- **Captures (mine):**
  - Presets: `R8_hub34`, `R8_spawn`, `R8_runner`, `R8_rear34`, `R8_eye`, `R8_close`, `R8_side`, `R8_sideHi`, `R8_lineup`.
  - Extra: `R8_front_icicles` (straight front at y 9.5), `R8_far45_negX` / `R8_far45_posX` (50 studs, ±45°),
    `R8_bays7to9_front_eye40` (48 studs, eye height), `R8_bay1_hub34_compare` (T1), `R8_crown_close_front_hi`,
    `R8_icicles_back_low`, `R8_plinth_corner`, `R8_exit_rear_low`, `R8_runner_zoomout_high`.
- **Ladder (measured in the lab, belt space):**

| Tier | Visible parts | Animated parts | Static peak | Solid top |
|---|---|---|---|---|
| x12 Emerald (bay 7) | 68 | 22 | 9.98 | 9.98 |
| **x14 Frost (bay 8)** | **88** | **27** | **12.80** (`sparkle_crown_5`) | **12.48** (`CrownCrystal_C`), cap 11.5 |
| x16 Galaxy (bay 9) | 89 | 38 | 14.40 | 12.70 |

## Review changes: all done
| # | Change | Status |
|---|---|---|
| 1 | `halo` and `HaloCradle_L/_R` removed | Done |
| 2 | Crown peak 12.80 (limit 12.8) and 12.83 at 110 % (limit 12.9). `CrownCrystal_C` 0.9x1.3x0.9 at y 11.18-12.48. Inner pair base at ±3.0. Sparkles 0.4 / 0.45 | Done |
| 3 | `CrownLight` in `CrownCrystal_C`: (190,230,255), Brightness 1.5, Range 12, Shadows off | Done |
| 4 | `chevron_1..4`: 0.6x0.12x1.4 SNOW Universal, y 0.266-0.386, on the navy strips. (x, z) = (-2.594, -3.0), (0, -1.2), (2.594, 0.6), (0, 2.4) | Done |
| 5 | CLEAR ICE at T 0.22 | Done |
| 6 | 88 parts | Done |

## Numbered items

1. **NICE: `ArchPlinth_L/_R` overhang the console bar ends by 0.11.**
   - The plinths span |x| 5.64-7.24, but the front console bar ends at |x| 7.13. That leaves a 0.11 navy lip on the
     outer end of each plinth. Every other joint in the gate is flush.
   - It is hard to see, because it is navy on navy (`R8_plinth_corner`), but it is the one misaligned brick in the
     build.
   - Fix: plinth `Size.X` 1.4935, centre x ±6.3868 (x 5.64-7.1335). The inner face stays flush with the end of
     `ConsoleSnow` (5.64), and the pillars (5.84-7.04) still sit inside the plinth.

2. **NICE: the long icicles leave a 0.14 sliver to the corner braces.**
   - `Icicle_L1/_R1` cover |x| 3.40-4.10 at the beam. The top inner edge of `ArchCorner_L/_R` is at |x| 4.24.
   - Straight-on from the plaza (`R8_front_icicles`, `R8_eye`), each long icicle reads as a pale tail of the brace,
     with a thin random slot between them.
   - Fix (pick one):
     - Butt them flush: centre x ±3.89, so x 3.54-4.24. The vertical edge then continues the brace's inner tip.
     - Clearly separate them: centre x ±3.60, so x 3.25-3.95, still outside the screen frame's 3.24.
   - Keep y 8.10-9.90.

3. **NICE: line up the beam runes with the crown crystals.**
   - `rune_6` / `rune_8` sit at x ±3.6, but `CrownCrystal_L1/_R1` stand at x ±3.0 (tips at ±3.125). The 0.6 offset is
     visible in every front shot (`R8_front_icicles`, `R8_hub34`).
   - The centre (rune_7 under `CrownCrystal_C`) and the pillars (rune_5/9 under the ±6.2 pinnacles) already line up.
   - Fix: move `rune_6` / `rune_8` to x ±3.0 (y 10.5, z0 unchanged). The beam then has 5 clean light-and-crystal
     columns.
   - Checks: the gap to the short icicles (|x| 1.5-2.1) stays 0.6, and the chase spacing stays even (3.9 / 3.0 / 3.0).

4. **NICE: make the Glass read solid from close range and against the sky (keep Glass, one look for all 7 parts).**
   - **Pillar blocks:** `ArchPillarIce_L/_R` at T 0.30 show sky and the neighbouring bays straight through the pillar
     from the console side (`R8_close`, `R8_plinth_corner`, `R8_front_icicles`). The gate's legs look interrupted.
   - **Crown:** the 5 crown crystals are the weakest element at 48-60 studs. Pale glass on a pale sky leaves only faint
     nubs (`R8_lineup`, `R8_bays7to9_front_eye40`).
   - Fix: all 7 Glass parts to T 0.15-0.18. Optionally tint them one step deeper, e.g. (170, 216, 248), for contrast
     against the sky.
   - Do not switch only some of them to Plastic: the review said "don't mix the two looks".

5. **NICE: give the hub side of the screen some frost.**
   - From the plaza, the largest thing inside the gate is the blank white studded back of the screen frame plus its
     white bracket (`R8_hub34`, `R8_eye`, `R8_bays7to9_front_eye40`). Galaxy fills the same spot with a starfield.
   - Fix: keep the frame SNOW, so the runner keeps the crisp white label border. Recolour only the chassis bracket
     (2.16x2.85x0.99, tilted) to ICE (168,214,244) / Weld, or GLACIER / Weld.
   - That is colour and variant only. The size and tilt don't change, so the label detector is unaffected.

6. **NICE: the idle look of the ice skids.**
   - When nobody runs, `chevron_1..4` sit frozen as 4 stray opaque-white tiles in a diagonal (`R8_exit_rear_low`,
     `R8_sideHi`, `R8_runner`).
   - While running, each one pops from z 3.4 back to -3.8 about once a second, in clear view of the runner camera.
   - Fix: CLEAR ICE (196,232,255), T 0.2, Plastic/Universal. Review change 4 allows this. The skids then read as ice
     inlays at idle, they separate from the white belt strips, and the wrap pop is softer. Keep the size and positions.

### Note for the orchestrator (not a builder item)
`TreadmillClient` moves `chevron_` parts at most 7.5 studs/s: `min(speed, 30) * 0.25`. The Conveyor's arrow Texture
on the same belt scrolls at `9 * (1 + 0.15 * (Tier - 1))`, which is 18.45 studs/s at tier 8. While running, the skids
will visibly lag the printed arrows by about 2.5x. x20's sliding diamond tiles have the same issue. If that bothers
the owner, it is a client tweak, not a model fix.

## What is good (keep it)
- **Theme:**
  - Navy (24,40,82) + snow (238,247,255) + clear ice + Glass reads as ice and snow instantly. It has nothing in common
    with T1's opaque toy cyan/blue (`R8_bay1_hub34_compare` vs `R8_hub34`).
  - GLACIER (120,185,240) is used sparingly and is not cyan.
- **Silhouette and ladder:**
  - A full snow-capped gate on the console is a clear step up from x12, which has no gate (`R8_lineup`, `R8_far45_negX`,
    `R8_bays7to9_front_eye40`).
  - It sits clearly below x16's filled purple monolith and planet: crown 12.8 vs planet 14.4, 27 vs 38 animated parts.
  - The `ArchSnowCap` overhang draws a crisp white line that reads at 50-60 studs.
- **Runner view** (`R8_runner`, `R8_runner_zoomout_high`, `R8_icicles_back_low`):
  - The gate frames the label perfectly.
  - "+700K / sec" is crisp on the deep-navy face (luminance 0.15) inside a white border.
  - No light lifts the face (R3 OK), and no icicle crosses the label, even from a zoomed-out camera.
  - The crown reads as real crystal spikes from here.
- **Craft:**
  - Flush, logical joints:
    - pillar inner faces on the handles (5.84);
    - the beam on the pillar tops, and the cap 0.2 proud all round;
    - crystals sunk into the cap;
    - posts on the snow layer and the rail on the posts;
    - the rail butting into the grip's back face (-5.27);
    - `ConsoleSnow` against the console posts, and `GemFrost` on the bar face.
  - Inlays and bands are 0.05-0.1 proud: no coplanar overlapping faces anywhere.
  - Symmetric pairs are true mirrors, including the CornerWedge icicles (checked in `R8_front_icicles`). The foot
    crystals correctly follow the chassis's slightly asymmetric feet.
- **The CornerWedge icicles** (the builder's change) read as pointed ice from the plaza, the runner and the side,
  rather than as sails. Good call.
- **Clear-ice handrails** at grip height with GLACIER clamp bands, navy posts and the end sparkles look great from
  `R8_rear34` / `R8_exit_rear_low`. They are a visible step up from x12's low rails.
- **Hooks:**
  - The 13-rune chase is numbered as one clean loop: left rail back→front, up, across, down, right rail front→back.
    The step spacing is even, 3.0-5.0.
  - Sparkles at 110 % stay inside every box: peak 12.83, rail sparkles 4.42 (< 4.5), foot sparkles |x| 7.14.
  - The skids stay under the Zone (top 0.386) over the whole wrap range.
- **Clearances:**
  - The exit walkway is empty (`R8_exit_rear_low`).
  - Nothing is at |x| > 6.4 in z 4-8.6, so both upgrade signs are unobstructed (`R8_rear34`).
  - Max |x| is 7.30, at the cap only (lamp from 7.7).
  - The over-head box and the runner corridor are empty.
- **Budgets:** 88 / 88 parts, 7 accent parts (8 %), 3 lights with Shadows off. No banned classes or materials.
