# Ivonrath (Ivon's pet): a fierce little red fire dragon. Fierce-cute: big chibi head, determined angled brows,
# amber eyes, tiny fangs, gold-tipped charcoal horns, crimson scales with a gold plated belly, orange back spikes,
# membrane wings, a living flame on the tail tip. Personality: proud and cheeky - chin up, looks around, tail
# swishes, flame flickers; roars with a puff of fire.
import math
from mathutils import Vector
import petkit as pk

DISPLAY = "Ivonrath"
MOTION = "Fly"
RIG = "wingquad"
HEIGHT = 7.5
C = pk.lin
TOP = C((168, 26, 40))
SIDE = C((214, 46, 44))
BELLY = C((255, 200, 112))
BELLY_D = C((236, 150, 72))
FOOT = C((118, 18, 30))
EMBER = C((255, 112, 60))
HORN = C((70, 44, 50))
HORN_TIP = C((255, 196, 90))
SPIKE = C((255, 132, 40))
SPIKE_TIP = C((255, 214, 96))
IVORY = C((255, 246, 226))
NOSE = C((90, 14, 24))
MEM_ROOT = C((228, 62, 46))
MEM_EDGE = C((255, 152, 58))
WBONE = C((130, 22, 34))
FLAME_O = "ff7a1e"
FLAME_Y = "ffdc50"

SPINE_CHAIN = [("Neck", -0.30), ("Spine", 0.35), ("Tail1", 1.0), ("Tail2", 1.45), ("Tail3", 1.9)]


def chain_w(co):
    """Weights for things stuck on the back/tail: blend between the chain bones by y."""
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
    c = pk.mix(c, FOOT, pk.smooth(0.15, 0.03, co.z))
    for sx in (1, -1):
        c = pk.mix(c, EMBER, pk.smooth(0.2, 0.05, (co - Vector((sx * 0.34, -1.06, 1.6))).length) * 0.75)
    return c


def model(k):
    E = [
        ("ell", (0, 0.35, 0.82), (0.56, 0.74, 0.52)),
        ("ell", (0, -0.12, 0.92), (0.50, 0.44, 0.50)),
        ("cap", (0, -0.22, 1.12), (0, -0.52, 1.50), 0.25),
        ("box", (0, -0.72, 1.72), (0.43, 0.45, 0.39), 0.30),
        ("ell", (0, -1.12, 1.60), (0.31, 0.30, 0.25)),
        ("ell", (0.21, -0.97, 1.89), (0.15, 0.13, 0.08)),
        ("ell", (-0.21, -0.97, 1.89), (0.15, 0.13, 0.08)),
        ("cap", (0, 1.00, 0.78), (0, 1.45, 0.58), 0.21),
        ("cap", (0, 1.45, 0.58), (0, 1.90, 0.48), 0.15),
        ("cap", (0, 1.90, 0.48), (0, 2.25, 0.54), 0.10),
    ]
    for sx in (1, -1):
        E += [("cap", (sx * 0.36, -0.16, 0.56), (sx * 0.38, -0.20, 0.13), 0.17),
              ("ell", (sx * 0.38, -0.27, 0.09), (0.17, 0.21, 0.10)),
              ("ell", (sx * 0.40, 0.78, 0.62), (0.26, 0.30, 0.32)),
              ("cap", (sx * 0.42, 0.80, 0.45), (sx * 0.42, 0.80, 0.13), 0.18),
              ("ell", (sx * 0.42, 0.73, 0.09), (0.18, 0.22, 0.10))]
    k.body(E, body_color, tris=5600)

    k.eyes([((0.55, -2.6, 1.86), (0.2, -0.7, 1.8)), ((-0.55, -2.6, 1.86), (-0.2, -0.7, 1.8))],
           size=(0.14, 0.165), style="fierce", iris=(255, 168, 30), lid=TOP, lid_tilt=22)

    def face(bm, L):
        for sx in (1, -1):
            loc, n = k.surf((sx * 0.11, -2.4, 1.84), (sx * 0.09, -1.0, 1.58))
            pk.ellipsoid(bm, L, loc - n * 0.012, (0.045, 0.03, 0.022), NOSE, x_axis=(1, 0, 0), z_axis=n)
            loc, n = k.surf((sx * 0.14, -2.2, 1.44), (sx * 0.12, -1.0, 1.56))
            pk.cone(bm, L, loc + Vector((0, 0.02, 0.02)), (0, -0.25, -1), 0.11, 0.038, IVORY)
    k.part("Face", face, "Head")

    def horns(bm, L):
        for sx in (1, -1):
            loc, n = k.surf((sx * 0.42, -0.48, 2.6), (sx * 0.14, -0.70, 1.7))
            pk.cone(bm, L, loc - n * 0.04, (sx * 0.34, 0.6, 0.62), 0.62, 0.095,
                    lambda t, a: pk.mix(HORN, HORN_TIP, pk.smooth(0.45, 1.0, t)), bend_axis=(1, 0, 0), bend_deg=-58,
                    sides=10, n=9)
            for j, (dy, dz) in enumerate(((-0.05, 0.05), (0.12, -0.12))):
                loc, n = k.surf((sx * 0.9, -0.5 + dy, 1.72 + dz), (0, -0.62 + dy, 1.72 + dz))
                pk.cone(bm, L, loc - n * 0.02, (sx * 0.65, 0.65, 0.12 - j * 0.15), 0.22 - j * 0.05, 0.06,
                        lambda t, a: pk.mix(SPIKE, SPIKE_TIP, t), sides=8, n=5)
    k.part("Horns", horns, "Head")

    def spikes(bm, L):
        N = 12
        for i in range(N):
            t = i / (N - 1)
            y = -0.32 + t * 2.38
            try:
                loc, n = k.surf((0, y, 3.0), (0, y, 0.0))
            except RuntimeError:
                continue
            h = 0.22 * (1 - 0.55 * t) + 0.05
            d = (n + Vector((0, 0.75, 0))).normalized()
            pk.cone(bm, L, loc - n * 0.03, d, h, h * 0.42, lambda tt, a: pk.mix(SPIKE, SPIKE_TIP, pk.smooth(0.3, 1, tt)),
                    sides=6, n=4)
    k.part("Spikes", spikes, chain_w)

    def claws(bm, L):
        for sx in (1, -1):
            for dx in (-0.08, 0.0, 0.08):
                pk.cone(bm, L, (sx * 0.38 + dx, -0.44, 0.06), (0, -1, -0.35), 0.08, 0.032, IVORY, sides=6, n=4)
                pk.cone(bm, L, (sx * 0.42 + dx, 0.52, 0.06), (0, -1, -0.35), 0.08, 0.032, IVORY, sides=6, n=4)

    def claw_w(co):
        side = "L" if co.x > 0 else "R"
        return {("Leg_F" if co.y < 0.2 else "Leg_B") + side: 1.0}
    k.part("Claws", claws, claw_w)

    for side, sx in (("L", 1), ("R", -1)):
        S, _ = k.surf((sx * 0.95, 0.10, 1.55), (0, 0.10, 0.95))
        S = S - Vector((sx * 0.03, 0, 0.03))
        W = S + Vector((sx * 0.70, 0.20, 0.66))
        tips = [W + Vector((sx * 0.78, 0.26, 0.30)), W + Vector((sx * 0.72, 0.70, -0.20)),
                W + Vector((sx * 0.30, 0.95, -0.58))]
        B = Vector((sx * 0.34, 0.92, 1.02))
        pk.membrane_wing(k, side, S, W, tips, B, "Wing_" + side, "WingTip_" + side, MEM_ROOT, MEM_EDGE, WBONE,
                         claw=IVORY)
        k.J_wing = getattr(k, "J_wing", {})
        k.J_wing[side] = (S, W)

    tail_tip = Vector((0, 2.30, 0.58))

    def flame_outer(bm, L):
        pk.blob(bm, L, pk.frame(tail_tip + Vector((0, 0.02, 0.13)), (1, 0, 0), (0, 0.25, 1)),
                lambda u: Vector((u.x * 0.13 * (1 - 0.45 * max(u.z, 0)), u.y * 0.13 * (1 - 0.45 * max(u.z, 0)),
                                  u.z * 0.22 + 0.08 * max(u.z, 0) ** 3)), pk.lin((255, 122, 30)), 12, 8)
        # breath flame hidden inside the head (slides out of the snout during the roar)
        pk.ellipsoid(bm, L, (0, -0.86, 1.62), (0.13, 0.25, 0.12), pk.lin((255, 122, 30)))

    def flame_inner(bm, L):
        pk.ellipsoid(bm, L, tail_tip + Vector((0, 0.0, 0.11)), (0.07, 0.07, 0.13), pk.lin((255, 220, 80)))
        pk.ellipsoid(bm, L, (0, -0.92, 1.62), (0.07, 0.16, 0.07), pk.lin((255, 220, 80)))

    def flame_w(co):
        return {"Breath": 1.0} if co.y < 0 else {"Flame": 1.0}
    pk.glow_part(k, "Glow_FlameO", FLAME_O, flame_outer, flame_w)
    pk.glow_part(k, "Glow_FlameY", FLAME_Y, flame_inner, flame_w)


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
        k.joint("Leg_F" + side, (sx * 0.37, -0.17, 0.50), "Spine", tail=(0, 0, -0.45))
        k.joint("Leg_B" + side, (sx * 0.42, 0.78, 0.52), "Spine", tail=(0, 0, -0.45))
        S, W = k.J_wing[side]
        k.joint("Wing_" + side, S, "Spine")
        k.joint("WingTip_" + side, W, "Wing_" + side, tail=(Vector((sx * 0.5, 0.4, 0.0))))
    k.body_bones = ["Spine", "Neck", "Head", "Tail1", "Tail2", "Tail3", "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]


# ------------------------------------------------------------------ animation
LEGS = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]


def wings(k, f, up, fwd, tip_up=0.0, tip_fwd=0.0, twist=0.0, asym=0.0):
    for side, sx in (("L", 1), ("R", -1)):
        a = 1 + asym * sx
        k.key("Wing_" + side, f, rot=(twist, -sx * fwd * a, -sx * up * a))
        k.key("WingTip_" + side, f, rot=(0, -sx * tip_fwd, -sx * tip_up))


FOLD = dict(up=-22, fwd=-34, tip_up=-30, tip_fwd=-40)  # wings folded along the back


def tail(k, f, n, yaw_amp, pitch=4.0, phase=0.0, cycles=1, pitch_amp=0.0):
    for i, b in enumerate(("Tail1", "Tail2", "Tail3")):
        lag = phase - 0.1 * i
        k.key(b, f, rot=(pitch + pitch_amp * pk.wave(f, n, lag, cycles), yaw_amp * (1 + 0.45 * i) * pk.wave(f, n, lag, cycles), 0))


def flame(k, f, n):
    """Flicker that repeats exactly over the clip length (loops stay seamless)."""
    c = max(1, round(n / 8))
    k.key("Flame", f, rot=(5 * pk.wave(f, n, 0.0, c), 6 * pk.wave(f, n, 0.3, c + 1), 7 * pk.wave(f, n, 0.6, c + 2)),
          loc=(0, 0, 0.025 * pk.wave(f, n, 0.2, c)))


def plant_pass(k, n, step=1):
    k.bake_bezier_now()
    import bpy
    for f in range(0, n + 1, step):
        bpy.context.scene.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


def idle(k):
    n = 60
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s, c = pk.wave(f, n), pk.cwave(f, n)
        k.key("Spine", f, rot=(-2.0 - 1.2 * s, 0, 1.0 * pk.wave(f, n, 0.3)), loc=(0, 0, 0.016 * (1 + s) / 2))
        # proud look-around: right, back, left, back (chin up)
        look = 18 * pk.wave(f, n, 0.0) * abs(pk.wave(f, n, 0.0)) ** 0.3
        k.key("Neck", f, rot=(-6 + 2 * c, look * 0.45, 0))
        k.key("Head", f, rot=(-5 + 3 * pk.wave(f, n, 0.15, 2), look * 0.55, -4 * pk.wave(f, n, 0.1)))
        wings(k, f, FOLD["up"] + 4 * pk.wave(f, n, 0.2), FOLD["fwd"] + 3 * c, FOLD["tip_up"], FOLD["tip_fwd"])
        tail(k, f, n, 10, pitch=6, phase=0.05, pitch_amp=3)
        k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
    for f in range(0, n + 1, 2):
        flame(k, f, n)
    plant_pass(k, n)
    k.finish()
    k.meta["planted"] = LEGS


def walk(k):
    n = 24

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.5 * pk.wave(f, n, 0, 2), 3 * pk.wave(f, n, 0.1), 2.5 * pk.wave(f, n)), loc=(0, 0, 0.035 * b))
        k.key("Neck", f, rot=(-5 - 2 * pk.wave(f, n, 0.1, 2), -2 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(-3 - 2.5 * pk.wave(f, n, 0.15, 2), -2.5 * pk.wave(f, n, 0.1), -2 * pk.wave(f, n, 0.05)))
        wings(k, f, FOLD["up"] + 3 * pk.wave(f, n, 0.1, 2), FOLD["fwd"], FOLD["tip_up"], FOLD["tip_fwd"])
        tail(k, f, n, 12, pitch=8, phase=0.2)
        k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
        flame(k, f, n)
    k.meta["legs"] = [("Leg_FL", 0.0), ("Leg_BR", 0.0), ("Leg_FR", 0.5), ("Leg_BL", 0.5)]
    stride = pk.walk_cycle(k, n, k.meta["legs"], 0.47 * math.sin(math.radians(22)), 0.12, body)
    return stride


FLY_N = 20


def fly_pose(k, f, n=FLY_N, key_legs=True):
    """Real flight: body pitched nose-down, head up to look ahead, legs tucked back, big strokes that sweep the
    wings forward/inward on the downstroke and fold the tips on the upstroke, tail streaming + waving."""
    ph = f / n
    flap = math.cos(2 * math.pi * ph)            # +1 top of stroke (f0), -1 bottom (f n/2)
    down = math.sin(2 * math.pi * ph)            # > 0 during the downstroke
    lag = math.cos(2 * math.pi * (ph - 0.13))
    rise = -math.sin(2 * math.pi * (ph - 0.05))  # body rises while the wings push down
    k.key("Spine", f, rot=(20 + 2.5 * flap, 0, 0), loc=(0, 0, 0.09 * (-rise)))
    k.key("Neck", f, rot=(-15 - 2 * lag, 0, 0))
    k.key("Head", f, rot=(-12 + 2 * lag, 0, 0))
    wings(k, f, up=-2 + 58 * flap, fwd=14 * down - 4, tip_up=-6 + 30 * lag + 12 * max(0, -down),
          tip_fwd=-14 * max(0, -down) + 6 * down, twist=8 * down)
    if key_legs:
        for leg, base in (("Leg_FL", 62), ("Leg_FR", 62), ("Leg_BL", 78), ("Leg_BR", 78)):
            k.key(leg, f, rot=(base + 6 * lag, 0, 0), loc=(0, 0, 0.06))
    for i, b in enumerate(("Tail1", "Tail2", "Tail3")):
        k.key(b, f, rot=(10 + 7 * math.sin(2 * math.pi * (ph - 0.12 * (i + 1))), 3 * math.sin(2 * math.pi * (ph * 1 - 0.2 * i)), 0))
    k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
    flame(k, f, n)


def fly(k):
    n = FLY_N
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, n)
    k.finish()


def takeoff(k):
    n = 27
    k.new_action("takeoff", n, False)
    import bpy
    # 0-10: crouch (anticipation, wings lifted high), 11 launch (big downstroke + leg push), 27 = fly at phase 0.45
    P = [(0, 0.0, -2, FOLD["up"], FOLD["fwd"], FOLD["tip_up"], FOLD["tip_fwd"]),
         (6, -0.10, -7, 30, -12, 10, -10),
         (10, -0.13, -9, 62, -6, 24, -4),
         (13, 0.22, 10, -30, 12, -8, 6),
         (17, 0.34, 14, 20, 0, 18, -6)]
    for f, z, p, up, fwd, tu, tf in P:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(-8 - p * 0.5, 0, 0))
        k.key("Head", f, rot=(-6, 0, 0))
        wings(k, f, up, fwd, tu, tf)
        tail(k, f, n, 0, pitch=6 + p * 0.4)
        k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
        flame(k, f, n)
    fly_pose(k, n, FLY_N, key_legs=False)  # ends exactly at the fly clip's phase 0.45 pose
    k.key("Spine", n, rot=None, loc=(0, 0, 0.09 * math.sin(2 * math.pi * (0.45 - 0.05))))
    k.bake_bezier_now()
    for f in range(0, 12):
        bpy.context.scene.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f, a_f, a_b in ((14, 30, 40), (20, 55, 70), (n, 62, 78)):
        for leg in LEGS:
            k.key(leg, f, rot=(a_f if "F" in leg[4] else a_b, 0, 0), loc=(0, 0, 0.06 if f == n else 0.0))
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    n = 27
    k.new_action("land", n, False)
    import bpy
    fly_pose(k, 0, FLY_N)
    P = [(7, 0.10, -16, 34, -26, 24, -18),   # flare: nose up, wings forward + up (air brake), legs reach
         (12, 0.06, -10, -12, -14, 4, -6),   # braking downstroke
         (16, -0.09, 5, 10, -8, -10, -14),   # touch-down (feet on the ground), absorb
         (21, 0.02, -1, -10, -26, -20, -30),
         (27, 0.0, -2, FOLD["up"], FOLD["fwd"], FOLD["tip_up"], FOLD["tip_fwd"])]
    for f, z, p, up, fwd, tu, tf in P:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(-6 - p * 0.4, 0, 0))
        k.key("Head", f, rot=(-5, 0, 0))
        wings(k, f, up, fwd, tu, tf)
        tail(k, f, n, 0, pitch=6 - p * 0.3)
        k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
        flame(k, f, n)
    for leg in LEGS:
        k.key(leg, 7, rot=(-22 if "F" in leg[4] else -8, 0, 0), loc=(0, 0, 0))
    k.bake_bezier_now()
    for f in range(16, n + 1):
        bpy.context.scene.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(16 / n, 3)}


def roar(k):
    """Rear back, then lunge with a puff of fire from the snout (the hidden Breath flame slides out)."""
    n = 45
    k.new_action("roar", n, False)
    P = [(0, 0, 0, 0, 0, FOLD["up"], FOLD["fwd"]),
         (11, -12, -22, -16, 0.0, 34, -10),
         (18, 7, 18, 10, -0.70, 46, 6),
         (30, 5, 14, 8, -0.74, 40, 4),
         (37, 0, 0, 0, -0.1, 4, -18),
         (45, 0, 0, 0, 0.0, FOLD["up"], FOLD["fwd"])]
    for f, sp, nk, hd, br, up, fwd in P:
        k.key("Spine", f, rot=(sp - 2, 0, 0), loc=(0, 0, 0.02 * (sp < 0)))
        k.key("Neck", f, rot=(nk - 6, 0, 0))
        k.key("Head", f, rot=(hd - 5, 0, 0))
        k.key("Breath", f, rot=(0, 0, 0), loc=(0, br, 0.04 * (br < 0)))
        wings(k, f, up, fwd, FOLD["tip_up"] * (0.2 if up > 0 else 1), FOLD["tip_fwd"] * (0.2 if up > 0 else 1))
        tail(k, f, n, 0, pitch=6 - sp * 0.6)
    for f in range(0, n + 1, 2):
        flame(k, f, n)
    plant_pass(k, n)
    k.finish(loop=False)


def stretch(k):
    """act: a big proud wing stretch with a tail curl."""
    n = 42
    k.new_action("act_stretch", n, False)
    P = [(0, FOLD["up"], FOLD["fwd"], FOLD["tip_up"], FOLD["tip_fwd"], 0),
         (12, 58, 4, 26, 6, -6),
         (24, 62, 8, 30, 10, -8),
         (34, 10, -20, -12, -24, -2),
         (42, FOLD["up"], FOLD["fwd"], FOLD["tip_up"], FOLD["tip_fwd"], 0)]
    for f, up, fwd, tu, tf, sp in P:
        k.key("Spine", f, rot=(sp - 2, 0, 0))
        k.key("Neck", f, rot=(-6 + sp, 0, 0))
        k.key("Head", f, rot=(-5 + sp * 0.5, 0, 4 * (f in (12, 24))))
        wings(k, f, up, fwd, tu, tf)
        k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
        tail(k, f, n, 14 * (f in (12, 24)), pitch=6 + 10 * (f in (12, 24)), phase=0.25)
    for f in range(0, n + 1, 2):
        flame(k, f, n)
    plant_pass(k, n)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    stretch(k)
    return stride
