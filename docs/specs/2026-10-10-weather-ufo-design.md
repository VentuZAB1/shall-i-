# SLINGSHOT Weather System + UFO Invasion - design (2026-10-10)

## Goal
Random server-wide weather events that make the runway more exciting and give players a new chase:
**mutated eggs**. The first weather is **UFO Invasion**: a mothership arrives in one area with a cinematic cutscene,
small UFOs grab players (throwing them into the waves or far away) and beam up eggs, which come back with the **UFO
mutation (x1.5)**. The system is built so more weathers (each with its own mutation) plug in later; their mutations
stack.
**Success:**
- Every server gets ONE weather per hour (owner 2026-10-11; first version: every 10-20 min).
- The cutscene plays for the right players while the waves freeze.
- UFOs catch players and eggs fairly.
- A UFO egg hatches into a pet that earns x1.5 forever.
- Old saves keep working untouched.

## Decisions (the owner, 2026-10-10)
| Topic | Decision |
|---|---|
| Scope | Weather core + UFO Invasion now; the next weathers later |
| Schedule | Per server. ONE per hour since 2026-10-11 (`EVERY` 3600: the next starts an hour after the last started; a new server's first one after 10-20 min), 5 min each, the scheduled pick skips one that started within 15 min |
| Area | Starts in a random area, then moves to another one. Each stay is random 30-90 s and the stays always add up to exactly 5:00 (owner, 2026-10-10; was "every ~75 s") |
| Cutscene | "Mothership arrival", ~8 s, for everyone EXCEPT players on the slingshot and players in the tutorial |
| Mothership | Cutscene only (owner, 2026-10-10): it comes down, opens its belly doors, the small UFOs fly out, then it leaves. It takes no part in the invasion |
| Egg beam look | The small UFO opens its belly doors, the green beam slowly reveals downward, lifts the egg with animation and drops it back (owner, 2026-10-10: the saucer gets belly doors like the mothership's) |
| Waves during the cutscene | Frozen exactly where they are; stay frozen 2 s after it ends, then continue from the same spot |
| UFO models | Custom in Blender: a mothership + a small saucer (renders shown to the owner before import) |
| VFX | From the owner's **VFX Studio** plugin, never hand-made particles |
| Sounds | Licensed Creator Store sounds only (no ripped game/anime audio) |
| Animation | Reference from animationreference.org before animating (owner's rule) |
| Mutation | Egg -> pet keeps it forever; pet income x1.5; future mutations MULTIPLY (x1.5 then x2 = x3) |
| Safe from UFOs | Trenches / VIP holes (the wave safe boxes), players on the slingshot, players in the tutorial |

## Player experience
1. **Start.** A siren plays and the announcement bar shows "UFO INVASION has begun in WATER!". The 8 s cutscene
   plays and all waves freeze:

   | Time | Shot |
   |---|---|
   | 0.0 s | Screen pulses green, sky and fog tint green |
   | 1.0 s | Camera tilts up over the area; the clouds swirl into a vortex |
   | 2.5 s | The mothership pushes down through the clouds, its light ring spinning |
   | 4.5 s | Its belly opens; 4 small UFOs drop out and zip over the runway |
   | 6.0 s | One UFO sweeps its green beam across the eggs |
   | 7.0 s | Title slams in: "UFO INVASION - WATER" |
   | 8.0 s | Camera returns; waves stay frozen 2 s more, then move on |

2. **During (5 min).**
   - A weather pill sits in the bottom-right stack (same style as the boost pills): UFO icon,
     "UFO INVASION · WATER · 4:12". Hover or tap explains it.
   - Players inside the affected area see a green-tinted sky and fog.
   - The mothership hangs high over the area and 4 small UFOs patrol its runway.
3. **Moves.** After a random 30-90 s stay the fleet flies to another random area (the stays add up to exactly 5:00). The bar says "UFOs are moving to FIRE!". There
   is no cutscene and the waves don't freeze.
4. **End.** The fleet flies up and out, the bar says "The UFOs have left!", the sky goes back to normal and the
   pill disappears.

### UFO actions
Each small UFO acts every 20-30 s (random). It picks one target in its area:
- **Player (40 %, when someone can be caught).**
  1. A green target ring appears under the player for 2 s. That's fair warning: they can dive into a trench.
  2. Still not safe after 2 s: the UFO hovers over them and a green beam lifts them up (floating/struggling pose).
     An egg they're carrying drops on the spot.
  3. After ~2 s in the air they are thrown (50/50):
     - **into the waves:** set down 25-40 studs in the path of the nearest incoming wave (if no wave is coming,
       "far away" is used instead);
     - **far away:** flung 120-200 studs further down the runway (deeper, away from home), landing safely.
  4. A caught player can't be caught again for 45 s.
- **Egg (otherwise).** An egg lying in the area that doesn't have the UFO mutation yet.
  - The UFO hovers and the egg rises into the green beam. It can't be picked up while it's in the beam.
  - The egg comes back down glowing green with "UFO" on its label, and gets +30 s on its countdown so players can
    race for it.
- **No target:** the UFO just keeps patrolling.

**Who can be caught:** alive, on the runway inside the weather's area, not in a trench/VIP safe box, not on the
slingshot (SlingPhase Aiming/Loading/Flying), not in the tutorial (TutorialDone ~= false), not already being caught,
and their 45 s cooldown is over.

### Mutations
- A mutated egg keeps its mutation everywhere it goes:
  - carried and dropped on the runway (green label tag);
  - banked into the hotbar (UFO badge on the slot);
  - placed and hatching in the base;
  - the hatched pet, forever.
- **Pet income = base income x product of its mutation multipliers.** UFO = x1.5; a future x2 mutation on the same
  pet = x3.
- Sell values follow income automatically.
- **Pets show it:**
  - a green aura (VFX Studio);
  - "UFO" in green before the name on the pet tag;
  - a badge in the Pets panel, hotbar and inventory.
- An egg/pet can carry each mutation only once.
- The Creature Index, rebirth requirements and the Heaviest board are unchanged. Income boards include the boost
  automatically.

## Architecture (units)
1. **`ReplicatedStorage.Mutations`** (ModuleScript, pure). The mutation registry and helpers:
   - `TYPES = {UFO = {mult = 1.5, color = Color3 green, tag = "UFO"}}`
   - `mult(list) -> number` (product; nil/empty = 1)
   - `add(list, name) -> list` (no duplicates)
   - `encode(list) -> "UFO,..."` and `decode(string) -> list` (for attributes)
   - `label(list) -> rich text`
   - Egg-entry helpers for the inventory format:
     - `entryKg(e)`, `entryMut(e)`
     - `makeEntry(kg, mut)`: a plain number when there's no mutation, so old saves look the same
     - `findEntry(list, kg, mutKey)`
2. **`ReplicatedStorage.WeatherConfig`** (ModuleScript). Schedule numbers and the weather registry:
   - Schedule: `EVERY 3600` (one per hour, 2026-10-11), `GAP 600-1200` (a new server's first one), `NO_REPEAT 900`
   - `TYPES.UFO = {title = "UFO INVASION", duration = 300, moveEvery = 75, cutscene = 8, waveHold = 2, mutation = "UFO",
     ufoCount = 4, actEvery = {20, 30}, playerChance = 0.4, ringTime = 2, liftTime = 2, catchCooldown = 45,
     throwWave = {25, 40}, throwFar = {120, 200}, eggBonusTime = 30}`
3. **`ServerScriptService.WeatherLogic`** (pure, unit-tested):
   - `pickNext(history, now, types, rng)`: a type not used within NO_REPEAT, or nil (wait)
   - `nextArea(current, areaCount, rng)`: a different area
   - `canCatch(info)`: the catch rules above, from a plain table
   - `pickAction(eggCount, playerCount, rng)`
   - `throwKind(rng, waveAhead)`
   - `nextGap(rng)`
4. **`ServerScriptService.WeatherServer`** (Script):
   - Owns the schedule and the state.
   - Workspace attributes: `Weather` ("" or "UFO"), `WeatherArea`, `WeatherEnds` (server time), `WeatherCutsceneAt`.
   - Starts the weather's server module (`ServerScriptService.Weathers.UFO`).
   - Freezes and unfreezes the waves through WaveServer.
   - Fires announcements.
   - Exposes `ServerStorage.WeatherStart:Invoke(type?)` and `WeatherStop` (admin + tests).
5. **`ServerScriptService.Weathers.UFO`** (ModuleScript, server). The fleet (mothership + UFOs as server models,
   anchored, tweened), patrol, target choice, player catch (server-driven: drop egg -> anchor the root -> tween up ->
   throw -> unanchor), egg beaming (through the EggSpawner API below).
6. **`StarterPlayerScripts.WeatherClient`** (LocalScript) + **`ReplicatedStorage.Weathers.UFOClient`**:
   - the cutscene (camera, controls locked, skipped for slingshot/tutorial players);
   - the area sky/fog tint;
   - the weather pill, placed in the same bottom-right stack as the boost pills (AdminBannerClient makes room);
   - target rings, beam VFX and sounds.
7. **WaveConfig / WaveServer / WaveClient - a pausable wave clock.**
   - `WaveConfig.Clock()` = server time - `WavePausedTotal` - (now - `WavePausedAt` while paused); both values are
     workspace attributes.
   - Every wave-position, spawn and hit check uses the clock instead of `GetServerTimeNow()`, so a frozen wave stays
     exactly where it was and continues from there.
   - Wave clean-up waits on the clock too.
   - `ServerStorage.WavePause:Invoke(true/false)`.
8. **EggSpawner API.**
   - Live eggs get the `Mutations` attribute; it carries through carry/drop/bank.
   - `makeEggTool` sets `EggMut`.
   - `ServerStorage.EggBeam:Invoke(egg, mutation)`: lifts the egg, blocks pick-up, applies the mutation, sets it back
     down with +30 s.
   - `ServerStorage.WeatherEggs:Invoke(area)`: lists the live eggs in an area.
9. **Mutation plumbing (read and write `{kg, mut}` entries and the pet `mut` list).**
   - **Server:** BaseHatchery (inventory read, place, `rec.mut`, `pet.mut`, the pay loop via `petIncome`, pet model
     attribute `PetMut`), SellServer, InventoryConfig.
   - **Client:** EggPlaceClient (sends the mutation), Satchel slot badge, InventoryClient, SellClient, PetsEggsUI,
     PetTag.
   - **New helper:** `CreatureConfig.petIncome(name, kg, mut)` = `income(name, kg) * Mutations.mult(mut)`. Every
     place that pays or shows a specific pet's income uses it.
10. **Admin menu.** An ADMIN ABUSE row "WEATHER: UFO INVASION [START] [STOP]" through WeatherStart/WeatherStop
    and AdminLogic validation (kind `weather`). This server only at first; **all servers since 2026-10-11** (see the
    admin-menu spec: stored record, late servers join with the time left, `WeatherStart:Invoke(type, area, seconds)`).

## Data (save compatibility)
- **EggInventory** stays `{Kind = {entry, ...}}`.
  - An entry is either a number (KG, no mutation; every existing save) or `{kg = n, mut = {"UFO"}}`.
  - New eggs without a mutation are still saved as plain numbers.
- **BaseData.eggs** records and **pets** (BaseData.pets, PetInventory) get an optional `mut` list. A missing field
  means no mutation.
- No PlayerData version bump is needed: the fields are additive.

## Edge cases
- **Player leaves or dies mid-catch:** the UFO lets go and moves on. A dropped egg stays where it fell.
- **Weather ends or moves mid-action:** the action finishes first (a few seconds), then the UFO leaves.
- **Egg picked up or despawning while targeted:** the target is dropped and a new one is picked next turn. An egg in
  the beam can't be picked up or despawn.
- **Admin "No Waves" during a weather:** both work. The frozen clock and No Waves are separate switches.
- **Cutscene and waves:** a player who joins mid-cutscene doesn't get it. Waves resume for everyone at the same
  server time.
- **Every runway area has a wave safe box (trench) reachable within the 2 s ring time** for an alert player. The
  ring time is a config value if it needs tuning.
- **Wave Shield** still protects a player thrown into a wave.

## Testing
- **Unit, Edit mode (`ServerStorage.WeatherTests`):**
  - the schedule: no repeat within 15 min, gaps 10-20 min;
  - area moves always change the area;
  - `canCatch` rules;
  - Mutations: mult product/stacking, encode/decode, entries backward compatible with plain numbers, findEntry;
  - `petIncome` = income x 1.5 for UFO.
- **Play/Server (`ServerStorage.WeatherServerTests`):**
  - WeatherStart sets the attributes and freezes the wave clock, which resumes after cutscene + 2 s;
  - waves don't move while frozen;
  - EggBeam mutates an egg; it banks into `{kg, mut}`, places, hatches into a pet with `mut`, and the pet earns x1.5;
  - an old plain-number inventory still loads and places;
  - a catch moves an eligible test player, never a safe/tutorial/slingshot one;
  - WeatherStop cleans up.
- **Manual (owner):** the cutscene look, the UFO models, VFX and sounds, and a 2-player catch test.

## Out of scope (this round)
The next weathers and their mutations, mutations from other sources, Robux products tied to weather, cross-server
weather, weather forecasts/notifications.
