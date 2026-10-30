# Treant (Wood egg #3): a chibi tree sprite - a round barrel trunk with a big friendly face, a puffy leaf crown full
# of pink blossoms and glowing golden fruit, twig arms with leaf hands, stubby root feet. Personality: a cheerful
# little sapling - sways in a breeze, soaks up the sun with arms up, waddles, waves hello; its 'roar' is a bloom
# burst (arms wide, crown puffs up and shakes).
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Treant"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 7.5
C = pk.lin
BARK = C((150, 100, 62))
BARK_L = C((190, 136, 86))
BARK_D = C((110, 72, 44))
FACE = C((222, 176, 120))
LEAF = C((86, 182, 72))
LEAF_L = C((150, 226, 96))
LEAF_D = C((58, 140, 60))
PINK = C((255, 172, 206))
GLOW = "ffd86b"
CROWN = Vector((0, 0.04, 1.62))


def body_color(co, n):
    grain = 0.5 + 0.5 * math.sin(math.atan2(co.x, co.y) * 14 + co.z * 3.0)
    c = pk.mix(BARK, BARK_L, pk.smooth(0.55, 0.95, grain) * 0.6)
    # lighter face patch on the front
    face = pk.smooth(-0.4, -0.85, n.y) * pk.smooth(0.55, 0.75, co.z) * pk.smooth(1.32, 1.1, co.z)
    c = pk.mix(c, FACE, face)
    c = pk.mix(c, BARK_D, pk.smooth(0.16, 0.05, co.z))
    for sx in (1, -1):
        c = pk.mix(c, pk.BLUSH, pk.smooth(0.12, 0.03, (co - Vector((sx * 0.25, -0.40, 0.84))).length) * 0.6)
    return c


def model(k):
    E = [
        ("ell", (0, 0.0, 0.80), (0.46, 0.40, 0.58)),
        ("ell", (0, 0.0, 0.34), (0.38, 0.34, 0.24)),
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.20, 0.0, 0.34), (sx * 0.23, -0.02, 0.10), 0.13),
              ("ell", (sx * 0.23, -0.07, 0.07), (0.16, 0.20, 0.08))]
    k.body(E, body_color, tris=4800)

    k.eyes([((0.55, -2.6, 0.98), (0.17, -0.3, 0.98)), ((-0.55, -2.6, 0.98), (-0.17, -0.3, 0.98))],
           size=(0.15, 0.17), style="big", iris=(96, 190, 80))

    def face(bm, L):
        pts = []
        for x in (-0.12, -0.06, 0.0, 0.06, 0.12):
            q, qn = k.surf((x, -2.4, 0.78 - 0.05 * (1 - (x / 0.12) ** 2)), (x * 0.5, 0, 0.78))
            pts.append(q + qn * 0.012)
        pk.tube(bm, L, pts, 0.016, pk.lin((90, 50, 36)), sides=6)
        # root toes
        for sx in (1, -1):
            for dx, ang in ((-0.09, -0.4), (0.0, 0.0), (0.09, 0.4)):
                pk.cone(bm, L, (sx * 0.23 + dx, -0.20, 0.06), (math.sin(ang) * sx * 0.6, -1, -0.15), 0.12, 0.05, BARK_D,
                        sides=6, n=4)
        # a little moss patch + mushroom on the side of the trunk
        p, n = k.surf((0.9, 0.2, 0.55), (0, 0.1, 0.55))
        pk.ellipsoid(bm, L, p, (0.14, 0.12, 0.05), LEAF, z_axis=n, useg=10, vseg=6)
    k.part("Face", face, lambda co: {"Spine": 1.0} if co.z > 0.25 else {("Leg_L" if co.x > 0 else "Leg_R"): 1.0})

    def crown(bm, L):
        balls = [((0, 0.0, 0.0), (0.56, 0.52, 0.40)), ((0.40, -0.1, -0.12), (0.30, 0.28, 0.26)),
                 ((-0.40, -0.1, -0.12), (0.30, 0.28, 0.26)), ((0.25, 0.32, -0.05), (0.30, 0.28, 0.28)),
                 ((-0.25, 0.32, -0.05), (0.30, 0.28, 0.28)), ((0.0, -0.35, -0.05), (0.32, 0.26, 0.26)),
                 ((0.0, 0.1, 0.30), (0.34, 0.32, 0.26))]
        for off, r in balls:
            c0 = CROWN + Vector(off)
            pk.ellipsoid(bm, L, c0, r, lambda u, lc: pk.mix(LEAF_D, LEAF_L, pk.smooth(-0.6, 0.9, u.z)), useg=16, vseg=10)
        for i in range(9):
            a = 2 * math.pi * i / 9
            d = Vector((math.cos(a), math.sin(a) * 0.9, 0.55)).normalized()
            p = CROWN + Vector((d.x * 0.62, d.y * 0.58, d.z * 0.48 + 0.02))
            pk.puffy_star(bm, L, pk.frame(p, (1, 0, 0), d), 0.08, PINK, depth=0.35)
    k.part("Crown", crown, "Crown")

    def arms(bm, L):
        for sx in (1, -1):
            s, n = k.surf((sx * 0.9, -0.02, 0.86), (0, -0.02, 0.86))
            pts = pk.arc_points(s - n * 0.05, (sx * 1.0, -0.1, -0.35), 0.44, bend_axis=(0, 1, 0), bend_deg=sx * -20, n=6)
            pk.tube(bm, L, pts, (0.085, 0.055), lambda t, a: pk.mix(BARK, BARK_L, t), sides=8)
            tip = pts[-1]
            d = (pts[-1] - pts[-2]).normalized()
            for ang in (-0.7, 0.0, 0.7):
                side = d.cross(Vector((0, 1, 0))).normalized()
                dd = (d + side * ang * 0.8).normalized()
                pk.ellipsoid(bm, L, tip + dd * 0.10, (0.055, 0.13, 0.025), LEAF, x_axis=dd.cross(Vector((0, 0, 1))),
                             z_axis=Vector((0, -1, 0.2)), useg=10, vseg=6)
    k.part("Arms", arms, lambda co: {"Arm_L" if co.x > 0 else "Arm_R": 1.0})

    def fruit(bm, L):
        for p in ((0.42, -0.30, -0.22), (-0.38, -0.32, -0.18), (0.05, -0.50, 0.12)):
            q = CROWN + Vector(p)
            pk.ellipsoid(bm, L, q, (0.07, 0.07, 0.08), pk.lin((255, 216, 107)), useg=10, vseg=8)
    pk.glow_part(k, "Glow_Fruit", GLOW, fruit, "Crown")


def rig(k):
    k.joint("Spine", (0, 0.0, 0.40), "Root", tail=(0, 0, 0.45))
    k.joint("Head", (0, 0.0, 0.92), "Spine", tail=(0, 0, 0.3))
    k.joint("Crown", (0, 0.04, 1.30), "Head", tail=(0, 0, 0.3))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Arm_" + side, (sx * 0.40, -0.03, 0.86), "Head", tail=(sx * 0.35, 0, -0.15))
        k.joint("Leg_" + side, (sx * 0.20, 0.0, 0.36), "Spine", tail=(0, 0, -0.3))
    k.body_bones = ["Spine", "Head", "Leg_L", "Leg_R"]


def arms(k, f, up_l, up_r, fwd_l=0.0, fwd_r=0.0):
    """up + = arm raised (rolls the +X arm up), fwd + = swung forward."""
    up_l, up_r = up_l - 40, up_r - 40       # rest = arms hanging down-out (the mesh is modelled straight out)
    k.key("Arm_L", f, rot=(0, -fwd_l, -up_l))
    k.key("Arm_R", f, rot=(0, fwd_r, up_r))


def idle(k):
    """Sways in a breeze, crown rustles; mid-cycle it lifts both arms to soak up the sun and wiggles happily."""
    n = 96
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        sway = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(1.0 * pk.wave(f, n, 0.2, 2), 0, 3.0 * sway), loc=(0, 0, 0.012 * (1 + pk.wave(f, n, 0, 4)) / 2))
        k.key("Head", f, rot=(-2 + 1.5 * pk.wave(f, n, 0.3, 2), 3 * pk.wave(f, n, 0.1), -2.0 * sway))
        k.key("Crown", f, rot=(3 * pk.wave(f, n, 0.15, 3), 4 * pk.wave(f, n, 0.4, 2), 5 * pk.wave(f, n, 0.1, 2)))
    for f, ul, ur in ((0, 0, 0), (30, 0, 0), (40, 70, 70), (46, 74, 68), (50, 68, 74), (54, 74, 68), (60, 70, 70),
                      (70, 0, 0), (96, 0, 0)):
        arms(k, f, ul, ur)
    for f in (42, 48, 54):
        k.key("Head", f, rot=(-10, 0, 6 if f != 48 else -6))
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish()
    k.meta["planted"] = cm.LEGS2


def walk(k):
    n = 24

    def body(f):
        k.key("Spine", f, rot=(2, 0, 5 * pk.wave(f, n)), loc=(0, 0, 0.035 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        k.key("Head", f, rot=(-2 + 2 * pk.wave(f, n, 0.15, 2), 4 * pk.wave(f, n, 0.1), -3 * pk.wave(f, n)))
        k.key("Crown", f, rot=(4 * pk.wave(f, n, 0.3, 2), 0, -4 * pk.wave(f, n, 0.15)))
        arms(k, f, 10, 10, 26 * pk.wave(f, n, 0.0), -26 * pk.wave(f, n, 0.0))
    return cm.biped_walk(k, n, 0.12, 0.09, body)


def roar(k):
    """Bloom burst: crouch, then arms flung wide and up, crown puffs up and shakes, settles."""
    n = 54
    k.new_action("roar", n, False)
    P = [(0, 0, 0, 0, 0), (8, 6, -0.05, -10, 0), (16, -8, 0.05, 80, 1), (34, -8, 0.05, 84, 1), (44, 2, 0, 10, 0), (54, 0, 0, 0, 0)]
    for f, sp, z, up, burst in P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Head", f, rot=(-8 * burst, 0, 0))
        k.key("Crown", f, rot=(0, 0, 0), loc=(0, 0, 0.10 * burst))
        arms(k, f, up, up, 15 * burst, 15 * burst)
    for f in range(18, 34, 3):
        w = 1 if (f // 3) % 2 else -1
        k.key("Crown", f, rot=(0, 6 * w, 8 * w), loc=(0, 0, 0.10))
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish(loop=False)


def wave(k):
    """act: waves hello with the right arm, tilting its head."""
    n = 54
    k.new_action("act_wave", n, False)
    for f, hd, roll in ((0, 0, 0), (8, -4, 8), (44, -4, 8), (54, 0, 0)):
        k.key("Spine", f, rot=(0, 0, -roll * 0.3))
        k.key("Head", f, rot=(hd, 0, roll))
        k.key("Crown", f, rot=(0, 0, roll * 0.5))
        k.key("Arm_L", f, rot=(0, 0, 40))
    for f, up, fw in ((0, 0, 0), (8, 112, 10), (14, 135, 10), (20, 100, 10), (26, 135, 10), (32, 100, 10),
                      (38, 135, 10), (44, 112, 10), (54, 0, 0)):
        k.key("Arm_R", f, rot=(0, fw, up - 40))
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    wave(k)
    return stride
