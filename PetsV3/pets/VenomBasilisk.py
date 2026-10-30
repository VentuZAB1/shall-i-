# Venom Basilisk v2 (Wood/Grass egg, NEW 5% pet, 2026-10-14) - FIERCE style "the serpent king's herald" (review 1
# brief): a sprawled jungle lizard built from tapered blocks under a Roblox stud skin. Value structure: dark DORSAL
# shells over the back / neck / tail top with stripe teeth growing down the flanks, a true-green hide, a pale belly.
# HERO: the ROYAL CROWN FRILL - 7 bone-tipped spines (deep-violet shafts) fanned round the back of a VIPER ARROWHEAD
# head with two-tone membranes (deep root band, light-violet outer band); split into Frill + Frill_L/R so the hiss
# really flares it. A darker basilisk back sail behind it, one horned-viper horn per side, lilac slit eyes, ivory
# sabre fangs with venom tips hanging outside the lip, a forked light-violet tongue (Tongue bone, slides out through
# the lip gap with a 3-4 deg jaw open), banded whip tail ending in a small violet tail-frill. No gold, no glow.
# Review 2 (2026-10-14): 7-point frill + hidden under-flaps, pale under-shells, fanned violet sail, scute seams.
# Old version: _tools/rex_versions/VenomBasilisk_v1.py
import math
from mathutils import Vector, Matrix

DISPLAY = "Venom Basilisk"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.0        # total height (frill tips) in studs at x1 - between Mossback (7) and Treant (10)

# Blender colours (Roblox renders ~0.6x darker) - review 1 palette
HIDE = (52, 144, 66)         # true green hide (lum 0.47)
DORSAL = (22, 72, 44)        # back shells, stripes, head V, neck / tail top, socks, body thorn shafts
PALE = (224, 228, 150)       # throat, chin, belly band, tail underside
PALE_D = (176, 186, 108)     # belly scute gaps
SEAM = (40, 104, 64)         # transverse scute seams on the dorsal shells
VENOM_DEEP = (92, 30, 146)   # sail membrane, frill shafts, frill inner band
VENOM = (198, 78, 255)       # fang tips, sail top edge
VENOM_L = (222, 128, 255)    # frill outer membrane, tail-frill, tongue
EYE = (232, 170, 255)        # eye slit
VENOM_HOT = (246, 214, 255)  # eye highlight
IVORY = (240, 234, 210)      # spine points, teeth, fangs
BLACK = (14, 14, 22)
MOUTH = (96, 20, 62)

LEGS = {"F": ((0.20, -0.40, 0.50), (0.42, -0.33, 0.30), (0.40, -0.44, 0.09), (0.40, -0.50, 0.04)),
        "B": ((0.20, 0.34, 0.50), (0.43, 0.24, 0.32), (0.42, 0.44, 0.12), (0.42, 0.38, 0.04))}
NECKP = [(0, -0.50, 0.60), (0, -0.68, 0.70), (0, -0.80, 0.74)]          # Neck, Neck2, Head (throat pivot)
TAILP = [(0, 0.52, 0.54), (0, 0.80, 0.47), (0, 1.06, 0.40), (0, 1.30, 0.35), (0, 1.50, 0.32)]
FRILL0 = Vector((0, -0.80, 0.86))       # frill root (back of the skull top)
FRILL_TILT = 12.0                       # modelled lean-back of the fan (deg): faces the high-behind game camera
FRILL_A = (-84, -58, -30, 0, 30, 58, 84)
FRILL_L = (0.38, 0.46, 0.52, 0.56, 0.52, 0.46, 0.38)
FRILL_BONE = ("Frill_R", "Frill_R", "Frill", "Frill", "Frill", "Frill_L", "Frill_L")


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


# ------------------------------------------------------------------ helpers (Ivonrath / MoltenBoar / Thunder Rex)
def prof(b, lz):
    t = (lz / b.h.z + 1) / 2
    fx = b.bot[0] + (b.top[0] - b.bot[0]) * t
    fy = b.bot[1] + (b.top[1] - b.bot[1]) * t
    return b.h.x * fx, b.h.y * fy, b.ts[1] * t


def shell(B, b, y0, y1, za, color, pad=0.024, bone=None, rnd=0.30, lift=0.0, **kw):
    """armour shell over body block b: local y range [y0, y1], local z from za up to the top (MoltenBoar)"""
    xa, ya, oa = prof(b, za)
    xb, yb, ob = prof(b, b.h.z)
    zb = b.h.z + pad + lift
    lo_a, hi_a = max(y0 + oa, oa - ya - pad), min(y1 + oa, oa + ya + pad)
    lo_b, hi_b = max(y0 + ob, ob - yb - pad), min(y1 + ob, ob + yb + pad)
    cy, hy = (lo_a + hi_a) / 2, (hi_a - lo_a) / 2
    hx = xa + pad
    c = b.world(Vector((0, cy, (za + zb) / 2)))
    return B.add(c, (hx, hy, (zb - za) / 2), color, bone or b.bone, R=b.R,
                 top=((xb + pad) / hx, (hi_b - lo_b) / 2 / hy), top_shift=(0, (lo_b + hi_b) / 2 - cy), rnd=rnd, **kw)


def ushell(B, b, zt, color, pad=0.012, rnd=0.30, **kw):
    """pale under-shell over body block b: local z from the bottom (-h.z - pad) up to zt (mirror of shell())"""
    xt, yt, ot = prof(b, zt)
    xb, yb, ob = prof(b, -b.h.z)
    z0 = -b.h.z - pad
    hz = (zt - z0) / 2
    c = b.world(Vector((0, ob, (zt + z0) / 2)))
    return B.add(c, (xb + pad, yb + pad, hz), color, b.bone, R=b.R,
                 top=((xt + pad) / (xb + pad), (yt + pad) / (yb + pad)), top_shift=(0, ot - ob), rnd=rnd, **kw)


def side_pt(b, s, ly, lz, off=0.006):
    hx, _, oy = prof(b, lz)
    p = b.world(Vector((s * (hx + off), ly + oy, lz)))
    dx = b.h.x * (b.top[0] - b.bot[0]) / (2 * b.h.z)
    n = (b.R @ Vector((s, 0, -dx))).normalized()
    return p, n


def surf_hit(B, blks, origin, direction):
    """exact hit point + normal on the bevelled meshes of `blks` (seats inlays ON tapered / rounded faces)"""
    import blockkit as bk
    from mathutils.bvhtree import BVHTree
    B._resolve()
    best = None
    d = Vector(direction).normalized()
    for blk in blks:
        bm = bk._box_bm(blk)
        t = BVHTree.FromBMesh(bm)
        bm.free()
        loc, nrm, _, dist = t.ray_cast(Vector(origin), d)
        if loc is not None and (best is None or dist < best[2]):
            best = (loc, nrm.normalized(), dist)
    if best is None:
        raise RuntimeError("surf_hit: no surface from %s" % (tuple(origin),))
    return best[0], best[1]


def surf_strip(B, blks, origins, direction, width, thick, color, bone, proud=0.009, tip0=False, tip1=False, **kw):
    """flush strip of bars along a surface: ray-cast every origin along direction, bars between the hits"""
    hits = [surf_hit(B, blks, o, direction) for o in origins]
    kw.setdefault("studs", [])
    kw.setdefault("bevel", 0.004)
    out = []
    for i in range(len(hits) - 1):
        (a, na), (b, nb) = hits[i], hits[i + 1]
        n = (na + nb).normalized()
        a2, b2 = a + n * (proud - thick), b + n * (proud - thick)
        if tip0 and i == 0:
            out.append(B.bar(b2, a2, n, width, thick, color, bone, top=(1, 0.15), **kw))
        elif tip1 and i == len(hits) - 2:
            out.append(B.bar(a2, b2, n, width, thick, color, bone, top=(1, 0.15), **kw))
        else:
            out.append(B.bar(a2, b2, n, width, thick, color, bone, **kw))
    return out


def fierce_eye(B, c, s, bone="Head", yaw=30.0, tilt=18.0, sc=1.15, brow_out=0.012):
    """black socket (inner corner down) -> lilac slit -> hot highlight, vertical reptile pupil, heavy dark brow"""
    from mathutils import Euler
    R = Euler((0, math.radians(-s * tilt), math.radians(s * yaw)), "XYZ").to_matrix()
    n = R @ Vector((0, -1, 0))
    c = Vector(c)
    B.add(c, (0.052 * sc, 0.008, 0.025 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0135 * sc), EYE, bone, R=R, studs=[], role="detail", bevel=0.003)
    B.add(c + n * 0.011 + R @ Vector((s * 0.022 * sc, 0, 0.002)), (0.014 * sc, 0.004, 0.006 * sc), VENOM_HOT, bone,
          R=R, studs=[], role="detail", bevel=0.002)
    B.add(c + n * 0.011 + R @ Vector((-s * 0.004, 0, 0)), (0.006 * sc, 0.004, 0.0135 * sc), BLACK, bone, R=R,
          studs=[], role="detail", bevel=0.002)
    Rb = Euler((0, math.radians(-s * 20), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.040 * sc)) + n * brow_out, (0.066 * sc, 0.03, 0.024 * sc), DORSAL, bone, R=Rb,
          role="detail", bevel=0.01)


def thorn(B, root, d, L, w, bone, col=DORSAL):
    """one thorn spine: shaft (0 -> 0.68 L) + ivory point (0.62 L -> L), flat-sided like Ivonrath's crests"""
    import blockkit as bk
    d = Vector(d).normalized()
    root = Vector(root)
    R = bk.frame_from(root, root + d, (1, 0, 0) if abs(d.x) < 0.7 else (0, 1, 0))
    B.add(root + d * L * 0.34, (w * 0.55, w, L * 0.34), col, bone, R=R, top=(0.7, 0.62), role="limb")
    B.add(root + d * L * 0.81, (w * 0.55 * 0.7, w * 0.62, L * 0.19), IVORY, bone, R=R, top=(0.12, 0.1), role="limb",
          studs=[], nostud=True)
    return root + d * L


def web(B, roots, tips, thick, colors, bones, scallop=0.12, reach=0.86, inner=0.35):
    """membrane between neighbouring spines: an inner band (root -> inner of the length, colors[0]) and an outer band
    (inner -> reach, colors[1], gently scalloped); bones = one bone per panel (str = all panels)"""
    n = len(roots) - 1
    for i in range(n):
        r0, t0, r1, t1 = roots[i], tips[i], roots[i + 1], tips[i + 1]
        bone = bones if isinstance(bones, str) else bones[i]
        a, b = r0.lerp(t0, reach), r1.lerp(t1, reach)
        i0, i1 = r0.lerp(t0, inner), r1.lerp(t1, inner)
        notch = a.lerp(b, 0.5).lerp(i0.lerp(i1, 0.5), scallop)
        if inner > 0.01:
            B.poly([r0.lerp(r1, 0.5), r0, i0, i1, r1], thick, colors[0], bone)
            B.poly([i0.lerp(i1, 0.5), i0, a, notch, b, i1], thick, colors[1], bone)
        else:
            B.poly([r0.lerp(r1, 0.5), r0, a, notch, b, r1], thick, colors[1], bone)


def frill_dirs():
    """fan directions of the crown frill: in-plane angle a (0 = straight up), plane leaned back FRILL_TILT deg, the
    outer spines swept back more (cupped ruff)"""
    T = math.radians(FRILL_TILT)
    out = []
    for a in FRILL_A:
        ar = math.radians(a)
        u = Vector((math.sin(ar), 0, math.cos(ar)))
        d = Vector((u.x, u.z * math.sin(T) + 0.16 + 0.42 * abs(u.x), u.z * math.cos(T))).normalized()
        out.append((u, d))
    return out


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=503, tier=3, plates=False)
    # ================= torso (+10 % width): low ribcage tapering underneath, tucked waist, heavy hips
    chest = B.add((0, -0.24, 0.52), (0.245, 0.30, 0.19), HIDE, "Chest", bot=(0.70, 0.60), top=(0.88, 0.95), rnd=0.30)
    B.seg((0, -0.10, 0.36), (0, 0.26, 0.44), 0.165, 0.07, PALE, "Spine", top=(0.82, 0.75), side=(1, 0, 0))   # tuck
    waist = B.add((0, 0.10, 0.53), (0.19, 0.20, 0.14), HIDE, "Spine", bot=(0.74, 0.72), top=(0.95, 1), rnd=0.30)
    hips = B.add((0, 0.34, 0.53), (0.21, 0.20, 0.15), HIDE, "Spine", rot=(-6, 0, 0), top=(0.84, 0.90), bot=(0.85, 0.9))
    torso = [chest, waist, hips]
    # DORSAL shells over the back (top + upper ~35 % of the flank)
    shells = [shell(B, b, -b.h.y, b.h.y, 0.30 * b.h.z, DORSAL, rnd=0.42) for b in torso]
    # pale under-shells (one clean cream form per block, up to -0.50 h.z) with PALE_D scute gaps on the flanks
    for b in torso:
        ub = ushell(B, b, -0.50 * b.h.z, PALE)
        for s in (1, -1):
            for f in (-0.55, -0.18, 0.18, 0.55):
                a, n = side_pt(ub, s, f * ub.h.y, ub.h.z * 0.75, off=0.004)
                c, n2 = side_pt(ub, s, f * ub.h.y, -ub.h.z * 0.6, off=0.004)
                B.bar(a, c, (n + n2).normalized(), 0.014, 0.008, PALE_D, b.bone, studs=[], bevel=0.003)
    # transverse scute seams across the dorsal shells (lighter dorsal, between the stripe teeth)
    for y in (-0.29, -0.07, 0.15, 0.31):
        b = chest if y < -0.05 else waist if y < 0.24 else hips
        hw = b.h.x * 0.8
        surf_strip(B, shells, [(x, y, 2.0) for x in (-hw, -hw * 0.5, 0.0, hw * 0.5, hw)], (0, 0, -1), 0.018, 0.010,
                   SEAM, b.bone, proud=0.006)
    # stripe teeth growing down the flanks from the shells (4 per side, slanted back 25 deg)
    for s in (1, -1):
        for y, b in ((-0.40, chest), (-0.18, chest), (0.04, waist), (0.26, hips)):
            ly = y - b.c.y
            za = 0.30 * b.h.z
            L = 0.80 * b.h.z - 0.02                      # tip ends 0.02 above the pale under-shell
            P = [side_pt(b, s, ly + dy, lz, off=0.008)[0] for dy, lz in
                 ((0.0, za + 0.03), (-0.05, za + 0.03), (-0.035, za - 0.41 * L), (0.09 * L / 0.22, za - L),
                  (0.05, za - 0.41 * L), (0.05, za + 0.03))]
            B.poly([P[0].lerp(P[3], 0.35)] + P[1:] + [P[1]], 0.016, DORSAL, b.bone)
    # ================= serpent neck (Neck + Neck2 pinch), pale throat, DORSAL top strip
    N0, N1, N2 = (Vector(p) for p in NECKP)
    B.seg(N0 + Vector((0, 0.04, -0.04)), N1, 0.15, 0.13, HIDE, "Neck", ext=0.06, ext1=0.03)
    B.seg(N1, N2 + Vector((0, -0.02, 0.03)), 0.12, 0.11, HIDE, "Neck2", ext=0.04, ext1=0.03)
    B.seg((0, -0.52, 0.475), (0, -0.74, 0.615), 0.10, 0.045, PALE, "Neck", ext=0.02)
    B.seg((0, -0.73, 0.61), (0, -0.84, 0.655), 0.085, 0.04, PALE, "Neck2", ext=0.02)
    for p0, p1, w, bone in (((0, -0.40, 0.675), (0, -0.62, 0.815), 0.11, "Neck"),
                            ((0, -0.64, 0.805), (0, -0.78, 0.875), 0.09, "Neck2")):
        B.seg(p0, p1, w, 0.024, DORSAL, bone, ext=0.02, ext1=0.02, rnd=0.4)
    # ================= VIPER ARROWHEAD head: flat wedge skull, venom-gland cheeks (widest), short tapering snout
    skull = B.seg((0, -0.80, 0.80), (0, -1.04, 0.79), 0.20, 0.085, HIDE, "Head", top=(0.55, 0.9), ext=0.02)
    B.add((0, -0.88, 0.715), (0.205, 0.08, 0.055), HIDE, "Head", top=(0.9, 0.9), rnd=0.35)  # venom glands (review 2
    # fix 7: on Head, so the widest mass stays with the skull when the jaw drops 36 deg in the roar)
    snout = B.seg((0, -1.00, 0.785), (0, -1.24, 0.76), 0.11, 0.056, HIDE, "Head", top=(0.55, 0.8), ext=0.01)
    for s in (1, -1):                                                                           # tip nostrils
        B.add((s * 0.033, -1.228, 0.80), (0.011, 0.014, 0.006), BLACK, "Head", rot=(0, 0, s * 25), studs=[],
              role="detail", bevel=0.003)
    # viper V marking on the flat skull top (two DORSAL bars converging on the snout)
    for s in (1, -1):
        surf_strip(B, [skull, snout], [(s * 0.13, -0.84, 2.0), (s * 0.07, -0.98, 2.0), (0.0, -1.12, 2.0)],
                   (0, 0, -1), 0.035, 0.010, DORSAL, "Head", proud=0.008, tip1=True)
    for i, y in enumerate((-1.04, -1.09, -1.14)):                                              # upper teeth (3)
        for s in (1, -1):
            B.spike((s * (0.085 - 0.012 * i), y, 0.72), (s * 0.1, 0, -1), 0.03, 0.011, IVORY, "Head")
    for s in (1, -1):                                                                           # SABRE FANGS
        f0 = Vector((s * 0.068, -1.19, 0.728))
        d = Vector((s * 0.10, -0.18, -1)).normalized()
        B.spike(f0, d, 0.10, 0.02, IVORY, "Head", top=(0.45, 0.45))
        B.spike(f0 + d * 0.095, d, 0.045, 0.0095, VENOM, "Head", top=(0.12, 0.12), studs=[], nostud=True)
    B.seg((0, -0.86, 0.665), (0, -1.22, 0.675), 0.105, 0.034, HIDE, "Jaw", top=(0.55, 0.9), ext=0.02)  # lower jaw
    B.seg((0, -0.88, 0.635), (0, -1.18, 0.645), 0.075, 0.014, PALE, "Jaw", top=(0.6, 1), ext=0.0)      # pale chin
    B.add((0, -1.04, 0.706), (0.07, 0.16, 0.006), MOUTH, "Jaw", top=(0.6, 1), studs=[], role="detail", bevel=0.003)
    for i, y in enumerate((-1.06, -1.11, -1.16)):                                              # lower teeth
        for s in (1, -1):
            B.spike((s * (0.07 - 0.012 * i), y, 0.705), (s * 0.1, 0, 1), 0.03, 0.010, IVORY, "Jaw")
    # forked light-violet tongue: lives inside the closed jaw, slides out at the lip line (loc keys)
    B.seg((0, -0.90, 0.703), (0, -1.10, 0.703), 0.024, 0.010, VENOM_L, "Tongue", studs=[], role="detail")
    for s in (1, -1):
        B.spike((0, -1.095, 0.703), (s * 0.35, -1, 0), 0.08, 0.016, VENOM_L, "Tongue", side=(0, 0, 1), studs=[],
                nostud=True)
    for s in (1, -1):
        fierce_eye(B, (s * 0.118, -1.02, 0.862), s, yaw=30, sc=1.15, brow_out=0.012)
        thorn(B, (s * 0.115, -1.00, 0.895), (s * 0.30, 0.35, 1), 0.13, 0.026, "Head")             # viper horn
    # ================= ROYAL CROWN FRILL (hero): 7 deep-violet spines with bone points, two-tone membranes
    roots, tips = [], []
    for (u, d), L, bone in zip(frill_dirs(), FRILL_L, FRILL_BONE):
        r = FRILL0 + Vector((u.x * 0.10, 0.02, u.z * 0.03 - 0.01))
        roots.append(r)
        tips.append(thorn(B, r - d * 0.02, d, L, 0.030, bone, col=VENOM_DEEP))
    # centre panels (on Frill) + outer panels (on Frill_L/R); the boundary panels (+-30 -> +-58) belong to the outer
    # bones and extend 15 deg under the centre membrane, 0.008 behind, so the outer groups can spread 15 deg
    web(B, roots[2:5], tips[2:5], 0.02, (VENOM_DEEP, VENOM_L), "Frill")
    web(B, roots[5:7], tips[5:7], 0.02, (VENOM_DEEP, VENOM_L), "Frill_L")
    web(B, roots[0:2], tips[0:2], 0.02, (VENOM_DEEP, VENOM_L), "Frill_R")
    web(B, roots[4:6], tips[4:6], 0.02, (VENOM_DEEP, VENOM_L), "Frill_L")          # visible boundary 30 -> 58
    web(B, roots[1:3], tips[1:3], 0.02, (VENOM_DEEP, VENOM_L), "Frill_R")
    nback = Vector((0, math.cos(math.radians(FRILL_TILT)), -math.sin(math.radians(FRILL_TILT)))) * 0.008
    T = math.radians(FRILL_TILT)

    def pseudo(a_deg, L):
        u = Vector((math.sin(math.radians(a_deg)), 0, math.cos(math.radians(a_deg))))
        d = Vector((u.x, u.z * math.sin(T) + 0.16 + 0.42 * abs(u.x), u.z * math.cos(T))).normalized()
        r = FRILL0 + Vector((u.x * 0.10, 0.02, u.z * 0.03 - 0.01))
        return r + nback, r + d * L + nback
    for sgn, bone in ((1, "Frill_L"), (-1, "Frill_R")):                            # hidden under-flap 15 -> 30
        (ra, ta), (rb, tb_) = pseudo(15 * sgn, 0.44), pseudo(30 * sgn, 0.50)
        pr, pt = ([ra, rb], [ta, tb_]) if sgn > 0 else ([rb, ra], [tb_, ta])
        web(B, pr, pt, 0.02, (VENOM_DEEP, VENOM_L), bone, scallop=0.0, reach=0.86)
    B.seg(FRILL0 + Vector((0, 0.03, -0.03)), FRILL0 + Vector((0, -0.04, 0.03)), 0.12, 0.035, DORSAL, "Frill",
          side=(1, 0, 0), top=(0.85, 1))                                                       # frill collar
    # ================= basilisk BACK SAIL: starts behind the neck, deep-violet webbing with a violet top edge
    sy = (-0.32, -0.18, -0.04, 0.10, 0.24, 0.36)
    sl = (0.22, 0.32, 0.36, 0.34, 0.26, 0.18)
    sb = ("Chest", "Chest", "Chest", "Spine", "Spine", "Spine")
    sroots = [Vector((0, y, 0.715)) for y in sy]
    stips = []
    for r, L, b, a_deg in zip(sroots, sl, sb, (8, 13, 18, 23, 28, 33)):
        sd = Vector((0, math.sin(math.radians(a_deg)), math.cos(math.radians(a_deg))))
        stips.append(thorn(B, r - sd * 0.04, sd, L, 0.028, b, col=VENOM_DEEP))
    web(B, sroots[:3], stips[:3], 0.018, (VENOM_DEEP, VENOM), "Chest", scallop=0.20, reach=0.80, inner=0.60)
    web(B, sroots[2:], stips[2:], 0.018, (VENOM_DEEP, VENOM), "Spine", scallop=0.20, reach=0.80, inner=0.60)
    # ================= sprawled legs: feet outside the elbows, DORSAL band on the upper leg, socks, splayed claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.05)), K, 0.085, 0.10, HIDE, leg, ext1=0.04, top=(0.8, 0.8))
                B.seg(H.lerp(K, 0.45), H.lerp(K, 0.62), 0.089, 0.104, DORSAL, leg, top=(0.97, 0.97))      # band
                B.seg(K, A, 0.066, 0.07, DORSAL, shin, top=(0.85, 0.85), ext=0.04, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.02, 0.05)), K, 0.10, 0.14, HIDE, leg, ext1=0.04, top=(0.75, 0.7))
                B.seg(H.lerp(K, 0.45), H.lerp(K, 0.62), 0.094, 0.13, DORSAL, leg, top=(0.97, 0.97))
                B.seg(K, A, 0.066, 0.07, DORSAL, shin, top=(0.85, 0.85), ext=0.04, ext1=0.02)
                B.seg(A, P + Vector((0, 0.03, 0.03)), 0.056, 0.056, DORSAL, foot, ext=0.03)
            B.spike(K + Vector((s * 0.05, 0.03, 0.0)), (s * 0.7, 0.7, 0.0), 0.10, 0.03, DORSAL,
                    shin if fb == "F" else leg)                                              # elbow / knee spur
            B.add(P, (0.08, 0.095, 0.042), DORSAL, foot, top=(0.85, 0.80))
            for gx in (-0.055, -0.018, 0.018, 0.055):
                B.spike((P.x + gx, P.y - 0.085, 0.033), (gx * 2.2, -1, -0.5), 0.085, 0.015, BLACK, foot)
    # ================= banded whip tail (shorter): HIDE sides, DORSAL top strip + rings, pale underside, thorn pairs
    T = [Vector(p) for p in TAILP]
    dims = ((0.15, 0.13), (0.115, 0.10), (0.085, 0.075), (0.06, 0.052))
    for i, ((a, b), (w, d)) in enumerate(zip(zip(T, T[1:]), dims)):
        bone = "Tail%d" % (i + 1)
        dn = dims[min(i + 1, 3)][1] * 0.82
        B.seg(a, b, w, d, HIDE, bone, ext=0.08 if i == 0 else 0.03, ext1=0.02, top=(0.82, 0.82))
        B.seg(a + Vector((0, 0, -d + 0.012)), b + Vector((0, 0, -dn + 0.012)), w * 0.7, 0.014, PALE, bone, ext=0.02)
        B.seg(a + Vector((0, 0, d - 0.008)), b + Vector((0, 0, dn - 0.008)), w * 0.78, 0.022, DORSAL, bone, ext=0.02,
              top=(0.82, 1), rnd=0.4)                                                          # top strip
        B.seg(a.lerp(b, 0.52), a.lerp(b, 0.72), w * 0.97, d * 1.04, DORSAL, bone, top=(0.94, 0.94))   # ring
        if i in (1, 2):
            for s in (1, -1):
                B.spike(a.lerp(b, 0.35) + Vector((s * w * 0.8, 0, d * 0.4)), (s * 0.55, 0.65, 0.5),
                        0.09 - 0.015 * i, 0.024, DORSAL, bone, top=(0.12, 0.35))
    # tail-frill: 3 deep-violet thorns fanned up / back / down with light-violet webbing (echo of the crown)
    tip = T[4]
    fr = [tip + Vector((0, -0.02, 0.025)), tip + Vector((0, 0.0, 0.0)), tip + Vector((0, -0.02, -0.025))]
    fd = [Vector((0, 0.55, 0.85)), Vector((0, 1, 0.05)), Vector((0, 0.6, -0.6))]
    ft = [thorn(B, r, d, L, 0.024, "Tail4", col=VENOM_DEEP) for r, d, L in zip(fr, fd, (0.20, 0.22, 0.15))]
    web(B, fr, ft, 0.016, (VENOM_DEEP, VENOM_L), "Tail4", scallop=0.15, reach=0.88, inner=0.0)
    B.build()
    mn, mx = k.bounds()
    pitch = 0.2243 * (mx.z - mn.z) / HEIGHT
    bk.stud_skin(k, pitch)
    return {"TH": round(B.th, 3), "pitch": round(pitch, 4), "H": round(mx.z - mn.z, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.18, 0.52), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.12, 0.52), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", NECKP[0], "Chest", tail=(0, -0.2, 0.1))
    k.joint("Neck2", NECKP[1], "Neck", tail=(0, -0.13, 0.04))
    k.joint("Head", NECKP[2], "Neck2", tail=(0, -0.35, 0.03))          # throat pivot
    k.joint("Jaw", (0, -0.88, 0.70), "Head", tail=(0, -0.3, 0))
    k.joint("Tongue", (0, -0.90, 0.703), "Jaw", tail=(0, -0.2, 0))
    k.joint("Frill", tuple(FRILL0), "Head", tail=(0, 0.1, 0.2))
    k.joint("Frill_L", tuple(FRILL0 + Vector((0.001, 0, 0))), "Frill", tail=(0.15, 0.05, 0.1))
    k.joint("Frill_R", tuple(FRILL0 + Vector((-0.001, 0, 0))), "Frill", tail=(-0.15, 0.05, 0.1))
    k.joint("Venom", (0, -1.28, 0.73), "Head", tail=(0, -0.25, 0))     # venom-drip VFX anchor (no mesh)
    for s, side in ((1, "L"), (-1, "R")):
        for fb, parent, knee in (("F", "Chest", (s * 0.8, 1, 0)), ("B", "Spine", (s * 0.8, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2")
    k.joint("Tail4", TAILP[3], "Tail3", tail=(0, 0.25, 0))


LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3", "Tail4"]
FRILLS = ["Frill", "Frill_L", "Frill_R"]


def check_pairs():
    P = []
    for s in ("L", "R"):
        P += [("Leg_F" + s, "Leg_B" + s), ("Shin_F" + s, "Shin_B" + s), ("Foot_F" + s, "Foot_B" + s)]
    P += [("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw") + tuple(FRILLS):
        for b in ("Chest", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR", "Leg_FL", "Leg_FR"):
            P.append((a, b))
    P += [("Jaw", "Neck"), ("Jaw", "Neck2"), ("Head", "Neck")]
    for f in FRILLS:
        P += [(f, "Neck"), (f, "Neck2")]
    for t in ("Tail2", "Tail3", "Tail4"):
        for b in ("Head", "Jaw", "Neck", "Neck2", "Chest", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR", "Foot_FL",
                  "Foot_FR"):
            P.append((t, b))
    return P


def joints():
    return [(NECKP[2], (0, -0.98, 0.80), 0.20, "Head"), (NECKP[1], NECKP[1], 0.16, "Neck2"),
            (NECKP[0], NECKP[0], 0.20, "Neck")]


# ------------------------------------------------------------------ animation
# Reference (owner rule 2026-10-10, notes in _review/ANIM_REFERENCES_1014.md): animationreference.org "Dragon Walk Cycle
# animation - Creature animation" (C. Sophocleous, 0.3-2.7 s): diagonal pairs, the head dips on each front contact a
# couple of frames late, the tail wave runs base -> tip a quarter cycle late with the tip curling on the trailing beat;
# "Sea Beasts" (0-3 s): heavy-head roar = drop/tuck, lift, the jaw opens ~0.4 s after the lift starts.
# Conventions: Frill "back" + = the fan folds back (kit pitch -), spread + = the outer groups open outward in the fan
# plane; the Jaw is modelled closed (never key below 0); the Tongue slides out on -Y (loc).
import petkit as pk
import _common as cm


def frill(k, f, back=0.0, spread=0.0, twitch=0.0):
    k.key("Frill", f, rot=(-back, 0, twitch))
    k.key("Frill_L", f, rot=(0, 0, spread))
    k.key("Frill_R", f, rot=(0, 0, -spread))


def tongue(k, f, out=0.0, flick=0.0):
    k.key("Tongue", f, rot=(0, flick, 0), loc=(0, -out, 0))


def neckhead(k, f, pitch=(0, 0, 0), yaw=(0, 0, 0), roll=0.0):
    k.key("Neck", f, rot=(pitch[0], yaw[0], 0))
    k.key("Neck2", f, rot=(pitch[1], yaw[1], 0))
    k.key("Head", f, rot=(pitch[2], yaw[2], roll))


def tail_keys(k, f, yaws=(0, 0, 0, 0), pitches=(0, 0, 0, 0)):
    for b, y, p in zip(TAIL, yaws, pitches):
        k.key(b, f, rot=(p, y, 0))


def ankle_T(k, leg, W):
    """ankle world position -> solve_leg target (x/y in the hip's rest frame, z = height over the rest ankle)"""
    L = k.legs2[leg]
    hipR, ankR = k.J[leg], k.J[L["foot"]]
    return Vector((W.x - ankR.x + hipR.x, W.y - ankR.y + hipR.y, W.z - ankR.z))


FOOT_LIFT = 0.003            # the claw tips sit 0.007 under the ankle plane: keep every planted claw >= -0.006


def rest_ankle(k, leg, dy=0.0):
    a = k.J[k.legs2[leg]["foot"]]
    return Vector((a.x, a.y + dy, a.z + FOOT_LIFT))


def foot_tracks(k, n, tracks, lift=0.06):
    """tracks: {leg: [(f0, f1, W)]} planted ankle spots; between two stances the foot swings (eased, arcing up by
    `lift` and out by 0.03 for the sprawl); outside any stance/swing the leg is left to its own rotation keys."""
    import bpy
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg, segs in tracks.items():
            W, z = None, 0.0
            for i, (a, b, P) in enumerate(segs):
                if a <= f <= b:
                    W = P
                    break
                if i + 1 < len(segs) and b < f < segs[i + 1][0] and segs[i + 1][0] - b <= 12:
                    u = (f - b) / float(segs[i + 1][0] - b)
                    s = u * u * (3 - 2 * u)
                    W = P.lerp(segs[i + 1][2], s)
                    z = math.sin(math.pi * u)
                    W = W + Vector((math.copysign(0.03 * z, W.x), 0, lift * z))
                    break
            if W is not None:
                k.solve_leg(leg, f, ankle_T(k, leg, W), toe=35.0 * min(1.0, lift * z / 0.12))


def idle(k):
    """VIPER WATCH: low and still, the throat breathes, two tongue flicks through the notch (out 6 f, back 4 f, the
    jaw cracks 3 deg), ONE slow look-around (25 deg one way, then the other), quick 3 f frill twitches, and a lazy
    tail S-curve; all four feet planted."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        b = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.006 * b))
        k.key("Chest", f, rot=(0.8 * b, 0, 0))
        cm.chain(k, f, n, TAIL, sway=4, pitch=0, cycles=1, lag=0.22, grow=0.6)
    look = [(0, 0), (14, 0), (28, 1), (44, 1), (60, -1), (76, -1), (90, 0), (120, 0)]   # +1 = 25 deg to its left
    for f, l in look:
        neckhead(k, f, pitch=(1, 0, -1), yaw=(8 * l, 7 * l, 10 * l))
    for f, j, t in ((0, 0, 0), (32, 0, 0), (34, 3, 0.06), (38, 3, 0.14), (40, 3, 0.14), (44, 0, 0), (96, 0, 0),
                    (98, 3, 0.06), (102, 3, 0.14), (104, 3, 0.14), (108, 0, 0), (120, 0, 0)):
        k.key("Jaw", f, rot=(j, 0, 0))
        tongue(k, f, t, 6 if 36 <= f <= 40 or 100 <= f <= 104 else 0)
    for f, tw in ((0, 0), (50, 0), (51, 4), (53, -3), (54, 0), (84, 0), (85, -4), (87, 3), (88, 0), (120, 0)):
        frill(k, f, 0, 0, tw)
    foot_tracks(k, n, {leg: [(0, n, rest_ankle(k, leg))] for leg in LEGS4})
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    """SPRAWL STRIDE: diagonal pairs; the lizard S comes from Spine yaw +-8 with the Chest and Neck countering (head
    steady on the target), the head dips a few frames after each front contact, the tail wave lags a quarter cycle;
    the sprawled feet swing out in a wide arc."""
    n = 32

    def body(f):
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 8 * pk.wave(f, n, 0.0), 2.5 * pk.wave(f, n, 0.25)),
              loc=(0, 0, 0.012 * pk.cwave(f, n, 0.05, 2)))
        k.key("Chest", f, rot=(0, -4 * pk.wave(f, n, 0.0), -1.5 * pk.wave(f, n, 0.25)))
        neckhead(k, f, pitch=(1 + 2 * pk.wave(f, n, 0.18, 2), 0, -1 - 2 * pk.wave(f, n, 0.22, 2)),
                 yaw=(-3 * pk.wave(f, n, 0.04), -0.6 * pk.wave(f, n, 0.06), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        tongue(k, f, 0)
        frill(k, f, 2 + 1.5 * pk.wave(f, n, 0.3, 2), 0, 0)
        cm.chain(k, f, n, TAIL, sway=-7, pitch=0, cycles=1, lag=0.25, grow=0.55)

    orig = k.solve_leg

    def arc(leg, f, T, foot_z=0.0, toe=None):                # sprawl: the swinging foot arcs out sideways
        x = k.J[leg].x
        toe = 35.0 * min(1.0, max(0.0, T.z) / 0.12) if toe is None else toe
        T = Vector(T) + Vector((math.copysign(0.45 * max(0.0, T.z), x), 0, FOOT_LIFT))
        return orig(leg, f, T, foot_z, toe)
    k.solve_leg = arc
    try:
        return cm.quad_walk(k, n, 0.12, 0.07, body, gait="trot")
    finally:
        del k.solve_leg


def roar(k):
    """VENOM CROWN (slow build, ref Sea Beasts: the jaw lags the head): tucks the chin and folds the frill back, then
    rears the chest up while the crown RISES over 10 f and its outer spines spread wide; the jaw drops late to 36 deg
    with the tongue fully out and quivering; long hold with a frill shiver; shuts and settles. Feet planted."""
    n = 72
    k.new_action("roar", n, False)
    K = [  # f, spine z, spine pitch, chest, neck, neck2, head, jaw, tongue, frill back, spread, tail pitch
        (0, 0.0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0),
        (8, -0.02, 2, 1, 4, 2, 6, 0, 0.0, 10, 0, -2),
        (12, -0.02, 2, 1, 4, 2, 6, 0, 0.0, 10, 0, -2),
        (20, 0.03, -5, -2, -6, -4, -14, 6, 0.04, -30, 12, 6),        # review 3: the fan faces the game camera
        (24, 0.03, -6, -3, -6, -4, -16, 36, 0.22, -32, 15, 8),
        (52, 0.03, -6, -3, -6, -4, -16, 34, 0.22, -32, 15, 8),
        (58, 0.01, -2, -1, -2, -1, -5, 0, 0.0, 0, 4, 3),
        (72, 0.0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0)]
    for f, z, p, ch, n1, n2, hd, jw, to, fb, sp, tp in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        neckhead(k, f, pitch=(n1, n2, hd))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tongue(k, f, to)
        frill(k, f, fb, sp)
        tail_keys(k, f, pitches=(tp, tp * 0.6, tp * 0.3, 0))
    for f in range(27, 52, 3):                      # hold: frill shiver + tongue-tip flutter + jaw buzz (head still)
        w = 1 if (f // 3) % 2 else -1
        frill(k, f, -32 + 1.5 * w, 15 + 2 * w)
        tongue(k, f, 0.22, 7 * w)
        k.key("Jaw", f, rot=(35 + 1.5 * w, 0, 0))
    foot_tracks(k, n, {leg: [(0, n, rest_ankle(k, leg))] for leg in LEGS4})
    k.finish(loop=False)
    k.events["roar"] = {"roar": round(22 / n, 3), "end": round(56 / n, 3)}


def dash(k):
    """SIGNATURE - BASILISK DASH (review-1 beat table): locks on with the weight back and the frill folded flat, REARS
    and sprints five steps on its sprawled hind legs (trunk ~36 deg up, front legs tucked and pumping, head locked
    level, tail a straight whipping counterweight), skids to a stop, slams down onto the front feet and FLASHES the
    frill (outer groups +15) with a short hiss and a venom drip, holds with a quiver, backs off to its spot with four
    sprawled backpedal steps and settles with a tongue flick."""
    import bpy
    n = 104
    k.new_action("act_dash", n, False)
    # ---- body
    K = [  # f, spine y, z, pitch, roll, chest, neck, neck2, head, tail1 pitch
        (0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0),
        (14, 0.05, -0.05, 4, 0, 2, 6, 0, 2, -4),
        (20, -0.08, 0.10, -36, 0, 2, -4, 0, 24, 40),
        (46, -0.62, 0.10, -44, 0, 2, -4, 0, 30, 46),
        (50, -0.62, 0.10, -44, 0, 2, -4, 0, 30, 46),
        (55, -0.62, -0.04, 6, 0, 1, 2, 0, -4, -6),
        (60, -0.62, -0.02, 2, 0, 0, 0, 0, -2, -2),
        (72, -0.62, 0.0, 0, 0, 0, 0, 0, -1, 0),
        (96, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0),
        (104, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0)]
    for f, y, z, p, r, ch, n1, n2, hd, t1 in K:
        k.key("Spine", f, rot=(p, 0, r), loc=(0, y, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        neckhead(k, f, pitch=(n1, n2, hd))
        tail_keys(k, f, pitches=(t1, 4 if 14 < f < 55 else 0, 2 if 14 < f < 55 else 0, 0))
    for i, c in enumerate(range(22, 43, 4)):          # sprint: 5 hind steps, roll / bob / tail whip on the beat
        s = 1 if i % 2 == 0 else -1
        y = -0.08 - 0.50 * (c - 20) / 22.0
        k.key("Spine", c, rot=(-36 + 3, 0, 6 * s), loc=(0, y, 0.085))
        if c < 42:                                     # the skid (f42-46) decelerates instead
            k.key("Spine", c + 2, rot=(-36 - 2, 0, 3 * s), loc=(0, y - 0.045, 0.11))
        k.key("Head", c, rot=(24, 0, -6 * s))
        k.key("Head", c + 2, rot=(25, 0, -3 * s))
        tail_keys(k, c, (-6 * s, -8 * s, -9 * s, -8 * s), (40, 4, 2, 0))
        tail_keys(k, c + 2, (-3 * s, -9 * s, -11 * s, -11 * s), (40, 4, 2, 0))
    tail_keys(k, 46, (0, 4, 6, 4), (46, 4, 2, 0))
    tail_keys(k, 56, (0, 0, 0, 0), (-6, -6, -3, 0))     # the tail slaps down
    for f, back in ((0, 0), (6, 8), (14, 20), (56, 20), (59, -8), (60, -11), (62, -8), (70, -8), (82, 0), (104, 0)):
        frill(k, f, back, 15 if 59 <= f <= 70 else 0)
    frill(k, 57, 18, 4)
    for f in range(62, 71, 2):                          # quiver + chest tremble
        w = 1 if (f // 2) % 2 else -1
        frill(k, f, -8 + 2 * w, 15)
        k.key("Chest", f, rot=(w * 1.0, 0, 0))
    for f, j in ((0, 0), (56, 0), (58, 18), (66, 18), (74, 0), (104, 0)):
        k.key("Jaw", f, rot=(j, 0, 0))
    for f, t in ((0, 0), (4, 0), (7, 0.12), (10, 0), (97, 0), (100, 0.12), (103, 0), (104, 0)):
        tongue(k, f, t)
    for f, j in ((4, 0), (6, 3), (9, 3), (11, 0), (97, 0), (99, 3), (102, 3), (104, 0)):   # jaw crack (as the idle)
        k.key("Jaw", f, rot=(j, 0, 0))
    for f in (8, 11):
        k.key("Tail4", f, rot=(-4, 8 if f == 8 else -8, 0))
    # ---- front legs: tucked against the chest from f19, pumping +-8 on the beat, unfold f50-54
    for f, a, b, c in ((19, 40, 70, 30), (46, 40, 70, 30), (50, 40, 70, 30), (52, -6, 30, 10)):
        for s in ("L", "R"):
            k.key("Leg_F" + s, f, rot=(a, 0, 0), loc=(0, 0, 0))
            k.key("Shin_F" + s, f, rot=(b, 0, 0))
            k.key("Foot_F" + s, f, rot=(c, 0, 0))
    for i, c in enumerate(range(22, 43, 4)):
        s = 1 if i % 2 == 0 else -1
        for side, sg in (("L", 1), ("R", -1)):
            k.key("Leg_F" + side, c, rot=(40 + 8 * s * sg, 0, 0), loc=(0, 0, 0))
    # ---- feet: rest -> sprint plants (beside the posed hips) -> skid -> slam plants -> backpedal -> rest
    k.bake_bezier_now()
    sc = bpy.context.scene

    def hip(leg, f):
        sc.frame_set(f)
        return k.arm.matrix_world @ k.arm.pose.bones[leg].head

    def plant_at(leg, f, ahead):
        h = hip(leg, f)
        a = rest_ankle(k, leg)
        return Vector((a.x, h.y - ahead, a.z))
    tr = {}
    for leg, contacts, last in (("Leg_BL", (22, 30, 38), 44), ("Leg_BR", (26, 34), 42)):
        segs = [(0, 18 if leg == "Leg_BL" else 22, rest_ankle(k, leg))]
        for c in contacts:
            segs.append((c, c + 4, plant_at(leg, c, 0.05)))
        segs.append((last, None, plant_at(leg, last, -0.02)))
        tr[leg] = segs
    for leg in ("Leg_FL", "Leg_FR"):
        tr[leg] = [(0, 13, rest_ankle(k, leg)), (17, 17, rest_ankle(k, leg, -0.04) + Vector((0, 0, 0.12))),
                   (55, None, rest_ankle(k, leg, -0.62))]                  # peel off the ground as it rears
    # backpedal: diagonal pairs (FL+BR at 74 / 86, FR+BL at 80 / 92), two steps each back to the rest spot
    for leg, steps in (("Leg_FL", (74, 86)), ("Leg_BR", (74, 86)), ("Leg_FR", (80, 92)), ("Leg_BL", (80, 92))):
        a, _, P = tr[leg][-1]
        Q = rest_ankle(k, leg)
        M = P.lerp(Q, 0.5)
        tr[leg][-1] = (a, steps[0], P)
        tr[leg] += [(steps[0] + 6, steps[1], M), (steps[1] + 6, n, Q)]
    foot_tracks(k, n, tr, lift=0.06)
    k.finish(loop=False)
    k.events["act_dash"] = {"launch": round(20 / n, 3), "stomp": round(55 / n, 3), "frill_flash": round(58 / n, 3),
                            "venom_drip": round(60 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    dash(k)
    return stride


HEAD_XF = []
