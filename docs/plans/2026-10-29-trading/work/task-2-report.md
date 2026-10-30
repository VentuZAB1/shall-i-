# Task 2 report: `TradeConfig` + `TradeCore` (pure state machine)

Status: **DONE_WITH_CONCERNS** (all checks green; the concerns are hand-off notes for Tasks 3/5/6, not defects here).
Builder: Opus, 2026-10-30. Studio `3bf21205-caff-490e-a927-3bd9f0097311`, Edit mode only. I never started a Play session,
never touched TestFreshSave, never saved or published.

## Scripts
| Path | Class | What it is |
|---|---|---|
| `ReplicatedStorage.TradeConfig` | ModuleScript (new) | limits, phrases, `ENABLED`, `stores()` |
| `ServerScriptService.TradeCore` | ModuleScript (new) | the pure state machine |
| `ServerStorage.TradeCoreTests` | ModuleScript (new) | `.pure(verbose?, over?)` in Edit |

No existing script was changed, so nothing went into `ServerStorage._Backup_Trading.Before`.

Run: `require(game.ServerStorage.TradeCoreTests:Clone()).pure()` (pass `true` for every check with its assert count).
`over = {TradeCore = ModuleScript?, TradeConfig = ModuleScript?}` runs the suite against another copy. I used it for the
mutation check below.

## TradeConfig (ReplicatedStorage, client-readable: values plus `stores()`, nothing else)
- `ENABLED = true`: the kill switch. `TradeCore.newSession` refuses while it's false. Every other TradeCore action keeps
  working, so cancel, recovery and settling still run.
- **Spec section 4 values:**
  - `MAX_ITEMS 9`, `READY_LOCK 5`, `ACCEPT_LOCK 5`, `IDLE_TIMEOUT 180`, `TOTAL_TIMEOUT 600`;
  - `CHANGE_PER_PLAYER 4` / `CHANGE_PLAYER_WINDOW 1`, `CHANGE_PER_TRADE 30` / `CHANGE_TRADE_WINDOW 10`;
  - `PHRASES = {"Add More", "L Trade", "Last Offer", "Deal?", "Fair Trade", "No Thanks"}`, `CHAT_GAP 1.5`,
    `SAME_PHRASE_GAP 5`, `CHAT_LINES 8`;
  - `REQUEST_TTL 30`, `REQUEST_ACK_WAIT 2`, `SEND_GAP 3`, `SEND_MAX 10` / `SEND_WINDOW 300`, `PENDING_MAX 3`,
    `DECLINE_COOLDOWN 30`;
  - `SEARCH_GAP 2`, `LIST_GAP 5`, `NAME_MIN 3` / `NAME_MAX 20`, `HISTORY_MAX 20`.
- **Spec section 5 values, for Tasks 4-6:**
  - `PRESENCE_TTL 120`, `PRESENCE_REFRESH 40`, `SESSION_TTL 900`, `ONLINE_REBUILD 10`, `FRIENDS_CACHE 300`;
  - `SEEN_FRIENDS_MAX 100`, `SEEN_READS_PER_MIN 40`, `SEEN_CACHE 600`;
  - `BUS_PER_SEC 4`, `POLL 2`, `COMMIT_DEAD_AFTER 30`, `RECORD_RETRY 2`, `RECORD_GIVE_UP 60`, `BACKOFF_MAX 10`,
    `SETTLED_KEEP 200`.
- The inventory caps (150 / 150) stay in `InventoryConfig`. They aren't duplicated here.
- `TradeConfig.stores() -> {Ledger, Seen, Presence, Busy, Sessions, Topic}` returns a NEW table every call. The names are
  `TradeLedger_v1`, `TradeSeen_v1`, `TradePresence_v1`, `TradeBusy_v1`, `TradeSessions_v1` and `Trade_v1`, and each gets
  `"_Studio"` when `RunService:IsStudio()`. The gift stores stay in SaveLock.

## TradeCore public API
Every action takes the session and returns `true, newSession` (a full deep copy) or `false, reason`. It never mutates
its input or the item passed in, and refused actions change nothing. `now` is always passed in, in seconds, and
TradeCore reads no clock. Its only service use is `ReplicatedStorage`, to find `TradeConfig` and `Mutations`.

```
TradeCore.config                                   -- the TradeConfig table this copy uses
TradeCore.validKg(kg) -> boolean                   -- finite number > 0
TradeCore.petSig(pet) -> sig | nil, reason          -- "id|name|%.17g|mutKey"  (pet = {id, name, kg, mut?})
TradeCore.eggSig(kind, kg, mutList) -> sig | nil, reason   -- "kind|%.17g|mutKey"
TradeCore.newSession(id, a, b, now) -> session | nil, reason   -- a/b = {uid, name, job}; phase select, ver 1, round 0
TradeCore.sideOf(s, uid) -> "a" | "b" | nil
TradeCore.addItem(s, side, item, owned, now)
TradeCore.removeItem(s, side, index, now)
TradeCore.ready(s, side, clientVer, now, localSeenAt?)
TradeCore.startConfirm(s, now)
TradeCore.setEscrowed(s, side, round, items)
TradeCore.accept(s, side, clientVer, now, localSeenAt)
TradeCore.toCommit(s, now?, localSeenAt?)
TradeCore.back(s, now)
TradeCore.cancel(s, why, now?)
TradeCore.finish(s, outcome, now)                  -- outcome "committed" -> done | "aborted" -> cancel; phase commit only
TradeCore.chat(s, side, phraseIndex, now)
TradeCore.expired(s, now) -> boolean, ("idle" | "total" | "broken")?
TradeCore.record(s) -> {a = uidA, b = uidB, itemsA, itemsB} | nil
```

**Session shape** (JSON-safe: string keys or dense lists only):
```
{id, ver, round, phase = "select"|"confirm"|"commit"|"done"|"cancel", a/b = {uid, name, job},
 offer = {a = {item...}, b = {item...}}, ready = {a = ver?, b = ver?}, accept = {a = ver?, b = ver?},
 escrowed = {a = {round, items}?, b = {round, items}?}, chat = {{s = side, p = phraseNumber, t = at}...} (last 8),
 startedAt, changedAt, confirmAt?, why?, rate = {a = {at...}, b = {at...}}, chatAt = {a?, b?},
 phraseAt = {a = {p1 = at, ...}, b = {...}}}
```

**Items:**
- pet: `{t = "pet", sig, id, name, kg, mut?}`;
- egg: `{t = "egg", sig, kind, kg, mut?}`.
- Extra display fields are kept, deep-copied.

**What changes `ver` / `changedAt`:**
- `ver` goes up on `addItem`, `removeItem`, `startConfirm`, `back`, `toCommit`, `cancel` and `finish`.
- `changedAt` is set by the offer changes and by every phase change that's given a clock (`toCommit` / `cancel` take
  `now` as an optional argument).
- `ready`, `accept`, `setEscrowed` and `chat` change neither.

**Reasons a refusal can return:**
- input: "Bad trade", "Bad side", "Bad time", "Bad item", "Bad KG", "Bad phrase", "Bad outcome", "Bad player";
- offers: "Offers are locked", "Slow down", "Max 9 items", "Already in offer", "You don't have that pet",
  "You don't have more of that egg";
- timing and versions: "Offer changed", "Wait Ns", "Already ready", "Already accepted", "Add an item first",
  "Both must be READY", "Not now";
- escrow and commit: "Old round", "Already secured", "Items changed", "Securing items...", "Waiting for both";
- ending: "The trade is completing", "Trade is over", "Trading is off", "You can't trade with yourself".

## Rulings (where the brief left room)
1. **Optional trailing arguments.** These go beyond the brief's signatures, but the brief's calls still work unchanged.
   Each one comes from the spec.
   - `ready(..., localSeenAt?)` and `toCommit(s, now?, localSeenAt?)`. The spec's exploit table says "each server
     counts the 5 s on its own clock", and invariant 3 needs "the 5 s wait has passed on the committing server".
     - READY counts the 5 s from `max(changedAt, localSeenAt)`.
     - ACCEPT and the timed `toCommit` count from `max(confirmAt, localSeenAt)`.
     - `accept` refuses when `localSeenAt` is missing.
   - `cancel(s, why, now?)`: the brief's `cancel(s, why)` has no clock, and phase changes should set `changedAt`.
2. **Extra functions.**
   - `finish` (commit -> done / cancel after the record). Without it, Task 6 would have to edit `phase` by hand.
   - `sideOf`, `validKg`, `config`.
3. **Refused calls don't change the rate ring.** The spec says a refused action changes nothing.
   - Spec 4's "Refused calls count against the limits too" therefore belongs to TradeServer's local per-remote limiter,
     which runs before any service call.
   - TradeCore's ring counts accepted changes only, and it holds across servers.
4. **`ready` refuses when both offers are empty** ("Add an item first"). This stops empty trades costing escrow saves and
   a ledger write. One empty side is fine (a gift), and so is an empty escrow list.
5. **`setEscrowed` checks the items against the offer.**
   - It refuses unless the items' sig multiset equals that side's offer: what the other player saw is what gets
     escrowed.
   - It works once per side per round, in phase confirm only, and doesn't change `ver`.
6. **`addItem` recomputes the item's sig from its own fields** and refuses a mismatch, so the KG on the card is the KG
   that `take()` will remove.
   - A pet id is allowed only once, even under a different name or KG.
   - `owned` must be a finite number (NaN or text is refused).
7. **Signatures:**
   - the parts can't contain `|`;
   - numeric pet ids are accepted (`tostring`);
   - `mut` may be a list or a mutKey string, and both give `Mutations.key` (sorted, known names only, the same matching
     as `Mutations.findEntry`). So a bare-number egg and `{kg}` with no mutation share one sig.
8. **`cancel` clears `escrowed`** (spec: "cleared on every abort"). It's refused in commit and once the trade is over.
9. **`record(s)` needs phase `commit`**, plus BOTH `escrowed` lists for `s.round` (an empty list is fine).
   - It returns userIds, and deep copies of the lists only.
   - TradeServer adds `state` and `at`.
   - "Aborted" records are written without `record()`: BACK / cancel have already cleared `escrowed`.
10. **`expired()` only fires in select / confirm.** In commit the record decides, and done / cancel are already over.
    A live session with missing clocks counts as expired ("broken"), so it can never keep a player busy.
11. **Chat is allowed in select and confirm.** The same-phrase timers are stored under string keys `p1..p6`, which keeps
    them JSON-safe.

## RED (before TradeConfig / TradeCore existed)
```
TradeCore: 0 pass / 28 fail
FAIL phase_flow [TradeCore not found]
FAIL old_ver_ready_refused [TradeCore not found]
FAIL ready_5s_lock [TradeCore not found]
FAIL accept_5s_lock [TradeCore not found]
FAIL accept_needs_own_escrow [TradeCore not found]
FAIL nine_cap [TradeCore not found]
FAIL dup_pet_refused [TradeCore not found]
FAIL egg_overcount_refused [TradeCore not found]
FAIL nan_inf_kg_refused [TradeCore not found]
FAIL change_clears_ready_accept [TradeCore not found]
FAIL back_empties_offers [TradeCore not found]
FAIL back_refused_in_commit [TradeCore not found]
FAIL cancel_refused_in_commit [TradeCore not found]
FAIL commit_needs_both_escrows [TradeCore not found]
FAIL record_from_escrow_only [TradeCore not found]
FAIL chat_keeps_ver [TradeCore not found]
FAIL idle_and_total_timeout [TradeCore not found]
FAIL studio_store_names [TradeConfig not found]
FAIL config_values [TradeConfig not found]
FAIL sig_format [TradeCore not found]
FAIL rate_limits [TradeCore not found]
FAIL offer_locked_after_select [TradeCore not found]
FAIL remove_item [TradeCore not found]
FAIL set_escrowed_rules [TradeCore not found]
FAIL finish_after_record [TradeCore not found]
FAIL new_session_rules [TradeCore not found]
FAIL inputs_never_mutated [TradeCore not found]
FAIL bad_input_never_errors [TradeCore not found]
```

## GREEN (final, `pure(true)`)
All 18 brief names are there, plus 11 extra checks: `config_values`, `sig_format`, `rate_limits`,
`offer_locked_after_select`, `remove_item`, `set_escrowed_rules`, `finish_after_record`, `new_session_rules`,
`inputs_never_mutated`, `bad_input_never_errors` and `json_round_trip` (added after GREEN; it drives the whole flow with
a JSON encode/decode between every step, as MemoryStore will).
```
TradeCore: 29 pass / 0 fail
ok   phase_flow [24 asserts]
ok   old_ver_ready_refused [25 asserts]
ok   ready_5s_lock [15 asserts]
ok   accept_5s_lock [18 asserts]
ok   accept_needs_own_escrow [15 asserts]
ok   nine_cap [26 asserts]
ok   dup_pet_refused [12 asserts]
ok   egg_overcount_refused [11 asserts]
ok   nan_inf_kg_refused [33 asserts]
ok   change_clears_ready_accept [21 asserts]
ok   back_empties_offers [23 asserts]
ok   back_refused_in_commit [14 asserts]
ok   cancel_refused_in_commit [25 asserts]
ok   commit_needs_both_escrows [22 asserts]
ok   record_from_escrow_only [29 asserts]
ok   chat_keeps_ver [41 asserts]
ok   idle_and_total_timeout [39 asserts]
ok   studio_store_names [17 asserts]
ok   config_values [93 asserts]
ok   sig_format [16 asserts]
ok   rate_limits [42 asserts]
ok   offer_locked_after_select [21 asserts]
ok   remove_item [13 asserts]
ok   set_escrowed_rules [27 asserts]
ok   finish_after_record [22 asserts]
ok   new_session_rules [8 asserts]
ok   inputs_never_mutated [40 asserts]
ok   bad_input_never_errors [174 asserts]
ok   json_round_trip [27 asserts]
```

## Mutation check (does each brief test catch its own rule being broken?)
I broke one rule at a time in a nil-parented copy of TradeCore / TradeConfig and ran `pure(false, {[name] = copy})`.
The real modules were never touched.

**Caught by their own test:** phase_flow (round not bumped), old_ver_ready_refused, ready_5s_lock, accept_5s_lock,
accept_needs_own_escrow, nine_cap (`>=` -> `>`), egg_overcount_refused, nan_inf_kg_refused, change_clears_ready_accept,
back_empties_offers, back_refused_in_commit, cancel_refused_in_commit, commit_needs_both_escrows,
record_from_escrow_only (record from the offer), chat_keeps_ver (chat bumps ver), idle_and_total_timeout,
studio_store_names (suffix removed), rate_limits, inputs_never_mutated (in-place edit) and set_escrowed_rules.

**dup_pet_refused:**
- Removing only the "same sig" line is not caught. That's expected: the pet-id check also refuses every same-sig pet,
  so the two lines are redundant guards.
- Removing the id check is caught.
- Removing both is caught.

## Concerns / hand-off notes
1. **Task 3 item shape.** `addItem` rebuilds the sig from the item's own fields.
   - `describe()` must give pets an `id` field (the plan writes `name/kind`) and eggs a `kind` field. Each item's
     `sig` must come from `TradeCore.petSig` / `eggSig`.
   - `take()`'s returned items must carry `sig`, because `setEscrowed` matches them against the offer.
2. **Clock source.** Every server must pass the same kind of `now`, because stamps written by one server are compared
   on another.
   - I recommend `workspace:GetServerTimeNow()`: it's synced and sub-second.
   - With `os.time()` (whole seconds) the rules still hold but are coarser. For example, the 1.5 s chat gap becomes 2 s.
3. **Refused calls must be counted by TradeServer's local limiter** (spec 4). TradeCore stores only accepted changes
   (ruling 3).
4. **BACK loop cost.** Each Phase 2 entry costs 2 escrow saves + 1 aborted record + 2 settle saves.
   - A BACK loop is bounded only by the 5 s READY lock (at most about one cycle per 5 s) and the 10-minute cap.
   - Task 6's budget measurement should include this loop.
5. **Edit require cache.** In a long Edit session, TradeCore's own `require` of TradeConfig can stay a cached copy if
   TradeConfig is edited later.
   - The suite reads limits through `TradeCore.config`.
   - `config_values` cross-checks those against a fresh TradeConfig clone, so a stale cache shows up as a failure,
     never as a false pass.

---

# Fix round 1 (2026-10-30)

Status: **DONE**. All review items are fixed, and the suite is 32 pass / 0 fail. I worked in Edit mode only: no Play
session, TestFreshSave untouched, no save or publish.

I rewrote `ServerScriptService.TradeCore` and `ServerStorage.TradeCoreTests` in full, because most functions changed.
Both are my own new modules from this task, so no backup was needed. `ReplicatedStorage.TradeConfig` is unchanged.

## What changed in TradeCore
- **I-1, `toCommit(s, now, localSeenAt)`:** both clocks are now REQUIRED.
  - A missing or non-finite `now` -> "Bad time"; a missing or non-finite `localSeenAt` -> "Bad local time".
  - The committing server's 5 s lock always runs: from `max(confirmAt, localSeenAt)` (spec invariant 3).
  - The old test that expected the no-clock bypass now expects a refusal.
- **I-2, timeouts are enforced inside every action.**
  - A shared `precheck` refuses with "Trade timed out" while `TradeCore.expired(s, now)` is true.
  - This covers `addItem`, `removeItem`, `ready`, `startConfirm`, `setEscrowed`, `accept`, `toCommit`, `back` and `chat`.
  - `cancel` and `finish` skip that check, so a dead trade can still end. `finish` only runs in phase commit, which
    never expires.
  - The reviewer's case is now a test: an ACCEPT at 10 min + 1 s is refused, and so is a commit at 10 min + 1 s.
- **`setEscrowed(s, side, round, items, now)`:** this gains a REQUIRED `now`, used only for the timeout rule. That's a
  signature change from the brief, so Task 6 must pass it. It still doesn't change `ver` or `changedAt`.
- **Minors:**
  - `cancel(s, why, now)` and `finish(s, outcome, now)` now require a finite `now` and always set `changedAt` (via the
    phase change).
  - `accept` with a missing or non-finite `localSeenAt` -> "Bad local time" (it used to be "Wait 5s").
  - `ready` with a `localSeenAt` that isn't finite -> "Bad local time". `localSeenAt` is still optional for READY.
  - `who()` type-checks the players: `uid` a whole number (Studio test players are negative), `name` a non-empty
    string, `job` a string. `""` is allowed for `job`, because Studio's `game.JobId` is empty.
  - `bad()` now requires a finite `confirmAt` in phase confirm.
  - `expired()` returns `true, "broken"` for a live-phase session TradeCore can't work on. `cancel` refuses that
    session as "Bad trade", so TradeServer must treat it as missing (spec 6 allows "aborted" for a missing session).
  - One helper, `lockReason(stamp, localSeenAt, now, secs)`, now holds the 5 s logic for READY, ACCEPT and the commit.

## Updated API (supersedes the matching lines above)
```
TradeCore.ready(s, side, clientVer, now, localSeenAt?)   -- localSeenAt optional, but must be finite if given
TradeCore.setEscrowed(s, side, round, items, now)        -- now REQUIRED (timeout rule)
TradeCore.accept(s, side, clientVer, now, localSeenAt)   -- localSeenAt REQUIRED ("Bad local time")
TradeCore.toCommit(s, now, localSeenAt)                  -- both REQUIRED
TradeCore.cancel(s, why, now)                            -- now REQUIRED; works on a timed-out trade
TradeCore.finish(s, outcome, now)                        -- now REQUIRED
TradeCore.expired(s, now) -> boolean, ("idle" | "total" | "broken")?
```
New reasons: "Trade timed out", "Bad local time". Rulings 1 and 10 above are superseded by this section.

## New / changed checks
- **New:**
  - `actions_refused_after_timeout`: idle in select, idle in confirm, the total 10 min in confirm, and cancel / finish
    still allowed after a timeout;
  - `cancel_finish_need_clock`;
  - `kill_switch_new_session`: it sets `ENABLED = false` for three calls. `newSession` is refused, while `cancel` and
    `finish` still work.
- **Extended:**
  - `commit_needs_both_escrows`: no clock / NaN / missing or inf `localSeenAt` are refused;
  - `accept_5s_lock`: "Bad local time" for nil and NaN;
  - `ready_5s_lock`: a NaN `localSeenAt`;
  - `set_escrowed_rules`: no clock;
  - `new_session_rules`: name / job / uid types, and a Studio player with uid -1 and job `""` is accepted;
  - `bad_input_never_errors`: a confirm session without `confirmAt`;
  - `inputs_never_mutated`: every argument (session, item, items, owned) is snapshotted and compared, a refused
    `setEscrowed` is included, and the caller's items list is changed after the call.
- `owned` is a number, so it can't be changed by reference. It's still part of the snapshot.

## RED (new tests against the unfixed TradeCore)
```
TradeCore: 24 pass / 8 fail
FAIL ready_5s_lock [ready b with a NaN local time: should be refused, got true / table: 0x4f8f8c7b017dcf8d]
FAIL accept_5s_lock [accept with no local sight time: reason 'Wait 5s', wanted 'Bad local time']
FAIL commit_needs_both_escrows [commit with no clock: should be refused, got true / table: 0xf2064eb5b492c74b]
FAIL actions_refused_after_timeout [idle select add: should be refused, got true / table: 0xb89b73a32942ffb4]
FAIL cancel_finish_need_clock [cancel without now: should be refused, got true / table: 0xec3ab2c4327d4bd0]
FAIL set_escrowed_rules [no clock: should be refused, got true / table: 0xc4288b1d26feeb07]
FAIL new_session_rules [a uid is a whole number]
FAIL bad_input_never_errors [confirm without confirmAt call 6 not refused: true table: 0x935304113f19911f]
```
`kill_switch_new_session` and the extended `inputs_never_mutated` already passed in RED: that behaviour existed, only the
tests were missing. The mutation check below shows both of them fail when their rule is removed.

## GREEN (`pure(true)`)
```
TradeCore: 32 pass / 0 fail
ok   phase_flow [24 asserts]
ok   old_ver_ready_refused [25 asserts]
ok   ready_5s_lock [17 asserts]
ok   accept_5s_lock [21 asserts]
ok   accept_needs_own_escrow [15 asserts]
ok   nine_cap [26 asserts]
ok   dup_pet_refused [12 asserts]
ok   egg_overcount_refused [11 asserts]
ok   nan_inf_kg_refused [33 asserts]
ok   change_clears_ready_accept [21 asserts]
ok   back_empties_offers [23 asserts]
ok   back_refused_in_commit [15 asserts]
ok   cancel_refused_in_commit [28 asserts]
ok   commit_needs_both_escrows [31 asserts]
ok   record_from_escrow_only [29 asserts]
ok   chat_keeps_ver [41 asserts]
ok   idle_and_total_timeout [39 asserts]
ok   studio_store_names [17 asserts]
ok   actions_refused_after_timeout [98 asserts]
ok   cancel_finish_need_clock [22 asserts]
ok   kill_switch_new_session [15 asserts]
ok   config_values [93 asserts]
ok   sig_format [16 asserts]
ok   rate_limits [42 asserts]
ok   offer_locked_after_select [21 asserts]
ok   remove_item [13 asserts]
ok   set_escrowed_rules [36 asserts]
ok   finish_after_record [22 asserts]
ok   new_session_rules [14 asserts]
ok   inputs_never_mutated [44 asserts]
ok   bad_input_never_errors [208 asserts]
ok   json_round_trip [27 asserts]
```

## Mutation check, re-run on the new TradeCore: 32 caught / 0 missed
I broke one rule at a time in a nil-parented copy; the real modules were untouched. Each breakage made its own test fail.

**Fix-round rules:**
- the commit's 5 s lock removed;
- the commit's `localSeenAt` check removed;
- the expiry line in `precheck` removed;
- the `now` checks in `cancel` / `finish` removed;
- `accept`'s "Bad local time" removed;
- `ready`'s NaN `localSeenAt` check removed;
- `who()`'s type checks removed;
- `bad()`'s `confirmAt` line removed;
- the `ENABLED` line removed;
- `setEscrowed` keeping the caller's items table;
- `setEscrowed` without `precheckSide`.

**All 21 original rules, re-targeted at the new source.** This time it includes the dup-pet id guard on its own.

## Hand-off notes (update)
- **The 150 / 150 caps stay in `InventoryConfig.MAX_PETS` / `MAX_EGGS`.** They are deliberately not duplicated in
  TradeConfig. The room check at READY and at Phase 2 entry belongs to TradeServer, which reads InventoryConfig.
- **Task 6 must pass the new required clocks:**
  - `setEscrowed(..., now)`;
  - `toCommit(s, now, localSeenAt)`, where `localSeenAt` = when that node first saw phase confirm;
  - `cancel(s, why, now)` and `finish(s, outcome, now)`.
- **TradeServer must treat a session that `expired()` calls "broken" as missing.** TradeCore can't cancel it.
- Concerns 1-4 above still stand: the Task 3 item shape, one clock source (`workspace:GetServerTimeNow()`), refused
  calls counted by TradeServer's limiter, and the BACK loop budget.
