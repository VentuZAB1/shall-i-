import sys, os, json
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\TPTrees")
sys.argv = ["x"]
import tptree as T
import bpy
bpy.ops.wm.open_mainfile(filepath=T.TREE_BLEND_WIP)
sc = T.review_setup()
for o in bpy.data.objects:
    if o.type == "MESH":
        o.hide_render = o.name not in ("TrunkHi", "TPHi")
rb = json.load(open(os.path.join(T.WIP, "tree_build.json")))["rollA"]["centre"]
T.shoot(os.path.join(T.WIP, "dbg_rollA.png"), tuple(rb), (0.45, -1, 0.3), 4.5, 35)
rb = json.load(open(os.path.join(T.WIP, "tree_build.json")))["rollB"]["centre"]
T.shoot(os.path.join(T.WIP, "dbg_rollB.png"), tuple(rb), (-0.5, 1, 0.2), 4.5, 35)
