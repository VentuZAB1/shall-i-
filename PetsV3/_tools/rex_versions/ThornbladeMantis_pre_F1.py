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
    B.spike(c - n * 0.01, n, size * 0.40, size * 0.34, RUBY_D, bone, top=(0.75, 0.75), nostud=True)  # (review 2 M2:
    B.spike(c + n * size * 0.22, n, size * 0.88, size * 0.30, RUBY, bone, top=(0.10, 0.10), nostud=True)  # a thorn,
    B.spike(c + n * size * 0.80, n, size * 0.36, size * 0.13, RUBY_HOT, bone, top=(0.08, 0.08), nostud=True)  # no die)


def gem_inlay(B, c, n, size, bone):
    """flush 45 deg diamond: deep frame -> ruby -> hot glint (review 2 M4)"""
    n = Vector(n).normalized()
    x = Vector((0, 0, 1)).cross(n).normalized()
    z = n.cross(x).normalized()
    Rr = Matrix((x, n, z)).transposed() @ Matrix.Rotation(math.radians(45), 3, "Y")
    kw = dict(R=Rr, studs=[], nostud=True, role="detail")
    B.add(c, (size, 0.008, size), RUBY_D, bone, bevel=0.004, **kw)
    B.add(c + n * 0.006, (size * 0.72, 0.007, size * 0.72), RUBY, bone, bevel=0.003, **kw)
    B.add(c + n * 0.011 + (x + z) * size * 0.25, (size * 0.16, 0.004, size * 0.16), RUBY_HOT, bone, bevel=0.002, **kw)


ANT0 = (0.055, -0.095, 0.105)          # antenna root offset from HC (above the V-brow)
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
        p = a.lerp(b, 0.85 if i < 2 else 0.95)                          # last band clear of the tegmina tips
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
        P = [leaf(s, t, w) - Vector((0, 0, 0.042)) for t, w in ((0.02, 0.1), (0.25, 0.85), (0.6, 0.85), (0.80, 0.5),
                                                                  (0.86, 0.05), (0.5, 0.0))]   # tip clear of Tail3
        B.poly([P[5], P[0], P[1], P[2], P[3], P[4]], 0.014, ARMOR, hb)
        eye = leaf(s, 0.55, 0.40) - Vector((0, 0, 0.042))
        # review 3 C3: a DEMON EYE on the dark wing - pale rim -> deep -> ruby -> black slit pupil, 1.35 long
        for i, (r, c, sx, sy) in enumerate(((0.10, RUBY_HOT, 0.75, 1.35), (0.078, RUBY_D, 0.75, 1.35),
                                            (0.058, RUBY, 0.75, 1.35), (0.03, BLACK, 0.45, 1.4))):
            disc(B, eye, r, c, hb, sx=sx, sy=sy, thick=0.004, dz=0.007 + 0.002 * i)   # top face + underside (FIX 7):
            disc(B, eye, r, c, hb, sx=sx, sy=sy, thick=0.004, dz=-(0.007 + 0.002 * i))  # thin stepped rings, clear of
            # the tegmina
            # above (their landing cut the old 0.012 stacks) and of the abdomen below
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
            B.spike(base + dv * L * 0.5, dv, L * 0.6, 0.02, RUBY, "Chest", studs=[], nostud=True)
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
    B.add(HC + Vector((0, -0.083, -0.15)), (0.03, 0.008, 0.016), ARMOR, "Head", studs=[], role="detail",
          bevel=0.004)                                                                         # mouth plate
    for s, side in ((1, "L"), (-1, "R")):                                                     # FIX 0: own side
        from mathutils import Euler
        e = HC + Vector((s * 0.165, -0.02, 0.075))                                             # FIX 2: ruby DOMES
        Re = Euler((0, math.radians(s * 12), math.radians(s * 18)), "XYZ").to_matrix()          # (lathed ovals)
        ellipsoid(B, e + Re @ Vector((-s * 0.004, 0.014, -0.012)), (0.066, 0.064, 0.084), RUBY_D, "Head", Re, n=24,
                  rings=14)                                                     # deep crescent tucked back + low
        eb, axb = e + Vector((s * 0.006, -0.008, 0.006)), (0.069, 0.067, 0.089)                   # ruby body (bigger)
        ellipsoid(B, eb, axb, RUBY, "Head", Re, n=24, rings=14)
        ellipsoid(B, on_surf(eb, axb, Re, (-s * 0.5, -0.86, -0.16), 0.95), (0.009, 0.012, 0.032), BLACK, "Head", Re,
                  n=12, rings=6)                                                # pupil: inner-front, under the lid
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
    B.add(HC + Vector((0, 0, 0.12)), (0.09, 0.06, 0.032), GOLD, "Head", top=(0.85, 0.85), role="limb", bevel=0.01,
          nostud=True)
    cb, cd = HC + Vector((0, 0, 0.14)), Vector((0, 0.25, 1)).normalized()
    B.spike(cb, cd, 0.34, 0.065, GOLD, "Head", top=(0.12, 0.12), nostud=True)                  # polished gold spire
    for f in (0.35, 0.65):                                                                      # S5: ornament rings
        w = 0.065 * (1 - 0.88 * f) + 0.008
        B.add(cb + cd * 0.34 * f, (w, w, 0.012), GOLD_D, "Head", R=__import__("blockkit").frame_from(
              cb, cb + cd, Vector((1, 0, 0))), studs=[], nostud=True, role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike(HC + Vector((s * 0.055, 0, 0.14)), (s * 0.5, 0.2, 1), 0.18, 0.042, GOLD, "Head", top=(0.12, 0.12),
                nostud=True)
    B.spike(HC + Vector((0, 0.02, 0.19)), (0, 0.35, 1), 0.16, 0.03, GOLD_D, "Head", top=(0.3, 0.3),
            nostud=True)                                                                         # cone keel
    gem_inlay(B, HC + Vector((0, -0.064, 0.12)), (0, -1, 0), 0.034, "Head")                    # M4 front jewel
    B.add(HC + Vector((0, 0.062, 0.115)), (0.07, 0.012, 0.03), GOLD, "Head", role="limb", bevel=0.006,
          nostud=True)                                                                           # back plate
    gem_inlay(B, HC + Vector((0, 0.076, 0.115)), (0, 1, 0), 0.026, "Head")                     # back jewel (game cam)
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
        B.spike(F1 + Vector((0, 0, 0.03)), (s * 0.7, 0.5, 0.5), 0.11, 0.032, GOLD, fore, top=(0.12, 0.12),
                nostud=True)                                                                         # knee spine
        td = (T1 - F1).normalized()
        B.seg(F1, T1, 0.032, 0.042, GOLD, blade, ext=0.02, top=(0.7, 0.6), nostud=True)              # gold tibia
        tedge = (fwd - td * fwd.dot(td)).normalized()
        hd_ = (td * 0.3 - tedge * 0.95).normalized()
        B.spike(T1 - td * 0.01, hd_, 0.08, 0.028, GOLD, blade, top=(0.3, 0.3), nostud=True)          # hook
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
    k.joint("Strike", tuple(HC + Vector((0, -0.45, -0.25))), "Chest", tail=(0, -0.2, 0))   # strike VFX anchor (moved
    k.joint("Crown", (0, -0.437, 1.61), "Head", tail=(0, 0.02, 0.08))                      # after keying, review 2)
    for s, side in ((1, "L"), (-1, "R")):
        C0, C1, F1, T1 = (X(p, s) for p in ARM)
        k.joint("Antenna_" + side, tuple(HC + Vector((s * ANT0[0], ANT0[1], ANT0[2]))), "Head",
                tail=(s * ANT1[0], ANT1[1], ANT1[2]))
        k.joint("Arm_" + side, tuple(C0), "Chest")
        k.joint("Fore_" + side, tuple(C1), "Arm_" + side)
        k.joint("Blade_" + side, tuple(F1), "Fore_" + side, tail=tuple(T1 - F1))
        k.joint("Elytra_" + side, tuple(X(WROOT, s)), "Spine", tail=(0, 0.5, 0.02))
        k.joint("Wing_" + side, tuple(X(WROOT, s) - Vector((0, 0, 0.02))), "Spine", tail=(0, 0.5, 0.02))
        k.joint("EyeSpot_" + side, tuple(leaf(s, 0.55, 0.40) - Vector((0, 0, 0.042))), "Wing_" + side,
                tail=(0, 0, -0.06))                                                      # hindwing eye-spot VFX
        F1v, T1v = Vector(F1), Vector(T1)
        td = (T1v - F1v).normalized()
        te = (Vector((0, -1, 0)) - td * Vector((0, -1, 0)).dot(td)).normalized()
        hd_ = (td * 0.3 - te * 0.95).normalized()
        tip = T1v - td * 0.01 + hd_ * 0.075 + (hd_ + td * 0.3).normalized() * 0.05
        k.joint("BladeTip_" + side, tuple(tip), "Blade_" + side, tail=tuple(hd_ * 0.05))   # claw tip VFX
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
              ("Wing_" + s, "Elytra_" + s), ("Shin_B" + s, "Tail2"), ("Shin_B" + s, "Tail3"),
              ("Wing_" + s, "Tail1"), ("Wing_" + s, "Tail2"), ("Wing_" + s, "Tail3")]
    P += [("Fore_L", "Fore_R"), ("Blade_L", "Blade_R"), ("Fore_L", "Blade_R"), ("Fore_R", "Blade_L"),
          ("Elytra_L", "Elytra_R"), ("Wing_L", "Wing_R"), ("Head", "Chest"), ("Elytra_L", "Wing_R"),
          ("Elytra_R", "Wing_L")]
    for s in ("L", "R"):                                                               # review 2 M5
        P += [("Elytra_" + s, "Chest"), ("Wing_" + s, "Chest"), ("Fore_" + s, "Chest"), ("Fore_" + s, "Leg_F" + s),
              ("Blade_" + s, "Leg_F" + s), ("Antenna_" + s, "Blade_" + s), ("Antenna_" + s, "Fore_" + s)]
    return P


def joints():
    # wing articulation strip: tegmina and hindwings hinge 0.02 apart along the thorax side, so the fan's roots cross
    # there (pose_try: every crossing of the display fan lies within 0.07 of this axis)
    return [(tuple(X(WROOT, s)), tuple(X(WROOT + Vector((0.02, 0.20, -0.005)), s)), 0.07, "Wing_" + side)
            for s, side in ((1, "L"), (-1, "R"))]


HEAD_XF = []


# ------------------------------------------------------------------ animation (review 2 section 4 brief)
# References (owner rule; notes in _review/ANIM_REFERENCES_1014.md #3, #5-7):
# - "Attack" (combat study set): body coils f6-11, the hand is COCKED and held 3 f (f12-14), the 2 f SNAP (smear f15,
#   full reach f16), then a 5 f follow-through hold -> our 4 f tell, 2 f snap, hard stop.
# - Monsters University scare pop: crouch 5 f -> explode into the arms-wide spread in 5-7 f -> hold (roar display).
# - How to Train Your Dragon forest approach: step / freeze / scan with the head moving while the body is still (the
#   predator head-lock in idle + lock-on).
# - Sea Beasts heavy-head roar: the jaw lags the head lift.
# The helpers take SEMANTIC values (up / tuck / open / curl / back) and convert them to kit signs: kit pitch + = nose
# down for -Y bones, LIFTS +Y bones (abdomen, tegmina), swings a down-pointing bone's tip BACK, tips a +Z bone FORWARD.
# ARM RULE (review 2): whenever the arm is raised (up) more than 5 deg it must already be yawed OUT >= 12 deg (else the
# gold knee spine drives into the eye dome) - every raise below leads with the yaw by >= 2 f.
# No head shakes: every head roll is one tilt, a hold and a return.
import petkit as pk
import _common as cm


def body(k, f, z=0.0, x=0.0, y=0.0, pitch=0.0, yaw=0.0, roll=0.0, chest=0.0, chest_yaw=0.0):
    """Spine: pitch + = nose down (kit). chest + = the prothorax REARS up (lower = negative), -10 .. +12"""
    k.key("Spine", f, rot=(pitch, yaw, roll), loc=(x, y, z))
    k.key("Chest", f, rot=(-chest, chest_yaw, 0))


def head(k, f, up=0.0, yaw=0.0, roll=0.0, jaw=None):
    """up + = head raised (Neck takes a third, <= 8), yaw split Neck 30 / Head 70, ONE-sided rolls only; jaw + = open"""
    nk = max(-8.0, min(8.0, up / 3.0))
    k.key("Neck", f, rot=(-nk, yaw * 0.3, 0))
    k.key("Head", f, rot=(-(up - nk), yaw * 0.7, roll))
    if jaw is not None:
        k.key("Jaw", f, rot=(jaw, 0, 0))


def arm(k, f, side, up=0.0, out=0.0, fore=0.0, blade=0.0):
    """up + = raised (- = swung forward-down), out + = yawed outward, fore + = femur tucked back (- = extends),
    blade + = tibia OPEN (- = folded tighter)"""
    s = 1 if side == "L" else -1
    k.key("Arm_" + side, f, rot=(-up, s * out, 0))
    k.key("Fore_" + side, f, rot=(-fore, 0, 0))
    k.key("Blade_" + side, f, rot=(-blade, 0, 0))


def arms(k, f, **kw):
    arm(k, f, "L", **kw)
    arm(k, f, "R", **kw)


def wings(k, f, el=0.0, el_roll=0.0, wi=0.0, wi_roll=0.0, yaw=0.0, el_splay=0.0, wi_splay=0.0):
    """el / wi + = tegmina / hindwings RAISED (kit + lifts a +Y bone); *_roll + = twisted about the wing's own long
    axis (the kit applies roll BEFORE pitch, so it only turns the face); *_splay + = swung OUT into a V (mirrored yaw,
    applied after the raise); yaw = the folded wings ride the abdomen sway (see abdomen())"""
    for s, sd in ((1, "L"), (-1, "R")):
        k.key("Elytra_" + sd, f, rot=(el, yaw - s * el_splay, s * el_roll))
        k.key("Wing_" + sd, f, rot=(wi, yaw - s * wi_splay, s * wi_roll))


def abdomen(k, f, curl=(0.0, 0.0, 0.0), yaw=(0.0, 0.0, 0.0)):
    """curl + = the abdomen curls UP. Returns the yaw the folded wings need so their tips (lying on Tail3, 0.9 from
    the hinge) follow the abdomen's lateral sway there."""
    for b, c, yw in zip(TAIL, curl, yaw):
        k.key(b, f, rot=(c, yw, 0))
    return 1.1 * (0.70 * yaw[0] + 0.38 * yaw[1] + 0.08 * yaw[2]) / 0.9


def antennae(k, f, back=0.0, l=0.0, r=0.0):
    """back + = swept back (kit + tips a +Z bone forward); l / r = per-side flicks (+ = forward)"""
    k.key("Antenna_L", f, rot=(-back + l, 0, 0))
    k.key("Antenna_R", f, rot=(-back + r, 0, 0))


def rest(k, f):
    body(k, f)
    head(k, f, jaw=0.0)
    arms(k, f)
    wings(k, f)
    abdomen(k, f)
    antennae(k, f)


def plant_all(k, n, frames=None):
    cm.plant(k, n, LEGS4, frames)
    k.meta["planted"] = LEGS4


def ease(a, b, f0, f1, f):
    if f <= f0:
        return a
    if f >= f1:
        return b
    u = (f - f0) / float(f1 - f0)
    return a + (b - a) * u * u * (3 - 2 * u)


def groom(k, f, a):
    """review 3 C2: the LEFT blade is drawn through the jaws - tibia SHUT along the femur, the arm swings IN (no raise)
    so the upper tibia passes in front of the mandibles; the head turns down to meet it (head(up=-6, yaw=8) x a).
    pose_try: the review's out -18 / fore -6 / head -8 yaw 12 cuts Fore|Jaw (14 pairs); its fallback ladder
    (head -6, out -15) + the femur reaching 10 (fore -10) + yaw 8 is collision-free"""
    arm(k, f, "L", up=0.0, out=-15.0 * a, fore=-10.0 * a, blade=-5.0 * a)


def idle(k):
    """STILL HUNTER: leaf-sway (Spine roll +-3, x +-0.015, 40 f) with the head counter-rolling (gaze level); ONE
    predatory tilt (12 in 5 f, hold 25, back in 8); a left-blade groom with 2 chomps; alternating antenna flicks."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        w = pk.wave(f, n, 0.0, 3)
        body(k, f, x=0.015 * w, roll=3.0 * w)
        abdomen(k, f)                                           # (the Spine carries the sway; wings ride with it)
        wings(k, f)
        tilt = ease(0, 12, 18, 23, f) if f <= 48 else ease(12, 0, 48, 56, f)
        g = ease(0, 1, 62, 72, f) if f <= 92 else ease(1, 0, 92, 102, f)
        head(k, f, up=-6.0 * g, yaw=8.0 * g, roll=-3.0 * w + tilt)
    for f, jw in ((0, 0), (76, 0), (78, 10), (80, 0), (84, 0), (86, 10), (88, 0), (120, 0)):     # 2 chomps
        k.key("Jaw", f, rot=(jw, 0, 0))
    # groom: the LEFT blade rises to the mouth (no raise = no arm-rule risk: yaw IN + tibia open + femur tuck)
    for f, a in ((0, 0.0), (62, 0.0), (72, 1.0), (92, 1.0), (102, 0.0), (120, 0.0)):
        groom(k, f, a)
        arm(k, f, "R")
    for f, l, r in ((0, 0, 0), (30, 0, 0), (33, 12, 0), (36, 0, 0), (40, 0, 12), (43, 0, 0), (104, 0, 0), (107, 12, 0),
                    (110, 0, 0), (120, 0, 0)):                                            # antenna flicks (3 f)
        antennae(k, f, l=l, r=r)
    plant_all(k, n)
    k.finish()
    k.events["idle"] = {"groom": round(78 / n, 3)}


def walk(k):
    """JERKY STALK: diagonal pairs (FL+BR / FR+BL), duty 0.6; a low leaf-rock layer (Spine roll +-1.5, 2 per cycle);
    Chest counter-yaws the Spine; the head is world-stable with a small lag; blades folded with a 2 deg counter-swing;
    the abdomen lags 2-3 f."""
    n = 32

    def bk(f):
        sy = 2.0 * pk.wave(f, n, 0.0)
        sr = 1.5 * pk.wave(f, n, 0.1, 2)
        body(k, f, z=0.006 * pk.wave(f, n, 0.15, 2), yaw=sy, roll=sr, chest_yaw=-0.8 * sy)
        head(k, f, yaw=-0.2 * sy - 1.0 * pk.wave(f, n, -0.08), roll=-0.6 * sr, jaw=0.0)
        for side, sgn in (("L", 1), ("R", -1)):
            arm(k, f, side, up=-2.0 * sgn * pk.wave(f, n, 0.25))
        abdomen(k, f)                       # the folded tegmina lie interleaved with the abdomen tip: they move as one
        wings(k, f)
        antennae(k, f, l=4.0 * pk.wave(f, n, 0.3), r=4.0 * pk.wave(f, n, 0.8))
    return cm.quad_walk(k, n, 0.07, 0.045, bk, gait="trot", duty=0.6)


# hindwing fan path (pose_try, every waypoint 0 cut-throughs vs the raised tegmina): spread SIDEWAYS while low, then
# lift at full splay (half-splayed at full height the hindwing slices the tegmen); the fold runs it backwards
HIND = [(0.0, 0, 0, 0), (0.06, 6, 0, 0), (0.11, 11, 6, 4), (0.17, 20, 15, 10),     # pure lift off the abdomen first
        (0.25, 27, 27, 20), (0.36, 35, 40, 30), (0.45, 38, 50, 37),
        (0.55, 39, 62, 46), (0.64, 42, 68, 50), (0.71, 44, 70, 51), (0.78, 46, 72, 52), (0.85, 50, 72, 52),
        (0.93, 54, 72, 52), (1.0, 58, 72, 52)]


def hind_path(u):
    u = max(0.0, min(1.0, u))
    for (u0, *a), (u1, *b) in zip(HIND, HIND[1:]):
        if u <= u1:
            t = (u - u0) / (u1 - u0)
            return tuple(x + (y - x) * t for x, y in zip(a, b))
    return tuple(HIND[-1][1:])


def roar(k):
    """DEIMATIC DISPLAY (90 f): crouch -> rear -> tegmina V + hindwing eye-spot fan + arms spread with the gold tibiae
    open (`display` f24) -> hold with wing shiver, 2 mandible clacks, 2 blade pumps -> hindwings fold FIRST, then the
    tegmina close over them -> settle."""
    n = 90
    k.new_action("roar", n, False)
    for f in range(0, n + 1, 2):
        if f <= 10:
            u = f / 10.0
            z, p, ch, hu = -0.04 * u, 4.0 * u, -6.0 * u, -6.0 * u
        elif f <= 20:                                  # head-lock: the body rears 22, the head stays on the threat
            z, p, ch, hu = ease(-0.04, 0.035, 10, 20, f), ease(4, -10, 10, 20, f), ease(-6, 12, 10, 20, f), \
                ease(-6, -4, 10, 20, f)
        elif f <= 60:
            z, p, ch, hu = 0.035, -10.0, 12.0, -4.0
        elif f <= 76:
            z, p, ch, hu = ease(0.035, 0.0, 60, 76, f), ease(-10, 0, 60, 76, f), ease(12, 0, 60, 76, f), \
                ease(-4, 0, 60, 76, f)
        else:
            z, p, ch, hu = -0.01 * math.sin(math.pi * (f - 76) / 14.0), 0.0, 0.0, 0.0
        rock = 2.0 * math.sin(2 * math.pi * (f - 26) / 17.0) if 26 <= f <= 60 else 0.0
        body(k, f, z=z, pitch=p, roll=rock, chest=ch)
        head(k, f, up=hu)
        # raise: pitch leads (the wings are clear of each other above ~6 deg) and the splay / twist follow; fold:
        # splay / twist go to 0 FIRST, then pure pitch down (a twisted wing near rest slices its stacked partner)
        te = ease(0, 1, 14, 20, f) if f <= 60 else ease(1, 0, 70, 78, f)          # tegmina pitch: up first, land last
        ter = ease(0, 1, 16, 22, f) if f <= 60 else ease(1, 0, 68, 72, f)         # tegmina splay / twist
        hu = ease(0, 1, 17, 27, f) if f <= 60 else ease(1, 0, 60, 70, f)          # hindwing path progress
        hp, hs, hr = hind_path(hu)
        shiver = (3.0 if (f // 3) % 2 == 0 else -3.0) if 26 <= f <= 58 else 0.0
        wings(k, f, el=66 * te, el_splay=10 * ter, el_roll=6 * ter, wi=hp, wi_splay=hs, wi_roll=hr + shiver)
        cu = ease(0, 1, 20, 28, f) if f <= 52 else ease(1, 0, 52, 60, f)    # curl only while the hindwings are up
        abdomen(k, f, curl=(8 * cu, 12 * cu, 16 * cu))
        # arms: tuck in the crouch, OUT 30 from f16, UP 20 only from f18 (arm rule), tibiae open 75 by f24, pumps,
        # then lower FIRST (up 0 by f66) and un-yaw after (out 0 by f70), blades folded by f72
        tuck = ease(0, 8, 0, 10, f) if f <= 16 else ease(8, 0, 16, 24, f)
        out = ease(0, 30, 16, 20, f) if f <= 60 else ease(30, 0, 64, 70, f)
        up = ease(0, 20, 18, 24, f) if f <= 60 else ease(20, 0, 60, 66, f)
        bl = ease(0, 75, 18, 24, f) if f <= 60 else ease(75, 0, 60, 72, f)
        if 38 <= f <= 42:
            bl = 75 - 15 * math.sin(math.pi * (f - 38) / 4.0)
        if 50 <= f <= 54:
            bl = 75 - 15 * math.sin(math.pi * (f - 50) / 4.0)
        arms(k, f, up=up, out=out, fore=tuck, blade=bl)
        antennae(k, f, back=ease(0, 25, 0, 10, f) if f <= 60 else ease(25, 0, 60, 76, f),
                 l=(6.0 if f in (40, 52) else 0.0), r=(6.0 if f == 46 else 0.0))
    for f, jw in ((0, 0), (20, 0), (24, 18), (33, 18), (34, 4), (36, 18), (43, 18), (44, 4), (46, 18), (60, 18),
                  (70, 0), (90, 0)):                         # jaw opens a beat after the head lift, clacks f34 / f44
        k.key("Jaw", f, rot=(jw, 0, 0))
    plant_all(k, n)
    k.finish(loop=False)
    k.events["roar"] = {"display": round(24 / n, 3), "clack1": round(34 / n, 3), "clack2": round(44 / n, 3)}


def act_thornstrike(k):
    """THORN STRIKE (100 f, review 3 C1): lock-on peering (head locked) -> COCK the scythes high beside the head (knee
    spines above the eye tops) + 4 f TELL with a blade tremble -> STRIKE 1: the whole foreleg shoots FORWARD nearly
    straight (knee 165 deg, tips 0.55 in front of the head at chest height) -> SNAP shut -> recoil to a half-cock ->
    STRIKE 2: the arms sweep in + down into a gold X in front of the chest (L leads 1 f, passes 0.07 higher) ->
    executioner hold (tibiae close 7 deg = the clutch; fully shut tibiae fold back along the femurs and can only cross
    with the elbows meeting at the midline) with ONE head tilt -> prayer -> groom (eased in) -> settle.
    Poses solved in world space with _tools/mantis_fk.py and checked collision-free in pose_try."""
    n = 100
    k.new_action("act_thornstrike", n, False)
    rest(k, 0)
    Bd = [  # f, z, x, y, pitch, chest, head_up
        (4, 0.0, 0.025, 0.0, 0, -8, -8), (9, 0.0, -0.025, 0.0, 0, -8, -8), (14, 0.0, 0.0, 0.0, 0, -8, -8),
        (20, -0.03, 0.0, 0.03, 0, -8, -8), (24, -0.03, 0.0, 0.03, 0, -8, -8),                # cock: weight back
        (25, -0.02, 0.0, -0.05, 3, -10, -8), (27, -0.02, 0.0, -0.05, 3, -10, -8),            # strike 1 / snap
        (31, -0.02, 0.0, -0.03, 2, -8, -8), (33, -0.02, 0.0, -0.03, 2, -8, -8),               # recoil
        (34, -0.02, 0.0, -0.05, 3, -6, -10), (36, -0.02, 0.0, -0.05, 3, -6, -10),            # strike 2 (X)
        (50, -0.02, 0.0, -0.05, 3, -6, -10), (60, 0.0, 0.0, 0.0, 0, -4, -8),                 # hold -> prayer
        (66, 0.0, 0.0, 0.0, 0, -4, -6), (72, 0.0, 0.0, 0.0, 0, -4, -6),                      # groom
        (80, 0.0, 0.0, 0.0, 0, -2, -4), (86, -0.008, 0.0, 0.0, 0, 0, 0), (92, 0.0, 0.0, 0.0, 0, 0, 0),
        (100, 0.0, 0.0, 0.0, 0, 0, 0)]
    for f, z, x, y, p, ch, hu in Bd:
        body(k, f, z=z, x=x, y=y, pitch=p, chest=ch)
        gy = 8.0 if 66 <= f <= 72 else 0.0                                       # the head turns to the groom
        head(k, f, up=hu, yaw=gy, roll=ease(0, 12, 36, 40, f) if f <= 60 else ease(12, 0, 72, 80, f))
    # f, (up, out, fore, blade) L, (up, out, fore, blade) R  - semantic arm values (see arm())
    A = [(14, (0, 0, 0, 0), (0, 0, 0, 0)),
         (16, (0, 20, 0, -6), (0, 20, 0, -6)),                                    # OUT first (arm rule) ...
         (18, (40, 26, -15, -10), (40, 26, -15, -10)),                            # ... then the big raise
         (20, (70, 26, -30, -10), (70, 26, -30, -10)),                            # COCKED: knee spines z 1.29
         (22, (70, 26, -30, -11), (70, 26, -30, -11)), (24, (70, 26, -30, -9), (70, 26, -30, -9)),   # tell tremble
         (25, (-40, 6, 8, 130), (-40, 6, 8, 130)),                               # STRIKE 1: reach (tips z 0.70)
         (27, (-25, 6, 25, 10), (-25, 6, 25, 10)),                               # SNAP shut, femurs back halfway
         (29, (-6, 12, 15, 6), (-6, 12, 15, 6)), (31, (12, 18, 10, 4), (12, 18, 10, 4)),   # recoil: half-cock
         (33, (12, 18, 10, 4), (12, 18, 10, 4)),
         (34, (-28, -22, 10, 85), None),                                          # STRIKE 2: L leads ...
         (35, (-28, -22, 10, 85), (-40, -22, 10, 95)),                            # ... R 1 f later, 0.07 lower
         (36, (-26, -22, 10, 78), (-42, -22, 10, 92)),                            # executioner hold (clutch)
         (50, (-26, -22, 10, 76), (-42, -22, 10, 90)),
         # un-cross in reverse arrival order (both together cut): R DROPS back first (pose_try: swinging it out
         # level at up -42 cuts L's tibia, at up -50 it is clear), slips out, then L leaves
         (51, (-26, -22, 10, 76), (-50, -22, 10, 90)), (52, (-26, -22, 10, 76), (-50, -10, 10, 90)),
         (53, (-26, -22, 10, 76), (-50, 0, 10, 70)), (54, (-26, -22, 10, 76), None),
         (55, None, (-30, 4, 8, 60)),
         (57, (-10, 14, 6, 30), (-10, 14, 6, 30)),
         (60, (0, 0, 0, 0), (0, 0, 0, 0))]
    arms(k, 0)
    for f, l, r in A:
        for side, v in (("L", l), ("R", r)):
            if v is not None:
                arm(k, f, side, up=v[0], out=v[1], fore=v[2], blade=v[3])
    for f, a in ((66, 1.0), (72, 1.0), (78, 0.0), (100, 0.0)):                   # groom (left blade), eased in
        groom(k, f, a)                                                           # from the f60 prayer key
        arm(k, f, "R")
    for f, jw in ((0, 0), (34, 0), (36, 15), (50, 15), (58, 0), (66, 0), (67, 10), (69, 0), (70, 0), (71, 10),
                  (73, 0), (100, 0)):
        k.key("Jaw", f, rot=(jw, 0, 0))
    for f, bk_, l, r in ((0, 0, 0, 0), (6, -12, 0, 0), (60, -12, 0, 0), (72, 0, 0, 0), (80, 0, 10, 0), (83, 0, 0, 0),
                         (100, 0, 0, 0)):
        antennae(k, f, back=bk_, l=l, r=r)
    rest(k, n)
    plant_all(k, n)
    k.finish(loop=False)
    k.events["act_thornstrike"] = {"lockon": round(6 / n, 3), "strike1": round(25 / n, 3), "strike2": round(34 / n, 3),
                                   "finish": round(36 / n, 3), "groom": round(66 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    act_thornstrike(k)
    return stride
