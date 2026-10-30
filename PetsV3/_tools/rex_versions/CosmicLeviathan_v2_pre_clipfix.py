# Cosmic Leviathan v2 (review 1 M1-M7 + S2-S4; Celestial egg SECRET 1 %, 2026-10-14) - "NEBULA SOVEREIGN" (plan review:
# _review/CosmicLeviathan_plan_review.md). A legless sky-sea leviathan floating in a rearing S: obsidian saddle plates
# over a plum-nebula hide and ivory belly scutes; the CORONA-FIN light language (obsidian root -> plum -> deep ->
# periwinkle-azure -> starlight point) on 4-panel flying-fish wing-fins, 3 falcate dorsals, cheek fins and a
# swallowtail fluke. HERO: the COMET CROWN - a closed gold coronet with 6 points, a swept-back gold comet horn (the
# model top) and an azure 4-point star gem. Underbite skull with azure slit eyes under a V brow, 2 ivory tusks.
# Gold ONLY on the crown. No glow mesh (VFX on the anchors). Old version: _tools/rex_versions/CosmicLeviathan_v0.py
import math
from mathutils import Vector, Matrix

DISPLAY = "Cosmic Leviathan"
MOTION = "Swim"
RIG = "fish"
HEIGHT = 10.0              # horn tip in studs at x1

# Blender colours (Roblox renders ~0.6x darker) - plan review section 1
ARMOR = (62, 62, 96)       # obsidian: skull cap, nasal plates, mandible plates, saddle plates, fin spars / roots
ARMOR_D = (40, 40, 66)     # brows, lip line
HIDE = (170, 54, 170)      # plum nebula: flanks, neck, snout sides, fin inner fields
BELLY = (244, 228, 192)    # ivory: chin, throat, ventral scutes
BELLY_D = (204, 182, 140)  # scute gap bars
DEEP = (66, 64, 214)       # the bridge step between plum and azure; gem roots
AZURE = (90, 148, 255)     # periwinkle-azure starfire (the Celestial Index colour): fin outer fields, eyes, gem
STAR = (224, 234, 255)     # fin points, eye hot spots, gem centre, horn tip
GOLD = (255, 196, 50)      # the crown ONLY
GOLD_D = (214, 150, 30)
IVORY = (240, 234, 214)    # tusks, teeth
MOUTH = (46, 16, 46)
BLACK = (14, 14, 22)

H_MODEL = 1.70
N_SE = 2.6
SEG = 20
# body centreline (curveloft stations y, z, hw, hh) - a true S: rearing neck, belly trough, flattening tail
ST = [(-0.86, 1.12, 0.19, 0.19), (-0.76, 1.00, 0.21, 0.22), (-0.64, 0.84, 0.25, 0.27), (-0.46, 0.66, 0.28, 0.29),
      (-0.12, 0.43, 0.245, 0.25), (0.22, 0.36, 0.20, 0.21), (0.54, 0.44, 0.15, 0.17), (0.84, 0.56, 0.105, 0.13),
      (1.10, 0.66, 0.07, 0.095), (1.32, 0.71, 0.045, 0.065)]
# bone splits along the body (y): Neck | Chest | Spine | Tail1 | Tail2 | Tail3 | Tail4
SPLIT = [("Neck", -0.86, -0.66), ("Chest", -0.66, -0.30), ("Spine", -0.30, 0.38), ("Tail1", 0.38, 0.74),
         ("Tail2", 0.74, 1.06), ("Tail3", 1.06, 1.22), ("Tail4", 1.22, 1.32)]
# skull (constant-y rings: y, zc, hw, hh) - the upper head above the mouth line
SKULL = [(-0.78, 1.22, 0.16, 0.14), (-0.80, 1.22, 0.17, 0.15), (-0.90, 1.22, 0.21, 0.17), (-0.98, 1.22, 0.19, 0.16),
         (-1.08, 1.15, 0.15, 0.09), (-1.20, 1.13, 0.12, 0.08), (-1.32, 1.12, 0.095, 0.07)]
# lower jaw (y, zc, hw, hh), modelled JAW_OPEN deg open about the hinge
JAWT = [(-0.84, 1.01, 0.19, 0.055), (-0.92, 1.01, 0.21, 0.055), (-1.08, 1.01, 0.17, 0.05), (-1.24, 1.01, 0.14, 0.045),
        (-1.36, 1.02, 0.115, 0.04)]
JAW_P = Vector((0, -0.90, 1.07))
JAW_OPEN = 6.0
HEADP = Vector((0, -0.80, 1.04))
NECKP = Vector((0, -0.64, 0.84))
HUB = Vector((0.28, -0.44, 0.56))
FINTIP_P = Vector((0.60, -0.25, 0.67))    # on the P1 spar at 45 % (v1c az 32, e 17)
ANCH = {}
L = None


def loft():
    global L
    if L is None:
        import curveloft as cl
        L = cl.Loft(ST, n=N_SE, seg=SEG)
    return L


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def tab(T, y):
    """linear interpolation in a (y, zc, hw, hh) table -> (zc, hw, hh)"""
    T = sorted(T, key=lambda r: r[0])
    if y <= T[0][0]:
        a, b = T[0], T[1]
    elif y >= T[-1][0]:
        a, b = T[-2], T[-1]
    else:
        a, b = next((T[i], T[i + 1]) for i in range(len(T) - 1) if T[i][0] <= y <= T[i + 1][0])
    t = (y - a[0]) / (b[0] - a[0])
    return tuple(a[i] + (b[i] - a[i]) * t for i in (1, 2, 3))


def zang(f):
    return math.asin(max(-1.0, min(1.0, math.copysign(abs(f) ** (N_SE / 2.0), f))))


def ys(T, y0, y1, step=0.05):
    lo, hi = min(y0, y1), max(y0, y1)
    m = max(2, int(math.ceil((hi - lo) / step)))
    out = set([lo + (hi - lo) * i / m for i in range(m + 1)]) | set(r[0] for r in T if lo < r[0] < hi)
    return sorted(out)


def ytube(B, T, y0, y1, color, bone, zlo=-1.0, zhi=1.0, grow=0.0, xf=None, nostud=False):
    """closed solid on constant-y rings through table T between y0..y1 (zlo / zhi: keep the part above / below)"""
    import blockkit as bk
    rings = []
    for y in ys(T, y0, y1):
        zc, w, h = tab(T, y)
        w, h = w + grow, h + grow
        if zlo > -1:
            a = zang(zlo)
            r = bk.superellipse(w, h, zc, y, N_SE, SEG // 2, a, math.pi - a)
        elif zhi < 1:
            a = zang(zhi)
            r = bk.superellipse(w, h, zc, y, N_SE, SEG // 2, math.pi - a, 2 * math.pi + a)
        else:
            r = bk.superellipse(w, h, zc, y, N_SE, SEG)
        rings.append([xf(p) for p in r] if xf else r)
    return B.tube(rings, color, bone, nostud=nostud)


def yband(B, T, y0, y1, color, bone, zlo=-1.0, zhi=1.0, grow=0.008, inset=0.02, xf=None):
    """flush pattern shell on a constant-y table (top band from zlo, or bottom band up to zhi)"""
    import blockkit as bk
    rings = []
    for y in ys(T, y0, y1, 0.06):
        zc, w, h = tab(T, y)
        if zlo <= -1:
            a = zang(zhi)
            a0, a1 = a, -math.pi - a
        else:
            a = zang(zlo)
            a0, a1 = math.pi - a, a
        o = bk.superellipse(w + grow, h + grow, zc, y, N_SE, SEG // 2, a0, a1)
        i = bk.superellipse(w - inset, h - inset, zc, y, N_SE, SEG // 2, a0, a1)
        if xf:
            o, i = [xf(p) for p in o], [xf(p) for p in i]
        rings.append((o, i))
    return B.tube(rings, color, bone, closed=False)


def jawpt(p):
    a = math.radians(JAW_OPEN)
    q = Vector(p) - JAW_P
    return JAW_P + Vector((q.x, q.y * math.cos(a) - q.z * math.sin(a), q.y * math.sin(a) + q.z * math.cos(a)))


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


def slit_eye(B, c, n, s, bone="Head", sc=1.2):
    """fierce azure slit eye seated on the skull (normal n): black socket -> AZURE slit -> STAR hot spot -> black slit
    pupil (<= 70 % of the iris height); inner corner down. No glint, no round pupil (never googly)."""
    n = Vector(n).normalized()
    fwd = Vector((0, -1, 0))
    t = (fwd - n * fwd.dot(n)).normalized()
    up = n.cross(t).normalized() * (1 if s > 0 else -1)
    if up.z < 0:
        up = -up
    tilt = math.radians(16)
    t2 = (t * math.cos(tilt) - up * math.sin(tilt)).normalized()
    up2 = n.cross(t2).normalized()
    if up2.z < 0:
        up2 = -up2
    R = Matrix((t2, n, up2)).transposed()
    c = Vector(c)
    B.add(c, (0.052 * sc, 0.008, 0.024 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.009)
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0135 * sc), AZURE, bone, R=R, studs=[], role="detail", bevel=0.003)
    B.add(c + n * 0.011 - t2 * 0.018 * sc, (0.009 * sc, 0.004, 0.005 * sc), STAR, bone, R=R, studs=[], role="detail",
          bevel=0.002)
    B.add(c + n * 0.011 + t2 * 0.004, (0.006 * sc, 0.004, 0.0094 * sc), BLACK, bone, R=R, studs=[], role="detail",
          bevel=0.002)
    # v1d LID: an ARMOR_D brow-plate laid OVER the eye's upper ~40 %, steeper than the slit (30 deg, front-low), so the
    # two sides form a V that pinches the eyes (the Mantis lesson - a brow floating above the eye reads as goggles)
    lt = math.radians(30)
    tL = (t * math.cos(lt) - up * math.sin(lt)).normalized()
    uL = n.cross(tL).normalized()
    if uL.z < 0:
        uL = -uL
    RL = Matrix((tL, n, uL)).transposed()
    B.add(c + n * 0.012 + uL * 0.019 * sc + tL * 0.012, (0.064 * sc, 0.006, 0.013 * sc), ARMOR_D, bone, R=RL, studs=[],
          role="detail", bevel=0.004)


def panel(B, a, b, hw0, th0, colors, bones, splits, n_up, top_w=0.25, top_t=0.6, off=0.0, tip_spike=None, root=None):
    """a tapered fin panel a -> b split along its length into colour/bone pieces at the fractions `splits`
    (len(colors) = len(splits) + 1); chord half hw0 at the root -> hw0*top_w at the tip, half-thickness th0 -> th0*top_t;
    the chord lies across the panel in the plane normal to n_up; offset `off` along n_up.
    root = (t_r, w_r): a narrow KNUCKLE - the chord grows from hw0*w_r at the root to hw0 at t_r, then tapers as above
    (v1d: a full-chord root is buried up to 0.11 in the hull and every flap sweeps it out through the skin)"""
    a, b = Vector(a), Vector(b)
    d = (b - a).normalized()
    n_up = Vector(n_up).normalized()
    side = n_up.cross(d).normalized()
    a, b = a + n_up * off, b + n_up * off
    fr = [0.0] + list(splits) + [1.0]

    def wid(t):
        if root and t < root[0]:
            return hw0 * (root[1] + (1 - root[1]) * t / root[0])
        t0 = root[0] if root else 0.0
        return hw0 * (1 - (1 - top_w) * (t - t0) / (1 - t0))
    out = []
    for i, (c, bn) in enumerate(zip(colors, bones)):
        brk = [fr[i]] + ([root[0]] if root and fr[i] < root[0] < fr[i + 1] else []) + [fr[i + 1]]
        for j, (t0, t1) in enumerate(zip(brk, brk[1:])):
            p0, p1 = a.lerp(b, t0), a.lerp(b, t1)
            w0, w1 = wid(t0), wid(t1)
            h0, h1 = th0 * (1 - (1 - top_t) * t0), th0 * (1 - (1 - top_t) * t1)
            smooth = c in (DEEP, AZURE, STAR, GOLD)
            kw = dict(studs=[], nostud=True, role="limb") if smooth else {}
            first, last = (i == 0 and j == 0), (i == len(colors) - 1 and j == len(brk) - 2)
            out.append(B.seg(p0 - d * (0.0 if first else 0.01), p1 + d * (0.0 if last else 0.01), w0, h0, c, bn,
                             side=side, top=(w1 / w0, h1 / h0), **kw))
    if tip_spike:
        L_, w_ = tip_spike
        B.spike(b - d * 0.01, d, L_, w_, STAR, bones[-1], top=(0.1, 0.1), nostud=True, studs=[])
    return out


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=611, tier=5, plates=False, th=0.68)       # th: tubes are not boxes
    Lf = loft()
    sy = Lf.s_at_y
    # ================= HULL: curveloft S-body, one tube per bone (flush overlapping joints)
    parts = [(bn, sy(y0), sy(y1)) for bn, y0, y1 in SPLIT]
    hull = []
    for i, (bn, a, b) in enumerate(parts):
        j0 = a if i > 0 else None
        j1 = b if i < len(parts) - 1 else None
        hull.append(Lf.tube(B, max(0.0, a - (0.06 if j0 is not None else 0)),
                            min(Lf.length, b + (0.06 if j1 is not None else 0)), HIDE, bn, j0=j0, j1=j1, step=0.10))
    # saddle armour: segmented top plates (zlo +0.25), one+ per bone, 0.03 plum gaps (NOT glowing seams)
    cuts = [sy(-0.78), sy(-0.66), sy(-0.48), sy(-0.30), sy(-0.02), sy(0.38), sy(0.74), sy(1.06), sy(1.22), sy(1.30)]
    owner = ["Neck", "Chest", "Chest", "Spine", "Spine", "Tail1", "Tail2", "Tail3", "Tail4"]
    # v1c: wider plum gaps; the rearing front half's plates wrap lower down the flank; the saddle is SPLIT along
    # the spine (plum midline strip, 2 x 9 deg) from the nape to Tail2 - the dorsals rise out of it
    for i_, ((a, b), bn) in enumerate(zip(zip(cuts, cuts[1:]), owner)):
        zl = -0.15 if bn in ("Neck", "Chest", "Spine") else (-0.05 if bn in ("Tail1", "Tail2") else 0.12)
        if i_ >= 1 and bn not in ("Tail3", "Tail4"):
            al = Lf.zang(zl)
            g = math.radians(9)
            for arc in ((math.pi - al, math.pi / 2 + g), (math.pi / 2 - g, al)):
                Lf.band(B, a + 0.03, b - 0.03, ARMOR, bn, grow=0.008, step=0.09, zlo=zl, arc=arc, aseg=SEG // 4 + 1)
        else:
            Lf.band(B, a + 0.03, b - 0.03, ARMOR, bn, zlo=zl, grow=0.008, step=0.09)
    # belly: ivory bottom band (zhi -0.50) per bone + BELLY_D scute gap bars every ~0.12
    bcuts = [sy(-0.86), sy(-0.66), sy(-0.30), sy(0.38), sy(0.74), sy(0.92)]
    bown = ["Neck", "Chest", "Spine", "Tail1", "Tail2"]
    bzhi = {"Neck": -0.80, "Chest": -0.88}                 # the rising neck + chest face the camera: a keel strip
    for (a, b), bn in zip(zip(bcuts, bcuts[1:]), bown):
        Lf.band(B, a, b, BELLY, bn, zlo=-1.0, zhi=bzhi.get(bn, -0.40), grow=0.008, step=0.09)
    s = sy(-0.76)
    while s < sy(0.54):
        y = Lf.at(s)[0].y
        bn = next(b for b, y0, y1 in SPLIT if y0 <= y < y1)
        wd, cc = (0.017, HIDE) if bn in ("Neck", "Chest") else (0.01, BELLY_D)
        Lf.band(B, s - wd, s + wd, cc, bn, zlo=-1.0, zhi=bzhi.get(bn, -0.40) - 0.02, grow=0.011, inset=0.01,
                step=0.02)
        s += 0.14
    # ================= SKULL (Head): its own tube, plum sides, obsidian cap, nasal plates, nostrils
    skull = ytube(B, SKULL, -0.78, -1.32, HIDE, "Head")
    yband(B, SKULL, -0.80, -1.10, ARMOR, "Head", zlo=0.08, grow=0.008)        # v1c: helmet down the cheeks
    yband(B, SKULL, -1.10, -1.31, ARMOR, "Head", zlo=0.45, grow=0.008)        # v1d: obsidian nasal bridge (front view:
    # a bare round plum snout with nostrils on top read as a pig snout)
    for yy, hw in ((-1.12, 0.045), (-1.20, 0.04), (-1.27, 0.035)):
        p, nn = surf_hit(B, [skull], (0, yy, 1.6), (0, 0, -1))
        Rn = bk.frame_from(p, p + Vector((0, -1, 0)), nn)
        B.add(p + nn * 0.004, (0.008, hw, 0.032), ARMOR, "Head", R=Rn, role="detail", bevel=0.006)
    for s_ in (1, -1):
        B.add((s_ * 0.099, -1.285, 1.142), (0.004, 0.014, 0.006), BLACK, "Head", studs=[], role="detail",
              R=Matrix.Rotation(math.radians(-s_ * 12), 3, "Z"), bevel=0.002)   # v1d: angled nostril slits cut into
    B.add((0, -1.325, 1.158), (0.082, 0.006, 0.034), ARMOR, "Head", studs=[], role="detail", bevel=0.01)  # the
    # obsidian ROSTRAL SHIELD over the upper tip face (a bare plum disc + 2 holes = pig snout)
    # throat (Head, under the skull behind the jaw) - ivory
    ytube(B, [(-0.80, 1.05, 0.15, 0.08), (-0.88, 1.03, 0.18, 0.07)], -0.80, -0.88, BELLY, "Head")
    # ================= JAW (underbite, 6 deg open): plum, obsidian mandible plates, ivory underside, mouth floor
    ytube(B, JAWT, -0.84, -1.36, HIDE, "Jaw", xf=jawpt)
    yband(B, JAWT, -0.86, -1.34, BELLY, "Jaw", zlo=-1.0, zhi=-0.30, grow=0.006, xf=jawpt)
    for s_ in (1, -1):
        for y0, y1 in ((-0.90, -1.06), (-1.10, -1.26)):
            pa = jawpt(Vector((s_ * (tab(JAWT, y0)[1] + 0.002), y0, 1.02)))
            pb = jawpt(Vector((s_ * (tab(JAWT, y1)[1] + 0.002), y1, 1.02)))
            B.bar(pa, pb, Vector((s_, 0, 0)), 0.05, 0.002, ARMOR, "Jaw", bevel=0.0015)   # S3: flush          # mandible plates
    B.add(jawpt(Vector((0, -1.12, 1.058))), (0.12, 0.20, 0.006), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    B.add((0, -1.12, 1.062), (0.10, 0.20, 0.006), MOUTH, "Head", studs=[], role="detail", bevel=0.003)   # roof
    # tusks (lower jaw, outside the snout), lower fangs (rim, overlapping the upper lip) + upper teeth (inside)
    for s_ in (1, -1):
        B.spike(jawpt(Vector((s_ * 0.118, -1.31, 1.05))), (0, -0.25, 1), 0.11, 0.017, IVORY, "Jaw", top=(0.15, 0.15))
        for i, yy in enumerate((-1.23, -1.13, -1.05)):
            w = tab(JAWT, yy)[1] - 0.012
            B.spike(jawpt(Vector((s_ * w, yy, 1.05))), (s_ * 0.1 * (i % 2), -0.1, 1), 0.05 + 0.02 * (i % 2), 0.013,
                    IVORY, "Jaw", top=(0.15, 0.15))
        for i, yy in enumerate((-1.27, -1.18, -1.09, -0.99)):
            w = tab(SKULL, yy)[1] - 0.03
            ang = math.radians(8 * (1 if i % 2 else -1))
            B.spike((s_ * w, yy, 1.07), (0, math.sin(ang), -1), 0.035 + 0.015 * (i % 2), 0.012, IVORY, "Head",
                    top=(0.15, 0.15))
    # ================= azure slit eyes under V brow-lids (ARMOR_D, in slit_eye)
    for s_ in (1, -1):
        c0 = Vector((s_ * 0.150, -1.035, 1.265))
        n0 = Vector((s_ * math.cos(math.radians(42)), -math.sin(math.radians(42)), 0.20)).normalized()
        p, nn = surf_hit(B, [skull], c0 + n0 * 0.3, -n0)
        slit_eye(B, p + nn * 0.004, nn, s_)
        ANCH["Eye_" + ("L" if s_ > 0 else "R")] = tuple(p + nn * 0.02)
    # ================= COMET CROWN (hero, the only gold): closed band, 6 points, comet horn, star gem
    kwg = dict(studs=[], nostud=True, role="limb")
    for y in (-1.00, -0.84):                                                                # front + back bars
        B.add((0, y, 1.365), (0.17, 0.0175, 0.030), GOLD, "Head", bevel=0.008, **kwg)
    for s_ in (1, -1):
        B.add((s_ * 0.19, -0.92, 1.36), (0.0175, 0.08, 0.030), GOLD, "Head", bevel=0.008, **kwg)   # side bars
        for y in (-1.00, -0.84):
            B.add((s_ * 0.175, y, 1.365), (0.026, 0.026, 0.035), GOLD, "Head", bevel=0.01, **kwg)  # corner blocks
        for (x, y, z, h, sp) in ((0.15, -0.99, 1.40, 0.09, 0), (0.20, -0.92, 1.39, 0.11, 20), (0.15, -0.85, 1.39, 0.08, 0)):
            d = Vector((s_ * math.sin(math.radians(sp)), math.sin(math.radians(15)), 1)).normalized()
            B.spike((s_ * x, y, z - 0.02), d, h, 0.030, GOLD, "Head", top=(0.12, 0.12), **kwg)
    B.seg((0, -0.95, 1.37), (0, -0.80, 1.52), 0.05, 0.042, GOLD, "Head", side=(1, 0, 0), top=(0.8, 0.8),
          **kwg)                                                                             # horn root
    hd = Vector((0, 0.707, 0.707))
    B.spike(Vector((0, -0.80, 1.52)) - hd * 0.02, hd, 0.22, 0.045, GOLD, "Head", top=(0.12, 0.12), **kwg)
    B.spike(Vector((0, -0.80, 1.52)) + hd * 0.195, hd, 0.05, 0.02, STAR, "Head", top=(0.1, 0.1), **kwg)
    B.seg((0, -0.93, 1.33), (0, -0.66, 1.60), 0.018, 0.03, GOLD_D, "Head", side=(1, 0, 0), top=(0.4, 0.4),
          **kwg)                                                                             # keel under the horn
    ANCH["Horn"] = tuple(Vector((0, -0.80, 1.52)) + hd * 0.245)
    gn = Vector((0, -math.cos(math.radians(20)), math.sin(math.radians(20))))
    gx = Vector((1, 0, 0))
    gz = gn.cross(gx).normalized()
    if gz.z < 0:
        gz = -gz
    Rg = Matrix((gx, gn, gz)).transposed()
    gc = Vector((0, -1.025, 1.39))
    B.add(Vector((0, -1.01, 1.38)), (0.075, 0.02, 0.06), GOLD, "Head", R=Rg, bevel=0.008, **kwg)   # gem plate
    for dv in (gz, -gz, gx, -gx):                                                            # 4-point star
        B.spike(gc + gn * 0.01, dv, 0.06, 0.022, AZURE, "Head", top=(0.1, 0.1), **kwg)
        B.spike(gc + gn * 0.006, dv, 0.035, 0.026, DEEP, "Head", top=(0.5, 0.5), **kwg)
    B.add(gc + gn * 0.018, (0.0175, 0.0175, 0.0175), STAR, "Head", R=Rg, bevel=0.005, **kwg)
    ANCH["Crown"] = tuple(gc + gn * 0.03)
    ANCH["Mouth"] = (0, -1.40, 1.06)
    ANCH["Core"] = (0, -0.46, 0.32)
    # ================= cheek fins (Head): ARMOR root 55 % -> AZURE -> STAR point
    for s_ in (1, -1):
        a, b = Vector((s_ * 0.19, -0.86, 1.14)), Vector((s_ * 0.40, -0.62, 1.30))
        d = (b - a).normalized()
        nup = Vector((s_, 0, 0)) - d * d.x * s_                       # chord ~vertical: a broad gill fin
        panel(B, a, b, 0.07, 0.015, [ARMOR, AZURE], ["Head", "Head"], [0.38], nup, top_w=0.3, top_t=0.7,
              tip_spike=(0.05, 0.016))
    # ================= WING-FINS (signature): 4-panel flying-fish fan per side, Fin (plum) / FinTip (light)
    for s_, sd in ((1, "L"), (-1, "R")):
        h0 = X(HUB, s_)
        p, nn = surf_hit(B, hull, h0 + Vector((s_ * 0.3, 0, -0.05)), (-s_, 0, 0.15))
        hub = p + nn * 0.02                       # v2 (S2): 0.01 proud - the slimmer chest reseats the hub inward
        # v1c: the trailing panels spread wider + longer (at 50-78 deg they bunched behind the spar and read as
        # crystals), +4 deg dihedral so the fan faces the tq / game cameras
        for i, (az, el, ln, hc, off) in enumerate(((32, 17, 0.86, 0.07, 0.008), (43, 16, 0.80, 0.15, 0.004),
                                                   (54, 15, 0.70, 0.15, 0.0), (65, 14, 0.58, 0.13, -0.004))):
            d = Vector((s_ * math.cos(math.radians(az)) * math.cos(math.radians(el)),
                        math.sin(math.radians(az)) * math.cos(math.radians(el)), math.sin(math.radians(el))))
            tip = hub + d * ln
            nup = Vector((0, 0, 1)) - d * d.z
            if i == 0:
                panel(B, hub, tip, hc, 0.025, [ARMOR, ARMOR, DEEP, AZURE], ["Fin_" + sd] + ["FinTip_" + sd] * 3,
                      [0.45, 0.62, 0.68], nup, off=off,
                      tip_spike=(0.06, 0.02), root=(0.40, 0.3))
                ANCH["FinEnd_" + sd] = tuple(tip + d * 0.06)
            else:
                panel(B, hub, tip, hc, 0.025, [HIDE, DEEP, AZURE], ["Fin_" + sd, "FinTip_" + sd, "FinTip_" + sd],
                      [0.46, 0.52], nup, off=off, tip_spike=(0.05, 0.018), root=(0.40, 0.25), top_w=0.45)   # azure from 42 %
    # ================= DORSALS (3 falcate fins): ARMOR 0-45 % / HIDE -70 % / DEEP step / AZURE + STAR point
    # v1c: tips swept back to the plan's 45 deg (the table's tips gave ~30 = upright spikes)
    for nm, (yf, yb), tip in (("Dorsal1", (-0.50, -0.16), (0.32, 0.03)),
                              ("Dorsal2", (-0.07, 0.23), (0.34, 0.03)),
                              ("Dorsal3", (0.44, 0.66), (0.25, 0.03))):
        Rf = Lf.surf(sy(yf), math.pi / 2) - Vector((0, 0, 0.03))
        Rb = Lf.surf(sy(yb), math.pi / 2) - Vector((0, 0, 0.03))
        _c, _T, _N, _w, _h = Lf.at(sy((yf + yb) / 2))
        U = (_N + Vector((0, 0, 1))).normalized()
        Bk = (_T - U * _T.dot(U)).normalized()
        T = (Rf + Rb) / 2 + U * tip[0] + Bk * ((Rb - Rf).length / 2 + tip[1])
        def FE(h):
            return Rf.lerp(T, h) + (U * 0.035 - Bk * 0.015) * math.sin(math.pi * h)

        def BE(h):
            return Rb.lerp(T, h) - Bk * 0.035 * math.sin(math.pi * h)
        def PP(h, f):
            return FE(h).lerp(BE(h), f)
        QS = 0.40
        for c, h0_, h1_, f0, f1, th0, th1 in ((ARMOR, 0.0, 0.36, 0.0, QS, 0.026, 0.021), (ARMOR, 0.36, 0.70, 0.0, QS, 0.021, 0.017),
                                             (ARMOR, 0.70, 0.95, 0.0, QS, 0.017, 0.013),
                                             (HIDE, 0.0, 0.32, QS, 1.0, 0.018, 0.015), (DEEP, 0.32, 0.38, QS, 1.0, 0.015, 0.014),
                                             (AZURE, 0.38, 0.95, QS, 1.0, 0.014, 0.010)):
            fm = (f0 + f1) / 2
            m0, m1 = PP(h0_, fm), PP(h1_, fm)
            w0 = max(0.010, (PP(h0_, f1) - PP(h0_, f0)).length / 2)
            w1 = max(0.006, (PP(h1_, f1) - PP(h1_, f0)).length / 2)
            side = (PP(h0_, f1) - PP(h0_, f0)).normalized()
            smooth = c in (DEEP, AZURE)
            kw = dict(studs=[], nostud=True, role="limb") if smooth else {}
            B.seg(m0 - (m1 - m0).normalized() * 0.008, m1 + (m1 - m0).normalized() * 0.006, w0, th0, c, nm, side=side,
                  top=(w1 / w0, th1 / th0), **kw)
        dT = (T - (Rf + Rb) / 2).normalized()
        B.spike(T - dT * 0.03, dT, 0.06, 0.018, STAR, nm, top=(0.1, 0.1), nostud=True, studs=[])
        ANCH[nm + "Tip"] = tuple(T + dT * 0.03)
    # ================= SWALLOWTAIL FLUKE (Fluke): ARMOR root / HIDE / DEEP + AZURE / STAR point, deep V notch
    for s_, sd in ((1, "L"), (-1, "R")):
        lead0 = Vector((s_ * 0.04, 1.30, 0.71))
        notch = Vector((0, 1.48, 0.71))
        tip = Vector((s_ * 0.40, 1.64, 0.75))
        root = (lead0 + notch) / 2
        d = (tip - root).normalized()
        nup = Vector((0, 0, 1)) - d * d.z
        panel(B, root, tip, 0.10, 0.03, [ARMOR, HIDE, DEEP, AZURE], ["Fluke"] * 4, [0.22, 0.52, 0.58], nup,
              top_w=0.35, top_t=0.5, tip_spike=(0.06, 0.02))
        ANCH["Fluke" + sd] = tuple(tip + d * 0.06)
    B.build()
    mn, mx = k.bounds()
    pitch = 0.2243 * mx.z / HEIGHT                      # H_MODEL = floor -> horn tip (it hovers; plan 9)
    bk.stud_skin(k, pitch)
    return {"TH": round(B.th, 3), "pitch": round(pitch, 4), "H": round(mx.z, 3), "lowest": round(mn.z, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    Lf = loft()
    c = lambda y: Lf.at(Lf.s_at_y(y))[0]
    k.joint("Spine", tuple(c(-0.10)), "Root", tail=(0, 0.3, 0))
    k.joint("Chest", tuple(c(-0.30)), "Spine", tail=(0, -0.3, 0.2))
    k.joint("Neck", tuple(NECKP), "Chest", tail=(0, -0.12, 0.18))
    k.joint("Head", tuple(HEADP), "Neck", tail=(0, -0.3, 0))
    k.joint("Jaw", tuple(JAW_P), "Head", tail=(0, -0.3, 0))
    prev = "Spine"
    for bn, y in (("Tail1", 0.38), ("Tail2", 0.74), ("Tail3", 1.06), ("Tail4", 1.22), ("Fluke", 1.32)):
        k.joint(bn, tuple(c(y)), prev, tail=(0, 0.2, 0))
        prev = bn
    for s, sd in ((1, "L"), (-1, "R")):
        k.joint("Fin_" + sd, tuple(X(HUB, s)), "Chest", tail=(s * 0.3, 0.2, 0.03))
        k.joint("FinTip_" + sd, tuple(X(FINTIP_P, s)), "Fin_" + sd, tail=(s * 0.3, 0.2, 0.03))
        k.joint("FinEnd_" + sd, ANCH.get("FinEnd_" + sd, (0, 0, 1)), "FinTip_" + sd, tail=(s * 0.05, 0.05, 0))
        k.joint("Fluke" + sd, ANCH.get("Fluke" + sd, (0, 1.6, 0.75)), "Fluke", tail=(s * 0.05, 0.05, 0))
        k.joint("Eye_" + sd, ANCH.get("Eye_" + sd, (0, -1, 1.3)), "Head", tail=(s * 0.05, -0.05, 0))
    for nm, y, bone in (("Dorsal1", -0.30, "Chest"), ("Dorsal2", 0.07, "Spine"), ("Dorsal3", 0.54, "Tail1")):
        p = Lf.surf(Lf.s_at_y(y), math.pi / 2)
        k.joint(nm, tuple(p - Vector((0, 0, 0.03))), bone, tail=(0, 0.1, 0.2))
    for nm, bone in (("Crown", "Head"), ("Horn", "Head"), ("Mouth", "Head"), ("Core", "Chest")):
        k.joint(nm, ANCH.get(nm, (0, -1, 1.3)), bone, tail=(0, 0, 0.08))


def check_pairs():
    P = [("Head", "Dorsal1"), ("Neck", "Dorsal1"), ("Fluke", "Tail2"), ("Fluke", "Dorsal3"), ("Tail4", "Dorsal3"),
         ("Jaw", "Neck"), ("Jaw", "Chest"), ("Head", "Chest"), ("Tail3", "Spine"), ("Tail2", "Spine"),
         ("Tail3", "Dorsal2"), ("Tail2", "Dorsal2")]
    for sd in ("L", "R"):
        P += [("Fin_" + sd, "Chest"), ("Fin_" + sd, "Spine"), ("FinTip_" + sd, "Spine"), ("FinTip_" + sd, "Chest"),
              ("FinTip_" + sd, "Tail1"), ("Fin_" + sd, "Head"), ("FinTip_" + sd, "Head"), ("Fin_" + sd, "Neck")]
    return P


def joints():
    out = [((0.22, -0.90, 1.07), (-0.22, -0.90, 1.07), 0.07, "Jaw"),                 # jaw hinge
           ((0.26, -0.92, 1.0), (-0.26, -0.92, 1.0), 0.15, "Jaw")]                     # v1d: throat junction - the
    # neck tube's front cap tilts forward under the jaw's rear corners (the neck rises 50 deg into the head); every
    # head-up / yaw crossing lies within 0.15 of this line (pose_try where=)
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((tuple(X(HUB, s)), tuple(X(HUB + Vector((0.10, 0.06, 0.0)), s)), 0.10, "Fin_" + sd))   # fin hub
        out.append((tuple(X(HUB, s)), tuple(X(HUB + Vector((0.07, 0.15, 0.03)), s)), 0.11, "Fin_" + sd))  # knuckle
        out.append((tuple(X(FINTIP_P - Vector((0.05, 0.08, 0)), s)), tuple(X(FINTIP_P + Vector((0.05, 0.08, 0)), s)),
                    0.04, "FinTip_" + sd))                                            # FinTip hinge
    return out


FIN_AXIS = Vector((math.cos(math.radians(65)) * math.cos(math.radians(14)),
                   math.sin(math.radians(65)) * math.cos(math.radians(14)), math.sin(math.radians(14))))


def axis_euler(axis, deg):
    """axis-angle -> kit (pitch, yaw, roll) for Rq = Rz(yaw) Rx(pitch) Ry(roll)"""
    x, y, z = Vector(axis).normalized()
    t = math.radians(deg)
    c, s_, C = math.cos(t), math.sin(t), 1 - math.cos(t)
    R = [[c + x * x * C, x * y * C - z * s_, x * z * C + y * s_],
         [y * x * C + z * s_, c + y * y * C, y * z * C - x * s_],
         [z * x * C - y * s_, z * y * C + x * s_, c + z * z * C]]
    p = math.asin(max(-1.0, min(1.0, R[2][1])))
    return (math.degrees(p), math.degrees(math.atan2(-R[0][1], R[1][1])), math.degrees(math.atan2(-R[2][0], R[2][2])))


def fin_rot(up, side):
    """v1d flap: + = UP. The fan hinges about its own inner edge (the P4 line), not the world Y axis - a Y roll swept
    the trailing panels' inner edges into the flank (pose_try: 40-140 pairs); this hinge leaves only hub-capsule ones"""
    s = 1 if side == "L" else -1
    p, yw, r = axis_euler(Vector((s * FIN_AXIS.x, FIN_AXIS.y, FIN_AXIS.z)), -s * up)
    return (p, yw, r)


HEAD_XF = []


# ------------------------------------------------------------------ animation (plan review section 7)
# References (owner rule; _review/ANIM_REFERENCES_1014.md):
# - #8 "Avatar" banshee flight: one wing stroke ~0.8-0.9 s, upstroke to a high V, downstroke ~25 deg below level, the
#   body barely bobs, the head stays level, the long tail streams almost straight with a small lagging bend.
# - #9 Children of the Sea humpback (Sakugabooru #111889): a heavy body rises in ~2 s and subsides 2-3x slower, with no
#   body bounce (overshoot only on the fluke tip).
# - #3 Sea Beasts roar: the head drops and tucks, lifts, and the jaw opens a beat AFTER the head lift.
# Kit signs: + pitch = nose DOWN on Spine/Chest/Neck/Head, + = tail UP on Tail1-4/Fluke; Jaw key = total - JAW_OPEN;
# fins flap about the fan's inner-edge hinge (fin_pose), + = up; dorsal + = erect (tip forward-up).
import petkit as pk

TAILS = ["Tail1", "Tail2", "Tail3", "Tail4"]
# fins_note: the fan's trailing panel (P4, az 66) lies along the flank, so ANY sweep-back yaw swings it into the body
# (pose_try: 8 deg = 106-119 pairs, 30 deg = 450). The plan's "fold back 18" (roar gather) and "sweep back 30" (plunge)
# are played as a DOWN fold (Fin down + FinTip down) instead; the forward sweep of the roar snap is kept.


def kit_euler(R):
    p = math.asin(max(-1.0, min(1.0, R[2][1])))
    return (math.degrees(p), math.degrees(math.atan2(-R[0][1], R[1][1])), math.degrees(math.atan2(-R[2][0], R[2][2])))


def fin_pose(up=0.0, back=0.0, side="L"):
    """flap UP about the fan hinge (inner edge, P4 line), then sweep BACK (yaw, tips toward the tail)"""
    s = 1 if side == "L" else -1
    ax = Vector((s * FIN_AXIS.x, FIN_AXIS.y, FIN_AXIS.z))
    R = Matrix.Rotation(math.radians(s * back), 3, "Z") @ Matrix.Rotation(math.radians(-s * up), 3, ax)
    return kit_euler(R)


def fins(k, f, up=0.0, back=0.0, tip=0.0, dl=0.0, dr=0.0, tip_l=0.0, tip_r=0.0):
    for sd, d, dt in (("L", dl, tip_l), ("R", dr, tip_r)):
        k.key("Fin_" + sd, f, rot=fin_pose(up + d, back, sd))
        k.key("FinTip_" + sd, f, rot=fin_pose(tip + dt, 0.0, sd))


def body(k, f, z=0.0, y=0.0, spine=0.0, roll=0.0, chest=0.0, neck=0.0, head=0.0, neck_yaw=0.0, head_yaw=0.0,
         jaw=None):
    """jaw = TOTAL opening (deg); modelled JAW_OPEN, so the key is total - JAW_OPEN (shut = -JAW_OPEN)"""
    k.key("Spine", f, rot=(spine, 0, roll), loc=(0, y, z))
    k.key("Chest", f, rot=(chest, 0, 0))
    k.key("Neck", f, rot=(neck, neck_yaw, 0))
    k.key("Head", f, rot=(head, head_yaw, 0))
    if jaw is not None:
        k.key("Jaw", f, rot=(max(0.0, jaw) - JAW_OPEN, 0, 0))


def tails(k, f, p=(0, 0, 0, 0), y=(0, 0, 0, 0), fluke=0.0, fluke_roll=0.0):
    for b, pp, yy in zip(TAILS, p, y):
        k.key(b, f, rot=(pp, yy, 0))
    k.key("Fluke", f, rot=(fluke, 0, fluke_roll))


def dorsals(k, f, e=0.0):
    for nm in ("Dorsal1", "Dorsal2", "Dorsal3"):
        k.key(nm, f, rot=(e, 0, 0))


def curve(keys, f):
    """smoothstep through (frame, value) keys"""
    if f <= keys[0][0]:
        return keys[0][1]
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            t = (f - f0) / float(f1 - f0)
            return v0 + (v1 - v0) * t * t * (3 - 2 * t)
    return keys[-1][1]


def ground_lift(k, n, target=0.02):
    """FLOOR RULE (Orca / Kraken): raise the body on any frame where a vertex dips under target"""
    import bpy
    sc = bpy.context.scene
    pb = k.arm.pose.bones["Spine"]
    R0 = k.arm.data.bones["Spine"].matrix_local.to_quaternion()
    k.bake_bezier_now()
    fix = []
    for f in range(0, n + 1):
        sc.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        ev = k.main.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        z = min((mw @ v.co).z for v in me.vertices)
        ev.to_mesh_clear()
        if z < target:
            fix.append((f, R0 @ pb.location, target - z))
    for f, cur, lift in fix:
        k.key("Spine", f, loc=(cur.x, cur.y, cur.z + lift))


def idle(k):
    """SKY DRIFT: heave +-0.03 (2 cycles), fins breathe +-8 (FinTip 4 f late, +-5), a tail micro-wave; ONE slow look
    left (f20-36) then ONE look right (f40-56), back by f62 (never a shake); the crown glint (head lifts, fins rise,
    event glow f78); a fluke flick f92-112 with a small overshoot."""
    n = 120
    k.new_action("idle", n, True)
    look = [(0, 0), (20, 0), (28, 1), (36, 1), (40, 0), (48, -1), (56, -1), (62, 0), (120, 0)]
    glint = [(0, 0), (70, 0), (78, 1), (84, 1), (90, 0), (120, 0)]
    flick = [(0, 0), (92, 0), (100, 1), (106, -0.15), (112, 0), (120, 0)]
    for f in range(0, n + 1, 2):
        u = f / n
        lk, gl, fl = curve(look, f), curve(glint, f), curve(flick, f)
        body(k, f, z=0.03 * math.sin(4 * math.pi * u), neck=-3 * gl, head=-6 * gl,
             neck_yaw=6 * lk, head_yaw=18 * lk, jaw=JAW_OPEN)
        w = [math.sin(4 * math.pi * (u - 0.08 * i)) for i in range(5)]
        tails(k, f, (2 * w[0], 3 * w[1], 5 * w[2] + 8 * fl, 7 * w[3] + 12 * fl), fluke=8 * w[4] + 16 * fl)
        fins(k, f, up=8 * math.sin(4 * math.pi * u) + 6 * gl, tip=5 * math.sin(4 * math.pi * (u - 4.0 / n)))
        dorsals(k, f, 0.0)
    ground_lift(k, n)
    k.finish()
    k.events["idle"] = {"glow": round(78 / n, 3)}


def swim(k):
    """MANTA FLIGHT: the wing-fins drive it - Fin +26 / -18 (the -20 limit), FinTip +-16 lagging 4 f, the power
    DOWNstroke takes 45 % of the cycle; the body heaves up at the end of the downstroke; a low vertical wave
    Spine / Tail1-4 (+-2 / 4 / 7 / 10 / 14, lag 0.08) in phase with the fins, the fluke +-10 lagging; the head is
    stabilised (counter-pitch) and the dorsals are rigid (ref 8: the tail streams almost straight)."""
    n = 36

    def ph45(u):
        u %= 1.0
        return 0.5 * u / 0.45 if u < 0.45 else 0.5 + 0.5 * (u - 0.45) / 0.55
    k.new_action("swim", n, True)
    for f in range(0, n + 1, 2):
        u = f / n
        ph = ph45(u)
        stroke = math.cos(2 * math.pi * ph)                 # +1 = top of the upstroke, -1 = bottom of the downstroke
        fin_up = 4 + 22 * stroke                            # +26 .. -18
        tip = 16 * math.cos(2 * math.pi * ph45(u - 4.0 / n))
        c = [math.cos(2 * math.pi * ph45(u - 0.08 * i)) for i in range(6)]
        sp = 2 * c[0]
        body(k, f, z=0.02 - 0.02 * math.cos(2 * math.pi * (ph - 0.5)), spine=sp, chest=0.0, neck=-0.4 * sp,
             head=-0.6 * sp, jaw=JAW_OPEN)
        tails(k, f, (4 * c[1], 7 * c[2], 10 * c[3], 14 * c[4]), fluke=10 * c[5])
        fins(k, f, up=fin_up, tip=tip)
        dorsals(k, f, 0.0)
    ground_lift(k, n)
    k.finish()
    return 0.0


def roar(k):
    """RIPPLE ROAR (66 f, in place): gather (root sinks, chin tucks, fins fold back, tail cocked down) -> a lifting
    ripple runs Fluke -> ... -> Head (1.25 f lag) and reaches the head at f22 -> the jaw opens a beat after the head lift
    (f24 -> 40 total at f27), the fins SNAP to full span and the dorsals erect (event roar f26) -> hold with jaw buzz,
    fin-tip quiver and a tail shiver -> release with a fin overshoot."""
    n = 66
    k.new_action("roar", n, False)
    chain = ["Fluke", "Tail4", "Tail3", "Tail2", "Tail1", "Spine", "Chest", "Neck", "Head"]
    pk_ = {b: 12 + 1.25 * i for i, b in enumerate(chain)}

    def pulse(b, f):                                         # -8 at the bone's peak, 0 three frames either side
        d = abs(f - pk_[b])
        return -8 * max(0.0, 1 - d / 3.0) ** 2 if b not in ("Neck", "Head") else 0.0
    frames = sorted(set(list(range(0, n + 1, 2)) + list(range(10, 31))))
    for f in frames:
        g = curve([(0, 0), (12, 1), (22, 0), (66, 0)], f)                    # gather
        hl = curve([(0, 0), (12, 0), (22, 1), (50, 1), (60, 0), (66, 0)], f)  # head lift, held
        jaw = curve([(0, JAW_OPEN), (24, JAW_OPEN), (27, 40), (50, 40), (60, JAW_OPEN), (66, JAW_OPEN)], f)
        if 28 <= f <= 50:
            jaw += 2 if (f // 3) % 2 == 0 else -2
        z = curve([(0, 0), (12, -0.05), (22, 0.03), (50, 0.03), (60, 0), (66, 0)], f)
        body(k, f, z=z, spine=4 * g + pulse("Spine", f), chest=pulse("Chest", f),
             neck=6 * g - 6 * hl, head=8 * g - 10 * hl, jaw=jaw)
        snap = curve([(0, 0), (22, 0), (26, 1), (50, 1), (58, -0.15), (66, 0)], f)
        q = (3 if (f // 2) % 2 == 0 else -3) if 28 <= f <= 50 else 0
        fins(k, f, up=-12 * g + 22 * snap, back=-10 * snap, tip=-8 * g + q)   # v1: NO sweep-back (see fins_note)
        sh = (5 if (f // 2) % 2 == 0 else -5) if 28 <= f <= 50 else 0
        tails(k, f, (-8 * g + pulse("Tail1", f), -10 * g + pulse("Tail2", f), -12 * g + pulse("Tail3", f),
                     pulse("Tail4", f) + sh), fluke=pulse("Fluke", f) + sh)
        dorsals(k, f, 8 * snap)
    ground_lift(k, n)
    k.finish(loop=False)
    k.events["roar"] = {"roar": round(26 / n, 3)}


def act_sounding(k):
    """COMET SOUNDING (120 f, in place): rise & ignite (event ignite f12) -> hold the breath -> THE PLUNGE, a travelling
    wave head -> tail (3 f lag; event plunge f28) into a held FLUKE-UP arch with two slow fluke swings (starfall1/2
    f48 / f60) -> the slip (the fluke sweeps down past rest, splash f78) -> resurface, a counter-wave tail -> head
    (glow f96) with two fin sculls -> settle exactly to rest. Heavy-mass timing: the rise is quick, every fall is
    2-3x slower (ref 9)."""
    n = 120
    k.new_action("act_sounding", n, False)
    C = {
        "z": [(0, 0), (14, 0.06), (22, 0.07), (40, 0.0), (82, 0.0), (96, 0.02), (112, 0.0), (120, 0)],
        "spine": [(0, 0), (14, -5), (22, -5), (32, 22), (70, 22), (80, 6), (90, -6), (110, 0), (120, 0)],
        "chest": [(0, 0), (14, -3), (22, -3), (30, 6), (70, 6), (80, 2), (92, -3), (110, 0), (120, 0)],
        "neck": [(0, 0), (14, -4), (22, -4), (28, 10), (70, 10), (80, 4), (94, -4), (112, 0), (120, 0)],
        "head": [(0, 0), (14, -8), (22, -8), (26, 18), (40, 18), (70, 20), (80, 6), (96, -8), (114, 0), (120, 0)],
        "jaw": [(0, JAW_OPEN), (10, JAW_OPEN + 4), (22, JAW_OPEN + 4), (28, 0), (72, 0), (86, JAW_OPEN),
                (120, JAW_OPEN)],
        "t1": [(0, 0), (14, -4), (22, -4), (34, 14), (70, 14), (80, -6), (92, 0), (120, 0)],
        "t2": [(0, 0), (14, -6), (22, -6), (36, 20), (70, 20), (80, -8), (94, 0), (120, 0)],
        "t3": [(0, 0), (14, -6), (22, -6), (38, 24), (70, 24), (80, -10), (96, 0), (120, 0)],
        "t4": [(0, 0), (22, 0), (40, 22), (70, 22), (80, -8), (98, 0), (120, 0)],
        "fl": [(0, 0), (22, 0), (40, 18), (70, 18), (80, -6), (100, 0), (120, 0)],
        "t4y": [(0, 0), (40, 0), (46, 6), (58, -6), (68, 0), (120, 0)],
        "flr": [(0, 0), (40, 0), (46, 4), (58, -4), (68, 0), (120, 0)],
        "fin": [(0, 0), (14, 14), (22, 14), (34, -10), (70, -10), (80, 0), (86, 12), (91, -4), (96, 12), (102, 0),
                (120, 0)],
        "back": [(0, 0), (120, 0)],                                       # v1: NO sweep-back (see fins_note)
        "tip": [(0, 0), (14, 8), (22, 8), (34, -10), (70, -10), (82, 0), (120, 0)],     # streamline = fold DOWN
        "dors": [(0, 0), (12, 8), (26, 8), (36, -6), (70, -6), (84, 0), (120, 0)],
    }
    for f in range(0, n + 1, 2):
        v = {c: curve(kk, f) for c, kk in C.items()}
        body(k, f, z=v["z"], spine=v["spine"], chest=v["chest"], neck=v["neck"], head=v["head"], jaw=v["jaw"])
        tails(k, f, (v["t1"], v["t2"], v["t3"], v["t4"]), (0, 0, 0, v["t4y"]), fluke=v["fl"], fluke_roll=v["flr"])
        fins(k, f, up=v["fin"], back=v["back"], tip=v["tip"])
        dorsals(k, f, v["dors"])
    ground_lift(k, n)
    k.finish(loop=False)
    k.events["act_sounding"] = {"ignite": round(12 / n, 3), "plunge": round(28 / n, 3), "starfall1": round(48 / n, 3),
                                "starfall2": round(60 / n, 3), "splash": round(78 / n, 3), "glow": round(96 / n, 3)}


def anim(k):
    idle(k)
    stride = swim(k)
    roar(k)
    act_sounding(k)
    return stride
