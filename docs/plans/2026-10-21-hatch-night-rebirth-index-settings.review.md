# Review: HATCH NIGHT Rebirth + Index + Settings plan (2026-10-21)

Plan: `docs/plans/2026-10-21-hatch-night-rebirth-index-settings.md` (792 lines). Reviewer: plan reviewer (read-only).

**Inputs I read:**
- the plan, all of it;
- the mockups `compare_rebirth/index/settings.png`, `sheet_phone.png` and `qa_report.txt`;
- the style spec;
- the Gift review (MUST 1 rings), the popup/Shop review, visual review and perf review, and the popup/Shop ledger.

**Code I read in Studio** (`script_read` / `script_grep` only, nothing written):
- MenuController (all), BrickUI (viewport fix + tail), BrickUI.Hatch (all 961 lines);
- RebirthClient (all), IndexClient (all), IndexConfig, TutorialClient (UI build, card sync 255-291, step 11 459-485);
- BackpackButton, DayNightClient, GameSounds (button hook), PotionConfig;
- the test files `hatch_containment.lua` (v2.2), `hatch_pure.lua` and `rebirth_client.lua`.

**Not read:** someone else's Play session was running (the MCP saw the client DataModel), so I could not read IndexServer, SettingsServer, PetIndex or RebirthServer. I did not stop that Play session. SHOULD 6 covers the one place where this matters.

## Verdict: **APPROVE WITH CHANGES**

The plan is careful. It applies most lessons from Gift and Shop:
- one `onScreen()` signal;
- dry run enforced in code;
- legacy copies in PlayerScripts;
- `PAGE_SKIN` cleared on fallback;
- InfoType Product;
- a frozen HUD region with a diff rule;
- additive helpers with a diff rule.

The fit numbers re-derive exactly. Five MUSTs remain, three of them repeats of earlier rulings:
- the 83 % text-fill wiring;
- the CLAIM-ring draw order;
- the hover/pulse test switches.

The step-11 tutorial overlap is not a "maybe": it happens at Studio native, at 1050x620 and on phones, and the planned Task 6b fix makes it worse.

---

## Verified (no change needed)

| Claim | Result |
|---|---|
| `B.skinFor`, `PAGE_SKIN` (BrickUI 585-586), MenuController `applySkin` / `hatchFit` / `openName` declared above `hatchFit` | yes. `hatch.setTheme(H.bandTheme(name))` and `H.pageCap(openName, gs.Y)` already handle any Hatch page. |
| Settings guard placement | The Settings block is the last block (lines 318-501). `local body = panel:WaitForChild("Body")` is line 325, and every connection is made above it. `if ... then return end` at chunk level is valid Luau. `PAGES.Settings` already exists (line 122) and only gains `icon`. `for name in PAGES` only hooks existing tiles, so no Settings tile appears. |
| HUD region of RebirthClient | The marker is at line 460. The `pageArrow` lines are 656-660 and the RenderStepped line is 686, exactly as 6.6 says. `TUT_ARROW` is defined at line 528, before 656. |
| TutorialClient contract | It reads `Body.RebirthPage` (name), `.Visible` and attribute `Confirming` only (268-283, 459-485). |
| Viewport fix present and not in conflict | `B.trackStroke` / `B.viewportSize` / `B.onViewport` and `waitViewport(5)` are in BrickUI 64-125 and 592-604. The plan only touches the `PAGE_SKIN` line in BrickUI. |
| `bindCanvasScale` hidden-page guard | Hatch line 642. |
| Helper signatures used by the plan | `H.image`, `H.chip(.., radius)`, `H.recess(.., z, radius)`, `H.tag`, `H.dot`, `H.sticker`, `H.glow`, `H.segment`, `H.shellCard{noHit, noHover, solid, tile, z}`, `glossButton{faceFrame, input, pulseAmp, hoverScale}`, `H.priceButton{pre, glyph, size}`. All match. |
| `H.pageCap` rewrite | The Shop result is unchanged (1.7718). R 0.6315 / 0.7069 come from the ledger (438.9 / 491.3 of 695). The 1080p Index ratio also comes out about 0.707: the old `fitScale` pill limit scales with the screen. |
| Section 3 rows and the R3 / R4 expectations | Re-derived: 1.3732 / 1.5371 / 1.0982 / 0.7106, and cx 960 / 980.85 / 635.65 / 407.24. |
| Layout gutters | Index, Rebirth and Settings all have 8 px gaps, and every box ends at x 730 / y ≤ 454. |
| `Potion_<key>`, `IndexBonus`, `IndexConfig.version` / `isUpdated` | They exist. The `again` (claimed 2 < version 3) and `claim` (version(1) = 2) setups are correct. |
| DayNightClient | `ClockTime` jumps at once (no tween), so the 2 s check works. |
| GameSounds | It hooks every GuiButton once. An `input` TextButton gives one click (risk 15 is fine). |
| MainMenu survives respawn | IndexClient, RebirthClient and ShopClient already build into `MainMenu.Body` from PlayerScripts once, and the Shop respawn check passed. |

---

## MUST changes

### 1. Wire the 83 % rule: `HatchFill` on every page label, and `HatchHug` on the now > next parts (sections 7.1.4, 4.6, 5.6, 6.6)

This repeats the Shop visual review's MUST 1.

**`HatchFill` is opt-in.** `H.fit` uses `room = (box - 2 x stroke) x (HatchFill or 1)` (Hatch line 203). Only the priceButton Word and the ShopClient / StarterPack labels that set it get the 83 % room. The plan never sets it. So every variant list falls back only at 100 %, and containment v2.2 (`textFill` is a FAIL on non-Gift pages) fails on cases like these:
- inspect V `"$12.5Qa/s"` in a 94 box, about 95 %;
- a longer `"YOU HAVE ONE: … KG"`;
- the refusal words on the REBIRTH and CLAIM gloss labels.

**`HatchHug` is missing on now > next.** `H.nowNext` makes Now and Next boxes of `tw + 8`, which is about 95 % fill. Containment skips only labels with `HatchHug` (`hatch_containment.lua` 260). As planned, every Head and every reward `Line` is a textFill FAIL.

**Required:**
1. Add an additive `opts.fill` to `H.text`: it sets `HatchFill` **before** its first `H.fit`, and the default path is unchanged. Each page builds text through a local `txt()` that passes `fill = 0.83`.
   - The gloss labels of REBIRTH, CLAIM, Toggle and CLAIM ALL get `label:SetAttribute("HatchFill", 0.83)` after creation. Their texts are re-fitted on every state change, so the attribute takes effect.
2. `H.nowNext` sets `HatchHug = true` on Now and Next, as `priceButton` does for Pre and Price.
3. `hatch_pure` gains R9: a 100-wide `H.text` with `fill = 0.83`, given `{"WWWWWWWW", "W"}`, picks the short variant.

### 2. The Index selection Ring goes UNDER the card content, in `Card.Face` (5.1 Cards table)

This repeats Gift review MUST 1.

**The problem:**
- The plan puts `Ring` in `badges` (Z7, the top layer). Its 3 px lime band (x 3..6 and 60.8..63.8) draws over the Portrait (x 4.4..62.4, plus the hover tilt).
- The existing containment `drawOrder` check matches `^Card%d$` + `HatchHolder`, so it covers the Index cards. It requires `ring.Parent == Face`, and fails with "no Ring" on a card that has none.

**As planned, IDX1-IDX4 fail on every card.**

**Required:**
- Create `Ring` on all 5 cards as a child of `Face` at ZIndex 1, after `Glow`. The geometry is unchanged: its outer box equals the face, and corner 11 + 3 = 14 = the face corner.
- Toggle only its `Visible`.
- `Badges` holds nothing on Index cards.

### 3. Step-11 tutorial: test the right object, and make the window clearance a measured, top-anchored fit (6.5, 6.8, 8.5 `tutorial`, Task 6b)

**(a) The test reads a hidden frame.** On Check-UI, TutorialClient hides the studded `TutorialUI.Card` (line 135). The visible guide is the new frame `TutorialUI.Guide`:
- 720 x 118, AnchorPoint (0.5, 0), y 0.015;
- UIScale = `deviceScale() x phoneFactor` (0.8 on touch screens under 520 px).

Both the `tutorial` check and the 6b code use `Card`, so the check measures an invisible object.

**(b) The overlap is certain, not conditional.**

| Screen | Window top (gui) | Guide bottom |
|---|---|---|
| Studio 1519x753 | 70 | about 149 |
| 1050x620 | 23 | about 126 |
| 844x390 | 6 | about 64 |

Even if TutorialUI ignores the top inset (58 / 58 / 44 px), the overlap is 22 / 46 / 15 px. Only 1080p and larger PCs clear: there the window top is 188 and the guide bottom about 154.

**(c) The planned 6b fix is worse than the problem.** It shrinks symmetrically (`gs.Y - 2 x topClear`):
- at 1050x620, s 0.61-0.85, which is text of 9.7-13.6 px;
- on a phone, s 0.41, which `fitWindow` clamps to 0.5 (8 pt text). The window, centred at 173, still starts at about y 55, so it still overlaps.

It also compares `AbsolutePosition` values across two ScreenGuis with different inset handling.

**Required:** move this into Task 6 itself (not 6b). In `hatchFit()`:
- When `openName == "Rebirth"`, `TutorialExtra == 3` and `TutorialUI.Enabled` and `Guide.Visible`:
  - `topClear` = the bottom of the Guide's visible text (`Pips` / `Sub`, the largest `AbsolutePosition.Y + AbsoluteSize.Y`), converted to MainMenu space: add `GuiService:GetGuiInset().Y` when TutorialUI ignores the inset and MainMenu does not; subtract MainMenu's own top. Then add 6.
- Then **shift first, shrink only the rest**:
  - `avail = gs.Y - topClear - 6`;
  - if `h > avail`: `s = avail / 470`, and recompute w and h;
  - `cy = math.max(cy, topClear + h / 2)`.
- Expected:
  - Studio: no shrink, the window moves down about 28 px;
  - 1050x620: s ≈ 1.03 (text 16.4 px);
  - 844x390: s ≈ 0.67 (10.7 pt).
  - Write the measured values in the ledger.
- The `tutorial` check measures `Guide` in screen space (not `Card`) at native, at 1.0982 and at 0.7106, after the 0.32 s open tween. It must pass first time.
- If the owner would rather keep the full-size window, the alternative is a TutorialClient change (line 270: the guide slides away in step 11 too). That is out of scope for this plan, so note it as an owner's call; don't build it.

### 4. The three pages must honour the Studio switches `HatchTestPulse` and `HatchTestHover` (4.6, 5.6, 6.6)

Containment's pulse and hover passes set these attributes on `testRoot`. StreakClient (884-899), ShopClient (1074) and StarterPackClient (583-658) each wire them up themselves. The plan's hook lists don't, so:
- The pulse pass samples a random phase of the live breathing, never the 1.04 / 1.03 peak.
- The hover pass leaves every gloss button at rest.
- The `tutorial` check "arrow left ≥ REBIRTH face right + 8 at HatchTestPulse 1.04" tests nothing.

**Required (Studio only):**
- `page:GetAttributeChangedSignal("HatchTestHover")` calls `H.setTestHover(v == true)` on all 3 pages.
- Rebirth and Index pass `fixed = page:GetAttribute("HatchTestPulse")` into `btn.pulse(t, fixed)` inside their RenderStepped while the button breathes.
- Add both to the 4.6 / 5.6 / 6.6 hook lists.

### 5. One REBIRTH button width (6.1 Buttons, 6.4)

The plan gives REBIRTH two widths: 476 (not ready, next to SKIP) and 500 (ready / MAX). `H.glossButton` sizes Side, Face, TopHL, Gloss, Label and Flash once at build and has no resize. A builder would have to stretch the holder (face off-centre, containment fails) or improvise a second button.

**Required:**
- Keep **476 x 60 in every state** and move only the holder: centre x **492** when not ready, **370** when ready or MAX. The `states` test expectations stay the same.
- At 1.04 the ready button spans 122.5..617.5, so the TutorialArrow at 640 clears it by 22.
- Update the 6.1 rect, the 6.4 table and the arrow comment.

---

## SHOULD changes

### Correctness and robustness
1. **6.7 contract table.** Also list:
   - `refresh`: the HUD's last line 709 calls it;
   - `ownedPets`: `canRebirth` uses it;
   - the requires the HUD uses: `B`, `RS`, `TweenService`, `RunService`, `RebirthConfig`.

   The PAGE region must keep these names. A rename breaks the badge or banner, or errors at load.
2. **Rebirth token loop (6.6).** The loop is `if dirty or os.clock() < confirmUntil + 0.6 then refresh() end`, so the 2.5 s confirm still times out with no Money change. The current text says both "if dirty" and "once per tick".
3. **`nowNext` MAX** shows "MAX REBIRTH" plus a gold "20" with **no chevron**, but `set(now, nxt)` always draws the chevron when `nxt` is set. Add `opts.arrow = false`, and add it to R6.
4. **Celebrate rays (6.1).** Centre-anchor `Rays` (AnchorPoint 0.5 at (86, 124)) so 120 -> 140 grows around the coin. At 140 its top is y 54, under the band teeth (bottom about 62) for 0.9 s. Cap the burst at **132**: top 58, a faint edge.
5. **Inspect stat rows.** L (8..108) and V (104..198) boxes overlap by 4 px. Make L `(8, 4, 92, 16)`; "HATCHED" is then 82 %.
6. **Index claim.** I couldn't verify IndexServer's return (Play was running), and today's client reads only `ok`.
   - Map the refusal as `{tostring(msg or ""):upper(), "TRY AGAIN"}` so a nil message can't error.
   - Add a `busy` flag so a fast double press can't show a red refusal after a successful claim.
7. **Settings respawn check.** Settings moves from a MainMenu script into PlayerScripts. Add a `respawn` section to `settings_client` (Humanoid.Health = 0, then after respawn exactly 1 `SettingsPage` with `HatchCanvas`).

### Tests
8. **Rebirth `refusal` setup.** With Rebirths 1 and no Water pet, the server may refuse for the pet first ("NEED A PET!"). Give a qualifying pet on the server first, so money is the only thing missing. Or accept either mapped word and assert which one.
9. **Big-PC scale.** No containment run checks big-PC scales: 1.3732 and 1.5371 never run. Add forced runs:
   - REB1 / SET1 at `HatchTestScale = 1.37`;
   - IDX1 at **1.45**, the largest that fits 695.

   Skip `onTop` / `hud` in these runs, as the Shop ledger ruled.
10. **Check Gift and Shop early.** Run the Gift and Shop snapshots plus G1 / S1 right after **Task 3**. `H.arrow` (used by the Shop's treadmill now > next) and `pageCap` change there, so a helper regression would show before 3 windows are built on top.
11. **`hatch_shop_snapshot`** waits for prices to settle: 2 dumps 1 s apart must be identical, as the gift snapshot does. Live prices replace the fallbacks about 0.3-1 s after the first open.
12. **`claimall`** also asserts `Potion_Money` / `Potion_Hatch` +2.
13. **Task 1 count.** It is 7 identical sources (MenuController, BrickUI, Hatch, IndexClient, RebirthClient, plus 2 legacy copies), not 6.

### Hard rules and process
14. **TestFreshSave and switches.**
   - Task 0: if TestFreshSave reads false (the fix-round builder resets it), set it true and read it back. Don't stop.
   - Set it **false and read it back at the end of every builder run and on any abort**, not only "after the last Play of the day".
   - Clear and read back `TestSettingsLegacy`, `TestIndexLegacy`, `TestRebirthLegacy` and `HatchBand` at the end of each run.
15. **Split the build into 3 runs**, one Opus builder each, sharing the ledger:
   - (A) Tasks 0-4: evidence, backups, tests, helpers, Settings;
   - (B) Task 5: Index;
   - (C) Tasks 6-9: Rebirth, cross-checks, wrap-up.

   **Why:** each of Index and Rebirth is a Shop-sized rewrite with its own test suite. One run risks running out of context mid-window. A Haiku visual review after each run catches a repeated mistake before the next window copies it, which is how Gift's lessons reached the Shop. `PAGE_SKIN` is flipped per window (D1), so every run ends in a saveable state.
16. **More colour on the dark cards** (Shop visual-review lesson, owner's "basic").
   - Rebirth reward cards: tint the face gradient top with 15 % of the tile colour, and use Glow 0.4.
   - Index known cards: tint 15 % with `area.colors[1]`.
   - The mockups read calm next to today's vivid tiles (`compare_rebirth.png`).

---

## Owner's calls: defaults

| # | Default | Review |
|---|---|---|
| 1 | Big on PC, as today | Keep it. It matches the owner's Shop rule. |
| 2 | Settings band steel-lilac + gear | Keep it. The band top (196, 192, 236) is light, so the visual reviewer must zoom on the white gear and title. Fallback: darken the first band stop to (172, 166, 226). |
| 3 | MUSIC ON lime | Keep it. Note that TIME "DAY" = gold reuses the Robux-buy colour. It's harmless in Settings, but mention it to the owner. |
| 4 | SKIP gold | Keep it. |
| 5 | Index names only in the inspect panel | **Flag to the owner.** It is the one content change against "just the layout how it looked". It is forced by min text 16 in a 67 px card. Show `compare_index.png` and offer the 2-row alternative. |
| 6 | Legacy copies 7 days | Keep it. |
| (new) | Step-11 window clearance (MUST 3) | Default: top-anchored fit. Alternative: the guide slides away (TutorialClient). |

## What's good
- The D7 frozen HUD region with an exact diff expectation, and the legacy path that returns **before** the HUD, so the banner and arrows exist exactly once.
- D8 / D9: no forever loops, and Money only marks the page dirty. These remove 3 always-on loops from RebirthClient, and `IndexClient` stops refreshing on hatches while closed.
- D11: `TestSkip` refuses without a dry run, receipts go through `TestReceipt`, and the only real presses are free.
- The Settings fallback race is thought through: the guard, the 10 s timeout, and the destroy if MenuController wins.
- Every number re-derives, and the gutters are exact.
