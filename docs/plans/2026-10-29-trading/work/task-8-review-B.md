# Task 8 whole-system security review: reviewer B (attacker view)

Reviewer: Haiku 5.5, read-only (script_read, script_grep, read-only Edit-datamodel listing). No Play, no edits, no writes to Studio.
Studio: 3bf21205-caff-490e-a927-3bd9f0097311. Line numbers are the live scripts at review time. Short names below map to
ServerScriptService.<name> unless marked otherwise (TradeClient is StarterPlayer.StarterPlayerScripts.TradeClient; TradeConfig is ReplicatedStorage).

## Summary
- Critical: 0
- Important: 2 (I-1 CONFIRMED, I-2 PLAUSIBLE)
- Minor: 5 (M-1 CONFIRMED, M-2 PLAUSIBLE, M-3 CONFIRMED, M-4 PLAUSIBLE, M-5 CONFIRMED)

No duplicate, lost or stolen pet/egg path found. Escrow, the single ledger record, settle-once, version-checked saves and
recovery hold on every path traced below. The earlier red-team fixes are present and do what they claim: P1, P2, P3, P4,
I-1, I-2, R-a, R-b, M-1, M-2, M-4, M-7, M-8. The only leftover from that round is the silent restore in writeAll (M-4 here).

## Important

### I-1. Four alt accounts can keep a player's 3 request slots full (CONFIRMED)
Impact: the victim cannot receive a trade request from any other player while the attack runs. No item effect. The spec's
§6 row "Request-bombing / stalking players" says this is blocked; the limits as built do not stop it.

Steps:
1. Four accounts (each finished the tutorial and passes PolicyService) each SEND to victim V.
2. HANDLERS.rq on V's node counts other senders' live requests and answers "full" at 3 (TradeNode.lua 1181-1185; the text is
   refusalText 462-468, "@V has too many requests"). A request lives REQUEST_TTL = 30 s (TradeNode 1193, TradeConfig 39).
3. A sender is limited to 1 SEND per 3 s and 10 per 5 min (RULES.send 719, CHECK.send 1291-1297, TradeConfig 41-43). Its
   outgoing request clears about 32 s after SEND (poll 2539-2545), so one account can re-send every ~32 s, about 9.4 per 5 min.
4. Four accounts staggered about 8 s apart keep at least 3 live requests at every moment. A decline frees a slot, but the
   30 s decline cooldown (1176, 735) blocks only that one pair, and another account refills the slot.

Fix: an intake limit on the receiver's own node, independent of the sender. For example, at most 2 new requests per receiver
per 30 s from any senders, checked in HANDLERS.rq before the cap at 1181. That keeps one slot for real players. Keep the
3-pending cap.

### I-2. Refused session calls still cost a MemoryStore UpdateAsync; one colluding pair can drive about 8 writes/s (PLAUSIBLE)
The request count is CONFIRMED by code. The quota effect is PLAUSIBLE: the MemoryStore per-minute quota and unit costs are not verified here.
Impact: presence, busy locks, trade sessions and the weather/event MemoryStore map in AdminServer (126, 620, 651) all share
the game quota (TradePresence.lua header line 8: "1000 + 120 x users"). Several pairs can throttle trading ("syncing...")
and weather/admin events game-wide. No item effect. The spec's §6 row "Two alts burning the game's MemoryStore budget"
assumes the per-trade cap (30 changes per 10 s) bounds the writes. Refused button presses are outside it.

Steps:
1. Accounts A and B are in one trade (B accepted A's request).
2. Each player sends READY, ACCEPT, BACK or CANCEL, or add/remove, as fast as the limiter allows. RULES.button (722) gives
   4/s per player and is shared by READY, ACCEPT, BACK, CANCEL and state. RULES.change (720) gives 4/s for add and remove.
   CHECK.ready, back and cancel are 1314-1320; CHECK.add is 1306-1309.
3. Each call reaches act() (1108-1124) and then writeSession() (789-817). The callback runs TradeCore's rule and returns nil
   when refused (801-804), but the UpdateAsync request is still made. A refused READY during the 5 s lock is one write. So is
   an add refused by the per-trade cap (TradeCore.rateOk 152-158, applied in addItem at 257).
4. That is up to 8 UpdateAsync/s (about 480/min) for one pair. The per-trade cap bounds only accepted changes.

Fix: charge every session write, accepted or refused, to a per-trade and per-node budget. Let the node refuse what its own
copy already proves (phase, lock window, a ver that is behind) with no service call. Lower READY/ACCEPT/BACK/CANCEL to
1/s per player. Feed the write budget into the existing MemoryStore backoff.

## Minor

### M-1. Rate-limit state is cleared on leave, so a rejoin resets pacing (CONFIRMED)
TradeNode.lua 2612 `limits[uid] = nil` in onLeave. The decline cooldown also lives on each node (1176, 735), so a rejoin by
the decliner clears it on that node. Impact: SEND and change pacing reset with each leave and rejoin. The cost is one join
(a DataStore load), so the impact is bounded.
Fix: do not clear the limiter on leave. Its entries already expire by their windows.

### M-2. A dead server leaves its players' busy locks held up to 15 minutes (PLAUSIBLE, needs a crashed node)
TradeNode 2426-2428: isSessionLive returns true for any state that is not "missing" or "over", so an "expired" session
(idle 180 s, TradeCore.expired 447-453) still holds the lock. Only the owning node's poll (2551-2576) cancels it, and the
lock is refreshed only by that owner (2567-2569). The lock TTL is SESSION_TTL = 900 s (TradePresence 612 and 664, TradeConfig 56).
Impact: both players see "already trading" for up to 15 minutes after the owning server dies. No item effect, since Phase 1
holds nothing in escrow. The attacker cannot trigger it.
Fix: after the second read, treat an expired session as not live. An expired session cannot commit (TradeCore.toCommit 363
runs precheck, which refuses expired). Escrow still settles from its record.

### M-3. DataLoaded is set after the 10 s recovery timeout while recovery still runs (CONFIRMED)
PlayerData.lua 172-174 warns "loading on" and continues. 276-278 set DataLoaded = true after runRecoveryHook returns. Impact:
a player can start a trade while older escrow entries are still unsettled. No duplicate: settleStep's SettledRounds gate
(TradeNode 1840-1848) and enterEscrow's wait for older entries (2095-2112, then failEntry) both hold.
Fix: a separate RecoveryPending attribute, cleared when recovery completes and checked by ownRules (1132-1140) and by notReady
(BaseHatchery 1062-1066).

### M-4. The take/give restore after a failed write is silent (PLAUSIBLE, very unlikely)
BaseHatchery.lua 1126: `pcall(p.SetAttribute, p, name, old[name])` ignores failures. If a SetAttribute in writeAll throws and
the restore also throws, a take leaves a half-write: items gone from the data with no escrow entry, which is a LOSS. This is
the open N2 from the fix round. Whether SetAttribute can throw at these sizes is not verified.
Fix: warn on a failed restore and stop trading and saving for that player until reload.

### M-5. Studio helpers on _G are not gated by IsStudio (CONFIRMED, not client-reachable, pre-existing)
BaseHatchery.lua 1415-1424: `_G.HatcheryGive` (mints eggs straight into the attribute), `_G.HatcheryPlaceAt`, and likewise
HatchAll, Rebase, Force and Validate (red-team H1, deferred by ruling). Only server code can read _G, so a client cannot reach it.
Fix: gate them with STUDIO.

## Checked and blocked (one line each, with the blocking line)
1. Forged remote args (types, sizes, ids): TradeServer 51-63 -> TradeNode.remote 2412-2416 (op allowlist, real Player only), handle 2399-2410 (here(uid) == player; CHECK before the call queue).
2. Acting on another player's offer: add and remove touch only t.side (1491-1510, TradeCore.addItem 260).
3. A client writes a session or fakes an accept: no remote writes a session; only TradeNode's writeSession does.
4. Early READY/ACCEPT: TradeCore.ready 302, accept 351, toCommit 370 (5 s locks on the node's own clock; OPS 1526, 1552).
5. Old ver: TradeCore.ready 301, accept 349 (clientVer must equal s.ver).
6. Forced commit without both accepts or both escrows: toCommit 367-368; committed record only with both lists (TradeCore.record 459, committedRecord 1777).
7. Change after accept: addItem 256 and removeItem 285 (select phase only).
8. Nine items, same pet nine times, over-count eggs: addItem 261, 267, 271-274.
9. NaN, inf or non-positive KG: validKg 49, cleanRef 353, petSig 115, eggSig 123.
10. Another player's pet id: describe reads only the caller's data (BaseHatchery 1182-1190); take refuses unknown ids (1226-1227).
11. KG rounding swap (100.5 vs 100.4): exact %.17g signature (TradeCore 124) and exact take match (BaseHatchery 1232-1254).
12. Mutation spoof in an egg ref: describe matches the exact signature (BaseHatchery 1193-1198).
13. Destroying another player's Tools: destroyPetTools matches PetId in own Backpack and Character only (BaseHatchery 1146-1158); CanBeDropped = false on pet and egg Tools (BaseHatchery 526, EggSpawner 448).
14. Settling a round twice: SettledRounds gate and entry removal in one synchronous step (TradeNode 1835-1876).
15. Two records for one round: the ledger write lands only in an empty key (TradeNode 1721-1747, 1750-1757).
16. Stale copy or two servers writing one save: judge (SaveLock 71-77), _run (186-202), a lost save stops writes and kicks (PlayerData 139-147).
17. A write re-sent after it landed: _readBack and the _wid check (SaveLock 154-168, 189-202).
18. Escrow before commit: the escrow save precedes setEscrowed (TradeNode 2146-2153); commit needs both marks (TradeCore 368).
19. Sell, place or equip during escrow: items leave the data at take (BaseHatchery writeAll 1281) and lookups are by id in data.
20. Leave or disconnect in any phase: onLeave cancels (2608-2615), recovery settles from the record (2294-2324), a leaving player is never given to (canSettle 1802-1804).
21. Teleport or Auto Reconnect mid-trade: Reconnecting is set and TradeCancelFor runs before the final save (AutoReconnectServer 139-148); the seal settles select and confirm and leaves commit to its record (sealCancel 2339-2358).
22. Shutdown mid-trade: node shutdown cancels select and confirm (2365-2378); PlayerData close saves release (446-460); escrow recovers on the next load.
23. The old server writing after a takeover: refused by its token (SaveLock 186-202); handleSession marks lostSave (992-998); recoverEntry cancels the live confirm first (2273-2292).
24. Accepting one request twice: list[reqId] = nil before any yield (1408), and trades[uid] is re-checked after ownRules (1396).
25. Two trades at once: takeBusy takes the lower uid first and releases only what this call took (TradePresence 637-652, takeOne 600-624); the session is written before the locks (OPS.respond 1436-1441).
26. A busy lock cleared while a live trade holds it: a second read before a missing lock is cleared (TradeNode 2420-2436); isDead is checked outside callbacks (TradePresence 579-582, 620).
27. A Robux receipt granted before its save: Receipts 73-76 returns PurchaseGranted only after saveNow; grant and id in one sync step (62-63).
28. A gift granted twice or written into another live save: GiftReceipts record first (ShopServer 293-320); inbox dedupes by purchaseId (SaveLock 260-280); AddGiftedPass writes only players loaded here (PlayerData 415-431).
29. A trade with yourself: OPS.send 1339; newSession 231.
30. Privacy of the player list: rows carry uid, name and status only (rowsFor 479-506, search 549-576); AWAY only for friends (497-498); a non-friend name and an unknown name both answer "isn't online" (563, 575).
31. Studio seams in a live game: _fault and _faultMid need STUDIO (BaseHatchery 1393-1394); TradeServerDebug (TradeServer 93); TradePresenceDebug (TradePresenceServer 18); SaveLock.useStores and setBackoff (SaveLock 229); TradePreview (TradeClient 2165); PlayerData test hooks (108-114, 143); Receipts tests (85); crashAt is passed only by the simulation.
32. Trade-window scam: the other side's cards come from the owner's node with ids hidden (viewOf 870-878); ACCEPT needs the ver the viewer saw (TradeCore 349).
33. Bus spoofing: only server code publishes; every handler re-reads the session and checks its id and state (HANDLERS 1162-1270, onMessage 1273).
34. Idle or total timeout bypass: idle 180 s and total 600 s (TradeCore.expired 447-453); chat does not reset idle (TradeCore.chat 420-441).
35. Remote spam: the limiter runs before the call queue (CHECK 1290-1333, allow 697-717); one call at a time per player (oneAtATime 739-756).
36. BACK or entry loop used to burn DataStore: ENTRY_MAX 6 per 300 s on the player's own node (ready 1518-1520, logEntry 568-573).
37. Presence or search leaking job ids: no; rows are built from entries and job is stripped (rowsFor 486, 500; search 567).

## Not verified
- MemoryStore and DataStore quota figures and per-call unit costs (I-2).
- Whether SetAttribute can throw at these sizes (M-4).
- MemoryStore read-after-write consistency (accepted in the red-team pass).
- TradeClient was read for its remote calls, Studio gates and the preview seam, not line by line. Every op it can send is re-checked by the server, so its residual risk is display only.
- The modal-lock edits in PetsEggsUI, SellClient, UpgradeClientLegacy, WeatherClient and MenuController are UI-only and were not read in depth.
