# Task 4 report: `TradePresence` (online list, AWAY friends, search, busy locks)

**Status: DONE_WITH_CONCERNS.** All tests pass: pure 13/13, live 11/11. The main concern is one ruling: presence lives in a
MemoryStore **SortedMap**, not the spec's HashMap. That choice was measured; see Ruling 1.

## Scripts (all new; no existing script was changed, so nothing went into `_Backup_Trading.Before`)
| Path | Class | Job |
|---|---|---|
| `ServerScriptService.TradePresence` | ModuleScript (27,486 chars) | the whole system; `TradePresence.new(env)` instances + a default instance wired to the real services |
| `ServerScriptService.TradePresenceServer` | Script (2,806 chars) | `TradePresence.start(game.JobId)`; in Studio only, also creates `ServerStorage.TradePresenceDebug` (a BindableFunction for the live tests) |
| `ServerStorage.TradePresenceTests` | ModuleScript (47,257 chars) | `.pure(verbose)` (Edit, fakes) / `.live(player, verbose)` (Play, TestFreshSave, real `_Studio` stores) |

Studio copies were checked byte-for-byte (length + checksum) against my local copies in
`C:\Users\ventu\AppData\Local\Temp\tp_build\`. No CollectionService tags. TestFreshSave is still `true`, as the rules say.

## API (`ServerScriptService.TradePresence`)
Rows never contain job ids or any other internal field. Every table returned is a new copy.

- `TradePresence.new(env) -> P`: an instance. Call its functions with a dot (`P.rowsFor(player)`).
  - `env` (all optional):
    - `jobId`;
    - `memory` (MemoryStoreService-like: `GetSortedMap` / `GetHashMap`);
    - `datastore` (DataStoreService-like: `GetOrderedDataStore`);
    - `players` (Players-like: `GetFriendsAsync`, `GetUserIdFromNameAsync`, `GetPlayers`, `PlayerAdded` / `PlayerRemoving`);
    - `clock()` (seconds, used only for caches and the read budget);
    - `isSessionLive(tradeId) -> boolean` (default: every trade is live);
    - `pause(s)` (the wait between retries);
    - `stores` (default `TradeConfig.stores()`);
    - `enabled` (overrides `TradeConfig.ENABLED` for `start`);
    - `quiet` (no warnings).
- The module-level functions below all forward to **one default instance** made on first use with the real services.

| Function | Returns | Notes |
|---|---|---|
| `start(jobId?)` | `started: boolean` | Hooks PlayerAdded/PlayerRemoving plus players already here, and starts the 40 s refresh loop. Returns `false` (and does nothing) when `TradeConfig.ENABLED == false`. Idempotent. An empty jobId keeps the generated one (Studio's `game.JobId` is `""`, so it's `"studio-<guid>"`). |
| `stop()` | - | Unhooks and ends the loop (tests). |
| `configure(env)` | - | Swaps `memory` / `datastore` / `players` / `clock` / `isSessionLive` / `pause` on a running instance. **Task 5 must call `TradePresence.configure({isSessionLive = fn})`.** |
| `join(player)` / `leave(player)` | `boolean` | Never yield. `player` = a Player, or a virtual player (an Instance with a `UserId` attribute; name = its `Name` attribute or its instance name). |
| `refresh()` | - | One refresh round now: rewrites presence for every local player and clears their dead busy locks. |
| `jobId()` | `string` | The job id written into presence. |
| `isOnline(uid)` | `online, job?` / `false, nil, "error"` | Local players are answered without a call. Others: a fresh `GetAsync`. An expired entry or a tombstone = offline. |
| `onlineList()` | `{{uid, name}}, fresh` | The cached list, rebuilt at most every `ONLINE_REBUILD` (10 s), on demand only. Local players are merged in at once. `fresh = false` = the last rebuild failed (the last good list is kept). |
| `rowsFor(viewer)` | `{{uid, name, status = "ONLINE"|"AWAY"}}` | All ONLINE rows (A-Z) first, then the viewer's AWAY friends (A-Z). Never the viewer. A friend who is online appears once, as ONLINE. `viewer` = a Player, a virtual player or a uid. |
| `search(viewer, text)` | `rows` / `reason: string` | See "search" below. |
| `takeBusy(uidA, uidB, tradeId)` | `true` / `false, "busy"|"error"|"bad", uid?` | Either argument order. `uid` = the player whose key failed. |
| `releaseBusy(uid, tradeId)` | `ok` | `true` = the key no longer holds tradeId (released now, or someone else's). `false` = the call errored (3 tries). |
| `refreshBusy(uid, tradeId)` | `ok, held` | Restarts the lock's TTL (`SESSION_TTL`), only if it still holds tradeId. |
| `busyOf(uid)` | `ok, tradeId?` | (Extra, for Task 5's "is B busy?") A dead trade's lock reads as free and is cleared. |
| `stats()` | counters | presenceWrites / presenceReads / listCalls / busyCalls / seenReads / seenWrites / friendCalls / nameLookups / errors, for Task 6's budget test. |
| `TradePresence.BAD_TEXT` / `SELF_TEXT` | strings | `"Type a username (3-20 letters, numbers or _)"` / `"That's you!"` |

### How each part works
- **Presence** (`TradePresence_v1`, a SortedMap):
  - Value: `userId -> {job, name}`, TTL 120 s.
  - The join writes it in a background thread (3 tries). The refresh rewrites it every 40 s with `UpdateAsync`, keeping any other fields.
  - The leave is a conditional `UpdateAsync`. It writes a `{gone = true}` tombstone (5 s TTL) only while `job` is still this server's.
  - Writes and removals for one player run one at a time (a small per-uid queue), so a leave's removal can never land after the next join's write.
- **TradeSeen** (OrderedDataStore):
  - Written with `SetAsync(uid, os.time())` in a background thread, once per join, when `DataLoaded` becomes `true`.
  - Never written when it's `false`. A PlayerData `reload` (nil -> true) in the same join doesn't write again.
- **rowsFor**:
  - Friends come from `GetFriendsAsync` (first 100), cached 5 min per viewer. A failed call is retried after 30 s.
  - "Has played" = a TradeSeen key exists. These reads run in parallel, at most 40 per rolling minute per instance, and each result is cached 10 min.
  - Reads slower than 5 s land in the cache for a later open.
- **search**:
  - Text must be 3-20 characters of `[%w_]`. One leading `@` is accepted. Anything else returns `BAD_TEXT` **before any service call**.
  - First it filters the viewer's rows (case-insensitive substring).
  - Otherwise it looks up the exact username (`GetUserIdFromNameAsync`, pcall, cached 10 min; misses are cached 60 s):
    - online in any server -> one ONLINE row (fresh read);
    - the viewer's friend who has played -> one AWAY row (within the read budget);
    - the viewer -> `SELF_TEXT`;
    - anything else -> `"@name isn't online"`.
  - No per-player rate state is kept here (TradeServer enforces 1 search / 2 s and 1 list / 5 s).
- **Busy locks** (`TradeBusy_v1`, a HashMap, `userId -> tradeId`, TTL `SESSION_TTL`):
  - **Taking:** one key at a time, lower userId first. Each take is a conditional `UpdateAsync` that changes nothing if another trade holds the key.
  - **A blocking lock:** `isSessionLive(blocker)` is asked *outside* the callback. If it says the session is dead, the lock is cleared conditionally and the take is tried once more. An error or anything other than `false` counts as live.
  - **When the second key fails:** the first is released, only if it still holds this tradeId. An errored take is also released, in case it landed anyway.
  - **Release:** writes a `"-"` tombstone (5 s TTL) only if the key still holds this id.
  - **Presence refresh:** runs `busyOf` for each local player, which clears a dead lock.
- **Pure callbacks:** every `UpdateAsync` callback only computes the new value and records what it saw. The fake map runs every callback twice on fresh copies to catch side effects.
- **Never blocks a load:**
  - PlayerData doesn't know about this module.
  - `join` / `leave` only spawn threads.
  - Every service call is pcall-wrapped. Errors are counted, with at most one `warn` a minute per instance.
  - During an outage, local players stay ONLINE in their own server's list.

## Rulings I made
1. **Presence uses a MemoryStore SortedMap, not a HashMap.** This was measured in Studio, 2026-10-30:
   - **The problem with a HashMap:**
     - One full `ListItemsAsync` scan of the `_Studio` HashMap, with **one** entry, took **21 page calls (20 empty partition pages) and about 5 s**. Each call takes about 0.2 s in Studio.
     - Roblox docs: a scan costs "partitions scanned + items returned". **Two back-to-back scans used up the whole minute's universe quota** (Studio: 1000 + 120 x 1 users). The third scan and a plain `GetAsync` both failed with `TotalRequestsOverLimit`.
     - So one scan costs about 500 request units, however few players are online.
     - The spec's plan (a HashMap scan every 10 s per server with the list open) would throttle the whole game's MemoryStore, trade sessions included, once a couple of servers had the list open.
   - **Why the SortedMap works:**
     - `GetRangeAsync` costs one unit per entry returned (1 for an empty read).
     - The 7-entry list was one call of about 0.17 s. 30 range reads in a row didn't throttle.
     - Paging uses `{key = lastKey}` bounds (verified in Studio).
   - **What didn't change:** the name (`TradeConfig.stores().Presence`), the value, the TTL, the conditional leave and the API.
   - **Please update the spec's Data table row** ("MemoryStore HashMap `TradePresence_v1`" -> SortedMap) and the controller's "ListItemsAsync" note.
2. **Default instance + a small Script**, matching the codebase pattern (systems are Scripts that require modules):
   - `TradePresenceServer` calls `start(game.JobId)`. Starting on first require would also start loops when Edit-mode tests require clones.
   - In a running server, TradeServer's `require` returns the same module table, so it gets the started instance and adds `isSessionLive` through `configure`. `start` is idempotent, so a second call does nothing.
   - The Task 5 two-node simulation uses `TradePresence.new({jobId = ..., ...})` for node B and calls `join` / `leave` with virtual players.
3. **Conditional delete = tombstone.** MemoryStore maps have no conditional delete. "Remove only if it still holds X" writes `"-"` (busy) or `{gone = true}` (presence) with a 5 s TTL inside the same conditional `UpdateAsync`. A tombstone counts as no entry everywhere. A `"-"` value with TTL 5 (and even 1) was verified in Studio.
4. **This server's own players** are merged into its ONLINE list at once, and `isOnline` answers for them without a call. An entry claiming this server for someone no longer here is hidden. Same-server players show instantly, and the list still works during an outage.
5. **Kill switch:** `start()` returns `false` when `TradeConfig.ENABLED == false`, so no presence quota is spent. The read functions still answer.
6. **Search details:** one leading `@` is allowed (the rows show `@name`). Searching for yourself returns `"That's you!"`. Bad text returns `BAD_TEXT`. Neither message text is in the spec, so TradeServer/UI can swap them.
7. **Extra API:** `busyOf`, `refreshBusy`, `stats`, `jobId`, `configure`, `stop`, `refresh`, `join` / `leave`, for Tasks 5/6 and the simulation.

## Tests
Every brief test name exists: `online_then_away`, `away_only_for_friends`, `search_exact_name`, `job_ids_stripped`,
`busy_take_both_or_none`, `busy_release_only_own`, `stale_busy_cleared`, `presence_failure_does_not_block_load`.

Extra pure tests:
- `leave_keeps_newer_server`
- `seen_read_budget`
- `seen_written_after_load`
- `online_list_cached` (rebuild interval, 500 cap, cost)
- `store_names_and_kill_switch`

Extra live tests:
- `live_running_instance` (the started default instance wrote this player's entry)
- `live_seen_written`
- `live_friends_and_list` (the real `GetFriendsAsync`, the real player in the list)

`presence_failure_does_not_block_load`:
- **Pure:** memory, datastore and players all fail. `start`, `join`, `join` while loading, `refresh` and `leave` never yield (checked with a coroutine) and never throw. The player's attributes are untouched, the load finishes, and every API returns an error result. With slow services (0.3 s per call), `join` returns in under 0.1 s. After recovery, the next refresh brings the player back online.
- **Live:** `TradePresenceDebug "fail"` swaps failing adapters into the running default instance. Then:
  - `rejoin` doesn't yield;
  - `PlayerDataDebug "reload"` reloads the save (`DataLoaded == true`, Money unchanged);
  - `rowsFor` answers;
  - `takeBusy` returns `false, "error"`;
  - after `restore` + `rejoin`, presence is written again.

### RED (before the module existed)
Pure (Edit):
```
TradePresence: 0 pass / 13 fail
FAIL online_then_away [ServerScriptService.TradePresence not found]
FAIL leave_keeps_newer_server [ServerScriptService.TradePresence not found]
FAIL away_only_for_friends [ServerScriptService.TradePresence not found]
FAIL seen_read_budget [ServerScriptService.TradePresence not found]
FAIL seen_written_after_load [ServerScriptService.TradePresence not found]
FAIL search_exact_name [ServerScriptService.TradePresence not found]
FAIL job_ids_stripped [ServerScriptService.TradePresence not found]
FAIL online_list_cached [ServerScriptService.TradePresence not found]
FAIL busy_take_both_or_none [ServerScriptService.TradePresence not found]
FAIL busy_release_only_own [ServerScriptService.TradePresence not found]
FAIL stale_busy_cleared [ServerScriptService.TradePresence not found]
FAIL presence_failure_does_not_block_load [ServerScriptService.TradePresence not found]
FAIL store_names_and_kill_switch [ServerScriptService.TradePresence not found]
```
Live (Play, TestFreshSave):
```
TradePresence: 0 pass / 11 fail
FAIL live_running_instance [ServerScriptService.TradePresence not found]
... (all 11: ServerScriptService.TradePresence not found)
```

### First implementation (HashMap): pure GREEN, live RED on quota
- Pure: `TradePresence: 13 pass / 0 fail`.
- Live:
```
TradePresence: 5 pass / 6 fail
FAIL live_friends_and_list [the real player is in the ONLINE list: 0 entries]
FAIL job_ids_stripped [other online]
FAIL busy_take_both_or_none [t1 holds both: [false,"error",-908996032]]
FAIL busy_release_only_own [taken]
FAIL stale_busy_cleared [t1 taken]
FAIL presence_failure_does_not_block_load [RequestThrottled: Recent MemoryStores requests hit one or more limits.]
```
That led to the measurements in Ruling 1. Once the module moved to the SortedMap, the old fakes (which had no sorted map) went RED:
`5 pass / 8 fail` (online_then_away, leave_keeps_newer_server, away_only_for_friends, search_exact_name,
job_ids_stripped, online_list_cached, presence_failure_does_not_block_load, store_names_and_kill_switch).

### GREEN (final)
Pure (Edit, run twice, the last time after Play):
```
TradePresence: 13 pass / 0 fail
ok   online_then_away [10 asserts]
ok   leave_keeps_newer_server [3 asserts]
ok   away_only_for_friends [16 asserts]
ok   seen_read_budget [7 asserts]
ok   seen_written_after_load [7 asserts]
ok   search_exact_name [23 asserts]
ok   job_ids_stripped [31 asserts]
ok   online_list_cached [13 asserts]
ok   busy_take_both_or_none [22 asserts]
ok   busy_release_only_own [12 asserts]
ok   stale_busy_cleared [12 asserts]
ok   presence_failure_does_not_block_load [27 asserts]
ok   store_names_and_kill_switch [8 asserts]
```
Live (Play, TestFreshSave, real `_Studio` stores, 30.8 s):
```
TradePresence: 11 pass / 0 fail
ok   live_running_instance [4 asserts]
ok   live_seen_written [1 asserts]
ok   online_then_away [7 asserts]
ok   away_only_for_friends [3 asserts]
ok   search_exact_name [6 asserts]
ok   live_friends_and_list [4 asserts]
ok   job_ids_stripped [8 asserts]
ok   busy_take_both_or_none [3 asserts]
ok   busy_release_only_own [5 asserts]
ok   stale_busy_cleared [3 asserts]
ok   presence_failure_does_not_block_load [11 asserts]
```
- **Console during the live run:** no throttling. The only warning was the expected injected one (`presence remove failed ... injected failure (GetSortedMap)`).
- **After the run:** the `_Studio` presence map held only the real test player's entry. TradeSeen_v1_Studio held only the test player's key. The virtual keys were cleaned up.

### Mutation check (first, HashMap version: each bug planted in a temporary copy, the real module put back)
Every planted bug turned the right test red:

| Planted bug | Failing test |
|---|---|
| leave removes any server's entry | leave_keeps_newer_server |
| no rollback of the first lock | busy_take_both_or_none |
| a session-check error counts as dead | stale_busy_cleared |
| TradeSeen written on a failed load | seen_written_after_load |
| job ids leak into onlineList | job_ids_stripped |
| join writes presence inline (yields) | presence_failure_does_not_block_load ("join with slow services yielded") |
| AWAY rows for strangers | away_only_for_friends, seen_read_budget, search_exact_name |
| no seen-read budget | seen_read_budget, search_exact_name |
| busy take ignores an existing lock | busy_take_both_or_none, stale_busy_cleared |
| release ignores the trade id | busy_release_only_own |

The SortedMap change was a single function (`scan`) plus the map getter, so the matrix wasn't re-run.

## Concerns
1. **Spec deviation (Ruling 1).** The spec's Data table and the controller's notes still say "HashMap / ListItemsAsync". Please confirm the SortedMap change and update the spec.
2. **Budget at scale (for Task 6's `budget` test):**
   - A rebuild costs one unit per presence entry read (at most 500, the cap), at most 6 times a minute per server, and only while someone in that server is asking for the list.
   - That grows with (online players) x (servers with the list open) against a quota of `1000 + 120 x users`.
   - At today's player numbers it's tiny. At large scale, raise `TradeConfig.ONLINE_REBUILD` or lower the cap. Both are one-line changes.
   - A SortedMap also has one structure's throughput limit (about 30k units/min). Presence writes are about 1.5/min per online player, so that's fine up to about 15-20k concurrent players.
3. **My quota measurements used up Studio's MemoryStore quota twice for about a minute each** (`TotalRequestsOverLimit`). Roblox docs say Studio data and quota are separate from production, so the live game wasn't affected.
4. **Leftovers from the throttled first live run,** in the `_Studio` stores only:
   - a few virtual busy keys in the `TradeBusy_v1_Studio` HashMap (expire within 15 min);
   - the old `TradePresence_v1_Studio` **HashMap** entries (expired after 120 s);
   - probe maps `TradeProbe_Studio` / `TradeProbeSorted_Studio` (keys removed).
5. **AWAY needs TradeSeen,** which is only written from now on. Friends who played before this ships won't appear as AWAY until they join once. A "never played" result is cached for 10 min per server, as the spec says.
6. **Until Task 5 wires `isSessionLive`**, every busy lock counts as live. A lost release then clears only by TTL (`SESSION_TTL`, 15 min).
7. **Studio-only debug hook.** `ServerStorage.TradePresenceDebug` exists only when `RunService:IsStudio()`. Its `fail` / `restore` ops change the running default instance's adapters until `restore` is called. The live test always restores, even when it fails.
8. **Pasted, not served.** HttpService is disabled in the place (left as is), so the sources were pasted through MCP and then checksum-verified.

---

# Fix round 1 (2026-10-30)

**Status: DONE.** Pure 16/16, live 12/12. Each new check was RED first: pure 6 fails, live 1 fail.

## What changed
| Path | Change | Backup |
|---|---|---|
| `ServerScriptService.TradePresence` | the fixes below (31,040 chars) | new in Task 4 (none needed) |
| `ServerStorage.TradePresenceTests` | new + adjusted checks (55,611 chars) | new in Task 4 |
| `ReplicatedStorage.TradeConfig` | **+1 line** `C.LOOKUPS_PER_MIN = 30`; the `Presence` comment now says SortedMap. Nothing else changed (diffed against the backup) | **`ServerStorage._Backup_Trading.Before.TradeConfig`** (made before the edit, no tags) |

The Studio copies match my local copies byte-for-byte (length + checksum). Local copies are in
`C:\Users\ventu\AppData\Local\Temp\tp_build\`, and the pre-fix copies in `...\tp_build\fix1\*.before.lua`.

### IMPORTANT 1: per-search reads are budgeted
- **search, exact ONLINE:**
  - It's answered only from this server's cached `entries()` list (rebuilt at most every 10 s). It never does a presence read per search; the live check `presenceReads == 0` confirms it.
  - Someone who joined after the last rebuild shows as "isn't online" until that rebuild (at most 10 s).
- **Lookup budget:**
  - `TradeConfig.LOOKUPS_PER_MIN = 30`, per server, in any rolling 60 s. It covers both `GetUserIdFromNameAsync` calls and `isOnline`'s direct presence reads.
  - Over the budget, `search` returns `TradePresence.LATER_TEXT` = `"Try again in a moment"` and `isOnline` returns `false, nil, "later"`. Neither makes a call.
  - Cached names cost nothing, even over the budget.
- **Name misses** are cached 5 min (`NAME_RETRY` 60 s -> 300 s). Hits are still cached 10 min.
- **`isOnline(uid)`** answers in this order:
  1. this server's players, without a call;
  2. else the cached list, while it's fresh (younger than 10 s from the last *good* build);
  3. else at most one direct read per uid per 10 s (memoized), within the budget.

  An answer can therefore lag a join or leave by up to 10 s. This is documented in the module header. Task 5 relies on the 2 s request ack anyway.
- Edit-mode `require` caches the old TradeConfig table, so the module reads `C.LOOKUPS_PER_MIN or 30` once at load. The `30` is only a fallback.

### IMPORTANT 2: paging uses the documented bound
- `scan()` now passes the documented exclusive lower bound, built from the last item: `{key = last.key, sortKey = last.sortKey}`. Our entries have no sort key, so `sortKey` is nil there.
- **Pure `scan_paging_bounds`:**
  - The fake returns items with `sortKey = 0` and refuses any lower bound that isn't `{key, sortKey}` from the last item.
  - 450 entries come back exactly once over 3 reads: the first unbounded, then after item 200, then after item 400.
- **Live `live_scan_250`:**
  - Writes 250 entries into a separate `TradePresenceScanTest_Studio` sorted map, in parallel batches of 25 with 0.5 s pauses.
  - `onlineList()` on an instance pointed at that map (`env.stores`) returns all 250 exactly once, fresh, in 2 range reads.
  - The same batching then removes all 250. Map left afterwards: 0 entries.
- **Note:** this live test also passed on the old `{key = ...}` code. The real service accepts a key-only bound, so the documented shape is enforced by the pure test.

### Minors
- `TradeConfig` `Presence` comment: "MemoryStore SortedMap" (Task 2's file, backed up first).
- **`takeBusy` releases only what THIS call took.**
  - `takeOne` now also returns `took`: true = this call newly took the key; false = this trade already held it.
  - For an error, `took` means "maybe took": the callback ran on a free key, then the call failed.
  - A key this trade already held stays held when the other key is busy or errors.
- **List cap:** a rebuild that reads `LIST_CAP` (500) entries counts in `stats().listCapped`. The first one per instance logs one `warn` (unless `quiet`).
- **AWAY lag comment** on `rowsFor`: the list is up to 10 s old. A friend who joined in the last 10 s can still show AWAY (and one who just left, ONLINE) until the next rebuild.
- `prune()` also drops `isOnline` memo entries older than 10 s.

### Test changes beyond the new checks
- **`online_then_away` / `leave_keeps_newer_server`:** the clock is advanced 10 s before "offline after leaving", because `isOnline` is now cached for up to 10 s.
- **`job_ids_stripped`:** the "exact search" row used to come from a player who joined after the cache was built; that now correctly answers "isn't online". It now uses a renamed player (the list has `OldLate`, the search is for `LateGuy`) after a rebuild, so the exact path is still the one checked.
- **Live polls on `isOnline`** advance the fake cache clock by 10 s per poll, so each poll can read again.
- **New checks:**
  - `busy_take_both_or_none`: an already-held key kept when the other is busy, and when it errors.
  - `search_exact_name`: not in the cache yet -> "isn't online"; found after the rebuild; a renamed player found by the exact path; no presence reads.
  - `online_list_cached`: `listCapped == 1`.
  - New tests: `scan_paging_bounds`, `is_online_cached`, `lookup_budget`.
  - Live `search_exact_name`: `presenceReads == 0`.
  - Live `live_scan_250`.

## RED (new checks against the unchanged module)
Pure (Edit):
```
TradePresence: 10 pass / 6 fail
FAIL search_exact_name [not in the cached list yet: [{"status":"ONLINE","uid":5006,"name":"FreshGuy"}]]
FAIL online_list_cached [a rebuild that hits the cap is counted (and warned once): {"busyCalls":0,"seenReads":0,"presenceWrites":0,"errors":0,"nameLookups":0,"listCalls":9,"presenceReads":0,"seenWrites":0,"friendCalls":1}]
FAIL busy_take_both_or_none [60 still t8 after a busy second key: -]
FAIL scan_paging_bounds [all 450 exactly once: 0 / 0 dupes]
FAIL is_online_cached [a fresh cached list answers without a read: [true,"jobB",1]]
FAIL lookup_budget [over the budget: @OneTooMany isn't online]
```
Live (Play, TestFreshSave, 53.8 s):
```
TradePresence: 11 pass / 1 fail
FAIL search_exact_name [search never reads presence directly: {"busyCalls":0,"seenReads":40,"presenceWrites":0,"errors":0,"nameLookups":2,"listCalls":1,"presenceReads":1,"seenWrites":0,"friendCalls":1}]
ok   live_scan_250 [4 asserts]   (the old key-only bound works on the real service; see IMPORTANT 2)
(the other 10 ok)
```
- After the fix, one run in between: `15 pass / 1 fail`. `job_ids_stripped` searched for a player who joined after the cache was built, which is now correctly "isn't online"; the test was adjusted (see above).
- Before that, an Edit-only `nil` compare at `TradePresence:294`: the Edit `require` cache still held the old TradeConfig. Fixed with the module-level `LOOKUPS_PER_MIN` read.

## GREEN
Pure (Edit, run twice, the last time after Play):
```
TradePresence: 16 pass / 0 fail
ok   online_then_away [10 asserts]
ok   leave_keeps_newer_server [3 asserts]
ok   away_only_for_friends [16 asserts]
ok   seen_read_budget [7 asserts]
ok   seen_written_after_load [7 asserts]
ok   search_exact_name [26 asserts]
ok   job_ids_stripped [32 asserts]
ok   online_list_cached [14 asserts]
ok   busy_take_both_or_none [27 asserts]
ok   busy_release_only_own [12 asserts]
ok   stale_busy_cleared [12 asserts]
ok   scan_paging_bounds [4 asserts]
ok   is_online_cached [5 asserts]
ok   lookup_budget [39 asserts]
ok   presence_failure_does_not_block_load [27 asserts]
ok   store_names_and_kill_switch [8 asserts]
```
Live (Play, TestFreshSave, real `_Studio` stores, 53.4 s):
```
TradePresence: 12 pass / 0 fail
ok   live_running_instance [4 asserts]
ok   live_seen_written [1 asserts]
ok   online_then_away [7 asserts]
ok   away_only_for_friends [3 asserts]
ok   search_exact_name [7 asserts]
ok   live_friends_and_list [4 asserts]
ok   job_ids_stripped [8 asserts]
ok   busy_take_both_or_none [3 asserts]
ok   busy_release_only_own [5 asserts]
ok   stale_busy_cleared [3 asserts]
ok   presence_failure_does_not_block_load [11 asserts]
ok   live_scan_250 [4 asserts]
```
- **Console:** no throttling or errors. The only warning was the expected injected one.
- **After the run:** `TradePresenceScanTest_Studio` had 0 entries. `TradePresence_v1_Studio` held only the real test player.
- TradeCoreTests pure was re-run after the TradeConfig edit: `32 pass / 0 fail`.

### Mutation check of the fixes
Each bug was planted in a temporary copy; the real module was put back afterwards (checked). Every one turned exactly one test red:

| Planted bug | Failing test |
|---|---|
| release the first lock even if it was already held | busy_take_both_or_none |
| no lookup budget | lookup_budget |
| bound without sortKey | scan_paging_bounds |
| isOnline ignores the cached list | is_online_cached |
| isOnline without the per-uid memo | is_online_cached |
| name misses cached 60 s | lookup_budget |
| cap not counted | online_list_cached |

## Budget note (MemoryStore, per server; updates concern 2 of the main report)
| Source | Request units |
|---|---|
| Presence refresh | 1 `UpdateAsync` per local player every 40 s (about 1.5/min per player), plus 1 on join and 1 on leave |
| **Refresh busy sweep** | **1 `GetAsync` on `TradeBusy_v1` per local player every 40 s (about 1.5/min per player)**, plus 1 conditional clear when a dead lock is found. This is new in this note |
| ONLINE list | at most 6 rebuilds/min, only while someone in the server asks, each costing one unit per entry read (at most 500) |
| Lookups | at most `LOOKUPS_PER_MIN` (30) a minute per server: name lookups + `isOnline` direct reads (also at most 1 per uid per 10 s) |
| Busy locks per trade | 2 takes (+ a clear and a retake for each stale lock) + TradeServer's `refreshBusy` calls + 2 releases |
| TradeSeen | DataStore reads (40/min max) and 1 write per join. These are not MemoryStore units |

The baseline is about 3 units/min per player (refresh + busy sweep), against a quota of `1000 + 120 x users`. The list rebuilds are the part to watch in Task 6's `budget` test.

---

# Fix round 2 (2026-10-30)

**Status: DONE.** Pure 18/18. The 2 new tests were RED first: 16 pass / 2 fail. Live was not re-run (see below).

## What changed
| Path | Change |
|---|---|
| `ServerScriptService.TradePresence` | N1, N2, the minor and the N5 comment (32,492 chars) |
| `ServerStorage.TradePresenceTests` | 2 new tests, the fake Players can error, fake header comments fixed (58,233 chars) |

TradeConfig was not touched this round. The Studio copies match my local copies byte-for-byte (length + checksum). The pre-round copies are
`C:\Users\ventu\AppData\Local\Temp\tp_build\fix1\*.before2.lua`.

### N1: a name-lookup error is no longer cached as a miss
`userIdOf` now treats the three outcomes differently:

| Outcome | Cached for | Search answers |
|---|---|---|
| a userId | 10 min | the player |
| Roblox's own "no such user" answer | 5 min | `"@name isn't online"` |
| any other error (an HTTP failure) | 10 s back-off for that name (`NAME_BACKOFF`) | `"Try again in a moment"`, with no call during the back-off |

- Roblox reports "no such user" as an error too: `Players:GetUserIdFromNameAsync() failed: Unknown user`. I checked this text against the real API in Studio, and the code matches `"unknown user"` case-insensitively.
- A real-API check in Edit, with the real Players service and a made-up name: the answer was `@zqxj_nosuch_8812 isn't online`, with `nameLookups=1` and `nameErrors=0`.
- **Minor:** an error also counts in `stats().nameErrors` (and `stats().errors`) and logs one `warn` per instance (unless `quiet`).

### N2: isOnline errors are memoized
- A direct presence read that errors is memoized per uid for 10 s (`direct[uid] = {at, err = true}`).
- Within those 10 s, `isOnline` returns `false, nil, "later"` with no read and no budget spent. After 10 s it reads again.

### N5 (controller ruling): kept, with a comment
- `isOnline` keeps the direct read on a fresh-list miss, because it catches players who joined after the last rebuild.
- The comment notes it's bounded by the per-uid 10 s memo (errors included) and the per-server lookup budget.

### Minor: the fake's header comment
- It now reads "GetRangeAsync (ascending, {key, sortKey} lower bound)".
- The fake Players comment documents `errNames` and the real "Unknown user" error text. The fake's unknown-user message now matches Roblox's exactly.

## Tests
- `name_lookup_errors`:
  - an erroring lookup for an online, renamed player answers LATER_TEXT, and `nameErrors == 1`;
  - a repeat during the back-off makes no call;
  - once the lookup works (after 10 s) the player is found ONLINE;
  - Roblox's "Unknown user" is still a 5-minute miss and isn't counted as an error.
- `is_online_error_memo`:
  - the first read errors (`"error"`);
  - 5 repeats within 10 s answer `"later"`, with `presenceReads == 1` (one budget unit for 6 calls);
  - after 10 s the read happens again.

### RED (new tests against the unchanged module)
```
TradePresence: 16 pass / 2 fail
FAIL name_lookup_errors [an erroring lookup says try again: @Flaky isn't online]
FAIL is_online_error_memo [repeat 1 within 10 s, no new read: [false,null,"error"]]
```

### GREEN (Edit)
```
TradePresence: 18 pass / 0 fail
ok   online_then_away [10 asserts]
ok   leave_keeps_newer_server [3 asserts]
ok   away_only_for_friends [16 asserts]
ok   seen_read_budget [7 asserts]
ok   seen_written_after_load [7 asserts]
ok   search_exact_name [26 asserts]
ok   job_ids_stripped [32 asserts]
ok   online_list_cached [14 asserts]
ok   busy_take_both_or_none [27 asserts]
ok   busy_release_only_own [12 asserts]
ok   stale_busy_cleared [12 asserts]
ok   scan_paging_bounds [4 asserts]
ok   is_online_cached [5 asserts]
ok   lookup_budget [39 asserts]
ok   name_lookup_errors [7 asserts]
ok   is_online_error_memo [8 asserts]
ok   presence_failure_does_not_block_load [27 asserts]
ok   store_names_and_kill_switch [8 asserts]
```

### Mutation check of this round
Each bug was planted in a temporary copy; the real module was put back afterwards (checked):

| Planted bug | Result | Failing test |
|---|---|---|
| an error cached as a miss | 17 / 1 fail | name_lookup_errors |
| isOnline errors not memoized | 17 / 1 fail | is_online_error_memo |
| no name back-off | 17 / 1 fail | name_lookup_errors |
| nameErrors not counted | 17 / 1 fail | name_lookup_errors |

### Live
Not re-run. No live-only path changed:
- `userIdOf` and the `isOnline` error memo are fully exercised by the pure tests on fakes.
- The one real-service behavior involved, Roblox's "Unknown user" error text, was checked against the real API in Studio (above).
- The last live run (fix round 1) stays the live result: 12/12.

TestFreshSave is still `true`.
