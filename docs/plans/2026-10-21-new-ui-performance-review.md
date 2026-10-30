# New UI performance review (2026-10-21)

Owner's ask: "check if the NEW UI is laggy etc, so we can prevent it from future happening issues".
Scope: StarterPackHud, StarterPackClient, the HATCH NIGHT Gift window (BrickUI.Hatch, StreakClient, PlaytimeClient,
MenuController skin hook, 2 bat ViewportFrames, Day 7 celebration CanvasGroup), RebirthClient (REBIRTH READY banner,
badge poll, step 11 arrows), the new map Lighting. Review only: no game code or Edit instance was changed.

## VERDICT: OK TO SHIP

There is no Critical finding. Nothing in the new UI causes lag today, nothing leaks, and every loop rests while its UI
is hidden, except the cheap polls listed below. The two Important findings are both in RebirthClient: JSON decoding
in a per-frame path and in a forever 0.5 s poll. They are not lag now, but their cost grows with the save size and lands on
phones. They are a ~15-line fix: do them in the next RebirthClient pass. Everything else is Minor or optional
future-proofing.

## How it was measured

- Studio Play solo, `TestFreshSave` true (set back to false after), `TestStarterPack` true, server: `Rebirths = 1` +
  `StarterDebug:Invoke("reset", player)`, so the offer was active (MagmaEgg, not restricted, 24 h countdown). Viewport
  1519 x 753 (HUD scale 1.18, full layout with the caption).
- Studio was in the background, so it was throttled to about 15 fps. The per-frame **Lua** costs below are real. Frame
  times and RenderCPU times are not representative, and they could not resolve the HUD's render cost: it is under the noise.
- StarterPackHud has no perf hook, so its loop body (lines 517-555) was copied exactly and run on the **live HUD
  instances** inside RenderStepped. The cost is the same as the script's own loop.
- **Phone estimates.** Luau and property writes on a low-end Android run roughly 5-10x slower than this PC. No real
  device was tested; that is the one gap left (see the end).

## Measured numbers

### StarterPackHud (the always-on HUD offer)

| What | Result |
|---|---|
| Motion loop, 300 RenderStepped frames (art shown) | avg **0.041 ms**, median 0.038, p95 0.056, max 0.140 ms per frame |
| Same body, tight loop x2000 (no render between) | 0.0155 ms/frame. The last-hour variant (pulsing timer) costs the same: 0.0153 ms |
| Work per frame | ~31 property writes, ~11 UDim2 allocations. No Instance.new, no string building, no tweens |
| Phone estimate | ~0.2-0.4 ms/frame while shown, about 1 % of a 30 fps frame |
| Art HIDDEN (window open) | the loop does nothing: the Float and suns stay frozen, and the pop counter stayed at 93 -> 93 over 2 s |
| 0.1 s poll while hidden | wanted() 0.0094 + layout() 0.0021 = **0.0115 ms per tick** (0.115 ms/s) |
| 0.1 s poll while shown | wanted() full path incl. overlapsAvoid/avoidRects **0.023 ms per tick**. WaveBanner has 0 descendants; HatchCard was absent |
| Render side (RenderCPU, 5 s each) | shown 4.12 ms / gui disabled 4.24 / hidden 4.39 / shown 4.27. The HUD's cost is inside the noise (< 0.3 ms) |
| 2 minutes shown (9 samples, 15 s apart) | total memory 2509.5 -> 2509.4 MB, LuaHeap 909.5 -> 902.7, Gui 106.60 -> 106.51, Signals 44.30 -> 44.17, GraphicsTexture 106.96 -> 107.02, PlayerGui 7711 -> 7711, GuiObjects 3192 -> 3192, HUD 37 -> 37 instances. 20 pops in 120 s (one every 6 s, as designed) |
| Hide / show x30 | re-shown 30/30. Total 2509.0 -> 2509.2 MB, LuaHeap 904.8 -> 904.9, Signals 44.24 -> 44.34, PlayerGui 7711 -> 7711, HUD 37 -> 37. The tween `.Completed` connection made per hide does not leak |
| 3 respawns | GuiObjects 3192 -> 3192, HUD 37 -> 37, shown again. Every new gui is ResetOnSpawn = false. PlayerGui gained +6 non-GUI instances, none of them in the new UI |
| Text re-layout probe | a forced re-layout after a UIScale change costs 0.0008 ms on the HUD price text; TextScaled "!" 0.0009 ms vs fixed size 0.0005 ms. Text churn is negligible |

### StarterPackClient (popup, Shop card, auto-popup)

| What | Result |
|---|---|
| 0.5 s loop, popup closed (Shop card timer + active()) | 0.002 ms per tick |
| 0.5 s loop, popup open (+ cash line + timer) | 0.004 ms per tick (0.008 ms/s) |
| Auto-popup poll (after the popup was seen) | 0.0003 ms per tick |
| Popup size | 148 instances. The open RenderStepped only turns one 196 px sunburst |

### Gift window (hatch_perf.lua re-run, same session)

| What | Builder (re-run) | This review |
|---|---|---|
| DAILY StreakClient | avg 0.0834 / max 0.4105 ms | avg **0.0709** / max 0.2218 ms |
| DAILY bats | avg 0.0077 / max 0.0338 ms | avg **0.0096** / max 0.0341 ms |
| PLAYTIME PlaytimeClient | avg 0.0447 / max 0.1212 ms | avg **0.0804** / max 2.1117 ms (one-off spike: 16 more 30-frame windows gave avg 0.07, max 0.26-0.48 ms) |
| PLAYTIME tabs/dots | avg 0.0046 / max 0.0343 ms | avg 0.0043 / max 0.0078 ms |
| Closed 3 s | counters frozen, BatLoop false | same: counters frozen, BatLoop false |
| Instances | 816 GuiObjects, 2 VPF, 1532 instances | same |
| 30 open/close + tab switches | flat | flat: GuiObjects 816 -> 816, VPF 2 -> 2, PlayerGui 7711 -> 7711. Memory total 2510.9 -> 2511.9, Lua 902.2 -> 904.7, Gui 106.5 -> 106.5 MB |

The builder's numbers hold. Phone estimate while the window is open: ~0.4-0.8 ms/frame. Closed: 0.

Day 7 celebration (`StreakCelebrate.TestCelebrate`): the CanvasGroup was visible for 12 of 105 frames (~0.8 s).
GraphicsTexture peaked +0.11 MB. The celebration closed itself (Enabled false at 7 s), and PlayerGui stayed at 7711 -> 7711.

### RebirthClient

| What | Result |
|---|---|
| canRebirth() on the fresh test save (BaseData 21 chars) | 0.0027 ms per call |
| canRebirth() with a veteran-sized save (BaseData 3610 chars = 20 pets + 20 eggs, PetInventory 2341 chars = 30 pets) | **0.060 ms per call**: two JSONDecodes plus their garbage |
| Arrow RenderStepped outside step 11 | 0.0006 ms per frame |

### Inventory (low-end phone view)

- **ViewportFrames:** 3 in PlayerGui. The 2 new bats (47 x 24 and 31 x 15 px, one skinned mesh each, no lights) render
  and animate only while the Gift window shows the Pumpkin band. The third is the pre-existing Backpack GearView.
- **CanvasGroups:** 1 new, the celebration TopHalf (182 x 106 logical, alive ~0.8 s, then Visible = false). The others
  are pre-existing: AdminBanner and the Roblox topbar (x2).
- **Images:** the HUD sunburst (130563114903838) is already used by 5 older screens (Tutorial finish, Free Gift,
  Offline, popup, Shop card), so it adds no texture memory. Its resolution could not be read: the asset is not owned,
  so EditableImage is refused. HUD egg 256 x 256, star 150 x 150, Hatch rays/glow 512 x 512. No big new textures.
- **Overdraw:** the HUD stacks 5 translucent or opaque layers (SunA 0.14, SunB 0.30, shadow 0.55, outline, egg) in a
  ~130 x 130 px area at scale 1.18. That is about 85K pixels, under 10 % of one 720p screen. Negligible. The full-screen
  backdrops (popup 0.45, celebration 0.2) only exist while those are open.
- **Batching:** with all windows closed, 148 GuiObjects are visible across 23 enabled ScreenGuis. The HUD is 25 of them,
  in its **own ScreenGui**. That is correct: its per-frame changes only re-batch its own 25 objects, not MainMenu.

### Lighting (new grade vs the captured original, ServerStorage._LightingPreview.Original)

| Effect | Original | Now | Cost change |
|---|---|---|---|
| DepthOfField | **Enabled** (FarIntensity 0.2, InFocus 110) | **Enabled = false** | cheaper: DOF was the heaviest pass |
| Bloom | Intensity 0.40, Size 30, Threshold 1.35 | 0.55, Size 24, Threshold 1.6 | cheaper: smaller blur, fewer pixels over the threshold |
| SunRays | 0.08, Spread 0.5 | 0.05, Spread 0.5 | same |
| ColorCorrection | Sat -0.06, Contrast 0.20 | Sat 0.30, Contrast 0.12 | same (one cheap per-pixel op) |
| Atmosphere | Density 0.34, Haze 1.6 | Density 0.2, Haze 0.1 | same |
| Sky | 6444884337 set, StarCount 0 | Sky7_Cumulus (18351376859 set), StarCount 3000 | same (6 faces either way; stars only draw at night) |
| Lighting | Brightness 2.7, ShadowSoftness 0.35 | Brightness 3, ShadowSoftness 0.25 | same |

Verdict: the new grade costs **less** than the old one. On low quality levels Roblox scales down or skips post-processing
by itself. The two ColorCorrections are not new: the second is WeatherClient's WeatherTint. Quality level was not toggled,
because it is a persistent Studio setting; this verdict comes from the settings above, not from a device test.

## Findings

### Critical (real lag now)

None.

### Important (lag at scale / over time / on phones)

**I-1. RebirthClient: JSON decode every frame during tutorial step 11.**
- **Where:** lines 648-670 (the arrow RenderStepped), line 656 (`... and canRebirth()`). canRebirth() is lines 463-469,
  ownedPets() lines 213-218.
- **Problem:** while TutorialExtra == 3 (a new player, from step 10 until the first rebirth, often 10+ minutes and mostly
  on phones), canRebirth() runs every frame. Each call JSON-decodes BaseData and PetInventory, so about 120 decodes per
  second plus fresh tables every frame. This happens even for R1, which has no pet requirement: `ownedPets()` is
  evaluated as an argument before `petMeets` sees `req == nil`.
- **Cost:** small today on a fresh save (0.003 ms). It is per-frame garbage on exactly the funnel players' devices, and it
  scales with the save: 0.06 ms per frame on this PC with a veteran-sized save, about 0.3-0.6 ms per frame on a low-end
  phone.
- **Fix:** see "Exact fix for I-1 + I-2" below. Use the cached `canNow` in the RenderStepped.
- **Expected gain:** the per-frame decode goes to 0. At most one cheap check per 0.5 s remains.

**I-2. RebirthClient: four JSON decodes every 0.5 s for every player, forever.**
- **Where:** lines 673-679 (poll) -> updateBadge (499-508) and updateReady (618-623, `not canRebirth()` at 621).
- **Problem:** canRebirth() runs twice per tick, so BaseData and PetInventory are decoded twice per tick, 4 decodes every
  0.5 s. This happens even when Money is far below the cost and even when the level has no pet requirement.
- **Cost:** veteran save 0.12 ms per tick on this PC, about 1 ms per tick on a low-end phone. That is a periodic micro-hitch
  every 0.5 s for the whole session, and it grows with the pet count.
- **Fix:** check money first, skip the pet scan when there is no requirement, re-decode only when the JSON strings
  change, and compute once per tick.
- **Expected gain:** in the common case ("can't afford it yet"), zero decodes. Otherwise at most one decode per actual
  BaseData/PetInventory change.

**Exact fix for I-1 + I-2 (RebirthClient)**

```lua
-- replace ownedPets() (lines 213-218): decode again only when either JSON string changed
-- (callers only read the list: bestFor and RebirthConfig.petMeets never modify it)
local petsCache, cacheBD, cachePI
local function ownedPets()
	local bd, pi = player:GetAttribute("BaseData"), player:GetAttribute("PetInventory")
	if petsCache and bd == cacheBD and pi == cachePI then return petsCache end
	local list = {}
	for _, pet in (decode("BaseData", {}).pets or {}) do table.insert(list, pet) end
	for _, pet in decode("PetInventory", {}) do table.insert(list, pet) end
	petsCache, cacheBD, cachePI = list, bd, pi
	return list
end

-- replace canRebirth() (lines 463-469): cheap checks first (same result: the terms are pure and AND-ed;
-- petMeets(pets, nil) is true)
local function canRebirth()
	if player:GetAttribute("DataLoaded") ~= true then return false end
	local r = player:GetAttribute("Rebirths") or 0
	if RebirthConfig.isMax(r) then return false end
	if (player:GetAttribute("Money") or 0) < RebirthConfig.cost(r) then return false end
	local req = RebirthConfig.requirement(r)
	return req == nil or RebirthConfig.petMeets(ownedPets(), req)
end

-- line 497 (above updateBadge): one answer per tick, shared
local canNow = false
-- updateBadge (499): first line
	canNow = canRebirth()
-- updateBadge (505): local on = canRebirth()   ->   local on = canNow
-- updateReady (621): ... or not canRebirth() then return end   ->   ... or not canNow then return end
-- arrow RenderStepped (656): ... ~= true and canRebirth()   ->   ... ~= true and canNow
```

Behaviour change: the step 11 tile arrow and the READY banner react within 0.5 s of becoming affordable instead of
within one frame. updateBadge also still runs at once on Rebirths, DataLoaded, BaseData and PetInventory changes.

### Minor (negligible now; cleanup and future-proofing)

**M-1. StarterPackHud, the always-on motion loop (lines 506-556). Optional low-end mode.**
- **Status:** this is the loop the owner was worried about, and it is fine. It stops completely while the art is hidden
  (line 507). Shown, it costs 0.041 ms per frame on this PC (about 0.2-0.4 ms on a low-end phone, ~1 % of a 30 fps
  frame), lives in its own ScreenGui, and leaks nothing over 2 minutes or 30 hide/show cycles.
- **Optional fix** if you want the 24 h offer even lighter on phones: run the motion at 30 Hz on touch devices.

```lua
-- above line 506
local MIN_DT = UserInputService.TouchEnabled and 1 / 30 or 0 -- (perf) phones: the motion at 30 Hz; desktop unchanged
local acc = 0
-- lines 506-507 become:
RunService.RenderStepped:Connect(function(dt)
	if not active then acc = 0 return end
	acc += dt
	if acc < MIN_DT then return end
	dt, acc = acc, 0
	-- (rest unchanged: hoverCur, the sunbursts and the stars already scale by dt)
```

- **Expected gain:** about -50 % of the HUD's Lua and re-batch work on phones. Trade-off: the drift steps at 30 fps on
  60 fps phones, so the owner should eyeball it. A cheaper, invisible cut: drop the price "breathing" (line 546,
  amplitude 0.04) and the SunA transparency wave (line 548). That removes 2 of the ~31 writes per frame.

**M-2. StarterPackHud, the 0.1 s poll never stops (lines 652-657).**
- **Problem:** it runs at 10 Hz for every player all session. That includes the cases where the offer is gone for good
  (owned or expired) and where it has not started: every 0-rebirth player has StarterEndsAt = 0.
- **Cost:** 0.0115 ms per tick, negligible. But any later addition to wanted() or avoidRects() is multiplied by
  10 Hz x every player x the whole session.
- **Fix:**

```lua
while true do
	task.wait(0.1)
	refreshTimer()
	if player:GetAttribute("StarterPack") == true or timeLeft() <= 0 then
		evaluate() -- wanted() is false: hides it
		player:GetAttributeChangedSignal("StarterEndsAt"):Wait() -- a new / restarted offer wakes the poll
	else
		layout()
		evaluate()
	end
end
```

- **Expected gain:** 10 wake-ups per second -> 0 for most players.

**M-3. StarterPackHud avoidRects() (lines 313-340).**
- **Status:** while the art is shown, it builds 2 closures and a few tables, and it walks every descendant of
  WaveBanner and HatchCard (line 322), 10 times a second. Today that costs 0.023 ms per tick: WaveBanner has 0
  descendants and HatchCard only exists during a hatch.
- **Fix:** no change needed now. Rule for later: never add a big gui to the avoid list as `addTexts(gui)`; add its 1-2
  known labels by name.

**M-4. StarterPackClient, the popup sunburst RenderStepped is connected forever (lines 468-470).**
- **Cost:** one bool check per frame.
- **Fix:** connect in `setOpen(true)` and disconnect in `setOpen(false)`. Delete lines 468-470 and use:

```lua
local sunConn
-- setOpen(true), after gui.Enabled = true:
if not sunConn then sunConn = RunService.RenderStepped:Connect(function(dt) heroSun.Rotation = (heroSun.Rotation + 20 * dt) % 360 end) end
-- setOpen(false), after gui.Enabled = false:
if sunConn then sunConn:Disconnect() sunConn = nil end
```

- **Expected gain:** about 0 (hygiene).

**M-5. StarterPackClient, the Shop card timer is updated while the Shop is closed (lines 479-483).**
- **Problem:** the TextScaled `T` label text and the tag colour are rewritten every 0.5 s for the whole 24 h, even when
  no window is open.
- **Fix:** line 479 `if card and card.row.Visible and menuWin.Visible and card.row.Parent.Visible then`.
- **Expected gain:** negligible.

**M-6. StarterPackClient, the auto-popup loop runs all session after it has done its job (lines 516-533).**
- **Fix:** first line inside `while true do`:
  `if owned() or player:GetAttribute("StarterPopup") == true then return end`. P.wantsPopup is false forever after that.
- **Expected gain:** 0.0003 ms per tick (hygiene).

**M-7. PlaytimeClient, the Gift tile badge is resized every frame (lines 274-277).**
- **Problem:** the badge pulse writes `badge.Size` every frame while it is visible. Since today it also lights while the
  daily streak reward waits (line 298), so it can pulse all session for a player who doesn't claim. It sits in MainMenu
  (1557 GuiObjects, 30 of them visible with the window closed).
- **Fix:** pulse a UIScale on the badge instead of its Size; it grows from the same AnchorPoint, so it looks identical.

```lua
local badgePulse = Instance.new("UIScale") badgePulse.Parent = badge -- near line 39
-- line 276: badge.Size = ...   ->   badgePulse.Scale = 1 + 0.12 * math.abs(math.sin(t * 4))
```

- **Expected gain:** tiny. No more per-frame Size invalidation inside MainMenu.

**M-8. RebirthClient, the badge "!" is TextScaled under a per-frame UIScale pulse (lines 491, 683-688).**
- **Cost:** about 1 microsecond per frame (measured).
- **Fix:** `mark.TextScaled = false` with a fixed TextSize. Same for the READY title, but that one only pulses for 4 s.
- **Expected gain:** tiny.

**M-9. RebirthClient, the arrow RenderStepped does lookups every frame for everyone (lines 648-655).**
- **Cost:** 4 FindFirstChild calls and 2 Visible writes per frame, all session (0.0006 ms).
- **Fix:** an early-out after the title pulse:

```lua
if player:GetAttribute("TutorialExtra") ~= 3 then
	if tileArrow.Visible then tileArrow.Visible = false end
	if pageArrow.Visible then pageArrow.Visible = false end
	return
end
```

**M-10. StreakClient, the daily auto-open poll keeps running after today's reward is claimed (lines 869-883).**
- **Problem:** if the reward was already claimed, the 0.5 s loop runs for the whole session.
- **Fix:** at the top of the loop:
  `if player:GetAttribute("StreakClaimable") ~= true then player:GetAttributeChangedSignal("StreakClaimable"):Wait() end`.
- **Expected gain:** negligible (hygiene).

**M-11. Gift window, one 2.1 ms PLAYTIME frame.**
- **Status:** seen once in 300 frames. It did not repeat in 16 more 30-frame windows (max 0.26-0.48 ms) or in the
  builder's runs. It is most likely GC or the first fill.
- **Fix:** no action. Re-check on a phone (M-13).

**M-12. Lighting.**
- **Status:** OK as built, and cheaper than before.
- **Optional:**
  - SunRays at 0.05 is close to invisible but still costs a pass on mid/high devices. Set `SunRays.Enabled = false` if
    the owner can't see a difference in screenshots (owner rule: pick from screenshots first).
  - WeatherClient line 83 (pre-existing): set `tint.Enabled = false` while no weather tint is on.

**M-13. Not measured: a real low-end phone.**
- **Why it matters:** every phone number above is an estimate.
- **Check:** 10 minutes on the oldest phone available, with the offer active and the Gift window opened a few times.
  Watch Developer Console (F9) > Memory (Gui / LuaHeap flat) and Script Performance (StarterPackHud, StreakClient,
  RebirthClient). Expect StarterPackHud under 1 % activity.

## Checklist answers

- **RenderStepped / Heartbeat / while loops / polls:**
  - HUD: 1 RenderStepped (idle when hidden) + a 0.1 s poll (M-2).
  - Popup: 1 RenderStepped (M-4) + 0.5 s loop + 0.5 s auto-popup poll (M-6).
  - Gift: StreakClient RenderStepped (one check when closed), PlaytimeClient RenderStepped (tile badge, M-7), bat loop
    (connected only while open), daily auto-open poll (M-10).
  - RebirthClient: 3 RenderSteppeds (rays only on the page, arrows M-9 / I-1, badge M-8) + 2 polls (I-2).
  - No Heartbeat loops.
- **Idle when hidden:** yes, for the HUD motion (verified), the Gift window (verified: counters frozen, BatLoop false),
  the popup sunburst (bool check) and the Rebirth page rays. The polls keep running: M-2, M-6, M-10, I-2.
- **Instance.new or strings per frame:** none. The 10 Hz text refreshes are guarded (H.fit caches on HatchText; the HUD
  timer only writes when the second changes). The fly-text and shards are per-claim and destroyed after 0.6-0.95 s.
- **TweenService:Create spam:** none per frame. Tweens are created on input, show/hide, every 3 s (Day 7 shine) and
  every 1.85 s (REBIRTH button, only while that page is open and ready).
- **Connections:** no leaks. Every new gui is ResetOnSpawn = false and built once from StarterPlayerScripts. Verified
  with 3 respawns, 30 HUD hide/shows and 30 Gift opens; the Signals memory stayed flat.
- **GetAttribute polling where a signal would do:** the HUD poll is justified (transient banners and toasts have no
  single signal) but should park when gone for good (M-2). RebirthClient polls Money on purpose but decodes too much
  (I-2). M-6 and M-10 can use signals.
- **TextScaled churn:** none per frame in the HUD (fixed TextSize). Per frame only in M-8 (1 label), measured
  negligible. Popup/Shop TextScaled labels change at most once a second.
- **UIGradient / rotation on many objects:** HUD 13 rotations per frame (2 suns, 2 stars, 9 bundle parts), no animated
  gradients. Gift DAILY: rays + prism gradient + CLAIM pulses while open. Celebration: rays + rainbow offset for 6 s.
  All fine.

## Final state

Studio is back in Edit, `TestFreshSave` = false (read back), `TestStarterPack` = true (untouched). No script or Edit
instance was changed; all measurement code ran in the Play datamodels only.
