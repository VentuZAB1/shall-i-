# blender -b --factory-startup --python PermafrostTitan/_scratch/kneel_cam.py -- <prefix> <frames> [views=game,game2x,tq,tq2x] [res=700]
# r10: fixed-camera renders of act_kneelrise. game / tq = pk.camera_for(k, view) at f0 (the gate cameras);
# game2x / tq2x = the same direction at half the distance, aimed at the kneeling knee's rest-hold area.
import sys, runpy, os, json
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
prefix, frames = argv[0], [int(v) for v in argv[1].split(",")]
opts = dict(a.split("=", 1) for a in argv[2:] if "=" in a)
views = opts.get("views", "game,game2x,tq,tq2x").split(",")
res = int(opts.get("res", "700"))
act = opts.get("act", "act_kneelrise")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk = R3["pk"]
R3["full"]("PermafrostTitan", save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = res
k.set_action(act)
sc.frame_set(0)
cams = {}
for v in ("game", "tq", "side"):
    loc, tgt = pk.camera_for(k, v)
    cams[v] = (Vector(loc), Vector(tgt))
# the 2x cameras look at the kneeling knee as it is at f40 (the hold) from half the distance
sc.frame_set(40)
low = k.arm.matrix_world @ k.arm.pose.bones["Knee_L"].head + Vector((0, 0, 0.30))
sc.frame_set(0)
for v in ("game", "tq"):
    loc, tgt = cams[v]
    d = (loc - tgt)
    cams[v + "2x"] = (low + d * 0.5, low)
    cams[v + "3x"] = (low + d / 3.0, low)   # r11: 3x crop of the lower body
out = os.path.join(k.dir, "_scratch", "r10")
os.makedirs(out, exist_ok=True)
files = []
for f in frames:
    sc.frame_set(f)
    for v in views:
        loc, tgt = cams[v]
        pk.aim(sc.camera, loc, tgt)
        p = os.path.join(out, "%s_%s_%02d.png" % (prefix, v, f))
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        files.append(p)
print("KNEELCAM " + json.dumps(files))
