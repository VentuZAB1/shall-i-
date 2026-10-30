# Tier10_x18 INFERNO: build notes (Phase B, 2026-10-12)

**Template:** `ServerStorage.Assets.Treadmills.Tier10_x18` (`Theme = "Inferno"`, other attributes unchanged), refreshed
into `Bay10`.

Built from PLAN.md plus the x18 section of PLAN_REVIEW.md. Everything is Plastic + MaterialVariant, except 2 Metal
exhaust pipes.

## Final validator (`T.validate(10)`)
```
== Tier10 Inferno: 0 FAIL, 0 WARN
ok   label screen = Part 6.1x3.1 colour (30,22,24) lum 0.09, 3 tilted parts
ok   106 visible parts (80 decor), 2 accent-material parts, 3 lights; animation hooks: flame_ x14, wing_R x4, belt_cracks x1, wing_L x4, wing_root_L x1, hood_emblem x1, skull_eyes x1, wing_root_R x1, screen_gem x1, sparkle_ x4, rune_ x10
```

## Ladder numbers (measured on the refreshed bay)
| | Built | Review target |
|---|---|---|
| Solid top (crater rim) | **13.40** | 13.4 |
| Static peak (`flame_core_C` tip) | **14.90** | <= 14.9 |
| Anim max (core x1.46) | **15.64** | <= 15.7 |
| Visible parts | **106** | 100-106 |
| Animated parts | **40** | ~40 |

The 40 animated parts are:
- 14 `flame_`;
- 10 `rune_`;
- 4 `sparkle_`;
- 8 fin parts;
- 4 pulse parts.

**R2 check at the extremes:** flames x1.46, sparkles 110 %, fins ±0.28 rad (34 poses checked).
- Nothing goes past |x| 7.00 or y 15.64.
- Nothing enters the Zone, the corridor, the head box, the sign keep-outs or the exit walkway.
- Fins:
  - The inner edge at full inward flex is at x 3.73 (review: keep >= 3.6).
  - The fin's back face is at z 1.40 (review: <= 1.4).
- Only intended contacts remain:
  - sparkles half-seated in their surfaces;
  - each flame core nested in its tongue;
  - flame bases sunk 0.1;
  - the centre and side crown tongues touch (0.05) so the crown reads as one fire.

**Chase and flicker order (from the refreshed bay):**
- Runes: 1 L z-4.3, 2 R -4.3, 3 L -1.7, 4 R, 5 L 0.9, 6 R, 7 L 3.5, 8 R, 9 L 6.1, 10 R 6.1. That is front to back on
  both rails, alternating sides.
- Flames alternate tongue then core, so neighbours flicker on different phases.

## What was built
**Palette:**
- BASALT (30,22,24)
- CRIMSON (196,20,40)
- LAVA (255,100,0)
- MAGMA (255,184,28)

**Chassis:** recoloured exactly as in PLAN.md section 3. The label face is BASALT/Universal at lum 0.09.

**Decor sub-models:**
- **Console** (6 parts):
  - `ConsoleBase` (basalt plinth);
  - `ConsoleStep` and `ConsoleSlope_L/_R` (crimson volcano trapezoid);
  - `belt_cracks` (lava seam across the front);
  - `hood_emblem` (magma diamond, 1.6).
- **Gate** (22 parts):
  - `GatePillar_L/_R` (basalt, floor to 7.8);
  - `PillarCap_L/_R` and `ArchCorbel_L/_R` (crimson, a pointed opening);
  - `LavaVeinLow/High_L/_R` (zig-zag cracks);
  - `sparkle_vein_L/_R` and `sparkle_lintel_L/_R`;
  - `Lintel` (14.27 wide);
  - `screen_gem` (on the runner-facing side of the lintel, above the label);
  - `Brazier_L/_R`, `flame_torch_L/_R` and `flame_torchcore_L/_R`.
- **Peak** (13 parts), as specified by the review:
  - `VolcanoTier1` (y 10.4-11.6) with `VolcanoSlope1_L/_R` (x ±3.8..5.2);
  - `VolcanoTier2` (11.6-12.8) with `VolcanoSlope2_L/_R` (x ±2.4..3.8);
  - `CraterRim` (12.8-13.4, crimson, holds `GateGlow`);
  - `flame_crown_C` (tip 14.8), `flame_core_C` (tip 14.9), `flame_crown_L/_R` (tip 14.5), `flame_core_L/_R` (tip 14.7). All bases at 13.3.
  - `skull_eyes`: see deviations.
- **Rails** (18 parts): 6 `RailPost`, 2 crimson `RailBeam`, and `rune_1..10` on the outer faces.
- **Fins** (10 parts):
  - `wing_root_L/_R` sockets (pivots);
  - per side, 4 parts all named exactly `wing_L` / `wing_R`: a crimson leading wedge, a crimson body, an orange tip
    wedge, and a basalt spar (back face z 1.4).
- **Spoiler** (10 parts):
  - `SpoilerPlate_L/_R` (crimson, x 5.71-6.31);
  - `SpoilerWing_L/_R` (split ducktail, see deviations);
  - `flame_spoiler_L/_R`;
  - `ExhaustPipe_L/_R` (Metal cylinders, floor level);
  - `flame_exhaust_L/_R` (grow backward, max z 8.99).

**Lights (Shadows off):**
| Light | Parent | Settings | Note |
|---|---|---|---|
| `GateGlow` | CraterRim | (255,120,30), Brightness 2, Range 16 | |
| `VolcanoGlow` | ConsoleStep | (255,90,20), Brightness 1.5, Range 12 | |
| `SpoilerGlow` | SpoilerWing_L | (255,90,20), Brightness 1.5, Range 10 | |

R3: in `runner` the label face stays black, and nothing lifts it, so no dimming was needed.

## Deviations from the plan / review (please confirm or veto)
1. **`skull_eyes` moved instead of dropped or put on the floor.**
   - It is now the **lava flow** down the volcano front: 0.6 x 3.6 x 0.2, LAVA, from the crater (12.8) down the lintel
     to 9.2, at z -11.435.
   - It pulses white-hot while running, so the plaza sees the "eruption".
   - It is nowhere near the walkway. If you'd rather not have it, renaming it `LavaFlow` costs nothing.
2. **EmblemPlate dropped**, to keep 106 parts with the volcano slopes 2. The magma badge reads fine on crimson.
3. **Volcano slope wedges are LAVA** (the tiers are BASALT). The all-dark cone read as a pagoda roof in `lineup_v1`. The
   orange flanks read as lava running down the cone (`hub34_v2`, `lineup_v2`).
4. **The spoiler halves are ducktail wedges**, not 0.5 blocks.
   - Size and place: `SpoilerWing_L/_R` is a WedgePart 1.6 x 1.325 x 2.25 at x ±(4.11..5.71), y 3.075-4.4, z 7.0-9.25,
     LAVA.
   - It rises out of the rail end toward the back.
   - The small basalt blocks didn't read at all in `rear34_v1`.
   - It is still outside the walkway (x >= 4.11) and under the corridor (top 4.4).
5. **Crown widths:** `flame_crown_C` is 1.2 wide (planned 1.1). The side tongues are 0.85 at x ±1.4 (planned 0.8 at
   ±1.3) so the crown reads at plaza distance. The heights are exactly the review's.
6. **Torch flame bases** are sunk 0.1 into the braziers, like the crown.
7. **Console part names:** they are `ConsoleBase/Step/Slope` (the plan said "Volcano...") to avoid confusion with the
   `VolcanoTier` peak.

## Captures (all taken under `T.lock("T10")`, one at a time)
| Round | What changed | Capture ids |
|---|---|---|
| v1 | first build | `T10_hub34_v1`, `T10_spawn_v1`, `T10_runner_v1`, `T10_side_v1`, `T10_sideHi_v1`, `T10_rear34_v1`, `T10_lineup_v1`, `T10_eye_v1`, `T10_close_v1` |
| v2 | lava flanks, wider crown, ducktail wedges (first try) | `T10_lineup_v2`, `T10_hub34_v2`, `T10_rear34_v2` |
| **v3 (final state)** | | `T10_rear34_v3`, `T10_sideHi_v2`, `T10_spawn_v2`, `T10_runner_v3`, `T10_side_v3`, `T10_hub34_v3`, `T10_eye_v3`, `T10_close_v3`, `T10_lineup_v3` |

## Unsure / for the reviewer
- **Camera changed between rounds.**
  - From the v3 round on, the Studio camera looked wider-angle than in v1, so it was probably changed outside this
    session.
  - `T10_lineup_v3` also shows a flat dark-green band across the bottom. That is a viewport artefact, not the model.
  - The geometry is identical, so compare shapes, not framing.
- **Crimson (196,20,40) reads as a bright hot red in sunlight.** It's clearly not T5's dark (151,0,0), but if the
  reviewer wants a deeper crimson, (176,16,34) is a one-line change.
- **Static flames look like bricks.** They are block tongues with the Inlet texture, and the flicker is what sells
  them as fire. It can't be seen in still captures.
- **The near ducktail is hidden from some rear angles.** In `rear34`, the right ducktail sits behind its end plate;
  the left one reads.

---

## Phase C: fixes from REVIEW.md (2026-10-12)
**Verdict received:** FIX with 1 MUST.
- Deviations 1, 2, 3, 4, 6 and 7 are approved.
- Deviation 5 (wider crown) is vetoed.
- Crimson (196,20,40) is kept.

All the changes below only resize or recolour existing parts. No parts were added. Every flame keeps its 45-degree turn
about Y and its original base height.

### MUST 1: tapered two-tone flames
| Part | Size | Centre | Tip |
|---|---|---|---|
| `flame_crown_C` | 0.9 x 1.1 x 0.9 | (0, 13.85) | 14.40 |
| `flame_core_C` | 0.5 x 1.6 x 0.5 (unchanged) | | 14.90 |
| `flame_crown_L/_R` | 0.7 x 0.8 x 0.7 | x +-1.4, y 13.7 | 14.10 |
| `flame_core_L/_R` | 0.35 x 1.3 x 0.35 | x +-1.4, y 13.95 | 14.60 |
| `flame_torch_L/_R` | 0.7 x 0.8 x 0.7 | y 11.2 | 11.60 |
| `flame_torchcore_L/_R` | 0.35 x 1.3 x 0.35 | y 11.45 | 12.10 |

Measured on the refreshed bay:
- Every flame shows 0.50 of yellow tip.
- The gap between the centre and side tongues is 0.27, so no tongues touch.
- The side tongues' outer corners are at x 1.895, inside the crater rim (2.0).
- The centre is the tallest point.

### NICE fixes, all done
2. **Lava flow:** `skull_eyes` (the lava flow) widened to 1.0 x 3.6 x 0.2 (x +-0.5), same y and z.
3. **Console slopes:** `ConsoleSlope_L/_R` recoloured to LAVA (255,100,0) / Inlet. `ConsoleStep` stays CRIMSON.
4. **Screen bracket:** the chassis bracket (2.16 x 2.85, 20 deg) is now BASALT / Studs instead of LAVA / Weld.
5. **Exhaust flames:** `flame_exhaust_L/_R` are now 0.5 x 0.6 x 0.5 (local Y points to +Z), base kept at z 8.36. The running tip is at z 9.236, inside the 9.3 limit.
6. **Screen gem:** `screen_gem` shrunk to 0.85. The diamond now spans y 9.199-10.401, so it sits within the lintel (9.2-10.4) instead of poking out.
7. **Runes (optional, done):**
   - All 10 runes were moved up so their tops sit 0.06 above the beam top: centre y 2.955, range 2.775-3.135. They stay on the beams' outer faces, uniform along both rails, so the plaza view is unchanged.
   - Segment test from the runner camera (0, 9, 12.5):
     - runes 7 and 8 (z 3.5) are now VISIBLE to the owner;
     - runes 1-6 stay hidden behind the fin sockets;
     - runes 9-10 are hidden behind the ducktails.
   - So the owner now sees the chase pass at the rear sides.

### Phase C validator and numbers
```
== Tier10 Inferno: 0 FAIL, 0 WARN
ok   label screen = Part 6.1x3.1 colour (30,22,24) lum 0.09, 3 tilted parts
ok   106 visible parts (80 decor), 2 accent-material parts, 3 lights; animation hooks: flame_ x14, wing_R x4, belt_cracks x1, wing_L x4, wing_root_L x1, hood_emblem x1, skull_eyes x1, wing_root_R x1, screen_gem x1, sparkle_ x4, rune_ x10
```

| Measure | Value |
|---|---|
| Solid top | **13.40** |
| Static peak | **14.90** |
| Anim max | **15.64** |
| Anim max z | 9.236 |
| Max \|x\| | 6.93 |
| Visible parts | 106 |
| Animated parts | 40 |
| Lights | 3 |

The R2 extremes were re-checked (flames x1.46, sparkles 110 %, fins +-0.28 rad). Nothing enters the Zone, the
corridor, the head box, the sign keep-outs or the exit walkway.

### Phase C captures
Taken with `T.lock("T10")` called again before every capture, one at a time, then unlocked. The Studio FOV was 70.

| What | Capture ids |
|---|---|
| Requested set | `T10C_peak_close` (crown and torches), `T10C_runner`, `T10C_lineup`, `T10C_far_front` (about 50 studs in front, eye-ish height), `T10C_spawn`, `T10C_hub34`, `T10C_eye`, `T10C_close` |
| Extra | `T10C_rear_eye` (exhausts, ducktails, belt from the base side) |

### Notes
- **Flames and bracket.**
  - In `T10C_peak_close` and `T10C_runner` the crown now reads as three separate tapered flames, centre tallest, each
    with a yellow tip, rather than a battlement.
  - From the front, the dark bracket now reads as a calm dark panel on the crimson screen back. In `runner`, nothing
    orange sits under the label any more.
- **Exhaust flames.** They are bigger, but at floor level they are still plain yellow (MAGMA) blocks in
  `T10C_rear_eye`. If the reviewer wants them to read more as flame, recolouring them LAVA is a one-line option. I
  didn't make that change.
- **Lineup band.** The flat green band at the bottom of the `lineup` / far-front frames is the same viewport artefact
  as in Phase B. It is not part of the model.
