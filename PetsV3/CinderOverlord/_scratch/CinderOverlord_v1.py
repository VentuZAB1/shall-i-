# Cinder Overlord (Magma / Fire egg ULTRA-RARE 0.5 %, 2026-10-27) - plan _review/CinderOverlord_plan.md v2. A volcanic
# serpent-dragon in the FIERCE studded style: no legs, no wings. The front third rears up in a cobra S (chest on the
# ground, neck rising, wedge head level at the top); the rear lies on the ground in a lateral S down to a thin tail with
# a rose ember spike. Mauve-obsidian studded hide, dark obsidian scale bands + small dorsal spikes, pale belly scutes,
# six pairs of rose lava vent slits along the flanks (hot centres), two small clawed forearms at the chest, a heavy
# wedge skull (obsidian brow ridges, rose slit eyes, four ivory fangs) and THE HERO: a crown of five smooth obsidian
# plates, each framed in house gold, the centre plate tipped rose-hot. No glow (embers / smoke = Studio VFX).
import math
from mathutils import Vector, Matrix, Euler, Quaternion

DISPLAY = "Cinder Overlord"
MOTION = "Walk"
RIG = "serpent"
HEIGHT = 10.5                # studs to the crown tip of the rearing head (H_MODEL)

# Blender colours (Roblox renders ~0.6x darker)
PLUM_OBS = (182, 132, 172)   # body scales (studded)
OBS_D = (96, 84, 96)         # crown plates, brow ridges, dorsal spikes, scale bands
PALE_S = (226, 210, 214)     # belly scutes, throat
ROSE = (255, 96, 150)        # THE accent: vent slits, eye slits, crown inner edges
ROSE_H = (255, 190, 214)     # vent hot centres, the ember tip, the centre crown gem
GOLD = (255, 196, 50)        # THE hero: the gold frames of the crown plates (crown only)
GOLD_D = (214, 150, 30)      # inner faces of the gold frames
BLACK = (14, 14, 22)         # claws, eye sockets, pupils, nostrils
IVORY = (238, 234, 220)      # fangs
MOUTH = (96, 26, 30)         # mouth

H_MODEL = 2.10
ANCH = {}

# ---- the spine curve. Rear (on the ground, lateral S): Spine -> Body1..4 -> Tail1..4 -> tip
CHAIN = ["Spine", "Body1", "Body2", "Body3", "Body4", "Tail1", "Tail2", "Tail3", "Tail4"]
CP = [Vector(p) for p in ((0.00, -0.24, 0.0), (0.08, 0.10, 0.0), (0.24, 0.44, 0.0), (0.24, 0.80, 0.0),
                          (0.06, 1.12, 0.0), (-0.18, 1.38, 0.0), (-0.32, 1.66, 0.0), (-0.28, 1.94, 0.0),
                          (-0.12, 2.16, 0.0), (0.04, 2.30, 0.0))]
RAD = [0.230, 0.218, 0.200, 0.180, 0.158, 0.134, 0.108, 0.082, 0.060, 0.042]
for _i, _p in enumerate(CP):
    _p.z = RAD[_i] * 0.96                       # lying on the ground (slightly flattened belly)
CP[9].z = 0.16                                  # the tail tip curls up
# front rise (cobra S): chest curve -> Neck1..3 -> throat
FRONT = [Vector(p) for p in ((0, -0.24, 0.207), (0, -0.47, 0.33), (0, -0.55, 0.64), (0, -0.54, 0.98),
                             (0, -0.47, 1.31), (0, -0.50, 1.60))]
FRAD = [0.230, 0.226, 0.212, 0.192, 0.172, 0.158]
NECKS = ["Neck1", "Neck2", "Neck3"]
THROAT = Vector((0, -0.50, 1.60))


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def frame_of(d, up=(0, 0, 1)):
    """orthonormal (side, upv) around direction d"""
    d = Vector(d).normalized()
    u = Vector(up)
    if abs(d.dot(u)) > 0.95:
        u = Vector((0, -1, 0))
    side = d.cross(u).normalized()
    upv = side.cross(d).normalized()
    return side, upv


def oval(c, side, upv, rw, rh, a0=0.0, a1=2 * math.pi, seg=18, n=2.2, off=0.0):
    closed = abs((a1 - a0) - 2 * math.pi) < 1e-6
    pts = []
    for i in range(seg if closed else seg + 1):
        a = a0 + (a1 - a0) * i / seg
        cs, sn = math.cos(a), math.sin(a)
        pts.append(c + side * ((rw + off) * math.copysign(abs(cs) ** (2.0 / n), cs)) +
                   upv * ((rh + off) * math.copysign(abs(sn) ** (2.0 / n), sn)))
    return pts


def body_seg(B, a, b, r0, r1, bone, color=None, ext0=0.0, ext1=0.0, flat=0.92, up=(0, 0, 1)):
    """smooth lofted body segment from a to b (radius r0 -> r1), ends extended + rounded to overlap neighbours"""
    a, b = Vector(a), Vector(b)
    L = (b - a).length
    d = (b - a) / L
    side, upv = frame_of(d, up)
    st = []                                              # (distance from a, radius factor, radius interpolation)
    if ext0 > 0:
        st += [(-ext0, 0.55, 0.0), (-ext0 * 0.55, 0.88, 0.0)]
    st += [(0.0, 1.0, 0.0), (L * 0.5, 1.0, 0.5), (L, 1.0, 1.0)]
    if ext1 > 0:
        st += [(L + ext1 * 0.55, 0.88, 1.0), (L + ext1, 0.55, 1.0)]
    rings = []
    for dist, kf, tt in st:
        r = (r0 + (r1 - r0) * tt) * kf
        rings.append(oval(a + d * dist, side, upv, r, r * flat))
    return B.tube(rings, color or PLUM_OBS, bone)


def band(B, a, b, r0, r1, bone, color, a0, a1, off=0.012, thick=0.02, up=(0, 0, 1), seg=10, flat=0.92, nr=3,
         nostud=True):
    """open shell strip on a body segment between angles a0..a1 (rad, 0 = side, pi/2 = top) - scutes / scale bands"""
    a, b = Vector(a), Vector(b)
    d = (b - a).normalized()
    side, upv = frame_of(d, up)
    rings = []
    for i in range(nr):
        t = i / (nr - 1.0)
        c = a.lerp(b, t)
        r = r0 + (r1 - r0) * t
        rings.append((oval(c, side, upv, r, r * flat, a0, a1, seg, off=off),
                      oval(c, side, upv, r, r * flat, a0, a1, seg, off=off - thick)))
    return B.tube(rings, color, bone, closed=False, nostud=nostud)


def surf_pt(a, b, r0, r1, t, ang, off=0.0, flat=0.92, up=(0, 0, 1)):
    """point + outward normal on the body segment surface at fraction t, angle ang (0 = +side, pi/2 = top)"""
    a, b = Vector(a), Vector(b)
    d = (b - a).normalized()
    side, upv = frame_of(d, up)
    r = r0 + (r1 - r0) * t
    n = (side * math.cos(ang) + upv * math.sin(ang) / flat).normalized()
    return a.lerp(b, t) + side * (r + off) * math.cos(ang) + upv * (r * flat + off) * math.sin(ang), n, d


def face_R(nn, up=(0, 0, 1)):
    y = -Vector(nn).normalized()
    z = Vector(up) - y * y.dot(Vector(up))
    if z.length < 1e-3:
        z = Vector((0, 1, 0)) - y * y.y
    z.normalize()
    return Matrix((y.cross(z), y, z)).transposed()


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


def vent(B, p, n, d, bone, L=0.095, w=0.026):
    """rose lava vent slit (flush): rose body, hot centre line; slanted back along the body"""
    n = Vector(n).normalized()
    dd = (Vector(d) - n * Vector(d).dot(n)).normalized()
    up = n.cross(dd).normalized()
    ax = (up * 0.85 + dd * 0.5).normalized()                 # slanted slit
    p0, p1 = p - ax * L / 2, p + ax * L / 2
    B.bar(p0, p1, n, w, 0.010, ROSE, bone, studs=[], nostud=True, role="detail", bevel=0.004)
    B.bar(p0 + ax * L * 0.18 + n * 0.006, p1 - ax * L * 0.18 + n * 0.006, n, w * 0.36, 0.008, ROSE_H, bone,
          studs=[], nostud=True, role="detail", bevel=0.002)


def plate_crown(B, base, up_d, back_d, h, w, bone, gem=False):
    """THE HERO piece: a smooth obsidian blade plate (pointed top) framed in gold, a rose inner edge line"""
    import blockkit as bk
    up_d, back_d = Vector(up_d).normalized(), Vector(back_d)
    side = up_d.cross(back_d).normalized()
    base = Vector(base)
    t = 0.030
    # obsidian blade (pentagon: base, shoulders at 55 %, point) - smooth, thick
    pts = [base - side * w, base - side * w * 0.95 + up_d * h * 0.55, base + up_d * h, base + side * w * 0.95 +
           up_d * h * 0.55, base + side * w]
    B.poly(pts, t, OBS_D, bone)
    # gold frame along the two upper edges and the two sides (front face, proud)
    nrm = up_d.cross(side).normalized()
    edges = [(pts[0], pts[1]), (pts[1], pts[2]), (pts[2], pts[3]), (pts[3], pts[4])]
    for (p, q) in edges:
        dv = (q - p).normalized()
        B.seg(p - dv * 0.012, q + dv * 0.012, 0.022, t * 0.5 + 0.010, GOLD, bone, side=nrm.cross(dv),
              studs=[], nostud=True, role="limb", rnd=0.25)
    # rose inner edge lines (inside the gold frame, on the front face)
    inner = [base.lerp(pp, 0.80) + up_d * h * 0.05 for pp in pts]
    for (p, q) in ((inner[1], inner[2]), (inner[2], inner[3])):
        B.bar(p + nrm * (t * 0.5 + 0.003), q + nrm * (t * 0.5 + 0.003), nrm, 0.016, 0.006, ROSE, bone, studs=[],
              nostud=True, role="detail", bevel=0.002)
    if gem:
        B.spike(pts[2] - up_d * 0.03, up_d + nrm * 0.1, 0.075, 0.026, ROSE_H, bone, nostud=True)
    return pts[2]


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=505, tier=5, plates=False, th=0.42)
    # ================= rear body on the ground (lateral S): lofted segments, obsidian back bands, pale scutes
    for i in range(9):
        a, b = CP[i], CP[i + 1]
        bone = CHAIN[i]
        body_seg(B, a, b, RAD[i], RAD[i + 1], bone, ext0=0.0 if i == 0 else RAD[i] * 0.55, ext1=RAD[i + 1] * 0.45)
        # dark obsidian scale band over the back (split per segment = scale bands)
        band(B, a.lerp(b, 0.08), a.lerp(b, 0.86), RAD[i] * 0.99, RAD[i + 1] * 1.0, bone, OBS_D,
             math.radians(48), math.radians(132), off=0.010, thick=0.024, nostud=False)
        # pale belly scutes along the flattened underside (visible from the side as a light lower edge)
        band(B, a.lerp(b, 0.05), a.lerp(b, 0.92), RAD[i], RAD[i + 1], bone, PALE_S, math.radians(205),
             math.radians(335), off=0.008, thick=0.02)
    # tail ember spike
    d = (CP[9] - CP[8]).normalized()
    tip0 = CP[9] - d * 0.03
    B.spike(tip0, d + Vector((0, 0.3, 0.6)), 0.16, 0.045, ROSE, "Tail4", nostud=True)
    B.spike(tip0 + (d + Vector((0, 0.3, 0.6))).normalized() * 0.09, d + Vector((0, 0.3, 0.6)), 0.10, 0.026, ROSE_H,
            "Tail4", nostud=True)
    ANCH["Tail_Tip"] = tuple(tip0 + (d + Vector((0, 0.3, 0.6))).normalized() * 0.18)
    # ================= front rise (Spine chest curve + Neck1..3): cobra S, pale throat scutes facing forward
    fb = ["Spine", "Spine", "Neck1", "Neck2", "Neck3"]
    for i in range(5):
        a, b = FRONT[i], FRONT[i + 1]
        body_seg(B, a, b, FRAD[i], FRAD[i + 1], fb[i], ext0=FRAD[i] * 0.5 if i else 0.0, ext1=FRAD[i + 1] * 0.5,
                 up=(0, 1, 0))
        band(B, a.lerp(b, 0.06), a.lerp(b, 0.92), FRAD[i], FRAD[i + 1], fb[i], PALE_S, math.radians(205),
             math.radians(335), off=0.008, thick=0.02, up=(0, 1, 0))                 # throat scutes (front)
        band(B, a.lerp(b, 0.10), a.lerp(b, 0.85), FRAD[i] * 0.99, FRAD[i + 1], fb[i], OBS_D, math.radians(48),
             math.radians(132), off=0.010, thick=0.024, up=(0, 1, 0), nostud=False)  # back bands (behind)
    # ================= dorsal spikes: small obsidian spikes down the back, shrinking to the tail
    for i, (bone, t, L) in enumerate((("Spine", 0.55, 0.13), ("Body1", 0.5, 0.12), ("Body2", 0.5, 0.11),
                                      ("Body3", 0.5, 0.095), ("Body4", 0.5, 0.08), ("Tail1", 0.5, 0.065))):
        j = CHAIN.index(bone)
        p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t, math.pi / 2, off=0.02)
        B.spike(p - n * 0.03, n + dv * 0.55, L + 0.03, 0.045 * (L / 0.13) + 0.012, OBS_D, bone, top=(0.12, 0.35))
    # ================= rose lava vents: 6 pairs along the flanks (slanted slits, hot centres)
    for vi, (bone, t) in enumerate((("Spine", 0.45), ("Body1", 0.5), ("Body2", 0.5), ("Body3", 0.5),
                                    ("Body4", 0.5), ("Tail1", 0.45))):
        j = CHAIN.index(bone)
        for s in (1, -1):
            ang = math.radians(18 if s > 0 else 162)
            p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t, ang, off=0.004)
            sc = RAD[j] / 0.23
            vent(B, p, n, dv, bone, L=0.11 * sc + 0.02, w=0.03 * sc + 0.006)
            if s > 0:
                ANCH["Vent_%d" % (vi + 1)] = (tuple(p + n * 0.03), bone)
    # ================= forearms: two small clawed arms at the chest (on the Spine curve)
    for s, side in ((1, "L"), (-1, "R")):
        sh = Vector((s * 0.16, -0.60, 0.50))
        el = Vector((s * 0.24, -0.70, 0.40))
        ha = Vector((s * 0.22, -0.80, 0.32))
        B.add(sh, (0.07, 0.07, 0.07), PLUM_OBS, "Arm_" + side, rnd=0.45)
        B.seg(sh, el, 0.052, 0.058, PLUM_OBS, "Arm_" + side, ext=0.03, ext1=0.02, top=(0.9, 0.9), rnd=0.4)
        B.seg(el, ha, 0.046, 0.05, OBS_D, "Claw_" + side, ext=0.02, ext1=0.02, top=(0.9, 0.9), rnd=0.4)
        B.add(ha, (0.05, 0.045, 0.04), OBS_D, "Claw_" + side, rnd=0.4)
        for gx in (-0.03, 0.0, 0.03):
            B.spike(ha + Vector((gx, -0.03, -0.01)), (gx * 2.5, -0.7, -0.9), 0.07, 0.014, BLACK, "Claw_" + side)
        ANCH["Claw_" + side] = (tuple(ha), tuple(el))
    # ================= head (throat pivot): wedge skull, heavy jaw, obsidian brows, rose slit eyes, fangs
    skull = B.seg((0, -0.52, 1.80), (0, -0.99, 1.735), 0.165, 0.125, PLUM_OBS, "Head", top=(0.62, 0.62),
                  ext=0.04, rnd=0.36)
    B.seg((0, -0.56, 1.905), (0, -0.95, 1.80), 0.06, 0.022, OBS_D, "Head", top=(0.55, 1.0), rnd=0.3)  # nasal ridge
    B.seg((0, -0.55, 1.70), (0, -0.95, 1.66), 0.13, 0.03, PALE_S, "Head", top=(0.65, 1.0), rnd=0.3, nostud=True)
    for s in (1, -1):                                                                   # cheek / jaw muscles
        B.add((s * 0.15, -0.62, 1.74), (0.05, 0.10, 0.08), PLUM_OBS, "Head", rot=(0, 0, s * 10), rnd=0.42)
        B.add((s * 0.042, -1.005, 1.765), (0.020, 0.010, 0.008), BLACK, "Head", rot=(0, -s * 25, -s * 20),
              studs=[], role="detail", bevel=0.003)                                     # nostril slits
    # jaw (open 6 deg at rest), pale underside, dark mouth, 2 lower fangs
    JR = Euler((math.radians(6), 0, 0), "XYZ").to_matrix()
    JP = Vector((0, -0.56, 1.67))

    def jp(p):
        return JP + JR @ Vector(p)
    B.seg(jp((0, 0.0, -0.01)), jp((0, -0.40, -0.03)), 0.130, 0.048, PLUM_OBS, "Jaw", top=(0.62, 0.8), ext=0.03,
          rnd=0.34)
    B.seg(jp((0, -0.02, -0.050)), jp((0, -0.38, -0.062)), 0.105, 0.016, PALE_S, "Jaw", top=(0.65, 1.0), rnd=0.3,
          nostud=True)
    B.seg(jp((0, -0.04, 0.028)), jp((0, -0.38, 0.010)), 0.095, 0.010, MOUTH, "Jaw", studs=[], role="detail",
          bevel=0.003, top=(0.6, 1))
    for s in (1, -1):
        B.spike(jp((s * 0.072, -0.33, 0.01)), JR @ Vector((0, -0.12, 1)), 0.12, 0.024, IVORY, "Jaw", nostud=True)
        B.spike(Vector((s * 0.088, -0.88, 1.70)), (0, -0.15, -1), 0.17, 0.030, IVORY, "Head", nostud=True)  # upper
    ANCH["Mouth"] = tuple(jp((0, -0.40, 0.02)))
    # eyes on the skull sides-front, under heavy obsidian V brows (20 deg inner-down)
    for s in (1, -1):
        ep, en = surf_hit(B, [skull], (s * 0.5, -0.70, 1.835), (-s, 0, 0))
        en = (en + Vector((0, -0.7, 0))).normalized()
        R = face_R(en) @ Euler((0, math.radians(-s * 20), 0), "XYZ").to_matrix()
        kw = dict(R=R, studs=[], role="detail")
        c = ep + Vector((0, 0, 0))
        B.add(c, (0.082, 0.010, 0.032), BLACK, "Head", bevel=0.005, **kw)                         # socket
        B.add(c + en * 0.008, (0.070, 0.007, 0.0185), ROSE, "Head", bevel=0.004, **kw)            # rose slit
        B.add(c + en * 0.013 + R @ Vector((-s * 0.012, 0, 0)), (0.008, 0.005, 0.017), BLACK, "Head",
              bevel=0.002, **kw)                                                                 # slit pupil
        Rb = face_R(en) @ Euler((0, math.radians(-s * 22), 0), "XYZ").to_matrix()
        B.add(c + en * 0.026 + Vector((0, 0, 0.045)), (0.105, 0.040, 0.030), OBS_D, "Head", R=Rb, role="limb",
              rnd=0.2, studs=[], nostud=True)                                                    # heavy brow
    # ================= THE HERO: crown of five obsidian plates framed in gold (own bones Crown_1..5)
    cb = Vector((0, -0.66, 1.905))
    tips = {}
    for i, (x, h, w, fan, back) in enumerate(((-0.13, 0.15, 0.050, -32, 26), (-0.068, 0.19, 0.058, -16, 22),
                                               (0.0, 0.25, 0.066, 0, 18), (0.068, 0.19, 0.058, 16, 22),
                                               (0.13, 0.15, 0.050, 32, 26))):
        bone = "Crown_%d" % (i + 1)
        base = cb + Vector((x, 0.02 + abs(x) * 0.25, -abs(x) * 0.35))
        up_d = Euler((math.radians(-back), math.radians(fan), 0), "XYZ").to_matrix() @ Vector((0, 0, 1))
        back_d = Vector((0, 1, 0))
        tips[bone] = plate_crown(B, base, up_d, back_d, h, w, bone, gem=(i == 2))
        B.add(base + Vector((0, 0.0, 0.0)), (w * 0.95, 0.04, 0.035), OBS_D, bone, rnd=0.35)       # plate socket
        ANCH[bone] = (tuple(base), tuple(tips[bone]))
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
    k.joint("Spine", tuple(CP[0]), "Root", tail=tuple(CP[1] - CP[0]))
    for i in range(1, len(CHAIN)):
        k.joint(CHAIN[i], tuple(CP[i]), CHAIN[i - 1], tail=tuple(CP[i + 1] - CP[i]))
    k.joint("Tail_Tip", ANCH.get("Tail_Tip", tuple(CP[9])), "Tail4", tail=(0, 0.05, 0.1))
    k.joint("Neck1", tuple(FRONT[2]), "Spine", tail=tuple(FRONT[3] - FRONT[2]))
    k.joint("Neck2", tuple(FRONT[3]), "Neck1", tail=tuple(FRONT[4] - FRONT[3]))
    k.joint("Neck3", tuple(FRONT[4]), "Neck2", tail=tuple(FRONT[5] - FRONT[4]))
    k.joint("Head", tuple(THROAT), "Neck3", tail=(0, -0.4, 0.15))                     # throat pivot
    k.joint("Jaw", (0, -0.56, 1.67), "Head", tail=(0, -0.35, -0.03))
    k.joint("Mouth", ANCH.get("Mouth", (0, -0.95, 1.66)), "Jaw", tail=(0, -0.1, 0))
    for i in range(1, 6):
        b, t = ANCH.get("Crown_%d" % i, ((0, -0.66, 1.9), (0, -0.66, 2.1)))
        k.joint("Crown_%d" % i, b, "Head", tail=tuple(Vector(t) - Vector(b)))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Arm_" + side, (s * 0.16, -0.60, 0.50), "Spine")
        h, e = ANCH.get("Claw_" + side, ((s * 0.22, -0.80, 0.32), (s * 0.24, -0.70, 0.40)))
        k.joint("Claw_" + side, e, "Arm_" + side, tail=tuple(Vector(h) - Vector(e)))
    for i in range(1, 7):
        p, bone = ANCH.get("Vent_%d" % i, ((0.2, 0.0, 0.2), "Spine"))
        k.joint("Vent_%d" % i, p, bone, tail=(0.1, 0, 0.05))


def check_pairs():
    P = []
    for a in ("Head", "Jaw", "Neck3", "Neck2"):
        for b in ("Spine", "Body1", "Body2", "Arm_L", "Arm_R", "Claw_L", "Claw_R"):
            P.append((a, b))
    for i in range(1, 6):
        P += [("Crown_%d" % i, "Neck3"), ("Crown_%d" % i, "Neck2")]
        if i < 5:
            P.append(("Crown_%d" % i, "Crown_%d" % (i + 1)))
    for a in ("Tail2", "Tail3", "Tail4", "Body4"):
        for b in ("Spine", "Body1", "Body2"):
            P.append((a, b))
    P += [("Body3", "Spine"), ("Tail1", "Body2"), ("Tail2", "Body3"), ("Tail3", "Body4"), ("Tail4", "Tail1"),
          ("Claw_L", "Claw_R"), ("Arm_L", "Neck1"), ("Arm_R", "Neck1"), ("Claw_L", "Neck1"), ("Claw_R", "Neck1")]
    return P


def joints():
    out = []
    for i in range(1, len(CHAIN)):
        out.append((tuple(CP[i]), tuple(CP[i]), RAD[i - 1] * 1.25, CHAIN[i]))
    for i, nb in enumerate(NECKS):
        out.append((tuple(FRONT[i + 2]), tuple(FRONT[i + 2]), FRAD[i + 1] * 1.25, nb))
    out.append((tuple(THROAT), tuple(THROAT + Vector((0, -0.06, 0.10))), 0.20, "Head"))
    out.append(((0, -0.56, 1.67), (0, -0.62, 1.67), 0.10, "Jaw"))
    for i in range(1, 6):
        b, t = ANCH.get("Crown_%d" % i, ((0, -0.66, 1.9), (0, -0.66, 2.1)))
        out.append((b, b, 0.07, "Crown_%d" % i))
    for s, side in ((1, "L"), (-1, "R")):
        out.append(((s * 0.16, -0.60, 0.50), (s * 0.16, -0.60, 0.50), 0.09, "Arm_" + side))
        out.append(((s * 0.24, -0.70, 0.40), (s * 0.24, -0.70, 0.40), 0.07, "Claw_" + side))
    return out


HEAD_XF = []
