# Tier 7 `Tier7_x12` (x12, 600K/s): EMERALD: BUILD NOTES (Phase B)

Built 2026-10-12 in `ServerStorage.Assets.Treadmills.Tier7_x12` exactly as PLAN.md was approved. PLAN_REVIEW.md's x12
section is APPROVED with notes N1-N4. Bay 7 was refreshed with `T.refresh(7)` after every step.

## Final validator output
```
== Tier7 Emerald: 0 FAIL, 0 WARN
ok   label screen = Part 6.1x3.1 colour (0,78,50) lum 0.23, 7 tilted parts
ok   68 visible parts (42 decor), 1 accent-material parts, 3 lights; animation hooks: sparkle_ x8, screen_gem x1, hood_emblem x1, rune_ x12
```
- **7 tilted parts:** the chassis bracket, face and frame, plus the 4 crest pieces. The crest pieces are 0.17-1.21
  stud². The label stays on the face.

## What was built
**Step 1: chassis recolour (26 parts, size and place untouched).**
- Chassis parts were matched by size and belt-space position, not by name.
- Colours and variants follow PLAN.md exactly, except the platinum shade (see deviations).
- `Theme` = "Emerald". Tier, TierName, SpeedPerSecond and LabelHeight 10.6 are unchanged.

**Step 2: decor (42 parts)** in `Decor`, all Anchored, with CanCollide/CanTouch/CanQuery false:
| Group | Parts |
|---|---|
| `RailStanchion_L/_R` | 2 |
| `RailBar_L/_R` | 2 |
| `RailPost_L1..3/R1..3` | 6 |
| `RailCollar_L1..3/R1..3` | 6 |
| `sparkle_RailL_1..3/R_1..3` | 6 |
| `rune_1..12` | 12 |
| `sparkle_ConsoleL/_R` | 2 |
| `ScreenCrestBase` + `ScreenCrestProng_L/_R` + `screen_gem` | 4 |
| `EmblemBadge` + `hood_emblem` | 2 |

- Sizes and positions are exactly PLAN.md's.
- The crest is built in the screen frame's local space, so it sits flush on the tilted top face.

**Lights (3 PointLights, Shadows off), colour (90, 255, 170):**
| Light | Parent | Brightness | Range |
|---|---|---|---|
| `CrestLight` | `screen_gem` | 1.0 | 8 |
| `RailLight_L` | `sparkle_RailL_2` | 1.0 | 7 |
| `RailLight_R` | `sparkle_RailR_2` | 1.0 | 7 |

**Rune order**, read back from the template (belt x, z):
```
1:(-5.19,5.97) 2:(-5.19,4.53) 3:(-5.19,1.56) 4:(-5.19,0.12) 5:(-5.19,-2.85) 6:(-5.19,-4.29)
7:(5.19,-4.29) 8:(5.19,-2.85) 9:(5.19,0.12) 10:(5.19,1.56) 11:(5.19,4.53) 12:(5.19,5.97)
```
- This runs up the left rail back to front, then down the right rail front to back: a clockwise loop of about 2 s
  (N1).

## Deviations from the plan (small; all in the pre-approved spirit)
1. **PLATINUM changed from (212,220,224) to (192,202,208)** on all 21 platinum parts.
   - Why: in the lab sun the first shade blew out to pure white (`T7_spawn_v1`, `T7_hub34_v1`). It could have read as
     Frost's snow white next door.
   - The deeper shade reads as clear metallic silver in shade and stays bright in sun (`T7_spawn_v2`, `T7_hub34_v2`).
2. **`CrestLight` lowered from Brightness 1.5 / Range 10 to 1.0 / 8.**
   - This follows N2 / R3 as a safety margin for darker hub lighting.
   - At 1.5 it didn't visibly lift the face in `runner` in daylight.
3. **No change needed** to the gem variant (Weld kept; its diagonal line reads as a facet), the crystal sizes or ONYX
   (it reads as dark green-black, not navy).

## Ladder check (PLAN_REVIEW §1)
| Check | Target | Built |
|---|---|---|
| Solid top | ~8.5 | Screen frame 8.53. The crest setting reaches 8.86 (base) and 9.33 (prongs) |
| Static peak | 10.0 | 9.98, the crest gem tip |
| Anim max | 10.1 | 9.98. `screen_gem` only changes colour |
| Visible parts | 64-72 | 68 |
| Animated parts | ~22 | 22: 12 runes + 8 sparkles + 2 colour pulses |

## R1 / R2 / R3 checks
**R1 rear walkway (|x| <= 4.1, z >= 7, 0.3 <= y <= 6.6):** empty. The nearest decor is the rails at |x| >= 4.69
(checked in code).

**R2 extremes (sparkles at 110 %, AABB in code):**
| Parts | y range | \|x\| range |
|---|---|---|
| Rail crystals | 2.43 .. 3.77 | 4.64 .. 5.73 |
| Console crystals | 4.35 .. 5.87 | 4.57 .. 5.81, at z -8.3 |

- All of this is below the 4.5 runner corridor, outside the Zone, the head box and the sign keep-out, and inside
  |x| 7.4.
- Decor overall: max |x| 5.81, max y 9.98.

**R3 label with the lights on:** `T7_runner_v2` and `T7_runner_v4` show "+600K / sec" in clear yellow on the deep
emerald face (lum 0.23). The face is not lifted.

## Captures
All taken under `T.lock("T7")`, one at a time, then `T.unlock("T7")`.

**Final state (v2 set):**
| Preset | Capture id |
|---|---|
| spawn | `T7_spawn_v2` |
| hub34 | `T7_hub34_v2` |
| eye | `T7_eye_v2` |
| side | `T7_side_v2` |
| sideHi | `T7_sideHi_v2` |
| runner | `T7_runner_v4` (`T7_runner_v3` is the same view, taken before the mock label rendered) |
| rear34 | `T7_rear34_v2` |
| close | `T7_close_v2` |
| lineup | `T7_lineup_v2` |

**First pass (before the platinum and crest-light tweak):** `T7_spawn_v1`, `T7_hub34_v1`, `T7_runner_v1` (label not
yet rendered), `T7_runner_v2`, `T7_rear34_v1`, `T7_side_v1`, `T7_sideHi_v1`, `T7_eye_v1`, `T7_close_v1`,
`T7_lineup_v1`.

**Phase A study:** `T7A_*`, listed in PLAN.md.

What the captures show:
- **spawn / hub34:**
  - The emerald faceted screen slab with its crown gem reads at once from the plaza.
  - Onyx frame and bars, with silver posts, plaque and feet.
  - Emerald plinth line at floor level.
  - Rails with gem-crowned posts along both sides.
- **runner:**
  - The rails frame the belt in the lower corners and keep their gems in view.
  - The console crystals flank the screen.
  - The crest sits above the label.
  - Nothing is over the head or in the corridor.
- **rear34:** the two-tone jewel belt, rails with chase inlays and collared crystals. The upgrade sign is fully clear.
- **side / sideHi:** the long low rail line (posts, collars, crystals, inlays). The stanchions visibly carry the
  handle grips.
- **eye / close:** the platinum plaque with the emerald diamond, the crest prongs gripping the Glass gem, and the
  crystals on the handle caps.
- **lineup:** clearly richer than x10 next to it (all-green screen, crest, crystals, lights), and clearly quieter than
  the x14 Frost gate on its left.

## Anything unsure
1. **Mock-label render delay:** right after a `T.refresh`, the `runner` capture sometimes shows the face without text
   (`T7_runner_v1`, `T7_runner_v3`). A second capture shows it (v2, v4). This is a capture timing artefact, not a model
   issue.
2. **Crystal girdle overhang:** a rail crystal's widest ring is slightly wider than its 1.0 collar.
   - It overhangs by about 0.07 in z, 0.13 at the 110 % twinkle, over only about 0.1 of height.
   - It reads as a gem wider than its cup and touches nothing else.
3. **Chassis screen bracket:** it sticks out about 0.3 past the frame's back face, so from the plaza it shows as a
   silver plate on the emerald screen back.
   - It's a fixed chassis part; I only chose its colour (platinum, so it reads as a mount).
   - If the visual reviewer prefers, it can be EMERALD and blend into the slab instead (a one-line change).
4. **Live behaviour:** the runes/sparkles/pulses can't be watched in Edit mode (no Play allowed). The hook names and
   the rune numbering match TreadmillClient's rules, and the extremes were checked in code.

---

## Phase C (FIX), 2026-10-12
REVIEW.md verdict: FIX, with 1 MUST and 2 NICE. Both changed items are done. Nothing else changed: the gem overhang and
the platinum (192,202,208) stay as the reviewer approved them.

1. **MUST, done: the screen bracket** (chassis 2.162 x 2.853 x 0.985 at belt (0, 5.577, -8.927), tilted 20 deg).
   - Recoloured from PLATINUM Universal to **EMERALD DEEP (0, 100, 60) Plastic/Studs**. Colour and variant only; size,
     CFrame and collision are unchanged.
   - From the plaza it now reads as a tonal green mount on the emerald slab, and the slab reads as one jewel. No white
     "sticker" (`T7_eye_v5`, `T7_far55_v2`, `T7_hub34_v4`).
   - From the runner it is a green stem under the label, like T6's gold stem (`T7_runner_v5`).
   - It doesn't read as a hole, so no onyx fallback was needed.
   - Platinum parts: 21 -> 20.
2. **NICE, done: the crest gem.** After step 1, the Glass `screen_gem` still read pale mint/white against the sky from
   both ±45 deg plaza angles (`T7_hubMinus45_v1`, `T7_hubPlus45_v1`).
   - It is now **Plastic/Weld GEM (60, 230, 140), Transparency 0.1**. Same size and CFrame, and `CrestLight` stays
     inside.
   - It now reads as a translucent emerald that matches the rail crystals (`T7_hubMinus45_v2`, `T7_hubPlus45_v2`,
     `T7_close_v3`).
   - Accent-material parts: 1 -> 0.
3. **NICE (crystal overhang, platinum shade): kept as built.**

### Validator after Phase C (`T.refresh(7)` then `T.validate(7)`)
```
== Tier7 Emerald: 0 FAIL, 0 WARN
ok   label screen = Part 6.1x3.1 colour (0,78,50) lum 0.23, 7 tilted parts
ok   68 visible parts (42 decor), 0 accent-material parts, 3 lights; animation hooks: sparkle_ x8, screen_gem x1, hood_emblem x1, rune_ x12
```
- The ladder is unchanged: crest tip 9.98, 68 visible parts, 22 animated parts.

### Phase C captures
All taken under lock `T7`, one at a time, then unlocked.

**Final state (both fixes):**
| View | Capture id |
|---|---|
| eye | `T7_eye_v5` |
| hub34 | `T7_hub34_v4` |
| spawn | `T7_spawn_v4` |
| far front, 55 studs (camera [622, 9.6, -155] -> [622, 4.6, -100]) | `T7_far55_v2` |
| -45 deg plaza angle (camera [601, 7.6, -121] -> [622, 4.6, -100]) | `T7_hubMinus45_v2` |
| +45 deg plaza angle (camera [643, 7.6, -121]) | `T7_hubPlus45_v2` |
| close | `T7_close_v3` |

**After the bracket fix, before the gem switch:** `T7_eye_v3`, `T7_eye_v4`, `T7_hub34_v3`, `T7_runner_v5`,
`T7_spawn_v3`, `T7_far55_v1`, `T7_hubMinus45_v1`, `T7_hubPlus45_v1`.

### Note on the captures
The Phase C captures render with a visibly wider field of view than the Phase B ones (compare `T7_runner_v4` with
`T7_runner_v5`: the neighbour bays now show at the sides).
- `workspace.CurrentCamera.FieldOfView` still reads 70 and the viewport is still 1169x753. So this is a change on the
  Studio or capture-tool side, not in the model.
- Compare Phase C captures with each other, not with the v1/v2 sets.
