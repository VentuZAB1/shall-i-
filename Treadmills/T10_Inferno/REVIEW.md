# Tier10_x18 INFERNO: visual review (Phase C, 2026-10-12)

Reviewer: independent visual reviewer. This was a read-only pass: I edited nothing in the game.
- Read: the brief, PLAN_REVIEW.md, PLAN.md, BUILD_NOTES.md and `TreadmillClient` (flame, wing, pulse and rune code).
- Dumped every template part in belt space and ran an AABB overlap / coplanar-face sweep (decor + chassis).
- Checked the R2 extremes by maths, and ran a runner-camera visibility test on every hook.
- `T.validate(10)`: **0 FAIL, 0 WARN**; 106 visible parts (80 decor), 2 accent parts, 3 lights.

Captures (camera lock `Rev10`, one at a time):

| Capture | Camera |
|---|---|
| `Rev10_hub34`, `Rev10_spawn`, `Rev10_eye`, `Rev10_close`, `Rev10_runner`, `Rev10_side`, `Rev10_sideHi`, `Rev10_rear34`, `Rev10_lineup` | the presets |
| `Rev10_peak_close` | crown and torches, close |
| `Rev10_far45L`, `Rev10_far45R` | about 50 studs at ±45° |
| `Rev10_bays9to11_rearHi` | ladder, x12 to x20 |
| `Rev10_rear_eye` | base side, eye height |
| `Rev10_rear_corner_low` | spoiler and exhausts |
| `Rev10_bay5_hub34` | T5 for comparison |

## VERDICT: **FIX**
There is one MUST. Everything else is NICE.

The build is strong and on spec:
- every plan-review change is done;
- the ladder numbers hit the targets exactly;
- the craft is clean.

The one thing standing between this and "on point" is the flame shape. x18's signature motif, the crown and the torches, still reads as orange crates.

---

## MUST

**1. Re-proportion the crown and torch flames into tapered two-tone flames.** This vetoes deviation 5.
- **The problem:**
  - `Rev10_peak_close`, `Rev10_runner`, `Rev10_hub34`: the crown is three touching orange cubes of almost the same height (tips 14.5 / 14.8 / 14.5). It reads as a castle battlement.
  - The magma cores poke out only 0.1 (C) and 0.2 (sides), so the yellow barely shows. The torches have the same problem.
  - Flicker only scales the height (×0.54 to ×1.46), so in game this becomes "bouncing crates", not fire.
- **The fix** (sizes and positions only, part-neutral; every flame stays rotated 45° about Y with its base at the same height):

| Part | Size | Centre y | Tip |
|---|---|---|---|
| `flame_crown_C` | 0.9 × 1.1 × 0.9 | 13.85 | 14.4 |
| `flame_core_C` | 0.5 × 1.6 × 0.5 (unchanged) | 14.1 (unchanged) | 14.9 |
| `flame_crown_L/_R` | 0.7 × 0.8 × 0.7, at x ±1.4 | 13.7 | 14.1 |
| `flame_core_L/_R` | 0.35 × 1.3 × 0.35, at x ±1.4 | 13.95 | 14.6 |
| `flame_torch_L/_R` | 0.7 × 0.8 × 0.7 | 11.2 | 11.6 |
| `flame_torchcore_L/_R` | 0.35 × 1.3 × 0.35 | 11.45 | 12.1 |

- **What this gives:**
  - Every flame shows an orange body with a yellow tip about 0.5 tall on top.
  - The crown peaks in the centre (14.9 against 14.6).
  - There is a 0.27 gap between the tongues, so they read as three separate fires.
  - The centre tongue no longer overhangs the crater rim's front face (today it is 0.05 out).
- **Ladder unchanged:** solid top 13.4, static peak 14.9 (`flame_core_C`), anim max 15.64.
  - New running tops: tongue C 14.91, side cores 15.20, torch cores 12.70.
  - All of them stay under 16 and inside |x| 7.4. The side tongues' outer corners are at x ±1.895, inside the rim (±2.0). The torches stay inside the brazier footprint.
- You may tune ±0.1, but keep three rules:
  - the centre is clearly the tallest;
  - at least 0.4 of yellow tip shows on every flame;
  - no two tongues touch.
- **Proof:** recapture a close view of the peak, `runner` and `lineup`.

## NICE (recommended; all part-neutral)

**2. Make the lava flow (`skull_eyes`) wider: 0.6 → 1.0 wide** (x ±0.5), same 3.6 height and the same z.
- It is the only thing that says "volcano erupting" on the plaza face.
- At 0.6 it disappears at 50-60 studs (`Rev10_lineup`, `Rev10_far45L/R`). From those views the peak reads closer to a stepped temple roof.

**3. Recolour `ConsoleSlope_L/_R` to LAVA (255,100,0) Plastic/Inlet.**
- They would echo the peak's lava flanks, so "lava runs down the sides" becomes one motif, top and bottom.
- They also break up the biggest flat red area on the plaza face: the crimson step plus the crimson screen back behind it (`Rev10_lineup`, `Rev10_eye`). That area is the most T5-like spot on the model.
- Keep `ConsoleStep` CRIMSON so the magma badge keeps its contrast.

**4. Change the chassis screen bracket from LAVA/Weld to BASALT/Studs** (or CRIMSON/Studs).
- From the front, the Weld "X" reads as an orange crate floating in the middle of the gate opening (`Rev10_eye`, `Rev10_close`, `Rev10_lineup`).
- From `runner` it is an orange tab right under the label.
- Dark makes both views calmer.

**5. Make the exhaust flames bigger: `flame_exhaust_L/_R` 0.4³ → 0.5 × 0.6 × 0.5**, with the same base at z 8.36.
- The running tip is then at z 9.24, inside the 9.3 envelope.
- Today they read as stray yellow dice on the floor (`Rev10_rear_eye`, `Rev10_rear_corner_low`).

**6. Shrink `screen_gem` 1.0 → 0.85** (diagonal 1.2, which equals the lintel height).
- Today its 45° diamond is 1.41 tall, so it pokes 0.107 above and below the lintel.
- The bottom corner shows as a stray nub under the lintel centre from the plaza (`Rev10_close`).

**7. The owner never sees the ember chase.**
- A segment test from the runner camera (0, 9, 12.5) shows 0 of 10 runes visible. They sit on the beams' outer faces, and the beam and fin socket hide them.
- The owner does see the fins, the 6 crown flames, the torches and `screen_gem`, so the runner view has life. The chase is plaza-only.
- This is acceptable as it is. If the owner should see it, a part-neutral option is to make runes 7-10 stand 0.05 above the beam top. Only the ones behind the fin socket (z > 1.4) can be seen from the camera.
- Your call. Don't move all 10 to the inner faces: that blinds the plaza side.

---

## The 7 deviations
| # | Deviation | Verdict | Why |
|---|---|---|---|
| 1 | `skull_eyes` kept as a pulsing lava flow down the volcano front (0.6 × 3.6, y 9.2-12.8, z -11.435) | **APPROVED** | It sits on the plaza face, nowhere near the R1 walkway. It is the single `skull_eyes` part the client pulses, and it sells the eruption. Widen it (NICE 2). |
| 2 | `EmblemPlate` dropped | **APPROVED** | The 1.6 magma diamond reads cleanly on crimson in `Rev10_eye`, `close` and `lineup`. |
| 3 | Lava-orange volcano slope wedges | **APPROVED** | The flanks are what makes the peak read hot at plaza distance, and the cone line runs straight from (5.2, 10.4) to (2.4, 12.8). NICE 2 and 3 push the volcano read further. |
| 4 | Spoiler halves as lava ducktail wedges (x ±4.11..5.71, y 3.075-4.4, z 7.0-9.25) | **APPROVED** | Outside the R1 walkway (x ≥ 4.11), under the corridor (top 4.4), and inside the sign keep-out (≤ 6.31). Flush against the plate inner faces, and it reads in `Rev10_rear_eye`. The near one hiding behind its plate in `rear34` is fine. |
| 5 | Slightly wider crown flames (C 1.2, sides 0.85 at ±1.4) | **VETOED** | Wider made them more cube-like and made the tongues touch. Replaced by MUST 1. |
| 6 | Torch flames sunk 0.1 into the braziers | **APPROVED** | Same as the crown: no floating bases, and the flicker grows from a seated base. |
| 7 | Console part names `ConsoleBase/Step/Slope_L/_R` | **APPROVED** | Clearer next to `VolcanoTier/Slope`. None of them are hook names. |

**Crimson: keep (196,20,40). Do NOT deepen it to (176,16,34).**
- T5 uses (151,0,0) and (181,0,0). The deeper value lands between them, which moves Inferno toward T5.
- It would also darken a model that is already the darkest one in the lineup (basalt is about 40 %).
- In `Rev10_bay5_hub34` vs `Rev10_hub34`, the brighter, slightly blue crimson next to the lava orange is part of what separates Inferno from T5.

---

## Checks that passed
**Ladder.** The bays measure exactly on target:

| Tier | Solid top | Static peak | Anim max | Visible parts | Animated parts |
|---|---|---|---|---|---|
| x16 Galaxy | 12.70 | 14.40 | | 89 | 38 |
| **x18 Inferno** | **13.40** | **14.90** | **15.64** | **106** | **40** |
| x20 Diamond | 14.55 | 15.75 (halo) | | 106 | 39 |

- `Rev10_lineup`, `Rev10_bays9to11_rearHi` and `Rev10_far45L/R` show a clear step over x16 and a clear step under x20.
- **Coordination note (not x18's fix):** x20 has 39 animated parts against x18's 40. PLAN_REVIEW requires x20 ≥ x18. All my changes here are part-neutral.

**Plan-review changes, all 5 done:**
- the volcano peak to the exact spec, with slope pair 2 included;
- the split spoiler, with `SpoilerGlow` in `SpoilerWing_L`;
- the fins: exact `wing_root_L/_R` and 4× `wing_L/_R`, back face at z 1.40, inner corner at full flex x 3.73 / y 8.03 (≥ 3.6 OK);
- the rune order: L/R pairs front to back;
- 106 parts.

**R2 extremes, by maths:**
- Flames ×1.46 peak at 15.64. The spoiler stacks reach 6.05 at |x| 5.66-6.36, which is under the 6.4 sign limit.
- Sparkles at 110 % reach z -11.66 at the front, inside -11.8.
- Fins at ±0.28 rad reach outer x 6.87 / inner x 3.73. They never move in z.
- The fin base dips only 0.06 into its own socket, and nothing else touches the fins.

**Craft:**
- Every part is Plastic with Studs, Inlet, Weld or Universal; the 2 Metal exhausts are the only accents.
- Fully mirrored.
- The overlap/coplanar sweep found no decor z-fighting.
  - The only decor overlaps are intended: flame bases 0.1, cores inside tongues, sparkles half-seated, the exhaust flames 0.05 in their pipes.
  - Two contacts are sub-0.005 and invisible: the console plinth against the console bar, and `ConsoleStep` against the upper bar.

**Clearances:**
- R1 walkway (|x| ≤ 4.1, z ≥ 7, y 0.3-6.6): empty. The exhaust tops are at 0.13.
- Runner corridor and head box: empty, including at full fin flex.
- Envelope: x ±7.135, z -11.66..9.25.
- The upgrade sign is fully clear and readable in `Rev10_rear34`, and the lamp zone is clear.

**Label.** In `Rev10_runner` the BASALT face (lum 0.09) with the crimson bezel shows "+900K / sec" crisp, and no light lifts it. `GateGlow` hits the face only at a grazing angle.
- If the live hub runs at night, re-check `runner` once in game; drop `GateGlow` to Brightness 1.5 if the face greys.

## What is good: keep it
- **The molten-river belt** (MAGMA centre → LAVA → CRIMSON → BASALT Inlet). `Rev10_runner` and `Rev10_rear_eye` are the best owner and base-side views of the whole x12-x20 set.
- **The gate:**
  - basalt pillars with the zig-zag lava veins and ember glints;
  - crimson corbels giving the pointed opening;
  - the full-width `belt_cracks` seam tying the pillars and plinth into one dark band;
  - the volcano-trapezoid console with the magma badge.
- **The swept fins:**
  - one continuous leading edge from (z -5.28, y 3.475) to (z 1.0, y 8.275);
  - the crimson → orange split and the dark spar;
  - the fin grows out of the handle grip.
  - They frame the runner view like a cockpit and never touch the label sight-lines (a flexed tip projects to x ≈ 7.2 at the label plane).
- **The stepped peak:** the straight cone line, the crimson crater, and the lava flanks. The silhouette is unlike x14's or x16's beams and x20's round arch.
- **The spoiler end plates with stacks and the split ducktail:** the walkway problem is solved without losing the rear read.
- **The palette discipline:** the orange always sits on basalt or crimson, so it never reads as T2's peach and never as T5's plain red.

## Process note
I let the camera lock lapse once: `Rev10_rear_corner_low` was taken while `Rev11` held the lock. My image shows bay 10 correctly. Any `Rev11` capture taken around that moment (just after my `Rev10_far45R`) should be checked for a swapped view.
