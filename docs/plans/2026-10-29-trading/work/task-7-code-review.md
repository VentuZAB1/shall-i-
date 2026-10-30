# Task 7 code review: trading UI (TradeClient, MenuController, AdminClient, PetsEggsUI, SellClient, UpgradeClientLegacy, WeatherClient)

Reviewer: Haiku, code review only (Studio read-only; no Play sessions, no writes). Scope: correctness, spec compliance, security, regressions. Screen looks are scored separately and were not judged here.

Method: read the full `StarterPlayer.StarterPlayerScripts.TradeClient` (2,109 lines), `ServerStorage.TradeUITests` (649 lines), the TradeUIPreview module, `ReplicatedStorage.TradeConfig`, and the server trade modules (`TradeNode`, `TradeCore`) by grep. A line diff of each changed script against its `ServerStorage._Backup_Trading.Before` copy, done by a read-only Luau query over `.Source`. The task 5 Remote API / Push schema, the task 6 Done Push and the task 3 describe rules were read from the reports. I did not run any test suite. Studio was in Play when the review began and later returned to Edit; I started and stopped no session.

## Spec Compliance

- [PASS] Op names and argument types match the task 5 Remote API (`TradeClient:1783-1785` remote map, `1816-1877` wrappers). `send` uid is a whole number (1817). `respond` takes a boolean (1828). `cancelRequest` takes the request id (1823). `add` takes a ref table (1836). `remove` takes an index 1..9 (1841-1842). `ready` / `accept` take the whole `view.ver` (1857). `chat` takes 1..6 (1872). `search` takes a string (1884). `list`, `history`, `state` take no arguments. An egg ref carries the exact kg from the client's own EggInventory (`1056`, `1069`).
- [PASS] All seven push kinds are handled in `Client.onPush` (`1919-1938`): trade, done, request, requestGone, outgoing, outgoingGone, toast.
- [PASS] Countdowns are seconds-left, counted on the client clock from arrival (`leftOf` `969-972`; request cards `949-950`).
- [PASS] `TradeConfig.PHRASES` is read in the spec order (`TradeConfig:33`). `MAX_ITEMS` 9, `CHAT_LINES` 8, `REQUEST_TTL` 30, `ENABLED` true.
- [ISSUES] The closed `phase = "done"` view is not handled (Important I-1). A refused back / cancel does not resync the window (Important I-2).
- [PASS] Modal lock: `openWindow` refuses and fires `TradeUI.Locked` (`MenuController:318-323`); PetsEggsUI `setOpen` refuses to open (`PetsEggsUI:508-513`); SellClient `373`; UpgradeClientLegacy `307`; WeatherClient skips cutscenes (`77`); TradeUI DisplayOrder 130 (`TradeClient:372`). Trade opening fires `CloseWindow` and `WindowOpened("Trade")` (`1011-1014`). I did not read the bodies of the Sell and Upgrade `WindowOpened` listeners (SellClient:396, UpgradeClientLegacy:326), so whether an already-open walk-in window closes is unverified.
- [PASS] Respawn: TradeUI, TradeRequests and TradeToast all use `ResetOnSpawn = false` (`369`, `855`, `720`). `rebuild` runs at start (`1951-1954`) and after `CharacterAdded` (`1956`), and rebuilds from `state` (`1897-1916`).
- [PASS] The admin button placement changed only in `placeButton` (`AdminClient` diff: lines 615-630 and 634-641 of the live script). Admin gating is unchanged. The ADMIN button sits in the Trading tile's row, below Index.
- [PASS] The five named tests exist (`TradeUITests:230`): menu_regression, trade_window_modal, rebuild_after_respawn, request_card_stack, ui_trade_end_to_end. The end-to-end test checks conservation (`605-607`) and deep-compares the last view and Done push against the server (`608-611`).
- [CANNOT VERIFY] Inventory source. The client lists `BaseData.pets` + `PetInventory` for pets and `EggInventory` for eggs (`1040-1059`), which matches the task 3 `describe` lookup. The brief's "equipped / placed" exclusion rule is not stated in `task-3-report.md`, so I could not confirm that non-offerable pets are hidden.
- [PASS] The Studio preview is gated: `Client.useFolder` (`1957-1963`) and the `TradePreview` BindableFunction (`2001-2108`) exist only under `if STUDIO`. `ReplicatedStorage.TradeUIPreview` does not exist in Edit (only as a Play copy). `ServerStorage.TradeUIPreview` is required by no live script.

## Strengths

- Every op goes through one `call(key, op, ...)` with an in-flight key (`1787-1798`). The double-press test asserts one `ready` call for two presses (`TradeUITests:563-574`).
- Argument checks happen before any call (`whole()` at `1806`; `withVer` at `1855-1861`). The server's own checks remain authoritative.
- Display text from the server or from players is escaped (`esc` on names and chat, e.g. `930`, `1219`, `1264`).
- The six changed existing scripts were changed only where needed. Each removed line is a replaced line (the HEADER_THEME / TITLES / LAYOUT entries and the old admin placement). No logic was dropped.
- The `TradeSimTests` harness change is a test-only hook (`TradeSimTests:253-254`) and an export (`3321`). Nothing live requires it.

## Issues

### Critical (must fix)

None found. No client path decides or computes items, counts or prices that the server then trusts; every op is re-validated by the server; and the Studio preview cannot run live.

### Important (should fix)

**I-1. A closed `done` view leaves the trade window half-live, and the lock stays until the Done push.**
- `TradeClient:1249-1258`: `renderTrade` sets `view = v` (`1247`) and, for a closed view with phase `done`, returns without closing. The window and the `TradeWindowOpen` lock stay.
- `TradeClient:1452-1468` then renders Phase 2 controls from that view. BACK stays enabled (`1468`, because the phase is not `commit`). ACCEPT shows "Securing items..." (`1462`). The timer reads "Ends in 0:00" in red (`1418-1420`).
- The server sends this closed view when the trade reaches phase done (`TradeNode:892-894`, `v.closed = true`, `why = "Trade complete!"`). The Done push comes later from the settle (`TradeNode:1910`).
- Result: the window shows stale, partly live controls for the whole settle time. If the Done push is lost, the window and the lock persist until respawn. The tests never send a closed `done` view (the end-to-end test waits for the Done screen).
- Fix: treat phase `done` as a waiting state (BACK off, "Completing..."), close on the Done push, and do not keep a closed view as the live `view`.

**I-2. No resync when the server says the trade is not active.**
- `onClose` (`1489-1491`) sends `cancel` whenever `view` is non-nil. `Client.cancel` / `back` / `accept` / `ready` (`1863-1870`, `1855-1861`) only show the refusal (`shown`, `1800-1805`).
- The server answers "You're not trading" (`TradeNode:1472`, `1583`). The window stays open and `TradeWindowOpen` stays set. [X] and BACK then do nothing except show a toast.
- Fix: on "You're not trading" from cancel / back / accept / ready, clear `view` and close the window (or call `rebuild`).
- The tests do not cover this path (`TradeUITests:434-466`, `521-615` exercise only the normal paths).

**I-3. A refused ACCEPT removes a live request card.**
- `Client.respond` (`1831`) calls `removeRequest(id)` for every refusal except "Slow down" and "Syncing... try again".
- So "Wait Ns", "Your items are still loading", "Reconnecting...", "Your inventory is full" and the call failure "Try again in a moment" (`1796`) all remove the card. The request stays pending on the server for up to 30 s, and the player can get it back only by respawn (rebuild, `1906-1913`).
- Fix: remove the card only when the request is accepted, declined, expired, or gone (`requestGone` already covers the gone case).

### Minor (nice to have)

- **M-1.** `Client.search` refusals show "Slow down" as the list note (`1883-1888` → `Menu.searchResult` `1737-1745` sets `searchNote` → shown at `1665-1666`). Lists and history skip "Slow down"; search should too.
- **M-2.** Money is summed on the client. The Done header $/s and the Net figure sum card `ps` (`sumPs` `1229-1233`; header `1366-1367`; Net `1402`), and inventory $/s uses `CreatureConfig.petIncome` locally (`1046-1047`). This is display only, but the brief says no price is computed on the client. Use server totals or document it.
- **M-3.** `call()` has no timeout (`1787-1798`). An `InvokeServer` that never returns keeps its in-flight key set, so that button stays dead; respawn does not clear `Client.inflight`.
- **M-4.** The CANCEL button on a sent row reads `outgoing.id` at click time (`1615`). If `outgoingGone` clears `outgoing` between redraw and click, this errors. Capture the id when the row is built.
- **M-5.** Kill-switch default mismatch. MenuController tests `ENABLED == true` (the Trading tile block, lines 29-30), while `TradeNode:482` uses `~= false` and `TradeCore:225` uses `not C.ENABLED`. Same result today; align the rule.
- **M-6.** ACCEPT also waits for `secured.them` (`1461-1462`), and shows "Securing items..." even when your own escrow is saved. The brief says ACCEPT needs yours. Confirm the stricter behaviour is intended.
- **M-7.** Test gaps: no test for the closed `done` view (I-1), a refused back / cancel (I-2), the kill switch (ENABLED false means no tile), or that the three ScreenGuis use `ResetOnSpawn = false`. `rebuild_after_respawn` simulates a wipe with `hide` (`TradeUITests:451`) rather than removing the ScreenGui.
- **M-8.** The Trade page IIFE yields on `pg:WaitForChild("MainMenu")` (`1501-1502`) before the server wiring (`1782+`) and the Heartbeat (`1968`) are set up. A late MainMenu delays all trade wiring.
- **M-9.** `Client.respond` checks `yes` but not `id` (`1828`). The server validates it, so nothing is exposed.
- **M-10.** `closeTrade` re-enables the Backpack (`TradeClient:1029`) even if another system had disabled it. Restore the previous state instead.

## Assessment

**Task quality:** Needs fixes.

**Reasoning:** No Critical findings: the ops and types match the contract, the server re-validates everything, and the preview is Studio-only. But I-1 and I-2 can leave the trade window and the modal lock stuck until respawn when a push is late or lost, and I-3 drops a live request card. The tests miss all three.
