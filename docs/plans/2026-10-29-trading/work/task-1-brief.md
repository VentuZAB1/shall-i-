# Task 1 brief: Version-checked saves (`SaveLock`) under PlayerData

Plan: `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\plans\2026-10-29-trading\plan.md` (do NOT read the whole plan; this brief is your requirements).
Spec (the binding authority, read the sections your task touches): `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\specs\2026-10-29-trading-design.md`

## Task 1: Version-checked saves (`SaveLock`) under PlayerData

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

