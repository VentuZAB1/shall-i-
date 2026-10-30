# blender -b --python _tools/lowpoint.py -- <Name> <clip> <frame> : which part is lowest at that frame
import sys, runpy
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, frame = argv[0], argv[1], int(argv[2])
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in body.data.vertices]
rest = [v.co.copy() for v in body.data.vertices]
k.set_action(clip)
bpy.context.scene.frame_set(frame)
ev = body.evaluated_get(bpy.context.evaluated_depsgraph_get())
me = ev.to_mesh()
pts = sorted(((ev.matrix_world @ v.co).z, i) for i, v in enumerate(me.vertices))[:8]
for z, i in pts:
    print("LOW", round(z, 3), owner[i], "rest", tuple(round(c, 2) for c in rest[i]))
ev.to_mesh_clear()
