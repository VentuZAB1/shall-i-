# Cvetibara (SECRET, Celestial egg): the approved lovely V2 angel capybara rebuilt in the Steal-an-Egg block style
# (STYLE_BIBLE 3 "Cvetibara", SECRET row: softest rounding, plate fill .45). A caramel loaf body with a huge boxy head,
# a blunt light snout with a big dark nose, lilac-glint lovely eyes with 2 highlights and blush, tiny dark-pawed legs,
# a floating gold halo, a pink star-lotus on her head, 4 gold stars on her back and 3-row white-to-gold feather wings.
# Clips ported from FriendPets/Cvetibara (v2): zen idle with a double wing flutter, trot walk, real flight (legs pump),
# takeoff (launch) / land (touch), roar = CELESTIAL BLESSING (rears up, wings wide, halo rises and spins),
# signature act_happy = joyful hop with a double wing flap and a halo spin.
import math
from mathutils import Vector, Quaternion
import wing3

DISPLAY = "Cvetibara"
MOTION = "Fly"
RIG = "wingquad"
HEIGHT = 7.5

CARAMEL = (214, 140, 80)
SNOUT = (240, 190, 140)
NOSE = (90, 50, 40)
NOSTRIL = (44, 26, 24)
WHITE = (250, 250, 255)
WARM = (255, 242, 214)
GOLD_L = (255, 226, 140)
GOLD = (255, 206, 70)
GOLD_D = (232, 168, 44)
PINK = (255, 150, 200)
PINK_D = (240, 112, 172)
CENTRE = (255, 230, 120)
BLUSH = (255, 140, 160)
IRIS = (110, 80, 220)
IRIS_L = (168, 140, 255)
SHEEN = (246, 244, 250)
INNER_EAR = (240, 160, 150)

TORSO_C, TORSO_H = (0, 0.10, 0.58), (0.45, 0.63, 0.33)          # TW 0.90, TL 1.26 (1.4 TW), TH 0.66
HEAD_C, HEAD_H = (0, -0.79, 1.06), (0.45, 0.36, 0.315)           # HW 0.90 (1.0 TW), HH 0.63 (0.95 TH)
LEGS = {"F": (0.27, -0.27), "B": (0.28, 0.47)}
LEG_TOP = 0.36                                                     # single-bone legs: joint height (foot at z 0)
WING = wing3.Wing(S=(0.42, -0.16, 0.93), W=(0.90, -0.03, 1.41), H=(0.86, 0.50, 0.99), BB=(0.41, 0.38, 0.93))
TIP = (1.62, 0.27, 1.87)
HALO_C = (0, -0.80, 1.66)
FLOWER_C = (0.15, -0.90, 1.37)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def front_y(blk, z):
    """y of the (tapered, unrotated) block's -y face at world height z"""
    t = ((z - blk.c.z) / blk.h.z + 1) / 2
    sy = blk.bot[1] + (blk.top[1] - blk.bot[1]) * t
    return blk.c.y + blk.ts[1] * t - blk.h.y * sy


def front_n(blk):
    dydz = -blk.h.y * (blk.top[1] - blk.bot[1]) / (2 * blk.h.z)
    return Vector((0, -1, dydz)).normalized()


def front_inlay(B, blk, x, z0, z1, width, thick, color, bone, **kw):
    """flush inlay on the -y face of a tapered block from height z0 to z1 (follows the taper)"""
    n = front_n(blk)
    p0 = Vector((x, front_y(blk, z0), z0)) + n * (thick + 0.002)
    p1 = Vector((x, front_y(blk, z1), z1)) + n * (thick + 0.002)
    kw.setdefault("studs", [])
    kw.setdefault("bevel", min(0.012, thick * 0.6))
    return B.bar(p0, p1, n, width, thick, color, bone, **kw)


def star(B, c, n, r, thick, color, bone, rot=0.0, depth=0.45):
    """5-point star of tapered rays lying on a surface with normal n (blocks, so plates under it are culled)"""
    c, n = Vector(c), Vector(n).normalized()
    u = Vector((1, 0, 0)) if abs(n.x) < 0.9 else Vector((0, 1, 0))
    u = (u - n * u.dot(n)).normalized()
    v = n.cross(u)
    B.add(c + n * (thick + 0.002), (r * depth * 0.8, r * depth * 0.8, thick), color, bone, studs=[],
          R=_frame(u, v, n), bevel=thick * 0.5, rot=None)
    for i in range(5):
        a = math.radians(rot + 90 + 72 * i)
        d = u * math.cos(a) + v * math.sin(a)
        B.bar(c + n * (thick + 0.002), c + n * (thick + 0.002) + d * r, n, r * 0.62, thick, color, bone, studs=[],
              top=(1, 0.12), bevel=thick * 0.5)


def _frame(u, v, n):
    from mathutils import Matrix
    return Matrix((u, v, n)).transposed()


def feather_wing(B, s, side):
    """STYLE_BIBLE 2d feather wing: gold arm bar, 6 white coverts on top, 7 warm-white secondaries hanging back to the
    hinge line (inner wing, Wing bone), 6 white primaries fanned from the wrist with gold tips (outer wing, WingTip
    bone, folds about the wrist->hinge line). Saw-edged tips, rows offset along the normal (no coplanar faces)."""
    S, W, H, BB = (X(p, s) for p in (WING.S, WING.W, WING.H, WING.BB))
    T = X(TIP, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    n = (W - S).cross(H - W).normalized()
    if n.z < 0:
        n = -n
    FT = 0.017
    B.seg(S, W, 0.042, 0.06, WHITE, wb, side=n, ext=0.10, studs=[], role="limb")
    B.add(W, (0.068, 0.068, 0.068), WHITE, wb, studs=[], role="limb")
    B.seg(W, W.lerp(T, 0.30), 0.036, 0.05, WHITE, tb, side=n, studs=[], top=(0.8, 0.8), role="limb")
    B.seg(S.lerp(W, 0.25), W, 0.046, 0.022, GOLD, wb, side=n, studs=[], role="limb")     # gold leading-edge trim
    NS = 9
    for i in range(NS):
        t = (i + 0.5) / NS
        a = S.lerp(W, 0.03 + 0.94 * t)
        e = BB.lerp(H, t)
        d = (e - a).normalized()
        L = (e - a).length + (0.11 if i % 2 else 0.04) * min(1.0, t * 2.2)
        o = n * (0.005 if i % 2 else -0.005)
        B.bar(a + o, a + d * L + o, n, 0.19, FT, WARM, wb, studs=[], top=(1, 0.50))
        B.bar(a.lerp(a + d * L, 0.72) + o, a + d * L + o, n, 0.19 * (1 - 0.5 * 0.72), FT + 0.002, GOLD_L, wb,
              studs=[], top=(1, 0.50 / (1 - 0.5 * 0.72)))
    NC = 7
    for i in range(NC):
        t = (i + 0.5) / NC
        a = S.lerp(W, 0.02 + 0.94 * t)
        e = BB.lerp(H, t)
        d = (e - a).normalized()
        o = n * (FT + 0.012 + 0.004 * (i % 2))
        B.bar(a + o - d * 0.03, a + d * (0.30 + 0.05 * (i % 2)) + o, n, 0.17, FT, WHITE, wb, studs=[], top=(1, 0.40))
    NP = 9                                         # fan step ~10 deg, tips touch: a scalloped gold edge, no rake
    hd, td = (H - W).normalized(), (T - W).normalized()
    PW, PT = 0.22, 0.55
    for j in range(NP):
        u = j / (NP - 1)
        d = hd.lerp(td, 0.16 + 0.84 * u).normalized()
        L = (T - W).length * (0.62 + 0.38 * u) + (0.05 if j % 2 else -0.01)
        o = -n * (0.010 + 0.005 * (j % 2))
        a = W + d * 0.02 + o
        e = W + d * L + o
        B.bar(a, e, n, PW, FT, WHITE, tb, studs=[], top=(1, PT))
        w70 = PW * (1 - (1 - PT) * 0.70)            # the gold tip = the outer 30 % of the same feather
        B.bar(a.lerp(e, 0.70), e, n, w70, FT + 0.002, GOLD, tb, studs=[], top=(1, PW * PT / w70))


def model(k):
    """Cvetibara, bible SECRET: loaf body, huge boxy head with a blunt snout, tiny legs, halo, star-lotus, gold stars,
    white-to-gold feather wings. Softest rounding (rnd .30 on the masses), plate fill .45, no glow."""
    import blockkit as bk
    B = bk.Blocks(k, seed=53, tier="S")
    mix0 = bk.STYLE["mix"]
    bk.STYLE["mix"] = (0.80, 0.20, 0.0)
    torso = B.add(TORSO_C, TORSO_H, CARAMEL, "Spine", bot=(0.92, 0.96), rnd=0.30, density=0.56)
    B.add((0, -0.49, 0.83), (0.38, 0.13, 0.14), CARAMEL, "Spine", studs=[], rnd=0.45)      # throat fill under the head
    # light chest bib under the head (flush inlay that follows the taper) + belly band
    front_inlay(B, torso, 0, 0.36, 0.70, 0.46, 0.006, SNOUT, "Spine")
    B.add((0, 0.10, 0.256), (0.34, 0.52, 0.012), SNOUT, "Spine", studs=[], bevel=0.008)
    r = 0.30 * min(TORSO_H[0] * 0.92, TORSO_H[1] * 0.96, TORSO_H[2])        # the torso's bevel radius
    z0 = TORSO_C[2] - TORSO_H[2]

    def xf(z):                                                              # flank x at height z (bottom taper)
        return TORSO_H[0] * (0.92 + 0.08 * (z - z0) / (2 * TORSO_H[2]))
    for s in (1, -1):
        zm = z0 + r + 0.065                                                 # flat lower flank band (z 0.35 - 0.48)
        nf = Vector((s, 0, -TORSO_H[0] * 0.08 / (2 * TORSO_H[2]))).normalized()
        pa = Vector((s * xf(zm), -0.42, zm)) + nf * 0.008
        B.bar(pa, pa + Vector((0, 1.04, 0)), nf, 0.135, 0.006, SNOUT, "Spine", studs=[], bevel=0.004)
        xc, zc = xf(z0) - r, z0 + r                                         # the rounded bottom corner, 45 deg facet
        nc = Vector((s * 0.7071, 0, -0.7071))
        pc = Vector((s * (xc + r * 0.7071), -0.40, zc - r * 0.7071)) + nc * 0.008
        B.bar(pc, pc + Vector((0, 1.0, 0)), nc, 0.085, 0.006, SNOUT, "Spine", studs=[], bevel=0.004)
    # 4 gold stars on the back
    for (x, y, r, rt) in ((0.0, -0.20, 0.085, 0), (0.17, 0.12, 0.07, 18), (-0.15, 0.30, 0.075, -12), (0.06, 0.52, 0.06, 30)):
        star(B, (x, y, 0.91), (0, 0, 1), r * 1.35, 0.012, GOLD, "Spine", rot=rt)
    # ---- head: final size, sits on the front of the loaf; blunt light snout, big dark nose, w mouth
    head = B.add(HEAD_C, HEAD_H, CARAMEL, "Head", top=(0.94, 0.94), rnd=0.30, density=0.85, pmix=(1.0, 0.0, 0.0),
                 studs=["+x", "-x", "+y", "+z"])
    snout = B.add((0, -1.22, 0.865), (0.28, 0.23, 0.155), SNOUT, "Head", top=(0.94, 0.92), rnd=0.36, studs=[])
    nz = 0.955
    ny = front_y(snout, nz)
    B.add((0, ny + 0.02, nz), (0.15, 0.07, 0.055), NOSE, "Head", top=(0.86, 0.80), studs=[], role="limb", rnd=0.45)
    for sx in (1, -1):
        B.add((sx * 0.055, ny - 0.05, nz - 0.018), (0.016, 0.006, 0.014), NOSTRIL, "Head", studs=[],
              bevel=0.004)
    B.add((-0.08, ny - 0.052, nz + 0.022), (0.018, 0.004, 0.012), SHEEN, "Head", studs=[], bevel=0.004)
    # "w" mouth: 4 small bars below the nose
    mz = 0.82
    my = front_y(snout, mz) - 0.008
    for (x, a) in ((-0.075, 35), (-0.028, -35), (0.028, 35), (0.075, -35)):
        B.add((x, my, mz), (0.032, 0.006, 0.011), NOSE, "Head", rot=(0, a, 0), studs=[], bevel=0.004)
    # lovely lilac-glint eyes, 2 highlights, high on the head (capybara), blush beside the snout
    E = B.face_eyes(head, "lovely", IRIS, base=CARAMEL, z=0.67, x=0.25, pupil_size=(0.10, 0.125), hl_size=(0.08, 0.03),
                    look=(0, 0.6))
    HW = E["HW"]
    iw, ih = 0.22 * HW, 0.25 * HW
    t = 0.011 * HW + 1.5 * 0.0045 * HW
    for side in ("L", "R"):          # lilac glint: lighter lower iris (ref_05)
        c = E[side]
        B.add(c + Vector((0, -(t / 2 + 0.002), -ih * 0.30)), (iw * 0.46, t / 2, ih * 0.19), IRIS_L, "Head", studs=[],
              rnd=0.0, bevel=0.006)
    hz = 0.86
    for sx in (1, -1):
        B.add((sx * 0.335, front_y(head, hz) - 0.008, hz), (0.062, 0.006, 0.026), BLUSH, "Head", studs=[], bevel=0.006)
    # small round capybara ears with light inner plates
    for s, side in ((1, "L"), (-1, "R")):
        ear = B.add((s * 0.31, -0.60, 1.41), (0.105, 0.055, 0.095), CARAMEL, "Ear_" + side, rot=(-10, 0, -s * 14),
                    studs=[], role="limb", rnd=0.40)
        B.add(ear.world((0, -0.059, -0.014)), (0.066, 0.006, 0.058), INNER_EAR, "Ear_" + side, R=ear.R, studs=[],
              bevel=0.008)
    # ---- star-lotus flower on the head (Flower bone): 5 pink petals + 5 inner petals + yellow centre
    fc = Vector(FLOWER_C)
    for i in range(5):
        a = math.radians(90 + 72 * i)
        d = Vector((math.cos(a), math.sin(a), 0.75)).normalized()
        B.spike(fc + d * 0.01, d, 0.21, 0.055, PINK, "Flower", side=Vector((-math.sin(a), math.cos(a), 0)),
                top=(0.15, 0.6), studs=[], role="limb")
        a2 = a + math.radians(36)
        d2 = Vector((math.cos(a2), math.sin(a2), 1.5)).normalized()
        B.spike(fc + d2 * 0.01, d2, 0.15, 0.045, PINK_D, "Flower", side=Vector((-math.sin(a2), math.cos(a2), 0)),
                top=(0.15, 0.6), studs=[], role="limb")
    B.add(fc + Vector((0, 0, 0.035)), (0.04, 0.04, 0.035), CENTRE, "Flower", studs=[], role="limb", rnd=0.45)
    # ---- floating gold halo: ring of 8 rounded blocks (Halo bone)
    hc = Vector(HALO_C)
    for i in range(8):
        a = math.radians(22.5 + 45 * i)
        p = hc + Vector((math.cos(a) * 0.25, math.sin(a) * 0.25, 0))
        B.add(p, (0.105, 0.046, 0.042), GOLD, "Halo", rot=(0, 0, math.degrees(a) + 90), studs=[], role="limb", rnd=0.4)
    # ---- tiny legs: one chunky block, flush dark sock + dark paw with 3 cream claw nubs
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            x, y = LEGS[fb]
            X0 = s * x
            bone = "Leg_" + fb + side
            B.add((X0, y, 0.235), (0.165, 0.17, 0.17), CARAMEL, bone, bot=(0.94, 0.94), rnd=0.36)
            B.add((X0, y - 0.015, 0.05), (0.185, 0.195, 0.05), NOSE, bone, studs=[], role="limb", rnd=0.4)
            for gx in (-0.085, 0.0, 0.085):
                B.add((X0 + gx, y - 0.212, 0.035), (0.026, 0.026, 0.024), (250, 236, 214), bone, studs=[])
    # ---- wings
    for s, side in ((1, "L"), (-1, "R")):
        feather_wing(B, s, side)
    try:
        B.build()
    finally:
        bk.STYLE["mix"] = mix0
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.12, 0.60), "Root", tail=(0, -0.4, 0))
    k.joint("Head", (0, -0.52, 0.80), "Spine", tail=(0, -0.35, 0.1))          # throat pivot (back-bottom of the head)
    k.joint("Flower", FLOWER_C, "Head", tail=(0, 0, 0.15))
    k.joint("Halo", HALO_C, "Head", tail=(0, 0, 0.15))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.30, -0.60, 1.33), "Head", tail=(0, 0, 0.15))
        for fb in ("F", "B"):
            x, y = LEGS[fb]
            k.joint("Leg_" + fb + side, (s * x, y, LEG_TOP), "Spine", tail=(0, 0, -0.3))
        k.joint("Wing_" + side, X(WING.S, s), "Spine")
        k.joint("WingTip_" + side, X(WING.W, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.1))


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    P = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
         ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ("Head", "Halo", "Flower", "Ear_L", "Ear_R", "Spine", "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"):
            P.append((w, b))
    P += [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
          ("Head", "Leg_FL"), ("Head", "Leg_FR"), ("Halo", "Head"), ("Halo", "Flower"), ("Halo", "Ear_L"),
          ("Halo", "Ear_R"), ("Flower", "Ear_L"), ("Flower", "Ear_R")]
    return P


def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.13, "Wing_" + sd))     # wing root knuckle on the back
    return out


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side=side)


def ears(k, f, l=0.0, r=None, back=0.0):
    r = l if r is None else r
    k.key("Ear_L", f, rot=(back, 0, l))
    k.key("Ear_R", f, rot=(back, 0, -r))


def pivot_loc(k, bone, pitch, P):
    """loc that makes a pitch of `bone` turn about the rest point P instead of its joint"""
    J = k.J[bone]
    q = Quaternion((1, 0, 0), math.radians(pitch))
    Pv = Vector(P)
    return tuple(Pv + q @ (J - Pv) - J)


def idle(k):
    """zen celestial capybara: slow breath, humming head tilt, halo bob, flower sway, a cute double wing flutter,
    a right-ear twitch."""
    n = 72
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n)
        k.key("Spine", f, rot=(1.0 * s, 0, 1.6 * pk.wave(f, n, 0.1)), loc=(0, 0, 0.014 * (1 + s) / 2))
        k.key("Head", f, rot=(-2.5 * pk.wave(f, n, 0.25), 4 * pk.wave(f, n, 0.1), 6 * pk.wave(f, n, 0.0, 2)))
        k.key("Halo", f, rot=(5 * pk.wave(f, n, 0.3), 0, 5 * pk.wave(f, n, 0.55)),
              loc=(0, 0, 0.05 * (1 + pk.wave(f, n, 0.15, 2)) / 2))
        k.key("Flower", f, rot=(0, 0, 9 * pk.wave(f, n, 0.4, 2)))
    for f, up, tp in ((0, 0, 0), (27, 0, 0), (31, 22, -14), (34, -6, 6), (37, 24, -16), (40, -6, 6), (45, 0, 0), (72, 0, 0)):
        wings(k, f, up, 0, 0, tp)
    for f, a in ((0, 0), (54, 0), (57, -22), (60, 6), (64, 0), (n, 0)):
        ears(k, f, 0, a)
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 24

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.5 * pk.wave(f, n, 0, 2), 0, 2.5 * pk.wave(f, n)), loc=(0, 0, 0.035 * b))
        k.key("Head", f, rot=(-3 * pk.wave(f, n, 0.12, 2), 4 * pk.wave(f, n, 0.1), -2 * pk.wave(f, n, 0.05)))
        wings(k, f, -6 + 6 * pk.wave(f, n, 0.1, 2), -8, 0, 4 * pk.wave(f, n, 0.0, 2))
        ears(k, f, 5 * pk.wave(f, n, 0.2, 2), 5 * pk.wave(f, n, 0.2, 2))
        k.key("Halo", f, rot=(3 * pk.wave(f, n, 0.2, 2), 0, 2 * pk.wave(f, n, 0.25)), loc=(0, 0, 0.03 * pk.wave(f, n, 0.3, 2)))
        k.key("Flower", f, rot=(0, 0, 8 * pk.wave(f, n, 0.35, 2)))
    legs = [("Leg_FL", 0.0), ("Leg_BR", 0.0), ("Leg_FR", 0.5), ("Leg_BL", 0.5)]
    return roll_walk(k, n, legs, 0.12, 0.08, body, 0.5, 0.20)


def roll_walk(k, n, legs, SH, lift, body, duty, edge):
    """the kit's walk_cycle, but each single-bone foot target is raised by edge * |sin(leg angle)|: the rigid paw rolls
    on its toe / heel edge instead of dipping a corner into the floor (ground check)"""
    import bpy
    k.new_action("walk", n, True)
    for f in range(0, n + 1, 2):
        body(f)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg, off in legs:
            g = pk.gait_target(k, leg, f, n, off, SH, lift, duty)
            J = k.J[leg]
            dy = g.y - J.y
            k.solve_leg(leg, f, Vector((g.x, g.y, g.z + edge * abs(dy) / math.hypot(dy, J.z))))
    k.finish()
    k.meta["walk_cycle"] = n
    k.meta["legs"] = legs
    k.meta["duty"] = duty
    return 2 * SH / duty


# ---- flight
FLY_N = 22
FLY_LIFT = 0.22          # flight poses ride clear of the floor (tucked paws hang below the belly)
PITCH = 10.0


def fly_legs(k, f, ph, amt=1.0):
    for leg in LEGS4:
        fr = leg[4] == "F"
        w = math.sin(2 * math.pi * (ph - (0.10 if fr else 0.22)))
        base = 56 if fr else 72
        k.key(leg, f, rot=(amt * (base + 12 * w), 0, 0), loc=(0, 0, 0.0))


def fly_pose(k, f, ph, legs=True):
    w = wing3.stroke(ph, top=30.0, bot=-46.0, sweep=12.0, twist=10.0, fold=30.0)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    k.key("Spine", f, rot=(PITCH - 2.5 * math.sin(2 * math.pi * (ph - 0.1)), 0, 0),
          loc=(0, 0, FLY_LIFT + 0.08 * math.cos(2 * math.pi * (ph - 0.45))))
    k.key("Head", f, rot=(-12 - 2 * math.sin(2 * math.pi * (ph - 0.3)), 0, 0))
    lag = math.cos(2 * math.pi * (ph - 0.13))
    ears(k, f, 0, 0, back=-24 - 4 * lag)
    k.key("Halo", f, rot=(-8 + 4 * lag, 0, 0), loc=(0, 0.04, -0.03 * math.cos(2 * math.pi * (ph - 0.45))))
    k.key("Flower", f, rot=(12 + 8 * lag, 0, 0))
    if legs:
        fly_legs(k, f, ph)


def fly(k):
    n = FLY_N
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, f / n)
    k.finish()


def rest_keys(k, f, z=0.0, pitch=0.0):
    k.key("Spine", f, rot=(pitch, 0, 0), loc=(0, 0, z))
    k.key("Head", f, rot=(0, 0, 0))
    wings(k, f, 0, 0, 0, 0)
    ears(k, f, 0, 0)
    k.key("Halo", f, rot=(0, 0, 0), loc=(0, 0, 0))
    k.key("Flower", f, rot=(0, 0, 0))


def takeoff(k):
    """crouch with the wings lifted high (0-10), LAUNCH at 11 on a big downstroke + leg push, into flight"""
    n = 27
    k.new_action("takeoff", n, False)
    rest_keys(k, 0)
    for f, z, p, w in ((6, -0.07, 4, (26, -8, -4, -10)), (10, -0.09, 6, (34, -4, -6, -16)),
                       (13, 0.20, -6, (-34, 10, 8, 4)), (17, 0.32, 4, (18, 0, 0, -10))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Head", f, rot=(-6 - p * 0.5, 0, 0))
        wings(k, f, *w)
        ears(k, f, 0, 0, back=-10 if f >= 13 else 0)
        k.key("Halo", f, rot=(0, 0, 0), loc=(0, 0, 0.02))
        k.key("Flower", f, rot=(0, 0, 0))
    fly_pose(k, 22, 0.0, legs=False)
    fly_pose(k, n, 0.22, legs=False)
    import bpy
    k.bake_bezier_now()
    for f in range(0, 12):
        bpy.context.scene.frame_set(f)
        for leg in LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f, a in ((14, 0.45), (19, 0.85)):
        fly_legs(k, f, 0.0, a)
    fly_legs(k, 22, 0.0)
    fly_legs(k, n, 0.22)
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """flare (nose up, wings forward as an air brake, legs reach), touch down at 16, absorb, settle"""
    n = 27
    k.new_action("land", n, False)
    fly_pose(k, 0, 0.0)
    for f, z, p, w in ((7, 0.10, -12, (26, 18, -10, -12)), (12, 0.06, -6, (-14, 10, -6, 0)),
                       (16, -0.07, 4, (10, 0, 0, -6)), (21, 0.02, -1, (2, 0, 0, -2))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Head", f, rot=(-5 - p * 0.3, 0, 0))
        wings(k, f, *w)
        ears(k, f, 0, 0, back=-12 if f < 16 else 0)
        k.key("Halo", f, rot=(0, 0, 0), loc=(0, 0, 0.03 if f < 21 else 0.0))
        k.key("Flower", f, rot=(0, 0, 0))
    rest_keys(k, n)
    for leg in LEGS4:
        k.key(leg, 7, rot=(-20 if leg[4] == "F" else -8, 0, 0), loc=(0, 0, 0))
    import bpy
    k.bake_bezier_now()
    for f in range(16, n + 1):
        bpy.context.scene.frame_set(f)
        for leg in LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(16 / n, 3)}


def roar(k):
    """CELESTIAL BLESSING: rears up on her hind legs (front paws up), wings spread wide and high with a happy shimmer,
    the halo floats up and spins, then she settles."""
    n = 54
    k.new_action("roar", n, False)
    hip = (0, LEGS["B"][1], LEG_TOP)
    for f, sp, hd, up, tp, halo, rear in ((0, 0, 0, 0, 0, 0.0, 0), (10, 5, 3, -4, 4, 0.0, 0),
                                          (20, -22, -8, 20, -24, 0.14, 1), (36, -22, -10, 22, -26, 0.16, 1),
                                          (46, 3, 2, -2, 4, 0.02, 0), (54, 0, 0, 0, 0, 0.0, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=pivot_loc(k, "Spine", sp, hip))
        k.key("Head", f, rot=(hd, 0, 0))
        wings(k, f, up, -4 * rear, 0, tp)
        k.key("Halo", f, rot=(0, 0, 40 * rear), loc=(0, 0, halo))
        k.key("Flower", f, rot=(0, 0, 10 * rear))
        ears(k, f, 8 * rear, 8 * rear)
    for f in range(22, 36, 4):          # happy wing shimmer while up
        w = 1 if (f // 4) % 2 else -1
        wings(k, f, 21 + 5 * w, -4, 0, -25 - 4 * w)
    cm.plant(k, n, legs=["Leg_BL", "Leg_BR"])
    cm.plant(k, n, legs=["Leg_FL", "Leg_FR"], frames=list(range(0, 11)) + list(range(47, n + 1)))
    for f in (16, 28, 40):
        for leg in ("Leg_FL", "Leg_FR"):
            k.key(leg, f, rot=(-40 if f != 40 else -12, 0, 0), loc=(0, 0, 0))
    k.finish(loop=False)


def happy(k):
    """SIGNATURE (Cvetibara only) - JOYFUL HOP: anticipation crouch, springs up with a double wing flap while her
    halo spins a full turn and the flower twirls, lands softly and wiggles her ears."""
    import bpy
    n = 36
    k.new_action("act_happy", n, False)
    P = [(0, 0.00, 0, 0, 0, 0), (6, -0.06, 4, 6, -6, 6), (12, 0.34, -6, -10, 34, -10), (16, 0.42, -4, -8, -12, -6),
         (20, 0.34, -2, -6, 34, -10), (25, 0.00, 3, 4, -6, 6), (29, -0.03, 2, 3, 6, 2), (36, 0.00, 0, 0, 0, 0)]
    for f, bz, bp, hp, wr, er in P:
        k.key("Spine", f, rot=(bp, 0, 0), loc=(0, 0, bz))
        k.key("Head", f, rot=(hp, 0, 0))
        wings(k, f, wr, 0, 0, -wr * 0.4)
        ears(k, f, er, er)
        k.key("Flower", f, rot=(0, 0, er * 3))
    for f, a, z in ((0, 0, 0), (8, 0, 0), (14, 120, 0.06), (20, 240, 0.08), (26, 360, 0.02), (36, 360, 0)):
        cm.key_axis(k, "Halo", f, (0, 0, 1), a, loc=(0, 0, z))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        if 9 <= f <= 24:
            u = math.sin(math.pi * (f - 9) / 15)
            for leg in LEGS4:
                k.key(leg, f, rot=((-16 if leg[4] == "F" else 16) * u, 0, 0), loc=(0, 0, 0))
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
    happy(k)
    return stride
