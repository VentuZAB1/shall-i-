# blender -b --factory-startup --python PermafrostTitan/_scratch/fist_probe.py -- <Name> <clip> <f,f,...>
# r3 M3 check: distance from the Fist_L / Hand_L-weighted fist mesh to the Leg_L-weighted (thigh) mesh, the fist
# centre height vs the chest line (the Chest bone head), per frame
import sys, runpy, json
from mathutils import Vector
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, frames = argv[0], argv[1], [int(v) for v in argv[2].split(",")]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
k.set_action(clip)
vg = {g.index: g.name for g in k.main.vertex_groups}
own = []
for v in k.main.data.vertices:
    own.append(vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?")
out = {}
for f in frames:
    bpy.context.scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    thigh = [mw @ me.vertices[i].co for i in range(len(me.vertices)) if own[i] == "Leg_L"]
    fist = [mw @ me.vertices[i].co for i in range(len(me.vertices)) if own[i] in ("Hand_L", "Fist_L")]
    tv = [i for i in range(len(me.vertices)) if own[i] == "Leg_L"]
    tset = set(tv)
    polys = [[v for v in pl.vertices] for pl in me.polygons if all(v in tset for v in pl.vertices)]
    bvh = BVHTree.FromPolygons([mw @ v.co for v in me.vertices], polys)
    gap = min(bvh.find_nearest(p)[3] for p in fist)                    # surface distance (true gap)
    c = sum(fist, Vector()) / len(fist)
    kd = KDTree(len(thigh))
    for i, p in enumerate(thigh):
        kd.insert(p, i)
    kd.balance()
    chest = (k.arm.matrix_world @ k.arm.pose.bones["Chest"].head).z
    out[f] = {"fist_to_thigh_min_gap": round(gap, 3), "fist_centre_to_thigh_surface": round(bvh.find_nearest(c)[3], 3),
              "fist_centre_z": round(c.z, 3), "chest_line_z": round(chest, 3)}
    ev.to_mesh_clear()
print("FIST " + json.dumps(out))
