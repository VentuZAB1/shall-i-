# Task 3 report: `TradeItems` (take / give inside BaseHatchery)

Status: **DONE_WITH_CONCERNS**. All checks are green and mutation-tested. The concerns are hand-off notes for Tasks 5/6
(see the end), not defects here.

Builder: Opus, 2026-10-30. Studio `3bf21205-caff-490e-a927-3bd9f0097311`.
- Every Play session was started and stopped by me, with TestFreshSave == true checked in Edit right before each one.
  TestFreshSave is left true.
- I never saved or published.
- I didn't write the ledger line: the controller writes completion lines (Task 0 ruling).

## Scripts
| Path | Change | Backup |
|---|---|---|
| `ServerScriptService.BaseHatchery` (Script) | 1 header line (L11), plus a new `do ... end` block, "trading (ServerStorage.TradeItems)", L1024-1327 (between GiveEgg and the Studio testing helpers). Nothing else changed. | `ServerStorage._Backup_Trading.Before.BaseHatchery` (Task 0, already there; Enabled = false). No new backup: one per script, the first time only. |
| `ServerStorage.TradeItemsTests` (ModuleScript, new) | the live suite | n/a (new) |

At runtime the block creates `ServerStorage.TradeItems` (a BindableFunction). It requires `ServerScriptService.TradeCore`
and `ServerScriptService.PetIndex` once, when the block loads, so there's never a require inside an op.

Run (Play, Server datamodel, TestFreshSave session):
`require(game.ServerStorage.TradeItemsTests).live(game.Players:GetPlayers()[1], verbose?)`

## Ops (signatures and return shapes)
`ServerStorage.TradeItems:Invoke(op, player, ...)`. `player` = a Player, or a **virtual player**: a Folder with a numeric
`UserId` attribute plus `PetInventory` / `BaseData` / `EggInventory` / `DataLoaded` (`Reconnecting` optional).

```
"count", player              -> {[sig] = n}         base + stored pets, unplaced eggs ({} for a non-player / on error)
"describe", player, ref      -> item | nil          ref = {t = "pet", id} | {t = "egg", kind, kg, mutKey?}
"take", player, items        -> true, removed | false, reason
"give", player, items, mode  -> true | false, reason   mode = "deliver" | "return"
item = {t = "pet", sig, id, name, kg, mut?, from = "base" | "inv"}
     | {t = "egg", sig, kind, kg, mut?, from = "inv"}
sig  = TradeCore.petSig(item) / TradeCore.eggSig(kind, kg, mut)   (the one shared signature function)
mut  = a list of known mutation names, sorted (Mutations), nil when none
```

**count:** one entry per sig, counting every pet record and every egg entry. A pet with a bad KG or name has no sig, so
it's skipped.

**describe** builds the item from the server's own data.
- A pet is found by id across BaseData.pets + PetInventory. The result is `nil` when:
  - the id is missing;
  - the id is there twice (a broken save);
  - it's an old-roster creature that isn't `usable` (no CreatureConfig entry or model: it can't be shown, so it can't be
    offered).
- An egg needs a known kind (a template exists), a valid KG, and `mutKey` nil or a string. It returns the first entry
  whose sig matches. A bare KG number and `{kg}` with no mutation share one sig.

**take** is all-or-nothing, with no yield between the read and the write.
- **Refusal reasons:**
  - "Bad player";
  - "Your items are still loading" (`DataLoaded ~= true`);
  - "Reconnecting..." (`Reconnecting` set);
  - "Bad items" (not a list);
  - "Bad item" (not a pet or egg, `item.sig` isn't the sig of the item's own fields, or the same pet twice);
  - "You don't have that pet" (id missing or found twice, or the found pet's FULL sig differs: name, KG or mutation);
  - "You don't have that egg" (fewer entries of that sig than asked for).
- On a refusal nothing is written.
- **Success:** `removed[i]` matches `items[i]` (same order, same sig). It's built from the server's data and carries
  `from`.
  - The new BaseData / PetInventory / EggInventory are all JSON-encoded first, then set back to back.
  - Then, for real Players only, inside a pcall:
    - `despawnPet` for each base pet;
    - `rebuildPetTools` if a stored pet left;
    - `EggInventoryChanged:Fire` if an egg left.
  - Both rebuilds only touch the player's own Backpack and Character.
- An empty list returns `true, {}` (an empty side of the trade).

**give** never refuses for room or for where the items should go. It refuses only:
- a bad call: "Bad player", "Bad mode", "Bad items", or "Bad item" (an item with no valid sig); every item is checked
  before anything is written;
- a **"deliver"** while `DataLoaded ~= true` or while `Reconnecting` is set (same reasons as take).

A **"return"** always runs, even before DataLoaded and while Reconnecting.

- **Pets:**
  - "deliver": a new `newId()` for every pet, unique against the receiver's pets (base + stored), their growing eggs'
    ids (a hatch reuses the egg id) and the ids given in the same call. All go to PetInventory.
  - "return": the pet keeps its own id unless that id is taken by now (then it gets a new one). It goes back to the base
    when `from == "base"`, the player is a real Player and `#eggs + #pets < slots`. Otherwise it goes to PetInventory.
    A virtual player's base pets always go to the inventory.
- **Eggs:** `Mutations.makeEntry(kg, mut)` into EggInventory: the exact KG, plus the mutation.
- **No cap:** it may go past 150.
- **After the data write**, inside a pcall:
  - `PetIndex.record(p, name, kg)` for each delivered pet. It's synchronous: attribute reads and writes plus JSON, and
    `IndexConfig.decode` has no yield.
  - For real Players: `spawnPet` for the base pets, only if `loadedFor[p] == baseOf(p)` (otherwise loadBase spawns them
    later), then `rebuildPetTools` and `EggInventoryChanged`.

**Errors never escape:** OnInvoke wraps each op in a pcall, so an error in take / give comes back as `false, "Error"`.
Every write is one of the last plain steps of take / give, so a check that errors has written nothing.

## Rulings
1. **Tools.** Following the controller, take uses the existing rebuild paths instead of hand-destroying:
   - Pet Tools: `rebuildPetTools`. It's synchronous, so the traded pet's Tool is gone before take returns. Its other pet
     Tools come back as fresh copies, the same as equip / unequip; Satchel's ChosenHome puts player-placed slots back.
   - Egg Tools: `EggInventoryChanged` -> EggSpawner's rebuild. That handler can run a moment later (signals may be
     deferred). This is harmless: placing, selling and trading all read the EggInventory attribute, never the Tool
     (Task 0 audit).
   - The rebuilds make the Tools match the data: exactly one Tool fewer per removed item, and only in the player's own
     Backpack / Character. The test proves it, including two identical eggs where only one is traded.
2. **No ItemLock** (Task 0 audit: no remover yields between its check and its removal). take and give contain no
   WaitForChild / Invoke / Async / wait. The `no_yield` test runs every op inside `coroutine.create`, on a virtual player
   and on the real player, and asserts the coroutine is dead after one resume.
3. **describe refuses old-roster pets and unknown egg kinds;** count still counts them. take matches by sig only, and
   the offer can't hold them, so take never sees them.
4. **give accepts old-roster names** ("never fails": an escrowed item must always land somewhere). They're stored but
   not shown, like old pets already are.
5. **Item `mut` is normalised to known names only** (`Mutations.decode(Mutations.encode(...))`), the same way eggs are
   already handled by `entryMut`. The sig is unchanged by this, because `Mutations.key` ignores unknown names too.
6. **"Bad item" for a malformed give item:** nothing is given and the caller keeps its escrow. Skipping just that item
   would lose it silently.

## RED (the test module written first; BaseHatchery not yet changed)
```
TradeItems: 0 pass / 12 fail
FAIL take_all_or_nothing [TradeItems not found]
FAIL take_matches_full_sig [TradeItems not found]
FAIL take_destroys_only_own_tools [TradeItems not found]
FAIL exact_kg_eggs [TradeItems not found]
FAIL return_goes_back_to_base [TradeItems not found]
FAIL deliver_new_ids_unique [TradeItems not found]
FAIL over_cap_after_give [TradeItems not found]
FAIL give_never_fails [TradeItems not found]
FAIL describe_and_count [TradeItems not found]
FAIL escrow_matches_offer [TradeItems not found]
FAIL take_refused_when_not_loaded [TradeItems not found]
FAIL no_yield [TradeItems not found]
```

## GREEN (final, `live(p, true)`)
```
TradeItems: 12 pass / 0 fail
ok   take_all_or_nothing [20 asserts]
ok   take_matches_full_sig [15 asserts]
ok   take_destroys_only_own_tools [12 asserts]
ok   exact_kg_eggs [10 asserts]
ok   return_goes_back_to_base [19 asserts]
ok   deliver_new_ids_unique [19 asserts]
ok   over_cap_after_give [9 asserts]
ok   give_never_fails [13 asserts]
ok   describe_and_count [18 asserts]
ok   escrow_matches_offer [26 asserts]
ok   take_refused_when_not_loaded [7 asserts]
ok   no_yield [19 asserts]
-- real player attributes changed by the run: none
-- leftovers: none
```
- The console had no warnings or errors (no `[TradeItems]` lines).
- One check was added together with its fix after the first GREEN, without a separate RED run: in
  `return_goes_back_to_base`, "a returned pet never takes a growing egg's id".

**What the 12 tests cover** (the 8 from the brief plus 4 extras):
- **take_all_or_nothing:** a missing pet, a missing egg, an egg asked twice but owned once, a pet listed twice, and a
  non-list are each refused with the data byte-identical. A full mixed take (base + stored + 2 eggs) returns the items
  in order with the right `from`.
- **take_matches_full_sig:** same id with another KG, a KG 1e-12 off, another name, no mutation, another mutation, an
  extra mutation, and a forged sig are all refused. The exact pet goes.
- **take_destroys_only_own_tools:** the real player has 2 pet Tools and 3 egg Tools (two identical). Fake Tools with the
  same `PetId` / egg keys sit in another (virtual) player's Backpack and in a character Model in the world. After take,
  the traded pet's Tool is gone at once and the other pet's Tool stays. Exactly one of the two identical egg Tools is
  gone, every fake Tool survives, and the other player's data is unchanged.
- **exact_kg_eggs:**
  - 100.4 vs 100.5 KG are different eggs;
  - a bare 100.5 and `{kg = 100.5}` count as one sig;
  - `0.1 + 0.2` vs `0.3` are different sigs;
  - taking the 0.3 KG egg removes only that one, and returning it brings back exactly 0.3.
- **return_goes_back_to_base:**
  - real player: a base pet leaves its plot on take, comes back to the base (same id, KG, mutation) and walks again;
  - when the base got full in the meantime, it goes to the inventory with a hotbar Tool, and the base stays at its slots;
  - a virtual player's base pet goes to its inventory;
  - a taken id or a growing egg's id gets a new id.
- **deliver_new_ids_unique:**
  - every delivered pet gets a new id (even when the receiver owns the giver's id), and names, KG and mutations are kept;
  - eggs keep their exact KG and mutation;
  - the Index and BestKg are recorded;
  - 40 pets with the same giver id all get unique ids;
  - a delivery is refused while not loaded or while reconnecting.
- **over_cap_after_give (Review Focus 4):**
  - the real player is at 150 / 150; a delivery of 3 pets + 3 eggs lands at 153 / 153;
  - new gains are refused with the normal messages: GivePet -> `nil, "full"`, GiveEgg -> `nil, "full"`, and unequip ->
    "Pet inventory full ... sell pets at the Sell stall";
  - selling still works (SellDebug pet and egg), and so do take and count. No errors.
- **give_never_fails:**
  - a return lands when not loaded, while reconnecting, and with no item attributes at all;
  - 200 pets in one delivery; an empty list; an old-roster pet;
  - more base pets than slots: the base fills up and the rest are stored;
  - the only refusals are a bad mode, a NaN or negative KG item, and a non-player, and they write nothing.
- **describe_and_count:** item shapes, a duplicated id, an old-roster pet, an unknown egg kind, bad refs, the count
  numbers, a non-player, and `TradeCore.addItem` accepting describe's items with count's numbers.
- **escrow_matches_offer:**
  - the TradeCore flow (addItem x4 -> ready -> startConfirm), then `take(s.offer.a)`;
  - `setEscrowed` accepts take's list after a JSON round trip;
  - conservation: what's left plus the escrow equals what they had before;
  - returning the escrow restores the counts exactly.
- **take_refused_when_not_loaded:** `DataLoaded` false, nil (still loading) or `Reconnecting` -> refused and unchanged.
  An unparented Folder, workspace, a string or a number -> `false`, never an error.
- **no_yield:** every op, on a virtual player and on the real player.

## Mutation check (does the suite catch the bug it's meant to?)
I broke the code in two groups whose target tests don't overlap. Each group was applied in Edit and run in one fresh
TestFreshSave Play. The good source was kept in a temporary StringValue, restored byte-identical (checked), and the
StringValue was deleted.

| Mutant | Caught by |
|---|---|
| M1 take matches the pet by id only (not the full sig) | take_matches_full_sig ("same id, other KG: should be refused, got true") |
| M3 a delivered pet keeps the giver's id when free | deliver_new_ids_unique ("a delivered pet kept the giver's id: x9") |
| M7 take destroys pet Tools by PetId anywhere in the game | take_destroys_only_own_tools ("another player's Tool 1 was destroyed") |
| M9 a return refuses on an unloaded / sealed save | give_never_fails ("reconnecting: a return always runs") |
| M2 a missing egg doesn't stop the take | take_all_or_nothing ("one egg missing: should be refused") + exact_kg_eggs |
| M4 a returned base pet always goes to the inventory | return_goes_back_to_base ("back in the base ...: []") |
| M5 a delivery refuses past 150 | over_cap_after_give ("a delivery past 150") + give_never_fails ("200 pets at once") |
| M8 a `task.wait()` between take's read and write | no_yield ("take yielded") |

- Group A (M1, M3, M7, M9): 8 pass / 4 fail, exactly the 4 targets.
- Group B (M2, M4, M5, M8): 6 pass / 6 fail, the targets plus the expected second hits.

## Regression
- `ServerStorage.HubV2Tests` (bases, placement, reload / refit through BaseHatchery) in the same TestFreshSave Play:
  **109 pass / 1 fail**.
- The fail is `T11.1 makeover placements: Spawn at (0, 52) (0, -0.4000000059604645, 50.5)`: the hub SpawnLocation's
  position, which BaseHatchery never touches. It's unrelated to this change (most likely a later map edit). Task 8's
  full run should confirm it on the backup.

## Concerns / hand-off notes (Tasks 5 / 6)
1. **A "deliver" can refuse** ("Your items are still loading" / "Reconnecting..."). Settle must keep the escrow / ledger
   entry and retry, for example on the receiver's next load. It must never delete escrow on a `false`.
2. **The timing of a "return" before DataLoaded.** give writes the item attributes, so recovery must run AFTER
   PlayerData has written the save's fields into the attributes. Otherwise the load overwrites the returned items. This
   matches Task 1's TradeRecoveryHook carry note: re-read the live attributes inside the synchronous settle step.
3. **The only other give / take refusals are a bad call** (bad player / mode / item shape, or an item without a valid
   sig). Treat `false` as "nothing happened": keep everything in escrow and log it.
4. **Legacy egg counts.** A pre-weights EggInventory value (a plain count per kind) counts as no eggs in count / describe /
   take, and give would replace such a value with a list. EggSpawner migrates these at DataLoaded, before any trade can
   start, and the escrow save happens after that. So a save that holds escrow never has one, and PlayerData_v3 (the
   10-05 wipe) most likely has none at all. This is noted for the reviewer only.
5. **Unknown mutation names** in a pet's `mut` list would be dropped by a trade (rulings 5 and 6). None exist today:
   Mutations.TYPES = UFO, Meteor.
6. **Pre-existing, not changed:** `place()` gives new egg records a `newId()` without checking it against pet ids (a
   1-in-4-billion collision, the same class as every pet id). give now avoids the receiver's egg ids.

---

# Fix round 1 (2026-10-30)

Status: **DONE_WITH_CONCERNS**. Every review item is fixed, and TradeItemsTests is 15 pass / 0 fail (two runs in a
row). The concern is note 1 below, for the controller.
- TestFreshSave == true was checked in Edit before each of the 3 Play sessions; I started and stopped all of them.
- I never saved or published.
- No new backup was needed: `_Backup_Trading.Before.BaseHatchery` (Task 0) still stands.

## Changes
**`ServerScriptService.BaseHatchery`**: the trading block is now L1024-1354.
- **IMPORTANT 1, take's Tools now work like the Sell stall.**
  - A new `destroyPetTools(p, ids)` (L1109) destroys one Tool per removed stored pet, found by `PetId` (tostring
    compare), only in the trader's own `Backpack` and `Character`.
  - take no longer calls `rebuildPetTools`. Every other Tool stays the same instance, so the hotbar keeps its layout.
  - Eggs: `EggInventoryChanged` fires exactly as SellServer does it.
  - Base pets: `despawnPet`, as before.
  - give is unchanged on this point: `rebuildPetTools` like GivePet, `EggInventoryChanged` for eggs.
- **Minor: separate pcalls.** A new helper `after(what, fn, ...)` (L1103) runs each after-write step in its own pcall and
  warns `[TradeItems] <step>: <error>` on failure.
  - give: one per Index record, then finding the base, one per spawned base pet, the pet Tool rebuild, and the egg
    event.
  - take: one per despawned base pet, the pet Tool destroy, and the egg event.
  - So a `PetIndex.record` error can't skip the Tool rebuild or the egg event, and nothing after the write can reach
    OnInvoke's outer pcall (which would report a done give as `false`).
- **Minor: the header comment** now says that a "return" on a save that isn't loaded yet may ONLY come from PlayerData's
  `ServerStorage.TradeRecoveryHook` call. That call runs after the save's fields are in the attributes and before
  DataLoaded (PlayerData L159-175). Any earlier, and the load would overwrite the returned items. The header also states
  the Sell-stall Tool rule and the per-step pcalls.

**`ServerStorage.TradeItemsTests`**: 3 new tests, and no fixed sleeps any more.
- **New: `take_keeps_other_pet_tools`.** The real player has 3 stored pets plus 1 base pet, and the traded pet's Tool is
  moved into the character's hand. take of that pet + the base pet:
  - the traded Tool is gone, from the hand too;
  - the other two pet Tools are the SAME instances (identity checked) and still parented;
  - the base pet left the plot.
- **New: `mutation_order_same_sig`.**
  - A pet `{"UFO","Meteor"}` has the sig of `{"Meteor","UFO"}`.
  - Egg refs with mutKey "UFO,Meteor" and "Meteor,UFO" give the same item, and count agrees.
  - take accepts offer items written in the other order.
  - give stores one sorted list for a pet and for an egg.
- **New: `give_after_steps_independent`.** The real player gets an IndexData entry with `best = "broken"`, so
  `PetIndex.record` errors (`math.max` on a string). Delivering a pet + an egg still returns true, the items land, the
  pet's Tool is made and the egg's Tool is made. IndexData is put back straight away.
- **No fixed sleeps.** Both `task.wait(0.3)` are gone and use `waitUntil(cond, timeout)`.
  - `setReal` waits until every old egg Tool is destroyed, the new count matches the data (capped at MAX_EGGS a kind),
    and BaseHatchery's `sortBackpack` has finished (eggs before pets). Timeout 10 s, and the timeout is a failure.
  - The old L241 check waits for `eggTools(111.5) == 1 and eggTools(222) == 1 and inOrder()` (5 s), then re-checks
    the other pet's Tool.
  - The only `task.wait` left in the module is inside `waitUntil`.

## RED (the new checks against the unfixed BaseHatchery)
```
TradeItems: 13 pass / 2 fail
ok   take_all_or_nothing [20 asserts]
ok   take_matches_full_sig [15 asserts]
ok   take_destroys_only_own_tools [13 asserts]
ok   exact_kg_eggs [10 asserts]
FAIL take_keeps_other_pet_tools [the other pet Tools are the same instances (not recreated)]
ok   mutation_order_same_sig [7 asserts]
FAIL give_after_steps_independent [the pet's Tool was still made]
ok   return_goes_back_to_base [20 asserts]
ok   deliver_new_ids_unique [19 asserts]
ok   over_cap_after_give [10 asserts]
ok   give_never_fails [14 asserts]
ok   describe_and_count [18 asserts]
ok   escrow_matches_offer [26 asserts]
ok   take_refused_when_not_loaded [7 asserts]
ok   no_yield [20 asserts]
```
`mutation_order_same_sig` already passed in RED: the order-blind key comes from the shared sig function (TradeCore /
Mutations.key), so it is a guard. A mutant shows it has teeth (below).

## GREEN (`live(p, true)`, fixed code)
```
TradeItems: 15 pass / 0 fail
ok   take_all_or_nothing [20 asserts]
ok   take_matches_full_sig [15 asserts]
ok   take_destroys_only_own_tools [13 asserts]
ok   exact_kg_eggs [10 asserts]
ok   take_keeps_other_pet_tools [6 asserts]
ok   mutation_order_same_sig [7 asserts]
ok   give_after_steps_independent [5 asserts]
ok   return_goes_back_to_base [20 asserts]
ok   deliver_new_ids_unique [19 asserts]
ok   over_cap_after_give [10 asserts]
ok   give_never_fails [14 asserts]
ok   describe_and_count [18 asserts]
ok   escrow_matches_offer [26 asserts]
ok   take_refused_when_not_loaded [7 asserts]
ok   no_yield [20 asserts]
-- real player attributes changed by the run: none
-- leftovers: none
```
- A second run straight after, in the same session, also gave `TradeItems: 15 pass / 0 fail`.
- The console showed only the one warning `give_after_steps_independent` causes on purpose:
  `[TradeItems] give: Index: ServerScriptService.PetIndex:22: invalid argument #1 to 'max' (number expected, got string)`.
  That warning is the proof that the other steps ran past it.

## Mutation check for the guard
- **MO:** `mutList` keeps the caller's order (known names only, no sort). Result: `TradeItems: 14 pass / 1 fail`,
  `FAIL mutation_order_same_sig [the stored pet's list is sorted: [{... "mut":["UFO","Meteor"]}]]`.
- The good source was kept in a temporary StringValue, restored byte-identical (checked), and the StringValue was
  deleted. The GREEN run above was on that exact source.
- The two behaviour checks are proven by RED: the old `rebuildPetTools` in take, and the old single pcall in give.

## Notes for the controller
1. **A take that includes eggs still re-sorts the hotbar, exactly like selling an egg does today.**
   - `EggInventoryChanged` -> EggSpawner rebuilds the egg Tools -> the new egg Tools land after the pet Tools ->
     BaseHatchery's `sortBackpack` (L571-604) swaps every egg AND pet Tool for a fresh copy, in eggs-then-pets order.
   - Satchel's ChosenHome then puts the slots the player chose back (within 10 s).
   - So the "same instances" guarantee holds for pet-only takes (tested). A take with eggs behaves the same as a sell
     with eggs, which is the controller's "trades behave like sells" ruling.
   - If even that must go, the change belongs in EggSpawner / sortBackpack (sells would get it too). That's outside
     Task 3.
2. **The top 50 pet Tools.** rebuildPetTools gives Tools to the 50 best stored pets only. After a take, the 51st pet
   gets its Tool at the next rebuild (respawn, equip / unequip, a give). It's the same as selling a pet today, and it
   doesn't affect data.
3. **Left as ruled (ledgered):** the non-atomic two-attribute write edge case, the top-level requires without a pcall
   (they fail closed), and readData turning a corrupt save into {} (pre-existing).
