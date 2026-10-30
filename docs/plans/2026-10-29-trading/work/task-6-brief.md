# Task 6 brief: `TradeServer` part B (escrow, commit, record, settle, recovery)

Plan: `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\plans\2026-10-29-trading\plan.md` (do NOT read the whole plan; this brief is your requirements).
Spec (the binding authority, read the sections your task touches): `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\specs\2026-10-29-trading-design.md`

## Task 6: `TradeServer` part B (escrow, commit, record, settle, recovery)

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

