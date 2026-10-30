# PetsV3 remake (Steal-an-Egg block style) - progress 2026-10-08

User rules: block style the user approved (Raiju), built BIG (real proportions), NO GLOW, every pet its own model +
its own idle / roar / ONE signature act (no shared motifs, NO head shakes), flyers flap with wings + legs pump
(wing3 rules: root-axis flap, hinge fold, small sweeps), 0 collisions (blockkit.overlap_report with check_pairs /
joints), audits clean.

Per pet (Blender MCP): `R3 = runpy.run_path(PetsV3/run3.py)`; `R3["model"](N)` -> `python sheet3.py N model_ 2`;
`R3["full"](N, pose_picks=[...])` + `overlap_report(k, m.check_pairs(), step=1, joints=m.joints() if any)` ->
`python sheet3.py N pose_tq 5`; `R3["export"]()` -> C:\cdimp\N.fbx + N/N_meta.json + N_bu.json + N/N.lua.
Studio (later, batch): Import FBX (Keep Zero Influence Bones), `python mkrbxmx.py C:/cdimp/PetsV2Clips.rbxmx A B..`
-> File > Import Roblox Model, `python setup3.py A B .. > out.lua` -> execute_luau; portraits `python icon3.py A B`.

| Pet | spec | exported | in Studio | signature |
|---|---|---|---|---|
| Raiju | done | done | done (V3) | act_thunderflip |
| StormWyvern | done | done | done (V3) | act_thunderclap |
| ThunderBull | done | done | - | act_charge |
| MossbackTortoise | done | done | - | act_shellspin |
| ForestStag | done | done | - | act_pronk |
| Treant | done | done | - | act_branchlash |
| Kappa | done | done | - | act_sumo |
| SeaTurtleWarrior | done | done | - | act_twirl |
| Kraken | done | done | - | act_crush |
| MoltenBoar | done | done | - | act_wallow |
| LavaGolem | done | done | - | act_pound |
| Cerberus | done | done | - | act_triplesnap |
| ShadePanther | done | done | - | act_pounce |
| NightmareStallion | | | | |
| BlackDragon | | | | |
| SolarLion | | | | |
| Griffin | | | | |
| CelestialDragon | | | | |
| Ivonrath | | | | |
| PharaohAsparuh | | | | |
| Cvetibara | | | | |

Signatures used so far (don't repeat): barrel roll, wing thunderclap leap, scrape+lunge+horn toss, shell spin on
the ground, stotting pronks, telescoping arm lash+grab+chest thumps, sumo shiko stomps+palm thrusts, trident
helicopter twirl+slam, tentacle ship-crusher drum slams, lava wallow (roll on back, legs kick), ground pound (2 fists + jump
smash), triple snap (3 heads bite in turn + pounce), stalk + butt wiggle + airborne pounce. Roars used: howl, lunge roar, bellow, snap-hiss, bugle, timber roar (arms spread), kappa screech (claws wide),
battle cry (fist to sky), kraken rise (tentacle crown), squeal-roar (mane erupts), flex roar
(double biceps), 3-head howl chorus, hiss (arched back).
LESSON: head pivot at the THROAT (low/back) or head-down swings the head's back corner into the chest.
Idles used: scan+pant (wolf), survey+wing stretch (wyvern), cud chew+tail flies (bull), neck stretch+graze+tree wind
(tortoise), alert freeze+alarm stomp+browse-up (stag).

## PRO pass (2026-10-08, owner: "LOW QUALITY", "make another agent to approve or decline")
- Art director -> STYLE_BIBLE.md; gate reviewer -> _review/<Name>_verdict.md + _review/LESSONS_ALL_PETS.md.
- Kit rebuilt to the bible (blockkit.py): role rounding + smooth shading, brick-grid plates with fake light,
  B.face_eyes, HEAD_XF translation, quaternion sign continuity (BlockPet.finish). Exporter: bible AO, normals OFF.
- Headless parallel pipeline: _tools/headless_model.py | headless_full.py [export] | collide_where.py.
- Raiju: rebuilt, gate APPROVED 8/10 (round 3), collision_free step 1, exported, imported in Studio (pilot).
- Builders: A Mossback/Stag/Treant/Kappa, B SeaTurtle/Kraken/ThunderBull/StormWyvern,
  C MoltenBoar/LavaGolem/Cerberus/ShadePanther, D Stallion/BlackDragon/SolarLion/Griffin,
  E new specs Cvetibara/Ivonrath/PharaohAsparuh/CelestialDragon.
- Studio: setup3.py zeroes the importer's +90 X PivotOffset (pets lay on their side); CreatureVFX particle
  presets (ReplicatedStorage.CreatureVFX, attached by PetAnimator); backup ServerStorage._Backup_PetsV3_prePro.

## FIERCE pass (2026-10-09, owner approved the storm-wolf Raiju: "The design is fire!")
Owner asks: stomach less like a BOX (done on Raiju), subagents review + plan, ALL models into the game, look cool at
every size (10K..10M) without becoming leg-only giants, EVERY model its own unique behaviour-based signature act.
- Kit: Blocks(plates=False) + bk.stud_skin(k, PITCH) (2-channel stud tile: R multiply, G additive rim), stud bake in
  petkit.bake_and_export(stud=...) with a visible-faces-only tight UV pack (_uv_visible_only), ao_mix (0.70, 0.30).
- Roblox renders colours ~0.6x darker than the Blender preview (ColorCorrection contrast +0.2, shadows near black):
  body colours must be bright (Raiju FUR (80,102,182)). MeshPart.Color doesn't tint a TextureID mesh.
- Size curve (ReplicatedStorage.CreatureConfig): SIZE_CURVE {{0,.8},{3,1.25},{4,1.45},{5,1.65},{6,1.9},{7,2.2}},
  MAX_PET_LENGTH 36 (was up to x4 / 44). Raiju 10M = 17.6 studs tall. Old source in ServerStorage._Backup_PetsV3_chibi.
- Studio: ServerStorage.PetSetup3 module = setup3.py as a module: require(PetSetup3:Clone())({cfg,...}).
  Backup of all chibi models/clips/VFX: ServerStorage._Backup_PetsV3_chibi.
- Agents: art director (FIERCE_PLAN.md), builders A Mossback/Stag/Treant/Kappa, B SeaTurtle/Kraken/ThunderBull/
  StormWyvern, C MoltenBoar/LavaGolem/Cerberus/ShadePanther, D Stallion/BlackDragon/SolarLion/Griffin,
  E CelestialDragon/Cvetibara/Ivonrath/PharaohAsparuh; reviewer gate = _tools/reviewer_fierce.md.
- Raiju: rebuilt, collision-free, exported + imported (pilot); re-export with the final palette in the batch import.

### FIERCE pass - final status (2026-10-09 ~20:50)
- ALL 21 fierce pets are in ReplicatedStorage.CreatureModels (Style="Fierce") with matching CreatureClips, VFX + size
  auras (CreatureVFX.attachAura: >=100K motes, >=1M haze, >=5M feet dust) and new Index portraits (IndexConfig.PORTRAITS).
- Final gate: every pet APPROVE (8-8.5). PharaohAsparuh was REVISE 7.5 -> fixed (belly tufts removed, haunch tufts ->
  flat fur locks, walk tail sweeps back instead of a flagpole), checked in-game.
- Polish pass after the gate (reviewer's optional notes):
  geometry + re-import: ThunderBull (rounded hump), NightmareStallion (fangs), MossbackTortoise (spiked tail),
  LavaGolem (studded brow), Cerberus (snake tail clear of the ears), ShadePanther (crystals laid back), PharaohAsparuh;
  clips only: Kraken (deeper wrap), StormWyvern (biggest 3rd clap + clap events), SolarLion (rays stay rooted),
  Griffin (forward tent 31, 38 collides), Treant (arms down the sides), Kappa (higher shiko), MoltenBoar (lies in the
  mud), ShadePanther (deeper bow), Ivonrath (head higher), Cvetibara (wings folded flat), CelestialDragon (tail arc + jaw snap).
  Portraits re-made for the 7 geometry pets.
- In-game check (Studio Play, client zoo of all 21): every pet builds, every clip plays, acts/walk/fly/swim OK, no
  console errors. 10M Stag in a base = 24 studs tall incl. antlers, whole body visible.
- Cleanup: TestFreshSave=false, 43 studiotest_ keys removed from PlayerData_v3, no stray models in Workspace.
- NOT saved/published - the owner does that.
