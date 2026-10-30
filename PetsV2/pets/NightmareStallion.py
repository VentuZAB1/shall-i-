# Nightmare Stallion (Void egg #2): a chibi midnight pony - deep indigo coat with a starry sheen, a soft lilac
# muzzle, big glowing violet eyes, silver-lilac hooves, and a mane + tail made of living purple shadow-flame (with a
# pale core). Personality: proud and dramatic - tosses its flaming mane, stamps a hoof, snorts; rears up with a
# neigh, front legs kicking (roar); prances on the spot with high knees (act).
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Nightmare Stallion"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.0
C = pk.lin
COAT = C((48, 40, 84))
COAT_L = C((76, 64, 128))
MUZZLE = C((150, 130, 200))
HOOF = C((196, 186, 236))
NOSTRIL = C((40, 30, 70))
GLOW = "a45cff"
GLOW_W = "e8c8ff"
HEAD = Vector((0, -0.62, 1.62))


def body_color(co, n):
    c = pk.mix(COAT, COAT_L, pk.smooth(0.5, 1.0, n.z) * 0.6)
    c = pk.mix(c, MUZZLE, pk.smooth(0.26, 0.16, (co - Vector((0, -1.02, 1.46))).length))
    c = pk.mix(c, HOOF, pk.smooth(0.17, 0.12, co.z))
    for sx in (1, -1):
        c = pk.mix(c, C((200, 120, 220)), pk.smooth(0.11, 0.03, (co - Vector((sx * 0.30, -0.88, 1.50))).length) * 0.6)
    return c


def mane_pts():
    # along the top of the neck from the forelock to the withers
    return [HEAD + Vector((0, -0.16, 0.36)), HEAD + Vector((0, 0.02, 0.40)), HEAD + Vector((0, 0.20, 0.32)),
            HEAD + Vector((0, 0.34, 0.16)), Vector((0, -0.24, 1.44)), Vector((0, -0.14, 1.32)), Vector((0, -0.04, 1.20)),
            Vector((0, 0.06, 1.10))]


def model(k):
    E = [
        ("ell", (0, 0.24, 1.00), (0.38, 0.62, 0.36)),
        ("ell", (0, -0.16, 1.06), (0.36, 0.32, 0.36)),
        ("cap", (0, -0.20, 1.18), (0, -0.50, 1.50), 0.19),
        ("ell", tuple(HEAD), (0.40, 0.38, 0.40)),
        ("ell", (0, -1.00, 1.46), (0.24, 0.22, 0.19)),
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.21, -0.14, 0.94), (sx * 0.22, -0.16, 0.14), 0.10),
              ("ell", (sx * 0.22, -0.17, 0.08), (0.12, 0.13, 0.09)),
              ("ell", (sx * 0.23, 0.58, 0.98), (0.19, 0.26, 0.28)),
              ("cap", (sx * 0.23, 0.62, 0.82), (sx * 0.23, 0.62, 0.14), 0.10),
              ("ell", (sx * 0.23, 0.60, 0.08), (0.12, 0.13, 0.09))]
    k.body(E, body_color, tris=5600)

    k.eyes([((0.62, -2.6, 1.70), (0.21, -0.7, 1.64)), ((-0.62, -2.6, 1.70), (-0.21, -0.7, 1.64))],
           size=(0.17, 0.195), style="big", iris=(222, 150, 255))

    def face(bm, L):
        for sx in (1, -1):
            q, qn = k.surf((sx * 0.10, -2.4, 1.44), (sx * 0.10, -0.6, 1.44))
            pk.ellipsoid(bm, L, q + qn * 0.005, (0.035, 0.025, 0.03), NOSTRIL, z_axis=qn)
            base, n = k.surf(HEAD + Vector((sx * 0.6, 0.15, 1.0)), HEAD + Vector((sx * 0.15, 0.1, 0.1)))
            pk.ear(bm, L, base - n * 0.04, (sx * 0.35, 0.1, 1.0), (0, -1, 0.2), 0.30, 0.14, 0.05,
                   lambda h, s, f: MUZZLE if (f < -0.2 and abs(s) < 0.6 and h < 0.8) else COAT)
        pts = []
        for x in (-0.08, -0.04, 0.0, 0.04, 0.08):
            q, qn = k.surf((x, -2.4, 1.33 + 0.02 * abs(x) / 0.08), (x * 0.5, -0.6, 1.36))
            pts.append(q + qn * 0.01)
        pk.tube(bm, L, pts, 0.011, NOSTRIL, sides=6)
    k.part("Face", face, "Head")

    def flames(bm, L, inner):
        s = 0.5 if inner else 1.0
        col = pk.lin((232, 200, 255)) if inner else pk.lin((164, 92, 255))
        for i, p in enumerate(mane_pts()):
            h = (0.56 - 0.035 * i) * s
            r = (0.17 - 0.01 * i) * s
            d = Vector((0, 0.75, 0.65)).normalized()
            pk.blob(bm, L, pk.frame(p + d * h * 0.3 + (Vector((0, 0, 0.02)) if inner else Vector()), (1, 0, 0), d),
                    lambda u, h=h, r=r: Vector((u.x * r * (1 - 0.6 * max(u.z, 0)), u.y * r * 0.8 * (1 - 0.6 * max(u.z, 0)),
                                                u.z * h * 0.55 + 0.10 * h * max(u.z, 0) ** 3)), col, 10, 8)
        if not inner:   # glowing star blaze on the forehead
            q, qn = k.surf(HEAD + Vector((0, -2.0, 0.55)), HEAD + Vector((0, 0, 0.12)))
            pk.puffy_star(bm, L, pk.frame(q + qn * 0.01, (1, 0, 0), qn), 0.09, col, depth=0.3)
        # flame tail
        for j, (dy, dz, h, r) in enumerate(((0.0, 0.0, 0.62, 0.20), (0.10, -0.14, 0.58, 0.17), (0.04, 0.12, 0.52, 0.15))):
            b = Vector((0, 0.88 + dy, 1.08 + dz))
            d = Vector((0, 0.7, 0.35 - 0.3 * j)).normalized()
            pk.blob(bm, L, pk.frame(b + d * h * s * 0.4, (1, 0, 0), d),
                    lambda u, h=h * s, r=r * s: Vector((u.x * r * (1 - 0.6 * max(u.z, 0)), u.y * r * (1 - 0.6 * max(u.z, 0)),
                                                        u.z * h * 0.55 + 0.10 * h * max(u.z, 0) ** 3)), col, 10, 8)

    def flame_w(co):
        if co.y > 0.6:
            return {"Tail1": 1.0}
        if co.z > 1.55 or co.y < -0.5:
            return {"Head": 1.0}
        return {"Mane": 1.0}
    pk.glow_part(k, "Glow_Flame", GLOW, lambda bm, L: flames(bm, L, False), flame_w)
    pk.glow_part(k, "Glow_FlameCore", GLOW_W, lambda bm, L: flames(bm, L, True), flame_w)


def rig(k):
    k.joint("Spine", (0, 0.24, 1.00), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.20, 1.18), "Spine")
    k.joint("Head", (0, -0.48, 1.48), "Neck", tail=(0, -0.3, 0.05))
    k.joint("Mane", (0, -0.20, 1.30), "Neck", tail=(0, 0.2, 0.2))
    k.joint("Tail1", (0, 0.86, 1.08), "Spine", tail=(0, 0.3, 0.05))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Leg_F" + side, (sx * 0.21, -0.14, 0.96), "Spine", tail=(0, 0, -0.6))
        k.joint("Leg_B" + side, (sx * 0.23, 0.62, 0.96), "Spine", tail=(0, 0, -0.6))
    k.body_bones = ["Spine", "Neck", "Head"] + cm.LEGS4


def flick(k, f, n, amp=1.0):
    k.key("Mane", f, rot=(6 * amp * pk.wave(f, n, 0.0, 3), 0, 6 * amp * pk.wave(f, n, 0.2, 2)))
    k.key("Tail1", f, rot=(6 * amp * pk.wave(f, n, 0.3, 3), 10 * amp * pk.wave(f, n, 0.1, 2), 0))


def idle(k):
    """Dramatic: flames flicker, a big head toss (mane whips), stamps the right front hoof twice, snorts."""
    n = 90
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(0.8 * s, 0, 0), loc=(0, 0, 0.012 * (1 + s) / 2))
        flick(k, f, n)
    for f, nk, hd, roll in ((0, -6, -4, 0), (16, -6, -4, 0), (22, 10, 8, 0), (27, -20, -14, 6), (32, -8, -6, -4), (38, -6, -4, 0),
                            (66, -6, -4, 0), (70, 2, 4, 0), (74, -6, -4, 0), (90, -6, -4, 0)):
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, roll))
    k.key("Mane", 27, rot=(30, 0, 10))
    cm.plant(k, n)
    cm.drop_keys(k, "Leg_FR", 45, 63)
    for f, a, z in ((46, 0, 0.0), (49, -26, 0.12), (52, 0, 0.0), (56, -26, 0.12), (59, 0, 0.0), (62, 0, 0.0)):
        k.key("Leg_FR", f, rot=(a, 0, 0), loc=(0, 0, z))
    k.finish()
    k.meta["planted"] = ["Leg_FL", "Leg_BL", "Leg_BR"]


def walk(k):
    n = 22

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.2 * pk.wave(f, n, 0.1, 2), 1.5 * pk.wave(f, n, 0.1), 2 * pk.wave(f, n)), loc=(0, 0, 0.045 * b))
        k.key("Neck", f, rot=(-8 - 3 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(-6 + 2 * pk.wave(f, n, 0.2, 2), 0, -2 * pk.wave(f, n)))
        flick(k, f, n, 1.4)
    return cm.quad_walk(k, n, 0.82 * math.sin(math.radians(18)), 0.16, body, gait="trot")


def roar(k):
    """Rears up on the hind legs with a neigh, front legs kicking, mane + tail blazing up, lands."""
    n = 64
    k.new_action("roar", n, False)
    P = [(0, 0, 0, -6, -4, 0), (10, 6, -0.04, -2, 2, 0), (22, -38, 0.12, -14, -16, 1), (44, -36, 0.12, -16, -18, 1),
         (54, 4, -0.03, -4, 0, 0), (64, 0, 0, -6, -4, 0)]
    for f, sp, z, nk, hd, up in P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Mane", f, rot=(-20 * up, 0, 0))
        k.key("Tail1", f, rot=(25 * up, 0, 0))
    cm.plant(k, n, legs=["Leg_BL", "Leg_BR"])
    cm.plant(k, n, legs=["Leg_FL", "Leg_FR"], frames=list(range(0, 12)) + list(range(54, n + 1)))
    for f, a, b in ((18, -80, -40), (24, -40, -80), (30, -85, -45), (36, -45, -85), (42, -70, -40), (48, -20, -20)):
        k.key("Leg_FL", f, rot=(a, 0, 0), loc=(0, 0, 0))
        k.key("Leg_FR", f, rot=(b, 0, 0), loc=(0, 0, 0))
    k.finish(loop=False)


def prance(k):
    """act: proud prance on the spot - high knees, alternating diagonal pairs, head bobbing, mane flowing."""
    import bpy
    n = 48
    k.new_action("act_prance", n, False)
    for f in range(0, n + 1, 2):
        on = 1.0 if 4 <= f <= 44 else 0.0
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / 24)
        k.key("Spine", f, rot=(0, 0, 3 * on * math.sin(2 * math.pi * f / 24)), loc=(0, 0, 0.06 * b * on))
        k.key("Neck", f, rot=(-12 * on - 6 * (1 - on), 0, 0))
        k.key("Head", f, rot=(-4 + 4 * on * math.sin(4 * math.pi * f / 24), 0, 0))
        flick(k, f, n, 1.5)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg, off in (("Leg_FL", 0.0), ("Leg_BR", 0.0), ("Leg_FR", 0.5), ("Leg_BL", 0.5)):
            t = ((f / 24) + off) % 1.0
            lift = 0.0
            if 4 <= f <= 44 and t >= 0.5:
                lift = (0.30 if "F" in leg[4] else 0.16) * math.sin(math.pi * (t - 0.5) / 0.5)
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y - (0.06 if "F" in leg[4] else 0.0) * (lift > 0), lift)))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    prance(k)
    return stride
