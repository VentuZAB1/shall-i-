# Shade Panther (Void egg #1): a chibi shadow-panther cub - inky indigo fur with a violet sheen, glowing purple
# rosette spots, huge glowing violet eyes, lavender inner ears, and a long tail that ends in a wisp of purple
# shadow-flame. Personality: sneaky + mysterious - prowls low, tail tip twitching, sharpens its claws on the ground,
# arches its back and hisses like a Halloween cat (roar), leaps forward in a big pounce (act).
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Shade Panther"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 6.5
C = pk.lin
FUR = C((44, 38, 70))
SHEEN = C((92, 70, 150))
BELLY = C((70, 60, 104))
EAR_IN = C((190, 150, 255))
NOSE = C((150, 110, 220))
GLOW = "b77bff"
GLOW_W = "e6ccff"
HEAD = Vector((0, -0.56, 1.10))
TAILP = [Vector((0, 0.80, 0.80)), Vector((0, 1.12, 0.96)), Vector((0, 1.30, 1.22)), Vector((0, 1.26, 1.50))]


def body_color(co, n):
    c = pk.mix(FUR, SHEEN, pk.smooth(0.55, 1.0, n.z) * 0.5)
    c = pk.mix(c, BELLY, pk.smooth(-0.2, -0.7, n.z))
    c = pk.mix(c, BELLY, pk.smooth(0.20, 0.10, (co - Vector((0, -0.92, 1.0))).length))
    for sx in (1, -1):
        c = pk.mix(c, C((150, 90, 200)), pk.smooth(0.11, 0.03, (co - Vector((sx * 0.30, -0.86, 1.00))).length) * 0.6)
    return c


def model(k):
    E = [
        ("ell", (0, 0.24, 0.72), (0.38, 0.62, 0.34)),
        ("ell", (0, -0.14, 0.78), (0.36, 0.30, 0.34)),
        ("ell", tuple(HEAD), (0.46, 0.40, 0.40)),
        ("ell", (0, -0.88, 1.00), (0.20, 0.15, 0.14)),
        ("cap", TAILP[0], TAILP[1], 0.10), ("cap", TAILP[1], TAILP[2], 0.09), ("cap", TAILP[2], TAILP[3], 0.08),
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.22, -0.14, 0.60), (sx * 0.23, -0.17, 0.10), 0.115),
              ("ell", (sx * 0.23, -0.22, 0.07), (0.13, 0.15, 0.075)),
              ("ell", (sx * 0.24, 0.60, 0.68), (0.20, 0.26, 0.26)),
              ("cap", (sx * 0.24, 0.62, 0.54), (sx * 0.24, 0.60, 0.10), 0.11),
              ("ell", (sx * 0.24, 0.57, 0.07), (0.13, 0.15, 0.075))]
    k.body(E, body_color, tris=5600)

    k.eyes([((0.62, -2.6, 1.18), (0.21, -0.7, 1.12)), ((-0.62, -2.6, 1.18), (-0.21, -0.7, 1.12))],
           size=(0.16, 0.18), style="big", iris=(176, 100, 255), pupil="slit")

    def face(bm, L):
        p, n = k.surf((0, -2.4, 1.06), (0, -0.6, 1.02))
        pk.ellipsoid(bm, L, p + n * 0.005, (0.05, 0.035, 0.03), NOSE, z_axis=n)
        for sx in (1, -1):
            a, _ = k.surf((sx * 0.005, -2.4, 0.97), (sx * 0.005, -0.6, 0.97))
            b, _ = k.surf((sx * 0.06, -2.4, 0.94), (sx * 0.06, -0.6, 0.94))
            c, _ = k.surf((sx * 0.11, -2.4, 0.97), (sx * 0.11, -0.6, 0.97))
            pk.tube(bm, L, [a + Vector((0, -0.01, 0)), b + Vector((0, -0.01, 0)), c + Vector((0, -0.01, 0))], 0.01,
                    C((20, 14, 34)), sides=6)
            root, rn = k.surf((sx * 0.16, -2.4, 1.0), (sx * 0.16, -0.6, 1.0))
            for dz in (0.03, -0.02):
                pk.cone(bm, L, root + rn * 0.01 + Vector((0, 0, dz)), (sx * 1.0, -0.15, dz * 4), 0.28, 0.009, C((210, 190, 255)),
                        bend_axis=(0, 1, 0), bend_deg=sx * 10, sides=5, n=5)
    k.part("Face", face, "Head")

    def ears(bm, L):
        for sx in (1, -1):
            base, n = k.surf(HEAD + Vector((sx * 0.7, 0.05, 0.9)), HEAD + Vector((sx * 0.15, 0.05, 0.1)))
            pk.ear(bm, L, base - n * 0.05, (sx * 0.5, 0.05, 1.0), (0, -1, 0.15), 0.34, 0.20, 0.06,
                   lambda h, s, f: EAR_IN if (f < -0.2 and abs(s) < 0.6 and h < 0.8) else FUR)
    k.part("Ears", ears, lambda co: {"Ear_L" if co.x > 0 else "Ear_R": 1.0})

    def glow(bm, L):
        # rosette spots on the back/flanks
        import random
        rnd = random.Random(5)
        for i in range(16):
            y = -0.1 + 0.85 * rnd.random()
            sx = 1 if i % 2 else -1
            a = math.radians(rnd.uniform(20, 75))
            q0 = Vector((sx * math.sin(a) * 2, y, 0.72 + math.cos(a) * 2))
            try:
                q, qn = k.surf(q0, Vector((0, y, 0.72)))
            except RuntimeError:
                continue
            for j in range(4):
                ang = 2 * math.pi * j / 4 + 0.4
                side = qn.orthogonal().normalized()
                from mathutils import Quaternion
                d = Quaternion(qn, ang) @ side
                pk.ellipsoid(bm, L, q + qn * 0.004 + d * 0.045, (0.022, 0.022, 0.008), pk.lin((183, 123, 255)), z_axis=qn,
                             useg=6, vseg=4)
        # glowing crescent moon on the forehead
        pts = []
        for j in range(9):
            t = j / 8
            ang = math.radians(-70 + 140 * t)
            q0 = HEAD + Vector((0.13 * math.sin(ang), -0.2, 0.22 + 0.13 * math.cos(ang) - 0.06))
            try:
                q, qn = k.surf(q0 + Vector((0, -2.0, 0.5)), q0 + Vector((0, 0.4, -0.1)))
            except RuntimeError:
                continue
            pts.append(q + qn * 0.012)
        if len(pts) > 2:
            pk.strip(bm, L, pts, lambda t: 0.012 + 0.05 * math.sin(math.pi * t), (0, -1, 0.3), pk.lin((183, 123, 255)), thick=0.02)
        # shadow-flame wisp at the tail tip
        tip = TAILP[3]
        pk.blob(bm, L, pk.frame(tip + Vector((0, -0.02, 0.10)), (1, 0, 0), (0, -0.2, 1)),
                lambda u: Vector((u.x * 0.11 * (1 - 0.5 * max(u.z, 0)), u.y * 0.11 * (1 - 0.5 * max(u.z, 0)),
                                  u.z * 0.20 + 0.06 * max(u.z, 0) ** 3)), pk.lin((183, 123, 255)), 10, 8)

    def glow_w(co):
        if co.y > 1.1 and co.z > 1.3:
            return {"Tail3": 1.0}
        if co.z > 1.15 and co.y < -0.5:
            return {"Head": 1.0}
        return {"Spine": 1.0}
    pk.glow_part(k, "Glow_Spots", GLOW, glow, glow_w)

    def core(bm, L):
        tip = TAILP[3]
        pk.ellipsoid(bm, L, tip + Vector((0, -0.02, 0.08)), (0.055, 0.055, 0.10), pk.lin((230, 204, 255)), useg=8, vseg=6)
    pk.glow_part(k, "Glow_Wisp", GLOW_W, core, "Tail3")


def rig(k):
    k.joint("Spine", (0, 0.24, 0.74), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.20, 0.84), "Spine")
    k.joint("Head", (0, -0.44, 1.00), "Neck", tail=(0, -0.3, 0.05))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Ear_" + side, HEAD + Vector((sx * 0.30, 0.05, 0.30)), "Head", tail=(sx * 0.1, 0, 0.3))
        k.joint("Leg_F" + side, (sx * 0.22, -0.14, 0.64), "Spine", tail=(0, 0, -0.45))
        k.joint("Leg_B" + side, (sx * 0.24, 0.62, 0.64), "Spine", tail=(0, 0, -0.45))
    k.joint("Tail1", tuple(TAILP[0]), "Spine")
    k.joint("Tail2", tuple(TAILP[1]), "Tail1")
    k.joint("Tail3", tuple(TAILP[2]), "Tail2", tail=TAILP[3] - TAILP[2])
    k.body_bones = ["Spine", "Neck", "Head", "Tail1", "Tail2", "Tail3"] + cm.LEGS4


TAIL = ["Tail1", "Tail2", "Tail3"]


def idle(k):
    """Prowling crouch: low body, head low and watchful, scanning; the tail sways in a slow S with a twitching tip;
    ears swivel; mid-cycle it rises a little, then sinks back."""
    n = 96
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        low = 0.5 + 0.5 * pk.cwave(f, n)
        k.key("Spine", f, rot=(2 * low, 0, 1.2 * pk.wave(f, n, 0.3)), loc=(0, 0, -0.08 * low + 0.01 * s))
        cm.chain(k, f, n, TAIL, sway=12, pitch=6, cycles=2, lag=0.14, grow=0.4)
        if f % 6 == 0:
            k.key("Tail3", f, rot=(6 + 10 * (1 if (f // 6) % 2 else -1) * low, 18 * pk.wave(f, n, 0.0, 2), 0))
    for f, yaw, hd in ((0, 0, 4), (16, 30, 4), (30, 30, 4), (46, -28, 4), (62, -28, 4), (76, 0, -4), (96, 0, 4)):
        k.key("Neck", f, rot=(hd * 0.5, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd * 0.5, yaw * 0.6, 0))
    for f, l, r in ((0, 0, 0), (12, 0, 0), (16, -20, 10), (22, 0, 0), (40, 0, 0), (46, 10, -22), (52, 0, 0), (96, 0, 0)):
        k.key("Ear_L", f, rot=(0, -l, 0))
        k.key("Ear_R", f, rot=(0, -r, 0))
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = cm.LEGS4


def walk(k):
    """Slinky stalk: lateral-sequence walk, shoulders roll, head level and low, tail flowing behind."""
    n = 26

    def body(f):
        k.key("Spine", f, rot=(1 * pk.wave(f, n, 0.1, 2), 3 * pk.wave(f, n, 0.1), 4 * pk.wave(f, n)),
              loc=(0, 0, -0.03 + 0.02 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        k.key("Neck", f, rot=(6, -3 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(2, -2 * pk.wave(f, n, 0.1), -2 * pk.wave(f, n)))
        cm.chain(k, f, n, TAIL, sway=14, pitch=-4, cycles=1, lag=0.15)
    return cm.quad_walk(k, n, 0.56 * math.sin(math.radians(20)), 0.10, body, gait="walk")


def roar(k):
    """Halloween-cat hiss: back arches high, fur up, tail straight up and puffed, head low with ears flat."""
    n = 56
    k.new_action("roar", n, False)
    for f, z, nk, hd, ear, tail in ((0, 0, 2, 2, 0, 0), (8, 0.02, 6, 4, -10, 0.3), (16, 0.16, 18, 4, -45, 1), (40, 0.16, 18, 4, -45, 1),
                                   (48, 0.02, 4, 2, -10, 0.3), (56, 0, 2, 2, 0, 0)):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Ear_L", f, rot=(0, 0, -ear * 0.6))
        k.key("Ear_R", f, rot=(0, 0, ear * 0.6))
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(18 * tail + (8 if i == 0 else 0) * tail, 0, 0))
    for f in range(18, 40, 2):
        w = 1 if (f // 2) % 2 else -1
        k.key("Tail3", f, rot=(18, 5 * w, 0))
    cm.plant(k, n)
    k.finish(loop=False)


def pounce(k):
    """act: butt wiggle, then a big leap forward-up (legs stretched), lands and looks proud."""
    import bpy
    n = 54
    k.new_action("act_pounce", n, False)
    keys = [(0, 0, 0, 0.0, 2, 2), (8, 4, 0, -0.10, 2, -2), (20, 4, 0, -0.10, 2, -2), (26, -18, -0.12, 0.40, -10, -8),
            (31, 8, -0.16, 0.34, 4, 0), (35, 10, -0.04, -0.06, 6, 4), (44, -2, 0, 0.0, 2, 2), (54, 0, 0, 0.0, 2, 2)]
    for f, sp, y, z, nk, hd in keys:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, y, z))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
    for f in range(8, 21, 2):
        w = 1 if (f // 2) % 2 else -1
        k.key("Spine", f, rot=(4, 3 * w, 5 * w), loc=(0, 0, -0.10))
        k.key("Tail1", f, rot=(0, 12 * w, 0))
    for f in (0, 6, 22, 30, 40, 54):
        cm.chain(k, f, n, TAIL, sway=0, pitch=-8 if 22 <= f <= 30 else 4)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        if 23 <= f <= 33:
            continue
        for leg in cm.LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f, fa, ba in ((27, -55, 45), (30, -40, 50)):
        for leg in cm.LEGS4:
            k.key(leg, f, rot=(fa if "F" in leg[4] else ba, 0, 0), loc=(0, 0, 0))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    pounce(k)
    return stride
