# per-frame LOCAL rotation step (deg, f-1 -> f) of the limb bones in the walk -> WALKDUMP json
import runpy, json, math, os
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"]("BrambleBadger", save=False)
k = R3["STATE"]["k"]
import bpy
sc = bpy.context.scene
k.set_action("walk")
n = k.clips["walk"][0]
bones = [b.name for b in k.arm.pose.bones if b.name.startswith(("Leg_", "Shin_", "Foot_"))]
prev = {}
rows = {b: [] for b in bones}
for f in range(0, n + 1):
    sc.frame_set(f)
    for b in bones:
        q = k.arm.pose.bones[b].rotation_quaternion.copy()
        if b in prev:
            a = math.degrees(prev[b].rotation_difference(q).angle); a = min(a, 360 - a)
            rows[b].append(round(a, 2))
        prev[b] = q
print("WALKDUMP " + json.dumps({"n": n, "rows": rows}))
