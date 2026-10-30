# blender -b --factory-startup --python IceMammoth/_scratch/vert_travel.py -- <Name> <clip> <fA> <fB> <bone,bone>
# Per listed bone: displacement of the vertices it owns (max weight) between frames fA and fB, in world units:
# max |d| in the side (y,z) plane, max |dx|, and the vertex (rest coords) with the largest side-plane move.
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, fa, fb, bones = argv[0], argv[1], int(argv[2]), int(argv[3]), argv[4].split(",")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k = R3["STATE"]["k"]
import bpy
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
k.set_action(clip)
pos = {}
for f in (fa, fb):
    bpy.context.scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = ev.to_mesh()
    pos[f] = [(ev.matrix_world @ v.co).copy() for v in me.vertices]
    ev.to_mesh_clear()
out = {}
for b in bones:
    idx = [i for i, o in enumerate(owner) if o == b]
    best, bx = (0.0, -1), 0.0
    for i in idx:
        d = pos[fb][i] - pos[fa][i]
        s = (d.y ** 2 + d.z ** 2) ** 0.5
        if s > best[0]:
            best = (s, i)
        bx = max(bx, abs(d.x))
    i = best[1]
    out[b] = {"verts": len(idx), "max_side_plane": round(best[0], 4), "max_dx": round(bx, 4),
              "at": [round(c, 3) for c in pos[fa][i]] if i >= 0 else None}
print("TRAVEL " + json.dumps(out))
