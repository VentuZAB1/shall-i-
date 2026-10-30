# blender -b --factory-startup --python VoltRhino/_scratch/probe.py -- <Name> <clip> <f,f,...> <bone,bone>
# Per frame: world z of the given bones' heads + the lowest mesh vertex per owning bone (Head / Jaw / ...).
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, frames, bones = argv[0], argv[1], [int(v) for v in argv[2].split(",")], argv[3].split(",")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k = R3["STATE"]["k"]
import bpy
arm, body = k.arm, k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
rest = [v.co.copy() for v in body.data.vertices]
for i, o in enumerate(owner):                          # split the Head group: horn (rest z > 0.98) vs the rest of the head
    if o == "Head" and rest[i].z < 0.98:
        owner[i] = "Head_noHorn"
k.set_action(clip)
out = {}
for f in frames:
    bpy.context.scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = ev.to_mesh()
    low = {}
    for i, v in enumerate(me.vertices):
        z = (ev.matrix_world @ v.co).z
        o = owner[i]
        if o not in low or z < low[o]:
            low[o] = z
    ev.to_mesh_clear()
    keep = {b: round(low[b], 3) for b in low if b and b.startswith("Foot")}
    out[f] = {"bones": {b: [round(c, 3) for c in (arm.matrix_world @ arm.pose.bones[b].head)] for b in bones},
              "low": dict(sorted(keep.items(), key=lambda x: x[1])[:4])}
print("PROBE " + json.dumps(out))
