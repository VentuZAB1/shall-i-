# HATCH NIGHT Gift window - implementation plan (2026-10-21)

> **For the builder (Opus):** follow this plan task by task. Every number here is final. If something in Studio
> contradicts a number, stop and write the conflict in the ledger
> (`docs/plans/2026-10-21-hatch-night-gift-window.progress.md`) before changing anything.
> Pipeline (owner rule): this plan -> Haiku plan reviewer -> build -> Haiku visual reviewer per screenshot set -> fixes -> Haiku lineup reviewer.

**Goal.** Rebuild the whole Gift window (DAILY tab, PLAYTIME tab and the window chrome while the Gift page is open) in style B, HATCH NIGHT. The owner picked it ("B HATCH looks cooler").

The owner's complaint is the acceptance test: "it looks so ugly overlooping and corners aren't even in the box". After this build, nothing overlaps and every corner and outline is inside its box. An automated containment test proves it.

**Sources (read before building):**
- Spec: `docs/specs/2026-10-21-slingshot-ui-style.md`. Read sections 2, 4 and 6.
- Mockups: `docs/plans/style-2026-10-21/`:
  - `B_hatchnight_pc.png`, `B_hatchnight_phone.png`, `B_hatchnight_sheet.png`;
  - `dirB_hatchnight.html` and `common.js` (the numbers below come from them).
- Evidence of the bug: `docs/plans/tests-2026-10-21/daily_rewards_owner_ugly.png`.
- Engineering rules kept:
  - the check-ui-clean-roblox skill (GothamBlack only, centre-anchored UIScale motion, ScaleType Fit icons, animations pause when hidden);
  - memory `roblox-ui-layout-rules.md` (one window at a time, toasts, respawn rule, phone rules).

**Out of scope:** StreakServer, StreakConfig, PlaytimeServer, PlaytimeConfig, ShopConfig, and every other window. Shop, Rebirth, Index and Settings must look exactly as today; Task 0 and Task 7 prove it.

---

## 0. Decisions (read first)

| # | Decision | Why |
|---|---|---|
| D1 | A new switch instead of a third `BrickUI.STYLE` value: `BrickUI.WINDOW_SKIN = "CheckUI"` plus `BrickUI.PAGE_SKIN = {Gift = "Hatch"}` and `BrickUI.skinFor(page)`. | 6 live scripts test `B.STYLE == "CheckUI"` (BrickUI, MenuController, TutorialClient, ShopClient, SellClient, UpgradeClient). `STYLE = "Hatch"` would flip all of them to the old Brick look. Phase 2 sets `WINDOW_SKIN = "Hatch"`, but each page's content also has to be rebuilt on the logical canvas then. |
| D2 | The helpers live in a new child ModuleScript `ReplicatedStorage.BrickUI.Hatch`. BrickUI loads it with `pcall`. | BrickUI's existing code stays byte-identical. If Hatch fails to load, every other window keeps working. |
| D3 | The window chrome is per page. MenuController builds `Window.HatchBack` (night shell, ZIndex 0) and `Window.HatchFront` (header band, ZIndex 2) once, and shows them only for Hatch pages. For Hatch pages it hides or saves these Check-UI pieces: Header, Close, Icon, Title, Depth, the Face fill and stroke, and the Body inset. Every other page gets the saved values back. | The other windows are untouched; Task 7's chrome snapshot diff proves it. |
| D4 | Everything is built in logical px. The window is 740 x 470 and the face is 740 x 463. Each layer has one UIScale (`SkinScale` on the chrome layers, `CanvasScale` on GiftPage), equal to the window px / 740. | Spec 6.1. Strokes, corners and text scale together. Never multiply by `deviceScale()` inside these layers. |
| D5 | The window size comes from a new fit rule (section 3): the spec formula, plus clearance from the left HUD, plus a right shift when needed. It replaces `fitScale` for Hatch pages only. | With the spec formula alone, the window would cover the left tiles and pills at 1050x620 and on phones. The PC 1080p result is unchanged: centred, 873 x 555. |
| D6 | The status line is deleted. Its messages move as in spec 2.4: `n/7` on the streak bar, the lime card, the countdown on the TOMORROW button, `LOST!` on the streak label, and a fly-text instead of the toast. | Spec 2.4. The client test now reads the card attribute `State` (section 8.2). |
| D7 | The bats are not built. | No uploaded bat art exists. An upload is the owner's call; see section 11. |
| D8 | The header teeth are spread evenly: 37 teeth, centres from x 16 to x 724. | The mockup loop stops 35 px short of the right edge. The spec text asks for 16 px from both edges. |
| D9 | The Day 7 chips are 74 and 120 px wide, not 98 + 98. | 98 + 98 leaves a 6 px gap, which breaks the 8 px rule. Late-game cash like `$7.25Qa` also needs more than 58 px. |
| D10 | Every card has a full-size `Hit` ImageButton on every device, not only on touch. | It is a superset of spec 2.3, and `press()` already ignores cards that are not claimable. |
| D11 | Inner rings (window rim, lime today ring, prism rim) use frames inset by the stroke width. `UIStroke.BorderStrokePosition` is not used. | That property exists in this Studio build (default Outer), but it is new. Inset frames match the mockup exactly. |
| D12 | The PLAYTIME tab puts a `PlayBar` on the right side of row 2: the warning `LEAVING RESETS!` plus a gold SKIP ALL button. The 12 slots (113 x 166) sit on the same two rows as the Daily cards. | The 6 x 2 grid fills the whole grid area, so the footer moves into row 2. `LEAVING RESETS PROGRESS!` (214 px) does not fit next to the button. |
| D13 | Card icons sit above the dim layer, and their brightness comes from `ImageColor3`. Icons were nudged up so none crosses the value line (y 89). | Locked cards keep the reward preview at 0.78 brightness (spec 2.4), which can't be done under a black overlay. |
| D14 | Text uses fixed `TextSize` from the mockup in boxes of `size + 2`. `H.fit()` steps the size down only to the minimum (16, or 15 for the "!" mark). Long error texts use short variants. | In-engine measurements below show every string fits. TextBounds.Y equals TextSize for GothamBlack. |

**In-engine GothamBlack widths** (`TextService:GetTextSize`, measured in Studio today; the + 5 in the room column is 2 x the 2.5 stroke):

| Text @ size | px | Box | Room after stroke |
|---|---|---|---|
| PLAYTIME REWARDS @26 | 253 | 400 | ok |
| PLAYTIME @18 (tab, inactive) | 84 | 120 | ok |
| STREAK @16 | 59 | 76 | ok |
| +12.5Qa SPEED @20 (worst value line) | 137 | 150 | 142 ok |
| PETS FULL! @18 | 93 | 142 | ok |
| 09:41:27 @17 | 63 | 94 | ok |
| THORNBLADE MANTIS @16 (longest secret pet) | 167 | 214 | ok |
| SECRET PET! @24 | 139 | 222 | ok |
| $7.25Qa @16 (chip) | 59 | 82 | ok |
| CLAIMED @16 (slot) | 69 | 97 | ok |
| LEAVING RESETS! @16 | 130 | 168 | ok |
| SKIP ALL @16 | 68 | 84 | ok |
| SECRET PET! @52 (celebration) | 296 | 600 | ok |

---

## 1. Files

| Instance | Action |
|---|---|
| `ReplicatedStorage.BrickUI` | Add 10 lines at the end (section 7.1). Nothing else changes. |
| `ReplicatedStorage.BrickUI.Hatch` | Create a ModuleScript with all the helpers (section 7.2). |
| `StarterGui.MainMenu.MenuController` | Add the skin hook (section 7.3). Change `mul()` to keep offsets. Nothing is deleted. |
| `StarterPlayer.StarterPlayerScripts.PlaytimeClient` | Rebuild the page part: the GiftPage canvas and the PLAYTIME tab (section 7.4). Tile badge logic unchanged. |
| `StarterPlayer.StarterPlayerScripts.StreakClient` | Rebuild the UI part: tabs, DAILY view, cards, Day 7, streak bar, motion, fly-text, celebration (section 7.5). Logic kept: `stateOf`, `press` (busy lock), the attributes, auto-open, `TestPress`, `applyTab` / `onShown`. |
| `ServerStorage.StreakTests` | Only `CLIENT_SRC` changes: it becomes the v2 client checks (section 8.2). `pure()` and `live()` stay byte-identical. |
| `ServerStorage._Backup_HatchNight.Before` | Backups (Task 1). |
| `docs/plans/tests-2026-10-21/` | Test files:<br>- `streak_client.lua` (v2; the old file is renamed `streak_client_v1.lua`);<br>- `hatch_pure.lua`, `hatch_containment.lua`, `hatch_assets.lua`, `hatch_chrome_snapshot.lua`;<br>- `hatch_chrome_before.txt` and `hatch_chrome_after*.txt` (snapshot outputs). |

---

## 2. Architecture

```
StarterGui.MainMenu (ScreenGui, ZIndexBehavior Sibling, CoreUISafeInsets, IgnoreGuiInset false)
  Window (Size/Position: Offset while a Hatch page is open; UIAspectRatioConstraint -> 740/470)
    HatchBack   Z0  [new, MenuController] night shell: Depth, Face{Rim, Sheen}      UIScale SkinScale = win.AbsoluteSize.X/740
    Depth       Z1  Check-UI depth   (Visible=false on Hatch pages)
    Face        Z1  Check-UI face    (Hatch: BackgroundTransparency 1, UIStroke disabled, Size (1, 463/470))
      Header, Close, Icon, Title     (Hatch: Visible=false)
      Body                           (Hatch: Size (1,1), Pos (0.5,0.5), BackgroundTransparency 1, UIStroke disabled)
        GiftPage  [PlaytimeClient] Offset canvas 740 x 463 at (0,0), AnchorPoint (0,0), UIScale CanvasScale = Body.AbsoluteSize.X/740
          Tabs          [StreakClient]   recess + pill + labels + dots + hits
          DailyView     [StreakClient]   Streak bar, Card1..Card7, Fx
          PlaytimeView  [PlaytimeClient] PlayBar, Slot1..Slot12, Fx
    HatchFront  Z2  [new, MenuController] Crack teeth, Band, BandFill, Gloss, Icon, Title, Close, CloseHit   UIScale SkinScale
PlayerGui.StreakCelebrate (DisplayOrder 45)  Day 7 hatch celebration  [StreakClient, rebuilt]
PlayerGui.StreakFly       (DisplayOrder 46)  claim fly-text           [StreakClient, new]
```

**Rendering and input rules (ZIndexBehavior Sibling).**
- Siblings draw in ZIndex order, and each sibling's whole subtree draws before the next sibling.
- HatchFront covers the whole window, but it holds only non-Active Frames except `CloseHit`, so clicks pass through to the GiftPage buttons.
- Every Frame, TextLabel and ImageLabel built here keeps `Active = false`. Only GuiButtons receive input.
- Section 8.3 check 4 verifies this with `GetGuiObjectsAtPosition`.

---

## 3. Window fit (Hatch pages)

The pure function goes in `H.fitWindow` (section 7.2). MenuController feeds it measured values.

- `guiW, guiH` = `MainMenu.AbsoluteSize`. That is the safe area minus the top bar, because MainMenu uses CoreUISafeInsets with IgnoreGuiInset false.
- `leftClear` = the largest right edge (relative to `MainMenu.AbsolutePosition.X`) of the left HUD, plus 6. Two pieces count:
  - `MainMenu.Menu` (the four left tiles; its AbsoluteSize includes the phone UIScale of 1.3);
  - `PlayerGui.SpeedUI.Holder` (the Speed and Money pills; bottom-left on PC, top-left on touch phones).

```
left  = max(8, leftClear);  right = guiW - 8
s     = clamp(min(1.18, (right - left) / 740, (guiH - 12) / 470), 0.5, 1.18)
w, h  = 740 s, 470 s
cx    = clamp(guiW / 2, left + w/2, max(left + w/2, right - w/2));   cy = guiH / 2
Window.Size = UDim2.fromOffset(w, h); Window.Position = UDim2.fromOffset(cx, cy)   (AnchorPoint stays 0.5, 0.5)
```

| Device (screen) | gui | Tiles right edge | Pills right edge | leftClear | s | Window | cx, cy | Min text |
|---|---|---|---|---|---|---|---|---|
| PC 1920x1080 | 1920x1022 | 252.8 | 406.1 | 412.1 | **1.18** | 873.2 x 554.6 | 960, 511 (centred) | 18.9 px |
| PC baseline 1050x620 | 1050x562 | 139.0 | 223.3 | 229.3 | **1.0982** | 812.7 x 516.2 | 635.65, 281 | 17.6 px |
| Phone 844x390 (notch 56 per side, top bar 44) | 732x346 | 110.2 (x1.3) | 138.3 | 144.3 | **0.7106** | 525.9 x 334.0 | 407.24, 173 | 11.4 pt |
| Phone 667x375 (no notch, top bar 44) | 667x331 | 105.1 (x1.3) | 131.9 | 137.9 | **0.6787** | 502.3 x 319.0 | 389.03, 165.5 | 10.9 pt |

**How the HUD edges are computed** (they are the expected values in `hatch_pure.lua`):
- Tiles: `0.0094 guiW + 0.2297 guiH`, times 1.3 on phones for the second term. This comes from Menu Size (0.1292, 0.2426), AR 0.9466, height-dominant.
- Pills: `0.0094 guiW + 0.3797 guiH`. This comes from Holder Size (0.2135, 0.2093), AR 1.814.

**Other rules.**
- The window is always at least 6 px from the gui edges vertically and 8 px horizontally. Its 3.5 px outline (x s, at most 4.13 px) stays on screen.
- Recompute and apply on `workspace.CurrentCamera.ViewportSize` changes while a Hatch page is open.
- **Studio test switch:** the MainMenu ScreenGui attribute `HatchTestScale` (number). Honoured only when `RunService:IsStudio()`. It forces `s` and centres the window. It is used to render phone-scale and 1050x620-scale windows on the Studio viewport. Remove the attribute after tests.

---

## 4. Geometry (logical px; the mockup numbers)

### 4.0 Conventions

- **`rect (x, y, w, h)`** is a top-left box in the parent's logical space. Frames use AnchorPoint (0, 0) and `UDim2.fromOffset`.
  - The exceptions are centre-anchored with AnchorPoint (0.5, 0.5), and their Position is the centre:
    - gloss buttons (the helper converts the rect);
    - pips;
    - rotated teeth and stickers;
    - the celebration pieces.
- **`text(s, x, y, w, size)`** = the mockup `txt()` box:
  - TextLabel at (x, y), Size (w, size + 2), TextSize = size;
  - centred X and Y, GothamBlack, `TextScaled = false`;
  - UIStroke Contextual, ink, 2.5 unless stated.
  - The "+3 ink copy" titles use a second label 3 px lower: ink fill, the same stroke, a lower ZIndex.
- **Stroke** = UIStroke, ApplyStrokeMode Border, colour **ink (13,11,28)**, Thickness in logical px (UIScale scales it). It draws outside the box.
- **Corners**: `UDim.new(0, px)`; "round" = `UDim.new(0.5, 0)`.
- **Gradients**: UIGradient Rotation 90 (top -> bottom) on a white background, unless stated.
- **Sticker** = an ImageLabel (ScaleType Fit) plus a `<Name>Shadow` sibling at +3 y: ImageColor3 (6,4,20), ImageTransparency 0.45, ZIndex one lower. The shadow follows Image, Rotation and Visible.
- **Glow** = ImageLabel `rbxassetid://121438949090215` (soft disc: solid to 50% of the radius, then fading), ScaleType Stretch, tinted with ImageColor3.
- **Test attributes** (set by the helpers or the builder; read by section 8.3):
  - `HatchPad` / `HatchPadBottom`: minimum logical gap to the parent's edges;
  - `HatchTile` + `HatchGap`: a group of siblings that must not overlap;
  - `HatchHit`: an invisible hit box;
  - `HatchRadial`: rotating radial art, checked by its unrotated box;
  - `HatchShell`: the window shell, checked against the ScreenGui.

**Palette** (`H` constants):

| Key | Values |
|---|---|
| INK | (13,11,28) |
| Canvas | top (46,37,102), bottom (27,22,66), side (15,11,40), rim (97,83,194) |
| Card | top (58,48,130), bottom (41,33,95), side (21,16,50), highlight (112,98,216) |
| Card today | top (76,63,170), bottom (48,38,122) |
| Recess | top (18,14,48), bottom (28,23,70), line (140,125,255) |
| Hero face | solid (31,24,82) |
| Text | LAV (210,202,255), LAV_DIM (167,159,224), LIME_TXT (184,255,106), GOLD_TXT (255,210,58), RED_TXT (255,110,120), WHITE |

| Button palette | top | bottom | side | top highlight | label colour |
|---|---|---|---|---|---|
| lime | (180,255,74) | (79,203,16) | (42,118,8) | (232,255,180) | white |
| red | (255,90,110) | (224,26,52) | (122,8,22) | (255,184,194) | white |
| silver | (222,218,244) | (159,152,200) | (87,81,132) | (255,255,255) | white |
| off | (70,62,136) | (53,45,108) | (27,22,64) | (106,96,184) | LAV_DIM (Day 7: GOLD_TXT) |
| gold | (255,224,112) | (245,154,0) | (142,86,0) | (255,243,176) | white |
| dusk | (58,50,128) | (44,37,96) | (22,18,54) | (106,96,184) | LIME_TXT (timer) |

| Band theme | Band gradient keys | BandFill keys | Tooth colour |
|---|---|---|---|
| Pumpkin | 0 (255,180,60), 0.55 (255,138,28), 1 (242,98,10) | 0 (255,142,31), 0.1 (255,138,28), 1 (242,98,10) | (242,98,10) |
| HatchGold | 0 (255,216,74), 1 (255,168,0) | 0 (255,192,37), 1 (255,168,0) | (255,168,0) |

- **Theme pick:** `H.bandTheme()` = `workspace:GetAttribute("HatchBand")` if it is set; otherwise "Pumpkin" while `workspace.HalloweenDecor` exists (a Folder; it exists today); otherwise "HatchGold". It is evaluated on every open.
- **Glow colours:**

| Key | Colour |
|---|---|
| cash | (108,255,90) |
| speed | (85,200,255) |
| gold | (255,225,90) |
| potions | (199,139,255) |
| blue | (127,160,255) |
| pet | (255,214,90) |
| Day 4 egg | `AREA_COLOR[StreakArea]` (Grass (120,240,90), Water (80,195,255), Thunder (250,240,90), Fire (255,140,50), Shadow (190,110,255), Celestial (255,205,95)) |

- **RAINBOW** = the Check-UI rainbow ColorSequence already in StreakClient (moves to `H.RAINBOW`).

### 4.1 HatchBack (Window child, ZIndex 0)

Frame "HatchBack": AnchorPoint (0.5, 0.5), Position (0.5,0,0.5,0), Size (0,740,0,470), transparent, Visible false. It holds UIScale `SkinScale` = `win.AbsoluteSize.X / 740`, re-bound on every AbsoluteSize change.

| Name | Class | rect | Z | Look |
|---|---|---|---|---|
| Depth | Frame | 0, 7, 740, 463 | 1 | Canvas side, corner 18, stroke 3.5. `HatchShell` |
| Face | Frame | 0, 0, 740, 463 | 2 | Canvas gradient top -> bottom, corner 18, stroke 3.5. `HatchShell` |
| Face.Rim | Frame | 1.5, 1.5, 737, 460 | 1 | Transparent, corner 16.5, stroke 1.5 rim colour with Transparency 0.45 (the stroke fills face px 0-1.5). |
| Face.Sheen | ImageLabel | 0, 46, 420, 220 | 2 | Glow, ImageColor3 (140,120,255), ImageTransparency 0.8 |

### 4.2 HatchFront (Window child, ZIndex 2)

The same frame recipe as HatchBack, named "HatchFront", with its own `SkinScale`. Children:

| Name | Class | rect / centre | Z | Look |
|---|---|---|---|---|
| Crack | Frame | 0, 0, 740, 470 | 1 | Transparent container for the teeth. |
| Crack.Ink1..37 | Frame | centre (cx_i, 46), size s_i + 5 | 1 | INK, Rotation 45 |
| Crack.Tooth1..37 | Frame | centre (cx_i, 46), size s_i | 2 | Theme tooth colour, Rotation 45 |
| Band | Frame | 0, 0, 740, 46 | 2 | White plus the theme band gradient, corner 18 |
| BandFill | Frame | 0, 23, 740, 23 | 3 | White plus the theme fill gradient, no corner (hides the band's lower rounded corners). |
| Gloss | Frame | 0, 0, 740, 20 | 4 | White, corner 18, UIGradient 90 transparency 0.72 -> 1 |
| Icon (+IconShadow) | sticker | 12, 4, 38 | 6 / 5 | `panel.Icon.Image` (gift 128336310005291) |
| TitleShadow | text | ("", 58, 13, 400, 26), left aligned | 5 | INK fill, stroke 3 |
| Title | text | ("", 58, 10, 400, 26), left aligned | 7 | White, stroke 3. Text = `panel.Title.Text:upper()` |
| Close | glossButton red | rect 694, 6, 34, 34; d 4, r 9, ol 2 | 8 | Label "X" text (0, 4, 34, 21). The face is a Frame, driven by CloseHit. `HatchPad 6` |
| CloseHit | ImageButton | 688, 0, 46, 46 | 9 | Fully transparent. `HatchHit`. Activated -> closeWindow |

- **Teeth:** `cx_i = 16 + (i-1) * 708/36` and `s_i = 11 + (((i-1)*7 + 3) % 5) * 1.6`, for i = 1..37.
- **Extents:** left 1.3, right 735.3, lowest point y 61.8 (the tabs start at y 66).

### 4.3 GiftPage and Tabs

**GiftPage** (built by PlaytimeClient): Frame, Position (0,0,0,0), AnchorPoint (0,0), Size (0,740,0,463), transparent, ZIndex 3, Visible false. It holds UIScale `CanvasScale` = `Body.AbsoluteSize.X / 740`, re-bound on change. GiftPage attributes:
- `Tab` ("Daily" / "Playtime"; the one switch, unchanged);
- `PlaytimeReady` (bool; set by PlaytimeClient);
- `HatchTestPulse` (Studio test: forces the CLAIM button scale).

**Tabs** (StreakClient): a recess at rect (10, 66, 308, 38), ZIndex 5, `HatchPad 8`, `HatchTile "row2"`, `HatchGap 8`.

| Name | Class | rect / centre | Z | Look |
|---|---|---|---|---|
| (self) | Frame | 10, 66, 308, 38 | 5 | Corner 19, stroke 2, recess gradient |
| TopShade | Frame | 19, 0, 270, 3 | 1 | Black, BackgroundTransparency 0.6 |
| BottomLine | Frame | 19, 36.5, 270, 1.5 | 1 | Recess line, BackgroundTransparency 0.65 |
| LabelDaily | text | ("DAILY", 8, 10, 115, 18) | 2 | LAV_DIM. Visible when Tab = Playtime. UIScale `HoverScale` |
| LabelPlaytime | text | ("PLAYTIME", 152, 10, 120, 18) | 2 | LAV_DIM. Visible when Tab = Daily. UIScale `HoverScale` |
| Pill | glossButton lime | slot A rect 3, 3, 148, 32 (centre 77, 19); slot B rect 157, 3, 148, 32 (centre 231, 19); d 3, r 15, ol 2 | 3 | Label text (0, 5, 148, 18) "DAILY" / "PLAYTIME". Face is a Frame. `HatchPad 3`, `HatchPadBottom 3` |
| DotDaily | dot | 127, 9, 20, 20 | 5 | Visible = `StreakClaimable` and Tab = Playtime |
| DotPlaytime | dot | 278, 9, 20, 20 | 5 | Visible = `GiftPage.PlaytimeReady` and Tab = Daily |
| HitDaily | TextButton | 0, -4, 154, 46 | 6 | Transparent, Text "". `HatchHit`. Activated -> `Tab = "Daily"` |
| HitPlaytime | TextButton | 154, -4, 154, 46 | 6 | Same; `Tab = "Playtime"` |

- **dot** = Frame 20x20, corner round, gradient (255,106,116) -> (224,16,42), stroke 2. Mark = text ("!", 0, 1.5, 20, 15) with stroke 1.5 and HatchMin 15.
- **Tab switch:** tween the Pill holder Position to the slot centre (0.15 s, Quad Out) and set its label. Hover on a Hit scales the hovered slot's visible label (the pill holder's ButtonScale, or the inactive label's HoverScale) to 1.04 (Quad Out, 0.08 s). Press on the active slot sinks the pill face (glossButton motion fed by `opts.input = hit`).

### 4.4 DailyView: streak bar

**DailyView**: Frame (0, 0, 740, 463), transparent, ZIndex 3. Children: `Streak`, `Card1..7` (ZIndex 2), and `Fx` (Frame 0, 0, 740, 463, transparent, ZIndex 10, for confetti).

**Streak** = a recess at rect (330, 66, 400, 38), ZIndex 2, `HatchPad 8`, `HatchTile "row2"`, `HatchGap 8`.

| Name | Class | rect / centre | Z | Look |
|---|---|---|---|---|
| TopShade, BottomLine | Frame | 19, 0, 362, 3 / 19, 36.5, 362, 1.5 | 1 | As in Tabs |
| Label | text | ("STREAK", 14, 11, 76, 16) | 4 | LAV, stroke 2. Shows "LOST!" in RED_TXT for 4 s (section 5.6). |
| Link1..6 | Frame | 120 + (i-1)*34, 18, 20, 3 | 1 | Corner 2. Lit (142,240,58), else (11,8,32) |
| TodayGlow | ImageLabel | centre = the today pip's centre, size 30 x 34 | 2 | Glow (255,214,40). ImageTransparency = 0.45 + 0.15 sin(2 pi t / 0.9). Hidden when nothing is claimable. |
| Pip1..7 | eggPip | centre (113 + (i-1)*34, 18.5), size 18 x 23 | 3 | Section 7.2 `eggPip`; attribute `State` |
| Count | text | ("1/7", 340, 10, 48, 18) | 4 | White |

**Pip states:**
- `done` = the gradient (230,255,176) -> 0.35 (142,240,58) -> (62,154,14), plus the white crack.
- `today` = (255,248,200) -> 0.35 (255,210,28) -> (224,138,0).
- `lock` = (78,70,144) -> 0.35 (45,39,99) -> (28,23,63), with no spec dot.
- `hero` = H.RAINBOW at Rotation 45. `herotoday` = hero plus the TodayGlow. `herodone` = hero plus the crack.

**Each pip** has a 2 px stroke and corner round. Its children:
- `Spec` (4, 4, 5, 4): white, BackgroundTransparency 0.35, round.
- `Crack`: a container (0, 0, 18, 23) holding 5 white segments, each 1.6 thick, centre-anchored. Columns are (cx, cy, length, rotation); the length includes +1.2 to close the joints:
  1. (2.5, 10.5, 4.81, -33.69)
  2. (5.5, 11.5, 6.2, 53.13)
  3. (8.5, 11.5, 6.2, -53.13)
  4. (11.5, 11.5, 6.2, 53.13)
  5. (15, 12, 6.2, -36.87)
- UIScale `PopScale`.

**Derivation** (every update):
- `claimable = StreakClaimable == true`, `nxt = StreakNext or 1`, `through = StreakThrough or 0`, `today = claimable and nxt or 0`.
- Pip i < 7: `done` if i <= through, `today` if i == today, else `lock`.
- Pip 7: `herodone` if through >= 7, `herotoday` if today == 7, else `hero`.
- Link i is lit if `i < (today > 0 and today or through + 1)`.
- Count = `(claimable and nxt or through) .. "/7"`.

### 4.5 Small day cards (Days 1-6)

**Positions:**

| Day | rect |
|---|---|
| 1 | 10, 112 |
| 2 | 176, 112 |
| 3 | 342, 112 |
| 4 | 10, 286 |
| 5 | 176, 286 |
| 6 | 342, 286 |

Every card is 158 x 166 (face 158 x 161), built with `H.shellCard`: `HatchPad 8`, `HatchTile "grid"`, `HatchGap 8`. The 8 px gaps and the bottom margin of 11 match spec 2.2.

| Name (in holder `Card<d>`) | Class | rect | Z | Look / rule |
|---|---|---|---|---|
| Hit | ImageButton | 0, 0, 158, 166 | 1 | Transparent, `HatchHit`. Activated -> press(d) |
| Side | Frame | 0, 5, 158, 161 | 2 | Card side, corner 14, stroke 2.5 |
| Face | Frame | 0, 0, 158, 161 | 3 | Card gradient (CLAIM: today gradient), corner 14, stroke 2.5, ClipsDescendants true |
| Face.TopHL | Frame | 9.1, 1, 139.8, 1.5 | 1 | Card highlight |
| Face.Glow | ImageLabel | 31, 12, 96, 88 | 1 | Glow, the day's colour, ImageTransparency 0.45 |
| Face.DayPill | pill | 45, 6, 68, 20 | 2 | Label text ("DAY n", 0, 1, 68, 16) with stroke 2. `HatchPad 6` |
| Face.Value | text | (line1, 4, 89, 150, 20) | 3 | White |
| Face.Sub | text | (line2, 4, 111, 150, 16) | 3 | LAV |
| Face.Button | glossButton | rect 8, 130, 142, 27; d 3, r 9, ol 2.5 | 4 | Label named **`State`**: text (0, 2, 142, 18). Clock ImageLabel (20, 3, 18, 18), hidden unless TOMORROW. `Flash` Frame (0, 0, 142, 24): white, BackgroundTransparency 1, corner 9, Z 5. `HatchPad 8`, `HatchPadBottom 3` |
| Dim | Frame | 0, 0, 158, 166 | 4 | Black, corner 14. BackgroundTransparency = brightness (table 5.1) |
| HoverFx | Frame | 0, 0, 158, 161 | 5 | White, BackgroundTransparency 1 -> 0.94 on hover, corner 14 |
| Icons | Frame | 0, 0, 158, 161 | 6 | ClipsDescendants true. Child `Pop` (AnchorPoint 0.5, centre (79, 80.5), size 158 x 161, UIScale `PopScale`) holds the icon stickers (section 4.6). |
| Badges | Frame | 0, 0, 158, 166 | 7 | |
| Badges.Ring | Frame | 3, 3, 152, 155 | 1 | Transparent, corner 11, stroke 3 (180,255,74) |
| Badges.RingGlow | Frame | 6, 6, 146, 149 | 1 | Transparent, corner 8, stroke 3 (150,255,60) with Transparency 0.6 |
| Badges.Check (+Shadow) | sticker | 50, 27, 58; Rotation -8 | 3 / 2 | Check 78526516923039, UIScale `Stamp`. Rotated box 46.3..111.7 x 23.3..88.7, inside |
| Badges.Lock (+Shadow) | sticker | 127, 6, 22 | 3 / 2 | Lock 124356037818343 |
| TestPress | BindableEvent | | | Studio only, unchanged: `.Event` -> press(d) |

- **pill** = Frame with corner 10. Dark: BackgroundColor3 (10,8,28), BackgroundTransparency 0.45, plus `PillHL` (8, 1, w-16, 1) white with BackgroundTransparency 0.88. Lime (`setToday(true)`): white plus the lime gradient (180,255,74) -> (79,203,16), stroke 2, PillHL hidden.
- **Button label boxes per state** (use `H.place`):
  - TOMORROW: `State` at (44, 2, 94, 17), left aligned, LIME_TXT. Clock visible.
  - Every other state: (0, 2, 142, 18), centred.

### 4.6 Day icons (in `Card<d>.Icons.Pop`, face coordinates; the spec mockup formula, nudged so every bottom <= 89.5)

| Day | Stickers in draw order: key (x, y, size) | Count text |
|---|---|---|
| 1 | cash (45, 21, 68); Money (91.8, 51, 38) | text ("x1", 109.8, 67, 26, 16) |
| 2 | Hatch (31.3, 32.5, 53); Speed (73.7, 32.5, 53); shoe (61, 53.5, 36) | |
| 3 | cash (45, 21, 68); Money (91.8, 51, 38) | text ("x2", 109.8, 67, 26, 16) |
| 4 | egg (46, 23, 66) | |
| 5 | Money (24.7, 39.5, 45); Hatch (88.3, 39.5, 45); Speed (54.5, 31.5, 49) | |
| 6 | cash (37.5, 23, 66); shoe (89.8, 47.5, 42) | |

**Image keys:**

| Key | Image |
|---|---|
| cash | 131724750673548 |
| shoe | 80829076123513 |
| Money / Hatch / Speed | `PotionConfig.byKey[key].icon` |
| egg | `StreakConfig.EGG_ICONS[StreakEgg]`, fallback 135711525932647 |

**Glow per day:**

| Day | Glow |
|---|---|
| 1 | cash |
| 2 | speed |
| 3 | gold |
| 4 | the area colour |
| 5 | potions |
| 6 | blue |

**Copy** (`lineTexts`, live numbers; fit with variants):

| Day | Value (20) | Sub (16) |
|---|---|---|
| 1 | `money(cashOf(15))` | `+1 POTION` |
| 2 | `"+" .. Format(speedOf(0.2)) .. " SPEED"` | `+2 POTIONS` |
| 3 | `money(cashOf(30))` | `+2 POTIONS` |
| 4 | `BIG EGG` | `Format(EGG_KG[area]) .. " KG"` |
| 5 | `3x ALL` | `POTIONS` |
| 6 | `money(cashOf(60))` | `"+" .. Format(speedOf(0.5)) .. " SPEED"` |

### 4.7 Day 7 hero card

Holder `Card7` at rect (508, 112, 222, 340): face 222 x 335, `shellCard` with `opts.solid = (31,24,82)` (no gradient; `setToday` is a no-op). `HatchPad 8`, `HatchTile "grid"`, `HatchGap 8`. Hit is (0, 0, 222, 340).

**Face children** (Z in this order):

| Name | Class | rect | Z | Look |
|---|---|---|---|---|
| BgGlow | ImageLabel | 0, 0, 222, 290 | 1 | Glow (107,76,230), ImageTransparency 0.1 |
| Rays | ImageLabel | 8, 30, 206, 206 | 2 | Rays 76624006953375, ScaleType Fit, ImageColor3 (255,196,70), ImageTransparency 0.55. Rotates 12 deg/s. `HatchRadial` |
| Halo | ImageLabel | 46, 56, 130, 160 | 3 | Glow (255,236,160), ImageTransparency 0.45 |
| DayPill | pill | 10, 8, 68, 20 | 4 | "DAY 7"; lime when Day 7 is CLAIM. `HatchPad 6` |
| Tag | Frame | 124, 7, 88, 22 | 4 | Corner 8, gradient (255,90,110) -> (217,20,46), stroke 2. TopHL (6, 1, 76, 1.5) (255,184,194). Label text ("SECRET!", 0, 2, 88, 16). `HatchPad 6` |
| TitleShadow | text | ("SECRET PET!", 0, 37, 222, 24) | 5 | INK fill, stroke 3 |
| Title | text | ("SECRET PET!", 0, 34, 222, 24) | 6 | White, UIGradient 90: 0 (255,248,196), 0.45 (255,224,74), 1 (255,174,0). Stroke 3 |
| Pet (+PetShadow) | sticker | 37, 58, 148 | 8 / 7 | `IndexConfig.PORTRAITS[StreakPet]` |
| Shell | Frame | 59, 158, 104, 60 | 9 | Transparent container |
| Shell.Ink1..4 / Tooth1..4 | Frame | centre (cx, 17); sizes s + 5 / s; Rotation 45 | 1 / 2 | INK / (255,230,128). Teeth (cx, s): (18, 15.2), (39.06, 18.4), (64.56, 13.6), (83.41, 16.8) |
| Shell.Clip | Frame | 0, 17, 104, 43 | 3 | ClipsDescendants true |
| Shell.Clip.Bowl | Frame | 4, -40, 96, 80 | 1 | Corner round, stroke 2.5, gradient 0 (255,230,128), 0.5 (255,230,128), 0.8 (255,176,0), 1 (216,138,0) |
| Shell.Clip.Spec | Frame | 18, 8, 14, 7 | 2 | White, BackgroundTransparency 0.3, round |
| Name | text | (pet display upper, 4, 220, 214, 16) | 10 | White, HatchMin 15 |
| Kg | text | (`Format(SECRET_KG[area]) .. " KG"`, 4, 240, 214, 16) | 10 | GOLD_TXT |
| Chip1 | chip | 10, 264, 74, 30 | 10 | Potions Money (4, 4, 22), Hatch (12, 4, 22), Speed (20, 4, 22) (plain ImageLabels, Z 1/2/3). Count text ("x5", 44, 6, 26, 16). `HatchPad 8`, `HatchTile "chips"`, `HatchGap 8` |
| Chip2 | chip | 92, 264, 120, 30 | 10 | Cash (5, 3, 24, 24). Value text (`money(cashOf(120))`, 32, 6, 82, 16). Same attributes |
| Button | glossButton | rect 10, 300, 202, 29; d 3, r 10, ol 2.5 | 11 | `State` text (0, 3, 202, 18). LockIcon (40, 4, 19, 19), hidden. Clock (50, 4, 18, 18), hidden. Flash. `HatchPad 8`, `HatchPadBottom 3` |
| Shine | Frame | 0, 0, 222, 335 | 12 | White, corner 14. UIGradient Rotation 20, Transparency (0 1, 0.42 1, 0.5 0.55, 0.58 1, 1 1), Offset -1 -> 1 in 0.8 s every 3 s |
| PrismRim | Frame | 4, 4, 214, 327 | 13 | Transparent, corner 10, stroke 4 white with a UIGradient (H.RAINBOW) child. Gradient Rotation += 30 deg/s |

- **chip** = Frame with corner 15, BackgroundColor3 (8,6,24), BackgroundTransparency 0.4, stroke 2, plus TopHL (10, 1, w-20, 1.5) white with BackgroundTransparency 0.86.
- **Hero Badges:** Ring (7, 7, 208, 321), corner 10, stroke 3 lime (no RingGlow). Check sticker (82, 100, 58), Rotation -8. No Lock sticker.
- **Hero button states:**

| State | Palette | State label | Icon |
|---|---|---|---|
| CLAIM | lime | "CLAIM!" | |
| CLAIMED (week not done) | silver | "CLAIMED" | |
| CLAIMED with week done (`through >= 7 and not claimable`) | dusk | timer `clock(secondsToNext)`; label box (72, 3, 100, 17), left aligned, LIME_TXT | Clock |
| TOMORROW | dusk | timer, same box | Clock |
| LOCKED | off | `"IN " .. n .. (n == 1 and " DAY" or " DAYS")` with `n = 7 - (claimable and nxt or through)`; label box (34, 3, 168, 18), GOLD_TXT | LockIcon |

### 4.8 PlaytimeView (PLAYTIME tab)

**PlaytimeView**: Frame (0, 0, 740, 463), transparent, ZIndex 3. Children: `PlayBar`, `Slot1..12`, `Fx` (same as DailyView).

**PlayBar** = a recess at rect (330, 66, 400, 38): `HatchPad 8`, `HatchTile "row2"`, `HatchGap 8`. TopShade and BottomLine as in Streak.

| Name | Class | rect | Look |
|---|---|---|---|
| Warning | text | ("LEAVING RESETS!", 14, 11, 168, 16), left aligned | RED_TXT |
| SkipAll | glossButton gold | rect 190, 3, 207, 32; d 3, r 15, ol 2 | Face is an ImageButton. `HatchPad 3`, `HatchPadBottom 3`. Hidden when all slots are done (as today). |
| SkipAll.Face.SkipLabel | text | ("SKIP ALL", 12, 5, 84, 16) | White |
| SkipAll.Face.Robux | ImageLabel | 102, 4.5, 20, 20 | 132185731364109, Fit |
| SkipAll.Face.Price | text | (price, 126, 5, 70, 16), left aligned | White. Price = `skipPrice()` (unchanged logic; Studio "48", live price, or "SOON") |

**Skip error flash** (1.3 s):
- SkipLabel moves to (12, 5, 183, 16) with `H.fit(label, {msg:upper(), "TRY AGAIN"})`; Robux and Price are hidden.
- Then everything is restored.

**Slots:** holder `Slot<i>`, 113 x 166 (face 113 x 161), `shellCard` with `HatchPad 8`, `HatchTile "grid"`, `HatchGap 8`.
- Column c = (i-1) % 6, row r = floor((i-1) / 6).
- x = 10 + c * 121.4, so the columns sit at x 10, 131.4, 252.8, 374.2, 495.6, 617.
- y = 112 + r * 174, so the rows sit at y 112 and 286.

| Name | Class | rect | Look |
|---|---|---|---|
| Hit | ImageButton | 0, 0, 113, 166 | `HatchHit`. Activated -> claim(i) |
| Face.TopHL | Frame | 9.1, 1, 94.8, 1.5 | |
| Face.Glow | ImageLabel | 8.5, 12, 96, 88 | Glow: cash / speed / `potion.color` / pet, ImageTransparency 0.45 |
| Face.TimePill | pill | 16.5, 6, 80, 20 | Text: `< 60` -> "n MIN", 60 -> "1 HR", 90 -> "90 MIN", 120 -> "2 HRS". Lime when ready. `HatchPad 6` |
| Face.Value | text | (…, 4, 89, 105, 20) | cash `"$" .. Format(amount)` (125,255,105); speed `"+" .. Format(amount)` (110,215,255); potion `key:upper()` in `potion.color`; pet `Format(PET_KG) .. " KG"` in GOLD_TXT |
| Face.Sub | text | (…, 4, 111, 105, 16) | LAV: "CASH" / "SPEED" / "POTION" / "PET" |
| Face.Button | glossButton | rect 8, 131, 97, 26; d 3, r 8, ol 2.5 | `State` text (0, 3, 97, 16). Flash. `HatchPad 8`, `HatchPadBottom 3` |
| Icons.Pop.Icon (+Shadow) | sticker | 24.5, 24, 64 (pet: 23.5, 22, 66) | cash / shoe / potion icon / pet portrait (`IndexConfig.PORTRAITS[PlaytimePet]`) |
| Badges.Ring | Frame | 3, 3, 107, 155 | Corner 11, stroke 3 lime |
| Badges.RingGlow | Frame | 6, 6, 101, 149 | Corner 8, stroke 3 (150,255,60) with Transparency 0.6 |
| Badges.Check (+Shadow) | sticker | 34.5, 30, 44; Rotation -8 | |

**Slot states:**

| State | Card | Button |
|---|---|---|
| WAIT | brightness 0.85, icon tint 217 | dusk, timer `fmt(left)` in LIME_TXT, centred |
| CLAIM | today face, lime TimePill, Ring + RingGlow, brightness 1 | lime "CLAIM!", pulsing |
| CLAIMED | brightness 0.6, tint 153, Check | silver, `H.fit(label, {"CLAIMED", "DONE"})` |

### 4.9 StreakCelebrate (Day 7, rebuilt in HATCH NIGHT)

ScreenGui `StreakCelebrate`: DisplayOrder 45, IgnoreGuiInset true, ResetOnSpawn false, ZIndexBehavior Sibling, Enabled false, default insets (as today).

| Name | Class | rect (logical; Box 640 x 500) | Z | Look |
|---|---|---|---|---|
| Backdrop | TextButton | full screen (Scale 1, 1) | 1 | (8,6,25), BackgroundTransparency 0.2. Activated -> close |
| Box | Frame | AnchorPoint 0.5, Position (0.5, 0.5), Size (0,640,0,500) | 2 | Transparent. UIScale `WindowScale` = `min(1.18, (cel.AbsoluteSize.X-16)/640, (cel.AbsoluteSize.Y-12)/500)` |
| Box.Pop | Frame | AnchorPoint 0.5, centre (320, 250), 640 x 500 | 1 | UIScale `PopScale` |
| Pop.Rays | ImageLabel | 150, 10, 340, 340 | 1 | Rays, ImageColor3 (255,196,70), ImageTransparency 0.3, 12 deg/s |
| Pop.Halo | ImageLabel | 205, 40, 230, 280 | 2 | Glow (255,236,160), ImageTransparency 0.35 |
| Pop.PetRoot | Frame | AnchorPoint 0.5, final centre (320, 170), 220 x 220 | 3 | UIScale `PetScale`. Children Shadow (0, 3, 220, 220) and Image (0, 0, 220, 220) |
| Pop.Egg | Frame | 235, 150, 170, 200 | 4 | Children below |
| Egg.Ink1..7 / Tooth1..7 | Frame | centre (cx_j, 100); sizes s_j + 6 / s_j; Rotation 45 | 1 / 2 | INK / (255,230,128). cx_j = 20 + (j-1) * 130/6; s_j = 14 + (((j-1)*7 + 2) % 5) * 1.6. Hidden until the crack |
| Egg.BottomHalf | Frame | -6, 100, 182, 106 | 3 | ClipsDescendants true, never rotated. Child Oval (6, -100, 170, 200) |
| Egg.TopHalf | **CanvasGroup** | -6, -6, 182, 106 | 4 | Child Oval (6, 6, 170, 200) + Spec (46, 36, 26, 14). Hidden until the crack |
| Egg.WholeEgg | Frame | AnchorPoint 0.5, centre (85, 100), 170 x 200 | 5 | The Oval look + Spec (40, 30, 26, 14). Wobbles |
| Egg.CrackLine | Frame | 0, 0, 170, 200 | 6 | 8 INK segments, 4 thick, through (4,100) (24,93) (44,107) (64,93) (85,107) (106,93) (126,107) (146,93) (166,100). Hidden |
| Pop.TitleRoot | Frame | AnchorPoint 0.5, centre (320, 386), 600 x 60 | 6 | UIScale `TitleScale`. TitleShadow text ("SECRET PET!", 0, 4, 600, 52) INK, stroke 4. Title text ("SECRET PET!", 0, 0, 600, 52) white + UIGradient H.RAINBOW + stroke 4 |
| Pop.Name | text | (pet upper .. "  " .. KG, 20, 414, 600, 22) | 6 | GOLD_TXT, stroke 3 |
| Pop.Sub | text | ("+5 OF EVERY POTION  +" .. cash, 20, 442, 600, 20) | 6 | LAV |
| Pop.Tap | text | ("TAP TO CONTINUE", 160, 472, 320, 16) | 6 | LAV_DIM, stroke 2 |

- **Oval** = Frame 170 x 200, corner round, stroke 4. Gradient 0 (255,244,190), 0.5 (255,230,128), 0.8 (255,176,0), 1 (216,138,0). Spec = white, BackgroundTransparency 0.3, round.
- **Studio hook:** BindableEvent `StreakCelebrate.TestCelebrate`. It replays the celebration with the current StreakPet and claims nothing.

### 4.10 StreakFly (claim fly-text)

ScreenGui `StreakFly`: DisplayOrder 46, ResetOnSpawn false, IgnoreGuiInset false, default insets (the same space as MainMenu, so AbsolutePositions match).

Per claim (Days 1-6), create one TextLabel:
- AnchorPoint 0.5, size 400 x 40, TextSize 28, stroke 3, UIScale = the window scale.
- Start: the card centre `(abs.X + abs.W/2, abs.Y + 56 * s)` minus `StreakFly.AbsolutePosition`.

| Day | Copy | Colour | Target |
|---|---|---|---|
| 1, 3, 6 | `"+" .. lines[1]` | (150,255,60) | centre of `SpeedUI.Holder.MoneyRow` |
| 2 | `lines[1]` | (85,200,255) | centre of `SpeedUI.Holder.SpeedRow` |
| 4 | `BIG EGG!` | GOLD_TXT | start minus (0, 120 s) |
| 5 | `+9 POTIONS` | (199,139,255) | start minus (0, 120 s) |

**Motion:**
1. Pop UIScale 0.5 -> 1.1 (0.12 s, Quad Out), then 1.1 -> 1 (0.08 s).
2. Hold 0.15 s.
3. Fly to the target (0.6 s, Quad In) while the scale goes to 0.6 and TextTransparency and stroke Transparency go to 0.3.
4. Destroy.

---

## 5. Behaviour

### 5.1 Card states (small cards and slots; the hero uses 4.7)

| State | Dim BackgroundTransparency (= brightness) | Icon ImageColor3 | Day pill | Ring | Badges | Button |
|---|---|---|---|---|---|---|
| CLAIM | 1.0 | 255 | lime | on | none | lime "CLAIM!" + pulse |
| CLAIMED | 0.6 | 153 | dark | off | Check | silver "CLAIMED" |
| TOMORROW | 0.85 | 217 | dark | off | none | dusk + Clock + timer |
| LOCKED | 0.45 (hero 0.95) | 199 | dark | off | Lock (not on the hero) | off "LOCKED" (hero: IN n DAYS) |

- **Applying a state:** `setCardState(c, d, st)` applies it only when the state changes. It writes `Card<d>:SetAttribute("State", st)`.
- **Tweens:** the dim and tint tween over 0.3 s (Quad Out) when the window is visible; otherwise they snap.
- **Check stamp:** on CLAIM -> CLAIMED while visible, the stamp `Stamp` goes 1.8 -> 1 and Rotation -20 -> -8 (Back, 0.22 s).
- **Button labels:** `H.fit` with variants. The flash override `flash[d] = {variants, until}` uses this mapping of server reasons:

| Server reason | Variants |
|---|---|
| "Come back tomorrow!" | {"TOMORROW!"} |
| "Please wait" | {"WAIT..."} |
| "Pets full!" | {"PETS FULL!"} |
| "Eggs full!" | {"EGGS FULL!"} |
| anything else | {"TRY AGAIN"} |

### 5.2 Idle motion (every frame, only while `page.Visible and win.Visible` and the view is visible)

- **CLAIM buttons:** `btn.pulse(t)`, i.e. `ButtonScale = 1 + 0.025 * (1 - cos(2 pi t / 1.2))` (1.00..1.05). If GiftPage `HatchTestPulse` is a number (Studio only), use that fixed value. Everything else: `btn.stopPulse()`.
- **Day 7 Rays** rotate 12 deg/s. **PrismRim** gradient Rotation += 30 deg/s. **Shine** sweeps every 3 s.
- **TodayGlow** transparency 0.45 + 0.15 sin(2 pi t / 0.9).
- **Text and state refresh** every 0.1 s (`updateCards` / the slot refresh), as today.

### 5.3 Hover and press

- **Buttons and tabs:** glossButton motion (section 7.2): hover 1.04 (Quad Out, 0.08 s); press: face +d (0.05 s) and scale 0.95; release: Back 0.18 s.
- **Cards** (`holder.MouseEnter`/`MouseLeave`): HoverFx -> BackgroundTransparency 0.94 (0.1 s); every ImageLabel in `Icons.Pop` -> Rotation -6 (Back Out, 0.15 s). Leave reverts both.

### 5.4 Claim sequence (Days 1-6; about 0.9 s; spec 2.5)

`press(d)` keeps today's logic (busy lock, `stateOf(d) ~= "CLAIM"` returns, compute `lines` before the claim, `Claim:InvokeServer()`). Then:
- **On failure:** set the flash and run `updateCards()`.
- **On success:**
  1. `SFX.play("HatchWin")`.
  2. `btn.flash()`: Flash BackgroundTransparency 0.1, wait 0.08 s, tween to 1 (0.1 s).
  3. Icon pop: `PopScale` 1 -> 1.25 (0.12 s, Quad Out), then 1 (0.23 s, Back Out). It stays inside the clipping `Icons` frame.
  4. Shards: `H.shards(DailyView.Fx, x + 79, y + 56)`. That is 9 pieces from the icon centre:
     - 6 Frames of 6 x 6 at Rotation 45, colours cycling (255,230,128), (255,176,0), white;
     - 3 star stickers of 12 px (112780117360743);
     - each one tweens 0.6 s (Quad Out) to `start + (cos a, sin a) * r`, with `a = k/9 * 2 pi + rand(-0.2, 0.2)` and `r = rand(40, 70)`, clamped to x 8..732 and y 66..455;
     - while flying they rotate ±180 deg and fade to 1, then are destroyed.
  5. The pip for day d: `PopScale` 1.35 -> 1 (Back, 0.25 s) plus the crack wobble (Rotation -8 -> 8 -> 0, 0.05 s each).
  6. Fly-text (4.10) if `res ~= 7`; for `res == 7`, `celebrate(pet, kgText, cashText)`.
  7. When StreakServer publishes the new attributes, `setCardState` runs the dim tween and the stamp (5.1).

**Slots** (`claim(i)`): the same flash, pop and shards into `PlaytimeView.Fx`, then the slot's own state change (5.1). There is no fly-text. Each slot has its own `busy` flag. Only CLAIM slots invoke the server.

### 5.5 Day 7 celebration timeline (t = seconds after `celebrate()`)

**Reference step (owner's animation rule; UI motion = one quick reference is enough):** open one egg-crack or hatch clip on animationreference.org. Note the anticipation, crack and pop frames. Write a 3-line Reference table in the progress ledger. Keep the timings below unless the reference clearly argues otherwise.

| t | What happens |
|---|---|
| 0.00 | Enabled. Reset: WholeEgg visible at Rotation 0; TopHalf, BottomHalf, teeth, CrackLine segments and PetRoot hidden; texts hidden. Backdrop BackgroundTransparency 1 -> 0.2 (0.2 s). PopScale 0.6 -> 1 (Back, 0.35 s). Rays ImageTransparency 1 -> 0.3 (0.4 s) |
| 0.35-1.25 | Wobble: WholeEgg.Rotation goes -10, 10, -8, 8, -5, 0, each step 0.15 s (Sine InOut) |
| 1.25-1.45 | CrackLine segments appear left to right, 0.025 s apart |
| 1.45 | Swap: WholeEgg and CrackLine hidden; TopHalf, BottomHalf and teeth visible. TopHalf Position +(30, -90), Rotation -25 (0.25 s, Quad Out), then Position +(0, 420), Rotation -80, GroupTransparency 1 (0.55 s, Quad In), then hidden |
| 1.55 | PetRoot visible at centre (320, 250) with PetScale 0.3. It tweens to (320, 170), PetScale 1 (Back Out, 0.45 s). The pet climbs out from behind BottomHalf (Z 3 < 4) |
| 1.70 | TitleScale 0 -> 1 (Back, 0.35 s). Name, Sub and Tap fade in (0.3 s) |
| idle | Rays turn 12 deg/s. Title gradient Offset X = sin(2t) * 0.3 (the prism sweep) |
| 6.0 | Auto close (the existing token logic). A Backdrop tap closes it at any time |

### 5.6 Other behaviour kept or rerouted

- **Tabs:** `applyTab()` keeps its logic (views, title, `updateCards`) and also calls `tabs.set(tab)` and the dot rules (4.3). `onShown` and the auto-open loop are unchanged.
- **Streak lost:** when DailyView becomes visible with `StreakLost == true` and claimable, the first time this session:
  - Label -> "LOST!" in RED_TXT for 4 s;
  - pips shake for 0.6 s (Position.X offset ±2, sine 25 Hz);
  - then "STREAK" in LAV.
- **Week complete:** the Day 7 button timer (4.7). Count shows "7/7".
- **TestPress:** `Card<d>.TestPress` (Studio) is unchanged.
- **Tile badge / "Claim!" label:** unchanged (PlaytimeClient).
- **The old status-line toast** is gone; the fly-text replaces it (spec 2.4).
- **Respawn:** MainMenu has ResetOnSpawn false. StreakCelebrate and StreakFly are created with ResetOnSpawn false (memory: respawn rule).

---

## 6. Assets (no uploads)

| Use | Asset id | In the game today? |
|---|---|---|
| Cash | 131724750673548 | yes (PlaytimeClient, IndexClient...) |
| Speed shoe | 80829076123513 | yes (SpeedStat.Icon) |
| Lock | 124356037818343 | yes (UpgradeClient) |
| Check | 78526516923039 | yes (StreakClient) |
| Clock (TOMORROW timers) | 106606523697579 | **no**: Check-UI pack `Item/Clock/Clock 1st`, a third-party public image |
| Robux (SKIP ALL) | 132185731364109 | yes (StarterPackClient, OfflineClient) |
| Gift (header icon) | 128336310005291 | yes (the MainMenu Gift tile icon) |
| Glow (glows, halo, sheen) | 121438949090215 | yes (RebirthClient; a soft disc, "glow2.png") |
| Rays (Day 7, celebration) | 76624006953375 | yes (RebirthClient) |
| Star (confetti sparkles) | 112780117360743 | yes (IndexClient, ShopConfig) |
| Potions | `PotionConfig.byKey.Money/Hatch/Speed.icon` = 88886704386081 / 79394853866565 / 94938733066793 | yes |
| Eggs | `StreakConfig.EGG_ICONS` (6 ids) + fallback 135711525932647 | yes |
| Pet portraits | `IndexConfig.PORTRAITS[...]` (all values) | yes |

- **No longer used by the Gift window:** sunburst 130563114903838 and `PotionConfig.TILE_ICON`.
- **Verification:** run `hatch_assets.lua` (8.5) in a Play test. Every id must report `Enum.AssetFetchStatus.Success`.
- **If the clock fails:**
  - set `H.ICON.clock = ""`;
  - the Clock images stay hidden;
  - the timer label boxes become centred: small cards (0, 2, 142, 17), hero (0, 3, 202, 17).
  - Write this in the ledger. **Do not upload** a replacement.
- **Optional, owner's call** (section 11): the bat sticker for the Halloween band. The SVG is in `dirB_hatchnight.html` (`BATS`). Upload it as a 168 x 84 PNG, group-owned by ZAB Studio. If approved, add an ImageLabel `Bats` (600, 3, 84, 42), Z 6, to HatchFront, visible only for the Pumpkin theme.

---

## 7. Code plan

### 7.1 BrickUI: append before `return BrickUI`

```lua
------------------------------------------------------------------ HATCH NIGHT window skin (2026-10-21)
-- The owner picked style B "HATCH NIGHT" (docs/specs/2026-10-21-slingshot-ui-style.md); its helpers live in the child
-- module BrickUI.Hatch. A MainMenu page's skin = PAGE_SKIN[page] or WINDOW_SKIN. Phase 1: only the Gift window.
-- Phase 2 = WINDOW_SKIN "Hatch" (each page's content must also be rebuilt on the 740 x 463 canvas). Not a third STYLE
-- value: 6 scripts test STYLE == "CheckUI" and would all fall back to the old Brick look.
BrickUI.WINDOW_SKIN = "CheckUI"
BrickUI.PAGE_SKIN = {Gift = "Hatch"}
function BrickUI.skinFor(page) return BrickUI.PAGE_SKIN[page] or BrickUI.WINDOW_SKIN end
do
	local ok, H = pcall(require, script:WaitForChild("Hatch", 5))
	if ok and type(H) == "table" then BrickUI.Hatch = H else warn("[BrickUI] Hatch skin not loaded: " .. tostring(H)) end
end
```

### 7.2 `ReplicatedStorage.BrickUI.Hatch`: helper API (write this module exactly; no `require` of BrickUI)

```lua
-- BrickUI.Hatch (2026-10-21): HATCH NIGHT, the owner's window style (spec docs/specs/2026-10-21-slingshot-ui-style.md,
-- direction B; plan docs/plans/2026-10-21-hatch-night-gift-window.md). Everything is built in LOGICAL px (window 740 x
-- 470, face 740 x 463) under one UIScale = window px / 740: strokes, corners and text scale together.
-- Containment rules (spec 2.1): every element + its Border UIStroke inside its parent, 8 px gutters, depth inside the
-- holder, pulse buttons only (<= 1.05), no badge rotated past its box, highlights inward, GothamBlack only, fixed TextSize.
-- Test attributes read by docs/plans/tests-2026-10-21/hatch_containment.lua: HatchPad, HatchPadBottom, HatchTile,
-- HatchGap, HatchHit, HatchRadial, HatchShell, HatchMin.
local TweenService = game:GetService("TweenService")
local TextService = game:GetService("TextService")
local H = {}
local C = Color3.fromRGB
H.W, H.H, H.FACE_H = 740, 470, 463
H.FONT = Font.fromEnum(Enum.Font.GothamBlack)
H.WHITE = Color3.new(1, 1, 1)
H.INK = C(13, 11, 28)
-- ... all palette / band / glow / icon constants of section 4.0 and 6 (H.CANVAS, H.CARD, H.CARD_TODAY, H.RECESS,
-- H.HERO_FACE, H.LAV, H.LAV_DIM, H.LIME_TXT, H.GOLD_TXT, H.RED_TXT, H.PAL, H.BAND, H.GLOW, H.AREA_GLOW, H.ICON, H.RAINBOW)
H.HEADER_TEETH = {}
for i = 0, 36 do H.HEADER_TEETH[i + 1] = {16 + i * 708 / 36, 11 + ((i * 7 + 3) % 5) * 1.6} end
H.SHELL_TEETH = {{18, 15.2}, {39.06, 18.4}, {64.56, 13.6}, {83.41, 16.8}}
H.PIP_CRACK = {{2.5, 10.5, 4.81, -33.69}, {5.5, 11.5, 6.2, 53.13}, {8.5, 11.5, 6.2, -53.13}, {11.5, 11.5, 6.2, 53.13}, {15, 12, 6.2, -36.87}}

function H.frame(parent, name, x, y, w, h, color, z) -- Offset frame, AnchorPoint (0,0); color nil = transparent
	local f = Instance.new("Frame")
	f.Name = name
	f.BorderSizePixel = 0
	f.Position = UDim2.fromOffset(x, y)
	f.Size = UDim2.fromOffset(w, h)
	f.BackgroundColor3 = color or H.WHITE
	f.BackgroundTransparency = color and 0 or 1
	f.ZIndex = z or 1
	f.Parent = parent
	return f
end
function H.corner(o, px) local c = Instance.new("UICorner") c.CornerRadius = px == "round" and UDim.new(0.5, 0) or UDim.new(0, px) c.Parent = o return c end
function H.stroke(o, px, color, transp)
	local s = Instance.new("UIStroke")
	s.ApplyStrokeMode = Enum.ApplyStrokeMode.Border
	s.Thickness = px
	s.Color = color or H.INK
	s.Transparency = transp or 0
	s.LineJoinMode = Enum.LineJoinMode.Round
	s.Parent = o
	return s
end
function H.gradient(o, keys, rotation) -- keys = {c0, c1} or {{t, color}, ...}
	local g = Instance.new("UIGradient")
	g.Rotation = rotation or 90
	H.setKeys(g, keys)
	g.Parent = o
	return g
end
function H.setKeys(g, keys)
	if typeof(keys[1]) == "Color3" then g.Color = ColorSequence.new(keys[1], keys[2]) return end
	local seq = {}
	for _, k in keys do table.insert(seq, ColorSequenceKeypoint.new(k[1], k[2])) end
	g.Color = ColorSequence.new(seq)
end
function H.image(parent, name, img, x, y, w, h, z, fit)
	local i = Instance.new("ImageLabel")
	i.Name = name
	i.BackgroundTransparency = 1
	i.BorderSizePixel = 0
	i.Image = img or ""
	i.ScaleType = fit and Enum.ScaleType.Fit or Enum.ScaleType.Stretch
	i.Position = UDim2.fromOffset(x, y)
	i.Size = UDim2.fromOffset(w, h)
	i.ZIndex = z or 1
	i.Parent = parent
	return i
end
function H.glow(parent, name, x, y, w, h, color, transp, z)
	local g = H.image(parent, name, H.ICON.glow, x, y, w, h, z)
	g.ImageColor3 = color
	g.ImageTransparency = transp
	return g
end
function H.sticker(parent, name, img, x, y, size, z) -- frameless art + ink drop shadow (+3 px, black 0.55)
	local sh = H.image(parent, name .. "Shadow", img, x, y + 3, size, size, z or 2, true)
	sh.ImageColor3 = C(6, 4, 20)
	sh.ImageTransparency = 0.45
	local im = H.image(parent, name, img, x, y, size, size, (z or 2) + 1, true)
	im:GetPropertyChangedSignal("Image"):Connect(function() sh.Image = im.Image end)
	im:GetPropertyChangedSignal("Rotation"):Connect(function() sh.Rotation = im.Rotation end)
	im:GetPropertyChangedSignal("Visible"):Connect(function() sh.Visible = im.Visible end)
	return im, sh
end

-- the mockup txt(): box (x, y, w, size + 2), fixed TextSize, centred, ink Contextual stroke (2.5 default)
function H.text(parent, name, text, x, y, w, size, opts)
	opts = opts or {}
	local t = Instance.new("TextLabel")
	t.Name = name
	t.BackgroundTransparency = 1
	t.BorderSizePixel = 0
	t.FontFace = H.FONT
	t.TextScaled = false
	t.TextWrapped = false
	t.RichText = false
	t.TextSize = size
	t.TextColor3 = opts.color or H.WHITE
	t.TextXAlignment = opts.align or Enum.TextXAlignment.Center
	t.TextYAlignment = Enum.TextYAlignment.Center
	t.Position = UDim2.fromOffset(x, y)
	t.Size = UDim2.fromOffset(w, size + 2)
	t.ZIndex = opts.z or 2
	t:SetAttribute("HatchBase", size)
	t:SetAttribute("HatchMin", opts.min or math.min(size, 16))
	local s = Instance.new("UIStroke")
	s.ApplyStrokeMode = Enum.ApplyStrokeMode.Contextual
	s.Thickness = opts.stroke or 2.5
	s.Color = H.INK
	s.LineJoinMode = Enum.LineJoinMode.Round
	s.Parent = t
	t.Parent = parent
	H.fit(t, text)
	return t
end
function H.place(t, x, y, w, size, align) -- move a label to another mockup box (the timer state, the flash)
	t.Position = UDim2.fromOffset(x, y)
	t.Size = UDim2.fromOffset(w, size + 2)
	t.TextXAlignment = align or Enum.TextXAlignment.Center
	t:SetAttribute("HatchBase", size)
	t:SetAttribute("HatchMin", math.min(size, 16))
	t:SetAttribute("HatchText", nil)
end
-- first variant that fits the box width (minus the stroke) at the biggest size from HatchBase down to HatchMin.
-- Never below HatchMin: if nothing fits it shows the last variant at HatchMin and returns false (tests catch it).
function H.fit(label, variants)
	if type(variants) == "string" then variants = {variants} end
	local key = table.concat(variants, "|")
	if label:GetAttribute("HatchText") == key then return true end
	label:SetAttribute("HatchText", key)
	local base, min = label:GetAttribute("HatchBase") or label.TextSize, label:GetAttribute("HatchMin") or 16
	local st = label:FindFirstChildOfClass("UIStroke")
	local room = label.Size.X.Offset - 2 * (st and st.Thickness or 0)
	for _, v in variants do
		for size = base, min, -1 do
			if v == "" or TextService:GetTextSize(v, size, Enum.Font.GothamBlack, Vector2.new(10000, 10000)).X <= room then
				label.TextSize = size
				label.Text = v
				return true
			end
		end
	end
	label.TextSize = min
	label.Text = variants[#variants]
	return false
end
```

**The remaining helpers.** Signatures and rules are exact; the bodies follow section 4.

- **`H.glossButton(parent, name, x, y, w, h, palName, opts) -> btn`**
  - opts: `d` (3), `r` (9), `ol` (2.5), `size` (18), `text`, `labelName` ("Label"), `color`, `z` (3), `input` (a GuiButton that drives the motion; then Face is a Frame, otherwise Face is an ImageButton).
  - Builds: holder (centre-anchored at (x + w/2, y + h/2), size w x h, UIScale `ButtonScale`); Side (0, d, w, h-d); Face (0, 0, w, h-d) with `UIGradient`; TopHL (0.65 r, 1, w - 1.3 r, 1.5); Gloss (3, 2, w-6, round(0.42 (h-d))) with corner max(r-2, 0) and transparency 0.58 -> 0.92; Label `text(opts.text, 0, round((h-d-size)/2) - 1, w, size)` at Z 4; Flash (0, 0, w, h-d), white, BackgroundTransparency 1, corner r, Z 5.
  - Returns `{holder, face, side, label, scale, flashFrame, d, w, h, setPalette(name), pulse(t, fixed?), stopPulse(), flash(), activated = (opts.input or face).Activated}`.
  - Motion:
    - `rest() = pressed and 0.95 or hovered and 1.04 or 1`;
    - MouseEnter/MouseLeave tween ButtonScale to `rest()` (Quad Out, 0.08 s) unless pulsing;
    - MouseButton1Down: face Position -> (0, d) (0.05 s) and scale 0.95;
    - MouseButton1Up: face -> (0, 0) (Back, 0.18 s) and scale `rest()` (Back, 0.18 s);
    - MouseLeave also releases a press.
  - `pulse(t, fixed)` sets `pulsing = true` and, if not pressed, `scale.Scale = fixed or 1 + 0.025 * (1 - cos(2 pi t / 1.2))`. `stopPulse()` sets `pulsing = false` and `scale.Scale = rest()`.
- **`H.recess(parent, name, x, y, w, h, z) -> frame`**: corner h/2, stroke 2, recess gradient, TopShade (19, 0, w-38, 3) black at BackgroundTransparency 0.6, BottomLine (19, h-1.5, w-38, 1.5) recess line at 0.65.
- **`H.pill(parent, name, x, y, w, text) -> {frame, label, setToday(bool)}`** (4.5). **`H.chip(parent, name, x, y, w) -> frame`** (4.7). **`H.dot(parent, name, x, y) -> frame`** (4.3). **`H.tag(parent, name, x, y, w, h, text) -> frame`** (4.7).
- **`H.shellCard(parent, name, x, y, w, h, opts) -> card`**: opts `z`, `tile`, `solid`. Builds the holder and children of 4.5 (Hit, Side, Face, TopHL, Dim, HoverFx, Icons{Pop + PopScale}, Badges) and the attributes `HatchPad 8`, `HatchTile`, `HatchGap 8`. Returns `{holder, hit, face, side, dim, hover, icons, pop, popScale, badges, setToday(on), setBright(level, animate), tint(v, animate)}`. It also hooks the hover of 5.3. `tint` sets ImageColor3 (v,v,v) on every ImageLabel in `pop` whose name doesn't end in "Shadow".
- **`H.eggPip(parent, name, cx, cy, z) -> pip`**: centre-anchored 18 x 23 (4.4). `pip.set(state)` takes `done|today|lock|hero|herotoday|herodone` and sets the attribute `State`. `pip.crackWobble()`.
- **`H.crackEdge(parent, teeth, yLine, color, inkGrow, z) -> inks, teeth`**: for each `{cx, s}` it adds an INK square (s + inkGrow) and then a coloured square (s), both centre-anchored at (cx, yLine) with Rotation 45. Ink frames get ZIndex z and coloured ones z + 1. Names `Ink<i>` / `Tooth<i>`.
- **`H.segment(parent, name, ax, ay, bx, by, thick, color, z) -> frame`**: a centre-anchored bar from A to B; length = |AB| + thick/2, Rotation = atan2.
- **`H.prismRim(face, inset, thick, radius) -> UIGradient`** (4.7).
- **`H.shards(fx, cx, cy)`** (5.4).
- **`H.windowChrome(win) -> chrome`**: builds HatchBack and HatchFront (4.1, 4.2), both with Visible false. Returns `{back, front, title, titleShadow, icon, closeBtn, closeHit, setTheme(name), setTitle(text), show(on)}`. The SkinScale UIScales are bound to `win.AbsoluteSize`.
- **`H.bandTheme() -> "Pumpkin" | "HatchGold"`** (4.0).
- **`H.bindCanvasScale(canvas, ref, logicalW) -> UIScale`**: a UIScale `CanvasScale` on the canvas, = `ref.AbsoluteSize.X / logicalW`, re-bound on change.
- **`H.fitWindow(guiW, guiH, leftClear, cap) -> s, w, h, cx, cy`** (pure; section 3):

```lua
function H.fitWindow(guiW, guiH, leftClear, cap)
	cap = cap or 1.18
	local left, right = math.max(8, leftClear or 0), guiW - 8
	local s = math.clamp(math.min(cap, (right - left) / H.W, (guiH - 12) / H.H), 0.5, cap)
	local w, h = H.W * s, H.H * s
	local lo = left + w / 2
	local cx = math.clamp(guiW / 2, lo, math.max(lo, right - w / 2))
	return s, w, h, cx, guiH / 2
end
```

### 7.3 MenuController: the skin hook

1. Line 25: `local header, closeFace` -> `local header, closeFace, closeHolder`. Line 38: drop the `local` (`closeHolder, closeFace = B.closeButton(...)`).
2. Line 75: `local function mul(s, k) return UDim2.new(s.X.Scale * k, s.X.Offset * k, s.Y.Scale * k, s.Y.Offset * k) end`. Scale-only sizes give identical results.
3. Insert after the CUI block (after line 57):

```lua
-- (2026-10-21) HATCH NIGHT per-page skin (BrickUI.skinFor): Hatch pages get the night shell (Window.HatchBack /
-- HatchFront from BrickUI.Hatch) and a full-face transparent Body (the page builds its own 740 x 463 canvas); every
-- other page gets today's Check-UI chrome back from `saved`. Plan: docs/plans/2026-10-21-hatch-night-gift-window.md
local H = CUI and B.Hatch or nil
local hatch = H and H.windowChrome(win) or nil
local bodyF = panel:WaitForChild("Body")
local saved = {
	faceSize = panel.Size, facePos = panel.Position, faceT = panel.BackgroundTransparency,
	faceStroke = panel:FindFirstChildOfClass("UIStroke"),
	bodySize = bodyF.Size, bodyPos = bodyF.Position, bodyT = bodyF.BackgroundTransparency,
	bodyStroke = bodyF:FindFirstChildOfClass("UIStroke"),
}
local skinNow = "CheckUI"
local function applySkin(skin)
	skinNow = skin
	local on = skin == "Hatch"
	if hatch then hatch.show(on) end
	win.Depth.Visible = not on
	panel.BackgroundTransparency = on and 1 or saved.faceT
	if saved.faceStroke then saved.faceStroke.Enabled = not on end
	panel.Size = on and UDim2.fromScale(1, 463 / 470) or saved.faceSize
	panel.Position = on and UDim2.fromScale(0.5, 463 / 940) or saved.facePos
	if header then header.Visible = not on end
	if closeHolder then closeHolder.Visible = not on end
	panel.Icon.Visible = not on
	panel.Title.Visible = not on
	bodyF.Size = on and UDim2.fromScale(1, 1) or saved.bodySize
	bodyF.Position = on and UDim2.fromScale(0.5, 0.5) or saved.bodyPos
	bodyF.BackgroundTransparency = on and 1 or saved.bodyT
	if saved.bodyStroke then saved.bodyStroke.Enabled = not on end
end
local function rightEdge(o)
	if not (o and o:IsA("GuiObject") and o.Visible) then return 0 end
	return o.AbsolutePosition.X - gui.AbsolutePosition.X + o.AbsoluteSize.X
end
local function hatchFit()
	local hud = player.PlayerGui:FindFirstChild("SpeedUI")
	local pills = hud and hud.Enabled and hud:FindFirstChild("Holder") or nil
	local gs = gui.AbsoluteSize
	local s, w, h, cx, cy = H.fitWindow(gs.X, gs.Y, math.max(rightEdge(menu), rightEdge(pills)) + 6)
	local test = RunService:IsStudio() and gui:GetAttribute("HatchTestScale")
	if type(test) == "number" then s = test w, h, cx, cy = H.W * s, H.H * s, gs.X / 2, gs.Y / 2 end
	return UDim2.fromOffset(w, h), UDim2.fromOffset(cx, cy)
end
panel:WaitForChild("Title"):GetPropertyChangedSignal("Text"):Connect(function()
	if hatch and skinNow == "Hatch" then hatch.setTitle(panel.Title.Text) end
end)
```

4. In `openWindow`, right after `panel.Body.Message.Visible = custom == nil` (line 182):

```lua
	local skin = (hatch and custom and B.skinFor(name) == "Hatch") and "Hatch" or "CheckUI"
	applySkin(skin)
	if skin == "Hatch" then
		hatch.setTheme(H.bandTheme())
		hatch.setTitle(panel.Title.Text)
		hatch.icon.Image = panel.Icon.Image
		local ar = win:FindFirstChildOfClass("UIAspectRatioConstraint")
		if ar then
			if not win:GetAttribute("BaseAspect") then win:SetAttribute("BaseAspect", ar.AspectRatio) end
			ar.AspectRatio = H.W / H.H
		end
		local size, pos = hatchFit()
		win.Position = pos
		win.Size = mul(size, 0.6)
		win.Visible = true
		setHotbar(false)
		tween(win, 0.32, {Size = size}, Enum.EasingStyle.Back)
		return
	end
```

   The CheckUI path below is unchanged. `fitScale` resets `win.Position = basePos`, and the AR line resets the aspect per page.

5. After the `openPage` block (line 219), add the following, and wire `hatch.closeHit.Activated:Connect(closeWindow)` where `closeFace.Activated` is connected (line 210):

```lua
workspace.CurrentCamera:GetPropertyChangedSignal("ViewportSize"):Connect(function()
	if openName and skinNow == "Hatch" and hatch then
		local size, pos = hatchFit()
		win.Size = size
		win.Position = pos
	end
end)
```

6. The `LAYOUT.Gift = {1.95, 1.2}` entry stays. It is only used if the Gift page ever falls back to CheckUI; rollback = the backups (section 10).

### 7.4 PlaytimeClient

- **Keep:** the requires, remotes, tile/badge code, `fmt`, `claimedSet`, `elapsed`, `skipPrice`, `petName`, the SkipAll handler logic, and the tile part of the RenderStepped loop.
- **Delete:**
  - the `B.frame` GiftPage/view;
  - `well`, studs, `cellsFrame` and its UIGridLayout;
  - the `B.brick` cells and their claim handler;
  - `warn` (the "Leaving Resets Progress!" label), `skipTitle`, `B.priceButton` and the old skip icon/label fiddling;
  - the NAVY/GREEN constants and the old cell drawing block.
- **Build:**
  - `local H = B.Hatch`;
  - `page = H.frame(body, "GiftPage", 0, 0, 740, 463)` with `page.Visible = false`, `page.ZIndex = 3`, and `H.bindCanvasScale(page, body, 740)`;
  - `view = H.frame(page, "PlaytimeView", 0, 0, 740, 463)` with ZIndex 3, plus `view.Fx`;
  - PlayBar and SkipAll (4.8) and the 12 slots (4.8);
  - claims via `claim(i)` (5.4);
  - the skip error flash per 4.8.
- **Refresh** (10x/s, only while `page.Visible and view.Visible`, except the tile part and `PlaytimeReady`):
  - compute `ready` as today and `page:SetAttribute("PlaytimeReady", ready)`;
  - per slot: the state (`claimed[i]` -> CLAIMED, `left <= 0.5` -> CLAIM, else WAIT), the texts (`H.fit` only when the text changes) and `setSlotState` on a change;
  - every frame while visible: `btn.pulse(t)` for CLAIM slots (or `HatchTestPulse`).

### 7.5 StreakClient

- **Keep as is:** lines 1-65 (requires and helpers; add `local H = B.Hatch`), `stateOf`, `flash`, `clock`, `press()` (with the 5.4 additions), the TestPress block, `applyTab` (plus `tabs.set` and the dots), `onShown`, the attribute listeners and the auto-open loop.
- **Delete:**
  - CARD_GRAD, LIME/SILVER/OFF, COL_X, `square`, `text`;
  - the tab row (lines 77-96);
  - the status line (lines 102-106);
  - the card loop (lines 108-180);
  - the old `lineTexts`/`iconOf` bodies;
  - the old `updateCards` visuals and status block;
  - the old celebration (lines 259-328);
  - the sunburst/shine/pulse code in RenderStepped.
  - Move RAINBOW to `H.RAINBOW`.
- **Build:**
  - Tabs (4.3), DailyView, Streak, Card1..6 (4.5/4.6), Card7 (4.7);
  - StreakFly (4.10) and StreakCelebrate (4.9);
  - `lineTexts(d)` per 4.6. Day 7 returns `{name upper, kgText, "x5", cashText}`.
- **`updateCards()`** (every 0.1 s while visible, and on attribute change):
  - per card: texts (fit on change), images (egg kind, pet portrait), Day 4 glow colour, `setCardState`, and the timer/flash label;
  - then the streak bar (4.4);
  - then the lost message (5.6).
- **RenderStepped:**
  - dots (4.3);
  - the celebration idle motion when `cel.Enabled`;
  - return if hidden;
  - pulse, rays, prism, shine, TodayGlow (5.2);
  - every 0.1 s `updateCards()`.

---

## 8. Test plan

Rules for every Play test:
- Read `workspace:GetAttribute("TestFreshSave")` in Edit before starting; it must be `true` (hard rule).
- Check `get_studio_state` first. Another agent may be in Play: never stop someone else's session; wait for Edit.
- Never drive the Studio UI (memory rule).
- The owner may be moving in the session, so tests only read GUI state.

### 8.1 `hatch_pure.lua` (Edit datamodel; `require(game.ReplicatedStorage.BrickUI.Hatch:Clone())`, because of the Edit require cache)

**Checks:**
1. `fitWindow` with the 4 rows of section 3 (tolerance 0.05 on s, 0.5 px on sizes). Input `(guiW, guiH, leftClear)` -> expected `(s, w, h, cx, cy)`:

| Input | Expected |
|---|---|
| (1920, 1022, 412.1) | (1.18, 873.2, 554.6, 960, 511) |
| (1050, 562, 229.3) | (1.0982, 812.7, 516.2, 635.65, 281) |
| (732, 346, 144.3) | (0.7106, 525.9, 334.0, 407.24, 173) |
| (667, 331, 137.9) | (0.6787, 502.3, 319.0, 389.03, 165.5) |

2. Also `fitWindow(500, 300, 140)` returns s = 0.5 (floor).
3. `#HEADER_TEETH == 37`. Ink extents left >= 0, right <= 740, bottom <= 62.
4. `#SHELL_TEETH == 4`. Extents inside 0..104 x 0..60.
5. The palettes lime/red/silver/off/gold/dusk exist; the band themes Pumpkin/HatchGold exist; every `H.ICON` entry is a non-empty string.
6. `H.fit` on an unparented label (150 wide, base 20, min 16, stroke 2.5):
   - "$9K" -> true, size 20;
   - `{"A VERY LONG LINE THAT CANNOT FIT HERE", "OK"}` -> true, Text "OK";
   - "A VERY LONG LINE THAT CANNOT FIT HERE" alone -> false, size 16.

Expected: all pass.

### 8.2 `streak_client.lua` v2 (Client datamodel, fresh session; also stored as `StreakTests.CLIENT_SRC`)

Copy v1 to `streak_client_v1.lua` first. v2 checks:

1. **auto_open**:
   - the window is visible within 20 s, then wait 0.6 s;
   - Tab == "Daily";
   - `Face.Title.Text == "Daily Rewards"` and `HatchFront.Title.Text == "DAILY REWARDS"`;
   - HatchBack and HatchFront are Visible;
   - `Face.Header`, `Face.Title` and `Depth` are not Visible;
   - the window AbsoluteSize ratio is 740/470 ± 0.01;
   - `GiftPage.CanvasScale.Scale == HatchBack.SkinScale.Scale` ± 0.001;
   - `Tabs` exists.
2. **states**: `State` attribute plus label (`Card<d>:FindFirstChild("State", true).ContentText`):
   - Card1 CLAIM / "CLAIM!";
   - Card2 LOCKED / "LOCKED";
   - Card7 LOCKED / "IN 6 DAYS";
   - Pip1 `State == "today"`, Count "1/7";
   - `Card1.Badges.Ring.Visible`;
   - the tile `Badge.Visible`.
3. **claim**: `Card1.TestPress:Fire()`, then within 3 s:
   - Card1 CLAIMED / "CLAIMED" and `Card1.Badges.Check.Visible`;
   - Card2 TOMORROW, label matching `^%d%d:%d%d:%d%d$`;
   - Pip1 `done`, Count "1/7";
   - `PlayerGui.StreakFly` gets a child within 1 s.
4. **playtime_tab**: set `Tab = "Playtime"`, wait 0.4 s:
   - PlaytimeView visible and DailyView not;
   - the titles are "Playtime Rewards" / "PLAYTIME REWARDS";
   - Slot1..Slot12 all exist;
   - the Pill holder Position X == 231 ± 0.5.
   - Then set Tab back to Daily.
5. **other windows keep Check-UI**: `OpenPage:Fire("Shop")`, wait 0.7 s:
   - HatchBack and HatchFront are not Visible;
   - `Face.Header`, `Face.Title`, `Depth` and `Face.Close` are Visible;
   - `Face.Body.Size.X.Scale == 0.9226` ± 0.001;
   - the Window AspectRatio is not 740/470.
   - Then `CloseWindow:Fire()`.

Expected: all pass. This replaces v1 checks 1-4. The old `Status.Right` countdown check becomes the Card2 label check (D6).

### 8.3 `hatch_containment.lua` (Client datamodel; the Gift window open)

It walks every visible GuiObject under `Window.HatchBack`, `Window.HatchFront` and `Body.GiftPage`. All values are screen px.
- `k(o)` = the product of the UIScales on o and its ancestors.
- `ws` = `HatchBack.SkinScale.Scale`.
- Tolerance TOL = 1 px (pixel snapping).

1. **Containment.** Every non-text, non-`HatchHit` object: its box (the rotated bounding box from AbsoluteRotation; `HatchRadial` objects use the unrotated box), grown by its Border UIStroke `Thickness * k(o)`, must lie inside the parent's box. Objects with `HatchShell` are checked against the MainMenu ScreenGui box instead. **UIStroke Border draws OUTSIDE the box**, which is why the box is grown.
2. **Padding** (layout pass only): objects with `HatchPad` need an unstroked distance to the parent edges of at least `HatchPad * k(parent)` on the left, top and right, and `HatchPadBottom` (or HatchPad) on the bottom.
3. **Tiles:** within each `HatchTile` group (row2, grid, chips), the stroked boxes never intersect. In the layout pass, the unstroked gap is at least `HatchGap * k(parent)`.
4. **Hits:**
   - every `HatchHit` button lies inside the Window box, and no two of them overlap (by more than TOL);
   - `PlayerGui:GetGuiObjectsAtPosition(x, y)` at the centre of `Card1.Face.Button`, `CloseHit`, `HitPlaytime` and `Card1.Hit` (point at card x + 20, y + 20) returns that button as the first GuiButton in the list.
5. **Text:** every TextLabel with text:
   - `TextScaled == false`;
   - `TextFits == true`;
   - `FontFace.Family == Font.fromEnum(Enum.Font.GothamBlack).Family`;
   - the glyph width `TextService:GetTextSize(Text, TextSize, GothamBlack).X * k`, placed by alignment and grown by the stroke `Thickness * k`, lies horizontally inside the label's parent;
   - on-screen size `TextSize * k >= HatchMin * ws - 0.01`.

**Passes.** Set GiftPage `HatchTestPulse = 1` for the layout pass (checks 1-5). Set it to `1.05` for the pulse-peak pass (checks 1, 3 overlap, 4). Clear it after.

**Run matrix.** Close and reopen the window between scale changes. States are set with `ServerStorage.StreakDebug` on the Server; `today = StreakToday`.

| # | State setup | Tab | `HatchTestScale` |
|---|---|---|---|
| A | fresh (Day 1 CLAIM) | Daily | none (native 1.18), 0.7106, 0.6787, 1.0982 |
| B | `set p, 2, today-1` (mid: 1-2 claimed, 3 CLAIM) | Daily | none, 0.7106 |
| C | `set p, 3, today` (next: 4 TOMORROW) | Daily | none, 0.7106 |
| D | `set p, 6, today-1` (Day 7 CLAIM) | Daily | none |
| E | `set p, 7, today` (week done) | Daily | none |
| F | client-only: `PlaytimeStart = now - 16*60`, `PlaytimeClaimed = "1,2"` | Playtime | none, 0.7106 |

Expected: 0 fails in every run. Paste the per-run summary lines into the ledger.

### 8.4 Hover, press and real input (PC)

- Optional `user_mouse_input` move or click on `Card1.Face.Button` only, using the AbsolutePosition centre. Never click outside the window: a miss walks the character (memory gotcha).
- Expected: ButtonScale shows 1.04 on hover; the claim works through a real click in state B.
- If the owner is playing, skip this and note it.

### 8.5 `hatch_assets.lua` (Client datamodel)

`ContentProvider:PreloadAsync(ids, cb)` over every id in section 6 (the PotionConfig, EGG_ICONS and IndexConfig.PORTRAITS values are read from the modules).

Expected: `failed 0`. If 106606523697579 fails, apply the clock fallback of section 6.

### 8.6 `hatch_chrome_snapshot.lua` (Client datamodel; "another window unchanged")

It opens Shop, Rebirth, Index and Settings in turn (`OpenPage:Fire`, wait 0.7 s, dump, `CloseWindow:Fire`, wait 0.4 s).
- The dump covers `Window` and its descendants, sorted by Name then ClassName.
- It skips `HatchBack`, `HatchFront` and every child of Body whose name matches `Page$` or equals `Message` (page content is not chrome).
- Recorded per object:

| Class | Properties |
|---|---|
| GuiObject | Visible, Size, Position, AnchorPoint, Rotation, ZIndex, BackgroundColor3, BackgroundTransparency, ClipsDescendants, AbsolutePosition/AbsoluteSize (rounded) |
| Text | Text, TextColor3, TextSize, TextScaled |
| Image | Image, ImageColor3, ImageTransparency |
| UIStroke | Enabled, Thickness, Color, Transparency |
| UICorner | radius |
| UIGradient | Color, Transparency, Rotation |
| UIAspectRatioConstraint | AspectRatio |
| UIScale | Scale |

- The first line is the viewport size.
- **Procedure:**
  - BEFORE the build (Task 0): save the output as `hatch_chrome_before.txt`.
  - AFTER the build: save `hatch_chrome_after_fresh.txt` (fresh session) and `hatch_chrome_after_gift.txt` (`OpenPage:Fire("Gift")` first, wait 1 s, then the dump).
- **Expected:** both AFTER files are identical to BEFORE when the viewport is identical. A hovered button's `ButtonScale` is the only allowed difference; keep the mouse off the window, or re-run.

### 8.7 StreakTests (must stay green)

- Edit: `require(game.ServerStorage.StreakTests:Clone()).pure()` -> 24/24.
- New fresh Play session, Server datamodel: `require(game.ServerStorage.StreakTests).live(game.Players:GetPlayers()[1])` -> all groups pass (20/20).
- Run `live` in its own session, never in the session used for 8.2-8.6. `get_console_output` must show no StreakServer, StreakClient or PlaytimeClient errors.

### 8.8 Screenshots (`screen_capture`; save to `docs/plans/tests-2026-10-21/hatch_*.png`)

| File | Setup |
|---|---|
| `hatch_pc_mid.png` | State B, native scale. Compare with `B_hatchnight_pc.png` |
| `hatch_pc_next.png` | State C (TOMORROW timer) |
| `hatch_pc_day7_claim.png` | State D |
| `hatch_pc_weekdone.png` | State E |
| `hatch_pc_lost.png` | `set p, 4, today-3`, reopen within 4 s (LOST! label) |
| `hatch_pc_flash.png` | State D + `StreakDebug failNext "pet"` + TestPress 7 ("PETS FULL!") |
| `hatch_cel_1.png`, `hatch_cel_2.png`, `hatch_cel_3.png` | `StreakCelebrate.TestCelebrate:Fire()`, captured at about 0.8 s (wobble), 1.6 s (top flying, pet rising) and 2.5 s (final) |
| `hatch_pc_playtime.png` | State F |
| `hatch_phone_mid.png`, `hatch_phone_next.png`, `hatch_phone_playtime.png` | `HatchTestScale = 0.7106`; crop the window and compare with `B_hatchnight_phone.png` |
| `hatch_shop_before.png` / `hatch_shop_after.png` | Shop window, the same viewport |
| `hatch_pc_hover.png` | Optional (8.4) |

- **Phone emulator (owner only):** in Studio, Test > Device, pick an iPhone in landscape (or a custom 844 x 390), then Play. Run 8.3 with no `HatchTestScale`.
  - Expected: the window sits right of the tiles and pills; nothing is under the notch; s is about 0.71.
  - The builder only asks the owner and then captures `hatch_phone_emulator.png`.
- **Visual review:** a Haiku visual reviewer checks each set against the mockups and the owner's complaint. Fix and re-shoot until it approves.

---

## 9. Build order

- [ ] **Task 0: Pre-flight and BEFORE evidence.**
  - Edit state; `TestFreshSave == true`.
  - Play (Client): run `hatch_chrome_snapshot.lua` and save `hatch_chrome_before.txt`.
  - Capture `hatch_shop_before.png` and the current Gift window (`hatch_gift_before.png`). Stop Play.
- [ ] **Task 1: Backups.** Create Folder `ServerStorage._Backup_HatchNight.Before` with clones of StreakClient, PlaytimeClient, MenuController, BrickUI (with its children) and StreakTests.
  - Set `Enabled = false` on the LocalScript clones.
  - Strip every CollectionService tag from each clone and its descendants.
  - Root attributes:
    - `WasEnabled = "StreakClient,PlaytimeClient,MenuController"`;
    - `HowToRestore = "Delete ReplicatedStorage.BrickUI.Hatch; replace the 5 scripts with these copies (Enabled = true for the LocalScripts); MenuController goes back under StarterGui.MainMenu"`.
  - On disk, copy `streak_client.lua` to `streak_client_v1.lua`.
- [ ] **Task 2: BrickUI.Hatch + the BrickUI hook.**
  - Write section 7.2 and the 7.1 lines.
  - Write `hatch_pure.lua` and run it in Edit (RED before the module exists, then GREEN).
  - **Probe:** in a throwaway Play test, a Frame with a 10 px UIStroke under a UIScale of 2 must render a 20 px outline (UIStroke scales with UIScale). Write the result in the ledger, then delete the probe.
- [ ] **Task 3: MenuController skin hook** (7.3).
  - Play: open Shop, Rebirth, Index and Settings; they must look unchanged (quick look).
  - Open Gift: the night shell must show (the Gift content is still old at this point; that's expected).
- [ ] **Task 4: PlaytimeClient** (7.4).
  - Play: the PLAYTIME tab renders; claim slot 1 after 1 min; Skip All prompts (Studio).
- [ ] **Task 5: StreakClient** (7.5).
  - First do the 5.5 Reference step (ledger).
  - Play: the states render; TestPress claims; the celebration plays via `TestCelebrate`.
- [ ] **Task 6: Tests.**
  - Write `streak_client.lua` v2, `hatch_containment.lua`, `hatch_assets.lua`; update `StreakTests.CLIENT_SRC`.
  - Run 8.2, 8.3 (the whole matrix), 8.5 and 8.6 in one session; 8.7 in a new session.
  - Fix until all green.
- [ ] **Task 7: Screenshots and review.**
  - 8.8 plus the visual reviewer loop.
  - Set `TestFreshSave = false` only after the last Play test of the day (memory rule).
- [ ] **Task 8: Wrap-up.**
  - Ledger summary.
  - Update memory `roblox-login-streak.md` (HATCH NIGHT Gift window, new test files) and add a pointer in `check-ui-skill.md` (the Gift window uses the Hatch skin).
  - Tell the owner: **Save + Publish** (File > Publish to Roblox), and the optional bat upload decision.

---

## 10. Risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | Shared chrome: a missed restore would change Shop, Rebirth, Index or Settings. | `saved` covers every property the hook touches (8 values + 5 Visible flags). Task 0 / 8.6 snapshot diff (fresh and after Gift). Check 5 of 8.2. |
| 2 | HatchFront covers the window and could block clicks. | Only `CloseHit` is a button in it; everything else is non-Active. 8.3 check 4 (GetGuiObjectsAtPosition) + 8.4 real click. |
| 3 | UIStroke not scaling with UIScale would make outlines too thin or thick. | Task 2 probe. If it fails, set strokes to `logical * scale` in the `SkinScale`/`CanvasScale` binders (store the logical width in attribute `HatchStroke`). |
| 4 | Text metrics: GetTextSize (enum) vs the rendered FontFace. | Section 0 table measured in-engine. `H.fit` plus the TextFits/width checks catch any drift. |
| 5 | Clock 106606523697579 is third-party; it may not load or may get moderated. | 8.5 preload. Fallback = hide the clock and centre the timer (section 6). No upload. |
| 6 | CanvasGroup (celebration TopHalf) may render blurry or not render on low-end devices. | Small texture (182 x 106). If artefacts show in `hatch_cel_2.png`: make TopHalf a ClipsDescendants Frame, drop its rotation (fly straight up, hide at the end) and log it. |
| 7 | ClipsDescendants ignores rotated children (hover tilt, flying shards). | Tilted icons stay well inside the face. Shards live in `Fx`, clamped inside the canvas. Rays use `HatchRadial`. |
| 8 | Pulse margin: the CLAIM button at 1.05 leaves 0.7 logical px above the card face bottom. | 8.3 pulse-peak pass. If a fail shows up from pixel snapping, lower the pulse amplitude to 1.04 (spec allows up to 1.06; never higher). |
| 9 | Phone: the window shifts right to clear the tiles and pills, so it isn't centred. | Intended (D5). The owner can judge it on the emulator screenshot. |
| 10 | 667x375 phones get 10.9 pt minimum text (below the spec's 11.4, which was for 844x390). | Accepted. Cheapest fix if the owner wants it: allow s up to 0.70 by also letting the window cover the top 6 px. Not planned. |
| 11 | `workspace.HalloweenDecor` streaming / timing. | It is a Folder (replicated). The theme is re-read on every open. `workspace` attribute `HatchBand` overrides it. |
| 12 | The Edit require cache would test an old Hatch module. | Always require a `:Clone()` in Edit. Play tests get a fresh require. |
| 13 | Another agent's Play session or the owner playing. | `get_studio_state` before each step; never stop someone else's Play; tests are read-only on GUI. |
| 14 | A Hatch module error. | BrickUI's pcall keeps every other window alive. The Gift page then fails to build; `get_console_output` shows `[BrickUI] Hatch skin not loaded`. |
| 15 | Instance count (about 650 GUI objects) and RenderStepped cost. | Built once. Loops return early when hidden. Text is re-fitted only on change. |
| 16 | Late-game numbers wider than measured. | Worst cases measured (`+12.5Qa SPEED`, `$7.25Qa`); fit steps down to 16. The containment test flags anything else. |

---

## 11. Owner actions (after the build)

1. **Save + Publish** (File > Publish to Roblox). Nothing is live until then.
2. **Optional:** check the phone layout in the Studio device emulator (Test > Device, iPhone landscape).
3. **Optional, owner's call:** upload the bat sticker for the Halloween band (section 6). Without it the band is clean, with no bats.
4. **Phase 2 (later):** say the word to restyle Shop, Rebirth, Index and Settings in HATCH NIGHT. That is `WINDOW_SKIN = "Hatch"` plus a canvas rebuild of each page with the same helpers.
