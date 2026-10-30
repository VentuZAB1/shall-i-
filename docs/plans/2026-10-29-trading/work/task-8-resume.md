# Task 8: resume checklist (written 2026-10-30 from a cloud session with no Studio access)

A cloud session can't reach Studio, and it can't reach the Windows PC's folders. Run this from a local session on the PC
with Studio open and the Studio MCP connected.

## Where Task 8 stands (from the ledger)
- Step 1: done. Review A has 0 C / 0 I / 6 M (`task-8-review-A.md`). Review B has 0 C / 2 I / 5 M (`task-8-review-B.md`).
- Step 1b: done. The hands-on red team found 0 holes. It found one UI issue (UI-1, the tall/narrow PC window).
- Steps 2-3: dispatched to a fresh Opus builder with the 12 fixes in `task-8-fix-decisions.md`. **No result is in the
  ledger, and there is no `task-8-report.md`.** Don't assume the builder finished, and don't assume it didn't. Check the
  place first (next section).
- Step 4: partly done (the vault and the memory note). Still open: the `_Studio` test keys, `TestFreshSave = false`,
  Save to Roblox, the owner report numbers, and the line `Task 8: complete`.

## 1. Find out which fixes are in the place (read-only: script_grep / script_read in Edit)
Use the table to mark each fix as present or missing. Send a builder only for the missing ones. Each still gets a test
first. The builder was probably cut off by the owner's weekly usage limit partway through. So count a fix as missing if
its code is there but its test isn't, or if its test doesn't pass.

| # | Fix | How to tell it's in |
|---|---|---|
| 1 | Pair cooldown after a decline / expiry / unanswered drop | `TradeConfig.PAIR_COOLDOWN == 120`; the cooldown is also set where a request expires or drops (TradeNode poll, near the old 2539-2545); `TradeSimTests` has `request_slot_griefing` |
| 2 | Refused calls are free | the node refuses from its own copy before `writeSession`; RULES.button is 1/s for READY/ACCEPT/BACK/CANCEL; TradeConfig has a per-trade write budget (~40/min); `TradeSimTests` has `refused_calls_free` |
| 3 | A-M1: the soft restart cancels first | AdminServer `saveBeforeLobby` calls `ServerStorage.TradeCancelFor` before `SavePlayerNow` |
| 4 | A-M2: settle is all-or-nothing | `settleStep` checks the three encoded lengths BEFORE `itemsCall("give", ...)` and restores on a throw; there's a fault-seam test |
| 5 | A-M3: the 30 s check reads twice | `verdict` treats "missing" as abort only after a second read at least POLL s later |
| 6 | A-M4: cancel before "aborted" | the expired-confirm case moves the session first; `recoverEntry` re-reads when the cancel write fails |
| 7 | A-M5 / B M-5: `_G` helpers are gated | `_G.HatcheryGive` / `PlaceAt` / `HatchAll` / `Rebase` / `Force` / `Validate` (BaseHatchery, near the old 1415-1436) are inside `RunService:IsStudio()`. The builder should have reported any live caller |
| 8 | B M-1: the limiter survives a leave | `onLeave` no longer has `limits[uid] = nil`; a timer sweeps out expired entries |
| 9 | B M-2: an expired session isn't live | `isSessionLive` returns false for "expired" after a second read; there's a test |
| 10 | B M-4: a failed restore blocks trading | the writeAll restore warns when it throws and sets a per-player flag; `ownRules` and take/give check the flag; there's a fault-seam test |
| 11 | UI-1: the tall/narrow PC window | `fitTrade` uses the 97 % rule when `gx / gy < 1.3` and reads the current TradeUI AbsoluteSize at every open; `phone_fit` covers 557x723 and two opens |
| 12 | The friends warning text | TradePresence says "friends list failed (AWAY friends hidden, trading and play go on)", or close to it |

Fix 1 also changes the spec. Once fix 1 is confirmed in the place, make two edits to
`docs/specs/2026-10-29-trading-design.md`:
- §4 Request limits: replace "after a decline, the same pair waits 30 s." with "after a decline, an expiry or an
  unanswered drop, the same pair waits 2 min (`PAIR_COOLDOWN`)."
- §6 "Request-bombing" row: replace "30 s cooldown after a decline" with "a 2 min pair cooldown after a decline, an
  expiry or an unanswered drop (keeping 3 slots full takes ~12 alts)".

If fix 2 landed, add this to §4 Rate limits: "READY / ACCEPT / BACK / CANCEL 1 per second per player; a call the
server's own copy already refuses costs no service call; a per-trade write budget (TradeConfig)."

## 2. Step 3: the full suite (TestFreshSave must be true before every Play)
Record pass/fail for each suite. The counts are the last ones in the ledger, before the Task 8 fixes. The new tests
raise them.

| Suite | Last known |
|---|---|
| SaveLockTests pure / live | 95/0 / 158/0 |
| TradeCoreTests | 32/0 |
| TradeItemsTests | 15/0 |
| TradePresenceTests pure / live | 18/18 / 12/12 |
| TradeSimTests partA / partB / crash / exploit / budget | 28/0 / 24/0 / 5/0 / 10/0 / 5/0 |
| TradeUITests | 15/15 |
| AutoReconnectTests server / unit | 79/0 / 83/0 |
| StreakTests, StarterPackTests (live parts) | regression: all pass |
| AdminServerTests | regression: all pass (fix 3 touches AdminServer) |

Re-run `budget` after fix 2 and put its numbers in the ledger. Fix any failure test-first, or report it with its cause
if it's pre-existing and unrelated to trading.

## 3. Step 4: the rest of the wrap-up
1. Delete the `_Studio` test keys, plus `studiotest_1793306247_1809064431` and every other `studiotest_` key made during
   this build (ledger, Task 0 line).
2. Set `workspace.TestFreshSave = false`. Do this only after the LAST Play test.
3. File > Save to Roblox. **Do NOT publish.** Check the new saved version through the saved-versions API.
4. Fill in the two `⟨pending⟩` sections of `OWNER-REPORT.md` ("Results" and "Test results") with the real numbers from
   step 2. Add the Task 8 rulings: PAIR_COOLDOWN 120, the 1/s button limit, the write budget, the `_G` gate, an expired
   session no longer holds busy locks.
5. Ledger: one line per fix outcome, then `Task 8: complete`.
