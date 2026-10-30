# HubGrime - numpy painting kit for the Halloween hub grime decals (2026-10-13).
# Everything is procedural (no image sources). Layers are composited as PREMULTIPLIED LINEAR RGBA on a supersampled
# canvas, box-downsampled, then exported as STRAIGHT-alpha sRGB PNG with push-pull colour bleed under alpha 0.
# Coordinates are in STUDS. Texture space: +x right, +y DOWN (row order). "Up" on a wall = -y.
import json
import math
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ...\HubGrime
DECALS = os.path.join(HERE, "decals")

# ------------------------------------------------------------------ palette (sRGB 0-255), see PLAN.md section 3
PAL = {
    "D1": (32, 30, 22), "D2": (66, 60, 42),
    "M1": (34, 50, 24), "M2": (66, 86, 34), "M3": (96, 116, 44), "M4": (146, 166, 60), "M5": (182, 194, 86),
    "G1": (178, 156, 98), "G2": (122, 112, 66), "G3": (70, 62, 40),
    "S1": (44, 98, 20), "S2": (118, 192, 34), "S3": (170, 226, 70), "S4": (236, 255, 190), "S5": (30, 62, 16),
    "W1": (40, 58, 18), "W2": (26, 40, 10), "W3": (96, 60, 22), "W4": (30, 34, 24), "W5": (238, 232, 205),
    "SO1": (52, 74, 20), "SO2": (26, 44, 8), "SU1": (104, 64, 22), "SU2": (52, 30, 10),
    "W8": (148, 128, 98), "W9": (52, 38, 22),
    "W7": (24, 40, 16),
    # round 4 "mushier": a brighter, more saturated moss family that still reads in the live game's wall shade
    # (the back wall only gets cyan-blue sky light there), darker wet damp, wet stains with gloss
    # round 5: body ~20 % toward olive (the round-4 lime out-saturated the slime); lime only on the minority of tips
    "MM1": (56, 68, 40), "MM2": (84, 106, 50), "MM3": (122, 150, 62), "MM4": (166, 194, 80), "MM5": (204, 226, 120),
    "MD1": (88, 92, 38), "MD2": (172, 170, 78),     # round 6: yellow-olive "dying" patches (no orange)
    "WD1": (20, 36, 12), "WD2": (12, 22, 6), "SH": (196, 224, 236), "GL": (238, 248, 252),
    "SW1": (40, 72, 22), "SW2": (18, 36, 8), "SU3": (92, 52, 16), "SU4": (40, 22, 6),
}

# round 5: the final moss look, shared by MossBase, G_Moss_A/B and W_Crack_C's notch/ledge moss
MOSS_PAL_R5 = {"M1": "MM1", "M2": "MM2", "M3": "MM3", "M4": "MM4", "M5": "MM5", "W1": "WD1"}
MOSS_LOOK_R5 = dict(pal=MOSS_PAL_R5, value=0.97, tip_amt=0.58, tip_lo=0.5, dome=0.55, lump_k=0.95, dying=0.9,
                    cav_k=0.22)

# fake light, texture space (x right, y down, z out of the surface); unit vectors
L_FLOOR = np.array([-0.25, -0.45, 0.86]); L_FLOOR /= np.linalg.norm(L_FLOOR)
L_WALL = np.array([-0.2, -0.75, 0.63]); L_WALL /= np.linalg.norm(L_WALL)


def lin(c):
    c = np.asarray(c, np.float32) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4).astype(np.float32)


def P(name):
    return lin(PAL[name])


def to_srgb(x):
    x = np.clip(x, 0.0, 1.0)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def ramp(v, stops):
    """v (...,) in 0..1 -> colour (...,3); stops = [(pos, rgb_lin), ...] sorted."""
    out = np.zeros(v.shape + (3,), np.float32)
    out[...] = stops[0][1]
    for (p0, c0), (p1, c1) in zip(stops[:-1], stops[1:]):
        t = np.clip((v - p0) / max(p1 - p0, 1e-6), 0, 1)[..., None]
        m = (v >= p0)[..., None]
        out = np.where(m, c0 + (c1 - c0) * t, out)
    return out


# ------------------------------------------------------------------ noise
class Noise2:
    """Gradient noise on a lattice; optionally periodic in x (and y). u, v in lattice units."""

    def __init__(self, seed, cx, cy, wrap_x=False, wrap_y=False):
        rng = np.random.default_rng(seed)
        ang = rng.uniform(0, 2 * np.pi, (cy + 1, cx + 1))
        if wrap_x:
            ang[:, -1] = ang[:, 0]
        if wrap_y:
            ang[-1, :] = ang[0, :]
        self.gx, self.gy = np.cos(ang).astype(np.float32), np.sin(ang).astype(np.float32)
        self.cx, self.cy, self.wx, self.wy = cx, cy, wrap_x, wrap_y

    def __call__(self, u, v):
        u = np.mod(u, self.cx) if self.wx else np.clip(u, 0, self.cx - 1e-4)
        v = np.mod(v, self.cy) if self.wy else np.clip(v, 0, self.cy - 1e-4)
        i = np.floor(u).astype(np.int32)
        j = np.floor(v).astype(np.int32)
        fu, fv = u - i, v - j
        i = np.minimum(i, self.cx - 1)
        j = np.minimum(j, self.cy - 1)

        def g(jj, ii, du, dv):
            return self.gx[jj, ii] * du + self.gy[jj, ii] * dv

        n00 = g(j, i, fu, fv)
        n10 = g(j, i + 1, fu - 1, fv)
        n01 = g(j + 1, i, fu, fv - 1)
        n11 = g(j + 1, i + 1, fu - 1, fv - 1)
        su = fu * fu * fu * (fu * (fu * 6 - 15) + 10)
        sv = fv * fv * fv * (fv * (fv * 6 - 15) + 10)
        return (lerp(lerp(n00, n10, su), lerp(n01, n11, su), sv) * 1.45).astype(np.float32)


class Field:
    """fBm in stud coordinates. period_x (studs) makes it exactly periodic in x. Output roughly -1..1."""

    def __init__(self, seed, cell, octaves=3, extent=(64.0, 64.0), period_x=None, origin=(-8.0, -8.0), gain=0.5):
        self.oct = []
        self.origin = origin
        self.period_x = period_x
        amp, tot = 1.0, 0.0
        for k in range(octaves):
            if period_x:
                cx = max(1, int(round(period_x / cell))) * (2 ** k)
                cs_x = period_x / cx
            else:
                cs_x = cell / (2 ** k)
                cx = int(math.ceil((extent[0] + 16) / cs_x)) + 2
            cs_y = cell / (2 ** k)
            cy = int(math.ceil((extent[1] + 16) / cs_y)) + 2
            self.oct.append((Noise2(seed * 7919 + k * 104729, cx, cy, wrap_x=bool(period_x)), cs_x, cs_y, amp))
            tot += amp
            amp *= gain
        self.norm = 1.0 / tot

    def __call__(self, X, Y):
        s = 0.0
        for n, csx, csy, amp in self.oct:
            if self.period_x:
                u = X / csx
            else:
                u = (X - self.origin[0]) / csx
            v = (Y - self.origin[1]) / csy
            s = s + amp * n(u, v)
        return s * self.norm


# ------------------------------------------------------------------ blur (3 x box ~ gaussian), cumsum based
def _box(a, r, axis, wrap):
    if r < 1:
        return a
    n = a.shape[axis]
    if wrap:
        a2 = np.concatenate([np.take(a, range(n - r, n), axis), a, np.take(a, range(0, r), axis)], axis)
    else:
        pad = [(0, 0)] * a.ndim
        pad[axis] = (r, r)
        a2 = np.pad(a, pad)
    cs = np.cumsum(a2, axis=axis, dtype=np.float64)
    zero_shape = list(cs.shape)
    zero_shape[axis] = 1
    cs = np.concatenate([np.zeros(zero_shape), cs], axis)
    hi = np.take(cs, range(2 * r + 1, 2 * r + 1 + n), axis)
    lo = np.take(cs, range(0, n), axis)
    return ((hi - lo) / (2 * r + 1)).astype(np.float32)


def blur(a, sigma_px, wrap_x=False):
    if sigma_px < 0.5:
        return a
    w = math.sqrt(4 * sigma_px * sigma_px + 1)
    r = max(1, int(round((w - 1) / 2)))
    out = a
    for _ in range(3):
        out = _box(out, r, 1, wrap_x)
        out = _box(out, r, 0, False)
    return out


def shift(a, dx_px, dy_px, wrap_x=False):
    """integer shift (content moves by +dx, +dy)."""
    dx, dy = int(round(dx_px)), int(round(dy_px))
    out = np.zeros_like(a)
    H, W = a.shape[:2]
    if wrap_x:
        a = np.roll(a, dx, axis=1)
        dx = 0
    ys0, ys1 = max(0, -dy), min(H, H - dy)
    xs0, xs1 = max(0, -dx), min(W, W - dx)
    out[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = a[ys0:ys1, xs0:xs1]
    return out


# ------------------------------------------------------------------ canvas
class Canvas:
    """Supersampled premultiplied-linear RGBA canvas. pps_out = output pixels per stud.
    x0/y0 = stud coordinate of the left/top edge (windows); period = x period in studs (seamless strips)."""

    def __init__(self, w_px, h_px, pps_out, ss=2, x0=0.0, y0=0.0, period=None):
        self.w, self.h, self.ss = w_px, h_px, ss
        self.W, self.H = w_px * ss, h_px * ss
        self.pps_out = float(pps_out)
        self.pps = float(pps_out * ss)
        self.x0, self.y0 = x0, y0
        self.period = period
        self.ws, self.hs = w_px / pps_out, h_px / pps_out
        self.X = (x0 + (np.arange(self.W) + 0.5) / self.pps).astype(np.float32)
        self.Y = (y0 + (np.arange(self.H) + 0.5) / self.pps).astype(np.float32)
        self.XX, self.YY = np.meshgrid(self.X, self.Y)
        self.rgb = np.zeros((self.H, self.W, 3), np.float32)
        self.a = np.zeros((self.H, self.W), np.float32)

    # stud bounds -> slices; for periodic canvases returns a list of (slice_y, slice_x, xoffset_studs)
    def boxes(self, xa, xb, ya, yb):
        out = []
        offs = [0.0]
        if self.period:
            offs = [-self.period, 0.0, self.period]
        for o in offs:
            i0 = int(math.floor((xa + o - self.x0) * self.pps))
            i1 = int(math.ceil((xb + o - self.x0) * self.pps))
            j0 = int(math.floor((ya - self.y0) * self.pps))
            j1 = int(math.ceil((yb - self.y0) * self.pps))
            i0, i1 = max(0, i0), min(self.W, i1)
            j0, j1 = max(0, j0), min(self.H, j1)
            if i1 > i0 and j1 > j0:
                out.append((slice(j0, j1), slice(i0, i1), o))
        return out

    def over(self, col, alpha):
        alpha = np.clip(alpha, 0, 1).astype(np.float32)
        col = np.asarray(col, np.float32)
        src = alpha[..., None] * col
        self.rgb = src + self.rgb * (1 - alpha)[..., None]
        self.a = alpha + self.a * (1 - alpha)

    def px(self, studs):
        return studs * self.pps

    def fade(self, mult):
        self.rgb *= mult[..., None]
        self.a *= mult

    def finish(self):
        ss = self.ss
        rgb = self.rgb.reshape(self.h, ss, self.w, ss, 3).mean((1, 3))
        a = self.a.reshape(self.h, ss, self.w, ss).mean((1, 3))
        return rgb, a


def edge_fade(cv, keep=(), margin_px=4, ramp_px=10, ramps=None):
    """Multiplier (canvas res) that is 0 in the outer `margin_px` output px and ramps to 1 over `ramp_px` (per-edge
    override in `ramps`, e.g. a 1 px ramp on a contact edge whose hidden band must stay at full strength), except on
    the edges listed in keep ('l', 'r', 't', 'b')."""
    ss = cv.ss
    ramps = ramps or {}
    m0 = margin_px * ss
    m1 = (margin_px + ramp_px) * ss
    me = {k: (margin_px + ramps.get(k, ramp_px)) * ss for k in "lrtb"}
    fx = np.ones(cv.W, np.float32)
    fy = np.ones(cv.H, np.float32)
    ix = np.arange(cv.W) + 0.5
    iy = np.arange(cv.H) + 0.5
    if "l" not in keep:
        fx *= smoothstep(m0, me["l"], ix)
    if "r" not in keep:
        fx *= smoothstep(m0, me["r"], cv.W - ix)
    if "t" not in keep:
        fy *= smoothstep(m0, me["t"], iy)
    if "b" not in keep:
        fy *= smoothstep(m0, me["b"], cv.H - iy)
    return fy[:, None] * fx[None, :]


# ------------------------------------------------------------------ export (straight alpha + bleed)
def push_pull(c, w):
    """Fill colours where w == 0 from an alpha-weighted pyramid. c (H,W,3) float, w (H,W) float weights."""
    pyr = []
    cw, ww = c * w[..., None], w.astype(np.float64)
    cw = cw.astype(np.float64)
    while True:
        pyr.append((cw, ww))
        H, W = ww.shape
        if H == 1 and W == 1:
            break
        Hp, Wp = H + (H % 2), W + (W % 2)
        cwp = np.zeros((Hp, Wp, 3))
        wwp = np.zeros((Hp, Wp))
        cwp[:H, :W] = cw
        wwp[:H, :W] = ww
        cw = cwp[0::2, 0::2] + cwp[1::2, 0::2] + cwp[0::2, 1::2] + cwp[1::2, 1::2]
        ww = wwp[0::2, 0::2] + wwp[1::2, 0::2] + wwp[0::2, 1::2] + wwp[1::2, 1::2]
    cw, ww = pyr[-1]
    col = cw / max(ww[0, 0], 1e-12) if ww[0, 0] > 0 else np.full_like(cw, 0.5)
    nlev = len(pyr) - 1
    for lev in range(nlev - 1, -1, -1):
        cw_l, ww_l = pyr[lev]
        H, W = ww_l.shape
        up = np.repeat(np.repeat(col, 2, 0), 2, 1)[:H, :W]
        own = cw_l / np.maximum(ww_l, 1e-12)[..., None]
        # confidence: a cell trusts its own colour only when it holds enough alpha mass (half its texels' worth)
        conf = np.clip(ww_l / (0.5 * (4 ** lev)), 0, 1)[..., None]
        col = conf * own + (1 - conf) * up
    return col


def export(cv_or_arrays, path, keep=(), seed=1, meta=None):
    """Finish a canvas (or take (rgb_pm, a) at output res), dither, alpha floor, bleed, save. Returns check dict."""
    if isinstance(cv_or_arrays, Canvas):
        rgb_pm, a = cv_or_arrays.finish()
    else:
        rgb_pm, a = cv_or_arrays
    a = np.clip(a, 0, 1)
    straight = np.where(a[..., None] > 1e-7, rgb_pm / np.maximum(a, 1e-7)[..., None], 0.0)
    srgb = to_srgb(straight)
    rng = np.random.default_rng(seed)
    soft = (a > 0) & (a < 1)
    # 1) TPDF dither (+-0.5 LSB) on alpha ramps and colour, BEFORE the alpha floor (review item 6)
    da = (rng.random(a.shape) + rng.random(a.shape) - 1.0) * 0.5
    a8 = np.clip(np.round(a * 255.0 + da * soft), 0, 255)
    dc = (rng.random(srgb.shape) + rng.random(srgb.shape) - 1.0) * 0.5
    c8 = np.clip(np.round(srgb * 255.0 + dc), 0, 255)
    # 2) alpha floor: nothing below 2/255 survives (no invisible fog over the carrier)
    a8[a8 < 2] = 0
    # 3) push-pull colour bleed under alpha 0 (colours of the nearest visible content, weighted by alpha)
    filled = push_pull(c8, a8 / 255.0)
    # near-invisible texels (alpha < 15/255) carry a colour eased toward the neighbourhood fill, so GPU-style straight
    # mips are not lightened/darkened by faint tails (composite change at mip 0 <= ~3/255)
    k = np.clip(a8 / 15.0, 0, 1)[..., None]
    c8 = np.round(filled + (c8 - filled) * k)
    out = np.dstack([c8, a8]).astype(np.uint8)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(out, "RGBA").save(path, optimize=True)
    return check_png(path, keep, meta)


# ------------------------------------------------------------------ checks
def naive_mip(rgb, a, k):
    """Straight-alpha mip like a GPU builds from a straight texture: average RGB and alpha separately (wrap pad)."""
    f = 2 ** k
    H, W = a.shape
    Hc, Wc = (H // f) * f, (W // f) * f
    r = rgb[:Hc, :Wc].reshape(Hc // f, f, Wc // f, f, 3).mean((1, 3))
    al = a[:Hc, :Wc].reshape(Hc // f, f, Wc // f, f).mean((1, 3))
    pm = (rgb[:Hc, :Wc] * a[:Hc, :Wc, None]).reshape(Hc // f, f, Wc // f, f, 3).mean((1, 3))
    return r, al, pm


def check_png(path, keep=(), meta=None, margin=4):
    im = Image.open(path)
    arr = np.asarray(im).astype(np.float32)
    res = {"file": os.path.basename(path), "mode": im.mode, "w": im.width, "h": im.height}
    a = arr[..., 3] / 255.0
    rgb = arr[..., :3] / 255.0
    res["alpha_min"] = float(a.min())
    res["alpha_max"] = float(a.max())
    res["transparent_pct"] = round(float((a == 0).mean() * 100), 1)
    res["max_side_ok"] = bool(max(im.width, im.height) <= 1024)
    res["mult4"] = bool(im.width % 4 == 0 and im.height % 4 == 0)
    edges = {"t": a[:margin, :], "b": a[-margin:, :], "l": a[:, :margin], "r": a[:, -margin:]}
    res["edges_with_content"] = sorted([k for k, v in edges.items() if v.max() > 0])
    res["edge_rule_ok"] = bool(set(res["edges_with_content"]) <= set(keep))
    res["edges_allowed"] = sorted(keep)
    # fringe/halo test: GPU-style naive straight-alpha mips (RGB and alpha averaged separately) vs correct premultiplied
    # mips, composited over the hub colours, measured in EDGE blocks (blocks that mix alpha-0 and visible texels, where a
    # halo would appear). Also what black-filled / white-filled transparent texels would give (the halo we avoid).
    stats = {}
    for k in (1, 2, 3):
        f = 2 ** k
        H, W = a.shape
        Hc, Wc = (H // f) * f, (W // f) * f
        R = rgb[:Hc, :Wc].reshape(Hc // f, f, Wc // f, f, 3)
        A = a[:Hc, :Wc].reshape(Hc // f, f, Wc // f, f)
        al = A.mean((1, 3))
        pm = (R * A[..., None]).mean((1, 3))
        edge = (A == 0).any((1, 3)) & (A > 0).any((1, 3))
        if not edge.any():
            continue
        e_ours, e_blk, e_wht = [], [], []
        for base in ((128, 170, 96), (96, 132, 170), (222, 205, 170)):
            b = np.array(base, np.float32) / 255.0
            correct = pm + b * (1 - al[..., None])
            for fill, acc in ((None, e_ours), (0.0, e_blk), (1.0, e_wht)):
                RR = R if fill is None else np.where(A[..., None] > 0, R, fill)
                naive = RR.mean((1, 3)) * al[..., None] + b * (1 - al[..., None])
                acc.append(np.abs(naive - correct).max(-1)[edge] * 255)
        e_ours, e_blk, e_wht = (np.concatenate(v) for v in (e_ours, e_blk, e_wht))
        stats[f"mip{k}"] = {"ours_p99": round(float(np.percentile(e_ours, 99)), 2),
                            "ours_max": round(float(e_ours.max()), 2),
                            "black_fill_p99": round(float(np.percentile(e_blk, 99)), 2),
                            "white_fill_p99": round(float(np.percentile(e_wht, 99)), 2)}
    res["halo_edge_blocks"] = stats
    worst = max([stats[m]["ours_p99"] for m in ("mip1", "mip2") if m in stats] + [0.0])
    res["fringe_max_err_255"] = round(worst, 2)
    m3 = stats.get("mip3")
    res["fringe_ok"] = bool(worst <= 8.0 and (m3 is None or m3["ours_p99"] <= m3["black_fill_p99"] + 1.0))
    if "l" in keep and "r" in keep:
        # seamless self-tiling: wrap difference vs typical neighbour difference
        rgba = arr / 255.0
        d_wrap = np.abs(rgba[:, 0] - rgba[:, -1]).max(axis=1)
        d_in = np.abs(rgba[:, 1:] - rgba[:, :-1]).max(axis=2)
        res["self_tile_wrap_max"] = round(float(d_wrap.max()), 4)
        res["self_tile_wrap_mean"] = round(float(d_wrap.mean()), 4)
        res["inner_neighbour_mean"] = round(float(d_in.mean()), 4)
        res["inner_neighbour_p99"] = round(float(np.percentile(d_in.max(axis=0), 99)), 4)
    if meta:
        res.update(meta)
    return res


# ------------------------------------------------------------------ geometry helpers
def rot(v, ang):
    c, s = math.cos(ang), math.sin(ang)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])


def jag(points, rough, levels, rng, slide=0.12):
    """Angular zig-zag by midpoint displacement (cracks)."""
    pts = [np.asarray(p, float) for p in points]
    for _ in range(levels):
        out = [pts[0]]
        for a, b in zip(pts[:-1], pts[1:]):
            d = b - a
            L = float(np.hypot(*d))
            n = np.array([-d[1], d[0]]) / max(L, 1e-9)
            m = (a + b) / 2 + n * rng.uniform(-1, 1) * rough * L + d * rng.uniform(-slide, slide)
            out += [m, b]
        pts = out
    return np.array(pts)


def arclen(pts):
    seg = np.hypot(*(pts[1:] - pts[:-1]).T)
    return np.concatenate([[0.0], np.cumsum(seg)])


def raster_strokes(cv, strokes, band):
    """Distance fields for a set of variable-width polylines.
    strokes: list of dicts {pts (N,2), hw (N,) half widths}. Returns dict of canvas arrays:
      sd = dist - halfwidth (studs, <0 inside), ox/oy = unit vector centreline->pixel, rel = dist/hw,
      s = arc length at the closest point (+ stroke offset 1000*k so strokes differ), hw = local half width."""
    H, W = cv.H, cv.W
    sd = np.full((H, W), 1e9, np.float32)
    ox = np.zeros((H, W), np.float32)
    oy = np.zeros((H, W), np.float32)
    rel = np.full((H, W), 9.0, np.float32)
    ss = np.zeros((H, W), np.float32)
    hwf = np.zeros((H, W), np.float32)
    for k, st in enumerate(strokes):
        pts = np.asarray(st["pts"], np.float32)
        hw = np.asarray(st["hw"], np.float32)
        cum = arclen(pts)
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            ha, hb = hw[i], hw[i + 1]
            m = max(ha, hb) + band
            for sy, sx, o in cv.boxes(min(a[0], b[0]) - m, max(a[0], b[0]) + m, min(a[1], b[1]) - m,
                                      max(a[1], b[1]) + m):
                X = cv.XX[sy, sx] - o
                Y = cv.YY[sy, sx]
                dx, dy = X - a[0], Y - a[1]
                d0, d1 = b[0] - a[0], b[1] - a[1]
                L2 = max(d0 * d0 + d1 * d1, 1e-12)
                t = np.clip((dx * d0 + dy * d1) / L2, 0, 1)
                px, py = dx - t * d0, dy - t * d1
                dist = np.sqrt(px * px + py * py)
                h = ha + (hb - ha) * t
                val = dist - h
                cur = sd[sy, sx]
                upd = val < cur
                if not upd.any():
                    continue
                inv = 1.0 / np.maximum(dist, 1e-6)
                sd[sy, sx] = np.where(upd, val, cur)
                ox[sy, sx] = np.where(upd, px * inv, ox[sy, sx])
                oy[sy, sx] = np.where(upd, py * inv, oy[sy, sx])
                rel[sy, sx] = np.where(upd, dist / np.maximum(h, 1e-6), rel[sy, sx])
                ss[sy, sx] = np.where(upd, cum[i] + t * (cum[i + 1] - cum[i]) + 1000.0 * k, ss[sy, sx])
                hwf[sy, sx] = np.where(upd, h, hwf[sy, sx])
    return {"sd": sd, "ox": ox, "oy": oy, "rel": rel, "s": ss, "hw": hwf}


def width_profile(n, wmax, rng, taper=(0.18, 0.72), wmin=0.02, pinch=0.25):
    """Half widths along a polyline of n points: swell in the middle, hairline ends, random pinches."""
    s = np.linspace(0, 1, n)
    prof = smoothstep(0.0, max(taper[0], 1e-3), s) * (1 - smoothstep(min(taper[1], 0.999), 1.0, s))
    prof = 0.25 + 0.75 * prof
    wob = 1 + pinch * np.interp(s, np.linspace(0, 1, 7), rng.uniform(-1, 1, 7))
    hw = wmax * prof * wob
    ends = np.minimum(smoothstep(0, 0.12, s), 1 - smoothstep(0.88, 1.0, s))
    hw = wmin + (hw - wmin) * ends
    return np.maximum(hw, wmin)


def convex_poly(center, radius, n, rng, irregular=0.35, ang0=None):
    ang0 = rng.uniform(0, 2 * np.pi) if ang0 is None else ang0
    angs = np.sort(ang0 + np.linspace(0, 2 * np.pi, n, endpoint=False) + rng.uniform(-0.35, 0.35, n) * (2 * np.pi / n))
    rr = radius * (1 + rng.uniform(-irregular, irregular, n))
    pts = np.stack([center[0] + rr * np.cos(angs), center[1] + rr * np.sin(angs)], 1)
    return pts


def poly_sdf(X, Y, poly):
    """Signed distance (approx outside, exact-ish inside) to a convex polygon (any winding). <0 inside."""
    poly = np.asarray(poly, float)
    c = poly.mean(0)
    d = np.full(X.shape, -1e9, np.float32)
    n = len(poly)
    for k in range(n):
        a, b = poly[k], poly[(k + 1) % n]
        e = b - a
        nrm = np.array([e[1], -e[0]]) / max(np.hypot(*e), 1e-9)
        if np.dot(c - a, nrm) > 0:
            nrm = -nrm
        d = np.maximum(d, (X - a[0]) * nrm[0] + (Y - a[1]) * nrm[1])
    return d


def cov_from_sd(cv, sd):
    """Anti-aliased coverage, 1 output pixel wide ramp (sd in studs, <0 inside)."""
    return np.clip(0.5 - sd * cv.pps_out, 0, 1).astype(np.float32)


# ------------------------------------------------------------------ crack geometry (straight runs + sharp kinks)
def crack_path(rng, p0, p1, seg=(0.35, 0.9), dev=30, micro=0.09, micro_len=0.16):
    """Walk from p0 toward p1 in straight segments with sharp kinks, then a light micro-jag."""
    p = np.array(p0, float)
    target = np.array(p1, float)
    pts = [p.copy()]
    for _ in range(400):
        to = target - p
        dist = float(np.linalg.norm(to))
        if dist < seg[1] * 1.1:
            pts.append(target.copy())
            break
        ang = math.atan2(to[1], to[0]) + math.radians(rng.uniform(-dev, dev))
        p = p + np.array([math.cos(ang), math.sin(ang)]) * rng.uniform(*seg)
        pts.append(p.copy())
    pts = np.array(pts)
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        d = b - a
        L = float(np.hypot(*d))
        nrm = np.array([-d[1], d[0]]) / max(L, 1e-9)
        k = max(1, int(round(L / micro_len)))
        for i in range(1, k):
            out.append(a + d * i / k + nrm * rng.uniform(-1, 1) * micro * L / k)
        out.append(b)
    return np.array(out)


def chain_path(rng, ctrl, **kw):
    pts = [np.asarray(ctrl[0], float)[None]]
    for a, b in zip(ctrl[:-1], ctrl[1:]):
        pts.append(crack_path(rng, a, b, **kw)[1:])
    return np.concatenate(pts, 0)


def crack_widths(pts, rng, w_typ, w_open, opens=1, open_len=(1.2, 2.4), tip=(1.0, 1.0), wmin=0.012, jitter=0.18):
    s = arclen(pts)
    S = s[-1]
    j = rng.uniform(-jitter, jitter, len(pts))
    j = np.convolve(np.pad(j, 1, mode="edge"), np.ones(3) / 3, mode="valid")
    hw = w_typ * (1 + j)
    for _ in range(opens):
        c = rng.uniform(0.3, 0.7) * S
        ln = rng.uniform(*open_len)
        bump = np.exp(-((s - c) / (ln / 2)) ** 4)
        hw = hw + (w_open - w_typ) * bump * (1 + 0.5 * j)
    t0 = np.clip(s / max(tip[0], 1e-3), 0, 1)
    t1 = np.clip((S - s) / max(tip[1], 1e-3), 0, 1)
    hw = wmin + (hw - wmin) * np.minimum(smoothstep(0, 1, t0), smoothstep(0, 1, t1)) ** 0.8
    return np.maximum(hw, wmin)


# ------------------------------------------------------------------ cracks
def paint_cracks(cv, strokes, light, opt, rng, seed):
    """Paint crack strokes: dirt halo, shadow lip (W4), ONE-SIDED BROKEN light lip (W5), dark core with depth."""
    o = dict(halo_a=0.16, halo_w=0.22, sh_a=0.32, sh_w=0.09, hl_a=0.26, hl_w=0.07, hl_on=0.45, band=0.35)
    o.update(opt or {})
    f = raster_strokes(cv, strokes, o["band"])
    sd, ox, oy, rel, s, hw = f["sd"], f["ox"], f["oy"], f["rel"], f["s"], f["hw"]
    # 1-2 px angular micro-jag on every edge (no smooth tubes): faceted cellular jitter + a little gradient noise
    ext, org = (cv.ws + 4, cv.hs + 4), (cv.x0 - 2, cv.y0 - 2)
    jf1, _jf2 = worley(cv.XX, cv.YY, 0.09, seed + 17, cv.period, org)
    jag_n = (jf1 / 0.09 - 0.45) * 2.0
    sd = sd + o.get("jag", 1.2 / cv.pps_out) * np.clip(jag_n, -1.2, 1.2) * smoothstep(0.02, 0.05, hw)
    f["sd"] = sd
    l2 = np.array(light[:2]) / max(np.hypot(*light[:2]), 1e-6)
    facing = ox * l2[0] + oy * l2[1]  # >0: pixel lies on the side of the crack that is toward the light
    wide = smoothstep(0.03, 0.12, hw)
    n_gate = Field(seed + 11, 0.55, 2, extent=(400, 4))
    n_brk = Field(seed + 12, 0.45, 2, extent=(cv.ws + 4, cv.hs + 4), origin=(cv.x0 - 2, cv.y0 - 2))
    outside = sd > 0
    # 1) dirt halo, broken by noise, only along the wider parts
    halo = o["halo_a"] * (1 - smoothstep(0.0, o["halo_w"], sd)) * outside
    halo *= smoothstep(-0.3, 0.4, n_brk(cv.XX, cv.YY)) * (0.35 + 0.65 * wide)
    cv.over(P("W1"), halo)
    # 2) shadow lip: on the edge that faces the light (that bevel faces away from the light)
    sh = o["sh_a"] * (1 - smoothstep(0.0, o["sh_w"], sd)) * outside * smoothstep(0.0, 0.55, facing)
    sh *= (0.4 + 0.6 * wide)
    cv.over(P("W4"), sh)
    # 3) light lip: the OTHER edge only, broken to <= hl_on of the length, never on hairlines
    gate_v = n_gate(s * 1.0, np.full_like(s, 1.7))
    thr = np.quantile(n_gate(np.linspace(0, 300, 4000), np.full(4000, 1.7)), 1 - o["hl_on"])
    gate = smoothstep(thr, thr + 0.12, gate_v)
    # round 3: a second, 2D gate with a different scale -> irregular gaps, no continuous lip along an open section
    n_brk2 = Field(seed + 13, 0.32, 2, extent=(cv.ws + 4, cv.hs + 4), origin=(cv.x0 - 2, cv.y0 - 2))
    gate = gate * smoothstep(-0.05, 0.3, n_brk2(cv.XX, cv.YY))
    prof = smoothstep(0.0, 0.012, sd) * (1 - smoothstep(o["hl_w"] * 0.35, o["hl_w"], sd))
    hl = o["hl_a"] * prof * outside * smoothstep(0.1, 0.6, -facing) * gate * smoothstep(0.06, 0.13, hw)
    cv.over(P("W5"), hl)
    # 4) core: the inner wall that faces the light (pixel on the far side from the light) gets D2, the rest D1
    k = np.clip(-facing * rel * 1.35, 0, 1) * smoothstep(0.06, 0.16, hw)
    col = lerp(P("D1"), P("D2"), (0.9 * k)[..., None])
    cv.over(col, cov_from_sd(cv, sd))
    return f


def paint_polys_hole(cv, poly, light, depth_cols=("D1", "D2"), rim_light=0.26):
    """A missing chunk / pocket: dark polygon with depth shading."""
    X, Y = cv.XX, cv.YY
    d = poly_sdf(X, Y, poly)
    c = np.asarray(poly).mean(0)
    l2 = np.array(light[:2]) / max(np.hypot(*light[:2]), 1e-6)
    dirx, diry = X - c[0], Y - c[1]
    nn = np.maximum(np.hypot(dirx, diry), 1e-6)
    facing = (dirx * l2[0] + diry * l2[1]) / nn
    k = np.clip(-facing, 0, 1) * smoothstep(0.0, 0.12, -d)
    col = lerp(P(depth_cols[0]), P(depth_cols[1]), (0.8 * k)[..., None])
    cv.over(P("W4"), 0.3 * (1 - smoothstep(0, 0.07, d)) * (d > 0) * smoothstep(0.0, 0.5, facing))
    cv.over(P("W5"), rim_light * (smoothstep(0, 0.01, d) * (1 - smoothstep(0.02, 0.06, d))) * (d > 0)
            * smoothstep(0.2, 0.7, -facing))
    cv.over(col, cov_from_sd(cv, d))
    return d


def paint_recess(cv, poly, light, a=0.42, edge_dark=0.0, edge_light=0.22, seed=0):
    """A chipped flake: a DARK recessed fill (W4, slightly deeper toward the light side, where its wall is in shade)
    and a thin BROKEN light edge on the side away from the light only (the wall that faces the light). No rim on the
    shadow side, no pale fill (review round 2: no glass shards)."""
    X, Y = cv.XX, cv.YY
    d = poly_sdf(X, Y, poly)
    c = np.asarray(poly).mean(0)
    l2 = np.array(light[:2]) / max(np.hypot(*light[:2]), 1e-6)
    dirx, diry = X - c[0], Y - c[1]
    nn = np.maximum(np.hypot(dirx, diry), 1e-6)
    facing = (dirx * l2[0] + diry * l2[1]) / nn
    inside = cov_from_sd(cv, d)
    cv.over(P("W4"), a * inside * (0.8 + 0.2 * smoothstep(-0.4, 0.8, facing)))
    if edge_dark > 0:
        band_d = inside * (1 - smoothstep(0.0, 0.03, -d))
        cv.over(P("D2"), edge_dark * band_d * smoothstep(0.3, 0.8, facing))
    gate = smoothstep(-0.1, 0.3, Field(seed + 41, 0.18, 1, extent=(cv.ws + 4, cv.hs + 4),
                                       origin=(cv.x0 - 2, cv.y0 - 2))(X, Y))
    band = inside * (1 - smoothstep(0.0, 0.03, -d))
    cv.over(P("W5"), edge_light * band * smoothstep(0.35, 0.8, -facing) * gate)


def paint_crater(cv, poly, light, fill=0.84, wall_w=0.24, seed=0):
    """An impact crater (round 2b): an OPAQUE rubble floor (the studs are broken away, so none show through), the wall
    nearest the light casts a soft shadow onto that floor, an inner wall band (D1 in shade on the light side, lit D2
    on the far side, with radial striations), a broken light lip on the far rim only."""
    X, Y = cv.XX, cv.YY
    d = poly_sdf(X, Y, poly)
    c = np.asarray(poly).mean(0)
    l2 = np.array(light[:2]) / max(np.hypot(*light[:2]), 1e-6)
    dirx, diry = X - c[0], Y - c[1]
    nn = np.maximum(np.hypot(dirx, diry), 1e-6)
    facing = (dirx * l2[0] + diry * l2[1]) / nn
    ext, org = (cv.ws + 4, cv.hs + 4), (cv.x0 - 2, cv.y0 - 2)
    n1 = Field(seed + 51, 0.22, 2, extent=ext, origin=org)(X, Y)
    n2 = Field(seed + 52, 0.07, 1, extent=ext, origin=org)(X, Y)
    inside = cov_from_sd(cv, d)
    # rubble floor: dark umber-grey, mottled, a few paler crumbs
    floor = lerp(P("D1"), P("W9"), smoothstep(-0.5, 0.6, n1)[..., None])
    floor = lerp(floor, P("D2"), (0.45 * smoothstep(0.35, 0.7, n2))[..., None])
    cv.over(floor, fill * inside)
    crumbs = smoothstep(0.55, 0.75, n2) * smoothstep(0.1, 0.5, n1)
    cv.over(P("W8"), 0.35 * crumbs * inside * smoothstep(wall_w, wall_w * 1.6, -d))
    # the light-side wall throws a soft shadow across part of the floor
    sh = smoothstep(0.0, 0.7, facing) * (1 - smoothstep(wall_w, wall_w + 0.45, -d))
    cv.over(P("D1"), 0.55 * sh * inside)
    # inner wall band with radial striations
    ang = np.arctan2(diry, dirx)
    stri = 0.75 + 0.25 * np.sin(ang * 23 + 3 * n1)
    wall = inside * (1 - smoothstep(wall_w * 0.75, wall_w, -d))
    col = lerp(P("D1"), P("D2"), smoothstep(-0.3, 0.6, -facing)[..., None])
    col = col * stri[..., None]
    cv.over(col, 0.92 * wall)
    # round 3: no pale lip on the crater rim (it read as a continuous white edge and mixed badly in far mips); the lit
    # D2 inner wall on the far side carries the depth read on its own
    return d


def paint_pebble(cv, poly, light, a_hi=0.26, a_sh=0.3, shadow=0.32):
    """Loose chip of the same plastic: transparent body (shows the base), lit half, shade half, contact shadow."""
    X, Y = cv.XX, cv.YY
    l2 = np.array(light[:2]) / max(np.hypot(*light[:2]), 1e-6)
    poly = np.asarray(poly)
    sh_poly = poly - l2 * 0.06
    ds = poly_sdf(X, Y, sh_poly)
    cv.over(P("W4"), shadow * np.clip(0.5 - ds / 0.035, 0, 1))
    d = poly_sdf(X, Y, poly)
    c = poly.mean(0)
    dirx, diry = X - c[0], Y - c[1]
    nn = np.maximum(np.hypot(dirx, diry), 1e-6)
    facing = (dirx * l2[0] + diry * l2[1]) / nn
    cov = cov_from_sd(cv, d)
    cv.over(P("W5"), a_hi * cov * smoothstep(-0.1, 0.6, facing))
    cv.over(P("W4"), a_sh * cov * smoothstep(-0.1, 0.6, -facing))


# ------------------------------------------------------------------ cellular (Worley) noise, optionally periodic in x
def worley(X, Y, cell, seed, period=None, origin=(-8.0, -8.0)):
    """F1, F2 distances (studs) to jittered feature points (one per cell). period (studs) wraps x exactly."""
    rng = np.random.default_rng(seed)
    if period:
        ncx = max(1, int(round(period / cell)))
        cx = period / ncx
        ox = 0.0
    else:
        ncx = 4096
        cx = cell
        ox = origin[0]
    cy = cell
    oy = origin[1]
    ncy = 4096
    jx = rng.random((256, 256)).astype(np.float32)
    jy = rng.random((256, 256)).astype(np.float32)
    gx = np.floor((X - ox) / cx).astype(np.int64)
    gy = np.floor((Y - oy) / cy).astype(np.int64)
    f1 = np.full(X.shape, 1e9, np.float32)
    f2 = np.full(X.shape, 1e9, np.float32)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            cxi = gx + dx
            cyi = gy + dy
            hx = np.mod(cxi, ncx) if period else cxi
            ix = np.mod(hx * 7 + cyi * 13, 256)
            iy = np.mod(hx * 11 + cyi * 5 + 3, 256)
            px = ox + (cxi + 0.1 + 0.8 * jx[iy, ix]) * cx
            py = oy + (cyi + 0.1 + 0.8 * jy[iy, ix]) * cy
            d = np.sqrt((X - px) ** 2 + (Y - py) ** 2)
            f2 = np.where(d < f1, f1, np.minimum(f2, d))
            f1 = np.minimum(f1, d)
    return f1, f2


# ------------------------------------------------------------------ moss
class MossScene:
    """Object description of moss (positions, radii, tints, stipple). Rendering is deterministic from this data, so
    shared objects render identically in every canvas/window (the MossBase seam band)."""

    def __init__(self):
        self.clumps = []   # (x, y, r, h0, tint, steep)
        self.stips = []    # (x, y, r, colour key)
        self.cushions = []  # (x, y, R, hR) - cushion-level shape (for the big-form normal)
        self.lumps = []    # (x, y, r, amp) - soft sub-cushion lumps (form)

    def extend(self, other):
        self.clumps += other.clumps
        self.stips += other.stips
        self.cushions += other.cushions
        self.lumps += other.lumps
        return self


def moss_cushion(scene, rng, cx, cy, R, light, r_rng=(0.07, 0.16), hR=None, squash=(1.0, 1.0), warp=0.28,
                 tip_p=0.55, edge_keep=0.22, min_r=0.06, region=None, lump_r=None):
    """Fill a warped, lobed cushion with overlapping micro-clumps (tufted contour) + soft sub-lumps (form)."""
    hR = R * 0.32 if hR is None else hR
    scene.cushions.append((cx, cy, R, hR, squash[0], squash[1]))
    lr = lump_r if lump_r else max(0.1, min(0.32, R * 0.4))
    nl = max(1, int(round((R / lr) ** 2 * 1.3)))
    for _ in range(nl):
        a = rng.uniform(0, 2 * np.pi)
        d = R * 0.85 * math.sqrt(rng.uniform(0, 1))
        lx, ly = cx + math.cos(a) * d * squash[0], cy + math.sin(a) * d * squash[1]
        if region is not None and not region(lx, ly):
            continue
        rr_ = lr * rng.uniform(0.75, 1.3)
        scene.lumps.append((lx, ly, rr_, rr_ * rng.uniform(0.45, 0.7)))
    rm = 0.5 * (r_rng[0] + r_rng[1])
    sp = rm * 0.95
    n = int(math.ceil(2.6 * R / sp))
    lobes = rng.uniform(0, 2 * np.pi), rng.integers(3, 6), rng.uniform(0.1, 0.22)
    l2 = np.array(light[:2]) / max(np.hypot(*light[:2]), 1e-6)
    for j in range(n):
        for i in range(n):
            px = cx + (i - n / 2 + rng.uniform(0, 1)) * sp
            py = cy + (j - n / 2 + rng.uniform(0, 1)) * sp
            dx, dy = (px - cx) / squash[0], (py - cy) / squash[1]
            d = math.hypot(dx, dy)
            ang = math.atan2(dy, dx)
            rr = R * (1 + lobes[2] * math.sin(lobes[1] * ang + lobes[0]) + warp * 0.5 * math.sin(3 * ang + 1.3 * lobes[0]))
            f = 1 - d / max(rr, 1e-6)
            if region is not None and not region(px, py):
                continue
            keep = smoothstep(-edge_keep, 0.06, f)
            if rng.random() > keep:
                continue
            r = rng.uniform(*r_rng) * (0.65 + 0.35 * smoothstep(0.0, 0.5, f))
            r = max(r, min_r)
            h0 = hR * math.sqrt(max(0.0, 1 - min(1.0, d / max(rr, 1e-6)) ** 2))
            tint = rng.normal(0, 1)
            steep = rng.uniform(0.55, 0.85)
            scene.clumps.append((px, py, r, h0, tint, steep))
            # lit-tip stipple: on the light side of the cushion and on higher clumps
            side = (dx * l2[0] + dy * l2[1]) / max(d, 1e-6) if d > 1e-6 else 0.0
            p = tip_p * (0.2 + 0.8 * smoothstep(-0.4, 0.7, side)) * (0.3 + 0.7 * smoothstep(0.0, 0.6, f))
            if rng.random() < p:
                k = int(rng.integers(1, 3))
                for _ in range(k):
                    ofs = r * rng.uniform(0.2, 0.5)
                    a = math.atan2(l2[1], l2[0]) + rng.uniform(-1.0, 1.0)
                    sx, sy = px + math.cos(a) * ofs, py + math.sin(a) * ofs
                    sr = max(min_r * 0.6, r * rng.uniform(0.3, 0.45))
                    key = "M5" if rng.random() < 0.18 else "M4"
                    scene.stips.append((sx, sy, sr, key))


def moss_scatter(scene, rng, cx, cy, spread, n, light, r_rng=(0.06, 0.12), cluster=(1, 5), tip_p=0.4, region=None,
                 min_r=0.06):
    """Satellite spores: small clusters around a centre, sparser with distance."""
    for _ in range(n):
        ang = rng.uniform(0, 2 * np.pi)
        dist = spread * math.sqrt(rng.uniform(0.15, 1.0))
        x, y = cx + math.cos(ang) * dist, cy + math.sin(ang) * dist * 0.85
        if region is not None and not region(x, y):
            continue
        R = rng.uniform(0.09, 0.22) * rng.integers(cluster[0], cluster[1] + 1) ** 0.5
        moss_cushion(scene, rng, x, y, R, light, r_rng=r_rng, tip_p=tip_p, edge_keep=0.1, min_r=min_r, region=region)


def moss_render(cv, scene, light, halo_a=0.26, halo_w=0.14, shadow_a=0.24, wrap=False, seed=5, ground_ao=True,
                noise_period=None, fine=0.09, thresh=0.55, fur=0.16, tip_amt=0.85, dome=1.0, lump=0.04, lump_k=1.0, value=0.88,
                pal=None, tip_lo=0.55, dying=0.0, cav_k=0.45, dying_gate=None, **_ignored):
    """Moss v5. Form: summed soft gaussian sub-lumps (one per clump) on top of each cushion's dome -> soft lumpy
    cushions, cavity only between lumps/cushions. Contour: thresholded field + fine fur noise -> irregular tufted
    edge with a crisp 1 px alpha edge (no stroke). Surface: blotchy speckle in COLOUR only (dark olive body, yellow-green
    tip blotches on the lit side, a few brighter sparks) - like the graveyard moss. No spheres, cells or pits."""
    H, W = cv.H, cv.W
    if not scene.clumps:
        return np.zeros((H, W), np.float32)

    def M(k):                       # round 4: optional palette remap (None = the original colours, bit for bit)
        return P(pal.get(k, k)) if pal else P(k)
    C = np.zeros((H, W), np.float32)
    Hs = np.zeros((H, W), np.float32)
    for (x, y, r, h0, tn, steep) in scene.clumps:
        R = 2.0 * r
        for sy, sx, o in cv.boxes(x - R, x + R, y - R, y + R):
            dx = cv.XX[sy, sx] - o - x
            dy = cv.YY[sy, sx] - y
            k = np.exp(-(dx * dx + dy * dy) / (r * r) * 1.25) * (0.9 + 0.12 * math.tanh(tn))
            C[sy, sx] += k
            Hs[sy, sx] += k * h0
    per = noise_period if noise_period else cv.period
    ext = (cv.ws + 4, cv.hs + 4)
    org = (cv.x0 - 2, cv.y0 - 2)
    nf = Field(seed + 31, fine, 2, extent=ext, period_x=per, origin=org)(cv.XX, cv.YY)       # fur / speckle A
    nt = Field(seed + 33, fine * 0.9, 2, extent=ext, period_x=per, origin=org)(cv.XX, cv.YY)  # speckle B
    nm = Field(seed + 32, fine * 3.0, 2, extent=ext, period_x=per, origin=org)(cv.XX, cv.YY)  # mottling
    F = np.minimum(C, 1.8) + fur * nf + 0.1 * nm
    gy, gx = np.gradient(F, 1.0 / cv.pps)
    gl = np.sqrt(gx * gx + gy * gy) + 1e-3
    cov = np.clip(0.5 + (F - thresh) / gl * cv.pps_out, 0, 1).astype(np.float32)
    inner = np.clip(F - thresh, 0, None)
    l3 = np.asarray(light, np.float32)
    l2 = l3[:2] / max(np.hypot(*l3[:2]), 1e-6)
    # glazes under the moss: irregular damp halo (<= 0.3) + contact shadow offset away from the light
    nz = Field(seed + 3, 0.5, 2, extent=ext, period_x=per, origin=org)(cv.XX, cv.YY)
    mask = blur(cov, cv.px(halo_w), wrap_x=wrap)
    halo = halo_a * np.clip(mask * 2.2, 0, 1) * smoothstep(-0.35, 0.45, nz) * (1 - cov)
    cv.over(M("W1"), np.minimum(halo, 0.3))
    shd = shift(blur(cov, cv.px(0.035), wrap_x=wrap), -l2[0] * cv.px(0.06), -l2[1] * cv.px(0.06), wrap_x=wrap)
    cv.over(M("W4"), shadow_a * shd * (1 - cov))
    # form: cushion dome + soft sub-lumps + a little of the clump field
    Hd = Hs / np.maximum(C, 1e-4)
    Hd = blur(Hd * smoothstep(0.0, 0.25, C), cv.px(0.05), wrap_x=wrap)
    Hl = np.zeros((H, W), np.float32)
    for (x, y, r, amp) in getattr(scene, "lumps", []):
        R = 2.2 * r
        for sy, sx, o in cv.boxes(x - R, x + R, y - R, y + R):
            dx = cv.XX[sy, sx] - o - x
            dy = cv.YY[sy, sx] - y
            Hl[sy, sx] = np.maximum(Hl[sy, sx], amp * np.exp(-(dx * dx + dy * dy) / (r * r)))
    Ht = Hd * dome + lump_k * Hl + lump * np.minimum(C, 1.4) + 0.05 * np.minimum(inner, 0.6)
    Ht = blur(Ht, cv.px(0.012), wrap_x=wrap)
    hy, hx = np.gradient(Ht, 1.0 / cv.pps)
    nx, ny = -hx * 1.4, -hy * 1.4
    inv = 1.0 / np.sqrt(nx * nx + ny * ny + 1)
    lam = (nx * l3[0] + ny * l3[1] + l3[2]) * inv
    dif = np.clip(0.42 + 0.62 * lam, 0, 1.1)
    cav = np.clip((blur(Ht, cv.px(0.06), wrap_x=wrap) - Ht) / 0.02, 0, 1)
    edge = 1 - smoothstep(0.0, 0.25, inner)
    v = dif * (1 - cav_k * cav) * value
    if ground_ao:
        v = v * (1 - 0.3 * edge)
    v = v + 0.07 * nm
    col = ramp(np.clip(v, 0, 1), [(0.0, M("M1") * 0.85), (0.38, M("M1")), (0.6, M("M2")), (0.82, M("M3")),
                                  (1.0, lerp(M("M3"), M("M4"), 0.3))])
    # colour speckle: yellow-green tip blotches, mostly on the lit side; a few sparks; darker mottles in shade
    lit = smoothstep(tip_lo, 0.92, dif * value) * (1 - 0.75 * edge) * (1 - 0.8 * cav)
    tips = np.maximum(smoothstep(0.05, 0.38, nt), 0.7 * smoothstep(0.2, 0.48, nf)) * lit * tip_amt
    col = lerp(col, M("M4"), np.clip(tips, 0, 1)[..., None])
    spark = smoothstep(0.5, 0.68, nt) * smoothstep(0.72, 0.95, dif) * (1 - edge)
    col = lerp(col, M("M5"), (0.85 * spark)[..., None])
    dark = smoothstep(0.2, 0.5, -nf) * (1 - lit) * 0.45
    col = lerp(col, M("M1") * 0.9, dark[..., None])
    if dying > 0:                   # round 5: a few olive / yellow-brown dying patches (low-frequency, periodic)
        # round 6: FEWER, LARGER, SOFTER patches (big cell, high + wide threshold), sitting on the lit mound tops
        # and the moss edges rather than as freckles in the body
        nd = Field(seed + 41, 1.7, 2, extent=ext, period_x=per, origin=org)(cv.XX, cv.YY)
        loc = np.maximum(smoothstep(0.55, 0.88, dif * value), 1 - smoothstep(0.0, 0.35, inner))
        dm = smoothstep(0.4, 0.85, nd) * dying * (0.3 + 0.7 * loc)
        if dying_gate is not None:          # e.g. MossBase: no dying patches inside the shared seam band
            dm = dm * dying_gate(cv.XX)
        dcol = lerp(P("MD1"), P("MD2"), np.clip(v, 0, 1)[..., None])
        col = lerp(col, dcol, (0.6 * dm)[..., None])
    cv.over(col, cov)
    return cov


# ------------------------------------------------------------------ dead grass sprigs
def grass_sprig(cv, rng, x, y, n, light, length=(0.3, 0.6), w0=0.03, up=None):
    """A few straw blades fanning from (x, y). up = preferred direction (unit) in texture space."""
    l2 = np.array(light[:2]) / max(np.hypot(*light[:2]), 1e-6)
    base_ang = math.atan2(up[1], up[0]) if up is not None else rng.uniform(0, 2 * np.pi)
    for i in range(n):
        ang = base_ang + rng.uniform(-0.9, 0.9)
        L = rng.uniform(*length)
        bend = rng.uniform(-0.5, 0.5)
        pts = []
        for t in np.linspace(0, 1, 9):
            a = ang + bend * t * t
            pts.append((x + math.cos(a) * L * t, y + math.sin(a) * L * t))
        pts = np.array(pts)
        hw = w0 * (1 - np.linspace(0, 1, 9) ** 1.3) + 0.004
        f = raster_strokes(cv, [{"pts": pts, "hw": hw}], 0.02)
        cov = cov_from_sd(cv, f["sd"])
        t = np.clip((f["s"] % 1000.0) / L, 0, 1)
        tone = rng.uniform(0, 1)
        tip = lerp(P("G2"), P("G1"), tone)
        col = lerp(P("G3"), tip, smoothstep(0.0, 0.45, t)[..., None])
        side = (f["ox"] * l2[0] + f["oy"] * l2[1])
        col = col * (1 + 0.18 * np.clip(side, -1, 1))[..., None]
        cv.over(col, cov)


# ------------------------------------------------------------------ slime
def slime_paint(cv, e, light, ew=0.22, hmax=0.12, outline=0.85, translucent=0.85, contact=0.34, view=(0, 0, 1),
                spec_lo=0.86, spec_hi=0.9, rim=True, wrap=False, thick_core=0.0):
    """Shade a slime body given its signed distance field e (studs, >0 inside)."""
    l3 = np.asarray(light, np.float32)
    l2 = l3[:2] / max(np.hypot(*l3[:2]), 1e-6)
    inside = np.clip(0.5 + e * cv.pps_out, 0, 1)
    t = np.clip(e / ew, 0, 1)
    h = hmax * np.sqrt(t)
    h = blur(h, cv.px(0.012), wrap_x=wrap)
    gy, gx = np.gradient(h, 1.0 / cv.pps)
    nx, ny = -gx, -gy
    inv = 1.0 / np.sqrt(nx * nx + ny * ny + 1)
    nx, ny, nz = nx * inv, ny * inv, inv
    lam = nx * l3[0] + ny * l3[1] + nz * l3[2]
    # contact ring (W7) offset away from the light, outside the body
    m = blur(inside, cv.px(0.06), wrap_x=wrap)
    ring = contact * np.clip(shift(m, -l2[0] * cv.px(0.05), -l2[1] * cv.px(0.05), wrap) * 1.6, 0, 1) * (1 - inside)
    cv.over(P("W7"), ring)
    v = np.clip(0.18 + 0.62 * lam, 0, 1)
    body = ramp(v, [(0.0, P("S1")), (0.4, P("S1")), (0.66, P("S2")), (0.86, P("S3")), (1.0, P("S3"))])
    thin = 1 - smoothstep(0.0, 0.6, t)
    body = lerp(body, P("S1") * 0.9, (0.55 * thin)[..., None])
    thick = smoothstep(0.3, 0.75, e) * thick_core
    body = lerp(body, lerp(P("S1"), P("S2"), 0.45), (0.5 * thick)[..., None])
    alpha = inside * (translucent + (1 - translucent) * smoothstep(0.0, 0.35, t))
    cv.over(body, alpha)
    # edges: outline on the light-facing edge... the edge whose normal points AWAY from the light is in shadow
    gny, gnx = np.gradient(e, 1.0 / cv.pps)
    gl = np.maximum(np.hypot(gnx, gny), 1e-6)
    outward_x, outward_y = -gnx / gl, -gny / gl
    facing = outward_x * l2[0] + outward_y * l2[1]  # >0 edge toward the light
    edge = inside * (1 - smoothstep(0.0, 0.035, e))
    cv.over(P("S5"), outline * edge * smoothstep(-0.1, 0.5, -facing))
    if rim:
        rimb = inside * smoothstep(0.012, 0.03, e) * (1 - smoothstep(0.035, 0.07, e)) * smoothstep(0.2, 0.7, facing)
        cv.over(P("S3"), 0.9 * rimb)
    # painted gloss
    vv = np.asarray(view, np.float32)
    hv = l3 + vv
    hv = hv / np.linalg.norm(hv)
    spec = nx * hv[0] + ny * hv[1] + nz * hv[2]
    sm = smoothstep(spec_lo, spec_hi, spec) * smoothstep(0.02, 0.06, e)
    cv.over(P("S4"), 0.95 * sm)
    return inside, (nx, ny, nz)


def smax(a, b, k):
    a = np.maximum(a, -50.0)
    b = np.maximum(b, -50.0)
    h = np.clip(0.5 + 0.5 * (a - b) / k, 0, 1)
    return lerp(b, a, h) + k * h * (1 - h)


def disc_field(cv, cx, cy, R, warp=None, squash=(1, 1)):
    dx = (cv.XX - cx) / squash[0]
    dy = (cv.YY - cy) / squash[1]
    d = np.sqrt(dx * dx + dy * dy)
    if warp is not None:
        d = d * (1 + warp)
    return R - d


def bubbles(cv, rng, e, light, n, rr=(0.04, 0.09), min_e=0.12):
    l3 = np.asarray(light)
    l2 = l3[:2] / max(np.hypot(*l3[:2]), 1e-6)
    ys, xs = np.nonzero(e > min_e)
    if len(xs) == 0:
        return
    for _ in range(n):
        k = rng.integers(0, len(xs))
        x, y = cv.X[xs[k]], cv.Y[ys[k]]
        r = rng.uniform(*rr)
        d = np.sqrt((cv.XX - x) ** 2 + (cv.YY - y) ** 2)
        away = -((cv.XX - x) * l2[0] + (cv.YY - y) * l2[1]) / np.maximum(d, 1e-6)
        ring = np.clip(0.5 - np.abs(d - r) * cv.pps_out / 0.9, 0, 1) * (0.35 + 0.65 * smoothstep(-0.3, 0.6, away))
        cv.over(P("S1"), 0.75 * ring)
        inner = np.clip(0.5 + (r - d) * cv.pps_out, 0, 1)
        cv.over(P("S3"), 0.35 * inner)
        hx, hy = x + l2[0] * r * 0.45, y + l2[1] * r * 0.45
        dh = np.sqrt((cv.XX - hx) ** 2 + (cv.YY - hy) ** 2)
        cv.over(P("S4"), 0.95 * np.clip(0.5 + (r * 0.32 - dh) * cv.pps_out, 0, 1))


def save_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=1)


def components(mask, max_iter=4000):
    """4-connected component labels of a boolean mask (numpy min-label propagation). Returns labels (-1 = off)."""
    H, W = mask.shape
    lab = np.where(mask, np.arange(H * W).reshape(H, W), H * W + 1).astype(np.int64)
    big = H * W + 1
    for _ in range(max_iter):
        n = lab.copy()
        n[1:, :] = np.minimum(n[1:, :], lab[:-1, :])
        n[:-1, :] = np.minimum(n[:-1, :], lab[1:, :])
        n[:, 1:] = np.minimum(n[:, 1:], lab[:, :-1])
        n[:, :-1] = np.minimum(n[:, :-1], lab[:, 1:])
        n = np.where(mask, n, big)
        if np.array_equal(n, lab):
            break
        lab = n
    return np.where(mask, lab, -1)
