# Task 3 brief: `TradeItems` (take / give inside BaseHatchery)

Plan: `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\plans\2026-10-29-trading\plan.md` (do NOT read the whole plan; this brief is your requirements).
Spec (the binding authority, read the sections your task touches): `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\specs\2026-10-29-trading-design.md`

## Task 3: `TradeItems` (take / give inside BaseHatchery)

**Files:**
- Modify: `ServerScriptService.BaseHatchery` (a new BindableFunction `ServerStorage.TradeItems`). Any remover that
  Task 0 found yielding gets the per-player `ItemLock`.
- Test: `ServerStorage.TradeItemsTests` (`.live(player)` in Play; it uses the HatcheryDebug give/place helpers).

**Interfaces:**
- Consumes: `TradeCore.petSig`, `TradeCore.eggSig`.
- Produces:
  - `TradeItems:Invoke("count", player) -> {[sig] = n}`: the owned counts for offers.
  - `TradeItems:Invoke("describe", player, ref) -> item | nil`. `ref = {t="pet", id}` or
    `{t="egg", kind, kg, mutKey}`; `item = {t, sig, name/kind, kg, mut, from = "base"|"inv"}` built from server data.
  - `TradeItems:Invoke("take", player, items) -> (true, removed: {item...}) | (false, reason)`: all-or-nothing, no
    yields; Tools destroyed by instance only in the player's own Backpack/Character, one per item.
  - `TradeItems:Invoke("give", player, items, mode) -> true`. `mode = "deliver"` (new pet ids, Index record, to the
    inventory) or `"return"` (same items back where they came from if a base slot is free, else the inventory). It
    never fails and may exceed 150. It rebuilds Tools, fires `EggInventoryChanged`, respawns base pets.

- [ ] **Step 1: Write the failing tests:**
  - `take_all_or_nothing` (one missing item -> nothing removed);
  - `take_matches_full_sig` (same id, different KG -> refused);
  - `take_destroys_only_own_tools` (a fake second player's Tool with the same `PetId` survives);
  - `exact_kg_eggs` (a 100.5 KG and a 100.4 KG egg are different sigs);
  - `return_goes_back_to_base`, `deliver_new_ids_unique`, `over_cap_after_give`, `give_never_fails`.
- [ ] **Steps 2-5:** FAIL -> implement -> pass -> ledger + reviewer gate.


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

