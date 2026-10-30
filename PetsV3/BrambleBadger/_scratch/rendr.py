# blender -b --factory-startup --python BrambleBadger/_scratch/rendr.py -- <spec.json>
# Fixed-camera pose renders (the camera does NOT follow a bone): spec = {
#   "picks": [["act_burrow", 64], ...], "target": [x, y, z] (world), "res": 600, "prefix": "neck",
#   "views": {"lowside": [[dx, dy, dz], dist], ...}, "out": "<dir>"}
# -> <out>/<prefix>_<view>_<act>_<f>.png ; act "rest" = the bind pose
import sys, runpy, os, json
from mathutils import Vector
spec = json.load(open(sys.argv[sys.argv.index("--") + 1]))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](spec.get("name", "BrambleBadger"), save=False)
k = R3["STATE"]["k"]
pk = R3["pk"]
import bpy
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = int(spec.get("res", 600))
out = spec["out"]
os.makedirs(out, exist_ok=True)
t = Vector(spec["target"])
files = []
for act, f in spec["picks"]:
    if act == "rest":
        k.arm.data.pose_position = "REST"
    else:
        k.arm.data.pose_position = "POSE"
        k.set_action(act)
        sc.frame_set(int(f))
    for v, (d, dist) in spec["views"].items():
        pk.aim(sc.camera, t + Vector(d).normalized() * dist, t)
        p = os.path.join(out, "%s_%s_%s_%02d.png" % (spec["prefix"], v, act, int(f)))
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        files.append(p)
k.arm.data.pose_position = "POSE"
print("RENDR_RESULT " + json.dumps(files))
