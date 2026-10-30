# Halloween garden, row 4 "Graveyard" (2026-10-12)

Build script: `graveyard.py` (headless, everything procedural, no booleans):

```
blender.exe -b --factory-startup --python graveyard.py -- grave A grave B grave C grass A grass B review verify
```

Extra steps: `preview <Name>` (5 quick renders into `wip\`) and `fast` (low-density test). Each asset step rebuilds the
.blend, the maps and the FBX.

- Blends: `Grave_A/B/C.blend` (the hidden bake sources `*_hi` / `*_mound_hi` are kept) and `DeadGrass_A/B.blend`.
- Maps: `maps\<Name>_albedo|normal|rough.png`. For the graves, `_ao.png` is reference only, because AO is already
  multiplied into the albedo.
- Numbers per asset: `<Name>.json`.

## Axes, pivot, orientation (all five FBX files)
- 1 Blender unit = 1 stud. Blender +Z = Roblox +Y. **Blender +Y = Roblox -Z.** The FBX is written with
  `hkit.export_fbx`.
- **Pivot / FBX origin = the ground contact point.** That is the centre of the stone's foot (or the root centre of the
  grass tuft) at soil level, Z = 0. Use "Set Pivot to Scene Origin" and put the pivot on the bed surface.
- Lowest points below Z = 0: graves -0.21 / -0.24 / -0.24 (the soil-mound rim and the buried foot), grass -0.15 (buried
  blade roots). All are within the 0.3 limit.
- **Front (carving) faces Blender -Y = Roblox +Z.** In Blender, "RIP" reads left to right when you look from -Y.
  - The PumpkinEggs builder noted that the Studio importer may turn models 180 degrees. If "RIP" faces away after
    import, just yaw the model 180 degrees.
  - The text is never mirrored: the axis change is a proper rotation.
- Roblox centres a MeshPart on its bounding box. The bbox-centre offset from the ground point is given below (Roblox
  axes) in case you place by MeshPart position instead of pivot.

## Objects
Each FBX holds ONE mesh object (one MeshPart) with one material. It embeds three 512 textures: colour (with AO for the
graves), tangent normal (OpenGL / +Y, Blender bake) and roughness. The import check (`verify`) shows all three are
packed=True.

| FBX (C:\cdimp) | Object | Tris | Size, Roblox X x Y x Z (whole asset) | Stone only, X x Y x Z | bbox centre from origin (Roblox) |
|---|---|---|---|---|---|
| `Halloween_Grave_A.fbx` | Grave_A | 3,279 (stone 2,271, mound 420, blades 588) | 4.78 x 4.24 x 3.47 | 3.07 x 4.04 x 1.16 | (0.03, 1.91, 0.07) |
| `Halloween_Grave_B.fbx` | Grave_B | 3,150 (stone 2,274, mound 450, blades 426) | 3.91 x 4.45 x 2.81 | 2.62 x 4.21 x 1.00 | (-0.02, 1.98, 0.25) |
| `Halloween_Grave_C.fbx` | Grave_C | 3,314 (stone 2,328, mound 462, blades 524) | 4.75 x 3.93 x 3.91 | 3.45 x 3.69 x 1.62 (leaning) | (0.05, 1.73, -0.04) |
| `Halloween_DeadGrass_A.fbx` | DeadGrass_A | 2,478 (103 blades) | 4.13 x 3.15 x 3.60 (3.0 above ground) | | (0.07, 1.42, -0.01) |
| `Halloween_DeadGrass_B.fbx` | DeadGrass_B | 2,234 (101 blades) | 2.85 x 2.66 x 2.93 (2.5 above ground) | | (0.16, 1.17, 0.07) |

- The whole-asset size includes the soil mound and the dead-grass blades. Y includes the buried part.
- The stone depth includes the lean.

All budgets are met: graves <= 4,000 tris with a 512 texture, grass <= 2,500 tris with a 512 texture.

**Attachment points:** none needed (no lights, spiders or webs on these).

## The assets
- **Grave_A, rounded-top headstone.**
  - Shape: 3.0 wide, 4.0 tall, 1.0 thick, tapering to 0.88 at the top. It leans 2.5 degrees back and 1.8 degrees
    sideways.
  - Carvings: a big serif "RIP" (1.0 tall, 0.085 deep, chamfered walls), a small cross above it, a carved border groove
    around the arch, and two worn illegible epitaph lines.
  - Weathering: a through-crack at the right shoulder, a small crack low on the left, and rounded chips along the rims.
  - Surface detail: pits, rain streaks, small lichen rosettes, moss in the letters and cracks and at the base, and a
    soil stain at the foot.
- **Grave_B, stone cross on a 2-step plinth.**
  - Shape: arms 2.6 wide with flared ends, 4.2 tall. It leans 3.5 degrees sideways and 1.2 degrees back.
  - Carvings: an inset border line along the cross, a diamond at the crossing, and a panel line on the plinth.
  - Weathering: a crack right through the shaft, a broken corner on the right arm, chips, and moss on the plinth.
- **Grave_C, old cracked slab.**
  - Shape: 3.14 wide, 0.9 thick. The lean is built into the mesh: 9.5 degrees back, 3 degrees sideways, and 4 degrees
    yaw. **Don't add more pitch in Studio.**
  - Damage:
    - The top-right corner is broken off. The break is a fresh, lighter, moss-free surface of chunky stepped rock
      facets about 0.15-0.3 stud across (round 2).
    - A deep through-crack cuts off the top-left piece, which sits slightly proud and lower.
    - A forked hairline crack runs at the lower right.
  - Carvings: a worn skull and crossbones (deep eye sockets) and four eroded epitaph lines. It has the most moss and
    lichen of the three.
- **Soil mound (all graves):** a low heaped mound mostly in front of the stone (0.22-0.42 high). It has clods,
  pebbles, a few dead-leaf bits and moss patches. Its rim sinks to -0.08, so it blends into the bed with no visible edge.
  A few dead-grass clumps grow at the stone's foot, some blades bent or broken.
- **DeadGrass_A / _B:** fountain-shaped tufts.
  - Blade layout (round 2):
    - 48 upright core blades with 3-4 segments; most are short and a few are tall.
    - 47 (A) / 47 (B) long arching and flopped blades with 8-10 segments each, a gentle even droop, and small
      twist/wobble.
    - 8 (A) / 6 (B) lying blades.
    - About 14% of blades are folded over as ONE sharp fold, and about 8% are snapped short.
    - Measured bend between neighbouring faces (reviewer's `grasscheck` method): A 4.7 degrees median, 6.7 degrees at
      the 90th percentile; B 4.4 / 6.3. Round 1 was 13 / 21.
  - Colours: 8 variants (straw, pale straw, golden, olive, olive-brown, straw-tan, ash grey, green-olive). Roots are
    darker and tips bleached. Straight fine vein streaks, and a tangent normal with veins and a mid-rib.
  - Blight spots are on the golden and olive-brown blades only, about 1 blade in 3-4. Round 2 removed the pink and
    lilac cast.
  - The blades are real tapered geometry: front strip + back strip, no alpha.

## Roblox setup
- **Import:** use the Studio 3D importer (creator ZAB Studio). The SurfaceAppearance comes from the embedded maps.
  - AlphaMode: none needed, because nothing is transparent.
  - No Neon and no emissive.
- **Graves:**
  - Collision: CanCollide on (they replace the rocks), CollisionFidelity Box or Hull. The mesh is open underground: the
    stone faces below Z = -0.06 and the mound faces under the stone are removed.
  - RenderFidelity: Automatic is fine.
- **Grass:**
  - Collision: CanCollide off, CanTouch off, CanQuery off.
  - The blades rely on Roblox's normal single-sided rendering, so leave DoubleSided off. Each blade is a front strip
    plus a back strip 0.004 apart.
  - CastShadow on looks good.
  - Scale freely: about 0.75 to 1.3. Use B, or A scaled to 0.6, for the small grass spots.
- **The red toadstools** stay as they are (lead's note).

## Known limitations
- The grass texture is a painted procedural strip atlas, not a Cycles bake. So there is no per-blade AO: blades darken
  toward the root instead.
- The grave blades use a reserved 48 px column of the grave's 512 atlas. The stone and mound UVs fill the other 90% of
  the width, with front islands at 1.55x texel density.
- The stone texture is 512, so very close up (under ~6 studs) the surface looks soft. At 20+ studs it is crisp: RIP and
  the skull read clearly at 50 studs (`review_50studs.png`).
- Under the review sky (blue fill), shadowed stone sides look blue-grey. The albedo itself is a warm-neutral grey,
  about (146,132,113) to (122,126,131) sRGB.

## Review renders
In this folder, all imported from the exported FBX files with backface culling on (like Roblox):
- `review_25studs.png`
- `review_50studs.png`
- `review_close_Grave_A.png`
- `review_close_grass.png`

More renders are in `wip\`: `review_34.png`, `review_back.png`, `review_close_Grave_B.png`,
`review_close_Grave_C.png`, `look_C_right.png` and the `pv_*.png` previews.

## Review round 1 fixes (2026-10-12)
Grave_A and Grave_B passed and are untouched. Their FBX files and maps are byte-identical to round 1. The script
changes are opt-in, so `grave A` / `grave B` still rebuild them exactly.

### FIX 1: Grave_C fracture
- **Cause:** the broken-corner outline was jittered every 0.07 stud and then extruded through the slab. That turned
  each zigzag into a ridge running through the thickness, which gave the parallel ripples and the "teeth" on the top
  edge.
- **New outline:** the break is now 6 chunky straight facets, 0.20-0.26 long.
  - The old `jag()` call is kept with its result unused, so every later random draw is unchanged: the cracks, epitaph,
    skull and moss are identical.
- **Isotropic Voronoi cut planes** (`facets` in the Grave_C spec):
  - each cell, 0.15-0.3 stud across, has its own tilted plane;
  - there are crisp 0.02 steps between cells, plus fine isotropic grain.
- **Bake vs game mesh:** the facets go into the bake source only. The game mesh gets a smooth mean-depth offset there,
  because decimating the sharp steps left triangular shards in the bake.
- **Colour:** the break is lighter and fresher, with moss reduced by 90% and no lichen.
- **Chips:** Grave_C's chips are broader and shallower: depth 0.08-0.20, chamfer slope 0.8, length 0.4-0.84. The
  narrow chip on the right face that read as a dark slot is now a wide shallow scoop.
- **Result:** triangles 3,308 -> 3,314. Re-baked and re-exported.
- **Evidence:** `wip\look_C_right.png`, `wip\look_C_right_hi.png`, `wip\look_C_r34_12.png`, `wip\look_C_edge.png`.

### FIX 2: grass faceting
- Long arching and flopped blades now have 8-10 segments, at most about 7 degrees per joint.
- Core blades have 3-4 segments.
- About 20% of the hidden centre budget moved to arching blades.
- Snapped blades stay a single sharp fold.
- Triangles: A 2,464 -> 2,478, B 2,268 -> 2,234.
- **Evidence:** `wip\grasscheck_round2.json` (the reviewer's script, run on the new FBX files).

### Optional items
- **Done:**
  - grass spots on fewer blades;
  - pink/lilac variants shifted to straw-tan and ash grey;
  - straight vein streaks;
  - DeadGrass_B footprint 2.96 x 3.19 -> 2.85 x 2.93.
    - It is still a little over 2.5. Scale it about 0.88 in Studio if it must be exactly 2.5.
- **Not done:**
  - **Mound rim blend toward the bed brown.** It would only apply to Grave_C, because Grave_A and Grave_B must not
    change, and the three mounds would no longer match. The lead can decide after comparing with the real bed soil;
    it is a one-line change applied to all three.
  - **Grave-base blade clumps** keep their round-1 segmentation, so the three graves stay consistent. They are short
    and the reviewer marked them non-blocking.
