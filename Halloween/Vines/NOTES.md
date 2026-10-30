# VineGrip: giant pumpkin-vine "fingers" gripping the back wall (Halloween hub, 2026-10-12)

Thick pumpkin vines come from behind the back wall (from the giant jack-o'-lantern), arch over the wall top with
raised knotted **knuckles**, and claw down the inner face like fingers: pressed at the top, the middle joint standing
off the face, the claw tip digging back in. Each tip ends in a **tight tendril coil** (A, B, D: conical spirals;
C: a corkscrew). A crown of 9 autumn pumpkin leaves (green, then yellowing, then brown and dry, with brown dry edges)
rises behind and between the knuckles, and two leaves hang over the edge. 7 loose curly tendrils: one is a spring
hanging beside finger B, one wraps vine C, two have a twist-reversal (perversion).

## Files
- Build script: `Halloween\Vines\vines.py` (headless; imports `hkit` read-only)
  `blender.exe -b --factory-startup --python vines.py -- build bake render export mirror pair points`
- Blend: `Halloween\Vines\vines.blend` (game meshes + hidden hi sculpts `VineGrip_Vines_hi` 369k tris,
  `VineGrip_Leaves_hi` 223k tris)
- Maps (1024, already embedded in the FBX): `Halloween\Vines\maps\VineGrip_{Vines,Leaves}_{albedo,normal,rough}.png`
  (albedo already includes AO; the `_ao.png` files are reference only)
- **FBX:** `C:\cdimp\Halloween_VineGrip.fbx` (VineGrip_Vines + VineGrip_Leaves)
- **Mirror FBX:** `C:\cdimp\Halloween_VineGripMirror.fbx` (VineGripM_Vines + VineGripM_Leaves) - see "Mirroring"
- Review renders: `review_hub.png` (hub side, 42 studs, looking up), `review_close.png`, `review_34.png`,
  `review_hub_backlit.png` (sun from behind the wall), `review_pair_culled.png` (both sides, backface culling on)

## Frame (Blender, studs) - both objects have their origin at (0, 0, 0)
- Origin = a point on the wall's **top inner edge**, at the middle of the grip. The edge runs along X.
- Wall body = y in [-6, 0], z in [-25, 0] (top surface z = 0, hub floor z = -25).
- Players are on **+Y** (Blender +Y = Roblox **-Z**). The vines come from -Y (behind the wall, toward the head).
- Roblox conversion: Blender (x, y, z) -> Roblox (x, z, -y).

## Objects
| Object | Tris | Maps | Size Blender X x Y x Z | Size Roblox X x Y x Z | BBox centre, Roblox offset from the edge point |
|---|---|---|---|---|---|
| `VineGrip_Vines` (vines + petioles + tendrils) | 16,746 | 1024 colour / normal / roughness | 28.5 x 18.7 x 16.8 | 28.5 x 16.8 x 18.7 | (-0.12, -3.20, +6.53) |
| `VineGrip_Leaves` (9 leaves, real top + underside) | 10,290 | 1024 colour / normal / roughness | 35.2 x 12.0 x 13.3 | 35.2 x 13.3 x 12.0 | (-0.50, +1.06, +3.23) |

Extents (Blender): Vines x -14.4..14.1, y -15.9..2.8, z -11.6..5.2; Leaves x -18.1..17.1, y -9.2..2.8, z -5.6..7.7.
The four fingers span x = -12.6..12.7 on the inner face (about 25 studs); leaves and tendrils reach further.
On the inner face the finger centrelines sit at y = +0.4..+1.7 and, with their coils, reach down to
z = -5.8 (D), -7.1 (C), -7.3 (A), -8.3 (B).
The vines rest on the wall: they sink ~0.14 into the top surface / inner face (solid contact, no floating gap),
so the wall must be exactly where the frame says.

**Placement:** with the model turned so its Roblox -Z faces the hub, put each MeshPart at
`EdgePoint + offset` from the table (the importer keeps the two parts aligned with each other, so placing one
places both). Hidden parts: the vines start behind the wall at y = -14..-15.9, z = -10..-11.6. If the head's front
is at -16 or closer they may enter the head, which is fine (it reads as the vines coming out of it).

## Mirroring
Roblox cannot mirror a MeshPart (no negative Size), and a 180 deg turn would put the vines on the players' side.
`Halloween_VineGripMirror.fbx` is a true X-mirror (geometry mirrored + faces re-wound, same UVs). It uses **the same
textures**: reuse the original SurfaceAppearance texture IDs on `VineGripM_*` instead of uploading the duplicates
(mirrored UV winding flips the tangent handedness, so the normal map stays correct; checked in
`review_pair_culled.png`). Mirror bbox centres: Vines (+0.12, -3.20, +6.53), Leaves (+0.50, +1.06, +3.23).

## Attachment points (object space, Blender -> Roblox offset from the edge point)
Useful for spider threads, drips or dew particles. Mirror copy: negate X.
| Vine | knuckle top (0.3 above the vine) | finger joint (centreline) | claw tip (centreline) | coil end |
|---|---|---|---|---|
| A (x<0, outer) | (-9.28, -1.50, 4.01) -> R(-9.28, 4.01, 1.50) | (-10.81, 1.39, -2.54) -> R(-10.81, -2.54, -1.39) | (-12.30, 0.45, -5.60) -> R(-12.30, -5.60, -0.45) | (-12.19, 1.46, -6.15) |
| B (longest) | (-3.80, -1.44, 4.33) -> R(-3.80, 4.33, 1.44) | (-3.62, 1.68, -2.88) -> R(-3.62, -2.88, -1.68) | (-3.10, 0.50, -6.90) -> R(-3.10, -6.90, -0.50) | (-3.29, 1.50, -7.37) |
| C (corkscrew) | (3.71, -1.33, 3.75) -> R(3.71, 3.75, 1.33) | (4.58, 1.47, -2.61) -> R(4.58, -2.61, -1.47) | (5.50, 0.45, -5.80) -> R(5.50, -5.80, -0.45) | (6.39, 2.05, -7.08) |
| D (x>0, short) | (10.08, -1.40, 3.26) -> R(10.08, 3.26, 1.40) | (11.34, 1.17, -2.13) -> R(11.34, -2.13, -1.17) | (12.40, 0.40, -4.60) -> R(12.40, -4.60, -0.40) | (12.33, 1.16, -4.99) |

## Roblox setup (lead)
- Import with the 3D importer (creator ZAB Studio); the importer builds the SurfaceAppearance (colour, normal,
  roughness; no metalness). No Neon, no emissive, nothing glows.
- Both parts: Anchored, **CanCollide / CanTouch / CanQuery = false** (decoration, no blocking), CastShadow = true
  (the fingers throw nice shadows on the wall), **RenderFidelity = Precise** (keeps the coils, serrations and leaf
  shapes at distance).
- **DoubleSided is not needed**: every leaf has a real underside 0.04 under the top (sharing the top's texture).
- Static: nothing moves.

## Build notes / known limitations
- Vines, petioles and tendrils are swept tubes: parallel-transport frames, 5 twisting ridges, knots (nodes, a big
  knuckle at the hump, a finger joint), lumps; hi = 96-sided rings every 0.05 stud with per-vertex colour (deep green,
  near-black grooves, yellow-brown dry streaks, woody base, darker knots) and a procedural prickle-hair bump; game
  mesh = 15/10/6-sided ridge-aligned rings (zippered where the count changes), tube-strip UVs in studs; the hidden
  behind-the-wall stretches get 0.4x texel density. Paths are pushed out of the wall slab and free bends are
  limited to 1.45x the tube radius (no pinching).
- Leaves are constrained-Delaunay sheets of a 5-lobed serrated outline (the game mesh puts its edge vertices exactly
  on the tooth tips and notches), shaped by cup / midrib fold / pleats / ruffled margin / droop / dry curl, moved off
  the vines only along their own normal (cannot flip triangles); the hi adds sunken main and secondary veins,
  per-vertex autumn colour and a tertiary vein-net bump.
- UV use: vines 71 %, leaves 57 % of the 1024 square. ~10 studs from the camera the leaf maps are a little soft.
- 8 game-mesh faces of the vines are pinched inside out where a vine wraps the wall's corner edges; they are inside
  the wall (invisible). Tiny normal-map marks where tendrils / petioles enter a vine (covered by them).
- The leaf underside shows the same colour as the top (the real underside would be paler), which is fine at hub
  distance.
