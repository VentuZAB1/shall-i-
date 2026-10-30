# r10b: does the kneeling knee slide on the snow after touch-down? Knee_L joint xy drift from the landing frame to f52
import runpy, json
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"]("PermafrostTitan", save=False)
k = R3["STATE"]["k"]
sc = bpy.context.scene
k.set_action("act_kneelrise")
P = {}
for f in range(14, 60):
    sc.frame_set(f)
    P[f] = (k.arm.matrix_world @ k.arm.pose.bones["Knee_L"].head).copy()
out = {}
for f0 in (16, 17, 18):
    out[f0] = round(max(((P[f] - P[f0]).to_2d()).length for f in range(f0, 53)), 4)
print("KNEESLIDE " + json.dumps({"drift_from": out, "f52_to_58": round(max(((P[f] - P[52]).to_2d()).length for f in range(52, 59)), 4)}))
