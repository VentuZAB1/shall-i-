# Redesigned Hub (A HORSESHOE) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> Owner pipeline (memory `feedback-subagent-build-pipeline`): this plan -> Haiku plan reviewer -> Opus builder, stage by
> stage -> Haiku visual reviewer -> performance check. One builder in Studio at a time; start only after the HATCH NIGHT
> Gift window build is finished.

**Goal:** Replace `workspace.Map.Hub` with a new horseshoe hub: 6 identical, skin-ready plots (max 60 x 90) in a U
around one open plaza behind the fixed slingshot, with the stalls, boards, Free Gift, spawn, decor and a seasonal
Halloween layer re-placed, and every hub system working for 6 players.

**Architecture:**
- The new hub is built off-map as the Model `Map.HubV2` at `Layout.OFFSET = (2000, 0, 0)` while the live hub keeps
  running. Every coordinate comes from one generated module (`ServerStorage.HubV2Kit.Layout`). A Luau validator
  (`HubV2Kit.Validate`) checks the build after every stage.
- The swap moves HubV2 by `-OFFSET`, re-parents the untouched Slingshot + LaunchPlatform into it and renames it `Hub`.
  The old hub and HalloweenDecor go whole into `ServerStorage._Backup_Hub.Before` with their tags stripped.
- All folder and model names stay the same (`Hub.Bases.Base<N>`, `Treadmills.Treadmill_B<N>`,
  `UpgradeSigns.UpgradeSign_B<N>`, `Stalls`, `Leaderboards`, `FreeGift`, `Spawn`, `Decor`, `MarketCorners`). That is
  why only 4 scripts change: BaseBuilder, BaseManager, BaseHatchery and AdminUI.Trailer.

**Tech Stack:** Luau in the owner's Roblox Studio via the Studio MCP (`execute_luau`, `script_read`, `multi_edit`,
`start_stop_play`, `screen_capture`, `search_asset`/`insert_asset`); Python + PIL for the layout checker
(`docs/plans/hub-2026-10-21/tools/`).

**Spec:** `Desktop/SLINGSHOT Creatures/docs/specs/2026-10-21-redesigned-hub-design.md` (owner-approved; binding).
Layout sketch picked by the owner: `docs/plans/hub-2026-10-21/A_horseshoe.png`.

**Planned layout (real studs):** `docs/plans/hub-2026-10-21/planned_layout.png`; side by side with the sketch:
`docs/plans/hub-2026-10-21/planned_vs_sketch.png`. Source of truth: `docs/plans/hub-2026-10-21/tools/hub_layout.py`
(49 rule checks, `python hub_layout.py` prints ALL PASS). The Luau module generated from it is
`docs/plans/hub-2026-10-21/HubLayout.lua` (`python make_layout_lua.py`).

---

## Global Constraints

- **Studio:** `studio_id = 0663e976-4faf-4dca-bf0c-91120a8d1353` (SLINGSHOT, group-owned by ZAB Studio). If it fails,
  re-check with `list_roblox_studios`. Never use another game's Studio.
- **Build only in Edit.** If Studio is in Play (another agent), wait. Never start or stop someone else's Play session.
- **Play tests:**
  - Before EVERY `start_stop_play`, read `workspace:GetAttribute("TestFreshSave")` in Edit and require `true`
    (memory `feedback-testfreshsave-before-play`).
  - Set it back to `false` only after the last Play test of the session.
  - The owner may play inside our Play sessions: read state, don't fight their input. When measuring, sink
    W/A/S/D/Space with a priority-9000 CAS action.
- **The owner's Studio:**
  - Never type into the command bar and never click Studio dialogs. Use `execute_luau` for DataModel work.
  - Never set `Camera.CameraType` from a script.
  - Never publish. The owner saves and publishes.
- **Heavy edits:** build in chunks with `task.wait()` between them. Build each chunk in a container outside the
  DataModel and parent it once (Studio MCP rule).
- **Edit require cache:** to test a ModuleScript you just edited, `require(module:Clone())` with the clone parented
  next to the original, then destroy the clone. Clone siblings it waits for (BaseBuilder has none; RebirthConfig waits for
  CreatureConfig and SpeedStat).
- **Deferred signals:** never set two related attributes in the same frame in tests (`task.wait()` between).
- **Tags (2026-10-21 rule, memory `roblox-slingshot-launch-bug-1021`):**
  - Staging (`Map.HubV2`) carries NO CollectionService tags. Every instance that needs a tag after the swap gets the
    attribute `_SwapTags = "Tag1,Tag2"`.
  - Every copy that goes to ServerStorage (backups, templates, stage snapshots) has ALL tags stripped. The removed tags
    are stored in the attribute `_RemovedTags`.
  - Why: `CollectionService:GetTagged` also returns ServerStorage instances. BaseManager and TreadmillServer would hand
    out a backup base or swap a backup treadmill.
- **Script backups:** before the first edit of a script, copy it to `ServerStorage._Backup_HubV2.Scripts.<Name>`. Clone
  it, set Disabled/Enabled = false on the copy, and strip its tags.
- **Stage snapshots:** after each build stage, clone `Map.HubV2` into `ServerStorage._Backup_HubV2.Stage<N>_<what>`.
  Strip tags (there should be none). Write one line to the progress ledger
  `docs/plans/2026-10-21-redesigned-hub.progress.md`. This is the commit-like checkpoint; there is no git for Studio.
- **Code style:** tabs, dated comments `-- (2026-10-21) ...`, the comment density of the file you edit, and a header
  line saying what changed.
- **Part rules:**
  - Every BasePart is Anchored.
  - Walkable flat parts are Plastic with `TopSurface = Studs` (the toy-brick look, memory `roblox-polish-1013`).
    Cylinders use `MaterialVariant = "Studs"`.
  - Small or thin parts get `CastShadow = false`. Natural props (trees, bushes, rocks) keep their shadow.
  - Decor that is not a walking obstacle: CanCollide / CanQuery / CanTouch false.
  - Every Halloween part has CanCollide / CanTouch / CanQuery false and MeshParts use CollisionFidelity Box (owner rule).
- **Toolbox:**
  - Search, insert, vet, then use (rule in Task 6).
  - The spec warns that both sky models inserted on 2026-10-21 hid backdoor scripts.
- **Owner hand edits:** the owner may move decor afterwards. Tests and the validator must never depend on exact decor
  positions, only on the rules (corridors, zones, gaps).
- **Fixed world:** never move `Hub.Slingshot`, `Hub.LaunchPlatform`, `Map.Runway` (incl. `LaunchGate`) or anything on
  the runway. `Slingshot.Config.GateZ = -60` and `PadCenter = (0, 1, -45)` stay.

## Review Focus

1. **A returning player whose eggs were saved on the old 64 x 80 floor (or another R1-R4 size) must load with every egg
   inside the new fence, none lost or overlapping.**
   - Egg records are floor-local, and the new floor centre and width differ.
   - Test: `T2.3 fit-on-load` in Task 2.
2. **A 7th player (the owner forgets the Creator Hub server size, or a Studio multi-client test) gets BaseId 0 and must
   not break anything.**
   - Expected: they stay at the Spawn, no errors from the tutorial, OfflineClient, TreadmillServer or BaseHatchery.
   - Test: `T10.2 seventh player` in Task 10.
3. **Backups and templates in ServerStorage must never be picked by `GetTagged`.**
   - Expected after the swap: exactly 6 `Base`, 6 `Treadmill`, 1 `Slingshot`, 1 `LaunchPad`, 1 `LaunchGate`, all
     descendants of workspace.
   - Test: `T9.4 tag census` in Task 9.
4. **Players walking across the plaza must not open the Upgrade / Sell / Free Gift windows by accident, and no prop may
   block a straight walk from the gate to any plot.**
   - The layout checker covers it on paper. Test: `T10.7 walker` in Task 10 (Humanoid:MoveTo between all key points
     arrives).
5. **The invisible bounds must not teleport players who walk along the hub edge or the runway mouth.**
   - The old `Runway_L_1` / `Runway_R_1` columns reach 11 studs into the new plaza.
   - Test: `T10.6 bounds` in Task 10 (stand 1 stud inside every edge and at (±70, -55) for 2 s: not moved).

---

## The layout (decided; all numbers from `HubLayout.lua`)

World axes: x right, z toward the back of the hub (the runway is at -Z). Every floor top is y = 0. `F` = a plot's
facing (from the plot to the plaza, = its Slot LookVector), `R = F x Up`.

**Fixed (never moved):**
- Slingshot pivot (0.53, 1, -44.97).
- LaunchPlatform 19 x 1 x 14 at (0.5, 0.5, -45).
- LaunchGate 120 x 16 x 2 at (0, 8, -61).
- Runway walls |x| 59..81 for z <= -60.

**Plots** (Slot 60 x 0.2 x 90 at y 0.1; the gate = the Slot's front-edge centre; plots grow back from the gate):

| BaseId | sketch | gate (x, z) | F | Slot centre | gate -> slingshot | treadmill pivot (y 0.6, look F) | upgrade sign pivot (y 3.2, look -F) | spawn spot |
|---|---|---|---|---|---|---|---|---|
| 1 | Grass, left front | (-122, -30) | +X | (-167, -30) | 123.4 | (-107.7, -48) | (-116, -58) | (-114, -30) |
| 2 | Water, left back | (-90, 42) | +X | (-135, 42) | 125.5 | (-75.7, 24) | (-84, 14) | (-82, 42) |
| 3 | Thunder, back left | (-40, 78) | -Z | (-40, 123) | 129.5 | (-58, 63.7) | (-66.5, 72) | (-40, 70) |
| 4 | Fire, back right | (40, 78) | -Z | (40, 123) | 129.1 | (58, 63.7) | (66.5, 72) | (40, 70) |
| 5 | Shadow, right back | (90, 42) | -X | (135, 42) | 124.8 | (75.7, 24) | (84, 14) | (82, 42) |
| 6 | Celestial, right front | (122, -30) | -X | (167, -30) | 122.4 | (107.7, -48) | (116, -58) | (114, -30) |

- **Rules met (checker):**
  - The plots are 12 / 20.9 / 20 / 20.9 / 12 studs apart at 60 x 90 (the minimum is 10). The front edge never moves,
    so smaller sizes are further apart.
  - Every gate is at most 129.5 from the slingshot (the limit is 140); fairness max/min = 1.058.
  - Nothing sits past z -60 or in the launch zone (x -14..15, z -62..-30).
  - Nothing is taller than 0.8 inside the intro corridor (x -12..24, z -40..12).
- **Growth per rebirth** (`RebirthConfig.baseSize(r, 60, 90)`): R0 40x40, R1 44x50, R2 48x60, R3 52x70, R4 56x80,
  R5+ 60x90.
- **Why the front pair sits further out than the sketch:**
  - With 4 plots on two straight side lines, the front and back gates differ by about 30 studs of walk.
  - Pushing plots 1/6 out to x ±122 keeps every walk within 6% and every walk under 130.
  - It still reads as the sketch's U (`planned_vs_sketch.png`).
- **Why the plaza is 130 deep, not the sketch's 180:** the spec's binding "gate to slingshot ≤ ~140" rule. At a 180
  depth the back plots would be 220 away.

**Plaza items** (`Layout.STALLS / BOARDS / FREE_GIFT / SPAWN`):

| item | where | facing |
|---|---|---|
| UpgradeStall (blue ring) | ring centre (-100, 0.6, -8); model pivot (= Plinth) (-104.425, 0.9, -7.031) | (0.977, -0.214), toward the plaza front |
| SellStall (gold ring) | ring (100, 0.6, -8); pivot (104.423, 0.9, -7.022) | (-0.976, -0.216) |
| MarketCorners decks | LeftMarket under Upgrade (-101.465, 0.3, -7.679); RightMarket under Sell (101.465, 0.3, -7.676); each 24 x 0.6 x 24 + DeckTrim 24.8 x 0.5 x 24.8 | with its stall |
| RichestBoard | pivot (-77.5, 10.2, 63.5) | (0.707, -0.707) |
| SpeedBoard | (-18, 10.2, 63) | -Z |
| HeaviestBoard | (18, 10.2, 63) | -Z |
| TimeBoard | (77.5, 10.2, 63.5) | (-0.707, -0.707) |
| Free Gift | PadRing.Fill centre (0, 0, 56); chest on it | chest faces -Z (toward the spawn) |
| Spawn | SpawnLocation 16 x 1 x 16 at (0, -0.4, 20) | - |
| Plaza medallion | `Decor.Plaza` (5 studded discs, 51.8 wide), centre (0, 0.2, 20) | - |

These match the sketch:
- Front: the Upgrade stall on the left, the Sell stall on the right.
- Middle: the Spawn.
- Back: the boards on the left and right, the Free Gift in the centre.

The stalls sit in the side pockets between plots 1/2 and 5/6, which are off every walking line, so nobody walks
through a ring by accident.

**Decor + seasonal** (`Layout.DECOR / LAMP_SPOTS / ALLEY_BED / HALLOWEEN_BEDS / PUMPKIN_ALLEY / GIANT_PUMPKIN`, per-plot `bed`, `pumpkins`):
- **Permanent decor (`Hub.Decor`):**
  - Corner trees (TreeRound) at (±90, -51) with rocks at (±83, -56.5).
  - Blossom trees at (±86, 73).
  - 4 benches at (±34, 16) and (±11, 48), all facing (0, 20).
  - 6 gate flower beds:
    - Plots 1/3/4/6: 20 x 4.
    - Plots 2/5: 5 x 4 (the corner boards need the room).
    - Each sits on the side of the gate away from the treadmill.
  - The alley bed (8 x 0.8 x 80 at (0, 0.4, 125)): low plants only, so the giant pumpkin stays visible.
- **Seasonal (`HalloweenDecor`):**
  - The GiantPumpkin pivot moves to (0, 64, 230) (it was (0, 64, 169)), keeping its rotation.
  - 8 street lamps at the `LAMP_SPOTS`.
  - 6 pumpkin-egg clusters:
    - 4 on the 20-long gate beds of plots 1/3/4/6 (`PLOTS[i].pumpkins`; plots 2/5 have none).
    - 2 on the alley bed at (0, 117) and (0, 157) (`PUMPKIN_ALLEY`). They are a "pumpkin lane" to the giant pumpkin.
  - 3 low Halloween beds at (0, 70), (0, 100) and (0, 140).
  - 4 spiders hanging from lamps 5-8.

**Ground, edges, bounds** (`Layout.GROUND / EDGES`):
- **Ground:** 3 tiles, top y 0, 8 thick:
  - GroundFront: x -215..215, z -60..12.
  - GroundMid: x -183..183, z 12..78.
  - GroundBack: x -73..73, z 78..171.
- **Edge walls:** 13 low walls (2 thick, 4 tall), built outside the floor along the outline. They skip the runway
  mouth (x -81..81 at z -60), where the runway walls and gate already close it.
- **Bounds:** 13 invisible `Map.Bounds` columns (4 thick, y 0..1040) just outside the walls.
- **Runway bounds:** `Runway_L_1` / `Runway_R_1` are cut back to end at z -60 (today they end at -49, inside the new
  plaza).

---

## Instance / file map

| What | Where | Task |
|---|---|---|
| Layout data (generated) | `ServerStorage.HubV2Kit.Layout` (ModuleScript, source = `docs/plans/hub-2026-10-21/HubLayout.lua`) | 0 |
| Validator | `ServerStorage.HubV2Kit.Validate` (ModuleScript, new) | 3 |
| Vetted prop templates | `ServerStorage.HubV2Kit.Templates.*`, quarantine `HubV2Kit._Quarantine` | 6 |
| Play test suite | `ServerStorage.HubV2Tests` (ModuleScript, new) | 10 |
| Skin-ready plot | `ServerScriptService.BaseBuilder` (modify) | 1 |
| 6 bases, debug hooks | `ServerScriptService.BaseManager` (modify) | 2 |
| Egg refit on load + reload hook | `ServerScriptService.BaseHatchery` (modify `loadBase` ~796-809, Studio debug ~995-1008) | 2 |
| Trailer re-pointing | `ServerStorage.AdminUI.Trailer` (modify ~568-575, ~615-616, ~1211-1215) + local `Desktop/SLINGSHOT Creatures/trailer/studio/Trailer.lua` | 8 |
| Staging hub | `workspace.Map.HubV2` (Model) -> `workspace.Map.Hub` (Folder) at the swap | 3-9 |
| Seasonal layer | `Map.HubV2.HalloweenV2` -> `workspace.HalloweenDecor` at the swap | 6, 9 |
| New bounds | `Map.HubV2.BoundsV2` -> `Map.Bounds.Hub_E1..Hub_E13` at the swap | 3, 9 |
| Backups | `ServerStorage._Backup_HubV2.{Scripts, Stage*}`, `ServerStorage._Backup_Hub.Before` (old Hub + HalloweenDecor + old bounds) | all |
| Ledger | `docs/plans/2026-10-21-redesigned-hub.progress.md` | all |
| Review shots | `docs/reviews/2026-10-21-redesigned-hub/` | 7, 11 |

**Scripts checked and needing NO change**, because names, tags and attributes are kept. Each one is still re-tested
in Task 10:
- TreadmillServer, TreadmillClient, TreadmillSignClient, ShopClient (UpgradeSigns by BaseId).
- TutorialClient (SAFE = (0, 2, -52), PAD, UpgradeZone, treadmill and floor are all looked up live) and TutorialServer.
- IntroCutscene: its hard-coded START (5, -4), HOP_FROM (0.5, -30) and FINISH (-6, -22) and its cameras all stay inside
  the kept-clear intro corridor and launch zone. Its occluder fade covers Hub.Decor, MarketCorners and HalloweenDecor,
  so all new props live there.
- OfflineClient (`Base<id>.Plot.Floor`), BaseSpawnCamera, BaseSignFloat, HatchClient.
- UpgradeClient / SellClient (zones found by name under Hub.Stalls), FreeGiftServer (snaps the zone onto
  PadRing.Fill) and FreeGiftClient.
- Leaderboards (scans workspace for the `Leaderboard` attribute), LeaderboardScroll.
- MapGuard (Map.Bounds + a raycast on Map; `map:FindFirstChild("Spawn", true)`), VipClient (the VIP rooms are on the
  runway).
- AutoReconnectServer (`ServerStorage.MountTreadmill`), SlingshotServer / Client (GateZ, tag lookup in workspace).
- EggSpawner (banks at GateZ + 2), WaveServer / WaveConfig, Weather* (runway areas only).
- HalloweenClient (pivot-relative head, bats and lights), BrickUI.Hatch (only checks that HalloweenDecor exists).
- PetPlaceClient / EggPlaceClient (the floor plane + `findSpot`).

---

### Task 0: Pre-flight, baseline, kit

**Files:** create `ServerStorage.HubV2Kit` (Folder) with `Layout` (ModuleScript), `Templates` (Folder) and
`_Quarantine` (Folder); create `ServerStorage._Backup_HubV2` with `Scripts`; create the ledger file.

**Interfaces:**
- Produces: `Layout` (see `HubLayout.lua`: `Layout.OFFSET`, `Layout.stage(cf)`, `PLOTS[i].{slot, gate, spawnSpot,
  treadmill, treadExit, sign, bed, bedSize, pumpkins}`, `STALLS`, `BOARDS`, `FREE_GIFT`, `SPAWN`, `MEDALLION`, `DECOR`,
  `LAMP_SPOTS`, `ALLEY_BED`, `GIANT_PUMPKIN`, `HALLOWEEN_BEDS`, `GROUND`, `EDGES`, `RUNWAY_BOUNDS_FIX`, `SIZES`,
  `LAUNCH_ZONE`, `INTRO_ZONE`, `ENTRY`, `GATE_EDGES`, `LINE_HALF`).
- Produces: `docs/plans/2026-10-21-redesigned-hub.progress.md` with the baseline numbers below.

- [ ] **Step 1: Re-check the layout and regenerate the module**
  - Run: `cd "Desktop/SLINGSHOT Creatures/docs/plans/hub-2026-10-21/tools" && python hub_layout.py && python make_layout_lua.py`.
  - Expected: `ALL PASS` (49 PASS lines) and `HubLayout.lua` rewritten.
- [ ] **Step 2: Put `HubLayout.lua` into `ServerStorage.HubV2Kit.Layout`**
  - Edit-mode check: `require(Layout:Clone())` returns `#PLOTS == 6`.
  - Check: `PLOTS[1].slot.LookVector:FuzzyEq(Vector3.xAxis, 1e-3)`.
  - Check: `(PLOTS[1].slot * CFrame.new(0, 0, -45)).Position` ≈ `PLOTS[1].gate + (0, 0.1, 0)`.
- [ ] **Step 3: Check the grep (expected unchanged since planning)**
  - Search every LuaSourceContainer (not `_Backup*`, not `ESCAPE TSUNAMI`, not the Satchel/PlayerModule packages) for
    `PivotTo(`, `MoveTo(` and `CFrame.new(<number>` lines that hold literal hub-area coordinates (|x| < 250 and
    -70 < z < 260).
  - Expected hits: IntroCutscene (START/HOP_FROM/FINISH/cameras: kept clear by the layout), Trailer (Task 8), and the
    dev tools `_GrimeRolloutEngine` / `AutoReconnectTests` (Spawn by name).
  - Anything else: stop and add it to Task 8 before going on.
- [ ] **Step 4: Record the baseline in the ledger (Edit + Play, TestFreshSave true)**
  - **Edit:** workspace BaseParts, instances, `Map.Hub` parts and `HalloweenDecor` instances.
    - Planning values (2026-10-21): 4,637 / 10,936 / 2,015 / 6,004.
  - **Play client:** the average RenderStepped dt over 10 s with the camera held at (0, 40, -80) looking at (0, 0, 40)
    (shot camera via `BindToRenderStep(Last+50)`), and `Stats:GetTotalMemoryUsageMb()`.
  - **Pass counts of the existing suites:**
    - `AutoReconnectTests`, `TutorialV11Tests.live`, `RebirthV6Tests`, `StreakTests`, `StarterPackTests`.
    - Run them as their headers say. Record each `pass/fail` total.
- [ ] **Step 5: Ledger line** `Task 0 done: baseline <numbers>`.

### Task 1: BaseBuilder - the skin-ready plot

**Files:** Modify `ServerScriptService.BaseBuilder` (189 lines): `Build` (137-186) and a new `BaseBuilder.BuildLook`.
Backup first.

**Interfaces:**
- Consumes: `baseModel.Slot`; attributes `MaxWidth`, `MaxLength`, `BaseId`.
- Produces: `BaseBuilder.Build(baseModel, width, length, style?, accent?) -> Model` (unchanged signature). It
  creates `baseModel.Plot` with:
  - `Floor` (the gameplay slab: same size, CFrame, collision and CanTouch as today, plus `Transparency = 1`).
  - `Fence` (unchanged: rails/pickets/posts/caps/Colliders/GateDoor).
  - `Look`.
- Produces: `BaseBuilder.BuildLook(plot: Model, root: CFrame, width: number, length: number, slot: BasePart,
  accent: Color3) -> Folder`. This is the ONE seam a future skin system replaces. `root` = the floor centre at y 0,
  LookVector toward the gate.
- Produces: `Plot.Look` contents (purely visual; every part CanCollide / CanQuery / CanTouch false, CastShadow false,
  Anchored, Plastic):
  - `FloorTop`: (width, 0.5, length) at the Floor CFrame, Color (80, 165, 62), TopSurface Studs. It carries 7
    Attachments (the decor anchors), local to FloorTop:
    - `CornerFL` / `CornerFR` (∓(w/2-3), 0.25, -(l/2-3)).
    - `CornerBL` / `CornerBR` (∓(w/2-3), 0.25, l/2-3).
    - `BackCentre` (0, 0.25, l/2-6).
    - `GateL` / `GateR` (∓(D.gateW/2+3), 0.25, -(l/2-2)).
  - The trim: a 1.2-wide, 0.3-tall rim on the floor top (y 0.5..0.8), Color (200, 154, 99), TopSurface Studs:
    - `TrimBack`: (width, 0.3, 1.2) at local (0, 0.65, l/2-0.6).
    - `TrimLeft` / `TrimRight`: (1.2, 0.3, length-2.4) at (∓(w/2-0.6), 0.65, 0).
    - `TrimFrontL` / `TrimFrontR`: from the corner to 1 stud short of the gate, i.e. each (w/2 - D.gateW/2 - 1) long,
      centred at ∓(w/2 + D.gateW/2 + 1)/2, z -(l/2-0.6).
  - `SlotBed`: the unclaimed land under the max plot. (slot.Size.X, 0.1, slot.Size.Z) at
    `slot.CFrame * CFrame.new(0, -0.05, 0)`, Color (110, 150, 82), TopSurface Studs.
  - The owner name sign's backing (behind the floating `OwnerSign.Card`, which is 17 x 14 studs at
    `root * (0, floorT + 11, hz)`):
    - `SignBoard`: (18, 15, 0.4) at `root * CFrame.new(0, D.floorT + 11, hz + 0.6)`, Color (58, 36, 24). Its front
      face (LookVector) faces the gate side.
    - `SignFrame`: (18.8, 15.8, 0.3) at `root * CFrame.new(0, D.floorT + 11, hz + 0.85)`, Color = `accent`.
    - `SignPostL` / `SignPostR`: (0.8, 3.5, 0.8) at `root * CFrame.new(∓7, D.floorT + 1.75, hz + 0.6)`, Color
      (58, 36, 24).
    - `hz = length/2 - D.inset`.

- [ ] **Step 1: Write the failing Edit-mode test** `ServerStorage.HubV2Kit.BuilderTest` (ModuleScript; returns
  `function(): (number, number, {string})`, i.e. pass, fail, lines).
  - **Setup:** it builds a lab base in a `Model` under `workspace` named `_HubV2BuilderLab`.
    - The lab's `Slot` is 60 x 0.2 x 90 at `CFrame.lookAt((5000, 0.1, 5000), (5000, 0.1, 4999))`.
    - Attributes: `BaseId = 1`, `MaxWidth = 60`, `MaxLength = 90`.
    - A plain `OwnerSign` Part (1 x 1 x 1).
  - **Per r = 0..5:** call `require(BaseBuilder:Clone()).Build(lab, w, l, RebirthConfig.fenceStyle(r),
    RebirthConfig.accent(1))` with `(w, l) = RebirthConfig.baseSize(r, 60, 90)`. Assert:
    - `lab:GetAttribute("Width") == w` and `Length == l`.
    - `Plot.Floor.Transparency == 1`, `Plot.Floor.CanCollide == true`, `Plot.Floor.CanTouch == true`,
      `Plot.Floor.Size == Vector3.new(w, 0.5, l)`.
    - The `Look` child names are exactly {FloorTop, TrimBack, TrimLeft, TrimRight, TrimFrontL, TrimFrontR, SlotBed,
      SignBoard, SignFrame, SignPostL, SignPostR}.
    - `Look.FloorTop.CFrame == Plot.Floor.CFrame` and the sizes are equal.
    - `#Look.FloorTop:GetChildren()` = 7 Attachments.
    - Every `Look` BasePart has CanCollide == false, CanQuery == false, CanTouch == false and Anchored == true.
    - The gate edge is fixed: `(Plot.Floor.CFrame * CFrame.new(0, 0, -l/2)).Position` equals
      `(Slot.CFrame * CFrame.new(0, -0.1, -45)).Position + (0, 0.25, 0)` within 0.01, for every r.
    - Every `Plot` BasePart except `Look.SlotBed` lies inside the Slot footprint ± 0.5. Check it in Slot object space:
      |x| ≤ 30.5 and |z| ≤ 45.5.
    - The number of BaseParts under `Plot` is ≤ {310, 380, 700, 860, 940, 610}[r+1].
      - Expected exactly: 295 / 358 / 669 / 822 / 894 / 575 (`tools/fence_parts.py`: fence + floor, plus the 11
        Look parts).
      - The model was checked against Studio: a 40 x 40 picket plot = 512 BaseParts, the same as today's Edit-time
        Base2.
  - **Cleanup:** destroy the lab.
- [ ] **Step 2: Run it** (Edit, `execute_luau`: `return require(game.ServerStorage.HubV2Kit.BuilderTest:Clone())()`).
  - Expected: FAIL on `Floor.Transparency` and on the `Look` children.
- [ ] **Step 3: Implement it.**
  - `floor.Transparency = 1` right after the floor is made.
  - `BaseBuilder.BuildLook(plot, root, width, length, slot, ST.cap)` is called after the gate door and before
    `plot.PrimaryPart = floor`.
  - `part()` is reused for the Look parts with `collide = false`, then `p.TopSurface = Enum.SurfaceType.Studs` where
    the list above says Studs.
  - Header comment: `-- (2026-10-21) redesigned hub: Floor = invisible gameplay slab; everything visual of a plot is in Plot.Look (skin-ready, BuildLook)`.
- [ ] **Step 4: Run the test.**
  - Expected: all PASS for r = 0..5, and `_HubV2BuilderLab` is gone afterwards.
- [ ] **Step 5: Live check on the OLD hub** (the change must be backward compatible).
  - In Edit, rebuild `Hub.Bases.Base2` once with `require(BaseBuilder:Clone()).Build(base, 40, 40)`.
  - Expected: it looks as before (grass visible via FloorTop) and the old `MaxWidth 64 / MaxLength 80` still work.
  - Take a screen_capture at (−6, 40, −20) → (−6, 0, 36).
- [ ] **Step 6: Checkpoint.** Ledger line `Task 1 done: BaseBuilder Look`.

### Task 2: BaseManager (6 bases, test hooks) + BaseHatchery refit on load

**Files:**
- Modify `ServerScriptService.BaseManager`: line 11 (fallback), `assign` (58-71), and a new Studio-only debug block at
  the end.
- Modify `ServerScriptService.BaseHatchery`: `loadBase` (796-809), and the Studio `HatcheryDebug` (995-1008) gets
  `"reload"`.
- Back up both first.

**Interfaces:**
- Produces: workspace attribute `TestBaseId` (Studio only). A number 1..6 makes `assign` hand out that base first when
  it is free; otherwise the normal order applies.
- Produces: `ServerStorage.BaseDebug` (BindableFunction, Studio only). `Invoke(cmd, ...)`:
  - `"fill", rebirths: number -> number` fake-owns every free base: `Owner = -(1000 + BaseId)`,
    `OwnerName = "Test"..BaseId`, and builds it at `rebirths`. It returns how many it filled. Fake ids never collide
    with Studio test players (-1, -2).
  - `"grow", baseId: number, rebirths: number -> (number, number)` rebuilds any base at that size and returns
    `(Width, Length)`.
  - `"release", baseId: number -> boolean` works for a fake owner only. It sets Owner 0, OwnerName nil, the sign off,
    and rebuilds at R0.
  - `"releaseAll" -> number`.
  - `"state" -> {[baseId] = {owner = number, w = number, l = number}}`.
  - `"reassign", player -> number` = `release(player)` then `assign(player)`. It returns the player's new BaseId
    (0 when every base is taken).
- Produces: `HatcheryDebug:Invoke("reload", player) -> {eggRecord}`. It clears `loadedFor[player]`, runs `loadBase`
  and returns the saved egg records.
- Produces (BaseHatchery, internal): `local function fitEggs(base: Model, data: table): boolean`.
  - For every egg record it takes `world = floor.CFrame:PointToWorldSpace(Vector3.new(rec.x, 0, rec.z))` and
    `spot = BaseConfig.findSpot(floor, world, eggRadius(rec.kg), placed) or world`.
  - It rewrites `rec.x/z` from `floor.CFrame:PointToObjectSpace(spot)` and appends `{x, z, r}` to `placed`.
  - It returns true if any record moved by more than 0.01.
  - `loadBase` calls it right after `fitSlots(player)` and `writeData`s when it returns true.

- [ ] **Step 1: Write the failing tests** `ServerStorage.HubV2Tests` (ModuleScript; `return function(player) -> (pass,
  fail, lines)`; Server context in Play). Sections T2.1-T2.3:
  - **T2.1 BaseManager defaults:** Edit-time read of BaseManager's source must contain `or 60` and `or 90` on the
    `RebirthConfig.baseSize` line.
  - **T2.2 debug hooks.** These work on any hub, so with `n` = the number of `Base`-tagged models (3 now, 6 after the
    swap):
    - `fill(0)` returns `n - 1` (the test player owns one base).
    - `state()` shows `n` owners ≠ 0.
    - `grow(id, 5)` returns that base's (MaxWidth, MaxLength): (64, 80) on the old hub, (60, 90) on the new one.
    - `reassign(player)` returns the player's same BaseId: release frees it and assign takes the only free base
      again.
    - `releaseAll()` returns `n - 1`, then `grow(id, 0)` puts the size back.
  - **T2.3 fit-on-load** (works on the old hub too):
    - Place one 1-KG `WoodEgg` through `HatcheryDebug "place"` at the floor centre.
    - Then, in a later frame, rewrite the player's `BaseData` JSON so that egg's `x = floor.Size.X/2 + 3` (outside
      the fence) and add a second egg record with the same x/z (overlapping).
    - `HatcheryDebug:Invoke("reload", player)`.
    - Assert both records are now `BaseConfig.inside(floor, world, eggRadius(kg))` and at least
      `BaseConfig.SPACING + r1 + r2 - 2` apart.
    - Assert the egg models `BaseContent.Base<id>.Eggs.Egg_<id>` stand at the new spots within 0.1.
- [ ] **Step 2: Run T2.3** (Play, TestFreshSave true; Server-context `execute_luau`:
  `return require(game.ServerStorage.HubV2Tests:Clone())(game.Players:GetPlayers()[1], {only = "T2"})`).
  - Expected: FAIL. There is no `"reload"` command, and the record stays outside.
- [ ] **Step 3: Implement it in Edit.**
  - **BaseManager:**
    - Line 11 becomes `... base:GetAttribute("MaxWidth") or 60, base:GetAttribute("MaxLength") or 90)`.
    - `assign` puts the `TestBaseId` base first when `RunService:IsStudio()`.
    - A `BaseDebug` block guarded by `RunService:IsStudio()` reuses `buildBase` and `setSign`.
  - **BaseHatchery:** add `fitEggs` (above `loadBase`) and the `"reload"` command.
  - Dated comments.
- [ ] **Step 4: Run T2.1, T2.2 and T2.3 again.** Expected: PASS.
- [ ] **Step 5: Checkpoint.** Ledger line `Task 2 done`.

### Task 3: Staging model - ground, edges, bounds, reference, validator

**Files:**
- Create `workspace.Map.HubV2` (Model, `WorldPivot = CFrame.new(Layout.OFFSET)`) with Folders `Ground`, `EdgeWalls`,
  `Decor`, `MarketCorners`, `Bases`, `Treadmills`, `UpgradeSigns`, `Stalls`, `Leaderboards`, `FreeGift`, and Models
  `BoundsV2` and `_StageRef`.
- Create `ServerStorage.HubV2Kit.Validate`.

**Interfaces:**
- Consumes: `Layout`.
- Produces: `Validate(root: Instance, offset: Vector3, mode: "stage" | "live") -> {string}` (failures; empty =
  pass). It runs these checks, in final coordinates (part position − offset):
  1. Every BasePart under `root` is Anchored.
  2. There is no LuaSourceContainer under `root`.
  3. In `stage` mode, there is no CollectionService tag under `root`. In `live` mode, there are only Base on Base<N>,
     Treadmill on Treadmill_B<N>, AdminTreadmill on Conveyor, Slingshot on Slingshot and LaunchPad on LaunchPlatform.
  4. `Bases.Base1..6`:
     - Each exists with BaseId = N, MaxWidth 60 and MaxLength 90.
     - The `Slot` is 60 x 0.2 x 90 and its CFrame equals `Layout.PLOTS[N].slot` (position ±0.05, LookVector ±1e-3).
  5. The plots at 60 x 90 (rectangles from the Slot CFrames) are pairwise ≥ 10 apart.
  6. Gate (= `Slot.CFrame * (0, -0.1, -45)`) to `Layout.SLING` is ≤ 140, and max/min ≤ 1.10.
  7. No CanCollide part (and no part taller than 0.8 above y 0) intersects `LAUNCH_ZONE` or `INTRO_ZONE`. Use
     `GetPartBoundsInBox` with an Include filter on `root`, the box shifted by `offset`. Exceptions: the Slingshot,
     the LaunchPlatform and the Ground parts.
  8. **Walking lines:** for each plot, sweep the oriented box from `Layout.ENTRY` to `PLOTS[N].spawnSpot` (width 12,
     y 0.5..6). Also sweep from each `GATE_EDGES` point (width 6). The sweeps contain no CanCollide part. Exceptions:
     `Treadmill_B<N>`, `UpgradeSign_B<N>`, `GateBed_B<N>` of that plot, Ground, the plot itself, MarketCorners decks,
     medallion discs and the SpawnLocation.
  9. Each walk-in zone centre (`UpgradeZone`, `SellZone`, `FreeGiftZone`) is ≥ `Radius + 6` from every main line
     and ≥ `Radius + 3` from every fan line.
  10. A raycast down from 10 above every `spawnSpot`, `treadExit`, zone centre and LAMP_SPOT (Include `root`) hits a
      `Ground` part. For the zones, a MarketCorners deck or a `PadRing` counts.
  11. For each `EDGES[i]`, at its midpoint 1 stud inside the floor a ray hits Ground. 3 studs outside it, the ray hits
      no Ground.
  12. `Treadmills.Treadmill_B1..6`:
      - Each exists with BaseId = N, `Belt`, `Zone`, `Conveyor`.
      - The pivot equals `PLOTS[N].treadmill` (±0.05).
      - The jump-off spot (`Belt.CFrame * (0, 0, 7.5)`) projected to y 0 is on Ground and outside the plot's Slot.
  13. `UpgradeSigns.UpgradeSign_B1..6` each exist with BaseId = N and `Board.Gui` holding `Box.Label`, `Tiers` and
      `RateRow.Rate` (TreadmillServer.updateSign needs them).
  14. `Stalls.UpgradeStall.UpgradeZone` and `Stalls.SellStall.SellZone` (Radius 6.2), `FreeGift.FreeGiftZone`
      (Radius 7.5) and `FreeGift.PadRing.Fill` exist.
  15. `Leaderboards` holds exactly 4 Models with `Leaderboard` ∈ {Income, Speed, Heaviest, Time}.
  16. Stage mode: `Spawn_V2` (SpawnLocation) exists with `Enabled == false`. Live mode: `Spawn` exists with
      `Enabled == true` and there is no `Spawn_V2`.
  17. The BasePart count under `root` (excluding `Bases.*.Plot`) is ≤ 1,800.
- Produces: `Map.HubV2.Ground.GroundFront/GroundMid/GroundBack`:
  - Plastic, Color (128, 170, 96) (= the old Hub.Floor), TopSurface Studs.
  - At `Layout.stage(GROUND[i].cf)`, size `GROUND[i].size`.
- Produces: `Map.HubV2.EdgeWalls.Edge1..13`:
  - Plastic, Color (96, 132, 170) (= the old walls), TopSurface Studs, at `Layout.stage(EDGES[i].wall)`, size
    `wallSize`, CanCollide true.
  - Each has a `TopTrim` child Part: (wallSize.X, 0.6, 2.6), top at y 4.6, Color = the old
    `Hub.Decor.WallTrim.TopTrim` colour (read it before the swap), Studs.
- Produces: `Map.HubV2.BoundsV2.Hub_E1..Hub_E13`:
  - At `Layout.stage(EDGES[i].bound)`, size `boundSize`.
  - Transparency 1, CanCollide true, CanQuery false, CanTouch false, CastShadow false.
  - `BoundsV2.ModelStreamingMode = Persistent`.
- Produces: `Map.HubV2._StageRef` (all CanCollide/CanQuery false, Transparency 0.5). It is removed at the swap:
  - a pad proxy 19 x 1 x 14 at stage (0.5, 0.5, -45);
  - fork proxies 2 x 26 x 2 at stage (±8, 13, -45);
  - a runway proxy 120 x 0.2 x 60 at stage (0, 0.1, -90);
  - runway wall proxies 22 x 48 x 60 at stage (±70, 24, -90).
- Produces: `Map.HubV2.Decor.Plaza`, a Clone of `Hub.Decor.Plaza` translated by `Layout.MEDALLION - (0, 0.2, -33.5)`
  plus `OFFSET`.
- Produces: `Map.HubV2.Spawn_V2`, a Clone of `Hub.Spawn` at `Layout.stage(Layout.SPAWN)` with `Enabled = false`. It
  is NOT named `Spawn` (MapGuard's `FindFirstChild("Spawn", true)`, and Roblox would spawn players there).

- [ ] **Step 1: Write `Validate`.** Run it on the empty `HubV2`.
  - Expected: failures for checks 4, 12-16 (nothing built yet). No Lua error.
- [ ] **Step 2: Build the Ground, EdgeWalls, BoundsV2, _StageRef, medallion and Spawn_V2.**
- [ ] **Step 3: Run `Validate(HubV2, Layout.OFFSET, "stage")`.**
  - Expected: only checks 4, 12-15 fail (plots, treadmills, signs, stalls, boards not built yet).
  - Checks 1-3, 7, 10 (spawn spots on ground), 11, 16 and 17 pass.
- [ ] **Step 4: Edit screenshot.**
  - `screen_capture` at (2000, 420, 55) → (2000, 0, 55): top-down of the bare plaza.
  - Save to `docs/reviews/2026-10-21-redesigned-hub/stage3_topdown.png`.
- [ ] **Step 5: Checkpoint.**
  - Snapshot `_Backup_HubV2.Stage3_Ground`.
  - Ledger line `Task 3 done: ground/edges/bounds, validator`.

### Task 4: Plots in staging - 6 bases, treadmills, upgrade signs

**Files:** `Map.HubV2.Bases.Base1..6`, `Map.HubV2.Treadmills.Treadmill_B1..6`, `Map.HubV2.UpgradeSigns.UpgradeSign_B1..6`.

**Interfaces:**
- Consumes: `Layout.PLOTS`, `BaseBuilder.Build` (Task 1).
- Produces: `Base<N>` (Model, attribute `_SwapTags = "Base"`, attributes BaseId N, MaxWidth 60, MaxLength 90,
  Owner 0). Its children:
  - `Slot`: a new Part, 60 x 0.2 x 90, Transparency 1, CanCollide/CanQuery/CanTouch false, at
    `Layout.stage(PLOTS[N].slot)`.
  - `OwnerSign`: a Clone of `Hub.Bases.Base1.OwnerSign` with its `Card` (Enabled false, Avatar "", PlayerName "").
  - `Plot`: built by `BaseBuilder.Build(base, 40, 40, RebirthConfig.fenceStyle(0), RebirthConfig.accent(N))`, so the
    Edit map shows R0 plots like today.
- Produces: `Treadmill_B<N>`:
  - A Clone of `Hub.Treadmills.Treadmill_B1` (Tier 1). Strip tags, and set
    `_SwapTags = "Treadmill"` on the model and `_SwapTags = "AdminTreadmill"` on its `Conveyor`.
  - Attributes BaseId N, Tier 1, TierName "x1", SpeedPerSecond 50000, LabelHeight 8.5.
  - `PivotTo(Layout.stage(PLOTS[N].treadmill))`.
- Produces: `UpgradeSign_B<N>`:
  - A Clone of `Hub.UpgradeSigns.UpgradeSign_B3` (the larger 4.0 x 2.6 board, so all six read alike).
  - Attribute BaseId N, `PivotTo(Layout.stage(PLOTS[N].sign))`.
  - Remove its `ClickDetector` if any (TreadmillServer does that at runtime anyway).

- [ ] **Step 1: Run the validator.** Expected: checks 4, 12, 13 fail.
- [ ] **Step 2: Build the 6 bases, treadmills and signs.**
- [ ] **Step 3: Validator.**
  - Expected: checks 4, 5, 6, 12 and 13 pass, and so do checks 8-11 for the plot items.
  - Only checks 14-15 still fail.
- [ ] **Step 4: Growth preview (Edit).**
  - For N = 1..6 and r = 0..5: `require(BaseBuilder:Clone()).Build(base, SIZES[r].X, SIZES[r].Y, ...)`.
  - Assert the Plot BaseParts stay inside the Slot ±0.5 and every pair of plots stays ≥ 10 apart (Plot bounding boxes in
    Slot space).
  - Then rebuild all at R0.
  - Take a top-down screenshot at R5 (`stage4_r5_topdown.png`) before rebuilding.
- [ ] **Step 5: Checkpoint.**
  - Snapshot `Stage4_Plots`.
  - Ledger line `Task 4 done: 6 plots`.

### Task 5: Plaza items in staging - stalls, decks, boards, Free Gift

**Files:** `Map.HubV2.Stalls.{UpgradeStall, SellStall}`, `Map.HubV2.MarketCorners.{LeftMarket, RightMarket}`,
`Map.HubV2.Leaderboards.{RichestBoard, SpeedBoard, HeaviestBoard, TimeBoard}`, `Map.HubV2.FreeGift.*`.

**Interfaces:**
- Consumes: `Layout.STALLS`, `BOARDS`, `FREE_GIFT`.
- Produces:
  - **Stalls:** clones of the live stall models with `PivotTo(Layout.stage(STALLS[n].pivot))`. Their PadRing and
    UpgradeZone / SellZone move with them.
    - Remove the stale `_OrigPos` / `_OrigRadius` attributes from the zones.
    - Afterwards the zone centre is within 0.3 of `STALLS[n].ring`.
  - **Decks:** `LeftMarket` / `RightMarket` (Models).
    - `Deck` Part at `Layout.stage(STALLS[n].deck)`, size 24 x 0.6 x 24.
    - `DeckTrim` 24.8 x 0.5 x 24.8 at the same CFrame shifted by (0, -0.1, 0) (the live LeftMarket offset).
    - Colour, material and Studs copied from the live `MarketCorners.LeftMarket.Deck` / `DeckTrim`.
  - **Boards:** clones of the 4 live boards with `PivotTo(Layout.stage(BOARDS[n]))`. Keep the `Leaderboard`
    attribute. The staging boards are drawn too during other agents' Play tests, which is harmless. Strip the legacy
    tags (`GlobalLeaderboard`, `TimeLeaderboard`; no script uses them).
  - **FreeGift:** clones of `Chest`, `FreeGiftZone`, `PadRing`, moved together by
    `T = CFrame.new(stage(Vector3.new(FREE_GIFT.pad.X, oldFillPos.Y, FREE_GIFT.pad.Z))) * CFrame.Angles(0, yaw(look) - yaw(oldChestLook), 0) * CFrame.new(-oldFillPos)`.
    - `yaw(v) = math.atan2(-v.X, -v.Z)`.
    - `oldChestLook` = the live `Chest:GetPivot().LookVector` flattened.
    - `oldFillPos` = the live `PadRing.Fill.Position` (y included, so the heights are kept).
    - Each child gets `PivotTo(T * child:GetPivot())`.

- [ ] **Step 1: Validator.** Expected: checks 14-15 fail.
- [ ] **Step 2: Build the stalls, decks, boards and Free Gift.**
- [ ] **Step 3: Validator.** Expected: ALL checks pass (0 failures).
- [ ] **Step 4: Edit screenshots.**
  - Top-down `stage5_topdown.png`.
  - Close-ups of each stall + ring, the gift and the 4 boards (6 shots) from 1.7 studs eye height at 18 studs away,
    for the visual reviewer.
- [ ] **Step 5: Checkpoint.**
  - Snapshot `Stage5_Plaza`.
  - Ledger line `Task 5 done`.

### Task 6: Props, decor and the seasonal Halloween layer

**Files:**
- `ServerStorage.HubV2Kit.Templates.{TreeRound, Blossom, Rock, Bush, BushSmall, GrassA, GrassB, Bench}`.
- `Map.HubV2.Decor.{Trees, Benches, GateBeds, AlleyBed}`.
- `Map.HubV2.HalloweenV2` (Folder; becomes `workspace.HalloweenDecor` at the swap) with `GiantPumpkin`,
  `StreetLamps`, `PumpkinEggs`, `Garden`, `Spiders`, `SpiderAnchors`.

**Interfaces:**
- Consumes: `Layout.DECOR`, `LAMP_SPOTS`, `ALLEY_BED`, `HALLOWEEN_BEDS`, `GIANT_PUMPKIN`, `PLOTS[N].bed/pumpkins`.
- Produces: templates whose pivot is the ground point under the prop's centre, with LookVector = the prop's front
  (normalise each one with `WorldPivot` once; for a bench, front = where a sitter faces).

**Prop sources, in this order:**
1. **Already in the game** (vetted, the world's own style):
   - `ServerStorage.HalloweenGardenBackup`: TreeRound (14 x 16 x 15), Blossom (10 x 13 x 10), Rock, Bush, BushSmall,
     grass tufts S28_Grass / S31_Grass / S19_Meshesgrass.
   - Clone them. Never move the backup's own items. Strip the `OriginalParent` / `HalloweenDrop` attributes from the
     clones.
   - NO Mushrooms (the owner removed them from the lobby on 2026-10-12).
2. **`ServerStorage.HalloweenTemplates`** for the seasonal layer: Grave_A/B/C, Bush_Thorn, Bramble, TPBush,
   DeadGrass_A/B, StreetLamp, Spider.
3. **Toolbox, benches only.** Use the first candidate that passes vetting:
   - 9717664338 "Studded Park Bench (Can sit)" (1xMilitia; studded, matches the toy-brick look);
   - 23153972 "Park Bench" (Roblox);
   - 393609716 "Park Bench" (AeliteOfficial).
   - If none passes: build a 7-part studded bench from Parts (seat 6 x 0.6 x 2, back 6 x 1.6 x 0.5, 4 legs, Color
     (150, 100, 60)).

**Toolbox vetting rule** (spec §1 + memory `roblox-models-as-files`):
1. `insert_asset` into `ServerStorage.HubV2Kit._Quarantine`, never into workspace.
2. Destroy every LuaSourceContainer, RemoteEvent / RemoteFunction / BindableEvent / BindableFunction, ClickDetector,
   ProximityPrompt, Tool, Humanoid, PackageLink, Sound and value object. Do it in two passes: scripts can hide inside
   MeshParts and Unions.
3. Strip all CollectionService tags and all attributes.
4. Check that `#descendants` of LuaSourceContainer is 0 and that no instance has a name like "Script", "Fix", "Virus",
   "Loader" or "Anti". Reject the asset if it has more than 30 BaseParts (a bench needs at most 12).
5. Set every BasePart to Anchored, CanTouch false, CanQuery false. Use CollisionFidelity Box for MeshParts. Collision
   only on a seat/body collider.
6. Set `SourceAsset = "<id> <creator>"` on the template and move it to `HubV2Kit.Templates`.
7. Delete the quarantine leftovers.

**Placement:**
- **Trees, rocks and benches:** `Layout.stage(DECOR[i].cf)` from the template of `DECOR[i].kind`.
  - Trees keep CanCollide only on the trunk (add an invisible 2 x 8 x 2 `TrunkCollider` if the mesh has no separate
    trunk). Canopies don't collide.
- **Gate beds:** `Decor.GateBeds.GateBed_B<N>`.
  - A soil Part `PLOTS[N].bedSize` (Color (96, 72, 50), Studs) at `stage(PLOTS[N].bed) * (0, 0.4, 0)`.
  - A 0.6-tall border of 4 Parts (Color (150, 150, 155), Studs) 0.4 outside the soil.
  - On it, 2 BushSmall + 3 grass tufts (1 BushSmall + 1 tuft on the 5-long beds).
  - Everything CanCollide false except the border (CanCollide true, 0.6 tall).
- **Alley bed:** `Decor.AlleyBed`, the same build at `stage(ALLEY_BED.cf)` (8 x 0.8 x 80), with 4 BushSmall, 2 Rock
  and 8 tufts. Nothing taller than 6.
- **Seasonal (`HalloweenV2`; all CanCollide / CanQuery / CanTouch false, Box collision):**
  - `GiantPumpkin`: a Clone of the live one with `PivotTo(CFrame.new(stage(GIANT_PUMPKIN)) * oldPivot.Rotation)`.
    Keep `ModelStreamingMode = Persistent`.
  - `StreetLamps.StreetLamp_1..8`: clones of the live lamps with `PivotTo(stage(LAMP_SPOTS[i]))`. Pivot = pole foot;
    the arm points along the LookVector, toward the plaza centre. Keep their PointLight / SpotLight attributes
    (Flicker, NightBrightness, NightRange): the HalloweenClient night boost reads them.
    - Then turn each lamp's `Pumpkin` part in 90° steps about the `Cage` centre until its carved face looks toward
      (0, 20) (memory `roblox-halloween-lamps-grime`). The clones keep the old per-lamp turns.
  - `PumpkinEggs`: the 6 live clusters (Cluster06, 07, 08, 09, 10, 12), in that order, to
    `PLOTS[1].pumpkins`, `PLOTS[3].pumpkins`, `PLOTS[4].pumpkins`, `PLOTS[6].pumpkins`, `PUMPKIN_ALLEY[1]` and
    `PUMPKIN_ALLEY[2]` (all staged).
    - The target CFrame is the cluster's bounding-box bottom centre. Each moves by
      `PivotTo(stage(target) * CFrame.new(0, 0.8 + (oldPivot.Y - oldBoxBottomY), 0) * CFrame.Angles(0, yawDelta, 0))`.
      That puts its base on the bed top (y 0.8) and turns its front toward the target's LookVector.
    - The clusters overhang the 4-wide beds; that's fine, they don't collide.
  - `Garden`: 3 beds at `stage(HALLOWEEN_BEDS[k])`, each a Grave (A/B/C for k = 1/2/3) + a Bush_Thorn / Bramble /
    TPBush + 3 DeadGrass. Fronts face -Z (`CFrame.lookAt(ground, ground + (0, 0, -1))`; front = model LookVector).
  - `SpiderAnchors` (one invisible anchored 1 x 1 x 1 Part at stage (0, -10, 0)) holds 4 Attachments `Thread5..8`
    for lamps 5-8.
    - Each Attachment's WorldPosition = `lamp.Cage.Position + (0, lamp.Cage.Size.Y/2 + 0.4, 0) - lampLook * 1.8`.
    - Set WorldPosition only AFTER parenting (memory gotcha).
    - Then check in a screenshot that the silk starts at the arm. Adjust only the height if not.
  - `Spiders.Spider5..8`: clones of 4 live spiders with `PivotTo(CFrame.new(anchor - (0, 4.5, 0)))`. Their `Silk`
    Beam gets `Attachment0` = the new anchor.
  - **Not re-placed** (they stay in `_Backup_Hub.Before.HalloweenDecor`, because they are mounted on the old 24-48
    stud walls and the new hub has 4-stud edge walls): Garlands, Webs, Vines, WallBats (4,620 instances), Grime.
    Tell the owner (Task 11).

- [ ] **Step 1: Vet the bench, build the templates.**
  - Edit check: `HubV2Kit.Templates` has 0 LuaSourceContainers and 0 tags.
- [ ] **Step 2: Place the permanent decor and the seasonal layer.**
- [ ] **Step 3: Run the validator.**
  - Expected: 0 failures. Check 8 proves no tree trunk, bench, lamp or bed blocks a walking line.
  - Add to `Validate` a check 18: every BasePart under `HalloweenV2` has CanCollide / CanQuery / CanTouch false.
- [ ] **Step 4: Eye-height screenshots (Edit, staging coords).**
  - From each plot's `spawnSpot` + (0, 5, 0) looking at the plaza centre (6 shots).
  - From the plaza centre looking at each plot (6 shots).
  - The alley toward the pumpkin.
  - Save to `docs/reviews/2026-10-21-redesigned-hub/stage6_*.png`.
- [ ] **Step 5: Checkpoint.**
  - Snapshot `Stage6_Decor`.
  - Ledger line `Task 6 done: decor + seasonal`.

### Task 7: Staging visual review (gate before the swap)

**Files:** `docs/reviews/2026-10-21-redesigned-hub/STAGE_REVIEW.md` (written by the reviewer).

- [ ] **Step 1: Hand the Task 3-6 screenshots, `planned_layout.png` and `A_horseshoe.png` to a fresh visual reviewer**
  (`model: "haiku"`, owner rule). Brief:
  - It must match the sketch's U.
  - The toy-brick, studded feel.
  - Nothing floats (raycast list).
  - No prop blocks a gate.
  - The stalls, gift and boards are readable from the spawn.
  - The Halloween layer reads but stays low in the alley.
- [ ] **Step 2: Do every MUST and NICE fix** (the owner wants perfect). Re-run the validator after each batch.
  - Expected: 0 failures.
- [ ] **Step 3: Checkpoint.**
  - Snapshot `Stage7_Reviewed`.
  - Ledger line `Task 7 done: review PASS`.

### Task 8: Re-point the trailer

**Files:** `ServerStorage.AdminUI.Trailer` (backup first) and the local copy
`Desktop/SLINGSHOT Creatures/trailer/studio/Trailer.lua`. Keep them byte-identical (memory `roblox-trailer`).

**Interfaces:**
- Consumes: the live `Map.Hub` names (valid after the swap) and `workspace.HalloweenDecor.GiantPumpkin.Pivot`.
- Produces: three relative rules instead of hard-coded hub coordinates.
  1. **The S6 hatch facing** (~568-575). `hatchFront` = the player's base `Slot.CFrame.LookVector`, flattened and
     unit. The fallback is the old `(0, 0, -33) - c` rule with `(0, 0, 20)` instead of `(0, 0, -33)`. That is the
     plot facing the plaza for any of the 6 plots.
  2. **The S8 treadmill** (~615-616). Use `Treadmills["Treadmill_B" .. player BaseId]`, else `Treadmill_B1`. The
     fallback CFrame becomes `Layout.PLOTS[1].treadmill` written out as
     `CFrame.lookAt(V(-107.7, 0.6, -48), V(-106.7, 0.6, -48))`.
  3. **The S10 Halloween glide** (~1211-1215), relative to the pumpkin. Exact code:

```lua
-- (2026-10-21) relative to the giant pumpkin (it moved with the redesigned hub); with the old pivot (0, 64, 169) this
-- is exactly the old path (-14,7,-44) -> (8,16,26) looking at (0, 18..58, 169)
local u = smooth(ramp(t, T.cut11, T.cut12))
local p = PUMPKIN_AT + V(-14 + 22 * u, -57 + 9 * u, -213 + 70 * u)
local at = PUMPKIN_AT + V(0, lerp(-46, -6, u), 0)
return look(p, at, 0.06 * (1 - u)), lerp(70, 58, u), at
```

  - `PUMPKIN_AT` is read once at the start of `M.play`: the GiantPumpkin `Pivot.Position`, else `V(0, 64, 230)`.
    The model is `ModelStreamingMode Persistent`, so the client has it.
  - S5 (in front of the gate) and S12 (from the runway looking back) need no change. Task 10 checks them.

- [ ] **Step 1: Failing check** (Edit, string test on the Source):
  - The Source contains `V(0, 0, -33)` and `"Treadmill_B2"`, and `V(0, lerp(18, 58, u), 169)`.
  - Expected: present → the "re-pointed" test fails.
- [ ] **Step 2: Make the three edits.** Copy the Source to the local `Trailer.lua`.
- [ ] **Step 3: String test again.**
  - Expected: none of the three old strings remain.
  - `PUMPKIN_AT` is defined once.
  - SHA-256 of the Studio Source == the local file.
- [ ] **Step 4: Checkpoint.** Ledger line `Task 8 done: trailer relative`.

### Task 9: The swap (+ rollback)

**Files:** `workspace.Map.Hub`, `workspace.HalloweenDecor`, `workspace.Map.Bounds`, `ServerStorage._Backup_Hub.Before`.

**Interfaces:**
- Consumes: the reviewed `Map.HubV2` (Task 7), `Layout.RUNWAY_BOUNDS_FIX`.
- Produces: the live hub. Every name the scripts use exists under `Map.Hub`. The tags are live. The old world is in
  the backup with `_RemovedTags`.

- [ ] **Step 1: Pre-swap gates (Edit, nobody in Play).**
  - `Validate(HubV2, OFFSET, "stage")` has 0 failures.
  - The Task 1-2 tests pass.
  - The Task 8 hash matches.
- [ ] **Step 2: Swap, in this exact order, one `execute_luau` call per letter (verify the result before the next):**
  - a. `HubV2:PivotTo(CFrame.new())` (WorldPivot was `CFrame.new(OFFSET)`). Verify `Bases.Base1.Slot.CFrame` equals
    `Layout.PLOTS[1].slot` within 0.01.
  - b. Record `Hub.Slingshot:GetPivot()` and `Hub.LaunchPlatform.CFrame`.
    - Re-parent both into `HubV2` (no movement).
    - Verify both CFrames are unchanged (exact) and that the `Slingshot` tag and the `LaunchPad` tag are still there.
  - c. For every descendant of the old `Map.Hub`:
    - Move its tags into `_RemovedTags` and remove them.
    - Rename it `Hub_Old` and parent it to `ServerStorage._Backup_Hub.Before` (create the folders).
  - d. The same for `workspace.HalloweenDecor` → `_Backup_Hub.Before.HalloweenDecor`.
  - e. Bounds:
    - Move the 7 `Map.Bounds.Hub_*` parts to `_Backup_Hub.Before.Bounds`.
    - Move `HubV2.BoundsV2` children into `Map.Bounds`.
    - For `Runway_L_1` / `Runway_R_1`: store `_OrigSize` / `_OrigCFrame` attributes, then set
      `Size = (22, 1000, 1206)` and `CFrame = CFrame.new(±70, 540, -663)` (zMin -1266, zMax -60).
  - f. `HubV2.HalloweenV2.Parent = workspace`, `Name = "HalloweenDecor"`.
  - g. Destroy `HubV2._StageRef` and the empty `HubV2.BoundsV2`.
  - h. Create a Folder `Hub` in `Map` and move every child of `HubV2` into it. Destroy the empty `HubV2`.
  - i. For every descendant of `Map.Hub` with `_SwapTags`, `AddTag` each tag and clear the attribute.
    `Spawn_V2.Name = "Spawn"`, `Enabled = true`.
- [ ] **Step 3: Live validation.**
  - `Validate(Map.Hub, Vector3.zero, "live")` has 0 failures.
  - **T9.4 tag census:**
    - `GetTagged` counts: Base 6, Treadmill 6, AdminTreadmill 6, Slingshot 1, LaunchPad 1, LaunchGate 1.
    - Every one `:IsDescendantOf(workspace)`.
    - 0 tagged instances under `ServerStorage._Backup_Hub`, `_Backup_HubV2` and `HubV2Kit`.
- [ ] **Step 4: Checkpoint.** Ledger line `Task 9 done: SWAPPED <time>`.

**Rollback (one `execute_luau` per line, Edit only):**
1. Move `Map.Hub.Slingshot` and `Map.Hub.LaunchPlatform` to a temp Folder in workspace (no movement).
2. Strip the tags of `Map.Hub` into `_RemovedTags`, rename it `Hub_New` and parent it to
   `ServerStorage._Backup_Hub.After`. Do the same for `workspace.HalloweenDecor` → `_Backup_Hub.After.HalloweenDecor`.
3. Parent `_Backup_Hub.Before.Hub_Old` to `Map` and rename it `Hub`. Re-add every `_RemovedTags`. Parent the old
   HalloweenDecor to workspace.
4. Parent the Slingshot + LaunchPlatform back into `Map.Hub`. Verify the CFrames.
5. Bounds: move `Hub_E*` → `_Backup_Hub.After.Bounds`, `_Backup_Hub.Before.Bounds.*` → `Map.Bounds`.
   `Runway_L_1` / `R_1` get `_OrigSize` / `_OrigCFrame` back.
6. Optional: restore the 4 script Sources from `_Backup_HubV2.Scripts`. The new code also works on the old hub.
7. Check: `GetTagged("Base")` = 3, all in workspace. Tell the owner.

### Task 10: Play tests (TestFreshSave only)

**Files:** `ServerStorage.HubV2Tests` (extend; Server context), client checks via Client-context `execute_luau`.

**Interfaces:**
- Consumes: `BaseDebug`, `HatcheryDebug`, `MountTreadmill`, `TutorialDebug`, `RebirthDebug`, `OfflineDebug`, workspace
  `TestBaseId` / `TestTutorial` / `TestIntro`, player attribute `IntroDebugT`.

For every session: read TestFreshSave == true in Edit → Play → run → Stop.
`require(HubV2Tests:Clone())(player, {only = "T10.x"})` prints `pass/fail` lines.

- [ ] **T10.1 six bases:**
  - `BaseDebug fill(0)` → 5.
  - `state()`: 6 distinct owners.
  - Every Base has `Width/Length 40`.
  - `TreadmillSignClient` built 6 SurfaceGuis named `TreadmillSign_UpgradeSign_B1..6` (client).
  - `releaseAll()` → 5.
  - Expected: PASS.
- [ ] **T10.2 seventh player:**
  - Recipe (Server context):
    1. `fill(0)`: the 5 other bases get fake owners.
    2. Set the player's own base `Owner = -1007`, which simulates a 7th person holding it. `release(player)` then
       finds no base of theirs.
    3. Wait a frame, then call `BaseDebug:Invoke("reassign", player)`.
  - Expect the return value 0, `BaseId == 0` and the `[BaseManager] no free base` warn line.
  - Then respawn: the character stays near the Spawn (0, 20) ± 12.
  - TutorialClient, OfflineClient and TreadmillServer leave 0 errors in `get_console_output` over 10 s.
- [ ] **T10.3 growth R0 → R5:**
  - `fill(0)`, then for r = 0..5 `grow(i, r)` for all 6.
  - Per r: the sizes equal `Layout.SIZES[r]`.
  - The pairwise Plot gaps are ≥ 10.
  - The fence Colliders lie inside the Slot ±0.5.
  - `OwnerSign` stands within 1 stud of the back fence centre.
  - No Look part overlaps another base.
  - Screenshot at R5 top-down + 2 eye-height shots of the corner pair 1/2.
- [ ] **T10.4 pets fit and wander** (test player at its own base):
  - Set `Rebirths = 20`, then in a later frame give 23 pets with `ServerStorage.GivePet` (CelestialDragon,
    1,000,000 KG).
  - From the client: `RS.Hatchery.PetAction:InvokeServer("equipBest")`.
  - Expect 23 pet models in `BaseContent.Base<id>.Pets`.
  - Sample every pet root every 0.5 s for 20 s: all `BaseConfig.inside(floor, pos, -1)`.
  - Then place 100,000-KG `StormEgg`s with `HatcheryDebug "place"` until "No room".
  - Record the count (informational; expected ≥ 12). Today's 64 x 80 holds about the same.
- [ ] **T10.5 treadmills, signs, re-mount** (6 sessions, one per `TestBaseId = 1..6`, combined with T10.8):
  - `MountTreadmill:Invoke(player)` → true and `TreadmillRun == "Treadmill_B<id>"`.
  - Speed rises within 1 s.
  - `TreadmillTier = 2` (a later frame): the model has `Tier 2`, the same pivot ±0.01, and the player is re-mounted.
  - The sign attributes are `NowName "x2"`.
  - Jump off from the client: the character lands within 1.5 of `Layout.PLOTS[id].treadExit` + (0, 3, 0) and stays
    put for 2 s (no MapGuard teleport).
  - Also run `AutoReconnectTests` in Edit (with `workspace.AutoReconnectTest` set) with the Task 0 pass count. The
    re-mount path is `MountTreadmill`, already covered here; a real teleport can't happen in Studio, so the owner
    tests that live.
  - **Streaming** (the hub is now 430 wide): from the client, standing at the session's spawn spot, all 6
    `Treadmills.Treadmill_B*.Belt`, all 6 `Bases.Base*.Plot.Floor` and all 4 boards' SurfaceGuis exist within 5 s
    (`WaitForChild`). TreadmillClient, TreadmillSignClient and TutorialClient rely on them.
- [ ] **T10.6 bounds and edges:**
  - For each `EDGES[i]` midpoint, put the character 1.5 studs inside the floor edge for 2 s: it is not moved.
  - Put it on the wall top centre (y 4 + 3): MapGuard moves it within 0.6 s.
  - Put it 2 studs outside the Bounds column at y 10: it is put back.
  - At (±70, 3, -55) (the old Runway_L_1/R_1 overlap): it is not moved for 2 s.
- [ ] **T10.7 walker (no stuck spots, the walking lines are clear):**
  - Freeze the owner input (CAS 9000 sink).
  - `Humanoid:MoveTo` between every ordered pair of {pad edge (0.5, -36), Spawn, UpgradeZone, SellZone, FreeGiftZone,
    the 6 spawn spots}.
  - Each leg reaches within 3 studs in `dist / WalkSpeed + 3` s (re-issue MoveTo every 7 s).
  - Expected: 110 legs reached. A failure names the blocking part (raycast along the leg).
- [ ] **T10.8 tutorial in every plot** (the same 6 sessions as T10.5; `TestTutorial = true`, `TestIntro = false`). The
  recipe from memory `roblox-tutorial`:
  - `HatcheryDebug "give"` → step 5: the target is within 3 of the own `Plot.Floor.Position + (0, 2, 0)`.
  - Teleport into the base → steps 6/7. `HatcheryDebug "place"` + `"hatchAll"` → step 8: the target is within 3 of
    `UpgradeZone.Position + (0, 2, 0)`.
  - Teleport into the UpgradeZone → `Upgrades.Buy("Sling")` (free) → step 9: the target is within 3 of the own
    `Treadmill_B<id>.Belt.Position + (0, 3, 0)`.
  - `MountTreadmill` 6 s → step 10: the target is the UpgradeZone.
  - Read the target from the client at `workspace.TutorialGuide.Target.Position`.
- [ ] **T10.9 intro cutscene** (1 session, `TestIntro = true`, `TestTutorial = true`):
  - Freeze frames with `IntroDebugT` = 0.5, 2.0, 2.8, 3.5, the T.gate value and T.outro - 0.3 (the last two from the
    `IntroTimeline` attribute).
  - Expected: the slingshot fills shot 1, and no plot, board or stall stands between the lens and the avatar.
  - Lamps may fade (the occluder fade).
  - The real character takes over at FINISH with no fall.
- [ ] **T10.10 trailer** (owner account in the session; `TestFreshSave` true):
  - `task.spawn(require(player.PlayerGui.AdminUI.Trailer).play)` with `TrailerDebugT` = 12.6 (S5), 13.8 (S6),
    19.5 (S8), 25.5 and 27.0 (S10) and 31.0 (S12).
  - Expected: the hatch is on the own plot facing the plaza, the treadmill is the own one, the S10 glide goes through
    the alley to the pumpkin without clipping, and S12 shows the slingshot + the pumpkin.
- [ ] **T10.11 hub items:**
  - Teleport into each ring: UpgradeUI.Enabled, the Sell window and the Free Gift window open.
  - 8 studs out: they close.
  - After 6 s each board's list shows `Row01` (Leaderboards drew it).
  - The `FreeSign` billboard sits over the chest within 1 stud in XZ (FreeGiftServer snap).
  - Night: set `Lighting.NightMode` via the Settings TIME toggle; the lamps' PointLights reach their NightBrightness
    values.
- [ ] **T10.12 regression:** run the Task 0 suites. Expected: the same pass counts as the baseline.
- [ ] **Step final:**
  - Set `TestFreshSave = false` after the last Play.
  - Remove the `studiotest_` keys this session made (memory `roblox-data-wipe` recipe:
    `ListKeysAsync("studiotest_", nil, nil, true)` + `RemoveAsync`).
  - Ledger line `Task 10 done: <counts>`.

### Task 11: Performance, final screenshots, owner handoff

**Files:** `docs/reviews/2026-10-21-redesigned-hub/{topdown.png, plot1..6_eye.png, plaza_from_plot1..6.png,
night_topdown.png, night_plaza.png, perf.md}`, the memory note.

- [ ] **Step 1: Worst-case performance** (Play, TestFreshSave). Measure with `BaseDebug fill` + `grow(i, 4)` for all 6
  (R4 = the most parts per plot, 883). Same camera as Task 0:
  - Workspace BaseParts ≤ 11,000.
  - Workspace instances ≤ the Task 0 baseline + 3,000. Dropping WallBats, Garlands and Grime saves about 5,000.
  - Average frame time ≤ baseline + 2.0 ms.
  - `GetTotalMemoryUsageMb` ≤ baseline + 60 MB.
- [ ] **Step 2: If any budget fails:**
  - In BaseBuilder `run()`, cap the pickets per section with `math.min(3, ...)` (about -25% fence parts on R2-R4).
  - Re-run the Task 1 test (raise nothing) and Step 1. The picket look stays the same from 10+ studs.
- [ ] **Step 3: Final screenshots** (Play shot camera; Day + Night):
  - Top-down from (0, 420, 55).
  - Eye height from every plot's spawn spot toward the plaza.
  - From the plaza centre toward every plot.
  - Night top-down + plaza.
  - Send them to a fresh visual reviewer (`model: "haiku"`). Fix MUSTs, then re-shoot.
- [ ] **Step 4: Owner handoff.**
  - Update memory `roblox-redesigned-hub.md` + the MEMORY.md index line: what moved, the layout file, the backups,
    rollback, and the dropped Halloween wall items.
  - Write the owner checklist below into `docs/HUB_V2_OWNER_CHECKLIST.md`.
  - Ledger line `Task 11 done`.

---

## Risks

1. **Tagged copies in ServerStorage hijack GetTagged:** BaseManager would hand out a backup base and TreadmillServer
   would swap a backup treadmill. Mitigation: no tags in staging, tags stripped into `_RemovedTags`, T9.4 census.
2. **Runway bounds overlap:** `Runway_L_1` / `R_1` reach z -49, which is inside the new front band, so MapGuard would
   teleport players there. Mitigation: shortened at the swap; T10.6.
3. **Staging spawn:** a staging SpawnLocation would be used by Roblox spawning in other agents' tests. Mitigation:
   `Spawn_V2` with Enabled false until the swap.
4. **Old egg records** land outside the new fence. Mitigation: `fitEggs` (T2.3).
5. **Part count:** six grown picket fences (up to 883 parts each). Mitigation: the budget plus the picket cap
   fallback (Task 11).
6. **Server size above 6:** players 7+ get no plot. It is handled gracefully (T10.2), but the owner MUST set 6.
7. **Owner hand edits after the swap:** the validator and tests check rules, not decor positions. Re-run
   `Validate(Map.Hub, Vector3.zero, "live")` after any owner edit.
8. **Edit require cache:** the BaseBuilder and RebirthConfig tests use clones.
9. **Another agent in Play:** build only in Edit, one builder in Studio, and start after the HATCH NIGHT Gift window.
10. **Halloween wall items dropped:** Garlands, Webs, Vines, WallBats and Grime are dropped because the new walls are
    low. The owner is told and the backup keeps them. Ask the owner where to put them if they want them back.
11. **The trailer's local copy drifts** from Studio. Mitigation: a hash check in Task 8.
12. **Studs on cylinders:** surfaces don't render on cylinders, so the medallion keeps its `MaterialVariant "Studs"`.

## Owner actions (to `docs/HUB_V2_OWNER_CHECKLIST.md`)

1. **Creator Hub** > SLINGSHOT > the start place > Settings / Places > **Server size (Max players) = 6**. It can't be
   set from Studio. Without it, players 7+ have no plot.
2. Look at the review shots and walk the hub in Studio Play (TestFreshSave stays on for testing).
3. **Save, then Publish, then Migrate to Latest Update.** Returning players' eggs refit to the new plots on their own.
4. **After October:** delete `workspace.HalloweenDecor` (the lamps go with it). The 8 lamp spots are in the plan
   (`LAMP_SPOTS`) if you want plain lamps there later. The garlands, webs, wall bats and grime are kept in
   `ServerStorage._Backup_Hub.Before.HalloweenDecor`.
5. **Rollback** if anything is wrong live: ask for "hub rollback" (plan Task 9), then Save + Publish.

## Self-review (spec coverage)

| Spec | Where |
|---|---|
| §1 6 players; owner sets server size | Layout (6 plots), T10.1-T10.2, Owner action 1 |
| §1 Runway / Slingshot / LaunchPlatform fixed | Global Constraints, Task 9 step 2b (exact CFrames), checker LAUNCH_ZONE |
| §1 Horseshoe; 60 x 90; basic identical plots; no paths; Toolbox vetted; Halloween one folder | Layout, Tasks 1, 4, 6, 9 |
| §2 Plaza front/middle/back items, MarketCorners, decor off walking lines | Layout tables, Tasks 5-6, validator check 8, T10.7 |
| §2 Plots ≥ 10 apart, gates face the plaza, treadmill + sign at the gate corner | Layout (checker 1, 8, 9), validator 5, T10.3 |
| §2 Walk ≤ ~140 and fair | Layout (≤ 129.5, max/min 1.058), validator 6 |
| §2 Edges + bounds + MapGuard | Task 3 (walls, BoundsV2), Task 9 step 2e, T10.6 |
| §3 Skin-ready `Look`, gameplay parts outside | Task 1 |
| §4 BaseManager/BaseBuilder 6 bases, 60 x 90, growth, assign/release | Tasks 1-2, T10.1-T10.3 |
| §4 Treadmills, AutoReconnect re-mount, upgrade signs | Task 4, T10.5 |
| §4 Stalls + rings, leaderboards, Free Gift, spawn + BaseSpawnCamera | Tasks 3, 5, T10.11, T10.8 |
| §4 IntroCutscene, Trailer, Tutorial, Offline line, Weather, Thumbnail-stage tags | Kept-clear corridor + T10.9; Task 8 + T10.10; T10.8; no change (Plot.Floor); runway only; tag rules + T9.4 |
| §4 HalloweenDecor (lamps, grime, spiders, garlands) | Task 6: lamps + spiders re-placed; grime + garlands dropped with reason (Risk 10) |
| §5 Staging HubV2, backup `_Backup_Hub.Before`, staged pipeline, visual review, perf | Tasks 3-11 |
| §6 Every test bullet | T10.1-T10.12, Task 11 |
