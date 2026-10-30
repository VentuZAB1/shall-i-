# Storm Wyvern (Storm egg #3): a chibi electric wyvern - its wings ARE its arms. Royal violet-blue scales, a pale
# yellow belly, a glowing cyan lightning crest down its head + neck, swept-back bolt horns, electric-blue wing
# membranes with cyan edges, and a lightning-bolt tail spade. Stands upright on two strong legs.
# Personality: a showy little thunder lizard - puffs its chest, flicks its wings, shakes off static (act);
# screeches with wings flung wide (roar); flies with big strong strokes, legs tucked back, body level.
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Storm Wyvern"
MOTION = "Fly"
RIG = "wingbiped"
HEIGHT = 7.0
C = pk.lin
TOP = C((80, 64, 196))
SIDE = C((128, 104, 236))
BELLY = C((255, 238, 160))
BELLY_D = C((236, 206, 110))
CLAW = C((250, 246, 230))
MEM_ROOT = C((70, 120, 250))
MEM_EDGE = C((150, 236, 255))
WBONE = C((56, 40, 140))
GLOW = "5ce8ff"
HEAD = Vector((0, -0.26, 1.58))
TAILP = [Vector((0, 0.40, 0.70)), Vector((0, 0.82, 0.46)), Vector((0, 1.18, 0.33)), Vector((0, 1.46, 0.30))]


def body_color(co, n):
    c = pk.mix(SIDE, TOP, pk.smooth(0.0, 0.85, n.z) * 0.7 + pk.smooth(-0.2, 0.6, n.y) * 0.3)
    belly = pk.smooth(-0.3, -0.75, n.y) * pk.smooth(0.25, 0.4, co.z) * pk.smooth(1.32, 1.18, co.z) * pk.smooth(0.3, 0.15, abs(co.x))
    if belly > 0:
        seg = 0.5 + 0.5 * math.cos(co.z * 2 * math.pi / 0.14)
        c = pk.mix(c, pk.mix(BELLY, BELLY_D, pk.smooth(0.8, 0.97, seg)), belly)
    c = pk.mix(c, BELLY, pk.smooth(0.22, 0.12, (co - Vector((0, -0.66, 1.42))).length))
    for sx in (1, -1):
        c = pk.mix(c, pk.BLUSH, pk.smooth(0.11, 0.03, (co - Vector((sx * 0.28, -0.52, 1.44))).length) * 0.5)
    return c


def model(k):
    E = [
        ("ell", (0, 0.10, 0.86), (0.38, 0.40, 0.46)),
        ("cap", (0, -0.04, 1.10), (0, -0.16, 1.36), 0.22),
        ("ell", tuple(HEAD), (0.48, 0.43, 0.41)),
        ("ell", (0, -0.64, 1.48), (0.23, 0.21, 0.17)),
        ("cap", TAILP[0], TAILP[1], 0.17), ("cap", TAILP[1], TAILP[2], 0.12), ("cap", TAILP[2], TAILP[3], 0.08),
    ]
    for sx in (1, -1):
        E += [("ell", (sx * 0.26, 0.15, 0.58), (0.18, 0.22, 0.24)),
              ("cap", (sx * 0.26, 0.14, 0.46), (sx * 0.27, 0.10, 0.11), 0.10),
              ("ell", (sx * 0.27, 0.02, 0.06), (0.12, 0.20, 0.065))]
    k.body(E, body_color, tris=5200)

    k.eyes([((0.62, -2.6, 1.70), (0.21, -0.5, 1.64)), ((-0.62, -2.6, 1.70), (-0.21, -0.5, 1.64))],
           size=(0.16, 0.18), style="big", iris=(255, 226, 70))

    def face(bm, L):
        for sx in (1, -1):   # cocky angled brows
            a, an = k.surf((sx * 0.10, -2.4, 1.90), (sx * 0.08, -0.4, 1.86))
            b, bn = k.surf((sx * 0.34, -2.4, 1.95), (sx * 0.26, -0.4, 1.90))
            pk.tube(bm, L, [a + an * 0.03, (a + b) / 2 + an * 0.035, b + bn * 0.03], (0.03, 0.02), pk.lin((40, 26, 110)), sides=6)
        for sx in (1, -1):
            q, qn = k.surf((sx * 0.09, -2.4, 1.52), (sx * 0.08, -0.6, 1.50))
            pk.ellipsoid(bm, L, q + qn * 0.005, (0.03, 0.02, 0.02), pk.lin((40, 30, 90)), z_axis=qn)
            q, qn = k.surf((sx * 0.12, -2.4, 1.38), (sx * 0.10, -0.6, 1.40))
            pk.cone(bm, L, q + Vector((0, 0.01, 0.02)), (0, -0.3, -1), 0.09, 0.03, CLAW)
            for dx in (-0.07, 0.0, 0.07):
                pk.cone(bm, L, (sx * 0.27 + dx, -0.16, 0.05), (0, -1, -0.3), 0.08, 0.03, CLAW, sides=6, n=4)
    k.part("Face", face, lambda co: {"Head": 1.0} if co.z > 1.0 else {("Leg_L" if co.x > 0 else "Leg_R"): 1.0})

    def horns(bm, L):
        for sx in (1, -1):
            base, n = k.surf(HEAD + Vector((sx * 0.4, 0.1, 0.9)), HEAD + Vector((sx * 0.15, 0.1, 0.1)))
            pts = [base - n * 0.03, base + Vector((sx * 0.06, 0.12, 0.10)), base + Vector((sx * 0.02, 0.22, 0.16)),
                   base + Vector((sx * 0.08, 0.36, 0.26))]
            pk.strip(bm, L, pts, lambda t: 0.10 * (1 - t) + 0.02, (sx, 0, 0.3), pk.lin((235, 250, 255)), thick=0.05)
    k.part("Horns", horns, "Head")

    k.crest = []

    def crest(bm, L):
        for i in range(9):
            t = i / 8
            p = HEAD + Vector((0, 0.05 + 0.55 * t, 0.36 - 0.70 * t))
            try:
                q, qn = k.surf(p + Vector((0, 0.4, 0.8)), p - Vector((0, 0.2, 0.4)))
            except RuntimeError:
                continue
            h = 0.16 * (1 - 0.6 * t)
            d = (qn + Vector((0, 0.8, 0))).normalized()
            pts = [q - qn * 0.02, q + d * h * 0.55 + Vector((0, -0.04, 0)), q + d * h]
            pk.strip(bm, L, pts, lambda tt: 0.08 * (1 - tt) + 0.01, (1, 0, 0), pk.lin((92, 232, 255)), thick=0.04)
        tip = TAILP[3]
        pts = [tip, tip + Vector((0, 0.10, 0.12)), tip + Vector((0, 0.04, 0.20)), tip + Vector((0, 0.22, 0.30))]
        pk.strip(bm, L, pts, lambda t: 0.22 * (1 - t) + 0.03, (1, 0, 0), pk.lin((92, 232, 255)), thick=0.06)

    def crest_w(co):
        if co.y > 1.3:
            return {"Tail3": 1.0}
        if co.z > 1.35:
            return {"Head": 1.0}
        return {"Neck": 1.0}
    pk.glow_part(k, "Glow_Crest", GLOW, crest, crest_w)

    for side, sx in (("L", 1), ("R", -1)):
        S, _ = k.surf((sx * 0.9, -0.02, 1.16), (0, -0.02, 1.0))
        S = S - Vector((sx * 0.03, 0, 0.02))
        W = S + Vector((sx * 0.62, 0.18, 0.52))
        tips = [W + Vector((sx * 0.74, 0.24, 0.24)), W + Vector((sx * 0.68, 0.66, -0.24)), W + Vector((sx * 0.26, 0.86, -0.62))]
        B = Vector((sx * 0.30, 0.42, 0.78))
        pk.membrane_wing(k, side, S, W, tips, B, "Wing_" + side, "WingTip_" + side, MEM_ROOT, MEM_EDGE, WBONE, claw=CLAW)
        k.J_wing = getattr(k, "J_wing", {})
        k.J_wing[side] = (S, W)


def rig(k):
    k.joint("Spine", (0, 0.12, 0.80), "Root", tail=(0, -0.2, 0.4))
    k.joint("Neck", (0, -0.06, 1.14), "Spine")
    k.joint("Head", (0, -0.20, 1.40), "Neck", tail=(0, -0.3, 0.1))
    k.joint("Tail1", tuple(TAILP[0]), "Spine")
    k.joint("Tail2", tuple(TAILP[1]), "Tail1")
    k.joint("Tail3", tuple(TAILP[2]), "Tail2", tail=TAILP[3] - TAILP[2])
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Leg_" + side, (sx * 0.26, 0.14, 0.50), "Spine", tail=(0, 0, -0.4))
        S, W = k.J_wing[side]
        k.joint("Wing_" + side, S, "Spine")
        k.joint("WingTip_" + side, W, "Wing_" + side, tail=Vector((sx * 0.5, 0.4, 0.0)))
    k.body_bones = ["Spine", "Neck", "Head", "Tail1", "Tail2", "Tail3", "Leg_L", "Leg_R"]


TAIL = ["Tail1", "Tail2", "Tail3"]
FOLD = dict(up=-62, fwd=-18, tip_up=8, tip_fwd=-82)


def folded(k, f, d_up=0.0, d_fwd=0.0):
    cm.wing_pair(k, f, FOLD["up"] + d_up, FOLD["fwd"] + d_fwd, FOLD["tip_up"], FOLD["tip_fwd"])


FL = None


def flight(k):
    return cm.Flight(k, n=20, body_pitch=48, neck=-20, head=-22, amp=54, mid=6, sweep=16,
                     tuck={"Leg_L": 72, "Leg_R": 72}, tail=TAIL, tail_pitch=-16, tail_wave=8, bob=0.08)


def rest_keys(k):
    def f_(f):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Neck", f, rot=(-4, 0, 0))
        k.key("Head", f, rot=(-4, 0, 0))
        folded(k, f)
        for b in TAIL:
            k.key(b, f, rot=(0, 0, 0))
    return f_


def idle(k):
    """Showy: puffs the chest up proudly, looks side to side, a quick double wing-flick, the tail swishes."""
    n = 84
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(-2 - 2 * s, 0, 1.5 * pk.wave(f, n, 0.3)), loc=(0, 0, 0.012 * (1 + s) / 2))
        cm.chain(k, f, n, TAIL, sway=10, pitch=0, cycles=2, lag=0.12)
    for f, yaw, hd in ((0, 0, -4), (14, 24, -6), (28, 24, -6), (40, -22, -6), (54, -22, -6), (66, 0, -10), (84, 0, -4)):
        k.key("Neck", f, rot=(-4, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, 0))
    for f, du in ((0, 0), (58, 0), (61, 28), (64, 0), (67, 28), (70, 0), (84, 0)):
        folded(k, f, du, du * 0.5)
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish()
    k.meta["planted"] = cm.LEGS2


def walk(k):
    n = 22

    def body(f):
        k.key("Spine", f, rot=(4, 0, 5 * pk.wave(f, n)), loc=(0, 0, 0.03 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        k.key("Neck", f, rot=(-4 + 2 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(-4 - 2 * pk.wave(f, n, 0.2, 2), 0, -4 * pk.wave(f, n)))
        folded(k, f, 4 * pk.wave(f, n, 0.1, 2))
        cm.chain(k, f, n, TAIL, sway=12, pitch=0, cycles=1, lag=0.15)
    return cm.biped_walk(k, n, 0.11, 0.09, body)


def roar(k):
    """Screech: rears back, wings flung wide + up, chin to the sky, tail lashes; then settles."""
    n = 56
    k.new_action("roar", n, False)
    for f, sp, nk, hd, up, fwd, open_ in ((0, 0, -4, -4, None, None, 0), (10, 8, 4, 4, 20, -20, 0.3), (18, -14, -18, -20, 50, 4, 1),
                                          (40, -14, -20, -22, 54, 6, 1), (48, 2, -4, -4, 0, -30, 0.2), (56, 0, -4, -4, None, None, 0)):
        k.key("Spine", f, rot=(sp, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        if up is None:
            folded(k, f)
        else:
            cm.wing_pair(k, f, up, fwd, 24 * open_, 8 * open_)
        cm.chain(k, f, n, TAIL, sway=0, pitch=-10 * open_)
    for f in range(20, 40, 3):
        w = 1 if (f // 3) % 2 else -1
        k.key("Tail3", f, rot=(-10, 16 * w, 0))
        k.key("Head", f, rot=(-20, 0, 3 * w))
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish(loop=False)


def shake(k):
    """act: shakes off static like a wet dog - fast body shimmy front to back, wings half open, ends with a proud pose."""
    n = 48
    k.new_action("act_shake", n, False)
    for f in (0, 6, 40, 48):
        k.key("Spine", f, rot=(0, 0, 0))
        k.key("Head", f, rot=(-4, 0, 0))
        k.key("Neck", f, rot=(-4, 0, 0))
        folded(k, f, 10 if f in (6, 40) else 0)
        cm.chain(k, f, n, TAIL, sway=0)
    for i, f in enumerate(range(8, 39, 3)):
        w = 1 if i % 2 else -1
        decay = 1 - i / 11
        k.key("Head", f, rot=(-4, 22 * w * decay, 10 * w * decay))
        k.key("Neck", f, rot=(-4, -10 * w * decay, 0))
        k.key("Spine", f, rot=(0, 8 * w * decay, -6 * w * decay))
        cm.wing_pair(k, f, -10 + 12 * w, -30, -10, -20)
        k.key("Tail2", f, rot=(0, -16 * w * decay, 0))
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fl = flight(k)
    fl.fly()
    fl.takeoff(rest_keys(k), legs=cm.LEGS2)
    fl.land(rest_keys(k), legs=cm.LEGS2)
    roar(k)
    shake(k)
    return stride
