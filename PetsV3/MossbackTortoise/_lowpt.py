# blender -b --factory-startup --python MossbackTortoise/_lowpt.py -- <Name> <clip> <frame>[,<frame>...]
# prints the lowest posed vertices (z) and the bone that owns them (no files written)
import sys, runpy
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, frames = argv[0], argv[1], [int(x) for x in argv[2].split(",")]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
out = R3["full"](name, save=False)
k = R3["STATE"]["k"]
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
k.set_action(clip)
for f in frames:
    bpy.context.scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = ev.to_mesh()
    rows = []
    for v in me.vertices:
        z = (ev.matrix_world @ v.co).z
        g = names[max(body.data.vertices[v.index].groups, key=lambda g: g.weight).group] if body.data.vertices[v.index].groups else "?"
        rows.append((z, g, tuple(round(c, 3) for c in (ev.matrix_world @ v.co))))
    rows.sort()
    seen = set()
    res = []
    for z, g, p in rows:
        if g not in seen:
            seen.add(g)
            res.append("%s %.3f %s" % (g, z, p))
        if len(res) >= 6:
            break
    ev.to_mesh_clear()
    print("LOWPT f%d: %s" % (f, " | ".join(res)))
