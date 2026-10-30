# blender -b --factory-startup --python EclipseSeraph/_scratch/clearance.py -- <Name> <bone> [action frame]
# (builder D scratch) min distance from the verts of one bone's vertex group to every OTHER part of the mesh (bind
# pose, or an action frame), plus the 5 nearest other groups - for floating hero pieces (halo clearance)
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name, bone = argv[0], argv[1]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy, bmesh
from mathutils.bvhtree import BVHTree
if len(argv) > 2:
    R3["full"](name, save=False)
    k = R3["STATE"]["k"]
    k.set_action(argv[2])
    bpy.context.scene.frame_set(int(argv[3]) if len(argv) > 3 else 0)
else:
    m = R3["spec"](name)
    k = R3["new_pet"](m, name)
    m.model(k)
ob = k.main
dg = bpy.context.evaluated_depsgraph_get()
ev = ob.evaluated_get(dg)
me = ev.to_mesh()
gi = {g.index: g.name for g in ob.vertex_groups}
vg = {}
for v in ob.data.vertices:
    best = max(v.groups, key=lambda g: g.weight, default=None)
    vg[v.index] = gi[best.group] if best else "?"
W = ob.matrix_world
co = [W @ v.co for v in me.vertices]
mine = [i for i in range(len(co)) if vg[i] == bone]
others = {}
for p in me.polygons:
    g = vg[p.vertices[0]]
    if g != bone:
        others.setdefault(g, []).append([co[i] for i in p.vertices])
res = {}
for g, polys in others.items():
    verts, faces = [], []
    for pl in polys:
        faces.append(list(range(len(verts), len(verts) + len(pl))))
        verts.extend(pl)
    t = BVHTree.FromPolygons(verts, faces)
    d = min((t.find_nearest(co[i])[3] for i in mine), default=9)
    res[g] = round(d, 3)
near = sorted(res.items(), key=lambda kv: kv[1])[:6]
print("CLEAR " + json.dumps({"bone": bone, "verts": len(mine), "nearest": near}))
