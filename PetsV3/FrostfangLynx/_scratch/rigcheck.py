# blender -b --factory-startup --python FrostfangLynx/_scratch/rigcheck.py -- <Name>
# builds model + rig (no clips) and prints the bone list + head pivot, to catch rig errors before the clip stage
import sys, runpy, json
name = sys.argv[sys.argv.index("--") + 1]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
m.rig(k)
k.build_rig()
bones = [b.name for b in k.arm.data.bones]
print("RIGCHECK " + json.dumps({"n": len(bones), "bones": bones,
                               "head": [round(v, 3) for v in k.arm.data.bones["Head"].head_local]}))
