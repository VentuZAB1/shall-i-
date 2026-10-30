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
    for z, da, half, out, col, mirror in ((1.24, 0.42, (0.05, 0.17, 0.12), 0.014, POLAR_NAVY, True),   # sunk (r2)
                                          (1.04, 0.0, (0.05, 0.16, 0.09), 0.016, NAVY_D, False)):
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
    # mouth interior riding the jaw, hidden inside the muzzle when closed: the open jaw (roar 26 deg) shows a dark
    # mouth from the side, never the background (clip review 3)
    B.add((0, -0.69, 1.392), (0.082, 0.062, 0.042), MOUTH, "Jaw", studs=[], role="detail", bevel=0.012)
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
        B.seg(Sv + (Ev - Sv) * 0.28 + Vector((0, -0.07, 0)), Sv + (Ev - Sv) * 0.70 + Vector((0, -0.06, 0)), 0.115,
              0.10, POLAR_NAVY, arm, top=(0.80, 0.80), rnd=0.50)                          # bicep block (r2 NICE)
        B.add(Fv, (0.13, 0.14, 0.125), BROW, hand, top=(0.82, 0.78), rnd=0.40)          # fist: knuckle wedge (r2)
        B.add(Fv + Vector((0, 0.03, -0.11)), (0.105, 0.105, 0.02), BROW, hand, studs=[], rnd=0.3, role="limb")
        for gx in (-0.078, 0.0, 0.078):
            B.spike((Fv.x + gx, Fv.y - 0.125, Fv.z - 0.075), (0, -1, -0.5), 0.08, 0.020, BLACK, hand)
        # 3 ice knuckle plates along the TOP edge of the fist (review 1 M1: the fist front stays smooth BROW)
        for i, gx in enumerate((-0.048, 0.048)):                       # 2 broad low plates (clip r3 NICE 6)
            c = Fv + Vector((gx, -0.075, 0.100))
            slab(B, c, (1, 0, 0), (0, 1, 0.45), (0, -0.45, 1),
                 [(-0.044, -0.045), (0.040, -0.05), (0.046, 0.02), (0.016, 0.048), (-0.040, 0.040)], 0.032, hand)
        # ice shelf 1: a crust over the deltoid (outer end tilted up 20 deg), icicle teeth on its rim, aurora seam
        pl = "Plate_" + side                                       # the crust rides the Plate bone (idle settle)
        cap = shell(B, dl, -0.03, PLATE_ICE, pad=0.035, rnd=0.14, nostud=True, role="limb", bone=pl)
        for ly, L, d in ((0.07, 0.13, (s * 1.0, 0.30, -0.15)),):   # one rim icicle, sweeping OUT and BACK (clip r3)
            base = cap.world(Vector((s * (cap.h.x - 0.015), ly, -cap.h.z + 0.025)))
            B.spike(base, cap.R @ Vector(d), L, 0.042, PLATE_ICE, pl, top=(0.10, 0.35), nostud=True)
        zs = -cap.h.z + 0.032
        hx, hy = cap.h.x + 0.004, cap.h.y + 0.004
        rim = [(-s * hx * 0.55, -hy, Vector((0, -1, 0))), (s * hx, -hy, Vector((s, -1, 0))),
               (s * hx, hy, Vector((s, 1, 0))), (-s * hx * 0.55, hy, Vector((0, 1, 0)))]
        for (xa, ya, na), (xb, yb, nb) in zip(rim, rim[1:]):                        # aurora seam round the rim
            pa, pb = cap.world(Vector((xa, ya, zs))), cap.world(Vector((xb, yb, zs)))
            B.bar(pa, pb, cap.R @ (na + nb).normalized(), 0.040, 0.008, AURORA, pl, studs=[], bevel=0.003)
        # ice shelf 2: a slab on the outer upper arm (jagged, tilted up 20 deg), aurora seam on its lower edge
        Ua = Sv + (Ev - Sv) * 0.50 + Vector((s * 0.145, 0.14, 0.0))      # back +0.14, down to 0.50 (r2 + clip r3)
        dn = (Ev - Sv).normalized()
        OL = [(-0.14, -0.10), (0.0, -0.14), (0.14, -0.09), (0.12, 0.05), (0.15, 0.12), (-0.02, 0.14), (-0.13, 0.09)]
        slab(B, Ua, (0, 1, 0), -dn, (s * math.cos(math.radians(20)), 0, math.sin(math.radians(20))),
             [(a * 0.85, b * 0.75) for a, b in OL], 0.05, arm, seam_edges=(0, 1, 2))     # 25 % shorter
    # ================= legs: thick thighs, short shins, broad feet with 3 dark toes + black claws
    for s, side in ((1, "L"), (-1, "R")):
        leg, shin, foot = "Leg_" + side, "Shin_" + side, "Foot_" + side
        H, K, A = (X(p, s) for p in LEG)
        B.seg(H + Vector((0, 0, 0.08)), K, 0.178, 0.19, POLAR_NAVY, leg, ext=0.0, ext1=0.04, top=(0.84, 0.79),
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
        k.add_leg2("Arm_" + side, "Fore_" + side, "Hand_" + side, knee=(s * 0.89, 0.46, 0))  # = the modelled elbow
        H, K, A = (X(p, s) for p in LEG)
        k.joint("Leg_" + side, H, "Spine")
        k.joint("Shin_" + side, K, "Leg_" + side)
        k.joint("Foot_" + side, A, "Shin_" + side, tail=(0, -0.25, 0))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(s * 0.31, -0.95, 0))   # = the modelled knee
        # VFX anchors (plan section 8): bones without mesh
        k.joint("FX_ShardBurst_" + side, tuple(X(FIST, s) + Vector((0, -0.10, -0.08))), "Hand_" + side,
                tail=(0, -0.1, 0))
        k.joint("FX_AuroraDust_" + side, tuple(Sv + Vector((s * 0.20, 0, 0.12))), "Plate_" + side, tail=(s * 0.1, 0, 0))
    k.joint("FX_SnowPuff", (0, -0.30, 0.95), "Chest", tail=(0, -0.1, 0))
    k.joint("FX_BreathCloud", (0, -0.84, 1.37), "Mouth", tail=(0, -0.1, 0))


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Hand_L", "Hand_R"), ("Fore_L", "Fore_R"),
         ("Hand_L", "Fore_R"), ("Hand_R", "Fore_L"), ("Arm_L", "Head"), ("Arm_R", "Head"), ("Head", "Chest"),
         ("Jaw", "Chest"), ("Plate_L", "Head"), ("Plate_R", "Head"), ("Plate_L", "Jaw"), ("Plate_R", "Jaw")]
    for s in ("L", "R"):
        for a in ("Fore_" + s, "Hand_" + s):
            for b in ("Spine", "Chest", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Foot_L", "Foot_R", "Head", "Jaw"):
                P.append((a, b))
    return P


def joints():
    out = [((-0.26, -0.44, 1.42), (0.26, -0.44, 1.42), 0.18, "Head"),      # the skull sits in the neck sleeve
           ((0, -0.12, 0.66), (0, 0.10, 0.66), 0.09, "Spine")]           # crotch: inner thigh slivers
    for s, side in ((1, "L"), (-1, "R")):
        Wv = X(W, s)
        out.append((Wv, Wv, 0.15, "Hand_" + side))
    return out


# ------------------------------------------------------------------ animation (plan section 7 + ANIM_REFS.md)
import petkit as pk
import _common as cm
import bpy

LEGS2 = ["Leg_L", "Leg_R"]


def tab(T, f):
    """eased (smoothstep) interpolation through [(frame, value | tuple)]"""
    if f <= T[0][0]:
        return T[0][1]
    for (f0, v0), (f1, v1) in zip(T, T[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / (f1 - f0) if f1 > f0 else 1.0
            u = u * u * (3 - 2 * u)
            if isinstance(v0, tuple):
                return tuple(a + (b - a) * u for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * u
    return T[-1][1]


def wrist(k, side, f, P, toe=0.0):
    """2-bone arm IK: put the wrist at world point P (fist kept level unless toe tilts it)"""
    s = 1 if side == "L" else -1
    Sv, Wv = X(S, s), X(W, s)
    P = Vector(P)
    k.solve_leg("Arm_" + side, f, Vector((Sv.x + P.x - Wv.x, Sv.y + P.y - Wv.y, P.z - Wv.z)), toe=toe)


def rest_wrist(side):
    return X(W, 1 if side == "L" else -1)


def plant_feet(k, f):
    for leg in LEGS2:
        k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


def head(k, f, pitch, yaw=0.0, rel=None):
    """key the Head; when it pitches UP relative to the chest (rel < 0) it also slides forward out of the neck
    sleeve so the back of the skull clears the trapezius hump"""
    r = pitch if rel is None else rel
    u = max(0.0, -r) / 15.0
    k.key("Head", f, rot=(pitch, yaw, 0), loc=(0, -0.05 * u, 0.015 * u))


def plates(k, f, a):
    """lift the outer rim of both shoulder crusts by a deg"""
    k.key("Plate_L", f, rot=(0, 0, -a))
    k.key("Plate_R", f, rot=(0, 0, a))


def idle(k):
    """PLATE SETTLE: slow hip sway (yaw +-4), three breaths; the shoulder crusts lift 4 deg and settle twice (f30-50);
    the head lowers 6 deg at f55-75 and is back by f100. Feet planted, arms hang."""
    n = 120
    k.new_action("idle", n, True)
    HD = [(0, 0.0), (55, 0.0), (65, 6.0), (75, 6.0), (100, 0.0), (120, 0.0)]
    PL = [(0, 0.0), (30, 0.0), (35, 6.0), (40, 0.8), (45, 6.0), (50, 0.0), (120, 0.0)]
    for f in range(0, n + 1, 2):
        br = 0.5 + 0.5 * pk.wave(f, n, 0.25, 3)
        k.key("Spine", f, rot=(0, 4.0 * pk.wave(f, n, 0.0, 1), 0), loc=(0, 0, -0.006 * br))
        k.key("Chest", f, rot=(-2.4 * br, -1.5 * pk.wave(f, n, 0.05, 1), 0))           # visible breath (r3 NICE 4)
        head(k, f, tab(HD, f) + 0.6 * br, -1.5 * pk.wave(f, n, 0.1, 1))
        k.key("Jaw", f, rot=(1.0 * br, 0, 0))
        plates(k, f, tab(PL, f))
    cm.plant(k, n, legs=LEGS2)
    k.finish()
    k.meta["planted"] = LEGS2
    k.events["idle"] = {"settle1": round(40 / n, 3), "settle2": round(50 / n, 3)}


def walk(k):
    """KNUCKLE WALK (Muybridge plate 747): diagonal sequence LH, RF, RH, LF; hunched (torso -0.07, chest +9 deg) so the
    fists plant on the snow; the swinging fist lifts with the elbow out; the chest yaws with the arm in stance; the head
    stays level."""
    n = 48
    S_, LIFT, DUTY = 0.12, 0.07, 0.62
    legs = [("Leg_L", 0.0), ("Arm_L", 0.25), ("Leg_R", 0.5), ("Arm_R", 0.75)]
    k.new_action("walk", n, True)
    for f in range(0, n + 1, 2):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(8.0 + 1.0 * pk.wave(f, n, 0.1, 2), 2 * pk.wave(f, n, 0.0), 2.0 * pk.wave(f, n, 0.05)),
              loc=(0, 0, -0.075 - 0.033 * b))
        k.key("Chest", f, rot=(1.0 + 0.8 * pk.wave(f, n, 0.15, 2), -4 * pk.wave(f, n, 0.0), -1.5 * pk.wave(f, n, 0.05)))
        head(k, f, -5.0 - 1.0 * pk.wave(f, n, 0.2, 2), 3 * pk.wave(f, n, 0.0))
        k.key("Jaw", f, rot=(1, 0, 0))
        plates(k, f, 1.0 + 1.0 * pk.wave(f, n, 0.3, 2))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg, off in legs:
            T = pk.gait_target(k, leg, f, n, off, S_, LIFT, DUTY)
            if leg.startswith("Arm"):
                T = Vector((T.x, T.y, T.z - 0.10))               # knuckles on the snow, 0.10 below the hang height
                k.solve_leg(leg, f, T, toe=-10.0 * max(0.0, T.z + 0.10) / LIFT)
            else:
                k.solve_leg(leg, f, T, toe=8.0 * max(0.0, T.z) / LIFT)   # long feet: small heel-up only
    k.finish()
    k.meta["walk_cycle"] = n
    k.meta["legs"] = legs
    k.meta["duty"] = DUTY
    k.events["walk"] = {"stomp": 0.5}                             # Leg_R touches down at f24
    return (2 * S_) / DUTY


def roar(k):
    """SHOULDER-HEAVE BELLOW: the shoulders pull back (chest lifts back), two heaves (chest yaw +10 / -10, the arm on
    the forward shoulder swinging with it), the head up 15 deg, the jaw opens late (f20-45) showing the fangs; settles.
    No chest beat, no arms raised. Feet planted."""
    n = 60
    k.new_action("roar", n, False)
    # f, spine z, chest pitch, chest yaw, head pitch, jaw, plates
    P = [(0, 0.0, 0, 0, 0, 0, 0), (12, 0.02, -6, 0, -4, 3, 3), (17, 0.0, 2, 10, -15, 6, 2), (22, 0.0, 2, -10, -20, 16, 3),
         (28, 0.0, 0, 0, -20, 26, 4), (45, 0.0, 0, 0, -20, 24, 4), (52, 0.0, 0, 0, -8, 6, 1), (60, 0.0, 0, 0, 0, 0, 0)]
    for f, sz, cp, cy, hp, jw, pl in P:
        k.key("Spine", f, rot=(cp * 0.6, cy * 0.6, 0), loc=(0, 0, sz))       # chest vs spine stays <= 5 deg
        k.key("Chest", f, rot=(cp * 0.4, cy * 0.4, 0))
        head(k, f, hp - cp, -cy * 0.5)
        k.key("Jaw", f, rot=(jw, 0, 0))
        plates(k, f, pl)
        for side, sx in (("L", 1), ("R", -1)):                     # the arm on the heaving shoulder swings forward
            sw = max(0.0, sx * cy) / 10.0
            k.key("Arm_" + side, f, rot=(-8 * sw + 3 * (cp < 0), 0, 0))
            k.key("Fore_" + side, f, rot=(-6 * sw, 0, 0))
    for f in (32, 38):                                            # a slight tremble in the held bellow
        k.key("Jaw", f, rot=(26 if f == 32 else 24, 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        plant_feet(k, f)
    k.finish(loop=False)
    k.events["roar"] = {"roar": round(24 / n, 3)}


def skid(k):
    """SIGNATURE - SNOW SKID AND BRAKE: drops onto wide-planted fists (chest -0.06H), sweeps both arms forward and back
    like a sled (skid1), slides the chest low with the feet planted (skid2), digs the fists in for a hard brake (brake,
    ice shards), pushes up with a shoulder heave and settles to rest. Root net 0."""
    n = 100
    k.new_action("act_skid", n, False)
    # f, spine z, spine pitch, chest pitch, chest yaw, head pitch, jaw, plates
    BODY = [(0, (0.0, 0, 0, 0, 0, 0, 0)), (7, (-0.08, 4, 12, 0, -10, 2, 2)), (16, (-0.10, 5, 15, 0, -13, 3, 3)),
            (22, (-0.11, 5, 16, 0, -14, 4, 4)), (34, (-0.12, 6, 17, 0, -14, 4, 4)), (42, (-0.14, 7, 18, 0, -15, 6, 5)),
            (52, (-0.13, 6, 17, 0, -14, 5, 4)), (56, (-0.11, 5, 14, 0, -12, 4, 3)), (58, (-0.14, 7, 19, 0, -16, 18, 6)),
            (62, (-0.14, 7, 19, 0, -16, 16, 6)), (66, (-0.12, 6, 16, 0, -14, 8, 4)), (74, (-0.02, 2, 2, 9, -4, 6, 3)),
            (80, (0.01, 0, -2, -7, -2, 4, 4)), (86, (0.0, 0, 0, 0, 0, 3, 1)), (92, (0.0, 0, 0, 0, 0, 1, 3)),
            (100, (0.0, 0, 0, 0, 0, 0, 0))]
    for f in range(0, n + 1, 2):
        sz, sp, cp, cy, hp, jw, pl = tab(BODY, f)
        c_p = max(-3.5, min(3.5, cp))                            # chest vs spine stays <= 5 deg
        k.key("Spine", f, rot=(sp + cp - c_p, cy * 0.65, 0), loc=(0, 0, sz))
        k.key("Chest", f, rot=(c_p, cy * 0.35, 0))
        head(k, f, hp, -cy * 0.4)
        k.key("Jaw", f, rot=(jw, 0, 0))
        plates(k, f, pl)
    k.bake_bezier_now()
    sc = bpy.context.scene
    # wrist targets (left side; the right is mirrored): rest -> planted wide -> sled sweeps -> slide -> dig -> rest
    R0 = tuple(rest_wrist("L"))
    WT = [(0, R0), (7, (0.66, -0.52, 0.44)), (16, (0.76, -0.62, 0.33)),       # plant wide on the snow
          (22, (0.74, -0.80, 0.36)), (28, (0.74, -0.42, 0.33)), (34, (0.74, -0.76, 0.35)),   # sled sweeps
          (42, (0.76, -0.70, 0.33)), (52, (0.76, -0.72, 0.33)),                           # slide low
          (55, (0.75, -0.74, 0.40)), (58, (0.76, -0.75, 0.31)), (64, (0.76, -0.75, 0.31)),   # cocked, DIG IN (brake)
          (74, (0.66, -0.56, 0.48)), (86, R0), (100, R0)]
    for f in range(0, n + 1):
        sc.frame_set(f)
        plant_feet(k, f)
        p = Vector(tab(WT, f))
        sweep = 1.0 if 16 < f < 36 else 0.0
        lift = 0.05 * sweep * max(0.0, math.sin(math.pi * (f - 16) / 6.0)) if sweep else 0.0
        for side, sx in (("L", 1), ("R", -1)):
            wrist(k, side, f, Vector((sx * p.x, p.y, p.z + (lift if side == "L" else lift))))
    k.finish(loop=False)
    k.events["act_skid"] = {"skid1": round(22 / n, 3), "skid2": round(42 / n, 3), "brake": round(58 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    skid(k)
    return stride


HEAD_XF = []
