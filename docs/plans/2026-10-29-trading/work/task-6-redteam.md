# Task 6 red-team: TradeServer part B (escrow, record, settle, recovery)

The adversarial reviewer (Haiku) read the code read-only. The controller saved its report here, because the agent's own
rules stopped it writing the file. The line numbers are from the code at review time.

**Summary:**
- CONFIRMED dupe/loss/steal: 0.
- PLAUSIBLE: 3 (P1, P2, P3).
- CONFIRMED desync with no item effect: 1 (P4).
- Hygiene: 1 (H1).

**Scope:**
- TradeNode (2536 lines), TradeServer, TradeCore, SaveLock;
- PlayerData load/write/release;
- the BaseHatchery TradeItems wrapper;
- the AutoReconnectServer seal;
- TradePresence busy locks;
- TradeConfig.

Every live writer of BaseData / PetInventory / EggInventory was checked for a yield between read and write.

## Findings

**P1. PLAUSIBLE. take/give are not atomic across their attribute writes.**
- How it breaks: take/give JSON-encode first, then write 1-3 attributes in a loop. If the second SetAttribute throws,
  the first has already landed.
  - **take:** the wrapper returns `nil, "error"`, so `enterEscrow` calls `failEntry`. The items are gone from the data
    with no escrow entry written: LOSS at the next autosave.
  - **give (delivery):** the error makes `settleStep` return "refused" and keep the entry. The next check gives again,
    so the attribute that already landed is delivered twice: DUPE.
- Code:
  - BaseHatchery 1241-1243 (the take set loop) and 1314-1317 (the give set loop);
  - TradeNode 1792-1793 (a give error = refused, the entry is kept) and 2023-2024 (a take error = failEntry).
- Impact: LOSS (take) or DUPE (a give retry).
- Fix:
  - check every encoded length against the attribute limit before the first write;
  - restore the old strings if a later write throws (or store the inventory in one attribute).
- Likelihood: low. Sizes are far under any limit, and BaseHatchery 1038-1044 assumes SetAttribute never throws (not
  verified).

**P2. PLAUSIBLE. readData, readPets and readInventory fail open.**
- How it breaks: PlayerData's load copies any stored BaseData string as it is (PlayerData 233-261). If that string is
  `""` or corrupt:
  - `readData` returns `{eggs = {}, pets = {}}` (BaseHatchery 73-79; readPets 488-491; readInventory 85-88);
  - a return for one base pet then writes `BaseData = {pets = [that pet]}` (1314-1315), erasing the base.
- Impact: LOSS of the base, hotbar or egg inventory.
- Fix:
  - a failed decode refuses (returns nil), so take/give refuse ("Bad save");
  - PlayerData treats an unparsable BaseData as a failed load.
- Also: `give("return")` has no DataLoaded check (1254-1260). TradeNode `canSettle` (1725-1733) is the only guard.
- Likelihood: low. It needs a corrupt stored string.

**P3. PLAUSIBLE. A busy lock is released when a live session reads as missing.**
- How it breaks:
  1. X is in a live trade T1 and holds lock T1.
  2. A read of T1 returns nil right after the write.
  3. `node.isSessionLive` returns false (TradeNode 2280-2283, from `stateOf` "missing" at 386-391).
  4. TradePresence `isDead` is true (579-582), so `clearIf` runs and `takeOne` (600-624) takes the lock for T2.
  5. X is now in two trades.
- Impact: a rule break ("one active trade"). No item effect: take removes the items from the data, so a second take of
  the same items fails.
- Fix: clear a lock only on a read that says done or cancel, or count "missing" as dead only after two reads spaced by
  POLL.
- Likelihood: depends on MemoryStore read-after-write consistency (not verified).

**P4. CONFIRMED behaviour, a desync only (no dupe, loss or steal).**
- How it happens:
  1. P's escrow is saved, then P reloads on another server.
  2. Recovery runs before DataLoaded.
  3. `recoverPlayer` writes "aborted" into the empty record (TradeNode 2172-2173): `verdict` returns "abort" for
     recovery without reading the session (1863).
  4. Q's node settles Q's own return.
  5. Meanwhile the session stays in confirm with both escrow marks until the idle expiry (180 s), and the busy locks
     stay held.
- No item effect: commit can't deliver (single record, 1665-1667).
- Fix: for recovery, use the same verdict as the 30 s check (a live confirm with an empty record is left alone), OR
  cancel the session in the same step as the aborted write (rule 4 order: the session first).

**H1. Hygiene (not client-reachable). Unguarded `_G` helpers in BaseHatchery.**
- `_G.HatcheryGive` (1373-1379) mints eggs.
- `_G.HatcheryPlaceAt` (1380), `HatchAll` (1383), `Rebase` (894), `Force` (336) and `Validate` (138) are not behind
  IsStudio.
- Only server code can read `_G`. Gate them with IsStudio.

## Blocked attacks (31): the blocking lines
1. A crash between give and save: settle is one sync step (TradeNode 1757-1798), the snapshot is sync (PlayerData
   290-302), and the record replays once on the next load (2155-2187).
2. Two servers settling one round: `here(uid) == p` (1725-1728), the SettledRounds gate (1762-1770), and the
   version-checked save (SaveLock 186-203).
3. A takeover during a settle save: `judge` refuses a foreign token (SaveLock 74); the lost save fires SaveLost
   (PlayerData 139-146, TradeNode 2189-2197).
4. A read-back racing a dead-committer abort: the only-if-empty write (1665-1667); settle acts only on the returned
   record (2063-2079, 1685-1694).
5. A stale session copy: the rev check (927-928); the re-read before take with round/ver checks (2010-2016).
6. An item re-offered while its escrow is open: take removes it from the data (BaseHatchery 1219-1243); count excludes
   it (1123-1139); enterEscrow waits for older entries (TradeNode 1996-2007).
7. Trading on server 2 while the old server holds a session: the busy lock (TradePresence 600-652); leave cancels
   (TradeNode 2454-2461, 2288-2319); the old server's writes are refused (SaveLock 186-203).
8. Forged refs / another player's pet id / an unowned egg / NaN or inf KG: CHECK.add 1251-1254, cleanRef 335-352,
   validKg (TradeCore 49), describe from own data (BaseHatchery 1141-1165), addItem (TradeCore 251-277).
9. An early READY/ACCEPT or an old ver: TradeCore.ready 298-299; accept 345-350.
10. Forcing a commit without both accepts or escrows: toCommit 365-366; record is nil unless both marks exist (TradeCore
    457); commitRound 2063.
11. Editing the other side's offer: add/remove write only `t.side` (1435, 1448); handle acts for the caller (2256-2257).
12. Settling twice: the SettledRounds gate (1762-1770), with the entry deleted in the same step (1779-1781).
13. The same pet 9x: addItem (TradeCore 262-270); takePet (BaseHatchery 1190).
14. Over-count eggs or a 100.5 / 100.4 KG swap: the addItem count (270-272); the exact `%.17g` sig (TradeCore 124); take
    eggNeed (BaseHatchery 1193-1216).
15. Selling or placing an offered item before escrow: take refuses (1189/1216), and the round aborts and returns
    (TradeNode 2022-2024, 1973-1979).
16. Selling or placing during Phase 2 after escrow: the items are out of the data (BaseHatchery 1219-1243), and those
    paths read the data.
17. Destroying another player's Tools: destroyPetTools touches only the player's own Backpack/Character, by PetId
    (1109-1121); CanBeDropped is false (526).
18. Using a surviving pet Tool: equip looks the pet up by id (631-645); unequip reads the base data (649-657).
19. Disconnecting at each phase: leave cancels (2454-2461, 2288-2319); the escrow is recovered from the save
    (2155-2187); a taken-over leave save is refused.
20. A teleport or Auto Reconnect in Phase 2: Reconnecting blocks take/deliver/new trades/entry; the seal cancels or
    settles only before the final save (AutoReconnect 139-148; TradeNode 2202-2217); commit is left to its record.
21. Remote spam: the limiter (651-671); CHECK before the queue (1227-1234, 2262-2263); oneAtATime (693-710).
22. Request flooding or duplicates: the pending cap, one per sender, the cooldown, busy (1119-1137).
23. Accepting a request twice: `list[reqId] = nil` before any yield (1353).
24. Two trades at once: takeBusy plus the trades checks (1120, 1197, 1289).
25. Other save writers bypassing SaveLock: only PlayerData writes PlayerData_v3; every live attribute writer is
    synchronous.
26. A yield between check and write in other removers (place, hatch, equip, unequip, GivePet, GiveEgg, bank, Sell,
    potionHatch, rebase): all yield-free.
27. A second ledger record for one round: the per-round key plus the only-if-empty write (146, 1665-1667).
28. A client writing sessions: no remote writes to MemoryStore.
29. Round number reuse: round only increases in startConfirm (TradeCore 310-323); trade ids are GUIDs.
30. Delivering to the wrong side: `rec[e.side] == uid` (1776).
31. A stale or replayed bus message: handlers re-read; ac/ar need a matching id and state (1186, 1207-1208, 1212-1215).

## Not verified
- MemoryStore GetAsync consistency right after UpdateAsync (P3).
- Whether SetAttribute can throw on valid strings, and at what size (P1, P2).
- Whether a timed-out UpdateAsync can apply after its error. SaveLock's token / `_wid` checks cover it if it can.
