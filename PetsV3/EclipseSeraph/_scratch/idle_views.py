# blender -b --factory-startup --python EclipseSeraph/_scratch/idle_views.py -- <Name> [views] [res]
# (builder D scratch) full build (model + rig + placeholder idle) and renders of idle f0 = the ground pose players see,
# from several views -> <Name>/renders/idle_<view>.png ; prints tris + the posed top / bottom.
import sys, runpy, os, json
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
views = argv[1].split(",") if len(argv) > 1 else ["tq", "front", "side", "back", "game"]
res = int(argv[2]) if len(argv) > 2 else 600
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
out = R3["full"](name, save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
pk.stage(k)
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
k.set_action("idle")
sc.frame_set(0)
dg = bpy.context.evaluated_depsgraph_get()
ev = k.main.evaluated_get(dg)
me = ev.to_mesh()
ws = [ev.matrix_world @ v.co for v in me.vertices]
zs = [w.z for w in ws]
xs = [w.x for w in ws]
ev.to_mesh_clear()
files = []
for v in views:
    loc, tgt = pk.camera_for(k, v)
    pk.aim(sc.camera, loc, tgt)
    p = os.path.join(k.dir, "renders", "idle_%s.png" % v)
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    files.append(p)
print("IDLE_RESULT " + json.dumps({"tris": out["tris_body"], "top": round(max(zs), 3), "low": round(min(zs), 3), "span": round(max(xs) - min(xs), 3),
                                   "files": len(files)}))
