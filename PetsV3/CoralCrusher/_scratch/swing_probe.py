# blender -b --factory-startup --python CoralCrusher/_scratch/swing_probe.py -- <Name> <clip> <fA> <fB> bone,bone
# world-space rotation angle (deg) of each bone between two frames + the bone direction change (deg)
import sys, runpy, json, math
argv = sys.argv[sys.argv.index("--") + 1:]
name, clip, fa, fb, bones = argv[0], argv[1], int(argv[2]), int(argv[3]), argv[4].split(",")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
k.set_action(clip)
arm = k.arm
M = {}
for f in (fa, fb):
    bpy.context.scene.frame_set(f)
    M[f] = {b: (arm.matrix_world @ arm.pose.bones[b].matrix).copy() for b in bones}
out = {}
for b in bones:
    qa, qb = M[fa][b].to_quaternion(), M[fb][b].to_quaternion()
    da, db = M[fa][b].col[1].xyz.normalized(), M[fb][b].col[1].xyz.normalized()
    out[b] = {"rot": round(math.degrees(qa.rotation_difference(qb).angle), 1),
              "dir": round(math.degrees(da.angle(db)), 1)}
print("SWING " + json.dumps(out))
