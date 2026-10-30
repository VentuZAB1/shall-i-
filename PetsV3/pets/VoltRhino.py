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
HEIGHT = 8.69                # total height in studs at x1: now the back ridge top (final85 T1). The withers stay at 8.5
#                              studs: HEIGHT and H_MODEL both grew by the bbox ratio 1.6014 / 1.5661, so the body's world
#                              size and the stud size are unchanged

IRON_D = (76, 84, 102)       # back, shoulder shield, saddle, rump plate, folds, brows, nasal ridge, feet, back ridge
#                              (final85 N1: was (92, 100, 116); a darker, richer back)
IRON = (146, 154, 168)       # legs, head (studded) (final85 N2: was (156, 164, 178); tamer stud highlights)
FLANK = (126, 134, 150)      # the barrel flanks (r2 T-a: a step darker than the legs and head)
PALE = (222, 224, 228)       # belly strip (follows the slope), chin
HORN_IVORY = (232, 224, 204)  # main horn + brow nub (smooth, warm ivory)
HORN_SHADE = (205, 198, 180)  # horn collars + growth rings
VOLT = (190, 255, 64)        # THE accent: horn lightning, shoulder bolts, eye slits
EYE_HOT = (238, 255, 168)    # small hot centre of the eye slit
BLACK = (14, 14, 22)         # toenails, nostrils, eye sockets
MOUTH = (86, 18, 30)
JAW_MAX = 14.0               # largest jaw opening the mouth interior covers (no see-through); clips never key past it

H_MODEL = 1.605              # model height in Blender units (same units-per-stud as the Raiju: 1.498 / 8); was 1.57
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


def ltube(B, p0, p1, st, color, bone, n=2.4, seg=20):
    """round pillar-leg segment (final85 M5: no stacked boxes; rnd cannot do it, the kit caps edge rounding at 0.45 x
    the smallest half size): a studded superellipse loft from p0 to p1 through stations (f along p0 -> p1, run past
    0 / 1 to bury or dome the ends; half width (x); half depth (fore-aft))"""
    import blockkit as bk
    p0, p1 = Vector(p0), Vector(p1)
    R = bk.frame_from(p0, p1, (1, 0, 0))
    rings = []
    for f, hw, hd in st:
        c = p0 + (p1 - p0) * f
        r = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            cs, sn = math.cos(a), math.sin(a)
            r.append(c + R @ Vector((hw * math.copysign(abs(cs) ** (2.0 / n), cs),
                                     hd * math.copysign(abs(sn) ** (2.0 / n), sn), 0.0)))
        rings.append(r)
    return B.tube(rings, color, bone)


def puck(B, P, st, color, bone, n=2.4, seg=20):
    """round foot pad: horizontal superellipse rings [(z, half width, half depth)] around (P.x, P.y)"""
    rings = []
    for z, hw, hd in st:
        r = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            cs, sn = math.cos(a), math.sin(a)
            r.append(Vector((P.x + hw * math.copysign(abs(cs) ** (2.0 / n), cs),
                             P.y + hd * math.copysign(abs(sn) ** (2.0 / n), sn), z)))
        rings.append(r)
    return B.tube(rings, color, bone)


# leg loft stations (f, half width, half depth), same extents as the old blocks (final85 M5)
LEG_ST = {"F_thigh": [(-0.08, 0.120, 0.140), (0.0, 0.170, 0.200), (0.45, 0.165, 0.190), (0.85, 0.150, 0.162),
                      (1.0, 0.146, 0.156), (1.06, 0.130, 0.140), (1.10, 0.090, 0.100)],
          "F_shin": [(-0.13, 0.100, 0.100), (-0.06, 0.135, 0.140), (0.0, 0.140, 0.145), (0.5, 0.132, 0.137),
                     (1.0, 0.124, 0.128), (1.30, 0.124, 0.128)],
          "B_thigh": [(-0.10, 0.100, 0.170), (0.0, 0.130, 0.220), (0.40, 0.128, 0.200), (0.80, 0.120, 0.160),
                      (1.0, 0.117, 0.145), (1.08, 0.100, 0.120), (1.12, 0.070, 0.080)],
          "B_shin": [(-0.12, 0.090, 0.090), (-0.05, 0.120, 0.125), (0.0, 0.125, 0.130), (0.5, 0.120, 0.125),
                     (1.0, 0.116, 0.121), (1.10, 0.110, 0.115)],
          "B_hock": [(-0.15, 0.116, 0.121), (0.0, 0.124, 0.128), (0.5, 0.116, 0.120), (1.0, 0.106, 0.110),
                     (1.10, 0.106, 0.110)]}
PAD = [(0.008, 0.148, 0.152), (0.020, 0.160, 0.165), (0.075, 0.156, 0.161), (0.105, 0.142, 0.147), (0.120, 0.120, 0.125)]


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
          (0.40, 0.93, "Spine", 0.06, 0.06, 0.032)]         # rump plate: starts where the saddle ends, one step (r2 MM1)


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


def fold_wedge(B, L, y, s, bone, f_end=-0.50, w=0.07, thick=0.014, n=6):   # final85 M2: 0.030 -> 0.014
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
    Lb.tube(B, 0.0, sj + 0.06, FLANK, "Chest", j1=sj, step=0.11)       # r2 T-a: darker flanks (legs / head stay IRON)
    Lb.tube(B, sj - 0.06, Lb.length, FLANK, "Spine", j0=sj, step=0.11)
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
    for y, bn in ((-0.065, "Chest"),):                  # final85 M2: the rear fold (y 0.405) is gone - no third hoop
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
    # final85 T2: a volt bolt on each upper side of the saddle (same zig as the rump bolts), so the game camera behind
    # and above the pet sees the accent on the back, not only on the horn and the rump
    for s in (1, -1):
        Q = []
        for y, a in ((-0.02, 1.22), (0.11, 1.02), (0.05, 0.91), (0.22, 0.72)):
            Q.append(surf(Lb, y, a if s > 0 else math.pi - a, grow=armour_grow(Lb, y, a) + 0.004))
        zig(B, Q, VOLT, "Spine", 0.068)
    # final85 T1: an armour ridge - three short IRON_D spikes along the spine over the saddle (a crest in the 64 px
    # silhouette instead of a flat top; low, broad and blunt, not Raiju's tall dorsal spines)
    for y, L in ((-0.10, 0.10), (0.12, 0.11), (0.30, 0.09)):
        p, nrm = surf(Lb, y, math.pi / 2, grow=armour_grow(Lb, y, math.pi / 2))
        d = (nrm + Vector((0, 0.45, 0))).normalized()                    # raked back
        base = p - d * 0.03
        tip = p + d * L
        B.add((base + tip) / 2, (0.028, 0.050, (tip - base).length / 2), IRON_D, "Spine",
              R=bk.frame_from(base, tip, (1, 0, 0)), top=(0.30, 0.25), top_shift=(0, 0.012), nostud=True,
              role="detail", bevel=0.008)
    # ---------------- neck: short, thick, a dark fold across the nape
    Ln.tube(B, 0.0, Ln.length, IRON, "Neck", step=0.06)
    Ln.band(B, 0.0, Ln.length, PALE, "Neck", zlo=-1.0, zhi=-0.55, grow=0.008, step=0.05)          # pale throat
    Ln.band(B, Ln.s_at_y(-0.92), Ln.s_at_y(-1.00), IRON_D, "Neck", zlo=-0.30, grow=0.03, inset=0.02, step=0.04)
    # ---------------- head (pivot at the throat): lofted upper head, dark nasal ridge, jaw, chin
    Lh.tube(B, 0.0, Lh.length, IRON, "Head", step=0.08)
    Lh.band(B, Lh.s_at_y(-1.56), Lh.s_at_y(-1.10), IRON_D, "Head", zlo=0.62, grow=0.012, inset=0.02, step=0.04)
    # (final85 r3 MUST 1: the separate pale Jaw chin seg is gone; it read as a flat plank under the open jaw)
    # r2 MM2: the small chin above sits inside the head (it only shows when the jaw opens). The pale underside of the
    # snout is a narrow rounded strip along the loft's bottom line (0.08 wide, 0.012-0.018 proud, smooth): it runs on
    # from the throat strip and reads as a strip, not a plate. (The suggested head-loft band was tried: the head's
    # studs poked through its thin shell in a ragged patch, so it was not kept.)
    # r3 MUST 1: the strip stops ~0.1 short of the snout tip (y -1.52) and is now a smooth rounded loft (superellipse
    # rings along the loft's bottom line) that tapers to points at both ends, so no flat face or straight hard edge
    strip = []
    NS = 12
    for j in range(NS + 1):
        t = j / NS
        y = -1.04 + (-1.52 + 1.04) * t
        tp = min(1.0, t / 0.18, (1.0 - t) / 0.30) ** 0.6
        tp = max(tp, 0.12)
        c = Lh.surf(Lh.s_at_y(y), -math.pi / 2)
        hw, hh = 0.036 * tp, 0.011 * tp
        r = []
        for i in range(12):
            a_ = 2 * math.pi * i / 12
            cs, sn_ = math.cos(a_), math.sin(a_)
            r.append(c + Vector((hw * math.copysign(abs(cs) ** 0.8, cs), 0.0,
                                 0.002 + hh * math.copysign(abs(sn_) ** 0.8, sn_))))
        strip.append(r)
    B.tube(strip, PALE, "Head", nostud=True)
    #   (final85 M3: 0.14 / 0.055 -> 0.10 / 0.040; 0.015 lower so its underside shows as a thin pale strip under the
    #    snout, continuing the belly / throat strip, instead of two pale specks poking through the head's underside)
    B.seg((0, -1.40, 0.765), (0, -1.66, 0.755), 0.100, 0.006, MOUTH, "Head", studs=[], role="detail", bevel=0.003,
          top=(0.80, 1.0))     # lip line, as narrow as the M3 chin (0.142 poked out as red dots at the snout corners)
    # mouth interior riding the jaw, hidden inside the snout when closed: an open jaw (<= JAW_MAX) shows dark mouth,
    # never the background (clip review 3 MUST 3d)
    B.seg((0, -1.08, 0.84), (0, -1.60, 0.80), 0.10, 0.05, MOUTH, "Jaw", studs=[], role="detail", bevel=0.014,
          top=(0.45, 0.76))                     # tapers inward (r4 0.30/0.50 hid the open mouth; r5 0.45/0.60 = 23 px -> 0.76)
    Lh.band(B, Lh.s_at_y(-1.71), Lh.s_at_y(-1.52), IRON_D, "Head", zlo=0.40, grow=0.018, inset=0.02, step=0.04)
    # r3 MUST 1: a dark domed nose cap over the snout's flat front (its lit IRON end cap read as a white sliver in
    # closeb_cside2); superellipse rings like the head loft, 0.004 proud, so the snout tip reads as a dark muzzle
    nose = []
    for y, z, hw, hh in ((-1.690, 0.832, 0.163, 0.118), (-1.712, 0.829, 0.156, 0.109), (-1.721, 0.827, 0.140, 0.093),
                         (-1.727, 0.826, 0.110, 0.069)):
        r = []
        for i in range(24):
            a_ = 2 * math.pi * i / 24
            cs, sn_ = math.cos(a_), math.sin(a_)
            r.append(Vector((hw * math.copysign(abs(cs) ** 0.8, cs), y, z + hh * math.copysign(abs(sn_) ** 0.8, sn_))))
        nose.append(r)
    B.tube(nose, IRON_D, "Head", nostud=True)
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
        for col, half, out in ((BLACK, (0.011, 0.074, 0.156), 0.004), (VOLT, (0.009, 0.036, 0.110), 0.010),  # r4: frame
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
    B.spike((0, -1.22, 1.11), (0, -0.40, 1.0), 0.12, 0.050, HORN_IVORY, "Head", top=(0.12, 0.12), nostud=True)  # T-b
    # ---------------- legs: pillar legs, dark foot pads with 3 black toenails
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            # final85 M5: round pillar legs (studded superellipse lofts with the old blocks' extents) flowing into a
            # round pad, instead of stacked boxes (thigh / shin / hock / box pad)
            if fb == "F":
                ltube(B, H + Vector((0, 0, 0.10)), K, LEG_ST["F_thigh"], IRON, leg, seg=12)       # T-f: 20 -> 12
                ltube(B, K, A, LEG_ST["F_shin"], IRON, shin)                       # runs into the pad
            else:
                ltube(B, H + Vector((0, 0.03, 0.10)), K, LEG_ST["B_thigh"], IRON, leg, seg=12)
                ltube(B, K, A, LEG_ST["B_shin"], IRON, shin)
                ltube(B, A, P + Vector((0, 0.0, 0.03)), LEG_ST["B_hock"], IRON, foot)   # hock: 0.125 -> 0.105
            dk = (A - K).normalized()          # ONE elbow / knee fold: a tapered wedge on the outer face (r2 M3)
            ox = s * (0.134 if fb == "F" else 0.119)            # on the round leg: shorter fore-aft (+-0.07)
            c0 = K + dk * 0.035 + Vector((ox, -0.07, 0.03))
            c1 = K + dk * 0.075 + Vector((ox, 0.07, -0.03))
            B.seg(c0, c1, 0.013, 0.032, IRON_D, shin, side=(1, 0, 0), top=(1.0, 0.15), studs=[], rnd=0.40,
                  role="limb", bevel=0.006)
            puck(B, P, PAD, IRON_D, foot)      # final85 M5: a round pad 0.11 tall (was a 0.15 box), sole at 0.008
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


def plant(k, f, moves=None, toes=None):
    """IK every foot on its rest spot; moves = {leg: T} overrides (a lifted foot), toes = {leg: deg} foot tilt
    overrides (the kit default tips a lifted foot 35 deg toe-down at 0.12 lift)"""
    bpy.context.scene.frame_set(f)
    for leg in LEGS4:
        T = moves[leg] if moves and leg in moves else Vector((k.J[leg].x, k.J[leg].y, 0.0))
        if toes and leg in toes:
            k.solve_leg(leg, f, T, toe=toes[leg])
        else:
            k.solve_leg(leg, f, T)


def idle(k):
    """HORN TILT: slow weight shift, the head yaws +-6 deg so the horn tilts side to side, the left foreleg lifts 0.12
    and stamps down (f46), ear twitches, one tail flick (f90). Legs planted otherwise."""
    n = 120
    k.new_action("idle", n, True)
    SNORT = {70: 0.0, 71: 1.0, 72: 1.0, 73: 0.35, 74: 0.0, 76: -0.25, 79: 0.0}   # snort f70-73; r3 9+: settle f76
    for f in sorted(set(range(0, n + 1, 2)) | set(SNORT)):
        br = 0.5 + 0.5 * pk.wave(f, n, 0.25, 3)
        # weight shift (one cycle). final85 C1 ref (animationreference.org /tags/elephants, adult elephant 11.3-12.6 s):
        # the weight moves OFF the foreleg before it lifts, so the shift peaks on the right side (sw = -1) at f38, the
        # middle of the left foreleg's lift (was phase 0: the body leaned onto the lifting leg)
        sw = pk.wave(f, n, 0.433, 1)
        sn = SNORT.get(f, 0.0)
        k.key("Spine", f, rot=(0, 0, 1.2 * sw), loc=(0.010 * sw, 0, -0.004 * br))
        k.key("Chest", f, rot=(0.4 * br, 0, -0.6 * sw))
        k.key("Neck", f, rot=(0.5 * br, 2.0 * pk.wave(f, n, 0.1, 1), 0))
        k.key("Head", f, rot=(0.6 * pk.wave(f, n, 0.3, 2) - 8.0 * sn, 4.0 * pk.wave(f, n, 0.15, 1), 0))   # r4: 8 deg toss
        k.key("Jaw", f, rot=(1.0 + 1.0 * br + 4.0 * max(0.0, sn), 0, 0))
    for f, l, r in ((0, 0, 0), (16, 0, 0), (18, 14, 0), (21, 0, 0), (60, 0, 0), (62, 0, 12), (65, 0, 0),
                    (104, 0, 0), (106, 10, 10), (109, 0, 0), (120, 0, 0)):
        ears(k, f, l, r)
    for f, p, r in ((0, 4, 0), (82, 4, 0), (86, 12, 14), (89, 22, 28), (92, 26, 34), (96, 15, 18), (101, 7, 5),
                    (107, 4, 0), (120, 4, 0)):
        tail(k, f, p, r)
    k.bake_bezier_now()
    J = k.J
    for f in range(0, n + 1):
        mv = tz = None
        if 30 <= f <= 46:                                           # the foreleg lift + stamp
            u = (f - 30) / 16
            tz = {"Leg_FL": 3.0 * math.sin(math.pi * u)}            # r3 MUST 3: the sole stays nearly flat (3 deg toe)
            mv = {"Leg_FL": Vector((J["Leg_FL"].x, J["Leg_FL"].y - 0.015 * math.sin(math.pi * u),
                                    0.120 * math.sin(math.pi * u) ** 0.8))}      # r3 MUST 3: 0.060 -> 0.120
        plant(k, f, mv, tz)
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
    (16, -1.0, -0.004, -2.8, -11.7, 7, 20, 10),        # r4 T6: neck base -2.8 (pump 5 deg up to -7.8 on each pulse)
    (40, -1.0, -0.004, -2.8, -11.7, 11, 26, 12),
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
        # final85 N3: a neck pump on each pulse - the neck lifts 2 deg more while the head tips 2 deg back down, so
        # head + neck stays at 15 and the snout stays forward (3-frame ease: f-2 .. f .. f+2)
        # r4 T6: pump 5 deg (base -2.8 -> pulse -7.8, under the neck limit 8), the head counters it: total 15
        k.key("Neck", f, rot=(-7.8, 0, 0), loc=neck_lift(15.0))
        k.key("Head", f, rot=(-7.2, 0, 0))
        for g in (f - 2, f + 2):
            k.key("Neck", g, rot=(-5.3, 0, 0), loc=neck_lift(14.5))
            k.key("Head", g, rot=(-9.2, 0, 0))
    for f in (24, 32):
        k.key("Jaw", f, rot=(9, 0, 0))
        k.key("Chest", f, rot=(-0.8, 0, 0), loc=(0, 0, -0.004))
        k.key("Neck", f, rot=(-2.8, 0, 0), loc=neck_lift(14.5))       # r4 T6: back to the base between pulses
        k.key("Head", f, rot=(-11.7, 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)
    k.events["roar"] = {"bellow1": round(20 / n, 3), "bellow2": round(28 / n, 3), "bellow3": round(36 / n, 3)}


SZ, SP, CP, HT = -0.024, 1.5, 3.8, 59.7   # the braced strike: spine drop + pitch, chest pitch, head pitch
# extra neck lift per strike frame (probed): puts the Horn_Tip at z ~0.008 on every hold frame; tap3 strikes 2.5 deg
# deeper, so its pivot rises to keep the tip touching instead of digging in
TAP_LIFT = {30: -0.005, 31: -0.005, 42: -0.016, 43: -0.016, 54: 0.039, 55: 0.039, 57: 0.020}
TAP_REACH = {54: -0.045, 55: -0.045, 57: -0.020}   # tap3: the neck reaches forward so the deeper-pitched cheek clears
#                                                    the brisket
TAP_P = [  # f, spine z, spine pitch, chest pitch, neck, head pitch, head yaw, jaw, tail pitch, ears
    (0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0),
    (8, -0.006, 0.0, 1.5, 3, 14, 0, 0, 4, 0),
    (16, -0.006, 0.0, 1.5, 4, 44, 0, 0, 10, -8),
    (22, -0.002, 0.0, 2.0, 6, 62, 0, 0, 14, -10),     # face down, horn forward just above the snow
    (27, -0.002, 0.0, 2.0, 6, 57, 0, 0, 14, -10),     # cocked: the tip lifts
    # final85 C3: each strike HOLDS 2 frames on the snow, then REBOUNDS 3 frames after the hit (head 4 deg up, the brace
    # releases: chest back to 2.0, the shoulders rise); tap3 strikes 2.5 deg deeper than tap1 (the neck lifts the head
    # pivot so the tip still only touches the snow); tap2 stays shallower and drags the horn sideways during its hold
    (30, SZ, SP, CP, 6, HT, 0, 0, 16, -10),            # tap1: braced strike (forequarters drop, front knees fold)
    (31, SZ, SP, CP, 6, HT, 0, 0, 16, -10),            # hold
    (33, -0.010, -1.5, 2.0, 6, HT - 6.0, 0, 0, 16, -10),  # rebound (r2 T-d: 6 deg up + a 1.5 deg spine recoil)
    (39, -0.004, 0.2, 2.0, 6, 56.5, 0, 0, 16, -10),   # cocked again
    (42, SZ, SP, CP, 6, HT - 0.6, 0, 0, 18, -10),      # tap2: lands a touch shallower ...
    (43, SZ, SP, CP, 6, HT - 0.6, 3, 0, 18, -10),      # ... and DRAGS the horn sideways along the snow (hold)
    (45, -0.010, -1.5, 2.0, 6, HT - 6.6, 6, 0, 18, -10),  # rebound, flicking off the end of the drag
    (51, -0.002, 0.0, 2.0, 6, 57, 2, 0, 18, -10),
    (54, SZ, SP, CP, 6, HT + 2.5, 0, 0, 20, -10),      # tap3: the hardest, 2.5 deg deeper
    (55, SZ, SP, CP, 6, HT + 2.5, 0, 0, 20, -10),      # hold
    (57, -0.010, -1.5, 2.0, 6, HT - 3.5, 0, 0, 22, -10),  # rebound (6 deg up) = the snap's wind-up
    # r4 T7: the SNAP UP is spread over 7 frames (f57-64, eased 10/13/14/13/9/6/2 deg per frame) instead of 5
    # (it peaked at 24 deg in one frame and read as a whip)
    (58, -0.004, -0.8, 1.6, 4.5, 46.1, 0, 1, 24, -5),
    (59, -0.002, 0.0, 1.0, 3, 33.3, 0, 2, 26, 0),
    (60, -0.004, 0.0, 0.3, 1, 19.2, 0, 4, 28, 4),       # snap event
    (61, -0.006, 0.0, -0.5, -1, 6.4, 0, 6, 30, 8),
    (62, -0.003, 0.0, -0.8, -2.5, -3.0, 0, 7, 31, 10),
    (63, 0.0, 0.0, -1.0, -3.5, -9.0, 0, 8, 32, 12),
    (64, 0.0, 0.0, -1.0, -4, -11, 0, 8, 32, 12),       # horn to the sky
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
        brace += TAP_LIFT.get(f, 0.0)                            # per-strike contact trim
        nl = neck_lift(-(nk + hd))
        k.key("Neck", f, rot=(nk, 0, 0), loc=(nl[0], nl[1] + TAP_REACH.get(f, 0.0), nl[2] + brace))
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
