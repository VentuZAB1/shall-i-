# Black Eastern Dragon (Void egg #3): a long lung dragon rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass): a 12-ring
# ink-indigo serpent tube (D tapering 1.0 -> 0.35) arched in a side-view S, lilac belly bands, diamond scale plates,
# a violet flame-blade mane from the head to the tail tip, 4 short sturdy legs with 3 gold talons each, a big
# eastern head (1.8 D wide, 2.4 D long) with an open jaw and 4 fangs, fierce gold slit eyes under heavy gold brows,
# gold antlers (1 branch each) and 2 thick drooping gold whiskers - and its treasure, a pearl floating by its cheek.
# FLIES WITHOUT WINGS (Motion = Fly): the whole body swims through the air in waves while the legs paddle.
# Own moves: idle = slow serpentine sway, plays with its pearl (nudges it with the snout, it drifts back); walk = lizard
# trot with the body snaking; fly / takeoff / land = wave-swimming flight; roar = rears the front up, neck high, jaw
# wide, tail curling; signature = COIL & PEARL (lies down and curls its body into a ring around the pearl, raises the
# pearl high, uncoils).
import math
from mathutils import Vector, Euler, Matrix

DISPLAY = "Black Eastern Dragon"
MOTION = "Fly"
RIG = "serpent"
HEIGHT = 9.0

INK = (46, 38, 74)            # ink-indigo base (V 29 %: the bible's dark-pet floor)
SNOUT = (64, 54, 100)         # a step lighter on the snout top (reads as a muzzle, not a black hole)
LILAC = (132, 112, 184)       # belly bands, lips, chin
DARK = (18, 14, 30)           # paws, nostrils
GOLD = (255, 200, 70)         # antlers, whiskers, talons, brows
MANE = (160, 96, 255)
MANE_L = (220, 170, 255)
PEARL = (236, 226, 255)
PEARL_C = (196, 150, 255)
IRIS = (255, 200, 60)
MOUTH = (120, 30, 60)
TONGUE = (236, 110, 140)
FANG = (246, 244, 250)

D = 0.44                                           # tube diameter at the chest
# 13 centre-line points (12 rings): low at the front legs, arched over the middle, low at the hind legs, tail rising
_ZS = (0.60, 0.54, 0.62, 0.80, 0.86, 0.70, 0.54, 0.56, 0.64, 0.76, 0.88, 1.00, 1.10)
PTS = [Vector((0, -0.30 + 0.20 * i, _ZS[i])) for i in range(13)]
RAD = [D / 2 * (1 - 0.65 * i / 12) for i in range(13)]
CHAIN = ["Spine", "Body1", "Body2", "Tail1", "Tail2", "Tail3"]
BODY = [PTS[2 * i] for i in range(7)]               # bone joints (2 rings per bone)
WIDTH = [RAD[2 * i] for i in range(6)]
LEGS = {"FL": ((0.10, -0.12, 0.52), (0.30, -0.22, 0.30), (0.26, -0.12, 0.11)),
        "BL": ((0.08, 0.84, 0.52), (0.27, 0.94, 0.30), (0.22, 0.84, 0.11))}
NECK = [Vector((0, -0.30, 0.60)), Vector((0, -0.50, 0.76)), Vector((0, -0.70, 0.94))]
HC = Vector((0, -0.96, 1.08))                      # cranium centre: HW 0.80 (1.8 D), HH 0.62 (1.4 D)
PEARL_P = Vector((0.66, -1.30, 1.30))


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def frame(z, x):
    z = Vector(z).normalized()
    x = Vector(x)
    x = (x - z * x.dot(z)).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


def blade(B, base, up, back, h, w, t, color, bone, tip_c=None):
    """a flame blade standing on a surface (up = surface normal), base length along `back`, tip swept back"""
    up = Vector(up).normalized()
    back = Vector(back)
    back = (back - up * back.dot(up)).normalized()
    R = Matrix((up.cross(back), back, up)).transposed()      # local x = side, y = back, z = up
    B.add(base + up * (h / 2), (t, w, h / 2), color, bone, R=R, top=(0.45, 0.2), top_shift=(0, w * 0.9),
          studs=[], role="limb")
    if tip_c:
        B.add(base + up * (h * 0.80) + back * (w * 0.75), (t + 0.006, w * 0.5, h * 0.2), tip_c, bone, R=R,
              top=(0.5, 0.2), top_shift=(0, w * 0.3), studs=[], role="limb")


def model(k):
    """STYLE_BIBLE BlackDragon (T5 Void top, eastern serpent flyer): 12 tapered rings arched in an S (amplitude 0.6 D)
    with lilac belly bands and diamond scale plates, a violet flame-blade mane (2 tones) from the poll to the tail tip,
    4 short sturdy legs (0.7 D, elbows out) with dark paws and 3 gold talons, a 1.8 D x 2.4 D eastern head with an
    open jaw and 4 fangs, fierce gold slit eyes (light rim, glint on the pupil) under heavy gold brows, gold antlers
    (beam 0.18 D, 1 branch), 2 thick drooping 3-segment gold whiskers, the pearl by the cheek. No glow (wisps = VFX)."""
    import blockkit as bk
    B = bk.Blocks(k, seed=149, tier=5, th=0.52)          # plate cell 0.22 D (rings are short: 0.30 D gave none)
    # ---- the tube: 12 rounded rings (2 per chain bone), each with a lilac belly band and a mane blade on top
    for i in range(12):
        bone = CHAIN[i // 2]
        a, b = PTS[i], PTS[i + 1]
        r0, r1 = RAD[i], RAD[i + 1]
        ring = B.seg(a, b, r0, r0, INK, bone, side=(1, 0, 0), ext=0.035, ext1=0.035, top=(r1 / r0, r1 / r0),
                     pvar="diamond", density=0.62, role="mass" if i < 8 else "limb")
        d = (b - a).normalized()
        down = Vector((0, d.z, -d.y)).normalized()
        if down.z > 0:
            down = -down
        rm = (r0 + r1) / 2
        B.seg(a + down * (rm * 0.66), b + down * (rm * 0.66), rm * 1.03, rm * 0.40, LILAC, bone, side=(1, 0, 0),
              studs=[], role="limb", top=(r1 / r0, 1))
        up = -down
        blade(B, a.lerp(b, 0.40) + up * (rm * 0.80), up, d, rm * 1.05, rm * 0.80, rm * 0.32,
              MANE if i % 2 == 0 else MANE_L, bone, tip_c=MANE_L if i % 2 == 0 else None)
    # tail tip: a flat violet flame fan (3 blades) ending in a point
    tip = PTS[12]
    for dv, ln, w, c in (((0, 1, 0.25), 0.34, 0.16, MANE), ((0, 0.75, 0.75), 0.26, 0.12, MANE_L),
                         ((0, 0.8, -0.45), 0.24, 0.11, MANE_L)):
        dv = Vector(dv).normalized()
        B.add(tip + dv * (ln / 2), (0.035, w / 2, ln / 2), c, "Tail3", R=frame(dv, (1, 0, 0)), top=(1.0, 0.12),
              studs=[], role="limb")
    # ---- neck: 2 rings from the chest up into the back of the head, lilac throat, mane blades
    for j in range(2):
        a, b = NECK[j], NECK[j + 1]
        B.seg(a, b, 0.225, 0.225, INK, "Neck", side=(1, 0, 0), ext=0.0 if j == 0 else 0.05, ext1=0.05, pvar="diamond",
              density=0.62)
        d = (b - a).normalized()
        down = Vector((0, d.z, -d.y))
        if down.z > 0:
            down = -down
        B.seg(a + down * 0.15, b + down * 0.15, 0.232, 0.09, LILAC, "Neck", side=(1, 0, 0), studs=[], role="limb")
        blade(B, a.lerp(b, 0.5) - down * 0.17, -down, -d, 0.27, 0.13, 0.065, MANE_L if j else MANE, "Neck",
              tip_c=MANE_L if j == 0 else None)
    # ---- head: cranium (faces -y) + long snout + open lower jaw
    head = B.add(HC, (0.40, 0.25, 0.31), INK, "Head", top=(0.92, 0.92), density=0.62, studs=["+x", "-x", "+z", "+y"])
    snout = B.add(HC + Vector((0, -0.36, -0.15)), (0.25, 0.30, 0.15), SNOUT, "Head", top=(0.88, 0.92), role="limb",
                  studs=["+z"], density=0.5)
    # lilac upper lip band, flared nostrils (raised knobs with dark holes) and a sheen on the snout top
    B.add(HC + Vector((0, -0.38, -0.285)), (0.255, 0.29, 0.03), LILAC, "Head", studs=[], role="limb")
    for s in (1, -1):
        knob = B.add(HC + Vector((s * 0.15, -0.58, 0.005)), (0.075, 0.07, 0.05), SNOUT, "Head", studs=[], role="limb")
        B.add(knob.world((0, -0.072, 0.0)), (0.04, 0.006, 0.028), DARK, "Head", rot=(0, s * 20, 0), studs=[],
              bevel=0.008)
    # mouth: dark roof, 2 upper fangs at the snout front
    B.add(HC + Vector((0, -0.37, -0.318)), (0.21, 0.26, 0.006), MOUTH, "Head", studs=[], bevel=0.004)
    for s in (1, -1):
        B.spike(HC + Vector((s * 0.15, -0.60, -0.30)), (0, -0.1, -1), 0.11, 0.033, FANG, "Head")
    # lower jaw (Jaw bone), open 16 deg at rest: lilac chin, red mouth, pink tongue, 2 lower fangs
    JR = Euler((math.radians(16), 0, 0), "XYZ").to_matrix()
    JP = HC + Vector((0, -0.12, -0.33))
    def jp(p):
        return JP + JR @ Vector(p)
    B.add(jp((0, -0.24, -0.06)), (0.21, 0.27, 0.06), INK, "Jaw", R=JR, bot=(0.8, 0.85), role="limb", studs=[])
    B.add(jp((0, -0.24, -0.115)), (0.17, 0.24, 0.012), LILAC, "Jaw", R=JR, studs=[], bevel=0.008)
    B.add(jp((0, -0.22, 0.002)), (0.17, 0.23, 0.005), MOUTH, "Jaw", R=JR, studs=[], bevel=0.004)
    B.add(jp((0, -0.20, 0.008)), (0.09, 0.16, 0.005), TONGUE, "Jaw", R=JR, studs=[], bevel=0.004)
    for s in (1, -1):
        B.spike(jp((s * 0.13, -0.44, 0.0)), JR @ Vector((0, 0.1, 1)), 0.09, 0.03, FANG, "Jaw")
    # fierce gold slit eyes (light rim on the dark face, glint on the pupil) under heavy gold brows
    B.face_eyes(head, "fierce", IRIS, base=INK, brow=GOLD, look=(0, 0.5), pupil_size=(0.05, 0.09),
                hl_size=(0.06, 0.0), hl_on_pupil=True, brow_spec=(0.32, 0.08, 20))
    # gold antlers: thick beam curving up and back in 3 segments + 1 forward branch, pointed tips
    for s in (1, -1):
        a0 = HC + Vector((s * 0.22, 0.10, 0.27))
        a1 = a0 + Vector((s * 0.10, 0.04, 0.24))
        a2 = a1 + Vector((s * 0.06, 0.16, 0.16))
        a3 = a2 + Vector((s * 0.02, 0.20, 0.04))
        for p, q, w in ((a0, a1, 0.052), (a1, a2, 0.046), (a2, a3, 0.040)):
            B.seg(p, q, w, w, GOLD, "Head", ext=0.035, studs=[], role="limb")
        B.spike(a3, a3 - a2, 0.12, 0.038, GOLD, "Head")
        B.spike(a1, (s * 0.25, -0.45, 0.85), 0.18, 0.040, GOLD, "Head")
    # 2 thick drooping 3-segment gold whiskers from the snout sides
    for s in (1, -1):
        w = [HC + Vector((s * 0.22, -0.52, -0.12)), HC + Vector((s * 0.38, -0.48, -0.22)),
             HC + Vector((s * 0.50, -0.36, -0.38)), HC + Vector((s * 0.56, -0.22, -0.56))]
        for j, (p, q) in enumerate(zip(w, w[1:])):
            B.seg(p, q, 0.036 - 0.006 * j, 0.036 - 0.006 * j, GOLD, "Head", ext=0.025, studs=[], role="limb")
        B.spike(w[3], w[3] - w[2], 0.07, 0.022, GOLD, "Head")
    # cheek frills: 3 violet blades per side fanned back from the back edge of the head (extend the silhouette)
    for s in (1, -1):
        for z, dz, L, c in ((-0.18, -0.50, 0.24, MANE), (-0.04, -0.10, 0.30, MANE_L), (0.10, 0.30, 0.22, MANE)):
            root = HC + Vector((s * 0.37, 0.14, z))
            d = Vector((s * 0.60, 0.70, dz)).normalized()
            B.seg(root, root + d * L, 0.085, 0.04, c, "Head", side=(0, 0, 1), ext=0.06, top=(0.15, 0.5), studs=[],
                  role="limb")
    # head mane: 3 blades fanned back from the poll between the antlers
    for x, ln in ((0.0, 0.30), (-0.13, 0.24), (0.13, 0.24)):
        blade(B, HC + Vector((x, 0.16, 0.27)), (x * 1.5, 0.55, 0.85), (0, 1, -0.3), ln, 0.11, 0.06, MANE, "Head",
              tip_c=MANE_L)
    # ---- legs: sturdy upper leg (elbow out), shin, dark paw with 3 gold talons
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            hw = 0.095 if fb == "F" else 0.088
            B.seg(H, K, hw, hw * 1.05, INK, leg, ext=0.03, ext1=0.05, side=(0, 1, 0), density=0.62)
            B.seg(K, A, hw * 0.88, hw * 0.92, INK, shin, ext=0.05, ext1=0.02, side=(0, 1, 0), density=0.62)
            B.add(A + Vector((0, -0.03, -0.065)), (hw * 1.2, hw * 1.3, 0.05), DARK, foot, studs=[], role="limb")
            for dx in (-0.065, 0.0, 0.065):
                B.spike(A + Vector((dx, -0.03 - hw * 1.3, -0.085)), (0, -1, -0.5), 0.10, 0.028, GOLD, foot,
                        top=(0.15, 0.15))
    # ---- the pearl (own bone): a rounded pearl with a single lilac core cube
    B.add(PEARL_P, (0.12, 0.12, 0.12), PEARL, "Pearl", studs=[], bevel=0.054, rnd=0.45, role="limb")
    B.add(PEARL_P + Vector((0, -0.105, 0.01)), (0.045, 0.03, 0.045), PEARL_C, "Pearl", rot=(0, 45, 0), studs=[],
          bevel=0.01)
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", tuple(BODY[0]), "Root", tail=tuple(BODY[1] - BODY[0]))
    for i in range(1, len(CHAIN)):
        k.joint(CHAIN[i], tuple(BODY[i]), CHAIN[i - 1], tail=tuple(BODY[i + 1] - BODY[i]))
    k.joint("Neck", tuple(NECK[0]), "Spine", tail=tuple(NECK[2] - NECK[0]))
    k.joint("Head", tuple(HC + Vector((0, 0.20, -0.22))), "Neck", tail=(0, -0.4, 0))       # throat pivot
    k.joint("Jaw", tuple(HC + Vector((0, -0.12, -0.33))), "Head", tail=(0, -0.3, 0))
    k.joint("Pearl", tuple(PEARL_P), "Spine", tail=(0, 0, 0.2))
    for s, side in ((1, "L"), (-1, "R")):
        for fb, parent, knee in (("F", "Spine", (s * 0.6, -0.8, 0)), ("B", "Body2", (s * 0.6, 0.8, 0))):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.2, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]


def waves(k, f, n, pitch=0.0, yaw=0.0, phase=0.0, cycles=1, lag=0.14, base=None, start=0):
    """travelling wave down the body chain (pitch = vertical swim waves, yaw = side-to-side snaking)"""
    for i, bn in enumerate(CHAIN[start:], start):
        ph = phase - lag * i
        b = base[i] if base else (0, 0)
        k.key(bn, f, rot=(b[0] + pitch * math.sin(2 * math.pi * (cycles * f / n + ph)),
                          b[1] + yaw * math.sin(2 * math.pi * (cycles * f / n + ph)), 0))


def pearl(k, f, p=(0, 0, 0)):
    k.key("Pearl", f, rot=(0, 0, 0), loc=p)


def legs_fk(k, f, front=0.0, hind=0.0, paddle=0.0, ph=0.0):
    """flight: legs swept back along the body, paddling (paddle = stroke size)"""
    for leg in LEGS4:
        fr = leg[4] == "F"
        side = leg[5:]
        s = 1 if side.endswith("L") else -1
        w = math.sin(2 * math.pi * (ph + (0.0 if fr else 0.5) + (0.0 if s > 0 else 0.25)))
        base = front if fr else hind
        k.key(leg, f, rot=(base + paddle * w, 0, -s * 10))
        k.key("Shin_" + side, f, rot=(30 + 0.6 * paddle * w, 0, 0))
        k.key("Foot_" + side, f, rot=(30, 0, 0))


def idle(k):
    """slow serpentine sway (a lazy side wave down the body), breathing, head follows its pearl: the pearl drifts away,
    the dragon nudges it back with its snout twice; the tail tip curls."""
    n = 144
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        waves(k, f, n, pitch=1.2, yaw=4.0, cycles=2, lag=0.12)
        k.key("Spine", f, rot=(1.2 * pk.wave(f, n, 0, 2), 4 * pk.wave(f, n, 0, 2), 0), loc=(0, 0, 0.01 * b))
    for f, px, py, pz, nk, hy, h, jw in ((0, 0, 0, 0, 0, 0, 0, 0), (20, 0.10, -0.04, 0.06, 0, 4, 0, 0),
                                         (40, 0.30, -0.14, 0.10, 0, 18, -4, 0), (52, 0.30, -0.14, 0.10, 6, 26, 6, 6),
                                         (56, 0.08, -0.02, 0.0, 4, 16, 2, 0), (76, 0.02, 0.0, 0.04, 0, 6, 0, 0),
                                         (96, -0.10, -0.20, 0.12, 0, -4, -6, 0), (108, -0.10, -0.20, 0.12, 8, 8, 8, 6),
                                         (112, 0.06, 0.0, 0.02, 4, 6, 2, 0), (130, 0, 0, 0, 0, 0, 0, 0), (n, 0, 0, 0, 0, 0, 0, 0)):
        pearl(k, f, (px, py, pz + 0.03 * math.sin(2 * math.pi * f / 24)))
        k.key("Neck", f, rot=(nk, hy * 0.4, 0))
        k.key("Head", f, rot=(h, hy * 0.6, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    """lizard trot: diagonal pairs, the long body snakes side to side, head steady, tail swinging."""
    n = 28

    def body(f):
        waves(k, f, n, pitch=0.8, yaw=7.0, cycles=1, lag=0.16)
        k.key("Spine", f, rot=(0, 5 * pk.wave(f, n, 0.0), 2 * pk.wave(f, n, 0.0)), loc=(0, 0, -0.02 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        k.key("Neck", f, rot=(0, -4 * pk.wave(f, n, 0.0), 0))
        k.key("Head", f, rot=(0, -2 * pk.wave(f, n, 0.0), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        pearl(k, f, (0, 0, 0.03 * pk.wave(f, n, 0, 2)))
    return cm.quad_walk(k, n, 0.16, 0.10, body, gait="trot")


FLY_N = 36
COIL_C = 40.0
COIL_RC = (-0.076, 1.352, -0.66)      # measured with the ring probe at act_coil f60 (C 40)


def fly_pose(k, f, n=FLY_N):
    """swimming flight: vertical waves travel from the chest to the tail tip, the head stays level, legs paddle"""
    u = f / n
    waves(k, f, n, pitch=9.0, yaw=3.0, cycles=1, lag=0.16, base=[(-4, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0)], start=1)
    k.key("Spine", f, rot=(-4 + 6 * math.sin(2 * math.pi * u), 0, 0), loc=(0, 0, 0.06 * math.sin(2 * math.pi * (u - 0.1))))
    k.key("Neck", f, rot=(10 - 6 * math.sin(2 * math.pi * (u - 0.08)), 0, 0))
    k.key("Head", f, rot=(-2, 0, 0))
    k.key("Jaw", f, rot=(4, 0, 0))
    legs_fk(k, f, front=40, hind=60, paddle=22, ph=u)
    pearl(k, f, (0.02, -0.04, 0.04 * math.sin(2 * math.pi * u)))


def fly(k):
    k.new_action("fly", FLY_N, True)
    for f in range(0, FLY_N + 1):
        fly_pose(k, f)
    k.finish()


def takeoff(k):
    """crouches low, springs up off all four legs (launch at frame 11), the body whips into the swimming wave."""
    import bpy
    n = 27
    k.new_action("takeoff", n, False)
    for f, z, p in ((0, 0, 0), (6, -0.14, 4), (10, -0.18, 6), (13, 0.22, -12), (18, 0.32, -6)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        waves(k, f, n, pitch=6 if f >= 13 else 0, cycles=1, lag=0.16, start=1)
        k.key("Neck", f, rot=(6 if f < 11 else 14, 0, 0))
        k.key("Head", f, rot=(0, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        pearl(k, f, (0, 0, 0))
    fly_pose(k, n)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, 12):
        sc.frame_set(f)
        for leg in LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f, t in ((15, 0.5), (21, 0.85)):
        legs_fk(k, f, front=40 * t, hind=60 * t, paddle=0)
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """glides in on the wave, the front swings up and the legs reach down, touches (frame 16), absorbs, settles."""
    import bpy
    n = 27
    k.new_action("land", n, False)
    fly_pose(k, 0)
    for f, z, p in ((8, 0.20, -10), (13, 0.06, -4), (16, -0.08, 2), (20, -0.10, 2), (27, 0, 0)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        waves(k, f, n, pitch=4 if f <= 13 else 0, cycles=1, lag=0.16, start=1)
        k.key("Neck", f, rot=(8 if f < 16 else 0, 0, 0))
        k.key("Head", f, rot=(0, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        pearl(k, f, (0, 0, 0))
    legs_fk(k, 8, front=-10, hind=10, paddle=0)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(16, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(16 / n, 3)}


def roar(k):
    """rears the front of its body up off the ground with the neck high, jaw wide, mane bristling, the tail curling
    round; the pearl rises above its head; holds, then sinks back down."""
    import bpy
    n = 70
    k.new_action("roar", n, False)
    for f, sp, z, nk, h, jw, tc, pz in ((0, 0, 0, 0, 0, 0, 0, 0), (12, 4, -0.06, 6, 4, 2, 6, 0.0),
                                        (24, -28, 0.10, -18, 4, 34, 18, 0.40), (48, -30, 0.10, -20, 4, 36, 20, 0.44),
                                        (58, -4, 0.0, -2, 0, 6, 8, 0.10), (70, 0, 0, 0, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Body1", f, rot=(-sp * 0.5, 0, 0))
        k.key("Body2", f, rot=(-sp * 0.4, 0, 0))
        k.key("Tail1", f, rot=(0, tc, 0))
        k.key("Tail2", f, rot=(0, tc, 0))
        k.key("Tail3", f, rot=(0, tc * 1.2, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(h, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        pearl(k, f, (0.12 * (pz > 0.2), 0.0, pz))
    for f in range(26, 48, 2):
        k.key("Jaw", f, rot=(35 + (3 if (f // 2) % 2 else -3), 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            if leg[4] == "F" and 16 <= f <= 56:
                u = 1.0 if 22 <= f <= 50 else ((f - 16) / 6 if f < 22 else (56 - f) / 6)
                side = leg[5:]
                k.key(leg, f, rot=(-30 * u, 0, -(1 if side.endswith("L") else -1) * 16 * u))
                k.key("Shin_" + side, f, rot=(50 * u, 0, 0))
                k.key("Foot_" + side, f, rot=(30 * u, 0, 0))
            else:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)


def coil(k):
    """SIGNATURE - COIL & PEARL: lies down and curls its long body into a ring around the pearl (each segment bends the
    same way), the head circles round to face the pearl, raises it high and spins it, then uncoils and stands."""
    import bpy
    n = 120
    k.new_action("act_coil", n, False)
    C = COIL_C                                # yaw per segment when fully coiled
    for f, c, z, nk, hy, h, jw in ((0, 0, 0, 0, 0, 0, 0), (12, 0, 0.0, 8, 0, 0, 0), (34, 1, -0.10, 4, 50, 6, 0),
                                   (88, 1, -0.10, 4, 50, 6, 0), (106, 0, -0.03, 4, 0, 0, 0), (n, 0, 0, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(0, -C * 0.6 * c, 0), loc=(0, 0, z))
        for i, bn in enumerate(CHAIN[1:], 1):
            k.key(bn, f, rot=(0, -C * c * (1.0 if i < 5 else 0.8), 0))
        k.key("Neck", f, rot=(nk, hy * 0.6, 0))
        k.key("Head", f, rot=(h, hy * 0.5, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    # pearl: to the ring centre, rises high and spins, comes back down to the cheek
    RC = COIL_RC                               # ring centre (measured), as a Pearl offset in the coiled body's frame
    for f, p in ((0, (0, 0, 0)), (12, (0, 0, 0)), (22, (0.30, 0.30, 0.10)), (34, RC), (48, RC), (88, RC),
                 (97, (0.60, 0.70, 0.45)), (106, (0, 0, 0)), (n, (0, 0, 0))):          # arcs out over the head
        k.key("Pearl", f, rot=(0, 0, 0), loc=p)
    for f in range(50, 87, 2):
        u = (f - 48) / 38
        cm.key_axis(k, "Pearl", f, (0, 0, 1), 720 * (0.5 - 0.5 * math.cos(math.pi * u)),
                    loc=(RC[0], RC[1], RC[2] + 1.15 * math.sin(math.pi * u)))
    for f in range(40, 82, 4):
        k.key("Head", f, rot=(6 - 10 * min(1, (f - 40) / 20) if f < 70 else -4, 25, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        if 14 <= f <= 110:                     # legs fold under the belly while coiled, unfold after the uncoil
            u = 1.0 if 22 <= f <= 98 else ((f - 14) / 8 if f < 22 else (110 - f) / 12)
            for leg in LEGS4:
                side = leg[5:]
                s = 1 if side.endswith("L") else -1
                k.key(leg, f, rot=((45 if leg[4] == "F" else -30) * u, 0, -s * 32 * u))     # fronts tuck back
                k.key("Shin_" + side, f, rot=(105 * u, 0, 0))                               # paws folded up
                k.key("Foot_" + side, f, rot=(-40 * u, 0, 0))                                # soles turned up
        else:
            for leg in LEGS4:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    coil(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"), ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw", "Neck"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Tail1", "Tail2", "Tail3", "Body2"):
            P.append((a, b))
    for a in ("Tail2", "Tail3"):
        for b in ("Spine", "Body1", "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR"):
            P.append((a, b))
    P += [("Pearl", "Head"), ("Pearl", "Jaw"), ("Pearl", "Neck"), ("Pearl", "Tail2"), ("Pearl", "Tail3"),
          ("Pearl", "Body2"), ("Pearl", "Tail1")]
    return P


def joints():
    """neck root inside the chest ring, and the overlapping ring ends at every chain joint (hidden hinges)"""
    out = [(Vector(NECK[0]), Vector(NECK[0]), 0.28, "Neck")]
    for i in range(1, len(CHAIN)):
        out.append((BODY[i], BODY[i], WIDTH[i - 1] * 1.3, CHAIN[i]))
    return out
