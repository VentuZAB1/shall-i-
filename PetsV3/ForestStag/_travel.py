# blender -b --factory-startup --python ForestStag/_travel.py  -> contact-tine travel per act_scratch stroke
import runpy
from mathutils import Vector
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
R3["full"]("ForestStag", save=False)
k, m = R3["STATE"]["k"], R3["STATE"]["m"]
P = [m.X(p, 1) for p in m.BEAM]
tips = [P[0].lerp(P[1], 0.30) + Vector((0.15, -1, 0.18)).normalized() * 0.26,
        P[0].lerp(P[1], 0.85) + Vector((0.25, -1, 0.80)).normalized() * 0.20,
        P[2] + Vector((0.30, -0.8, 1)).normalized() * 0.20]
k.set_action("act_scratch")
sc = bpy.context.scene


def at(f):
    sc.frame_set(f)
    M = k.arm.matrix_world @ k.arm.pose.bones["Head"].matrix @ k.arm.data.bones["Head"].matrix_local.inverted()
    return [M @ t for t in tips]


out = []
for a, b in ((22, 28), (32, 38), (42, 48), (52, 58), (62, 69)):
    pa, pb = at(a), at(b)
    out.append("%d->%d: %s" % (a, b, " ".join("%.3f" % (y - x).length for x, y in zip(pa, pb))))
print("TRAVEL " + " | ".join(out))
