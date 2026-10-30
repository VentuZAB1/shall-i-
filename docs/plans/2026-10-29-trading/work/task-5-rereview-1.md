# Task 5 re-review, fix round 1 (scoped)

Scope: only the listed findings (I1, I3, I4, M3, M4, M5, M10, M12) and whether a fix broke its neighbours. Out of scope and not flagged: I2, M1, M2, M7, M8, I5, M14, M15.
Read-only: `ServerScriptService.TradeNode` (1,759 lines), `ServerStorage.TradeSimTests` (1,418 lines). Also read `TradePresence`, `TradeCore`, `TradeConfig`, `BaseHatchery` (1335-1341) and the `TradePresenceTests` stubs. No test was re-run (REVIEWER_RULES). Test logic was checked by reading, plus the builder's mutation table.

## Findings

### I1 (expired session counted as dead): Fixed
- `ServerScriptService.TradeNode:1493-1501`: `isSessionLive` returns true for `expired`. Only done, cancelled or missing returns false. A read error still raises (line 1496).
- `ServerScriptService.TradePresence:579-582`: `isDead` clears a lock only when the call succeeds and returns `false`. Both the error path and the expired path keep the lock. `TradeNode:1754` wires the node's function into each presence instance.
- `ServerStorage.TradeSimTests:1085-1114` (`expired_session_keeps_lock`): calls the real `H.B.isSessionLive` and the real `H.presB.takeBusy`. Another trade is refused with "busy", and the normal expiry cancel then frees both locks. Not a mock.
- Note: the brief's one-line wording for I1 reads backwards ("counts an expired session as live"). The original review's bug is that expired was counted dead. The code now counts it live, as spec section 5 requires.
- Residual, by design (not a defect): if neither node is alive to cancel an expired trade, the lock ends at its TTL, 900 s after the last refresh (`TradeConfig:52`, `TradePresence` 612/664), not at once.

### I3 (queue ran before the limiter and type checks): Fixed
- `node:handle` (`TradeNode:1472-1483`): kill switch (1477), then `CHECK[op]` (1479-1480), then `oneAtATime` (1482).
- `CHECK` table (`TradeNode:1108-1151`): no yield and no service call. `limited` reaches `allow`, which only reads the clock. All 14 ops have a CHECK entry, and no OPS function calls `allow` any more.
- `oneAtATime` (`TradeNode:585-602`): the first waiter sets `waiting[uid]` (587-588). Any further call returns "Slow down" at once (586-587). `calling[uid]` is set at 594 and cleared at 596 after `pcall(fn)`. The pcall catches every error, so the flag clears on every path. A timed-out waiter clears `waiting` at 591, before its exit check at 592.
- No deadlock: each wait is bounded (CALL_WAIT at 589-590, REQUEST_ACK_WAIT inside SEND and respond). Nothing in the queue re-enters `handle`, and same-node bus messages use `task.defer`. The wait bounds use `os.clock`, which is I2 and out of scope.
- Test `call_queue_capped` (`TradeSimTests:1117-1137`): counts threads still alive after `task.spawn` (at most 2), at least 48 "Slow down", at most 2 service writes. The builder's mutation (waiter cap removed, 4 in flight) fails it.
- Note: a call that passes the limiter and is then refused by the queue has used its slot. The builder's semantics note matches spec section 4 ("refused calls count").

### I4 (no remote-path tests for the caps and room): Fixed
- 10th item: `offer_caps_refused` 1159-1161 expects "Max 9 items" (`TradeCore:259`, `TradeConfig:14`).
- Same pet twice: 1151-1152, "Already in offer" (`TradeCore:265`).
- Egg over owned: 1163-1168, "You don't have more of that egg" (`TradeCore:271`), with two owned.
- READY over 150: `ready_room_refused` 1175-1197. `OPS.ready` checks both sides (`TradeNode:1346`, `1348`). Virtual B holds 150.
- Phase 2 entry, room: `entry_recheck_aborts` 1200-1222, round aborts with `room:b` via `standInEscrow` (`TradeNode:1549`) and `abortRound` (1563). Policy: 1223-1233, `rules:b`.
- All go through `H.do_` into `handle`, so they use the real queue, CHECK and OPS.

### M3 (giveUp left a landed session open): Fixed
- `giveUp` (`TradeNode:1233-1240`) now calls `cancelSession` (897-909): it cancels a landed session, or writes the marker if none exists.
- Test `giveup_cancels_landed_session` (`TradeSimTests:1275-1296`): the write really lands and then errors (`T.slowMemory`, 133-135). The test checks the stored session reads back as cancel, A's record is gone, and no lock is held.
- Residual: the cancel is one attempt. If that write also errors, the open session stays until its 180 s idle expiry, with no retry. "Can no longer leave an open session" holds when the cancel lands.

### M4 (refresh had no pcall, reading[id] could stick): Fixed
- `refresh` (`TradeNode:876-892`) wraps `refreshOnce` in `pcall`. `reading[id]` is cleared at 891 on every exit, including the error break (887). Errors count into `stats.errors` and go through `oops`.
- Test `refresh_survives_error` (`TradeSimTests:1299-1314`): an error is injected through `H.boomIn` at a real `now()` call inside `handleSession` (161-173). `s` messages to B are dropped, so B must poll. The builder's mutation (no pcall) fails it.

### M5 (refused "full" request still replaced the sender's older one): Fixed
- `rq` (`TradeNode:997-1010`): the cap counts other senders' live requests first (1000-1003). A "full" refusal returns at 1003, before the replace loop (1004-1010).
- Test `full_keeps_older_request` (`TradeSimTests:1317-1341`): asserts no `requestGone` for A2's older request.

### M10 (silent item and income errors): Not fixed (live path)
- TradeNode side is fixed: `itemError` (`TradeNode:447-450`) counts and warns. `OPS.add` (1301-1308) and `income`/`card` (247-265; viewOf at 713, 721) route errors there. Test `item_errors_counted` (`TradeSimTests:1344-1356`).
- The live path is not covered. `TradeServer` uses the default `items`, which is `SS.TradeItems:Invoke` (`TradeNode:402-406`). `BaseHatchery:1335-1341` wraps `count` and `describe` in pcall and returns `{}` or `nil` on error (`ok and n or {}` at 1338, `ok and item or nil` at 1341). In play, TradeNode never sees those errors. A count or describe failure is still silent: it fails closed, but it is not logged.
- The test injects its error in its own `items` wrapper (`TradeSimTests:216-223`). It proves TradeNode's counting, not the live path.
- Needed: `BaseHatchery` (Task 3's file, which the builder left alone) must warn (throttled) or re-raise on those pcall failures and keep the fail-closed return. Alternatively, the controller rules the live path out of scope.

### M12 (no Reconnecting tests): Fixed
- `reconnecting_paths` (`TradeSimTests:1237-1272`) covers: the own-rule refusal on send (`OPS.send` via `ownRules`, `TradeNode:1158`, "Reconnecting..."); the other node's refusal on rq (`TradeNode:991`); the Phase 1 poll seal (`reconnect:b`, 1656-1659); the Phase 2 seal with `onCancelInConfirm` (1271).
- Not covered: the accept-time `ownRules` in `OPS.respond` (`TradeNode:1212`). It is the same function, so the risk is low.

## New issues from the fix round
None that break behaviour. Checked:
- Strict CHECK types (`respond` boolean, `ready`/`accept` whole ver of at least 1, `remove` 1..9, `chat`, `search`): no client caller in the place (a search for `"respond"` finds only the TradeServer header and the tests), so no live caller is refused by them.
- The limiter now runs first. The kill switch still refuses before CHECK (1477). The existing send_limits, change_rate_limits, chat_limits, query_ops, kill_switch_refuses and second_trade_refused expectations read as consistent with the new order.
- `TradePresenceTests` stubs `isSessionLive` (lines 351, 1087), so it is unaffected. `TradeCore` is unchanged this round.
- Housekeeping: the report says "No existing script changed, so no new backups", but its own "What changed" section edits `TradeNode` and `TradeSimTests`. The note should be corrected.

## Assessment
Seven of the eight listed findings are fixed. M10 is not fixed on the live path: the TradeNode side works, but `BaseHatchery:1337-1341` still swallows count and describe errors before TradeNode can see them.

**Verdict: Needs fixes**
