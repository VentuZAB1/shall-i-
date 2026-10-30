# builder E: which bone owns the lowest posed vertex?  blender -b ... --python Cvetibara/_low.py -- <Name> clip:frame,...
import sys, runpy
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
picks = [(t.split(":")[0], int(t.split(":")[1])) for t in argv[1].split(",")]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
for clip, f in picks:
    k.set_action(clip)
    bpy.context.scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = ev.to_mesh()
    lows = {}
    for v in me.vertices:
        z = (ev.matrix_world @ v.co).z
        b = owner[v.index]
        if z < lows.get(b, (9, None))[0]:
            lows[b] = (round(z, 3), tuple(round(c, 2) for c in body.data.vertices[v.index].co))
    ev.to_mesh_clear()
    print("LOW", clip, f, sorted(lows.items(), key=lambda kv: kv[1][0])[:4])
