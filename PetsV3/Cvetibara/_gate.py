# builder E gate helper (background Blender):
#   blender -b --factory-startup --python Cvetibara/_gate.py -- <Name> [head_bone_center x,y,z] [dist]
# Builds the model with run3, prints plates per big block face, renders a 512 px face crop, a top view and a 64 px
# silhouette (black on white) into <Name>/renders/gate_*.png.
import sys, runpy, json, math, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
from mathutils import Vector
bk = R3["blockkit"]
pk = R3["pk"]
counts = {}
cur = {"blk": None}
orig_studs = bk.Blocks._studs_for
orig_plate = bk._plate


def studs_for(self, blk, bm, L):
    cur["blk"] = blk
    return orig_studs(self, blk, bm, L)


def plate(bm, L, ctr, u, v, n, a, b, hgt, color, jit=1.0, flush=False):
    blk = cur["blk"]
    if blk is not None and blk.h.x * blk.h.y * blk.h.z > 0.004:
        key = "%s(%.2f,%.2f,%.2f) n=(%.0f,%.0f,%.0f)" % (blk.bone, blk.c.x, blk.c.y, blk.c.z, n.x, n.y, n.z)
        counts[key] = counts.get(key, 0) + 1
    return orig_plate(bm, L, ctr, u, v, n, a, b, hgt, color, jit, flush)


bk.Blocks._studs_for = studs_for
bk._plate = plate
m = R3["spec"](name)
k = R3["new_pet"](m, name)
info = m.model(k) or {}
# big blocks without any plate on a visible face
big = []
for blk in k.blocks.items:
    if isinstance(blk, bk.Poly) or blk.studs == []:
        continue
    if blk.h.x * blk.h.y * blk.h.z > 0.004:
        big.append("%s(%.2f,%.2f,%.2f) half(%.2f,%.2f,%.2f) role=%s" % (blk.bone, blk.c.x, blk.c.y, blk.c.z, blk.h.x, blk.h.y,
                                                                      blk.h.z, blk._role))
pk.stage(k)
sc = bpy.context.scene
cam = sc.camera
d = os.path.join(k.dir, "renders")
fc = Vector(tuple(float(v) for v in argv[1].split(","))) if len(argv) > 1 else None
dist = float(argv[2]) if len(argv) > 2 else 2.2
files = []
if fc is not None:
    sc.render.resolution_x = sc.render.resolution_y = 512
    cam.data.lens = 70
    pk.aim(cam, fc + Vector((0.0, -dist, 0.08)), fc)
    sc.render.filepath = os.path.join(d, "gate_face.png")
    bpy.ops.render.render(write_still=True)
    files.append(sc.render.filepath)
mn, mx = k.bounds()
c = (mn + mx) / 2
size = max((mx - mn).length, 2.0)
sc.render.resolution_x = sc.render.resolution_y = 420
pk.aim(cam, c + Vector((0.001, 0.3, 1.0)).normalized() * size * 1.75, c)
sc.render.filepath = os.path.join(d, "gate_top.png")
bpy.ops.render.render(write_still=True)
files.append(sc.render.filepath)
# 64 px silhouette from the tq view
for o in bpy.data.collections["Stage"].objects:
    if o.type == "MESH":
        o.hide_render = True
w = sc.world
w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
blk_mat = bpy.data.materials.new("Sil")
blk_mat.use_nodes = True
blk_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0, 0, 0, 1)
blk_mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
for o in k.coll.objects:
    if o.type == "MESH":
        o.data.materials.clear()
        o.data.materials.append(blk_mat)
for o in bpy.data.collections["Stage"].objects:
    if o.type == "LIGHT":
        o.hide_render = True
sc.render.resolution_x = sc.render.resolution_y = 64
loc, tgt = pk.camera_for(k, "tq")
pk.aim(cam, loc, tgt)
sc.render.filepath = os.path.join(d, "gate_sil64.png")
bpy.ops.render.render(write_still=True)
files.append(sc.render.filepath)
print("GATE_RESULT " + json.dumps({"info": info, "plates_per_face": counts, "files": files}, default=str))
