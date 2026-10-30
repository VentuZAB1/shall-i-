# Task 4 brief: `TradePresence` (online list, busy locks, friends, search)

Plan: `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\plans\2026-10-29-trading\plan.md` (do NOT read the whole plan; this brief is your requirements).
Spec (the binding authority, read the sections your task touches): `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\specs\2026-10-29-trading-design.md`

## Task 4: `TradePresence` (online list, busy locks, friends, search)

**Files:**
- Create: `ServerScriptService.TradePresence` (ModuleScript; injectable `memory` / `datastore` / `players` adapters,
  so tests can fail them).
- Test: `ServerStorage.TradePresenceTests` (`.live(player)` in Play).

**Interfaces:**
- Consumes: `TradeConfig.stores()`.
- Produces:
  - `TradePresence.start(jobId)` (refresh loop every 40 s, TTL 120 s; on join it writes `TradeSeen` after a
    successful load; it never yields the load path).
  - `TradePresence.isOnline(uid) -> (online: boolean, job: string?)`.
  - `TradePresence.onlineList() -> {{uid, name}}` (cached, rebuilt at most every 10 s).
  - `TradePresence.rowsFor(viewer) -> {{uid, name, status = "ONLINE"|"AWAY"}}`: ONLINE (any server) + the viewer's
    AWAY friends, with job ids stripped. Friends: `GetFriendsAsync`, cached 5 min; up to 100 checked; 40 seen-reads per
    minute per server, cached 10 min.
  - `TradePresence.search(viewer, text) -> rows | reason`: exact username lookup; non-friends who are away ->
    `"@name isn't online"`.
  - `TradePresence.takeBusy(uidLow, uidHigh, tradeId) -> ok` (conditional, rolled back on failure, stale locks cleared
    first) / `TradePresence.releaseBusy(uid, tradeId)` (only if it still holds this id).

- [ ] **Step 1: Write the failing tests:**
  - `online_then_away`, `away_only_for_friends` (a fake friend list), `search_exact_name`, `job_ids_stripped`;
  - `busy_take_both_or_none`, `busy_release_only_own`, `stale_busy_cleared`;
  - `presence_failure_does_not_block_load` (an injected failing memory adapter).
- [ ] **Steps 2-5:** FAIL -> implement -> pass -> ledger + reviewer gate.


## Global Constraints
- **NEVER publish.** At the very end the controller does File > Save to Roblox only (not Publish). The owner publishes.
- **TestFreshSave:** before EVERY Play test, check `workspace:GetAttribute("TestFreshSave") == true` in Edit (set it if
  it isn't). The controller sets it back to `false` after the LAST test of the whole job.
- **Never type into the Studio command bar or click Studio dialogs.** Use `execute_luau` for DataModel work. Never set
  `Camera.CameraType` from Edit scripts.
- **Backups:** before changing any existing script, clone it into `ServerStorage._Backup_Trading.Before`, with
  `Disabled`/`Enabled = false` and all CollectionService tags stripped. One backup per script, the first time only.
- **Studio names:** every DataStore / OrderedDataStore / MemoryStore map / MessagingService topic name gets the suffix
  `_Studio` when `RunService:IsStudio()`. Studio must never read or write a live trading store. `PlayerData_v3`
  itself keeps its existing test keys (`studiotest_<tag>_<userId>` when TestFreshSave).
- **Kill switch:** `ReplicatedStorage.TradeConfig.ENABLED` (default true). When false: no Trading tile, every trade
  remote refuses, sessions can't start. Recovery and settle ALWAYS run (items in escrow must still come back).
- **Every `UpdateAsync` callback is pure** (it may run more than once): side effects only after it returns.
- **Big execute_luau work** is chunked with `task.wait()`; scripts are written with `multi_edit` or by setting
  `.Source` from `execute_luau`.
- **UI:**
  - The `check-ui-clean-roblox` skill look only: GothamBlack, slate `#3B5866` panels, `#181E22` strokes, 3D [X],
    2-tier header divider, damier fade. Reuse `ReplicatedStorage.BrickUI` (the project's Check-UI builder) wherever
    it has a piece.
  - One layout on every device (phones = the PC layout scaled).
  - The window fit rule: cap at ~58 % of the screen width, wider on short phone screens.
  - Tap targets ≥ 42 px.
- **Ship bar:** every UI screen is reviewed by a fresh reviewer and must score ≥ 8.5/10 before it counts as done.
- **Reviewers / planners = Haiku, builders = Opus** (owner rule).
- **Limits (spec section 4):**
  - 9 items per side;
  - READY locked 5 s after the last change;
  - ACCEPT locked 5 s after Phase 2 starts (and until your own escrow is saved);
  - request pop-up 30 s;
  - 1 SEND per 3 s and 10 per 5 min;
  - 3 pending requests per receiver;
  - a 30 s pair cooldown after a decline;
  - offer changes 4/s per player and 30 per 10 s per trade;
  - quick chat 1 per 1.5 s, same phrase 1 per 5 s;
  - search 1 per 2 s, list 1 per 5 s;
  - idle 3 min, total 10 min;
  - 150 pets / 150 eggs (deliveries and returns may exceed it).
- **Quick chat phrases (exact, in this order):** Add More, L Trade, Last Offer, Deal?, Fair Trade, No Thanks.


## Review Focus
1. **Existing live saves** have no `_session` / `_ver` / `_wid`. The first load after publish must take them over
   and save normally, with nothing else changed. Test in Task 1: `legacy_save_loads`.
2. **A Studio session must never touch a live trading store.** Test in Task 2: `studio_store_names`, which asserts
   every name in `TradeConfig.stores()` ends in `_Studio` in Studio.
3. **A MemoryStore / MessagingService outage must never block or break a player's join or normal play.** Only
   trading pauses. Test in Task 4: `presence_failure_does_not_block_load`, with an injected failing MemoryStore.
4. **A player over 150 pets/eggs after a delivery** can still play: selling works, new gains are refused with the
   normal message, no error. Test in Task 3: `over_cap_after_give`.
5. **The existing menu tiles, the Admin button and every other window still open and close** on PC and on a phone
   once the Trading tile is added. Test in Task 7: `menu_regression` (+ the phone emulator pass).

