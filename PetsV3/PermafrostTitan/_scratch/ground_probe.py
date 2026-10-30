# blender -b --factory-startup --python PermafrostTitan/_scratch/ground_probe.py -- <Name> <clip> [f0-f1]
# per-frame lowest mesh z (and the bone of the lowest vertex) of one clip - to tune ground contacts (kneels, crouches)
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip = argv[0], argv[1]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
n = k.clips[clip][0]
a, b = (int(v) for v in argv[2].split("-")) if len(argv) > 2 else (0, n)
k.set_action(clip)
vg = {g.index: g.name for g in k.main.vertex_groups}
out = []
for f in range(a, b + 1):
    bpy.context.scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    best = min(range(len(me.vertices)), key=lambda i: (mw @ me.vertices[i].co).z)
    z = (mw @ me.vertices[best].co).z
    src = k.main.data.vertices[best]
    bone = max(src.groups, key=lambda g: g.weight).group if src.groups else -1
    per = {}
    for i, v in enumerate(me.vertices):
        gs = k.main.data.vertices[i].groups
        if not gs:
            continue
        bn = vg.get(max(gs, key=lambda g: g.weight).group, "?")
        zz = (mw @ v.co).z
        if zz < per.get(bn, 9):
            per[bn] = zz
    low = sorted(per.items(), key=lambda t: t[1])[:3]
    out.append((f, round(z, 3), vg.get(bone, "?"), [(b, round(v, 3)) for b, v in low]))
    ev.to_mesh_clear()
print("GROUND " + json.dumps(out))
