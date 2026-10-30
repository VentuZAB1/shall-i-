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

CHAR_TEAL = (112, 152, 162)  # body, legs, trunk, head (studded)
WOOL_D = (64, 84, 96)        # wool mane: head dome, hump, back, chest bib, tail tuft, brows
BELLY_PALE = (206, 214, 216)  # belly strip, inside of the trunk, chin
TUSK_ICE = (238, 246, 250)   # tusks (smooth)
MINT = (150, 236, 210)       # THE accent: tusk crack lines, eye slits
DARK = (52, 62, 68)          # tusk sockets, trunk tip, toenails, foot soles
BLACK = (14, 14, 22)         # eye sockets / slit pupils
MOUTH = (86, 18, 30)

H_MODEL = 1.83               # model height in Blender units (same units-per-stud as the Raiju: 1.498 / 8)
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)   # same world stud size as the Raiju
PROTO = os.environ.get("MAMMOTH_PROTO") == "1"                   # build gate: head + trunk + tusks only

# trunk chain (root buried in the face -> tip curling forward), bones Trunk1..Trunk4
TRUNK = [(0, -1.205, 1.07), (0, -1.255, 0.86), (0, -1.28, 0.665), (0, -1.275, 0.49), (0, -1.33, 0.355)]
TRUNK_TIP = (0, -1.43, 0.37)
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
JAW_P = Vector((0, -1.08, 0.98))
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
        sx, sy = w1[0] / w0[0] * 0.90, w1[1] / w0[1] * 0.90
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
    B.add((0, -1.02, 1.30), (0.215, 0.20, 0.26), CHAR_TEAL, "Head", top=(0.74, 0.70), bot=(0.88, 0.86), rnd=0.42)
    B.seg((0, -1.03, 1.52), (0, -1.205, 1.10), 0.175, 0.10, CHAR_TEAL, "Head", top=(0.82, 0.9), ext=0.03, rnd=0.40)
    for s in (1, -1):                                                         # cheeks over the tusk roots
        B.add((s * 0.14, -1.09, 1.10), (0.085, 0.13, 0.13), CHAR_TEAL, "Head", rot=(12, 0, 0), top=(0.85, 0.8),
              rnd=0.42)
    # wool dome (mane) over the crown, rising to the top of the pet
    B.add((0, -0.98, 1.585), (0.17, 0.19, 0.10), WOOL_D, "Head", top=(0.55, 0.55), rnd=0.45)
    for x, y, z, dz, L in ((0.0, -1.10, 1.58, 0.2, 0.15), (0.09, -1.06, 1.57, 0.3, 0.13), (-0.09, -1.06, 1.57, 0.3, 0.13),
                           (0.0, -0.90, 1.62, 0.8, 0.14)):
        B.spike((x, y, z), (x * 2.5, -0.9 + dz, 1.0), L, 0.07, WOOL_D, "Head", top=(0.2, 0.4), studs=None,
                role="limb")
    # heavy dark brow shelf (a V, inner ends low) over small deep-set slanted mint eyes with a black slit pupil
    for s in (1, -1):
        B.add((s * 0.098, -1.198, 1.418), (0.108, 0.042, 0.036), WOOL_D, "Head", rot=(-14, -s * 22, 0),
              role="detail", bevel=0.012)
        rot = (0, -s * 17, s * 14)
        B.add((s * 0.128, -1.186, 1.352), (0.068, 0.012, 0.027), DARK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.005)
        B.add((s * 0.130, -1.195, 1.352), (0.058, 0.008, 0.015), MINT, "Head", rot=rot, studs=[], role="detail",
              bevel=0.004)
        B.add((s * 0.138, -1.199, 1.354), (0.010, 0.004, 0.014), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.002)
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
    # ================= TUSKS: dark socket, a smooth curved ice tube (socket -> down-out -> forward -> up-in tip),
    # 2 mint crack lines across the outer third
    for s in (1, -1):
        P = tusk_pts(s)
        d0 = (P[1] - P[0]).normalized()
        B.seg(P[0] - d0 * 0.05, P[0] + d0 * 0.055, 0.092, 0.092, CHAR_TEAL, "Head", top=(0.95, 0.95), rnd=0.42)
        B.seg(P[0] + d0 * 0.05, P[0] + d0 * 0.085, 0.086, 0.086, DARK, "Head", rnd=0.35, role="limb", nostud=True)
        C, R = tusk_curve(s)
        B.tube(tube_rings(C, R, 10), TUSK_ICE, "Head", nostud=True)
        for t in (0.62, 0.78):
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
                B.bar(u, v, ((u + v) / 2 - c).normalized(), 0.022, 0.007, MINT, "Head", studs=[], bevel=0.003)
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
    Lb.band(B, sy(-0.60), sj, BELLY_PALE, "Chest", zlo=-1.0, zhi=-0.70, grow=0.008, step=0.08)       # pale belly
    Lb.band(B, sj, sy(0.62), BELLY_PALE, "Spine", zlo=-1.0, zhi=-0.70, grow=0.008, step=0.08)
    # dark wool mane over the back (hump -> mid back), a dome over the shoulders
    Lb.band(B, sy(-0.84), sj, WOOL_D, "Chest", zlo=0.42, grow=0.026, inset=0.02, step=0.08)
    Lb.band(B, sj, sy(0.40), WOOL_D, "Spine", zlo=0.52, grow=0.022, inset=0.02, step=0.08, narrow1=0.55)
    # mane ridge tufts laid back along the spine (the shaggy hump silhouette)
    for y, L, ang, bn in ((-0.74, 0.15, 56, "Chest"), (-0.60, 0.17, 60, "Chest"), (-0.44, 0.18, 63, "Chest"),
                          (-0.28, 0.17, 66, "Chest"), (-0.12, 0.15, 68, "Chest"), (0.06, 0.14, 70, "Spine"),
                          (0.22, 0.12, 72, "Spine")):
        c = Lb.at(sy(y))
        top = c[0] + Vector((0, 0, c[4] + 0.01))
        if bn == "Chest" and -0.62 < y < -0.40:
            top.z = max(top.z, 1.60)
        d = (0, math.sin(math.radians(ang)), math.cos(math.radians(ang)))
        B.spike(top - Vector((0, 0, 0.05)), d, L + 0.05, 0.085, WOOL_D, bn, top=(0.25, 0.35), studs=None,
                role="limb")
    # ================= WOOL LOCKS: 3 shingled rows down each flank (top row dark), pointed hanging blocks
    ROWS = ((0.40, 0.25, WOOL_D, 0.0), (0.02, 0.29, CHAR_TEAL, 0.5), (-0.38, 0.30, CHAR_TEAL, 0.0))
    for f, L, col, off in ROWS:
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
                ln = L * (1.0 + 0.16 * r)
                lock(B, p, nrm, ln, 0.098, 0.036, col, bn, flare=0.16 + 0.06 * r, sway=0.025 * r)
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


HEAD_XF = []
