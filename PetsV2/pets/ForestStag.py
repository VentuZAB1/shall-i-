# Forest Stag (Wood egg #2): a chibi fawn-stag - huge glossy doe eyes, long soft ears, a white-spotted back, white
# puff tail, and little leafy branch antlers with glowing pink blossoms. Personality: curious and a bit shy -
# ears flick independently, sniffs the air, freezes when startled; prances; rears up proudly to 'roar'; pronks.
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Forest Stag"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.0
C = pk.lin
TOP = C((190, 116, 62))
SIDE = C((224, 158, 96))
BELLY = C((255, 238, 214))
HOOF = C((92, 62, 52))
NOSE = C((58, 38, 38))
EAR_IN = C((255, 196, 186))
BARK = C((122, 84, 56))
BARK_L = C((160, 116, 76))
LEAF = C((108, 196, 82))
LEAF_L = C((170, 232, 110))
GLOW = "ff9ad5"

HEAD = Vector((0, -0.56, 1.62))
SPOTS = [Vector((sx * x, y, 0)) for sx in (1, -1) for x, y in ((0.10, 0.02), (0.20, 0.20), (0.08, 0.32), (0.22, 0.46),
                                                                   (0.10, 0.60), (0.17, 0.74), (0.24, -0.06))]


def body_color(co, n):
    c = pk.mix(SIDE, TOP, pk.smooth(0.1, 0.8, n.z))
    c = pk.mix(c, BELLY, max(pk.smooth(-0.1, -0.6, n.z) * pk.smooth(0.55, 0.75, co.z),
                             pk.smooth(-0.3, -0.8, n.y) * pk.smooth(1.25, 0.95, co.z) * pk.smooth(0.72, 0.88, co.z)
                             * pk.smooth(0.2, -0.2, co.y)))
    # muzzle + chin lighter
    c = pk.mix(c, BELLY, pk.smooth(0.20, 0.10, (co - Vector((0, -0.98, 1.44))).length))
    # white back spots
    if n.z > 0.3 and co.z > 0.95:
        for s in SPOTS:
            d = Vector((co.x - s.x, co.y - s.y)).length
            c = pk.mix(c, BELLY, pk.smooth(0.065, 0.045, d))
    c = pk.mix(c, HOOF, pk.smooth(0.13, 0.10, co.z))
    for sx in (1, -1):
        c = pk.mix(c, pk.BLUSH, pk.smooth(0.13, 0.03, (co - Vector((sx * 0.30, -0.84, 1.42))).length) * 0.55)
    return c


def model(k):
    E = [
        ("ell", (0, 0.26, 0.98), (0.36, 0.60, 0.33)),
        ("ell", (0, -0.12, 1.02), (0.33, 0.30, 0.33)),
        ("cap", (0, -0.16, 1.12), (0, -0.44, 1.44), 0.16),
        ("ell", tuple(HEAD), (0.40, 0.37, 0.38)),
        ("ell", (0, -0.92, 1.50), (0.19, 0.17, 0.15)),
        ("ell", (0, 0.86, 1.10), (0.11, 0.09, 0.12)),
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.20, -0.12, 0.92), (sx * 0.20, -0.14, 0.12), 0.085),
              ("ell", (sx * 0.20, -0.16, 0.07), (0.095, 0.11, 0.075)),
              ("ell", (sx * 0.22, 0.56, 0.95), (0.18, 0.25, 0.27)),
              ("cap", (sx * 0.22, 0.62, 0.80), (sx * 0.22, 0.62, 0.12), 0.085),
              ("ell", (sx * 0.22, 0.60, 0.07), (0.095, 0.11, 0.075))]
    k.body(E, body_color, tris=6000)

    k.eyes([((0.62, -2.6, 1.68), (0.20, -0.7, 1.62)), ((-0.62, -2.6, 1.68), (-0.20, -0.7, 1.62))],
           size=(0.15, 0.175), style="big", iris=(176, 104, 52))

    def face(bm, L):
        p, n = k.surf((0, -2.4, 1.56), (0, -0.8, 1.50))
        pk.ellipsoid(bm, L, p + n * 0.01, (0.07, 0.045, 0.04), NOSE, z_axis=n)
        pts = []
        for x in (-0.07, -0.035, 0.0, 0.035, 0.07):
            q, qn = k.surf((x, -2.4, 1.43 + 0.02 * (abs(x) / 0.07)), (x * 0.5, -0.8, 1.45))
            pts.append(q + qn * 0.01)
        pk.tube(bm, L, pts, 0.011, NOSE, sides=6)
    k.part("Face", face, "Head")

    def ears(bm, L):
        for sx in (1, -1):
            base, n = k.surf(HEAD + Vector((sx * 0.8, 0.05, 0.25)), HEAD + Vector((sx * 0.1, 0.05, 0.1)))
            pk.ear(bm, L, base - n * 0.04, (sx * 1.0, 0.15, 0.45), (0, -1, 0.3), 0.40, 0.17, 0.055,
                   lambda h, s, f: EAR_IN if (f < -0.2 and abs(s) < 0.6 and h < 0.85) else pk.mix(SIDE, TOP, h),
                   bend=-0.04)
    k.part("Ears", ears, lambda co: {"Ear_L" if co.x > 0 else "Ear_R": 1.0})

    k.tips = []

    def antlers(bm, L):
        for sx in (1, -1):
            base, n = k.surf(HEAD + Vector((sx * 0.30, -0.05, 1.0)), HEAD + Vector((sx * 0.12, -0.05, 0.1)))
            main = pk.arc_points(base - n * 0.03, (sx * 0.35, 0.15, 1.0), 0.52, bend_axis=(0, 1, 0), bend_deg=sx * 40, n=7)
            pk.tube(bm, L, main, (0.055, 0.03), lambda t, a: pk.mix(BARK, BARK_L, t), sides=8)
            tine1 = pk.arc_points(main[3], (-sx * 0.2, -0.5, 1.0), 0.24, bend_axis=(1, 0, 0), bend_deg=20, n=5)
            pk.tube(bm, L, tine1, (0.032, 0.02), BARK_L, sides=6)
            tine2 = pk.arc_points(main[2], (sx * 0.6, 0.6, 0.7), 0.2, n=4)
            pk.tube(bm, L, tine2, (0.03, 0.02), BARK_L, sides=6)
            for tip, d in ((main[-1], (sx * 0.6, 0.0, 0.8)), (tine1[-1], (0, -0.6, 0.8)), (tine2[-1], (sx * 0.7, 0.4, 0.5))):
                k.tips.append(tip)
                for j, (ax, ang) in enumerate((((1, 0, 0), 0.0), ((0, 1, 0), 1.2), ((0, 1, 0), -1.2))):
                    dd = Vector(d).normalized()
                    side = dd.orthogonal().normalized()
                    q = tip + dd * 0.07 + side * (0.06 * math.sin(ang))
                    pk.ellipsoid(bm, L, q, (0.05, 0.10, 0.018),
                                 lambda u, lc: pk.mix(LEAF, LEAF_L, pk.smooth(-0.5, 1.0, u.y)), x_axis=side, z_axis=dd.cross(side),
                                 useg=10, vseg=6)
    k.part("Antlers", antlers, "Head")

    def blossoms(bm, L):
        for i, tip in enumerate(k.tips):
            if i % 3 == 1:
                continue
            pk.ellipsoid(bm, L, tip + Vector((0, 0, 0.04)), (0.062, 0.062, 0.062), pk.lin((255, 154, 213)), useg=8, vseg=6)
    pk.glow_part(k, "Glow_Blossoms", GLOW, blossoms, "Head")


def rig(k):
    k.joint("Spine", (0, 0.26, 0.98), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.16, 1.12), "Spine")
    k.joint("Head", (0, -0.44, 1.46), "Neck", tail=(0, -0.3, 0.1))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Ear_" + side, HEAD + Vector((sx * 0.36, 0.05, 0.12)), "Head", tail=(sx * 0.3, 0, 0.1))
        k.joint("Leg_F" + side, (sx * 0.20, -0.12, 0.92), "Spine", tail=(0, 0, -0.5))
        k.joint("Leg_B" + side, (sx * 0.22, 0.62, 0.92), "Spine", tail=(0, 0, -0.5))
    k.joint("Tail1", (0, 0.82, 1.08), "Spine", tail=(0, 0.1, 0.1))
    k.body_bones = ["Spine", "Neck", "Head", "Tail1"] + cm.LEGS4


def ear_track(k, n, events):
    """events: [(f, left_flick, right_flick)] in degrees of quick backward flick."""
    for f, l, r in events:
        k.key("Ear_L", f, rot=(0, 0, -l))
        k.key("Ear_R", f, rot=(0, 0, r))


def idle(k):
    """Curious fawn: looks left, sniffs the air, ear flicks, a startled freeze (ears up, head high), relaxes."""
    n = 96
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(0.8 * s, 0, 0), loc=(0, 0, 0.012 * (1 + s) / 2))
    track = [(0, -6, -4, 0, 0), (14, -6, -6, 22, 0), (24, -2, 6, 22, 4), (28, -4, 2, 22, -4), (32, -2, 6, 22, 4),
             (40, -6, -4, 0, 0), (56, -16, -12, -10, 0), (62, -16, -12, -10, 0), (74, -6, -4, -8, 0), (96, -6, -4, 0, 0)]
    for f, nk, hd, yaw, roll in track:
        k.key("Neck", f, rot=(nk, yaw * 0.45, 0))
        k.key("Head", f, rot=(hd, yaw * 0.55, roll))
    ear_track(k, n, [(0, 0, 0), (8, 0, 0), (10, 25, 0), (13, 0, 0), (44, 0, 0), (46, 0, 28), (49, 0, -4), (52, 0, 0),
                     (55, -12, -12), (64, -12, -12), (70, 0, 0), (84, 0, 0), (86, 22, 22), (89, 0, 0), (96, 0, 0)])
    for f, t in ((0, 0), (20, 0), (22, 18), (24, -14), (26, 10), (28, 0), (60, 0), (62, 20), (64, 0), (96, 0)):
        k.key("Tail1", f, rot=(t * 0.5, 0, 0))
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = cm.LEGS4


def walk(k):
    n = 22

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.5 * pk.wave(f, n, 0.1, 2), 2 * pk.wave(f, n, 0.1), 2.0 * pk.wave(f, n)), loc=(0, 0, 0.04 * b))
        k.key("Neck", f, rot=(-6 + 2 * pk.wave(f, n, 0.15, 2), -2 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(-4 - 2.5 * pk.wave(f, n, 0.2, 2), -2 * pk.wave(f, n, 0.1), -2 * pk.wave(f, n)))
        ear_track(k, n, [(f, 4 * pk.wave(f, n, 0.3, 2), 4 * pk.wave(f, n, 0.3, 2))])
        k.key("Tail1", f, rot=(8 * pk.wave(f, n, 0.2, 2), 0, 0))
    return cm.quad_walk(k, n, 0.86 * math.sin(math.radians(17)), 0.13, body, gait="trot")


def roar(k):
    """Proud bugle: rears up on the hind legs with the front legs tucked, chin up, ears back, then lands."""
    import bpy
    n = 60
    k.new_action("roar", n, False)
    P = [(0, 0, 0, -6, -4, 0), (10, 6, -0.04, -2, 2, 0), (22, -34, 0.10, -6, -4, 1), (40, -32, 0.10, -8, -6, 1),
         (50, 4, -0.03, -4, 0, 0), (60, 0, 0, -6, -4, 0)]
    for f, sp, z, nk, hd, up in P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        ear_track(k, n, [(f, -20 * up, -20 * up)])
        k.key("Tail1", f, rot=(20 * up, 0, 0))
    cm.plant(k, n, legs=["Leg_BL", "Leg_BR"])
    cm.plant(k, n, legs=["Leg_FL", "Leg_FR"], frames=list(range(0, 12)) + list(range(50, n + 1)))
    for f, a in ((18, -70), (26, -40), (32, -75), (38, -45), (44, -20)):   # front legs paddle in the air
        k.key("Leg_FL", f, rot=(a, 0, 0), loc=(0, 0, 0))
        k.key("Leg_FR", f, rot=(a + (20 if a < -50 else -20), 0, 0), loc=(0, 0, 0))
    k.finish(loop=False)


def pronk(k):
    """act: happy fawn pronk - two springy hops straight up with all four legs stiff, ears flopping."""
    import bpy
    n = 50
    k.new_action("act_pronk", n, False)
    hop = [(0, 0.0, 0), (6, -0.08, 0), (11, 0.42, 1), (16, 0.0, 0), (19, -0.08, 0), (24, 0.46, 1), (30, 0.0, 0),
           (34, -0.05, 0), (42, 0.0, 0), (50, 0.0, 0)]
    for f, z, air in hop:
        k.key("Spine", f, rot=(-6 * air, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(-6 - 6 * air, 0, 0))
        k.key("Head", f, rot=(-4 + 6 * air, 0, 0))
        ear_track(k, n, [(f, 25 * air, 25 * air)])
        k.key("Tail1", f, rot=(25 * air, 0, 0))
    k.bake_bezier_now()
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        if 8 <= f <= 14 or 21 <= f <= 28:
            continue
        for leg in cm.LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f in (11, 24):
        for leg in cm.LEGS4:
            k.key(leg, f, rot=(-6 if "F" in leg[4] else 6, 0, 0), loc=(0, 0, 0))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    pronk(k)
    return stride
