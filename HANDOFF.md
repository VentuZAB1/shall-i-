# SLINGSHOT creatures: handoff for the next session (2026-09-30)

Roblox place: "My Roblox bla bla test." (placeId 97952972919986), SLINGSHOT game.
Folder: `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\`

## What the user wants (the big picture)
- Creatures hatch from eggs captured on the runway. Eggs can only be placed **inside the player's own base (inside the fences)**.
- Hatch timer is **1 s for testing** (`ReplicatedStorage.BaseConfig.HatchSeconds`). At 0 the player presses **E** to hatch.
- A **cool hatching animation** that gets bigger with the egg's KG: shaking, cracks, then the pop. It must be hand-made, with no generic glow effects.
- Hatched creatures wander **only inside the base fences**: walk, pause about 5 s, walk again. Flyers fly around and land for 5 s breaks.
- Saving: placed eggs, their timers and the pets persist. Slots grow with base size. There's no pet interaction yet.
- Roster: Grass 4, Water 4, Thunder 6 (this batch = 14). Later: Fire 8, Shadow 10, Celestial 10. Rarity = area.
- **STYLE RULE (important):** creatures must look **cool, fierce, "stylized fierce"**, NOT cute or kid-friendly. The user rejected every cute version. VFX must be on the creature itself (trails, glowing eyes, footstep dust, embers, and so on), never on its surroundings, and shouldn't always be "things falling off its head".

## Docs
- Spec: `docs/2026-09-30-creatures-hatching-design.md`
- Plan (9 tasks): `docs/2026-09-30-creatures-hatching-plan.md`
- Progress ledger: `docs/progress.md`

## Done so far in Studio
- Task 1: `ReplicatedStorage.BaseConfig` and `ReplicatedStorage.CreatureConfig` (roster, odds 50/28/15/7 and 35/25/17/12/7/4, KG luck, tier). Tested.
- Tasks 2 to 4: my own Blender models of all 14 (the `blender\` folder: creature_kit.py, grass.py, water.py, thunder.py, combine.py). They're imported, rigged with `ReplicatedStorage.CreatureRig` (Motor6D and RestC0 attributes) and live in `ReplicatedStorage.CreatureModels`. **BUT they're the cute style, so they will be REPLACED by the Claude Design fierce models below.**
- NOT started: Task 5 (BaseEggs server: place, hatch, save), 6 (EggPlaceClient ghost), 7 (HatchClient animation), 8 (BasePets and PetAnimator), 9 (showcase). No existing scripts were modified.

## Claude Design models (the fierce versions the user wants)
Claude Design (claude.ai/design, "3D object" template) exports **only OBJ+MTL or GLB** (the GLB carries the animation clips). Keep prompts simple and realistic. A generation takes about 5 to 8 min. The user's Claude Design account has a session usage limit (it hit it once, and the limit resets after a few hours).
Downloads from the app's browser pane land in `~/Downloads` automatically. Copy them into `claude_design\<Name>\` with `claude_design\save_dl.sh <Name>` (run `touch ~/.dl_marker` before clicking the downloads). Buttons in the viewer: "Download OBJ + MTL" and "Download GLB" (bottom right).

### Saved (in claude_design\)
| Creature | Folder | Notes |
|---|---|---|
| Vine Serpent (fierce thorny viper) | `claude_design\VineSerpent` | 2,394 tris, Idle+Slither, spore trail |
| Kraken (fierce red, the user's original look) | `claude_design\Kraken` | 8,497 tris, 69 parts (heavy), Idle+Swim, includes KrakenAnimate.server.lua |
| (old cute) MossbackTortoise, ForestFawn, TreantSprout | their folders | OUTDATED, replace with the v2 downloads below |

### Made but NOT downloaded yet (download OBJ+MTL and GLB)
| Creature | Project URL |
|---|---|
| Mossback Tortoise v2 (armoured beast), 2,498 tris, Idle+Walk | https://claude.ai/design/p/77e0fba4-ea42-48c6-b8ac-549326afc1f4?file=Mossback+Tortoise+v2.html |
| Forest Stag (was Forest Fawn), 2,900 tris, Idle+Walk+IdleRub | https://claude.ai/design/p/af264173-a94e-408f-91f3-321fc7785828?file=Forest+Fawn.html |
| Treant (angry, amber glow), 2,424 tris, Idle+Walk | https://claude.ai/design/p/7ead5b18-8d16-4440-9872-3b7642d3291f?file=Treant.html |
| Sea Turtle Warrior, 2,123 tris, Idle+Walk | https://claude.ai/design/p/8723402e-76b1-4dfb-bde9-ddb0e1935c57?file=Sea+Turtle.html |
| Vine Serpent (already saved above) | https://claude.ai/design/p/dee4b379-2bdf-4379-9e36-b962a87bbee9 |
| Kraken (already saved above) | https://claude.ai/design/p/ec043553-e9e7-4ae8-8561-76e3d90fb1a0 |

### Still to generate in Claude Design (fierce style)
1. **Kappa**: fierce river demon, spiked shell, fanged beak, seaweed hair around the water dish. Parts Body/Head/ArmL/ArmR/LegL/LegR. Idle+Walk. VFX: dripping water, wet footprint trail. (The prompt was typed but NOT sent, because the page was still loading.)
2. **Hippocampus**: armoured sea-horse steed, fin mane, curled fish tail. Swim/float. VFX: bubble/water trail.
3. **Spark Fox**: sharp lightning fox, zigzag tail. VFX: electric sparks trailing from its tail and paws.
4. **Raijū**: thunder wolf-beast with a lightning mane. VFX: crackling arcs, glowing eyes.
5. **Cloud Ram / Storm Ram**: storm-cloud wool, heavy gold curled horns. VFX: small lightning flickers in the wool.
6. **Thunder Bull**: massive dark bull, glowing bolt markings. VFX: sparks from the hooves when it stomps.
7. **Thunderbird**: huge storm eagle. Fly animation. VFX: lightning trail off its wingtips.
8. **Storm Wyvern**: dragon with bolt-tipped tail. Fly animation. VFX: electric trail and glowing eyes.

Prompt template that worked: "Model a 3D object: "<Name>" creature for my Roblox game (<Area> area): <fierce look description>. Stylized but menacing and cool, not cute. Build it from separate named parts (<parts>) so I can animate it in Roblox Studio. Animations: "Idle" (...) and "Walk"/"Fly"/"Swim" (...). VFX on the creature only: <trail/glow>. No ground or background. Keep it Roblox-friendly: under ~3,000 triangles, small textures (max 1024px). Export as OBJ+MTL and GLB."
Tip: on claude.ai/design, wait about 3 s after the page loads, then click the "3D object" template and the prompt box, type, and press Enter.

## Next steps after all the models are downloaded
1. Import each OBJ into Studio. For per-part colours, use the Blender palette pipeline (memory: roblox-colored-mesh-import). Rebuild it as named MeshParts and rig with `CreatureRig` (a joints-from-parts approach like `blender\combine.py` + the rig_import script). Replace the models in `ReplicatedStorage.CreatureModels` (same names as `CreatureConfig`). Note: Roblox usually drops GLB animation clips, so animation will be procedural in `PetAnimator` using the named parts, with the GLB clips as reference.
2. Rebuild each creature's viewer VFX as ParticleEmitters/Trails attached to its parts.
3. Carry on with plan Tasks 5 to 9 (placing, hatching, hatch animation, wandering, showcase).

## UPDATE 2026-09-30 afternoon: all remaining models generated (NOTHING downloaded yet)
The user said no downloads until they are home. The full list of what to download is in `claude_design\TO_SAVE.md`.
To download: Mossback v2, Forest Stag, Treant, Sea Turtle Warrior, Kappa, Spark Fox, Raiju, Storm Ram, Thunder Bull, Thunderbird, Storm Wyvern.
Hippocampus: two attempts, both rejected as ugly. The user said SKIP it for now.
Prompt lessons are in TO_SAVE.md: one generation at a time, a new project each, a concrete sculpt spec, and "one pass, skip verification".

## UPDATE 2026-09-30 evening: switched to MESHY (real 3D models). Claude Design is abandoned except the 4 keepers
- Keepers from Claude Design: Forest Stag (Fawn), Vine Serpent, Treant, Mossback.
- Meshy prompts (Preview + Texture) for all 38 creatures: `meshy\MESHY_PROMPTS.md`. Grass area = the 4 keepers.
- API runner: `meshy\meshy_run.py` (key in `meshy\meshy_key.txt`, never print it). About 30 credits per creature (preview + refine). Output goes to `~\Downloads\Meshy\<Name>.glb/.fbx/.png` (the png is an alpha thumbnail, usable as a UI icon). Task ids are in `meshy\meshy_tasks.json`.
- The user made Kraken (file `krakens.*`), Sea Turtle Warrior, Kappa, Hippocampus, Spark Fox, Raiju, Storm Ram and Thunder Bull by hand. The API made Thunderbird through Qilin (29).
- Celestial Dragon: done 2026-10-01. All 38 creatures now exist. Meshy balance is 40 credits.
- Overview picture: `meshy\overview.png`. Possible redos: Magma Salamander (came out upright/bipedal), Wraith Hound (thin), Qilin (small/thin), Star Pegasus (pale/toy-like), Lunar Jackal (humanoid Anubis).
- Next: import into Studio. They're single meshes (no named parts), so split them into parts in Blender for the procedural PetAnimator, or use Roblox auto-setup. Then plan Tasks 5 to 9.


## UPDATE 2026-10-01: creatures are IN THE GAME (hatching + pets work)
### Models (41 of 42 in ReplicatedStorage.CreatureModels)
- 38 Meshy models + Forest Stag, Mossback Tortoise and Vine Serpent (Claude Design). **Treant is missing.** Its download is stuck behind a Save dialog in the Claude app (cancel the Forest Stag one, then Save the Treant one as `~/Downloads/Treant.glb`).
- Pipeline (`SLINGSHOT Creatures\rig\`):
  1. Claude Design GLBs only: `blender -b -P prep_cd.py -- <in.glb> rig/src/<Name>.glb` (joins the parts and bakes the colours into a palette texture).
  2. `python run_all.py <Name>` renders posed review sheets (out/review*.png); `python run_all.py --export <Name>` writes out/<Name>.fbx. The rig type per creature is in `creatures.py`.
  3. Studio: Import Queue → add the FBX → Import. Then normalise it like the others: Body MeshPart + invisible Root part at the feet (PrimaryPart, facing -Z), scale to its Height, attributes DisplayName/Rig/Motion/Height, move it into ReplicatedStorage.CreatureModels. Meshy imports come in lying down: PivotTo(CFrame.fromMatrix(p, X, Z, -Y)) first. Claude Design imports come in upright, so skip that step.
- Animation: `ReplicatedStorage.CreatureAnimator` drives Bone.Transform by rig type (quad/biped/bird/wingquad/multileg/serpent/snake/jelly/kraken/moth/seahorse): walk, fly, swim, slither, idle, roar.

### Gameplay scripts
- `ServerScriptService.BaseHatchery`: placing (rules: inside the fence, spacing, slots, owns the egg), hatch timer by KG, FREE "Skip Hatch" prompt (TODO Robux developer product), hatching, pet wandering planner, saving in the player attribute BaseData (PlayerData saves it). In Studio, `ServerStorage.HatcheryDebug:Invoke("give"/"place"/"hatchAll"/"force", ...)` is available for tests.
- `StarterPlayerScripts.EggPlaceClient`: ghost egg + click to place.
- `StarterPlayerScripts.HatchClient`: egg timers, hatch animation, CUTSCENE for lucky millions eggs.
- `StarterPlayerScripts.PetAnimator`: draws and animates pets locally.
- `ReplicatedStorage.CreatureConfig`: rosters for all 6 areas, odds, hatchSeconds, isCinematic.
- Old cute models were moved to ServerStorage._OldCreatureModels (backup).

### Ideas / open points
- A pet cap per base (pets don't use slots yet). Pets walk through eggs. Hatch sounds aren't added yet (Creator Store).
- Possible redos: Magma Salamander (upright), Wraith Hound (thin), Qilin, Star Pegasus, Lunar Jackal (humanoid). Meshy has 40 credits left.

## UPDATE 2026-10-01 (later): ANIMATION SYSTEM v2 (Blender-authored clips)
The user said the old animations looked terrible (sinking into the ground, ugly flying and hopping). Everything was rebuilt:
- **anim/** (new): `author.py` runs in Blender after `rig/rigger.py` and builds the clips per creature with real 2-bone IK
  (planted feet never slide or sink): idle, walk, roar, personality acts (sniff/shake/stomp/stretch/look/crouch/pound/twitch/wingstretch),
  flyers fly/glide/takeoff/land, swimmers swim, snakes slither/strike. Personality per creature is in `anim/profiles.py`.
  Output: `anim/blend/<Name>.blend` (open to see/tweak the actions), `anim/out/<Name>.json`, `anim/preview/<Name>.png` (contact sheets).
- Rebuild: `python anim/run_anim.py [--preview] [names]` → `python anim/to_luau.py` → serve `anim/luau` on 127.0.0.1:8765 and
  in Studio set HttpEnabled=true, GetAsync each `<Name>.lua` into `ReplicatedStorage.CreatureClips.<Name>` (ModuleScripts), then set HttpEnabled back to false.
  Also recompute the `WalkSpeed` attribute on CreatureModels (stride*k/len*1.1).
- Roblox: `ReplicatedStorage.CreatureAnimator` v2 = clip player (blend loops by speed, walk phase driven by the distance moved,
  one-shots via anim:play). `PetAnimator` v2 = movement (turn-on-the-spot, eased walking, Hermite flight curves with no mid-air stops,
  banking/pitch, takeoff/land timed to the clip events, idle acts, roars, look at the player). The old versions are in ServerStorage._CreatureAnimator_v1 / _PetAnimator_v1.
- Server `BaseHatchery`: walkers use the template's `WalkSpeed`×scale; flights = slow climb-out + 2-5 cruise waypoints + slow landing.
- Rig v2 (`rig/rigger.py`): a tail is never skinned to a leg; `creatures.FEET` holds hand-placed feet (Flame Lynx, Shade Panther, Shadow Mantis);
  Spark Fox is now `biped` (stands upright) and Void Dragon is `bird`. 16 models were re-imported with v2 rigs (the originals are in ServerStorage._OldCreatureModels_rigv1).
  `rigger.py --v1` reproduces the old weights. Coordinate mapping: Blender (x,y,z) → Roblox root space (-x, z, y)·k.
- Known leftovers: Sea Turtle has 3 legs (one flipper is raised in the model). Creatures still marked CALM (legs kept calm in FK poses):
  Mossback, Sea Turtle, Cinder Scorpion, Inferno Drake, Celestial Dragon. Treant still missing.
- 2026-10-01 follow-up: flyers lean their whole body forward in flight (auto `LEAN` from the spine angle, `lean` override in profiles; Griffin 0.9),
  legs trail/tuck and pump with the wingbeat, glide looks around. Flyers now WALK on the ground (walk clips + WalkSpeed) and fly only every 2-3 min
  (BaseHatchery `nextFlight`). The 38 Meshy models were scaled ×1.25 (attribute SizeBoosted; Height and WalkSpeed updated); the Claude Design 3
  (ForestStag, MossbackTortoise, VineSerpent) were not. MAX_PET_LENGTH 16→20 (server + HatchClient).
