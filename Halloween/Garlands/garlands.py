# SLINGSHOT Halloween - bunting GARLANDS on the inner face of the hub's back wall (2026-10-12).
# Headless:  blender.exe -b --factory-startup --python garlands.py -- tex build hook render export
#
# Space (Blender, 1 m = 1 stud, +Z up, +Y = toward the players = Roblox -Z). The wall face is behind at y = -0.6.
#   Garland_Long  : hook points (-13,0,0) / (+13,0,0), catenary sag 3.5, 9 pennants (+ paper bat + felt pumpkin)
#   Garland_Short : hook points (-9.5,0,0) / (+9.5,0,0), sag 2.6, 7 pennants (+ paper bat + felt pumpkin)
#   Garland_Hook  : pivot = the hook point (the rope's support point); wall-plate back face at y = -0.6
# Pennants hang in the X-Z plane and face +Y.
#
# Cloth maps are authored directly in UV space (numpy, 2x supersampled). Every pennant UV island is an isometric copy
# (rotated, never mirrored on the front) of its flat sewing pattern (x = to the viewer's right, w = up from the tip),
# so colour (fabric, faded dye, per-thread tone, crisp printed symbol from signed-distance shapes, stitches, fraying,
# dirt), height (canvas weave, seam grooves, puckers, drape creases -> tangent normal map), roughness and an analytic AO
# are evaluated per pixel. One 1024 atlas is shared by both garlands. The hook uses the kit pipeline (hi sculpt ->
# bake_set).
import sys, os, math, random, json, time, bisect
HALLOWEEN = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween"
sys.path.insert(0, HALLOWEEN)
from hkit import *  # noqa
import pumpkin as PK  # read-only: grin()
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix, geometry

OUT = os.path.join(HALLOWEEN, "Garlands")
MAPS = os.path.join(OUT, "maps")
BLEND = os.path.join(OUT, "garlands.blend")
os.makedirs(MAPS, exist_ok=True)

# ------------------------------------------------------------------ dimensions (studs)
T = 0.02          # cloth thickness (front skin at +T, back skin at 0 relative to the rope plane)
ROPE_R = 0.09     # rope radius (0.18 thick)
TIP = 2.48        # pennant tip below the rope centre (sleeve top is +0.125 -> 2.6 long)
ST = 0.20         # hem stitch line below the rope centre
W_ST = TIP - ST   # pattern w of the stitch line
SL_R = 0.125      # sleeve (hem roll) outer radius
STRIP = 0.08      # folded-back hem strip below the back stitch
HW = 0.9          # half width (1.8 wide)
ROWS = 13         # triangular lattice rows tip -> stitch
WRAP_R = 0.13     # rope centre radius around the hook arm (arm 0.04 + rope 0.09)
WRAP_DY = 0.30    # forward shift of the rope over its 1.4 turns around the arm
ARM_Z = -WRAP_R   # hook arm axis height below the hook point

# ------------------------------------------------------------------ atlas layout (final px, 1024)
ATLAS = 1024
SS = 2
D = 155.0         # px per stud
MARG = 8
DELTA = 1.17      # interleave step between neighbouring pennant islands (studs)


def _hermite(p0, m0, p1, m1, t):
    t2, t3 = t * t, t * t * t
    return (2 * t3 - 3 * t2 + 1) * p0 + (t3 - 2 * t2 + t) * m0 + (-2 * t3 + 3 * t2) * p1 + (t3 - t2) * m1


def _sleeve_dense():
    """Front half of the hem's outer skin, (y, z) relative to the rope centre: stitch -> over the rope -> top."""
    phi0 = math.radians(-35.0)
    pc = Vector((SL_R * math.cos(phi0), SL_R * math.sin(phi0)))
    tc = Vector((-math.sin(phi0), math.cos(phi0)))
    pf = Vector((T, -ST))
    front = [_hermite(pf, Vector((0.0, 0.17)), pc, tc * 0.17, i / 40) for i in range(41)]
    arc = [Vector((SL_R * math.cos(p), SL_R * math.sin(p))) for p in np.linspace(phi0, math.pi / 2, 61)[1:]]
    half = front + arc
    s = [0.0]
    for i in range(1, len(half)):
        s.append(s[-1] + (half[i] - half[i - 1]).length)
    return half, s, s[len(front) - 1]


HALF, HALF_S, S_BEZ = _sleeve_dense()
S_TOP = HALF_S[-1]
W_TOP = W_ST + S_TOP


def _half_at(s):
    i = min(max(bisect.bisect_left(HALF_S, s), 1), len(HALF_S) - 1)
    t = (s - HALF_S[i - 1]) / max(1e-9, HALF_S[i] - HALF_S[i - 1])
    return HALF[i - 1].lerp(HALF[i], max(0.0, min(1.0, t)))


def sleeve_at(s):
    """(y forward, z up) of the hem's outer skin at arc length s from the front stitch (0 .. 2*S_TOP + STRIP)."""
    if s <= S_TOP:
        return _half_at(s)
    if s <= 2 * S_TOP:
        p = _half_at(2 * S_TOP - s)
        return Vector((-p.x, p.y))
    return Vector((-T, -ST - (s - 2 * S_TOP)))


def sleeve_samples():
    f = [0.0, S_BEZ * 0.5, S_BEZ, S_BEZ + (S_TOP - S_BEZ) / 3, S_BEZ + 2 * (S_TOP - S_BEZ) / 3, S_TOP]
    return f + [2 * S_TOP - x for x in reversed(f[:-1])] + [2 * S_TOP + STRIP]


def flag_island(k):
    row, col = (0, k) if k < 5 else (1, k - 5)
    return dict(cx=MARG + HW * D + col * DELTA * D, y0=MARG + row * (W_TOP * D + MARG), o=1 if col % 2 == 0 else -1)


def flag_uv(isl, xp, w):
    if isl["o"] > 0:
        u, v = isl["cx"] + xp * D, isl["y0"] + w * D
    else:
        u, v = isl["cx"] - xp * D, isl["y0"] + (W_TOP - w) * D
    return (u / ATLAS, v / ATLAS)


ROW1_TOP = MARG + 2 * (W_TOP * D + MARG)            # ~864
ROPE_UX0 = 8.0
ROPE_Y0 = ROW1_TOP + 10.0
ROPE_HS = 2 * math.pi * ROPE_R * D                  # strip height = circumference
L_STRIP = (ATLAS - 8.0 - ROPE_UX0) / D              # studs of rope along the strip
BAT_S = 0.45                                        # paper bat: normalized -> studs
BAT_C = (930.0, 492.0)
R_P, RZ_P = 0.30, 0.22                              # felt pumpkin radius / half height
PUMP_C = (930.0, 606.0)
STEM_PATCH = (868.0, 676.0, 992.0, 700.0)
THREAD_PATCH = (868.0, 712.0, 992.0, 728.0)


def rope_uv(s, frac):
    return ((ROPE_UX0 + s * D) / ATLAS, (ROPE_Y0 + frac * ROPE_HS) / ATLAS)


def patch_uv(patch, fu, fv):
    x0, y0, x1, y1 = patch
    return ((x0 + 4 + fu * (x1 - x0 - 8)) / ATLAS, (y0 + 4 + fv * (y1 - y0 - 8)) / ATLAS)


# ------------------------------------------------------------------ designs
COL = dict(O=(196, 92, 30), B=(40, 35, 42), P=(92, 44, 124))
INK = dict(black=(25, 20, 23), orange=(226, 118, 34), bone=(228, 214, 180), moon=(236, 216, 152))
THREAD = dict(O=(46, 30, 22), B=(208, 130, 52), P=(222, 208, 174))
OLIVE = (98, 102, 44)
FLESH = (244, 200, 118)
DESIGNS = [
    dict(name="O_Bat", fab="O", sym="bat", ink="black", lift=0.0, seed=11),
    dict(name="B_Jack", fab="B", sym="jack", ink="orange", seed=12),
    dict(name="P_Skull", fab="P", sym="skull", ink="bone", seed=13),
    dict(name="O_Spider", fab="O", sym="spider", ink="black", seed=14),
    dict(name="B_Moon", fab="B", sym="moon", ink="moon", seed=15),
    dict(name="P_Bat", fab="P", sym="bat", ink="orange", lift=16.0, seed=16),
    dict(name="O_Face", fab="O", sym="face", ink="black", seed=17),
    dict(name="B_SkullBones", fab="B", sym="skullbones", ink="bone", seed=18),
    dict(name="P_Spider", fab="P", sym="spider", ink="bone", seed=19),
]
GARLANDS = {
    "Garland_Long": dict(a=13.0, d=3.5, flags=[0, 1, 2, 3, 4, 5, 6, 7, 8], pitch=2.7,
                         extras=[("bat", 2, 0.56), ("pumpkin", 5, 0.46)], seed=101),
    "Garland_Short": dict(a=9.5, d=2.6, flags=[0, 1, 8, 6, 4, 2, 3], pitch=2.6,
                          extras=[("bat", 1, 0.74), ("pumpkin", 4, 0.50)], seed=202),
}


def L3(c):
    return np.array(lin(c), np.float32)


# ------------------------------------------------------------------ numpy noise + signed distances
def sstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def _hash(i, j, seed):
    h = (np.asarray(i, np.int64) * 374761393 + np.asarray(j, np.int64) * 668265263 + int(seed) * 2654435761) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    h = h ^ (h >> 16)
    return (h & 0xFFFFFF).astype(np.float64) / 16777216.0


def vnoise(x, y, seed=0, py=None):
    xf, yf = np.floor(x), np.floor(y)
    fx, fy = x - xf, y - yf
    xi, yi = xf.astype(np.int64), yf.astype(np.int64)
    y0, y1 = yi, yi + 1
    if py:
        y0, y1 = y0 % py, y1 % py
    ux, uy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b = _hash(xi, y0, seed), _hash(xi + 1, y0, seed)
    c, d = _hash(xi, y1, seed), _hash(xi + 1, y1, seed)
    return (a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy) * 2 - 1


def fbm2(x, y, octaves=4, seed=0, py=None):
    s, amp, norm = 0.0, 1.0, 0.0
    for o in range(octaves):
        s = s + amp * vnoise(x, y, seed + o * 17, py * (2 ** o) if py else None)
        norm += amp
        amp *= 0.5
        x, y = x * 2.0, y * 2.0
    return s / norm


def sd_circle(x, y, cx, cy, r):
    return np.hypot(x - cx, y - cy) - r


def sd_ellipse(x, y, cx, cy, a, b):
    px, py = (x - cx) / a, (y - cy) / b
    f = np.hypot(px, py)
    g = np.hypot(px / a, py / b) / np.maximum(f, 1e-6)
    return (f - 1) / np.maximum(g, 1e-6)


def sd_capsule(x, y, ax, ay, bx, by, r):
    pax, pay, bax, bay = x - ax, y - ay, bx - ax, by - ay
    h = np.clip((pax * bax + pay * bay) / (bax * bax + bay * bay), 0, 1)
    return np.hypot(pax - bax * h, pay - bay * h) - r


def sd_polyline(x, y, pts, r):
    d = np.full(np.shape(x), 1e9)
    for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
        d = np.minimum(d, sd_capsule(x, y, ax, ay, bx, by, r))
    return d


def sd_rbox(x, y, cx, cy, hx, hy, r):
    qx, qy = np.abs(x - cx) - hx + r, np.abs(y - cy) - hy + r
    return np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - r


def sd_poly(x, y, pts):
    """Exact signed distance to a closed polygon (negative inside)."""
    pts = np.asarray(pts, np.float64)
    d = np.full(np.shape(x), 1e18)
    s = np.ones(np.shape(x))
    n = len(pts)
    for i in range(n):
        vix, viy = pts[i]
        vjx, vjy = pts[i - 1]
        ex, ey = vjx - vix, vjy - viy
        wx, wy = x - vix, y - viy
        t = np.clip((wx * ex + wy * ey) / (ex * ex + ey * ey), 0, 1)
        bx, by = wx - ex * t, wy - ey * t
        d = np.minimum(d, bx * bx + by * by)
        c1, c2, c3 = y >= viy, y < vjy, ex * wy > ey * wx
        flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
        s = np.where(flip, -s, s)
    return s * np.sqrt(d)


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


def star4(cx, cy, ro, ri_k=0.34, rot=0.0):
    pts = []
    for k in range(8):
        a = math.pi / 2 + rot + k * math.pi / 4
        r = ro if k % 2 == 0 else ro * ri_k
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ------------------------------------------------------------------ symbols (normalized units, y up)
def bat_outline(lift_deg=0.0):
    """Fierce bat silhouette. Returns (right half top-centre -> bottom-centre, full closed outline)."""
    head = [(0.0, 0.150), (0.048, 0.185), (0.092, 0.385), (0.125, 0.165), (0.155, 0.085)]
    lead = [(0.30, 0.17), (0.43, 0.29), (0.53, 0.41), (0.56, 0.48), (0.585, 0.415), (0.72, 0.40), (0.87, 0.37),
            (1.00, 0.31)]
    fingers = [(1.00, 0.31), (0.80, -0.03), (0.58, -0.21), (0.35, -0.22), (0.15, -0.15)]
    depths = [0.20, 0.22, 0.18, 0.16]
    trail = []
    for (ax, ay), (bx, by), dp in zip(fingers[:-1], fingers[1:], depths):
        L = math.hypot(bx - ax, by - ay)
        nx, ny = -(by - ay) / L, (bx - ax) / L          # left normal of the chord (points out of the wing)
        cx, cy = (ax + bx) / 2 - nx * dp * L, (ay + by) / 2 - ny * dp * L
        for t in (0.2, 0.4, 0.6, 0.8):
            trail.append(((1 - t) ** 2 * ax + 2 * (1 - t) * t * cx + t * t * bx,
                          (1 - t) ** 2 * ay + 2 * (1 - t) * t * cy + t * t * by))
        trail.append((bx, by))
    body = [(0.11, -0.31), (0.055, -0.41), (0.0, -0.46)]
    right = head + lead + trail + body
    if lift_deg:
        ox, oy = 0.155, 0.085
        out = []
        for x, y in right:
            a = math.radians(lift_deg) * float(sstep(0.16, 0.6, np.array(x)))
            dx, dy = x - ox, y - oy
            out.append((ox + dx * math.cos(a) - dy * math.sin(a), oy + dx * math.sin(a) + dy * math.cos(a)))
        right = out
    left = [(-x, y) for x, y in reversed(right[1:-1])]
    return right, right + left


def bat_sd(x, y, lift=0.0):
    _r, full = bat_outline(lift)
    d = sd_poly(x, y, full)
    d = np.minimum(d, sd_ellipse(x, y, 0.0, -0.10, 0.125, 0.29))
    return np.minimum(d, sd_circle(x, y, 0.0, 0.07, 0.11))


def skull_sd(x, y):
    cran = sd_circle(x, y, 0.0, 0.16, 0.58)
    face = sd_rbox(x, y, 0.0, -0.18, 0.42, 0.30, 0.14)
    jaw = sd_rbox(x, y, 0.0, -0.55, 0.27, 0.15, 0.08)
    sk = smin(smin(cran, face, 0.10), jaw, 0.06)
    notch = np.minimum(sd_circle(x, y, 0.64, -0.44, 0.26), sd_circle(x, y, -0.64, -0.44, 0.26))
    sk = np.maximum(sk, -notch)
    eye = [(0.09, 0.00), (0.44, 0.13), (0.41, -0.11), (0.22, -0.19)]
    eyes = np.minimum(sd_poly(x, y, eye), sd_poly(x, y, [(-px, py) for px, py in eye])) - 0.035
    nose = sd_poly(x, y, [(0.0, -0.20), (0.095, -0.35), (0.0, -0.30), (-0.095, -0.35)]) - 0.012
    teeth = sd_capsule(x, y, -0.23, -0.50, 0.23, -0.50, 0.022)
    for tx in (-0.17, -0.085, 0.0, 0.085, 0.17):
        teeth = np.minimum(teeth, sd_capsule(x, y, tx, -0.41, tx, -0.61, 0.016))
    crack = sd_polyline(x, y, [(0.24, 0.74), (0.15, 0.55), (0.25, 0.43), (0.17, 0.30)], 0.016)
    return sk, np.minimum(np.minimum(eyes, nose), np.minimum(teeth, crack))


def crossbones_sd(x, y):
    d = np.full(np.shape(x), 1e9)
    for (ax, ay, bx, by) in ((-0.80, -0.78, 0.80, 0.50), (0.80, -0.78, -0.80, 0.50)):
        d = np.minimum(d, sd_capsule(x, y, ax, ay, bx, by, 0.065))
        L = math.hypot(bx - ax, by - ay)
        nx, ny = -(by - ay) / L * 0.07, (bx - ax) / L * 0.07
        for ex, ey in ((ax, ay), (bx, by)):
            d = np.minimum(d, sd_circle(x, y, ex + nx, ey + ny, 0.085))
            d = np.minimum(d, sd_circle(x, y, ex - nx, ey - ny, 0.085))
    return d


def jack_sd(x, y, seed):
    body = np.full(np.shape(x), 1e9)
    for cx, cy, a, b in ((0, -0.05, 0.36, 0.60), (0.30, -0.06, 0.38, 0.57), (-0.30, -0.06, 0.38, 0.57),
                         (0.55, -0.08, 0.34, 0.47), (-0.55, -0.08, 0.34, 0.47)):
        body = np.minimum(body, sd_ellipse(x, y, cx, cy, a, b))
    stem = sd_poly(x, y, [(-0.085, 0.45), (-0.07, 0.62), (-0.02, 0.76), (0.09, 0.87), (0.17, 0.81), (0.07, 0.70),
                          (0.06, 0.58), (0.085, 0.45)])
    ribs = np.full(np.shape(x), 1e9)
    for k in (-0.46, -0.17, 0.17, 0.46):
        xc = k * np.sqrt(np.clip(1 - ((y + 0.05) / 0.64) ** 2, 0, 1))
        ribs = np.minimum(ribs, np.abs(x - xc) - 0.016)
    ribs = np.maximum(ribs, body + 0.04)
    eye = [(0.10, 0.00), (0.48, 0.25), (0.40, -0.07)]
    holes = np.minimum(sd_poly(x, y, eye), sd_poly(x, y, [(-px, py) for px, py in eye]))
    holes = np.minimum(holes, sd_poly(x, y, [(-0.085, -0.21), (0.085, -0.21), (0.0, -0.06)]))
    mouth = PK.grin(0.56, (-0.31, 0.11), (-0.52, 0.22),
                    top_teeth=[(-0.24, 0.12, 0.02, 0.12), (0.20, 0.12, 0.02, 0.13)],
                    bot_teeth=[(-0.02, 0.12, 0.02, 0.12)], corner_up=0.06, step=0.025, jit=0.004, seed=seed)
    holes = np.minimum(holes, sd_poly(x, y, mouth))
    return body, stem, ribs, holes


def face_sd(x, y, seed):
    eye = [(0.08, 0.06), (0.56, 0.36), (0.46, -0.03)]
    d = np.minimum(sd_poly(x, y, eye), sd_poly(x, y, [(-px, py) for px, py in eye]))
    d = np.minimum(d, sd_poly(x, y, [(-0.10, -0.13), (0.10, -0.13), (0.0, 0.06)]))
    mouth = PK.grin(0.64, (-0.31, 0.12), (-0.58, 0.26),
                    top_teeth=[(-0.30, 0.13, 0.02, 0.15), (0.26, 0.13, 0.02, 0.16)],
                    bot_teeth=[(-0.02, 0.14, 0.02, 0.16)], corner_up=0.07, step=0.025, jit=0.004, seed=seed)
    return np.minimum(d, sd_poly(x, y, mouth))


def moon_sd(x, y):
    moon = np.maximum(sd_circle(x, y, -0.10, 0.0, 0.70), -sd_circle(x, y, 0.24, 0.16, 0.60))
    craters = np.minimum(np.minimum(sd_circle(x, y, -0.56, -0.12, 0.085), sd_circle(x, y, -0.36, -0.47, 0.06)),
                         np.minimum(sd_circle(x, y, -0.62, 0.22, 0.05), sd_circle(x, y, -0.18, -0.62, 0.04)))
    craters = np.maximum(craters, moon + 0.03)
    stars = np.minimum(sd_poly(x, y, star4(0.40, -0.36, 0.15)), sd_poly(x, y, star4(0.56, 0.40, 0.11)))
    stars = np.minimum(stars, sd_poly(x, y, star4(0.12, -0.78, 0.08)))
    return moon, craters, stars


SPIDER_LEGS = [((0.08, 0.18), (0.36, 0.42), (0.50, 0.80)),
               ((0.11, 0.14), (0.46, 0.30), (0.78, 0.38)),
               ((0.11, 0.08), (0.44, 0.10), (0.74, -0.24)),
               ((0.08, 0.04), (0.34, -0.06), (0.52, -0.64))]


def spider_sd(x, y):
    ceph = sd_ellipse(x, y, 0.0, 0.12, 0.12, 0.12)
    head = sd_ellipse(x, y, 0.0, 0.25, 0.07, 0.06)
    abd = sd_ellipse(x, y, 0.0, -0.18, 0.20, 0.25)
    body = smin(smin(ceph, abd, 0.05), head, 0.03)
    legs = np.full(np.shape(x), 1e9)
    for sgn in (-1, 1):
        for c, k, t in SPIDER_LEGS:
            legs = np.minimum(legs, sd_capsule(x, y, sgn * c[0], c[1], sgn * k[0], k[1], 0.034))
            legs = np.minimum(legs, sd_capsule(x, y, sgn * k[0], k[1], sgn * t[0], t[1], 0.023))
    fang = np.minimum(sd_poly(x, y, [(0.015, 0.30), (0.06, 0.29), (0.03, 0.38)]),
                      sd_poly(x, y, [(-0.015, 0.30), (-0.06, 0.29), (-0.03, 0.38)]))
    spider = np.minimum(np.minimum(body, legs), fang)
    hour = np.minimum(sd_poly(x, y, [(-0.075, -0.07), (0.075, -0.07), (0.0, -0.17)]),
                      sd_poly(x, y, [(-0.075, -0.27), (0.075, -0.27), (0.0, -0.17)])) - 0.006
    return spider, hour


def sym_layers(dsg, X, Wd):
    """Paint layers in order: (signed distance in studs, 'ink'|'base', colour)."""
    s = dsg["sym"]
    ink = L3(INK[dsg["ink"]])
    if s == "bat":
        S, wc = 0.48, 1.80
        return [(bat_sd(X / S, (Wd - wc) / S, dsg.get("lift", 0.0)) * S, "ink", ink)]
    if s == "jack":
        S, wc = 0.50, 1.69
        body, stem, ribs, holes = jack_sd(X / S, (Wd - wc) / S, dsg["seed"])
        rim = np.maximum(holes, -(holes + 0.032))
        return [(body * S, "ink", ink), (stem * S, "ink", L3(OLIVE)), (ribs * S, "ink", ink * 0.42),
                (holes * S, "base", None), (rim * S, "ink", L3(FLESH))]
    if s in ("skull", "skullbones"):
        S, wc = (0.46, 1.70) if s == "skull" else (0.42, 1.71)
        x, y = X / S, (Wd - wc) / S
        sk, holes = skull_sd(x, y)
        out = []
        if s == "skullbones":
            out.append((np.maximum(crossbones_sd(x, y), -(sk - 0.06)) * S, "ink", ink))
        return out + [(sk * S, "ink", ink), (holes * S, "base", None)]
    if s == "moon":
        S, wc = 0.50, 1.70
        moon, craters, stars = moon_sd(X / S, (Wd - wc) / S)
        return [(moon * S, "ink", ink), (craters * S, "ink", ink * 0.72), (stars * S, "ink", ink)]
    if s == "spider":
        S, wc = 0.50, 1.50
        sp, hour = spider_sd(X / S, (Wd - wc) / S)
        thread = sd_capsule(X, Wd, 0.0, wc + 0.30 * S, 0.0, W_ST - 0.035, 0.0065)
        return [(np.minimum(sp * S, thread), "ink", ink), (hour * S, "base", None)]
    if s == "face":
        S, wc = 0.55, 1.62
        f = face_sd(X / S, (Wd - wc) / S, dsg["seed"])
        rim = np.maximum(f, -(f + 0.026))
        return [(f * S, "ink", ink), (rim * S, "ink", L3(FLESH))]
    return []


SYM_BOX = dict(bat=(0.62, 1.40, 2.12), jack=(0.58, 1.30, 2.18), skull=(0.40, 1.38, 2.10),
               skullbones=(0.50, 1.28, 2.12), moon=(0.45, 1.30, 2.10), spider=(0.48, 1.14, 2.28),
               face=(0.42, 1.25, 1.90))


# ------------------------------------------------------------------ pattern -> pixels
def flag_pattern(X, Wd, dsg, pix):
    sd0 = dsg["seed"]
    fab = L3(COL[dsg["fab"]])
    n = X.shape[0]
    # canvas weave, 0.05 stud thread pitch, slightly irregular
    p = 0.05
    jx = X + 0.007 * vnoise(X * 7, Wd * 7, sd0 + 1)
    jy = Wd + 0.007 * vnoise(X * 7 + 31.7, Wd * 7, sd0 + 2)
    gi, gj = np.floor(jx / p), np.floor(jy / p)
    fx, fy = jx / p - gi, jy / p - gj
    gi, gj = gi.astype(np.int64), gj.astype(np.int64)
    ti = 0.82 + 0.36 * _hash(gi, 7, sd0)
    tj = 0.82 + 0.36 * _hash(gj, 11, sd0)
    slub_i = 1 + 0.18 * vnoise(gi * 3.1, jy * 2.5, sd0 + 5)
    slub_j = 1 + 0.18 * vnoise(jx * 2.5, gj * 3.1, sd0 + 6)
    # plain weave: at every crossing (cell centre) one thread is fully over, the other fully under (checkerboard)
    warp = np.sin(np.pi * fx) ** 0.7 * ti * slub_i * (0.5 + 0.5 * np.cos(np.pi * (jy / p - 0.5) + np.pi * gi))
    weft = np.sin(np.pi * fy) ** 0.7 * tj * slub_j * (0.5 + 0.5 * np.cos(np.pi * (jx / p - 0.5) + np.pi * gj + np.pi))
    hwv = np.clip(np.maximum(warp, weft), 0, 1.3)
    tone = np.where(warp > weft, ti, tj)
    col = fab[None, :] * (0.80 + 0.24 * hwv)[:, None] * (1 + 0.28 * (tone - 1.0))[:, None]
    col *= (1 + 0.12 * fbm2(X * 1.3 + sd0 * 3.1, Wd * 1.3, 4, sd0 + 3))[:, None]
    fade = sstep(0.05, 0.55, fbm2(X * 0.8 + 11, Wd * 0.8, 3, sd0 + 4))
    lum = (col * np.array([0.2126, 0.7152, 0.0722], np.float32)).sum(1)
    faded = (lum[:, None] + 0.55 * (col - lum[:, None])) * 1.2
    col = col + (faded - col) * (0.34 * fade)[:, None]
    # edges of the pattern
    hw_at = HW * np.minimum(1.0, Wd / W_ST)
    ke = 1.0 / math.sqrt(1 + (HW / W_ST) ** 2)
    dside = np.where(Wd <= W_ST, (hw_at - np.abs(X)) * ke, HW - np.abs(X))
    # dust / grime: toward the tip and along the edges (dust reads lighter on black)
    dirt = 0.22 * (1 - sstep(0.0, 1.0, Wd)) * (0.6 + 0.4 * fbm2(X * 5, Wd * 5, 3, sd0 + 7))
    dirt += 0.10 * (1 - sstep(0.0, 0.07, dside))
    col = col + (L3((70, 56, 42))[None, :] - col) * np.clip(dirt, 0, 0.4)[:, None]
    fabric = col.copy()
    # printed symbol
    ink = np.zeros(n, np.float32)
    wear = sstep(0.35, 0.8, fbm2(X * 6, Wd * 6, 3, sd0 + 9)) * np.clip(hwv, 0, 1)
    box = SYM_BOX[dsg["sym"]]
    sel = (np.abs(X) < box[0]) & (Wd > box[1]) & (Wd < box[2])
    if sel.any():
        Xs, Ws = X[sel], Wd[sel]
        cs, inks, fabs = col[sel], ink[sel], fabric[sel]
        rag = 0.0022 * vnoise(Xs * 45, Ws * 45, sd0 + 21)
        for sd, kind, c in sym_layers(dsg, Xs, Ws):
            a = np.clip(0.5 - (sd + rag) / pix, 0, 1)
            if kind == "ink":
                ci = c[None, :] * (0.88 + 0.14 * np.clip(hwv[sel], 0, 1.2))[:, None]
                a = a * (1 - 0.25 * wear[sel])
                cs = cs * (1 - a)[:, None] + ci * a[:, None]
                inks = inks * (1 - a) + a
            else:
                cs = cs * (1 - a)[:, None] + fabs * a[:, None]
                inks = inks * (1 - a)
        col[sel], ink[sel] = cs, inks
    # stitches: running stitch along the hem line and 0.07 inside both slanted edges
    thread = L3(THREAD[dsg["fab"]])
    pitch, dash = 0.105, 0.031
    w_seam = W_ST + 0.012
    xc = np.round((X - 0.02) / pitch) * pitch + 0.02
    d_top = np.hypot(np.maximum(np.abs(X - xc) - dash, 0), Wd - w_seam) - 0.0105
    d_top = np.where(np.abs(X) < HW - 0.05, d_top, 1.0)
    lal = Wd / ke
    lc = np.round(lal / pitch) * pitch
    side_rng = (Wd > 0.34) & (Wd < W_ST - 0.04)
    d_sd = np.hypot(np.maximum(np.abs(lal - lc) - dash, 0), dside - 0.07) - 0.0095
    d_sd = np.where(side_rng, d_sd, 1.0)
    d_st = np.minimum(d_top, d_sd)
    a_st = np.clip(0.5 - d_st / pix, 0, 1)
    twist = 0.5 + 0.5 * np.sin((X * 0.7 + Wd) / 0.009)
    col = col * (1 - a_st)[:, None] + (thread[None, :] * (0.8 + 0.35 * twist)[:, None]) * a_st[:, None]
    # loose weft threads at the raw tip
    tipz = 1 - sstep(0.06, 0.42, Wd)
    edge = 1 - sstep(0.0, 0.04, dside)
    stripes = 0.5 + 0.5 * np.sin(lal / 0.012 + 3 * vnoise(lal * 30, dside * 30, sd0 + 31))
    fr = tipz * edge
    col = col * (1 + 0.35 * fr * stripes)[:, None]
    # height (studs)
    H = 0.0022 * hwv
    H += -0.0045 * np.exp(-((Wd - w_seam) / 0.028) ** 2) * (np.abs(X) < HW - 0.02)
    H += -0.0025 * np.exp(-((dside - 0.07) / 0.02) ** 2) * side_rng
    H += 0.0035 * np.sqrt(np.clip(-d_st / 0.0105, 0, 1))
    H += 0.0028 * (1 - sstep(0.035, 0.05, dside)) * side_rng
    H += 0.0030 * np.sin(2 * np.pi * X / 0.14 + 2.0 * vnoise(X * 6, Wd * 2, sd0 + 8)) * np.exp(-((Wd - W_ST) / 0.08) ** 2)
    H += 0.0020 * fr * stripes
    rng = random.Random(sd0 * 7 + 3)
    for _ in range(3):                   # drape creases from the hem toward the tip
        sg = rng.choice((-1, 1))
        ax, aw = sg * rng.uniform(0.25, 0.8), W_ST - rng.uniform(0.02, 0.15)
        bx, bw = sg * rng.uniform(-0.05, 0.22), W_ST - rng.uniform(0.7, 1.5)
        dcap = sd_capsule(X, Wd, ax, aw, bx, bw, 0.0)
        tt = np.clip(((X - ax) * (bx - ax) + (Wd - aw) * (bw - aw)) / ((bx - ax) ** 2 + (bw - aw) ** 2), 0, 1)
        H += rng.uniform(0.004, 0.008) * np.exp(-(dcap / 0.05) ** 2) * (1 - tt) ** 1.5 * (Wd < W_ST)
    # ambient occlusion (analytic): weave gaps, seam crease, the roll's shadow on the panel, edges, loose threads
    ao = 0.84 + 0.16 * np.clip(hwv, 0, 1)
    ao *= 1 - 0.38 * np.exp(-((Wd - w_seam) / 0.034) ** 2)
    ao *= 1 - 0.22 * np.exp(-((W_ST - Wd) / 0.10) ** 2) * (Wd < W_ST)
    ao *= 1 - 0.12 * np.exp(-((Wd - (W_ST + S_BEZ * 0.4)) / 0.05) ** 2)
    ao *= 1 - 0.18 * (1 - sstep(0.0, 0.03, dside))
    ao *= 1 - 0.15 * fr * (1 - stripes)
    ao *= 1 - 0.25 * (1 - sstep(0.0, 0.006, -d_st)) * a_st
    rough = 0.88 + 0.05 * vnoise(X * 9, Wd * 9, sd0 + 12) - 0.04 * np.clip(hwv, 0, 1)
    rough = rough * (1 - ink) + 0.70 * ink
    rough = rough * (1 - a_st) + 0.74 * a_st
    return col, H, rough, ao


def rope_pattern(S_, TH):
    """Z-laid 2-ply jute rope. S_ along (studs), TH around (0..2pi). The last 0.15 studs of the strip = frayed brush."""
    P = 0.40
    r = ROPE_R
    psi = TH - 2 * np.pi * S_ / P
    beta = np.mod(psi, np.pi) - np.pi / 2
    ply = np.clip(np.cos(beta), 0, 1) ** 0.55
    which = np.mod(np.floor(psi / np.pi), 2)
    arc = TH * r
    ca, sa = math.cos(math.radians(24)), math.sin(math.radians(24))

    def fib_noise(a):
        q = -S_ * sa + a * ca
        al = S_ * ca + a * sa
        return vnoise(q * 260, al * 9, 61) * 0.6 + vnoise(q * 120, al * 4, 62) * 0.4

    w = sstep(2 * np.pi - 0.7, 2 * np.pi, TH)
    fib = fib_noise(arc) * (1 - w) + fib_noise(arc - 2 * np.pi * r) * w
    hair = _hash(np.floor((-S_ * sa + arc * ca) * 260).astype(np.int64), 3, 63)
    c_dark, c_mid, c_light = L3((66, 47, 30)), L3((138, 103, 62)), L3((182, 144, 92))
    col = c_dark[None, :] + (c_mid - c_dark)[None, :] * sstep(0.0, 0.55, ply)[:, None]
    col = col + (c_light - col) * (0.5 * sstep(0.6, 1.0, ply) * (0.5 + 0.5 * fib))[:, None]
    col *= (1 + 0.18 * fib)[:, None] * (1 - 0.07 * which)[:, None]
    col *= np.where(hair < 0.06, 0.62, 1.0)[:, None]
    H = 0.024 * ply + 0.004 * fib
    ao = 0.42 + 0.58 * sstep(0.0, 0.65, ply)
    rough = 0.9 - 0.05 * fib
    # frayed brush at the end of the strip: straight unravelled fibres, lighter
    fz = sstep(L_STRIP - 0.17, L_STRIP - 0.08, S_)
    fb = vnoise(S_ * 3, TH / (2 * np.pi) * 40, 64, py=40)
    col_f = c_mid[None, :] * (1.15 + 0.3 * fb)[:, None]
    col = col + (col_f - col) * fz[:, None]
    H = H * (1 - fz) + 0.006 * fb * fz
    ao = ao * (1 - fz) + (0.85 + 0.1 * fb) * fz
    return col, H, rough, ao


def bat_paper(xb, zb, pix):
    """Paper bat (black card), viewer coords in studs."""
    col = L3((30, 27, 34))[None, :] * (1 + 0.07 * fbm2(xb * 60, zb * 60, 3, 41))[:, None]
    S = BAT_S
    bones = np.full(np.shape(xb), 1e9)
    for sg in (-1, 1):
        wr = (sg * 0.565 * S, 0.43 * S)
        for tx, ty in ((1.0, 0.31), (0.80, -0.03), (0.58, -0.21), (0.35, -0.22)):
            bones = np.minimum(bones, sd_capsule(xb, zb, wr[0], wr[1], sg * tx * S, ty * S, 0.0035))
        bones = np.minimum(bones, sd_capsule(xb, zb, wr[0], wr[1], sg * 0.16 * S, 0.06 * S, 0.0045))
    a = np.clip(0.5 - bones / pix, 0, 1)
    col = col * (1 - 0.8 * a)[:, None] + L3((62, 58, 70))[None, :] * (0.8 * a)[:, None]
    eye = [(0.03, 0.075), (0.085, 0.10), (0.075, 0.055)]
    e = np.minimum(sd_poly(xb / S, zb / S, eye), sd_poly(xb / S, zb / S, [(-x, y) for x, y in eye])) * S
    ae = np.clip(0.5 - e / pix, 0, 1)
    col = col * (1 - ae)[:, None] + L3((214, 120, 30))[None, :] * ae[:, None]
    H = 0.0008 * fbm2(xb * 80, zb * 80, 3, 42) + 0.0016 * np.sqrt(np.clip(-bones / 0.0035, 0, 1))
    rough = 0.58 + 0.04 * fbm2(xb * 30, zb * 30, 2, 43)
    ao = np.ones_like(xb)
    return col, H, rough, ao


def pumpkin_felt(px, py, pix):
    """Felt pumpkin ornament; px = longitude arc (studs, + = viewer's right), py = latitude arc (studs)."""
    phi = px / R_P
    lat = py / RZ_P
    col = L3((214, 100, 28))[None, :] * np.ones((px.shape[0], 1), np.float32)
    groove = np.abs(np.sin(4 * phi)) ** 6
    fuzz = fbm2(px * 90, py * 90, 3, 51)
    col *= ((1 - 0.32 * groove) * (1 + 0.08 * fuzz))[:, None]
    col = col + (L3((96, 82, 36)) - col) * sstep(0.95, 1.4, lat)[:, None]
    col = col * (1 - 0.25 * sstep(-0.9, -1.5, lat))[:, None]
    eye = [(0.025, 0.035), (0.125, 0.085), (0.105, 0.0)]
    f = np.minimum(sd_poly(px, py, eye), sd_poly(px, py, [(-x, y) for x, y in eye]))
    f = np.minimum(f, sd_poly(px, py, [(-0.022, -0.035), (0.022, -0.035), (0.0, 0.005)]))
    mouth = PK.grin(0.15, (-0.065, 0.025), (-0.12, 0.055), top_teeth=[(-0.05, 0.035, 0.006, 0.03),
                    (0.05, 0.035, 0.006, 0.03)], bot_teeth=[(0.0, 0.035, 0.006, 0.03)], corner_up=0.015,
                    step=0.008, jit=0.001, seed=5)
    f = np.minimum(f, sd_poly(px, py, mouth))
    a = np.clip(0.5 - f / pix, 0, 1)
    col = col * (1 - a)[:, None] + L3((26, 22, 24))[None, :] * a[:, None]
    H = 0.0015 * fuzz - 0.008 * groove + 0.0018 * np.sqrt(np.clip(-f / 0.01, 0, 1))
    rough = np.full(px.shape, 0.95)
    ao = 1 - 0.3 * groove
    return col, H, rough, ao


def lin_to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def write_png(arr, name, colorspace):
    """arr: (N, N, 3) values to store as-is (0-1), row 0 = bottom (Blender order)."""
    n = arr.shape[0]
    img = bpy.data.images.new(name, n, n, alpha=False)
    img.colorspace_settings.name = colorspace
    rgba = np.ones((n, n, 4), np.float32)
    rgba[..., :3] = arr
    img.pixels.foreach_set(rgba.ravel())
    path = os.path.join(MAPS, name + ".png")
    save_png(img, path)
    return path


def make_textures():
    t0 = time.time()
    N = ATLAS * SS
    pix = 1.0 / (D * SS)
    alb = np.zeros((N, N, 3), np.float32)
    alb[:] = L3((58, 52, 58))
    Hh = np.zeros((N, N), np.float32)
    rough = np.full((N, N), 0.9, np.float32)
    ao = np.ones((N, N), np.float32)
    best = np.full((N, N), 1e9, np.float32)
    owner = np.full((N, N), -1, np.int32)

    def grid(x0, x1, y0, y1):
        i0, i1 = max(0, int(math.floor(x0 * SS))), min(N, int(math.ceil(x1 * SS)))
        j0, j1 = max(0, int(math.floor(y0 * SS))), min(N, int(math.ceil(y1 * SS)))
        U, V = np.meshgrid((np.arange(i0, i1) + 0.5) / SS, (np.arange(j0, j1) + 0.5) / SS)
        return (slice(j0, j1), slice(i0, i1)), U, V

    def claim(oid, sl, sd, limit):
        b = best[sl]
        o = owner[sl]
        m = (sd < b) & (sd < limit)
        b[m] = sd[m]
        o[m] = oid

    def paint(oid, sl, fn, *coords):
        m = owner[sl] == oid
        if not m.any():
            return
        c, h, r, a = fn(*[q[m] for q in coords])
        alb[sl][m] = c
        Hh[sl][m] = h
        rough[sl][m] = r
        ao[sl][m] = a

    outline = [(0.0, 0.0), (HW, W_ST), (HW, W_TOP), (-HW, W_TOP), (-HW, W_ST)]
    pad = 14.0
    flag_cache = {}
    for k in range(len(DESIGNS)):
        isl = flag_island(k)
        x0, x1 = isl["cx"] - HW * D - pad, isl["cx"] + HW * D + pad
        y0, y1 = isl["y0"] - pad, isl["y0"] + W_TOP * D + pad
        sl, U, V = grid(x0, x1, y0, y1)
        X = isl["o"] * (U - isl["cx"]) / D
        Wd = (V - isl["y0"]) / D if isl["o"] > 0 else W_TOP - (V - isl["y0"]) / D
        sd = sd_poly(X, Wd, outline)
        claim(k, sl, sd, 0.075)
        flag_cache[k] = (sl, X, Wd)
    # bat island
    _r, bat_full = bat_outline(0.0)
    bat_pts = [(x * BAT_S, y * BAT_S) for x, y in bat_full]
    sl, U, V = grid(BAT_C[0] - 0.5 * D - pad, BAT_C[0] + 0.5 * D + pad, BAT_C[1] - 0.25 * D - pad, BAT_C[1] + 0.25 * D + pad)
    xb, zb = (U - BAT_C[0]) / D, (V - BAT_C[1]) / D
    claim(101, sl, sd_poly(xb, zb, bat_pts), 0.06)
    bat_cache = (sl, xb, zb)
    # pumpkin island (front half unwrap)
    hx, hy = math.pi / 2 * R_P, math.pi / 2 * RZ_P
    sl, U, V = grid(PUMP_C[0] - hx * D - pad, PUMP_C[0] + hx * D + pad, PUMP_C[1] - hy * D - pad, PUMP_C[1] + hy * D + pad)
    px, py = (U - PUMP_C[0]) / D, (V - PUMP_C[1]) / D
    claim(102, sl, np.maximum(np.abs(px) - hx, np.abs(py) - hy), 0.05)
    pump_cache = (sl, px, py)
    # patches
    for oid, patch in ((103, STEM_PATCH), (104, THREAD_PATCH)):
        sl, U, V = grid(*[patch[0], patch[2], patch[1], patch[3]])
        claim(oid, sl, np.full(U.shape, -1.0, np.float32), 1.0)
    # rope strip (periodic around: pad rows wrap naturally)
    sl, U, V = grid(ROPE_UX0 - 6, ROPE_UX0 + L_STRIP * D + 6, ROPE_Y0 - 6, ROPE_Y0 + ROPE_HS + 6)
    S_ = np.clip((U - ROPE_UX0) / D, 0, L_STRIP)
    TH = np.mod((V - ROPE_Y0) / ROPE_HS * 2 * np.pi, 2 * np.pi)
    claim(100, sl, np.full(U.shape, -1.0, np.float32), 1.0)
    rope_cache = (sl, S_, TH)
    t1 = time.time()
    # paint
    for k, (sl, X, Wd) in flag_cache.items():
        paint(k, sl, lambda a, b: flag_pattern(a, b, DESIGNS[k], pix), X, Wd)
    sl, xb, zb = bat_cache
    paint(101, sl, lambda a, b: bat_paper(a, b, pix), xb, zb)
    sl, px, py = pump_cache
    paint(102, sl, lambda a, b: pumpkin_felt(a, b, pix), px, py)
    sl, S_, TH = rope_cache
    paint(100, sl, rope_pattern, S_, TH)
    for oid, patch, c, r in ((103, STEM_PATCH, (80, 74, 34), 0.9), (104, THREAD_PATCH, (34, 32, 36), 0.7)):
        x0, y0, x1, y1 = [int(round(v * SS)) for v in patch]
        alb[y0:y1, x0:x1] = L3(c)
        rough[y0:y1, x0:x1] = r
    # normal map from the height field (UV space == tangent space: islands are rotated, never mirrored)
    gx = np.zeros_like(Hh)
    gy = np.zeros_like(Hh)
    gx[:, 1:-1] = (Hh[:, 2:] - Hh[:, :-2]) / (2 * pix)
    gy[1:-1, :] = (Hh[2:, :] - Hh[:-2, :]) / (2 * pix)
    nrm = np.stack([-gx, -gy, np.ones_like(Hh)], -1)
    nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)

    def down(a):
        return a.reshape(ATLAS, SS, ATLAS, SS, *a.shape[2:]).mean((1, 3))

    alb_f = down(alb * ao[..., None] ** 0.9)
    nrm_f = down(nrm)
    nrm_f /= np.linalg.norm(nrm_f, axis=-1, keepdims=True)
    rough_f = down(rough)
    ao_f = down(ao)
    paths = dict(
        albedo=write_png(lin_to_srgb(alb_f), "Garland_albedo", "sRGB"),
        normal=write_png(nrm_f * 0.5 + 0.5, "Garland_normal", "Non-Color"),
        rough=write_png(np.repeat(rough_f[..., None], 3, -1), "Garland_rough", "Non-Color"),
        ao=write_png(np.repeat(ao_f[..., None], 3, -1), "Garland_ao", "Non-Color"))
    return dict(paths=paths, setup_s=round(t1 - t0, 1), total_s=round(time.time() - t0, 1))


# ------------------------------------------------------------------ geometry
def catenary_c(a, d):
    lo, hi = 1e-3, 1e6
    for _ in range(200):
        c = 0.5 * (lo + hi)
        if c * math.cosh(a / c) - c > d:
            lo = c
        else:
            hi = c
    return 0.5 * (lo + hi)


class Rope:
    def __init__(self, a, d):
        self.a, self.d = a, d
        self.c = catenary_c(a, d)
        self.L = 2 * self.c * math.sinh(a / self.c)

    def x_of(self, s):
        return self.c * math.asinh(s / self.c - math.sinh(self.a / self.c))

    def p(self, s):
        x = self.x_of(s)
        return Vector((x, 0.0, self.c * math.cosh(x / self.c) - self.c - self.d))

    def beta(self, s):
        return math.atan(math.sinh(self.x_of(s) / self.c))

    def tan(self, s):
        b = self.beta(s)
        return Vector((math.cos(b), 0.0, math.sin(b)))


class MB:
    def __init__(self):
        self.bm = bmesh.new()
        self.uv = self.bm.loops.layers.uv.new("UVMap")

    def v(self, p):
        return self.bm.verts.new(p)

    def f(self, vs, uvs, ref=None, smooth=True):
        if ref is not None:
            nrm = (vs[1].co - vs[0].co).cross(vs[2].co - vs[0].co)
            if nrm.dot(ref) < 0:
                vs, uvs = vs[::-1], uvs[::-1]
        try:
            face = self.bm.faces.new(vs)
        except ValueError:
            return None
        for lp, uv in zip(face.loops, uvs):
            lp[self.uv].uv = uv
        face.smooth = smooth
        return face


def zip_rows(ax, bx):
    """Triangles between two rows sorted by x: list of ((row, idx), (row, idx), (row, idx))."""
    i = j = 0
    tris = []
    while i < len(ax) - 1 or j < len(bx) - 1:
        if j == len(bx) - 1 or (i < len(ax) - 1 and ax[i + 1] <= bx[j + 1]):
            tris.append((("A", i), ("B", j), ("A", i + 1)))
            i += 1
        else:
            tris.append((("A", i), ("B", j), ("B", j + 1)))
            j += 1
    return tris


def build_flag(mb, rope, s_c, isl, rng):
    P0 = rope.p(s_c)
    beta = rope.beta(s_c)
    t = Vector((math.cos(beta), 0.0, math.sin(beta)))
    dn = Vector((math.sin(beta), 0.0, -math.cos(beta)))
    es, up = -t, -dn
    Yv = Vector((0.0, 1.0, 0.0))
    prm = dict(tilt=rng.uniform(-0.02, 0.07), A=rng.uniform(0.06, 0.10), lam=rng.uniform(1.2, 1.9),
               ph=rng.uniform(0, 2 * math.pi), kap=rng.uniform(-1.2, 1.2), B=rng.uniform(-0.05, 0.10),
               E=rng.uniform(0.02, 0.10), C=rng.uniform(-0.12, 0.18), Tw=rng.uniform(-0.14, 0.14), shear=0.35,
               F=rng.uniform(0.03, 0.055), fa=rng.choice((-1, 1)) * rng.uniform(0.6, 1.0), fl=rng.uniform(0.9, 1.3),
               fp=rng.uniform(0, 2 * math.pi))

    def disp(xp, w):
        dl = W_ST - w
        if dl <= 0:
            return 0.0
        r = smoothstep(0.0, 0.7, dl)
        hwv = max(1e-4, HW * min(1.0, w / W_ST))
        a = max(-1.0, min(1.0, xp / hwv))
        y = dl * math.tan(prm["tilt"])
        y += prm["A"] * r * math.sin(2 * math.pi * xp / prm["lam"] + prm["ph"] + prm["kap"] * dl)
        y += prm["B"] * r * (1 - a * a) * math.sin(math.pi * min(dl, W_ST) / W_ST)
        y += prm["E"] * r * abs(a) ** 3 * (dl / W_ST)
        y += prm["C"] * smoothstep(1.5, W_ST, dl) ** 2
        y += prm["Tw"] * xp * smoothstep(0.9, W_ST, dl)
        # a diagonal drape ripple running down from one hem corner
        y += prm["F"] * r * math.sin(2 * math.pi * (xp * math.cos(prm["fa"]) + dl * math.sin(prm["fa"])) / prm["fl"]
                                     + prm["fp"])
        if y < -0.22:   # soft limit: never closer than ~0.26 to the wall (y = -0.6)
            y = -0.22 - 0.12 * math.tanh((-0.22 - y) / 0.12)
        return y

    def pos(xp, w, yoff):
        dl = max(0.0, W_ST - w)
        p = P0 + es * xp + dn * (TIP - w)
        p.x -= prm["shear"] * dl * math.sin(beta)
        p.y = yoff + disp(xp, w)
        return p

    R = ROWS
    rf, rb, rxw = [], [], []
    for r in range(R + 1):
        w = W_ST * r / R
        xs = [0.0] if r == 0 else [HW * (r / R) * (-1 + 2 * j / r) for j in range(r + 1)]
        f_row, b_row, xw_row = [], [], []
        for xp in xs:
            jx = jw = 0.0
            if r <= 2:   # raw, slightly frayed cut at the tip
                jx, jw = rng.uniform(-0.012, 0.012), rng.uniform(-0.012, 0.008)
            xw_row.append((xp + jx, w + jw))
            f_row.append(mb.v(pos(xp + jx, w + jw, T)))
            b_row.append(mb.v(pos(xp + jx, w + jw, 0.0)))
        rf.append(f_row)
        rb.append(b_row)
        rxw.append(xw_row)
    for r in range(R):
        tris = [(("A", j), ("B", j), ("B", j + 1)) for j in range(r + 1)] + \
               [(("A", j), ("B", j + 1), ("A", j + 1)) for j in range(r)]
        for tri in tris:
            pick = lambda rows, k, j: rows[r][j] if k == "A" else rows[r + 1][j]
            vf = [pick(rf, k, j) for k, j in tri]
            vb = [pick(rb, k, j) for k, j in tri]
            xw = [pick(rxw, k, j) for k, j in tri]
            mb.f(vf, [flag_uv(isl, x, w) for x, w in xw], ref=Yv)
            mb.f(vb, [flag_uv(isl, -x, w) for x, w in xw], ref=-Yv)
    # the hem roll (sleeve) around the rope + the folded-back strip
    ss = sleeve_samples()
    ncol = 4
    sx = [HW * (-1 + 2 * m / ncol) for m in range(ncol + 1)]
    rows = [rf[R]]
    xrows = [[x for x, _ in rxw[R]]]
    for s in ss[1:]:
        yz = sleeve_at(s)
        row = []
        for xp in sx:
            p = P0 + es * xp + up * yz.y
            p.y = yz.x
            row.append(mb.v(p))
        rows.append(row)
        xrows.append(sx)

    def suv(xp, s):
        if s <= S_TOP + 1e-9:
            return flag_uv(isl, xp, W_ST + s)
        return flag_uv(isl, -xp, W_ST + 2 * S_TOP - s)

    for k in range(len(ss) - 1):
        s0, s1 = ss[k], ss[k + 1]
        back = s1 > S_TOP + 1e-9
        for tri in zip_rows(xrows[k], xrows[k + 1]):
            vs, uvs = [], []
            for rr, j in tri:
                kk = k if rr == "A" else k + 1
                vs.append(rows[kk][j])
                sv = s0 if rr == "A" else s1
                uvs.append(suv(xrows[kk][j], sv) if not back else flag_uv(isl, -xrows[kk][j], W_ST + 2 * S_TOP - sv))
            c = sum((q.co for q in vs), Vector()) / 3
            if s0 >= 2 * S_TOP - 1e-9:
                ref = -Yv
            else:
                rel = c - P0
                ref = rel - es * rel.dot(es)
            mb.f(vs, uvs, ref=ref)
    # a few loose threads at the frayed tip
    for k in range(3):
        if k == 0:
            side, w0 = 0, 0.0
        else:
            side, w0 = (-1 if k == 1 else 1), rng.uniform(0.05, 0.32)
        xp0 = side * HW * w0 / W_ST * 0.97
        dx, dw = side * 0.55 + rng.uniform(-0.25, 0.25), -1.0
        Ld = math.hypot(dx, dw)
        dx, dw = dx / Ld, dw / Ld
        ln = rng.uniform(0.07, 0.15)
        px_, pw_ = -dw, dx
        quad = [(xp0 + px_ * 0.009, w0 + pw_ * 0.009), (xp0 - px_ * 0.009, w0 - pw_ * 0.009),
                (xp0 + dx * ln - px_ * 0.004, w0 + dw * ln - pw_ * 0.004),
                (xp0 + dx * ln + px_ * 0.004, w0 + dw * ln + pw_ * 0.004)]
        uvq = [flag_uv(isl, xp0 * 0.9, max(w0, 0.05) + 0.02)] * 4
        for yoff, ref in ((T * 0.5 + 0.003, Yv), (T * 0.5 - 0.003, -Yv)):
            vq = [mb.v(pos(x, w, yoff)) for x, w in quad]
            mb.f([vq[0], vq[1], vq[2]], uvq[:3], ref=ref)
            mb.f([vq[0], vq[2], vq[3]], uvq[:3], ref=ref)


def tube(mb, pts, radii, sides, us, vrange, cap=False, n1=None):
    n = len(pts)
    tans = [(pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized() for i in range(n)]
    if n1 is None:
        ref = Vector((0, 1, 0)) if abs(tans[0].y) < 0.9 else Vector((1, 0, 0))
        n1 = ref - tans[0] * ref.dot(tans[0])
    n1 = n1.normalized()
    rings = []
    for i in range(n):
        t = tans[i]
        n1 = (n1 - t * n1.dot(t)).normalized()
        n2 = n1.cross(t)
        rings.append([mb.v(pts[i] + (n1 * math.cos(2 * math.pi * j / sides) + n2 * math.sin(2 * math.pi * j / sides))
                           * radii[i]) for j in range(sides)])
    v0, v1 = vrange
    for i in range(n - 1):
        for j in range(sides):
            j2 = (j + 1) % sides
            va, vb = v0 + (v1 - v0) * j / sides, v0 + (v1 - v0) * (j + 1) / sides
            q = [rings[i][j], rings[i + 1][j], rings[i + 1][j2], rings[i][j2]]
            uq = [(us[i], va), (us[i + 1], va), (us[i + 1], vb), (us[i], vb)]
            fc = sum((x.co for x in q), Vector()) / 4
            ref = fc - (pts[i] + pts[i + 1]) / 2
            mb.f([q[0], q[1], q[2]], [uq[0], uq[1], uq[2]], ref=ref)
            mb.f([q[0], q[2], q[3]], [uq[0], uq[2], uq[3]], ref=ref)
    if cap:
        tipp = pts[-1] + tans[-1] * radii[-1] * 0.55
        tv = mb.v(tipp)
        for j in range(sides):
            j2 = (j + 1) % sides
            va, vb = v0 + (v1 - v0) * j / sides, v0 + (v1 - v0) * (j + 1) / sides
            mb.f([rings[-1][j], rings[-1][j2], tv], [(us[-1], va), (us[-1], vb), (us[-1] + 0.004, (va + vb) / 2)],
                 ref=tans[-1])
    return rings


ROPE_VR = (ROPE_Y0 / ATLAS, (ROPE_Y0 + ROPE_HS) / ATLAS)


def end_path(rope, s_start, rng):
    """Right-hand rope end: catenary out of the last sleeve -> blend -> 1.4 turns round the hook arm -> knot -> tail."""
    L, a = rope.L, rope.a
    s_bl = L - 0.32
    n = max(2, int(math.ceil((s_bl - s_start) / 0.5)))
    pts = [rope.p(s_start + (s_bl - s_start) * k / n) for k in range(n + 1)]
    rad = [ROPE_R] * len(pts)
    be = rope.beta(L)
    C = Vector((a, 0.0, ARM_Z))
    th0 = math.pi / 2 + be
    Pt = C + Vector((math.cos(th0), 0.0, math.sin(th0))) * WRAP_R
    tq = rope.tan(s_bl)
    tc = Vector((math.sin(th0), 0.0, -math.cos(th0)))
    ch = (Pt - pts[-1]).length
    q0 = pts[-1].copy()
    for k in (1, 2):
        pts.append(_hermite(q0, tq * ch, Pt, tc * ch, k / 2))
        rad.append(ROPE_R)
    sweep, nw = math.radians(510), 15
    for k in range(1, nw + 1):
        th = th0 - sweep * k / nw
        pts.append(Vector((C.x + WRAP_R * math.cos(th), WRAP_DY * k / nw, C.z + WRAP_R * math.sin(th))))
        rad.append(ROPE_R)
    the = th0 - sweep
    E = pts[-1].copy()
    te = Vector((math.sin(the), 0.0, -math.cos(the)))
    tl = rng.uniform(0.40, 0.50)
    E2 = E + Vector((-0.10, 0.0, -tl))
    nt = 6
    for k in range(1, nt + 1):
        f = k / nt
        q = _hermite(E, te * 0.35, E2, Vector((0, 0, -1)) * 0.35, f)
        q.y = WRAP_DY
        knot = math.exp(-((f - 0.2) / 0.1) ** 2)
        pts.append(q)
        rad.append(ROPE_R * (1 + 0.42 * knot))
    rad[-1] = ROPE_R * 1.18   # frayed brush flares
    return pts, rad


def build_rope(mb, rope, s_cs, rng):
    for i in range(len(s_cs) - 1):
        s0, s1 = s_cs[i] + HW - 0.3, s_cs[i + 1] - HW + 0.3
        ss = [s0 + (s1 - s0) * k / 3 for k in range(4)]
        off = rng.uniform(0.0, L_STRIP - 0.4 - (s1 - s0))
        tube(mb, [rope.p(s) for s in ss], [ROPE_R] * 4, 6, [rope_uv(off + s - s0, 0)[0] for s in ss], ROPE_VR)
    for side in (1, -1):
        if side > 0:
            pts, rad = end_path(rope, s_cs[-1] + HW - 0.3, rng)
        else:   # mirror image of a right-hand end that starts at the mirrored point of the first sleeve
            pts, rad = end_path(rope, rope.L - (s_cs[0] - HW + 0.3), rng)
            pts = [Vector((-p.x, p.y, p.z)) for p in pts]
        cum = [0.0]
        for i in range(1, len(pts)):
            cum.append(cum[-1] + (pts[i] - pts[i - 1]).length)
        us = [rope_uv(L_STRIP - 0.02 - (cum[-1] - c), 0)[0] for c in cum]
        tube(mb, pts, rad, 6, us, ROPE_VR, cap=True)


def build_bat(mb, top, hang, rng):
    S = BAT_S
    right, _full = bat_outline(0.0)
    fold = math.radians(22)
    yaw = math.radians(rng.uniform(-10, 10))
    roll = math.radians(rng.uniform(-4, 4))
    origin = top - Vector((0, 0, hang + 0.15 * S))
    rot = Matrix.Rotation(yaw, 3, "Z") @ Matrix.Rotation(roll, 3, "Y")
    tris = geometry.tessellate_polygon([[Vector((x, y, 0.0)) for x, y in right]])

    def P(x, y, yoff):
        loc = Vector((x * S * math.cos(fold), abs(x) * S * math.sin(fold) + yoff, y * S))
        return origin + rot @ loc

    Yv = rot @ Vector((0, 1, 0))
    for sg in (1, -1):
        pts = [(sg * x, y) for x, y in right]
        for yoff, ref, mirror in ((0.006, Yv, 1), (-0.006, -Yv, -1)):
            vs = [mb.v(P(x, y, yoff)) for x, y in pts]
            for a, b, c in tris:
                tri = [vs[a], vs[b], vs[c]]
                uvs = [((BAT_C[0] - mirror * pts[i][0] * S * D) / ATLAS, (BAT_C[1] + pts[i][1] * S * D) / ATLAS)
                       for i in (a, b, c)]
                mb.f(tri, uvs, ref=ref, smooth=False)
    a0 = origin + rot @ Vector((0, 0, 0.15 * S))
    tube(mb, [top + Vector((0, 0.0, -0.02)), a0], [0.011, 0.011], 3,
         [patch_uv(THREAD_PATCH, 0, 0)[0], patch_uv(THREAD_PATCH, 1, 0)[0]],
         (patch_uv(THREAD_PATCH, 0, 0)[1], patch_uv(THREAD_PATCH, 0, 1)[1]))


def build_pumpkin(mb, top, hang, rng):
    yaw = math.radians(rng.uniform(-14, 14))
    rot = Matrix.Rotation(yaw, 3, "Z")
    stem_len = 0.10
    ztop = RZ_P * 0.70
    centre = top - Vector((0, 0, hang + stem_len + ztop))
    lats = [-60, -30, 0, 30, 60]
    nl = 16
    phis = [-180 + 22.5 * k for k in range(nl)]

    def P(phi_d, lat_d):
        ph, la = math.radians(phi_d), math.radians(lat_d)
        groove = 1.0 if (round((phi_d + 180) / 22.5) % 2) else 0.0
        rr = R_P * (1 - 0.08 * groove) * math.cos(la) ** 0.85
        z = RZ_P * math.sin(la)
        if lat_d >= 60:
            z *= 0.88
        return centre + rot @ Vector((-math.sin(ph) * rr, math.cos(ph) * rr, z))

    def uvp(phi_d, lat_d, back):
        phm = phi_d if not back else (math.copysign(180.0, phi_d if phi_d != 0 else 1) - phi_d)
        if back and abs(phi_d) == 180:
            phm = 0.0
        return ((PUMP_C[0] + math.radians(phm) * R_P * D) / ATLAS, (PUMP_C[1] + math.radians(lat_d) * RZ_P * D) / ATLAS)

    rings = [[mb.v(P(ph, la)) for ph in phis] for la in lats]
    vtop = mb.v(centre + rot @ Vector((0, 0, ztop)))
    vbot = mb.v(centre + rot @ Vector((0, 0, -RZ_P * 0.86)))
    for li in range(len(lats) - 1):
        for k in range(nl):
            k2 = (k + 1) % nl
            pa, pb = phis[k], phis[k] + 22.5
            back = not (-90 <= pa and pb <= 90)
            q = [rings[li][k], rings[li][k2], rings[li + 1][k2], rings[li + 1][k]]
            uq = [uvp(pa, lats[li], back), uvp(pb, lats[li], back), uvp(pb, lats[li + 1], back), uvp(pa, lats[li + 1], back)]
            ref = sum((x.co for x in q), Vector()) / 4 - centre
            mb.f([q[0], q[1], q[2]], uq[:3], ref=ref)
            mb.f([q[0], q[2], q[3]], [uq[0], uq[2], uq[3]], ref=ref)
    for k in range(nl):
        k2 = (k + 1) % nl
        pa, pb = phis[k], phis[k] + 22.5
        back = not (-90 <= pa and pb <= 90)
        mid = (pa + pb) / 2
        for ring, pole, la_r, la_p in ((rings[-1], vtop, 60, 90), (rings[0], vbot, -60, -90)):
            tri = [ring[k], ring[k2], pole]
            uvs = [uvp(pa, la_r, back), uvp(pb, la_r, back), uvp(mid, la_p * 0.97, back)]
            ref = sum((x.co for x in tri), Vector()) / 3 - centre
            mb.f(tri, uvs, ref=ref)
    # stem + the twine it hangs by
    s0 = centre + rot @ Vector((0, 0, ztop - 0.02))
    s1 = centre + rot @ Vector((0.025, 0.01, ztop + stem_len))
    su = [patch_uv(STEM_PATCH, 0, 0)[0], patch_uv(STEM_PATCH, 1, 0)[0]]
    tube(mb, [s0, s1], [0.036, 0.028], 5, su, (patch_uv(STEM_PATCH, 0, 0)[1], patch_uv(STEM_PATCH, 0, 1)[1]), cap=True)
    tube(mb, [s1 - Vector((0, 0, 0.02)), top + Vector((0, 0, -0.02))], [0.016, 0.016], 4,
         [rope_uv(0.5, 0)[0], rope_uv(0.5 + hang, 0)[0]], ROPE_VR)


def atlas_material():
    m = bpy.data.materials.get("Garland_PBR")
    if m:
        return m
    imgs = {}
    for key, cs in (("albedo", "sRGB"), ("normal", "Non-Color"), ("rough", "Non-Color")):
        img = bpy.data.images.load(os.path.join(MAPS, f"Garland_{key}.png"), check_existing=True)
        img.colorspace_settings.name = cs
        imgs[key] = img
    tmp = link(bpy.data.objects.new("_tmp", bpy.data.meshes.new("_tmp")))
    pbr_material(tmp, "Garland_PBR", imgs)
    m = tmp.data.materials[0]
    bpy.data.objects.remove(tmp)
    return m


def build_garland(name):
    G = GARLANDS[name]
    rope = Rope(G["a"], G["d"])
    mb = MB()
    n = len(G["flags"])
    s_cs = [rope.L / 2 + (i - (n - 1) / 2) * G["pitch"] for i in range(n)]
    for i, k in enumerate(G["flags"]):
        build_flag(mb, rope, s_cs[i], flag_island(k), random.Random(G["seed"] * 100 + i))
    nv_flags = len(mb.bm.verts)
    rng = random.Random(G["seed"])
    build_rope(mb, rope, s_cs, rng)
    nv_rope = len(mb.bm.verts)
    tie = {}
    for kind, gap, hang in G["extras"]:
        # the pennants hang perpendicular to the sloped rope, so the gap between them drifts sideways with depth:
        # tie the extra on where it will hang centred in the gap at its own depth
        s_mid = (s_cs[gap] + s_cs[gap + 1]) / 2
        h_mid = hang + (0.1 if kind == "bat" else 0.35)
        top = rope.p(s_mid + 0.85 * h_mid * math.sin(rope.beta(s_mid)))
        tie[kind] = [round(v, 3) for v in top]
        (build_bat if kind == "bat" else build_pumpkin)(mb, top, hang, rng)
    # clearance: dangling extras vs pennants, and pennant cloth vs the wall plane
    from mathutils import kdtree
    mb.bm.verts.ensure_lookup_table()
    kd = kdtree.KDTree(nv_flags)
    for i in range(nv_flags):
        kd.insert(mb.bm.verts[i].co, i)
    kd.balance()
    clear = min(kd.find(mb.bm.verts[i].co)[2] for i in range(nv_rope, len(mb.bm.verts)))
    ymin_flags = min(mb.bm.verts[i].co.y for i in range(nv_flags))
    bmesh.ops.triangulate(mb.bm, faces=mb.bm.faces[:], quad_method="BEAUTY", ngon_method="BEAUTY")
    ob = obj_from_bm(mb.bm, name, smooth=False)
    ob.data.materials.append(atlas_material())
    info = dict(tris=len(ob.data.polygons), arc_len=round(rope.L, 3), c=round(rope.c, 3),
                extras_to_flags_min=round(clear, 3), flags_min_y=round(ymin_flags, 3), extras_tie=tie,
                flag_designs=[DESIGNS[k]["name"] for k in G["flags"]],
                flag_centres_s=[round(s, 3) for s in s_cs],
                flag_centres_xyz=[[round(v, 3) for v in rope.p(s)] for s in s_cs])
    return ob, info


# ------------------------------------------------------------------ the hook (kit pipeline: hi sculpt -> bake)
def hook_path(dense):
    """Arm centre line (x = 0): out of the wall plate along +Y at z = ARM_Z, then an upturned J with a short scroll."""
    pts, tw = [], []
    y0, y1 = -0.56, 0.44
    n = 40 if dense else 14
    for k in range(n + 1):
        f = k / n
        y = y0 + (y1 - y0) * f
        pts.append(Vector((0.0, y, ARM_Z)))
        tw.append(2 * math.pi * sstep(-0.42, 0.26, np.array(y)).item())
    cr, cz = 0.085, ARM_Z + 0.085
    m = 30 if dense else 8
    for k in range(1, m + 1):
        ph = math.radians(215) * k / m
        rr = cr - 0.02 * max(0.0, (ph - math.pi) / math.radians(35))
        pts.append(Vector((0.0, y1 + rr * math.sin(ph), cz - rr * math.cos(ph))))
        tw.append(tw[-1])
    return pts, tw


def square_sweep(pts, tw, half, ring_fn, name, dense):
    """Sweep a (twisted) square bar. ring_fn(i) -> half-size scale. Returns an object (hi: rounded corners)."""
    bm = bmesh.new()
    n = len(pts)
    tans = [(pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized() for i in range(n)]
    n1 = Vector((1, 0, 0))
    prof = []
    if dense:
        for k in range(24):     # rounded square (superellipse)
            a = 2 * math.pi * k / 24 + math.pi / 4
            c, s = math.cos(a), math.sin(a)
            e = 0.16
            prof.append((math.copysign(abs(c) ** e, c), math.copysign(abs(s) ** e, s)))
    else:
        prof = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    rings = []
    cols = []
    for i in range(n):
        t = tans[i]
        n1 = (n1 - t * n1.dot(t)).normalized()
        n2 = n1.cross(t)
        ca, sa = math.cos(tw[i]), math.sin(tw[i])
        a1, a2 = n1 * ca + n2 * sa, -n1 * sa + n2 * ca
        h = half * ring_fn(i, n)
        ring = []
        for px, py in prof:
            p = pts[i] + (a1 * px + a2 * py) * h
            if dense:
                dent = 0.0025 * noise.noise(p * 38.0) + 0.0012 * noise.noise(p * 90.0)
                nn = (a1 * px + a2 * py).normalized()
                p = p + nn * dent
                corner = abs(abs(px) - abs(py)) < 0.35 and abs(px) > 0.6
                cols.append(1.0 if corner else 0.0)
            ring.append(bm.verts.new(p))
        rings.append(ring)
    m = len(prof)
    for i in range(n - 1):
        for j in range(m):
            j2 = (j + 1) % m
            f = bm.faces.new((rings[i][j], rings[i][j2], rings[i + 1][j2], rings[i + 1][j]))
    for ring, cen, d in ((rings[0], pts[0], -tans[0]), (rings[-1], pts[-1], tans[-1])):
        f = bm.faces.new(ring)
        if f.normal.dot(d) < 0:
            f.normal_flip()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = obj_from_bm(bm, name, smooth=True)
    if not dense:
        me = ob.data
        for e in me.edges:   # bar corners + end-cap rims are sharp
            ia, ib = e.vertices[0] // 4, e.vertices[1] // 4
            if ia != ib or ia in (0, n - 1):
                e.use_edge_sharp = True
    return ob, cols


def plate_outline(k_pts=16, ry=0.27, rx=0.16, concave=0.30):
    out = []
    for k in range(k_pts):
        a = 2 * math.pi * k / k_pts
        c, s = math.cos(a), math.sin(a)
        # diamond with concave sides
        r = 1.0 / (abs(c) ** (1 / (1 - concave)) + abs(s) ** (1 / (1 - concave))) ** (1 - concave)
        out.append((r * c * rx, r * s * ry))
    return out


def build_plate(name, dense):
    """Forged wall plate: a diamond with concave sides, bevelled rim, slightly domed + hammered face (hi)."""
    bm = bmesh.new()
    kk = 64 if dense else 16
    yb, yf = -0.60, -0.555
    outer = plate_outline(kk)
    back = [bm.verts.new((x, yb, ARM_Z + z)) for x, z in outer]
    fo = [bm.verts.new((x, yf - 0.012, ARM_Z + z)) for x, z in outer]
    nr = 12 if dense else 1
    rings = []
    for r in range(nr):
        k = 1.0 - r / nr
        ring = []
        for x, z in outer:
            p = Vector((x * 0.82 * k, yf + 0.004 * (1 - k * k), ARM_Z + z * 0.86 * k))
            if dense:
                p.y += 0.0016 * noise.noise(p * 32.0) + 0.0008 * noise.noise(p * 75.0)
            ring.append(bm.verts.new(p))
        rings.append(ring)
    centre = bm.verts.new((0.0, yf + 0.004, ARM_Z))
    bm.faces.new(list(reversed(back)))
    for i in range(kk):
        j = (i + 1) % kk
        bm.faces.new((back[i], back[j], fo[j], fo[i]))
        bm.faces.new((fo[i], fo[j], rings[0][j], rings[0][i]))
        for r in range(nr - 1):
            bm.faces.new((rings[r][i], rings[r][j], rings[r + 1][j], rings[r + 1][i]))
        bm.faces.new((rings[-1][i], rings[-1][j], centre))
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = obj_from_bm(bm, name, smooth=dense)
    if not dense:
        for p in ob.data.polygons:
            p.use_smooth = False
    return ob


def build_nails(name, dense):
    bm = bmesh.new()
    seg = 16 if dense else 6
    for zc in (ARM_Z + 0.185, ARM_Z - 0.185):
        base = [bm.verts.new((0.03 * math.cos(2 * math.pi * k / seg), -0.556, zc + 0.03 * math.sin(2 * math.pi * k / seg)))
                for k in range(seg)]
        mid = [bm.verts.new((0.022 * math.cos(2 * math.pi * k / seg), -0.538, zc + 0.022 * math.sin(2 * math.pi * k / seg)))
               for k in range(seg)]
        tip = bm.verts.new((0.0, -0.531, zc))
        for k in range(seg):
            j = (k + 1) % seg
            bm.faces.new((base[k], base[j], mid[j], mid[k]))
            bm.faces.new((mid[k], mid[j], tip))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for f in bm.faces:
        if f.normal.y < -0.2:
            f.normal_flip()
    return obj_from_bm(bm, name, smooth=True)


def hook_colors(ob, corner_flags=None):
    me = ob.data
    cols, rough = [], []
    for i, v in enumerate(me.vertices):
        p = v.co
        base = mix(lin((40, 38, 38)), lin((58, 52, 48)), 0.5 + 0.5 * fbm(p * 22.0, 3))
        rust = smoothstep(0.38, 0.72, fbm(p * 9.0 + Vector((3, 1, 7)), 3))
        near_wall = smoothstep(-0.50, -0.57, p.y) * (1 - smoothstep(0.10, 0.20, abs(p.z - ARM_Z) + abs(p.x)))
        rust = min(1.0, rust * 0.55 + 0.45 * near_wall * smoothstep(0.0, 0.45, fbm(p * 30.0, 2)))
        col = mix(base, lin((98, 54, 30)), 0.6 * rust)
        worn = corner_flags[i] if corner_flags else 0.0
        col = mix(col, lin((96, 92, 88)), 0.45 * worn * (1 - rust))
        r = 0.5 + 0.35 * rust - 0.15 * worn
        cols.append(col)
        rough.append((r, r, r))
    set_colors(me, "Col", cols)
    set_colors(me, "Rough", rough)
    me.materials.append(mat_vc("Iron_" + ob.name, metallic=0.0))


def build_hook():
    pts_lo, tw_lo = hook_path(False)
    pts_hi, tw_hi = hook_path(True)

    def flare(i, n):     # forged (upset) shoulder at the plate, tapered scroll end
        f = i / (n - 1)
        return 1.0 + 0.45 * max(0.0, 1 - f / 0.05) - 0.45 * smoothstep(0.85, 1.0, f)

    arm_lo, _ = square_sweep(pts_lo, tw_lo, 0.03, flare, "HookArm_lo", False)
    arm_hi, corner = square_sweep(pts_hi, tw_hi, 0.03, flare, "HookArm_hi", True)
    hook_colors(arm_hi, corner)
    plate_lo, plate_hi = build_plate("Plate_lo", False), build_plate("Plate_hi", True)
    hook_colors(plate_hi)
    nails_lo, nails_hi = build_nails("Nails_lo", False), build_nails("Nails_hi", True)
    hook_colors(nails_hi)
    for o in (arm_lo, plate_lo, nails_lo):
        only(o)
    for o in bpy.context.scene.objects:
        o.select_set(o in (arm_lo, plate_lo, nails_lo))
    bpy.context.view_layer.objects.active = arm_lo
    bpy.ops.object.join()
    lo = arm_lo
    lo.name = "Garland_Hook"
    lo.data.name = "Garland_Hook"
    bm = bmesh.new()
    bm.from_mesh(lo.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bm.to_mesh(lo.data)
    bm.free()
    smart_uv(lo, angle=60, margin=0.02)
    imgs = bake_set(lo, [arm_hi, plate_hi, nails_hi], 256, "Hook", cage=0.02, maxray=0.05, ao_strength=0.5,
                    ao_dist=0.15, outdir=MAPS)
    pbr_material(lo, "Hook_PBR", imgs)
    for o in (arm_hi, plate_hi, nails_hi):
        o.hide_render = True
        o.hide_viewport = True
    return lo, dict(tris=len(lo.data.polygons), miss=round(imgs["miss_fraction"], 4))


# ------------------------------------------------------------------ steps
def step_build():
    fresh(samples=16)
    rep = {}
    for nm in GARLANDS:
        ob, info = build_garland(nm)
        rep[nm] = info
    lo, hinfo = build_hook()
    rep["Garland_Hook"] = hinfo
    for ob in bpy.data.objects:
        if ob.type == "MESH" and not ob.hide_render:
            bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
            mn = Vector((min(v.x for v in bb), min(v.y for v in bb), min(v.z for v in bb)))
            mx = Vector((max(v.x for v in bb), max(v.y for v in bb), max(v.z for v in bb)))
            rep.setdefault(ob.name, {})["bbox_min"] = [round(v, 3) for v in mn]
            rep[ob.name]["bbox_max"] = [round(v, 3) for v in mx]
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return rep


def wall_scene(span, sag):
    """Slate-blue wall face at y = -0.6 (+ two pillars) for the reviews."""
    wall_col = lin((96, 132, 170))
    W = span + 14
    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in ((-W, -0.6, -20), (W, -0.6, -20), (W, -0.6, 12), (-W, -0.6, 12))]
    bm.faces.new(vs)
    w = obj_from_bm(bm, "Wall", smooth=False)
    w.data.materials.append(mat_noise("WallMat", wall_col, lin((88, 122, 160)), nscale=0.6, detail=3, rough=0.8,
                                      lo=0.35, hi=0.65))
    out = [w]
    for sx in (-1, 1):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co = Vector((v.co.x * 1.8 + sx * (span + 1.5), v.co.y * 1.2 - 0.1, v.co.z * 32 - 4))
        p = obj_from_bm(bm, "Pillar", smooth=False)
        p.data.materials.append(mat_flat("PillarMat", lin((84, 116, 150)), rough=0.8))
        out.append(p)
    return out


def place_hooks(a):
    src = bpy.data.objects["Garland_Hook"]
    out = []
    for sx in (-1, 1):
        o = src.copy()
        o.location = (sx * a, 0, 0)
        o.hide_render = False
        link(o)
        out.append(o)
    return out


def step_render(which=("long", "short")):
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = review_setup(res=(1600, 1000), sky=(0.36, 0.5, 0.72), sky_strength=0.9, sun=3.5)
    sun = bpy.data.objects["Sun"]
    sun.rotation_euler = Vector((-0.35, -0.85, -0.55)).to_track_quat("-Z", "Y").to_euler()   # from the front-top-left
    out = []
    long_ob, short_ob = bpy.data.objects["Garland_Long"], bpy.data.objects["Garland_Short"]
    bpy.data.objects["Garland_Hook"].hide_render = True
    if "long" in which:
        short_ob.hide_render, long_ob.hide_render = True, False
        tmp = wall_scene(13.0, 3.5) + place_hooks(13.0)
        out.append(shoot(os.path.join(OUT, "review_long_30.png"), (0, 0, -3.0), (0, 1, -0.32), 30, lens=32))
        out.append(shoot(os.path.join(OUT, "review_long_oblique.png"), (0, 0, -3.0), (0.85, 1, -0.25), 22, lens=32))
        out.append(shoot(os.path.join(OUT, "review_close.png"), (7.9, 0, -2.6), (0.25, 1, -0.2), 5.5, lens=40))
        out.append(shoot(os.path.join(OUT, "review_hook_close.png"), (12.85, 0.05, -0.3), (-0.55, 1, -0.05), 3.2, lens=50))
        out.append(shoot(os.path.join(OUT, "review_flags_10.png"), (0, 0, -4.6), (0, 1, -0.15), 10.0, lens=32))
        solo = place_hooks(20.0)
        solo[0].location = (20.0, 0.0, -2.0)
        bpy.data.objects.remove(solo[1])
        out.append(shoot(os.path.join(OUT, "review_hook_solo.png"), (20.0, -0.1, -2.1), (0.8, 1, 0.35), 1.7, lens=50))
        bpy.data.objects.remove(solo[0])
        for o in tmp:
            bpy.data.objects.remove(o)
    if "short" in which:
        short_ob.hide_render, long_ob.hide_render = False, True
        tmp = wall_scene(9.5, 2.6) + place_hooks(9.5)
        out.append(shoot(os.path.join(OUT, "review_short_30.png"), (0, 0, -2.6), (0, 1, -0.32), 30, lens=40))
        for o in tmp:
            bpy.data.objects.remove(o)
    return out


def step_export():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    rep = {}
    for nm in ("Garland_Long", "Garland_Short", "Garland_Hook"):
        rep[nm] = export_fbx([bpy.data.objects[nm]], os.path.join(CDIMP, f"Halloween_{nm}.fbx"))
    return rep


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["tex", "build"]
    rep = {}
    for step in argv:
        t0 = time.time()
        if step == "tex":
            fresh()
            rep["tex"] = make_textures()
        elif step == "build":
            rep["build"] = step_build()
        elif step == "render":
            rep["render"] = step_render()
        elif step == "export":
            rep["export"] = step_export()
        rep[step + "_s"] = round(time.time() - t0, 1)
    print("GARLAND_REPORT " + json.dumps(rep))
