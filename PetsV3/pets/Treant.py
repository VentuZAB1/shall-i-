# Treant (Wood egg #3, T1 top, biped) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the ancient ent"): a hunched oak
# giant: root-trunk legs ending in splayed root toes (Root bones, they drive down in act_takeroot), a trunk that
# tapers at the waist and flares to the shoulders with a burl hump on the back, no neck - the head is the top of the
# trunk with the face sunk under a heavy knot brow: amber slit eyes in dark knot sockets, a jagged mouth gash with
# splinter teeth and a moss beard; long gnarled arms (forearm thicker than the upper arm) ending in 3 twig talons;
# a crown of twisted branches carrying dark leaf clumps; vertical bark fissures and 3 amber sap cracks.
# Old chibi version: _tools/chibi_specs/Treant.py
import math
from mathutils import Vector, Matrix, Euler

DISPLAY = "Treant"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 10.0

BARK = (126, 94, 66)        # oak bark (Roblox renders ~0.6x darker -> dark old oak in game)
BARK_D = (88, 64, 46)       # burls, brows, back, talons
FISSURE = (50, 36, 26)      # bark fissures, eye sockets
HEART = (186, 142, 98)      # heartwood: face, inner limbs
LEAF = (58, 118, 54)
LEAF_L = (84, 150, 66)
LEAF_D = (42, 90, 42)
MOSS = (104, 156, 66)
SAP = (255, 170, 30)        # THE accent: eyes + sap cracks
SAP_HOT = (255, 228, 150)
TEETH = (222, 198, 150)
MOUTH = (40, 24, 18)

PITCH = 0.053               # stud pitch: 0.042 x (U / U_raiju), U = model height / HEIGHT

S = (0.47, -0.23, 1.30)      # shoulder
E = (0.60, -0.20, 0.89)      # elbow
W = (0.61, -0.40, 0.55)      # wrist
LEG = ((0.20, 0.03, 0.80), (0.22, -0.11, 0.44), (0.22, 0.02, 0.13))   # hip, knee, ankle
HEAD_C = Vector((0, -0.40, 1.40))
RH = Euler((math.radians(16), 0, 0), "XYZ").to_matrix()               # head thrust forward, below the hump
CROWN_D = Vector((0, -0.22, -0.15))                                   # crown offset (moved with the head)
# trunk blocks (centre, half, bottom taper, top taper, pitch deg): waist and the hunched upper trunk
WAIST = ((0, -0.03, 1.00), (0.27, 0.20, 0.13), (1, 1), (1.30, 1.15), 14)
UPPER = ((0, -0.15, 1.25), (0.43, 0.25, 0.165), (0.80, 0.88), (1.0, 0.92), 34)
EYE_X = 0.125


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def HP(x, y, z):
    """head-local point -> world"""
    return HEAD_C + RH @ Vector((x, y, z))


def frame(u, n):
    z = Vector(n).normalized()
    x = Vector(u)
    x = (x - z * x.dot(z)).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


def face_pt(blk, key, u, v):
    """point, outward normal, across axis on a face of a tapered block pitched about x; u in [-1, 1] across,
    v in [0, 1] from the bottom edge to the top edge"""
    c, h, bt, tp, pitch = Vector(blk[0]), Vector(blk[1]), blk[2], blk[3], blk[4]
    Rm = Euler((math.radians(pitch), 0, 0), "XYZ").to_matrix()
    ax = 0 if key[1] == "x" else 1
    ot = 1 - ax
    sg = 1 if key[0] == "+" else -1
    ea, eo = Vector((0, 0, 0)), Vector((0, 0, 0))
    ea[ax], eo[ot] = sg, 1
    xa = h[ax] * (bt[ax] + (tp[ax] - bt[ax]) * v)
    ac = h[ot] * (bt[ot] + (tp[ot] - bt[ot]) * v)
    p = ea * xa + eo * (u * ac) + Vector((0, 0, -h.z + 2 * h.z * v))
    along = ea * (h[ax] * (tp[ax] - bt[ax])) + Vector((0, 0, 2 * h.z))
    n = eo.cross(along).normalized()
    if n.dot(ea) < 0:
        n = -n
    return c + Rm @ p, Rm @ n, Rm @ eo


def ridge(B, p0, p1, n, bone, w=0.035):
    """raised bark ridge 0.03 proud"""
    n = Vector(n).normalized()
    B.bar(p0 + n * 0.008, p1 + n * 0.008, n, w, 0.022, BARK_D, bone, rnd=0.3, role="limb")


def split(B, p0, p1, n, bone, w=0.038, drip=False):
    """sap SPLIT (not a bolt): one kink <= 0.006 sideways, lens-tapered 0.3 -> 1 -> 0.3, dark rim, optional drip"""
    n = Vector(n).normalized()
    p0, p1 = Vector(p0), Vector(p1)
    d = (p1 - p0).normalized()
    side = n.cross(d).normalized()
    pk = p0.lerp(p1, 0.5) + side * 0.006
    for col, ww, lift in ((FISSURE, w * 1.6, 0.004), (SAP, w, 0.011)):
        B.bar(p0 + n * lift, pk + n * lift, n, ww, 0.008, col, bone, studs=[], bevel=0.003, bot=(1, 0.3))
        B.bar(pk + n * lift, p1 + n * lift, n, ww, 0.008, col, bone, studs=[], bevel=0.003, top=(1, 0.3))
    if drip:
        up = d * -1
        B.add(p1 - up * 0.035 + n * 0.012, (0.015, 0.008, 0.03), SAP, bone, R=Matrix((side, n, d)).transposed(),
              top=(0.45, 1), role="detail", bevel=0.004)


def zig(B, pts, n, w, bone, col=SAP):
    """a sap crack: flat zigzag bars on a surface with normal n, narrowing to a point (SAP sits 0.006 proud of
    its dark FISSURE rim)"""
    n = Vector(n).normalized()
    m = len(pts) - 1
    lift = n * (0.006 if col == SAP else 0.0)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        f = 1.0 - 0.35 * i / max(1, m)
        d = (Vector(b) - Vector(a)).normalized()
        B.bar(Vector(a) - d * 0.008 + lift, Vector(b) + d * 0.008 + lift, n, w * f, 0.012, col, bone, studs=[],
              bevel=0.004, top=(1, 0.2) if i == m - 1 else (1, 1))


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=61, tier=1, plates=False, th=0.70)
    # ---------------- trunk: pelvis < waist (tapered) < hunched upper trunk (leaning 28 deg) + a burl hump on top
    B.add((0, 0.02, 0.84), (0.25, 0.19, 0.12), BARK, "Spine", rnd=0.3, role="mass")
    for blk in (WAIST, UPPER):
        B.add(blk[0], blk[1], BARK, "Chest", rot=(blk[4], 0, 0), bot=blk[2], top=blk[3], rnd=0.3, role="mass")
    B.add((0, 0.04, 1.48), (0.31, 0.19, 0.20), BARK, "Chest", rot=(34, 0, 0), rnd=0.45, role="mass")     # burl hump
    for c, h in (((0.16, 0.16, 1.60), (0.10, 0.09, 0.09)), ((0.24, 0.12, 1.46), (0.07, 0.07, 0.065))):       # knots
        B.add(c, h, BARK_D, "Chest", rnd=0.45, role="limb")
    for c, h in (((-0.26, 0.12, 1.40), (0.12, 0.11, 0.11)), ((0.30, 0.20, 1.30), (0.09, 0.08, 0.08))):       # burls
        B.add(c, h, BARK, "Chest", rnd=0.45, role="limb")
    # raised bark ridges (0.03 proud), following the trunk tilt: 3 front, 2 per side, 4 back
    for key, us in (("-y", (-0.55, 0.0, 0.55)), ("+x", (-0.45, 0.35)), ("-x", (-0.45, 0.35)),
                    ("+y", (-0.65, -0.22, 0.22, 0.65))):
        for u in us:
            for blk, v0, v1 in ((WAIST, 0.05, 0.98), (UPPER, 0.03, 0.97 if key != "+y" else 0.55)):
                q0, n, _ = face_pt(blk, key, u, v0)
                q1, _, _ = face_pt(blk, key, u * 1.02, v1)
                ridge(B, q0, q1, n, "Chest")
    # sap split on the chest (amber, lens-shaped) with a drip
    q0, n, _ = face_pt(UPPER, "-y", 0.52, 0.82)
    q1, _, _ = face_pt(UPPER, "-y", 0.50, 0.22)
    split(B, q0, q1, n, "Chest", drip=True)
    # broken branch stubs: a gnarled silhouette
    for p0, d, L, w in (((0.30, 0.04, 1.52), (0.5, 0.5, 0.9), 0.24, 0.05), ((-0.18, 0.18, 1.60), (-0.4, 0.7, 0.7), 0.20, 0.045),
                        ((-0.42, 0.0, 1.16), (-1, 0.5, 0.3), 0.15, 0.04)):
        d = Vector(d).normalized()
        B.seg(Vector(p0), Vector(p0) + d * L, w, w, BARK_D, "Chest", ext=0.04, top=(0.7, 0.7), role="limb")
        B.spike(Vector(p0) + d * L * 0.6, d + Vector((0, -0.6, 0.6)), 0.09, 0.02, BARK_D, "Chest")
    # moss on the shoulders: top slab + an overhang down the outer side (the 2 shoulders differ)
    for s, yaw in ((1, 25), (-1, -10)):
        Sv = X(S, s)
        Rz = Euler((math.radians(12), 0, math.radians(yaw)), "XYZ").to_matrix()
        top = Sv + Vector((s * 0.0, 0.02, 0.145))
        B.add(top - Vector((0, 0, 0.02)), (0.13, 0.14, 0.03), LEAF_D, "Chest", R=Rz, rnd=0.4, role="limb")
        B.add(top, (0.12, 0.13, 0.04), MOSS, "Chest", R=Rz, rnd=0.4, role="limb")
        B.add(top + Vector((s * 0.12, -0.02, -0.08)), (0.05, 0.09, 0.07), LEAF_D, "Chest", R=Rz, top=(1.2, 1),
              bot=(0.6, 0.8), rnd=0.4, role="limb")
    # ---------------- head = the top of the trunk (no neck), leaning forward; face sunk under a knot brow
    B.add(HEAD_C, (0.29, 0.22, 0.16), BARK, "Head", R=RH, top=(0.85, 0.85), rnd=0.3, role="mass")
    B.add(HP(0, -0.215, -0.03), (0.23, 0.012, 0.11), HEART, "Head", R=RH, studs=[], role="detail", bevel=0.01)  # face
    B.add(HP(0, -0.245, 0.09), (0.27, 0.05, 0.045), BARK_D, "Head", R=RH, top=(0.9, 0.7), rnd=0.3, role="limb")  # brow
    for s in (1, -1):
        Rb = RH @ Euler((0, math.radians(-s * 20), 0), "XYZ").to_matrix()
        B.add(HP(s * 0.13, -0.255, 0.058), (0.125, 0.052, 0.038), BARK_D, "Head", R=Rb, rnd=0.3, role="limb")
        # dark knot socket + amber slit + hot centre
        Re = RH @ Euler((0, math.radians(-s * 16), 0), "XYZ").to_matrix()
        c = HP(s * EYE_X, -0.225, 0.0)

        def P(dx, dy, dz):
            return c + Re @ Vector((s * dx, dy, dz))
        B.add(P(0, 0, 0), (0.085, 0.012, 0.046), FISSURE, "Head", R=Re, studs=[], role="detail", bevel=0.008)
        B.add(P(0.003, -0.011, -0.002), (0.064, 0.007, 0.019), SAP, "Head", R=Re, studs=[], role="detail", bevel=0.003)
        B.add(P(0.014, -0.016, 0.0), (0.024, 0.005, 0.008), SAP_HOT, "Head", R=Re, studs=[], role="detail",
              bevel=0.002)
    B.add(HP(0, -0.255, -0.045), (0.05, 0.045, 0.055), BARK, "Head", R=RH, top=(0.7, 0.8), rnd=0.3, role="limb")  # nose
    # jagged mouth gash + splinter teeth hanging from the upper lip
    Rm = RH @ Euler((0, math.radians(5), 0), "XYZ").to_matrix()
    B.add(HP(0, -0.228, -0.11), (0.17, 0.012, 0.03), MOUTH, "Head", R=Rm, studs=[], role="detail", bevel=0.006)
    for x, L in ((-0.11, 0.05), (-0.05, 0.035), (0.02, 0.05), (0.09, 0.04)):
        B.spike(HP(x * 1.1, -0.236, -0.083), RH @ Vector((0, -0.15, -1)), L, 0.017, TEETH, "Head")
    # chin (Jaw): lower lip with splinter teeth, moss beard
    B.add(HP(0, -0.185, -0.162), (0.21, 0.06, 0.042), BARK, "Jaw", R=RH, rnd=0.3, role="limb")
    for x, L in ((-0.08, 0.04), (0.0, 0.05), (0.07, 0.035)):
        B.spike(HP(x * 1.1, -0.236, -0.138), RH @ Vector((0, -0.1, 1)), L, 0.016, TEETH, "Jaw")
    for x, L, w in ((-0.13, 0.13, 0.04), (-0.06, 0.20, 0.045), (0.02, 0.24, 0.05), (0.10, 0.17, 0.045),
                    (0.16, 0.11, 0.035)):
        r0 = HP(x * 1.1, -0.23, -0.18)
        B.seg(r0, r0 + Vector((x * 0.25, 0.06, -L)), w, 0.02, MOSS, "Jaw", side=(1, 0, 0), top=(0.25, 0.6), ext=0.02,
              role="limb")
    # ---------------- crown: twisted branches with big dark leaf clumps (span ~ the trunk width)
    branches = [((0.10, -0.16, 1.68), (0.22, -0.10, 1.86), (0.40, -0.13, 1.96), (0.55, -0.07, 2.10)),
                ((-0.10, -0.15, 1.68), (-0.20, -0.18, 1.88), (-0.38, -0.09, 1.98), (-0.53, -0.13, 2.08)),
                ((0.05, -0.05, 1.70), (0.10, 0.05, 1.92), (0.25, 0.13, 2.04)),
                ((-0.04, -0.07, 1.70), (-0.09, 0.02, 1.96), (-0.17, 0.10, 2.16)),
                ((0.02, -0.28, 1.68), (0.07, -0.37, 1.86))]
    for br in branches:
        P = [Vector(p) + CROWN_D for p in br]
        for i, (a, b) in enumerate(zip(P, P[1:])):
            w = 0.062 - 0.012 * i
            B.seg(a, b, w, w * 1.1, BARK_D, "Crown", ext=0.03, ext1=0.02, top=(0.8, 0.8), role="limb")
            if i == 1:
                d = (b - a).normalized()
                B.spike(a.lerp(b, 0.5), d + Vector((0, 0.4, 0.6)), 0.10, 0.022, BARK_D, "Crown")          # twig
    for c, sc in (((0.55, -0.07, 2.13), 1.0), ((-0.53, -0.13, 2.11), 0.95), ((0.25, 0.13, 2.09), 0.85),
                  ((-0.17, 0.10, 2.21), 1.0), ((0.07, -0.38, 1.90), 0.6)):
        c = Vector(c) + CROWN_D
        rz = (15, 35, 22, 28, 18)[int(sc * 100) % 5]
        B.add(c, (0.16 * sc, 0.15 * sc, 0.10 * sc), LEAF_D, "Crown", rot=(0, 0, rz), rnd=0.40, role="mass")
        B.add(c + Vector((0.05, -0.04, 0.07)) * sc, (0.11 * sc, 0.11 * sc, 0.08 * sc), LEAF, "Crown", rot=(0, 0, -rz),
              rnd=0.4, role="mass")
        B.add(c + Vector((-0.07, 0.05, 0.04)) * sc, (0.09 * sc, 0.09 * sc, 0.07 * sc), LEAF_L, "Crown",
              rot=(0, 0, rz * 0.5), rnd=0.4, role="limb")
    # ---------------- arms: gnarled, forearm thicker than the upper arm, elbow knot, 3 long twig talons + thumb
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        B.add(Sv + Vector((s * 0.02, 0, 0.02)), (0.14, 0.14, 0.12), BARK_D, "Arm_" + side, rnd=0.4, role="limb")
        B.seg(Sv, Ev, 0.095, 0.10, BARK, "Arm_" + side, ext=0.05, ext1=0.03, rnd=0.3)
        B.add(Ev + Vector((s * 0.02, 0.02, 0)), (0.11, 0.11, 0.09), BARK_D, "Fore_" + side, rnd=0.4, role="limb")
        B.seg(Ev, Wv, 0.13, 0.12, BARK, "Fore_" + side, ext=0.03, top=(0.85, 0.85), rnd=0.3)
        d = (Wv - Ev).normalized()
        nf = Vector((0, -1, 0))
        nf = (nf - d * nf.dot(d)).normalized()
        ridge(B, Ev + d * 0.08 + nf * 0.12, Wv - d * 0.05 + nf * 0.105, nf, "Fore_" + side)
        hc = Wv + Vector((0, -0.03, -0.07))
        B.add(hc, (0.11, 0.10, 0.08), BARK_D, "Hand_" + side, rnd=0.3, role="limb")
        for dx in (-0.07, 0.0, 0.07):
            r0 = hc + Vector((dx, -0.05, -0.04))
            dd = Vector((dx * 0.8, -0.35, -1)).normalized()
            m = r0 + dd * 0.13
            B.seg(r0, m, 0.03, 0.03, BARK_D, "Hand_" + side, ext=0.02, top=(0.8, 0.8), role="limb")
            B.spike(m - dd * 0.01, dd + Vector((0, -0.3, 0)), 0.10, 0.024, FISSURE, "Hand_" + side, top=(0.12, 0.12))
        B.spike(hc + Vector((-s * 0.09, -0.04, 0.0)), (-s * 0.7, -0.5, -0.4), 0.12, 0.026, BARK_D, "Hand_" + side,
                top=(0.15, 0.15))
    da = (X(E, 1) - X(S, 1)).normalized()
    na = Vector((1, 0, 0))
    na = (na - da * na.dot(da)).normalized()
    split(B, X(S, 1).lerp(X(E, 1), 0.22) + na * 0.096, X(S, 1).lerp(X(E, 1), 0.75) + na * 0.096, na, "Arm_L")
    # ---------------- legs: root trunks widening into a root base; splayed root toes on the Root bone
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A = (X(p, s) for p in LEG)
        B.seg(H, K, 0.17, 0.17, BARK, "Leg_" + side, ext=0.08, top=(0.82, 0.82), rnd=0.3)
        B.seg(K, A, 0.15, 0.16, BARK, "Shin_" + side, ext=0.06, top=(1.40, 1.35), rnd=0.3)
        dt = (K - H).normalized()
        nt = Vector((0, -1, 0))
        nt = (nt - dt * nt.dot(dt)).normalized()
        ridge(B, H + dt * 0.10 + nt * 0.165, K - dt * 0.04 + nt * 0.142, nt, "Leg_" + side)
        B.seg(K + Vector((s * 0.14, -0.04, -0.02)), A + Vector((s * 0.25, -0.10, -0.07)), 0.022, 0.03, BARK_D,
              "Shin_" + side, side=(0, 1, 0), ext=0.02, top=(1.6, 1.3), role="limb")                    # root buttress
        B.add(A + Vector((0, -0.01, -0.065)), (0.20, 0.20, 0.07), BARK_D, "Foot_" + side, top=(0.85, 0.85), rnd=0.3)
        for ang, L, dz in ((-26, 0.18, -0.03), (-5, 0.27, -0.03), (30, 0.23, -0.03), (150, 0.15, 0.0)):
            a = math.radians(ang)
            d = Vector((s * math.sin(a), -math.cos(a), 0))
            p0 = A + Vector((0, 0, -0.05)) + d * 0.12
            p1 = p0 + d * L + Vector((0, 0, dz))
            pm = p0.lerp(p1, 0.6)
            B.seg(p0, pm, 0.055, 0.045, BARK_D, "Root_" + side, side=(0, 0, 1), ext=0.04, top=(0.8, 0.8), role="limb")
            B.seg(pm, p1, 0.044, 0.034, FISSURE, "Root_" + side, side=(0, 0, 1), ext=0.015, top=(0.35, 0.5),
                  role="limb")
    H, K = X(LEG[0], -1), X(LEG[1], -1)
    dt = (K - H).normalized()
    nl = Vector((-1, 0, 0))
    nl = (nl - dt * nl.dot(dt)).normalized()
    split(B, H.lerp(K, 0.18) + nl * 0.166, H.lerp(K, 0.72) + nl * 0.15, nl, "Leg_R")      # sap split, right thigh
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.02, 0.80), "Root", tail=(0, 0, 0.3))
    k.joint("Chest", (0, 0.02, 0.95), "Spine", tail=(0, 0, 0.4))
    k.joint("Head", (0, -0.30, 1.28), "Chest", tail=(0, -0.10, 0.3))           # base of the head (trunk top)
    k.joint("Jaw", tuple(HP(0, -0.12, -0.13)), "Head", tail=(0, -0.2, 0))
    k.joint("Crown", tuple(Vector((0, -0.12, 1.70)) + CROWN_D), "Head", tail=(0, 0, 0.4))
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        k.joint("Arm_" + side, Sv, "Chest")
        k.joint("Fore_" + side, Ev, "Arm_" + side)
        k.joint("Hand_" + side, Wv, "Fore_" + side, tail=(0, -0.05, -0.25))
        H, K, A = (X(p, s) for p in LEG)
        k.joint("Leg_" + side, H, "Spine")
        k.joint("Shin_" + side, K, "Leg_" + side)
        k.joint("Foot_" + side, A, "Shin_" + side, tail=(0, -0.25, 0))
        k.joint("Root_" + side, tuple(A + Vector((0, -0.10, -0.06))), "Foot_" + side, tail=(0, -0.25, 0))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))


# ------------------------------------------------------------------ animation (FIERCE_PLAN: wind sway / timber lean /
# act_takeroot). k.key rot = (pitch, yaw, roll) deg, armature axes, relative to the parent.
import petkit as pk
import _common as cm

LEGS2 = ["Leg_L", "Leg_R"]


def jaw(k, f, a):
    """a = 0 closed .. 1 wide open: the chin drops and tips forward"""
    k.key("Jaw", f, rot=(-12 * a, 0, 0), loc=(0, -0.02 * a, -0.09 * a))


def arm(k, f, side, pitch=0.0, yaw=0.0, roll=0.0, elbow=0.0, hand=0.0):
    """pitch - swings the arm forward/up, roll + lifts it out to the side, elbow + bends the forearm forward/up,
    hand + curls the twig talons (- splays them)"""
    s = 1 if side == "L" else -1
    k.key("Arm_" + side, f, rot=(pitch, s * yaw, -s * roll))
    k.key("Fore_" + side, f, rot=(-elbow, 0, 0))
    k.key("Hand_" + side, f, rot=(-hand, 0, 0))


def roots(k, f, pl=0.0, yl=0.0, pr=None, yr=None):
    """pitch + tips the root toes down, yaw + spreads them (left toes toward +x)"""
    pr = pl if pr is None else pr
    yr = yl if yr is None else yr
    k.key("Root_L", f, rot=(pl, -yl, 0))
    k.key("Root_R", f, rot=(pr, yr, 0))


def idle(k):
    """WIND SWAY: the whole tree sways (Spine roll +-4) with the arms lagging like heavy branches and the crown
    counter-swaying; a GUST bends the crown and swings the arms; then a slow creaking back-stretch."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        sw = pk.wave(f, n, 0, 2)
        lag = pk.wave(f - 6, n, 0, 2)
        g = math.sin(math.pi * (f - 55) / 20) if 55 <= f <= 75 else 0.0
        st = math.sin(math.pi * (f - 90) / 20) if 90 <= f <= 110 else 0.0
        k.key("Spine", f, rot=(0, 0, 4 * sw), loc=(0, 0, 0.006 * pk.wave(f, n, 0.1, 4)))
        k.key("Chest", f, rot=(-8 * st - 1.0 * pk.wave(f, n, 0.1, 4), 1.2 * sw, 1.0 * sw))
        k.key("Head", f, rot=(-3 * st, 0, -1.5 * sw))
        k.key("Crown", f, rot=(10 * g + 1.5 * pk.wave(f, n, 0.3, 4), 0, -4 * sw + 3 * g * math.sin(f * 0.9)))
        jaw(k, f, 0.12 * st)
        for side, s in (("L", 1), ("R", -1)):
            arm(k, f, side, pitch=-3 * lag - 12 * g, roll=4 + 5 * s * lag, elbow=10 + 4 * g, hand=8)
        roots(k, f, 0, 0)
    cm.plant(k, n, legs=LEGS2)
    k.finish()
    k.meta["planted"] = LEGS2


def walk(k):
    n = 44

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(2, 4 * pk.wave(f, n, 0.0), 4 * pk.wave(f, n, 0.0)), loc=(0, 0, -0.035 * b))
        k.key("Chest", f, rot=(2 + 1.5 * pk.wave(f, n, 0.1, 2), -5 * pk.wave(f, n, 0.0), -2.5 * pk.wave(f, n, 0.05)))
        k.key("Head", f, rot=(-2 - 1.5 * pk.wave(f, n, 0.2, 2), 3 * pk.wave(f, n, 0.0), 0))
        jaw(k, f, 0)
        k.key("Crown", f, rot=(-3 * pk.wave(f, n, 0.3, 2), 0, -4 * pk.wave(f, n, 0.15)))
        for side, ph in (("L", 0.5), ("R", 0.0)):
            arm(k, f, side, pitch=16 * pk.wave(f, n, ph + 0.05), roll=5, elbow=12 + 8 * pk.wave(f, n, ph + 0.15),
                hand=10)
        tilt = {}
        for side, off in (("L", 0.0), ("R", 0.5)):
            t = ((f / n) + off) % 1.0
            z = 0.10 * math.sin(math.pi * (t - 0.62) / 0.38) if t >= 0.62 else 0.0
            tilt[side] = -35.0 * min(1.0, z / 0.12)
        roots(k, f, tilt["L"], 0, tilt["R"], 0)
    return cm.biped_walk(k, n, 0.14, 0.10, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.62)


def roar(k):
    """TIMBER LEAN: creaks back, then tips FORWARD 28 deg from the ankles like a falling tree (feet planted), arms
    hanging forward with the talons splayed, jaw wide, roars while the crown whips forward, then hauls itself back
    upright with an overshoot."""
    n = 60
    k.new_action("roar", n, False)
    piv = Vector((0, 0.02, 0.13))                      # tip about the ankles
    hip = Vector((0, 0.02, 0.80))
    for f, a, ch, hd, jw, cr, ap, el, hn in ((0, 0, 0, 0, 0, 0, 0, 10, 8), (10, -6, -3, -4, 0.1, -4, 6, 14, 8),
                                             (14, -5, -3, -4, 0.2, -4, 6, 14, 8), (26, 25, 4, -18, 1.0, 14, 22, 8, -25),
                                             (30, 25, 4, -18, 1.0, 16, 22, 8, -25), (44, 25, 4, -18, 0.95, 12, 23, 8, -25),
                                             (52, -4, -2, 2, 0.1, -6, 0, 12, 8), (56, 2, 0, 0, 0, 2, 0, 10, 8),
                                             (60, 0, 0, 0, 0, 0, 0, 10, 8)):
        r = math.radians(a)
        d = hip - piv
        nd = Vector((0, d.y * math.cos(r) - d.z * math.sin(r), d.y * math.sin(r) + d.z * math.cos(r)))
        k.key("Spine", f, rot=(a, 0, 0), loc=tuple(piv + nd - hip))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        jaw(k, f, jw)
        k.key("Crown", f, rot=(cr, 0, 0))
        for side in ("L", "R"):
            arm(k, f, side, pitch=ap, roll=8, elbow=el, hand=hn)
        roots(k, f, 0, 0)
    for f in range(30, 44, 3):
        k.key("Crown", f, rot=(14 + (5 if (f // 3) % 2 else -3), 0, 0))
    cm.plant(k, n, legs=LEGS2)
    k.finish(loop=False)


def takeroot(k):
    """SIGNATURE act_takeroot - TAKE ROOT & UPROOT: plants its feet wide (knees bend), the root toes wriggle and grip
    while the body sinks, the arms rise up and out into a branch V, the head tilts up - and it FREEZES as a tree
    (only the crown sways in the wind). Then the head snaps forward (eyes on), two effortful yanks tear the left foot
    free, then the right (roots curling back), and the branches lower."""
    import bpy
    n = 100
    k.new_action("act_takeroot", n, False)
    # body: (f, z, chest pitch, spine roll, head pitch)
    for f, z, ch, rl, hd in ((0, 0, 0, 0, 0), (10, -0.04, 2, 0, 0), (25, -0.10, 0, 0, 0), (40, -0.10, -4, 0, -10),
                             (62, -0.10, -4, 0, -10), (66, -0.10, -2, 0, 4), (68, -0.10, 0, -3, 4), (72, -0.09, 6, -8, 4),
                             (74, -0.10, 2, -4, 4), (78, -0.08, 8, -8, 4), (80, -0.06, 4, 0, 2), (84, -0.08, 8, 8, 2),
                             (88, -0.05, 2, 0, 0), (94, -0.01, 0, 0, 0), (100, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(0, 0, rl), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        jaw(k, f, 0.6 if 72 <= f <= 84 else 0.0)
    # arms: hanging -> branch V (frozen) -> lowered
    for f, p, ro, el, hn in ((0, 0, 4, 10, 8), (25, 0, 6, 12, 8), (40, -150, 30, 20, -30), (62, -150, 30, 20, -30),
                             (72, -120, 34, 26, -20), (80, -70, 60, 22, -10), (88, -20, 35, 14, 4),
                             (100, 0, 4, 10, 8)):          # branches droop down through the SIDES (not the front)
        for side in ("L", "R"):
            arm(k, f, side, pitch=p, roll=ro, elbow=el, hand=hn)
    for f in range(0, n + 1, 2):
        sway = 4 * math.sin(2 * math.pi * f / 22) if 40 <= f <= 62 else 0.0
        base = 8 if 30 <= f <= 64 else 0
        k.key("Crown", f, rot=(-base + 0.3 * sway, 0, sway))
    # roots: wriggle + grip on the ground (they stay on the surface), curl back when a foot tears free
    for f, pl, yl, pr, yr in ((0, 0, 0, 0, 0), (12, 0, 10, 0, 10), (15, 0, -6, 0, -6), (18, 0, 10, 0, 10),
                              (21, 0, -4, 0, -4), (25, 3, 6, 3, 6), (66, 3, 6, 3, 6), (70, 0, 0, 3, 6), (73, -20, 0, 3, 6),
                              (76, -30, 0, 3, 6), (79, -5, 0, 3, 6), (80, 0, 0, 0, 0), (83, 0, 0, -20, 0), (86, 0, 0, -30, 0),
                              (89, 0, 0, -5, 0), (90, 0, 0, 0, 0), (100, 0, 0, 0, 0)):
        roots(k, f, pl, yl, pr, yr)
    k.bake_bezier_now()
    WIDE = 0.07

    def foot(leg, f):
        """foot target: steps out wide at 2-6 / 6-10, yanks free + steps back home at 68-80 / 80-90"""
        s = 1 if leg.endswith("L") else -1
        x0 = k.J[leg].x
        hop = ((2, 6) if s > 0 else (6, 10))
        back = ((70, 80) if s > 0 else (80, 90))
        tug = (66, 70) if s > 0 else (76, 80)
        x, z = x0, 0.0
        if f >= hop[0]:
            u = min(1.0, (f - hop[0]) / (hop[1] - hop[0]))
            x = x0 + s * WIDE * (0.5 - 0.5 * math.cos(math.pi * u))
            z = 0.06 * math.sin(math.pi * u) if f <= hop[1] else 0.0
        if tug[0] <= f <= tug[1]:                       # first yank: barely moves
            z = 0.025 * math.sin(math.pi * (f - tug[0]) / (tug[1] - tug[0]))
        if f >= back[0]:
            u = min(1.0, (f - back[0]) / (back[1] - back[0]))
            x = x0 + s * WIDE * (1 - (0.5 - 0.5 * math.cos(math.pi * u)))
            z = 0.20 * math.sin(math.pi * u) if f <= back[1] else 0.0
        return Vector((x, k.J[leg].y - 0.04 * math.sin(math.pi * min(1, max(0, (f - back[0]) / 10))), z))

    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS2:
            k.solve_leg(leg, f, foot(leg, f), toe=0.0)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    takeroot(k)
    return stride


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Root_L", "Root_R"), ("Root_L", "Foot_R"),
         ("Root_R", "Foot_L")]
    for s in ("L", "R"):
        for a in ("Fore_" + s, "Hand_" + s):
            for b in ("Spine", "Chest", "Head", "Jaw", "Crown", "Leg_L", "Leg_R", "Shin_L", "Shin_R"):
                P.append((a, b))
        P.append(("Arm_" + s, "Head"))
        P.append(("Arm_" + s, "Crown"))
    P.append(("Hand_L", "Hand_R"))
    P.append(("Fore_L", "Fore_R"))
    return P


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        Wv = X(W, s)
        out.append((Wv, Wv, 0.10, "Hand_" + side))
    return out


HEAD_XF = []
