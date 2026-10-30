# blender -b --factory-startup --python BlizzardRoc/_scratch/crouch_depth.py -- <Name> <refclip> <clip:f,...> : (builder D
# scratch) how far the body sinks: z drop of the Spine / Chest / Neck / Head bone heads and of the body top (max z of
# the Spine + Chest + Neck vertices) against the ref clip's f0, in BU and in % of H (rest mesh height)
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](argv[0], save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
names = {g.index: g.name for g in k.main.vertex_groups}
dom = [names[max(v.groups, key=lambda g: g.weight).group] if v.groups else "" for v in k.main.data.vertices]
H = max(v.co.z for v in k.main.data.vertices) - min(v.co.z for v in k.main.data.vertices)


def snap(clip, f):
    k.set_action(clip)
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    top = max((ev.matrix_world @ v.co).z for v, d in zip(me.vertices, dom) if d in ("Spine", "Chest", "Neck"))
    ev.to_mesh_clear()
    out = {b: (k.arm.matrix_world @ k.arm.pose.bones[b].head).z for b in ("Spine", "Chest", "Neck", "Head")
           if b in k.arm.pose.bones}
    out["body_top"] = top
    return out


ref = snap(argv[1], 0)
res = {"H": round(H, 3)}
for tok in argv[2].split(","):
    c, f = tok.rsplit(":", 1)
    s = snap(c, int(f))
    res[tok] = {b: [round(ref[b] - s[b], 3), round(100 * (ref[b] - s[b]) / H, 1)] for b in s}
print("CROUCH " + json.dumps(res))
