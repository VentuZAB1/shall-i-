# TPTrees: toilet-paper-pranked autumn tree and bush (2026-10-12, review round 1 rework)

This is row 2 of `GARDEN_BRIEF.md`. It holds an autumn tree with a lobed, leaf-cluster canopy and a round
green-to-autumn bush. Both are TP-pranked:
- crumpled, torn toilet-paper streamers thrown over the foliage;
- sagging festoons and a loose loop;
- tails that end in mid-air;
- real rolls with a core hole.

Everything is procedural, built in headless Blender 5.2.2 with the shared kit (`hkit.py`, used read-only).

## Files
- Build script: `tptree.py`. It runs one step per call:
  `blender.exe -b --factory-startup --python tptree.py -- build|bake|render|export|preview tree|bush`.
  Put `quick` before the step for a low-density shape test.
- Scenes:
  - Final (baked): `tptree.blend`, `tpbush.blend`.
  - Pre-bake: `wip\tree_wip.blend`, `wip\bush_wip.blend`. These hold the hi-poly sculpts.
- FBX outputs. Textures are embedded; both were checked by a fresh import with `verify_fbx.py`
  (log `wip\log_verify.txt`):
  - `C:\cdimp\Halloween_TPTree.fbx` (13.3 MB, md5 `b75689f88724241d27bfaba107c4c228`)
  - `C:\cdimp\Halloween_TPBush.fbx` (4.3 MB, md5 `a8fc1e97d5b8859eed76556479abee34`)
- Maps are in `maps\` as `<prefix>_albedo/_normal/_rough.png`. `_ao.png` is reference only, because AO is already
  multiplied into the albedo.
- Logs: `log_build_*.txt`, `log_bake_*.txt`, `log_export_*.txt`, `wip\log_render_*.txt`. Build reports:
  `wip\tree_build.json`, `wip\bush_build.json`.

## Objects (each becomes one MeshPart)
| FBX | Object | Triangles | Maps (albedo / tangent normal / roughness) | Notes |
|---|---|---|---|---|
| TPTree | `Trunk` | 5,200 | 1024 | Bark; branch parts hidden inside the canopy are removed. |
| TPTree | `CanopyA` | 8,257 | 1024 | Canopy half with Blender x >= 0 (Roblox X >= 0). |
| TPTree | `CanopyB` | 8,341 | 1024 | Canopy half with x < 0. |
| TPTree | `TP` | 7,880 | 1024 | 10 strips plus 2 rolls, in one part. |
| **TPTree total** | | **29,678** | | Budget is 30,000 or fewer; each part is under 20,000. |
| TPBush | `Canopy` | 7,299 | 1024 | The flat bottom resting on the soil is removed (never seen). |
| TPBush | `TP` | 2,572 | 512 | 5 strips plus 1 roll. |
| **TPBush total** | | **9,871** | | Budget is 10,000 or fewer. |

- The tree canopy is split into two parts only to double the leaf texel density. Both halves carry the unsplit
  canopy's custom normals, so there is no shading seam at x = 0. Two tiny sliver faces left by decimation were
  deleted.
- All materials are opaque PBR. There is no alpha, no Neon and no emissive. Metalness is 0.
- Measured map statistics (final maps):

| Map | Near-black texels (luma < 0.10) | Mean roughness | Inverted normal texels |
|---|---|---|---|
| CanopyA | 0.9% (was 19-20%) | 0.86 | — |
| CanopyB | 0.9% | 0.86 | — |
| Bush canopy | 0.1% (was 17.6%) | 0.88 | — |
| TP (both assets) | — | 0.86 | 0 |

- The paper is about (236, 232, 220).

## Size, pivot, orientation
1 Blender metre = 1 stud. The FBX objects import with scale 0.01, so 1 local unit = 1 stud. Blender +Y = Roblox -Z,
so Roblox = (bx, bz, -by). Sizes are given as Roblox X x Y(up) x Z.

- **Tree**: 14.25 x 15.95 x 14.20 studs, against the 14 x 16 x 14 target.
  - Blender bbox: min (-7.378, -6.935, -0.156), max (6.875, 7.268, 15.791).
  - Bbox centre in Roblox axes: (-0.25, 7.82, -0.17).
  - The canopy spans Y 6.4 to 15.6.
- **Bush**: 5.51 x 4.75 x 6.49 studs, including the roll and the paper on the soil in front.
  - The foliage alone is 5.50 x 4.70 x 5.51 and sits on the soil.
  - Blender bbox: min (-2.700, -3.692, -0.050), max (2.806, 2.801, 4.700).
- **Pivot**: the FBX origin (0, 0, 0) is the centre of the trunk base (bush base) at soil level, Z = 0.
  - Every object has its origin there and no rotation.
  - The roots sink at most 0.156 below Z = 0 (the bush 0.05). Use "Set Pivot to Scene Origin".
- **Front**: Blender -Y = Roblox +Z.
  - The tree's twig roll and the fallen roll are on that side.
  - The bush roll faces it too. It is turned 45 degrees, so the core hole reads from both the front and the +X side.

## Attachment / reference points (Roblox axes, relative to the FBX origin)
- **Tree, twig roll**, hanging on an outer twig 7.3 studs up:
  - Centre (3.11, 7.33, 5.35); axis (0.68, -0.14, 0.72).
  - 0.75 stud clear of the foliage.
  - It unrolls into a 4-stud torn tail.
- **Tree, fallen roll**, lying on the soil beside the trunk:
  - Centre (-1.34, 0.55, 1.99); axis (0.50, 0, 0.87).
  - Its sheet trails about 2 studs along the soil.
- **Bush roll**, on the soil in front:
  - Centre (0.44, 0.55, 3.11); axis (0.80, 0.06, 0.60), tipped slightly.
  - Its sheet leaves the outer surface, runs under the roll and along the soil, then climbs the bush diagonally.
- Tree canopy centre (a suggested sway pivot): (0, 10, 0). Bush centre: (0, 1.8, 0).
- Roll size (both assets): 0.96 across and 0.45 wide.
  - Cardboard core: outer radius 0.20.
  - Real through-hole: radius 0.17.
  - There is a loose outer layer.

## Roblox setup for the lead
- Import with the 3D importer (creator ZAB Studio). The SurfaceAppearance comes from the embedded maps.
  AlphaMode can stay at the default (Overlay), since no part uses alpha.
- **The `TP` part may sway, but only very slightly.** The strips rest on the leaves and branches.
  - Rotations above about 0.5 degrees, or moves above about 0.05 stud, make the paper clip into the leaves or float.
  - If you add sway, rotate `TP` by 0.3 degrees or less about the canopy centre (bush: about (0, 1.8, 0)).
  - Otherwise leave it static.
- Suggested collisions:
  - Tree: `Trunk` CanCollide on, CollisionFidelity Hull. `CanopyA`, `CanopyB` and `TP` CanCollide off.
  - Bush: everything CanCollide off, or a Box.
- CastShadow on for all parts.
- BushSmall: scale the bush 0.75 to 0.85, as the brief says.

## Round 1 changes (answers to REVIEW.md)
**Tree**
1. **Paper reads as paper, not ribbon.** Each strip's low mesh now has these:
   - edges that vary ±13% in width, so no strip has parallel edges;
   - real crumples: folds, bunching next to snags, 1-2 sharp kinks per strip, and a slight grime tint;
   - softened (rounded) edges;
   - ragged torn ends with a zig-zag tear outline, cut into the geometry by ear clipping;
   - in the hi-poly bake source, irregular perforation creases with uneven spacing and depth, small crumple
     detail, and value patches.
2. **Two readable rolls**, each 0.96 across with a visible core hole:
   - One hangs on an outer twig 7.3 studs up (Roblox +X+Z side), wrapped once with a loose layer, and unrolls into
     a 4-stud torn tail.
   - One lies on the soil beside the trunk, its sheet trailing along the ground.
   - Both are visible from the front at 25 and 45 studs; the fallen roll also shows from the side.
3. **Paper on every side.**
   - 4 rim festoons: front, right, back and left. Each sags (sag 1.16-1.2) and has long tails of 0.9-4.3.
   - 2 over-the-top streamers with tails of 4.2-4.8, which hang down the back and sides.
   - 2 strips hang over twigs.
   - In total: 10 strips, 128.8 studs, 78 px per stud.
4. **Lobed canopy.** Before decimating, I added leaf-cluster lobes:
   - Poisson-spaced every 1.1 studs, radius 0.6-0.85, height 0.2-0.3, with creases between them.
   - The lobes now break up the silhouette and survive into the low mesh.
   - Under each lobe tip the leaves are slightly lighter.
   - The trunk went from 7,199 to 5,200 triangles; the canopy got 16,600.
5. **Matte leaves**: leaf roughness is now 0.82-0.90 (bake mean 0.86).
6. **No near-black gaps**:
   - The gap colour is now a deep warm red-brown (84, 32, 20) with roughness 0.95.
   - The darkest autumn stop was lifted to (150, 32, 22).
   - The canopy AO is milder (strength 0.45, distance 0.8).

**Bush**
1. **Re-draped so it looks thrown**:
   - `BRoll`: from the roll, along the soil, then diagonally up the front and over the right side of the crown.
     It ends in a 1.15-stud torn tail on the back-right.
   - `BBack`: thrown diagonally across the back, from near the crown down to the left as seen from behind. Its
     torn tail ends 1.05 above the soil.
   - `BShoulder`: one strip over the left shoulder, whose two tails end 0.8 above the soil.
   - `BCaught`: a short slack piece caught on the right side, with both ends free (lowest 0.8 above the soil).
   - `BLoop`: a loose loop sagging off the back-right below the widest girth.
   - There is no cross on top, and only the roll's strip reaches the ground.
2. **Same paper treatment as the tree**: torn ends, width variation, crumples and soft edges.
3. **Paper comes off the roll**:
   - The roll is tipped slightly.
   - The sheet makes a loose outer wrap over the top and far side, leaves tangentially from under the roll, lies
     on the soil for a short run, then climbs.
   - The roll is turned so the hole shows from the front and the side.
4. **Shape**:
   - Lobed leaf clusters: spacing 0.72, radius 0.36-0.52, height 0.15-0.24.
   - Two asymmetry clumps: a low bulge on the front-right and a raised shoulder on the back-left.
   - The hidden flat bottom was deleted before decimating, which put more triangles on the visible outline.
   - The bottom rim was re-baked, with no leaves on the hidden bottom.
5. **Gloss and gaps**:
   - Leaf roughness is 0.84-0.90 (bake mean 0.88).
   - The gap colour is now a deep green-brown (46, 50, 24).
   - The autumn change now also follows the lobe tips: every cluster turns at its tip, not only top-to-bottom.

## How it was made (summary)
- **Canopy**:
  - The base shape is clumps (spheres plus sub-blobs with flattened undersides). They are joined by voxel union,
    smoothed, given noise, then the lobe field.
  - The hi-poly adds sculpted leaves (tree about 14k, bush about 3.8k): pointed ellipses with a mid-rib fold,
    tilted like shingles. Undersides are flatter.
  - Each clump has its own autumn hue, plus mottling and lighter lobe tips.
  - The low-poly is the base pushed out to the mean leaf height, then decimated.
  - The bake (normal + colour x AO + roughness) is done at 2048 and box-filtered to 1024.
- **Trunk**:
  - A skeleton of tapered tubes (trunk, root flare, roots, limbs, twigs, sawn stubs) is voxel-unioned and smoothed.
  - Bark fissures and plates use nearest-skeleton coordinates, with lichen and moss at the collar.
- **TP**:
  - Each strip is a Verlet rope. It has gravity, length and bending constraints, and friction, and it collides
    with the canopy, trunk, ground, rolls and earlier strips.
  - Its frame lies flat on contact and twists where it hangs free.
  - The low mesh is a box section with the crumple, width and tear treatment described above.
  - The hi-poly is the low strip plus bounded detail.
  - Each strip is baked only against its own hi-poly (2x supersampled). Any texel whose baked normal tilts more
    than about 48 degrees is treated as a miss and refilled from that strip's own neighbouring texels. The result
    is 0 inverted normal texels.

## Review renders (this folder)
All renders use EEVEE with the player camera: 5 studs eye height, 70 degree vertical field of view, backface
culling, a green ground, a soil bed and the sun.
- Tree:
  - `review_tree_{front,back,side,left}_{25,45}.png`
  - `review_tree_close_twigroll.png`, `review_tree_close_fallenroll.png`
  - `review_tree_under_lookup.png`, `review_tree_close_canopy.png`
- Bush:
  - `review_bush_{front,back,side,left}_25.png`, `review_bush_front_45.png`
  - `review_bush_close.png`, `review_bush_close_roll.png`, `review_bush_close_back.png`
- `review_hi_*.png` are hi-poly bake-source previews.
- `wip\rv\rv_*.png`: the reviewer's own `rv_render.py`, run read-only on the exported FBX files into my folder.
  - Tree: front, back and side at 25 and 45 studs, plus under/back lookups.
  - Bush: front, back and side at 25 and 45 studs, plus the close shots.

## Known limitations
- The leaves exist only in the maps; the silhouette is the lobed low mesh. Leaf edges in the map look slightly
  stair-stepped up close, like serrated leaves.
- Bark close-ups (under about 3 studs) show stair-stepped fissure edges and one abrupt band where the root flare
  meets the trunk. This comes from the bark colour being stored per vertex on the voxel mesh. From 5 studs and
  further it reads as bark.
- On the shadow side the canopy gaps still go dark in EEVEE (the albedo itself has under 1% near-black).
- Where strips cross, the upper strip is lifted up to about 0.2-0.3 stud, which leaves small gaps.
- The bush roll's ground run is hidden behind the roll from straight in front. It shows from the side and in a
  three-quarter view.
- A few small perforation dents show as tiny dark marks on the hanging tails up close.
