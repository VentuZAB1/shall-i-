# Halloween garden: SpookyBushes (GARDEN_BRIEF row 3), 2026-10-12, review round 1

Build script: `bushes.py` (headless Blender 5.2, everything procedural, imports `hkit.py` read-only). Run each step in
its own process: `blender.exe -b --factory-startup --python bushes.py -- thorn` (also `autumn`, `bramble`), then
`render` and `export`. `eye thorn` (or `autumn` / `bramble`) renders the player-eye check shots into `wip\`.
Put `fast` first for a quick low-res test (256 textures, 1/3 of the leaves).
A full build takes 15-60 s, bakes included. Blends: `thorn.blend`, `autumn.blend`, `bramble.blend`. Maps: `maps\`.
Reports: `*_report.json`. The round-0 script is kept as `wip\bushes_v1_backup.py`.

**Axes:** 1 Blender m = 1 stud. Roblox X = Blender X, Roblox Y (up) = Blender Z, **Roblox Z = Blender -Y**.
The front (gourds, spider cane, front orb web) faces Blender -Y = **Roblox +Z**.
**Pivot:** every object sits at location (0,0,0). **The FBX origin is the base centre on the ground (Z = 0)**, so use
"Set Pivot to Scene Origin". Nothing in the exported meshes sinks more than 0.18 stud below Z = 0 (Thorn 0.125).

## How they're built
- **Bake source:** a voxel-union clump body covered by 2,360-3,245 real leaf blades. The vein pattern is a shader
  bump, baked into the normal map. The source also has the full canes, thorns, stems, berries and gourds (warts as
  geometry).
- **Game mesh:** the clump body decimated to 2.5-3.1k triangles and pushed 0.1 stud out into the leaf layer, plus REAL
  protruding leaves on the surface and silhouette. Each leaf has two sheets (top and bottom), 16-32 triangles, and no
  alpha cards. The exposed canes, thorns, stems, berries and twigs are real geometry too.
- **Bakes:** Cycles, per surface group (body, leaves, wood, berries), each group matched only to its own source.
  Maps: tangent normal (OpenGL), colour x AO (AO tinted deep red / purple, not grey) and roughness. One atlas per
  part.

## Round-1 changes (review FIX items)
**Bush_Thorn, rebuilt:**
1. **Cobweb reads from eye height.** The flat veil is gone. There are now two near-vertical **orb webs**:
   - **Front web:** 2.91 x 2.55, hung down the front (Roblox +Z face) between the front-left and front-right canes.
   - **Left web:** 2.53 x 2.66, on the left side (Roblox -X).
   Each web has 10-11 radials, a sagging, unevenly spaced catch spiral, a hub mat, an irregular frame, two torn holes
   and a few broken or dangling ends. All of it is painted as strong threads into a 1024 RGBA silk atlas on two-sided
   sheets. The sheets are kept 0.15 clear of the foliage and billow out 0.12.
2. **Strands are no longer tubing or clothesline.**
   - Geometric frame threads trace each web's edge.
   - 16 thread lines in total. Anchor threads run from the frame corners to nearby thorn tips and leaf tips, at
     irregular angles with uneven catenary sag.
   - The top corners tie into their supporting canes.
   - No tip-to-tip loops. The vertical rod and the hanging broken-end rod are removed. Near-vertical anchors are
     rejected.
   - Thickness 0.077-0.084, silvery off-white (208,210,218) with dust, roughness 0.6.
3. **Body no longer reads as a boulder.**
   - The body is 5 lobes on a widened, scalloped skirt, with dark AO crevices between them. The foliage is about
     4.5 tall.
   - 79 protruding outline leaves (weighted to the silhouette and the lower half), 18 leaves drooping over the base
     rim, and 8 leaves on the canes. Inner leaves are mostly dropped (3), and leaves under the silk are skipped.
   - Outline leaves are swung about their normal so none dips into the soil.
   - Asymmetric crown: arching canes of different heights and lean, one **snapped grey-olive dead cane** with a
     hanging piece, and a spider cane on the front-right.
   - 3 canes arc out of the sides and root into the soil. 2 thorny ground runners. 2 short thorn spikes.
4. **Berries:** 10 berries in 3 clusters: 6 black, 3 deep purple, 1 red.

**Optional polish (done):**
- **Autumn:** 18 extra leaves hang over the rim and around the back, hiding the bare stems (no "creature on legs").
  Gourd warts are darker and smaller, so they read less like mould.
- **Bramble:** every twig tip has its own taper length and sharpness (no identical points). The bark is a warmer
  grey-brown.

## FBX files (C:\cdimp)
| File | MeshPart | Triangles | Textures (embedded) |
|---|---|---|---|
| `Halloween_Bush_Thorn.fbx` | `Bush` | 8,759 | 1024 colour, normal, roughness (`BushThorn_*`) |
| | `Web` (frame + anchor threads) | 576 | 128 colour (`BushThornWeb_albedo`) |
| | `WebSilk` (two orb webs) | 336 | **1024 RGBA** colour (`BushThornSilk_albedo`) |
| | **total** | **9,671** (budget 10,000) | |
| `Halloween_Bush_Autumn.fbx` | `Bush` | 8,088 | 1024 colour, normal, roughness (`BushAutumn_*`) |
| | `Gourds` | 1,520 | 512 colour, normal, roughness (`BushAutumnGourds_*`) |
| | **total** | **9,608** (budget 10,000) | |
| `Halloween_Bramble.fbx` | `Bramble` | 4,515 (budget 5,000) | 512 colour, normal, roughness (`Bramble_*`) |

I re-imported each FBX in a fresh Blender. All textures are embedded, and the roughness map stays linked to Roughness.
The silk alpha stays linked to Alpha. The objects sit at (0,0,0) and carry no vertex colours.

## Sizes (Roblox X x Y x Z, whole asset) and part centres (Roblox axes, from the FBX origin)
| Asset | Size | Parts: size / centre |
|---|---|---|
| Bush_Thorn | **6.35 x 5.94 x 6.09** (brief 6 x 5.5 x 6) | Bush 6.35x5.94x6.02 @ (-0.020, 2.842, -0.055); Web 4.43x3.49x4.73 @ (-0.838, 3.045, 0.661); WebSilk 4.40x3.14x4.49 @ (-0.750, 3.119, 0.756) |
| Bush_Autumn | **6.19 x 5.21 x 6.07** (brief 6 x 5 x 6; 5.03 above the ground) | Bush 6.19x5.21x6.07 @ (0.050, 2.426, 0.132); Gourds 2.28x1.30x1.26 @ (-0.095, 0.620, 1.328) |
| Bramble | **3.88 x 3.06 x 3.85** (brief 4 x 3 x 4) | Bramble @ (0.025, 1.376, -0.028) |

The Thorn foliage mound is about 5.4 x 4.5 x 5.2. The arching canes and the spider cane reach 5.81. The rooting side
canes and runners reach about 3.1 from the centre.

## Attachment points (Roblox axes, relative to the FBX origin)
- **Bush_Thorn spider thread point (MOVED):** **(2.570, 3.790, 1.733)**.
  - It is 0.06 under the tip of the front-right spider cane, which arches out past the foliage. The ground is 3.79
    straight below, with nothing in between, so the spider hangs free.
  - Relative to the `Bush` part centre it is (2.590, 0.948, 1.788).
  - The existing `Halloween_Spider` is 6.75 studs tall. Scale it to about 0.3 (about 2 studs), with a thread of about
    0.8-1.2.
  - Use the WebsSpiders formula: `hangPoint = bushPivot * Vector3.new(2.570, 3.790, 1.733)`.
- **Orb web hubs** (where an extra spider could sit):
  - Front: hub (-0.135, 3.518, 2.803). Corners BL (-1.55, 2.05, 2.95), BR (1.45, 2.15, 3.00),
    TL (-1.449, 4.502, 2.451), TR (1.356, 4.689, 2.512).
  - Left: hub (-2.643, 3.002, -0.014). Corners BL (-2.85, 1.65, -1.15), BR (-2.95, 1.55, 1.15),
    TL (-2.087, 4.268, -1.488), TR (-2.355, 4.043, 1.251).
- **Gourd stem tops (Bush_Autumn):** pumpkin (-0.658, 0.686, 1.292), goblin gourd (0.379, 1.032, 1.629). These are
  only useful for small decoration.

## Roblox setup the lead must do
- SurfaceAppearance comes from the importer: ColorMap, NormalMap and RoughnessMap. If the importer drops the roughness
  map, set `RoughnessMap` by hand from `maps\*_rough.png`. The berries are glossy (0.14-0.22) and go flat without it.
- **`WebSilk`: `SurfaceAppearance.AlphaMode = Transparency` is REQUIRED.** With Overlay it shows as an opaque white
  sheet. The sheets are two-sided geometry, so they don't need DoubleSided. Fallback without alpha: Transparency 0.5,
  Color (230,228,234).
- `Web`: plain colour strands, 0.077-0.084 thick. If the map is dropped, use Color (208,210,218) SmoothPlastic,
  roughness about 0.6.
- `Web` and `WebSilk`: CastShadow false, CanCollide / CanTouch / CanQuery false.
- **RenderFidelity = Precise** on every part: thin canes, thorns, twigs and leaf edges get mangled by automatic LOD.
- Collision: decorative. Use CanCollide false, or a Box hull on `Bush` / `Bramble` if players must not walk through.
- Anchored. No Neon or emissive anywhere. Everything is static, with no moving parts. Keep each asset's parts
  together in one Model.
- BushSmall slots: scale a bush model to 0.75-0.85, as the brief says.

## Review renders (this folder)
They use the hkit `review_setup` sky and sun, a green ground and soil beds. Backface culling and dithered alpha are on
to match the reviewer.
- **Player eye height (5 studs up), new for round 1:**
  - `review_thorn_eye40_front.png`, `review_thorn_eye40_back.png`, `review_thorn_eye40_left.png`: 40 studs away
    through a 150 mm lens.
  - `review_thorn_eye25_frame.png`: 25 studs away, 70 degree frame.
  - `review_thorn_sil_0.png`: flat black front silhouette with the webs hidden.
  - `review_autumn_eye40_back.png`: 40 studs, back view.
- `review_lineup_25.png` (25 studs) and `review_lineup_50.png` (50 studs): Thorn, Autumn, Bramble.
- Close-ups: `review_thorn_close.png`, `review_thorn_back34.png`, `review_autumn_close.png`,
  `review_bramble_close.png`.
- More eye-height shots (low close-up, silhouettes at 90 / 200 degrees) are in `wip\eye_*`.

## Known limitations (honest self-review)
- **The Thorn is a little over the brief:** 6.35 x 5.94 x 6.09 against about 6 x 5.5 x 6.
  - The extra width and depth come from the rooting side canes, the runners and the front web.
  - The extra height comes from the arching canes and the spider cane, at 5.81 above the ground.
  - I already pulled the rooting canes and runners in from 3.5 to about 3.1 from the centre.
  - If the slot is tight, scale the model to 0.95.
- The webs are stylised. The painted threads are strong and white so they read at 25-40 studs, so up close (under
  about 8 studs) they look graphic rather than fine silk. The painted silk is flat. Only the frame and anchor threads
  are real geometry.
- The 3 rooting side canes can read as spider legs from the back. That suits Halloween, but it is a choice.
- The game-mesh clump body is still a lumpy shell with leaf detail in the normal map. The lobes, crevices and real
  outline leaves break it up, but face-on at very close range the centre of a lobe still looks smooth.
- Under the strong review sun (AgX), the sunlit autumn leaves render slightly peach. Sky specular lifts the
  near-zero blue channel. The albedo itself is saturated: the mean saturation is 0.93.
- Leaf bottoms reuse the top's texels, so the vein relief is mirrored underneath. All lo thorns share one small UV
  template. The atlases are about 50-61% filled: many small islands with 2-px margins.
- The Thorn canes are 4-5 sided and the bramble twigs 3-6 sided. Their polygon edges show only in very close shots.
- The pumpkin's and gourd's warts are mostly in the normal map. Their silhouettes are smooth ribbed shapes.
