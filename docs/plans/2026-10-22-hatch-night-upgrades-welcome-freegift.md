# HATCH NIGHT Upgrades + Welcome Back + Free Gift: implementation plan (2026-10-22)

> **For the builder (Opus):** follow this plan task by task. Every number is final and matches the mockups.
> If Studio contradicts a number, stop and write the conflict in the ledger
> (`docs/plans/style-2026-10-21/uwf/progress.md`, create it in Task 0) before changing anything.
> Pipeline (owner rule): this plan -> Haiku plan reviewer -> build (3 runs, section 9) -> Haiku visual reviewer per screenshot
> set -> fixes -> Haiku lineup reviewer.

**Goal.** Rollout step 3 of HATCH NIGHT phase 2: give the three **walk-in / pop-up windows that live outside MainMenu** the game's
own style:
- **Free Gift** (`PlayerGui.FreeGiftUI`, `FreeGiftClient`): like + join the group -> 3 potions once.
- **Welcome Back** (`PlayerGui.OfflineUI`, `OfflineClient`): offline earnings, CLAIM / CLAIM x5 (39 R$, product 3718679677).
- **Upgrades** (`PlayerGui.UpgradeUI`, `UpgradeClient`): the walk-in stall window, Slingshot Power / Fast Grab / Wave Shield,
  the money buy and the Robux +1 LV.

The owner's rules for this step:
- "Their own unique style, applied to ALL UIs, window by window."
- "restore it, but new design. just the layout how it looked": **each window keeps its current layout and content; only the
  look changes.** Where the current layout breaks a style rule (min text 16, the 83 % fill, 8 px gutters, outlines inside the
  box), this plan says what moves and why (tables "Kept vs moved").
- Acceptance = the same as Gift / Shop / Settings / Index / Rebirth: no overlaps, every outline inside its box, no text hovering
  over text, every line of copy at most 83 % of its box, nothing "basic". **Timers have no background** (none of these three
  windows has a timer).

**Sources (read before building):**
- Spec `docs/specs/2026-10-21-slingshot-ui-style.md` (sections 2, 4, 6).
- The RIS plan + review + ledger: `plans/2026-10-21-hatch-night-rebirth-index-settings{,.review}.md`,
  `plans/style-2026-10-21/ris/progress.md`. The popup/Shop plan + reviews + ledger (`plans/2026-10-21-hatch-night-popup-shop*.md`,
  `plans/style-2026-10-21/popup_shop/progress.md`): the Starter Pack popup is the template for a HATCH window **outside**
  MainMenu (`H.windowChrome(holder)`, fit into MainMenu's safe box, `off = mm.AbsolutePosition - gui.AbsolutePosition`, Size
  pop instead of a UIScale, dry-run hooks).
- **Mockups (the builder must match them):** `docs/plans/style-2026-10-21/uwf/`
  - PC 1920x1080: `freegift_pc.png` (not in the group), `freegift_joined_pc.png`, `freegift_claimed_pc.png`,
    `freegift_refusal_pc.png`, `welcome_pc.png`, `welcome_big_pc.png` ($12.5Qa + a 4-digit price), `welcome_x5_pc.png`,
    `welcome_refusal_pc.png`, `upgrades_pc.png` (mid game), `upgrades_free_pc.png` (tutorial step 8 + guide),
    `upgrades_step10_pc.png`, `upgrades_max_pc.png`, `upgrades_refusal_pc.png`, `sheet_pc.png` (every button state).
  - Phone 844x390: `freegift_joined_phone.png`, `welcome_phone.png`, `upgrades_phone.png`, `upgrades_free_phone.png`; strip
    `sheet_phone.png`. 1050x620: `*_1050.png`, strip `sheet_small.png`. 667x375: `*_667.png`, strip `sheet_667.png`.
  - **Current vs new:** `compare_freegift.png`, `compare_welcome.png`, `compare_upgrades.png` (`make_compare.py`). The current
    Free Gift / Welcome Back images are the 2026-10-15 review captures (`docs/reviews/2026-10-15-*-ui/current_v2.jpg`, the
    live v2 layouts). **No capture of the live Upgrades window exists** (built at run time; the planner may not Play):
    `current_upgrades_1519.png` is a reconstruction from UpgradeClient's numbers (`current_upgrades.html`). Task 0 shoots
    the real one and re-runs `CUR_UPGRADES=<shot> python make_compare.py`.
  - Sources: `uwf.html` + `uwf.js` + `engine.js` (a copy of `../ris/engine.js` with per-window logical sizes, the Upgrades
    big-PC cap, the right-tile clearance and the tutorial guide). `bash render.sh qa` re-renders; output in `qa_report.txt`.
  - **QA result: 26 views (14 PC, 4 phone, 3 x 1050, 3 x 667, + sheet), 0 OUT, 0 OVERLAP, 0 gap < 8, 0 text overflow,
    every fill <= 83 %.** Tightest: "ONE-TIME GIFT!"@16 83 % (the tag is sized from it), "TEST SAVE ONLY"@26 82 %,
    "JOIN THE GROUP FIRST!"@17 81 %, "CELESTIAL"@16 77 %, "SURVIVE 1 WAVE HIT"@16 76 %, "30 MIN EACH • USE ANYTIME!"@16 75 %.
    Min text: 18.9 px PC, 16.2 px Upgrades at 1050x620, 11.4-11.6 pt phone (9.3 pt Upgrades in tutorial steps 8/10, section 6.5).
  - Stand-in art: the group icon (drawn; the build uses Check-UI `4 Players 1st` 137195579182647), the 👍 (system emoji, as
    today), Roket / Bolt / Heart / Boost / Locked from `Downloads/Verctor` (the same pack as the live ids), the tutorial arrow
    (the right arrow rotated; the build uses the down arrow 93838363576146 at Rotation 90).
- Code read for this plan (read-only, `script_read` / `script_grep`): FreeGiftClient, FreeGiftServer, OfflineClient,
  OfflineServer, OfflineConfig, UpgradeClient, UpgradeServer, UpgradeConfig, ShopConfig (UpgradeProducts, ROBUX_ICON,
  studioFree), Receipts (TestReceipt), BrickUI.Hatch (all 1092 lines), BrickUI (PAGE_SKIN), MenuController (fit, tutorialTop,
  applySkin), StarterPackClient (popup fit / motion / dry run), TutorialClient (steps 8 / 10 / 11, the Guide), StreakClient
  (auto-open), RebirthClient HUD (`windowOpen`), StarterPackHud (`MODALS`), PetsEggsUI (`RightTiles`, `tilesAway`),
  HubV2Tests (zone positions), the test files in `docs/plans/tests-2026-10-21/`.

**Out of scope (do not touch):** Lighting, the hub / map (stalls, chest, PadRings, zones, the FREE! sign BillboardGui),
every server script (FreeGiftServer, OfflineServer, UpgradeServer, TutorialServer, Receipts, PlayerData), OfflineConfig,
UpgradeConfig, ShopConfig, every window already built (Gift: StreakClient / PlaytimeClient; Shop: ShopClient / StarterPackClient /
StarterPackHud; Settings: SettingsClient; Index: IndexClient; Rebirth: RebirthClient), MenuController, TutorialClient,
PetsEggsUI, and these **frozen regions** inside the three scripts: OfflineClient's "You earn $X/Day offline!" base line,
UpgradeClient's Fast Grab prompt tuning + Wave Shield bubble + ShieldToast, FreeGiftClient's FREE! sign bob / fade + sparkles
(section 4.6 / 5.6 / 6.6 diff rules).

---

## 0. Decisions (read first)

| # | Decision | Why |
|---|---|---|
| D1 | **The switch is `BrickUI.PAGE_SKIN`** with three new keys `FreeGift`, `WelcomeBack`, `Upgrades` (one key per task, flipped in the same sitting as that window's new script). `B.skinFor(key)` is read by the window script itself. MenuController only reads keys of its own `PAGES`, so the new keys never reach it. | One line per window, the same switch as every other HATCH window. A key on "Hatch" with the old script would do nothing (the old scripts never read it), so a half-built state is harmless. |
| D2 | **Each window keeps its own logical size** (today's Check-UI canvas): Free Gift **560 x 460**, Welcome Back **540 x 430**, Upgrades **740 x 470** (its 1.6 aspect = the standard HATCH window). The chrome gets `opts.w / opts.h` (`H.windowChrome`), the fit gets `lw / lh` (`H.fitWindow`). | "Just the layout how it looked": every zone stays at today's logical position; on big PCs the two small windows are exactly today's size (1.18 x 560 = 661 px, 1.18 x 540 = 637 px). |
| D3 | **Band colours** (each window its own, spec 4 "other pages keep their own band colours"): **Free Gift = emerald** (new `H.BAND.FreeGift`, the lime FREE! sign / pad ring family but deeper than the lime CLAIM), **Welcome Back = gold** (`HatchGold`, today's gold header), **Upgrades = royal blue** (new `H.BAND.Upgrades`, the blue stall ring). | Today Free Gift and Upgrades both use the Codes cyan, which is now the Index band (owner's call 1). |
| D4 | **Fit = a standalone HATCH window** (`H.fitStandalone`, 7.1 item 9): centred in MainMenu's safe box, clear of the **left HUD** (the MenuController rule: menu tiles + Speed/Money pills + 6) **and of the right tile column** (`PetsEggsUI.RightTiles`: those tiles slide away only for MainMenu windows), cap 1.18; Upgrades gets the big-PC cap (D5); a visible tutorial guide moves the window down first and shrinks it only by what is missing (`H.tutorialFit`, the Rebirth step-11 recipe). No backdrop (walk-in windows, as today). | Same fit as every HATCH window, plus the right tiles that MainMenu windows never meet. |
| D5 | **Upgrades as big as today on big PCs**: `H.PAGE_CAP_R.Upgrades = R_U`, measured in Task 0 (today's window = 0.62 of the full screen: expected **466.9 / 695 = 0.6718** at Studio 1519x753). 1080p: s 1.4608, 1081 x 687 (today 1071 x 670). Free Gift / Welcome Back: plain 1.18 cap (= today's deviceScale clamp). | The RIS D4 ruling (owner's call 1 there: "as big as today"). |
| D6 | **Fixed-width gloss buttons, one width in every state** (review MUST 5 lesson): Free Gift CLAIM 260, JOIN 134; Welcome Back CLAIM x5 276, CLAIM 216; Upgrades Buy 156, Robux 118. States only change palette / text / visibility; nothing resizes. Neighbours 8 px apart use `hoverScale = 1` (the gloss brightens instead: the Rebirth SKIP / REBIRTH ruling). | `H.glossButton` sizes its parts once at build. |
| D7 | **Purchases are gold `H.priceButton`s** (Robux hex + live price as one centred group); in-game money buys are **lime** (`priceButton` with the cash glyph, D8); locked = **off** + lock glyph; MAX / CLAIMED = **silver**; refusals = **red** 1.2-1.3 s; JOIN = **violet** (social, like Shop gifting); "can't afford" = **off** (owner's call 3: today it is red). | Spec 4 button roles; the Shop / Rebirth precedent. |
| D8 | `H.priceButton` gets 3 additive options: `glyphImage` (default the Robux hex; Upgrades Buy uses the cash 131724750673548 / lock 124356037818343), `top` + `topSize` (a fixed line above the group: Upgrades "+1 LV"), and `btn.setGlyph(img)`. Default paths byte-identical (pure A/B test U8). | The +1 LV button keeps today's 2-line content inside its own face; the money button shares the price-group layout (centred, steps down to 16). |
| D9 | **Re-layouts forced by the rules, nothing else** (tables 4.3 / 5.3 / 6.3): Free Gift's one-line "x2 MONEY • x2 HATCH • x2 SPEED" becomes a 3-row list with potion icons (one row needs 310 > 304 px at 16 px); the red hint line becomes the CLAIM button's refusal word (8 px gutters leave no row for it); Welcome Back's price tag moves **into** the x5 button (it hung over the button's corner: "corners aren't even in the box"); Upgrades' long sentences get short copy and the stat becomes `now > next` (min 16 px in a 336 px column). | Spec 2.1 / 2.3. |
| D10 | **A one-line switch for every content change** (top of each script): Upgrades `FULL_COPY = false` (true = today's sentences, down to 12 px), `SHORT_RED = false` (true = red when you can't afford, today's colour), `HIDE_ROBUX_IN_TUTORIAL = true` (the Sling row's +1 LV hides while the step-10 arrow points at the $ button); Welcome Back `X5_STYLE = "gold"` (`"rainbow"` = today's rainbow face); Free Gift `THUMB_EMOJI = true` (false = the heart icon 108186731829732 instead of 👍). | Repeated review lesson: the owner can undo any copy / colour change in one line. |
| D11 | **Nothing runs while closed** (owner's lag rule, review MUST 2 of the Shop): one RenderStepped per window, connected only while its gui is `Enabled` (rays 12 deg/s, the breathing button, the tutorial arrow bob); Upgrades' refresh = a 0.5 s token loop only while open, `Money` only marks dirty, level / rebirth / FreeSling attributes refresh at once if open, else mark dirty (refresh on open). Today: 3 forever RenderSteppeds (one per script) + UpgradeClient's forever 1 s loop. | Measured by `hatch_uwf_perf.lua`. The 0.15 s walk-in zone polls (world triggers) and the FREE! sign bob (world) stay as they are (out of scope; noted for the HUD/world batch). |
| D12 | **Tests never open a real Robux or Roblox prompt.** Studio-only dry run on the window's gui: `TestDryRun = true` makes the Upgrades +1 LV press record `{"Upgrades.Buy", kind, "robux"}`, the Welcome Back x5 record `{"PromptProductPurchase", 3718679677}`, and the Free Gift JOIN (and the auto-join after a "group" refusal) record `{"PromptJoinAsync", GROUP_ID}` in `TestLastBuy`, with `TestDryRunResult` as the reply. `TestPress` refuses (warn) every Robux / join key unless `TestDryRun == true`. Receipts go through `ServerStorage.TestReceipt:Invoke(player, productId)`. | Owner rule. `Upgrades.Buy(kind, "robux")` calls `PromptProductPurchase` on the SERVER, so the guard must be on the client before the remote. |
| D13 | **Welcome Back celebrates on the attribute, not only on the prompt**: while open, `OfflineLastX5` turning true (and not yet celebrated this welcome-back) runs the x5 celebration (amount x5, shards, HatchWin, close after 1.4 s). The `PromptProductPurchaseFinished` path is kept for `prompting`; a `celebrated` flag stops a double run. | TestReceipt never fires `PromptProductPurchaseFinished`; a late live receipt also shows. |
| D14 | **The window sinks clicks**: `Holder` is a TextButton (Text "", transparent, `HatchBlocker`) as the popup's. | Today the Window is a Frame: a click inside it falls through to the world and click-to-move walks the character out of the zone (memory: "a click that misses the UI lands in the world"), which closes the window. |
| D15 | **Decide first, then build, then the frozen parts.** Each script: requires -> fallback decision (no `B.Hatch`, key not "Hatch", Studio `workspace.Test<Key>Legacy == true`) -> `pcall(build)` -> on failure destroy + fallback -> only then the frozen regions + logic. Fallback = enable the disabled byte copy `<Script>Legacy` and `return` before any frozen region runs. | The legacy copy runs the whole old script (frozen parts included) exactly once; the RebirthClient precedent (return before the HUD). |
| D16 | **Shared helpers are additive** (7.1); every old default path byte-identical, proved by A/B pure tests against `BrickUI_preUWF.Hatch` (hatch_pure U2 / U5 / U7 / U8) and by the Gift / Shop / Settings / Index / Rebirth snapshots (8.6). MenuController is not edited. | Five built windows share these helpers. |

---

## 1. Files

| Instance | Action |
|---|---|
| `ReplicatedStorage.BrickUI` | 1 line, edited 3 times (Tasks 4 / 5 / 6): `BrickUI.PAGE_SKIN = {Gift = "Hatch", Shop = "Hatch", Settings = "Hatch", Index = "Hatch", Rebirth = "Hatch", FreeGift = "Hatch"}` (+ `WelcomeBack`, then `Upgrades`). Comment: "phase 2 step 3 (2026-10-22): Free Gift / Welcome Back / Upgrades (standalone windows read their own key). Plan docs/plans/2026-10-22-hatch-night-upgrades-welcome-freegift.md". Nothing else. |
| `ReplicatedStorage.BrickUI.Hatch` | Additions of section 7.1 (Task 3). |
| `StarterPlayer.StarterPlayerScripts.FreeGiftClient` | Window region rewritten; world region kept (4.6). |
| `StarterPlayer.StarterPlayerScripts.OfflineClient` | Window region rewritten; base-line region byte-identical (5.6). |
| `StarterPlayer.StarterPlayerScripts.UpgradeClient` | Window region rewritten; Fast Grab + Wave Shield regions byte-identical (6.6). |
| `StarterPlayer.StarterPlayerScripts.FreeGiftClientLegacy`, `OfflineClientLegacy`, `UpgradeClientLegacy` | NEW: disabled byte copies of today's scripts, tags stripped, attribute `Note = "Fallback only: the new script enables this if BrickUI.Hatch fails"`. Each made at the start of its window's run (and checked equal to its `_preUWF` backup). |
| `ServerStorage._Backup_HatchNight.Before` | `FreeGiftClient_preUWF`, `OfflineClient_preUWF`, `UpgradeClient_preUWF` (Enabled false), `BrickUI_preUWF` (with `Hatch`); attributes `WasEnabled_preUWF`, `HowToRestore_preUWF` (Task 1). |
| `ServerStorage.HatchUWFTests` | Test mirrors (the `HatchRISTests` recipe: ModuleScripts with a `Note` attribute, copied to ReplicatedStorage at run time only, FNV-checked against the local files). |
| `docs/plans/tests-2026-10-21/` | New: `freegift_client.lua`, `welcome_client.lua`, `upgrade_client.lua`, `hatch_pages_snapshot.lua`, `hatch_uwf_perf.lua`. Changed: `hatch_pure.lua` (+ block UWF, 8.1), `hatch_containment.lua` (v4, 8.2), `hatch_assets.lua` (+ ids, 8.8). Results: `hatch_pages_before_uwf.txt` / `_after_uwf.txt`, `hatch_gift_*_uwf.txt`, `hatch_shop_*_uwf.txt`, `hatch_chrome_*_uwf.txt`, `hatch_uwf_perf_results.txt`. |
| `docs/plans/hatch-night-build/uwf/{freegift,welcome,upgrades}/` | Screenshots (8.10). |
| `docs/plans/style-2026-10-21/uwf/progress.md` | The build ledger. |

---

## 2. Architecture

```
PlayerGui.FreeGiftUI / OfflineUI / UpgradeUI   (ScreenGui: same names, ResetOnSpawn false, IgnoreGuiInset true, DisplayOrder 20,
                                                ZIndexBehavior Sibling, Enabled = open; Studio attributes: section 4.6 / 5.6 / 6.6)
  Holder  TextButton (HatchBlocker), AnchorPoint 0.5, Offset size lw*s x lh*s at H.fitStandalone's spot (MainMenu safe box -> gui space)
    HatchBack  Z0  night shell        \  H.windowChrome(Holder, {bats = false, w = lw, h = lh}); setTheme(H.bandTheme(key));
    HatchFront Z2  band, teeth, icon,  /  icon.Image = the window icon; setTitle(...); show(true). Upgrades: + RebirthPill in HatchFront
                   title, red X (CloseHit)
    Canvas     Z1  Frame lw x (lh - 7), UIScale CanvasScale = Holder px / lw (H.bindCanvasScale), attribute HatchCanvas = true
      ... the window's content (sections 4.1 / 5.1 / 6.1); Fx (Z20) for shards
```
- Open: `Holder.Size` tweens 0.85 x -> 1 x (Quad Out 0.2 s; no UIScale on the Holder or above: SkinScale / CanvasScale follow
  it, popup D11). Close: as today (walk-in windows close at once; Welcome Back keeps its 0.15 s shrink then closes).
- Refit: on open, on `MainMenu.AbsoluteSize` change while open, on the gui's `HatchTestScale`, and (Upgrades) on `TutorialExtra`
  / `FreeSling` / `SlingLevel` changes and the guide's `Visible` while open.
- Rendering / input: every Frame / TextLabel / ImageLabel `Active = false`; only GuiButtons take input. HatchFront holds only
  `CloseHit` as a button.

---

## 3. Window fit (all three)

`H.fitStandalone(gui, mm, lw, lh, {cap})` (7.1 item 9):
1. `left, right = H.hudClear(pg, mm)` = the MenuController formula `max(rightEdge(Menu), rightEdge(SpeedUI.Holder)) + 6`, and
   `right` = `mm.AbsoluteSize.X - (RightTiles.AbsolutePosition.X - mm.AbsolutePosition.X) + 6` while `PetsEggsUI.RightTiles` is
   visible and on screen (else 8).
2. `s, w, h, _, cy = H.fitWindow(gs.X - right + 8, gs.Y, left, cap, lw, lh)` (the usable width ends 6 px left of the tiles).
3. `cx = max(left + w/2, min(gs.X/2, gs.X - right - w/2))` (centred when it can be, else pushed off the HUD side).
4. Studio `gui.HatchTestScale` (number): `s` forced, `w, h = lw*s, lh*s`, centred (the MainMenu switch's behaviour).
5. `top = H.guideClear(pg, mm)` (the TutorialUI guide's visible text bottom + 6, or nil): `s, w, h, cx, cy = H.tutorialFit(s, cx, cy, gs.Y, top, lw, lh)`.
6. `off = mm.AbsolutePosition - gui.AbsolutePosition`; `Holder.Position = (off.X + cx, off.Y + cy)`, `Size = (w, h)`.

`right` is an **estimate until Task 0 measures `RightTiles`** (from the 1519x753 capture: tiles' left edge 1437 -> right 88;
scaled by gui height: 1080p 126, 1050x620 72.3, 844x390 57.3 incl. the phone UIScale 1.3, 667x375 55). Task 0 writes the
measured values; only the Upgrades rows at 1050x620 / 667x375 depend on them.

| Screen (gui, left / right) | Free Gift 560 x 460: s, px, (cx, cy) | Welcome Back 540 x 430 | Upgrades 740 x 470 (cap 0.6718) | Min text (FG 16 / WB 26 / UP 16 logical) |
|---|---|---|---|---|
| PC 1920x1080 (1920x1022, 412.1 / 126) | **1.18**, 660.8 x 542.8, (960, 511) = today | **1.18**, 637.2 x 507.4, (960, 511) = today | **1.4608**, 1081.0 x 686.6, (960, 511) | 18.9 / 30.7 / 23.4 px |
| Studio 1519x753 (1519x695, 284.2 / 88) | **1.18**, 660.8 x 542.8, (759.5, 347.5) | **1.18**, 637.2 x 507.4, (759.5, 347.5) | **1.18**, 873.2 x 554.6, (759.5, 347.5) | 18.9 / 30.7 / 18.9 px |
| **PC 1050x620** (1050x562, 229.3 / 72.3) | **1.18**, **660.8 x 542.8**, (559.7, 281); top-left (229.3, 9.6) | **1.18**, **637.2 x 507.4**, (547.9, 281); (229.3, 27.3) | **1.0114**, **748.4 x 475.4**, (603.5, 281); (229.3, 43.3) | 18.9 / 30.7 / 16.2 px |
| Phone 844x390 (732x346, 144.3 / 57.3) | **0.7261**, 406.6 x 334.0, (366, 173) | **0.7767**, 419.4 x 334.0, (366, 173) | **0.7106**, 525.9 x 334.0, (407.24, 173) | 11.6 / 20.2 / 11.4 pt |
| Phone 667x375 (667x331, 137.9 / 55) | **0.6935**, 388.3 x 319.0, (333.5, 165.5) | **0.7419**, 400.6 x 319.0, (338.2, 165.5) | **0.6407**, 474.1 x 301.1, (374.95, 165.5) | 11.1 / 19.3 / 10.3 pt (accepted, Gift risk 10) |

**Tutorial guide visible (Upgrades in steps 8 / 10; any window if a tutorial player opens it):** guide text bottom (RIS run C
measurements): Studio 142.6 -> clear 148.6 -> Upgrades s **1.1498**, 850.9 x 540.4, cy 418.8; 1050x620 120.4 -> 126.4 ->
s **0.914** (14.6 px text); 844x390 61.5 -> 67.5 -> s **0.5798** (9.3 pt, owner's call 7); 1080p 147.5 -> no change (window top
167.7 > 153.5). Free Gift at Studio with a guide: s 1.1748.

**Exact px = logical x s.** 1050x620: Free Gift / Welcome Back x 1.18 (16 -> 18.9, 18 -> 21.2, 22 -> 26.0, 26 -> 30.7, 30 -> 35.4,
34 -> 40.1, 52 -> 61.4 px); Upgrades x 1.0114 (16 -> 16.2, 18 -> 18.2, 20 -> 20.2, 22 -> 22.3, 26 -> 26.3 px).

---

## 4. Window 1: FREE GIFT (build first)

### 4.0 Current layout inventory (FreeGiftClient v2, `docs/reviews/2026-10-15-freegift-ui/current_v2.jpg`)

| Zone | Today (logical px of a 560 x 460 window, deviceScale UIScale) |
|---|---|
| Window | slate canvas + damier, 3.5 border, centred on the screen, DisplayOrder 20, opened by the walk-in `FreeGiftZone` (radius 7.5) on the chest pad; once claimed the pad no longer opens it |
| Header (0..60) | Codes cyan checker header, gift icon 46 at (42, 29), "FREE GIFT!" left at x 74, 3D red [X] |
| Art (left) | 3 potions (Money -14 deg 86, Speed +14 deg 86, Hatch 108) over a 230 px turning sunburst, centred (118, 140) |
| Headline (right, centre x 378) | "~ ONE-TIME GIFT! ~" red gradient; "3 POTIONS!" cyan->green 58 tall; RichText "x2 MONEY • x2 HATCH • x2 SPEED"; "30 MIN EACH • USE ANYTIME!" |
| Steps | 2 cards 254 x 130 at centres (145, 290) / (415, 290): "1. Like the game!" (👍 + "Click LIKE on the game page!"), "2. Join the group!" (group icon + cyan JOIN, or JOINED! + check) |
| Hint | red line at y 367 ("Join the group first, then press CLAIM!" / "Loading your data... try again in a second!", 3 s) |
| CLAIM | 236 x 56 at (280, 408): lime CLAIM! / silver CLAIMED! |
| Logic | `checkGroup` (IsInGroup), `claimed()`, `refresh()` (+ sign / sparkles), `promptJoin` (GroupService:PromptJoinAsync), the claim handler (ok -> HatchWin, pop, sparkles burst, potions pop; "group" -> hint + shake + promptJoin; "claimed"; "wait"), `setOpen` (CloseWindow / WindowOpened), the 0.15 s zone poll, one forever RenderStepped (sign bob / fade + sunburst) |

### 4.1 HATCH NIGHT version (logical px; canvas 560 x 453; `freegift*_pc.png`)

**Chrome:** `H.windowChrome(holder, {bats = false, w = 560, h = 460})`, `setTheme(H.bandTheme("FreeGift"))` (emerald),
`icon.Image = GIFT_ICON 128336310005291`, `setTitle("Free Gift!")`. Teeth `H.headerTeeth(560)` (28 teeth, centres 16..544),
X at (514, 6, 34, 34), CloseHit 56 x 56 centred (532, 28), title box (58, 10, 400, 26).

| Name | Class | rect (x, y, w, h) | Z | Look |
|---|---|---|---|---|
| Rays | ImageLabel `H.ICON.rays` | (42, 74, 164, 164), Fit | 1 | ImageColor3 (190,150,255), ImageTransparency 0.5, `HatchRadial`; 12 deg/s only while open |
| Glow | `H.glow` | (14, 76, 220, 160) | 2 | `H.GLOW.potions`, 0.35 |
| Art | Frame, AnchorPoint 0.5 | centre (124, 150), 228 x 168 (= 10..238, 66..234); UIScale `PopScale` | 3 | transparent |
| Art.PotionMoney | `H.sticker` | (20, 56, 84), Rotation -14 | 3 | `PotionConfig.byKey.Money.icon`; rotated box 21.1..122.9 x 113.1..214.9 (canvas) |
| Art.PotionSpeed | sticker | (124, 56, 84), Rotation 14 | 4 | `.Speed.icon`; 125.1..226.9 |
| Art.PotionHatch | sticker | (60, 20, 108) | 5 | `.Hatch.icon`; canvas 70..178 x 86..194 |
| Tag | `H.tag` | (398 - tw/2, 72, tw, 22), tw = even(`H.textWidth("ONE-TIME GIFT!", 16)` / 0.83 + 5) | 4 | red tag, label "ONE-TIME GIFT!" (fill 0.83) |
| Headline | text @34, stroke 3 | (246, 100, 304, 34) | 4 | UIGradient (0,225,255) -> (40,240,130): "3 POTIONS!" |
| ListIcon1..3 | sticker 20 | (345, 141 + 22 (i - 1), 20) | 4 | Money / Hatch / Speed potion icons |
| List1..3 | text @16, left | (371, 142 + 22 (i - 1), 110, 16) | 4 | "x2 MONEY" (255,215,60), "x2 HATCH" (120,240,90), "x2 SPEED" (90,200,255) |
| Each | text @16 | (246, 212, 304, 16) | 4 | (225,235,245): `{"30 MIN EACH • USE ANYTIME!", "30 MIN EACH!"}` |
| Like / Group | `H.shellCard` noHit, noHover, tile "steps" | (10, 240, 266, 130) / (284, 240, 266, 130); face 266 x 125 | 2 | |
| *.Title | text @18 | (8, 8, 250, 18) | 2 | `{"1. LIKE THE GAME!", "1. LIKE US!"}` / `{"2. JOIN THE GROUP!", "2. JOIN GROUP!"}` |
| *.Well | `H.recess` | (8, 34, 250, 82), radius 14 | 2 | `HatchPad 8` |
| Like.Well.Thumb | TextLabel (THUMB_EMOJI) | (8, 17, 48, 48), TextSize 40, no stroke | 3 | "👍" (false: `H.sticker` heart 108186731829732) |
| Like.Well.How1 / How2 | text @16, left | (62, 20, 180, 16) / (62, 42, 180, 16) | 3 | "CLICK LIKE ON" (touch: "TAP LIKE ON") / "THE GAME PAGE!" |
| Group.Well.Icon | sticker | (8, 17, 48) | 3 | GROUP_ICON 137195579182647 |
| Group.Well.Join | glossButton violet | (100, 19, 134, 44); d 4, r 12, ol 2.5, size 22, "JOIN" | 4 | label HatchFill 0.83; hover 1.04 (137.3 wide max: ends 236.7 < 242) |
| Group.Well.Joined | text @22, left | (64, 30, 136, 22) | 3 | `H.LIME_TXT` "JOINED!" |
| Group.Well.Done | sticker | (206, 27, 28) | 4 | `H.ICON.check` |
| Claim | glossButton | (150, 382, 260, 60); d 4, r 12, size 30 | 5 | label HatchFill 0.83; states 4.2; breathing 1.00..1.03 (`pulseAmp 0.015`, 1.2 s) only in the "joined" state |
| Fx | Frame | (0, 0, 560, 453) | 20 | `H.shards(fx, 124, 150)` on a claim |

Vertical stack: band 0..46 (teeth to ~62), art 66..234, list to 206, Each 212..230, cards 240..370, CLAIM 382..442 (11 px
bottom margin; at the 1.03 peak 381.1..442.9, 10.1 px).

### 4.2 States

| State | Steps | CLAIM | Motion |
|---|---|---|---|
| Not in the group (client `joined == false`; Studio `TestJoined = false`) | JOIN violet | **off** "CLAIM!" (LAV_DIM), pressable: the server's reason shows | none |
| In the group | JOINED! + check | **lime** "CLAIM!", breathing | rays + breathing |
| Refusal "group" | JOIN (joined reset) | **red** `{"JOIN THE GROUP FIRST!", "JOIN FIRST!"}` 2.0 s; the Group card shakes (today) and `promptJoin()` runs (dry-run aware) | |
| Refusal "wait" / "slow" | | red `{"LOADING... TRY AGAIN!", "TRY AGAIN"}` 1.3 s | |
| Claimed | JOINED! | **silver** "CLAIMED!", `Active = false` | potions pop (PopScale 1 -> 1.1 -> 1, Back 0.4), shards, HatchWin, sparkles burst (today) |

### 4.3 Kept vs moved

| Kept (same zone, same order) | Moved, and why |
|---|---|
| Header with the gift icon + title + X; potion art left over turning rays; tag + "3 POTIONS!" + the x2 line + "30 MIN EACH" right; the 2 step cards with the same titles, thumb, "Click LIKE on the game page", group icon, JOIN / JOINED! + check; CLAIM centred below; the walk-in open / close; JOINED / CLAIMED behaviour; claimed = no sign / sparkles, pad doesn't reopen | **x2 line -> 3 rows** with potion icons: one row at the 16 px minimum needs 3 x 98 + gaps = 310 > 304. **Red hint line -> the CLAIM word** (2 s): between the cards (370) and CLAIM (382) there is no 8 px-gutter row for a 16 px line. **The "~ ~" tildes -> a red tag** (not rotated, inside its box). **Cyan header -> emerald** (D3). **Check-UI checker cards -> shell cards with recessed wells.** |

### 4.4 Exact sizes at 1050x620 (s 1.18; window 660.8 x 542.8 at (229.3, 9.6))

| Element | Logical | Px |
|---|---|---|
| Step card / well | 266 x 130 / 250 x 82 | 313.9 x 153.4 / 295.0 x 96.8 |
| CLAIM / JOIN | 260 x 60 / 134 x 44 | 306.8 x 70.8 / 158.1 x 51.9 |
| Hatch potion / side potions | 108 / 84 | 127.4 / 99.1 |
| Text 16 / 18 / 22 / 30 / 34 | | 18.9 / 21.2 / 26.0 / 35.4 / 40.1 px |

### 4.5 Phone checks (844x390, s 0.7261; `freegift_joined_phone.png`)

- CLAIM 188.8 x 43.6 pt; JOIN 97.3 x 31.9 pt; CloseHit 40.7 pt. All >= 31 pt.
- Window 406.6 x 334 at gui (162.7..569.3, 6..340): clear of the left HUD (144.3) and the right tiles (est. 674.7).
- Min text 11.6 pt ("ONE-TIME GIFT!" 16). 667x375: s 0.6935, 11.1 pt.
- The 👍 is the platform emoji (as today); Android shows its own glyph.

### 4.6 Code plan (FreeGiftClient)

**Top switches:** `local THUMB_EMOJI = true` (D10).

**Order (D15):**
1. Services / requires (today's lines 7-21) + `local B = require(RS.BrickUI)`, `local H = B.STYLE == "CheckUI" and B.Hatch`.
2. Fallback: `if not H or B.skinFor("FreeGift") ~= "Hatch" or (RunService:IsStudio() and workspace:GetAttribute("TestFreeGiftLegacy") == true) then`
   enable `script.Parent.FreeGiftClientLegacy`, `warn("[FreeGiftClient] fallback: FreeGiftClientLegacy")`, `return end`.
3. `local ok, err = pcall(build)` (gui, Holder, chrome, Canvas, 4.1 tables) -> on failure: destroy the gui, fallback (2), return.
   `gui.Parent = pg` last.
4. The rest (logic + world).

**Keep verbatim:** `checkGroup`, `claimed()`, `findSign` + `SIGN_NEAR / SIGN_FAR`, the sign / sparkles lines of `refresh()`
(`if sign then sign.Enabled = not done end`, sparkles), `showHint`'s role (now the CLAIM word), the claim handler's mapping and
its order (pcall `Claim:InvokeServer()`; ok -> HatchWin + findSign + `sparkles:Emit(35)` + refresh; "group" -> joined false +
shake + promptJoin; "claimed" -> refresh; "wait" -> word), `setOpen`'s CloseWindow / WindowOpened / `ownSignalUntil` rules, the
WindowOpened listener, the 0.15 s zone poll (byte-identical), and from the RenderStepped only the sign part (bob, scale, distance
fade) in its own connection, byte-identical lines.

**Delete:** the Check-UI constants / `standardButton` / `card` / `text` / `stroke` builders, the deviceScale `windowScale`, the
`pop` UIScale, the `hint` label, the sunburst line of the RenderStepped.

**New:**
- `refresh()`: window part = 4.2 (Join / Joined / Done visibility, CLAIM palette + word via `btn.setPalette` + `H.fit`), writes
  only on change; then the kept sign lines. Studio probe `FreeGiftRefreshN`.
- `promptJoin()`: Studio `gui.TestDryRun == true` -> `TestLastBuy = JSON {"PromptJoinAsync", GROUP_ID}`, reply
  `TestDryRunResult` (nil = no change); else today's `GroupService:PromptJoinAsync` path.
- Claim press: `if busy or claimed() then return end`; Studio `gui.TestClaimFail` (string) = that refusal without the remote
  (then cleared); probe `FreeGiftClaimCalls` (count of real invokes).
- Motion (D11): `gui:GetPropertyChangedSignal("Enabled")` connects / disconnects ONE RenderStepped (rays; `claimBtn.pulse(t, fixed)`
  in the joined state with `fixed = gui.HatchTestPulse`); probes `RaysLoop`, `HatchPerfFreeGift` = "<frames> <sum ms of 30> <max ms>".
- Fit: `H.fitStandalone(gui, mainMenu, 560, 460)` on open + refit triggers (section 2).
- Studio hooks (only `RunService:IsStudio()`): `gui.TestOpen` / `gui.TestClose` (BindableEvents: `setOpen(true / false)`, TestOpen
  ignores the claimed rule), `gui.TestPress` (key `"Join"` / `"Claim"` / `"Close"`; `"Join"` refuses + warns unless `TestDryRun`),
  attributes `TestDryRun`, `TestDryRunResult`, `TestDryRunHold` (the red word stays; containment), `TestClaimFail`, `TestJoined`
  (false = draw the not-in-group state, UI only), `HatchTestScale`, `HatchTestPulse`, `HatchTestHover` (-> `H.setTestHover`).

**Diff rule:** the zone poll loop and the sign lines are byte-identical to `FreeGiftClient_preUWF` (LCS diff in the ledger).

### 4.7 Contracts

| Reader | Reads | Kept by |
|---|---|---|
| StarterPackClient 613, StarterPackHud `MODALS` | `PlayerGui.FreeGiftUI.Enabled` | same name, Enabled = open |
| FreeGiftServer | `RS.FreeGift.Claim`, attribute `GroupId`, player attribute `FreeGift` | untouched |
| HubV2Tests T10.11 / T11.1 | the chest, `FreeGiftZone`, `SignAnchor.FreeSign` | world untouched |
| MainMenu | `WindowOpened` / `CloseWindow` | same calls |

---

## 5. Window 2: WELCOME BACK

### 5.0 Current layout inventory (OfflineClient, `docs/reviews/2026-10-15-offline-ui/current_v2.jpg`)

| Zone | Today (logical px of 540 x 430) |
|---|---|
| Window | slate canvas + damier, centred on the screen, DisplayOrder 20; opens 1.5 s after `OfflineReady` when `OfflinePending > 0` and TutorialDone |
| Header (0..60) | gold (Skip palette) checker header, cash icon 44, "WELCOME BACK!", 3D red [X] |
| Body | "OFFLINE EARNINGS" (270, 93) 420 x 38; a 270 px sunburst + the 184 px cash centred (270, 192); the green amount (270, 286) 380 x 62 overlapping the cash |
| Buttons | CLAIM x5! 240 x 64 at centre (160, 364), rainbow; its price tag "39 [R]" 92 x 28 at (50, 330) **over the button's top-left corner**; CLAIM! 200 x 64 at (400, 364), lime |
| Logic | `claimNormal` (busy, `Claim:InvokeServer()`, Bank, `finish(0.25)`), X = claim the x1, x5 = `MarketplaceService:PromptProductPurchase(player, 3718679677)` + `PromptProductPurchaseFinished` -> wait `OfflineLastX5` <= 15 s -> amount x5, HatchWin, cash pop, `finish(1.4)`; another window opening claims the x1; `show()`; `onReady` (+1.5 s); live price (GetProductInfo, InfoType Product) |
| Base line (frozen) | `OfflineBaseUI.PerDay` "You earn $X/Day offline!" at the top while on your own base (0.25 s loop) |

### 5.1 HATCH NIGHT version (logical px; canvas 540 x 423; `welcome*_pc.png`)

**Chrome:** `H.windowChrome(holder, {bats = false, w = 540, h = 430})`, `setTheme(H.bandTheme("WelcomeBack"))` (= "HatchGold"),
`icon.Image = CASH 88694661500877`, `setTitle("Welcome Back!")`. Teeth `H.headerTeeth(540)` (27), X (494, 6), CloseHit (512, 28).

| Name | Class | rect | Z | Look |
|---|---|---|---|---|
| Heading | text @26, stroke 3 | (10, 70, 520, 26) | 4 | WHITE "OFFLINE EARNINGS" |
| Rays | ImageLabel `H.ICON.rays` | (155, 67, 230, 230), Fit | 1 | ImageColor3 (255,220,120), 0.45, `HatchRadial`; 12 deg/s while open |
| Glow | `H.glow` | (150, 102, 240, 160) | 2 | `H.GLOW.cash`, 0.35 |
| Hero | Frame, AnchorPoint 0.5 | centre (270, 182), 168 x 168, UIScale `PopScale` | 3 | |
| Hero.Cash | sticker | (9, 9, 150) | 3 | CASH 88694661500877 (canvas 195..345 x 107..257, shadow to 260) |
| Amount | text @52, stroke 4, fill 0.83 | (10, 262, 520, 52) | 5 | UIGradient (180,255,25) -> (60,205,0); `"$" .. SpeedStat.Format(n)` |
| ClaimX5 | `H.priceButton` gold | (20, 336, 276, 64); d 4, r 12, `pre = "CLAIM x5!"`, glyph 28, size 26, hoverScale 1, `HatchTile "btns"` | 5 | `setPrice(live price)`; X5_STYLE "rainbow" = the face UIGradient `H.RAINBOW` Rotation 20 (owner's call 4) |
| Claim | glossButton lime | (304, 336, 216, 64); d 4, r 12, size 30, "CLAIM!", hoverScale 1, `HatchTile "btns"` | 5 | label HatchFill 0.83 |
| Fx | Frame | (0, 0, 540, 423) | 20 | shards at (270, 182) |

Vertical stack: heading 70..98, cash 107..260, amount 262..316, buttons 336..400 (23 px bottom margin). The x5 pop
(PopScale 1.1, 0.45 s Back) spans 99.5..264.5: under the heading, a 2.5 px transient touch with the amount box top only.

### 5.2 States

| State | Amount | ClaimX5 | Claim |
|---|---|---|---|
| Normal | "$547K" | gold "CLAIM x5! [R] 39" (live, regional; a 4-digit price steps the group down, min 18) | lime CLAIM! |
| x5 prompt open | | unchanged (`prompting`) | unchanged |
| x5 paid (D13) | `"$" .. Format(OfflineLast x 5)`, PopScale 1 -> 1.1 -> 1, shards, HatchWin | `Active = false` | `Active = false`; close after 1.4 s |
| Dry-run refusal | | red `{MSG:upper(), "TRY AGAIN"}` 1.4 s ("TEST SAVE ONLY" 82 %) | |
| Claimed (x1) | | | Bank SFX, Holder pop 1.05, close after 0.25 s (today) |

### 5.3 Kept vs moved

| Kept | Moved, and why |
|---|---|
| Header gold with the cash icon + "WELCOME BACK!" + X; "OFFLINE EARNINGS"; the big cash over turning rays; the big green amount under it; CLAIM x5 left, CLAIM right, same sizes (64 tall); X claims the x1; another window claims the x1; the x5 flow | **The price tag -> inside the x5 button** (gold price group): today it sits over the button's top-left corner (the owner's "corners aren't even in the box" / "hovers over text"). **Rainbow -> gold** (every Robux buy is gold; owner's call 4, `X5_STYLE`). **The amount no longer overlaps the cash art** (the art moves up 10, the amount box starts below the cash shadow). |

### 5.4 Exact sizes at 1050x620 (s 1.18; window 637.2 x 507.4 at (229.3, 27.3))

| Element | Logical | Px |
|---|---|---|
| CLAIM x5 / CLAIM | 276 x 64 / 216 x 64 | 325.7 x 75.5 / 254.9 x 75.5 |
| Cash / rays | 150 / 230 | 177.0 / 271.4 |
| Heading / amount / buttons text | 26 / 52 / 26-30 | 30.7 / 61.4 / 30.7-35.4 px |

### 5.5 Phone checks (844x390, s 0.7767; `welcome_phone.png`)

- CLAIM x5 214.4 x 49.7 pt, CLAIM 167.8 x 49.7 pt, CloseHit 43.5 pt. Min text 20.2 pt (26 logical; the smallest copy is 26).
- Window 419.4 x 334 at gui (156.3..575.7): clear of both HUD sides. 667x375: s 0.7419.

### 5.6 Code plan (OfflineClient)

**Top switch:** `local X5_STYLE = "gold"` (D10).

**Regions.** WINDOW = today's lines 21-267 (Check-UI constants .. `task.spawn(onReady)`) + the final RenderStepped (347-349).
BASE LINE = lines 269-345 ("You earn $X/Day offline!": `baseGui` .. the 0.25 s loop) **byte-identical** (moved after the window
code is allowed; the diff must show only the moved block + the deleted final RenderStepped).

**Order (D15):** requires -> fallback (`B.skinFor("WelcomeBack")`, `workspace.TestWelcomeLegacy`; enable `OfflineClientLegacy`,
return before the base line) -> `pcall(build)` -> logic -> base line region.

**Keep:** `claimNormal`, `finish`, the X = claim rule, the x5 prompt + `PromptProductPurchaseFinished` handler (`prompting`,
the 15 s `OfflineLastX5` wait), the WindowOpened listener (claims the x1), `show()` (pending > 0, TutorialDone), `onReady` (1.5 s),
the live price (`GetProductInfo(PRODUCT, Enum.InfoType.Product)` -> `x5.setPrice`).

**Delete:** Check-UI builders, `windowScale` / `pop` UIScales (the Holder Size pop instead; `finish` shrinks the Holder Size to
0.85 in 0.15 s), the forever RenderStepped.

**New:**
- x5 press: Studio `gui.TestDryRun` -> `TestLastBuy = {"PromptProductPurchase", OfflineConfig.PRODUCT}`, reply `TestDryRunResult`
  (refusal word) - never calls MarketplaceService; else today's prompt.
- D13: `player:GetAttributeChangedSignal("OfflineLastX5")` while `gui.Enabled and not celebrated` -> the x5 celebration (the
  prompt-finished path sets `celebrated` too).
- Motion: one RenderStepped only while Enabled (rays); probes `RaysLoop`, `HatchPerfWelcome`.
- Fit: `H.fitStandalone(gui, mainMenu, 540, 430)`.
- Studio hooks: `gui.TestPress` (`"Claim"` / `"ClaimX5"` / `"Close"`; `"ClaimX5"` refuses + warns unless `TestDryRun`),
  `gui.TestOpen` (BindableEvent, arg = an amount: layout tests without the server; a later Claim gets "false" and closes, today's
  rule), attributes `TestDryRun`, `TestDryRunResult`, `TestDryRunHold`, `TestX5Hold` (the paid state stays; containment),
  `TestPriceOverride`, `HatchTestScale`, `HatchTestHover`.

### 5.7 Contracts

| Reader | Reads | Kept by |
|---|---|---|
| StreakClient 963 (Gift auto-open waits for it), RebirthClient HUD `windowOpen` 726, StarterPackClient 613, StarterPackHud | `PlayerGui.OfflineUI.Enabled` | same name / semantics |
| OfflineServer | `RS.Offline.Claim`, attributes `OfflineReady / Pending / Last / LastX5`, receipt 3718679677 | untouched |
| `OfflineBaseUI.PerDay` | | frozen region |

---

## 6. Window 3: UPGRADES (build last)

### 6.0 Current layout inventory (UpgradeClient; reconstruction `current_upgrades_1519.png`)

| Zone | Today |
|---|---|
| Window | `UpgradeUI.Root` 0.62 x 0.62 of the screen (phones 0.8 x 0.82), aspect 1.6, slate studded brick; opens on the walk-in `Stalls.UpgradeZone` (radius 6.2, ring at (-70, -48.36)), closes on walking out |
| Header (0..0.17) | Codes cyan checker header, BOOST icon, LuckiestGuy "Upgrades", purple brick "REBIRTH n" at x 0.79, red X |
| Rows (3) | 0.95 x 0.22 dark frames at y 0.215 / 0.46 / 0.705: coloured icon tile, Name (LuckiestGuy), Desc (Fredoka, "Launch further down the runway" / "Pick up eggs quicker" / "Survive 1 wave hit on every trip"), "Lv n/max" in the row colour + bar, Stat (RichText "Range 833 -> 910 studs (Thunder)" / "Grab time 1.2s -> 0.9s" / "Survive 0 hits -> 1 hit per trip"), $ button (green / red / dark lock "REBIRTH n" / grey MAX / green FREE), purple "+1 LV [R] n" |
| Foot | "Upgrades are yours forever - even after a rebirth!" |
| Tutorial | step 8 (FreeSling): FREE + a bouncing down arrow over the Sling $ button (gold text flash), Robux hidden; step 10 (TutorialExtra 2, affordable): the same arrow |
| Logic | `freeSling()`, `tutorialBuy()`, `robux()` live-price cache, `statText`, `refresh()`, the money / Robux handlers + refusal mapping, attribute listeners, a forever 1 s refresh loop, a forever RenderStepped (arrow), `setOpen`, the 0.15 s zone poll; plus Fast Grab tuning, the Wave Shield bubble (Heartbeat) and ShieldToast (frozen) |

### 6.1 HATCH NIGHT version (logical px; canvas 740 x 463; `upgrades*_pc.png`, `sheet_pc.png`)

**Chrome:** `H.windowChrome(holder, {bats = false})` (740 x 470 = the default path), `setTheme(H.bandTheme("Upgrades"))`
(royal blue), `icon.Image = BOOST 104087244878251`, `setTitle("Upgrades")`.

**RebirthPill** (in `chrome.front`, not a button): Frame (520, 9, 160, 28), Z 6, gradient `H.PAL.violet` top/bottom, corner 14,
stroke 2 INK, TopHL (14, 1, 132, 1.5) `H.PAL.violet.hl`; Label text @18 (0, 4, 160, 18), fill 0.83:
`{"REBIRTH " .. r, "R " .. r}`. Ends at 680; the X starts at 694.

**Rows** (i = 1..3: Sling, Grab, Shield): `H.shellCard(canvas, "Row_" .. kind, 10, 66 + 122 (i - 1), 720, 114, {noHit = true,
noHover = true, tile = "rows", grad = {H.CARD.top:Lerp(color, 0.15), H.CARD.bottom}})` -> y 66 / 188 / 310, face 720 x 109.
Colours: Sling (255,150,40), Grab (80,200,255), Shield (170,110,255) (today's).

| Name | Class | rect (face) | Z | Look |
|---|---|---|---|---|
| Glow | `H.glow` | (6, 6, 88, 96) | 1 | row colour, 0.4 |
| Icon | sticker | (18, 20, 64) | 2 | Roket 84334196742101 / Bolt 104553006398763 / Heart 131653504755402 |
| Name | text @22, left | (100, 10, 330, 22) | 2 | WHITE "SLINGSHOT POWER" / "FAST GRAB" / "WAVE SHIELD" |
| Desc | text @16, left | (100, 38, 216, 16) | 2 | LAV_DIM "LAUNCH FURTHER" / "GRAB EGGS FASTER" / "SURVIVE 1 WAVE HIT" (FULL_COPY: today's sentences, `HatchMin 12`) |
| Area | text @16, right | (308, 38, 112, 16) | 2 | Sling only: `U.areaAt(range of the next level):upper()` (MAX: of the max), `H.AREA_GLOW[area index]` |
| Bar | `H.progressBar` | (100, 64, 128, 30), size 16, `fill = {color:Lerp(WHITE, 0.3), color:Lerp(BLACK, 0.12)}` | 2 | `("LV %d/%d"):format(level, max)`, fill level / max (hidden at 0) |
| Stat | `H.nowNext` align left | (236, 69, 184, 18) | 3 | Sling `now = round(range(level))`, `next = round(range(level + 1)) .. " STUDS"`; Grab `("%.1fS")` now > next; Shield "0 HITS" > "1 HIT"; MAX: `nn.set(maxText, nil, {c1 = H.GOLD_TXT})` ("2300 STUDS", "0.2S", "1 HIT") |
| Buy | `H.priceButton` (D8) | (428, 25, 156, 60); d 4, r 12, size 22, glyph 26, `glyphImage = H.ICON.cash`, hoverScale 1, pulseAmp 0.02, `HatchTile "btns"` | 4 | states 6.2 |
| Robux | `H.priceButton` gold | (592, 25, 118, 60); d 4, r 12, size 20, glyph 20, `top = "+1 LV"`, topSize 16, hoverScale 1, `HatchTile "btns"` | 4 | `setPrice(robux(band.id, band.price))`; hidden at MAX, during FREE and (switch) during the step-10 arrow |
| FreeArrow | ImageLabel TUT_ARROW 93838363576146 (Sling row face) | (622, 31, 48, 48), Fit, Rotation 90 (points left), Z 10 | 10 | visible = open and (FREE or step 10); x bob `622 + 12 * abs(sin(4t))` (622..682 < 710) |

**Foot:** text @16 (10, 432, 720, 16), LAV_DIM: "UPGRADES ARE YOURS FOREVER - EVEN AFTER A REBIRTH!" (64 %).

Margins: rows end 424, foot 432..450, bottom 13. Buy at its 1.04 breathing peak: 424.9..587.1 (Robux hidden then), 2.5 px from
the info column (420) after its stroke; the arrow's left 622 is 35 px clear.

### 6.2 States

| State | Buy (156 x 60) | Robux (118 x 60) | Other |
|---|---|---|---|
| Affordable | **lime** [cash] `money(cost)` | gold "+1 LV" [R] price | |
| Can't afford | **off** [cash] price (SHORT_RED: red) | gold | |
| Locked (`rebirths < need`) | **off** [lock] `"REBIRTH " .. need` (steps to 16: "REBIRTH 13" fits) | gold (Robux needs no rebirth) | |
| MAX | **silver** `setWord("MAX")`, `Active = false` | hidden | Stat gold, Area of the max |
| FREE (step 8, `freeSling()`) | **lime** `setWord("FREE!", "lime", 26)`, breathing 1.00..1.04 | hidden | FreeArrow; the guide above the window (3) |
| Step 10 (`tutorialBuy()`) | lime price, breathing 1.00..1.04 | hidden (HIDE_ROBUX_IN_TUTORIAL) | FreeArrow |
| $ refusal (1.2 s) | **red** `{"NEED MORE $!", "NEED $!"}`; "Need Rebirth n" -> `{"NEED REBIRTH " .. n, "NEED R" .. n}`; else `{MSG:upper(), "TRY AGAIN"}` | | |
| Robux refusal (1.2 s) | | **red** `{MSG:upper(), SHORT[MSG] or "RETRY"}` with `SHORT = {["Test save only"] = "TEST!", ["Please wait"] = "WAIT!", Soon = "SOON!"}` (the 118 button's room is 97) | |

`btn.basePal` is set to the state palette before `setPrice` (priceButton restores `basePal`).

### 6.3 Kept vs moved

| Kept | Moved, and why |
|---|---|
| Header icon + title + REBIRTH n + X; 3 rows top to bottom in the same order and colours; per row: icon left, name over desc, level + bar, now -> next stat (+ the Sling area), $ button, +1 LV Robux button right; the foot line; the walk-in open / close; FREE + arrow in step 8, the arrow in step 10; rebirth locks; MAX | **Desc -> short copy** (FULL_COPY): "Launch further down the runway" at the 16 px minimum is 307 px in a 216 px box. **"Lv n/max" -> inside the bar** and **the stat -> `now > next`** without "Range" / "Grab time" / "per trip" (min 16 px in a 336 px column; "Range 833 -> 910 studs (Thunder)" is 29 characters, ~10 px today). **The Sling area -> its own label** on the desc line (area colour, right). **Icon tiles -> frameless stickers on a glow** (spec 4). **Purple +1 LV -> gold**, **red "can't afford" -> off** (owner's call 3), **purple REBIRTH brick -> a flat violet pill**. **The step-10 arrow takes the Robux slot** (no room above the button under the band teeth). |

### 6.4 Exact sizes at 1050x620 (s 1.0114, right-tile clearance; window 748.4 x 475.4 at (229.3, 43.3))

| Element | Logical | Px |
|---|---|---|
| Row / face | 720 x 114 / 720 x 109 | 728.2 x 115.3 / 728.2 x 110.2 |
| Buy / Robux | 156 x 60 / 118 x 60 | 157.8 x 60.7 / 119.3 x 60.7 |
| Icon / bar | 64 / 128 x 30 | 64.7 / 129.5 x 30.3 |
| Name / desc / stat | 22 / 16 / 18 | 22.3 / 16.2 / 18.2 px |

### 6.5 Phone checks (844x390, s 0.7106; `upgrades_phone.png`, `upgrades_free_phone.png`)

- Buy 110.9 x 42.6 pt, Robux 83.9 x 42.6 pt, CloseHit 39.8 pt. Min text 11.4 pt.
- Window 525.9 x 334 at gui (144.3..670.2): left HUD clear; right tiles est. 674.7 (4.5 px; Task 0 measures; if the tiles
  reach further left the fit shrinks, `rightHud` containment check).
- **Tutorial steps 8 / 10 on phones:** the guide stays above the window, so s = 0.5798 (9.3 pt) for that one step, exactly as
  the Rebirth step 11 already built (owner's call 7: accept, or hide the guide while a window is open = a TutorialClient change,
  out of scope).

### 6.6 Code plan (UpgradeClient)

**Top switches:** `FULL_COPY = false`, `SHORT_RED = false`, `HIDE_ROBUX_IN_TUTORIAL = true` (D10).

**Regions.** FAST GRAB = today's lines 45-53; WINDOW = 55-351; SHIELD = 353-407. FAST GRAB and SHIELD are **byte-identical**
(FAST GRAB moves below the window build: D15). Diff vs `UpgradeClient_preUWF` in the ledger: only WINDOW changes.

**Order (D15):** requires (today's 13-43 + `HttpService`) -> fallback (`B.skinFor("Upgrades")`, `workspace.TestUpgradesLegacy`;
enable `UpgradeClientLegacy`, return) -> `pcall(build)` -> FAST GRAB -> window logic -> zone poll -> SHIELD.

**Keep:** `freeSling()`, `tutorialBuy()`, `robux(id, fallback)` (InfoType Product; on arrival `dirty = true`), the stat maths
(`U.slingRange`, `U.grabTime`, `U.areaAt`, hits), `refresh()`'s computations (have, rebirths, level, free, band, need, cost), the
money handler (`Buy:InvokeServer(kind)`, Bank on ok, refusal mapping, `flashUntil`), the Robux handler (`Buy:InvokeServer(kind,
"robux")`, `rflashUntil`), the attribute list (`Money`, `Rebirths`, `SlingLevel`, `GrabLevel`, `ShieldLevel`, `FreeSling`) + add
`TutorialExtra`, `setOpen` (CloseWindow / WindowOpened / `ownSignalUntil`), the WindowOpened listener, the 0.15 s zone poll
(byte-identical).

**Delete:** every `B.*` build, `SIZE / PHONE_SIZE`, the `scale` UIScale, the forever 1 s loop, the forever RenderStepped, RichText.

**New:**
- Lifecycle (D11): on Enabled: `token += 1`, `refresh()`, start `while token == my and gui.Enabled do if dirty or os.clock() <
  flashEnd then refresh() end task.wait(0.5) end`; connect ONE RenderStepped while the arrow shows or the Buy breathes (arrow bob,
  `buy.pulse(t, gui.HatchTestPulse)`). Disabled: `token += 1`, disconnect, `stopPulse`. Probes `UpgradeLoop`, `UpgradeMotion`,
  `UpgradeRefreshN`, `HatchPerfUpgrades`.
- Dry run (D12): the Robux handler first checks Studio `gui.TestDryRun` -> `TestLastBuy = {"Upgrades.Buy", kind, "robux"}`, reply
  `TestDryRunResult` (nil / "prompted" = ok).
- Fit: `H.fitStandalone(gui, mainMenu, 740, 470, {cap = H.pageCap("Upgrades", mainMenu.AbsoluteSize.Y)})`.
- Studio hooks: `gui.TestOpen` / `gui.TestClose`, `gui.TestPress` (`"Buy_<kind>"`, `"Robux_<kind>"` - refuses + warns unless
  `TestDryRun`, `"Close"`), attributes `TestDryRun`, `TestDryRunResult`, `TestDryRunHold`, `TestPriceOverride` (every Robux price
  text), `HatchTestScale`, `HatchTestPulse`, `HatchTestHover`.

### 6.7 Contracts

| Reader | Reads | Kept by |
|---|---|---|
| TutorialClient 425 / 516 (steps 8 / 10 text) | `PlayerGui.UpgradeUI.Enabled` | same |
| RebirthClient HUD `windowOpen`, StarterPackClient 613, StarterPackHud `MODALS`, HubV2Tests T11.2 | `UpgradeUI.Enabled` | same |
| TutorialServer step 10 | `ServerStorage.UpgradeBought` (server) | untouched |
| UpgradeServer | `RS.Upgrades.Buy(kind[, "robux"])` | same args (dry run records them) |
| SlingshotServer / WaveServer | `SlingMaxSpeed`, `ShieldCharges` | server, untouched |

---

## 7. Shared code

### 7.1 BrickUI.Hatch additions (additive; Task 3)

1. **Bands:**
```lua
H.BAND.FreeGift = {band = {{0, C(120, 245, 160)}, {0.55, C(30, 215, 120)}, {1, C(0, 160, 90)}},
	fill = {{0, C(38, 218, 124)}, {0.1, C(30, 215, 120)}, {1, C(0, 160, 90)}}, tooth = C(0, 160, 90)}
H.BAND.Upgrades = {band = {{0, C(130, 175, 255)}, {0.55, C(60, 110, 255)}, {1, C(30, 60, 220)}},
	fill = {{0, C(66, 116, 255)}, {0.1, C(60, 110, 255)}, {1, C(30, 60, 220)}}, tooth = C(30, 60, 220)}
H.PAGE_BAND.FreeGift, H.PAGE_BAND.Upgrades, H.PAGE_BAND.WelcomeBack = "FreeGift", "Upgrades", "HatchGold"
```
2. **`H.headerTeeth(w)`**: `n = math.floor(36 * (w - 32) / 708 + 0.5)`; teeth `i = 0..n`: `{16 + i * (w - 32) / n, 11 + ((i * 7 + 3) % 5) * 1.6}`; `w = 740` returns exactly `H.HEADER_TEETH` (37 entries).
3. **`H.windowChrome(win, opts)`**: new `opts.w` / `opts.h` (defaults `H.W` / `H.H`). Every 740 / 470 / 463 / 737 / 460 in the
   function becomes `W` / `HH` / `HH - 7` / `W - 3` / `HH - 10`; the teeth table = `W == 740 and H.HEADER_TEETH or H.headerTeeth(W)`;
   Sheen width `math.min(420, W * 0.57)`; title boxes `math.min(400, W - 128)`; Close at `(W - 46, 6)`; CloseHit centre
   `(W - 28, 28)`; Bats at `(W - 140, 3)`; SkinScale = `win.AbsoluteSize.X / W`; `setHeight` uses `W`. Default path identical (U2).
4. **`H.fitWindow(guiW, guiH, leftClear, cap, lw, lh)`**: `lw, lh = lw or H.W, lh or H.H` replace `H.W` / `H.H` in the 2 lines.
5. **`H.PAGE_CAP_R.Upgrades = <Task 0 R_U>`** (expected 0.6718).
6. **`H.tutorialFit(s, cx, cy, guiH, topClear, lw, lh)`**: same, `lw / lh` default `H.W / H.H`.
7. **`H.priceButton`** opts `glyphImage` (the sticker image; the child keeps the name `Robux` so containment `priceGroup` finds
   it), `top` / `topSize` (a `Top` text (8, 5, w - 16, topSize), fill 0.83, shown by `setPrice`, hidden by `setWord`; the group's
   vertical centre moves to `topH + (fh - topH) / 2` with `topH = topSize + 7`), and `btn.setGlyph(img)` (sets the image, clears
   the cached key so the next `setPrice` re-lays out). Defaults identical (U8).
8. **`H.hudClear(pg, mm) -> left, right`** and **`H.guideClear(pg, mm) -> topClear | nil`** (section 3 formulas; `guideClear` =
   MenuController's `tutorialTop` without its TutorialExtra 3 gate: Title / Sub / Pips visible bottom, screen -> `mm` space, + 6).
9. **`H.fitStandalone(gui, mm, lw, lh, opts) -> size, pos, s`** (section 3, steps 1-6).

**Diff rule (ledger):** against `BrickUI_preUWF.Hatch`, the only changed old lines are: the `windowChrome` lines with 740 / 470 /
463 / 737 / 460 / 420 / 400 / 694 / 712 / 600 / `H.W` (each to its `W` / `HH` expression), the `fitWindow` and `tutorialFit`
signatures + their `H.W` / `H.H` lines, the `PAGE_CAP_R` line, the priceButton sticker line + its 2 y lines + `setWord`'s
visibility lines. Everything else is new code at the end, before `return H`.

### 7.2 BrickUI (1 line, Tasks 4 / 5 / 6)

`PAGE_SKIN = {..., Rebirth = "Hatch", FreeGift = "Hatch"}` (Task 4), `+ WelcomeBack` (Task 5), `+ Upgrades` (Task 6).

### 7.3 Assets (no uploads)

| Use | Id |
|---|---|
| Free Gift header / group / heart (THUMB_EMOJI false) | 128336310005291 / 137195579182647 / 108186731829732 |
| Potions | `PotionConfig.byKey.Money / Hatch / Speed .icon` |
| Welcome Back header + hero cash | 88694661500877 |
| Upgrades header / row icons | 104087244878251 / 84334196742101, 104553006398763, 131653504755402 |
| Cash glyph / lock glyph / check / rays / glow / star | `H.ICON.cash` / `H.ICON.lock` / `H.ICON.check` / `.rays` / `.glow` / `.star` |
| Robux | `H.ICON.robuxWhite` |
| Tutorial arrow | 93838363576146 |

---

## 8. Tests

**Rules for every Play test** (all earlier plans): `workspace.TestFreshSave == true` read in Edit before Play; `get_studio_state`
before every step; never drive the Studio UI; never stop a Play session you didn't start; never press a real Robux / join button
(no `user_mouse_input` on any window button; every `TestPress` Robux / join key needs `TestDryRun`). Local attribute toggles only
drive this client's UI; restore them at the end of each section. **Session preamble** (every session that opens a window):
(1) run `rebirth_client.lua` / `streak_client.lua` first when listed; (2) Server `TutorialDone = true`, `TutorialExtra = 0`, then
wait <= 12 s for StreakClient's Gift auto-open and close it (it would claim / close Welcome Back mid-test); (3) if
`StarterPackUI.Enabled`, set it false locally (TestStarterPack auto-popup, RIS run C ruling); (4) wait 0.4 s after every open
(the Size pop) before measuring.

### 8.1 `hatch_pure.lua` + block "UWF" (Edit; `require(Hatch:Clone())` and `require(BrickUI_preUWF.Hatch:Clone())`)

| Test | Assertion |
|---|---|
| U1 headerTeeth | `headerTeeth(740)` == `HEADER_TEETH` (37 pairs, exact); `headerTeeth(560)` 28 teeth, first x 16, last 544; `(540)` 27, last 524 |
| U2 chrome A/B | `windowChrome(f, {bats = false})` and `windowChrome(f2)` built with the new H and the pre-UWF H: every descendant's Name, Class, Position, Size, ZIndex, BackgroundColor3, Transparency, corner, stroke equal |
| U3 chrome 560 x 460 | HatchBack / HatchFront Size (560, 460); Face (560, 453); Rim (557, 450); Close holder centre (531, 23); CloseHit centre (532, 28); every tooth's centre in [16, 544]; Title Size.X 400; SkinScale = win px / 560 |
| U4 fitWindow rows | the section 3 table: `(1920, 1022, 412.1, 1.18, 560, 460)` -> (1.18, 660.8, 542.8); `(732 - 57.3 + 8, 346, 144.3, 1.18, 560, 460)` -> 0.7261; `(..., 540, 430)` -> 0.7767; Upgrades `(1050 - 72.3 + 8, 562, 229.3, pageCap, 740, 470)` -> 1.0114; +-0.001 |
| U5 fitWindow A/B | 8 inputs (the Gift / popup / Shop rows) give identical results with no lw / lh and with the pre-UWF H |
| U6 pageCap | `pageCap("Upgrades", 1022)` = max(1.18, R_U x 1022 / 470) (1.4608 for 0.6718); `("Upgrades", 695)` = 1.18; Shop / Rebirth / Index / Settings unchanged |
| U7 tutorialFit | `(1.18, 759.5, 347.5, 695, 148.6, 740, 470)` -> s 1.1498, cy 418.8; `(0.7106, 407.24, 173, 346, 67.5)` -> 0.5798; no lw / lh = the pre-UWF results |
| U8 priceButton | default (no top / glyphImage) A/B identical after `setPrice("49")` and `setWord("OWNED", "silver")`; `top = "+1 LV"`: Top visible at y 5, group centre y = 23 + (56 - 23) / 2 +-1, `setWord` hides Top; `glyphImage = cash`: Robux.Image = cash; `setGlyph(lock)` then `setPrice("REBIRTH 13")`: Robux.Image = lock, group inside w - 16 |
| U9 bands | `BAND.FreeGift.tooth` (0,160,90), `BAND.Upgrades.tooth` (30,60,220); `bandTheme("FreeGift" / "Upgrades" / "WelcomeBack")` = "FreeGift" / "Upgrades" / "HatchGold"; workspace `HatchBand = "Pumpkin"` overrides all three (restored) |
| U10 helpers exist | `H.hudClear`, `H.guideClear`, `H.fitStandalone` are functions (values: Play, 8.3-8.5 `fit`) |

Command: `hatch_pure.lua` with `execute_luau` (Edit). **Expected RED (Task 2):** U1-U9 fail, the 161 older checks pass
(`pass 161 + <U10/partial>`). **Expected GREEN (Task 3):** `pass <161 + UWF count> fail 0` (write the count in the ledger).

### 8.2 `hatch_containment.lua` v4 (Client; `_G.HatchContain(label, cfg)`)

- New `_G.HatchUWFCfg(name, opts)` for `"FreeGift"`, `"WelcomeBack"`, `"Upgrades"`: `gui = PlayerGui[FreeGiftUI | OfflineUI |
  UpgradeUI]`, `root = gui.Holder.Canvas` (assert `HatchCanvas`), `win = gui.Holder`, `back / front` = the chrome, `safe = MainMenu`,
  `screen = gui`, `hud = true`, `scaleGui = gui`, `testRoot = gui`, `textClear = true`, `pulse` = 1.03 Free Gift / 1.04 Upgrades /
  nil Welcome Back, `allowOnTop = {"GiftToast"}`, `noOnTop = opts.noOnTop`, `probes()` = every shown GuiButton under the canvas +
  `front.CloseHit`.
- v4 changes: `hud()` reads `HatchTestScale` from `cfg.scaleGui or mm`; new check **`rightHud`** (window stroked right <=
  `PetsEggsUI.RightTiles` left - 6 when the tiles are visible, native scale only). textFill stays a FAIL (83 %).
- Run matrix (close and reopen between scale changes; the gui's `HatchTestScale`):

| # | Window | Setup | Scales |
|---|---|---|---|
| FG1 | Free Gift | TestJoined false (off CLAIM, JOIN) | native, 0.7261, 0.6935 |
| FG2 | Free Gift | in the group, breathing; pulse pass 1.03 | native, 0.7261 |
| FG3 | Free Gift | claimed (CLAIMED! silver) | native |
| FG4 | Free Gift | `TestClaimFail = "group"` + `TestDryRunHold` (red JOIN FIRST!) | native, 0.7261 |
| WB1 | Welcome Back | TestOpen "$547K" | native, 0.7767, 0.7419 |
| WB2 | Welcome Back | TestOpen "$12.5Qa" + `TestPriceOverride = "1499"` | native, 0.7767 |
| WB3 | Welcome Back | dry-run refusal held ("TEST SAVE ONLY") | native |
| WB4 | Welcome Back | x5 paid state held (`TestX5Hold`) | native |
| UP1 | Upgrades | local Rebirths 2, SlingLevel 6, GrabLevel 1, Money 200000 | native, 0.7106, 0.6787, 1.0114, forced 1.46 (noOnTop) |
| UP2 | Upgrades | step 8: local FreeSling true, SlingLevel 0 (+ guide); pulse pass 1.04 | native, 0.7106 |
| UP3 | Upgrades | local SlingLevel 25, GrabLevel 4, Rebirths 20, Money 4e10; Robux refusal held | native, 0.7106 |
| UP4 | Upgrades | local Rebirths 13, SlingLevel 24, GrabLevel 3, `TestPriceOverride = "1499"`, $ refusal held | native, 0.6787 |
| G1 / S1 / SET1 / IDX1 / REB1 | the built windows | their configs (smoke) | native |

Command per run: `_G.HatchContain("<#>", _G.HatchUWFCfg("<Name>"))`. **Expected:** `<#>: ... fails 0` in every run (paste the
summary lines into the ledger).

### 8.3 `freegift_client.lua` (Client + Server steps; `_G.FreeGiftTests(section)`)

| Section | Assertions | Expected |
|---|---|---|
| `open` | TestOpen, 0.4 s: Enabled; Title "FREE GIFT!"; Tooth1 (0,160,90); Holder AR 560/460 +-0.01; CanvasScale == SkinScale +-0.001; HatchCanvas; exactly 1 FreeGiftUI; FreeGiftClientLegacy disabled; Holder is a TextButton with HatchBlocker; no Bats | `open: 10 pass / 0 fail` |
| `fit` | Holder size = `H.fitStandalone` expectation +-1; left >= hudClear; right <= RightTiles left - 6; HatchTestScale 0.7261 -> 406.6 x 334 +-1 | `fit: 4 pass / 0 fail` |
| `walkin` | HRP to `FreeGiftZone.Position + (0, 3, 0)` -> Enabled within 0.6 s; 12 studs away -> closed within 0.6 s | `walkin: 2 pass / 0 fail` |
| `joined` | (owner account in ZAB Studio) Joined + Done visible, Join hidden, CLAIM lime, `RaysLoop` true + the CLAIM ButtonScale changes over 0.6 s | `joined: 5 pass / 0 fail` |
| `notjoined` | `TestJoined = false`: Join visible, Joined hidden, CLAIM palette off, label "CLAIM!" | `notjoined: 4 pass / 0 fail` |
| `joindry` | `TestDryRun`: TestPress "Join" -> `TestLastBuy == ["PromptJoinAsync", GROUP_ID]`; TestDryRun cleared -> TestPress "Join" leaves TestLastBuy unchanged (warn) | `joindry: 2 pass / 0 fail` |
| `refusal` | `TestClaimFail = "group"` (+ TestDryRun): CLAIM red "JOIN THE GROUP FIRST!" or "JOIN FIRST!" within 0.5 s; Group card moved within 0.25 s (shake); `TestLastBuy` = PromptJoinAsync (auto-join, dry); back after 2.1 s; server `FreeGift` still false; `"wait"` -> "LOADING... TRY AGAIN!" / "TRY AGAIN" | `refusal: 6 pass / 0 fail` |
| `claim` (real, once) | Record `Potion_Money / Hatch / Speed`; TestPress "Claim" -> within 3 s: `FreeGift` true; each potion +1 (3); CLAIM silver "CLAIMED!", Active false (2); FreeSign.Enabled false, Sparkles.Enabled false (2) | `claim: 8 pass / 0 fail` |
| `once` | TestPress "Claim" again -> `FreeGiftClaimCalls` unchanged, potions unchanged after 1.5 s; walk out + in -> stays closed | `once: 3 pass / 0 fail` |
| `lifecycle` | close -> `RaysLoop` false within 0.3 s; `HatchPerfFreeGift` frozen 2 s; `FreeGiftRefreshN` frozen while closed | `lifecycle: 3 pass / 0 fail` |
| `respawn` | Server Health 0 -> after respawn exactly 1 FreeGiftUI, TestOpen works | `respawn: 2 pass / 0 fail` |
| `legacy` (own session, Edit `workspace.TestFreeGiftLegacy = true`, cleared after) | Legacy enabled; exactly 1 FreeGiftUI; it has `Holder.Window` (Check-UI) and no `HatchBack` | `legacy: 3 pass / 0 fail` |

### 8.4 `welcome_client.lua` (Client + Server; `_G.WelcomeTests(section)`)

Server step "pending n": `p:SetAttribute("OfflinePending", n); game.ServerStorage.OfflineDebug:Invoke(p, 0)`.

| Section | Assertions | Expected |
|---|---|---|
| `open` | pending 547000 -> within 3.5 s: Enabled; Title "WELCOME BACK!"; Tooth1 (255,168,0); Amount "$547K"; Price = live / fallback "39"; Pre "CLAIM x5!"; AR 540/430; CanvasScale == SkinScale; HatchCanvas; OfflineClientLegacy disabled; exactly 1 OfflineUI + 1 OfflineBaseUI | `open: 11 pass / 0 fail` |
| `claim` (real) | TestPress "Claim" -> server Money +547000 within 2 s; OfflinePending 0; closed within 1 s | `claim: 3 pass / 0 fail` |
| `close` | pending 1000 -> TestPress "Close" -> Money +1000; closed | `close: 2 pass / 0 fail` |
| `other` | pending 2000 -> `OpenPage:Fire("Shop")` -> Money +2000 within 2 s; OfflineUI closed; Shop open (closed after) | `other: 3 pass / 0 fail` |
| `x5dry` | pending 3000; TestDryRun: TestPress "ClaimX5" -> `TestLastBuy == ["PromptProductPurchase", 3718679677]`; `TestDryRunResult = "Test save only"` -> red "TEST SAVE ONLY", price back after 1.5 s; TestDryRun cleared -> TestPress "ClaimX5" refused (TestLastBuy unchanged); window still open (Claim after) | `x5dry: 4 pass / 0 fail` |
| `x5receipt` | pending 10000 -> Server `TestReceipt:Invoke(p, 3718679677)` == true; Money +50000; `OfflineLastX5` true; Amount "$50K" within 1 s; Fx shards seen within 0.5 s; closed within 2.5 s; 2nd TestReceipt == false, Money unchanged | `x5receipt: 7 pass / 0 fail` |
| `x5after` | pending 10000 -> Claim (+10000) -> TestReceipt -> +40000 | `x5after: 2 pass / 0 fail` |
| `tutorial` | Server TutorialDone false + pending 5000 -> no window within 4 s (restore TutorialDone true) | `tutorial: 1 pass / 0 fail` |
| `lifecycle` | closed: `RaysLoop` false; `HatchPerfWelcome` frozen 2 s | `lifecycle: 2 pass / 0 fail` |
| `legacy` (own session, `TestWelcomeLegacy`) | Legacy enabled; 1 OfflineUI + 1 OfflineBaseUI; pending -> the Check-UI `Holder.Window` | `legacy: 4 pass / 0 fail` |

### 8.5 `upgrade_client.lua` (Client + Server; `_G.UpgradeTests(section)`)

Expected texts are computed from `UpgradeConfig` / `ShopConfig` in the test (never literals): e.g. `tostring(math.floor(U.slingRange(6) + 0.5))`.

| Section | Assertions | Expected |
|---|---|---|
| `open` | TestOpen: Enabled; Title "UPGRADES"; Tooth1 (30,60,220); RebirthPill "REBIRTH 0"; Row_Sling / Grab / Shield at y 66 / 188 / 310; AR 740/470; CanvasScale == SkinScale; HatchCanvas; UpgradeClientLegacy disabled; exactly 1 UpgradeUI + 1 ShieldToast | `open: 10 pass / 0 fail` |
| `fit` | s = `fitStandalone` expectation +-0.002 (Studio 1.18); left >= hudClear; right <= tiles - 6 | `fit: 3 pass / 0 fail` |
| `walkin` | HRP to UpgradeZone (+0, 3, 0) -> open within 0.6 s; 12 studs away -> closed | `walkin: 2 pass / 0 fail` |
| `states` | local Rebirths 2, SlingLevel 6, Money 200000: Sling Buy lime, price `money(slingCost(7))`, Area, Stat Now / Next, Bar "LV 6/25", Pill "REBIRTH 2" (6); GrabLevel 1: Grab Buy off + lock glyph + "REBIRTH 3"; Shield "REBIRTH 10" (4); Money 1000: Sling Buy off, price unchanged (2); SlingLevel 25: Word "MAX" silver, Active false, Robux hidden, Stat "2300 STUDS" (gold, no Arrow), Area of the max (5); Robux_Sling price == `robux(band(7))` (1) | `states: 18 pass / 0 fail` |
| `free` | local FreeSling true, SlingLevel 0: Word "FREE!" lime; Robux_Sling hidden; FreeArrow visible; `UpgradeMotion` true; Buy ButtonScale changes over 0.6 s | `free: 5 pass / 0 fail` |
| `step10` | local TutorialExtra 2, FreeSling false, SlingLevel 1, Money >= cost(2): FreeArrow visible; Robux_Sling hidden; Buy breathing | `step10: 3 pass / 0 fail` |
| `buy` (real $) | Server Money 1e6, SlingLevel 0, FreeSling false, Rebirths 0: TestPress "Buy_Sling" -> SlingLevel 1 within 2 s; Money == 1e6 - slingCost(1); price == money(slingCost(2)); Bar "LV 1/25" | `buy: 4 pass / 0 fail` |
| `freebuy` (real) | Server FreeSling true, SlingLevel 0, Money 0: TestPress "Buy_Sling" -> SlingLevel 1, FreeSling false, Money 0 | `freebuy: 3 pass / 0 fail` |
| `refusal` | Server Money 0: "Buy_Sling" -> "NEED MORE $!" / "NEED $!" red within 1 s, back after 1.4 s; Rebirths 0 + GrabLevel 0: "Buy_Grab" -> "NEED REBIRTH 1" / "NEED R1" red | `refusal: 3 pass / 0 fail` |
| `robuxdry` | TestDryRun: "Robux_Sling" -> `TestLastBuy == ["Upgrades.Buy","Sling","robux"]`; `TestDryRunResult = "Test save only"` -> red "TEST SAVE ONLY" / "TEST!"; restored after 1.4 s; TestDryRun cleared -> "Robux_Grab" refused (TestLastBuy unchanged) | `robuxdry: 4 pass / 0 fail` |
| `robuxreceipt` | Server `TestReceipt:Invoke(p, ShopConfig.upgradeProduct("Sling", L + 1).id)` == true; SlingLevel L + 1 within 2 s; client Bar "LV (L+1)/25" within 1 s; Grab receipt at level 0 -> GrabLevel 1 (no rebirth needed) | `robuxreceipt: 4 pass / 0 fail` |
| `maxreceipt` | Server SlingLevel 25 -> `TestReceipt(p, band 5 id)` == false | `maxreceipt: 1 pass / 0 fail` |
| `tutorial` | local TutorialExtra 2 + Money (guide visible): guide text bottom <= Holder top - 4 at native, HatchTestScale 1.0114 and 0.7106 (3); FreeArrow at its bob max inside the Sling face (1) | `tutorial: 4 pass / 0 fail` |
| `lifecycle` | close -> `UpgradeLoop` false within 0.6 s, `UpgradeMotion` false; 20 local Money changes -> `UpgradeRefreshN` frozen; reopen -> +1 | `lifecycle: 4 pass / 0 fail` |
| `respawn` | after a respawn: 1 UpgradeUI, 1 ShieldToast, TestOpen works | `respawn: 3 pass / 0 fail` |
| `legacy` (own session, `TestUpgradesLegacy`) | Legacy enabled; 1 UpgradeUI with `Root` (Check-UI); 1 ShieldToast | `legacy: 3 pass / 0 fail` |

### 8.6 Other windows unchanged (snapshots)

- `hatch_gift_snapshot.lua`: Task 0 BEFORE -> `hatch_gift_before_uwf.txt`; after each run -> `_after_uwf.txt`. **Expected:** 181-group
  list `ae122c90` (the RIS baseline), identical.
- `hatch_shop_snapshot.lua` (2 dumps 1 s apart identical): **Expected** ALL `985d5a8c`, identical.
- `hatch_chrome_snapshot.lua` v3 (fresh session, normal mode, the run C order): **Expected** Shop `225c112d`, Rebirth `a67275d8`,
  Index `60d834c0`, Settings `5435f5b8` (if Task 0 differs, Task 0's values are the baseline; write why in the ledger).
- **NEW `hatch_pages_snapshot.lua`** (the gift-snapshot recipe): fresh save, open Settings -> Index -> Rebirth, dump each
  `<Name>Page` subtree (volatile, not recorded: Rays Rotation, ButtonScale / PopScale, UIGradient Offset / Rotation, the Index
  Pill tween position, live price texts); 2 dumps 1 s apart identical. BEFORE in Task 0, AFTER after each run. **Expected:**
  identical FNV group lists.
- The popup (StarterPackUI) shares `windowChrome` / `priceButton`: covered by U2 / U8 A/B + `starter_popup_client.lua` `open` (8.9).

### 8.7 `hatch_uwf_perf.lua` (Client; `_G.UWFPerf(section)`)

| Section | Measure | Target / Expected |
|---|---|---|
| `idle` | all three closed 3 s, 20 local Money changes | `RaysLoop` false (FreeGiftUI, OfflineUI), `UpgradeLoop` / `UpgradeMotion` false, every `HatchPerf*` / `*RefreshN` frozen |
| `cost` | each window open 300 frames; Upgrades 20 refreshes | RenderStepped avg <= 0.05 ms per window; Upgrades refresh avg <= 0.5 ms |
| `counts` | GuiObjects / instances / UIStrokes per window | recorded (estimate: Free Gift ~150, Welcome Back ~90, Upgrades ~260 GuiObjects) |
| `leaks` x30 | TestOpen / TestClose each window (Upgrades + 2 presses with TestDryRun) | GuiObjects and instances flat; LuaHeap <= +3 MB |

Results -> `hatch_uwf_perf_results.txt`. **Expected:** every target met.

### 8.8 `hatch_assets.lua`

Add the 7.3 ids. **Expected:** `failed 0`.

### 8.9 Regression suites

| Suite | Expected |
|---|---|
| `rebirth_client.lua` (first in its session; reads UpgradeUI / OfflineUI) | 13/0 |
| `streak_client.lua` v2 (first; the auto-open waits for OfflineUI) | 48/0 |
| `starter_hud_client.lua` sections layout, hidden-window, overlaps (MODALS) | pass |
| `ServerStorage.StarterPackTests` pure / live, `StreakTests` pure / live, `RebirthV6Tests` pure / live | 38 / 33, 24 / 20, 45 / 5 |
| `ServerStorage.HubV2Tests` T10.11 + T11.2 (avenue walker: UpgradeUI stays closed) | pass |
| `shop_client` open / reopen / analytics / canvasguard; `settings_client` open / reopen; `index_client` open; `rebirth_page_client` open / tutorial; `starter_popup_client` open / close | all pass |
| `get_console_output` | no errors from FreeGiftClient, OfflineClient, UpgradeClient, BrickUI; only the expected dry-run refusal warns |

### 8.10 Screenshots (`docs/plans/hatch-night-build/uwf/<window>/`, Studio 1519x753)

| File | Setup | Compare with |
|---|---|---|
| `freegift_before.jpg`, `welcome_before.jpg`, `upgrades_before.jpg` | Task 0 | the compare sheets |
| `freegift_notjoined.jpg`, `freegift_joined.jpg`, `freegift_claimed.jpg`, `freegift_refusal.jpg` | FG1-FG4 | `freegift*_pc.png` |
| `welcome.jpg`, `welcome_big.jpg`, `welcome_x5.jpg`, `welcome_refusal.jpg` | WB1-WB4 | `welcome*_pc.png` |
| `upgrades_mid.jpg`, `upgrades_free.jpg` (+ guide), `upgrades_step10.jpg`, `upgrades_max.jpg`, `upgrades_refusal.jpg` | UP1-UP4 | `upgrades*_pc.png` |
| `*_phone.jpg` | HatchTestScale 0.7261 / 0.7767 / 0.7106, cropped | `*_phone.png` |
| `*_legacy_fallback.jpg` | the legacy sessions | today's look |
| `*_zoom.png` | 2-4x: band + teeth corners, the x5 price group, the +1 LV button, the lock / cash glyph groups, the area word, the step cards' wells, the RebirthPill | |
| `compare_*_build.jpg` | the build next to `compare_*.png` | |

Visual review: a Haiku visual reviewer per window against the mockups and the owner's complaint list; fix and re-shoot until it
approves.

---

## 9. Build order (TDD; 3 builder runs, one window each, shared ledger)

**Run A = Tasks 0-4 (groundwork + FREE GIFT). Run B = Task 5 (WELCOME BACK). Run C = Tasks 6-9 (UPGRADES + cross-checks + wrap-up).**
Every run starts with `get_studio_state` (Edit, no Play), TestFreshSave set true + read back, and ends in Edit with TestFreshSave
**false** (read back) and `TestFreeGiftLegacy / TestWelcomeLegacy / TestUpgradesLegacy / HatchBand / HatchTestScale` nil (read back).
`PAGE_SKIN` is flipped per window, so every run ends in a saveable state.

- [ ] **Task 0: pre-flight and BEFORE evidence.**
  - Edit: `TestFreshSave` -> set true, read back. **Expected:** `true`.
  - Edit: `hatch_pure.lua`. **Expected:** `pass 161 fail 0`.
  - Play (fresh): check `ServerStorage.TestReceipt`, `ServerStorage.OfflineDebug` exist; `Map.Hub.Stalls.UpgradeZone` near (-70, -48.36), `Map.Hub.FreeGift.FreeGiftZone` on the chest. **Expected:** 4 found (write positions).
  - Measure R_U = `UpgradeUI.Root.AbsoluteSize.Y / MainMenu.AbsoluteSize.Y` (walk in, 0.9 s). **Expected:** ~0.6718.
  - Measure `PetsEggsUI.RightTiles` left edge in MainMenu space -> `right` at 1519x753 (expected ~88); write the scaled rows of section 3.
  - Snapshots BEFORE: gift, shop, chrome v3, NEW pages. **Expected:** gift `ae122c90`, shop `985d5a8c`, chrome as 8.6, pages list written.
  - Shots `freegift_before.jpg` (walk in), `welcome_before.jpg` (pending via OfflineDebug), `upgrades_before.jpg` (walk in, mid state); re-run `CUR_UPGRADES=... python make_compare.py`. Stop Play.
- [ ] **Task 1: backups.** `_Backup_HatchNight.Before`: `FreeGiftClient_preUWF`, `OfflineClient_preUWF`, `UpgradeClient_preUWF` (Enabled false), `BrickUI_preUWF` (+Hatch); tags stripped; attributes `WasEnabled_preUWF = "FreeGiftClient,OfflineClient,UpgradeClient"`, `HowToRestore_preUWF = "Replace StarterPlayerScripts.FreeGiftClient / OfflineClient / UpgradeClient and ReplicatedStorage.BrickUI (+Hatch) with these copies, Enabled = true; delete the three *Legacy scripts"`. `FreeGiftClientLegacy` (byte copy, disabled, Note). **Expected:** 5 sources identical (4 backups + 1 legacy), 0 tags.
- [ ] **Task 2: tests first (RED).** Write `hatch_pure.lua` UWF block, `hatch_containment.lua` v4, `freegift_client.lua`, `hatch_pages_snapshot.lua`, `hatch_uwf_perf.lua` (Free Gift sections; the others say "skipped (Check-UI)"), `hatch_assets.lua` (+ ids); mirror to `HatchUWFTests` (same FNV).
  - Edit `hatch_pure`. **Expected:** U1-U9 FAIL, 161 older pass.
  - Play `_G.FreeGiftTests("open")`. **Expected:** fails on HatchCanvas / tooth / Holder (RED), no script errors.
- [ ] **Task 3: BrickUI.Hatch additions (7.1)** with the Task 0 R_U. **Expected:** `hatch_pure` `pass <161 + UWF> fail 0`; the diff matches the 7.1 rule (ledger). Then, fresh session: gift / shop / pages snapshots + G1 / S1 / SET1 / IDX1 / REB1. **Expected:** identical to Task 0, 0 fails.
- [ ] **Task 4: FREE GIFT** (one sitting): `FreeGiftClient` + the BrickUI line (`FreeGift = "Hatch"`).
  - Play: `_G.FreeGiftTests` open, fit, walkin, joined, notjoined, joindry, refusal, claim, once, lifecycle, respawn. **Expected:** the 8.3 lines, 0 fails.
  - Containment FG1-FG4. **Expected:** 0 fails each. Perf (Free Gift). **Expected:** targets met.
  - Own session `TestFreeGiftLegacy`: `legacy`. **Expected:** `3 pass / 0 fail`.
  - Shots + visual review (Free Gift). Run A closes.
- [ ] **Task 5: WELCOME BACK** (run B): `OfflineClientLegacy` byte copy (== `_preUWF`); `welcome_client.lua` RED (`open` fails); `OfflineClient` + BrickUI `+ WelcomeBack`.
  - Play: `_G.WelcomeTests` open, claim, close, other, x5dry, x5receipt, x5after, tutorial, lifecycle. **Expected:** the 8.4 lines, 0 fails.
  - Base-line region diff vs `_preUWF`. **Expected:** byte-identical (moved block only).
  - Containment WB1-WB4; perf; own session `legacy`. **Expected:** 0 fails / targets / `4 pass`. Snapshots (gift / shop / pages). **Expected:** identical. Shots + review.
- [ ] **Task 6: UPGRADES** (run C): `UpgradeClientLegacy`; `upgrade_client.lua` RED; `UpgradeClient` + BrickUI `+ Upgrades`.
  - FAST GRAB / SHIELD region diff. **Expected:** byte-identical.
  - New fresh session: `rebirth_client.lua` first. **Expected:** `pass 13 fail 0`. Then `_G.UpgradeTests` open, fit, walkin, states, free, step10, buy, freebuy, refusal, robuxdry, robuxreceipt, maxreceipt, tutorial, lifecycle, respawn. **Expected:** the 8.5 lines, 0 fails.
  - Containment UP1-UP4; own session `legacy`. **Expected:** 0 fails; `3 pass`.
- [ ] **Task 7: cross-checks.** Snapshots AFTER (8.6). **Expected:** identical. `hatch_uwf_perf.lua` all sections. **Expected:** targets met. `hatch_assets`. **Expected:** `failed 0`. Regression (8.9). **Expected:** all green; console clean.
- [ ] **Task 8: screenshots + visual review loop** (8.10).
- [ ] **Task 9: wrap-up.** Ledger summary; memory updates: `roblox-upgrade-stall.md` (HATCH window, switches, hooks), `roblox-offline-earnings.md` (HATCH window, D13, hooks), `roblox-free-gift-chest.md` (HATCH window, hooks), `slingshot-ui-style-hatch-night.md` (batch built, the next = HUD then Admin). Tell the owner: **Save + Publish**, plus the owner's calls.

---

## 10. Hard rules

1. **TestFreshSave:** set `workspace.TestFreshSave = true` and read it back in Edit **before every Play**; set it **false** and read it back at the end of every builder run and on any abort. (False = the tests edit the owner's real save.)
2. **Never stop a Play session you didn't start.** `get_studio_state` before every step; someone else in Play = wait for Edit.
3. **No Studio command bar, no Studio dialogs, no Studio UI driving.** DataModel work goes through `execute_luau`; **never change `Camera.CameraType` in Edit.**
4. **Never publish.** The owner saves and publishes.
5. **No real Robux or Roblox prompts:** the +1 LV, CLAIM x5 and JOIN keys only with `TestDryRun = true` (enforced in code); receipts only through `ServerStorage.TestReceipt`; no `user_mouse_input` on any window button.
6. **Out of scope:** Lighting, the hub / map (incl. the stalls, chest, pads, zones, the FREE! sign), every server script, every window already built (Gift, Shop + Starter popup + HUD, Settings, Index, Rebirth), MenuController, TutorialClient, PetsEggsUI, and the frozen regions (4.6 / 5.6 / 6.6).
7. One sitting per window task: the PAGE_SKIN key flips in the same sitting as that window's new script.
8. Backups before edits (Task 1); strip CollectionService tags from every copy (backups and legacy).

---

## 11. Risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | A real prompt: +1 LV prompts on the SERVER, x5 on the client, JOIN opens a Roblox dialog (also auto after a "group" refusal) | D12 dry run in each client before the remote / service; `TestPress` refuses without it; receipts via TestReceipt; rule 5 |
| 2 | Free Gift is once per save; the owner's account is in the group, so the server's "group" path can't happen for real | Fresh save (rule 1); `TestClaimFail` / `TestJoined` (UI only) for the refusal looks; the real claim runs once in `claim` |
| 3 | StreakClient's Gift auto-open (TutorialDone true) claims and closes Welcome Back mid-test | Session preamble step 2 (wait for it, close it) |
| 4 | TestStarterPack auto-popup on tutorial attribute changes covers windows | Preamble step 3 (the RIS run C ruling) |
| 5 | Shared helper edits leak into Gift / Shop / popup / Settings / Index / Rebirth | D16: additive opts, A/B pure tests U2 / U5 / U7 / U8, the 4 snapshots before / after, smoke containment |
| 6 | Fallback runs a frozen region twice (two base lines, two ShieldToasts, two sign loops) | D15 decide-first order; the `legacy` sections count exactly 1 of each |
| 7 | Welcome Back x5 celebrates twice (attribute + prompt-finished) | `celebrated` flag (D13); `x5receipt` checks one close |
| 8 | Right tile column positions are estimates | Task 0 measures; `rightHud` containment check; the fit shrinks / shifts by itself |
| 9 | Tutorial steps 8 / 10 on phones: s 0.58 (9.3 pt) | Same as the built Rebirth step 11; owner's call 7 |
| 10 | Long values: "$12.5Qa", 4-digit regional prices, "REBIRTH 13", "CELESTIAL", "2300 STUDS" | `H.fit` variants, priceButton step-down to 16, WB2 / UP3 / UP4 runs |
| 11 | GothamBlack vs the mockup font | Hug boxes measured in-engine (`H.textWidth`); the mockup used the wider Montserrat for hug boxes; textFill FAIL in containment |
| 12 | Clicks inside the window no longer reach the world (D14) | Intended (today a click there can walk you out of the zone); `walkin` still passes |
| 13 | The Upgrades window on big PCs hides more of the stall | Owner's call 2 (default = today's size) |
| 14 | World work that still runs while closed: the 0.15 s zone polls, the FREE! sign RenderStepped, the shield Heartbeat, the $/Day 0.25 s loop | Out of scope (world / HUD); listed for the HUD batch |
| 15 | ShieldToast and the $/Day line keep their Check-UI look | Frozen here; the HUD batch restyles them |
| 16 | The 👍 is a platform emoji | Today's art; `THUMB_EMOJI = false` = the heart icon |
| 17 | The live Upgrades window was never captured for the plan | Task 0 shoots it; the compare sheet is rebuilt |
| 18 | Another agent or the owner in Play | Rule 2 |

---

## 12. Owner's calls (recommended default in bold) and owner actions

1. **Band colours: Free Gift emerald, Welcome Back gold, Upgrades royal blue** (Free Gift / Upgrades were the cyan that is now the Index's).
2. **Upgrades on big PCs as big as today** (1081 x 687 at 1080p), or the standard 873 x 555.
3. **"Can't afford" $ button: dark** (red only for refusals), or today's red (`SHORT_RED = true`).
4. **CLAIM x5: gold like every Robux buy**, or today's rainbow (`X5_STYLE = "rainbow"`).
5. **Upgrades short copy** ("LAUNCH FURTHER", `833 > 910 STUDS`), or today's sentences at a smaller size (`FULL_COPY = true`, below the 16 px rule).
6. **Tutorial step 10: hide the Sling row's +1 LV while the arrow points at the green $ button** (`HIDE_ROBUX_IN_TUTORIAL`), or keep it.
7. **Phones in tutorial steps 8 / 10: the smaller window under the guide** (as Rebirth step 11), or hide the guide while a window is open (TutorialClient; one decision for all four windows).
8. **Keep the three *Legacy copies 7 days live, then delete them.**

**Owner actions after the build:** Save + Publish; optional: the Studio phone emulator (Test > Device, iPhone landscape) at the
stall, the chest and a rejoin.
