# Halloween hub decoration - shared brief for every builder agent (2026-10-12)

## The project
SLINGSHOT ("Slingshot for Eggs") is a Roblox egg/pet simulator. The owner asked (their words): "re-make the hub to be
halloween decorate on the walls, maybe behind the walls there's a giant halloween head decoration watching the players
... Make the models in blender, if using any vfx, make them in blender, **do not create low quality things**. Make also
pumpkin eggs in the hub, spyder webs on the walls, you get the vision right?" Design note:
`C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\docs\specs\2026-10-12-halloween-hub-design.md` (read it).

**Quality bar:** the owner has rejected low-poly / flat / "cheap" models before ("low polygon ... looks like trash").
Creatures must look **cool / fierce / semi-realistic, never cute**. Style = stylized-realistic HQ PBR: rich saturated
colours, real forms, baked detail (normal + AO + colour + roughness), clean silhouettes that read from 20-150 studs.
Style reference: `Halloween\review_head_front.png` / `review_head_back.png` (the giant jack-o'-lantern, made with the
kit below).

## Hard rules
- **No Neon, no emissive** in meshes or maps (owner rule). Glows/flames are Roblox particles + PointLights that the
  lead (me) sets up in Studio. You may model a candle wick, a lantern cage etc.; leave the light itself to Studio.
- Do **NOT** open or edit Roblox Studio, and do **NOT** use the GUI Blender MCP. Work only with headless Blender:
  `"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python <your_script.py> -- <args>`
  (Blender 5.2.2). Run long jobs with a timeout; redirect output to a log in your folder.
- Do **NOT** edit `Halloween\hkit.py`, `Halloween\pumpkin.py` or another agent's files. Import them read-only
  (`sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween"); from hkit import *`). If you
  need a changed helper, copy it into your own script.
- Work in your own folder `Halloween\<YourTask>\` (scripts, .blend, maps, renders, NOTES.md). FBX output goes to
  `C:\cdimp\Halloween_<Name>.fbx` (one FBX per asset; the asset centred at the origin unless the notes say otherwise).
- No git commits. No downloads of third-party models or textures: everything is procedural in Blender.

## Units and axes
1 Blender metre = 1 Roblox stud. +Z is up. **Blender +Y = Roblox -Z.** `hkit.export_fbx(objs, path)` already uses the
right FBX settings (global_scale 0.01, axis_forward -Z, axis_up Y, embedded textures, path_mode COPY).

## The kit (`Halloween\hkit.py`)
`lin(srgb255)`, `smoothstep`, `fbm(p, octaves)`, `mix`, `fresh(samples)`, `link`, `only`, `apply_mods(ob)`,
`obj_from_bm(bm, name, smooth=True)`, `set_colors(me, attr, [(r,g,b)...])` (per-vertex FLOAT_COLOR),
`quad_bezier(a, c, b, n)`, materials `mat_vc(name, col="Col", rough="Rough")` (Principled from colour attributes),
`mat_noise(...)`, `mat_flat(...)`, game mesh helpers `decimate_copy(hi, name, target_faces)`, `split_faces`,
`smart_uv(ob)`, bakes `bake_set(lo, [hi...], size, prefix, cage, maxray, ao_strength, ao_dist, outdir)` ->
`imgs` (tangent normal, colour x AO, roughness; ray misses are masked and repaired) and `pbr_material(lo, name, imgs)`,
review `review_setup()` + `shoot(path, target, direction, dist, lens)`, export `export_fbx(objs, path)`.
`Halloween\pumpkin.py` (read-only) has `pumpkin_sculpt(name, P)`, `cutter(...)`, `carve(...)`, `grin(...)`,
`stem_sculpt(...)`, `inner_materials()` and `build_head()` as a worked example.

## Pipeline + lessons already learned
1. Dense procedural sculpt (bmesh, per-vertex colour "Col" + roughness "Rough", or procedural shader materials).
2. Game mesh = **its own coarse version of the same procedural shape** (same seed, no micro detail) when the shape has
   booleans/holes (decimating a boolean result moves the hole edges and the bake shows dark rims). For organic shapes
   without holes, `decimate_copy` is fine.
3. Booleans: Solidify with `use_even_offset = False` on noisy surfaces (even offset folds the inner shell and the
   EXACT boolean silently drops it). Cut walls flat-shaded + sharp edges between materials (smooth shading across a knife
   edge bakes a sawtooth band).
4. Bake with `bake_set` (Cycles CPU). Texture <= 1024 (Roblox SurfaceAppearance max). Small repeated props: 512.
5. **Roblox limits:** one MeshPart <= 20,000 triangles. Props that repeat many times in the hub should be far lighter
   (eggs ~6-9k, small props 1-4k). Split a big asset into several named objects if needed (each becomes a MeshPart).
6. Thin things (strands, ropes): make them thick enough to read at 30-60 studs (>= 0.08-0.12 stud).
7. Review honestly before you report: render from the in-game distance (20-60 studs for hub props) AND a close-up, on
   the sky-blue background (`review_setup`) - look for dark rims, faceting, stretched UVs, flat/plastic colour, cute
   proportions. Fix and re-render until it would pass a senior game-art lead. Put the renders in your folder.

## Deliverables (report these back when done)
- FBX file(s) in `C:\cdimp\` and the build script(s) + .blend in your folder.
- `NOTES.md` in your folder: per object name, size in studs, triangle count, texture size, orientation (what faces
  +Y), pivot, and **attachment points** in object space (e.g. candle wick tips, the inside-light point of a pumpkin,
  a spider's thread point), plus any Roblox setup the lead must do (colours/materials of untextured parts, transparency,
  which part moves).
- 2-4 review render PNGs.
- A short final message: what you made, file paths, triangle counts, attachment points, known limitations.
