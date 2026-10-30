# Task 7 code re-review 1: fix round 1 (scoped)

Reviewer: Haiku, read-only (Studio Edit mode; no Play, no writes). Scope: each listed item in `task-7-code-review.md` (line numbers there are pre-fix), plus regressions next to each fix. Scripts read: `StarterPlayer.StarterPlayerScripts.TradeClient` (2,256 lines), `ServerStorage.TradeUITests` (1,136 lines), `StarterGui.MainMenu.MenuController` (line 30), `ServerScriptService.TradeCore`, and the server references needed to check the rules (`TradeNode`, `TradePresence`, `BaseHatchery`). The TradeCore diff against `ServerStorage._Backup_Trading.Before.TradeCore` was a read-only Luau line diff: only lines 225-227 changed.

## Verdicts

- **I-1 (closed view frees window + lock; Done shows by itself): Fixed with a new issue.**
  - Fixed: `renderTrade` closed branch (`TradeClient:1290-1308`) drops the view (`1294`) and closes at once unless the Done screen shows (`1295`). Done opens via `renderDone` (`1394-1400`). The 6 s fallback is at `1297-1302`. The lock is set only in `openTrade` (`1035`) and cleared only in `closeTrade` (`1044`).
  - New issue, Important: a late Done push can close or cover a NEW trade's live window. See New issues #1.
- **I-2 (not-trading / trade-over resyncs): Fixed.** `inTrade` (`1954-1963`) covers add, remove, ready, accept, back, cancel and chat; it closes, frees the lock and spawns `rebuild`. Server texts: `TradeNode:1472`, `1583`; `TradeCore:398`, `423`. Minor: see New issues #2.
- **I-3 (request cards dropped only for final reasons): Fixed.** `requestOver` (`1938-1943`) and `Client.respond` (`1944-1949`). Final texts match the server: "That request has expired" (`TradeNode:1385`, `1398`), "You're already trading" (`1396`, `1449`), "X is already trading" (`464`, `1449`), "X isn't online right now" (`1424`, `1440`), "Trade cancelled" (`1423`, `1433`, `1458`). The last three are after the request is consumed (`1408`), so they are truly final. Transient reasons keep the card. Minor: `TradeNode:1396` refuses before the request is consumed, so the server keeps it until expiry; a rebuild brings the card back (the test at `TradeUITests:860-868` asserts this).
- **M-1 (search note): Fixed.** `Menu.searchResult` (`1811-1831`) never sets the note for "Slow down". One retry after `TradeConfig.SEARCH_GAP` (= 2, read-only check), and `searchRetry` stops a second retry. Tested at `TradeUITests:881-886`.
- **M-3 (call timeout; keys cleared on respawn): Fixed.** `call` (`1881-1903`): 10 s timeout (`1880`, `1897`); a token-guarded free (`1900`); a late answer is dropped (`over`, `1892`); respawn clears `inflight` (`2084`).
- **M-4 (outgoing id captured at build): Fixed.** `sentId` (`1675`), used at `1688`.
- **M-5 (ENABLED ~= false everywhere): Fixed.** `MenuController:30` uses `~= false`. `TradeCore:227` is `== false`. `TradeNode:482` is `~= false`, and the kill checks `1169`, `1242`, `2094`, `2404`, `2511` are unchanged. `TradePresence:720-721` is unchanged (nil falls back to `C.ENABLED`, then `== false` refuses). See the note in New issues #3.
- **M-6 (ACCEPT on YOUR escrow): Fixed.** `tick` (`1517-1525`): "Securing items..." only when `not sec.you` (`1519-1520`). Server: `TradeCore.accept:350` checks `escrowedNow(s, side)` for your side only; `toCommit:368` checks both. Consistent.
- **M-7 (new tests): Fixed.** All 8 new tests are in `NAMES` (`TradeUITests:378-380`) and defined: `hotbar_state` (583), `closed_view_closes` (613), `accept_gate` (654), `kill_switch` (676), `rebuild_after_respawn` (730; real death via `bot kill` 162-167; ResetOnSpawn asserted at 733-736; screens removed at 764), `request_refusals` (841), `not_trading_resyncs` (903), `inventory_matches_server` (947). Gap: no test for a late Done push during a new live trade (New issues #1). M-8 has no test (the builder says so).
- **M-8 (wiring before the MainMenu wait): Fixed.** The page is built in `task.spawn` (`1572-1573`); stand-ins (`1557-1571`) keep your request. Wiring, pushes (`2046-2065`), `rebuild` (`2079-2080`) and the Heartbeat (`2098`) do not wait for MainMenu.
- **M-9 (respond id type check): Fixed.** `goodId` (`1927`) gates `cancelRequest` (`1929`) and `respond` (`1945`, which also checks `yes` is a boolean).
- **M-10 (previous Backpack state restored): Fixed.** `setHotbar` (`982-994`) hides only an enabled hotbar and restores only one the trade hid (`TradeHotbarHidden`). Called from `openTrade` (`1036`), `closeTrade` (`1045`) and the Heartbeat (`2101`).
- **M-2 (server totals preferred): Fixed.** `renderTrade` uses `v.total` (`1324`, `1328-1329`, `1345-1346`). `renderDone` uses the server totals when the last view is this trade's closed done view with the same cards (`1408-1412`). The sums left (`sumPs` `1270-1274`, fallback `1412`, inventory `ps` `1087`) are display-only; nothing is sent back.
- **Inventory parity: Fixed.** `myItems` (`1068-1103`) matches `BaseHatchery.describe` (`1178-1202`: a duplicate id gives nil at `1185`; `usable` at `507-509` is CreatureConfig + model). Eggs match the template check (`1192`) and `eggSig` / `validKg`. `EGG_AREA` (`72`) equals the seven `ServerStorage.Assets.Eggs` templates (read-only check). Minor: see New issues #4.

## Other checks

- **Lock cannot strand the player:** the only way the window stays open with the lock set is `done.Visible`, which OK (`1466-1470`) or X (`onClose`, `1549`) releases. No stuck path found.
- **Views race (state fix):** `rebuild` (`2017-2043`) skips the trade part if a view arrived during its call (`Client.views`, `1289`, `2022`, `2025`). Verified.

## New issues

1. **Important (must fix): a late Done push can close or cover a NEW trade's live window.**
   - `renderDone`, non-completed branch: `closeTrade()` runs unconditionally (`TradeClient:1384-1385`). Completed branch: `view = nil` and the Done screen is drawn over whatever window is open (`1394-1400`).
   - The server releases the busy locks as soon as a trade ends (`TradeNode:941-945`). But a cancelled trade's Done push waits for settle when the other side has escrow (`TradeNode:933-937`; `pushDone` at `1910`, called from `settle` at `1948`).
   - So a new trade can open before the old Done push lands. That push then closes it (lock freed, live view kept). Nothing reopens it until the next push.
   - Fix: in `renderDone`, return when `view ~= nil` (a live trade is on screen). The closed view for the same trade always arrives first (`TradeNode:928` before `935`; the closed done view before settle's push at `1910`). Add a test: live view, then a cancelled Done push, and the window stays open.
2. **Minor: the GONE toast overwrites the reason.** `inTrade` shows "You're not trading" (`TradeClient:1958`) even when the window is already closed. That replaces the closed view's reason toast (`1304`). Fix: skip the toast when `tradeGui.Enabled` was already false.
3. **Note for the lead (not a defect under the stated rule): a missing ENABLED now allows new sessions in TradeCore too.** Before, `TradeCore` refused nil. Now only an explicit `false` refuses (`TradeCore:227`). Explicit false still refuses everywhere it did (`TradeNode:2404` refuses every op, `2094` fails Phase 2 entry, `2511` ends live trades; `TradePresence:720-721`). `settle` (`TradeNode:1934-1956`) has no kill-switch gate, so recovery and settle still run. Decide whether a missing key should fail closed; `TradeConfig.ENABLED = true` is explicit today, so there is no current effect.
4. **Minor: `EGG_AREA` is a hand-copied list** (`TradeClient:72`). A new egg template would be hidden until someone updates it. The inventory test catches that.
- Also minor: `renderDone`'s non-completed branch (`1384-1392`) does not clear `view`. A stale `view` is harmless while the window is closed, but it is inconsistent with the closed-view path.

The single Important item is New issues #1; fix it and add its test, then this round can be approved.

**Verdict: Needs fixes**
