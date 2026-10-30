# Task 6 report: `TradeServer` part B (escrow, commit, record, settle, recovery)

**Status: DONE_WITH_CONCERNS.**

Final runs on the final code:

| Suite | Result |
|---|---|
| TradeSimTests.partB | 16 pass / 0 fail |
| TradeSimTests.crash | 4 pass / 0 fail |
| TradeSimTests.exploit | 10 pass / 0 fail |
| TradeSimTests.budget | 4 pass / 0 fail |
| TradeSimTests.partA (re-run) | 28 pass / 0 fail |
| TradeItemsTests | 15 pass / 0 fail |
| SaveLockTests live | 158 pass / 0 fail |
| AutoReconnectTests.server | 79 pass / 0 fail |
| AutoReconnectTests.unit (Edit) | 83 pass / 0 fail |

The SaveLockTests live run includes `seal_still_works` (the AutoReconnect server suite) and `recovery_hook`.

The mutation spot check was caught 6/6. The concerns are a DataStore budget limit under heavy BACK looping, and the session size against the MemoryStore memory quota. Neither is a hole in the item rules.

Builder: Opus, 2026-10-30. Studio `3bf21205-caff-490e-a927-3bd9f0097311`.
- I started and stopped every Play session myself, and checked `TestFreshSave == true` in Edit right before each one.
  TestFreshSave is left `true`. `AutoReconnectTest` is back to unset.
- I never saved or published. There are no leftovers in ServerStorage (`_T6_GoodTradeNode` and `_T6_ARReport` were deleted).
- Stores: only `_Studio` ones. The ledger is `TradeLedger_v1_Studio`; the harness asserts the suffix before it runs.

## Scripts created or changed
| Path | Class | Size now | Backup | What changed |
|---|---|---|---|---|
| `ServerScriptService.TradeNode` | ModuleScript (own) | 109,078 chars (was 72,749) | none: own script | the part B section, the real hooks, Done push, why-codes, OVER_TTL, `checkEscrows` in the poll, SaveLost, shutdown, sealCancel, `kill` |
| `ServerScriptService.TradeServer` | Script (own) | 4,369 chars, 101 lines | none: own script | `TradeRecoveryHook` -> `node:recover`; new `ServerStorage.TradeCancelFor`; `BindToClose` -> `node:shutdown(Studio 3 s / live 20 s)`; Studio-only `ServerStorage.TradeServerDebug` ("pause" / "resume" / "stats") |
| `ServerStorage.TradeSimTests` | ModuleScript (own) | 138,509 chars | none: own script | `.partB` / `.crash` / `.exploit` / `.budget`, the part B harness, and the part A test edits listed under Rulings |
| `ServerScriptService.BaseHatchery` | Script | 65,128 chars | `ServerStorage._Backup_Trading.Before.BaseHatchery` (from Task 0) | only the TradeItems wrapper (decision 7), described below |
| `ServerScriptService.AutoReconnectServer` | Script | 14,885 chars | `ServerStorage._Backup_Trading.Before.AutoReconnectServer` | `reconnect()`: `TradeCancelFor:Invoke(player)` in pcall, right after `Reconnecting = true` and BEFORE `SealForReconnect` (the final save) |
| `ServerStorage.SaveLockTests` | ModuleScript | 64,387 chars (was 63,818) | `ServerStorage._Backup_Trading.Before.SaveLockTests` (made in this task) | test-only fixes for two stale spots: see "AutoReconnect / SaveLock regression" |

- `ServerScriptService.PlayerData` is unchanged. Task 1's hook call is used as it is.
- No script has a CollectionService tag.
- These are made at runtime by TradeServer and don't exist in Edit: `TradeCancelFor`, `TradeServerDebug`, and Task 5's `TradeRecoveryHook` and `ReplicatedStorage.Trade`.

**BaseHatchery TradeItems wrapper:**
- Each op (count / describe / take / give) runs in `pcall`.
- An internal error returns `nil, "error"` and warns at most once per 60 s. It is never `nil` / `{}` dressed up as an answer.
- An unknown op returns `false, "Unknown op"`.
- Studio only: `Invoke("_fault", op, player?)` makes that op's next call (for that player) error INSIDE the wrapper. This is the live-path test seam.
- TradeNode's `itemsCall` sends a thrown error or `nil, "error"` to `itemError` (counted, fails closed).

**To run the suites:** Play, Server datamodel, in a TestFreshSave session.
- They take minutes, so run each one in a thread, the same way as Task 5:
  `task.spawn(function() workspace:SetAttribute("_TradeSim", require(game.ServerStorage.TradeSimTests).partB(game.Players:GetPlayers()[1], true)) end)`
- The same works for `.crash(p, verbose, only)`, `.exploit(p, verbose, only)` and `.budget(p, verbose)`.
- The harness pauses the default node (`TradeServerDebug "pause"`) and resumes it at teardown.

## What each hook does now
`TradeNode.defaultHooks` (`partAHooks` is the same table, kept for Task 5's tests):

| Hook | Calls | What it does |
|---|---|---|
| `onEnterConfirm(s, side)` | `node:enterEscrow(s, side)` | On the player's OWN node. It first runs the checks:<br>- loaded, not leaving or lost or sealed;<br>- no older open escrow entry (it waits up to ENTRY_WAIT 8 s for one to settle);<br>- then a RE-READ of the session: phase confirm, the same round, the same ver, this side not secured yet.<br>Then, in one synchronous step: `take()` plus the `TradeEscrow["<id>#<round>"]` entry (the item data with sigs). Then the queued SaveLock write. Only then `TradeCore.setEscrowed(s, side, round, items, now)` in one conditional UpdateAsync.<br>Any failure (take refused or errored, save `false, "lost" \| "error"`, setEscrowed refused) is a failed entry: `failEntry` -> `abortRound` (the session first, then the only-if-empty "aborted" record), then settle from the RETURNED record. |
| `onBothAccepted(s)` | `node:commitRound(s)` | The node that moved the session to commit writes the record, `TradeLedger_v1_Studio` `t_<id>_<round>`, written only if empty, from `TradeCore.record` (`committedRecord`).<br>If the escrow lists are incomplete, it writes "aborted" instead.<br>After an error it reads back with a no-change UpdateAsync. It retries every RECORD_RETRY 2 s; after RECORD_GIVE_UP 60 s it switches to "aborted" (single-write: whatever landed decides).<br>Then `finishRound` with the RETURNED state, and each player on this node settles. |
| `onCancelInConfirm(s, why)` | `node:roundEnded(s, why)` | BACK, cancel, timeout or a failed entry, after the session moved. It works from the entry keys, not `s.round` (a marker may have no round).<br>It writes "aborted" only-if-empty and acts on the returned record. If "committed" is found, it settles as committed. |
| `onSessionSeen(s, side)` | `node:sessionSeen(s, side)` | Debounced per trade. It sets `commitSeen` (this node's first sight of commit) and runs `considerPlayer`.<br>It makes no store call for a live confirm under 30 s. |
| `recover(player)` | `node:recoverPlayer(player)` | From `ServerStorage.TradeRecoveryHook`: synchronous, after the attributes, before DataLoaded. Every entry's record is read; an empty one becomes "aborted". Each one settles:<br>- a RETURN may run before DataLoaded (only here);<br>- a DELIVERY waits for DataLoaded, then the entry check.<br>It also clears `lostSave[player]`, since this is a fresh load. |
| (poll) | `node:checkEscrows()` | The cheap timer for the 30 s check, for every own player with entries. It runs every POLL s, with a per-player backoff from 2 s up to 30 s on the trade clock. |
| `SaveLost` | `node:saveLost(p)` | `lostSave[p] = true`: this node never gives to them again.<br>- select/confirm: cancel plus an "aborted" record;<br>- commit: the record decides.<br>The new server's recovery settles the entry from the save. |
| `TradeCancelFor` | `node:sealCancel(p)` | Auto Reconnect, before its final save.<br>- select/confirm: cancels. It waits up to SEAL_WAIT 8 s for returns to settle; settling is allowed while Reconnecting, for this path only and only before the final save.<br>- commit: refused (the entry is already in the save, so the next server recovers it). |
| `BindToClose` | `node:shutdown(maxWait)` | Phase 1/2 trades cancel ("left"); commit is left to its record.<br>It never gives to a player whose final save has gone out (`leaving`). Their entry stays in the save for recovery on the next load. |
| `PlayerRemoving` | (part A `cancelFor` + part B guards) | It cancels in select/confirm and keeps the trade in commit. `leaving[p]` blocks any later give. A re-join clears `leaving` (onJoin). |

**Settle (`settleStep`, one synchronous step, no yield):**
1. Re-read the live attributes.
2. The SettledRounds gate (`SaveLock.hasId(settled, key)`): if the round is already settled, drop a stale entry and skip.
3. Give: the other side's items for "committed", your own back for "aborted". A false, nil or error from give changes nothing, and the entry waits.
4. Delete the TradeEscrow entry.
5. Add `<id>#<round>` to SettledRounds.
6. Add the History line (completed trades only).
7. Then the queued save, and then the Done push.

**Never give to a player:**
- whose save this node lost (`lostSave`);
- who is leaving;
- who is Reconnecting (outside sealCancel);
- or before DataLoaded, except a return run from the recovery hook.

## Recovery / entry-check decision table, as built (`verdict` in `considerEntry`)
First, if a record already exists for the entry (cached or read), it settles at once, whatever the session says. `finishIfCommit` also moves a session still in commit on to done/cancel.

Otherwise:

| Situation | Verdict | Store calls |
|---|---|---|
| Called from recovery (`how = "recovery"`, the load hook) | abort | "aborted" written only-if-empty, act on the returned record |
| The session is missing, or in phase cancel | abort | only-if-empty "aborted" |
| Session round < entry round (a stale read) | leave | none |
| Session round > entry round (the round moved on) | abort | only-if-empty "aborted" |
| Commit, and THIS node is writing the record (`committing`) | leave | none |
| Commit, < 30 s since THIS node first saw it (`commitSeen`) | read | one no-change read; settle if a record exists |
| Commit, >= 30 s since this node first saw it (the dead-committer rule) | abort | only-if-empty "aborted"; whichever record landed decides |
| Done | read | read, then settle |
| Live confirm on the same round, < 30 s since the entry was first seen (`entrySeen`) | leave | none |
| Live confirm on the same round, >= 30 s | read | at most one read per 30 s |
| Anything else (select, an expired or timed-out confirm) | abort | only-if-empty "aborted" |

"abort" never means "the items come back regardless": it is a write into an EMPTY key, and the node acts only on what the store returns. A "committed" record found there is delivered. A read error is never treated as "no record".

## Done Push (`Push "done"`) for Task 7
This sits next to Task 5's Push schema (`trade`, `request`, `requestGone`, `outgoing`, `outgoingGone`, `toast`).
```
Push("done", {
  id       = tradeId,
  outcome  = "completed" | "cancelled",
  why      = text,                       -- "Trade complete!" | the cancel reason (whyText)
  with     = {name = otherName, uid = otherUserId},
  gave     = {card...},                  -- what you gave (completed)
  got      = {card...},                  -- what you received (completed)
  returned = {card...},                  -- your items that came back (cancelled after escrow)
  late     = true?,                      -- it came from recovery / a later check, not the live trade
})
card (display only, no ids or sigs):
  pet = {t = "pet", name, display, kg, mut?, ps}
  egg = {t = "egg", kind, display, kg, mut?}
```
- **completed:** sent when THAT player's delivery settles; `why = "Trade complete!"`.
- **cancelled:** sent at `endLocal` when none of their items are in escrow, else when their items have come back (`returned` filled in).
- **BACK** sends no Done push. The trade goes on to round 2, and the `trade` view shows it.
- Each player gets their own push from their own node, once per trade. `doneSent` dedups it, capped at CACHE_MAX 2000.

**TradeHistory entry** (decision 13; `OPS.history` returns it as-is):
- `{name, uid, gave = {card...}, got = {card...}, outcome = "completed", at = os.time()}`.
- Newest first, capped at `TradeConfig.HISTORY_MAX` (20).
- It has no job ids, sigs, item ids or other players' private ids.

**New why-codes** (whyText, for toasts and Done):

| Code | Text for you | Text about the other player |
|---|---|---|
| `item:<side>` | "One of your items is no longer available" | "@B's item is no longer available" |
| `save:` | "Your items couldn't be saved" | "@B's items couldn't be saved" |
| `escrow:` | "Your last trade is still finishing" | |
| `lost:` | "You joined from another server" | "@B left the game" |
| `aborted` | "The trade couldn't finish - your items are back" | |

## Budget (`TradeSimTests.budget`, final run)
```
TradeSim budget: 4 pass / 0 fail
ok   BACK loop of ONE pair stays under the DataStore limit of a 6-player server [70 < 120]
ok   a normal trade costs <= 8 DataStore calls [8]
ok   a normal trade costs <= 40 MessagingService sends [16]
ok   a normal trade's session calls stay <= 80 (both servers) [33]
per cross-node trade (2 items a side, start to finish, both servers): MemoryStore 39.0 (sessions 21.0 reads / 12.0 writes, presence 6.0), DataStore 8.0 (ledger 4.0, saves 4.0), MessagingService 16.0
per same-server trade: MemoryStore 19.0 (sessions 5.0 reads / 10.0 writes, presence 4.0), DataStore 7.0 (ledger 3.0, saves 4.0), MessagingService 0.0
per BACK / re-confirm cycle (both servers): MemoryStore 20.3 (sessions 13.3 reads / 7.0 writes, presence 0.0), DataStore 7.0 (ledger 3.0, saves 4.0), MessagingService 7.0
one ONLINE list rebuild: 1 MemoryStore calls (1 unit per online player)
the biggest session (9 + 9 pets with mutations, Phase 2, both escrow lists): 6443 bytes; MemoryStore memory = 64 KB + 1 KB x users game-wide; a finished session now lives 60 s (was 15 min)
BACK loop at full speed (one pair, both on one server, a cycle every 6 s): DataStore 70 / min (limit 120), MessagingService 70 / min (limit 510), MemoryStore 263 / min (this server's share 600)
three pairs looping on one 6-player server: DataStore 210 / min (limit 120)
steady MemoryStore per server per minute: 30 session reads per open trade (the 2 s poll), 9 presence refreshes (6 players), 3 busy-lock refreshes per trading pair, <= 6 list rebuilds x online players
```
Limits used for a 6-player server:
- MessagingService: 150 + 60 x 6 = 510 per minute.
- DataStore writes: 60 + 10 x 6 = 120 per minute.
- MemoryStore: 1000 + 100 x players per minute, game-wide; one server's share is about 600.

A normal trade is far under every limit. The one number over a limit is three pairs BACK-looping at full speed on one server: about 210 DataStore calls per minute against 120 (see Concerns). The RED budget run showed DataStore 0, because part A's stand-ins made no escrow.

## RED (the named tests written first, run against part A's stand-ins)
```
TradeSim partB: 0 pass / 15 fail
FAIL trade_completes_cross_node [P's entry: nil]
FAIL trade_completes_same_node [... "phase":"cancel" ... "why":"Trade cancelled, nothing was moved" ...]
FAIL both_accept_same_tick [record]
FAIL back_racing_commit [the record doesn't match: nil]
FAIL back_then_round2_commits [round 1 escrow]
FAIL escrow_fail_aborts_round [the round didn't end: ... "phase":"confirm" ...]
FAIL escrow_save_refused_aborts [(a) the round didn't end]
FAIL record_error_after_landing [errAfter: ... "why":"Trade cancelled, nothing was moved" ...]
FAIL dead_committer_finished [P's node never saw the commit]
FAIL check_30s_leaves_live_confirm [missing method 'checkEscrows']
FAIL check_30s_settles_existing_record [missing method 'checkEscrows']
FAIL takeover_mid_trade [P's saved data has no escrow entry]
FAIL item_wrapper_errors [no fault seam in the wrapper]
FAIL seal_cancels_before_final_save [AutoReconnectServer doesn't cancel the trade before its final save]
FAIL leave_and_shutdown [no aborted record]

TradeSim crash: 0 pass / 4 fail
FAIL crash_after_escrow [ServerStorage.TradeSimTests:2361: attempt to call missing method 'kill' of table]
FAIL crash_after_commit_phase [node C didn't crash at the commit]
FAIL crash_after_record [node C didn't crash after the record]
FAIL crash_before_settle [node C didn't crash at the settle]

TradeSim exploit: 3 pass / 7 fail
(every trade-to-completion case closed "Trade cancelled, nothing was moved" through part A's stand-in;
 full_inventory_refused: "send: @SimPeerB is already trading")

TradeSim budget: 4 pass / 0 fail   (DataStore 0 per trade: there was no escrow yet)
```
- `stale_hook_takes_nothing` (partB #16, an extra beyond the brief's 15) was added during GREEN to pin the re-read-before-take rule against a stale Phase 2 copy. It fails against the mutation (below).
- All 10 exploit tests existed at RED: 3 passed and 7 failed.

## GREEN (final code)
```
TradeSim partB: 16 pass / 0 fail
ok   trade_completes_cross_node [65 asserts]
ok   trade_completes_same_node [32 asserts]
ok   both_accept_same_tick [40 asserts]
ok   back_racing_commit [83 asserts]
ok   back_then_round2_commits [78 asserts]
ok   escrow_fail_aborts_round [35 asserts]
ok   escrow_save_refused_aborts [70 asserts]
ok   record_error_after_landing [82 asserts]
ok   dead_committer_finished [46 asserts]
ok   check_30s_leaves_live_confirm [45 asserts]
ok   check_30s_settles_existing_record [40 asserts]
ok   takeover_mid_trade [45 asserts]
ok   item_wrapper_errors [53 asserts]
ok   seal_cancels_before_final_save [33 asserts]
ok   leave_and_shutdown [67 asserts]
ok   stale_hook_takes_nothing [38 asserts]
(node B lastError: one REAL MemoryStore "InternalError" on a session write - handled by the retry, the test passed)

TradeSim crash: 4 pass / 0 fail
ok   crash_after_escrow [34 asserts]
ok   crash_after_commit_phase [37 asserts]
ok   crash_after_record [37 asserts]
ok   crash_before_settle [38 asserts]

TradeSim exploit: 10 pass / 0 fail
ok   forged_refs [62 asserts]
ok   other_players_pet_id [47 asserts]
ok   same_pet_9x [53 asserts]
ok   fake_egg [33 asserts]
ok   early_ready_accept [44 asserts]
ok   old_ver [48 asserts]
ok   remote_spam [41 asserts]
ok   tenth_item [58 asserts]
ok   full_inventory_refused [347 asserts]
ok   away_target_refused [13 asserts]

TradeSim partA: 28 pass / 0 fail   (re-run at the end: all 28 ok, incl. ready_lock_resets / entry_recheck_aborts on the real paths)
TradeItemsTests: 15 pass / 0 fail
```
- Every test ends with the conservation check: the item multiset across both players is the same before and after, and no item appears twice.
- Each crash test:
  1. drops node C at its crash point (`escrowSaved`, `committed`, `recorded`, `settle`) with no leave handling (`kill`);
  2. reloads the players through recovery on node A or B;
  3. then checks conservation.
- The console showed only deliberate test output: the TradeItemsTests warning, simulated takeovers, injected faults, and the hook that errors or hangs.

## Mutation spot check (each gate switched off in a copy, then restored byte-identical)
| Mutation | Caught by |
|---|---|
| SettledRounds gate off (`if SaveLock.hasId(settled, key)` never true) | `FAIL back_then_round2_commits [a replayed settle gave sim_b1 again: 2]` |
| Re-read before take() replaced by `true, s` (the stale hook copy is trusted) | `FAIL stale_hook_takes_nothing [a stale Phase 2 copy took P's items]` |
| Only-if-empty record off (always write `want`) | `FAIL dead_committer_finished [the record changed: ...committed...]` and `FAIL check_30s_settles_existing_record [the record changed: ...]` |
| SaveLost check off (`lostSave[p]` dropped from canSettle's refusal line) | `FAIL takeover_mid_trade [the old server gave to P after losing the save]` and `FAIL escrow_save_refused_aborts [(b) node B gave to a player whose save it lost]` |

The restore check:
- `identical = true`, length 109,078, fnv `44397df4`;
- no planted line is left;
- the temporary `ServerStorage._T6_GoodTradeNode` is deleted.

## AutoReconnect / SaveLock regression (the seal path changed)
- **First full run:** `SaveLockTests.live`: **154 pass / 32 fail**. All 32 failures were in `seal_still_works` (AutoReconnect "request -> started") and `recovery_hook`. Both are stale-test problems, not regressions of the seal path:
  1. **`seal_still_works`:**
     - The gift sections (added in Task 1 after its last full run; its later runs skipped `seal_still_works`) leave the tester with `GiftAt` set by ShopServer.
     - AutoReconnect's `GIFT_HOLD` (120 s) then answers every request with `"wait", "gift"`.
     - I confirmed it: setting `GiftAt` gives `wait/gift`; clearing it gives `started`.
     - Run alone on the new seal path, `AutoReconnectTests.server` is 79/0.
  2. **`recovery_hook`:**
     - The test parents a SECOND `TradeRecoveryHook`. Since Task 5, TradeServer creates the real one, and PlayerData calls `FindFirstChild` (the first one), so the test's hook was never called (`[0]`).
- **Fix (test-only; SaveLockTests backed up first):**
  - `seal_still_works` clears the tester's `GiftAt` before the AutoReconnect suite.
  - `recovery_hook` sets the real hook aside (Parent nil) while its own stands in, and puts it back after. The body runs in pcall, so a failing check still restores it.
- **After the fix:** `SaveLock live: 158 pass / 0 fail`. `AutoReconnectTests.unit` in Edit: 83/0.

## Rulings (decided here, please confirm in review)
1. **The simulation's virtual players save to an in-memory fake store behind the REAL SaveLock** (compare-and-swap; every callback runs twice). The real tester's save (`PlayerData_v3` `studiotest_*`), the ledger (`TradeLedger_v1_Studio`) and the MemoryStore sessions are real `_Studio` services.
2. **`OVER_TTL = 60 s`** for a session that's over (done / cancel / poison marker), down from SESSION_TTL.
   - A full run hit `TotalMemoryOverLimit`: MemoryStore memory is 64 KB + 1 KB per user game-wide, and finished 6 KB sessions were crowding it.
   - Every node reads an end within POLL s, so 60 s is plenty.
   - This changes the TTL on part A's end writes (`cancelSession`, `finishRound`, `poison`).
3. **The 30 s check on a live confirm** reads (never writes) once the entry is 30 s old (decision 9's "past 30 s"), at most once per 30 s. Under 30 s there is no store call.
4. **The record carries `names`** (both display names), so a late Done push / History line can name the other player without a lookup. Nothing private is in it.
5. **History holds completed trades only.** Cancelled trades go to the Done push only.
6. **ENTRY_WAIT 8 s:** a Phase 2 entry waits for the player's older open escrow to settle. If it hasn't, the entry fails with `escrow:` ("Your last trade is still finishing").
7. **sealCancel may settle while Reconnecting**, only on that path and only before the final save. That is how returns land in the sealed final save.
8. **`leaving[p]` is cleared on join.** A re-join reuses the Player object only in the simulation, but the guard must not carry over.
9. **Extra Studio-only seams:**
   - `env.crashAt` (nil on a real server);
   - BaseHatchery `"_fault"` (`RunService:IsStudio()` only);
   - `TradeServerDebug` (Studio only).
10. **The `partAHooks` name is kept** as an alias of `defaultHooks`, so Task 5's references still work.
11. **Part A test edits** (TradeSimTests, own file). Part A's stand-ins are gone, so:
    - `ready_lock_resets` now expects "Trade complete!" and waits for settles before round 2;
    - `entry_recheck_aborts` waits for settles;
    - `expired_session_keeps_lock` quiets the bus during its check (a late coalesced ping correctly woke a node, which cancelled the expired session);
    - `H.do_` no longer retries `respond`, which isn't idempotent.
12. **SaveLockTests got 2 test-only fixes** (see the regression section above).

## Concerns
1. **DataStore budget under BACK looping:** 3 pairs looping at full speed on one 6-player server is about 210 DataStore calls per minute, against 120. One pair is 70.
   - A BACK cycle costs about 7 DataStore calls: 3 ledger plus 4 saves (the escrow save and the return save for each side).
   - Possible mitigations, all a Task 5/2 rules change, not mine to make: skip the post-settle save after a BACK return (the next autosave or escrow save carries it); or a longer READY lock after BACK, which keeps the 6 s cycle from repeating.
   - DataStore throttling only queues SaveLock writes. It never breaks the item rules, but heavy loops would delay other saves on that server.
2. **Session size against the MemoryStore memory quota:** the biggest session (9+9 pets with mutations, Phase 2) is 6,443 bytes, and the quota is 64 KB + 1 KB per user game-wide.
   - OVER_TTL helps.
   - Shrinking `escrowed` / sigs in the session would be a Task 2/5 change.
3. **After BACK, the items are out of the inventory for about 1 s** while they come back (the return settle and save). The UI should show them as "returning", not missing (Task 7).
4. **If `TradeRecoveryHook` isn't there when a player loads** (script start order on a fresh server), PlayerData waits HOOK_WAIT 10 s and then loads on. Recovery for that player then falls to the 30 s check (poll + `considerPlayer`), which still settles everything. It is only slower.
5. Two part A flake sources were fixed in the harness, not in the node: the bus-ping race and the `respond` retry. They were expected behaviour, not bugs.

---

# Fix round 1 (2026-10-30)

**Status: DONE_WITH_CONCERNS.**

Every finding (I-1, I-2, P1-P4, M-1-M-10) and both rulings (R-a, R-b) are in.

Every suite is green:

| Suite | Result |
|---|---|
| partB | 24 / 0 (16 + 8 new) |
| crash | 5 / 0 (+ `crash_after_unsaved_return`) |
| exploit | 10 / 0 |
| partA | 28 / 0 |
| budget | 5 / 0 |
| TradeItemsTests | 15 / 0 |
| SaveLockTests live | 158 / 0 |
| AutoReconnectTests.server | 79 / 0 |
| AutoReconnectTests.unit | 83 / 0 |

The mutation check: the 4 gates plus P1 and P4. Each mutant is caught, and both scripts were restored byte-identical.

The one concern left:
- The **cross-server** variant of the budget (6 players here, each looping with a partner on another server) peaks at about 72 DataStore calls in one minute.
- That is over the 60 bar but under the 120 limit.
- The ruled scenario (3 colluding pairs on one server) peaks at 54.

How the session ran:
- I started and stopped every Play session myself, with `TestFreshSave == true` checked in Edit before each one.
- TestFreshSave is left `true`, and `AutoReconnectTest` is back to unset.
- Nothing was saved or published. No `_T6_*` leftovers remain.

## Scripts changed in this round
| Path | Size now | Backup | Changes |
|---|---|---|---|
| `ServerScriptService.TradeNode` (own) | 118,304 chars, fnv `4e2bf5ff` | none (own script) | R-a, R-b, I-1, I-2, P3, P4 (+ movedTo), M-1, M-2, M-3, M-4, M-6 comment, M-7, M-8, M-10 comment, the record de-dupe |
| `ServerScriptService.BaseHatchery` | 67,478 chars, fnv `a2a9ac11` | `ServerStorage._Backup_Trading.Before.BaseHatchery` (already there) | P1 `writeAll`, P2 `checkSave`, M-10 comment, the `_faultMid` seam |
| `ReplicatedStorage.TradeConfig` | 4,979 chars | `ServerStorage._Backup_Trading.Before.TradeConfig` (already there) | `ENTRY_MAX = 6`, `ENTRY_WINDOW = 300` |
| `ServerStorage.TradeSimTests` (own) | 157,472 chars, fnv `ee3156e7` | none (own script) | 9 new tests, 4 changed tests, the `throwAt` seam, the budget scenario |

TradeServer, AutoReconnectServer, PlayerData and SaveLockTests are unchanged in this round. No new backups were needed.

## What changed, per item
- **R-a (an aborted return isn't saved by itself):**
  - `settle` saves only after a `"deliver"`. A `"return"` settles in memory only. The next escrow save, autosave, leave save or the seal's final save carries it.
  - Until then the stored save holds the entry plus the `"aborted"` record, and that recovers to exactly the same result.
  - Tests:
    - `back_then_round2_commits`: B's stored save still holds round 1's entry after BACK, and round 2's escrow save carries the return.
    - `takeover_mid_trade`: the new server's return isn't saved until its next save.
    - New crash test `crash_after_unsaved_return`: node C dies right after X's in-memory return (new crash point `"returned"`). X's stored save still has the entry, and X's reload returns the items exactly once.
- **R-b (at most 6 Phase 2 entries per player per 5 min):**
  - Counted in `entryLog[uid]` on the player's own node at each Phase 2 entry, including failed ones, deduped per round key.
  - `OPS.ready` refuses past the limit with `waitText(...)` ("Wait Ns"). A new trade doesn't reset the count. The poll prunes old entries.
  - New test `entry_limit_per_player`:
    - 6 BACK rounds, then both READYs (on their own nodes) answer "Wait";
    - a new trade still answers "Wait";
    - after the window, Phase 2 works again.
  - **Also for the budget:** `recordOnce` now runs one ledger call per round key at a time per node. A second asker waits for the first and reuses its result from the record cache, so a same-server pair pays for one record call per round, not two or three.
- **I-1:** `enterEscrow` builds and encodes the entry from a copy of the offer BEFORE `take()`, and fails the entry (nothing taken) if it can't be encoded. The give-back branch is gone.
  - After `take()`, the real items are encoded. If that ever failed (it can't: the same items), the probe's JSON is the entry.
  - No path gives back without checking the result.
  - There is no test: without a seam inside JSONEncode this is unreachable. It is covered by construction.
- **I-2:** `recoverPlayer` runs each entry in its own `pcall(recoverEntry, ...)` and clears `resolving[tag]` and `rerun[tag]` on every exit. An error is warned (throttled `oops`).
  - New test `recovery_error_retried`: the harness's `throwAt.settle` throws inside settle during recovery, then the next entry check settles the entry.
- **P1:** take and give write through `writeAll(p, set, op)`:
  - every string is encoded first, and the writes run inside `pcall`;
  - if a write throws, the strings already set are put back and the op errors, which the wrapper answers as `nil, "error"`.
  - The Studio seam `Invoke("_faultMid", "take" | "give", player)` throws right after the FIRST write.
  - New test `item_writes_all_or_nothing`:
    - (a) B's pet+egg take throws mid-way: both strings are unchanged and the round aborts;
    - (b) a delivery of a pet+egg to B throws mid-way: the entry stays and a later check delivers exactly once.
- **P2:** take and give only (`checkSave`): a non-empty `BaseData` / `PetInventory` / `EggInventory` string that doesn't decode to a table raises "a broken save", which comes back as `nil, "error"`, never as empty data.
  - `nil` and `""` still mean "nothing yet".
  - `readData` / `readPets` / `readInventory` for other systems are untouched.
  - New test `broken_save_refused`: 5 cases (give egg/pet/egg with each field broken, take with Pet/Egg broken). Each is refused and nothing changes, and an empty `""` EggInventory still takes a return.
- **P3:** `isSessionLive`:
  - `"over"` (done / cancel) is dead at once;
  - `"missing"` reads again after `C.POLL` s and counts as dead only if the second read is missing too.
  - Presence calls it outside UpdateAsync, so the wait is safe.
  - New test `missing_needs_two_reads`: a live session behind a forced nil read stays live and took at least POLL s; a GUID that's really gone is dead; a cancelled session is dead at once.
- **P4:** recovery (`recoverEntry`) reads the session. If it is a LIVE confirm for that entry's round, it cancels it first (conditional write, why `"lost:<side>"`, OVER_TTL, `applied` pings both sides), then writes `"aborted"` only-if-empty.
  - **Follow-on found by the GREEN run:**
    - `takeover_mid_trade` then failed: the OLD server learned of the cancel at once and returned the items in memory to its stale copy of P, before its own SaveLost arrived.
    - That had no effect on the stored data (the old server's saves are refused), but it breaks decision 12's intent.
    - Fix: the recovery cancel also writes `movedTo = <this jobId>`. Another node that sees a session over with `why == "lost:<its player's side>"` and `movedTo ~= its jobId` marks that player's `lostSave` (`handleSession`).
    - That can only ever stop a give: the entry stays in the stored save.
    - A same-server rejoin is excluded (`movedTo == jobId`).
  - New test `recovery_cancels_live_confirm`: X's old node dies in a live confirm, X reloads on node B, and the session is cancelled by the recovery. P's items come back without a 30 s or idle wait, P's trade ends, and both busy locks free.
  - `crash_after_escrow` was updated to the new order: no idle-timeout wait any more.
- **M-1:** `commitSeen` goes through `seeCommit` (capped at CACHE_MAX like `records`) and is pruned on settle.
- **M-2:**
  - What changed: the ENTRY_WAIT and sealCancel loops still watch the attribute every 0.25 s, but force the entry check at most every `RECORD_RETRY` (2 s).
  - New test `waits_are_paced`: with node A's ledger down, an 8.4 s seal wait made at most 24 record calls (the RED run made 48).
- **M-3:** past `RECORD_GIVE_UP`, `commitRound` waits `COMMIT_DEAD_AFTER` (30 s) between record attempts. There is no test: it needs 60+ s of real waiting.
- **M-4:**
  - What changed: `saveAfter` runs after a delivery. A save that fails with `"error"` is warned and retried 3 times, 2 / 4 / 8 s apart, while the player is still here and their save isn't lost. A `"lost"` save is never retried.
  - New test `delivery_save_retried`: B's save after its delivery errors once, and a retry lands within 12 s.
- **M-6:** a comment in `shutdown` explains why it's safe (accepted as is).
- **M-7:** `playerSaves().onLost` warns when `SaveLost` never shows up, and `start` warns (throttled) when it gets no connection.
- **M-8:** `considerPlayer` warns (throttled) on an unreadable `TradeEscrow`.
- **M-9:** the comment in `seal_cancels_before_final_save` says the source-order check is an extra guard and the behaviour asserts are the real test.
- **M-10:** comments at `settleStep` and at the top of BaseHatchery's `give`: give must never yield, and every step after its data write is a plain call.
- **M-5 (decision 9 kept):**
  - What changed: a timing assertion in `back_then_round2_commits`: a BACK on the OTHER node returns this node's player's items in under 5 s.
  - It passed in the RED run too, as a guard, not a fix.
- **H1:** deferred, as ruled.

## RED (the new and changed tests, run against the code before the fixes)
```
TradeSim partB: 0 pass / 11 fail
FAIL recovery_error_retried [the entry check never settled the entry (stuck)]
FAIL recovery_error_retried (reset) [escrow left open: SimCrash1 {"44fb986e-...#1":{...}}]
FAIL item_writes_all_or_nothing [no between-the-writes fault seam in the wrapper]
FAIL broken_save_refused [give with a broken EggInventory went through]
FAIL missing_needs_two_reads [one missing read counted a live session as dead]
FAIL recovery_cancels_live_confirm [recovery left the session in confirm]
FAIL entry_limit_per_player [ServerStorage.TradeSimTests:2720: invalid 'for' limit (number expected, got nil)]
FAIL delivery_save_retried [no retry save after the failed one: {"b25b9fd9-...#1":{...}}]
FAIL waits_are_paced [node A made 48 record calls in a 8.4 s seal wait]
FAIL back_then_round2_commits [R-a: B's return was saved by itself: []]
FAIL takeover_mid_trade [R-a: the new server saved the return by itself]

TradeSim crash: 0 pass / 2 fail
FAIL crash_after_unsaved_return [node C didn't crash at the return]
FAIL crash_after_escrow [P didn't settle by the record]

TradeSim budget: 3 pass / 1 fail
FAIL R-b: READY refused after ENTRY_MAX Phase 2 entries [8 rounds, then nil]
```
In the RED `back_then_round2_commits`, the M-5 assertion (before the R-a check) passed.

## GREEN (final code)
```
TradeSim partB: 24 pass / 0 fail
ok   trade_completes_cross_node [65 asserts]      ok   recovery_error_retried [31 asserts]
ok   trade_completes_same_node [32 asserts]       ok   item_writes_all_or_nothing [73 asserts]
ok   both_accept_same_tick [40 asserts]           ok   broken_save_refused [33 asserts]
ok   back_racing_commit [83 asserts]              ok   missing_needs_two_reads [31 asserts]
ok   back_then_round2_commits [82 asserts]        ok   recovery_cancels_live_confirm [36 asserts]
ok   escrow_fail_aborts_round [35 asserts]        ok   entry_limit_per_player [129 asserts]
ok   escrow_save_refused_aborts [70 asserts]      ok   delivery_save_retried [39 asserts]
ok   record_error_after_landing [82 asserts]      ok   waits_are_paced [29 asserts]
ok   dead_committer_finished [46 asserts]
ok   check_30s_leaves_live_confirm [45 asserts]
ok   check_30s_settles_existing_record [40 asserts]
ok   takeover_mid_trade [47 asserts]
ok   item_wrapper_errors [53 asserts]
ok   seal_cancels_before_final_save [33 asserts]
ok   leave_and_shutdown [67 asserts]
ok   stale_hook_takes_nothing [38 asserts]
TradeSim crash: 5 pass / 0 fail   (crash_after_escrow 34, crash_after_commit_phase 37, crash_after_record 37,
                                   crash_before_settle 38, crash_after_unsaved_return 35 asserts)
TradeSim exploit: 10 pass / 0 fail   (full_inventory_refused 347 asserts)
TradeSim partA: 28 pass / 0 fail
TradeItems: 15 pass / 0 fail
SaveLock live: 158 pass / 0 fail   (incl. seal_still_works = AutoReconnectTests.server, and recovery_hook)
AutoReconnectTests.server (alone): 79 pass / 0 fail
AutoReconnectTests.unit (Edit): 83 pass / 0 fail
```
The console showed only deliberate test output:
- the simulated takeover;
- the "studio test" gift, teleport and save faults;
- the hook that errors or hangs;
- TradeItemsTests' Index warning;
- the describe fault.

## Budget (final run)
```
TradeSim budget: 5 pass / 0 fail
ok   R-b: READY refused after ENTRY_MAX Phase 2 entries [6 rounds, then Wait 252s]
ok   R-b: 3 colluding pairs on one 6-player server stay <= 60 DataStore calls / min (the worst minute) [54]
ok   a normal trade costs <= 8 DataStore calls [8]
ok   a normal trade costs <= 40 MessagingService sends [16]
ok   a normal trade's session calls stay <= 80 (both servers) [33]
per cross-node trade (2 items a side, start to finish, both servers): MemoryStore 39.0 (sessions 21.0 reads / 12.0 writes, presence 6.0), DataStore 8.0 (ledger 4.0, saves 4.0), MessagingService 16.0
per same-server trade: MemoryStore 18.0 (sessions 4.0 reads / 10.0 writes, presence 4.0), DataStore 7.0 (ledger 3.0, saves 4.0), MessagingService 0.0
per BACK / re-confirm cycle (both servers): MemoryStore 20.7 (sessions 13.7 reads / 7.0 writes, presence 0.0), DataStore 4.0 (ledger 2.0, saves 2.0), MessagingService 7.0
one ONLINE list rebuild: 1 MemoryStore calls (1 unit per online player)
the biggest session (9 + 9 pets with mutations, Phase 2, both escrow lists): 6442 bytes
R-b, one colluding pair on one server, BACK + cancel/re-SEND alternating as fast as allowed: 6 Phase 2 rounds in 55 s of trade time, then READY said "Wait 252s"; DataStore 18 (ledger 6, saves 12) = 3.0 per round, MemoryStore 96, MessagingService 0
R-b, three such pairs on one 6-player server: DataStore 54 in the worst minute, 10.8 / min over the 300 s window (bar 60, limit 120)
(cross-server variant: 6 players here, each with a partner elsewhere, ENTRY_MAX rounds each in one minute: about 72 DataStore calls in that minute, 14.4 / min over the window, limit 120)
steady MemoryStore per server per minute: 30 session reads per open trade (the 2 s poll), 9 presence refreshes (6 players), 3 busy-lock refreshes per trading pair, <= 6 list rebuilds x online players
```
Compared with the first report:
- **BACK cycle (cross-node):** DataStore went from 7.0 to 4.0 per cycle (ledger 3 to 2, saves 4 to 2). R-a drops the return saves, and the record de-dupe drops a ledger call.
- **Same-server colluding pair:** 3.0 DataStore per round, 1 record + 2 escrow saves.
- **Three pairs on one server:**
  - before: 210 calls per minute, with no cap;
  - now: at most 54 in any minute and 10.8 per minute sustained.

## Mutation spot check (each mutant made in a copy of the source, then restored byte-identical)
| Group | Mutant | Caught by |
|---|---|---|
| 1 | SettledRounds gate off (`if false and SaveLock.hasId(settled, key)`) | `FAIL back_then_round2_commits [a replayed settle gave sim_b1 again: 2]` |
| 1 | Re-read before take() off (`local okR, cur = true, s`) | `FAIL stale_hook_takes_nothing [a stale Phase 2 copy took P's items]` |
| 2 | Only-if-empty off (`if want == nil then return nil end`) | `FAIL dead_committer_finished [the record changed: ..."state":"committed"...]` |
| 2 | SaveLost off (`lostSave[p]` dropped from canSettle) | `FAIL takeover_mid_trade [the old server gave to P after losing the save]`, `FAIL escrow_save_refused_aborts [(b) node B gave to a player whose save it lost]` |
| 3 | P1 restore off (writeAll keeps a half write) | `FAIL item_writes_all_or_nothing [(a) a half-written take: [PetInventory without sim_b1, EggInventory unchanged]]` |
| 3 | P4 cancel off (`if false and okS and full(s) ...`) | `FAIL recovery_cancels_live_confirm [recovery left the session in confirm]` |

The restore check:
- TradeNode is identical to the kept copy (118,304 chars, fnv `4e2bf5ff`), and so is BaseHatchery (67,478 chars, fnv `a2a9ac11`). Both match the builder's local copies.
- No "MUTANT" text is left.
- The temporary `ServerStorage._T6_Good_*` StringValues are deleted.

One note on the only-if-empty mutant:
- In the first round, `check_30s_settles_existing_record` also caught it. It no longer does.
- The reason is the new per-node record cache in `recordOnce`: the committer's node already holds the "aborted" record in memory, so it never sends the overwrite. That is a second defense, not a gap.
- `dead_committer_finished`, where the committer has no cached record, still catches the mutant.

## Rulings (new in this round, please confirm)
1. **movedTo (follow-on to P4):** the recovery cancel writes `movedTo = jobId`. Another server that sees `why == "lost:<its player's side>"` with a different `movedTo` marks that player's save as lost. It only ever blocks gives, and the stored entry stays for recovery.
2. **The record de-dupe in `recordOnce`:** one ledger call per round key per node at a time, and a cached record is reused. It is needed for the R-b budget, and it only ever reuses a record the store returned.
3. **R-b counts every Phase 2 entry, a failed one too** (the save or record work may already have happened), deduped per round key. The count lives in memory per node, so a server hop starts a fresh count. That is fine for a per-server budget.
4. **P2 refuses with an error (`nil, "error"`), not "Bad save".** The wrapper warns once a minute and TradeNode counts it as an item error. An entry that can't be returned waits in escrow and is never lost.
5. **M-4 retries 3 times (2 / 4 / 8 s), then leaves it to the next save.** The stored entry still recovers correctly if nothing lands.

## Concerns
1. **Cross-server peak:** 6 players on one server, each looping with a partner on ANOTHER server, cost this server about 72 DataStore calls in the worst minute (14.4 per minute sustained). That is under the 120 limit but over the 60 bar. The ruled scenario (3 local pairs) peaks at 54. A per-minute sub-cap (for example at most 3 entries per minute) would bring it to about 36. That is a rules change for the controller.
2. **P3:** a busy-lock check on a session that reads "missing" now waits POLL (2 s) before clearing it. A new trade blocked by a truly dead lock starts about 2 s later (rare).
3. **Not tested by a failing check:** I-1 (unreachable without a JSON seam), M-3 (needs 60+ s of real waiting), and M-1, M-6, M-7, M-8, M-10 (comments, warnings, caps). All were checked by reading.
