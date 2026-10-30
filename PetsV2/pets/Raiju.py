# Raiju (Storm egg #1): the thunder pup - a fluffy chibi fox-wolf in sunny yellow + cream with electric-blue
# lightning stripes, spiky cheek fluff, a big glowing zig-zag lightning-bolt tail, little storm-cloud puffs on its
# ankles. Personality: hyper - never still: bouncy play-bows, tail wagging like crazy, head tilts; zooms when it
# walks; howls with the bolt tail straight up (roar); chases its own tail in circles (act).
import math
from mathutils import Vector, Quaternion
import petkit as pk
import _common as cm

DISPLAY = "Raijū"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.0
C = pk.lin
FUR = C((255, 214, 72))
FUR_D = C((240, 170, 40))
CREAM = C((255, 246, 222))
STRIPE = C((48, 120, 255))
NOSE = C((50, 40, 60))
EAR_IN = C((255, 236, 200))
CLOUD = C((236, 242, 255))
CLOUD_D = C((176, 190, 230))
BOLT = "7ff6ff"
BOLT_Y = "fff27a"
HEAD = Vector((0, -0.52, 1.30))


def body_color(co, n):
    c = pk.mix(FUR, FUR_D, pk.smooth(0.3, 0.95, n.z) * 0.6)
    under = pk.smooth(-0.1, -0.6, n.z)
    chest = pk.smooth(-0.3, -0.8, n.y) * pk.smooth(1.05, 0.75, co.z) * pk.smooth(0.55, 0.7, co.z) * pk.smooth(0.2, -0.2, co.y)
    muzzle = pk.smooth(0.24, 0.12, (co - Vector((0, -0.95, 1.18))).length)
    c = pk.mix(c, CREAM, max(under * pk.smooth(0.4, 0.55, co.z), chest, muzzle))
    # lightning stripes over the back + forehead
    if n.z > 0.2:
        zig = abs(((co.y * 6.0) % 2.0) - 1.0) * 0.12
        for x0 in (0.16, -0.16):
            d = abs(co.x - x0 - (zig - 0.06) * (1 if x0 > 0 else -1))
            band = pk.smooth(0.045, 0.02, d) * pk.smooth(-0.1, 0.1, co.y) * pk.smooth(0.85, 0.55, co.y)
            c = pk.mix(c, STRIPE, band)
        fore = pk.smooth(0.05, 0.02, abs(co.x - 0.04 * math.sin(co.z * 30))) * pk.smooth(1.48, 1.6, co.z) * pk.smooth(-0.4, -0.7, co.y)
        c = pk.mix(c, STRIPE, fore)
    c = pk.mix(c, CREAM, pk.smooth(0.16, 0.06, co.z))
    for sx in (1, -1):
        c = pk.mix(c, pk.BLUSH, pk.smooth(0.12, 0.03, (co - Vector((sx * 0.30, -0.84, 1.18))).length) * 0.6)
    return c


def bolt_pts():
    # zig-zag lightning tail rising up + back from the rump
    base = Vector((0, 0.78, 0.86))
    return [base, base + Vector((0, 0.18, 0.18)), base + Vector((0, 0.08, 0.36)), base + Vector((0, 0.30, 0.52)),
            base + Vector((0, 0.18, 0.70)), base + Vector((0, 0.44, 0.92))]


def model(k):
    E = [
        ("ell", (0, 0.24, 0.82), (0.36, 0.56, 0.32)),
        ("ell", (0, -0.10, 0.86), (0.34, 0.30, 0.34)),
        ("ell", tuple(HEAD), (0.46, 0.40, 0.40)),
        ("ell", (0, -0.86, 1.18), (0.20, 0.20, 0.14)),
    ]
    for sx in (1, -1):
        E += [("ell", (sx * 0.42, -0.62, 1.16), (0.18, 0.15, 0.14)),          # spiky cheek fluff
              ("ell", (sx * 0.52, -0.56, 1.08), (0.10, 0.09, 0.09)),
              ("cap", (sx * 0.21, -0.10, 0.70), (sx * 0.22, -0.12, 0.10), 0.10),
              ("ell", (sx * 0.22, -0.15, 0.07), (0.11, 0.13, 0.075)),
              ("ell", (sx * 0.22, 0.52, 0.76), (0.18, 0.24, 0.24)),
              ("cap", (sx * 0.22, 0.56, 0.62), (sx * 0.22, 0.56, 0.10), 0.10),
              ("ell", (sx * 0.22, 0.53, 0.07), (0.11, 0.13, 0.075))]
    k.body(E, body_color, tris=5600)

    k.eyes([((0.62, -2.6, 1.38), (0.20, -0.7, 1.32)), ((-0.62, -2.6, 1.38), (-0.20, -0.7, 1.32))],
           size=(0.15, 0.17), style="big", iris=(60, 140, 255))

    def face(bm, L):
        p, n = k.surf((0, -2.4, 1.24), (0, -0.8, 1.20))
        pk.ellipsoid(bm, L, p + n * 0.01, (0.06, 0.04, 0.035), NOSE, z_axis=n)
        pts = []
        for x in (-0.08, -0.04, 0.0, 0.04, 0.08):
            q, qn = k.surf((x, -2.4, 1.10 + 0.025 * (abs(x) / 0.08)), (x * 0.5, -0.8, 1.12))
            pts.append(q + qn * 0.01)
        pk.tube(bm, L, pts, 0.012, NOSE, sides=6)
        # cloud puffs on the ankles
        for sx in (1, -1):
            for y in (-0.13, 0.55):
                for a in range(5):
                    ang = 2 * math.pi * a / 5
                    pk.ellipsoid(bm, L, (sx * 0.22 + 0.12 * math.cos(ang), y + 0.12 * math.sin(ang), 0.18), (0.075, 0.075, 0.06),
                                 lambda u, lc: pk.mix(CLOUD_D, CLOUD, pk.smooth(-0.5, 0.6, u.z)), useg=10, vseg=6)

    def face_w(co):
        if co.z > 0.5:
            return {"Head": 1.0}
        return {("Leg_F" if co.y < 0.2 else "Leg_B") + ("L" if co.x > 0 else "R"): 1.0}
    k.part("Face", face, face_w)

    def ears(bm, L):
        for sx in (1, -1):
            base, n = k.surf(HEAD + Vector((sx * 0.55, 0.05, 0.9)), HEAD + Vector((sx * 0.15, 0.05, 0.1)))
            pk.ear(bm, L, base - n * 0.05, (sx * 0.45, 0.05, 1.0), (0, -1, 0.1), 0.42, 0.19, 0.06,
                   lambda h, s, f: EAR_IN if (f < -0.2 and abs(s) < 0.6 and h < 0.8) else (STRIPE if h > 0.78 else FUR))
    k.part("Ears", ears, lambda co: {"Ear_L" if co.x > 0 else "Ear_R": 1.0})

    def bolt(bm, L, inner):
        pts = bolt_pts()
        col = pk.lin((127, 246, 255)) if not inner else pk.lin((255, 242, 122))
        pk.strip(bm, L, pts, (lambda t: 0.30 - 0.14 * t) if not inner else (lambda t: 0.13 - 0.06 * t), (1, 0, 0), col,
                 thick=0.12 if not inner else 0.15)

    def tail_w(co):
        u = (co.z - 0.86) / 0.92
        if u < 0.33:
            return {"Tail1": 1.0}
        if u < 0.66:
            return {"Tail2": 1.0}
        return {"Tail3": 1.0}
    pk.glow_part(k, "Glow_Bolt", BOLT, lambda bm, L: bolt(bm, L, False), tail_w)
    pk.glow_part(k, "Glow_BoltCore", BOLT_Y, lambda bm, L: bolt(bm, L, True), tail_w)


def rig(k):
    k.joint("Spine", (0, 0.24, 0.84), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.14, 0.94), "Spine")
    k.joint("Head", (0, -0.40, 1.16), "Neck", tail=(0, -0.3, 0.1))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Ear_" + side, HEAD + Vector((sx * 0.30, 0.05, 0.30)), "Head", tail=(sx * 0.1, 0, 0.3))
        k.joint("Leg_F" + side, (sx * 0.21, -0.10, 0.74), "Spine", tail=(0, 0, -0.5))
        k.joint("Leg_B" + side, (sx * 0.22, 0.56, 0.74), "Spine", tail=(0, 0, -0.5))
    p = bolt_pts()
    k.joint("Tail1", tuple(p[0]), "Spine", tail=p[2] - p[0])
    k.joint("Tail2", tuple(p[2]), "Tail1", tail=p[4] - p[2])
    k.joint("Tail3", tuple(p[4]), "Tail2", tail=p[5] - p[4])
    k.body_bones = ["Spine", "Neck", "Head"] + cm.LEGS4


TAIL = ["Tail1", "Tail2", "Tail3"]


def idle(k):
    """Can't keep still: tail wags fast the whole time, head tilts (curious), a bouncy play-bow mid-cycle, ear perks."""
    n = 72
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        cm.chain(k, f, n, TAIL, sway=12, pitch=0, cycles=6, lag=0.10, grow=0.3)
    P = [(0, 0, 0.0, -6, -4, 0), (12, 0, 0.0, -6, -4, 14), (20, 0, 0.0, -6, -4, -12), (28, 0, 0.0, -6, -4, 0),
         (34, 14, -0.10, -10, -8, 0), (38, 14, -0.10, -10, -8, 10), (42, 14, -0.10, -10, -8, -10), (46, 14, -0.10, -10, -8, 0),
         (52, -4, 0.06, -6, -4, 0), (58, 0, 0.0, -6, -4, 0), (72, 0, 0.0, -6, -4, 0)]
    for f, sp, z, nk, hd, tilt in P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, tilt))
    for f, a in ((0, 0), (8, 0), (10, -18), (13, 0), (60, 0), (62, -18), (64, 6), (66, 0), (72, 0)):
        cm.ears(k, f, pitch=0, twitch_r=a)
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = cm.LEGS4


def walk(k):
    n = 18

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(2 * pk.wave(f, n, 0.1, 2), 2 * pk.wave(f, n, 0.1), 3 * pk.wave(f, n)), loc=(0, 0, 0.05 * b))
        k.key("Neck", f, rot=(-4 + 2 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(-3 - 3 * pk.wave(f, n, 0.2, 2), 0, -3 * pk.wave(f, n)))
        cm.chain(k, f, n, TAIL, sway=10, pitch=-8, cycles=2, lag=0.1)
        cm.ears(k, f, pitch=-10 + 4 * pk.wave(f, n, 0.2, 2))
    return cm.quad_walk(k, n, 0.74 * math.sin(math.radians(20)), 0.14, body, gait="trot")


def roar(k):
    """Howl: sits back a little, chin to the sky, ears back, the bolt tail snaps straight up and buzzes."""
    n = 60
    k.new_action("roar", n, False)
    for f, sp, nk, hd, tp in ((0, 0, -6, -4, 0), (10, -10, -10, -10, 0.4), (18, -16, -30, -24, 1), (44, -16, -32, -26, 1),
                              (52, -4, -10, -8, 0.3), (60, 0, -6, -4, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, -0.03 * (sp < 0)))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(-20 * tp, 0, 0))
        cm.ears(k, f, pitch=20 * tp)
    for f in range(20, 44, 2):
        w = 1 if (f // 2) % 2 else -1
        k.key("Tail3", f, rot=(-20, 6 * w, 0))
        k.key("Head", f, rot=(-25, 0, 2 * w))
    cm.plant(k, n)
    k.finish(loop=False)


def chase(k):
    """act: chases its own tail - two full spins on the spot with little hopping steps, then a dizzy wobble."""
    import bpy
    n = 64
    k.new_action("act_chase", n, False)
    spin = [(0, 0), (6, 0), (12, 90), (18, 180), (24, 270), (30, 360), (36, 450), (42, 540), (48, 630), (54, 720)]
    for f, deg in spin:
        # unbounded angle -> continuous quaternion components (double cover), keys 90 deg apart interpolate cleanly
        cm.key_axis(k, "Spine", f, (0, 0, 1), deg, loc=(0, 0, 0.06 if 6 < f < 54 else 0))
    cm.key_axis(k, "Spine", n, (0, 0, 1), 720, loc=(0, 0, 0))
    for f in range(8, 54, 3):
        k.key("Head", f, rot=(-4, 30, 8))
        cm.chain(k, f, n, TAIL, sway=-14, pitch=0, cycles=2)
    for f, r in ((0, 0), (54, 0), (57, 8), (60, -6), (64, 0)):
        k.key("Head", f, rot=(-4, 0, r))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in cm.LEGS4:
            if 7 <= f <= 53:
                hop = math.sin(math.pi * ((f - 7) % 6) / 6)
                k.key(leg, f, rot=(-12 * hop if "F" in leg[4] else 12 * hop, 0, 0), loc=(0, 0, 0))
            else:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    chase(k)
    return stride
