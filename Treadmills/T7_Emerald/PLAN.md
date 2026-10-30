# Tier 7 `Tier7_x12` (x12, 600K/s): EMERALD: PLAN (Phase A)

Builder: T7. Template `ServerStorage.Assets.Treadmills.Tier7_x12`, lab `workspace._TreadmillLab.Bays.Bay7` (pivot 622, 0.6, -100).
Phase A was read-only. The current template is the clean T6 copy: `T.validate(7)` = 0 FAIL, 1 WARN (gold screen face, lum 0.78).

## What I studied
- **Bays 1-6.** Captures: `T7A_lineup_bays1to7`, `T7A_T1to3_hub34`, `T7A_T4_spawn`, `T7A_T5_hub34`, `T7A_T6_spawn`,
  `T7A_T6_hub34`, `T7A_T6_runner`, `T7A_T6_side`, `T7A_bay7_rear34`, `T7A_bay7_close`.
  - Tiers 1-6 are chassis-only. T5 and T6 are the same 26-part chassis in two colours each (black + red / black + gold).
    They have no decor, no animation hooks and no lights.
  - So T7 is the first tier with a `Decor` model at all.
- **The family look:** chunky Plastic bricks.
  - Studs (square sockets) on the dark frames.
  - Weld (diagonal X) on the accent blocks.
  - Inlet on the belt strips.
  - The lab's blue-grey ambient renders (17,17,17) black as dark navy.
- **The `side` preset is blocked for Bay 7.** Its camera (596, 6.6, -101) sits inside Bay 6, 4 studs from Bay 6's dummy
  (the same thing happens one bay down in `T7A_T6_side`). In Phase B I'll also capture an unobstructed `side_hi`:
  camera P+(-26, 16, -1) looking at P+(0, 4, -1) = [596, 16.6, -101] -> [622, 4.6, -101].
- **TreadmillClient hooks**, read from the source:
  - `rune_` parts flash in **GetDescendants order**, not by their number. Only one is white at a time, and the rest dim
    45 % toward black while running.
  - `sparkle_` parts resize around their centre.
  - `screen_gem` and `hood_emblem` lerp toward white while running.
  - The screen detector takes parts at z < -6 whose ToOrientation X is 0.25-0.45 rad, then picks the smallest one with
    area >= 75 % of the largest.

## Concept
**"Emerald Vault":** an onyx-black jewel box set in platinum.
- Low platinum side rails run the full belt length, set with emerald-cut gems. While the owner runs, a white glint
  chases around both rails.
- Gem-crowned rail posts and console corners twinkle.
- A big faceted emerald crest sits on a bright emerald screen.

## Palette (exact RGB, MaterialVariant per role)
| Role | RGB | Variant | Notes |
|---|---|---|---|
| ONYX (dark frame) | (16, 38, 30) | Studs | green-black. Clearly not T5/T6's neutral (17,17,17), still the family's dark frame |
| EMERALD (main jewel green) | (0, 172, 100) | Weld (Inlet on belt strips) | hue ~155 deg, full saturation, blue-leaning jewel green. T4 is ~105-110 deg, 45-70 % saturation, yellow-grass |
| EMERALD DEEP | (0, 100, 60) | Inlet | belt stripes |
| SCREEN DEEP (label face) | (0, 78, 50) | Universal | luminance 0.23 (limit 0.45), opaque. Yellow "+600K" text reads well on it |
| PLATINUM (trim) | (212, 220, 224) | Universal | cool silver-white. No gold anywhere, so T7 can't read as "T6 with green" |
| GEM (bright emerald) | (60, 230, 140) | Weld | see the gem table below |

How GEM is used:
| Parts | Finish |
|---|---|
| runes, hood_emblem | opaque |
| crystals | Transparency 0.25 |
| `screen_gem` | **Glass**, Transparency 0.15. This is the only accent-material part (1 of 68, limit 15 % = 10) |

Phase B check: if Weld's X pattern looks noisy on the small gems, switch the gems to Universal and note it.

## Chassis recolour map (26 parts; size and position untouched)
Positions are belt-space AABB centres.
| Chassis part | Role | Variant |
|---|---|---|
| Side frames 1.6x1.47x15.56 at x ±4.91 | ONYX | Studs |
| Belt strips x = 0, ±2.59 | EMERALD DEEP | Inlet |
| Belt strips x = ±1.30, ±3.89 | EMERALD | Inlet |
| Front console bar 14.27x2.16x1.73 (z -8.47) | ONYX | Studs |
| Console posts 1.3x1.73x1.12 (x -2.85 / +2.64) | PLATINUM | Universal |
| Centre console panel 4.19x1.73x0.69 | EMERALD | Weld |
| Upper console bar 9.08x1.47x1.73 | ONYX | Studs |
| Screen bracket 2.16x2.85x0.99 (tilted) | PLATINUM | Universal |
| Screen face 6.14x3.11x0.86 (label) | SCREEN DEEP | Universal |
| Screen frame 6.48x3.46x0.86 | EMERALD | Weld |
| Handles 1.3x1.47x2.59 (x ±5.19) | ONYX | Studs |
| Handle caps 1.3x0.61x1.47 (top y 5.108) | PLATINUM | Universal |
| Handle grips 1.21x1.21x1.64 (x ±5.19, z -6.1) | EMERALD | Weld |
| Base plate 12.71x0.61x15.39 | EMERALD | Weld |
| Front feet 1.25x1.21x4.58 (x +6.33 / -6.20) | PLATINUM | Universal |

What this does:
- **Screen frame:** the big emerald slab the plaza sees, with Weld's X tiles reading as facets.
- **Base plate:** shows as a 0.65-wide emerald plinth line along both sides at floor level.
- **Belt:** two-tone green "jewel lane" in the T5/T6 stripe rhythm, under the white arrow texture.

## Decor list (all inside `Decor`)
Every decor part: Anchored, CanCollide/CanTouch/CanQuery false, Plastic + variant unless noted.

Coordinates:
- Positions are belt space (`Belt.CFrame * CFrame.new(x, y, z)`), axis-aligned unless a rotation is given.
- **Rail line x = ±5.188**, the exact centre of the chassis handles and grips, so the rails continue the handle line.
- **Crystal rotation** (point-up cube) = `CFrame.Angles(rad(35.264), 0, 0) * CFrame.Angles(0, 0, rad(45))`. Its
  ToOrientation X is 35 deg, outside the screen detector's 14-26 deg window.

| # | Name | Size | Position (centre) | Colour / variant | Purpose |
|---|---|---|---|---|---|
| 1 | `RailStanchion_L` / `_R` | 1.0 x 2.292 x 1.0 | (±5.188, 2.017, -5.775) | PLATINUM / Universal | Column from the side-frame top (y 0.871) up to the grip bottom (3.163). It "holds up" the handle grip and is the rail's front anchor. Back face flush with the grip's back face (z -5.275) |
| 2 | `RailBar_L` / `_R` | 0.8 x 0.6 x 13.23 | (±5.188, 2.5, 1.34) | PLATINUM / Universal | The low side rail, y 2.2-2.8 (upper-thigh height on the dummy). Runs z -5.275 (butts into the stanchion) to 7.955 (flush with the side-frame back end) |
| 3 | `RailPost_L1..L3` / `R1..R3` | 0.8 x 1.329 x 0.8 | (±5.188, 1.536, z) at z = -1.365, 3.045, 7.455 | PLATINUM / Universal | Posts from the side-frame top (0.871) to the rail bottom (2.2). Even 4.41 spacing from the stanchion |
| 4 | `RailCollar_L1..L3` / `R1..R3` | 1.0 x 0.3 x 1.0 | (±5.188, 2.95, z_post) | ONYX / Studs | Dark setting cup on the rail top over each post (y 2.8-3.1). The rear one is flush with the rail end (z 7.955) |
| 5 | `sparkle_RailL_1..3` / `sparkle_RailR_1..3` | 0.7 cube, crystal rotation | (±5.188, 3.1, z_post) | GEM / Weld, T 0.25 | Point-up emerald crystal. Its centre sits on the collar top, so the lower half stays seated even at 55 % twinkle. Tip at y 3.71 (3.77 at 110 %) |
| 6 | `rune_1 .. rune_12` | 0.5 x 0.2 x 0.9 | on the rail top, y 2.9 (2.8-3.0), x ±5.188 | GEM opaque / Weld | Emerald-cut gem inlays, 2 per rail span (all spans 3.41 long, even gaps). See the rune order below |
| 7 | `sparkle_ConsoleL` / `_R` | 0.8 cube, crystal rotation | (±5.188, 5.108, -8.344) | GEM / Weld, T 0.25 | Crystal points crowning the two console corners. They sit centred on the platinum handle caps, tip at y 5.80, and frame the screen from both sides |
| 8 | `ScreenCrestBase` | 2.4 x 0.35 x 0.865 | built in the screen frame's local space: `frame.CFrame * CFrame.new(0, 1.7295 + 0.175, 0)` -> belt (0, 8.543, -9.758), tilted 20 deg with the screen | PLATINUM / Universal | Setting bar flush on the frame's top face. Front and back faces flush with the frame, so nothing overlaps |
| 9 | `ScreenCrestProng_L` / `_R` | 0.35 x 0.5 x 0.865 | `frame.CFrame * CFrame.new(±0.95, 2.3295, 0)` -> belt (±0.95, 8.942, -9.903) | PLATINUM / Universal | Prongs that hug the gem's side points |
| 10 | `screen_gem` | 1.1 x 1.1 x 0.7 | `frame.CFrame * CFrame.new(0, 2.5295, 0) * CFrame.Angles(0, 0, rad(45))` -> belt (0, 9.130, -9.972), top tip y 9.98 | GEM / **Glass**, T 0.15 | The big faceted emerald crest (a diamond facing the runner and the plaza). Its lower tip is seated 0.33 into the base |
| 11 | `EmblemBadge` | 3.0 x 1.2 x 0.2 | (0, 0.48, -9.438) | PLATINUM / Universal | Plaque on the front face of the front console bar (z -9.338), facing the plaza and spawn |
| 12 | `hood_emblem` | 0.8 x 0.8 x 0.3, rotated 45 deg about Z | (0, 0.48, -9.638) | GEM opaque / Weld | Emerald diamond on the plaque, seated 0.05 into it |

Rune positions:
- Per rail: z = -4.288, -2.851, 0.122, 1.559, 4.532, 5.969.
- The three spans are stanchion -> post 1, post 1 -> post 2 and post 2 -> post 3, each 3.41 long with 0.54 gaps.

**Rune order (= chase order, because they're parented in this order):**
- `rune_1..6` = LEFT rail, back to front (z 5.969 down to -4.288).
- `rune_7..12` = RIGHT rail, front to back.
- So the white glint runs up the left rail and down the right: a clockwise loop around the runner, about 2 s per lap.

## Animation hooks (TreadmillClient, no scripts)
- `rune_1..12` (12): steady bright emerald inlays when idle. While running, one white glint chases around both rails
  and the others dim slightly.
- `sparkle_` (8): 6 rail crystals + 2 console crystals. They twinkle 55-110 % all the time, faster while running.
- `screen_gem`: the crest emerald pulses toward white while running.
- `hood_emblem`: the front emblem diamond pulses toward white while running.
- Kept back for higher tiers on purpose: halo, wings, flames, screen bars, orb.

## Lights (3, all PointLight, `Shadows = false`)
| Light | Parent | Colour | Brightness | Range |
|---|---|---|---|---|
| `CrestLight` | `screen_gem` | (90, 255, 170) | 1.5 | 10 |
| `RailLight_L` | `sparkle_RailL_2` | (90, 255, 170) | 1.0 | 7 |
| `RailLight_R` | `sparkle_RailR_2` | (90, 255, 170) | 1.0 | 7 |

The rail lights sit at the mid posts (z 3.045). They throw a soft green glow on the belt and the runner. The label
GUI has LightInfluence 0, so it isn't tinted.

## Progression
**vs T6 (x10)**, which is a bare gold/black chassis with no decor, no motion, no lights and a too-bright screen:
- **New silhouette element:** full-length side rails with gem-crowned posts. The side profile grows from a 0.9-high deck
  to a 3.7-high rail line along the whole 13-stud length, and the console gains corner crystals and a crest. The top
  rises from 8.5 to 10.0.
- **First animated life in the ladder:** 4 hook types and 22 animated parts, against none for T6.
- **First lit tier:** 3 green lights.
- **Richer palette:** onyx + two emeralds + platinum + translucent gems, against flat 2-colour.

**vs tiers 1-6:**
- No other tier is green-blue jewel tone with platinum. T4 is matte yellow-grass green (hue ~105-110 deg) on green
  frames, no trim and no gems.
- T1's cyan (hue 180-200 deg) stays clearly bluer than emerald (155 deg).
- T6's gold is gone completely.

**Restraint (it stays the smallest new step):**
- No arch, tall console, fins/wings, crown/halo, flames or pylons. Those are the T8-T11 steps.
- Everything sits at y <= 3.8 except the console crystals and the crest.
- 42 decor parts, leaving about 40 parts of headroom for the four tiers above.

## Limits (how each hard limit is respected)
- **Functional parts:** Conveyor / Belt / Zone / Blocker / FrontStop are not touched.
- **Attributes:** Name, Tier 7, TierName "x12", SpeedPerSecond 600000 and LabelHeight 10.6 stay. Add
  `SetAttribute("Theme", "Emerald")`.
- **Chassis:** only Color and MaterialVariant change. Collision stays as it is.
- **Envelope:**
  - Decor |x| max is 5.688 (the stanchions). The chassis grips stay at 5.793.
  - z ranges from -10.57 (crest gem's lowest corner) to 7.955 (rail end).
  - Top y is 9.98 (crest tip). Lowest decor y is -0.12 (the badge), above the floor.
- **Upgrade-sign keep-out (|x| > 6.4, 4 <= z <= 8.6):** nothing in decor goes past |x| 5.688.
- **Runner Zone (|x| <= 3.1, 0.6-6.6, |z| <= 7.1):** all decor is at |x| >= 4.688 except the crest and emblem, which
  are at z < -9.
- **Runner camera corridor (|x| <= 5, y >= 4.5, z >= 1.5):** the rail parts overlap |x| <= 5, but their top is 3.77
  (crystal tip at 110 %). Below 4.5, so I expect no WARN.
- **Over-head box (|x| <= 3.5, 6.6-12, -7 <= z <= 1.5):** empty. The crest is at z < -9.2.
- **Label screen:**
  - The face is SCREEN DEEP, luminance 0.23, opaque.
  - The only new 20 deg-tilted parts at z < -6 are the crest pieces: base 0.84, prongs 0.17 each, gem 1.21 stud².
    All are far below the bracket (6.2) and below 75 % of the frame (22.4), so the label stays on the face.
  - The console crystals (ToOrientation X 35 deg) and the emblem (no X tilt) are outside the 14-26 deg window.
- **Banned items:** no Neon, ForceField, Scripts, VFX, Decals, MeshParts or Unions. All parts are Part blocks.
  The rotated cubes and diamonds are plain blocks.
- **Materials:**
  - No SmoothPlastic, and every Plastic part has a variant.
  - Accent materials: 1 (the Glass `screen_gem`), well under the 15 % cap.
- **Lights:** 3, with Shadows off.

## Estimated part count
| Group | Parts |
|---|---|
| Chassis | 26 |
| Decor | 42 |

Decor breakdown:
| Decor group | Parts |
|---|---|
| Stanchions | 2 |
| Rail bars | 2 |
| Posts | 6 |
| Collars | 6 |
| Rail crystals | 6 |
| Runes | 12 |
| Console crystals | 2 |
| Crest (base + 2 prongs + gem) | 4 |
| Emblem (badge + gem) | 2 |

**Total about 68 visible parts** (aim <= 110, FAIL at 140).

## Phase B build notes and risks
- **How I'll build it:**
  - One `execute_luau` builder that only touches `Tier7_x12`.
  - It finds chassis parts by their belt-space AABB, never by name (they're all called "Part").
  - It parents the runes in chase order, then runs `T.refresh(7)`.
  - Captures: all 8 presets plus `side_hi`, ids `T7_<preset>_v<n>`.
- **Risk: chase order on clients.** The chase follows client GetDescendants order. If replication ever reorders the
  runes, the glint just flashes in a scrambled order. It still reads as gem glints, and nothing breaks.
- **Phase B tuning I may do, and will report:**
  - Gem variant (Weld or Universal).
  - Crystal size ±0.1.
  - ONYX may need a touch more green, if it reads as plain navy under the lab ambient.
- **Questions for the plan reviewer:**
  1. Trim: platinum, as chosen to keep T7 clearly apart from T6's gold, or gold?
  2. Rail height: low, top 2.8 plus crystals to 3.7, as chosen, or grip height (about 3.8, a continuous handrail line)?
