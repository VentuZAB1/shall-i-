# Tier 8 `Tier8_x14` (x14, 700K/s): FROST: PLAN (Phase A, 2026-10-12)

Builder: T8. Template `ServerStorage.Assets.Treadmills.Tier8_x14`, lab `workspace._TreadmillLab.Bays.Bay8`
(belt centre 644, 0.6, -100). Phase A was read-only.

Today the template is the clean T6 copy. `T.validate(8)` gives 0 FAIL and 1 WARN: the gold screen face has
luminance 0.78.

## What I studied
- **Captures:**
  - `T8A_lineup_bays1to6_b` (T1-T5 from the front)
  - `T8A_bay6_hub34`, `T8A_bay6_runner_b`
  - `T8A_bay1_hub34` (T1's cyan/blue), `T8A_bay5_spawn`
  - `T8A_bay8_lineup`, `T8A_bay8_side`, `T8A_bay8_side_hi`, `T8A_bay8_rear34`, `T8A_bay8_close`
- **Tiers 1-6** are chassis-only: 14-26 bricks, no Decor, no hooks, no lights, top at y 8.5.
  - Family look: Studs on the frames, Weld on the accent blocks, Inlet on the belt strips.
  - The lab's blue-grey ambient makes (17,17,17) look dark navy.
  - T1 = saturated mid-blue (8,120,181) / (9,137,207), plus full cyan (0,255,255) and teal (0,197,197). Every T1 brick
    is opaque.
- **From the hub** people see the console front, the handles and the BACK of the tilted screen frame. The label only
  faces the runner.
  - In `runner` the label sits dead centre above the dummy's head. There is open sky above it and open air at both
    sides of the console.
  - That empty frame around the screen is where the arch goes.
- **The `side` preset is blocked.** Its camera (618, 6.6, -101) is 4 studs from Bay 7's centre, and Bay 7's dummy
  fills the shot.
  - In Phase B I will also capture `side_hi`: camera [618, 16.6, -101] looking at [644, 4.6, -101]. I checked it: a
    clean profile of Bay 8 (`T8A_bay8_side_hi`).
- **Read from the code (`_TreadLabTools.validate`, `TreadmillClient`):**
  - **Runes** chase in GetDescendants order, about 6 steps/s. The active one goes white. While running, the others dim
    45 % toward black.
  - **`halo`** = `bcf * CFrame.new(pos + bob) * Angles(0, ang*0.5, 0) * originalRotation`. It spins about the belt
    vertical, so a diamond tilted about Z spins like a coin.
  - **`sparkle_`** parts resize about their centre.
  - **`screen_gem`** lerps up to 45 % toward white.
  - **findScreen** takes parts at z < -6 whose ToOrientation X is within 0.25-0.45 rad.
- **Neighbour plans (read so the ladder stays in order):**
  - **x12 Emerald:** 68 parts, top y 9.98. Low platinum rails (y 2.2-2.8). 22 animated parts, but none of them moves:
    the hooks only change colour or size. No arch.
  - **x16 Galaxy:** 89 parts. Arch lintel y 11.4-12.7, a tall second screen, and a planet with moons up to y 15.65.
    38 animated parts.

## Concept (one line)
**"Frost Gate":** a snow-and-glass ice gate over the console. It has a navy beam hung with icicles, a crown of glass ice
crystals, and a floating, spinning ice diamond. Clear-ice handrails run down both sides on snow-capped frames, and a
frost current of light runs along the rails, up the gate, across and back.

## Palette
| Role | RGB | Material / Variant | Used for |
|---|---|---|---|
| FRAME (deep glacier navy, the dark frame) | (24, 40, 82) | Plastic / Studs (Inlet on the belt) | side frames, console bars, handles, rail posts, arch plinths, arch lintel, dark belt strips |
| SNOW (snow white) | (238, 247, 255) | Plastic / Studs on bricks, Weld on caps and plates, Universal on sparkles | snow caps, pillar bricks, screen frame + bracket, feet, light belt strips, sparkles, cradle, corner wedges |
| ICE (pale ice blue, opaque) | (168, 214, 244) | Plastic / Weld | base plate rim, console core pieces |
| CLEAR ICE (translucent) | (196, 232, 255), Transparency 0.35 | Plastic / Universal | icicles, rail bars, foot crystals |
| GLACIER (accent / lights) | (96, 165, 225) | Plastic / Weld | runes, handle grips, screen_gem |
| MIDNIGHT (label face only) | (16, 40, 92) | Plastic / Universal | screen face. Luminance 0.15 (limit 0.45), opaque |
| GLASS ICE (accent material) | (196, 232, 252), Transparency 0.3 | **Glass** | 2 pillar ice blocks, 4 crown crystals |
| ICE CRYSTAL (accent material) | (210, 238, 255) | **Ice** | `halo` |

- **Theme colours:** snow, ice, clear ice and glacier, plus FRAME navy. MIDNIGHT is only a darker shade for the screen.
- **What reads from 40-60 studs:** white and translucent ice on navy.
- **No cyan anywhere.** The bluest colour, GLACIER, sits on 16 small parts. Its hue (210 deg) and its paleness keep it
  apart from T1's (0,255,255) and (9,137,207).
- **Accent materials:** 7 parts (1 Ice + 6 Glass). That is under the 15 % cap: 12 of 85.

## Chassis recolour map (26 parts: size and position untouched, collision kept)
| Chassis part (belt-space AABB) | Role | Variant |
|---|---|---|
| Side frames 1.6x1.47x15.56, x ±(4.107..5.707) | FRAME | Studs |
| Belt strips x = 0, ±2.59 (3) | FRAME | Inlet |
| Belt strips x = ±1.30, ±3.89 (4) | SNOW | Inlet |
| Base plate 12.71x0.61x15.39 (0.65 rim each side) | ICE | Weld |
| Front console bar 14.27x2.16x1.73 | FRAME | Studs |
| Console posts 1.3x1.73x1.12 (2) + centre panel 4.19x1.73x0.69 | ICE | Weld |
| Upper console bar 9.08x1.47x1.73 | FRAME | Studs |
| Handles 1.3x1.47x2.59 (2) + handle caps 1.3x1.47x0.61 (2) | FRAME | Studs |
| Handle grips 1.21x1.21x1.64 (2) | GLACIER | Weld |
| Screen bracket 2.16x2.85x0.99 (tilted) | SNOW | Studs |
| Screen FRAME 6.48x3.46x0.86 (tilted) | SNOW | Studs |
| Screen FACE 6.14x3.11x0.86 (tilted, the label) | MIDNIGHT | Universal |
| Front feet 1.25x1.21x4.58 (2) | SNOW | Weld |

What this gives:
- **Runner view:** a navy label screen with a crisp white border, under a navy beam.
- **Hub view:** the white back of the screen, framed by white and glass pillars and the navy beam.
- **Belt:** navy and snow stripes, the T5/T6 rhythm.

## Decor list
Every decor part is in `Decor`: Anchored, CanCollide / CanTouch / CanQuery false.

Coordinates:
- Belt space, part centres, sizes X x Y x Z.
- **Axis z0 = -8.4738**, the depth centre of the front console bar.
- No part gets an X-tilt. Rotations are only about Z (lean / diamond), or 90 / 180 deg for wedges. So findScreen
  still sees exactly 3 tilted parts. Phase B checks this with the validator's tilted count.
- Chassis parts are found by AABB (they are all named "Part").
- Sub-models `Decor/Arch`, `Decor/Rails` and `Decor/Front` keep it tidy. All runes go directly in `Decor`, in chase
  order.

### A. Frost Gate arch (34 parts)
It stands on the ends of the front console bar and frames the label screen.

| # | Name | Size | Position | Colour / variant | Purpose |
|---|---|---|---|---|---|
| 1 | `ArchPlinth_L/_R` | 1.6 x 0.8 x 1.7293 | (±6.4365, 1.9632, z0) | FRAME / Studs | Base on the bar top (y 1.5632-2.3632), flush with the bar's front and back faces |
| 2 | `ArchPillarLow_L/_R` | 1.2 x 2.6 x 1.4 | (±6.4365, 3.6632, z0) | SNOW / Studs | x 5.8365-7.0365. Its inner face is flush on the handle's outer face (5.8365) |
| 3 | `ArchPillarIce_L/_R` | 1.2 x 2.4 x 1.4 | (±6.4365, 6.1632, z0) | GLASS ICE / Glass T0.3 | Glass ice block, y 4.96-7.36. It holds a PointLight |
| 4 | `ArchPillarHigh_L/_R` | 1.2 x 2.5368 x 1.4 | (±6.4365, 8.6316, z0) | SNOW / Studs | y 7.36-9.90 |
| 5 | `ArchLintel` | 14.073 x 1.2 x 1.4 | (0, 10.5, z0) | FRAME / Studs | Navy beam, y 9.9-11.1. It sits on the pillar tops, flush front and back |
| 6 | `ArchSnowCap` | 14.6 x 0.4 x 1.8 | (0, 11.3, z0) | SNOW / Weld | Snow on the beam, y 11.1-11.5. It overhangs 0.2 all round, so its silhouette is a white line |
| 7 | `ArchCorner_L/_R` | Wedge 1.6 (x) x 1.6 (y) x 1.4 (z) | x ±(4.2365..5.8365), y 8.3-9.9, z0 | SNOW / Weld | Inner corner braces with the slope facing down and inward, which rounds the gate. Triangle faces ±Z (90 deg about Y) |
| 8 | `Icicle_L1/_R1` | Wedge, 0.7 wide, 1.8 long, 0.6 deep | x ±3.75, y 8.1-9.9, z0 | CLEAR ICE / Universal | Long icicles BESIDE the screen. x 3.4-4.1, outside the screen's ±3.24 |
| 9 | `Icicle_L2/_R2` | Wedge, 0.6 wide, 0.8 long, 0.6 deep | x ±1.8, y 9.1-9.9, z0 | CLEAR ICE / Universal | Short icicles over the screen. They end at 9.1, above the runner's line of sight to the label top (about 8.45 at this depth; 8.7 even from a zoomed-out camera) |
| 10 | `CrownCrystal_L1/_R1` | 0.8 x 2.0 x 0.8 | base (±1.9, 11.2, z0), leaning 12 deg outward (about Z) | GLASS ICE / Glass T0.3 | Inner crown spikes, tip at about y 13.16. The base is sunk 0.3 into the snow cap |
| 11 | `CrownCrystal_L2/_R2` | 0.7 x 1.4 x 0.7 | base (±6.2, 11.2, z0), leaning 20 deg outward | GLASS ICE / Glass T0.3 | Pinnacles over the pillars, tip at about y 12.5, max abs(x) about 7.0 |
| 12 | `sparkle_crown_1..4` | 0.5 cube, 45 deg about Z | centred on each crown crystal's tip (`crystal.CFrame * (0, H/2, 0)`) | SNOW / Universal | White glints. Half of each is sunk into its crystal, so it stays seated while twinkling |
| 13 | `HaloCradle_L/_R` | Wedge 0.6 (x) x 0.5 (y) x 0.8 (z) | x ±(0.45..1.05), y 11.5-12.0, z0 | SNOW / Weld | Snow V-seat under the floating diamond. Each slope faces up and inward, about parallel to the diamond's lower edges (0.6 gap) |
| 14 | `halo` | 1.6 x 1.6 x 0.45, 45 deg about Z | (0, 13.0, z0) | ICE CRYSTAL / Ice | The floating ice diamond (see the clearance check below). It holds a PointLight |
| 15 | `rune_4` .. `rune_10` (7) | 0.6 x 0.6 x 1.6 | listed under the hooks below | GLACIER / Weld | Square frost-light inlays. They pass through the 1.4-deep pillars and beam and show 0.1 proud on both faces, so the hub and the runner both see them |

**Halo clearance:**
- Static, the diamond spans y 11.87-14.13. With the client's ±0.18 bob it spans 11.69-14.31.
- The snow cap top is 11.5, so the gap never closes.
- Spinning, it sweeps a radius of 1.13: z -9.60..-7.34 and abs(x) up to 1.13.
- That clears the cradle, the inner crystals (about 0.75 away at the same height) and the over-head box (z >= -7).

### B. Frost rails (18 parts)
The handrails continue the chassis handle line, x = ±5.188. They are at grip height, so they read as one rail from the
grip to the back.

| # | Name | Size | Position | Colour / variant | Purpose |
|---|---|---|---|---|---|
| 16 | `SideSnow_L/_R` | 1.5996 x 0.3 x 15.564 | (±4.907, 1.0215, 0.1729) | SNOW / Studs | Snow layer on the navy side frames (y 0.8715-1.1715), exactly their footprint. It gives a white line down both sides, seen from every angle |
| 17 | `RailPost_L1..L3/_R1..R3` | 0.8 x 2.2966 x 0.8 | (±5.188, 2.3198, z), z = -1.8, 2.6, 7.2 | FRAME / Studs | Posts from the snow top (1.1715) up to the rail bottom (3.4681) |
| 18 | `RailBar_L/_R` | 0.7 x 0.6 x 12.8745 | (±5.188, 3.7681, 1.1628) | CLEAR ICE / Universal | Clear ice handrail, y 3.47-4.07. It runs from the grip's back face (z -5.2745) to z 7.6, flush with the back post |
| 19 | `rune_1..3`, `rune_11..13` (6) | bands 0.8 x 0.7 x 0.5 | (±5.188, 3.7681, z), z = -3.54, 0.4, 4.9 (mid-span) | GLACIER / Weld | Clamp bands around the ice rail, 0.05 proud on every side. Top at 4.12 |
| 20 | `sparkle_rail_L/_R` | 0.45 cube, 45 deg about Z | (±5.188, 4.0681, 7.2) | SNOW / Universal | Glint on the rail end over the back post. Top 4.39 (4.42 at 110 %) |

### C. Front (7 parts)
| # | Name | Size | Position | Colour / variant | Purpose |
|---|---|---|---|---|---|
| 21 | `ConsoleSnow` | 11.273 x 0.3 x 0.4323 | (0, 1.7132, -9.1223) | SNOW / Studs | Snow along the front lip of the console bar, between the plinths. Its back face is flush with the console posts' front faces (-8.9061) |
| 22 | `GemFrost` | 1.4 x 1.4 x 0.15, 45 deg about Z | (0, 0.4824, -9.4134) | SNOW / Weld | White diamond plate flush on the bar face (z -9.3384), y -0.51..1.47 |
| 23 | `screen_gem` | 1.0 x 1.0 x 0.3, 45 deg about Z | (0, 0.4824, -9.6384) | GLACIER / Weld | Frost-core gem seated on the plate. It faces the plaza and pulses white while the owner runs |
| 24 | `FootCrystal_L/_R` | 0.8 x 1.8 x 0.8 | base on the foot top (x -6.204 / 6.3337, y 0.6121, z -5.4), sunk 0.3, leaning 15 deg outward | CLEAR ICE / Universal | Ice crystal on each front foot, so the ground line has crystals in the spawn and hub views. Max abs(x) about 7.2 (the path lamp starts at 7.7) |
| 25 | `sparkle_foot_L/_R` | 0.45 cube, 45 deg about Z | on each foot crystal's tip | SNOW / Universal | Ground-level glints |

```
FRONT ELEVATION (seen from the hub, -Z)                                   y
                              <>  halo (spins + floats)                   14.1
                 /*\          \/          /*\                             13.2  crown crystals + sparkles
       /*\      /   \      [cradle]      /   \      /*\                   12.5
     [===================== SNOW CAP =====================]               11.5
     [P]=[r]=============[r]=====[r]=============[r]=[P]                  11.1-9.9  navy beam + runes
     |S|\       v           v       v           v      /|S|               icicles (long beside the screen)
     |r|  \__                                     __/  |r|                corner wedges
     |G|      [ white back of the label screen ]       |G|  <- glass ice + PointLight
     |S|[==handle==]==== upper console bar ====[==handle==]|S|            4.5
     |r|                                                    |r|
   [plinth]~~~~~~~~~~~~ snow lip ~~~~~~~~~~~~~~~~~~~~~~[plinth]           1.56
   [========== front console bar  <> gem on a white diamond ==========]
     ^ foot crystal                                       foot crystal ^
```

## Animation hooks (TreadmillClient only, no scripts): 23 animated parts, 4 hook types
- **`rune_1..13`: the frost current.** All runes are created in this order as direct children of `Decor`.
  - Left rail, back to front: `rune_1` (z 4.9), `rune_2` (z 0.4), `rune_3` (z -3.54).
  - Up the left pillar: `rune_4` (-6.4365, 3.6632), `rune_5` (-6.4365, 8.6316).
  - Across the beam (y 10.5): `rune_6` (x -3.6), `rune_7` (x 0), `rune_8` (x 3.6).
  - Down the right pillar: `rune_9` (6.4365, 8.6316), `rune_10` (6.4365, 3.6632).
  - Right rail, front to back: `rune_11` (z -3.54), `rune_12` (z 0.4), `rune_13` (z 4.9).
  - **Idle:** steady glacier-blue lights.
  - **Running:** a white flash circles the runner, along the left rail, over the gate and back down the right rail.
    That is 13 steps, a 2.2 s loop. The others dim.
  - After `T.refresh(8)` I will print the rune order in the bay clone to confirm it.
- **`halo`:** the ice diamond floats ±0.18 and spins about the vertical, like a coin. It turns slowly when idle and
  about 5x faster while running. **It is the first moving part in the new ladder**: x12's hooks only change colour or
  size.
- **`sparkle_` (8):** 4 crown tips, 2 rail ends and 2 foot crystals twinkle 55-110 %, faster while running.
- **`screen_gem`:** the frost-core gem on the console front pulses toward white while running.
- **Not used:** flame_ (fire flicker is wrong for ice), wing_, orb_, screen_bar_, chevron_ and led_side_ (forced
  cyan). I leave them for x16-x20.

## Lights (3, all PointLight, Shadows = false)
| Light | Parent | Colour | Brightness | Range |
|---|---|---|---|---|
| `HaloLight` | `halo` | (190, 230, 255) | 1.5 | 12 |
| `PillarLight_L` / `_R` | `ArchPillarIce_L` / `_R` | (170, 220, 255) | 1.0 | 8 |

- They give a cold glow from the gate's glass blocks and its crown.
- The label GUI has LightInfluence 0, so it is not tinted.
- If the `runner` capture shows the pillar lights washing the label frame, I will lower them to Brightness 0.6.

## Progression
**vs x12 Emerald** (rails only, top 9.98, 68 parts, 22 animated, nothing moves):
- **New silhouette:** a full gate over the console, with a crown and a floating diamond. Top 9.98 → 14.1.
- **Taller handrails** at grip height (top 4.1 vs 2.8), running on white snow-capped frames.
- **First real motion:** the spinning, floating halo.
- **A longer chase:** 13 runes that loop around the runner and over the gate, against 12 on the rails only.
- **More animated parts:** 23 vs 22, with 7 accent-material parts (glass + ice) vs 1.
- **Size:** 85 parts vs 68.

**Stays below x16 Galaxy** (89 parts, beam at 11.4-12.7, tall second screen, planet to 15.65, 38 animated):
- My beam is lower (9.9-11.1, cap 11.5) and my top is lower (14.1).
- No second screen and no orbit system.
- Fewer parts (85) and fewer animated parts (23).
- So Galaxy's "same gate + tall console + planet" still reads as the next step up.

**vs tiers 1-6:**
- The only white-and-translucent build: snow, glass and ice on deep navy.
- T1 is opaque saturated blue and cyan with no white, no translucency and no decor.
- Frost has no cyan, and blue is only a small accent: the GLACIER runes and gem.
- Nothing like T5/T6's black with red/gold.
- The gate silhouette is new in the ladder.

## Limits: how every hard limit is respected
- **Functional parts** (Conveyor, Belt, Zone, Blocker, FrontStop): not touched.
- **Attributes:**
  - Name, Tier 8, TierName "x14", SpeedPerSecond 700000 and LabelHeight 10.6 stay.
  - Add `SetAttribute("Theme", "Frost")`.
- **Chassis:** only Color and MaterialVariant change. Collision and anchoring stay.
- **Envelope:**
  - Max abs(x) is 7.3 (snow cap). Plinths reach 7.2365 and foot crystals about 7.2.
  - z runs from -9.79 (gem front) to 7.95. The halo's spin reaches -9.60.
  - Max y is 14.13 static (14.31 at the bob peak).
  - Lowest decor y is -0.51 (GemFrost), above the floor (-0.5985).
  - The path lamp (x ≥ 7.7) is clear.
- **Upgrade-sign keep-out (abs(x) > 6.4, 4 <= z <= 8.6):** nothing there.
  - The rails, posts, runes and sparkles stay at abs(x) <= 5.59.
  - The only decor beyond abs(x) 6.4 is the arch and the foot crystals, at z <= -5.
- **Runner Zone (abs(x) <= 3.1, 0.6-6.6, abs(z) <= 7.1):** nothing.
  - Decor with abs(x) <= 3.1 is either at z <= -8.9 (console snow, gem, plate), or at z about -8.47 and y >= 9.1
    (icicles, beam, crown, halo).
- **Runner-camera corridor (abs(x) <= 5, y >= 4.5, z >= 1.5):** nothing.
  - The rail parts overlap abs(x) <= 5, but they top out at 4.12 (runes) and 4.39 (sparkles at 100 %).
  - So I expect no WARN here.
- **Over-head box (abs(x) <= 3.5, 6.6-12, -7 <= z <= 1.5):** empty. Every arch part is at z <= -7.34, including the
  halo sweep.
- **Label screen:**
  - The face is MIDNIGHT, luminance 0.15, opaque.
  - No decor part is X-tilted, so the tilted count stays 3. Phase B verifies it.
  - Nothing sits in front of the label in the runner view:
    - The beam bottom is 9.9 and the short icicles end at 9.1. The line of sight to the label top is about 8.45.
    - The long icicles hang at abs(x) >= 3.4, outside the frame (abs(x) 3.24).
- **Banned items:** no Neon, ForceField, Script, VFX, Decal, Texture, MeshPart or Union.
  - Only Part blocks plus WedgeParts (the corner braces, icicles and cradle).
- **Materials:**
  - No SmoothPlastic. Every Plastic part has a Studs / Inlet / Universal / Weld variant.
  - Accent materials are 7 of about 85 (cap 12).
  - Translucency: 0.3-0.35, within the brief's 0.2-0.45.
- **Lights:** 3, Shadows off.
- **Craft:**
  - Every piece sits flush on something: plinth on bar, pillar on plinth, beam on pillars, cap on beam, crystals sunk
    into the cap, posts on the snow layer, rail on the posts and the grip.
  - Symmetric pairs throughout.
  - Touching faces only meet back-to-back. The inlays and bands are 0.05-0.1 proud, so no faces are coplanar and
    overlapping.
  - The only intentional gap is the animated halo over its cradle.

## Estimated part count
| Group | Parts |
|---|---|
| Chassis | 26 |
| Arch | 34 |
| Rails | 18 |
| Front | 7 |
| **Total visible** | **85** |

- Arch breakdown: plinths 2, pillars 6, beam 1, cap 1, corner wedges 2, icicles 4, crown crystals 4, crown sparkles 4,
  cradle 2, halo 1, arch runes 7.
- Rails breakdown: snow layers 2, posts 6, bars 2, rail runes 6, sparkles 2.
- Front breakdown: console snow 1, gem plate 1, gem 1, foot crystals 2, foot sparkles 2.
- Under the 110 aim and the 140 cap.
- 7 accent-material parts, 3 lights, 23 animated parts.

## Phase B order (after approval)
1. Recolour the chassis and set Theme. `T.refresh(8)`; capture `runner` (label contrast) and `hub34`.
2. Arch: plinths, pillars, beam, cap, corner wedges and icicles. Refresh, then capture `runner`, `close`, `hub34` and
   `eye`.
   - First I test the wedge orientations on one icicle and one corner brace.
3. Crown crystals, cradle, halo and lights. Refresh, then check the tilted count and capture `lineup` and `spawn`.
4. Rails, the snow layers and the front pieces. Refresh, then capture `rear34`, `side_hi` and `runner`.
5. Runes in chase order. Refresh and print the rune order from the bay clone.
6. Capture all 8 presets plus `side_hi` (ids `T8_<preset>_v<n>`). Target the validator at 0 FAIL / 0 WARN. Write
   BUILD_NOTES.md.

## Risks and Phase B tuning (I will report any change)
- **Glass:** it may render too dark or too clear in the lab. Fallback: Plastic / Universal at Transparency 0.35. That
  also drops the accent count to 1.
- **Icicle wedges:** right-triangle shards may read oddly. Fallback: thin translucent sticks of the same lengths.
- **Glacier runes on the navy beam:** if they don't pop, I lighten GLACIER toward (120, 185, 240).
- **Lab ambient:** it may push FRAME navy toward black. If so, FRAME goes to (30, 50, 100).
