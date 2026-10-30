# HubGrime - the 17 grime decal textures (15 + 2 MossBase end caps). Re-runnable, fixed seeds.
#   python gen\make_decals.py            -> all
#   python gen\make_decals.py G_Crack_A W_MossBase_A ...
# Output: HubGrime\decals\<name>.png (RGBA straight alpha) + HubGrime\checks.json (merged).
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grime_lib import (HERE, DECALS, L_FLOOR, L_WALL, P, Canvas, Field, MossScene, arclen, blur, bubbles,  # noqa
                       convex_poly, cov_from_sd, disc_field, edge_fade, export, grass_sprig, jag, lerp,
                       moss_cushion, moss_render, moss_scatter, paint_cracks, paint_pebble, paint_polys_hole,
                       paint_recess, raster_strokes, rot, slime_paint, smax, smoothstep, width_profile)

from make_specs import SPECS  # noqa: E402  (single source of truth, shared with the Blender preview)


def canvas(name, ss=2, **kw):
    sp = SPECS[name]
    pps = sp["px"][0] / sp["studs"][0]
    return Canvas(sp["px"][0], sp["px"][1], pps, ss=ss, **kw)


def contact_ramps(name):
    """Contact edge: keep the content at full strength for >= 0.26 stud past the contact line, then a short ramp into
    the 4 px alpha-0 margin (review item 1: the hidden band sinks into the floor / behind the trim)."""
    sp = SPECS[name]
    if "contact" not in sp:
        return {}
    pps = sp["px"][0] / sp["studs"][0]
    edge, band = sp["contact"]
    band_px = int(round(band * pps)) - 4
    full_px = int(math.ceil(0.26 * pps))
    return {{"bottom": "b", "top": "t"}[edge]: max(1, band_px - full_px)}


def finish(cv, name, seed):
    sp = SPECS[name]
    keep = sp.get("keep", ())
    cv.fade(edge_fade(cv, keep=keep, ramps=contact_ramps(name)))
    meta = {"studs": list(sp["studs"]), "px_per_stud": round(sp["px"][0] / sp["studs"][0], 2),
            "surface": sp["surface"]}
    if "contact" in sp:
        meta["contact_edge"], meta["hidden_band_studs"] = sp["contact"]
    return export(cv, os.path.join(DECALS, name + ".png"), keep=keep, seed=seed, meta=meta)


# ------------------------------------------------------------------ cracks (recipes in rec_cracks.py)
import rec_cracks as RC  # noqa: E402
import rec_stains as RS  # noqa: E402
from grime_lib import chain_path, crack_widths  # noqa: E402


def _crack(name, seed, fn, *extra):
    rng = np.random.default_rng(seed)
    cv = canvas(name)
    fn(cv, rng, seed, *extra)
    return finish(cv, name, seed)


def G_Crack_A():
    return _crack("G_Crack_A", 101, RC.g_crack_a)


def G_Crack_B():
    return _crack("G_Crack_B", 102, RC.g_crack_b)


def G_Crack_C():
    return _crack("G_Crack_C", 103, RC.g_crack_c)


def W_Crack_A():
    return _crack("W_Crack_A", 501, RC.w_crack_a)


def W_Crack_B():
    return _crack("W_Crack_B", 502, RC.w_crack_b)


def W_Crack_C():
    return _crack("W_Crack_C", 503, RC.w_crack_c, stain_layer, lobed)


# ------------------------------------------------------------------ floor moss
def stain_layer(cv, e, col="W1", a_in=0.24, a_core=0.05, tide_a=0.34, tide_col="W2", rings=(), feather=0.25,
                nlow=None, core_w=1.8, seed=0, mottle=0.3):
    """A damp / mud stain that does not look like a sticker: soft feathered edge, low-frequency mottling, a BROKEN
    irregular tide line just inside the edge, faint broken inner rings."""
    X, Y = cv.XX, cv.YY
    ext = (cv.ws + 4, cv.hs + 4)
    org = (cv.x0 - 2, cv.y0 - 2)
    n1 = Field(seed + 71, 0.9, 2, extent=ext, origin=org)(X, Y)
    n2 = Field(seed + 72, 2.2, 2, extent=ext, origin=org)(X, Y)
    n3 = Field(seed + 73, 0.45, 2, extent=ext, origin=org)(X, Y)
    nl = 0 if nlow is None else nlow
    mot = np.clip(1 + mottle * n2 + 0.5 * mottle * n1 + 0.1 * nl, 0.35, 1.7)
    inside = smoothstep(-0.35 * feather, 0.65 * feather, e)
    a = (a_in * inside + a_core * smoothstep(0.15, core_w, e)) * mot
    cv.over(P(col), np.clip(a, 0, 0.6))
    brk = smoothstep(-0.25, 0.35, n3)
    band = smoothstep(-0.02, 0.03, e) * np.exp(-np.maximum(e - 0.03, 0) / 0.06)
    tide = tide_a * band * (0.3 + 0.7 * brk)
    for r, ra in rings:
        tide = tide + ra * np.exp(-((e - r) / 0.04) ** 2) * smoothstep(-0.1, 0.4, n1)
    cv.over(P(tide_col), np.clip(tide, 0, 0.55))


def lobed(cv, discs, k=0.5, warp=None):
    e = None
    for (x, y, R, sx, sy) in discs:
        f = disc_field(cv, x, y, R, warp=warp, squash=(sx, sy))
        e = f if e is None else smax(e, f, k)
    return e


def G_Moss_A():
    name, seed = "G_Moss_A", 201
    rng = np.random.default_rng(seed)
    cv = canvas(name)
    L = L_FLOOR
    nz = Field(seed, 1.1, 3, extent=(8, 8))
    w = 0.24 * nz(cv.XX, cv.YY)
    e = lobed(cv, [(4.0, 4.1, 2.2, 1.0, 0.92), (2.9, 3.2, 1.3, 1, 1), (5.3, 5.0, 1.4, 1, 1), (4.8, 2.8, 1.0, 1, 1)],
              k=0.6, warp=w)
    stain_layer(cv, e, a_in=0.26, a_core=0.08, tide_a=0.26, rings=(), feather=0.4, nlow=nz(cv.XX * 0.5, cv.YY * 0.5))
    # a hairline crack running out of the patch (under the moss)
    st = RC.branch(rng, np.array([4.8, 4.6]), np.array([1.0, 0.85]), 3.0, 0.06)
    paint_cracks(cv, [st], L, {"hl_a": 0.2, "halo_a": 0.1}, rng, seed)
    sc = MossScene()
    # round 4: bigger, fatter cushions (radius x1.3, a little more spread) + the bright mushy palette
    for (x, y, R) in ((4.05, 4.15, 1.5), (2.65, 3.1, 0.95), (5.45, 5.05, 1.0), (5.0, 2.65, 0.7), (2.95, 5.05, 0.66),
                      (6.05, 3.65, 0.5)):
        moss_cushion(sc, rng, x, y, R, L, r_rng=(0.085, 0.18), tip_p=0.65)
    moss_scatter(sc, rng, 4.0, 4.0, 2.9, 12, L)
    moss_render(cv, sc, L, halo_a=0.26, halo_w=0.13, shadow_a=0.26, **MOSS_LOOK_FLOOR)
    return finish(cv, name, seed)


def G_Moss_B():
    name, seed = "G_Moss_B", 202
    rng = np.random.default_rng(seed)
    cv = canvas(name)
    L = L_FLOOR
    t = np.linspace(0, 1, 40)
    path = np.stack([1.0 + 8.0 * t, 3.0 + 0.75 * np.sin(t * np.pi * 1.6 + 0.4) - 0.2 * t], 1)
    # damp band along the joint
    f = raster_strokes(cv, [{"pts": path, "hw": 0.25 + 0.75 * np.sin(t * np.pi) ** 0.8}], 1.6)
    nz = Field(seed, 1.2, 3, extent=(10, 6))
    e = -f["sd"] + 0.15 * nz(cv.XX, cv.YY)
    stain_layer(cv, e, a_in=0.26, a_core=0.06, tide_a=0.3, nlow=nz(cv.XX * 0.5, cv.YY * 0.5))
    # the hidden joint: a thin crack along the path, visible at the ends
    jp = chain_path(rng, path[::6], seg=(0.3, 0.6), dev=16)
    joint = {"pts": jp, "hw": crack_widths(jp, rng, 0.04, 0.06, opens=0, tip=(1.2, 1.2))}
    paint_cracks(cv, [joint], L, {"hl_a": 0.2, "halo_a": 0.08}, rng, seed)
    sc = MossScene()
    for k in range(16):
        tt = 0.06 + 0.88 * (k + rng.uniform(-0.3, 0.3)) / 15
        p = np.array([1.0 + 8.0 * tt, 3.0 + 0.75 * math.sin(tt * math.pi * 1.6 + 0.4) - 0.2 * tt])
        R = 0.3 + 0.8 * math.sin(tt * math.pi) ** 1.2 * rng.uniform(0.75, 1.15)      # round 4: x1.3 fatter
        p = p + rng.normal(0, 0.12, 2)
        moss_cushion(sc, rng, p[0], p[1], R, L, r_rng=(0.085, 0.17), squash=(1.15, 0.9), tip_p=0.65)
    for tt in (0.25, 0.5, 0.75):
        p = np.array([1.0 + 8.0 * tt, 3.0 + 0.75 * math.sin(tt * math.pi * 1.6 + 0.4)])
        moss_scatter(sc, rng, p[0], p[1], 1.6, 5, L)
    moss_render(cv, sc, L, halo_a=0.26, halo_w=0.13, shadow_a=0.26, **MOSS_LOOK_FLOOR)
    grass_sprig(cv, rng, 7.6, 3.05, 4, L, length=(0.3, 0.5), w0=0.03)
    return finish(cv, name, seed)


# ------------------------------------------------------------------ stains
def G_Stain_A():
    name, seed = "G_Stain_A", 301
    rng = np.random.default_rng(seed)
    cv = canvas(name)
    RS.g_stain_a(cv, rng, seed, lobed, disc_field)
    return finish(cv, name, seed)


def G_Stain_B():
    name, seed = "G_Stain_B", 302
    rng = np.random.default_rng(seed)
    cv = canvas(name)
    RS.g_stain_b(cv, rng, seed, lobed, disc_field)
    return finish(cv, name, seed)


# ------------------------------------------------------------------ slime puddle
def G_Slime_A():
    """Round 2: an asymmetric splat - a thick pool (darker core) with an uneven rim, ONE tongue running out toward the
    upper right, droplets thrown to that side only (elongated along the throw), a contact ring that shows on cream."""
    name, seed = "G_Slime_A", 401
    rng = np.random.default_rng(seed)
    cv = Canvas(512, 512, 512 / 5.0, ss=2)      # round 4: drawn in 5-stud space, shown on the 6-stud carrier (1.2x)
    L = L_FLOOR
    nz = Field(seed, 0.9, 2, extent=(5, 5))
    w = 0.07 * nz(cv.XX, cv.YY)
    e = lobed(cv, [(2.0, 2.85, 0.88, 1.12, 0.9), (1.5, 2.3, 0.46, 1, 1), (2.5, 3.4, 0.5, 1, 1),
                   (1.2, 3.0, 0.3, 1, 1), (1.62, 3.62, 0.3, 1, 1), (2.6, 2.4, 0.5, 1, 1)], k=0.22, warp=1.6 * w)
    run = np.array([(2.45, 2.55), (2.9, 2.3), (3.25, 2.2), (3.5, 1.98)])
    tongue = raster_strokes(cv, [{"pts": run, "hw": np.array([0.55, 0.42, 0.34, 0.3])}], 0.3)
    e = smax(e, np.maximum(-tongue["sd"], -5.0), 0.14)
    e = smax(e, disc_field(cv, 3.62, 1.9, 0.36, warp=w), 0.1)            # blunt terminal lobe of the run-off
    from rec_stains import ellipse_field
    ang = math.atan2(-0.75, 1.0)
    for (x, y, l, wd) in ((4.3, 1.42, 0.17, 0.1), (4.48, 1.78, 0.12, 0.065), (4.12, 1.12, 0.11, 0.065),
                          (4.62, 1.25, 0.08, 0.05), (4.4, 0.95, 0.07, 0.04)):
        e = smax(e, ellipse_field(cv, x, y, l, wd, ang + rng.uniform(-0.3, 0.3)), 0.03)
    slime_paint(cv, e, L, ew=0.24, hmax=0.12, spec_lo=0.985, spec_hi=0.996, contact=0.46, thick_core=1.0)
    bubbles(cv, rng, e, L, 3, rr=(0.05, 0.1), min_e=0.25)
    return finish(cv, name, seed)


# ------------------------------------------------------------------ MossBase (seamless strips + end caps)
MB_W = 24.0
MB_PPS = 1024 / 24.0
MB_YC = 6.0          # contact line (floor top), studs from the top of the texture
MB_SEED = 700
# round 4: the mushier moss family (bright saturated greens + lime tips that survive the wall shade, dark wet damp halo)
from grime_lib import MOSS_LOOK_R5 as MOSS_LOOK  # noqa: E402  (round 5: olive-shifted, flat macro shading)
# floor cushions keep their round-4 volume (domes are right on the floor); only the colour changes
MOSS_LOOK_FLOOR = dict(MOSS_LOOK, dome=1.25, lump_k=1.0, cav_k=0.45)
H_CAP = 4.35          # damp height cap (its soft top then ends below the texture top edge + fade)
BAND = 1.5           # shared seam band half width (studs)
_MBF = None


def MB_FADE_NOISE(x):
    global _MBF
    if _MBF is None:
        _MBF = Field(MB_SEED + 33, 0.45, 2, extent=(24, 4), period_x=MB_W)
    x = np.asarray(x, float)
    return _MBF(x, np.full_like(x, 1.3))



def mb_dseam(x):
    xm = np.mod(x, MB_W)
    return np.minimum(xm, MB_W - xm)


def mb_weight(x):
    return 1 - smoothstep(BAND, 2 * BAND, mb_dseam(x))


def mb_profile(x, kind):
    """Damp-band height (studs above the floor) for the unique part of each output. Round 4: a TALLER wet band that
    sits above the taller moss (A about 3.4, B about 3.0 with rounded rising-damp wicks); the caps fade out smoothly."""
    x = np.asarray(x, float)
    xm = np.mod(x, MB_W)
    two_pi = 2 * np.pi
    nz = MB_FADE_NOISE(x)
    if kind == "A":
        h = 3.35 + 0.4 * np.sin(xm / MB_W * two_pi * 2 + 0.7) + 0.25 * np.sin(xm / MB_W * two_pi * 5 + 2.0) \
            + 0.12 * np.sin(xm / MB_W * two_pi * 11 + 0.4)
    elif kind == "B":
        h = 2.95 + 0.25 * np.sin(xm / MB_W * two_pi * 3 + 1.1) + 0.12 * np.sin(xm / MB_W * two_pi * 9 + 2.6)
        for c, amp, wdt in ((5.4, 0.6, 0.32), (6.05, 1.1, 0.42), (6.75, 0.8, 0.32), (7.5, 0.4, 0.28),
                            (16.3, 0.95, 0.36), (17.0, 0.55, 0.28), (17.8, 0.75, 0.32)):
            d = np.minimum(np.abs(xm - c), MB_W - np.abs(xm - c))
            h = h + amp * np.exp(-(d / wdt) ** 2) * (0.8 + 0.2 * nz)
    elif kind == "EndL":
        t = np.clip((x + 5.2) / 3.6 + 0.12 * np.sin(x * 1.3 + 0.8), 0, 1)
        h = 3.0 * np.sin(t * np.pi / 2) ** 1.2
        h = h + 0.42 * np.exp(-((x + 4.6) / 0.26) ** 2) + 0.3 * np.exp(-((x + 3.95) / 0.3) ** 2)  # round 6: lumpy end
    elif kind == "EndR":
        t = np.clip((5.2 - x) / 3.6 + 0.12 * np.sin(x * 1.3 + 2.1), 0, 1)
        h = 3.0 * np.sin(t * np.pi / 2) ** 1.2
        h = h + 0.38 * np.exp(-((x - 4.5) / 0.28) ** 2) + 0.32 * np.exp(-((x - 3.8) / 0.26) ** 2)
    else:
        h = np.zeros_like(x)
    return h


def mb_shared_profile(x):
    xm = np.mod(x, MB_W)
    d = np.minimum(xm, MB_W - xm) * np.sign(np.where(xm < MB_W / 2, 1, -1))
    return 3.0 + 0.18 * np.sin(d * 1.7)


def mb_damp(cv, kind, nzA, nzB):
    """Rising damp, round 4: a DARK wet band (alpha up to ~0.74 at the floor) fading upward, ragged top, a broken tide
    line on flat stretches only, and a subtle WET SHEEN (faint pale vertical streaks, as if the plastic were wet).
    Everything here is a function of x through periodic fields, so the seam band stays identical in every output."""
    X, Y = cv.XX, cv.YY

    def hfun(Xs):
        w = mb_weight(Xs) if kind in ("A", "B") else (1 - smoothstep(BAND, 2 * BAND, np.abs(Xs)))
        h0 = w * mb_shared_profile(Xs) + (1 - w) * mb_profile(Xs, kind)
        # round 6: in the caps (outside the shared band) the fine ragged-top octaves are damped -> no comb streaks
        ramp_k = 1.0 if kind in ("A", "B") else (w + (1 - w) * 0.4)
        h1 = h0 + (0.22 * nzA(Xs, Xs * 0 + 0.5) + ramp_k * (0.12 * nzA(2 * Xs, Xs * 0 + 3.3)
                   + 0.06 * nzA(4 * Xs, Xs * 0 + 5.1))) * smoothstep(0.7, 1.5, h0)
        # round 5: where the damp fades out (cap ends) a PROPORTIONAL wobble keeps the fade irregular without spikes
        if kind in ("EndL", "EndR"):      # caps: a wobbly fade over its whole length (outside the shared seam band)
            h1 = h1 + h0 * (0.24 * nzA(1.5 * Xs, Xs * 0 + 1.9) + 0.1 * nzA(3 * Xs, Xs * 0 + 6.2)) * (1 - w)
        else:
            h1 = h1 + h0 * (0.3 * nzA(1.5 * Xs, Xs * 0 + 1.9) + 0.12 * nzA(3 * Xs, Xs * 0 + 6.2)) * (1 - smoothstep(0.7, 1.5, h0))
        if kind == "EndR":                # final nit: EndR's fade kept faint vertical streaks -> smooth h(x) there
            xr, hr, wr = Xs[0], h1[0], w[0]
            dx_ = float(xr[1] - xr[0])
            k = np.arange(-int(0.75 / dx_), int(0.75 / dx_) + 1) * dx_
            g = np.exp(-0.5 * (k / 0.25) ** 2)
            g /= g.sum()
            pad = len(k) // 2
            hs = np.convolve(np.pad(hr, pad, mode="edge"), g, mode="valid")
            h1 = np.broadcast_to(wr * hr + (1 - wr) * hs, h1.shape)
        return -smax(-h1, -np.full_like(h1, H_CAP), 0.35)          # soft cap: the damp top stays inside the tile

    h = hfun(X)
    z = MB_YC - Y
    t = np.clip(z / np.maximum(h, 0.05), 0, 3)
    fade = 1 - smoothstep(0.85, 1.22, t)
    wc = None
    if kind in ("EndL", "EndR"):          # round 6: caps get a softer top fade + a wobbly outer end (outside the band)
        wc = 1 - smoothstep(BAND, 2 * BAND, np.abs(X))
        fade = wc * fade + (1 - wc) * (1 - smoothstep(0.7, 1.32, t))
        sgn = -1.0 if kind == "EndL" else 1.0
        zc = np.maximum(z, 0.25)          # constant through the hidden band, so the band stays intact
        xe = 5.2 - 0.22 * zc + 0.42 * nzB(X * 0 + 1.3, zc * 1.3) + 0.18 * nzA(X * 0 + 4.1, zc * 3.0)  # wobbly end
        fade = fade * smoothstep(-0.05, 0.45, xe - sgn * X)
    a = 0.74 * (1 - 0.6 * np.clip(t, 0, 1) ** 1.25) * fade
    a = a * smoothstep(0.02, 0.3, h) * np.clip(1 + 0.25 * nzB(X, Y) + 0.12 * nzA(3 * X, Y * 3), 0.45, 1.5)
    cv.over(P("WD1"), np.clip(a, 0, 0.78))
    # wet sheen: faint pale streaks running down the wet band (vertical noise), strongest mid-band
    sh = smoothstep(0.42, 0.75, nzA(6 * X, Y * 0.3 + 9.0)) * smoothstep(0.1, 0.35, t) * (1 - smoothstep(0.55, 0.9, t))
    sh = sh * smoothstep(0.6, 1.4, h) * (0.6 + 0.4 * smoothstep(-0.2, 0.4, nzB(2 * X, Y + 4.0)))
    if wc is not None:
        sh = sh * (wc + (1 - wc) * 0.4)
    cv.over(P("SH"), np.clip(0.11 * sh, 0, 0.12))
    slope = np.abs(hfun(X + 0.03) - hfun(X - 0.03)) / 0.06
    flat = 1 - smoothstep(0.25, 0.6, slope)
    brk = smoothstep(0.15, 0.45, 0.8 * nzA(0.5 * X, Y * 0 + 7.7) + 0.3 * nzB(X, Y * 0 + 3.1))
    tide = 0.22 * np.exp(-((z - 0.97 * h) / 0.055) ** 2) * smoothstep(0.9, 1.4, h) * brk * flat
    cv.over(P("WD2"), np.clip(tide, 0, 0.28))


def mb_base_run(sc, rng, x0, x1, light, Rr=(0.45, 1.0), big=(), gap_p=0.0, low=(), big_squash=(1.15, 0.85),
                base_squash=(1.25, 0.82)):
    """Cushions sitting on the contact line between x0 and x1, plus a few big ones. low = (xa, xb) slots where the
    moss stays <= ~1.1 studs tall (W_Crack_C slots)."""
    x = x0
    while x < x1:
        R = rng.uniform(*Rr)
        if any(a <= x <= b for a, b in low):
            R = min(R, 0.62)
        for a_, b_ in low:                    # round 4: a fat neighbour must not spill tall moss into the slot
            dd = (a_ - x) if x < a_ else (x - b_) if x > b_ else 0.0
            if 0 < dd < 3.0:
                R = min(R, 0.62 + dd / 1.35)
        if rng.random() >= gap_p:
            moss_cushion(sc, rng, x, MB_YC + 0.12, R, light, r_rng=(0.085, 0.19), squash=base_squash, tip_p=0.55,
                         min_r=0.075, region=lambda px, py: py < MB_YC + 0.3)
        x += R * rng.uniform(1.0, 1.6)
    for (bx, bR) in big:
        moss_cushion(sc, rng, bx, MB_YC + 0.2, bR, light, r_rng=(0.09, 0.2), squash=big_squash, tip_p=0.6,
                     min_r=0.075, region=lambda px, py: py < MB_YC + 0.3)


def mb_tongue(sc, rng, x, top, light, wander=0.5, foot=1.05, top_r=0.26, lean=None):
    """A ragged CLIMBING TONGUE: a modest foot, then a column of overlapping cushions that narrows toward the top,
    leans to one side (round 6: the lean is given, so the two tongues of a tile lean opposite ways) and has ragged
    flanks. Round 6: the top is BLUNT and broken - a cluster of 3 lumps across the top, not a spire point."""
    lean = rng.uniform(-0.3, 0.3) * wander if lean is None else lean
    moss_cushion(sc, rng, x, MB_YC - 0.6, foot, light, r_rng=(0.085, 0.16), squash=(1.45, 0.8), tip_p=0.5,
                 min_r=0.08)
    z = 1.1
    xx = x
    top_c = top - 0.45                             # the column stops below the top; the lump cluster finishes it
    while z < top_c:
        f = min(1.0, (z - 1.1) / max(top_c - 1.1, 1e-6))
        R = (foot * 0.62) * (1 - f) ** 0.8 + max(top_r, 0.34)
        xx = x + lean * f + 0.15 * math.sin(z * 2.1 + x) * wander + rng.uniform(-0.08, 0.08)
        moss_cushion(sc, rng, xx, MB_YC - z, R, light, r_rng=(0.08, 0.14),
                     squash=(rng.uniform(1.1, 1.3), rng.uniform(0.8, 0.95)), tip_p=0.5, min_r=0.075, edge_keep=0.14)
        for side in (-1, 1):                       # ragged flanks: side cushions that touch the column
            if rng.random() < 0.5:
                moss_cushion(sc, rng, xx + side * R * rng.uniform(0.75, 1.0), MB_YC - z + rng.uniform(-0.1, 0.15),
                             R * rng.uniform(0.4, 0.6), light, r_rng=(0.075, 0.12), tip_p=0.5, min_r=0.075,
                             edge_keep=0.1)
        z += R * rng.uniform(0.55, 0.75)
    # blunt, broken top: three lumps across the tip - the middle one highest, the side ones lower and smaller, so the
    # top is neither a spire point nor a flat block
    for dx, dz, r in ((-0.36, 0.32, 0.27), (0.02, 0.0, 0.34), (0.37, 0.2, 0.29)):
        moss_cushion(sc, rng, xx + lean * 0.35 + dx + rng.uniform(-0.06, 0.06), MB_YC - top + 0.3 + dz,
                     r * rng.uniform(0.9, 1.1), light, r_rng=(0.075, 0.12), squash=(1.1, 0.95), tip_p=0.5, min_r=0.075,
                     edge_keep=0.1)


def mb_mass(sc, rng, x, light, top=2.1, half=2.6, lumps=(-0.45, 0.4), half_r=None, lump_spec=None):
    """Round 6: a broad moss MASS with ROUNDED SHOULDERS: 1-2 tall centre cushions (a short top), then lower shoulder
    cushions that reach the full half-width, so the sides fall at about 45-55 deg; the top line is broken by 1-2
    lumps - no clipped box hedge, no flat top. half = half-width at the foot (studs)."""
    region = lambda px, py: py < MB_YC + 0.3                                  # noqa: E731
    Rc = top / 1.45
    offs = (-0.45 * (half - 2.0), 0.45 * (half - 2.0)) if half > 2.6 else (0.0,)
    for o in offs:
        moss_cushion(sc, rng, x + o, MB_YC + 0.1, Rc, light, r_rng=(0.09, 0.19), squash=(1.05, 1.45), tip_p=0.6,
                     min_r=0.08, region=region)
    Rs = 0.55 * top
    for side in (-1, 1):
        hw = half if (side < 0 or half_r is None) else half_r
        moss_cushion(sc, rng, x + side * (hw - Rs * 1.12), MB_YC + 0.1, Rs, light, r_rng=(0.09, 0.17),
                     squash=(1.25, 1.1), tip_p=0.55, min_r=0.08, region=region)
    if lump_spec is None:
        for dx in lumps:
            moss_cushion(sc, rng, x + dx + rng.uniform(-0.1, 0.1), MB_YC - top + 0.05, rng.uniform(0.38, 0.46), light,
                         r_rng=(0.08, 0.14), squash=(1.2, 0.9), tip_p=0.55, min_r=0.075, edge_keep=0.1)
    else:                                   # (dx, drop below the top, radius): round lumps at different heights
        for dx, dz, r in lump_spec:
            moss_cushion(sc, rng, x + dx, MB_YC - top + 0.05 + dz, r, light, r_rng=(0.08, 0.14), squash=(1.0, 1.05),
                         tip_p=0.55, min_r=0.075, edge_keep=0.1)


def mb_spores(sc, rng, x0, x1, n, light, zmax=5.0):
    """Satellite bits ATTACHED to the moss mass (round 2): each sits within 0.1-0.4 stud above/beside an existing
    clump near the top of the mass, and gets smaller the further out it is. ~30 % of the round-1 count."""
    base = [c for c in sc.clumps if x0 <= c[0] <= x1 and c[1] < MB_YC + 0.05]
    if not base:
        return
    base.sort(key=lambda c: c[1])                    # highest (smallest y) first
    top = base[:max(3, len(base) // 4)]
    for _ in range(n):
        cx, cy, r = top[int(rng.integers(0, len(top)))][:3]
        ang = rng.uniform(-math.pi * 0.85, -math.pi * 0.15)   # upward-ish (texture y down)
        d = rng.uniform(0.1, 0.4)
        x, y = cx + math.cos(ang) * (r + d), cy + math.sin(ang) * (r + d)
        if MB_YC - y > zmax:
            continue
        R = rng.uniform(0.1, 0.17) * (1 - d / 0.6)
        moss_cushion(sc, rng, x, y, R, light, r_rng=(0.075, 0.11), tip_p=0.45, min_r=0.075, edge_keep=0.06)


def mb_shared_scene():
    """The shared seam set (round 5): a thick base mat + a LOW mound (<= ~1.5 studs) centred on every join, identical in
    every MossBase output, so the chain is continuous but does not pulse every 24 studs."""
    rng = np.random.default_rng(MB_SEED + 50)
    sc = MossScene()
    mb_base_run(sc, rng, -1.25, 1.25, L_WALL, Rr=(0.65, 0.9), base_squash=(1.3, 1.05))
    moss_cushion(sc, rng, 0.0, MB_YC + 0.12, 1.05, L_WALL, r_rng=(0.09, 0.17), squash=(1.35, 1.12), tip_p=0.55,
                 min_r=0.08, region=lambda px, py: py < MB_YC + 0.3)
    return sc


def ok_unique(x, R):
    return mb_dseam(np.array([x]))[0] >= BAND + 1.3 * R + 0.45


def mb_unique_scene(kind):
    """Round 4 "mushier": dense base runs, big mounds up to ~3-3.5 studs, plumes climbing to ~4.5-5 in places; the
    W_Crack_C low-moss slots (A 6.7-10.3, B 12.2-15.8) stay <= ~1.1 stud."""
    rng = np.random.default_rng(MB_SEED + {"A": 1, "B": 2, "EndL": 3, "EndR": 4}[kind])
    sc = MossScene()
    L = L_WALL
    lo, hi = BAND + 0.45 + 0.9, MB_W - (BAND + 0.45 + 0.9)
    if kind == "A":
        # round 5: thick 1-2 stud mat, two broad masses capped near 3 studs at uneven spacing, two ragged tongues
        mb_base_run(sc, rng, lo, hi, L, Rr=(0.95, 1.35), low=((6.7, 10.3),), base_squash=(1.35, 1.1))
        mb_mass(MossScene(), rng, 4.4, L, top=2.5, half=2.3, lumps=(-0.45, 0.35))   # draws kept, result discarded
        # final nit: A's first mass rebuilt clear of the seam-band filter (no clipped vertical left flank), a low
        # cushion filling the mat gap left of it, round top lumps instead of a flat slab; own rng -> rest of A identical
        r1 = np.random.default_rng(MB_SEED + 71)
        mb_mass(sc, r1, 4.6, L, top=2.5, half=2.0, half_r=2.0,
                lump_spec=((-0.42, 0.12, 0.4), (0.4, 0.34, 0.3)))
        moss_cushion(sc, r1, 2.45, MB_YC + 0.12, 0.62, L, r_rng=(0.08, 0.12), squash=(1.35, 1.0), tip_p=0.55,
                     min_r=0.075, region=lambda px, py: py < MB_YC + 0.3)
        # a low filler that closes the mat gap between the shared seam moss (ends ~1.56) and the unique zone (~2.03);
        # it is kept outside the 1.125-stud identity band (its halo reaches ~1.3), so every join stays identical
        fill = MossScene()
        moss_cushion(fill, r1, 1.95, MB_YC + 0.05, 0.42, L, r_rng=(0.075, 0.1), squash=(1.35, 1.0), tip_p=0.5,
                     min_r=0.075, region=lambda px, py: py < MB_YC + 0.3)

        def below_slope(x, y, r):         # left flank of that mass: nothing above a ~49 deg line from the mat
            return not (1.9 <= x <= 4.0 and (MB_YC - y + r) > 0.6 + 1.15 * (x - 2.1))
        sc.clumps = [c for c in sc.clumps if below_slope(c[0], c[1], c[2])]
        sc.stips = [st for st in sc.stips if below_slope(st[0], st[1], st[2])]
        sc.lumps = [lm for lm in sc.lumps if below_slope(lm[0], lm[1], lm[2])]
        mb_mass(sc, rng, 15.5, L, top=2.7, half=3.8, lumps=(-0.7, 0.55))
        mb_tongue(sc, rng, 13.7, 4.0, L, foot=1.1, top_r=0.32, wander=0.9, lean=0.55)     # leans right
        mb_tongue(sc, rng, 20.7, 3.3, L, foot=1.0, top_r=0.3, wander=0.8, lean=-0.5)      # leans left
        mb_spores(sc, rng, lo, hi, 4, L, zmax=4.6)
    elif kind == "B":
        mb_base_run(sc, rng, lo, hi, L, Rr=(0.85, 1.25), gap_p=0.04, low=((12.2, 15.8),), base_squash=(1.35, 1.05))
        mb_mass(sc, rng, 9.2, L, top=2.5, half=3.0, lumps=(-0.5, 0.4))
        mb_mass(sc, rng, 19.4, L, top=2.6, half=2.5, lumps=(-0.4, 0.45))
        mb_tongue(sc, rng, 5.9, 4.05, L, wander=0.9, foot=1.15, top_r=0.32, lean=-0.55)   # leans left
        mb_tongue(sc, rng, 17.5, 3.1, L, wander=0.8, foot=1.0, top_r=0.3, lean=0.5)       # leans right
        mb_spores(sc, rng, lo, hi, 3, L, zmax=4.6)
    elif kind == "EndL":
        x = -(BAND + 0.45 + 0.75)
        while x > -4.9:
            f = (-x - 2.0) / 3.0
            R = 0.95 * (1 - 0.62 * f)
            if rng.random() < 1 - 0.4 * f:
                moss_cushion(sc, rng, x, MB_YC + 0.12, R, L, r_rng=(0.09, 0.17), squash=(1.25, 1.1 - 0.3 * f),
                             tip_p=0.55, min_r=0.08, region=lambda px, py: py < MB_YC + 0.3)
            x -= R * rng.uniform(0.9, 1.4)
    elif kind == "EndR":
        x = BAND + 0.45 + 0.75
        while x < 4.9:
            f = (x - 2.0) / 3.0
            R = 0.95 * (1 - 0.62 * f)
            if rng.random() < 1 - 0.4 * f:
                moss_cushion(sc, rng, x, MB_YC + 0.12, R, L, r_rng=(0.09, 0.17), squash=(1.25, 1.1 - 0.3 * f),
                             tip_p=0.55, min_r=0.08, region=lambda px, py: py < MB_YC + 0.3)
            x += R * rng.uniform(0.9, 1.4)
    # keep the seam band free of unique objects (+ their halo reach)
    sc.clumps = [c for c in sc.clumps if mb_dseam(np.array([c[0]]))[0] >= BAND + 0.45 + c[2]]
    sc.stips = [s for s in sc.stips if mb_dseam(np.array([s[0]]))[0] >= BAND + 0.45]
    sc.lumps = [lm for lm in sc.lumps if mb_dseam(np.array([lm[0]]))[0] >= BAND + 0.45 + 1.1 * lm[2]]
    if kind == "A":
        sc.clumps += [c for c in fill.clumps if c[0] >= 1.62 + c[2]]
        sc.stips += [st for st in fill.stips if st[0] >= 1.62]
        sc.lumps += [lm for lm in fill.lumps if lm[0] >= 1.62 + lm[2]]
    return sc


def mossbase(kind):
    name = {"A": "W_MossBase_A", "B": "W_MossBase_B", "EndL": "W_MossBase_EndL", "EndR": "W_MossBase_EndR"}[kind]
    seed = MB_SEED + 10 + len(kind)
    nzA = Field(MB_SEED + 21, 1.2, 3, extent=(24, 7), period_x=MB_W)
    nzB = Field(MB_SEED + 22, 1.6, 2, extent=(24, 7), period_x=MB_W)
    sc = mb_shared_scene().extend(mb_unique_scene(kind))
    if kind in ("A", "B"):
        cv = Canvas(1024, 272, MB_PPS, ss=2, x0=0.0, y0=0.0, period=MB_W)
        mb_damp(cv, kind, nzA, nzB)
        moss_render(cv, sc, L_WALL, halo_a=0.24, halo_w=0.12, shadow_a=0.24, wrap=True, noise_period=MB_W, fine=0.14,
                    dying_gate=lambda X: smoothstep(BAND + 0.4, BAND + 1.2, mb_dseam(X)), **MOSS_LOOK)
        cv.fade(edge_fade(cv, keep=("l", "r"), ramps=contact_ramps(name)))
        rgb, a = cv.finish()
    else:
        # render a wider window (3 studs of seam context) so blurs near the inner edge match the strips exactly
        x0 = -6.0 if kind == "EndL" else -3.0
        cv = Canvas(384, 272, MB_PPS, ss=2, x0=x0, y0=0.0, period=None)
        mb_damp(cv, kind, nzA, nzB)
        moss_render(cv, sc, L_WALL, halo_a=0.24, halo_w=0.12, shadow_a=0.24, wrap=False, noise_period=MB_W, fine=0.14,
                    dying_gate=lambda X: smoothstep(BAND + 0.4, BAND + 1.2, mb_dseam(X)), **MOSS_LOOK)
        keep = ("r",) if kind == "EndL" else ("l",)
        # fade only the outer edge + top/bottom; inner edge keeps content
        full = edge_fade(cv, keep=("l", "r"), ramps=contact_ramps(name))
        outer = edge_fade(cv, keep=("r", "t", "b") if kind == "EndL" else ("l", "t", "b"))
        cv.fade(full * outer)
        rgb, a = cv.finish()
        if kind == "EndL":
            rgb, a = rgb[:, :256], a[:, :256]
        else:
            rgb, a = rgb[:, 128:], a[:, 128:]
    sp = SPECS[name]
    meta = {"studs": list(sp["studs"]), "px_per_stud": round(MB_PPS, 2), "surface": "wall",
            "contact_edge": "bottom", "hidden_band_studs": 0.375}
    return export((rgb, a), os.path.join(DECALS, name + ".png"), keep=sp["keep"], seed=seed, meta=meta)


def W_MossBase_A():
    return mossbase("A")


def W_MossBase_B():
    return mossbase("B")


def W_MossBase_EndL():
    return mossbase("EndL")


def W_MossBase_EndR():
    return mossbase("EndR")


# ------------------------------------------------------------------ drips
def W_Drip_A():
    name, seed = "W_Drip_A", 601
    rng = np.random.default_rng(seed)
    cv = canvas(name)
    L = L_WALL
    yc = 0.35   # contact line (trim bottom); hidden band above it up to the 4 px margin
    X, Y = cv.XX, cv.YY
    nz = Field(seed, 0.8, 3, extent=(4, 12))
    n2 = Field(seed + 9, 0.35, 2, extent=(4, 12))
    z = Y - yc
    # seep band under the trim: dense at the trim, ragged soft lower edge
    band_h = 0.45 + 0.18 * nz(X, X * 0 + 0.3) + 0.08 * n2(X, X * 0 + 1.1)
    tb = np.clip(z / band_h, -2, 2)
    a_band = 0.42 * (1 - smoothstep(0.35, 1.15, tb)) + 0.2 * (z < 0)
    streaks = ((0.8, 3.2, 0.5), (1.72, 9.6, 0.72), (2.55, 5.8, 0.58), (3.25, 7.6, 0.52))
    a_st = np.zeros_like(X)
    for (x0, Ls, wt) in streaks:
        yy = np.clip(z, 0, Ls)
        f = yy / Ls
        cx = x0 + 0.12 * nz(yy * 0.5 + x0 * 3, np.full_like(yy, 2.0)) + 0.05 * f
        hw = (wt * (1 - f ** 0.8) + 0.13 * f ** 0.8) / 2 * (1 + 0.25 * n2(yy * 2 + x0, np.full_like(yy, 4.0)))
        d = np.abs(X - cx)
        edge = 1 - smoothstep(hw * 0.55, hw * 1.15, d)
        dens = (0.5 - 0.22 * f) * (1 + 0.2 * n2(X * 2, Y * 0.7))
        tip = 1 - smoothstep(Ls - 0.15, Ls + 0.12, z)
        drop = 0.1 * np.exp(-((z - Ls + 0.2) / 0.3) ** 2)
        a_st = np.maximum(a_st, (dens + drop) * edge * tip * (z > -0.05))
        # faint tide edges along the sides of the streak, broken
        sides = 0.07 * np.exp(-((d - hw) / 0.035) ** 2) * tip * (z > 0.3) * smoothstep(-0.2, 0.4, n2(X * 3, Y))
        a_st = a_st + sides
    a = np.clip(np.maximum(a_band, a_st) + 0.4 * np.minimum(a_band, a_st), 0, 0.62)
    cv.over(P("W1"), a)
    sc = MossScene()
    for (x, R) in ((1.05, 0.22), (2.85, 0.17), (2.05, 0.12)):
        moss_cushion(sc, rng, x, yc - 0.13, R * 1.2, L, r_rng=(0.05, 0.1), squash=(1.4, 1.15), tip_p=0.5, min_r=0.045)
    moss_render(cv, sc, L, halo_a=0.12, halo_w=0.05, shadow_a=0.18)
    return finish(cv, name, seed)


def W_Drip_B():
    name, seed = "W_Drip_B", 602
    rng = np.random.default_rng(seed)
    cv = canvas(name)
    L = L_WALL
    yc = 0.35
    X, Y = cv.XX, cv.YY
    z = Y - yc
    nz = Field(seed, 0.6, 2, extent=(4, 9))
    # the band thins out to nothing at the left end and ends in a rounded ooze lobe at the right end
    uL = np.clip((X - 0.3) / 1.05, 0, 1)
    envL = np.sqrt(1 - (1 - uL) ** 2)                                 # round 3: rounded, sagging left end
    env = envL * (1 - smoothstep(3.25, 3.75, X)) ** 0.7
    band_h = (0.55 + 0.13 * nz(X, X * 0 + 0.4)) * env - 0.06
    e = band_h - z
    sag = 0.17 - np.sqrt(((X - 0.66) / 1.0) ** 2 + ((z - 0.36) / 1.2) ** 2)    # goo sagging at the end
    e = smax(e, sag, 0.08)
    lobe = 0.26 - np.sqrt(((X - 3.45) / 1.0) ** 2 + ((z - 0.32) / 1.25) ** 2)       # ooze lobe at the right end
    e = smax(e, lobe, 0.1)
    # hidden part (behind the trim) also rounded at both ends
    e = np.minimum(e, np.minimum(X - 0.3, 3.82 - X) + 0.3 * (z > -0.02))
    e = np.minimum(e, z + 0.31)  # top of the goo stays inside the hidden band (4 px margin above)
    drips = ((0.95, 1.2, 0.13, 0.15), (1.42, 6.5, 0.2, 0.24), (2.18, 2.6, 0.17, 0.2), (2.86, 4.2, 0.18, 0.21),
             (3.45, 1.1, 0.14, 0.17))
    for (x0, Ld, w0, rb) in drips:
        yy = np.clip(z, 0, Ld)
        t = yy / Ld
        cx = x0 + 0.05 * np.sin(yy * 1.7 + x0 * 5)
        hw = w0 * (1 - 0.6 * t ** 0.7)
        el = hw - np.abs(X - cx)
        el = np.where((z >= -0.05) & (z <= Ld), el, -1.0)
        cxe = x0 + 0.05 * math.sin(Ld * 1.7 + x0 * 5)
        bulb = rb - np.sqrt((X - cxe) ** 2 + ((z - Ld) * 1.12) ** 2)
        e = smax(e, smax(el, bulb, 0.1), 0.1)
    # detached drop under the longest drip (teardrop)
    dx, dz = 1.42 + 0.05 * math.sin(6.5 * 1.7 + 1.42 * 5), 6.5 + 0.62
    drop = 0.12 - np.sqrt((X - dx) ** 2 + ((z - dz) * 1.0) ** 2)
    tail = 0.05 * (1 - np.clip((dz - z) / 0.28, 0, 1)) - np.abs(X - dx)
    tail = np.where((z < dz) & (z > dz - 0.28), tail, -1)
    e = np.maximum(e, smax(drop, tail, 0.05))
    # faint old trail below the longest drip
    trail_e = 0.07 - np.abs(X - dx)
    tr = 0.14 * smoothstep(-0.01, 0.03, trail_e) * smoothstep(6.6, 7.0, z) * (1 - smoothstep(7.6, 8.0, z))
    cv.over(P("W1"), tr)
    slime_paint(cv, e, L, ew=0.16, hmax=0.1, contact=0.3, spec_lo=0.975, spec_hi=0.99)
    bubbles(cv, rng, e, L, 2, rr=(0.04, 0.06), min_e=0.14)
    return finish(cv, name, seed)


ALL = ["G_Crack_A", "G_Crack_B", "G_Crack_C", "G_Moss_A", "G_Moss_B", "G_Stain_A", "G_Stain_B", "G_Slime_A",
       "W_Crack_A", "W_Crack_B", "W_Crack_C", "W_MossBase_A", "W_MossBase_B", "W_MossBase_EndL", "W_MossBase_EndR",
       "W_Drip_A", "W_Drip_B"]


def main(names):
    path = os.path.join(HERE, "checks.json")
    checks = {}
    if os.path.exists(path):
        try:
            checks = json.load(open(path))
        except Exception:
            checks = {}
    for n in names:
        t0 = time.time()
        res = globals()[n]()
        res["seconds"] = round(time.time() - t0, 1)
        checks[n] = res
        flag = "OK " if (res["edge_rule_ok"] and res["fringe_ok"] and res["max_side_ok"]) else "BAD"
        print(f"{flag} {n:18s} {res['w']}x{res['h']} edges={res['edges_with_content']} "
              f"fringe={res['fringe_max_err_255']} transp={res['transparent_pct']}% t={res['seconds']}s", flush=True)
    checks = {k: checks[k] for k in ALL if k in checks}
    with open(path, "w") as f:
        json.dump(checks, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1:] or ALL)
