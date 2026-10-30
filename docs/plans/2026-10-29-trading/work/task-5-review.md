### Spec Compliance
- ISSUES FOUND (details in Important I1, I2, I4, I5 and Minor M1, M7):
  - The busy-lock clearing rule is broader than spec section 5 (I1).
  - Trade timing, backoff and the bus rate window use `os.clock()`, not the trade clock the controller required (I2).
  - Limiter-refused calls are not counted, against spec section 4 "Refused calls count against the limits too" (M1; the builder's ruling needs controller sign-off).
  - Bus payloads carry names and inventory counts, against "ids only" (M7).
  - The room and Phase 2 policy/room re-checks have no tests (I4).
- PASS: All 15 brief-named tests exist by name (`ServerStorage.TradeSimTests` 378-385), plus `request_same_node`, `query_ops`, `stale_read_ignored`. The RED and GREEN output is in the report. Not re-run, per the rules.
- PASS: The remote ops match brief and spec sections 3-4. Remotes act only for the real caller (`ServerScriptService.TradeNode` 1411-1413, 1421-1425). Each op validates types before the service calls (e.g. 1074-1076, 1222-1224, 1258-1262).
- PASS: PolicyService field verified in Studio before the build (`work/task-0-report.md` lines 48-53: `IsPaidItemTradingAllowed = true`).
- PASS: Every store and topic name comes from `C.stores()` with the `_Studio` suffix (`ReplicatedStorage.TradeConfig` 67-83). No hard-coded names in TradeNode or TradePresence.
- PASS: The session is written before `takeBusy` (`TradeNode` 1178-1183, then 1183). Both locks are taken lower-uid-first, both or none, with partial release (`TradePresence` 637-652). Releases are conditional (585-595, 626-633) and run when a trade ends (`endLocal` 757-760).
- PASS: Kill switch: `TradeConfig` 11, `TradeCore.newSession` 225, `TradeNode` 960, 1030, 1416, and the poll path 1530-1547.
- PASS: Limit values match the brief list (`TradeConfig` 17-58).
- PASS: `partA` asserts `TestFreshSave == true` before any Play work (`TradeSimTests` 1060). Stores are `_Studio` through `C.stores()`.
- UNVERIFIED: real-server behaviour of `os.clock()` (I2). `TradeItems` `describe` / `count` bodies (BaseHatchery 1024-1110 header only; Task 3 scope). Ownership rests on the Invoke wrapper passing the real Player (BaseHatchery 1335-1341). Whether the `Instance.new("BindableFunction")` fallback at BaseHatchery 1333 is parented (outside the lines read; the tests assert it exists in Play). Live cross-server behaviour beyond the Studio simulation and the one live message in the report.

### Strengths
- Every session change is one `UpdateAsync` whose pure callback applies a TradeCore function (`TradeNode` 616-643). TradeCore copies its input and never mutates it (`TradeCore` 251-277, 294-307). The READY and ACCEPT version checks sit inside the same write, so an offer change cannot slip between a READY and its check.
- No session reaches a client. Every OPS return path strips it (`done` 917-920; `OPS.cancel` 1331).
- Duplicate-trade guards are race-free within a node. The check and the record write have no yield between them (`ac` 1040-1042; `respond` 1140-1151). Locks are both-or-none, lower-uid-first, and conditional on the trade id.
- Stale copies are ignored by revision (`handleSession` 781-786), and a test covers the bug it guards (`stale_read_ignored`).
- The test harness runs the real TradeNode against the real `_Studio` MemoryStore with a JSON round-trip bus. The leak test checks the raw JSON of every push (`TradeSimTests` 420-427, 668-672).
- Client-supplied item refs are cleaned to whitelisted fields (`cleanRef` 262-279). Owned counts come from the server (`OPS.add` 1226-1231).

### Issues

#### Critical (must fix)
None found. No path lets a client act for another player, act on a trade it is not in, skip a phase, or change an offer after READY/ACCEPT without a reset. Part A moves no items, so no duplication path exists in this task.

#### Important (should fix)
**I1. A busy lock is cleared for an expired session that is still live.**
- `ServerScriptService.TradeNode` 1429-1435 (`isSessionLive`) returns `st == "live" or st == "commit"`. `stateOf` (313-321, line 319) returns `"expired"` for an idle or total timeout, so an expired session counts as dead.
- `TradePresence` 579-582 treats anything but `false` as live, so the expired session's lock is cleared (`takeOne` 620, `busyOf` 684).
- Spec section 5 (`docs/specs/2026-10-29-trading-design.md` line 197) clears a lock only when the session is "done, cancelled or missing". Expired is not in that list.
- Exposure is narrow. While the home node still holds the record, `ac` (1040) and `respond` (1140) refuse. It opens when the home node died or lost its record while the session stayed open. Another server can then take the lock and start a second trade for the same player while the expired session exists.
- Fix: count an expired session as live. The expiry cancel on either node (`handleSession` 809-813 to `cancelTrade`) ends it and releases the lock. If both nodes are gone, the session TTL frees the lock.

**I2. Trade timing uses `os.clock()`, against the controller decision.**
- The controller required every node to use `workspace:GetServerTimeNow()`. `os.clock()` is used for:
  - `TradeNode` 182, 185 (60 s PolicyService retry); 484-486 (2 s request ack wait); 499 (the 4/s per-trade bus window, the MessagingService guard); 572-574 (`CALL_WAIT`); 596 and 599 (MemoryStore backoff); 1574-1575 (leave retry); 1586-1588 (busy-lock refresh every 40 s); 1617-1619 (outbox cleanup); 434-435 (warn throttle).
  - `TradePresence` 121 (the default clock for its caches and lookup budget); 379-380, 409-411, 468-469 (waits).
- `os.clock()` is process CPU time in standard Lua (C `clock()`). Roblox game servers run on Linux. If it does not track wall time on a live server, the ack wait, the bus cap, the backoff and the refresh interval are all wrong.
- Verify on a live server: compare `os.clock()` deltas with `GetServerTimeNow()` deltas over 60 s, idle and under load.
- Fix: put the limiter, cooldown and bus-window timers on the injected node clock. Keep task-based waits only where the wall-clock behaviour is verified.

**I3. The per-player call queue runs before the limiter, a server-cost hole.**
- `node:handle` (`TradeNode` 1411-1419) calls `oneAtATime` (571-585) before any type check or limiter. A call that finds `calling[uid]` set loops on `task.wait()` every frame for up to `CALL_WAIT` = 10 s (573-576, `CALL_WAIT` at 76).
- The holder can be SEND or accept, which block up to 2 s (1092, 1156).
- The limiter (`allow` 530-550) and the type checks run only after that wait, inside each OPS.
- A client can stack thousands of waiting threads, each resumed every frame, and every refused call pays that cost. Service calls stay capped, so this is a server-cost hole rather than a duplication path.
- Fix: cap waiting calls per player (for example 2; more get "Slow down" at once), and reject bad types before queueing.

**I4. No test for the duplicate, over-count, 10th-item or room refusals through the remote path.**
- The named tests (`TradeSimTests` 378-385) don't cover these. `offer_sync_cross_node` (632-676) and `change_rate_limits` (778-829) use 1-3 items and never add a duplicate.
- The pure rules are covered in `ServerStorage.TradeCoreTests` (261-269, 276-279, 868).
- Not covered: the owner-count wiring (`items("count")` at `TradeNode` 1230-1231 feeding `addItem`); the READY room check (`overCap` 1273-1275, 289-309); and the Phase 2 entry room and policy re-check (`standInEscrow` 1482-1483). `policy_refused` covers accept only.
- Spec section 4 (lines 133-135) and section 6 row 345 depend on exactly these paths.
- Add tests: a 10th item via `add`; the same pet twice; an egg count over owned; READY refused when one side would pass 150 (virtual player counts); the Phase 2 entry abort for room and for policy.

**I5. Hook hazard for part B: `onEnterConfirm` gets a copy that may already be out of date.**
- `handleSession` (`TradeNode` 814-819) spawns `onEnterConfirm` with the copy read earlier (poll, bus or own write). By the time the hook runs, the other side may already have gone BACK, cancelled or timed out, so the session is in select or cancel.
- The stand-in is safe because `setEscrowed` re-checks phase and round inside its own `UpdateAsync` (`TradeCore` 327-338, lines 330-331; `TradeNode` 1485-1490).
- Part B's order (per the report's hook table: `take()`, then the TradeEscrow save, then `setEscrowed`) removes items before any conditional check.
- As written, the only thing that unwinds a stale take is the 30 s check (spec rule 6), which also blocks that player's new escrows meanwhile.
- Part B must re-read the session inside the hook and check phase, round and ver before `take()`. A refused `setEscrowed` must be treated as a failed entry that returns the taken items through the record.

#### Minor (nice to have)
- **M1.** Limiter-refused calls are not counted: `allow` returns before storing (`TradeNode` 529, 547-549). Spec line 148 says refused calls count. The effect stays bounded, so this is a ruling for the controller to accept or reverse.
- **M2.** Two nil reads a second apart end the local record (`handleSession` 787-797), and `endLocal` (757-760) then releases both locks even if the session is still live. MemoryStore reads should be consistent, so the risk is low. Release only on a session copy that shows over or missing.
- **M3.** A phantom session after a failed receiver write. `respond` 1182 calls `giveUp` (1157-1164). The write may have landed, since an error can be ambiguous. `poison` refuses a live session (646-652), so it stays. The sender's node then activates it (`handleSession` 800-821) with no receiver record and no locks, and the sender is blocked until the 3-minute idle timeout. Not actionable by the receiver, and no items move in part A. Fix: `giveUp` should cancel the session if it exists.
- **M4.** `refresh` has no `pcall` (841-865). An error in `handleSession` leaves `reading[id] = true` (846), so later refreshes only set "again" and this node stops polling that trade. Wrap the body and reset on every path.
- **M5.** The request cap check runs after the replace step (971-980). A refused "full" request still removes the sender's older pending request, and no `rg` tells that sender.
- **M6.** Reordered bus messages. `ac` before `ra` gets "gone" (1029, 1166-1170). A late `ra` then sets the sender to pending for up to 30 s on a request the receiver already dropped (1106-1107). A `rq` arriving after its `rx` leaves a stale pop-up (rx ignores unknown ids, 998-1004). `respond` also removes the pop-up and cancels the accepter's own outgoing (1143-1153) before the sender confirms (1166). UX, not security.
- **M7.** Bus payloads carry names and counts: `rq` `n` (1091); `ar` `cp`, `ce`, `j` (1045). Spec line 199 says ids only. Messages go to every server on the topic, not to clients. Decide or accept.
- **M8.** Cross-server stamps as lock floors. `lockReason` (`TradeCore` 60-65) and `lockLeft` (`TradeNode` 367-371, used at 724-726) take the later of `s.changedAt` / `s.confirmAt` (written by another server) and the local sighting. This only lengthens locks, which is safe, but the controller said never use another server's stamp. Countdowns can disagree with enforcement when clocks differ.
- **M9.** Kill-switch order differs from the report. `node:remote` checks the op list first (1421-1423). The kill switch sits in `handle` (1416), after the op lookup and before queueing. Valid ops refuse correctly; unknown ops answer "Bad request" while off. The report's "kill switch first" is not exact.
- **M10.** Swallowed errors that look like answers. `OPS.add` returns "You don't have that pet" when `describe` errors (1226-1228). A `count` error becomes `{}` (BaseHatchery 1337-1338). `income` returns $0/s on error (`TradeNode` 245-249). All fail closed, but they hide faults. Log them.
- **M11.** `limits[uid]` can be re-created by a call in flight after `onLeave` cleared it (1627; `allow` 530-535). Tiny: the `leaving` set blocks `here`, so only a stale table remains.
- **M12.** No test for the Reconnecting paths: `ownRules` 927 and the poll seal 1591-1593. The brief names the Reconnecting re-check. Add a test.
- **M13.** `TradeNode.new` is one function of about 1,300 lines (383-1690). `copy`, `finite`, `whole`, `validUid` and `isList` are duplicated across TradeNode, TradeCore, TradePresence and BaseHatchery. Split and share the helpers.
- **M14.** `onCancelInConfirm` can receive a marker with no `round` on the malformed-session path (`cancelSession` 874-876, then `cancelTrade` 887-888). Practically unreachable, but part B should not assume `s.round`.
- **M15.** Hand-offs for part B. `OPS.history` (1381-1389) returns the TradeHistory attribute as-is, so job ids and other players' pet ids must never be written there. The stand-in `standInEscrow` marks "secured" without checking that the items still exist (1485-1490). That is fine for part A and must be replaced by `take()` in part B.

### Assessment
**Task quality:** Needs fixes. **Reasoning:** No Critical hole was found: the state machine, the locks and the input checks hold up against the owner's exploit list. Five Important items remain: a lock-clearing rule broader than the spec (I1), trade timing on `os.clock()` against the controller decision (I2), a call queue that runs before the limiter (I3), no tests for the duplicate and room refusals (I4), and a stale-input hazard for part B's escrow hook (I5).
