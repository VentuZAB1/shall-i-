# Reviewer: verify the Thorn spider thread point from NOTES (Roblox (1.525, 3.740, 2.641) = Blender (1.525, -2.641, 3.74)).
import bpy
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=r"C:\cdimp\Halloween_Bush_Thorn.fbx")
for o in bpy.context.scene.objects:
    o.scale = (1, 1, 1)
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
sc = bpy.context.scene
import os
rx, ry, rz = [float(v) for v in os.environ.get("SPIDER_ROBLOX", "1.525,3.74,2.641").split(",")]
pt = Vector((rx, -rz, ry))  # Roblox (X, Y, Z) -> Blender (X, -Z, Y)
# nearest surface to the point
best = None
for o in sc.objects:
    if o.type != "MESH":
        continue
    ok, loc, n, i = o.closest_point_on_mesh(o.matrix_world.inverted() @ pt)
    if ok:
        d = (o.matrix_world @ loc - pt).length
        if best is None or d < best[0]:
            best = (d, o.name)
print("NEAREST_SURFACE", best)
hit, loc, n, i, ob, m = sc.ray_cast(dg, pt - Vector((0, 0, 0.02)), Vector((0, 0, -1)))
print("DROP_HIT", hit, tuple(round(x, 3) for x in loc) if hit else None, ob.name if hit else None)
hit, loc, n, i, ob, m = sc.ray_cast(dg, pt + Vector((0, 0, 0.5)), Vector((0, 0, -1)))
print("FROM_ABOVE_HIT", hit, tuple(round(x, 3) for x in loc) if hit else None, ob.name if hit else None)
