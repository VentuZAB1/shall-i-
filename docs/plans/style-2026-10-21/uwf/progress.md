# HATCH NIGHT Upgrades + Welcome Back + Free Gift: build ledger (2026-10-22)

Plan `docs/plans/2026-10-22-hatch-night-upgrades-welcome-freegift.md`, review `...review.md` (APPROVE WITH CHANGES: all 6
MUSTs + the SHOULDs). Builder: one Opus session (the RIS builder), the only Studio writer. Coordinator rulings (owner asleep,
"do as recommended"): MUST 1 = hide the hotbar while each window is open (Sell-stall rule); MUST 3 = TestDryRun ON for every
Free Gift session; MUST 5 = the click sink on mouse only, never on touch; the Free Gift "ONE-TIME GIFT!" stays a prominent
headline (red / gold accent, 83 % fit), not a small tag; x2 list as 3 rows OK; CLAIM x5 gold + a one-line rainbow switch;
can't-afford dark; step-10 +1 LV hidden behind a switch; phones in tutorial = H.tutorialFit (as Rebirth). Order: Free Gift ->
Welcome Back -> Upgrades, all in one go; after each run a builder self visual check vs the mockups.

## Task 0 (pre-flight) - 2026-10-22 04:50
- [x] Edit, no Play. hatch_pure **161/0** (after RIS run C). `HatchUWFTests` folder created; `hatch_pages_snapshot.lua`
  (NEW, 6216 B, FNV e257e738) mirrored.
- [x] Play (fresh, TestFreshSave true -> false read back after): `ServerStorage.TestReceipt` + `OfflineDebug` exist;
  `Map.Hub.Stalls.UpgradeStall.UpgradeZone` (-70.0, 0.7, -48.36) r 6.2; `Map.Hub.FreeGift.FreeGiftZone` (0, 0.95, 20) r 7.5.
  - **R_U measured 0.6717** (Root 746.98 x 466.86 of MainMenu 695; plan 0.6718) -> `PAGE_CAP_R.Upgrades = 0.6717`.
  - **RightTiles** left 1437.79 (MainMenu space) -> `right` **87.2** at 1519x753 (plan est. 88).
  - **Hotbar (MUST 1)**: `BackpackGui` DisplayOrder 120, IgnoreGuiInset, frame `Backpack` 655 x 70 at (432.5, 625) screen.
  - BEFORE snapshots: gift reduced 181 groups **4b73c224**, shop ALL **44616b30** (146), chrome Shop 225c112d / Rebirth
    a67275d8 / Index 60d834c0 / Settings 5435f5b8 (= RIS run C), NEW pages ALL **6d1b0fd8** (588 groups, stable 1st try).
    Ruling: the gift / shop hashes depend on per-save random data, not on the UI: this fresh save has PlaytimePet
    VenomBasilisk (the playtime slots) and StarterArea 4 / MagmaEgg / 10000 KG (the shop's starter slot) - run C's session
    had others (ae122c90 / 985d5a8c). AFTER runs set those 4 attributes LOCALLY to these values before dumping.
  - Shots `hatch-night-build/uwf/{freegift,welcome,upgrades}/*_before.jpg` (the REAL live Upgrades window, walk-in, R0 $0);
    `compare_upgrades.png` rebuilt with it (`CUR_UPGRADES=...upgrades_before.jpg python make_compare.py`).

## Task 1 (backups) - 05:00
- [x] `ServerStorage._Backup_HatchNight.Before`: `FreeGiftClient_preUWF` (22452), `OfflineClient_preUWF` (19384),
  `UpgradeClient_preUWF` (19606) disabled, `BrickUI_preUWF` (+ `Hatch`) - all equal to live (6 identical sources incl. the
  legacy copy, review SHOULD 6); attributes `WasEnabled_preUWF` / `HowToRestore_preUWF`; 0 tags.
- [x] `StarterPlayerScripts.FreeGiftClientLegacy` / `OfflineClientLegacy` / `UpgradeClientLegacy`: byte copies, Enabled
  false, 0 tags, Note "Fallback only: the new script enables this if BrickUI.Hatch fails".

## Task 2 (tests first) - 05:05
- [x] `hatch_pages_snapshot.lua` (Task 0), `hatch_containment.lua` **v4** (01ee94ca, 33511 B): `hud()` reads HatchTestScale
  from `cfg.scaleGui`, new `rightHud` (stroked right <= RightTiles left - 6, native) and `hotbar` (no visible BackpackGui
  slot meets the stroked window, review MUST 1) checks, `_G.HatchUWFCfg(name)`.
- [x] `hatch_pure.lua` + block UWF (U0-U10, 43735 B, **3d323ad8**). **RED: pass 175 fail 23** (the 161 older pass; every
  U1/U3/U4/U6/U7-lw/U8-top/U9/U10 assertion fails; the A/B checks pass trivially before the change).
- [x] `freegift_client.lua` (NEW, 15618 B, **e8abf548**): open, fit, walkin, **hotbar** (MUST 1: hidden while open, back on
  close, still hidden when it opens right after a MainMenu window closed, walk-in / walk-away), joined, notjoined, joindry,
  refusal, lifecycle, claim, once, respawn, **touch** (MUST 5), legacy. Every call sets `TestDryRun = true` first (MUST 3);
  claim / once assert `TestLastBuy` unchanged. Mirrored to `HatchUWFTests`. (RED by construction: the old script has no
  TestOpen / TestPress hooks.)

## Task 3 (BrickUI.Hatch additions) - 05:10
- [x] 7.1 written by exact one-occurrence replacements on the pre-UWF source + an additive block before `return H`:
  `windowChrome` opts.w / opts.h (W / HH in the 17 sizes, `headerTeeth(W)` unless 740, Sheen `min(420, 0.57 W)`, titles
  `min(400, W - 128)`, Close / CloseHit / Bats from W, setHeight), `fitWindow` / `tutorialFit` lw / lh,
  `PAGE_CAP_R.Upgrades = 0.6717`, priceButton `glyphImage` / `top` + `topSize` (Top text fill 0.83, group centred under
  it via `topH`; topH 0 = every old y expression) / `btn.setGlyph`, bands FreeGift / Upgrades + PAGE_BAND (WelcomeBack =
  HatchGold), `H.headerTeeth`, `H.hudClear` (right = tiles room + 6 + 5 stroke, review SHOULD 2), `H.guideClear` (a guide
  above the screen = none), `H.fitStandalone`, `H.bindHotbar` (MUST 1: hides BackpackGui while open, holds it hidden against
  MenuController's re-enable, restores on close only if a standalone window hid it - BackpackGui attribute
  HatchHotbarHidden - and no MainMenu / other standalone window is open). Hatch 58034 chars, FNV **e0ae6870**.
- [x] **hatch_pure GREEN: pass 203 fail 0** (161 + 42 UWF). A/B vs `BrickUI_preUWF.Hatch`: windowChrome (both default
  paths) identical, fitWindow 8 rows identical, tutorialFit 4 rows identical, pageCap 5 pages x 4 heights identical,
  priceButton default + `pre` identical.

## Run 1 FREE GIFT (Task 4) - 05:12 .. 05:35
- [x] One sitting: `FreeGiftClient` rewritten (20948 chars, FNV **3632e72b**) + `BrickUI.PAGE_SKIN.FreeGift = "Hatch"`.
  Diff rule checked before writing: the 0.15 s zone poll (751 B) and the sign lines of the RenderStepped (585 B)
  byte-identical to `FreeGiftClient_preUWF`; `findSign` and the 2 refresh sign lines identical (MUST 2 names kept).
- Look: emerald band, 560 x 460 chrome; **ONE-TIME GIFT! stays a big red headline** (24 px red gradient, ink stroke 3,
  a gold star each side; its box hugs it at the 83 % rule) - coordinator ruling, not the plan's 16 px tag; 3 POTIONS! 34;
  x2 list as 3 rows with potion icons; shell step cards with recessed wells; JOIN violet; CLAIM lime (breathing only in
  the joined state) / off / red word / silver CLAIMED!. Every label via `txt()` fill 0.83; JOIN / CLAIM labels HatchFill;
  Thumb FontFace H.FONT + HatchHug (MUST 4). Holder = TextButton HatchBlocker on mouse, a plain Frame on touch (MUST 5).
- [x] Play (fresh save, TestFreshSave true -> false read back): **open 10/0, fit 4/0, walkin 2/0, hotbar 6/0, joined 5/0,
  notjoined 4/0, joindry 2/0, refusal 6/0, lifecycle 3/0, claim 9/0 (real claim: FreeGift true, potions +1 x3, silver
  CLAIMED!, FREE! sign + sparkles off, TestLastBuy unchanged), once 4/0, respawn 4/0** (Server Health 0; hotbar hidden /
  back after respawn too). TestDryRun ON all session (MUST 3): the only TestLastBuy writes were the dry `PromptJoinAsync`.
- [x] Containment (v4, 83 % textFill FAIL rule): **FG1 native 601/0, 0.7261 598/0, 0.6935 598/0; FG2 native 586/0, 0.7261
  583/0; FG3 native 586/0; FG4 native 601/0, 0.7261 598/0** (hotbar + rightHud checks pass at native). One FG3 run right
  after `once` failed 3 (the zone poll closed the window on the walk-away the section ends with: a test race, re-run clean).
- [x] Perf: open RenderStepped 0.25 ms per 30 frames (0.008 ms/frame), max 0.014 ms; closed: RaysLoop false within 0.3 s,
  HatchPerfFreeGift + FreeGiftRefreshN frozen (lifecycle).
- [x] Shots `hatch-night-build/uwf/freegift/`: freegift_joined / notjoined / refusal / claimed / phone (0.7261).
- **Visual review: builder self-check vs mockup** (`freegift_joined_pc.png` vs `freegift_joined.jpg`): same zones, sizes
  and colours; the one intended difference is the big ONE-TIME GIFT! headline (ruling). The refusal word "JOIN THE GROUP
  FIRST!" fits at 18 px (H.fit takes the long variant first); hotbar hidden in every shot. Nothing to fix.
- [ ] Pages snapshot this session ALL 53b783a8 vs Task 0 6d1b0fd8: this session claimed the gift, respawned and had other
  random save data before the dump -> re-dump first thing in the next fresh session (with the Task 0 attribute values).

## Run 2 WELCOME BACK (Task 5) - 05:20 .. 05:35
- [x] One sitting: `OfflineClient` rewritten (18938 chars, FNV **b8a9a8c8**) + `PAGE_SKIN.WelcomeBack = "Hatch"`. Diff rule
  checked before writing: the BASE LINE region (`OfflineBaseUI` .. the 0.25 s loop, 3392 B) byte-identical to
  `OfflineClient_preUWF`; the frozen names `new`, `stroke`, `FONT`, `WHITE` (+ `player`, `OfflineConfig`, `SpeedStat`,
  `TweenService`) kept above it (MUST 2); the old forever RenderStepped deleted.
- Look: gold band 540 x 430; OFFLINE EARNINGS; the cash over turning rays + glow; $547K 52 px green; **CLAIM x5 = gold
  price button with the price inside** (`X5_STYLE = "gold"`; `"rainbow"` = H.RAINBOW face, one line); CLAIM lime. Modal:
  the Holder sinks clicks on every device (MUST 5 allows it). D13 celebration on `OfflineLastX5`; the dry run never sets
  `prompting` (SHOULD 4, probe WelcomePrompting).
- [x] Play (fresh, TestFreshSave true -> false read back; this session also ran with `workspace.TestTouchUI = true`, cleared
  after): **open 13/0** (Amount $547K, price 39 live, Pre CLAIM x5!, AR, CanvasScale, HatchCanvas, Legacy disabled, 1 OfflineUI +
  1 OfflineBaseUI, PerDay exists, hotbar hidden), **claim 2/0 (+547000, pending 0)**, **close 2/0 (+1000)**, **other 2/0
  (+2000, Shop open)**, **x5dry 8/0** (TestLastBuy PromptProductPurchase 3718679677, red TEST SAVE ONLY, price back,
  WelcomePrompting false, refused without TestDryRun, still open, claim +3000), **x5receipt**: TestReceipt true, +50000,
  OfflineLastX5, Amount $50K + shards at +0.78 s, closed 1.6 s later; 2nd receipt false, +0; **x5after**: claim +10000 then
  receipt +40000; **none 1/0**; **tutorial** (TutorialDone false + pending 5000: no window in 4 s, run last, restored);
  **lifecycle 2/0**; **base 2/0 (MUST 2)**: the frozen line shows "You earn $2.07M/Day offline!" on the own base (local
  BaseIncome 120, restored); SHOULD 5 pure cap: amount(2 days) == amount(86400) > 0.
  - Test-harness note: OfflineDebug only fires the client's `OfflineReady` change once; later rounds set OfflineReady false,
    wait 0.4 s, then pending + OfflineDebug (`_G.UWF_PEND`). Same in the old script (unchanged logic).
- [x] Containment: **WB1 native 397/0, 0.7767 394/0, 0.7419 394/0; WB2 ($12.5Qa + price 1499) native 397/0, 0.7767 394/0;
  WB3 (TEST SAVE ONLY held) native 381/0; WB4 (x5 paid held) native 397/0** (hotbar + rightHud + priceGroup pass).
- [x] Perf: open 0.068 ms per 30 frames (max 0.004 ms); closed RaysLoop false, HatchPerfWelcome frozen.
- [x] Shots `uwf/welcome/`: welcome, welcome_big, welcome_x5, welcome_refusal, welcome_phone (0.7767).
- **Visual review: builder self-check vs mockup** (`welcome_pc.png` vs `welcome.jpg`): same zones, gold band, price inside
  the gold x5 button, the amount clear of the cash art. Nothing to fix.

## Free Gift MUST 5 touch proof (this session, `TestTouchUI = true`) - 05:24
- touch 4/1 then the walk-off re-done with `Humanoid:MoveTo` (the ControlModule overwrites `Humanoid:Move` every frame from
  a test context): **Holder = plain Frame, Active false; no FreeGiftUI object sinks input at 3 background points
  (GetGuiObjectsAtPosition); with the window open the character WALKED 13 studs off the pad and the window closed (0.38 s),
  hotbar back.** Limitation: Studio's device emulator needs Studio UI driving (forbidden), so the real thumbstick was not
  pressed; the Frame holder is the same pass-through as the old window.

## Other windows unchanged (session 2, fresh, the Task 0 save values PlaytimePet VenomBasilisk / StarterArea 4 / MagmaEgg /
10000 KG came up by themselves)
- [x] **Pages ALL 6d1b0fd8 (588 groups) = Task 0 BEFORE** (Settings / Index / Rebirth). (Session 1's 53b783a8 was taken
  after a claim + respawn: state.)
- [x] **Chrome Shop 225c112d / Rebirth a67275d8 / Index 60d834c0 / Settings 5435f5b8 = Task 0 BEFORE.**
- [x] Shop ALL d31e8fb0: every chrome / page-frame group = the RIS baseline list; the only groups that differ are the known
  session-state groups (GiftPicker.Box, Rail.Label1-5, Scroll.List - the RIS ledger's ruling).
- [x] Gift 181-group list 096d8710 (stable in-session: the same 6 min later): every HatchBack / HatchFront chrome group =
  the RIS baseline; the differing groups are the content state (Daily cards 1 / 7 + Streak, Playtime slots / PlayBar /
  SkipAll, the tab Pill / Dot) - day / playtime state, not Hatch code (every shared helper's default path is A/B-identical:
  hatch_pure U2 / U5-U8).

## Run 3 UPGRADES (Task 6) - 05:36 .. 05:47
- [x] One sitting: `UpgradeClient` rewritten (24769 chars, FNV **6665e8ac**) + `PAGE_SKIN.Upgrades = "Hatch"`. Diff rule
  checked before writing: FAST GRAB (455 B, moved below the build), the zone poll (816 B) and SHIELD (2114 B) byte-identical
  to `UpgradeClient_preUWF`; their names (`U`, `ProximityPromptService`, `player`, `B`, `RunService`, `TweenService`, `SFX`,
  `SlingConfig`) kept (MUST 2). The forever 1 s loop and the forever RenderStepped are gone (D11).
- Look: royal-blue band, violet REBIRTH pill, 3 shell rows (icon on a glow, name / short desc / Sling area word, LV bar,
  now > next), money button lime / **off when you can't afford** (`SHORT_RED` one line) / off + lock "REBIRTH n" / silver
  MAX / lime FREE!; **gold +1 LV** with the price inside. Switches `FULL_COPY` / `SHORT_RED` / `HIDE_ROBUX_IN_TUTORIAL`
  (false path defined: +1 LV stays, no arrow, the button breathes). SHOULD 1 box fixes (Sling Desc 200 wide; Joined 130).
  Fit = `H.fitStandalone` with `pageCap("Upgrades")` (big PCs as big as today); a tutorial guide moves it down / shrinks it
  (`H.tutorialFit`, the Rebirth step-11 recipe).
- [x] Play (fresh, TestFreshSave true -> false read back): **open 11/0, walkin 4/0 (hotbar hidden / back), robuxdry 4/0
  (TestLastBuy `["Upgrades.Buy","Grab","robux"]`, red TEST! word, refused without TestDryRun), states 4/0 (off / locked +
  lock glyph / MAX silver + gold stat), step8 5/0 (FREE!, arrow, breathing, motion off after), step10 5/0 (arrow,
  Sling +1 LV hidden, Grab +1 LV shown, back after), lifecycle 3/0 (closed: UpgradeLoop false, 20 Money changes ->
  UpgradeRefreshN frozen), buy 4/0 (real $ buy: SlingLevel +1, money spent, bar LV 1/25)**; **+1 LV via TestReceipt**
  (Grab product 3716713439): true, GrabLevel 0 -> 1.
- [x] Containment: **UP1 native 1245/0, 0.7106 1242/0, 0.6407 1242/0 (MUST 6), 1.0114 1242/0**; forced 1.46 (noOnTop)
  3 fails = the HatchBack stroke 1.1 px over the top of the 695-tall Studio gui (a 1080p scale emulated on a smaller
  screen; on a real 1080p gui the window is 686.6 of 1022). **UP2 step 8 (guide on screen, s 1.147) native 1155/0, 0.7106
  1152/0; UP3 (MAX + Robux refusal held) native 1058/0** (first run 1 fail: TutorialUI's finish screen on top after my
  local FreeSling flip - re-run clean, the RIS REB3 artifact); UP3 0.7106: the same 1 onTop fail (TutorialUI, same run, not re-run); **UP4 (locked / $ refusal
  "NEED R3" held / price 1499) native 1237/0, 0.6407 1234/0.**
- [x] Perf: motion loop (only in steps 8 / 10) 0.30 ms per 30 frames, max 0.019 ms; closed = no loop, no motion, no
  refresh. UpgradeUI 251 GuiObjects / 416 instances.
- [x] Shots `uwf/upgrades/`: upgrades_mid, upgrades_free_step8 (the tutorial step-8 overlay: guide above, window moved
  down), upgrades_step10 (step-10 overlay), upgrades_max, upgrades_refusal, upgrades_phone (0.7106),
  compare_upgrades_build.jpg (live BEFORE vs AFTER), upgrades_zoom_buttons.png.
- **Visual review: builder self-check vs mockup** (`upgrades_pc.png` vs `upgrades_mid.jpg`): same rows, sizes, colours,
  pill, bar, now > next, buttons. Nothing to fix.

## Legacy session (all 3 fallbacks at once: TestFreeGiftLegacy / TestWelcomeLegacy / TestUpgradesLegacy) - 05:48
- [x] **FG legacy 3/0, WB legacy 3/0, UP legacy 2/0**; the old Check-UI Free Gift opens on walk-in
  (`freegift/freegift_legacy_fallback.jpg`). Console: only the 3 expected "fallback ... (switch)" warns, no errors.
- [x] Chrome Shop 225c112d / Rebirth a67275d8 / Index 60d834c0 / Settings 5435f5b8 (= BEFORE again).
- [x] Pages: this fresh session 53b783a8 (as session 1), session 2 6d1b0fd8 (= Task 0): two values across fresh sessions
  with the same code -> per-save data, not code (session 2 proves the new code reproduces the BEFORE dump exactly).

## End state - 05:50
- Edit. **TestFreshSave false** (read back); cleared and read back nil: TestFreeGiftLegacy, TestWelcomeLegacy,
  TestUpgradesLegacy, HatchBand, HatchTestScale, TestTouchUI, TestSettingsLegacy, TestIndexLegacy, TestRebirthLegacy,
  TestCardNames. TestStarterPack stays true. PAGE_SKIN = Gift / Shop / Settings / Index / Rebirth / FreeGift / WelcomeBack
  / Upgrades "Hatch". The 3 new scripts enabled, the 3 Legacy copies disabled, 0 tags.
- Not done (time): `hatch_uwf_perf.lua` as a file (perf measured inline above), `hatch_assets.lua` + the 7.3 ids (all ids
  already used in-game and seen loaded in the shots), the 30x leak loop, the regression suites (streak_client,
  rebirth_client, starter_hud, StarterPack / Streak / RebirthV6 / HubV2 tests) - next session.
- Owner calls to show: big ONE-TIME GIFT! headline (kept big, ruling), gold CLAIM x5 (rainbow = 1 line), dark
  can't-afford (red = 1 line), step-10 +1 LV hidden (1 line), hotbar hidden while these windows are open.

## Coordinator review - 05:55
- **Visual review: orchestrator, SHIP** (the three compare_*_build.jpg: Free Gift, Welcome Back, Upgrades read clean, nothing over text, corners inside).

## Follow-up (coordinator: regression suites, assets, leaks, UP3) - 06:00 .. 06:25
Edit pure: **StreakTests 24/0, StarterPackTests 38/0, RebirthV6Tests 45/0.**
Session A (fresh; TestFreshSave true read back before Play, false after):
- [x] **streak_client v2 48/0** (first in the session), **rebirth_client 13/0**.
- [x] `hatch_uwf_perf.lua` (NEW): **idle 6/0** (all 3 closed + 20 Money changes: every probe frozen, no loop);
  **leaks 12/0**: 30 x open / close each (Upgrades + 2 dry Robux presses per round): PlayerGui GuiObjects 4105 -> 4105,
  descendants 8572 -> 8572 for all three; Lua heap +0.3 MB per window (7.9 -> 8.2, 8.4 -> 8.7, 8.9 -> 9.2 MB).
- [x] **UP3 re-run, the tutorial screen cleared (TutorialUI disabled during the run): 0.7106 1055/0, native 1058/0.**
- [x] `hatch_assets.lua` + the 5 UWF ids (group, heart, rocket, bolt, shield heart; 3931 B, FNV c1aa8050, mirrored
  `HatchUWFTests.hatch_assets`): **assets 73 (72 image ids + the bat), ok 73, failed 0** (all 8 HATCH windows).
- [x] **shop_client 80/0** (open 15, layout 15, prices 22, refusal 7, scroll 11, reopen 4, analytics 4, canvasguard 2).
- [x] **starter_popup_client**: open 31/0, inside 7/0, timer normal 8/0, buy 7/0; seen 1/1: the open -> StarterPopup true
  check passes; the precondition (StarterPopup false) fails because TestStarterPack's auto-popup (on by rule) opens and
  marks the offer seen within seconds of the server reset, before a client call can run (twice) - harness timing.
- [x] Server live: **StreakTests 20/0, StarterPackTests 33/0, RebirthV6Tests 5/0, TutorialV11Tests 13/0.**
- HubV2Tests all-in-one after those: 105/3 (T10.1 / T10.4b / T11.2) = state from the live suites (Rebirths 20, pets).
Sessions B / C (fresh, HubV2 first):
- B all-in-one: 106/2 (T10.4b: the suite needs the documented CLIENT equipBest step between T10.4 and T10.4b; T11.2).
- **C with the client step: T2 22/0, T10.1 8/0, T10.2 5/0, T10.3 12/0, T10.4 2/0, [client equipBest], T10.4b 3/0,
  T10.5 9/0, T10.11 3/0 (boards + free sign + lamps), T11 46/1** (T11.1 makeover placements, T11.3 pathfinding, T11.4 walls
  hold pass; **T11.2 avenue walker fails only in sequence**: the first leg never starts from the fresh `put`; alone it
  passes 3 / 3, also right after T11.1). Later T11.1 runs gave 15/1 (Treadmill_B1 off the R0 layout after T10.5 changed
  the base-1 treadmill tier: state). No server / world / hub file was touched by UWF -> not fixed here (hub scripts are
  out of scope); flagged for the hub owner: T11.2 needs a settle wait after `put`, T11.1 needs the R0 treadmill.
- End: Edit, TestFreshSave false (read back), all switches nil, TestStarterPack true.
