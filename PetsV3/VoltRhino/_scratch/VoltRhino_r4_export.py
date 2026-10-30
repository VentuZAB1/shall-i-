# Volt Rhino (Thunder / Storm egg, HIGH 6 %) - FIERCE style (2026-10-27, Glacier update, plan _review/VoltRhino_plan.md
# v2): an armoured Indian-style rhino under a Roblox stud skin. A smooth lofted barrel body (curveloft) whose belly line
# rises from the brisket to the flank, a dark iron shoulder shield, saddle and rump plate laid over it as raised shells
# with heavy fold rims crossing the flanks, a withers hump, lighter iron flanks and pillar legs, a pale belly strip.
# The lofted head is held low with a dark nasal ridge, a small ivory brow nub and ONE huge ivory horn sweeping
# forward-up with a volt-lime lightning inlay down both sides (the hero piece). Narrow lime slit eyes under heavy dark
# brows, cupped tube ears, dark foot pads with 3 black toenails, a short tail with a dark tuft. No glow (sparks = VFX).
import math
from mathutils import Vector, Matrix

DISPLAY = "Volt Rhino"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.5                 # total height (withers hump top) in studs at x1

IRON_D = (92, 100, 116)      # back, shoulder shield, saddle, rump plate, folds, brows, nasal ridge, feet
IRON = (156, 164, 178)       # flanks, legs, head (studded)
PALE = (222, 224, 228)       # belly strip (follows the slope), chin
HORN_IVORY = (232, 224, 204)  # main horn + brow nub (smooth, warm ivory)
HORN_SHADE = (205, 198, 180)  # horn collars + growth rings
VOLT = (190, 255, 64)        # THE accent: horn lightning, shoulder bolts, eye slits
EYE_HOT = (238, 255, 168)    # small hot centre of the eye slit
BLACK = (14, 14, 22)         # toenails, nostrils, eye sockets
MOUTH = (86, 18, 30)
JAW_MAX = 14.0               # largest jaw opening the mouth interior covers (no see-through); clips never key past it

H_MODEL = 1.57               # model height in Blender units (same units-per-stud as the Raiju: 1.498 / 8)
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)   # same world stud size as the Raiju

# leg joints (left side): shoulder/hip, elbow/stifle, carpus/hock, foot centre
LEGS = {"F": ((0.25, -0.56, 0.98), (0.25, -0.47, 0.58), (0.25, -0.53, 0.22), (0.25, -0.55, 0.07)),
        "B": ((0.20, 0.60, 1.00), (0.20, 0.46, 0.63), (0.20, 0.66, 0.30), (0.20, 0.61, 0.07))}
TAILP = [(0, 0.93, 1.20), (0, 1.01, 1.08), (0, 1.04, 0.96), (0, 1.05, 0.84)]
# body loft stations (y, zc, half width, half height), front -> back; the belly line rises 0.62 -> 0.77
BODY = [(-0.94, 1.08, 0.24, 0.31), (-0.86, 1.07, 0.31, 0.40), (-0.62, 1.08, 0.385, 0.46), (-0.30, 1.07, 0.39, 0.43),
        (0.02, 1.09, 0.37, 0.39), (0.34, 1.10, 0.345, 0.345), (0.62, 1.08, 0.325, 0.32), (0.84, 1.04, 0.27, 0.27),
        (0.96, 1.01, 0.15, 0.16)]
NECK = [(-0.70, 1.10, 0.27, 0.32), (-0.88, 1.07, 0.26, 0.29), (-1.06, 1.03, 0.225, 0.255)]
# head loft (upper head above the mouth line), front -> back: lip, nose, muzzle, eyes, cheeks, poll
HEAD = [(-1.71, 0.825, 0.150, 0.095), (-1.63, 0.84, 0.185, 0.14), (-1.45, 0.885, 0.20, 0.185),
        (-1.26, 0.965, 0.24, 0.24), (-1.07, 1.035, 0.265, 0.285), (-0.975, 1.06, 0.225, 0.25)]
SPLIT_Y = -0.06              # Chest | Spine split of the body loft
THROAT = Vector((0, -0.93, 0.86))
JAW_P = Vector((0, -1.02, 0.79))

_L = {}


def loft(name):
    if name not in _L:
        import curveloft as cl
        _L[name] = cl.Loft({"body": BODY, "neck": NECK, "head": HEAD}[name], n=2.5, seg=24)
    return _L[name]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def surf(L, y, a, grow=0.0):
    """point on loft L at y, section angle a (0 = +x side, pi/2 = top) + its outward normal"""
    s = L.s_at_y(y)
    p = L.surf(s, a, grow=grow)
    t1 = L.surf(s, a + 0.03, grow=grow) - L.surf(s, a - 0.03, grow=grow)
    t2 = L.surf(min(L.length, s + 0.01), a, grow=grow) - L.surf(max(0.0, s - 0.01), a, grow=grow)
    n = t1.cross(t2).normalized()
    c = L.at(s)[0]
    if n.dot(p - c) < 0:
        n = -n
    return p, n


def zig(B, Q, color, bone, w, thick=0.012, tip=True):
    """flat bars through [(point, normal)], the last one pointed (lightning)"""
    for i, ((a, n), (c, n2)) in enumerate(zip(Q, Q[1:])):
        d = (c - a).normalized()
        a2 = a - d * (w * 0.35 if i else 0.0)
        B.bar(a2, c, (n + n2).normalized(), w, thick, color, bone, studs=[], bevel=0.004,
              top=(1, 0.15) if (tip and i == len(Q) - 2) else (1, 1))


# armour plates (y0, y1, bone, lower-edge height fraction front, rear, grow): sloped bottoms (review 1 M3)
ARMOUR = [(-0.90, -0.08, "Chest", -0.26, -0.12, 0.034),     # shoulder shield (proud, overlaps the saddle)
          (-0.14, 0.40, "Spine", 0.34, 0.06, 0.020),        # saddle (rear edge runs down the flank, review 2 M4)
          (0.36, 0.93, "Spine", -0.30, 0.06, 0.032)]        # rump plate (rear edge tapered, review 2 NICE)


def arc_half(L, f):
    """half-angle (from the top) of a top band whose lower edge sits at height fraction f"""
    return math.pi / 2 - L.zang(f)


def armour_grow(L, y, a):
    """outer offset of the armour covering body point (y, section angle a on the +x side), 0 on bare hide"""
    g = 0.0
    for y0, y1, bn, f0, f1, gr in ARMOUR:
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0)
            half = arc_half(L, f0) * (1 + (arc_half(L, f1) / arc_half(L, f0) - 1) * t)
            if abs(a - math.pi / 2) <= half:
                g = max(g, gr)
    return g


def fold_wedge(B, L, y, s, bone, f_end=-0.50, w=0.07, thick=0.030, n=6):
    """tapered skin-fold wedge from the spine down the flank to a point at height fraction f_end"""
    a0, a1 = math.pi / 2, L.zang(f_end)
    pts = []
    for i in range(n + 1):
        t = i / n
        a = a0 + (a1 - a0) * t
        th = thick * (1 - 0.75 * t)
        aa = a if s > 0 else math.pi - a
        p, nrm = surf(L, y, aa, grow=armour_grow(L, y, a) + th / 2)
        pts.append((p, nrm, w * (1 - 0.85 * t), th))
    for (p, nrm, wa, ta), (q, nq, wb, tb) in zip(pts, pts[1:]):
        B.seg(p, q, wa / 2, ta / 2, IRON_D, bone, side=(0, 1, 0), top=(wb / wa, tb / ta), ext=0.008, ext1=0.008,
              rnd=0.30, role="limb")


def horn_pts():
    """horn centreline (world): base buried in the nose top -> forward-up, curving upward"""
    b0 = Vector((0, -1.52, 0.99))
    h1 = b0 + Vector((0, -0.766, 0.643)) * 0.28
    h2 = h1 + Vector((0, -0.643, 0.766)) * 0.25
    tip = h2 + Vector((0, -0.500, 0.866)) * 0.24
    return b0, h1, h2, tip


def _cr(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def horn_curve(n=18):
    """smooth horn centreline through horn_pts (Catmull-Rom), per-sample side axis A (x), fore-aft axis D, half
    width W (along A) and half depth H; the base starts buried in the nose"""
    P = list(horn_pts())
    P[0] = P[0] - (P[1] - P[0]).normalized() * 0.05
    E = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    seg = len(P) - 1
    C = []
    for i in range(n + 1):
        u = i / n * seg
        j = min(int(u), seg - 1)
        C.append(_cr(E[j], E[j + 1], E[j + 2], E[j + 3], u - j))
    A, D, W, H = [], [], [], []
    for i, c in enumerate(C):
        d = (C[min(i + 1, n)] - C[max(i - 1, 0)]).normalized()
        ax = Vector((1, 0, 0))
        ax = (ax - d * ax.dot(d)).normalized()
        A.append(ax)
        D.append(d.cross(ax).normalized())
        t = i / n
        W.append(0.112 * (1 - t ** 1.35) + 0.005)
        H.append(0.120 * (1 - t ** 1.35) + 0.005)
    return C, A, D, W, H


def horn_rings(C, A, D, W, H, m=16, n_se=3.0):
    """superellipse rings (flat-ish sides for the lightning inlay) around the horn centreline"""
    rings = []
    for c, ax, dv, w, h in zip(C, A, D, W, H):
        r = []
        for j in range(m):
            a = 2 * math.pi * j / m
            cx, sz = math.cos(a), math.sin(a)
            r.append(c + ax * (w * math.copysign(abs(cx) ** (2 / n_se), cx)) +
                     dv * (h * math.copysign(abs(sz) ** (2 / n_se), sz)))
        rings.append(r)
    return rings


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=63, tier=3, plates=False, th=0.86)
    Lb, Ln, Lh = loft("body"), loft("neck"), loft("head")
    sy = Lb.s_at_y
    # ---------------- body: one lofted barrel split Chest | Spine (flush overlapping joint)
    sj = sy(SPLIT_Y)
    Lb.tube(B, 0.0, sj + 0.06, IRON, "Chest", j1=sj, step=0.11)
    Lb.tube(B, sj - 0.06, Lb.length, IRON, "Spine", j0=sj, step=0.11)
    # pale belly strip along the rising underside
    Lb.band(B, sy(-0.80), sy(-0.56), PALE, "Chest", zlo=-1.0, zhi=-0.92, zhi1=-0.24, grow=0.008, step=0.04)
    Lb.band(B, sy(-0.56), sj, PALE, "Chest", zlo=-1.0, zhi=-0.24, grow=0.008, step=0.06)
    Lb.band(B, sj, sy(0.56), PALE, "Spine", zlo=-1.0, zhi=-0.24, grow=0.008, step=0.06)
    Lb.band(B, sy(0.56), sy(0.82), PALE, "Spine", zlo=-1.0, zhi=-0.24, zhi1=-0.92, grow=0.008, step=0.04)
    # ---------------- iron armour: shoulder shield (proud, overlaps the saddle), saddle, rump plate
    # (review 1 M3: every lower edge slopes - narrow1 sweeps the band edge between its front and rear height)
    for y0, y1, bn, f0, f1, g in ARMOUR:
        Lb.band(B, sy(y0), sy(y1), IRON_D, bn, zlo=f0, grow=g, inset=0.02, step=0.06,
                narrow1=arc_half(Lb, f1) / arc_half(Lb, f0))
    # fold wedges (review 1 M2): from the spine down the flank to a point at the belly line, proud 0.030 -> 0
    for y, bn in ((-0.065, "Chest"), (0.405, "Spine")):
        for s in (1, -1):
            fold_wedge(B, Lb, y, s, bn)
    # volt shoulder bolts on the shield (one per side)
    for s in (1, -1):
        Q = []
        for y, a in ((-0.70, 0.62), (-0.52, 0.42), (-0.60, 0.30), (-0.38, 0.08)):
            p, n = surf(Lb, y, a if s > 0 else math.pi - a, grow=0.038)
            Q.append((p, n))
        zig(B, Q, VOLT, "Chest", 0.072)
    # volt rump bolts on the rump plate (review 1 M7)
    for s in (1, -1):
        Q = []
        for y, a in ((0.50, 0.62), (0.63, 0.42), (0.57, 0.31), (0.74, 0.12)):
            Q.append(surf(Lb, y, a if s > 0 else math.pi - a, grow=armour_grow(Lb, y, a) + 0.004))
        zig(B, Q, VOLT, "Spine", 0.068)
    # ---------------- neck: short, thick, a dark fold across the nape
    Ln.tube(B, 0.0, Ln.length, IRON, "Neck", step=0.06)
    Ln.band(B, 0.0, Ln.length, PALE, "Neck", zlo=-1.0, zhi=-0.55, grow=0.008, step=0.05)          # pale throat
    Ln.band(B, Ln.s_at_y(-0.92), Ln.s_at_y(-1.00), IRON_D, "Neck", zlo=-0.30, grow=0.03, inset=0.02, step=0.04)
    # ---------------- head (pivot at the throat): lofted upper head, dark nasal ridge, jaw, chin
    Lh.tube(B, 0.0, Lh.length, IRON, "Head", step=0.08)
    Lh.band(B, Lh.s_at_y(-1.56), Lh.s_at_y(-1.10), IRON_D, "Head", zlo=0.62, grow=0.012, inset=0.02, step=0.04)
    B.seg((0, -1.00, 0.80), (0, -1.65, 0.738), 0.14, 0.055, PALE, "Jaw", top=(0.78, 0.62), ext=0.0, rnd=0.45)   # tapers to the chin
    B.seg((0, -1.40, 0.765), (0, -1.66, 0.755), 0.142, 0.006, MOUTH, "Head", studs=[], role="detail", bevel=0.003)
    # mouth interior riding the jaw, hidden inside the snout when closed: an open jaw (<= JAW_MAX) shows dark mouth,
    # never the background (clip review 3 MUST 3d)
    B.seg((0, -1.08, 0.84), (0, -1.60, 0.80), 0.10, 0.05, MOUTH, "Jaw", studs=[], role="detail", bevel=0.014,
          top=(0.70, 0.75))                                                                    # tapers inward
    Lh.band(B, Lh.s_at_y(-1.71), Lh.s_at_y(-1.52), IRON_D, "Head", zlo=0.40, grow=0.018, inset=0.02, step=0.04)
    for s in (1, -1):                                                                       # nostril slits (side)
        p, n = surf(Lh, -1.645, math.radians(18 if s > 0 else 162), grow=0.002)
        B.add(p, (0.005, 0.012, 0.034), BLACK, "Head", R=bk.frame_from(p, p + Vector((0, 0.55, 1.0)), n),
              studs=[], role="detail", bevel=0.003)
    # ---------------- eyes: narrow lime slits on the side-front, inner (front) end low, under heavy dark brows
    for s in (1, -1):
        p, n = surf(Lh, -1.27, math.radians(30 if s > 0 else 150), grow=0.0)
        n = (n + Vector((0, -0.85, 0))).normalized()                    # turn the eye toward the front
        back = Vector((0, 1, 0))
        up = n.cross(back).normalized() * s * -1
        if up.z < 0:
            up = -up
        d = (back * math.cos(math.radians(22)) + up * math.sin(math.radians(22))).normalized()
        for col, half, out in ((BLACK, (0.010, 0.034, 0.094), 0.004), (VOLT, (0.008, 0.018, 0.080), 0.010),
                               (EYE_HOT, (0.004, 0.007, 0.026), 0.014)):
            c = p + n * out + (d * 0.022 if col is EYE_HOT else Vector())
            B.add(c, half, col, "Head", R=bk.frame_from(c, c + d, n), studs=[], role="detail", bevel=0.003)
        bc = p + up * 0.066 + n * 0.006 + d * 0.004                       # sunk 0.010 (review 2 M2)
        bd = (back * math.cos(math.radians(26)) + up * math.sin(math.radians(26))).normalized()
        B.add(bc, (0.040, 0.026, 0.096), IRON_D, "Head", R=bk.frame_from(bc, bc + bd, n), role="detail",
              bevel=0.012)                                                                    # heavy brow
    # ---------------- small dark ear flaps at the poll (review 1 M5), black inner
    for s, side in ((1, "L"), (-1, "R")):
        root = Vector((s * 0.14, -0.98, 1.18))
        d = Vector((s * 0.40, 0.35, 1.0))
        B.spike(root, d, 0.20, 0.064, IRON_D, "Ear_" + side, top=(0.55, 0.40), studs=None, role="limb")
        B.spike(root + d.normalized() * 0.09 + Vector((0, -0.035, 0)), d, 0.10, 0.034, BLACK, "Ear_" + side,
                top=(0.65, 0.3), nostud=True)
    # ---------------- the HORN (hero): 3 tapered ivory segments + a volt lightning inlay on both sides; brow nub
    C, A, D, W, H = horn_curve()
    B.tube(horn_rings(C, A, D, W, H), HORN_IVORY, "Head", nostud=True)
    # horn root collar (review 1 M6) + 2 thin growth rings on the upper horn (NICE)
    for t0, t1, g in ((0.05, 0.13, 0.014), (0.47, 0.51, 0.0015), (0.66, 0.70, 0.0015)):   # rings flush (review 2 M1)
        i0, i1 = int(t0 * (len(C) - 1)), int(math.ceil(t1 * (len(C) - 1)))
        B.tube(horn_rings(C[i0:i1 + 1], A[i0:i1 + 1], D[i0:i1 + 1], [w + g for w in W[i0:i1 + 1]],
                          [h + g for h in H[i0:i1 + 1]]), HORN_SHADE, "Head", nostud=True)
    # lightning down each flat-ish side of the horn (3 zigzag segments + a point)
    for s in (1, -1):
        Q = []
        for t, dz in ((0.16, 0.045), (0.33, -0.040), (0.52, 0.030), (0.68, -0.020), (0.80, 0.006)):
            i = t * (len(C) - 1)
            j = min(int(i), len(C) - 2)
            u = i - j
            c = C[j].lerp(C[j + 1], u)
            ax = A[j].lerp(A[j + 1], u).normalized()
            dv = D[j].lerp(D[j + 1], u).normalized()
            hw = W[j] + (W[j + 1] - W[j]) * u
            hd = H[j] + (H[j + 1] - H[j]) * u
            Q.append((c + ax * s * (hw - 0.007) + dv * dz, ax * s, min(0.060, 1.15 * hd)))   # sunk (r2 NICE)
        for i_, ((a_, na), (c_, nc)) in enumerate(zip([(q[0], q[1]) for q in Q], [(q[0], q[1]) for q in Q[1:]])):
            d_ = (c_ - a_).normalized()
            w_ = min(Q[i_][2], Q[i_ + 1][2])
            B.bar(a_ - d_ * (w_ * 0.35 if i_ else 0.0), c_, (na + nc).normalized(), w_, 0.013, VOLT, "Head",
                  studs=[], bevel=0.004, top=(1, 0.15) if i_ == len(Q) - 2 else (1, 1))
    i0, i1 = int(0.84 * (len(C) - 1)), int(math.ceil(0.90 * (len(C) - 1)))     # lime tip band (game camera)
    B.tube(horn_rings(C[i0:i1 + 1], A[i0:i1 + 1], D[i0:i1 + 1], [w + 0.004 for w in W[i0:i1 + 1]],
                      [h + 0.004 for h in H[i0:i1 + 1]]), VOLT, "Head", nostud=True)
    B.spike((0, -1.22, 1.11), (0, -0.40, 1.0), 0.21, 0.050, HORN_IVORY, "Head", top=(0.12, 0.12), nostud=True)
    # ---------------- legs: pillar legs, dark foot pads with 3 black toenails
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.10)), K, 0.17, 0.20, IRON, leg, ext=0.0, ext1=0.04, top=(0.86, 0.78))
                B.seg(K, A, 0.14, 0.145, IRON, shin, top=(0.86, 0.86), ext=0.04, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.03, 0.10)), K, 0.15, 0.22, IRON, leg, bot=(0.85, 1), top=(0.78, 0.66),
                      ext=0.0, ext1=0.04)                                                      # thigh
                B.seg(K, A, 0.125, 0.13, IRON, shin, top=(0.90, 0.90), ext=0.04, ext1=0.02)
                B.seg(A, P + Vector((0, 0.0, 0.06)), 0.115, 0.115, IRON, foot, ext=0.03, top=(0.95, 0.95))  # hock
            dk = (A - K).normalized()          # ONE elbow / knee fold: a tapered wedge on the outer face (r2 M3)
            ox = s * (0.138 if fb == "F" else 0.122)
            c0 = K + dk * 0.035 + Vector((ox, -0.125, 0.03))
            c1 = K + dk * 0.075 + Vector((ox, 0.125, -0.03))
            B.seg(c0, c1, 0.013, 0.032, IRON_D, shin, side=(1, 0, 0), top=(1.0, 0.15), studs=[], rnd=0.40,
                  role="limb", bevel=0.006)
            B.add(P + Vector((0, 0.0, 0.015)), (0.160, 0.165, 0.075), IRON_D, foot, top=(0.84, 0.82), rnd=0.40)
            for gx in (-0.092, 0.0, 0.092):
                B.add((P.x + gx, P.y - 0.150, 0.040), (0.038, 0.030, 0.040), BLACK, foot, top=(0.80, 0.55),
                      top_shift=(0, 0.01), role="limb", nostud=True)
    # ---------------- short tail with a dark tuft
    T = [Vector(p) for p in TAILP]
    for (a, b), w, bn in zip(zip(T, T[1:]), (0.055, 0.047, 0.040), ("Tail1", "Tail2", "Tail3")):
        B.seg(a, b, w, w, IRON, bn, ext=0.04, top=(0.85, 0.85))
    tp = T[3]
    for dx, dy, L in ((0, 0.0, 0.19), (0.55, 0.25, 0.15), (-0.55, 0.25, 0.15), (0, 0.6, 0.13)):
        B.spike(tp + Vector((0, 0, 0.04)), (dx, dy, -1), L, 0.055, IRON_D, "Tail3", top=(0.2, 0.3))
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.30, 1.04), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, SPLIT_Y, 1.04), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.72, 1.06), "Chest", tail=(0, -0.2, -0.04))
    k.joint("Head", tuple(THROAT), "Neck", tail=(0, -0.35, 0.0))               # throat pivot (low/back)
    k.joint("Jaw", tuple(JAW_P), "Head", tail=(0, -0.3, -0.04))
    k.joint("Mouth", (0, -1.66, 0.76), "Head", tail=(0, -0.1, 0))
    b0, h1, h2, tip = horn_pts()
    k.joint("Horn_Base", tuple(b0), "Head", tail=tuple((h1 - b0) * 0.6))
    k.joint("Horn_Tip", tuple(tip), "Horn_Base", tail=(0, -0.05, 0.08))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.14, -0.98, 1.24), "Head", tail=(s * 0.06, 0.05, 0.15))
        k.joint("Shoulder_" + side, (s * 0.40, -0.52, 1.22), "Chest", tail=(s * 0.1, 0, 0))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2", tail=(0, 0.01, -0.2))
    # VFX anchors (plan section 8): bones without mesh, parented to the bone that carries the effect
    k.joint("FX_BoltTrail", tuple(tip + Vector((0, -0.02, 0.02))), "Horn_Tip", tail=(0, -0.06, 0.06))
    k.joint("FX_ChargeGlow", tuple(b0 + Vector((0, -0.04, 0.06))), "Horn_Base", tail=(0, 0, 0.1))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("FX_BoltSpark_" + side, (s * 0.44, -0.52, 1.24), "Shoulder_" + side, tail=(s * 0.08, 0, 0))
    k.joint("FX_DustTap", (0.25, -0.55, 0.02), "Foot_FL", tail=(0, -0.1, 0))
    k.joint("FX_BellowRing", (0, -1.74, 0.78), "Mouth", tail=(0, -0.1, 0))


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Head", "Chest"), ("Jaw", "Chest"), ("Ear_L", "Ear_R"),
         ("Head", "Leg_FL"), ("Head", "Leg_FR"), ("Head", "Shin_FL"), ("Head", "Shin_FR"), ("Jaw", "Shin_FL"),
         ("Jaw", "Shin_FR"), ("Head", "Foot_FL"), ("Head", "Foot_FR"), ("Jaw", "Neck"),
         ("Tail2", "Shin_BL"), ("Tail2", "Shin_BR"), ("Tail3", "Shin_BL"), ("Tail3", "Shin_BR"),
         ("Tail3", "Foot_BL"), ("Tail3", "Foot_BR"), ("Tail2", "Leg_BL"), ("Tail2", "Leg_BR")]
    return P


def joints():
    return [(tuple(THROAT), (0, -1.02, 1.0), 0.26, "Head")]


# ------------------------------------------------------------------ animation (plan section 7 + ANIM_REFS.md)
import petkit as pk
import _common as cm
import bpy

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]


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


def ears(k, f, l=0.0, r=None, fwd=0.0):
    """roll the upright ears: + tips them outward; fwd + tips them forward"""
    r = l if r is None else r
    k.key("Ear_L", f, rot=(fwd, 0, l))
    k.key("Ear_R", f, rot=(fwd, 0, -r))


def tail(k, f, pitch=0.0, roll=0.0, lag=(1.0, 0.8, 0.6)):
    """pitch + lifts the hanging tail backward, roll swings it sideways"""
    for b, g in zip(TAIL, lag):
        k.key(b, f, rot=(pitch * g, 0, roll * g))


def neck_lift(up):
    """neck offset that goes with a head+neck pitch-up of `up` deg: the neck reaches forward and a little up so the
    back of the skull clears the shoulder shield"""
    u = max(0.0, up) / 16.0
    return (0, -0.07 * u, 0.025 * u)


def plant(k, f, moves=None):
    """IK every foot on its rest spot; moves = {leg: T} overrides (a lifted foot)"""
    bpy.context.scene.frame_set(f)
    for leg in LEGS4:
        T = moves[leg] if moves and leg in moves else Vector((k.J[leg].x, k.J[leg].y, 0.0))
        k.solve_leg(leg, f, T)


def idle(k):
    """HORN TILT: slow weight shift, the head yaws +-6 deg so the horn tilts side to side, the left foreleg lifts 0.03
    and stamps down (f46), ear twitches, one tail flick (f90). Legs planted otherwise."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        br = 0.5 + 0.5 * pk.wave(f, n, 0.25, 3)
        sw = pk.wave(f, n, 0.0, 1)                                  # weight shift (one cycle)
        k.key("Spine", f, rot=(0, 0, 1.2 * sw), loc=(0.010 * sw, 0, -0.004 * br))
        k.key("Chest", f, rot=(0.4 * br, 0, -0.6 * sw))
        k.key("Neck", f, rot=(0.5 * br, 2.0 * pk.wave(f, n, 0.1, 1), 0))
        k.key("Head", f, rot=(0.6 * pk.wave(f, n, 0.3, 2), 4.0 * pk.wave(f, n, 0.15, 1), 0))
        k.key("Jaw", f, rot=(1.0 + 1.0 * br, 0, 0))
    for f, l, r in ((0, 0, 0), (16, 0, 0), (18, 14, 0), (21, 0, 0), (60, 0, 0), (62, 0, 12), (65, 0, 0),
                    (104, 0, 0), (106, 10, 10), (109, 0, 0), (120, 0, 0)):
        ears(k, f, l, r)
    for f, p, r in ((0, 4, 0), (82, 4, 0), (86, 12, 14), (89, 22, 28), (92, 26, 34), (96, 15, 18), (101, 7, 5),
                    (107, 4, 0), (120, 4, 0)):
        tail(k, f, p, r)
    k.bake_bezier_now()
    J = k.J
    for f in range(0, n + 1):
        mv = None
        if 30 <= f <= 46:                                           # the foreleg lift + stamp
            u = (f - 30) / 16
            mv = {"Leg_FL": Vector((J["Leg_FL"].x, J["Leg_FL"].y - 0.015 * math.sin(math.pi * u),
                                    0.032 * math.sin(math.pi * u) ** 0.8))}
        plant(k, f, mv)
    k.finish()
    k.meta["planted"] = ["Leg_FR", "Leg_BL", "Leg_BR"]
    k.events["idle"] = {"stamp": round(46 / n, 3), "flick": round(90 / n, 3)}


def walk(k):
    """HEAVY LATERAL-SEQUENCE WALK (Muybridge walking bison + plate 733): hind then fore on the same side, the head
    carried low and dipping on each front contact, the body sinks 0.02H per step and rolls, the tail lags."""
    n = 40

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.5 * pk.wave(f, n, 0.1, 2), 1.2 * pk.wave(f, n, 0.0), -2.0 * pk.wave(f, n, 0.25)),
              loc=(0, 0, -0.022 - 0.014 * b))              # rolls toward the planted side (left legs swing ~f35-f5)
        k.key("Chest", f, rot=(0.8, -1.5 * pk.wave(f, n, 0.25), -1.2 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(1.5 + 1.0 * pk.wave(f, n, 0.12, 2), 0, 0))
        k.key("Head", f, rot=(1.5 * pk.wave(f, n, 0.65, 2), 1.5 * pk.wave(f, n, 0.3), 0))   # dips 2 f after FL/FR touch
        k.key("Jaw", f, rot=(1.5, 0, 0))
        tail(k, f, 6, 8 * pk.wave(f, n, 0.3))
        ears(k, f, 3 * pk.wave(f, n, 0.2, 2), 3 * pk.wave(f, n, 0.7, 2))
    legs = [("Leg_BL", 0.0), ("Leg_FL", 0.75), ("Leg_BR", 0.5), ("Leg_FR", 0.25)]   # touch-down at f0, 10, 20, 30
    k.meta["legs"], k.meta["duty"] = legs, 0.70
    return pk.walk_cycle(k, n, legs, 0.12, 0.08, body, duty=0.70)


ROAR_P = [  # f, chest pitch, chest z, neck, head, jaw, tail pitch, ears
    (0, 0.0, 0.0, 0, 0, 0, 0, 0),
    (6, 1.0, -0.006, 1, 4, 0, 4, -6),
    (10, -0.2, -0.005, -1.5, -5, 2, 10, 3),
    (16, -1.0, -0.004, -3.5, -11, 7, 20, 10),
    (40, -1.0, -0.004, -3.5, -11, 11, 26, 12),
    (50, 0.0, -0.002, -2, -5, 4, 12, 4),
    (60, 0.0, 0.0, 0, 0, 0, 0, 0)]


def roar(k):
    """HORN-TO-THE-SKY BELLOW: tuck (anticipation), the head lifts 16 deg with the snout forward, the jaw opens late
    and the bellow pulses three times (jaw + flank pump: bellow1-3 on Mouth), slow return. Legs planted."""
    n = 60
    k.new_action("roar", n, False)
    for f, cp, cz, nk, hd, jw, tp, er in ROAR_P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Chest", f, rot=(cp, 0, 0), loc=(0, 0, cz))
        k.key("Neck", f, rot=(nk, 0, 0), loc=neck_lift(-(nk + hd)))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tail(k, f, tp, 0, lag=(1.0, 0.6, 0.4))
        ears(k, f, er, er, fwd=-er * 0.5)
    for f in (20, 28, 36):                                          # the three bellow pulses
        k.key("Jaw", f, rot=(JAW_MAX, 0, 0))
        k.key("Chest", f, rot=(-1.0, 0, 0), loc=(0, 0, 0.004))
        k.key("Head", f, rot=(-11.5, 0, 0))
    for f in (24, 32):
        k.key("Jaw", f, rot=(9, 0, 0))
        k.key("Chest", f, rot=(-0.8, 0, 0), loc=(0, 0, -0.004))
        k.key("Head", f, rot=(-11, 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)
    k.events["roar"] = {"bellow1": round(20 / n, 3), "bellow2": round(28 / n, 3), "bellow3": round(36 / n, 3)}


SZ, SP, CP, HT = -0.024, 1.5, 3.8, 59.7   # the braced strike: spine drop + pitch, chest pitch, head pitch
TAP_P = [  # f, spine z, spine pitch, chest pitch, neck, head pitch, head yaw, jaw, tail pitch, ears
    (0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0),
    (8, -0.006, 0.0, 1.5, 3, 14, 0, 0, 4, 0),
    (16, -0.006, 0.0, 1.5, 4, 44, 0, 0, 10, -8),
    (22, -0.002, 0.0, 2.0, 6, 62, 0, 0, 14, -10),     # face down, horn forward just above the snow
    (27, -0.002, 0.0, 2.0, 6, 57, 0, 0, 14, -10),     # cocked: the tip lifts
    (30, SZ, SP, CP, 6, HT, 0, 0, 16, -10),            # tap1: braced strike (forequarters drop, front knees fold)
    (34, -0.006, 0.5, 2.5, 6, 59, 0, 0, 16, -10),
    (39, -0.002, 0.0, 2.0, 6, 57, 0, 0, 16, -10),
    (42, SZ, SP, CP, 6, HT - 0.6, 0, 0, 18, -10),      # tap2: lands a touch shallower ...
    (46, -0.016, 1.0, 3.3, 6, HT - 1.2, 6, 0, 18, -10),  # ... and DRAGS the horn sideways along the snow
    (51, -0.002, 0.0, 2.0, 6, 57, 2, 0, 18, -10),
    (54, SZ, SP, CP, 6, HT, 0, 0, 20, -10),            # tap3
    (56, SZ, SP, CP, 6, HT, 0, 0, 20, -10),
    (58, -0.002, 0.0, 1.0, 3, 32, 0, 2, 26, 0),        # SNAP UP (in-betweens every 2 f)
    (60, -0.006, 0.0, -0.5, -1, 2, 0, 6, 30, 8),
    (62, 0.0, 0.0, -1.0, -4, -11, 0, 8, 32, 12),       # horn to the sky
    (66, 0.0, 0.0, -1.0, -4, -10.5, 0, 6, 30, 12),
    (86, 0.0, 0.0, -1.0, -4, -10.5, 0, 5, 26, 10),
    (94, 0.0, 0.0, -0.3, -1, -3, 0, 2, 8, 3),
    (100, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0)]


def horntap(k):
    """SIGNATURE - LIGHTNING TAPS: the forequarters lower and the head drives down at the throat, horn forward, the snout
    clear of the snow; three taps of the horn tip (tap1-3, a cocked lift then a 2-frame strike); the head snaps up and
    the horn points at the sky in 6 frames; hold while the lightning inlays flash (charge); slow return to rest."""
    n = 100
    k.new_action("act_horntap", n, False)
    for f, sz, sp, cp, nk, hd, hy, jw, tp, er in TAP_P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, sz))
        k.key("Chest", f, rot=(cp, 0, 0))
        brace = max(0.0, -sz - 0.002) / 0.022 * 0.080           # the shoulders drop, the neck holds the head up
        nl = neck_lift(-(nk + hd))
        k.key("Neck", f, rot=(nk, 0, 0), loc=(nl[0], nl[1], nl[2] + brace))
        k.key("Head", f, rot=(hd, hy, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tail(k, f, tp, 0, lag=(1.0, 0.6, 0.4))
        ears(k, f, abs(er), abs(er), fwd=er)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)
    k.events["act_horntap"] = {"tap1": round(30 / n, 3), "tap2": round(42 / n, 3), "tap3": round(54 / n, 3),
                               "snap": round(60 / n, 3), "charge": round(70 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    horntap(k)
    return stride


HEAD_XF = []
