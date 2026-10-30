# blender -b --factory-startup --python FrostcrownDragon/_scratch/minz.py -- <Name> <clip:f,...> : (builder D scratch)
# lowest vertex z (and its bone) at each clip frame
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](argv[0], save=False)
k = R3["STATE"]["k"]
names = {g.index: g.name for g in k.main.vertex_groups}
dom = [names[max(v.groups, key=lambda g: g.weight).group] if v.groups else "" for v in k.main.data.vertices]
out = {}
for tok in argv[1].split(","):
    c, f = tok.rsplit(":", 1)
    k.set_action(c)
    bpy.context.scene.frame_set(int(f))
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    zs = [(ev.matrix_world @ v.co).z for v in me.vertices]
    i = min(range(len(zs)), key=lambda j: zs[j])
    out[tok] = [round(zs[i], 4), dom[i]]
    ev.to_mesh_clear()
print("MINZ " + json.dumps(out))
