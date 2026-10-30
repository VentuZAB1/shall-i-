# HubGrime - crack recipes (floor G_Crack_A/B/C, wall W_Crack_A/B/C) + crack helpers. Imported by make_decals.py.
# Round 2 (REVIEW.md): no loose pale shards (chips only where they touch a crack core, as dark one-side-lit flakes),
# 1-2 px angular micro-jag on every core edge (grime_lib.paint_cracks), wedge ray roots + a 1.8-stud crater with a D2
# inner wall (G_Crack_B), a non-ladder G_Crack_C, and W_Crack_C redrawn as a zigzag crack rising from a broken notch.
import math

import numpy as np

from grime_lib import (L_FLOOR, L_WALL, P, Field, MossScene, arclen, chain_path, convex_poly, cov_from_sd,
                       crack_path, crack_widths, grass_sprig, moss_cushion, moss_render, paint_crater, paint_cracks,
                       paint_polys_hole, poly_sdf, rot, smoothstep)

# floor crack half widths (studs): typical 0.10 (0.2 wide), open sections up to 0.22 - bold for the eye-height
# foreshortening; wall: typical 0.055, open 0.13
FW_TYP, FW_OPEN = 0.1, 0.22
WW_TYP, WW_OPEN = 0.055, 0.13


def branch(rng, start, direction, length, hw0, dev=28, seg=(0.22, 0.55), wmin=0.012, root=0.0):
    """A tapering branch. root > 0 makes a WEDGE root: the width starts at (1 - root) * hw0 and opens over 0.25 stud."""
    d = np.asarray(direction, float)
    d /= np.linalg.norm(d)
    end = np.asarray(start, float) + d * length
    pts = crack_path(rng, start, end, seg=seg, dev=dev, micro=0.08, micro_len=0.13)
    sa = arclen(pts)
    s = sa / max(sa[-1], 1e-6)
    hw = wmin + (hw0 - wmin) * (1 - s) ** 1.1
    if root > 0:
        hw = hw * (1 - root * (1 - smoothstep(0.0, 0.25, sa)))
    return {"pts": pts, "hw": np.maximum(hw, wmin)}


def main_crack(rng, ctrl, w_typ, w_open, opens=1, dev=30, seg=(0.35, 0.85), tip=(1.1, 1.1), open_len=(1.2, 2.4)):
    pts = chain_path(rng, ctrl, seg=seg, dev=dev)
    return {"pts": pts, "hw": crack_widths(pts, rng, w_typ, w_open, opens=opens, tip=tip, open_len=open_len)}


def point_at(st, frac):
    s = arclen(st["pts"])
    t = frac * s[-1]
    i = int(np.searchsorted(s, t)) - 1
    i = max(0, min(i, len(s) - 2))
    p = st["pts"][i] + (st["pts"][i + 1] - st["pts"][i]) * ((t - s[i]) / max(s[i + 1] - s[i], 1e-9))
    tan = st["pts"][i + 1] - st["pts"][i]
    tan = tan / max(np.linalg.norm(tan), 1e-9)
    hw = float(np.interp(t, s, st["hw"]))
    return p, tan, hw


def spall(rng, st, frac, side, length, depth):
    """A chip polygon that OVERLAPS the crack core (it starts inside the core, so it always touches it)."""
    p, tan, hw = point_at(st, frac)
    n = np.array([-tan[1], tan[0]]) * side
    c = p + n * (hw * 0.6 + depth * 0.35)
    poly = convex_poly((0, 0), 1.0, 6, rng, irregular=0.2)
    poly = np.stack([poly[:, 0] * length * 0.5, poly[:, 1] * depth * 0.5], 1)
    ang = math.atan2(tan[1], tan[0])
    return np.array([rot(q, ang) for q in poly]) + c


def moss_in_crack(scene, rng, st, fracs, light, R=(0.2, 0.3)):
    for f in fracs:
        p, tan, hw = point_at(st, f)
        moss_cushion(scene, rng, p[0], p[1], rng.uniform(*R), light, r_rng=(0.06, 0.11), squash=(1.0, 0.85),
                     tip_p=0.55, min_r=0.05)


# floor crack half widths and the wall equivalents are above; the cracks themselves:
def g_crack_a(cv, rng, seed):
    L = L_FLOOR
    main = main_crack(rng, [(1.1, 4.2), (4.4, 3.3), (7.3, 3.9), (10.3, 2.9), (12.9, 3.4)], FW_TYP, FW_OPEN, opens=2,
                      dev=34)
    strokes = [main]
    br = []
    for frac, side, ang, ln in ((0.3, -1, 38, 2.4), (0.47, 1, 52, 2.0), (0.63, -1, 30, 2.8), (0.82, 1, 58, 1.5)):
        p, tan, hw = point_at(main, frac)
        b = branch(rng, p, rot(tan, math.radians(ang) * side), ln, max(hw * 0.6, 0.055), dev=34)
        br.append(b)
        strokes.append(b)
    p, tan, hw = point_at(br[2], 0.45)
    strokes.append(branch(rng, p, rot(tan, math.radians(45)), 0.8, max(hw * 0.7, 0.03), dev=34))
    for frac, side in ((0.42, 1), (0.71, -1)):     # round 3: chips dropped (rng draws kept: shapes unchanged)
        spall(rng, main, frac, side, rng.uniform(0.55, 0.8), rng.uniform(0.24, 0.32))
    paint_cracks(cv, strokes, L, {"hl_a": 0.26}, rng, seed)
    sc = MossScene()
    moss_in_crack(sc, rng, main, (0.5, 0.535), L)
    moss_render(cv, sc, L, halo_a=0.2, halo_w=0.08, shadow_a=0.2)
    p, tan, hw = point_at(main, 0.47)
    grass_sprig(cv, rng, p[0], p[1], 4, L, length=(0.32, 0.55), w0=0.03)


def g_crack_b(cv, rng, seed):
    """Impact fracture (round 3: no spider read): an ANGULAR, slightly long crater pit; TWO long, bold, straight-kinked
    rays roughly across each other; the other rays are short THIN hairline stubs at uneven angles (no legs, no knee
    bends); straight concentric ring CHORDS between rays that cross them a little (web fracture) - two bold, one thin."""
    L = L_FLOOR
    c = np.array([4.85, 5.15])
    crater = convex_poly(c, 0.86, 8, rng, irregular=0.32)
    crater = (crater - c) * np.array([1.12, 0.9]) + c
    paint_crater(cv, crater, L, fill=0.84, wall_w=0.24, seed=seed)
    strokes = []
    for a0, a1 in ((0.3, 1.5), (2.4, 3.4), (4.3, 5.4)):        # broken rim cracks
        angs = np.linspace(a0, a1, 5)
        pts = np.stack([c[0] + 0.98 * np.cos(angs), c[1] + 0.86 * np.sin(angs)], 1)
        pts = chain_path(rng, pts, seg=(0.15, 0.3), dev=20)
        n = len(pts)
        strokes.append({"pts": pts, "hw": 0.016 + 0.024 * np.sin(np.linspace(0, np.pi, n)) ** 0.7})

    def rim_r(a):
        return 0.86 * math.hypot(1.12 * math.cos(a), 0.9 * math.sin(a))

    def ray_pt(a, r, off=0.0):
        d = np.array([math.cos(a), math.sin(a)])
        return c + d * r + np.array([-d[1], d[0]]) * off

    def ray(a, ln, hw0, kinks, root=0.7):
        d = np.array([math.cos(a), math.sin(a)])
        nrm = np.array([-d[1], d[0]])
        r0 = rim_r(a)
        p0 = c + d * r0
        ctrl = [p0] + [p0 + d * ln * f + nrm * o for f, o in kinks] + [p0 + d * ln]
        pts = chain_path(rng, ctrl, seg=(0.4, 0.9), dev=6)
        sa = arclen(pts)
        s = sa / max(sa[-1], 1e-6)
        hw = 0.012 + (hw0 - 0.012) * (1 - s) ** 1.05
        hw = hw * (1 - root * (1 - smoothstep(0.0, 0.25, sa)))
        return {"pts": pts, "hw": np.maximum(hw, 0.012)}

    LONG = ((0.42, 3.5, 0.15, ((0.35, 0.16), (0.7, -0.12))), (3.62, 3.05, 0.14, ((0.3, -0.14), (0.64, 0.13))))
    SHORT = ((1.3, 0.75, 0.06), (2.2, 0.45, 0.05), (2.85, 0.6, 0.055), (4.75, 0.85, 0.06), (5.6, 0.5, 0.05))
    for a, ln, hw0, k in LONG:
        strokes.append(ray(a, ln, hw0, k))
    for a, ln, hw0 in SHORT:
        strokes.append(ray(a, ln, hw0, ((0.5, rng.uniform(-0.05, 0.05)),), root=0.4))

    def chord(a0, r0, a1, r1, bold, over=0.14):
        p0, p1 = ray_pt(a0, r0), ray_pt(a1, r1)
        t = (p1 - p0) / np.linalg.norm(p1 - p0)
        p0, p1 = p0 - t * over, p1 + t * over                 # cross the rays slightly: a web, not a leg joint
        pts = chain_path(rng, [p0, p1], seg=(0.25, 0.45), dev=12)
        n = len(pts)
        prof = np.sin(np.linspace(0, np.pi, n)) ** 0.5
        return {"pts": pts, "hw": (0.014 + 0.046 * prof) if bold else (0.011 + 0.02 * prof)}

    # bold ring pieces between the long rays and the next stub; one thin ring piece
    strokes += [chord(0.42, 1.55, 1.3, 1.36, True), chord(3.62, 1.6, 4.75, 1.45, True),
                chord(2.85, 1.3, 3.62, 1.38, False), chord(4.75, 1.28, 5.6, 1.2, False, over=0.08)]
    paint_cracks(cv, strokes, L, {"hl_a": 0.25, "halo_a": 0.14}, rng, seed)
    sc = MossScene()
    moss_cushion(sc, rng, c[0] + 0.3, c[1] + 0.3, 0.3, L, r_rng=(0.06, 0.1), squash=(1.2, 0.8), tip_p=0.5, min_r=0.05)
    moss_render(cv, sc, L, halo_a=0.16, halo_w=0.06, shadow_a=0.2)


def g_crack_c(cv, rng, seed):
    """Split band with chunks, NOT a ladder: the rail gap varies (0.6-1.4), cross cracks run at angles, one chunk is
    missing (hole with moss + grass) and one is visibly tilted (sunken edge + lit raised edge)."""
    L = L_FLOOR
    xs = np.array([2.7, 4.05, 5.6, 6.8, 8.35, 9.5])
    yu = 3.45 - 0.1 * (xs - 6) + np.array([0.0, -0.18, 0.05, -0.1, 0.15, 0.0])
    yl = yu + np.array([0.75, 1.15, 1.25, 0.8, 1.35, 0.7])          # varying gap
    xl = xs + np.array([-0.3, 0.45, -0.5, 0.42, -0.38, 0.2])        # angled cross cracks
    chunks = [np.array([(xs[k], yu[k]), (xs[k + 1], yu[k + 1]), (xl[k + 1], yl[k + 1]), (xl[k], yl[k])])
              for k in range(len(xs) - 1)]
    paint_polys_hole(cv, chunks[2], L)
    X, Y = cv.XX, cv.YY
    d4 = poly_sdf(X, Y, chunks[3])
    cov4 = cov_from_sd(cv, d4) * smoothstep(0.02, 0.2, -d4)          # feathered: no straight pane edge
    ctr = chunks[3].mean(0)
    axis = np.array([0.35, 1.0])
    axis /= np.linalg.norm(axis)
    tt = ((X - ctr[0]) * axis[0] + (Y - ctr[1]) * axis[1]) / 0.55
    mot = 1 + 0.15 * Field(seed + 61, 0.3, 2, extent=(12, 8))(X, Y)
    cv.over(P("W4"), np.clip((0.12 + 0.5 * smoothstep(-0.7, 1.0, tt)) * mot, 0, 0.7) * cov4)   # sinks toward one rail

    def line(pts, w_typ, w_open, opens=1):
        p = chain_path(rng, pts, seg=(0.25, 0.6), dev=24)
        return {"pts": p, "hw": crack_widths(p, rng, w_typ, w_open, opens=opens, tip=(1.0, 1.0), open_len=(0.8, 1.8))}

    up = line([(0.9, 3.95)] + list(zip(xs, yu)) + [(11.2, 3.0)], 0.095, 0.17, opens=2)
    lo = line([(1.9, 4.6)] + list(zip(xl, yl)) + [(10.4, 4.7)], 0.08, 0.15)
    strokes = [up, lo]
    for k in (1, 3, 4):                                            # not every chunk boundary: no even rungs
        p = chain_path(rng, [(xs[k], yu[k]), (xl[k], yl[k])], seg=(0.18, 0.35), dev=26)
        strokes.append({"pts": p, "hw": np.full(len(p), 0.055)})
    p = chain_path(rng, [(xs[2], yu[2]), ((xs[2] + xl[2]) / 2 - 0.1, (yu[2] + yl[2]) / 2)], seg=(0.15, 0.3), dev=26)
    strokes.append({"pts": p, "hw": np.linspace(0.05, 0.014, len(p))})  # a half cross crack
    p, tan, hw = point_at(lo, 0.22)
    strokes.append(branch(rng, p, rot(tan, math.radians(50)), 1.3, max(hw * 0.7, 0.035), dev=32))
    p, tan, hw = point_at(up, 0.82)
    strokes.append(branch(rng, p, rot(tan, math.radians(-42)), 1.5, max(hw * 0.7, 0.035), dev=32))
    spall(rng, up, 0.34, -1, 0.7, 0.28)             # round 3: chip dropped (rng draw kept)
    paint_cracks(cv, strokes, L, {"hl_a": 0.25}, rng, seed)
    sc = MossScene()
    hc = chunks[2].mean(0)
    moss_cushion(sc, rng, hc[0] + 0.12, hc[1] + 0.14, 0.4, L, r_rng=(0.06, 0.11), squash=(1.1, 0.8), tip_p=0.55,
                 min_r=0.05, region=lambda x, y: poly_sdf(np.array([x]), np.array([y]), chunks[2])[0] < 0.05)
    moss_render(cv, sc, L, halo_a=0.14, halo_w=0.06, shadow_a=0.2)
    grass_sprig(cv, rng, hc[0] - 0.3, hc[1] - 0.05, 4, L, length=(0.3, 0.5), w0=0.03, up=(-0.3, -1))


# ------------------------------------------------------------------ wall cracks (texture top = up)
def w_crack_a(cv, rng, seed):
    L = L_WALL
    main = main_crack(rng, [(2.7, 0.7), (2.2, 3.0), (2.9, 5.2), (2.2, 7.4), (2.5, 9.3)], WW_TYP, WW_OPEN, opens=2,
                      dev=34)
    strokes = [main]
    for frac, side, ang, ln in ((0.22, 1, 58, 1.2), (0.48, -1, 70, 1.0), (0.7, 1, 62, 1.4)):
        p, tan, hw = point_at(main, frac)
        strokes.append(branch(rng, p, rot(tan, math.radians(ang) * side), ln, max(hw * 0.6, 0.03), dev=32))
    spall(rng, main, 0.52, 1, 0.7, 0.28)            # round 3: chip dropped (rng draw kept)
    paint_cracks(cv, strokes, L, {"hl_a": 0.24, "hl_w": 0.06, "sh_a": 0.34}, rng, seed)
    sc = MossScene()
    p, tan, hw = point_at(main, 0.8)
    moss_cushion(sc, rng, p[0] + 0.05, p[1] + 0.08, 0.22, L, r_rng=(0.06, 0.1), squash=(1.3, 0.7), min_r=0.05,
                 tip_p=0.5)
    moss_render(cv, sc, L, halo_a=0.16, halo_w=0.06, shadow_a=0.22)


def w_crack_b(cv, rng, seed):
    L = L_WALL
    main = main_crack(rng, [(6.9, 0.9), (5.6, 3.1), (4.3, 4.9), (2.8, 6.9), (1.2, 9.1)], WW_TYP, WW_OPEN, opens=2,
                      dev=32)
    strokes = [main]
    p0, tan0, hw0 = point_at(main, 0.13)
    for ang, ln in ((-38, 1.0), (30, 0.8)):
        strokes.append(branch(rng, p0, rot(-tan0, math.radians(ang)), ln, max(hw0 * 0.55, 0.03), dev=32))
    for frac, side, ang, ln in ((0.55, 1, 50, 1.3), (0.78, -1, 40, 1.0)):
        p, tan, hw = point_at(main, frac)
        strokes.append(branch(rng, p, rot(tan, math.radians(ang) * side), ln, max(hw * 0.6, 0.03), dev=32))
    p, tan, hw = point_at(main, 0.45)
    nrm = np.array([-tan[1], tan[0]])
    if nrm[1] < 0:
        nrm = -nrm
    ang = math.atan2(tan[1], tan[0])
    chip = convex_poly((0, 0), 1.0, 8, rng, irregular=0.18)
    chip = np.array([rot(q, ang) for q in np.stack([chip[:, 0] * 0.55, chip[:, 1] * 0.34], 1)]) + p + nrm * 0.16
    convex_poly((0, 0), 1.0, 7, rng, irregular=0.25)   # round 3: chip + pocket dropped (rng draws kept)
    paint_cracks(cv, strokes, L, {"hl_a": 0.24, "hl_w": 0.06, "sh_a": 0.34}, rng, seed)


def w_crack_c(cv, rng, seed, stain_layer, lobed):
    """Floor-up crack (round 2 redraw): a broken triangular NOTCH at the base (D1/D2 depth), from its apex an angular
    zigzag crack (sharp 25-40 deg kinks) whose width pulses open and closed, short branches leaving SHALLOW or
    DOWNWARD with hairline ends, moss tucked IN the notch and on 1-2 ledges. No trunk taper, no upward fork, no bush.
    Contact line (floor top) at y = 12.0; content runs into the hidden band to 12.32."""
    L = L_WALL
    X, Y = cv.XX, cv.YY
    nz = Field(seed, 0.9, 3, extent=(6, 13))
    # faint rising damp at the foot (irregular, tapers sideways)
    z = 12.0 - Y
    # round 3: a soft ROUNDED fan (half-ellipse, low-frequency wobble only) instead of a peaked outline
    rr = np.sqrt(((X - 3.0) / 2.0) ** 2 + (np.maximum(z, 0) / 1.45) ** 2)       # elliptical fan distance
    rr = rr * (1 + 0.12 * nz(X * 0.9, Y * 0.9))
    mot = 1 + 0.22 * nz(X * 1.3 + 7, Y * 1.3)
    a = 0.42 * (1 - smoothstep(0.15, 1.0, rr)) ** 1.3 * mot
    cv.over(P("W1"), np.clip(a, 0, 0.5))
    # the broken notch (irregular, off-centre)
    notch = np.array([(2.1, 12.36), (3.95, 12.36), (3.75, 11.75), (3.3, 11.2), (2.9, 10.95), (2.55, 11.35)])
    paint_polys_hole(cv, notch, L, rim_light=0.0)          # round 3: no pale tick on the notch rim
    apex = np.array([2.92, 11.02])
    # angular zigzag rising from the apex; width pulses (two open sections), hairline top
    ctrl = [apex, (2.55, 9.9), (3.2, 8.6), (2.6, 7.2), (3.15, 5.7), (2.55, 4.3), (2.95, 2.8), (2.6, 1.6)]
    pts = chain_path(rng, ctrl, seg=(0.35, 0.75), dev=34)
    sa = arclen(pts)
    hw = crack_widths(pts, rng, 0.055, 0.12, opens=2, tip=(0.05, 1.3), open_len=(0.9, 1.6))
    hw = np.maximum(hw, 0.012)
    hw[sa < 0.3] = np.maximum(hw[sa < 0.3], 0.09)               # meets the notch apex without a trunk flare
    main = {"pts": pts, "hw": hw}
    strokes = [main]
    # branches: shallow / downward, hairline ends (texture +y = down)
    for frac, d, ln in ((0.22, (1.0, 0.35), 1.1), (0.45, (-1.0, 0.25), 1.3), (0.66, (1.0, 0.05), 0.9),
                        (0.8, (-1.0, 0.4), 0.7)):
        p, tan, hw_ = point_at(main, frac)
        strokes.append(branch(rng, p, d, ln, max(hw_ * 0.6, 0.03), dev=30))
    spall(rng, main, 0.33, -1, 0.6, 0.26)           # round 3: chip dropped (rng draw kept)
    paint_cracks(cv, strokes, L, {"hl_a": 0.24, "hl_w": 0.06, "sh_a": 0.34}, rng, seed)
    # moss: IN the notch (filling its lower part, spilling a little over the lip) + two small ledges on kinks
    sc = MossScene()
    in_notch = lambda x, y: poly_sdf(np.array([x]), np.array([y]), notch)[0] < 0.08 or y > 12.2
    for (x, y, R) in ((2.75, 12.1, 0.62), (3.4, 12.15, 0.55), (3.05, 11.7, 0.42)):
        moss_cushion(sc, rng, x, y, R, L, r_rng=(0.07, 0.13), squash=(1.25, 0.75), tip_p=0.55, region=in_notch)
    for frac, R in ((0.25, 0.2), (0.52, 0.16)):
        p, tan, hw_ = point_at(main, frac)
        moss_cushion(sc, rng, p[0] + 0.04, p[1] + 0.06, R, L, r_rng=(0.06, 0.1), squash=(1.4, 0.65), tip_p=0.5,
                     min_r=0.055)
    # round 5: the notch + ledge moss takes the FINAL MossBase look (colours only); halo/shadow glazes keep their
    # round-3 colours, so no crack pixel changes
    from grime_lib import MOSS_LOOK_R5
    look = dict(MOSS_LOOK_R5, pal={k: v for k, v in MOSS_LOOK_R5["pal"].items() if k.startswith("M")})
    moss_render(cv, sc, L, halo_a=0.2, halo_w=0.08, shadow_a=0.22, **look)
    # round 3: the grass sprig in the notch read as a pink worm -> removed
