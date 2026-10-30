# Several weathers at once, admin auto-pause, stacked mutations, weather tiles: implementation plan (2026-10-12)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Any number of weathers can run at once (only a lone one gets a cutscene). The owner can start and stop them
together from the Admin panel and pause the hourly weather in every server. The HUD shows one square tile per running
weather in the bottom-right corner. Pets carrying several mutations multiply them (x1.5 x x1.5 = x2.25).

**Architecture:**
- **WeatherServer** keeps a table of running weathers, one entry per type, each with its own area loop and end time.
- **Server attributes:** a sorted comma list (`Weather`) plus per-type attributes. Everything the clients need comes
  from these.
- **Pure rules:** the list helpers live in `WeatherConfig`, which clients can require. The server-only rules live in
  `WeatherLogic`.
- **Admin:** keeps its existing pattern (MessagingService + MemoryStore `AdminEvent`), now with a merged weather record
  and a new `autoWeather` key.
- **Tiles:** a new focused LocalScript, `WeatherTilesClient`. It tells `AdminBannerClient` where its row starts through
  one attribute.

**Tech Stack:** Roblox Luau in Studio through the Studio MCP:
- `execute_luau` (Edit / Server / Client);
- `ScriptEditorService:UpdateSourceAsync` for source edits;
- `start_stop_play`, `get_console_output`, `screen_capture`.

**Spec:** `docs/specs/2026-10-12-weather-multi-design.md`

## Global Constraints
- **Publishing:** never save or publish. The owner does Save + Publish + Migrate to Latest Update.
- **TestFreshSave:**
  - `workspace.TestFreshSave` must be `true` before EVERY Play test. Set it back to `false` after the last one.
  - If the owner is in Play, wait. Never stop their session.
- **Backups:** before a script's first edit, copy it into `ServerStorage._Backup_WeatherMulti.Before`.
  - No git commits: the Studio place is the source of truth, and the Desktop folder sits inside the home-folder repo.
  - Every "Commit" step below = the backup exists + a ledger line in this file.
- **UI:**
  - ALL UI (tiles, tip, admin rows) is built with the `check-ui-clean-roblox` skill: solid `#3B5866` canvas, `#181E22`
    stroke, GothamBlack + black UIStroke, UIScale on a `1050 x 620` baseline clamped `[0.52, 1.18]`, centre-anchored
    hover/click, `ScaleType.Fit` icons.
  - Invoke the skill at the start of Tasks 6 and 7.
- **Weather modules:** the server modules `Weathers.UFO` / `Weathers.Meteor` do not change. The client modules change
  only their cutscene-loop check (Task 5).
- **Attribute names (exact):**
  - `Weather` = the running types, comma-joined and sorted (`""`, `"UFO"`, `"Meteor,UFO"`);
  - `WeatherArea_<T>` (0 = off), `WeatherEnds_<T>` (server time), `WeatherCutsceneAt_<T>` (stamped only when that
    weather plays a cutscene);
  - `WeatherAutoOffUntil` (os.time, 0 = on);
  - `WeatherNextAt` unchanged. The old `WeatherArea` / `WeatherEnds` / `WeatherCutsceneAt` are removed (set to nil).
- **Cutscene rule:** a weather plays its cutscene and freezes the waves only when no other weather runs AND it is the
  only one being started.
- **Admin pause choices:** 1 h / 6 h / 24 h. The admin record key is `autoWeather` = `{offUntil}`.
- **Admin weather join:** a late server joins an admin weather only with at least `AdminLogic.WEATHER_MIN_JOIN` = 60 s
  left.
- **Mutations:** the product of the multipliers. UFO + Meteor = x2.25; a third x1.5 type = x3.375.
- **Tiles:**
  - the countdown text is red when under 1:00;
  - on touch screens the row sits left of the jump button;
  - the Admin Abuse boost column ends above the row;
  - the weather pill leaves that column.
- **Owner rules that apply here:** licensed sounds only (none planned), no neon/emissive, nothing under hub/runway
  removed, HttpService stays off.

## Review Focus
1. **Admin starts UFO, then Meteor a minute later; a server opens after both.** It must run BOTH. The spec's
   one-record-per-command shape would forget UFO, so the record merges (Task 2 `mergeWeatherRecord`). Test in Task 2
   and Task 4.
2. **One of two weathers ends by itself.** The survivor keeps its area, end and tile, and `Weather` drops to just it.
   Test in Task 3.
3. **STOP-all during a lone weather's cutscene (waves frozen).** The waves must unfreeze. Test in Task 3.
4. **A pause runs out by itself.** The hourly weather comes back without RESUME. A pause message with a bad `offUntil`
   (past 24 h + 2 min, negative, a string) is refused. Tests in Task 1 (`autoOn`) and Task 2 (`recheck`).
5. **A player joins or respawns while two weathers run.** They get two tiles at once, no cutscene, and the right tint for
   their area. Test in Task 6 (tiles built from the current attributes at script start), plus the visual check in Task 8.

---

### Task 1: Pure helpers + stacked-mutation unit tests

**Files:**
- Modify: `ReplicatedStorage.WeatherConfig` (append the helpers)
- Modify: `ServerScriptService.WeatherLogic` (append before `return L`)
- Test: `ServerStorage.WeatherTests` (new section "multi-weather")

**Interfaces:**
- Produces:
  - `WeatherConfig.split(s: string?) -> {string}`: known types only, de-duplicated, sorted. nil/"" -> `{}`.
  - `WeatherConfig.join(list: {string}) -> string`: same filtering, sorted, comma-joined.
  - `WeatherConfig.has(s: string?, t: string) -> boolean`.
  - `WeatherConfig.tintFor(arrived: {[string]: number}, areas: {[string]: number}, myArea: number?) -> string?`:
    of the types whose `areas[T] == myArea`, the one with the largest `arrived[T]`. nil when none or `myArea` is nil.
  - `WeatherLogic.cutsceneFor(runningCount: number, startingCount: number) -> boolean`: true only when
    `runningCount == 0 and startingCount == 1`.
  - `WeatherLogic.autoOn(offUntil: any, now: number) -> boolean`: true unless `offUntil` is a number `> now`.

- [ ] **Step 1: Write the failing tests** in WeatherTests (use `fresh(...)` for WeatherConfig, WeatherLogic, Mutations,
  CreatureConfig; Edit caches modules):
```lua
check("split sorts + filters", table.concat(C.split("UFO,Meteor,Bogus,UFO"), ",") == "Meteor,UFO")
check("split empty", #C.split("") == 0 and #C.split(nil) == 0)
check("join", C.join({"UFO", "Meteor"}) == "Meteor,UFO" and C.join({}) == "")
check("has", C.has("Meteor,UFO", "UFO") and not C.has("Meteor", "UFO") and not C.has(nil, "UFO"))
check("tint: last arrived in my area", C.tintFor({UFO = 5, Meteor = 9}, {UFO = 2, Meteor = 2}, 2) == "Meteor")
check("tint: only mine", C.tintFor({UFO = 5, Meteor = 9}, {UFO = 2, Meteor = 3}, 2) == "UFO")
check("tint: none", C.tintFor({UFO = 5}, {UFO = 2}, 4) == nil and C.tintFor({UFO = 5}, {UFO = 2}, nil) == nil)
check("cutscene alone", L.cutsceneFor(0, 1) == true)
check("no cutscene with another running", L.cutsceneFor(1, 1) == false)
check("no cutscene when starting 2", L.cutsceneFor(0, 2) == false)
check("auto on: 0 / nil / past", L.autoOn(0, 100) and L.autoOn(nil, 100) and L.autoOn(99, 100))
check("auto off: future", L.autoOn(101, 100) == false)
check("auto on: junk", L.autoOn("x", 100) == true)
check("UFO+Meteor = x2.25", math.abs(M.mult({"UFO", "Meteor"}) - 2.25) < 1e-9)
check("add twice keeps one", #M.add(M.add({"UFO"}, "Meteor"), "Meteor") == 2)
M.TYPES.Test3 = {mult = 1.5, color = Color3.new(1, 1, 1), hex = "#FFFFFF", tag = "T3"}
check("third type = x3.375", math.abs(M.mult({"UFO", "Meteor", "Test3"}) - 3.375) < 1e-9)
local base = CC.petIncome(<any pet name in CreatureConfig>, 10, nil)
check("petIncome x2.25 for Meteor,UFO", math.abs(CC.petIncome(<same>, 10, M.decode("Meteor,UFO")) - base * 2.25) < 1e-6)
```
  (`CC` must require the fresh `M`. If CreatureConfig requires Mutations by path, redirect it with the existing
  `MutationsFresh` gsub trick; see the earlier ledger.)

- [ ] **Step 2: Run, expect FAIL**
  - Run (Edit): `return require(game.ServerStorage.WeatherTests:Clone())()`
  - Expected: the new checks fail (`split` / `cutsceneFor` / `autoOn` / `tintFor` are nil). The mutation checks may
    already pass: the rule exists, and these tests pin it.
- [ ] **Step 3: Implement** the six functions with the signatures above.
- [ ] **Step 4: Run, expect PASS**
  - Run: same command.
  - Expected: `N passed, 0 failed` (97 + the new ones).
- [ ] **Step 5: Commit:** back up the two modules first, then add the ledger line.

### Task 2: AdminLogic: multi-weather commands, merged record, auto-pause

**Files:**
- Modify: `ServerScriptService.AdminLogic` (`V.weather` at :168, `weatherSync` at :290, `recheck`, the kind allow-list)
- Test: `ServerStorage.AdminTests`

**Interfaces:**
- Consumes: `WeatherConfig.split/join` (Task 1).
- Produces:
  - `V.weather(a)`:
    - `{action="start", weathers="Meteor,UFO"}` from `a.weathers` (comma string), falling back to the old single
      `a.weather`;
    - `{action="stop", weathers=""|"<list>"}`, where `""` = all;
    - errors: `"Pick a weather"` (start with none), `"Unknown weather"` (any unknown name), `"Start or stop the
      weather"`.
  - `V.autoWeather(a)` -> `{action="pause", hours=h}` (h in `AdminLogic.AUTO_HOURS = {1, 6, 24}`) or
    `{action="resume"}`; error `"Pause for 1, 6 or 24 hours"`.
  - `recheck("autoWeather", args)`: accepts `args.offUntil`, a number in `[0, os.time() + 24*3600 + 120]`. Anything else
    is refused.
  - `AdminLogic.mergeWeatherRecord(old: any, id: string, now: number, startEnds: {[string]: number}?,
    stopWhich: ({string} | "all")?) -> rec`. Here `rec = {id, weathers = {[T] = endsAt}, stopped = {T...}|"all"|nil}`.
    - It starts from `old.weathers` entries with `endsAt > now`.
    - A start adds the new types and keeps an existing type's `endsAt` unchanged.
    - A stop removes the listed types (or all) and sets `stopped`.
  - `AdminLogic.weatherSync(rec, now, appliedId) -> {start = {[T] = left}, stop = {T...}|"all"|nil}?`:
    - nil for the same id or a bad record;
    - `start` holds only the types with `left >= WEATHER_MIN_JOIN`;
    - nil when there is nothing to start and nothing to stop.

- [ ] **Step 1: Write the failing tests** (replace the single-weather `weatherSync` / `V.weather` checks):
```lua
local ok, a = L.validate("weather", {action = "start", weathers = "UFO,Meteor"}, OWNER)
check("start two", ok and a.weathers == "Meteor,UFO")
check("start none refused", not (L.validate("weather", {action = "start", weathers = ""}, OWNER)))
check("unknown refused", not (L.validate("weather", {action = "start", weathers = "UFO,Nope"}, OWNER)))
check("old single still ok", select(2, L.validate("weather", {action = "start", weather = "UFO"}, OWNER)).weathers == "UFO")
check("stop all", select(2, L.validate("weather", {action = "stop"}, OWNER)).weathers == "")
check("pause 6h", select(2, L.validate("autoWeather", {action = "pause", hours = 6}, OWNER)).hours == 6)
check("pause 5h refused", not (L.validate("autoWeather", {action = "pause", hours = 5}, OWNER)))
check("recheck offUntil ok", L.recheck("autoWeather", {offUntil = os.time() + 3600}) ~= nil)
check("recheck offUntil too far", L.recheck("autoWeather", {offUntil = os.time() + 25 * 3600}) == nil)
check("recheck offUntil junk", L.recheck("autoWeather", {offUntil = "x"}) == nil and L.recheck("autoWeather", {offUntil = -5}) == nil)
-- merge (Review Focus 1)
local r1 = L.mergeWeatherRecord(nil, "a", 1000, {UFO = 1300})
local r2 = L.mergeWeatherRecord(r1, "b", 1060, {Meteor = 1360, UFO = 1360})
check("merge keeps UFO + its end", r2.weathers.UFO == 1300 and r2.weathers.Meteor == 1360 and r2.id == "b")
local r3 = L.mergeWeatherRecord(r2, "c", 1100, nil, {"UFO"})
check("stop one", r3.weathers.UFO == nil and r3.weathers.Meteor == 1360 and r3.stopped[1] == "UFO")
check("stop all", next(L.mergeWeatherRecord(r2, "d", 1100, nil, "all").weathers) == nil)
check("ended entries dropped", L.mergeWeatherRecord(r1, "e", 1400, {Meteor = 1700}).weathers.UFO == nil)
-- sync
local s = L.weatherSync(r2, 1100, nil)
check("sync starts both", s and math.abs(s.start.UFO - 200) < 1 and math.abs(s.start.Meteor - 260) < 1)
check("sync skips < 60 s left", L.weatherSync(r2, 1250, nil).start.UFO == nil)
check("sync same id = nil", L.weatherSync(r2, 1100, "b") == nil)
check("sync stop", L.weatherSync(r3, 1100, nil).stop[1] == "UFO")
check("sync nothing = nil", L.weatherSync(L.mergeWeatherRecord(nil, "f", 2000, {UFO = 2030}), 2000, nil) == nil)
```
- [ ] **Step 2: Run, expect FAIL**
  - Run (Edit): `return require(game.ServerStorage.AdminTests:Clone())()`
  - Expected: the new checks fail.
- [ ] **Step 3: Implement** `V.weather`, `V.autoWeather`, the `autoWeather` kind in the allow-list and in `recheck`,
  `AUTO_HOURS`, `mergeWeatherRecord`, and the new `weatherSync`.
- [ ] **Step 4: Run, expect PASS**
  - Run: same command.
  - Expected: `N passed, 0 failed`.
- [ ] **Step 5: Commit:** backup + ledger line.

### Task 3: WeatherServer: a set of running weathers

**Files:**
- Modify: `ServerScriptService.WeatherServer` (rewrite the state section, `moveWeather`, `stop`, `start`, `safeStart`,
  the bindables and the scheduler; update the header comment)
- Test: `ServerStorage.WeatherServerTests`:
  - update the single-weather checks at :248-299, :338, :461, :506-510, :669, :687 to the per-type attributes;
  - add a "multi-weather" section.

**Interfaces:**
- Consumes: `WeatherConfig.join`, `WeatherLogic.cutsceneFor`, `WeatherLogic.autoOn` (Task 1).
- Produces:
  - `ServerStorage.WeatherStart:Invoke(t?, area?, seconds?, quiet?) -> ok, type|reason`:
    - refused while `t` already runs (`"That weather is already running"`);
    - `t == nil` (the scheduled pick) is refused while any weather runs.
  - `ServerStorage.WeatherStop:Invoke(t?) -> boolean`: nil = all. True when something stopped.
  - `ServerStorage.WeatherMove:Invoke(area, t?) -> boolean` (Studio only): `t` nil = the only running weather.
  - `ServerStorage.WeatherDueNow:Invoke()` (Studio only, new): sets `due = os.clock()`, so the scheduler is due now.
  - Attributes as in Global Constraints.
    - At boot: `Weather = ""`; for every type in `TYPES`, `WeatherArea_<T> = 0` and `WeatherEnds_<T> = 0`; the old
      single attributes set to nil.
- **Cutscene:** `cutscene = Logic.cutsceneFor(<count running before this start>, quiet and 2 or 1)`. Only then stamp
  `WeatherCutsceneAt_<T>` and call `wavePause:Invoke(true)` (`frozen` per entry).
  - The cfg passed to the module is NOT altered: modules keep their arrival timing.
- **Stop:** each entry's stop releases its own freeze. `safeStart` undoes only that type on error.
- **Scheduler:** it runs only when no weather is running, `Logic.autoOn(workspace:GetAttribute("WeatherAutoOffUntil"),
  os.time())` is true, and `os.clock() >= due`. While paused it simply waits.

- [ ] **Step 1: Write the failing tests** (a multi section; `WeatherTestFast = true` gives 20 s weathers; clear any
  running weather first):
```lua
local cutU, cutM = workspace:GetAttribute("WeatherCutsceneAt_UFO"), workspace:GetAttribute("WeatherCutsceneAt_Meteor")
check("multi: UFO quiet ok", (WStart:Invoke("UFO", 1, nil, true)) == true)
check("multi: Meteor ok", (WStart:Invoke("Meteor", 2)) == true)  -- another runs -> quiet by the rule
check("multi: list", workspace:GetAttribute("Weather") == "Meteor,UFO")
check("multi: own areas", workspace:GetAttribute("WeatherArea_UFO") == 1 and workspace:GetAttribute("WeatherArea_Meteor") == 2)
check("multi: no cutscene stamps", workspace:GetAttribute("WeatherCutsceneAt_UFO") == cutU and workspace:GetAttribute("WeatherCutsceneAt_Meteor") == cutM)
check("multi: waves not frozen", not Config.Paused())
check("multi: same type refused", (WStart:Invoke("UFO")) == false)
check("multi: scheduled pick refused while any runs", (WStart:Invoke(nil)) == false)
check("multi: WeatherMove by type", SS.WeatherMove:Invoke(3, "Meteor") == true and workspace:GetAttribute("WeatherArea_Meteor") == 3 and workspace:GetAttribute("WeatherArea_UFO") == 1)
check("multi: stop one", WStop:Invoke("UFO") == true and workspace:GetAttribute("Weather") == "Meteor" and workspace:GetAttribute("WeatherArea_UFO") == 0 and workspace:GetAttribute("WeatherArea_Meteor") == 3)
check("multi: stop a type not running = false", WStop:Invoke("UFO") == false)
check("multi: stop all", WStop:Invoke() == true and workspace:GetAttribute("Weather") == "")
-- Review Focus 2: one ends by itself, the other keeps going (fast mode: both last 20 s)
WStart:Invoke("Meteor", 2, nil, true)
task.wait(6)
WStart:Invoke("UFO", 1)
check("multi: survivor keeps running", waitFor(function() return workspace:GetAttribute("Weather") == "UFO" end, 24)
  and workspace:GetAttribute("WeatherArea_UFO") == 1 and (workspace:GetAttribute("WeatherEnds_UFO") or 0) > workspace:GetServerTimeNow())
-- lone start: cutscene + freeze; Review Focus 3: stop-all during it unfreezes
WStop:Invoke()
check("lone: cutscene stamped", (WStart:Invoke("UFO", 1)) == true and math.abs((workspace:GetAttribute("WeatherCutsceneAt_UFO") or 0) - workspace:GetServerTimeNow()) < 1)
check("lone: waves frozen", Config.Paused())
check("lone: stop-all unfreezes", WStop:Invoke() == true and not Config.Paused())
-- scheduler: paused, then resumed
workspace:SetAttribute("WeatherAutoOffUntil", os.time() + 3600)
SS.WeatherDueNow:Invoke()
task.wait(3)
check("paused: scheduler starts nothing", workspace:GetAttribute("Weather") == "")
workspace:SetAttribute("WeatherAutoOffUntil", 0)
check("resumed: scheduler starts one", waitFor(function() return workspace:GetAttribute("Weather") ~= "" end, 3))
WStop:Invoke()
-- stacked mutations on a real egg + the money chain (spec section 5)
local egg  -- the first egg in weatherEggs:Invoke(1) with no Mutations attribute
eggBeam:Invoke(egg, "UFO", egg:GetPivot().Position.Y + 20)
check("strike after beam ok", SS.EggStrike:Invoke(egg, "Meteor") == true)
local muts = M.decode(egg:GetAttribute("Mutations"))
check("egg carries both", M.has(muts, "UFO") and M.has(muts, "Meteor") and math.abs(M.mult(muts) - 2.25) < 1e-9)
local before = P:GetAttribute("Money")
Money.Earn(P, 100)
check("Money.Earn x Boosts.money", math.abs((P:GetAttribute("Money") - before) - 100 * Boosts.money(P)) < 1e-6)
```
  The test player is the existing `P`; `M` = `require(RS.Mutations)`, `Money` = `require(SSS.Money)`, `Boosts` =
  `require(RS.Boosts)`. Use the existing `waitFor(fn, seconds) -> boolean` helper, and wait for `Struck` to clear
  before reading the egg (as the meteor section does).
- [ ] **Step 2: Run, expect FAIL**
  - Run: set `workspace.TestFreshSave = true` (Edit), start Play, then on the Server:
    `return require(game.ServerStorage.WeatherServerTests)()`
  - Expected: the multi checks fail (`WeatherArea_UFO` is nil, the second start is refused). The egg + money checks may
    already pass.
- [ ] **Step 3: Implement** WeatherServer as described in Interfaces.
  - Each entry: `{type, cfg, module, area, token, frozen}` in `running[T]`.
  - The area loop per entry is today's loop, keyed by its own token.
  - `Weather` is rewritten with `WeatherConfig.join` on every start and stop.
- [ ] **Step 4: Run, expect PASS**
  - Run: stop Play, start Play (clean session), same command.
  - Expected: `N passed, 0 failed`.
- [ ] **Step 5: Commit:** backup + ledger line.

### Task 4: AdminServer: multi START/STOP, merged record, auto-pause everywhere

**Files:**
- Modify: `ServerScriptService.AdminServer`:
  - `ARG_KEYS` (:507): add `"weathers"`, `"hours"`;
  - `runWeather` / `applyGlobal.weather` / `syncWeather` (:227-272);
  - `run.weather` (:479);
  - new `applyGlobal.autoWeather` / `run.autoWeather`;
  - the startup and 60 s sync (:611-631).
- Test: `ServerStorage.AdminServerTests` (replace the weather checks at :124-150).

**Interfaces:**
- Consumes:
  - `AdminLogic.mergeWeatherRecord`, `weatherSync`, `V.weather`, `V.autoWeather` (Task 2);
  - `WeatherStart` / `WeatherStop` (Task 3).
- Produces:
  - `run.weather(admin, a)`:
    - start: `ends = {[T] = os.time() + duration}` for each selected type; an already-running one keeps its stored end;
    - `eventMap:UpdateAsync("weather", mergeWeatherRecord(...), WEATHER_KEEP)`;
    - broadcast `"weather"` with `{action, weathers, ends = rec.weathers}` for a start, or `{action="stop", weathers}`
      for a stop.
  - `applyGlobal.weather(msg)`:
    - start: each type not running here starts with `seconds = ends[T] - os.time()` (skipped if `< WEATHER_MIN_JOIN`)
      and `quiet = (#toStart > 1)`;
    - an `ends[T]` that is missing or not a number falls back to `os.time() + duration` (today's rule, per type);
    - stop: `WeatherStop:Invoke(T)` per listed type, or `WeatherStop:Invoke()` for `""` (all, scheduled ones too:
      the owner pressed it).
  - `adminWeathers: {[string]: true}`: the admin types running here. A late `stop` from `syncWeather` only ends these.
  - `run.autoWeather(admin, a)`:
    - pause: `SetAsync("autoWeather", {offUntil = os.time() + hours*3600}, hours*3600 + 120)`;
    - resume: `RemoveAsync("autoWeather")`;
    - then broadcast `"autoWeather"` with `{offUntil}` (0 = resume). Reply text: `"Auto weather PAUSED for 6 h in
      every server"` / `"Auto weather back ON in every server"`.
  - `applyGlobal.autoWeather(msg)`: `recheck`, then `workspace:SetAttribute("WeatherAutoOffUntil", offUntil)`.
  - `syncWeather(forget)` also reads `"autoWeather"`:
    - found: set the attribute to its `offUntil`;
    - missing: set 0;
    - read error: leave the attribute as it is (a new server starts at 0 = ON).

- [ ] **Step 1: Write the failing tests** (the existing `dbg` / `sync` helpers; `run` through the existing admin-call
  path):
```lua
local r = call("weather", {action = "start", weathers = "UFO,Meteor"})
check("start two everywhere", r.ok and workspace:GetAttribute("Weather") == "Meteor,UFO")
check("started quiet (2 at once)", not Config.Paused())
local rec = select(2, pcall(eventMap.GetAsync, eventMap, "weather"))
check("record holds both", rec.weathers.UFO and rec.weathers.Meteor)
r = call("weather", {action = "start", weathers = "UFO"})
check("start a running one = left alone", r.ok and math.abs(workspace:GetAttribute("WeatherEnds_UFO") - <ends before>) < 1)
r = call("weather", {action = "stop", weathers = "UFO"})
check("stop selected", r.ok and workspace:GetAttribute("Weather") == "Meteor")
-- Review Focus 1: late server with two admin weathers
WStop:Invoke(); call("weather", {action = "start", weathers = "UFO"}); call("weather", {action = "start", weathers = "Meteor"})
WStop:Invoke()  -- pretend this server never ran them
check("late join runs both", sync:Invoke(true) == true and workspace:GetAttribute("Weather") == "Meteor,UFO")
r = call("weather", {action = "stop"})
check("stop all", r.ok and workspace:GetAttribute("Weather") == "")
WStart:Invoke("UFO")  -- not an admin weather
check("late stop leaves a non-admin weather", sync:Invoke(true) == false and workspace:GetAttribute("Weather") == "UFO")
WStop:Invoke()
r = call("autoWeather", {action = "pause", hours = 1})
check("pause applied", r.ok and math.abs(workspace:GetAttribute("WeatherAutoOffUntil") - (os.time() + 3600)) <= 2)
check("pause stored", select(2, pcall(eventMap.GetAsync, eventMap, "autoWeather")).offUntil ~= nil)
workspace:SetAttribute("WeatherAutoOffUntil", 0); sync:Invoke(true)
check("late server picks up the pause", (workspace:GetAttribute("WeatherAutoOffUntil") or 0) > os.time())
r = call("autoWeather", {action = "resume"})
check("resume", r.ok and workspace:GetAttribute("WeatherAutoOffUntil") == 0)
```
  `eventMap` = `MemoryStoreService:GetHashMap("AdminEvent")`; in Studio, use the same name the server uses (with its
  Studio suffix, if it has one). `call` / `sync` = the suite's existing helpers.
- [ ] **Step 2: Run, expect FAIL**
  - Run (Play, TestFreshSave = true, Server): `return require(game.ServerStorage.AdminServerTests)()`
  - Expected: the new checks fail.
- [ ] **Step 3: Implement** as in Interfaces.
- [ ] **Step 4: Run, expect PASS.** Run AdminServerTests, then WeatherServerTests again in a clean Play session.
  - Expected: both `0 failed`.
- [ ] **Step 5: Commit:** backup + ledger line.

### Task 5: Clients: several weather modules, per-type cutscenes, the tint

**Files:**
- Modify: `StarterPlayer.StarterPlayerScripts.WeatherClient` (rewrite `refresh`, `onCutscene`, `refreshTint`, the
  connections at :78-81, and the header)
- Modify: `ReplicatedStorage.Weathers.UFOClient:632`: `WeatherConfig.has(workspace:GetAttribute("Weather"), "UFO")`
- Modify: `ReplicatedStorage.Weathers.MeteorClient:1047`: the same with `"Meteor"`
- Test: a client check run from the Client datamodel during Play (below)

**Interfaces:**
- Consumes: `WeatherConfig.split`, `has`, `tintFor` (Task 1); the per-type attributes (Task 3).
- Produces: `running: {[string]: module}`.
  - **`refresh()`:** stops the modules that left the list and starts the new ones (pcall each). It mirrors the running
    set as the local player attribute `WeatherClientRunning` (comma list, client-only), so tests can see it.
  - **`onCutscene(T)`:** on `WeatherCutsceneAt_<T>` changes, with today's skip rules, calls
    `module.cutscene(WeatherArea_<T>, at)`.
  - **Tint:** `arrived[T] = os.clock()` on every `WeatherArea_<T>` change. `refreshTint()` uses `WeatherConfig.tintFor`
    with the player's `CurrentArea`.

- [ ] **Step 1: Write the failing check** (Client datamodel, Play, with UFO + Meteor running quietly; start them from
  the Server with `WStart:Invoke("UFO", 1, nil, true)` and `WStart:Invoke("Meteor", 2)`):
```lua
return tostring(game.Players.LocalPlayer:GetAttribute("WeatherClientRunning"))
```
  Expected now: `nil`. The old `refresh` looks up a module for the name "Meteor,UFO", which is no type at all, so
  neither client module runs.
- [ ] **Step 2: Implement** the three changes.
- [ ] **Step 3: Re-run the check.** Expected: `Meteor,UFO`; the screenshot shows the saucers and the storm cloud, and no
  cutscene played. Then stop UFO and start it alone: the check reads `Meteor,UFO` again, the UFO cutscene plays
  (screenshot), and Meteor's visuals stay.
- [ ] **Step 4: Regression.** Re-run WeatherTests (Edit) and WeatherServerTests (Play). Both `0 failed`.
- [ ] **Step 5: Commit:** backup + ledger line.

### Task 6: Weather tiles (bottom right) + the boost column moves up

**Files:**
- Create: `StarterPlayer.StarterPlayerScripts.WeatherTilesClient` (LocalScript)
- Modify: `StarterPlayer.StarterPlayerScripts.AdminBannerClient`:
  - remove the weather pill (:493-503 and the `b.weather` branch of `fillTip` :327-332, plus its `byKey` entry);
  - `placeBoosts(n)` (:442-472) ends the column above the tile row.

**Interfaces:**
- Consumes: `Weather`, `WeatherEnds_<T>`, `WeatherConfig.TYPES[T].icon/hex/title/tip`, `WeatherConfig.split`.
- Produces: `PlayerGui.WeatherTiles`:
  - a ScreenGui, `ResetOnSpawn = false`;
  - attribute `RowTop` (number, px) = the row's top `AbsolutePosition.Y` while at least one tile shows, else 0.
  - `AdminBannerClient` listens to that attribute's change and re-runs `placeBoosts`.

- [ ] **Step 0:** invoke the `check-ui-clean-roblox` skill and build to it.
- [ ] **Step 1: Write the failing check** (Client, Play, two weathers running):
```lua
local g = game.Players.LocalPlayer.PlayerGui:FindFirstChild("WeatherTiles")
local n = 0
if g then for _, t in g:GetDescendants() do if t:GetAttribute("WeatherTile") then n += 1 end end end
return ("tiles=%d rowTop=%s"):format(n, tostring(g and g:GetAttribute("RowTop")))
```
  Expected now: `tiles=0 rowTop=nil`, and the screenshot shows the old weather pill in the boost column.
- [ ] **Step 2: Implement the tiles.**
  - **Placement:**
    - square tiles (side = viewport height x 0.085) in a horizontal row, AnchorPoint (1, 1), in the bottom-right
      corner;
    - on touch: the row's right edge = the jump button's left edge minus one gap (`TouchGui.TouchControlFrame.JumpButton`).
  - **Each tile** (attribute `WeatherTile = T`):
    - Check-UI canvas, with an accent bar in `hex`;
    - the icon, `ScaleType.Fit`;
    - a smooth countdown ring in `hex` around the icon. Use the two-half clip technique: two `ClipsDescendants`
      halves, each holding a UICorner circle with a `UIGradient` hard edge rotated by the progress, and an inner disc
      in `#1A2C34`;
    - the time "m:ss" in GothamBlack + stroke, red (`#FF3B3B`) under 60 s.
  - **Motion:** a new tile slides in from the right (TweenService Back.Out); a leaving tile shrinks out.
  - **Tip:** hover (MouseEnter / MouseLeave) or tap (Activated) shows a tip above the tile, styled like the banner tip:
    the title in `hex` + `TYPES[T].tip`.
  - **Startup:** build from the current `Weather` at script start (Review Focus 5), and update the countdown every
    0.25 s.
- [ ] **Step 3: Remove the weather pill** from AdminBannerClient, and clamp the boost column's bottom to `RowTop - gap`
  when `RowTop > 0`.
- [ ] **Step 4: Re-run the check.** Expected: `tiles=2 rowTop=<px greater than 0>`, and the pill is gone.
  - Screenshots on PC and in the phone emulator (Device: iPhone).
  - Two tiles, no overlap with the jump button or the boost column.
  - Under 1:00 the time turns red (use `WeatherTestFast` to get there).
- [ ] **Step 5: Respawn check.** Reset the character: still two tiles (no duplicates). Then commit (backup + ledger
  line).

### Task 7: Admin panel: multi-select WEATHER row + AUTO WEATHER row

**Files:**
- Modify: `ServerStorage.AdminUI.AdminClient`:
  - `chips(...)` gets a multi-select mode;
  - the WEATHER row at `yFun+152`;
  - a new AUTO WEATHER row under it, growing the panel/canvas height to fit.

**Interfaces:**
- Consumes: `send(kind, args, onDone)`; the kinds `weather` / `autoWeather` and their args (Task 2); the attribute
  `WeatherAutoOffUntil`.
- Produces: `chips(parent, name, options, default, size, pos, multi?)`.
  - With `multi = true`, the getter returns a `{string}` of the selected options and the setter takes a list.
  - Single-select is unchanged for every existing caller.

- [ ] **Step 0:** invoke the `check-ui-clean-roblox` skill.
- [ ] **Step 1: Implement:**
  - **WEATHER row:**
    - the chips toggle (CYAN on / SILVER off);
    - START sends `{action="start", weathers=WeatherConfig.join(selected)}`. With none selected it shows
      "Pick a weather" locally and sends nothing;
    - STOP sends `{action="stop", weathers=WeatherConfig.join(selected)}` (`""` = all). The button reads "STOP ALL" while
      nothing is selected.
  - **AUTO WEATHER row:**
    - single-select chips `[1h] [6h] [24h]` (default 1h), PAUSE (crimson) and RESUME (lime);
    - a status label refreshed every second: "AUTO WEATHER: ON" (lime) or "PAUSED h:mm:ss" (amber), counted from
      `WeatherAutoOffUntil - workspace:GetServerTimeNow()`.
- [ ] **Step 2: Live check** in Play as the owner (TestFreshSave = true):
  - select UFO + Meteor, START: two tiles, no cutscene, and the reply says "in every server";
  - STOP with UFO selected: one tile;
  - STOP ALL: none;
  - PAUSE 1h: the status counts down from 0:59:59 and `WeatherAutoOffUntil` is set;
  - RESUME: ON.
  - Screenshot the panel.
- [ ] **Step 3: Regression.** Run AdminTests (Edit) and AdminServerTests (Play): `0 failed`.
- [ ] **Step 4: Commit:** backup + ledger line.

### Task 8: Full regression, visual sign-off, docs + memory

**Files:**
- Modify: `docs/weather-live-checklist.md`, `docs/admin-live-checklist.md`
- Modify: memory `roblox-weather-system.md`, `roblox-admin-menu.md`, and `MEMORY.md` hooks
- Modify: this plan (the ledger)

- [ ] **Step 1: Run all four suites.**
  - WeatherTests and AdminTests in Edit.
  - WeatherServerTests and AdminServerTests in a clean Play session, TestFreshSave = true.
  - Expected: all `0 failed`. Record the counts.
- [ ] **Step 2: Visual checks** (screenshots into `Weather/multi/`):
  - two weathers at once: no cutscene, both visible, tiles;
  - one alone: its cutscene;
  - phone emulator: the tile row and the boost column;
  - a 2-player Server & Clients run: the second client joins mid-weather and gets two tiles, no cutscene (Review
    Focus 5).
- [ ] **Step 3:** set `workspace.TestFreshSave = false` and stop Play.
- [ ] **Step 4: Docs and memory.**
  - The checklists get the new attributes, the AUTO WEATHER row and the "STOP = all when none selected" rule.
  - Memory: the per-type attributes, the merged record, the `RowTop` hand-off and the pause key.
- [ ] **Step 5: Report to the owner:** the suite counts, the screenshots, every Ruling, and the reminder: **Save +
  Publish + Migrate to Latest Update**.

## Ledger
(one line per task: `Task N: complete (...)`, plus `Ruling:` lines)
- Executor: Native (owner's choice, 2026-10-12), executing-plans skill.
- Ruling (setup): no git worktree / task-start / task-done scripts. The code lives in the Studio place, not in git. The
  record is this ledger, the "Commit" step = a backup in `ServerStorage._Backup_WeatherMulti.Before` + a ledger line, and
  each task's test run is the Studio suite named in its brief. *Cost if wrong:* none (the plan's Global Constraints say
  so).
- Pre-flight (shared interfaces):
  - T1 -> T2/T3/T5/T6/T7: `WeatherConfig.split/join/has/tintFor`, `WeatherLogic.cutsceneFor/autoOn`. Consistent.
  - T2 -> T4: `mergeWeatherRecord(old, id, now, startEnds?, stopWhich?)` and the `weatherSync -> {start, stop}?` table;
    `V.weather` stop `weathers = ""` means all, which T4 maps to `stopWhich = "all"`. Consistent.
  - T3 -> T4/T5: `WeatherStart(t?, area?, seconds?, quiet?)`, `WeatherStop(t?)`, the per-type attributes. Consistent.
  - T6 -> AdminBannerClient: the `RowTop` attribute. Consistent.
  - T2/T4 -> T7: the kinds `weather` (`weathers` comma string) / `autoWeather` (`action`, `hours`). Consistent.
- Ruling (plan): the admin weather record merges (`mergeWeatherRecord`) instead of being replaced per command.
  - Why: with replace, a server that opens after "START UFO" then "START Meteor" would run only Meteor.
  - Cost if wrong: one function; the stored shape gains a `stopped` field next to `weathers`.
- Ruling (plan): the selection travels as a comma string (`weathers = "Meteor,UFO"`).
  - Why: AdminServer's `ARG_KEYS` copies only scalar args, and lists are dropped by design (security).
- Ruling (plan): a quiet start doesn't change the module's cfg. The UFO mothership still descends in the world, and the
  first act still waits `cutscene + waveHold` (10 s). Only the camera cutscene and the wave freeze are skipped.
  - Cost if wrong: an admin might expect the first beam sooner. That's a `cfg` tweak in WeatherServer.
- Ruling (plan): when the auto-pause can't be read, the server keeps its current value (0 = ON on a new server) instead
  of flipping to ON. This avoids flapping between paused and on during a MemoryStore hiccup.
- Task 1: complete (WeatherConfig.split/join/has/tintFor + WeatherLogic.cutsceneFor/autoOn; RED 13 failed -> GREEN; tests: WeatherTests (Edit) -> 116 passed, 0 failed)
- Task 2: complete (AdminLogic V.weather multi + V.autoWeather + AUTO_HOURS + recheck autoWeather + mergeWeatherRecord + weatherSync table; RED 11 failed -> GREEN; tests: AdminTests (Edit) -> 130 passed, 0 failed)
- Task 2: Ruling: the AdminTests loader now gives AdminLogic a FRESH WeatherConfig clone (gsub on its require). Edit caches modules, and the cached WeatherConfig had no `join`. *Cost if wrong:* none (test-only).
- Task 2: Ruling: an old-shape record (`{id, type, endsAt}` / `{stopped = true}`) is ignored by `weatherSync`. It lives at most ~7 min, and Migrate to Latest Update restarts every server anyway. *Cost if wrong:* a server opening in those minutes misses one admin weather.
- Task 3: complete (WeatherServer: `running[T]` entries, per-type attributes, cutscene rule, `WeatherStop(t?)`, `WeatherMove(area, t?)`, Studio `WeatherDueNow`, scheduler waits while any runs or paused; RED 19 failed -> GREEN; tests: WeatherServerTests (Play, TestFreshSave) -> 163 passed, 0 failed; console: only the two errors the tests cause on purpose)
- Task 3: Ruling: the "resumed" scheduler check accepts "a weather started OR WeatherNextAt moved +30 s". Both types already ran in the test, so NO_REPEAT forbids a real start; what the check proves is that the scheduler acts again once resumed. *Cost if wrong:* none.
- Task 3: Ruling: the pay check uses `math.floor(base x 2.25 x Boosts.money)`, because `Money.Earn` floors. *Cost if wrong:* none.
- Task 3: Ruling: per-entry identity (`running[t] == w`) replaces the old global `token`, and `safeStart` undoes only the types this start added (it works for the scheduled pick too, whose type isn't known up front). *Cost if wrong:* none (covered by the errored-start tests).
- Task 4: complete (AdminServer: ARG_KEYS + weathers/hours, startWeathers/stopWeathers/adminWeathers, applyGlobal.weather/autoWeather, merged record via UpdateAsync, run.weather multi, run.autoWeather, syncWeather reads autoWeather; RED 13 failed -> GREEN; tests: AdminServerTests (Play) -> 55 passed, 0 failed; WeatherServerTests (clean Play) -> 163 passed, 0 failed)
- Task 4: Ruling: the START message carries `ends` only for the selected types, not every entry in the record. Other admin weathers still in the record reach a server that lacks them through the 60 s `syncWeather`. *Cost if wrong:* up to a minute's delay healing a server that missed an earlier START.
- Task 5: complete (WeatherClient: a `running[T]` module set + `WeatherClientRunning`, per-type cutscene signals, tint by `WeatherConfig.tintFor`; UFOClient/MeteorClient cutscene loops use `WeatherConfig.has`. RED: running=nil with "Meteor,UFO" -> GREEN: running=Meteor,UFO, no cutscene, storm tint in area 1 (screenshot); a lone UFO: cutscene ran (`InWeatherCutscene` + UFOCutscene gui, Scriptable camera at ~4.5 s); Meteor added during it: no cutscene. Regression: WeatherTests 116/116, WeatherServerTests (clean Play) 163/163)
- Task 5: Ruling: plan Step 3 said "stop UFO and start it alone" while Meteor runs. That contradicts the cutscene rule (it wouldn't be alone). Checked instead: stop all -> UFO alone plays its cutscene -> Meteor added while UFO runs plays none. *Cost if wrong:* none.
- Task 5: Ruling: the MCP `screen_capture` / `execute_luau` reset the Play camera, so a mid-cutscene screenshot shows the normal view. The cutscene is proven by its own flags (`InWeatherCutscene`, the UFOCutscene gui, the Scriptable camera at ~4.5 s), not by a screenshot. *Cost if wrong:* none (the cutscene code itself only changed its loop condition).
- Task 5: Ruling: two pre-existing test flakes were fixed, test code only. (1) The Studio-only `MeteorDebug "egg"` hook (inside `Weathers.Meteor`) now strikes the plain egg with the most time left: it had picked one 0.3 s from expiring. The Global Constraint says the modules don't change, but this is Studio-only test tooling, and gameplay code is untouched. (2) The WST pause check stores `autoWeather` in MemoryStore like AdminServer does, because AdminServer's 60 s re-read reset the bare attribute. *Cost if wrong:* none for players.
- Task 6: complete (new `StarterPlayerScripts.WeatherTilesClient` + AdminBannerClient: weather pill removed, boost column ends above `RowTop`. RED tiles=0 rowTop=nil -> GREEN on PC: tiles=2, rowTop=908, boost column bottom 837 (no overlap), hover tip "UFO INVASION / UFOs grab players and mutate eggs (x1.5)", Meteor at 0:14 in red, an ending tile leaves (holders=UFO), respawn: 1 gui + 2 tiles. iPhone 17 Pro emulator: row 5 px left of the jump button, bottoms aligned, the tap tip shows. Screenshots checked: tiles_pc, tiles_zoom_inspect, tiles_tip, tiles_red, phone zooms)
- Task 6: Ruling: tile look = a gradient in the weather's colour + checkerboard + pastel ring on a dark track, like the HUD's Eggs/Pets/Potions tiles, instead of the plan's solid slate canvas. The slate looked dull beside the bright HUD, and the owner asked for "cooler". *Cost if wrong:* a few colours in `makeTile`.
- Task 6: Ruling: the minimum tile size is 40 px everywhere (plan: 46 on touch). At 46 the tiles were 1.5x the phone HUD tiles; 40 is still tappable. *Cost if wrong:* one number.
- Task 6: Ruling: the ring's full length = the weather's configured duration, so a weather a server joined late (an admin weather with less time) shows a partly empty ring. That is accurate. *Cost if wrong:* one line in `tick()`.
- Task 6: Ruling: on touch-only screens, MouseEnter/MouseLeave are ignored. A phone fires MouseEnter on the tap right before Activated, so the tip showed and the tap hid it at once. The same pre-existing bug was in the Admin Abuse boost pills (confirmed on the phone emulator: a tap showed nothing), and it got the same 2-line guard there, verified (the "x2 MONEY / Everyone earns x2 money" tip shows on tap). *Cost if wrong:* none.
- Task 7: complete (AdminClient: `chips(..., multi)`; WEATHER row = multi-select chips + START (none picked -> "Pick a weather first", nothing sent) + STOP / "STOP ALL"; new HOURLY WEATHER row = 1H/6H/24H + PAUSE + RESUME + live state "AUTO WEATHER: ON" / "PAUSED h:mm:ss". Live in Play with real clicks: both picked + START -> "Started METEOR SHOWER + UFO INVASION for 5 min in every server", 2 tiles, no cutscene stamps; UFO picked + STOP -> Weather=Meteor; none + STOP ALL -> "Stopped all weathers in every server"; PAUSE 1H -> "PAUSED 0:59:46" (offUntil = now + 3592 s); RESUME -> ON (0). Regression: AdminTests (Edit) 130/130, AdminServerTests (Play) 55/55)
- Task 7: Ruling: the hourly row's heading is "HOURLY WEATHER IN ALL SERVERS", with the state on the right ("AUTO WEATHER: ON" / "PAUSED 5:41:12"), so the words "AUTO WEATHER" don't appear twice. The button columns are aligned with the WEATHER row above. *Cost if wrong:* label text.
- Task 8: complete (all four suites in clean sessions: WeatherTests 116/116, AdminTests 130/130, WeatherServerTests 163/163, AdminServerTests 55/55. Visual: two at once with no cutscene + tiles (Tasks 5-7), a lone one plays its cutscene (Task 5), phone emulator tile row + boost column (Task 6). Late join, via a temporary server Script that started both weathers with 0 players in (deleted afterwards): the joiner got running=Meteor,UFO, 2 tiles, no cutscene, and the storm tint in the Meteor's area. TestFreshSave set back to false. Docs: weather-live-checklist 2c + section 3, admin-live-checklist item 8. Memory: roblox-weather-system, roblox-admin-menu, MEMORY.md hooks)
- Task 8: Ruling: the plan's "2-player Server & Clients" late-join check was done with a temporary boot-time server Script instead. The MCP play tool has no multi-client mode, and the Script gives a real join after both weathers started. *Cost if wrong:* the two-server live check in the owner's checklist still covers it.
- Task 8: found and fixed (a RED -> GREEN check in Play) a late-join tile bug. A client that builds its tiles while its viewport is still sizing up kept 40 px tiles (expected 92 at 1080p): `layout()` resized the slot but not the tile, and the slide-in tween then reset the slot to the old size. Now a resize also sizes the tile and cancels the slot's slide-in tween. Check: holder=92, tile=92 for the late joiner.
- Final review: a fresh reviewer (opus, read-only on Studio) found 0 Critical, 3 Important and 9 Minor. Verdict "with fixes".
- Final: fixed "UFO and Meteor can grab the same player at once". `eligible` in Weathers.UFO now refuses a player with `MeteorDownAt`, and Weathers.Meteor one with `UfoCaught`. Tests: "never caught: knocked down by a meteor" + "meteor: never targeted while a UFO holds them", RED -> GREEN; WeatherServerTests 165/165.
- Final: Ruling: the server weather modules DID change (one line each), against the plan's "modules do not change". The spec allows two weathers in one area, and a player must not be fought over by both. *Cost if wrong:* none.
- Final: fixed "a server that missed a START never catches up" (this also made the Task 4 ruling true). `AdminLogic.weatherSync(rec, now, appliedId, ranHere)` now starts every record weather this server hasn't run (`ranHere[T] ~= endsAt`), whatever command id it applied last; stops still go by id. AdminServer keeps `ranHere` (type -> exact endsAt). Tests: AdminTests "a missed START is joined after a later command was applied" + "a weather this server already ran is never started again", and AdminServerTests "a missed START is joined by the normal sync" (real path, forget = false), RED -> GREEN; AdminTests 133/133, AdminServerTests 59/59.
- Final: fixed "a failed MemoryStore write for PAUSE/RESUME is still broadcast, then undone by the minute sync". `run.autoWeather` now refuses ("Couldn't save it - nothing changed, try again") and sends nothing. A STOP whose write fails is no longer undone by the sync either (`ranHere`). New Studio-only switch `workspace.AdminTestStoreFail`. Tests: "a pause that can't be stored is refused" RED -> GREEN, plus "STOP with a failed store write ... the sync doesn't bring them back" (it passed vacuously before the switch existed; now it tests the real path).
- Final: Ruling: the HUD design changed at the OWNER's request mid-review ("the picture + timer would be cool like picture i've sent": a reference row of buff icons with timers under them). Each weather is now its icon (Fit) with its timer under it (red under 1:00): no tile frame, no countdown ring. Placement, tips, slide in/out, RowTop and the late-join resize fix are kept. Icon size = viewport height x 0.06, clamped 34..76 px (65 at 1080p). The tile version is kept disabled in `SS._Backup_WeatherMulti.Before.WeatherTilesClient_v1Tiles`. This supersedes the spec's ring and the Task 6 tile-look rulings. Checked: PC screenshot (65 px icons, "4:47 / 4:48"), iPhone emulator (left of the jump button), suites green.
- Final: Ruling (declined-to-judge items): PAUSE leaves an already-running scheduled weather on (spec: the scheduler just waits; STOP exists). An admin START leaves a same-type scheduled weather with its own end ("left alone"). A server that opens during a lone admin weather plays its cutscene for its players (cutscene rule: it is alone there). Old-shape records are ignored (Task 2). The ring note is moot now that the ring is gone. MeteorDebug is test-only. Touch + boost + weather row: checked on the phone emulator, no overlap. Clock skew and the MemoryStore budget are negligible. All stand.
- Final: minor (deferred): `adminWeathers[T]` isn't cleared when an admin weather ends by itself, so a late stop could end a later scheduled weather of the same type (the old code had the same flaw).
- Final: minor (deferred): there is no revision ordering between weather commands. Out-of-order messages or a stale sync read can bring a stopped weather back for up to 60 s (it heals at the next sync; the old code had the same race).
- Final: minor (deferred): for a late joiner with two weathers in their area, the tint pick is arbitrary (no arrival time known).
- Final: minor (deferred): the admin STOP / STOP ALL label lags the chip selection by up to 0.5 s.
- Final: minor (deferred): when a pause ends (or on RESUME), every overdue server starts its hourly weather within about 1 s (judged acceptable).
- Final: minor (deferred): the HUD sizes come from the viewport in pixels, not the Check-UI UIScale 1050x620 baseline.
- Final: minor (deferred): during Migrate to Latest Update, old and new servers misread each other's weather messages (temporary).
- Final: minor (deferred): the boot sync can skip the record if WeatherStart isn't ready within 30 s (the old code had the same flaw).
- Final: minor (deferred): stale text: the AdminServer header still describes "replaces whatever runs / {id, type, endsAt}", and WeatherConfig `short` / "HUD pill" comments are unused.
- Finish: no git branch and no workspace to delete (Studio place). The owner saves, publishes and migrates.

## Follow-up 2026-10-12: the deferred minors (owner: "fix the small issues u left for later") + Admin Abuse restyle
Backups: `SS._Backup_WeatherMulti.BeforeMinors` (every script touched below).
- Minor 1 fixed: AdminServer drops a type from `adminWeathers` when it leaves `Weather`, so a late stop never ends a later scheduled weather of the same type. Test (AST) "minors: a late stop leaves a later scheduled weather of the same type", RED -> GREEN.
- Minor 2 fixed: the weather record carries `rev` (`AdminLogic.nextRev`). AdminServer keeps `weatherRev` and ignores older messages or records (`weatherSync(..., lastRev)`). Tests: AdminTests "rising revision", "sync ignores a record older..."; AST "an older weather command is ignored". All RED -> GREEN.
- Minor 3 fixed: WeatherServer stamps `WeatherArrivedAt_<T>` (start + every move, cleared at stop), and WeatherClient's tint uses it, so it's right for late joiners too. Tests: WST "arrival stamped per weather", "a move stamps a new arrival", RED -> GREEN; "stop clears the arrival" was vacuous before.
- Minor 4 fixed: the AdminClient chips call `onChange`, so STOP / STOP ALL changes the moment a chip is picked; the 0.5 s loop no longer touches it. Verified in Play: before = "STOP ALL", after picking = "STOP". Ruling: no automated test, because UI timing is not reliably testable through the MCP. *Cost if wrong:* none.
- Minor 5 fixed: when a pause ends and the hour already passed, the next hourly weather comes after GAP (10-20 min), not in every server at once. Test (WST) "after a pause the next one is 10-20 min away", RED (29.9 s) -> GREEN.
- Minor 6 fixed: the weather row (and the new boost row) size at the Check-UI baseline (S 55 / TH 19 / GAP 9) with a UIScale clamped 0.52-1.18: 65 px at 1080p, 34 px on a phone.
- Minor 7 fixed: `AdminLogic.weatherMessage`: a single START also carries the old `weather` + `endsAt`; a STOP of picked ones travels as `stopSome` (old servers ignore it; new ones read it as a stop of those). `AdminLogic.messageEnds` honours an old server's `endsAt`. Tests: AdminTests (5 checks) + AST "an old server's START keeps its end" (RED: 297 s -> GREEN 147 s).
- Minor 8 fixed: `startWeathers` / `stopWeathers` mark a command applied only after the bindable exists, and the sync no longer runs an empty start step (that step had marked the record applied, so the next sync skipped a stop that couldn't run). Test (AST) "a stop that couldn't run is applied at the next sync", RED -> GREEN (the first GREEN attempt failed and exposed that empty start step).
- Minor 9 fixed: the AdminServer header describes the multi record; the WeatherConfig `short` fields and "HUD pill" comments were removed; the WeatherTests config check no longer reads `short`.
- Owner request mid-work ("Even the admin abuse icons/style to be like the events style please"): the Admin Abuse boosts are now icon + timer (red under 1:00) with an "x2"/"x3" badge, in a row right above the weather icons under a small "ADMIN ABUSE" label. Same Check-UI sizes; they pop in; hover/tap tip above. WeatherTilesClient publishes `RowRight` / `RowBottom` so the rows line up (PC corner; phone left of the jump button). Verified: PC screenshot (Money x2, Speed x3, Lucky Eggs + Meteor + UFO), hover tip "x2 MONEY / Everyone earns x2 money", iPhone 17 Pro emulator. Ruling: the "ADMIN ABUSE" label stays (the owner's 2026-10-10 identity for the boosts). *Cost if wrong:* delete one label.
- Suites: WeatherTests 116/116, AdminTests 147/147 (Edit, final); WeatherServerTests 169/169, AdminServerTests 63/63 (Play). TestFreshSave false; test boosts stopped; emulator back on HD 1080.

## Follow-up 2026-10-12: one icon row (owner: "Remove the admin abuse text, make all icons ... next to each other, in order i start them")
Backup: `SS._Backup_WeatherMulti.BeforeOneRow` (WeatherTilesClient + AdminBannerClient).
- The "ADMIN ABUSE" label and the separate boost row (`AdminBanner.EventBoosts`) are gone. AdminBannerClient parents the boost holders into `PlayerGui.WeatherTiles.Row`.
- Both scripts take LayoutOrder from `nextOrder()` (the row's `NextOrder` attribute), so the newest icon is at the right end. Boosts now grow in and shrink out like the weathers (attribute `Leaving`), and `layout()` counts every visible, non-leaving icon.
- The RowTop / RowRight / RowBottom attributes were removed; nothing else read them. The boost tip converts Y between the two ScreenGuis.
- RED (before): with a weather and 2 boosts running, the row held only "UFO", and the "ADMIN ABUSE" label was showing.
- GREEN (Play):
  - Money, LuckyRain (running at load), then UFO, Speed and Meteor started in that order -> row `Money#1 LuckyRain#2 UFO#3 Speed#4 Meteor#5`, left to right, 75 px apart.
  - Stopping UFO + Money and starting them again -> `LuckyRain Speed Meteor Money UFO`.
  - Hover tips on PC: boost and weather tips, each above its own icon.
  - iPhone 17 Pro: one row left of the jump button; a tap shows "x2 MONEY / Everyone earns x2 money".
  - Stop all -> the row is empty. No errors from either script.
- Ruling: order = when this client saw it start; no server start stamp was added. On a late join, things already running show in load order. *Cost if wrong:* add a start stamp to the boost state and the weather attributes.
- TestFreshSave false; test boosts + weathers stopped; emulator back on HD 1080.
