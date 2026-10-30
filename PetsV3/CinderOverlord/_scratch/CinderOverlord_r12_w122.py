# Cinder Overlord (Magma / Fire egg ULTRA-RARE 0.5 %, 2026-10-27; model round 2 after review 1) - plan
# _review/CinderOverlord_plan.md v2. A volcanic serpent-dragon in the FIERCE studded style: no legs, no wings. The
# front third rears up in a cobra S (chest on the ground, neck rising, wedge head level at the top); the rear lies on the
# ground in a lateral S down to a thin tail with a rose ember spike (lava tip). Oxblood studded hide under an obsidian
# dorsal saddle with obsidian rings, small dorsal spikes, pale belly scutes wrapping the flanks, six pairs of wide rose
# vent slits with lava hot cores, two small clawed forearms, a lofted wedge skull with a squared muzzle (obsidian cap,
# pointed brows, rose slit eyes, four ivory fangs) and THE HERO: a crown of five obsidian blades on an obsidian mount,
# gold on the upper edges (the centre blade fully framed and tipped lava-hot). No glow (embers / smoke = Studio VFX).
import math
from mathutils import Vector, Matrix, Euler, Quaternion

DISPLAY = "Cinder Overlord"
MOTION = "Walk"
RIG = "serpent"
HEIGHT = 11.72               # studs to the crown tip of the rearing head (H_MODEL). r11: 10.5 x 2.829 / 2.534 (the raised
                             # head) so studs per BU stay as approved: same body size, stud pitch and stride in studs

# Blender colours (Roblox renders ~0.6x darker)
PLUM_OBS = (176, 72, 54)    # f85 r2 (coordinator): +value, same ember hue (was 166,66,50). r4 lead ruling: EMBER body, away from the pink wine (160,87,102)
                             # of review 3 (it read as a pink worm at 64 / 128 px; hue_cmp.png candidate A2). Before:
                             # r4 wine (160, 87, 102), r3 (144, 80, 96). Body scales (studded); review 1 MUST 1 moved it to (150,84,110) H 336; the portrait
                             # still read pink, so per the review's fallback it went deeper + redder: oxblood H 345,
                             # S 0.44, luma 101 (45 deg off the Cosmic Leviathan's H 300 magenta; r1 was 160,90,136)
OBS_D = (62, 50, 64)         # obsidian: crown plates, brow ridges, dorsal spikes, scale bands (plan 96,84,96)
PALE_S = (222, 194, 158)     # r4 lead ruling: warm ash / bone (was 245,236,240). Belly scutes (wrapping the flanks), throat (review 1 MUST 7)
ROSE = (20, 92, 250)         # r6 (lead ruling A): DEEP SULFUR-BLUE accent (H 223, S 0.92, luma 88) - vent slits, eye slits, tail spike;
                             # the ruling's (24,104,255) sat 2 deg / RGB 28 from ThunderRex DEEP (34,110,230), so a touch darker
                             # (r5 40,160,255 was 2.8 deg from Kraken RING)
CROWN_IN = (20, 92, 250)     # r6: the crown's inner edge lines, same deep sulfur blue
LAVA = (226, 240, 255)       # r6 (lead ruling A): WHITE-HOT cores with a faint blue tint (S 0.11) - vent cores, tail tip, crown centre gem
                             # (the crown centre gem since r2 MUST 5)
GOLD = (250, 160, 35)        # THE hero: the gold frames of the crown plates (crown only). r5 MUST 1: was (255,196,50),
                             # whose lit faces clipped to lemon H 60 in the kit render; this base renders H 40-52 (amber gold)
GOLD_D = (214, 150, 30)      # inner faces of the gold frames
BLACK = (14, 14, 22)         # claws, eye sockets, pupils, nostrils
IVORY = (238, 234, 220)      # fangs
MOUTH = (96, 26, 30)         # mouth

H_MODEL = 2.10
ANCH = {}
SEGS = {}                    # r8: rear body segment tubes (vents snap to the real skin)
# f85 (review M4 "dark arms over the brows" = the brows' outer ends seen from the front): shorter, less rolled brows
BROW_ROLL, BROW_HL, BROW_IN = 10, 0.070, 0.030      # f85 r2 R2-M2 (f85: 16 / 0.090 / 0.018; r6: 22 deg, 0.108)
BROW_DZ = 0.040                                     # f85 r2: 0.016 lower (was 0.056)

# ---- the spine curve. Rear (on the ground, lateral S): Spine -> Body1..4 -> Tail1..4 -> tip
CHAIN = ["Spine", "Body1", "Body2", "Body3", "Body4", "Tail1", "Tail2", "Tail3", "Tail4"]
# the r5 ground path (x, y) + radii: the reference for the segment lengths (= the slither stride, closed at 5.0089)
_P0 = ((0.00, -0.24), (0.08, 0.10), (0.24, 0.44), (0.24, 0.80), (0.06, 1.12), (-0.18, 1.38), (-0.32, 1.66), (-0.28, 1.94),
       (-0.12, 2.16), (-0.032, 2.237))                                     # f85 r2 T-b: Tail4 45 % shorter (was 0.04, 2.30)
_R0 = (0.297, 0.308, 0.280, 0.252, 0.200, 0.168, 0.135, 0.103, 0.072, 0.042)
RAD = [0.297, 0.3388, 0.308, 0.2772, 0.220, 0.168, 0.135, 0.103, 0.072, 0.042]   # r6 MUST 1: RAD[1..4] +10 % (thicker from the game camera); f85 M1 body +12 %, T2 tail +25 %
# (r1 MUST 6 +15 %, r2 MUST 4 +10 %; r6 was 0.265, 0.275, 0.250, 0.225, 0.180, 0.134, 0.108, 0.082, 0.060, 0.042)
COIL = 1.5   # r6 MUST 1: the lateral S coils 1.5x (each segment's heading deviation from the mean x1.5) so the body reads
             # as a coiled serpent, not a straight worm, from the game camera; every segment keeps its r5 3D length,
             # so the slither stride stays 5.0089 BU / 48 f


def _cp_path():
    def z(R, i):
        return 0.13 if i == 9 else R[i] * 0.96             # lying on the ground; the tail tip curls up (f85 r2 0.13)
    L3 = [((_P0[i + 1][0] - _P0[i][0]) ** 2 + (_P0[i + 1][1] - _P0[i][1]) ** 2 + (z(_R0, i + 1) - z(_R0, i)) ** 2) ** 0.5
          for i in range(9)]
    th = [math.atan2(_P0[i + 1][0] - _P0[i][0], _P0[i + 1][1] - _P0[i][1]) for i in range(9)]
    tm = sum(th) / 9
    pts = [Vector((_P0[0][0], _P0[0][1], z(RAD, 0)))]
    for i in range(9):
        t = tm + COIL * (th[i] - tm)
        dz = z(RAD, i + 1) - z(RAD, i)
        L = (L3[i] ** 2 - dz * dz) ** 0.5
        pts.append(Vector((pts[-1].x + L * math.sin(t), pts[-1].y + L * math.cos(t), z(RAD, i + 1))))
    return pts


CP = _cp_path()
# front rise (cobra S): chest curve -> Neck1..3 -> throat
HEAD_LIFT = 0.18             # r11 MUST 1 (owner: RAISED COBRA STANCE): the throat / head rise 0.18 BU
FRONT = [Vector(p) for p in ((0, -0.24, 0.285), (0, -0.48, 0.37), (0, -0.60, 0.62), (0, -0.585, 0.90),
                             (0, -0.51, 1.16 + 0.12), (0, -0.50, 1.42 + HEAD_LIFT))]     # r11: FRONT[4] 1.28, FRONT[5] 1.60
FRAD = [0.282, 0.275, 0.257, 0.231, 0.208, 0.189]    # f85 M1 +5 % (r6 0.268, 0.262, 0.245, 0.220, 0.198, 0.180)
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


def loft(B, p0, p1, stations, color, bone, n=2.6, seg=20, up=(0, 0, 1)):
    """closed lofted solid from p0 to p1 through (f, rw, rh, dz) stations; returns (tube, frame(f))"""
    p0, p1 = Vector(p0), Vector(p1)
    d = (p1 - p0).normalized()
    side, upv = frame_of(d, up)
    L = (p1 - p0).length

    def fr(f):
        for (fa, wa, ha, za), (fb, wb, hb, zb) in zip(stations, stations[1:]):
            if fa <= f <= fb:
                u = (f - fa) / max(fb - fa, 1e-6)
                return (p0 + d * L * f + Vector((0, 0, za + (zb - za) * u)), side, upv, wa + (wb - wa) * u,
                        ha + (hb - ha) * u)
        fa, wa, ha, za = stations[-1]
        return p0 + d * L * f + Vector((0, 0, za)), side, upv, wa, ha
    rings = [oval(p0 + d * L * f + Vector((0, 0, dz)), side, upv, rw, rh, seg=seg, n=n) for f, rw, rh, dz in stations]
    return B.tube(rings, color, bone), fr


def ellip(B, c, rx, ry, rz, color, bone):
    """smooth ellipsoid bulge (lofted along y)"""
    c = Vector(c)
    rings = []
    for t in (-0.97, -0.8, -0.45, 0.0, 0.45, 0.8, 0.97):
        k = math.sqrt(max(1 - t * t, 0.05))
        rings.append(oval(c + Vector((0, t * ry, 0)), Vector((1, 0, 0)), Vector((0, 0, 1)), rx * k, rz * k, seg=14))
    return B.tube(rings, color, bone)


PAW_BOX = (0.070, 0.062, 0.056)        # r10 MUST 1a: paw half-size (r9 0.052, 0.046, 0.042)
PAW_CLAW = (0.110, 0.020)              # r10 MUST 1a: claw spike length / half-width (r9 0.075 / 0.015)
PAW_GX = 0.050                         # r11 NICE 1: wider claw fan (r10 0.042, r9 0.03)
SH_Z = 0.77                            # shoulder height (r10 tried 0.74: the root still meets Neck2 inside the neck, so kept)
SH_X, SH_Y = 0.251, -0.765             # r11 MUST 3b: the shoulder ball sits ON the neck side, <= 0.035 deep (r10 0.17, -0.71: 0.10 deep)
EXT_CHEST1, EXT_NECK2_0 = 0.30, 0.30   # r11 MUST 3b: the chest end cap / Neck2 start cap inside Neck1 (were 0.5 x r)
EXT_BODY2_1, EXT_BODY4_0 = 0.30, 0.35  # r11 MUST 3b: the Body2 end / Body4 start caps inside the Body3 bend (0.45 / 0.55)
PAW_ARM = (0.060, 0.066, 0.056, 0.060)  # r10: upper arm / forearm segment widths (r9 0.054, 0.060, 0.048, 0.052)
# r10 MUST 1b: swept-back obsidian skull FRILL, one pair per side on the rear skull above the cheek spikes:
# (base x, y, z), (dir x, y, z), length, half-width - built at head scale 1.0 (then x1.15 wide, x1.45 HEAD_XF)
FRILL = (((0.150, -0.470, 1.790), (0.80, 0.56, 0.28), 0.26, 0.050),       # r11 NICE 2: 0.22 / 0.17 -> 0.26 / 0.21
         ((0.165, -0.465, 1.715), (0.86, 0.50, 0.04), 0.21, 0.045))
CR_X1, CR_X2 = 0.310, 0.168   # r11 MUST 3a: outer / middle crown blade x (r10 0.300 / 0.150) - every neighbour >= 0.02
HEAD_WX = 1.15              # r9 MUST 1b: skull + jaw width (x only); the crown blades keep their socket spacing


def _xscale(B, bones, sx):
    """x-only scale about x = 0 for every part of the given bones (blockkit's HEAD_XF is uniform only). Boxes keep
    their rotation; each local half-size grows by the length of its scaled local axis."""
    import blockkit as bk
    S = Matrix(((sx, 0, 0), (0, 1, 0), (0, 0, 1)))
    for blk in B.items:
        if blk.bone not in bones:
            continue
        if isinstance(blk, bk.Tube):
            blk.map(lambda q: Vector((q.x * sx, q.y, q.z)))          # (map updates the rings, pts and c)
        elif isinstance(blk, bk.Poly):
            blk.pts = [Vector((q.x * sx, q.y, q.z)) for q in blk.pts]
            blk.c = sum(blk.pts, Vector()) / len(blk.pts)
        else:
            blk.c = Vector((blk.c.x * sx, blk.c.y, blk.c.z))
            blk.h = Vector([blk.h[i] * (S @ blk.R.col[i]).length for i in range(3)])


def vent_flush(B, j, t, ang, L, w, bone, side, seg_blk=None):
    """r8: a deep-blue slit that FOLLOWS the curved flank (4 short bars between 5 surface points) and sits flush
    (top 0.001 proud). Slanted: the upper end sweeps toward the tail (as the r4 straight slit did)."""
    r = (RAD[j] + RAD[j + 1]) / 2
    seglen = (CP[j + 1] - CP[j]).length
    pts = []
    for u in (-0.5, -0.3, -0.1, 0.1, 0.3, 0.5):
        tt = t + u * L * 0.5 / seglen
        aa = ang + side * u * L * 0.85 / r
        q, nq, _dq = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], tt, aa, off=0.0)
        if seg_blk is not None:                    # the loft is a superellipse: snap to the REAL skin (ray cast)
            hq, hn = surf_hit(B, [seg_blk], q + nq * 0.2, -nq)
            if hq is not None:
                q, nq = hq, hn
        pts.append((q, nq))
    w = w * 0.65                                   # a crack, not a plate
    for k_, ((p0, n0), (p1, n1)) in enumerate(zip(pts, pts[1:])):
        nn = (n0 + n1).normalized()
        dd = (p1 - p0).normalized()
        e = 0.012 if 0 < k_ < len(pts) - 2 else 0.006      # overlap the neighbours (no gaps at the bends)
        B.bar(p0 - dd * e - nn * 0.005, p1 + dd * e - nn * 0.005, nn, w, 0.006, ROSE, bone, studs=[], nostud=True,
              role="detail", bevel=0.002)                                  # slit: top at +0.001
        if k_ in (1, 2, 3):
            B.bar(p0 - dd * e - nn * 0.002, p1 + dd * e - nn * 0.002, nn, w * 0.45, 0.004, ROSE, bone, studs=[],
                  nostud=True, role="detail", bevel=0.002)                 # core line: top at +0.002
    return pts[2]


def vent(B, p, n, d, bone, L=0.095, w=0.026):
    """deep-blue vent slit (flush), a raised blue core ridge (r4: the white-hot core read as ladder rungs); slanted"""
    n = Vector(n).normalized()
    dd = (Vector(d) - n * Vector(d).dot(n)).normalized()
    up = n.cross(dd).normalized()
    ax = (up * 0.85 + dd * 0.5).normalized()                 # slanted slit
    p0, p1 = p - ax * L / 2, p + ax * L / 2
    B.bar(p0, p1, n, w, 0.006, ROSE, bone, studs=[], nostud=True, role="detail", bevel=0.002, top=(1, 0.55))  # r3 T1: flush
    B.bar(p0 + ax * L * 0.16 + n * 0.004, p1 - ax * L * 0.22 + n * 0.004, n, w * 0.50, 0.004, ROSE, bone,   # r4: was LAVA
          studs=[], nostud=True, role="detail", bevel=0.002)


def plate_crown(B, base, up_d, back_d, h, w, bone, gem=False, gw=0.025, nib=0.0, fd=0.009, gin=0.0):
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
    # gold frame along the two upper edges (all blades) + the two sides (centre blade only) - review 1 MUST 2: no
    # four-edge tiara frames
    nrm = up_d.cross(side).normalized()
    edges = [(pts[1], pts[2]), (pts[2], pts[3])]
    if gem:
        # r10 MUST 3: the side frames start 0.033 ABOVE the blade foot (was 0.012 below it): their lower ends sat in the
        # crown mount and grazed the neighbour blades' sockets (proxy-free check); the visible frame is unchanged
        edges += [(pts[0] + up_d * 0.045, pts[1]), (pts[3], pts[4] + up_d * 0.045)]
    for (p, q) in edges:
        dv = (q - p).normalized()
        sd = nrm.cross(dv)                                # in the blade plane, across the edge
        if sd.dot(base + up_d * h * 0.45 - (p + q) / 2) < 0:
            sd = -sd                                      # -> toward the blade centre
        # r6 MUST 2: gin widens the frame INWARD only (the centre moves in by gin, the half-width grows by gin), so the
        # outer edge - and the blade-to-blade clearance in the molt / roar - stays where it was
        B.seg(p - dv * 0.012 + sd * gin, q + dv * 0.012 + sd * gin, gw + gin, t * 0.5 + fd, GOLD, bone, side=nrm.cross(dv),
              studs=[], nostud=True, role="limb", rnd=0.25)
    # rose inner edge lines (inside the gold frame, on the front face)
    inner = [base.lerp(pp, 0.66) + up_d * h * 0.05 for pp in pts]
    for (p, q) in ((inner[1], inner[2]), (inner[2], inner[3])):
        B.bar(p + nrm * (t * 0.5 + 0.003), q + nrm * (t * 0.5 + 0.003), nrm, 0.016, 0.006, CROWN_IN, bone, studs=[],
              nostud=True, role="detail", bevel=0.002)
    if gem:
        B.spike(pts[2] - up_d * 0.03, up_d + nrm * 0.1, 0.075, 0.026, LAVA, bone, nostud=True)    # r2 MUST 5
    if nib > 0:
        # f85 M5: a rounded gold tip nib over the top of the blade (above the blue V apex; its shading stays gold in
        # the kit portrait where flat gold faces clip to lemon)
        B.add(base + up_d * h * (1.0 - nib), (w * 0.52, t * 0.5 + 0.013, h * nib), GOLD, bone,
              R=Matrix((side, nrm, up_d)).transposed(), top=(0.22, 0.75), rnd=0.45, studs=[], nostud=True,
              role="limb")
    return pts[2]


# ---- r12 MUST 1 (owner: COBRA HOOD): two flat, studded hood panels per side on Neck2 (lower) and Neck3 (upper) - thin
# lofted shells (NOT a neck-radius scale): ember front face, an obsidian studded back plate, an obsidian rim, ember
# ribs and a sulfur-blue eye spot (white-hot centre) per side on the back. The panels sit just behind the neck axis and
# cup forward at the rim (a fan from behind); they reach |x| 0.55 (neck side 0.21, skull side 0.37), widest just
# below the head.
HOOD_BACK, HOOD_CUP, HOOD_STACK, HOOD_T = 0.07, 0.10, 0.028, 0.026   # behind the axis, rim forward, upper behind, thick
HOOD_ROOT = 0.10                                                     # inner edge (buried in the neck)
HOOD_W = 1.22          # outline width factor about the root: widest |x| 0.10 + 0.37 x 1.22 = 0.55 (skull side 0.37)
HOOD_DARK = 0.010      # obsidian studded back plate on each panel (the hood reads dark against the ember neck)
HOOD_PANELS = (                       # bone, (z, outer |x|) outline from bottom to top; widest just under the head
    ("Neck2", ((1.08, 0.18), (1.13, 0.24), (1.19, 0.31), (1.25, 0.37), (1.30, 0.41))),
    ("Neck3", ((1.26, 0.40), (1.32, 0.44), (1.38, 0.465), (1.44, 0.47), (1.50, 0.455), (1.55, 0.43), (1.60, 0.38),
               (1.635, 0.32), (1.67, 0.18))))
HOOD_RIBS = (("Neck2", 0.17, 1.20, 0.36, 1.27), ("Neck3", 0.18, 1.39, 0.44, 1.43), ("Neck3", 0.18, 1.53, 0.40, 1.58))
HOOD_SPOT = ("Neck3", 0.30, 1.475, 0.052, 0.036)                     # bone, |x|, z, half width, half height


def hood_axis_y(z):
    """y of the neck axis at height z (FRONT[3] -> FRONT[4] -> FRONT[5])"""
    for a, b in ((FRONT[3], FRONT[4]), (FRONT[4], FRONT[5])):
        if z <= b.z:
            u = (z - a.z) / (b.z - a.z)
            return a.y + (b.y - a.y) * u
    return FRONT[5].y


def hood_x(x):
    return HOOD_ROOT + (x - HOOD_ROOT) * HOOD_W


def hood_pt(sx, x, z, stack):
    """x = the outline |x| BEFORE the HOOD_W widening"""
    return Vector((sx * hood_x(x), hood_axis_y(z) + HOOD_BACK + stack - HOOD_CUP * (x - HOOD_ROOT) / 0.37, z))


def hood_n(sx, z, stack):
    """outward (back-facing, +y) normal of a panel"""
    dx = hood_pt(sx, 0.40, z, stack) - hood_pt(sx, 0.20, z, stack)
    dz = hood_pt(sx, 0.30, z + 0.05, stack) - hood_pt(sx, 0.30, z - 0.05, stack)
    n = dx.cross(dz).normalized()
    return n if n.y > 0 else -n


def cobra_hood(B):
    for sx in (1, -1):
        for pi, (bone, outline) in enumerate(HOOD_PANELS):
            stack = HOOD_STACK if pi == 1 else 0.0
            rings = []
            for z, xo in outline:
                n = hood_n(sx, z, stack)
                xs = [HOOD_ROOT + (xo - HOOD_ROOT) * i / 5.0 for i in range(6)]
                pts = [hood_pt(sx, x, z, stack) for x in xs]
                rings.append(([q + n * HOOD_T / 2 for q in pts], [q - n * HOOD_T / 2 for q in pts]))
            B.tube(rings, PLUM_OBS, bone, closed=False, nostud=True)           # ember panel (front face)
            dark = []                                                          # obsidian studded back plate
            for z, xo in outline[1:-1]:
                n = hood_n(sx, z, stack)
                xs = [HOOD_ROOT + 0.04 + (xo - 0.025 - HOOD_ROOT - 0.04) * i / 5.0 for i in range(6)]
                pts = [hood_pt(sx, x, z, stack) for x in xs]
                dark.append(([q + n * (HOOD_T / 2 + HOOD_DARK) for q in pts], [q + n * (HOOD_T / 2 - 0.002) for q in pts]))
            B.tube(dark, OBS_D, bone, closed=False, nostud=False)
            rim = [hood_pt(sx, xo, z, stack) for z, xo in outline if xo >= 0.20]
            for a, b in zip(rim, rim[1:]):                                     # obsidian rim
                n = hood_n(sx, (a.z + b.z) / 2, stack)
                dv = (b - a).normalized()
                B.seg(a, b, 0.018, HOOD_T / 2 + 0.008, OBS_D, bone, side=n.cross(dv), ext=0.012, ext1=0.012,
                      studs=[], nostud=True, role="limb", rnd=0.3)
        for bone, x0, z0, x1, z1 in HOOD_RIBS:                                # ember ribs on the dark back
            stack = HOOD_STACK if bone == "Neck3" else 0.0
            n = hood_n(sx, (z0 + z1) / 2, stack)
            a = hood_pt(sx, x0, z0, stack) + n * (HOOD_T / 2 + HOOD_DARK + 0.004)
            b = hood_pt(sx, x1, z1, stack) + n * (HOOD_T / 2 + HOOD_DARK + 0.004)
            B.bar(a, b, n, 0.026, 0.010, PLUM_OBS, bone, studs=[], nostud=True, role="detail", bevel=0.004)
        bone, x, z, hw, hh = HOOD_SPOT                                         # sulfur-blue eye spot (cobra marking)
        n = hood_n(sx, z, HOOD_STACK)
        c = hood_pt(sx, x, z, HOOD_STACK) + n * (HOOD_T / 2 + HOOD_DARK + 0.005)
        B.add(c, (hw, 0.006, hh), ROSE, bone, R=face_R(n), studs=[], role="detail", bevel=0.004, top=(0.8, 0.8))
        B.add(c + n * 0.007, (hw * 0.42, 0.004, hh * 0.42), LAVA, bone, R=face_R(n), studs=[], role="detail",
              bevel=0.003)


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

    def dorsal(a, b, r0, r1, bone, half_deg, up=(0, 0, 1)):
        """obsidian dorsal saddle along the top (r2: obsidian-dominant back; rings drop from it down the flanks)"""
        band(B, a.lerp(b, -0.05), a.lerp(b, 1.05), r0 + (r1 - r0) * -0.05, r0 + (r1 - r0) * 1.05, bone, OBS_D,
             math.radians(90 - half_deg), math.radians(90 + half_deg), off=0.0095, thick=0.024, up=up, seg=8,
             nostud=False)

    # ================= rear body on the ground (lateral S): lofted segments, obsidian rings + dorsal saddle, pale
    # ventral scutes
    for i in range(9):
        a, b = CP[i], CP[i + 1]
        bone = CHAIN[i]
        SEGS[i] = body_seg(B, a, b, RAD[i], RAD[i + 1], bone,
                           ext0=0.0 if i == 0 else RAD[i] * (EXT_BODY4_0 if i == 4 else 0.55),
                           ext1=RAD[i + 1] * (EXT_BODY2_1 if i == 2 else 0.45))         # r11 MUST 3b (Body2 / Body4 caps)
        # rings: full band on the body, thinner on the tail (review 1 NICE 1: no caterpillar read)
        if i not in (2, 3, 4, 5, 6, 7, 8):  # r9: rings only on Spine / Body1 (r8 + Tail4; r6 skip 2, 3, 5, 6, 7)
            ring_band(a, b, RAD[i], RAD[i + 1], bone, *((0.62, 0.80) if i < 5 else (0.66, 0.76)))   # f85: narrowed
        # pale scutes wrap the flanks on the body so the pale band shows from the game camera (review 1 MUST 7)
        a0, a1 = (180, 360) if 1 <= i < 5 else (188, 352) if i == 0 else ((200, 340) if i == 5 else (212, 328))  # f85 T1
        if i < 8:
            dorsal(a, b, RAD[i], RAD[i + 1], bone, 9 if i < 5 else 8)                   # r2 MUST 3 (was 32 / 26)
        scutes(a, b, RAD[i], RAD[i + 1], bone, a0, a1, ts=((0.04, 0.44), (0.52, 0.94)))
    # tail ember spike (rose, LAVA hot tip - review 1 MUST 3)
    d = (CP[9] - CP[8]).normalized()
    tip0 = CP[9] - d * 0.03
    de = (d + Vector((0, 0.3, 0.6))).normalized()
    B.spike(tip0, de, 0.17, 0.048, ROSE, "Tail4", nostud=True)
    B.spike(tip0 + de * 0.10, de, 0.11, 0.028, LAVA, "Tail4", nostud=True)
    ANCH["Tail_Tip"] = tuple(tip0 + de * 0.19)
    # ================= front rise (Spine chest curve + Neck1..3): cobra S, stacked throat scutes facing forward
    fb = ["Spine", "Spine", "Neck1", "Neck2", "Neck3"]
    for i in range(5):
        a, b = FRONT[i], FRONT[i + 1]
        body_seg(B, a, b, FRAD[i], FRAD[i + 1], fb[i], ext0=FRAD[i] * (EXT_NECK2_0 if i == 3 else 0.5) if i else 0.0,
                 ext1=FRAD[i + 1] * (EXT_CHEST1 if i == 1 else 0.5),
                 up=(0, 1, 0))
        scutes(a, b, FRAD[i], FRAD[i + 1], fb[i], 238, 302, up=(0, 1, 0), ts=((0.04, 0.46), (0.52, 0.94)))
        if i == 2:                                        # r3 MUST 2: a full ring on Neck1 only
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.50, 0.84, up=(0, 1, 0))
        elif i == 3:                                      # r4: Neck2 a thin band (0.70-0.80); Neck3 has none
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.70, 0.80, up=(0, 1, 0))
            # (r2 MUST 3: the neck saddle is dropped - the rings carry the obsidian on the neck)
    # ================= dorsal spikes: small obsidian spikes on the rings, shrinking to the tail
    for bone, t, L in (("Spine", 0.69, 0.14), ("Body1", 0.69, 0.13), ("Body2", 0.69, 0.12), ("Body3", 0.69, 0.10),
                       ("Body4", 0.69, 0.085), ("Tail1", 0.69, 0.07)):
        j = CHAIN.index(bone)
        p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t, math.pi / 2, off=0.02)
        B.spike(p - n * 0.03, n + dv * 0.55, (L + 0.03) * 1.25, (0.045 * (L / 0.13) + 0.012) * 1.25, OBS_D, bone,
                top=(0.12, 0.35))                                                       # r8: +25 % (spined read from behind)
    for i, (t, L) in ((2, (0.67, 0.11)), (3, (0.67, 0.10)), (4, (0.67, 0.09))):
        p, n, dv = surf_pt(FRONT[i], FRONT[i + 1], FRAD[i], FRAD[i + 1], t, math.pi / 2, off=0.02, up=(0, 1, 0))
        B.spike(p - n * 0.03, n + Vector((0, 0, -0.45)), (L + 0.03) * 1.25, (0.045 * (L / 0.13) + 0.012) * 1.25, OBS_D,
                fb[i], top=(0.12, 0.35))                                                # r8: +25 %
    cobra_hood(B)                                                  # r12 MUST 1: the cobra hood (Neck2 / Neck3)
    # ================= rose lava vents: 6 pairs along the flanks, double slits in the plum gap before each ring
    for vi, (bone, t) in enumerate((("Spine", 0.27), ("Body1", 0.27), ("Body2", 0.27))):   # r7 MUST 1a: Body3-Tail1 dropped
        j = CHAIN.index(bone)
        sc = RAD[j] / 0.23
        vw, vl = 0.060 * sc + 0.014, (0.22 * sc + 0.04) * 1.15   # review 1 MUST 4; f85 r2 R2-M3: +15 % long
        seglen = (CP[j + 1] - CP[j]).length
        dt0 = min(0.17, 0.72 * vw / seglen)                       # keep the two slits of a pair apart (gap ~0.25 w)
        for s in (1, -1):
            ang = math.radians(32 if s > 0 else 148)                       # f85 r2 (f85 28 / 152, r6 24 / 156): clear of the scutes
            vent_flush(B, j, t, ang, vl * 0.70, vw, bone, 1 if s > 0 else -1, SEGS.get(j))   # r8: 30 % shorter, flush, curved
            if s > 0:
                p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t, ang, off=0.000)
                ANCH["Vent_%d" % (vi + 1)] = (tuple(p + n * 0.03), bone)
    # ================= forearms: two small clawed arms held at the chest (Neck1)
    for s, side in ((1, "L"), (-1, "R")):
        sh = Vector((s * SH_X, SH_Y, SH_Z))                   # r11: on the neck side (r2 0.17, -0.71); r10 z SH_Z
        el = Vector((s * 0.42, -0.82, 0.65))                  # r10 MUST 1a: 0.40 -> 0.42 (r9: out of the neck silhouette, was 0.28)
        ha = Vector((s * 0.39, -0.93, 0.59))                  # r10: 0.36 -> 0.39 (far paw >= 0.10 BU past the neck on the game camera)
        B.add(sh, (0.072, 0.072, 0.072), PLUM_OBS, "Arm_" + side, rnd=0.45)
        B.seg(sh, el, PAW_ARM[0], PAW_ARM[1], PLUM_OBS, "Arm_" + side, ext=0.03, ext1=0.02, top=(0.9, 0.9), rnd=0.4)
        B.seg(el, ha, PAW_ARM[2], PAW_ARM[3], OBS_D, "Claw_" + side, ext=0.02, ext1=0.02, top=(0.9, 0.9), rnd=0.4)
        B.add(ha, PAW_BOX, OBS_D, "Claw_" + side, rnd=0.4)           # r10 MUST 1a (r9 0.052 x 0.046 x 0.042)
        for gx in (-PAW_GX, 0.0, PAW_GX):                                # r10 MUST 1a: claws 0.075 / 0.015 -> 0.110 / 0.020
            B.spike(ha + Vector((gx, -PAW_BOX[1] + 0.016, -0.014)), (gx * 2.5, -0.7, -0.9), PAW_CLAW[0], PAW_CLAW[1],
                    BLACK, "Claw_" + side)
        ANCH["Claw_" + side] = (tuple(ha), tuple(el), tuple(sh))
    # ================= head (throat pivot): lofted wedge skull with a squared muzzle (review 1 MUST 5: no brick),
    # obsidian skull cap brow-to-crown, lofted jaw, jaw-muscle bulges, brows with forward points, rose slit eyes, fangs
    SK0, SK1 = Vector((0, -0.45, 1.696)), Vector((0, -1.10, 1.618))
    SKS = ((0.0, 0.110, 0.090, 0.0), (0.06, 0.172, 0.138, 0.0), (0.18, 0.200, 0.155, 0.0), (0.40, 0.186, 0.142, -0.004),
           (0.62, 0.150, 0.112, -0.014), (0.82, 0.112, 0.066, -0.026), (0.96, 0.060, 0.028, -0.034),   # r12 MUST 2: 0.082 / 0.040 -> 0.066 / 0.028
           (1.0, 0.044, 0.022, -0.036))     # r11 MUST 2: tip half-height 0.032 -> 0.022 (flat nose, no bulb); r9 MUST 2: the muzzle tapers to a narrower tip (0.070 / 0.055 wide) - no nose pad                                             # r4 T-b: tip 10 % flatter (0.048 / 0.040)                                             # r2 MUST 2: V muzzle tip
    skull, skf = loft(B, SK0, SK1, SKS, PLUM_OBS, "Head", n=2.8)
    snout = B.tube([oval(*skf(f)[:3], skf(f)[3] + 0.004, skf(f)[4] + 0.004, seg=20, n=2.8) for f in (0.74, 0.82, 0.90, 0.96, 1.0)]
                   + [oval(*skf(1.012)[:3], skf(1.0)[3] * 0.80, skf(1.0)[4] * 0.60, seg=20, n=2.8)],   # r11: cap height x0.60 (r9 x0.80)
                   PLUM_OBS, "Head", nostud=True)                                  # f85 r2 T-a: snout tip without stud dots
    # r5 T-b: + a smaller ring 0.012 ahead of the tip = a smooth nose cap over the skull's front-face studs (the
    # 'pig snout' the review saw from the front was those studs on the flat snout front)
    cap = []                                   # obsidian skull cap (r2: darker, fiercer face read; brow to crown)
    for f in (0.03, 0.08, 0.18, 0.30, 0.42, 0.54):                     # r3 MUST 1: cap ends at the eye line (was ... 0.78)
        c, side_v, up_v, rw, rh = skf(f)
        aa, ab = math.radians(65), math.radians(115)                                     # r2 MUST 1 (was 55-125)
        cap.append((oval(c, side_v, up_v, rw, rh, aa, ab, seg=8, n=2.8, off=0.008),
                    oval(c, side_v, up_v, rw, rh, aa, ab, seg=8, n=2.8, off=-0.014)))
    B.tube(cap, OBS_D, "Head", closed=False, nostud=False)
    r0, _ = surf_hit(B, [skull, snout], (0, -0.95, 2.4), (0, 0, -1))
    r1, _ = surf_hit(B, [skull, snout], (0, -1.07, 2.4), (0, 0, -1))
    B.seg(r0, r1, 0.010, 0.020, OBS_D, "Head", top=(0.6, 1.0), rnd=0.3, ext=0.05)    # nasal ridge tip (thin, NICE 2)
    B.seg((0, -0.54, 1.560), (0, -0.98, 1.548), 0.12, 0.03, PALE_S, "Head", top=(0.50, 1.0), rnd=0.3, nostud=True)
    for s in (1, -1):                                                                   # jaw-muscle bulges
        ellip(B, (s * 0.158, -0.62, 1.628), 0.035, 0.069, 0.053, PLUM_OBS, "Head")      # f85 M2: 60 % bulge
        c0, n0 = surf_hit(B, [skull], (s * 0.6, -0.565, 1.628), (-s, 0, 0))
        c1, n1 = surf_hit(B, [skull], (s * 0.6, -0.800, 1.612), (-s, 0, 0))
        B.seg(c0 + n0 * 0.006, c1 + n1 * 0.006, 0.050, 0.011, OBS_D, "Head", side=(0, 0, 1), top=(0.55, 1.0),
              rnd=0.25, studs=[], nostud=True, role="limb")                             # f85 M2: flat cheek plate
        npt, nn = surf_hit(B, [skull, snout], (s * 0.042, -1.07, 2.4), (0, 0, -1))      # r3 MUST 3: at the tip
        B.add(npt, (0.009, 0.005, 0.012), BLACK, "Head", R=face_R(nn, up=(s * 0.4, 1, 0)), studs=[], role="detail",
              bevel=0.003)                                     # nostril pits (on top); r7 9+: >= 0.02 BU shown (x1.38 head)
        for z, dz, L, w in ((1.60, -0.35, 0.15, 0.040), (1.67, -0.05, 0.18, 0.044), (1.74, 0.25, 0.13, 0.036)):
            B.spike((s * 0.20, -0.53, z), (s * 0.55, 0.85, dz), L, w, OBS_D, "Head", top=(0.12, 0.35))  # cheek spikes
        for (bx, by, bz), (dx, dy, dz), L, w in FRILL:                  # r10 MUST 1b: swept-back skull frill
            B.spike((s * bx, by, bz), (s * dx, dy, dz), L, w, OBS_D, "Head", top=(0.12, 0.35))
    JR = Euler((math.radians(6), 0, 0), "XYZ").to_matrix()
    JP = Vector((0, -0.55, 1.555))

    def jp(p):
        return JP + JR @ Vector(p)
    _jaw, jkf = loft(B, jp((0, 0.03, -0.01)), jp((0, -0.46, -0.035)), ((0.0, 0.118, 0.044, 0.0), (0.12, 0.148, 0.054, 0.0),
                                                            (0.55, 0.126, 0.052, 0.0), (0.85, 0.078, 0.032, 0.0),   # r10 MUST 2: rw 0.098 -> 0.078 (r9: rh 0.040 -> 0.032, tip 0.02 back)
                                                            (1.0, 0.034, 0.016, 0.0)), PLUM_OBS, "Jaw", n=2.8)  # r10 MUST 2: tip 0.046 / 0.020 -> 0.034 / 0.016 (< nose 0.044)
    B.tube([oval(*jkf(f)[:3], jkf(f)[3] + 0.004, jkf(f)[4] + 0.004, seg=20, n=2.8) for f in (0.80, 0.88, 0.95, 1.0)]
           + [oval(*jkf(1.006)[:3], jkf(1.0)[3] * 0.80, jkf(1.0)[4] * 0.80, seg=20, n=2.8)],   # r8 / r9: flatter cap
           PLUM_OBS, "Jaw", nostud=True)                                            # r5 T-b: chin front without stud dots
    B.seg(jp((0, -0.02, -0.052)), jp((0, -0.42, -0.062)), 0.11, 0.014, PALE_S, "Jaw", top=(0.6, 1.0), rnd=0.3,
          nostud=True)
    B.seg(jp((0, -0.04, 0.030)), jp((0, -0.42, 0.012)), 0.11, 0.010, MOUTH, "Jaw", studs=[], role="detail",
          bevel=0.003, top=(0.6, 1))
    for s in (1, -1):
        B.spike(jp((s * 0.064, -0.37, 0.012)), JR @ Vector((0, -0.12, 1)), 0.12, 0.025, IVORY, "Jaw", nostud=True)  # r10: on the narrower rim (was 0.075)
        B.spike(Vector((s * 0.092, -0.93, 1.585)), (0, -0.15, -1), 0.17, 0.031, IVORY, "Head", nostud=True)  # upper
    ANCH["Mouth"] = tuple(jp((0, -0.44, 0.02)))
    for s in (1, -1):                                                # eyes on the skull sides-front, heavy brows
        ep, en = surf_hit(B, [skull], (s * 0.6, -0.86, 1.722), (-s, 0, 0))            # r4 T-a: -0.86 (r3 -0.83, r2 -0.80)
        en = (en + Vector((0, -1.1, 0.15))).normalized()
        R = face_R(en) @ Euler((0, math.radians(-s * 20), 0), "XYZ").to_matrix()
        kw = dict(R=R, studs=[], role="detail")
        ei = R @ Vector((-s * 0.015, 0, 0))                     # r5 / r7 T-a: outer ends in 0.03 in all, inner ends stay
        B.add(ep + ei, (0.110, 0.010, 0.036), BLACK, "Head", bevel=0.005, top=(0.78, 1.0), **kw)  # socket (f85 M3)
        B.add(ep + ei + en * 0.018 + R @ Vector((0, 0, -0.004)), (0.095, 0.010, 0.020), ROSE, "Head", bevel=0.004,
              top=(0.55, 1.0), **kw)                                                            # rose slit (wedge)
        B.add(ep + en * 0.026 + R @ Vector((-s * 0.008, 0, -0.004)), (0.0065, 0.005, 0.020), BLACK, "Head",
              bevel=0.002, **kw)                                                                # reptile pupil
        Rb = face_R(en) @ Euler((0, math.radians(-s * BROW_ROLL), 0), "XYZ").to_matrix()
        bc = ep + en * 0.020 + Vector((0, 0, BROW_DZ)) + Rb @ Vector((-s * BROW_IN, 0, 0))    # f85: kept toward the nose
        B.add(bc, (BROW_HL, 0.036, 0.030), OBS_D, "Head", R=Rb, role="limb",
              rnd=0.2, studs=[], nostud=True)                                                   # heavy brow
        bf = bc + Rb @ Vector((-s * (BROW_HL - 0.018), 0, 0))
        B.spike(bf, Vector((-s * 0.30, -1.0, -0.28)), 0.090, 0.028, OBS_D, "Head", top=(0.12, 0.35),
                nostud=True)                                                            # brow forward point (NICE 3)
    # ================= THE HERO: crown of five obsidian blades framed in gold on an obsidian crown mount. The blades
    # stand side by side (no x overlap, tops fanned outward) so each can lift on its own hinge (act_molt) untouched.
    for s in (1, -1):                                       # crown mount: ends taper to 0.04 high (NICE 2)
        B.seg((0, -0.585, 1.835), (s * 0.26, -0.585, 1.815), 0.034, 0.050, OBS_D, "Head", side=(0, 0, 1),   # r7: 0.22 -> 0.26
              ext=0.02, top=(0.59, 0.85), rnd=0.40)                      # f85 M4: ends 0.30 -> 0.22, dropped 0.02
        # (f85 M4: the two side blocks at s * 0.27 are removed - the blades alone carry the crown)
    # r5 (review 4 MUST 3 + NICE 3): the crown blades grow ~6 % taller (centre 0.30 -> 0.32), same widths (wider ones touch in the molt)
    for i, (x, h, w, roll, back) in enumerate(((-CR_X1, 0.18, 0.042, -24, 24), (-CR_X2, 0.23, 0.050, -12, 24),
                                               (0.0, 0.40, 0.064, 0, 24), (CR_X2, 0.23, 0.050, 12, 24),
                                               (CR_X1, 0.18, 0.042, 24, 24))):
        bone = "Crown_%d" % (i + 1)
        base = Vector((x, -0.585 + abs(x) * 0.08, 1.858 - abs(x) * 0.05))
        up_d = Euler((math.radians(-back), math.radians(roll), 0), "XYZ").to_matrix() @ Vector((0, 0, 1))
        back_d = Vector((0, 1, 0))
        gw0 = 0.020 if i in (0, 4) else 0.038 if i == 2 else 0.028
        gx = 0.0 if i in (0, 4) else 0.004                               # r7 MUST 2: centre / middle +0.004 INWARD (outward touched)
        tip = plate_crown(B, base, up_d, back_d, h, w, bone, gem=(i == 2), gw=gw0, gin=0.25 * gw0 + gx,   # r6 MUST 2: gold +25 % inward (crest only)
                          nib=0.17 if i == 2 else 0.13 if i in (1, 3) else 0.0,                  # f85 M5
                          fd=0.022 if i == 2 else 0.017 if i in (1, 3) else 0.009)
        B.add(base + Vector((0, 0.0, -0.012)), (w * 0.95, 0.042, 0.030), OBS_D, bone,
              R=Euler((0, math.radians(roll), 0), "XYZ").to_matrix(), rnd=0.35)                 # plate socket
        ANCH[bone] = (tuple(base), tuple(tip))
    _xscale(B, ("Head", "Jaw", "Mouth"), HEAD_WX)                 # r9 MUST 1b: a broader, heavier skull
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
        h, e, sh = ANCH.get("Claw_" + side, ((s * 0.39, -0.93, 0.59), (s * 0.42, -0.82, 0.65),
                                             (s * SH_X, SH_Y, SH_Z)))
        k.joint("Arm_" + side, sh, "Neck1")
        k.joint("Claw_" + side, e, "Arm_" + side, tail=tuple(Vector(h) - Vector(e)))
    for i in range(1, 7):
        if "Vent_%d" % i not in ANCH:                                    # r7: Vent_4..6 go with their slits
            continue
        p, bone = ANCH["Vent_%d" % i]
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
    # r10 MUST 3: the paws against the chest / ground body, the skull + jaw against the lowest neck bone, and every
    # crown blade against the Head group (= the skull, the cheek spikes and the new frill) for the molt lift
    for a in ("Arm_L", "Arm_R", "Claw_L", "Claw_R"):
        P += [(a, "Spine"), (a, "Body1"), (a, "Neck2")]
    P += [("Head", "Neck1"), ("Jaw", "Neck1"), ("Head", "Neck2"), ("Jaw", "Neck2")]   # r12: + Neck2 (hood lower panels)
    P += [("Crown_%d" % i, "Head") for i in range(1, 6)]
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
        if i == 3:
            # r10 MUST 3: the centre blade's socket (0.12 wide with its gold side frames) is seated IN the crown mount;
            # its hinge is a segment along the socket, not a point (a 0.07 sphere left the socket ends as 'new' hits
            # once Crown_3 vs Head was checked). Measured: every Crown_3 x Head crossing, rest and all clips, lies in
            # x +/-0.102, y -0.628..-0.536, z 1.809..1.871 (build space) = inside the mount block.
            b = Vector(b) + Vector((0, 0, -0.012))
            out.append((tuple(b - Vector((0.10, 0, 0))), tuple(b + Vector((0.10, 0, 0))), 0.07, "Crown_3"))
        else:
            out.append((b, b, 0.07, "Crown_%d" % i))
    for s, side in ((1, "L"), (-1, "R")):
        out.append(((s * SH_X, SH_Y, SH_Z), (s * SH_X, SH_Y, SH_Z), 0.09, "Arm_" + side))
        out.append(((s * 0.42, -0.82, 0.65), (s * 0.42, -0.82, 0.65), 0.07, "Claw_" + side))   # elbow hinge (r10 x 0.42)
    return out


# r11 MUST 1: scale 1.45 -> 1.60 (review: ~1.54; 1.60 keeps the kit-portrait gold >= 103 on the taller figure: 1.54
# gave 102) and the offset -0.08 -> -0.08 + HEAD_LIFT. The pivot stays the BUILD-space throat
# (THROAT, where the head group is modelled), so the Head joint lands on the raised FRONT[5] (z 1.60) - the same world
# result as the review's 'pivot 1.68 + jaw pivot / Jaw joint +0.18', with no build coordinate to re-type.
HEAD_XF = [((0, -0.50, 1.50), 1.60, ["Head", "Jaw", "Mouth", "Crown_1", "Crown_2", "Crown_3", "Crown_4",
                                      "Crown_5"], (0, 0, -0.08 + HEAD_LIFT))]     # head group built at 1.0, shown 20 % bigger


# ------------------------------------------------------------------ animation (clips 2026-10-27, refs: ANIM_REFS.md)
# No legs: the rear body lies on the ground (all its bends are yaw = in the ground plane, so it never sinks); the reared
# neck holds the head level (cobra, ref S2). The crown blades each hinge on their own bone (Crown_1..5).
import petkit as pk
import _common as cm

NECK3 = ["Neck1", "Neck2", "Neck3"]
CROWN = ["Crown_%d" % i for i in range(1, 6)]
CROWN_OUT = [-1, -1, 0, 1, 1]           # outward roll sign per blade (blade 1 is at -x)
SL_AMP = [3, 6, 9, 10, 10, 9, 8, 7, 6]  # slither curvature amplitude per chain bone (deg), U2


def curve(keys, f):
    """smoothstep through (frame, value) keys"""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            return v0 + (v1 - v0) * u * u * (3 - 2 * u)
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]


def sn(f, n, ph=0.0, cyc=1):
    return math.sin(2 * math.pi * (cyc * f / n + ph))


def rest_chain(k, f, skip=()):
    for b in CHAIN:
        if b not in skip:
            k.key(b, f, rot=(0, 0, 0))


def neck(k, f, pitch=0.0, yaw=0.0, head_pitch=0.0, head_yaw=0.0):
    """pitch < 0 = the neck leans back / rises (each neck bone gets a third, <= 8 deg); the head pitch is separate"""
    for b in NECK3:
        k.key(b, f, rot=(pitch / 3.0, yaw / 3.0, 0))
    k.key("Head", f, rot=(head_pitch, head_yaw, 0))


def crown(k, f, vals):
    """vals: per blade (lift, out[, rise]): lift + = the blade rises (the rest lean-back is 24 deg), out + = it fans
    outward, rise = the blade lifts off its socket (BU, straight up)"""
    for b, sgn, v in zip(CROWN, CROWN_OUT, vals):
        lift, out = v[0], v[1]
        rise = v[2] if len(v) > 2 else 0.0
        k.key(b, f, rot=(lift, 0, sgn * out), loc=(0, 0, rise))   # + pitch = the blade rises toward vertical


def arms(k, f, paddle_l=0.0, paddle_r=0.0, spread=0.0, curl=0.0):
    for s, side, pdl in ((1, "L", paddle_l), (-1, "R", paddle_r)):
        k.key("Arm_" + side, f, rot=(pdl, 0, -s * spread))
        k.key("Claw_" + side, f, rot=(curl, 0, 0))


def idle(k):
    """COBRA SWAY (r11, raised cobra stance; refs S2 C1/C2): the reared neck stands upright and sways slowly side to side
    (a lateral roll, 2.2 deg per neck bone, one sway per loop) with the head held level and turning a little into the
    sway; two slow breaths stay small (neck 1 deg per bone, crown and jaw lift) so the head and crown keep their full
    height from the game camera (the r10 idle leaned the neck back 13.5 deg on each breath, which dropped the head
    toward the camera); the vents smoke on each breath; one quick tail flick at f80."""
    n = 120
    k.new_action("idle", n, True)
    flick = [(0, 0), (74, 0), (78, 8), (81, -3), (86, 0), (120, 0)]
    for f in range(0, n + 1, 2):
        br = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)                  # 0 -> 1 -> 0 twice
        sw = sn(f, n)                                                   # one side-to-side sway per loop
        sw_l = sn(f, n, -0.04)                                          # the head follows the neck ~5 f later
        for b in NECK3:
            k.key(b, f, rot=(-1.0 * br, 0.4 * sw, 2.2 * sw))            # pitch (rise), yaw, ROLL (lateral sway)
        k.key("Head", f, rot=(0.8 * br, 3.0 * sw_l, -4.4 * sw_l))      # level: counter-roll most of the 6.6 deg
        k.key("Jaw", f, rot=(2.25 * br, 0, 0))
        rest_chain(k, f, skip=("Tail3", "Tail4"))
        k.key("Tail3", f, rot=(0, 0.4 * curve(flick, f), 0))
        k.key("Tail4", f, rot=(0, curve(flick, f), 0))
        crown(k, f, [(2.25 * br, 0)] * 5)
        arms(k, f, paddle_l=3 * br, paddle_r=3 * br)
    k.finish()
    k.events["idle"] = {"smoke1": round(30 / n, 3), "flick": round(80 / n, 3), "smoke2": round(90 / n, 3)}


def walk(k):
    """SLITHER (refs U1-U4): a lateral curvature wave runs head -> tail (each chain bone lags the one in front by
    3 f), amplitude growing to mid-body; the reared neck counter-yaws so the head stays on its line; the forearms
    paddle 6 deg. Returns the body travel per cycle (the bends stay put on the ground: wave speed x cycle)."""
    n = 48
    lag = 3
    k.new_action("walk", n, True)
    for f in range(0, n + 1, 2):
        for i, b in enumerate(CHAIN):
            k.key(b, f, rot=(0, SL_AMP[i] * sn(f - lag * i, n), 0))
        nk = -SL_AMP[0] * sn(f, n)                                       # cancels the Spine yaw for the front
        neck(k, f, pitch=0.0, yaw=nk + 1.5 * sn(f, n, 0.25), head_yaw=-0.5 * sn(f, n, 0.25),
             head_pitch=0.6 * sn(f, n, 0.1, 2))
        k.key("Jaw", f, rot=(0, 0, 0))
        crown(k, f, [(0, 0)] * 5)
        arms(k, f, paddle_l=6 * sn(f, n, 0.0), paddle_r=6 * sn(f, n, 0.5))
    k.finish()
    k.meta["walk_cycle"] = n
    k.events["walk"] = {"paddle1": round(12 / n, 3), "paddle2": round(36 / n, 3)}     # forearm paddle peaks
    seg = sum((CP[i + 1] - CP[i]).length for i in range(len(CHAIN))) / len(CHAIN)
    return seg / lag * n


def roar(k):
    """CROWN FLARE (plan; refs #3 + #6): the neck gathers (12 deg up) with the head held level; the five blades flare
    out and up 15 deg with a 2-frame lag (`flare` f20); the jaw opens late, fangs show, the forearms spread (`roar`
    f30); the jaw closes and the blades settle back slower."""
    n = 66
    k.new_action("roar", n, False)
    gather = [(0, 0), (14, -12), (44, -12), (58, -2), (66, 0)]
    head = [(0, 0), (14, 10), (26, 8), (44, 8), (58, 1), (66, 0)]
    jaw = [(0, 0), (24, 0), (30, 26), (44, 24), (54, 2), (66, 0)]
    spread = [(0, 0), (26, 0), (32, 16), (44, 16), (56, 0), (66, 0)]
    for f in range(0, n + 1, 2):
        neck(k, f, pitch=curve(gather, f), head_pitch=curve(head, f))
        k.key("Jaw", f, rot=(curve(jaw, f), 0, 0))
        rest_chain(k, f)
        vals = []
        for i in range(5):
            d = 2 * abs(i - 2)                                           # centre first, the outer blades lag
            u = curve([(0, 0), (14 + d, 0), (22 + d, 1), (44, 1), (60 + d / 2, 0), (66, 0)], f)
            vals.append((15 * u, (10 if i != 2 else 0) * u))
        crown(k, f, vals)
        arms(k, f, spread=curve(spread, f), curl=-0.6 * curve(spread, f))
    k.finish(loop=False)
    k.events["roar"] = {"flare": round(20 / n, 3), "roar": round(30 / n, 3)}


def act_molt(k):
    """THE CROWN SHEDS (plan; refs #9 + U1): the neck arches 22.5 deg with the head level; from f12 the blades lift one
    by one (3-frame lag; f85 C1: the four outer blades 45 deg and fan out like a crest, the centre 35; blade 1 is fully
    up at `lift1` f22); the centre blade rises to 40 and holds while the outer blades drop back (`lift2` f48, `shed`
    f56); a ripple runs along the body (tail -> head, 6 deg per bone, 3-bone lag); the blades reseat in reverse order,
    slower than they rose (centre f84-100, outers by f108); exact rest."""
    n = 110
    k.new_action("act_molt", n, False)
    arch = [(0, 0), (18, -22.5), (84, -22.5), (100, -4), (110, 0)]           # r4 NICE 6: 7.5 deg per neck bone
    head = [(0, 0), (18, 20.5), (84, 20.5), (100, 3), (110, 0)]
    for f in range(0, n + 1, 2):
        neck(k, f, pitch=curve(arch, f), head_pitch=curve(head, f))
        k.key("Jaw", f, rot=(curve([(0, 0), (50, 0), (56, 8), (62, 0), (110, 0)], f), 0, 0))
        vals = []
        for i in range(5):
            up_f = 12 + 3 * i                                            # lift one by one (blade 1 -> 5), 3 f lag; f85 C1: from f12 (was 18) so blade 1 is up at lift1 f22
            back_f = 100 - 2 * i                                         # reseat in reverse order (f85 C1: was 96)
            if i == 2:
                # r4 (review 3 M3): the centre reseat 40 -> 6 takes 11 f (f84-95), peak ~4.6 deg/f < its 5.2 deg/f rise
                keys = [(0, 0), (up_f, 0), (up_f + 10, 35), (44, 35), (52, 40), (84, 40), (100, 6), (106, 0), (110, 0)]
            else:
                keys = [(0, 0), (up_f, 0), (up_f + 10, 50), (44, 50), (54, 10), (84, 10), (back_f, 2), (108, 0), (110, 0)]  # r4: 45 -> 50
            lift = curve(keys, f)
            fan = (18 if i in (0, 4) else 14 if i in (1, 3) else 0) * lift / 35.0     # opens like a crest (front read; f85 middles 10 -> 14)
            vals.append((lift, fan, 0.05 * lift / 40.0 if i == 2 else 0.025 * min(lift, 35.0) / 35.0))
        crown(k, f, vals)
        for i, b in enumerate(CHAIN):                                    # the ripple: tail -> head
            j = len(CHAIN) - 1 - i
            env = curve([(0, 0), (62, 0), (68, 1), (78, 1), (86, 0), (110, 0)], f - 3 * j)
            amp = 4.5 if b == "Spine" else 6.0                         # r4 (review 3 M2): the Spine = chest base <= 5
            k.key(b, f, rot=(0, amp * env * sn(f - 3 * j, 16), 0))
        arms(k, f, curl=curve([(0, 0), (18, 10), (84, 10), (100, 0), (110, 0)], f))
    k.finish(loop=False)
    k.events["act_molt"] = {"lift1": round(22 / n, 3), "lift2": round(48 / n, 3), "shed": round(56 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    act_molt(k)
    return stride
