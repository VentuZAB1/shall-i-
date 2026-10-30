# Review: Starter Pack HUD offer v2 plan (2026-10-21)

**Reviewed:** `docs/plans/2026-10-21-starter-pack-hud-icon.md`, the mock `tests-2026-10-21/starter_hud_v2_mock.jpg`, both owner references, the v1 shots, Check-UI `SKILL.md` + `DESIGN_SYSTEM.md`, and the screen-zone memory.

**Checked live:** the owner's Studio, Edit DataModel, read-only. Nothing was written and Play was not touched.

## Verdict: APPROVE WITH CHANGES

The plan gets the big calls right:
- Placement: frameless art above the right column.
- One motion loop.
- It yields instead of fighting for space.
- The popup is the only way to buy.
- An exact list of removals.

Four things must change before it is built:
- **The art reads as icons orbiting an egg, not as a bundle.** The pieces float apart with gaps between them, and the hero egg is too small.
- **The left-right motion is too small to see.** ±2 px of drift is not what the owner asked for.
- **Four states would leave the art on screen when it shouldn't be:**
  - the slingshot flight
  - weather cutscenes
  - the inventory window
  - the Auto Reconnect label on phones
- **One touch bug:** after one tap, the hover spring sticks at 1.05 and the pops stop for good.

All of these are small, exact edits. Nothing needs a re-plan.

---

## 0. Owner ruling R1 (player list kept): the rule

**Decision: (a) accept it.** The offer never reads, guesses or reacts to the Roblox player list:
- no `GetCore` / `SetCore` call
- no `CoreGui` access
- no Tab-key tracking
- no `SetCoreGuiEnabled`
- no change of position or visibility while the list is open

**Why not (b), detecting the list:**
- **No supported API.** Nothing exposes "the player list is open". CoreGui is not readable from a LocalScript; the planner's "0 visible frames" came from plugin security in Studio, which a live client doesn't have.
- **Tab tracking is flaky.** The list also opens and closes from the Roblox menu and the top bar. Its default state also depends on the device and the screen size. Counting Tab presses goes out of sync on the first toggle that isn't Tab.
- **Hiding or moving the art would make it jump** every time someone presses Tab. That is worse than sitting under the list.

**Why (a) is safe for the owner's complaint:**
- CoreGui always draws above PlayerGui. The list covers the art, never the other way round, so the art can never cover the list's text.
- Clicks on the list go to the list.

**What to expect:** with the list open on PC, how much of the art it covers depends on the server's player count (MaxPlayers is 60, so a busy server means a tall list). The Shop card and the one-time popup still carry the offer.

**Check:** the Studio reading ("closed") does not prove the live default. In one live PC join, take one screenshot with the list open and save it as `tests-2026-10-21/starter_hud_v2_playerlist.jpg`. No code test is needed.

---

## MUST changes

### MUST 1: Make it one tight bundle with a bigger hero (the "basic" fix)

**Why:**
- In both references, the side items peek out from BEHIND the hero and overlap it heavily, so the whole art reads as one sticker.
- In the mock, the items orbit the egg with clear gaps, and the price sits beside a potion instead of on the hero.
- The hero is 68 baseline px, about 55% of the art. In the references the hero is about 63-65%.

**Change:** replace the Float table in plan section 5.2 with this. Every offset is from the Float centre.

| Layer | Size | Offset | Rest rot | ZIndex | Read |
|---|---|---|---|---|---|
| SunA | 108 | (0, 0) | spins +20°/s | 1 | unchanged |
| SunB | 86 | (0, 0) | spins -14°/s | 2 | unchanged |
| PotionBack (Speed) | 32 | (-27, -27) | -20 | 3 | about half hidden BEHIND the egg's upper left |
| CashBack | 44 | (28, -28) | 14 | 3 | about half hidden BEHIND the egg's upper right |
| EggShadow | 80 | Egg + (3, 5) | = Egg | 4 | |
| **Egg** | **80** (was 68) | (0, -4) | -6 | 5 | the hero, about 63% of the art |
| PotionL (Money) | 36 | (-32, 26) | -14 | 6 | in front, over the egg's lower left |
| PotionM (Hatch) | 38 | (-6, 34) | 6 | 7 | in front of the egg's base |
| Star1 / Star2 | 14 / 11 | (44, 4) / (-46, -8) | spin | 8 | |
| Price | 58x25 | (32, 38) | -8 | 9 | ON the egg's lower right, like reference 2 |

**Restricted players:** Egg and EggShadow show the cash image at 74 (was 62); the rest is unchanged.

**Float rest centre:** `(73, 73)` (was `(75, 72)`).

**The new envelope:** I recomputed it with the plan's own over-estimates:
- pop 1.08
- PriceScale up to 1.14
- the per-item kicks
- the sway corner term
- the new drift and bob from MUST 2

The result is right 76, left 73, up 72, down 72 from the Float centre. Inside Root 150 x 170 (caption top at 147) and 150 x 146 (compact), that means:
- right edge 149 of 150
- left edge 0.2
- top 1.2
- bottom 145.2

**Builder rule:** the section 10 envelope test is the judge. If any edge fails by more than 1 px, scale ALL Float offsets by 0.96. Never move the Root or the caption.

### MUST 2: Visible left-right and up-down motion (the owner's words)

**Why:**
- ±2 px of drift (2.4 px at 1080p) can hardly be seen. The owner asked for "left n right up n down".
- Periods of 3.6 s and 2.4 s make a 2:3 Lissajous curve, not the figure-8 the plan describes.

**Replace the section 6.2 formulas with these:**

| Property | Formula |
|---|---|
| Float X | `73 + wave(4, 4.0, 0, t)` |
| Float Y | `73 - wave(5, 2.0, 0, t)` |
| Float Rotation | `wave(3, 4.0, math.pi/2, t)` |

- The 1:2 periods trace a true ∞ path.
- The ±3° rotation leans into the direction of the drift.
- Per-item bobs, tilts and pops stay as planned.
- At 1080p this is ±4.7 px across and ±5.9 px up and down, at a gentle ~18 px/s peak. Lively, not nauseating.

### MUST 3: Show and hide must not overshoot the envelope

**Why:** Back easing overshoots to about 1.10.
- Back Out on show and Back In on hide scale the whole Body about 10% past the envelope, once per show and once per hide.
- On a phone (compact, 3.8 px gap) the art's bottom then dips about 1 px into the Eggs tile.
- Inside the clipping CoreUISafeInsets space, it can also get cut at the edge.

**Change:**
- **Show:** `TweenInfo.new(0.22, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)` to 1, then `popStart = now + 0.22`. The regular pop, already inside the envelope budget, gives the bounce.
- **Hide:** `TweenInfo.new(0.14, Enum.EasingStyle.Quad, Enum.EasingDirection.In)` to 0.

### MUST 4: One state machine, so it never flickers

- **Show** only after `wanted()` has been true **continuously for 0.30 s**.
- **Hide** at once.
- **One tween at a time:** keep one `currentTween`. Cancel it on every change, and always tween `ShowScale` from its CURRENT value; never snap it to 0 before a show.
- **`Root.Visible = false`** only in the hide tween's `Completed`, and only if that tween is still the current one.

**Why this matters:**
- The column's `SLIDE_IN` is Back Out, so on the way home its X passes `HOME_X` and overshoots past it.
- Treadmill on/off and modal open/close can toggle within a fraction of a second.
- The debounce removes the 1-frame "wanted" blips.

### MUST 5: DisplayOrder 1, not 2

**Why:** at DisplayOrder 2 it ties with PetsEggsUI and SpeedOffer, and the draw order of a tie is undefined (the plan's R6).

**At 1:**
- the column tiles and the SpeedOffer always draw OVER the art
- AreaTitle and SpeedUI (0) stay under it

Every other HUD element with text is at 3 or higher, so the art can never draw over their text either. I checked that no other ScreenGui uses DisplayOrder 1.

### MUST 6: Missing hide states (add them to `wanted()`)

| Add | Why (verified in code) |
|---|---|
| `workspace.CurrentCamera.CameraType == Enum.CameraType.Scriptable` → hidden | One generic rule for every scripted camera: intro, hatch cinematic, the UFO and Meteor cutscenes, the admin trailer, the pouch and the flight. Nothing else in the game sets Scriptable. |
| `player:GetAttribute("InWeatherCutscene") == true` → hidden | Set by UFOClient and MeteorClient; the plan misses it |
| `pg.SlingUI.Enabled == true` → hidden | `SlingLocalPhase` is only `"Aiming"` (Boarding, Height, Power) and **nil during Launching and Flying**. The plan's comment "the whole slingshot flow" is wrong. Keep the SlingLocalPhase check too, because it is instant. |
| MODALS += `"InventoryUI"`, `"IntroCutsceneGui"` | InventoryUI (DisplayOrder 115) is a real window that sits on the hotbar; the one-window-at-a-time rule applies. IntroCutsceneGui is a backup to IntroPlaying, like `quiet()` does. |
| `phone and pg.SpeedOffer.Enabled` → hidden. `phone = UserInputService.TouchEnabled and Camera.ViewportSize.Y < 520`, read once at start (exactly as SpeedOfferClient does) | It's a rule, not a rect test. SpeedOfferClient places its brick with `task.defer` after Enabled turns on, so for one frame the rect is stale. On PC it stays rect-tested, and stays visible. |

### MUST 7: Yield to the Auto Reconnect label

Add `AutoReconnect.Label` (when `Visible`) to the `overlapsAvoid()` list.

**Why:**
- The label shows after **30 s idle** (`AutoReconnectConfig.SHOW_AFTER = 30`). That is exactly when a player is looking at their base and the art is up.
- On phones, `AutoReconnectConfig.place()` walks its avoid chain (hotbar → touch jump button → **RightTiles**). Each hit pushes the label up, and the last push puts it directly above the column, in our slot.
- It draws at DisplayOrder 4, over the art. That is the same "text on the art" mess v1 had.

### MUST 8: The odds guard (paid random items)

- **StarterPackHud never sells.** No `PromptProductPurchase`, no `StarterPack.Buy` and no `Shop.Buy` in the script. Its only action is `popup:FindFirstChild("Open")`, looked up at click time, then `:Fire()`.
- **If StarterPackUI or its `Open` event never appears, the art never shows.** That would mean no odds path, so no offer.
  - Wait for it with a loop of `WaitForChild(…, 5)` until found. Don't `error` on a nil after 30 s.
  - Also gate `wanted()` on `popup ~= nil and popup:FindFirstChild("Open") ~= nil`.

**The "i" button: not added. I agree with the planner.**
- The whole art opens the popup, and the popup shows numeric odds for every outcome before BUY.
- A tap never prompts a purchase.
- An "i" would open the same popup, and on phones it would be about 15 px, far below the tap minimum.
- Reference 2 needs an "i" because its art buys directly; ours doesn't.
- Restricted players (StarterRestricted) get the cash hero: no random item, so no odds needed.

### MUST 9: The hover spring breaks on touch

**Bug:** section 6.5 sets the target to 1.05 on `MouseButton1Up`.
- On touch there is no `MouseLeave`, so the art stays at 1.05.
- "While hovered, skip the pop" then stops all pops for good.
- The same thing happens on PC when the popup opens over the art: the art is occluded, and `MouseLeave` is not guaranteed.

**Rule:**
- The target goes to 1.05 only for real mouse hover: `MouseEnter` while `UserInputService:GetLastInputType()` is `MouseMovement`, `MouseButton1` or `MouseWheel`.
- `MouseButton1Up` goes back to 1.05 only in that same case; otherwise it goes to 1.
- On every hide AND every show: `hoverTarget, hoverCur, hovered = 1, 1, false`.

### MUST 10: Make the layout math testable for screens Studio can't switch to

**Why:** the builder can't change the viewport (the owner drives the emulator), so section 4.4's phone, ultra-wide and 16:10 rows can't be checked live.

**Change:**
- Write the math of `layout()` as a pure function: `solve(gs: Vector2, k: number, colTop: number, colRight: number, insetY: number) -> (s, compact, x0, y0, x1, y1)`. `layout()` only calls it.
- In Studio only, add a BindableFunction `StarterOfferHud.TestLayout`, the same pattern as `TestOpen` / `TestBuy`. It returns `solve(...)` for the numbers passed in.

**The builder asserts these rows to ±1 px.** All values are gui px with a top bar of 58. The last three rows are new; I computed them.

| Screen | Gui size | k | Column top / right | s | Root rect (gui) |
|---|---|---|---|---|---|
| 1050x620 | 1050x562 | 1.00 | 190.0 / 1040.1 | 1.00 full | 890..1040, 14..184 |
| 1920x1080 | 1920x1022 | 1.18 | 345.4 / 1902.0 | 1.18 full | 1725..1902, 137.7..338.3 |
| 1519x753 | 1519x695 | 1.18 | 234 / 1504 | 1.18 full | 1327..1504, 26..227 |
| 744x435 (column at 1.3) | 744x377 | 0.70 | 109.1 / 737 | 0.68 compact | 635..737, 6..105 |
| 844x390 phone, safe width 750 | 750x332 | 0.63 | 96.1 / 743 | 0.60 compact | 653..743, 5..92 |
| 667x375 phone | 667x317 | 0.61 | 92 / 661 | 0.57 compact | 575..661, 5..88 |
| **1440x900 (16:10)** | 1440x842 | 1.18 | **289.7** / 1426.5 | 1.18 full | 1249..1426, 82..283 |
| **1024x768 iPad (touch, no 1.3)** | 1024x710 | 0.975 | **261.6** / 1014.4 | 0.975 full | 868..1014, 90..256 |
| **2560x1080 (21:9)** | 2560x1022 | 1.18 | 345.4 / 2536 | 1.18 full | 2359..2536, 138..338 |

For each row, also assert no intersection with these formula rects:
- **REBIRTH READY:** centre 0.5 x screen width, half-width `310·k·1.1`. The 1.1 is its Back pop. Right edges:
  - 1123 at 1440
  - 845 at the iPad
  - 866 at 1050
- **The $/Day band:** screen y 8..58.

### MUST 11: Live test additions (section 10.3)

**1. Force transients visible before the overlap test**, otherwise their rects are stale and `hit()` proves nothing:
- `RebirthReadyUI.Banner.Visible = true` with its `Pop` UIScale at 1.1
- `AreaTitle.Banner.Visible = true` with the longest area name + emoji; test its TextBounds rect, not the 70% box (on 4:3 the box touches the art by 2 px; the text never does)
- AdminBanner with a long test message
- AutoReconnect: its Studio switch + `AutoReconnectIgnoreInput`, waiting out the 3 s test `SHOW_AFTER`

Then for each one, assert either "no overlap" or "art hidden (yielded)".

**2. Add these to the overlap list:**
- `AutoReconnect.Label`
- `SpeedUI.Holder.Potions`
- `SpeedOffer.Offer`
- `RebirthReadyUI.Banner`
- `AdminBanner.Banner`
- the `AreaTitle.Banner.Title` TextBounds rect
- `SlingUI.Exit`

**3. Toggle tests** for the MUST 6 rules (each: hidden, then back after ≥ 0.3 s):
- CameraType Scriptable → Custom
- `InWeatherCutscene` true → nil
- `SlingUI.Enabled` true → false
- `InventoryUI.Enabled` true → false

Before asserting visible, confirm `CameraType == Custom`.

**4. Flicker test:**
- **Fast toggling:** toggle `pg.OfflineUI.Enabled` every 0.1 s for 2 s. Sample every frame. Assert `Root.Visible` never turns true and `ShowScale.Scale` never goes above 0.05.
- **Slow toggling:** one 1 s on, 1 s off cycle gives exactly one hide and one show. The show starts ≥ 0.30 s after the modal closes, and `ShowScale` changes by less than 0.2 per frame.

**5. Touch hover (MUST 9):** fire `Hit.MouseButton1Up` with the last input type Touch. Then assert `hoverTarget == 1`, and that a pop happens within 6 s.

**6. Grep assertion (MUST 8):** the StarterPackHud source contains none of `PromptProductPurchase`, `Buy`, `InvokeServer`.

### MUST 12: R1, as in section 0

- **In code:** no player-list detection, no repositioning, and no `SetCoreGuiEnabled(PlayerList, …)`.
- **In the plan text:** replace risk R1 with the section 0 rule.

---

## SHOULD changes

1. **Tighten the caption to the art (looks like reference 1).**
   - Caption centre y **148** (was 156), so its top is at 139. FULL Root height **162** (was 170).
   - The rest gap between the art and the caption drops from 19 to 11 baseline px.
   - At the motion extremes the art slips up to about 6 px BEHIND the caption. The caption's ZIndex 20 keeps the text on top, so it is never covered.
   - The envelope test's "clear of the caption" becomes "every Float descendant ZIndex < Caption.ZIndex".
   - This is a look call; the owner can veto it from the screenshot.
2. **Caption stroke 2.2** (was 2.6). Check-UI pairs 13-16 px text with a 1.8-2.2 stroke; 2.6 on GothamBlack at 16 px muddies the letter gaps when scaled.
3. **Hit area = the art, not the motion envelope.**
   - Hit Size **120x112**, centred at (73, 73).
   - In FULL mode, plus a second transparent TextButton **140x20** over the caption.
   - Egg placement is tap/click on the world, so the envelope's transparent corners (177x201 at 1080p) should not swallow those clicks. On phones that's 72x67 px, still above 44.
4. **Reduced motion.** `GuiService.ReducedMotionEnabled` exists in this build (read: false). When true:
   - all drift, bob and tilt amplitudes ×0.3
   - no pops
   - the sunbursts still turn
5. **Inset signal.** Name it: `GuiService:GetPropertyChangedSignal("TopbarInset")` → `layout()`. Early in startup `GetGuiInset()` can still be 0.
6. **Cheap extra avoids:**
   - `WeatherTiles.Tip`
   - the TextBounds rects of the `HatchCard` TextLabels (normal hatches put a 0.9-width text box at y 0.24 that runs through our x range; the actual text never reaches it today)
7. **Fix plan section 2.4.** The column is width-limited whenever the gui W/H < 1.7775: 16:10 laptops, 4:3, iPad. The general formula is `colTop = 0.5H - min(0.16205H, 0.091165W) * scale`. The code is fine because `layout()` reads the live column; the documentation and the table aren't.
8. **Amount box width 44** (was 36), so a 3-digit regional price still renders at the 22 px maximum. Shift the Price frame to 64 wide, centred at the same point. The envelope then grows by 3 px on the right; take it from the Float X, using 72.
9. **HOME_X sanity check** in the test: at rest, `math.abs(RightTiles.Position.X.Scale - HOME_X) < 1e-4`. PetsEggsUI computes TILES_X the same way, and the test catches any later drift.
10. **Egg outline twin, only if needed.** Some egg icons may lack a dark outline of 2 px or more. For those, add `EggOutline` behind the egg: the same image, ImageColor3 black, size 86, ZIndex 4. That gives the sticker edge the reference items have.
11. **Phone stroke check.** In the phone screenshot, confirm the Amount stroke still reads as an outline at s 0.6 (about 13 px text). If it blobs, set `UIStroke.Thickness = 3 * math.max(s, 0.75)` in `layout()`.

---

## What's good

- **Placement:** above the right column is the right zone. The left side loses to the chat (PC) and the moved pills (phones). The measured HUD map is accurate; I re-derived the 1050, 1080p, 1519, 744 and both phone rows.
- **Frameless:** no tile and no ribbon, with a price on the art and a white stroked caption. It matches both references.
- **Motion design:** one RenderStepped loop that's idle while hidden; only Show and Hide are tweened. Hit and Root never move, animated parts are centre-anchored, and the Root's (1, 1) anchor is a pure layout anchor.
- **Yield, don't fight:** `overlapsAvoid()` plus its own rect numbers, because AbsolutePosition goes stale while hidden.
- **Live price:** one GetProductInfo, shared through the `Price` attribute on StarterPackUI. The HUD and the BUY button can't disagree.
- **The StarterPackClient removal table is exact.** I checked every line in Studio:
  - 4-6 header
  - 18 `UserInputService` (used only at 392)
  - the 384-464 block
  - the `tiles` move for `quiet()` at line 574
  - 508-512, 532, 535-548, 552
- **Other plan details that are correct:**
  - Compact mode on phones: dropping the caption is right. With a caption the art would shrink to s 0.51 and the caption would be 8 px, smaller than "Potions" on the tiles.
  - The 3 s PolicyService delay and the restricted hero.
  - The backup, the TestFreshSave rules, and the "don't drive Studio UI" note.

---

## Owner's calls

1. **R1 player list:** decided. Keep the list, and the art lives under it (section 0).
2. **PC on the treadmill:** today both offers show on PC (Speed bottom left, Starter top right; no overlap). Should the Starter art also yield to the Speed offer on PC ("one offer at a time")? My default is no: it costs Starter exposure during long treadmill sessions.
3. **The caption tightening** (SHOULD 1). Judge it from `starter_hud_v2_idle.jpg`.
4. **R9:** if it still reads "basic" in game after MUST 1-2, the next step is a Blender-rendered bundle PNG through the group FBX carrier. That needs the owner's go-ahead for an upload.
5. **R2:** on 1440p and above the art stays at the 1.18 clamp, smaller than the tiles. Accept it, or allow s up to `colWidth / 83`. I recommend accepting; it matches reference 1's proportions at 1080p.

---

## Verified in Studio (Edit, read-only)

- **Display orders:**
  - PetsEggsUI 2, SpeedOffer 2, MainMenu 3
  - OfflineBaseUI 4, AutoReconnect 4
  - RebirthReadyUI 6, AdminBanner 6, SlingUI 6
  - WaveBanner 8, TopbarPlus 10
  - InventoryUI 115
  - nothing at 1
- **RightTiles:** home X = 1 - 0.0094. UIScale 1.3 when Vy < 520 (no touch check), and it slides with Back Out.
- **Slingshot attributes:** `SlingLocalPhase` is `"Aiming"` or nil only. `SlingPhase` (server) starts as `"None"`. SlingUI is enabled for Launching and Flying too.
- **Other attributes:** `InWeatherCutscene` (UFO, Meteor), `InHatchCinematic` and `IntroPlaying` all exist.
- **Scriptable camera:** set only by SlingshotClient, HatchClient, IntroCutscene, UFO, Meteor and the Trailer.
- **AutoReconnect:** the label shows after 30 s idle, and its `place()` pushes it above RightTiles when blocked.
- **REBIRTH READY:** 620x120 × deviceScale at (0.5, 0.22), Back pop from 0.3.
- **AreaTitle:** text box 0.7W, banner y 0.059..0.170H, slides with Back.
- **Player list and server:** PlayerList CoreGui is enabled, and MaxPlayers is 60.
- **Assets and config:** every asset id in section 12 matches the code. `P.POTIONS = {"Money", "Hatch", "Speed"}`.
- **Reduced motion:** `GuiService.ReducedMotionEnabled` is readable.
