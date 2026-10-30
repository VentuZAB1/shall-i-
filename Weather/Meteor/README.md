# Meteor Shower: Meteor / MeteorBig / MeteorChunk models + icon

Models and HUD icon for the SLINGSHOT "Meteor Shower" weather (spec `docs/specs/2026-10-10-weather-meteor-design.md`,
plan + ledger `docs/plans/2026-10-10-weather-meteor.md`). **Imported into Studio 2026-10-10** (creator ZAB Studio).


## HQ models (2026-10-11): what is live now
The owner on the first models: "they are low polygon, we need high quality, it looks like trash" (and "also the storm
models fix"). Everything was rebuilt with a game-art pipeline in `HQ/`: a dense procedural sculpt, a game mesh within
Roblox's 20k-tris-per-MeshPart limit, and baked PBR maps (colour x AO, tangent normal, roughness) that the 3D importer turns
into a **SurfaceAppearance**. All parts are set to **RenderFidelity Precise**: on "Automatic", Roblox swaps in a
simplified mesh at range, which made the old 8k-tri cloud look even blockier. Still no neon / emissive: the magma
cracks are albedo only, and every glow is VFX.

| File (`HQ/`) | What it is |
|---|---|
| `build_hq.py` | The rocks. Sculpt: icosphere (1.3M tris for MeteorBig) with fracture faces (smooth-min planes), domain-warped Voronoi crack network with heated rims, craters, melt-flow streaks on the flanks, grain. Bakes per rock. Steps `rocks \| render \| export \| all` |
| `build_storm_hq.py` | The cloud. A signed-distance field from 3 levels of billows (~200 storm masses, 1,100 billows, 6,500 cauliflower puffs; Geometry Nodes Points to SDF Grid), cut flat by a rough storm base with mammatus lobes (SDF intersect), creases filleted, 2.1M-tri sculpt, decimated and split into 4 pieces of 19k tris, each with its own 1024 maps. Steps `build \| render \| export \| all` |
| `meteor_hq.blend`, `storm_hq.blend` | Sources |
| `*_albedo / _normal / _rough / _ao / _hot.png` | Baked maps (`_hot` = the crack mask that keeps AO off the glowing cracks) |
| `review_*.png`, `review_sheet.png`, `storm_hq_*.png`, `storm_hq_sheet.png` | Review renders |
| `ingame_cutscene_hq.png` | In-game check: the storm forms, its belly glows, MeteorBig tears out, the barrage, the title |

Exports go to `C:\cdimp\MeteorHQ.fbx`, `MeteorBigHQ.fbx`, `MeteorChunkHQ.fbx`, `StormCloudHQ.fbx` (maps embedded).
Import: Home > Import 3D, creator **ZAB Studio**; then zero each MeshPart's PivotOffset, set Precise, and swap it into
`ReplicatedStorage.WeatherAssets.Meteor` under the same name.

| In Studio | Size (studs) | Game tris | Mesh / ColorMap / NormalMap / RoughnessMap |
|---|---|---|---|
| `Meteor` | 6.9 x 6.1 x 8.0 | 7,000 | 120035068553740 / 74284294742054 / 118675021137583 / 137182064290382 |
| `MeteorBig` (cutscene) | 66.1 x 56.6 x 69.7 | 19,500 | 77274685381157 / 127574996437996 / 96750297902615 / 81797328313430 |
| `MeteorChunk` (debris) | 2.3 x 1.6 x 2.5 | 1,500 | 84042723802074 / 125836995303308 / 120965928609035 / 125677787999048 |
| `StormCloud` = **Model** of `StormCloud1-4` | 207 x 93 x 405 overall | 4 x 19,000 | 1: 86073558249350 / 97884464773493 / 115067997372219; 2: 74611469249162 / 113336233241885 / 74151834401514; 3: 126434673255310 / 82162330876224 / 120077396650249; 4: 104478576045628 / 88616561428065 / 104592829256304; shared roughness 87385172335346 |

- The cloud is a Model because one MeshPart can't hold more than 20k tris. `MeteorClient.makeCloud` makes an invisible
  core Part the size of the Model's bounding box (the VFX attachments and the rumble hang on it). The pieces follow the
  core every frame, and are resized only while the cloud forms or dissolves.
- The cloud's flat base sits **10** studs above the mesh's bottom (`MeteorClient.POUCH`), and
  `WeatherConfig.TYPES.Meteor.cloudSize` = (207, 93, 405). The server uses `cloudSize` for where meteors leave the base.
- The cloud's colour ramp starts at warm charcoal sRGB (36, 32, 30), not near-black. In game, a belly at sRGB 10 read as
  a flat black ceiling with no lobes. Crevices are darkened by the baked AO (0.12 + 0.88 x AO^1.3).
- The old low-poly set (v1 below) is kept in `ServerStorage._Backup_MeteorV1` (Meteor, MeteorBig, MeteorChunk, StormCloud).

# v1 (2026-10-10, superseded by the HQ models above)

## Files
| File | What it is |
|---|---|
| `build_meteor.py` | Builds everything procedurally; re-run it to tweak (usage in the header) |
| `meteor_models.blend` | Source file (`.blend1` = the previous save) |
| `Meteors.fbx` | Export: the three rocks, palette PNG embedded |
| `meteor_palette.png` | 64x64 palette, 16 px cells |
| `Meteor_hot / _back.png`, `MeteorBig_*`, `MeteorChunk_*` | Review renders: leading (hot) face and back |
| `Meteor_lineup.png` | Size lineup |
| `icon/meteor_icon_raw.png` | Icon render: rock + flame trail (the trail is render-only, never exported) |
| `icon/meteor_icon.png` | Final icon: black outline like the saucer icon, specks removed |

Re-run (headless, does not touch an open Blender):
```
"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python build_meteor.py -- all
```
Steps: `build | render | export | icon | all`.

## In Studio
| What | Where / id |
|---|---|
| `Meteor` (7.5 x 7.7 x 6.7 studs, 844 tris) | `ReplicatedStorage.WeatherAssets.Meteor.Meteor`, mesh `rbxassetid://122367153647511` |
| `MeteorBig` (66 x 73.5 x 56.5 studs, 2,740 tris, cutscene only) | `...Meteor.MeteorBig`, mesh `rbxassetid://130414726440643` |
| `MeteorChunk` (1.8 x 2.4 x 1.7 studs, 20 tris, debris) | `...Meteor.MeteorChunk`, mesh `rbxassetid://111257225977182` |
| Palette texture | `rbxassetid://120339252456726` |
| HUD icon | `rbxassetid://84492648795778` (`WeatherConfig.TYPES.Meteor.icon`) |

- All parts: Anchored, CanCollide/CanQuery/CanTouch off, SmoothPlastic, PivotOffset identity (the importer's +90 deg X
  turn was zeroed).
- The hot leading face points along Roblox -Z (LookVector): the client flies a meteor with
  `CFrame.lookAt(pos, pos + velocity)`, so the glowing side always leads.
- **No neon / emissive** (owner rule). The magma cracks are inset geometry in palette colours; all glow, fire, smoke and
  sparks come from VFX Studio templates in `ReplicatedStorage.WeatherFX`: `MeteorTrail`, `MeteorImpact`,
  `MeteorScorch`, `MeteorRing`, `MeteorAura`.

## Storm cloud (added 2026-10-11, owner: "a black dark cloud hovering over it, thunder around it, the meteors falling from there")
| What | Where / id |
|---|---|
| `build_cloud.py` | Builds it: metaball cumulonimbus bank, flattened base with hanging mammatus pouches, voxel remesh, decimate to 8,000 tris, height-gradient UVs. Steps `build \| render \| export \| all` (same headless command as above) |
| `storm_cloud.blend`, `storm_cloud_gradient.png`, `StormCloud.fbx` | Source, gradient texture (near-black charcoal underside to dark grey tops), export |
| `storm_player_view / _from_below / _side / _far.png` | Review renders over a 120 x 400 runway with 40-stud walls |
| `StormCloud` (190 x 87 x 389 studs, 8,000 tris) | `ReplicatedStorage.WeatherAssets.Meteor.StormCloud`, mesh `rbxassetid://90058592416808`, texture `rbxassetid://123372180614349` (ZAB Studio) |
| Its effects (VFX Studio textures) | `WeatherFX.MeteorCloud` (Churn: soft billows, Smoke #4 `4510290214`; Fringe: ragged scud, Smoke #14 `14201973571`, + falling embers), `WeatherFX.MeteorLightning` (bolts: Lightning #7 `1463939561` / #10 `11736666805`; spider flash #6 `332491482`; glow), `WeatherFX.MeteorCloudBurst` (Smoke #5 `243474653` puffs, fireball, glow, light) |

- The client hangs it `cloudBase` (85) studs over the floor of the weather's area. Its flat base sits 7 studs above the mesh's bottom; the pouches hang lower.
- It casts a shadow and glides between areas.
- The ramp is neutral-warm on purpose. A cooler ramp read navy under Roblox's blue sky light, and the owner wants it black.
- The first billow texture (Smoke #3, a cumulus puff) had ink outlines, which looked like bubbles on the cloud. It was replaced with the soft #4.

## Palette (sRGB; cell i = column i % 4, row i // 4, row 0 = bottom of the PNG)
| # | Name | Hex | Used for |
|---|---|---|---|
| 0 | CHAR | `#1C1614` | crater floors |
| 1 | BASALT_D | `#2E2522` | dark basalt |
| 2 | BASALT | `#463935` | basalt |
| 3 | ASH | `#655650` | light ash ridges |
| 4 | SCORCH | `#5A2E1E` | heat-scorched leading face |
| 5 | EMBER | `#7E2410` | crack walls |
| 6 | MAGMA_R | `#C9361A` | magma red |
| 7 | MAGMA_O | `#FF7A1F` | magma orange (the weather's colour) |
| 8 | MAGMA_Y | `#FFC247` | magma yellow core |
| 9 | HOTWHITE | `#FFE9B0` | hottest specks (leading face) |
| 10 | RUST | `#7A4A36` | iron flecks |
| 11 | SOOT | `#241E1D` | soot band behind the hot face |

## FBX export
Same settings as `Weather/UFO/build_ufo.py` (`global_scale=0.01`, `axis_forward="-Z"`, `axis_up="Y"`, embedded
palette, FACE smoothing, no armature, no animation). Studio import: Home > Import 3D > `Meteors.fbx`, creator
**ZAB Studio** (the place is group-owned).
