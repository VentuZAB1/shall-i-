# blender -b --factory-startup --python BlizzardRoc/_scratch/under_view.py -- <Name> [res] : (builder D scratch) bind
# pose seen from below with the ground hidden -> renders/model_under.png (wing roots, tail base, trousers)
import sys, runpy, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
res = int(argv[1]) if len(argv) > 1 else 600
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["model"](name, views=("tq",), res=200)
import bpy
k = R3["STATE"]["k"]
pk = R3["pk"]
sc = bpy.context.scene
for o in bpy.data.objects:
    if o.name.lower().startswith("ground"):
        o.hide_render = True
sc.render.resolution_x = sc.render.resolution_y = res
pk.VIEWS["under"] = (0.25, -0.35, -1.0)
loc, tgt = pk.camera_for(k, "under")
pk.aim(sc.camera, loc, tgt)
sc.render.filepath = os.path.join(k.dir, "renders", "model_under.png")
bpy.ops.render.render(write_still=True)
print("UNDER_OK")
