# S2: open Frostfall Glacier (checklist)

Written by the S1 builder on 2026-10-27, from the live scripts in Studio `a7ffd071-09f7-457b-87ec-ff2b0334fe81`.
Line numbers are from **after** S1.

Numbers come from ECONOMY_PLAN.md. Where it differs from AREA7_PLAN.md, ECONOMY_PLAN wins.

The owner's decisions (2026-10-27) are built in:
- **No new wave type.** No Blizzard wave and no wave tint, so WaveServer and WaveClient do not change.
- **Hatch factor:** `AREA_HATCH[7] = 2`.
- **Mythics:** they are bonus Index cards.
- **Weather:** it also covers the Glacier.
- **More areas later:** keep every list data-driven.

## Before you start

1. Back up every script you touch into `ServerStorage._Backup_GlacierS2.Before`:
   - Disable the scripts.
   - Strip their tags.
2. The S2_OpenMap module (step A) backs up the map objects it changes by itself.
3. **Order matters (AREA7_PLAN G13):** pets before eggs.
   1. The 6 Glacier pets need their `CreatureModels` and `CreatureClips`.
   2. Then add `CreatureConfig.Areas.GlacierEgg` (B4).
   3. Only then register the egg template (step A6). If you register it earlier, a hatch rolls a pet with no model.
4. **Server restart:** MapGuard, SafeBoxes, EggSpawner `areas`, WeatherServer `bounds` and WaveConfig are all read at server start.
   - In Studio, a new Play test restarts them.
   - Live, the owner must Migrate to Latest Update.

---

## A. Map (Edit mode, one call)

**Since the visual review (2026-10-27), `Area7_Glacier` is PARKED in `ServerStorage._GlacierStage`, not in the workspace.**
- Why: nothing should show past the end wall on Lv25 launch arcs.
- While it is parked, its CollectionService tags (AreaZone `Area`, HideZone `Gap`, VipGate `VipGate`, 14 spots `CreatureSpot`) are stripped and stored in the attribute `_StageTags`.
- Owner preview in Edit (the folder stays `Closed`, behind the old end wall): `require(game.ServerStorage._GlacierStage.Preview:Clone())()` toggles it in and out.

S1 already wrote the whole map step as a module and dry-ran it with the folder parked. Step **A0** moves the folder back first:

```lua
require(game.ServerStorage._Backup_GlacierS1.S2_OpenMap:Clone())(true)   -- dry run: prints the list below
require(game.ServerStorage._Backup_GlacierS1.S2_OpenMap:Clone())(false)  -- apply
```

| # | Object | Today (S1) | S2 value |
|---|---|---|---|
| A0 | `Area7_Glacier` | parked in `ServerStorage._GlacierStage`, tags in `_StageTags` | moved to **`workspace.Map.Runway`**, tags restored on 17 instances (`_GlacierStage.Preview` `show()`) |
| A1 | `ServerStorage._Backup_GlacierS2.Before` | - | Clones (untagged) of Area6 EndWall, `Map.Bounds.Runway_End`, `Map.Markers.TsunamiPlaceholder` |
| A2 | `Map.Runway.Area6_Celestial.Walls.EndWall` | 160x48x20 @ (0,16,-2470) | **Deleted.** Area7 has its own EndWall @ (0,16,-2870) already |
| A3 | `Area7_Glacier.Walls.WallL_1` | 20x48x**10** @ (-70,16,**-2485**) | 20x48x**30** @ (-70,16,**-2475**). Read from its `S2Size` / `S2CFrame` attributes |
| A3 | `Area7_Glacier.Walls.WallR` (the 40.3 piece) | 20x48x**20.33** @ (70,16,**-2490.17**) | 20x48x**40.33** @ (70,16,**-2480.17**). Read from its `S2Size` / `S2CFrame` attributes |
| A4 | `Map.Bounds.Runway_End` | (0,540,-2470), 162x1000x22 | **(0,540,-2870)**, same size |
| A4 | `Map.Bounds.Runway_L_3` | - | New: a clone of L_2 @ **(-70,540,-2670)**, size **22x1000x422** (z -2459 .. -2881) |
| A4 | `Map.Bounds.Runway_R_3` | - | New: a clone of R_2 @ **(70,540,-2670)**, size **22x1000x422** |
| A5 | `Map.Markers.TsunamiPlaceholder` | z -2500 | z **-2900** (nothing reads it; kept in step with StartZ) |
| A6 | `ServerStorage.Assets.Eggs.GlacierEgg` | `PendingArea = 7`, no `Area` | **`Area = 7`**, `PendingArea` removed. EggSpawner registers templates by this attribute |
| A7 | `Map.Runway.Area7_Glacier` | attribute `Closed = true` | Attribute **removed**. EggSpawner line 102 skips Closed folders |
| A8 | `ServerStorage._GlacierStage` | holds the parked folder + `Preview` | **Deleted** (empty after A0) |

Why A3 exists: in S1 the old EndWall fills z -2460..-2480. Two Glacier wall pieces would have shared that volume, and their top faces at y 40 would z-fight, which you can see from a launch arc. So S1 started them at z -2480.

---

## B. Scripts

### B1. `ReplicatedStorage.UpgradeConfig` (Slingshot Lv26-30, ECONOMY_PLAN section 2)

| Line | Today | New |
|---|---|---|
| 1-14 | header "25 levels ... Lv25 lands deep in Celestial" | "30 levels ... Glacier Lv27 at R20 (for R21)" |
| 22-25 | `AREAS` ends `{name = "Celestial", z = -2060},` | add `{name = "Glacier", z = -2460},` (`areaAt`, line 71-76, loops the table) |
| 48 | `U.SLING_MAX = 25` | `U.SLING_MAX = 30` + new line `U.SLING_SLOPE_LEVELS = 25` (the slope stays (2300-370)/25) |
| 50 | `U.SLING_MAX_RANGE = 2300` | unchanged (= the Lv25 range; WaterWallTests asserts `slingRange(25) == SLING_MAX_RANGE`) |
| 56 | `... * l / U.SLING_MAX + ...` | `... * l / U.SLING_SLOPE_LEVELS + ...` (Lv0-25 stay bit-for-bit) |
| 87 | `U.SLING_REBIRTH` (25 entries) | `{0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 7, 7, 7, 9, 9, 11, 11, 13, 13, 16, 20, 20, 22, 22}`. **All 30 entries are required:** `rebirthNeeded` (line 101) returns 0 for a missing level, which would let anyone buy Lv26+ at R0 |

- **Check:** `slingRange(26..30)` = 2377 / 2454 / 2532 / 2609 / 2686. `areaAt(slingRange(27)) == "Glacier"` and `areaAt(slingRange(26)) == "Celestial"`.
- **No change needed:** `slingCost` already continues past 25.

### B2. `ReplicatedStorage.RebirthConfig` (R21-R25, ECONOMY_PLAN section 3)

| Line | Today | New |
|---|---|---|
| 7-9, 28-30 | comments "area 1..6", "R20 = a lucky 1M+ KG egg" | Glacier R21-R25 |
| 22 | `RebirthConfig.MAX_REBIRTH = 20` | `= 25` |
| 26 | `AREA_NAMES = {... "Celestial"}` | add `"Glacier"`. **It must equal the folder suffix:** UFOClient line 465 and MeteorClient line 418 find `("Area%d_%s"):format(area, AREA_NAMES[area])` |
| after 51 | `{cost = 32000000000000, area = 6, kg = 1000000},` | add 5 rows: `{cost = 40000000000000, area = 7, kg = 1}`, `{cost = 130000000000000, area = 7, kg = 1000}`, `{cost = 230000000000000, area = 7, kg = 10000}`, `{cost = 350000000000000, area = 7, kg = 100000}`, `{cost = 500000000000000, area = 7, kg = 1000000}` |

### B3. `ReplicatedStorage.WaveConfig`

| Line | Today | New |
|---|---|---|
| 5 | `StartZ = -2500, -- far end of Celestial` | `StartZ = -2900, -- far end of Glacier (its floor ends at -2860)` |

- **No Blizzard type.** The owner said no new wave type.
- **Owner OK still pending:** AREA7_PLAN C.2 and G7 flag this as a global rhythm change. Waves reach the hub later: Normal +7.3 s, Fast +2.9 s. ECONOMY_PLAN section 6 shows the number of waves passing a spot does not change.
- **No other code:** WaveServer and WaveClient read `Config.StartZ`.

### B4. `ReplicatedStorage.CreatureConfig` (needs the 6 pet models first)

| Line | Today | New |
|---|---|---|
| 11-13 | `c(name, display, motion, odds, secret)`; comment "minimum 1 %" | add a 6th arg `mythic`: `{..., secret = secret, mythic = mythic}`; comment "minimum 0.1 %" |
| 14-57 | 6 eggs x 5 pets | new 6-pet lists (ECONOMY_PLAN section 5) + `GlacierEgg = {area = 7, list = {...}}` (section 4: FrostfangLynx 50, IceMammoth 26, GlacierYeti 14, BlizzardRoc 7.4, PermafrostTitan 2.5 secret, FrostcrownDragon 0.1 secret+mythic). **Mythics: `CinderOverlord`, `EclipseSeraph`, `FrostcrownDragon`** = `secret = true, mythic = true` |
| 78-80 | `byName` record | add `mythic = cr.mythic` |
| 107 | `AREA_HATCH = {..., 1, 2}` | **already done in S1** |
| 161 | `AREA_INCOME = {..., 55000, 300000}` | **already done in S1** |

### B5. `ServerScriptService.EggSpawner`

| Line | Today | New |
|---|---|---|
| 38-41 | KG arrays with a 7th entry: 800000 / 2.0 / 180 / 10000000 | **already done in S1** |
| 75-82 | `ICONS` x6 | add `GlacierEgg = "rbxassetid://<new egg icon>",`. Render it the same way as the other egg icons. **Without it the hotbar egg has no picture** |
| 102 | `... and a:GetAttribute("Closed") ~= true` | keep it. A7 removes the attribute. The next area can be built closed the same way |

### B6. Weather (owner: weather covers the Glacier)

| Script : line | Today | New |
|---|---|---|
| `ReplicatedStorage.WeatherConfig` 10 | `C.AREAS = 6` | `C.AREAS = 7` |
| `ServerStorage.WeatherTests` 67 | `C.AREAS == 6` | `C.AREAS == 7` |

- **Data-driven option:** WeatherServer could use the highest key of its `bounds` table (line 62-74, built from the runway folders) instead of `WeatherConfig.AREAS`, and skip `Closed` folders there.
- **Today it is safe:** `bounds[7]` already exists (S1), but nothing asks for area 7. Random picks use `WeatherConfig.AREAS`, and AdminServer passes `area = nil`.

### B7. `ServerScriptService.Analytics`

| Line | Today | New |
|---|---|---|
| 34 | `A.AREAS = {..., "Glacier"}` | **already done in S1** (Area Ladder step 7) |
| 80 | `... or r <= 15 and "R11-15" or "R16-20"` | `... or r <= 15 and "R11-15" or r <= 20 and "R16-20" or "R21-25"` |
| 12 (doc) | "Rebirth 1 ... 20" | "... 25". The Creator Hub funnel steps are edited by hand |

### B8. `ReplicatedStorage.StreakConfig`

| Line | Today | New |
|---|---|---|
| 27 | `S.EGG_KG = {..., 500000}` | add `800000` |
| 28 | `S.SECRET_KG = {..., 250000}` | add `400000` |
| 30-37 | `EGG_ICONS` x6 | add `GlacierEgg = "<icon>"` |
| 76 | `if info.area == a and info.secret and models:FindFirstChild(name)` | `info.secret and not info.mythic`. `pairs()` order is random, so without this Day 7 could hand out a 0.1-0.5% mythic (AREA7_PLAN G5) |

- **Check `ServerStorage.StreakTests`:** add `secretFor(7) == "PermafrostTitan"` next to line 55. Lines 58-59 check `[6]` only.

### B9. Pools that must never give a mythic away

| Script : line | Note |
|---|---|
| `RS.PlaytimeConfig` 52 | `not info.secret`. This is OK only because mythics are also `secret = true` |
| `RS.StarterPackConfig` | no change (Magma/Shadow eggs; secrets show as silhouettes) |
| `SSS.ChatAnnounce` 24, 69-86 | secrets are always announced, so mythics are too. An optional `MYTHIC!` line is visible text and needs the owner's OK |

### B10. Index (owner: mythics are BONUS cards)

| Script : line | Today | New |
|---|---|---|
| `RS.IndexConfig` 15-22 | 6 AREAS, versions 2/2/2/3/3/3 | versions **3/3/3/4/4/4** (+1 pet each). Add `{area = 7, egg = "GlacierEgg", name = "Glacier", version = 1, colors = {Color3.fromRGB(200, 240, 255), Color3.fromRGB(60, 120, 220)}, reward = {pct = 0.05, potions = {Money = 1, Hatch = 1}}}`. **Re-claim economy (G12):** a version bump lets everyone claim areas 1-6 again (+5% each) |
| `RS.IndexConfig` 93-98 `areaComplete` | every card must be found | skip bonus cards: `if not d.found[c.name] and not c.mythic then return false end` (owner: mythics don't block the claim) |
| `RS.IndexConfig` 30-34 / 85-91 | `total()` / `discovered()` count every card | decide if bonus cards count in "x/N" (display only) |
| `RS.IndexConfig` 102+ | PORTRAITS | add 12 portraits |
| `SPS.IndexClientLegacy` 8, 130-131, 172-182 | "x/21", 7th tab at y 0.07 + 6 x 0.142 = 0.92 (off the column), `for slot = 1, 5` (5 cards hard-coded) | 7 tabs, 6 cards (`#IndexConfig.creatures(i)`), mythic badge. **Visible UI: a mockup and the owner's OK first** |
| `ServerStorage.HatchRISTests.index_client` 113-114 | "rail: 6 hits" | 7 |

### B11. Client egg tables (the Glacier egg: sapphire (30,70,160) + ice band (120,220,255))

| Script : line | New |
|---|---|
| `SPS.HatchClient` 25-32 `SHELL` | `GlacierEgg = {Color3.fromRGB(30, 70, 160), Color3.fromRGB(120, 220, 255)},` (else it falls back to WoodEgg) |
| `SPS.PetsEggsUI` 36-43 | `GlacierEgg = "<icon>",` |
| `SPS.InventoryClient` 22-29 / 30 / 32-39 | icon; `GlacierEgg = 7` in `EGG_AREA`; 7th `AREA_COLOR` `Color3.fromRGB(120, 235, 255), -- Glacier` |
| `SPS.SellClient` 35-37 / 39 / 40-43 | the same 3 entries |

### B12. Pet look

| Script : line | New |
|---|---|
| `RS.CreatureVFX` 142-152 `ELEMENT` | 6 Glacier pets `= "Glacier"` + the 6 new area pets, each to its own element |
| `RS.CreatureVFX` 153-157 `AURA` | `Glacier = {rgb(220, 250, 255), rgb(60, 140, 230)}`. Unknown names fall back to the Celestial gold aura (line 161) |
| `RS.PetEventFX` | only for new pets with clip events |

### B13. Robux (owner OK; NEVER create the product yourself)

| Script : line | New |
|---|---|
| `RS.ShopConfig` 109-110 | `{upTo = 30, id = <new product>, price = 65}` after `{upTo = 25, ...}`. Without it, Lv26+ cannot be bought with Robux |

### B14. Tests to update

| Test : line | Change |
|---|---|
| `RebirthV6Tests` 6-12 | add R21-R25 rows |
| `StreakTests` 53-59 | `secretFor 7` |
| `WeatherTests` 67 | `C.AREAS == 7` |
| `HatchRISTests.index_client` 113-114 | 7 rail hits |
| `HubV2Tests` 358-361 | R25: 28 pets on a 60 x 90 plot (today: 23) |
| `WaterWallTests` | must still pass 19/19 (Lv0-25 unchanged) |

---

## C. S2 tests (Play needs TestFreshSave == true; set it back to false after the last one)

1. **Eggs:**
   - Area 7 keeps 6 eggs on FloorA/FloorB with |x| <= 42, none in the trench.
   - The label reads "Glacier Egg".
   - Areas 1-6 are unchanged.
2. **Lv27 / Lv29 / Lv30 launches:**
   - Landings at about -2499 / -2654 (trench edge) / -2731, all in Glacier.
   - A Lv26 launch lands in Celestial.
   - Test on a cold client too (streaming).
3. **MapGuard:**
   - At z -2850 the player is not reset.
   - The end at -2870 blocks the player.
   - The highest Lv30 arc gives no false teleport.
4. **AreaTitle:**
   - "Frostfall Glacier 🧊" in (170,235,255).
   - Check on the phone emulator: 20 characters vs Celestial's 12.
5. **VIP:** the 6 doors at z -2518.3 .. -2801.7 prompt a non-VIP, and the VipSafe moves a non-VIP outside.
6. **Weather:** UFO and Meteor in area 7 show "- GLACIER -" and the zone lookup finds Area7_Glacier.
7. **Streak:** Day 7 for area 7 = Permafrost Titan, never a mythic.
8. **Index:** 7 tabs and 6 cards; mythics are bonus cards; claim works.
9. **Rebirth:** R21-R25 requirement text "Glacier pet ..."; MAX shows 25.
10. **Waves:** they spawn at -2900. A Normal wave reaches -2600 about 5.5 s after it spawns. Trench and VIP rooms are safe.

## D. Risks (AREA7_PLAN G, updated for S1 and the owner decisions)

0. **Folder still parked:** if `Area7_Glacier` stays in `ServerStorage._GlacierStage`, area 7 has no floor or walls. A0 moves it back with its tags. Check that `CollectionService:GetTagged("Area")` returns 7 zones on the server afterwards.
1. **Bounds not moved:** Runway_End at -2470 keeps blocking area 7. A4 fixes this together with A2.
2. **Old EndWall left in place:** it stands in the middle of the opened area. A2 removes it.
3. **`AREA_INCOME[7]` fallback:** done in S1 ($300K), so area 7 pets never pay $1/s.
4. **Silent egg break:**
   - The template's `Area = 7` (A6) and `Closed` removed (A7) are both needed, or EggSpawner skips area 7 without an error.
   - The KG arrays already have entry 7.
5. **Streak mythic:** fix StreakConfig line 76 (B8).
6. **Free Slingshot levels:** SLING_REBIRTH needs all 30 entries (B1).
7. **Global wave rhythm (StartZ -2900):** this needs the owner's OK (B3). The Blizzard wave was dropped by the owner.
8. **Lv0-25 must stay identical:** keep `SLING_MAX_RANGE = 2300` and use `SLING_SLOPE_LEVELS`. Run WaterWallTests.
9. **Lv29 lands at the trench edge** (-2654): test it.
10. **Streaming of far landings:** do a cold-client Lv30 test.
11. **Index UI:** this is visible UI, so it needs a mockup first. There are now 2 secret cards plus a mythic badge in Glacier.
12. **Index re-claim:** the version bump re-pays +5% per area. This is the owner's call.
13. **Pets before eggs:** the models and clips must exist before A6.
14. **Phone performance:**
    - Glacier has 323 BaseParts and 208 MeshParts (after the 6 wall crystals); Celestial has 387 and 232.
    - No Neon and no lights in Glacier decor.
    - The crystals use Precise render fidelity, like every other area's crystals.
15. **Walkable surface:** no Ice material anywhere. The floor is Plastic with studs.
16. **Banner length on phones:** "Frostfall Glacier 🧊" is 20 characters.
17. **Wave tint:** dropped (no new wave type).
18. **R25 side effects:** 28 pet slots and x7.25 (HubV2Tests).
19. **Analytics funnels:** the Creator Hub steps are edited by hand.
20. **TsunamiPlaceholder:** A5 moves it.
21. **SafeBoxes etc. are built at server start:** restart after A. In S1 there are already 8 Glacier safe boxes (harmless).
22. **AdminServer / AdminUI:** checked in S1.
    - AdminServer passes `area = nil` to WeatherStart (line 273).
    - A grep of the admin scripts found no area lists.
    - So nothing to change.

## Pet names + the old IceMammoth (added late on 10-27)
23. **The final pet NAMES (two words, owner rule)** are FrostcrownDragon, CinderOverlord and CoralCrusher. They are NOT AbsoluteZeroDragon, CinderWyrmOverlord or CoralCrusherCrab. ECONOMY_PLAN and AREA7_PLAN were updated to the new names on 10-27 late; any old name you meet is a typo. Also, the FBX files, clip Lua and portraits use the new names. Use the new names in CreatureConfig, IndexConfig, the odds tables, ChatAnnounce and the streak/playtime skips.
24. **An OLD IceMammoth already exists:**
    - The 10-02 studded Claude Design model is `ReplicatedStorage.CreatureModels.IceMammoth` + `ReplicatedStorage.CreatureClips.IceMammoth`. It is not in any egg; a CreatureConfig comment says so.
    - Before importing the new one, move both into `ServerStorage._Backup_GlacierS2.OldIceMammoth`, then strip tags and scripts from the copies.
    - Check that nothing else references the old clips module (grep "CreatureClips.IceMammoth").
    - The old 10-02 `C:\cdimp\IceMammoth.fbx` is overwritten by the new export. Check the file date is 10-27 or later before importing.
25. **The Coral Crusher portrait** = `PetsV3\CoralCrusher\CoralCrusher_portrait_alt.png` (game camera), NOT the `_portrait_raw.png` that the export wrote.
    - **The Cinder Overlord portrait** (10-28 r14) = the kit portrait `PetsV3\CinderOverlord\CinderOverlord_portrait_raw.png` (gold 117, area 0.378). NOT the `_portrait_alt.png`, which is now a reference only (0.369 < Thunder Rex 0.372).

## Studio checks from the final gate reviews (added 10-28)
26. **Walk stride matches the clip module.** `CreatureAnimator` L305-306 drives the walk phase by distance travelled: `ph += dist / (clip.stride * k)`. So a wrong `stride` in a clip module makes the walk skate.
    - For every new pet, check that `CreatureClips.<Pet>.walk.stride` equals the stride the builder measured, normalised the same way as the old pets.
    - The Cinder's stride is 5.009 BU per 48 f, after Tail4 was cut 45 %.
    - Then watch each pet follow at run speed for 10 s.
    - **10-28 13:25 DONE for the 10 imported pets:** every `walk.stride` equals the cfg stride. WalkSpeed is now bone-measured (k = ref bone vs Root / ref.dist, the animator's own k): Seraph 1.44 -> 1.87 (its `_bu.json` height came from the raised-wing portrait pose, 30 % off), Yeti 1.30 -> 1.34, Dragon 1.87 -> 1.89, Roc 1.87 -> 1.85, Rhino 1.40 -> 1.39, the other 5 unchanged. `PetSetup3` patched to do this itself (backup `_Backup_GlacierS2.PetSetup3_before_boneK`). The 10 s follow watch is still open (Play test).
27. **Yeti look-turn.** The look-turn adds yaw to both Neck and Head, so it is about 2x on this pet. Cap it in Studio if it reads too big at 5 studs.
28. **Mammoth colour (80,150,176)** and **Titan colour:** judge both under game lighting at 5 studs. The Mammoth fallback is (72,140,164), but that breaks the 170 brightest-channel floor, so it needs the owner's OK.
29. **VFX the lead adds:**
    - Lynx ICE sparks on claw1 f48 and claw2 f60;
    - Cinder ember aura + blue vent flame;
    - Wraith smoke;
    - Cinder idle breath readability at 5 studs.
30. **Cinder VFX anchors:** the vents on Body3, Body4 and Tail1 were removed in the final gate (10-28). `Vent_4..6` anchors no longer exist, so build FX_VentSmoke only on the remaining vent anchors.
31. **Titan kneel snow puff:** add a small snow-puff VFX at the `Knee_L` anchor when the knee lands (act_kneelrise, knee lands EXACTLY f18 = the `icecrack` event 0.18 since the r10 export 14:02), to sell the contact from the game camera (lead ruling 10-28).
