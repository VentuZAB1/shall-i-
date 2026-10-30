# Coral Crusher (Tide / Water egg, MEDIUM 15 %, 2026-10-27) - plan _review/CoralCrusher_plan.md v2. A giant armoured
# crab in the FIERCE studded style: a wide low bronze carapace (loft tube, domed top, flatter belly) with slate ridges
# (an H groove), rose-coral teeth along the front-side margin, short thick eyestalks sunk in orbits under a slate V brow
# plate with narrow rose slit eyes, pale mandible plates with ivory teeth, two big raised claws (the right one is the
# heavier CRUSHER, the left the slimmer cutter - real crab asymmetry) with rose spikes on their outer edges and dark
# fingertips, and six slate walking legs (2 joints, black tips) on the AbyssWeaver multi-leg IK chain.
# No glow (rose sparkles / bubbles / sand puffs = Studio VFX on the anchor bones).
import math
from mathutils import Vector, Matrix, Euler, Quaternion

DISPLAY = "Coral Crusher"
MOTION = "Walk"
RIG = "quad"                 # the label the Studio side stores for multi-leg walkers (Weaver / Mantis precedent)
HEIGHT = 7.5                 # studs to the top of the raised claws (H_MODEL)

# Blender colours (Roblox renders ~0.6x darker)
BRONZE = (196, 150, 104)     # carapace top, claw bodies (studded)
SHELL_D = (132, 96, 66)      # legs, seams / ridges, claw knuckles, brow plate, fingertips
BELLY_PALE = (240, 226, 200) # underside, mandible plates
ROSE = (255, 120, 150)       # THE accent: claw spikes, margin teeth, eye slits
ROSE_D = (200, 70, 110)      # spike bases
BLACK = (14, 14, 22)         # claw tips, pupils, eye sockets, leg tips
IVORY = (240, 236, 222)      # mandible teeth
MOUTH = (86, 26, 40)         # mouth

H_MODEL = 1.42               # measured top of the claws (refreshed by model())
ANCH = {}

# ---- carapace stations: y, half width, centre z, top half-height, bottom half-height
CAR = [(-0.535, 0.36, 0.475, 0.07, 0.07), (-0.48, 0.52, 0.48, 0.13, 0.10), (-0.38, 0.64, 0.48, 0.18, 0.115),
       (-0.20, 0.70, 0.475, 0.215, 0.125), (0.00, 0.67, 0.47, 0.22, 0.125), (0.20, 0.57, 0.465, 0.20, 0.115),
       (0.36, 0.43, 0.455, 0.16, 0.105), (0.48, 0.27, 0.45, 0.105, 0.085), (0.545, 0.12, 0.445, 0.05, 0.05)]
NC = 2.4

# ---- legs (left side; right = mirror): azimuth (deg from +x toward +y), hip (x, y, z), knee (r, z), ankle (r, z),
# toe (r, z) measured from the hip along the azimuth
HIPZ = 0.40
LEGP = {1: (-30, (0.50, -0.20), (0.27, 0.58), (0.49, 0.10), (0.545, 0.015)),
        2: (2, (0.56, 0.04), (0.28, 0.59), (0.51, 0.10), (0.565, 0.015)),
        3: (32, (0.48, 0.28), (0.26, 0.57), (0.48, 0.10), (0.535, 0.015))}
POLE = {1: (0.35, -0.20, 1.0), 2: (0.40, 0.0, 1.0), 3: (0.35, 0.22, 1.0)}
# claw joints (left side): shoulder, elbow (merus/carpus), wrist (carpus/palm), finger base; c = size factor
CLAW = (Vector((0.32, -0.40, 0.40)), Vector((0.56, -0.64, 0.50)), Vector((0.50, -0.84, 0.64)),
        Vector((0.44, -0.97, 0.92)))
CSIZE = {"L": 0.90, "R": 1.12}         # R = the CRUSHER (the big claw that waves), L = the cutter


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def leg_name(i, side):
    """legs 1-3 = left front -> back, 4-6 = right front -> back (the plan's Foot_1..Foot_6 anchors)"""
    return i if side == "L" else i + 3


def leg_pts(i, s=1):
    a, (hx, hy), kn, an, to = LEGP[i]
    d = Vector((math.cos(math.radians(a)), math.sin(math.radians(a)), 0))
    base = Vector((hx, hy, 0))
    pts = (Vector((hx, hy, HIPZ)), base + d * kn[0] + Vector((0, 0, kn[1])), base + d * an[0] + Vector((0, 0, an[1])),
           base + d * to[0] + Vector((0, 0, to[1])))
    return tuple(X(p, s) for p in pts)


def ring(y, hw, zc, ht, hb, n=NC, seg=28, out=0.0):
    pts = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        c, s = math.cos(a), math.sin(a)
        h = (ht if s > 0 else hb) + out
        pts.append(Vector(((hw + out) * math.copysign(abs(c) ** (2.0 / n), c), y,
                           zc + h * math.copysign(abs(s) ** (2.0 / n), s))))
    return pts


def car_at(y):
    for a, b in zip(CAR, CAR[1:]):
        if a[0] <= y <= b[0]:
            t = (y - a[0]) / (b[0] - a[0])
            return tuple(a[i] + (b[i] - a[i]) * t for i in range(1, 5))
    return CAR[-1][1:] if y > 0 else CAR[0][1:]


def surf_hit(B, blks, origin, direction):
    """first hit of a ray on the given parts (blocks or tubes) -> (point, outward normal) (AbyssWeaver)"""
    import blockkit as bk
    from mathutils.bvhtree import BVHTree
    B._resolve()
    best = None
    d = Vector(direction).normalized()
    for blk in blks:
        bm = bk.part_bm(blk)
        t = BVHTree.FromBMesh(bm)
        bm.free()
        loc, nrm, _, dist = t.ray_cast(Vector(origin), d)
        if loc is not None and (best is None or dist < best[2]):
            best = (loc, nrm.normalized(), dist)
    if best is None:
        raise RuntimeError("surf_hit: no surface from %s" % (tuple(origin),))
    return best[0], best[1]


def face_R(nn, up=(0, 0, 1)):
    y = -Vector(nn).normalized()
    z = Vector(up) - y * y.dot(Vector(up))
    if z.length < 1e-3:
        z = Vector((0, 1, 0)) - y * y.y
    z.normalize()
    return Matrix((y.cross(z), y, z)).transposed()


def rose_spike(B, base, d, L, w, bone, side=(1, 0, 0)):
    """coral spike: rose-dark base collar -> rose body to a point (smooth)"""
    d = Vector(d).normalized()
    base = Vector(base)
    B.spike(base - d * 0.012, d, L * 0.40, w * 1.15, ROSE_D, bone, side=side, top=(0.80, 0.80), nostud=True)
    B.spike(base + d * L * 0.22, d, L * 0.78, w, ROSE, bone, side=side, top=(0.10, 0.10), nostud=True)


def crab_eye(B, c, s, n, bone, tilt=15.0, sc=1.0):
    """black socket (inner corner down) -> rose slit -> black slit pupil (no glint)"""
    R = face_R(n) @ Euler((0, math.radians(-s * tilt), 0), "XYZ").to_matrix()
    nn = Vector(n).normalized()
    kw = dict(R=R, studs=[], role="detail")
    B.add(c, (0.050 * sc, 0.008, 0.026 * sc), BLACK, bone, bevel=0.004, **kw)
    B.add(c + nn * 0.006, (0.041 * sc, 0.006, 0.0125 * sc), ROSE, bone, bevel=0.003, **kw)
    B.add(c + nn * 0.010 + R @ Vector((-s * 0.006 * sc, 0, 0)), (0.0055 * sc, 0.004, 0.0125 * sc), BLACK, bone,
          bevel=0.002, **kw)


def claw_frame(side):
    """palm axis a, opening direction o (dactyl side), outer side direction (for the spikes) of the given claw"""
    s = 1 if side == "L" else -1
    S, E, W, F = (X(p, s) for p in CLAW)
    F = W + (F - W) * CSIZE[side]                 # the crusher's palm is longer too
    a = (F - W).normalized()
    o = Vector((-s * 0.55, 0.0, 0.83))
    o = (o - a * o.dot(a)).normalized()
    out = a.cross(o).normalized()
    if out.x * s < 0:
        out = -out
    return S, E, W, F, a, o, out


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=1515, tier=3, plates=False, th=0.36)
    # ================= carapace (Spine): domed bronze loft, flatter underside, slate rim band
    car = B.tube([ring(y, hw, zc, ht, hb) for y, hw, zc, ht, hb in CAR], BRONZE, "Spine")
    B.tube([ring(y, hw + 0.016, zc + 0.004, 0.026, 0.026, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], SHELL_D,
           "Spine", nostud=True)                                                                   # rim band
    B.tube([ring(y, hw * 0.80, zc - hb * 0.72, 0.03, 0.035, n=2.2, seg=20) for y, hw, zc, ht, hb in CAR[1:-1]],
           BELLY_PALE, "Spine", nostud=True)                                                       # sternum
    # slate H-groove ridges on the dome: midline (front half), the cervical V, two branchial arcs

    def bar_on(pts, w, bone="Spine", color=SHELL_D, thick=0.014):
        hits = [surf_hit(B, [car], (x, y, 2.0), (0, 0, -1)) for x, y in pts]
        for (a, na), (b, nb) in zip(hits, hits[1:]):
            n = (na + nb).normalized()
            d = (b - a).normalized()
            B.bar(a + na * 0.003 - d * 0.012, b + nb * 0.003 + d * 0.012, n, w, thick, color, bone, studs=[],
                  nostud=True, role="limb", rnd=0.3)
    bar_on([(0, -0.46), (0, -0.37), (0, -0.28), (0, -0.19), (0, -0.11)], 0.055)
    bar_on([(-0.44, 0.08), (-0.32, -0.01), (-0.17, -0.075), (0, -0.10), (0.17, -0.075), (0.32, -0.01),
            (0.44, 0.08)], 0.048)
    for s in (1, -1):
        bar_on([(s * 0.13, -0.07), (s * 0.19, 0.05), (s * 0.20, 0.18), (s * 0.17, 0.30), (s * 0.11, 0.40)], 0.042)
    # rose-coral teeth along the front-side (anterolateral) margins + two small frontal teeth
    for s in (1, -1):
        for y, L, w in ((-0.47, 0.095, 0.032), (-0.39, 0.12, 0.038), (-0.30, 0.13, 0.040), (-0.20, 0.125, 0.040),
                        (-0.10, 0.11, 0.036), (0.0, 0.09, 0.032)):
            hw, zc, ht, hb = car_at(y)
            p = Vector((s * (hw + 0.008), y, zc + 0.012))
            rose_spike(B, p, (s * 1.0, -0.45, 0.25), L, w, "Spine")
        rose_spike(B, Vector((s * 0.075, -0.538, 0.53)), (s * 0.15, -1.0, 0.35), 0.07, 0.026, "Spine")
    # ================= front: orbits + short thick eyestalks, rose slit eyes, slate V brow plate
    for s, side in ((1, "L"), (-1, "R")):
        eb = "Eye_" + side
        base = Vector((s * 0.20, -0.49, 0.50))
        top = base + Vector((s * 0.02, -0.06, 0.075))
        B.add(Vector((s * 0.20, -0.505, 0.50)), (0.068, 0.03, 0.05), BLACK, "Spine", role="detail", bevel=0.012,
              studs=[])                                                                             # orbit
        B.seg(base, top, 0.042, 0.042, BRONZE, eb, ext=0.03, rnd=0.42, role="limb")              # stalk (0.07H)
        bulb = B.add(top + Vector((0, -0.012, 0.012)), (0.060, 0.046, 0.052), BRONZE, eb, rnd=0.45, role="limb")
        ep, en = surf_hit(B, [bulb], (s * 0.225, -1.0, 0.585), (0, 1, 0))
        crab_eye(B, ep + en * 0.002, s, en, eb, tilt=15, sc=1.15)
        ANCH["Eye_" + side] = tuple(base)
    for s in (1, -1):                                                                              # brow plate
        Rb = Euler((math.radians(-12), math.radians(-s * 15), 0), "XYZ").to_matrix()
        B.add(Vector((s * 0.135, -0.565, 0.638)), (0.13, 0.045, 0.024), SHELL_D, "Spine", R=Rb, rnd=0.3,
              role="limb", top=(0.92, 0.85))
    # ================= mandibles (Mouth): flat pale plates over a dark mouth, small ivory teeth on the inner edges
    B.add(Vector((0, -0.528, 0.405)), (0.10, 0.012, 0.048), MOUTH, "Spine", role="detail", bevel=0.004, studs=[])
    for s in (1, -1):
        B.add(Vector((s * 0.058, -0.548, 0.405)), (0.046, 0.016, 0.062), BELLY_PALE, "Mouth", rot=(6, 0, -s * 8),
              rnd=0.35, role="limb", nostud=True, bot=(0.8, 1.0))
        for z in (0.44, 0.405, 0.37):
            B.spike(Vector((s * 0.014, -0.56, z)), (-s * 1.0, -0.2, -0.1), 0.026, 0.010, IVORY, "Mouth")
    ANCH["Mouth"] = (0, -0.58, 0.41)
    # ================= claws: merus (Arm), carpus (Fore), oval palm + fixed finger (Claw), movable finger (Pincer)
    for s, side in ((1, "L"), (-1, "R")):
        c = CSIZE[side]
        S, E, W, F, a, o, out = claw_frame(side)
        arm, fore, claw, pin = "Arm_" + side, "Fore_" + side, "Claw_" + side, "Pincer_" + side
        B.seg(S, E, 0.072 * c, 0.090 * c, BRONZE, arm, side=(0, 0, 1), ext=0.04, ext1=0.03, top=(0.95, 0.95),
              rnd=0.40)                                                                              # merus
        for t in (0.40, 0.75):                                                                       # merus spikes
            p = S.lerp(E, t) + Vector((0, 0, 0.085 * c))
            rose_spike(B, p, (s * 0.35, -0.25, 1.0), 0.075 * c, 0.026 * c, arm)
        B.add(E, (0.088 * c, 0.088 * c, 0.088 * c), SHELL_D, fore, rnd=0.42)                          # knuckle
        B.seg(E, W, 0.085 * c, 0.092 * c, BRONZE, fore, ext=0.02, ext1=0.03, top=(1.1, 1.1), rnd=0.42)  # carpus
        rose_spike(B, E.lerp(W, 0.55) + out * 0.08 * c, out + Vector((0, -0.3, 0.4)), 0.08 * c, 0.028 * c, fore)
        B.add(W, (0.095 * c, 0.095 * c, 0.095 * c), SHELL_D, claw, rnd=0.42)                          # wrist knuckle
        # palm: a big oval bronze block, thin across (out), tall in the finger plane (o)
        P0 = W - a * 0.03
        palm = B.seg(P0, F, 0.118 * c, 0.170 * c, BRONZE, claw, side=out, top=(0.92, 0.86), rnd=0.45)
        for t, L in ((0.18, 0.08), (0.42, 0.095), (0.66, 0.10), (0.88, 0.09)):                     # outer spikes
            p = P0.lerp(F, t) + out * 0.114 * c + o * 0.05 * c
            rose_spike(B, p, out * 1.0 + a * 0.35 + o * 0.2, L * c, 0.030 * c, claw)
        # fixed finger (pollex, -o side) on Claw; movable finger (dactyl, +o side) on Pincer; tips curve inward
        for bone, sgn, Lf, w0 in ((claw, -1, 0.28, 0.080), (pin, 1, 0.30, 0.074)):
            r0 = F + o * sgn * 0.085 * c - a * 0.05
            dirf = (a - o * sgn * 0.22).normalized()
            tip = r0 + dirf * Lf * c
            B.seg(r0, r0.lerp(tip, 0.66), w0 * c, 0.062 * c, BRONZE, bone, side=out, top=(0.82, 0.74),
                  rnd=0.40)
            m = r0.lerp(tip, 0.60)
            B.seg(m, m.lerp(tip, 0.78), w0 * 0.70 * c, 0.046 * c, SHELL_D, bone, side=out, top=(0.70, 0.70),
                  rnd=0.35, role="limb")
            B.spike(m.lerp(tip, 0.66), dirf, (tip - m).length * 0.50, w0 * 0.42 * c, BLACK, bone, side=out)
            for t in (0.28, 0.52):                                                                  # crusher molars
                q = r0.lerp(tip, t) - o * sgn * 0.058 * c
                B.add(q, (0.026 * c, 0.020 * c, 0.018 * c), SHELL_D, bone, R=bk.frame_from(r0, tip, out),
                      role="detail", bevel=0.005, studs=[])
            if bone == pin:
                ANCH["Claw_Tip_" + side] = tuple(tip)
                ANCH["Hinge_" + side] = tuple(r0)
                rose_spike(B, r0.lerp(tip, 0.30) + o * 0.06 * c, o + a * 0.7, 0.07 * c, 0.024 * c, pin)
    # ================= six walking legs: slate coxa + flat merus, bronze knee, slate propodus, black dactyl tip
    for s, side in ((1, "L"), (-1, "R")):
        for i in (1, 2, 3):
            j = leg_name(i, side)
            H, K, A, T = leg_pts(i, s)
            leg, shin, foot = "Leg_%d" % j, "Shin_%d" % j, "Foot_%d" % j
            B.add(H, (0.066, 0.066, 0.055), SHELL_D, leg, rnd=0.42)                                  # coxa
            B.seg(H, K, 0.056, 0.078, SHELL_D, leg, side=(0, 0, 1), ext=0.05, ext1=0.025, top=(0.90, 0.85),
                  rnd=0.40)                                                                         # merus (flat)
            B.add(K, (0.058, 0.058, 0.058), BRONZE, shin, rnd=0.42)                                   # knee
            B.seg(K, A, 0.046, 0.056, SHELL_D, shin, ext=0.02, ext1=0.01, top=(0.80, 0.80), rnd=0.38)  # propodus
            B.seg(A, T, 0.034, 0.036, SHELL_D, foot, ext=0.02, top=(0.7, 0.7), rnd=0.3)              # dactyl
            B.spike(T - (T - A).normalized() * 0.012, T - A, 0.045, 0.022, BLACK, foot)              # black tip
            ANCH["Foot_%d" % j] = tuple(T)
    B.build()
    global H_MODEL
    mn, mx = k.bounds()
    H_MODEL = mx.z
    pitch = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)
    bk.stud_skin(k, pitch)
    return {"TH": round(B.th, 3), "pitch": pitch, "H": round(mx.z, 3), "lowest": round(mn.z, 3),
            "size": [round(v, 3) for v in (mx - mn)]}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, -0.05, 0.47), "Root", tail=(0, -0.30, 0))
    k.joint("Mouth", (0, -0.54, 0.46), "Spine", tail=(0, -0.05, -0.10))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Eye_" + side, ANCH.get("Eye_" + side, (s * 0.215, -0.50, 0.585)), "Spine", tail=(s * 0.02, -0.06,
                                                                                                    0.08))
        S, E, W, F, a, o, out = claw_frame(side)
        k.joint("Arm_" + side, tuple(S), "Spine")
        k.joint("Fore_" + side, tuple(E), "Arm_" + side)
        k.joint("Claw_" + side, tuple(W), "Fore_" + side, tail=tuple(a * 0.3))
        k.joint("Pincer_" + side, ANCH.get("Hinge_" + side, tuple(F)), "Claw_" + side, tail=tuple(a * 0.25))
        k.joint("Claw_Tip_" + side, ANCH.get("Claw_Tip_" + side, tuple(F + a * 0.3)), "Pincer_" + side,
                tail=tuple(a * 0.1))
        for i in (1, 2, 3):
            j = leg_name(i, side)
            H, K, A, T = leg_pts(i, s)
            k.joint("Leg_%d" % j, tuple(H), "Spine")
            k.joint("Shin_%d" % j, tuple(K), "Leg_%d" % j)
            k.joint("Foot_%d" % j, tuple(A), "Shin_%d" % j, tail=tuple(T - A))
            p = POLE[i]
            k.add_leg2("Leg_%d" % j, "Shin_%d" % j, "Foot_%d" % j, knee=(s * p[0], p[1], p[2]))


def check_pairs():
    P = []
    for side, legs in (("L", (1, 2, 3)), ("R", (4, 5, 6))):
        for a, b in ((legs[0], legs[1]), (legs[1], legs[2])):
            for x in ("Leg", "Shin", "Foot"):
                for y in ("Leg", "Shin", "Foot"):
                    P.append(("%s_%d" % (x, a), "%s_%d" % (y, b)))
        P += [("Arm_" + side, "Leg_%d" % legs[0]), ("Arm_" + side, "Shin_%d" % legs[0]),
              ("Fore_" + side, "Shin_%d" % legs[0]), ("Claw_" + side, "Shin_%d" % legs[0]),
              ("Claw_" + side, "Spine"), ("Pincer_" + side, "Spine"), ("Fore_" + side, "Spine"),
              ("Claw_" + side, "Eye_L"), ("Claw_" + side, "Eye_R"), ("Pincer_" + side, "Eye_L"),
              ("Pincer_" + side, "Eye_R"), ("Claw_" + side, "Mouth"), ("Pincer_" + side, "Mouth"),
              ("Claw_" + side, "Pincer_" + side)]
    P += [("Claw_L", "Claw_R"), ("Pincer_L", "Pincer_R"), ("Claw_L", "Pincer_R"), ("Claw_R", "Pincer_L"),
          ("Fore_L", "Fore_R"), ("Eye_L", "Spine"), ("Eye_R", "Spine"), ("Mouth", "Spine")]
    return P


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        S, E, W, F, a, o, out_ = claw_frame(side)
        c = CSIZE[side]
        out += [(tuple(S), tuple(S), 0.11 * c, "Arm_" + side), (tuple(E), tuple(E), 0.10 * c, "Fore_" + side),
                (tuple(W), tuple(W), 0.11 * c, "Claw_" + side),
                (ANCH.get("Hinge_" + side, tuple(F)), ANCH.get("Hinge_" + side, tuple(F)), 0.08 * c,
                 "Pincer_" + side)]
        out.append((ANCH.get("Eye_" + side, (s * 0.215, -0.50, 0.585)), ANCH.get("Eye_" + side, (s * 0.215, -0.50,
                                                                                                0.585)), 0.07,
                    "Eye_" + side))
        for i in (1, 2, 3):
            j = leg_name(i, side)
            H, K, A, T = leg_pts(i, s)
            out += [(tuple(H), tuple(H), 0.09, "Leg_%d" % j), (tuple(K), tuple(K), 0.07, "Shin_%d" % j),
                    (tuple(A), tuple(A), 0.05, "Foot_%d" % j)]
    out.append(((0, -0.54, 0.46), (0, -0.54, 0.38), 0.07, "Mouth"))
    return out


HEAD_XF = []
