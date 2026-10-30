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
PLUM_OBS = (160, 90, 136)   # body scales (studded); plan (182,132,172) deepened (H 319, away from the
                             # Cosmic Leviathan's H 300 magenta hide)
OBS_D = (62, 50, 64)         # obsidian: crown plates, brow ridges, dorsal spikes, scale bands (plan 96,84,96)
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
FRONT = [Vector(p) for p in ((0, -0.24, 0.221), (0, -0.48, 0.34), (0, -0.58, 0.60), (0, -0.57, 0.89),
                             (0, -0.50, 1.16), (0, -0.50, 1.42))]
FRAD = [0.235, 0.232, 0.218, 0.198, 0.180, 0.166]
NECKS = ["Neck1", "Neck2", "Neck3"]
THROAT = Vector((0, -0.50, 1.50))


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


def oval(c, side, upv, rw, rh, a0=0.0, a1=2 * math.pi, seg=16, n=2.2, off=0.0):
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


def band(B, a, b, r0, r1, bone, color, a0, a1, off=0.012, thick=0.02, up=(0, 0, 1), seg=8, flat=0.92, nr=2,
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
    B.bar(p0, p1, n, w, 0.012, ROSE, bone, studs=[], nostud=True, role="detail", bevel=0.004, top=(1, 0.55))
    B.bar(p0 + ax * L * 0.16 + n * 0.007, p1 - ax * L * 0.22 + n * 0.007, n, w * 0.38, 0.008, ROSE_H, bone,
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
        B.seg(p - dv * 0.010, q + dv * 0.010, 0.016, t * 0.5 + 0.009, GOLD, bone, side=nrm.cross(dv),
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

    def scutes(a, b, r0, r1, bone, a0, a1, up=(0, 0, 1), ts=((0.04, 0.30), (0.36, 0.62), (0.68, 0.94))):
        for t0, t1 in ts:                                    # transverse ventral scute plates (gaps between)
            band(B, a.lerp(b, t0), a.lerp(b, t1), r0 + (r1 - r0) * t0, r0 + (r1 - r0) * t1, bone, PALE_S,
                 math.radians(a0), math.radians(a1), off=0.009, thick=0.022, up=up)

    def ring_band(a, b, r0, r1, bone, t0, t1, up=(0, 0, 1)):
        """obsidian scale band wrapping the back and the flanks (banded-krait rings)"""
        band(B, a.lerp(b, t0), a.lerp(b, t1), r0 + (r1 - r0) * t0, r0 + (r1 - r0) * t1, bone, OBS_D,
             math.radians(8), math.radians(172), off=0.011, thick=0.026, up=up, seg=12, nostud=False)

    # ================= rear body on the ground (lateral S): lofted segments, obsidian rings, pale ventral scutes
    for i in range(9):
        a, b = CP[i], CP[i + 1]
        bone = CHAIN[i]
        body_seg(B, a, b, RAD[i], RAD[i + 1], bone, ext0=0.0 if i == 0 else RAD[i] * 0.55, ext1=RAD[i + 1] * 0.45)
        ring_band(a, b, RAD[i], RAD[i + 1], bone, 0.52, 0.86)
        scutes(a, b, RAD[i], RAD[i + 1], bone, 212, 328, ts=((0.04, 0.44), (0.52, 0.94)))
    # tail ember spike
    d = (CP[9] - CP[8]).normalized()
    tip0 = CP[9] - d * 0.03
    de = (d + Vector((0, 0.3, 0.6))).normalized()
    B.spike(tip0, de, 0.17, 0.048, ROSE, "Tail4", nostud=True)
    B.spike(tip0 + de * 0.10, de, 0.11, 0.028, ROSE_H, "Tail4", nostud=True)
    ANCH["Tail_Tip"] = tuple(tip0 + de * 0.19)
    # ================= front rise (Spine chest curve + Neck1..3): cobra S, stacked throat scutes facing forward
    fb = ["Spine", "Spine", "Neck1", "Neck2", "Neck3"]
    for i in range(5):
        a, b = FRONT[i], FRONT[i + 1]
        body_seg(B, a, b, FRAD[i], FRAD[i + 1], fb[i], ext0=FRAD[i] * 0.5 if i else 0.0, ext1=FRAD[i + 1] * 0.5,
                 up=(0, 1, 0))
        scutes(a, b, FRAD[i], FRAD[i + 1], fb[i], 232, 308, up=(0, 1, 0))
        if i >= 1:
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.50, 0.84, up=(0, 1, 0))
    # ================= dorsal spikes: small obsidian spikes on the rings, shrinking to the tail
    for bone, t, L in (("Spine", 0.69, 0.14), ("Body1", 0.69, 0.13), ("Body2", 0.69, 0.12), ("Body3", 0.69, 0.10),
                       ("Body4", 0.69, 0.085), ("Tail1", 0.69, 0.07)):
        j = CHAIN.index(bone)
        p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t, math.pi / 2, off=0.02)
        B.spike(p - n * 0.03, n + dv * 0.55, L + 0.03, 0.045 * (L / 0.13) + 0.012, OBS_D, bone, top=(0.12, 0.35))
    for i, (t, L) in ((2, (0.67, 0.11)), (3, (0.67, 0.10)), (4, (0.67, 0.09))):
        p, n, dv = surf_pt(FRONT[i], FRONT[i + 1], FRAD[i], FRAD[i + 1], t, math.pi / 2, off=0.02, up=(0, 1, 0))
        B.spike(p - n * 0.03, n + Vector((0, 0, -0.45)), L + 0.03, 0.045 * (L / 0.13) + 0.012, OBS_D, fb[i],
                top=(0.12, 0.35))
    # ================= rose lava vents: 6 pairs along the flanks, double slits in the plum gap before each ring
    for vi, (bone, t) in enumerate((("Spine", 0.27), ("Body1", 0.27), ("Body2", 0.27), ("Body3", 0.27),
                                    ("Body4", 0.27), ("Tail1", 0.27))):
        j = CHAIN.index(bone)
        sc = RAD[j] / 0.23
        for s in (1, -1):
            ang = math.radians(16 if s > 0 else 164)
            for dt in (-0.06, 0.06):
                p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t + dt, ang, off=0.004)
                vent(B, p, n, dv, bone, L=0.18 * sc + 0.035, w=0.042 * sc + 0.010)
            if s > 0:
                p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t, ang, off=0.004)
                ANCH["Vent_%d" % (vi + 1)] = (tuple(p + n * 0.03), bone)
    # ================= forearms: two small clawed arms held at the chest (Neck1)
    for s, side in ((1, "L"), (-1, "R")):
        sh = Vector((s * 0.15, -0.68, 0.76))
        el = Vector((s * 0.25, -0.78, 0.64))
        ha = Vector((s * 0.21, -0.88, 0.58))
        B.add(sh, (0.072, 0.072, 0.072), PLUM_OBS, "Arm_" + side, rnd=0.45)
        B.seg(sh, el, 0.054, 0.060, PLUM_OBS, "Arm_" + side, ext=0.03, ext1=0.02, top=(0.9, 0.9), rnd=0.4)
        B.seg(el, ha, 0.048, 0.052, OBS_D, "Claw_" + side, ext=0.02, ext1=0.02, top=(0.9, 0.9), rnd=0.4)
        B.add(ha, (0.052, 0.046, 0.042), OBS_D, "Claw_" + side, rnd=0.4)
        for gx in (-0.03, 0.0, 0.03):
            B.spike(ha + Vector((gx, -0.03, -0.01)), (gx * 2.5, -0.7, -0.9), 0.075, 0.015, BLACK, "Claw_" + side)
        ANCH["Claw_" + side] = (tuple(ha), tuple(el), tuple(sh))
    # ================= head (throat pivot): big wedge skull, heavy jaw, obsidian brows, rose slit eyes, fangs
    skull = B.seg((0, -0.50, 1.69), (0, -1.04, 1.625), 0.195, 0.150, PLUM_OBS, "Head", top=(0.56, 0.56),
                  ext=0.05, rnd=0.36)
    B.seg((0, -0.56, 1.83), (0, -0.99, 1.70), 0.07, 0.024, OBS_D, "Head", top=(0.50, 1.0), rnd=0.3)  # nasal ridge
    B.seg((0, -0.54, 1.565), (0, -0.98, 1.555), 0.15, 0.03, PALE_S, "Head", top=(0.60, 1.0), rnd=0.3, nostud=True)
    for s in (1, -1):                                                                   # jaw muscles / cheek plates
        B.add((s * 0.17, -0.60, 1.64), (0.065, 0.12, 0.095), PLUM_OBS, "Head", rot=(0, 0, s * 10), rnd=0.42)
        B.add((s * 0.205, -0.56, 1.66), (0.03, 0.09, 0.07), OBS_D, "Head", rot=(0, 0, s * 12), rnd=0.4)
        B.add((s * 0.040, -0.995, 1.712), (0.014, 0.020, 0.008), BLACK, "Head", rot=(-28, 0, s * 18),
              studs=[], role="detail", bevel=0.003)                                     # nostril pits (on top)
        for z, dz, L, w in ((1.60, -0.35, 0.15, 0.040), (1.67, -0.05, 0.18, 0.044), (1.74, 0.25, 0.13, 0.036)):
            B.spike((s * 0.20, -0.53, z), (s * 0.55, 0.85, dz), L, w, OBS_D, "Head", top=(0.12, 0.35))  # cheek spikes
    JR = Euler((math.radians(6), 0, 0), "XYZ").to_matrix()
    JP = Vector((0, -0.55, 1.555))

    def jp(p):
        return JP + JR @ Vector(p)
    B.seg(jp((0, 0.0, -0.01)), jp((0, -0.45, -0.03)), 0.150, 0.052, PLUM_OBS, "Jaw", top=(0.58, 0.8), ext=0.04,
          rnd=0.34)
    B.seg(jp((0, -0.02, -0.055)), jp((0, -0.42, -0.068)), 0.12, 0.016, PALE_S, "Jaw", top=(0.6, 1.0), rnd=0.3,
          nostud=True)
    B.seg(jp((0, -0.04, 0.030)), jp((0, -0.42, 0.012)), 0.11, 0.010, MOUTH, "Jaw", studs=[], role="detail",
          bevel=0.003, top=(0.6, 1))
    for s in (1, -1):
        B.spike(jp((s * 0.075, -0.37, 0.012)), JR @ Vector((0, -0.12, 1)), 0.12, 0.025, IVORY, "Jaw", nostud=True)
        B.spike(Vector((s * 0.092, -0.93, 1.585)), (0, -0.15, -1), 0.17, 0.031, IVORY, "Head", nostud=True)  # upper
    ANCH["Mouth"] = tuple(jp((0, -0.44, 0.02)))
    for s in (1, -1):                                                # eyes on the skull sides-front, heavy brows
        ep, en = surf_hit(B, [skull], (s * 0.6, -0.80, 1.722), (-s, 0, 0))
        en = (en + Vector((0, -1.1, 0.15))).normalized()
        R = face_R(en) @ Euler((0, math.radians(-s * 20), 0), "XYZ").to_matrix()
        kw = dict(R=R, studs=[], role="detail")
        B.add(ep, (0.088, 0.010, 0.032), BLACK, "Head", bevel=0.005, top=(0.78, 1.0), **kw)       # socket
        B.add(ep + en * 0.008 + R @ Vector((0, 0, -0.004)), (0.074, 0.007, 0.0165), ROSE, "Head", bevel=0.004,
              top=(0.55, 1.0), **kw)                                                            # rose slit (wedge)
        B.add(ep + en * 0.013 + R @ Vector((-s * 0.006, 0, -0.004)), (0.0055, 0.005, 0.0165), BLACK, "Head",
              bevel=0.002, **kw)                                                                # reptile pupil
        Rb = face_R(en) @ Euler((0, math.radians(-s * 22), 0), "XYZ").to_matrix()
        B.add(ep + en * 0.020 + Vector((0, 0, 0.056)), (0.108, 0.036, 0.030), OBS_D, "Head", R=Rb, role="limb",
              rnd=0.2, studs=[], nostud=True)                                                   # heavy brow
    # ================= THE HERO: crown of five obsidian blades framed in gold on an obsidian crown mount. The blades
    # stand side by side (no x overlap, tops fanned outward) so each can lift on its own hinge (act_molt) untouched.
    B.add((0, -0.585, 1.835), (0.30, 0.050, 0.034), OBS_D, "Head", top=(0.92, 0.80), rnd=0.40)       # crown mount
    for s in (1, -1):
        B.add((s * 0.27, -0.565, 1.825), (0.06, 0.055, 0.040), OBS_D, "Head", rot=(0, s * 14, 0), rnd=0.40)
    for i, (x, h, w, roll, back) in enumerate(((-0.300, 0.15, 0.040, -24, 24), (-0.150, 0.19, 0.048, -12, 24),
                                               (0.0, 0.25, 0.060, 0, 24), (0.150, 0.19, 0.048, 12, 24),
                                               (0.300, 0.15, 0.040, 24, 24))):
        bone = "Crown_%d" % (i + 1)
        base = Vector((x, -0.585 + abs(x) * 0.08, 1.858 - abs(x) * 0.05))
        up_d = Euler((math.radians(-back), math.radians(roll), 0), "XYZ").to_matrix() @ Vector((0, 0, 1))
        back_d = Vector((0, 1, 0))
        tip = plate_crown(B, base, up_d, back_d, h, w, bone, gem=(i == 2))
        B.add(base + Vector((0, 0.0, -0.012)), (w * 0.95, 0.042, 0.030), OBS_D, bone,
              R=Euler((0, math.radians(roll), 0), "XYZ").to_matrix(), rnd=0.35)                 # plate socket
        ANCH[bone] = (tuple(base), tuple(tip))
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
    k.joint("Jaw", (0, -0.55, 1.555), "Head", tail=(0, -0.35, -0.03))
    k.joint("Mouth", ANCH.get("Mouth", (0, -0.95, 1.66)), "Jaw", tail=(0, -0.1, 0))
    for i in range(1, 6):
        b, t = ANCH.get("Crown_%d" % i, ((0, -0.66, 1.9), (0, -0.66, 2.1)))
        k.joint("Crown_%d" % i, b, "Head", tail=tuple(Vector(t) - Vector(b)))
    for s, side in ((1, "L"), (-1, "R")):
        h, e, sh = ANCH.get("Claw_" + side, ((s * 0.21, -0.88, 0.58), (s * 0.25, -0.78, 0.64),
                                             (s * 0.15, -0.68, 0.76)))
        k.joint("Arm_" + side, sh, "Neck1")
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
    out.append(((0, -0.55, 1.555), (0, -0.61, 1.555), 0.10, "Jaw"))
    for i in range(1, 6):
        b, t = ANCH.get("Crown_%d" % i, ((0, -0.66, 1.9), (0, -0.66, 2.1)))
        out.append((b, b, 0.07, "Crown_%d" % i))
    for s, side in ((1, "L"), (-1, "R")):
        out.append(((s * 0.15, -0.68, 0.76), (s * 0.15, -0.68, 0.76), 0.09, "Arm_" + side))
        out.append(((s * 0.25, -0.78, 0.64), (s * 0.25, -0.78, 0.64), 0.07, "Claw_" + side))
    return out


HEAD_XF = [((0, -0.50, 1.50), 1.20, ["Head", "Jaw", "Mouth", "Crown_1", "Crown_2", "Crown_3", "Crown_4",
                                      "Crown_5"], (0, 0, -0.08))]     # head group built at 1.0, shown 20 % bigger
