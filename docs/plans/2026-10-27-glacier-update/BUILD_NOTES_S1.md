# Glacier update, stage S1: build notes

**Date:** 2026-10-27.
**Studio:** `a7ffd071-09f7-457b-87ec-ff2b0334fe81` ([🎃] Slingshot for Eggs).
**Builder:** S1 Studio builder.

**Status (v2, after the visual review FIX 6/10):** area 7 is built, fixed, and PARKED in `ServerStorage._GlacierStage`.
- It is not in the workspace, so nothing shows past the end wall and nothing changes for players.
- Nothing was saved or published.
- **The owner must File > Save** (and Publish whenever they choose; S1 is invisible to players).
- Studio is in Edit. `TestFreshSave` = false.

## 0. Visual-review fixes (v2)

Review: `AREA7_VISUAL_REVIEW.md`.

| Item | Done |
|---|---|
| **M1** walls/floor contrast | All 13 wall parts (incl. EndWall) (165,210,240) -> **(112,168,216)**; 3 sills (185,222,245) -> **(150,196,228)**; VipHideout Back + Roof -> **(96,150,200)**. Floor (210,240,252) and gold trim unchanged. **Also changed:** the 4 `VipFiller`s go to (96,150,200) too. They had the same colour as the Roof and form the same left-wall face, so they stay one colour. |
| **M2** trench rims | RimA/RimB -> **(40,140,215)**, height 0.3 -> **0.6** (same centre y 0.2), CanCollide off. TrenchBottom unchanged. |
| **M3** wall frost | 6 `WallCrystal` clusters (PropLibrary Crystal4) grow out of the wall faces, tilted 35° up. **Sizes:** 3.2-3.8 studs, points (120,205,255) SmoothPlastic, bases snow (238,246,252). **Placement:** right wall z -2575 / -2700 / -2810, left wall z -2510 / -2745 / -2850, at y 14-23.6. In world space they reach |x| 56.4..60.4 (embedded ~0.4 in the wall); at least 27 studs from every VIP door span. **Flags:** CastShadow off, CanCollide/Query/Touch off, Anchored, no Neon. |
| **N1** boulders | All 5 rocks tinted **(200,222,236)** and sunk 1 stud. |
| **N3** Glacier material on wall caps | **Skipped.** There are no separate cap parts, so this needs new slabs, and the raycast renderer can't show materials, so I can't judge "if it looks right". |
| **M5** egg render | Done; see section 5. Verdict: **the egg stands out strongly**. I also made 2 small tweaks to the egg (see below). |
| **M4** park | `Area7_Glacier` moved to `ServerStorage._GlacierStage.Area7_Glacier`. **Tags:** stripped while parked (17 instances) and kept in `_StageTags`. **`_GlacierStage.Preview`** (show / hide / toggle) is for owner previews. The S2 opener moves it back first (step A0, dry-run OK). |

**Box collision fidelity on the wall crystals:** the review asked for it, but **I could not set it from a script on parented parts** (42/42 refused). They stay Hull like every other runway crystal. They have CanCollide/Query/Touch off, so this has no physics effect.

## 1. What I built

### `Area7_Glacier` (Folder; now parked in `ServerStorage._GlacierStage`)
**Folder attributes:**
- `Area = 7`
- `AreaName = "Glacier"` (same short form as the other folders; nothing reads it)
- `Emoji = "🧊"`
- `Closed = true` (new; see section 2)
- `BuiltBy`

**The shell is a part-for-part mirror of Area6_Celestial, shifted z -400.** All of it is Plastic with studs, like every other area.

| Folder | Celestial (BaseParts/MeshParts) | Glacier | Notes |
|---|---|---|---|
| Floor | 2 / 0 | 2 / 0 | FloorA (0,-4,-2557), FloorB (0,-4,-2763), 120x8x194, (210,240,252) pale ice, top Studs |
| Gap | 4 / 0 | 4 / 0 | TrenchBottom (0,-7.5,-2660) navy (25,55,100); rims (40,140,215) 0.6 tall; HideZone (0,-3.5,-2660), `Area = 7`, tag `Gap` |
| Walls | 16 / 0 | 16 / 0 | (112,168,216), sills (150,196,228); own EndWall 160x48x20 @ (0,16,-2870) |
| CreatureLine | 14 / 0 | 14 / 0 | z -2480 .. -2844, `Area = 7`, tag `CreatureSpot` (nothing reads it; kept for parity) |
| VipHideout (Model) | 23 / 0 | 23 / 0 | pivot (-60,12,-2660); doors z -2575 / -2688.3 / -2801.7; floor (170,225,250), back/roof/fillers (96,150,200), gold trim; `Area = 7` on model + VipGate |
| VipRoomsB (Model) | 15 / 0 | 15 / 0 | doors z -2518.3 / -2631.7 / -2745; gold trim |
| AreaZone | 1 / 0 | 1 / 0 | 120x40x400 @ (0,20,-2660), tag `Area`, `AreaName = "Frostfall Glacier"`, `Emoji = "🧊"`, `TextColor = (170,235,255)`, colour (150,220,255) |
| Decor | 237 / 207 (18 items) | 194 / 166 (20 items) | StartLine (mirror, sits under the old EndWall) + 13 side props + 6 WallCrystals |
| Ground | 75 / 25 (28 items) | 54 / 42 (12 items) | 6 small crystals + 6 flat snow patches |
| **Total** | **387 / 232** | **323 / 208** | |

**Decor:** 25 props (13 big, 6 small, 6 on the walls) plus 6 flat snow patches. It reuses `ServerStorage.PropLibrary` meshes; there are no Toolbox inserts.
- **Big props (13):**
  - 8 crystals (Crystal1/2/3/5, 8.5-10 studs), points in ice blue (120,200,245) / (165,225,250), bases snow (238,246,252)
  - 5 frozen boulders (Rock / Rock2, 6-7 studs, (200,222,236))
  - positions: |x| 48.5..58.8, at least ~12 studs in z from every VIP door
- **Small props (6):** Crystal4, 2.5-3 studs, at |x| 56-58.
- **Wall crystals (6):** see M3 above.
- **Snow patches (6):** 9 x 0.2 x 18-24 at x ±51 (|x| 46.5..55.5), colour (240,249,255).
- **Rules followed:**
  - Nothing at |x| < 46 except the shell and the flat StartLine. Eggs use |x| <= 42.
  - No trees, bushes, seats, signs, Neon or lights.
  - Every decor part has CanCollide/CanQuery/CanTouch off and is Anchored.
  - Scripts and tags were stripped from the clones.
- **Gotcha:** the PropLibrary crystal points are **Neon**. I switched them all to SmoothPlastic, like the 632 crystal points already on the runway.

**One deliberate difference from the mirror:**
- Two Glacier wall pieces would sit inside the old Area6 EndWall (z -2460..-2480): `WallL_1` and the 40.3-long `WallR`.
- Their top faces at y 40 would z-fight with the EndWall's top.
- In S1 they start at z -2480 (lengths 10 and 20.33).
- Their full size and CFrame are stored as attributes `S2Size` / `S2CFrame`. The S2 map step restores them.

### `ServerStorage.Assets.Eggs.GlacierEgg` (Model)
It is a clone of CelestialEgg, recoloured:
- **Layers:** Glass, transparency 0.12, banded sapphire (30,70,160) / (38,88,185).
- **Core:** `GlacierEgg_Core` (12,28,75).
- **Band:** `FrostBand` (was `GoldBand`), Glass, ice-cyan (120,220,255).
  - **v2:** moved to the equator (y 2.4, between the two widest layers) and widened to 3.32. It now shows as a ring; before it sat hidden inside the second layer.
- **Speckles:** 2 `Frost` parts (were Neon `Star`).
  - **v2:** SmoothPlastic (240,250,255), so they read as frost, not a glow.
- **Unchanged:** the wood Nest, and `GlacierEgg_Shell`, the invisible 3.2x6x3.2 sizing shell (EggSpawner / BaseHatchery find `<Kind>_Shell`).
- **Not registered:** it has **no `Area` attribute**, only `PendingArea = 7`. EggSpawner builds `EGG_FOR_AREA` from `Area`, so `EGG_FOR_AREA[7]` is nil and nothing spawns.

### Inert data entries (nothing reads them while no Glacier egg exists)
| Script : line | Change |
|---|---|
| `SSS.EggSpawner` 36-41 | 7th KG entries: `KG_MAX` 800000, `KG_SKEW` 2.0, `KG_LUCKY_ODDS` 180, `KG_LUCKY_MAX` 10000000 (+ a 2-line comment) |
| `SSS.EggSpawner` 101-102 | areas loop skips runway folders with `Closed == true` (data-driven guard for this and any future area) |
| `RS.CreatureConfig` 107 | `AREA_HATCH = {0.02, 0.04, 0.1, 0.25, 0.5, 1, 2}` |
| `RS.CreatureConfig` 160-161 | `AREA_INCOME = {20, 120, 300, 1800, 10000, 55000, 300000}` (+ a comment line) |
| `SSS.Analytics` 34 | `A.AREAS` + `"Glacier"` (name translation only) |

**Not touched (S2), on purpose:**
- UpgradeConfig, RebirthConfig (AREA_NAMES / LADDER / MAX), IndexConfig + Index UI
- Streak / Playtime / StarterPack / ChatAnnounce, CreatureConfig pets and odds
- WaveConfig.StartZ, WeatherConfig.AREAS
- Map.Bounds, Area6 EndWall
- Lighting

## 2. Keeping it closed

**Parked (v2), so no runway loop sees area 7 at all:**
- SafeBoxes are back to 48.
- `GetTagged("Area")` returns 6 zones.
- There is no `bounds[7]` and no zone 7 for `CurrentArea`.

The checks below were done in v1 with the folder IN the workspace (still Closed). They still hold for owner previews and for S2.

| System | With Area7_Glacier present | Action |
|---|---|---|
| EggSpawner `areas` (line 99-106) | skipped: no template with `Area = 7`, and the folder is `Closed` | guard added (line 102) |
| EggSpawner AdminEggs / lucky rain / EggAssist `areaAt` | loop over `areas`, so area 7 is never in it | none |
| EggSpawner `CurrentArea` zones (line ~905) | zone 7 is listed; nobody can stand there | none |
| `WaveConfig.buildSafe` | +8 safe boxes in Glacier (56 total), unreachable | none |
| WaveServer VipGate loop / MapGuard VipSafe rooms / VipClient doors | pick up the Glacier VIP parts, unreachable | none |
| AreaTitleController (tag `Area`) | zone 7 is listed; only shows when you are inside | none |
| WeatherServer `bounds` | `bounds[7]` exists; random picks use `WeatherConfig.AREAS = 6`; AdminServer passes `area = nil` | none (S2: AREAS = 7, see checklist B6) |
| UFO / Meteor clients | area numbers come from the server (1-6) | none |
| Analytics `A.AREAS` | the 7th name is only used when a Glacier egg is grabbed | none |
| IntroCutscene, Trailer, HubV2Kit | only Area1 / fixed shots / hub | none |

**Why nobody can enter (even during a preview):**
- The old EndWall at -2470 stays in place.
- `Map.Bounds.Runway_End` (1000 tall) stays in place.
- `Runway_L_2` / `R_2` end at -2481.
- `WaveConfig.StartZ` stays at -2500.

## 3. Scripts touched + backups

**Backups:** `ServerStorage._Backup_GlacierS1`
- **`Before`:**
  - EggSpawner (Disabled), CreatureConfig, Analytics: all untagged, each with an `OriginalPath` attribute.
  - `Area7_Glacier_v1` and `GlacierEgg_v1`: the S1 state before the review fixes, tags stripped.
  - `S2_OpenMap_v1`: the superseded opener, commented out.
- **`UntouchedState`:** a StringValue recording Runway_End, Runway_L_2/R_2, the Area6 EndWall, StartZ and TestFreshSave before S1.
- **`Revert`:** `require(game.ServerStorage._Backup_GlacierS1.Revert:Clone())()`. It removes Area7_Glacier (workspace) and `_GlacierStage` (parked), removes GlacierEgg, and restores the 3 scripts.
- **`S2_OpenMap` (v2):** the S2 map step (checklist section A); step A0 brings the folder back from the stage.
  - `(true)` is a dry run and was OK with the folder parked.
  - `(false)` applies it.

**`ServerStorage._GlacierStage`:**
- `Area7_Glacier`: parked.
- `Preview`: `local P = require(game.ServerStorage._GlacierStage.Preview:Clone())`, then `P()` toggles, `P.show()`, `P.hide()`, `P.where()`.
  - The hide → show → hide round trip was tested: the 17 tagged instances were stripped, restored and stripped again.

## 4. Tests

**Edit (unit):**
- CreatureConfig (required as a clone): `AREA_INCOME[7] = 300000`, `AREA_HATCH[7] = 2`, areas 1-6 unchanged, no `GlacierEgg` in `Areas`.
- `WaterWallTests.pure()`: **19 / 0**.
- Validator on Area7:
  - 0 unanchored parts
  - 0 decor/ground parts with collide/query/touch on (the StartLine mirrors Celestial's flags)
  - 0 in the lane, 0 Neon, 0 scripts/lights/emitters

**Play 1 (v1, folder in the workspace, Closed). TestFreshSave was checked true in Edit right before Start; I started and stopped the session myself:**
- **Console:** 0 errors on server and client.
- **Eggs:** areas 1-6 have 7/6/6/6/6/6 eggs, Glacier 0. After 224 s it was the same; farthest egg z -2439.9.
- **Waves:** running.
- **Lv25 launch:**
  - How I drove it: the real `Aim` + `LaunchRequest` remotes, then the client release physics replicated.
  - Result: it **landed on Celestial FloorB at z -2335.8** (flight 7.67 s).
- **End wall:**
  - Walking and jumping stopped at **z -2459.5**.
  - MapGuard sent the player back from the top of the wall (y 44) and from y 300.

**Play 2 (v2, folder parked; TestFreshSave checked true right before Start):**
- **Server:** 0 errors.
- **Client:** 0 errors; only the TopbarPlus notice.
- **Area7 visibility:** not in the workspace on the server or the client.
- **Eggs:** 7/6/6/6/6/6; farthest z -2405.5.
- **Waves and SafeBoxes:** waves running; SafeBoxes 48; 6 `Area` zones.
- **Afterwards:** Play stopped, `TestFreshSave` back to **false**, Studio in **Edit**.

**Left untouched:** Bounds / EndWall / StartZ, re-checked after both tests.

**Not tested:**
- The phone banner, because area 7 is closed.
- A real touch/mouse launch.

## 5. Renders (raycast renderer `HubV2Kit.Render`; player eye 5 studs, FOV 70)

All renders are in `docs/plans/2026-10-27-glacier-update/s1_renders/`.

**v2, after the fixes:**
- `g1_entrance.png`, `g2_trench.png`, `g3_sidewall.png`, `g4_vip.png`, `g7_top.png`
- `g8_wallcrystal.png`: a right-wall crystal at z -2700.

**Parked:**
- `g6_arc_over_end_parked.png` (the v1 arc view) and `g6b_apex_view_parked.png` (from about the Lv25 apex, y 590): nothing past the pink end wall.

**Egg (M5):**
- `egg_glacier_near.png`, `egg_glacier_mid.png`: GlacierEggs at x 0 / -40 / +40 on FloorA, scales 1.3 / 1 / 2.2 (about 3K / 1K / 50K KG).
- `egg_glacier_closeup.png`, `egg_glacier_top.png`
- `egg_celestial_compare.png`: today's CelestialEgg next to a GlacierEgg on the Celestial floor.

**Earlier frames:** `*_v1.png` are the frames the review judged; `g5_celestial_end.png` is unchanged.

**Egg verdict:** it **stands out strongly**.
- The dark sapphire body on the pale floor is the highest contrast of any egg/floor pair here. It reads clearly at 25 and 55 studs, and also on the shadowed left side.
- The ice-cyan equator ring and the white frost tip read against the dark body.
- On the Celestial floor it also pops more than today's Celestial egg (grey-on-cream).
- Limit: the renderer has no Glass reflections or lighting, so the in-game egg will be a bit lighter and shinier. The contrast margin is big enough that this should not matter.

**Renderer limits:**
- Flat shading with a fixed sun, so the left side is always in shadow.
- No textures, studs, GUIs or real materials.
- The renders show layout and colour only.

## 6. Unsure / for the lead and the reviewer

1. **Wall crystals look small.** At the requested 3-4 studs, the 6 wall crystals read as small accents on a 48-stud wall (g8). If the reviewer wants more presence, 5-6 studs or pairs per spot is the next step.
2. **Wall material:** Plastic with studs (house style) instead of the plan's "Glacier" material. N3 (Glacier caps) was skipped, see section 0.
3. **Decor sources:** PropLibrary crystal and rock meshes, not the plan's block-part recipes. They match the other areas' crystals.
4. **VipFiller colour:** set to the Roof colour (96,150,200) so the left wall face stays one colour. The review named only Back and Roof.
5. **CreatureLine:** mirrored for parity. Nothing reads it.
6. **Folder `AreaName`:** set to "Glacier". The banner title "Frostfall Glacier" lives on the AreaZone. The plan's D.3 question (Frostfall vs Frost) is still open.
7. **WeatherServer:** has no `Closed` guard. It is not needed (parked, and nothing requests area 7).
8. **Owner OK still pending:** StartZ -2900 (global wave timing) is in the S2 checklist.
9. **Water vs Glacier lineup check (M1 note):** not done; it needs the S2 lineup.
