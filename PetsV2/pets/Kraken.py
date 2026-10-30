# Kraken (Tide egg #3): a chibi baby kraken - a big round purple-pink mantle speckled with glowing cyan
# bioluminescent dots, huge sparkly eyes, rosy cheeks, eight curly tentacles with cream suckers. Personality:
# a playful little troublemaker - bobs and curls its tentacles, jets around with real pulse strokes, splays all
# eight tentacles out to look scary (roar ... it is not scary), waves hello with one tentacle.
import math
from mathutils import Vector, Quaternion
import petkit as pk
import _common as cm

DISPLAY = "Kraken"
MOTION = "Swim"
RIG = "kraken"
HEIGHT = 7.5
C = pk.lin
TOP = C((150, 76, 200))
MID = C((206, 110, 214))
LOW = C((255, 160, 206))
SUCK = C((255, 222, 228))
SPOT = C((232, 170, 240))
GLOW = "52f0ff"
MANTLE = Vector((0, 0.06, 1.22))
N_T = 8
R_BASE = 0.34
Z_BASE = 0.62


def t_angle(i):
    return math.radians(90 + 22.5 + 45 * i)   # no tentacle straight in front, so the face stays clear


def t_path(i, n=10):
    a = t_angle(i)
    d = Vector((math.cos(a), math.sin(a), 0))
    pts = []
    for j in range(n):
        t = j / (n - 1)
        r = R_BASE + 0.82 * t
        z = Z_BASE - 0.56 * t + 0.50 * t ** 3
        curl = 0.16 * t ** 3
        pts.append(Vector((d.x * (r - curl), d.y * (r - curl), z)))
    return pts


def body_color(co, n):
    c = pk.mix(MID, TOP, pk.smooth(0.9, 1.6, co.z))
    c = pk.mix(c, LOW, pk.smooth(0.85, 0.6, co.z))
    sp = math.sin(co.x * 13 + 1.0) * math.sin(co.y * 12 + 0.4) * math.sin(co.z * 14 + 2.0)
    c = pk.mix(c, SPOT, pk.smooth(0.35, 0.55, sp) * pk.smooth(1.0, 1.3, co.z))
    for sx in (1, -1):
        c = pk.mix(c, pk.BLUSH, pk.smooth(0.12, 0.03, (co - Vector((sx * 0.34, -0.42, 0.96))).length) * 0.6)
    return c


def model(k):
    E = [("ell", tuple(MANTLE), (0.60, 0.58, 0.62)),
         ("ell", (0, 0.20, 1.55), (0.42, 0.44, 0.40)),            # the mantle's soft bulb, tipped back
         ("ell", (0, 0.0, 0.74), (0.50, 0.48, 0.30))]             # skirt where the tentacles start
    k.body(E, body_color, tris=4200)

    k.eyes([((0.62, -2.6, 1.08), (0.21, -0.3, 1.04)), ((-0.62, -2.6, 1.08), (-0.21, -0.3, 1.04))],
           size=(0.17, 0.19), style="big", iris=(60, 196, 255))

    def face(bm, L):
        pts = []
        for x in (-0.08, -0.04, 0.0, 0.04, 0.08):
            q, qn = k.surf((x, -2.4, 0.86 - 0.035 * (1 - (x / 0.08) ** 2)), (x * 0.5, 0, 0.86))
            pts.append(q + qn * 0.01)
        pk.tube(bm, L, pts, 0.014, pk.lin((90, 30, 70)), sides=6)
    k.part("Face", face, "Head")

    def tentacles(bm, L):
        for i in range(N_T):
            pts = t_path(i)
            pk.tube(bm, L, pts, lambda t: 0.13 * (1 - t) ** 0.8 + 0.03,
                    lambda t, a: pk.mix(MID, LOW, pk.smooth(0.0, 0.6, t)), sides=10)
            a = t_angle(i)
            d = Vector((math.cos(a), math.sin(a), 0))
            for j in range(2, 9):
                t = j / 9
                p = pts[j]
                rad = 0.13 * (1 - t) ** 0.8 + 0.03
                pk.ellipsoid(bm, L, p + Vector((0, 0, -rad * 0.85)), (rad * 0.42, rad * 0.42, rad * 0.25), SUCK,
                             useg=8, vseg=5)

    def t_w(co):
        a = math.atan2(co.y, co.x)
        best = min(range(N_T), key=lambda i: abs((a - t_angle(i) + math.pi) % (2 * math.pi) - math.pi))
        r = Vector((co.x, co.y)).length
        u = (r - R_BASE) / 0.80
        w = pk.smooth(0.30, 0.55, u)
        if u < 0.05:
            return {"Spine": 1.0}
        return {f"T{best + 1}a": 1 - w, f"T{best + 1}b": w}
    k.part("Tentacles", tentacles, t_w)

    def crown(bm, L):
        top, tn = k.surf(MANTLE + Vector((0.25, 0.2, 1.5)), MANTLE + Vector((0, 0.1, 0.2)))
        ax = (tn + Vector((0.1, 0, 0.6))).normalized()
        pk.torus(bm, L, top + ax * 0.02, 0.17, 0.035, pk.lin((255, 200, 64)), x_axis=(1, 0, 0), z_axis=ax, N=24, M=6)
        side = ax.orthogonal().normalized()
        for j in range(5):
            q = Quaternion(ax, 2 * math.pi * j / 5) @ side
            pk.cone(bm, L, top + ax * 0.04 + q * 0.17, ax, 0.16, 0.05, pk.lin((255, 210, 80)), sides=6, n=4)
        k.crown = (top, ax)
    k.part("Crown", crown, "Head")

    def dots(bm, L):
        top, ax = k.crown
        pk.ellipsoid(bm, L, top + ax * 0.10, (0.07, 0.07, 0.07), pk.lin((200, 250, 255)), useg=10, vseg=8)
        for i in range(22):
            a = 2 * math.pi * i / 22 + (0.3 if i % 2 else 0)
            z = 1.18 + 0.45 * ((i * 37) % 11) / 11
            d = Vector((math.cos(a), math.sin(a), 0))
            if d.y < -0.5 and z < 1.45:
                continue
            q, qn = k.surf(MANTLE + Vector((d.x * 2, d.y * 2, z - MANTLE.z + 0.3)), Vector((0, 0.06, z)))
            pk.ellipsoid(bm, L, q, (0.06, 0.06, 0.025), pk.lin((82, 240, 255)), z_axis=qn, useg=8, vseg=4)
    pk.glow_part(k, "Glow_Dots", GLOW, dots, "Head")


def rig(k):
    k.joint("Spine", (0, 0.02, 0.70), "Root", tail=(0, 0, 0.4))
    k.joint("Head", (0, 0.04, 1.12), "Spine", tail=(0, 0, 0.4))
    for i in range(N_T):
        pts = t_path(i)
        k.joint(f"T{i + 1}a", tuple(pts[0]), "Spine", tail=pts[4] - pts[0])
        k.joint(f"T{i + 1}b", tuple(pts[4]), f"T{i + 1}a", tail=pts[9] - pts[4])
    k.body_bones = ["Spine", "Head"]


def tent(k, f, i, a_deg, b_deg, twist=0.0):
    """a/b + = that segment swings DOWN (toward the body's underside), - = up/out. twist sways sideways."""
    a = t_angle(i)
    tan = Vector((-math.sin(a), math.cos(a), 0))
    side = Quaternion(Vector((0, 0, 1)), math.radians(twist))
    cm.key_axis(k, f"T{i + 1}a", f, tan, a_deg, extra=side)
    cm.key_axis(k, f"T{i + 1}b", f, tan, b_deg)


def idle(k):
    """Floating: a lazy bob, the mantle sways, every tentacle curls in a travelling wave around the body."""
    n = 72
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        k.key("Spine", f, rot=(2 * pk.wave(f, n, 0.1), 0, 3 * pk.wave(f, n, 0.3)), loc=(0, 0, 0.06 * pk.wave(f, n, 0, 2)))
        k.key("Head", f, rot=(-3 * pk.wave(f, n, 0.25, 2), 4 * pk.wave(f, n, 0.1), -3 * pk.wave(f, n, 0.3)))
        for i in range(N_T):
            ph = i / N_T
            tent(k, f, i, 10 * pk.wave(f, n, ph, 2), -18 + 16 * pk.wave(f, n, ph - 0.12, 2), 6 * pk.wave(f, n, ph + 0.2))
    k.finish()


def swim(k):
    """Jet strokes: tentacles open wide (recover), then snap down + together (power) - the body surges up and
    tilts forward on each stroke; the mantle squishes."""
    n = 30
    k.new_action("swim", n, True)
    for f in range(0, n + 1):
        ph = f / n
        power = 0.5 - 0.5 * math.cos(2 * math.pi * ph)          # 0 open .. 1 closed (mid-cycle)
        k.key("Spine", f, rot=(14 + 6 * power, 0, 0), loc=(0, 0, 0.10 * math.sin(2 * math.pi * (ph - 0.15))))
        k.key("Head", f, rot=(-4 - 6 * power, 0, 0), loc=(0, 0, 0.03 * power))
        for i in range(N_T):
            back = 1.0 if math.sin(t_angle(i)) > 0 else 0.6      # back tentacles trail more
            tent(k, f, i, -26 + 52 * power * back, -12 + 30 * math.sin(2 * math.pi * (ph - 0.18)))
    k.finish()


def roar(k):
    """'Scary' pose: all eight tentacles splay out + up, the mantle puffs tall and wobbles... then flops back."""
    n = 54
    k.new_action("roar", n, False)
    for f, op, puff in ((0, 0, 0), (8, 0.2, -0.04), (16, 1, 0.12), (34, 1, 0.12), (42, -0.2, -0.03), (54, 0, 0)):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.12 * max(op, 0)))
        k.key("Head", f, rot=(-6 * max(op, 0), 0, 0), loc=(0, 0, puff))
        for i in range(N_T):
            tent(k, f, i, -34 * op + 10 * (op < 0), 12 * op)
    for f in range(18, 34, 3):
        w = 1 if (f // 3) % 2 else -1
        k.key("Head", f, rot=(-6, 0, 5 * w), loc=(0, 0, 0.12))
    k.finish(loop=False)


def wave(k):
    """act: waves hello with a front tentacle while the others curl."""
    n = 60
    k.new_action("act_wave", n, False)
    for f in range(0, n + 1, 3):
        k.key("Spine", f, rot=(0, 0, 4 * pk.wave(f, n, 0, 1) * (1 if 6 < f < 54 else 0)), loc=(0, 0, 0.04 * pk.wave(f, n, 0, 2)))
        k.key("Head", f, rot=(0, 0, 6 * pk.wave(f, n, 0, 1) * (1 if 6 < f < 54 else 0)))
        for i in range(N_T):
            if i == 4:
                continue
            tent(k, f, i, 6 * pk.wave(f, n, i / N_T, 2), -16 + 10 * pk.wave(f, n, i / N_T - 0.1, 2))
    i = 4   # a front tentacle (front-left) waves
    for f, a, b, tw in ((0, 0, -16, 0), (8, -80, -40, 0), (14, -84, -10, 25), (20, -84, -50, -25), (26, -84, -10, 25),
                        (32, -84, -50, -25), (38, -84, -10, 25), (46, -70, -30, 0), (60, 0, -16, 0)):
        tent(k, f, i, a, b, tw)
    k.finish(loop=False)


def anim(k):
    idle(k)
    swim(k)
    roar(k)
    wave(k)
    return 0.0
