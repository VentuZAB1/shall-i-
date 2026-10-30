# AREA 7 PLAN: Frostfall Glacier (Area7_Glacier)

Status: PLAN ONLY. Nothing was built or changed in Studio.
Studio: `[🎃] Slingshot for Eggs` (studio_id a7ffd071-09f7-457b-87ec-ff2b0334fe81, placeId 97952972919986).
Facts: read-only `execute_luau` (Edit) + `script_read` / `script_grep`, 2026-10-27.
Spec: `docs/plans/2026-10-22-new-pets-glacier-area.md`. Owner answers (progress.md, 10-27): keep all 12 names, Frost Glacier theme, extend rebirths to R25.

Coordinates below are exact Studio values unless marked "proposal".

---

## 0. What Studio actually has (verified)

### 0.1 Area 5 and Area 6 (reference structure)

| Item | Area5_Shadow | Area6_Celestial (mirror source) |
|---|---|---|
| Folder attrs | Area=5, AreaName=Shadow, Emoji=🌑 | Area=6, AreaName=Celestial, Emoji=✨ |
| Z span | -1660 .. -2060 | -2060 .. -2460 |
| Floor | FloorA (0,-4,-1757) + FloorB (0,-4,-1963); 120x8x194; Plastic (75,72,90) | FloorA (0,-4,-2157) + FloorB (0,-4,-2363); 120x8x194; Plastic (255,245,215); top=Studs, front/left=Smooth (verified) |
| Gap (trench) | TrenchBottom 120x3x12 @ (0,-7.5,-1860), HideZone 120x5x11 @ (0,-3.5,-1860) (transparent, the safe box), RimA/RimB 120x0.3x1 @ z -1853.5 / -1866.5 | TrenchBottom 120x3x12 @ (0,-7.5,-2260) Plastic (153,147,129), HideZone 120x5x11 @ (0,-3.5,-2260) transparent, RimA/RimB 120x0.3x1 @ z -2253.5 / -2266.5 gold (255,215,0) |
| Walls | 15 parts, Plastic (40,22,62); WallL x=-70 (20 thick, 48 high) | 16 parts, Plastic (235,130,235); WallL_1 z-2075, WallL_2 z-2445 (x=-70); WallR x=70 pieces; **EndWall 160x48x20 @ (0,16,-2470)** |
| Right/left doors | Door frames at x=-70..-80 | 3 door frames on the right wall at z -2345 / -2231.7 / -2118.3 (6x48x36 + 14x16x36 header + 14x8x36 sill) |
| AreaZone | Part 120x40x400 @ (0,20,-1860), transparent, no collide/query/touch, tag `Area`, TextColor (180,90,255), colour (170,80,255) | Part 120x40x400 @ (0,20,-2260), tag `Area`, TextColor (255,210,90), colour (255,215,0) |
| VipHideout (LEFT, Model) | 3 VipDoor + 3 VipSafe + Floor/Back/Roof + VipGate | Model pivot (-60,12,-2260). Floor 14x8x340 @ (-67,-4,-2260); Back 6x48x340 @ (-77,16,-2260); Roof 14x16x340 @ (-67,32,-2260); VipGate 1x24x340 @ (-60,12,-2260) transparent, CanCollide false; 3 VipDoor 0.4x24x36 @ x=-60, z -2175 / -2288.3 / -2401.7 (transparent, no collide/query/touch); 3 VipSafe 14x24x36 @ x=-67 same z; 4 VipFiller 14x24 @ x=-67 (z -2424.8 len 10.3, -2345 len 77.3, -2231.7 len 77.3, -2123.5 len 67); 9 VipTrim gold 1x23x1 / 1x1x36 @ x=-60.2 |
| VipRoomsB (RIGHT, Model) | — | Model pivot (66.8,12,-2231.7). 3 VipDoor 0.4x24x36 @ x=60, z -2345 / -2231.7 / -2118.3; 3 VipSafe 14x24x36 @ x=67; 9 VipTrim gold @ x=60.2 |
| CreatureLine | 14 Spot parts 6x0.6x6 @ x=0, z -1680 .. -2044 step 26 (skips trench) | 14 Spot parts @ x=0, z -2080 .. -2444 step 26 (skips trench). **No script reads CreatureLine (0 hits).** |
| Ground | 106 descendants: Patch x18, Crystal x5, Model x4, S19 x2, S31 x3, Mushrooms x5 | 75 BaseParts/models: Patch x16 (17.5x0.2x16.9, Plastic, cc off), Crystal x3, Model x5, S19 x2, S28 x1, S31 x1 |
| Decor | 169 desc: TreeTilt x8, Pine x7, Crystal x12, Rock x5 | 237 BaseParts, 17 models: TreeRound x7, Blossom x4, Crystal x6, StartLine part. x range about ±47..56 (the side) |
| Part totals (BaseParts / MeshParts) | 330 / 186 | 387 / 232 (Area1 281/129, Area3 654/474 = heaviest) |

Other facts:
- Area6 shell (Floor 2 + Gap 4 + Walls 16 + CreatureLine 14 + VipHideout 23 + VipRoomsB 15 + AreaZone 1) = 75 BaseParts. Ground+Decor = 312.
- Surfaces: floor top = Studs, floor front/left = Smooth; walls top/front = Studs. Studs-on-Plastic is the house style.
- `workspace.StreamingEnabled = true`. `Map.Bounds` is a Persistent Model.
- Every area folder is a plain Folder (not a Model).
- The Area folder's `Area` attribute is what the scripts read; AreaZone is found by name `AreaZone` and by CollectionService tag `Area` (6 tagged, 1 per area).

### 0.2 Bounds and end-of-runway objects (current)

| Object | Current value | Note |
|---|---|---|
| `Map.Bounds.Runway_End` | Pos (0,540,-2470), size 162x1000x22, CanQuery false, Transparency 1 | Invisible wall at the old end |
| `Map.Bounds.Runway_L_2` | Pos (-70,540,-1872.5), size 22x1000x1217 (z -1264 .. -2481) | Left side bound, last segment |
| `Map.Bounds.Runway_R_2` | Pos (70,540,-1872.5), size 22x1000x1217 | Right side bound |
| `Map.Bounds.Runway_L_1` / `_R_1` | Pos (∓70,540,-663), size 22x1000x1206 | Unchanged |
| `Map.Runway.Area6_Celestial.Walls.EndWall` | Pos (0,16,-2470), 160x48x20 | Visible end wall; must MOVE (see A.6) |
| `Map.Markers.TsunamiPlaceholder` | Pos (0,20,-2500), 160x40x40, transparent, attr Role=TsunamiStart | **Nothing reads it** (0 grep hits) |
| `Map.Runway.LaunchGate` | Pos (0,6.4,-61), 119.8x13.2x2 | Unchanged |

---

## 1. Systems that depend on the runway end or area count (grep-verified)

Legend: **AUTO** = loops over the runway at server start, no change needed if Area7_Glacier is built with the same attributes/tags. **CHANGE** = a hard-coded table or number that must be edited.

| System | Reads | Status |
|---|---|---|
| `ReplicatedStorage.WaveConfig` | `StartZ = -2500` (line 5, "far end of Celestial"), `EndZ = -62`, `HalfWidth = 60` | CHANGE: StartZ to -2900 (section C) |
| `ServerScriptService.WaveServer` | VIP gates loop over `Map.Runway` (lines 26-30); tutorial bounds Grass only (162-171) | AUTO |
| `WaveConfig.buildSafe` (trench + VipSafe + VipHideout boxes) | Loops `Map.Runway` children at server start (lines 143-163) | AUTO (SafeBoxes JSON, ~8 boxes per area) |
| `ServerScriptService.MapGuard` | `Map.Bounds` children at start (line 29); `VipSafe` in `Map.Runway` (line 42) | AUTO for VIP; bounds positions read at server start (A.5) |
| `StarterGui.AreaTitle.AreaTitleController` | CollectionService tag `Area` on AreaZone parts; reads AreaName / Emoji / TextColor | AUTO if the tag is copied (Clone copies tags) |
| `ServerScriptService.EggSpawner` areas loop | `Map.Runway` children with `Area` attr and `Floor` and `ServerStorage.Assets.Eggs` template for that Area (lines 96-103); zone detection lines 899-928 | AUTO for placement, but the 4 KG arrays and the egg template are CHANGE (section F) |
| `EggSpawner.rollWeight` | `area = math.clamp(area, 1, #KG_SKEW)` (line 43) | **Silent trap:** area 7 would use area 6 values unless the arrays get a 7th entry |
| `EggSpawner` AdminEggs / lucky rain | loops `areas` (line 623) | AUTO |
| `EggAssist` (new-player landing assist) | `areaAt(z)` over `areas` with `zone.Size.Z` (EggSpawner 793-798) | AUTO |
| `ServerScriptService.WeatherServer` | `bounds[n]` from AreaZone + Floor top (lines 61-74); random area = `Logic.nextArea(WeatherConfig.AREAS)` | AUTO bounds, CHANGE `WeatherConfig.AREAS = 6` (line 10) |
| `Weathers.UFO` / `Weathers.Meteor` | `WaveConfig.StartZ + 40` clamp (UFO 244-254) | AUTO (follows StartZ) |
| `ReplicatedStorage.Weathers.UFOClient` / `MeteorClient` | `workspace.Map.Runway:FindFirstChild("Area%d_%s")` with `RebirthConfig.AREA_NAMES[area]` (UFO 465, Meteor 418) | CHANGE: AREA_NAMES[7] must equal the folder suffix, so the folder is `Area7_Glacier` and the name is `"Glacier"` |
| `ReplicatedStorage.UpgradeConfig` | `AREAS` table (line 22-25) with z of each area start; `SLING_MAX = 25`; `SLING_MAX_RANGE = 2300`; `SLING_REBIRTH` 25 entries | CHANGE (section D.4 / F) |
| `ServerScriptService.UpgradeServer` | clamps SlingLevel to `U.SLING_MAX` (line 36); sets SlingMaxSpeed (line 37) | AUTO once SLING_MAX changes |
| `ServerScriptService.SlingshotServer` | launch speed = MinSpeed + (SlingMaxSpeed - MinSpeed) * power (lines 109-110), streams around landing (123-132) | AUTO. No speed cap in code. |
| `ReplicatedStorage.RebirthConfig` | `AREA_NAMES` (6), `LADDER` (20 entries, max area 6), `MAX_REBIRTH = 20` | CHANGE |
| `RebirthClientLegacy` line 425 | `IndexConfig.AREAS[req.area]` for colours | needs entry 7 in IndexConfig |
| `ServerScriptService.Analytics` | `A.AREAS` (6 names, line 34); funnels doc says "Rebirth 1 ... 20" (line 12) | CHANGE (Creator Hub funnel steps are edited by hand) |
| `ReplicatedStorage.CreatureConfig` | 6 eggs, `AREA_HATCH` (6), `AREA_INCOME` (6) | CHANGE. **Silent trap:** `AREA_INCOME[info.area] or 1` means a missing area 7 pays $1/s base |
| `ReplicatedStorage.IndexConfig` | `AREAS` (6, versions 2,2,2,3,3,3), `PORTRAITS` (per pet) | CHANGE |
| `IndexClientLegacy` line 131 | Tab y = 0.07 + (i-1)*0.142 per area | **Visible UI change:** tab 7 would sit at y 0.92..1.05 (off-screen). Needs re-spacing and an owner mockup |
| `ReplicatedStorage.StreakConfig` | `EGG_KG` (6), `SECRET_KG` (6), `EGG_ICONS` (6); `S.secretFor(area)` uses `pairs()` (lines 73-79) | CHANGE, and fix the non-deterministic secret pick (section G) |
| `ReplicatedStorage.PlaytimeConfig` | `C.petFor` skips `secret` pets (lines 42-52) | AUTO if Frostcrown Dragon is flagged secret |
| `ServerScriptService.ChatAnnounce` | colours from `IndexConfig.AREAS` (line 36); secrets always announced (line 69-71) | AUTO |
| `ReplicatedStorage.CreatureVFX` | `ELEMENT[name]` (lines 142-152); `AURA[ELEMENT[name] or "Celestial"]` (line 161) | CHANGE: new pets fall back to the Celestial aura unless added |
| `ReplicatedStorage.PetEventFX` | `PetEventFX.has(name)` | AUTO: no entry = no extra FX (safe default) |
| `StarterPlayer.StarterPlayerScripts.InventoryClient` | `EGG_ICONS` (22-29), `EGG_AREA` (30), `AREA_COLOR` (32-39, 6 colours) | CHANGE |
| `StarterPlayer.StarterPlayerScripts.SellClient` | `EGG_ICONS` + `EGG_AREA` (lines 37, 39) | CHANGE |
| `StarterPlayer.StarterPlayerScripts.HatchClient` | egg colour pair table (line 31) | CHANGE |
| `StarterPlayer.StarterPlayerScripts.PetsEggsUI` | egg icon table (line 42) | CHANGE |
| `StarterPlayer.StarterPlayerScripts.AdminBannerClient` | `AREA_NAMES` from RebirthConfig (line 171) | AUTO |
| `StarterPlayer.StarterPlayerScripts.VipClient` | every VipDoor in `Map.Runway` descendants (lines 47-49) | AUTO |
| `StarterPlayer.StarterPlayerScripts.SkyEnvironment` | camera-following 3x3 grid of 2048-stud cells at y -150 / -320 (covers about ±3072 studs around the camera) | No change. Covers z -2900 from anywhere near the runway |
| `StarterPlayer.StarterPlayerScripts.IntroCutscene` | END_Z = -62; only `Area1_Grass` | No change |
| Trailer (`ServerStorage.AdminUI.Trailer`) | fixed shots at z -660 etc. | No change (not verified in full) |
| Admin Abuse UI area dropdowns (AdminServer / AdminUI) | not verified | **Check before build** |

---

## A. GEOMETRY: `Workspace.Map.Runway.Area7_Glacier` (new Folder)

### A.0 Method
Area 7 is Area 6 shifted by **Z -400**, part for part. Every x, y, size and rotation stays the same. The shift is applied to each part's Z only.
- **Clone** the shell children: Floor, Gap, Walls (without EndWall), VipHideout, VipRoomsB, AreaZone. Put them in a new Folder `Area7_Glacier`, shift each by Z -400, then recolour per section B.
- **Do NOT clone** Ground or Decor. Those hold Celestial's TreeRound and Blossom models. Build Glacier decor from B.4.
- **CreatureLine: skip.** No script reads it. If kept for parity, use the Z list in A.8.
- Back up Area6's EndWall into `ServerStorage._Backup_Glacier.Before` before moving it (backup rule).
- Write in chunks of about 40-60 parts with `task.wait()` between chunks (StreamingEnabled, MCP freeze rule).

### A.1 Folder attributes
- `Area7_Glacier`: Area=7, AreaName="Frostfall Glacier", Emoji="🧊"

### A.2 Floor (Folder `Floor`, 2 parts, ALL CanCollide/CanQuery/CanTouch true, Anchored)
| Name | Size | Position | Material | RGB | Surfaces |
|---|---|---|---|---|---|
| FloorA | 120 x 8 x 194 | (0, -4, -2557) | Plastic | 210,240,252 | Top Studs, Front/Left Smooth |
| FloorB | 120 x 8 x 194 | (0, -4, -2763) | Plastic | 210,240,252 | Top Studs, Front/Left Smooth |

FloorA spans z -2460 .. -2654. FloorB spans z -2666 .. -2860. The 12-stud gap between them is the trench.

### A.3 Gap (Folder `Gap`, 4 parts)
| Name | Size | Position | Material | RGB | Flags |
|---|---|---|---|---|---|
| TrenchBottom | 120 x 3 x 12 | (0, -7.5, -2660) | Plastic | 25,55,100 | CanCollide on |
| RimA | 120 x 0.3 x 1 | (0, 0.2, -2653.5) | Plastic | 150,230,255 | CanCollide off |
| RimB | 120 x 0.3 x 1 | (0, 0.2, -2666.5) | Plastic | 150,230,255 | CanCollide off |
| HideZone | 120 x 5 x 11 | (0, -3.5, -2660) | Plastic | 0,255,0 (hidden) | Transparency 1, CanCollide off. WaveConfig reads CFrame + Size only. Attr Area=7 |

### A.4 Walls (Folder `Walls`, 15 parts, Plastic/Glacier per B.1, Top/Front Studs)
| Name | Size | Position |
|---|---|---|
| WallL_1 | 20 x 48 x 30 | (-70, 16, -2475) |
| WallL_2 | 20 x 48 x 30 | (-70, 16, -2845) |
| WallR | 20 x 48 x 97 | (70, 16, -2811.5) |
| WallR (door frame @ z -2745) | 6 x 48 x 36 | (77, 16, -2745) |
| WallR (door header) | 14 x 16 x 36 | (67, 32, -2745) |
| WallR (door sill) | 14 x 8 x 36 | (67, -4, -2745) |
| WallR | 20 x 48 x 77.3 | (70, 16, -2688.3) |
| WallR (door frame @ z -2631.7) | 6 x 48 x 36 | (77, 16, -2631.7) |
| WallR (door header) | 14 x 16 x 36 | (67, 32, -2631.7) |
| WallR (door sill) | 14 x 8 x 36 | (67, -4, -2631.7) |
| WallR | 20 x 48 x 77.3 | (70, 16, -2575) |
| WallR (door frame @ z -2518.3) | 6 x 48 x 36 | (77, 16, -2518.3) |
| WallR (door header) | 14 x 16 x 36 | (67, 32, -2518.3) |
| WallR (door sill) | 14 x 8 x 36 | (67, -4, -2518.3) |
| WallR | 20 x 48 x 40.3 | (70, 16, -2480.2) |

The right wall is continuous from z -2460 to -2860. The three door openings sit at the VipRoomsB doors.

### A.5 Bounds (the invisible wall columns, `Map.Bounds`)
| Object | Current | New |
|---|---|---|
| `Runway_End` | pos (0,540,-2470), 162x1000x22 | **pos (0,540,-2870)**, size unchanged (z -2859 .. -2881) |
| `Runway_L_2` | pos (-70,540,-1872.5), 22x1000x1217 | **pos (-70,540,-2072.5), 22x1000x1617** (z -1264 .. -2881) |
| `Runway_R_2` | pos (70,540,-1872.5), 22x1000x1217 | **pos (70,540,-2072.5), 22x1000x1617** |

Keep Transparency 1, CanQuery false, CanTouch false, CanCollide true, Persistent. MapGuard reads these at server start, so a server restart is needed.

### A.6 EndWall (moves from Area6 to Area7)
- Area6 `Walls.EndWall` at (0,16,-2470) **must be deleted** (back it up first). Leaving it in place puts a wall in the middle of Area 7.
- New `Area7_Glacier.Walls.EndWall`: 160 x 48 x 20 at **(0, 16, -2870)**, Studs top/front, Glacier RGB 165,210,240.

### A.7 AreaZone (the title and zone box)
- Part `AreaZone`: 120 x 40 x 400 at **(0, 20, -2660)**. Transparency 1, CanCollide/CanQuery/CanTouch false, Anchored.
- **CollectionService tag `Area`** (required by AreaTitleController, line 16).
- Attributes: Area=7, AreaName="Frostfall Glacier", Emoji="🧊", TextColor=Color3(170,235,255), _HadShadow=true.
- Part colour (150,220,255). It spans z -2460 .. -2860.

### A.8 CreatureLine (optional, no reader)
14 Spot parts 6 x 0.6 x 6, transparent, no collide, at x=0, y=0.3, z = -2480, -2506, -2532, -2558, -2584, -2610, -2636, -2688, -2714, -2740, -2766, -2792, -2818, -2844. The trench gap at -2654..-2666 is skipped.

### A.9 VipHideout (LEFT, Model; pivot (-60,12,-2660))
All Area6 values shifted by Z -400. Parts:
- Floor 14x8x340 @ (-67,-4,-2660); colour 170,225,250
- Back 6x48x340 @ (-77,16,-2660); colour 120,190,235
- Roof 14x16x340 @ (-67,32,-2660); colour 120,190,235
- VipGate 1x24x340 @ (-60,12,-2660); transparent 1, **CanCollide false**, CanQuery/CanTouch true
- VipDoor x3 0.4x24x36 @ x=-60, z **-2575 / -2688.3 / -2801.7** (transparent, no collide/query/touch)
- VipSafe x3 14x24x36 @ x=-67, same z (transparent, no collide/query/touch)
- VipFiller x4 14x24 @ x=-67: z -2824.8 (len 10.3), -2745 (len 77.3), -2631.7 (len 77.3), -2523.5 (len 67); colour 120,190,235
- VipTrim x9, gold SmoothPlastic (255,215,0), 1x23x1 or 1x1x36 @ x=-60.2 (Area6 z values minus 400: e.g. -2557.5, -2801.7, -2819.2, -2784.2, -2688.3, -2705.8, -2670.8, -2575, -2592.5)

### A.10 VipRoomsB (RIGHT, Model; pivot (66.8,12,-2631.7))
- VipDoor x3 0.4x24x36 @ x=60, z **-2745 / -2631.7 / -2518.3** (transparent, no collide/query/touch)
- VipSafe x3 14x24x36 @ x=67, same z (transparent, no collide/query/touch)
- VipTrim x9 gold @ x=60.2 (Area6 z values minus 400)

Result: 6 VipDoor + 6 VipSafe per area, same as Celestial. `MapGuard` and `VipClient` pick them up with no code change.

### A.11 Part budget
- Shell: 75 BaseParts (same as Area6).
- Decor: 14 props, about 44 parts (B.4), plus 6 snow patches. Total about 125 BaseParts, 0 MeshParts (Area6 has 387 BaseParts + 232 MeshParts). Celestial's decor is the heavy part, so Glacier is much lighter.

---

## B. LOOK

### B.1 Palette (RGB, all Plastic unless marked)
| Part | Material | RGB (hex) | Why |
|---|---|---|---|
| Floor (FloorA/B) | Plastic, Studs top | 210,240,252 (#D2F0FC) | Pale icy blue. The eggs must stand out on it |
| Trench bottom | Plastic | 25,55,100 (#193764) | Deep navy hole reads as "ice crack" |
| Trench rims | Plastic | 150,230,255 (#96E6FF) | Ice-cyan edge; not gold, gold is VIP trim |
| Walls (outer, EndWall) | Glacier (verify enum in Studio), Studs top/front | 165,210,240 (#A5D2F0) | Mid-ice, distinct from Water walls (35,80,205) |
| VipHideout Back / Roof / VipFiller | Plastic | 120,190,235 (#78BEEB) | |
| VipHideout Floor | Plastic | 170,225,250 (#AAE1FA) | |
| VIP trim (all VipTrim) | SmoothPlastic | 255,215,0 (#FFD700) | Gold = VIP across all areas |
| Decor: ice spikes, crystals | Glacier | 150,220,250 / 120,205,255 | |
| Decor: snow mounds, snow patches | Snow | 246,250,255 | |
| Decor: ice blocks | Glacier | 200,235,250 | |

Area colours in the UI: `AreaZone` TextColor (170,235,255) (#AAEBFF), name colour in InventoryClient AREA_COLOR (120,235,255).

Do not use the **Ice** material for floors. Roblox material friction is not verified here, and players run on floors. Check Studio before using Ice on anything walkable.

Area 2 (Water) floors are (110,195,255) and walls (35,80,205). Glacier floors are much paler, so the two areas stay distinct.

### B.2 Lighting
No change. Never change global Lighting. The sky stays the existing SkyEnvironment cloud sea (camera-following, no area change).

### B.3 Glacier egg (proposal, economy plan not on disk yet)
- Shell: deep sapphire (30,70,160) #1E46A0.
- Frost speckles: (235,248,255) #EBF8FF.
- Equator band: ice-cyan (120,220,255) #78DCFF.
- Contrast against the floor (210,240,252): very high, dark body on pale floor. The Celestial egg is pale-on-cream, so Glacier is deliberately the opposite.
- Name colour (InventoryClient AREA_COLOR): (120,235,255).
- Owner or economy agent to confirm.

### B.4 Decor: 14 side props (no trees, bushes, seats, signs or lane props)
Rules: |x| >= 46 (egg lanes clear, owner rule). Hug the walls (x = ±54 is 6 studs from the wall face at ±60). At least 12 studs in z from any VIP door, so no prop blocks a door.

Slots (z, x = ±54):
| Side | z | Type |
|---|---|---|
| Right (+54) | -2485 | Ice spikes |
| Right | -2560 | Snow mound |
| Right | -2600 | Crystal cluster |
| Right | -2665 | Ice blocks |
| Right | -2700 | Ice spikes |
| Right | -2780 | Snow mound |
| Right | -2830 | Crystal cluster |
| Left (-54) | -2490 | Ice spikes |
| Left | -2530 | Snow mound |
| Left | -2620 | Crystal cluster |
| Left | -2650 | Ice blocks |
| Left | -2735 | Ice spikes |
| Left | -2760 | Crystal cluster |
| Left | -2835 | Snow mound |

Recipes (simple Block parts, rotations in degrees around Z, all CanCollide/CanQuery/CanTouch false, Box fidelity, CastShadow false, tag `_HadShadow`):
- **Ice spikes** (3 parts, Glacier 150,220,250): 2x8x2 rot Z 8; 1.6x5.5x1.6 rot Z -12 at +1.5 x; 1.2x10x1.2 rot Z 5 at -1.2 x.
- **Snow mound** (3 parts, Snow 246,250,255): 12x2x9 at y=1; 8x2x6 at y=3; 5x1.5x4 at y=4.5 (stepped, not a Ball).
- **Crystal cluster** (4 parts, Glacier 120,205,255): 2.5x9x2.5 rot Z 14; 2x7x2 rot Z -18; 2x5x2 rot Z 30; 1.6x3.5x1.6 rot 0. Spread about 3 studs.
- **Ice blocks** (2 parts, Glacier 200,235,250): 6x6x6 at y=3; 5x5x5 at (1.5, 8.5, -1), stacked to about 11 high.

Ground: 6 snow patches (Snow 246,250,255, 17x0.2x17, CanCollide off), placed only at |x| 46..58. None in the lanes (Celestial has a patch at x -21, do not copy that).

Owner rules: no signs, no trees, no bushes, no seats, nothing bright or glowing, nothing over 12 studs tall.

Toolbox props: not used. Existing `ServerStorage.PropLibrary.Crystal` (Crystal1..5 meshes, Precise) can be considered only with owner approval and Automatic fidelity.

### B.5 Materials checklist
- Floors and trench: Plastic + Studs (matches house style).
- Walls: Glacier (verify `Enum.Material.Glacier` in Studio; fall back to Plastic if it renders badly).
- Decor: Glacier / Snow (see B.4).
- RenderFidelity: Box for all decor, never Precise.
- CastShadow off on every decor part and every rim.
- No Lighting edits.
- No Toolbox assets.

---

## C. WAVES

### C.1 Current behaviour (verified)
- Waves are GLOBAL. There is no per-area speed, size or colour in code.
- Speeds per type (`WaveConfig.Types`): Normal 55, SemiFast 90, Fast 140, Ultrakill 230, Thin 120, Swing 70 studs/s.
- Accent colours per type drive the posts, crest, highlight and spray (WaveClient lines 96, 106, 111, 123, 136, 174, 178). The mesh body is textured, not tinted.
- Waves spawn at `StartZ` and roll toward `EndZ = -62`. Front position: `StartZ + speed * (clock - start)`.

### C.2 Change: StartZ from -2500 to -2900 (WaveConfig line 5)
- New start is 20 studs behind the far face of the new end wall (-2880). Same margin as the old setup.
- Travel time to the hub (computed from `(EndZ - StartZ) / speed`):

| Type | Speed | Old (StartZ -2500) | New (StartZ -2900) | Added |
|---|---|---|---|---|
| Normal | 55 | 44.3 s | 51.6 s | +7.3 s |
| SemiFast | 90 | 27.1 s | 31.5 s | +4.4 s |
| Fast | 140 | 17.4 s | 20.3 s | +2.9 s |
| Ultrakill | 230 | 10.6 s | 12.3 s | +1.7 s |
| Thin (jump) | 120 | 20.3 s | 23.7 s | +3.4 s |
| Swing | 70 | 34.8 s | 40.5 s | +5.7 s |

**Consequences for every player, including Grass:** waves reach Grass about 7 s later (Normal), and about 16% more waves are on the runway at once. This changes the hazard rhythm for the whole game. Owner rule: "Big changes to a hazard's rhythm -> reverted; small tweaks only, ask first." **Owner must OK this before the build.**

Alternative without the global change: waves stop at Celestial, and Glacier has no waves. This contradicts the spec (blizzard waves) and is not recommended.

### C.3 Blizzard look (spec: blizzard white / ice blue)
- Waves travel toward +z. A wave is "in Glacier" only while its front is between z -2880 and -2460. That is about 420 studs, which is about 7 s for Normal, 3 s for Fast, 2 s for Hyper.
- Implementation (WaveClient, builder task): when the wave's front crosses **z = -2460**, swap the accent-coloured parts to ICE accent once. Posts, crest and highlight get colour (150,225,255). The spray emitter's ColorSequence becomes (FOAM 235,248,255, ICE 150,225,255). Then swap back to the type accent when the front passes -2460 into Celestial. Cost: one re-tint per wave, no per-frame work.
- Keep FOAM (235,248,255) as is.
- Optional: a short frost-trail emitter on the sprayHost while in Glacier. Keep it small (owner: "small VFX only").
- The wave-body textures stay.

### C.4 Speed and economy
- No speed change proposed in this plan.
- Any wave speed change is a global hazard change. Owner must approve it separately (see C.2).

---

## D. TITLE (AreaZone + name strings)

### D.1 Banner
- AreaTitleController builds `AreaName .. " " .. Emoji` (line 74) = **"Frostfall Glacier 🧊"**.
- Colour = AreaZone attribute `TextColor` = Color3(170,235,255).
- Shown only inside the AreaZone box (z -2460 .. -2860), so it appears on the far end of the runway.
- **Phone check:** 20 characters vs Celestial's 12 ("Celestial ✨"). Check the full-width banner on the mobile emulator. If it wraps, switch to "Glacier 🧊" (the folder name stays Glacier either way).

### D.2 Strings used elsewhere
- `RebirthConfig.AREA_NAMES[7] = "Glacier"` (must equal the folder suffix `Area7_Glacier`, used in UFOClient / MeteorClient lookup).
- Weather subtitle "- GLACIER -" (UFO line 501, Meteor line 871).
- Admin banner "GLACIER" (AdminBannerClient line 175).
- Analytics area name "Glacier" (A.AREAS, 7th).
- Index tab name "Glacier" (IndexConfig.AREAS name).

### D.3 Owner question
The spec and this plan use "Frostfall Glacier". progress.md (10-27) says "Frost Glacier theme". Confirm which one is the title.

### D.4 Upgrade-stall label
Area name markers come from `UpgradeConfig.AREAS` (add `{name = "Glacier", z = -2460}`). See F.

---

## E. VIP HIDEOUT AND ROOMS (pattern copy)

Same as Celestial, shifted -400 (see A.9, A.10):
- LEFT hideout: 3 VipDoor (x=-60) + 3 VipSafe (x=-67), z -2575 / -2688.3 / -2801.7. The VipGate is transparent and CanCollide off, so WaveServer's loop sets it walk-through.
- RIGHT rooms: 3 VipDoor (x=60) + 3 VipSafe (x=67), z -2518.3 / -2631.7 / -2745.
- Gold trim on all doors.
- Server: MapGuard puts a non-VIP player back outside the door (VipSafe scan, automatic).
- Client: VipClient makes every VipDoor solid for non-VIP (automatic).
- Prompt: `MarketplaceService:PromptGamePassPurchase` (automatic).
- Test with the owner's VIP pass state (see H.2).

---

## F. SYSTEMS INVENTORY (every script and line that needs an Area 7 entry)

Columns: file | line / entry | exact change | status.

### F.1 Hard changes (must do)
| # | File / object | Line / entry | Exact change |
|---|---|---|---|
| 1 | `Map.Runway.Area6_Celestial.Walls.EndWall` | — | Delete (back up first). Recreate as Area7 EndWall at (0,16,-2870) |
| 2 | `Map.Runway.Area7_Glacier` | new | Build per section A |
| 3 | `Map.Bounds.Runway_End` | — | pos z -2470 -> -2870 |
| 4 | `Map.Bounds.Runway_L_2` / `Runway_R_2` | — | size z 1217 -> 1617; pos z -1872.5 -> -2072.5 |
| 5 | `ReplicatedStorage.WaveConfig` | line 5 | StartZ = -2500 -> **-2900** (owner OK first, C.2). Comment update |
| 6 | `ReplicatedStorage.WaveConfig` | line 1-3 comments | none (comments only) |
| 7 | `StarterPlayer.StarterPlayerScripts.WaveClient` | ~96-178 Accent uses; render loop ~415-425 | Add the Glacier accent swap at z -2460 (C.3) |
| 8 | `ReplicatedStorage.WeatherConfig` | line 10 | `C.AREAS = 6` -> **7** (weather can start in Glacier) |
| 9 | `ReplicatedStorage.RebirthConfig` | line 22 | `MAX_REBIRTH = 20` -> **25** (owner answer 10-27) |
| 10 | `ReplicatedStorage.RebirthConfig` | line 26 | `AREA_NAMES` add 7th = `"Glacier"` |
| 11 | `ReplicatedStorage.RebirthConfig` | lines 31-52 (LADDER) | Add R21..R25 with `area = 7` requirements and costs (economy plan) |
| 12 | `ReplicatedStorage.UpgradeConfig` | lines 22-25 (AREAS) | add `{name = "Glacier", z = -2460}` |
| 13 | `ReplicatedStorage.UpgradeConfig` | line 48 | `U.SLING_MAX = 25` -> **30** |
| 14 | `ReplicatedStorage.UpgradeConfig` | lines 54-56 (slingRange) | Keep levels 0..25 identical. For levels 26..30: `2300 + 75 * (level - 25) + (SLING_EARLY_RANGE[l] or 0)` (proposal, see F.4) |
| 15 | `ReplicatedStorage.UpgradeConfig` | line 87 (SLING_REBIRTH, 25 entries) | Extend to 30 entries (proposal in F.3). **Mandatory:** `U.rebirthNeeded` returns 0 for a missing level (`or 0`), which would let players buy Lv26+ with money at R0 |
| 16 | `ReplicatedStorage.CreatureConfig` | lines 14-56 (Areas) | Add `GlacierEgg = {area = 7, list = {...}}` (6 pets, F.2) |
| 17 | `ReplicatedStorage.CreatureConfig` | line 107 (AREA_HATCH) | add 7th (proposal 1.5 = 13.5 h at 200K) |
| 18 | `ReplicatedStorage.CreatureConfig` | line 160 (AREA_INCOME) | add 7th = **302500** (= 55000 x 5.5, the spec's ~$300K) |
| 19 | `ReplicatedStorage.CreatureConfig` | lines 4-5, 11-12 (comments) | "minimum 1%" -> "minimum 0.1%" (comment only) |
| 20 | `ServerScriptService.EggSpawner` | lines 36-39 | Add 7th entry to KG_MAX, KG_SKEW, KG_LUCKY_ODDS, KG_LUCKY_MAX (economy values) |
| 21 | `ServerScriptService.EggSpawner` | line 79 (ICONS) | add `GlacierEgg = "rbxassetid://..."` (new icon) |
| 22 | `ServerStorage.Assets.Eggs.GlacierEgg` | new | Model with attribute Area=7 (clone of CelestialEgg, Blender recolour). Name must be `GlacierEgg` (display "Glacier Egg") |
| 23 | `ReplicatedStorage.IndexConfig` | lines 15-22 (AREAS) | add `{area = 7, egg = "GlacierEgg", name = "Glacier", version = 1, colors = {Color3.fromRGB(200,240,255), Color3.fromRGB(60,120,220)}, reward = {pct = 0.05, potions = {Money = 1, Hatch = 1}}}`; bump areas 1-3 to version 3 and 4-6 to version 4 (+1 pet each) |
| 24 | `ReplicatedStorage.IndexConfig` | lines 102-136 (PORTRAITS) | add 6 Glacier portraits (after the pets are rendered) |
| 25 | `ReplicatedStorage.StreakConfig` | lines 27-28 (EGG_KG, SECRET_KG) | add 7th each (EGG_KG[7] = the KG_MAX[7]; SECRET_KG[7] about half) |
| 26 | `ReplicatedStorage.StreakConfig` | lines 30-37 (EGG_ICONS) | add `GlacierEgg` icon |
| 27 | `ReplicatedStorage.StreakConfig` | lines 73-79 (`S.secretFor`) | **Make deterministic** (G.5): pick the secret with the highest `chance` (= Permafrost Titan, 2.5%), never the 0.1% dragon |
| 28 | `ServerScriptService.Analytics` | line 34 (A.AREAS) | add 7th = "Glacier" |
| 29 | `ServerScriptService.Analytics` | line 12 (funnel doc) | "Rebirth 1 ... 20" -> "... 25"; Creator Hub funnel steps edited by hand |
| 30 | `ReplicatedStorage.CreatureVFX` | lines 142-152 (ELEMENT) | add 6 Glacier pets -> element "Glacier" |
| 31 | `ReplicatedStorage.CreatureVFX` | lines 153-157 (AURA) | add `Glacier = {rgb(220,250,255), rgb(60,140,230)}` |
| 32 | `StarterPlayer.StarterPlayerScripts.InventoryClient` | lines 22-29 (EGG_ICONS) | add GlacierEgg icon |
| 33 | `StarterPlayer.StarterPlayerScripts.InventoryClient` | line 30 (EGG_AREA) | add `GlacierEgg = 7` |
| 34 | `StarterPlayer.StarterPlayerScripts.InventoryClient` | lines 32-39 (AREA_COLOR) | add 7th colour (120,235,255) |
| 35 | `StarterPlayer.StarterPlayerScripts.SellClient` | lines 37, 39 | add GlacierEgg icon and `GlacierEgg = 7` |
| 36 | `StarterPlayer.StarterPlayerScripts.HatchClient` | line 31 | add `GlacierEgg = {Color3.fromRGB(30,70,160), Color3.fromRGB(120,220,255)}` |
| 37 | `StarterPlayer.StarterPlayerScripts.PetsEggsUI` | line 42 | add GlacierEgg icon |
| 38 | `StarterPlayer.StarterPlayerScripts.IndexClientLegacy` | line 131 | tab spacing 0.142 -> about 0.12 so 7 tabs fit. **Visible UI: owner mockup first** |
| 39 | `CreatureModels` + `CreatureClips` | 6 new | FrostfangLynx, IceMammoth (replace the old unused one), GlacierYeti, BlizzardRoc, PermafrostTitan, FrostcrownDragon (models + clip modules, PetsV3 pipeline) |

### F.2 Glacier egg list (proposal, sorted most to least common, each egg sums to 100)
| Creature (name) | Display | Motion | Odds | secret | Note |
|---|---|---|---|---|---|
| FrostfangLynx | Frostfang Lynx | Walk | 50 | — | Starter |
| IceMammoth | Ice Mammoth | Walk | 26 | — | Replaces unused old model |
| GlacierYeti | Glacier Yeti | Walk | 14 | — | |
| BlizzardRoc | Blizzard Roc | Fly | 7.4 | — | |
| PermafrostTitan | Permafrost Titan | Walk | 2.5 | true | Secret |
| FrostcrownDragon | Frostcrown Dragon | Fly | 0.1 | true | MYTHIC: secret=true + a new `mythic` flag (proposal) |

Rarity money (existing formula `max(1,(50/pct)^0.35)`): 50% x1, 14% x1.56, 2.5% x2.85, 0.1% x8.8.

### F.3 SLING_REBIRTH proposal (economy agent to confirm)
Rule from UpgradeConfig header: a Slingshot level opens one rebirth before the rebirth that needs that area's pet. First Glacier pet at R21, so:
- Lv26 -> R16 (Celestial, a little after Lv22 at R11 and Lv24/25 at R13)
- Lv27 -> R20 (first Glacier landing, one before R21)
- Lv28 -> R21, Lv29 -> R22, Lv30 -> R23

### F.4 Slingshot numbers (proposal)
- Keep levels 0..25 identical (existing formula, Lv25 lands at z -2345 with range 2300).
- Levels 26..30 use step **75 studs per level** from 2300 (the existing slope is about 77). Landing z = -45 - range:

| Level | Range | Landing z | Area |
|---|---|---|---|
| 25 | 2300 | -2345 | Celestial (unchanged) |
| 26 | 2375 | -2420 | Celestial |
| 27 | 2450 | -2495 | **Glacier (first)** |
| 28 | 2525 | -2570 | Glacier |
| 29 | 2600 | -2645 | Glacier (FloorA, 9 studs before the trench at -2654) |
| 30 | 2675 | -2720 | Glacier (FloorB) |

- Launch speed (computed from `rangeOf()` in UpgradeConfig, 25 studs height): about 423 studs/s at Lv25, about 457 at Lv30. No speed cap in code.
- Upgrade prices on the existing curve (economy to confirm): Lv27 about $870B, Lv30 about $6.4T.

### F.5 Pets that must NOT be secret or mythic in pools
- PlaytimeConfig (line 52) and StarterPack: secret excluded automatically. Permafrost Titan and Frostcrown Dragon must have `secret = true`.
- `S.secretFor`: see G.5.

### F.6 No change needed (verified AUTO)
- `ServerScriptService.WaveServer` (VIP gates, safe checks)
- `WaveConfig.buildSafe` (SafeBoxes JSON)
- `ServerScriptService.MapGuard` (bounds + VipSafe scan)
- `ServerScriptService.WeatherServer` (bounds from AreaZone)
- `ServerScriptService.Weathers.UFO` / Meteor (follow StartZ)
- `ReplicatedStorage.Weathers.UFOClient` / `MeteorClient` (follow AREA_NAMES)
- `StarterGui.AreaTitle.AreaTitleController`
- `StarterPlayer.StarterPlayerScripts.VipClient`
- `ServerScriptService.EggAssist` path in EggSpawner (uses `areas`)
- `ServerScriptService.UpgradeServer` (clamps to SLING_MAX; sets SlingMaxSpeed)
- `ServerScriptService.SlingshotServer` (speed from SlingMaxSpeed)
- `StarterPlayer.StarterPlayerScripts.UpgradeClientLegacy` line 207 (slingRange per level)
- `ServerScriptService.RebirthServer` (cap from MAX_REBIRTH)
- `StarterPlayer.StarterPlayerScripts.AdminBannerClient` (AREA_NAMES)
- `ServerScriptService.ChatAnnounce` (colours from IndexConfig)
- `StarterPlayer.StarterPlayerScripts.StarterPackClient` (AREAS by index)
- `ReplicatedStorage.PetEventFX` (no entry = no FX)
- `StarterPlayer.StarterPlayerScripts.SkyEnvironment` (no change)
- `StarterPlayer.StarterPlayerScripts.IntroCutscene`, trailer (no change)

### F.7 Not verified (check before build)
- AdminServer / AdminUI: area dropdowns for lucky eggs or "start weather in zone N" (grep was capped at 50 and backups flooded results).
- Live Upgrade window "max level" label and any area markers on the Slingshot bar.
- Full read of WaveClient 150-470 and EggSpawner 240-765 (only the parts above were read).

---

## G. RISKS (ordered by severity)

1. **Bounds not moved (critical).** `Runway_End` at -2470 blocks area 7, and MapGuard would reset players who get inside the bounds. Do section A.5 before anything else testable.
2. **Old EndWall left in Area6 (critical, visible).** It would stand in the middle of Area 7.
3. **Silent economy break: AREA_INCOME fallback (critical).** `CreatureConfig.income` uses `AREA_INCOME[area] or 1`. If area 7 is missing from the table, its pets pay $1/s. Add entry 7 before any Glacier pet can hatch.
4. **Silent egg break.** If `ServerStorage.Assets.Eggs.GlacierEgg` (Area=7) is missing, EggSpawner skips area 7 with no error. If the 4 KG arrays are not extended, `rollWeight` clamps area 7 to area 6 values with no error.
5. **Non-deterministic streak pet (high).** `S.secretFor` loops `pairs(byName)`. With two secret-flagged pets in area 7, Day 7 could give the 0.1% **Frostcrown Dragon**, which breaks the "never mythics" rule. Fix: pick the secret with the highest `chance`. Extend `ServerStorage.StreakTests` (secretFor 6 check) with `secretFor 7 == PermafrostTitan`.
6. **Free Slingshot levels (high).** Without SLING_REBIRTH entries 26..30, `U.rebirthNeeded` returns 0, so Lv26+ can be bought with money at R0. Extend the table first.
7. **Global hazard change (high, owner decision).** StartZ -2900 delays every wave by up to 7 s and adds about 16% more waves in flight, including in Grass. Owner must approve (C.2).
8. **Lv0..25 must stay identical.** The new slingRange branch must keep levels 0..25 bit-for-bit. Run `ServerStorage.WaterWallTests` (Lv1 Water, Lv5 Water, Lv6 Thunder, "range Lv25 = max"). Note: test line 45 asserts `slingRange(25) == SLING_MAX_RANGE`; keep `SLING_MAX_RANGE = 2300` as the Lv25 value and use a separate constant for the new step, or update the test.
9. **Lv29 landing near the trench** (-2645, trench edge at -2654). Landing in the trench is safe but odd. Test a Lv29 landing.
10. **Streaming and far landings.** StreamingEnabled is on. Upgraded launches stream around the landing (SlingshotServer 123-132), but the cold-client landing at Lv30 has not been tested. The perf audit says the owner's StreamingTargetRadius is about 512 (not readable). Test a first launch on a cold client.
11. **Index needs a mockup (visible UI).** Seven tabs overflow the left column at the current spacing. Two SECRET cards in one area (Titan + Dragon) need a "MYTHIC" badge decision. Owner mockup before any build.
12. **Index re-claim economy.** Bumping IndexConfig versions for areas 1-6 lets every existing player claim them again. Each claim adds +5% money and +5% speed (IndexBonus stacks per claim). This is an economy decision, not just a version number.
13. **Pets before eggs.** `CreatureConfig.roll` returns names. If a model or clip module is missing, the hatch breaks. Ship the 6 pet models and clips before the GlacierEgg entry and the egg template.
14. **Phone performance.** Celestial: 387 BaseParts + 232 MeshParts, and about 1,070 Precise runway meshes across the runway. Glacier target: about 125 BaseParts, 0 MeshParts, Box fidelity, CastShadow off on decor. Measure with `execute_luau` (Edit) and the mobile emulator.
15. **Walkable surface.** No Ice material on floors (friction not verified here).
16. **Banner length on phone** (20 characters). Check on the emulator (D.1).
17. **Wave tint crossing point.** The swap at -2460 must run once per wave. A per-frame colour write on every emitter would cost FPS.
18. **Rebirth R25 side effects.** Pet slots at R25 = 3 + 25 = 28 (base capacity and memory test). Money multiplier at R25 = 1 + 0.25 x 25 = 7.25x. Economy and perf must review.
19. **Analytics funnels.** Creator Hub funnel steps (Rebirth 1..25, Area Ladder 7) are edited by hand. Missing steps mean missing data, not errors.
20. **Leftover marker.** `Map.Markers.TsunamiPlaceholder` at z -2500 is referenced by nothing. Harmless (transparent). Move to -2900 or delete.
21. **SafeBoxes is computed at server start.** Area 7 needs to exist in the place before the server starts, and any later trench/VIP move needs a server restart (Play restarts it).
22. **Unverified areas of the code.** AdminServer/AdminUI dropdowns and the Trailer may have area lists. Check before build (F.7).

---

## H. BUILD ORDER AND TESTS

### H.0 Before writing (owner decisions)
1. Wave StartZ -2900 OK? (C.2, global change)
2. Title "Frostfall Glacier" or "Frost Glacier"? (D.3)
3. Glacier egg colour (B.3) and icon.
4. Slingshot step 75 and rebirth locks for Lv26..30 (F.3, F.4), rebirth R21..25 costs (economy plan).
5. Mythic badge and two SECRET cards in one area (G.11).
6. Index tab mockup approval (G.11).

### H.1 Build order (one Studio writer at a time; Edit mode for structure)
1. **Backups**: `ServerStorage._Backup_Glacier.Before` gets a clone of Area6 `Walls.EndWall` and a record of the current Bounds values (A.5).
2. **Area7 shell**: clone and shift (A.0). Set folder and zone attributes and tags (A.1, A.7). Do not add Ground or Decor yet. Make sure the AreaZone has tag `Area`.
3. **Delete Area6 EndWall**, build Area7 EndWall at -2870 (A.6).
4. **Bounds**: Runway_End, Runway_L_2, Runway_R_2 (A.5).
5. **Slingshot tables**: UpgradeConfig (AREAS, SLING_MAX 30, slingRange branch, SLING_REBIRTH 30 entries). Run WaterWallTests.
6. **Rebirth tables**: RebirthConfig (AREA_NAMES, MAX 25, LADDER 21..25 with area 7).
7. **Pets**: 6 models and clip modules in CreatureModels / CreatureClips (PetsV3 pipeline). Then CreatureVFX (ELEMENT, AURA).
8. **Creature + economy tables**: CreatureConfig (GlacierEgg, AREA_HATCH, AREA_INCOME). IndexConfig (AREAS, versions). StreakConfig (arrays, icons, deterministic secretFor). Run StreakTests.
9. **Egg**: GlacierEgg template (Area=7) and icons. EggSpawner arrays (7th entries). Client tables (Inventory, Sell, Hatch, PetsEggsUI).
10. **Weather and analytics**: WeatherConfig.AREAS = 7, Analytics.AREAS. Run WeatherServerTests.
11. **Waves**: WaveConfig StartZ -2900 (after the owner OK), Markers.TsunamiPlaceholder move, WaveClient Glacier accent swap.
12. **Decor**: 14 props (B.4) + 6 snow patches, all with Box fidelity and CastShadow off.
13. **Index UI**: tab spacing (after mockup). PORTRAITS (after portraits are rendered).
14. **Server restart** (Bounds, SafeBoxes, WaveConfig are read at start).
15. **Tests** (H.2).

### H.2 Tests (Play tests need TestFreshSave == true first; owner plays inside Play tests, so freeze input while measuring; execute_luau resets CameraType, so the owner sets Camera.CameraType = Fixed afterwards)
Unit (no Play needed):
- `UpgradeConfig.slingRange(l)` for l = 0..25 equals the backup values exactly.
- `slingRange(27)` gives landing z -2495, so `areaAt` returns "Glacier". `slingRange(26)` is Celestial.
- `rebirthNeeded("Sling", 26..30) > 0` (no free levels).
- `CreatureConfig.AREA_INCOME[7] == 302500` (or the economy value). Every area has an AREA_HATCH entry.
- `StreakConfig.secretFor(7) == "PermafrostTitan"`; `secretFor(7) ~= "FrostcrownDragon"`.
- `CreatureConfig.roll("GlacierEgg", kg)` returns only the 6 names, and each model exists in CreatureModels.
- `IndexConfig.creatures(7)` has 6 entries; `IndexConfig.total()` updates.
- `WeatherConfig.AREAS == 7` and `bounds[7]` exists on the server (WeatherServer).

Play tests:
- **Egg spawn**: area 7 has 6 eggs, each with |x| <= 42, on FloorA or FloorB, not within END_MARGIN of an end, label "Glacier Egg". No egg in the trench.
- **Egg pickup and bank**: carry a Glacier egg back to the hub; it banks with kind GlacierEgg.
- **Launch at Lv27 and Lv30** (set the level in a test): the landing is in Glacier on the floor (not the trench, not Celestial). Test Lv29 too (landing -2645).
- **Cold-client launch**: a fresh client launches at Lv30; the landing area streams in and the egg is visible.
- **MapGuard**: standing at z -2850 is not reset; walking into the end (z -2880) is blocked by the EndWall and Runway_End; no false teleport from the highest Lv30 arc.
- **Waves**: a Normal wave spawns at z -2900 and reaches z -2600 after about 5 s (speed check). A player at z -2600 in the wave's path is knocked out. The same player in the trench (z -2660, x=0) or in a VIP room is safe.
- **Wave tint**: a wave changes to ice accent when its front crosses -2460 and back when it passes -2460 into Celestial (no per-frame cost).
- **Title**: AreaTitle shows "Frostfall Glacier 🧊" with TextColor (170,235,255) at z -2660; at z -2450 it shows Celestial; on the emulator (mobile) the banner text fits.
- **VIP**: each of the 6 VipDoors (z -2518.3 .. -2801.7) prompts a non-VIP player once every 6 s and lets a VIP through; a non-VIP inside a VipSafe is moved outside.
- **Weather**: `WeatherStart("UFO", 7)` and `("Meteor", 7)` work; subtitle reads "- GLACIER -"; the zone folder lookup finds Area7_Glacier.
- **Streak**: Day 4 gives a Glacier egg at EGG_KG[7]; Day 7 gives Permafrost Titan (never Frostcrown Dragon).
- **Index**: 7 tabs fit on the phone; Glacier shows 6 cards; the 2 SECRET cards show the badge; claim works.
- **Rebirth**: R21..R25 show "Glacier pet" requirement text; MAX REBIRTH shows 25.
- **Performance**: count Area7 BaseParts (target <= 150) and MeshParts (0); no Precise fidelity; FPS on a phone emulator stays flat walking through Glacier.
- **Lighting**: no change to Lighting in Edit (diff the Lighting properties).

---

## OPEN QUESTIONS (owner)
1. Waves start at -2900 (C.2)? This delays waves for everyone by up to 7 s and adds about 16% more waves in flight.
2. Title: "Frostfall Glacier" (spec) or "Frost Glacier" (progress.md)?
3. Glacier egg colour: sapphire + frost + ice band (B.3), or another colour?
4. Slingshot: step 75 per level, Lv26..30 (F.4), and the rebirth locks for Lv26..30 (F.3).
5. Rebirths R21..R25: costs and pet requirements (economy plan).
6. Frostcrown Dragon: a MYTHIC badge (new UI) and two SECRET cards in the Glacier tab (needs a mockup).
7. Index: 7 tabs (re-spaced column) and a mockup before any visible change (G.11).
8. Re-claim of areas 1-6 after the +1 pet bump (G.12): accept the extra +5% per claim, or keep the version bump off?
9. Blizzard tint only while a wave crosses Glacier (C.3, about 7 s for Normal), or a stronger look?
10. Economy: Glacier egg KG_MAX / skew / lucky odds, AREA_HATCH, AREA_INCOME (302500 proposed).

## NOT VERIFIED / LIMITS
- Not read: the full WaveClient (150-470 except the parts above), the full EggSpawner (240-765), the AdminServer / AdminUI area lists, the Trailer, and the Upgrade window's live label. Listed in F.7.
- Searches were capped at 50 matches and included many `_Backup_*` copies. Only live (non-backup) scripts were used for conclusions.
- Roblox material enum names (Glacier, Snow) and Ice friction were not checked in Studio. Verify before use.
- One read-only query created a throwaway unparented Folder (no DataModel change). No property was set, nothing was created or moved in the DataModel, and no camera or Play state was touched.
