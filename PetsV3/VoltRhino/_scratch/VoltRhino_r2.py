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

H_MODEL = 1.57               # model height in Blender units (same units-per-stud as the Raiju: 1.498 / 8)
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)   # same world stud size as the Raiju

# leg joints (left side): shoulder/hip, elbow/stifle, carpus/hock, foot centre
LEGS = {"F": ((0.25, -0.56, 0.98), (0.25, -0.47, 0.58), (0.25, -0.53, 0.22), (0.25, -0.55, 0.07)),
        "B": ((0.20, 0.60, 1.00), (0.20, 0.46, 0.63), (0.20, 0.66, 0.30), (0.20, 0.61, 0.07))}
TAILP = [(0, 0.93, 1.20), (0, 1.01, 1.08), (0, 1.04, 0.96), (0, 1.05, 0.84)]
# body loft stations (y, zc, half width, half height), front -> back; the belly line rises 0.62 -> 0.77
BODY = [(-0.98, 1.08, 0.20, 0.26), (-0.86, 1.07, 0.31, 0.40), (-0.62, 1.08, 0.385, 0.46), (-0.30, 1.07, 0.39, 0.43),
        (0.02, 1.09, 0.37, 0.39), (0.34, 1.10, 0.345, 0.345), (0.62, 1.08, 0.325, 0.32), (0.84, 1.04, 0.27, 0.27),
        (0.96, 1.01, 0.15, 0.16)]
NECK = [(-0.70, 1.10, 0.27, 0.32), (-0.88, 1.07, 0.26, 0.29), (-1.06, 1.03, 0.225, 0.255)]
# head loft (upper head above the mouth line), front -> back: lip, nose, muzzle, eyes, cheeks, poll
HEAD = [(-1.71, 0.825, 0.150, 0.095), (-1.63, 0.84, 0.185, 0.14), (-1.45, 0.885, 0.20, 0.185),
        (-1.26, 0.965, 0.24, 0.24), (-1.07, 1.035, 0.265, 0.285), (-0.92, 1.075, 0.235, 0.26)]
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
          (-0.14, 0.40, "Spine", 0.34, 0.22, 0.020),        # saddle
          (0.36, 0.93, "Spine", -0.30, -0.02, 0.032)]       # rump plate


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
    B.seg((0, -1.00, 0.80), (0, -1.65, 0.738), 0.14, 0.055, PALE, "Jaw", top=(0.92, 0.85), ext=0.0, rnd=0.40)
    B.seg((0, -1.40, 0.765), (0, -1.66, 0.755), 0.142, 0.006, MOUTH, "Head", studs=[], role="detail", bevel=0.003)
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
        bc = p + up * 0.066 + n * 0.016 + d * 0.004
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
    for t0, t1, g in ((0.05, 0.13, 0.014), (0.47, 0.51, 0.008), (0.66, 0.70, 0.008)):
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
            Q.append((c + ax * s * (hw + 0.004) + dv * dz, ax * s, min(0.060, 1.15 * hd)))
        for i_, ((a_, na), (c_, nc)) in enumerate(zip([(q[0], q[1]) for q in Q], [(q[0], q[1]) for q in Q[1:]])):
            d_ = (c_ - a_).normalized()
            w_ = min(Q[i_][2], Q[i_ + 1][2])
            B.bar(a_ - d_ * (w_ * 0.35 if i_ else 0.0), c_, (na + nc).normalized(), w_, 0.013, VOLT, "Head",
                  studs=[], bevel=0.004, top=(1, 0.15) if i_ == len(Q) - 2 else (1, 1))
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
            dk = (A - K).normalized()                                                          # elbow / knee fold
            B.seg(K + dk * 0.02, K + dk * 0.09, (0.15 if fb == "F" else 0.137), (0.155 if fb == "F" else 0.142),
                  IRON_D, shin, rnd=0.40, role="limb")
            if fb == "F":                                                                       # shin gaiter
                B.seg(K + dk * 0.22, K + dk * 0.30, 0.134, 0.139, IRON_D, shin, rnd=0.40, role="limb")
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


HEAD_XF = []
