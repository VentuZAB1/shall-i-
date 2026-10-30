# blender -b --factory-startup --python PermafrostTitan/_scratch/knee_frames.py -- <tag> [f0-f1]
# r10b: per frame of act_kneelrise - the kneeling knee height (lowest Shin_L vert within 0.14 of the Knee_L joint,
# as kneel_vis.py), the left foot's lowest point, and the lowest mesh point + its part
import sys, runpy, json, os
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
argv = sys.argv[sys.argv.index("--") + 1:]
tag = argv[0]
a, b = (int(v) for v in (argv[1] if len(argv) > 1 else "0-100").split("-"))
R3["full"]("PermafrostTitan", save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
k.set_action("act_kneelrise")
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in k.main.data.vertices]
knee_ids = None
rows = []
for f in range(a, b + 1):
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    W = [ev.matrix_world @ v.co for v in me.vertices]
    ev.to_mesh_clear()
    kj = k.arm.matrix_world @ k.arm.pose.bones["Knee_L"].head
    if knee_ids is None:
        knee_ids = [i for i in range(len(W)) if own[i] == "Shin_L" and (W[i] - kj).length < 0.14]
    gi = min(range(len(W)), key=lambda i: W[i].z)
    rows.append([f, round(min(W[i].z for i in knee_ids), 4),
                 round(min(W[i].z for i in range(len(W)) if own[i] == "Foot_L"), 4), round(W[gi].z, 4), own[gi]])
print("KNEEFRAMES " + json.dumps(rows))
open(os.path.join(k.dir, "_scratch", "knee_frames_%s.json" % tag), "w").write(json.dumps(rows))
