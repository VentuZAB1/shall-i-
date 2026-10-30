# Sea Turtle Warrior (Tide egg #2): a brave little sea turtle standing tall - determined eyes under a red bandana
# whose knot tails flutter behind, a domed teal shell with golden scutes, a cream plastron, flipper arms, and a
# golden trident with a glowing aqua gem. Personality: a tiny hero - bouncy ready stance, spins the trident, battle
# cry with the trident raised (roar), a 3-hit thrust combo (act).
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Sea Turtle Warrior"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 7.0
C = pk.lin
SKIN = C((96, 190, 150))
SKIN_L = C((150, 222, 176))
SKIN_D = C((60, 140, 110))
PLAST = C((250, 228, 150))
PLAST_D = C((214, 184, 104))
SHELL = C((40, 140, 168))
SHELL_L = C((76, 186, 200))
SCUTE = C((232, 186, 90))
BANDANA = C((232, 58, 62))
BANDANA_D = C((180, 32, 44))
GOLD = C((255, 202, 72))
SHAFT = C((60, 96, 150))
GEM = "5cf6ff"
HEAD = Vector((0, -0.06, 1.30))


def body_color(co, n):
    c = pk.mix(SKIN, SKIN_D, pk.smooth(0.3, 0.9, n.z) * 0.3)
    # sea-turtle head scales: lighter polygons
    if co.z > 1.0:
        cell = (math.sin(co.x * 23) * math.sin(co.y * 21 + 1.3) * math.sin(co.z * 25 + 0.7))
        c = pk.mix(c, SKIN_L, pk.smooth(0.15, 0.4, cell) * 0.6)
    pl = pk.smooth(-0.4, -0.8, n.y) * pk.smooth(0.24, 0.36, co.z) * pk.smooth(0.98, 0.86, co.z)
    if pl > 0:
        seg = 0.5 + 0.5 * math.cos(co.z * 2 * math.pi / 0.16)
        c = pk.mix(c, pk.mix(PLAST, PLAST_D, pk.smooth(0.85, 0.98, seg)), pl)
    for sx in (1, -1):
        c = pk.mix(c, pk.BLUSH, pk.smooth(0.11, 0.03, (co - Vector((sx * 0.30, -0.40, 1.16))).length) * 0.5)
    return c


def model(k):
    E = [
        ("ell", (0, 0.0, 0.62), (0.38, 0.34, 0.38)),
        ("cap", (0, -0.02, 0.86), (0, -0.04, 1.02), 0.20),
        ("ell", tuple(HEAD), (0.42, 0.40, 0.38)),
        ("ell", (0, -0.36, 1.18), (0.24, 0.12, 0.17)),
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.19, 0.0, 0.34), (sx * 0.21, -0.03, 0.10), 0.12),
              ("ell", (sx * 0.22, -0.12, 0.05), (0.14, 0.22, 0.055))]
    k.body(E, body_color, tris=4800)

    k.eyes([((0.56, -2.6, 1.40), (0.18, -0.3, 1.34)), ((-0.56, -2.6, 1.40), (-0.18, -0.3, 1.34))],
           size=(0.14, 0.16), style="fierce", iris=(64, 110, 210), lid=SKIN_D, lid_tilt=-14)

    def face(bm, L):
        pts = []
        for x in (-0.11, -0.05, 0.0, 0.05, 0.11):
            q, qn = k.surf((x, -2.4, 1.12 + 0.03 * (1 - (x / 0.11) ** 2) - 0.02), (x * 0.5, 0, 1.14))
            pts.append(q + qn * 0.01)
        pk.tube(bm, L, pts, 0.013, pk.lin((40, 70, 60)), sides=6)
        for sx in (1, -1):
            q, qn = k.surf((sx * 0.05, -2.4, 1.24), (sx * 0.05, 0, 1.24))
            pk.ellipsoid(bm, L, q, (0.016, 0.012, 0.012), pk.lin((40, 70, 60)), z_axis=qn)
    k.part("Face", face, "Head")

    def bandana(bm, L):
        c0 = HEAD + Vector((0, 0.0, 0.16))
        ring = []
        for i in range(41):
            a = 2 * math.pi * i / 40
            d = Vector((math.sin(a), -math.cos(a), 0.12 * math.cos(a)))
            q, qn = k.surf(c0 + d * 1.2, c0)
            ring.append(q + qn * 0.02)
        pk.strip(bm, L, ring, 0.13, lambda t: (ring[min(int(t * 40), 39)] - c0).normalized(),
                 BANDANA, thick=0.035)
        back = HEAD + Vector((0, 0.42, 0.16))
        pk.ellipsoid(bm, L, back, (0.07, 0.06, 0.06), BANDANA_D)
        for sx in (1, -1):
            pts = [back + Vector((sx * (0.03 + 0.10 * t), 0.06 + 0.20 * t, -0.34 * t - 0.04 * math.sin(t * 5)))
                   for t in [i / 6 for i in range(7)]]
            pk.strip(bm, L, pts, lambda t: 0.09 - 0.03 * t, (sx * 1.0, 0.3, 0.1), BANDANA, thick=0.03)
    k.part("Bandana", bandana, "Head")

    def shell(bm, L):
        c0 = Vector((0, 0.15, 0.66))
        fr = pk.frame(c0, (1, 0, 0), (0, 1, 0.1))
        PL = [Vector((0, 0, 1))] + [Vector((math.sin(0.8) * math.cos(a), math.sin(0.8) * math.sin(a), math.cos(0.8)))
                                    for a in [2 * math.pi * i / 6 for i in range(6)]]

        def col(u, lc):
            d = u.normalized()
            ds = sorted((d - p).length for p in PL)
            c = pk.mix(SHELL_L, SHELL, pk.smooth(0.0, 0.6, ds[0]))
            return pk.mix(SCUTE, c, pk.smooth(0.04, 0.10, ds[1] - ds[0]))
        pk.blob(bm, L, fr, lambda u: Vector((u.x * 0.48, u.y * 0.52, max(u.z, -0.1) * 0.38)), col, 40, 20)
    k.part("Shell", shell, "Spine")

    def flippers(bm, L):
        for sx in (1, -1):
            s, n = k.surf((sx * 0.9, -0.04, 0.80), (0, -0.04, 0.80))
            d = Vector((sx * 0.55, -0.1, -0.8)).normalized()
            m = pk.frame(s - n * 0.02 + d * 0.20, d.cross(Vector((0, 1, 0))).normalized(), Vector((0, -1, 0)))
            pk.blob(bm, L, m, lambda u: Vector((u.x * 0.10, u.y * 0.24 * (1 + 0.15 * u.x), u.z * 0.05)),
                    lambda u, lc: pk.mix(SKIN, SKIN_L, pk.smooth(-0.2, 0.8, u.z)), 14, 8)
            if sx < 0:   # trident in the right flipper
                hand = s + d * 0.36 + Vector((0, -0.08, 0))
                k.hand = hand
                pk.tube(bm, L, [hand + Vector((0, 0, -0.42)), hand + Vector((0, 0, 0.62))], 0.03, SHAFT, sides=8)
                top = hand + Vector((0, 0, 0.62))
                pk.tube(bm, L, [top + Vector((-0.13, 0, 0.12)), top + Vector((-0.13, 0, 0.0)), top, top + Vector((0.13, 0, 0)),
                                top + Vector((0.13, 0, 0.12))], 0.022, GOLD, sides=6)
                for dx in (-0.13, 0.0, 0.13):
                    pk.cone(bm, L, top + Vector((dx, 0, 0.10 if dx else 0.0)), (0, 0, 1), 0.2 if dx == 0 else 0.13, 0.032, GOLD,
                            sides=6, n=4)
                pk.torus(bm, L, top + Vector((0, 0, -0.05)), 0.04, 0.015, GOLD, N=12, M=6)
    k.part("Flippers", flippers, lambda co: {"Arm_L" if co.x > 0 else "Arm_R": 1.0})

    def gem(bm, L):
        top = k.hand + Vector((0, 0, 0.62))
        pk.ellipsoid(bm, L, top + Vector((0, -0.01, -0.02)), (0.045, 0.035, 0.055), pk.lin((92, 246, 255)), useg=10, vseg=8)
    pk.glow_part(k, "Glow_Gem", GEM, gem, "Arm_R")


def rig(k):
    k.joint("Spine", (0, 0.0, 0.40), "Root", tail=(0, 0, 0.45))
    k.joint("Head", (0, -0.04, 0.98), "Spine", tail=(0, 0, 0.35))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Arm_" + side, (sx * 0.34, -0.04, 0.80), "Spine", tail=(sx * 0.2, 0, -0.3))
        k.joint("Leg_" + side, (sx * 0.19, 0.0, 0.36), "Spine", tail=(0, 0, -0.3))
    k.body_bones = ["Spine", "Head", "Leg_L", "Leg_R"]


def arms(k, f, up_l, up_r, fwd_l=0.0, fwd_r=0.0, tw_r=0.0):
    k.key("Arm_L", f, rot=(0, -fwd_l, -up_l))
    k.key("Arm_R", f, rot=(tw_r, fwd_r, up_r))


def idle(k):
    """Ready stance: bouncy fighter's bob, glances left/right, taps the trident on the ground twice, nods."""
    n = 72
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        b = 0.5 - 0.5 * math.cos(2 * math.pi * f * 4 / n)
        k.key("Spine", f, rot=(4, 4 * pk.wave(f, n), 2 * pk.wave(f, n, 0.25)), loc=(0, 0, -0.03 * b))
    for f, yaw, hd in ((0, 0, -4), (14, 18, -4), (26, 18, -4), (34, -16, -4), (46, -16, -4), (54, 0, 4), (58, 0, -6), (72, 0, -4)):
        k.key("Head", f, rot=(hd, yaw, 0))
    for f, ur, fr in ((0, 10, 10), (48, 10, 10), (52, 30, 20), (55, 6, 6), (58, 30, 20), (61, 6, 6), (66, 10, 10), (72, 10, 10)):
        arms(k, f, 15, ur, 25, fr)
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish()
    k.meta["planted"] = cm.LEGS2


def walk(k):
    n = 20

    def body(f):
        k.key("Spine", f, rot=(6, 0, 6 * pk.wave(f, n)), loc=(0, 0, 0.035 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        k.key("Head", f, rot=(-5, 3 * pk.wave(f, n, 0.1), -4 * pk.wave(f, n)))
        arms(k, f, 15 + 6 * pk.wave(f, n, 0.1, 2), 10, 25 + 18 * pk.wave(f, n), 10 - 8 * pk.wave(f, n))
    return cm.biped_walk(k, n, 0.11, 0.09, body)


def roar(k):
    """Battle cry: plants its feet, throws the trident high over its head, chin up, holds, then a proud nod."""
    n = 54
    k.new_action("roar", n, False)
    for f, sp, hd, ur, ul, z in ((0, 4, -4, 10, 15, 0), (8, 10, 6, 0, 10, -0.05), (16, -8, -18, 150, 60, 0.04),
                                 (36, -8, -20, 155, 64, 0.04), (44, 4, 6, 20, 20, 0), (54, 4, -4, 10, 15, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Head", f, rot=(hd, 0, 0))
        arms(k, f, ul, ur, 25, 10)
    for f in range(18, 36, 3):
        k.key("Spine", f, rot=(-8, 0, 3 if (f // 3) % 2 else -3), loc=(0, 0, 0.04))
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish(loop=False)


def combo(k):
    """act: thrust - thrust - big spin-slash (body twists), then back to the ready stance."""
    n = 60
    k.new_action("act_combo", n, False)
    keys = [(0, 0, 10, 10, 0), (6, -14, 40, -10, 0), (10, 14, 70, 60, 0), (16, -14, 40, -10, 0), (20, 14, 70, 60, 0),
            (28, -30, 90, 0, 0), (34, 40, 90, 70, 0), (44, 0, 30, 20, 0), (60, 0, 10, 10, 0)]
    for f, yaw, ur, fr, _ in keys:
        k.key("Spine", f, rot=(6, yaw, 0))
        k.key("Head", f, rot=(-4, -yaw * 0.5, 0))
        arms(k, f, 20, ur, 25, fr)
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    combo(k)
    return stride
