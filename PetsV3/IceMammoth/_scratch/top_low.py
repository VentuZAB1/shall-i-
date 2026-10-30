# blender -b --factory-startup --python IceMammoth/_scratch/top_low.py -- <Name> <clip> <f,f,...> <bone,bone>
# Per frame and bone: the highest and the lowest world z of the vertices the bone owns (max weight) -> TOPLOW json
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, frames, bones = argv[0], argv[1], [int(v) for v in argv[2].split(",")], argv[3].split(",")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k = R3["STATE"]["k"]
import bpy
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
k.set_action(clip)
out = {}
for f in frames:
    bpy.context.scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = ev.to_mesh()
    r = {}
    for i, v in enumerate(me.vertices):
        o = owner[i]
        if o in bones:
            z = (ev.matrix_world @ v.co).z
            lo, hi = r.get(o, (9.0, -9.0))
            r[o] = (min(lo, z), max(hi, z))
    ev.to_mesh_clear()
    out[f] = {b: [round(r[b][0], 4), round(r[b][1], 4)] for b in r}
print("TOPLOW " + json.dumps(out))
