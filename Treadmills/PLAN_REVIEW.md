# PLAN REVIEW: treadmills x12-x20 (2026-10-12)

Reviewer: independent plan reviewer. I read the brief, the five PLAN.md files, `TreadmillClient` and `_TreadLabTools`
(validator), measured the Tier6 chassis in belt space, and took captures `PR_T6_runner` and `PR_lineup_bays3to8`
(camera lock `PlanReview`). Nothing in the game was edited.

## Verdicts
| Tier | Verdict | Required changes |
|---|---|---|
| x12 Emerald | **APPROVED** | none (notes only) |
| x14 Frost | **APPROVED WITH CHANGES** | 6 |
| x16 Galaxy | **APPROVED WITH CHANGES** | 3 |
| x18 Inferno | **APPROVED WITH CHANGES** | 5 |
| x20 Diamond Rainbow | **APPROVED WITH CHANGES** | 7 |

All five plans are careful and rule-aware. The changes fix six things:
- the height ladder;
- one copied motif (two floating spinning diamonds);
- a dimming problem on the x20 arch;
- a walk-through problem behind the belt (x18, x20);
- x20 falling behind x18 in the side view and in part count;
- a few tight clearances.

---

## 0. Facts every builder must use (from the code, not the brief)
- **Runes:** the client now SORTS `rune_<n>` by number. **Numbering = chase order**; creation order no longer matters.
  The x12/x14/x16 "GetDescendants order" risk is gone.
  - 6 steps/s. Only while running: one rune is white, the others go 45 % toward BLACK.
- **Wings:**
  - Every part named exactly `wing_L` / `wing_R` turns rigidly about `wing_root_L` / `_R`. The roots never move.
  - The flap direction comes from the sign of each part's own X.
  - Amplitude ±0.06 rad idle and ±0.28 rad running (≈ ±16°), about 1.4 Hz while running. Both sides lean in and out
    together.
  - The names must be EXACT: `FinSocket` is not a root.
- **Halo:**
  - Spins about the belt vertical: 0.4 rad/s idle, 2.15 rad/s running. Floats ±0.18.
  - The spin never changes its rx.
- **Flames:** grow up their local Y from the bottom. Peak ×1.26 idle and **×1.46 running**.
- **Sparkles:** 55-110 % about their centre.
- **Orb:**
  - `orb_core` floats ±0.15 and pulses to ×1.12 while running.
  - The ring and shards turn about the vertical through the core.
- **Chevrons:** move only while running. Their centres wrap in z -3.8 → 3.4.
- **Screen detector:**
  - Tilted means |rx| between 14.3° and 25.7° at z < -6.
  - A wedge turned 90° about Y and then swept θ in its own plane gets **rx = θ**. A 15° sweep counts as tilted
    (harmless if it's tiny, see x20). 90° and 180° turns give rx = 0.
- **Exit spot:**
  - On Jump the owner is put at belt (0, ·, **+7.5**), FACING +Z (toward their base).
  - They then walk to the base through z 7-14. Other players cross here too.
- **Upgrade sign:** it faces **+Z** (the base side), at belt x -10.4 / +8.7, z ≈ +6.2, top y ≈ 2.8.
- **Lab captures:** the `side` preset now sits in the gap between bays, and `sideHi` exists. Use these, not custom
  side cameras.

### New rules from this review (they apply to all tiers)
- **R1 Rear walkway:**
  - Keep |x| ≤ 4.1, z ≥ 7.0, 0.3 ≤ y ≤ 6.6 EMPTY.
  - Floor pieces with a top ≤ 0.3 are fine.
  - Reason: anything at chest or neck height there is walked through every time the owner gets off.
- **R2 Animated extremes:** check every hook at its extreme: flap 0.28 rad, bob, pulse ×1.12, flicker ×1.46, twinkle
  110 %. At the extreme, nothing may:
  - go past y 16 or |x| 7.4;
  - enter the Zone, the over-head box or the runner corridor;
  - poke into another part.
- **R3 Label in `runner` with the lights on:** if a light visibly lifts the screen face, lower it (Brightness ≤ 1.0).

---

## 1. The agreed ladder
How to read the height columns:
- **Solid top** = the highest static part that is attached to the build. Floating parts, flames and sparkles don't
  count.
- **Static peak** = the highest point at rest, including floating parts, sparkles and flames.
- **Anim max** = the highest point any moving part can reach. Hard cap 16.

| Tier | Concept | Solid top | Static peak | Anim max | Visible parts | Motion (animated parts) |
|---|---|---|---|---|---|---|
| x10 (T6) | gold/black chassis | 8.5 | 8.5 | - | 26 | none |
| **x12** Emerald | jewel rails, crest on the screen | 8.5 | **10.0** | 10.1 | **64-72** (plan 68) | ~22: rail chase, 8 gem twinkles, 2 pulses (colour/size only) |
| **x14** Frost | white ice gate ON the console, glass crystal crown, icicles | **11.5** (snow cap) | **≤ 12.8** | ≤ 12.9 | **82-88** | ~27: 13-rune chase over the gate, 9 twinkles, 1 pulse, NEW sliding ice skids |
| **x16** Galaxy | violet star gate ON the console, filled by a 2nd tall screen, planet on top | **≤ 12.7** | **≤ 14.4** | ≤ 14.7 | **88-96** | ~38: gate chase, 17 star twinkles, NEW equalizer, NEW planet + precessing ring + 3 orbiting moons |
| **x18** Inferno | basalt gate on the FLOOR in front of the console, stepped volcano peak, flame crown, flexing fins | **13.4** (crater rim) | **≤ 14.9** (flame tips) | ≤ 15.7 | **100-106** | ~40: NEW 14 flickering flames, NEW flexing fins, rail chase, twinkles, 3-4 pulses |
| **x20** Diamond Rainbow | round rainbow arch on the floor, winged crown + spinning diamond, crystal pylons | **14.55** (crown points) | **15.75** (halo) | ≤ 15.95 | **104-110, ≥ x18** | ≥ x18: NEW spinning, floating diamond, NEW flapping wings, arch chase, EQ, sliding diamonds, twinkles. Most families (8) |

**The gate grows, and each tier has its own outline:**
- x14: a flat snow beam with icicles, on the console, top 11.5.
- x16: a filled monolith with a planet, on the console, top 12.7.
- x18: a deep floor gate with a stepped volcano, top 13.4.
- x20: a round arch with a crown, top 14.55.

**Signature motifs, one owner each:**
| Motif | Owner |
|---|---|
| Floating spinning diamond | x20 only |
| Planet / orb | x16 only |
| Flames and fins | x18 only |

**Shared motifs that are accepted:**
- **Sliding belt pieces:** x14 has long ice skids and x20 has diamond tiles. They are different shapes.
- **Equalizer above the label:** x16 has a big display with 5 bars and stars; x20 has a slim marquee with 7 rainbow
  bars. This is the cumulative "tall console" step.
- **Console-front diamond badge:** it's a family badge, in each tier's own colour.

---

## 2. Per tier

### x12 EMERALD: APPROVED
Clean, restrained first step: jewel palette, rails, crest, first lights, first motion. Its peak of 9.98 and its 68
parts sit right on the ladder. Build it as written.

Notes (not changes):
- **N1 Runes:** your numbering is exactly right: `rune_1..6` run up the left rail back to front, `rune_7..12` run down
  the right rail front to back. The client sorts by number, so the scrambled-chase risk is gone.
- **N2 Crest light:** `CrestLight` sits about 1.5 above the label. If `runner` shows the dark face greening up, use
  Brightness 1.0 / Range 8.
- **N3 Side view:** use the lab's `side` and `sideHi` presets. Your custom `side_hi` is no longer needed.
- **N4 Phase B tuning:** all the tuning you listed is pre-approved (Weld → Universal on the gems, crystal size ±0.1, a
  greener ONYX).

Answers:
- **Platinum or gold? Platinum.** Gold on green would read as "T6 plus green". Gold also comes back in x18's magma
  cores. Platinum keeps x12 a clean jewel step.
- **Rail height? Keep the low rails** (top 2.8, crystals to 3.7):
  - At grip height (≈ 3.8) the crystals would reach about 4.7 inside |x| ≤ 5, which puts them in the runner corridor
    (WARN).
  - The handle grips stay the visual "handles".
  - x14's grip-height ice rails then become a visible step up.

### x14 FROST: APPROVED WITH CHANGES
Keep the frost gate on the console: snow/glass pillars, navy beam with snow cap, icicles, glass crown, the frost
current running over the gate, the snow layer on the frames and the foot crystals. They are all good and clearly unlike
T1.

**1. Remove `halo` and `HaloCradle_L/_R`.**
- The floating spinning diamond over the arch centre is x20's crown jewel. From the plaza, two "arch with a diamond
  floating at top centre" tiers would read the same.
- It also puts x14's top at 14.1-14.3, above x16's planet and x18's flames.

**2. Cap the crown: static peak ≤ 12.8 including sparkles at 100 %, ≤ 12.9 at 110 %.**
- `CrownCrystal_L1/_R1`: 1.2 tall, keep the 12° lean (tip ≈ 12.37). `sparkle_crown_1/_2`: 0.4 cubes (top ≈ 12.65).
- `CrownCrystal_L2/_R2`: 1.2 tall, keep the 20° lean (tip ≈ 12.33). Their sparkles are 0.4 cubes.
- NEW `CrownCrystal_C`: 0.9 × 1.3 × 0.9, GLASS ICE, upright at x 0, base sunk 0.3 (y 11.2-12.5).
- NEW `sparkle_crown_5`: 0.45 cube, 45° about Z, centred on its tip (top ≈ 12.82). The centre is now the crown's
  tallest point.
- Recommended rhythm: move the inner pair to x ±3.0, so the crystals sit at 0, ±3.0 and ±6.2.

**3. Re-home the halo light.** `HaloLight` becomes `CrownLight` inside `CrownCrystal_C`: (190, 230, 255),
Brightness 1.5, Range 12, Shadows off.

**4. New motion to replace the halo: `chevron_1..4` "ice skids".**
- Size and finish: 0.6 × 0.12 × 1.4, long axis along Z. SNOW (opaque) or CLEAR ICE (Transparency ≤ 0.2),
  Plastic/Universal.
- Placement: lying on the NAVY belt strips (x 0 and ±2.59), bottom y 0.27 (top 0.39).
- Start z values -3.0, -1.2, 0.6, 2.4, alternating x -2.59 / 0 / +2.59 / 0.
- They slide back under the runner's feet while running. That makes x14 the first tier with sliding parts.

**5. Translucency:** icicles and ice rail bars at Transparency 0.2-0.25 (not 0.35). Pale blue at 0.35 disappears
against the sky in `runner` and `lineup`.

**6. Parts ≤ 88:** 85 - 3 + 2 + 4 = 88.

Answers (fallbacks): **all pre-approved.**
- **Glass:** try Glass first. If it reads murky or invisible in `hub34`/`lineup`, switch ALL the crown and pillar
  crystals to Plastic/Universal (196, 232, 252) at T 0.25. Don't mix the two looks.
- **Wedge icicles:** keep them if they read as points. If they look like sails, use 2-brick tapered sticks
  (0.6 × L1 on top of 0.35 × L2). Keep the same tips: the short ones end at y ≥ 9.1, the long ones stay at |x| ≥ 3.4.
- **Colours:** GLACIER (120, 185, 240) is approved, and recommended from the start, because running dims the runes
  45 %. FRAME (30, 50, 100) is approved if the navy goes black.

### x16 GALAXY: APPROVED WITH CHANGES
Keep everything else:
- the violet gate with magenta bands;
- the tall second screen: starfield on the hub side, equalizer on the runner side;
- the magenta planet with ring and moons;
- the space-runway belt, the rails and the front stars.

**1. Lower the top 0.5 and shrink the planet.** Targets: solid top ≤ 12.7, static peak ≤ 14.4, anim max ≤ 14.7.

| Part | New value |
|---|---|
| `ArchPost_L/_R` | y 2.06-10.9 (8.84 tall) |
| `ArchLintel` | y 10.9-12.2 |
| Corner wedges | y 9.6-10.9 |
| Post rune bands | keep 2.45 and 5.65; move the others to ≈ 7.45 and 9.25 (clear of the wedge at 9.6) |
| `ScreenTower` | y 8.55-12.2 (3.65 tall) |
| `ScreenDisplayRunner` | y 8.85-10.75 |
| `screen_bar_1..5` | bottom 9.05, heights 0.9 / 1.15 / 1.4 / 1.15 / 0.9 (tops ≤ 10.45) |
| `sparkle_scr_1/_2` | y ≤ 10.45 |
| `ScreenDisplayFront` | y 8.85-11.9; re-spread the starfield inside it |
| `TopperBase` | 0.3 thick (12.2-12.5) |
| `PlanetDish` | 0.2 thick (12.5-12.7) |
| `orb_core` | Ø 1.4, centre y 13.7 → static 13.0-14.4; with bob + pulse 12.77-14.63 (clears the dish) |
| `orb_ring_a` | Ø 3.0, same 25° tilt → about 13.0-14.4 |
| Moons | Ø 0.45, orbit radius 2.0, at y 13.4-14.1. They clear the ring rim by about 0.27 and the topper by more than 0.4 with the bob |

**2. Screen seam:** keep the 0.02 contact (see the answer below).

**3. Lights:** as planned. Drop the runner-display PointLight if `runner` shows it greying the label face.

Parts stay about 89, inside 88-96.

Answers:
- **Planet height:** lowered as above.
  - At 15.65 it towered over x18 and almost matched x20.
  - At 14.4 it is clearly above x14's crown (12.8) and clearly below x18's flames (14.9).
- **The 0.02 seam:** fine. The label frame's top face is tilted, so the gap is a thin wedge, 0.02 at the front corner
  and about 0.3 at z -9.34. The tower's front face hides it from the plaza. It reads as a bezel shadow line.
  - Do not sink the tower into the tilted frame.
  - Only if `side`/`sideHi` shows a sky sliver: fill it with one WedgePart (6.48 wide, about 0.3 × 0.8, slope 20°,
    VOID or FRAME). Use only 0° / 180° turns, so it is not X-tilted.

### x18 INFERNO: APPROVED WITH CHANGES
Keep everything else:
- the molten-river belt and the basalt/crimson/lava palette (clearly not T5, and not T2: the orange always sits on
  dark);
- the floor gate with the pointed corbel opening, lava veins, torches and the volcano console;
- the lava-channel rails with the ember chase;
- the swept tail fins with the multi-part wing trick;
- the flame stacks and the exhausts.

**1. Height: add a stepped volcano peak on the lintel.** Today the gate tops out at 10.4-11.0, under x16's gate, and
the flames at 13.0 sit under x16's planet.

| Part | Spec |
|---|---|
| `VolcanoTier1` | 7.6 × 1.2 × 2.0 at (0, 11.0, -10.335): y 10.4-11.6 |
| `VolcanoSlope1_L/_R` | WedgePart 1.4 (x) × 1.2 × 2.0 at x ±(3.8..5.2), sloping down and outward, on the lintel |
| `VolcanoTier2` | 4.8 × 1.2 × 2.0, y 11.6-12.8 |
| `VolcanoSlope2_L/_R` (optional, only if the total stays ≤ 106) | the same wedge at x ±(2.4..3.8) on tier 1, for one smooth cone |
| `CraterRim` (4.0 × 0.6 × 1.6) | moves up to y 12.8-13.4. `GateGlow` goes with it |
| Crown flames | bases sunk 0.1 into the rim (y 13.3) |
| `flame_crown_C` | 1.1 × 1.5 (tip 14.8) |
| `flame_core_C` | 0.5 × 1.6 (tip 14.9; running peak ≈ 15.64) |
| Side tongues | 0.8 × 1.2 (tip 14.5) |
| Side cores | 0.4 × 1.4 (tip 14.7) |

- Colours: your choice of BASALT / CRIMSON Studs; the crater stays CRIMSON.
- The braziers and torches stay as they are. They now flank the volcano foot with about 0.6 of clearance.
- Result: solid top 13.4, static peak 14.9, running peak ≤ 15.7, between x16 (14.4) and x20 (15.75).
- The stepped volcano is also what makes this gate unlike x14's and x16's flat beams.

**2. Rear walkway (R1): no full-width spoiler.**
- `SpoilerWing` (11.42 wide, y 3.6-4.1, z 8.0-9.25) and the `skull_eyes` lip sit at neck height exactly where the owner
  lands (z +7.5) and walks to the base. They would be walked through on every exit.
- **Spoiler:** replace it with `SpoilerWing_L/_R` 1.6 × 0.5 × 1.25 at x ±(4.11..5.71), y 3.6-4.1, z 8.0-9.25, each
  butting into its end plate's inner face. That makes a split "ducktail" wing, and the gap is the walkway.
- **`skull_eyes`:** drop it, OR make it a floor-level lava sill 8.0 × 0.25 × 0.4 at y -0.6..-0.35, z 8.0-8.4.
- **Light:** move `SpoilerGlow` into `SpoilerWing_L` or one of the plates.
- The exhausts (floor level, |x| 3.3-3.9) are fine.

**3. Fins (OK, see the answer below).**
- Name the sockets EXACTLY `wing_root_L` / `wing_root_R`, and all four fin parts per side exactly `wing_L` / `wing_R`.
- Move `FinSpar` forward so the fin's back face is at z ≤ 1.4. This keeps a corridor margin while the fin flexes.
- At the full 0.28 rad inward flex, the inner top corner reaches x ≈ 3.73, y ≈ 8.03. That clears the over-head box
  (3.5); keep it ≥ 3.6.

**4. Runes:** number them in chase order. The planned L/R pairs, front to back, are fine.

**5. Part budget:** 100-106 total (100 + 4..6 for the volcano; the spoiler change is part-neutral).

Answers:
- **Four parts per side all named `wing_L` / `wing_R`: OK.** The client turns every same-named part about the same
  static root with the same angle, so the four pieces flex as one rigid fin.
  - The pivot sits 0.2 under the fin base, so the seam opens or closes by only about 0.05.
  - Nothing else may use those names or be attached to the fins.
- **Height coordination:** the volcano peak above. Your "x16 ≤ 11.5" request isn't needed; x16 is capped at 14.4
  instead.

### x20 DIAMOND RAINBOW: APPROVED WITH CHANGES
Keep everything else:
- the rainbow road;
- the round 7-stone rainbow arch on white legs, with alternating stone depths;
- the obsidian crown with the floating diamond and flapping wings;
- the crystal towers with the marquee equalizer;
- the low crystal rails, the rear pylons, the sliding diamond tiles and the console badge.

**1. Arch chase on inlays, not on the stones.**
- The problem: the client dims every non-active rune 45 % toward black while running. With the voussoirs as runes, the
  whole rainbow arch turns muddy (yellow → olive, red → maroon) for all the hours the owner runs.
- **Stones:** the voussoirs become static `ArchStone_1..7` (same rainbow colours and Studs).
- **Inlays:** add `rune_1..7`, one inlay per stone at its centre:
  - 0.7 × 0.7 × (stone depth + 0.2), i.e. 1.3 or 1.5;
  - rotated with its stone (rotZ), proud 0.1 on both faces;
  - W diamond-white, Plastic/Universal;
  - numbered red → violet.
- Result: the arch stays at full colour, and a white flash still sweeps across it.

**2. Rear walkway (R1):** delete `RearSpoiler` (10.4 wide, y 3.15-3.65, z 8.05-9.05). It sits at neck height at the
exit spot. The rails already run into the pylons, and the crown wings carry the fins/spoiler step.

**3. Taller rear pylons:** x20 must beat x18 from `side`, `sideHi` and `rear34`, and x18's fins reach 8.3.
- Keep `PylonBody` (y -0.6..5.4) and the collars.
- `PylonShaft_L/_R`: 0.8 × 3.6 × 0.8 crystal (C, Weld), y 5.4-9.0.
- `PylonCap_L/_R`: 1.0 × 0.4 × 1.0, W Weld, y 9.0-9.4.
- `sparkle_pylon_L/_R`: 0.7 cube on its vertex, centred at 9.4 (top ≈ 10.0).
- Keep them 1.0 wide at |x| ≤ 6.3, outside the corridor.

**4. Crown clearance.**
- Today the spinning halo (horizontal radius 0.90) clears the crown sparkles at 110 % by only about 0.1, and the crown
  points by about 0.15.
- Keep ≥ 0.15 to both: put the points and sparkles at (±1.3, z_a ± 0.6), widening the band to 3.2 if needed, or use
  a 1.0 halo.

**5. Marquee: raise it 0.15, to y 8.85-10.15.**
- It is the only part in FRONT of the label's top edge (y 8.39, z -9.15). At 8.7 a high camera just clips the top of
  the label.
- The equalizer bars move up with it. In the front view the inner arch at x 3.9 is at 10.19, so it still fits.

**6. Reach x18's richness:** final visible parts and animated parts must both be ≥ x18's final counts, and stay
≤ 110. Planned is 92; with changes 1-3 it is 92 + 7 - 1 + 2 = 100. Add:
- a second, smaller crystal feather under each wing, also named `wing_L` / `wing_R` (C Weld, about 2.2 span × 0.9),
  +2 animated;
- `sparkle_rail_L2/_R2` on the middle rail posts, +2;
- `sparkle_leg_L/_R`: a 0.5 gem centred on each arch leg's front face at y ≈ 2.6 (plaza eye level), +2.

That gives about 106 parts and about 39-41 animated parts.

**7. Arch seating:** no voussoir corner may stick out past the capitals. Widen the capitals to 1.5, or nudge y.
Check it in `close` and `hub34`.

Recommended (not required):
- Make W a neutral (248, 248, 250). (242, 246, 255) is nearly Frost's snow (238, 247, 255).
- If the tiny Glass sparkles render grey or invisible, use Plastic/Universal W instead.
- The 15° wing sweep gives rx = 15°, so the validator will count the wings as tilted parts. This is harmless: the
  area is about 0.4, and 16.8 is needed to become the label. If you want the tilted count to stay 3, sweep them 10° or
  30° instead.

Answers:
- **One merged arch: yes.**
  - A second arch over the runner would hit the head box and crowd the owner's view.
  - The single grand arch on the floor, with the crown on its keystone, is clearly bigger than x14's and x16's gates on
    the console and x18's volcano gate.
- **Crown wings vs static fins: keep the crown wings.** They are animated, and the runner and the plaza both see them.
  - Do NOT add static side fins: they would copy x18's signature silhouette.
  - The side and rear presence comes from the taller pylons (change 3).
- **Rear pylons vs the upgrade sign: acceptable.**
  - The sign faces +Z. Its own side and straight-behind views are clear.
  - Only a viewer behind the OPPOSITE half (for example belt (+8, 16) looking at the left sign) has the pylon in the
    line.
  - Height doesn't matter for that: the sign top is at y 2.8, so only the pylon body occludes. The taller shaft adds
    no occlusion.
  - Keep the pylons 1.0 wide and at |x| ≤ 6.3.

---

## 3. Phase B reminders (all builders)
- Camera lock around captures, one capture at a time, then unlock.
- Print the rune order from the refreshed bay.
- Check every animated hook at its extreme (R2).
- Capture all the presets, including `side` and `sideHi`, plus `lineup` against your neighbours: the ladder above is
  what the reviewer will check in Phase C.
- Report any deviation from these numbers in BUILD_NOTES.md.
