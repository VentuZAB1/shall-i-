# Molten Boar (Magma egg #1): a round chibi lava piglet - charcoal-dark hide with glowing ember veins, a big
# soft pink-orange snout, little ivory tusks, floppy ears, a blazing flame mohawk (orange + yellow core) and a
# curly tail with a flame tip. Personality: a snuffly, excitable piglet - sniffs everything with a wiggly snout,
# flops its ears, digs with its nose, squeals with the mohawk flaring (roar).
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Molten Boar"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.0
C = pk.lin
HIDE = C((74, 60, 66))
HIDE_L = C((110, 88, 92))
VEIN = C((255, 112, 40))
SNOUT = C((255, 168, 140))
NOSTRIL = C((120, 50, 50))
TUSK = C((255, 248, 226))
HOOF = C((40, 32, 36))
EAR_IN = C((255, 140, 110))
FLAME = "ff8a2a"
FLAME_Y = "ffd84a"
HEAD = Vector((0, -0.60, 1.10))


def body_color(co, n):
    c = pk.mix(C((130, 58, 48)), HIDE, pk.smooth(0.0, 0.75, n.z))
    # molten glow from underneath + on the chest
    c = pk.mix(c, VEIN, pk.smooth(-0.15, -0.75, n.z) * pk.smooth(0.3, 0.5, co.z) * 0.85)
    c = pk.mix(c, HOOF, pk.smooth(0.16, 0.08, co.z))
    for sx in (1, -1):
        c = pk.mix(c, VEIN, pk.smooth(0.12, 0.03, (co - Vector((sx * 0.32, -0.92, 1.0))).length) * 0.55)
    return c


def model(k):
    E = [
        ("ell", (0, 0.20, 0.80), (0.50, 0.64, 0.46)),
        ("ell", tuple(HEAD), (0.46, 0.42, 0.42)),
        ("cap", (0, 0.82, 0.92), (0, 0.94, 0.98), 0.06),
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.27, -0.16, 0.56), (sx * 0.28, -0.18, 0.10), 0.12),
              ("ell", (sx * 0.28, -0.20, 0.07), (0.12, 0.13, 0.075)),
              ("cap", (sx * 0.27, 0.56, 0.56), (sx * 0.28, 0.56, 0.10), 0.12),
              ("ell", (sx * 0.28, 0.54, 0.07), (0.12, 0.13, 0.075))]
    k.body(E, body_color, tris=5200)

    k.eyes([((0.62, -2.6, 1.22), (0.21, -0.7, 1.16)), ((-0.62, -2.6, 1.22), (-0.21, -0.7, 1.16))],
           size=(0.15, 0.17), style="big", iris=(255, 150, 40))

    def snout(bm, L):
        p, n = k.surf((0, -2.4, 1.00), (0, -0.6, 1.00))
        pk.blob(bm, L, pk.frame(p - n * 0.06, (1, 0, 0), n), lambda u: Vector((u.x * 0.19, u.y * 0.15, u.z * 0.11 + 0.04)), SNOUT, 16, 10)
        for sx in (1, -1):
            pk.ellipsoid(bm, L, p + n * 0.092 + Vector((sx * 0.07, 0, 0.0)), (0.035, 0.05, 0.02), NOSTRIL, z_axis=n)
    k.part("Snout", snout, "Snout")

    def face(bm, L):
        for sx in (1, -1):
            q, qn = k.surf((sx * 0.20, -2.4, 0.88), (sx * 0.16, -0.6, 0.92))
            pk.cone(bm, L, q - qn * 0.02, (sx * 0.4, -0.6, 0.8), 0.16, 0.04, TUSK, bend_axis=(0, 1, 0), bend_deg=sx * 25, sides=8, n=5)
        pts = []
        for x in (-0.07, -0.035, 0.0, 0.035, 0.07):
            q, qn = k.surf((x, -2.4, 0.84 + 0.02 * abs(x) / 0.07), (x * 0.5, -0.6, 0.88))
            pts.append(q + qn * 0.01)
        pk.tube(bm, L, pts, 0.012, NOSTRIL, sides=6)
    k.part("Face", face, "Head")

    def ears(bm, L):
        for sx in (1, -1):
            base, n = k.surf(HEAD + Vector((sx * 0.8, 0.05, 0.5)), HEAD + Vector((sx * 0.1, 0.05, 0.1)))
            pk.ear(bm, L, base - n * 0.04, (sx * 0.9, -0.3, 0.4), (0, -0.7, 0.7), 0.30, 0.17, 0.05,
                   lambda h, s, f: EAR_IN if (f < -0.2 and abs(s) < 0.6 and h < 0.85) else HIDE_L, bend=0.08)
    k.part("Ears", ears, lambda co: {"Ear_L" if co.x > 0 else "Ear_R": 1.0})

    k.mohawk = []

    def flames(bm, L, inner):
        for i in range(6):
            t = i / 5
            p = HEAD + Vector((0, -0.18 + 0.62 * t, 0.42 - 0.10 * t))
            try:
                q, qn = k.surf(p + Vector((0, 0, 1.0)), p - Vector((0, 0, 0.6)))
            except RuntimeError:
                continue
            h = (0.34 - 0.12 * t) * (0.55 if inner else 1.0)
            r = (0.11 - 0.03 * t) * (0.55 if inner else 1.0)
            d = (qn + Vector((0, 0.55, 0.2))).normalized()
            base = q - qn * 0.03 + (qn * 0.03 if inner else Vector())
            pk.blob(bm, L, pk.frame(base + d * h * 0.35, (1, 0, 0), d),
                    lambda u, h=h, r=r: Vector((u.x * r * (1 - 0.6 * max(u.z, 0)), u.y * r * 0.7 * (1 - 0.6 * max(u.z, 0)),
                                                u.z * h * 0.55 + 0.08 * h * max(u.z, 0) ** 3)),
                    pk.lin((255, 216, 74)) if inner else pk.lin((255, 138, 42)), 10, 8)
        # tail flame
        tip = Vector((0, 0.98, 1.02))
        s = 0.55 if inner else 1.0
        pk.blob(bm, L, pk.frame(tip + Vector((0, 0.03, 0.08)), (1, 0, 0), (0, 0.4, 1)),
                lambda u: Vector((u.x * 0.08 * s, u.y * 0.08 * s, u.z * 0.14 * s)),
                pk.lin((255, 216, 74)) if inner else pk.lin((255, 138, 42)), 10, 8)

        if not inner:   # glowing lava cracks on both flanks
            for sx in (1, -1):
                for (y0, z0) in ((-0.02, 0.98), (0.38, 0.86)):
                    pts = []
                    for j, dz in enumerate((0.0, -0.05, -0.04, -0.12, -0.13, -0.2)):
                        y = y0 + 0.06 * j
                        z = z0 + dz
                        try:
                            q, qn = k.surf((sx * 1.2, y, z), (0, y, z))
                        except RuntimeError:
                            continue
                        pts.append(q + qn * 0.01)
                    if len(pts) > 2:
                        pk.strip(bm, L, pts, lambda t: 0.04 * (1 - t) + 0.012, (sx, 0, 0), pk.lin((255, 138, 42)), thick=0.02)

    def flame_w(co):
        if abs(co.x) > 0.3:
            return {"Spine": 1.0}
        return {"Tail1": 1.0} if co.y > 0.8 else {"Mohawk": 1.0}
    pk.glow_part(k, "Glow_Flame", FLAME, lambda bm, L: flames(bm, L, False), flame_w)
    pk.glow_part(k, "Glow_FlameCore", FLAME_Y, lambda bm, L: flames(bm, L, True), flame_w)


def rig(k):
    k.joint("Spine", (0, 0.20, 0.80), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.26, 0.92), "Spine")
    k.joint("Head", (0, -0.48, 1.04), "Neck", tail=(0, -0.3, 0.05))
    k.joint("Snout", (0, -0.86, 1.00), "Head", tail=(0, -0.2, 0))
    k.joint("Mohawk", HEAD + Vector((0, 0.05, 0.36)), "Head", tail=(0, 0, 0.25))
    k.joint("Tail1", (0, 0.82, 0.92), "Spine", tail=(0, 0.15, 0.1))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Ear_" + side, HEAD + Vector((sx * 0.36, 0.05, 0.30)), "Head", tail=(sx * 0.2, 0, 0.1))
        k.joint("Leg_F" + side, (sx * 0.27, -0.16, 0.60), "Spine", tail=(0, 0, -0.45))
        k.joint("Leg_B" + side, (sx * 0.27, 0.56, 0.60), "Spine", tail=(0, 0, -0.45))
    k.body_bones = ["Spine", "Neck", "Head", "Tail1"] + cm.LEGS4


def sniff(k, f, amt):
    k.key("Snout", f, rot=(-6 * amt, 0, 0), loc=(0, -0.025 * amt, 0.01 * amt))


def flop(k, f, l, r):
    k.key("Ear_L", f, rot=(l, 0, -l * 0.5))
    k.key("Ear_R", f, rot=(r, 0, r * 0.5))


def idle(k):
    """Snuffly: snout wiggles in quick sniff bursts, looks left/right at smells, ears flop, curly tail wags."""
    n = 80
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(0.8 * s, 0, 1.2 * pk.wave(f, n, 0.2)), loc=(0, 0, 0.012 * (1 + s) / 2))
        k.key("Tail1", f, rot=(0, 26 * pk.wave(f, n, 0.0, 8), 0))
        k.key("Mohawk", f, rot=(4 * pk.wave(f, n, 0.1, 4), 0, 5 * pk.wave(f, n, 0.3, 3)))
    for f, yaw, hd in ((0, 0, 4), (16, 26, 8), (30, 26, 8), (40, -24, 6), (56, -24, 6), (66, 0, 10), (80, 0, 4)):
        k.key("Neck", f, rot=(hd * 0.5, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd * 0.5, yaw * 0.6, 0))
    vals = [(0, 0)]
    for burst in (18, 46, 68):
        vals += [(burst, 0), (burst + 2, 1), (burst + 4, 0), (burst + 6, 1), (burst + 8, 0)]
    vals.append((80, 0))
    for f, a in vals:
        sniff(k, f, a)
    for f, l, r in ((0, 0, 0), (14, 0, 0), (18, 20, 0), (22, 0, 0), (40, 0, 0), (44, 0, 22), (48, 0, 0), (80, 0, 0)):
        flop(k, f, l, r)
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = cm.LEGS4


def walk(k):
    n = 18

    def body(f):
        k.key("Spine", f, rot=(1.5 * pk.wave(f, n, 0.1, 2), 2 * pk.wave(f, n, 0.1), 4 * pk.wave(f, n)),
              loc=(0, 0, 0.04 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        k.key("Neck", f, rot=(2 + 2 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(2 - 3 * pk.wave(f, n, 0.2, 2), 0, -3 * pk.wave(f, n)))
        k.key("Tail1", f, rot=(0, 18 * pk.wave(f, n, 0.0, 2), 0))
        k.key("Mohawk", f, rot=(6 * pk.wave(f, n, 0.3, 2), 0, 0))
        flop(k, f, 10 * pk.wave(f, n, 0.2, 2), 10 * pk.wave(f, n, 0.2, 2))
        sniff(k, f, 0)
    return cm.quad_walk(k, n, 0.50 * math.sin(math.radians(20)), 0.11, body, gait="trot")


def roar(k):
    """Squeal: rears the head up, snout scrunched, ears back, mohawk flares tall, little hop on the front legs."""
    n = 50
    k.new_action("roar", n, False)
    for f, sp, z, nk, hd, flare in ((0, 0, 0, 2, 2, 0), (8, 4, -0.03, 6, 6, 0), (14, -10, 0.05, -18, -16, 1), (34, -10, 0.05, -18, -16, 1),
                                    (42, 2, 0, 2, 2, 0.2), (50, 0, 0, 2, 2, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Mohawk", f, rot=(-10 * flare, 0, 0), loc=(0, 0, 0.10 * flare))
        sniff(k, f, flare)
        flop(k, f, 30 * flare, 30 * flare)
        k.key("Tail1", f, rot=(30 * flare, 0, 0))
    for f in range(16, 34, 2):
        w = 1 if (f // 2) % 2 else -1
        k.key("Mohawk", f, rot=(-10, 0, 8 * w), loc=(0, 0, 0.10))
    cm.plant(k, n)
    k.finish(loop=False)


def dig(k):
    """act: roots in the ground - head down, snout shoves forward 3 times, a happy snort + ear flop."""
    n = 60
    k.new_action("act_dig", n, False)
    for f, sp, nk, hd in ((0, 0, 2, 2), (10, 6, 22, 18), (40, 6, 22, 18), (48, -2, -6, -6), (60, 0, 2, 2)):
        k.key("Spine", f, rot=(sp, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Tail1", f, rot=(0, 0, 0))
        k.key("Mohawk", f, rot=(0, 0, 0))
        sniff(k, f, 0)
    for i, f in enumerate(range(12, 40, 4)):
        push = i % 2
        k.key("Head", f, rot=(18 + 10 * push, 0, 4 * (1 if i % 4 < 2 else -1)))
        sniff(k, f, push)
    for f in (49, 52, 55):
        flop(k, f, 20 if f != 52 else 0, 20 if f != 52 else 0)
    flop(k, 0, 0, 0)
    flop(k, 60, 0, 0)
    for f in range(0, n + 1, 3):
        k.key("Tail1", f, rot=(0, 24 * pk.wave(f, n, 0, 6), 0))
    cm.plant(k, n)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    dig(k)
    return stride
