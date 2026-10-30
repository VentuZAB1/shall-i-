import runpy, json
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"]("FrostfangLynx", save=False)
k = R3["STATE"]["k"]
import bpy
sc = bpy.context.scene
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
k.set_action("walk")
out = []
for f in range(0, 31):
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get(); ev = body.evaluated_get(dg); me = ev.to_mesh()
    i, z = min(((i, (ev.matrix_world @ v.co).z) for i, v in enumerate(me.vertices)), key=lambda t: t[1])
    out.append((f, round(z, 4), owner[i]))
    ev.to_mesh_clear()
print("LOWEST " + json.dumps(out))
