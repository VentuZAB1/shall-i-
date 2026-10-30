# Forest Stag (Wood egg #2, T1 Grass, quad) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the royal stag"): an adult
# red-deer stag: deep chest tucking up to a narrow flank, long jointed legs with knees, hocks and split black hooves,
# a long neck in two bones (Neck + Neck2, for the antler scratch) under a shaggy dark mane, a long narrow head with
# narrow emerald eyes under heavy brows, a black nose, a pale rump patch, and a royal 12-point rack (brow, bez, trez
# and a crown of 3 per side, bone-white tips) with 3 hanging emerald moss drapes per antler.
# Old chibi version: _tools/chibi_specs/ForestStag.py
import math
from mathutils import Vector, Matrix, Euler

DISPLAY = "Forest Stag"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 11.0             # gate 2026-10-09: withers ~5 studs at x1 (the rack adds the rest)

FLANK = (168, 102, 64)      # chestnut flanks (Roblox renders ~0.6x darker -> deep chestnut in game)
BACK = (120, 74, 48)        # dark back / saddle / face blaze
MANE = (86, 60, 46)         # shaggy neck mane, brows, tail top
PALE = (230, 210, 170)      # belly, throat, rump patch, lip
ANTLER = (212, 192, 150)
TIP = (246, 238, 216)       # bone-white tine tips
HOOF = (30, 24, 22)
EMERALD = (40, 220, 130)    # THE accent: hanging moss, eyes
EMERALD_D = (24, 150, 92)
EYE = (70, 240, 150)
EYE_HOT = (210, 255, 226)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
MOUTH = (86, 18, 30)

PITCH = 0.0445              # stud pitch: 0.042 x (U / U_raiju), U = model height / HEIGHT

# leg joints (left side): hip/shoulder, knee(stifle)/elbow, ankle(hock)/fetlock, hoof centre
LEGS = {"F": ((0.11, -0.40, 0.80), (0.11, -0.32, 0.55), (0.11, -0.37, 0.10), (0.11, -0.40, 0.04)),
        "B": ((0.115, 0.36, 0.82), (0.115, 0.22, 0.55), (0.115, 0.46, 0.30), (0.115, 0.41, 0.04))}
N0, N1, N2 = Vector((0, -0.44, 0.88)), Vector((0, -0.60, 1.08)), Vector((0, -0.75, 1.27))   # neck base, mid, throat
EYE_P = (0.074, -0.905, 1.318)
EYE_YAW = 40
BEAM = [(0.05, -0.80, 1.42), (0.17, -0.72, 1.53), (0.30, -0.60, 1.68), (0.385, -0.50, 1.86), (0.40, -0.47, 2.03)]
EAR = ((0.085, -0.69, 1.37), (0.27, -0.64, 1.375))     # ear root, tip (left)
TAILP = [(0, 0.555, 0.95), (0, 0.65, 0.83)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def eye_frames(s):
    R = Euler((0, math.radians(-s * 18), math.radians(s * EYE_YAW)), "XYZ").to_matrix()
    Rb = Euler((0, math.radians(-s * 22), math.radians(s * (EYE_YAW - 8))), "XYZ").to_matrix()
    return R, Rb


def tine(B, base, d, L, w, bone="Head"):
    """antler tine: antler-coloured shaft + bone-white tip"""
    d = Vector(d).normalized()
    m = base + d * L * 0.62
    B.seg(base, m, w, w, ANTLER, bone, ext=0.02, top=(0.78, 0.78), role="limb")
    B.spike(m - d * 0.01, d, L * 0.40, w * 0.8, TIP, bone, top=(0.15, 0.15))


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=53, tier=1, plates=False, th=0.50)
    # ---------------- torso: deep ribcage tapering underneath, sloped tuck up to a narrow flank, rump rotated -8
    B.add((0, -0.24, 0.77), (0.17, 0.32, 0.25), FLANK, "Chest", bot=(0.66, 0.56), top=(0.90, 0.95), rnd=0.30)
    B.add((0, -0.34, 0.985), (0.13, 0.22, 0.055), BACK, "Chest", top=(0.55, 0.75), rnd=0.3)          # withers
    B.seg((0, -0.14, 0.615), (0, 0.24, 0.73), 0.12, 0.08, FLANK, "Spine", top=(0.82, 0.75), side=(1, 0, 0))
    B.add((0, 0.10, 0.845), (0.128, 0.21, 0.145), FLANK, "Spine", bot=(0.72, 0.70), top=(0.95, 1), rnd=0.30)
    B.add((0, 0.36, 0.83), (0.148, 0.19, 0.17), FLANK, "Spine", rot=(-8, 0, 0), top=(0.84, 0.90), bot=(0.85, 0.9))
    B.add((0, 0.04, 0.985), (0.13, 0.30, 0.025), BACK, "Spine", top=(0.85, 1))                         # saddle
    B.add((0, 0.36, 0.995), (0.10, 0.16, 0.02), BACK, "Spine", rot=(-8, 0, 0))
    # pale underside following the slope, pale chest front, cream rump patch
    B.add((0, -0.25, 0.515), (0.10, 0.17, 0.022), PALE, "Chest", bot=(0.8, 0.9), studs=[])
    B.seg((0, -0.14, 0.53), (0, 0.22, 0.643), 0.08, 0.02, PALE, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    B.add((0, 0.535, 0.815), (0.09, 0.02, 0.10), PALE, "Spine", rot=(-8, 0, 0), bot=(0.6, 1), studs=[])
    # ---------------- neck (2 bones) + shaggy dark mane on the throat and sides
    d1 = (N1 - N0).normalized()
    B.seg(N0 - d1 * 0.10, N1, 0.125, 0.155, FLANK, "Neck", top=(0.88, 0.84), ext1=0.04)
    B.seg(N1, N2, 0.105, 0.125, FLANK, "Neck2", top=(0.72, 0.66), ext=0.04)
    for dx in (-0.035, 0.035):                                                                       # nape tufts
        B.spike(N2 + Vector((dx, 0.07, 0.07)), (dx * 2, math.cos(math.radians(30)), math.sin(math.radians(30))), 0.10,
                0.04, MANE, "Neck2", top=(0.15, 0.3))
    B.seg((0, -0.56, 0.86), (0, -0.67, 1.005), 0.07, 0.02, PALE, "Neck", side=(1, 0, 0), ext=0.0)       # throat
    B.seg((0, -0.67, 1.005), (0, -0.82, 1.18), 0.064, 0.02, PALE, "Neck2", side=(1, 0, 0), ext=0.01)
    d2 = (N2 - N1).normalized()
    up2 = Vector((0, -d2.z, d2.y)) if d2.z < 0 else Vector((0, d2.z, -d2.y))
    up2 = up2 if up2.z > 0 else -up2
    B.bar(N1 + up2 * 0.126 - d2 * 0.04, N2 + up2 * 0.088, up2, 0.06, 0.008, BACK, "Neck2", studs=[], bevel=0.003)
    B.seg(N0 - d1 * 0.02, N0.lerp(N1, 0.95), 0.138, 0.168, MANE, "Neck", top=(0.86, 0.82), rnd=0.3)  # mane sleeve
    for t, L in ((0.10, 0.12), (0.32, 0.18), (0.55, 0.22), (0.78, 0.20)):                             # throat locks
        c = N0.lerp(N1, t) + Vector((0, -0.11, -0.12))
        for dx, LL in ((0.0, L), (0.06, L * 0.8), (-0.06, L * 0.8)):
            LL = min(LL, c.z - 0.70)
            B.seg(c + Vector((dx, 0, 0)), c + Vector((dx * 1.4, 0.10 + 0.25 * LL, -LL)), 0.042, 0.022, MANE, "Neck",
                  side=(1, 0, 0), top=(0.15, 0.6), ext=0.02, role="limb")
    for s in (1, -1):                                                                                  # side shag
        for t, L in ((0.25, 0.17), (0.6, 0.17), (0.92, 0.14)):
            c = N0.lerp(N1, t) + Vector((s * 0.12, 0.0, -0.03))
            B.seg(c, c + Vector((s * 0.06, 0.13, -L)), 0.045, 0.02, MANE, "Neck", side=(0, 1, 0), top=(0.15, 0.6),
                  ext=0.02, role="limb")
    for t, L in ((0.15, 0.12), (0.55, 0.12)):                                                          # dorsal crest
        c = N0.lerp(N1, t) + Vector((0, 0.10, 0.11))
        B.spike(c, (0, 0.9, 0.5), L, 0.05, MANE, "Neck", top=(0.15, 0.3))
    # ---------------- head (pivot at the throat): braincase, long narrow face, black nose, heavy brows
    B.seg((0, -0.74, 1.37), (0, -0.98, 1.25), 0.088, 0.092, FLANK, "Head", top=(0.84, 0.86), rnd=0.25)
    B.seg((0, -0.92, 1.265), (0, -1.14, 1.125), 0.062, 0.068, FLANK, "Head", top=(0.84, 0.82), ext=0.03)
    B.seg((0, -0.80, 1.43), (0, -1.06, 1.25), 0.05, 0.02, BACK, "Head", side=(1, 0, 0), top=(0.6, 1))   # face blaze
    B.add((0, -1.16, 1.135), (0.05, 0.03, 0.045), BLACK, "Head", rot=(-32, 0, 0), role="detail", bevel=0.01)  # nose
    B.seg((0, -0.98, 1.155), (0, -1.15, 1.07), 0.056, 0.016, PALE, "Head", side=(1, 0, 0), top=(0.8, 1))  # upper lip
    # lower jaw (opens in the rut roar)
    B.seg((0, -0.86, 1.19), (0, -1.12, 1.045), 0.05, 0.026, PALE, "Jaw", top=(0.8, 1), ext=0.02)
    B.add((0, -1.0, 1.133), (0.032, 0.10, 0.005), MOUTH, "Jaw", rot=(29, 0, 0), studs=[], role="detail", bevel=0.002)
    # narrow emerald eyes + heavy brows + dark tear-gland streaks
    for s in (1, -1):
        R, Rb = eye_frames(s)
        c = X(EYE_P, s)

        def P(Rm, dx, dy, dz):
            return c + Rm @ Vector((s * dx, dy, dz))
        B.add(P(R, 0, 0, 0), (0.05, 0.010, 0.024), BLACK, "Head", R=R, studs=[], role="detail", bevel=0.004)
        B.add(P(R, 0.002, -0.008, 0), (0.042, 0.006, 0.013), EYE, "Head", R=R, studs=[], role="detail", bevel=0.003)
        B.add(P(R, 0.010, -0.012, 0.002), (0.018, 0.004, 0.006), EYE_HOT, "Head", R=R, studs=[], role="detail",
              bevel=0.002)
        B.add(P(Rb, -0.012, 0.006, 0.045), (0.07, 0.032, 0.026), MANE, "Head", R=Rb, role="detail", bevel=0.01)
        B.bar(P(R, -0.045, -0.004, -0.012), P(R, -0.075, -0.004, -0.085), R @ Vector((0, -1, 0)), 0.022, 0.006,
              MANE, "Head", studs=[], bevel=0.003, top=(1, 0.3))
    # ears: leaf-shaped, set back, pale inner
    for s, side in ((1, "L"), (-1, "R")):
        r0, r1 = X(EAR[0], s), X(EAR[1], s)
        d = (r1 - r0).normalized()
        B.seg(r0, r1, 0.048, 0.017, FLANK, "Ear_" + side, side=(0, -0.3, 1), top=(0.25, 0.8), ext=0.03, role="limb")
        B.seg(r0 + d * 0.03 + Vector((0, -0.016, 0)), r1 - d * 0.02 + Vector((0, -0.016, 0)), 0.026, 0.005, PALE,
              "Ear_" + side, side=(0, -0.3, 1), top=(0.3, 1), studs=[], role="detail")
    # ---------------- antlers: burr, beam in 4 tapering segments, 6 tines per side, 3 hanging moss drapes
    for s in (1, -1):
        P = [X(p, s) for p in BEAM]
        B.add(P[0] + Vector((0, 0, 0.01)), (0.042, 0.042, 0.022), ANTLER, "Head", rnd=0.3, role="limb")   # burr
        for (a, b), w in zip(zip(P, P[1:]), (0.035, 0.031, 0.028, 0.025)):
            B.seg(a, b, w, w, ANTLER, "Head", ext=0.025, ext1=0.02, role="limb")
        tine(B, P[0].lerp(P[1], 0.30), (s * 0.15, -1, 0.18), 0.26, 0.027)        # brow tine, over the face
        tine(B, P[0].lerp(P[1], 0.85), (s * 0.25, -1, 0.80), 0.20, 0.024)        # bez
        tine(B, P[2], (s * 0.30, -0.8, 1), 0.20, 0.023)                           # trez
        tine(B, P[4], (s * 0.35, -0.05, 1), 0.17, 0.022)                          # crown cup of 3 (+ the beam tip)
        tine(B, P[4] - Vector((0, 0, 0.03)), (s * 0.15, -0.55, 1), 0.15, 0.02)
        tine(B, P[3].lerp(P[4], 0.6), (s * 0.60, 0.50, 0.95), 0.15, 0.02)
        tine(B, P[4] - (P[4] - P[3]).normalized() * 0.02, (-s * 0.25, 0.25, 1), 0.12, 0.02)
        for t, (a, b), L in ((0.55, (P[1], P[2]), 0.14), (0.3, (P[2], P[3]), 0.17), (0.85, (P[2], P[3]), 0.14)):
            c = a.lerp(b, t) + Vector((s * 0.02, 0.012, -0.012))
            # hanging moss curtain: a flat sheet under the beam + a 3-point fringe, broad face to the front-side
            n = Vector((s * 0.7, -0.7, 0)).normalized()
            w0 = n.cross(Vector((0, 0, 1))).normalized()
            B.add(c + Vector((0, 0, 0.012)), (0.045, 0.04, 0.03), EMERALD_D, "Head", rnd=0.35, role="limb")  # wrap
            top = c - Vector((0, 0, 0.01))
            B.seg(top, top - Vector((0, 0, L * 0.45)), 0.048, 0.007, EMERALD_D, "Head", side=w0, ext=0.015,
                  top=(0.85, 1), role="limb")
            for dw, LL, col in ((-0.03, 0.42, EMERALD), (0.0, 0.62, EMERALD), (0.032, 0.35, EMERALD_D)):
                r0 = top - Vector((0, 0, L * 0.40)) + w0 * dw + n * 0.004
                B.seg(r0, r0 - Vector((0, 0, L * LL)) + w0 * dw * 0.4, 0.017, 0.006, col, "Head", side=w0, ext=0.01,
                      top=(0.12, 1), role="limb")
    # ---------------- legs: thin and long, knee / hock, pastern, split black hooves
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, Pp = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.08)), K, 0.06, 0.09, FLANK, leg, ext1=0.03, top=(0.85, 0.72))   # upper arm
                kn = K.lerp(A, 0.52)
                B.seg(K, kn, 0.042, 0.052, FLANK, shin, top=(0.82, 0.78), ext=0.03)                        # forearm
                B.add(kn, (0.038, 0.04, 0.035), FLANK, shin, rnd=0.3, role="limb")                         # knee
                B.seg(kn, A, 0.03, 0.033, FLANK, shin, ext=0.01, ext1=0.02)                                # cannon
            else:
                B.seg(H + Vector((0, 0.03, 0.08)), K, 0.075, 0.13, FLANK, leg, bot=(0.85, 1), top=(0.72, 0.6),
                      ext1=0.03)                                                                           # thigh
                B.seg(K, A, 0.045, 0.06, FLANK, shin, top=(0.75, 0.62), ext=0.03, ext1=0.02)              # gaskin
                B.seg(A + Vector((0, 0.01, 0.02)), Pp + Vector((0, 0.03, 0.06)), 0.03, 0.034, FLANK, foot, ext=0.02)
            # pastern + split hooves (dark socks on the pastern)
            pt = Pp + Vector((0, 0.025, 0.07))
            B.seg(A, pt, 0.028, 0.03, BACK, foot, ext=0.01)
            for gx in (-0.017, 0.017):
                B.add(Pp + Vector((gx, -0.005, 0)), (0.016, 0.04, 0.04), HOOF, foot, top=(0.9, 0.7), role="limb",
                      bevel=0.008)
    # ---------------- short tail: dark top, pale under
    T0, T1 = Vector(TAILP[0]), Vector(TAILP[1])
    B.seg(T0, T1, 0.045, 0.03, PALE, "Tail1", side=(1, 0, 0), top=(0.55, 0.65), ext=0.04, role="limb")
    B.seg(T0 + Vector((0, -0.012, 0.012)), T1 + Vector((0, -0.012, 0.01)), 0.022, 0.026, MANE, "Tail1",
          side=(1, 0, 0), top=(0.6, 0.8), role="limb")
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.22, 0.84), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.06, 0.84), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", tuple(N0), "Chest", tail=tuple((N1 - N0) * 0.8))
    k.joint("Neck2", tuple(N1), "Neck", tail=tuple((N2 - N1) * 0.8))
    k.joint("Head", tuple(N2), "Neck2", tail=(0, -0.35, -0.12))                 # throat pivot
    k.joint("Jaw", (0, -0.86, 1.20), "Head", tail=(0, -0.25, -0.12))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, X(EAR[0], s), "Head", tail=tuple((X(EAR[1], s) - X(EAR[0], s)) * 0.8))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, Pp = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", TAILP[0], "Spine", tail=(0, 0.1, -0.12))


# ------------------------------------------------------------------ animation (FIERCE_PLAN: scent the wind / rut roar /
# act_scratch). k.key rot = (pitch, yaw, roll) deg, armature axes, relative to the parent; pitch + = nose down,
# yaw + = toward the pet's left-back, roll + = the +X side goes down.
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]


def ears(k, f, fl=0.0, fr=None, dl=0.0, dr=None):
    """fl/fr + = the ear turns its opening forward, dl/dr + = the ear droops down"""
    fr = fl if fr is None else fr
    dr = dl if dr is None else dr
    k.key("Ear_L", f, rot=(0, -fl, dl))
    k.key("Ear_R", f, rot=(0, fr, -dr))


def neck(k, f, n1=0.0, n2=0.0, hd=0.0, y1=0.0, y2=0.0, hy=0.0, hr=0.0, jaw=0.0):
    k.key("Neck", f, rot=(n1, y1, 0))
    k.key("Neck2", f, rot=(n2, y2, 0))
    k.key("Head", f, rot=(hd, hy, hr))
    k.key("Jaw", f, rot=(jaw, 0, 0))


def idle(k):
    """SCENT THE WIND: the nose lifts with 3 sniff ticks, the ears swivel independently, an alert FREEZE, then it
    relaxes and dips to nibble low twice, comes back up with one tail flick."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.006 * b))
        k.key("Chest", f, rot=(-0.6 * b, 0, 0))
    #       f   n1   n2   hd   jaw
    P = [(0, 0, 0, 0, 0), (6, -2, -4, -8, 0), (10, -2, -4, -10, 2), (12, -2, -4, -12, 0), (14, -2, -4, -10, 2),
         (16, -2, -4, -12, 0), (18, -2, -4, -10, 2), (20, -2, -4, -12, 0), (48, -2, -4, -12, 0),
         (52, -4, -6, -6, 0), (64, -4, -6, -6, 0), (74, 30, 22, 14, 0), (78, 32, 24, 16, 8), (81, 32, 24, 16, 1),
         (84, 32, 24, 16, 8), (88, 20, 12, 8, 0), (92, 32, 24, 16, 1), (95, 32, 24, 16, 8), (98, 32, 24, 16, 1),
         (110, 0, 0, 0, 0), (120, 0, 0, 0, 0)]
    for f, n1, n2, hd, jaw in P:
        neck(k, f, n1, n2, hd, jaw=jaw)
    for f, fl, fr, dl, dr in ((0, 0, 0, 0, 0), (20, 0, 0, 0, 0), (24, 30, -25, 0, 0), (32, 30, -25, 0, 0),
                              (36, -25, 30, 0, 0), (44, -25, 30, 0, 0), (50, 22, 22, -6, -6), (64, 22, 22, -6, -6),
                              (72, 0, 0, 8, 8), (100, 0, 0, 8, 8), (110, 0, 0, 0, 0), (114, 0, -20, 0, 0),
                              (117, 0, 0, 0, 0), (120, 0, 0, 0, 0)):
        ears(k, f, fl, fr, dl, dr)
    for f, tp, ty in ((0, 0, 0), (52, 0, 0), (54, 25, 0), (62, 25, 0), (66, 0, 0), (104, 0, 0), (106, 22, 10),
                      (109, 0, 0), (120, 0, 0)):
        k.key("Tail1", f, rot=(tp, ty, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish()


def walk(k):
    n = 30

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 1.0 * pk.wave(f, n, 0.0), 1.6 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.02 * b))
        k.key("Chest", f, rot=(0, -1.5 * pk.wave(f, n, 0.25), -1.2 * pk.wave(f, n, 0.25)))
        neck(k, f, 2 + 2.5 * pk.wave(f, n, 0.15, 2), -1 * pk.wave(f, n, 0.2, 2), -2 - 2 * pk.wave(f, n, 0.2, 2),
             hy=1.5 * pk.wave(f, n, 0.25))
        k.key("Tail1", f, rot=(4, 5 * pk.wave(f, n, 0.3), 0))
        ears(k, f, 8, 8)
    return cm.quad_walk(k, n, 0.14, 0.10, body, gait="walk")


def roar(k):
    """RUT ROAR: braces, drops the neck to horizontal and stretches it FORWARD, jaw wide, 3 roaring bouts (the chest
    pumps, the jaw half closes between them), tail flag up; then pitches the head down so the rack points at the
    viewer (threat) and settles."""
    n = 64
    k.new_action("roar", n, False)
    #       f   n1   n2   hd   jaw  chest  z
    P = [(0, 0, 0, 0, 0, 0, 0), (10, 20, 6, -18, 4, 2, -0.03), (16, 24, 8, -26, 30, -2, -0.03),
         (22, 24, 8, -26, 12, 1, -0.03), (26, 24, 8, -27, 31, -3, -0.03), (32, 24, 8, -26, 12, 1, -0.03),
         (36, 24, 8, -27, 32, -3, -0.03), (44, 24, 8, -26, 28, -2, -0.03), (48, 20, 10, 25, 4, 0, -0.02),
         (54, 20, 10, 25, 2, 0, -0.02), (60, 4, 2, 4, 0, 0, 0), (64, 0, 0, 0, 0, 0, 0)]
    for f, n1, n2, hd, jaw, ch, z in P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        neck(k, f, n1, n2, hd, jaw=jaw)
        on = 12 <= f <= 46
        ears(k, f, 0, 0, 22 if on else 0, 22 if on else 0)
        k.key("Tail1", f, rot=(32 if on else 0, 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def scratch(k):
    """SIGNATURE act_scratch - ANTLER SCRATCH: shifts its weight onto the right legs, lifts the left hind leg, curls
    the neck round to the left flank and rakes it with the antler tines (4 strokes, ears flopping in bliss, a tail
    flick on stroke 3), one long last rub, swings the head back, sets the leg down and settles."""
    import bpy
    n = 90
    k.new_action("act_scratch", n, False)
    for f, x, r in ((0, 0, 0), (8, -0.03, -3), (80, -0.03, -3), (90, 0, 0)):
        k.key("Spine", f, rot=(0, 0, r), loc=(x, 0, 0))
    # neck curl to the left flank: (f, n1, y1, n2, y2, hd, hy, hr)
    base = (32, 73, 10, 28, 54, 31, 84)            # contact pose (searched: a tine 0.03 off the left flank)
    P = [(0, 0, 0, 0, 0, 0, 0, 0), (8, 2, 6, 0, 4, 0, 0, 0), (22,) + base]
    rake = (53, 86, 11, 11, 55, 22, 85)            # rake-end (searched: the tine drags 0.15 back + down the flank)
    long = tuple(round(b + (r - b) * 1.3, 1) for b, r in zip(base, rake))      # the long last rub (1.3 x travel)
    for i, f0 in enumerate((22, 32, 42, 52)):
        P.append((f0 + 6,) + rake)                 # drag (6 f) ...
        P.append((f0 + 10,) + base)                # ... and back to contact (4 f)
    P += [(69,) + long, (72,) + base,
          (80, 0, 0, 0, 0, 0, 0, 0), (84, -2, -3, 0, -2, -1, 0, 0), (90, 0, 0, 0, 0, 0, 0, 0)]
    for f, n1, y1, n2, y2, hd, hy, hr in P:
        neck(k, f, n1, n2, hd, y1=y1, y2=y2, hy=hy, hr=hr)
    for f, r in [(0, 0), (22, 0)] + [(f0 + d, 3 * (d == 6)) for f0 in (22, 32, 42, 52) for d in (6, 10)] +             [(69, 3.5), (72, 0), (90, 0)]:
        k.key("Chest", f, rot=(0, 0, r))          # the shoulder leans into the rack on each drag
    for f, fl, dl, dr in ((0, 0, 0, 0), (12, 0, -6, 0), (20, 0, -12, 16), (26, 0, -12, 32), (62, 0, -12, 32), (70, 0, -18, 0), (76, 0, -16, 0),
                          (78, 25, 0, 0), (81, 0, 0, 0), (90, 0, 0, 0)):
        ears(k, f, fl, fl, dl, dr)
    for f, tp, ty in ((0, 0, 0), (40, 0, 0), (43, 22, 14), (47, 0, 0), (90, 0, 0)):
        k.key("Tail1", f, rot=(tp, ty, 0))
    k.bake_bezier_now()

    def lift(f):
        if f <= 10 or f >= 80:
            return 0.0
        u = (f - 10) / 10 if f < 20 else 1.0 if f <= 70 else 1 - (f - 70) / 10
        return 0.5 - 0.5 * math.cos(math.pi * u)

    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if leg == "Leg_BL":
                u = lift(f)
                T = T + Vector((0.02 * u, -0.14 * u, 0.22 * u))
            k.solve_leg(leg, f, T)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    scratch(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"), ("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"),
         ("Head", "Chest"), ("Head", "Spine"), ("Head", "Neck"), ("Jaw", "Chest"), ("Neck2", "Chest"),
         ("Ear_L", "Head"), ("Ear_R", "Head"), ("Ear_L", "Neck2"), ("Ear_R", "Neck2")]
    for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Leg_BL", "Shin_BL", "Foot_BL"):
        P.append(("Head", b))
    for b in ("Leg_BL", "Leg_BR"):
        P.append(("Tail1", b))
    return P


def joints():
    """ear hinges: ignore the sliver where an ear turns against its own root"""
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        p = X(EAR[0], s)
        out.append((p, p, 0.07, "Ear_" + side))
    return out


HEAD_XF = []
