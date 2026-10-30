# SLINGSHOT Trading System: design (2026-10-29, v4 after three security review rounds)

Owner's request (2026-10-29): add trading of pets and eggs with other players, in any server, safe from hackers.
"Security is the highest priority. No player should ever be able to steal pets or eggs."

## Decisions made with the owner
| Question | Decision |
|---|---|
| AWAY players (played before, not online now) | Shown, SEND greyed ("AWAY"), trades are live only. Only your Roblox FRIENDS are shown as AWAY (privacy) |
| Block button | No (request limits only) |
| Extras | History tab + quick chat buttons. No Settings tab |
| Request pop-up | The player who RECEIVES a request sees it in the bottom-right corner |
| Items per player per trade | Up to 9 (pets + eggs together) |
| Cross-server | A: live cross-server trading (no teleport); same-server trades use the same path |
| Cancel / BACK | Offers are emptied; players re-add their pets or eggs ("they gotta re-add the pets or eggs") |
| Security model | Escrow + one permanent trade record per confirm round + version-checked saves (section 6) |

## 1. HUD
- The Admin button (only for whitelisted UserIds, `AdminLogic` ADMINS) moves BELOW the Rebirth and Index tiles. It's
  currently placed above the Shop tile by `ServerStorage.AdminUI.AdminClient.placeButton`.
- A new **🤝 Trading** tile goes in the same left menu area, styled like the other menu tiles (Check-UI).
- The exact placement and look come from a mockup the owner approves before it's built.

## 2. Trading menu (one window, Check-UI, one layout on every device)
Header "TRADE" with a [X] close button. Tabs: **Players | History**.

**Players tab**
- A search box ("Search player here...") and a scrolling list of rows: avatar headshot, @username, a status dot +
  word, and a SEND button.
  - **ONLINE** (green): in the game right now, in ANY server. SEND is enabled.
  - **AWAY** (yellow): has joined Slingshot before, not online now (or no live online entry). SEND is greyed out and
    reads "AWAY". **Only your Roblox friends are ever shown as AWAY** (owner, 2026-10-29: "Friends only"), so
    strangers can't see when other kids were last online.
  - A player who has never joined Slingshot is never shown.
- Default list: every online player (all servers) first, then your AWAY friends. Yourself is never listed.
  - Friends come from `Players:GetFriendsAsync`, cached for 5 minutes.
  - "Has played" is checked in `TradeSeen_v1` for up to 100 friends, at most 40 reads a minute per server, with
    results cached per server for 10 minutes. Friends not checked yet appear on a later open.
- Search filters the list as you type. If nothing matches and the text is a valid username (3-20 letters, digits or
  `_`), the server looks up that exact username:
  - online now (any server): one ONLINE row;
  - your friend who has played: one AWAY row;
  - anyone else: "@name isn't online".
- **Invite Friends** button at the bottom of the list (always there, most useful with 5-10 players). It opens Roblox's
  own invite menu (`SocialService:PromptGameInvite`, after `CanSendGameInviteAsync`).
- If trading is off for you (see Rules): the list still shows, every SEND is disabled, and one line explains why.

**History tab**
- Your last 20 completed trades, newest first: who with (@name), when ("2 h ago"), what you gave and what you got
  (small item cards).

## 3. Trade flow
**Request**
1. A presses SEND on an online player B.
   - A's server asks B's server first and waits up to 2 s for an answer.
   - No answer (B's server is gone) means "@B isn't online right now".
2. B gets a pop-up in the **bottom-right corner**: "@A wants to trade", with ACCEPT / DECLINE and a 30 s timer bar.
   It sits above the bottom-right event icon row.
   - Pending requests are stored on B's server, keyed by request id.
   - B can have at most 3 pending requests, shown stacked with the newest on top. A 4th is refused for its sender with
     "@B has too many requests".
   - Accepting one runs every rule check again (on each player's own server) and takes both players' busy locks: one
     key at a time, lower userId first, with the first lock released again if the second fails. The other requests
     then fail with "@B is already trading".
3. Decline, timeout or A cancelling makes it vanish, and A gets a toast ("@B declined").
4. Accept opens the trade window for both players.

**Trade window**, built from the owner's screenshots in our Check-UI look:
- Left: your inventory, with tabs Pets / Eggs. It holds your base (equipped) pets, your hotbar/inventory pets and your
  unplaced eggs.
- Centre: "Your Offer" and "@B's Offer", 3x3 each. A card shows the creature picture, name, KG, mutation badge and
  $/s (eggs: picture, name, KG, mutation). Each side shows its total $/s.
- Right: Trade Chat with 6 quick chat buttons.
- **While you're trading:**
  - The trade window is modal: the other menu tiles (Shop, Index...) are disabled until it ends.
  - If the window disappears (respawn deletes PlayerGui folders), it's rebuilt from the session, and dying never
    cancels a trade.
  - A disabled button always shows why (tutorial not done, not allowed in your country, busy, inventory full).

**Phase 1: select items**
- Click an inventory card to add it to your offer; click it in your offer to remove it.
- Both players see both offers update live: same server instantly, cross-server usually within 1-2 s. A small
  "syncing..." shows while a change is on its way.
- READY is locked for **5 s after the last change by either player** (countdown under the button, "2.9s Left").
- Any change clears both READYs and restarts the 5 s.
- CANCEL ends the trade.

**Phase 2: final confirmation** (when both pressed READY on the same offer)
- Both offers are shown read-only and the inventory panel is hidden. The items are now in escrow (section 6).
  - Until both escrows are saved, the window shows "Securing items..." and ACCEPT stays locked.
- Anti-scam view:
  - every card shows its mutation in words and the exact KG (no rounding);
  - one plain summary line: "You give 1 egg - You get 2 pets", with the $/s difference.
- ACCEPT unlocks **5 s after Phase 2 starts** (countdown on the button).
- Each player presses ACCEPT. The first one shows "Waiting for @B...". The trade completes only when both have
  accepted this exact offer.
- BACK returns both players to Phase 1 with **both offers EMPTY** (owner, 2026-10-29: "when they cancel the trade,
  they gotta re-add the pets or eggs"). The escrow goes back to the inventories, every accept and ready is cleared,
  and both players add their items again from scratch.
- Closing the window [X] or CANCEL ends the trade. Everything goes back, and a new trade always starts with empty
  offers. Nothing is remembered.

**Done**: both players see "Trade complete!" with what they GAVE and what they GOT. Received pets go to the
hotbar/inventory with new IDs; received eggs go to the egg inventory. Both players' saves are written immediately.

**Quick chat**
- The preset phrases from the owner's reference: Add More, L Trade, Last Offer, Deal?, Fair Trade, No Thanks.
- The client sends only the phrase number, never free text, so nothing needs the text filter.
- The last 8 lines are shown as "@name: Deal?".
- Chat never changes the offer version or the idle timer.
- One message per 1.5 s, and the same phrase at most once per 5 s (no "Last Offer" spam).

## 4. Rules and limits (all checked by the server)
- **Who can trade:**
  - your data has loaded (`DataLoaded == true`, so never on an unsaved session) and the tutorial is done
    (`TutorialDone == true`);
  - Roblox's policy allows paid-item trading for you
    (`PolicyService:GetPolicyInfoForPlayerAsync(player).IsPaidItemTradingAllowed`). Roblox requires us to respect it,
    and Starter Pack eggs are paid items.
  - Each player's OWN server checks them on join, caches the result for the session and passes it into the request
    and the session.
  - A PolicyService error counts as "not allowed". The result is checked at SEND, at request accept and at Phase 2
    entry, and both players must pass.
  - **The field name is verified in Studio before any code is built.** If it doesn't exist, the build stops and
    the owner is asked.
- **One active trade per player** (including an outgoing request). Trading with yourself is refused.
- **Items:**
  - Max 9 per side.
  - Pets: equipped (base) or stored. Eggs: unplaced only. Eggs on the base / hatching can't be traded.
  - **No duplicates:** a pet id can be in the offer only once. For eggs, the number of offered cards with the same
    kind + KG + mutation can never be more than the player owns. KG must be a finite number > 0: NaN and inf are
    refused.
- **Room:** both players must have room after the trade (150 pets / 150 eggs, `InventoryConfig`). This is checked at
  READY and again at Phase 2 entry. Equipped pets they give away don't free inventory room. Otherwise it's refused
  with "@B's inventory is full".
  - Delivering a completed trade and returning escrow can never fail: they may go over 150 by the trade's item count
    (like the Starter Pack egg's `force`).
  - New gains are still blocked at 150 until the player is back under, by selling at the Sell stall (the existing
    exit path).
- **Request limits:**
  - 1 SEND per 3 s and at most 10 SENDs per 5 minutes per player;
  - at most 3 pending requests per receiver;
  - a request expires after 30 s;
  - after a decline, the same pair waits 30 s.
- **Rate limits:**
  - offer changes 4 per second per player, and at most 30 per 10 s per trade;
  - quick chat (see above), search 1 per 2 s, list refresh 1 per 5 s.
  - Refused calls count against the limits too.
- **Time limits:** an idle trade (no offer/phase change for 3 minutes) is cancelled, and no trade can last longer than
  10 minutes in total. That stops two alts keeping a trade busy forever.
- Every remote checks types and sizes, acts only for the caller and returns `ok, reason` for a toast. A refused action
  changes nothing (not even the idle timer). Bad input is refused before any service call is made.

## 5. Architecture (server only; the client only displays and sends requests)

**Modules**
| Piece | Where | Job |
|---|---|---|
| `TradeConfig` | ReplicatedStorage | numbers above, quick chat phrases, store names (`_Studio` suffix in Studio for EVERY store and the topic; Studio never touches live names) |
| `TradeCore` | ServerScriptService | PURE state machine: a session + an action -> the new session or a refusal. No services, fully unit-tested |
| `TradePresence` | ServerScriptService | the ONLINE map, busy locks, away/seen registry, name search |
| `TradeServer` | ServerScriptService | remotes, requests, sessions in MemoryStore, the bus, escrow, commit, recovery |
| `TradeItems` | BaseHatchery (BindableFunction) | `take(player, refs)` / `give(player, items)`: the only code that edits PetInventory / BaseData / EggInventory for trades, with no yields (atomic inside the server) |
| `TradeClient` + UI | StarterPlayerScripts | Trading menu, request pop-up, trade window (Check-UI) |

**`TradeItems` rules**
- **Item signatures:**
  - pet = id + name + KG + mutation key;
  - egg = kind + the EXACT KG (the stored number, written with full precision, e.g. `%.17g`; never rounded) +
    mutation key (empty when none). A bare-number entry and `{kg}` with no mutation are the same signature, so two
    eggs share a signature only when they're truly identical.
  - The offer-count check and `take()` use ONE shared signature function. KG must be finite and > 0.
- `take(player, sideOffer)` removes exactly the items in that side's session offer at the Phase 2 version. It's
  all-or-nothing:
  - each pet must match on id AND name, KG and mutation, found exactly once across BaseData + PetInventory;
  - each egg signature must have enough entries;
  - any mismatch removes nothing and fails (the round aborts).
  - On success it despawns the trader's own base pets and destroys the matching Tools ONLY in the trader's own
    Backpack and Character. Tools are destroyed by instance, exactly one per removed item, and other players' Tools
    are never touched. It returns exactly the item list it removed (signature data + where each came from).
  - Pet and egg Tools must have `CanBeDropped = false` (task 0 checks this), so no copy can lie in Workspace.
- `give()` adds items and never fails. Pets get new ids, checked unique against the receiver's own pets. Returned pets
  go back to the base if they came from there and a slot is free, otherwise to the inventory. Received pets are
  recorded in the Index (`PetIndex.record`).
- **One item lock per player:** `take()`, `give()` and EVERY other remover (sell, place egg, equip/unequip, equip
  best, hatch) run their check-and-remove with no yield in between. If any of them must yield, it holds a
  synchronous per-player `ItemLock`, and the others refuse while it's held. Each existing remover is audited for this
  before building (task 0).

**Data**
| Store | Key -> value | Use |
|---|---|---|
| PlayerData save (`PlayerData_v3`), new meta fields | `_session` (token of the server that owns the save, `nil` = nobody), `_ver` (write counter), `_wid` (id of the last write) | version-checked saves (invariant 1) |
| PlayerData fields (new) | `TradeEscrow` = JSON map `"<tradeId>#<round>"` -> {userId, side, items}; `SettledRounds` = the newest 200 settled `"<tradeId>#<round>"` keys; `TradeHistory` = last 20 | escrow, settle-once, History tab |
| DataStore `TradeLedger_v1` | `t_<tradeId>_<round>` -> {state = "committed" or "aborted", a, b, itemsA, itemsB, at} | THE permanent trade record |
| MemoryStore **SortedMap** `TradePresence_v1` (2026-10-30 build ruling: a HashMap ListItemsAsync scan measured ~21 page calls / ~500 quota units, a SortedMap read costs 1 unit per entry) | userId -> {job, name} (TTL 120 s, refreshed every 40 s) | ONLINE list. Removed on leave only if `job` is still this server |
| MemoryStore HashMap `TradeBusy_v1` | userId -> tradeId (TTL = the session's TTL, refreshed with it) | the "busy in trade" lock: busy = the lock exists. When a trade ends, its lock is deleted with a conditional `UpdateAsync` (only if it still holds this trade id). Before refusing a request as "busy", the server checks the lock's session and clears the lock if that session is done, cancelled or missing. The presence refresh does the same, so a lost release never leaves a player busy |
| MemoryStore HashMap `TradeSessions_v1` | tradeId -> session (TTL 15 min, refreshed on change) | live trade state |
| MessagingService topic `Trade_v1` | {to = userId, k = event, id}, ids only (payload limit 1 KiB) | wakes the other server. Sends are coalesced to at most 4 per second per trade, and a 2 s poll of active sessions is the backup. Handlers always re-read the session, so lost, doubled or out-of-order messages are harmless |
| OrderedDataStore `TradeSeen_v1` | userId -> last join os.time (integer), written by the player's own server after every successful load | "has played before" for your friends (AWAY rows) |
| DataStore `GiftInbox_v1` | userId -> list of {gift, purchaseId} | gifts for players who aren't in the gifting server (invariant 1). Nothing else ever writes into another player's save |

**Service budget** (MemoryStore's quota is shared by the whole game, so it's protected game-wide, not just per player)
- Each server keeps ONE cached ONLINE list, rebuilt at most every 10 s. Clients never trigger their own scan.
- Each viewer's rows are built on the SERVER: that ONLINE list plus the viewer's own AWAY friends. Server job ids and
  other internal fields are stripped. A client never receives strangers' AWAY status.
- Bad or rate-limited calls are refused before any service call.
- On a MemoryStore throttling error the server backs off (doubling waits up to 10 s). Trades pause and show
  "syncing..." instead of failing.
- The budget is measured in the two-server simulation (expected use per trade per minute), and the result is
  recorded in the plan.
- Names come from `Players:GetUserIdFromNameAsync` / `GetNameFromUserIdAsync` (pcall + cache). Headshots use
  `rbxthumb://type=AvatarHeadShot`, with no HTTP calls.
- **Every `UpdateAsync` callback is pure:** it only computes the new value. Side effects (take, give, kicks, messages)
  happen after the call returns, because Roblox may run a callback more than once.

**Session** (in `TradeSessions_v1`):
`{id, ver, round, phase = select|confirm|commit|done|cancel, a/b = {uid, name, job}, offer = {a = {...}, b = {...}},
ready = {a, b}, accept = {a, b}, escrowed = {a = {round, items}?, b = {round, items}?}, chat = {...}, changedAt}`

- `tradeId` is a new GUID for every trade and is never reused. `round` goes up every time Phase 2 starts.
- `ver` goes up on every offer/phase change (phase changes count for the idle timer; chat and refused actions don't).
- READY and ACCEPT are recorded only if the client's `ver` equals the session's current `ver`, checked inside the
  same MemoryStore `UpdateAsync`. Anything else is refused.
- **ACCEPT is refused on the server** until that player's own `escrowed[side]` is set for the current round (not only
  locked in the UI).
- `escrowed[side]` = {round, the exact list `take()` returned}. It's written only after that player's escrow SAVE
  succeeded, and it's identical to the entry in their save. It is cleared on every abort and at every Phase 2 start,
  and commit reads only current-round entries.
- Offer items are built by the OWNER's server from the owner's real data. The client only sends a reference: pet id,
  or egg kind + KG + mutation key.
- Busy locks: accepting a request takes the two locks one key at a time, lower userId first, each with a conditional
  `UpdateAsync` that fails if that player already has a live trade. On failure, every lock already taken is released,
  but only if it still holds this trade id.
- AWAY means: in `TradeSeen_v1`, no live presence entry, and a Roblox friend of the viewer. A presence entry that has
  expired counts as "not online".

## 6. Safety model
**Invariants (the tests check every one)**
1. **Version-checked saves (a save lock).** This closes stale-save dupes.
   - Loading a save is an `UpdateAsync` that writes a fresh `_session` token (a new GUID for EVERY load, never just a
     server id) and bumps `_ver` in the same step, so the newest load always takes over the save.
   - Every later write (autosave, leave, shutdown, on-demand, trade) is an `UpdateAsync` that writes ONLY if the
     stored `_session` is still this server's token and `_ver` equals the version this server last wrote; it then
     bumps `_ver`.
   - All of a player's writes on a server go through ONE queue (never two writes at once). A queued write takes its
     snapshot and the expected `_ver` when it RUNS, not when it was queued.
   - Each write also stores a unique write id (`_wid`). If a write errors or times out, the server never just
     re-sends it. It first reads the save back, with an `UpdateAsync` that changes nothing (never a cached `GetAsync`):
     - its own `_wid` is there: the write landed;
     - same `_session` and the `_ver` it expected: it didn't land, so it's sent again;
     - another server's `_session` or a different `_ver`: the save is lost.
     - Queue / throttling errors are retried and never count as "lost". Task 0 records the exact error codes/texts.
     - A read error is never counted as "missing" or "lost". It's retried.
   - If this server has really lost the save, it never writes that player again, cancels their trade (record
     "aborted"; their items settle through recovery on the new server) and kicks them with "You joined from another
     server".
   - The leave-save (and the save before a kick) writes `_session = nil`: the save is released.
   - A failed load = no saves and no trading that session (as today). The soft-restart lobby never loads or saves.
   - **Gifts to a player who isn't in this server** (`AddGiftedPass`) never touch their save. They go into
     `GiftInbox_v1[userId]` with one `UpdateAsync` that adds {gift, purchaseId} only if that purchaseId isn't there yet.
     - The recipient's own server takes the inbox in one step that adds the gift AND records the purchase id in the
       save: on every load, and every 60 s or on a MessagingService ping while they're online. Then it removes those
       entries from the inbox.
     - No writer ever takes over or edits a save another server owns.
   - **Robux receipts:**
     - The grant and its purchase id (`ReceiptIds`) are set in ONE synchronous step, so no save can ever hold one
       without the other.
     - `ProcessReceipt` returns `PurchaseGranted` only after the version-checked save containing both has succeeded,
       or when the loaded save already contains that id. Otherwise it returns `NotProcessedYet`, so Roblox retries.
     - `ReceiptIds` keeps the newest 200 (today: 50).
     - Audited in task 0.
   - **Every server-made teleport saves FIRST.** That covers Auto Reconnect's seal on the old server, and the old
     server's save before it sends players to the soft-restart lobby (the lobby itself never loads or saves). So the
     new server's takeover never throws away the last minute of progress.
     - Before that final save, an open trade in phase select or confirm is cancelled (rule 4 order).
     - A trade in phase commit is NOT cancelled (that would be refused): the save keeps the escrow entry, and the
       record decides on the next load.
   - Shutdown (BindToClose) does the same inside the shutdown window. Anything left unfinished is resolved by recovery
     on the player's next load.
2. **Escrow before commit.**
   - At Phase 2 start each server runs `take()` for its own player and stores the returned items in `TradeEscrow`
     under `"<tradeId>#<round>"` (a marker is written for both players, even with an empty offer).
   - It then saves through the queue. Only after that save succeeds does it write `escrowed[side] = {round, items}`.
   - If the escrow save is refused (lost save) or `take()` fails, the round aborts (rule 4 order). The other side
     settles back, and this side settles through recovery.
   - A player can't start ANY new escrow while they have ANY open escrow entry (any trade, any round). Rounds with a
     record are settled quickly (rule 6), so this never blocks a player for long.
3. **One record decides each round.** `TradeLedger_v1` key `t_<id>_<round>` goes from empty to "committed" OR to
   "aborted", never both.
   - **Every record write is one DataStore `UpdateAsync` whose callback writes only if the key is still empty.** The
     server acts only on the value that `UpdateAsync` returns, never on an earlier `GetAsync`, which may be cached.
   - Commit happens only when: phase confirm, both accepts == ver, BOTH `escrowed.a` and `escrowed.b` exist for this
     round (an empty item list is fine; a missing one never is), and the 5 s wait has passed on the committing server.
     This is checked inside the same session `UpdateAsync` that sets phase commit.
   - The record write itself is refused if either item list is missing.
   - The session moves to phase `commit` first (MemoryStore `UpdateAsync`), so BACK/cancel are refused from then on.
   - The record's `itemsA` / `itemsB` are copied from the session's `escrowed` lists (the exact `take()` results),
     never from the offer.
   - If a server sees phase `commit` with no record for 30 s, counted from the FIRST time THIS server saw phase commit
     (never from another server's clock), the committing server is assumed dead. Then this server may write the
     record itself, and the single-write rule keeps it safe.
4. **Escrow is released only by the record.**
   - Escrowed items go back to their owner ONLY after this round's record says "aborted", and go to the other player
     ONLY when it says "committed".
   - **Order for BACK / cancel / timeouts:**
     - First the session moves to cancel (or back to select) with a conditional `UpdateAsync`, which is refused in
       phase commit.
     - Only then is "aborted" written.
     - If that write finds "committed", the trade completes instead.
     - A failed escrow on either side, a player leaving and a lost save follow the same path.
   - **After any error on a record write, the server reads the record with an `UpdateAsync` that changes nothing and
     acts only on what it finds.** An error never counts as "aborted".
5. **Settle once.**
   - Each round settles exactly once per player, in ONE synchronous step with no yields:
     - committed: give the other side's items, plus a History entry;
     - aborted: give back their own escrowed items.
   - In the same step: delete the `TradeEscrow` entry and add `"<tradeId>#<round>"` to `SettledRounds`. Then save
     through the queue. The credit, the deleted entry and the settled marker are always in the same snapshot, so any
     save has all three or none.
   - A round already in `SettledRounds`, or with no escrow entry, is skipped.
   - `SettledRounds` keeps the newest 200 keys and is trimmed only in the same save that adds a newer one.
   - Recovery finds its side by comparing its own userId with the record's a / b (the entry also stores userId + side).
6. **Recovery on every load.** For every entry in the loaded `TradeEscrow`, read the record:
   - committed: settle (rule 5);
   - aborted: settle (rule 5);
   - empty: write "aborted" (rule 3), then settle with whatever the write returned.
   - This runs before `DataLoaded = true`, so no other system sees half-done data.
   - **The 30 s check** on a live server reads the record of each of its players' open entries:
     - Whenever a record EXISTS (committed or aborted), the entry is settled at once, whatever the session's phase.
     - Writing "aborted" into an EMPTY record is allowed only if the session is missing, expired, cancelled or back in
       phase select, or (rule 3) it has sat in phase commit for 30 s since this server first saw it.
     - A live confirm session with an empty record is left alone.
   - If recovery can't read the record (a service error), the player still loads. The entry stays in escrow (those
     items just aren't usable yet), and the 30 s check keeps retrying. Nothing is lost.

**The owner's exploit list -> the defence**
| Exploit | Why it fails |
|---|---|
| Skip / shorten the 5 s timers | Each server counts the 5 s on its own clock from when it saw that version/phase. Early READY/ACCEPT is refused |
| Freeze / pause / lag the trade to steal | Nothing moves until both accept the same version. A stuck trade times out (3 min) into "aborted", and a dead committer is finished by the other server after 30 s |
| Force completion without both accepting | Commit needs `accept.a == accept.b == ver` AND both escrow lists for this round, inside the session's `UpdateAsync`. ACCEPT itself is refused until your own escrow is saved. The client can't write the session |
| Change items after both accepted | In phase confirm/commit, offer changes are refused. Items are already in escrow, so they can't be sold or placed |
| Fake remote calls (other player's items, fake acceptances, fake completion) | Remotes act only for the caller. Items are looked up in the caller's own server-side data. There is no "complete" remote |
| Send fake item data / the same item 9 times | The client sends only a reference. Duplicates and over-count eggs are refused when added. `take()` is all-or-nothing, and the record uses what `take()` really removed |
| Modify another player's offer | Each player's server edits only that player's side of the offer |
| Sell / place an offered item before escrow | `take()` fails, which aborts the round through the record, so the other player's escrow returns safely. Nothing is lost or duped |
| Dupe by disconnecting / resetting / server shutdown | Escrow + record + recovery on load: the outcome is "completed once" or "everything returned" |
| Dupe by switching servers / a late save from an old server | Version-checked saves: the newest server takes over the save, and the old server can never write again |
| Dupe by lag / desync / two accepts at once | Session updates are serialized (`UpdateAsync`). The record can be written only once per round. Settle-once guard |
| Dupe a Robux purchase or a gift | Grant + purchase id set in one step and saved before PurchaseGranted. Gifts go through an inbox, never into a live save |
| Destroy another player's Tools / swap an egg for a lighter one | `take()` touches only the trader's own Backpack/Character, by instance. Egg signatures use the exact KG |
| Simultaneous trade requests / two trades at once | One busy lock per player (`TradeBusy_v1`, `UpdateAsync`, lower userId first, released only by its own trade). Escrow refuses a second open entry |
| Spamming remotes to break things | Rate limits per remote, refused before any service call. Bad input = refused, never an error that skips a check |
| Request-bombing / stalking players | 10 SENDs per 5 min, 3 pending per receiver, 30 s cooldown after a decline. One cached list per server. AWAY status is shown only to friends |
| Two alts burning the game's MemoryStore budget | 4 changes/s per player, 30 per 10 s per trade, 10-minute trade limit, coalesced messages, backoff on throttling |

**Remaining risk (accepted)**
- Roblox services being down: then trades can't start or complete, and items in escrow wait in the save until
  recovery runs.
- Nothing is lost or duped in that case. It's only delayed.

## 7. Failure and recovery
| Moment | What happens |
|---|---|
| Phase 1, someone leaves / X / timeout | Session cancelled, nothing was moved, the other player gets a toast |
| An offered item was sold/placed during Phase 1 | `take()` fails at Phase 2 start: round "aborted", the other side's escrow returns, and both go back to Phase 1 with empty offers and "X is no longer available" |
| Phase 2, someone leaves / BACK / X / timeout | Session moved to cancel/select first (refused in phase commit), then record "aborted", then each escrow settles once (pets go back where they were, or to the inventory if the base is full). In phase commit the record decides instead |
| Server crash after escrow, before the record | The next load (any server), or the other server's 30 s check (only once the session is gone or cancelled), writes "aborted" and settles the items back |
| Server crash after phase commit, before the record | The other server writes the record after 30 s; recovery follows the record |
| Server crash after "committed", before settling | The next load settles once (`SettledRounds`) |
| BACK, then a later round commits | Each round has its own escrow entry and settled marker, so the aborted round's items come back once and the committed round's items are delivered once |
| Player joins another server mid-trade | The new server takes over the save; the old server's next write is refused, so it cancels the trade. The record decides, and recovery on the new server follows it |
| MemoryStore / Messaging error mid-trade | No commit without a clean session update. The 2 s poll retries, and a 3-minute timeout ends in "aborted" |
| DataStore error writing the record | Read the record back and follow it. If it's still empty, retry every 2 s; after 60 s write "aborted" instead (the single-write rule decides which wins) |

## 8. Changes to existing scripts (each backed up first in `ServerStorage._Backup_Trading.Before`)
- **PlayerData:**
  - version-checked saves: `_session` / `_ver` / `_wid`, a load that takes over the save, one write queue per
    player, release on leave, and lost-save handling;
  - 3 new FIELDS (`TradeEscrow`, `SettledRounds`, `TradeHistory`);
  - recovery before `DataLoaded`;
  - the seal / `SavePlayerNow` / `AddGiftedPass` paths moved onto the same rules; the soft restart saves before it
    teleports.
  - This is the biggest change: every player's save goes through it, so it gets its own task and its own tests
    (including the Auto Reconnect tests) before any trading code.
- **BaseHatchery:** the `TradeItems` BindableFunction (take/give). Received pets count as found in the Index.
- **Receipts / ShopServer gifts:** `PurchaseGranted` only after a successful version-checked save with the grant +
  purchase id set in one step. Gifts to players not in this server go through `GiftInbox_v1` (invariant 1).
- **Task 0, an audit before any code** (results recorded in the plan):
  - every item remover (sell, place egg, equip/unequip, equip best, hatch) for yields between its check and its
    remove;
  - pet AND egg Tools have `CanBeDropped = false`, and every place/equip path checks the live server data, not the
    Tool;
  - `ProcessReceipt`'s return path;
  - the PolicyService field name;
  - the current save size against the 4 MB limit.
- **MenuController / AdminClient:** the Trading tile, and the Admin button below Rebirth + Index.

## 9. UI
- Check-UI skill only. Windows open through the MainMenu window system (one window at a time) and keep the 58 %
  width cap rule (wider on short phone screens). The request pop-up is a small card, not a window.
- **Mockups first:** the Trading tile + moved Admin button, the Trading menu (Players / History), the request pop-up
  and the trade window (Phase 1 and Phase 2). They're reviewed by a fresh reviewer (8.5+) and shown to the owner,
  and built only after the owner says yes.
- Phones: one layout, checked in Studio's Device emulator (tap targets ≥ 42 px; text that decides a trade, such as the Phase 2 rows, must be readable through LAYOUT, never a global text floor: the owner rejected text-floor restyles, see feedback-ui-look-owner-judges).

## 10. Testing (Studio, `TestFreshSave == true` before every Play)
- **`SaveLockTests`:**
  - a second "server" taking over a save: the old server's writes are refused, it stops saving and its trade is
    cancelled;
  - a slow autosave racing a newer write (it must be refused);
  - a write that errors after landing (read-back finds its `_wid`);
  - a gift to a player owned by another server (it waits, never overwrites);
  - a Robux receipt whose save is refused (it returns NotProcessedYet);
  - the existing Auto Reconnect tests still pass.
- **`TradeCoreTests` (pure):** every phase change; old ready/accept refused; the 5 s locks; the 9-item cap;
  duplicates and over-count eggs refused; a change clears ready/accept; BACK empties both offers; idle timeout; chat
  doesn't change ver.
- **Two-server simulation in one Studio server:** two `TradeServer` nodes with their own fake "job" ids and an
  in-memory bus. It **yields between every read and write**, so the race windows are exercised, not just end states.
  Real MemoryStore/DataStore `_Studio` stores and test players. It covers:
  - same-server and cross-server trades;
  - simultaneous accepts, BACK racing the commit;
  - an escrow failure on one side, a record write that errors after landing (simulated);
  - a dead committer;
  - a player taking over their save on the other node mid-trade;
  - BACK then a new round that commits (round 1 settles back once, round 2 delivers once);
  - the 30 s check never aborting a live confirm session, and settling at once when a record exists;
  - ACCEPT / commit with one side's escrow missing (must be refused);
  - a Robux grant with a crash between grant and save (no double grant);
  - a gift while the recipient is online on the other node (it arrives through the inbox, nothing is overwritten);
  - two players with the same pet id: trading one never touches the other's Tool.
- **Crash / recovery:** kill a node at each step (after escrow, after phase commit, after the record, before settling).
  Reload the players, then check **conservation**: the total pets + eggs across both players is the same before and
  after, every item is with exactly one owner, and no item appears twice.
- **Exploit tests:** wrong types, other players' pet ids, the same pet/egg added 9 times, eggs they don't have,
  NaN/inf KG, early READY/ACCEPT, old versions, remote spam, 10th item, full inventory, a trade with themselves, a
  player who hasn't played, an AWAY target, a second trade while one is open.
- **Budget:** the simulation counts MemoryStore / DataStore / Messaging calls per trade and per minute. The numbers
  go into the plan, and the build stops if a normal trade costs more than planned.
- **UI:** phone emulator pass; the window survives a respawn; other menu tiles are locked during a trade; a fresh
  reviewer (8.5+) on the final screens.
- **A final security review of the finished code** by a fresh reviewer, against this section's invariants and the
  exploit table.

## Out of scope
- Trading money, potions, passes or gear.
- Free-text chat.
- A trade Settings tab (requests from friends only / off).
- Requests that wait for AWAY players.
- Reserving offered items during Phase 1: a sold/placed item just aborts the round safely.
