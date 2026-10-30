# Starter Pack HUD offer v2: plan (2026-10-21)

**Owner's verdict on v1:** "the HUD ICON Placement is so bad, the UI is so ugly it hovers over text, looks so basic..."

**Owner's motion note:** "its like animated style going left n right up n down shit like that"

**Scope:**
- Only the HUD entry point changes.
- The popup (PlayerGui.StarterPackUI) and the Shop card stay as they are.
- Server, config and product are untouched.

**Planner:** this file is a plan. No game code was changed.

---

## 0. The decision

1. **Where.** RIGHT edge, directly ABOVE the Eggs / Pets / Potions column (PetsEggsUI.RightTiles).
   - The art's bottom-right corner is pinned to the column's home top-right corner, with a 6 px gap at baseline.
   - It sits in its own ScreenGui. It is not a tile and is not inside the column.
2. **What.** A FRAMELESS bundle: no tile, no card, no ribbon.
   - **Hero:** the next area's BIG egg.
   - **Around the egg:** the 3 potions spilling out and a cash stack.
   - **Behind:** two counter-rotating sunbursts and two twinkling stars.
   - **Price:** a lime Robux price ("49", live regional price) overlapping the art's lower right.
   - **Caption:** a white GothamBlack "STARTER PACK" under the art, static and stroked.
3. **Motion.**
   - **Always on:** the whole bundle floats in a slow figure-8 (left-right drift plus up-down bob) and sways ±3°.
   - **Per item:** each item bobs and tilts on its own phase.
   - **Every 6 s:** a pop (the egg hops, the potions kick, the price pops).
   - **Implementation:** one RenderStepped loop that runs only while the art is visible. The ONLY tweens are show and hide.
4. **States.**
   - **Hidden:**
     - in the tutorial, the intro and the hatch cinematic
     - in the slingshot (any SlingLocalPhase)
     - while any window or popup is open
     - while the column is stepped aside (side panel, window, pouch)
     - while something overlaps its spot (phones: the treadmill Speed offer)
   - **Owned:** gone for good.
5. **Phones.**
   - The same art, auto-fitted into the ~85 px gap above the column.
   - Below a 11 px caption the layout switches to COMPACT: the caption drops, while the art and the price stay.

**Mock** (placement plus composition at 1519x753; a generic egg stands in for the in-game Tide egg):
- `tests-2026-10-21/starter_hud_v2_mock.jpg`
- The red box is the Root (the motion envelope). The cyan box is the RightTiles column.

---

## 1. The owner's references

### Reference 1: `tests-2026-10-21/starter_reference_owner.webp` (1919x1079)

The owner's main reference: **frameless art above the offer stack.**
- **Where.** RIGHT side, upper middle. A frameless bundle art: a unicorn pet with a gold potion behind on the left, a lightning bolt behind at the top and a rebirth icon on the right.
  - It is about 103x115 px at x 1712..1815, y 307..422.
  - There is no tile, no box and no card, only a faint warm glow behind.
- **Caption.** "STARTER PACK" under it: white GothamBlack-like text with a black stroke, about 11-12 px tall, at y 421..432.
- **The stack below.** About 25 px further down are the stacked offer bricks: +2x SKILL / ONLY 5 R$ and 2x WINS / ONLY 55 R$. Each is 180x75 at x 1722..1902, starting at y 457.
  - The art is NOT centred on the stack. Its centre (x 1763) is left of the stack's centre (x 1812), and its right edge stops mid-stack.
- **Clearance.** Nothing overlaps it, and it overlaps nothing.

### Reference 2: `tests-2026-10-21/starter_reference_owner2.webp` (1919x1079)

The owner pointed at its LEFT side.

**Left: "Random Brainrot"**
- **Art.** A frameless black-silhouette pet (a mystery item), about 70x110 px at y 125..235. It is centred over the 2x2 menu grid (Shop / Index / Rebirth / Trade at x 22..285, y 293..570).
- **Price.** A green Robux "7" with NO box, just text and icon with a dark stroke, overlapping the art's lower right.
- **"i" button.** A blue round "i" at the art's top left, the odds/info button.
- **Caption.** "Random Brainrot", white with a black stroke, about 20 px, at y 238..262. The gap down to the grid is about 30 px.

**Right: the same pattern again**
- A tilted pet art ("Buffaroni Pizzanini") with a tilted green "399".
- It sits above the stacked x2 Power [10m] / x2 Cash [10m] bricks, right edges near the screen edge.

**Also visible:**
- a red "FREE" tag hanging off the Shop tile
- frameless bottom-left icons (gift, calendar with a red "!")

### What we take from them

| Taken | Our version |
|---|---|
| Frameless bundle art, items spilling around a hero | The BIG egg as the hero; potions + cash around it; glow behind |
| A price ON the art, no box | Lime Robux icon + amount, tilted -8°, overlapping the lower right |
| A small white stroked caption under the art | "STARTER PACK", GothamBlack, white, black stroke |
| Sits ABOVE the stack of side buttons, clear space all round | Above the Eggs / Pets / Potions column, auto-fitted to the free gap |
| Feels alive (owner's note) | A constant float, sway and per-item motion, plus a pop every 6 s |

**Not taken: the "i" button.**
- Here the whole art opens the popup, and the popup already shows the egg's odds before any purchase.
- A second target the size of a tooltip would be about 15 px on a phone, below the minimum tap size.
- It would open the same thing anyway.

---

## 2. The measured HUD map

### 2.1 How it was measured

- **Session:** Studio Play, one session, TestFreshSave = true (set back to false afterwards), on a PC.
- **Viewport:** 1519x753. GuiService inset = 58, so the top bar band is screen y 0..58.
- **Notes:**
  - All y values below are SCREEN px (AbsolutePosition.Y + 58).
  - The Daily Rewards window auto-opened on join and was closed before measuring. Expect it on every fresh join.
  - The session was stopped from outside right after the dump (not by me). TestFreshSave was then set back to false and verified.

### 2.2 Measured elements

| Element | Gui (DisplayOrder, IgnoreGuiInset) | Rect (screen px) | Notes |
|---|---|---|---|
| Roblox core top-bar buttons | CoreGui | x 0..208, y 0..58 | |
| TopbarPlus icons (Inventory, Settings) | TopbarStandard (10, true) | x 216..369, y 12..56 | Left-aligned; nothing on the right |
| OfflineBaseUI.PerDay "You earn $X/Day" | (4, true) | x 379..1139, y 10..56 | Inside the top band on PC. On phones it slides right and narrows (it can reach x = W-8) |
| AreaTitle.Banner (1.9 s on entering an area) | (0, false) | Full-width strip, y 99..177 | Title text box x 227..1291 (centre 70%) |
| RebirthReadyUI.Banner | (6, true) | x 394..1126, y 95..237 | Centred (0.5, 0.22), 620x120 x deviceScale |
| AdminBanner.Banner (transient bar) | (6, false) | Centred, top at gui 0.2H = screen 197, ~53 tall | AutomaticSize width, at most 80% of the screen (x 152..1367 max) |
| TutorialUI Card / Guide / Banner / Finish | (5, false) | Top centre (Guide x 334..1184, y 68..207) | Tutorial only |
| WaveBanner "INCOMING" | (8, false) | Centred 50% width, gui y 0.004..0.054 | |
| EggPlaceUI.Toast | (0, true) | x 459..1059, y 220..260 | |
| Shield / Inventory / Gift toasts | (30 / 116 / 30) | Centred 50-70% width | GiftToast.Granted y 87..132; Toast y 614..655 |
| MainMenu.Menu (2x2: Shop/Claim, Rebirth/Index) | (3, false) | x 14..173, y 321..489 | Claim "!" badge reaches y 324 |
| AdminUI.AdminButton (OWNER ONLY) | (4, false) | x 23..163, y 290..320 | Directly above the left grid |
| SpeedUI.Holder (Speed, Money, Friends pills) | (0, false) | x 14..278, y 595..745 | |
| PotionHud timers (SpeedUI.Holder.Potions) | | x 286..536, y 662..704 | Right of the money pill |
| SpeedOffer.Offer (treadmill only) | (2, true) | PC: between the left grid and the pills | Phones: right above RightTiles, right edges aligned |
| **PetsEggsUI.RightTiles** | (2, false) | **x 1437..1504, y 292..518** | Eggs 292..364, Pets 369..441, Potions 446..518. Right margin 15 px. Home X scale = 1 - 0.0094 = 0.9906 |
| v1 StarterPackTile (the problem) | inside RightTiles | Ribbon x 1430..1512, y 182..201; tile y 195..268; price pill y 260..282 | Sunburst x 1406..**1536** (runs off-screen), y 167..**297** (over the Eggs tile). The potions cover its "Starter" label |
| SlingUI.Exit (slingshot only) | (6, true) | x 1443..1496, y 53..105 | Top right |
| WeatherTiles.Row + AutoReconnect.Label | (5 / 4, false) | Bottom-right corner, growing left / above | |
| Hotbar (Satchel) | BackpackGui | Bottom centre | Hidden while a window is open |

### 2.3 Not in PlayerGui, but checked

- **Roblox player list:** NOT disabled.
  - StarterGui:GetCoreGuiEnabled(PlayerList) = true, and leaderstats.Speed exists.
  - No game script calls SetCoreGuiEnabled(PlayerList, false). Only TopbarPlus toggles it for right-aligned dropdowns, and we have none.
  - In this session it was closed (0 visible frames in CoreGui.PlayerList).
  - On PC a player can open it (Tab). It drops from the top-right under the top bar, and CoreGui draws over PlayerGui. See risk R1.
- **Roblox chat window:** ON.
  - TextChatService ChatWindowConfiguration: Enabled, HorizontalAlignment Left, VerticalAlignment Top.
  - On PC it occupies the TOP-LEFT under the top bar.
- **MaxPlayers** is 60.

### 2.4 Geometry formulas (for any screen)

H = the safe-area height below the top bar; W = the safe-area width.

- **Left menu:** height 0.2426H, AspectRatio 0.9466 (height-dominant), centred at y 0.5H.
  - With UIScale 1.3 when the viewport Y < 520 at startup (MenuController).
- **RightTiles:**
  - height 0.32409H, width 0.09631H, anchor (1, 0.5) at (0.9906W, 0.5H)
  - UIScale 1.3 when the viewport Y < 520 at startup (PetsEggsUI; any device, Studio included)
  - Column top = 0.5H - 0.16205H x scale.
- **deviceScale k** = clamp(min(Vx/1050, Vy/620), 0.52, 1.18), with Vx, Vy the full viewport.

---

## 3. Placement

### 3.1 Chosen: right, above the column (reference 1 and the right half of reference 2)

**Why right beats left:**

| | Right, above RightTiles | Left, above the 2x2 grid (ref 2 left) |
|---|---|---|
| PC 1519x753, free height | 227 px (screen y 58..285) | 232 px |
| What else lives there on PC | Nothing (player list only if a player opens it) | The Roblox chat window (top-left by default) and the owner's ADMIN button right above the grid |
| Phones, free height | ~84-88 px (column top 92-96 px below the top bar) | ~40 px: the Speed/Money pills and potion timers move to the top-left on phones (y 4..74), and the 1.3-scaled grid starts at about 114 |
| Neighbours | Only the treadmill Speed offer on phones (handled: the art yields) | The Claim "!" badge, the step-11 Rebirth arrow, the PC SpeedOffer between grid and pills |
| Reads like the reference | Yes: an offer art above a stack of side buttons | Yes (ref 2), but busier |

**Rejected alternatives:**
- **Left above the grid:** it collides with the chat window (PC) and the moved pills (phones). The owner's own ADMIN button sits there.
- **Keep it as a tile in RightTiles (v1):** it reads as "one more menu tile" ("basic"). Its sunburst ran over Eggs and off the screen, and its corner icons covered its own label.
- **Left of the column (beside Eggs/Pets):** it pushes an offer into the 3D view next to the character and breaks the "art above the stack" read.
- **Top centre:** that is the zone of the wave strip, area title, REBIRTH READY, admin bar, $/Day line and tutorial card.
- **Bottom right:** the weather/boost icon row, the Auto Reconnect label, and the jump/PULL buttons on phones.

### 3.2 When the column slides away: HIDE (shrink out), don't follow

- The column slides off to the right for a side panel, any MainMenu window, and the pouch on touch screens.
- The art shrinks out (0.14 s) as soon as the column leaves home. It pops back in (0.28 s) once the column is home again.
- **Why not follow:**
  - In those moments the space is needed: the Potions panel's top reaches 0.2H, and the Shop's side tabs hang off the window there.
  - A 180 px art gliding alongside a sliding panel is noise.
  - One thing open at a time is the layout rule.
- The art's anchor is always computed from the column's HOME position (X scale 0.9906). It never reads the live sliding X, so it never jumps mid-slide.

---

## 4. Layout math (exact)

### 4.1 The ScreenGui

New ScreenGui `StarterOfferHud`:
- ResetOnSpawn = false
- IgnoreGuiInset = false
- ScreenInsets = CoreUISafeInsets, the same space as PetsEggsUI, so its AbsoluteSize equals PetsEggsUI's
- ZIndexBehavior = Sibling
- DisplayOrder = 2
- Enabled = true. Root.Visible does the showing.

### 4.2 Baseline sizes (at deviceScale 1, the 1050x620 baseline)

- **Root FULL** = 150 x 170 (art plus caption). **Root COMPACT** = 150 x 146 (art only).
- These include the motion envelope (section 6.4), so the moving art never leaves the Root box.

### 4.3 layout()

Run it:
- on start and on every show
- on Camera.ViewportSize, gui AbsoluteSize, RightTiles AbsoluteSize and GuiService inset changes

```lua
local FULL, COMPACT = Vector2.new(150, 170), Vector2.new(150, 146)
local fits, compact, s, rect = false, false, 1, nil
local loadedAt = os.clock() -- reset when DataLoaded turns true (if it was already true at start, it's start time)
local function layout()
	local gp, gs = gui.AbsolutePosition, gui.AbsoluteSize
	if gs.X <= 0 or tiles.AbsoluteSize.Y <= 0 then fits = false return end
	local k = deviceScale()                                   -- clamp(min(Vx/1050, Vy/620), 0.52, 1.18)
	local colRight = gs.X * HOME_X                            -- HOME_X = 1 - MainMenu.Menu.Position.X.Scale (0.9906)
	local colTop = tiles.AbsolutePosition.Y - gp.Y            -- the column only slides in X: its top is always valid
	local top = math.max(8 * k, 60 - GuiService:GetGuiInset().Y) -- clear of OfflineBaseUI's $/Day line (screen y 10..56) + 4
	local bottom = colTop - 6 * k                             -- 6 px gap above the Eggs tile
	local slot = bottom - top
	s = math.min(k, slot / FULL.Y)
	compact = 16 * s < 11                                     -- the caption would be under 11 px: drop it
	if compact then s = math.min(k, slot / COMPACT.Y) end
	fits = s >= 0.45                                          -- no room at all: stay hidden
	local size = compact and COMPACT or FULL
	root.Size = UDim2.fromOffset(size.X, size.Y)
	caption.Visible = not compact
	windowScale.Scale = s
	root.Position = UDim2.fromOffset(math.floor(colRight + 0.5), math.floor(bottom + 0.5))
	-- the art's rect in AbsolutePosition space (own numbers: AbsolutePosition doesn't update while hidden)
	rect = {gp.X + colRight - size.X * s, gp.Y + bottom - size.Y * s, gp.X + colRight, gp.Y + bottom}
end
```

- Root has AnchorPoint (1, 1) and attribute `AnchorReason = "edge-pinned HUD (top of the right column)"`.
- Its UIScale `WindowScale` grows it from that corner.

### 4.4 Resulting layout per screen

Gui-local px; screen y = gui y + inset.

| Screen | k | Column top / right / width | Slot | Mode | s | Root px | Root rect (gui) |
|---|---|---|---|---|---|---|---|
| 1050x620 PC (baseline) | 1.00 | 190 / 1040 / 54 | 8..184 = 176 | full | 1.00 | 150x170 | x 890..1040, y 14..184 |
| 1920x1080 PC | 1.18 | 345 / 1902 / 98 | 9..338 = 329 | full | 1.18 | 177x201 | x 1725..1902, y 137..338 |
| 1519x753 PC (owner's Studio, measured) | 1.18 | 234 / 1504 / 66 | 9..227 = 218 | full | 1.18 | 177x201 | x 1327..1504, y 26..227 (screen 84..285) |
| 744x435 PC small window (column 1.3) | 0.70 | 109 / 737 / 47 | 6..105 = 99 | compact | 0.68 | 102x99 | x 635..737, y 6..105 |
| 844x390 phone (inset 58, safe W 750) | 0.63 | 96 / 743 / 42 | 5..92 = 87 | compact | 0.60 | 90x87 | x 653..743, y 5..92 |
| 667x375 phone (inset 58) | 0.61 | 92 / 661 / 40 | 5..88 = 83 | compact | 0.57 | 86x83 | x 575..661, y 5..88 |

- The art is right-aligned to the column, like reference 2 right.
- It is visibly left of the column's centre, like reference 1.
- On every screen it stays clear of everything in section 2:
  - The REBIRTH READY banner's right edge is at most 0.5W + 366 (x 1126 at 1519, 617 on an 844 phone). The art starts further right.
  - The AreaTitle text and the admin bar are centred.

---

## 5. The look, element by element

### 5.1 Hierarchy

All sizes and positions are baseline px; WindowScale scales them.

```
StarterOfferHud (ScreenGui, DisplayOrder 2)
└ Root            Frame  AnchorPoint (1,1)  Size 150x170 / 150x146  BackgroundTransparency 1
  ├ WindowScale   UIScale (s, layout only)
  ├ Hit           TextButton  AnchorPoint (.5,.5) Pos (.5,0,.5,0) Size (1,0,1,0)  Text ""  BackgroundTransparency 1
  │               AutoButtonColor false  Selectable true  ZIndex 30      <- the ONLY input target; never animated
  └ Body          Frame  AnchorPoint (.5,.5) Pos (.5,0,.5,0) Size (1,0,1,0)  transparent
    ├ ShowScale   UIScale (0 <-> 1: show / hide pop; the only tweened thing)
    ├ Float       Frame  AnchorPoint (.5,.5) Size 100x100  Pos fromOffset(75, 72) + motion  Rotation = sway  ZIndex 1
    │ ├ PopScale  UIScale (= pop(t) x hover spring, set every frame)
    │ ├ SunA, SunB, PotionBack, CashBack, EggShadow, Egg, PotionL, PotionM, Star1, Star2
    │ └ Price     Frame (58x25, rotated -8)  + PriceScale UIScale
    │     ├ RobuxOutline, Robux (ImageLabels)
    │     └ Amount (TextLabel)
    └ Caption     TextLabel  ZIndex 20  (static: never moves, never covered by the art)
```

### 5.2 Float layers

- **Rules for every ImageLabel:**
  - BackgroundTransparency 1, AnchorPoint (0.5, 0.5), **ScaleType Fit** (never stretched), square offset sizes.
- **Positions:**
  - "Pos" is the centre in Float-local px: Float centre (50, 50) + offset.
  - Offsets are relative to the Float centre. The Float centre sits at Root (75, 72).

| Layer | Image | Size | Offset from Float centre | Rest rot | ZIndex | Colour / transparency |
|---|---|---|---|---|---|---|
| SunA | sunburst `rbxassetid://130563114903838` | 108 | (0, 0) | spins +20°/s | 1 | ImageColor3 (255, 214, 90), ImageTransparency 0.34 ± 0.04 (breathes) |
| SunB | sunburst (same) | 86 | (0, 0) | spins -14°/s | 2 | ImageColor3 (255, 110, 200), ImageTransparency 0.50 |
| PotionBack (Speed) | `PotionConfig.byKey.Speed.icon` | 32 | (-32, -29) | -20 | 3 | |
| CashBack | cash `rbxassetid://88694661500877` | 43 | (34, -29) | 14 | 3 | |
| EggShadow | same image as Egg | 68 | Egg + (3, 4.5) | = Egg's | 4 | ImageColor3 (0, 0, 0), ImageTransparency 0.55 (cartoon drop shadow; follows the bob, NOT the hop) |
| Egg (hero) | `StreakConfig.EGG_ICONS[StarterEgg]` (fallback TideEgg) | 68 | (-2, -2) | -6 | 5 | |
| PotionL (Money) | `PotionConfig.byKey.Money.icon` | 34 | (-34, 27) | -14 | 6 | |
| PotionM (Hatch) | `PotionConfig.byKey.Hatch.icon` | 36 | (-7, 36) | 6 | 7 | |
| Star1 | star `rbxassetid://93906069548754` (the popup's header star) | 14 | (43, 5) | spins +90°/s | 8 | ImageColor3 (255, 240, 150), own UIScale twinkle |
| Star2 | star (same) | 11 | (-45, -5) | spins +90°/s | 8 | ImageColor3 (255, 240, 150), own UIScale twinkle |
| Price | Frame, BackgroundTransparency 1, AnchorPoint (.5,.5) | 58x25 | (31, 40) | -8 | 9 | Holds the 3 below + UIScale "PriceScale" |

**Inside Price** (Price-local px, from its top-left):

| Child | Spec |
|---|---|
| RobuxOutline | ImageLabel, white Robux `rbxassetid://132185731364109`, ImageColor3 (0, 0, 0), Size 22x22, centre (11, 12.5), ZIndex 9 (fake outline for the icon) |
| Robux | ImageLabel, same asset, ImageColor3 (150, 255, 40) lime, Size 18x18, centre (11, 12.5), ZIndex 10 |
| Amount | TextLabel, Text = live price. AnchorPoint (0, 0.5), Position (22, 0, 12.5, 0) offsets, Size 36x25. GothamBlack, TextScaled + UITextSizeConstraint MaxTextSize 22, TextXAlignment Left. TextColor3 white + UIGradient Rotation 90 (200, 255, 80) -> (90, 220, 0) (the Check-UI lime). UIStroke Thickness 3, Color black, LineJoinMode Round. ZIndex 10 |

**Restricted players** (StarterRestricted == true: no egg in the pack):
- Egg and EggShadow show the CASH image at size 62, rest rot 0.
- CashBack is hidden. Everything else is the same.
- This mirrors the popup's restricted hero.

### 5.3 Caption (Body child, static)

- TextLabel "Caption", Text **"STARTER PACK"**, AnchorPoint (.5, .5), Position fromOffset(75, 156), Size 140x18.
- Font GothamBlack, TextScaled + UITextSizeConstraint MaxTextSize 16, TextColor3 white.
- UIStroke Thickness 2.6, black, LineJoinMode Round. ZIndex 20.
- Measured width at 15 px: 125 baseline px, so it fits 140.
- Hidden in COMPACT mode.
- It is white like both references, with no box and no ribbon.

### 5.4 Fonts, strokes, depth (Check-UI checklist)

- Every text is GothamBlack with a black UIStroke: Caption 2.6, Amount 3.
- Every icon is Fit, with no squash and no stretch. The "pop" is a uniform UIScale.
- **Cartoon depth comes from:**
  - the egg's black drop-shadow twin
  - the black outline twin behind the Robux icon
  - the two counter-rotating sunbursts at different sizes and colours
  - items overlapping front and back
- Every animated thing scales from its centre (Body, Float, Price, Stars; all AnchorPoint .5,.5).
- Root's (1, 1) anchor is a layout anchor only: WindowScale is the device scale, never an animation.
- Sunbursts turn at 20°/s per Check-UI, plus a slower counter-turn for depth.
- They only turn while the loop is active, so they are paused while hidden.

### 5.5 The live price

- **Source:** StarterPackClient already calls `GetProductInfo(ShopConfig.StarterPackProduct, Enum.InfoType.Product)` on the client. That gives the regional PriceInRobux for this player.
- **Change:** it now also publishes the price: `gui:SetAttribute("Price", price)` in `refreshAll` (section 9.2).
- **HUD side:**
  - `Amount.Text = popup:GetAttribute("Price") or tostring(ShopConfig.StarterPackPrice)`
  - Listen to `popup:GetAttributeChangedSignal("Price")`.
- One fetch, one source of truth, the same number the popup's BUY button shows.

---

## 6. Motion: the core of the look

### 6.1 The loop

- One `RunService.RenderStepped` connection, made once. It returns immediately while `active == false` (hidden).
- Time is `t = os.clock()`.
- No tweens except ShowScale (show/hide). Hover/press is a spring computed inside the loop.
- All amplitudes are baseline px; WindowScale scales them with everything else.

```lua
local TAU = 2 * math.pi
local function wave(a, period, phase, t) return a * math.sin(TAU * t / period + phase) end
```

### 6.2 Whole bundle (Float)

Float is the art group. The hit area and the Root never move.

| Property | Formula | Feel |
|---|---|---|
| Position X | `75 + wave(2, 3.6, 0, t)` | Drifts left-right ±2 px every 3.6 s |
| Position Y | `72 - wave(3.5, 2.4, 0, t)` | Bobs up-down ±3.5 px every 2.4 s (rises first) |
| Rotation | `wave(3, 3.0, π/2, t)` | Sways ±3° every 3.0 s |
| PopScale.Scale | `popFactor(p) * hoverCur` | Pop every 6 s, plus hover/press |

The X and Y periods are 3:2, so the bundle traces a slow figure-8: "left n right up n down".

### 6.3 Per item (on top of the Float motion; each on its own phase)

Final position = rest + bob; final rotation = rest + tilt + kick.

| Layer | Bob A (px) / period (s) / phase | Tilt A (°) / period (s) / phase | Pop kick (°) |
|---|---|---|---|
| Egg | 2 / 1.8 / 0 | 3 / 2.6 / π/3 | 0 (it hops instead) |
| EggShadow | Same bob as the Egg, no hop | = Egg's rotation | |
| PotionBack | 2.5 / 2.1 / 3π/2 | 5 / 2.4 / 0 | +10 |
| CashBack | 2.5 / 1.9 / π/4 | 6 / 2.8 / π | -10 |
| PotionL | 2.5 / 1.5 / π/2 | 6 / 2.0 / 0 | +12 |
| PotionM | 2.5 / 1.7 / π | 5 / 2.2 / π/2 | -10 |
| Price | none | `Rotation = -8 + wave(2, 1.6, 0, t)` | `PriceScale = 1 + wave(0.04, 1.2, 0, t) + pricePop` |
| SunA | none | `Rotation += 20·dt` | `ImageTransparency = 0.34 + wave(0.04, 2.0, 0, t)` |
| SunB | none | `Rotation -= 14·dt` | |
| Star1 / Star2 | none | `Rotation += 90·dt` | `scale = max(0, sin(TAU·t/1.6 + ph))^2`, with ph 0 / π (they twinkle in turn) |

### 6.4 The pop

- **When:** every 6 s. The first one comes 1.2 s after each show, to draw the eye.
- **Phase:** `p = t - popStart`. When `p > 0.5`, set `popStart += 6`.

```lua
local function popFactor(p) -- uniform (icons are never stretched): 1 -> 1.08 -> 0.97 -> 1 in 0.5 s
	if p < 0 or p > 0.5 then return 1 end
	if p < 0.12 then local x = p / 0.12 return 1 + 0.08 * (1 - (1 - x) ^ 2) end
	if p < 0.26 then local x = (p - 0.12) / 0.14 return 1.08 - 0.11 * (x * x * (3 - 2 * x)) end
	local x = (p - 0.26) / 0.24 return 0.97 + 0.03 * (x * x * (3 - 2 * x))
end
local hop  = (p >= 0 and p <= 0.4) and -7 * math.sin(math.pi * p / 0.4) or 0           -- egg only
local kick = (p >= 0 and p <= 0.5) and math.sin(math.pi * p / 0.25) * (1 - p / 0.5) or 0 -- x per-layer kick
local pricePop = (p >= 0.15 and p <= 0.4) and 0.10 * math.sin(math.pi * (p - 0.15) / 0.25) or 0
```

- No sound: an idle HUD must not spam audio.
- While hovered (PC), skip the pop (`popFactor = 1`), so hover and pop never stack.

### 6.5 Hover / press (spring in the loop, Check-UI values)

| Event on Hit | hoverTarget |
|---|---|
| MouseEnter | 1.05 |
| MouseLeave | 1.00 |
| MouseButton1Down | 0.94 |
| MouseButton1Up | 1.05 |

- Spring each frame: `hoverCur += (hoverTarget - hoverCur) * (1 - math.exp(-18 * dt))`.
- **Hit.Activated:** `SFX.play("Click")`, then `popup.Open:Fire()`. That opens StarterPackUI, which shows the odds and is the only way to buy.

### 6.6 Motion envelope (why the Root is 150x170)

- **Rest content** (rotated bounding boxes, relative to the Float centre): left 55, right 61, up 55, down 56.
- **Worst case:** the larger of pop 1.08 and hover 1.05, never stacked, plus:
  - sway 3° at the far corner: 4.8 px
  - drift 2 / bob 3.5
  - per-item bob/tilt: about 2.5
- **That gives about:**
  - right 75 (Root right edge = 150, exactly)
  - left 68 (Root x 7)
  - up 70 (Root y 2)
  - down 72 (Root y 144, under the caption's top at 147)
- The moving art therefore never leaves the Root and never reaches the caption.
- On top of that, the Caption's ZIndex is above the whole Float subtree.
- These are bounding-box over-estimates; real pixels are smaller. The builder's envelope test (section 10) checks it live.

---

## 7. States

### 7.1 wanted()

Polled every 0.2 s. It is also run at once on these signals:
- menuWin.Visible
- RightTiles.Position
- the attributes below
- popup.Enabled

```lua
local MODALS = {"OfflineUI", "FreeGiftUI", "UpgradeUI", "SellUI", "StreakCelebrate", "StarterPackUI"}
local function wanted()
	if player:GetAttribute("StarterPack") == true then return false end                     -- owned: gone for good
	if player:GetAttribute("DataLoaded") ~= true or player:GetAttribute("StarterRestricted") == nil then return false end
	if os.clock() - loadedAt < 3 then return false end  -- let PolicyService answer (StarterRestricted starts true = unknown)
	if player:GetAttribute("TutorialDone") ~= true or (player:GetAttribute("TutorialExtra") or 0) ~= 0 then return false end
	if player:GetAttribute("IntroPlaying") == true or player:GetAttribute("InHatchCinematic") == true then return false end
	if player:GetAttribute("SlingLocalPhase") ~= nil then return false end                   -- the whole slingshot flow (Exit sits top-right)
	if menuWin.Visible then return false end                                                -- any MainMenu window (Shop, Gift, Index...)
	for _, n in MODALS do local g = pg:FindFirstChild(n) if g and g:IsA("ScreenGui") and g.Enabled then return false end end
	local adm = pg:FindFirstChild("AdminUI"); local aw = adm and adm:FindFirstChild("Window")
	if aw and aw:IsA("GuiObject") and aw.Visible then return false end                       -- owner's admin window
	if math.abs(tiles.Position.X.Scale - HOME_X) > 0.002 then return false end               -- side panel / window / pouch
	if not fits then return false end
	return not overlapsAvoid()                                                               -- 7.2
end
```

### 7.2 Yield to overlap: the "never covers anything" guarantee

- `overlapsAvoid()` tests `rect`, grown by 4·s px, against each shown element below. Shown means visible up the chain and its ScreenGui enabled.
- Transient banners make the art yield (shrink out) instead of fighting for the spot.

| Avoid | Why it is in the list |
|---|---|
| `SpeedOffer.Offer` (when SpeedOffer.Enabled) | **Phones:** it sits exactly in our slot while you run on your treadmill. On PC it is bottom-left and never intersects |
| `AdminBanner.Banner` | A long admin message (≥ ~75% of the width) can reach our x range at y 0.2H |
| `RebirthReadyUI.Banner` | Never intersects by the numbers in section 4; it costs nothing |
| `AreaTitle.Banner.Title` | Use the TEXT rect (centre ± TextBounds/2), not the full-width strip. The strip's faded right end may pass under the art (DisplayOrder 0 < 2), but text never does |
| `WaveBanner` TextLabels; `GiftToast.Granted`; `ShieldToast.Toast`; `InventoryToast.TextLabel`; `EggPlaceUI.Toast` | Centred toasts. Cheap insurance against a later move |

### 7.3 Show / hide

- **Show:**
  1. `layout()`
  2. `Root.Visible = true`, `active = true`
  3. `ShowScale.Scale = 0`, then tween to 1 over 0.28 s (Back, Out)
  4. `popStart = now + 1.2`
- **Hide:**
  1. Tween ShowScale to 0 over 0.14 s (Back, In).
  2. On Completed, if still unwanted: `Root.Visible = false`, `active = false`. The loop stops working, and the sunbursts are paused.
- **Owned:** the same hide, and it never comes back because wanted() stays false.
  - Keep the gui; don't destroy it. A Studio `StarterDebug "reset"` then brings it back for re-tests.
- **Live updates while shown, no re-show needed:**
  - StarterEgg changes the Egg image (with a pop: `popStart = now`)
  - StarterRestricted changes the hero (egg or cash)
  - the Price attribute changes the Amount text
- **Respawn:** nothing happens (ResetOnSpawn false).

---

## 8. Phones

- **Detection:** `TouchEnabled and Vy < 520`. The column and the left menu get UIScale 1.3 from PetsEggsUI / MenuController. Our layout reads the column's real AbsoluteSize/Position, so it needs no phone branch.
- **Size:** the slot is about 83-87 px, so the layout is COMPACT at s ≈ 0.57-0.60.
  - Root about 86-90 px square; egg about 40 px (≈ the 40-42 px tile width); price text about 13 px.
  - Hit area about 86x83, well above the 44 px minimum tap size.
- **Caption:** dropped in compact mode. At 8-9 px it would be unreadable.
  - The art, the price and a tap that opens "STARTER PACK!" carry it, like the tiny captions in the references.
- **Treadmill:** the Speed offer moves above the column on phones (SpeedOfferClient), so the art yields until you step off.
  - One contextual offer at a time; on the treadmill the Speed offer is the relevant one.
- **Pouch (aiming):** the column slides away and the art is hidden anyway (SlingLocalPhase).
- **The $/Day line:** layout keeps the art's top below screen y 60, since `top = max(8k, 60 - inset)`.
  - With the measured 58 px top bar that changes nothing. It only matters if a phone's top bar is shorter, and then the art never jumps when you walk onto your base.
- **Portrait:** none. StarterGui.ScreenOrientation is LandscapeSensor.

---

## 9. Code changes

### 9.1 NEW: StarterPlayer.StarterPlayerScripts.StarterPackHud (LocalScript)

**Header comment:** what it is, a link to this plan, and "opens StarterPackUI.Open; never sells by itself".

**Requires:**
- ReplicatedStorage.ShopConfig (fallback price)
- PotionConfig (`byKey[...].icon`)
- StreakConfig (`EGG_ICONS`)
- SFX
- No BrickUI.

**Waits for:**
- `PlayerGui.StarterPackUI` (with `.Open`), timeout 30
- `PlayerGui.PetsEggsUI.RightTiles`
- `PlayerGui.MainMenu.Window`
- `MainMenu.Menu`, for HOME_X = 1 - Menu.Position.X.Scale

**Order inside:**
1. constants
2. builders (the tree in section 5.1, ZIndex and colours per section 5.2)
3. `deviceScale`, `layout` (section 4.3)
4. `overlapsAvoid` (section 7.2), `wanted` (section 7.1)
5. `setShown` (section 7.3)
6. the Hit handlers (section 6.5)
7. the RenderStepped loop (sections 6.1-6.4)
8. the 0.2 s poll and the signals
9. `loadedAt` = os.clock() when DataLoaded turns true

**Rules:**
- No other script changes beyond 9.2.
- No server change.
- Check-UI only: no BrickUI studs, no Luckiest font.

### 9.2 EDIT: StarterPlayer.StarterPlayerScripts.StarterPackClient

Remove v1's HUD icon. Line numbers are as of 2026-10-21 10:30.

| Lines | Change |
|---|---|
| 4-6 (header) | Replace the "HUD icon: a pink tile..." bullet with: "HUD offer: StarterPackHud (own LocalScript, frameless art above the right column); it opens this popup via StarterPackUI.Open and reads the live price from StarterPackUI's Price attribute." |
| 18 | Delete `local UserInputService = ...` (only used by `phone`, line 392) |
| 384-464 | Delete the whole section "the HUD icon (above the Eggs / Pets / Potions column)": petsGui/tiles/menu locals, TILE_H/TILE_STEP/colH/ABOVE/LEFT/phone, the tile clone and its tinting, tileSun, `corner()`, the potion/cash corner icons, the price pill (pill, pillRobux, pillText), the ribbon, tileScale, the up/down `setY` press handlers, the `face.Activated` handler, `iconWanted()`, `placeTile()` |
| (move) | Keep two of those lines and put them right above `local function guiOn` (≈ line 559): `local petsGui = pg:WaitForChild("PetsEggsUI")` and `local tiles = petsGui:WaitForChild("RightTiles")`. `quiet()` still uses `tiles` (line 574) |
| 508-512 (in `refreshAll`) | Delete `local show = iconWanted()`, `if tile.Visible ~= show ...`, `face.Icon.Image = ...`, `face.Icon.Visible = ...`, `pillText.Text = price`. Add as the first line: `gui:SetAttribute("Price", price)` |
| 532 | Delete `local pulseAt = os.clock() + 4` |
| 535-548 | In RenderStepped delete the `if tile.Visible then ... end` block (tile sunburst + the 10 s double pulse). Keep only `if gui.Enabled then heroSun.Rotation = ... end` |
| 552 | In the 0.5 s loop delete `placeTile()` |

- **Untouched:**
  - the popup (lines 138-382)
  - the Shop card (466-504)
  - the one-time popup logic (558-594)
  - Open / TestOpen / TestBuy (596-611)
  - all server and config code
- **Backup first:** `ServerStorage._Backup_StarterHud.Before`, holding StarterPackClient as it is now.

---

## 10. Test checklist (builder)

### 10.1 Before Play

- Check get_studio_state = Edit.
- `workspace:SetAttribute("TestFreshSave", true)` and read it back as true.
- Never stop a session you didn't start.
- After Play: stop, then set TestFreshSave back to false.

### 10.2 Getting it visible

- **The fresh test save already qualifies:** TutorialDone true, StarterPack false, Rebirths 0.
- **Close the auto-opened Daily Rewards window first:** `pg.MainMenu.CloseWindow:Fire()`. The art then appears about 3 s after DataLoaded.
- **If it was bought in the session:** Server `ServerStorage.StarterDebug:Invoke("reset", player)`.

### 10.3 Client checks (execute_luau, Client)

1. **Placement:**
   - Root rect equals section 4.4 for the current viewport (±1 px).
   - `rect[4] <= RightTiles.AbsolutePosition.Y - 5`.
   - `rect[3] <= gui width`.
   - Root right edge equals the column's right edge.
2. **Envelope test (13 s = 2 pops):** sample every RenderStepped and union a conservative box for each Float child.

```lua
local pg = game.Players.LocalPlayer.PlayerGui
local root = pg.StarterOfferHud.Root
local float, caption = root.Body.Float, root.Body.Caption
local function artBox()
	local fc = float.AbsolutePosition + float.AbsoluteSize / 2
	local a = math.rad(float.Rotation)
	local x0, y0, x1, y1 = math.huge, math.huge, -math.huge, -math.huge
	for _, o in float:GetChildren() do
		if o:IsA("GuiObject") and o.Visible then
			local c = o.AbsolutePosition + o.AbsoluteSize / 2 - fc -- (AbsolutePosition ignores the parent's Rotation: rotate it)
			c = Vector2.new(c.X * math.cos(a) - c.Y * math.sin(a), c.X * math.sin(a) + c.Y * math.cos(a)) + fc
			local r = (o.Name:match("^Sun") and o.AbsoluteSize.X / 2) or o.AbsoluteSize.Magnitude / 2
			x0, y0, x1, y1 = math.min(x0, c.X - r), math.min(y0, c.Y - r), math.max(x1, c.X + r), math.max(y1, c.Y + r)
		end
	end
	return x0, y0, x1, y1
end
local U = {math.huge, math.huge, -math.huge, -math.huge}
local conn = game:GetService("RunService").RenderStepped:Connect(function()
	local a, b, c, d = artBox()
	U = {math.min(U[1], a), math.min(U[2], b), math.max(U[3], c), math.max(U[4], d)}
end)
task.wait(13) conn:Disconnect()
local function rect(o) local p, s = o.AbsolutePosition, o.AbsoluteSize return {p.X, p.Y, p.X + s.X, p.Y + s.Y} end
local function hit(r) return U[1] < r[3] and r[1] < U[3] and U[2] < r[4] and r[2] < U[4] end
local out = {("envelope x %d..%d y %d..%d"):format(U[1], U[3], U[2], U[4])}
local vp = workspace.CurrentCamera.ViewportSize
table.insert(out, "on screen: " .. tostring(U[1] >= 0 and U[3] <= vp.X and U[2] >= -2))   -- y < 0 = under the top bar
table.insert(out, "above the column: " .. tostring(U[4] <= pg.PetsEggsUI.RightTiles.AbsolutePosition.Y))
if caption.Visible then table.insert(out, "clear of the caption: " .. tostring(U[4] <= caption.AbsolutePosition.Y + 2)) end
for name, o in {Column = pg.PetsEggsUI.RightTiles, Menu = pg.MainMenu.Menu, Pills = pg.SpeedUI.Holder,
	PerDay = pg.OfflineBaseUI.PerDay, WeatherRow = pg.WeatherTiles.Row} do
	table.insert(out, name .. " overlap: " .. tostring(hit(rect(o))))
end
for _, d in pg.TopbarStandard:GetDescendants() do
	if d.Name == "IconButton" and d:IsA("GuiObject") and d.AbsoluteSize.X > 0 then table.insert(out, "Topbar overlap: " .. tostring(hit(rect(d)))) end
end
return table.concat(out, "\n")
```

   Expected: on screen true, above the column true, clear of the caption true, and every overlap false.
   - The sunbursts count as circles of radius size/2; the other layers count as their half-diagonal (conservative).
3. **Visible / hidden states.** After each toggle wait 0.5 s and assert `Root.Visible`; then undo it and assert it is back after 0.6 s.

   | Toggle | Expected | Undo |
   |---|---|---|
   | `pg.MainMenu.OpenPage:Fire("Shop")` | hidden | `CloseWindow:Fire()` brings it back |
   | `pg.PetsEggsUI.OpenPanel:Fire("Potions")` | hidden (column away) | `OpenPage:Fire("Shop")` + `CloseWindow:Fire()` bring it back |
   | `player:SetAttribute("SlingLocalPhase", "Aiming")` (local) | hidden | nil brings it back |
   | `InHatchCinematic` = true | hidden | nil brings it back |
   | `IntroPlaying` = true | hidden | nil brings it back |
   | `TutorialExtra` = 3 (local) | hidden | 0 brings it back |
   | `pg.StarterPackUI.TestOpen:Fire()` | hidden | `pg.StarterPackUI.Enabled = false` brings it back |
   | `pg.OfflineUI.Enabled = true` | hidden | false brings it back |
   | `pg.SpeedOffer.Enabled = true` on PC | stays VISIBLE (no overlap on PC) | false |
4. **Content:**
   - `player:SetAttribute("StarterEgg", "StormEgg")` (server) swaps the Egg image and plays a pop.
   - `StarterDebug:Invoke("restricted", player, true)` turns the cash hero on and hides CashBack. `false` brings the egg back.
   - `pg.StarterPackUI:SetAttribute("Price", "45")` makes Amount "45".
   - `Amount.TextFits`, `Caption.TextFits` and `TextBounds.X <= AbsoluteSize.X` are all true.
5. **Owned:** Server `StarterDebug:Invoke("grant", player)`.
   - The art shrinks out for good and the Shop card goes.
   - `"reset"` brings the art back.
6. **Respawn:** set the Humanoid's Health to 0 (server). After respawn the art is still there and moving.
7. **Cost:** with the art hidden, the RenderStepped handler returns at once (active false). While shown, one handler writes about 30 properties per frame. Check MicroProfiler / no new warnings in get_console_output.
8. **Popup still fine:** TestOpen shows the same price as `Amount.Text`, and the v1 tile no longer exists:
   ```lua
   pg.PetsEggsUI.RightTiles:FindFirstChild("StarterPackTile") == nil
   ```
9. **Click:** ask the owner to click the art once. It must open the popup.
   - Don't drive Studio UI yourself.
   - A missed viewport click walks the character.

### 10.4 Screenshots

screen_capture; save them in `docs/plans/tests-2026-10-21/`.

| File | Shot |
|---|---|
| `starter_hud_v2_idle.jpg` | The owner's normal Studio size, idle. Compare with `starter_hud_v2_mock.jpg` |
| `starter_hud_v2_pop.jpg` | Mid-pop |
| `starter_hud_v2_rebirth.jpg` | The REBIRTH READY banner up (v1's bad shot) |
| `starter_hud_v2_restricted.jpg` | The restricted variant |
| `starter_hud_v2_hidden_window.jpg`, `starter_hud_v2_hidden_panel.jpg` | Hidden with a window / a side panel open |
| `starter_hud_v2_phone.jpg` | Phone emulator, 844x390 or the owner's device. **The owner switches the emulator**; we don't click Studio UI. Compact mode on and off the treadmill |

If screen_capture is down, use the offline preview recipe (memory: roblox-ui-offline-preview).

---

## 11. Risks

- **R1 Player list:** NOT disabled (CoreGui PlayerList on, leaderstats.Speed exists).
  - When a PC player opens it (Tab), CoreGui draws it over the top-right, covering the art.
  - None of our text is covered, but the art is hidden under it until they close the list.
  - A LocalScript can't detect it.
  - **Owner decision:** keep it as is, or disable the player list (it would lose the Speed column).
- **R2 Device-scale clamp at 1.18 (Check-UI rule):** on 1440p and larger the art (about 177 px Root, about 80 px egg) is smaller than the column's tiles (about 143 px). It reads a bit less "featured" there. It looks right from phones up to 1080p.
- **R3 Top-bar height on phones:** the layout assumes nothing. It measures the inset and keeps clear of the $/Day line. If a device's top bar differs from 58, verify it in the emulator.
- **R4 Compact mode drops the caption** on phones and on PC windows under about 500 px tall (where PetsEggsUI gives the column its 1.3 scale). That is intentional: 8-10 px text is worse than none.
- **R5 StarterRestricted starts true** (unknown) until PolicyService answers.
  - The 3 s first-show delay hides that.
  - If the policy is slower, the cash hero shows first and swaps to the egg with a pop.
- **R6 Same DisplayOrder (2) as PetsEggsUI:** their draw order is undefined, but they never overlap (6·k px gap, checked by the envelope test).
- **R7 The AreaTitle strip** (full-width, DisplayOrder 0) passes under the art for 1.9 s when entering an area. Its centred text is never touched.
- **R8 Owner testing in the same Studio:** the owner may stop or play in your Play session (it happened during this measurement). Re-check TestFreshSave before every Play.
- **R9 A new transparent bundle-art upload (group FBX carrier) is NOT proposed.**
  - The composition uses existing transparent icons, follows the player's next area live, and needs no upload.
  - Only if the owner still calls it "basic" after seeing it in game: a Blender/PIL-rendered bundle PNG via the group carrier is the next step.
- **R10 The product image 93658935949382 is not used.**
  - It is a square sunburst CARD with STARTER/PACK baked in and a fixed egg. That is a tile again.
  - Its in-game ImageLabel load stays untested (the session ended first; not needed).

---

## 12. Assets used (all already in the game)

| What | Id |
|---|---|
| Eggs | StreakConfig.EGG_ICONS (Wood 104751715957734, Tide 82378660960261, Storm 73957439433353, Magma 76929317115555, Void 94946523996428, Celestial 131707897219887) |
| Potions | PotionConfig.byKey: Money 88886704386081, Hatch 79394853866565, Speed 94938733066793 |
| Cash | 88694661500877 |
| White Robux | 132185731364109 |
| Sunburst | 130563114903838 |
| Star | 93906069548754 (the popup header's) |
| Product | ShopConfig.StarterPackProduct 3720595447 (fallback price 49) |
