# Thornblade Mantis (Wood/Grass egg, NEW 2% SECRET, 2026-10-14) - FIERCE style "the jade executioner": a warrior
# praying mantis built from tapered blocks under a Roblox stud skin. A raised prothorax carries a triangular head with
# huge RUBY compound eyes (black pseudo-pupils), an angry brow, dark mandibles and a GOLD cone-crown (hero piece #1,
# reads at icon size). Two raptorial forelegs held in the prayer pose: jade coxa, a broad femur with a GOLD scythe edge
# lined with RUBY thorn crystals and a folded GOLD tibia hook (hero piece #2). Four long spidery walking legs, a
# segmented abdomen under folded leaf-wings (tegmina: dark rim, jade panel, dark veins, gold costal stripe) that hide
# the hindwings with RUBY eye-spots - revealed in the threat display (roar). 3-band colour: dark teal armour / jade
# hide / pale mint underside. No glow.
import math
from mathutils import Vector, Matrix

DISPLAY = "Thornblade Mantis"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 10.0       # total height (crown tip) in studs at x1 - the 2% secret stands over its egg (Treant 10, Stag 11)

# Blender colours (Roblox renders ~0.6x darker)
ARMOR = (18, 74, 70)         # dark teal armour: plates, rims, veins, brows, mandibles, tibiae
HIDE = (36, 182, 146)        # jade hide
HIDE_L = (88, 214, 170)      # light jade wing panels
BELLY = (198, 242, 216)      # pale mint underside
BELLY_D = (150, 206, 178)
GOLD = (255, 196, 50)        # HERO: crown, scythe edges, tibia hooks, costal stripes
GOLD_D = (204, 138, 24)
RUBY_D = (128, 10, 44)       # ACCENT crystal steps: deep -> ruby -> hot
RUBY = (240, 40, 76)
RUBY_HOT = (255, 192, 204)
BLACK = (14, 14, 22)
IVORY = (240, 234, 210)

# walking legs (left): hip, knee (high, out), ankle, toe;  F = middle pair, B = hind pair
LEGS = {"F": ((0.12, -0.06, 0.42), (0.35, -0.22, 0.64), (0.45, -0.40, 0.11), (0.48, -0.51, 0.02)),     # FIX 8
        "B": ((0.12, 0.14, 0.42), (0.37, 0.30, 0.64), (0.47, 0.56, 0.11), (0.50, 0.67, 0.02))}
PRO = (Vector((0, -0.06, 0.52)), Vector((0, -0.38, 0.94)))        # prothorax (Chest) base -> top
NECK = Vector((0, -0.40, 0.96))
HEADP = Vector((0, -0.45, 1.02))                                  # head pivot
HC = Vector((0, -0.52, 1.14))                                     # head centre (FIX 1: +30 % head)
# raptorial foreleg (left): coxa root, coxa-femur joint ("elbow", low), femur-tibia joint (high), tibia tip
ARM = (Vector((0.08, -0.30, 0.84)), Vector((0.17, -0.46, 0.62)), Vector((0.21, -0.64, 1.00)),     # FIX 4: knee at
       Vector((0.20, -0.73, 0.66)))                                                                # head height
ABD = [Vector(p) for p in ((0, 0.20, 0.44), (0, 0.52, 0.45), (0, 0.82, 0.48), (0, 1.06, 0.56))]
WROOT = Vector((0.03, 0.02, 0.58))     # wing hinge (left)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def ruby_gem(B, c, n, size, bone):
    """faceted ruby crystal: deep base -> ruby body -> hot tip along n"""
    n = Vector(n).normalized()
    c = Vector(c)
    B.spike(c - n * 0.01, n, size * 1.0, size * 0.55, RUBY_D, bone, top=(0.7, 0.7))
    B.spike(c + n * size * 0.25, n, size * 0.85, size * 0.42, RUBY, bone, top=(0.15, 0.15))
    B.spike(c + n * size * 0.75, n, size * 0.40, size * 0.18, RUBY_HOT, bone, top=(0.1, 0.1))


ANT0 = (0.03, -0.095, 0.105)          # antenna root offset from HC (above the V-brow)
ANT1 = (0.05, -0.07, 0.15)


def surf_hit(B, blks, origin, direction):
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


def ellipsoid(B, c, ax, color, bone, R=None, n=18, rings=10):
    """lathed ellipsoid (a smooth dome, no studs): semi-axes ax=(x, y, z) in the local frame R, centre c"""
    from mathutils import Matrix
    R = R if R is not None else Matrix.Identity(3)
    out = []
    for i in range(rings + 1):
        th = math.pi * (0.03 + 0.94 * i / rings)
        z, r = math.cos(th), math.sin(th)
        out.append([Vector(c) + R @ Vector((ax[0] * r * math.cos(2 * math.pi * j / n),
                                            ax[1] * r * math.sin(2 * math.pi * j / n), ax[2] * z))
                    for j in range(n)])
    return B.tube(out, color, bone, nostud=True)


def on_surf(c, ax, R, u, t=1.0):
    """the point of the ellipsoid (c, ax, R) in direction u (scaled by t: < 1 sinks it in)"""
    u = Vector(u).normalized()
    return Vector(c) + R @ Vector((ax[0] * u.x, ax[1] * u.y, ax[2] * u.z)) * t


def disc(B, c, r, color, bone, sx=0.75, sy=1.15, thick=0.012, dz=0.0):
    pts = [c + Vector((r * sx * math.cos(a), r * sy * math.sin(a), dz)) for a in
           [2 * math.pi * i / 12 for i in range(12)]]
    B.poly([c + Vector((0, 0, dz))] + pts + [pts[0]], thick, color, bone)


def leaf(s, t, w):
    """outline point of the folded tegmen at length t (0 hinge -> 1 tip), across w (0 midline -> 1 outer edge)"""
    y = WROOT.y + t * 1.00
    half = 0.17 * math.sin(math.pi * min(1.0, t * 1.08) ** 0.75) + 0.02
    x = s * (0.02 + w * half)
    z = 0.592 + 0.04 * t - 0.035 * w * w
    return Vector((x, y, z))


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=211, tier=3, plates=False)
    # ---------------- thorax (Spine): meso/metathorax block, dark dorsal plate, pale underside
    B.add((0, 0.04, 0.44), (0.13, 0.20, 0.10), HIDE, "Spine", bot=(0.8, 0.85), top=(0.85, 0.95), rnd=0.30)
    B.add((0, 0.04, 0.542), (0.10, 0.18, 0.018), ARMOR, "Spine", top=(0.85, 0.9))
    B.add((0, 0.04, 0.338), (0.09, 0.15, 0.014), BELLY, "Spine", studs=[])
    # ---------------- abdomen (Tail1-3): wide flat segments, pale ventral plates, dark tergite rings, rising tip
    dims = ((0.15, 0.085), (0.155, 0.085), (0.11, 0.07))
    for i, ((a, b), (w, d)) in enumerate(zip(zip(ABD, ABD[1:]), dims)):
        bone = "Tail%d" % (i + 1)
        B.seg(a, b, w, d, HIDE, bone, ext=0.06 if i == 0 else 0.02, ext1=0.02, top=(0.9 if i < 2 else 0.55, 0.85))
        B.seg(a + Vector((0, 0, -d + 0.05)), b + Vector((0, 0, -d * 0.8 + 0.05)), w * 1.03, 0.06, BELLY, bone,
              ext=0.01, top=(0.9 if i < 2 else 0.6, 1))                                       # sternites: mint stripe
        u = (b - a).normalized()
        p = a.lerp(b, 0.85)
        tw = 1.04 if i < 2 else 0.80
        B.seg(p - u * 0.022 + Vector((0, 0, d * 0.40)), p + u * 0.022 + Vector((0, 0, d * 0.40)), w * tw, d * 0.62,
              ARMOR, bone, top=(0.98, 0.98))                                                 # tergite band (upper 60 %)
        B.seg(p - u * 0.014 + Vector((0, 0, -d * 0.85 + 0.04)), p + u * 0.014 + Vector((0, 0, -d * 0.85 + 0.04)),
              w * 1.045 * (1 if i < 2 else 0.7), 0.054, BELLY_D, bone, studs=[])              # sternite gap bar
    for s in (1, -1):                                                                       # cerci at the tip
        B.spike(ABD[3] + Vector((s * 0.03, -0.02, 0)), (s * 0.3, 1, 0.25), 0.10, 0.014, ARMOR, "Tail3")
    # ---------------- folded hindwings (hidden under the tegmina; RUBY eye-spot shown in the threat display)
    for s, side in ((1, "L"), (-1, "R")):
        hb = "Wing_" + side
        P = [leaf(s, t, w) - Vector((0, 0, 0.026)) for t, w in ((0.02, 0.1), (0.25, 0.85), (0.6, 0.85), (0.9, 0.5),
                                                                  (0.97, 0.05), (0.5, 0.0))]
        B.poly([P[5], P[0], P[1], P[2], P[3], P[4]], 0.014, ARMOR, hb)
        eye = leaf(s, 0.55, 0.45) - Vector((0, 0, 0.026))
        sc = 0.10 / 0.085
        for r, c, dz in ((0.085, BLACK, 0.0), (0.062, RUBY_D, 0.004), (0.046, RUBY, 0.008), (0.018, RUBY_HOT, 0.012)):
            disc(B, eye, r * sc, c, hb, dz=dz)                                                  # top face
            disc(B, eye, r * sc, c, hb, dz=-0.016 - dz / 0.004 * 0.004)                          # underside (FIX 7)
    # ---------------- tegmina (folded leaf-wings, the main read from the game camera)
    for s, side in ((1, "L"), (-1, "R")):
        eb = "Elytra_" + side
        out = [leaf(s, t, 1.0) for t in (0.0, 0.12, 0.3, 0.5, 0.7, 0.86, 0.97)]
        mid = [leaf(s, t, 0.0) for t in (0.97, 0.7, 0.4, 0.1)]
        B.poly([leaf(s, 0.45, 0.5)] + out + mid + [out[0]], 0.024, ARMOR, eb)                   # dark rim
        inner = [leaf(s, t, 0.80) + Vector((0, 0, 0.006)) for t in (0.08, 0.3, 0.5, 0.7, 0.84)]
        inner += [leaf(s, t, 0.16) + Vector((0, 0, 0.006)) for t in (0.84, 0.6, 0.3, 0.08)]
        B.poly([leaf(s, 0.45, 0.5) + Vector((0, 0, 0.006))] + inner + [inner[0]], 0.022, HIDE_L, eb)  # jade panel
        # gold costal stripe along the outer edge + dark veins
        cs = [leaf(s, t, 0.93) + Vector((0, 0, 0.012)) for t in (0.06, 0.25, 0.45, 0.65, 0.82)]
        for a, b in zip(cs, cs[1:]):
            B.bar(a, b, Vector((s * 0.25, 0, 1)), 0.032, 0.008, GOLD, eb, studs=[], bevel=0.003)
        vm = [leaf(s, t, 0.5) + Vector((0, 0, 0.014)) for t in (0.06, 0.3, 0.55, 0.8, 0.93)]
        for a, b in zip(vm, vm[1:]):
            B.bar(a, b, Vector((0, 0, 1)), 0.016, 0.006, ARMOR, eb, studs=[], bevel=0.002)      # mid vein
        for t in (0.28, 0.48, 0.68):
            a = leaf(s, t, 0.5) + Vector((0, 0, 0.014))
            b = leaf(s, t + 0.1, 0.88) + Vector((0, 0, 0.014))
            B.bar(a, b, Vector((0, 0, 1)), 0.012, 0.006, ARMOR, eb, studs=[], bevel=0.002)      # side veins
        st = leaf(s, 0.42, 0.72)
        for i, (r, c) in enumerate(((0.035, RUBY_D), (0.025, RUBY), (0.012, RUBY_HOT))):        # ruby stigma (W2)
            disc(B, st, r, c, eb, sx=1.0, sy=1.3, thick=0.006, dz=0.014 + 0.004 * i)
    # ---------------- prothorax (Chest): long raised neck-shield, dark dorsal ridge, pale throat, pronotum flare
    B.seg(PRO[0] + Vector((0, 0.04, -0.04)), PRO[1], 0.085, 0.075, HIDE, "Chest", ext=0.05, ext1=0.03, top=(0.8, 0.9))
    d = (PRO[1] - PRO[0]).normalized()
    n_up = Vector((0, 0.795, 0.606))

    def A(t):
        return PRO[0].lerp(PRO[1], t) + n_up * 0.09

    def shw(t):                                       # shield half-width: a diamond, widest at the front third
        return 0.155 * (0.42 + 0.58 * (t - 0.15) / 0.30 if t < 0.45 else 1.0 - 0.65 * (t - 0.45) / 0.53)
    B.seg(A(0.15), A(0.45), 0.155, 0.018, ARMOR, "Chest", bot=(0.42, 1))                    # PRONOTUM SHIELD (FIX 5)
    B.seg(A(0.45), A(0.98), 0.155, 0.018, ARMOR, "Chest", top=(0.35, 1))
    for t, L in ((0.25, 0.07), (0.45, 0.09), (0.65, 0.07)):                                  # thorny edge, ruby points
        for s in (1, -1):
            base = A(t) + Vector((s * shw(t) * 0.92, 0, 0))
            dv = (Vector((s, 0, 0)) + d * 0.35 + n_up * 0.25).normalized()
            B.spike(base, dv, L, 0.024, ARMOR, "Chest", top=(0.3, 0.3))
            B.spike(base + dv * L * 0.6, dv, L * 0.55, 0.014, RUBY, "Chest", studs=[], nostud=True)
    nrm = Vector((0, 0.8, -0.6)).normalized()
    B.seg(PRO[0].lerp(PRO[1], 0.40) + Vector((0, -0.05, -0.04)),
          PRO[1] + Vector((0, -0.05, -0.05)), 0.045, 0.03, BELLY, "Chest", top=(0.8, 1))               # throat tie
    for t in (0.55, 0.78):
        q = PRO[0].lerp(PRO[1], t) + Vector((0, -0.05, -0.045))
        B.seg(q - d * 0.012, q + d * 0.012, 0.047, 0.032, BELLY_D, "Chest", studs=[])
    B.seg(NECK + Vector((0, 0.02, -0.03)), HEADP + Vector((0, -0.02, 0.0)), 0.07, 0.05, HIDE, "Neck", ext=0.03)
    # ---------------- head: triangular face, huge RUBY compound eyes, black pseudo-pupils, angry brow
    B.add(HC, (0.15, 0.09, 0.11), HIDE, "Head", bot=(0.38, 0.85), top=(1.0, 0.95), rnd=0.25)        # FIX 1 head
    B.add(HC + Vector((0, -0.02, -0.145)), (0.065, 0.06, 0.045), HIDE, "Head", bot=(0.6, 0.8))       # lower face
    B.add(HC + Vector((0, -0.088, 0.055)), (0.085, 0.012, 0.05), ARMOR, "Head", bot=(0.35, 1), role="detail",
          bevel=0.006)                                                                         # executioner hood
    B.add(HC + Vector((0, -0.083, -0.15)), (0.03, 0.008, 0.016), BELLY_D, "Head", studs=[], role="detail",
          bevel=0.004)                                                                         # mouth plate
    for s, side in ((1, "L"), (-1, "R")):                                                     # FIX 0: own side
        from mathutils import Euler
        e = HC + Vector((s * 0.165, -0.02, 0.075))                                             # FIX 2: ruby DOMES
        Re = Euler((0, math.radians(s * 12), math.radians(s * 18)), "XYZ").to_matrix()          # (lathed ovals)
        ellipsoid(B, e, (0.072, 0.07, 0.090), RUBY_D, "Head", Re, n=24, rings=14)               # deep rim (back)
        eb, axb = e + Vector((s * 0.012, -0.018, 0.004)), (0.066, 0.064, 0.086)
        ellipsoid(B, eb, axb, RUBY, "Head", Re, n=24, rings=14)                                  # ruby body
        ellipsoid(B, on_surf(eb, axb, Re, (-s * 0.12, -0.98, 0.0), 0.92), (0.009, 0.012, 0.032), BLACK, "Head",
                  Re)                                                                            # pseudo-pupil slit
        B.add(HC + Vector((s * 0.115, -0.105, 0.088)), (0.105, 0.018, 0.022), ARMOR, "Head",
              rot=(0, -s * 22, s * 14), role="detail", bevel=0.008)                            # V-brow = ANGRY LID
        # mandibles (dark, ivory tips) + palps
        m0 = HC + Vector((s * 0.035, -0.05, -0.185))
        B.spike(m0, (-s * 0.55, -0.6, -0.55), 0.10, 0.024, ARMOR, "Jaw", top=(0.4, 0.4))
        B.spike(m0 + Vector((-s * 0.04, -0.045, -0.045)), (-s * 0.9, -0.3, -0.3), 0.045, 0.011, IVORY, "Jaw")
        B.spike(HC + Vector((s * 0.06, -0.035, -0.155)), (s * 0.4, -0.5, -1), 0.085, 0.012, ARMOR, "Jaw")
        # antennae: from ABOVE the V, swept up-back (never through the brows); tips under the crown tip
        a0 = HC + Vector((s * ANT0[0], ANT0[1], ANT0[2]))
        a1 = a0 + Vector((s * ANT1[0], ANT1[1], ANT1[2]))
        a2 = a1 + Vector((s * 0.10, 0.06, 0.10))                                               # arc up, out, back
        a3 = a2 + Vector((s * 0.13, 0.20, 0.03))
        B.seg(a0, a1, 0.013, 0.013, ARMOR, "Antenna_" + side, ext=0.01, role="limb")
        B.seg(a1, a2, 0.010, 0.010, ARMOR, "Antenna_" + side, ext=0.006, role="limb")
        B.seg(a2, a3, 0.008, 0.008, ARMOR, "Antenna_" + side, ext=0.005, role="limb")
    # GOLD CROWN (FIX 3, hero #1): solid band between the eye domes + a dominant 0.34 cone (the model top) + prongs
    B.add(HC + Vector((0, 0, 0.12)), (0.09, 0.06, 0.032), GOLD, "Head", top=(0.85, 0.85), role="limb", bevel=0.01)
    B.spike(HC + Vector((0, 0, 0.14)), (0, 0.25, 1), 0.34, 0.065, GOLD, "Head", top=(0.12, 0.12))
    for s in (1, -1):
        B.spike(HC + Vector((s * 0.055, 0, 0.14)), (s * 0.5, 0.2, 1), 0.18, 0.042, GOLD, "Head", top=(0.12, 0.12))
    B.spike(HC + Vector((0, 0.02, 0.19)), (0, 0.35, 1), 0.16, 0.03, GOLD_D, "Head", top=(0.3, 0.3))   # cone keel
    ruby_gem(B, HC + Vector((0, -0.062, 0.12)), (0, -1, 0.15), 0.06, "Head")
    B.add(HC + Vector((0, 0.062, 0.115)), (0.07, 0.012, 0.03), GOLD, "Head", role="limb", bevel=0.006)  # back plate
    ruby_gem(B, HC + Vector((0, 0.072, 0.115)), (0, 1, 0.15), 0.045, "Head")
    # ---------------- raptorial forelegs (hero #2): coxa -> femur scythe (gold edge, ruby thorns) -> gold tibia hook
    for s, side in ((1, "L"), (-1, "R")):
        C0, C1, F1, T1 = (X(p, s) for p in ARM)
        arm, fore, blade = "Arm_" + side, "Fore_" + side, "Blade_" + side
        B.seg(C0, C1, 0.05, 0.055, HIDE, arm, ext=0.04, ext1=0.03, top=(0.8, 0.8))                  # coxa
        B.add(C1, (0.055, 0.055, 0.055), ARMOR, arm, rnd=0.5)                                        # joint
        B.seg(C1, F1, 0.045, 0.075, ARMOR, fore, ext=0.03, ext1=0.03, top=(0.75, 0.6))              # dark femur
        fd = (F1 - C1).normalized()
        fwd = Vector((0, -1, 0))
        edge = (fwd - fd * fwd.dot(fd)).normalized()                                             # femur's front edge
        P0 = C1 + fd * 0.03 + edge * 0.075
        Pm = C1.lerp(F1, 0.5) + edge * 0.11
        P1 = F1 - fd * 0.03 + edge * 0.07
        kw = dict(side=(1, 0, 0), studs=[], nostud=True, role="limb")
        B.seg(P0, Pm, 0.035, 0.04, GOLD, fore, bot=(0.7, 0.7), ext1=0.01, **kw)                    # GOLD CRESCENT
        B.seg(Pm, P1, 0.035, 0.04, GOLD, fore, top=(0.7, 0.7), ext=0.01, **kw)

        def cres(t):
            return P0.lerp(Pm, t * 2) if t < 0.5 else Pm.lerp(P1, t * 2 - 1)
        for i, t in enumerate((0.2, 0.36, 0.52, 0.68, 0.84)):                                    # ruby saw: outer row
            ruby_gem(B, cres(t) + edge * 0.035, edge * 0.8 + fd * 0.3 + Vector((s * 0.45, 0, 0)),
                     0.075 if i % 2 == 0 else 0.05, fore)
        for t in (0.28, 0.6):                                                                     # inner row
            ruby_gem(B, cres(t) + edge * 0.03, edge * 0.8 + fd * 0.3 - Vector((s * 0.35, 0, 0)), 0.045, fore)
        B.add(F1, (0.045, 0.045, 0.045), ARMOR, fore, rnd=0.5)                                       # knee knuckle
        B.spike(F1 + Vector((0, 0, 0.03)), (s * 0.7, 0.5, 0.5), 0.11, 0.032, GOLD, fore, top=(0.12, 0.12))  # spine
        td = (T1 - F1).normalized()
        B.seg(F1, T1, 0.032, 0.042, GOLD, blade, ext=0.02, top=(0.7, 0.6))                           # gold tibia
        tedge = (fwd - td * fwd.dot(td)).normalized()
        hd_ = (td * 0.3 - tedge * 0.95).normalized()
        B.spike(T1 - td * 0.01, hd_, 0.08, 0.028, GOLD, blade, top=(0.3, 0.3))                       # hook
        B.spike(T1 - td * 0.01 + hd_ * 0.075, hd_ + td * 0.3, 0.05, 0.015, BLACK, blade)              # claw
    # ---------------- walking legs: jade femur up-out to a high knee, dark tibia down, black tarsus
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            B.seg(H, K, 0.048, 0.054, HIDE, leg, ext=0.03, ext1=0.03, top=(0.8, 0.8))
            B.add(K, (0.052, 0.052, 0.052), ARMOR, leg, rnd=0.3)
            B.seg(K, A, 0.038, 0.040, ARMOR, shin, ext=0.02, ext1=0.02, top=(0.7, 0.7))
            for t in (0.3, 0.55):
                B.spike(K.lerp(A, t), (s * 0.5, 0.0, -0.4) if fb == "F" else (s * 0.5, 0.3, -0.3), 0.04, 0.009,
                        BLACK, shin)
            B.seg(A, P, 0.024, 0.022, ARMOR, foot, ext=0.015)
            B.spike(P, P - A, 0.05, 0.012, BLACK, foot)
    B.build()
    mn, mx = k.bounds()
    pitch = 0.2243 * (mx.z - mn.z) / HEIGHT
    bk.stud_skin(k, pitch)
    return {"TH": round(B.th, 3), "pitch": round(pitch, 4), "H": round(mx.z - mn.z, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.04, 0.44), "Root", tail=(0, -0.3, 0))
    k.joint("Chest", tuple(PRO[0]), "Spine", tail=tuple(PRO[1] - PRO[0]))
    k.joint("Neck", tuple(NECK), "Chest", tail=(0, -0.05, 0.06))
    k.joint("Head", tuple(HEADP), "Neck", tail=(0, -0.1, 0.1))
    k.joint("Jaw", tuple(HC + Vector((0, -0.03, -0.12))), "Head", tail=(0, -0.05, -0.08))
    k.joint("Strike", tuple(HC + Vector((0, -0.45, -0.25))), "Chest", tail=(0, -0.2, 0))   # strike VFX anchor
    for s, side in ((1, "L"), (-1, "R")):
        C0, C1, F1, T1 = (X(p, s) for p in ARM)
        k.joint("Antenna_" + side, tuple(HC + Vector((s * ANT0[0], ANT0[1], ANT0[2]))), "Head",
                tail=(s * ANT1[0], ANT1[1], ANT1[2]))
        k.joint("Arm_" + side, tuple(C0), "Chest")
        k.joint("Fore_" + side, tuple(C1), "Arm_" + side)
        k.joint("Blade_" + side, tuple(F1), "Fore_" + side, tail=tuple(T1 - F1))
        k.joint("Elytra_" + side, tuple(X(WROOT, s)), "Spine", tail=(0, 0.5, 0.02))
        k.joint("Wing_" + side, tuple(X(WROOT, s) - Vector((0, 0, 0.02))), "Spine", tail=(0, 0.5, 0.02))
        for fb, knee in (("F", (s * 0.5, -0.2, 1)), ("B", (s * 0.5, 0.2, 1))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, "Spine")
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=tuple(P - A))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", tuple(ABD[0]), "Spine")
    k.joint("Tail2", tuple(ABD[1]), "Tail1")
    k.joint("Tail3", tuple(ABD[2]), "Tail2", tail=tuple(ABD[3] - ABD[2]))


LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]


def check_pairs():
    P = []
    for s in ("L", "R"):
        P += [("Leg_F" + s, "Leg_B" + s), ("Shin_F" + s, "Shin_B" + s), ("Foot_F" + s, "Foot_B" + s),
              ("Fore_" + s, "Head"), ("Blade_" + s, "Head"), ("Fore_" + s, "Jaw"), ("Blade_" + s, "Jaw"),
              ("Blade_" + s, "Chest"), ("Fore_" + s, "Shin_F" + s), ("Blade_" + s, "Shin_F" + s),
              ("Elytra_" + s, "Tail1"), ("Elytra_" + s, "Tail2"), ("Elytra_" + s, "Tail3"),
              ("Wing_" + s, "Elytra_" + s), ("Shin_B" + s, "Tail2"), ("Shin_B" + s, "Tail3")]
    P += [("Fore_L", "Fore_R"), ("Blade_L", "Blade_R"), ("Fore_L", "Blade_R"), ("Fore_R", "Blade_L"),
          ("Elytra_L", "Elytra_R"), ("Wing_L", "Wing_R")]
    return P


HEAD_XF = []
