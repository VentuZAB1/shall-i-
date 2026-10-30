# blender -b --factory-startup --python GlacierYeti/_scratch/footfalls.py -- <Name>
# Measured footfall order of the walk clip: per limb (k.meta legs), the frames where its foot / fist TOUCHES DOWN
# (world z of the foot joint drops back to its planted height after a swing).
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k = R3["STATE"]["k"]
import bpy
k.set_action("walk")
n = k.clips["walk"][0]
legs = [l for l, _ in k.meta["legs"]]
z = {l: [] for l in legs}
for f in range(0, 2 * n + 1):
    bpy.context.scene.frame_set(f % n if f != n else n)
    for l in legs:
        z[l].append(k.foot_world(l).z)
out = {}
for l in legs:
    lo = min(z[l][:n])
    down = [abs(v - lo) < 0.002 for v in z[l]]
    td = [f for f in range(1, 2 * n + 1) if down[f] and not down[f - 1]]
    out[l] = sorted(set(f % n for f in td))
order = sorted(((fs[0], l) for l, fs in out.items() if fs))
print("FOOTFALLS " + json.dumps({"n": n, "touchdown": out, "order": [l for _, l in order]}))
