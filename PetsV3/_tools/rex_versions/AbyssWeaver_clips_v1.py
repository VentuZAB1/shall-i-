# Abyss Weaver (Void egg, NEW 1.5 % SECRET pet, 2026-10-14) - FIERCE style "THE BLOOD-WIDOW QUEEN OF THE VOID" (plan
# review brief _review/AbyssWeaver_plan_review.md, palette BLOOD ORCHID): a plum-black armoured spider on eight arched,
# red-kneed legs; a spiked gold crown over a cluster of 8 orchid eyes; two ivory dagger fangs; HERO = a long gold-set
# VOID RIFT split open along the armoured abdomen (its front half faces the portrait camera, its rear half the game
# camera). Studded plum armour plates over blood-wine seams, a pale silk belly band, orchid-tipped knee thorns. No glow
# meshes: the rift / eye light are Studio VFX on the anchors. Proportions follow the reviewer's tested mock.
import math
from mathutils import Vector, Matrix, Euler

DISPLAY = "Abyss Weaver"
MOTION = "Walk"
RIG = "quad"                 # the label the Studio side already stores (Mantis precedent)
HEIGHT = 8.0                 # studs to the pair-2 knee-thorn tips (H_MODEL)

# ---- BLOOD ORCHID (Blender values; in game ~x0.6)
ARMOR = (76, 58, 88)         # plum-black: carapace, turret, chelicerae, femurs, abdomen plates, spine/thorn sockets
ARMOR_D = (58, 44, 70)       # tibiae, metatarsi, tarsi, knuckles, clypeus, brows, carapace grooves
VELVET = (148, 30, 72)       # blood-wine: abdomen hull (plate seams), carapace rim, coxae, knee bands, femur strips
SILK = (214, 204, 224)       # sternum, abdomen belly band, spinneret tips
DEEP = (118, 24, 156)        # rift field, small-eye rims, gem frame
ORCHID = (212, 72, 255)      # eye lenses, rift body, thorn + spine middles, crown gem
HOT = (246, 222, 255)        # rift seam, eye hot spots, thorn points
GOLD = (255, 196, 50)        # crown + rift lips + rift settings ONLY
GOLD_D = (214, 150, 30)      # circlet inner faces, rift lip inner edges
IVORY = (240, 234, 214)      # fangs
BLACK = (14, 14, 22)         # claws, fang tips, eye sockets + pupils, tibial spines, palp claws

H_MODEL = 1.10
ANCH = {}

# ---- legs (brief 4.9): pair: azimuth (deg from +x toward +y), hip (x, y), knee (r, z), ankle (r, z), toe (r, z)
HIPZ = 0.37
LEGP = {1: (-54, (0.16, -0.45), (0.34, 0.92), (0.76, 0.10), (0.83, 0.035)),
        2: (-20, (0.21, -0.32), (0.36, 0.97), (0.80, 0.10), (0.87, 0.035)),
        3: (16, (0.22, -0.18), (0.36, 0.95), (0.78, 0.10), (0.85, 0.035)),
        4: (44, (0.18, -0.05), (0.35, 0.90), (0.82, 0.10), (0.89, 0.035))}
POLE = {1: (0.19, -0.27, 0.94), 2: (0.31, -0.11, 0.95), 3: (0.32, 0.09, 0.94), 4: (0.24, 0.22, 0.94)}
LEGS8 = ["Leg%d_%s" % (i, s) for s in "LR" for i in (1, 2, 3, 4)]

# ---- abdomen frame (brief 4.5): origin A0, axis AX tilted 10 deg rear-up, dorsal UP
A0 = Vector((0, 0.14, 0.50))
AX = Vector((0, math.cos(math.radians(10)), math.sin(math.radians(10))))
UP = Vector((0, -AX.z, AX.y))
ABD = [(0.00, 0.10, 0.10), (0.08, 0.21, 0.19), (0.22, 0.35, 0.28), (0.40, 0.39, 0.31), (0.60, 0.36, 0.29),
       (0.80, 0.26, 0.22), (0.96, 0.14, 0.13), (1.06, 0.05, 0.05)]
NA = 2.3
CAR = [(-0.58, 0.48, 0.150, 0.080), (-0.48, 0.47, 0.220, 0.110), (-0.34, 0.46, 0.260, 0.125),
       (-0.18, 0.45, 0.265, 0.120), (-0.04, 0.44, 0.220, 0.100), (0.04, 0.44, 0.140, 0.070)]   # y, zc, hw, hh
RIFT_U = (0.19, 0.76)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def leg_pts(i):
    """rest hip, knee, ankle, toe of the LEFT leg i"""
    a, (hx, hy), kn, an, to = LEGP[i]
    d = Vector((math.cos(math.radians(a)), math.sin(math.radians(a)), 0))
    base = Vector((hx, hy, 0))
    return (Vector((hx, hy, HIPZ)), base + d * kn[0] + Vector((0, 0, kn[1])), base + d * an[0] + Vector((0, 0, an[1])),
            base + d * to[0] + Vector((0, 0, to[1])))


def abd_ring(u, hw, hh, a0=0.0, a1=2 * math.pi, seg=24, n=NA, off=0.0):
    out = []
    closed = abs((a1 - a0) - 2 * math.pi) < 1e-6
    c0 = A0 + AX * u
    for i in range(seg if closed else seg + 1):
        a = a0 + (a1 - a0) * i / seg
        c, s = math.cos(a), math.sin(a)
        x = (hw + off) * math.copysign(abs(c) ** (2.0 / n), c)
        w = (hh + off) * math.copysign(abs(s) ** (2.0 / n), s)
        out.append(c0 + Vector((x, 0, 0)) + UP * w)
    return out


def abd_interp(u):
    for (u0, w0, h0), (u1, w1, h1) in zip(ABD, ABD[1:]):
        if u <= u1:
            t = (u - u0) / (u1 - u0)
            return w0 + (w1 - w0) * t, h0 + (h1 - h0) * t
    return ABD[-1][1], ABD[-1][2]


def abd_top(u, side=0.0, out=0.0):
    """hull surface point at axial u, lateral fraction side (-1..1 of the half-width) on the dorsal half, lifted out"""
    hw, hh = abd_interp(u)
    t = min(0.999, abs(side))
    w = hh * (1 - t ** NA) ** (1.0 / NA)
    return A0 + AX * u + Vector((side * hw, 0, 0)) + UP * (w + out)


def abd_nrm(u, side=0.0):
    e = 0.01
    pu = abd_top(min(u + e, 0.96), side) - abd_top(max(u - e, 0.0), side)
    ps = abd_top(u, side + e) - abd_top(u, side - e)
    n = ps.cross(pu).normalized()
    return n if n.z > 0 else -n


def surf_hit(B, blks, origin, direction):
    """first hit of a ray on the given parts (blocks or tubes) -> (point, outward normal) (Mantis recipe)"""
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


def face_R(nn):
    """frame whose local -y is the outward normal nn and local z points as close to world up as possible"""
    y = -Vector(nn).normalized()
    z = Vector((0, 0, 1)) - y * y.z
    if z.length < 1e-3:
        z = Vector((0, 1, 0)) - y * y.y
    z.normalize()
    return Matrix((y.cross(z), y, z)).transposed()


def main_eye(B, c, s, bone="Head", yaw=18.0, tilt=20.0, sc=0.9):
    """ThunderRex fierce_eye recolored: black socket (inner corner down) -> a tall orchid slit lens with a black
    vertical pupil (70 %) at the inner front, a thin ARMOR_D V-brow lidding ~30 % from the portrait camera. No HOT spot
    (it read as a cute glint once the eye shows; the EyeGlow VFX carries the burn - review 1 FIX 1)"""
    R = Euler((0, math.radians(-s * tilt), math.radians(s * yaw)), "XYZ").to_matrix()
    n = R @ Vector((0, -1, 0))
    kw = dict(R=R, studs=[], role="detail")
    B.add(c, (0.052 * sc, 0.008, 0.028 * sc), BLACK, bone, bevel=0.004, **kw)                  # socket
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0165 * sc), ORCHID, bone, bevel=0.003, **kw)     # lens (review 1 FIX 1)
    B.add(c + n * 0.011 + R @ Vector((-s * 0.004, 0, 0)), (0.006 * sc, 0.004, 0.0115 * sc), BLACK, bone,
          bevel=0.002, **kw)                                                                  # slit pupil, 70 %
    Rb = Euler((0, math.radians(-s * 22), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.040 * sc)) + n * 0.010, (0.074 * sc, 0.022, 0.026 * sc), ARMOR_D, bone, R=Rb,
          role="detail", bevel=0.010)                                                         # thin V-brow, no glint


def gem_inlay(B, c, n, size, bone):
    """flush 45 deg diamond: DEEP frame -> ORCHID -> HOT glint (Mantis recipe)"""
    n = Vector(n).normalized()
    x = Vector((0, 0, 1)).cross(n).normalized()
    z = n.cross(x).normalized()
    Rr = Matrix((x, n, z)).transposed() @ Matrix.Rotation(math.radians(45), 3, "Y")
    kw = dict(R=Rr, studs=[], nostud=True, role="detail")
    B.add(c, (size, 0.008, size), DEEP, bone, bevel=0.004, **kw)
    B.add(c + n * 0.006, (size * 0.72, 0.007, size * 0.72), ORCHID, bone, bevel=0.003, **kw)
    B.add(c + n * 0.011 + (x + z) * size * 0.25, (size * 0.16, 0.004, size * 0.16), HOT, bone, bevel=0.002, **kw)


def spine3(B, base, d, L, w, bone):
    """ARMOR socket (62 % of L) -> ORCHID middle from 50 % -> HOT point (house crystal step)"""
    d = Vector(d).normalized()
    B.spike(base, d, L * 0.62, w, ARMOR, bone, top=(0.55, 0.55))
    B.spike(base + d * L * 0.5, d, L * 0.5, 0.026, ORCHID, bone, top=(0.25, 0.25), nostud=True)
    B.spike(base + d * L * 0.92, d, L * 0.18, 0.012, HOT, bone, nostud=True)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=515, tier=3, plates=False, th=0.26)
    kw = dict(studs=[], nostud=True, role="limb")
    # ================= cephalothorax (Spine): armour tube, wine rim band, silk sternum, fovea + radial grooves
    car = B.tube([bk.superellipse(hw, hh, zc, y, n=2.4, seg=20) for y, zc, hw, hh in CAR], ARMOR, "Spine")
    B.tube([bk.superellipse(hw + 0.012, hh * 0.75, zc - 0.035, y, n=2.4, seg=20) for y, zc, hw, hh in CAR[1:5]],
           VELVET, "Spine")
    B.add((0, -0.24, 0.335), (0.17, 0.22, 0.03), SILK, "Spine", rnd=0.4)                          # sternum
    fp, fn = surf_hit(B, [car], (0, -0.24, 1.0), (0, 0, -1))
    B.add(fp + fn * 0.002, (0.035, 0.008, 0.05), ARMOR_D, "Spine", R=face_R(fn), studs=[], role="detail",
          bevel=0.004)                                                                          # fovea (flush)
    for s in (1, -1):
        for ang in (-40, 0, 40):
            a = math.radians(ang)
            dv = Vector((s * math.cos(a), math.sin(a), 0))
            p0, n0 = surf_hit(B, [car], fp + dv * 0.07 + Vector((0, 0, 0.3)), (0, 0, -1))
            p1, n1 = surf_hit(B, [car], fp + dv * 0.19 + Vector((0, 0, 0.3)), (0, 0, -1))
            B.bar(p0 + n0 * 0.002, p1 + n1 * 0.002, (n0 + n1).normalized(), 0.03, 0.006, ARMOR_D, "Spine", studs=[],
                  role="detail", bevel=0.003)                                                   # radial groove
    # ================= ocular turret (Head) + clypeus + 8 eyes
    tur = B.add((0, -0.50, 0.605), (0.12, 0.095, 0.065), ARMOR, "Head", top=(0.80, 0.74), rnd=0.35)
    cly = B.add((0, -0.60, 0.485), (0.12, 0.03, 0.06), ARMOR_D, "Head", bot=(0.8, 1.0), rnd=0.3)
    for s in (1, -1):
        p, nn = surf_hit(B, [tur], (s * 0.065, -0.9, 0.605), (0, 1, 0))
        main_eye(B, p + nn * 0.003, s)                                                          # E1 main pair
        for x, z in ((0.030, 0.548), (0.098, 0.557)):                                           # E2 front row (frown)
            p, nn = surf_hit(B, [tur, cly], (s * x, -0.9, z), (0, 1, 0))
            R = face_R(nn)
            B.add(p + nn * 0.004, (0.020, 0.010, 0.018), DEEP, "Head", R=R, studs=[], role="detail", bevel=0.006)
            B.add(p + nn * 0.012, (0.013, 0.006, 0.012), ORCHID, "Head", R=R, studs=[], role="detail", bevel=0.004)
        p, nn = surf_hit(B, [tur], (s * 0.4, -0.48, 0.645), (-s, 0, 0))                         # E3 top-side pair
        R = face_R(nn)
        B.add(p + nn * 0.004, (0.026, 0.012, 0.026), DEEP, "Head", R=R, studs=[], role="detail", bevel=0.006)
        B.add(p + nn * 0.011, (0.018, 0.008, 0.018), ORCHID, "Head", R=R, studs=[], role="detail", bevel=0.004)
        B.add(p + nn * 0.010 + R @ Vector((0, 0, 0.026)), (0.03, 0.012, 0.008), ARMOR_D, "Head", R=R, studs=[],
              role="detail", bevel=0.004)                                                     # its small lid
    ANCH["EyeGlow"] = (0, -0.63, 0.60)
    # ================= the CROWN (Head, all GOLD smooth): closed circlet + 8 straight points rising to the back
    zb = 0.675
    B.seg((-0.10, -0.585, zb), (0.10, -0.585, zb), 0.032, 0.026, GOLD, "Head", side=(0, 0, 1), ext=0.02, ext1=0.02, **kw)
    B.seg((-0.10, -0.415, zb), (0.10, -0.415, zb), 0.032, 0.026, GOLD, "Head", side=(0, 0, 1), ext=0.02, ext1=0.02, **kw)
    B.seg((-0.085, -0.556, zb), (0.085, -0.556, zb), 0.026, 0.006, GOLD_D, "Head", side=(0, 0, 1), **kw)
    B.seg((-0.085, -0.444, zb), (0.085, -0.444, zb), 0.026, 0.006, GOLD_D, "Head", side=(0, 0, 1), **kw)
    for s in (1, -1):
        B.seg((s * 0.115, -0.59, zb), (s * 0.115, -0.41, zb), 0.026, 0.032, GOLD, "Head", **kw)
        B.seg((s * 0.086, -0.555, zb), (s * 0.086, -0.445, zb), 0.006, 0.026, GOLD_D, "Head", **kw)
        for x, y, h in ((0.04, -0.585, 0.10), (0.105, -0.58, 0.13), (0.105, -0.42, 0.17), (0.04, -0.415, 0.20)):
            d = Vector((s * 0.22, 0.22 if y > -0.5 else 0.10, 1.0)).normalized()
            B.spike(Vector((s * x, y, zb + 0.02)), d, h, 0.034, GOLD, "Head", top=(0.12, 0.12), **kw)
    gem_inlay(B, Vector((0, -0.613, 0.675)), (0, -1, 0), 0.028, "Head")
    ANCH["Crown"] = (0, -0.50, 0.90)
    # ================= chelicerae (VELVET boss), ivory dagger fangs (black tips), palps outside them
    for s, side in ((1, "L"), (-1, "R")):
        r0, r1 = Vector((s * 0.062, -0.60, 0.45)), Vector((s * 0.058, -0.69, 0.28))
        B.seg(r0, r1, 0.050, 0.060, ARMOR, "Chel_" + side, ext=0.03, top=(0.78, 0.72))
        B.seg(r0 + Vector((0, -0.055, -0.02)), r1 + Vector((0, -0.035, 0.02)), 0.036, 0.012, VELVET, "Chel_" + side,
              studs=[], role="detail", bevel=0.006)
        f0 = Vector((s * 0.058, -0.70, 0.28))
        d1 = Vector((-s * 0.12, -0.15, -1)).normalized()
        B.spike(f0, d1, 0.10, 0.028, IVORY, "Fang_" + side, top=(0.62, 0.62), nostud=True)
        p1 = f0 + d1 * 0.095
        d2 = Vector((-s * 0.25, 0.45, -0.85)).normalized()
        B.spike(p1, d2, 0.06, 0.019, IVORY, "Fang_" + side, top=(0.45, 0.45), nostud=True)
        B.spike(p1 + d2 * 0.055, d2, 0.03, 0.012, BLACK, "Fang_" + side, nostud=True)
        ANCH["FangTip_" + side] = tuple(p1 + d2 * 0.085)
        pp0, pp1, pp2 = Vector((s * 0.15, -0.55, 0.39)), Vector((s * 0.20, -0.72, 0.28)), Vector((s * 0.19, -0.81, 0.12))
        B.seg(pp0, pp1, 0.028, 0.030, ARMOR, "Palp_" + side, ext=0.02, ext1=0.015)
        B.add(pp1, (0.032, 0.032, 0.032), VELVET, "Palp_" + side, rnd=0.4)
        B.seg(pp1, pp2, 0.024, 0.026, ARMOR, "Palp_" + side, ext=0.01)
        B.spike(pp2, (0, -0.4, -1), 0.04, 0.012, BLACK, "Palp_" + side)
    # ================= pedicel + abdomen (Abd): wine hull, armour plates with wine seams, silk belly band, spines
    B.seg((0, -0.02, 0.45), (0, 0.20, 0.505), 0.075, 0.065, VELVET, "Pedicel", ext=0.02, ext1=0.02)
    B.tube([abd_ring(u, hw, hh) for u, hw, hh in ABD], VELVET, "Abd")

    def shell(u0, u1, a0, a1, color, off=0.022, thick=0.03, seg=10, nr=4):
        rings = []
        for i in range(nr):
            u = u0 + (u1 - u0) * i / (nr - 1.0)
            hw, hh = abd_interp(u)
            rings.append((abd_ring(u, hw, hh, math.radians(a0), math.radians(a1), seg=seg, off=off),
                          abd_ring(u, hw, hh, math.radians(a0), math.radians(a1), seg=seg, off=off - thick)))
        return B.tube(rings, color, "Abd", closed=False)
    shell(0.05, 0.16, 10, 170, ARMOR)                                            # P1 front (full width)
    for u0, u1 in ((0.20, 0.40), (0.44, 0.64)):                                  # P2, P3 flank the rift
        shell(u0, u1, 14, 78, ARMOR)
        shell(u0, u1, 102, 166, ARMOR)
    shell(0.68, 0.99, -15, 195, ARMOR, seg=14)                                   # P4 rear cap (hides the band end)
    shell(0.14, 0.64, 205, 335, SILK, off=0.014, thick=0.02, seg=12, nr=6)       # belly band (6 rings: no poke-through)
    for s in (1, -1):
        spine3(B, abd_top(0.20, s * 0.70, -0.01), (s * 0.35, 0.25, 0.90), 0.17, 0.05, "Abd")   # shoulder horns
        spine3(B, abd_top(0.60, s * 0.95, -0.01), (s * 0.90, 0.35, 0.25), 0.12, 0.042, "Abd")  # rear-side spines
    # ================= HERO: the VOID RIFT (DEEP field -> ORCHID body -> HOT seam) in gold lips with GOLD_D inner edges
    U0, U1 = RIFT_U
    N = 14                                       # the brief's minimum (fewer pieces read as candy stripes)

    def wt(t):
        return 0.15 * math.sin(math.pi * t) ** 0.8
    # review 1 FIX 2: a torn orchid body + a meandering HOT crack with 2 side fractures (never a pupil slit, never a
    # regular zig-zag bolt); the closed gold lip frame stays
    JAG = [0.55, 0.62, 0.72, 0.58, 0.66, 0.80, 0.62, 0.70, 0.82, 0.64, 0.56, 0.70, 0.60, 0.55]   # torn orchid edge
    ZZ = [0.0, 0.20, 0.42, 0.16, -0.28, -0.48, -0.20, 0.18, 0.46, 0.30, -0.06, -0.36, -0.22, 0.06, 0.0]  # crack path
    for i in range(N):
        t0, t1 = i / N, (i + 1) / N
        ua, ub = U0 + (U1 - U0) * t0, U0 + (U1 - U0) * t1
        nm = abd_nrm((ua + ub) / 2, 0)
        B.bar(abd_top(ua, 0, 0.010), abd_top(ub, 0, 0.010), nm, 2 * max(0.010, wt((t0 + t1) / 2)), 0.006, DEEP,
              "Abd", studs=[], nostud=True, role="detail", bevel=0.003)                      # void field
        B.bar(abd_top(ua, 0, 0.016), abd_top(ub, 0, 0.016), nm, 2 * max(0.010, JAG[i] * wt((t0 + t1) / 2)), 0.006,
              ORCHID, "Abd", studs=[], nostud=True, role="detail", bevel=0.003)              # glow body, torn edge
    pts = []
    for i in range(N + 1):                                    # HOT: a meandering crack (S + jitter)
        t = i / N
        u = U0 + (U1 - U0) * t
        hw, _ = abd_interp(u)
        pts.append((abd_top(u, ZZ[i] * 0.45 * wt(t) / hw, 0.021), u))
    for (a, ua), (b, ub) in zip(pts, pts[1:]):
        d = (b - a).normalized()
        B.bar(a - d * 0.010, b + d * 0.010, abd_nrm((ua + ub) / 2, 0), 0.026, 0.004, HOT, "Abd", studs=[],
              nostud=True, role="detail", bevel=0.002)
    for i, side, du in ((5, -1, 0.05), (9, 1, -0.05)):       # 2 short side fractures (an eye never branches)
        a, ua = pts[i]
        ub = ua + du
        hw, _ = abd_interp(ub)
        b = abd_top(ub, (ZZ[i] * 0.45 + side * 0.42) * wt((ub - U0) / (U1 - U0)) / hw, 0.021)
        B.bar(a, b, abd_nrm((ua + ub) / 2, 0), 0.016, 0.004, HOT, "Abd", studs=[], nostud=True, role="detail",
              bevel=0.002)
    for s in (1, -1):
        lip, inner = [], []
        for i in range(N + 1):
            t = i / N
            u = U0 + (U1 - U0) * t
            hw, _ = abd_interp(u)
            lip.append((abd_top(u, s * (wt(t) + 0.035) / hw, 0.020), u))
            inner.append(abd_top(u, s * (wt(t) - 0.004) / hw, 0.022))
        for (a, ua), (b, ub) in zip(lip, lip[1:]):
            B.seg(a, b, 0.045, 0.028, GOLD, "Abd", side=abd_nrm((ua + ub) / 2, 0), ext=0.01, ext1=0.01, **kw)
        for a, b in zip(inner[::2], inner[2::2]):
            B.seg(a, b, 0.008, 0.030, GOLD_D, "Abd", side=Vector((1, 0, 0)), ext=0.008, ext1=0.008, **kw)
    for ue, dirv in ((U0 - 0.02, -1), (U1 + 0.02, 1)):                            # 3-prong claw settings at the ends
        c = abd_top(ue, 0, 0.02)
        nm = abd_nrm(ue, 0)
        tg = (abd_top(ue + 0.01) - abd_top(ue - 0.01)).normalized() * dirv
        for sx, L in ((-1, 0.065), (0, 0.09), (1, 0.065)):
            d = Matrix.Rotation(math.radians(35 * sx), 3, nm) @ tg
            d = (d * math.cos(math.radians(20)) + nm * math.sin(math.radians(20))).normalized()
            B.spike(c, d, L, 0.03, GOLD, "Abd", top=(0.15, 0.15), **kw)
    ANCH["Rift"] = tuple(abd_top(0.47, 0, 0.02))
    # ================= spinnerets (Spinner): 2 big + 2 small, silk tips
    for s in (1, -1):
        b = abd_top(1.03, 0, -0.03) + Vector((s * 0.035, 0, -0.03))
        d = Vector((s * 0.25, 0.8, -0.55)).normalized()
        B.spike(b, d, 0.10, 0.032, ARMOR, "Spinner")
        B.spike(b + d * 0.07, d, 0.045, 0.020, SILK, "Spinner", nostud=True)
        b2 = b + Vector((-s * 0.02, -0.01, -0.03))
        d2 = Vector((s * 0.12, 0.85, -0.5)).normalized()
        B.spike(b2, d2, 0.06, 0.022, ARMOR, "Spinner")
        B.spike(b2 + d2 * 0.042, d2, 0.03, 0.014, SILK, "Spinner", nostud=True)
    ANCH["Spinneret"] = (0, 1.27, 0.62)
    # ================= 8 legs: wine coxa, armour femur (wine under-strip), knuckles, BLOOD knee band, bowed armour_d
    # tibia + metatarsus, tarsus, black claw; black tibial spines; one orchid-tipped thorn per knee
    for s, side in ((1, "L"), (-1, "R")):
        for i in (1, 2, 3, 4):
            H, K, A, T = (X(p, s) for p in leg_pts(i))
            leg, shin, foot = "Leg%d_%s" % (i, side), "Shin%d_%s" % (i, side), "Foot%d_%s" % (i, side)
            out = Vector((K.x - H.x, K.y - H.y, 0)).normalized()
            B.add(H + Vector((0, 0, -0.01)), (0.066, 0.066, 0.05), VELVET, leg, rnd=0.45)            # coxa
            B.seg(H, K, 0.060, 0.066, ARMOR, leg, ext=0.05, ext1=0.02, top=(0.78, 0.78))              # femur
            fd = (K - H).normalized()
            dn = (Vector((0, 0, -1)) + fd * fd.z).normalized()
            B.seg(H + fd * 0.08 + dn * 0.05, K - fd * 0.06 + dn * 0.04, 0.046, 0.022, VELVET, leg, studs=[],
                  role="limb")                                                                       # under-strip
            B.add(K, (0.064, 0.064, 0.064), ARMOR_D, shin, rnd=0.42)                                  # patella
            M = K.lerp(A, 0.50) + out * 0.06
            km = (M - K).normalized()
            B.seg(K + km * 0.045, K + km * 0.13, 0.054, 0.056, VELVET, shin, role="limb")             # knee band
            B.seg(K, M, 0.050, 0.052, ARMOR_D, shin, ext=0.01, ext1=0.01, top=(0.85, 0.85))           # tibia
            B.add(M, (0.046, 0.046, 0.046), ARMOR_D, shin, rnd=0.42)                                  # T/M knuckle
            B.seg(M, A, 0.040, 0.042, ARMOR_D, shin, ext=0.01, ext1=0.01, top=(0.82, 0.82))           # metatarsus
            for t in (0.35, 0.70):
                B.spike(K.lerp(M, t) + out * 0.03, out * 0.6 + Vector((0, 0, -0.5)) + km * 0.4, 0.045, 0.013,
                        BLACK, shin)                                                                 # tibial spines
            B.seg(A, T, 0.030, 0.030, ARMOR_D, foot, ext=0.015)                                       # tarsus
            cd = ((T - A).normalized() + Vector((0, 0, -0.6))).normalized()
            B.spike(T, cd, 0.045, 0.016, BLACK, foot)                                                # claw
            if i == 4:
                ANCH["Silk_" + side] = tuple(T + cd * 0.045)
            dth = (Vector((0, 0.35, 1)) + out * 0.25).normalized()
            kb = K + dth * 0.045
            B.spike(kb, dth, 0.05, 0.028, ARMOR, shin, top=(0.6, 0.6))                                # knee thorn
            B.spike(kb + dth * 0.03, dth, 0.05, 0.022, ORCHID, shin, top=(0.4, 0.4), nostud=True)
            B.spike(kb + dth * 0.07, dth, 0.022, 0.010, HOT, shin, nostud=True)
    B.build()
    mn, mx = k.bounds()
    pitch = 0.2243 * mx.z / HEIGHT
    bk.stud_skin(k, pitch)
    # tris per group (brief 4.11)
    grp = {}
    for o in k.coll.objects:
        if o.type != "MESH" or not o.name.startswith("P_"):
            continue
        g = o.name[2:].split(".")[0]
        key = ("legs" if g[:3] in ("Leg", "Shi", "Foo") else "abdomen" if g in ("Abd", "Pedicel", "Spinner")
               else "face" if g[:4] in ("Chel", "Fang", "Palp") else "head" if g == "Head" else "ceph")
        grp[key] = grp.get(key, 0) + sum(len(pl.vertices) - 2 for pl in o.data.polygons)
    return {"TH": round(B.th, 3), "pitch": round(pitch, 4), "H": round(mx.z, 3), "lowest": round(mn.z, 3),
            "bounds": [[round(v, 3) for v in mn], [round(v, 3) for v in mx]], "tris_by_group": grp}


# ------------------------------------------------------------------ rig (brief 5.1-5.3)
def rig(k):
    k.joint("Spine", (0, -0.22, 0.44), "Root", tail=(0, -0.30, 0))
    k.joint("Head", (0, -0.47, 0.50), "Spine", tail=(0, -0.10, 0.10))
    k.joint("Pedicel", (0, 0.0, 0.47), "Spine", tail=(0, 0.12, 0.03))
    k.joint("Abd", tuple(A0), "Pedicel", tail=tuple(AX * 0.9))
    k.joint("Spinner", (0, 1.13, 0.66), "Abd", tail=(0, 0.10, -0.06))
    k.joint("Crown", ANCH.get("Crown", (0, -0.50, 0.90)), "Head", tail=(0, 0, 0.1))
    k.joint("EyeGlow", ANCH.get("EyeGlow", (0, -0.63, 0.60)), "Head", tail=(0, -0.1, 0))
    k.joint("Rift", ANCH.get("Rift", (0, 0.55, 0.90)), "Abd", tail=tuple(abd_nrm(0.47, 0) * 0.1))
    k.joint("Spinneret", ANCH.get("Spinneret", (0, 1.27, 0.62)), "Spinner", tail=(0, 0.1, -0.03))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Chel_" + side, (s * 0.062, -0.60, 0.45), "Head", tail=(0, -0.09, -0.17))
        k.joint("Fang_" + side, (s * 0.058, -0.70, 0.28), "Chel_" + side, tail=(-s * 0.012, -0.015, -0.10))
        k.joint("FangTip_" + side, ANCH.get("FangTip_" + side, (s * 0.025, -0.73, 0.11)), "Fang_" + side,
                tail=(0, -0.02, -0.05))
        k.joint("Palp_" + side, (s * 0.15, -0.55, 0.39), "Spine", tail=(s * 0.05, -0.17, -0.11))
        for i in (1, 2, 3, 4):
            H, K, A, T = (X(p, s) for p in leg_pts(i))
            k.joint("Leg%d_%s" % (i, side), tuple(H), "Spine")
            k.joint("Shin%d_%s" % (i, side), tuple(K), "Leg%d_%s" % (i, side))
            k.joint("Foot%d_%s" % (i, side), tuple(A), "Shin%d_%s" % (i, side), tail=tuple(T - A))
            p = POLE[i]
            k.add_leg2("Leg%d_%s" % (i, side), "Shin%d_%s" % (i, side), "Foot%d_%s" % (i, side),
                       knee=(s * p[0], p[1], p[2]))
        k.joint("Silk_" + side, ANCH.get("Silk_" + side, tuple(X(leg_pts(4)[3], s))), "Foot4_" + side,
                tail=(s * 0.05, 0.05, 0))


def check_pairs():
    P = []
    for s in ("L", "R"):
        for a, b in ((1, 2), (2, 3), (3, 4)):                         # same-side neighbours: all 9 combinations
            for x in ("Leg", "Shin", "Foot"):
                for y in ("Leg", "Shin", "Foot"):
                    P.append(("%s%d_%s" % (x, a, s), "%s%d_%s" % (y, b, s)))
        P += [("Leg1_" + s, "Head"), ("Shin1_" + s, "Head"), ("Leg2_" + s, "Head"), ("Shin1_" + s, "Chel_" + s),
              ("Shin1_" + s, "Palp_" + s), ("Leg1_" + s, "Palp_" + s), ("Foot1_" + s, "Palp_" + s)]     # roar raise
        P += [("Fang_" + s, "Palp_" + s), ("Chel_" + s, "Palp_" + s), ("Fang_" + s, "Spine")]           # face
        P += [("Leg4_" + s, "Abd"), ("Shin4_" + s, "Abd"), ("Foot4_" + s, "Abd"), ("Leg3_" + s, "Abd"),
              ("Shin3_" + s, "Abd"), ("Spinner", "Shin4_" + s), ("Spinner", "Foot4_" + s)]              # abdomen
    P += [("Shin1_L", "Shin1_R"), ("Foot1_L", "Foot1_R"), ("Chel_L", "Chel_R"), ("Fang_L", "Fang_R"),
          ("Abd", "Spine"), ("Abd", "Head")]
    return P


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        for i in (1, 2, 3, 4):
            H, K, A, T = (X(p, s) for p in leg_pts(i))
            out += [(tuple(H), tuple(H), 0.10, "Leg%d_%s" % (i, side)), (tuple(K), tuple(K), 0.08, "Shin%d_%s" % (i, side)),
                    (tuple(A), tuple(A), 0.05, "Foot%d_%s" % (i, side))]
        out += [((s * 0.062, -0.60, 0.45), (s * 0.062, -0.60, 0.45), 0.07, "Chel_" + side),
                ((s * 0.058, -0.70, 0.28), (s * 0.058, -0.70, 0.28), 0.045, "Fang_" + side),
                ((s * 0.15, -0.55, 0.39), (s * 0.15, -0.55, 0.39), 0.045, "Palp_" + side)]
    out += [((0, 0.0, 0.47), tuple(A0), 0.10, "Abd"), ((0, 0.0, 0.47), (0, 0.0, 0.47), 0.09, "Pedicel"),
            ((-0.12, -0.50, 0.55), (0.12, -0.50, 0.55), 0.05, "Head"), ((0, 1.13, 0.66), (0, 1.13, 0.66), 0.05, "Spinner")]
    return out


# ------------------------------------------------------------------ animation v1 (brief section 6). References (owner
# rule, _review/ANIM_REFERENCES_1014.md): #7 HTTYD step-freeze-scan (idle), #4 creature weight + the brief's
# metachronal tetrapod (walk; no spider clip exists on animationreference.org / Sakugabooru), #6 Monsters University
# scare pop (roar: crouch, explode in 5-7 f, hold), #5 "Attack" cocked tell -> 2-frame snap + hard stop (act cast).
# Rules: no head shakes, no spins, no jumps, no thread-hanging; every leg solved every frame; same pole all clip;
# any swing > 60 deg between two frames gets an in-between.
import petkit as pk
import _common as cm

AZ = {i: LEGP[i][0] for i in LEGP}
WALK_OFF = [("Leg4_R", 0.18), ("Leg3_L", 0.12), ("Leg2_R", 0.06), ("Leg1_L", 0.00),
            ("Leg4_L", 0.68), ("Leg3_R", 0.62), ("Leg2_L", 0.56), ("Leg1_R", 0.50)]
WALK_LIFT = {1: 0.075, 2: 0.060, 3: 0.055, 4: 0.050}


def curve(keys, f):
    """smoothstep through (frame, value) keys"""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            return v0 + (v1 - v0) * u * u * (3 - 2 * u)
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]


def body(k, f, z=0.0, pitch=0.0, yaw=0.0, roll=0.0, y=0.0):
    """Spine = the whole body (Root move); pitch + = nose DOWN"""
    k.key("Spine", f, rot=(pitch, yaw, roll), loc=(0, y, z))


def head(k, f, pitch=0.0, yaw=0.0):
    k.key("Head", f, rot=(pitch, yaw, 0))


def abdomen(k, f, lift=0.0, yaw=0.0, ped=0.0, ped_yaw=0.0, spin=0.0):
    """+Y bones: lift + = rear UP (rift to the front), - = rear DOWN (rift to the game camera); ped_yaw + swings the
    abdomen toward -x (the R side)"""
    k.key("Pedicel", f, rot=(ped, ped_yaw, 0))
    k.key("Abd", f, rot=(lift, yaw, 0))
    k.key("Spinner", f, rot=(spin, 0, 0))


def fangs(k, f, spread=0.0, lift=0.0, unfold=0.0):
    """chelicerae spread OUT (yaw) and lift forward; fangs unfold forward (- pitch on the -Z fang bones)"""
    for s, sd in ((1, "L"), (-1, "R")):
        k.key("Chel_" + sd, f, rot=(-lift, s * spread, 0))
        k.key("Fang_" + sd, f, rot=(-unfold, 0, 0))


def palps(k, f, spread=0.0, pitch=0.0, alt=0.0, l_extra=0.0):
    """spread OUT (yaw); pitch + = the tips swing DOWN-back, - = up-forward; alt = alternating pitch (L +alt, R -alt:
    the rasp / stride swing)"""
    k.key("Palp_L", f, rot=(pitch + alt + l_extra, spread, 0))
    k.key("Palp_R", f, rot=(pitch - alt, -spread, 0))


def leg_raise(k, f, i, side, fem=0.0, shin=0.0, foot=0.0, shin_fwd=0.0):
    """FK about the leg-plane axis (brief 5.7, review W4): fem + = the femur leans OUT, shin / foot + = the knee /
    ankle OPEN (the shin swings up). R = the mirrored axis with the opposite angle. shin_fwd = a forward yaw on the
    SHIN only (review 1 s6.2: legs 1 read as a raised V, not the banned sideways T; never yaw the femur)."""
    from mathutils import Quaternion
    a = math.radians(AZ[i])
    s = 1 if side == "L" else -1
    t = Vector((-s * math.sin(a), math.cos(a), 0))
    cm.key_axis(k, "Leg%d_%s" % (i, side), f, t, s * fem)
    cm.key_axis(k, "Shin%d_%s" % (i, side), f, t, -s * shin,
                extra=Quaternion((0, 0, 1), math.radians(-s * shin_fwd)) if shin_fwd else None)
    cm.key_axis(k, "Foot%d_%s" % (i, side), f, t, -s * foot)


def ankle_to(k, leg, f, P, toe=None):
    """raised-ankle helper (brief 5.3): put the ANKLE of `leg` at world point P (call after frame_set(f))"""
    hipR, ankR = k.J[leg], k.J[k.legs2[leg]["foot"]]
    k.solve_leg(leg, f, Vector((P.x - (ankR.x - hipR.x), P.y - (ankR.y - hipR.y), P.z - ankR.z)), toe=toe)


def plant8(k, frames, legs=None):
    """every listed leg keeps its claw on its rest spot (no slide)"""
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in (legs or LEGS8):
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


def tap(k, leg, f, keys):
    """a planted leg's claw lifted by curve(keys) (web-line test taps)"""
    k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, curve(keys, f))))


# ---- idle
def idle(k):
    """STILL HUNTER (ref #7): long holds; an L1 web tap (2 taps); the whole body turns toward a sound (+8, one way per
    loop, the head leading by 2 f); a fang flex with a palp rasp; an R2 double tap with a rift pump; exact rest f120."""
    import bpy
    n = 120
    k.new_action("idle", n, True)
    yaw_c = [(0, 0), (30, 0), (38, 8), (50, 8), (60, 0), (120, 0)]
    head_c = [(0, 0), (28, 0), (36, 6), (48, 6), (58, 0), (120, 0)]
    chel = [(0, 0), (64, 0), (70, 8), (80, 8), (86, 0), (120, 0)]
    unf = [(0, 0), (64, 0), (70, 25), (76, 25), (84, 0), (120, 0)]
    pump = [(0, 0), (98, 0), (100, 3), (106, 0), (120, 0)]
    twitch = [(0, 0), (11, 0), (12, -10), (15, 0), (120, 0)]
    for f in range(0, n + 1, 2):
        body(k, f, z=0.006 * pk.wave(f, n, 0.0, 2), yaw=curve(yaw_c, f))
        head(k, f, yaw=curve(head_c, f))
        abdomen(k, f, lift=1.5 * pk.wave(f, n, 0.1, 2) + curve(pump, f), ped=0.5 * pk.wave(f, n, 0.05, 2))
        rasp = (6 if (f // 2) % 2 else -6) if 70 <= f <= 78 else 0
        palps(k, f, alt=rasp, l_extra=curve(twitch, f))
        fangs(k, f, spread=curve(chel, f), unfold=curve(unf, f))
    for f in (11, 13):                                      # the palp twitch lands between the 2-f keys
        palps(k, f, l_extra=curve(twitch, f))
    k.bake_bezier_now()
    tap1 = [(0, 0), (8, 0), (10, 0.05), (13, 0), (15, 0.05), (18, 0), (22, 0), (120, 0)]
    tap2 = [(0, 0), (92, 0), (94, 0.05), (97, 0), (99, 0.05), (102, 0), (106, 0), (120, 0)]
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        for leg in LEGS8:
            if leg == "Leg1_L":
                tap(k, leg, f, tap1)
            elif leg == "Leg2_R":
                tap(k, leg, f, tap2)
            else:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish()
    k.meta["planted"] = [l for l in LEGS8 if l not in ("Leg1_L", "Leg2_R")]
    k.events["idle"] = {"pulse1": round(40 / n, 3), "flex": round(70 / n, 3), "pulse2": round(100 / n, 3)}


# ---- walk
def walk(k):
    """SCUTTLE: metachronal tetrapod (brief 5.4), duty 0.58, stride half 0.085, per-pair lift; one body bob per
    tetrapod, yaw +-1.2 / roll +-0.8, the head counter-yaws, the abdomen lags 2 f (ref #4), palps swing with legs 1."""
    import bpy
    n, S, duty = 32, 0.085, 0.58
    k.new_action("walk", n, True)
    for f in range(0, n + 1, 2):
        yw = 1.2 * pk.wave(f, n, 0.0, 1)
        body(k, f, z=0.006 * pk.wave(f, n, 0.10, 2), yaw=yw, roll=0.8 * pk.wave(f, n, 0.25, 1))
        head(k, f, yaw=-0.5 * yw)
        abdomen(k, f, lift=1.0 * pk.wave(f, n, 0.04, 2), yaw=-1.5 * pk.wave(f, n, -0.06, 1))
        palps(k, f, alt=6 * pk.wave(f, n, 0.0, 1))
        fangs(k, f)
    k.bake_bezier_now()
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        for leg, off in WALK_OFF:
            k.solve_leg(leg, f, pk.gait_target(k, leg, f, n, off, S, WALK_LIFT[int(leg[3])], duty))
    k.finish()
    k.meta["walk_cycle"] = n
    k.meta["legs"] = list(WALK_OFF)
    k.meta["duty"] = duty
    return 2 * S / duty


# ---- roar
def roar(k):
    """FANG FLARE (ref #6): gather (crouch, palps tuck) -> rear (Spine -14 nose-up, ABDOMEN LEVEL RULE) -> legs 1 raise
    by OPENING the knee (LEG-1 RULE), legs 2 lower and 2 f later -> fang flare (`flare` f22) -> stridulation rasp hold
    with one fang stab -> legs 2 land, then legs 1 (shin closes before the femur) -> exact rest f72."""
    import bpy
    n = 72
    k.new_action("roar", n, False)
    zc = [(0, 0), (10, -0.04), (20, 0.06), (54, 0.06), (62, 0.01), (66, 0.0), (68, -0.01), (72, 0)]
    pc = [(0, 0), (10, 5), (20, -14), (54, -14), (62, -4), (66, 0), (72, 0)]
    ped = [(0, 0), (10, 0), (20, 6), (54, 6), (66, 0), (72, 0)]
    abd = [(0, 0), (10, 0), (20, 8), (54, 8), (66, 0), (72, 0)]
    chs = [(0, 0), (18, 0), (24, 12), (54, 12), (62, 0), (72, 0)]
    chl = [(0, 0), (18, 0), (24, 18), (54, 18), (62, 0), (72, 0)]
    unf = [(0, 0), (18, 0), (22, 45), (24, 65), (38, 65), (40, 53), (44, 65), (54, 65), (62, 0), (72, 0)]
    pls = [(0, 0), (18, 0), (24, 28), (54, 28), (62, 0), (72, 0)]
    # palps lift a little in the crouch (+ pitch swings their tips DOWN into the ground), flare at +12 so the
    # +-7 rasp stays inside the femur-clear band +5..+19 (W4 static tests)
    plp = [(0, 0), (10, -6), (18, -6), (24, 12), (54, 12), (62, 0), (72, 0)]
    for f in range(0, n + 1):
        thrum = (2 if (f // 3) % 2 else -2) if 24 <= f <= 54 else 0
        body(k, f, z=curve(zc, f), pitch=curve(pc, f))
        head(k, f)
        abdomen(k, f, lift=curve(abd, f) + thrum, ped=curve(ped, f))
        rasp = (7 if (f // 2) % 2 else -7) if 26 <= f <= 50 else 0
        palps(k, f, spread=curve(pls, f), pitch=curve(plp, f), alt=rasp)
        fangs(k, f, spread=curve(chs, f), lift=curve(chl, f), unfold=curve(unf, f))
    # legs 1: FK raise f12 -> f22 (keys every 2 f), hold + shin tremble, land f60 -> f66 (shin closes first)
    # (FK starts at the rest shape once the rear has lifted the front: at f12 the gather crouch would dip the claws)
    L1 = [(14, (0, 0, 0)), (16, (3, 16, 4)), (18, (7, 40, 10)), (20, (12, 65, 16)), (22, (15, 80, 20)),
          (60, (15, 80, 20)), (62, (15, 55, 14)), (64, (12, 25, 8)), (65, (3, 8, 3))]
    L2 = [(16, (0, 0, 0)), (18, (2, 14, 4)), (20, (4, 30, 8)), (22, (5, 40, 10)),
          (58, (5, 40, 10)), (60, (3, 18, 5)), (61, (1, 6, 2))]
    for side in ("L", "R"):
        for f, (fe, sh, fo) in L1:
            tr = (2 if (f // 3) % 2 else -2) if 24 <= f <= 54 else 0
            leg_raise(k, f, 1, side, fe, sh + tr, fo, shin_fwd=35.0 * sh / 80.0)
        for f in range(24, 55, 3):                              # the leg-1 shin tremble keys
            leg_raise(k, f, 1, side, 15, 80 + (2 if (f // 3) % 2 else -2), 20, shin_fwd=35.0)
        for f, (fe, sh, fo) in L2:
            leg_raise(k, f, 2, side, fe, sh, fo)
    plant8(k, range(0, n + 1), ["Leg3_L", "Leg3_R", "Leg4_L", "Leg4_R"])
    plant8(k, list(range(0, 14)) + list(range(66, n + 1)), ["Leg1_L", "Leg1_R"])
    plant8(k, list(range(0, 16)) + list(range(62, n + 1)), ["Leg2_L", "Leg2_R"])
    k.finish()
    k.events["roar"] = {"flare": round(22 / n, 3), "rasp": round(26 / n, 3), "pulse": round(36 / n, 3),
                        "stab": round(40 / n, 3)}


# ---- act
def act_riftweave(k):
    """RIFT WEAVE (signature; ref #5 for the cast): wind-up (rear up) -> PRESENT: the abdomen tilts rear-DOWN so the
    rift faces the game camera (`rift` f24) -> three silk draws by the hind legs (L4, R4, L4: out-back-up to
    (+-1.02, 0.70, 0.45), `silk1-3`), each with a spinner flick, an abdomen pump and the pedicel turning AWAY from the
    drawing leg -> CAST: the abdomen whips down-up -8 -> +10 in 6 f with an in-between, a hard stop at f80 (`cast`)
    -> settle, exact rest f120."""
    import bpy
    n = 120
    k.new_action("act_riftweave", n, False)
    draws = [("Leg4_L", 28, 1), ("Leg4_R", 42, -1), ("Leg4_L", 56, 1)]
    zc = [(0, 0), (12, 0.02), (24, 0.06), (74, 0.06), (80, 0.05), (100, 0.01), (120, 0)]
    yc = [(0, 0), (74, 0), (78, 0.03), (84, 0), (120, 0)]
    pc = [(0, 0), (12, 3), (24, -6), (74, -6), (80, 2), (96, 0), (120, 0)]
    ped = [(0, 0), (12, 0), (24, -4), (74, -4), (80, 2), (100, 0), (120, 0)]
    abd = [(0, 0), (12, 8), (18, 0), (24, -8), (74, -8), (77, 1), (80, 10), (92, -2), (100, 0), (120, 0)]
    unf = [(0, 0), (74, 0), (78, 25), (80, 35), (84, 35), (96, 0), (120, 0)]
    plp = [(0, 0), (12, 12), (72, 12), (84, 0), (120, 0)]
    spin, pump, pyaw = [(0, 0)], [(0, 0)], [(0, 0)]
    for leg, d0, s in draws:
        spin += [(d0 + 4, 0), (d0 + 6, -12), (d0 + 9, 0)]
        pump += [(d0 + 4, 0), (d0 + 6, -3), (d0 + 8, 0)]
        pyaw += [(d0, 0), (d0 + 4, 4 * s), (d0 + 10, 4 * s), (d0 + 14, 0)]
    spin, pump, pyaw = spin + [(n, 0)], pump + [(n, 0)], pyaw + [(n, 0)]
    for f in range(0, n + 1):
        body(k, f, z=curve(zc, f), pitch=curve(pc, f), y=curve(yc, f))
        head(k, f)
        abdomen(k, f, lift=curve(abd, f) + curve(pump, f), ped=curve(ped, f), ped_yaw=curve(pyaw, f),
                spin=curve(spin, f))
        palps(k, f, pitch=curve(plp, f))
        fangs(k, f, unfold=curve(unf, f))
    k.bake_bezier_now()
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        busy = None
        for leg, d0, s in draws:
            if d0 <= f <= d0 + 12:
                busy = (leg, d0, s)
        for leg in LEGS8:
            if busy and leg == busy[0]:
                _, d0, s = busy
                A0 = k.J[k.legs2[leg]["foot"]].copy()
                T = Vector((s * 1.02, 0.70, 0.45))
                up = A0 + Vector((0, 0, 0.04))
                path = [(d0, A0), (d0 + 2, up), (d0 + 6, T), (d0 + 8, T), (d0 + 12, A0)]
                toe = curve([(d0, 0), (d0 + 6, 30), (d0 + 8, 30), (d0 + 12, 0)], f)
                for (f0, P0), (f1, P1) in zip(path, path[1:]):
                    if f0 <= f <= f1:
                        u = (f - f0) / float(f1 - f0)
                        P = P0.lerp(P1, u * u * (3 - 2 * u))
                        break
                ankle_to(k, leg, f, P, toe=toe)
            else:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish()
    k.events["act_riftweave"] = {"rift": round(24 / n, 3), "silk1": round(34 / n, 3), "silk2": round(48 / n, 3),
                                 "silk3": round(62 / n, 3), "cast": round(80 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    act_riftweave(k)
    return stride
