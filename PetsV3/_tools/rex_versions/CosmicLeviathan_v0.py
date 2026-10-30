# Cosmic Leviathan (Celestial egg SECRET 1 %, 2026-10-14) - v0 HULL TEST ONLY (curveloft S-body), the real build
# follows the plan review (_review/CosmicLeviathan_plan.md + _plan_review.md).
import math
from mathutils import Vector

DISPLAY = "Cosmic Leviathan"
MOTION = "Swim"
RIG = "fish"
HEIGHT = 10.0

ARMOR = (24, 26, 48)
HIDE = (34, 74, 190)
BELLY = (248, 230, 178)

# centreline stations head -> tail: y, z, half-width, half-height
ST = [(-1.16, 1.24, 0.13, 0.12), (-1.02, 1.22, 0.19, 0.17), (-0.82, 1.02, 0.20, 0.22), (-0.55, 0.72, 0.30, 0.30),
      (-0.15, 0.45, 0.27, 0.26), (0.20, 0.40, 0.23, 0.22), (0.55, 0.48, 0.18, 0.17), (0.90, 0.62, 0.13, 0.12),
      (1.20, 0.78, 0.085, 0.08), (1.42, 0.90, 0.05, 0.05)]
JOINT_Y = {"Neck": -0.92, "Chest": -0.70, "Spine": -0.30, "Tail1": 0.38, "Tail2": 0.74, "Tail3": 1.06, "Tail4": 1.32}
L = None


def loft():
    global L
    if L is None:
        import curveloft as cl
        L = cl.Loft(ST, n=2.4, seg=24)
    return L


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=501, tier=5, plates=False, th=0.60)       # th: tubes are not boxes
    Lf = loft()
    js = {b: Lf.s_at_y(y) for b, y in JOINT_Y.items()}
    order = [("Head", 0.0, js["Neck"]), ("Neck", js["Neck"], js["Chest"]), ("Chest", js["Chest"], js["Spine"]),
             ("Spine", js["Spine"], js["Tail1"]), ("Tail1", js["Tail1"], js["Tail2"]),
             ("Tail2", js["Tail2"], js["Tail3"]), ("Tail3", js["Tail3"], js["Tail4"]), ("Tail4", js["Tail4"], Lf.length)]
    for i, (bone, a, b) in enumerate(order):
        j0 = a if i > 0 else None
        j1 = b if i < len(order) - 1 else None
        Lf.tube(B, max(0.0, a - (0.06 if j0 else 0)), min(Lf.length, b + (0.06 if j1 else 0)), HIDE, bone, j0=j0, j1=j1)
    Lf.band(B, js["Neck"] - 0.05, js["Tail3"], BELLY, "Chest", zlo=-1.0, zhi=-0.45)
    Lf.band(B, js["Chest"], js["Tail2"], ARMOR, "Spine", zlo=0.45, narrow1=0.3)
    B.build()
    return {}


def rig(k):
    Lf = loft()
    prev = "Root"
    for b in ("Spine",):
        pass
    c = lambda y: Lf.at(Lf.s_at_y(y))[0]
    k.joint("Spine", tuple(c(JOINT_Y["Spine"])), "Root", tail=(0, 0.3, 0))
    k.joint("Chest", tuple(c(JOINT_Y["Chest"])), "Spine", tail=(0, -0.3, 0))
    k.joint("Neck", tuple(c(JOINT_Y["Neck"])), "Chest", tail=(0, -0.2, 0.1))
    k.joint("Head", tuple(c(-1.02)), "Neck", tail=(0, -0.2, 0))
    k.joint("Tail1", tuple(c(JOINT_Y["Tail1"])), "Spine", tail=(0, 0.3, 0))
    k.joint("Tail2", tuple(c(JOINT_Y["Tail2"])), "Tail1", tail=(0, 0.3, 0))
    k.joint("Tail3", tuple(c(JOINT_Y["Tail3"])), "Tail2", tail=(0, 0.25, 0))
    k.joint("Tail4", tuple(c(JOINT_Y["Tail4"])), "Tail3", tail=(0, 0.2, 0))


def check_pairs():
    return []


def joints():
    return []
