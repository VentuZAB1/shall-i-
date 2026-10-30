# HubGrime - round-2 stains (REVIEW.md MUST 2 + NICE 4): wet-ground watermarks that cannot be read as cast shadows.
#   * the hue shifts, not just the value: deep OLIVE (G_Stain_A) / warm UMBER (G_Stain_B), more saturated than the
#     ground (a shadow desaturates);
#   * watermark structure: lighter interior (alpha ~0.25-0.3), a CRISP darker rim band (alpha ~0.6, ~0.13-0.15 stud),
#     1-2 broken inner rings -> it survives 5x foreshortening as a ring, not a solid blob;
#   * drops are irregular and elongated (no round rivets), with no rim of their own.
import math

import numpy as np

from grime_lib import P, Field, chain_path, cov_from_sd, raster_strokes, smax, smoothstep


def ellipse_field(cv, cx, cy, rx, ry, ang, warp=None):
    """~signed distance (studs, >0 inside) of a rotated ellipse, optionally warped."""
    c, s = math.cos(ang), math.sin(ang)
    dx, dy = cv.XX - cx, cv.YY - cy
    u = (dx * c + dy * s) / rx
    v = (-dx * s + dy * c) / ry
    rho = np.sqrt(u * u + v * v)
    if warp is not None:
        rho = rho * (1 + warp)
    return (1 - rho) * min(rx, ry)


def watermark(cv, e, col, rim_col, seed, a_in=0.26, rim_a=0.6, rim_w=0.14, rings=((0.55, 0.26), (1.2, 0.18)),
              mottle=0.22, centre_lift=0.25, core_w=1.6, centre=None, breaks=(), width_var=0.0):
    X, Y = cv.XX, cv.YY
    ext, org = (cv.ws + 4, cv.hs + 4), (cv.x0 - 2, cv.y0 - 2)
    n1 = Field(seed + 81, 0.8, 2, extent=ext, origin=org)(X, Y)
    n2 = Field(seed + 82, 2.0, 2, extent=ext, origin=org)(X, Y)
    n3 = Field(seed + 83, 0.35, 2, extent=ext, origin=org)(X, Y)
    inside = cov_from_sd(cv, -e)            # crisp 1 px edge
    mot = np.clip(1 + mottle * n2 + 0.5 * mottle * n1, 0.5, 1.6)
    lift = 1 - centre_lift * smoothstep(0.3, core_w, e)   # the middle is lighter (dried)
    cv.over(P(col), np.clip(a_in * mot * lift * inside, 0, 0.5))
    rw, gap = rim_w, 1.0
    if centre is not None:
        # round 3: the rim varies in width around the outline and is BROKEN in a few places (angle around centre)
        th = np.arctan2(Y - centre[1], X - centre[0])
        nth = Field(seed + 84, 0.9, 2, extent=(4, 4), origin=(-2, -2))(np.cos(th) * 1.2, np.sin(th) * 1.2)
        rw = rim_w * (1 + width_var * np.clip(nth * 1.6, -1, 1))
        for (ang, half) in breaks:
            dth = np.abs(np.angle(np.exp(1j * (th - ang))))
            gap = gap * (0.12 + 0.88 * smoothstep(half * 0.5, half, dth))
    rim = inside * (1 - smoothstep(rw * 0.45, rw, e)) * (0.82 + 0.18 * smoothstep(-0.3, 0.4, n3)) * gap
    cv.over(P(rim_col), np.clip(rim_a * rim, 0, 0.7))
    for r, ra in rings:
        ring = ra * np.exp(-((e - r) / 0.035) ** 2) * smoothstep(-0.15, 0.35, n1 + 0.4 * n3) * inside
        cv.over(P(rim_col), np.clip(ring, 0, 0.5))


def gloss(cv, e, rng, seed, n=26, min_e=0.35, ang=0.35, size=(0.07, 0.2), a=(0.5, 0.78), sheen=None, meniscus=None,
          wmax=None):
    """Round 4: WET GLOSS - small elongated specular flecks (sky reflections, all roughly one direction) scattered
    over the wet interior (never on the rim), plus an optional soft broad sheen patch. They make the stain read as wet
    and glossy, which a cast shadow never is."""
    ys, xs = np.nonzero(e > min_e)
    if len(xs) == 0:
        return
    for _ in range(n):
        i = int(rng.integers(0, len(xs)))
        x, y = cv.XX[ys[i], xs[i]], cv.YY[ys[i], xs[i]]
        L = rng.uniform(*size)
        w = L * rng.uniform(0.28, 0.45)
        if wmax:
            w = min(w, wmax)
        th = ang + rng.uniform(-0.35, 0.35)
        ef = ellipse_field(cv, x, y, L / 2, w / 2, th)
        core = smoothstep(-0.006, 0.03, ef)
        cv.over(P("GL"), rng.uniform(*a) * core * smoothstep(min_e * 0.6, min_e, e))
    if meniscus:                          # a thin, broken sky-reflection line just inside the far-side rim
        nb = Field(seed + 95, 0.35, 2, extent=(cv.ws + 4, cv.hs + 4), origin=(cv.x0 - 2, cv.y0 - 2))(cv.XX, cv.YY)
        far = smoothstep(meniscus[0] + 1.2, meniscus[0] - 0.6, cv.YY)          # upper part of the image
        line = np.exp(-((e - 0.09) / 0.028) ** 2) * far * smoothstep(-0.05, 0.25, nb)
        cv.over(P("GL"), np.clip(meniscus[1] * line, 0, 0.6))
    if sheen is not None:
        sx, sy, sr = sheen
        d = np.sqrt((cv.XX - sx) ** 2 + ((cv.YY - sy) * 1.6) ** 2)
        cv.over(P("SH"), 0.07 * (1 - smoothstep(0.1 * sr, sr, d)) * smoothstep(0.1, 0.4, e))


def drops(cv, specs, col, rim_col, seed, a=0.42):
    """Irregular elongated drops: (x, y, length, width, angle). Soft-cored, slightly darker toward the tail end."""
    ext, org = (cv.ws + 4, cv.hs + 4), (cv.x0 - 2, cv.y0 - 2)
    warp = 0.18 * Field(seed + 91, 0.12, 2, extent=ext, origin=org)(cv.XX, cv.YY)
    for (x, y, L, w, ang) in specs:
        e = ellipse_field(cv, x, y, L / 2, w / 2, ang, warp=warp)
        # a small trailing lobe makes it a splash, not an ellipse
        e = smax(e, ellipse_field(cv, x - math.cos(ang) * L * 0.45, y - math.sin(ang) * L * 0.45, L * 0.18, w * 0.32,
                                  ang, warp=warp), 0.02)
        cov = cov_from_sd(cv, -e)
        cv.over(P(col), a * cov)
        cv.over(P(rim_col), 0.3 * cov * (1 - smoothstep(0.0, 0.05, e)))


def g_stain_a(cv, rng, seed, lobed, disc_field):
    """Damp watermark puddle: olive, lighter middle, crisp dark rim, two broken inner rings, a few thrown drops."""
    from grime_lib import Field as F
    w = 0.16 * F(seed, 2.0, 3, extent=(10, 10))(cv.XX, cv.YY) + 0.07 * F(seed + 5, 0.6, 2, extent=(10, 10))(cv.XX, cv.YY)
    # round 3: one lobe is a long flat run-off (not a round "ear"), the upper-left lobe is squashed too
    e = lobed(cv, [(4.7, 5.2, 2.2, 1.15, 0.85), (3.0, 4.15, 1.2, 1.25, 0.72), (7.2, 6.55, 1.25, 1.65, 0.55),
                   (6.2, 3.6, 0.95, 1, 1), (3.4, 6.6, 0.9, 1, 1), (2.2, 5.3, 0.7, 1, 1), (7.8, 5.2, 0.8, 1, 1)],
              k=0.55, warp=1.25 * w)
    # round 4: wetter + darker + a deeper green tint, a clearly DEFINED tide edge (2 short breaks only), gloss
    watermark(cv, e, "SW1", "SW2", seed, a_in=0.4, rim_a=0.74, rim_w=0.13, rings=((0.5, 0.28), (1.2, 0.22)),
              centre=(4.9, 5.2), breaks=((-2.45, 0.2), (1.95, 0.17)), width_var=0.35, centre_lift=0.18)
    gloss(cv, e, np.random.default_rng(seed + 900), seed, n=14, min_e=0.35, ang=0.35, size=(0.22, 0.48),
          a=(0.26, 0.42), sheen=(4.4, 4.7, 1.6), meniscus=(4.2, 0.42), wmax=0.07)   # round 5: 14 long faint streaks
    c = np.array([5.0, 5.2])
    specs = []
    for ang, dist, L in ((0.6, 3.9, 0.42), (0.95, 4.2, 0.26), (2.6, 3.7, 0.34), (4.1, 3.6, 0.3), (5.5, 3.9, 0.22)):
        x, y = c[0] + math.cos(ang) * dist, c[1] + math.sin(ang) * dist
        specs.append((x, y, L, L * rng.uniform(0.38, 0.5), ang + rng.uniform(-0.25, 0.25)))
    drops(cv, specs, "SW1", "SW2", seed, a=0.5)


def g_stain_b(cv, rng, seed, lobed, disc_field):
    """Mud SKID/DRAG (warm umber), drag direction +x: a dense irregular splash head (no round blob), then broad
    overlapping scuff streaks that fan out, break up and taper (different lengths, gaps), a broken edge, elongated
    splatter thrown ahead and to the sides. Watermark structure on the wide parts only (no outlined 'tentacles')."""
    from grime_lib import Field as F, blur
    X, Y = cv.XX, cv.YY
    w = 0.2 * F(seed, 1.2, 3, extent=(12, 8))(X, Y) + 0.08 * F(seed + 5, 0.4, 2, extent=(12, 8))(X, Y)
    head = lobed(cv, [(2.4, 4.15, 0.78, 0.8, 1.15), (2.0, 3.55, 0.45, 1, 1), (2.15, 4.85, 0.42, 1, 1),
                      (2.85, 4.2, 0.6, 1.2, 1.0)], k=0.3, warp=w)
    strokes = []
    gaps = F(seed + 6, 0.7, 2, extent=(40, 40))
    lanes = ((-0.95, 3.2, 0.3), (-0.62, 6.2, 0.42), (-0.3, 4.6, 0.46), (0.02, 8.0, 0.5), (0.34, 5.6, 0.46),
             (0.66, 7.0, 0.4), (0.98, 3.8, 0.28))
    for k, (dy, L, hw0) in enumerate(lanes):
        x0, y0 = 2.5, 4.2 + dy * 0.6
        x1, y1 = x0 + L, 4.2 + dy * (1.0 + 0.12 * L) + rng.uniform(-0.15, 0.15)
        pts = chain_path(rng, [(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + rng.uniform(-0.12, 0.12)), (x1, y1)],
                         seg=(0.5, 1.0), dev=6)
        t = np.linspace(0, 1, len(pts))
        hw = 0.02 + (hw0 - 0.02) * (1 - t) ** 1.15 * (1 + 0.18 * np.sin(t * 13 + k * 1.7))
        # broken lanes: pinch to nothing in a gap or two
        g = gaps(pts[:, 0] * 1.0 + k * 3.1, np.full(len(pts), 1.0 + k))
        hw = hw * np.clip(0.2 + 1.6 * (g + 0.35), 0.0, 1.0) ** 0.6
        strokes.append({"pts": pts, "hw": np.maximum(hw, 0.004)})
    f = raster_strokes(cv, strokes, 0.6)
    e_st = np.maximum(-f["sd"], -5.0)   # clamp: a 1e9 "far" distance would cancel catastrophically in float32
    e = smax(head, e_st, 0.22)
    e = e + 0.045 * F(seed + 7, 0.16, 2, extent=(12, 8))(X, Y)   # broken, irregular edge
    s_along = np.clip((X - 2.5) / 8.0, 0, 1)
    n2 = F(seed + 82, 1.6, 2, extent=(12, 8))(X, Y)
    n3 = F(seed + 83, 0.3, 2, extent=(12, 8))(X, Y)
    inside = cov_from_sd(cv, -e)
    lift = 1 - 0.3 * smoothstep(0.25, 0.8, e)
    a_in = 0.54 * (1 - 0.4 * s_along)                       # round 4: wetter / darker umber
    cv.over(P("SU3"), np.clip(a_in * (1 + 0.22 * n2) * lift * inside, 0, 0.6))
    wide = smoothstep(0.05, 0.12, blur(np.maximum(e, 0).astype(np.float32), cv.px(0.1)))
    rim = inside * (1 - smoothstep(0.05, 0.12, e)) * (0.8 + 0.2 * smoothstep(-0.3, 0.4, n3)) * wide
    cv.over(P("SU4"), np.clip(0.7 * rim * (1 - 0.35 * s_along), 0, 0.78))
    ring = 0.22 * np.exp(-((e - 0.36) / 0.035) ** 2) * smoothstep(-0.1, 0.35, n3) * inside * (head > -0.1)
    cv.over(P("SU2"), ring)
    specs = []
    for _ in range(12):
        side = rng.choice([-1, 1])
        x = rng.uniform(3.6, 10.8)
        y = 4.2 + side * rng.uniform(1.0, 2.3) * (0.55 + 0.45 * (x - 3.6) / 7.2)
        L = rng.uniform(0.14, 0.42) * (1.2 - 0.5 * (x - 3.6) / 7.2)
        specs.append((x, y, L, L * rng.uniform(0.3, 0.45), rng.uniform(-0.15, 0.15) + side * 0.15))
    drops(cv, specs, "SU3", "SU4", seed, a=0.55)
    gloss(cv, e, np.random.default_rng(seed + 900), seed, n=26, min_e=0.18, ang=0.05, size=(0.08, 0.24),
          sheen=(3.0, 4.2, 1.2))
