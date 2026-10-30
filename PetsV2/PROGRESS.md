# PetsV2 remake - progress (overnight run 2026-10-08)

Pipeline: `pets/<Name>.py` (model/rig/anim) -> Blender MCP `runpy.run_path(run.py)`: `R["model"](name)`,
`R["full"](name, pose_picks)`, `R["export"]()` -> `C:\cdimp\<Name>.fbx` + `<Name>/<Name>.lua` + `_meta.json` + portrait.
Studio: Home > Import (FBX, tick Keep Zero Influence Bones) ; clips: `python mkrbxmx.py C:/cdimp/PetsV2Clips.rbxmx A B ..`
then File > Import Roblox Model (lands in ServerStorage.PetsV2Clips) ; `python setup_lua.py <Name>` -> execute_luau
(scales, Neon glow, attributes, moves model to CreatureModels + clips to CreatureClips, replaces old).
Portrait: `python icon.py <Name>` then upload_image http://localhost:8765/<Name>/<Name>_icon.png (http.server in PetsV2).
Asset ids: asset_ids.json. Old models: ServerStorage._Backup_PetsV1.

| Pet | Blender | Studio model | clips | portrait |
|---|---|---|---|---|
| Ivonrath | done | done | done (v2 twist) | done |
| PharaohAsparuh | done | done | done | done |
| Cvetibara | v2 clips (FriendPets/Cvetibara/cvetibara_v2.py) | (v1 model kept) | done | (v1) |
| MossbackTortoise, ForestStag, Treant, Kappa, SeaTurtleWarrior, Kraken | done | done | done | done (IndexConfig updated) |
| Raiju, ThunderBull, StormWyvern, MoltenBoar, LavaGolem, Cerberus | done | done | done | done |
| ShadePanther, NightmareStallion, BlackDragon, SolarLion, Griffin, CelestialDragon | done | done | done | done |

Code done: CreatureConfig (friend pets = 4th SECRET per egg, ODDS[4] 57/27/12/4), IndexConfig (versions, isClaimed,
claims, totalClaims, discovered, portraits Ivonrath + Asparuh), IndexServer (re-claim), IndexClient (4 cards, SECRET badge,
CLAIM AGAIN). Logic test passed in Edit (19/19). Still to do: play test.

Play test #1 (9 pets in base, TestFreshSave): all built + animated, no console errors. TestFreshSave set back to false.
Helpers: pets/_common.py (plant, chain, Flight class w/ takeoff/land events, biped_walk, quad_walk, key_axis, crack).

## Finished 2026-10-08 ~06:50
- All 12 remaining models imported (batch Import Queue, Keep Zero Influence Bones ticked per row), clips via rbxmx
  (NOTE: File > Import Roblox Model drops into the SELECTED service - this time Workspace; the setup script only looked
  in ServerStorage, so clips were moved by hand. Check `game:GetDescendants()` for PetsV2Clips after import).
- CreatureConfig: BlackDragon -> Fly. Flyers: StormWyvern, Ivonrath, BlackDragon, Griffin, CelestialDragon, Cvetibara.
- IndexConfig.PORTRAITS: all 21 = PetsV2 portraits (asset_ids.json). Old ids in ServerStorage._Backup_PetsV1.IndexConfig.
- Clip bones vs model bones: 21/21 match. Play test #2 (TestFreshSave): 12 new pets hatched, all animate, all 4 flyers
  take off / fly at 10-15 studs / land; Index legacy save -> refuses claim until the secret is found, CLAIM AGAIN works,
  IndexBonus 0.30 -> 0.35 -> 0.45, potions given, no double-claim; secret odds 4.0% / 4.0% / 3.8% over 20k rolls.
- Cleanup: TestFreshSave false, 38 studiotest_ keys removed, 10/10 real saves intact, http.server stopped.
- Overview image: ALL_PETS_V2.png
