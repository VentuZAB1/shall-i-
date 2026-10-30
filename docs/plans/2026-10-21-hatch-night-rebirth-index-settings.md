# HATCH NIGHT Rebirth + Index + Settings: implementation plan (2026-10-21)

> **For the builder (Opus):** follow this plan task by task. Every number is final and matches the mockups.
> If Studio contradicts a number, stop and write the conflict in the ledger
> (`docs/plans/style-2026-10-21/ris/progress.md`) before changing anything.
> Pipeline (owner rule): this plan -> Haiku plan reviewer -> build -> Haiku visual reviewer per screenshot set -> fixes -> Haiku lineup reviewer.

**Goal.** Rollout step 2 of HATCH NIGHT phase 2: reskin the **Settings**, **Creature Index** and **Rebirth** windows.

The owner's rules for this step:
- "Their own unique style, applied to ALL UIs, window by window."
- When a new layout was disliked: "restore it, but new design. just the layout how it looked". So **each window keeps its current layout and content; only the look changes.** Where the current layout breaks a style rule (min text 16, 83 % fill, 8 px gutters), this plan says which part moves and why.
- The acceptance test is the same as for Gift and Shop: no overlaps, every outline inside its box, no text hovering over text, every line of copy at most 83 % of its box, nothing "basic". Timers have no background (these 3 windows have no timer).

**Sources (read before building):**
- Spec: `docs/specs/2026-10-21-slingshot-ui-style.md`, sections 2, 4 and 6.
- Gift plan `docs/plans/2026-10-21-hatch-night-gift-window.md` (section 4.0 conventions, 8.3 containment) and its reviews.
- Popup + Shop plan `docs/plans/2026-10-21-hatch-night-popup-shop.md`, its review / visual review / perf review, and the ledger `docs/plans/style-2026-10-21/popup_shop/progress.md` (the rulings apply here too: K = s for scrolls, the deferred probes, the textFill 83 % rule, the legacy-fallback pattern).
- `docs/plans/2026-10-21-new-ui-performance-review.md` (RebirthClient I-1 / I-2 / M-8 / M-9 are already in the live script).
- **Mockups (the builder must match them):** `docs/plans/style-2026-10-21/ris/`
  - PC (1920x1080, s 1.18 = the Studio 1519x753 scale): `settings_pc.png`, `settings_off_pc.png`, `index_pc.png`, `index_claim_pc.png`, `rebirth_pc.png`, `rebirth_ready_pc.png`, `rebirth_need_pc.png`, `rebirth_confirm_pc.png`, `rebirth_max_pc.png`.
  - Baseline 1050x620 (s 1.0982): `settings_1050.png`, `index_1050.png`, `rebirth_need_1050.png`.
  - Phone 844x390 (s 0.7106): `settings_phone.png`, `index_phone.png`, `rebirth_need_phone.png`, strip `sheet_phone.png`.
  - Current vs new: `compare_settings.png`, `compare_index.png`, `compare_rebirth.png` (`make_compare.py`).
  - Sources: `ris.html` + `ris.js` + `engine.js` (a copy of `../popup_shop/engine.js` with a `pc1050` device). `bash render.sh qa` re-renders; the output is in `qa_report.txt`.
  - **QA result: 15 views, 0 OUT, 0 OVERLAP, 0 gap < 8, 0 text overflow, every fill <= 83 %.** Tightest: "HATCHED"@16 79 %, "RACE TO FINISH"@18 79 %, "+5%"@16 78 %, "YOU HAVE ONE: 12.5K KG"@16 78 %, "CELESTIAL"@16 77 %. Min text 18.9 px PC, 17.6 px at 1050x620, 11.4 pt phone (the H.dot "!" is 15 by design).
  - Stand-in art: tile icons from `Desktop/SLINGSHOT Icons/out` (the live tile icons differ), paw + red X drawn, Venom Basilisk = the Storm Wyvern portrait, eggs = `egg.png` hue-shifted, the Settings gear = the old 3D gear, the tutorial arrow = `Right_arrow.png`. The build uses the real ids in section 7.4.
- Current look: `docs/plans/hatch-night-build/popup_shop/rebirth_after.jpg`, `index_after.jpg`, `settings_after.jpg`.
- Code read for this plan (read-only, `script_read` / `script_grep`): MenuController (all; it is mid-change by the fix-round builder: `B.trackStroke`, `B.viewportSize`, `B.onViewport`, `SNAP_SHOP_ON_TOUCH` are new), BrickUI (tail + deviceScale), BrickUI.Hatch (all), RebirthClient (all), IndexClient (all), RebirthServer, IndexServer, PetIndex (API), SettingsServer, IndexConfig, CreatureConfig, PotionConfig, StreakConfig (EGG_ICONS), TutorialClient (step 11 contract), BackpackButton (Settings icon).

**Out of scope:** Lighting, the hub, the Gift window, the Shop, the Starter Pack popup and StarterPackHud, every server script (RebirthServer, IndexServer, PetIndex, SettingsServer, PlayerData), RebirthConfig / IndexConfig / CreatureConfig, GameSounds, DayNightClient, TutorialClient, and **RebirthClient's HUD part** (the "!" tile badge, the cached `canRebirth()` 0.5 s poll, the REBIRTH READY banner, the step-11 tile arrow). The only HUD lines that change are the 2 that place the page's own `TutorialArrow` (section 6.6).

---

## 0. Decisions (read first)

| # | Decision | Why |
|---|---|---|
| D1 | The 3 pages switch skin through `BrickUI.PAGE_SKIN` (`Settings`, `Index`, `Rebirth` = "Hatch"), one key per task, in the same sitting as that page's new script. | The skin hook already exists (Gift, Shop). A key flipped before its page is rebuilt would put the night shell around a Scale-based page (never save that state; Shop review SHOULD 23). |
| D2 | **Band colours: each window keeps its own colour** (spec 4: "other pages keep their own band colours"), all year: Rebirth **violet**, Index **cyan**, Settings **steel-lilac**. New `H.BAND.Rebirth / Index / Settings` and `H.PAGE_BAND` entries. | Same identity as today's Check-UI headers (Rebirth purple, Index "Codes" cyan, Settings silver). Settings is steel-lilac, not white: the white top-bar gear and the white title must read on it (owner's call 2). |
| D3 | **Same layout, new look.** Every zone stays where it is (tables "Kept" in 4.3 / 5.3 / 6.3). Re-layouts, each forced by a rule: Index card names move to the inspect panel; the Index reward strip becomes 3 rows; Rebirth's one-line keep text becomes 2 lines; Index stats labels get short copy. | A 740-logical canvas with min text 16 and the 83 % fill rule cannot hold today's 9-px copy in the same boxes (measured in 5.0 / 6.0). |
| D4 | **Window size: as big as today on big screens.** `H.pageCap(page, guiH)` becomes table-driven: `H.PAGE_CAP_R = {Shop = 0.8148, Rebirth = R_R, Index = R_I, Settings = R_S}`, R = today's Check-UI window height / MainMenu height, measured in Task 0 (the popup/Shop ledger measured 438.9 / 491.3 / 438.9 of 695 -> **0.6315 / 0.7069 / 0.6315**). The Shop value and every phone / 1050x620 / Studio result are unchanged (section 3). | Today the Rebirth / Settings windows are 1.55 x BaseSize and Index 2.0 x BaseSize. The 1.18 cap alone would make them 70-77 % of today's linear size at 1080p. Owner's call 1 offers the Gift size instead. |
| D5 | **Settings moves into its own script** `StarterPlayerScripts.SettingsClient`. MenuController keeps its Check-UI Settings block as the fallback, behind a 2-line guard (section 4.6). | MenuController is shared chrome and is being edited by the fix-round builder; a separate script keeps this change to 3 lines there. The guard makes the Check-UI page appear only if the HATCH page never shows up. |
| D6 | **Rebirth and Index keep their scripts** (rewrite of the page part), with disabled byte copies `RebirthClientLegacy` / `IndexClientLegacy` as the fallback (the Shop's D15 / review MUST 10 pattern). | A blank Rebirth or Index page would block progression and rewards. |
| D7 | **RebirthClient: the HUD part is frozen.** Everything from `-- HUD: "!" on the Rebirth tile` to the end stays byte-identical, except the 2 `TutorialArrow` lines (6.6). The new page keeps the names the HUD and TutorialClient read: `page` (`Body.RebirthPage`), `ready`, attribute `Confirming`, `TestPress`. | The banner and the cached poll are out of scope and were just perf-fixed. |
| D8 | **Nothing runs while closed** (the Shop's MUST 2): every page uses one `onScreen()` = page, Body, Face, Window all `Visible` and `MainMenu.Enabled`, and one `sync()` on those 5 signals. Today RebirthClient's rays RenderStepped, pulse loop and 0.5 s refresh loop keep running after X (closeWindow only hides Window, so `page.Visible` stays true), and IndexClient refreshes on every hatch while closed. | Owner's lag rule; measured by `hatch_ris_perf.lua`. |
| D9 | Rebirth refresh: `Money` changes only mark the page dirty; a 0.5 s token loop (only while shown) refreshes. Rebirths / BaseData / PetInventory refresh at once. | Money changes several times a second; today every change runs the whole refresh. |
| D10 | **Purchases are gold, states are the HATCH set:** SKIP Rebirth = gold `H.priceButton` (pre "SKIP"); REBIRTH = off (not ready, still pressable for the server's reason) / lime + breathing 1.00..1.04 (ready) / silver MAX; Index CLAIM = lime + breathing 1.00..1.03 / silver CLAIMED! / off "n LEFT"; CLAIM ALL = gold; Settings ON = lime, OFF = off, DAY = gold, NIGHT = violet. | Spec 4 button roles; the Shop uses gold for every Robux buy. Today SKIP is purple and MUSIC ON is pink (owner's calls 3 and 4). |
| D11 | **Tests never open a real Robux prompt.** The SKIP path has the Shop's dry run (`RebirthPage.TestDryRun`, `TestLastBuy`, `TestDryRunResult`); the Studio hook `TestSkip` refuses unless `TestDryRun == true`. The receipt side uses the existing `ServerStorage.TestReceipt:Invoke(player, ShopConfig.SkipRebirthProduct)` (no prompt). Free REBIRTH presses and Index claims are real (in-game) on a TestFreshSave save. | Owner rule. `RebirthRequest("skip")` calls `PromptProductPurchase` for real (RebirthServer line 103). |
| D12 | Copy is fixed, upper case, no RichText. Today's rich-text colour runs ("REBIRTH 0 <lime>▶ 1</lime>") become separate labels + the lime chevron (`H.nowNext`). | Spec copy rule; RichText was part of the cramped look. |
| D13 | Shared helpers are additive: `H.arrow` gets an optional `k` (size factor, default 1 = today), new `H.nowNext` and `H.progressBar`; `H.pageCap` becomes table-driven with identical Shop results. Old default paths stay byte-identical (diff rule 7.1). | Gift and Shop must not change (snapshots, section 8.6). |
| D14 | Pulses: only the window's main action breathes (Rebirth ready 1.00..1.04, Index CLAIM 1.00..1.03). They are never on screen together. Settings has no pulse. Cards never scale; non-clickable cards get `noHover` (hover = clickable). | Spec 2.1.4 / 2.5. |

---

## 1. Files

| Instance | Action |
|---|---|
| `ReplicatedStorage.BrickUI` | 1 line, edited 3 times (Tasks 4 / 5 / 6): `BrickUI.PAGE_SKIN = {Gift = "Hatch", Shop = "Hatch", Settings = "Hatch", Index = "Hatch", Rebirth = "Hatch"}`. Nothing else. |
| `ReplicatedStorage.BrickUI.Hatch` | Additions of section 7.1. |
| `StarterGui.MainMenu.MenuController` | 3 lines (4.6): the Settings icon in `PAGES`, and the 2-line guard at the top of the Settings block. Conditional +2 lines (6.8, only if the step-11 tutorial check fails). |
| `StarterPlayer.StarterPlayerScripts.SettingsClient` | NEW LocalScript (4.6). |
| `StarterPlayer.StarterPlayerScripts.IndexClient` | Rewrite of the UI; logic kept (5.6). |
| `StarterPlayer.StarterPlayerScripts.RebirthClient` | Rewrite of the page part (top to the line before `-- HUD:`); HUD part frozen except 2 lines (6.6). |
| `StarterPlayer.StarterPlayerScripts.IndexClientLegacy`, `RebirthClientLegacy` | NEW: disabled byte copies of today's scripts, tags stripped, the note in attribute `Note` (Task 1). |
| `ServerStorage._Backup_HatchNight.Before` | `MenuController_preRIS`, `BrickUI_preRIS` (with `Hatch`), `IndexClient_preRIS`, `RebirthClient_preRIS` (Task 1). |
| `docs/plans/tests-2026-10-21/` | New: `settings_client.lua`, `index_client.lua`, `rebirth_page_client.lua`, `hatch_shop_snapshot.lua`, `hatch_ris_perf.lua`. Changed: `hatch_pure.lua` (+ section 8.1), `hatch_containment.lua` (v3, 8.2), `hatch_chrome_snapshot.lua` (v3, 8.6), `hatch_assets.lua` (+ ids), `streak_client.lua` (section 5 now expects Rebirth on HATCH NIGHT). Results: `hatch_gift_before_ris.txt` / `_after_ris.txt`, `hatch_shop_before_ris.txt` / `_after_ris.txt`, `hatch_chrome_before_v3.txt` / `hatch_chrome_after_v3_legacy.txt`, `hatch_ris_perf_results.txt`. |
| `docs/plans/hatch-night-build/ris/` | Screenshots (section 8.10). |

---

## 2. Architecture

```
StarterGui.MainMenu (ScreenGui, DO 3, CoreUISafeInsets, IgnoreGuiInset false)
  Window (Hatch pages: Offset size from hatchFit with H.pageCap(openName), AR 740/470)
    HatchBack  Z0  night shell (unchanged)                           \  H.windowChrome: setTheme(H.bandTheme(name)),
    HatchFront Z2  band Rebirth / Index / Settings, title, icon, X   /  title = panel.Title, icon = panel.Icon
    Face (transparent on Hatch pages) > Body (full face, transparent)
      GiftPage  [PlaytimeClient + StreakClient]   unchanged
      ShopPage  [ShopClient]                       unchanged
      SettingsPage [SettingsClient]  Frame 0,0,740,463, Z3, UIScale CanvasScale (H.bindCanvasScale), attr HatchCanvas
        Row_music, Row_volume, Row_song, Row_sfx, Row_night  (shell cards 720 x 70)
      IndexPage [IndexClient]        Frame 0,0,740,463, Z3, CanvasScale, attr HatchCanvas
        Rail (recess, 6 slots + lime Pill), AreaHead, Card1..Card5, Reward, Total (recess), Inspect
      RebirthPage [RebirthClient]    Frame 0,0,740,463, Z3, CanvasScale, attr HatchCanvas, attr Confirming
        Rays, Glow, Medallion, Head (now > next), LineA, LineB, GetLabel + lines, Reward_slots..Reward_base,
        NeedPet, NeedMoney, Skip, Rebirth (+Shine), TutorialArrow, Flash
PlayerGui.RebirthReadyUI / RebirthTutorialUI  [RebirthClient HUD part]  unchanged
```

**Rendering and input** (the Gift rules): ZIndexBehavior Sibling. Every Frame / TextLabel / ImageLabel keeps `Active = false`; only GuiButtons take input. HatchFront holds only `CloseHit` as a button.

**Page attribute `HatchCanvas = true`** on each new page (tests use it to tell the HATCH page from the Check-UI fallback).

---

## 3. Window fit (all three pages)

MenuController's existing `hatchFit()` = `H.fitWindow(gs.X, gs.Y, leftClear, H.pageCap(openName, gs.Y))`. Only `H.pageCap` changes (D4). With R = 0.6315 (Rebirth, Settings) and 0.7069 (Index):

| Screen | gui | leftClear | Rebirth / Settings: s, window, (cx, cy) | Index: s, window, (cx, cy) | Min text 16 |
|---|---|---|---|---|---|
| PC 1920x1080 | 1920x1022 | 412.1 | **1.3732**, 1016.2 x 645.4, (960, 511) | **1.5371**, 1137.5 x 722.4, (980.85, 511) | 22.0 / 24.6 px |
| Studio 1519x753 | 1519x695 | 284.2 | **1.18**, 873.2 x 554.6, (759.5, 347.5) | **1.18**, same | 18.9 px |
| **PC baseline 1050x620** | 1050x562 | 229.3 | **1.0982**, **812.7 x 516.2**, (635.65, 281); top-left (229.3, 22.9) | same | **17.6 px** |
| Phone 844x390 | 732x346 | 144.3 | **0.7106**, 525.9 x 334.0, (407.24, 173) | same | 11.4 pt |
| Phone 667x375 | 667x331 | 137.9 | **0.6787**, 502.3 x 319.0, (389.03, 165.5) | same | 10.9 pt (accepted, Gift risk 10) |

- `H.pageCap(p, guiH) = max(1.18, R_p * guiH / 470)`; at 1050x620 and on phones the 1.18 cap and the width term win, so those rows equal the Gift rows.
- **Exact px at 1050x620 = logical x 1.0982.** Text sizes: 16 -> 17.6, 18 -> 19.8, 20 -> 22.0, 22 -> 24.2, 26 -> 28.6, 28 -> 30.7, 40 -> 43.9 px. Phone: 16 -> 11.4, 18 -> 12.8, 20 -> 14.2, 26 -> 18.5 pt.
- The window re-fits on every open and on viewport changes (existing code).

---

## 4. Window 1: SETTINGS (build first)

### 4.0 Current layout inventory (MenuController `-- Settings page` block; `settings_after.jpg`)

| Zone | Today |
|---|---|
| Window | LAYOUT {1.55 x BaseSize, aspect 1.3}; white/silver checker header "Settings", red X; no header icon (there is no Settings tile; BackpackButton opens it from the top bar) |
| Page | `Body.SettingsPage` 0.96 x 0.92 of Body, 5 recessed dark rows stacked (each 0.97 x 0.172, y 0.1 + 0.2 (i-1)) |
| Row content | LuckiestGuy title (MUSIC / VOLUME / SONG / SOUNDS / TIME) + a small subtitle on the left; the control on the right |
| Controls | MUSIC on/off (pink ON / grey OFF); VOLUME `-` [orange bar "100%"] `+` (blue squares, tap or drag the bar, 10 % steps); SONG `<` "ALL SONGS" `>`; SOUNDS on/off (lime ON); TIME DAY (amber) / NIGHT (purple) |
| Logic | `settingsData()`, `send(key, value)` -> `RS.Settings.Set`, defaults music true / sfx true / night false / musicVol 1 / track 0; `refresh()` on the `Settings` attribute; the drag on `UIS.InputChanged` (throttled 0.25 s, final send on release) |

### 4.1 HATCH NIGHT version (logical px; `settings_pc.png`, `settings_off_pc.png`)

**Band:** `Settings` (steel-lilac, 7.1). **Title:** SETTINGS. **Icon:** the top-bar gear `rbxassetid://98060718033874` (MenuController `PAGES.Settings.icon`, 4.6).

**Page:** `H.frame(body, "SettingsPage", 0, 0, 740, 463, nil, 3)`, `Visible = false`, `H.bindCanvasScale(page, body, 740)`, attribute `HatchCanvas = true`.

**Rows** (i = 1..5, keys `music`, `volume`, `song`, `sfx`, `night`): `H.shellCard(page, "Row_" .. key, 10, 66 + 78 (i - 1), 720, 70, {noHit = true, noHover = true, tile = "rows"})` -> y 66 / 144 / 222 / 300 / 378, face 720 x 65, gaps 8, bottom margin 15.

Inside every row face:

| Name | Class | rect | Z | Look |
|---|---|---|---|---|
| Title | text | (TITLE, 22, 10, 300, 22), left | 2 | WHITE: MUSIC / VOLUME / SONG / SOUNDS / TIME |
| Sub | text | (SUB, 22, 36, 300, 16), left | 2 | LAV_DIM: BACKGROUND MUSIC / MUSIC LOUDNESS / PICK THE MUSIC / SOUND EFFECTS / DAY OR NIGHT SKY |

Toggle rows (`music`, `sfx`, `night`):

| Name | Class | rect | Look |
|---|---|---|---|
| Toggle | glossButton | (524, 9, 188, 48); d 4, r 12, ol 2.5, size 20, hoverScale 1.04, Z 3 | Label: music / sfx ON = lime "ON", OFF = off "OFF" (label LAV_DIM); night DAY = gold "DAY", NIGHT = violet "NIGHT". `HatchPad 8` |

Volume row:

| Name | Class | rect | Look |
|---|---|---|---|
| Minus | glossButton dusk, faceFrame | (420, 9, 48, 48); d 4, r 12, no text, `HatchTile "ctl"`, `HatchGap 8` | Face holds a drawn minus: `H.segment(face, "Ink", 15, 22, 33, 22, 8, INK, 3)` + `H.segment(face, "Bar", 15, 22, 33, 22, 4, LIME (184,255,106), 4)` (a GothamBlack "-" is a thin dash) |
| VolBar | `H.progressBar` | (476, 15, 180, 36), text size 18, `HatchTile "ctl"` | Fill lime (hidden at 0), text `"70%"` |
| Hit | TextButton | (476, 4, 180, 57), Z 7, transparent, `HatchHit` | Tap / drag (today's handlers, `volAt` from `Hit.AbsolutePosition` / `AbsoluteSize` of the bar) |
| Plus | glossButton dusk, faceFrame | (664, 9, 48, 48), `HatchTile "ctl"` | Drawn plus: bars (15,22)-(33,22) and (24,13)-(24,31), ink 8 + lime 4 |
| MinusHit / PlusHit | the faces' input | | `input =` a TextButton the size of the holder (so the drawn bars never eat clicks) |

Song row:

| Name | Class | rect | Look |
|---|---|---|---|
| Prev | glossButton dusk | (420, 9, 48, 48), `HatchTile "ctl"` | `H.arrow(face, "Arrow", 15, 11, 3)` with `Rotation = 180` (the "<") |
| NameBox | `H.recess` | (476, 15, 180, 36, 3, 18), `HatchTile "ctl"` | |
| NameBox.SongName | text | ("ALL SONGS", 0, 8, 180, 18) | WHITE, `H.fit({name:upper()})` down to 16 |
| Next | glossButton dusk | (664, 9, 48, 48) | `H.arrow(face, "Arrow", 15, 11, 3)` |

### 4.2 States

| Control | States |
|---|---|
| MUSIC / SOUNDS | ON lime "ON" / OFF off "OFF" |
| TIME | DAY gold / NIGHT violet |
| VOLUME | 0..100 % in 10 % steps; 0 % hides the fill, text "0%" |
| SONG | "ALL SONGS" (track 0) or `TRACKS[t].name:upper()` (longest today "RACE TO FINISH" 79 %) |

### 4.3 Kept vs moved

| Kept (same place, same order) | Changed look only |
|---|---|
| 5 rows top to bottom: MUSIC, VOLUME, SONG, SOUNDS, TIME; title + subtitle left, control right; `-` bar `+`; `<` name `>`; tap or drag the bar; 10 % steps | Rows = dark shell cards in the night canvas (the window is the only box); GothamBlack upper case; gloss buttons; the song name sits in a recess; MUSIC ON lime instead of pink (owner's call 3) |

### 4.4 Exact sizes at 1050x620 (s 1.0982; window 812.7 x 516.2 at (229.3, 22.9))

| Element | Logical | Px at 1050x620 |
|---|---|---|
| Row | 720 x 70 | 790.7 x 76.9 |
| Toggle | 188 x 48 | 206.5 x 52.7 |
| `-` / `+` / `<` / `>` | 48 x 48 | 52.7 x 52.7 |
| Volume bar / name box | 180 x 36 | 197.7 x 39.5 |
| Title / Sub text | 22 / 16 | 24.2 / 17.6 px |

### 4.5 Phone checks (844x390, s 0.7106)

- Toggle 133.6 x 34.1 pt; `-` `+` `<` `>` 34.1 pt square; the bar hit 127.9 x 40.5 pt. All >= 34 pt.
- Window 525.9 x 334 at (144.3, 6): clears the left tiles / pills (fitWindow) and the notch.
- Min text 11.4 pt (`settings_phone.png`).
- Drag on touch: `Hit.InputBegan` with `Touch` (today's code) - check in the emulator (owner, optional).

### 4.6 Code plan

**MenuController (3 lines; anchor by content, the file is being edited by another builder):**
1. In `local PAGES = {...}`: `Settings = {color = Color3.fromRGB(70, 88, 135), text = "", icon = "rbxassetid://98060718033874"},` (the top-bar gear; `hatch.icon.Image = panel.Icon.Image` picks it up).
2. Right after `local body = panel:WaitForChild("Body")` inside the `-- Settings page` block, insert:
```lua
-- (2026-10-21 HATCH NIGHT, plan 2026-10-21-hatch-night-rebirth-index-settings.md 4.6) SettingsClient builds the
-- Settings page; this Check-UI page is only the fallback when it never appears. KEEP THIS BLOCK LAST IN THE SCRIPT.
if H and B.skinFor("Settings") == "Hatch" and body:WaitForChild("SettingsPage", 10) then return end
if B.PAGE_SKIN then B.PAGE_SKIN.Settings = nil end
```
   (`return` at chunk level ends only this script's main thread; every connection above is already made. The Settings block is the last block today.)

**SettingsClient (new LocalScript, StarterPlayerScripts):**
- Keep (copy verbatim from MenuController): `settingsData()`, `send()`, the `switch` defaults (music true, sfx true, night false), `step()`, `savedVol()`, `volAt()`, the `UIS.InputBegan / InputChanged / InputEnded` drag code (0.25 s throttle, final send), `savedTrack()`, `songLabel()`, the wrap of `<` / `>`, `refresh()` on `GetAttributeChangedSignal("Settings")`.
- Build order: (1) `local B = require(RS.BrickUI)`; `local H = B.STYLE == "CheckUI" and B.Hatch`; if not H, or `B.skinFor("Settings") ~= "Hatch"`, or Studio `workspace:GetAttribute("TestSettingsLegacy") == true` -> `B.PAGE_SKIN.Settings = nil` and return (MenuController builds Check-UI). (2) Build the page off-screen inside `pcall`; on error: destroy it, `B.PAGE_SKIN.Settings = nil`, `warn`, return. (3) `if body:FindFirstChild("SettingsPage") then page:Destroy() return end` (MenuController's fallback won the race), then `page.Parent = body`.
- `refresh()`: `btn.setPalette(pal)` + `H.fit(btn.label, text)` per switch; `showVol(v)` = `bar.set(v, round(v * 100) .. "%")`; song name via `H.fit`. Writes only on change (H.fit caches).
- No loops. Studio probes: `SettingsRefreshN` (count of refreshes).
- Studio hooks (only `RunService:IsStudio()`): `page.TestPress` (BindableEvent, key `music` / `sfx` / `night` / `volMinus` / `volPlus` / `songPrev` / `songNext`) = the same handler as the click; `page.TestVolAt` (number 0..1) = the drag-end path (`showVol` + `send("musicVol", v)`).

---

## 5. Window 2: CREATURE INDEX

### 5.0 Current layout inventory (IndexClient; `index_after.jpg`)

| Zone | Today |
|---|---|
| Window | LAYOUT {2.0 x BaseSize, aspect 1.75}; cyan checker header "Creature Index" + the book icon |
| Left | 6 area tabs (studded bricks in the area colours) "GRASS / 0/5"; gold star when claimed, red "!" when claimable; the active tab shifts right and scales 1.06 |
| Centre top | area header (gradient in the area colours): "GRASS CREATURES", "Hatched from the Wood Egg", a progress bar "0 / 5" |
| Centre middle | 5 creature cards (area gradient; secret = gold + a pink SECRET pill): name ("???" until found), portrait (black silhouette + "?" until found), hatch chance pill "52%"; the selected card scales 1.04 with a white stroke |
| Centre bottom | reward strip: "COMPLETE GRASS:" + 4 chips (+5% money, +5% speed, x1 Money Potion, x1 Hatch Potion) + CLAIM button (green CLAIM! / CLAIM AGAIN! / grey CLAIMED! / dark "n LEFT") |
| Bottom | "DISCOVERED x / 30" bar with the book + CLAIM ALL (n) (gold, only when n > 0) |
| Right | inspect panel: glow + pedestal + big portrait, name, 4 rows Income (best KG) / Best weight / Hatched / Hatch chance (+ "$x1.6" rarity bonus in lime) |
| Logic | `data = IndexConfig.decode(IndexData)`, `setModel()` (portrait or a still ViewportFrame fallback, silhouette, 0.86 -> 1 pop), `pctText`, `claimable()`, `refresh()`, `claim(which)` -> `Index.Claim` (SFX Rebirth on ok), refresh on `IndexData` and on page Visible; no loops |

### 5.1 HATCH NIGHT version (logical px; `index_pc.png`, `index_claim_pc.png`)

**Band:** `Index` (cyan). **Title:** CREATURE INDEX (from MenuController TITLES). **Icon:** the Index tile icon (unchanged path).

**Page:** `H.frame(body, "IndexPage", 0, 0, 740, 463, nil, 3)`, `bindCanvasScale`, `HatchCanvas = true`.

**Rail (left):** `H.recess(page, "Rail", 10, 66, 116, 342, 4, 20)`, `HatchPad 8`. Slots i = 1..6, `T = 3 + 56 (i - 1)`.

| Name | Class | rect | Z | Look |
|---|---|---|---|---|
| Pill | glossButton lime, faceFrame | (3, T_active, 110, 56); d 3, r 16, ol 2, hoverScale 1 | 3 | `HatchPad 3`, `HatchPadBottom 3`. Tweens to the active slot (centre (58, T + 28)) in 0.15 s Quad Out; snaps on open |
| Name<i> | text | (AREA:upper(), 2, T + 8, 112, 16) | 7 | `area.colors[1]`; WHITE on the active slot. "CELESTIAL" 77 % |
| Egg<i> | sticker | (`StreakConfig.EGG_ICONS[area.egg]`, 12, T + 29, 22) | 5/6 | |
| Prog<i> | text | ("3/5", 38, T + 31, 48, 16), left | 7 | LAV; WHITE on the active slot |
| Star<i> | sticker | (`H.ICON.star`, 88, T + 30, 20) | 5/6 | complete and claimed |
| Dot<i> | `H.dot` | (88, T + 30) | 8 | complete and not claimed |
| Hit<i> | TextButton | (0, T, 116, 56) | 9 | `HatchHit`. Activated -> `areaSel = i; creatureSel = nil; refresh()`; hover: Egg Rotation -8 (Back 0.15) |

**AreaHead:** `H.shellCard(page, "AreaHead", 134, 66, 366, 50, {noHit = true, noHover = true})`, face 366 x 45.

| Name | Class | rect | Look |
|---|---|---|---|
| Glow | glow | (4, 2, 46, 41) | area colour, 0.45 |
| Egg | sticker | (EGG_ICONS[area.egg], 8, 3, 36) | |
| Title | text | (AREA:upper(), 52, 3, 170, 20), left | area colour |
| Sub | text | (`IndexConfig.eggName(area.egg):upper()` = "WOOD EGG", 52, 24, 170, 16), left | LAV_DIM |
| Bar | `H.progressBar` | (226, 10, 130, 26) | text "3 / 5"; fill = found / #list (0.35 s tween) |

**Cards** (slot = 1..5): `H.shellCard(page, "Card" .. slot, 134 + 74.8 (slot - 1), 124, 66.8, 142, {tile = "cards", z = 2})`, face 66.8 x 137. Its `Hit` selects the creature (today's `face.Activated`).

| Name | Parent | rect | Look |
|---|---|---|---|
| (face gradient) | face | | refresh sets the face UIGradient: `secret` -> known (140,106,30) -> (90,58,16), unknown (74,58,34) -> (46,36,20); else `H.CARD` |
| Glow | face | (3.4, 18, 60, 64) | area colour (secret (255,214,90)), 0.45; hidden while unknown |
| Pedestal | face | Frame (8.4, 76, 50, 10), round | INK, BackgroundTransparency 0.55 |
| Star | pop | sticker (`H.ICON.star`, 24.4, 2, 18) | secret only |
| Portrait | pop | ImageLabel (4.4, 22, 58, 58), Fit, centre-anchored, UIScale `PicScale` | today's `setModel` (portrait or the fallback ViewportFrame child; unknown = ImageColor3 BLACK, ImageTransparency 0.15; pop 0.86 -> 1 Back 0.35). 58 (not 62) so the -6 deg hover tilt stays inside the 66.8 face (63.8) |
| Q | pop | text ("?", 4.4, 38, 58, 26) | WHITE, TextTransparency 0.25, unknown only |
| Pct | face | text (`pctText(odds[slot])`, 0, 102, 66.8, 16) | WHITE ("13.5%" 72 %) |
| Ring | badges | Frame (3, 3, 60.8, 131), corner 11, UIStroke 3 (184,255,106) | selected only (inward ring, spec 2.1.6) |

**Reward strip:** `H.shellCard(page, "Reward", 134, 274, 366, 134, {noHit = true, noHover = true})`, face 366 x 129.

| Name | Class | rect | Look |
|---|---|---|---|
| Title | text | (12, 10, 342, 18), left | GOLD_TXT: `"COMPLETE " .. AREA .. ":"`; again: `{"NEW PET! CLAIM AGAIN:", "NEW PET!"}` |
| Chip1..4 | `H.chip(face, name, 11 + 88 (i - 1), 38, 80, 32, 16)` (`HatchTile "chips"`) | | Icon sticker (6, 2, 24): cash 131724750673548 / shoe 80829076123513 / `PotionConfig.byKey.Money.icon` / `.Hatch.icon`; Text (32, 7, 44, 16) left WHITE "+5%" / "+5%" / "x1" / "x1". A potion chip with 0 hides (today's rule); the others don't move |
| Claim | glossButton | (12, 82, 342, 40); d 4, r 12, size 20 | complete + not claimed: lime "CLAIM!" breathing 1.00..1.03 (`pulseAmp 0.015`, 1.2 s); claimed: silver "CLAIMED!", `Active = false`; incomplete: off `(n) .. " LEFT"`; refusal: red `H.fit({MSG:upper(), "TRY AGAIN"})` 1.3 s |

**Total:** `H.recess(page, "Total", 10, 416, 490, 38, 4, 19)`.

| Name | Class | rect | Look |
|---|---|---|---|
| Book | sticker | (BOOK_ICON 122195701390652, 8, 2, 30) | |
| Bar | `H.progressBar` | (46, 8, 272, 22) | `"DISCOVERED " .. total .. " / " .. all` (62 %) |
| ClaimAll | glossButton gold | (326, 3, 160, 32); d 3, r 14, ol 2, size 16; `HatchPad 3` | `"CLAIM ALL (" .. n .. ")"`; visible when n > 0; `input = ClaimAllHit` TextButton (326, 0, 160, 38), `HatchHit` |

**Inspect:** `H.shellCard(page, "Inspect", 508, 66, 222, 388, {noHit = true, noHover = true, solid = H.HERO_FACE})`, face 222 x 383.

| Name | rect | Look |
|---|---|---|
| Glow | (21, 4, 180, 160) | area colour (secret gold; unknown (70,75,100)), 0.45 |
| Pedestal | Frame (51, 146, 120, 14), round | INK 0.55 |
| BigPortrait (pop) | ImageLabel (36, 6, 150, 150), Fit, `PicScale` | `setModel`; Q text ("?", 36, 60, 150, 40) when unknown |
| SecretTag | `H.tag(face, "SecretTag", x, 164, 92, 22, "SECRET!")` | secret only |
| Bonus | `H.chip(face, "Bonus", x, 164, 76, 22, 11)` + sticker cash (6, 0, 20) + text (30, 2, 42, 16) LIME `("x%.1f"):format(rarityMult)` | only when `rarityMult > 1.005` (today's rule). Tag + Bonus are one group centred in 222, gap 8 |
| Name1 / Name2 | text @18 (8, 194, 206, 18) / (8, 214, 206, 18) | WHITE. Rule: if `H.textWidth(NAME, 18) <= 0.83 x 201` one line in Name1 at y 204; else split at the space nearest the middle (2 lines); each line `H.fit` down to 16. "???" when unknown. Longest: BLACK EASTERN / DRAGON, SEA TURTLE / WARRIOR, THORNBLADE / MANTIS |
| Stat1..4 | `H.chip(face, "Stat" .. k, 8, 240 + 34 (k - 1), 206, 26, 13)`, `HatchTile "stats"` | L text (8, 4, 100, 16) left LAV_DIM: INCOME / BEST KG / HATCHED / CHANCE. V text (104, 4, 94, 16) right: known `{"$1.6K/s", "$1.6K"}` LIME, `{"2.4K KG", "2.4K"}`, `"x3"`, `pctText(odds)`; unknown "???" / "???" / "x0" / pct |

### 5.2 States

| State | Card | Inspect | Strip / Rail |
|---|---|---|---|
| Unknown creature | silhouette + "?" + dim face | silhouette, "???", stats ??? | |
| Known | portrait, area glow | portrait, name, stats | |
| Secret | gold face + star | SECRET! tag + Bonus | |
| Selected | lime inward Ring | | |
| Area incomplete | | | Claim off "n LEFT"; no dot |
| Complete, unclaimed | | | Claim lime CLAIM! (breathing); rail Dot; CLAIM ALL (n) |
| Claimed | | | Claim silver CLAIMED!; rail Star |
| Claim again (area grew) | | | Title "NEW PET! CLAIM AGAIN:", Claim lime CLAIM! |

### 5.3 Kept vs moved

| Kept (same zone) | Moved, and why |
|---|---|
| Tabs left, top to bottom; area header top-centre with egg name + progress; 5 cards in one row; reward strip under the cards; DISCOVERED bar + CLAIM ALL at the bottom spanning tabs + centre; inspect panel full height on the right; star / "!" on the tabs; secret cards gold; silhouettes + "?" | **Card names -> inspect panel only:** a card is 66.8 wide; at min 16 px a name fits ~6 letters (MOSSBACK alone needs 85 px). **Reward strip -> 3 rows** (title / 4 chips / full-width CLAIM): title 185 + 4 chips + a button do not fit 366 in one row at 16 px. **Inspect labels -> short copy** (INCOME / BEST KG / HATCHED / CHANCE): "Income (best KG)" is 150 px at 16. **The rarity bonus -> its own chip** next to the SECRET tag (it was a lime suffix on the chance row). **Area tabs -> one recessed rail with the lime pill** (as the Shop rail), area colour in the name text (spec 4: area colours only as glow / name text) |

### 5.4 Exact sizes at 1050x620 (x 1.0982)

| Element | Logical | Px |
|---|---|---|
| Rail / slot | 116 x 342 / 110 x 56 | 127.4 x 375.6 / 120.8 x 61.5 |
| AreaHead | 366 x 50 | 401.9 x 54.9 |
| Card | 66.8 x 142 | 73.4 x 155.9 |
| Portrait card / inspect | 58 / 150 | 63.7 / 164.7 |
| Reward strip / Claim | 366 x 134 / 342 x 40 | 401.9 x 147.2 / 375.6 x 43.9 |
| Total / CLAIM ALL | 490 x 38 / 160 x 32 | 538.1 x 41.7 / 175.7 x 35.1 |
| Inspect | 222 x 388 | 243.8 x 426.1 |

### 5.5 Phone checks (0.7106)

- Rail slot hit 82.4 x 39.8 pt; card hit 47.5 x 100.9 pt; Claim 243 x 28.4 pt; CLAIM ALL hit 113.7 x 27 pt (the hit is the full recess height, 38 logical). All >= 27 pt; the cards are narrow but tall (same as today).
- Min text 11.4 pt; the "!" dot 10.7 pt (by design, as Gift).
- `index_phone.png`: nothing past the window; right tiles slide away while a window is open (existing).

### 5.6 Code plan (IndexClient rewrite of the UI)

- **Keep:** the requires, `data` decode + `IndexData` listener, `shown` / `fallbackViewport` / `setModel` (the image is now the card Portrait / BigPortrait), `pctText`, `claimable`, the refresh computations (found counts, default selection, odds `CreatureConfig.odds(area.egg, 1)`, `info.rarityMult`, `CreatureConfig.income`, reward pct / potions, done / claimed / again, totals), `claim(which)` (+ SFX Rebirth on ok).
- **Delete:** every `B.*` build, `cardLayout` (5 fixed slots now), `evenChips`, RichText strings, the tab `scale` / position shift.
- **New:**
  - `local H = B.STYLE == "CheckUI" and B.Hatch`; on nil / build error / Studio `workspace.TestIndexLegacy == true`: destroy what was built, `B.PAGE_SKIN.Index = nil`, enable `script.Parent:FindFirstChild("IndexClientLegacy")`, return.
  - Build off-screen, parent `IndexPage` last.
  - `onScreen()` / `sync()` (D8): on shown -> `refresh()`; `IndexData` changes while hidden set `dirty = true` (refresh on the next show).
  - Claim: only invokes when the area is complete and not claimed (else no remote). Refusal -> red word 1.3 s.
  - Studio hooks: `page.TestPress` (key `Tab_<i>` / `Card_<slot>` / `Claim` / `ClaimAll`); attribute `TestClaimFail` (string: the next press shows that refusal without calling the server); probes `IndexRefreshN`, `HatchPerfIndex` = "<refreshes> <last ms> <max ms>".

---

## 6. Window 3: REBIRTH (build last)

### 6.0 Current layout inventory (RebirthClient page part; `rebirth_after.jpg`)

| Zone | Today |
|---|---|
| Window | LAYOUT {1.55 x BaseSize, aspect 1.25}; purple checker header "Rebirth" + the rebirth swirl icon |
| Hero (top) | gold studded medallion with the NEXT rebirth number, slowly spinning rays + halo behind; "REBIRTH 0 ▶ 1" (RichText, lime next); "Money + Speed reset. You keep everything else!" (red / green) |
| YOU WILL GET | gold label centred ("YOUR REWARDS" at MAX) |
| 4 reward tiles | PET SLOT (orange), SPEED (pink), MONEY (green), BASE SIZE (blue): icon, big value "+1" / "x1.25", name, "now ▶ next" |
| Needs | pet card (area ring portrait or silhouette, "WATER PET", "Hatch one from the Tide Egg" / "100+ KG" / "You have one: 5 KG", check / X) + money card (cash, bar "$0 / $25K", check / X). R1 has no pet card: the money card is centred |
| Buttons | SKIP [R] 20 (purple, only while not ready) + REBIRTH! (grey not ready / green ready: centred, pulse 1.04 + shine sweep; first press "TAP AGAIN!" for 2.5 s; refusals "NEED MORE $" / "NEED A PET" / MSG for 1.3 s); MAX: grey "MAX" |
| Motion | rays RenderStepped, a forever pulse loop, a forever 0.5 s refresh loop, celebration (medallion pop 1.5, rays burst, flash) on a Rebirths increase while shown |
| HUD (frozen) | "!" tile badge, cached `canRebirth()` poll, REBIRTH READY banner, step-11 arrows (`TileArrow`, page `TutorialArrow`) |

### 6.1 HATCH NIGHT version (logical px; `rebirth_*_pc.png`)

**Band:** `Rebirth` (violet). **Title:** REBIRTH. **Icon:** the Rebirth tile icon (unchanged path).

**Page:** `H.frame(body, "RebirthPage", 0, 0, 740, 463, nil, 3)`, `bindCanvasScale`, `HatchCanvas = true`, attribute `Confirming` (kept).

**Hero:**

| Name | Class | rect | Z | Look |
|---|---|---|---|---|
| Rays | ImageLabel | (`RAYS` 76624006953375, 26, 64, 120, 120), Stretch | 1 | ImageColor3 (255,222,120), ImageTransparency 0.1, `HatchRadial`; 12 deg/s only while shown |
| Glow | glow | (36, 74, 100, 100) | 2 | (255,214,90), 0.25 |
| Medallion | glossButton gold, faceFrame | (44, 82, 84, 88); d 4, r 42, ol 3, hoverScale 1 | 3 | A coin. Face children: `CoinRing` Frame (7, 7, 70, 70) round, UIStroke 2 (200,120,0) Transparency 0.3; `Num` text (tostring(nr), 0, 20, 84, 40), stroke 3; MAX: ("MAX", 0, 28, 84, 24) |
| Head | `H.nowNext(page, "Head", 148, 80, 560, 28, {align = "left"})` | | 3 | Now "REBIRTH " .. r (WHITE), lime chevron (k 1), Next tostring(nr) (LIME_TXT). MAX: Now "MAX REBIRTH", no chevron, Next "20" GOLD_TXT |
| LineA | text | (148, 116, 560, 18), left | 3 | normal RED_TXT "MONEY + SPEED RESET!"; confirming GOLD_TXT "TAP AGAIN TO REBIRTH!"; MAX GOLD_TXT "YOU REACHED THE TOP!" |
| LineB | text | (148, 138, 560, 18), left | 3 | normal LIME_TXT "YOU KEEP EVERYTHING ELSE!"; confirming RED_TXT "MONEY + SPEED RESET!"; MAX LIME_TXT "LEGEND!" |
| GetLabel | text | (270, 176, 200, 18) | 3 | GOLD_TXT "YOU WILL GET" / "YOUR REWARDS" |
| GetLineL / GetLineR | Frame | (10, 184, 346 - tw/2, 2) / (384 + tw/2, 184, 346 - tw/2, 2), tw = `H.textWidth(label, 18)` | 2 | `H.RECESS.line`, BackgroundTransparency 0.65, corner 1: 14 px clear of the label on each side, ends at x 10 and 730; re-laid when the label changes (YOUR REWARDS) |

**Reward cards** (i = 1..4: slots, speed, money, base): `H.shellCard(page, "Reward_" .. key, 10 + 182 (i - 1), 200, 174, 122, {noHit = true, noHover = true, tile = "rewards"})`, face 174 x 117.

| Name | rect | Look |
|---|---|---|
| Glow | (6, 4, 68, 68) | tile colour, 0.45 |
| Icon | sticker (14, 12, 52) | PET SLOT 107611738765467, SPEED 80829076123513, MONEY 131724750673548, BASE 131090032079108 |
| Value | text (74, 14, 92, 28), left WHITE | "+1" / `mult(multiplier(nr))` / same / "+1"; MAX: `petSlots(r)` / mult / mult / "MAX" ("x1.25" 75 %) |
| Name | text (8, 68, 158, 16) | tile colour: PET SLOT (255,186,70), SPEED (255,120,225), MONEY (130,235,95), BASE SIZE (100,200,255) |
| Line | `H.nowNext(face, "Line", 8, 90, 158, 16)` centred, k 0.75 | now WHITE > next LIME: "3 > 4", "x1 > x1.25", "x1 > x1.25", "0/5 > 1/5". MAX: Now "MAX" GOLD_TXT, no chevron; base at max size: "BIGGEST BASE" GOLD_TXT |

**Needs row** (hidden at MAX):

| Name | Class | rect | Look |
|---|---|---|---|
| NeedPet | `H.chip(page, "NeedPet", 10, 330, 356, 56, 16)`, `HatchTile "needs"` | | visible when `RebirthConfig.requirement(r) ~= nil` |
| NeedPet.Ring | Frame (8, 6, 44, 44), round, UIStroke 2 INK, UIGradient area colours | | |
| Ring.Pet | ImageLabel (2, 2, 40, 40), Fit | | best: `PORTRAITS[best.name]` WHITE; else the area's first creature, ImageColor3 (16,16,28) |
| NeedPet.Title | text (60, 8, 248, 18), left | | area colour, `AREA:upper() .. " PET"` |
| NeedPet.Sub | text (60, 30, 248, 16), left | | LAV: best `{"YOU HAVE ONE: " .. kg .. " KG", kg .. " KG"}`; `req.kg <= 1` `{"FROM THE " .. EGG:upper(), EGG:upper()}`; else `{"NEEDS " .. kg .. "+ KG", kg .. "+ KG"}` |
| NeedPet.Status | sticker (314, 12, 32) | | CHECK 78526516923039 / X 71044264112125 |
| NeedMoney | `H.chip(page, "NeedMoney", req and 374 or 192, 330, 356, 56, 16)`, `HatchTile "needs"` | | R1 (no pet): centred at x 192 (today's rule) |
| NeedMoney.Cash | sticker (8, 6, 40) | | cash |
| NeedMoney.CostBar | `H.progressBar` (56, 14, 248, 28) | | `money(min(have, cost)) .. " / " .. money(cost)`; fill have / cost |
| NeedMoney.Status | sticker (314, 12, 32) | | CHECK / X |

**Buttons:**

| Name | Class | rect | Look |
|---|---|---|---|
| Skip | `H.priceButton` gold | (10, 394, 236, 60); d 4, r 12, pre "SKIP", glyph 28, size 26; `HatchTile "btns"` | visible while not ready and not MAX. `setPrice(skipRobux())` (today's live price, InfoType Product). Refusal: `setWord({MSG:upper(), "TRY AGAIN"}, "red")` 1.3 s |
| Rebirth | glossButton | not ready (254, 394, 476, 60); ready / MAX (120, 394, 500, 60); d 4, r 12, size 26; `HatchTile "btns"` | not ready: off "REBIRTH!" (pressable: the server's reason shows); ready: lime "REBIRTH!" breathing 1.00..1.04 (`pulseAmp 0.02`, 1.2 s); confirming: lime "TAP AGAIN!"; refusal: red `{"NEED MORE $!", "NEED $!"}` / `{"NEED A PET!", "NEED PET!"}` / `{MSG:upper(), "TRY AGAIN"}` 1.3 s; MAX: silver "MAX", Active false |
| Rebirth.Shine | Frame in the face (0, 0, w, h - d), corner 12, UIGradient Rotation 20, transparency (0 1, .4 1, .5 .45, .6 1, 1 1) | | Offset -1 -> 1 (0.7 s Quad) every 1.85 s while ready and shown |
| TutorialArrow | ImageLabel (TUT_ARROW 93838363576146, 640, 400, 48, 48), Fit, Rotation 90, Z 10 | | Placed by the HUD loop (6.6). x 640: clear of the 1.04 pulse (110..630) and of the 12 px bob (right edge 700 < 730) |
| Flash | Frame (0, 0, 740, 463), corner 18, WHITE, Z 20 | | BackgroundTransparency 1 -> 0.35 -> 1 (0.5 s) on celebrate |

**Celebrate** (Rebirths increased while shown): Medallion `ButtonScale` 1.25 -> 1 (Back 0.6; at 1.25 the coin spans y 71..181, below the teeth 62); Rays 120 -> 140 and ImageTransparency 0 -> 0.1 (0.9 s); Flash.

### 6.2 States

| State | Head / lines | Needs | Buttons |
|---|---|---|---|
| R0, not ready | REBIRTH 0 > 1; reset / keep | money only, centred, X | SKIP gold + REBIRTH off |
| R0, ready (step 11) | same | money check | REBIRTH lime centred, breathing, shine; TutorialArrow (TutorialExtra 3) |
| Rn needs a pet | REBIRTH n > n+1 | pet card (silhouette + X) + money | SKIP + REBIRTH off |
| Confirming | TAP AGAIN TO REBIRTH! / MONEY + SPEED RESET! | both checks | lime TAP AGAIN!; `Confirming = true` for 2.5 s |
| Refusal | | | red word 1.3 s |
| MAX | MAX REBIRTH 20; YOU REACHED THE TOP! / LEGEND! | hidden | silver MAX |

### 6.3 Kept vs moved

| Kept | Moved, and why |
|---|---|
| Medallion top-left with the next number + rays; title right of it; YOU WILL GET centred; 4 reward tiles in one row in the same order and colours; needs row (pet left, money right; money centred on R1); SKIP left + REBIRTH right; REBIRTH centred when ready; TAP AGAIN!; MAX state; the step-11 arrow right of the button | **Keep line -> 2 lines** (LineA / LineB): one line at 18 px is 470 px (the old 9-px line). **Reward tiles -> dark shell cards** with the tile colour as glow + name text (spec 4). **SKIP purple -> gold** (owner's call 4). **Not-ready REBIRTH grey checker -> HATCH "off"** |

### 6.4 Exact sizes at 1050x620 (x 1.0982)

| Element | Logical | Px |
|---|---|---|
| Medallion | 84 x 88 | 92.2 x 96.6 |
| Head text / lines | 28 / 18 | 30.7 / 19.8 px |
| Reward card | 174 x 122 | 191.1 x 134.0 |
| Need chip | 356 x 56 | 391.0 x 61.5 |
| SKIP | 236 x 60 | 259.2 x 65.9 |
| REBIRTH (not ready / ready) | 476 x 60 / 500 x 60 | 522.7 x 65.9 / 549.1 x 65.9 |

### 6.5 Phone checks (0.7106)

- SKIP 167.7 x 42.6 pt, REBIRTH 338-355 x 42.6 pt, reward cards 123.6 x 86.7 pt.
- Min text 11.4 pt (`rebirth_need_phone.png`).
- **Step 11 on phones:** the window is 334 pt tall in a 346 pt gui (top at y 6). TutorialClient keeps its card ABOVE the window in step 11 (TutorialClient lines 265-272). Test 8.5 check `tutorial` measures it; if they overlap, Task 6b applies.

### 6.6 Code plan (RebirthClient)

**Region rule.** The script has 2 regions: PAGE (line 1 up to the line before `---------------------------------------------------------------- HUD: "!" on the Rebirth tile`) and HUD (from that line to the end). The HUD region stays byte-identical except:
1. The `local pageArrow = B.image(page, "TutorialArrow", ...)` line and its next 4 lines (`UIAspectRatioConstraint`, Rotation, ZIndex, Visible) become:
```lua
local pageArrow = H.image(page, "TutorialArrow", TUT_ARROW, ARROW_X, ARROW_Y, 48, 48, 10, true) -- (HATCH NIGHT 2026-10-21; H is set: the fallback returned before the HUD)
pageArrow.Rotation = 90 -- turned 90 deg clockwise the down arrow points left
pageArrow.Visible = false
```
2. In the arrow RenderStepped: `pageArrow.Position = UDim2.fromScale(btnHolder.Position.X.Scale + ...)` becomes `pageArrow.Position = UDim2.fromOffset(ARROW_X + bob * 12, ARROW_Y)`.
`ARROW_X = 640`, `ARROW_Y = 400` are PAGE-region constants. The builder diffs the HUD region against `RebirthClient_preRIS` and writes the diff in the ledger (expected: exactly these lines).

**PAGE region - keep:** the requires and remote; `skipRobux()`; `decode` / `ownedPets` (perf cache) / `bestFor`; `refresh()`'s computations (r, have, maxed, confirming, nr, req, best, cost, `ready`, `page:SetAttribute("Confirming", confirming and ready)`); `press()` (confirm window 2.5 s, busy, `remote:InvokeServer()`, refusal mapping); the skip handler (skipBusy, `remote:InvokeServer("skip")`, 1.3 s refusal); `celebrate()` on a Rebirths increase while shown; `TestPress`.

**PAGE region - delete:** every `B.*` build, `square`, `left`, `unify`, `fitTiles`, `setButton`, `layoutButtons`, the always-on rays RenderStepped, the forever pulse loop, the forever 0.5 s loop, RichText.

**PAGE region - new:**
- `local H = B.STYLE == "CheckUI" and B.Hatch`. On nil, a build error (pcall) or Studio `workspace.TestRebirthLegacy == true`: destroy what was built, `B.PAGE_SKIN.Rebirth = nil`, enable `script.Parent:FindFirstChild("RebirthClientLegacy")`, and **return before the HUD region** (the legacy copy then runs the banner / badge / arrows exactly once).
- Build off-screen; parent `RebirthPage` last.
- Lifecycle (D8 / D9): `onScreen()` + `sync()`. Shown: `token += 1`, `refresh()`, connect ONE RenderStepped (rays rotation; `btn.pulse(t)` while ready; shine every 1.85 s), start `while token == my do if dirty then refresh() end task.wait(0.5) end` (also refreshes once per tick for the confirm timeout and the live price). Hidden: `token += 1`, disconnect, `btn.stopPulse()`. `Money` -> `dirty = true`; `Rebirths` / `BaseData` / `PetInventory` -> `refresh()` if shown else `dirty = true`.
- Dry run (D11): the skip handler first checks Studio `page:GetAttribute("TestDryRun") == true` -> `page:SetAttribute("TestLastBuy", HttpService:JSONEncode({"RebirthRequest", "skip"}))` and uses `TestDryRunResult` (default "prompted" = ok) instead of the remote.
- Studio hooks: `page.TestSkip` (BindableEvent; `warn` and return unless `TestDryRun == true`); `TestDryRunHold` (a refusal word stays until cleared; containment only); probes `RebirthLoop` (bool), `HatchPerfRebirth` = "<frames> <sum ms of 30> <max ms>", `RebirthRefreshN`.

### 6.7 Contracts that must keep working

| Reader | Reads | Kept by |
|---|---|---|
| TutorialClient 268-283, 459-485 | `Body.RebirthPage` (name), `.Visible`, attribute `Confirming` | same name, same attribute writes |
| RebirthClient HUD | `page`, `ready`, `pageArrow` (`page.TutorialArrow`) | same locals |
| `rebirth_client.lua` (13 checks) | `RebirthPage.TutorialArrow` visible in step 11 | 6.6 |
| `ServerStorage.RebirthV6Tests` | server only | untouched |
| MenuController / BackpackButton / RebirthReadyUI | `OpenPage:Fire("Rebirth")` | untouched |

### 6.8 Task 6b (conditional): step-11 tutorial card vs the window

Only if `rebirth_page_client.lua` check `tutorial` fails (the tutorial card's bottom is below the window top - 4 at native or at 0.7106): MenuController `hatchFit()` gets 2 lines after `local gs = gui.AbsoluteSize`:
```lua
local tc = openName == "Rebirth" and player:GetAttribute("TutorialExtra") == 3 and player.PlayerGui:FindFirstChild("TutorialUI")
local topClear = tc and tc.Enabled and tc:FindFirstChild("Card") and (tc.Card.AbsolutePosition.Y + tc.Card.AbsoluteSize.Y - gui.AbsolutePosition.Y + 6) or 0
```
and `gs.Y` in the `H.fitWindow` call becomes `gs.Y - 2 * topClear` (the window stays centred, so it shrinks by twice the clearance). Re-run the check. Write the result in the ledger either way.

---

## 7. Shared code

### 7.1 BrickUI.Hatch additions (additive; old default paths byte-identical)

1. **Bands:**
```lua
H.BAND.Rebirth = {band = {{0, C(206, 120, 255)}, {0.55, C(160, 40, 255)}, {1, C(112, 0, 214)}},
	fill = {{0, C(164, 47, 255)}, {0.1, C(160, 40, 255)}, {1, C(112, 0, 214)}}, tooth = C(112, 0, 214)}
H.BAND.Index = {band = {{0, C(110, 230, 255)}, {0.55, C(0, 190, 255)}, {1, C(0, 120, 235)}},
	fill = {{0, C(10, 194, 255)}, {0.1, C(0, 190, 255)}, {1, C(0, 120, 235)}}, tooth = C(0, 120, 235)}
H.BAND.Settings = {band = {{0, C(196, 192, 236)}, {0.55, C(150, 142, 214)}, {1, C(104, 96, 176)}},
	fill = {{0, C(154, 147, 216)}, {0.1, C(150, 142, 214)}, {1, C(104, 96, 176)}}, tooth = C(104, 96, 176)}
H.PAGE_BAND.Rebirth, H.PAGE_BAND.Index, H.PAGE_BAND.Settings = "Rebirth", "Index", "Settings"
```
2. **`H.PAGE_CAP_R`** = `{Shop = H.SHOP_CAP_R, Rebirth = <Task 0>, Index = <Task 0>, Settings = <Task 0>}`; `H.pageCap(page, guiH)` body becomes `local r = H.PAGE_CAP_R[page] if r then return math.max(1.18, r * (guiH or 0) / H.H) end return nil` (Shop result unchanged).
3. **`H.arrow(parent, name, x, y, z, k)`**: optional `k` (default 1). Box `18k x 22k`, every point and thickness x k. `k = nil` is byte-identical in output.
4. **NEW `H.nowNext(parent, name, x, y, w, size, opts) -> nn`**: a transparent Frame `name` (x, y, w, size + 2) holding `Now` (text, left), `Arrow` (`H.arrow`, k = `opts.k or (size >= 24 and 1 or 0.75)`), `Next` (text, left, LIME_TXT). `nn.set(now, nxt, opts)`: widths from `H.textWidth`; `Now` box `tw1 + 8` at `x0`; Arrow at `x0 + tw1 + 10`, vertically centred on the line; `Next` at `x0 + tw1 + 14 + 18k`, box `tw2 + 8`; `x0 = 0` (align left) or `(w - G) / 2` with `G = tw1 + 8 + (nxt and (2 + 18k + 4 + tw2 + 8) or 0)`. `nxt == nil` hides Arrow + Next. Colours `opts.c1` / `opts.c2`. If `G > w` it steps the size down to 16 (`H.fit` rule). Sets `HatchTile "nn"` + `HatchGap 0` on the 3 parts (overlap check).
5. **NEW `H.progressBar(parent, name, x, y, w, h, opts) -> bar`**: `H.recess(parent, name, x, y, w, h, opts.z, h / 2)` + `Fill` Frame (3, 3, *, h - 6), corner (h - 6)/2, lime UIGradient (180,255,74) -> (79,203,16), a gloss Frame (top 45 %, white 0.55 -> 0.9) + `Text` (`H.text`, size `opts.size or 16`, centred, Z 3). `bar.set(k, text, animate)`: k clamped 0..1; `k <= 0` hides Fill; else width `max(h - 6, (w - 6) k)` (tween 0.35 s Quad when `animate`). Fill colours `opts.fill` (default lime).
6. **`H.bindCanvasScale`**: the hidden-page guard (perf review I-4) was added by the fix round (Hatch line ~642, verified while planning). Task 0 confirms it is there; if not, add it exactly as the perf review's code.

**Diff rule:** after editing, diff against `BrickUI_preRIS.Hatch`. Allowed changed old lines: the `H.arrow` signature + its 4 segment lines (`* k`), the `H.pageCap` body. Write the diff in the ledger.

### 7.2 BrickUI (1 line, Tasks 4 / 5 / 6)

`BrickUI.PAGE_SKIN = {Gift = "Hatch", Shop = "Hatch", Settings = "Hatch"}` (Task 4), then `+ Index` (Task 5), then `+ Rebirth` (Task 6). Comment: "phase 2 step 2 (2026-10-21): Settings / Index / Rebirth. Plan docs/plans/2026-10-21-hatch-night-rebirth-index-settings.md".

### 7.3 MenuController

Section 4.6 (3 lines) and, only if needed, 6.8 (2 lines + 1 changed). Nothing else: `applySkin`, `hatchFit`, the theme / title / icon lines already handle every Hatch page.

### 7.4 Assets (no uploads)

| Use | Id |
|---|---|
| Settings header icon | 98060718033874 (BackpackButton's gear) |
| Index book | 122195701390652 |
| Area eggs | `StreakConfig.EGG_ICONS` (6 ids) |
| Portraits | `IndexConfig.PORTRAITS` |
| Potions | `PotionConfig.byKey.Money.icon` 88886704386081, `.Hatch.icon` 79394853866565 |
| Cash / shoe / star / check / glow / rays | 131724750673548 / 80829076123513 / `H.ICON.star` / 78526516923039 / 121438949090215 / 76624006953375 |
| Paw / house / X | 107611738765467 / 131090032079108 / 71044264112125 |
| Tutorial arrow | 93838363576146 |
| Robux (SKIP) | `H.ICON.robuxWhite` |

---

## 8. Tests

**Rules for every Play test** (Gift / Shop plans): `workspace.TestFreshSave == true` read in Edit before Play; `get_studio_state` before every step; never drive the Studio UI; never stop a Play session you didn't start; never press a real Robux button. Local attribute toggles (`Rebirths`, `Money`, `IndexData`, `Settings`, `TutorialExtra`, `PetInventory` set on the client) only drive this client's UI; restore them at the end of each section.

### 8.1 `hatch_pure.lua` + block "RIS" (Edit; `require(Hatch:Clone())`)

| Test | Assertion |
|---|---|
| R1 bands | `H.BAND.Rebirth / Index / Settings` have `band`, `fill`, `tooth`; tooth = (112,0,214) / (0,120,235) / (104,96,176) |
| R2 bandTheme | `bandTheme("Rebirth") == "Rebirth"`, Index, Settings; `bandTheme("Gift") == bandTheme()`; with workspace `HatchBand = "HatchGold"` all three return "HatchGold" (attribute restored) |
| R3 pageCap | `pageCap("Rebirth", 1022)` = `max(1.18, R_R x 1022 / 470)` +-0.001 (1.3732 for R 0.6315); Index 1.5371; Settings 1.3732; each at 562 = 1.18; `pageCap("Shop", 1022)` = 1.7718 (unchanged); `pageCap("Gift", 1022) == nil` |
| R4 fitWindow rows | `fitWindow(1920, 1022, 412.1, pageCap("Rebirth", 1022))` = (1.3732, 1016.2, 645.4, 960, 511); Index = (1.5371, 1137.5, 722.4, 980.85, 511); `fitWindow(1050, 562, 229.3, pageCap(p, 562))` = (1.0982, 812.7, 516.2, 635.65, 281) for all 3; `(732, 346, 144.3, ...)` = (0.7106, 525.9, 334.0, 407.24, 173) |
| R5 arrow | `H.arrow(f, "A", 0, 0)` Size (18, 22) and `Ink1` Position / Size equal to the pre-RIS values; `H.arrow(f, "B", 0, 0, 3, 0.75)` Size (13.5, 16.5) |
| R6 nowNext | left: `set("REBIRTH 0", "1")` -> `Now.Size.X == textWidth("REBIRTH 0", 28) + 8`, `Arrow.Position.X == tw1 + 10`, `Next.Position.X == tw1 + 14 + 18`; centred (w 158, size 16): group centre = 79 +-1; `set("MAX", nil)` -> Arrow and Next hidden |
| R7 progressBar | `set(0)` Fill hidden; `set(0.5)` Fill width = (w - 6) x 0.5; `set(0.01)` width = h - 6; `set(2)` width = w - 6; Text = the given text |
| R8 canvas guard | a hidden canvas's `CanvasScale` does not change when its ref resizes; shown -> = ref / 740 |

Command: run `hatch_pure.lua` with `execute_luau` (Edit). **Expected:** `pass <Task 0 count + 26> fail 0`. RED run (Task 2, before 7.1): **Expected:** the R1-R7 lines FAIL, every older check still passes.

### 8.2 `hatch_containment.lua` v3 (Client; `_G.HatchContain(label, cfg)`)

- New `_G.HatchRISCfg(name)` for `"Settings"`, `"Index"`, `"Rebirth"`: `root = Body[name .. "Page"]`, `win = Window`, `back / front` = the chrome, `safe = screen = MainMenu`, `hud = true`, `testRoot = root`, `textClear = true`, `pulse` = 1.04 (Rebirth), 1.03 (Index), nil (Settings: no pulse pass), `probes()` = every visible GuiButton's centre (Toggles, Minus / Plus / Prev / Next inputs, Hit, rail Hits, card Hits, Claim, ClaimAllHit, Skip, Rebirth).
- **textFill (the 83 % rule) is a FAIL on these 3 pages** (v2.2 made it a note only for Gift): glyph width / (box - 2 x stroke) <= 0.83 for every visible TextLabel, TextTruncate labels excepted.
- New check `nowNext`: within every `HatchTile "nn"` group the 3 boxes don't overlap, are in x order, and the Arrow's centre y is the Now box's centre y +-1.
- New check `barFill`: every progressBar `Fill` is inside its trough with 3 px +-1 on top / bottom / left.
- The run matrix (close and reopen between scale changes; MainMenu `HatchTestScale`):

| # | Page | Setup (local unless "Server") | Scales |
|---|---|---|---|
| SET1 | Settings | defaults | native, 0.7106, 0.6787, 1.0982 |
| SET2 | Settings | local `Settings` = `{"music":false,"sfx":false,"night":true,"musicVol":0,"track":3}` | native, 0.7106 |
| IDX1 | Index | fresh save (0 / 30) | native, 0.7106, 0.6787, 1.0982 |
| IDX2 | Index | local `IndexData`: Grass 3 found, Water complete + claimed, Thunder complete; Card 3 selected | native, 0.7106 |
| IDX3 | Index | Grass complete, Card 5 (secret, bonus, 2-line name) selected; pulse pass | native, 0.7106 |
| IDX4 | Index | all 30 found (best 12.5M KG); tabs 1..6 in turn, card 3 / 2 / 5 selected (BLACK EASTERN DRAGON, SEA TURTLE WARRIOR, THORNBLADE MANTIS) | native |
| REB1 | Rebirth | Rebirths 0, Money 0 | native, 0.7106, 0.6787, 1.0982 |
| REB2 | Rebirth | Rebirths 0, Money 25000, TutorialExtra 3 (arrow); pulse pass 1.04 | native, 0.7106 |
| REB3 | Rebirth | Rebirths 3, Money 11.2M, no Thunder pet | native, 0.7106 |
| REB4 | Rebirth | Rebirths 3, Money 18M + a qualifying pet in PetInventory; one TestPress (confirming) | native |
| REB5 | Rebirth | Rebirths 20 (MAX) | native, 0.7106 |
| REB6 | Rebirth | refusals held (`TestDryRunHold`): REBIRTH "NEED MORE $!", Skip dry-run result "TEST SAVE ONLY" | native, 0.7106 |
| REB7 | Rebirth | Rebirths 19, Money 9.99e12 (bar "$9.99T / $32T") | native |
| G1 / S1 | Gift (Daily + Playtime), Shop top | unchanged configs | native |

Command per run: `_G.HatchContain("<#>", _G.HatchRISCfg("<Page>"))`. **Expected:** `<#>: ... 0 fails` in every run (paste the summary lines into the ledger).

### 8.3 `settings_client.lua` (Client; `_G.SettingsTests(section)`)

| Section | Assertions | Expected |
|---|---|---|
| `open` | `OpenPage:Fire("Settings")`, 0.7 s: HatchBack / HatchFront visible; HatchFront.Title "SETTINGS"; Tooth1 colour (104,96,176); `HatchFront.Icon.Image` = gear id; Window AR 740/470 +-0.01; `SettingsPage.CanvasScale.Scale == HatchBack.SkinScale.Scale` +-0.001; `HatchCanvas == true`; exactly 1 `SettingsPage` in Body; rows `Row_music..Row_night` at y 66 / 144 / 222 / 300 / 378 | `open: 10 pass / 0 fail` |
| `toggles` | for music, sfx, night: old = decode(Settings)[key] (default); `TestPress:Fire(key)` -> within 2 s decode(Settings)[key] == not old (server-written = saved); Toggle label + palette match 4.2; press again -> back. night: `Lighting.ClockTime` changes within 2 s, and back | `toggles: 13 pass / 0 fail` |
| `volume` | `volMinus` from 1 -> musicVol 0.9 within 2 s, bar text "90%"; `volPlus` -> 1, "100%"; `TestVolAt:Fire(0.34)` -> 0.3, "30%"; `TestVolAt:Fire(0)` -> 0, Fill hidden, "0%"; restore 1 | `volume: 8 pass / 0 fail` |
| `song` | `songNext` -> track 1, SongName = `TRACKS[1].name:upper()`; `songPrev` -> 0 "ALL SONGS"; `songPrev` from 0 -> `#TRACKS`; `songNext` -> 0 | `song: 4 pass / 0 fail` |
| `reopen` | `CloseWindow`, reopen: labels = the saved values; `SettingsRefreshN` did not change while closed with no Settings change | `reopen: 2 pass / 0 fail` |
| `legacy` (own session; Edit `workspace.TestSettingsLegacy = true` before Play) | within 12 s exactly 1 `SettingsPage`, no `HatchCanvas`; open -> `Face.Header` visible, HatchBack hidden; the Check-UI MUSIC toggle press flips `music` | `legacy: 4 pass / 0 fail` |

Presses are 0.4 s apart (SettingsServer allows 30 changes per 10 s).

### 8.4 `index_client.lua` (Client + Server steps; `_G.IndexTests(section)`)

Server step "complete area i" (Server DataModel):
```lua
local PI = require(game.ServerScriptService.PetIndex) local p = game.Players:GetPlayers()[1] local d = PI.read(p)
for _, c in require(game.ReplicatedStorage.IndexConfig).creatures(i) do d.found[c.name] = {n = 1, best = 5} end
PI.write(p, d)
```

| Section | Assertions | Expected |
|---|---|---|
| `open` | title "CREATURE INDEX", Tooth1 (0,120,235), AR, CanvasScale == SkinScale, `HatchCanvas`, 6 rail `Hit`, Pill on slot 1, Card1..Card5, Inspect; `IndexClientLegacy.Enabled == false` | `open: 10 pass / 0 fail` |
| `tabs` | `TestPress:Fire("Tab_3")` -> within 0.3 s Pill centre y = 143 +-0.5; AreaHead Title "THUNDER"; Pct1..5 = `pctText(odds(StormEgg, 1)[slot])` | `tabs: 7 pass / 0 fail` |
| `cards` | `Card_3` -> Ring visible only on Card3; Inspect Name1 = display:upper() (known) or "???" | `cards: 2 pass / 0 fail` |
| `claim` | Server: complete area 1. Client: Dot1 visible; Claim "CLAIM!" lime; ClaimAll "CLAIM ALL (1)". Record Potion_Money / Potion_Hatch / IndexBonus. `TestPress:Fire("Claim")` -> within 3 s: decode(IndexData).claimed["1"] == version(1); IndexBonus +0.05; Potion_Money +1; Potion_Hatch +1; Claim "CLAIMED!" silver, Active false; Star1 visible, Dot1 hidden; ClaimAll hidden. A 2nd press sends nothing (IndexBonus unchanged after 1 s) | `claim: 12 pass / 0 fail` |
| `claimall` | Server: complete 2 and 3. ClaimAll "CLAIM ALL (2)" -> press -> both claimed within 3 s, IndexBonus +0.10 | `claimall: 3 pass / 0 fail` |
| `refusal` | Server: complete 4. `TestClaimFail = "Nothing to claim"` -> Claim press -> "NOTHING TO CLAIM" red; after 1.4 s "CLAIM!" lime; server state unchanged | `refusal: 3 pass / 0 fail` |
| `again` | local IndexData with `claimed["4"] = 2` (old version) + area 4 complete -> Title "NEW PET! CLAIM AGAIN:", Claim "CLAIM!" | `again: 2 pass / 0 fail` |
| `names` | Shadow tab, Card 3 known -> Name1 "BLACK EASTERN", Name2 "DRAGON"; Grass Card 3 -> "TREANT" on one line, Name2 hidden | `names: 3 pass / 0 fail` |
| `lifecycle` | close; Server: complete area 5 -> `IndexRefreshN` unchanged; reopen -> +1 and Dot5 visible | `lifecycle: 2 pass / 0 fail` |
| `legacy` (own session, `TestIndexLegacy`) | `IndexClientLegacy.Enabled`; exactly 1 IndexPage, no `HatchCanvas`; open -> Check-UI chrome | `legacy: 3 pass / 0 fail` |

### 8.5 `rebirth_page_client.lua` (Client + Server; `_G.RebirthPageTests(section)`)

| Section | Assertions | Expected |
|---|---|---|
| `open` | title "REBIRTH", Tooth1 (112,0,214), AR, CanvasScale == SkinScale, `HatchCanvas`; Medallion, Head, Reward_slots / speed / money / base, NeedMoney, Skip, Rebirth exist; `RebirthClientLegacy.Enabled == false`; exactly 1 `RebirthReadyUI` and 1 `RebirthTutorialUI` in PlayerGui | `open: 9 pass / 0 fail` |
| `states` | local R0 / $0: Head.Now "REBIRTH 0", Head.Next "1"; NeedPet hidden; NeedMoney x 192; CostBar "$0 / $25K"; Skip visible, its price = `skipRobux()`; Rebirth palette off at centre x 492. Local Money 25000 -> within 0.6 s Rebirth lime at centre x 370, Skip hidden. Local R3 + no pet -> NeedPet visible, Title = `area:upper() .. " PET"` of `requirement(3)`, Status = X; + a qualifying pet -> Status check, Sub starts "YOU HAVE ONE". Local R20 -> Medallion "MAX", Rebirth silver "MAX", NeedPet / NeedMoney hidden, Head "MAX REBIRTH" + "20" | `states: 14 pass / 0 fail` |
| `confirm` | Server: Rebirths 0, Money 25000. `TestPress:Fire()` -> Confirming true, label "TAP AGAIN!", LineA "TAP AGAIN TO REBIRTH!". After 2.7 s without a press: Confirming false, "REBIRTH!". Press twice -> within 3 s server Rebirths 1, Money 0; Medallion Num "2"; Flash seen below transparency 1 within 0.3 s | `confirm: 7 pass / 0 fail` |
| `refusal` | Server: Money 0 (Rebirths 1). `TestPress` -> label "NEED MORE $!" or "NEED $!", palette red, within 1 s; back to "REBIRTH!" off after 1.4 s | `refusal: 3 pass / 0 fail` |
| `skipdry` | `TestDryRun = true`; `TestSkip:Fire()` -> `TestLastBuy == ["RebirthRequest","skip"]`; `TestDryRunResult = "Test save only"` -> Skip word "TEST SAVE ONLY" red, price back after 1.4 s; clear `TestDryRun`, `TestSkip:Fire()` -> `TestLastBuy` unchanged (refused + warn) | `skipdry: 4 pass / 0 fail` |
| `skipreceipt` | Server: Money 0; `ServerStorage.TestReceipt:Invoke(p, ShopConfig.SkipRebirthProduct)` -> server Rebirths +1 within 2 s; client Head.Now "REBIRTH " .. new r; celebrate seen (Medallion ButtonScale > 1.1 within 0.3 s) | `skipreceipt: 3 pass / 0 fail` |
| `lifecycle` | close -> `RebirthLoop == false` within 0.6 s; `HatchPerfRebirth` frame counter frozen 2 s; local Money changes while closed -> `RebirthRefreshN` frozen; reopen -> `RebirthLoop == true` | `lifecycle: 4 pass / 0 fail` |
| `tutorial` | local TutorialExtra 3, R0, Money 25000, page open: `TutorialArrow.Visible`; its left >= Rebirth face right + 8 at HatchTestPulse 1.04; inside the window; `PlayerGui.TutorialUI.Card` bottom <= Window top - 4 at native and at HatchTestScale 0.7106 (fail -> Task 6b) | `tutorial: 4 pass / 0 fail` |

Regression: `rebirth_client.lua` (banner / arrows). **Expected:** `pass 13 fail 0`.

### 8.6 Snapshots: Gift and Shop unchanged, the fallback looks like today

- `hatch_gift_snapshot.lua` (existing): BEFORE in Task 0 -> `hatch_gift_before_ris.txt`; AFTER in Task 7 -> `hatch_gift_after_ris.txt`. **Expected:** identical FNV group list.
- `hatch_shop_snapshot.lua` (NEW, the gift-snapshot recipe): fresh save (no Starter offer), `OpenPage:Fire("Shop")`, 1 s, dump HatchBack, HatchFront and the ShopPage subtree (the gift snapshot's property list); volatile, not recorded: texts matching `%d+:%d%d`, `CanvasPosition`, `ButtonScale` / `PopScale`, UIGradient Offset / Rotation, Rays Rotation. BEFORE Task 0, AFTER Task 7. **Expected:** identical.
- `hatch_chrome_snapshot.lua` v3: v2 + the HUD-edge header (fix round). Task 0: `hatch_chrome_before_v3.txt` (today's Check-UI Rebirth / Index / Settings chrome, after the viewport fix). Task 7, own session with `TestRebirthLegacy`, `TestIndexLegacy`, `TestSettingsLegacy` all true: `hatch_chrome_after_v3_legacy.txt`. **Expected:** the Rebirth, Index and Settings sections identical to BEFORE v3 except the Settings header Icon (the new gear id: 1 line, owner's call 2).

### 8.7 `hatch_ris_perf.lua` (Client; `_G.RISPerf(section)`)

| Section | Measure | Target / Expected |
|---|---|---|
| `idle` | every window closed 3 s | `RebirthLoop == false`; `HatchPerfRebirth`, `IndexRefreshN`, `SettingsRefreshN` frozen |
| `canvasguard` | count `CanvasScale.Scale` writes on Settings / Index / Rebirth / Shop / Gift pages while ANOTHER window opens / closes 3 times | 0 writes on every hidden page |
| `cost` | Rebirth open + ready 300 frames; one Index tab sweep x 6; 20 Settings refreshes | Rebirth RenderStepped avg <= 0.05 ms; Rebirth refresh <= 0.3 ms; Index refresh <= 2 ms; Settings refresh <= 0.3 ms |
| `counts` | GuiObjects / instances / UIStrokes under each page | recorded (estimate: Settings ~180, Index ~420, Rebirth ~230 GuiObjects) |
| `leaks` x30 | open Settings / Index (6 tab presses + 5 card presses) / Rebirth, close | GuiObjects and instances flat; LuaHeap <= +3 MB; Signals +-0.2 MB |

Results -> `hatch_ris_perf_results.txt`. **Expected:** every target met.

### 8.8 `hatch_assets.lua`

Add every id of 7.4. **Expected:** `failed 0`.

### 8.9 Regression suites

| Suite | Expected |
|---|---|
| `streak_client.lua` v2 (section 5 updated: Rebirth opens on HATCH NIGHT: HatchBack visible, title "REBIRTH") | all pass |
| `shop_client.lua` `open`, `reopen`, `analytics` (Rebirth after the Shop = exactly one false), `canvasguard` | all pass |
| `starter_popup_client.lua` `open`, `close` | all pass |
| `ServerStorage.StreakTests` pure / live (own session) | 24/24, 20/20 |
| `ServerStorage.RebirthV6Tests` pure / live (own session) | all pass |
| `get_console_output` | no errors from SettingsClient, IndexClient, RebirthClient, MenuController, BrickUI |

### 8.10 Screenshots (`docs/plans/hatch-night-build/ris/`, Studio 1519x753)

| File | Setup | Compare with |
|---|---|---|
| `settings_pc.jpg`, `settings_off.jpg` | SET1, SET2 | `settings_pc.png`, `settings_off_pc.png` |
| `index_pc.jpg`, `index_claim.jpg`, `index_names.jpg` | IDX2, IDX3, IDX4 (Shadow, Black Eastern Dragon) | `index_pc.png`, `index_claim_pc.png` |
| `rebirth_pc.jpg`, `rebirth_ready.jpg`, `rebirth_need.jpg`, `rebirth_confirm.jpg`, `rebirth_max.jpg`, `rebirth_refusal.jpg` | REB1..REB6 | `rebirth_*_pc.png` |
| `settings_phone.jpg`, `index_phone.jpg`, `rebirth_phone.jpg` | HatchTestScale 0.7106, cropped | `*_phone.png` |
| `gift_after.jpg`, `shop_after.jpg` | unchanged windows | the popup/Shop build shots |
| `*_zoom.png` | 2-4x crops: nowNext chevrons, progress bars, the Index card row, inspect name + badges, the Settings `-` / `+`, the SKIP price group | |
| `compare_*_build.jpg` | the build next to `compare_*.png` | |

Visual review: a Haiku visual reviewer checks each set against the mockups and the owner's complaint list ("hovers over text", "corners aren't even in the box", "looks so basic"). Fix and re-shoot until it approves.

---

## 9. Build order (TDD; Settings -> Index -> Rebirth)

Settings first: smallest, no Robux, and it proves the shared helpers (`progressBar`, `arrow k`) on a simple page. Rebirth last: it shares a script with the frozen HUD and has the only Robux path.

- [ ] **Task 0: pre-flight and BEFORE evidence.**
  - The fix-round builder is finished: its ledger says so and `get_studio_state` shows Edit. Re-read MenuController, BrickUI and BrickUI.Hatch now (they changed while this plan was written) and write any anchor drift in the ledger.
  - Edit: `workspace:GetAttribute("TestFreshSave")` -> **Expected:** `true`.
  - Play (Client): measure R for Rebirth, Index, Settings = `Window.AbsoluteSize.Y / MainMenu.AbsoluteSize.Y` with each Check-UI window open (wait 0.8 s for the tween). **Expected:** about 0.6315 / 0.7069 / 0.6315; write the measured values (they go into `H.PAGE_CAP_R`).
  - Confirm `H.bindCanvasScale` has the hidden-page guard. **Expected:** present (line ~642).
  - Run `hatch_pure.lua` (Edit). **Expected:** `fail 0`; write the pass count.
  - Play: `hatch_gift_snapshot.lua` -> `hatch_gift_before_ris.txt`; `hatch_shop_snapshot.lua` -> `hatch_shop_before_ris.txt`; `hatch_chrome_snapshot.lua` v3 -> `hatch_chrome_before_v3.txt`; capture `rebirth_before.jpg`, `index_before.jpg`, `settings_before.jpg`. Stop Play. **Expected:** 3 files + 3 shots.
- [ ] **Task 1: backups + legacy copies.**
  - Clone into `ServerStorage._Backup_HatchNight.Before`: `MenuController_preRIS`, `BrickUI_preRIS` (with `Hatch`), `IndexClient_preRIS`, `RebirthClient_preRIS`. LocalScripts `Enabled = false`; every CollectionService tag stripped from each clone and descendant.
  - Folder attributes: `WasEnabled_preRIS = "MenuController,IndexClient,RebirthClient"`; `HowToRestore_preRIS = "Replace MenuController (StarterGui.MainMenu), BrickUI (+Hatch), StarterPlayerScripts.IndexClient and RebirthClient with these copies, Enabled = true on the LocalScripts; delete StarterPlayerScripts.SettingsClient, IndexClientLegacy, RebirthClientLegacy"`.
  - `StarterPlayerScripts.IndexClientLegacy` / `RebirthClientLegacy`: byte copies of today's scripts, `Enabled = false`, tags stripped, attribute `Note = "Fallback only: the new script enables this if BrickUI.Hatch fails"`.
  - Check (Edit): each backup `Source == live Source`; 0 tags in the folder. **Expected:** 6 identical sources, 0 tags.
- [ ] **Task 2: tests first (RED).**
  - Write `hatch_pure.lua` RIS block, `hatch_containment.lua` v3, `settings_client.lua`, `index_client.lua`, `rebirth_page_client.lua`, `hatch_shop_snapshot.lua`, `hatch_ris_perf.lua`; update `hatch_assets.lua`, `streak_client.lua` section 5.
  - Run `hatch_pure.lua` (Edit). **Expected:** R1-R7 FAIL (RED), all older checks pass.
  - Play: `_G.SettingsTests("open")`, `_G.IndexTests("open")`, `_G.RebirthPageTests("open")`. **Expected:** each FAILS on `HatchCanvas` / the band tooth (RED); no script errors.
- [ ] **Task 3: BrickUI.Hatch additions (7.1) with the Task 0 R values.**
  - Run `hatch_pure.lua`. **Expected:** `pass <Task 0 count + 26> fail 0` (GREEN).
  - Diff against `BrickUI_preRIS.Hatch`. **Expected:** only the 7.1 diff-rule lines changed (ledger).
- [ ] **Task 4: SETTINGS.** MenuController 3 lines (4.6) + `SettingsClient` + the BrickUI line (`Settings = "Hatch"`), in one sitting.
  - Play: `_G.SettingsTests` `open`, `toggles`, `volume`, `song`, `reopen`. **Expected:** the 8.3 lines, 0 fails.
  - Containment SET1 (4 scales) + SET2 (2 scales). **Expected:** 0 fails each.
  - Own session (`TestSettingsLegacy = true` in Edit, cleared after): `_G.SettingsTests("legacy")`. **Expected:** `legacy: 4 pass / 0 fail`.
- [ ] **Task 5: INDEX.** `IndexClient` rewrite + the BrickUI line (`+ Index`).
  - Play: `_G.IndexTests` `open`, `tabs`, `cards`, `claim`, `claimall`, `refusal`, `again`, `names`, `lifecycle`. **Expected:** the 8.4 lines, 0 fails.
  - Containment IDX1-IDX4. **Expected:** 0 fails each.
  - Own session (`TestIndexLegacy`): `_G.IndexTests("legacy")`. **Expected:** `legacy: 3 pass / 0 fail`.
- [ ] **Task 6: REBIRTH.** `RebirthClient` page rewrite + the 2 HUD lines + the BrickUI line (`+ Rebirth`).
  - HUD-region diff vs `RebirthClient_preRIS`. **Expected:** only the 6.6 lines (ledger).
  - Play: `_G.RebirthPageTests` `open`, `states`, `confirm`, `refusal`, `skipdry`, `skipreceipt`, `lifecycle`, `tutorial`. **Expected:** the 8.5 lines, 0 fails (`tutorial` fail -> Task 6b, then re-run).
  - New fresh session: `rebirth_client.lua` (run FIRST in the session). **Expected:** `pass 13 fail 0`.
  - Containment REB1-REB7. **Expected:** 0 fails each.
  - Own session (`TestRebirthLegacy`): open -> Check-UI page, `RebirthClientLegacy.Enabled`, exactly 1 `RebirthReadyUI`. **Expected:** 3 pass / 0 fail.
- [ ] **Task 6b (conditional):** section 6.8, then `_G.RebirthPageTests("tutorial")`. **Expected:** `tutorial: 4 pass / 0 fail`.
- [ ] **Task 7: cross-checks.**
  - Snapshots AFTER (8.6). **Expected:** gift and shop identical; chrome v3 legacy = BEFORE v3 except the Settings icon line.
  - `hatch_ris_perf.lua` (8.7). **Expected:** every target met; results file written.
  - `hatch_assets.lua`. **Expected:** `failed 0`.
  - Regression suites (8.9). **Expected:** all green; console clean.
- [ ] **Task 8: screenshots + visual review loop (8.10).** Set `TestFreshSave = false` after the last Play test of the day (read it back: **Expected:** `false`).
- [ ] **Task 9: wrap-up.** Ledger summary; update memory `slingshot-ui-style-hatch-night.md` (Rebirth / Index / Settings built), `roblox-rebirth-system.md` (page v7, dry-run hooks, HUD frozen), `roblox-index.md` (HATCH layout, test hooks), `roblox-polish-1013.md` (Settings in SettingsClient). Tell the owner: **Save + Publish**, plus the owner's calls.

---

## 10. Hard rules

1. **TestFreshSave:** `workspace.TestFreshSave == true`, read in Edit, before EVERY Play. Set it back to `false` after the last Play test of the day and read it back. (False = the tests edit the owner's real save.)
2. **Never stop a Play session you didn't start.** `get_studio_state` before every step; if someone else is in Play, wait for Edit.
3. **No Studio command bar, no Studio dialogs, no Studio UI driving.** DataModel work goes through `execute_luau`; never change `Camera.CameraType` in Edit.
4. **Never publish.** The owner saves and publishes.
5. **No real Robux prompts:** SKIP only with `TestDryRun = true` (enforced in code); the receipt side only through `ServerStorage.TestReceipt`; no `user_mouse_input` on any price button.
6. **Out of scope, do not touch:** Lighting, the hub, the Gift window (StreakClient, PlaytimeClient), the Shop (ShopClient, ShopClientLegacy), the Starter Pack popup (StarterPackClient), StarterPackHud, every server script, RebirthClient's HUD region (except the 2 lines of 6.6).
7. One sitting per window task: never save with a `PAGE_SKIN` key on "Hatch" while that page's script is still the old one.
8. Backups before edits (Task 1); strip tags from every copy.

---

## 11. Risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | The fix-round builder is editing BrickUI / MenuController / ShopClient right now; anchors and line numbers move | Task 0 waits for its ledger + Edit, re-reads all three, anchors by content (never by line number) |
| 2 | The Settings guard `return` in MenuController skips code someone appends later | "KEEP THIS BLOCK LAST" comment; `settings_client open` + `streak_client` + `shop_client open` prove OpenPage, CloseWindow and the viewport re-fit still work |
| 3 | SettingsClient fails silently -> Settings blank for up to 10 s, then Check-UI | Only on failure; the `legacy` session tests the path; console check |
| 4 | Step-11 tutorial card overlaps the bigger Rebirth window (phones: the window is 334 of 346 pt) | `tutorial` check at native + 0.7106; Task 6b fix ready |
| 5 | Breaking TutorialClient / the HUD (RebirthPage name, `Confirming`, `ready`, `pageArrow`) | 6.7 contract table; HUD-region diff rule; `rebirth_client.lua` 13/13 |
| 6 | A real Robux prompt during tests | Dry run enforced in code (`TestSkip` refuses without it); receipts via TestReceipt |
| 7 | Real rebirths / claims change the save | TestFreshSave (rule 1); every test restores its local attributes |
| 8 | Gift / Shop changed through shared helpers | Additive helpers + diff rule; gift and shop snapshots BEFORE / AFTER; containment G1 / S1 |
| 9 | Bigger windows on big PCs (D4) re-scale more GuiObjects per tween frame | The canvas guard keeps hidden pages idle; `hatch_ris_perf.lua`; owner's call 1 offers the Gift size |
| 10 | Index density on phones (47.5 pt cards, 27 pt CLAIM ALL) | Hit boxes = full slot / card / recess height; owner's optional emulator look |
| 11 | GothamBlack wider than estimated on long strings | Mockup factor 0.889 is the max of 24 measured strings; `H.fit` variants on every long line; containment `textFill` fails on these pages |
| 12 | Long names / huge numbers ("BLACK EASTERN DRAGON", "$12.5Qa/s", "$9.99T / $32T") | Split / variant rules; IDX4 and REB7 runs |
| 13 | A creature without a portrait | The kept `fallbackViewport` path (a still ViewportFrame); none today |
| 14 | SettingsServer rate limit (30 changes / 10 s) makes toggle tests flaky | Presses 0.4 s apart; no presses in the leak loop |
| 15 | GameSounds clicks twice on buttons with an `input` hit | Listen once in `settings_client toggles` (count SFX Click plays per press = 1) |
| 16 | The white top-bar gear on the steel-lilac band reads poorly | Ink drop shadow (sticker); owner's call 2; zoom shot |
| 17 | Mockup stand-in art (tile icons, paw, X, eggs, arrow) differs from the real ids | Section 7.4 lists the real ids; the visual reviewer compares layout, not art |
| 18 | Another agent or the owner in Play | `get_studio_state` before every step (rule 2) |

---

## 12. Owner's calls (recommended default in bold) and owner actions

1. **Window size on big PC screens: as big as today per window** (1016 x 645 Rebirth / Settings, 1137 x 722 Index at 1080p), or the Gift size for all three (873 x 555). Studio, 1050x620 and phones are the same either way.
2. **Settings band: steel-lilac with the top-bar gear icon**, or Check-UI silver (then the white gear needs a dark tint).
3. **MUSIC ON: lime like SOUNDS** (one meaning per colour), or keep today's pink.
4. **SKIP Rebirth: gold like every Robux buy in the Shop**, or keep today's purple.
5. **Index card names: in the inspect panel only** (a 67-px card can't hold a 16-px name), or bigger cards in 2 rows (a new layout; not planned).
6. **Keep `RebirthClientLegacy` / `IndexClientLegacy` 7 days live, then delete them** (delete sooner if either script's logic changes first).

**Owner actions after the build:** Save + Publish (File > Publish to Roblox); optional: look at the 3 windows in the Studio phone emulator (Test > Device, iPhone landscape), including the volume drag.
