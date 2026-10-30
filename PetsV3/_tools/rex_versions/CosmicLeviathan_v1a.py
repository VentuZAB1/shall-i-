# Cosmic Leviathan v1 (Celestial egg SECRET 1 %, 2026-10-14) - "NEBULA SOVEREIGN" (plan review:
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
SEG = 24
# body centreline (curveloft stations y, z, hw, hh) - a true S: rearing neck, belly trough, flattening tail
ST = [(-0.86, 1.12, 0.19, 0.19), (-0.76, 1.00, 0.21, 0.22), (-0.64, 0.84, 0.25, 0.27), (-0.46, 0.64, 0.30, 0.34),
      (-0.12, 0.42, 0.25, 0.27), (0.22, 0.36, 0.20, 0.21), (0.54, 0.44, 0.15, 0.17), (0.84, 0.56, 0.105, 0.13),
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
FINTIP_P = Vector((0.59, -0.22, 0.61))
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


def ys(T, y0, y1, step=0.04):
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
    for y in ys(T, y0, y1, 0.03):
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
    B.add(c, (0.052 * sc, 0.008, 0.024 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0135 * sc), AZURE, bone, R=R, studs=[], role="detail", bevel=0.003)
    B.add(c + n * 0.011 - t2 * 0.018 * sc, (0.013 * sc, 0.004, 0.006 * sc), STAR, bone, R=R, studs=[], role="detail",
          bevel=0.002)
    B.add(c + n * 0.011 + t2 * 0.004, (0.006 * sc, 0.004, 0.0094 * sc), BLACK, bone, R=R, studs=[], role="detail",
          bevel=0.002)


def panel(B, a, b, hw0, th0, colors, bones, splits, n_up, top_w=0.25, top_t=0.6, off=0.0, tip_spike=None):
    """a tapered fin panel a -> b split along its length into colour/bone pieces at the fractions `splits`
    (len(colors) = len(splits) + 1); chord half hw0 at the root -> hw0*top_w at the tip, half-thickness th0 -> th0*top_t;
    the chord lies across the panel in the plane normal to n_up; offset `off` along n_up"""
    a, b = Vector(a), Vector(b)
    d = (b - a).normalized()
    n_up = Vector(n_up).normalized()
    side = n_up.cross(d).normalized()
    a, b = a + n_up * off, b + n_up * off
    fr = [0.0] + list(splits) + [1.0]
    out = []
    for i, (c, bn) in enumerate(zip(colors, bones)):
        t0, t1 = fr[i], fr[i + 1]
        p0, p1 = a.lerp(b, t0), a.lerp(b, t1)
        w0, w1 = hw0 * (1 - (1 - top_w) * t0), hw0 * (1 - (1 - top_w) * t1)
        h0, h1 = th0 * (1 - (1 - top_t) * t0), th0 * (1 - (1 - top_t) * t1)
        smooth = c in (DEEP, AZURE, STAR, GOLD)
        kw = dict(studs=[], nostud=True, role="limb") if smooth else {}
        out.append(B.seg(p0 - d * (0.01 if i else 0.0), p1 + d * (0.01 if i < len(colors) - 1 else 0.0), w0, h0, c, bn,
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
                            min(Lf.length, b + (0.06 if j1 is not None else 0)), HIDE, bn, j0=j0, j1=j1))
    # saddle armour: segmented top plates (zlo +0.25), one+ per bone, 0.03 plum gaps (NOT glowing seams)
    cuts = [sy(-0.78), sy(-0.66), sy(-0.48), sy(-0.30), sy(-0.02), sy(0.38), sy(0.74), sy(1.06), sy(1.22), sy(1.30)]
    owner = ["Neck", "Chest", "Chest", "Spine", "Spine", "Tail1", "Tail2", "Tail3", "Tail4"]
    for (a, b), bn in zip(zip(cuts, cuts[1:]), owner):
        Lf.band(B, a + 0.015, b - 0.015, ARMOR, bn, zlo=0.25, grow=0.008)
    # belly: ivory bottom band (zhi -0.50) per bone + BELLY_D scute gap bars every ~0.12
    bcuts = [sy(-0.86), sy(-0.66), sy(-0.30), sy(0.38), sy(0.74), sy(0.92)]
    bown = ["Neck", "Chest", "Spine", "Tail1", "Tail2"]
    for (a, b), bn in zip(zip(bcuts, bcuts[1:]), bown):
        Lf.band(B, a, b, BELLY, bn, zlo=-1.0, zhi=-0.50, grow=0.008)
    s = sy(-0.76)
    while s < sy(0.54):
        y = Lf.at(s)[0].y
        bn = next(b for b, y0, y1 in SPLIT if y0 <= y < y1)
        Lf.band(B, s - 0.01, s + 0.01, BELLY_D, bn, zlo=-1.0, zhi=-0.52, grow=0.011, inset=0.01)
        s += 0.12
    # ================= SKULL (Head): its own tube, plum sides, obsidian cap, nasal plates, nostrils
    skull = ytube(B, SKULL, -0.78, -1.32, HIDE, "Head")
    yband(B, SKULL, -0.80, -1.06, ARMOR, "Head", zlo=0.30, grow=0.008)
    for yy, hw in ((-1.12, 0.045), (-1.20, 0.04), (-1.27, 0.035)):
        p, nn = surf_hit(B, [skull], (0, yy, 1.6), (0, 0, -1))
        Rn = bk.frame_from(p, p + Vector((0, -1, 0)), nn)
        B.add(p + nn * 0.002, (hw, 0.008, 0.032), ARMOR, "Head", R=Rn, role="detail", bevel=0.006)
    for s_ in (1, -1):
        B.add((s_ * 0.05, -1.32, 1.16), (0.014, 0.012, 0.008), BLACK, "Head", studs=[], role="detail", bevel=0.003)
    # throat (Head, under the skull behind the jaw) - ivory
    ytube(B, [(-0.80, 1.05, 0.15, 0.08), (-0.88, 1.03, 0.18, 0.07)], -0.80, -0.88, BELLY, "Head")
    # ================= JAW (underbite, 6 deg open): plum, obsidian mandible plates, ivory underside, mouth floor
    ytube(B, JAWT, -0.84, -1.36, HIDE, "Jaw", xf=jawpt)
    yband(B, JAWT, -0.86, -1.34, BELLY, "Jaw", zlo=-1.0, zhi=-0.30, grow=0.006, xf=jawpt)
    for s_ in (1, -1):
        for y0, y1 in ((-0.90, -1.06), (-1.10, -1.26)):
            pa = jawpt(Vector((s_ * (tab(JAWT, y0)[1] + 0.004), y0, 1.02)))
            pb = jawpt(Vector((s_ * (tab(JAWT, y1)[1] + 0.004), y1, 1.02)))
            B.bar(pa, pb, Vector((s_, 0, 0)), 0.05, 0.006, ARMOR, "Jaw", bevel=0.004)          # mandible plates
    B.add(jawpt(Vector((0, -1.12, 1.058))), (0.12, 0.20, 0.006), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    B.add((0, -1.12, 1.062), (0.10, 0.20, 0.006), MOUTH, "Head", studs=[], role="detail", bevel=0.003)   # roof
    # tusks (lower jaw, outside the snout), lower fangs (rim, overlapping the upper lip) + upper teeth (inside)
    for s_ in (1, -1):
        B.spike(jawpt(Vector((s_ * 0.118, -1.31, 1.05))), (0, -0.25, 1), 0.11, 0.017, IVORY, "Jaw", top=(0.15, 0.15))
        for i, yy in enumerate((-1.24, -1.17, -1.10, -1.04)):
            w = tab(JAWT, yy)[1] - 0.012
            B.spike(jawpt(Vector((s_ * w, yy, 1.05))), (s_ * 0.1 * (i % 2), -0.1, 1), 0.05 + 0.02 * (i % 2), 0.013,
                    IVORY, "Jaw", top=(0.15, 0.15))
        for i, yy in enumerate((-1.28, -1.21, -1.135, -1.07, -1.01, -0.96)):
            w = tab(SKULL, yy)[1] - 0.03
            ang = math.radians(8 * (1 if i % 2 else -1))
            B.spike((s_ * w, yy, 1.07), (0, math.sin(ang), -1), 0.035 + 0.015 * (i % 2), 0.012, IVORY, "Head",
                    top=(0.15, 0.15))
    # ================= brows (V, ARMOR_D), azure slit eyes
    for s_ in (1, -1):
        B.bar((s_ * 0.18, -0.93, 1.385), (s_ * 0.05, -1.04, 1.325), Vector((0, -0.35, 1)), 0.05, 0.02, ARMOR_D, "Head",
              bevel=0.008, role="detail")
        c0 = Vector((s_ * 0.155, -1.00, 1.29))
        n0 = Vector((s_ * math.cos(math.radians(25)), -math.sin(math.radians(25)), 0.15)).normalized()
        p, nn = surf_hit(B, [skull], c0 + n0 * 0.3, -n0)
        slit_eye(B, p + nn * 0.004, nn, s_)
        ANCH["Eye_" + ("L" if s_ > 0 else "R")] = tuple(p + nn * 0.02)
    # ================= COMET CROWN (hero, the only gold): closed band, 6 points, comet horn, star gem
    kwg = dict(studs=[], nostud=True, role="limb")
    for y in (-1.00, -0.84):                                                                # front + back bars
        B.add((0, y, 1.365), (0.17, 0.0175, 0.035), GOLD, "Head", bevel=0.008, **kwg)
    for s_ in (1, -1):
        B.add((s_ * 0.19, -0.92, 1.36), (0.0175, 0.08, 0.035), GOLD, "Head", bevel=0.008, **kwg)   # side bars
        for y in (-1.00, -0.84):
            B.add((s_ * 0.175, y, 1.365), (0.03, 0.03, 0.04), GOLD, "Head", bevel=0.01, **kwg)     # corner blocks
        for (x, y, z, h, sp) in ((0.15, -0.99, 1.40, 0.10, 0), (0.20, -0.92, 1.39, 0.12, 20), (0.15, -0.85, 1.39, 0.09, 0)):
            d = Vector((s_ * math.sin(math.radians(sp)), math.sin(math.radians(15)), 1)).normalized()
            B.spike((s_ * x, y, z - 0.02), d, h, 0.030, GOLD, "Head", top=(0.12, 0.12), **kwg)
    B.seg((0, -0.95, 1.37), (0, -0.80, 1.52), 0.055, 0.045, GOLD, "Head", side=(1, 0, 0), top=(0.8, 0.8),
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
        panel(B, a, b, 0.07, 0.015, [ARMOR, AZURE], ["Head", "Head"], [0.55], nup, top_w=0.3, top_t=0.7,
              tip_spike=(0.05, 0.016))
    # ================= WING-FINS (signature): 4-panel flying-fish fan per side, Fin (plum) / FinTip (light)
    for s_, sd in ((1, "L"), (-1, "R")):
        h0 = X(HUB, s_)
        p, nn = surf_hit(B, hull, h0 + Vector((s_ * 0.3, 0, -0.05)), (-s_, 0, 0.15))
        hub = p - nn * 0.02
        for i, (az, el, ln, hc, off) in enumerate(((35, 8, 0.86, 0.07, 0.008), (50, 7, 0.76, 0.09, 0.004),
                                                   (65, 6, 0.62, 0.09, 0.0), (78, 5, 0.46, 0.08, -0.004))):
            d = Vector((s_ * math.cos(math.radians(az)) * math.cos(math.radians(el)),
                        math.sin(math.radians(az)) * math.cos(math.radians(el)), math.sin(math.radians(el))))
            tip = hub + d * ln
            nup = Vector((0, 0, 1)) - d * d.z
            if i == 0:
                panel(B, hub, tip, hc, 0.025, [ARMOR, ARMOR], ["Fin_" + sd, "FinTip_" + sd], [0.45], nup, off=off,
                      tip_spike=(0.06, 0.02))
                ANCH["FinEnd_" + sd] = tuple(tip + d * 0.06)
            else:
                panel(B, hub, tip, hc, 0.025, [HIDE, DEEP, AZURE], ["Fin_" + sd, "FinTip_" + sd, "FinTip_" + sd],
                      [0.50, 0.57], nup, off=off, tip_spike=(0.05, 0.018))
    # ================= DORSALS (3 falcate fins): ARMOR 0-45 % / HIDE -70 % / DEEP step / AZURE + STAR point
    for nm, (yf, yb), tip in (("Dorsal1", (-0.40, -0.20), (0, -0.10, 1.22)),
                              ("Dorsal2", (-0.04, 0.18), (0, 0.28, 0.98)),
                              ("Dorsal3", (0.46, 0.62), (0, 0.74, 0.86))):
        Rf = Lf.surf(sy(yf), math.pi / 2) - Vector((0, 0, 0.03))
        Rb = Lf.surf(sy(yb), math.pi / 2) - Vector((0, 0, 0.03))
        T = Vector(tip)
        for c, h0_, h1_ in ((ARMOR, 0.0, 0.45), (HIDE, 0.45, 0.70), (DEEP, 0.70, 0.75), (AZURE, 0.75, 0.97)):
            F0, B0 = Rf.lerp(T, h0_), Rb.lerp(T, h0_)
            F1, B1 = Rf.lerp(T, h1_), Rb.lerp(T, h1_)
            m0, m1 = (F0 + B0) / 2, (F1 + B1) / 2
            w0, w1 = max(0.012, (B0 - F0).length / 2), max(0.008, (B1 - F1).length / 2)
            t0, t1 = 0.04 - 0.018 * h0_, 0.04 - 0.018 * h1_
            side = (B0 - F0).normalized()
            smooth = c in (DEEP, AZURE)
            kw = dict(studs=[], nostud=True, role="limb") if smooth else {}
            B.seg(m0 - (m1 - m0).normalized() * 0.008, m1, w0, t0, c, nm, side=side, top=(w1 / w0, t1 / t0), **kw)
            if c == HIDE:                                                                     # lit trailing edge
                B.bar(B0 - side * 0.012, B1 - side * 0.008, Vector((1, 0, 0)), 0.02, t0 + 0.004, AZURE, nm,
                      studs=[], nostud=True, bevel=0.003)
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
        panel(B, root, tip, 0.10, 0.03, [ARMOR, HIDE, DEEP, AZURE], ["Fluke"] * 4, [0.34, 0.66, 0.72], nup,
              top_w=0.35, top_t=0.5, tip_spike=(0.06, 0.02))
        ANCH["Fluke" + sd] = tuple(tip + d * 0.06)
    B.build()
    mn, mx = k.bounds()
    pitch = 0.2243 * (mx.z - mn.z) / HEIGHT
    bk.stud_skin(k, pitch)
    return {"TH": round(B.th, 3), "pitch": round(pitch, 4), "H": round(mx.z - mn.z, 3), "lowest": round(mn.z, 3)}


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
    out = [((0.22, -0.90, 1.07), (-0.22, -0.90, 1.07), 0.07, "Jaw")]                 # jaw hinge
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((tuple(X(HUB, s)), tuple(X(HUB + Vector((0.10, 0.06, 0.0)), s)), 0.10, "Fin_" + sd))   # fin hub
        out.append((tuple(X(FINTIP_P - Vector((0.05, 0.08, 0)), s)), tuple(X(FINTIP_P + Vector((0.05, 0.08, 0)), s)),
                    0.04, "FinTip_" + sd))                                            # FinTip hinge
    return out


HEAD_XF = []
