# Forest Stag (Wood egg #2, T1 Grass, quad lovely): a compact fawn-stag in the Steal-an-Egg block style, rebuilt to
# STYLE_BIBLE.md (2026-10-08 pro pass): head held high on a short thick neck, oversized ears with cream linings, a wide
# V of thick antlers (2 tines per side) with leaf clusters and a blossom, lovely eyes with lashes, a cream muzzle with a
# round dark nose, a fluffy 3-tuft cream bib, 8 cream fawn spots along the spine, cream socks over split dark hooves
# and an upright cream-backed tail flag.
# Own moves: idle = ear swivels, snaps to an alert freeze, ALARM STOMP of a fore-hoof, then stretches up to browse a
# high branch; walk = elegant high-stepping walk; roar = elk BUGLE (nose to the sky, antlers laid back, jaw squeal
# + grunts); signature = STOTTING LEAPS (three stiff-legged pronks in place, each higher, tail flag up, proud finish).
import math
from mathutils import Vector

DISPLAY = "Forest Stag"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 9.0

FAWN = (200, 124, 64)
CREAM = (250, 236, 212)
DARK = (64, 42, 32)
ANTLER = (140, 98, 62)
LEAF = (104, 200, 88)
LEAF_D = (66, 160, 74)
BLOSSOM = (255, 168, 206)
POLLEN = (255, 224, 110)
IRIS = (138, 86, 46)            # V 54 %: the pupil stays readable at game distance
MOUTH = (120, 40, 50)
TONGUE = (236, 110, 140)
SHEEN = (246, 244, 250)

# legs: hip, knee, ankle (front knee forward, hind hock back)
LEGS = {"FL": ((0.21, -0.34, 0.82), (0.21, -0.44, 0.45), (0.21, -0.34, 0.10)),
        "BL": ((0.15, 0.34, 0.82), (0.15, 0.44, 0.45), (0.15, 0.34, 0.10))}
PMIX = (0.75, 0.25, 0.0)       # 1x1 + vertical 1x2 only: no 2x1 bars clustering into letter shapes
HEAD_C = Vector((0, -0.74, 1.47))
HEAD_H = Vector((0.36, 0.30, 0.305))          # HW 0.72 = 1.13 TW, HH 0.61 = 1.02 TH


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def frame(u, n):
    """rotation: local x = u, local z = n (surface normal), local y = z x x"""
    from mathutils import Matrix
    z = Vector(n).normalized()
    x = Vector(u)
    x = (x - z * x.dot(z)).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


def flower(B, c, n, u, petal, mid, bone, size=0.04):
    """a "+" flower facing n: 4 rounded petals around a pollen centre"""
    c, n = Vector(c), Vector(n).normalized()
    R = frame(u, n)
    ux, vy = R.col[0], R.col[1]
    for d in (ux, -ux, vy, -vy):
        B.add(c + d * size * 1.15, (size, size, 0.025), petal, bone, R=R, studs=[], role="limb", rnd=0.4)
    B.add(c + n * 0.014, (0.03, 0.03, 0.02), mid, bone, R=R, studs=[], role="limb", rnd=0.3)


def model(k):
    """STYLE_BIBLE ForestStag: compact fawn, head high, oversized ears, a wide V of thick leafy antlers."""
    import blockkit as bk
    B = bk.Blocks(k, seed=53, tier=1)
    D = 0.62
    # ---- one torso: chest 18 % wider / 20 % taller than the hips, 44 % overlap, level back line
    chest = B.add((0, -0.20, 0.80), (0.32, 0.36, 0.30), FAWN, "Chest", bot=(0.92, 1.0), density=D, pmix=PMIX)
    B.add((0, 0.20, 0.84), (0.27, 0.36, 0.25), FAWN, "Spine", bot=(0.90, 0.95), density=D, pmix=PMIX)
    # cream belly + raised V bib with 3 fluffy tufts
    B.add((0, -0.18, 0.505), (0.22, 0.30, 0.03), CREAM, "Chest", studs=[], role="limb")
    B.add((0, -0.575, 0.86), (0.20, 0.05, 0.18), CREAM, "Chest", bot=(0.62, 1), studs=[], role="limb")
    for x, l in ((-0.10, 0.14), (0.0, 0.18), (0.10, 0.14)):
        B.spike((x, -0.60, 0.72), (0, -0.30, -1), l, 0.065, CREAM, "Chest", top=(0.2, 0.35))
    # 8 cream fawn spots: 4 per upper flank, staggered, flush on the TAPERED flank surface (LESSONS 2)
    for s in (1, -1):
        for y, z in ((-0.42, 0.99), (-0.15, 0.95), (0.28, 0.99), (0.46, 0.95)):
            if y < 0.16:      # chest: x = 0.32 * (0.92 + 0.08 t), t over z 0.50..1.10
                t, hx, bt, hz, bone = (z - 0.50) / 0.60, 0.32, 0.92, 0.60, "Chest"
            else:             # hips: x = 0.27 * (0.90 + 0.10 t), t over z 0.59..1.09
                t, hx, bt, hz, bone = (z - 0.59) / 0.50, 0.27, 0.90, 0.50, "Spine"
            xs = hx * (bt + (1 - bt) * t)
            n = Vector((s, 0, -hx * (1 - bt) / hz)).normalized()
            B.add(Vector((s * xs, y, z)) + n * 0.003, (0.045, 0.045, 0.003), CREAM, bone, R=frame((0, 1, 0), n),
                  studs=[], bevel=0.002)
    # ---- short thick neck in the body colour (W 0.46 = 0.72 TW), top buried in the head's back
    B.seg((0, -0.38, 0.98), (0, -0.58, 1.38), 0.26, 0.22, FAWN, "Neck", side=(1, 0, 0), density=0.7, role="mass", pmix=PMIX)
    # ---- head: HW 0.67, HH 0.57, held high
    head = B.add(HEAD_C, HEAD_H, FAWN, "Head", top=(0.94, 0.94), density=0.62, pmix=PMIX)
    hb = HEAD_C.z - HEAD_H.z
    fy = HEAD_C.y - HEAD_H.y
    # cream muzzle (W 0.58 HW, H 0.45 HH, protrudes 0.20, buried 0.11) + round dark nose with sheen + small smile
    muz = B.add((0, fy - 0.045, hb + 0.07), (0.195, 0.155, 0.12), CREAM, "Head", top=(0.88, 1.0), studs=[],
                role="limb")
    mf = fy - 0.20                                   # muzzle front
    B.add((0, mf - 0.03, hb + 0.15), (0.08, 0.04, 0.048), DARK, "Head", studs=[], role="limb")
    B.add((-0.035, mf - 0.072, hb + 0.172), (0.012, 0.004, 0.012), SHEEN, "Head", studs=[], bevel=0.003)
    B.add((0, mf - 0.004, hb + 0.045), (0.034, 0.006, 0.013), DARK, "Head", studs=[], bevel=0.003)
    for s in (1, -1):
        B.add((s * 0.062, mf - 0.004, hb + 0.058), (0.035, 0.006, 0.013), DARK, "Head", rot=(0, -s * 32, 0), studs=[],
              bevel=0.003)
    B.add((0, fy - 0.08, hb - 0.046), (0.15, 0.10, 0.006), MOUTH, "Head", studs=[], bevel=0.003)       # mouth roof
    # lower jaw (opens in the bugle)
    B.add((0, fy - 0.07, hb - 0.085), (0.17, 0.13, 0.04), CREAM, "Jaw", bot=(0.85, 0.9), studs=[], role="limb")
    B.add((0, fy - 0.07, hb - 0.042), (0.14, 0.10, 0.005), MOUTH, "Jaw", studs=[], bevel=0.003)
    B.add((0, fy - 0.10, hb - 0.036), (0.07, 0.05, 0.005), TONGUE, "Jaw", studs=[], bevel=0.003)
    # lovely eyes + 2 lash blocks at each outer corner
    E = B.face_eyes(head, "lovely", IRIS, base=FAWN, z=0.60, pupil_size=(0.10, 0.12), hl_size=(0.08, 0.0), look=(0, -0.6))
    HW = 2 * HEAD_H.x
    for s, side in ((1, "L"), (-1, "R")):
        c = E[side]
        for a, l in ((22, 0.05), (55, 0.045)):
            r = math.radians(a)
            d = Vector((s * math.cos(r), 0, math.sin(r)))
            root = Vector((c.x + s * 0.13 * HW, c.y - 0.012, c.z + 0.11 * HW))
            B.seg(root, root + d * l, 0.009, 0.008, DARK, "Head", side=(0, 1, 0), ext=0.012, studs=[], role="detail")
    # ---- oversized ears (0.5 HH long) with cream linings, pointing out and a little up
    for s, side in ((1, "L"), (-1, "R")):
        root = Vector((s * 0.29, -0.62, hb + 0.42))
        tip = root + Vector((s * 0.37, 0.06, 0.10))
        d = (tip - root).normalized()
        sd = Vector((-d.z, 0, d.x)) * s
        B.seg(root, tip, 0.125, 0.045, FAWN, "Ear_" + side, side=sd, ext=0.04, top=(0.36, 0.8), studs=[], role="limb")
        B.seg(root + d * 0.09 + Vector((0, -0.045, 0)), tip - d * 0.04 + Vector((0, -0.045, 0)), 0.078, 0.008, CREAM,
              "Ear_" + side, side=sd, top=(0.40, 1), studs=[], role="detail")
    # ---- antlers: a wide V (span 1.8 HW), beam >= 0.12 HW, 2 thick tines per side, 2 leaf clusters + 1 blossom each
    ht = hb + 2 * HEAD_H.z
    for s in (1, -1):
        A = [Vector((s * 0.12, -0.70, ht - 0.06)), Vector((s * 0.29, -0.70, ht + 0.14)),
             Vector((s * 0.47, -0.67, ht + 0.28)), Vector((s * 0.60, -0.63, ht + 0.44))]
        for (p0, p1), w in zip(zip(A, A[1:]), (0.055, 0.049, 0.043)):
            B.seg(p0, p1, w, w, ANTLER, "Head", ext=0.035, studs=[], role="limb")
        B.spike(A[3] - (A[3] - A[2]).normalized() * 0.03, A[3] - A[2], 0.11, 0.043, ANTLER, "Head", top=(0.5, 0.5))
        for base, d, L, w in ((A[1].lerp(A[2], 0.15), (s * 0.15, -0.55, 1), 0.22, 0.042),
                              (A[2].lerp(A[3], 0.2), (-s * 0.30, -0.05, 1), 0.22, 0.040)):
            B.spike(base - Vector((0, 0, 0.02)), d, L, w, ANTLER, "Head", top=(0.5, 0.5))
        # leaf clusters: on the outer side of the first fork and at the beam tip; a blossom at the second fork
        for c, sc, angs in ((A[1] + Vector((s * 0.05, 0.02, 0.03)), 1.0, (0, 38, 76)),
                            (A[3] + Vector((s * 0.04, 0.02, 0.06)), 1.0, (-10, 35, 80))):
            for i, (ang, col) in enumerate(zip(angs, (LEAF, LEAF_D, LEAF))):
                r = math.radians(ang)
                d = Vector((s * math.cos(r), 0.20, math.sin(r))).normalized()
                B.seg(c, c + d * 0.17 * sc, 0.065 * sc, 0.024, col, "Head", side=(-d.z, 0, d.x), ext=0.03,
                      top=(0.25, 1), studs=[], role="limb")
        flower(B, A[2] + Vector((0, -0.06, 0.0)), (0, -1, 0), (1, 0, 0), BLOSSOM, POLLEN, "Head")
    # ---- legs: upper + shin along the bones, flush cream socks, split dark hooves
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "B":
                B.seg(H, K, 0.105, 0.13, FAWN, leg, ext=0.10, bot=(0.88, 0.90), studs=[], role="limb")
            else:
                B.seg(H, K, 0.105, 0.115, FAWN, leg, ext=0.12, studs=[], role="limb")
            B.seg(K, A, 0.095, 0.10, FAWN, shin, ext=0.07, density=D, role="limb")
            d = (K - A).normalized()
            B.seg(A, A + d * 0.11, 0.095 * 1.03, 0.10 * 1.03, CREAM, shin, ext=0.005, studs=[], role="limb")
            for gx in (-0.054, 0.054):
                B.add((A.x + gx, A.y - 0.012, 0.05), (0.051, 0.12, 0.05), DARK, foot, studs=[], role="limb")
    # ---- upright tail flag: fawn front, cream back
    B.seg((0, 0.53, 0.98), (0, 0.64, 1.26), 0.10, 0.05, FAWN, "Tail1", side=(1, 0, 0), ext=0.05, top=(0.55, 0.7),
          studs=[], role="limb")
    B.seg((0, 0.582, 1.00), (0, 0.69, 1.25), 0.075, 0.012, CREAM, "Tail1", side=(1, 0, 0), top=(0.55, 1), studs=[],
          role="detail")
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.22, 0.84), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.06, 0.84), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.38, 1.02), "Chest", tail=(0, -0.2, 0.4))
    k.joint("Head", (0, -0.56, 1.23), "Neck", tail=(0, -0.4, 0.05))          # throat pivot
    k.joint("Jaw", (0, -0.86, 1.09), "Head", tail=(0, -0.3, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.29, -0.62, 1.585), "Head", tail=(s * 0.2, 0, 0))
        for fb, parent, knee in (("F", "Chest", (0, -1, 0)), ("B", "Spine", (0, 1, 0))):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.2, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", (0, 0.54, 1.00), "Spine", tail=(0, 0.1, 0.3))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]


def ears(k, f, yl=0.0, yr=0.0, pl=0.0, pr=None):
    """yaw + swivels the ear opening toward the front; pitch + tips it down/back"""
    pr = pl if pr is None else pr
    k.key("Ear_L", f, rot=(0, -yl, pl))
    k.key("Ear_R", f, rot=(0, yr, -pr))


def idle(k):
    """alert forest king: ears swivel independently, snaps to an ALERT freeze, stamps a fore-hoof in alarm, relaxes,
    then stretches up to browse a high branch (nibbles), tail flicks."""
    import bpy
    n = 150
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 5)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.008 * b))
        k.key("Chest", f, rot=(-0.8 * b, 0, 0))
    for f, nk, hd, ly, jw in ((0, 0, 0, 0, 0), (18, 0, 0, 0, 0), (24, -10, -6, 0, 0), (62, -10, -6, 0, 0),
                              (74, 0, 2, 0, 0), (86, 0, 0, 0, 0), (98, -20, -22, -0.06, 0), (102, -20, -22, -0.06, 10),
                              (105, -20, -22, -0.06, 2), (108, -20, -22, -0.06, 10), (111, -20, -22, -0.06, 2),
                              (114, -21, -20, -0.06, 9), (118, -20, -22, -0.06, 1), (130, -2, 0, 0, 0), (150, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, 0, 0), loc=(0, ly, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    for f, yl, yr, pl, pr in ((0, 0, 0, 0, 0), (8, 30, 0, 0, 0), (14, 30, -20, 0, 0), (20, 0, 0, 0, 0),
                              (24, 25, 25, -8, -8), (62, 25, 25, -8, -8), (70, 0, 0, 0, 0), (84, -25, 10, 0, 0),
                              (92, 0, 0, 0, 0), (98, 0, 0, 14, 14), (118, 0, 0, 14, 14), (126, 0, 30, 0, 0),
                              (132, 0, 0, 0, 0), (150, 0, 0, 0, 0)):
        ears(k, f, yl, yr, pl, pr)
    for f, tp, ty in ((0, 0, 0), (10, 0, 0), (12, 30, 8), (15, 0, 0), (68, 0, 0), (70, 30, -8), (73, 0, 0),
                      (134, 0, 0), (136, 30, 8), (139, 0, 0), (150, 0, 0)):
        k.key("Tail1", f, rot=(tp, ty, 0))
    for f, z in ((46, 0), (48, -0.02), (51, 0)):
        k.key("Spine", f, loc=(0, 0, z))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if leg == "Leg_FL" and 36 <= f <= 48:          # ALARM STOMP: lift high, slam down
                u = (f - 36) / 12
                T.z = 0.18 * math.sin(math.pi * min(1.0, u / 0.7) * 0.5) if u < 0.7 else 0.18 * (1 - (u - 0.7) / 0.3) ** 2
                T.y -= 0.04 * math.sin(math.pi * u)
            k.solve_leg(leg, f, T)
    k.finish()
    k.meta["planted"] = ["Leg_FR", "Leg_BL", "Leg_BR"]


def walk(k):
    n = 30

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 1.0 * pk.wave(f, n, 0.0), 1.6 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.025 * b))
        k.key("Chest", f, rot=(0, -1.5 * pk.wave(f, n, 0.25), -1.2 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(-4 + 3 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(-2 - 2.5 * pk.wave(f, n, 0.15, 2), 1.5 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        k.key("Tail1", f, rot=(6, 5 * pk.wave(f, n, 0.3), 0))
        ears(k, f, 10, 10, 0, 0)
    return cm.quad_walk(k, n, 0.14, 0.10, body, gait="walk")


def roar(k):
    """elk BUGLE: braces, swings the head up until the nose points at the sky (antlers lie back), mouth opens and the
    jaw quivers through the long squeal, then three deep grunts on the way down; tail flag up, ears back."""
    n = 72
    k.new_action("roar", n, False)
    for f, ch, nk, hd, jw, tl, z in ((0, 0, 0, 0, 0, 0, 0), (10, 3, 6, 6, 0, 10, -0.03), (22, -6, -24, -34, 22, 40, 0.0),
                                     (46, -6, -26, -36, 24, 40, 0.0), (52, -3, -12, -16, 14, 30, -0.01),
                                     (55, -3, -12, -16, 2, 30, -0.01), (58, -2, -8, -10, 14, 20, -0.01),
                                     (61, -2, -8, -10, 2, 20, -0.01), (64, -1, -4, -4, 10, 10, 0),
                                     (67, 0, -2, -2, 0, 4, 0), (72, 0, 0, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Tail1", f, rot=(tl, 0, 0))
        e = -30 if 16 <= f <= 50 else 0
        ears(k, f, 0, 0, -e * 0.0 + (20 if 16 <= f <= 50 else 0), 20 if 16 <= f <= 50 else 0)
    for f in range(24, 46, 2):
        k.key("Jaw", f, rot=(23 + (2.5 if (f // 2) % 2 else -2.5), 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def pronk(k):
    """SIGNATURE - STOTTING LEAPS: crouch, then three stiff-legged pronks straight up (each higher, tail flag up, legs
    locked straight), absorbing each landing, finishing in a proud head-high pose."""
    import bpy
    n = 104
    k.new_action("act_pronk", n, False)
    jumps = [(12, 28, 0.30), (36, 54, 0.42), (62, 84, 0.55)]      # (launch, land, apex height)
    crouch = {0: 0.0, 8: -0.08, 11: -0.09, 31: -0.08, 34: -0.09, 57: -0.09, 60: -0.10, 88: -0.11, 94: 0.01, 98: 0.0,
              104: 0.0}

    def body_z(f):
        for a, b, h in jumps:
            if a <= f <= b:
                u = (f - a) / (b - a)
                return 4 * h * u * (1 - u)
        keys = sorted(crouch)
        for i in range(len(keys) - 1):
            a, b = keys[i], keys[i + 1]
            if a <= f <= b:
                u = (f - a) / (b - a)
                return crouch[a] + (crouch[b] - crouch[a]) * (0.5 - 0.5 * math.cos(math.pi * u))
        return 0.0

    def air(f):
        return any(a < f < b for a, b, h in jumps)

    for f in range(0, n + 1):
        z = body_z(f)
        p = 0.0
        for a, b, h in jumps:
            if a - 3 <= f <= b + 3:
                u = (f - a) / (b - a)
                p = -6 * math.sin(math.pi * min(max(u, 0), 1)) * (h / 0.55) + (3 if b <= f <= b + 3 else 0)
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(-3 if air(f) else 0, 0, 0))
    for f, nk, hd, tl in ((0, 0, 0, 0), (8, 4, 4, 10), (14, -10, -8, 45), (90, -10, -8, 45), (94, -14, -14, 30),
                          (100, -6, -6, 10), (104, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Tail1", f, rot=(tl, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        ears(k, f, 15 if 14 <= f <= 90 else 0, 15 if 14 <= f <= 90 else 0)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        z = body_z(f)
        for leg in LEGS4:
            s = 1 if leg.endswith("L") else -1
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if air(f) and z > 0:          # locked straight legs, slightly splayed, hooves together under the body
                T = Vector((k.J[leg].x + s * 0.02, k.J[leg].y, z - 0.01))
            k.solve_leg(leg, f, T)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    pronk(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"), ("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Head", "Chest"), ("Head", "Spine"),
         ("Ear_L", "Head"), ("Ear_R", "Head"), ("Ear_L", "Neck"), ("Ear_R", "Neck")]
    for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR"):
        P.append(("Head", b))
    for b in ("Leg_BL", "Leg_BR"):
        P.append(("Tail1", b))
    return P


def joints():
    """ear hinges: ignore the sliver where an ear turns against its own root block"""
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        p = Vector((s * 0.29, -0.62, 1.585))
        out.append((p, p, 0.16, "Ear_" + side))
    return out
