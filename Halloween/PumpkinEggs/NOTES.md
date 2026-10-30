# Pumpkin eggs + candles (Halloween hub decoration), 2026-10-12

Script: `eggs.py`. Run with `blender.exe -b --factory-startup --python eggs.py -- egg A | egg B | egg C | plain P1 | plain P2 | candles | review`. Add `fast` for a low-res test.
.blend files: `egg_A/B/C.blend`, `plain_P1/P2.blend`, `candles.blend`. The bake sources are kept in each file, hidden.
Maps: `maps\<Name>_albedo|normal|rough|ao.png`. Per-asset numbers: `<Name>.json`.
FBX: `C:\cdimp\Halloween_<Name>.fbx`. Each FBX holds ONE mesh object and embeds three textures: colour (AO already multiplied in), tangent normal, and roughness.

## Coordinates: all numbers are in BLENDER OBJECT SPACE
- 1 Blender unit = 1 stud. +Z is up.
- Every mesh is centred on its bounding box, so the object origin is the bbox centre (the MeshPart pivot).
- **Bottom offset** = the bbox centre to the ground, along Blender Z. Each model touches the ground exactly at the bottom of its bbox.
- Carved faces look along **Blender +Y**. The lead noted that the Studio importer turns models 180 deg (Blender +Y comes out as Roblox +Z, Blender +X as Roblox -X). Convert these numbers on your side.

| Object | Size x / y / z (studs) | Tris | Texture | Bottom offset (z) |
|---|---|---|---|---|
| PumpkinEgg_A | 5.110 / 5.041 / 6.920 | 7,212 | 1024 | -3.460 |
| PumpkinEgg_B | 5.305 / 5.280 / 7.299 | 7,840 | 1024 | -3.649 |
| PumpkinEgg_C | 5.447 / 5.366 / 6.684 | 7,166 | 1024 | -3.342 |
| PumpkinEgg_Plain1 | 2.967 / 3.103 / 3.951 | 4,200 | 512 | -1.976 |
| PumpkinEgg_Plain2 | 2.764 / 2.837 / 3.616 | 3,804 | 512 | -1.808 |
| Candles | 3.559 / 3.154 / 2.396 | 2,376 | 512 | -1.198 |

Heights include the stem.

## Carved eggs (A, B, C)
These are hollow, egg-shaped jack-o'-lanterns: narrow top, weight-flattened bottom, 8 ribs on A and C and 9 on B. Each has a gnarly stem and one curled vine tendril. Every egg is ONE mesh: outer skin, flat knife-cut walls (pale flesh with a thin rind line along the outer edge), scraped inner wall, stem and tendril.
- **A**: slanted, scowling eyes; small triangle nose; grin with two long fangs and small teeth. Shell 0.28.
- **B**: narrow sinister slit eyes; dagger nose; zigzag lightning mouth. Shell 0.30.
- **C**: crazed eyes, one big lopsided staring eye with a hard brow cut and one small squint; crooked nose; wide grin of sharp shark teeth. Shell 0.27.
- Every face hole is cut all the way through. A build check confirms 4 holes in both the bake source and the game mesh.

Attachment points (Blender object space):

| Egg | Cavity centre | Cavity floor (inside, centre) | Suggested flame + PointLight |
|---|---|---|---|
| A | (-0.008, -0.019, -0.498) | (-0.008, -0.019, -3.288) | (-0.008, -0.019, -2.34) |
| B | (-0.034, -0.005, -0.541) | (-0.034, -0.005, -3.461) | (-0.034, -0.005, -2.51) |
| C | (0.008, -0.006, -0.451) | (0.008, -0.006, -3.175) | (0.008, -0.006, -2.23) |

Studio setup:
- **Put the light LOW, not at the cavity centre.** The suggested point is about 0.95 above the floor, like a candle standing inside. The knife walls are radial from the egg centre, so a light exactly at the centre grazes them and leaves them dark. A low light catches the upper walls of every hole, which is the classic lit-pumpkin look. The review renders use this placement (PointLight about 160 W in Blender terms, warm (1, 0.55, 0.2)).
- PointLight `Shadows = true` is recommended. With shadows off, the light passes through the shell and tints the whole outer skin orange instead of only shining out through the face.
- Glow and flame particles can sit at the cavity centre or just above the flame point. The cavity is about 4.5 wide and 5.6 tall inside.
- RenderFidelity Precise. Collision: hull (the brief says eggs collide).
- No neon and no emissive anywhere. The glow is entirely your lights and particles.

## Plain eggs
- **Plain1**: deep red-orange egg pumpkin, 10 ribs, dark green stem.
- **Plain2**: pale cream "ghost" pumpkin, 9 ribs, green-grey streaks down the grooves, pale stem.
- Both are uncarved, have no attachments, and collide with a hull.

## Candles
One mesh: 3 melted church candles on a wax puddle with wax tongues. Rims are uneven with overflow notches, drips run down from them ending in teardrop bulbs, and the pool sits in each crater. The wax is ivory/bone, with a slightly different tint per candle. Wicks are black and curled with an ash tip.

| Candle | Rim height | Radius | Wick tip (end of the curl) | Wick top (highest point) |
|---|---|---|---|---|
| 1 (short) | 1.2 | 0.47 | (-0.103, 0.743, 0.002) | (-0.119, 0.710, 0.016) |
| 2 (middle) | 1.8 | 0.53 | (0.400, -0.317, 0.528) | (0.435, -0.306, 0.542) |
| 3 (tall) | 2.4 | 0.58 | (-0.762, -0.342, 1.095) | (-0.726, -0.351, 1.109) |

- Flame centre: wick top + (0, 0, 0.12). The review renders use that point with a small warm PointLight (+0.18).
- On the tall candle the wick sits in a deep crater: its top is about 0.1 below the highest part of the rim. The flame rises above the rim and lights the inside wall of the crater.
- Collision: off, or a simple box (it is a small prop).

## Review renders (in this folder)
- `review_day_25studs.png`: all six assets in daylight from 25 studs.
- `review_night_lit.png`: the same view at night, lit from inside.
- `review_close_A_lit.png`: close-up of A lit from inside.
- `review_close_candles_lit.png`: close-up of the lit candles.

More views (back, 3/4, close-ups of B and C) are in `wip\`. The flames in the renders are review-only stand-ins and are not exported.

## Pipeline notes (also relevant to the giant head)
1. **The EXACT boolean does not interpolate point colour attributes onto the new cut vertices.** They come out as (0, 0, 0, 0). On the bake source this leaves a black, glossy band along every knife edge, and that band bakes into the dark serrated rims around the holes. `repair_attrs()` refills each of those vertices from its valid neighbours on the same surface; it fixed about 1,000-1,600 vertices per egg.
2. **`cutter_radial` can break on long concave outlines.** It scales the outline onto a curved surface, so the ear-clipped cap is non-planar. On B's zigzag mouth the cap triangles cut through the island's own walls, and the boolean wiped most of the shell. `cutter_planar()` keeps the same radial walls but builds each cap as the central projection of the outline onto a plane, so the caps are planar.
3. **Bakes run per surface group.** The groups are skin + stem + tendril, cut walls, and inner wall. Each low-poly part only matches rays against its own bake-source part. Before any pass, every low-poly bake copy is hidden from AO and shadow rays.
4. **UV packing uses `shape_method="CONVEX"`.** The concave packer had nested stem and wall islands inside the face holes of the front skin island. The skin and inner wall are ANGLE_BASED lunes cut along three rib grooves. The inner wall gets 0.55x texel density.

## Known limitations
- Under the blue review sky and the AgX view, Plain2 and the candle wax read cooler and whiter than their albedo. The baked colours are warm cream and ivory, and they read warmer under Roblox lighting and the candle flames.
- Egg C has a natural cluster of small dark rot spots near the top-right shoulder (blemish noise). The stem and tendril are coarse on the game mesh (10- and 5-sided) and carry their detail in the maps. The candle lip is a 28-gon.
