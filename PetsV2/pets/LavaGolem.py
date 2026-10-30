# Lava Golem (Magma egg #2): a gentle little giant - a round basalt boulder body with glowing lava cracks, a
# glowing magma heart crystal in its chest, a small rocky head with big kind eyes and a 'hairdo' of rock chunks,
# huge boulder fists on short arms, stubby legs. Personality: big softie - slow heavy breaths, bumps its fists
# together, checks its hands; pounds its chest like a gorilla (roar); smashes the ground with both fists (act).
import math
from mathutils import Vector
import petkit as pk
import _common as cm

DISPLAY = "Lava Golem"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 8.5
C = pk.lin
ROCK = C((78, 66, 70))
ROCK_L = C((118, 100, 98))
ROCK_D = C((48, 40, 46))
EMBER = C((255, 120, 46))
GLOW_O = "ff7a1e"
GLOW_Y = "ffd24a"
HEAD = Vector((0, -0.06, 1.48))


def rock_noise(co):
    return 0.5 + 0.5 * math.sin(co.x * 11 + 1.3) * math.sin(co.y * 10 + 0.4) * math.sin(co.z * 12 + 2.2)


def body_color(co, n):
    c = pk.mix(ROCK_D, ROCK, pk.smooth(-0.6, 0.6, n.z) * 0.6 + 0.4)
    c = pk.mix(c, ROCK_L, pk.smooth(0.55, 0.85, rock_noise(co)) * 0.6)
    c = pk.mix(c, EMBER, pk.smooth(-0.3, -0.85, n.z) * pk.smooth(0.25, 0.45, co.z) * 0.6)
    for sx in (1, -1):
        c = pk.mix(c, EMBER, pk.smooth(0.12, 0.03, (co - Vector((sx * 0.25, -0.36, 1.36))).length) * 0.5)
    return c


def model(k):
    E = [
        ("ell", (0, 0.0, 0.88), (0.58, 0.48, 0.56)),
        ("ell", tuple(HEAD), (0.40, 0.36, 0.34)),
        ("ell", (0, 0.0, 0.40), (0.46, 0.40, 0.26)),
    ]
    for sx in (1, -1):
        E += [("ell", (sx * 0.26, -0.02, 0.24), (0.18, 0.20, 0.22)),
              ("ell", (sx * 0.27, -0.08, 0.08), (0.19, 0.24, 0.09))]
    k.body(E, body_color, tris=5200)

    k.eyes([((0.55, -2.6, 1.54), (0.17, -0.3, 1.50)), ((-0.55, -2.6, 1.54), (-0.17, -0.3, 1.50))],
           size=(0.16, 0.18), style="big", iris=(255, 150, 50))

    def face(bm, L):
        pts = []
        for x in (-0.08, -0.04, 0.0, 0.04, 0.08):
            q, qn = k.surf((x, -2.4, 1.36 - 0.03 * (1 - (x / 0.08) ** 2)), (x * 0.5, 0, 1.38))
            pts.append(q + qn * 0.01)
        pk.tube(bm, L, pts, 0.014, C((40, 24, 26)), sides=6)
        # rock hairdo
        for j, (dx, dy, h) in enumerate(((0.0, 0.0, 0.24), (0.16, 0.08, 0.18), (-0.16, 0.06, 0.2), (0.06, 0.18, 0.16), (-0.08, -0.12, 0.15))):
            b, bn = k.surf(HEAD + Vector((dx, dy, 1.0)), HEAD + Vector((dx * 0.5, dy * 0.5, 0)))
            pk.cone(bm, L, b - bn * 0.05, (bn + Vector((dx, dy, 0.3))).normalized(), h, 0.09, lambda t, a: pk.mix(ROCK, ROCK_L, t), sides=5, n=3)
    k.part("Face", face, "Head")

    def arms(bm, L):
        for sx in (1, -1):
            sh = Vector((sx * 0.58, -0.02, 1.06))
            pk.ellipsoid(bm, L, sh, (0.20, 0.20, 0.20), lambda u, lc: pk.mix(ROCK, ROCK_L, pk.smooth(-0.3, 0.8, u.z)), useg=12, vseg=8)
            pk.tube(bm, L, [sh, sh + Vector((sx * 0.10, -0.04, -0.30))], (0.15, 0.13), ROCK, sides=8)
            fist = sh + Vector((sx * 0.13, -0.08, -0.50))
            pk.blob(bm, L, pk.frame(fist, (1, 0, 0), (0, 0, 1)),
                    lambda u: Vector((u.x * 0.26 * (1 + 0.08 * math.sin(u.y * 9)), u.y * 0.27, u.z * 0.25 * (1 + 0.06 * math.sin(u.x * 11)))),
                    lambda u, lc: pk.mix(ROCK_D, ROCK_L, pk.smooth(-0.4, 0.9, u.z)), 14, 10)
            for dz in (-0.08, 0.0, 0.08):
                pk.ellipsoid(bm, L, fist + Vector((sx * 0.03, -0.24, dz + 0.04)), (0.07, 0.05, 0.05), ROCK, useg=8, vseg=6)
    k.part("Arms", arms, lambda co: {"Arm_L" if co.x > 0 else "Arm_R": 1.0})

    def lava(bm, L, inner):
        if not inner:
            # wandering lava cracks over the body
            for i, (yaw, z) in enumerate(((-40, 1.10), (35, 0.80), (70, 1.05), (-75, 0.70), (140, 0.95), (-150, 1.15), (200, 0.70))):
                cm.crack(k, bm, L, yaw, z, 11 + i * 5, pk.lin((255, 122, 30)), steps=6)
        # magma heart crystal in the chest
        p, n = k.surf((0, -2.4, 0.98), (0, 0, 0.98))
        s = 0.55 if inner else 1.0
        pk.blob(bm, L, pk.frame(p + n * (0.02 if inner else -0.01), (1, 0, 0), n),
                lambda u: Vector((u.x * 0.15 * s * (1 - 0.35 * u.y), u.y * 0.17 * s, u.z * 0.06 * s + 0.02)),
                pk.lin((255, 210, 74)) if inner else pk.lin((255, 122, 30)), 12, 8)
    pk.glow_part(k, "Glow_Lava", GLOW_O, lambda bm, L: lava(bm, L, False), lambda co: {"Spine": 1.0} if co.z < 1.2 else {"Head": 1.0})
    pk.glow_part(k, "Glow_Core", GLOW_Y, lambda bm, L: lava(bm, L, True), "Spine")


def rig(k):
    k.joint("Spine", (0, 0.0, 0.45), "Root", tail=(0, 0, 0.5))
    k.joint("Head", (0, -0.04, 1.22), "Spine", tail=(0, 0, 0.3))
    for side, sx in (("L", 1), ("R", -1)):
        k.joint("Arm_" + side, (sx * 0.58, -0.02, 1.06), "Spine", tail=(sx * 0.12, -0.06, -0.5))
        k.joint("Leg_" + side, (sx * 0.26, 0.0, 0.36), "Spine", tail=(0, 0, -0.3))
    k.body_bones = ["Spine", "Head", "Leg_L", "Leg_R"]


def arms(k, f, up_l, up_r, fwd_l=0.0, fwd_r=0.0, in_l=0.0, in_r=0.0):
    """arms hang down: fwd + = swing forward (pitch -), up + = raise sideways, in + = toward the body (yaw)."""
    k.key("Arm_L", f, rot=(-fwd_l, 0, -(up_l - in_l)))
    k.key("Arm_R", f, rot=(-fwd_r, 0, up_r - in_r))


def idle(k):
    """Slow heavy breathing, looks down at its fists, bumps them together twice, a happy little sway."""
    n = 96
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(1.5 * s, 0, 2 * pk.wave(f, n, 0.2)), loc=(0, 0, 0.02 * (1 + s) / 2))
    for f, hd, yaw in ((0, -2, 0), (24, 14, 0), (40, 14, 0), (56, -2, 0), (70, -4, 16), (84, -4, -12), (96, -2, 0)):
        k.key("Head", f, rot=(hd, yaw, 0))
    for f, fw, inn in ((0, 0, 0), (24, 40, 30), (30, 40, 44), (33, 40, 30), (36, 40, 44), (40, 40, 30), (52, 0, 0), (96, 0, 0)):
        arms(k, f, 0, 0, fw, fw, inn, inn)
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish()
    k.meta["planted"] = cm.LEGS2


def walk(k):
    n = 28

    def body(f):
        k.key("Spine", f, rot=(3, 4 * pk.wave(f, n), 7 * pk.wave(f, n)), loc=(0, 0, 0.04 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        k.key("Head", f, rot=(-2, -3 * pk.wave(f, n), -5 * pk.wave(f, n)))
        arms(k, f, 6, 6, 20 * pk.wave(f, n, 0.05), -20 * pk.wave(f, n, 0.05))
    return cm.biped_walk(k, n, 0.12, 0.08, body)


def roar(k):
    """Gorilla chest-pound: fists alternate on the chest 4 times, head back with a roar, then a proud stance."""
    n = 60
    k.new_action("roar", n, False)
    for f, sp, hd in ((0, 0, -2), (8, -6, -10), (40, -6, -14), (50, 2, -2), (60, 0, -2)):
        k.key("Spine", f, rot=(sp, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
    arms(k, 0, 0, 0)
    for i, f in enumerate(range(10, 42, 4)):
        l_hit = i % 2 == 0
        arms(k, f, 20, 20, 70 if l_hit else 40, 40 if l_hit else 70, 60 if l_hit else 30, 30 if l_hit else 60)
    arms(k, 50, 10, 10, 0, 0)
    arms(k, 60, 0, 0)
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish(loop=False)


def smash(k):
    """act: both fists up over the head ... SLAM the ground (body crouches), a shake, then back up."""
    n = 54
    k.new_action("act_smash", n, False)
    for f, sp, z, fw, up in ((0, 0, 0, 0, 0), (12, -10, 0.04, 150, 10), (18, -12, 0.05, 160, 10), (22, 28, -0.10, 40, 0),
                             (32, 26, -0.10, 40, 0), (42, 4, 0, 10, 0), (54, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Head", f, rot=(-sp * 0.4, 0, 0))
        arms(k, f, up, up, fw, fw, 20 if fw > 100 else 0, 20 if fw > 100 else 0)
    for f in (24, 27, 30):
        k.key("Head", f, rot=(-8, 0, 6 if f != 27 else -6))
    cm.plant(k, n, legs=cm.LEGS2)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    smash(k)
    return stride
