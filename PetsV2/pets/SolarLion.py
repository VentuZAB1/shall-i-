# Solar Lion (Celestial egg #1): a chibi lion cub king - warm golden fur, a cream muzzle, huge amber eyes, a glowing
# sun emblem on its forehead, and a MANE OF SUN RAYS: a fluffy orange ruff ringed by twelve glowing golden rays that
# slowly turn like a spinning sun. A tufted tail. Personality: a proud little king - chest out, chin up, the sun
# mane turning; ROARS with the rays spinning fast; shakes its mane out like a wet dog (act).
import math
from mathutils import Vector, Quaternion
import petkit as pk
import _common as cm

DISPLAY = "Solar Lion"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.0
C = pk.lin
FUR = C((246, 190, 92))
FUR_D = C((222, 150, 62))
CREAM = C((255, 240, 200))
RUFF = C((240, 120, 40))
RUFF_L = C((255, 170, 60))
NOSE = C((150, 70, 60))
RAYS = "ffd04a"
SUN = "fff2a0"
HEAD = Vector((0, -0.62, 1.30))
N_RAYS = 12


def body_color(co, n):
    c = pk.mix(FUR, FUR_D, pk.smooth(0.3, 0.95, n.z) * 0.5)
    c = pk.mix(c, CREAM, max(pk.smooth(-0.1, -0.6, n.z) * pk.smooth(0.45, 0.6, co.z),
                             pk.smooth(0.24, 0.12, (co - Vector((0, -0.98, 1.18))).length)))
    c = pk.mix(c, CREAM, pk.smooth(0.16, 0.08, co.z))
    for sx in (1, -1):
        c = pk.mix(c, C((255, 140, 120)), pk.smooth(0.12, 0.03, (co - Vector((sx * 0.30, -0.90, 1.18))).length) * 0.6)
    return c


def model(k):
    E = [
        ("ell", (0, 0.24, 0.84), (0.40, 0.62, 0.38)),
        ("ell", (0, -0.12, 0.90), (0.40, 0.34, 0.38)),
        ("ell", tuple(HEAD), (0.42, 0.38, 0.38)),
        ("ell", (0, -0.94, 1.18), (0.22, 0.18, 0.15)),
        ("cap", (0, 0.82, 0.96), (0, 1.10, 0.80), 0.06), ("cap", (0, 1.10, 0.80), (0, 1.30, 0.92), 0.05),
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.24, -0.12, 0.70), (sx * 0.25, -0.15, 0.10), 0.12),
              ("ell", (sx * 0.25, -0.19, 0.07), (0.13, 0.15, 0.075)),
              ("ell", (sx * 0.26, 0.58, 0.80), (0.20, 0.26, 0.26)),
              ("cap", (sx * 0.26, 0.60, 0.64), (sx * 0.26, 0.60, 0.10), 0.12),
              ("ell", (sx * 0.26, 0.57, 0.07), (0.13, 0.15, 0.075))]
    k.body(E, body_color, tris=5800)

    k.eyes([((0.62, -2.6, 1.40), (0.21, -0.7, 1.34)), ((-0.62, -2.6, 1.40), (-0.21, -0.7, 1.34))],
           size=(0.15, 0.17), style="big", iris=(250, 160, 40))

    def face(bm, L):
        p, n = k.surf((0, -2.4, 1.24), (0, -0.6, 1.22))
        pk.blob(bm, L, pk.frame(p + n * 0.005, (1, 0, 0), n), lambda u: Vector((u.x * 0.06, u.y * 0.04 * (1 + 0.5 * u.x * 0), u.z * 0.03)), NOSE, 10, 6)
        for sx in (1, -1):
            a, _ = k.surf((sx * 0.005, -2.4, 1.15), (sx * 0.005, -0.6, 1.15))
            b, _ = k.surf((sx * 0.06, -2.4, 1.12), (sx * 0.06, -0.6, 1.12))
            c, _ = k.surf((sx * 0.11, -2.4, 1.15), (sx * 0.11, -0.6, 1.15))
            pk.tube(bm, L, [a + Vector((0, -0.01, 0)), b + Vector((0, -0.01, 0)), c + Vector((0, -0.01, 0))], 0.012, NOSE, sides=6)
        # tail tuft
        for a in range(6):
            ang = 2 * math.pi * a / 6
            pk.ellipsoid(bm, L, (0.05 * math.cos(ang), 1.34 + 0.05 * math.sin(ang), 0.96), (0.07, 0.07, 0.08), RUFF, useg=8, vseg=6)
        # round ears peeking out of the ruff
        for sx in (1, -1):
            base, bn = k.surf(HEAD + Vector((sx * 0.7, 0.05, 0.8)), HEAD + Vector((sx * 0.15, 0.05, 0.1)))
            pk.ellipsoid(bm, L, base + bn * 0.04, (0.11, 0.05, 0.11), FUR_D, x_axis=(1, 0, 0), z_axis=(sx * 0.6, -0.3, 1))
    k.part("Face", face, lambda co: {"Head": 1.0} if co.y < 0.5 else {"Tail1": 1.0})

    def ruff(bm, L):
        # fluffy orange ruff: a ring of puffs behind the face
        for i in range(16):
            a = 2 * math.pi * i / 16
            d = Vector((math.cos(a), 0, math.sin(a)))
            p = HEAD + Vector((0, 0.10, -0.02)) + d * 0.40
            pk.ellipsoid(bm, L, p, (0.17, 0.12, 0.17), lambda u, lc: pk.mix(RUFF, RUFF_L, pk.smooth(-0.6, 0.6, u.y * -1)),
                         x_axis=(math.cos(a + math.pi / 2), 0, math.sin(a + math.pi / 2)), z_axis=(0, -1, 0), useg=10, vseg=6)
    k.part("Ruff", ruff, "Head")

    def rays(bm, L):
        c0 = HEAD + Vector((0, 0.16, -0.02))
        for i in range(N_RAYS):
            a = 2 * math.pi * i / N_RAYS
            d = Vector((math.cos(a), 0, math.sin(a)))
            side = Vector((-math.sin(a), 0, math.cos(a)))
            b = c0 + d * 0.50
            m = pk.frame(b + d * 0.12, side, Vector((0, -1, 0)))
            # a tapered ray pointing outward (the frame's y axis is the ray direction)
            pk.blob(bm, L, m, lambda u: Vector((u.x * 0.07 * (1 - 0.38 * (u.y + 1)), u.y * 0.16, u.z * 0.035)),
                    pk.lin((255, 208, 74)), 8, 6)
        # sun emblem on the forehead
        q, qn = k.surf(HEAD + Vector((0, -2.0, 0.55)), HEAD + Vector((0, 0, 0.12)))
        pk.ellipsoid(bm, L, q + qn * 0.01, (0.05, 0.05, 0.015), pk.lin((255, 242, 160)), z_axis=qn, useg=10, vseg=4)

    def ray_w(co):
        if co.y < -0.8:
            return {"Head": 1.0}
        return {"Mane": 1.0}
    pk.glow_part(k, "Glow_Rays", RAYS, rays, ray_w)


def rig(k):
    k.joint("Spine", (0, 0.24, 0.86), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.20, 0.96), "Spine")
    k.joint("Head", (0, -0.48, 1.18), "Neck", tail=(0, -0.3, 0.05))
    k.joint("Mane", HEAD + Vector((0, 0.16, -0.02)), "Head", tail=(0, 0.3, 0))
    k.joint("Tail1", (0, 0.82, 0.96), "Spine", tail=(0, 0.3, -0.16))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Leg_F" + side, (sx * 0.24, -0.12, 0.74), "Spine", tail=(0, 0, -0.5))
        k.joint("Leg_B" + side, (sx * 0.26, 0.60, 0.74), "Spine", tail=(0, 0, -0.5))
    k.body_bones = ["Spine", "Neck", "Head", "Tail1"] + cm.LEGS4


STEP = 360.0 / N_RAYS


def offset_cycles(k, bone):
    """a continuously turning channel (start != end): cycle with offset so the handles + loop stay smooth"""
    for fc in k.fcurves():
        if fc.data_path.startswith(f'pose.bones["{bone}"]'):
            for m in fc.modifiers:
                if m.type == "CYCLES":
                    m.mode_before = m.mode_after = "REPEAT_OFFSET"
            fc.update()


def mane_spin(k, f, deg):
    """spin the sun rays about the head's forward axis (continuous angle -> clean quaternion interpolation)"""
    cm.key_axis(k, "Mane", f, (0, 1, 0), deg)


def idle(k):
    """The proud king: chest out, chin up, slow look around, tail tuft flicks; the sun rays turn one ray-step per loop
    (12-fold symmetric, so the loop is seamless)."""
    n = 90
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(-1.5 - 1.0 * s, 0, 0), loc=(0, 0, 0.014 * (1 + s) / 2))
        k.key("Tail1", f, rot=(6 * pk.wave(f, n, 0.0, 2), 14 * pk.wave(f, n, 0.1, 3), 0))
        mane_spin(k, f, STEP * f / n)
    for f, yaw, hd in ((0, 0, -8), (18, 22, -8), (34, 22, -6), (50, -20, -8), (66, -20, -6), (80, 0, -10), (90, 0, -8)):
        k.key("Neck", f, rot=(hd * 0.4, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd * 0.6, yaw * 0.6, 0))
    cm.plant(k, n)
    k.finish()
    offset_cycles(k, "Mane")
    k.meta["planted"] = cm.LEGS4


def walk(k):
    n = 22

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.2 * pk.wave(f, n, 0.1, 2), 2 * pk.wave(f, n, 0.1), 3 * pk.wave(f, n)), loc=(0, 0, 0.04 * b))
        k.key("Neck", f, rot=(-2 + 2 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(-4 - 2 * pk.wave(f, n, 0.2, 2), 0, -3 * pk.wave(f, n)))
        k.key("Tail1", f, rot=(4 * pk.wave(f, n, 0.0, 2), 12 * pk.wave(f, n, 0.1), 0))
        mane_spin(k, f, STEP * f / n)
    stride = cm.quad_walk(k, n, 0.64 * math.sin(math.radians(19)), 0.12, body, gait="walk")
    offset_cycles(k, "Mane")
    return stride


def roar(k):
    """Big roar: crouch, then head thrust up-forward, the sun rays whirl fast (four ray-steps), tail lashes."""
    n = 60
    k.new_action("roar", n, False)
    for f, sp, nk, hd in ((0, 0, -3, -5), (10, 6, 8, 6), (18, -6, -14, -12), (42, -6, -16, -14), (52, 0, -3, -5), (60, 0, -3, -5)):
        k.key("Spine", f, rot=(sp, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Tail1", f, rot=(20 if 18 <= f <= 42 else 0, 0, 0))
    for f in range(0, n + 1, 3):
        u = min(1.0, max(0.0, (f - 12) / 36))
        mane_spin(k, f, STEP * 4 * (u * u * (3 - 2 * u)))
    cm.plant(k, n)
    k.finish(loop=False)


def shake(k):
    """act: shakes its mane out like a wet dog - fast head shimmy with decay, rays wobble, then a proud pose."""
    n = 48
    k.new_action("act_shake", n, False)
    for f in (0, 6, 40, 48):
        k.key("Head", f, rot=(-5, 0, 0))
        k.key("Neck", f, rot=(-3, 0, 0))
        k.key("Spine", f, rot=(0, 0, 0))
        k.key("Tail1", f, rot=(0, 0, 0))
        mane_spin(k, f, 0 if f < 20 else STEP)
    for i, f in enumerate(range(8, 39, 3)):
        w = 1 if i % 2 else -1
        d = 1 - i / 11
        k.key("Head", f, rot=(-5, 18 * w * d, 14 * w * d))
        k.key("Neck", f, rot=(-3, -8 * w * d, 0))
        k.key("Spine", f, rot=(0, 4 * w * d, -6 * w * d))
        k.key("Tail1", f, rot=(0, -16 * w * d, 0))
    cm.plant(k, n)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    shake(k)
    return stride
