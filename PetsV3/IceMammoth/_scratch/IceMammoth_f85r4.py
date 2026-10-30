# Ice Mammoth (Glacier egg, MEDIUM 26 %) - FIERCE style (2026-10-27, Glacier update, plan _review/IceMammoth_plan.md
# v2): a huge woolly mammoth under a Roblox stud skin. A lofted barrel body sloping from a high shoulder hump down to
# low hindquarters, covered in shingled wool-lock blocks (3 rows down each flank, a shaggy chest bib), a dark wool mane
# over the head dome, hump and back, columnar legs on flat dark-soled pads with dark toenails, a thin tail with a wool
# tuft. The tall domed head carries small slanted mint eyes under heavy dark brow shelves, small flat ears, two big
# curved ice tusks (3 tapered segments, mint crack lines on the outer one) out of dark sockets, and a 4-segment trunk
# (ridged accordion bands, pale inner strip, dark two-finger tip) that hangs and curls forward. No glow.
import math
import os
from mathutils import Vector, Matrix

DISPLAY = "Ice Mammoth"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 9.0                 # total height (top of the head dome / wool hump) in studs at x1

CHAR_TEAL = (80, 150, 176)   # body, legs, trunk, head (studded) (final85 M1: was (96, 168, 184), read pale aqua)
WOOL_D = (80, 110, 124)      # wool mane: head dome, hump, back, chest bib, tail tuft
BROW_D = (64, 84, 96)        # brow slabs: the darkest of the wool family, so the scowl reads (r3 9+)
BELLY_PALE = (206, 214, 216)  # belly strip, inside of the trunk, chin
TUSK_ICE = (226, 240, 246)   # tusks (smooth)
MINT = (150, 236, 210)       # THE accent: tusk crack lines, tusk caps
EYE_MINT = (56, 196, 168)    # eye slits (final85 M2: a dark-mint slit; MINT read as a pale window)
ICE_MINT = (190, 240, 230)   # short transition ring between the white tusk and its mint cap
DARK = (52, 62, 68)          # tusk sockets, trunk tip, toenails, foot soles
BLACK = (14, 14, 22)         # eye sockets / slit pupils
MOUTH = (86, 18, 30)
MOUTH_IN = (40, 8, 14)       # mouth interior (dark cavity, final85)

H_MODEL = 1.76               # model height in Blender units (same units-per-stud as the Raiju: 1.498 / 8)
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)   # same world stud size as the Raiju
PROTO = os.environ.get("MAMMOTH_PROTO") == "1"                   # build gate: head + trunk + tusks only

# trunk chain (root buried in the face -> tip curling forward), bones Trunk1..Trunk4
TRUNK = [(0, -1.205, 1.07), (0, -1.255, 0.86), (0, -1.28, 0.655), (0, -1.27, 0.455), (0, -1.32, 0.285)]
TRUNK_TIP = (0, -1.425, 0.30)
TRUNK_W = [(0.118, 0.108), (0.100, 0.092), (0.084, 0.078), (0.070, 0.064), (0.060, 0.054)]   # (hw, hd) at each joint
# body loft stations (y, zc, half width, half height), front -> back; the back slopes from the hump to the low rump,
# the belly line rises 0.60 -> 0.69
BODY = [(-0.86, 1.18, 0.22, 0.30), (-0.70, 1.13, 0.36, 0.46), (-0.46, 1.09, 0.42, 0.50), (-0.14, 1.03, 0.41, 0.44),
        (0.18, 0.99, 0.38, 0.38), (0.46, 0.96, 0.35, 0.31), (0.68, 0.95, 0.29, 0.26), (0.82, 0.94, 0.17, 0.16)]
SPLIT_Y = -0.10
LEGS = {"F": ((0.25, -0.50, 1.00), (0.25, -0.44, 0.58), (0.25, -0.48, 0.21), (0.25, -0.49, 0.07)),
        "B": ((0.22, 0.50, 0.95), (0.22, 0.40, 0.58), (0.22, 0.54, 0.26), (0.22, 0.50, 0.07))}
TAILP = [(0, 0.84, 1.08), (0, 0.90, 0.97), (0, 0.925, 0.86), (0, 0.93, 0.76)]
THROAT = Vector((0, -0.90, 1.06))
JAW_DROP = 0.020                     # r3 CM1b: roar jaw slide-down at the 22 deg peak
JAW_P = Vector((0, -0.97, 0.99))   # r2 CM1: the hinge at the back of the chin (was -1.08, 0.98: mid-chin, so the
#                                    open jaw barely made a gap); the chin front now drops ~0.07 at 20 deg
S_HEAD = 1.12                # the head group (head, trunk, tusks, ears) is scaled about the throat


_L = {}


def loft():
    if "b" not in _L:
        import curveloft as cl
        _L["b"] = cl.Loft(BODY, n=2.5, seg=24)
    return _L["b"]


def surf(L, y, a, grow=0.0):
    """point on loft L at y, section angle a (0 = +x side, pi/2 = top) + its outward normal"""
    s = L.s_at_y(y)
    p = L.surf(s, a, grow=grow)
    t1 = L.surf(s, a + 0.03, grow=grow) - L.surf(s, a - 0.03, grow=grow)
    t2 = L.surf(min(L.length, s + 0.01), a, grow=grow) - L.surf(max(0.0, s - 0.01), a, grow=grow)
    n = t1.cross(t2).normalized()
    if n.dot(p - L.at(s)[0]) < 0:
        n = -n
    return p, n


def lock(B, p, n, L, hw, hd, color, bone, flare=0.18, sway=0.0):
    """pointed wool lock hanging down along the surface from p (normal n): width along the body, thin along n.
    flare = how far the tip stands off the body, sway = tip shift along the body (shaggy irregularity)"""
    down = Vector((0, 0, -1))
    dt = (down - n * down.dot(n))
    dt = dt.normalized() if dt.length > 1e-4 else down
    p0 = p + n * (hd * 0.6) - dt * 0.03
    p1 = p0 + dt * L + n * (L * flare) + Vector((0, sway, 0))
    B.seg(p0, p1, hw, hd, color, bone, side=(0, 1, 0), top=(0.42, 0.60), rnd=0.40, role="limb")


def cuff(B, K, A, hw, hd, bone, seg=16):
    """shaggy wool cuff: a studded superellipse loft from just above the knee K down the top quarter of the shin K -> A,
    0.022 proud of the shin (half width hw, half depth hd), flaring at a jagged hem (alternate points hang lower)"""
    import blockkit as bk
    K, A = Vector(K), Vector(A)
    R = bk.frame_from(K, A, (1, 0, 0))
    L = (A - K).length
    rings = []
    for f, grow, jag in ((-0.10, 0.012, 0.0), (0.0, 0.022, 0.0), (0.30, 0.030, 0.0), (0.50, 0.040, 0.07)):   # r2 MM1
        r = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            cs, sn = math.cos(a), math.sin(a)
            ff = f + (jag if i % 2 else 0.0)
            c = K + (A - K) * ff
            r.append(c + R @ Vector(((hw + grow) * math.copysign(abs(cs) ** (2 / 2.4), cs),
                                     (hd + grow) * math.copysign(abs(sn) ** (2 / 2.4), sn), 0.0)))
        rings.append(r)
    return B.tube(rings, WOOL_D, bone)


def HX(p):
    """build-space point of the head group -> world (scaled S_HEAD about the throat)"""
    return THROAT + (Vector(p) - THROAT) * S_HEAD


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def tusk_pts(s):
    """tusk centreline (left side s = 1): socket -> down-forward-out -> forward -> up-in tip"""
    p0 = Vector((s * 0.135, -1.15, 1.05))
    p1 = p0 + Vector((s * 0.075, -0.11, -0.20))
    p2 = p1 + Vector((s * 0.050, -0.22, -0.035))
    p3 = p2 + Vector((-s * 0.035, -0.15, 0.15))
    tip = p3 + Vector((-s * 0.050, -0.03, 0.16))
    return [p0, p1, p2, p3, tip]


def _cr(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def tusk_curve(s, n=16):
    """smooth Catmull-Rom centreline through tusk_pts + radius taper (socket 0.064 -> tip point)"""
    P = tusk_pts(s)
    E = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    C = []
    seg = len(P) - 1
    for i in range(n + 1):
        u = i / n * seg
        j = min(int(u), seg - 1)
        C.append(_cr(E[j], E[j + 1], E[j + 2], E[j + 3], u - j))
    R = [0.074 * (1 - (i / n) ** 1.5) + 0.004 for i in range(n + 1)]
    return C, R


def tube_rings(C, R, m=10):
    """circular rings of radius R[i] around C[i], perpendicular to the curve (parallel-transported frame)"""
    rings = []
    ref = Vector((1, 0, 0))
    for i, c in enumerate(C):
        d = (C[min(i + 1, len(C) - 1)] - C[max(i - 1, 0)]).normalized()
        a = (ref - d * ref.dot(d)).normalized()
        ref = a
        b = d.cross(a).normalized()
        rings.append([c + (a * math.cos(2 * math.pi * j / m) + b * math.sin(2 * math.pi * j / m)) * R[i]
                      for j in range(m)])
    return rings


def trunk_part(B, k_, a, b, wa, wb, bone, bands=2):
    """one trunk segment a -> b as `bands` stacked ridged bands (each narrows toward its lower end), body colour,
    with a pale strip down the inner (back) side"""
    for i in range(bands):
        t0, t1 = i / bands, (i + 1) / bands
        p0, p1 = a.lerp(b, t0), a.lerp(b, t1)
        w0 = (wa[0] + (wb[0] - wa[0]) * t0, wa[1] + (wb[1] - wa[1]) * t0)
        w1 = (wa[0] + (wb[0] - wa[0]) * t1, wa[1] + (wb[1] - wa[1]) * t1)
        sx, sy = w1[0] / w0[0] * 0.94, w1[1] / w0[1] * 0.94
        B.seg(p0, p1, w0[0], w0[1], CHAR_TEAL, bone, side=(1, 0, 0), ext=0.012, ext1=0.0, top=(sx, sy), rnd=0.40,
              role="limb")
    d = (b - a).normalized()
    back = Vector((1, 0, 0)).cross(d).normalized()                  # the trunk's inner (back) face direction
    if back.y < 0:
        back = -back
    B.seg(a + back * (wa[1] * 0.78), b + back * (wb[1] * 0.70), wa[0] * 0.62, 0.016, BELLY_PALE, bone,
          side=(1, 0, 0), top=(wb[0] / wa[0], 1), studs=[], role="limb", ext=0.0)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=77, tier=3, plates=False, th=0.94)
    # ================= HEAD (pivot at the throat): tall skull, wool dome, sloping face, cheeks, brows, eyes, ears
    B.add((0, -1.045, 1.30), (0.215, 0.178, 0.26), CHAR_TEAL, "Head", top=(0.74, 0.70), bot=(0.88, 0.86), rnd=0.55)
    B.seg((0, -1.03, 1.52), (0, -1.205, 1.10), 0.175, 0.10, CHAR_TEAL, "Head", top=(0.82, 0.9), ext=0.03, rnd=0.55)
    for s in (1, -1):                                                         # cheeks over the tusk roots
        B.add((s * 0.14, -1.09, 1.10), (0.085, 0.13, 0.13), CHAR_TEAL, "Head", rot=(12, 0, 0), top=(0.85, 0.8),
              rnd=0.42)
    # wool dome (mane) over the crown, rising to the top of the pet
    B.add((0, -1.02, 1.585), (0.17, 0.15, 0.10), WOOL_D, "Head", top=(0.55, 0.55), rnd=0.45)
    for base, d, L in (((0, -1.08, 1.56), (0, -0.45, 1.0), 0.11), ((0, -0.96, 1.585), (0, 0.2, 1.0), 0.11)):
        B.spike(base, d, L, 0.098, WOOL_D, "Head", top=(0.62, 0.62), studs=None, role="limb", rnd=0.55)  # 2 big clumps
    # heavy dark brow shelf (a V, inner ends low) over small deep-set slanted mint eyes with a black slit pupil
    for s in (1, -1):
        B.add((s * 0.098, -1.188, 1.410), (0.108, 0.042, 0.036), BROW_D, "Head", rot=(-22, -s * 28, 0),
              role="detail", bevel=0.012)                                   # final85 TO9 1: a scowl over the slit
        rot = (0, -s * 17, s * 14)
        B.add((s * 0.128, -1.186, 1.350), (0.084, 0.012, 0.028), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.005)                                                  # final85 M2: black socket, larger
        B.add((s * 0.130, -1.195, 1.350), (0.056, 0.008, 0.009), EYE_MINT, "Head", rot=rot, studs=[], role="detail",
              bevel=0.004)
        # (r3 9+: the black pupil is gone, so the teal slit reads as one line, not a visor)
    # small flat ears on the sides of the head (not floppy)
    for s, side in ((1, "L"), (-1, "R")):
        B.add((s * 0.218, -0.91, 1.27), (0.028, 0.095, 0.105), CHAR_TEAL, "Ear_" + side, rot=(-12, 0, s * 28),
              top=(0.70, 0.55), bot=(0.9, 0.75), rnd=0.48, role="limb")                    # rounded flap, back edge out
        for dz, L in ((-0.06, 0.10), (0.02, 0.09)):                                       # hairy fringe at its rim
            B.spike((s * 0.245, -0.85, 1.27 + dz), (s * 0.55, 0.75, -0.35), L, 0.035, WOOL_D, "Ear_" + side,
                    top=(0.2, 0.4))
    # lower lip / chin under the trunk root (pale), dark mouth line
    B.seg((0, -0.98, 0.99), (0, -1.16, 0.95), 0.10, 0.045, BELLY_PALE, "Jaw", top=(0.85, 0.8), rnd=0.40)
    B.add((0, -1.10, 0.995), (0.075, 0.07, 0.006), MOUTH, "Head", studs=[], role="detail", bevel=0.003)
    # final85 TO9 3: a dark mouth interior riding the jaw, hidden in the head when closed; the roar's 18 deg jaw shows a
    # dark cavity under the trunk root instead of a pale gap
    B.add((0, -1.09, 1.005), (0.092, 0.085, 0.030), MOUTH_IN, "Jaw", studs=[], role="detail", bevel=0.020)   # r3 +0.03 fwd, r4 0.01 back
    # ================= TUSKS: dark socket, a smooth curved ice tube (socket -> down-out -> forward -> up-in tip),
    # 2 mint crack lines across the outer third
    for s in (1, -1):
        P = tusk_pts(s)
        d0 = (P[1] - P[0]).normalized()
        B.seg(P[0] - d0 * 0.05, P[0] + d0 * 0.055, 0.092, 0.092, CHAR_TEAL, "Head", top=(0.95, 0.95), rnd=0.42)
        B.seg(P[0] + d0 * 0.05, P[0] + d0 * 0.085, 0.086, 0.086, WOOL_D, "Head", rnd=0.35, role="limb", nostud=True)
        C, R = tusk_curve(s)
        B.tube(tube_rings(C, R, 10), TUSK_ICE, "Head", nostud=True)
        i0 = int(0.60 * (len(C) - 1))                                       # mint ice cap on the tusk tip
        im = int(0.52 * (len(C) - 1))                                       # pale ice-mint ring: soft cap edge
        B.tube(tube_rings(C[im:i0 + 1], [r + 0.002 for r in R[im:i0 + 1]], 10), ICE_MINT, "Head", nostud=True)
        B.tube(tube_rings(C[i0:], [r + 0.004 for r in R[i0:]], 10), MINT, "Head", nostud=True)
        for t in (0.55, 0.68, 0.79):
            i = int(t * (len(C) - 1))
            c, d = C[i], (C[i + 1] - C[i - 1]).normalized()
            r = R[i]
            out = Vector((s, 0, 0))
            out = (out - d * out.dot(d)).normalized()
            upv = d.cross(out).normalized()
            if upv.y > 0:
                upv = -upv
            q0 = c + (out * 0.9 - upv * 0.45).normalized() * (r + 0.002) - d * 0.010
            q1 = c + out * (r + 0.002) + d * 0.012
            q2 = c + (out * 0.55 + upv * 0.85).normalized() * (r + 0.002) - d * 0.006
            q3 = c + upv * (r + 0.002) + d * 0.008
            for u, v in ((q0, q1), (q1, q2), (q2, q3)):
                B.bar(u, v, ((u + v) / 2 - c).normalized(), 0.035, 0.012, MINT, "Head", studs=[], bevel=0.004)
    # ================= TRUNK: 4 ridged segments, pale inner strip, dark two-finger tip curling forward
    T = [Vector(p) for p in TRUNK]
    for i in range(4):
        trunk_part(B, k, T[i], T[i + 1], TRUNK_W[i], TRUNK_W[i + 1], "Trunk%d" % (i + 1), bands=3 if i < 2 else 2)
    tip = Vector(TRUNK_TIP)
    d = (tip - T[4]).normalized()
    B.seg(T[4], tip, TRUNK_W[4][0], TRUNK_W[4][1], CHAR_TEAL, "Trunk4", side=(1, 0, 0), ext=0.03, top=(1.1, 1.0),
          rnd=0.40, role="limb")
    B.seg(tip - d * 0.02, tip + d * 0.035, TRUNK_W[4][0] * 1.08, TRUNK_W[4][1] * 1.05, DARK, "Trunk4",
          side=(1, 0, 0), rnd=0.40, role="limb", nostud=True)                       # dark flared tip
    for s in (1, -1):                                                       # two finger lips at the tip
        B.spike(tip + Vector((s * 0.026, 0, 0.012)), d + Vector((0, 0, 0.55)), 0.06, 0.022, DARK, "Trunk4",
                top=(0.35, 0.45))
    for blk in B.items:                                       # scale the whole head group about the throat
        if isinstance(blk, bk.Tube):
            blk.map(HX)
        else:
            blk.c = HX(blk.c)
            blk.h = blk.h * S_HEAD
            if blk.bevel is not None:
                blk.bevel *= S_HEAD
    if PROTO:
        B.seg((0, -0.70, 1.25), (0, -0.98, 1.30), 0.24, 0.28, CHAR_TEAL, "Neck", ext=0.04)
        B.build()
        bk.stud_skin(k, PITCH)
        return {"TH": round(B.th, 3), "PITCH": PITCH, "proto": True}
    Lb = loft()
    sy = Lb.s_at_y
    # ================= BODY: lofted barrel split Chest | Spine, the back sloping from the hump to the low rump
    sj = sy(SPLIT_Y)
    Lb.tube(B, 0.0, sj + 0.06, CHAR_TEAL, "Chest", j1=sj, step=0.11)
    Lb.tube(B, sj - 0.06, Lb.length, CHAR_TEAL, "Spine", j0=sj, step=0.11)
    Lb.band(B, sy(-0.60), sj, BELLY_PALE, "Chest", zlo=-1.0, zhi=-0.18, grow=0.008, step=0.08)       # pale belly
    Lb.band(B, sj, sy(0.84), BELLY_PALE, "Spine", zlo=-1.0, zhi=-0.18, grow=0.008, step=0.08)
    # dark wool mane over the back (hump -> mid back), a dome over the shoulders
    Lb.band(B, sy(-0.84), sj, WOOL_D, "Chest", zlo=0.66, grow=0.026, inset=0.02, step=0.08)
    Lb.band(B, sj, sy(0.40), WOOL_D, "Spine", zlo=0.74, grow=0.022, inset=0.02, step=0.08, narrow1=0.55)
    for y in (-0.42, -0.06):
        Lb.band(B, sy(y) - 0.009, sy(y) + 0.009, CHAR_TEAL, "Chest" if y < SPLIT_Y else "Spine", zlo=0.64,
                grow=0.030, inset=0.02, step=0.009)
    # mane ridge tufts laid back along the spine (the shaggy hump silhouette)
    for y, L, ang, bn in ((-0.74, 0.11, 60, "Chest"), (-0.58, 0.12, 64, "Chest"), (-0.42, 0.12, 66, "Chest"),
                          (-0.26, 0.12, 68, "Chest"), (-0.10, 0.11, 70, "Chest"), (0.07, 0.10, 72, "Spine"),
                          (0.23, 0.10, 74, "Spine")):
        c = Lb.at(sy(y))
        top = c[0] + Vector((0, 0, c[4] + 0.01))
        if bn == "Chest" and -0.62 < y < -0.40:
            top.z = max(top.z, 1.60)
        d = (0, math.sin(math.radians(ang)), math.cos(math.radians(ang)))
        B.spike(top - Vector((0, 0, 0.05)), d, L + 0.05, 0.085, WOOL_D, bn, top=(0.7, 0.7), studs=None,
                role="limb", rnd=0.45)                                                  # laid-back wool clump
    # ================= WOOL LOCKS: 3 shingled rows down each flank (top row dark), pointed hanging blocks
    ROWS = ((0.40, 0.19, WOOL_D, 0.0, 0.16), (0.02, 0.20, CHAR_TEAL, 0.5, 0.12), (-0.38, 0.11, CHAR_TEAL, 0.0, 0.10))  # r3
    for f, L, col, off, var in ROWS:
        a = Lb.zang(f)
        n_ = 9
        for i in range(n_):
            y = -0.66 + (i + off) * 0.155
            if y > 0.68:
                continue
            for s in (1, -1):
                p, nrm = surf(Lb, y, a if s > 0 else math.pi - a)
                bn = "Chest" if y < SPLIT_Y else "Spine"
                r = (i * 7 + int(f * 10) + (0 if s > 0 else 1)) % 3 - 1
                ln = L * (1.0 + var * r)
                lock(B, p, nrm, ln, 0.098, 0.036, col, bn, flare=0.16 + 0.06 * r, sway=0.025 * r)
    # r3 9+: a short WOOL_D fringe on the pale belly's lower edge (between the legs), so the belly reads as wool,
    # not a flat plate, in model_side (a 2-row WOOL_D strip at its top edge hid under the lock row and cost 1.3k tris)
    for j, y in enumerate((-0.22, -0.11, 0.00, 0.11, 0.22)):
        for s in (1, -1):
            p, nrm = surf(Lb, y, Lb.zang(-0.84) if s > 0 else math.pi - Lb.zang(-0.84))
            r = (j + (0 if s > 0 else 1)) % 2
            lock(B, p, nrm, 0.085 + 0.020 * r, 0.056, 0.026, WOOL_D, "Chest" if y < SPLIT_Y else "Spine",
                 flare=0.06, sway=0.012 * (1 - 2 * r))
    # chest bib: shaggy dark wool hanging at the chest front (in front of the front legs)
    for x, L in ((0.0, 0.30), (0.10, 0.26), (-0.10, 0.26), (0.19, 0.20), (-0.19, 0.20)):
        p = Vector((x, -0.86 + abs(x) * 0.25, 1.02))
        B.seg(p + Vector((0, 0, 0.06)), p + Vector((0, -0.04, -L)), 0.055, 0.040, WOOL_D, "Chest",
              side=(1, 0, 0), top=(0.30, 0.6), rnd=0.35, role="limb")
    # ================= NECK: short and thick, mane over the nape
    B.seg((0, -0.70, 1.22), (0, -0.98, 1.30), 0.25, 0.29, CHAR_TEAL, "Neck", ext=0.05, rnd=0.42)
    B.seg((0, -0.72, 1.47), (0, -0.98, 1.50), 0.20, 0.07, WOOL_D, "Neck", top=(0.8, 1), ext=0.03, rnd=0.42)
    # ================= LEGS: thick columns, flat round pads with a dark sole rim and 4 dark toenails
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.10)), K, 0.175, 0.19, CHAR_TEAL, leg, ext=0.0, ext1=0.04, top=(0.90, 0.86))
                B.seg(K, A, 0.155, 0.16, CHAR_TEAL, shin, top=(0.95, 0.95), ext=0.04, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.03, 0.10)), K, 0.165, 0.21, CHAR_TEAL, leg, bot=(0.85, 1), top=(0.82, 0.72),
                      ext=0.0, ext1=0.04)
                B.seg(K, A, 0.14, 0.145, CHAR_TEAL, shin, top=(0.95, 0.95), ext=0.04, ext1=0.02)
                B.seg(A, P + Vector((0, 0.0, 0.07)), 0.14, 0.14, CHAR_TEAL, foot, ext=0.03, top=(1.05, 1.05))
            # final85 M3: a shaggy WOOL_D cuff over the knee and the top quarter of the shin (a second band on the
            # legs, like a real mammoth's shaggy legs): a studded loft 0.022 proud of the shin, with a jagged hem
            cuff(B, K, A, 0.155 if fb == "F" else 0.14, 0.16 if fb == "F" else 0.145, shin)
            B.add(P + Vector((0, 0.0, 0.08)), (0.180, 0.185, 0.07), CHAR_TEAL, foot, top=(0.88, 0.88), rnd=0.40)
            B.add(P + Vector((0, 0.0, 0.022)), (0.188, 0.193, 0.022), DARK, foot, studs=[], rnd=0.40, role="limb")
            for gx in (-0.105, -0.036, 0.036, 0.105):
                B.add((P.x + gx, P.y - 0.170, 0.052), (0.030, 0.026, 0.034), DARK, foot, top=(0.80, 0.55),
                      top_shift=(0, 0.008), role="limb", nostud=True)
    # ================= TAIL: thin, hanging, a dark wool tuft
    T = [Vector(p) for p in TAILP]
    for (a, b), w, bn in zip(zip(T, T[1:]), (0.040, 0.034, 0.028), ("Tail1", "Tail2", "Tail3")):
        B.seg(a, b, w, w, CHAR_TEAL, bn, ext=0.04, top=(0.85, 0.85))
    tp = T[3]
    for dx, dy, L in ((0, 0.0, 0.18), (0.55, 0.25, 0.14), (-0.55, 0.25, 0.14), (0, 0.6, 0.12)):
        B.spike(tp + Vector((0, 0, 0.04)), (dx, dy, -1), L, 0.05, WOOL_D, "Tail3", top=(0.2, 0.3))
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.30, 1.00), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, SPLIT_Y, 1.04), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.70, 1.18), "Chest", tail=(0, -0.2, 0.0))
    k.joint("Head", tuple(THROAT), "Neck", tail=(0, -0.3, 0.1))               # throat pivot (low/back)
    k.joint("Jaw", tuple(HX(JAW_P)), "Head", tail=(0, -0.1, -0.05))
    k.joint("Breath", tuple(HX((0, -1.30, 0.95))), "Head", tail=(0, -0.1, 0))
    prev = "Head"
    for i in range(4):
        a, b = HX(TRUNK[i]), HX(TRUNK[i + 1])
        k.joint("Trunk%d" % (i + 1), tuple(a), prev, tail=tuple(b - a))
        prev = "Trunk%d" % (i + 1)
    k.joint("Trunk_Tip", tuple(HX(TRUNK_TIP)), "Trunk4", tail=(0, -0.05, 0.05))
    k.joint("Back", (0, -0.30, 1.56), "Chest", tail=(0, 0, 0.15))
    for s, side in ((1, "L"), (-1, "R")):
        P = tusk_pts(s)
        k.joint("Tusk_" + side, tuple(HX(P[4])), "Head", tail=(0, -0.05, 0.08))
        k.joint("Ear_" + side, tuple(HX((s * 0.20, -0.92, 1.30))), "Head", tail=(s * 0.1, 0.05, 0))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, P_ = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2", tail=(0, 0.01, -0.2))
    # VFX anchors (plan section 8): bones without mesh, parented to the bone that carries the effect
    k.joint("FX_SnowSpray", tuple(HX(Vector(TRUNK_TIP) + Vector((0, -0.04, 0.0)))), "Trunk_Tip", tail=(0, -0.08, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("FX_TuskSparkle_" + side, tuple(HX(tusk_pts(s)[4])), "Tusk_" + side, tail=(0, 0, 0.06))
    k.joint("FX_FrostPuff", (0, -0.30, 1.62), "Back", tail=(0, 0, 0.1))
    k.joint("FX_IceCrack", (0.25, -0.49, 0.02), "Foot_FL", tail=(0, -0.1, 0))
    k.joint("FX_BreathCloud", tuple(HX((0, -1.34, 0.95))), "Breath", tail=(0, -0.1, 0))


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Head", "Chest"), ("Jaw", "Chest"), ("Ear_L", "Ear_R"),
         ("Tail2", "Shin_BL"), ("Tail2", "Shin_BR"), ("Tail3", "Shin_BL"), ("Tail3", "Shin_BR"),
         ("Tail3", "Foot_BL"), ("Tail3", "Foot_BR")]
    for t in ("Trunk2", "Trunk3", "Trunk4"):
        P += [(t, "Head"), (t, "Jaw"), (t, "Chest"), (t, "Leg_FL"), (t, "Leg_FR"), (t, "Shin_FL"), (t, "Shin_FR"),
              (t, "Foot_FL"), (t, "Foot_FR"), (t, "Neck")]
    P += [("Trunk3", "Trunk1"), ("Trunk4", "Trunk1"), ("Trunk4", "Trunk2"), ("Head", "Shin_FL"), ("Head", "Shin_FR")]
    return P


def joints():
    """throat hinge carried by the Head: the skull's lower back corner meets the chest bib at the pivot"""
    return [((-0.24, -0.88, 1.03), (0.24, -0.88, 1.03), 0.09, "Head")]


# ------------------------------------------------------------------ animation (plan section 7 + ANIM_REFS.md)
import petkit as pk
import _common as cm
import bpy

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]
TRK = ["Trunk1", "Trunk2", "Trunk3", "Trunk4"]


def tab(T, f):
    """eased (smoothstep) interpolation through [(frame, value | tuple)]"""
    if f <= T[0][0]:
        return T[0][1]
    for (f0, v0), (f1, v1) in zip(T, T[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / (f1 - f0) if f1 > f0 else 1.0
            u = u * u * (3 - 2 * u)
            if isinstance(v0, tuple):
                return tuple(a + (b - a) * u for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * u
    return T[-1][1]


def trunk(k, f, pitch=(0, 0, 0, 0), roll=(0, 0, 0, 0)):
    """pitch - curls the hanging trunk FORWARD / UP (each bone relative to the one above), roll + swings it to -x"""
    for b, p, r in zip(TRK, pitch, roll):
        k.key(b, f, rot=(p, 0, r))
    k.key("Trunk_Tip", f, rot=(0, 0, 0))


def tail(k, f, pitch=0.0, roll=0.0, lag=(1.0, 0.8, 0.6)):
    """pitch + lifts the hanging tail backward, roll swings it sideways"""
    for b, g in zip(TAIL, lag):
        k.key(b, f, rot=(pitch * g, 0, roll * g))


def ears(k, f, flare=0.0):
    """flare + swings the back edge of both ear flaps out from the head"""
    k.key("Ear_L", f, rot=(0, -flare, 0))
    k.key("Ear_R", f, rot=(0, flare, 0))


def neck_lift(hd):
    """neck offset for a head pitch of hd deg (head + neck). Pitch-UP: the neck reaches forward and up so the back of
    the wool dome clears the shoulder hump. Pitch-DOWN past 6 deg (the scoops): the neck reaches forward so the chin
    clears the chest bib."""
    u = max(0.0, -hd) / 15.0
    d = max(0.0, hd - 6.0) / 12.0
    return (0, -0.05 * u - 0.05 * d, 0.045 * u)


def bell(f, c, w):
    """smooth 0..1..0 bump centred on frame c, half width w"""
    u = abs(f - c) / w
    return 0.0 if u >= 1 else 0.5 + 0.5 * math.cos(math.pi * u)


def idle(k):
    """TRUNK SWING: the trunk swings slowly side to side as a lagged chain (tip +-12 deg, two cycles), three slow
    breaths, an exhale at f80 (the trunk tip lifts, the ears flick out). Tusks still, feet planted."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        br = 0.5 + 0.5 * pk.wave(f, n, 0.25, 3)                     # 0..1, three breaths
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, -0.004 * br))
        k.key("Chest", f, rot=(3.0 * br, 0, 0))                    # final85: breath 0.5 -> 1.2 -> 2.0 -> 3.0 deg (r4)
        ex = bell(f, 80, 12)                                        # the exhale
        k.key("Neck", f, rot=(0.6 * br - 1.0 * ex, 0, 0))
        k.key("Head", f, rot=(0.8 * pk.wave(f, n, 0.1, 2) - 1.5 * ex, 0, 0))
        k.key("Jaw", f, rot=(1.5 * ex, 0, 0))
        rl = [a * pk.wave(f, n, -0.07 * i, 2) for i, a in enumerate((3.2, 4.8, 5.6, 5.6))]   # tip +-12 -> 16 -> 19 (r4)
        pt = [1.0 * pk.wave(f, n, 0.25 - 0.07 * i, 2) - c * ex for i, c in enumerate((2, 4, 8, 12))]
        trunk(k, f, pt, rl)
        tail(k, f, 4 + 3 * br, 9 * pk.wave(f, n, 0.15, 2), lag=(1.0, 0.9, 0.8))
        ears(k, f, 3 * pk.wave(f, n, 0.3, 2) + 9 * bell(f, 82, 8) + 13 * bell(f, 40, 6))   # C1: ear flap at f40 (8 -> 10 -> 13, r4)
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4
    k.events["idle"] = {"exhale": round(80 / n, 3)}


def walk(k):
    """HEAVY LATERAL-SEQUENCE WALK (Muybridge plate 733): hind then fore on the same side, high duty, the body sinks
    after each contact and rolls away from the swinging side, the trunk swings 6 deg per step, the tail lags."""
    n = 40

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.7 * pk.wave(f, n, 0.1, 2), 1.0 * pk.wave(f, n, 0.0), -2.5 * pk.wave(f, n, 0.25)),
              loc=(0, 0, -0.022 - 0.012 * b))              # rolls toward the planted side (left legs swing ~f29-f10)
        # (per-clip r4: roll 1.5 -> 2.5 deg, pitch rock 0.4 -> 0.7, sink 0.008 -> 0.012, so the back line moves)
        k.key("Chest", f, rot=(0.6, -1.2 * pk.wave(f, n, 0.25), -1.0 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(0.8 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(-0.8 * pk.wave(f, n, 0.25, 2), 1.0 * pk.wave(f, n, 0.3), 0))
        k.key("Jaw", f, rot=(1.0, 0, 0))
        # per-clip r4: the trunk swings like a pendulum with each step (fore-aft, read in the side view): 3 -> 11 deg
        # summed (f10 -> f20 tip travel 0.09 -> >= 0.2 BU); the side swing (one cycle) 3 -> 6 deg
        pt = [a * pk.wave(f, n, 0.3 - 0.06 * i, 2) for i, a in enumerate((2.3, 3.0, 3.0, 3.0))]   # peaks ~f8/f18
        rl = [a * pk.wave(f, n, 0.3 - 0.07 * i) for i, a in enumerate((1.2, 1.6, 1.6, 1.6))]       # r4: 3 -> 6 deg
        trunk(k, f, pt, rl)
        tail(k, f, 6, 9 * pk.wave(f, n, 0.3), lag=(1.0, 0.9, 0.8))
        ears(k, f, 3 * pk.wave(f, n, 0.2, 2))
    # TRUE lateral sequence (plate 733): touch-downs LH f0, LF f10, RH f20, RF f30. (cm.quad_walk "walk" measured
    # BL, FR, BR, FL = a diagonal sequence, so the offsets are set here.)
    legs = [("Leg_BL", 0.0), ("Leg_FL", 0.75), ("Leg_BR", 0.5), ("Leg_FR", 0.25)]
    k.meta["legs"], k.meta["duty"] = legs, 0.72
    stride = pk.walk_cycle(k, n, legs, 0.115, 0.075, body, duty=0.72)
    k.events["walk"] = {"stomp": 0.25}                             # Leg_FL touches down at f10 (FX_IceCrack)
    return stride


ROAR_P = [  # f, chest z, chest pitch, neck, head, jaw, trunk pitch x4, tail pitch, ear flare
    (0, 0.0, 0.0, 0, 0, 0, (0, 0, 0, 0), 0, 0),
    (8, -0.006, 0.5, 1, 4, 0, (2, 4, 6, 10), 6, -4),
    (16, -0.010, -0.6, -2, -9, 2, (-40, -30, -12, -4), 30, 8),
    (22, -0.010, -1.0, -2, -13, 6, (-62, -48, -16, -6), 42, 14),
    (26, -0.010, -1.0, -2, -13, 9, (-66, -52, -18, -6), 45, 16),
    (30, -0.010, -1.0, -2, -13, 13, (-76, -52, -18, -6), 45, 16),     # r2 CM1: the root lifts 10 more (f30-50) so it
    (34, -0.010, -1.0, -2, -13, 22, (-76, -52, -18, -6), 45, 16),     # clears the chin; jaw fully open f34, 22 deg (r3)
    (50, -0.010, -1.0, -2, -13, 16, (-76, -52, -18, -6), 45, 16),     # (final85: 14 -> 18 -> 20 at f34; 16 at f50)
    (58, -0.006, -0.4, -1, -6, 4, (-30, -20, -8, -2), 22, 6),
    (66, 0.0, 0.0, 0, 0, 0, (0, 0, 0, 0), 0, 0)]


def roar(k):
    """TRUMPET: a small tuck of the head (anticipation), then the head lifts 15 deg and the trunk rises fast and curls
    up to the sky in front of the brow; the mouth opens after the lift (jaw lag); hold with a trunk tremble, ears
    spread, tail up; the trunk lowers more slowly than it rose. Legs planted."""
    n = 66
    k.new_action("roar", n, False)
    for f, cz, cp, nk, hd, jw, tp, tl, er in ROAR_P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Chest", f, rot=(cp, 0, 0), loc=(0, 0, cz))
        k.key("Neck", f, rot=(nk, 0, 0), loc=neck_lift(hd + nk))
        k.key("Head", f, rot=(hd, 0, 0))
        # r3 CM1b: the cheeks hang over the chin, so from the side the hinge alone only shows a thin wedge; the jaw
        # also slides down (a real jaw drop), up to 0.02 at the 22 deg peak, so the dark interior shows as a band
        k.key("Jaw", f, rot=(jw, 0, 0), loc=(0, 0, -JAW_DROP * max(0.0, jw - 6) / 16.0))
        trunk(k, f, tp)
        k.key("Trunk1", f, loc=(0, 0, 0.02 * min(1.0, max(0.0, -tp[0] / 62.0))))   # TO9 3: the trunk root lifts 0.02
        tail(k, f, tl, 0, lag=(1.0, 0.5, 0.3))
        ears(k, f, er)
    for f in range(28, 50, 2):                                     # trunk tremble +-3 deg (the trumpet; r2: was +-2)
        d = 3.0 if (f // 2) % 2 else -3.0
        root = -66.0 - 10.0 * min(1.0, (f - 26) / 4.0)            # r2 CM1: the root lifts -66 -> -76 by f30
        tp = tuple(v + d * w for v, w in zip((root, -52, -18, -6), (0.2, 0.4, 0.7, 1.0)))
        trunk(k, f, tp)
        ears(k, f, 16 + 0.5 * d)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)
    k.events["roar"] = {"trumpet": round(26 / n, 3)}


DUST_P = [  # f, head pitch, neck, trunk pitch x4, tail pitch, tail roll
    # final85 C2: every scoop HOLDS its deepest pose on the snow for 4 frames (f18-22, f64-68, f78-82), so it reads as
    # a scoop, not a one-frame tap; the moves around the holds are 1-2 frames tighter. The head dips 0.5 deg more
    # at the holds so the FX_SnowSpray anchor sits <= 0.012 while the trunk tip only grazes the snow
    (0, 0, 0, (0, 0, 0, 0), 0, 0),
    (10, 8, 2, (4, 2, 4, 20), 4, 0),                 # the head dips, the trunk swings back toward the forefeet
    (18, 14.5, 3, (0, 0, 4, 40), 6, 0),                # SCOOP 1: the tip turns down into the snow (scoop1) - hold
    (20, 14.5, 3, (0, 0, 4, 40), 6, 0),
    (22, 14.5, 3, (0, 0, 4, 40), 6, 0),
    (24, 11, 3, (-4, -2, 4, 44), 6, 0),              # the scoop rolls through the snow
    (32, -4, 0, (-26, -18, -4, 18), 8, 0),           # lift, the tip still curled in
    (44, -14, -2, (-55, -40, -26, -8), 12, 0),       # cocked hold in front of the face (the tell); r3: root 5 deg higher
    (48, -15, -2, (-57, -42, -28, -10), 12, 0),
    (52, -15, -2, (-65, -52, -36, -20), 14, 0),      # in-between of the snap
    (56, -15, -2, (-70, -60, -40, -26), 16, 0),      # FLICK over the brow: dust1 (crest 5 deg higher, r3)
    (58, -14, -2, (-68, -58, -40, -24), 14, 0),      # follow-through drift
    (61, 0, 0, (-34, -28, -15, 2), 10, 0),
    (63, 9, 2, (-12, -9, -2, 30), 9, 0),            # the tip curls in BEFORE it reaches the snow (no dig-in)
    (64, 13.5, 3, (0, 0, 4, 38), 8, 0),                # SCOOP 2 (scoop2) - hold
    (66, 13.5, 3, (0, 0, 4, 38), 8, 0),
    (68, 13.5, 3, (0, 0, 4, 38), 8, 0),
    (70, 2, 1, (-18, -14, -6, 14), 9, 0),
    (74, -7, -1, (-29, -24, -14, -3), 11, 0),        # flick 2 (smaller): dust2 (smaller than r4: max swing <= 60)
    (76, 3, 1, (-12, -9, -3, 24), 9, 0),            # the tip curls in before it reaches the snow
    (78, 13.5, 3, (0, 0, 4, 38), 8, 0),                # SCOOP 3 (scoop3) - hold
    (80, 13.5, 3, (0, 0, 4, 38), 8, 0),
    (82, 13.5, 3, (0, 0, 4, 38), 8, 0),
    (84, 2, 0, (-12, -10, -4, 6), 8, 0),
    (86, -6, -1, (-30, -25, -13, -5), 9, 0),         # flick 3 (smallest): dust3
    (92, -2, 0, (-12, -8, -6, -4), 6, 0),
    (95, 0, 0, (-2, -1, 0, 0), 14, 22),              # one tail flick
    (98, 0, 0, (0, 0, 0, 0), 4, -6),
    (100, 0, 0, (0, 0, 0, 0), 0, 0)]


def dustover(k):
    """SIGNATURE - DUST OVER THE BACK: the trunk scoops snow at the forefeet, lifts it in front of the face, holds a
    beat, then flicks it back over the brow onto the hump (dust1); two smaller scoops and flicks (dust2, dust3);
    the trunk returns, one tail flick, exact rest. Legs planted, no shake, no spin."""
    n = 100
    k.new_action("act_dustover", n, False)
    for f, hd, nk, tp, tlp, tlr in DUST_P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Chest", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0), loc=neck_lift(hd + nk))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(2 if hd < -8 else 0, 0, 0))
        trunk(k, f, tp)
        tail(k, f, tlp, tlr, lag=(1.0, 0.9, 0.8))
        ears(k, f, 6 if hd < -8 else 0)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)
    k.events["act_dustover"] = {"scoop1": round(20 / n, 3), "dust1": round(56 / n, 3), "scoop2": round(66 / n, 3),
                                "dust2": round(74 / n, 3), "scoop3": round(80 / n, 3), "dust3": round(86 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    dustover(k)
    return stride


HEAD_XF = []
