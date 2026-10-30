# T11 `Tier11_x20` (x20, 1M/s) DIAMOND RAINBOW: VISUAL REVIEW (Phase C, 2026-10-12)

Reviewer: independent visual reviewer (`Rev11`). READ-ONLY: nothing in the game was edited (no refresh/reset, no template
or lab edits). I read the brief, `PLAN_REVIEW.md`, `PLAN.md`, `BUILD_NOTES.md` and `TreadmillClient`, dumped every part of
`Bays.Bay11.Treadmill` in belt space (the lab copy matches the template; differences are float rounding only), and
re-computed every animated hook at its extreme.

`T.validate(11)`: **0 FAIL, 0 WARN**: 106 visible parts (80 decor), 13 accent (Glass), 3 lights, 3 tilted parts, label face
(30,26,64) lum 0.12.

## VERDICT: **FIX**
It's a beautiful, clean model, and the closest of the five to "on point". It is NOT finished yet, for four reasons:
- It fails one agreed ladder number: the animated parts.
- The winged crown doesn't yet make x20 the *obvious* king at hub distance.
- A light gap shows under the marquee from normal (raised) player cameras.
- The twinkling gems lift off their posts.

All four are small, numeric fixes. The total after the fixes is 109 parts (≤ 110).

---

## Items

### 1. MUST: animated parts are below x18's (plan-review change 6)
- x20 has **39** moving parts: 7 runes, 1 halo, 4 wing parts, 12 sparkles, 7 EQ bars, `screen_gem`, `hood_emblem`, 6 chevrons.
- x18's final count is **40** (the orchestrator confirmed this): 14 flames, 8 fin parts, 10 runes, 4 sparkles, `belt_cracks`,
  `skull_eyes`, `hood_emblem`, `screen_gem`.
- The visible parts tie at 106 / 106.
- Change 6 requires x20 ≥ x18 on both counts.

**Fix:** add at least 2 animated parts, symmetric or centred.
- Recommended: `chevron_7` / `chevron_8`.
  - Same tile as now: 0.8 × 0.12 × 0.8, 45° about Y, W Plastic/Universal, y 0.32 (0.26-0.38).
  - Place them on the GREEN centre strip (x 0) at z −1.4 and +1.0, between the existing rows.
  - This makes a 3-lane diamond stream under the runner. The tiles stay below the Zone (0.6), so nothing clips the feet.
- The result is 41 animated parts.
- If x18 grows again in its own fix pass, stay ≥ it.

### 2. MUST: make the winged crown read as the king at 40-60 studs
**Evidence (fair comparison): `R11_front55_b10b11`.**
- The camera is centred exactly between bays 10 and 11, 52 studs out, at eye height 7.
- x20's **opaque** top sits at x18's flame-tip height:
  - x20 crown points 14.55, wing tips 14.77;
  - x18 flame tips 14.9 static, about 15.6 while running.
- Only the small glass diamond (15.75) is higher, by about 7 px.

**Other captures:**
- `R11_lineup7to11` and `R11_hub45_plusX`: the main feathers (3.0 span × 0.25 thick) read as thin grey shards against the
  bright sky.
- x18's dense black/red gate reads heavier.

The rainbow arch makes x20 the most *distinctive* model. It is not yet the obvious *biggest*.

**Fix: enlarge the two MAIN feathers** (the white `wing_L` / `wing_R` WedgeParts):
- span about 3.0 → **4.1**;
- height 1.3 → **1.6**;
- thickness 0.25 → **0.35**;
- root edge flush on the hinge's outer face (x ∓2.0, see item 7);
- tip at rest ≈ (∓6.1, 14.7).

I computed the tip about the hinge (∓1.8, 13.25) at ±0.28 rad:

| Flap | Tip position | Check |
|---|---|---|
| Up | ≈ (∓5.53, **15.83**) | ≤ 16 |
| Down | ≈ (∓6.33, 13.46) | \|x\| ≤ 6.4; ≈ 4.4 above the arch shoulder (the arch's outer face at x 6.33 is at y ≈ 9.0) |

- Scale the crystal under-feather in proportion (about 2.9 × 1.1).
- Re-check all wedge vertices at both extremes.
  - The taller root moves its bottom vertex to about (∓2.12, 12.74) at the down-flap, against the arch's outer face at
    about 12.6 there. Keep ≥ 0.15.
  - Also keep clear of the halo (radius 0.90) and the crown points.
- The result is an ~12-wide winged crown spread over the 14.6-wide arch. Nothing else in the lineup has that silhouette.

**Optional, if `R11_front55_b10b11` still doesn't show x20 clearly above x18 after the wing change:**
- `CrownPoint_1..4`: 0.9 → 1.35 tall (y 13.65-15.0).
- Their sparkles: centre 15.19 (see item 4); top at 110 % is 15.57.
- The horizontal clearance to the spinning halo stays 0.21.

**Re-capture** `runner` afterwards: the bigger wings must stay a top-of-frame accent, nowhere near the label.

### 3. MUST: light gap between the screen top and the marquee (builder open point: fill it)
**The gap:**
- The screen frame's top edge is at y 8.53 (z −9.29).
- The marquee bottom is at 8.85 (front face z −9.07).
- From any camera above about 8.5, a pale strip shows across the full 6.5-wide screen. Roblox's default third-person camera
  usually sits up there.
- It reads as a construction gap, as if the screen hangs loose under the marquee.

**Evidence:**
- Visible in `R11_close` (strongest), `R11_hub34` and `R11_front_mid_hi`.
- Hidden at eye level (`R11_eye`) and from the runner (`R11_runner`, `R11_runner_low`).

**Fix:** one axis-aligned filler, `MarqueeSkirt`.
| Property | Value |
|---|---|
| Size | 6.48 × 0.32 × 0.22 |
| Position (belt) | (0, 8.69, −9.18), i.e. y 8.53-8.85, z −9.29 to −9.07 |
| Finish | O (26,24,40) Plastic/Studs or Weld |
| Flags | the usual Decor flags |

- Its rx is 0, so it can never become the label screen.
- It rests on the frame's top/back edge and butts the marquee's front-bottom edge.
- From the plaza, the dark screen then runs straight up to the white marquee.
- From the runner, it sits above the frame lip and the label top (8.39), so the label stays clear.
- Verify in `close`, `hub34` and `runner`.

### 4. MUST: twinkling gems lift off their posts (only the diamond may hover)
**The problem:**
- `sparkle_crown_1..4` and `sparkle_rail_L/_R/_L2/_R2` touch their supports exactly at 100 % (Edit mode).
- The client scales them 55-110 % **about their centre** (`TreadmillClient` lines 535-537).
- So in game they float most of the time: the gap is up to **0.156** at 55 %, and the mean size is about 90 %.

**Fix:** lower each centre by 0.156 so the gem still touches at 55 %:
| Gems | Centre now | Centre after | At 110 % |
|---|---|---|---|
| Crown sparkles | 14.90 | **14.74** | top 15.12, sinks 0.19 into the point |
| Rail sparkles | 2.95 | **2.79** | sinks 0.19 into the bar |

- If you do item 2's optional taller points, the crown sparkles' centre is 15.19 instead.
- `sparkle_pylon_L/_R` (centred on the cap top) and `sparkle_leg_L/_R` (half sunk) are already correct.

### 5. NICE: the diamond kisses the crown band at the bottom of its float
- The `halo` bottom is 13.85 at rest and 13.67 at the float minimum. The `CrownBand` top is 13.65.
- That leaves **0.017** of clearance, so every ~3.1 s the gem looks like it bounces on the band.
- **Fix:** halo cube 1.1 → **1.05**, centre y 14.80 → **14.86**.
  - Float range: 13.77-15.95.
  - Minimum gap: 0.12. Top: 15.95 ≤ 16.
  - Horizontal radius: 0.86, so the clearance to the points grows to 0.25.
- Keep the PointLight inside it.

### 6. NICE: close the V-notches at the arch's outer rim (builder open point)
**The notches:**
- The stones are 2.99 long, so their outer corners stop 1.05° short of each joint.
- That leaves six notches about 0.27 wide × 0.5 deep on the outer rim.
- They are visible up close (`R11_eye`, `R11_crown_close`, `R11_front_mid_hi`). From 40 studs and more they vanish.
- They read as "segmented", not as a LEGO arch.

**Fix:** `ArchStone_1..7` length 2.99 → **3.26**.
- The outer corners then meet on the joint bisectors (r 7.33).
- The extra inner overlap stays buried inside the neighbouring stone, thanks to the alternating 1.1 / 1.3 depths.

**Checked:**
- The end stones' outer-bottom corners move to (±7.333, 5.702), still inside the capitals (x ≤ 7.35, top 5.83).
- \|x\| stays ≤ 7.4.
- The keystone becomes ±1.63, so widen `CrownBand` 3.2 → 3.3 (or accept a 0.03 lip).
- The rune inlays are centred and stay as they are.

### 7. NICE: the main feathers float off their hinges
- At rest, the main feather's root edge runs from x ∓2.23 (y 12.97) to ∓2.00 (y 14.25).
- The `wing_root_L/_R` outer face is at x ∓2.0 (y 12.85-13.65).
- That leaves a **0.11-0.23** gap over the hinge height. Today the crystal under-feather behind it hides most of it.
- When you resize in item 2, make the root edge flush with the hinge's outer face over 12.85-13.65.

### 8. NICE: slit between the arch legs and the console bar
- The `ArchLeg_L/_R` back face is at z −9.485. The console-bar front is at −9.338.
- That leaves a **0.147** slit for y 0.2-1.56; the capital is 0.047 off.
- It shows as a hairline from the side and from 45°.
- **Fix:** `ArchLeg` depth 1.3 → 1.45, centre z −10.135 → −10.06. The front face stays at −10.785, the back face becomes flush,
  and `sparkle_leg` doesn't move.

### 9. NICE: the crystal reads as a "ghost lattice" against the sky
- Transparency 0.25 plus the Weld X-pattern makes `PylonShaft_L/_R` and the crystal under-feathers look like faint white
  scaffolding from 45-60 studs (`R11_hub45_plusX`, `R11_lineup7to11`, `R11_sideFar_plusX`).
- **Fix:** take those 4 parts to Transparency **0.1-0.15**, so they hold their shape against the sky.
- Leave the console towers and rail posts at 0.25: they are seen against the model, and they read fine there.

### 10. KEEP: the obsidian screen frame (builder's deviation is approved)
**From the plaza** (`R11_eye`, `R11_front_mid_hi`, `R11_spawn`):
- The dark screen back is the focal anchor of the front.
- It splits the white console, marquee and arch legs into clear horizontal bands.
- A white frame would merge into one flat white slab (the builder's v1 captures).

**From the runner** (`R11_runner`, `R11_runner_low`):
- The label stays crisp.
- The frame (26,24,40) and the face (30,26,64) are almost the same darkness, so there is no visible bezel.
- That's fine: the white towers and marquee frame the screen.

Do not revert.

---

## Ladder check (x16 → x18 → x20)
| Measure | x16 Galaxy | x18 Inferno | x20 now | Agreed x20 target |
|---|---|---|---|---|
| Static peak | 14.40 | 14.90 | **15.75** | 15.75 ✓ |
| Solid / opaque top | ≤ 12.7 | 13.4 (flames 14.9 look solid) | 14.55 (points), wings 14.77 | 14.55 ✓ (but see item 2) |
| Visible parts | 89 | 106 | 106 (109 after fixes) | ≥ x18, ≤ 110 ✓ |
| Animated parts | 38 | **40** | **39** ✗ | ≥ x18 → item 1 |
| Width | 14.5 | 14.3 | **14.7** (widest) | ✓ |

**Front** (`R11_front55_b10b11`, `R11_lineup`, `R11_lineup7to11`):
- The tiers step up cleanly, and x20 is the tallest and the only rainbow build.
- But x18 out-masses it. Items 2 and 9 close that gap.

**Rear** (`R11_rear34`, `R11_rear_straight`):
- A clear step: the white pylons frame the rainbow road leading to the arch and crown, and the crown is visibly higher than
  x18's volcano and fins.

**Side** (`R11_side`, `R11_sideHi`, `R11_sideFar_plusX`):
- The arch is edge-on, so the side presence comes from the pylons (gem top 10.0, above x18's fins at 8.3) and the crown.
  That's acceptable.
- Bigger wings (item 2) help here too.

## Readability and hub checks (all OK)
- **Runner view** (`R11_runner`, `R11_runner_low`):
  - "+1M / sec" is crisp on the midnight face.
  - The raised marquee and EQ sit fully above the label (the EQ bars only shrink, 55-100 %).
  - The wings and crown sit at the top of the frame and cover nothing.
  - The face is not lifted by the 3 lights (capitals 1.0 / 9, diamond 2 / 12). Rule R3 is OK.
- **Upgrade signs:** both lab copies are fully readable from the base side (`R11_rear34`, `R11_rear_straight`).
  - The pylons (x 5.25-6.25, z 7.95-9.15; gems ≤ 6.36 at 110 %) stay out of the sign keep-out.
  - The hub lamp (x 7.7-9.1, z −6.8) is clear: the nearest parts are the plinths at z ≤ −9.3.
- **Exit walkway (R1):** \|x\| ≤ 4.1, z ≥ 7, y 0.3-6.6 is empty. The rails are at \|x\| ≥ 4.79 and the pylons at ≥ 5.25.
- **R2 extremes**, re-computed from the code:
  - wings ±0.28 rad: main x 1.72-5.25, y 12.86-15.58, 0.25 above the arch;
  - halo: 13.67-15.93, 0.21 clear of the points horizontally;
  - crown sparkles: ≤ 15.28 at 110 %;
  - chevrons: wrap z −3.8 to 3.4 at y 0.26-0.38.
  - Nothing passes y 16, \|x\| 7.4, the Zone, the head box or the corridor.
- **Craft:**
  - No z-fighting: alternating stone depths, and inlays 0.1 proud.
  - Flush stacks everywhere else: towers on the upper bar, marquee on the towers, rail posts on the frames, collars 0.05 proud.
  - Plastic + Studs/Inlet/Weld/Universal throughout; Glass only on the 13 gems (12 %); 4 wedges (the wings only).
  - Symmetric apart from the intended rainbow order.

## What is good: keep all of this
- The **rainbow road**: red on the runner's left through violet, Inlet. The best runner view in the lineup (`R11_runner`).
- The **round 7-stone rainbow arch** on white legs with obsidian capitals and plinths. The white inlay chase keeps the stones
  at full colour while running (plan-review change 1 done right).
- The **floating spinning diamond**: from the front it reads as a crisp white rhombus over the obsidian band
  (`R11_front_mid_hi`, `R11_crown_close`).
- The **white marquee with the 7-bar rainbow EQ** on crystal towers, raised to 8.85-10.15 as agreed, with the blue
  `screen_gem` on the plaza face and the violet `hood_emblem` badge.
- The **rear pylons** (taller as agreed), no spoiler, a clean walkway. The rear view is lovely (`R11_rear_straight`).
- The neutral white W (248,248,250), unlike Frost's snow. The palette is premium (white + obsidian + spectrum) and not
  toy-like.
- 0 FAIL / 0 WARN. All 7 plan-review changes are applied; only change 6 is now one part short because x18 grew (item 1).

## Captures (all mine, under `T.lock("Rev11")`, one at a time)
| Group | Capture ids |
|---|---|
| Presets | `R11_spawn`, `R11_hub34`, `R11_eye`, `R11_side`, `R11_sideHi`, `R11_runner`, `R11_rear34`, `R11_close`, `R11_lineup` |
| Extra views | `R11_front55_b10b11` (fair x18 vs x20, centred between the bays, 52 studs), `R11_lineup7to11` (85 studs), `R11_hub45_plusX`, `R11_hub45_minusX` (x18 in the foreground; framing only), `R11_sideFar_plusX` (38-stud profile), `R11_rear_straight`, `R11_crown_close`, `R11_front_mid_hi`, `R11_runner_low` |

- I checked every image against its camera maths. None shows another bay's view, so the lock lapse the orchestrator reported
  did not affect these.
- The mock "+1M" label was present in all the runner-side captures.

## After the fixes
1. Run `T.refresh(11)` and `T.validate(11)`: 0 FAIL / 0 WARN, ≤ 110 parts, animated ≥ x18.
2. Re-capture `close`, `hub34`, `runner` and `lineup`, plus the `R11_front55_b10b11` framing: camera (699, 7, −152) looking at
   (699, 7, −100).
3. Re-run the R2 extremes for the new wings and the sunk sparkles.
4. Append the results to `BUILD_NOTES.md`.
