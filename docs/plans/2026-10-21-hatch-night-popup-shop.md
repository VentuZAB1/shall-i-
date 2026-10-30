# HATCH NIGHT Starter Pack popup + Shop: implementation plan (2026-10-21)

> **For the builder (Opus):** follow this plan task by task. Every number here is final and matches the mockups.
> If something in Studio contradicts a number, stop and write the conflict in the ledger
> (`docs/plans/2026-10-21-hatch-night-popup-shop.progress.md`) before changing anything.
> Pipeline (owner rule): this plan -> Haiku plan reviewer -> build -> Haiku visual reviewer per screenshot set -> fixes -> Haiku lineup reviewer.

**Goal.** This is rollout step 1 of HATCH NIGHT phase 2 (owner-approved order): rebuild the **Starter Pack popup** (`PlayerGui.StarterPackUI`) and the **Shop window** (`MainMenu ... Body.ShopPage`) in the HATCH NIGHT style.
- Every buy path, the gifting, ScrollTo, analytics, live prices and the paid-random-item odds keep working.
- Rebirth, Index and Settings stay **exactly** as they are, and the Gift window stays exactly as built.

**The owner's acceptance test** is the same as for the Gift window: "overlaps, corners outside boxes, cramped text, basic". After this build:
- nothing overlaps;
- every outline is inside its box;
- every line of copy is at most 83 % of its box;
- prices are the biggest text on every card (22-32 logical px).

The art is frameless juicy stickers on the night canvas, and the CTAs are gold.

**Sources (read before building):**
- Spec: `docs/specs/2026-10-21-slingshot-ui-style.md`, sections 2, 4 and 6.
- The Gift plan, `docs/plans/2026-10-21-hatch-night-gift-window.md`, with its `.review.md` and `.visual-review.md`. This plan reuses its conventions (section 4.0), the fit rule (section 3), the test files and the lessons (MUST/SHOULD lists).
- **Mockups (the builder must match them):** `docs/plans/style-2026-10-21/popup_shop/`
  - Popup: `popup_pc.png`, `popup_phone.png`, `popup_restricted_pc.png`, `popup_restricted_phone.png`, `popup_thanks_pc.png`, `popup_error_pc.png`, `popup_urgent_pc.png`.
  - Shop: `shop_top_pc.png`, `shop_top_phone.png`, `shop_speed_pc.png`, `shop_potions_pc.png`, `shop_potions_phone.png`, `shop_bottom_pc.png`, `shop_gift_pc.png`, `shop_gift_phone.png`.
  - `shop_long.png` is the whole scroll list at 1:1 logical px, with each section's y.
  - `sheet.png` holds the button states, tags and rail tabs.
  - Sources: `popup_shop.html` + `engine.js` (the same recipe as `dirB_hatchnight.html` / `common.js`). Run `bash render.sh qa` to re-render; the QA output is in `qa_report.txt`.
  - **QA result:** 0 OUT, 0 OVERLAP, 0 gap < 8, 0 text overflow. Every line of copy is at most 83 % of its box (GothamBlack estimate). Minimum text is 18.9 px on PC and 11.4 px on the 844x390 phone.
  - The art is stand-in art: the Magma egg is `egg.png` tinted, two odds portraits are other pets, and the treadmill icon is a drawn chevron. The build uses the real ids in section 4.0.
- Old look:
  - Popup: `docs/plans/tests-2026-10-21/starter_popup_v3_*.jpg`.
  - Shop: `docs/plans/hatch-night-build/hatch_shop_before.jpg`.
- Code read for this plan: ShopClient, StarterPackClient, StarterPackHud (top + the popup contract), MenuController, BrickUI (tail), BrickUI.Hatch, SpeedBoostCards, ShopConfig, StarterPackConfig, CreatureConfig (odds lists), PlaytimeClient (canvas pattern), PetsEggsUI (GET MORE). Read-only.

**Out of scope:**
- Every server script: ShopServer, StarterPackServer, Receipts, Analytics server.
- ShopConfig, StarterPackConfig, SpeedBoostCards, StarterPackHud, PetsEggsUI, StreakClient, PlaytimeClient.
- Every other window.

---

## 0. Decisions (read first)

| # | Decision | Why |
|---|---|---|
| D1 | The Shop gets the per-page skin through `BrickUI.PAGE_SKIN = {Gift = "Hatch", Shop = "Hatch"}`. MenuController changes in 1 line: `hatch.setTheme(H.bandTheme(name))`. | The skin hook already exists (Gift). Rebirth, Index and Settings fall through to `WINDOW_SKIN = "CheckUI"` untouched. |
| D2 | The Shop and the popup use a new band theme, **`Shop`**: magenta-pink, `(255,96,196) -> 0.55 (255,36,150) -> (220,0,100)`, teeth `(220,0,100)`, no bats. `H.bandTheme(page)` returns, in order: workspace `HatchBand` (the test override); `H.PAGE_BAND[page]` (Shop); the seasonal Pumpkin / HatchGold (Gift, as today). | The spec says "other pages keep their own band colours". The Shop's Check-UI header was magenta, and the Starter Pack HUD art is magenta. With Pumpkin on Gift and magenta on the Shop, the two windows are told apart at a glance. Owner's call 1 can switch the Shop to Pumpkin for Halloween. |
| D3 | **The popup is a full HATCH NIGHT window** (740 x 470 logical, the same chrome helper `H.windowChrome` as Gift), modal and centred in MainMenu's safe box (`H.fitWindow(..., leftClear 0)`). | One window size and one look across the game. The bigger canvas gives the BUY CTA 492 px and a readable odds strip (owner: big prices, juicy art). |
| D4 | **The Shop's tabs become a vertical rail INSIDE the window** (x 10..130), replacing the side tiles outside the window's right edge. | On a 844x390 phone the fitted window ends at x 670 of 732: there is no room outside it. A vertical rail keeps the side-tab muscle memory and leaves the most vertical room for content (386 logical). Owner's call 2 offers top tabs instead. |
| D5 | **One long scroll, tabs scroll to their section** (today's behaviour). The section you look at lights its tab, and `ScrollTo` works as today. Layout is manual and in logical px (section 4.4), not a UIListLayout. | Behaviour kept. Logical y positions make `scrollTo` exact at every scale, and they avoid UIListLayout's AbsoluteContentSize-under-UIScale double scaling. |
| D6 | **SpeedBoostCards stays byte-identical.** The Shop reads `SpeedBoostCards.CARDS` (its data: `title()` / `sub()` functions, `buy` args, `id`, `price`, `best`) and draws HATCH NIGHT cards with `H`. `SpeedBoostCards.build` is no longer called. | `script_grep` shows the live `UpgradeClient` does **not** use SpeedBoostCards: the stall's SPEED BOOSTS strip was removed 2026-10-06, and only backups reference it. So nothing changes for the stall either way. The stall's own HATCH NIGHT rebuild (rollout step 3) can reuse the same data. |
| D7 | Shop cards are `H.shellCard`s **without the full-card Hit** (new `opts.noHit`). Only the price buttons buy. | A stray tap on a card must never start a Robux prompt. |
| D8 | All Robux purchases are **gold** `H.priceButton`s: a white Robux hex (`ShopConfig.ROBUX_ICON` 109535585247625) with an ink drop shadow, plus the price, laid out as one centred group from `H.textWidth`. In-game money buys (treadmill $) are **lime**. Gifting is **violet**. OWNED / MAX are **silver**. Refusals are **red** for 1.3 s. | Spec purchase colour. On gold, a white glyph with an ink shadow reads better than the grey/green glyph (visual review SHOULD 12). |
| D9 | Price sizes: popup BUY 32, wide cards and Starter card 28, treadmill 26, passes 24, small cards and picker 22. Copy minimum 16 (the Gift rule). | "The Shop is the money page": the price is the biggest text on every card. Phone 0.7106: 22.7 / 19.9 / 18.5 / 17.1 / 15.6 pt. |
| D10 | The **Starter Pack Shop card** stays owned by StarterPackClient, through a new slot contract. ShopClient creates `List.StarterSlot` (a 576 x 128 frame, hidden). StarterPackClient builds the card inside it and sets `StarterSlot.Visible = active()`. ShopClient re-lays the list out when the slot's Visible changes (every section moves 142). | The logic (timer, `active()`, `setOpen`) stays in one script. The slot keeps the card at the very top only while the 24 h offer runs, as today. |
| D11 | **No UIScale on the popup Holder or its ancestors.** The open / close animation tweens `Holder.Size` (0.85x -> 1x, Quad Out 0.2 s), like MenuController. | `H.windowChrome`'s SkinScale and the canvas's CanvasScale are bound to `Holder.AbsoluteSize.X / 740`. A UIScale pop would scale them twice. |
| D12 | Pulses: the popup BUY and the Starter card BUY breathe **1.00..1.02** (1.6 s; new `glossButton opts.pulseAmp = 0.01`). Their hover is 1.02. Nothing else in the Shop pulses. | The CTA gets a gentle beat. At 1.02 the containment margins hold (section 4.12). Spec 2.1.4: only buttons pulse, never cards. |
| D13 | **Nothing runs while closed.** The Shop refresh runs only while the page is shown (a token loop). Analytics "shop on screen" becomes event-driven, which removes the forever 0.5 s poll. The popup's rays RenderStepped connects only while `StarterPackUI.Enabled` (perf review M-4). StarterPackClient's 0.5 s forever loop becomes an expiry timer plus a 0.5 s ticker that runs only while the popup or the Shop card is visible (M-5). | Owner's lag rule. Proven by `hatch_shop_perf.lua` (section 7.7). |
| D14 | **Tests never open a real Robux prompt.** Studio-only dry run: the attribute `TestDryRun = true` on ShopPage / StarterPackUI makes every buy path record its exact remote args in `TestLastBuy` (JSON) instead of invoking. The receipt side keeps using the existing server tools (`ServerStorage.TestReceipt`, `StarterDebug`). | Owner rule: never click real Robux prompts. It also tests the exact args, which is what "keep every buy path" means. |
| D15 | **Fallback.** If `BrickUI.Hatch` fails to load, ShopClient enables `StarterPlayerScripts.ShopClientLegacy`, a disabled byte copy of today's ShopClient, and returns. MenuController then has no `hatch`, so every page, Shop included, uses Check-UI as today. StarterPackClient without H builds no popup and no `Open` event. The HUD then hides the offer by its own rule ("no odds path = no offer"). | The Shop is the revenue page and must never come up blank. The paid-random-item rule stays safe. |
| D16 | Snapshot filter v2: the chrome snapshot also skips `Window.ShopTabs` and `Body.GiftPicker`, which are Shop content that moves into ShopPage. BEFORE is re-captured with v2 in Task 0. Rebirth / Index / Settings must then be byte-identical. | The old v1 BEFORE file includes those two objects, which the rebuild removes by design. |
| D17 | The **Gift window must not change**: a new `hatch_gift_snapshot.lua` (BEFORE in Task 0, AFTER at the end). Every pre-existing `H` function keeps its default path byte-identical, and new behaviour is opt-in only. | Shared helpers are the main way this work could leak into Gift. |
| D18 | Copy is short and fixed, with no RichText. Pass copy, boost/pack sub-lines and popup lines are tables in the scripts (section 4). | Spec copy rule (11-14 characters per line at 16). TextScaled and RichText are what made the old Shop cramped. |

---

## 1. Files

| Instance | Action |
|---|---|
| `ReplicatedStorage.BrickUI` | 1 line: `BrickUI.PAGE_SKIN = {Gift = "Hatch", Shop = "Hatch"}` (plus the comment "phase 2 step 1: Shop"). Nothing else changes. |
| `ReplicatedStorage.BrickUI.Hatch` | Add the helpers of section 6.2. Additive only; the default path of every existing function stays the same. |
| `StarterGui.MainMenu.MenuController` | 1 line (line 242): `hatch.setTheme(H.bandTheme(name))`. |
| `StarterPlayer.StarterPlayerScripts.ShopClient` | Rewrite the UI (section 6.4). The logic is kept: `robux()` live prices, the buy args, gifting, toasts, refresh math, ScrollTo, analytics. |
| `StarterPlayer.StarterPlayerScripts.ShopClientLegacy` | NEW: a disabled byte copy of today's ShopClient (D15). |
| `StarterPlayer.StarterPlayerScripts.StarterPackClient` | Rebuild the popup UI and the Shop card UI (section 6.5). Logic kept as listed in section 5. |
| `ServerStorage._Backup_HatchNight.Before` | Add `ShopClient_prePopupShop`, `StarterPackClient_prePopupShop`, `MenuController_prePopupShop`, `BrickUI_prePopupShop` (with its `Hatch` child). Task 1. |
| `docs/plans/tests-2026-10-21/` | New: `shop_client.lua`, `starter_popup_client.lua`, `hatch_gift_snapshot.lua`, `hatch_shop_perf.lua`, `hatch_scroll_probe.lua`. Changed: `hatch_containment.lua` (v2: configurable roots, section 7.5), `hatch_chrome_snapshot.lua` (v2 filter), `hatch_pure.lua` (+ section 7.1 checks), `hatch_assets.lua` (+ new ids), `starter_hud_client.lua` (`S.popup` retired: it tests the old popup tree; it is replaced by `starter_popup_client.lua`). Results: `hatch_chrome_before_v2.txt`, `hatch_chrome_after_v2*.txt`, `hatch_gift_before.txt`, `hatch_gift_after.txt`, `hatch_shop_perf_results.txt`. |

---

## 2. Architecture

```
StarterGui.MainMenu (ScreenGui, DO 3, CoreUISafeInsets, IgnoreGuiInset false)
  Window (Hatch pages: Offset size from hatchFit, AR 740/470)
    HatchBack  Z0   night shell (H.windowChrome, unchanged)
    Depth/Face Z1   Check-UI chrome, hidden on Hatch pages (MenuController applySkin, unchanged)
      Body                                   (full face, transparent on Hatch pages)
        GiftPage  [PlaytimeClient]           unchanged
        ShopPage  [ShopClient] Frame 740 x 463 logical, UIScale CanvasScale = Body px / 740, Z3, attrs: ScrollTo, Studio tests
          Rail       recess 10, 66, 120, 386: Pill (lime) + 5 x {Icon, Label, Hit}
          Scroll     ScrollingFrame 134, 66, 596, 386 (bar 8, VerticalScrollBarInset Always)
            List     Frame 0, 0, 584, CanvasH   (content origin = List (4, 4))
              StarterSlot  4, 4, 576, 128  [the card is built by StarterPackClient]; Visible = offer active
              Header_PASSES, Pass_Growth2x .. Pass_Speed2x, Header_SPEED, Double, Boost_Speed15m/Speed3/Speed2h,
              Header_POTIONS, Pack_Money3 .. Pack_Speed10, Header_TREADMILL, Treadmill, Header_EGGS, Eggs
          GiftPicker TextButton 0, 0, 740, 463, Z20 (shade) -> Box (shell card 160, 66, 420, 386) -> Players (ScrollingFrame)
    HatchFront Z2   band (theme "Shop"), crack teeth, icon (Shop tile icon), title "SHOP", red X (CloseHit)
PlayerGui.GiftToast (DO 30) [ShopClient]   Toast (gift) + Granted, restyled text (section 4.11)
PlayerGui.StarterPackUI (DO 22, IgnoreGuiInset true, Enabled = popup open) [StarterPackClient]
  Backdrop  TextButton full screen, ink (8,6,25) 0.45 -> closes
  Holder    TextButton (sinks clicks), AnchorPoint 0.5, Offset size 740 s x 470 s at MainMenu's safe-box centre (section 3)
    HatchBack Z0 / HatchFront Z2  (H.windowChrome(Holder, {bats = false}), theme "Shop", star icon, "STARTER PACK!")
    Canvas    Z1 Frame 740 x 463, UIScale CanvasScale = Holder px / 740
      Hero (centre-anchored, PopScale) {Rays, Glow, potions, Cash, EggOutline, Egg}, EndsIn, EggRow/PotionRow/CashRow,
      OddsCaption, Odds{Odds1..n}, NoThanks, Buy, Fx
  Open (BindableEvent), TestOpen / TestBuy (Studio), attribute Price (read by StarterPackHud)
```

**Rendering and input:**
- These are the Gift rules (ZIndexBehavior Sibling). Every Frame, TextLabel and ImageLabel has `Active = false`. Only GuiButtons take input.
- HatchFront holds only `CloseHit` as a button, so clicks pass through it to the page.
- The popup `Holder` is a TextButton (Text "", transparent, AutoButtonColor false), so a click inside the window never reaches the Backdrop. This is today's trick, kept.

---

## 3. Window fit

### 3.1 Shop: the Gift fit, unchanged

MenuController's existing `hatchFit()` (`H.fitWindow` with HUD clearance) is used unchanged:

| Device (screen) | gui | leftClear | s | Window | cx, cy | Min text (16) | Price 22 / 28 |
|---|---|---|---|---|---|---|---|
| PC 1920x1080 | 1920x1022 | 412.1 | **1.18** | 873.2 x 554.6 | 960, 511 | 18.9 px | 26.0 / 33.0 px |
| PC baseline 1050x620 | 1050x562 | 229.3 | **1.0982** | 812.7 x 516.2 | 635.65, 281 | 17.6 px | 24.2 / 30.7 px |
| Phone 844x390 | 732x346 | 144.3 | **0.7106** | 525.9 x 334.0 | 407.24, 173 | 11.4 pt | 15.6 / 19.9 pt |
| Phone 667x375 | 667x331 | 137.9 | **0.6787** | 502.3 x 319.0 | 389.03, 165.5 | 10.9 pt | 14.9 / 19.0 pt |

The 10.9 pt minimum on the 667x375 phone is the same risk that was accepted for Gift (Gift plan risk 10).

### 3.2 Popup: modal, centred, leftClear 0

```
mm = PlayerGui.MainMenu                          -- CoreUISafeInsets: its box = the safe area below the top bar
s, w, h, cx, cy = H.fitWindow(mm.AbsoluteSize.X, mm.AbsoluteSize.Y, 0)
test = RunService:IsStudio() and gui:GetAttribute("HatchTestScale")   -- Studio switch, as MainMenu's
if type(test) == "number" then s = test; w, h = 740 s, 470 s; cx, cy = mm.AbsoluteSize.X / 2, mm.AbsoluteSize.Y / 2 end
off = mm.AbsolutePosition - gui.AbsolutePosition  -- StarterPackUI ignores the inset: shift into its space
Holder.AnchorPoint = (0.5, 0.5); Holder.Position = fromOffset(off.X + cx, off.Y + cy); Holder.Size = fromOffset(w, h)
```

| Device | mm box | s | Window | cx, cy (mm space) | Min text | BUY @32 |
|---|---|---|---|---|---|---|
| PC 1920x1080 | 1920x1022 | **1.18** | 873.2 x 554.6 | 960, 511 | 18.9 px | 37.8 px |
| PC 1050x620 | 1050x562 | **1.1702** | 866.0 x 550.0 | 525, 281 | 18.7 px | 37.4 px |
| Phone 844x390 | 732x346 | **0.7106** | 525.9 x 334.0 | 366, 173 | 11.4 pt | 22.7 pt |
| Phone 667x375 | 667x331 | **0.6787** | 502.3 x 319.0 | 333.5, 165.5 | 10.9 pt | 21.7 pt |

**When to re-fit:**
- On every open.
- On `workspace.CurrentCamera.ViewportSize` changes while `gui.Enabled`.
- The Size tween in D11 runs from `0.85 * size` to `size`. Close: `size -> 0.85 size` in 0.12 s, then `Enabled = false`.

---

## 4. Geometry (logical px; the mockup numbers)

### 4.0 Conventions, constants, assets

**Conventions:** Gift plan section 4.0 applies unchanged.
- `rect (x, y, w, h)` is top-left. Stickers and gloss buttons are given top-left; the helper centre-anchors them.
- `text(s, x, y, w, size)` is a box of height `size + 2`, fixed TextSize, ink Contextual stroke 2.5.
- Stroke = Border UIStroke, ink, drawn outside the box.
- Test attributes: HatchPad, HatchPadBottom, HatchTile, HatchGap, HatchHit, HatchRadial, HatchShell, HatchMin, HatchHolder. **New:** `HatchBlocker` marks modal click-sinks (the popup Holder, GiftPicker, Box), which the hit checks skip.

**New constants in `H`:**

| Key | Value |
|---|---|
| `H.BAND.Shop` | band `{{0, (255,96,196)}, {0.55, (255,36,150)}, {1, (220,0,100)}}`; fill `{{0, (255,42,154)}, {0.1, (255,36,150)}, {1, (220,0,100)}}`; tooth `(220,0,100)` |
| `H.PAGE_BAND` | `{Shop = "Shop", StarterPack = "Shop"}` |
| `H.PAL.violet` | top (214,128,255), bottom (150,50,220), side (80,20,130), hl (240,200,255), label WHITE |
| `H.ICON.robuxWhite` | `"rbxassetid://109535585247625"` (= `ShopConfig.ROBUX_ICON`) |
| `H.GOLD_TIMER` / `H.RED_TIMER` | ColorSequence (255,240,120) -> (255,170,0) / (255,235,225) -> (255,60,50). These are today's popup timer keys; the HUD test reads the last keypoint. |

**Assets:** no uploads. Every id is already in the game.

| Use | Id / source |
|---|---|
| Popup header star | 93906069548754 (`STAR`, StarterPackClient) |
| Shop header icon | `panel.Icon.Image` (the Shop tile), set by MenuController as for Gift |
| Rail / section icons | FEATURED 93906069548754, SPEED 80829076123513, POTIONS `PotionConfig.TILE_ICON`, TREADMILL 104087244878251, EGGS 135711525932647 (ShopClient constants) |
| Pass icons | `ShopConfig.Passes[i].icon` |
| Potions | `PotionConfig.byKey[key].icon` |
| Eggs | `StreakConfig.EGG_ICONS[StarterEgg]` (popup, card) |
| Cash | 88694661500877 (the popup's / HUD's cash) |
| Odds portraits | `IndexConfig.PORTRAITS[name]` |
| Clock | `H.ICON.clock` (106606523697579, loads in the Gift build) |
| Rays / glow / star / check | `H.ICON.rays`, `.glow`, `.star` |
| Robux | `H.ICON.robuxWhite` |
| Gift | `H.ICON.gift` |

### 4.1 Popup: `StarterPackUI` (face 740 x 463; everything in `Canvas`)

**Chrome:** `H.windowChrome(Holder, {bats = false})`, then `setTheme("Shop")` and `icon.Image = STAR`.
- `setTitle("Starter Pack!")` shows STARTER PACK!; the THANK YOU state shows THANK YOU!.
- `closeHit.Activated -> closePopup`.
- Header geometry is the Gift's 4.2: the band ends at 46 and the teeth at 61.8.

**Hero group:**
- `Canvas.Hero` is a Frame, AnchorPoint 0.5, at centre **(155, 196)** (restricted **(155, 220)**), size 270 x 270, Z 2.
- It has a UIScale `PopScale`.
- The table gives canvas coordinates. The child's Position = canvas xy - (20, 61) (restricted (20, 85)).

| Name | Class | rect (canvas) | Z | Look |
|---|---|---|---|---|
| Rays | ImageLabel | 45, 90, 220, 220 | 1 | `H.ICON.rays`, ImageColor3 (255,150,220), ImageTransparency 0.5, Fit. Rotates 12 deg/s while open. `HatchRadial` |
| Glow | glow | 30, 100, 250, 200 | 2 | `H.AREA_GLOW[StarterArea]` (Magma (255,140,50)); restricted: cash (108,255,90). ImageTransparency 0.35 |
| PotionSpeed (+Shadow) | sticker | 52, 120, 54; Rotation -12 | 3/4 | `byKey.Speed.icon` |
| PotionMoney (+Shadow) | sticker | 64, 212, 60; Rotation -16 | 3/4 | `byKey.Money.icon` |
| PotionHatch (+Shadow) | sticker | 186, 212, 60; Rotation 16 | 3/4 | `byKey.Hatch.icon` |
| Cash (+Shadow) | sticker | 188, 106, 68; Rotation 12 | 3/4 | CASH. Hidden when restricted |
| EggOutline | ImageLabel | 71, 112, 168 (centre-anchored) | 5 | The hero's image, ImageColor3 BLACK (today's ink twin, hero + 8) |
| Egg | ImageLabel | 75, 116, 160 (centre-anchored) | 6 | `S.EGG_ICONS[eggKind()]`. Restricted: CASH (the cash is the hero) |

Restricted: every hero child moves +24 in y; Cash is hidden; the hero image is CASH.

**Rotated extents (canvas):**

| Item | x | y |
|---|---|---|
| PotionMoney | 56.9..131.1 | 204.9..279.1 |
| PotionHatch | 178.9..253.1 | 204.9..279.1 |
| PotionSpeed | 47..111 | 115..179 |
| Cash | 181.7..262.3 | 99.7..180.3 |

Everything is left of the rows (318) and above the caption (288). The timer's stroked bottom is 97, so the gap to the Cash top is 2.7.

**Other canvas elements:**

| Name | Class | rect | Z | Look |
|---|---|---|---|---|
| EndsIn | text | ("ENDS IN 23:59:48", 10, 70, 290, 22), stroke 3 | 6 | White plus UIGradient 90 `H.GOLD_TIMER`; `H.RED_TIMER` under 1 h. Text `"ENDS IN " .. P.clockText(left)`. No background (owner) |
| EggRow / PotionRow / CashRow | chip (corner 14) | 318, 66 / 140 / 214, 412, 66 | 4 | `H.chip(..., 66, 14)`; `HatchTile "rows"`, `HatchGap 8`, `HatchPad 8`. Restricted: PotionRow at y **149**, CashRow at **223**, EggRow hidden |
| row.Icon (+Shadow) | sticker | 10, 8, 50 | 2/3 | Egg row `EGG_ICONS[eggKind]`, potion row `PotionConfig.TILE_ICON`, cash row CASH |
| row.Line1 | text | (…, 70, 10, 332, 22), left | 2 | White: `"BIG " .. AREA:upper() .. " EGG"`, `potionCount() .. "x EVERY POTION"`, `"1 HOUR OF INCOME"` |
| row.Line2 | text | (…, 70, 38, 332, 16), left; the cash row uses (70, 36, 332, 20) | 2 | Egg: `Format(kg) .. " KG - A RANDOM PET!"`, GOLD_TXT. Potion: `"MONEY + HATCH + SPEED"`, LAV. Cash: `"+$" .. Format(cashAmount())` @20, (150,255,60) |
| OddsCaption | text | ("EGG ODDS - HATCHES ONE OF THESE:", 10, 288, 720, 16) | 4 | LAV |
| Odds | recess, corner 20 | 10, 310, 720, 62 | 4 | `H.recess(canvas, "Odds", 10, 310, 720, 62, 4, 20)`. `HatchPad 8` |
| Odds<i> | Frame | (i-1) * cw, 0, cw, 62 with `cw = 720 / n` | 2 | Transparent. Children below |
| NoThanks | glossButton dusk | 10, 384, 212, 60; d 4, r 12, ol 2.5 | 5 | "NO THANKS" @20, LAV. `HatchTile "btns"`, `HatchGap 8`, `HatchPad 8` (bottom 3). Hover 1.04 |
| Buy | priceButton gold | 238, 384, 492, 60; d 4, r 12 | 5 | `pre = "BUY"`, glyph 34, price @32. hoverScale 1.02, pulseAmp 0.01. `HatchTile "btns"` |
| Fx | Frame | 0, 0, 740, 463 | 20 | Shards (thanks) |

**Odds cell layout** (n = `#P.odds(...)`; today n = 5 for every egg):

| n | Pet sticker | Pct text (@20, left) |
|---|---|---|
| ≤ 5 (cw ≥ 144) | (6, 4, 54) | (62, 21, cw - 66, 20) |
| 6 (cw 120) | (4, 9, 44) | (52, 21, cw - 56, 20) |
| ≥ 7 | (3, 12, 38) | (44, 21, cw - 47, 20) |

- `H.fit` steps the pct size down to its minimum of 16.
- **Secret:** the pet sticker gets ImageColor3 BLACK (a silhouette). Add a `Secret` text "?" (pet box, y + 14, size 26) with a `H.GOLD_TIMER` gradient. The Pct text also gets the gold gradient.
- Pct = `P.pctText(o.pct)`.

**Vertical stack:** header 0..46 (teeth to 62), rows 66..280, caption 288..306, odds 310..372, buttons 384..444, bottom margin 8 to 452.

**Popup states:**

| State | Title | Buy | NoThanks | Other |
|---|---|---|---|---|
| Normal | STARTER PACK! | gold: BUY + Robux + price, pulsing 1.00..1.02 | dusk | Rays turn |
| Restricted (`StarterRestricted ~= false`) | same | same | same | No egg row, no caption, no odds. The cash is the hero (the +24 layout). PotionRow says `10x EVERY POTION` |
| Last hour | same | same | same | EndsIn gets RED_TIMER |
| Refusal (Buy returned false) | same | **red**, `H.fit(label, {MSG:upper(), "TRY AGAIN"})` @32, no glyph, no pulse, for 1.4 s, then restored | same | Server reasons today: "Offer ended" -> OFFER ENDED, "Owned" -> OWNED, others upper |
| Owned (`StarterPack` true while open) | THANK YOU! | **lime** "OWNED!" @32, no pulse | hidden | `Hero.PopScale` 1 -> 1.15 -> 1 (Back 0.35 s); `H.shards(Fx, 155, 196)`; HatchWin; close after 1.6 s (as today) |

### 4.2 Shop page and rail

**ShopPage:** `H.frame(body, "ShopPage", 0, 0, 740, 463, nil, 3)`, `Visible = false`, `H.bindCanvasScale(page, body, 740)`.

**Rail:** `H.recess(page, "Rail", 10, 66, 120, 386, 4, 20)`, `HatchPad 8`. There are 5 slots, `T_i = 3 + 76 (i - 1)`.

| Name | Class | rect / centre | Z | Look |
|---|---|---|---|---|
| Pill | glossButton lime | rect 3, T_active, 114, 76; d 3, r 16, ol 2 | 3 | `faceFrame = true`, `hoverScale = 1` (the gloss brightens instead; Gift review MUST 2), no label. `HatchPad 3`, `HatchPadBottom 3`. The holder tweens to the slot centre (60, T + 38) in 0.15 s Quad Out; it snaps on open |
| Icon<i> (+Shadow) | sticker | 40, T + 7, 40 | 5/6 | The section icon; the treadmill uses TREADMILL_ICON |
| Label<i> | text | (TAB, 3, T + 51, 114, 16) | 7 | WHITE on the active slot, LAV_DIM otherwise. Tabs: FEATURED, SPEED, POTIONS, TREADMILL, EGGS |
| Hit<i> | TextButton | centre (60, T + 38), 120 x 76 | 8 | Transparent, Text "". `HatchHit`. Activated -> SFX Click, `scrollTo(section, true)`. Hover: icon Rotation -8 (Back 0.15 s), label WHITE; the active slot's Pill gloss brightens (`btn.bind(hit)` filter) |

Hit boxes are contiguous (69..449 in page y) and never overlap. At 0.7106 a tab hit is 85 x 54 pt.

**Scroll:** ScrollingFrame `Scroll` at rect 134, 66, 596, 386, Z 3.
- BackgroundTransparency 1, BorderSizePixel 0.
- `ScrollBarThickness 8`, `ScrollBarImageColor3 (167,159,224)`, `ScrollBarImageTransparency 0.3`.
- `VerticalScrollBarInset Always`, `ScrollingDirection Y`, `ElasticBehavior WhenScrollable`.
- CanvasSize = `(0, CanvasH)` in the unit the probe finds (section 7.2).
- The visible content width is 588. The bar sits at page x 722..730, 10 from the window edge.

**List:** Frame `List` at (0, 0, 584, CanvasH), transparent.
- **Content coordinates:** every rect in sections 4.3 to 4.9 is relative to the content origin. The instance Position = (x + 4, y + 4) in List.
- So every 2.5 outline stays inside List (4 px margin), and the right edge (580 + 2.5) clears the bar at 588.

**Section header:** Frame `Header_<KEY>` at content (0, y, 576, 30).

| Child | rect | Look |
|---|---|---|
| Icon sticker | (0, 2, 26) | The section icon |
| Title text | (KEY, 34, 5, 200, 20), left | Section colour: PASSES (255,214,60), SPEED (90,220,255), POTIONS (205,130,255), TREADMILL (255,150,70), EGGS (120,255,120) |
| Line Frame | (34 + tw + 12, 14, 576 - 46 - tw, 2) with `tw = H.textWidth(KEY, 20)` | `H.RECESS.line`, BackgroundTransparency 0.65, corner 1 |

### 4.3 Shop list layout (content y; `shop_long.png`)

| Item | y, Starter slot shown | y, slot hidden (-142) |
|---|---|---|
| StarterSlot (576 x 128) | 0 | hidden |
| Header_PASSES | 142 | 0 |
| Pass row 1 / row 2 (x 0 and 292; 284 x 150) | 178 / 336 | 36 / 194 |
| Header_SPEED | 504 | 362 |
| Double (576 x 124) | 540 | 398 |
| Boosts (x 0 / 195 / 390; 186 x 176) | 672 | 530 |
| Header_POTIONS | 866 | 724 |
| Pack row 1 (x3 packs) / row 2 (x10 packs) (x 0 / 195 / 390; 186 x 176) | 902 / 1086 | 760 / 944 |
| Header_TREADMILL | 1280 | 1138 |
| Treadmill (576 x 124) | 1316 | 1174 |
| Header_EGGS | 1458 | 1316 |
| Eggs (576 x 124) | 1494 | 1352 |
| Content height H | 1626 | 1484 |
| CanvasH = H + 8 | 1634 | 1492 |
| Max scroll = CanvasH - 386 | 1248 | 1106 |

- **Spacing:** header to cards 6 (header 30 + 6); between cards 8 (passes) or 9 (3-across, 3 x 186 + 2 x 9 = 576); between sections 18.
- **Tiles:** `HatchTile` "passes" / "boosts" / "packs" with `HatchGap 8`.
- **scrollTo(name):** PASSES -> 0 (the very top, Starter card included, as today). Every other section -> its header y. Clamp to [0, max scroll].
- **Active tab:** the last header with `y <= scrollY + 135` (0.35 x 386). If `scrollY >= max - 2`, it is EGGS.

### 4.4 The Starter Pack card (StarterPackClient builds it inside `List.StarterSlot`)

- `card = H.shellCard(slot, "Card", 0, 0, 576, 128, {noHit = true, grad = {(110,36,150), (60,22,104)}})`.
- Then `card.holder:SetAttribute("HatchPad", 0)`: the slot positions it.
- Face 576 x 123.

| Name | Class | rect | Z | Look |
|---|---|---|---|---|
| Face.Ring | Frame | 3, 3, 570, 117 | 1 | Transparent, corner 11, stroke 3 (255,214,90). An inward gold rim, not an outer glow |
| Face.Rays | ImageLabel | 12, 2, 118, 118 | 1 | Rays, ImageColor3 (255,150,220), ImageTransparency 0.55. **Static**. `HatchRadial` |
| Face.Glow | glow | 14, 6, 116, 108 | 1 | Area colour, ImageTransparency 0.6 |
| Pop.PotionMoney / PotionHatch | sticker | 8, 72, 36, Rotation -14 / 100, 72, 36, Rotation 14 | | |
| Pop.Cash | sticker | 96, 10, 40, Rotation 10 | | Hidden when restricted |
| Pop.EggOutline / Pop.Egg | ImageLabel | 26, 14, 88 / 28, 16, 84 | | Black twin / egg. Restricted: the hero is CASH |
| Title | text | ("STARTER PACK", 148, 12, 240, 24), left | 3 | White |
| Line1 | text | (`potionCount() .. "x EVERY POTION"`, 148, 44, 240, 16), left | 3 | White |
| Line2 | text | ("+ 1 HOUR OF INCOME", 148, 64, 240, 16), left | 3 | LAV |
| Line3 | text | (`"+ BIG " .. AREA .. " EGG!"`, 148, 84, 240, 16), left | 3 | GOLD_TXT. Hidden when restricted |
| Buy | priceButton gold | 404, 20, 160, 56; d 4, r 12 | 4 | glyph 30, price @28, hover 1.02, pulseAmp 0.01 (pulses while visible). Activated -> SFX Click, `setOpen(true)`. **It only opens the popup** (odds rule) |
| Timer | text | ("23:59:48 LEFT", 404, 86, 160, 16), stroke 2.5 | 4 | `H.GOLD_TIMER` gradient; RED under 1 h; no background |

The rotated sticker extents stay inside 4..140 x 6..112. The text column starts at 148.

### 4.5 Pass card (x4; 284 x 150, face 145; `Pass_<key>`)

| Name | rect | Look |
|---|---|---|
| Face.Glow | 6, 6, 104, 96 | `p.face[1]`, ImageTransparency 0.55 |
| Pop.Icon (+Shadow) | sticker 14, 12, 84 | `p.icon` |
| Title | text (…, 106, 14, 170, 22), left | White |
| Line1 / Line2 | text (…, 106, 44, 170, 16) / (…, 106, 63, 170, 16), left | LAV |
| Gift | glossButton violet 10, 98, 54, 40; d 4, r 10 | Gift sticker (13, 4, 28) on the face. Activated -> `openGift(p)`. `HatchTile "passbtn"`, `HatchGap 8` |
| Buy | priceButton gold 76, 98, 198, 40; d 4, r 10 | glyph 26, price @24. **Owned:** `setWord("OWNED", "silver")` @20, Active false. `HatchTile "passbtn"`, `HatchPad 8` (bottom 3) |
| BuyHit | TextButton, centre (175, 117), 198 x 50 | Invisible (`input =` this hit drives the button motion). 35 pt tall on phones |

**PASS_COPY** (fixed, ShopClient):

| Key | Title | Line 1 | Line 2 |
|---|---|---|---|
| Growth2x | x2 GROWTH | EGGS HATCH | x2 FASTER! |
| Money2x | x2 MONEY | PETS EARN | x2 MONEY! |
| VIP | VIP | VIP ROOMS | + VIP TAG! |
| Speed2x | x2 SPEED | x2 SPEED ON | TREADMILLS! |

A future pass falls back to `p.title:upper()` plus `p.desc` with its tags stripped, split at the space nearest the middle.

### 4.6 SPEED: Double card (576 x 124, face 119) and boost cards (186 x 176, face 171)

**Double:**

| Name | rect | Look |
|---|---|---|
| Glow | 8, 6, 132, 108 | (85,200,255), 0.55 |
| Pop.Icon | sticker 26, 14, 90 | SPEED_ICON |
| Pop.Badge | text ("x2", 92, 78, 44, 24) | GOLD_TXT |
| Title | text ("DOUBLE SPEED", 142, 16, 250, 24), left | White |
| Now | text ("x" .. mult(now), 142, 48, tw + 8, 22), left | White |
| Arrow | `H.arrow(face, "Arrow", 142 + tw + 10, 49)` | Lime chevron 18 x 22 |
| Next | text ("x" .. mult(next), arrowX + 26, 48, 120, 22), left | (150,255,60) |
| Sub | text ("EVERY BUY DOUBLES IT!", 142, 82, 250, 16), left | LAV |
| Buy | priceButton gold 404, 32, 160, 54; d 4, r 12 | glyph 30, price @28 |

- `mult()` is today's function. **MAX:** Now = `"x" .. mult .. " MAX"` in GOLD_TXT; Arrow and Next are hidden; Buy becomes `setWord("MAX", "silver")`.
- Buy -> `buy("speed")`, the price of the current ladder step (`ShopConfig.doubleSpeedStep`, `robux(step.id, ...)`).

**Boost cards** `Boost_Speed15m`, `Boost_Speed3`, `Boost_Speed2h` (data from `SpeedBoostCards.CARDS[key]`):

| Name | rect | Look |
|---|---|---|
| Glow | 38, 4, 110, 92 | Card colour, 0.55 |
| BestValue (Speed2h) | `H.tag(face, "BestValue", 8, 6, 124, 22, "BEST VALUE")` | Not rotated, inside the top band |
| Pop.Art | sticker 54, 32, 56 (shoe) or 50, 32, 56 (potion) | Speed15m / Speed2h: SPEED_ICON plus `Pop.Clock` sticker (108, 60, 26). Speed3: `byKey.Speed.icon` plus `Count` text ("x3", 110, 48, 56, 26) left, GOLD_TXT |
| Title | text (…, 6, 90, 174, 22) | Card colour: Speed15m (255,140,230) `CARDS.Speed15m.title()` (+90M); Speed3 (125,210,255) "3 POTIONS"; Speed2h (255,180,110) `CARDS.Speed2h.title()` |
| Sub | text (…, 6, 114, 174, 16) | LAV: "15 MIN OF SPEED" / "x2 SPEED 30 MIN" / "2 HRS OF SPEED" |
| Buy | priceButton gold 10, 134, 166, 32; d 3, r 10 | glyph 22, price @22. `robux(CARDS[key].id, CARDS[key].price)`. Buy -> `buy(table.unpack(CARDS[key].buy))` |
| BuyHit | TextButton, centre (93, 151), 166 x 44 | Invisible, drives the button. 31 pt on phones |

### 4.7 POTIONS: pack cards (186 x 176; `Pack_<key>`)

Row 1 = Money3, Hatch3, Speed3. Row 2 = Money10, Hatch10, Speed10.

| Name | rect | Look |
|---|---|---|
| Glow | 38, 4, 110, 92 | PACK colour (Money (255,214,80), Hatch (130,235,110), Speed (110,205,255)), 0.6 |
| BestValue (count ≥ 10) | `H.tag(..., 8, 6, 124, 22, "BEST VALUE")` | |
| Pop.Art | sticker 50, 32, 56 | `byKey[pack.potion].icon` |
| Pop.Count | text ("x" .. count, 110, 48, 64, 26), left | GOLD_TXT |
| Title | text (POTION:upper(), 6, 90, 174, 22) | PACK colour |
| Sub | text (…, 6, 114, 174, 16) | LAV: Money "x2 CASH 30 MIN", Hatch "x2 HATCH 30 MIN", Speed "x2 SPEED 30 MIN" |
| Buy / BuyHit | as the boost cards | `buy("potion", pack.key)` |

### 4.8 TREADMILL card (576 x 124)

| Name | rect | Look |
|---|---|---|
| Glow | 8, 6, 132, 108 | (255,150,70) |
| Pop.Icon | sticker 26, 14, 90 | TREADMILL_ICON |
| Title | text ("TREADMILL", 142, 16, 176, 24), left | White |
| Now / Arrow / Next | as Double, y 48 | `sign:GetAttribute("NowName")` / `NextName` (today's source) |
| Sub | text ("KEPT ON REBIRTH", 142, 82, 176, 16), left | LAV |
| Money | glossButton lime 326, 32, 112, 54; d 4, r 12; label @26 | `"$" .. Format(TreadmillMoney[tier + 1])` -> `buy("treadmillMoney")`. `HatchTile "treadbtn"` |
| Robux | priceButton gold 452, 32, 112, 54; d 4, r 12; glyph 26, price @26 | `robux(TreadmillProducts[tier + 1] or 0, TreadmillRobux[tier + 1])` -> `buy("treadmillRobux")`. `HatchTile "treadbtn"` |
| MaxText | text ("MAX LEVEL", 326, 46, 238, 24) | GOLD_TXT, shown only when maxed |

**States** (today's rules):
- **hideRobux** (`TreadmillRobuxHidden[tier + 1]`): Robux is hidden and Money moves to x 452.
- **maxed:** both buttons are hidden, MaxText is shown, and Now / Arrow / Next become `MAX` in gold.

### 4.9 EGGS card (576 x 124)

| Name | rect | Look |
|---|---|---|
| Glow | 8, 6, 132, 108 | (120,255,120), 0.6 |
| Pop.Icon | sticker 26, 14, 90 | EGG_ICON |
| Title | text ("HATCH ALL EGGS", 142, 16, 250, 24), left | White |
| Line1 / Line2 | text ("EVERY EGG IN YOUR BASE", 142, 50, 250, 16) / ("HATCHES RIGHT NOW!", 142, 70, 250, 16), left | LAV |
| Buy | priceButton gold 404, 32, 160, 54; glyph 30, price @28 | `robux(GrowAllProduct, GrowAllPrice)`. Activated -> `invokeSkip("all")`. A failure flashes `(msg or "No eggs"):upper()` red for 1.3 s |

### 4.10 Gift picker (`ShopPage.GiftPicker`, Z 20)

| Name | Class | rect | Look |
|---|---|---|---|
| GiftPicker | TextButton | 0, 0, 740, 463 | INK at BackgroundTransparency 0.35, corner 18. `HatchBlocker`. Activated -> closePicker |
| Box | `H.shellCard(picker, "Box", 160, 66, 420, 386, {noHit = true, solid = (31,24,82)})` | | Its holder also gets a full-size transparent TextButton `Sink` (`HatchBlocker`), so clicks don't close the picker |
| Title | text (`"GIFT " .. PASS_COPY.title`, 16, 12, 340, 22), left | | GOLD_TXT |
| Close | glossButton red 372, 8, 34, 34; d 4, r 9, ol 2, "X" @21; `input = CloseHit` | | CloseHit TextButton, centre (389, 25), 46 x 46, `HatchHit` |
| Sub | text ("PICK A PLAYER IN THIS SERVER", 16, 42, 388, 16), left | | LAV |
| Players | ScrollingFrame | 8, 66, 404, 307; bar 8 (inset Always) | Rows at (4, 4 + 68 (i - 1), 380, 60); `CanvasSize = 8 + 68 n` |

Each row is `H.chip(players, "P" .. userId, 4, y, 380, 60, 14)`, with `HatchTile "rows"`:

| Child | rect | Look |
|---|---|---|
| Head | Frame (8, 8, 44, 44), round, stroke 2 | Fill (72,62,150), plus an ImageLabel headshot (thumbnail cache, as today) |
| Name | text (DisplayName, 62, 10, 176, 18), left | White, `H.fit` down to 16 |
| User | text ("@" .. Name, 62, 32, 176, 16), left | LAV_DIM |
| Gift | priceButton gold (238, 10, 134, 40), glyph 24, price @22 = `robux(p.giftId, p.price, Product)`. Owned (`Pass_<key>` on the target): `setWord("OWNED", "silver")` @18 | |

- **Empty list:** "NOBODY ELSE IS HERE YET" (16, 160, 388, 18) and "INVITE A FRIEND!" (16, 184, 388, 16), centred, LAV.
- **Behaviour** (today's code, kept):
  - `buildPicker` runs on open (deferred), on PlayerAdded / PlayerRemoving, and on the target's `Pass_<key>` change.
  - It clears `pickerConns` on every rebuild and on close.
  - Studio switch: workspace `TestGiftSelf`.
  - A row failure shows `MSG:upper()` red for 1.5 s, then rebuilds. Success closes the picker.

### 4.11 Toasts (`PlayerGui.GiftToast`, DisplayOrder 30, ResetOnSpawn false)

Positions and timing are today's: Toast at (0.5, 0.83) for 4 s; Granted at (0.5, 0.075) for 3.5 s with a 0.6 -> 1 Back pop.

**Look:**
- GothamBlack (`H.FONT`), `TextScaled = false`, TextSize 28, ink Contextual stroke 3.
- Each label has a UIScale `WindowScale` = the Shop window scale `s` (the MainMenu fit, re-read on show).
- Colours as today: gold (255,214,60) / lime (125,255,105) / pink (255,120,230).
- Box 600 x 32 logical. Text copy is unchanged.

### 4.12 Containment margins (every number checked)

| Element | At rest | At hover / pulse peak |
|---|---|---|
| Pass Buy (198 x 40) in a 284 x 145 face | right gap 10, bottom 7 | hover 1.04: right 280.5, bottom 141.3 |
| Pass Gift vs Buy | gap 12 | both hovered: 67.6 vs 69.5, no overlap |
| Small Buy (166 x 32) in a 186 x 171 face | 10 / 10 / 5 | hover 1.04: bottom 169.1 |
| Wide Buy (160 x 54) in 576 x 119 | right 12 | hover 1.04: right 569.7 |
| Treadmill Money vs Robux | gap 14 | both hovered: 442.7 vs 447.3 |
| Starter Buy (160 x 56) | | pulse / hover 1.02: right 568 |
| Popup Buy (492 x 60) | right 10 | 1.02: right 737.4, inside the rim (738.5) |
| Popup NoThanks (212 wide) vs Buy | gap 16 | NoThanks hover 1.04: stroked right 228.7; Buy pulse / hover peak 1.02: stroked left 230.6, so 1.9 px clear even with both at peak |
| Rail Pill | 3 px inside the recess | hoverScale 1, so no growth |
| Picker row Gift (134 x 40) in 380 | right 8 | hover 1.04: 377.2 |

- The popup Holder at 1.0 with its Size tween (D11) never exceeds the fitted size.
- **Text fills** (QA report): the tightest are "TREADMILL"@16 82 %, "EVERY EGG IN YOUR BASE"@16 82 %, "29.4%"@20 78 %, "BEST VALUE"@16 81 %. Every other line is lower.
- In-engine GothamBlack is narrower: 0.858 x Montserrat on average (24 measured strings, max 0.889).
- Refusal words are `H.fit` variants down to 16. For example, "ALREADY OWNED" steps down to 18 in a 166 button.

---

## 5. Behaviour that must keep working (and how each is tested)

| # | Behaviour | Where | Test |
|---|---|---|---|
| B1 | Shop opens from the Shop tile and `OpenPage:Fire("Shop")`. HATCH NIGHT chrome, title SHOP, band "Shop", AR 740/470, canvas scale = skin scale | MenuController + ShopClient | `shop_client.lua` check 1 |
| B2 | Every buy path sends exactly today's remote args: `("pass", key)` x4, `("gift", key, userId)`, `("speed")`, `("speedPack","Speed15m")`, `("potion","Speed3")`, `("speedPack","Speed2h")`, `("potion", pack.key)` x6, `("treadmillMoney")`, `("treadmillRobux")`, `SkipEgg("all")`, Starter `Buy:InvokeServer("Popup")` | ShopClient, StarterPackClient | dry run (D14): `shop_client.lua` check 4, `starter_popup_client.lua` check 5 |
| B3 | Refusals: "Not enough money" -> NEED MORE $!, other reasons -> MSG:upper(), "prompted" / ok -> nothing. 1.3 s, red, then back. The treadmill money path works for real at $0 | ShopClient | dry-run result string; the real `treadmillMoney` invoke on a $0 test save |
| B4 | Live (regional) prices: `robux(id, fallback, infoType)` cache; Studio id 0 -> fallback, live -> "SOON". The price group re-lays out on text change | ShopClient | check 3: every price label == `robux(...)` / ShopConfig fallback; `TestPriceOverride` attribute "1499" re-centres |
| B5 | Owned passes -> OWNED (silver, not Active); Double at max -> MAX; treadmill hideRobux / maxed | ShopClient | client-local attribute toggles (`Pass_VIP`, `SpeedBoosts = 10`, `TreadmillTier`), restored after |
| B6 | Gifting: picker over the page, players listed (TestGiftSelf), owned targets OWNED, rows rebuild on join / leave / attribute, closes on page hide, gift toast | ShopClient | check 6; Server: `Shop.Gifted:FireClient(p, "got", "VIP", "Tester")` -> toast text `TESTER GIFTED YOU VIP!` |
| B7 | `ShopPage` attribute `ScrollTo` (PetsEggsUI GET MORE: `OpenPage:Fire("Shop")` then `SetAttribute("ScrollTo","POTIONS")`) scrolls to the section and clears the attribute. The page opens at the top | ShopClient | check 5 |
| B8 | Tab press -> animated scroll; the active tab follows the scroll | ShopClient | check 5 |
| B9 | Analytics: `Analytics.UI:FireServer("shop", true/false)` exactly once per change of "page and every ancestor visible and MainMenu enabled" | ShopClient | Studio counter `ShopFunnelSent` = "n:last"; open / close x3 -> 6 fires alternating |
| B10 | Granted toast (`Shop.Granted`) | ShopClient | Server `Shop.Granted:FireClient(p, "+1.2B SPEED!")` -> visible, text equal |
| B11 | Starter card at the very top only while the offer runs. Buy opens the popup (never buys) | StarterPackClient | check 2 / 7 in `starter_popup_client.lua` |
| B12 | Popup: `Open` bindable (HUD), `TestOpen` / `TestBuy` (Studio), Backdrop / X / NO THANKS close, opening fires `Seen` once (`StarterPopup` false -> true), the `Price` attribute | StarterPackClient | `starter_popup_client.lua` checks 1-3 |
| B13 | Auto-popup (after Rebirth 1, 10 s after load + 2.5 s quiet, once) | unchanged code | `starter_popup_client.lua` check 9 (fresh save + `Rebirths 1` + StarterDebug reset) |
| B14 | 24 h timer: "ENDS IN hh:mm:ss", red in the last hour; card "LEFT"; on expiry the popup closes and the card hides | StarterPackClient | StarterDebug `endsAt now + 1800` (red), `endsAt now + 8` (expiry within 9 s) |
| B15 | Owned flow: THANK YOU!, OWNED!, closes after 1.6 s, card gone, HUD gone | StarterPackClient | StarterDebug `grant` while open |
| B16 | Restricted variant: no egg, no odds, 10x potions | StarterPackClient | StarterDebug `restricted` |
| B17 | **Odds visible before purchase** (paid random item rule) | StarterPackClient | section 7.4 odds check |
| B18 | StarterPackHud contract: `StarterPackUI.Open`, `Price` attribute, the HUD hides while `StarterPackUI.Enabled`; the tests may set `Enabled = false` directly, and the loops must stop then too | StarterPackClient | `starter_hud_client.lua` sections layout / placement / hover / content / overlaps / timer / expiry still pass |
| B19 | Other windows unchanged; Gift unchanged | MenuController / BrickUI | sections 7.6 and 7.5 Gift runs |
| B20 | Respawn: MainMenu, StarterPackUI and GiftToast have ResetOnSpawn false; the Shop and popup work after a respawn | all | `shop_client.lua` check 8 (separate session) |

---

## 6. Code plan

### 6.1 BrickUI (1 line)

`BrickUI.PAGE_SKIN = {Gift = "Hatch", Shop = "Hatch"}` (line 512). Comment: "phase 2 step 1 (2026-10-21): Shop. Plan docs/plans/2026-10-21-hatch-night-popup-shop.md".

### 6.2 BrickUI.Hatch: extensions (additive; old default paths byte-identical)

1. **Constants** of section 4.0: `H.BAND.Shop`, `H.PAGE_BAND`, `H.PAL.violet`, `H.ICON.robuxWhite`, `H.GOLD_TIMER`, `H.RED_TIMER`.
2. **`H.bandTheme(page)`:** workspace override first (unchanged), then `H.PAGE_BAND[page]`, then today's seasonal rule. A `nil` page behaves as today.
3. **`H.recess(parent, name, x, y, w, h, z, radius)`:** a new optional `radius`, default `h / 2`. TopShade / BottomLine inset becomes `radius` instead of `h / 2`; with the default it is identical.
4. **`H.chip(parent, name, x, y, w, h, radius)`:** a new optional `radius`, default `h / 2`.
5. **`H.glossButton` opts.pulseAmp** (default 0.025): `pulse()` uses `1 + btn.pulseAmp * (1 - cos(...))`. The default is identical to today.
6. **`H.shellCard` opts:**
   - `noHit` (Hit not created; there is no `hit` field);
   - `grad = {top, bottom}` (face gradient keys, also used by `setToday(false)`).
   - Defaults are unchanged.
7. **`H.windowChrome(win, opts)`:** a new optional `opts.bats` (default true). `false` skips the bat ViewportFrames and `syncBats` is a no-op.
8. **NEW `H.priceButton(parent, name, x, y, w, h, opts) -> btn`:**
   - It is a `glossButton(parent, name, x, y, w, h, opts.pal or "gold", {d, r, ol, hoverScale, pulseAmp, input, z})` with no `opts.text`.
   - Children on the face: `Pre` (text, only if `opts.pre`), `Robux` (`H.sticker` robuxWhite, size `opts.glyph`), `Price` (text @`opts.size`), `Word` (text, full face width, hidden).
   - `btn.setPrice(s)`: Word hidden, Pre/Robux/Price shown, then the group is laid out. `pw = textWidth(pre, size) + 6`; `prw = textWidth(s, size) + 6`; `G = (pre and pw + 2 or 0) + glyph + 6 + prw`; `x0 = floor((w - G) / 2)`. Labels sit at y `round((h - d - size) / 2) - 1`; the glyph is vertically centred on the face. It restores `btn.basePal`.
   - `btn.setWord(s, pal, size)`: Pre/Robux/Price hidden; Word = `H.fit(word, {s, "TRY AGAIN"})` at `size or opts.size`; `setPalette(pal)`.
   - `btn.restore()`: `setPrice(btn.price)`.
   - It sets `HatchPad 8`, `HatchPadBottom 3`.
9. **NEW `H.arrow(parent, name, x, y, z)`:**
   - A Frame 18 x 22 with 2 ink `H.segment`s, thickness 7, (3,3)-(14,11) and (14,11)-(3,19), plus 2 lime ones (184,255,106), thickness 3.2, on top.
10. **NEW `H.sectionHeader(parent, name, x, y, w, title, icon, color) -> frame`:** section 4.2.
11. **`H.fitWindow`:** unchanged (the popup passes leftClear 0).

**Rule for the builder:** after editing, diff the module source against `BrickUI_prePopupShop.Hatch`. Every changed old line must be one of: the 3 signature lines (recess, chip, windowChrome), the pulse expression, the shellCard Hit / gradient lines (wrapped in `if not opts.noHit`), and the bandTheme body. Write that diff in the ledger.

### 6.3 MenuController (1 line)

Line 242: `hatch.setTheme(H.bandTheme())` -> `hatch.setTheme(H.bandTheme(name))`. Nothing else.

### 6.4 ShopClient (rewrite of the UI; logic kept)

**Keep (copy as is):**
- the requires, `robux()`, `flashUntil` / `free` timing, the `result()` message mapping, `mySign()`;
- the refresh math (pass owned, Double mult and ladder price, pack prices, treadmill tier, maxed and hideRobux, GrowAll price);
- the gift picker logic (targets, sort, owns, thumbs cache, `pickerConns`, rebuild triggers, TestGiftSelf);
- `Gifted` / `Granted` handlers (copy texts);
- the ScrollTo handler (0.45 s delay kept);
- the "page opens at the top" rule, `closePicker` on hide.

**Delete:**
- the ScrollingFrame / UIListLayout / UIPadding page and `fitCanvas`;
- `row()`, `header()`, `grid()`, `card()`, `wideCard()`, `wideButton()`, `centre()`, `plain()`;
- the side tabs (`Window.ShopTabs`) and the `CUI` branch;
- the B.* text / brick builds;
- the 0.3 s forever loop and the 0.5 s analytics poll.

**Build, in this order:**
1. `local H = B.Hatch`. If nil: `warn`, enable `ShopClientLegacy` (D15), return.
2. The ShopPage canvas, the Rail, Scroll / List and `StarterSlot` (sections 4.2-4.3).
3. The sections (4.5-4.9) via `layout(starterVisible)` (a pure function returning the y table of 4.3).
4. The GiftPicker (4.10) and the toasts (4.11).

**`buy(btn, ...)` / `invokeSkip(kind)`:**
- Studio: if `page:GetAttribute("TestDryRun")`, set `page:SetAttribute("TestLastBuy", HttpService:JSONEncode({...}))`, then return `false, page:GetAttribute("TestDryRunResult") or "prompted"`.
- Otherwise: `Buy:InvokeServer(...)` / `SkipEgg:InvokeServer(kind)`.
- Then: `result(btn, ok, msg)` -> `btn.setWord(word, "red")` for 1.3 s (no pulse while red), then `refresh()`.

**`refresh()`:** today's computations, written into the new labels and buttons (`setPrice` / `setWord`). Text is set only when it changes (`H.fit` caches).

**Loops (D13):**
- `local token = 0`. On `page.Visible` true:
  - `token += 1`; snap scroll to 0; `activeName = nil`; `refresh()`; `updateActive()`; snap the Pill.
  - `task.spawn(loop, token)`, where loop = `while page.Visible and token == my and win.Visible do refresh(); task.wait(0.3) end`.
- On hidden: `closePicker()`.
- `Scroll:GetPropertyChangedSignal("CanvasPosition"):Connect(updateActive)`.
- Pulse (the Starter card Buy only): StarterPackClient's own RenderStepped, connected while the slot is visible and the page is shown (section 6.5).
- **Studio perf probe:** `page:SetAttribute("HatchPerfShop", "<n refreshes> <sum ms of the last 30> <max ms>")`, and `ShopLoop` true while the loop runs.

**Analytics (event-driven):**
- `local function onScreen()` = page and every GuiObject ancestor `Visible`, and MainMenu `Enabled`.
- Connect `GetPropertyChangedSignal("Visible")` on page, Body, Face, Window, and `Enabled` on MainMenu, to `check()`.
- `check()` fires `AnalyticsUI:FireServer("shop", now)` only when `now ~= was`.
- Studio: `page:SetAttribute("ShopFunnelSent", n .. ":" .. tostring(now))`.

**updateActive / scrollTo:**
- Logical y (4.3) and the probe unit K (section 7.2): `CanvasPosition = Vector2.new(0, target * K)` and `scrollY = Scroll.CanvasPosition.Y / K`.
- Pill tween only when the active section changes.

**Studio test hooks** (only when `RunService:IsStudio()`):
- `page.TestPress` (BindableEvent, arg = button key: `Pass_<key>`, `Gift_<key>`, `Double`, `Boost_<key>`, `Pack_<key>`, `TreadMoney`, `TreadRobux`, `Eggs`, `Tab_<SECTION>`) runs the same handler as the click.
- `page.TestGiftRow` (userId) presses that picker row.
- Attributes:
  - `TestDryRun`, `TestDryRunResult`;
  - `TestDryRunHold` (a refusal word stays until the attribute is cleared, for the containment matrix);
  - `TestPriceOverride` (forces every Robux price text, to test the layout);
  - `TestPickerRows` (n fake picker rows built from the local player, layout only);
  - `HatchTestPulse` / `HatchTestHover` (as GiftPage; forwards `H.setTestHover`).
- Read-only probes: `HatchPerfShop`, `ShopLoop`, `ShopFunnelSent`, `PickerConns` (= `#pickerConns`, written on every picker build / close).

### 6.5 StarterPackClient (UI rebuild; logic kept)

**Keep verbatim:**
- lines 14-37 (services, requires, remotes), 110-137 (pack state + live price);
- `setOpen` guards (owned / not active, `thanked = false`, `Seen:FireServer()` when `StarterPopup ~= true`, SFX Open);
- `closePopup`, `pressBuy` (busy, `pcall(Buy.InvokeServer, Buy, "Popup")`, 1.4 s refusal), `onOwned` (THANK YOU, HatchWin, close after 1.6 s);
- the attribute listener list (lines 459-465);
- the auto-popup `quiet()` + loop (lines 494-543);
- `Open` / `TestOpen` / `TestBuy`;
- `gui` name / DisplayOrder 22 / IgnoreGuiInset true / ResetOnSpawn false;
- the `Price` attribute.

**Delete:** the Check-UI constants and helpers (lines 38-108), the popup build (139-292, 294-351), the old card (406-444), the sunburst RenderStepped (468-470), and the 0.5 s forever loop (471-492).

**Build:**
1. `local H = B.Hatch`. If nil: `warn` and do not create `Open` (D15); the Shop card is skipped. Return before building.
2. Backdrop (TextButton; ink (8,6,25), BackgroundTransparency 0.45), Holder (TextButton, `HatchBlocker`).
3. `chrome = H.windowChrome(Holder, {bats = false})`, Canvas + `H.bindCanvasScale(canvas, Holder, 740)`.
4. Section 4.1 tables. `refreshPopup()` (restricted layout, texts, odds per `eggKind/kg` key as today) and `layoutBuy(price)`.
5. **Fit:** section 3.2, on open and on viewport change while enabled.
6. **Motion:**
   - `gui:GetPropertyChangedSignal("Enabled")` connects / disconnects ONE RenderStepped: Rays rotation 12 deg/s, plus the Buy pulse unless refusing or thanked.
   - Studio: `RaysLoop` attribute, `HatchPerfPopup` probe.
   - It also starts the ticker.
7. **Ticker + expiry (D13):**
   - `scheduleExpiry()` on `StarterEndsAt` / `StarterPack` changes and at start: `task.delay(max(0, timeLeft()) + 0.2, token-checked: refreshAll(); if not active() and gui.Enabled and not thanked then closePopup() end)`.
   - `startTicker()` (idempotent) runs `while (gui.Enabled and not thanked) or cardShown() do updateTimer(); updateCard(); task.wait(0.5) end`.
     - `cardShown()` = `slot.Visible and shopPage.Visible and menuWin.Visible`.
   - Started on popup open, on ShopPage / Window `Visible` true, and on slot shown.
8. **Shop card:**
   - `slot = menuWin.Face.Body:WaitForChild("ShopPage", 60):WaitForChild("Scroll"):WaitForChild("List"):WaitForChild("StarterSlot")`.
   - If it is not found (legacy shop), skip the card.
   - Build section 4.4. `refreshAll()` sets `slot.Visible = active()`, the restricted variant, the texts and the price.
   - Studio: `slot.TestPress` -> the Buy handler.
9. **Studio dry run:** `gui:GetAttribute("TestDryRun")` -> `pressBuy` records `{"StarterBuy", "Popup"}` in `TestLastBuy` and uses `TestDryRunResult` as the server reply.
10. **Studio test switches** (all on `gui`):
    - `HatchTestScale`;
    - `HatchTestOdds` (n; repeats the odds list to n cells, layout test only);
    - `HatchTestPulse`, `HatchTestHover`;
    - `TestDryRunHold` (the refusal word stays);
    - `TestThanksHold` (the THANK YOU state does not auto-close; containment only).
    - Read-only probes: `HatchPerfPopup`, `RaysLoop`, `StarterTicker`.

### 6.6 ShopClientLegacy (D15)

- A clone of today's ShopClient, with `Enabled = false` and tags stripped. Header comment: "Fallback only: ShopClient enables this if BrickUI.Hatch fails to load".
- Rename only the script. The source is byte-identical.

### 6.7 Backups (Task 1)

**Clones** into `ServerStorage._Backup_HatchNight.Before`:
- `ShopClient_prePopupShop`
- `StarterPackClient_prePopupShop`
- `MenuController_prePopupShop`
- `BrickUI_prePopupShop` (with `Hatch`)

**For every clone:**
- `Enabled = false` on the LocalScripts;
- every CollectionService tag removed from the clone and its descendants (memory: strip tags from backup copies).

**Folder attributes:**
- `WasEnabled_prePopupShop = "ShopClient,StarterPackClient,MenuController"`.
- `HowToRestore_prePopupShop` = "Replace ShopClient, StarterPackClient, MenuController (under StarterGui.MainMenu) and BrickUI (+Hatch) with these copies, set Enabled = true on the LocalScripts, delete StarterPlayerScripts.ShopClientLegacy".

---

## 7. Tests

**Rules (every Play test, as in the Gift plan):**
- `workspace:GetAttribute("TestFreshSave") == true`, read in Edit before Play (HARD RULE).
- `get_studio_state` before every step. Never stop someone else's Play session; wait for Edit.
- Never drive the Studio UI.
- **Never press a real Robux button:** no `user_mouse_input` on any price button, no `TestBuy` without `TestDryRun`.
- Client-local attribute toggles (`Pass_*`, `SpeedBoosts`, `TreadmillTier`) are UI-only. Restore them at the end of each test.

### 7.1 `hatch_pure.lua` (Edit; `require(Hatch:Clone())`): new checks

1. **`fitWindow` popup rows** (leftClear 0):

| Input | Expected (s, w, h, cx, cy) |
|---|---|
| (1920, 1022, 0) | (1.18, 873.2, 554.6, 960, 511) |
| (1050, 562, 0) | (1.1702, 866.0, 550.0, 525, 281) |
| (732, 346, 0) | (0.7106, 525.9, 334.0, 366, 173) |
| (667, 331, 0) | (0.6787, 502.3, 319.0, 333.5, 165.5) |

   The 4 Gift rows still pass.
2. `bandTheme("Shop") == "Shop"`; `bandTheme("Gift") == bandTheme()`; with workspace `HatchBand = "HatchGold"`, `bandTheme("Shop") == "HatchGold"` (attribute restored).
3. `PAL.violet` and `BAND.Shop` exist; `ICON.robuxWhite == ShopConfig.ROBUX_ICON`.
4. `recess` with no radius gives the same TopShade Position / Size as before. With radius 20, TopShade is at x 20.
5. **`priceButton` layout:** w 160, glyph 30, size 28, price "49" -> group centred within ±1 px. `setWord("OWNED", "silver")` hides Robux. `setPrice("1250")` re-centres with group width ≤ w - 16.
6. `glossButton` with no pulseAmp: `pulse(0.6)` -> Scale 1.05 (unchanged); with pulseAmp 0.01 -> 1.02.

### 7.2 `hatch_scroll_probe.lua` (Task 2; throwaway Play test, then delete the probe instances)

Build a ScrollingFrame (200 x 100 logical, CanvasSize (0, 1000), ScrollBarThickness 8) under a Frame with UIScale 0.5. Record:
- (a) `AbsoluteCanvasSize.Y` (expect 500 if CanvasSize scales);
- (b) the CanvasPosition range after `CanvasPosition = (0, 99999)`: 900 (logical, K = 1) or 450 (px, K = s);
- (c) the rendered bar width (4 or 8 px);
- (d) a 10 px UIStroke inside at scale 0.5 renders 5 px (re-confirms the Gift probe).

Write K in the ledger and use it in `scrollTo` / `updateActive`. If (c) shows the bar does not scale, set `ScrollBarThickness = round(8 * s)` in the CanvasScale binder.

### 7.3 `shop_client.lua` (Client datamodel; fresh session)

1. **open:** `OpenPage:Fire("Shop")`, wait 0.7 s.
   - HatchBack / HatchFront visible; HatchFront.Title `SHOP`; the first Tooth colour (220,0,100); Bats not visible.
   - Window AR 740/470 ± 0.01; `ShopPage.CanvasScale == HatchBack.SkinScale` ± 0.001.
   - `Window.ShopTabs` and `Body.GiftPicker` do not exist.
   - Rail has 5 Hit buttons; the Pill is on FEATURED.
2. **layout:** with the offer inactive, every `Header_*` content y is per the 4.3 "hidden" column and CanvasH = 1492.
   - Server: `Rebirths 1` + `StarterDebug:Invoke("reset", p)`. Then `StarterSlot.Visible` is true and the y values match the "shown" column; CanvasH 1634.
3. **prices:** every price label equals `robux(...)` (the same cache: compare with `ShopConfig` fallbacks in Studio, or the live price read via GetProductInfo).
   - `TestPriceOverride = "1499"` -> every gold group fits inside its button face (Price right edge + stroke ≤ face right - 4) and stays centred ±1 px. Then clear it.
4. **dry-run buy paths:** `TestDryRun = true`. For each key in B2: `TestPress:Fire(key)`, then decode `TestLastBuy` and compare with the expected args table.
   - Then `TestDryRunResult = "Not enough money"`: press `Pack_Money3` -> its button word `NEED MORE $!`, palette red; after 1.4 s it is back to the price, palette gold.
   - `TestDryRunResult = "prompted"` -> no word change.
   - Clear both attributes.
   - **Real:** `TestPress:Fire("TreadMoney")` on the $0 save -> `NEED MORE $!` (a server reply, no prompt).
5. **scroll:** `TestPress:Fire("Tab_POTIONS")` -> within 0.6 s `CanvasPosition.Y / K` equals the POTIONS header y for the current slot state (866 shown / 724 hidden; 4.3) ±1, and the Pill is on POTIONS.
   - `Tab_EGGS` -> max scroll, Pill EGGS.
   - Close; then `OpenPage:Fire("Shop")` + `SetAttribute("ScrollTo","POTIONS")` (the PetsEggsUI path) -> within 0.9 s: POTIONS position, attribute nil.
   - Reopen -> top (0), FEATURED.
6. **gift:** workspace `TestGiftSelf = true`; `TestPress:Fire("Gift_VIP")` -> `GiftPicker.Visible`, Title `GIFT VIP`, a row `P<userId>` exists.
   - `TestDryRun`: `TestGiftRow:Fire(userId)` -> `TestLastBuy == ["gift","VIP",<userId>]`.
   - Close the Shop -> picker hidden, `#pickerConns == 0` (Studio attribute `PickerConns`).
   - Server: `Gifted:FireClient` -> toast visible with the expected text, hidden after 4 s.
7. **states:** local `Pass_VIP = true` -> its Buy shows OWNED, silver, `Face.Active == false`. Local `SpeedBoosts = 10` -> Double MAX. `TreadmillTier = 1` -> Robux hidden, Money at x 452. `TreadmillTier = 11` -> MAX LEVEL. Restore all of them.
8. **respawn** (separate session): with the Shop open, kill the character. After respawn, `OpenPage:Fire("Shop")` works and the GiftToast gui still exists.
9. **analytics:** open / close the Shop 3 times -> `ShopFunnelSent` count +6, alternating true / false. Opening Rebirth after the Shop gives exactly one false.

### 7.4 `starter_popup_client.lua` (Client; Server steps via StarterDebug as in `starter_hud_client.lua`)

1. **open paths:**
   - `TestOpen` -> Enabled, Holder fitted (3.2), `HatchFront.Title == "STARTER PACK!"`, band tooth (220,0,100), `Bats` absent.
   - `Open:Fire()` (HUD path) -> same.
   - Shop card `slot.TestPress` -> same.
2. **close paths:** CloseHit, NoThanks, Backdrop each close. A click inside the window (`GetGuiObjectsAtPosition` at Canvas (600, 300)) returns Holder (or a child) as the first GuiButton, not the Backdrop.
3. **Seen:** on a fresh offer, after the first open the server `StarterPopup == true` within 2 s.
4. **timer:** `EndsIn.Text` matches `^ENDS IN %d+:%d%d`; gradient last key (255,170,0). With `endsAt now + 1800`, the last key is (255,60,50). The card Timer matches `LEFT$`.
5. **dry-run buy:** `TestDryRun` + `TestBuy:Fire()` -> `TestLastBuy == ["StarterBuy","Popup"]`.
   - `TestDryRunResult = "Offer ended"` -> Buy word OFFER ENDED, red, for 1.4 s, then gold BUY + price.
   - `Price` attribute = the label text.
6. **odds visible** (the paid random item rule), with the offer active and not restricted. In both states:
   - (a) `Odds.Visible` and `OddsCaption.Visible`.
   - (b) the cell count == `#P.odds(StarterEgg, StarterKg, CreatureConfig)`.
   - (c) every `Pct.Text == P.pctText(o.pct)`, in order.
   - (d) the secret cell's pet ImageColor3 is black and `Secret` is visible.
   - (e) every cell's box is inside the Holder box and inside MainMenu's safe box.
   - (f) sampling `PlayerGui:GetGuiObjectsAtPosition` on a 6 x 3 grid over the Odds recess, the first drawn object belongs to StarterPackUI.
   - (g) Buy is visible at the same time with no scrolling (the Holder has no ScrollingFrame).
   - Also with `HatchTestOdds = 6` and `7`: (a)-(e) plus containment (7.5).
   - Server `restricted`: no Odds / Egg / EggRow, PotionRow `10x EVERY POTION`, Hero image = CASH.
7. **owned:** while open, Server `grant` -> title THANK YOU!, Buy word OWNED! lime, NoThanks hidden. Closed within 2.2 s; `slot.Visible == false`; StarterPackHud art hidden.
8. **expiry:** Server reset + `endsAt now + 8` while open -> closed by t = 9 s; slot hidden.
9. **auto-popup:** fresh save, Server `Rebirths 1` + reset, close all windows, wait -> Enabled within 15 s, once. After closing it does not reappear within 20 s.

### 7.5 `hatch_containment.lua` v2 (`_G.HatchContain(label, cfg)`)

**Refactor:** `cfg = nil` is exactly today's Gift run (same checks, same output). The new cfg fields:

| Field | Meaning |
|---|---|
| `root` | the canvas: GiftPage / ShopPage / popup Canvas |
| `win` | Window / Holder |
| `back`, `front` | the chrome layers |
| `safe` | the box for `HatchShell` and the window bounds (MainMenu box for both) |
| `screen` | the gui for `onTop` (MainMenu / StarterPackUI) |
| `hud` | bool: left-HUD clearance at native scale (true for the Shop) |
| `probes()` | the list of {button, x, y} |
| `testRoot` | where HatchTestPulse / HatchTestHover are set |
| `extra` | Gift-only checks: heroButton, iconTops, drawOrder |

**New rules:**
- **Skips:** `HatchBlocker` objects are skipped by the hit checks.
- **ScrollingFrame descendants:**
  - `hitInWindow` / `hitOverlap` / `hitFirst` only for hits whose box intersects the scroll's visible box (AbsolutePosition, AbsoluteWindowSize);
  - containment is unchanged (the parent boxes are scroll-independent);
  - new `scrollFit`: every child of List has its stroked box inside List; `List.AbsoluteSize.X ≤ Scroll.AbsoluteWindowSize.X + TOL`.
- **New `centred`** (popup): the Holder centre equals the MainMenu box centre ±1 (no HatchTestScale).
- **New `priceGroup`:** for every priceButton, the Pre / Robux / Price union is centred in the face ±1 px and its stroked box is inside the face.

**Passes:** layout, pulse peak (HatchTestPulse 1.05 for Gift; the Shop/popup pulse buttons use their own amplitude, so pass `1.02`), and hover (HatchTestHover).

**Run matrix** (close and reopen between scale changes; MainMenu / StarterPackUI `HatchTestScale`):

| # | Target | Setup | Scroll / state | Scales |
|---|---|---|---|---|
| S1 | Shop | offer inactive | top | native, 0.7106, 0.6787, 1.0982 |
| S2 | Shop | offer active | top, SPEED (504), POTIONS (866), TREADMILL (1280), bottom (1248) | native, 0.7106 |
| S3 | Shop | `Pass_*` all true (local), SpeedBoosts 10, TreadmillTier 11 | top, SPEED, bottom | native |
| S4 | Shop | TreadmillTier 1 (hideRobux), refusals via dry run on 3 buttons (words held: `TestDryRunHold = true` keeps the word) | TREADMILL, POTIONS | native, 0.7106 |
| S5 | Shop | `TestPriceOverride = "1499"`; `IncomePerSec` / `SpeedMultiplier` local huge (boost titles `+12.5Qa`) | top, SPEED | native, 0.6787 |
| S6 | Shop | Gift picker open (TestGiftSelf + 1 row; with `TestPickerRows = 8` fake rows, Studio) | top | native, 0.7106 |
| P1 | Popup | normal (Magma) | | native, 0.7106, 0.6787, 1.1702 |
| P2 | Popup | restricted | | native, 0.7106 |
| P3 | Popup | last hour, refusal held, thanks (frozen before close: `TestThanksHold`) | | native |
| P4 | Popup | `HatchTestOdds` 6 and 7 | | native, 0.6787 |
| G1 | Gift | the Gift plan's A (Daily) and F (Playtime) runs | | native, 0.7106 |

**Expected:** 0 fails in every run. Paste the summary lines into the ledger.

### 7.6 Snapshots: other windows and Gift unchanged

- **`hatch_chrome_snapshot.lua` v2:**
  - The walker also skips `Window.ShopTabs` and `Body.GiftPicker`. PRE may be nil, "Gift" or "Shop".
  - Task 0 (before any change): save `hatch_chrome_before_v2.txt` (fresh session).
  - After the build: save `hatch_chrome_after_v2_fresh.txt`, `..._gift.txt` (PRE "Gift") and `..._shop.txt` (PRE "Shop").
  - **Expected:** the Rebirth, Index and Settings sections are byte-identical to BEFORE v2, with the same viewport. The Shop section differs by design (Hatch chrome); it is covered by 7.3.
- **`hatch_gift_snapshot.lua`** (new):
  - Fresh session, fresh save (Day 1 claimable). `OpenPage:Fire("Gift")`, wait 1 s, `GiftPage.HatchTestPulse = 1`, wait 3 frames.
  - Dump HatchBack, HatchFront and the GiftPage subtree, with the 8.6 property list.
  - Then `Tab = "Playtime"`, wait 0.5 s, and dump again.
  - **Volatile, not recorded:**
    - the Text / TextSize of labels whose Text matches `%d+:%d%d`;
    - the PlayBar `Time` and `Fill` size;
    - the Position of `Bats` children;
    - `Rotation` of `Rays`;
    - UIGradient `Rotation` / `Offset`;
    - the ImageTransparency of `TodayGlow`;
    - `ButtonScale` / `PopScale` / `BadgePulse`.
  - Task 0: `hatch_gift_before.txt`; end: `hatch_gift_after.txt`. **Expected:** identical (the FNV hash list, as 8.6).

### 7.7 `hatch_shop_perf.lua` (Client; TestFreshSave; offer active)

1. **idle:** Shop and popup closed for 3 s.
   - `HatchPerfShop` / `HatchPerfPopup` counters do not move.
   - `ShopLoop == false`, `RaysLoop == false`.
   - The ticker is not running (`StarterTicker == false`).
   - `ShopFunnelSent` does not change.
2. **cost:** Shop open, 300 frames while scrolling (`Tab_*` presses every 0.5 s); popup open 300 frames. Report avg / max ms per refresh tick and per frame.
   - **Targets:** Shop refresh ≤ 0.3 ms per tick (every 0.3 s); popup frame ≤ 0.05 ms avg.
3. **instances:** GuiObjects under ShopPage, StarterPackUI, GiftToast.
4. **leaks x30:** each cycle opens the Shop, presses 5 tabs, opens / closes the picker, opens / closes the popup (TestOpen + close), and closes the Shop.
   - GuiObject and instance counts flat; `PickerConns` 0; LuaHeap within +3 MB.
5. Write the results to `hatch_shop_perf_results.txt`.

### 7.8 `hatch_assets.lua`

Add to the preload list: 109535585247625, 93906069548754, 104087244878251, 135711525932647, `PotionConfig.TILE_ICON`, every `ShopConfig.Passes[i].icon`, 88694661500877, the `EGG_ICONS` values.

**Expected:** `failed 0`.

### 7.9 Regression suites (must stay green)

| Suite | Expected |
|---|---|
| `ServerStorage.StarterPackTests` pure (Edit, `:Clone()`) | 38/38 |
| `ServerStorage.StarterPackTests` live (own session) | 33/33 |
| `ServerStorage.StreakTests` pure / live | 24/24, 20/20 |
| `starter_hud_client.lua` sections layout, placement, envelope, motion, states, flicker, hover, content, overlaps, timer, expiry | pass (`S.popup` is retired, replaced by 7.4) |
| `streak_client.lua` v2 | all pass |
| `get_console_output` | no errors from ShopClient, StarterPackClient, MenuController, BrickUI, StreakClient, PlaytimeClient |

### 7.10 Screenshots (`screen_capture`; `docs/plans/hatch-night-build/popup_shop/`)

| File | Setup | Compare with |
|---|---|---|
| `shop_top.jpg` | S1/S2 top, offer active | `shop_top_pc.png` |
| `shop_speed.jpg`, `shop_potions.jpg`, `shop_bottom.jpg` | Tab presses | `shop_speed_pc.png` / `shop_potions_pc.png` / `shop_bottom_pc.png` |
| `shop_gift.jpg` | Picker open | `shop_gift_pc.png` |
| `shop_states.jpg` | S3 (OWNED / MAX / MAX LEVEL) | `sheet.png` |
| `shop_refusal.jpg` | S4 held refusal | `sheet.png` red button |
| `shop_phone_top.jpg`, `shop_phone_potions.jpg` | HatchTestScale 0.7106, crop the window | `shop_top_phone.png` / `shop_potions_phone.png` |
| `popup.jpg`, `popup_restricted.jpg`, `popup_urgent.jpg`, `popup_error.jpg`, `popup_thanks.jpg` | P1-P3 | `popup_*_pc.png` |
| `popup_phone.jpg` | HatchTestScale 0.7106 | `popup_phone.png` |
| `gift_after.jpg`, `rebirth_after.jpg`, `index_after.jpg`, `settings_after.jpg` | Unchanged windows | the Gift `v2_pc_mid.jpg` / today's look |
| `*_zoom.png` | 2-4x crops of: price groups, rail pill, BEST VALUE tags, odds strip, popup Buy | |

**Visual review:** a Haiku visual reviewer checks each set against the mockups and the owner's complaint list. Fix and re-shoot until it approves.

---

## 8. Build order

- [ ] **Task 0: pre-flight and BEFORE evidence.**
  - Edit; `TestFreshSave == true`.
  - Check that `ServerStorage.TestReceipt`, `ServerStorage.StarterDebug` and `ServerStorage.StarterPackTests` exist. `StarterPackTests` was found by `script_grep`. The other two are documented in memory, but no script text containing "TestReceipt" or "StarterDebug" turned up while this plan was written (they may be named in code another way). Write the real names and call signatures in the ledger.
  - Play (Client): run `hatch_chrome_snapshot.lua` v2 and save `hatch_chrome_before_v2.txt`.
  - Run `hatch_gift_snapshot.lua` and save `hatch_gift_before.txt`.
  - Capture `shop_before.jpg` and `popup_before.jpg` (TestOpen with an active offer). Stop Play.
- [ ] **Task 1: backups** (section 6.7) **and `ShopClientLegacy`** (section 6.6).
- [ ] **Task 2: BrickUI.Hatch extensions** (6.2) + `hatch_pure.lua` (RED, then GREEN) + the scroll probe (7.2, K into the ledger) + an in-engine `TextService` width table for every string in section 4.12 and the QA report's top 5 (ledger).
- [ ] **Task 3: BrickUI line + MenuController line.** Play: Rebirth / Index / Settings look unchanged. Shop opens on the night shell with the magenta band (content still old: expected).
- [ ] **Task 4: ShopClient rewrite** (6.4). Play: every section renders; dry-run every button; ScrollTo from GET MORE.
- [ ] **Task 5: StarterPackClient rebuild** (6.5). Play: the popup in all states (StarterDebug), the Shop card in the slot, HUD still opens the popup.
- [ ] **Task 6: tests.** 7.3, 7.4, 7.5 (whole matrix), 7.6, 7.7 and 7.8 in one session; 7.9 in their own sessions. Fix until all are green.
- [ ] **Task 7: screenshots + visual review loop** (7.10). Set `TestFreshSave = false` after the last Play test of the day.
- [ ] **Task 8: wrap-up.**
  - Ledger summary.
  - Update memory `slingshot-ui-style-hatch-night.md` (Shop + popup built), `roblox-shop.md` (new Shop layout, the dry-run hooks, the StarterSlot contract) and `roblox-starter-pack.md` (popup v4, the ticker / expiry).
  - Tell the owner: **Save + Publish**, plus the owner's calls.

---

## 9. Risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | ScrollingFrame under a UIScale: CanvasPosition units, bar thickness, AbsoluteCanvasSize | Task 2 probe (7.2), K factor, manual logical layout (no UIListLayout, no AutomaticCanvasSize). ScrollTo keeps today's 0.45 s delay |
| 2 | Shared helper edits leak into Gift | D17: additive opts, the old default paths kept and diffed (6.2 rule); `hatch_gift_snapshot.lua`; Gift containment runs G1 |
| 3 | The snapshot baseline changes (ShopTabs / GiftPicker removed) | Filter v2 + a NEW BEFORE captured with v2 before any change (Task 0) |
| 4 | A real Robux prompt opened during tests | D14 dry run on every path; the rules in 7.0; only `treadmillMoney` (in-game money) is invoked for real |
| 5 | The paid random item rule broken (odds hidden, cut or off-screen) | The popup is still the only buy path (the card Buy opens it); 7.4 check 6 incl. on-top sampling; restricted = no egg; D15 fallback = no offer |
| 6 | Popup double scaling | D11: no UIScale on the Holder; 7.4 check 1 asserts `SkinScale == CanvasScale == Holder px / 740` |
| 7 | Load order: StarterPackClient waits for `StarterSlot` | ShopClient creates the slot and its Visible listener together; the card is built when found (60 s WaitForChild); a legacy shop skips the card |
| 8 | Loops while closed / tests setting `Enabled = false` directly | Loops keyed on `Enabled` / `Visible` signals, not on `setOpen`; perf idle check; B18 |
| 9 | Long numbers: `$200T`, `+12.5Qa`, `x1.02K`, 4-digit regional prices | Sizes chosen with ≥ 17 % headroom (4.12); `H.fit` down to 16; S5 matrix with `TestPriceOverride` |
| 10 | GothamBlack width vs the mockup font | In-engine table in Task 2; mockup font is ~14 % wider (conservative); TextFits / textWidth checks |
| 11 | 667x375 phones: 10.9 pt minimum | Accepted, as for Gift (its risk 10) |
| 12 | Analytics semantics change (poll -> events) | 7.3 check 9 counts the fires; ancestors covered (page, Body, Face, Window, MainMenu.Enabled) |
| 13 | Phone scrolling: drags start on buttons | ScrollingFrame cancels Activated on drag (engine behaviour); hits are full-width; verify by hand in the emulator (owner, optional) |
| 14 | Instance count (~1000 GuiObjects Shop + ~260 popup) | Built once, never rebuilt (except picker rows); perf 7.7 |
| 15 | The ShopClientLegacy copy drifts from the live logic over time | It only runs if Hatch fails; note in `roblox-shop.md` that Shop logic changes must also be made there, or the legacy copy deleted after a few stable weeks (owner's call 6) |
| 16 | The `clock` asset is third-party | Already loads for Gift; 7.8 preload; fallback = hide the clock sticker (boosts still read) |
| 17 | The owner prefers the old SpeedBoostCards product art ("I like the style", 2026-10-05) | Owner's call 3 |
| 18 | Another agent / the owner in Play | `get_studio_state` before every step; tests are read-only on the GUI except the documented local attributes |

---

## 10. Owner's calls and owner actions

**Owner's calls (defaults in bold):**

1. **Band colour: Shop and popup magenta all year** or Pumpkin during Halloween. Pumpkin is one line: `H.PAGE_BAND.Shop = nil` while HalloweenDecor exists.
2. **Tabs: left rail inside the window** or a top segmented pill (row 2 like Gift; 5 x 140, costs 46 px of scroll height).
3. **Speed boost art: frameless stickers** (shoe / potion + clock) or the old square product tiles from SpeedBoostCards (87962104425261 ...) inside the cards.
4. **Popup size: the full 740 x 470 window** or a smaller 600 x 420 popup (re-layout needed; not planned).
5. **BUY breathing 1.00..1.02: on** or off.
6. Keep **`ShopClientLegacy`** as a safety net, or delete it after the new Shop has been live for a week.

**Owner actions after the build:**

1. **Save + Publish** (File > Publish to Roblox). Nothing is live until then.
2. Optional: look at the phone layout in the device emulator (Test > Device, iPhone landscape).
