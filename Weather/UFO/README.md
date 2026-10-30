# UFO Invasion: Mothership + Saucer models

These are the models for the SLINGSHOT weather event. They are not imported into Studio yet; the owner approves the look first.

## Files
| File | What it is |
|---|---|
| `ufo_models.blend` | Source file with 3 scenes: `Mothership`, `Saucer`, `Lineup` (the lineup uses collection instances plus a 5-stud capsule) |
| `build_ufo.py` | Builds everything procedurally, so you can tweak it and re-run it (usage is in the header) |
| `Mothership.fbx`, `Saucer.fbx` | Export files, with the palette PNG embedded |
| `ufo_palette.png` | 64x64 palette, 16 px cells (the same file is embedded in both FBX files) |
| `Mothership_front / _threequarter_below / _underside.png` | Mothership renders (Eevee, back faces culled like Roblox) |
| `Mothership_doors_open.png` | Extra render: both belly doors swung 85 deg about their hinges (checks the pivots) |
| `Saucer_front / _threequarter_below / _underside.png` | Saucer renders (doors closed) |
| `Saucer_doors_open.png` | Saucer belly doors swung 85 deg: green emitter lens in the bay |
| `UFO_lineup.png` | Orthographic lineup (exact scale): mothership, saucer, and a 5-stud player capsule |

Re-run inside Blender (MCP):
```python
import runpy; U = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Weather\UFO\build_ufo.py")
U["build_all"](); U["render_all"](); U["export_all"](); U["report"](); U["check_normals"]()
# saucer only (leaves the approved Mothership and Mothership.fbx alone):
U["rebuild_saucer"](); U["render_all"](models=("Saucer",)); U["export_model"]("Saucer")
```
Blender object names must be unique, so in the .blend the objects carry an `MS_` or `SC_` prefix. `export_model()` strips the prefix temporarily, which makes the FBX node names (and so the MeshPart names) exactly the ones listed below.

## Units / axes
- 1 Blender metre = 1 Roblox stud.
- Blender Z (up) becomes Roblox Y (up). Blender (x, y, z) maps to Roblox (x, z, -y).
- Each model's bounding-box centre is at the origin.

## Mothership: 120 x 42.6 x 120 studs (W x H x D)
The 42.6 height includes the antenna; the hull disc alone is 21.6 tall. Total: 18,932 tris, all under the 20k-per-MeshPart limit.

| MeshPart | Tris | Size (studs) | Pivot / notes |
|---|---|---|---|
| `Hull` | 7,916 | 120 x 21.6 x 120 | Model centre. Includes the 8 underside thrusters, 8 girders, the hazard ring, the bay walls and ceiling, and the window slots |
| `LightRing` | 6,768 | 117.9 x 3.0 x 117.9 | 24 green pods on the rim's lower chamfer. Origin on the vertical axis at Y = -13.19. **Spins about Y.** Rotationally symmetric, so its bbox centre is on the axis too |
| `Bridge` | 2,592 | 38.6 x 13.3 x 38.6 | Model centre. Command deck with a window band, plus a ribbed teal glass dome |
| `BellyDoorL` | 588 | 18.55 x 0.92 x 37.1 | Hinge (origin) at (-18.67, -20.285, 0), i.e. the door's outer edge at its top face. Hinge axis is Roblox Z (Blender Y) |
| `BellyDoorR` | 588 | 18.55 x 0.92 x 37.1 | Hinge (origin) at (+18.67, -20.285, 0), mirrored |
| `Antenna` | 480 | 3 x 8.6 x 3 | Model centre. Mast with a green ball tip on top of the dome |
| `BeamOrigin` (Empty) | - | - | (0, -21.285, 0): centre of the belly opening, in the frame's bottom plane. Arrow points down |

- **Belly opening:** radius 18.8 (diameter 37.6, which is 31% of the ship). The bay is 8.1 studs deep (ceiling at Y = -13.19) and has 4 clamps and a green hatch on the ceiling. Saucers are 16 x 6.25, so they fit.
- **Doors** are modelled CLOSED. Opening is a rotation about the hinge line, parallel to Roblox Z:
  - `BellyDoorL`: `CFrame.Angles(0, 0, -a)` swings its inner edge down.
  - `BellyDoorR`: `CFrame.Angles(0, 0, +a)`.
  - About 85 deg looks right; see `Mothership_doors_open.png`.
  - If the importer resets pivots to the bbox centre, the hinge sits at the door's outer bbox edge on its top face:
    - L: `PivotOffset = CFrame.new(-Size.X/2, Size.Y/2, 0)`
    - R: `PivotOffset = CFrame.new(Size.X/2, Size.Y/2, 0)`
  - The signs assume the FBX arrives upright. Verify once in Studio.

## Saucer: 16 x 6.25 x 16 studs (rev 2, 2026-10-10: opening belly doors)
Total: 7,722 tris.

| MeshPart | Tris | Size (studs) | Pivot / notes |
|---|---|---|---|
| `Hull` | 2,586 | 16 x 4.3 x 16 | Model centre. Disc with a dome collar, a green rim line, a belly collar and a frame around a round opening. Inside the opening: a dark bay with a dark-green band and a **green emitter lens** on the bay ceiling |
| `RimLights` | 3,000 | 15.3 x 0.94 x 15.3 | 12 green pods on the rim's lower chamfer. Origin on the axis at Y = -1.65. **Spins about Y** (symmetric) |
| `Dome` | 960 | 7.1 x 2.6 x 7.1 | Model centre. Dark teal glass with a cartoon highlight streak |
| `BellyDoorL` | 588 | 3.17 x 0.36 x 6.34 | Hinge (origin) at (-3.22, -2.725, 0), i.e. the door's outer edge at its top face. Hinge axis is Roblox Z |
| `BellyDoorR` | 588 | 3.17 x 0.36 x 6.34 | Hinge (origin) at (+3.22, -2.725, 0), mirrored |
| `BeamOrigin` (Empty) | - | - | (0, -3.125, 0): bottom centre of the opening (the frame's bottom plane, the lowest point of the closed ship). Arrow points down |

- **Belly opening:**
  - Radius 3.25 (diameter 6.5, about 40% of the saucer).
  - The bay is 1.75 deep (ceiling at Y = -1.375).
  - The emitter lens hangs from the ceiling. Its lowest point is (0, -1.875, 0); use that if the beam should start at the lens rather than at `BeamOrigin`.
- **Doors** are modelled CLOSED and use the same mechanism and signs as the mothership:
  - `BellyDoorL`: `CFrame.Angles(0, 0, -a)`.
  - `BellyDoorR`: `CFrame.Angles(0, 0, +a)`.
  - About 85 deg looks right; see `Saucer_doors_open.png`.
  - Fallback pivots if the importer resets pivots:
    - L: `PivotOffset = CFrame.new(-Size.X/2, Size.Y/2, 0)`
    - R: `PivotOffset = CFrame.new(Size.X/2, Size.Y/2, 0)`
  - Fully open, the doors hang about 2.8 studs below the closed hull bottom (lowest point near Y = -5.9). Keep that in mind for the hover height over eggs and players.
- **Closed underside, as seen from below:** steel collar, then a dark-green frame ring, then two doors. Each door has a steel frame, a dark-green band, steel and gunmetal iris stripes, and a green half-lens; together the halves read as one split green circle.

## Palette (sRGB; cell i = column i % 4, row i // 4, row 0 = bottom of the PNG)
| # | Name | Hex | Used for |
|---|---|---|---|
| 0 | SILVER | `#C9D1DA` | top hull panels |
| 1 | STEEL | `#98A3AF` | light gunmetal: rims, frames, girders |
| 2 | GUNMETAL | `#5B646F` | underside |
| 3 | DEEP | `#3A414A` | darker underside panels, window frames |
| 4 | GREEN | `#78FF5A` | light pods, strips, lens, hazard stripes |
| 5 | DKGREEN | `#2E8A2A` | pod bezels, accent rings |
| 6 | GLASS | `#1E5B55` | dark tinted teal glass (opaque) |
| 7 | GLASS_HI | `#4E9E8F` | glass highlight streak |
| 8 | BAY | `#171B20` | bay interior |
| 9 | WHITE | `#EEF2F6` | (spare) |
| 10 | MIDGREEN | `#4CC23A` | (spare) |
| 11 | TRIM | `#262B31` | seams, grooves |
| 12-15 | - | `#C9D1DA` | unused, filled with silver |

- Every face's UVs sit on the centre of its colour cell.
- The image uses Closest interpolation.
- No emissive, glow, or neon materials. The light pods are plain green geometry; glow comes later from the VFX plugin.

## FBX export settings
These are the same as `PetsV2/petkit.py bake_and_export` (path_mode COPY, embed_textures, mesh_smooth_type FACE, no leaf bones, no anim, default axes), with three changes:

```
use_selection=True, global_scale=0.01, apply_unit_scale=True, apply_scale_options="FBX_SCALE_NONE",
axis_forward="-Z", axis_up="Y", object_types={"MESH","EMPTY"}, use_mesh_modifiers=True,
mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False, path_mode="COPY", embed_textures=True
```

1. **`global_scale=0.01`.** The pet pipeline's default export lands in Studio at 100 studs per Blender metre (`studio_setup.lua`: `studsPerBU = 100 * scale`, then `ScaleTo`). At that default the 120 m mothership would come in at 12,000 studs, which is over the 2,048-stud MeshPart limit. With 0.01 it should arrive at 120 studs.
2. **`EMPTY` added** so `BeamOrigin` is exported.
3. **No `ARMATURE`**, because these models are static.

`Saucer.fbx` was re-exported 2026-10-10 for the doors revision. `Mothership.fbx` was not touched.

Checked by re-importing both FBX files into Blender (the Saucer again after the revision):
- names match;
- the size ratio is correct;
- the palette is packed;
- all islands are closed, with normals facing outward (`check_normals()`: 0 inside-out, 0 non-manifold edges).

## Open points for the Studio import (not done here)
- If the import comes in at the wrong size, `ScaleTo` until the mothership is 120 wide (saucer 16).
- Known importer quirk from the pets: it may add a +90 deg X turn to the PivotOffset. Zero that rotation if the parts look tilted when pivoted.
- `BeamOrigin` is an FBX null node. Studio may drop it or turn it into something odd. If so, add an Attachment at the coordinates above.
- Suggested part settings: Anchored, CanCollide/CanQuery/CanTouch off (sky decoration), CastShadow on the Mothership Hull only.
