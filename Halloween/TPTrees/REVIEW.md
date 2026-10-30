# TPTrees: independent review (2026-10-12)

The reviewer is an independent art-review agent. It did not build these assets and changed none of the builder's files.

## FINAL VERDICT (after round 2)

| Asset | Final verdict |
|---|---|
| `Halloween_TPTree.fbx` | **PASS** |
| `Halloween_TPBush.fbx` | **PASS** |

Every round-1 FIX item is resolved (6 on the tree, 5 on the bush). What is left is small optional polish, visible only within a
few studs. Neither asset needs another round.

---

## Round 2

Reviewed files (snapshotted to `review\fbx_r2\`; the md5 sums match the builder's NOTES):
- `C:\cdimp\Halloween_TPTree.fbx` (13:31), md5 `b75689f88724241d27bfaba107c4c228`
- `C:\cdimp\Halloween_TPBush.fbx` (13:41), md5 `a8fc1e97d5b8859eed76556479abee34`

Method: as in round 1. The same `rv_check.py` checks, the same `rv_render.py` player camera (5 studs up, 70 degree vertical FOV,
backface culling, a 5-stud reference block), front, back and side at 25 and 45 studs plus left at 25, and close-ups at the new
roll positions. Renders are in `review\renders_r2\`; data is in `review\r2\`.

### Technical (round 2): pass on both

| Check | TPTree | TPBush |
|---|---|---|
| Triangles | Trunk 5,200 / CanopyA 8,257 / CanopyB 8,341 / TP 7,880 = **29,678 / 30,000** | Canopy 7,299 / TP 2,572 = **9,871 / 10,000** |
| Textures | 4 x 3 maps at 1024, packed and wired correctly; alpha 1.0; no emission; metal 0 | canopy 1024, TP 512; same |
| Size, Roblox X x Y x Z | 14.25 x 15.95 x 14.20 (target 14 x 16 x 14) | 5.51 x 4.75 x 6.49. The Z includes the roll and paper on the soil; the foliage alone is 5.50 x 4.70 x 5.51. This fits the Bush and BushSmall beds |
| Pivot | trunk-base centre at Z = 0, min Z -0.156 | min Z -0.05, base centred |
| Near-black canopy texels (luma below 0.10) | 0.4% (was 19-20%) | 0.0% (was 17.6%) |
| Leaf roughness, sampled on the surface | mean 0.88 (p5 0.83) | mean 0.90 (p5 0.85) |
| Paper clipping into other parts | 0.9% of TP vertices (was 3.2%), max 0.14 | 3.0%, max 0.13 |
| Paper floating more than 0.4 above a surface | 0.85% of TP vertices, mostly on the canopy top (not visible) plus paper snagged around twigs; it reads as caught paper (`rv_tree_gap_frontleft*.png`) | 0% |

### Round-1 FIX items: status

**Tree**
1. Paper reads as paper: **resolved.** Torn zig-zag ends, ±13% width, real folds and kinks, softened edges. It reads as
   crumpled TP from 25 studs (`rv_tree_front_25_crop.png`) and up close (`rv_tree_close_rim_back.png`,
   `rv_tree_close_twigroll_34.png`).
2. Readable rolls: **resolved.**
   - The twig roll shows its core hole, with the twig through it, from the front, three-quarter and under views
     (`rv_tree_close_twigroll.png`, `rv_tree_under_lookup.png`).
   - The fallen roll and its trailing sheet read at 25 and 45 studs from the front, side and left (`rv_tree_close_fallenroll.png`).
3. Paper on every side: **resolved.** Rim festoons and long tails read from the front, back, side and left at 25 and 45 studs
   (`rv_tree_back_45_crop.png`, `rv_tree_side_45_crop.png`, `rv_tree_left_25_crop.png`).
4. Balloon canopy: **resolved.** The lobed leaf clusters break the silhouette from every side (`rv_tree_close_canopy.png`). The
   underside smear is much reduced and no longer stands out.
5. Glossy leaves: **resolved.** There is no milky pink film from below (`rv_tree_under_lookup.png`, `rv_tree_diag_canopy_under.png`).
6. Near-black gaps: **resolved.** The gaps read as warm red-brown depth, and front-lit colour is rich red, orange and amber.

**Bush**
1. Sack in straps: **resolved.** There is no cross on top: diagonal throws, a loose loop and mid-air torn tails
   (`rv_bush_front_25_crop.png`, `rv_bush_back_25_crop.png`, `rv_bush_close_right.png`). It now reads as a TP'd bush from all four
   sides.
2. Paper quality: **resolved**, the same treatment as the tree.
3. Roll connection: **resolved.** The sheet wraps the roll and comes off its outer surface, with an unrolled end on the soil
   (`rv_bush_close_roll_34.png`, `rv_bush_close.png`).
4. Blob silhouette: **resolved.** The outline is lobed and asymmetric, the bottom rim is clean, and the smears are gone
   (`rv_bush_close.png`, `rv_bush_gap_loop.png`).
5. Gloss and gaps: **resolved.** The leaves are matte, and the gaps are deep green-brown.

### Optional polish (round 2; none of it blocks)
- **Tree, perforation dents.** A few show as tiny dark rectangular marks on the hanging tails, only within about 10 studs
  (`rv_tree_close_twigroll_34.png`, `rv_tree_close_trunk.png` top right).
- **Tree, twist notch.** Where an over-the-top strip twists across a crease at the top-back-left (about Blender (-2.85, 3.1,
  12.8)), there is a small self-intersection notch. It shows only when zoomed (`rv_tree_gap_backleft.png`).
- **Tree, dark pocket.** One deep crease between lobes on the upper-left front reads as a dark pocket at 25 studs
  (`rv_tree_front_25_crop.png`). Lightening the AO in that crease would soften it.
- **Tree, stray sliver.** A stray 7-vertex sliver is left in `Trunk` at Blender (3.15, 0.28, 9.65), inside the canopy. It is
  harmless; delete it on the next export.
- **Tree, bark.** The close-up bark is still a painted-looking pattern with stair-stepped fissures, and there is a band where the
  root flare meets the trunk (the builder knows). It is fine from 5 studs and further.
- **Bush, paper tone.** The bush paper is slightly greyer than the tree's: median albedo luma 0.70 against 0.86, from grime and AO
  on the outward face of the roll strip. It reads white in sun, but if the two stand side by side, halve the grime so they match.
- **Bush, left view.** From the left, the shoulder strip's two tails hang parallel and vertical (`rv_bush_close_left.png`), a faint
  echo of the old "straps". Angling one tail would remove it.

### Round 2 render paths (`review\renders_r2\`)
**Tree**
- Player view, full frame and crop: `rv_tree_{front,back,side}_{25,45}.png` and `rv_tree_left_25.png`, each with a matching
  `_crop.png`.
- Close-ups:
  - rolls: `rv_tree_close_twigroll.png`, `rv_tree_close_twigroll_34.png`, `rv_tree_close_fallenroll.png`
  - canopy: `rv_tree_close_canopy.png`, `rv_tree_close_rim_front.png`, `rv_tree_close_rim_back.png`
  - from below: `rv_tree_under_lookup.png`, `rv_tree_back_close_lookup.png`, `rv_tree_diag_canopy_under.png`
  - trunk: `rv_tree_close_trunk.png`
- Floating-paper checks: `rv_tree_gap_frontleft.png`, `rv_tree_gap_frontleft_b.png`, `rv_tree_gap_backleft.png`,
  `rv_tree_left_12.png`.

**Bush**
- Player view, full frame and crop: `rv_bush_{front,back,side}_{25,45}.png` and `rv_bush_left_25.png`, each with a matching
  `_crop.png`.
- Close-ups:
  - all round: `rv_bush_close.png`, `rv_bush_close_back.png`, `rv_bush_close_left.png`, `rv_bush_close_right.png`
  - roll: `rv_bush_close_roll.png`, `rv_bush_close_roll_34.png`
  - top: `rv_bush_diag_top.png`
- Floating-paper checks: `rv_bush_gap_loop.png`, `rv_bush_gap_right.png`.

Reproduce: `set RV_ROUND=2` (diagnostics: `RV_ROUND=2d`), then
`blender -b --factory-startup --python rv_render.py -- fbx_r2\Halloween_TPTree.fbx tree renders_r2` (or `... TPBush.fbx bush ...`).

---

## Round 1 (history)

Reviewed files (snapshots in `review\fbx\`):
- `C:\cdimp\Halloween_TPTree.fbx` (11:53), md5 `5f1c30e27b44d425d1861f530b44f8f2`
- `C:\cdimp\Halloween_TPBush.fbx` (12:01), md5 `079af94957734319f1dab12368333b22`

| Asset | Round-1 verdict | Technical (budgets, scale, pivot, maps) | Art |
|---|---|---|---|
| `Halloween_TPTree.fbx` | **FIX** | passes | 6 fix items |
| `Halloween_TPBush.fbx` | **FIX** | passes | 5 fix items |

Both assets are technically clean and ready to import. Both FIX verdicts are about the look. On the tree, the toilet paper reads
as white ribbons, no roll is visible from the ground, and the canopy reads as smooth balloons with a leaf print. On the bush, the
paper is laid out so that the bush looks like a sack tied up with straps.

### Round 1: technical checks (fresh headless import, Blender 5.2.2)

| Check | TPTree | TPBush |
|---|---|---|
| Triangles per part | Trunk 7,199 / CanopyA 7,270 / CanopyB 7,328 / TP 7,340 | Canopy 7,600 / TP 2,172 |
| Total vs budget | **29,137 / 30,000**, pass | **9,772 / 10,000**, pass |
| Embedded textures | 4 x (albedo, normal, rough) at 1024, packed, wired to Base Color, Normal Map and Roughness | Canopy 1024, TP 512, packed, wired correctly |
| Albedo alpha | 1.0 everywhere, so the default AlphaMode is safe | 1.0 everywhere |
| Emission / metal | none / 0 | none / 0 |
| Unit convention | object scale 0.01, UnitScaleFactor 1.0. This matches the accepted `HalloweenHead.fbx`, so 1 local unit = 1 stud | same |
| Size, Roblox X x Y x Z | **14.34 x 16.09 x 14.14** against 14 x 16 x 14 (TreeRound beds are 13-14 x 15-16 x 14-15), pass | **6.22 x 4.91 x 5.86** against 6 x 5 x 6, pass |
| Pivot | origin at the trunk-base centre (lowest-ring centroid 0.01, 0.07), min Z -0.153, pass | min Z -0.079, base centred, pass |
| Normals / UVs | outward (positive signed volumes); UVs inside 0-1; texel density canopy ~43, trunk ~54, TP ~73 px/stud with no stretched areas | canopy ~73, TP ~67 px/stud; about 7% of TP area is at half density (the rolls), which is fine |
| TP floating | negligible (0.05% of TP vertices more than 0.4 above the surface beneath them); no floating paper seen from eye height | none seen |
| TP clipping | 3.2% of TP vertices more than 0.04 inside other parts (max 0.29). This is mostly the two deliberately lodged rolls and strips dipping into crevices on the canopy top (z about 13.5), which can't be seen from the ground | 5.8% (max 0.24), at the crossings on top; this reads as tucked-in paper |

Data: `review\check_tree.json`, `review\check_bush.json`, `review\log_tpdark_*.txt`.

**TP "dark spots".** About 25-30% of the TP albedo is at about half brightness (luma ~0.5-0.6 against ~0.88). I traced it: it is
the AO on the strip undersides that press into the foliage (60-85% of those faces), which are hidden. The hanging tails are 92%
full-bright on both sides, so this is not a visible fault. The only visible dark spots are small geometry notches at folded strip
ends (see the optional polish lists).

### Round 1: how I rendered (player view)

- Lighting: `hkit.review_setup` (the same sky fill and warm sun the builders use), plus a green grass plane and a brown soil disc
  (r 8.6 for the tree, 4.2 for the bush).
- Reference: a grey **2 x 1 x 5 stud block**, about the size of a Roblox character.
- Engine and camera: EEVEE at 48 samples, 1600 x 900, Roblox's default **70 degree vertical FOV**, camera **5 studs up**,
  looking level or slightly up.
- **Backface culling on.**
- Shots: front (-Y), back (+Y) and side (+X), each at 25 and 45 studs, plus close-ups.
- `*_crop.png` files are the asset's pixels exactly as a player sees them on a 900p screen.
- Lighting caveat: the sun comes from the front-right, so the back shots are backlit, and Blender's fill is weaker than a typical
  Roblox OutdoorAmbient. I did not judge colour from the backlit views alone. The gloss and gap findings below rest on map
  statistics and controlled A/B renders.

---

### Round 1: Halloween_TPTree.fbx, **FIX** (resolved in round 2)

**Read at 40-45 studs:** from the front, an autumn tree with white streamers. The prank idea mostly comes through the hanging tails.
From the back and sides the read is weaker. It is not yet an instant "toilet-papered tree": the paper looks like ribbon, and no roll
can be seen from the ground. Front-lit colour is good: rich red, orange and amber (about 46% red, 49% orange, 5% amber), not muddy.

1. **The TP reads as clean white ribbons or straps, not soft paper.** This affects all 13 strips. See `rv_tree_under_lookup.png`,
   `rv_tree_close_canopy.png`, `rv_tree_close_fork.png`, and at 25 studs `rv_tree_front_25_crop.png`.
   - Why it reads that way:
     - every strip is exactly 0.45 wide with straight parallel edges;
     - the ends are cut square, like box tabs (for example both ends of the front festoon);
     - hard 90-degree box edges outline every strip;
     - the crease lines, evenly spaced every 0.5 stud, read as tape segments or bandage;
     - the crinkle exists only in the normal map and disappears beyond about 10 studs;
     - the tails twist in smooth, wide helices, like satin ribbon.
   - Change:
     - (a) Replace every square end with a ragged tear: 3-5 irregular teeth over the last 0.15-0.3 stud, slightly curled.
     - (b) Vary the width by +/-10-15% and give the edges a gentle waviness.
     - (c) Put real crumple into the low-poly:
       - small cross-folds and kinks along the hanging tails (0.04-0.08 stud, every 0.6-1.2 stud);
       - a few sharp kinks where a tail changes direction;
       - bunching where a strip goes over a branch.
     - (d) Round the strip edge normals (or add a tiny bevel), so the edges don't draw a crisp outline.
     - (e) Make the perforation creases subtler and less regular, and add about +/-5% off-white value variation, with faint warm
       grime where the paper touches bark or leaves.
   - Keep: albedo about (236, 232, 220), roughness about 0.86, no alpha, thickness of 0.06 or more.

2. **Neither roll can be seen from the ground.**
   - Roll A (in the fork, Roblox (0.43, 6.29, 0.65)) is wrapped by its own strip and screened by the front tails. From every
     eye-height angle it reads as a white knot, not a roll. See `rv_tree_close_fork.png` and `rv_tree_diag_rollA_side.png`.
   - Roll B (Roblox (-2.98, 10.73, -5.75)) sits about 1.5 studs inside the canopy's top-back and is invisible from eye height at
     12, 25 and 45 studs. See `rv_tree_close_rollB.png` and `rv_tree_back_25_crop.png`.
   - Change:
     - Put at least one roll on an outer lower branch or the canopy rim, 7-10 studs up on the front side, with its end face and
       hole showing and its tail unrolling downward.
     - Scale the rolls to about 0.9-1.0 diameter. The current 0.68 is only 6-10 px at 25-45 studs.
     - Optionally, add a fallen, half-unrolled roll on the soil by the trunk. It is cheap and reads instantly as TP.
     - Update the NOTES attachment points.

3. **The paper is concentrated on the front, and the loops are hidden.**
   - The front (-Y) has the festoon and 3 over-the-top strips. From the back (+Y) and the side, only 2 vertical strips plus thin
     tails read. See `rv_tree_back_45_crop.png` and `rv_tree_side_45_crop.png`.
   - The 2 "sagging loops between limbs" hang under the canopy and can't be seen beyond about 10 studs.
   - The trees stand in round beds and are seen from every side.
   - Change:
     - Add 2-3 festoons sagging along the outer canopy rim on the back and both sides: 7-10 studs up, with a 0.8-1.5 stud sag.
     - Add 2-3 longer tails on the back and sides that end 2-4 studs above the ground.
     - Move the two inner loops out to the rim. For the triangle budget, see item 4.

4. **The canopy reads as smooth balloons with a leaf print.** See `rv_tree_front_25_crop.png`, `rv_tree_side_25_crop.png` and
   `rv_tree_front_45_crop.png`.
   - Every clump outline is a perfectly smooth sphere arc, because the leaves exist only in the maps. The hi-poly
     (`review_hi_tree_25studs.png`) had a broken, leafy outline that the game mesh lost.
   - Under about 10 studs the clump outlines are visibly faceted (`rv_tree_under_lookup.png`, `rv_tree_close_rollB.png`). The
     faceted bottom outline also casts straight-edged light patches onto the trunk (`rv_tree_diag_trunk_noTP.png`). I checked
     that pale patch: it is sunlight through a canopy gap, not a bake fault.
   - Change:
     - Before decimating the low-poly, displace it with lobed leaf-cluster bumps: lobes of about 1.0-1.5 stud, amplitude 0.2-0.3
       stud, strongest on the outer and lower rims that players see against the sky. Then re-bake. Keep the clumps; only break
       their contours.
     - Pay for the triangles by trimming the Trunk (7.2k, though most upper limbs are hidden) to about 5.5k and by coarsening the
       straight TP spans that lie on the canopy. A rough split: Trunk 5.5k, TP 7k, canopy halves 8.5k each.
   - Also: the leaves on the lower bellies of the clumps bake into horizontal smears. See the top band of `rv_tree_close_fork.png`
     and the lower rims in `rv_tree_diag_canopy_under.png`; they are obvious when you stand under the tree. Fix the cage or ray
     distance there, or turn the hi-poly underside leaves so they face the surface instead of grazing it.

5. **The leaves are too glossy, which gives a milky pink-lilac film on shaded and grazing areas.** See
   `rv_tree_under_lookup.png`, `rv_tree_diag_canopy_under.png` and `rv_tree_close_rollB.png`.
   - The leaf roughness is 0.51-0.68 (mean 0.65).
   - A/B check: with the canopy roughness forced to 0.9 the film is gone, and the shaded leaves read as red and orange leaves.
     Compare `renders\variant_rough09\rv_tree_diag_canopy_under.png` with `renders\rv_tree_diag_canopy_under.png`.
   - The albedo itself is fine (`renders\variant_albedo\...`).
   - Change: leaf roughness 0.82-0.9, gaps 0.95.

6. **The gaps between leaves are near-black.**
   - 19-20% of the canopy surface has albedo luma below 0.10 (`check_tree.json`).
   - From 25-45 studs this reads as black speckle across the crown. On the shaded side the crown turns muddy maroon-brown
     (`rv_tree_back_25_crop.png`, `rv_tree_back_45_crop.png`).
   - Change:
     - Lift the gap colour to a deep warm red-brown, about sRGB (75-90, 28-35, 18-22).
     - Keep the AO for depth, but cap how far it darkens the gaps.
     - Aim for less than 8% of the surface below luma 0.10.
     - Keep the leaf hues as they are.

#### Optional polish (tree, round 1)
- Close up, the bark reads like a painted pattern: evenly spaced wavy dark lines with stair-stepped (aliased) edges on smooth tubes,
  with little relief (`rv_tree_diag_trunk_noTP.png`). It is fine from 25 studs. Suggested: deeper fissures in the normal map, an
  anti-aliased fissure mask, and more variation between bark plates.
- The folded end of the front festoon has a small dark triangular notch, a self-intersection at about Blender (-1.6, -5.7, 8.9)
  (`rv_tree_diag_festoon_end.png`). You can only see it within a few studs, and it goes away if the ends are rebuilt as tears
  (item 1).
- Leaf edges in the map are stair-stepped under about 8 studs.
- CanopyA contains a stray 4-vertex sliver at Blender (2.88, 3.18, 10.44). It is harmless; delete it.

---

### Round 1: Halloween_TPBush.fbx, **FIX** (resolved in round 2)

**Read at 40-45 studs:** a round bundle tied with white straps, like a sack or a wrapped parcel, rather than a TP-pranked bush
(`rv_bush_front_45_crop.png`, `rv_bush_front_25_crop.png`). Size, colour mix and budget are fine: 37% green, 33% amber, 25%
orange, 6% red.

1. **The TP layout makes the bush look like a sack in a strap harness.** See `rv_bush_close.png`, `rv_bush_diag_top.png` and
   `rv_bush_side_25_crop.png`.
   - The three strips meet in a symmetric cross on top, then run straight down the sides to the soil like meridians, on every side.
   - Change: re-drape it so it looks thrown.
     - Lay 1-2 strips diagonally across the top, not as a cross.
     - Let at least one loose loop sag off a side.
     - Let 1-2 tails hang free and end in mid-air, 0.5-1.5 studs above the soil, with torn ends.
     - Let slack, crumpled paper catch on the foliage.
     - Only the strip coming from the roll should reach the ground.

2. **The paper problem from tree item 1 is worse here, because players walk right past a 5-stud bush.** The strips look like padded
   straps: the perforation creases read as quilting stitches and the ends are boxy (`rv_bush_close.png`, `rv_bush_close_roll.png`).
   - Change: apply the same torn ends, width variation, crumple and soft edges as tree item 1.
   - Budget: 228 triangles are left under 10k. If you need more, take them from the canopy's hidden underside.

3. **The paper doesn't come off the roll.** The strip enters the top of the ground roll as a narrow twisted tab, as if clipped on
   (`rv_bush_close_roll.png`).
   - Change: make the sheet leave the roll tangentially from its outer surface, lie on the soil for a short run, then climb the
     bush. Tip the roll slightly, or show a few loose layers.

4. **The canopy is a smooth, symmetric, pear-shaped blob.**
   - There is no leaf-cluster breakup in the outline, so together with the straps it reads as a stuffed sack.
   - The lower outline is faceted, and the bottom rim bakes into dark blue-black smears where it meets the soil (`rv_bush_close.png`,
     `rv_bush_diag_end_right.png`).
   - Change: as tree item 4, apply lobed leaf-cluster displacement (lobes of 0.6-1.0 stud, amplitude 0.15-0.25), make the outline
     less symmetric, and re-bake the bottom rim.

5. **Leaf gloss and gaps have the same problems as tree items 5 and 6.**
   - The leaf roughness is 0.51-0.67, which gives a milky grey-pink sheen on the shaded top (`rv_bush_close_back.png`).
   - 17.6% of the surface is near-black gaps (luma below 0.10).
   - Change: leaf roughness about 0.85-0.9, and lift the gap colour to a deep green-brown.

#### Optional polish (bush, round 1)
- The autumn colour is a top-to-bottom gradient (orange and yellow on top, green below) rather than "green turning autumn at the
  tips". Consider warming the outer tips of each lobe so the change reads per cluster.
- A crumpled strip end on top shows as a grey wad with dark facets (`rv_bush_diag_top.png`, right side).
- After the re-drape, re-check the paper that sinks into the foliage (now 6%, up to 0.24 stud deep).

---

### Round 1 render paths
All renders are in `C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\TPTrees\review\renders\`.

**Tree**
- Player view, full frame and crop (`*_crop.png`):
  - `rv_tree_front_25.png`, `rv_tree_front_45.png`
  - `rv_tree_back_25.png`, `rv_tree_back_45.png`
  - `rv_tree_side_25.png`, `rv_tree_side_45.png`
- Close-ups:
  - `rv_tree_under_lookup.png` (player by the trunk, looking up)
  - `rv_tree_back_close_lookup.png`
  - `rv_tree_close_fork.png`, `rv_tree_close_rollB.png`, `rv_tree_close_canopy.png`
- Diagnostics:
  - `rv_tree_diag_trunk_noTP.png`, `rv_tree_diag_trunk_noTP_back.png`
  - `rv_tree_diag_festoon_end.png`, `rv_tree_diag_rollA_side.png`, `rv_tree_diag_canopy_under.png`
- A/B variants of the diagnostics: `variant_rough09\` (canopy roughness 0.9), `variant_albedo\` (albedo only),
  `variant_nonormal\` (normal map unplugged).

**Bush**
- Player view, full frame and crop:
  - `rv_bush_front_25.png`, `rv_bush_front_45.png`
  - `rv_bush_back_25.png`, `rv_bush_back_45.png`
  - `rv_bush_side_25.png`, `rv_bush_side_45.png`
- Close-ups: `rv_bush_close.png`, `rv_bush_close_back.png`, `rv_bush_close_roll.png`
- Diagnostics: `rv_bush_diag_top.png`, `rv_bush_diag_end_right.png`

### Round 1 reproduce
All commands run from `review\`. The scripts are reviewer-owned and import `hkit` read-only.
```
blender -b --factory-startup --python rv_check.py  -- fbx\Halloween_TPTree.fbx tree . C:\cdimp\HalloweenHead.fbx
blender -b --factory-startup --python rv_render.py -- fbx\Halloween_TPTree.fbx tree renders            (all shots)
blender -b --factory-startup --python rv_render.py -- fbx\Halloween_TPTree.fbx tree renders diag_all   (diagnostics)
set RV_VARIANT=rough09|albedo|nonormal   (A/B material variants of the diagnostics)
blender -b --factory-startup --python rv_tpdark.py -- fbx\Halloween_TPTree.fbx 6.42   (where the darker TP albedo sits)
```
