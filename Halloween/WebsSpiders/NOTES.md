# Halloween hub: spider webs + spider (WebsSpiders), 2026-10-12

Build script: `webs_spiders.py` (headless, everything procedural):
`blender.exe -b --factory-startup --python webs_spiders.py -- webs render_webs export_webs spider render_spider export_spider`
Blends: `webs.blend`, `spider.blend`. Maps: `maps\`. Reports: `webs_report.json`, `spider_report.json`.

Axes: 1 Blender m = 1 stud. Blender +X = Roblox +X, Blender +Z = Roblox +Y, **Blender +Y = Roblox -Z**.
All "local" offsets below are in **Roblox axes, measured from the MeshPart's own centre** (Roblox centres every
MeshPart on its bounding box).

## FBX files (C:\cdimp)
| File | Objects (MeshParts) | Triangles |
|---|---|---|
| `Halloween_SpiderWeb_Corner.fbx` | SpiderWeb_Corner | 6,472 |
| `Halloween_SpiderWeb_Corner_Mirror.fbx` | SpiderWeb_Corner_Mirror | 6,472 |
| `Halloween_SpiderWeb_Torn.fbx` | SpiderWeb_Torn + SpiderWeb_Torn_Silk | 8,112 + 1,168 = 9,280 |
| `Halloween_SpiderWeb_Torn_Mirror.fbx` | SpiderWeb_Torn_Mirror + SpiderWeb_Torn_Mirror_Silk | 9,280 |
| `Halloween_Spider.fbx` | Spider + SpiderThread (optional helper) | 7,122 + 24 |

**Why the _Mirror files:** Roblox can't mirror a MeshPart (no negative size). Rotating a web 90 degrees would make its sag, its hanging
loose strands and the silk sheets fall sideways. Use the original or the `_Mirror` file, then only yaw it (rotate around Y).

---------------------------------------------------------------------------------------------------------------------
## SpiderWeb_Corner (fresh orb web for the upper corners of the back-wall bays)
- **Size (Roblox X x Y x Z):** 13.16 x 12.91 x 0.86 studs. R = 13. It fills the quadrant beside and below the corner.
- **Build:** real tube strands. 15 radials, 4-sided, 0.10 thick. Frame and anchor threads, 4-sided, 0.12 thick. A 16-ring catch
  spiral, 3-sided, 0.075 thick, sagging between radials as a catenary (toward the hub plus a little gravity). Hub spiral and silk
  mat near the corner, anchor threads to the corner, the pillar and the trim, and guy lines back to the wall. 6 snapped spans
  with hanging loose ends, 3 long old threads hanging down, and one silk-wrapped prey bundle. Smooth noise irregularity.
- **Facing:** the front faces Roblox **-Z**. The web bows up to 0.55 toward the viewer. The wall is assumed **0.3 studs behind**
  the corner point (guy lines touch it).
- **Corner point (local):** `(-6.530, +6.404, +0.124)`. It is the web's upper-RIGHT point as seen from the hub, so the pillar is on
  the viewer's right. The web body extends to the viewer's left (+X) and down.
- **_Mirror:** pillar on the viewer's LEFT. Corner point `(+6.530, +6.404, +0.124)`.
- **Texture:** `WebCorner_albedo.png` 256 (embedded; planar silver-white silk, dust toward the walls).
  Optional roughness map: `maps\WebCorner_rough.png` 256 (0.38 to 0.72).

## SpiderWeb_Torn (old ragged web for the outer wall corners)
- **Size:** strands 18.02 x 17.97 x 1.11. Same frame as the corner web, R = 18.
- **Build:** 12 radials and a 14-ring spiral with 4 torn holes, random breaks and cut radials hanging loose. Droopy frame. 5
  sagging clumps of 2-3 twisted strands. 12 slack tangle threads along the pillar and the trim. Long strands and a snapped bundle
  hanging down. 2 silk-wrapped prey bundles.
- **SpiderWeb_Torn_Silk** (separate part, 1,168 tris, 16.67 x 10.12 x 1.19): 3 hanging dusty silk sheets plus a dense silk mat in
  the very corner. Each sheet has real front and back faces, so DoubleSided is not needed.
  Texture: `WebSilk_albedo.png` **512 RGBA**: a fibre tangle, a gauze film with torn organic holes, dust, frayed edges.
- **Corner point (local, SpiderWeb_Torn):** `(-8.957, +8.931, +0.247)`. Same handedness as the corner web: pillar on the
  viewer's right. **_Mirror:** `(+8.957, +8.931, +0.247)`.
- **Silk part centre, relative to the strands part centre:** `(-0.621, +3.870, -0.238)`. **_Mirror:** `(+0.621, +3.870, -0.238)`.
  The importer keeps them in place inside one Model; move them together (PrimaryPart = the strands part).
- **Textures:** strands `WebTorn_albedo.png` 256 (dusty grey-beige). Optional `maps\WebTorn_rough.png` (0.55 to 0.85).

### Roblox setup for the webs
- Anchored, CanCollide / CanTouch / CanQuery **false**, CollisionFidelity Box.
- **RenderFidelity = Precise.** Automatic LOD mangles 0.08-stud strands at distance.
- CastShadow **false** recommended (0.1-stud strands give noisy shadow-map speckle). Transparency 0. No Neon.
- **Silk parts: `SurfaceAppearance.AlphaMode = Transparency` is REQUIRED.** With the default Overlay, the see-through parts show
  the part Color as an opaque sheet. Fallback if alpha can't be used: Transparency 0.45, Color (226,222,214).
- If the importer drops the colour map, use: corner web Color (228,230,236) SmoothPlastic; torn web Color (206,202,194).

### Placement (Luau), works for all four web variants
```lua
-- innerCorner = the point where the pillar side, the trim underside and the wall face meet
-- n = wall normal (unit, into the hub); a = unit vector along the wall from the pillar INTO the bay
-- k = corner offset from the table above (e.g. Vector3.new(-6.530, 6.404, 0.124) for SpiderWeb_Corner)
local function webCFrame(innerCorner, n, a, isMirror, k)
	local xAxis = isMirror and -a or a
	local cf = CFrame.fromMatrix(innerCorner + n * 0.3, xAxis, Vector3.yAxis) -- local -Z (the front) = n
	return cf * CFrame.new(-k)                                                -- corner point -> part centre
end
-- Torn web: strands.CFrame = webCFrame(...); silk.CFrame = strands.CFrame * CFrame.new(silkOffset)
```
Use the original where the pillar is on the RIGHT as seen from the hub. Use `_Mirror` where it's on the LEFT.

---------------------------------------------------------------------------------------------------------------------
## Spider (fierce orb-weaver, hanging on its thread)
- **Size (Roblox X x Y x Z):** 5.85 x 6.75 x 2.27 studs (leg span about 6.8 tall x 5.9 wide). Body (cephalothorax + abdomen
  + jaws) is about 3.1 long.
- **Triangles:** 7,122 (budget 9,000). Sculpt is about 263k tris with real hair strands, spines, 8 eyes, fangs and leg ridges,
  baked to a **1024** set: `Spider_albedo.png` (colour x AO), `Spider_normal.png` (tangent, OpenGL Y+, hair streaks softened),
  `Spider_rough.png`. UVs are explicit islands packed by texel priority: about 166 px/stud on average, more on the abdomen,
  head and jaws. 6% of the map is unused.
- **Look:** black-purple body. Bold nested orange chevrons, orange shoulder spots and a rust folium outline on the abdomen. Red
  hourglass on the belly. 8 glossy red-black eyes. Big glossy dark-red chelicerae with curved fangs that have orange-red tips.
  8 jointed hairy legs with rust bands and black spines. Short palps.
- **Pose / facing:** head DOWN, abdomen and spinnerets UP. The **back (chevrons) faces Roblox -Z**, tilted 15 degrees toward the
  floor so viewers below see the markings and the face. Front legs reach down and forward, legs III bunched, legs IV reach up
  beside the thread. Static mesh, no rig.
- **Pivot:** bounding-box centre = origin.
- **THREAD ATTACH POINT (spinneret tip), local:** **`(-0.055, +2.921, -0.562)`** (Blender `(-0.055, 0.562, 2.921)`).
  The thread goes straight up (+Y) from there. Legs IV reach about 0.45 studs above it, on both sides of the thread.
- Eyes centre (local): `(-0.056, +0.075, +0.050)`.
- **SpiderThread** (optional helper): a 0.07-thick silk tube, 10.06 studs long, from 0.06 below the attach point straight up.
  Its centre is local `(-0.055, +7.891, -0.562)` from the Spider centre. Untextured: Color (226,226,230), SmoothPlastic,
  CastShadow false. It stretches cleanly with Size.Y, or replace it with a Beam / RopeConstraint.

### Roblox setup for the spider
- SurfaceAppearance: ColorMap and NormalMap come from the FBX. **Set `RoughnessMap = Spider_rough.png`** by hand. hkit's FBX
  export only carries colour + normal; without it the glossy eyes, fangs and carapace go flat.
- Anchored, CanCollide / CanTouch / CanQuery false, **RenderFidelity Precise** (thin legs), CastShadow true (its shadow on the
  wall reads very well). No Neon / emissive anywhere.
- Bobbing: move Spider and SpiderThread together. Or keep the thread top fixed and change its Size.Y with the bob.
```lua
-- hangPoint = where the thread is tied (wall top); n = wall normal into the hub; L = thread length
local ATTACH = Vector3.new(-0.055, 2.921, -0.562)
local rot = CFrame.lookAt(Vector3.zero, n)                    -- local -Z (the spider's back) faces the hub
spider.CFrame = rot + (hangPoint - Vector3.yAxis * L - rot:VectorToWorldSpace(ATTACH))
thread.Size = Vector3.new(thread.Size.X, L + 0.06, thread.Size.Z)
thread.CFrame = CFrame.new(hangPoint - Vector3.yAxis * (L + 0.06) / 2)
```

---------------------------------------------------------------------------------------------------------------------
## Review renders (this folder)
- In-game distance (70 degree vertical FOV, 30 studs, from the hub floor, wall stand-in):
  `review_corner_wall_30.png`, `review_torn_wall_30.png`, `review_spider_wall_30.png`, `review_spider_30.png`.
  Also `review_webs_60.png` (60 studs) and `review_webs_sky_30.png`.
- Close-ups: `review_corner_close.png`, `review_torn_close.png`, `review_spider_close.png`, `review_spider_face.png`,
  `review_spider_34.png`.

## Known limitations
- Roughness maps are not in the FBX files (same as the head pipeline). Assign them by hand if wanted. For the spider it matters.
- Web strands are 0.075-0.12 thick: crisp at 15-40 studs, about 1 px at 60+ studs. That is expected for webs.
- Silk sheets depend on AlphaMode = Transparency (see above).
- The spider is a single static pose (no rig). Its fine hair, spine and fang detail only shows within about 15 studs. At 30+
  studs it reads as a fierce dark spider with orange chevrons.
- The web stand-in walls in the renders are guesses (grey stone), not the real hub materials.
