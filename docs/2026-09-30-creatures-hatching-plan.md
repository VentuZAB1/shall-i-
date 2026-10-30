# Creatures + Base Hatching Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 14 textured, animated creatures (Grass/Water/Thunder) that hatch from eggs placed inside the player's fenced base and then wander/fly inside it, all saved.

**Architecture:** Creatures are Blender low-poly multi-mesh FBX → Studio MeshParts rigged with Motor6D from `Body`. Game logic is server-authoritative (`BaseEggs` places/hatches, `BasePets` plans wandering via attributes); clients do the visuals (`EggPlaceClient` ghost, `HatchClient` animation, `PetAnimator` motion). Pure logic lives in ReplicatedStorage modules so it can be tested with `execute_luau`.

**Tech Stack:** Roblox Studio (Luau, via Studio MCP `execute_luau`/`multi_edit`), Blender 5.2 (`C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`, headless `-b -P`), Studio Import 3D via computer-use, DataStoreService.

**Spec:** `SLINGSHOT Creatures\docs\2026-09-30-creatures-hatching-design.md`

## Global Constraints
- Place: "My Roblox bla bla test." (placeId 97952972919986). Build inside Studio via MCP; no .rbxmx files.
- Per creature ≤ 3,000 triangles; each mesh ≤ 20,000 (Roblox limit); textures ≤ 512 px (Roblox max 1024).
- Creature parts: CanCollide/CanQuery/CanTouch false, Massless, CastShadow true. Only the root is Anchored.
- `HatchSeconds = 1` (testing value, in `ReplicatedStorage.BaseConfig`).
- Slots: `max(6, floor(width*length/270))`. Fence inset 4 studs. Min egg spacing 5 studs.
- Rest pause 4–6 s. Flyers 8–14 studs up and land to rest. Swimmers bob 3–6 studs up.
- Hatch animation: hand-keyed motion + shell chunks + dust ring only. No glow/sparkle particle VFX.
- Odds (first→last): 4 creatures 50/28/15/7; 6 creatures 35/25/17/12/7/4. Luck `clamp(log10(kg)/7,0,1)`, weight i ×= `1 + luck*3*i/(n-1)`.
- Tier = `clamp(floor(log10(kg))+1, 1, 7)`.
- Blender sources/exports go in `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\blender\` (NOT Downloads).
- FBX imports come in at 100x and on their side: rotate -90° X then 180°, and rescale.
- The avatar uses AnimationConstraint joints; nothing here touches the avatar.
- Studio `screen_capture` doesn't render client GUIs: verify GUIs with computer-use screenshots. Disable `WaveServer` during playtests.

## Review Focus
1. Pressing E twice fast / two clients firing hatch → only one creature spawns (server `hatching` flag per egg id).
2. Player leaves mid-hatch → the record is already `pet` in BaseData before the animation, so the pet is there on rejoin.
3. Base rebuilt smaller (release/rebuild) → eggs/pets re-clamped inside the new inset rect, never outside the fence.
4. Placing before `DataLoaded`/without a base, in someone else's base, or with an egg not in EggInventory → rejected, egg kept.
5. Huge KG (90M Storm) → tier clamps to 7, luck clamps to 1, no NaN from log10(0) (kg floored at 1).

---

### Task 1: Config + odds modules

**Files:**
- Create: `ReplicatedStorage.BaseConfig` (ModuleScript)
- Create: `ReplicatedStorage.CreatureConfig` (ModuleScript)

**Interfaces:**
- Produces: `BaseConfig.HatchSeconds`, `BaseConfig.INSET`, `BaseConfig.SPACING`, `BaseConfig.slots(w,l)->int`, `BaseConfig.innerRect(floorPart)->(cf: CFrame, halfX, halfZ)`, `BaseConfig.inside(floorPart, worldPos, margin)->bool`, `BaseConfig.clampInside(floorPart, worldPos, margin)->Vector3`
- Produces: `CreatureConfig.Areas[eggKind] = {area=int, list={{name, display, motion}}}`, `CreatureConfig.odds(eggKind, kg)->{number}`, `CreatureConfig.roll(eggKind, kg, rng?)->name`, `CreatureConfig.tier(kg)->1..7`, `CreatureConfig.byName[name] = {eggKind, display, motion}`

- [ ] **Step 1: Write the failing test** (run with `execute_luau`, Edit)

```lua
local RS = game.ReplicatedStorage
local C = require(RS.CreatureConfig); local B = require(RS.BaseConfig)
local function near(a,b) return math.abs(a-b) < 1e-6 end
local o = C.odds("WoodEgg", 1); assert(near(o[1],.50) and near(o[4],.07), "base odds")
local s=0; for _,v in C.odds("WoodEgg", 1e7) do s+=v end; assert(near(s,1), "normalised")
assert(C.odds("WoodEgg",1e7)[4] > 0.15, "luck raises rarest")
assert(#C.odds("StormEgg",1) == 6 and near(C.odds("StormEgg",1)[6], .04))
assert(C.tier(0)==1 and C.tier(1)==1 and C.tier(999)==3 and C.tier(9e7)==7)
local counts={}; local r=Random.new(1); for i=1,20000 do local n=C.roll("WoodEgg",1,r); counts[n]=(counts[n] or 0)+1 end
assert(math.abs(counts.MossbackTortoise/20000-.5)<.02, "roll matches odds")
assert(B.slots(40,40)==6 and B.slots(64,120)==28)
local f = Instance.new("Part"); f.Size=Vector3.new(40,.5,40); f.CFrame=CFrame.new(0,0,0)
assert(B.inside(f, Vector3.new(15,0,15), 0) and not B.inside(f, Vector3.new(17,0,0), 0))
assert(B.clampInside(f, Vector3.new(100,5,-100), 1).X == 15)
f:Destroy(); return "ok"
```

- [ ] **Step 2: Run it → FAIL** ("CreatureConfig is not a valid member").

- [ ] **Step 3: Implement**

`BaseConfig`:
```lua
-- BaseConfig: shared numbers for eggs/pets inside player bases (server + client).
local BaseConfig = {}
BaseConfig.HatchSeconds = 1 -- TESTING value; real hatch times come later
BaseConfig.INSET = 4        -- keep eggs/pets this far inside the fence line
BaseConfig.SPACING = 5      -- min distance between placed eggs
BaseConfig.REST = {4, 6}    -- pets pause this many seconds between moves
BaseConfig.FLY_HEIGHT = {8, 14}
BaseConfig.SWIM_HEIGHT = {3, 6}

function BaseConfig.slots(width, length)
	return math.max(6, math.floor(width * length / 270))
end

-- Floor top-centre CFrame and the usable half extents after the inset.
function BaseConfig.innerRect(floor)
	local cf = floor.CFrame * CFrame.new(0, floor.Size.Y / 2, 0)
	return cf, floor.Size.X / 2 - BaseConfig.INSET, floor.Size.Z / 2 - BaseConfig.INSET
end

function BaseConfig.inside(floor, pos, margin)
	local cf, hx, hz = BaseConfig.innerRect(floor)
	local p = cf:PointToObjectSpace(pos)
	return math.abs(p.X) <= hx - margin and math.abs(p.Z) <= hz - margin
end

function BaseConfig.clampInside(floor, pos, margin)
	local cf, hx, hz = BaseConfig.innerRect(floor)
	local p = cf:PointToObjectSpace(pos)
	local mx, mz = math.max(0, hx - margin), math.max(0, hz - margin)
	return cf:PointToWorldSpace(Vector3.new(math.clamp(p.X, -mx, mx), p.Y, math.clamp(p.Z, -mz, mz)))
end

return BaseConfig
```

`CreatureConfig`:
```lua
-- CreatureConfig: which creatures hatch from which egg, their odds and how they move.
-- Rarity comes from the area; inside an area the list goes common -> rarest.
local CreatureConfig = {}

local ODDS = {
	[4] = {50, 28, 15, 7},
	[6] = {35, 25, 17, 12, 7, 4},
}

CreatureConfig.Areas = {
	WoodEgg = {area = 1, list = {
		{name = "MossbackTortoise", display = "Mossback Tortoise", motion = "Walk"},
		{name = "ForestFawn", display = "Forest Fawn", motion = "Walk"},
		{name = "TreantSprout", display = "Treant Sprout", motion = "Walk"},
		{name = "VineSerpent", display = "Vine Serpent", motion = "Slither"},
	}},
	TideEgg = {area = 2, list = {
		{name = "SeaTurtlePup", display = "Sea Turtle Pup", motion = "Walk"},
		{name = "Kappa", display = "Kappa", motion = "Walk"},
		{name = "Hippocampus", display = "Hippocampus", motion = "Swim"},
		{name = "KrakenHatchling", display = "Kraken Hatchling", motion = "Swim"},
	}},
	StormEgg = {area = 3, list = {
		{name = "SparkFox", display = "Spark Fox", motion = "Walk"},
		{name = "Raiju", display = "Raijū", motion = "Walk"},
		{name = "CloudRam", display = "Cloud Ram", motion = "Walk"},
		{name = "ThunderBull", display = "Thunder Bull", motion = "Walk"},
		{name = "Thunderbird", display = "Thunderbird", motion = "Fly"},
		{name = "StormWyvern", display = "Storm Wyvern", motion = "Fly"},
	}},
}

CreatureConfig.byName = {}
for eggKind, def in CreatureConfig.Areas do
	for _, c in def.list do
		CreatureConfig.byName[c.name] = {eggKind = eggKind, display = c.display, motion = c.motion}
	end
end

function CreatureConfig.tier(kg)
	return math.clamp(math.floor(math.log10(math.max(kg or 1, 1))) + 1, 1, 7)
end

function CreatureConfig.odds(eggKind, kg)
	local list = CreatureConfig.Areas[eggKind].list
	local n = #list
	local base = ODDS[n]
	local luck = math.clamp(math.log10(math.max(kg or 1, 1)) / 7, 0, 1)
	local w, total = {}, 0
	for i = 1, n do
		w[i] = base[i] * (1 + luck * 3 * (i - 1) / (n - 1))
		total += w[i]
	end
	for i = 1, n do w[i] /= total end
	return w
end

function CreatureConfig.roll(eggKind, kg, rng)
	local w = CreatureConfig.odds(eggKind, kg)
	local r = (rng or Random.new()):NextNumber()
	local list = CreatureConfig.Areas[eggKind].list
	for i, p in w do
		r -= p
		if r <= 0 then return list[i].name end
	end
	return list[#list].name
end

return CreatureConfig
```

- [ ] **Step 4: Run the test → "ok".**
- [ ] **Step 5: Save** (File → Save in Studio is the user's; just note it in the summary).

---

### Task 2: Blender creature kit

**Files:**
- Create: `SLINGSHOT Creatures\blender\creature_kit.py`

**Interfaces:**
- Produces (Python): `new_scene(name)`, `palette(colors: dict[name->hex]) -> material`, `box(name, size, loc, color, bevel=0.15, parent=None)`, `ellipsoid(name, radii, loc, color, segs=10, parent=None)`, `cone(name, r1, r2, depth, loc, color, verts=8, parent=None)`, `join_as(name, objs)` (merge pieces that don't move separately into one rig part), `pivot(obj, world_point)` (set origin = joint), `tri_count()`, `export_fbx(path)`, `render_lineup(path)`.
- Palette: one 64×64 PNG per creature, 8×8 grid of 8-px cells, each face's UVs collapse to its colour's cell centre (Closest interpolation) — same technique as the treadmills.
- Rig-part naming contract (used by Task 4/8): `Body` (root), `Head`, `Jaw`, `LegFL`,`LegFR`,`LegBL`,`LegBR` (or `LegL`,`LegR` for bipeds), `ArmL`,`ArmR`, `Tail1..N`, `WingL`,`WingR`, `Tentacle1..N`, `Seg1..N` (serpent), `Ear*`, `Eye*` (joined into Head unless named `EyeGlow*`). Each part's origin is placed at its joint.

- [ ] **Step 1: Test script** `kit_test.py`: build a 2-part test (Body box + Head ellipsoid pivoted at neck), assert `tri_count() < 3000`, export to `blender\export\_test.fbx`, assert file exists and size > 0.
- [ ] **Step 2: Run** `"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P kit_test.py` → FAIL (no kit).
- [ ] **Step 3: Implement `creature_kit.py`** with bmesh primitives + bevel modifier applied, palette PNG saved next to the export, `bpy.ops.export_scene.fbx(filepath, use_selection=False, path_mode='COPY', embed_textures=True, object_types={'MESH'}, apply_unit_scale=True, bake_space_transform=False, add_leaf_bones=False)`.
- [ ] **Step 4: Run test → PASS.**

---

### Task 3: Model the 14 creatures

**Files:**
- Create: `blender\grass.py`, `blender\water.py`, `blender\thunder.py` (each defines one function per creature using the kit, then exports `blender\export\<Name>.fbx` and renders `blender\renders\<Name>.png`).

Look per creature (chunky, readable at 3–6 studs, Escape-Tsunami-bright palette, 2 eye whites + dark pupils, beveled blocks + rounded shells):
- MossbackTortoise (Walk, 4 legs): domed hex-plated shell with moss top + 3 tiny flowers, stubby legs, round head. 
- ForestFawn (Walk, 4 legs): slim body, white spots, leaf-sprout antlers, big ears.
- TreantSprout (Walk, 2 legs + 2 arms): stump body with face, twig arms, leafy crown, root feet.
- VineSerpent (Slither, Seg1..8 + Head + Jaw): tapered green segments with leaf frills, flower on head.
- SeaTurtlePup (Walk, 4 flippers): teal shell with sand-coloured rim, flipper legs.
- Kappa (Walk, biped): green imp, turtle shell back, beak, water dish on head (dish has a blue water disc).
- Hippocampus (Swim): horse front + curled fish tail Tail1..4, fin mane, flipper forelegs.
- KrakenHatchling (Swim): round purple head-body, big eyes, Tentacle1..6 each 3 segments (Tentacle1_1..3).
- SparkFox (Walk, 4 legs): yellow fox, zigzag tail Tail1..3, pointed ears.
- Raiju (Walk, 4 legs): blue-white wolf-cat, lightning-bolt shaped mane spikes, bolt tail.
- CloudRam (Walk, 4 legs): puffy white cloud wool (cluster of spheres), curled gold horns.
- ThunderBull (Walk, 4 legs): dark-slate bulk, yellow bolt markings, big horns, nose ring.
- Thunderbird (Fly): big eagle, WingL/WingR (each wing 2 parts: WingL, WingL2 tip), yellow-edged feathers, tail fan.
- StormWyvern (Fly): dragon body, WingL/R (+ tips), Tail1..5, horns, 2 hind legs.

- [ ] **Step 1:** Write `grass.py`; run headless; check each tri count < 3000 and PNG renders.
- [ ] **Step 2:** Same for `water.py`, `thunder.py`.
- [ ] **Step 3:** Render `renders\lineup.png` of all 14 and look at it (Read the PNG). Fix anything unreadable (eyes, proportions) before importing.

---

### Task 4: Import + rig templates in Studio

**Files:**
- Create: `ServerStorage.Assets.Creatures.{Grass,Water,Thunder}.<Name>` (Models)
- Create: `ReplicatedStorage.CreatureRig` (ModuleScript)

**Interfaces:**
- Produces: `CreatureRig.build(model)` → creates `Root` (invisible anchored 1×1×1 Part at the feet, PrimaryPart) and Motor6Ds named after the child part, parented under the parent part. Parent rule: `Head,Jaw(→Head),Leg*,Arm*,Wing*(tips→wing),Tail1(→Body),TailN(→TailN-1),Seg1(→Body),SegN(→SegN-1),Tentacle*_1(→Body),*_k(→*_k-1)`, everything else → Body. For the serpent, `Body` is the neck block behind `Head`. Stores each motor's rest `C0` in attribute `RestC0` (CFrame).
- Template attributes: `Motion`, `EggKind`, `DisplayName`, `Height` (studs, bounding box Y).
- Template Clone for pets goes to `ReplicatedStorage.CreatureModels` (clients need them for the hatch reveal and pet visuals).

- [ ] **Step 1:** Import each FBX via Studio Import 3D (computer-use: Home → Import 3D, type full path, Import). Orientation fix `-90° X, 180°`, scale so the creature is 3–6 studs tall (walkers ~3.5, flyers/wyvern ~5).
- [ ] **Step 2:** Run `CreatureRig.build` on each; move into the area folders; clone to `ReplicatedStorage.CreatureModels`.
- [ ] **Step 3: Test** (`execute_luau`): for every name in `CreatureConfig.byName`, the template exists, has `Root` PrimaryPart, every BasePart except Root is welded by a Motor6D, triangle proxy check (`#parts ≤ 40`), all parts CanCollide false, textures present (`MeshPart.TextureID ~= ""`).

---

### Task 5: Save + server egg placing/hatching (`BaseEggs`)

**Files:**
- Modify: `ServerScriptService.PlayerData` — add `BaseData = '{"eggs":[],"pets":[]}'` to FIELDS.
- Create: `ServerScriptService.BaseEggs` (Script)
- Create remotes in ReplicatedStorage: `PlaceEgg` (RemoteFunction), `HatchStart` (RemoteEvent)

**Interfaces:**
- Consumes: BaseConfig, CreatureConfig, EggInventory attribute + `EggSpawner` rebuild (EggSpawner exposes `ReplicatedStorage.EggInventoryChanged` BindableEvent — add it: fire `(player)` → EggSpawner calls `rebuildBackpack(player)`).
- Produces: `workspace.BaseContent.<BaseId>` folder with `Egg_<id>` models (attrs `EggId`, `Kind`, `KG`, `ReadyAt` server time, `Owner`) and pets (from Task 7). `HatchStart:FireAllClients(eggModel, creatureName, kg, tier, duration)`. BindableEvent `ServerStorage.SpawnPet` `(player, petRecord)`.

Core logic:
```lua
-- validate(player, kind, kg, pos) -> ok, reason
-- 1 DataLoaded == true and BaseId ~= 0; base floor = baseOf(player).Plot.Floor
-- 2 BaseConfig.inside(floor, pos, 1.5) (egg radius margin)
-- 3 distance to every other egg in this base >= BaseConfig.SPACING
-- 4 #data.eggs < BaseConfig.slots(base.Width, base.Length) (pets don't use slots)
-- 5 EggInventory[kind] contains kg (exact number, first match removed)
```
Hatch: ProximityPrompt (`HoldDuration 0`, `KeyboardKeyCode E`, `RequiresLineOfSight false`, `Enabled` only when `workspace:GetServerTimeNow() >= ReadyAt`; a server loop enables it). On `Triggered` by the owner and `not hatching[id]`: roll creature, move record eggs→pets in BaseData (write attribute immediately), `HatchStart:FireAllClients(...)`, `task.delay(duration, destroy egg + SpawnPet)`. `duration = 1.4 + (tier-1) * 0.43 + 1.2` (wobble + hold/pop).
Rejoin: after DataLoaded and base assigned, spawn all eggs (ReadyAt = placedAt-based: `placedAt + HatchSeconds` mapped to server time via `os.time()` difference) and all pets.
Base released → destroy `BaseContent.<BaseId>`.

- [ ] **Step 1: Test** validate() with a fake player table stub (validate takes `(state, base, kind, kg, pos)` pure-ish so it's testable): outside fence rejected, too close rejected, full rejected, missing kg rejected, good spot accepted.
- [ ] **Step 2:** Implement, run tests → pass.
- [ ] **Step 3:** Playtest: bank egg → call PlaceEgg from the client console → egg appears, EggInventory shrinks, BaseData grows; stop/start play → egg is back.

---

### Task 6: `EggPlaceClient` ghost placement

**Files:** Create `StarterPlayerScripts.EggPlaceClient` (LocalScript)

- While a Tool with `EggKind` is equipped and `CurrentArea` is nil: every RenderStep raycast mouse (or touch position / screen centre on mobile) against own base `Plot.Floor` only (RaycastParams Include). Ghost = template clone (sized with EggSize.height(kg)), all parts Transparency 0.5, `Highlight` green (valid via BaseConfig.inside + spacing vs `BaseContent` eggs + slot count) or red. Hidden when the ray misses.
- `tool.Activated` (click/tap) → `PlaceEgg:InvokeServer(kind, kg, pos)`; on false show a small red toast with the reason ("Outside your base", "Base full 6/6", "Too close").
- Slot counter label "Eggs 3/6" in the corner while equipped.

- [ ] Test: playtest, equip egg, screenshot (computer-use) green inside / red outside; click places; full base shows toast.

---

### Task 7: `HatchClient` animation

**Files:** Create `StarterPlayerScripts.HatchClient` (LocalScript), sounds under `ReplicatedStorage.HatchSounds` (Creator Store: creak, crack, pop, thud — vetted).

Timeline (T = tier 1..7, `k = (T-1)/6`):
1. Wobble `1.4 + 2.6k` s: 3–(3+4k) bursts; each burst rotates ±(8+14k)° around a random horizontal axis with `sin` decay, gap shrinks; squash Y 0.92 / stretch 1.06 per burst; creak sound pitch rises. After burst 2, crack pieces (thin dark wedges parented to the shell surface, count 2+6k) fade in.
2. Hold 0.35 s: still, then squash to Y 0.8 over 0.15 s. T ≥ 6: 0.25 s slow-mo (all tweens ×0.3 speed) + FOV −6.
3. Pop: shell → `6 + 18k` chunks (small wedge Parts coloured from the shell's texture average, Material Plastic), launched outward/up with random spin (client-side unanchored, CanCollide true vs floor only via collision group `HatchChunks`), bounce, fade after 1.2 s. Dust ring: flat cylinder, off-white, Transparency 0.4→1, size 1→(10+14k) over 0.6 s. Owner camera shake amplitude `0.15 + 0.6k` decaying over 0.5 s.
4. Creature reveal: clone from `ReplicatedStorage.CreatureModels`, scale 0 → 1.15 (Back Out 0.35 s) → 1.0; hop 1.5 studs; Head motor tilts up (roar) 0.4 s; name label "Spark Fox" pops above for 2 s.
The server spawns the real pet at the end; the client then destroys its reveal clone the moment the real pet appears at the same spot (match by `EggId` attribute copied to the pet).

- [ ] Test: playtest with forced tiers 1, 4, 7 (debug: server command `_G.ForceKG`) and record screenshots of each phase.

---

### Task 8: `BasePets` + `PetAnimator`

**Files:** Create `ServerScriptService.BasePets` (Script), `StarterPlayerScripts.PetAnimator` (LocalScript)

Server (`SpawnPet` handler + rejoin): pet model = template clone, Root anchored at a random inside point, tag `BasePet`, attrs `Creature`, `KG`, `EggId`, `Motion`. Planner loop per pet:
```lua
-- pick target inside BaseConfig.clampInside(floor, randomPoint, radius)
-- height: Walk/Slither 0; Fly rand(FLY_HEIGHT) while moving, 0 when resting; Swim rand(SWIM_HEIGHT)
-- speed: Walk 6, Slither 5, Swim 4, Fly 10 (studs/s)
-- set attrs From (Vector3), To (Vector3), T0 (server time), Dur, State="Move"
-- after Dur: server snaps Root.CFrame to To (keeps server truth), State="Rest", wait rand(REST), repeat
```
Client: for each tagged pet, every RenderStepped: `alpha = (now - T0)/Dur` smoothstep, position lerp From→To, face travel direction (turn rate limited), flyers arc up/land with an ease; set a local `CFrame` on the anchored Root (client-side visual override). Limb animation by Motion using each motor's `RestC0`:
- Walk: diagonal leg pairs swing `sin(phase)*0.6 rad`, body bob, head nod; bipeds alternate legs + arms.
- Slither: `Seg_i` yaw `sin(phase - i*0.7)*0.35`.
- Fly: wings flap `sin(phase*1.6)*0.9` while moving, glide hold when descending, folded when resting.
- Swim: tail/tentacles wave slowly, body bob `sin(t)*0.3`.
- Rest (all): breathing scale on Body 1±0.02, occasional head look-around.
Only animate pets within 150 studs of the camera.

- [ ] Test: playtest with 14 pets in one base (debug spawn), watch 60 s: none leaves the fence rect (server check each second: `BaseConfig.inside(floor, root.Position, 0)`), pauses ~5 s, flyers land.

---

### Task 9: Show all 14 in-game

- [ ] Temporarily bump the tester's base to 64×120 via `BaseBuilder.Build` so 14 fit, hatch one of each (debug roll override), take computer-use screenshots of the hatch and of the base with all 14 wandering, show the user. Then restore the base size and remove the debug hooks.
- [ ] Update memory (`roblox-game-direction.md`, `roblox-creature-rigging.md`) with the new systems and file locations.
