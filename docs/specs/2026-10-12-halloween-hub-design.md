# Halloween hub decoration - design (2026-10-12)

Owner's request: "re-make the hub to be halloween decorate on the walls, maybe behind the walls there's a giant
halloween head decoration watching the players ... Make the models in blender, if using any vfx, make them in blender,
do not create low quality things. Make also pumpkin eggs in the hub, spyder webs on the walls."

Owner's answers (2026-10-12, before going to sleep):
- Pumpkin eggs = **decoration only** (no gameplay).
- Giant head = **jack-o'-lantern**; its eyes follow the players.
- Glow + VFX = **effects made in Blender + real lights, still no Neon** (overrides "VFX only from VFX Studio" for this job).
- **No sky / lighting change** now: a Halloween atmosphere may become an event later.

## Rules kept
- Nothing under `Map.Hub` / runway is removed or moved. Everything new lives in **`Workspace.HalloweenDecor`** (one
  folder: delete it, or move it to ServerStorage, after Halloween).
- HQ assets: dense procedural sculpt -> game mesh (<= 20k tris per MeshPart) -> baked colour (x AO) / normal / roughness
  -> FBX with embedded textures -> Studio 3D importer (creator ZAB Studio) -> SurfaceAppearance, RenderFidelity Precise
  on the big ones. Same pipeline as the HQ meteors (`Weather/Meteor/HQ/build_hq.py`).
- No Neon, no emissive. "Glow" = unlit particles (LightEmission 1, LightInfluence 0) using Blender-rendered textures,
  plus PointLights.
- Decorations don't block paths: webs, garlands, spiders, head and vines have no collision; pumpkin eggs collide
  (hull) and stand only at edges (garden rims, wall feet, beside stalls), never on a path.

## Pieces (Blender: `Halloween/`)
1. **Giant jack-o'-lantern** behind the back wall (centre x 0, ~110 studs wide), its grin just above the wall line,
   so from spawn it peeks over the wall. A carved shell (angry slanted eyes, triangle nose, jagged grin with teeth),
   hollow inside, a twisted stem. Split into Front / Back / Inner MeshParts for texture detail.
   - **Watching:** a dark slit pupil floats in each glowing eye socket. Client-side (`HalloweenClient`), every
     player sees it watch THEM: the pupils snap to you fast, then the head turns after them slowly (yaw +-20 deg,
     pitch -12..+6). Every few seconds it glances at another player, then comes back.
   - **Fire inside:** big glow + rising fire-tongue + ember particles, and a flickering PointLight, seen through the
     carved holes.
   - **Vine fingers:** thick pumpkin vines with leaves and curly tendrils come from behind and grip the wall top on
     both sides of the head (static).
2. **Pumpkin eggs** (the game is about eggs): egg-shaped pumpkins, 3 carved faces + 1 uncarved, ~4-8 studs, each lit
   inside (candle flame + glow particles + small PointLight), in clusters with **candles** (wax, drips, flames).
3. **Spider webs:** corner webs (real strand geometry, sagging spiral, a few broken strands) in the upper corners of
   the back-wall bays and the wall corners.
4. **Spiders:** fierce black spiders with orange markings hanging on silk from the wall top, bobbing slowly.
5. **Garlands:** a twisted rope sagging between the back-wall pillars with cloth pennants (orange / black / purple,
   bat / pumpkin / skull symbols).
6. **VFX textures (rendered in Blender):** CandleFlame (8x8 loop), FireTongue (8x8 one-shot), Glow, Ember, Mist.

## Motion reference
animationreference.org `/tags/subtle`, "How To Train Your Dragon" (Hiccup reading by candlelight): the eyes move
first while the head holds; the head follows later and slower. The candle flame is a tall teardrop with a white-yellow
core, swaying gently and flickering only now and then. Used for the pupil/head timing (eyes ~0.15 s, head ~1.2 s
critically damped) and for the CandleFlame flipbook.
7. **Bat flock** (added during the build): 12 Blender-made bats (`Halloween/Bats`, clips fly + glide) circle the head
   client-side. Each flies its own loop, more than 66 studs from the head's centre. They flap when climbing, glide when
   diving and bank up to 25 degrees into turns.

## Garden (owner request, 2026-10-12, later the same day)
Owner: "There's Garden decor on the hub, let's change it to halloween stylized ones, do not make them low poly, make
them high quality. Trees with bushes maybe with spiders / webs on it or toilet paper ? Or different variations off it,
make different subagents to do that / reviewers".

**Replaced** in the 11 beds of `Map.Hub.Decor.Gardens`: Blossom and TreeRound trees, Bush and BushSmall, Rock, and the
grass tufts. The soil beds and the red toadstools stay. The originals move to a backup in ServerStorage (not deleted),
so they can go back after Halloween.

**New pieces** (`Halloween/GARDEN_BRIEF.md` has sizes and budgets):
- DeadTree (bare, gnarled, cobwebs + spiders) and HauntedTree (a face in the bark, dead leaves).
- TPTree (autumn canopy, toilet-paper-pranked) and TPBush.
- Bush_Thorn (bramble + cobweb), Bush_Autumn (with gourds) and Bramble (dead shrub).
- Grave_A / B / C (they replace the rocks) and DeadGrass_A / B.

**Process:** one Blender builder agent per family. Then an independent reviewer agent per family writes `REVIEW.md`
(PASS or a FIX list, at most 2 rounds) before the lead imports anything into Studio (`HalloweenDecor.Garden`).
