# Performance + robustness review: HATCH NIGHT Starter Pack popup + Shop (2026-10-21)

**Owner's ask:** "check if the NEW UI is laggy etc, so we can prevent future issues". Many players are on low-end phones.

**Scope:**
- ShopClient (rebuilt, 1007 lines)
- StarterPackClient (rebuilt popup + the Shop card, 657 lines)
- BrickUI.Hatch (the new helpers, lines 827-940, and the changed glossButton / shellCard / windowChrome code)
- MenuController (the 3 changed lines, plus the lines that read the viewport)
- StarterPackHud (its contract with the popup)
- ShopClientLegacy (the fallback)

**How I reviewed it:**
- Read-only, with Studio in Edit. I used `script_read` and `script_grep` only and changed nothing.
- I read the plan, its review (MUST 6 = the picker-row leak), the ledger, `hatch_shop_perf_results.txt` and the `hatch_shop_perf.lua` probe, plus the earlier `2026-10-21-new-ui-performance-review.md` for its method and its bar.
- **The builder's numbers** (the Lua work inside our own loops):
  - Shop refresh: 0.10 ms avg / 0.16 ms max per 0.3 s tick.
  - Popup RenderStepped: 0.012 ms avg per frame.
  - 30 open/close cycles: flat.
- **What those numbers do not cover:**
  - **Engine-side layout and render cost.** The frame times in the results file are the 15 fps unfocused-Studio throttle (66.7 ms in every state), so they show nothing.
  - **A real phone.** The plan's SHOULD 24 (phone emulator + MicroProfiler) was skipped. See I-3.
- **Phone estimates** below use the earlier review's factor: Luau and property writes run 5-10x slower on a low-end Android than on this PC.

## Verdict: OK TO SHIP

- **No CRITICAL finding.**
- **Closed state:** the Shop and the popup do zero per-frame work and run no polling loop. I checked every loop in the code.
- **Leaks:** none. MUST 6 (picker rows leaving `H.buttons`) is built correctly and measured flat.
- **Open state:** cheap in Lua.
- **The 4 IMPORTANT findings are all small, safe changes** (about 5-25 lines each):
  - I-1 and I-2 are the code fixes for these two scripts. Do them in the next ShopClient / StarterPackClient pass, or now if this build is not published yet.
  - I-3 is a 2-minute check by the owner on a real phone.
  - I-4 is cheap insurance in BrickUI.Hatch that matters more with every window converted to HATCH NIGHT.
- **Item 7** (thin Check-UI outlines, a left menu that changes width) is a pre-existing start-up race, not caused by this build. It has its own section at the end.

## What runs, and when (checks 1 and 2)

### Closed (Shop and popup both closed)

| Where | What | Runs while closed? |
|---|---|---|
| ShopClient 876-883 `loop(my)` | the 0.3 s refresh | **No.** `while token == my`; `sync()` (884-911) bumps the token on close, and the loop ends at its next wake (at most 0.3 s). Started only when `onScreen()` turns true. |
| ShopClient 909-911 | 4 `Visible` signals + `MainMenu.Enabled` -> `sync()` | events only; `sync()` returns at once when nothing changed |
| ShopClient 579-580 | slot `Visible` -> `applyLayout`; `CanvasPosition` -> `updateActive` | events only |
| ShopClient | RenderStepped / Heartbeat | **none in the file** |
| StarterPackClient 323-356 `syncMotion` | the ONE RenderStepped (rays + BUY breathing + the card pulse) | **No.** Connected only while `gui.Enabled or cardShown()`, and disconnected on the next `Enabled` / `Visible` change |
| StarterPackClient 358-371 `startTicker` | the 0.5 s timer ticker | **No.** `while (gui.Enabled and not thanked) or cardShown()` |
| StarterPackClient 474-485 | the offer's end | one token-checked `task.delay` (no poll) |
| StarterPackClient 591-618 | the auto-popup quiet check, 0.5 s | until the popup was seen or the pack is owned, then it **parks** on an attribute signal (the earlier review's M-6, done) |
| BrickUI.Hatch 727 / 775-799 | bat ViewportFrames | the popup has none (`bats = false`). In MainMenu's chrome the Shop band is magenta, so `bats.Visible = false` and the bat loop stays disconnected |
| StarterPackHud 662-678 | its own 0.1 s poll | pre-existing and untouched. It parks when the offer is gone (the earlier review's M-2, done) and hides while any window or the popup is up (370-373), so its RenderStepped idles while the Shop is open |

The builder's idle probe agrees: counters frozen over 3 s, before and after 30 cycles; `ShopLoop`, `RaysLoop` and `StarterTicker` are all false.

### Open

| State | Every frame | Periodic | Tweens |
|---|---|---|---|
| Shop open, offer running | **1 write:** the Starter card BUY `ButtonScale` (StarterPackClient 333-335), plus ~7 property reads in `cardShown()` | refresh every 0.3 s (all sections; most writes early-out on the `shownKey` / `HatchText` caches); card timer every 0.5 s (its text changes once a second) | Pill 0.15 s only when the active section changes; scroll 0.35 s per tab press; hover tweens on input |
| Shop open, no offer (most players after 24 h) | **nothing** | refresh 0.3 s | as above |
| Popup open | **2 writes:** `Rays.Rotation`, BUY `ButtonScale` | EndsIn + cash line every 0.5 s (the text changes once a second); `endsGrad.Color` re-assigned every 0.5 s | open pop 0.2 s, close 0.12 s |

- **Gradients and strokes:** none animate. No gradient Offset or Rotation moves, and no stroke Thickness changes. Only the timer gradient swaps colour once, at the 1-hour mark.
- **Countdowns:** they tick from a 0.5 s ticker and never per frame. The text changes once a second; `H.fit` re-measures only on a change.
- **Phone estimate:**
  - refresh: ~0.5-1 ms per 0.3 s tick (one short spike every ~10 frames);
  - popup motion: ~0.1 ms per frame.
  - Both fine at 30 fps. Engine-side cost: see I-1, I-3 and I-4.

## Leaks (check 3)

| Item | Result |
|---|---|
| Gift picker rows | **OK (MUST 6).** `H.priceButton(..., transient = true)` (ShopClient 715) -> `holder.Destroying:Once` removes the button from `H.buttons` (Hatch 346-351). `pickerConns` are disconnected on every rebuild and close (670-683). The row closures (`go`, `glossV`, the sticker signals) all hang off destroyed instances or cleared tables (`rowPress`, `busy`). The builder measured it flat: `HatchButtons` 50 -> 50 after 10 rebuilds, `PickerConns` 0 |
| Players.PlayerAdded / PlayerRemoving | 2 permanent connections (756-757), made once and guarded by `picker.Visible`. Fine |
| MarketplaceService callbacks | none in either script (purchases go through `Shop.Buy` / `StarterPack.Buy` remotes) |
| ViewportFrames / CanvasGroups | none in the Shop, the popup or the card |
| Respawn | ShopClient and StarterPackClient run once (StarterPlayerScripts). `StarterPackUI` (line 94) and `GiftToast` (line 481) are `ResetOnSpawn = false`, and MainMenu is too (plan B20, tested by the builder). No duplicates |
| Open / close connections | none are made per open: every connection is made once at start. Per-open work is tokens, `task.delay` and tweens only |
| Odds cells (popup) | rebuilt only when the egg/kg key changes (`oddsKey`, 199-201); old cells destroyed |
| Gap in the probe | `hatch_shop_perf.lua` checks instance counts and LuaHeap, but not the **Signals** memory tag the earlier review used. See M-6 |

## Price lookups (check 4)

**ShopClient `robux()`, lines 136-146:**
- one cache per id;
- the first call returns the ShopConfig fallback and starts one `task.spawn` with `pcall(GetProductInfo, id, infoType)`;
- the label updates on the next 0.3 s tick.
- It never blocks the UI thread, and the InfoType is correct everywhere (MUST 3).

**Calls per session:**
- About 16 on the **first Shop open**:
  - 4 passes (GamePass);
  - 1 Double step (a new one after each purchase);
  - 3 boosts;
  - 6 packs;
  - 1 treadmill (a new one per tier);
  - 1 Grow All.
- 4 gift ids, only when the gift picker is first opened.
- StarterPackClient: 1 at start (83-89).

**Gaps:**
- **No retry.** A throttled or failed call shows the fallback for the whole session (M-1).
- **Prices are no longer prefetched at join.** The old forever loop fetched them; now they are fetched on the first open, so the first open shows the fallback for ~0.3-1 s (M-1).
- **`robux(nil, ...)` errors** (see I-2).

**Repo-wide (pre-existing):** 9 client scripts keep their own GetProductInfo cache, so the same ids are fetched several times per session (M-4).

## Instances (check 5)

**Builder's probe:** ShopPage **599 GuiObjects / 1096 instances**; StarterPackUI 175 / 254 (with the odds strip); GiftToast 2 / 6.

**My breakdown from the helper code** (it sums to ~565 GuiObjects and ~470 others, consistent with the probe):

| Kind | ShopPage | Notes |
|---|---|---|
| UIStroke | **~188** | ~105 are Contextual **text** strokes (every `H.text`); ~83 are Border strokes (2 per glossButton, 2 per shellCard, chips, tags) |
| UIGradient | ~67 | 2 per glossButton, 1 per shellCard / recess / tag |
| UICorner | ~165 | 4 per glossButton, 4 per shellCard |
| UIScale | ~40 | 1 per glossButton (`ButtonScale`), 1 per shellCard (`PopScale`), CanvasScale |
| ViewportFrame / CanvasGroup | 0 | |

- **The plan's ~300 UIStroke estimate was high:** it is ~188.
- **Visible at once:** the ScrollingFrame clips, so only the rail and ~2.5 rows of cards draw (about 35-40 % of the list).
- **The popup:** ~40 UIStrokes. The Shop card: ~12.

**Lazy build?** No. The Shop is built eagerly, once, at script start:
- off-screen, then parented last (line 499);
- hidden (`Visible = false` + window hidden), so it costs memory and one build at join, not frames.
- The old Check-UI ShopClient was also built at start, so this is not a regression.
- **Do not make it lazy:**
  - StarterPackClient waits up to 60 s for `ShopPage` (line 501);
  - PetsEggsUI's GET MORE looks it up (PetsEggsUI 378);
  - MenuController picks the page by `Body.ShopPage` on open.
- **The build time was never measured** (M-2).

## Images (check 6)

**Shop, ~17 unique ids:**
- treadmill, egg, shoe/speed, star, the potion tile;
- 4 pass icons;
- glow, gift, clock, white Robux hex;
- 3 potion icons.
- (`BOOST_ART` is loaded only if `USE_BOOST_PRODUCT_ART` is set to true.)

**Popup + card, ~10 more:**
- rays, cash;
- the starter egg icon;
- 5-7 pet portraits.
- The rest are shared with the Shop.

**Gift picker:** one headshot per other player, cached (`thumbs`, 651-668).

**Load and memory:**
- `hatch_assets.lua` loaded all 62 HATCH NIGHT assets (failed 0).
- Every image is 512 px or smaller. Glow and rays are one texture each, shared with the Gift window, so texture memory is small.
- **Preload:** none. No game script calls `ContentProvider:PreloadAsync`, so on a slow phone the first Shop open can show icons popping in (M-3).

---

## Findings

### CRITICAL

None.

### IMPORTANT

**I-1. The Starter card's BUY keeps breathing every frame even after the card has scrolled out of view.**
- **Where:**
  - StarterPackClient 311 `cardShown()`;
  - 324 `local want = gui.Enabled or cardShown()`;
  - 333-335 `if cardShown() then cardBuy.pulse(...)`.
- **Evidence:**
  - While the Shop is open and the offer runs, `cardShown()` is true for the whole visit, even when the player is on POTIONS / TREADMILL and the card is clipped away.
  - So the RenderStepped stays connected and writes the card's `ButtonScale` every frame.
  - That re-lays out a ~50-object subtree (12 UIStrokes, 6 stroked texts) inside MainMenu, the biggest ScreenGui (~600 Shop GuiObjects).
  - It is the **only** continuous per-frame work in the open Shop. Lua cost is tiny (0.012 ms); the engine side was never measured (I-3).
- **Fix:** about 6 lines, StarterPackClient.

```lua
-- below cardShown() (line 311): the card's BUY breathes only while the card is inside the scroll's visible box
local cardScroll -- ShopPage.Scroll (set in the card task)
local function cardInView()
	if not (cardShown() and cardScroll) then return false end
	return slot.AbsolutePosition.Y + slot.AbsoluteSize.Y > cardScroll.AbsolutePosition.Y + 4
end
-- line 324:   local want = gui.Enabled or cardInView()
-- line 334:   if cardInView() then cardBuy.pulse(t - t0, testPulseShop) else cardBuy.stopPulse() end
-- card task, after `slot = s` (line 506):   cardScroll = sc
-- card task, after line 564:   sc:GetPropertyChangedSignal("CanvasPosition"):Connect(syncMotion)
```

- The ticker keeps using `cardShown()`, so the timer is current when you scroll back. That costs one text per second, negligible.
- **Result:** scrolled past the card, or no offer, means zero per-frame work while the Shop is open.
- **Test:** `hatch_shop_perf.lua` "cost" adds `Tab_POTIONS`, waits 0.5 s, and asserts `RaysLoop == false` and that the `HatchPerfPopup` frame counter is flat for 1 s. Back at `Tab_FEATURED`, `RaysLoop == true`.

**I-2. One bad config row freezes every Shop section below it; `robux(nil)` throws.**
- **Where:**
  - ShopClient 801-854 `refresh()`, 857-860 `refreshSafe()`;
  - 136-139 `robux()`.
- **Evidence:**
  - Review SHOULD 3 asked for a pcall "so one section cannot freeze the others". The build wraps the **whole** `refresh()` in one pcall.
  - An error in PASSES (802-809) therefore skips the Double, boosts, packs, treadmill and Eggs updates on every tick. It warns once (`refreshWarned`).
  - The price buttons are built with an empty price (Hatch 855), so those buttons would show a bare Robux hex with no number for the whole session.
  - The likely trigger is a future ShopConfig edit (the Shop is now data-driven, SHOULD 9). For example, a pass or pack row without an `id`, or `doubleSpeedStep` returning nil: `robux(nil, ...)` passes the `id == 0` check, then `live[nil] = ...` throws "table index is nil".
  - The gift picker has the same exposure through `p.giftId` (line 720).
- **Fix:**

```lua
-- robux(), line 137
if not id or id == 0 then return STUDIO and tostring(fallbackPrice) or "SOON" end

-- refresh(): split the body (802-853) into 6 local functions, unchanged inside -
-- refreshPasses, refreshDouble, refreshBoosts, refreshPacks, refreshTreadmill, refreshEggs - then:
local PARTS = {refreshPasses, refreshDouble, refreshBoosts, refreshPacks, refreshTreadmill, refreshEggs}
local partWarned = {}
local function refresh()
	for i, f in PARTS do
		local ok, err = pcall(f)
		if not ok and not partWarned[i] then partWarned[i] = true warn(("[ShopClient] refresh part %d: %s"):format(i, tostring(err))) end
	end
end
```

- `refreshSafe()` keeps its outer pcall and the perf probe.
- **Test:** add a Studio-only switch, ShopPage attribute `TestBreakSection = 1`, that makes `refreshPasses` raise an error. (`execute_luau` runs in its own Lua VM, so editing ShopConfig from there would not reach ShopClient's copy.) Then assert:
  - the Double, boost, pack, treadmill and Eggs prices are still set;
  - exactly one warning.

**I-3. The phone render and layout cost of the open Shop has never been measured.**
- **Where:**
  - SHOULD 24 was skipped (ledger, "SHOULD skipped");
  - `hatch_shop_perf_results.txt` line 2 (throttled at 15 fps).
- **Evidence:**
  - The probes time our Lua only. The engine work on a phone is unknown:
    - opening the Shop tweens `Window.Size` for 0.32 s (MenuController 253-256), so Body.AbsoluteSize changes every frame;
    - `CanvasScale` then re-scales all ~600 GuiObjects and ~105 stroked texts every frame of the tween (Hatch 635-641);
    - fixed-size text under a changing UIScale is re-shaped at each new pixel size;
    - scrolling re-lays out the visible cards.
  - The Gift window passed the same pattern earlier with no device test either.
- **Fix (owner, about 2 minutes, after publish or in a private server):**
  1. On the oldest phone, join and open the Shop 5 times.
  2. Scroll from top to bottom, open the popup, and close everything.
  3. Turn on the MicroProfiler (in-game Settings > MicroProfiler).
  4. Watch the frame bar during the open and while scrolling.
- **Pass:**
  - Shop-open steady frames are within ~1 ms of Shop-closed frames;
  - no frame over ~50 ms during the open.
- **If the open hitches,** snap the Shop open on touch devices (MenuController 253-256; `UserInputService` is already at line 9):

```lua
-- MenuController, Hatch branch, replacing lines 253 and 256:
local snap = UserInputService.TouchEnabled and name == "Shop" -- (perf) phones: no per-frame re-scale of the 600-object page
win.Size = snap and size or mul(size, 0.6)
-- (lines 254-255 unchanged)
if not snap then tween(win, 0.32, {Size = size}) end
```

**I-4. Hidden HATCH NIGHT pages re-scale on every window tween; this grows with each converted page.**
- **Where:** BrickUI.Hatch 635-643 `H.bindCanvasScale`, used by ShopClient 188 (ShopPage, 599 GuiObjects) and PlaytimeClient 106 (GiftPage, 816 GuiObjects). Both pages live in the same `Body`.
- **Evidence:**
  - `bind()` runs on every `Body.AbsoluteSize` change, whether or not the page is shown.
  - Every window open and close tween (0.32 s / 0.15 s) on **any** page, plus every viewport resize, writes the `CanvasScale` of both hidden pages every frame. That includes Rebirth, Index and Settings.
  - The engine then invalidates the layout of ~1400 hidden GuiObjects per tween frame. AbsoluteSize stays live for hidden objects, so this work is not free.
  - Phase 2 adds Rebirth / Index / Settings canvases to the same Body, so this multiplies.
- **Fix:** 3 lines, additive. Byte-identical at rest, because a page re-applies its scale when it shows.

```lua
function H.bindCanvasScale(canvas, ref, logicalW)
	local sc = Instance.new("UIScale")
	sc.Name = "CanvasScale"
	sc.Parent = canvas
	local function bind()
		if not canvas.Visible then return end -- (perf) a hidden page keeps its last scale; re-applied when it shows
		local x = ref.AbsoluteSize.X if x > 0 then sc.Scale = x / logicalW end
	end
	ref:GetPropertyChangedSignal("AbsoluteSize"):Connect(bind)
	canvas:GetPropertyChangedSignal("Visible"):Connect(bind)
	bind()
	return sc
end
```

- **Why it is safe:**
  - MenuController sets the page's `Visible` before it sizes the window (lines 235-236, then 251-256), so the shown page tracks every frame of its own tween.
  - The popup canvas is always `Visible`, so it is unchanged.
  - The same guard can go on `windowChrome`'s `SkinScale` (Hatch 668-670, `f.Visible`). That one is optional: those layers are small.
- **Test:** the Gift snapshot must stay byte-identical, and so must containment S1/G1. Add a probe: open Rebirth and assert `ShopPage.CanvasScale.Scale` does not change during the tween.

### MINOR

**M-1. Prices: no prefetch, no retry** (ShopClient 136-146).
- The first Shop open shows the ShopConfig fallback for ~0.3-1 s.
- Regional-price players see the base price flip to theirs.
- A failed or throttled call keeps the fallback all session. The purchase prompt still shows the right price.
- **Fix:**

```lua
-- robux(): the spawn body becomes two attempts
task.spawn(function()
	for _ = 1, 2 do
		local ok, info = pcall(MarketplaceService.GetProductInfo, MarketplaceService, id, infoType)
		if ok and info and info.PriceInRobux then live[id] = tostring(info.PriceInRobux) return end
		task.wait(10)
	end
end)
-- after line 911: warm the cache in the background (the old forever loop did this at join)
task.delay(8, function()
	for _, p in ShopConfig.Passes do robux(p.id, p.price, GAMEPASS) end
	for _, key in BOOST_KEYS do local d = SpeedBoostCards.CARDS[key] robux(d.id, d.price, PRODUCT) end
	for _, c in packCards do robux(c.pack.id, c.pack.price, PRODUCT) end
	robux(ShopConfig.GrowAllProduct, ShopConfig.GrowAllPrice, PRODUCT)
end)
```

**M-2. The Shop build time at join is unmeasured** (ShopClient 503).
- About 1100 `Instance.new` plus ~100 `H.fit` text measurements run in one synchronous chunk while the game loads.
- Estimate: ~15-40 ms on PC, so ~100-250 ms on a low-end phone. It happens once, but it lands in the first-60-seconds window.
- **Fix:** measure first.
  - `local t0 = os.clock()` before line 503.
  - After it: `if STUDIO and page then page:SetAttribute("HatchBuildMs", (os.clock() - t0) * 1000) end`.
  - Target: 20 ms or less on PC.
- **If it is above that,** add a `task.wait()` between the section blocks inside `build()`:
  - the sections are independent, and `page` is parented last;
  - StarterPackClient's 60 s wait already tolerates it.
- Keep the build eager (see check 5).

**M-3. No image preload** (no `PreloadAsync` in any game script).
- Optional fix: preload the ~17 Shop ids plus the starter egg and portraits once, in the background, after `DataLoaded` + 10 s:
  `task.spawn(function() pcall(ContentProvider.PreloadAsync, ContentProvider, {page}) end)`
- Passing the built `page` preloads every image under it.
- Low priority: texture memory is small, and this only removes pop-in on a slow phone's first open.

**M-4. Nine separate GetProductInfo caches** (pre-existing):
- TreadmillSignClient 30, ShopClient 141, PlaytimeClient 65, RebirthClient 201, SpeedOfferClient 107, UpgradeClient 194, OfflineClient 163, StarterPackClient 84, SpeedBoostCards 32.
- The same ids (boosts, packs, treadmill) are fetched by 2-3 scripts per session.
- **Future fix:** one `ReplicatedStorage.PriceCache` module, `get(id, infoType, fallback)`, with the retry from M-1. Swap callers one at a time.

**M-5. The popup's `Open` event is created after unbounded waits** (StarterPackClient 570-571, then 636-639).
- `pg:WaitForChild("PetsEggsUI")` and `:WaitForChild("RightTiles")` have no timeout.
- If PetsEggsUI ever fails before making `RightTiles`, `Open` is never created, and StarterPackHud shows no offer ("no odds path = no offer").
- This ordering is pre-existing.
- **Fix:** move lines 635-639 (the `Open` block) above line 569, or move lines 570-571 inside the auto-popup `task.spawn` (591).

**M-6. The leak probe does not track signals** (`hatch_shop_perf.lua` `snapshot()`).
- **Fix:** add `Stats:GetMemoryUsageMbForTag(Enum.DeveloperMemoryTag.Signals)` to the snapshot. Keep the +3 MB LuaHeap rule, and expect Signals flat within ±0.2 MB, as in the earlier review.

**M-7. Optional: a lighter refresh** (ShopClient 876-883).
- Each 0.3 s tick runs ~16 `setPrice` / `setWord` calls. Each builds a key string, and OWNED / MAX also build a variants table; most then early-out.
- It also runs 3 `title()` speed-amount formats and 2 `Boosts.speed` calls.
- That is 0.10 ms on PC. It only needs attention if the Shop grows.
- If so: tick at 0.5 s and also refresh on the attribute signals that matter (`Pass_*`, `SpeedBoosts`, `TreadmillTier`, `Money`).

---

## Item 7: thin Check-UI outlines and a left menu that changes width (separate, pre-existing bug)

### Root cause

These read `workspace.CurrentCamera.ViewportSize` once, when the script starts:
- `BrickUI.deviceScale()` (BrickUI 65-70);
- MenuController 135 (`smallScreen`);
- PetsEggsUI 181.

On the client, the camera exists before its viewport is sized. Its `ViewportSize` is **(1, 1)** for the first frame(s): this is the same Studio gotcha noted in memory, where the viewport is (1, 1) while the window isn't drawing.

**What (1, 1) does:**
- **The strokes.** It passes the guard at BrickUI 68 (`vp.X <= 0`), so `deviceScale()` returns `clamp(min(1/1050, 1/620), 0.52, 1.18)` = **0.52**. Every Check-UI pixel size is created once from that value and never recomputed:
  - `pxStroke` (106): window / tile / close / innerHighlight strokes;
  - `restyle` (475): menu tiles and the window Depth / Face;
  - MenuController 47: the Body stroke;
  - header TopHighlight / divider heights (393 / 395);
  - damier TileSize (145).
- **The menu width.** `smallScreen` (MenuController 135) reads `1 < 520` as true, so the left menu gets **UIScale 1.3 on a PC** (136-140). PetsEggsUI 181 does the same to the right tile column.
- **No later fix-up.** The only ViewportSize handler (MenuController 298-304) re-fits HATCH NIGHT windows only.

**The builder's numbers match this exactly:**

| Piece | 0.52 session | 1.18 session | Base x 0.52 / x 1.18 |
|---|---|---|---|
| Window stroke | 1.82 | 4.13 | 3.5 x 0.52 / x 1.18 |
| Body stroke | 0.78 | 1.77 | 1.5 x 0.52 / x 1.18 |
| innerHighlight | 0.62 | 1.42 | 1.2 x 0.52 / x 1.18 |
| Close stroke | 1.46 | 3.3 | 2.8 x 0.52 / x 1.18 |
| Header dividers | 2 px | 4 px | |
| Header highlight | 1 px | 2 px | |

- **The menu edge:** the right edge was 221.76 vs 173.88.
- Solving `L + W = 173.88` and `L + 1.3 W = 221.76` gives W = 159.6 and L = 14.28.
- L equals the `SpeedUI.Holder` left edge (14.28) in the ledger header. So the 1.3 scale on the same menu explains the whole difference.

**Why it varies between sessions:**
- It depends on whether these LocalScripts reach those lines before or after the first real frame.
- MainMenu is `ResetOnSpawn = false`, so a bad start sticks for the whole session.

**Scope:**
- **The new HATCH NIGHT UI is immune.** It sizes from `AbsoluteSize` and at open time.
- **One knock-on:** `hatchFit` uses `rightEdge(menu)` as its left clearance. In a bad session the Shop has 48 px less room on narrow screens. At 1519x753 there is no effect, because the height limit wins.

### Minimal, safe fix

**Part 1 stops the race** (BrickUI only, about 12 lines; no change for other callers):

```lua
-- BrickUI, above deviceScale(): the client camera reports ViewportSize (1, 1) until its first real frame
local function viewportReady(vp) return vp.X >= 100 and vp.Y >= 100 end
function BrickUI.waitViewport(timeout) -- client only; returns true once the camera has its real size
	if not game:GetService("RunService"):IsClient() then return true end
	local t0 = os.clock()
	repeat
		local cam = workspace.CurrentCamera
		if cam and viewportReady(cam.ViewportSize) then return true end
		task.wait()
	until os.clock() - t0 > (timeout or 5)
	return false
end
-- deviceScale(), line 68:  if not viewportReady(vp) then return 1 end   -- (not 0.52: 1 = the 1050 x 620 baseline)
-- just before `return BrickUI` (line 519):
BrickUI.waitViewport(5)
```

**Why part 1 alone fixes the reported bug:**
- Every client script that builds Check-UI requires BrickUI before reading the viewport: MenuController line 20 (read at 135), PetsEggsUI 69 (read at 181), RebirthClient 24, IndexClient 22, and the rest.
- So their first `deviceScale()` and `smallScreen` read now see the real viewport. Cost: the menu appears one or two frames later.
- The module already yields at require time (`WaitForChild("Hatch", 5)`, line 515), so a yield there is not new.
- The `IsClient` guard keeps a server `require` from waiting.

**Part 2 follows later size changes** (recommended; handles phone rotation and window resizes):

```lua
-- BrickUI: device-scaled sizes re-applied on every ViewportSize change (weak keys: destroyed UI drops out)
local scaledStrokes = setmetatable({}, {__mode = "k"}) -- UIStroke -> base px
local scaledTiles = setmetatable({}, {__mode = "k"})   -- damier ImageLabel -> base tile px
local scaledHeaders = setmetatable({}, {__mode = "k"}) -- header Frame -> true
function BrickUI.trackStroke(s, px) scaledStrokes[s] = px s.Thickness = px * BrickUI.deviceScale() return s end
-- pxStroke (106): `s.Thickness = ...` -> BrickUI.trackStroke(s, px)
-- restyle strokes() (475): `s.Thickness = ...` -> BrickUI.trackStroke(s, window and 3.5 or 2.6)
-- damier (145): after setting TileSize -> scaledTiles[d] = tilePx or 19
-- header (after 399): scaledHeaders[h] = true
local function sizeHeader(h, k)
	local px = math.max(2, math.floor(3 * k + 0.5))
	h.TopHighlight.Size = UDim2.new(1, 0, 0, math.max(1, math.floor(2 * k)))
	h.DividerDark.Size = UDim2.new(1, 0, 0, px)
	h.DividerBlack.Size = UDim2.new(1, 0, 0, px)
	h.DividerBlack.Position = UDim2.new(0.5, 0, 1, px)
end
local function rescale()
	local k = BrickUI.deviceScale()
	for s, px in scaledStrokes do s.Thickness = px * k end
	for d, t in scaledTiles do d.TileSize = UDim2.fromOffset(t * k, t * k) end
	for h in scaledHeaders do sizeHeader(h, k) end
end
if game:GetService("RunService"):IsClient() then
	local camConn
	local function hook()
		if camConn then camConn:Disconnect() end
		local cam = workspace.CurrentCamera
		if cam then camConn = cam:GetPropertyChangedSignal("ViewportSize"):Connect(rescale) end
		rescale()
	end
	workspace:GetPropertyChangedSignal("CurrentCamera"):Connect(hook)
	hook()
end
```

```lua
-- MenuController 47:  bs.Thickness = 1.5 * B.deviceScale()  ->  B.trackStroke(bs, 1.5)
-- MenuController 135-140 (and PetsEggsUI 181-185 the same way, on its `holder`): the phone size follows the screen
local menuScale = menu:FindFirstChildOfClass("UIScale")
local baseMenuScale = menuScale and menuScale.Scale or 1
local function applySmall()
	local small = workspace.CurrentCamera.ViewportSize.Y < 520
	if small and not menuScale then menuScale = Instance.new("UIScale") menuScale.Parent = menu end
	if menuScale then menuScale.Scale = small and 1.3 or baseMenuScale end
end
applySmall()
workspace.CurrentCamera:GetPropertyChangedSignal("ViewportSize"):Connect(applySmall)
```

**Why part 2 is safe:**
- The tables hold numbers keyed by Instances, so nothing keeps destroyed UI alive.
- `rescale()` runs only on a resize (rotation, a Studio viewport change).

**Tests:**
- **Every Play session:** `Window.Face.UIStroke.Thickness == 3.5 * deviceScale()` (±0.01), and `Menu.UIScale.Scale == (ViewportSize.Y < 520 and 1.3 or 1)`. Run it twice, as a fresh Play and as a second Play.
- **The chrome snapshot:** Rebirth / Index / Settings BEFORE and AFTER must now give the same strokes every session. Re-capture `hatch_chrome_before_v2.txt` once the fix is in; the current BEFORE file was taken in a 0.52 session.
- **The race itself:** with `deviceScale()` hooked to return 0.52 at start, part 2 alone must fix the thickness on the first `ViewportSize` change.
