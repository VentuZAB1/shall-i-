# Rebirth v6 + Tutorial Rebirth Step + 7-Day Login Streak Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Rebirth 1 reachable and celebrated (cheaper ladder, REBIRTH READY banner, tutorial step 11) and give
players a daily reason to return (a 7-day login streak inside the Gift window).

**Architecture:**
- Everything lives in the owner's open Roblox Studio (SLINGSHOT) and is edited through the Studio MCP.
- New pure logic goes into ReplicatedStorage config modules (RebirthConfig, the new StreakConfig), so it can be
  unit-tested in Edit mode. Server scripts own every reward. Client scripts only draw state that the server publishes
  as player attributes.
- The streak UI is a second tab inside the existing Gift window page (`Body.GiftPage`), next to the Playtime grid.

**Tech Stack:** Luau, Roblox Studio MCP (`execute_luau`, `script_read`, `multi_edit`, `start_stop_play`,
`screen_capture`, `get_console_output`), BrickUI (Check-UI style), the Analytics module.

**Spec:** `Desktop/SLINGSHOT Creatures/docs/specs/2026-10-21-rebirth-tutorial-streak-design.md` (owner-approved
2026-10-21, including: every Day 7 gives a secret pet, a missed day fully resets).

## Global Constraints

- **Studio:**
  - `studio_id = 0663e976-4faf-4dca-bf0c-91120a8d1353`. If it fails, re-check with `list_roblox_studios`.
  - Never use the Guard an Egg Studio (`08ad5583-...`).
- **Play tests:**
  - **Before every Play test:** `workspace:GetAttribute("TestFreshSave") == true`. Set it true from Edit if needed and put it back to false when the task's tests are done.
  - The owner may play inside our Play sessions: freeze nothing of theirs, and read state rather than drive input.
- **The owner's Studio:**
  - Never type into the owner's command bar and never click Studio dialogs. Use `execute_luau` for DataModel work.
  - Never publish. The owner Saves + Publishes.
- **Backups:** before the first edit of any script, copy it to `ServerStorage._Backup_RebirthStreak.Before.<ScriptName>`. Clone, keep the Source, set `Disabled`/`Enabled = false` on the copy, and strip CollectionService tags.
- **Edit-mode requires are cached:** to test a ModuleScript you just edited, `require(module:Clone())`.
- **Deferred signals:**
  - Workspace.SignalBehavior is Deferred. In tests, never set two related attributes in the same frame (`task.wait()` between them).
  - Your own attribute write comes back later through Changed signals.
- **Code and copy style:**
  - Code style: tabs, dated comments `-- (2026-10-21) ...`, and the comment density of the surrounding file.
  - The file header comment says what changed.
- **UI:** use the `check-ui-clean-roblox` skill and the BrickUI helpers (`B.brick`, `B.text`, `B.image`, `B.damier`, `B.innerHighlight`, `B.deviceScale`, `B.SUNBURST`, `B.GOTHAM`).
  - Font: GothamBlack with a black UIStroke. Icons use `ScaleType.Fit`.
  - Animations scale from the centre (AnchorPoint 0.5,0.5 + UIScale).
- **No git:** Studio is the source of truth and the git root is the user's home folder.
  - Progress ledger: `docs/plans/2026-10-21-rebirth-tutorial-streak.progress.md`, one line per finished task.
  - Before the final review, each changed script is exported to `docs/plans/review-2026-10-21/<Name>.lua`.
- **Rebirth ladder (exact, `RebirthConfig.LADDER`):** cost, then pet area and kg.

  | R | Cost | Pet requirement |
  |---|---|---|
  | 1 | 25,000 | none |
  | 2 | 1,200,000 | area 2, kg 1 |
  | 3 | 4,000,000 | area 3, kg 1 |
  | 4 | 18,000,000 | area 3, kg 100 |
  | 5 | 90,000,000 | area 4, kg 1 |
  | 6 | 550,000,000 | area 4, kg 100 |
  | 7 | 1,300,000,000 | area 4, kg 1000 |
  | 8 | 3,000,000,000 | area 5, kg 1 |
  | 9 | 15,000,000,000 | area 5, kg 100 |
  | 10 | 38,000,000,000 | area 5, kg 1000 |
  | 11 | 120,000,000,000 | area 5, kg 10000 |
  | 12 | 400,000,000,000 | area 6, kg 1 |
  | 13 | 1,500,000,000,000 | area 6, kg 100 |
  | 14 | 2,600,000,000,000 | area 6, kg 1000 |
  | 15 | 4,000,000,000,000 | area 6, kg 5000 |
  | 16 | 6,500,000,000,000 | area 6, kg 10000 |
  | 17 | 9,500,000,000,000 | area 6, kg 25000 |
  | 18 | 13,000,000,000,000 | area 6, kg 50000 |
  | 19 | 19,000,000,000,000 | area 6, kg 100000 |
  | 20 | 32,000,000,000,000 | area 6, kg 1000000 |

- **Streak rewards (exact, `StreakConfig.DAYS`):**

  | Day | Parts |
  |---|---|
  | 1 | cash 15 min; Money potion ×1 |
  | 2 | Hatch potion ×1; Speed potion ×1; speed pct 0.20 |
  | 3 | cash 30 min; Money potion ×2 |
  | 4 | egg (furthest area's egg at `EGG_KG[area]`) |
  | 5 | Money, Hatch and Speed potions ×3 each |
  | 6 | cash 60 min; speed pct 0.50 |
  | 7 | pet (furthest area's SECRET at `SECRET_KG[area]`); Money, Hatch and Speed potions ×5 each; cash 120 min |

  - `EGG_KG = {30000, 60000, 100000, 200000, 300000, 500000}`
  - `SECRET_KG = {15000, 30000, 50000, 100000, 150000, 250000}`
- **Streak days:** UTC day number `math.floor(os.time() / 86400)`. In Studio only, `+ workspace:GetAttribute("StreakDayOffset")` (a number). Live servers ignore the offset.

## Review Focus

1. **UTC midnight passes while the player is in the game.** The server must flip `StreakClaimable` within 30 s without a rejoin, and the DAILY tab must update live. Test: Task 4 "rollover" (offset change → attributes within 1 s), plus the 30 s poll.
2. **Inventory full when the pet (Day 7) or the egg (Day 4) is given.** The day must not be used up, nothing else may be given, and the message must be clear. Test: Task 4 `failNext` for "full" (pet) and "full" (egg).
3. **A stage-3 tutorial player rebirths without the button flow** (Robux Skip Rebirth, or Rebirths changed by the admin): the tutorial must still finish with its reward exactly once. Test: Task 3 "rebirths attribute bump".
4. **R0 players open the Rebirth page or see the badge now that R1 has no pet requirement** (nil `req`). There must be no Luau error and the money card must be centred. Test: Task 1 client check + console scan.
5. **Two quick UpgradeBought events, or a deferred re-fire, in tutorial stage 2.** The stage must go 2 → 3 once and never skip to 0 with a reward while R0. Test: Task 3 "double UpgradeBought".

---

### Task 1: Rebirth ladder v6

**Files:**
- Modify: `ReplicatedStorage.RebirthConfig`
  - the header comment;
  - `LADDER` (l.26-47);
  - `requirement` (l.61-65);
  - `petMeets` (l.68-75);
  - `requirementText` (l.78-82).
- Modify: `StarterPlayerScripts.RebirthClient`
  - `refresh` (l.272-346): the pet card when there is no requirement;
  - `canRebirth` (l.446-452): no change needed once petMeets(nil) is true. Re-check it.
- Modify: `ServerScriptService.RebirthServer`: the Studio-only `RebirthDebug` hook (Interfaces).
- Modify: `Desktop/SLINGSHOT Creatures/economy/v6_rebirth.py`: change `V6[1]` to `1_200_000`.
- Create (test): `ServerStorage.RebirthV6Tests` (ModuleScript), with `pure() -> (pass:number, fail:number, lines:{string})` and `live(player) -> same`.

**Interfaces:**
- Produces:
  - `RebirthConfig.requirement(rebirths) -> {area, kg} | nil`. It returns nil when the next step has no pet requirement, as well as at the cap.
  - `RebirthConfig.petMeets(pets, nil) -> true`.
  - `RebirthConfig.requirementText(nil) -> ""`.
  - `RebirthConfig.cost(0) == 25000`.
  - Task 3 and RebirthClient rely on these.
  - `ServerStorage.RebirthDebug` (Studio only, in RebirthServer after `rebirth`, l.61-77): BindableFunction
    `OnInvoke(player) -> ok, result`, the same `rebirth(player)` the remote runs.

- [ ] **Step 1: Back up** RebirthConfig and RebirthClient (Global Constraints recipe).
- [ ] **Step 2: Write `RebirthV6Tests.pure()`.** It requires `RebirthConfig:Clone()` and checks:
  - `cost(r)` for r = 0..19 equals the ladder table above;
  - `cost(20) == nil`;
  - `requirement(0) == nil`;
  - `requirement(1)` is `{area = 2, kg = 1}`;
  - `requirement(19)` is `{area = 6, kg = 1000000}`;
  - `petMeets({}, nil) == true`;
  - `petMeets({}, {area = 2, kg = 1}) == false`;
  - `requirementText(nil) == ""`;
  - `requirementText({area = 3, kg = 100}) == "Thunder pet 100+ KG"`.
- [ ] **Step 3: Run it in Edit and confirm it fails.**
  - Run: `execute_luau` (Edit): `local t = require(game.ServerStorage.RebirthV6Tests:Clone()) return t.pure()`.
  - Expected: failures on `cost(0)` (40000) and `requirement(0)` (not nil).
- [ ] **Step 4: Implement the RebirthConfig changes.**
  - `LADDER[1] = {cost = 25000}`, with no `area` or `kg` fields.
  - `requirement` returns nil when `step.area == nil`.
  - `petMeets(pets, nil)` returns true.
  - `requirementText(nil)` returns "".
  - Update the header comment: v6 2026-10-21, the R1 money-only reason (11% reached R1), and the new pacing target "R10 ~5 h, R20 ~95 h".
- [ ] **Step 5: Re-run `pure()`.** Expected: all pass, 0 fail.
- [ ] **Step 6: Change RebirthClient `refresh`.**
  - When `req == nil`: `petCard.Visible = false`, `moneyCard.Position = UDim2.fromScale(0.5, 0.725)`.
  - Otherwise, the pet card shows and the money card goes back to x 0.755.
  - `ready = have >= cost and (req == nil or best ~= nil)`.
  - Never index `IndexConfig.AREAS[req.area]` when `req` is nil.
- [ ] **Step 7: Write `RebirthV6Tests.live(player)`.** It runs on the Server datamodel during Play, on the TestFreshSave player.
  1. Setup: set `Rebirths 0`, `PetInventory "[]"`, `BaseData '{"eggs":[],"pets":[]}'`, then `task.wait()`.
  2. Set `Money 25000`, then `task.wait()`.
  3. `ServerStorage.RebirthDebug:Invoke(player)`.
     - Expect `true, 1`, then `Money == 0`, then `Rebirths == 1`.
  4. Then `Money 1200000` with no Water pet.
     - Expect `false, "Need a Water pet"`.
  5. Restore `Rebirths 0` and `Money 0`.
- [ ] **Step 8: Run the live test in Play.**
  - Check TestFreshSave == true, then `start_stop_play` (start).
  - `execute_luau` (Server): `return require(game.ServerStorage.RebirthV6Tests).live(game.Players:GetPlayers()[1])`.
  - Expected: all pass.
- [ ] **Step 9: Client check for Review Focus #4.**
  - In the same Play session, with Rebirths 0, Client `execute_luau`: fire `PlayerGui.MainMenu.OpenPage:Fire("Rebirth")` and wait 1 s. Read `RebirthPage.NeedPet.Visible`, then `NeedMoney.Position`, then `RebirthButton` label text.
  - Then `get_console_output` and search for "RebirthClient".
  - Expected:
    - `NeedPet.Visible == false`;
    - `NeedMoney` at x 0.5;
    - no RebirthClient errors.
  - Stop Play.
- [ ] **Step 10: Re-run the simulation.** Run: `cd "Desktop/SLINGSHOT Creatures/economy" && python v6_rebirth.py 20`. Expected: the v6 total at R10 ≤ 5.3 h, and the v6 R2 run ≤ the v5 R2 run.
- [ ] **Step 11: Ledger line:** `Task 1: complete (RebirthV6Tests pure+live pass, sim R10 <x> h)`.

---

### Task 2: REBIRTH READY banner + rebirth tutorial arrows (RebirthClient)

**Files:**
- Modify: `StarterPlayerScripts.RebirthClient` (the HUD section, after l.437) and `refresh` (`Confirming` attribute).
- Test: `ServerStorage.RebirthV6Tests.client()`. Its source is run as a string in the Client datamodel: the client can't require ServerStorage, so the test copies `tests.CLIENT_SRC` into `execute_luau`.

**Interfaces:**
- Consumes: Task 1 `requirement/petMeets`. `canRebirth()` already exists (l.446).
- Produces:
  - **`RebirthPage` attribute `Confirming`** (bool): true while the first press waits for "TAP AGAIN!". Task 3 reads it.
  - **ScreenGui `RebirthReadyUI`** (DisplayOrder 6, ResetOnSpawn false, IgnoreGuiInset true) with a TextButton `Banner`. Children: `Title` and `Sub`.
  - **ScreenGui `RebirthTutorialUI`** (DisplayOrder 6), ImageLabel `TileArrow`.
  - **`RebirthPage.TutorialArrow`**, an ImageLabel.
  - **`RebirthPage.TestPress`** (Studio only): a BindableEvent that runs the REBIRTH button's own handler. Move the
    `btn.Activated` body into `local function press()` and connect both to it.
  - Tutorial stage 3 = player attribute `TutorialExtra == 3` (Task 3 sets it).

- [ ] **Step 1: Write `client()` checks.** Before each check, run in Play on the client:
  - `Banner_once`:
    - Setup: `TutorialDone true`, `TutorialExtra 0`, Rebirths 0, then Money 30000 (set on the server, one frame apart).
    - Expect `RebirthReadyUI.Banner.Visible` true within 1 s, with `Title.Text == "REBIRTH READY!"` and `Sub.Text == "+1 PET SLOT  •  x1.25 MONEY & SPEED"`.
    - After 5 s: not visible.
    - Set Money 0 then 30000 again: not shown again.
  - `Banner_waits_for_window`:
    - Setup: use a fresh level (set Rebirths 1, then PetInventory `'[{"id":"t_water","name":"Kappa","kg":5}]'`, then
      Money 1200000). Open the Shop window (OpenPage "Shop") before the Money write.
    - Expect not visible while the window is open, then visible ≤ 1 s after CloseWindow. Restore PetInventory "[]".
  - `Banner_never_in_tutorial`:
    - Setup: `TutorialExtra 3`, R0, Money 30000.
    - Expect the banner hidden. Expect `TileArrow.Visible` true while the window is closed.
    - Open the Rebirth page: `TileArrow` hidden and `RebirthPage.TutorialArrow.Visible` true.
- [ ] **Step 2: Run the checks (Play) and confirm they fail.** Expected: "RebirthReadyUI not found".
- [ ] **Step 3: Implement the banner** in RebirthClient's HUD section.
  - Look: Check-UI floating text, built like TutorialClient's finish text.
    - `Title`: GothamBlack, UIGradient (160,0,255) → (96,0,200) at Rotation 90, UIStroke black 4.
    - `Sub`: white, stroke 2.4.
    - Centred at `UDim2.fromScale(0.5, 0.22)`, offset size 620×120, one `WindowScale` UIScale = `B.deviceScale()`.
  - Motion:
    - Pop-in on an inner UIScale (0.3 → 1, Back, 0.45 s).
    - Pulse `1 + 0.04*sin`.
    - It stays 4 s, then scales to 0 (Back In, 0.3 s).
  - SFX: `SFX.play("Boost")`.
  - Sub text: `("+1 PET SLOT  •  x%g MONEY & SPEED"):format(RebirthConfig.multiplier(r + 1))`.
  - Tapping the banner fires `MainMenu.OpenPage:Fire("Rebirth")` and hides it.
  - Rule, checked every 0.5 s by the existing badge poll loop. Show when all of these hold:
    - `canRebirth()`;
    - `shownFor ~= r`;
    - `TutorialDone == true`;
    - `(TutorialExtra or 0) == 0`;
    - `IntroPlaying ~= true`;
    - `MainMenu.Window.Visible == false`.

    Then set `shownFor = r`. `shownFor` is a local, reset only by a new session.
- [ ] **Step 4: Implement the `Confirming` attribute and `TestPress`.** In `refresh`:
  `page:SetAttribute("Confirming", confirming and ready)`. When maxed: false. `TestPress` per Interfaces.
- [ ] **Step 5: Implement the tutorial arrows.** Both use the tutorial's down-arrow image `rbxassetid://93838363576146` and are updated on RenderStepped.
  - **`TileArrow`:**
    - Rotation 90 (points left). Size = 0.75 × the Rebirth tile's `Face.AbsoluteSize.Y` (square).
    - Placed just right of the tile: `AbsolutePosition.X + AbsoluteSize.X + 6 + bob*14` px, vertical centre of the tile, `bob = |sin(t*4)|`.
    - Visible when all of these hold:
      - `TutorialExtra == 3`;
      - `canRebirth()`;
      - the window is not visible;
      - `IntroPlaying ~= true`.
  - **`TutorialArrow`:**
    - On the page: `AnchorPoint (0.5, 1)`, Size `UDim2.fromScale(0.07, 0.16)` + UIAspectRatioConstraint, X = the button holder's centre.
    - Y = top of `btnHolder` − bob × 0.03. ZIndex 10.
    - Visible when `TutorialExtra == 3 and ready and page.Visible`.
- [ ] **Step 6: Re-run the client checks.** Expected: all pass. Take one `screen_capture` of the banner and one of the TileArrow for the ledger.
- [ ] **Step 7: Ledger line.** Stop Play. Write `Task 2: complete (...)`.

---

### Task 3: Tutorial step 11 = first rebirth

**Files:**
- Modify: `ServerScriptService.TutorialServer`
  - the l.33-87 block: stage 3, finish on rebirth, resume rule, debug hook;
  - header comments.
- Modify: `StarterPlayerScripts.TutorialClient`
  - TOTAL l.43;
  - `extraStage` l.424-427;
  - `extraStep` l.442-476;
  - `finish` l.602-640;
  - header l.10-13.
- Modify: `ServerScriptService.PlayerData`: only the FIELDS comment on `TutorialExtra` (l.46), which now lists 3 = rebirth next.
- Test: `ServerStorage.TutorialV11Tests` (ModuleScript) `live(player)`.

**Interfaces:**
- Consumes:
  - Task 1 `RebirthConfig.cost(0) == 25000`.
  - Task 2 `RebirthPage:GetAttribute("Confirming")`, `TileArrow` and `TutorialArrow`.
  - `ServerStorage.UpgradeBought` (existing BindableEvent) and `ServerStorage.GivePotion`.
- Produces:
  - **TutorialExtra stages:** 1 run → 2 upgrade → 3 rebirth → 0 done.
  - **`ServerStorage.TutorialDebug`** (Studio only) BindableFunction `OnInvoke(op, player)`. Op `"check"` runs the DataLoaded resume check now and returns `TutorialExtra`.

**Server rules (TutorialServer)**
- `afterUpgrade(player)` replaces `complete`. Only in stage 2:
  - Rebirths ≥ 1 → `done(player)`;
  - otherwise set stage 3.
  - UpgradeBought and stuckCheck both call it.
- `done(player)`: only in stage 2 or 3. Set TutorialExtra 0 FIRST, then `GivePotion(player, "Money", 1)` in a pcall.
- Rebirths changed: if DataLoaded, TutorialExtra == 3 and Rebirths ≥ 1 → `done`.
- Resume check, on DataLoaded and in the debug op:
  - If `TutorialDone == true`, TutorialExtra == 0, Rebirths == 0 and `OnboardStep == 12` → stage 3.
  - If TutorialExtra == 3 and Rebirths ≥ 1 → `done`.
  - Players who already got the step-10 potion before today get one more at their rebirth (accepted: ≤ 1 potion, small group).
  - The spec puts this rule in PlayerData's load. It lives here instead, with the same effect on DataLoaded and
    testable through `TutorialDebug`: every save since 10-15 already stores `TutorialExtra` (as 0), so PlayerData's
    `value == nil` branch never runs for them.

**Client copy (TutorialClient step 11, `n = 11`)**

| State | Title | Sub | World target |
|---|---|---|---|
| Money < `cost(r)` and no pets | "Hatch a PET to earn $!" | "Grab EGGS on the runway" | PAD while in the hub |
| Money < `cost(r)` | `"Earn $" .. Format(cost) .. " to REBIRTH!"` | `("$%s / $%s - grab more EGGS!")` | PAD while in the hub |
| Ready, page closed | "REBIRTH is READY!" | TOUCH "Tap the REBIRTH button on the left", else "Click the REBIRTH button on the left" | none |
| Page open, not confirming | "Press REBIRTH!" | "Money + Speed reset - you keep your PETS!" | none |
| Page open, `Confirming` | "Tap AGAIN to confirm!" | "Money + Speed reset - you keep your PETS!" | none |

- "Page open" = `MainMenu.Window.Visible and Body.RebirthPage.Visible`.
- `extraStage()` accepts 1, 2 and 3.
- `rewarded = true` when the stage disappears after 2 or 3.
- `finish()`: when the last stage was 3, `task.delay(1.2, CloseWindow:Fire())`, so the finish plays over the world. The finish line stays "Next: reach the WATER area!".
- TOTAL = 11, so 11 pips.

- [ ] **Step 1: Back up** TutorialServer, TutorialClient and PlayerData.
- [ ] **Step 2: Write `TutorialV11Tests.live(player)`.** Each case sets up attributes one frame apart and restores them after.
  1. `stage2_to_3`:
     - Setup: Rebirths 0, TutorialDone true, TutorialExtra 2.
     - `UpgradeBought:Fire(player)`, wait 0.2 s.
     - Expect TutorialExtra 3, and the `Potion_Money` count unchanged.
  2. `double_upgrade`:
     - Setup: stage 2, R0.
     - Fire UpgradeBought twice in the same frame.
     - Expect stage 3 and potions unchanged (Review Focus #5).
  3. `stage2_r1_done`:
     - Setup: Rebirths 1, stage 2.
     - Fire UpgradeBought.
     - Expect stage 0 and `Potion_Money` +1.
  4. `rebirth_finishes`:
     - Setup: stage 3, R0, wait.
     - Set Rebirths 1 (a direct attribute bump, which covers Robux Skip).
     - Expect stage 0 and `Potion_Money` +1 exactly once: re-set Rebirths 2, and the potions stay the same (Review Focus #3).
  5. `stuck_to_3`:
     - Setup: stage 2, R0, SlingLevel 25 (nothing buyable), then a `TutorialExtra` re-set to fire stuckCheck.
     - Expect stage 3.
  6. `resume`:
     - Setup: TutorialExtra 0, Rebirths 0, OnboardStep 12, TutorialDone true.
     - `TutorialDebug:Invoke("check", player)` returns 3.
     - The same setup with OnboardStep 13 returns 0.
- [ ] **Step 3: Run it (Play, Server) and confirm it fails.**
  - Expected: `stage2_to_3` fails (stage becomes 0).
  - "TutorialDebug missing" for `resume`.
- [ ] **Step 4: Implement the TutorialServer rules** above. `TutorialDebug` exists only when `RunService:IsStudio()`.
- [ ] **Step 5: Re-run the live tests.** Expected: 6/6 pass.
- [ ] **Step 6: Implement the TutorialClient step 11** per the copy table. Update the header comment: step 11, 2026-10-21.
- [ ] **Step 7: Client checks** (Play, Client `execute_luau`). Read `PlayerGui.TutorialUI.Guide.Pop.Title.Text`, stripping rich text.
  1. Setup: stage 3, R0, Money 1000. Expect "Earn $25K to REBIRTH!" and Sub "$1K / $25K - grab more EGGS!". There are 11 pips.
  2. Money 30000 → "REBIRTH is READY!", and `RebirthTutorialUI.TileArrow.Visible`.
  3. `OpenPage:Fire("Rebirth")` → "Press REBIRTH!".
  4. `RebirthPage.TestPress:Fire()` once. Expect "Tap AGAIN to confirm!".
  5. `TestPress:Fire()` again: the real rebirth through the remote, Rebirths becomes 1. Expect `TutorialUI.Finish`
     visible with "TUTORIAL COMPLETE!", and the Reward row visible. After 2 s, `MainMenu.Window.Visible == false`.
  - Take a `screen_capture` of each state.
- [ ] **Step 8: Full fresh run.**
  - Set `TestTutorial = true` and TestFreshSave true, then Play.
  - Read the Guide title every 2 s while the owner (or a scripted `MoveTo`) is NOT driving. Only check that step 1 shows "Walk to the SLINGSHOT!" and the pips row has 11 children.
  - Stop and set TestTutorial false.
- [ ] **Step 9: Ledger line:** `Task 3: complete (...)`.

---

### Task 4: Streak core (config, server, saved fields, rewards, analytics)

**Files:**
- Create: `ReplicatedStorage.StreakConfig` (ModuleScript).
- Create: `ServerScriptService.StreakServer` (Script).
- Modify: `ServerScriptService.BaseHatchery`: add `ServerStorage.GiveEgg` next to GivePet (l.928-947).
- Modify: `ServerScriptService.PlayerData`: add FIELDS `StreakDay = 0` and `StreakLast = 0`, with a comment.
- Modify: `ServerScriptService.Analytics`:
  - `INCOME_TX.Streak = TX.TimedReward.Name`;
  - new `A.streak(player, day, cycleStart)`;
  - header FUNNELS list +"Daily Streak".
- Test: `ServerStorage.StreakTests` (ModuleScript) `pure()` and `live(player)`.

**Interfaces:**
- **StreakConfig produces** (all pure):
  - `S.DAYS[d]`: a list of parts. A part is `{kind = "cash", minutes}`, `{kind = "speed", pct}`, `{kind = "potion", potion = "Money"|"Hatch"|"Speed", count}`, `{kind = "egg"}` or `{kind = "pet"}`.
  - `S.EGG_KG`, `S.SECRET_KG` (Global Constraints).
  - `S.EGG_ICONS`: a copy of PetsEggsUI's EGG_ICONS map, l.36-43.
  - `S.today(now: number, offset: number?) -> number`.
  - `S.secondsToNext(now: number) -> number`: `86400 - now % 86400`.
  - `S.view(day, last, today) -> {claimable: bool, next: 1..7, lost: bool, claimedThrough: 0..7}`. Algorithm below.
  - `S.furthestArea(foundNames: {[string]: any}, CreatureConfig) -> 1..6`: the highest `area` among discovered names, default 1.
  - `S.secretFor(area, CreatureConfig, models: Instance) -> string?`: the creature with `secret == true` in `area` whose model exists. If none, the next lower area.
  - `S.eggFor(area, IndexConfig) -> string`: `IndexConfig.AREAS[area].egg`.
- **StreakServer produces:**
  - RemoteFunction `ReplicatedStorage.Streak.Claim`, invoked with no arguments. It returns `(true, day)` or `(false, reason)`. Reasons: "Please wait", "Come back tomorrow!", "Pets full!", "Eggs full!", "Try again".
  - Player attributes it keeps current:
    - `StreakToday` (number);
    - `StreakClaimable` (bool);
    - `StreakNext` (1-7);
    - `StreakLost` (bool);
    - `StreakThrough` (0-7);
    - `StreakArea` (1-6);
    - `StreakPet` (string);
    - `StreakEgg` (string).
  - `ServerStorage.StreakDebug` (Studio only) BindableFunction `OnInvoke(op, ...)`:
    - `"set", player, day, last` writes `StreakDay`/`StreakLast` and re-publishes;
    - `"failNext", "pet"|"egg"` makes the next pet/egg give return `nil, "full"`;
    - `"publish", player`;
    - `"claim", player` runs the exact claim function the remote runs and returns its results.
- **BaseHatchery produces:** `ServerStorage.GiveEgg:Invoke(player, kind: string, kg: number) -> entry | (nil, "full")`. It checks DataLoaded, a known kind and `InventoryConfig.eggCount < MAX_EGGS`. It appends `Mutations.makeEntry(kg, nil)`, writes `EggInventory` and fires `ServerStorage.EggInventoryChanged`.
- **Analytics produces:** `A.streak(player, day: number, cycleStart: number)`, which calls `A.funnel(player, "Daily Streak", userId .. "-S" .. cycleStart, day, "Day " .. day)`.

**`S.view` algorithm** (exact):
```lua
if day < 1 or last < 1 then return {claimable = true, next = 1, lost = false, claimedThrough = 0} end
if last >= today then return {claimable = false, next = day % 7 + 1, lost = false, claimedThrough = day} end
if last == today - 1 then
	local nxt = day % 7 + 1
	return {claimable = true, next = nxt, lost = false, claimedThrough = nxt - 1}
end
return {claimable = true, next = 1, lost = true, claimedThrough = 0}
```

**StreakServer rules**
- `publish(player)` runs on:
  - DataLoaded;
  - IndexData change;
  - after a claim;
  - every 30 s for all players;
  - `workspace` `StreakDayOffset` change (Studio).
- Claim order: busy lock and DataLoaded check → `view` claimable? → give parts.
  - Pet and egg go FIRST, because they're the only refusable parts. A refusal returns its reason and changes nothing.
  - Then potions via GivePotion. A failed potion is warned and the claim continues.
  - Then cash: `PlaytimeConfig.amount({kind="cash", minutes=m}, IncomePerSec, Speed)` → Money + `Analytics.moneyIn(player, amount, "Streak")`.
  - Then speed: `PlaytimeConfig.amount({kind="speed", pct=p}, ...)` → Speed.
- After the gives: set `StreakDay = next`, then `StreakLast = today`, then call `Analytics.streak(player, next, today - next + 1)`, then `publish`.
- The busy lock is cleared on PlayerRemoving.

- [ ] **Step 1: Back up** BaseHatchery, PlayerData and Analytics.
- [ ] **Step 2: Write `StreakTests.pure()`.** It requires a Clone of StreakConfig and checks:
  - `view(0,0,100)` → `{true,1,false,0}`;
  - `view(3,100,100)` → `{false,4,false,3}`;
  - `view(3,99,100)` → `{true,4,false,3}`;
  - `view(7,99,100)` → `{true,1,false,0}`;
  - `view(7,100,100)` → `{false,1,false,7}`;
  - `view(4,97,100)` → `{true,1,true,0}`;
  - `view(2,101,100)` → claimable false;
  - `today(86400*5+10) == 5`;
  - `today(86400*5+10, 2) == 7`;
  - `secondsToNext(86400*5+10) == 86390`;
  - `furthestArea({}, CC) == 1`;
  - `furthestArea({ThunderRex = true, ForestStag = true}, CC) == 3`;
  - `secretFor(1, CC, models) == "ThornbladeMantis"`;
  - `secretFor(3, ...) == "ThunderRex"`;
  - `secretFor(6, ...) == "CosmicLeviathan"`;
  - `eggFor(6, IC) == "CelestialEgg"`;
  - `#DAYS == 7`;
  - DAYS[7] has 1 pet part, potion counts 5/5/5 and cash 120;
  - DAYS[4] is exactly `{ {kind="egg"} }`.
- [ ] **Step 3: Run `pure()` in Edit and confirm it fails.** Expected: "StreakConfig not found".
- [ ] **Step 4: Implement StreakConfig.** Its header comment covers the rules, the spec path and the owner decisions.
- [ ] **Step 5: Re-run `pure()`.** Expected: all pass.
- [ ] **Step 6: Implement GiveEgg (BaseHatchery), the PlayerData FIELDS, the Analytics additions and StreakServer.**
- [ ] **Step 7: Write `StreakTests.live(player)`.** It runs in Play on the Server, on the TestFreshSave player, with `StreakDayOffset` starting at 0. Restore the offset to 0 at the end.
  1. `day1`:
     - Expect `StreakClaimable` true and `StreakNext` 1.
     - `StreakDebug:Invoke("claim", player)` → `true, 1`.
     - `Potion_Money` +1; Money +≥ 9000; `StreakDay` 1; `StreakLast == StreakToday`.
  2. `same_day`: claim → `false, "Come back tomorrow!"`.
  3. `rollover`:
     - Set offset 1, wait ≤ 1 s.
     - Expect `StreakToday` +1 and claimable, next 2 (Review Focus #1).
  4. `day2`: claim → Hatch +1, Speed potion +1, Speed attribute increased.
  5. `egg_full`:
     - Offset 2, then claim → day 3.
     - Offset 3, `failNext "egg"`, then claim → `false, "Eggs full!"`, with StreakDay still 3 and potions/money unchanged (Review Focus #2).
     - Claim again → `true, 4`, and EggInventory[StreakEgg] gained one entry of `EGG_KG[StreakArea]`.
  6. `missed`:
     - Offset 5 (day +4 skipped).
     - Expect `StreakLost` true, next 1, through 0.
  7. `pet_full_day7`:
     - `set` day 6, last = today − 1.
     - `failNext "pet"`, then claim → `false, "Pets full!"`, and StreakDay is still 6.
     - Claim again → `true, 7`.
     - PetInventory contains `{name = StreakPet, kg = SECRET_KG[StreakArea]}`; each potion +5; Money +≥ 72000.
  8. `cycle`: offset +1 → next 1, lost false, through 0.
- [ ] **Step 8: Run `live` (Play, Server).** Expected: 8/8 pass. `get_console_output` shows no StreakServer warnings except the expected test ones.
- [ ] **Step 9: Analytics check.** Same session, with `AnalyticsDebug = true`. One claim prints `[Analytics] funnel Daily Streak 1 Day 1`. Stop Play and set AnalyticsDebug false.
- [ ] **Step 10: Ledger line:** `Task 4: complete (...)`.

---

### Task 5: Gift window tabs + DAILY page + auto-open (StreakClient)

**Files:**
- Create: `StarterPlayerScripts.StreakClient` (LocalScript).
- Modify: `StarterPlayerScripts.PlaytimeClient`.
  - Its content moves into a child frame `PlaytimeView` (Size `UDim2.fromScale(1, 0.87)`, Position `UDim2.fromScale(0.5, 0.565)`, transparent).
  - Refresh draws cells only while `page.Visible and view.Visible`.
  - Tile: `badge.Visible = ready or player:GetAttribute("StreakClaimable") == true`; the label says "Claim!" if either.
- Modify: `StarterGui.MainMenu.MenuController`: `LAYOUT.Gift = {1.95, 1.2}` (l.185).
- Test: `ServerStorage.StreakTests.CLIENT_SRC` (a string, run in the Client datamodel).

**Interfaces:**
- **Consumes:**
  - Task 4 attributes (`StreakClaimable`, `StreakNext`, `StreakThrough`, `StreakLost`, `StreakToday`, `StreakArea`, `StreakPet`, `StreakEgg`) and `RS.Streak.Claim`.
  - `StreakConfig.DAYS`, `EGG_KG`, `SECRET_KG`, `EGG_ICONS`, `secondsToNext`.
  - `PlaytimeConfig.amount` for live cash/speed numbers.
  - `MainMenu.OpenPage` / `CloseWindow`, `Window.Face.Title`, `Body.GiftPage`.
- **Produces:**
  - `GiftPage.Tabs` holds the TabDaily and TabPlaytime buttons. `GiftPage.DailyView` holds `Status` and `Card1..Card7`.
  - Each card has `State` (TextLabel: "CLAIM" / "CLAIMED" / "TOMORROW" / "DAY n") and `Claim` (the button Face).
  - `GiftPage` attribute `Tab` = "Daily" | "Playtime".
  - ScreenGui `StreakCelebrate` (DisplayOrder 45).

**Layout and look** (DailyView = the same rect as PlaytimeView; Tabs = Size (0.5, 0.1) at (0.5, 0.055))
- **Tabs:** two iconless Check-UI buttons, 0.48 wide each. Active = lime (180,255,25)→(105,225,0) with bevel (15,120,15); inactive = silver (216,222,228)→(148,160,176).
  - Text: "DAILY" / "PLAYTIME".
  - TabDaily shows a small "!" dot while `StreakClaimable` is true.
- **Status line** (y 0.05 of DailyView), in this order of precedence:
  - left: "Streak lost - back to Day 1!" (red, while `StreakLost` and claimable); "DAY n OF 7" otherwise;
  - right, one of:
    - "Today's reward is READY!" (lime) when claimable;
    - "Next reward in HH:MM:SS" (white) from `secondsToNext(GetServerTimeNow() + offset*86400)`. The offset only applies in Studio: read `workspace:GetAttribute("StreakDayOffset")`. The countdown itself just counts to the next UTC midnight;
    - "Week complete! New week tomorrow" when `StreakThrough == 7` and not claimable.
- **Grid:** row 1 = Day 1-4; row 2 = Day 5, Day 6, and Day 7 spanning 2 columns.
  - Cell width 0.235, gap 0.02, row height 0.4. Row tops at y 0.12 and 0.56 of DailyView.
- **Card:** `B.brick` with a gradient.
  - Colours (Rotation 90):
    - Days 1-3 cyan (0,210,255)→(0,120,255);
    - Day 4 purple (176,32,255)→(112,0,224);
    - Day 5 magenta (208,0,224)→(128,0,160);
    - Day 6 amber (255,170,0)→(224,96,0);
    - Day 7 the Check-UI rainbow sequence at Rotation 45.
  - Every card also gets `B.damier` and `B.innerHighlight`.
  - Content:
    - "DAY n" top (GothamBlack, stroke 2.6).
    - The icon centre:
      - cash `rbxassetid://131724750673548`;
      - speed `rbxassetid://80829076123513`;
      - potions `PotionConfig.byKey[k].icon`;
      - egg `S.EGG_ICONS[StreakEgg]`;
      - Day 7 `IndexConfig.PORTRAITS[StreakPet]` with `B.SUNBURST` behind it, turning 20°/s, and a red "SECRET!" ribbon label on the top-right corner.
    - Reward lines, with live numbers:
      - Day 1: "$X" + "+1 Money Potion".
      - Day 2: "+1 Hatch Potion", "+1 Speed Potion", "+X Speed".
      - Day 3: "$X" + "+2 Money Potions".
      - Day 4: "BIG EGG" + "<Egg Name> <KG> KG".
      - Day 5: "+3 of EVERY Potion".
      - Day 6: "$X" + "+X Speed".
      - Day 7: "SECRET PET!", "<display> <KG> KG", "+5 of EVERY Potion", "$X".
  - Bottom state:
    - `d <= StreakThrough` → silver "CLAIMED" + check icon `rbxassetid://78526516923039`, icon at 0.55 transparency;
    - `d == StreakNext` and claimable → a lime "CLAIM" button pulsing `1 + 0.04|sin 4t|`;
    - `d == StreakNext` and not claimable → "TOMORROW";
    - otherwise a dark overlay (0.45) + "DAY n".
  - Day 7 also gets a white shine band (UIGradient offset sweep every 2.5 s).
- **Claim feedback:**
  - Days 1-6: the card pops (UIScale 1.15 → 1, Back 0.35 s) + `SFX.play("HatchWin")`. The status line shows the reward text for 3 s.
  - Day 7: the `StreakCelebrate` overlay, dismissed by a tap or after 6 s:
    - full-screen black at 0.35 transparency;
    - a turning sunburst (rainbow ImageColor3 cycling);
    - the pet portrait popping 0.2 → 1 (Back 0.6 s);
    - the title "SECRET PET!" with the rainbow UIGradient;
    - the sub line "<display> <KG> KG + 5 of every potion + $X";
    - "TAP TO CONTINUE".
  - Errors flash on the card's State text for 1.5 s ("PETS FULL!" etc., uppercased reason).
- **Tab rules:**
  - The `GiftPage` attribute `Tab` is the one switch. Its change shows that view, hides the other and sets
    `Window.Face.Title.Text` to "Daily Rewards" / "Playtime Rewards". The tab buttons only set the attribute.
  - When GiftPage becomes visible (deferred one frame), `Tab` is set to "Daily" if `StreakClaimable`, otherwise
    "Playtime".
- **Auto-open:** once per session.
  1. After DataLoaded wait 6 s, then poll every 0.5 s for at most 120 s.
  2. Open when all of these hold:
     - `StreakClaimable`;
     - `OfflineUI` is missing or not `Enabled` (if it was Enabled, wait 1 s after it closes);
     - `IntroPlaying ~= true`;
     - `TutorialDone == true`;
     - `(TutorialExtra or 0) == 0`;
     - `MainMenu.Window.Visible == false`;
     - a live Humanoid.
  3. Then `OpenPage:Fire("Gift")`, which lands on the Daily tab.

- [ ] **Step 1: Back up** PlaytimeClient and MenuController.
- [ ] **Step 2: Write the `CLIENT_SRC` checks.** They need a fresh TestFreshSave player with Day 1 claimable.
  1. `auto_open`: within 15 s of DataLoaded, `MainMenu.Window.Visible` is true, `GiftPage.Tab == "Daily"` and the title is "Daily Rewards".
  2. `states`:
     - `Card1.State.Text == "CLAIM"`;
     - `Card2.State.Text == "DAY 2"`;
     - the Gift tile `Badge.Visible` is true.
  3. `claim`:
     - Fire Card1's claim through `RS.Streak.Claim:InvokeServer()`, the same as the button.
     - Within 1 s: `Card1.State.Text == "CLAIMED"`, `Card2.State.Text == "TOMORROW"`, and the status matches "^Next reward in %d%d:%d%d:%d%d$".
  4. `playtime_tab`: `GiftPage:SetAttribute("Tab", "Playtime")`.
     - Expect `PlaytimeView.Visible`, `DailyView.Visible == false` and the title "Playtime Rewards".
- [ ] **Step 3: Run the checks (Play, Client) and confirm they fail.** Expected: "Tabs not found".
- [ ] **Step 4: Implement the PlaytimeClient and MenuController changes, then StreakClient.**
- [ ] **Step 5: Re-run the client checks.** Expected: all pass.
- [ ] **Step 6: Day 7 visual.**
  - Server `StreakDebug "set"` day 6, last = today − 1.
  - Client: claim → `StreakCelebrate` is Enabled with the pet portrait Image non-empty.
  - `screen_capture`, then let it auto-close after 6 s.
- [ ] **Step 7: Screenshots.**
  - Desktop: the DAILY tab with day 3 claimable (set day 2, last = today − 1), and the PLAYTIME tab.
  - Ask the owner to switch the Studio device emulator to a phone (iPhone 16 Pro, landscape) for one DAILY screenshot. Never click that dialog myself.
  - Check: no text overflow, the cards readable at phone size, the [X] not covering the tabs. Fix and re-shoot until clean.
- [ ] **Step 8: Console scan.** `get_console_output`: no errors from StreakClient, PlaytimeClient or MenuController. Stop Play and set TestFreshSave back to false.
- [ ] **Step 9: Ledger line:** `Task 5: complete (...)`.

---

### Task 6: Final review, owner hand-off, memory

**Files:**
- Create: `docs/plans/review-2026-10-21/*.lua`, the exported Source of every changed and new script:
  - RebirthConfig, RebirthServer, RebirthClient;
  - TutorialServer, TutorialClient, PlayerData;
  - BaseHatchery (GiveEgg block only), Analytics;
  - StreakConfig, StreakServer, StreakClient;
  - PlaytimeClient, MenuController.
- Modify: memory files.
  - `roblox-rebirth-system.md`: v6 ladder, R1 money-only, READY banner.
  - `roblox-tutorial.md`: step 11 + stage 3.
  - New `roblox-login-streak.md`: rules, rewards, debug switches, files.
  - `MEMORY.md`: one index line.

- [ ] **Step 1: Export** the scripts with `execute_luau` (Edit). Return each Source and Write it to the review folder.
- [ ] **Step 2: Reviewer subagent.** Use `roblox-dev:roblox-reviewer`; the owner rule is reviewers = Haiku 5.5.
  - Inputs: the review folder, this plan, the spec, and the Review Focus list verbatim.
  - Focus: remote security (Claim spam, client-chosen values: there are none), DataStore fields, nil paths, deferred-signal races, Check-UI conformance.
- [ ] **Step 3: Fix pass.** Fix every Critical/Important finding with a failing check first. Re-run Task 1, 3, 4 and 5 tests: all pass. Log Minor findings in the ledger as deferred.
- [ ] **Step 4: Clean-up check.**
  - `TestFreshSave`, `TestTutorial` and `AnalyticsDebug` are false; `StreakDayOffset` is nil.
  - `settings().Network.IncomingReplicationLag == 0`.
  - The backups exist under `_Backup_RebirthStreak.Before` (they must have no tags).
- [ ] **Step 5: Memory files + MEMORY.md line.** Tell the owner what to Save + Publish, including the still-unpublished launch fix.
