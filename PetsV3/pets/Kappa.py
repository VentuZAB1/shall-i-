# Kappa (Tide egg #1, T2 Water, biped) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the river imp"): a lean, hunched
# river yokai (snapping turtle + frog + monkey): crouched frog legs with webbed 3-toe feet, a narrow waist with a dark
# rope belt (the sumo mawashi), a forward-leaning chest with a ribbed plastron, a keeled carapace hump on the back, long
# arms reaching the knee with webbed 3-claw hands, a hooked dark beak, narrow aqua eyes under heavy brows, aqua gill
# stripes on the neck and the water DISH on the head, ringed by 7 shaggy hair locks swept back.
# Old chibi version: _tools/chibi_specs/Kappa.py
import math
from mathutils import Vector, Matrix, Euler

DISPLAY = "Kappa"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 7.0

SKIN = (54, 126, 112)       # river teal (Roblox renders ~0.6x darker -> deep teal in game)
SKIN_D = (34, 84, 76)       # back, brows, knuckles
WEB = (104, 176, 156)       # webbing between fingers / toes
SHELL = (96, 118, 78)
SHELL_L = (128, 152, 98)
RIDGE = (58, 72, 48)
PLAS = (204, 194, 136)
PLAS_D = (168, 158, 106)
HAIR = (34, 56, 52)
BEAK = (72, 64, 48)
BELT = (48, 56, 110)        # navy rope mawashi
BELT_L = (78, 88, 150)
DISH = (200, 210, 204)
AQUA = (40, 230, 220)       # THE accent: dish water, eyes, gills
EYE_HOT = (205, 255, 250)
BLACK = (14, 14, 22)
MOUTH = (90, 26, 34)

PITCH = 0.047               # stud pitch: 0.042 x (U / U_raiju), U = model height / HEIGHT

CHEST_C = Vector((0, 0.0, 0.92))
RC = Euler((math.radians(30), 0, 0), "XYZ").to_matrix()               # hunched chest leans forward
S = (0.26, -0.13, 1.04)      # shoulder
E = (0.36, -0.13, 0.79)      # elbow
W = (0.38, -0.30, 0.57)      # wrist
LEG = ((0.15, 0.06, 0.62), (0.26, -0.14, 0.38), (0.20, 0.0, 0.10))     # hip, knee (bent, splayed out), ankle
NK0, NK1 = Vector((0, -0.12, 1.07)), Vector((0, -0.27, 1.19))
HEAD_C = Vector((0, -0.35, 1.27))
HH = Vector((0.16, 0.15, 0.13))
EYE_P = (0.088, -0.502, 1.315)
EYE_YAW = 26


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def face_local(blk, key, u, v):
    """chest-local point, outward normal and across axis on a face of an (unrotated in chest space) tapered block;
    u in [-1, 1] across, v in [0, 1] from the bottom edge to the top edge"""
    c, h, bt, tp = Vector(blk[0]), Vector(blk[1]), blk[2], blk[3]
    ax = 0 if key[1] == "x" else 1
    ot = 1 - ax
    sg = 1 if key[0] == "+" else -1
    ea, eo = Vector((0, 0, 0)), Vector((0, 0, 0))
    ea[ax], eo[ot] = sg, 1
    xa = h[ax] * (bt[ax] + (tp[ax] - bt[ax]) * v)
    ac = h[ot] * (bt[ot] + (tp[ot] - bt[ot]) * v)
    p = c + ea * xa + eo * (u * ac) + Vector((0, 0, -h.z + 2 * h.z * v))
    along = ea * (h[ax] * (tp[ax] - bt[ax])) + Vector((0, 0, 2 * h.z))
    n = eo.cross(along).normalized()
    if n.dot(ea) < 0:
        n = -n
    return p, n, eo, ac


def frame(u, n):
    z = Vector(n).normalized()
    x = Vector(u)
    x = (x - z * x.dot(z)).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


# carapace: ONE oval shield (wide at the shoulders, narrow at the belt) + a raised scute field (chest-local)
CAR = ((0, 0.21, 0.0), (0.25, 0.10, 0.31), (0.60, 0.9), (0.90, 0.8))
DOME = ((0, 0.29, 0.01), (0.22, 0.07, 0.22), (0.60, 0.9), (0.75, 0.8))
SHIELD_Y, SHIELD_T, SHIELD_A, SHIELD_B = 0.21, 0.20, 0.25, 0.31   # oval shield: centre y, thickness, half w, half h


def shield_pt(th, shrink=0.0):
    """chest-local point + outward in-plane normal on the egg-shaped shield outline (wider at the shoulders)"""
    def at(t):
        w = 0.78 + 0.22 * (math.sin(t) + 1) / 2
        return Vector(((SHIELD_A - shrink) * math.cos(t) * w, SHIELD_Y, (SHIELD_B - shrink) * math.sin(t)))
    p = at(th)
    tg = (at(th + 0.01) - at(th - 0.01)).normalized()
    n = Vector((tg.z, 0, -tg.x))
    if n.dot(Vector((p.x, 0, p.z))) < 0:
        n = -n
    return p, n


def CP(x, y, z):
    """chest-local point -> world"""
    return CHEST_C + RC @ Vector((x, y, z))


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=71, tier=2, plates=False, th=0.44)
    # ---------------- narrow waist, rope belt, hunched chest with a ribbed plastron, keeled carapace hump
    B.add((0, 0.05, 0.64), (0.16, 0.13, 0.085), SKIN, "Spine", rnd=0.3, role="mass")
    B.add(CHEST_C, (0.24, 0.17, 0.22), SKIN, "Chest", R=RC, bot=(0.62, 0.84), top=(1.0, 0.95), rnd=0.30,
          role="mass")
    B.add(CP(0, -0.166, 0.0), (0.165, 0.008, 0.185), PLAS_D, "Chest", R=RC, bot=(0.45, 1), studs=[],
          role="detail", bevel=0.006)                                                                   # plastron
    for z, w in ((-0.125, 0.08), (0.0, 0.11), (0.125, 0.14)):
        B.add(CP(0, -0.176, z), (w, 0.012, 0.052), PLAS, "Chest", R=RC, studs=[], role="detail", bevel=0.008)
    B.poly([CP(*shield_pt(2 * math.pi * i / 24)[0]) for i in range(24)], SHIELD_T, RIDGE, "Chest")   # oval shield
    B.add(CP(*DOME[0]), DOME[1], RIDGE, "Chest", R=RC, bot=DOME[2], top=DOME[3], rnd=0.45, role="mass")

    def tile(blk, key, u, v, hu, hv, col, t=0.024):
        q, n, ax, _ = face_local(blk, key, u, v)
        pw, nw = CP(*q), RC @ n
        B.add(pw + nw * (t / 2 - 0.006), (hu, hv, t / 2), col, "Chest", R=frame(RC @ ax, nw), top=(0.85, 0.85),
              rnd=0.3, role="limb")
        return pw, nw
    for v in (0.19, 0.5, 0.81):                         # 3 vertebral scutes (keeled) + 3 costal per side
        pw, nw = tile(DOME, "+y", 0, v, 0.06, 0.065, SHELL_L)
        B.spike(pw + nw * 0.012, nw + RC @ Vector((0, 0, 0.55)), 0.085, 0.045, RIDGE, "Chest", top=(0.12, 0.45))
        ac = face_local(DOME, "+y", 0, v)[3]
        for sx in (1, -1):
            x = min(0.13, ac - 0.03)
            tile(DOME, "+y", sx * x / ac, v, 0.035, 0.065, SHELL)
    for i in range(10):                                 # scalloped marginal ring round the oval edge
        q, n = shield_pt(2 * math.pi * (i + 0.5) / 10, shrink=0.012)
        nw = RC @ n
        B.add(CP(*q) + nw * 0.006, (0.088, 0.072, 0.02), SHELL, "Chest", R=frame(RC @ Vector((0, 1, 0)), nw),
              top=(0.85, 0.8), rnd=0.3, role="limb")
    # rope mawashi belt: a twisted rope band, front knot, two hanging rope ends
    B.add((0, 0.04, 0.70), (0.18, 0.15, 0.046), BELT, "Spine", rnd=0.4, role="limb")
    for i in range(6):
        x = -0.15 + i * 0.06
        B.add((x, -0.118, 0.70), (0.022, 0.012, 0.038), BELT_L, "Spine", rot=(0, 30, 0), studs=[], role="detail",
              bevel=0.006)
    B.add((0, -0.125, 0.695), (0.06, 0.03, 0.055), BELT, "Spine", rnd=0.4, role="limb")
    for x in (-0.03, 0.03):
        B.seg((x, -0.14, 0.665), (x * 1.5, -0.15, 0.53), 0.018, 0.016, BELT, "Spine", top=(0.7, 0.7), role="detail")
    # ---------------- neck with aqua gill stripes
    B.seg(NK0, NK1, 0.105, 0.10, SKIN, "Neck", ext=0.04, ext1=0.02, rnd=0.3)
    nd = (NK1 - NK0).normalized()
    for s in (1, -1):
        for t in (0.35, 0.68):
            c = NK0.lerp(NK1, t) + Vector((s * 0.104, 0, 0))
            B.bar(c - Vector((0, -0.03, 0.045)), c + Vector((0, -0.03, 0.045)), (s, 0, 0), 0.03, 0.008, AQUA, "Neck",
                  studs=[], bevel=0.003)
    # ---------------- head: snapper skull, hooked dark beak, heavy brows, narrow aqua eyes, the dish + hair ring
    B.seg(HEAD_C + Vector((0, HH.y, 0.012)), HEAD_C - Vector((0, HH.y, 0.012)), HH.x, HH.z, SKIN, "Head",
          top=(0.74, 0.84), rnd=0.3, role="mass")                                          # wedge skull
    for s in (1, -1):
        B.add(HEAD_C + Vector((s * 0.14, 0.03, -0.06)), (0.04, 0.08, 0.05), SKIN, "Head", top=(0.6, 0.6), rnd=0.45,
              role="limb")                                                                 # jowls
    B.add(HEAD_C + Vector((0, 0.03, HH.z - 0.01)), (0.13, 0.12, 0.02), SKIN_D, "Head", role="limb")        # crown
    hb, fy = HEAD_C.z - HH.z, HEAD_C.y - HH.y
    B.seg((0, fy + 0.04, hb + 0.095), (0, fy - 0.12, hb + 0.075), 0.105, 0.05, BEAK, "Head", top=(0.40, 0.6),
          rnd=0.2, role="limb")                                                                         # upper beak
    B.seg((0, fy - 0.10, hb + 0.09), (0, fy - 0.15, hb + 0.03), 0.045, 0.035, BEAK, "Head", top=(0.3, 0.4),
          role="limb")                                                                                  # hook
    for s in (1, -1):
        B.add((s * 0.025, fy - 0.075, hb + 0.108), (0.01, 0.012, 0.006), BLACK, "Head", rot=(-15, 0, 0), studs=[],
              role="detail", bevel=0.002)                                                               # nostrils
    B.add((0, fy + 0.03, hb + 0.03), (0.04, 0.09, 0.005), MOUTH, "Head", studs=[], role="detail", bevel=0.002)
    # lower beak (Jaw)
    B.seg((0, fy + 0.10, hb + 0.01), (0, fy - 0.11, hb + 0.02), 0.09, 0.03, BEAK, "Jaw", top=(0.5, 0.7), rnd=0.25)
    B.add((0, fy + 0.01, hb + 0.04), (0.04, 0.08, 0.005), MOUTH, "Jaw", studs=[], role="detail", bevel=0.002)
    for s in (1, -1):
        R = Euler((0, math.radians(-s * 18), math.radians(s * EYE_YAW)), "XYZ").to_matrix()
        Rb = Euler((0, math.radians(-s * 24), math.radians(s * (EYE_YAW - 6))), "XYZ").to_matrix()
        c = X(EYE_P, s)

        def P(Rm, dx, dy, dz):
            return c + Rm @ Vector((s * dx, dy, dz))
        B.add(P(R, 0, 0, 0), (0.05, 0.010, 0.024), BLACK, "Head", R=R, studs=[], role="detail", bevel=0.004)
        B.add(P(R, 0.002, -0.008, 0), (0.042, 0.006, 0.013), AQUA, "Head", R=R, studs=[], role="detail", bevel=0.003)
        B.add(P(R, 0.010, -0.012, 0.002), (0.018, 0.004, 0.006), EYE_HOT, "Head", R=R, studs=[], role="detail",
              bevel=0.002)
        B.add(P(Rb, -0.010, 0.006, 0.046), (0.068, 0.032, 0.026), SKIN_D, "Head", R=Rb, role="detail", bevel=0.01)
    # the dish (sara): bone rim ring around an aqua water disc
    dz = HEAD_C.z + HH.z + 0.012
    dc = Vector((0, HEAD_C.y + 0.02, dz))
    for rz in (0, 45):                                                     # octagonal plate + water
        B.add(dc + Vector((0, 0, -0.006)), (0.115, 0.115, 0.02), DISH, "Head", rot=(0, 0, rz), nostud=True,
              role="limb")
        B.add(dc + Vector((0, 0, 0.018)), (0.082, 0.082, 0.012), AQUA, "Head", rot=(0, 0, rz), studs=[],
              role="detail", bevel=0.004)
    for i in range(8):                                                     # raised rim ring
        a = math.radians(22.5 + 45 * i)
        B.add(dc + Vector((0.112 * math.cos(a), 0.112 * math.sin(a), 0.03)), (0.026, 0.05, 0.03), DISH, "Head",
              rot=(0, 0, math.degrees(a)), rnd=0.3, nostud=True, role="limb")
    # 7 shaggy hair locks swept back round the dish (open over the forehead)
    for adeg, L, dzl in ((5, 0.13, -1.1), (40, 0.21, -0.8), (72, 0.20, -0.25), (90, 0.22, -0.22), (108, 0.20, -0.25),
                         (140, 0.21, -0.8), (175, 0.13, -1.1)):
        a = math.radians(adeg)
        d = Vector((math.cos(a), math.sin(a), 0))
        base = dc + Vector((d.x * 0.135, d.y * 0.135, 0.0))
        out = (d * 0.9 + Vector((0, 0.55, dzl))).normalized()
        B.seg(base, base + out * L, 0.05, 0.022, HAIR, "Head", side=(-d.y, d.x, 0), top=(0.18, 0.5), ext=0.05,
              role="limb")
    # ---------------- long arms reaching the knee; webbed 3-claw hands
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        B.add(Sv + Vector((s * 0.01, 0, -0.01)), (0.07, 0.07, 0.065), SKIN, "Arm_" + side, rnd=0.4, role="limb")
        B.seg(Sv, Ev, 0.055, 0.06, SKIN, "Arm_" + side, ext=0.04, ext1=0.02, rnd=0.3)
        B.seg(Ev, Wv, 0.058, 0.062, SKIN, "Fore_" + side, ext=0.03, top=(0.85, 0.85), rnd=0.3)
        hc = Wv + Vector((0, -0.02, -0.06))
        B.add(hc, (0.07, 0.06, 0.06), SKIN_D, "Hand_" + side, rnd=0.3, role="limb")
        tips = []
        for dx, ang in ((-0.05, -16), (0.0, 0), (0.05, 16)):
            a = math.radians(ang)
            d = Vector((s * math.sin(a), -0.35, -math.cos(a))).normalized()
            r0 = hc + Vector((dx, -0.02, -0.04))
            m = r0 + d * 0.10
            B.seg(r0, m, 0.022, 0.024, SKIN, "Hand_" + side, ext=0.02, role="limb")
            B.spike(m - d * 0.01, d + Vector((0, -0.4, 0)), 0.06, 0.02, BLACK, "Hand_" + side)
            tips.append((r0, m))
        for (a0, a1), (b0, b1) in zip(tips, tips[1:]):
            B.poly([a0, a1.lerp(a0, 0.25), b1.lerp(b0, 0.25), b0], 0.008, WEB, "Hand_" + side)
    # ---------------- crouched frog legs, webbed 3-toe feet with black claws
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A = (X(p, s) for p in LEG)
        B.seg(H, K, 0.085, 0.09, SKIN, "Leg_" + side, ext=0.06, ext1=0.03, rnd=0.3)
        B.seg(K, A, 0.068, 0.072, SKIN, "Shin_" + side, ext=0.04, rnd=0.3)
        B.add(A + Vector((0, -0.04, -0.07)), (0.075, 0.085, 0.03), SKIN_D, "Foot_" + side, rnd=0.3, role="limb")
        toes = []
        for ang in (-28, 0, 28):
            a = math.radians(ang)
            d = Vector((s * math.sin(a), -math.cos(a), 0))
            p0 = A + Vector((0, -0.06, -0.075))
            p1 = p0 + d * 0.17
            B.seg(p0, p1, 0.024, 0.022, SKIN, "Foot_" + side, side=(0, 0, 1), ext=0.02, role="limb")
            B.spike(p1 - d * 0.01, d + Vector((0, 0, -0.3)), 0.05, 0.018, BLACK, "Foot_" + side)
            toes.append((p0, p1))
        for (a0, a1), (b0, b1) in zip(toes, toes[1:]):
            B.poly([a0 + Vector((0, 0, 0.012)), a1.lerp(a0, 0.2) + Vector((0, 0, 0.012)),
                    b1.lerp(b0, 0.2) + Vector((0, 0, 0.012)), b0 + Vector((0, 0, 0.012))], 0.008, WEB, "Foot_" + side)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.05, 0.64), "Root", tail=(0, 0, 0.3))
    k.joint("Chest", (0, 0.06, 0.74), "Spine", tail=tuple(RC @ Vector((0, 0, 0.4))))
    k.joint("Neck", tuple(NK0), "Chest", tail=tuple((NK1 - NK0) * 0.8))
    k.joint("Head", (0, -0.27, 1.17), "Neck", tail=(0, -0.3, 0.05))           # throat pivot
    k.joint("Jaw", (0, HEAD_C.y - HH.y + 0.10, HEAD_C.z - HH.z + 0.02), "Head", tail=(0, -0.2, 0))
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        k.joint("Arm_" + side, Sv, "Chest")
        k.joint("Fore_" + side, Ev, "Arm_" + side)
        k.joint("Hand_" + side, Wv, "Fore_" + side, tail=(0, -0.05, -0.2))
        H, K, A = (X(p, s) for p in LEG)
        k.joint("Leg_" + side, H, "Spine")
        k.joint("Shin_" + side, K, "Leg_" + side)
        k.joint("Foot_" + side, A, "Shin_" + side, tail=(0, -0.2, 0))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(s * 0.35, -0.9, 0))


# ------------------------------------------------------------------ animation (FIERCE_PLAN: dish guard / screech crouch /
# act_sumo). k.key rot = (pitch, yaw, roll) deg, armature axes, relative to the parent.
import petkit as pk
import _common as cm

LEGS2 = ["Leg_L", "Leg_R"]


def arm(k, f, side, pitch=0.0, yaw=0.0, roll=0.0, elbow=0.0, hand=0.0):
    """pitch - swings the arm forward/up, roll + lifts it out to the side, elbow + bends the forearm forward/up,
    hand + curls the claws (- spreads them)"""
    s = 1 if side == "L" else -1
    k.key("Arm_" + side, f, rot=(pitch, s * yaw, -s * roll))
    k.key("Fore_" + side, f, rot=(-elbow, 0, 0))
    k.key("Hand_" + side, f, rot=(-hand, 0, 0))


REST_ARM = dict(pitch=0, roll=4, elbow=14, hand=8)
THIGH = dict(pitch=6, roll=-4, elbow=34, hand=-6)          # hands on the thighs (sumo squat)
CUP = dict(pitch=-124, roll=-16, elbow=58, hand=60)         # right hand cupped over the dish


def idle(k):
    """DISH GUARD: a frog squat breathing - the body bobs but the head stays dead LEVEL (counter-rotated); the right
    hand rises to cup the dish, a sly sideways leer (held), then one deep frog-squat bounce."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        sq = math.sin(math.pi * (f - 95) / 15) if 95 <= f <= 110 else 0.0
        sp, ch = 1.5 * b + 4 * sq, 2.0 * b + 6 * sq
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, 0.008 * b - 0.08 * sq))
        k.key("Chest", f, rot=(ch, 0, 0))
        leer = 0.0
        if 65 <= f <= 90:
            leer = min(1.0, (f - 65) / 5, (90 - f) / 5)
        cnt = -(3.5 * b) * 0.5 - (10 * sq) * 0.15          # breathing fully countered, the bounce only a little
        k.key("Neck", f, rot=(cnt, 8 * leer, 0))
        k.key("Head", f, rot=(cnt, 12 * leer, 0))
        k.key("Jaw", f, rot=(2 + 1.5 * max(0.0, b), 0, 0))
        arm(k, f, "L", **REST_ARM)
    for f, a in ((0, REST_ARM), (35, REST_ARM), (44, CUP), (54, CUP), (62, REST_ARM), (120, REST_ARM)):
        arm(k, f, "R", **a)
    cm.plant(k, n, legs=LEGS2)
    k.finish()
    k.meta["planted"] = LEGS2


def walk(k):
    n = 26

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(2, 5 * pk.wave(f, n, 0.0), 5 * pk.wave(f, n, 0.0)), loc=(0, 0, -0.025 * b))
        k.key("Chest", f, rot=(2, -6 * pk.wave(f, n, 0.0), -4 * pk.wave(f, n, 0.0)))
        k.key("Neck", f, rot=(-2, 0, 0))
        k.key("Head", f, rot=(-2, 0, 6 * pk.wave(f, n, 0.0)))         # keeps the dish level against the waddle
        k.key("Jaw", f, rot=(2, 0, 0))
        for side, ph in (("L", 0.5), ("R", 0.0)):
            arm(k, f, side, pitch=22 * pk.wave(f, n, ph + 0.05), roll=8, elbow=18 + 10 * pk.wave(f, n, ph + 0.2),
                hand=8)
    return cm.biped_walk(k, n, 0.10, 0.08, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.58)


def roar(k):
    """SCREECH CROUCH: drops into a low crouch, flings the arms wide with the claws spread, gapes the beak forward at
    head height and holds trembling, then snaps back up."""
    n = 58
    k.new_action("roar", n, False)
    for f, z, sp, ch, nk, hd, jw, ro, p, el, hn in ((0, 0, 0, 0, 0, 0, 2, 4, 0, 14, 8),
                                                    (10, -0.06, 4, 8, 4, 2, 2, 8, 4, 40, 20),
                                                    (18, -0.10, 6, 12, -6, -4, 34, 72, -36, 8, -32),
                                                    (44, -0.10, 6, 12, -6, -4, 32, 74, -38, 8, -32),
                                                    (50, -0.02, 2, 2, -4, -2, 4, 20, -8, 24, 8),
                                                    (58, 0, 0, 0, 0, 0, 2, 4, 0, 14, 8)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0), loc=(0, -0.04 * (18 <= f <= 44), 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        for side in ("L", "R"):
            arm(k, f, side, pitch=p, roll=ro, elbow=el, hand=hn)
    for f in range(20, 44, 2):
        k.key("Jaw", f, rot=(33 + (3 if (f // 2) % 2 else -3), 0, 0))
        k.key("Chest", f, rot=(12 + (1 if (f // 2) % 2 else -1), 0, 0))
    cm.plant(k, n, legs=LEGS2)
    k.finish(loop=False)


def sumo(k):
    """SIGNATURE act_sumo - SHIKO & TSUPPARI: sinks into a deep sumo squat with the hands on the thighs, swings the left
    leg HIGH out to the side and STOMPS, then the right; back into the squat for three palm thrusts R-L-R at chest
    height with a beak snap each, rises, and one hand checks the dish (not spilled)."""
    import bpy
    n = 100
    k.new_action("act_sumo", n, False)
    #        f    z     roll  chest  spine
    for f, z, r, ch, sp in ((0, 0, 0, 0, 0), (12, -0.12, 0, 8, 4), (20, -0.06, -14, 4, 2), (26, -0.03, -18, 2, 2),
                            (30, -0.03, -18, 2, 2), (33, -0.13, -2, 10, 5), (36, -0.12, 0, 8, 4), (44, -0.06, 14, 4, 2),
                            (50, -0.03, 18, 2, 2), (54, -0.03, 18, 2, 2), (57, -0.13, 2, 10, 5), (60, -0.12, 0, 8, 4),
                            (64, -0.12, 0, 6, 4), (88, -0.11, 0, 6, 4), (96, 0, 0, 0, 0), (100, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(sp, 0, r), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, -r * 0.3))
        k.key("Neck", f, rot=(-(ch + sp) * 0.2, 0, 0))
        k.key("Head", f, rot=(-(ch + sp) * 0.2, 0, r * 0.5))
    snaps = (70, 78, 86)
    for f in range(0, n + 1, 2):
        j = 2
        for sf in snaps:
            if sf - 2 <= f <= sf + 2:
                j = 26 if abs(f - sf) <= 0 else 14
        k.key("Jaw", f, rot=(j, 0, 0))
    for f in (34, 58):
        k.key("Jaw", f, rot=(18, 0, 0))
    up = dict(pitch=-18, roll=62, elbow=14, hand=-16)        # balance arm thrown out during the leg raise
    keys = {"L": {0: REST_ARM, 12: THIGH, 18: up, 30: up, 34: THIGH, 42: THIGH, 54: THIGH, 58: THIGH, 64: THIGH},
            "R": {0: REST_ARM, 12: THIGH, 18: THIGH, 30: THIGH, 34: THIGH, 42: up, 54: up, 58: THIGH, 64: THIGH}}
    cock = dict(pitch=-30, roll=10, elbow=78, hand=-20)
    thrust = dict(pitch=-82, roll=4, elbow=6, hand=-40)
    for side, hit in (("R", (70, 86)), ("L", (78,))):
        for h in hit:
            keys[side][h - 4] = cock
            keys[side][h] = thrust
            keys[side][h + 4] = cock
        keys[side][90] = THIGH
    keys["L"][96] = REST_ARM
    keys["R"][95] = CUP                                                  # checks the dish
    keys["R"][97] = CUP
    keys["L"][100] = REST_ARM
    keys["R"][100] = REST_ARM
    for side, kk in keys.items():
        for f in sorted(kk):
            arm(k, f, side, **kk[f])
    k.bake_bezier_now()

    def raise_t(f, a, b, c, d):
        """leg up a->b, held b->c, slammed down c->d"""
        if a <= f <= b:
            u = (f - a) / (b - a)
            return 0.5 - 0.5 * math.cos(math.pi * u)
        if b < f <= c:
            return 1.0
        if c < f <= d:
            u = (f - c) / (d - c)
            return 1 - u * u
        return 0.0

    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg, w in (("Leg_L", (14, 26, 30, 33)), ("Leg_R", (38, 50, 54, 57))):
            s = 1 if leg.endswith("L") else -1
            t = raise_t(f, *w)
            T = Vector((k.J[leg].x + s * 0.34 * t, k.J[leg].y + 0.03 * t, 0.46 * t))   # HIGH shiko swing
            k.solve_leg(leg, f, T, toe=0.0)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    sumo(k)
    return stride


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Head", "Chest"), ("Jaw", "Chest"),
         ("Hand_L", "Hand_R"), ("Fore_L", "Fore_R")]
    for s in ("L", "R"):
        for a in ("Fore_" + s, "Hand_" + s):
            for b in ("Spine", "Chest", "Head", "Jaw", "Leg_L", "Leg_R", "Shin_L", "Shin_R"):
                P.append((a, b))
    return P


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        Wv = X(W, s)
        out.append((Wv, Wv, 0.08, "Hand_" + side))
    return out


HEAD_XF = []
