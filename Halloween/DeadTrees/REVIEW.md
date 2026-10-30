# DeadTrees: independent review, round 1 (2026-10-12)

Reviewer: independent art-review agent. I imported each FBX fresh in headless Blender 5.2.2, measured it, and rendered
it in a hub-like scene. The builder's files are untouched. My scripts, stats, renders and crops are in `DeadTrees\review\`.

## Round 2 (final, 2026-10-12)

The re-exported FBX files were copied byte-identical (md5 checked) to `review\r2\src\` and re-checked with the same
scripts, now with `RV_ROUND=2`. That run uses the new spider points, aims the web cameras at the new web hubs, moves the face
cameras forward for the burl, and adds 45 deg face views and look-up joint shots. The scene is unchanged: eye height 5,
vertical FOV 70, light-green bed, warm sun, backface culling on, silk alpha-blended.

### Final verdicts

| Asset | Final verdict |
|---|---|
| `Halloween_DeadTree.fbx` | **PASS** |
| `Halloween_HauntedTree.fbx` | **PASS** |

### Round-1 FIX items: all resolved

| Item | Result | Evidence (`review\r2\`) |
|---|---|---|
| Dead 1: webs too small, all facing one side | **Resolved.** 3 orb webs (4.9 x 3.7, 5.2 x 3.5, 4.1 x 2.7) in three limb gaps. At 25 studs a web reads from every side. At 40-45 studs the crown reads as cobwebbed from the front, back, both sides and 3/4. Up close they are clean orb webs (hub, spokes, spiral, silk). | `r2_dead_{front,back,left,right}_25.png`, `z2_dead_45_sheet.png`, `r2_dead_web1_front_8.png`, `r2_dead_web2_side_8.png`, `r2_dead_web3_8.png` |
| Dead 2: branch-base bake seams | **Resolved.** No pale bands or black square notches at any fork, looking up from 4 studs on all 4 sides. | `r2_dead_joint_up_{front,back,left,right}_4.png`, `z2_dead_joint_right.png` |
| Haunted 1: broken mouth | **Resolved.** `HauntedTree_Trunk` is one connected piece (round 1: 11 pieces). The only open edges are the planned Trunk/Limbs cut and the removed ground cap; there are none at the face. Thick rolled lips and solid fangs; no shards from either low 3/4 angle. | `r2_haunted_mouth_low_4.png`, `r2_haunted_mouth_lowL_4.png`, `r2_haunted_face_5.png` |
| Haunted 2: see-through eyes / mouth | **Resolved.** From both sides at 6 and 25 studs and at 45 deg, the eye and mouth pockets read as dark notches. No sky or grass shows through them. Renders with culling off look the same. | `r2_haunted_face_side_{L,R}_6.png`, `r2_haunted_face_side_{L,R}_25.png`, `r2_haunted_face_q45{L,R}_6.png`, `z2_side_R6_profile.png`, `z2_side_L6_profile.png`, `z2_side25_pair.png`, `r2nocull_haunted_face_side_{L,R}_6.png` |
| Haunted 3: web read as a ladder | **Resolved.** A real orb web (spokes + spiral, fan-shaped, about 4.6 x 3.2) in the left-arm fork, facing the front. It reads as a cobweb at 8, 18 and 25 studs and as a white web patch at 45. | `r2_haunted_web_front_8.png`, `r2_haunted_face_18.png`, `r2_haunted_front_25.png`, `z2_haunted_45_sheet.png` |
| Haunted 4: branch-base bake seams | **Resolved.** The one tube start the builder flagged, at Roblox (-1.58, 8.86, -1.28), is not noticeable. Dark stripes at the right crotch are bark furrows plus twig shadows, not a bake fault: checked with shadows off. | `r2_haunted_joint_up_front_4.png`, `r2_haunted_start_flagged_4.png`, `z2_h_stripes.png`, `z2_h_stripes_noshadow.png` |

### The look (round 2)
- **DeadTree:** the round-1 strengths are kept: crooked, natural silhouette, grey-brown bark with cool lichen, and a dark hollow. Now the cobwebbed crown is the Halloween read at 40 studs from any angle.
- **HauntedTree:** the burl makes the face much stronger.
  - Almond eye pockets under a heavy V brow, a gnarled nose, and a fanged open mouth that read at once from 18-45 studs (`r2_haunted_face_18.png`, `r2_haunted_front_25.png`).
  - From 3/4 views at 6 studs it is a menacing carved-wood face, cool and not goofy (`r2_haunted_face_q45{L,R}_6.png`).
  - The leaves curl more and add a warm red / rust accent.

### Technical re-check (all PASS; `review\r2\stats_*.json`)

| Check | DeadTree | HauntedTree |
|---|---|---|
| Triangles per part | Trunk 7,256 / Limbs 6,157 / Branches 7,647 / Web 5,996 / WebSilk 1,292 | Trunk 9,049 / Limbs 4,175 / Branches 7,160 / Leaves 5,852 / Web 1,962 / WebSilk 440 |
| Total (budget 30,000) | 28,348 | 28,638 |
| Size, Roblox X x Y x Z | 13.45 x 16.24 x 13.30 | 13.06 x 15.24 x 10.81 |
| Pivot | lowest -0.25, 0 verts below -0.3. Base centroid (0.10, 0.02) | lowest -0.25, 0 verts below -0.3. Base centroid (0.18, -0.02) |
| Textures | all packed. PBR 1024 (Leaves 512) with alpha 1.0; Web 256 alpha 1.0; WebSilk 512 with real alpha (0..1, mean 0.31), wired to Alpha on import | same |
| Face direction | n/a (hollow unchanged) | eye pockets span azimuth 208-330 deg and the mouth 220-312 deg, both centred on Blender -Y = Roblox +Z |
| Spider points (new) | all 3 sit 0.02-0.035 under a branch, with a clear drop to the ground and a clear 1.2-stud ring | both sit 0.001-0.013 under a branch, with a clear drop and a clear ring |
| Topology | no loose parts, no non-manifold edges, consistent winding | same |

`chk_tunnel.py` was not used to decide the see-through question. Its side slab cannot tell a blind pocket from a tunnel, as the
builder noted. The see-through verdict above comes from the eye-height side renders and the culling-off comparison.

### Optional polish left (not blocking; the builder's NOTES list most of these as known)
- **Core-to-tube crease:** a faint shading step where a branch leaves the sculpted core. You only see it from directly underneath, within about 5 studs (`z2_dead_joint_back.png`).
- **Thick branch tubes:** they still kink visibly at bends within about 5 studs.
- **Root flare:** it is still the smooth "melted skirt" on both trees (`r2_dead_close_hollow_7.png`).
- **HauntedTree face mesh:**
  - It shows flat facets on the lips and chin within about 4 studs.
  - The burl narrows into a "neck" under the chin. From close 3/4 views it reads a little like a head set on the trunk; blending the burl's lower edge into the trunk would make it look more grown-in.
- **DeadTree webs:** all three cluster in the main crotch. It reads as one cobwebbed crown, which works; a fourth, small web on an outer fork would only add variety.
- **Lead setup note:** the Trunk bottoms are now open at Y -0.25 (ground cap removed). That is fine under a bed surface with Hull collision, but don't place the trees where the base underside can be seen.

---

# Round 1 (history)

## Round 1 verdicts (superseded by Round 2 above)

| Asset | Verdict | Summary |
|---|---|---|
| `Halloween_DeadTree.fbx` | **FIX** (2 items) | Great silhouette and colour, technically clean. The cobwebs are too small and point the wrong way to carry the "cobwebbed" read at 40 studs. The branch bases show bake seams. |
| `Halloween_HauntedTree.fbx` | **FIX** (4 items) | The face reads well from the front. But the mouth has loose slivers and holes, the eyes and mouth are see-through from the side, and the web looks like a white ladder. The branch bases also show bake seams. |

## Technical checks (both assets PASS)

| Check | DeadTree | HauntedTree |
|---|---|---|
| Triangles per MeshPart (re-import) | Trunk 7,630 / Limbs 6,167 / Branches 6,418 / Web 2,972 / WebSilk 564 | Trunk 8,476 / Limbs 5,014 / Branches 6,004 / Leaves 4,620 / Web 1,518 / WebSilk 288 |
| Total (budget 30,000) | 23,751 | 25,920 |
| Textures embedded | yes, all packed: 1024 colour / normal / roughness, Web 256, WebSilk 512 | yes, all packed: 1024 x3 per bark part, Leaves 512, Web 256, WebSilk 512 |
| Colour-map alpha | PBR colour maps are alpha 1.0 everywhere, so they are safe in Overlay mode | same |
| WebSilk alpha | real alpha: 0..1, 256 levels, mean 0.35. The importer wires it to Alpha | same |
| Import scale | object scale 0.01 on re-import (the hkit cm convention, the same as the other assets), so x100 gives studs | same |
| Size, Roblox X x Y x Z | 13.29 x 16.24 x 13.08 (brief ~13 x 16 x 13; fits the TreeRound slot) | 12.81 x 15.24 x 10.69 (brief ~12 x 15 x 12; fine) |
| Pivot | lowest Z -0.25, 0 verts below -0.3. Trunk base centroid (0.14, -0.01) | lowest Z -0.25, 0 verts below -0.3. Base centroid (0.21, 0.00) |
| Face / front | hollow faces Roblox (+0.47, 0, +0.88), as the NOTES say | eye sockets centred on azimuth 270 deg = Blender -Y = Roblox +Z. Correct |
| Spider points | all 3 sit 0.001-0.017 under a branch, with a clear drop to the ground | both points verified the same way |
| UVs | none outside 0-1. Trunk / Limbs have no stretch. Branches: 9.7 % of area has stretch > 2:1, not visible | same pattern |
| Trunk / Limbs split seam | not visible (Y 6.55) | not visible (Y 7.28) |

The lowest-density 5 % of each trunk's UV area (4.4 px/stud) is the hidden ground-cut cap at Z -0.25 (normals face down),
so that is not a real issue.

---

## Halloween_DeadTree: FIX

**What works (keep it):**
- The silhouette is excellent: crooked, zig-zag limbs, hooked claws, and a natural taper. It is not an L-system broom.
- It reads as a spooky dead tree from every side at 25-45 studs.
- The hollow reads as a real dark hole.
- The colour is warm grey-brown with cool lichen (mean bark sRGB about 85/78/63, saturation 0.27). It is not black mush and not flat grey.
- The trunk / limb / buttress unions are seamless.
- The bark is not stair-stepped or smeared.
- The pivot, budgets and textures are all correct.

1. **The cobwebs don't carry the "cobwebbed tree" read at 40 studs.**
   - **Problem:**
     - Both webs are about 3.4-3.8 studs across and sit high in the crown (Roblox Y 7.2 and 12.8).
     - Both planes face Roblox -X: the normals are (-0.86, -0.06, -0.50) and (-0.85, 0.30, 0.43).
   - **How it shows:**
     - From the front (the hollow side) and the back, both webs are about 60 deg off-axis and almost disappear (`rv_dead_front_25.png`, `rv_dead_front_45.png`, crop `zD_dead_front25_webs.png`).
     - Even from their best side at 45 studs, they are two small pale triangles (`zH_dead_left45.png`).
     - At 7-25 studs they do read as cobwebs (`rv_dead_close_web1_7.png`, `zD_dead_left25_webs.png`), so the design is right. The scale and orientation are the problem.
   - **Change:**
     - Enlarge both webs to a radius of about 2.5-3 (spans of 5-6 studs).
     - Turn web 1 (the main crotch) so its plane faces the front, Roblox +Z, within about 30 deg. Keep web 2 facing the side. That way at least 3 of 4 sides see a web face-on.
     - Optionally add a third, lower web at eye level (Roblox Y 4-6.5, a trunk/limb crotch) facing the back.
     - There is about 6k triangles of headroom. Keep the strands 0.08-0.12 thick.
     - A slightly denser silk near the hub would give each web a pale mass that survives at 40 studs.
2. **Bake seams at branch bases ("crenellated" collars and notches).**
   - **Problem:** Where a child branch tube meets its parent, part of the tube's buried base is exposed. It shows the dark rows of square teeth from the island edges in `maps\DeadTree_Branches_albedo.png`. You see a pale band with black rectangular notches.
   - **Where it shows:**
     - `zF_collar1.png`, cropped from `rv_dead_seam_back_5.png` (upper left, behind the main crotch).
     - Blocky light/dark notches on the left limb in `zF_notch.png`, cropped from `rv_dead_close_web1_7.png`.
   - **Who notices:** a player standing under the tree (5-10 studs), and the owner in Studio.
   - **Change:**
     - Start every child tube deeper inside its parent: at least 1.2-1.5 x the parent radius below the surface.
     - Mask the buried section in the bake so its colour and AO match the neighbouring bark instead of the dark "buried" tone.
     - Square-cut tube end caps should be rounded or hidden.
     - Re-check every fork with a close orbit render (5-8 studs, from below).

**Optional polish (not blocking):**
- The thick branch tubes (radius over about 0.1) have 6 sides, angular kinks at the segment joints, and flat cut ends (`zF_facet.png`, `rv_dead_seam_back_5.png` right side). With the triangle headroom, use 8-10 sides and more rings on the bends for the thickest branches.
- The root buttresses look like a smooth, flat "melted skirt" ending in rounded paddles that rest on the soil (`rv_dead_base_5.png`, `rv_dead_close_hollow_7.png`). Rope-like, knuckled roots that taper and dip below Z 0 would look more gnarled. This is fine from 25+ studs.
- Mesh leftovers, all invisible in renders; clean them up when rebuilding:
  - a loose 36-face chip in `DeadTree_Trunk` at Roblox (-0.29, 1.45, -0.77);
  - single-face slivers or 3-edge holes at (-1.17, 3.03, 0.98) in Trunk and (2.16, 7.02, 0.22) in Limbs.
- The flat ground-cut cap under the trunk (about 364 tris, never seen) can be deleted.
- The lichen patches have fairly hard edges and look a little "camo" up close (`rv_dead_close_bark_6.png`).

---

## Halloween_HauntedTree: FIX

**What works (keep it):**
- From the front, the face reads immediately at 18-45 studs as an angry evil-tree face (`rv_haunted_face_18.png`, `zB_h45.png`):
  - V-shaped brows;
  - dark sockets with dull "dead-eye" pupils;
  - a jagged grin.
- The face is cool and Halloween, not cute.
- The arm-like limbs with hooked claws make a good silhouette.
- The rust / red / plum leaves read as sparse dead leaves and add a nice warm accent at 25-45 studs.
- The pivot, budgets, textures and face direction are all correct.

1. **The mouth geometry is broken: loose slivers, open holes, paper-thin torn lips.**
   - **Problem:**
     - `HauntedTree_Trunk` has **8 loose shards floating at the mouth corners**, at Roblox about (±0.7..1.08, 3.3-3.7, 1.30-1.35). The largest are a 6-face shard and a 4-face shard, each 0.19 tall, at (0.94, 3.52, 1.32) and (-0.76, 3.51, 1.32).
     - There are **20 open boundary edges** (holes) in the mouth, around (0.0-0.1, 3.3-3.7, 1.3).
     - The lips and lower teeth are torn, paper-thin flaps with stair-stepped edges.
   - **Where it shows:** obvious from 3/4 angles at 4-10 studs (`rv_haunted_mouth_low_4.png`, crop `zE_mouthlow.png`; also the top right of `rv_haunted_base_5.png`).
   - **Change:**
     - Make the mouth carve a watertight result.
     - Delete loose parts under about 50 faces after the boolean / remesh.
     - Fill or merge the open edges.
     - Give the lips and fangs real thickness (at least 0.12-0.15 stud) with rounded edges.
     - Rebake the trunk.
2. **The eyes and mouth are see-through from the side (the face reads as a thin hollow mask).**
   - **Problem:** The face is about 2.4 studs wide on a trunk about 2.66 studs across at that height. So the eye sockets and the mouth corners wrap round to the sides and are open there.
   - **How it shows:**
     - From ±X and 3/4 views, the **sky shows through each eye** under the brow and the **grass shows through the mouth corner**.
     - It is visible at 25 studs on the side views (`rv_haunted_left_25.png`, `rv_haunted_right_25.png`; crops `zC_left_mouth.png`, `zC_right_mouth.png`, `zH_haunted_left45.png`).
     - It is obvious at 6 studs (`rv_haunted_face_side_R_6.png`, `rv_haunted_face_side_L_6.png`).
   - **It is not a culling artefact:** it looks identical with backface culling off (`nocull_haunted_face_side_R_6.png`).
   - **Change:**
     - Make each socket and the mouth a blind pocket with a bark wall at least 0.3 stud thick on the outer (temple / cheek) side. Carve straight back (Blender +Y) instead of radially.
     - Better for the 40-stud read too: swell the trunk into a forward "burl" at face height (Roblox Y about 3-5.8, 0.4-0.6 stud forward and a little wider), so the features sit inside solid wood.
     - Verify with side renders from ±X and 45 deg at 6 and 25 studs.
3. **The web reads as a white ladder / fishbone, not a cobweb.**
   - **Problem:** The single web is squeezed into a narrow fork above the left eye. It is a tall, narrow funnel, about 1.4 x 1.7 across and 3.6 tall. Its spiral threads read as rungs between two long side threads.
   - **Where it shows:** `rv_haunted_close_web_7.png`, `rv_haunted_face_8.png`, `rv_haunted_seam_5.png`, crop `zD_h_18_web.png`.
   - **Change:**
     - Move it to a wider fork, for example between the left arm and the central crown limbs.
     - Give it a roughly triangular span of at least 2.5-3 studs each way.
     - Build it like the DeadTree webs (hub + 9-12 spokes + spiral), which read correctly.
     - Point the plane at the front (Roblox +Z) within about 30 deg. Keep the silk part.
4. **Bake seams at branch bases.**
   - **Problem:** the same treekit issue as DeadTree item 2, for example the light/dark notch at the left arm joint (`zG_hjoint2.png`, from `rv_haunted_seam_5.png`).
   - **Change:** the same fix.

**Optional polish (not blocking):**
- The thick branch tubes are faceted and kinked at under 8 studs, the same as on the DeadTree.
- The root flare is a smooth "melted skirt" with rounded lobes (`rv_haunted_base_5.png`). Knuckled, tapering roots would look more gnarled.
- The leaves look like folded flat cards (2-3 planar facets) at under 8 studs (`rv_haunted_close_leaves_R.png`). A little more cup and curl would sell "crispy". They are fine at play distance.
- The lichen patch on the forehead / brow competes with the face. Less lichen on the face area would make the features pop.
- Mesh leftovers:
  - 2 single-face slivers in `HauntedTree_Limbs` near Roblox (-1.0, 7.8, -1.5);
  - a 9-face fragment at (4.96, 7.26, 1.18) in Trunk, the arm underside below the split; check that it is meant to be there.
- The flat ground-cut cap (about 320 tris) can be deleted.

---

## How I tested
- **Script:** `review\rv.py` (modes `stats` and `render`). Extra checks:
  - `chk_density.py`: texel density;
  - `chk_topo.py`: boundary, non-manifold and winding;
  - `chk_loose.py`: loose parts;
  - `chk_tunnel.py`: side-ray gaps.
- **Stats:** `review\stats_dead.json`, `review\stats_haunted.json`.
- **Input:** byte-identical copies of the FBX (md5 checked) in `review\src\`. I imported them fresh with `--factory-startup` and scaled them x100 (the hkit 0.01 convention).
- **Scene:**
  - EEVEE, 1280x900, AgX - Punchy.
  - Gradient sky-blue world: the camera sees a horizon (176, 214, 246) to zenith (92, 160, 232) gradient; the sky fill strength is 0.85.
  - Warm sun key (1.0, 0.94, 0.84), strength 4.2, 42 deg elevation, from front-left.
  - Green grass plane.
  - Light-green bed disc, radius 7.5, about (92, 168, 70).
  - Orange 2 x 1 x 5 stud reference block (a player's height).
- **Cameras:** player eye height 5, level or slightly up, vertical FOV 70.
- **Roblox matching:**
  - Backface culling on for every material.
  - WebSilk rendered alpha-blended from the colour-map alpha (`AlphaMode = Transparency`).
  - Web / WebSilk cast no shadows (as in the NOTES).
  - Normal / roughness maps set to Non-Color.

## Render paths (all in `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\DeadTrees\review\`)

**DeadTree**
- 25 studs: `rv_dead_front_25.png`, `rv_dead_back_25.png`, `rv_dead_left_25.png`, `rv_dead_right_25.png`
- 40-45 studs: `rv_dead_front_45.png`, `rv_dead_left_45.png`, `rv_dead_q34_40.png`
- Close-ups:
  - `rv_dead_close_hollow_7.png`, `rv_dead_close_web1_7.png`, `rv_dead_close_web2_10.png`, `rv_dead_close_bark_6.png`, `rv_dead_close_crown_12.png`
  - `rv_dead_seam_5.png`, `rv_dead_seam_back_5.png`, `rv_dead_base_5.png`, `rv_dead_hole_z3.png`, `rv_dead_limbhole_7.png`, `rv_dead_limbhole_8.png`
- Zoom crops: `zD_dead_front25_webs.png`, `zD_dead_left25_webs.png`, `zH_dead_left45.png`, `zF_collar1.png`, `zF_notch.png`, `zF_facet.png`, `zA_*.png`

**HauntedTree**
- 25 studs: `rv_haunted_front_25.png`, `rv_haunted_back_25.png`, `rv_haunted_left_25.png`, `rv_haunted_right_25.png`
- 40-45 studs: `rv_haunted_front_45.png`, `rv_haunted_left_45.png`, `rv_haunted_q34_40.png`
- Face:
  - `rv_haunted_face_18.png`, `rv_haunted_face_q34_15.png`, `rv_haunted_face_8.png`, `rv_haunted_face_5.png`
  - `rv_haunted_face_side_R_6.png`, `rv_haunted_face_side_L_6.png` (+ `nocull_haunted_*` versions)
  - `rv_haunted_mouth_low_4.png`
- Other close-ups: `rv_haunted_close_web_7.png`, `rv_haunted_close_leaves_L.png`, `rv_haunted_close_leaves_R.png`, `rv_haunted_seam_5.png`, `rv_haunted_seam_back_5.png`, `rv_haunted_base_5.png`, `rv_haunted_back_hole_4.png`
- Zoom crops: `zB_h45.png`, `zB_h18face.png`, `zC_left_mouth.png`, `zC_right_mouth.png`, `zE_mouthlow.png`, `zE_eyes5.png`, `zD_h_18_web.png`, `zG_hjoint1-3.png`, `zH_haunted_left45.png`

I also looked at all 13 of the builder's `review_*.png`. They are shot from above eye height on a brown soil disc, which
hides the side see-through and makes the webs look bigger than they do at eye level.
