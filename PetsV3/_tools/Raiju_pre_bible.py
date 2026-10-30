# Raiju (Thunder egg): a proud thunder wolf in the Steal-an-Egg block style.
# Built BIG: long legs, deep chest, forward-leaning neck, long muzzle, tall pointed ears, so a heavy pet looks huge.
# Electric-blue fur with a white muzzle / bib / cheek ruffs, navy boots + brows, glowing yellow eyes, glowing
# lightning bolts on the flanks, glowing bands on the legs and a lightning-bolt tail.
import math
from mathutils import Vector

DISPLAY = "Raijū"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.0

BLUE = (52, 104, 236)
BLUE_D = (40, 82, 200)
WHITE = (236, 242, 255)
NAVY = (30, 36, 86)
YELLOW = (255, 206, 46)
DARK = (22, 22, 38)
MOUTH = (150, 40, 64)
BOLT = "ffd23a"
EYE = "ffe65c"


def slab(B, p0, p1, width, thick, color, bone, **kw):
    """flat bar from p0 to p1 in a y-z plane (its thin side along x)"""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    th = math.degrees(math.atan2(-d.y, d.z))
    return B.add((p0 + p1) / 2, (thick, width / 2, d.length / 2), color, bone, rot=(th, 0, 0), **kw)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, cell=0.12, stud_h=0.03, seed=11)
    # ---- body
    B.add((0, 0.36, 1.27), (0.34, 0.46, 0.31), BLUE, "Spine", bot=(0.92, 0.95))                  # hips
    B.add((0, -0.38, 1.24), (0.40, 0.40, 0.40), BLUE, "Chest", bot=(0.86, 1.0))                  # chest
    B.add((0, -0.79, 1.18), (0.27, 0.02, 0.30), WHITE, "Chest", studs=[], bevel=0.012, bot=(0.75, 1))  # bib
    for x in (-0.15, 0.0, 0.15):                                                                 # chest fur tufts
        B.add((x, -0.74, 0.80), (0.075, 0.05, 0.11), WHITE, "Chest", rot=(170, 0, 0), top=(0.12, 0.3), studs=[])
    for i in range(3):                                                                           # back stripes
        B.add((0, 0.12 + i * 0.22, 1.585), (0.24 - i * 0.02, 0.035, 0.012), NAVY, "Spine", studs=[], bevel=0.008)
    # ---- neck + head
    B.add((0, -0.74, 1.62), (0.26, 0.24, 0.34), BLUE, "Neck", rot=(32, 0, 0))
    B.add((0, -0.948, 1.49), (0.18, 0.012, 0.26), WHITE, "Neck", rot=(32, 0, 0), studs=[], bevel=0.01)  # throat
    B.add((0, -1.04, 2.02), (0.30, 0.28, 0.26), BLUE, "Head", studs=["+x", "-x", "+y", "+z"])
    for y, z, sz in ((-0.62, 1.88, 1.0), (-0.50, 1.74, 0.85)):                                  # neck mane
        B.add((0, y, z), (0.07 * sz, 0.08 * sz, 0.14 * sz), BLUE_D, "Neck", rot=(-48, 0, 0), top=(0.15, 0.25), studs=[])
    B.add((0, -1.50, 1.90), (0.17, 0.12, 0.20), WHITE, "Head", rot=(90, 0, 0), top=(0.82, 0.85))  # muzzle
    B.add((0, -1.47, 2.03), (0.075, 0.19, 0.012), BLUE, "Head", studs=[], bevel=0.008)          # blaze on the muzzle
    B.add((0, -1.715, 1.96), (0.062, 0.03, 0.048), DARK, "Head", studs=[], bevel=0.015)        # nose
    B.add((0, -1.46, 1.775), (0.13, 0.17, 0.012), MOUTH, "Head", studs=[], bevel=0.006)         # mouth roof
    B.mirror((0.08, -1.645, 1.75), (0.024, 0.018, 0.045), WHITE, "Head", studs=[], bevel=0.006,
             top=(0.15, 0.2), rot=(180, 0, 0))                                                   # fangs
    B.add((0, -1.40, 1.72), (0.14, 0.18, 0.055), WHITE, "Jaw", bot=(0.85, 0.9))                 # lower jaw
    B.mirror((0.31, -0.98, 1.88), (0.09, 0.10, 0.12), WHITE, "Head", rot=(0, 80, 25), top=(0.12, 0.2), studs=[])
    B.mirror((0.29, -0.90, 1.78), (0.07, 0.08, 0.10), WHITE, "Head", rot=(0, 95, 35), top=(0.12, 0.2), studs=[])
    B.add((0, -0.96, 2.32), (0.07, 0.09, 0.10), BLUE, "Head", rot=(-25, 0, 0), top=(0.2, 0.3), studs=[])  # forelock
    B.mirror((0.19, -0.96, 2.42), (0.105, 0.065, 0.20), BLUE, "Ear_{s}", rot=(0, 14, 0), top=(0.12, 0.35))
    B.mirror((0.19, -1.03, 2.40), (0.065, 0.012, 0.15), YELLOW, "Ear_{s}", rot=(0, 14, 0), top=(0.12, 1),
             studs=[], bevel=0.006)
    # ---- face: glowing eyes, slit pupils, angled brows
    for s in (1, -1):
        B.eye((s * 0.135, -1.322, 2.13), (s * 0.12, -1, 0), 0.09, 0.08, (255, 214, 52), look=(-s * 0.15, 0))
    B.mirror((0.14, -1.345, 2.235), (0.118, 0.016, 0.028), NAVY, "Head", rot=(0, -20, 0), studs=[], bevel=0.008)
    # ---- legs (long, so a big Raiju stands tall): blue leg, navy boot + paw, glowing band
    B.mirror((0.24, -0.50, 0.52), (0.12, 0.13, 0.46), BLUE, "Leg_F{s}")
    B.mirror((0.24, -0.50, 0.24), (0.135, 0.145, 0.11), NAVY, "Leg_F{s}")
    B.mirror((0.24, -0.56, 0.07), (0.15, 0.19, 0.07), NAVY, "Leg_F{s}", studs=[])
    B.mirror((0.24, -0.50, 0.37), (0.138, 0.148, 0.02), (255, 210, 58), "Leg_F{s}", studs=[], bevel=0.008, glow=BOLT)
    B.mirror((0.25, 0.52, 1.02), (0.15, 0.27, 0.27), BLUE, "Leg_B{s}", rot=(-10, 0, 0))          # haunch
    B.mirror((0.25, 0.66, 0.50), (0.11, 0.12, 0.40), BLUE, "Leg_B{s}", rot=(-8, 0, 0))
    B.mirror((0.25, 0.62, 0.24), (0.13, 0.14, 0.11), NAVY, "Leg_B{s}")
    B.mirror((0.25, 0.57, 0.07), (0.15, 0.19, 0.07), NAVY, "Leg_B{s}", studs=[])
    B.mirror((0.25, 0.63, 0.37), (0.133, 0.143, 0.02), (255, 210, 58), "Leg_B{s}", studs=[], bevel=0.008, glow=BOLT)
    # ---- glowing lightning bolts on the flanks
    for s in (1, -1):   # on the chest sides (the chest tapers: x = 0.344 at z 0.84 -> 0.40 at z 1.64)
        nrm = Vector((s * 0.9976, 0, -0.07))
        pts = [(-0.64, 1.54), (-0.38, 1.28), (-0.48, 1.23), (-0.14, 0.94)]
        P = [Vector((s * (0.344 + (z - 0.84) * 0.07 + 0.012), y, z)) for y, z in pts]
        for a, b in zip(P, P[1:]):
            B.bar(a, b, nrm, 0.085, 0.014, (255, 210, 58), "Chest", studs=[], bevel=0.006, glow=BOLT)
    # ---- lightning-bolt tail on a furry base
    B.add((0, 0.86, 1.50), (0.11, 0.12, 0.15), BLUE, "Tail1", rot=(-55, 0, 0))
    slab(B, (0, 0.88, 1.52), (0, 1.12, 1.92), 0.15, 0.055, (255, 210, 58), "Tail1", studs=[], glow=BOLT)
    slab(B, (0, 1.14, 1.90), (0, 0.98, 2.04), 0.14, 0.055, (255, 210, 58), "Tail2", studs=[], glow=BOLT)
    B.add((0, 1.15, 2.24), (0.055, 0.085, 0.26), (255, 210, 58), "Tail3", rot=(-38, 0, 0), top=(0.4, 0.1),
          studs=[], glow=BOLT)
    B.build()
    return {"studs": B.stud_count}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.30, 1.27), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.05, 1.26), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.56, 1.45), "Chest")
    k.joint("Head", (0, -0.86, 1.90), "Neck", tail=(0, -0.35, 0.05))
    k.joint("Jaw", (0, -1.24, 1.75), "Head", tail=(0, -0.3, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.18, -0.96, 2.24), "Head", tail=(0, 0, 0.3))
        k.joint("Leg_F" + side, (s * 0.24, -0.50, 1.00), "Chest", tail=(0, 0, -0.45))
        k.joint("Leg_B" + side, (s * 0.25, 0.60, 1.05), "Spine", tail=(0, 0, -0.45))
    k.joint("Tail1", (0, 0.82, 1.45), "Spine")
    k.joint("Tail2", (0, 1.12, 1.90), "Tail1")
    k.joint("Tail3", (0, 1.00, 2.02), "Tail2", tail=(0, 0.3, 0.4))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm
TAIL = ["Tail1", "Tail2", "Tail3"]


def ears(k, f, l=0.0, r=None, splay=0.0):
    r = l if r is None else r
    k.key("Ear_L", f, rot=(l, 0, splay))
    k.key("Ear_R", f, rot=(r, 0, -splay))


def idle(k):
    """Proud sentinel: scans left and right with snappy turns and holds, ear flicks, light panting, tail bolt sways,
    then puffs its chest out with the chin raised high before settling again."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.012 * b))
        k.key("Chest", f, rot=(-1.5 - 1.2 * b, 0, 0))
        cm.chain(k, f, n, TAIL, sway=7, pitch=0, cycles=2, lag=0.12, grow=0.5)
        k.key("Jaw", f, rot=(3 + 3 * pk.wave(f, n, 0, 10), 0, 0))
    # head: look ahead -> left -> right -> ahead (snappy turns, holds)
    for f, nk, hd, yaw, tilt in ((0, -6, -6, 0, 0), (22, -6, -6, 0, 0), (28, -8, -4, 26, 4), (48, -8, -4, 26, 4),
                                 (54, -6, -8, -22, -3), (74, -6, -8, -22, -3), (80, -6, -6, 0, 0),
                                 (86, -6, -6, 0, 0), (92, -14, -10, 0, 0), (106, -14, -10, 0, 0), (114, -6, -6, 0, 0), (120, -6, -6, 0, 0)):
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, tilt))
    # ears: perked, flick right at 40, flick left at 66, both perk forward when it looks around
    for f, l, r in ((0, 0, 0), (26, 6, 6), (38, 6, 6), (40, 6, -22), (43, 6, 6), (46, 6, -16), (50, 6, 6),
                    (64, 4, 4), (66, -22, 4), (70, 4, 4), (82, 0, 0), (120, 0, 0)):
        ears(k, f, l, r)
    # proud chest puff 86-112: chest lifts, chin high, then settles
    for f, ch in ((84, -1.5), (92, -7), (106, -7), (114, -1.5)):
        k.key("Chest", f, rot=(ch, 0, 0))
    cm.plant(k, n)
    k.finish()


def walk(k):
    n = 20

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.0 * pk.wave(f, n, 0.1, 2), 0, 2.2 * pk.wave(f, n)), loc=(0, 0, 0.035 * b))
        k.key("Chest", f, rot=(-1.5, 3.0 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n)))
        k.key("Neck", f, rot=(-4 + 2.5 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(-4 - 2.5 * pk.wave(f, n, 0.2, 2), -2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(5 + 2 * pk.wave(f, n, 0, 2), 0, 0))
        ears(k, f, -8, -8)
        cm.chain(k, f, n, TAIL, sway=9, pitch=-4, cycles=1, lag=0.15)
    return cm.quad_walk(k, n, 0.30, 0.14, body, gait="trot")


def roar(k):
    """HOWL: leans back, chin to the sky, jaw wide open, ears pinned back, tail bolt snaps up and buzzes."""
    n = 66
    k.new_action("roar", n, False)
    P = [(0, 0, -6, -6, 3, 0), (10, -6, -14, -12, 6, 0.4), (20, -10, -34, -30, 28, 1), (48, -10, -36, -32, 30, 1),
         (56, -3, -12, -10, 8, 0.3), (66, 0, -6, -6, 3, 0)]
    for f, ch, nk, hd, jw, t in P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, -0.03 * t))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        ears(k, f, -30 * t, -30 * t)
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(14 * t, 0, 0))
    for f in range(22, 48, 2):          # the howl wavers
        w = 1 if (f // 2) % 2 else -1
        k.key("Head", f, rot=(-31, 0, 2.5 * w))
        k.key("Tail3", f, rot=(14, 7 * w, 0))
    cm.plant(k, n)
    k.finish(loop=False)


def thunderflip(k):
    """SIGNATURE (Raiju only): crouches low with ears pinned, EXPLODES upward into a full barrel roll with all four
    legs tucked, lands on all fours and holds a proud power pose (chest high, chin up, tail bolt raised)."""
    import bpy
    n = 64
    k.new_action("act_thunderflip", n, False)
    Y = (0, 1, 0)
    # body path: (frame, spine z, roll degrees about the body axis, chest pitch, neck, head, ears, tail pitch)
    P = [(0, 0.0, 0, 0, -6, -6, 0, 0), (8, -0.07, 0, 4, -2, -4, -20, 4), (14, -0.11, 0, 6, 0, -2, -30, 4),
         (18, 0.30, 0, -4, -10, -8, -30, 8), (21, 0.70, 90, -2, -8, -8, -30, 10), (24, 0.95, 180, 0, -6, -8, -30, 10),
         (27, 0.95, 270, 0, -6, -8, -30, 10), (30, 0.70, 360, -2, -8, -8, -26, 6), (34, 0.18, 360, -4, -16, -14, -10, 0),
         (38, -0.08, 360, 2, -10, -8, 0, 0), (44, 0.0, 360, -6, -14, -10, 10, 14), (56, 0.0, 360, -6, -14, -10, 10, 14),
         (64, 0.0, 360, 0, -6, -6, 0, 0)]
    for f, z, roll, ch, nk, hd, ear, tp in P:
        cm.key_axis(k, "Spine", f, Y, roll, loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(14 if 44 <= f <= 56 else 3, 0, 0))
        ears(k, f, ear, ear)
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(tp, 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in list(range(0, 17)) + list(range(36, n + 1)):          # paws planted before take-off and after landing
        sc.frame_set(f)
        for leg in cm.LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f, front, back, spl in ((18, 30, 34, 0), (22, 16, -16, 12), (30, 16, -16, 12), (34, 0, 4, 2)):  # push, tuck, reach
        for leg in cm.LEGS4:
            sx = 1 if leg.endswith("L") else -1
            k.key(leg, f, rot=(front if "_F" in leg else back, 0, -sx * spl), loc=(0, 0, 0))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    thunderflip(k)
    return stride


# 2026-10-08 head pass (user: heads far too small for the big bodies): grow the head group about the neck junction
HEAD_XF = [((0, -0.86, 1.90), 1.5, ("Head", "Jaw", "Ear_L", "Ear_R"))]
