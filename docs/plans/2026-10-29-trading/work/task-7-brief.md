# Task 7 brief: UI (Trading tile, Admin button, Trading menu, request pop-up, trade window)

Plan: `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\plans\2026-10-29-trading\plan.md` (do NOT read the whole plan; this brief is your requirements).
Spec (the binding authority, read the sections your task touches): `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\specs\2026-10-29-trading-design.md`

## Task 7: UI (Trading tile, Admin button, Trading menu, request pop-up, trade window)

**Files:**
- Create: `StarterPlayer.StarterPlayerScripts.TradeClient` (LocalScript).
- Modify: `StarterGui.MainMenu.MenuController` (the Trading tile in the left menu tiles; a modal lock while a trade is
  open; a `Trade` page id).
- Modify: `ServerStorage.AdminUI.AdminClient` (`placeButton`: below the Rebirth and Index tiles instead of above Shop).
- Create mockup files: `docs/plans/2026-10-29-trading/ui/` (screenshots / offline renders of every screen).
- Test: `ServerStorage.TradeUITests` (client checks: the window opens/closes, the modal lock, the respawn rebuild,
  `menu_regression`).

**Interfaces:**
- Consumes: the Task 5/6 remotes and the `Push` view payload.
- Produces the screens:
  - the tile "🤝 Trading";
  - the Trading menu (Players | History, search, rows with headshot / @name / status / SEND, a disabled SEND with its
    reason, Invite Friends);
  - the bottom-right request card (ACCEPT / DECLINE, 30 s bar, up to 3 stacked);
  - the trade window:
    - Phase 1: inventory Pets / Eggs, the two 3x3 offers with $/s totals, READY with countdown, CANCEL, chat with the 6
      phrases, "syncing...";
    - Phase 2: read-only, exact KG + mutation words, the "You give / You get" line, "Securing items...", ACCEPT with
      countdown, BACK, "Waiting for @B...";
    - Done: "Trade complete!" with what you gave and what you got.
- [ ] **Step 1: Mockups** of every screen (Check-UI), reviewed by a fresh reviewer until each scores ≥ 8.5.
- [ ] **Step 2:** Write the failing UI tests (`menu_regression`, `trade_window_modal`, `rebuild_after_respawn`,
  `request_card_stack`).
- [ ] **Step 3:** Build to the approved mockups.
- [ ] **Step 4:** Run the tests. Phone emulator pass (the Device emulator, landscape phone) with text floors / tap
  targets measured. Final screenshots reviewed ≥ 8.5.
- [ ] **Step 5:** Ledger + reviewer gate.


## Global Constraints
- **NEVER publish.** At the very end the controller does File > Save to Roblox only (not Publish). The owner publishes.
- **TestFreshSave:** before EVERY Play test, check `workspace:GetAttribute("TestFreshSave") == true` in Edit (set it if
  it isn't). The controller sets it back to `false` after the LAST test of the whole job.
- **Never type into the Studio command bar or click Studio dialogs.** Use `execute_luau` for DataModel work. Never set
  `Camera.CameraType` from Edit scripts.
- **Backups:** before changing any existing script, clone it into `ServerStorage._Backup_Trading.Before`, with
  `Disabled`/`Enabled = false` and all CollectionService tags stripped. One backup per script, the first time only.
- **Studio names:** every DataStore / OrderedDataStore / MemoryStore map / MessagingService topic name gets the suffix
  `_Studio` when `RunService:IsStudio()`. Studio must never read or write a live trading store. `PlayerData_v3`
  itself keeps its existing test keys (`studiotest_<tag>_<userId>` when TestFreshSave).
- **Kill switch:** `ReplicatedStorage.TradeConfig.ENABLED` (default true). When false: no Trading tile, every trade
  remote refuses, sessions can't start. Recovery and settle ALWAYS run (items in escrow must still come back).
- **Every `UpdateAsync` callback is pure** (it may run more than once): side effects only after it returns.
- **Big execute_luau work** is chunked with `task.wait()`; scripts are written with `multi_edit` or by setting
  `.Source` from `execute_luau`.
- **UI:**
  - The `check-ui-clean-roblox` skill look only: GothamBlack, slate `#3B5866` panels, `#181E22` strokes, 3D [X],
    2-tier header divider, damier fade. Reuse `ReplicatedStorage.BrickUI` (the project's Check-UI builder) wherever
    it has a piece.
  - One layout on every device (phones = the PC layout scaled).
  - The window fit rule: cap at ~58 % of the screen width, wider on short phone screens.
  - Tap targets ≥ 42 px.
- **Ship bar:** every UI screen is reviewed by a fresh reviewer and must score ≥ 8.5/10 before it counts as done.
- **Reviewers / planners = Haiku, builders = Opus** (owner rule).
- **Limits (spec section 4):**
  - 9 items per side;
  - READY locked 5 s after the last change;
  - ACCEPT locked 5 s after Phase 2 starts (and until your own escrow is saved);
  - request pop-up 30 s;
  - 1 SEND per 3 s and 10 per 5 min;
  - 3 pending requests per receiver;
  - a 30 s pair cooldown after a decline;
  - offer changes 4/s per player and 30 per 10 s per trade;
  - quick chat 1 per 1.5 s, same phrase 1 per 5 s;
  - search 1 per 2 s, list 1 per 5 s;
  - idle 3 min, total 10 min;
  - 150 pets / 150 eggs (deliveries and returns may exceed it).
- **Quick chat phrases (exact, in this order):** Add More, L Trade, Last Offer, Deal?, Fair Trade, No Thanks.


## Review Focus
1. **Existing live saves** have no `_session` / `_ver` / `_wid`. The first load after publish must take them over
   and save normally, with nothing else changed. Test in Task 1: `legacy_save_loads`.
2. **A Studio session must never touch a live trading store.** Test in Task 2: `studio_store_names`, which asserts
   every name in `TradeConfig.stores()` ends in `_Studio` in Studio.
3. **A MemoryStore / MessagingService outage must never block or break a player's join or normal play.** Only
   trading pauses. Test in Task 4: `presence_failure_does_not_block_load`, with an injected failing MemoryStore.
4. **A player over 150 pets/eggs after a delivery** can still play: selling works, new gains are refused with the
   normal message, no error. Test in Task 3: `over_cap_after_give`.
5. **The existing menu tiles, the Admin button and every other window still open and close** on PC and on a phone
   once the Trading tile is added. Test in Task 7: `menu_regression` (+ the phone emulator pass).

