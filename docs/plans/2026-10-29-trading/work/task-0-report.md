# Task 0 report: Audit + backups (no behaviour change)

Status: DONE_WITH_CONCERNS (the audit found four existing holes that later tasks must close; nothing was changed)
Date: 2026-10-29. Studio id 3bf21205-caff-490e-a927-3bd9f0097311, place 97952972919986.

## What I built / changed
- **Created** `ServerStorage._Backup_Trading` (Folder) > `Before` (Folder) holding 10 clones. Each clone has
  Enabled = false (Receipts is a ModuleScript), its CollectionService tags stripped (none existed), and the attributes
  `_OriginalPath` and `_BackedUp`. None of the scripts had children.

  | Backup | Original |
  |---|---|
  | `ServerStorage._Backup_Trading.Before.PlayerData` | `ServerScriptService.PlayerData` (376 lines) |
  | `...Before.BaseHatchery` | `ServerScriptService.BaseHatchery` (1082) |
  | `...Before.Receipts` | `ServerScriptService.Receipts` (98) |
  | `...Before.ShopServer` | `ServerScriptService.ShopServer` (346) |
  | `...Before.AdminServer` | `ServerScriptService.AdminServer` (765) |
  | `...Before.AutoReconnectServer` | `ServerScriptService.AutoReconnectServer` (290) |
  | `...Before.SellServer` | `ServerScriptService.SellServer` (156) |
  | `...Before.EggSpawner` | `ServerScriptService.EggSpawner` (934) |
  | `...Before.MenuController` | `StarterGui.MainMenu.MenuController` (616) |
  | `...Before.AdminClient` | `ServerStorage.AdminUI.AdminClient` (637) |

  I checked again after the Play session: every backup's Source still matches its live script exactly.
- **Edited** the ledger `docs/plans/2026-10-29-trading/progress.md`. I replaced the "## Audit" placeholder with 28 fact
  lines and did NOT write "Task 0: complete".
- **No script was changed.** Every audit step was a read, except two harmless side effects:
  - In the Play session I gave the test-save player 1 Wood Egg and 1 Molten Boar so I could inspect their Tools, then
    put EggInventory and PetInventory back exactly as they were. This touched only the throwaway save
    `studiotest_1793306247_<owner>`.
  - In Edit I read 294 `studiotest_` keys with GetAsync. Nothing was written.
- `workspace.TestFreshSave` was false. I set it to **true** before the Play test and left it true, as BUILDER_RULES
  says. The Play session I started is stopped: Studio is back in Edit.

## Tests
This is an audit-only task, so there are no TDD suites (no code to test). These are the live checks I ran instead:
- **PolicyService** (TestFreshSave Play, Server datamodel, player Santrinio, DataLoaded = true, TestSaveTag
  1793306247). `GetPolicyInfoForPlayerAsync` returned:
  ```
  AllowedExternalLinkReferences = {} (table)
  AreAdsAllowed = true (boolean)
  ArePaidRandomItemsRestricted = false (boolean)
  IsContentSharingAllowed = true (boolean)
  IsEligibleToPurchaseCommerceProduct = false (boolean)
  IsEligibleToPurchaseSubscription = true (boolean)
  IsEndlessContentAutoplayAllowed = true (boolean)
  IsEndlessContentLoadAllowed = true (boolean)
  IsPaidItemTradingAllowed = true (boolean)
  IsPhotoToAvatarAllowed = false (boolean)
  IsSubjectToChinaPolicies = false (boolean)
  IsThirdPartyAccountLinkingAllowed = true (boolean)
  ```
  -> `IsPaidItemTradingAllowed` is present, so no ruling was needed.
- **CanBeDropped** (same Play session):
  ```
  Backpack.Bat kind=other CanBeDropped=false
  Backpack.Wood Egg kind=egg CanBeDropped=false
  Backpack.Molten Boar kind=pet CanBeDropped=false
  ```
- **Yield probe** (Edit, coroutine status after one resume):
  ```
  BindableFunction:Invoke (non-yielding handler): dead
  BindableEvent:Fire (handler yields): dead
  WaitForChild (child exists): dead
  pcall(bf.Invoke): dead
  BindableFunction:Invoke (yielding handler): suspended
  ```
- **Save size:**
  - 294 studiotest_ keys were read, with 0 failures. The largest is `studiotest_1792638194_1809064431` at 7,162 bytes
    (69 pets in PetInventory). Next are 5,664 bytes and 4,290 bytes.
  - Synthetic worst case: 32,737 bytes (0.78 % of 4,194,304), built from:
    - 150 pets with the 17-character longest name, each with 2 mutations;
    - 28 base slots at R25;
    - 150 mutated eggs;
    - all 42 creatures in the Index;
    - 50 receipt ids;
    - 45 numeric fields.

    PetInventory alone takes 13.5 KB. Plenty of room for TradeEscrow, SettledRounds and TradeHistory.

## Audit facts
They're all in the ledger's "## Audit" section, one line each with script lines. Below are the ones that matter for
later tasks.

### Removers (all ten: no yield between check and remove)
- I read the whole path of every remover in the brief:
  - SellServer egg / allEggs / batch / pet;
  - BaseHatchery place / equip / unequip / equipBest / hatch / skip;
  - EggSpawner bank / drop.

  None of them yields between its check and its remove. Calls in those windows are pure config functions, JSON
  encode/decode and SetAttribute. BindableEvent:Fire calls only come AFTER the removal.
- place and equip check the live attributes, never the Tool (BaseHatchery L279 / L630). The client sends only
  kind/kg/mut or an id.
- Only skip/hatch check `Reconnecting` (L252, L732). Sell, place, equip, unequip, equipBest, bank and drop don't. While
  a player's save is sealed, those changes are lost on teleport: a rollback, not a dupe. Trading `take()` / `give()`
  must refuse while Reconnecting.
- `bank` (EggSpawner L548-568) checks neither DataLoaded nor the egg cap. The cap is checked only at pickup (L330), so a
  player over 150 eggs can still bank a carried egg. This matters for Task 3's `over_cap_after_give`.
- `hatch` (L338-342) adds the pet even if the egg record has already gone from BaseData. Only the `hatching[]` flag and
  the egg model guard it. If a trade ever removes placed eggs, it must also destroy the egg model or set `hatching`.

### Receipts
- The order is **grant -> addId -> save**: handler L57, addId L59, saveNow L68. PurchaseGranted comes only after a
  successful save, and that save is a blind UpdateAsync.
- **Grants then yields: SkipHatch** (BaseHatchery L778-783).
  - hatch writes the pet into BaseData (L343), then runs the GROW_SKIP task.wait loop (L352-358, about 1.2 s) before
    the handler returns true.
  - If the player leaves in that window, their leave-save holds the pet but no ReceiptIds entry. process sees
    player.Parent == nil and returns NotProcessedYet. Roblox's retry in the next server then hatches another egg.
- **Gift handler** (ShopServer L228 -> AddGiftedPass). It yields for up to 30 + 30 s plus an UpdateAsync before
  granting the target. If the buyer leaves meanwhile:
  1. the target keeps the pass;
  2. the buyer's receipt returns NotProcessedYet;
  3. the retry has no pendingGift, so ShopServer L235 gives the BUYER the pass as well.
- Every other handler (11 sites) grants with no yield after the grant.

### AddGiftedPass
- Only ShopServer.giveGift L179 calls it.
- It writes the target's save directly (PlayerData L305-316) whenever the target isn't `loaded` in THIS server. It
  doesn't check whether another server owns that save, so that server's next autosave erases the gift. The spec's
  GiftInbox_v1 fixes this.
- Its UpdateAsync callback sets `added = true` (L312), which is impure.

### Soft restart
- `sendToLobby` (AdminServer L161-184) teleports with no save first. Auto Reconnect, by contrast, seals first
  (AutoReconnectServer L139-140).

### DataStore errors (spec section 5 asks Task 0 for the exact texts)
- I recorded the throttle and queue texts from the Roblox docs page "Error codes and limits" (fetched 2026-10-29) in the
  ledger. I didn't reproduce them in Studio, because flooding the live store isn't worth the risk.
- Task 1's "throttled = retry, never lost" check should match on:
  - codes 301-306;
  - `"request was throttled"`;
  - `"queue was full"`;
  - `"exceeds the allowed maximum"`;
  - 502 with 429.

## Rulings
- Ruling: "remover" covers exactly the brief's list. I also grepped every live script for writers of
  PetInventory / EggInventory / BaseData. All of them are server-side in BaseHatchery, EggSpawner and SellServer, so
  the brief's list is complete for removals. Cost if wrong: a missed remover would need its own ItemLock in Task 3.
- Ruling: for the gift handler, I report "yields BEFORE the grant (to another player)" rather than "grant then yield".
  I flagged the double-grant path it opens separately. Cost if wrong: none, since both are in the ledger.
- Ruling: I added a worst-case synthetic save size next to the largest real test save. The biggest test save (7 KB)
  says little about a full 150/150 player. Cost: none.
- Ruling: I recorded the DataStore error texts from the docs, not from a reproduction. Cost if wrong: Task 1's
  error-text matching may need a tweak if Roblox changes the wording. Match on codes first.

## Concerns (for the controller / owner)
1. **SkipHatch grants, then yields** (see above): a crash or leave in that 1.2 s can grant twice. Task 1 must set the
   grant and the purchase id in one synchronous step: do the hatch's save part, then return, and animate afterwards.
2. **SkipHatch returns true when nothing hatched** (BaseHatchery L781-782, "Egg not found"). Today a paid skip whose egg
   is already gone takes the Robux and gives nothing. GrowAll also returns true with 0 eggs. This is existing behaviour,
   not changed here. **Owner:** consider making these return false (NotProcessedYet) or giving a fallback.
3. **Gift double grant** when the buyer leaves mid-gift (see above). Task 1 / GiftInbox should fix it.
4. **AddGiftedPass edits saves other servers own.** This is already covered by the spec's GiftInbox_v1.
5. Sell / place / equip / bank don't check Reconnecting, and bank skips the DataLoaded / cap checks. These are inputs
   for Task 3's ItemLock and over-cap rules.
6. The Studio Output shows one error from my own probe: "OfflineConfig:6: attempt to index nil with 'WaitForChild'".
   It came from requiring a CLONE of ShopConfig / OfflineConfig in Edit, whose WaitForChild then had no parent. It's
   harmless: the clones were never parented, and no game script was affected.
7. My Play session created one more test key, `studiotest_1793306247_1809064431`. It should go in the final
   studiotest_ cleanup.
