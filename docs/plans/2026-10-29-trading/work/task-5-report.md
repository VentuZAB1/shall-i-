# Task 5 report: `TradeServer` part A (requests, sessions, phases, the bus)

**Status: DONE_WITH_CONCERNS.** TradeSimTests.partA is 18 pass / 0 fail (the 15 brief tests + 3 extras), two full runs
in a row on the final code, with 0 MemoryStore errors and 0 retries. A 5-bug mutation check was caught 5/5. The concerns
are hand-off notes for Task 6 (part B) and Task 7 (UI), not defects in part A.

Builder: Opus, 2026-10-30. Studio `3bf21205-caff-490e-a927-3bd9f0097311`.
- I started and stopped every Play session myself (7), and checked `TestFreshSave == true` in Edit right before each.
  TestFreshSave is left `true`.
- I never saved or published. HttpService is off, so all sources were written through MCP (`multi_edit`).
- No existing script was changed, so nothing new went into `ServerStorage._Backup_Trading.Before`. TradeConfig is
  unchanged (4,718 chars, the same as after Task 4).

## Scripts
| Path | Class | Size | What it is |
|---|---|---|---|
| `ServerScriptService.TradeNode` | ModuleScript (new) | 69,740 chars | all of the trade server's logic, as a node with an injectable env |
| `ServerScriptService.TradeServer` | Script (new) | 3,026 chars | creates `ReplicatedStorage.Trade` (Request / Action / Query / Push) and `ServerStorage.TradeRecoveryHook`, starts the default node on the real services |
| `ServerStorage.TradeSimTests` | ModuleScript (new) | 48,270 chars | `.partA(player, verbose?, only?)`: the two-node simulation |

None of them has a CollectionService tag. `ReplicatedStorage.Trade` and `ServerStorage.TradeRecoveryHook` are created at
runtime by TradeServer (they don't exist in Edit), following the codebase rule that the server script that owns remotes
creates them.

**To run the suite:** Play, Server datamodel, TestFreshSave session. It takes about 80 s, which is longer than one MCP
call, so run it in a thread and poll for the result:
`task.spawn(function() workspace:SetAttribute("_TradeSim", require(game.ServerStorage.TradeSimTests).partA(game.Players:GetPlayers()[1], true)) end)`

## Remote API (`ReplicatedStorage.Trade`)
Every call is `remote:InvokeServer(op, ...)` and returns `ok, data | reason` (the reason is a toast text).
- Each remote takes only its own ops (anything else returns "Bad request"), and only from a real Player, acting for the
  caller only.
- The order of checks:
  1. the kill switch ("Trading is off" for every op);
  2. types and sizes (bad input is refused first and never reaches a service);
  3. the per-player limiter;
  4. the work.
- One player's calls run one at a time.

| Remote | Op, args | Returns |
|---|---|---|
| **Request** (RF) | `"send", uid` | `true, {id, to = name, toUid, expiresIn}` / `false, reason` |
| | `"respond", reqId, accept: boolean` | `true` / `false, reason` (accept = the trade opens through Push) |
| | `"cancelRequest", reqId` | `true` / `false, "No request to cancel"` |
| **Action** (RF) | `"add", ref`, where ref = `{t = "pet", id}` or `{t = "egg", kind, kg, mutKey?}` (kg = the exact number from the client's own EggInventory) | `true` / `false, reason` |
| | `"remove", i` (an index into the view's `mine`) | same |
| | `"ready", ver` / `"accept", ver` (the `ver` from the latest view) | same |
| | `"back"` / `"cancel"` | same |
| | `"chat", n` (1-6, `TradeConfig.PHRASES`) | same |
| **Query** (RF) | `"list"` | `true, {rows = {{uid, name, status = "ONLINE" or "AWAY"}}, why = reason or nil}` (why = why YOU can't trade: the line under the list) |
| | `"search", text` | `true, rows` / `false, reason` (TradePresence's texts: BAD_TEXT, "@x isn't online", "That's you!", LATER_TEXT) |
| | `"history"` | `true, list` (the player's `TradeHistory`, at most HISTORY_MAX, newest first; part B writes the entries) |
| | `"state"` (extra, see ruling 11) | `true, {trade = view?, requests = {{id, from, fromUid, expiresIn}}, outgoing = {id, to, toUid, expiresIn}?}` |
| **Push** (RE, server to client) | `kind, data` | the schema below |

**Refusal reasons (exact texts):**
- kill switch and input:
  - "Trading is off"
  - "Bad request" (wrong remote / op / type)
  - "Bad player" (send uid)
  - "Bad item" (ref / index)
  - "Bad phrase"
- limiter:
  - "Slow down"
  - "Too many requests, wait Ns" (10 per 5 min)
  - "Wait Ns" (the same phrase, or the pair cooldown after a decline)
- your own rules:
  - "Your items are still loading"
  - "Finish the tutorial first"
  - "Reconnecting..."
  - "Trading isn't allowed in your country"
  - "You can't trade with yourself"
  - "You're already trading"
  - "You already sent a request"
  - "Your inventory is full"
- the other player:
  - "@B isn't online right now" ("That player ..." when the name is unknown)
  - "@B has too many requests"
  - "@B is already trading"
  - "@B can't trade right now"
  - "@B's inventory is full"
  - "Wait a moment before asking @B again"
- trade state:
  - "That request has expired"
  - "You're not trading"
  - "You don't have that pet" / "You don't have that egg"
  - "Syncing... try again" (MemoryStore error or backoff)
- plus every TradeCore reason ("Wait 5s", "Offer changed", "Offers are locked", "Max 9 items", "Securing items...",
  "Trade timed out", ...).

## Push payload schema (`Push:FireClient(player, kind, data)`), for Task 7
**`"trade"`** is the viewer's view, sent whenever it changes (deduplicated) and always once more when the trade ends:
```
{
  phase   = "select" | "confirm" | "commit" | "done" | "cancel",
  ver     = number,        -- pass it back to ready(ver) / accept(ver)
  round   = number,        -- the Phase 2 round (0 before the first)
  side    = "a" | "b",     -- your side
  you     = {name, uid}, them = {name, uid},       -- uid for rbxthumb headshots
  mine    = {card...},     -- your offer, in order (remove(i) uses this index)
  theirs  = {card...},
  total   = {mine = $/s, theirs = $/s},
  summary = {give = {pets, eggs}, get = {pets, eggs}, diff = total.theirs - total.mine},   -- the Phase 2 line
  ready   = {you = bool, them = bool},   -- for THIS ver
  accept  = {you = bool, them = bool},
  secured = {you = bool, them = bool},   -- escrow saved for this round; ACCEPT needs yours ("Securing items...")
  chat    = {{you = bool, name = "@x", p = 1..6, text = "Deal?"}...},   -- the last 8, oldest first
  syncing = bool,          -- a change on its way / MemoryStore backing off: show "syncing..."
  readyIn = seconds,       -- phase select only: what's left of the 5 s READY lock on THIS server's count
  acceptIn = seconds,      -- phase confirm only: the 5 s ACCEPT lock
  endsIn  = seconds,       -- select / confirm: until the idle (3 min) or total (10 min) limit
  closed  = true, why = text,   -- only once the trade is over (phase done / cancel): show `why`, close the window
}
pet card = {t = "pet", name = <creature key, for the picture>, display = "Abyss Weaver", kg = <exact number>,
            mut = {"UFO", ...}?, ps = <$/s, CreatureConfig.petIncome>, id = <pet id: YOUR cards only>}
egg card = {t = "egg", kind = "WoodEgg", display = "Wood Egg", kg = <exact>, mut = {...}?}
```
- The countdowns are seconds LEFT, so the client counts them down on its own clock from when the push arrived.
- A view never contains job ids, sigs, `from`, the other player's pet ids or any other internal field. The tests check
  this against the JSON of every push.
- **Why texts:**
  - "You cancelled the trade" / "@B cancelled the trade"
  - "@B left the game", "@B is reconnecting"
  - "The trade timed out", "Trades can last 10 minutes at most"
  - "Trading is off"
  - "Trade cancelled, nothing was moved" (the part A stand-in)
  - "Trade complete!" (part B adds gave / got)
  - "Trade cancelled" (anything else)
- **A trade that never had a full session** (it broke, or never started) is closed with
  `{phase, closed = true, side, mine = {}, theirs = {}, them = {name, uid}, why}`.

**The other kinds:**
- `"request"` = `{id, from = name, fromUid, expiresIn}`: the bottom-right pop-up. Answer it with `respond(id, ...)`.
- `"requestGone"` = `{id, why}`, where why = expired | declined | accepted | cancelled | trading | replaced | off.
- `"outgoing"` = `{id, to = name, toUid, expiresIn}`: your SEND was delivered.
- `"outgoingGone"` = `{id, why}`, where why = accepted | declined | expired | cancelled | trading | left | refused | off.
- `"toast"` = `{text}`. Examples: "@B declined", "@B didn't answer", "@B is already trading", "@B went back - add your
  items again", "@B's inventory is full - add your items again".

## TradeNode env interface
`TradeNode.new(env) -> node`. Every field is optional, and the defaults are the real services.

| env field | Default | Notes |
|---|---|---|
| `jobId` | `presence.jobId()` | written into the session's `a.job` / `b.job` |
| `bus` | `TradeNode.messagingBus(stores.Topic)` | `{publish(msg), subscribe(fn(msg)) -> {Disconnect}}`. The real one retries SubscribeAsync with backoff |
| `players` | `TradeNode.playerList(true)` | `{get(uid), all(), add(folder), remove(folder), onJoin(fn), onLeave(fn)}`: real Players and/or virtual Folders (UserId / Name / item attributes) |
| `memory` | MemoryStoreService | `GetHashMap(stores.Sessions)` only |
| `presence` | the TradePresence module | `jobId, onlineList, rowsFor, search, takeBusy, releaseBusy, refreshBusy, configure`. The node calls `presence.configure({isSessionLive = node.isSessionLive})` |
| `items` | `ServerStorage.TradeItems:Invoke` | `items(op, player, ...)`: part A uses "describe" and "count" |
| `policy` | `TradeNode.policyChecker()` | `fn(player) -> allowed`. Cached per player; an error = not allowed (retried after 60 s); virtual players use the `IsPaidItemTradingAllowed` attribute |
| `push` | the Push RemoteEvent (real Players only) | `fn(player, kind, data)` |
| `clock` | `workspace:GetServerTimeNow` | the trade clock: locks, timeouts, limiter windows, cooldowns, request expiry |
| `hooks` | `TradeNode.partAHooks` | see below |
| `enabled` | `TradeConfig.ENABLED ~= false` | the kill switch |
| `stores` | `TradeConfig.stores()` | |
| `ledger`, `saves` | (none) | part B: kept on `node.env` |
| `quiet` | false | no warnings |

**Node methods:**
- `start()` / `stop()`
- `handle(player, op, ...)`, `remote(remoteName, player, op, ...)`
- `isSessionLive(tradeId)` (a dot function; it raises on a read error, which TradePresence counts as live)
- `poll()`, `cancelFor(player | uid, kind)`, `recover(player)`
- `tradeOf(uid)`, `sessionOf(uid)`, `pendingFor(uid)`, `stats()`, `setPoll(on)`
- `standInEscrow(s, side)`, `abortRound(s, code)`, `finishRound(s, outcome)`

**Fields the node adds to the session** (TradeCore keeps extra fields):
- `rev`: +1 on every write, so a stale read is ignored (ruling 5);
- `pol = {a = true, b = true}`: both passed PolicyService on their own node;
- `cnt = {a = {p, e}, b = {p, e}}`: each side's pet / egg counts, written by that side's node (the "@B's inventory is
  full" check, ruling 3);
- `backBy`, `backWhy`: who / why Phase 2 went back.

**Cancel codes (`s.why`):** `cancel:<side>`, `left:<side>`, `reconnect:<side>`, `room:<side>`, `rules:<side>`, `idle`,
`total`, `off`, `busy`, `aborted`, `gone` / `broken` (markers).

**Bus messages** carry ids and codes only. The largest measured was 154 bytes.

| k | Meaning | Fields |
|---|---|---|
| `rq` | request | `{to, id, f = sender, n = sender's name}` |
| `ra` | answer | `{ok, w, n = receiver's name, f = receiver}` |
| `rx` | the sender cancels | `{f}` |
| `rg` | the receiver drops it | `{w}` |
| `ac` | accept | `{t = tradeId, f}` |
| `ar` | the accept answer | `{ok, w, j = job id, n, cp, ce}` |
| `s` | the session changed | `{to, id}` |

## Part B hook points (`TradeNode.partAHooks`, called as `hook(node, ...)`)
| Hook | When | Part A stand-in | Part B fills in |
|---|---|---|---|
| `onEnterConfirm(node, s, side)` | this node's OWN player first sees Phase 2 of `s.round` (once per round per side), in its own thread | the entry checks again (`ownRules` + room), then `setEscrowed` with the offer as it stands. **No items move.** A failure goes to `node:abortRound(s, "rules:x" or "room:x")` | the entry checks, then `take()`, then the TradeEscrow entry, then the queued save, then `setEscrowed(..., now)`. On a failure, `abortRound` |
| `onBothAccepted(node, s)` | THIS node moved the session to phase commit (the second ACCEPT; `toCommit` is chained in the same UpdateAsync) | `node:finishRound(s, "aborted")`: never a fake completion | the record (written only if empty, built with `TradeCore.record`), `finish`, settle, the dead-committer rule |
| `onCancelInConfirm(node, s, why)` | THIS node moved a session out of confirm (BACK, cancel, a timeout, a leave, a failed entry). `s` = the new session, `s.round` = the round that ended | nothing | the round's "aborted" record (rule 4 order: the session already moved) and a "committed" found instead |
| `onSessionSeen(node, s, side)` | every fresh copy of a session for an own player (the poll, a bus message, a write), spawned | nothing | the 30 s check (`node:sessionOf(uid)`; `commitSeenAt` lives in the record), settling once a record exists |
| `recover(node, player)` | synchronously, from `ServerStorage.TradeRecoveryHook` (PlayerData, before DataLoaded) | nothing | invariant 6 recovery |

- The other helpers part B can call: `node:cancelFor(player, "reconnect" or "left")` for the teleport seal and shutdown
  (it cancels in select / confirm; commit is refused, so the record decides), plus `node:abortRound` and
  `node:finishRound`.
- **This node's own clock stamps** are on its record: `seenVerAt`, `confirmSeenAt` and `commitSeenAt`.

## Tests (`ServerStorage.TradeSimTests.partA`)
**Setup:**
- Two `TradeNode`s, each with its own `TradePresence.new` instance and fake job id `simA-<guid>` / `simB-<guid>`.
- An in-memory bus with a delay of 0.05 s, plus drop and inject. It JSON round-trips every message, like
  MessagingService, and every subscriber gets every message.
- The real `_Studio` MemoryStore, through a wrapper that yields before every call (and can serve a stale or empty read
  on demand).
- The real `ServerStorage.TradeItems`.
- A fake trade clock that only moves when a test advances it.
- Node A hosts the real test player plus virtual senders A2-A4; node B hosts the virtual peers B and C.
- The real player's PetInventory / EggInventory are swapped for test items and put back in teardown. I checked
  afterwards: no test folder left, the original items back, no busy lock left.

**Brief tests:**
- `request_cross_node`: SEND, the 2 s ack, the pop-up, ACCEPT; one session with both job ids; both busy locks; the bus
  fields allow-listed and under 1 KiB; no job ids or sigs in any push; cancel; locks released.
- `request_ack_timeout`: no node, so refused after about 2 s. A slow bus (1.2 s each way) is refused in time, and the
  late yes cancels B's pending request through `rx`.
- `three_pending_max`: the 4th request is refused; 30 s later the pop-ups expire and the senders get "didn't answer".
- `send_limits`: bad types are free; 1 per 3 s; a refused SEND (to yourself) still counts; 10 per 5 min; one outgoing
  request at a time.
- `decline_cooldown`: the toast and the 30 s pair wait, on the sender's node AND on the receiver's node (an injected
  request).
- `self_trade_refused`: SEND to yourself; a forged "B to B" bus request is ignored; `newSession` refuses.
- `tutorial_refused`: the sender's own rule, the receiver's rule at the request, and the re-check at accept on EACH node.
- `policy_refused`: the same three, for PolicyService (node A's real PolicyService behind a test override; B's from its
  attribute).
- `offer_sync_cross_node`: a pet, an exact-KG egg, a mutation, a remove; a dropped `s` message is synced by the 2 s poll;
  no ids on the other side's cards; someone else's pet id is refused.
- `ready_lock_resets`:
  - an early READY gets "Wait 5s"; any change clears both READYs; an old ver gets "Offer changed";
  - **each node counts the 5 s from its own sighting**: A's node sees B's change 3 s late, so B can READY and A gets
    "Wait 3s";
  - both READY leads to Phase 2 on both nodes, with both sides secured; offers are locked; ACCEPT waits 5 s;
  - BACK empties both offers, clears everything, toasts A and calls `onCancelInConfirm` on B's node;
  - round 2 leads to the commit hook on the committing node (phase commit, round 2), with 4 `onEnterConfirm` calls in
    total; the stand-in closes both windows.
- `change_rate_limits`: 4 changes a second per player (the local limiter); refused calls count; bad refs (NaN / inf KG,
  wrong t) are free and never reach MemoryStore; TradeCore's 30 per 10 s per trade, with both players just under 4 a
  second: exactly 30 accepted, then "Slow down".
- `chat_limits`: 1 per 1.5 s and the same phrase once per 5 s, both refused before any write; chat changes neither ver
  nor changedAt; the other side sees "@name: phrase"; bad phrases; the last 8 lines on both nodes.
- `idle_and_total_timeout`: 179 s is not cancelled, 181 s is (`why = "idle"`, both windows close, lock released). The
  10-minute cap holds with changes every 170 s: a change after it gets "Trade timed out", then `why = "total"`.
- `second_trade_refused`: B's other pending requests fail ("@B is already trading") when B accepts one; there's no
  second trade either way; the busy lock holds across servers.
- `kill_switch_refuses`: all 14 ops get "Trading is off" with no service call; an incoming bus request is refused; the
  open trade is cancelled (`why = "off"`); pending requests go; the real remotes exist; each remote refuses another
  remote's op and a non-Player caller.

**Extras:**
- `request_same_node`: both players on node A; changes show at once with no bus messages.
- `query_ops`: list / search / history / state, their limits, and no job ids in the rows.
- `stale_read_ignored`: a late older copy and one empty read don't roll back or end a live trade (ruling 5).

### RED (before TradeNode existed)
```
TradeSim partA: 0 pass / 17 fail
FAIL request_cross_node [harness: ServerStorage.TradeSimTests:124: ServerScriptService.TradeNode is missing]
FAIL request_ack_timeout [harness: ... TradeNode is missing]
FAIL three_pending_max [harness: ... TradeNode is missing]
FAIL send_limits [harness: ... TradeNode is missing]
FAIL decline_cooldown [harness: ... TradeNode is missing]
FAIL self_trade_refused [harness: ... TradeNode is missing]
FAIL tutorial_refused [harness: ... TradeNode is missing]
FAIL policy_refused [harness: ... TradeNode is missing]
FAIL offer_sync_cross_node [harness: ... TradeNode is missing]
FAIL ready_lock_resets [harness: ... TradeNode is missing]
FAIL change_rate_limits [harness: ... TradeNode is missing]
FAIL chat_limits [harness: ... TradeNode is missing]
FAIL idle_and_total_timeout [harness: ... TradeNode is missing]
FAIL second_trade_refused [harness: ... TradeNode is missing]
FAIL kill_switch_refuses [harness: ... TradeNode is missing]
FAIL request_same_node [harness: ... TradeNode is missing]
FAIL query_ops [harness: ... TradeNode is missing]
```

**What the first implementation run caught (14/17):**
- 2 test-order bugs. A second SEND at the same fake instant hit the 1-per-3 s limiter before the rule under test, so the
  fix was to advance the clock.
- 1 real node bug. A backup poll read that started before a newer write landed after it, and rolled the node's copy of
  the session back (a stale ver in the view, and `localSeenAt` re-stamped later). The fix is the `rev` guard.
- I wrote `stale_read_ignored` for that bug. RED with the guard disabled: `FAIL stale_read_ignored [B went back to an
  old copy: 2]`.
- One later run flaked once (an add refused "Syncing...", `syncing = true` in a view) after back-to-back Studio runs. The
  node behaved as designed: it backs off on a MemoryStore error. The harness now retries an op up to 3 times only on that
  exact reason, and counts the retries in the verbose stats (0 in the final runs).

### GREEN (final code, `partA(p, true)`; the run before it was also 18/18)
```
TradeSim partA: 18 pass / 0 fail
ok   request_cross_node [47 asserts]
ok   request_ack_timeout [8 asserts]
ok   three_pending_max [13 asserts]
ok   send_limits [28 asserts]
ok   decline_cooldown [10 asserts]
ok   self_trade_refused [3 asserts]
ok   tutorial_refused [11 asserts]
ok   policy_refused [9 asserts]
ok   offer_sync_cross_node [24 asserts]
ok   ready_lock_resets [40 asserts]
ok   change_rate_limits [24 asserts]
ok   chat_limits [31 asserts]
ok   idle_and_total_timeout [21 asserts]
ok   second_trade_refused [15 asserts]
ok   kill_switch_refuses [29 asserts]
ok   request_same_node [11 asserts]
ok   query_ops [13 asserts]
ok   stale_read_ignored [13 asserts]
node A {"memErrors":0,"memReads":77,"busSends":119,"pushes":188,"memWrites":68,"busIn":103}
node B {"memErrors":0,"memReads":87,"busSends":101,"pushes":173,"memWrites":51,"busIn":126}
memory calls {"nilNext":false,"writes":119,"staleNext":false,"reads":164}, bus sends 220, biggest message 154 bytes, sync retries 0
```

### Mutation check (5 bugs planted at once in the live module, the 5 owning tests run, the source restored and re-verified)
```
TradeSim partA: 0 pass / 5 fail
FAIL ready_lock_resets [A READY counted from A's sight: nil]        <- localSeenAt dropped from READY
FAIL kill_switch_refuses [send: You're already trading]              <- kill switch removed from handle()
FAIL send_limits [1 per 3 s: {"id":...,"to":"SimPeerB",...}]         <- the limiter never counts
FAIL three_pending_max [{"id":...,"to":"SimPeerB",...}]              <- no PENDING_MAX check
FAIL second_trade_refused [{"id":...,"to":"Santrinio",...}]          <- a request to a busy player accepted
```

### Live checks (the real TradeServer, same Play session)
- **Client-side calls on the real remotes:**

  | Call | Result |
  |---|---|
  | `state` | `true {"requests":[]}` |
  | `list` | `true {"rows":[]}` (solo: the viewer is never listed) |
  | `list` again | `Slow down` |
  | `history` | `true []` |
  | `add` on Request | `Bad request` |
  | unknown op | `Bad request` |
  | `chat` with no trade | `You're not trading` |
  | `chat "x"` | `Bad phrase` |
  | send to self | `You can't trade with yourself` |
  | the next send | `Slow down` |

- **The real MessagingService path:** a request published on `Trade_v1_Studio` was picked up by the default node, which
  pushed `request {"id":"live-test-1","from":"LiveTester","expiresIn":30,"fromUid":123}` to the real client and published
  `ra {"ok":true,...}`. Then `respond(..., false)` produced `requestGone`.
- The console was clean (no TradeNode / TradeServer warnings or errors).

## Rulings I made
1. **Limiter semantics.**
   - Types are checked first, and bad input is free.
   - A call the limiter lets through counts, even when it's refused later (spec: "refused calls count").
   - A call the limiter itself refuses is NOT counted. It cost nothing, so it doesn't extend the lockout. Under spam, the
     service calls still never exceed the limit.
2. **Unlisted limits.**
   - respond / cancelRequest / ready / accept / back / cancel / state share a "button" limiter at `CHANGE_PER_PLAYER`
     per `CHANGE_PLAYER_WINDOW`.
   - history uses `LIST_GAP`. TradeConfig has no history gap, and I didn't re-type the number.
3. **Room at READY.**
   - Your own room comes from your live data.
   - The other side's room comes from `s.cnt[other]`: the counts their node writes with each of its own changes, and in
     the accept answer.
   - Refused only when the trade would RAISE a count to over the cap. Someone already over 150 can still give items
     away. Equipped pets given away don't free room.
   - The Phase 2 entry re-checks room and every rule on each player's own node (in the stand-in). Part B must keep doing
     this before `take()`.
4. **Bus payloads.** "Ids only" was read as "no session data".
   - Messages carry public usernames, the accepting node's job id and its pet / egg counts (`ar`), all short. 154 bytes
     max.
   - A request message carries no policy flag: it only exists if the sender's own node passed every check, and accept
     re-checks both. The session carries `pol`.
5. **A stale read guard.**
   - Every write bumps `s.rev`, and a node ignores any copy older than the one it holds.
   - A single "missing" read after a session existed is read again before the trade ends. A session that's broken (not
     merely missing) ends at once and gets a cancelled marker, so the other node ends too.
6. **Cancelled markers.** A trade that was accepted but never started (or broke) gets `{id, phase = "cancel", why}`
   written only-if-empty. It can then never start later. The session create is only-if-empty too.
7. **PolicyService.** A success is cached per player for the session. An error = not allowed, asked again after 60 s.
   Warmed on join.
8. **Part A stand-ins** never fake a completion: both accepted leads to `finish("aborted")`. If part A were ever live
   alone, an exploiter could at most open and cancel trades. Nothing can move.
9. **Same-server.** A message for a player on this node is delivered locally (`task.defer`): the same handlers, no
   network.
10. **Small flow choices.**
    - Accepting a request cancels your own outgoing request.
    - When a trade starts, the accepter's other pending requests fail with "trading".
    - A decline sets the pair cooldown on both nodes.
    - A sender's newer request replaces their older one on the receiver (their server lost track of it).
    - Back to Phase 1 records `backBy` / `backWhy`, so the other player gets a toast.
11. **The extra `state` op** on Query is for the client starting up, or rebuilding the window after a respawn.
12. **The Reconnecting seal and the kill switch** have poll-based backstops (at most POLL s late).
    - Reconnecting cancels a select / confirm trade.
    - The kill switch cancels open select / confirm trades (`why = "off"`) and drops requests. Commit goes on.

## Concerns / hand-off notes
1. **For Task 6: the teleport seal must cancel explicitly before AutoReconnect's final save** (spec invariant 1), for
   example by calling `node:cancelFor(player, "reconnect")` from the seal path. Part A's poll backstop can be up to 2 s
   late.
2. **A player who leaves in phase commit:** the node drops its local record (the cancel is refused there). Part B's
   record / recovery decides, as the spec says.
3. **No cross-server liveness check.** If the other server crashes (so it never sends its leave-cancel), the trade ends
   by the 3-minute idle timeout (spec section 7). After that, the dead lock is cleared through `isSessionLive`.
4. **MessagingService budget.** The "session changed" sends are capped at 4/s per trade, and the offer limiter keeps
   real use far lower. Task 6's `budget` test should still measure publishes per server against 150 + 60 x players a
   minute. The simulation counters are a starting point: the whole 18-test run (about 3 min) was 164 reads, 119 writes
   and 220 bus messages.
5. **`onSessionSeen` is spawned on every fresh copy** (the poll every 2 s, every bus message). Part B's handler must stay
   cheap or debounce itself.
6. **The test knobs** `setPoll` / `tradeOf` / `sessionOf` / `pendingFor` / `stats` exist on every node (harmless live;
   part B tests will need them too).
7. **The live `list` in solo Play returned no rows** (correct: the viewer is never listed). The row content is covered by
   `query_ops` (rows have no job ids) and by TradePresenceTests.

---

# Fix round 1 (2026-10-30)

**Status: DONE.** Every listed item is fixed or covered.
- `partA` is now **28 pass / 0 fail**: the 18 earlier tests plus 10 new ones.
- Each new test fails with its fix switched off (the mutation spot check: 10/10).
- Not changed, per the rulings: I2 (rejected), M1 / M2 / M7 / M8 (accepted as built), I5 / M14 / M15 (carried to part B;
  the hooks are unchanged).
- Housekeeping:
  - I started and stopped every Play session myself (4 this round), with TestFreshSave == true checked in Edit right
    before each one. TestFreshSave is left true.
  - No save, no publish. No existing script changed, so no new backups.
  - `TradeServer` is unchanged.

## What changed
**`ServerScriptService.TradeNode`** (now 72,749 chars, 1,759 lines):

| Item | Lines | Change |
|---|---|---|
| **I1** | 1491-1501 (`isSessionLive`) | an `"expired"` session counts as LIVE, so its busy locks are never cleared by TradePresence. Spec 5 clears a lock only for a session that's done, cancelled or missing. The normal expiry cancel (`handleSession` -> `cancelTrade`) ends it and `endLocal` frees both locks. If both nodes are gone, the TTL frees them |
| **I3** | 1099-1151 (new `CHECK` table + `limited`) | each op's type / size check and limiter, with no yield and no service call. Every op body (1153+) lost its own check / `allow` lines; a source scan finds 0 `allow` calls left in the OPS |
| | 1472-1483 (`node:handle`) | runs the kill switch, then `CHECK[op]`, then the queue |
| | 583-602 (`oneAtATime`) + 422 (`waiting`) | one call runs and at most ONE waits. Any further call answers "Slow down" at once, with no wait loop |
| | 27-31 | the header comment says the same |
| **M3** | 1231-1240 (`giveUp` in `respond`) | now `cancelSession(t, code)`: the cancelled marker if nothing is there, else the normal TradeCore cancel. A create write that errored after landing can no longer leave an open session with no receiver record (it used to be `poison`, which refuses a live session) |
| **M4** | 857-892 | the body is now `refreshOnce(id)`. `refresh` runs it in `pcall`, counts and warns an error (`stats.errors`, through `oops`), and resets `reading[id]` on every path. The next poll reads again |
| **M5** | 995-1010 (the `rq` handler) | the cap is counted first: live requests from OTHER senders. A "full" refusal returns before any change; only then is the sender's own older request replaced |
| **M10** | 446-450 (`itemError`), 427-428 (`stats.itemErrors`, `stats.errors`) | a TradeItems error is counted and warned through the one-a-minute `oops` throttle |
| | 1300-1308 (`OPS.add`) | a `describe` error, or a `count` error / non-table, calls `itemError`. Both still fail closed (refused; owned = 0) |
| | 245-265, 713 / 721 | `income` returns `0, err` on an error, and `card(it, own, onError)` reports it from `viewOf` |

**`ServerStorage.TradeSimTests`** (now 63,063 chars, 1,418 lines):
- **Harness:**
  - `T.slowMemory` 105-141: `counts.errAfterWrite` (the next UpdateAsync lands, then errors).
  - `H.now` 161-172: `H.boomIn = "<function name>"` makes the next clock read inside that node function error once,
    found with `debug.info(level, "n")`.
  - 216-224: an `items` env wrapper with `H.itemsBoom` (the next describe / count errors).
  - `H.reset` 362-370 clears these flags and every virtual player's `Reconnecting`.
- **New tests** (NAMES 419-422; helpers `hook` / `fullInventory` 1066-1083):
  - `expired_session_keeps_lock` 1085: both polls off, the clock pushed past the idle limit. `isSessionLive` stays true,
    another trade can't take the lock, and the lock stays the trade's. Then the normal cancel frees both locks.
  - `call_queue_capped` 1117: 50 adds fired at once. At most 2 are still running after the spawn (checked by
    `coroutine.status`), at least 48 answer "Slow down" synchronously, and at most 2 service writes happen.
  - `offer_caps_refused` 1140, through the remote path:
    - the same pet twice gives "Already in offer";
    - 9 items are accepted, then the 10th gives "Max 9 items" (a virtual player holding 10 pets);
    - P owns two identical 10 KG eggs: 2 cards, and the 3rd gives "You don't have more of that egg";
    - an egg not owned gives "You don't have that egg".
  - `ready_room_refused` 1175: B (virtual) holds 150 pets. P's READY gives "@SimPeerB's inventory is full" and B's
    READY gives "Your inventory is full". Once B gives a stored pet back, P's READY passes.
  - `entry_recheck_aborts` 1200: B readies while fine, then (a) fills to 150 pets, (b) loses PolicyService. P's READY
    starts Phase 2, B's node's entry check aborts the round (offers emptied, back to select), P gets the toast, and
    `onCancelInConfirm(room:b / rules:b)` is called on B's node.
  - `reconnecting_paths` 1237:
    - the own-rule refusal ("Reconnecting...") and the other node's refusal;
    - the poll's seal ends a Phase 1 trade (`why = "reconnect:b"`, "@SimPeerB is reconnecting");
    - the poll's seal ends a Phase 2 trade, with `onCancelInConfirm(reconnect:b)`.
  - `giveup_cancels_landed_session` 1275: the receiver's session-create write lands, then errors. The session ends
    cancelled, the sender's node drops its half-open record, and no lock is held.
  - `refresh_survives_error` 1299: an injected error inside B's `handleSession`, during a poll. B only learns by polling
    (`s` messages to B dropped), and B's next poll still shows A's new item.
  - `full_keeps_older_request` 1317: A2's old request (expired, not swept) plus 3 other live ones, then a new A2
    request is refused "full". A2's older request is NOT removed: no `requestGone`.
  - `item_errors_counted` 1344: an injected describe error, then a count error. Both adds are refused ("You don't have
    that pet"), `itemErrors` goes +1 each time, and nothing is added.

## RED (the 10 new tests against the unchanged node)
```
TradeSim partA: 4 pass / 6 fail
FAIL expired_session_keeps_lock [an expired session counted as dead]
FAIL call_queue_capped [50 calls in flight at once]
ok   offer_caps_refused [26 asserts]
ok   ready_room_refused [12 asserts]
ok   entry_recheck_aborts [19 asserts]
ok   reconnecting_paths [21 asserts]
FAIL giveup_cancels_landed_session [the landed session stayed open: {... "phase":"select" ...}]
FAIL refresh_survives_error [B's node stopped polling the trade after the error]
FAIL full_keeps_older_request [A2 send: @SimPeerB is already trading]      <- cascade: the M4 bug left B stuck
FAIL item_errors_counted [send: @SimPeerB is already trading]              <- (same cascade)
```
Those two cascaded failures re-run alone on a fresh harness, still the unchanged node:
```
TradeSim partA: 0 pass / 2 fail
FAIL full_keeps_older_request [the refused request removed A2's older one (replaced)]
FAIL item_errors_counted [describe error not counted: nil]
```
The 4 I4 / M12 tests are coverage for rules that were already built (the spec section 4 room / count / cap checks and
the Reconnecting paths). They pass on the old code, and the mutation check below proves each one catches its rule.

## GREEN (the final code, full suite, `partA(p, true)`)
```
TradeSim partA: 28 pass / 0 fail
ok   request_cross_node [47 asserts]
ok   request_ack_timeout [8 asserts]
ok   three_pending_max [13 asserts]
ok   send_limits [28 asserts]
ok   decline_cooldown [10 asserts]
ok   self_trade_refused [3 asserts]
ok   tutorial_refused [11 asserts]
ok   policy_refused [9 asserts]
ok   offer_sync_cross_node [24 asserts]
ok   ready_lock_resets [40 asserts]
ok   change_rate_limits [24 asserts]
ok   chat_limits [31 asserts]
ok   idle_and_total_timeout [21 asserts]
ok   second_trade_refused [15 asserts]
ok   kill_switch_refuses [29 asserts]
ok   request_same_node [11 asserts]
ok   query_ops [13 asserts]
ok   stale_read_ignored [13 asserts]
ok   expired_session_keeps_lock [11 asserts]
ok   call_queue_capped [9 asserts]
ok   offer_caps_refused [26 asserts]
ok   ready_room_refused [12 asserts]
ok   entry_recheck_aborts [19 asserts]
ok   reconnecting_paths [21 asserts]
ok   giveup_cancels_landed_session [8 asserts]
ok   refresh_survives_error [8 asserts]
ok   full_keeps_older_request [6 asserts]
ok   item_errors_counted [10 asserts]
node A {"memErrors":0,"itemErrors":2,"memReads":118,"errors":0,"busSends":173,"pushes":278,"memWrites":106,"busIn":156}
node B {"memErrors":1,"errors":1,"itemErrors":0,"memWrites":82,"busIn":183,"lastError":"session write: injected: the write landed, then the call failed","memReads":146,"busSends":154,"pushes":260}
memory calls {"staleNext":false,"errAfterWrite":false,"writes":188,"nilNext":false,"reads":264}, bus sends 327, biggest message 155 bytes, sync retries 0
```
The counters show exactly the injected faults:
- node A: 2 item errors (the injected describe and count);
- node B: 1 handled `handleSession` error and 1 memory error (the injected write-then-error).

## Mutation spot check (12 plants, each test's fix switched off, the 10 new tests run, `refresh_survives_error` last)
`refresh_survives_error` runs last because its own mutation leaves B's node stuck, which would cascade into later tests.
After the run the source was restored, checked byte-identical to the GREEN code, and checked to contain no plant.
```
TradeSim partA: 0 pass / 10 fail
FAIL expired_session_keeps_lock [an expired session counted as dead]              <- I1: expired counted dead again
FAIL call_queue_capped [4 calls in flight at once]                                <- I3: no 1-waiting cap
FAIL offer_caps_refused [a 3rd egg: nil]                                          <- the owned count ignored (n = 99)
FAIL ready_room_refused [A's READY: nil]                                          <- both READY room checks off
FAIL entry_recheck_aborts [room: the round didn't end: {... "phase":"confirm" ...}]  <- the stand-in's rules + room re-check off
FAIL reconnecting_paths [Phase 1 seal: nil]                                       <- the poll seal off
FAIL giveup_cancels_landed_session [the landed session stayed open: {... "select" ...}]  <- giveUp back to poison
FAIL full_keeps_older_request [the refused request removed A2's older one (replaced)]   <- replace before the cap
FAIL item_errors_counted [describe error not counted: 0]                          <- the counter off
FAIL refresh_survives_error [B's node stopped polling the trade after the error]  <- no pcall in refresh
```

## Notes
- **M10 scope.** BaseHatchery's own `TradeItems` OnInvoke (Task 3, lines 1335-1341) still turns an internal describe /
  count error into `nil` / `{}`. TradeNode can't tell that apart from "not owned".
  - TradeNode now counts and warns every error that reaches it, plus a `count` that isn't a table.
  - I didn't change BaseHatchery: it's Task 3's file, and this round's scope is TradeNode.
- **I3 semantics.** The limiter now counts at arrival, before the queue. A call refused by the queue cap has already
  used its limiter slot. That's consistent with "refused calls count", and the service calls stay capped either way.
