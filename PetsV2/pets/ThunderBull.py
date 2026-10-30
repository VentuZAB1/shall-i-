# Thunder Bull (Storm egg #2): a stubby, stubborn little storm calf - slate-blue with yellow lightning flashes on
# its flanks, a soft pale muzzle with a golden nose ring, golden horns with glowing tips, and its own tiny storm
# cloud (with a glowing bolt) sitting on its head. Personality: grumpy-cute tough guy - scrapes the ground, snorts
# and shakes its head; lowers its horns and stomps (roar); bucks with both back legs (act).
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Thunder Bull"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.0
C = pk.lin
TOP = C((66, 84, 140))
SIDE = C((92, 116, 176))
BELLY = C((168, 186, 228))
MUZZLE = C((232, 210, 222))
NOSTRIL = C((120, 80, 100))
HOOF = C((52, 48, 70))
FLASH = C((255, 220, 70))
HORN = C((255, 210, 90))
HORN_D = C((222, 160, 50))
CLOUD = C((236, 240, 252))
CLOUD_D = C((160, 170, 200))
GLOW = "ffe94a"
HEAD = Vector((0, -0.74, 1.28))


def body_color(co, n):
    c = pk.mix(SIDE, TOP, pk.smooth(0.2, 0.9, n.z))
    c = pk.mix(c, BELLY, pk.smooth(-0.1, -0.6, n.z) * pk.smooth(0.35, 0.5, co.z))
    # lightning flash on each flank
    if abs(n.x) > 0.5 and 0.55 < co.z < 1.15 and -0.1 < co.y < 0.75:
        t = (co.y + 0.1) / 0.85
        zig = 0.82 + 0.12 * (1 if int(t * 4) % 2 == 0 else -1) * ((t * 4) % 1.0 - 0.5) * 2 - 0.25 * t
        c = pk.mix(c, FLASH, pk.smooth(0.07, 0.035, abs(co.z - zig)))
    c = pk.mix(c, MUZZLE, pk.smooth(0.34, 0.22, (co - Vector((0, -1.20, 1.08))).length))
    c = pk.mix(c, HOOF, pk.smooth(0.14, 0.10, co.z))
    return c


def model(k):
    E = [
        ("ell", (0, 0.26, 0.86), (0.48, 0.66, 0.44)),
        ("ell", (0, -0.20, 0.90), (0.46, 0.38, 0.44)),
        ("ell", tuple(HEAD), (0.52, 0.45, 0.45)),
        ("ell", (0, -1.14, 1.10), (0.32, 0.24, 0.22)),          # big soft muzzle
        ("cap", (0, 0.90, 0.98), (0, 1.10, 0.70), 0.06),          # tail
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.28, -0.20, 0.70), (sx * 0.29, -0.22, 0.12), 0.14),
              ("ell", (sx * 0.29, -0.24, 0.08), (0.15, 0.16, 0.08)),
              ("ell", (sx * 0.30, 0.62, 0.80), (0.24, 0.30, 0.32)),
              ("cap", (sx * 0.30, 0.66, 0.64), (sx * 0.30, 0.66, 0.12), 0.14),
              ("ell", (sx * 0.30, 0.64, 0.08), (0.15, 0.16, 0.08)),
              ("ell", (sx * 0.52, -0.66, 1.36), (0.18, 0.09, 0.10))]   # floppy ears (in the body)
    k.body(E, body_color, tris=5600)

    k.eyes([((0.66, -2.6, 1.42), (0.24, -0.7, 1.36)), ((-0.66, -2.6, 1.42), (-0.24, -0.7, 1.36))],
           size=(0.15, 0.17), style="big", iris=(255, 196, 60))

    def face(bm, L):
        for sx in (1, -1):   # grumpy little brows
            a, an = k.surf((sx * 0.14, -2.4, 1.62), (sx * 0.12, -0.6, 1.58))
            b, bn = k.surf((sx * 0.38, -2.4, 1.66), (sx * 0.30, -0.6, 1.62))
            pk.tube(bm, L, [a + an * 0.03, (a + b) / 2 + an * 0.035, b + bn * 0.03], (0.03, 0.022), pk.lin((40, 50, 90)), sides=6)
        for sx in (1, -1):
            q, qn = k.surf((sx * 0.11, -2.4, 1.14), (sx * 0.11, -0.8, 1.12))
            pk.ellipsoid(bm, L, q + qn * 0.005, (0.04, 0.03, 0.025), NOSTRIL, z_axis=qn)
        q, qn = k.surf((0, -2.4, 0.98), (0, -0.8, 1.02))
        pk.torus(bm, L, q + Vector((0, -0.04, -0.03)), 0.08, 0.018, pk.lin((255, 206, 70)), x_axis=(1, 0, 0),
                 z_axis=(0, 1, 0), N=16, M=6)
        # tail tuft = a little cloud
        for a in range(5):
            ang = 2 * math.pi * a / 5
            pk.ellipsoid(bm, L, (0.06 * math.cos(ang), 1.12 + 0.06 * math.sin(ang), 0.66), (0.07, 0.07, 0.07), CLOUD, useg=8, vseg=6)
    k.part("Face", face, lambda co: {"Head": 1.0} if co.y < -0.3 else {"Tail1": 1.0})

    k.horn_tips = []

    def horns(bm, L):
        for sx in (1, -1):
            base, n = k.surf(HEAD + Vector((sx * 0.9, 0.05, 0.3)), HEAD + Vector((sx * 0.1, 0.05, 0.15)))
            pts = pk.arc_points(base - n * 0.04, (sx * 1.0, -0.1, 0.2), 0.50, bend_axis=(0, 1, 0), bend_deg=sx * -80, n=9)
            pk.tube(bm, L, pts, lambda t: 0.11 * (1 - t) ** 0.8 + 0.014, lambda t, a: pk.mix(HORN_D, HORN, t), sides=10)
            k.horn_tips.append(pts[-1])
    k.part("Horns", horns, "Head")

    def cloud(bm, L):
        top, n = k.surf(HEAD + Vector((0, 0.05, 1.2)), HEAD)
        c0 = top + Vector((0, 0.02, 0.10))
        k.cloud = c0
        for off, r in (((0, 0, 0.04), 0.17), ((0.15, 0.02, 0.0), 0.13), ((-0.15, 0.02, 0.0), 0.13), ((0.07, -0.08, -0.02), 0.11),
                       ((-0.06, 0.10, 0.02), 0.12)):
            pk.ellipsoid(bm, L, c0 + Vector(off), (r, r * 0.9, r * 0.8),
                         lambda u, lc: pk.mix(CLOUD_D, CLOUD, pk.smooth(-0.6, 0.5, u.z)), useg=12, vseg=8)
    k.part("Cloud", cloud, "Cloud")

    def glow(bm, L):
        c0 = k.cloud
        pts = [c0 + Vector((0.02, -0.02, -0.10)), c0 + Vector((-0.05, -0.04, -0.20)), c0 + Vector((0.04, -0.05, -0.24)),
               c0 + Vector((-0.03, -0.06, -0.36))]
        pk.strip(bm, L, pts, lambda t: 0.08 - 0.05 * t, (0, -1, 0), pk.lin((255, 233, 74)), thick=0.04)
        for tip in k.horn_tips:
            pk.ellipsoid(bm, L, tip, (0.035, 0.035, 0.035), pk.lin((255, 233, 74)), useg=8, vseg=6)
    pk.glow_part(k, "Glow_Bolt", GLOW, glow, lambda co: {"Cloud": 1.0} if abs(co.x) < 0.12 else {"Head": 1.0})


def rig(k):
    k.joint("Spine", (0, 0.26, 0.88), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.30, 0.98), "Spine")
    k.joint("Head", (0, -0.56, 1.10), "Neck", tail=(0, -0.3, 0.05))
    k.joint("Cloud", HEAD + Vector((0, 0.05, 0.40)), "Head", tail=(0, 0, 0.2))
    k.joint("Tail1", (0, 0.90, 0.98), "Spine", tail=(0, 0.2, -0.3))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Leg_F" + side, (sx * 0.28, -0.20, 0.72), "Spine", tail=(0, 0, -0.5))
        k.joint("Leg_B" + side, (sx * 0.30, 0.66, 0.72), "Spine", tail=(0, 0, -0.5))
    k.body_bones = ["Spine", "Neck", "Head", "Tail1"] + cm.LEGS4


def cloud(k, f, n, amp=1.0):
    k.key("Cloud", f, rot=(4 * amp * pk.wave(f, n, 0.2, 2), 0, 5 * amp * pk.wave(f, n, 0.0, 2)),
          loc=(0, 0, 0.025 * amp * (1 + pk.wave(f, n, 0.1, 2)) / 2))


def idle(k):
    """Grumpy guard: tail swish, scrapes the ground twice with the right front hoof, snorts with a head shake."""
    import bpy
    n = 90
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(0.8 * s, 0, 0), loc=(0, 0, 0.012 * (1 + s) / 2))
        k.key("Tail1", f, rot=(0, 20 * pk.wave(f, n, 0.0, 3), 0))
        cloud(k, f, n)
    for f, nk, hd, roll in ((0, 2, 2, 0), (20, 6, 6, 0), (40, 6, 6, 0), (52, -2, -6, 0), (55, -2, -6, 12), (58, -2, -6, -12),
                            (61, -2, -6, 10), (64, -2, -6, -6), (70, 2, 2, 0), (90, 2, 2, 0)):
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, roll))
    cm.plant(k, n)
    # scrape: right front hoof drags back twice (f 22-46)
    cm.drop_keys(k, "Leg_FR", 21, 47)
    for f, a, z in ((22, 0, 0.0), (26, -18, 0.10), (31, 24, 0.0), (35, -18, 0.10), (40, 24, 0.0), (46, 0, 0.0)):
        k.key("Leg_FR", f, rot=(a, 0, 0), loc=(0, 0, z))
    k.finish()
    k.meta["planted"] = ["Leg_FL", "Leg_BL", "Leg_BR"]


def walk(k):
    n = 26

    def body(f):
        k.key("Spine", f, rot=(1.0 * pk.wave(f, n, 0.1, 2), 2 * pk.wave(f, n, 0.1), 3.5 * pk.wave(f, n)),
              loc=(0, 0, 0.03 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        k.key("Neck", f, rot=(4 + 3 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(3 - 2 * pk.wave(f, n, 0.2, 2), 3 * pk.wave(f, n, 0.1), -3 * pk.wave(f, n)))
        k.key("Tail1", f, rot=(0, 14 * pk.wave(f, n, 0.2), 0))
        cloud(k, f, n, 1.5)
    return cm.quad_walk(k, n, 0.60 * math.sin(math.radians(17)), 0.11, body, gait="walk")


def roar(k):
    """Horns down + double stomp, then a big head toss to the sky."""
    import bpy
    n = 60
    k.new_action("roar", n, False)
    for f, sp, nk, hd in ((0, 0, 2, 2), (8, 8, 18, 14), (30, 8, 18, 14), (38, -8, -20, -22), (48, -8, -22, -24), (60, 0, 2, 2)):
        k.key("Spine", f, rot=(sp, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Tail1", f, rot=(30 if 8 <= f <= 48 else 0, 0, 0))
        k.key("Cloud", f, rot=(0, 0, 0), loc=(0, 0, 0.12 if 38 <= f <= 48 else 0.0))
    for f in range(40, 48, 2):
        k.key("Cloud", f, rot=(0, 0, 10 if (f // 2) % 2 else -10), loc=(0, 0, 0.12))
    cm.plant(k, n)
    for leg, f0 in (("Leg_FL", 10), ("Leg_FR", 20)):
        cm.drop_keys(k, leg, f0 + 1, f0 + 7)
        k.key(leg, f0 + 3, rot=(-22, 0, 0), loc=(0, 0, 0.14))
    k.finish(loop=False)


def buck(k):
    """act: two bucks - the front stays planted, the rump kicks up, back legs fly out behind."""
    import bpy
    n = 50
    k.new_action("act_buck", n, False)
    for f, sp, z, kick in ((0, 0, 0, 0), (6, -6, 0.02, 0), (12, 22, 0.10, 1), (18, -4, 0.0, 0), (24, 22, 0.10, 1),
                           (32, -2, 0.0, 0), (40, 0, 0, 0), (50, 0, 0, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(-sp * 0.6, 0, 0))
        k.key("Head", f, rot=(-sp * 0.3, 0, 0))
        k.key("Tail1", f, rot=(40 * kick, 0, 0))
        cloud(k, f, n, 2)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in ("Leg_FL", "Leg_FR"):
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
        for leg in ("Leg_BL", "Leg_BR"):
            if 9 <= f <= 15 or 21 <= f <= 27:
                continue
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f in (12, 24):
        for leg in ("Leg_BL", "Leg_BR"):
            k.key(leg, f, rot=(55, 0, 0), loc=(0, 0, 0))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    buck(k)
    return stride
