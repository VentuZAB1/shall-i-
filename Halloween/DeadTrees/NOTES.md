# Halloween garden: DeadTrees (DeadTree + HauntedTree), 2026-10-12, review round 1 fixes applied

## Files
- **Build scripts** (headless, all procedural; `hkit.py` is imported read-only):
  - `treekit.py`: the kit for this job (noise, skeleton growth, SDF / OpenVDB core, bark, tubes, UVs, webs, silk, bakes, mesh cleanup).
  - `trees.py`: the DeadTree spec and the pipeline steps.
  - `haunted.py`: the HauntedTree spec, the burl face and the dead leaves.
- **Run:**
  - One step per run: `blender.exe -b --factory-startup --python trees.py -- dead build`, then `bake`, `render`, `export`; the same for `haunted`.
  - `_chain.sh` runs all 8 steps (about 11 minutes).
- **Check scripts:**
  - `verify_fbx.py`: re-imports an FBX and lists the parts, triangles and embedded textures.
  - `points_roblox.py`: prints the attachment points below.
  - `wip\chk_wall.py`: the face see-through and wall test.
  - `wip\chk_starts2.py`: the exposed tube-start test.
- **Blends:** `dead_tree.blend`, `haunted_tree.blend`. The game meshes are visible; the hidden `*_hi` objects are the bake sources.
- **Maps:** `maps\` (1024 colour with AO already multiplied in, tangent normal, roughness; `_ao.png` is for reference only).
- **Reports:** `*_build.json`, `*_bake.json`, `*_export.json`, `verify_*.json.txt`.
- **FBX** (all textures embedded, checked by re-import):
  - `C:\cdimp\Halloween_DeadTree.fbx` (11.5 MB)
  - `C:\cdimp\Halloween_HauntedTree.fbx` (12.8 MB)

## What changed in round 2 (answers to REVIEW.md)
**Both trees**
- **Branch-joint bake seams fixed.**
  - Child tubes start well inside their parent:
    - fork children 1.4 x the parent radius back along the parent axis;
    - core-to-tube continuations 1.6 x 0.13 inside the sculpted core.
  - The buried part of every tube is flagged (a "Buried" vertex attribute on the bake source). The bake treats it like a ray miss, so its colour, AO and normal grow in from the visible bark next to it (about 7 % of the Branches texels). The pale bands with black square notches are gone.
  - A tube leaves the core at about 0.9 x its radius and only reaches full size about 2.5 radii further on, so its rim never overhangs the core.
  - The core sculpt is hidden from the branch bake, so it no longer draws a dark AO ring on the tubes.
  - A forking branch necks down inside its fork children, so its flat tube end no longer shows.
- **Mesh cleanup:**
  - No loose parts. The 2-face sliver and the single faces are gone, and small islands at the Trunk / Limbs cut are handed to the part they connect to.
  - No non-manifold or pinched edges. A decimation pinch is cut out and capped.
  - No holes, apart from the two below.
  - The flat ground cap under the trunk is deleted, so the Trunk's bottom at Y -0.25 is open (never visible).
  - Trunk and Limbs each have an open cut edge where they meet; together they close it.
- Softer lichen edges. Thick tubes have 10 sides (8 at radius 0.06-0.1).

**DeadTree**
- **3 cobwebs instead of 2, much bigger,** in three different gaps between the five main limbs. There is a web face-on or near face-on from every side.
- The web picker now scores the web build_web really makes (the best-fit plane of the whole frame and its widths). It rejects webs that a limb passes through and webs that cross each other.
  - In round 1 a crotch whose branches curved out of plane gave a sliver web.

**HauntedTree**
- **The face sits on a burl.**
  - The trunk swells about 0.55 forward (and wider) at face height. The face surface is at Roblox Z of about 1.8-1.9 (nose tip 2.22); the bark above and below is at 1.3.
  - The burl carries the trunk's own bark furrows, and the grain bends around the features.
  - Every feature is carved into solid wood as a blind pocket cut straight back.
- **No see-through from the side.**
  - Test: 410,670 rays from the sides (60-120 deg off the face direction, pitch -25..+25 deg), each aimed at a point inside the eye and mouth pockets. 0 of them pass through (`wip\chk_wall.py`).
  - The side wall, 0.4+ stud behind the face surface, is 0.73-0.97 thick (median).
- **The mouth is watertight.**
  - Thick rolled lips (a 0.14-radius roll, about 0.28 thick).
  - 3 upper and 2 lower fangs. They are solid wooden wedges about 0.2 wide at the root, running the full 0.8 depth of the mouth.
  - The game mesh has no loose parts and no open edges at the face.
- The eyes are almond-shaped and slanted (26 deg, inner corners low) under the V brow. Lichen is kept off the face.
- **The web moved** to the wide fork between the left arm and the central limb (span 4.6 x 3.2). It is built like the DeadTree webs and faces the front.
- The leaves curl and cup more (a 5 x 5 vertex grid instead of 3 folds).

## Axes / pivot
- 1 Blender m = 1 stud.
- **Roblox (X, Y, Z) = (Blender X, Blender Z, -Blender Y).** All points below are already in Roblox axes, relative to the FBX origin.
- **FBX origin = the trunk base centre on the ground (Y = 0).** Every part keeps this origin; use "Set Pivot to Scene Origin".
- The lowest vertices are at Roblox Y -0.25 (the root bottoms). Nothing goes lower.
- **Front = Blender -Y = Roblox +Z.** That is the HauntedTree's face, and roughly the DeadTree hollow.
- The PumpkinEggs NOTES say the lead once saw the importer turn models 180 degrees. If the face ends up pointing away, negate X and Z of every point below.

## Halloween_DeadTree.fbx: gnarled bare tree with a hollow and 3 cobwebs
| Part (MeshPart) | Triangles | Textures | Notes |
|---|---|---|---|
| `DeadTree_Trunk` | 7,256 | 1024 colour / normal / roughness | trunk + 7 root buttresses + lower crotch, about 68 px/stud |
| `DeadTree_Limbs` | 6,157 | 1024 colour / normal / roughness | the 5 crooked limbs above Roblox Y 6.65 |
| `DeadTree_Branches` | 7,647 | 1024 colour / normal / roughness | ~190 branches and twigs (4-10 sided tubes) |
| `DeadTree_Web` | 5,996 | 256 colour | 3 orb webs, real tube strands |
| `DeadTree_WebSilk` | 1,292 | **512 RGBA** | silk mat in each crotch, a tattered drape, a denser pale patch round each hub. Two-sided |
| **Total** | **28,348** | | budget 30,000 |

- **Size (Roblox X x Y x Z): 13.45 x 16.24 x 13.30.** Bounds: X -6.27..7.18, Y -0.25..15.99, Z -6.28..7.03.
- **Look** (unchanged):
  - A crooked flared trunk with root buttresses.
  - Zig-zag limbs with hooked claws.
  - Furrowed bark with bare-wood patches and lichen.
  - Broken stubs.
  - An almond **hollow**: opening centre (0.59, 1.97, 1.11), facing Roblox (+0.47, 0, +0.88).

### Attachment points (Roblox axes, studs, from the FBX origin)
- **Spider thread points:** the underside of a branch. Each has a free drop of 8+ studs and a clear 1.2-stud ring.
  1. (4.40, 5.97, 6.79), branch radius 0.11 (moved: front right, low)
  2. (-5.46, 9.06, -5.69), branch radius 0.12
  3. (5.99, 10.18, -1.77), branch radius 0.13
- **Webs:**
  - "Span" is the planar frame's widest / narrowest width.
  - "Radius" is the hub's distance to the farthest frame corner.
  - Each web has 12 spokes (web 3: 10) and catch spirals.

| Web | Faces | Hub | Plane normal | Span | Radius | Anchors: crotch, branch A, branch B |
|---|---|---|---|---|---|---|
| 1 | front / back (Roblox +-Z, 20 deg) | (1.19, 8.03, -0.53) | (0.07, 0.34, 0.94) | 4.9 x 3.7 | 3.25 | (0.21, 6.43, -0.05), (4.11, 8.99, -1.25), (0.62, 10.94, -1.91) |
| 2 | sides (Roblox +-X, 27 deg) | (-0.93, 7.97, 0.69) | (-0.89, -0.07, -0.45) | 5.2 x 3.5 | 3.52 | (-0.30, 6.55, 0.40), (-2.14, 9.71, 3.52), (0.06, 10.10, -1.16) |
| 3 | diagonal, behind the trunk | (-1.06, 7.20, -1.14) | (-0.72, 0.27, 0.64) | 4.1 x 2.7 | 2.81 | (-0.38, 6.35, -0.26), (-2.44, 7.79, -3.56), (-0.10, 8.90, -1.01) |

## Halloween_HauntedTree.fbx: twisted tree with a face on a burl, dead leaves, 1 web
| Part | Triangles | Textures | Notes |
|---|---|---|---|
| `HauntedTree_Trunk` | 9,049 | 1024 colour / normal / roughness | trunk + burl face + roots |
| `HauntedTree_Limbs` | 4,175 | 1024 colour / normal / roughness | limbs above Roblox Y 7.39 |
| `HauntedTree_Branches` | 7,160 | 1024 colour / normal / roughness | branches + twigs |
| `HauntedTree_Leaves` | 5,852 | 512 colour / normal / roughness | 77 curled dead leaves in 13 clusters + petioles |
| `HauntedTree_Web` | 1,962 | 256 colour | 1 orb web |
| `HauntedTree_WebSilk` | 440 | **512 RGBA** | silk mat + drape + hub patch |
| **Total** | **28,638** | | budget 30,000 |

- **Size (Roblox X x Y x Z): 13.06 x 15.24 x 10.81.** Bounds: X -6.61..6.46, Y -0.25..14.99, Z -5.20..5.61.
- **The face looks along Roblox +Z (Blender -Y).** Measured on the game mesh:
  - **Burl:** about Y 2.2-6.2 and 3.9 wide. The face surface is at Z 1.8-1.9; the nose tip is at (0.09, 4.45, 2.22).
  - **Eye sockets:** centres (-0.53, 4.95) and (0.71, 4.95). They are about 1.2 deep (the bottom is at Z 0.62), with deeper pupil holes.
  - **Mouth:** centre (0.09, 3.50), about 1.6 wide, about 0.8 deep (the bottom is at Z 1.04).
  - **Brow ridge** at Y about 5.4.

### Attachment points (Roblox axes)
- **Spider thread points:** both have an 8+ stud free drop and a clear ring.
  1. (-5.98, 7.76, 1.64), under the left arm, branch radius 0.07
  2. (5.95, 7.63, 1.21), under the right arm, branch radius 0.10
- **Web 1** (left arm / central limb fork, above the face):
  - Hub (-1.33, 8.11, 1.08).
  - Normal (-0.04, 0.51, -0.86). It faces the front and tilts down toward players on the ground, 31 deg off +Z.
  - Span 4.6 x 3.2, radius 2.99, 12 spokes.
  - Anchors: crotch (-0.54, 7.18, 0.61), arm (-3.82, 7.89, 1.27), limb (-0.79, 10.51, 2.83).
- Leaf cluster centres are in `haunted_tree.blend`, as the custom property `clusters` on `HauntedTree_Leaves` (Blender axes).

## Roblox setup (lead)
- **Import:** 3D importer, creator ZAB Studio. Keep the parts together in one Model. The pivot is the FBX origin = the trunk base.
- **SurfaceAppearance:**
  - The colour, normal and roughness maps are embedded and linked in the FBX.
  - If the importer drops the roughness map, assign `maps\<Part>_rough.png` by hand.
  - **`*_WebSilk`: `SurfaceAppearance.AlphaMode = Transparency` is REQUIRED.** With Overlay it shows as an opaque sheet.
  - `*_Web` needs no alpha.
- **Collision:** `*_Trunk` CanCollide true, CollisionFidelity Hull. Every other part: CanCollide / CanTouch / CanQuery false. All parts Anchored.
- **RenderFidelity:** Precise on `*_Branches`, `*_Leaves`, `*_Web`, `*_WebSilk`. Trunk and Limbs can stay Automatic.
- **CastShadow:** true for Trunk / Limbs / Branches / Leaves, false for Web / WebSilk.
- **Spider:** scale `Halloween_Spider` (6.75 studs tall) to about 0.45-0.55. Hang it 1-3 studs below a thread point.
- **No Neon or emissive anywhere.** Nothing moves.

## Review renders
- **My render step** (this folder; EEVEE, eye height 5, vfov 70, backface culling, light-green bed (92, 168, 70) of radius 7.5, orange 2 x 1 x 5 player block):
  - DeadTree:
    - `review_dead_{front,back,left,right}_25.png`, `review_dead_{front,left}_45.png`, `review_dead_q34_40.png`
    - `review_dead_hollow_7.png`, `review_dead_web{0,1,2}_close.png`, `review_dead_joint{0,1,2}_below.png`
  - HauntedTree:
    - `review_haunted_{front,back,left,right}_25.png`, `review_haunted_{front,left}_45.png`, `review_haunted_q34_40.png`
    - `review_haunted_face_{18,8,q34_15}.png`, `review_haunted_face_side_{L,R}_6.png`, `review_haunted_mouth_low_4.png`
    - `review_haunted_web0_close.png`, `review_haunted_joint{0,1,2}_below.png`
- **The reviewer's `review\rv.py` shot set, run on the final FBX:** `wip\rv3_dead_*.png`, `wip\rv3_haunted_*.png`.
  - Its web close-ups (`close_web*`) still aim at the round-1 web positions.

## Known limitations
- **Core-to-tube transitions:** where a branch leaves the sculpted core and continues as a tube, a thin crease line remains. It is a shading step plus a faint AO line. You see it within about 5 studs, looking up.
  - The tube starts themselves are hidden.
  - `wip\chk_starts2.py`: on the HauntedTree, 1 of 19 core-cut tube starts (Roblox (-1.58, 8.86, -1.28)) has half its start ring just outside the decimated core; the DeadTree has none. On both trees, the square corners of some 4-sided twig forks (radius about 0.02) poke out of their parent by about 0.001.
- **Thick tubes** have 10 sides and visible kinks at their bends within about 5 studs. The root flare is still the smooth "melted skirt". Both were optional in the review and are unchanged.
- **The face game mesh** (decimated to about 9k triangles for the whole Trunk part) shows some flat facets on the lips and chin within about 4 studs. The read at 8-45 studs is clean.
- **The reviewer's `review\chk_tunnel.py`** now reports "gaps": its face slab runs through the new burl and crosses the blind pockets sideways (in through one cheek, across the pocket, out through the other). It cannot tell a blind pocket from a tunnel. Use the see-through test above instead.
- **The DeadTree's 3 webs** all hang in the main crotch area (hubs about 2-2.5 apart, in different limb gaps). It reads as one cobwebbed crown. No other crotch is big enough for a 2.5+ radius web.
- **Bake miss figures** in `*_bake.json` (0.15-0.37) count the empty UV space around the islands, not holes in the bake.
- **Twig tips** taper to 0.012-0.02 radius, so they fade out at 50+ studs. This is intended.
- **Rebuilds:** webs and spider points are chosen by the script (fork scoring + raycast clearance). The JSON reports hold the current values.
