# Task 6 review: TradeServer part B (escrow, commit, record, settle, recovery)

Reviewer: Haiku 5.5 (fresh, read-only). Studio `3bf21205-caff-490e-a927-3bd9f0097311` read via `script_read` / `script_grep` only. Nothing written to Studio, no Play, no test re-runs.

Read: `ServerScriptService.TradeNode` (all 2536 lines; part B at 1597-2352, helpers 156-1000 for context), `ServerScriptService.TradeServer` (all), `ServerScriptService.BaseHatchery` TradeItems (1024-1369, plus `rebuildPetTools` 546, `despawnPet` 515, `spawnPet` 396-477, `baseOf` 63, `PetIndex.record`), `ServerScriptService.AutoReconnectServer` (129-165) vs `ServerStorage._Backup_Trading.Before.AutoReconnectServer` (129-152), `ServerStorage.TradeSimTests` (harness 161-330, runner 2802-2832, partB 1827-2398, crash 2400-2506, exploit 2508-2796, budget 2836-2962), `ServerScriptService.PlayerData` (save/hook 163-175, 285-319, FIELDS 78-82, onRemoving 389-402), `ServerScriptService.TradeCore` (327-459). Spec sections 3-7 and the controller decisions.

---

### Spec Compliance

- ✅ **Settle is one synchronous step** (`settleStep` 1757-1798): the SettledRounds gate reads the live attribute (1761), the escrow JSON and History JSON are encoded before the give (1779-1791), the give result is checked (1792-1793), then the entry is deleted, the mark is added and History is set (1794-1796). The save is queued after that (`settle` 1852).
- ✅ **take() only after a fresh re-read** (`enterEscrow` 2010-2016): `readSession`, then phase confirm, same round, same ver, not secured, live. The take at 2022 has no yield after the re-read; the older-entry and lost/leaving checks are repeated at 2018-2020.
- ✅ **Records**: one only-if-empty `UpdateAsync` (`ledgerCall` 1658-1684), a no-change read-back after an error (`recordOnce` 1687-1694), and only the returned record is acted on. RECORD_GIVE_UP switches to aborted after 60 s (2073-2075).
- ✅ **Dead committer** counts from this node's first sight of commit (`observe` 913-916; `verdict` 1877-1885).
- ✅ **BACK / cancel order**: session first, then aborted (`cancelTrade` 1036-1048; `OPS.back` 1509-1521; `abortRound` 2326-2340).
- ✅ **Recovery** (`recoverPlayer` 2155-2187): records read, an empty one written as aborted, settled through the gate; a return before DataLoaded only via `canSettle(p,"recovery")` (1729).
- ✅ **Seal**: AutoReconnect calls `TradeCancelFor` inside pcall after `Reconnecting` is set and before `SealForReconnect` (AutoReconnectServer 139-148). The only added lines versus the backup are 140-147.
- ✅ **Shutdown / leave**: select and confirm cancel as "left", commit is left to its record (2221-2234, 2454-2461).
- ✅ **SaveLost** (2189-2197): `lostSave` set, cancel through the record. `lostSave` is cleared on a new load (2157).
- ✅ **History and Done push** (1746-1751, 1803-1833): display cards only, the other player's name and uid, no ids, sigs, `from` or job ids.
- ✅ **Test names**: every brief name exists (`NAMES_B` 1827-1835, `NAMES_CRASH` 1836, `NAMES_EXPLOIT` 1837-1840, `budget` 2836).
- ⚠️ **Spec invariant 6 vs decision 9.** Spec 6 says "whenever a record EXISTS, the entry is settled at once, whatever the session's phase." The code does not read the record for a live confirm under 30 s of this node's first sight (`verdict` 1888-1895; `considerEntry` 1928-1931 returns "leave" before any read). The builder followed decision 9, which says no DataStore read unless commit or past 30 s. The two rules conflict. Not a dupe or loss path (see M-5).
- ⚠️ **Ruling 2 (OVER_TTL = 60 s, line 97)** for ended sessions, against spec §5's 15 min. Safe: a missing session only ever produces an only-if-empty aborted write, and a committed record cannot be overwritten. Recommend recording the deviation in the spec.
- ⚠️ **Ruling 11, shutdown**: `node:shutdown` does not set `leaving[p]` (2221-2234). See M-6.
- ⚠️ **Cannot verify by reading**: the RED/GREEN counts, the mutation spot checks, and the budget figures in the report. Not re-run, per the rules.

### Strengths

- The settle gate, give, entry delete and mark are one step, and the gate is on the live attribute.
- Every give goes through `canSettle` (1725-1733), which checks `lostSave`, `here()` (which covers leaving), DataLoaded and Reconnecting. The one exception, the `"return"` before DataLoaded, is only allowed from the recovery path.
- The `enterEscrow` give-back (2029) is synchronous with its own `here`/`lostSave` check (2018).
- Every escrow failure ends through `abortRound` and then the record. No path returns items without a record.
- The single-write record rule holds across every writer (commit, roundEnded, recovery, entry check, dead-committer). A committed record can't be overwritten, so the round can't settle both ways.
- `TradeItems` take/give (BaseHatchery 1167-1330): every check runs before any write, all JSON is encoded before the first SetAttribute, and the post-write steps are pcall'd. I read every post-write helper (`spawnPet` only starts a `task.spawn` loop; `rebuildPetTools`, `despawnPet`, `baseOf`, `PetIndex.record` and `eggsChanged` (a Fire) do not yield). The one-step argument for settle holds by reading (see M-10).
- The wrapper (1333-1368) turns every internal error into `nil, "error"`. The `_fault` seam returns `false, "Unknown op"` when not in Studio (1352-1353). TradeNode's `itemsCall` (546-557) fails closed on it.
- Callbacks are pure. Upvalue writes (`why`/`bug` in `writeSession` 747-752, `seen`/`wrote` in `ledgerCall` 1660-1666, `was` in `cancelSession` 1026-1028) are bookkeeping only. `setEscrowed` and `ready` use `copy()`.
- Studio-only seams are unreachable on a live server. The default node is built with no `crashAt` (`TradeServer` 48). `kill` is only reached through `crashed()` with `crashAt` (1644-1653). `TradeServerDebug` exists only in Studio (TradeServer 93). `_fault` is gated.
- Stores: the ledger name is asserted `_Studio` by the harness (226). `runSuite` asserts TestFreshSave (2803).
- The tests exercise real paths: the real SaveLock, the real `_Studio` ledger, injected faults at each point, a live `_fault` in the BaseHatchery wrapper, and a conservation check on each. The fake save store runs each callback twice (165-184), which is the right purity probe.

---

### Issues

#### Critical (must fix)

None found. I looked specifically for: a dupe (a give that is not gated, or the same round settled twice); a loss (take without a record, or an unchecked failure after take); a round settled both ways; a give after a lost save or while leaving; a non-pure callback; and a Studio seam that is reachable live. None of these holds on reading.

#### Important (should fix)

**I-1. The give-back after take() ignores its result, so a failed give drops the items** (`ServerScriptService.TradeNode` 2026-2031)

```
local json = enc(esc)
if json == "" then
    itemsCall("give", p, removed, "return") -- (it can't be recorded: straight back, in the same step)
    return failEntry(s, "item:" .. side, p)
end
```

The items were removed by `take()` at 2022. If `enc` fails, they are given back, but the return value of `itemsCall` is dropped. If that give refuses or errors (`nil, "error"`), the items are gone: removed from the inventory, not in escrow, not returned. Decision 7 says "never treat false / nil / an error as done", and this path does exactly that. It looks unreachable with plain data, but it is a loss path by construction.
Fix: check the JSON before `take()`. Encode a probe entry built from `copy(cur.offer[side])` at 2021, and call `failEntry` before any take if it is empty. Then this branch cannot run.

**I-2. A Lua error in `recoverPlayer` leaves its entry locked out of the 30 s check for the rest of the session** (`ServerScriptService.TradeNode` 2164-2177)

```
local ok, err = pcall(function()
    for key in esc do
        ...
        resolving[tag] = true
        local okR, rec = recordOnce(recKey(id, round), abortedRecord(id, round, nil))
        if okR and rec then settle(p, key, rec, "recovery") end
        resolving[tag] = nil      -- skipped if settle() throws
        ...
```

`settle` is not pcall'd on its own here. If it throws, `resolving[tag]` stays true. `considerPlayer` (1951-1952) then only sets `rerun` for that tag, and nothing ever consumes it. The entry is never checked again on this node until the player leaves and re-loads. Nothing is lost (the save still holds the entry, so recovery on the next load settles it), but the delivery or return stalls for the whole session. Spec 7 says the check keeps retrying.
Fix: clear `resolving[tag]` on every exit (pcall each key separately, or clear in the error branch), and warn when the pcall fails.

#### Minor (nice to have)

**M-1. `commitSeen` is never pruned** (516, 916, 1883). Every committed round on the node keeps an entry forever. Small, but unbounded. Clear it with the entry on settle, or cap it like `records` (CACHE_MAX).

**M-2. Forced re-checks in two loops bypass the back-off.** The ENTRY_WAIT loop calls `considerPlayer(p, nil, true)` every 0.5 s for up to 8 s (1998-2005). The sealCancel loop calls `considerPlayer(p, "seal", true)` every 0.25 s for up to 8 s (2207-2214). While a record is pending, each iteration is a ledger read, so that is up to about 16-32 DataStore calls per wait. Suggest a 2 s cadence, or respecting `retryAt`.

**M-3. `commitRound` retries forever during a DataStore outage** (2065-2077). Each stuck round makes about 2 ledger calls per 2 s (the write and its read-back), roughly 60/min per round, and it shares the DataStore budget with saves. This is per spec §7 ("retry every 2 s"), but after RECORD_GIVE_UP it should back off (for example to 30 s) rather than keep the 2 s cadence.

**M-4. `settle` ignores `saveOf`'s result** (1852). A save that fails with "error" is not retried by settle. The in-memory give is not persisted until a later save (autosave, leave, or the next settle). That is safe: the stored save still holds the entry, so a crash means recovery gives it once. Worth a warn or a scheduled save.

**M-5. Spec 6 vs decision 9, live confirm under 30 s** (`verdict` 1888-1895; `considerEntry` 1928-1931). A record that exists is not read until this node has held the entry for 30 s. Only latency is affected (up to 30 s). The controller should confirm which wording stands and update the spec or the code.

**M-6. Shutdown does not mark players as leaving** (`node:shutdown` 2221-2234; ruling 11). Settles after the close save are in-memory only, unless their queued save lands, and that save carries the give and the mark together. So there is no dupe, but the literal ruling ("never give after the final save unless another save follows") is only met through that queued save. Either set `leaving[p]` in shutdown or record the accepted behaviour.

**M-7. `saves.onLost` is silent if `SaveLost` is missing after 30 s** (`playerSaves.onLost` 279-282; `start` 2479-2486). The hook returns nil and nothing is logged. `lostSave` is still set from `saveOf`'s "lost", so the only effect is a delayed trade cancel. Warn.

**M-8. `considerPlayer` returns silently on an unreadable `TradeEscrow`** (1946-1947; also `checkEscrows` 2243). Those entries are never checked and nothing warns. `recoverPlayer` does warn (2160). Add a throttled warn.

**M-9. Test `seal_cancels_before_final_save` checks source text** (`TradeSimTests` 2314-2318: `src:find` order). The behavioural assertions after it are real, so the test is fine, but say so in its comment, or drop the text check.

**M-10. The one-step rule for settle depends on `TradeItems.give/take` never yielding after their data write, and nothing enforces it.** True today by reading (see Strengths). Suggest a comment at `settleStep` (1757) and at the top of `give` (BaseHatchery 1254), or a test that fails on a yield inside give.

---

### Assessment

**Task quality:** Needs fixes.

**Reasoning:** The core paths hold on reading: the settle gate and its single step, take and its re-read, the single-write record, the lost-save and leaving guards, and the atomic give/take. I found no dupe or loss path. Two fragile error-path holes (I-1 unchecked give-back after take, I-2 a stuck `resolving` flag after a recovery error) need fixing before this can be trusted. The spec-vs-decision-9 conflict (M-5) and the shutdown wording (M-6) need a controller ruling.
