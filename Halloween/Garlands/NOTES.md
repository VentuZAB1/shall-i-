# Halloween garlands - NOTES (2026-10-12)

Bunting garlands for the inner face of the hub's back wall (slate-blue, 24 studs tall). A jute rope sags between two
wrought-iron hooks, with stitched cloth pennants (orange / black / deep purple) and a printed symbol on each. Each
garland also has two small dangling extras: a black paper bat and an orange felt pumpkin.

## Files
- Build script: `garlands.py` (headless: `blender.exe -b --factory-startup --python garlands.py -- tex build render export`)
- Scene: `garlands.blend`. The hook's hi-res sculpts are hidden in the scene.
- Maps (`maps\`):
  - `Garland_albedo/normal/rough/ao.png`: 1024, one atlas shared by BOTH garlands.
  - `Hook_albedo/normal/rough/ao.png`: 256.
- FBX: `C:\cdimp\Halloween_Garland_Long.fbx`, `C:\cdimp\Halloween_Garland_Short.fbx`, `C:\cdimp\Halloween_Garland_Hook.fbx`
- Reviews (slate-blue wall, sRGB 96,132,170, at y = -0.6):
  - `review_long_30.png`, `review_short_30.png`: 30 studs, from below.
  - `review_long_oblique.png`: 22 studs, from the side.
  - `review_flags_10.png`: 10 studs.
  - `review_close.png`: 5.5 studs.
  - `review_hook_close.png`: the rope wrap on the hook.
  - `review_hook_solo.png`: the hook on its own.

## Axes
1 Blender m = 1 stud. Blender +Y = Roblox -Z (toward the players). Roblox coordinates below are (X, Y up, Z).
In object space the wall face is at Blender y = -0.6, i.e. Roblox Z = +0.6, behind the rope.

## Objects
| Object | Size, Roblox X x Y x Z (studs) | Triangles | Maps | Faces | Pivot (FBX origin) |
|---|---|---|---|---|---|
| `Garland_Long` | 26.43 x 6.15 x 0.71 | 5,296 | 1024 atlas | pennant fronts face Roblox -Z (Blender +Y) | midpoint between the two hook points |
| `Garland_Short` | 19.43 x 5.27 x 0.72 | 4,306 | 1024 atlas (same images) | same | midpoint between the two hook points |
| `Garland_Hook` | 0.32 x 0.54 x 1.15 | 310 | 256 | arm points Roblox -Z, J-tip curls up | the hook point; plate back on the wall |

Bounding boxes, in case the importer recentres a MeshPart on its bounds. Values are Blender coordinates, then the bbox
centre in Roblox axes:
- Long: min (-13.216, -0.293, -6.072), max (13.216, 0.420, 0.078). Centre (Roblox) **(0, -2.997, -0.064)**.
- Short: min (-9.716, -0.297, -5.196), max (9.716, 0.420, 0.078). Centre (Roblox) **(0, -2.559, -0.062)**.
- Hook: min (-0.16, -0.60, -0.40), max (0.16, 0.553, 0.14). Centre (Roblox) **(0, -0.130, 0.024)**.

## Attachment points (object space, Blender = Roblox here because they all have y = 0)
- **Hook points:**
  - Long: (-13, 0, 0) and (+13, 0, 0). Catenary sag 3.5 (lowest rope point (0, 0, -3.5)), arc length 27.22, c = 24.705.
  - Short: (-9.5, 0, 0) and (+9.5, 0, 0). Sag 2.6 (lowest point (0, 0, -2.6)), arc length 19.92, c = 17.773.
  - The hook point is the rope's centre line at the top of its wrap round the hook arm. The rope makes about 1.4 turns
    round the arm, drifting forward 0.3 toward the players. It ends in a knot and a frayed tail that hangs about 0.65
    below the hook point, slightly in front of it. The wrap, knot and tail are part of the garland mesh.
- **Hook geometry** (object space of `Garland_Hook`, Blender axes):
  - Plate back face at y = -0.6 (on the wall).
  - Arm axis at z = -0.13 (rope radius 0.09 + bar 0.04 below the hook point). The arm runs from the plate to y = +0.44,
    then the J curls up to about z = +0.04 so the rope can't slide off.
  - The same hook works at both ends (it is symmetric in X).
- **Pennant centres** (the rope point at each sleeve centre, x / z):
  - Long: -10.48/-1.24, -7.96/-2.21, -5.36/-2.92, -2.70/-3.35, 0/-3.50, 2.70/-3.35, 5.36/-2.92, 7.96/-2.21, 10.48/-1.24.
  - Short: -7.57/-0.96, -5.13/-1.86, -2.59/-2.41, 0/-2.60, 2.59/-2.41, 5.13/-1.86, 7.57/-0.96.
- **Extras' tie points on the rope:**
  - Long: bat (-4.12, 0, -3.16), pumpkin (4.14, 0, -3.15).
  - Short: bat (-4.02, 0, -2.14), pumpkin (4.02, 0, -2.14).
  - The bat hangs 0.56 below its tie point (Short: 0.74) on a thread. The pumpkin hangs 0.46 below (Short: 0.50) on
    twine.
  - Both are merged into the garland mesh, so they are static.
- **Clearances:**
  - Pennant cloth stays at y >= -0.124, at least 0.47 in front of the wall.
  - The pumpkin is the deepest part (y = -0.297, 0.30 from the wall).
  - The extras are at least 0.18 from any pennant.
  - The lowest pennant tip is 6.07 below the hooks on Long and 5.20 on Short.

## Pennants (pattern 1.8 wide x 2.6 long, 155 px/stud in the atlas)
- Each pennant is built as cloth:
  - A triangle with a folded, stitched hem that wraps over the rope as a sleeve (roll radius 0.125).
  - A folded-back strip behind it, and real back faces. The back shows the symbol unmirrored, so **DoubleSided is not
    needed**.
  - Gentle cloth shape: a sideways wave, a belly, a diagonal drape ripple, edge curl, tip curl and a slight twist.
  - The pennant shears slightly toward vertical where the rope slopes.
  - The tip is a raw cut with 3 loose threads.
- Each pennant's maps include:
  - A canvas plain weave in the normal map, plus seam grooves, puckers and drape creases.
  - Faded, mottled dye with per-thread tone.
  - Dust toward the tip and along the edges.
  - Running stitches along the hem and both sides, in contrasting thread.
  - A crisp printed symbol, slightly worn, with the weave showing through.
- Designs in Blender +X order, i.e. from the **viewer's right to left** when facing the wall:
  - **Long:**
    1. orange / black bat
    2. black / orange jack-o'-lantern (carved holes with a flesh rim)
    3. purple / bone skull
    4. orange / black-widow spider on a thread
    5. black / crescent moon with stars
    6. purple / orange bat (wings raised)
    7. orange / carved angry jack face
    8. black / skull and crossbones
    9. purple / bone spider
  - **Short:** orange bat, black jack-o'-lantern, purple spider, orange jack face, black moon, purple skull, orange spider.
- Colours (sRGB):
  - Fabric: orange 196,92,30; black 40,35,42; purple 92,44,124.
  - Ink: black 25,20,23; orange 226,118,34; bone 228,214,180; moon 236,216,152.
- Rope: 0.18 thick, twisted 2-ply jute (Z-lay, 0.40 pitch), from the normal and colour maps on a 6-sided tube.
- Extras:
  - Paper bat: black card with a crisp V-fold, wing-bone lines and tiny orange eye slits. Wingspan 0.83.
  - Felt pumpkin: 0.60 wide, ribbed, with a black-felt angry face and a stem.

## Roblox setup the lead must do
1. Import each FBX with the 3D importer (creator ZAB Studio).
2. Textures:
   - The FBX embeds ColorMap and NormalMap only. The **RoughnessMap is not embedded**, same as the head pipeline (the
     kit's material wiring).
   - Optionally upload `maps\Garland_rough.png` and `maps\Hook_rough.png` and set them as SurfaceAppearance.RoughnessMap.
     Without them, cloth and rope look slightly flatter than in the reviews.
   - No metalness, no transparency (AlphaMode untouched), **no Neon / emissive**.
   - Both garland FBXs embed byte-identical atlas images, so they can share the same uploaded texture IDs.
3. Part properties:
   - Every part: Anchored, CanCollide false, CanTouch false, CanQuery false.
   - Garlands: CastShadow true. Hooks: CastShadow can be false.
   - RenderFidelity Automatic is fine.
   - Put everything under `Workspace.HalloweenDecor`.
4. Placement:
   - Set the garland pivot at the bay centre, at the chosen height, **0.6 studs in front of the wall face**. Orient it
     so its local -Z (Roblox) points into the hub, toward the players.
   - Put a `Garland_Hook` at `garlandCF * CFrame.new(+-13, 0, 0)` (Short: `+-9.5`) with the same rotation. Its plate
     then sits flat on the wall.
   - If a MeshPart was recentred on its bounds, offset it by the bbox centres above. For example
     `MeshPart.CFrame = garlandCF * CFrame.new(0, -2.997, -0.064)` for Long.
   - Suggested height: hooks about 19-20 studs above the floor, which puts the lowest tips about 13-14 above the floor.
   - Use Long for the ~26.5-stud bays and Short for the ~19-stud bays.
   - If the clear span between pillar faces is under 26 / 19 studs, mount the hooks on the pillar sides, or scale the
     garland's X by up to ~3% (that won't visibly distort it).
5. Nothing moves. The bat and pumpkin are merged, so they can't sway.

## Known limitations
- The roughness map is not embedded (see above).
- Static cloth: there's no wind motion.
- Rope and hook bars are low-sided tubes (6-sided rope, 4-sided twisted iron bar). The facets only show closer than
  ~3 studs.
- At the very far mip levels, a pennant's outermost texel can pick up a faint tint from the next UV island. The
  margins are 9 px plus dilation.
