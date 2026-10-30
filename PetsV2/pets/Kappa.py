# Kappa (Tide egg #1): a polite little water imp - teal skin, a yellow duck beak, a turtle shell on its back, a
# white dish on its head full of glowing water (ringed by a mossy hair fringe), webbed feet, and its favourite
# snack: a cucumber in one hand. Personality: careful + polite - wobbles and steadies the precious water dish,
# bows deeply (its 'roar'), munches its cucumber happily.
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Kappa"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 6.5
C = pk.lin
SKIN = C((96, 198, 162))
SKIN_D = C((64, 148, 128))
BELLY = C((242, 232, 156))
BEAK = C((255, 196, 64))
BEAK_D = C((226, 146, 40))
SHELL = C((128, 98, 58))
SHELL_L = C((176, 140, 84))
HAIR = C((46, 122, 90))
DISH = C((244, 244, 236))
CUKE = C((74, 164, 70))
CUKE_L = C((150, 214, 110))
WATER = "6fe8ff"
HEAD = Vector((0, -0.04, 1.28))


def body_color(co, n):
    c = pk.mix(SKIN, SKIN_D, pk.smooth(0.2, 0.9, n.z) * 0.35 + pk.smooth(0.1, 0.5, co.y) * 0.3)
    c = pk.mix(c, BELLY, pk.smooth(-0.4, -0.8, n.y) * pk.smooth(0.30, 0.42, co.z) * pk.smooth(0.92, 0.80, co.z))
    for sx in (1, -1):
        c = pk.mix(c, pk.BLUSH, pk.smooth(0.12, 0.03, (co - Vector((sx * 0.30, -0.38, 1.18))).length) * 0.6)
    return c


def model(k):
    E = [
        ("ell", (0, 0.0, 0.60), (0.36, 0.32, 0.36)),
        ("ell", tuple(HEAD), (0.46, 0.42, 0.42)),
        ("cap", (0, 0.0, 0.80), (0, -0.02, 1.0), 0.20),
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.17, 0.0, 0.34), (sx * 0.19, -0.02, 0.10), 0.11),
              ("ell", (sx * 0.20, -0.08, 0.05), (0.15, 0.19, 0.06))]
    k.body(E, body_color, tris=4600)

    k.eyes([((0.58, -2.6, 1.38), (0.19, -0.3, 1.34)), ((-0.58, -2.6, 1.38), (-0.19, -0.3, 1.34))],
           size=(0.14, 0.16), style="big", iris=(232, 168, 56))

    def face(bm, L):
        p, n = k.surf((0, -2.4, 1.16), (0, 0, 1.16))
        # duck beak: upper + lower
        pk.blob(bm, L, pk.frame(p + n * 0.02, (1, 0, 0), n), lambda u: Vector((u.x * 0.17, u.y * 0.07, u.z * 0.13 + 0.03)),
                lambda u, lc: pk.mix(BEAK_D, BEAK, pk.smooth(-0.6, 0.6, u.y)), 14, 8)
        pk.blob(bm, L, pk.frame(p + n * 0.01 + Vector((0, 0, -0.07)), (1, 0, 0), n),
                lambda u: Vector((u.x * 0.13, u.y * 0.04, u.z * 0.09 + 0.02)), BEAK_D, 12, 6)
        for sx in (1, -1):
            q = p + n * 0.15 + Vector((sx * 0.04, 0, 0.04))
            pk.ellipsoid(bm, L, q, (0.014, 0.01, 0.01), pk.lin((120, 70, 30)))
        # webbed toes
        for sx in (1, -1):
            for dx in (-0.08, 0.0, 0.08):
                pk.ellipsoid(bm, L, (sx * 0.20 + dx, -0.24, 0.035), (0.05, 0.07, 0.03), SKIN_D, useg=8, vseg=6)
    k.part("Face", face, lambda co: {"Head": 1.0} if co.z > 0.5 else {("Leg_L" if co.x > 0 else "Leg_R"): 1.0})

    def shell(bm, L):
        c0 = Vector((0, 0.16, 0.64))
        pk.blob(bm, L, pk.frame(c0, (1, 0, 0), (0, 1, 0.15)),
                lambda u: Vector((u.x * 0.45, u.y * 0.47, max(u.z, -0.1) * 0.36)),
                lambda u, lc: pk.mix(SHELL, SHELL_L, pk.smooth(0.2, 0.9, u.z)) if (abs(u.x) % 0.5 > 0.06 and abs(u.y) % 0.5 > 0.06)
                else SHELL, 28, 16)
        ring = [c0 + pk.frame((0, 0, 0), (1, 0, 0), (0, 1, 0.15)).to_3x3() @ Vector((math.cos(a) * 0.455, math.sin(a) * 0.475, -0.03))
                for a in [2 * math.pi * i / 40 for i in range(41)]]
        pk.tube(bm, L, ring, 0.04, SHELL_L, sides=6)
    k.part("Shell", shell, "Spine")

    def dish(bm, L):
        top, n = k.surf(HEAD + Vector((0, 0, 1.0)), HEAD)
        pk.torus(bm, L, top + Vector((0, 0, 0.02)), 0.22, 0.05, DISH, N=28, M=8)
        pk.ellipsoid(bm, L, top - Vector((0, 0, 0.01)), (0.21, 0.21, 0.03), DISH)
        for i in range(14):
            a = 2 * math.pi * i / 14
            b = top + Vector((math.cos(a) * 0.30, math.sin(a) * 0.30, -0.04))
            pk.cone(bm, L, b, (math.cos(a) * 0.5, math.sin(a) * 0.5, 0.9), 0.15, 0.06, HAIR, sides=6, n=4)
        k.dish_top = top
    k.part("Dish", dish, "Head")

    def arms(bm, L):
        for sx in (1, -1):
            s, n = k.surf((sx * 0.9, -0.02, 0.76), (0, -0.02, 0.76))
            pts = pk.arc_points(s - n * 0.03, (sx * 1.0, -0.15, -0.6), 0.34, bend_axis=(0, 1, 0), bend_deg=sx * 15, n=5)
            pk.tube(bm, L, pts, (0.075, 0.06), SKIN, sides=8)
            pk.ellipsoid(bm, L, pts[-1] + (pts[-1] - pts[-2]).normalized() * 0.05, (0.08, 0.08, 0.07), SKIN, useg=10, vseg=8)
            if sx > 0:   # the cucumber, held in the left hand
                h = pts[-1] + Vector((0.02, -0.08, 0.0))
                pk.tube(bm, L, [h + Vector((0, 0.02, -0.16)), h + Vector((0, -0.04, 0.02)), h + Vector((0, -0.06, 0.20))],
                        lambda t: 0.05 * (1 - 0.3 * abs(t - 0.5) * 2) + 0.01,
                        lambda t, a: CUKE_L if math.cos(a * 6) > 0.6 else CUKE, sides=10)
    k.part("Arms", arms, lambda co: {"Arm_L" if co.x > 0 else "Arm_R": 1.0})

    def water(bm, L):
        t = k.dish_top
        pk.ellipsoid(bm, L, t + Vector((0, 0, 0.035)), (0.19, 0.19, 0.025), pk.lin((111, 232, 255)), useg=18, vseg=6)
    pk.glow_part(k, "Glow_Water", WATER, water, "Head")


def rig(k):
    k.joint("Spine", (0, 0.0, 0.42), "Root", tail=(0, 0, 0.4))
    k.joint("Head", (0, -0.02, 0.92), "Spine", tail=(0, 0, 0.35))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Arm_" + side, (sx * 0.32, -0.03, 0.76), "Spine", tail=(sx * 0.3, 0, -0.2))
        k.joint("Leg_" + side, (sx * 0.17, 0.0, 0.36), "Spine", tail=(0, 0, -0.3))
    k.body_bones = ["Spine", "Head", "Leg_L", "Leg_R"]


def arms(k, f, up_l, up_r, fwd_l=0.0, fwd_r=0.0):
    k.key("Arm_L", f, rot=(0, -fwd_l, -up_l))
    k.key("Arm_R", f, rot=(0, fwd_r, up_r))


def idle(k):
    """Balancing the water dish: a slow wobble that gets a bit too big - both hands fly up to steady it - phew."""
    n = 96
    k.new_action("idle", n, True)
    wob = [(0, 0), (12, 3), (24, -3), (36, 5), (44, -8), (50, 9), (56, -4), (66, 0), (80, 2), (96, 0)]
    for f, r in wob:
        k.key("Spine", f, rot=(1.0, 0, r * 0.4), loc=(0, 0, 0.0))
        k.key("Head", f, rot=(-2, 0, r))
    for f in range(0, n + 1, 4):
        k.key("Spine", f, loc=(0, 0, 0.012 * (1 + pk.wave(f, n, 0, 3)) / 2))
    for f, ul, ur, fl, fr in ((0, 0, 0, 10, 0), (40, 0, 0, 10, 0), (46, 105, 105, 30, 30), (58, 110, 110, 30, 30),
                              (64, 20, 20, 15, 10), (72, 0, 0, 10, 0), (96, 0, 0, 10, 0)):
        arms(k, f, ul, ur, fl, fr)
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish()
    k.meta["planted"] = cm.LEGS2


def walk(k):
    n = 22

    def body(f):
        k.key("Spine", f, rot=(3, 0, 6 * pk.wave(f, n)), loc=(0, 0, 0.03 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        k.key("Head", f, rot=(-3, 0, -5 * pk.wave(f, n)))     # keeps the dish level
        arms(k, f, 20, 20, 10 + 18 * pk.wave(f, n), -18 * pk.wave(f, n))
    return cm.biped_walk(k, n, 0.10, 0.08, body)


def roar(k):
    """A deep, polite bow (careful! the dish tips), then it pops back up with a happy little bounce."""
    n = 56
    k.new_action("roar", n, False)
    P = [(0, 0, 0, 0, 0), (10, 4, -2, 0, 0), (22, 40, 18, 0, 1), (34, 42, 20, 0, 1), (40, -6, -6, 0.04, 0), (46, 2, 0, 0, 0),
         (56, 0, 0, 0, 0)]
    for f, sp, hd, z, bow in P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Head", f, rot=(hd, 0, 0))
        arms(k, f, 30 * bow, 30 * bow, 50 * bow, 50 * bow)
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish(loop=False)


def munch(k):
    """act: brings the cucumber to its beak and munches - crunch, crunch - a happy wiggle."""
    n = 60
    k.new_action("act_munch", n, False)
    for f, ul, fl, hd in ((0, 0, 10, 0), (10, 40, 70, 4), (40, 40, 70, 4), (50, 0, 10, -2), (60, 0, 10, 0)):
        arms(k, f, ul, 0, fl, 0)
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Spine", f, rot=(0, 0, 0))
    for f in range(12, 40, 4):
        k.key("Head", f, rot=(8 if (f // 4) % 2 else -2, 0, 0))
    for f, r in ((44, 6), (48, -6), (52, 4), (56, 0)):
        k.key("Spine", f, rot=(0, 0, r))
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    munch(k)
    return stride
