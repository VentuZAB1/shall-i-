# Coral Crusher (Tide / Water egg, MEDIUM 15 %, 2026-10-27; model round 2 after review 1) - plan
# _review/CoralCrusher_plan.md v2. A giant armoured crab in the FIERCE studded style: a wide low copper-bronze carapace
# (loft tube, domed top) with raised slate armour plates (an H groove), a slate rim band over a cream lip, a stepped
# rear ledge, rose-coral teeth along the front-side margin, short dark eyestalks under slate lids with narrow rose slit
# eyes, one slate V brow plate, small slate mandibles with ivory hook tips, two big claws (the right one is the heavier
# CRUSHER, the left the slimmer cutter) with rose spikes, cream undersides and dark fingertips, and six low walking legs
# (dark-bronze merus, slate propodus, black tips) on the AbyssWeaver multi-leg IK chain.
# No glow (rose sparkles / bubbles / sand puffs = Studio VFX on the anchor bones).
import math
from mathutils import Vector, Matrix, Euler, Quaternion

DISPLAY = "Coral Crusher"
MOTION = "Walk"
RIG = "quad"                 # the label the Studio side stores for multi-leg walkers (Weaver / Mantis precedent)
HEIGHT = 6.1                 # studs to the top of the claws (H_MODEL). r2: the rest claws dropped 15 deg (N3), H_MODEL
                             # 1.287 -> 1.049; 7.5 x 1.049 / 1.287 = 6.1 keeps the in-game body size of round 1

# Blender colours (Roblox renders ~0.6x darker)
BRONZE = (214, 110, 70)      # f85 MM1: RUST COPPER (was 200,136,88 - read tan / mud). Carapace top, claw bodies (studded)
BRONZE_D = (150, 74, 50)     # f85 MM1 (was 146,96,62): leg merus, eye stalks + bulbs (a darker copper)
SHELL_D = (80, 46, 34)       # f85 MM1 (was 100,66,46): legs, seams / ridges, claw knuckles, brow plate, fingertips
BELLY_PALE = (240, 226, 200) # underside, pale lip, sternum
ROSE = (255, 135, 165)       # THE accent: claw spikes, margin teeth, eye slits (r2 N5: clearer at 0.6x)
ROSE_D = (200, 70, 110)      # spike bases
BLACK = (14, 14, 22)         # claw tips, pupils, eye sockets, leg tips
IVORY = (240, 236, 222)      # mandible tooth tips
MOUTH = (86, 26, 40)         # mouth

H_MODEL = 1.42               # measured top of the claws (refreshed by model())
ANCH = {}

# ---- carapace stations: y, half width, centre z, top half-height, bottom half-height
CAR = [(-0.535, 0.36, 0.385, 0.07, 0.07), (-0.48, 0.52, 0.39, 0.13, 0.10), (-0.38, 0.64, 0.39, 0.18, 0.115),
       (-0.20, 0.70, 0.385, 0.215, 0.125), (0.00, 0.67, 0.38, 0.22, 0.125), (0.20, 0.57, 0.375, 0.20, 0.115),
       (0.36, 0.43, 0.365, 0.16, 0.105), (0.48, 0.27, 0.36, 0.105, 0.085), (0.545, 0.12, 0.355, 0.05, 0.05)]
NC = 2.4
RIM_OUT, RIM_H = 0.030, 0.040   # f85 MM2: the cream rim band (r5 slate band 0.016 proud, 0.026 half-height)


def rear(y):
    """0 at the shell middle -> 1 at the rear (the game camera sees the rear edge; no spines or legs cover it)"""
    return min(max(y / 0.36, 0.0), 1.0)


def rim_h(y):
    return RIM_H + 0.045 * rear(y)          # f85 MM2: the band deepens downward toward the rear (0.040 -> 0.085)

# ---- legs (left side; right = mirror): azimuth (deg from +x toward +y), hip (x, y, z), knee (r, z), ankle (r, z),
# toe (r, z) measured from the hip along the azimuth
HIPZ = 0.27
LEGP = {1: (-34, (0.50, -0.20), (0.21, 0.30), (0.35, 0.068), (0.40, 0.014)),      # r2 (M2): low knees, short chain
        2: (0, (0.56, 0.04), (0.23, 0.30), (0.37, 0.068), (0.42, 0.014)),
        3: (34, (0.48, 0.28), (0.21, 0.29), (0.345, 0.068), (0.395, 0.014))}
POLE = {1: (0.35, -0.20, 1.0), 2: (0.40, 0.0, 1.0), 3: (0.35, 0.22, 1.0)}
# claw joints (left side): shoulder, elbow (merus/carpus), wrist (carpus/palm), finger base; c = size factor
CLAW0 = (Vector((0.30, -0.46, 0.30)), Vector((0.60, -0.71, 0.46)), Vector((0.53, -0.92, 0.62)),
         Vector((0.50, -1.10, 0.90)))
CLAW_DROP = 15.0                        # r2 (N3): rest claws 15 deg lower, so the act's lift reads as a lift
CLAW = tuple(CLAW0[0] + Matrix.Rotation(math.radians(CLAW_DROP), 3, "X") @ (p - CLAW0[0]) for p in CLAW0)
CSIZE = {"L": 0.98, "R": 1.20}         # R = the CRUSHER (the big claw that waves), L = the cutter


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
    B.add(c, (0.050 * sc, 0.008, 0.026 * sc), BLACK, bone, bevel=0.004, top=(0.78, 1.0), **kw)
    B.add(c + nn * 0.006 + R @ Vector((0, 0, -0.003)), (0.042 * sc, 0.006, 0.0125 * sc), ROSE, bone, bevel=0.003,
          top=(0.55, 1.0), **kw)
    B.add(c + nn * 0.010 + R @ Vector((-s * 0.004 * sc, 0, -0.003)), (0.0042 * sc, 0.004, 0.0125 * sc), BLACK,
          bone, bevel=0.0015, **kw)


def claw_frame(side):
    """palm axis a, opening direction o (dactyl side), outer side direction (for the spikes) of the given claw"""
    s = 1 if side == "L" else -1
    S, E, W, F = (X(p, s) for p in CLAW)
    F = W + (F - W) * CSIZE[side]                 # the crusher's palm is longer too
    a = (F - W).normalized()
    o = Vector((-s * 0.18, 0.0, 1.0))
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
    B.tube([ring(y, hw + RIM_OUT + 0.035 * rear(y), zc + 0.004 - rim_h(y) + RIM_H, rim_h(y), rim_h(y), seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], BELLY_PALE,
           "Spine", nostud=True)                                                   # rim band (f85 MM2: cream, was slate)
    B.tube([ring(y, hw + 0.012, zc + 0.010 + RIM_H, 0.006, 0.006, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], SHELL_D,
           "Spine", nostud=True)                                                   # f85 MM2: thin slate seam above it (inside the band edge)
    B.tube([ring(y, hw * 0.80, zc - hb * 0.72, 0.03, 0.035, n=2.2, seg=20) for y, hw, zc, ht, hb in CAR[1:-1]],
           BELLY_PALE, "Spine", nostud=True)                                                       # sternum
    # pale underside (r2 M4b): a cream skin hugging the lower carapace from just under the slate rim band down to
    # the belly (0.008 proud), so it shows as a cream band from the side between the legs
    B.tube([ring(y, hw + 0.008, zc - 0.012, 0.012, hb + 0.008, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]],
           BELLY_PALE, "Spine", nostud=True)                                                       # pale underside

    def shell_w(hw, hb, dz):                     # carapace half width at dz below the station centre
        return hw * max(1.0 - (min(dz / hb, 0.99)) ** NC, 0.0) ** (1.0 / NC)
    B.tube([ring(y, hw + 0.040 + 0.030 * rear(y), zc - 0.100, 0.026, 0.030, seg=28)
            for y, hw, zc, ht, hb in CAR[1:-1]], BELLY_PALE, "Spine", nostud=True)   # cream lip (f85 MM2: lower, wider)
    # stepped rear plate (r2 M4a): a slate ledge above the rim band around the rear half of the shell
    STEP = ((0.0, 0.000), (0.10, 0.010), (0.20, 0.016), (0.36, 0.016), (0.46, 0.010), (0.52, 0.000))
    srings = []
    for y, pr in STEP:
        hw, zc, ht, hb = car_at(y)
        zz = 0.40 * ht - 0.010                                  # r2 N3: 0.01 lower (one dome, not a shelf)
        srings.append(ring(y, hw * (1.0 - (zz / ht) ** NC) ** (1.0 / NC) + pr, zc + zz, 0.020, 0.020, seg=28))
    B.tube(srings, SHELL_D, "Spine", nostud=True)
    # slate H-groove ridges on the dome: midline (front half), the cervical V, two branchial arcs

    def bar_on(pts, w, bone="Spine", color=SHELL_D, thick=0.022, proud=0.020):
        """raised slate armour plate along the dome (r2 M4a: 0.022 thick, 0.02 proud)"""
        hits = [surf_hit(B, [car], (x, y, 2.0), (0, 0, -1)) for x, y in pts]
        for (a, na), (b, nb) in zip(hits, hits[1:]):
            n = (na + nb).normalized()
            d = (b - a).normalized()
            B.bar(a + na * (proud - thick) - d * 0.016, b + nb * (proud - thick) + d * 0.016, n, w, thick, color,
                  bone, studs=[], nostud=True, role="detail", bevel=0.008)
    bar_on([(0, -0.46), (0, -0.37), (0, -0.28), (0, -0.19), (0, -0.11)], 0.062)
    bar_on([(-0.36, 0.33), (-0.22, 0.25), (-0.10, 0.215), (0, 0.205), (0.10, 0.215), (0.22, 0.25), (0.36, 0.33)],
           0.050)                                                                    # r2 N1: rear plate row
    bar_on([(-0.44, 0.08), (-0.32, -0.01), (-0.17, -0.075), (0, -0.10), (0.17, -0.075), (0.32, -0.01),
            (0.44, 0.08)], 0.056)
    for s in (1, -1):
        bar_on([(s * 0.13, -0.07), (s * 0.19, 0.05), (s * 0.20, 0.18), (s * 0.17, 0.30), (s * 0.11, 0.40)], 0.050)
    # rose-coral teeth along the front-side (anterolateral) margins + two small frontal teeth
    for s in (1, -1):
        for ti, (y, L, w) in enumerate(((-0.47, 0.095, 0.032), (-0.39, 0.12, 0.038), (-0.30, 0.13, 0.040),
                                        (-0.20, 0.125, 0.040), (-0.10, 0.11, 0.036), (0.0, 0.095, 0.033),
                                        (0.11, 0.08, 0.030), (0.22, 0.065, 0.026))):
            hw, zc, ht, hb = car_at(y)
            p = Vector((s * (hw + 0.008), y, zc + 0.012))
            big = ti % 2 == 1                                   # r2 N4: large / small alternating spines
            rose_spike(B, p, (s * 1.0, -0.45, 0.25), L * (1.45 if big else 0.80), w * (1.15 if big else 0.90),
                       "Spine")
    # rose coral growths on the rear carapace (the game camera sees the back): short smooth branches
    for x, y, sc, rot in ((0.26, 0.20, 1.0, 20), (-0.20, 0.30, 0.85, -35), (0.06, 0.40, 0.7, 60),
                          (0.075, 0.075, 1.30, 10), (-0.085, 0.02, 1.20, -30)):           # f85 9+ 3: dome centre
        p, n = surf_hit(B, [car], (x, y, 2.0), (0, 0, -1))
        B.add(p + n * 0.005, (0.045 * sc, 0.045 * sc, 0.022 * sc), ROSE_D, "Spine", R=face_R(-n, up=(0, 1, 0)),
              rnd=0.45, nostud=True)
        for bx, by, L, lean in ((0.0, 0.0, 0.11, 0.0), (0.03, 0.02, 0.08, 0.6), (-0.03, -0.01, 0.075, -0.6)):
            d = Vector((bx * 8 + lean * 0.5, by * 6, 1.0))
            d = Euler((0, 0, math.radians(rot)), "XYZ").to_matrix() @ d
            B.spike(p + Vector((bx, by, 0)) * sc, d, L * sc, 0.024 * sc, ROSE, "Spine", top=(0.85, 0.85),
                    nostud=True, rnd=0.45, role="limb")
    # ================= front: orbits + short thick eyestalks, rose slit eyes, slate V brow plate
    for s, side in ((1, "L"), (-1, "R")):
        eb = "Eye_" + side
        base = Vector((s * 0.20, -0.525, 0.40))
        top = base + Vector((s * 0.02, -0.055, 0.07))
        B.seg(base, top, 0.044, 0.044, BRONZE_D, eb, ext=0.02, rnd=0.42, role="limb", nostud=True)  # stalk
        bulb = B.add(top + Vector((0, -0.016, 0.012)), (0.062, 0.046, 0.054), BRONZE_D, eb, rnd=0.45, role="limb",
                     nostud=True)                                                                  # bulb (r2 M7)
        ep, en = surf_hit(B, [bulb], (s * 0.222, -1.0, 0.476), (0, 1, 0))
        crab_eye(B, ep + en * 0.002, s, en, eb, tilt=15, sc=1.1)
        Rl = face_R(en) @ Euler((0, math.radians(-s * 18), 0), "XYZ").to_matrix()
        B.add(ep + en * 0.012 + Vector((s * 0.004, 0, 0.030)), (0.074, 0.024, 0.022), SHELL_D, eb, R=Rl,
              rnd=0.25, role="limb", studs=[], nostud=True)                                       # slate lid / brow
        ANCH["Eye_" + side] = tuple(base)
    for s in (1, -1):                                         # ONE slate V brow plate, ~0.14 wide (r2 N1)
        Rb = Euler((math.radians(-8), math.radians(-s * 16), math.radians(-s * 14)), "XYZ").to_matrix()
        B.add(Vector((s * 0.036, -0.560, 0.452)), (0.042, 0.030, 0.026), SHELL_D, "Spine", R=Rb, rnd=0.3,
              role="limb", top=(0.92, 0.85))
    # ================= mandibles (Mouth): flat pale plates over a dark mouth, small ivory teeth on the inner edges
    B.add(Vector((0, -0.522, 0.335)), (0.085, 0.012, 0.045), MOUTH, "Spine", role="detail", bevel=0.004, studs=[])
    for s in (1, -1):                                         # r2 M3: small slate mandibles, ivory hook tips only
        B.add(Vector((s * 0.030, -0.546, 0.335)), (0.020, 0.012, 0.034), SHELL_D, "Mouth",
              rot=(8, s * 20, -s * 6), rnd=0.35, role="limb", nostud=True, bot=(0.70, 1.0))
        B.spike(Vector((s * 0.022, -0.556, 0.306)), (-s * 0.8, -0.35, -0.6), 0.014, 0.0065, IVORY, "Mouth")
    ANCH["Mouth"] = (0, -0.57, 0.33)
    # ================= claws: merus (Arm), carpus (Fore), oval palm + fixed finger (Claw), movable finger (Pincer)
    for s, side in ((1, "L"), (-1, "R")):
        c = CSIZE[side]
        S, E, W, F, a, o, out = claw_frame(side)
        arm, fore, claw, pin = "Arm_" + side, "Fore_" + side, "Claw_" + side, "Pincer_" + side
        B.add(S, (0.080 * c, 0.080 * c, 0.080 * c), BRONZE_D, arm, rnd=0.45, nostud=True)          # shoulder knuckle
        B.seg(S, E, 0.072 * c, 0.090 * c, BRONZE, arm, side=(0, 0, 1), ext=0.0, ext1=0.03, top=(0.95, 0.95),
              rnd=0.40)                                                                              # merus
        for t in (0.40, 0.75):                                                                       # merus spikes
            p = S.lerp(E, t) + Vector((0, 0, 0.085 * c))
            rose_spike(B, p, (s * 0.35, -0.25, 1.0), 0.10 * c, 0.034 * c, arm)
        B.add(E, (0.088 * c, 0.088 * c, 0.088 * c), BRONZE_D, fore, rnd=0.42, nostud=True)            # knuckle
        B.seg(E, W, 0.085 * c, 0.092 * c, BRONZE, fore, ext=0.02, ext1=0.03, top=(1.1, 1.1), rnd=0.42)  # carpus
        rose_spike(B, E.lerp(W, 0.55) + out * 0.08 * c, out + Vector((0, -0.3, 0.4)), 0.10 * c, 0.034 * c, fore)
        B.add(W, (0.095 * c, 0.095 * c, 0.095 * c), BRONZE_D, claw, rnd=0.42, nostud=True)            # wrist knuckle
        # palm: a big oval bronze block, thin across (out), tall in the finger plane (o)
        P0 = W - a * 0.03
        rings = []
        for t, wx, wo in ((0.0, 0.070, 0.095), (0.10, 0.098, 0.140), (0.32, 0.118, 0.172), (0.58, 0.120, 0.172),
                          (0.82, 0.108, 0.152), (1.0, 0.088, 0.128)):
            cc = P0.lerp(F, t)
            rg = []
            for q in range(20):
                ang = 2 * math.pi * q / 20
                cs, sn = math.cos(ang), math.sin(ang)
                rg.append(cc + out * (wx * c * math.copysign(abs(cs) ** (2 / 2.3), cs)) +
                          o * (wo * c * math.copysign(abs(sn) ** (2 / 2.3), sn)))
            rings.append(rg)
        palm = B.tube(rings, BRONZE, claw, nostud=True)                                 # oval palm (smooth, r2 M1)
        # (r3, review 2 M1: the cream claw underside is dropped entirely - claws are smooth bronze)
        # (r2 N2: the pale palm keel + merus keel strips were dropped - they read as plastic inserts)
        for t, L in ((0.18, 0.08), (0.42, 0.095), (0.66, 0.10), (0.88, 0.09)):                     # outer spikes
            p = P0.lerp(F, t) + out * 0.114 * c + o * 0.05 * c
            rose_spike(B, p, out * 1.0 + a * 0.35 + o * 0.2, L * 1.28 * c, 0.036 * c, claw)
        # fixed finger (pollex, -o side) on Claw; movable finger (dactyl, +o side) on Pincer; tips curve inward
        for bone, sgn, L1, L2, w0 in ((claw, -1, 0.20, 0.17, 0.080), (pin, 1, 0.21, 0.18, 0.074)):
            r0 = F + o * sgn * 0.097 * c - a * 0.06                # f85 9+ 2: roots 0.085 -> 0.097 (gape ~0.06 H)
            d1 = (a - o * sgn * 0.06).normalized()
            m1 = r0 + d1 * L1 * c
            d2 = (a - o * sgn * 0.36).normalized()                 # r3: tips no longer overlap at rest
            tip = m1 + d2 * L2 * c
            B.seg(r0, m1, w0 * c, 0.054 * c, BRONZE, bone, side=out, ext1=0.02, top=(0.88, 0.80), rnd=0.40,
                  nostud=True)                                      # finger base (smooth bronze, r2 M1)
            B.seg(m1 - d1 * 0.03, m1 + d2 * L2 * 0.62 * c, w0 * 0.82 * c, 0.046 * c, SHELL_D, bone, side=out,
                  top=(0.72, 0.70), rnd=0.35, role="limb", nostud=True)
            B.spike(m1 + d2 * L2 * 0.50 * c, d2, L2 * 0.55 * c, w0 * 0.45 * c, BLACK, bone, side=out)
            for t in (0.35, 0.75):                                                                  # crusher molars
                q = r0.lerp(m1, t) - o * sgn * 0.052 * c
                B.add(q, (0.030 * c, 0.026 * c, 0.022 * c), SHELL_D, bone, R=bk.frame_from(r0, m1, out),  # f85: bigger
                      role="detail", bevel=0.005, studs=[])
            if bone == pin:
                ANCH["Claw_Tip_" + side] = tuple(tip)
                ANCH["Hinge_" + side] = tuple(r0)
                rose_spike(B, r0.lerp(m1, 0.55) + o * 0.06 * c, o + a * 0.7, 0.10 * c, 0.034 * c, pin)
    # ================= six walking legs: slate coxa + flat merus, bronze knee, slate propodus, black dactyl tip
    for s, side in ((1, "L"), (-1, "R")):
        for i in (1, 2, 3):
            j = leg_name(i, side)
            H, K, A, T = leg_pts(i, s)
            leg, shin, foot = "Leg_%d" % j, "Shin_%d" % j, "Foot_%d" % j
            B.add(H, (0.080, 0.080, 0.068), SHELL_D, leg, rnd=0.42)                                  # coxa (f85)
            B.seg(H, K, 0.084, 0.110, BRONZE_D, leg, side=(0, 0, 1), ext=0.05, ext1=0.03, top=(0.90, 0.86),
                  rnd=0.40)                                                         # merus (f85 9+ 1: +20 %)
            dm = (K - H).normalized()
            B.seg(H + dm * 0.03 + Vector((0, 0, 0.068)), K - dm * 0.03 + Vector((0, 0, 0.070)), 0.022, 0.086,
                  BRONZE, leg, side=(0, 0, 1), top=(1.0, 0.85), rnd=0.35)                           # merus top plate
            rose_spike(B, H.lerp(K, 0.62) + Vector((0, 0, 0.094)), dm * 0.35 + Vector((0, 0, 1)), 0.085, 0.029, leg)
            B.add(K, (0.072, 0.072, 0.072), BRONZE_D, shin, rnd=0.42)                                 # knee (r2 M2)
            B.seg(K, A, 0.060, 0.070, SHELL_D, shin, ext=0.025, ext1=0.01, top=(0.76, 0.76), rnd=0.38)  # propodus
            B.seg(A, T, 0.038, 0.040, SHELL_D, foot, ext=0.02, top=(0.7, 0.7), rnd=0.3)              # dactyl
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
    k.joint("Spine", (0, -0.05, 0.38), "Root", tail=(0, -0.30, 0))
    k.joint("Mouth", (0, -0.535, 0.375), "Spine", tail=(0, -0.05, -0.10))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Eye_" + side, ANCH.get("Eye_" + side, (s * 0.20, -0.525, 0.40)), "Spine", tail=(s * 0.02, -0.06,
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
                (ANCH.get("Hinge_" + side, tuple(F)), ANCH.get("Hinge_" + side, tuple(F)), 0.12 * c,
                 "Pincer_" + side)]
        out.append((ANCH.get("Eye_" + side, (s * 0.20, -0.525, 0.40)), ANCH.get("Eye_" + side, (s * 0.215, -0.50,
                                                                                                0.40)), 0.09,
                    "Eye_" + side))
        for i in (1, 2, 3):
            j = leg_name(i, side)
            H, K, A, T = leg_pts(i, s)
            out += [(tuple(H), tuple(H), 0.09, "Leg_%d" % j), (tuple(K), tuple(K), 0.07, "Shin_%d" % j),
                    (tuple(A), tuple(A), 0.05, "Foot_%d" % j)]
    out.append(((0, -0.535, 0.375), (0, -0.535, 0.29), 0.07, "Mouth"))
    return out


HEAD_XF = []


# ------------------------------------------------------------------ animation (clips 2026-10-27, refs: ANIM_REFS.md)
# BASE POSE (review 2 M2, lead ruling): every clip keys the Spine at the walk's 45 deg yaw with the six feet planted on
# the yawed rest spots, so the runtime idle <-> walk crossfade turns nothing (only the leg phase blends). The game moves
# pets along their facing (-Y); the walk carries the body at 45 deg (a diagonal scuttle, the crusher side leads) and
# steps the legs along the travel axis in alternating tripods.
import petkit as pk
import _common as cm

LEGS6 = ["Leg_%d" % j for j in range(1, 7)]
YAW_WALK = 45.0                 # r2 (M1, lead ruling): a 45 deg diagonal scuttle
BASE_YAW = YAW_WALK             # r3 (review 2 M2): idle / roar / act rest at the same yaw
WALK_OFF = [("Leg_1", 0.00), ("Leg_5", 0.04), ("Leg_3", 0.08), ("Leg_4", 0.50), ("Leg_2", 0.54), ("Leg_6", 0.58)]


def curve(keys, f):
    """smoothstep through (frame, value) keys"""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            return v0 + (v1 - v0) * u * u * (3 - 2 * u)
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]


def about_spine(k, P, yaw):
    J = k.J["Spine"]
    return J + Quaternion((0, 0, 1), math.radians(yaw)) @ (Vector(P) - J)


def ankle_to(k, leg, f, P, yaw=0.0, toe=0.0):
    """put the ANKLE of `leg` at world point P; the dactyl keeps its rest direction turned by the body yaw"""
    foot = k.legs2[leg]["foot"]
    hipR, ankR = k.J[leg], k.J[foot]
    k.solve_leg(leg, f, Vector((P.x - (ankR.x - hipR.x), P.y - (ankR.y - hipR.y), P.z - ankR.z)), toe=toe)
    k._aim(foot, f, Quaternion((0, 0, 1), math.radians(yaw)) @ Quaternion((1, 0, 0), math.radians(toe)))


def plant6(k, frames, legs=None, yaw=BASE_YAW):
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in (legs or LEGS6):
            ankle_to(k, leg, f, about_spine(k, k.J[k.legs2[leg]["foot"]], yaw), yaw=yaw)


def claw(k, f, side, lift=0.0, spread=0.0, fore=0.0, wrist=0.0, pinch=0.0):
    """FK claw: lift + = the merus rises (about merus x up), spread + = swings outward (yaw), fore + = the carpus
    rises, wrist + = the palm tips up (about its out axis), pinch + = the dactyl opens"""
    s = 1 if side == "L" else -1
    S, E, W, F, a, o, out = claw_frame(side)
    dm = (E - S).normalized()
    ax_up = dm.cross(Vector((0, 0, 1))).normalized()
    cm.key_axis(k, "Arm_" + side, f, ax_up, lift, extra=Quaternion((0, 0, 1), math.radians(s * spread)))
    dfo = (W - E).normalized()
    cm.key_axis(k, "Fore_" + side, f, dfo.cross(Vector((0, 0, 1))).normalized(), fore)
    cm.key_axis(k, "Claw_" + side, f, out * s, wrist)
    cm.key_axis(k, "Pincer_" + side, f, out * s, -pinch)         # + opens (r3 re-checked: + with -pinch sweeps away)


def eyes(k, f, l=0.0, r=0.0, up=0.0):
    k.key("Eye_L", f, rot=(-up, l, 0))
    k.key("Eye_R", f, rot=(-up, r, 0))


def body(k, f, up=0.0, pitch=0.0, roll=0.0):
    """the carapace at the base yaw; up = rise (BU), pitch + = nose down, roll"""
    k.key("Spine", f, rot=(pitch, BASE_YAW, roll), loc=(0, 0, up))


def idle(k):
    """CLAW GUARD (plan; ref #7): the crusher lifts 20 deg to guard and BREATHES there (f85 CM1: +/-3 deg over one 35 f
    arc, troughs f45 / f80, peak f62; the body bobs 0.008), the eyestalks swivel one at a time with freezes between,
    the cutter taps the shell once (f70). Starts and ends in the base pose (portrait = f0)."""
    n = 120
    k.new_action("idle", n, True)
    guard = [(0, 0), (12, 0), (28, 20), (98, 20), (114, 0), (120, 0)]
    gfore = [(0, 0), (12, 0), (28, 8), (98, 8), (114, 0), (120, 0)]
    gpin = [(0, 0), (14, 0), (26, 10), (34, 4), (98, 4), (112, 0), (120, 0)]
    tap = [(0, 0), (60, 0), (66, 12), (70, -1), (74, 0), (120, 0)]
    eyl = [(0, 0), (18, 0), (24, 10), (44, 10), (50, 0), (120, 0)]
    eyr = [(0, 0), (54, 0), (60, -10), (80, -10), (86, 0), (120, 0)]
    breath = [(0, 0), (28, 0), (45, -3), (62, 3), (80, -3), (98, 0), (120, 0)]   # f85 CM1: the guard breathes
    for f in range(0, n + 1, 2):
        body(k, f, up=0.008 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n)))       # f85 CM1: bob 0.004 -> 0.008
        claw(k, f, "R", lift=curve(guard, f) + curve(breath, f), fore=curve(gfore, f), pinch=curve(gpin, f))
        claw(k, f, "L", lift=curve(tap, f), pinch=0.6 * curve(tap, f))
        eyes(k, f, l=curve(eyl, f), r=curve(eyr, f), up=2 * pk.wave(f, n, 0.1, 1))
        k.key("Mouth", f, rot=(3 * max(0.0, pk.wave(f, n, 0.3, 2)), 0, 0))
    plant6(k, range(0, n + 1))
    k.finish()
    k.meta["planted"] = LEGS6
    k.events["idle"] = {"tap": round(70 / n, 3)}


def walk(k):
    """diagonal scuttle (refs R1-R4): tripods along the travel line, body at 45 deg, claws folded low (review 2 N5)"""
    import bpy
    n, S, LIFT, duty = 30, 0.085, 0.07, 0.55
    k.new_action("walk", n, True)
    for f in range(0, n + 1, 2):
        k.key("Spine", f, rot=(0, YAW_WALK, 1.2 * pk.wave(f, n, 0.1, 2)),
              loc=(0, 0, 0.010 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        for sd in ("L", "R"):
            claw(k, f, sd, lift=-10 + 3 * pk.wave(f, n, 0.0 if sd == "L" else 0.5), fore=-4,
                 wrist=2 * pk.wave(f, n, 0.2),
                 spread=4 * pk.wave(f, n, 0.125, 2) if sd == "R" else 0.0)       # f85 9+ 4: crusher sway
        eyes(k, f, l=-6 * pk.wave(f, n, 0.22), r=-6 * pk.wave(f, n, 0.22))       # the eyes lag (plan)
        k.key("Mouth", f, rot=(0, 0, 0))
    k.bake_bezier_now()
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        for leg, off in WALK_OFF:
            A0 = about_spine(k, k.J[k.legs2[leg]["foot"]], YAW_WALK)
            t = ((f / n) + off) % 1.0
            if t < duty:
                y, z = -S + 2 * S * (t / duty), 0.0
            else:
                u = (t - duty) / (1 - duty)
                y, z = S - 2 * S * (0.5 - 0.5 * math.cos(math.pi * u)), LIFT * math.sin(math.pi * u)
            ankle_to(k, leg, f, A0 + Vector((0, y, z)), yaw=YAW_WALK)
    k.finish()
    k.meta["walk_cycle"] = n
    k.meta["legs"] = list(WALK_OFF)
    k.meta["duty"] = duty
    k.events["walk"] = {"sand1": round(13.8 / n, 3), "sand2": round(28.8 / n, 3)}   # tripod B / A touch-downs
    return 2 * S / duty


def roar(k):
    """CLACK THREAT (plan; refs #6 + #5): a short crouch, the body rises 0.05 H and both claws lift forward 30 deg;
    three clacks (cocked open 2 f -> snap shut 2 f -> hard stop); the mandibles open; lower and settle."""
    n = 60
    k.new_action("roar", n, False)
    rise = [(0, 0), (4, -0.012), (14, 0.052), (40, 0.052), (52, 0.0), (60, 0.0)]
    lift = [(0, 0), (4, -4), (14, 30), (40, 30), (52, 0), (60, 0)]            # review 3 N3: 25 -> 30
    spread = [(0, 0), (14, 14), (40, 14), (52, 0), (60, 0)]
    fore = [(0, 0), (14, 12), (40, 12), (52, 0), (60, 0)]
    pin = [(0, 0), (12, 14), (16, 14), (20, 30), (22, 0), (24, 8), (28, 30), (30, 0), (32, 8), (36, 30), (38, 0),
           (40, 4), (52, 0), (60, 0)]
    mouth = [(0, 0), (14, 0), (20, 14), (44, 14), (52, 0), (60, 0)]
    for f in range(0, n + 1, 2):
        u = curve(rise, f)
        body(k, f, up=u, pitch=-4 * u / 0.052 if u > 0 else 0.0)
        for sd in ("L", "R"):
            claw(k, f, sd, lift=curve(lift, f), spread=curve(spread, f), fore=curve(fore, f), pinch=curve(pin, f))
        eyes(k, f, up=8 * max(0.0, u) / 0.052)
        k.key("Mouth", f, rot=(curve(mouth, f), 0, 0))
    plant6(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["roar"] = {"clack1": round(22 / n, 3), "clack2": round(30 / n, 3), "clack3": round(38 / n, 3),
                        "bubble": round(24 / n, 3)}


def act_semaphore(k):
    """THE FIDDLER WAVE (plan; refs F1-F3 + the site refs S1 / S2 in ANIM_REFS.md): stand tall, the crusher unfolds up and
    waves three slow display arcs. Each top is HELD 8 f (f26-34 / f49-57 / f72-80, hold centres f30 / f53 / f76), the
    down-stroke takes 5 f (S2 H3: the drop is quick) and the up-sweep 10 f (H1, F3). Then the claw points out and holds
    while the cutter taps twice (f90 / f96), swings in, then folds down (f96-110); exact rest f110-120. Legs planted
    every frame."""
    n = 120
    k.new_action("act_semaphore", n, False)
    up = [(0, 0), (18, 1), (98, 1), (110, 0), (120, 0)]
    # the wave: top = the claw raised high (F1), held 8 f; trough = swung down and forward in front (F2, f39 / f62):
    # merus 16 <-> 40, spread 6 <-> 34, carpus -12 <-> 10, palm -40 <-> -6 deg; 10 f up, 5 f down (review 4 NICE 1-2)
    HOLD, DOWN, UP = 8, 5, 10
    TOPS = (26, 26 + HOLD + DOWN + UP, 26 + 2 * (HOLD + DOWN + UP))         # 26, 49, 72
    TROUGHS = tuple(t0 + HOLD + DOWN for t0 in TOPS[:2])                    # 39, 62

    def wave_keys(top, low, first, end):
        ks = [(0, 0), (18, first)]
        for i, t0 in enumerate(TOPS):
            ks += [(t0, top), (t0 + HOLD, top)]
            if i < len(TROUGHS):
                ks.append((TROUGHS[i], low))
        return ks + end

    lift_r = wave_keys(40, 16, 30, [(86, 38), (96, 38), (103, 30), (110, 0), (120, 0)])
    spread_r = wave_keys(34, 6, 30, [(86, 44), (96, 44), (103, 10), (110, 0), (120, 0)])  # in first, then down
    fore_r = wave_keys(10, -12, 0, [(86, 0), (120, 0)])
    wrist_r = wave_keys(-6, -40, -10, [(86, 0), (120, 0)])                     # the palm swings down at the trough
    pin_r = [(0, 0), (18, 10), (80, 10), (86, 2), (106, 0), (120, 0)]
    tap_l = [(0, 0), (18, -6), (86, -6), (88, 6), (90, -6), (94, 6), (96, -6), (102, -6), (110, 0), (120, 0)]
    # f85 CM2: the wave's top/trough rhythm shifted 2 f later (tops held f28-36 / f51-59 / f74-82, troughs f41 / f64)
    track = [(0, 0), (20, 0.6)]
    for i, t0 in enumerate(TOPS):
        track += [(t0 + 2, 1.0), (t0 + HOLD + 2, 1.0)]
        if i < len(TROUGHS):
            track.append((TROUGHS[i] + 2, 0.0))
    track += [(88, 0.6), (100, 0.3), (110, 0), (120, 0)]
    for f in range(0, n + 1):
        u = curve(up, f)
        tr = curve(track, f)
        body(k, f, up=0.10 * u, pitch=-5 * u, roll=-2 * u - 2 * (2 * tr - 1) * u)   # f85 CM2: +/-2 deg with each beat
        claw(k, f, "R", lift=curve(lift_r, f), spread=curve(spread_r, f), fore=curve(fore_r, f),
             wrist=curve(wrist_r, f), pinch=curve(pin_r, f))
        claw(k, f, "L", lift=curve(tap_l, f))
        eyes(k, f, up=6 * u + 4 * tr * u, l=-12 * tr * u, r=4 * u + 12 * tr * u)    # f85 CM2: both eyes track the crusher (the eye bones are mirrored: L -, R +)
        k.key("Mouth", f, rot=(0, 0, 0))
    plant6(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["act_semaphore"] = {"wave1": round(30 / n, 3), "wave2": round(53 / n, 3), "wave3": round(76 / n, 3),
                                 "tap1": round(90 / n, 3), "tap2": round(96 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    act_semaphore(k)
    return stride
