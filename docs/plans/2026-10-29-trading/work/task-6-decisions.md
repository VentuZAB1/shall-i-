# Task 6: controller decisions and carries (binding; the brief is the requirements, the spec is the authority)

These come from the reviews and rulings of Tasks 1-5. Each one is a requirement for part B.

## Order and atomicity
1. **Escrow entry (onEnterConfirm)** gets a session copy that may be stale. Inside the hook, RE-READ the session and
   check phase == confirm, the same round and the same ver BEFORE `take()`. Then:
   - `take()`;
   - the `TradeEscrow["<id>#<round>"]` entry (the item data, with sigs);
   - the queued SaveLock write;
   - then `TradeCore.setEscrowed(s, side, round, items, now)` in one UpdateAsync.
2. **setEscrowed can refuse AFTER take()** (for example "Trade timed out", or the round moved on). A refused setEscrowed,
   a failed take, or a save that returns `(false, "lost" | "error")` is a failed entry:
   - abort the round through the record (only-if-empty "aborted", act on the RETURNED record);
   - then settle back.
   - Never return items any other way.
3. **BACK / cancel order (rule 4):** the session moves first, then the "aborted" record. If a "committed" record is
   found instead, settle as committed. `onCancelInConfirm` may get a marker with no `round`: don't assume `s.round`.
4. **Commit:** THIS node moved the session to commit, so it writes the record:
   - `UpdateAsync` on `TradeLedger_v1` `t_<id>_<round>`, written only if empty, built with `TradeCore.record`;
   - act ONLY on the returned value;
   - after an error, read it back with a no-change UpdateAsync, never assume.
5. **Dead-committer rule:** 30 s from THIS node's first sight of commit (`commitSeenAt`, this node's own clock) with no
   record means write "aborted" only-if-empty, then act on the returned record. Whichever record lands decides.
6. **Settle is ONE synchronous step, with no yield** between the check and the writes:
   - check `SettledRounds` for `<id>#<round>`;
   - give (deliver the other side's items, or return your own);
   - delete the TradeEscrow entry;
   - add the round to SettledRounds;
   - add the History entry.
   - Only then the queued save.
   - `give` is NOT idempotent, so the SettledRounds gate is the ONLY thing stopping a replayed settle from duplicating
     items.
7. **Errors:** `give` refuses while the player isn't loaded or is Reconnecting, and BaseHatchery's TradeItems wrapper
   turns its own internal errors into nil / `{}`. Settle must tell an ERROR or refusal apart from success:
   - never treat false / nil / an error as done;
   - keep the escrow entry and retry later (the 30 s check, or the next load).
   - **BaseHatchery's TradeItems wrapper** (about L1337-1341, Task 3's code) currently turns its own internal errors
     into nil / `{}`. Change it (back up BaseHatchery first if `_Backup_Trading.Before` doesn't already hold it) so
     every op (count / describe / take / give) returns a distinguishable error (for example `nil, "error"`) that is
     warned once a minute. TradeNode routes it to `itemError`, still failing closed. Add a live-path test that injects
     a fault INSIDE the wrapper (not in a test wrapper) and sees it counted.

## Recovery (spec invariant 6)
8. **`recover(player)`** runs from `ServerStorage.TradeRecoveryHook`, synchronously, after PlayerData copied the save
   into the attributes and before DataLoaded. It can overrun its 10 s cap and keep running AFTER DataLoaded. So:
   - re-read the live attributes inside its synchronous settle step;
   - be idempotent (the SettledRounds gate);
   - a "return before load" happens ONLY from this hook.
9. **The 30 s check** runs for own players with escrow entries. Do it through `onSessionSeen`, debounced per trade, plus
   a cheap timer. `onSessionSeen` fires about every 2 s per trade, so it must stay cheap: no DataStore read unless a
   round is in commit or past 30 s.

## Leaving, teleports, shutdown, lost saves
10. **Auto Reconnect seal** (the existing AFK teleport script, which seals the save before teleporting): it must cancel
    the trade explicitly BEFORE its final save.
    - Expose `ServerStorage.TradeCancelFor` (a BindableFunction made by TradeServer) and call it from the seal path
      inside pcall.
    - Back up that script first (BUILDER_RULES).
    - In select/confirm it cancels. In commit it's refused: the record decides, and the escrow entry is already in the
      save, so the next server recovers it.
11. **PlayerRemoving / BindToClose:**
    - cancel in select/confirm ("left"), keep in commit;
    - returns started while leaving must never give to a player whose FINAL save has already gone out, unless another
      save follows;
    - otherwise leave the entry for recovery on the next load (the aborted record already exists, so recovery returns
      the items).
12. **SaveLost** (`ServerStorage.SaveLost`: another server took over the save) means:
    - this node must never give to that player again;
    - cancel the trade through the record (select/confirm: cancel + aborted record; commit: the record decides).
    - The new server's recovery settles the escrow entry from the save.
    - This is what `takeover_mid_trade` tests.

## Data and clients
13. **TradeHistory** holds no job ids, sigs or other players' private ids. Only:
    - the other player's name and userId;
    - the display fields of the items given and received;
    - the outcome and the time.
    - Cap it as the spec says.
    - `OPS.history` returns it as-is, so what you write IS what the client sees.
14. **Done screen:** add the Push kind for a finished trade (completed, with the items received / cancelled, with the
    reason) and DOCUMENT it in the report next to Task 5's Push schema. Task 7 builds the Done screen on it.

## Clocks and budget
15. **Clocks:**
    - `now = workspace:GetServerTimeNow()` (the injected clock) for every trade rule;
    - `localSeenAt` / `commitSeenAt` = THIS node's first sight;
    - always pass the required clocks: `setEscrowed(s, side, round, items, now)`, `toCommit(s, now, localSeenAt)`,
      `cancel(s, why, now)`, `finish(s, outcome, now)`.
16. **The `budget` test** prints MemoryStore / DataStore / MessagingService calls per trade and per minute per server,
    including:
    - BACK / re-confirm loops (about 5 DataStore writes per 5 s up to the 10-min cap);
    - the presence list rebuild (1 unit per online player, at most 6/min per server with the list open);
    - the bus sends.
    - Compare them against the limits: MessagingService 150 + 60 x players per minute; DataStore writes 60 + 10 x players
      per minute; MemoryStore 1000 + 100 x players per minute.
    - Put the numbers in the report: the controller copies them into the ledger.

## Scope
- Part A's rulings stand. Don't reopen I2, M1, M2, M7 or M8 (see the ledger).
- The part A stand-ins (`standInEscrow`, `finishRound(s, "aborted")` for both-accepted) are REPLACED by the real paths.
- Each crash test drops a node (stops it without its leave handlers), reloads the players through recovery, and ends
  with the conservation check: the item multiset across both players before == after, and no item twice.
