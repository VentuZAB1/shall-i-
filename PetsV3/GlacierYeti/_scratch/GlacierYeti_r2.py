# Glacier Yeti (Glacier egg, BIG 14 %) - FIERCE style (2026-10-27, Glacier update, plan _review/GlacierYeti_plan.md v2):
# a hunched navy snow beast under a Roblox stud skin. Short thick legs, a narrow pelvis, a barrel chest leaning 30 deg
# forward under a trapezius hump, the head sunk low and forward between broad shoulders, long thick arms ending in
# heavy fists that hang near the snow. Broken ice-shelf slabs (smooth, jagged) armour the shoulders and upper arms,
# ice knuckle plates on the fists, thin aurora-green seams along the plate edges (the ONE accent). A wide flat skull
# with a heavy dark brow shelf (V, inner ends low), deep-set pale plate-grey slit eyes in black sockets, a snow muzzle,
# a broad black nose, a jutting underbite jaw with two ivory fangs, dark fists and feet, black claws. No glow, no tail.
import math
from mathutils import Vector, Matrix, Euler

DISPLAY = "Glacier Yeti"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 9.0                  # total height (head top at rest) in studs at x1

POLAR_NAVY = (108, 116, 196)  # torso, legs, head, arms, muzzle (studded)
NAVY_D = (92, 100, 178)       # belly / pelvis, abdominal mass, shins (one step darker)
PLATE_ICE = (206, 226, 240)   # shoulder / arm / knuckle ice slabs (smooth) + the eye slits
AURORA = (120, 240, 160)      # THE accent: plate seam lines ONLY
BROW = (52, 58, 96)           # brow shelf, toes, palms
BLACK = (14, 14, 22)          # claws, eye sockets + pupils, nose
IVORY = (238, 234, 220)       # underbite fangs
MOUTH = (86, 18, 30)

H_MODEL = 1.63                # model height in Blender units (same units-per-stud as the Raiju: 1.498 / 8)
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)   # same world stud size as the Raiju

S = (0.47, -0.22, 1.27)       # shoulder (left)
E = (0.59, -0.30, 0.83)       # elbow
W = (0.56, -0.45, 0.42)       # wrist
FIST = (0.56, -0.48, 0.25)    # fist centre
LEG = ((0.18, 0.10, 0.66), (0.25, -0.10, 0.40), (0.21, 0.04, 0.12))   # hip, knee (forward), ankle
THROAT = Vector((0, -0.40, 1.33))
# hunched torso loft (y, zc, half width, half depth) from the pelvis up and forward to the neck
TORSO = [(0.12, 0.58, 0.20, 0.14), (0.10, 0.73, 0.25, 0.18), (0.06, 0.90, 0.27, 0.20), (0.00, 1.03, 0.33, 0.25),
         (-0.08, 1.16, 0.40, 0.29), (-0.18, 1.27, 0.42, 0.29), (-0.30, 1.35, 0.33, 0.23), (-0.40, 1.40, 0.20, 0.16)]
SPLIT_Z = 0.98                # Spine | Chest split height on the torso loft
_L = {}


def loft():
    if "t" not in _L:
        import curveloft as cl
        _L["t"] = cl.Loft(TORSO, n=2.4, seg=24)
    return _L["t"]


def s_at_z(L, z):
    for i in range(len(L.pts) - 1):
        a, b = L.pts[i].z, L.pts[i + 1].z
        if (a - z) * (b - z) <= 0 and a != b:
            return L.s[i] + (L.s[i + 1] - L.s[i]) * (z - a) / (b - a)
    return L.length


def shell(B, b, za, color, pad=0.03, rnd=0.25, bone=None, **kw):
    """cap over block b from local z = za to its top, following its tapers (ice crust over a deltoid)"""
    t = (za / b.h.z + 1) / 2
    fx = b.bot[0] + (b.top[0] - b.bot[0]) * t
    fy = b.bot[1] + (b.top[1] - b.bot[1]) * t
    hx, hy = b.h.x * fx + pad, b.h.y * fy + pad
    zb = b.h.z + pad
    c = b.world(Vector((0, 0, (za + zb) / 2)))
    return B.add(c, (hx, hy, (zb - za) / 2), color, bone or b.bone, R=b.R,
                 top=((b.h.x * b.top[0] + pad) / hx, (b.h.y * b.top[1] + pad) / hy), rnd=rnd, **kw)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def Rx(d):
    return Matrix.Rotation(math.radians(d), 3, "X")


def fpt(b, lx, lz, off=0.006):
    """point on the FRONT (-y) face of tapered block b at local (lx, lz) + its normal"""
    t = (lz / b.h.z + 1) / 2
    fy = b.bot[1] + (b.top[1] - b.bot[1]) * t
    fx = b.bot[0] + (b.top[0] - b.bot[0]) * t
    p = b.world(Vector((lx * fx, -(b.h.y * fy + off), lz)))
    g = b.h.y * (b.top[1] - b.bot[1]) / (2 * b.h.z)
    return p, (b.R @ Vector((0, -1, g))).normalized()


def slab(B, c, u, v, n, outline, thick, bone, seam_edges=()):
    """broken ice shelf: a smooth jagged flat prism in the plane (u, v) at c (normal n), outline in (u, v) units
    (star-shaped from outline[0]); thin aurora seams along the listed outline edges (i -> i + 1), on the outer face"""
    u, v, n = Vector(u).normalized(), Vector(v).normalized(), Vector(n).normalized()
    pts = [Vector(c) + u * a + v * b for a, b in outline]
    B.poly(pts, thick, PLATE_ICE, bone)
    for i in seam_edges:
        a, b = pts[i], pts[(i + 1) % len(pts)]
        d = (b - a).normalized()
        inward = n.cross(d).normalized()
        cen = sum(pts, Vector()) / len(pts)
        if inward.dot(cen - a) < 0:
            inward = -inward
        o = n * (thick / 2 + 0.004) + inward * 0.022
        B.bar(a + o + d * 0.012, b + o - d * 0.012, n, 0.040, 0.008, AURORA, bone, studs=[], bevel=0.003)
    return pts


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=91, tier=3, plates=False)
    Lt = loft()
    sj = s_at_z(Lt, SPLIT_Z)
    # ================= hunched torso: one curved loft (pelvis -> barrel chest -> neck), split Spine | Chest
    Lt.tube(B, 0.0, sj + 0.05, NAVY_D, "Spine", j1=sj, step=0.08)
    Lt.tube(B, sj - 0.05, Lt.length, POLAR_NAVY, "Chest", j0=sj, step=0.08)
    # trapezius hump bridging the shoulders up to the back of the skull (the hunch)
    B.add((0, -0.14, 1.47), (0.27, 0.20, 0.12), POLAR_NAVY, "Chest", rot=(30, 0, 0), top=(0.55, 0.55), rnd=0.45)
    # chest form (review 1 M4): two pectoral masses + one abdominal mass laid on the loft front, studded
    MX = Matrix(((-1, 0, 0), (0, 1, 0), (0, 0, 1)))
    for z, da, half, out, col, mirror in ((1.24, 0.42, (0.05, 0.17, 0.12), 0.024, POLAR_NAVY, True),
                                          (1.04, 0.0, (0.05, 0.16, 0.09), 0.022, NAVY_D, False)):
        sv = s_at_z(Lt, z)
        c0, T, N, w_, h_ = Lt.at(sv)
        pnt = Lt.surf(sv, -math.pi / 2 + da)
        nrm = (pnt - c0).normalized()
        along = (-T - nrm * (-T).dot(nrm)).normalized()
        if along.z < 0:
            along = -along
        c = pnt + nrm * (out - half[0])
        Rm = bk.frame_from(c, c + along, nrm)
        B.add(c, half, col, "Chest", R=Rm, rnd=0.50)
        if mirror:                                                   # exact mirror for the other pectoral
            B.add(MX @ c, half, col, "Chest", R=MX @ Rm @ MX, rnd=0.50)
    # broken ice sheets frozen onto the hump (shingled, rear edge lifted), aurora seams on their lower edges
    for z, hw, hl, tilt in ((1.25, 0.20, 0.13, 20), (1.10, 0.17, 0.12, 14)):
        sv = s_at_z(Lt, z)
        c0, T, N, w_, h_ = Lt.at(sv)
        p = Lt.surf(sv, math.pi / 2, grow=0.02)
        nrm = (p - c0).normalized()
        v = (-T).normalized()                                   # down the back (toward the pelvis)
        v = (v * math.cos(math.radians(tilt)) + nrm * math.sin(math.radians(tilt))).normalized()
        nrm = Vector((1, 0, 0)).cross(v).normalized()
        if nrm.dot(p - c0) < 0:
            nrm = -nrm
        slab(B, p + nrm * 0.02, (1, 0, 0), v, nrm,
             [(-hw, -hl), (-hw * 0.3, -hl * 1.15), (hw * 0.4, -hl * 0.9), (hw, -hl * 1.05), (hw * 1.05, hl * 0.2),
              (hw * 0.7, hl), (0.0, hl * 0.85), (-hw * 0.6, hl * 1.1), (-hw * 1.05, hl * 0.3)], 0.05,
             "Chest" if z > SPLIT_Z else "Spine", seam_edges=(5, 6, 7))
    # ================= head (pivot at the throat), sunk between the shoulders: wide flat skull, heavy brow V,
    # deep-set pale slit eyes on navy, a snow muzzle + cheek mask, a broad black nose, an underbite jaw with fangs
    B.seg((0, -0.24, 1.38), (0, -0.47, 1.43), 0.19, 0.16, POLAR_NAVY, "Chest", ext=0.04, rnd=0.42)       # neck
    B.add((0, -0.535, 1.475), (0.220, 0.155, 0.150), POLAR_NAVY, "Head", top=(0.80, 0.78), bot=(0.95, 0.95),
          rnd=0.38)                                                                              # skull
    B.add((0, -0.715, 1.418), (0.118, 0.080, 0.066), POLAR_NAVY, "Head", top=(0.78, 0.70), bot=(1.0, 0.9), rnd=0.42)  # muzzle
    B.add((0, -0.785, 1.463), (0.066, 0.022, 0.030), BLACK, "Head", top=(0.75, 1.0), studs=[], role="detail",
          bevel=0.009)                                                                            # broad flat nose
    for s in (1, -1):
        # heavy brow shelf (V, inner end low, 25 deg) overhanging the eyes
        B.add((s * 0.086, -0.694, 1.552), (0.095, 0.060, 0.040), BROW, "Head", rot=(-14, -s * 25, 0),
              role="detail", bevel=0.013)
        # eyes: black socket + pale plate-grey slit + black slit pupil, tilted 20 deg, inner end low (on navy)
        rot = (0, -s * 20, s * 8)
        B.add((s * 0.100, -0.688, 1.497), (0.072, 0.008, 0.025), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.004)
        B.add((s * 0.102, -0.694, 1.497), (0.060, 0.006, 0.0125), PLATE_ICE, "Head", rot=rot, studs=[],
              role="detail", bevel=0.003)
        B.add((s * 0.109, -0.698, 1.499), (0.009, 0.004, 0.0115), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.002)
        # small pointed ears set low on the skull sides
        B.spike((s * 0.19, -0.49, 1.47), (s * 1.0, 0.45, 0.35), 0.11, 0.045, BROW, "Head", top=(0.2, 0.6),
                role="limb")
        # cheek tufts swept back from the jaw line
        for z, dz, L in ((1.37, -0.30, 0.14), (1.44, 0.05, 0.15)):
            B.spike((s * 0.18, -0.58, z), (s * 0.45, 0.85, dz), L, 0.048, POLAR_NAVY, "Head", top=(0.15, 0.4),
                    studs=None, role="limb")
    # jutting lower jaw (underbite) + two ivory fangs rising past the upper lip at the mouth corners
    B.add((0, -0.735, 1.318), (0.148, 0.108, 0.046), POLAR_NAVY, "Jaw", top=(1.0, 0.95), bot=(0.86, 0.9), rnd=0.36)
    B.add((0, -0.705, 1.362), (0.105, 0.040, 0.006), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike((s * 0.112, -0.818, 1.335), (s * 0.22, -0.15, 1.0), 0.10, 0.028, IVORY, "Jaw", top=(0.08, 0.12))
    # ================= arms: tilted deltoid under an ice crust, bulging upper arm, thick forearm, heavy fist
    for s, side in ((1, "L"), (-1, "R")):
        arm, fore, hand = "Arm_" + side, "Fore_" + side, "Hand_" + side
        Sv, Ev, Wv, Fv = X(S, s), X(E, s), X(W, s), X(FIST, s)
        dl = B.add(Sv + Vector((s * 0.04, 0.0, 0.0)), (0.165, 0.17, 0.15), POLAR_NAVY, arm, rot=(0, -s * 20, 0),
                   rnd=0.45)                                                                   # deltoid
        B.seg(Sv, Ev, 0.17, 0.17, POLAR_NAVY, arm, ext=0.0, ext1=0.05, top=(0.82, 0.82), rnd=0.50)   # 0.17 -> 0.14
        B.seg(Ev, Wv, 0.15, 0.15, POLAR_NAVY, fore, ext=0.06, ext1=0.0, top=(0.68, 0.68), rnd=0.50)  # 0.15 -> 0.10
        B.add(Fv, (0.13, 0.14, 0.125), BROW, hand, rnd=0.50)                                           # fist (rounded)
        B.add(Fv + Vector((0, 0.03, -0.11)), (0.105, 0.105, 0.02), BROW, hand, studs=[], rnd=0.3, role="limb")
        for gx in (-0.078, 0.0, 0.078):
            B.spike((Fv.x + gx, Fv.y - 0.125, Fv.z - 0.075), (0, -1, -0.5), 0.08, 0.020, BLACK, hand)
        # 3 ice knuckle plates along the TOP edge of the fist (review 1 M1: the fist front stays smooth BROW)
        for i, gx in enumerate((-0.075, 0.0, 0.075)):
            c = Fv + Vector((gx, -0.075, 0.105))
            slab(B, c, (1, 0, 0), (0, 1, 0.45), (0, -0.45, 1),
                 [(-0.034, -0.045), (0.030, -0.05), (0.036, 0.02), (0.012, 0.048), (-0.030, 0.040)], 0.04, hand)
        # ice shelf 1: a crust over the deltoid (outer end tilted up 20 deg), icicle teeth on its rim, aurora seam
        cap = shell(B, dl, -0.03, PLATE_ICE, pad=0.035, rnd=0.14, nostud=True, role="limb")
        for j, (ly, L, tilt) in enumerate(((-0.08, 0.10, 0.20), (0.07, 0.14, 0.45))):       # 2 rim icicles
            base = cap.world(Vector((s * (cap.h.x - 0.015), ly, -cap.h.z + 0.025)))
            B.spike(base, cap.R @ Vector((s * tilt, 0.15 * (2 * j - 1), -1)), L, 0.042, PLATE_ICE, arm,
                    top=(0.10, 0.35), nostud=True)
        zs = -cap.h.z + 0.032
        hx, hy = cap.h.x + 0.004, cap.h.y + 0.004
        rim = [(-s * hx * 0.55, -hy, Vector((0, -1, 0))), (s * hx, -hy, Vector((s, -1, 0))),
               (s * hx, hy, Vector((s, 1, 0))), (-s * hx * 0.55, hy, Vector((0, 1, 0)))]
        for (xa, ya, na), (xb, yb, nb) in zip(rim, rim[1:]):                        # aurora seam round the rim
            pa, pb = cap.world(Vector((xa, ya, zs))), cap.world(Vector((xb, yb, zs)))
            B.bar(pa, pb, cap.R @ (na + nb).normalized(), 0.040, 0.008, AURORA, arm, studs=[], bevel=0.003)
        # ice shelf 2: a slab on the outer upper arm (jagged, tilted up 20 deg), aurora seam on its lower edge
        Ua = Sv + (Ev - Sv) * 0.42 + Vector((s * 0.145, 0.0, 0.0))
        dn = (Ev - Sv).normalized()
        slab(B, Ua, (0, 1, 0), -dn, (s * math.cos(math.radians(20)), 0, math.sin(math.radians(20))),
             [(-0.14, -0.10), (0.0, -0.14), (0.14, -0.09), (0.12, 0.05), (0.15, 0.12), (-0.02, 0.14), (-0.13, 0.09)],
             0.05, arm, seam_edges=(0, 1, 2))
    # ================= legs: thick thighs, short shins, broad feet with 3 dark toes + black claws
    for s, side in ((1, "L"), (-1, "R")):
        leg, shin, foot = "Leg_" + side, "Shin_" + side, "Foot_" + side
        H, K, A = (X(p, s) for p in LEG)
        B.seg(H + Vector((0, 0, 0.08)), K, 0.19, 0.19, POLAR_NAVY, leg, ext=0.0, ext1=0.04, top=(0.79, 0.79),
              rnd=0.50)                                                                   # thigh 0.19 -> 0.15
        B.seg(K, A, 0.14, 0.14, NAVY_D, shin, ext=0.05, ext1=0.02, top=(0.71, 0.71), rnd=0.50)   # shin 0.14 -> 0.10
        dk = (A - K).normalized()
        B.add(K + dk * 0.10 + Vector((0, 0.06, 0)), (0.11, 0.08, 0.10), NAVY_D, shin, rnd=0.50)   # calf bulge
        B.seg((A.x, A.y + 0.06, 0.065), (A.x, A.y - 0.19, 0.055), 0.125, 0.06, BROW, foot, top=(0.70, 0.78),
              rnd=0.45)                                                                   # wedge foot (heel -> toe)
        for gx in (-0.062, 0.0, 0.062):
            B.add((A.x + gx, A.y - 0.215, 0.042), (0.040, 0.045, 0.040), BROW, foot, rnd=0.45, role="limb")
            B.spike((A.x + gx, A.y - 0.25, 0.035), (0, -1, -0.45), 0.07, 0.017, BLACK, foot)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.06, 0.80), "Root", tail=(0, 0, 0.3))
    k.joint("Chest", (0, 0.02, 0.98), "Spine", tail=(0, -0.2, 0.35))
    k.joint("Head", tuple(THROAT), "Chest", tail=(0, -0.25, 0.1))              # pivot low at the back of the throat
    k.joint("Jaw", (0, -0.62, 1.34), "Head", tail=(0, -0.2, 0))
    k.joint("Mouth", (0, -0.79, 1.38), "Head", tail=(0, -0.1, 0))
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        k.joint("Arm_" + side, Sv, "Chest")
        k.joint("Fore_" + side, Ev, "Arm_" + side)
        k.joint("Hand_" + side, Wv, "Fore_" + side, tail=(0, -0.05, -0.25))
        k.joint("Plate_" + side, tuple(Sv + Vector((s * 0.05, 0, 0.17))), "Arm_" + side, tail=(s * 0.1, 0, 0.1))
        k.add_leg2("Arm_" + side, "Fore_" + side, "Hand_" + side, knee=(s * 1.0, 0.15, 0))   # arm IK (knuckles)
        H, K, A = (X(p, s) for p in LEG)
        k.joint("Leg_" + side, H, "Spine")
        k.joint("Shin_" + side, K, "Leg_" + side)
        k.joint("Foot_" + side, A, "Shin_" + side, tail=(0, -0.25, 0))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Hand_L", "Hand_R"), ("Fore_L", "Fore_R"),
         ("Hand_L", "Fore_R"), ("Hand_R", "Fore_L"), ("Arm_L", "Head"), ("Arm_R", "Head"), ("Head", "Chest"),
         ("Jaw", "Chest")]
    for s in ("L", "R"):
        for a in ("Fore_" + s, "Hand_" + s):
            for b in ("Spine", "Chest", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Foot_L", "Foot_R", "Head", "Jaw"):
                P.append((a, b))
    return P


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        Wv = X(W, s)
        out.append((Wv, Wv, 0.15, "Hand_" + side))
    return out


HEAD_XF = []
