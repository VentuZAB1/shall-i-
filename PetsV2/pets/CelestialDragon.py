# Celestial Dragon (Celestial egg #3): an elegant chibi moon dragon - midnight-blue scales fading to periwinkle,
# a pearl-white belly, big silver-blue eyes, silver crescent-moon horns and a glowing crescent gem on its brow,
# glowing star freckles down its back, galaxy wings (deep blue -> pale cyan, silver bones, glowing stars) and a
# glowing nebula tuft on its tail. Personality: dreamy + serene - gazes up at the sky, slow graceful tail sway,
# a lazy wing stretch; breathes a little glowing star (roar); twirls happily in a full circle (act).
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Celestial Dragon"
MOTION = "Fly"
RIG = "wingquad"
HEIGHT = 7.5
C = pk.lin
TOP = C((24, 30, 92))
SIDE = C((64, 80, 178))
BELLY = C((236, 238, 255))
BELLY_D = C((196, 204, 244))
SILVER = C((222, 230, 250))
SILVER_D = C((150, 164, 210))
MEM_ROOT = C((46, 56, 160))
MEM_EDGE = C((170, 206, 255))
WBONE = C((200, 210, 240))
STAR = "c8e8ff"
NEBULA = "d6b8ff"
MOON = "fff0b0"
SPINE_CHAIN = [("Neck", -0.30), ("Spine", 0.35), ("Tail1", 1.0), ("Tail2", 1.45), ("Tail3", 1.9)]


def chain_w(co):
    y = co.y
    if y <= SPINE_CHAIN[0][1]:
        return {SPINE_CHAIN[0][0]: 1.0}
    for (a, ya), (b, yb) in zip(SPINE_CHAIN, SPINE_CHAIN[1:]):
        if y <= yb:
            t = (y - ya) / (yb - ya)
            return {a: 1 - t, b: t}
    return {SPINE_CHAIN[-1][0]: 1.0}


def body_color(co, n):
    c = pk.mix(SIDE, TOP, pk.smooth(0.0, 0.85, n.z))
    under = pk.smooth(-0.05, -0.6, n.z)
    front = pk.smooth(-0.25, -0.8, n.y) * pk.smooth(1.42, 0.7, co.z) * pk.smooth(0.5, -0.3, co.y)
    b = max(under, front * 0.95)
    if b > 0:
        stripe = 0.5 + 0.5 * math.cos((co.y - co.z * 0.7) * 2 * math.pi / 0.17)
        c = pk.mix(c, pk.mix(BELLY, BELLY_D, pk.smooth(0.72, 0.95, stripe) * 0.65), b)
    c = pk.mix(c, SILVER_D, pk.smooth(0.15, 0.03, co.z))
    for sx in (1, -1):
        c = pk.mix(c, C((190, 150, 255)), pk.smooth(0.18, 0.05, (co - Vector((sx * 0.34, -1.06, 1.6))).length) * 0.6)
    return c


def model(k):
    E = [
        ("ell", (0, 0.35, 0.82), (0.52, 0.72, 0.48)),
        ("ell", (0, -0.12, 0.92), (0.46, 0.42, 0.48)),
        ("cap", (0, -0.22, 1.12), (0, -0.52, 1.52), 0.23),
        ("ell", (0, -0.70, 1.72), (0.42, 0.40, 0.38)),
        ("ell", (0, -1.10, 1.62), (0.26, 0.30, 0.22)),
        ("cap", (0, 1.00, 0.78), (0, 1.45, 0.58), 0.19),
        ("cap", (0, 1.45, 0.58), (0, 1.90, 0.50), 0.13),
        ("cap", (0, 1.90, 0.50), (0, 2.25, 0.58), 0.09),
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.34, -0.16, 0.56), (sx * 0.36, -0.20, 0.13), 0.15),
              ("ell", (sx * 0.36, -0.27, 0.09), (0.15, 0.19, 0.09)),
              ("ell", (sx * 0.38, 0.78, 0.62), (0.24, 0.28, 0.30)),
              ("cap", (sx * 0.40, 0.80, 0.45), (sx * 0.40, 0.80, 0.13), 0.16),
              ("ell", (sx * 0.40, 0.73, 0.09), (0.16, 0.20, 0.09))]
    k.body(E, body_color, tris=5600)

    k.eyes([((0.58, -2.6, 1.86), (0.2, -0.7, 1.8)), ((-0.58, -2.6, 1.86), (-0.2, -0.7, 1.8))],
           size=(0.16, 0.18), style="big", iris=(150, 205, 255))

    def face(bm, L):
        for sx in (1, -1):
            loc, n = k.surf((sx * 0.11, -2.4, 1.70), (sx * 0.09, -1.0, 1.62))
            pk.ellipsoid(bm, L, loc - n * 0.012, (0.04, 0.028, 0.02), C((30, 30, 70)), x_axis=(1, 0, 0), z_axis=n)
        # silver crescent-moon horns
        for sx in (1, -1):
            loc, n = k.surf((sx * 0.40, -0.50, 2.6), (sx * 0.14, -0.70, 1.7))
            pts = pk.arc_points(loc - n * 0.05, (sx * 0.38, 0.80, 0.42), 0.86, bend_axis=(1, 0, 0), bend_deg=150, n=13)
            pk.tube(bm, L, pts, lambda t: 0.105 * math.sin(math.pi * min(0.18 + t * 0.82, 0.999)) ** 0.8 + 0.01,
                    lambda t, a: pk.mix(SILVER_D, SILVER, t), sides=10)
        for sx in (1, -1):   # claws
            for dx in (-0.08, 0.0, 0.08):
                pk.cone(bm, L, (sx * 0.36 + dx, -0.44, 0.06), (0, -1, -0.35), 0.08, 0.03, SILVER, sides=6, n=4)
                pk.cone(bm, L, (sx * 0.40 + dx, 0.52, 0.06), (0, -1, -0.35), 0.08, 0.03, SILVER, sides=6, n=4)

    def face_w(co):
        if co.z > 1.2:
            return {"Head": 1.0}
        return {("Leg_F" if co.y < 0.2 else "Leg_B") + ("L" if co.x > 0 else "R"): 1.0}
    k.part("Face", face, face_w)

    k.J_wing = {}
    k.wing_geo = {}
    for side, sx in (("L", 1), ("R", -1)):
        S, _ = k.surf((sx * 0.95, 0.10, 1.55), (0, 0.10, 0.95))
        S = S - Vector((sx * 0.03, 0, 0.03))
        W = S + Vector((sx * 0.72, 0.18, 0.68))
        tips = [W + Vector((sx * 0.80, 0.26, 0.32)), W + Vector((sx * 0.74, 0.72, -0.20)), W + Vector((sx * 0.30, 0.96, -0.60))]
        B = Vector((sx * 0.34, 0.92, 1.02))
        pk.membrane_wing(k, side, S, W, tips, B, "Wing_" + side, "WingTip_" + side, MEM_ROOT, MEM_EDGE, WBONE, claw=SILVER)
        k.J_wing[side] = (S, W)
        k.wing_geo[side] = (W, tips, B)

    def stars(bm, L):
        import random
        rnd = random.Random(3)
        for i in range(11):   # star freckles down the back
            t = i / 10
            y = -0.30 + 2.2 * t
            x = (0.10 + 0.08 * rnd.random()) * (1 if i % 2 else -1)
            try:
                q, qn = k.surf((x, y, 3.0), (x, y, 0.0))
            except RuntimeError:
                continue
            pk.puffy_star(bm, L, pk.frame(q + qn * 0.012, (1, 0, 0), qn), 0.055 * (1 - 0.4 * t), pk.lin((200, 232, 255)), depth=0.35)
        for side, sx in (("L", 1), ("R", -1)):   # stars scattered on the wing membranes (both faces)
            W, tips, B = k.wing_geo[side]
            rays = tips + [B]
            nrm = (tips[0] - W).cross(B - W).normalized()
            for i, a, b, sz in ((0, 0.62, 0.5, 0.06), (1, 0.45, 0.5, 0.05), (2, 0.62, 0.45, 0.055), (0, 0.32, 0.45, 0.035),
                                (2, 0.32, 0.6, 0.035), (1, 0.75, 0.35, 0.04)):
                p = W.lerp(rays[i].lerp(rays[i + 1], b), a * (1 - 0.22 * math.sin(math.pi * b)))
                for s in (1, -1):
                    pk.puffy_star(bm, L, pk.frame(p + nrm * 0.016 * s, (1, 0, 0), nrm * s), sz, pk.lin((200, 232, 255)), depth=0.15)

    def star_w(co):
        co = Vector(co)
        if abs(co.x) > 0.6:   # same blend as the membrane under it
            side = "L" if co.x > 0 else "R"
            S, W = k.J_wing[side]
            _, tips, B = k.wing_geo[side]
            reach = max((t - W).length for t in tips + [B])
            s = (co - W).length / reach
            along = (co - S).dot((W - S).normalized()) / (W - S).length
            wt = pk.smooth(-0.05, 0.25, s) * pk.smooth(0.55, 1.0, along + 0.4 * s)
            return {"WingTip_" + side: wt, "Wing_" + side: max(0.0, 1 - wt)}
        return chain_w(co)
    pk.glow_part(k, "Glow_Stars", STAR, stars, star_w)

    def nebula(bm, L):
        tip = Vector((0, 2.26, 0.58))
        # crescent-moon tail fin (thick at the middle, sharp horns up + back)
        pts = []
        for j in range(15):
            t = j / 14
            ang = math.radians(-150 + 210 * t)
            pts.append(tip + Vector((0, 0.12 + 0.30 * math.cos(ang), 0.12 + 0.32 * math.sin(ang))))
        pk.strip(bm, L, pts, lambda t: 0.03 + 0.18 * math.sin(math.pi * t) ** 1.3, (1, 0, 0), pk.lin((214, 184, 255)), thick=0.07)
        # the star-breath orb, hidden inside the head (slides out in the roar)
        pk.ellipsoid(bm, L, (0, -0.86, 1.62), (0.12, 0.16, 0.12), pk.lin((214, 184, 255)))

    def neb_w(co):
        return {"Breath": 1.0} if co.y < 0 else {"Flame": 1.0}
    pk.glow_part(k, "Glow_Nebula", NEBULA, nebula, neb_w)

    def moon(bm, L):
        # small glowing crescent on the brow, laid in the tangent plane of the forehead (horns pointing up)
        q, qn = k.surf((0, -2.4, 2.06), (0, -0.6, 1.86))
        up = (Vector((0, 0, 1)) - qn * qn.z).normalized()
        rt = qn.cross(up).normalized()
        pts = [q + qn * 0.01 + rt * (0.11 * math.sin(math.radians(-115 + 230 * j / 12)))
               - up * (0.11 * math.cos(math.radians(-115 + 230 * j / 12))) + up * 0.03 for j in range(13)]
        pk.strip(bm, L, pts, lambda t: 0.01 + 0.05 * math.sin(math.pi * t), qn, pk.lin((255, 240, 176)), thick=0.03)
    pk.glow_part(k, "Glow_Moon", MOON, moon, "Head")


def rig(k):
    k.joint("Spine", (0, 0.35, 0.85), "Root", tail=(0, -0.45, 0.2))
    k.joint("Neck", (0, -0.25, 1.12), "Spine")
    k.joint("Head", (0, -0.55, 1.55), "Neck", tail=(0, -0.35, 0.1))
    k.joint("Breath", (0, -0.86, 1.62), "Head", tail=(0, -0.25, 0))
    k.joint("Tail1", (0, 1.00, 0.78), "Spine")
    k.joint("Tail2", (0, 1.45, 0.58), "Tail1")
    k.joint("Tail3", (0, 1.90, 0.48), "Tail2")
    k.joint("Flame", (0, 2.30, 0.60), "Tail3", tail=(0, 0, 0.2))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Leg_F" + side, (sx * 0.35, -0.17, 0.50), "Spine", tail=(0, 0, -0.45))
        k.joint("Leg_B" + side, (sx * 0.40, 0.78, 0.52), "Spine", tail=(0, 0, -0.45))
        S, W = k.J_wing[side]
        k.joint("Wing_" + side, S, "Spine")
        k.joint("WingTip_" + side, W, "Wing_" + side, tail=(Vector((sx * 0.5, 0.4, 0.0))))
    k.body_bones = ["Spine", "Neck", "Head", "Tail1", "Tail2", "Tail3", "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]


TAIL = ["Tail1", "Tail2", "Tail3"]
FOLD = dict(up=-22, fwd=-34, tip_up=-30, tip_fwd=-40)


def folded(k, f, du=0.0, df=0.0):
    cm.wing_pair(k, f, FOLD["up"] + du, FOLD["fwd"] + df, FOLD["tip_up"], FOLD["tip_fwd"])


def nebula(k, f, n):
    c = max(1, round(n / 10))
    k.key("Flame", f, rot=(4 * pk.wave(f, n, 0.0, c), 5 * pk.wave(f, n, 0.3, c + 1), 6 * pk.wave(f, n, 0.6, c)))
    k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))


def flight(k):
    def extra(kk, f, ph):
        kk.key("Flame", f, rot=(6 * math.sin(2 * math.pi * ph), 4 * math.sin(2 * math.pi * (ph + 0.3)), 0))
        kk.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
    return cm.Flight(k, n=24, body_pitch=16, neck=-14, head=-10, amp=50, mid=10, sweep=14,
                     tuck={"Leg_FL": 62, "Leg_FR": 62, "Leg_BL": 78, "Leg_BR": 78}, tail=TAIL, tail_pitch=8, tail_wave=8,
                     bob=0.08, extra=extra)


def rest_keys(k):
    def f_(f):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Neck", f, rot=(-6, 0, 0))
        k.key("Head", f, rot=(-5, 0, 0))
        folded(k, f)
        for b in TAIL:
            k.key(b, f, rot=(4, 0, 0))
        k.key("Flame", f, rot=(0, 0, 0))
        k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
    return f_


def idle(k):
    """Dreamy: slow breathing, gazes up at the sky and slowly back, graceful tail S-sway, a lazy half wing-stretch."""
    n = 108
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(-1.5 - 1.0 * s, 0, 0.8 * pk.wave(f, n, 0.3)), loc=(0, 0, 0.014 * (1 + s) / 2))
        cm.chain(k, f, n, TAIL, sway=10, pitch=4, cycles=2, lag=0.12, grow=0.45)
        nebula(k, f, n)
    for f, nk, hd, yaw in ((0, -6, -5, 0), (20, -6, -5, 0), (36, -18, -20, 10), (56, -18, -22, 10), (70, -6, -5, -12),
                           (88, -6, -5, -12), (108, -6, -5, 0)):
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, 0))
    for f, du, df in ((0, 0, 0), (60, 0, 0), (70, 40, 26), (82, 40, 26), (92, 0, 0), (108, 0, 0)):
        folded(k, f, du, df)
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = cm.LEGS4


def walk(k):
    n = 26

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.2 * pk.wave(f, n, 0, 2), 2.5 * pk.wave(f, n, 0.1), 2.0 * pk.wave(f, n)), loc=(0, 0, 0.03 * b))
        k.key("Neck", f, rot=(-7 - 2 * pk.wave(f, n, 0.1, 2), -2 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(-4 - 2 * pk.wave(f, n, 0.15, 2), -2 * pk.wave(f, n, 0.1), -2 * pk.wave(f, n, 0.05)))
        folded(k, f, 3 * pk.wave(f, n, 0.1, 2))
        cm.chain(k, f, n, TAIL, sway=12, pitch=6, cycles=1, lag=0.15)
        nebula(k, f, n)
    return cm.quad_walk(k, n, 0.46 * math.sin(math.radians(20)), 0.11, body, gait="walk")


def roar(k):
    """Star breath: rears back, then breathes out a glowing little star (the hidden orb slides out of the snout)."""
    n = 50
    k.new_action("roar", n, False)
    P = [(0, 0, 0, 0, 0.0), (11, -12, -22, -16, 0.0), (18, 7, 16, 10, -0.66), (32, 5, 14, 8, -0.70), (40, 0, 0, 0, -0.1),
         (50, 0, 0, 0, 0.0)]
    for f, sp, nk, hd, br in P:
        k.key("Spine", f, rot=(sp - 2, 0, 0), loc=(0, 0, 0.02 * (sp < 0)))
        k.key("Neck", f, rot=(nk - 6, 0, 0))
        k.key("Head", f, rot=(hd - 5, 0, 0))
        k.key("Breath", f, rot=(0, 0, 0), loc=(0, br, 0.04 * (br < 0)))
        folded(k, f, 30 if 11 <= f <= 32 else 0, 10 if 11 <= f <= 32 else 0)
        for b in TAIL:
            k.key(b, f, rot=(4 - sp * 0.5, 0, 0))
    for f in range(0, n + 1, 2):
        k.key("Flame", f, rot=(4 * pk.wave(f, n, 0, 5), 0, 0))
    cm.plant(k, n)
    k.finish(loop=False)


def twirl(k):
    """act: a happy twirl - spins once on the spot with little steps, wings half open, then a graceful pose."""
    import bpy
    n = 56
    k.new_action("act_twirl", n, False)
    spin = [(0, 0), (8, 0), (16, 90), (24, 180), (32, 270), (40, 360), (48, 360), (56, 360)]
    for f, deg in spin:
        cm.key_axis(k, "Spine", f, (0, 0, 1), deg, loc=(0, 0, 0.05 if 8 < f < 40 else 0))
        folded(k, f, 26 if 8 <= f <= 40 else 0, 14 if 8 <= f <= 40 else 0)
        k.key("Neck", f, rot=(-10 if 8 <= f <= 40 else -6, 0, 0))
        k.key("Head", f, rot=(-8 if 8 <= f <= 40 else -5, 0, 0))
        for b in TAIL:
            k.key(b, f, rot=(4, -14 if 8 < f < 40 else 0, 0))
        k.key("Flame", f, rot=(0, 0, 0))
        k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in cm.LEGS4:
            if 9 <= f <= 39:
                hop = math.sin(math.pi * ((f - 9) % 6) / 6)
                k.key(leg, f, rot=(-10 * hop if "F" in leg[4] else 10 * hop, 0, 0), loc=(0, 0, 0))
            else:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fl = flight(k)
    fl.fly()
    fl.takeoff(rest_keys(k))
    fl.land(rest_keys(k))
    roar(k)
    twirl(k)
    return stride
