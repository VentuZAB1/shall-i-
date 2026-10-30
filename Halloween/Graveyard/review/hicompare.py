# Reviewer (read-only on the builder's .blend: never saved): compare the hi-poly fracture corner of Grave_C with the game mesh.
import bpy, os, math, sys
from mathutils import Vector
D = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\Graveyard\Grave_C.blend")
for o in bpy.data.objects:
    print("OBJ", o.name, o.type, o.hide_render, len(o.data.polygons) if o.type == "MESH" else "")
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"; sc.render.resolution_x, sc.render.resolution_y = 900, 900
sc.render.filepath = ""
hi = [o for o in bpy.data.objects if o.type == "MESH" and o.name.endswith("_hi") and "mound" not in o.name]
lo = [o for o in bpy.data.objects if o.type == "MESH" and not o.name.endswith("_hi")]
w = sc.world or bpy.data.worlds.new("W"); sc.world = w
ld = bpy.data.lights.new("RSun", "SUN"); ld.energy = 4; l = bpy.data.objects.new("RSun", ld); sc.collection.objects.link(l)
l.rotation_euler = (math.radians(50), 0, math.radians(30))
cd = bpy.data.cameras.new("RC"); cam = bpy.data.objects.new("RC", cd); sc.collection.objects.link(cam); cd.lens = 50
cam.location = (5.0, -4.6, 4.2); cam.rotation_euler = (Vector((0.9, 0, 3.0)) - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.camera = cam
for grp, tag in ((hi, "hi"), (lo, "lo")):
    for o in bpy.data.objects:
        if o.type == "MESH":
            o.hide_render = o not in grp
    sc.render.filepath = os.path.join(D, f"compare_GraveC_corner_{tag}.png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath)
