# Task 8 whole-system review, reviewer A (invariants and save lock)

Read-only review. Studio was only read (script_read, script_grep, read-only Edit execute_luau). Nothing was edited or played.

Read in full: SaveLock, PlayerData, TradeServer, TradeCore, TradeNode (all 2690 lines), TradeConfig, Receipts, Mutations (entry helpers). Read in part: BaseHatchery trading section (1020-1474), AutoReconnectServer (30-230), AdminServer restart (150-275). Checked against spec sections 5-7, the ledger "Ruling:" lines, the Task 6 report, and the Task 6 red-team notes.

## Verdict

- Critical: 0. Important: 0.
- Minor: 6 (3 CONFIRMED, 3 PLAUSIBLE).
- No path found where an item ends in two places, in no place, or with the wrong owner.
- The guarantee comes from four things: (a) `take()` removes items from the save in the same synchronous step that writes the TradeEscrow entry; (b) each round has one ledger record, written only into an empty key; (c) settle-once through SettledRounds, written in the same attribute step as the credit; (d) the version-checked save lock, which stops a server that lost a save from persisting its credits.

## Prior findings: did the fixes hold?

- Red-team P1 (take/give writes not atomic): holds for TradeItems. `writeAll` rolls back (BaseHatchery 1112-1128). Still open for settleStep's own writes after give (M2).
- Red-team P2 (fail-open readData on take/give): holds for take and give. `checkSave` refuses a broken save (BaseHatchery 1132-1143, called at 1209 and 1314). count/describe still read fail-open, but they never write.
- Red-team P3 (busy lock cleared on one missing read): holds in `isSessionLive` (TradeNode 2428-2435, two reads). Not applied in the 30 s check (M3).
- Red-team P4 (recovery writes "aborted" while the session is live): holds through cancel-first (TradeNode 2276-2288). Not if the cancel write fails (M4).
- Red-team H1 (unguarded `_G` helpers): still open (M5).

## Findings

### M1. Minor. CONFIRMED. Soft restart saves open trades without cancelling them first

- Spec section 6, invariant 1: before a server-made teleport's final save, a trade in phase select or confirm is cancelled.
- AdminServer.lua:165-185 `saveBeforeLobby` calls `SavePlayerNow` for every player. `sendToLobby` (195-223) then teleports. Nothing in AdminServer cancels the trade. `TradeCancelFor` is only called from AutoReconnectServer:143.
- Effect: the pre-teleport save holds a live escrow entry, and the session stays open until `onLeave` (TradeNode 2608-2615) cancels it.
- No item effect found. Recovery (2273-2292) and the ledger record decide on the next load.
- Fix: cancel each player's Phase 1/2 trade before `saveBeforeLobby`, the way AutoReconnect does through `TradeCancelFor`. Or change the spec text to match the code.

### M2. Minor. PLAUSIBLE. Writes after `give` in settleStep can duplicate items

- TradeNode.lua:1870 `itemsCall("give", ...)` succeeds. Then 1872-1874 `p:SetAttribute` for TradeEscrow, SettledRounds and TradeHistory run with no guard.
- If one of them throws after the credit, settle returns an error, the entry stays, and the next check gives again. That is a duplicate.
- Practically unreachable at normal sizes. History is about 75 KB at most, SettledRounds about 9 KB, against the attribute size limit (about 200 KB). The comment at 1830-1831 assumes this. Not tested in Studio.
- Fix: check the three string lengths before `give`, or extend `writeAll` to cover them.

### M3. Minor. PLAUSIBLE. The 30 s check treats one nil read as "missing"

- TradeNode.lua:1968-1976 `verdict`: one `readSession`. A nil read gives "missing", which gives "abort", which writes an only-if-empty "aborted" record for a possibly live trade.
- Safe: the record decides, so no commit and no item effect. The effect is a spurious cancel.
- The double-read rule from red-team P3 (2428-2435, and handleSession 975-987) is not used here.
- Fix: count "missing" as abort only after a second read one POLL later.

### M4. Minor. CONFIRMED. "aborted" can be written before the session moves (spec section 6, rule 4 order)

- `verdict` returns "abort" for an expired confirm session at TradeNode.lua:1994, while the session is still phase confirm. The session moves to cancel only later, in handleSession's expired branch (1007-1011).
- `recoverEntry` (2280-2290) still writes "aborted" when the cancel write failed (`okC` false).
- Safe: `toCommit` refuses expired sessions (TradeCore.lua:82 precheck), and a competing commit loses to the single record (TradeNode 1728). Both sides settle from the record.
- Fix: move the session first in the expired case, or record the deviation in the spec.

### M5. Minor. CONFIRMED. Unguarded `_G` test helpers in BaseHatchery (red-team H1, still open)

- BaseHatchery.lua:1415-1436: `_G.HatcheryGive` (writes EggInventory directly), `_G.HatcheryPlaceAt` and `_G.HatcheryHatchAll` have no IsStudio gate. Only the `HatcheryDebug` dispatcher (1437-1474) is gated.
- Not reachable from a client: `_G` is server-only, and grep finds no live caller.
- Fix: wrap these in `RunService:IsStudio()`, or move them into the gated block.

### M6. Minor. PLAUSIBLE. An unreadable TradeEscrow leaves items stuck

- TradeNode.lua:158-165 `escrowOf` returns nil for undecodable data. `recoverPlayer` (2297-2301) returns after one warning. `settleStep` (1837) refuses, and `considerPlayer` (2044-2048) logs every poll.
- The player loads normally but can never trade, and the items stay stuck until the save is repaired by hand.
- Reachable only from corrupt stored data. PlayerData does not check TradeEscrow at load. BaseHatchery's `checkSave` does this for the other item fields.
- Fix: at load, treat an undecodable TradeEscrow as a failed load (like `checkSave`), so the save is not used.

## Accepted rulings re-checked and still holding

- The HOOK_WAIT overrun (PlayerData 163-175): DataLoaded can come before recovery finishes. Trades then wait in enterEscrow (ENTRY_WAIT 8 s, TradeNode 2100-2113). Items stay safe because of the SettledRounds gate (1840) and settle-once.
- R-a (aborted returns settle in memory only): safe. The unsaved return is either saved with the entry still present, or dropped with the lost save, and then recovered from the record (PlayerData 389-402, TradeNode 2273-2292).

## Paths checked and blocked (path: blocking line)

1. Normal trade: commit needs both escrow marks, toCommit 362-374 and TradeCore.record 457-461. Record is one only-if-empty write (TradeNode 1721-1731). Settle is once per player per round (1835-1876, SettledRounds at 1840).
2. Phase 1 leave, X, idle or total timeout: nothing was moved, so there is nothing to return. cancelFor 2440-2471, TradeCore.cancel 394-404.
3. BACK in phase 2: TradeCore.back 379-390 clears offers and escrow marks, then roundEnded writes "aborted" after the move (2208-2249).
4. BACK racing commit: TradeCore.back refuses commit (TradeCore 382). toCommit moves the session first (371-373), and the record decides (1721-1731).
5. Cancel in commit: refused (TradeCore 397). commitRound (2165-2206) follows the record.
6. Idle or total timeout: TradeCore.expired 447-453. toCommit and accept refuse expired (precheck TradeCore 82). verdict abort only after the record check (1994).
7. Timeout in commit: commit never expires (TradeCore 448, LIVE only). Dead committer after 30 s: verdict 1979-1982 with seeCommit (1981).
8. Leave in phase 2, own escrow saved: PlayerData release (398, snapshot taken with the entry), settle refused for a leaving player (canSettle 1804), recovery on next load (2294-2324).
9. Leave in phase 2, commit: cancel refused (TradeCore 397), record decides, leaving player's settle skipped (canSettle 1804).
10. Auto Reconnect seal: Reconnecting set (AutoReconnectServer 139) before TradeCancelFor (143-147). sealCancel (2339-2358). canSettle "seal" only (1807). take refuses Reconnecting (BaseHatchery 1064). give deliver refuses it (1298-1300). Saves refused after seal (PlayerData 348, 317).
11. Server shutdown: TradeServer 89-91 and PlayerData 446-460 run in parallel. Either order is safe: the entry stays in the save with the record, and recovery settles it once.
12. Crash after escrow save, before setEscrowed: no escrowed mark, so toCommit refuses (TradeCore 367-368). Idle expiry, then verdict abort (1994), then return.
13. Crash after commit, before record: 30 s rule (1979-1982), then recordOnce, then the record decides.
14. Crash after record, before settle: recovery (2273-2292), SettledRounds gate (1840), deliver waits for DataLoaded (BaseHatchery 1063).
15. SaveLost takeover mid-trade: token check (SaveLock 71-77), `_lose` (144-150), PlayerData onLost (139-148), TradeNode saveLost (2326-2334), lostSave in canSettle (1802), saveOf (1785-1795).
16. Recovery on next load: hook before DataLoaded (PlayerData 276), recoverEntry (2273-2292), canSettle "recovery" (1805).
17. 30 s check: live confirm is never aborted (verdict 1985-1992). Commit abort only after 30 s (1979-1982).
18. Kill switch: handle refuses everything (2404). poll cancels only live trades and leaves commit to its record (2511-2528). enterEscrow fails closed (2094).
19. Sell or place of an offered item before escrow: take is all-or-nothing (BaseHatchery 1227-1240, writeAll 1281). Failure aborts the round (TradeNode 2134-2136).
20. Same pet nine times, or a pet not owned: addItem (TradeCore 264-272), take takePet (BaseHatchery 1228), describe refuses duplicate ids (1185).
21. Egg 100.4 vs 100.5 KG swap: exact-KG signature (TradeCore 124), take signature check (BaseHatchery 1232-1233).
22. Forged remote, other player's pet id: OPS.add reads the caller's own data (TradeNode 1483), CHECK.add (1306-1309), handle requires here(uid) == player (2401).
23. Early READY or ACCEPT, old ver: TradeCore.ready 298-301, accept 345-350, lockReason 60-65.
24. Forced commit: toCommit needs both accepts and both escrow marks (TradeCore 362-374). No "complete" remote (REMOTES 110-114).
25. Two trades at once: no new escrow while an older entry is open (TradeNode 2100-2113, 2125-2126). Busy locks as well.
26. Other writers racing a trade: all removers run with no yield (BaseHatchery 1037-1038). settleStep has no yield (1835).
27. Autosave racing a trade write: snapshot taken when the write runs (SaveLock 170-175), one queue per save (131-141).
28. Late in-flight write from an old lock: expected-version check (SaveLock 71-77), unsure-write ids (214), so it is refused or accepted as its own.
29. Gift path: only PlayerData writes PlayerData_v3 (grep; live only). AddGift (PlayerData 415-431) and inbox (SaveLock 260-280).
30. Robux receipt: PurchaseGranted only after the save (Receipts 73-75). Grant and id set in one step (63).
31. Tools: destroyPetTools touches only the trader's own Backpack and Character, by PetId (BaseHatchery 1146-1158). CanBeDropped false (526). sortBackpack is synchronous (581-604), so no race with take.
32. Studio seams unreachable live: TradePreview (TradeClient 2165), TradeServerDebug (TradeServer 93), TradeItems `_fault` (BaseHatchery 1393-1394), HatcheryDebug (1437), `crashAt` (env only, TradeNode 1711, TradeServer passes an empty env), PlayerDataDebug (PlayerData 462-474).
33. Remote spam: limiter (TradeNode 697-717), one call at a time (739-756).
34. Stale session copy: revision check (TradeNode 972-973).

## Answer, path by path

- Two places: none found on any path above. The only copies that can exist at once are in-memory credits on a server that has lost its save. They never persist (SaveLock 71-77 and 170-216), and the new owner recovers from the save and the record.
- No place: items are held in escrow while a round is pending. That is a delay, not a loss. It ends on the next load (2273-2292) or on the 30 s check (1964-2035). The only stuck case is the corrupt-data case in M6.
- Wrong owner: none found. Settle requires `e.userId == uid` (TradeNode 1851) and `rec[e.side] == uid` (1854).
