# blender -b --factory-startup --python VoltRhino/_scratch/pose_under.py -- <Name> <act:frame,...> <Bone> <dist> [res] [views]
# Posed renders from BELOW with the ground hidden (pclose_* uses a ground-level camera that ends up under the floor):
# aims at the posed head of <Bone> from each view direction -> renders/punder_<view>_<act>_<f>.png
import sys, runpy, os, json
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
name, bone, dist = argv[0], argv[2], float(argv[3])
picks = [(t.rsplit(":", 1)[0], int(t.rsplit(":", 1)[1])) for t in argv[1].split(",")]
res = int(argv[4]) if len(argv) > 4 else 480
views = argv[5].split(",") if len(argv) > 5 else ["under", "underside"]
D = {"under": (0.25, -0.55, -1.0), "underside": (1.0, -0.35, -0.55), "underback": (0.4, 0.8, -0.8)}
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
import bpy
sc = bpy.context.scene
g = bpy.data.objects.get("Ground")
if g:
    g.hide_render = True
sc.render.resolution_x = sc.render.resolution_y = res
files = []
for act, f in picks:
    k.set_action(act)
    sc.frame_set(f)
    t = k.arm.matrix_world @ k.arm.pose.bones[bone].head
    for v in views:
        pk.aim(sc.camera, t + Vector(D[v]).normalized() * dist, t)
        p = os.path.join(k.dir, "renders", "punder_%s_%s_%02d.png" % (v, act, f))
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        files.append(p)
print("HEADLESS_RESULT " + json.dumps(files))
