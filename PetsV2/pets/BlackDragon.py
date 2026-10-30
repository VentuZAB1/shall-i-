# Black Eastern Dragon (Void egg #3): a chibi lung dragon - glossy black-violet scales with a golden belly, a big
# lion-dragon face with huge violet eyes, golden branching antlers, long golden whiskers, a flowing glowing violet
# mane + tail tuft, four little golden-clawed legs, and its treasure: a glowing pearl that floats by its cheek.
# It FLIES without wings, like eastern dragons do: the whole serpent body swims through the air in waves.
# Personality: wise but playful - idles with a slow body wave, plays with its pearl; coils up and roars (roar);
# chases its pearl in a little loop (act).
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Black Eastern Dragon"
MOTION = "Fly"
RIG = "serpent"
HEIGHT = 7.0
C = pk.lin
SCALE = C((40, 34, 60))
SHEEN = C((84, 66, 134))
BELLY = C((242, 198, 96))
BELLY_D = C((214, 156, 64))
GOLD = C((255, 214, 110))
GOLD_D = C((220, 160, 60))
NOSE = C((20, 16, 30))
MANE = "9d6bff"
PEARL = "f2eaff"
HEAD = Vector((0, -0.76, 1.20))
BODY = [Vector((0, -0.34, 0.80)), Vector((0, 0.06, 0.56)), Vector((0.20, 0.50, 0.52)), Vector((-0.18, 0.96, 0.54)),
        Vector((0.12, 1.40, 0.66)), Vector((-0.04, 1.80, 0.86))]
RAD = [0.26, 0.28, 0.26, 0.22, 0.16, 0.09]


def body_color(co, n):
    c = pk.mix(SCALE, SHEEN, pk.smooth(0.4, 1.0, n.z) * 0.5)
    sc = 0.5 + 0.5 * math.sin(co.y * 26) * math.sin(co.x * 26 + co.z * 20)
    c = pk.mix(c, SHEEN, pk.smooth(0.75, 0.95, sc) * 0.35)
    belly = pk.smooth(-0.15, -0.6, n.z) * pk.smooth(-0.6, -0.2, co.y + 0.2)
    if belly > 0:
        seg = 0.5 + 0.5 * math.cos(co.y * 2 * math.pi / 0.16)
        c = pk.mix(c, pk.mix(BELLY, BELLY_D, pk.smooth(0.8, 0.97, seg)), belly)
    c = pk.mix(c, BELLY, pk.smooth(-0.3, -0.8, n.y) * pk.smooth(1.1, 0.8, co.z) * pk.smooth(-0.1, -0.35, co.y))
    c = pk.mix(c, SHEEN, pk.smooth(0.24, 0.14, (co - Vector((0, -1.14, 1.24))).length) * 0.6)
    for sx in (1, -1):
        c = pk.mix(c, C((170, 90, 200)), pk.smooth(0.12, 0.03, (co - Vector((sx * 0.30, -1.02, 1.20))).length) * 0.6)
    return c


def model(k):
    E = [("ell", tuple(HEAD), (0.42, 0.40, 0.37)), ("ell", (0, -1.10, 1.24), (0.24, 0.24, 0.18))]
    for i in range(len(BODY) - 1):
        E.append(("cap", tuple(BODY[i]), tuple(BODY[i + 1]), RAD[i] * 0.5 + RAD[i + 1] * 0.5))
    E.append(("cap", tuple(HEAD + Vector((0, 0.20, -0.16))), tuple(BODY[0]), 0.22))
    for sx in (1, -1):
        for (p0, foot) in ((Vector((sx * 0.22, 0.0, 0.48)), Vector((sx * 0.26, -0.06, 0.08))),
                           (Vector((sx * 0.22 - 0.18, 0.96, 0.46)), Vector((sx * 0.26 - 0.18, 0.92, 0.08)))):
            E += [("cap", tuple(p0), tuple(foot + Vector((0, 0, 0.06))), 0.12), ("ell", tuple(foot), (0.13, 0.15, 0.07))]
    k.body(E, body_color, tris=6200)

    k.eyes([((0.62, -2.6, 1.42), (0.21, -0.7, 1.36)), ((-0.62, -2.6, 1.42), (-0.21, -0.7, 1.36))],
           size=(0.16, 0.18), style="big", iris=(170, 110, 255))

    def face(bm, L):
        for sx in (1, -1):
            q, qn = k.surf((sx * 0.10, -2.4, 1.30), (sx * 0.10, -0.6, 1.28))
            pk.ellipsoid(bm, L, q + qn * 0.005, (0.035, 0.025, 0.025), NOSE, z_axis=qn)
            # long whiskers flowing back
            pts = [q + Vector((sx * 0.04, 0.0, -0.04))]
            for j in range(1, 8):
                t = j / 7
                pts.append(pts[0] + Vector((sx * (0.18 * t + 0.10 * t * t), 0.55 * t, -0.18 * t + 0.10 * math.sin(t * 5))))
            pk.tube(bm, L, pts, lambda t: 0.034 * (1 - t) + 0.010, lambda t, a: pk.mix(GOLD_D, GOLD, t), sides=7)
            # golden claws
            for (fx, fy) in ((sx * 0.26, -0.06), (sx * 0.26 - 0.18, 0.92)):
                for dx in (-0.06, 0.0, 0.06):
                    pk.cone(bm, L, (fx + dx, fy - 0.11, 0.05), (0, -1, -0.3), 0.07, 0.026, GOLD, sides=6, n=4)
        # small fangs
        for sx in (1, -1):
            q, qn = k.surf((sx * 0.12, -2.4, 1.14), (sx * 0.10, -0.6, 1.16))
            pk.cone(bm, L, q + Vector((0, 0.01, 0.02)), (0, -0.3, -1), 0.08, 0.026, C((255, 250, 236)))
        # dorsal spikes (gold) along the back
        for i in range(10):
            t = i / 9
            seg = t * (len(BODY) - 1)
            a = int(min(seg, len(BODY) - 2))
            p = BODY[a].lerp(BODY[a + 1], seg - a)
            r = RAD[a] * (1 - (seg - a)) + RAD[a + 1] * (seg - a)
            pk.cone(bm, L, p + Vector((0, 0, r * 0.82)), (0, 0.6, 1), 0.07 * (1 - 0.5 * t) + 0.03, 0.035, GOLD, sides=6, n=3)

    def face_w(co):
        if co.y < -0.5 and co.z > 0.9:
            return {"Head": 1.0}
        return body_w(co)
    k.part("Face", face, face_w)

    def antlers(bm, L):
        for sx in (1, -1):
            base, n = k.surf(HEAD + Vector((sx * 0.35, 0.1, 1.0)), HEAD + Vector((sx * 0.12, 0.1, 0.1)))
            main = pk.arc_points(base - n * 0.03, (sx * 0.3, 0.45, 1.0), 0.46, bend_axis=(1, 0, 0), bend_deg=30, n=7)
            pk.tube(bm, L, main, (0.05, 0.025), lambda t, a: pk.mix(GOLD_D, GOLD, t), sides=8)
            tine = pk.arc_points(main[3], (sx * 0.6, -0.2, 0.8), 0.18, n=4)
            pk.tube(bm, L, tine, (0.03, 0.015), GOLD, sides=6)
    k.part("Antlers", antlers, "Head")

    def mane(bm, L):
        col = pk.lin((157, 107, 255))
        # behind the head
        for j, (dx, dz) in enumerate(((0, 0.30), (0.22, 0.16), (-0.22, 0.16), (0.30, -0.06), (-0.30, -0.06))):
            b = HEAD + Vector((dx, 0.28, dz))
            d = Vector((dx * 0.8, 0.9, 0.25)).normalized()
            pk.blob(bm, L, pk.frame(b + d * 0.12, (1, 0, 0), d),
                    lambda u: Vector((u.x * 0.11 * (1 - 0.6 * max(u.z, 0)), u.y * 0.08 * (1 - 0.6 * max(u.z, 0)),
                                      u.z * 0.22 + 0.05 * max(u.z, 0) ** 3)), col, 10, 8)
        # a flowing mane down the back
        for i in range(7):
            t = (i + 0.5) / 7 * 0.8
            seg = t * (len(BODY) - 1)
            a = int(seg)
            p = BODY[a].lerp(BODY[a + 1], seg - a)
            r = RAD[a] * (1 - (seg - a)) + RAD[a + 1] * (seg - a)
            d = Vector((0, 0.8, 0.6)).normalized()
            hh = 0.20 * (1 - 0.5 * t)
            pk.blob(bm, L, pk.frame(p + Vector((0, 0.04, r * 0.85)) + d * hh * 0.4, (1, 0, 0), d),
                    lambda u, hh=hh: Vector((u.x * 0.05 * (1 - 0.6 * max(u.z, 0)), u.y * 0.09 * (1 - 0.6 * max(u.z, 0)),
                                             u.z * hh * 0.6 + 0.04 * max(u.z, 0) ** 3)), col, 8, 6)
        # tail tuft
        tip = BODY[-1]
        for j, ang in enumerate((-0.5, 0.0, 0.5)):
            d = Vector((math.sin(ang) * 0.6, 0.8, 0.3 + 0.2 * abs(ang))).normalized()
            pk.blob(bm, L, pk.frame(tip + d * 0.14, (1, 0, 0), d),
                    lambda u: Vector((u.x * 0.09 * (1 - 0.6 * max(u.z, 0)), u.y * 0.07, u.z * 0.20 + 0.05 * max(u.z, 0) ** 3)),
                    col, 10, 8)

    def mane_w(co):
        if co.y < -0.35:
            return {"Head": 1.0}
        return body_w(co)
    pk.glow_part(k, "Glow_Mane", MANE, mane, mane_w)

    def pearl(bm, L):
        pk.ellipsoid(bm, L, HEAD + Vector((0.52, -0.36, -0.18)), (0.11, 0.11, 0.11), pk.lin((242, 234, 255)), useg=14, vseg=10)
    pk.glow_part(k, "Glow_Pearl", PEARL, pearl, "Pearl")


def body_w(co):
    """blend along the serpent chain by y"""
    chain = [("Spine", BODY[0].y), ("Body1", BODY[1].y), ("Body2", BODY[2].y), ("Body3", BODY[3].y), ("Tail", BODY[4].y)]
    y = co.y
    if co.z < 0.36:   # legs
        if co.y < 0.5:
            return {"Leg_F" + ("L" if co.x > 0 else "R"): 1.0}
        return {"Leg_B" + ("L" if co.x > -0.18 else "R"): 1.0}
    if y <= chain[0][1]:
        return {chain[0][0]: 1.0}
    for (a, ya), (b, yb) in zip(chain, chain[1:]):
        if y <= yb:
            t = (y - ya) / (yb - ya)
            return {a: 1 - t, b: t}
    return {chain[-1][0]: 1.0}


def rig(k):
    k.joint("Spine", tuple(BODY[0]), "Root", tail=(0, -0.3, 0.2))
    k.joint("Neck", tuple(HEAD + Vector((0, 0.22, -0.18))), "Spine")
    k.joint("Head", tuple(HEAD + Vector((0, 0.10, -0.08))), "Neck", tail=(0, -0.3, 0.05))
    k.joint("Pearl", tuple(HEAD + Vector((0.52, -0.36, -0.18))), "Head", tail=(0, 0, 0.15))
    k.joint("Body1", tuple(BODY[1]), "Spine", tail=BODY[2] - BODY[1])
    k.joint("Body2", tuple(BODY[2]), "Body1", tail=BODY[3] - BODY[2])
    k.joint("Body3", tuple(BODY[3]), "Body2", tail=BODY[4] - BODY[3])
    k.joint("Tail", tuple(BODY[4]), "Body3", tail=BODY[5] - BODY[4])
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Leg_F" + side, (sx * 0.22, 0.0, 0.48), "Spine", tail=(0, 0, -0.35))
        k.joint("Leg_B" + side, (sx * 0.22 - 0.18, 0.96, 0.46), "Body2", tail=(0, 0, -0.35))
    k.body_bones = ["Spine", "Neck", "Head", "Body1", "Body2", "Body3", "Tail"] + cm.LEGS4


CHAIN = ["Body1", "Body2", "Body3", "Tail"]


def undulate(k, f, n, yaw=0.0, pitch=0.0, cycles=1, phase=0.0, lag=0.18):
    """a travelling wave down the serpent body (yaw = side to side on the ground, pitch = up/down in the air)"""
    for i, b in enumerate(CHAIN):
        ph = phase - lag * (i + 1)
        k.key(b, f, rot=(pitch * pk.wave(f, n, ph, cycles), yaw * pk.wave(f, n, ph, cycles), 0))


def pearl(k, f, n, amp=1.0):
    k.key("Pearl", f, rot=(0, 30 * pk.wave(f, n, 0.0, 1), 0), loc=(0.02 * amp * pk.wave(f, n, 0.25, 2), 0, 0.06 * amp * pk.wave(f, n, 0.0, 2)))


def idle(k):
    """A slow, wise sway: the body waves gently, the head watches its pearl float + bob, whisker-twitch nods."""
    n = 96
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(1 * s, 0, 0), loc=(0, 0, 0.015 * (1 + s) / 2))
        undulate(k, f, n, yaw=10, cycles=2, lag=0.2)
        pearl(k, f, n)
        k.key("Neck", f, rot=(-4 + 2 * pk.wave(f, n, 0.2, 2), 10 * pk.wave(f, n, 0.05), 0))
        k.key("Head", f, rot=(-4, 14 * pk.wave(f, n, 0.0), 6 * pk.wave(f, n, 0.1)))
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = cm.LEGS4


def walk(k):
    n = 24

    def body(f):
        k.key("Spine", f, rot=(1 * pk.wave(f, n, 0.1, 2), 6 * pk.wave(f, n), 3 * pk.wave(f, n)), loc=(0, 0, 0.03 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        undulate(k, f, n, yaw=14, cycles=1, lag=0.22)
        k.key("Neck", f, rot=(-4, -5 * pk.wave(f, n), 0))
        k.key("Head", f, rot=(-3, -4 * pk.wave(f, n), -2 * pk.wave(f, n)))
        pearl(k, f, n, 0.6)
    return cm.quad_walk(k, n, 0.50 * math.sin(math.radians(20)), 0.10, body, gait="trot")


FLY_N = 32


def fly_pose(k, f, n=FLY_N, legs=True):
    """Swims through the air: a big travelling up/down wave from the chest to the tail tip, the head stays steady
    and looks ahead, legs tucked back along the belly, mane + pearl trail."""
    ph = f / n
    k.key("Spine", f, rot=(6 * math.sin(2 * math.pi * ph), 0, 2 * math.sin(2 * math.pi * (ph - 0.2))),
          loc=(0, 0, 0.10 * math.sin(2 * math.pi * (ph + 0.1))))
    for i, b in enumerate(CHAIN):
        p = 2 * math.pi * (ph - 0.16 * (i + 1))
        k.key(b, f, rot=(22 * math.sin(p), 6 * math.sin(p - 0.8), 0))
    k.key("Neck", f, rot=(-8 - 5 * math.sin(2 * math.pi * ph), 0, 0))
    k.key("Head", f, rot=(-6 - 2 * math.sin(2 * math.pi * (ph + 0.05)), 0, 0))
    if legs:
        for leg in cm.LEGS4:
            k.key(leg, f, rot=(70 + 6 * math.sin(2 * math.pi * ph), 0, 0), loc=(0, 0, 0.04))
    k.key("Pearl", f, rot=(0, 0, 0), loc=(0.02, 0.10 + 0.04 * math.sin(2 * math.pi * ph), 0.05 * math.sin(2 * math.pi * (ph + 0.3))))


def fly(k):
    k.new_action("fly", FLY_N, True)
    for f in range(0, FLY_N + 1):
        fly_pose(k, f)
    k.finish()


def rest(k, f):
    k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
    for b in CHAIN:
        k.key(b, f, rot=(0, 0, 0))
    k.key("Neck", f, rot=(-4, 0, 0))
    k.key("Head", f, rot=(-4, 0, 0))
    k.key("Pearl", f, rot=(0, 0, 0), loc=(0, 0, 0))


def takeoff(k):
    import bpy
    n = 27
    k.new_action("takeoff", n, False)
    rest(k, 0)
    for f, z, sp, wave in ((6, -0.10, 6, 0.4), (10, -0.12, 8, 0.6), (13, 0.24, -14, 1.0), (17, 0.34, -6, 1.0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        for i, b in enumerate(CHAIN):
            k.key(b, f, rot=(-18 * wave * math.sin(1.4 * i + f * 0.3), 0, 0))
        k.key("Neck", f, rot=(-8 - sp * 0.5, 0, 0))
        k.key("Head", f, rot=(-6, 0, 0))
    fly_pose(k, n, legs=False)
    k.bake_bezier_now()
    for f in range(0, 12):
        bpy.context.scene.frame_set(f)
        for leg in cm.LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f, t in ((14, 0.4), (20, 0.85), (n, 1.0)):
        for leg in cm.LEGS4:
            k.key(leg, f, rot=(70 * t, 0, 0), loc=(0, 0, 0.04 if f == n else 0.0))
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    import bpy
    n = 27
    k.new_action("land", n, False)
    fly_pose(k, 0)
    for f, z, sp in ((7, 0.12, -14), (12, 0.06, -8), (16, -0.08, 4)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        for i, b in enumerate(CHAIN):
            k.key(b, f, rot=(10 * math.sin(1.3 * i + f * 0.4) * (1 if f < 16 else 0.3), 0, 0))
        k.key("Neck", f, rot=(-6 - sp * 0.4, 0, 0))
        k.key("Head", f, rot=(-5, 0, 0))
    for f in (21, 27):
        rest(k, f)
    for leg in cm.LEGS4:
        k.key(leg, 7, rot=(-20 if "F" in leg[4] else -6, 0, 0), loc=(0, 0, 0))
    k.bake_bezier_now()
    for f in range(16, n + 1):
        bpy.context.scene.frame_set(f)
        for leg in cm.LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(16 / n, 3)}


def roar(k):
    """Rears its head up high (the body coils into an S), roars at the sky, the pearl flares up beside it."""
    n = 60
    k.new_action("roar", n, False)
    for f, sp, nk, hd, coil in ((0, 0, -4, -4, 0), (10, 4, 6, 6, 0.4), (20, -18, -24, -20, 1), (44, -18, -26, -22, 1),
                                (52, 2, -4, -4, 0.2), (60, 0, -4, -4, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, 0.05 * coil))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        for i, b in enumerate(CHAIN):
            k.key(b, f, rot=(0, 26 * coil * (1 if i % 2 == 0 else -1), 0))
        k.key("Pearl", f, rot=(0, 0, 0), loc=(0, 0, 0.25 * coil))
    cm.plant(k, n)
    k.finish(loop=False)


def chase(k):
    """act: plays with its pearl - the pearl circles around the head, the head follows it, the tail wiggles."""
    n = 60
    k.new_action("act_pearl", n, False)
    rest(k, 0)
    for f in range(6, 55, 4):
        a = 2 * math.pi * (f - 6) / 48
        k.key("Pearl", f, rot=(0, 0, 0), loc=(-0.30 * (1 - math.cos(a)), -0.20 * math.sin(a), 0.18 * math.sin(a)))
        k.key("Head", f, rot=(-4 - 12 * math.sin(a), -30 * (1 - math.cos(a)) * 0.5, 8 * math.sin(a)))
        k.key("Neck", f, rot=(-4, -10 * (1 - math.cos(a)) * 0.5, 0))
        for i, b in enumerate(CHAIN):
            k.key(b, f, rot=(0, 14 * math.sin(a * 2 - 0.6 * i), 0))
    rest(k, n)
    cm.plant(k, n)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    chase(k)
    return stride
