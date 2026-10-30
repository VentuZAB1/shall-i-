# Task 1 report: version-checked saves (SaveLock) under PlayerData

Builder: Opus, 2026-10-29. Studio id `3bf21205-caff-490e-a927-3bd9f0097311`. Nothing published or saved to Roblox.

## Status
DONE_WITH_CONCERNS: every check is green (pure 69/0, live 64/0, AutoReconnect server suite 79/0 inside the live run, AutoReconnect unit suite 83/0). The concerns below are about the rollout window and a few design rulings the reviewer should confirm.

## Scripts created / changed (backups)
| Script | What | Backup |
|---|---|---|
| `ServerScriptService.SaveLock` (ModuleScript, NEW, 339 lines) | the lock: `new / load / write / release / lost / onLost`, the queue, read-back, `judge`; gift inbox `inbox / addGift / takeGifts / ackGifts`; gift receipts `recordGift / giftRecord`; `addId / hasId`; `storeName` (`_Studio`); `useStores` / `backoff` test seams | new, no backup |
| `ServerStorage.SaveLockTests` (ModuleScript, NEW) | `.pure(verbose)` (Edit, fake stores), `.live(player, opts)` (Play), `.start()` (background run, report in `ServerStorage.SaveLockTestReport`) | new |
| `ServerScriptService.PlayerData` (Script, 376 -> 514 lines) | load via `lock:load()` (L202), inbox take on load (L219) + `applyGifts` (L177), `TradeRecoveryHook` (L160, called at L264, before DataLoaded), `write` through the lock (L273), `saveThenAck` / `deliverInbox` (L311 / L317), Unseal refuses a lost/released lock (L358), leave-save releases (L377), `AddGiftedPass` -> inbox (L402), autosave + 60 s inbox, BindToClose "close" release (L442), `SaveLost` event + kick (L132-145), 3 new FIELDS (L80-82), new debug ops | `ServerStorage._Backup_Trading.Before.PlayerData` (Task 0, verified identical to the pre-edit source) |
| `ServerScriptService.Receipts` (ModuleScript) | `KEEP = 200` (L19), header + comments (grant and id in one step, a lost save = NotProcessedYet). Logic unchanged: it already did `addId` straight after the handler returned and PurchaseGranted only after `SavePlayerNow` == true | `..._Backup_Trading.Before.Receipts` |
| `ServerScriptService.BaseHatchery` (Script) | SkipHatch receipt handler: `task.spawn(skipNow, player, target)` (L784), so the ~1.2 s grow wait runs in its own thread and the handler returns right after the grant. Same grant; still returns true when the egg is gone (owner decision, untouched) | `..._Backup_Trading.Before.BaseHatchery` |
| `ServerScriptService.ShopServer` (Script) | requires SaveLock (L30); `giveGift(..., purchaseId)` -> `AddGiftedPass(target, key, purchaseId)` (L182); gift receipt with no `pendingGift`: `SaveLock.giftRecord(purchaseId)` first, record = acknowledge only (true), read error = false, no record = the old buyer fallback (L244); Studio id-0 path uses `"studio_" .. GUID` (L315) | `..._Backup_Trading.Before.ShopServer` |
| `ServerScriptService.AdminServer` (Script) | `saveBeforeLobby(players)` (L164): `SavePlayerNow` for everyone in parallel, at most 10 s, called first in `sendToLobby` (L193; also covers the late-joiner path). Studio hook `ServerStorage.AdminSaveBeforeLobby` (L182). Lobby code untouched | `..._Backup_Trading.Before.AdminServer` |

The other Task 0 backups (AutoReconnectServer, SellServer, EggSpawner, MenuController, AdminClient) were not touched.

## RED (tests written first)
`.pure()` in Edit, before SaveLock existed:
```
SaveLock pure: 0 pass / 1 fail
FAIL SaveLock module loads [ServerScriptService.SaveLock not found]
```
`.live()` in Play against the OLD code (TestFreshSave + AutoReconnectTest, seal suite skipped):
```
SaveLock live: 12 pass / 21 fail
FAIL live_load: stored save has a _session token
FAIL live_load: stored _ver >= 1
FAIL live_load: the lock's token = the stored _session
FAIL live_load: new FIELDS with their defaults
FAIL live_load: ServerStorage.SaveLost is a BindableEvent
FAIL SavePlayerNow: _ver bumped, same token, new _wid
FAIL refused save (simulated takeover) -> NotProcessedYet [PurchaseGranted]
FAIL lost: SaveLost attribute set (SaveLockTestNoKick)
FAIL lost: ServerStorage.SaveLost fired for them
FAIL lost: the other server's save was never overwritten
FAIL cleanup: reacquire
FAIL cleanup: SaveLost cleared, saving again
FAIL leave: one leave-save [false]
FAIL leave: stored _session == nil (released) [nil]
FAIL cleanup: reacquire
FAIL cleanup: owned again, saving
FAIL gift_inbox_delivery: SaveLock module [missing]
FAIL gift_absent_player: SaveLock module [missing]
FAIL gift_retry_no_pending: SaveLock module [missing]
FAIL AdminSaveBeforeLobby hook exists
FAIL recovery_hook: SaveLock module [missing]
```
In that run the SkipHatch atomicity check passed by accident: a 1 KG egg starts at full height, so the grow wait never ran. I reproduced the real bug by hand on the old code with a growing 10000 KG egg (the same deferred probe the test uses: it runs at the receipt's first yield, the moment an autosave could take its snapshot):
```
placed=true | eggs: WoodEgg 10000 kg left=89 | decision=PurchaseGranted in 2.27 s | probe at first yield: granted=true id=false
```
That's the pet in the save without its purchase id. The test now uses a 10000 KG egg.

## GREEN
`.pure(true)` in Edit: **SaveLock pure: 69 pass / 0 fail**. It covers: legacy_save_loads (no meta -> `_session` + `_ver = 1`, nothing else changed, next write ok; a brand-new or meta-only save counts as new; load retried; a failed load never writes), takeover_refuses_old_writer (A -> `false, "lost"`, onLost once, a lost lock never calls the store or releases again, B writes), slow_old_write_refused (A in flight during B's takeover: compare-and-swap re-run -> lost; and A's queued write that only RUNS after the takeover -> lost), readback_after_error (landed then errored -> landed, exactly 1 commit; errored before landing -> sent again, 1 commit; throttled x2 -> retried; landed + every read-back failing -> "error", not lost, and the next write adopts it; not landed + read-backs failing -> "error", next write lands; snapshot nil -> nothing written), release_sets_nil (+ no write after it, a released save loads normally, a release whose answer was lost = landed), queue_one_at_a_time (order snap1, done1, snap2, done2; both land; never 2 requests at once), gift_inbox_once (same purchaseId twice = 1 entry; take + ack empties it; ack only the acked ids; inbox read error -> nil; gift record written once, read error is never "no record"; `_Studio` store names), addId keeps the newest 200. The fake store runs every UpdateAsync callback TWICE on fresh copies, with compare-and-swap, so a callback with side effects would show up.

`.live()` in Play (TestFreshSave = true and AutoReconnectTest = true, both checked in Edit right before Play), last run:
```
SaveLock live: 64 pass / 0 fail
```
The verbose run before it (63/63, before the hook-save check was added):
```
ok   live_load: stored save has a _session token / _ver >= 1 / lock token = stored _session / new FIELDS defaults / SaveLost is a BindableEvent
ok   SavePlayerNow ok / _ver bumped, same token, new _wid
ok   potion receipt -> PurchaseGranted; receipt_grant_and_id_atomic (potion): grant + id in one snapshot [granted true, id true]
ok   potion: stored save has the grant and the id; a retry is only acknowledged [3]
ok   SkipHatch receipt -> PurchaseGranted; receipt_grant_and_id_atomic (SkipHatch, growing egg): grant + id in one snapshot [granted true, id true]; pet in base data
ok   refused save (simulated takeover) -> NotProcessedYet; SaveLost attribute; SaveLost fired; not kicked (NoKick); SavePlayerNow refused; other server's save never overwritten; cleanup reacquire
ok   leave: one leave-save [leave]; stored _session == nil (released); nothing saved after it; cleanup reacquire
ok   addGift into my inbox; the 60 s check delivers it [1]; GiftedPasses has the pass; purchase id in the save; inbox emptied (acked after the save); stored save has it; a pass already there isn't added twice [1]; second gift acked
ok   AddGiftedPass to an absent player -> true; gift in their inbox; GiftReceipts record; their save never written; same purchase twice = one entry; no-purchaseId call works
ok   gift retry with a record -> PurchaseGranted, buyer gets nothing; without a record -> fallback, buyer has the pass, recorded
ok   AdminSaveBeforeLobby: 1 saved in 0.5 s; a version-checked write landed; one write in the log
ok   seal_still_works: AutoReconnectTests.server all pass [79 pass / 0 fail]; saving works after
ok   reload ok; TradeRecoveryHook called once; hook runs BEFORE DataLoaded, after the attributes [nil/{}]; load takes the inbox; inbox acked after the save; a hook that errors: load goes on; a hook that hangs: load goes on [11.2 s]; saving works after
```
The final run adds `the hook can save (SavePlayerNow inside it)`. After stopping Play I read the session's test key back in Edit: `_session = nil` (the BindToClose / leave release landed). The AutoReconnect unit suite in Edit is 83/0.

## Rulings (decided here, please confirm in review)
1. **`lock:write(snapshot)` takes a table OR a function.** The function is called when the write RUNS, which is what the "snapshot taken when it runs" rule needs. A function returning nil calls the write off, and nothing is written (PlayerDataDebug `failNext` uses that). `release` returns `ok, why`, and its first value is the brief's `ok`.
2. **The seal's final write is a version-checked write that does NOT release.** The token stays, so `UnsealPlayer` can go back to normal saving without a new takeover. The new server's load takes over anyway. A sealed player whose final write landed gets no leave-save (as before), so their save keeps the old token, which does no harm.
3. **A write whose outcome is unknown can be adopted later.** If a write errors and every read-back also errors, it returns `false, "error"` (never "lost") and its `_wid` is kept as "unsure". The next write accepts a stored `_wid` from that set (with our token) as our own landed write. That's the spec's "own `_wid` = landed" rule applied one write later. The literal "different `_ver` = lost" would falsely kick a player after a DataStore hiccup. After an unknown read-back, the next try is itself a conditional UpdateAsync that checks `_wid` first, so a write can never land twice.
4. **A brand-new player's load writes a lock-only stub,** so the takeover works for new players too. `isNew` means "no field other than the lock's", so a crash before the first real save doesn't turn a new player into a veteran.
5. **`takeGifts` reads with an uncached `GetAsync` (read budget only).** Applying is idempotent, and the ack happens only after a save that holds the gifts, so a stale read only delays a gift. `giftRecord` is a grant decision, so it uses a no-change UpdateAsync.
6. **Inbox keys follow PlayerData's key rule.** In Studio fresh sessions the key is `studiotest_<TestSaveTag>_<userId>`, so a free Studio id-0 gift can never reach a real save through the inbox. Live keys are `u_<userId>`. Gift receipts use `p_<purchaseId>`. Stores are `GiftInbox_v1` / `GiftReceipts_v1`, with `_Studio` added in Studio.
7. **Gift purchase ids from the inbox also go into the recipient's `ReceiptIds`** (spec: "records the purchase id in the save"). They share the 200-id window.
8. **An in-server gift is now saved at once.** If that save fails, the gift also goes to their inbox. A pass is a set, so this never doubles anything. The path returns true once the attribute is set, because returning false would trigger the buyer self-grant fallback, which is a double grant. For the same reason, a failed `GiftReceipts` write after delivery only warns.
9. **SkipHatch: only the receipt handler changed** (`task.spawn(skipNow, ...)`, the same pattern HatchAll already uses). `hatch()` and the free skip path are untouched.
10. **`loaded[player] = true` is now set before `TradeRecoveryHook`,** and DataLoaded still comes after it, so recovery can save through the queue (Task 6 needs this; tested). A player who leaves during the hook gets a release leave-save of fully loaded attributes.
11. **BindToClose writes a "close" release for every loaded player and doesn't clear `loaded`.** A leave-save after a failed close write still retries the release. After a landed release it's refused quietly.
12. **The soft-restart save is a normal write, not a release,** so if the teleport fails the player keeps saving.
13. **The 60 s inbox check is folded into the autosave.** If gifts were delivered (which saves them), the extra autosave write is skipped.
14. **Log kinds changed for the test log:** a normal leave-save is now kind `"leave"` (was `"save"`), and BindToClose is `"close"`. AutoReconnectTests only checks sealed leaves, which are unchanged.
15. **The test harness holds off the idle Studio client's Auto Reconnect.** `AutoReconnectTest = true` gives a 25 s idle limit, and in the first run it sealed the save mid-suite. The suite uses `AutoReconnectDebug "joinAge"` plus the client's `AutoReconnectFakeInput` switch, and opens the gate again for the AutoReconnect suite.

## Concerns
1. **Rollout window (owner should Migrate to Latest Update).** While old-version servers still run, an old server's blind leave-save that lands after a new server's takeover strips the lock fields. The new server's next write is then refused, and that player is kicked once with "You joined from another server". Their progress is in that leave-save, so they lose only the seconds spent in the new server. Old servers' `AddGiftedPass` also still writes saves directly. Shutting old servers down at publish ends both.
2. **More DataStore calls:** every join is now an UpdateAsync (read + write budget) instead of a GetAsync, plus one uncached GetAsync of the gift inbox per online player per minute. That's well inside the per-server budget (60 + 10 per player per minute).
3. **A hung `TradeRecoveryHook` keeps running after the 10 s cap** while the load goes on. TradeServer (Task 5/6) must cope with finishing after DataLoaded.
4. **Remaining gift double-grant window:** a crash between the inbox write and the `GiftReceipts` record, with the buyer's save also lost, means the retry finds no record and the buyer gets the pass too. It's tiny and the same class as before.
5. **Inbox entries of unknown kinds are never acked.** They're left for future code; harmless.
6. **Pre-existing, unchanged (owner decision):** paid SkipHatch / GrowAll return true when nothing was granted. Also pre-existing: ShopServer clears `pendingGift` before delivery, so a failed delivery's retry falls back to the buyer.
7. **Studio-only additions** (never exist live): PlayerDataDebug ops `lock`, `reacquire`, `pollInbox`, `reload` (and `forceUnseal` now re-takes a released or lost save); the `ServerStorage.AdminSaveBeforeLobby` hook; and a `dbg.reloading` branch in `load` (dbg is nil live).

## Studio state left / clean-up for the controller
- `workspace.TestFreshSave = true` (left on as instructed). `AutoReconnectTest` is back to unset (it was nil before). `SaveLockTestNoKick` was never set in Edit; tests set it only inside Play.
- Play sessions: all four that I started are stopped. No leftover instances (`SaveLockTestReport` and `TradeRecoveryHook` existed only in Play).
- Test keys made by this task, all throwaway:
  - `PlayerData_v3`: `studiotest_1793308120_1809064431` (RED run), `studiotest_1793308802_1809064431`, `studiotest_1793308976_1809064431`, `studiotest_1793309201_1809064431`.
  - `GiftInbox_v1_Studio`: `studiotest_<same tags>_1809064431` and `studiotest_<same tags>_-98765` (mostly emptied lists).
  - `GiftReceipts_v1_Studio`: `p_slt_*` and `p_pd_*` records.

---

# Fix round 1 (review: Critical 1, Important 2 + 3, 3 minors)

Status: DONE. pure 80/0, live 95/0. The seal and the write queue are untouched, so the Auto Reconnect suite wasn't re-run (it was 79/0 in the last full run). This round replaces concerns 4 and 6 above: gifts are now recorded before delivery, and pendingGift is kept until delivery.

## What changed
| Script | Change |
|---|---|
| `ServerScriptService.ShopServer` | **Critical 1:** the gift receipt (L264) now writes `GiftReceipts {target, key, pid}` FIRST (`SaveLock.recordGift`, L286), then delivers to the STORED target (`giveGift` -> AddGiftedPass, idempotent). A retry with no pendingGift reads the record; if one exists it delivers again to `rec.target`, then acknowledges. If the record can't be written or read, the receipt is NotProcessedYet and pendingGift is kept; pendingGift is cleared only after a successful delivery. The buyer fallback runs only when NO record exists, which now means nothing was ever delivered. **Important 2:** `pendingGift[buyer] = {[giftProductId] = {key, target}}` (L198), and a second gift prompt is refused while one is paying (`"Other gift pending"`, L356). `PromptProductPurchaseFinished` with `isPurchased = false` frees it (L206). Studio-only `ServerStorage.ShopGiftDebug` (L416): fault points `record` / `beforeDeliver` / `afterDeliver`, setPending / pending / clearPending, a prompt stub, `buy`, `finished`. |
| `ServerScriptService.PlayerData` | **Important 3:** `AddGiftedPass` (L403) returns false when both the in-server save and the inbox write failed, so the receipt stays NotProcessedYet. **Minor:** the in-server path writes the purchase id into the target's `ReceiptIds` in the same synchronous step as `GiftedPasses` (L413), like an inbox delivery. AddGiftedPass no longer writes the record; the receipt does that first. |
| `ServerScriptService.SaveLock` | `recordGift` returns `true, storedRecord` (the first record wins) and stores the full `pid`. `giftRecord` / `recordGift` return false on a pid mismatch (never guess). **Critical 1:** `addGift` reads the inbox back (uncached) when every try errored, so a landed write counts as delivered; false now only means "unknown", which is NotProcessedYet. **Minor:** `backoff` is a local, and `setBackoff` / `useStores` exist only in Studio. **New, found by the live run:** DataStore keys are max 50 characters, so a purchase id longer than 48 characters gets a fixed-length key (`h_<2 x FNV-1a>_<len>`, `receiptKey`, L321) instead of failing every call with KeyNameLimit. |
| `ServerScriptService.AdminServer` | **Minor:** `saveBeforeLobby` returns `saved, want`, and `sendToLobby` warns "soft restart: saved X of Y players before the teleport" when it falls short (L200). |
| `ServerStorage.SaveLockTests` | New pure checks: setBackoff/useStores seams, no public backoff field, recordGift returns the stored record, an erroring recordGift is not ok, addGift read-back, ids of 64 characters, and the fake store enforcing the 50-char key limit. New live sections `gift_faults` and `gift_pending`. Updated `gift_absent_player` (AddGiftedPass doesn't record) and `gift_retry_no_pending` (a record = delivered again to its target). Test purchase ids are now ~32-char ids like Roblox's (the old ones were 50+ characters with the `p_` prefix). |

Backups: no new scripts were touched. All the edited scripts already had their Task 0 copies in `ServerStorage._Backup_Trading.Before`.

## About "between delivery and the record"
With record-first, our code can never deliver before the record exists, so that cut point no longer exists. `gift_faults` cuts the receipt at every point that can happen now, then retries in the buyer's "next server" (pendingGift cleared):
- `record`: the record write fails. Nothing is recorded or delivered and pendingGift is kept; the retry in the same server delivers.
- `beforeDeliver`: the record landed, then the server "dies". The retry with no pendingGift reads the record and delivers to the friend.
- `afterDeliver`: delivered, then the server "dies" before the buyer's id and save. The retry delivers again (the inbox dedupes) and acknowledges.

Each case checks: the retry is PurchaseGranted, the target's inbox holds exactly one entry for that purchase id, the buyer has neither the pass in GiftedPasses nor its Pass_ attribute, pendingGift is cleared, and a third call is only acknowledged.

"No yield between grant and id": a gift's grant lands in the TARGET's data together with its purchase id (the inbox entry carries it; the in-server path now also writes it into the target's ReceiptIds in the same step). The buyer's save holds no grant, so recording the buyer's id after the handler's yields can't leave any save with a grant but no id. Every retry is idempotent through the record.

## Commands and outputs
RED, Edit, `require(game.ServerStorage.SaveLockTests:Clone()).pure()` (tests written before the fix):
```
SaveLock pure: 71 pass / 5 fail
FAIL Studio-only test seams exist (setBackoff, useStores)
FAIL no public backoff field to overwrite
FAIL recordGift returns the STORED record (a retry delivers to the first target)
FAIL recordGift on a new id returns its own record
FAIL addGift errored after landing: read back -> true
```
RED, Play (TestFreshSave true + AutoReconnectTest true, checked in Edit), Server, `require(SS.SaveLockTests).live(p, {only = {gift_absent_player, gift_retry_no_pending, gift_faults, gift_pending}})`:
```
SaveLock live: 11 pass / 4 fail
FAIL absent: AddGiftedPass only delivers (the receipt writes the record, first)
FAIL gift retry with a record: delivered to the record's target [0]
FAIL ShopGiftDebug hook exists
FAIL ShopGiftDebug hook exists
```
First GREEN attempt, live (`start(p, {verbose = true, skip = {seal_still_works = true}})`): 81 pass / 14 fail. Every failure was in `gift_faults` / `gift_pending`, and the console showed `DataStoreService: KeyNameLimit: Key name exceeds the 50 character limit. API: UpdateAsync, Data Store: GiftReceipts_v1_Studio`. My test ids (`slt_cutbeforeDeliver_<GUID>`) went past 50 characters, and a fault that was never reached leaked into `gift_pending`'s receipt B. The fix was the hashed key for long ids in SaveLock, the 50-char limit in the fake store, Roblox-shaped test ids, and a fault reset after each cut.

GREEN, Edit, pure:
```
SaveLock pure: 80 pass / 0 fail
long key: h_6926aec5a42283ef_64 (21)
```
GREEN, Play, Server, `require(game.ServerStorage.SaveLockTests).start(p, {verbose = true, skip = {seal_still_works = true}})`, then reading `ServerStorage.SaveLockTestReport`:
```
SaveLock live: 95 pass / 0 fail
... (all earlier sections ok, plus:)
ok   cut at record: NotProcessedYet / no record, nothing delivered, pendingGift kept / the retry -> PurchaseGranted / the target has it exactly once [1] / never the buyer / pendingGift cleared after the delivery / a third call only acknowledges
ok   cut at beforeDeliver: NotProcessedYet / the record was written first / the retry -> PurchaseGranted / the target has it exactly once [1] / never the buyer / pendingGift cleared / a third call only acknowledges
ok   cut at afterDeliver: NotProcessedYet / the record was written first / the retry -> PurchaseGranted / the target has it exactly once [1] / never the buyer / pendingGift cleared / a third call only acknowledges
ok   first gift -> prompted / a second gift while one is paying -> refused [false/Other gift pending] / the first gift's pending entry is untouched / a cancelled prompt frees it / then another gift can start
ok   receipt B -> granted / receipt A -> granted / each gift reached the friend with its own pass / the buyer got neither
ok   soft restart saves everyone first (<= 10 s) [1 saved in 0.5 s]
ok   the hook can save (SavePlayerNow inside it) [true]
```
The console showed only the deliberate test messages (the simulated takeover's "another server took their save over", the hook that errors, the hook that hangs).

## Notes / concerns
- **New player-facing text:** "Other gift pending" is returned by Shop.Buy for a second gift while one is paying. It shows wherever the Shop already shows its gift errors; there's no UI change.
- **What a stuck gift costs:** a gift whose prompt was bought but whose receipt keeps failing blocks that buyer's next gift until it's processed or they leave (PlayerRemoving clears it). A prompt closed without buying frees it at once. If Roblox ever reports `isPurchased = false` for a purchase that went through, its receipt finds no pendingGift and no record, and the buyer gets the pass. That's still one grant for one payment.
- **Hashed receipt keys:** a hashed-key clash (64-bit FNV, only for ids over 48 characters) returns false (NotProcessedYet) instead of guessing.
- **Studio state:** `workspace.TestFreshSave = true` (left on); `AutoReconnectTest` back to unset; `TestGiftSelf` unset (the test sets and restores it inside Play). Both Play sessions I started this round are stopped.
- **More test keys** (all throwaway): `PlayerData_v3` `studiotest_1793310437_1809064431` and `studiotest_1793310663_1809064431` (plus the RED session's key); their `GiftInbox_v1_Studio` keys; `GiftReceipts_v1_Studio` `p_t*` records.

---

# Fix round 2 (re-review: a cross-purchase pendingGift clash, 2 minors)

Status: DONE. pure 87/0, live 115/0 (the Auto Reconnect suite is skipped again: the seal and the queue are untouched).

## What changed
| Script | Change |
|---|---|
| `ServerScriptService.PlayerData` | New saved FIELD `GiftUnresolved = "{}"` (L85): JSON `{["<giftProductId>"] = target userId (0 = unknown)}` for this buyer's gift receipts left NotProcessedYet. |
| `ServerScriptService.ShopServer` | **Saved marker:** `unresolved / markUnresolved / clearUnresolved` (L215-L235). Every NotProcessedYet from a gift receipt sets the marker for that product, with the target if known (the first known target stays), and saves the buyer at once (SavePlayerNow). A receipt that resolves that product clears it in the same synchronous step as the purchase id Receipts adds next, so the clear is saved with it. **Refusal:** a new gift of a pass whose product is unresolved is refused with the existing `"Other gift pending"` (L401). **Receipt order (L295):** (1) this purchase's own record is read FIRST; a retry that finds it delivers to `rec.target` and never touches pendingGift. (2) With no record, the target is chosen in this order: the saved marker's target, else this server's pending entry for the product (used only when it matches the marker's target), else the buyer fallback. (3) A pending entry is used only by first turning it into this purchase's GiftReceipts record (L325), and only then removed, and only if it's still the entry that was read. **Minor 3:** the gift prompt is pcalled (L414); if it throws, the pending entry is cleared and the player gets `"Try again"`. The Studio debug `stubPrompt "error"` makes the stub throw. |
| `ServerScriptService.SaveLock` | **Minor 2:** `addGift`'s callback (L265) builds a new list instead of inserting into `old`. All the other callbacks (load, write, read-back, ack, record) already built new tables. |
| `ServerStorage.SaveLockTests` | The fake store has a `sharedRuns` mode: both callback runs get the SAME table, so a callback that edits its input shows up. New pure section `callbacks_pure` (load / write / release / addGift x2 / ack / record under sharedRuns). `gift_faults` now also checks that the marker is set and saved with the friend, then cleared once resolved. `gift_pending` checks that a throwing prompt leaves nothing pending. New live section `gift_cross` covers the reviewer's scenario (below). |

Not changed, as instructed (ledgered): the AddGift ReceiptIds handling for non-set gift kinds, and the pre-existing "no pend, no record, buyer already owns the pass -> NotProcessedYet forever" case. That case deliberately does NOT set the marker, which would otherwise block that pass's gifts for good.

## The cross-purchase test (`gift_cross`)
1. Gift A1 to F1 (-98765) has its record write cut, so it's NotProcessedYet. The marker `{A: F1}` is in the buyer's STORED save.
2. The buyer "leaves and rejoins": pendingGift is cleared, then `PlayerDataDebug "reload"` loads them from the save, and the marker comes back.
3. A new gift of pass A (`Shop.Buy` handler) is refused with `"Other gift pending"`, and nothing is left pending.
4. A newer entry A -> F2 (-98766) is forced in as the worst case. A1's retry is PurchaseGranted: A1 reached F1, never F2, F2's entry is untouched, and the marker is cleared.
5. A2's receipt is PurchaseGranted and reaches F2. The buyer got neither pass.

## Commands and outputs
RED, Edit, `require(game.ServerStorage.SaveLockTests:Clone()).pure()` (tests first):
```
SaveLock pure: 85 pass / 2 fail
FAIL pure callbacks: a second addGift lands
FAIL pure callbacks: ackGifts
```
(the second `addGift` saw its own first run's insert into `old` and wrote nothing)

RED, Play (TestFreshSave true + AutoReconnectTest true, checked in Edit), Server, `start(p, {only = {gift_faults, gift_pending, gift_cross}})`:
```
SaveLock live: 39 pass / 13 fail
FAIL cut at record: unresolved marker set + saved, with the friend
FAIL cut at beforeDeliver: unresolved marker set + saved, with the friend
FAIL cut at afterDeliver: unresolved marker set + saved, with the friend
FAIL a prompt that throws: refused, nothing pending [true/prompted]
FAIL cross: A1 unresolved in the buyer's SAVED data
FAIL cross: reload from the save
FAIL cross: a new gift of that pass is refused meanwhile [true/prompted]
FAIL cross: nothing pending after the refusal
FAIL cross: A1 reached F1
FAIL cross: A1 never reached F2
FAIL cross: F2's entry untouched by A1's retry
FAIL cross: A2 reached F2
FAIL cross: the buyer got neither
```
That's the reported bug reproduced: A1's retry took F2's entry, and A2 ended up with the buyer.

GREEN, Edit, pure:
```
SaveLock pure: 87 pass / 0 fail
```
GREEN, Play, Server, `require(game.ServerStorage.SaveLockTests).start(p, {verbose = true, skip = {seal_still_works = true}})`:
```
SaveLock live: 115 pass / 0 fail
ok   cut at record / beforeDeliver / afterDeliver: NotProcessedYet; unresolved marker set + saved, with the friend [{"3716713251":-98765}]; ...; the target has it exactly once [1]; never the buyer; pendingGift cleared; marker cleared once resolved; a third call only acknowledges
ok   a prompt that throws: refused, nothing pending [false/Try again]
ok   cross: A1 left for retry
ok   cross: A1 unresolved in the buyer's SAVED data
ok   cross: reload from the save
ok   cross: a new gift of that pass is refused meanwhile [false/Other gift pending]
ok   cross: nothing pending after the refusal
ok   cross: A1's retry -> PurchaseGranted
ok   cross: A1 reached F1
ok   cross: A1 never reached F2
ok   cross: F2's entry untouched by A1's retry
ok   cross: A1 resolved (marker cleared)
ok   cross: A2 -> PurchaseGranted
ok   cross: A2 reached F2
ok   cross: the buyer got neither
(+ every earlier section ok: load, versioned saves, receipts atomic incl. SkipHatch, lost save, leave release, inbox, absent gifts, record retries, soft restart, recovery hook)
```
The console showed only the deliberate test messages: the simulated takeover, "gift prompt failed: studio test: the prompt failed", the hook that errors, and the hook that hangs.

## Notes / residual risk
- **Remaining gap (no marker):** the marker is only set when the gift HANDLER returns NotProcessedYet. A receipt held back before the handler runs leaves no marker. That happens when Receipts refuses it because the buyer is still loading, is sealed for Auto Reconnect, or isn't in the server. In those states nothing can be saved for the buyer anyway (a sealed save takes no more writes; an unloaded buyer has no save to write). In that case the old behaviour stands: if the buyer starts a new gift of the SAME pass in their next server before Roblox retries the old receipt, the old receipt could take the new gift's target. That needs a receipt held back during a load or a teleport AND a new gift of the same pass within seconds of rejoining. No double grant is possible.
- **Marker storage:** the marker is cleared only through a resolving receipt. A marker can't get stuck from abandoned prompts, because it's set only from a real receipt that Roblox keeps retrying.
- **Studio state:** `workspace.TestFreshSave = true` (left on); `AutoReconnectTest` back to unset; `TestGiftSelf` unset. Both Play sessions I started this round are stopped.
- **More test keys** (all throwaway): `PlayerData_v3` `studiotest_1793311434_1809064431` and `studiotest_1793311557_1809064431`; `GiftInbox_v1_Studio` keys for -98765 / -98766 under those tags; `GiftReceipts_v1_Studio` `p_t*` records.

---

# Fix round 3 (controller's ruling: ONE saved gift intent per buyer)

Status: DONE. pure 88/0, live 135/0 (the Auto Reconnect suite is skipped: the seal and the queue are untouched). This round replaces round 2's per-product `GiftUnresolved` markers and the per-server `pendingGift`; both are gone from the code.

## What changed
| Script | Change |
|---|---|
| `ServerScriptService.PlayerData` | FIELD `GiftUnresolved` removed and `GiftIntent = ""` added (L86): JSON `{id, product, target, key, at}`. On load, an intent older than 24 h (or unreadable) is cleared (`GIFT_INTENT_TTL`, L26; the check is at L264), in the same synchronous step as the other fields, before DataLoaded. |
| `ServerScriptService.ShopServer` | The `pendingGift` table, the per-product markers and their helpers are removed. New helpers `intentOf / setIntent / saveNow / dropIntent` (L201-L233). **Starting a gift (L378-L410):** if the buyer already has an intent (any gift product), they get "Other gift pending"; an intent older than 24 h is dropped here too. Otherwise the intent is set and the buyer is SAVED (version-checked SavePlayerNow). Only if that save succeeds is the prompt opened (pcalled); a failed save or a throwing prompt clears the intent and returns "Try again". **Cancelled prompt (L235):** `PromptProductPurchaseFinished(isPurchased = false)` for the intent's product clears it (and saves that). **Gift receipt (L292):** (1) if this purchase has a GiftReceipts record, deliver again to its target (idempotent), then acknowledge; (2) else, if the buyer's intent is for this product, write the record from it (target, key, and the intent id, L307), deliver, then clear the intent in the same synchronous step as the grant + purchase id; (3) else (no record, no intent: only receipts from before this change) the old fallback. Every failure is NotProcessedYet, and the intent stays in the save. A record clears the current intent only if the record was made from that intent (`rec.intent == intent.id`, L316), so a late retry of an older purchase never clears a newer intent. `PlayerRemoving` no longer touches gifts (the intent stays in the save on purpose). The Studio `ShopGiftDebug` ops are now `setIntent` (saved, optional `at`) / `intent` / `clearIntent` instead of the pending ops. |
| `ServerScriptService.SaveLock` | `recordGift(purchaseId, target, key, intentId)` (L334) stores the intent id in the record. |
| `ServerStorage.SaveLockTests` | Gift sections rewritten for intents: `gift_faults`, `gift_pending` (concurrent + cancel + a throwing prompt + a failed intent save), `gift_cross`. New `gift_held`, `gift_expiry`, `gift_stuck`. Pure check: the record keeps its intent id. `live_load` checks that `GiftIntent == ""` and that `GiftUnresolved` is gone. |

## How it closes the three findings
- **(a)** A1's record and its intent are separate: the intent stays until A1 *resolves*. So no other gift, of ANY pass, can start while A1 is unresolved, and A2 can never meet A1's leftovers. A retry of A1 always follows A1's own record.
- **(b)** Nothing per-product can block forever any more. The pre-existing "no record, no intent, buyer owns the pass -> NotProcessedYet" receipt sets no intent, so the buyer can still gift (`gift_stuck`). An intent that never resolves expires after 24 h.
- **The receipt held before the handler:** the intent is in the SAVE before the prompt opens, so the next server's fresh load brings it back. The held receipt then reaches the intent's friend, never the buyer (`gift_held`, with a real reload from the save).

## Commands and outputs
RED, Edit, `require(game.ServerStorage.SaveLockTests:Clone()).pure()` (tests first):
```
SaveLock pure: 87 pass / 1 fail
FAIL recordGift keeps the intent id it was made from
```
RED, Play (TestFreshSave true + AutoReconnectTest true, checked in Edit), Server, `start(p, {only = {live_load, gift_faults, gift_pending, gift_cross, gift_held, gift_expiry, gift_stuck}})`:
```
SaveLock live: 42 pass / 35 fail
FAIL live_load: new FIELDS with their defaults
FAIL cut at record: the intent is in the saved data
FAIL cut at record: the intent stays for the retry
FAIL cut at record: the target has it exactly once
FAIL cut at record: never the buyer
FAIL cut at beforeDeliver: the intent is in the saved data / the record was written from the intent / the intent stays for the retry / the retry -> PurchaseGranted / the target has it exactly once / never the buyer / a third call only acknowledges
FAIL cut at afterDeliver: (the same 7)
FAIL its intent: this product + target
FAIL its intent was SAVED before the prompt
FAIL the intent's save fails: refused, no intent [true/prompted]
FAIL cross: A1's record says F1 / no new gift (any pass) while A1 is unresolved / A1 reached F1 once / A2 -> PurchaseGranted / A2 reached F2, not F1 / A2's intent cleared / the newer intent is untouched / the buyer got nothing
FAIL held: the saved intent came back
FAIL held: it reached the intent's friend
FAIL held: never the buyer
FAIL expiry: a 1 h old intent stays
FAIL expiry: an expired intent doesn't block a new gift [false/Other gift pending]
```
(`held: never the buyer` failing is the reviewer's point: on the old code, a receipt held before the handler gave the BUYER the friend's pass)

GREEN, Edit, pure:
```
SaveLock pure: 88 pass / 0 fail
```
GREEN, Play, Server, `require(game.ServerStorage.SaveLockTests).start(p, {verbose = true, skip = {seal_still_works = true}})`:
```
SaveLock live: 135 pass / 0 fail
ok   live_load: ... new FIELDS with their defaults (GiftIntent "", no GiftUnresolved)
ok   cut at record / beforeDeliver / afterDeliver: the intent is in the saved data; NotProcessedYet; (no record, nothing delivered | the record was written from the intent); the intent stays for the retry; the retry -> PurchaseGranted; the target has it exactly once; never the buyer; intent cleared once resolved (and saved so); a third call only acknowledges
ok   first gift -> prompted; its intent: this product + target; its intent was SAVED before the prompt; a gift of another pass meanwhile -> refused [false/Other gift pending]; the same pass again -> refused; another product's closed prompt leaves the intent; a cancelled prompt clears the intent (and saves that); then another gift can start; a prompt that throws: refused, no intent [false/Try again]; the intent's save fails: refused, no intent [false/Try again]
ok   cross: A1 recorded, delivery cut -> NotProcessedYet; A1's record says F1; A1's intent stays; no new gift (any pass) while A1 is unresolved; A1's retry -> PurchaseGranted; A1 reached F1 once; A1 resolved, intent cleared; A2 -> PurchaseGranted; A2 reached F2, not F1; A2's intent cleared; the older purchase's retry -> PurchaseGranted; it reached ITS record's friend (F1), not the intent's; the newer intent is untouched; the buyer got nothing
ok   held: NotProcessedYet before the handler ran; no record yet; the next server loads the save fresh; the saved intent came back; the retry -> PurchaseGranted; it reached the intent's friend; never the buyer; intent cleared
ok   expiry: reload; a 25 h old intent is cleared on load; a 1 h old intent stays; an expired intent doesn't block a new gift [true/prompted]
ok   stuck: NotProcessedYet (pre-existing); it leaves no intent; the buyer can still gift [true/prompted]
(+ every other section ok: versioned load/saves, receipts atomic incl. SkipHatch, lost save, leave release, inbox, absent gifts, record retries, soft restart, recovery hook)
```
The console showed only the deliberate test messages: the simulated takeover, "gift prompt failed: studio test", the `failNext` "save failed ... error", the hook that errors, and the hook that hangs.

## Notes / residual risk
- **Remaining "buyer gets it" cases (one grant per payment, never a double):** the old fallback now only runs for a receipt with no record and no intent. That's a receipt from before this change, or one whose intent was cleared early: Roblox reporting `isPurchased = false` for a purchase that did go through, or the receipt only arriving more than 24 h after its intent was saved.
- **Gifting is now strictly one at a time per buyer, across sessions.** A bought gift whose receipt keeps failing blocks that buyer's next gift until it resolves, or for at most 24 h.
- **An intent counts only once it's saved.** The prompt opens only after the intent's version-checked save, so a DataStore outage at gift time means "Try again" and no purchase.
- **Studio state:** `workspace.TestFreshSave = true` (left on); `AutoReconnectTest` back to unset; `TestGiftSelf` unset. Both Play sessions I started this round are stopped.
- **More test keys** (all throwaway): `PlayerData_v3` `studiotest_1793312143_1809064431` and `studiotest_1793312283_1809064431`; `GiftInbox_v1_Studio` keys for -98765 / -98766 under those tags; `GiftReceipts_v1_Studio` `p_t*` records.

---

# Fix round 4 (controller's ruling: GiftIntent TTL 30 min, new refusal text)

Status: DONE_WITH_CONCERNS. pure 95/0, live 156/0 (the Auto Reconnect suite is skipped again because the seal and the queue are untouched). The concerns are below; there are no code gaps.

## What changed
| Script | Change |
|---|---|
| `ServerScriptService.SaveLock` | **The one constant:** `SaveLock.GIFT_INTENT_TTL = 30 * 60` (L373), plus `SaveLock.intentExpired(intent)` (L375): true when `os.time() - intent.at > TTL`, or when there's no intent / no readable `at`. All three places call this one helper, so the check is the same everywhere. It lives in SaveLock because SaveLock is the only module both PlayerData and ShopServer already require. |
| `ServerScriptService.PlayerData` | The local `GIFT_INTENT_TTL = 24 * 3600` (old L26) is removed. **On load** (L262-269): an unreadable intent, or one where `SaveLock.intentExpired(t)` is true, is cleared (L267). It's the same synchronous step as before. |
| `ServerScriptService.ShopServer` | The local `GIFT_INTENT_TTL` (old L201) is removed and the header comment updated (L196-200). **Gift receipt** (L299): an intent with `SaveLock.intentExpired(it)` is treated as no intent, so a receipt with no record takes the existing "no record, no intent" route. The comment at L283-286 is updated. The expired intent is only ignored there, not cleared (the next load or gift start drops it). **Gift start** (L381): `SaveLock.intentExpired(current)` replaces the inline 24 h check. **Refusal text** (L385): `"Your last gift is still processing - try again in a few minutes"` replaces `"Other gift pending"`. Unchanged: `purchased == false` still clears the intent, a record still clears only its own intent, and there are no new fields. |
| `ServerStorage.SaveLockTests` | New pure section `gift_intent_ttl` (L429): the TTL is 1800, `intentExpired` gives 31 min = expired, 29 min = not, no time / no intent = expired. A source check confirms PlayerData and ShopServer hold no TTL of their own and call `SaveLock.intentExpired` in 1 and 2 places. Live: `GIFT_BUSY` constant (L455), and `gift_pending` / `gift_cross` expect the new text (L748, L750, L800). `gift_expiry` (L851) now uses 30 min: a 31 min old intent is cleared on load and a 29 min one stays. Its old "an expired intent doesn't block a new gift" part moved to `gift_ttl_start`. New `gift_ttl_receipt` (L895), `gift_ttl_start` (L928), `gift_cancel_late` (L960). |

Backups: PlayerData and ShopServer already had their Task 0 copies in `ServerStorage._Backup_Trading.Before` (checked). SaveLock and SaveLockTests are new in Task 1, so they have no backup.

## The new live tests
- `gift_ttl_receipt`: (a) with a 29 min old intent the receipt goes to the intent's friend, not the buyer, and resolves the intent. (b) With a 31 min old intent the receipt is PurchaseGranted, the record is the buyer's with no intent id (the intent was ignored), the buyer gets the pass (the old fallback), the expired intent's friend gets nothing, and the expired intent is left as it was (ignored, not used up).
- `gift_ttl_start`: a 29 min old intent still refuses a new gift with the new text and stays as it was. A 31 min old intent doesn't block: the new gift is prompted, and its intent replaces the old one (new id, product B) and is saved.
- `gift_cancel_late` (the reviewer's case). Setup: intent for F1, then a cancel through the real `PromptProductPurchaseFinished` handler (intent cleared), then the same product started for F2, then an OLD receipt with no record. The Shop.Buy handler needs the friend in the server, so both gift starts use the debug `setIntent`, which does the handler's same set + save. Asserted: the old receipt is PurchaseGranted with **one grant total** `[F1 0 / F2 1 / buyer 0]`, recorded for **F2, the new friend**, and a retry of it only acknowledges (still one grant). Recorded but not asserted: F2's intent was **used up by the old receipt**. Extra, asserted as "never two": if F2's own prompt was also bought, that receipt then has no record and no intent, so it falls back to **the buyer** `[F1 0 / F2 0 / buyer 1]`. That's one grant per payment, but F2's purchase lands with the buyer and F1 gets nothing.

## Commands and outputs
RED, Edit, `require(game.ServerStorage.SaveLockTests:Clone()).pure()` (tests first):
```
SaveLock pure: 88 pass / 2 fail
FAIL gift intent TTL = 30 min (SaveLock.GIFT_INTENT_TTL)
FAIL SaveLock.intentExpired exists
```
RED, Play (TestFreshSave true + AutoReconnectTest true, checked in Edit right before Play; tag 1793313078), Server, `require(SS.SaveLockTests).start(nil, {verbose = true, only = {gift_pending, gift_cross, gift_expiry, gift_ttl_receipt, gift_ttl_start, gift_cancel_late}})`:
```
SaveLock live: 41 pass / 11 fail
FAIL a gift of another pass meanwhile -> refused [false/Other gift pending]
FAIL the same pass again -> refused [false/Other gift pending]
FAIL cross: no new gift (any pass) while A1 is unresolved [Other gift pending/Other gift pending]
FAIL expiry: a 31 min old intent is cleared on load
FAIL ttl receipt: the expired intent was ignored (recorded for the buyer, not from the intent) [-98765/ec3e9fe9-...]
FAIL ttl receipt: the fallback - the buyer got it
FAIL ttl receipt: never the expired intent's friend [1]
FAIL ttl receipt: the expired intent is only ignored (left for the load / the next gift start)
FAIL ttl start: a 29 min old intent still refuses a new gift [false/Other gift pending]
FAIL ttl start: a 31 min old intent doesn't block a new gift [false/Other gift pending]
FAIL ttl start: the new gift's intent replaced it, and is saved
ok   late: the old receipt = one grant total, never two [F1 0 / F2 1 / buyer 0]
ok   late: recorded for the one who got it [F2, the new friend]
ok   late: the new friend's own receipt after it: never two grants [PurchaseGranted: F1 0 / F2 0 / buyer 1]
```
`gift_cancel_late` tests behaviour that already existed, so it passed on the old code too. The 29 min control checks also passed.

GREEN, Edit, pure:
```
SaveLock pure: 95 pass / 0 fail
ok   gift intent TTL = 30 min (SaveLock.GIFT_INTENT_TTL) [1800]
ok   SaveLock.intentExpired exists
ok   intentExpired: 31 min old -> expired / 29 min old -> not expired / no time / no intent -> expired
ok   PlayerData: no TTL of its own; SaveLock.intentExpired in 1 place(s) [1]
ok   ShopServer: no TTL of its own; SaveLock.intentExpired in 2 place(s) [2]
```
(RED had 90 checks because the section stopped early when `intentExpired` was missing.)

GREEN, Play (switches checked again in Edit; tag 1793313223), Server, `require(game.ServerStorage.SaveLockTests).start(p, {verbose = true, skip = {seal_still_works = true}})`:
```
SaveLock live: 156 pass / 0 fail
ok   a gift of another pass meanwhile -> refused [false/Your last gift is still processing - try again in a few minutes]
ok   the same pass again -> refused [false/Your last gift is still processing - try again in a few minutes]
ok   cross: no new gift (any pass) while A1 is unresolved [Your last gift is still processing - .../...]
ok   expiry: reload / a 31 min old intent is cleared on load / a 29 min old intent stays
ok   ttl receipt: a 29 min old intent -> PurchaseGranted / it reached the intent's friend, not the buyer / resolved that intent
ok   ttl receipt: a 31 min old intent -> PurchaseGranted
ok   ttl receipt: the expired intent was ignored (recorded for the buyer, not from the intent) [1809064431/nil]
ok   ttl receipt: the fallback - the buyer got it / never the expired intent's friend [0] / the expired intent is only ignored
ok   ttl start: a 29 min old intent still refuses a new gift [false/Your last gift is still processing - try again in a few minutes]
ok   ttl start: ... and stays as it was / a 31 min old intent doesn't block a new gift [true/prompted] / the new gift's intent replaced it, and is saved
ok   late: the cancel cleared the first intent / the old receipt -> PurchaseGranted
ok   late: the old receipt = one grant total, never two [F1 0 / F2 1 / buyer 0]
ok   late: recorded for the one who got it [F2, the new friend]
ok   late: the new friend's intent after it [used up by the old receipt]
ok   late: a retry of the old receipt only acknowledges, still one grant [F1 0 / F2 1 / buyer 0]
ok   late: the new friend's own receipt after it: never two grants [PurchaseGranted: F1 0 / F2 0 / buyer 1]
(+ every other section ok: live_load, versioned saves, receipts atomic incl. SkipHatch, lost save, leave release, inbox, absent gifts, record retries, gift_faults, gift_pending, gift_cross, gift_held, gift_stuck, soft restart, recovery hook)
```
The console showed only the deliberate test messages: the simulated takeover, "gift prompt failed: studio test", the `failNext` "save failed ... error", the hook that errors, and the hook that hangs.

## Noticed / concerns
1. **The new text is long for where the client shows it.** `StarterPlayerScripts.ShopClientLegacy` L555 puts the refusal reason on the Gift button itself, upper-cased, for 1.5 s (`label.Text = string.upper(tostring(msg))`). The other reasons are button-sized ("Reconnecting - try soon"). A 62-character message will probably render tiny or be cut off on that button, especially on a phone. I made no UI change (owner rule: visible UI changes need the owner's OK). The controller should decide whether the client needs a toast or a shorter button text.
2. **The 30 min window also applies to the receipt.** A receipt that arrives more than 30 min after its intent was saved, with no record (for example held back while the buyer was mid-teleport, or loading, and only retried after they came back 30+ min later), now goes to the buyer, not the friend. Before, that window was 24 h. It's still one grant per payment, never a double.
3. **`gift_cancel_late` outcome, for the record:** a purchase Roblox wrongly reported as "not bought" is delivered to whoever the CURRENT intent for that product names (F2), and uses that intent up. F2's own purchase then falls back to the buyer, and F1 gets nothing. Each payment is exactly one grant. If the buyer had already owned the pass, F2's receipt would land in the pre-existing "no record, no intent, owns it -> NotProcessedYet" case (`gift_stuck`).
4. `intentExpired` reads `at` with `tonumber`, where PlayerData's old load check required a number type. That's the same for real data (`at` is always `os.time()` written by ShopServer).

## Studio state
- `workspace.TestFreshSave = true` (left on). `AutoReconnectTest` back to unset. `TestGiftSelf` and `SaveLockTestNoKick` unset. No leftovers in ServerStorage (`SaveLockTestReport`, `TradeRecoveryHook` and `ShopGiftDebug` exist only in Play).
- Play sessions: both that I started this round are stopped. Nothing saved or published.
- More test keys (all throwaway): `PlayerData_v3` `studiotest_1793313078_1809064431` (RED) and `studiotest_1793313223_1809064431` (GREEN); their `GiftInbox_v1_Studio` keys for -98765 / -98766; `GiftReceipts_v1_Studio` `p_t*` records.
