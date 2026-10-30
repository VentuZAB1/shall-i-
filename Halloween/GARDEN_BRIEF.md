# Halloween GARDEN - brief for the builder + reviewer agents (2026-10-12)

**Read `Halloween\AGENT_BRIEF.md` first - every rule there applies** (headless Blender 5.2 only, no Studio, no GUI
Blender MCP, no Neon/emissive, no downloads, the kit `hkit.py` read-only, your own folder, FBX to `C:\cdimp`, the
quality bar, triangle limits, Roblox axes, NOTES.md + review renders).

## The owner's request (their words)
"There's Garden decor on the hub, let's change it to halloween stylized ones, do not make them low poly, make them high
quality. Trees with bushes maybe with spiders / webs on it or toilet paper ? Or different variations off it"

## What gets replaced
The hub has 11 garden beds (`Map.Hub.Decor.Gardens`). Each bed is a round soil patch with stylized trees, bushes, rocks,
grass tufts and red toadstools. The lead swaps them in Studio. The originals go to a backup and the red toadstools stay.
Match these footprints (Roblox studs, W x H x D) so the new pieces sit in the same beds:

| Original | Count | Size | Halloween replacement |
|---|---|---|---|
| Blossom (pink cherry tree) | 7 | 10 x 13-14 x 10 | trees (mix of the variants below) |
| TreeRound (round green tree) | 6 | 13-14 x 15-16 x 14-15 | trees |
| Bush | 4 | 5-6 x 6 x 5-6 | bushes |
| BushSmall | 13 | 5-6 x 4-5 x 6-7 | bushes (the lead scales a bush down 0.75-0.85) |
| Rock | 3 | 6 x 4 x 6 | gravestones |
| grass tufts (3 kinds) | ~45 | 2x3x2 up to 5x6x7 | dead grass tufts |

The hub is a bright, saturated, sunny Roblox simulator. **No sky or lighting change** (owner rule). The Halloween look
must come from the models: shapes, colours, webs, toilet paper. Keep it a little playful: think "Halloween decorated
yard" (TP-pranked trees, cobwebs, gravestones), not grim horror. Never low poly, never flat colours, never cute.
Style match: the giant jack-o'-lantern (`Halloween\review_head_front.png`) and the pumpkin eggs
(`Halloween\PumpkinEggs\review_day_25studs.png`). Stylized-realistic HQ PBR with baked normal + AO + colour + roughness,
strong readable silhouettes, exaggerated (but believable) forms.

## Asset list (one builder agent per row; the FBX names are fixed)
1. **DeadTrees** (`Halloween\DeadTrees\`)
   - `Halloween_DeadTree.fbx`: a gnarled, twisted BARE tree, about 13 x 16 x 13. Thick, flared, root-buttressed trunk
     that splits into 3-4 crooked limbs that fork into twisting branches, with fine twig ends. Deep bark grooves, knots,
     a hollow. Bark is dark grey-brown with a cool lichen tint, not black. Add 2 **cobweb sheets** stretched across
     branch forks: real strands plus a separate silk part with an RGBA texture, like the
     `WebsSpiders` webs (see `WebsSpiders\NOTES.md`). Add 2-3 **spider thread points**, the branch spots where the lead
     hangs the existing spider asset, and give them in NOTES.
   - `Halloween_HauntedTree.fbx`: a twisted tree with a **spooky face** formed in the trunk bark, about 12 x 15 x 12:
     hollow eye knotholes and a gaping mouth hollow, dark inside but NOT emissive. The face reads from 40 studs and faces
     Blender -Y, which is Roblox +Z after import. Sparse clusters of dead, curled, dark-red / brown leaves still hang on some
     branch ends (sculpted clusters, not flat cards). One small web. 1-2 spider points.
2. **TPTrees** (`Halloween\TPTrees\`)
   - `Halloween_TPTree.fbx`: a full autumn tree, about 14 x 16 x 14. It has a stylized clumpy canopy (big sculpted leaf
     clumps with leaf-shaped surface detail in the normal map, warm orange / red / amber with darker gaps; no flat leaf
     cards) on a sturdy curving trunk. It is **TP-pranked**: toilet-paper streamers draped over the canopy and branches,
     sagging catenary loops between branches, and long tails hanging down and twisting; 1-2 half-unrolled rolls are stuck
     in the branches. The paper is off-white (about 236,232,220), soft and matte, with crinkles and folds in the bake, and
     must read at 40 studs. Ribbon width is about 0.45 stud, thickness 0.06 or more, and both sides are real geometry.
   - `Halloween_TPBush.fbx`: a round leafy bush, about 6 x 5 x 6, in deep green turning autumn at the tips, draped with
     TP streamers and one roll at the base.
3. **SpookyBushes** (`Halloween\SpookyBushes\`)
   - `Halloween_Bush_Thorn.fbx`: a dark bramble or thorn bush, about 6 x 5.5 x 6, with twisted thorny stems, dark
     purple-green leaves and a few black berries. One cobweb sheet is draped over the top (strands plus silk RGBA part),
     with 1 spider point.
   - `Halloween_Bush_Autumn.fbx`: a dense leafy bush, about 6 x 5 x 6, in orange / red / yellow autumn colours. Two
     small warty gourds or mini pumpkins sit at its base.
   - `Halloween_Bramble.fbx`: a small dead shrub, about 4 x 3 x 4: dry tangled twigs with a few hanging dead leaves.
4. **Graveyard** (`Halloween\Graveyard\`)
   - `Halloween_Grave_A.fbx`: a rounded-top headstone with a carved "RIP" and a simple carved border, about 3 x 4 x 1.
   - `Halloween_Grave_B.fbx`: a stone cross, about 2.6 x 4.2 x 0.9.
   - `Halloween_Grave_C.fbx`: an old cracked slab that leans and has a chipped corner, about 3.2 x 3.6 x 0.9.
   - All three are weathered grey stone with moss in the cracks and a small mound of soil and dead grass at the base, and
     are **cartoon-chunky but detailed**. The carving is real geometry or a strong bake. The front faces Blender -Y.
   - `Halloween_DeadGrass_A.fbx` (about 4 x 3 x 4) and `Halloween_DeadGrass_B.fbx` (about 2.5 x 2.5 x 2.5): dry
     straw / olive grass tufts, a few blades bent or broken. The blades are real geometry, so no alpha is needed.

## Budgets (triangles, textures)
- Trees: 30,000 or fewer total. Split them into named MeshParts (for example `Trunk`, `Canopy`, `TP`, `Web`,
  `WebSilk`), each with 20,000 or fewer. Textures 1024.
- Bushes: 10,000 or fewer each, Bramble 5,000 or fewer. Textures 1024 for the bushes, 512 for the Bramble.
- Graves: 4,000 or fewer each, textures 512. Dead grass: 2,500 or fewer each, texture 512 (or vertex colour).
- Silk parts use an RGBA albedo. In Studio they need `SurfaceAppearance.AlphaMode = Transparency`; note that in NOTES.

## Pivot / orientation (important for placing ~50 pieces)
- **The FBX origin = the ground contact point** (the centre of the trunk or base at soil level, Z = 0). Nothing
  sinks more than 0.3 stud below Z = 0. The lead uses "Set Pivot to Scene Origin", so the model pivot = this point.
- Front (faces, carvings) faces **Blender -Y**.
- Give in NOTES: the size (Roblox X x Y x Z), triangles per object, texture sizes, and attachment points in **Roblox
  axes relative to the FBX origin** (spider thread points, web anchor points).

## Review process (the owner asked for reviewers)
1. **Builder:** build, self-review (renders at 25 and 50 studs plus a close-up, on the `review_setup` sky background
   with a green ground plane and a sunny key light like the hub), and fix. Then write NOTES.md and report.
2. **Independent reviewer agent:** it imports your FBX in a fresh headless Blender, renders it the same way, and
   writes `REVIEW.md` in your folder: **PASS** or **FIX** with a numbered list. Its checks:
   - the Halloween read from 40 studs;
   - silhouette and detail (not low poly, no faceting on curves);
   - bake faults (dark rims, black patches, seams, stretched UVs);
   - colour (rich, not plastic, not muddy);
   - TP / web readability;
   - scale vs the footprint table;
   - pivot at the ground;
   - triangle and texture budgets;
   - FBX has embedded textures.
3. The builder fixes every FIX item, re-renders and re-exports. At most 2 rounds.
