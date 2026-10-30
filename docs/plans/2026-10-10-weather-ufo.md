# Weather System + UFO Invasion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:**
- Random per-server weather events, with UFO Invasion as the first one.
- A cinematic arrival cutscene that freezes the waves.
- UFOs that catch players and beam up eggs.
- A UFO mutation (x1.5) that goes from the egg to the hatched pet forever.

**Architecture:**
- **Pure rule modules, unit-tested in Edit:** `Mutations`, `WeatherConfig` and `WeatherLogic`.
- **A server core, `WeatherServer`:**
  - schedules weathers and holds the state as workspace attributes;
  - drives one module per weather (`Weathers.UFO`);
  - freezes waves through a new pausable wave clock.
- **Client side:** `WeatherClient` + `Weathers.UFOClient` play the cutscene and draw the HUD and effects.
- **Mutations ride on existing data:**
  - live egg attribute `Mutations`;
  - inventory entries `{kg, mut}`;
  - pet `mut` lists;
  - one income helper `CreatureConfig.petIncome`.

**Tech Stack:**
- Roblox Studio (Luau) through the Studio MCP: `execute_luau`, `multi_edit`, `script_read`, `start_stop_play`, `user_mouse_input`, `screen_capture`.
- Blender MCP for the models.
- The owner's VFX Studio plugin.

**Spec:** `Desktop/SLINGSHOT Creatures/docs/specs/2026-10-10-weather-ufo-design.md`

## Global Constraints
- **Place:** SLINGSHOT, place 97952972919986. Studio ids change on restart, so get the current one from `list_roblox_studios`.
- **Never publish.** The owner saves and publishes.
- **Play-mode switches:** set workspace `TestFreshSave = true` while play-testing and back to `false` after. Never touch real `u_` save keys.
- **The owner often plays in the same Studio session.** Ask before stopping their Play session. Don't move the real mouse (use Studio virtual input).
- **Backups:** before a task edits an existing script, clone it into `ServerStorage._Backup_Weather.Before` (scripts disabled), once per script.
- **VFX:** from the owner's **VFX Studio** plugin only, never hand-made ParticleEmitter "slop".
- **NO GLOW / Neon on meshes.** "Glowing" eggs and pets = VFX Studio effects.
- **Sounds:** licensed Creator Store / Roblox library sounds only (no ripped game/anime audio). Each new id must pass `ContentProvider:PreloadAsync` (Success).
- **Animation:** pull 1-3 clips from animationreference.org first (tags `flying`, `creature-animation`, `impact-frames`) and note the frames. 25 free clip opens per day.
- **UI:** the HUD pill uses the clean potion-pill style (AdminBannerClient). The menu row (Admin) uses the Check-UI builders already in AdminClient.
- **Spec numbers, verbatim:**
  - Schedule: gap 600-1200 s, NO_REPEAT 900 s, duration 300 s, moveEvery 75 s, cutscene 8 s, waveHold 2 s.
  - UFO actions: ufoCount 4, actEvery 20-30 s, playerChance 0.4, ringTime 2 s, liftTime 2 s, catchCooldown 45 s.
  - Throws and eggs: throwWave 25-40 studs, throwFar 120-200 studs, eggBonusTime 30 s.
  - Mutation: UFO mult 1.5.
- **Save compatibility:** inventory entries without a mutation stay plain numbers. A missing `mut` = no mutation. No PlayerData version bump.
- **Test commands:**
  - Edit: `return require(game.ServerStorage.WeatherTests:Clone())()`
  - Play/Server: `return require(game.ServerStorage.WeatherServerTests)()`
  - Existing suites must stay green: `AdminTests` (94), `AdminServerTests` (33).

## Review Focus
1. **A player leaves, dies or respawns while being lifted.** No character is left anchored, nothing errors, and the UFO moves on (test in Task 10).
2. **A weather stops or moves while a UFO is mid-catch or mid-beam.** The player is released on the ground, the egg is set back down, and no orphan models or beams remain (test in Task 10).
3. **One inventory list holds a plain `500` and a mutated `{kg=500, mut={"UFO"}}`.** Placing or selling takes the right one, matched by kg + mutation (test in Task 5).
4. **A frozen wave clock meets admin No Waves / Start a wave and normal wave clean-up.** Waves resume exactly, admin waves spawned while frozen also wait, and nothing lingers forever (test in Task 3).
5. **An egg under the beam hits its despawn timer, or someone tries to pick it up.** Neither can happen until it's back down. A mutated egg gets exactly +30 s (test in Task 4).

---

### Task 1: Mutations module + pet income helper

**Files:**
- Create: `ReplicatedStorage.Mutations` (ModuleScript)
- Modify: `ReplicatedStorage.CreatureConfig` (add `petIncome` next to `income`, line ~139)
- Test: create `ServerStorage.WeatherTests` (ModuleScript returning `function() -> "N passed, M failed\n..."`, same shape as `AdminTests`)

**Interfaces:**
- Produces:
  - `Mutations.TYPES = {UFO = {mult = 1.5, color = Color3.fromRGB(120,255,90), hex = "#78FF5A", tag = "UFO"}}`
  - `Mutations.mult(list: {string}?) -> number` (product of known multipliers; nil/empty -> 1)
  - `Mutations.has(list?, name) -> boolean`
  - `Mutations.add(list?, name) -> {string}` (new table; no duplicates; unknown names ignored)
  - `Mutations.encode(list?) -> string` ("" or "UFO,...", sorted)
  - `Mutations.decode(s: string?) -> {string}` (unknown/blank dropped)
  - `Mutations.key(list?) -> string` (= encode, for matching)
  - `Mutations.label(list?) -> string` (rich text `<font color="#78FF5A">UFO</font> ` per mutation, "" when none)
  - `Mutations.entryKg(e) -> number` (a number -> itself; a table -> `e.kg`)
  - `Mutations.entryMut(e) -> {string}`
  - `Mutations.makeEntry(kg, mut?) -> number | {kg: number, mut: {string}}` (plain number when `mut` is empty)
  - `Mutations.findEntry(list, kg, mutKey) -> number?` (index of the first entry with that kg and `key(entryMut) == mutKey`)
  - `CreatureConfig.petIncome(name, kg, mut?) -> number` = `income(name, kg) * Mutations.mult(mut)`

- [ ] **Step 1: Write the failing tests in `WeatherTests`**
```lua
check("mult none = 1", M.mult(nil) == 1 and M.mult({}) == 1)
check("mult UFO = 1.5", M.mult({"UFO"}) == 1.5)
check("mult stacks (multiply)", (function() M.TYPES.TestX2 = {mult = 2, hex = "#FFFFFF", tag = "X2"}; local v = M.mult({"UFO", "TestX2"}); M.TYPES.TestX2 = nil; return v == 3 end)())
check("add no duplicates", #M.add({"UFO"}, "UFO") == 1)
check("add ignores unknown", #M.add({}, "Nope") == 0)
check("encode/decode round trip", M.encode(M.decode("UFO")) == "UFO" and M.encode({}) == "")
check("decode drops junk", #M.decode("UFO,,Nope") == 1)
check("plain entry stays a number", M.makeEntry(500, {}) == 500 and M.makeEntry(500, nil) == 500)
check("mutated entry is a table", (function() local e = M.makeEntry(500, {"UFO"}); return type(e) == "table" and e.kg == 500 and e.mut[1] == "UFO" end)())
check("entryKg/entryMut on both", M.entryKg(500) == 500 and #M.entryMut(500) == 0 and M.entryKg({kg = 7, mut = {"UFO"}}) == 7)
check("findEntry matches kg + mutation", M.findEntry({500, {kg = 500, mut = {"UFO"}}}, 500, "UFO") == 2 and M.findEntry({500, {kg = 500, mut = {"UFO"}}}, 500, "") == 1)
check("findEntry miss = nil", M.findEntry({500}, 500, "UFO") == nil)
check("label empty / UFO", M.label(nil) == "" and M.label({"UFO"}):find("UFO") ~= nil)
check("petIncome x1.5", math.abs(CC.petIncome("Raiju", 5000, {"UFO"}) / CC.income("Raiju", 5000) - 1.5) < 1e-9)
check("petIncome no mut = income", CC.petIncome("Raiju", 5000, nil) == CC.income("Raiju", 5000))
```
(`M` = a fresh clone of `ReplicatedStorage.Mutations`, `CC` = a fresh clone of `CreatureConfig`. Clone + parent + require + destroy, as in `AdminTests`, because Edit-mode `require` caches.)

- [ ] **Step 2: Run, expect FAIL.** Run the Edit command. Expected: a load error / failures because `Mutations` is missing.
- [ ] **Step 3: Implement `Mutations` and `CreatureConfig.petIncome`** with the signatures above. `CreatureConfig` requires `Mutations` lazily, inside `petIncome`, to avoid a require cycle.
- [ ] **Step 4: Run, expect PASS.** Expected: `15 passed, 0 failed`.

### Task 2: WeatherConfig + WeatherLogic (pure rules)

**Files:**
- Create: `ReplicatedStorage.WeatherConfig`, `ServerScriptService.WeatherLogic` (ModuleScripts)
- Test: add to `ServerStorage.WeatherTests`

**Interfaces:**
- Produces:
  - `WeatherConfig.GAP = {600, 1200}`, `WeatherConfig.NO_REPEAT = 900`, `WeatherConfig.AREAS = 6`
  - `WeatherConfig.TYPES.UFO = {title = "UFO INVASION", duration = 300, moveEvery = 75, cutscene = 8, waveHold = 2, mutation = "UFO", ufoCount = 4, actEvery = {20, 30}, playerChance = 0.4, ringTime = 2, liftTime = 2, catchCooldown = 45, throwWave = {25, 40}, throwFar = {120, 200}, eggBonusTime = 30, icon = "", hex = "#78FF5A"}`
  - `WeatherLogic.nextGap(rng) -> number` (in GAP)
  - `WeatherLogic.pickNext(lastStart: {[string]: number}, now: number, types, rng) -> string?` (only types whose last start is nil or `<= now - NO_REPEAT`)
  - `WeatherLogic.nextArea(current: number?, count: number, rng) -> number` (1..count, `~= current`)
  - `WeatherLogic.canCatch(i) -> boolean`, where `i = {alive, inArea, safe, slingPhase, tutorialDone, beingCaught, cooldownUntil, now}`
  - `WeatherLogic.pickAction(eggCount, playerCount, chance, rng) -> "player" | "egg" | nil`
  - `WeatherLogic.throwKind(rng, waveAhead: boolean) -> "wave" | "far"` ("far" whenever `not waveAhead`)

- [ ] **Step 1: Failing tests** (fixed-seed `Random.new(1)`):
```lua
check("gap in 600..1200", (function() for _ = 1, 200 do local g = L.nextGap(rng); if g < 600 or g > 1200 then return false end end return true end)())
check("never repeats within 900 s", L.pickNext({UFO = 1000}, 1000 + 899, C.TYPES, rng) == nil)
check("allowed after 900 s", L.pickNext({UFO = 1000}, 1000 + 900, C.TYPES, rng) == "UFO")
check("first time allowed", L.pickNext({}, 5, C.TYPES, rng) == "UFO")
check("area always changes", (function() for _ = 1, 200 do if L.nextArea(3, 6, rng) == 3 then return false end end return true end)())
check("area in range", (function() for _ = 1, 200 do local a = L.nextArea(nil, 6, rng); if a < 1 or a > 6 then return false end end return true end)())
local ok = {alive = true, inArea = true, safe = false, slingPhase = "None", tutorialDone = true, beingCaught = false, cooldownUntil = 0, now = 100}
check("catchable", L.canCatch(ok))
local function with(over) local t = table.clone(ok) for k, v in over do t[k] = v end return t end
for _, case in {{"safe", {safe = true}}, {"slingshot aiming", {slingPhase = "Aiming"}}, {"flying", {slingPhase = "Flying"}}, {"tutorial", {tutorialDone = false}},
	{"dead", {alive = false}}, {"other area", {inArea = false}}, {"already caught", {beingCaught = true}}, {"cooldown", {cooldownUntil = 101}}} do
	check("not catchable: " .. case[1], not L.canCatch(with(case[2])))
end
check("no targets -> nil", L.pickAction(0, 0, 0.4, rng) == nil)
check("only eggs -> egg", L.pickAction(3, 0, 0.4, rng) == "egg")
check("only players -> player", L.pickAction(0, 2, 0.4, rng) == "player")
check("no wave -> far", L.throwKind(rng, false) == "far")
```
- [ ] **Step 2: Run, expect FAIL** (missing modules).
- [ ] **Step 3: Implement both modules** with the values and signatures above. `slingPhase` counts as "on the slingshot" for `Aiming`, `Loading` or `Flying`.
- [ ] **Step 4: Run, expect PASS** (Task 1 + Task 2 checks all green).

### Task 3: Pausable wave clock

**Files:**
- Modify: `ReplicatedStorage.WaveConfig` (add `Clock`), `ServerScriptService.WaveServer` (spawn/hit/clean-up use the clock; spawning loop waits while paused; `WavePause` bindable), `StarterPlayer.StarterPlayerScripts.WaveClient` (every `GetServerTimeNow()` used for wave position, holes, banners and hits becomes `Config.Clock()`)
- Test: create `ServerStorage.WeatherServerTests` (Play/Server ModuleScript, same shape as `AdminServerTests`)

**Interfaces:**
- Produces:
  - `WaveConfig.Clock() -> number` = `GetServerTimeNow() - (WavePausedTotal or 0) - ((WavePausedAt or 0) > 0 and (GetServerTimeNow() - WavePausedAt) or 0)`. Workspace attributes: `WavePausedAt` (0 = running) and `WavePausedTotal`.
  - `ServerStorage.WavePause:Invoke(on: boolean) -> boolean`. On: sets `WavePausedAt = now` if not paused. Off: `WavePausedTotal += now - WavePausedAt`, `WavePausedAt = 0`.
  - `spawnWave` stamps `Start = Config.Clock() + lead`.
  - Clean-up waits until `Config.Clock() > start + travel + 3` instead of `task.delay`.

- [ ] **Step 1: Failing Play tests**
```lua
-- spawn a Normal wave via AdminWave, wait 1 s, pause
local front0 = Config.FrontZ(t, start, Config.Clock()); task.wait(2)
check("frozen wave doesn't move", math.abs(Config.FrontZ(t, start, Config.Clock()) - front0) < 0.5)
pause(false); task.wait(1)
check("resumes from the same spot", Config.FrontZ(t, start, Config.Clock()) - front0 < t.Speed * 1.3 and Config.FrontZ(t, start, Config.Clock()) > front0)
-- Review Focus 4: an admin wave spawned while paused waits too; No Waves still clears; clean-up still happens
pause(true); local w2 = AdminWave:Invoke("Normal"); task.wait(1)
check("wave spawned while paused hasn't moved", Config.Clock() <= <w2 Start> + 0.05)
pause(false)
workspace:SetAttribute("Event_NoWaves", true); task.wait(0.3)
check("No Waves still clears", #waves() == 0); workspace:SetAttribute("Event_NoWaves", nil)
check("clock never runs backwards", <Clock sampled 5x over 1 s is non-decreasing>)
```
- [ ] **Step 2: Run in Play, expect FAIL** (`Config.Clock` is nil).
- [ ] **Step 3: Implement** per the Interfaces. In WaveClient, replace the cached `v.start` math so positions use `Config.Clock()`. Banner lead countdowns also use the clock.
- [ ] **Step 4: Run, expect PASS.** Also re-run `AdminServerTests` (33/33; its No Waves checks must still pass).
- [ ] **Step 5: Manual check:** in Play, `WavePause:Invoke(true)` shows a wave visibly stopped on the client (screenshot). Invoke `false` and it continues.

### Task 4: Mutated eggs on the runway + EggBeam

**Files:**
- Modify: `ServerScriptService.EggSpawner`:
  - `readInventory` keeps table entries;
  - `rebuildBackpack` sorts by `Mutations.entryKg`;
  - `makeEggTool(kind, entry)` sets `EggWeight`, `EggMut` (encode) and `MutText` (`Mutations.encode` or "");
  - `bank` inserts `Mutations.makeEntry(weight, decode(egg.Mutations))`;
  - the label title gets `Mutations.label(...)`;
  - new bindables.
- Test: `WeatherServerTests`

**Interfaces:**
- Consumes: Task 1 `Mutations`.
- Produces:
  - Live egg attribute `Mutations` (string).
  - `ServerStorage.WeatherEggs:Invoke(area: number) -> {Model}`: live, on-ground, not-carried eggs in that area.
  - `ServerStorage.EggBeam:Invoke(egg: Model, mutation: string, hoverY: number) -> boolean`:
    - blocks pick-up (prompt disabled) and pauses the egg's countdown;
    - tweens the egg up to `hoverY` over 1.5 s, holds 0.5 s, then back down over 1.5 s;
    - adds the mutation and refreshes the label/prompt text;
    - sets `expires += eggBonusTime` (30);
    - returns false if the egg is gone or already has the mutation.

- [ ] **Step 1: Failing Play tests**
```lua
local egg = WeatherEggs:Invoke(1)[1]
local left0 = <egg Remaining/expires via label or a new attribute "ExpiresAt">
task.spawn(EggBeam.Invoke, EggBeam, egg, "UFO", egg:GetPivot().Y + 20)
task.wait(0.5)
check("can't pick up mid-beam", egg.Hitbox.PickUp.Enabled == false)
task.wait(4)
check("egg has UFO", egg:GetAttribute("Mutations") == "UFO")
check("+30 s on its timer", <expires grew by 30 ± 1>)
check("beaming twice is refused", EggBeam:Invoke(egg, "UFO", 0) == false)
-- bank it: carry + walk-in simulated through the existing carry path (move the test player into the hub with it)
check("banked as {kg, mut}", <EggInventory WoodEgg list contains a table entry with mut {"UFO"}>)
check("tool shows the mutation", <a backpack tool has EggMut == "UFO">)
```
(Expose `egg:SetAttribute("ExpiresAt", state.expires - os.clock() + workspace:GetServerTimeNow())` in `activate`, and update it on bonus/pause, so tests and clients can read the timer.)

- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement.** The egg's countdown loop must skip despawn while `state.beaming` is set (Review Focus 5).
- [ ] **Step 4: Run, expect PASS.** Also run the existing eggs flow manually: pick up, drop and bank a plain egg, and check it still saves as a number.

### Task 5: Mutations through hatchery, pets, income and selling (server)

**Files:**
- Modify: `ServerScriptService.BaseHatchery`:
  - `validate` + `place` take a 4th `mutKey` and remove via `Mutations.findEntry`;
  - `rec.mut`;
  - `hatch` -> `pet.mut = rec.mut`;
  - `spawnPet` sets entry attribute `Mut` = encode;
  - pet tools set `PetMut`;
  - `incomeOf(pet)` -> `CreatureConfig.petIncome(pet.name, pet.kg, pet.mut)`;
  - the line ~522 sort uses `petIncome` with `PetMut`.
- Modify: `StarterPlayerScripts.EggPlaceClient` (InvokeServer adds `tool:GetAttribute("EggMut") or ""`), `ReplicatedStorage.SellConfig` (`eggValue(kind, kg, mut?)`, `petValue(name, kg, mut?)` x `Mutations.mult`), `ServerScriptService.SellServer` (eggs matched with `findEntry`; batch egg items `{kind, kg, mutKey}`; pets pass `pet.mut`).
- Test: `WeatherServerTests`

**Interfaces:**
- Consumes: Task 1, Task 4.
- Produces:
  - `PlaceEgg:InvokeServer(kind, kg, pos, mutKey?)`
  - pet tables `{id, name, kg, mut?}`
  - pet `Configuration` attribute `Mut` (string)
  - Satchel pet-tool attribute `PetMut`

- [ ] **Step 1: Failing Play tests**
```lua
-- inventory {WoodEgg = {500, {kg = 500, mut = {"UFO"}}}}  (Review Focus 3)
local ok = HatcheryDebug:Invoke("place", P, "WoodEgg", 500, floorPos)          -- plain
check("plain egg placed, mutated one left", ok and <inventory WoodEgg == {{kg=500,mut={"UFO"}}}>)
ok = <place via the PlaceEgg path with mutKey "UFO">
check("mutated egg placed, list empty", ok and <inventory WoodEgg empty or nil>)
check("placed record carries mut", <BaseData.eggs[last].mut[1] == "UFO">)
HatcheryDebug:Invoke("hatchAll", P); task.wait(8)
check("pet keeps mut", <BaseData.pets has an entry with mut {"UFO"}>)
check("pet Configuration has Mut", <the base Pets folder entry:GetAttribute("Mut") == "UFO">)
check("income x1.5", <IncomePerSec after the hatch ≈ (plain pet income + 1.5 x UFO pet income) x Money.Multiplier ± 1>)
check("sell value x1.5", SellConfig.petValue("Raiju", 5000, {"UFO"}) == math.floor(SellConfig.petValue("Raiju", 5000) * 1.5 + 0.5) or <within 1>)
check("old plain inventory still loads/places", <a fresh {WoodEgg = {42}} inventory places fine>)
```
(HatcheryDebug "place" needs an optional 5th arg `mutKey`; add it next to `placeForced`.)

- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement** per the Interfaces.
- [ ] **Step 4: Run, expect PASS.** Re-run `AdminServerTests` (give pet / give potion still pass).

### Task 6: Mutation display (client) + aura

**Files:**
- Modify: `ReplicatedStorage.PetTag` (`attach(model, name, kg, height, owner, size, mut?)`: a green `Mutations.label` line above the KG and income via `petIncome`), `StarterPlayerScripts.PetAnimator` (pass `entry:GetAttribute("Mut")`; attach the UFO aura when present), `PetPlaceClient` (pass the tool's `PetMut`), `PetsEggsUI` (sort + earn via `petIncome`; UFO badge), `SellClient` + `InventoryClient` (eggs: iterate entries with `entryKg`/`entryMut`; show a badge; send `mutKey` when selling), `SatchelLoader...satchel` (next to `KgBadge`, a small green `MutBadge` showing `MutText` when non-empty).
- Create: `ReplicatedStorage.WeatherFX` folder (filled in Task 8), here `UFOAura` (placeholder slot).

**Interfaces:**
- Consumes: Tasks 1, 4, 5. Task 8 fills `WeatherFX.UFOAura`; until then the aura code skips when the template is missing.

- [ ] **Step 1: Client check (fails first).** In Play, give the test player a UFO pet (`GivePet` + set `mut` through a debug path), then from the Client: `PetTag` shows "UFO" and `$x1.5`; the hotbar slot has `MutBadge` visible with text "UFO". Expected now: FAIL (no badge, no label).
- [ ] **Step 2: Implement** the display changes.
- [ ] **Step 3: Re-run the check, expect PASS,** and take screenshots: pet tag, hotbar slot, Pets panel, Sell list, Inventory.
- [ ] **Step 4:** Check that plain pets and eggs look exactly as before (screenshot compare).

### Task 7: UFO models (Blender)

**Files:**
- Create: `Desktop/SLINGSHOT Creatures/Weather/UFO/` (`mothership.blend`, `saucer.blend`, FBX exports, renders)
- Studio: `ReplicatedStorage.WeatherAssets.UFO.Mothership`, `...Saucer` (Models)

**Interfaces:**
- Produces:
  - `Mothership`: about 120 studs wide. Child meshes `Hull`, `LightRing` (spins), `BellyDoorL`, `BellyDoorR` (open by rotating), attachment `BeamOrigin`, attribute `Height`.
  - `Saucer`: about 16 studs wide. `Hull`, `Dome`, `RimLights` (spins), attachment `BeamOrigin` (underside centre).
  - Both: PrimaryPart `Hull`, anchored, CanCollide false, CanQuery false. No Neon/glow materials (lights = VFX in Task 8).

- [ ] **Step 1:** Model both in Blender (Blender MCP), styled to match the game's clean, chunky look. Bake a colour palette onto the meshes (no texture images; see the coloured-mesh import notes). Moving parts are separate objects.
- [ ] **Step 2:** Render front, 3/4 and underside of each to PNG and **show the owner. Stop for approval** (they chose custom models; it's their call).
- [ ] **Step 3:** After approval, export FBX, import into Studio, assemble the Models with the names above, and check sizes in a screenshot over the runway.

### Task 8: VFX (VFX Studio) + sounds

**Files:**
- Studio: `ReplicatedStorage.WeatherFX`: `TractorBeam` (Beam/emitters between two attachments), `TargetRing` (ground decal/emitters), `UFOAura` (pet/egg aura), `MothershipLights`, `VortexClouds`, `CutsceneFlash`, `AbductSparkle`
- Modify: `ReplicatedStorage.SFX` LIB: `UFOSiren`, `UFOHum` (loop, 3D), `UFOBeam`, `UFOWarp`

**Interfaces:**
- Produces: effect templates that the runtime clones and enables with `:Emit()` or `.Enabled`. Each has an attribute `Kind = "beam" | "ring" | "aura" | ...`.

- [ ] **Step 1:** Open VFX Studio in the owner's Studio (computer-use with access granted, while the owner is away from the mouse), or ask the owner to insert the chosen presets. Build each effect from its library. Strip any scripts.
- [ ] **Step 2:** Pick 4 licensed sounds (Creator Store / Roblox library, no ripped audio). Each must preload with Success. Add them to `SFX.LIB`.
- [ ] **Step 3:** Screenshot each effect over the runway for the owner.

### Task 9: WeatherServer core (schedule, state, moves, cutscene wave freeze, announcements)

**Files:**
- Create: `ServerScriptService.WeatherServer` (Script), `ServerScriptService.Weathers` (Folder) with `UFO` stub (`start/moveTo/stop` that only print in this task)
- Modify: `StarterPlayerScripts.AdminBannerClient` (Banner kind `"weather"`: no name prefix; `phase = "start" | "move" | "end"` -> "UFO INVASION has begun in WATER!" / "UFOs are moving to FIRE!" / "The UFOs have left!"; title in the weather hex; sound `UFOSiren` on start)
- Test: `WeatherServerTests`

**Interfaces:**
- Consumes: Tasks 2, 3, 8 (sound id).
- Produces:
  - Workspace attributes: `Weather` (string, "" = none), `WeatherArea` (number, 0 = none), `WeatherEnds` (server time), `WeatherCutsceneAt` (server time; clients start the cutscene on change).
  - `ServerStorage.WeatherStart:Invoke(type: string?, area: number?) -> (boolean, string)` (refuses while one runs)
  - `ServerStorage.WeatherStop:Invoke() -> boolean`
  - Weather module interface: `module.start(ctx)`, `module.moveTo(area)`, `module.stop()`. `ctx = {type, cfg, area, areaBounds(area) -> {zMin, zMax, y}}`; bounds come from `workspace.Map.Runway[*].AreaZone`.
  - Studio-only `workspace` attribute `WeatherTestFast = true` -> moveEvery 6 s, duration 20 s (tests).

- [ ] **Step 1: Failing Play tests**
```lua
local ok = WeatherStart:Invoke("UFO", 2)
check("start ok", ok and workspace:GetAttribute("Weather") == "UFO" and workspace:GetAttribute("WeatherArea") == 2)
check("cutscene stamped", math.abs(workspace:GetAttribute("WeatherCutsceneAt") - workspace:GetServerTimeNow()) < 1)
check("waves frozen during cutscene", (workspace:GetAttribute("WavePausedAt") or 0) > 0)
task.wait(8 + 2 + 0.5)
check("waves running after cutscene + 2 s", (workspace:GetAttribute("WavePausedAt") or 0) == 0)
check("second start refused", (WeatherStart:Invoke("UFO")) == false)
-- WeatherTestFast: a move happens and changes the area
check("area moved", <WeatherArea changed within 7 s and ~= 2>)
check("stop clears", WeatherStop:Invoke() and workspace:GetAttribute("Weather") == "" and workspace:GetAttribute("WeatherArea") == 0)
check("schedule respects NO_REPEAT", <after stop, WeatherStart (scheduled path) refuses UFO until 900 s; the manual admin start ignores NO_REPEAT>)
```
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement.**
  - The scheduler loop: first gap `nextGap`; after each event `nextGap`; `pickNext` with `lastStart`.
  - Start: set attributes, `WavePause(true)`, fire the Banner start, call `module.start`. After `cutscene + waveHold`: `WavePause(false)`.
  - Every `moveEvery`: `nextArea`, fire the Banner move, `module.moveTo`.
  - At `duration`: `module.stop`, then the Banner end and clear the attributes.
- [ ] **Step 4: Run, expect PASS;** also screenshot the start announcement bar.

### Task 10: UFO server behaviour (Weathers.UFO)

**Files:**
- Modify: `ServerScriptService.Weathers.UFO` (the real module)
- Test: `WeatherServerTests`

**Interfaces:**
- Consumes:
  - Task 2 (`canCatch`, `pickAction`, `throwKind`)
  - Task 4 (`WeatherEggs`, `EggBeam`)
  - Task 7 models
  - `ServerStorage.DropCarriedEgg`
  - `WaveConfig` (nearest incoming wave via `Clock`, `FrontZ`)
  - `WaveConfig.IsSafe`
- Produces:
  - `workspace.Weather.UFOFleet` (Mothership + 4 Saucers, server models).
  - Player attributes: `UfoRingAt` (server time the ring started; clients draw the ring) and `UfoCaught` (true while lifted).
  - Saucer attributes: `TargetKind`, `TargetName` (for client beams).

- [ ] **Step 1: Failing Play tests** (with `WeatherTestFast`; the test player stands in area 2):
```lua
-- force one catch via a Studio-only bindable WeatherDebug:Invoke("catch", player)
check("eligible player gets a ring", <UfoRingAt set within 1 s>)
check("lifted then thrown", <UfoCaught true during the lift; afterwards root position moved > 25 studs and UfoCaught false/nil>)
check("carried egg dropped at the catch spot", <CarryingEgg nil and an egg near the old spot>)
check("cooldown 45 s", <a second forced catch within 45 s is refused>)
for _, who in {"in a trench", "tutorial (TutorialDone=false)", "SlingPhase=Aiming"} do check("never caught: " .. who, <forced catch refused>) end
-- Review Focus 1: the player resets mid-lift
check("reset mid-lift leaves nothing anchored", <after LoadCharacter mid-lift: new root not anchored, no error in output>)
-- Review Focus 2: WeatherStop mid-lift / mid-beam
check("stop mid-lift releases on the ground", <root unanchored, UfoCaught nil, fleet gone>)
check("stop mid-beam sets the egg down", <egg back on its spot, prompt enabled>)
check("egg action mutates an egg", <WeatherDebug:Invoke("beam") -> some egg in the area gets Mutations "UFO">)
```
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement.**
  - **Fleet:** spawns high over the area. Saucers patrol random points over the area's runway; the mothership drifts high.
  - **Act loop:** each saucer acts every `actEvery`; `pickAction` chooses player or egg.
  - **Player catch:**
    1. Set the ring for `ringTime`.
    2. Re-check `canCatch` (the player may have hidden).
    3. `DropCarriedEgg`, then anchor the root and tween it up `liftTime`.
    4. `throwKind`: "wave" = set down at `front + rng(throwWave)` toward the hub side of the nearest wave whose front is behind the player; "far" = `z - rng(throwFar)`, clamped inside the runway.
    5. Unanchor, apply a small velocity, set the cooldown.
  - **Egg:** `EggBeam` with `hoverY` = the saucer's underside.
  - **Every wait** re-checks that the player/egg and the weather still exist.
- [ ] **Step 4: Run, expect PASS.**

### Task 11: WeatherClient (cutscene, sky tint, pill, rings, beams, abduction pose)

**Files:**
- Create: `StarterPlayerScripts.WeatherClient` (LocalScript), `ReplicatedStorage.Weathers.UFOClient` (ModuleScript)
- Modify: `StarterPlayerScripts.AdminBannerClient` (`placeBoosts` leaves room above for the weather pill: one shared column, weather on top)

**Interfaces:**
- Consumes: Task 9 attributes, Task 10 attributes, Task 8 FX/sounds, Task 7 models (cutscene uses client clones of `WeatherAssets`).
- Produces: `UFOClient.cutscene(area, startAt)`, `UFOClient.ring(player, at)`, `UFOClient.beam(saucer, targetPart)`.

- [ ] **Step 1: References first.** Open 2-3 animationreference.org clips (`/tags/flying` for hovering saucers and a swooping arrival; `/tags/impact-frames` for the title slam). Note the key frames in the task notes (24 fps x 1.25 = 30 fps frames).
- [ ] **Step 2: Implement the cutscene beats exactly as in the spec (0-8 s).**
  - It plays when `WeatherCutsceneAt` changes and the local player is NOT (SlingPhase in Aiming/Loading/Flying or `SlingLocalPhase`) and NOT (`TutorialDone == false`).
  - It runs on a Scriptable camera bound with `BindToRenderStep(..., Last + 50)`, and controls are sunk via ContextActionService. Both are restored at 8 s and on any error (`pcall`).
  - A player who joins mid-cutscene gets none: play only if `GetServerTimeNow() - WeatherCutsceneAt < 1` when the change arrives.
- [ ] **Step 3:** Sky/fog tint while `CurrentArea == WeatherArea` (tween Lighting/Atmosphere, restore on leave/end).
- [ ] **Step 4:** Weather pill: icon + "UFO INVASION · WATER · m:ss" in the AdminBanner column. Hover (PC) / tap (phone) tip: "UFOs grab players and mutate eggs (x1.5)".
- [ ] **Step 5:** Rings under `UfoRingAt` players, beams from saucer `BeamOrigin` to the target, abduction pose (arms up, gentle spin) while `UfoCaught`, hum/beam sounds.
- [ ] **Step 6: Verify:** a full Play run with `WeatherTestFast`. Screenshot every beat: 0 s, 2.5 s, 4.5 s, 7 s, back to the player, a ring, a beam on a player, a beam on an egg, the pill. Check that a player aiming the slingshot gets no cutscene, a TestTutorial player gets none, and the camera/controls always come back.

### Task 12: Admin menu weather row

**Files:**
- Modify: `ServerScriptService.AdminLogic` (`validate("weather", {action = "start" | "stop", weather = "UFO"})`), `ServerScriptService.AdminServer` (`run.weather` -> `WeatherStart` / `WeatherStop`, this server only; ARG_KEYS += "action", "weather"), `ServerStorage.AdminUI.AdminClient` (ADMIN ABUSE: a row "WEATHER  UFO INVASION  [START] [STOP]" under the wave row, fixed text sizes as the rest; `CanvasSize` grows by the row)
- Test: `AdminTests` (validate) and `AdminServerTests` (start/stop)

- [ ] **Step 1: Failing tests:**
```lua
check("weather start ok", (v("weather", {action = "start", weather = "UFO"})) == true)
check("weather bad action", (v("weather", {action = "boom"})) == false)
check("weather unknown type", (v("weather", {action = "start", weather = "Nope"})) == false)
```
plus, in Play, `run(P, "weather", {action = "start", weather = "UFO"}).ok == true` and `Weather == "UFO"`, then stop -> "".
- [ ] **Step 2: FAIL -> implement -> PASS.** AdminTests 97, AdminServerTests 35.
- [ ] **Step 3:** Screenshot the ADMIN ABUSE tab: nothing cut and the text sizes match.

### Task 13: Full regression + owner hand-off

- [ ] **Step 1:** Run all suites: WeatherTests, WeatherServerTests, AdminTests, AdminServerTests. All green.
- [ ] **Step 2:** 2-player Server & Clients test. Player 2 gets caught (ring -> lift -> throw), sees the cutscene, picks up a UFO egg, banks, places and hatches it, and the pet shows UFO + x1.5.
- [ ] **Step 3:** Set `TestFreshSave`/`TestTutorial`/`WeatherTestFast` back to false and clear the `Weather*` / `WavePaused*` attributes in Edit.
- [ ] **Step 4:** Update memory (new `roblox-weather-system.md` + MEMORY.md line) and write a short owner checklist `docs/weather-live-checklist.md`. Remind the owner to save and publish.
