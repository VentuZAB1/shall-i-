# Cerberus (Magma egg #3): a chibi three-headed puppy - soft charcoal fur with warm tan 'rottweiler' points, red
# spiked collars with gold studs, floppy ears, and a little tail that burns at the tip. Each head has its own
# personality: LEFT is sleepy (droopy lids, yawns), CENTER is the alert guard, RIGHT is a goofball (tongue out,
# panting, head tilts). They howl one after another (roar) and squabble with each other (act).
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Cerberus"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.5
C = pk.lin
FUR = C((62, 54, 66))
FUR_D = C((40, 34, 46))
TAN = C((236, 148, 74))
NOSE = C((26, 20, 30))
TONGUE = C((255, 120, 140))
COLLAR = C((200, 40, 50))
STUD = C((255, 206, 80))
FLAME = "ff6a2a"
FLAME_Y = "ffcf4a"
HC = Vector((0, -0.76, 1.40))
HL = Vector((0.58, -0.52, 1.13))
HR = Vector((-0.58, -0.52, 1.13))
HEADS = {"C": HC, "L": HL, "R": HR}


def body_color(co, n):
    c = pk.mix(FUR, FUR_D, pk.smooth(0.2, 0.9, n.z) * 0.6)
    # tan points: muzzles, eyebrow dots, chest, lower legs
    for h in HEADS.values():
        d = co - h
        c = pk.mix(c, TAN, pk.smooth(0.18, 0.10, (co - (h + Vector((0, -0.24, -0.08)))).length))
        for sx in (1, -1):
            c = pk.mix(c, TAN, pk.smooth(0.05, 0.025, (co - (h + Vector((sx * 0.11, -0.24, 0.17)))).length))
    c = pk.mix(c, TAN, pk.smooth(-0.3, -0.8, n.y) * pk.smooth(1.0, 0.8, co.z) * pk.smooth(0.55, 0.7, co.z) * pk.smooth(0.25, -0.1, co.y))
    c = pk.mix(c, TAN, pk.smooth(0.30, 0.18, co.z))
    return c


def model(k):
    E = [
        ("ell", (0, 0.20, 0.84), (0.44, 0.60, 0.38)),
        ("ell", (0, -0.20, 0.92), (0.46, 0.36, 0.40)),
        ("cap", (0, -0.30, 1.04), HC + Vector((0, 0.16, -0.12)), 0.17),
        ("cap", (0.20, -0.26, 1.00), HL + Vector((-0.10, 0.12, -0.10)), 0.14),
        ("cap", (-0.20, -0.26, 1.00), HR + Vector((0.10, 0.12, -0.10)), 0.14),
        ("ell", tuple(HC), (0.35, 0.32, 0.32)),
        ("ell", tuple(HC + Vector((0, -0.26, -0.08))), (0.15, 0.14, 0.11)),
        ("ell", tuple(HL), (0.29, 0.27, 0.27)),
        ("ell", tuple(HL + Vector((0.04, -0.23, -0.07))), (0.13, 0.12, 0.10)),
        ("ell", tuple(HR), (0.29, 0.27, 0.27)),
        ("ell", tuple(HR + Vector((-0.04, -0.23, -0.07))), (0.13, 0.12, 0.10)),
        ("cap", (0, 0.78, 0.94), (0, 0.98, 1.12), 0.07),
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.25, -0.16, 0.70), (sx * 0.26, -0.18, 0.10), 0.11),
              ("ell", (sx * 0.26, -0.21, 0.07), (0.12, 0.14, 0.075)),
              ("ell", (sx * 0.27, 0.54, 0.78), (0.19, 0.25, 0.26)),
              ("cap", (sx * 0.27, 0.58, 0.62), (sx * 0.27, 0.58, 0.10), 0.11),
              ("ell", (sx * 0.27, 0.55, 0.07), (0.12, 0.14, 0.075))]
    k.body(E, body_color, tris=6400)

    def eye_pts(h, spread, out):
        o = out.normalized()
        side = Vector((-o.y, o.x, 0)).normalized()
        if side.x < 0:
            side = -side
        pts = []
        for s in (1, -1):
            tgt = h + side * spread * s + Vector((0, 0, 0.05))
            pts.append((tgt + o * 2.0 + Vector((0, 0, 0.05)), tgt))
        return pts
    k.eyes(eye_pts(HC, 0.15, Vector((0, -1, 0))), size=(0.11, 0.125), style="big", iris=(255, 120, 40), name="EyesC", bone="Head")
    k.eyes(eye_pts(HL, 0.12, Vector((0.45, -1, 0))), size=(0.095, 0.11), style="sleepy", iris=(255, 120, 40), lid=FUR,
           name="EyesL", bone="Head_L")
    k.eyes(eye_pts(HR, 0.12, Vector((-0.45, -1, 0))), size=(0.095, 0.11), style="big", iris=(255, 120, 40), name="EyesR",
           bone="Head_R")

    def faces(bm, L):
        for key, h in HEADS.items():
            out = {"C": Vector((0, -1, 0)), "L": Vector((0.45, -1, 0)), "R": Vector((-0.45, -1, 0))}[key].normalized()
            m = h + Vector((0, 0, -0.06)) + out * 0.1
            p, n = k.surf(m + out * 1.5, m - out * 0.2)
            pk.ellipsoid(bm, L, p + n * 0.01, (0.055, 0.04, 0.035), NOSE, z_axis=n)
            if key == "R":   # goofy tongue out
                t, tn = k.surf(m + out * 1.5 + Vector((0, 0, -0.10)), m - out * 0.2 + Vector((0, 0, -0.10)))
                pk.ellipsoid(bm, L, t + tn * 0.02 + Vector((0.02, 0, -0.05)), (0.05, 0.035, 0.08), TONGUE, z_axis=(0, -0.4, -1))
            # floppy ears
            for sx in (1, -1):
                side = Vector((-out.y, out.x, 0)).normalized()
                if side.x < 0:
                    side = -side
                base, bn = k.surf(h + side * sx * 1.0 + Vector((0, 0.05, 0.25)), h + Vector((0, 0.05, 0.05)))
                pk.ear(bm, L, base - bn * 0.04, (side * sx * 0.9 + Vector((0, 0, 0.3))), (out + Vector((0, 0, 0.3))), 0.26, 0.15,
                       0.05, lambda hh, s, f: pk.mix(FUR_D, TAN, 0.2 if f < 0 else 0.0), bend=-0.10)
            # spiked collar
            ring_c = h + Vector((0, 0.18, -0.30)) if key == "C" else h + Vector((-0.06 if key == "L" else 0.06, 0.14, -0.30))
            ax = (h - ring_c).normalized()
            pk.torus(bm, L, ring_c, 0.17 if key == "C" else 0.155, 0.045, COLLAR, x_axis=(1, 0, 0), z_axis=ax, N=20, M=6)
            sideax = ax.orthogonal().normalized()
            from mathutils import Quaternion
            for j in range(6):
                q = Quaternion(ax, 2 * math.pi * j / 6) @ sideax
                pk.cone(bm, L, ring_c + q * 0.19, q, 0.07, 0.035, STUD, sides=6, n=3)

    def face_w(co):
        best = min(HEADS, key=lambda kk: (co - HEADS[kk] - Vector((0, 0.0, -0.15))).length)
        return {{"C": "Head", "L": "Head_L", "R": "Head_R"}[best]: 1.0}
    k.part("Faces", faces, face_w)

    def flame(bm, L, inner):
        tip = Vector((0, 1.0, 1.14))
        s = 0.55 if inner else 1.0
        pk.blob(bm, L, pk.frame(tip + Vector((0, 0.03, 0.10)), (1, 0, 0), (0, 0.4, 1)),
                lambda u: Vector((u.x * 0.10 * s * (1 - 0.5 * max(u.z, 0)), u.y * 0.10 * s * (1 - 0.5 * max(u.z, 0)),
                                  u.z * 0.18 * s + 0.05 * max(u.z, 0) ** 3)),
                pk.lin((255, 207, 74)) if inner else pk.lin((255, 106, 42)), 10, 8)
    pk.glow_part(k, "Glow_Flame", FLAME, lambda bm, L: flame(bm, L, False), "Tail1")
    pk.glow_part(k, "Glow_FlameCore", FLAME_Y, lambda bm, L: flame(bm, L, True), "Tail1")


def rig(k):
    k.joint("Spine", (0, 0.20, 0.86), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.30, 1.04), "Spine")
    k.joint("Head", HC + Vector((0, 0.10, -0.10)), "Neck", tail=(0, -0.3, 0.05))
    k.joint("Neck_L", (0.20, -0.26, 1.00), "Spine")
    k.joint("Head_L", HL + Vector((-0.04, 0.08, -0.10)), "Neck_L", tail=(0.1, -0.3, 0.05))
    k.joint("Neck_R", (-0.20, -0.26, 1.00), "Spine")
    k.joint("Head_R", HR + Vector((0.04, 0.08, -0.10)), "Neck_R", tail=(-0.1, -0.3, 0.05))
    k.joint("Tail1", (0, 0.78, 0.94), "Spine", tail=(0, 0.2, 0.18))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Leg_F" + side, (sx * 0.25, -0.16, 0.74), "Spine", tail=(0, 0, -0.5))
        k.joint("Leg_B" + side, (sx * 0.27, 0.58, 0.74), "Spine", tail=(0, 0, -0.5))
    k.body_bones = ["Spine", "Neck", "Head", "Neck_L", "Head_L", "Neck_R", "Head_R", "Tail1"] + cm.LEGS4


def heads(k, f, c=(0, 0, 0), l=(0, 0, 0), r=(0, 0, 0)):
    """(pitch, yaw, roll) per head; necks take 40%, heads 60%."""
    for (nb, hb), (p, y, rl) in ((("Neck", "Head"), c), (("Neck_L", "Head_L"), l), (("Neck_R", "Head_R"), r)):
        k.key(nb, f, rot=(p * 0.4, y * 0.4, 0))
        k.key(hb, f, rot=(p * 0.6, y * 0.6, rl))


def idle(k):
    """Three moods at once: LEFT nods off and yawns, CENTER keeps watch (looks around), RIGHT pants + tilts its head."""
    n = 96
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(0.8 * s, 0, 0), loc=(0, 0, 0.012 * (1 + s) / 2))
        k.key("Tail1", f, rot=(0, 24 * pk.wave(f, n, 0.0, 6), 0))
    left = {0: (8, 6, 6), 30: (22, 6, 10), 44: (24, 6, 12), 50: (-24, 6, 0), 58: (-26, 6, 0), 66: (6, 6, 6), 96: (8, 6, 6)}
    center = {0: (-6, 0, 0), 16: (-6, 26, 0), 32: (-6, 26, 0), 48: (-6, -24, 0), 64: (-6, -24, 0), 80: (-10, 0, 0), 96: (-6, 0, 0)}
    right = {0: (0, -8, 0), 20: (0, -8, -16), 34: (0, -8, -16), 40: (0, -8, 14), 54: (0, -8, 14), 62: (0, -8, 0), 96: (0, -8, 0)}
    def at(tr, f):
        ks = sorted(tr)
        for a, b in zip(ks, ks[1:]):
            if a <= f <= b:
                t = (f - a) / (b - a)
                t = t * t * (3 - 2 * t)
                return tuple(tr[a][i] + (tr[b][i] - tr[a][i]) * t for i in range(3))
        return tr[ks[-1]]
    for f in range(0, n + 1, 3):
        r = at(right, f)
        pant = 4 * math.sin(2 * math.pi * f / 6)          # the goofy head pants
        heads(k, f, at(center, f), at(left, f), (r[0] + pant, r[1], r[2]))
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = cm.LEGS4


def walk(k):
    n = 20

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.5 * pk.wave(f, n, 0.1, 2), 2 * pk.wave(f, n, 0.1), 3 * pk.wave(f, n)), loc=(0, 0, 0.04 * b))
        heads(k, f, (-4 + 3 * pk.wave(f, n, 0.15, 2), 0, -3 * pk.wave(f, n)), (4 + 3 * pk.wave(f, n, 0.25, 2), 8, 4),
              (-2 + 3 * pk.wave(f, n, 0.05, 2), -10, -6 * pk.wave(f, n, 0.1)))
        k.key("Tail1", f, rot=(0, 20 * pk.wave(f, n, 0, 2), 0))
    return cm.quad_walk(k, n, 0.64 * math.sin(math.radians(19)), 0.12, body, gait="trot")


def roar(k):
    """Triple howl: left, then center, then right head throws its chin up (staggered), then all together."""
    n = 66
    k.new_action("roar", n, False)
    def up(f0, f):
        return 1.0 if f0 + 4 <= f <= 50 else (0.0 if f < f0 else 0.0)
    keys = [0, 6, 10, 14, 18, 22, 26, 50, 58, 66]
    for f in keys:
        a = lambda f0: (1.0 if f0 + 4 <= f <= 50 else 0.0)
        heads(k, f, (-6 - 34 * a(8), 0, 0), (8 - 40 * a(2), 10 * a(2), 0), (0 - 36 * a(14), -10 * a(14), 0))
        k.key("Spine", f, rot=(-6 * a(2), 0, 0))
        k.key("Tail1", f, rot=(30 * a(2), 0, 0))
    cm.plant(k, n)
    k.finish(loop=False)


def squabble(k):
    """act: LEFT and RIGHT turn toward each other and nip, nip, nip - CENTER rolls its head, annoyed - then calm."""
    n = 60
    k.new_action("act_squabble", n, False)
    for f in (0, 8):
        heads(k, f, (-6, 0, 0), (8, 6, 6), (0, -8, 0))
    for i, f in enumerate(range(12, 42, 4)):
        jab = i % 2
        heads(k, f, (-10, 0, 10 if i % 4 < 2 else -10), (2 + 8 * jab, -34 - 10 * jab, 0), (2 + 8 * (1 - jab), 34 + 10 * (1 - jab), 0))
    for f in (48, 60):
        heads(k, f, (-6, 0, 0), (8, 6, 6), (0, -8, 0))
    for f in (0, 60):
        k.key("Tail1", f, rot=(0, 0, 0))
        k.key("Spine", f, rot=(0, 0, 0))
    cm.plant(k, n)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    squabble(k)
    return stride
