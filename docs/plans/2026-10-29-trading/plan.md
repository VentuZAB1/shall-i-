# SLINGSHOT Trading System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cross-server, server-authoritative pet/egg trading that can't duplicate, steal or lose items, plus the HUD
changes and the trading UI the owner asked for.

**Architecture:**
- Version-checked saves (`SaveLock`) under PlayerData.
- A pure state machine (`TradeCore`).
- Item escrow inside BaseHatchery (`TradeItems`).
- Presence + busy locks in MemoryStore (`TradePresence`).
- A trade node (`TradeServer`) that runs sessions in MemoryStore, wakes the other server through MessagingService,
  writes one DataStore record per round, and settles each round exactly once.
- A Check-UI client (`TradeClient`).

**Tech Stack:** Roblox Luau in Studio (scripts live in the place and are edited through the Studio MCP). DataStoreService,
OrderedDataStore, MemoryStoreService HashMaps, MessagingService, PolicyService, SocialService.

**Spec:** `Desktop/SLINGSHOT Creatures/docs/specs/2026-10-29-trading-design.md` (v4). Read it fully before any task.
The spec wins over this plan.

**Ledger:** `Desktop/SLINGSHOT Creatures/docs/plans/2026-10-29-trading/progress.md`. One line per finished task, one
`Ruling:` line per deviation. There is no git: "commit" = a ledger line + the backup rule below.

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

---

### Task 0: Audit + backups (no behaviour change)

**Files:**
- Create: `ServerStorage._Backup_Trading.Before` (Folder) with backups of PlayerData, BaseHatchery, Receipts,
  ShopServer, AdminServer, AutoReconnectServer, SellServer, EggSpawner, StarterGui.MainMenu.MenuController,
  ServerStorage.AdminUI.AdminClient.
- Create: `docs/plans/2026-10-29-trading/progress.md` (ledger, first line `# SDD ledger - plan: <this file>`).

**Interfaces:**
- Produces (ledger section "Audit"): facts later tasks rely on.

- [ ] **Step 1:** Make the backups (Global Constraints rule).
- [ ] **Step 2: Audit and record in the ledger, one line each:**
  - every item remover (SellServer handle; BaseHatchery place / equip / unequip / equipBest / hatch / skip;
    EggSpawner bank / drop): a yield between its check and its remove, yes or no, with the line;
  - `Tool.CanBeDropped` for pet AND egg tools (expected false for both);
  - Receipts `process()` order: grant -> `addId` -> save. List every Receipts handler that yields AFTER granting;
  - every caller of `ServerStorage.AddGiftedPass` and when it writes an absent player's save;
  - the soft restart `sendToLobby` (no save before the teleport today);
  - the JSON size of the largest test save (expect far below the 4 MB limit).
- [ ] **Step 3: Verify the PolicyService field name in a TestFreshSave Play session (Server datamodel):**
  `PolicyService:GetPolicyInfoForPlayerAsync(player)` and print its keys.
  - Expected: `IsPaidItemTradingAllowed` present -> ledger line.
  - If absent: `Ruling:` use the closest documented field, and mark it for the owner in the final report.
- [ ] **Step 4:** Ledger line `Task 0: complete`.

### Task 1: Version-checked saves (`SaveLock`) under PlayerData

**Files:**
- Create: `ServerScriptService.SaveLock` (ModuleScript).
- Modify: `ServerScriptService.PlayerData` (load / write / seal / SavePlayerNow / AddGiftedPass / leave / BindToClose).
- Modify: `ServerScriptService.Receipts` (`KEEP = 200`; the grant and `addId` in one synchronous step: no yield
  between a handler's grant and `addId`, and PurchaseGranted only after a successful save).
- Modify: `ServerScriptService.AdminServer` (`sendToLobby`: `SavePlayerNow` for each player, up to 10 s total, before
  the teleport; the lobby itself never loads or saves).
- Modify: `ServerScriptService.ShopServer` only if Task 0 found a gift path that writes an owned save.
- Test: `ServerStorage.SaveLockTests` (ModuleScript): `.pure()` in Edit, `.live(player)` in Play.

**Interfaces:**
- Produces:
  - `SaveLock.new(store: DataStore, key: string) -> lock`, a per-save object with:
    - `lock:load() -> (ok: boolean, data: table?, isNew: boolean)`;
    - `lock:write(snapshot: table) -> (ok: boolean, why: string?)`, where `why` is `"lost" | "error"`;
    - `lock:release(snapshot: table) -> ok`;
    - `lock.lost: boolean`.
  - `load` = an `UpdateAsync` that writes `_session = HttpService:GenerateGUID(false)` (new per load), `_ver += 1`,
    `_wid = GUID` and returns the stored table (nil -> new save).
  - `write`:
    - queued per lock, one at a time; the snapshot and the expected `_ver` are taken when the write RUNS;
    - writes only if the stored `_session` == the lock's token and `_ver` == expected; bumps `_ver` and sets a new
      `_wid`;
    - on error, reads back with a no-change `UpdateAsync`: own `_wid` = landed, same token + expected ver = resend,
      anything else = lost.
  - `release` = write with `_session = nil`.
  - `SaveLock.inbox(userId) -> store key` helpers for `GiftInbox_v1`:
    - `SaveLock.addGift(userId, gift, purchaseId) -> ok` (one `UpdateAsync`, no duplicate purchaseId);
    - `SaveLock.takeGifts(userId) -> {entries}`, then `SaveLock.ackGifts(userId, purchaseIds)`.
  - PlayerData keeps every existing BindableFunction name and signature (`SavePlayerNow`, `SealForReconnect`,
    `UnsealPlayer`, `AddGiftedPass`, `PlayerDataDebug`).
  - New: `ServerStorage.SaveLost` (BindableEvent `(player)`) fires when a save is lost. In Studio with
    `workspace.SaveLockTestNoKick == true`, it doesn't kick (sets the attribute `SaveLost = true` instead).
  - New PlayerData FIELDS: `TradeEscrow = "{}"`, `SettledRounds = ""`, `TradeHistory = "[]"`.
  - New hook for Task 5: `ServerStorage.TradeRecoveryHook` (BindableFunction, set by TradeServer), called with
    `(player)` after the attributes are set and BEFORE `DataLoaded = true`. If it's missing or errors, the load
    continues (the 30 s check retries later).

- [ ] **Step 1: Write the failing tests in `SaveLockTests` (each a named check):**
  - `legacy_save_loads`: a stored save with no meta fields loads, gets `_session` + `_ver = 1`, and the next write
    succeeds.
  - `takeover_refuses_old_writer`: lock A loads, lock B loads the same key, then A's write returns
    `false, "lost"` and B's succeeds.
  - `slow_old_write_refused`: A's write runs after B took over -> lost (simulated delay).
  - `readback_after_error`: a write that "errors" after landing is detected as landed through `_wid`, with no second
    write.
  - `release_sets_nil`: after `release`, the stored `_session == nil`.
  - `queue_one_at_a_time`: two writes started together run in order, and both land.
  - `gift_inbox_once`: `addGift` twice with the same purchaseId gives one entry; `takeGifts` + `ackGifts` empties it.
  - `receipt_grant_and_id_atomic`: in a live test, `TestProcessReceipt` with a granting product leaves `ReceiptIds`
    containing the id in the same attribute snapshot as the grant. A forced refused save (simulated takeover) returns
    `NotProcessedYet`.
  - `seal_still_works`: `AutoReconnectTests.server(player)` all pass (existing suite).
- [ ] **Step 2:** Run `.pure()` (Edit) -> FAIL (module missing).
- [ ] **Step 3:** Implement `SaveLock` and wire PlayerData / Receipts / AdminServer as in Interfaces.
  - AddGiftedPass for an absent player uses `SaveLock.addGift` (never writes the save).
  - Every load takes the inbox (`takeGifts`), adds `GiftedPasses` + `ReceiptIds`-style ids in one step, saves, then
    `ackGifts`.
  - Online players also take their inbox every 60 s.
- [ ] **Step 4:** Run `.pure()` (Edit) and `.live(player)` (Play, TestFreshSave) -> all pass; the AutoReconnect
  suite passes.
- [ ] **Step 5:** Ledger line + reviewer gate.

### Task 2: `TradeConfig` + `TradeCore` (pure state machine)

**Files:**
- Create: `ReplicatedStorage.TradeConfig` (ModuleScript: the limits, the phrases, `ENABLED`, `stores()` returning
  every store/topic name with the Studio suffix rule).
- Create: `ServerScriptService.TradeCore` (ModuleScript, no services).
- Test: `ServerStorage.TradeCoreTests` (`.pure()` in Edit).

**Interfaces:**
- Produces (all pure, `now` is passed in; every function returns `(ok, newSessionOrResult | reason)` and never
  mutates its input):
  - `TradeCore.petSig(pet) -> string` = `id|name|%.17g kg|mutKey`;
    `TradeCore.eggSig(kind, kg, mutList) -> string` = `kind|%.17g kg|mutKey` (`kg` must be finite and > 0).
  - `TradeCore.newSession(id, a: {uid,name,job}, b: {uid,name,job}, now) -> session`
    (phase `select`, `ver = 1`, `round = 0`).
  - `TradeCore.addItem(s, side, item, owned, now)`, where `item = {t = "pet"|"egg", sig, ...}` and `owned` = the count
    of that sig the owner has. Refuses: wrong phase, 9 items, a duplicate pet sig, egg count > owned, rate limits.
  - `TradeCore.removeItem(s, side, index, now)`.
  - `TradeCore.ready(s, side, clientVer, now)`: refuses if `clientVer ~= s.ver` or `now < s.changedAt + 5`.
  - `TradeCore.startConfirm(s, now)`: when both ready == ver -> phase `confirm`, `round += 1`, `escrowed = {}`,
    `confirmAt = now`.
  - `TradeCore.setEscrowed(s, side, round, items)`.
  - `TradeCore.accept(s, side, clientVer, now, localSeenAt)`: refuses unless phase confirm, ver matches,
    `escrowed[side].round == s.round`, and `now >= localSeenAt + 5`.
  - `TradeCore.toCommit(s)`: only if both accepts == ver and both `escrowed` == round -> phase `commit`.
  - `TradeCore.back(s, now)`: phase confirm -> `select` with EMPTY offers, cleared ready / accept / escrowed, `ver += 1`.
    Refused in phase commit.
  - `TradeCore.cancel(s, why)`: refused in phase commit.
  - `TradeCore.chat(s, side, phraseIndex, now)`: doesn't change ver or changedAt.
  - `TradeCore.expired(s, now) -> boolean` (idle 3 min / total 10 min).
  - `TradeCore.record(s) -> {a, b, itemsA, itemsB}`: only from `escrowed`; nil if either list is missing.

- [ ] **Step 1: Write the failing tests:**
  - `phase_flow` (select -> confirm -> commit);
  - `old_ver_ready_refused`, `ready_5s_lock`, `accept_5s_lock`, `accept_needs_own_escrow`;
  - `nine_cap`, `dup_pet_refused`, `egg_overcount_refused`, `nan_inf_kg_refused`;
  - `change_clears_ready_accept`, `back_empties_offers`, `back_refused_in_commit`, `cancel_refused_in_commit`;
  - `commit_needs_both_escrows`, `record_from_escrow_only`;
  - `chat_keeps_ver`, `idle_and_total_timeout`, `studio_store_names`.
- [ ] **Step 2:** Run -> FAIL. **Step 3:** Implement. **Step 4:** Run -> all pass. **Step 5:** Ledger + reviewer gate.

### Task 3: `TradeItems` (take / give inside BaseHatchery)

**Files:**
- Modify: `ServerScriptService.BaseHatchery` (a new BindableFunction `ServerStorage.TradeItems`). Any remover that
  Task 0 found yielding gets the per-player `ItemLock`.
- Test: `ServerStorage.TradeItemsTests` (`.live(player)` in Play; it uses the HatcheryDebug give/place helpers).

**Interfaces:**
- Consumes: `TradeCore.petSig`, `TradeCore.eggSig`.
- Produces:
  - `TradeItems:Invoke("count", player) -> {[sig] = n}`: the owned counts for offers.
  - `TradeItems:Invoke("describe", player, ref) -> item | nil`. `ref = {t="pet", id}` or
    `{t="egg", kind, kg, mutKey}`; `item = {t, sig, name/kind, kg, mut, from = "base"|"inv"}` built from server data.
  - `TradeItems:Invoke("take", player, items) -> (true, removed: {item...}) | (false, reason)`: all-or-nothing, no
    yields; Tools destroyed by instance only in the player's own Backpack/Character, one per item.
  - `TradeItems:Invoke("give", player, items, mode) -> true`. `mode = "deliver"` (new pet ids, Index record, to the
    inventory) or `"return"` (same items back where they came from if a base slot is free, else the inventory). It
    never fails and may exceed 150. It rebuilds Tools, fires `EggInventoryChanged`, respawns base pets.

- [ ] **Step 1: Write the failing tests:**
  - `take_all_or_nothing` (one missing item -> nothing removed);
  - `take_matches_full_sig` (same id, different KG -> refused);
  - `take_destroys_only_own_tools` (a fake second player's Tool with the same `PetId` survives);
  - `exact_kg_eggs` (a 100.5 KG and a 100.4 KG egg are different sigs);
  - `return_goes_back_to_base`, `deliver_new_ids_unique`, `over_cap_after_give`, `give_never_fails`.
- [ ] **Steps 2-5:** FAIL -> implement -> pass -> ledger + reviewer gate.

### Task 4: `TradePresence` (online list, busy locks, friends, search)

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

### Task 5: `TradeServer` part A (requests, sessions, phases, the bus)

**Files:**
- Create: `ServerScriptService.TradeServer` (Script), which requires `ServerScriptService.TradeNode` (ModuleScript:
  everything with an injectable `{jobId, bus, players, memory, ledger, items, saves}` so two nodes can run in one
  Studio server).
- Create: remotes in `ReplicatedStorage.Trade`:
  - `Request` (RemoteFunction): `send(uid)`, `respond(reqId, accept)`, `cancelRequest(reqId)`;
  - `Action` (RemoteFunction): `add(ref)`, `remove(i)`, `ready(ver)`, `accept(ver)`, `back()`, `cancel()`, `chat(n)`;
  - `Query` (RemoteFunction): `list()`, `search(text)`, `history()`;
  - `Push` (RemoteEvent, server -> client): session views, request pop-ups, toasts.
- Test: `ServerStorage.TradeSimTests` (`.partA(player)` in Play; node A = the real test player, node B = a virtual
  player object on a second node).

**Interfaces:**
- Consumes: Task 2 TradeCore, Task 3 TradeItems ("describe" / "count" only in this part), Task 4 TradePresence.
- Produces:
  - `TradeNode.new(env) -> node` with `node:handle(player, op, ...)` (used by the remotes and by the tests), the
    session store read/write through `TradeCore`, the 2 s poll, coalesced bus sends (≤ 4/s per trade), the per-viewer
    session view sent on `Push`, and every rate limit.
  - PolicyService is checked on the player's own node, cached for the session, and carried in the request/session.
- [ ] **Step 1: Write the failing tests:**
  - `request_cross_node`, `request_ack_timeout`, `three_pending_max`, `send_limits`, `decline_cooldown`;
  - `self_trade_refused`, `tutorial_refused`, `policy_refused`;
  - `offer_sync_cross_node`, `ready_lock_resets`, `change_rate_limits`, `chat_limits`;
  - `idle_and_total_timeout`, `second_trade_refused`, `kill_switch_refuses`.
- [ ] **Steps 2-5:** FAIL -> implement -> pass -> ledger + reviewer gate.

### Task 6: `TradeServer` part B (escrow, commit, record, settle, recovery)

**Files:**
- Modify: `ServerScriptService.TradeNode`.
- Modify: `ServerScriptService.PlayerData` (only: set `ServerStorage.TradeRecoveryHook` use, already added in Task 1).
- Test: `ServerStorage.TradeSimTests` (`.partB(player)`), plus `ServerStorage.TradeSimTests.crash(player)` and
  `.exploit(player)` / `.budget(player)`.

**Interfaces:**
- Consumes: Task 1 SaveLock (the queue write, `SaveLost`, `TradeRecoveryHook`), Task 3 take/give, Task 2
  `toCommit` / `record`.
- Produces:
  - **Escrow:** `take` -> a `TradeEscrow["<id>#<round>"]` entry -> a queued save -> on success
    `escrowed[side] = {round, items}`.
  - **Commit:** session -> `commit` (conditional), then the ledger `UpdateAsync` writes only if empty, using
    `TradeCore.record`; act only on the returned value; read back after an error; the dead-committer rule (30 s from
    this node's first sight).
  - **Settle:** one synchronous step (give + delete entry + add to `SettledRounds` + History), then save.
  - **Recovery:** on the `TradeRecoveryHook` and the 30 s check, exactly per spec invariant 6.
  - **BACK / cancel order:** session first, then "aborted".
  - **Teleport / shutdown:** cancel in select/confirm, keep in commit.
  - **SaveLost** -> cancel through the record.
- [ ] **Step 1: Write the failing tests (each ends with a conservation check: the item multiset across both players
  before == after, no item twice):**
  - `trade_completes_cross_node`, `trade_completes_same_node`, `both_accept_same_tick`;
  - `back_racing_commit`, `back_then_round2_commits`;
  - `escrow_fail_aborts_round`, `escrow_save_refused_aborts`, `record_error_after_landing`;
  - `dead_committer_finished`, `check_30s_leaves_live_confirm`, `check_30s_settles_existing_record`;
  - `takeover_mid_trade` (node B "loads" the test player's save mid-trade);
  - `crash_after_escrow`, `crash_after_commit_phase`, `crash_after_record`, `crash_before_settle` (drop the node,
    reload the players through recovery);
  - exploit set: `forged_refs`, `other_players_pet_id`, `same_pet_9x`, `fake_egg`, `early_ready_accept`, `old_ver`,
    `remote_spam`, `tenth_item`, `full_inventory_refused`, `away_target_refused`;
  - `budget` (prints MemoryStore / DataStore / Messaging calls per trade and per minute into the ledger).
- [ ] **Steps 2-5:** FAIL -> implement -> pass -> ledger + reviewer gate.

### Task 7: UI (Trading tile, Admin button, Trading menu, request pop-up, trade window)

**Files:**
- Create: `StarterPlayer.StarterPlayerScripts.TradeClient` (LocalScript).
- Modify: `StarterGui.MainMenu.MenuController` (the Trading tile in the left menu tiles; a modal lock while a trade is
  open; a `Trade` page id).
- Modify: `ServerStorage.AdminUI.AdminClient` (`placeButton`: below the Rebirth and Index tiles instead of above Shop).
- Create mockup files: `docs/plans/2026-10-29-trading/ui/` (screenshots / offline renders of every screen).
- Test: `ServerStorage.TradeUITests` (client checks: the window opens/closes, the modal lock, the respawn rebuild,
  `menu_regression`).

**Interfaces:**
- Consumes: the Task 5/6 remotes and the `Push` view payload.
- Produces the screens:
  - the tile "🤝 Trading";
  - the Trading menu (Players | History, search, rows with headshot / @name / status / SEND, a disabled SEND with its
    reason, Invite Friends);
  - the bottom-right request card (ACCEPT / DECLINE, 30 s bar, up to 3 stacked);
  - the trade window:
    - Phase 1: inventory Pets / Eggs, the two 3x3 offers with $/s totals, READY with countdown, CANCEL, chat with the 6
      phrases, "syncing...";
    - Phase 2: read-only, exact KG + mutation words, the "You give / You get" line, "Securing items...", ACCEPT with
      countdown, BACK, "Waiting for @B...";
    - Done: "Trade complete!" with what you gave and what you got.
- [ ] **Step 1: Mockups** of every screen (Check-UI), reviewed by a fresh reviewer until each scores ≥ 8.5.
- [ ] **Step 2:** Write the failing UI tests (`menu_regression`, `trade_window_modal`, `rebuild_after_respawn`,
  `request_card_stack`).
- [ ] **Step 3:** Build to the approved mockups.
- [ ] **Step 4:** Run the tests. Phone emulator pass (the Device emulator, landscape phone) with text floors / tap
  targets measured. Final screenshots reviewed ≥ 8.5.
- [ ] **Step 5:** Ledger + reviewer gate.

### Task 8: Whole-system security review, fixes, wrap-up

- [ ] **Step 1:** A fresh reviewer reads the spec's safety section + every new/changed script, and attacks the code
  (not the design) against invariants 1-6 and the exploit table.
- [ ] **Step 1b: Hands-on red team** (owner, 2026-10-29: "you do the testing, use my computer if needed, to do trading
  and trying to find a hole"). The controller drives Studio with computer-use:
  - start Test > Clients and Servers with 2 players (TestFreshSave on) and do real trades between the two clients:
    same items, BACK / CANCEL, closing a client mid-Phase-2, spam-clicking, a full inventory, eggs with mutations;
  - from a client datamodel (`execute_luau`), fire every trade remote with forged arguments (other players' pet ids,
    wrong versions, early accept, huge strings, spam);
  - after each attempt, check conservation on the server.
  - Every hole found becomes a failing test + fix (Step 2).
- [ ] **Step 2:** Every Critical/Important finding gets a failing test first, then the fix, then the full suite.
- [ ] **Step 3:** Full suite once more: SaveLockTests, TradeCoreTests, TradeItemsTests, TradePresenceTests,
  TradeSimTests (partA, partB, crash, exploit, budget), TradeUITests, AutoReconnectTests, the existing StreakTests /
  StarterPackTests live parts (regression).
- [ ] **Step 4:**
  - Clean up `_Studio` test keys.
  - Set `TestFreshSave = false`.
  - File > Save to Roblox (NOT publish) and verify the new saved version through the saved-versions API.
  - Update memory + vault (game-agnostic lessons only).
  - Write the owner report: what was built, every test and its result, rulings, what the owner must do (Publish,
    then Migrate servers).
