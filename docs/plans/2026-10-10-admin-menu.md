# SLINGSHOT Admin Menu Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** An owner-only in-game admin menu (announce to all servers, Admin Abuse events, player tools, server tools).

**Architecture:** Pure rules live in one testable module (`AdminLogic`). `AdminServer` is the only place commands
run: it checks the owner, validates, rate-limits, logs, applies the command on its own server at once and publishes it
on MessagingService (other servers apply it, duplicates dropped by id). Running events live in MemoryStore and become
workspace attributes that the existing Boosts / BaseHatchery / EggSpawner code reads.

**Tech Stack:** Roblox Studio via the Studio MCP (execute_luau, multi_edit, play), Luau, MessagingService,
MemoryStoreService, DataStoreService, TextService, Players:BanAsync, TeleportService, BrickUI (Check-UI style).

**Spec:** `docs/specs/2026-10-10-admin-menu-design.md`

## Global Constraints
- Admins: `{[1809064431] = true}` only. Every remote call checks it on the server first.
- Multipliers: money {2,3,5}, speed {2,3,5}, hatch {2,3}; event duration 5..120 minutes; announcement 1..200 chars.
- Give limits: money 1..1e15, pet KG 1..1e7 and a name in CreatureConfig.byName, potion key in PotionConfig.byKey, 1..50.
- Ban durations: 3600, 86400, 604800 seconds or -1 (forever); reason 1..100 chars.
- Never show unfiltered text: filter failure = announcement not sent.
- UI = check-ui-clean-roblox via BrickUI (GothamBlack, slate canvas, 3D bevels, red [X]); one window at a time
  (fire MainMenu `CloseWindow`).
- No git here: before editing an existing script, clone it into `ServerStorage._Backup_Admin.Before` (Disabled).
- Tests use TestFreshSave = true; set it back to false at the end. Never publish (the owner does).

## Review Focus
1. Own echo: the sending server gets its own MessagingService message back -> must not apply twice (dedupe by id).
2. Player not in any server -> no server answers -> the menu shows "not online" after 6 s, not a hang.
3. Owner targets themselves with kick/ban -> rejected with a message.
4. Event end passes with no stop message (or a server that started late) -> attributes cleared at endsAt.
5. Blank / whitespace-only / 201-char announcement or a non-number amount -> rejected before anything is sent.

---

### Task 1: AdminLogic (pure rules) + test runner

**Files:**
- Create: `ServerScriptService.AdminLogic` (ModuleScript)
- Create: `ServerStorage.AdminTests` (ModuleScript returning `function(): (number, {string})` = passed, failures)

**Interfaces (Produces):**
- `AdminLogic.ADMINS: {[number]: boolean}`, `AdminLogic.isAdmin(userId: number): boolean`
- `AdminLogic.validate(kind: string, args: table, ownerId: number): (boolean, table | string)` - kinds:
  `announce{text}`, `eventStart{money?, speed?, hatch?, luckyRain?, minutes}`, `eventStop{}`,
  `giveMoney{user, amount}`, `givePet{user, pet, kg}`, `givePotion{user, potion, count}`, `kick{user, reason}`,
  `ban{user, seconds, reason, alts}`, `unban{user}`, `restart{message}`, `eggs{count}`, `wave{waveType}`.
  Returns cleaned args (trimmed strings, integers) or an error text. `user` = 3..20 chars `[%w_]`.
- `AdminLogic.eventAttributes(ev: {money, speed, hatch, luckyRain, endsAt}?, now: number): {[string]: any}` ->
  `Event_Money, Event_Speed, Event_Hatch` (1 when off), `Event_LuckyRain` (bool), `Event_EndsAt` (0 when off).
- `AdminLogic.luckyOdds(base: number, rain: boolean): number` (0 stays 0; rain -> max(1, floor(base / 10))).
- `AdminLogic.hatchExtra(potion: boolean, eventHatch: number): number` (extra seconds per second: potion 1 + event-1).
- `AdminLogic.newLimiter(gap: number)` -> `limiter:allow(key, now): boolean` (1 call per `gap` seconds per key).
- `AdminLogic.newSeen(max: number)` -> `seen:add(id): boolean` (false if already seen; keeps the last `max` ids).

- [ ] **Step 1: Write the failing tests** in `AdminTests` (mini runner: `check(name, cond)`), including:
  `isAdmin(1809064431) == true`, `isAdmin(1) == false`;
  `validate("announce", {text = "  hi  "}).text == "hi"`; blank, `string.rep("a", 201)` -> false;
  `validate("eventStart", {money = 4, minutes = 10})` false; `{money = 5, minutes = 10}` ok; minutes 4 / 121 false;
  all-boosts-off eventStart false; `validate("giveMoney", {user = "Bob", amount = "x"})` false;
  `validate("kick", {user = "Santrinio", reason = "x"}, ...)` with ownerName "Santrinio" -> false (self);
  `validate("ban", {user = "Bob", seconds = 5, ...})` false, `seconds = -1` ok;
  `eventAttributes(nil, 0).Event_Money == 1`; `eventAttributes({money = 2, endsAt = 100}, 50).Event_Money == 2`;
  `eventAttributes({money = 2, endsAt = 100}, 100).Event_Money == 1`;
  `luckyOdds(0, true) == 0`, `luckyOdds(800, true) == 80`, `luckyOdds(800, false) == 800`;
  `hatchExtra(true, 3) == 3`, `hatchExtra(false, 1) == 0`;
  limiter: allow(1, 0) true, allow(1, 0.5) false, allow(1, 1.1) true;
  seen: add("a") true, add("a") false.
  (Self-target check: `validate` takes the owner's username as `args._ownerName`, set by the server.)
- [ ] **Step 2: Run** in Edit: `return require(game.ServerStorage.AdminTests:Clone())()` -> Expected: fails (module missing).
- [ ] **Step 3: Implement `AdminLogic`** with the values from Global Constraints.
- [ ] **Step 4: Run** the same -> Expected: all passed, 0 failures.

### Task 2: Game hooks (events change the real game)

**Files:**
- Modify: `ReplicatedStorage.Boosts` (`Boosts.money`, `Boosts.speed`)
- Modify: `ServerScriptService.BaseHatchery` (`potionHatch` -> extra = `AdminLogic.hatchExtra(...)`)
- Modify: `ServerScriptService.EggSpawner` (`rollWeight` odds, `AdminEggs` BindableFunction, no respawn for bonus eggs)
- Modify: `ServerScriptService.WaveServer` (`AdminWave` BindableFunction)
- Modify: `ServerScriptService.PlayerData` (no load/save in the soft-restart lobby)

**Interfaces:**
- Consumes: workspace attributes from Task 1 names; `AdminLogic.luckyOdds`, `AdminLogic.hatchExtra`.
- Produces: `ServerStorage.AdminEggs:Invoke(count: number): number` (lucky eggs spawned per area, AdminBonus = true,
  not replaced when they expire); `ServerStorage.AdminWave:Invoke(waveType: string?): string` (type started);
  restart lobby = `game.PrivateServerId ~= "" and game.PrivateServerOwnerId == 0`.

- [ ] **Step 1: Back up** the 5 scripts into `ServerStorage._Backup_Admin.Before`.
- [ ] **Step 2: Failing test** (append to AdminTests): stand-in player `{GetAttribute = function() return nil end}`;
  set `workspace:SetAttribute("Event_Money", 3)`; `Boosts.money(p) == 3 * Boosts.money(p)` measured with the
  attribute 1 vs 3 (ratio 3); same for `Event_Speed` on `Boosts.speed`; clear attributes after.
- [ ] **Step 3: Run** -> Expected: ratio test fails.
- [ ] **Step 4: Implement**: Boosts multiplies by `(workspace:GetAttribute("Event_Money") or 1)` / `Event_Speed`;
  BaseHatchery runs the per-second egg advance when `extra > 0` using `extra` instead of 1; EggSpawner uses
  `AdminLogic.luckyOdds(KG_LUCKY_ODDS[area], workspace:GetAttribute("Event_LuckyRain") == true)` and a
  `forceLucky` counter for AdminEggs; expiry respawn skipped when `egg:GetAttribute("AdminBonus")`;
  WaveServer AdminWave calls `spawnWave(waveType or pickType(anyType))`; PlayerData returns early from load/save in
  the lobby.
- [ ] **Step 5: Run** unit tests -> all pass. Play test (server): set `Event_Hatch = 3` and confirm an egg's
  `ReadyAt` drops ~3 s per second; `AdminEggs:Invoke(1)` returns the area count and new eggs have Weight > KG_MAX of
  their area (lucky); `AdminWave:Invoke("Normal")` adds a Wave in `workspace.Waves`. Clear attributes.

### Task 3: AdminServer (commands, cross-server, events, log)

**Files:**
- Create: `ServerScriptService.AdminServer` (Script)
- Create at runtime: `ReplicatedStorage.Admin` folder with `Command` (RemoteFunction), `Banner` (RemoteEvent),
  `Reply` (RemoteEvent, admins only)
- Create: `ServerStorage.AdminDebug` (BindableFunction, Studio only): `Invoke(fakePlayer, kind, args)` runs the same
  handler as the remote.

**Interfaces:**
- Consumes: Task 1 (`validate`, `isAdmin`, `newLimiter`, `newSeen`, `eventAttributes`), Task 2 bindables,
  `ServerStorage.GivePet`, `ServerStorage.GivePotion`, `Players:BanAsync/UnbanAsync`.
- Produces: `Command:InvokeServer(kind, args) -> {ok: boolean, msg: string}`;
  `Banner:FireAllClients({kind = "announce" | "restart", text, from, seconds?})`;
  `Reply:FireClient(admin, {id, ok, msg})` for answers that arrive later from other servers;
  MessagingService topics `Admin` ({id, kind, args, from, fromServer}) and `AdminReply` ({id, ok, msg, to});
  MemoryStore hash map `AdminEvent`, key `current`; DataStore `AdminLog_v1` key `log` (last 100).

- [ ] **Step 1: Failing integration test** (Play, Server): `AdminDebug:Invoke({UserId = 123, Name = "x"}, "announce",
  {text = "hi"})` -> `{ok = false}`; owner stand-in (UserId 1809064431) announce "hello" -> ok, a client listener
  on `Banner` receives text "hello"; eventStart money 2 for 5 min -> `workspace.Event_Money == 2` and the MemoryStore
  key exists; eventStop -> `Event_Money == 1`; giveMoney to the local player 1000 -> Money +1000 exactly (no boosts);
  givePet / givePotion -> inventory / count grows; giveMoney to "NoSuchUser123" -> reply "not online" within 6 s;
  kick of the owner -> rejected; second command within 1 s -> "slow down".
- [ ] **Step 2: Run** -> Expected: fails (AdminServer missing).
- [ ] **Step 3: Implement AdminServer**: handler = isAdmin -> limiter -> validate -> log -> apply.
  Local apply + publish (with `pcall`, 2 retries); subscriber skips ids already seen.
  Player commands: the server where `Players:FindFirstChild(user)` (case-insensitive Name match) runs it and
  publishes `AdminReply`; the origin server forwards to the admin with `Reply`; origin starts a 6 s timer -> "not online".
  Events: write MemoryStore (expiry = minutes*60 + 30), publish; every server sets attributes from
  `eventAttributes`; a 1 s loop clears them at `Event_EndsAt`; on start each server reads `current`.
  Announce: `TextService:FilterStringAsync(text, admin.UserId, Enum.TextFilterContext.PublicChat)` ->
  `GetNonChatStringForBroadcastAsync()`; failure -> `{ok=false, msg="Filter failed - not sent"}`.
  Ban/unban: `Players:BanAsync({UserIds={id}, Duration=seconds, DisplayReason=reason, PrivateReason="by admin",
  ExcludeAltAccounts=not alts, ApplyToUniverse=true})`, id from `Players:GetUserIdFromNameAsync`.
  Restart: every server (ignore if the server is < 60 s old) fires `Banner` restart with 30 s, waits, then
  `TeleportService:TeleportAsync(game.PlaceId, players, options with ReservedServerAccessCode)`; in the lobby server
  each joining player is teleported back to `game.PlaceId` (3 tries, then kick "The game updated - please rejoin").
  Eggs / wave: call Task 2 bindables (owner's server only). Log: `UpdateAsync` append, keep 100.
- [ ] **Step 4: Run** the integration test -> Expected: all lines pass (ban/restart/teleport: Studio returns the
  engine's "not available in Studio" error as `{ok=false}` - accepted, verified live).

### Task 4: Banner + event pill (every player)

**Files:**
- Create: `StarterPlayerScripts.AdminBannerClient` (LocalScript; builds `PlayerGui.AdminBanner`, ResetOnSpawn false,
  DisplayOrder 6)

**Interfaces:** Consumes `ReplicatedStorage.Admin.Banner` payloads and workspace `Event_*` attributes (Task 3).

- [ ] **Step 1: Failing check** (Play, Client): after `Banner` fires "hello", `PlayerGui.AdminBanner.Banner.Visible`
  is true and its text contains "hello"; with `Event_Money = 2` and `Event_EndsAt = now + 300` the pill is visible and
  reads "ADMIN ABUSE" + "x2 MONEY" + "4:5x".
- [ ] **Step 2: Run** -> fails.
- [ ] **Step 3: Implement**: amber Check-UI banner (BrickUI.brick amber + header-style damier), top centre y 0.19,
  width 0.46, slide/pop in, 8 s (restart: live countdown "SERVER RESTART IN 30"), queue of messages, SFX
  `HatchWin`; event pill (purple brick, GothamBlack) top centre y 0.185 listing active boosts + mm:ss, moved to y 0.30
  while `TutorialUI` is visible; hidden when `Event_EndsAt <= now`.
- [ ] **Step 4: Run** -> passes; screenshot at 1080p and a phone-size viewport (no overlap with AreaTitle / HUD).

### Task 5: Admin menu (owner only)

**Files:**
- Create: `ServerStorage.AdminUI` (ScreenGui, ResetOnSpawn false, DisplayOrder 4) with LocalScript `AdminClient`
- Modify: `AdminServer` - clone `AdminUI` into the PlayerGui of admins on join (never for others)

**Interfaces:** Consumes `Command`, `Reply` (Task 3); MainMenu `CloseWindow` / `WindowOpened` BindableEvents.

- [ ] **Step 1: Failing check** (Play, Client as owner): `PlayerGui.AdminUI.AdminButton` exists; clicking it opens
  `Window` with tabs Announce / Events / Players / Server; Announce Send with "test" shows the green reply line.
  (Server side, AdminDebug: a fake non-admin player join path never receives AdminUI.)
- [ ] **Step 2: Run** -> fails.
- [ ] **Step 3: Implement** with BrickUI: amber 3D "ADMIN" button at the left edge just above the HUD tile grid;
  window 528x415-equivalent (Scale, WindowScale UIScale), Settings header "ADMIN", red [X], 4 tab buttons, pages:
  Announce (TextBox 200 chars + Send), Events (4 rows: toggle + multiplier chips, duration chips 5/15/30/60/120,
  Start / Stop), Players (username box, rows Give Money [amount], Give Pet [name dropdown + KG], Give Potion
  [key + count], Kick [reason], Ban [1h/1d/7d/forever + reason + alts toggle], Unban), Server (Soft restart
  [message] with a confirm press, Spawn lucky eggs [count 1..5], Start wave [type]); a reply line at the bottom
  (green ok / red error), filled from `InvokeServer` results and `Reply` events. Opening fires `CloseWindow`.
- [ ] **Step 4: Run** -> passes; screenshot each tab at 1080p and phone size.

### Task 6: Full verification + hand-off
- [ ] Run AdminTests (all pass) and the Task 3-5 checks again in one play session; console has no errors.
- [ ] Security pass: from the client, `Command:InvokeServer` with every kind while `AdminLogic.ADMINS` temporarily
  lacks the owner (Studio-only override attribute `AdminTestDenyOwner`) -> every call rejected, nothing changed.
- [ ] TestFreshSave false, remove test leftovers, export the new/changed sources to `docs/review/admin/` and get a
  fresh roblox-dev:roblox-reviewer pass; fix Critical/Important.
- [ ] Owner live checklist (two servers): announce, event start/stop + timer, give/kick across servers, ban/unban
  an alt, soft restart. Update memory.
