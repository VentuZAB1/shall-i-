# Mossback Tortoise (Wood egg #1): a sleepy, gentle chibi tortoise carrying a little garden on its shell - soft
# moss lumps, white + pink flowers with glowing hearts, a red-cap mushroom. Big sleepy eyes, rosy cheeks.
# Personality: an old softie - dozes off standing up and wakes with a start, munches grass, hides in its shell
# when it 'roars' and peeks back out.
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Mossback Tortoise"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 6.5
C = pk.lin
SKIN = C((150, 204, 120))
SKIN_D = C((112, 168, 92))
BELLY = C((246, 230, 160))
SHELL = C((168, 118, 70))
SHELL_L = C((206, 158, 96))
SHELL_RIM = C((120, 80, 48))
MOSS = C((104, 190, 78))
MOSS_L = C((156, 222, 104))
PETAL = C((255, 250, 244))
PETAL_P = C((255, 170, 200))
CAP = C((232, 64, 56))
STEM = C((250, 240, 220))
NAIL = C((250, 240, 214))
GLOW = "ffe066"

SH_C = Vector((0, 0.12, 0.74))
SH_R = (0.80, 0.92, 0.54)


def body_color(co, n):
    c = pk.mix(SKIN, SKIN_D, pk.smooth(0.3, 0.9, n.z) * 0.5)
    c = pk.mix(c, BELLY, pk.smooth(-0.3, -0.8, n.z) * pk.smooth(-0.6, -0.2, co.y))
    for sx in (1, -1):
        c = pk.mix(c, pk.BLUSH, pk.smooth(0.15, 0.04, (co - Vector((sx * 0.30, -1.20, 0.80))).length) * 0.6)
    return c


def plates():
    pts = [Vector((0, 0, 1))]
    for i in range(6):
        a = 2 * math.pi * i / 6
        pts.append(Vector((math.sin(math.radians(42)) * math.cos(a), math.sin(math.radians(42)) * math.sin(a),
                           math.cos(math.radians(42)))))
    for i in range(12):
        a = 2 * math.pi * (i + 0.5) / 12
        pts.append(Vector((math.sin(math.radians(78)) * math.cos(a), math.sin(math.radians(78)) * math.sin(a),
                           math.cos(math.radians(78)))))
    return pts


PLATES = plates()


def shell_color(u, lc):
    d = u.normalized()
    ds = sorted((d - p).length for p in PLATES)
    edge = ds[1] - ds[0]
    rim = pk.smooth(-0.15, -0.45, d.z)
    c = pk.mix(SHELL_L, SHELL, pk.smooth(0.0, 0.5, ds[0]))
    c = pk.mix(SHELL_RIM, c, pk.smooth(0.03, 0.09, edge))
    return pk.mix(c, SHELL_RIM, rim)


def model(k):
    E = [
        ("ell", (0, 0.12, 0.58), (0.66, 0.78, 0.36)),                       # torso inside the shell
        ("cap", (0, -0.40, 0.62), (0, -0.78, 0.74), 0.20),                  # neck
        ("ell", (0, -0.98, 0.86), (0.42, 0.40, 0.37)),                      # big chibi head
        ("ell", (0, -1.28, 0.78), (0.24, 0.16, 0.16)),                      # snout
        ("cap", (0, 0.86, 0.42), (0, 1.12, 0.30), 0.09),                    # tail
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.48, -0.34, 0.46), (sx * 0.50, -0.38, 0.10), 0.18),
              ("ell", (sx * 0.50, -0.42, 0.08), (0.20, 0.22, 0.09)),
              ("cap", (sx * 0.48, 0.58, 0.46), (sx * 0.50, 0.60, 0.10), 0.18),
              ("ell", (sx * 0.50, 0.56, 0.08), (0.20, 0.22, 0.09))]
    k.body(E, body_color, tris=5000)

    k.eyes([((0.55, -2.6, 0.98), (0.17, -0.8, 0.92)), ((-0.55, -2.6, 0.98), (-0.17, -0.8, 0.92))],
           size=(0.15, 0.165), style="sleepy", iris=(96, 64, 40), lid=SKIN_D)

    def face(bm, L):
        pts = []
        for x in (-0.09, -0.04, 0.0, 0.04, 0.09):
            p, n = k.surf((x, -2.4, 0.72 - 0.03 * (1 - abs(x) / 0.09)), (x * 0.5, -0.8, 0.76))
            pts.append(p + n * 0.01)
        pk.tube(bm, L, pts, 0.012, pk.lin((70, 50, 40)), sides=6)
        for sx in (1, -1):
            p, n = k.surf((sx * 0.05, -2.4, 0.86), (sx * 0.05, -0.8, 0.84))
            pk.ellipsoid(bm, L, p, (0.018, 0.012, 0.012), pk.lin((70, 90, 50)), z_axis=n)
        # toe nails
        for leg_y in (-0.42, 0.56):
            for sx in (1, -1):
                for dx in (-0.09, 0.0, 0.09):
                    pk.ellipsoid(bm, L, (sx * 0.50 + dx, leg_y - 0.19, 0.05), (0.045, 0.04, 0.035), NAIL)
    k.part("Face", face, lambda co: {"Head": 1.0} if co.z > 0.5 else
           {("Leg_F" if co.y < 0.1 else "Leg_B") + ("L" if co.x > 0 else "R"): 1.0})

    def shell(bm, L):
        pk.blob(bm, L, pk.frame(SH_C, (1, 0, 0), (0, 0, 1)), lambda u: Vector((u.x * SH_R[0], u.y * SH_R[1],
                (u.z if u.z > 0 else u.z * 0.55) * SH_R[2])), shell_color, 64, 32)
        # rim lip: a tube around the shell's oval edge
        ring = [SH_C + Vector((math.cos(a) * SH_R[0] * 1.01, math.sin(a) * SH_R[1] * 1.01, -0.02))
                for a in [2 * math.pi * i / 56 for i in range(57)]]
        pk.tube(bm, L, ring, 0.07, SHELL_RIM, sides=8)
    k.part("Shell", shell, "Spine")

    def top(u):  # point on the shell top at unit direction u
        d = Vector(u).normalized()
        return SH_C + Vector((d.x * SH_R[0], d.y * SH_R[1], d.z * SH_R[2]))

    def garden(bm, L):
        lumps = [((0.0, 0.05, 1), 0.30), ((0.35, -0.25, 1), 0.22), ((-0.40, 0.30, 1), 0.24), ((0.25, 0.45, 1), 0.2),
                 ((-0.2, -0.38, 1), 0.2), ((0.5, 0.2, 1), 0.18), ((-0.5, -0.1, 1), 0.18), ((0.0, 0.62, 1), 0.17),
                 ((0.1, -0.55, 1), 0.15)]
        for u, r in lumps:
            p = top(u)
            pk.ellipsoid(bm, L, p - Vector((0, 0, r * 0.3)), (r, r * 1.05, r * 0.78),
                         lambda uu, lc: pk.mix(MOSS, MOSS_L, pk.smooth(0.0, 1.0, uu.z)), useg=12, vseg=8)
        # flowers
        for u, col, s in (((0.45, 0.05, 1), PETAL, 0.15), ((-0.35, -0.15, 1), PETAL_P, 0.14), ((0.05, 0.5, 1), PETAL, 0.13)):
            p = top(u) + Vector((0, 0, 0.17))
            pk.puffy_star(bm, L, pk.frame(p, (1, 0, 0), (0, 0, 1)), s, col, depth=0.35)
        # mushroom
        b = top((-0.42, 0.42, 1)) + Vector((0, 0, 0.08))
        pk.tube(bm, L, [b, b + Vector((0, 0, 0.16))], (0.045, 0.04), STEM, sides=8)
        pk.blob(bm, L, pk.frame(b + Vector((0, 0, 0.16)), (1, 0, 0), (0, 0, 1)),
                lambda u: Vector((u.x * 0.14, u.y * 0.14, max(u.z, -0.15) * 0.10)), CAP, 14, 8)
        for a in range(5):
            ang = 2 * math.pi * a / 5
            pk.ellipsoid(bm, L, b + Vector((0.08 * math.cos(ang), 0.08 * math.sin(ang), 0.22)), (0.022, 0.022, 0.012),
                         STEM, useg=6, vseg=4)
    k.part("Garden", garden, "Spine")

    def glow(bm, L):
        for u in ((0.45, 0.05, 1), (-0.35, -0.15, 1), (0.05, 0.5, 1)):
            p = top(u) + Vector((0, 0, 0.21))
            pk.ellipsoid(bm, L, p, (0.055, 0.055, 0.04), pk.lin((255, 224, 102)), useg=8, vseg=6)
    pk.glow_part(k, "Glow_Flowers", GLOW, glow, "Spine")


def rig(k):
    k.joint("Spine", (0, 0.12, 0.60), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.42, 0.62), "Spine")
    k.joint("Head", (0, -0.80, 0.78), "Neck", tail=(0, -0.3, 0.05))
    k.joint("Tail1", (0, 0.86, 0.42), "Spine", tail=(0, 0.25, -0.12))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Leg_F" + side, (sx * 0.48, -0.34, 0.46), "Spine", tail=(0, 0, -0.4))
        k.joint("Leg_B" + side, (sx * 0.48, 0.58, 0.46), "Spine", tail=(0, 0, -0.4))
    k.body_bones = ["Spine", "Neck", "Head", "Tail1"] + cm.LEGS4


# ------------------------------------------------------------------ animation
def idle(k):
    """Dozes off: breathing shell, head slowly droops ... snaps awake with a little shake, blinks around, settles."""
    n = 96
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(0.8 * s, 0, 0), loc=(0, 0, 0.014 * (1 + s) / 2))
        k.key("Tail1", f, rot=(0, 10 * pk.wave(f, n, 0.1, 3), 0))
    track = [(0, -4, -3, 0, 0), (12, -4, -2, 0, 0), (40, 12, 18, 0, 0), (52, 16, 24, 0, 0), (55, -10, -12, 0, 0),
             (58, -6, -6, 0, 8), (61, -6, -6, 0, -8), (64, -6, -6, 0, 5), (68, -5, -4, 0, 0), (76, -4, -3, 14, 0),
             (86, -4, -3, -8, 0), (96, -4, -3, 0, 0)]
    for f, nk, hd, yaw, roll in track:
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, roll))
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = cm.LEGS4


def walk(k):
    n = 32

    def body(f):
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 0, 3.0 * pk.wave(f, n)), loc=(0, 0, 0.02 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        k.key("Neck", f, rot=(-3 + 3 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(-2 - 2 * pk.wave(f, n, 0.2, 2), 3 * pk.wave(f, n, 0.1), -2.5 * pk.wave(f, n)))
        k.key("Tail1", f, rot=(0, 12 * pk.wave(f, n, 0.3), 0))
    return cm.quad_walk(k, n, 0.42 * math.sin(math.radians(17)), 0.09, body, gait="walk")


def roar(k):
    """Hides in its shell (head + legs pull in, shell thumps down and wobbles), then peeks out and pops back."""
    import bpy
    n = 72
    k.new_action("roar", n, False)
    keys = [(0, 0.0, 0, 0, -4, -3, 0), (8, 0.0, 0, 0, -10, -14, 0), (14, -0.30, 0.50, 1, 0, 14, 0),
            (18, -0.33, 0.52, 1, 0, 14, 3), (22, -0.30, 0.52, 1, 0, 14, -3), (26, -0.32, 0.52, 1, 0, 14, 2),
            (40, -0.32, 0.52, 1, 0, 14, 0), (48, -0.30, 0.22, 1, 4, 6, 0), (56, -0.30, 0.22, 1, 4, 6, 0),
            (62, 0.02, 0.0, 0, -8, -10, 0), (72, 0.0, 0, 0, -4, -3, 0)]
    for f, z, back, hide, nk, hd, wob in keys:
        k.key("Spine", f, rot=(0, 0, wob), loc=(0, 0, z))
        k.key("Neck", f, rot=(nk, 0, 0), loc=(0, back, -0.12 * hide))
        k.key("Head", f, rot=(hd, 14 if 48 <= f <= 56 else 0, 0))
        k.key("Tail1", f, rot=(0, 0, 0), loc=(0, -0.12 * hide, 0.05 * hide))
    k.bake_bezier_now()
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        for leg in cm.LEGS4:
            if 13 <= f <= 59:
                continue
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f in (14, 40, 56):
        for leg in cm.LEGS4:
            k.key(leg, f, rot=(0, 0, 0), loc=(0, 0, 0.30))
    k.finish(loop=False)


def munch(k):
    """act: lowers its head to the grass, nibbles three times, chews happily with the head up."""
    n = 60
    k.new_action("act_munch", n, False)
    for f, nk, hd, sp in ((0, -4, -3, 0), (10, 22, 16, 4), (34, 22, 16, 4), (42, -6, -8, 0), (54, -6, -8, 0), (60, -4, -3, 0)):
        k.key("Spine", f, rot=(sp, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Tail1", f, rot=(0, 0, 0))
    for f in range(12, 33, 4):
        k.key("Head", f, rot=(16 + (10 if (f // 4) % 2 else 0), 0, 0))
    for f in range(43, 55, 3):
        k.key("Head", f, rot=(-8, 0, 4 if (f // 3) % 2 else -4))
    cm.plant(k, n)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    munch(k)
    return stride
