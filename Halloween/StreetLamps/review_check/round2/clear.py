# Reviewer clearance check on the fresh FBX import: min distance + overlap between parts (studs).
import bpy, sys, os, json, math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import bmesh

FBX = r"C:\cdimp\Halloween_StreetLamp.fbx"
OUT = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=FBX)
objs = {o.name: o for o in bpy.context.scene.objects if o.type == "MESH"}
for o in objs.values():
    o.scale = (1, 1, 1)
bpy.context.view_layer.update()


def bvh(o):
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bm.transform(o.matrix_world)
    t = BVHTree.FromBMesh(bm)
    verts = [v.co.copy() for v in bm.verts]
    bm.free()
    return t, verts


T = {n: bvh(o) for n, o in objs.items()}
rep = {}
pairs = [("Web", "Cage"), ("Web", "Pumpkin"), ("WebSilk", "Cage"), ("Cage", "Post"), ("Pumpkin", "Post"),
         ("Pumpkin", "Cage"), ("Web", "Post"), ("WebSilk", "Post")]
for a, b in pairs:
    ta, va = T[a]
    tb, vb = T[b]
    over = len(ta.overlap(tb))
    best = (1e9, None)
    for v in va:
        hit = tb.find_nearest(v)
        if hit[0] is not None and hit[3] < best[0]:
            best = (hit[3], tuple(round(c, 3) for c in v))
    rep[a + "-" + b] = dict(overlap_tri_pairs=over, min_dist=round(best[0], 4), at=best[1])
# lowest points and head geometry
for n in ("Cage", "Pumpkin", "Web", "WebSilk"):
    vs = T[n][1]
    rep[n + "_minz"] = round(min(v.z for v in vs), 3)
    rep[n + "_maxz"] = round(max(v.z for v in vs), 3)
# cap height: Cage verts above the top ring near the axis
cage = T["Cage"][1]
rep["cage_points_above_14_7_near_axis_maxz"] = round(max(v.z for v in cage if math.hypot(v.x, v.y + 3.55) < 0.9 and v.z < 15.6), 3)
with open(os.path.join(OUT, "clearance.json"), "w") as fh:
    json.dump(rep, fh, indent=1)
print(json.dumps(rep, indent=1))
