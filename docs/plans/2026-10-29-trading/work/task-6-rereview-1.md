# Task 6 re-review 1: TradeServer part B, fix round 1

Reviewer: Haiku 5.5 (fresh, scoped, read-only). Studio `3bf21205-caff-490e-a927-3bd9f0097311` read via `script_read` / `script_grep` only. No Play, no test re-runs. The builder's claims were checked against the code and the test bodies, not taken on trust.

Read: TradeNode (part B 1655-2691, plus the helpers it touches), BaseHatchery TradeItems (writeAll 1112, checkSave 1132, take 1204, give 1294, wrapper 1381-1411), TradeConfig (all), TradeSimTests (harness 1-340, part B tests 1833-2800, budget 3180-3316), TradePresence (busy locks 578-690, refresh 709-713), TradeCore (cancel 392, sideOf 243), PlayerData (snapshot 285-314).

---

### Item verdicts

- **R-a: Fixed.** `settle` saves only a delivery (TradeNode 1954). A `"return"` never calls `saveAfter`. The entry removal, the SettledRounds mark and the give run in one synchronous step (settleStep 1835-1876: encodes at 1857-1869, give at 1870, writes at 1872-1874). The PlayerData snapshot reads every FIELD in one loop (PlayerData 290-296), so no save can carry the mark without the removal. A stored aborted round always holds the entry plus the "aborted" record, which recovers to the same result. Saves are whole-record snapshots, so a later save carries the in-memory return and nothing combines into a second copy. Tests: back_then_round2_commits (TradeSimTests 2024-2029, 2039-2041), crash_after_unsaved_return (2536-2556), takeover_mid_trade (2264-2267).
- **R-b: Fixed.** Checked at `OPS.ready` on the player's own node (TradeNode 1518-1520) via `entryWait` / `logEntry` (563-573). Entries are logged in `enterEscrow` (2090), which runs synchronously from `applied` / `task.spawn`, so the count is not raced. Values are in TradeConfig 23-24 (ENTRY_MAX 6, ENTRY_WINDOW 300). A new trade does not reset it: `entryLog` is keyed by uid and is not cleared on leave. Test entry_limit_per_player (2715-2771). Budget: see N1 and N5.
- **I-1: Fixed (by reading).** `enterEscrow` builds and encodes the probe entry before `take` (2130-2133, take at 2134). The only give-back is settleStep's give (1870), and its result is checked (1871). See N4.
- **I-2: Fixed.** `recoverPlayer` runs each key in its own pcall (2306-2315), and clears `resolving` / `rerun` on every exit (2312). Test recovery_error_retried (2561-2574). Without the fix, the resolving guard in considerPlayer (2052-2053) would skip the entry for good, so the test has teeth.
- **P1: Fixed.** `writeAll` encodes first (callers 1281 and 1358), restores the names already set when a write throws (1115-1127), then errors. The wrapper answers nil, "error" (1400-1407). `_faultMid` is gated by STUDIO (1393-1397) and only arms take / give. Test item_writes_all_or_nothing (2578-2619). See N2.
- **P2: Fixed.** `checkSave` (1132-1143) runs first in take (1209) and give (1314) over BaseData, PetInventory and EggInventory. nil and "" pass. A refused op writes nothing. Test broken_save_refused (2623-2658): the five broken cases plus the "" case. See N3.
- **P3: Fixed.** `isSessionLive` (2420-2436): over is dead at once; missing needs a second read after `task.wait(C.POLL)` (2431); a read error raises, so the lock is kept. Both callers (TradePresence 620 and busyOf 684) are outside any UpdateAsync callback. Test missing_needs_two_reads (2662-2686). See N8.
- **P4: Fixed.** `recoverEntry` (2273-2292) reads the session. A live confirm of this round is cancelled first (conditional write 2280-2286; TradeCore.cancel refuses commit, TradeCore 395), then the aborted record is written (2290). `movedTo` is set only by that cancel (2284), inside a pure callback. The old node marks `lostSave` only when `why == "lost:<its side>"` and `movedTo ~= its jobId` (handleSession 992). That mark only blocks gives and entry-check actions (canSettle 1802, ownRules 1136, enterEscrow 2095). The entry stays in the stored save.
  - Abuse: a client never writes sessions. A player can only cancel their own trade, which BACK and cancel already allow. The mark lands only on the loading player's own side.
  - Legitimate settle: a committed round can't be cancelled (TradeCore 395). The owning server's recovery settles the entry. The other side ends through endLocal (940-945), which releases both busy locks.
  - Test recovery_cancels_live_confirm (2691-2713).
- **M-1: Fixed.** `seeCommit` is capped (537-548), and `commitSeen[key]` is cleared on settle (1946). See N6.
- **M-2: Fixed.** The ENTRY_WAIT loop (2102-2112) and sealCancel (2348-2351) force a check at most every RECORD_RETRY. Test waits_are_paced (2793-2807).
- **M-3: Fixed (by reading).** commitRound waits COMMIT_DEAD_AFTER between tries after RECORD_GIVE_UP (2182-2189). `committing[rk]` keeps this node's verdict at "leave" meanwhile (1980). The commit's own loop switches to aborted after 60 s, so there is no liveness hole.
- **M-4: Fixed.** `saveAfter` (1913-1930) retries a delivery's save 3 times (2 / 4 / 8 s) on "error", never on "lost", and stops if the player left or was lost. Test delivery_save_retried (2775-2789).
- **M-5: Fixed.** Timing assertion in back_then_round2_commits (2017-2020), real clock, under 5 s. Decision 9 is kept. The spec 6 vs decision 9 wording still needs the controller's ruling, which is outside this round's items.
- **M-7: Fixed.** `playerSaves().onLost` warns (TradeNode 282-285). `start` warns through `oops` when there is no connection (2634-2640).
- **M-8: Fixed.** considerPlayer warns, throttled, on an unreadable TradeEscrow (2044-2047).
- **M-9: Fixed.** Comment at TradeSimTests 2345-2346.
- **M-10: Fixed.** Comments at TradeNode 1832-1833 and BaseHatchery 1292-1293.
- M-6: accepted. Comment at TradeNode 2362-2364. Not re-flagged.

---

### New issues (all Minor; none changes an item's verdict)

- **N1 (budget test, R-b).** TradeSimTests 3284-3285 compute `worst1 = d.ds * math.min(1, 60 / secs)`. A loop slower than 60 s of trade time scales the measured count down. The cap allows all ENTRY_MAX rounds of a pair inside one real minute, so the bar should use `d.ds` unscaled. Both give 54 in this run (secs 55). Drop the min factor.
- **N2 (P1).** The restore in writeAll is pcall'd and silent (BaseHatchery 1126). If a restore throws, the op still errors and the half-write stays, which for take is a loss. The old code had the same hole, and a restore of a value that was just valid is very unlikely to fail. Warn on a failed restore.
- **N3 (P2).** checkSave (BaseHatchery 1137-1139) refuses any non-empty value that does not decode to a table. JSON `null` decodes to nil (believed, not verified in Studio), so `null` now refuses. The spec's "nothing there yet" is only nil or "". Refusing is fail-closed (items stay in escrow). Confirm that no writer can produce "null".
- **N4 (I-1).** The fallback at TradeNode 2140-2142 writes the probe's copy if the post-take encode fails. Its ids, sigs, kg and mut match what take removed. Only `from` could differ, and that affects only where a return lands. Benign. "Can't fail" is reasoning, not a test.
- **N5 (R-b).** The count lives in memory per server (`entryLog`, TradeNode 532), so a teleport starts a new count. This matches "enforced on the player's own node". The controller should confirm that this is the intended bound, since it is the cross-server case already accepted.
- **N6 (M-1).** `commitSeenCount` (TradeNode 541) is never decremented when entries are pruned (1946), so the CACHE_MAX clear fires early. Latency only: the 30 s count restarts, and nothing settles early.
- **N7 (P4, cosmetic).** whyText's "lost" branch (TradeNode 436) tells the other side "@X left the game" when X joined another server. The lost player sees the right text.
- **N8 (P3).** `P.refresh` (TradePresence 709-713) calls busyOf, so a dead lock now costs POLL s inside the serialized refresh loop, once per dead lock (busyOf clears it). Latency only.

---

### Controller rulings from the builder's list

1. movedTo: agree (see P4).
2. Record de-dupe in recordOnce: agree. A cached record is only what the store returned.
3. R-b counts failed entries: agree. N5 is the only open point.
4. P2 refuses with nil, "error": agree.
5. M-4 retries: agree. A stored entry recovers if no save lands.

### Not verified by reading

- JSON `null` decode (N3).
- Whether SetAttribute can throw at these sizes (P1; unchanged from the original review).
- The test outputs (not re-run, per the rules).

---

### Assessment

No Critical or Important findings. I traced each fix for a dupe, loss or steal path and found none. The reasoning is in the item verdicts above.

**Verdict: Approved**
