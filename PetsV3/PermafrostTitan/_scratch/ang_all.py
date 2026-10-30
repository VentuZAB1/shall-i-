# blender -b --factory-startup --python PermafrostTitan/_scratch/ang_all.py -- <Name> bone,bone
# per clip, the max rotation angle (deg, matrix_basis vs rest = vs the parent) of each bone; the Chest = chest vs spine,
# the Head = head vs chest
import sys, runpy, json, math
argv = sys.argv[sys.argv.index("--") + 1:]
name, bones = argv[0], argv[1].split(",")
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"](name, save=False)
k = R3["STATE"]["k"]
arm = k.arm
out = {}
for clip, (n, loop) in k.clips.items():
    k.set_action(clip)
    mx = {b: (0.0, 0) for b in bones}
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        for b in bones:
            a = math.degrees(arm.pose.bones[b].matrix_basis.to_quaternion().angle)
            if a > mx[b][0]:
                mx[b] = (round(a, 2), f)
    out[clip] = mx
print("ANGALL " + json.dumps(out))
