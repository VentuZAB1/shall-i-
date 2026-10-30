# Review: HATCH NIGHT Starter Pack popup + Shop plan (2026-10-21)

Plan: `docs/plans/2026-10-21-hatch-night-popup-shop.md` (966 lines). Reviewer: plan reviewer (read-only).

**Inputs I read:**
- the plan, all of it;
- the mockups: `popup_pc`, `popup_phone`, `popup_restricted_pc`, `popup_thanks_pc`, `shop_top_pc`, `shop_top_phone`, `shop_speed_pc`, `shop_potions_pc`, `shop_bottom_pc`, `shop_gift_pc`, `sheet.png`, and `qa_report.txt`;
- the old look: `hatch_shop_before.jpg` and `starter_popup_v3_magma.jpg`;
- the built Gift window `v2_pc_mid.jpg`, the Gift plan review, and spec section 2.3;
- the owner references `starter_reference_owner*.webp`;
- the memory notes for the Shop, the Starter Pack, HATCH NIGHT, the layout rules and the analytics.

**Code I read in Studio** (script_read / script_grep only; Studio was in Edit; I wrote nothing):
- ShopClient (all of it), StarterPackClient (all of it), StarterPackHud (contract parts), MenuController (all of it);
- BrickUI (tail) and BrickUI.Hatch (lines 1-793);
- SpeedBoostCards, ShopServer (refusal strings), StarterPackServer, Receipts (tail), Analytics (Shop funnel), AnalyticsServer (UI handler);
- PetsEggsUI (GET MORE), StarterPackTests (live part);
- the test files `hatch_chrome_snapshot.lua`, `hatch_containment.lua`, `starter_hud_client.lua`.

## Verdict: **APPROVE WITH CHANGES**

The plan is precise and most of its numbers check out (verified table below). The design is consistent with the built Gift window, and the popup is a clear step up from the old one.

There are 11 required changes, three of them functional bugs:
- **The Shop gets smaller than today on PC.** At 1920x1080 it goes from about 1239x774 to 873x555, which is about half the area. The owner's 2026-10-05 rule was that the Shop is BIG.
- **The open/close lifecycle hangs off `page.Visible` only.** After closing with X and reopening, the refresh loop never restarts, the page doesn't go back to the top, and the gift picker stays open.
- **Three `robux()` calls lose their InfoType.** That means wrong or non-regional prices.

---

## Verified (no change needed)

| Claim in the plan | Result |
|---|---|
| Planner's open question: `TestReceipt` / `StarterDebug` | Both exist, but **only at runtime, in the Play SERVER DataModel**, never in Edit. See MUST 9 for the exact signatures. |
| `MenuController` line 242 = `hatch.setTheme(H.bandTheme())`; BrickUI line 512 = `PAGE_SKIN = {Gift = "Hatch"}` | yes |
| `B.Hatch` is nil when the child module fails | yes: BrickUI 514-517 uses `pcall(require, ...)` and leaves `B.Hatch` nil. Then MenuController's `hatch` is nil and every page uses Check-UI (line 239). |
| D6: no live script but ShopClient uses SpeedBoostCards | yes. Only `_Backup_Monetization.Round3.UpgradeClient` references it. |
| `SpeedBoostCards.CARDS` fields (`title()` / `sub()` / `buy` / `id` / `price` / `best`) | yes. `buy` = `{"speedPack","Speed15m"}`, `{"potion","Speed3"}`, `{"speedPack","Speed2h"}`. |
| B2 remote args | They match today's ShopClient: lines 225, 236, 279, 295-296, 308 and 528, and StarterPackClient line 384. |
| Section 3 fit rows | They match the Gift review's verified rows. `H.fitWindow(guiW, guiH, leftClear, cap)` already takes a `cap` (default 1.18): see MUST 1. |
| 4.3 y table | I re-added it: 142 / 178 / 336 / 504 / 540 / 672 / 866 / 902 / 1086 / 1280 / 1316 / 1458 / 1494 / 1618 (+8 = 1626, CanvasH 1634, max 1248). The -142 column also checks out. |
| 4.12 margins | Re-derived: popup Buy at 1.02, right edge 737.5; NoThanks 228.7 vs Buy 230.6; Pass Buy hover 280.6. All correct. |
| Analytics: Face/Body stay `Visible` on Hatch pages | yes. `applySkin` only changes transparency and size (MenuController 87-94), so an event-driven `onScreen()` works. |
| The HUD "no odds path = no offer" rule | yes. StarterPackHud line 358 requires `StarterPackUI.Open`, and line 615 waits for it. |
| Chrome snapshot v1 includes `Window.ShopTabs` and `Body.GiftPicker` in **every** section | yes. The walker only skips `HatchBack`/`HatchFront` and `Body.*Page`/`Message`. So D16 (filter v2 plus a new BEFORE) is needed. |
| `chrome.setTheme` hides the bats for any band but Pumpkin | yes (Hatch line 775). With `bats = false` on the popup, no bat loop can run while it is closed. Holder.Visible never changes, so this matters. |

---

## MUST changes

### 1. The Shop must be at least as big as today on PC: per-page cap

**Today's Shop** comes from MenuController `LAYOUT.Shop = {2.0, 1.6, 0.11}`. `Window.BaseSize` is `{0.3229,0},{0.4074,0}` (Gift review), and the aspect constraint is DominantAxis Height. So the window's height is about 0.76-0.83 of the gui height, and its width is 1.6x that:
- memory, 1080p: about **1239 x 774**;
- `hatch_shop_before.jpg` at 1519x753: **914 x 575**.

**The plan's Shop** uses the shared 1.18 cap:

| Screen | Old Shop | Planned Shop | Old Shop / planned |
|---|---|---|---|
| 1920x1080 | ~1239 x 774 | 873 x 555 | 70 % linear, 49 % area |
| 1519x753 (Studio) | 914 x 575 | 873 x 555 | 95 % |
| 844x390 phone | ~451 x 282 | 526 x 334 | the new one is bigger |

At 1080p, the most common PC screen, text shrinks too. A pass title was about 35 px; at 22 x 1.18 it is 26 px.

**Required:**
1. Add to `BrickUI.Hatch` (additive): `function H.pageCap(page, guiH) if page == "Shop" then return math.max(1.18, 0.80 * guiH / H.H) end return nil end`.
2. MenuController line 105 becomes: `local s, w, h, cx, cy = H.fitWindow(gs.X, gs.Y, math.max(rightEdge(menu), rightEdge(pills)) + 6, H.pageCap(openName, gs.Y))`.
   - `openName` is already set when `hatchFit()` runs, from both `openWindow` and the ViewportSize handler.
   - This is the only other MenuController line that changes (2 lines total). Update sections 1 and 6.3.
3. **Task 0:** measure today's Check-UI Shop as `win.AbsoluteSize.Y / mm.AbsoluteSize.Y` and write it in the ledger.
   - If it is above 0.80, use the measured ratio as R in place of 0.80.
4. **What the change gives:**
   - At 1920x1080: s = 1.739, window 1287 x 817, cx 1055.5. That clears the HUD: `lo = 412.1 + 643.5`.
   - Text: min 27.8 px; prices 38-49 px.
   - Phones are unchanged at 0.7106: the height term gives 0.59, so the 1.18 cap and the width limit win.
   - **Gift, the popup and the toasts are unchanged:** `pageCap` returns nil for them. So `hatch_gift_snapshot` must stay byte-identical.
5. **Tests:**
   - `hatch_pure.lua`:
     - `pageCap("Shop", 1022) = 1.739`;
     - `fitWindow(1920, 1022, 412.1, 1.739)` gives `(1.739, 1286.9, 817.3, 1055.55, 511)`;
     - `pageCap("Shop", 346)` gives 1.18;
     - `pageCap("Gift", 1022) == nil`.
   - **Containment:** add a forced `HatchTestScale = 1.45` run to S1 and S2. 1.45 is the largest scale that fits the 1519x753 Studio viewport.
6. **Owner-facing note:** the Shop is deliberately bigger than the other HATCH NIGHT windows on big screens (owner, 2026-10-05: "it looks too small").

### 2. Run the open/close lifecycle on ONE "on screen" signal, not on `page.Visible`

`closeWindow` (MenuController 200-206) only hides `Window`, so `ShopPage.Visible` stays true. Reopening the Shop therefore changes no page `Visible` either. As planned (6.4 "On `page.Visible` true ..."):
- **The refresh loop never restarts** after X then reopen. `win.Visible` went false, so the loop exited. OWNED, prices and treadmill state go stale.
- **7.3 check 5** ("Reopen -> top (0), FEATURED") fails.
- **7.3 check 6** ("Close the Shop -> picker hidden, `#pickerConns == 0`") fails. The picker stays open behind the closed window, with its connections.
- StreakClient already learned this: it connects both `page.Visible` and `win.Visible` (StreakClient 880-881).

**Required:**
1. Use one `onScreen()`: page, Body, Face and Window all `Visible`, and `MainMenu.Enabled`.
2. Connect one `sync()` to those 4 `Visible` signals plus `MainMenu.Enabled`.
3. `sync()` keeps `shown` state and does nothing when it doesn't change. On a change:
   - **true:** `token += 1`, CanvasPosition 0, clear `activeName` and the pressed tab, `refresh()`, `updateActive()`, snap the Pill, `task.spawn(loop, token)`.
   - **false:** `token += 1` (the loop exits), `closePicker()`.
   - **Then, both ways:** the analytics fire, with `ShopFunnelSent`.
4. The loop is `while token == my do refresh() task.wait(0.3) end`.
5. StarterPackClient's `cardShown()` / ticker / card pulse use the same condition, plus `MainMenu.Enabled`.
6. Add **B21**: "every open, including X then reopen, starts at the top, refreshes, restarts the loop and closes the picker". Test it in 7.3 check 5: close with `CloseWindow:Fire()`, reopen, then:
   - `ShopLoop == true`;
   - a `Pass_VIP` toggle shows OWNED within 0.6 s.

### 3. Every `robux()` call keeps its InfoType

`robux(id, fallback, infoType)` passes `infoType` to `GetProductInfo`, which defaults to `Asset` when it is nil. These plan calls drop it:
- 4.6 boosts: `robux(CARDS[key].id, CARDS[key].price)`;
- 4.8 treadmill: `robux(TreadmillProducts[tier+1] or 0, ...)`;
- 4.9 eggs: `robux(GrowAllProduct, GrowAllPrice)`.

With Asset, a developer-product id is looked up as an asset, a different id namespace. The result is the fallback (no regional price) or a wrong number.

**Required:**
1. `Enum.InfoType.GamePass` for passes.
2. `Enum.InfoType.Product` for everything else: Double ladder step, boosts, packs, treadmill Robux, Grow All and gift ids.
3. B4 / 7.3 check 3 compare each label with `GetProductInfo(id, <that InfoType>).PriceInRobux`. Assert at least one boost and the Grow All label equal that live value. In Studio the live value can differ from the ShopConfig fallback, because prices were halved on 2026-10-13.

### 4. `priceButton.setPrice` must step the price size down to fit

The 112-wide treadmill Robux button fails the plan's own S5 check with a 4-digit price. At @26: `G = 26 + 6 + (textWidth("1499",26) ≈ 68 + 6) ≈ 106`, but the room is `112 - 16 = 96`. The group then starts at x ≈ 3, so "price right + stroke <= face right - 4" fails.

**Required:**
1. Add to `setPrice`: `for sz = opts.size, math.max(16, opts.size - 8), -1 do (compute G with sz) if G <= w - 16 then break end end`.
   - Set `Price.TextSize = sz`. Keep the glyph size, and remember `sz`.
2. 7.1 check 5 adds `w 112, glyph 26, size 26, "1499"`: G must be at most 96, and the size about 23 (the Task 2 width table decides).

### 5. Refusal words need a short variant for "Not enough money"

Section 6.2.8 gives `setWord = H.fit(word, {s, "TRY AGAIN"})`. On the 112-wide treadmill **Money** button, "NEED MORE $!" is about 115 px even at 16, and the room is 107. So the most common refusal on the main money button would read "TRY AGAIN", which tells the player the wrong thing.

**Required:**
1. Map `result()` as:
   - "Not enough money" -> `{"NEED MORE $!", "NEED $!"}`;
   - any other message -> `{MSG:upper(), "TRY AGAIN"}`.
2. S4 holds the TreadMoney refusal and checks that the word is NEED MORE $! or NEED $!, with `textFits` true.

### 6. Picker rows must not leak through `H.buttons`

`H.glossButton` does `table.insert(H.buttons, btn)` (Hatch line 333) and never removes it. Every `buildPicker` creates new row `priceButton`s, on each open, on PlayerAdded/Removing and on every attribute change. Each one is kept forever in that module table, together with its closures and destroyed instances. In a long session this is an unbounded leak, and `H.setTestHover` walks dead buttons.

**Required:**
1. Pick one of these, additive (the default path is unchanged for existing callers):
   - `opts.transient = true`: the button is not registered;
   - or `holder.Destroying:Once(...)` removes it from `H.buttons`.
2. Use it for picker rows.
3. 7.7 check 4 adds a Studio probe `HatchButtons = #H.buttons`. It must be flat after the 30 cycles.

### 7. Long player names never leave their boxes

- **Picker rows:**
  - A 20-character DisplayName @16 is about 230 px, and "@" plus a 20-character username is about 195 px. The room is 171 (box 176 minus stroke).
  - `H.fit` gives up at 16 and draws past x 238, into the Gift price button.
  - **Required:** after `H.fit`, set `Name.TextTruncate = User.TextTruncate = Enum.TextTruncate.AtEnd`.
- **Toasts (4.11):**
  - `TextScaled = false` at a fixed 28 in a 600 box. "<20-char NAME> GIFTED YOU X2 GROWTH!" is about 740 px.
  - **Required:** use `H.fit` variants (full; then the name cut to 12 characters plus "..."), with min 18, and `TextTruncate = AtEnd` as the last guard.
- **Tests:**
  - S6 sets `TestPickerRows` names to a 20-character string.
  - B6 fires `Gifted` with a 20-character name.
  - Both need `textWidth` and `textFits` to pass.

### 8. Tabs: a pressed tab wins over the scroll clamp, and fix S2

Max scroll is 1248 (1106 with the slot hidden), so the TREADMILL header (1280 / 1138) can never reach the top:
- `scrollTo("TREADMILL")` clamps to the max.
- The 4.3 rule "`scrollY >= max - 2` -> EGGS" then lights **EGGS** after a TREADMILL press.
- S2 lists "TREADMILL (1280)", a scroll position that cannot exist.

**Required:**
1. **A pressed tab wins:** the Pill and label go to the pressed tab at once. `updateActive()` is ignored until the user scrolls away, meaning that after the tween completes, CanvasPosition differs from the tween target by more than 2 logical px.
2. **Manual scrolling** keeps the 4.3 rule.
3. **The default is FEATURED** when no header is above the line. With the slot shown, PASSES is at 142 and the line is 135 at scroll 0.
4. **S2 positions** become top, 504, 866 and bottom (1248).
5. **New test (7.3 check 5):** `Tab_TREADMILL` puts the Pill on TREADMILL.

### 9. Task 0: the real test tools, and the forbidden calls

Fix Task 0's second bullet and the 7.0 rules as follows.

**Test tools (all created at runtime, Studio only):**

| Tool | Created by | Call | Notes |
|---|---|---|---|
| `ServerStorage.TestReceipt` (BindableFunction) | ModuleScript `ServerScriptService.Receipts`, lines 80-95, when first required | `:Invoke(player, productId)` | Runs that product's handler and returns its result. No prompt. |
| `ServerStorage.TestProcessReceipt` | the same | `:Invoke(player, productId, purchaseId)` | Returns the decision name. |
| `ServerStorage.StarterDebug` | `ServerScriptService.StarterPackServer`, lines 158-190 | `:Invoke(op, player, value)` | ops below |

**StarterDebug ops:**
- `reset`;
- `endsAt` (value = `os.time()` based);
- `restricted` (value `true`/`false`; restore with `nil`);
- `seen`;
- `grant` (gives the egg, potions and cash, and fires `Shop.Granted`);
- `buy`.

**Where to check them:** they exist only in the **Server DataModel during Play**. Check them there, not in Edit. Only `StarterPackTests` is checked in Edit.

**Forbidden:**
- `StarterDebug "buy"` while the offer is active and not owned. It calls the real `MarketplaceService:PromptProductPurchase` (StarterPackServer line 126). StarterPackTests only uses it in states that refuse.
- 7.3 check 4's real `TreadMoney` press runs only after asserting `Money < TreadmillMoney[tier + 1]`. A `grant` earlier in the session gives an hour of income, and the press would then really buy a treadmill tier.

### 10. Make the fallback safe, and test it once

D15 is safe as written: on `B.Hatch == nil`, ShopClient returns before building anything. Two holes remain, plus a never-run path.

**Required:**
1. **Enable the right copy.** ShopClient enables `script.Parent:FindFirstChild("ShopClientLegacy")`, the PlayerScripts copy. Setting `StarterPlayer.StarterPlayerScripts.ShopClientLegacy.Enabled` from the client does nothing for this player.
2. **Wrap the build in `pcall`.**
   - Hook remote handlers (`Gifted`, `Granted`, analytics) only after the build succeeds.
   - On H == nil, a build error, or the Studio switch `workspace.TestShopLegacy == true`, do this in order:
     - (a) destroy everything this script created (ShopPage, GiftToast);
     - (b) `B.PAGE_SKIN.Shop = nil`, so MenuController shows the legacy page on Check-UI and not inside the night shell (the module table is shared on the client);
     - (c) enable the legacy copy.
3. **Test the fallback** (new 7.3 check 10, its own session with `TestShopLegacy = true`):
   - the Check-UI Shop opens with its side tabs;
   - there is exactly one `Body.ShopPage` and one `PlayerGui.GiftToast`;
   - a dry-run-free tab press scrolls.
4. **Every normal run** (7.3 check 1) asserts:
   - `PlayerScripts.ShopClientLegacy.Enabled == false`;
   - one `ShopPage`;
   - one `GiftToast`.
5. **Fix the 6.6 contradiction:** "header comment" vs "byte-identical source". Keep the source byte-identical, and put the note in an attribute `Note`.

### 11. Test hooks must not be able to open a real Robux prompt

Make D14 enforced in code, not just a rule. In Studio:
- `ShopPage.TestPress` for any Robux key, `TestGiftRow`, `StarterSlot.TestPress` and `StarterPackUI.TestBuy` do `warn(...)` and return **unless `TestDryRun == true`**.
- Only `TreadMoney` (in-game money) and `Tab_*` run for real.
- Today `TestBuy` presses the real BUY (StarterPackClient 556-559). No test file relies on that.

---

## SHOULD changes

### Owner taste (premium vs basic)

1. **More juice on the dark cards.** The mockups read premium at the CTA level (gold buttons, big prices), but the Shop cards are much calmer than the owner's references, which are saturated and frameless, and than the old coloured pass cards. Two changes:
   - raise the art glows: pass cards to `ImageTransparency 0.4`, boosts and packs to 0.45, wide cards to 0.4;
   - tint each pass card's face gradient top with 15 % of `p.face[1]`, so Growth / Money / VIP / Speed keep their identity colours.
   - The visual reviewer should compare against `starter_reference_owner*.webp` specifically for "basic".
2. **Owned popup:** hide `EndsIn` in the THANK YOU state (a running timer after purchase reads oddly), and cap `PopScale` at **1.08**, as today. At 1.15 the hero's EggOutline (bottom 280) reaches about 292.6 and PotionMoney about 291.6, which crosses OddsCaption (288) during the pop. At 1.08 they reach 286.7 and 285.7.

### Robustness

3. **`mySign()` must be nil-safe.** Today it reads `workspace.Map.Hub:FindFirstChild(...)`, which errors if `Map` exists without `Hub`. Another agent is rebuilding the hub right now, and the error would kill refresh.
   - Use `local hub = map and map:FindFirstChild("Hub")`.
   - Call `refresh()` through `pcall` (log once) so one section cannot freeze the others.
   - Add **B26**: the treadmill card works with no sign. It shows "x1 > ?", as today.
4. **StarterPackClient's slot chain:** give every `WaitForChild` a timeout (`ShopPage` 60, then `Scroll`, `List` and `StarterSlot` 10 each), inside `task.spawn`. ShopClient builds the whole page tree off-screen and parents `ShopPage` to Body last.
5. **The ticker also refreshes `CashRow.Line2`** (cash depends on `IncomePerSec`), as today's 0.5 s loop does (StarterPackClient 476).
6. **Popup re-fit:** listen to `mm:GetPropertyChangedSignal("AbsoluteSize")` while enabled, not ViewportSize. MainMenu's box updates after the viewport. Cancel a running Size tween before re-fitting.
7. **Offer expiry while the Shop is open:** re-layout (-142), clamp CanvasPosition to the new max, and recompute the active tab. Add this as **B24**.
8. **Policy answer while the popup is open:** flip `StarterDebug "restricted"` true then false while open, and assert the odds appear live. Add this as **B23**; it is an odds-rule case.
9. **Data-driven counts:** build passes and packs from `ShopConfig.Passes` / `PotionPacks`, grouping packs by `count`. `layout()` takes `#Passes`, and asserts plus warns if the counts are not 4 and 6, so a new item is never silently dropped.

### Clarity (things a builder would guess at)

10. **Popup chrome:**
    - call `chrome.show(true)` once after building;
    - use `chrome.setTheme(H.bandTheme("StarterPack"))`, not a hard-coded `"Shop"`, so owner's call 1 applies to both.
11. **Pulse period:**
    - D12 says 1.6 s, but `btn.pulse` hard-codes 1.2. Add `opts.pulsePeriod` (default 1.2).
    - 7.1 check 6 then expects `pulse(0.8) -> 1.02` for the 1.6 s button.
12. **Treadmill Now/Next text** is `NowName` / `NextName` verbatim; they already include the "x". The `Next` box width is `textWidth + 8`, not 120, and it must end at 318 or less (treadmill) or 396 or less (Double).
13. **Card Line3** is `"+ BIG " .. areaName():upper() .. " EGG!"` (upper case).
14. **`H.chip` defaults:** it sets ZIndex 10 and `HatchTile "chips"`. Popup rows must override these to Z4 and `"rows"` after creation.
15. **The 6.2 diff rule:** list all changed old lines:
    - the `H.corner` lines in recess and chip;
    - the TopShade / BottomLine lines;
    - the shellCard Hit and gradient lines;
    - the pulse expression;
    - the bandTheme body.
    The rule is: "each changed line reduces to the old expression when the new opt is nil".
16. **Hero frame:** the plan gives it 270 x 270, centred at (155, 196), so it overlaps the caption and odds as a box. Say it is a transparent container, skipped by every overlap check. Or size it to the children's union: x 30..280, y 90..310.
17. **Picker Box:** the `shellCard` hover (white overlay plus icon tilt) shouldn't run on a dialog. Add `opts.noHover`, or disconnect it.
18. **`TestPress` keys:** the tab keys are `Tab_PASSES|SPEED|POTIONS|TREADMILL|EGGS`. Say whether `Tab_FEATURED` is an alias.

### Tests

19. **Containment v2:**
    - `hitFirst` probes only hits whose **centre** is inside the scroll's visible box.
    - Add a `textClear` check: inside each card face, every visible text glyph box plus its stroke must not meet a glossButton holder box (stroked), at rest and at hover.
    - The small cards' Sub (box 114..132) and Buy (stroked top 131.5, 130.9 at hover) touch today. If `textClear` fails, shift them: Art y 30, Title y 88, Sub y 110.
20. **7.4 check 9 (auto-popup):**
    - set Server `TutorialDone = true`, `TutorialExtra = 0`, `IntroSeen = true` (or no intro), `Rebirths = 1` and `StarterDebug reset`;
    - wait out 10 s after DataLoaded.
    A fresh save fails `quiet()`, so the check as written can never pass.
21. **7.4 check 8:** allow 10 s, not 9. `endsAt` is `os.time()` (whole seconds) against the client's `GetServerTimeNow()`, plus the 0.2 s delay.
22. **Snapshots and the hub agent:**
    - write the HUD edges (`Menu` right edge, `SpeedUI.Holder` rect) into the header of `hatch_chrome_before_v2.txt` and of every AFTER file;
    - if they differ, re-capture BEFORE before diffing;
    - capture BEFORE and AFTER the same day, at the same 1519x753 viewport.
23. **Task 3 intermediate state:** the night shell around the old ScrollingFrame must never be saved or published. Run Tasks 3-5 in one sitting, or revert the PAGE_SKIN line if the session must stop.
24. **Perf:** add a phone-emulator MicroProfiler glance with the Shop open (about 1000 GuiObjects and about 300 UIStrokes), and note the frame time in the ledger.
25. **The 20 behaviours:** add B21-B26 (MUST 2, SHOULD 3, 7, 8, plus boost titles equal `CARDS[key].title()` live, and the Double's numbers equal `Boosts.speed(player)` / `(player, 1)` as the HUD shows).
26. **Toasts:** use the standard (1.18-capped) fit scale, not the Shop's bigger `pageCap` scale.

---

## What's good

- **The numbers are real.** The fit rows, the y table, the canvas heights and the 4.12 hover/pulse margins all re-derive exactly.
- **Logical-px manual layout** in the Shop plus the scroll probe (K) avoids the UIListLayout-under-UIScale trap. It makes `scrollTo` exact at every scale.
- **D7** (no full-card hit on money cards), **D11** (no UIScale on the popup Holder) and **D14** (dry run with exact args) are the right calls for a revenue page.
- **The odds rule is handled thoroughly:**
  - the popup is still the only buy path;
  - the card Buy only opens it;
  - 7.4 check 6 includes on-top sampling and the 6/7-cell variants;
  - restricted means no egg;
  - the fallback means no offer.
- **D13 performance:**
  - the analytics poll becomes events;
  - the RenderStepped loop runs only while enabled;
  - the expiry timer plus a ticker that runs only while shown replace both forever-loops;
  - an idle probe proves it.
- **D16 / D17 protect the other windows properly:** the filter v2 with a re-captured BEFORE in Task 0, a new Gift snapshot, and additive-only helper changes with a diff rule.
- **D10:** the slot contract keeps the Starter logic in one script.
- **The design** is consistent with the built Gift window (same chrome and header, gold for purchase, silver for owned, red for refusal).
  - The popup is clearly better than the old one: the hero is bigger, the odds portraits go from 40 to 54, and the BUY is 492 wide @32.
  - Timers have no background, as the owner asked.
- **D4's rail** keeps the side-tab muscle memory, and the phone tab hits are 85 x 54 pt.

---

## Owner's calls: recommended defaults (owner said "do as recommended")

| # | Call | Recommended default | Why |
|---|---|---|---|
| 1 | Band colour | **Magenta all year** (Shop and popup) | It matches the Starter HUD art and the old Shop header, and tells the Shop apart from the Pumpkin Gift window at a glance. Halloween already shows on the Gift band. |
| 2 | Tabs | **Left rail inside the window** | It keeps the side-tab habit, leaves the most scroll height (386 vs 340), and gives big phone hits. |
| 3 | Speed boost art | **Frameless stickers** (shoe / potion + clock) | It matches HATCH NIGHT and the owner's frameless references. Keep the old product-art ids in one table (`BOOST_ART`) so a swap is a single line if the owner asks. |
| 4 | Popup size | **The full 740 x 470 window** | Same chrome as Gift. It gives the big BUY (37.8 px at 1080p) and readable odds. |
| 5 | BUY breathing 1.00..1.02 | **On** | It is the only motion on a CTA, and gentle; the margins are verified at 1.02. |
| 6 | `ShopClientLegacy` | **Keep it for 7 days live, then delete it** | Delete it sooner if any Shop logic changes first, so it can never drift. Note it in `roblox-shop.md`. |
| (new) | Shop size on big screens | **As big as today** (MUST 1); not optional | The owner already decided this on 2026-10-05: "it looks too small". |
