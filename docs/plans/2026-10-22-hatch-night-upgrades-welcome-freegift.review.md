# Review: HATCH NIGHT Upgrades + Welcome Back + Free Gift plan (2026-10-22)

Plan: `docs/plans/2026-10-22-hatch-night-upgrades-welcome-freegift.md` (839 lines). Reviewer: plan reviewer (read-only).

**Read:** the plan (all), `compare_*.png`, `qa_report.txt`, the RIS plan review + ledger (`ris/progress.md`), the popup/Shop
review headings, the containment harness (`tests-2026-10-21/hatch_containment.lua` v3).
**Code read in Studio** (Edit, nobody in Play; `script_read` / `script_grep` only): FreeGiftClient, FreeGiftServer,
OfflineClient, OfflineServer, OfflineConfig, UpgradeClient, UpgradeServer, UpgradeConfig, Receipts (TestReceipt),
BrickUI.Hatch (all 1092 lines), BrickUI `skinFor` / `PAGE_SKIN`, MenuController 1-345 (tutorialTop, hatchFit,
setHotbar, closeWindow), TutorialClient (guide 100-291, steps 8-11 395-540, start/check 690-796), PetsEggsUI
(tilesAway / slide 487-567), StreakClient auto-open, RebirthClient `windowOpen`, StarterPackClient holder, GameSounds,
Satchel (`BackpackGui` DisplayOrder, hotbar layout).

## Verdict: **APPROVE WITH CHANGES**

The plan is careful and its numbers re-derive (fit rows, `headerTeeth` 37 / 28 / 27 teeth, `tutorialFit` 1.1498 /
cy 418.8, the U-table expectations, the UpgradeConfig-based test values: cost(7) $150K at R2, Grab Lv2 = REBIRTH 3,
Shield = REBIRTH 10, `slingRange(25)` = 2300, CELESTIAL). It carries most earlier lessons: one switch per window,
decide-first fallback before frozen regions, dry run enforced in code before the remote, Size pop instead of UIScale,
nothing running while closed, fixed-width gloss buttons, hoverScale 1 for 8 px neighbours, A/B pure tests + 4
snapshots. Six MUSTs remain. Two are new geometry/behaviour problems that the HatchTestScale emulation can't see (the
hotbar and touch input). Two are repeats of RIS findings (83 % wiring, the frozen-region contract). Two are test
safety / correctness.

---

## Verified (no change needed)

| Claim | Result |
|---|---|
| Region line numbers | OfflineClient WINDOW 21-267 + 347-349, BASE LINE 269-345; UpgradeClient FAST GRAB 45-53, WINDOW 55-351, SHIELD 353-407: exact. |
| `B.skinFor(key)` | `PAGE_SKIN[page] or WINDOW_SKIN` (BrickUI 586): new keys are harmless; MenuController only asks for its own PAGES. |
| Server untouched + contracts | FreeGiftServer: `GetGroupsAsync` group check, `FreeGift` set first, refusals wait / claimed / slow / group. OfflineServer: tutorial players get nothing, Claim pays once, x5 receipt pays `pending + last x 4` once (`OfflineLastX5`), `OfflineDebug`. UpgradeServer: FreeSling taken by either button, Robux prompts on the SERVER (`PromptProductPurchase`), receipts refuse at `band.upTo`. All match 4.7 / 5.7 / 6.7 and the test expectations. |
| Readers of the 3 guis | Only `.Enabled` (TutorialClient 425 / 516, RebirthClient 726, StarterPackClient 613, StarterPackHud MODALS, StreakClient 963). |
| Helpers consumed | `H.text` opts.fill, `H.fit` HatchFill, priceButton Word HatchFill + Pre/Price HatchHug, `nowNext` HatchHug, `progressBar` Text fill 0.83, `pageCap` / `PAGE_CAP_R`, `tutorialFit`, `shellCard{noHit, noHover, tile, grad}`, `recess(.., radius)`, `tag`, `PAL.violet`, `ICON.*` all exist with the signatures the plan uses. |
| Tutorial guide | Step 8 starts the guide from a local `FreeSling` change (`check()` -> `start(true)`), step 10 from `TutorialExtra` 2: UP2 / step10 setups work. |
| TestReceipt | Runs the product handler and returns its result: `x5receipt` / `robuxreceipt` / `maxreceipt` expectations are right. |

---

## MUST changes

### 1. The hotbar draws over the bottom of these windows (sections 3, 4.4, 5.4, 6.4, 6.5, 8.2; new)

MainMenu windows hide the hotbar while open (`MenuController.setHotbar(false)`, lines 178 / 291 / 313); these three
standalone windows don't. Satchel's `BackpackGui` is **DisplayOrder 120** (> 20), IgnoreGuiInset, hotbar frame 70 px
(5 + 60 + 5) at the screen bottom (satchel 163-164, 311-317), always shown (the bat in slot 1). The plan's fit uses
MainMenu's full safe box (made for windows that hide it), so:
- **1050x620:** hotbar slots y 555..615 (screen). Free Gift CLAIM = 518..589, under the slots by 34 px; Welcome Back and
  Upgrades shell bottoms (593 / 577) are under them. Today (deviceScale 1.0) all three end above 550.
- **Studio 1519x753, tutorial steps 8 / 10:** Upgrades s 1.1498, cy 418.8 -> bottom 747 (screen) vs slots 688..748: the
  Wave Shield row and the foot sit under the hotbar. UP2 / `upgrades_free.jpg` will fail `onTop` at native.
- **Phones 844x390:** hotbar from 320; Free Gift CLAIM 327..371 is fully under it.

HatchTestScale runs are centred and smaller, so only the Studio tutorial run catches it; the mockups don't draw the hotbar.

**Required.** Default (recommended; same rule as every MainMenu window, incl. the walk-in Sell stall): **hide the
hotbar while the window is open.**
- On open, set `BackpackGui.Enabled = false`. Then hold it false while open: MenuController's `closeWindow` re-enables
  it 0.15 s later from its tween's `Completed`, so watch `BackpackGui.Enabled` while open.
- On close, set it true only if `MainMenu.Window.Visible == false` and no other of the 3 guis is Enabled.

Alternative (owner's call): keep the hotbar and add a bottom clearance to `H.fitStandalone`:
- clearance = the visible hotbar's top - 6, in MainMenu space;
- 1080p unchanged; 1050x620 Free Gift s ~1.04;
- phones drop to s ~0.57 (9 pt).

Either way:
- Task 0 measures the hotbar frame.
- Tests:
  - containment adds a `hotbar` check (no visible BackpackGui slot meets the stroked window, native + tutorial);
  - `freegift_client` / `upgrade_client` gain a `hotbar` section: hidden while open; back after close; still hidden
    when the window opens straight after a MainMenu window closes.
- Add it to section 12.

### 2. Keep the names the frozen regions use (5.6 "Delete", 4.6, 6.6; repeat of RIS SHOULD 1)

OfflineClient's byte-identical BASE LINE (269-345) calls `new(...)` (270, 271, 274, 277), `stroke(line, 3.5)` (275),
`FONT` and `WHITE` (271). These are Check-UI builder locals defined in the WINDOW region, and 5.6 says "Delete:
Check-UI builders". As written, the base line errors at load (no `OfflineBaseUI`, no "$X/Day").

**Required:** add a frozen-region contract table and keep these locals above the frozen code:
- Offline base line: `new`, `stroke`, `FONT`, `WHITE`, `player`, `OfflineConfig`, `SpeedStat`, `TweenService`.
- Upgrade SHIELD: `B` (`B.text`, `B.LUCKY`), `RunService`, `TweenService`, `SFX`, `SlingConfig`, `player`.
- FAST GRAB: `U`, `ProximityPromptService`, `player`.
- Free Gift zone poll / sign lines: `findSign`, `refresh`, `claimed`, `setOpen`, `sign`, `signScale`, `signText`,
  `signStroke`, `sparkles`, `SIGN_NEAR`, `SIGN_FAR`.

`welcome_client open` already counts `OfflineBaseUI`. Also assert its `PerDay` label exists.

### 3. No real Join prompt from the real claim (8.3 `claim` / `once`, D12, risk 1)

The auto-join after a "group" refusal calls `promptJoin()`. `claim` runs without `TestDryRun`. If the server's group
check comes back false (e.g. a `GetGroupsAsync` hiccup in Studio), the client opens a **real** `PromptJoinAsync`.

**Required:**
- Every Free Gift test session sets `gui.TestDryRun = true` first. Only `joindry`'s negative half clears it, then
  restores it.
- `claim` / `once` assert `TestLastBuy` unchanged (no join attempted).

### 4. Wire the 83 % rule on every label (4.1 / 5.1 / 6.1; repeat of RIS MUST 1)

`HatchFill` is opt-in (Hatch 174 / 204). The plan sets it on only 6 labels (Tag, JOIN, both CLAIMs, Amount,
RebirthPill). Variants on the other labels (step titles, How1 / How2, Each, Name, Desc, Area, Joined, Heading, Foot)
fall back only at 100 %, and containment `textFill` is a FAIL off Gift.

**Required:**
- Each script builds text through a local `txt()` passing `fill = 0.83`.
- Set `HatchFill 0.83` on every gloss label and on the `H.tag` Label (H.tag has no fill option).
- The priceButton `Top` text gets fill 0.83.
- The 👍 Thumb uses `FontFace = H.FONT` (else a `font` FAIL) and `HatchHug = true`: it's an icon, and a 40 px emoji in
  a 48 box is about 90 % (a textFill FAIL).

### 5. D14 must not swallow touches on phones (D14, 2, risk 12)

A full-window TextButton `Holder` sinks touch input. On a phone the Upgrades / Free Gift window covers gui
x 144..670 of 732 and y 6..340, so the dynamic thumbstick (and part of the jump button) can't start under it. Today the
window is plain Frames (touches pass through), so phone players can simply walk out of the stall / chest pad. Also,
GameSounds hooks every GuiButton (hover tick + click on the window background).

**Required:**
- Keep the sink for mouse only (no `TouchEnabled`: the TextButton).
- On touch screens the Holder is a plain Frame (today's pass-through). Welcome Back may keep the sink (modal).
- Test it once in the phone emulator (walk out of the zone with the thumbstick) and write it in the ledger.

### 6. Upgrades' smallest real scale is untested (8.2 UP1 / UP4)

UP1 and UP4 run **0.6787**, which is the Gift/Rebirth 667x375 scale. Section 3 gives Upgrades **0.6407** at 667x375
(10.3 pt, width-limited by the right tiles).

**Required:**
- Replace 0.6787 with 0.6407 in UP1 / UP4 (the `tutorial` section keeps its 3 scales).
- If MUST 1 takes the clearance alternative, also run FG / WB at their new 1050x620 scale.

---

## SHOULD changes

### Layout
1. **Overlapping label boxes (repeat of RIS SHOULD 5).**
   - Sling `Desc` (100..316) overlaps `Area` (308..420) by 8 px: make the Sling Desc `(100, 38, 200, 16)` ("LAUNCH
     FURTHER" about 72 %).
   - `Joined` (64..200) is 6 px from `Done` (206): make it `(64, 30, 130, 22)`.
2. **Refit triggers (section 2).**
   - **The guide's position.** `TutorialUI.Guide` tweens its Position: off-screen while a MainMenu window was open just
     before (then 0.3 s back), and to CARD_LOW 0.185 under an AreaTitle / WaveBanner (TutorialClient 256-290). Refit on
     its `AbsolutePosition` while open; `guideClear` ignores a guide above the screen.
   - **The right tiles.** A Pets/Eggs side panel closing on `WindowOpened` slides `RightTiles` back in over about 0.5 s,
     so a fit at open sees no tiles. Refit on `RightTiles.AbsolutePosition` while open (signals, no loop).
   - **The chrome stroke.** `right` should include the chrome stroke (3.5 x s): at 1050x620 the width-limited Upgrades
     sits 2.5 px from the tiles.
3. **Switch false paths must be legal (D10).**
   - `HIDE_ROBUX_IN_TUTORIAL = false` leaves the FreeArrow (622..682) over the visible +1 LV button (592..710). Define
     that path, e.g. no arrow, the Buy breathes and the guide text points.
   - `FULL_COPY = true`: "Launch further down the runway" is about 230 px at 12 px in a 211 px room, so it fails at its
     own minimum. Give it a wider box (Grab / Shield: to 420; Sling: drop the Area word) or HatchMin 10.
   - Run one containment pass with each switch flipped.

### Behaviour and tests
4. **Welcome Back dry run.** It must not set `prompting`, or later presses and the other-window x1 claim stay blocked
   until a real `PromptProductPurchaseFinished`. `x5dry` asserts a probe `WelcomePrompting == false` afterwards.
5. **Welcome Back coverage and hygiene.**
   - Add `none`: pending 0 / seconds < MIN -> no window in 4 s.
   - Add a pure 24 h cap check: `OfflineConfig.amount(p, 2 days) == amount(p, 86400)` with a stub `BaseIncome`.
   - Run `tutorial` (server TutorialDone false starts TutorialClient) **last** in its session. Clear `OfflinePending`
     after it, and wait for `TutorialUI.Finish` to hide before any containment (the RIS REB3 artifact).
6. **Task 1 count (repeat of RIS SHOULD 13).** It is **6** identical sources: FreeGiftClient, OfflineClient,
   UpgradeClient, BrickUI, BrickUI.Hatch, FreeGiftClientLegacy. Not 5.
7. **TestFreshSave.** Set it false and read it back after every Play session the builder stops (the RIS practice), not
   only at the end of the run (10.1).

### Owner taste (section 12)
8. **Add and flag these calls.** Show the compare sheets.
   - (a) **The hotbar call** from MUST 1.
   - (b) **Free Gift content changes.** The x2 line becomes 3 rows, the red hint becomes the CLAIM word, and today's big
     red "~ ONE-TIME GIFT! ~" line becomes a 16 px tag. That reads much quieter: "basic" risk. Consider the tag at 18-20.
   - (c) **Call 3, the dark can't-afford button.** It is consistent with the Rebirth "off", but the hub's treadmill signs
     next to the stall stay green/red.
   - (d) **Call 4, gold x5.** The old rainbow was a deliberate "special" look; show the sheet's RAINBOW variant.
   - (e) **Call 6.** Hiding the +1 LV in step 10 changes today's step-10 look.

---

## Owner's calls: defaults

| # | Default | Review |
|---|---|---|
| 1 | Bands emerald / gold / royal blue | Keep. |
| 2 | Upgrades as big as today on big PCs | Keep (1081 x 687 at 1080p; the hotbar is clear there). |
| 3 | Can't-afford dark | Keep, but tell the owner (SHOULD 8c). `SHORT_RED` is one line. |
| 4 | CLAIM x5 gold | Keep, but show the rainbow alternative (SHOULD 8d). |
| 5 | Short copy | Keep. FULL_COPY must work if flipped (SHOULD 3). |
| 6 | Hide +1 LV in step 10 | Keep. Define the `false` path (SHOULD 3). |
| 7 | Phones in steps 8 / 10: s 0.58 | Keep, the same as Rebirth step 11. Only valid with MUST 1's default (hide the hotbar). With the clearance alternative it drops further. |
| new | Hotbar while a walk-in window is open | Default: hidden (MUST 1). |

## What's good
- **Decide first, then build, then the frozen parts (D15).** The legacy copy returns before any frozen region, and the
  `legacy` sections count exactly 1 of each frozen gui.
- **Dry run before the remote (D12).** It recognises that the +1 LV prompts on the SERVER. TestPress refuses without
  a dry run.
- **D13 (celebrate on `OfflineLastX5`).** TestReceipt never fires `PromptProductPurchaseFinished`, so this is the only
  way the x5 path is testable. It also fixes a late live receipt.
- **D11.** Three forever RenderSteppeds and a forever 1 s loop go; probes prove they're gone.
- **Exact layouts.** Every gutter and margin is listed, and the QA covers 26 views.
