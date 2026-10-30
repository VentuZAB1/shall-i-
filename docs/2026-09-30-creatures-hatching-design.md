# SLINGSHOT — Creatures, egg placing, hatching, base pets (design)

Date: 2026-09-30 · Place: "My Roblox bla bla test." (97952972919986) · Scope: Grass, Water, Thunder (14 creatures)

## Decisions (from the user)
- Models: Blender low-poly, one MeshPart per body part, Motor6D rig, code-driven animation (like Fenrir).
- Hatch result: weighted random within the egg's area; heavier KG shifts odds toward the rarer creatures.
- Placing: equip the egg Tool, ghost preview, click inside your own fences.
- KG: bigger egg = bigger, longer hatch animation. Hand-made motion only, no generic glow/sparkle VFX.
- Saving: placed eggs (with timers) and hatched pets persist; timers keep running offline.
- Capacity: grows with base size.
- Pets: no interaction yet (just wander).
- Show all 14 in-game at once.
- Water pets (Hippocampus, Kraken Hatchling) float-swim in the air.

## Roster (rarity = area)
| Area | Egg | Creatures (common → rarest in area) | Motion |
|---|---|---|---|
| Grass (Common) | Wood | Mossback Tortoise, Forest Fawn, Treant Sprout, Vine Serpent | walk, walk, walk, slither |
| Water (Uncommon) | Tide | Sea Turtle Pup, Kappa, Hippocampus, Kraken Hatchling | walk, walk, swim, swim |
| Thunder (Rare) | Storm | Spark Fox, Raijū, Cloud Ram, Thunder Bull, Thunderbird, Storm Wyvern | walk ×4, fly, fly |

Base odds per area (first → last): 4 creatures 50/28/15/7; 6 creatures 35/25/17/12/7/4.
KG luck: `luck = clamp(log10(kg)/7, 0, 1)`; each weight i (0-based, n creatures) is multiplied by `1 + luck * 3 * i/(n-1)`.

## 1. Models
- Built in Blender with Python scripts (sources in `SLINGSHOT Creatures\blender\`), one shared painted palette texture per creature (≤512 px).
- Each creature ≤ 3,000 triangles total (Roblox: ≤ 20,000 per mesh, textures ≤ 1024 px).
- Parts named for the rig: `Body`, `Head`, `Jaw`, `LegFL/FR/BL/BR`, `Tail1..n`, `WingL/R`, `Tentacle1..n`, etc.
- Exported as one FBX per creature → Studio Import 3D → fix orientation/scale → Motor6D rig from `Body` → template in `ServerStorage.Assets.Creatures.<Area>.<Name>` with attributes `Motion` (Walk/Slither/Fly/Swim), `Area`, `DisplayName`, `BaseHeight`.
- All parts: Anchored off (driven by one anchored root), CanCollide/CanQuery/CanTouch false, Massless.

## 2. Placing eggs
- `ReplicatedStorage.BaseConfig` (ModuleScript): `HatchSeconds = 1`, `slots(width, length) = max(6, floor(w*l/270))`, fence inset 4 studs, min egg spacing 5 studs.
- Client `EggPlaceClient`: while an egg Tool is equipped and the player is in/near their own base, raycast mouse → base Floor; ghost egg (transparent clone) green if valid, red if not; click → `PlaceEgg:InvokeServer(kind, kgIndex, localXZ)`.
- Server `BaseEggs` validates: owner's base, inside inset rect, spacing, free slot, egg exists in EggInventory. Removes it from EggInventory, destroys the Tool, adds a record, spawns the placed egg.

## 3. Incubation + hatch
- Placed egg: egg model on the floor + BillboardGui countdown (studs-sized, like the runway eggs) using `PlacedAt` server time.
- At 0: owner-only ProximityPrompt "Hatch" (E, instant). Server rolls the creature, marks the record hatched, fires `HatchStart(eggId, creature, kg, tier)` to all clients, removes the egg after the animation length, then spawns the pet.
- Tier = 1..7 from `floor(log10(kg))+1`.

## 4. Hatch animation (client `HatchClient`, all hand-keyed)
1. Wobble: rocking in bursts that get stronger (duration 1.4s → 4s by tier), squash/stretch, crack pieces appear on the shell.
2. Hold: short stillness, deep squash.
3. Pop: shell splits into chunks (6 → 24 by tier, same material/colour as the shell) that arc out, bounce once on the floor and fade; flat dust ring expands along the ground; creature springs from scale 0 with overshoot and settles, then a hop/roar pose.
4. Owner camera shake scales with tier; tiers ≥ 6 get a brief slow-motion beat before the pop. Sounds: wobble creaks, crack, pop (Creator Store audio).

## 5. Pets in the base
- Server `BasePets` owns each pet's plan: pick a random target in the inset rect, set attributes `From`, `To`, `T0`, `Speed`, `State` (Move/Rest); rest 4–6 s (≈5 s) then repeat. Flyers target 8–14 studs up and land to rest; swimmers bob 3–6 studs up and drift slower.
- Client `PetAnimator` (CollectionService tag `BasePet`): interpolates position/facing from the attributes and drives limbs per `Motion` (leg gait, serpent wave, wing flap/glide, swim undulation), idle breathing while resting.
- Straight lines between points inside a rectangle stay inside the rectangle, so pets never leave the fences. Base rebuild/resize re-clamps them.

## 6. Saving
- New PlayerData field `BaseData` (JSON): `{eggs = {{id, kind, kg, x, z, placedAt}}, pets = {{id, creature, kg}}}` with `placedAt` = `os.time()`.
- On join (DataLoaded + base assigned): spawn eggs/pets; eggs past their time come back ready to hatch. On leave the base is cleared.

## Testing / showing
- Play test: bank an egg, place it, hatch it, check limits (outside fence, full base, other player's base).
- Showcase: hatch one of each of the 14 creatures in the player's base and screenshot them wandering/flying.

## Out of scope (later)
Fire/Shadow/Celestial creatures, pet pickup/sell, money from pets, real hatch times, pet size by KG.
