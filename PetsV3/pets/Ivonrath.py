# Ivonrath (SECRET of the Magma egg, wingquad, flies) - FIERCE style (2026-10-09, FIERCE_PLAN "the crimson wyrm"):
# a crimson croc-dragon built from tapered blocks under a Roblox stud skin: low-slung wide body with copper belly
# scute bands and a keeled chest, sprawled legs (elbows / knees out) with black claws, a short thick neck (Neck +
# Neck2), a long crocodile head with interlocking teeth along both lips, narrow flame-gold reptile eyes under heavy
# brow ridges, 2 back-swept dark horns with flame tips + 2 cheek spikes, a flame-gold crown band between the horns
# (the SECRET hero piece), 2 rows of dark crest blades with flame tips, broad crimson membrane wings and a long tail
# ending in a dark spade. No glow (fire breath / tail flame / embers = particle VFX on the Breath / Flame anchors).
# Chibi version: _tools/chibi_specs/Ivonrath.py
import math
from mathutils import Vector, Matrix
import wing3

DISPLAY = "Ivonrath"
MOTION = "Fly"
RIG = "wingquad"
HEIGHT = 7.5

RED = (198, 42, 40)         # crimson (Roblox renders it ~0.6x darker -> deep crimson)
DARK = (112, 24, 30)        # back, crests, socks, brows, spade
BELLY = (232, 140, 90)      # copper belly scutes
BELLY2 = (190, 104, 66)     # scute gaps
MEM = (146, 32, 38)
MEM_IN = (104, 22, 30)
HORN = (128, 104, 90)       # dark bone horns
FLAME = (255, 184, 32)      # ACCENT: horn tips, crown, crest tips, eyes
FLAME_HOT = (255, 240, 170)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
MOUTH = (80, 14, 26)

LEGS = {"F": ((0.22, -0.46, 0.62), (0.36, -0.37, 0.36), (0.31, -0.50, 0.10), (0.31, -0.56, 0.045)),
        "B": ((0.22, 0.40, 0.62), (0.36, 0.27, 0.38), (0.33, 0.51, 0.13), (0.33, 0.45, 0.045))}
NECKP = [(0, -0.60, 0.70), (0, -0.80, 0.80), (0, -0.93, 0.84)]          # Neck, Neck2, Head (throat pivot)
TAILP = [(0, 0.62, 0.68), (0, 1.08, 0.54), (0, 1.54, 0.42), (0, 1.96, 0.34), (0, 2.30, 0.31)]
WING = wing3.Wing(S=(0.21, -0.34, 0.86), W=(0.80, -0.16, 1.32), H=(0.82, 0.68, 0.74), BB=(0.16, 0.20, 0.84))
F1, F2 = (1.62, 0.08, 1.46), (1.52, 0.62, 1.02)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def surf_hit(B, blks, origin, direction):
    """exact hit point + normal on the bevelled meshes of `blks` (seats inlays ON tapered / rounded faces)"""
    import blockkit as bk
    from mathutils.bvhtree import BVHTree
    B._resolve()
    best = None
    d = Vector(direction).normalized()
    for blk in blks:
        bm = bk._box_bm(blk)
        t = BVHTree.FromBMesh(bm)
        bm.free()
        loc, nrm, _, dist = t.ray_cast(Vector(origin), d)
        if loc is not None and (best is None or dist < best[2]):
            best = (loc, nrm.normalized(), dist)
    if best is None:
        raise RuntimeError("surf_hit: no surface from %s" % (tuple(origin),))
    return best[0], best[1]


def seat_plate(B, blks, origin, direction, half, color, bone, proud=0.010, **kw):
    """plate whose local -y face lies on the surface hit from origin along direction, <= proud above it"""
    p, n = surf_hit(B, blks, origin, direction)
    y = -n
    x = Vector((1, 0, 0)) - n * n.x
    x = x.normalized() if x.length > 1e-4 else Vector((0, 0, 1))
    z = x.cross(y).normalized()
    R = Matrix((x, y, z)).transposed()
    kw.setdefault("studs", [])
    return B.add(p + n * (proud - half[1]), half, color, bone, R=R, **kw)


def surf_strip(B, blks, origins, direction, width, thick, color, bone, proud=0.009, tip0=False, tip1=False, **kw):
    """flush strip of bars along a surface: ray-cast every origin along direction, bars between the hits"""
    hits = [surf_hit(B, blks, o, direction) for o in origins]
    kw.setdefault("studs", [])
    kw.setdefault("bevel", 0.004)
    out = []
    for i in range(len(hits) - 1):
        (a, na), (b, nb) = hits[i], hits[i + 1]
        n = (na + nb).normalized()
        a2, b2 = a + n * (proud - thick), b + n * (proud - thick)
        if tip0 and i == 0:
            out.append(B.bar(b2, a2, n, width, thick, color, bone, top=(1, 0.15), **kw))
        elif tip1 and i == len(hits) - 2:
            out.append(B.bar(a2, b2, n, width, thick, color, bone, top=(1, 0.15), **kw))
        else:
            out.append(B.bar(a2, b2, n, width, thick, color, bone, **kw))
    return out


def fierce_eye(B, c, s, bone="Head", yaw=20.0, tilt=18.0, sc=1.0, brow_c=DARK, pupil=True):
    """FIERCE_PLAN D: black socket (tilted, inner corner down) -> accent slit -> hot highlight on the outer half,
    vertical reptile pupil, heavy dark brow above."""
    from mathutils import Euler
    R = Euler((0, math.radians(-s * tilt), math.radians(s * yaw)), "XYZ").to_matrix()
    n = R @ Vector((0, -1, 0))
    c = Vector(c)
    B.add(c, (0.052 * sc, 0.008, 0.025 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0135 * sc), FLAME, bone, R=R, studs=[], role="detail", bevel=0.003)
    B.add(c + n * 0.011 + R @ Vector((s * 0.022 * sc, 0, 0.002)), (0.014 * sc, 0.004, 0.006 * sc), FLAME_HOT, bone,
          R=R, studs=[], role="detail", bevel=0.002)
    if pupil:
        B.add(c + n * 0.011 + R @ Vector((-s * 0.004, 0, 0)), (0.006 * sc, 0.004, 0.0135 * sc), BLACK, bone, R=R,
              studs=[], role="detail", bevel=0.002)
    Rb = Euler((0, math.radians(-s * 20), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.042 * sc)) + n * 0.022, (0.068 * sc, 0.03, 0.026 * sc), brow_c, bone, R=Rb,
          role="detail", bevel=0.01)


def crest(B, base, ang, L, w, bone, tip=True):
    """ONE tapered crest blade laid back `ang` deg from vertical (toward +y), flat side-view blade: dark 0 -> 0.58 L,
    then a bold flame point 0.58 L -> L that starts at the dark part's top width (no step, no needle)"""
    d = Vector((0, math.sin(math.radians(ang)), math.cos(math.radians(ang))))
    base = Vector(base)
    R = _frame(base, base + d)
    if not tip:
        B.add(base + d * L * 0.5, (w * 0.45, w, L * 0.5), DARK, bone, R=R, top=(0.3, 0.12), role="limb")
        return
    B.add(base + d * L * 0.29, (w * 0.45, w, L * 0.29), DARK, bone, R=R, top=(0.7, 0.6), role="limb")
    B.add(base + d * L * 0.79, (w * 0.45 * 0.7, w * 0.6, L * 0.21), FLAME, bone, R=R, top=(0.12, 0.1),
          role="limb")


def _frame(p0, p1):
    import blockkit as bk
    return bk.frame_from(p0, p1, (1, 0, 0))


def membrane_wing(B, s, side):
    """dark arm + fingers, wrist knuckle + horn thumb claw, 2-tone crimson membrane (inner darker), dark scalloped
    trailing-edge trim."""
    S, W, f3, bb = (X(p, s) for p in (WING.S, WING.W, WING.H, WING.BB))
    f1, f2 = X(F1, s), X(F2, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    B.seg(S, W, 0.058, 0.062, DARK, wb, side=(0, 0, 1), ext=0.10, role="limb")
    B.add(W, (0.075, 0.075, 0.075), DARK, wb, role="limb")
    B.spike(W + Vector((s * 0.02, -0.03, 0.04)), (s * 0.5, -0.5, 0.7), 0.17, 0.034, HORN, wb, top=(0.12, 0.12))
    B.seg(W, f3, 0.038, 0.042, DARK, wb, side=(0, 0, 1), top=(0.45, 0.45), role="limb")
    for f, w in ((f1, 0.046), (f2, 0.042)):
        B.seg(W, f, w, w + 0.004, DARK, tb, side=(0, 0, 1), top=(0.4, 0.4), role="limb")
    e12 = f1.lerp(f2, 0.5).lerp(W, 0.20)
    e23 = f2.lerp(f3, 0.5).lerp(W, 0.20)
    q = f3.lerp(bb, 0.5).lerp(S, 0.14)
    B.poly([S, W, f3, q, bb], 0.03, MEM_IN, wb)
    B.poly([W, f1, e12, f2], 0.03, MEM, tb)
    B.poly([W, f2, e23, f3], 0.03, MEM, tb)
    nrm = (f1 - W).cross(f3 - W).normalized()
    for a, b, bone in ((f1, e12, tb), (e12, f2, tb), (f2, e23, tb), (e23, f3, tb), (f3, q, wb), (q, bb, wb)):
        B.bar(a, b, nrm, 0.045, 0.024, DARK, bone, studs=[], bevel=0.008)
    for f in (f1, f2):                                             # finger-tip claws
        d = (f - W).normalized()
        B.spike(f - d * 0.02, d, 0.10, 0.026, HORN, tb)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=61, tier="S", plates=False)
    # ---------------- torso: wide low croc ribcage tapering underneath, sloped tuck, narrower waist, heavy hips
    B.add((0, -0.28, 0.60), (0.25, 0.36, 0.24), RED, "Chest", bot=(0.70, 0.60), top=(0.88, 0.95), rnd=0.30)
    B.add((0, -0.40, 0.82), (0.20, 0.22, 0.06), DARK, "Chest", top=(0.70, 0.80))                    # shoulders
    B.seg((0, -0.14, 0.42), (0, 0.30, 0.51), 0.17, 0.08, RED, "Spine", top=(0.82, 0.75), side=(1, 0, 0))   # tuck
    B.add((0, 0.14, 0.62), (0.19, 0.22, 0.15), RED, "Spine", bot=(0.74, 0.72), top=(0.95, 1), rnd=0.30)   # waist
    B.add((0, 0.40, 0.62), (0.21, 0.22, 0.17), RED, "Spine", rot=(-6, 0, 0), top=(0.84, 0.90), bot=(0.85, 0.9))
    B.add((0, 0.08, 0.78), (0.13, 0.34, 0.025), DARK, "Spine")                                      # saddle
    # copper belly: brisket + scute strip that follows the tuck, keeled chest plate; transverse scute gaps
    B.add((0, -0.30, 0.375), (0.15, 0.19, 0.025), BELLY, "Chest", bot=(0.8, 0.9), studs=[])
    belly = B.seg((0, -0.14, 0.343), (0, 0.28, 0.443), 0.12, 0.022, BELLY, "Spine", side=(1, 0, 0), top=(0.8, 1),
                  ext=0.03)
    ribs = [blk for blk in B.items if blk.bone == "Chest"][:1]
    keel = seat_plate(B, ribs, (0, -2, 0.60), (0, 1, 0), (0.17, 0.022, 0.15), BELLY, "Chest", proud=0.010,
                      bot=(0.55, 1), top=(0.92, 1), rnd=0.25)                                   # keel ON the chest
    for v in (-0.07, 0.0, 0.07):
        B.add(keel.world((0, -0.023, v)), (0.15 * (0.75 + 0.25 * (v + 0.15) / 0.30), 0.004, 0.009), BELLY2,
              "Chest", R=keel.R, studs=[], role="detail", bevel=0.003)
    # copper flank band along the lower edge, rising with the tuck (z 0.40 at the brisket -> 0.52 at the thigh)
    torso = [blk for blk in B.items if blk.bone in ("Chest", "Spine")][:5]
    for s in (1, -1):
        pts = [(-0.45 + 0.69 * t, 0.435 + 0.12 * t) for t in (0, 0.25, 0.5, 0.75, 1.0)]
        surf_strip(B, torso, [(s * 1.0, y, z) for y, z in pts[:3]], (-s, 0, 0), 0.07, 0.010, BELLY, "Chest",
                   proud=0.009)
        surf_strip(B, torso, [(s * 1.0, y, z) for y, z in pts[2:]], (-s, 0, 0), 0.07, 0.010, BELLY, "Spine",
                   proud=0.009)
        for y, z in pts[1:4]:
            p, n = surf_hit(B, torso, (s * 1.0, y, z), (-s, 0, 0))
            B.bar(p + n * 0.006 - Vector((0, 0, 0.034)), p + n * 0.006 + Vector((0, 0, 0.034)), n, 0.014, 0.006,
                  BELLY2, "Chest", studs=[], role="detail", bevel=0.002)
    for y in (-0.42, -0.30, -0.18):
        B.add((0, y, 0.349), (0.13, 0.009, 0.004), BELLY2, "Chest", studs=[], role="detail", bevel=0.002)
    for t in (0.2, 0.45, 0.7, 0.92):
        B.add(belly.world((0, 0.024, (t - 0.5) * 2 * belly.h.z)), (0.10, 0.004, 0.009), BELLY2, "Spine",
              R=belly.R, studs=[], role="detail", bevel=0.002)
    # ---------------- short thick neck (Neck + Neck2), copper throat
    N0, N1, N2 = (Vector(p) for p in NECKP)
    B.seg(N0 + Vector((0, 0.04, -0.04)), N1, 0.17, 0.15, RED, "Neck", ext=0.06, ext1=0.03)
    B.seg(N1, N2 + Vector((0, -0.02, 0.03)), 0.15, 0.13, RED, "Neck2", ext=0.04, ext1=0.03)
    B.seg((0, -0.62, 0.56), (0, -0.84, 0.70), 0.12, 0.05, BELLY, "Neck", ext=0.02)
    B.seg((0, -0.83, 0.69), (0, -0.98, 0.75), 0.11, 0.045, BELLY, "Neck2", ext=0.02)
    # ---------------- crocodile head: skull, long flat snout, heavy lower jaw, interlocking teeth
    B.add((0, -1.02, 0.905), (0.15, 0.125, 0.095), RED, "Head", top=(0.86, 0.90))                  # skull
    B.add((0, -0.98, 1.01), (0.10, 0.09, 0.02), DARK, "Head", top=(0.8, 0.8))                      # dark crown
    B.seg((0, -1.10, 0.885), (0, -1.50, 0.845), 0.112, 0.052, RED, "Head", top=(0.78, 0.86), ext=0.02)    # snout
    B.add((0, -1.45, 0.905), (0.058, 0.045, 0.026), RED, "Head", top=(0.8, 0.8))                    # nostril bump
    for s in (1, -1):
        B.add((s * 0.026, -1.47, 0.93), (0.012, 0.018, 0.006), BLACK, "Head", rot=(0, 0, s * 18), role="detail",
              bevel=0.003)
    B.seg((0, -1.12, 0.94), (0, -1.40, 0.905), 0.05, 0.018, DARK, "Head", top=(0.6, 0.7))          # snout ridge
    for i, y in enumerate((-1.15, -1.21, -1.27, -1.33, -1.39, -1.45)):                             # upper teeth
        for s in (1, -1):
            L = 0.06 if i in (1, 4) else 0.042
            B.spike((s * 0.092, y, 0.80), (s * 0.15, 0, -1), L, 0.013, TEETH, "Head")
    B.seg((0, -0.98, 0.765), (0, -1.48, 0.775), 0.104, 0.036, RED, "Jaw", top=(0.85, 0.9), ext=0.02)     # lower jaw
    B.seg((0, -1.00, 0.735), (0, -1.44, 0.748), 0.075, 0.015, BELLY, "Jaw", ext=0.0)                # pale chin
    B.add((0, -1.18, 0.805), (0.08, 0.24, 0.006), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    for i, y in enumerate((-1.18, -1.24, -1.30, -1.36, -1.42)):                                    # lower teeth
        for s in (1, -1):
            L = 0.055 if i in (0, 3) else 0.04
            B.spike((s * 0.086, y, 0.795), (s * 0.12, 0, 1), L, 0.012, TEETH, "Jaw")
    B.add((0, -1.04, 0.79), (0.13, 0.08, 0.05), RED, "Jaw", top=(0.95, 0.9))                       # jaw muscle
    for s in (1, -1):
        B.add((s * 0.105, -1.125, 0.962), (0.05, 0.03, 0.042), RED, "Head", rot=(0, 0, s * 26), role="detail",
              bevel=0.01)                                                                     # raised eye socket
        fierce_eye(B, (s * 0.086, -1.158, 0.968), s, yaw=26, sc=1.05)
    # cheek spikes (2 per side, swept back) + 2 back-swept 3-segment horns with flame tips
    for s in (1, -1):
        B.spike((s * 0.15, -0.95, 0.83), (s * 0.55, 0.82, -0.12), 0.15, 0.04, DARK, "Head", top=(0.12, 0.4))
        B.spike((s * 0.14, -0.92, 0.90), (s * 0.50, 0.86, 0.05), 0.13, 0.036, DARK, "Head", top=(0.12, 0.4))
        P = [Vector((s * 0.09, -0.96, 0.99)), Vector((s * 0.14, -0.84, 1.07)), Vector((s * 0.19, -0.69, 1.12)),
             Vector((s * 0.23, -0.52, 1.13))]
        B.seg(P[0], P[1], 0.045, 0.048, HORN, "Head", side=(1, 0, 0), ext=0.06, top=(0.85, 0.85), role="limb")
        B.seg(P[1], P[2], 0.038, 0.04, HORN, "Head", side=(1, 0, 0), ext=0.02, top=(0.8, 0.8), role="limb")
        B.spike(P[2] - (P[3] - P[2]).normalized() * 0.02, P[3] - P[2], (P[3] - P[2]).length + 0.05, 0.034, FLAME,
                "Head", top=(0.12, 0.12))
    # crown band between the horns (hero piece): flame-gold band, 3 points, dark-red gem
    B.add((0, -0.965, 1.04), (0.12, 0.05, 0.028), FLAME, "Head", top=(0.9, 0.9), role="limb", bevel=0.01)
    for x, h in ((-0.09, 0.08), (-0.045, 0.12), (0.0, 0.15), (0.045, 0.12), (0.09, 0.08)):
        B.spike((x, -0.975, 1.06), (0, -0.2, 1), h, 0.026, FLAME, "Head", top=(0.12, 0.12))
    B.add((0, -1.017, 1.04), (0.026, 0.006, 0.02), RED, "Head", rot=(0, 45, 0), studs=[], role="detail",
          bevel=0.004)                                                                       # red gem
    # ---------------- 2 rows of crest blades: neck -> back -> tail, flame tips
    rows = [(-0.84, 0.955, 50, 0.13, "Neck2"), (-0.617, 0.865, 54, 0.15, "Neck"), (-0.393, 0.875, 58, 0.17, "Chest"),
            (-0.17, 0.85, 62, 0.17, "Chest"), (0.053, 0.80, 65, 0.16, "Spine"), (0.277, 0.80, 68, 0.15, "Spine"),
            (0.50, 0.78, 70, 0.13, "Spine")]
    for y, z, ang, L, bone in rows:
        for s in (1, -1):
            crest(B, (s * 0.075, y, z), ang, L * 1.25, 0.064, bone)
    # ---------------- sprawled legs: elbows / knees out, dark socks, 4 black claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.05)), K, 0.09, 0.105, RED, leg, ext1=0.04, top=(0.8, 0.8))
                B.seg(K, A, 0.072, 0.075, DARK, shin, top=(0.85, 0.85), ext=0.04, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.02, 0.05)), K, 0.105, 0.15, RED, leg, ext1=0.04, top=(0.75, 0.7))
                B.seg(K, A, 0.07, 0.075, DARK, shin, top=(0.85, 0.85), ext=0.04, ext1=0.02)
                B.seg(A, P + Vector((0, 0.03, 0.03)), 0.06, 0.06, DARK, foot, ext=0.03)
            B.spike(K + Vector((s * 0.05, 0.03, 0.0)), (s * 0.7, 0.7, 0.0), 0.10, 0.03, DARK,
                    shin if fb == "F" else leg)                                              # elbow / knee spur
            B.add(P, (0.085, 0.10, 0.045), DARK, foot, top=(0.85, 0.80))
            for gx in (-0.055, -0.018, 0.018, 0.055):
                B.spike((P.x + gx, P.y - 0.088, 0.035), (0, -1, -0.55), 0.075, 0.016, BLACK, foot)
    # ---------------- long heavy tail (4 bones), crest pairs, copper underside, dark spade blade
    T = [Vector(p) for p in TAILP]
    dims = ((0.15, 0.14), (0.115, 0.11), (0.085, 0.082), (0.06, 0.058))
    for i, ((a, b), (w, d)) in enumerate(zip(zip(T, T[1:]), dims)):
        bone = "Tail%d" % (i + 1)
        B.seg(a, b, w, d, RED, bone, ext=0.08 if i == 0 else 0.03, ext1=0.02, top=(0.82, 0.82))
        B.seg(a + Vector((0, 0, -d + 0.012)), b + Vector((0, 0, -dims[min(i + 1, 3)][1] * 0.82 + 0.012)), w * 0.7,
              0.014, BELLY, bone, ext=0.02)
        for t in (0.3, 0.75):
            p = a.lerp(b, t)
            if i < 2:
                for s in (1, -1):
                    crest(B, p + Vector((s * w * 0.4, 0, d * 0.85)), 70, 0.16 - 0.025 * i, 0.05 - 0.006 * i, bone)
            else:                                                       # one centre row on Tail3 / Tail4
                crest(B, p + Vector((0, 0, d * 0.85)), 70, 0.13 - 0.025 * (i - 2), 0.044 - 0.006 * (i - 2), bone)
    C = T[4] + Vector((0, 0.17, 0.0))
    spade = [C, T[4] + Vector((0, -0.02, 0)), T[4] + Vector((0, -0.04, 0.12)), C + Vector((0, -0.04, 0.21)),
             C + Vector((0, 0.08, 0.16)), C + Vector((0, 0.26, 0.0)), C + Vector((0, 0.08, -0.16)),
             C + Vector((0, -0.04, -0.21)), T[4] + Vector((0, -0.04, -0.12))]
    B.poly(spade, 0.05, DARK, "Tail4")
    B.poly([C + Vector((0, 0.13, 0)), C + Vector((0, 0.08, 0.16)), C + Vector((0, 0.26, 0.0)),
            C + Vector((0, 0.08, -0.16))], 0.054, FLAME, "Tail4")                               # flame point
    B.seg(T[4] - Vector((0, 0.05, 0)), C + Vector((0, 0.04, 0)), 0.035, 0.035, DARK, "Tail4")
    # ---------------- wings
    for s, side in ((1, "L"), (-1, "R")):
        membrane_wing(B, s, side)
    B.build()
    mn, mx = k.bounds()
    pitch = 0.2243 * (mx.z - mn.z) / HEIGHT
    bk.stud_skin(k, pitch)
    return {"TH": round(B.th, 3), "pitch": round(pitch, 4), "H": round(mx.z - mn.z, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.20, 0.62), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.12, 0.62), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", NECKP[0], "Chest", tail=(0, -0.2, 0.1))
    k.joint("Neck2", NECKP[1], "Neck", tail=(0, -0.13, 0.04))
    k.joint("Head", NECKP[2], "Neck2", tail=(0, -0.35, 0.03))          # throat pivot
    k.joint("Jaw", (0, -1.00, 0.80), "Head", tail=(0, -0.3, 0))
    k.joint("Breath", (0, -1.56, 0.84), "Head", tail=(0, -0.25, 0))    # fire-breath VFX anchor (no mesh)
    for s, side in ((1, "L"), (-1, "R")):
        for fb, parent, knee in (("F", "Chest", (s * 0.8, 1, 0)), ("B", "Spine", (s * 0.8, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
        k.joint("Wing_" + side, X(WING.S, s), "Chest")
        k.joint("WingTip_" + side, X(WING.W, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.1))
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2")
    k.joint("Tail4", TAILP[3], "Tail3")
    k.joint("Flame", (0, 2.50, 0.31), "Tail4", tail=(0, 0, 0.2))       # tail-flame VFX anchor (no mesh)


LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3", "Tail4"]


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    P = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
         ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ("Head", "Neck", "Neck2", "Chest", "Spine", "Tail1", "Tail2", "Tail3", "Tail4",
                  "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"):
            P.append((w, b))
    for s in ("L", "R"):
        P += [("Leg_F" + s, "Leg_B" + s), ("Shin_F" + s, "Shin_B" + s), ("Foot_F" + s, "Foot_B" + s)]
    P += [("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Chest", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR", "Leg_FL", "Leg_FR"):
            P.append((a, b))
    P += [("Jaw", "Neck"), ("Jaw", "Neck2"), ("Head", "Neck")]
    for t in ("Tail2", "Tail3", "Tail4"):
        for b in ("Head", "Jaw", "Neck", "Neck2", "Chest", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR", "Foot_FL",
                  "Foot_FR"):
            P.append((t, b))
    return P


def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.13, "Wing_" + sd))
    out.append((NECKP[2], (0, -0.98, 0.86), 0.20, "Head"))
    out.append((NECKP[1], NECKP[1], 0.18, "Neck2"))
    out.append((NECKP[0], NECKP[0], 0.22, "Neck"))
    return out


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm
FOLD = dict(up=26, fwd=-6, twist=0, tip=120)          # ground pose: wrist high, outer wing tucked under (no sail)


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side=side)


def folded(k, f, du=0.0, dfwd=0.0, dtip=0.0, dtw=0.0, side=None):
    wings(k, f, FOLD["up"] + du, FOLD["fwd"] + dfwd, FOLD["twist"] + dtw, FOLD["tip"] + dtip, side)


def anchors(k, f):
    k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
    k.key("Flame", f, rot=(0, 0, 0))


def tail_keys(k, f, yaws, pitches=(0, 0, 0, 0)):
    for b, y, p in zip(TAIL, yaws, pitches):
        k.key(b, f, rot=(p, y, 0))


def idle(k):
    """CLAW DRUM: impatient - the right forepaw drums its claws on the ground (4 quick taps, twice) while it
    watches it, a slow one-sided sneer (50-70), then the long tail curls round its front feet like a cat's and
    uncurls (80-115)."""
    import bpy
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        b = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.007 * b))
        k.key("Chest", f, rot=(0.6 + 0.6 * b, 0, 0))
        k.key("Neck2", f, rot=(0, 0, 0))
        anchors(k, f)
    for f, nk, hd, yaw, roll in ((0, 0, 0, 0, 0), (8, 3, 8, -14, 0), (48, 3, 8, -14, 0), (54, -2, -4, 4, -4),
                                 (68, -2, -4, 4, -4), (76, 0, 0, 0, 0), (120, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, roll))
    for f, jw, jr in ((0, 2, 0), (50, 2, 0), (56, 9, 6), (66, 9, 6), (72, 2, 0), (120, 2, 0)):
        k.key("Jaw", f, rot=(jw, 0, jr))                                        # one-sided sneer
    for f in list(range(0, 79, 3)) + [116, 120]:
        cm.chain(k, f, n, TAIL, sway=5, pitch=0, cycles=1, lag=0.18, grow=0.5)
    for f in (88, 104):                                                       # tail curls round the front feet
        tail_keys(k, f, (-16, -34, -46, -40), (2, 0, -2, -2))
    for f, du in ((0, 0), (60, 0), (70, 3), (80, 0), (120, 0)):
        folded(k, f, du=du)
    cm.plant(k, n, legs=LEGS4)
    sc = bpy.context.scene
    for start in (8, 28):                                                     # 4 taps, twice
        for f in range(start, start + 17):
            u = ((f - start) % 4) / 4.0
            sc.frame_set(f)
            leg = "Leg_FR"
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)), toe=-16 * math.sin(math.pi * u))
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 24

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 3.0 * pk.wave(f, n, 0.1), 2.0 * pk.wave(f, n)),
              loc=(0, 0, 0.02 * b))
        k.key("Chest", f, rot=(0.6, -2.0 * pk.wave(f, n, 0.25), -1.0 * pk.wave(f, n)))
        k.key("Neck", f, rot=(1 + 1.5 * pk.wave(f, n, 0.15, 2), 2 * pk.wave(f, n, 0.2), 0))
        k.key("Neck2", f, rot=(0, 1.5 * pk.wave(f, n, 0.25), 0))
        k.key("Head", f, rot=(-1, 2 * pk.wave(f, n, 0.3), 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        folded(k, f, du=2 * pk.wave(f, n, 0.1, 2))
        cm.chain(k, f, n, TAIL, sway=11, pitch=1, cycles=1, lag=0.15, grow=0.5)
        anchors(k, f)
    return cm.quad_walk(k, n, 0.14, 0.08, body, gait="trot")


# ---- flight: heavy dragon, fast powerful strokes, strong body bob, hind legs kick on the downstroke
FLY_N = 20
PITCH = 12.0
FLY_LIFT = 0.30


def fly_legs(k, f, ph, amt=1.0):
    kick = max(0.0, math.sin(2 * math.pi * (ph - 0.05)))                   # hind legs kick back on each downstroke
    for s in ("L", "R"):
        k.key("Leg_F" + s, f, rot=(-36 * amt, 0, 0), loc=(0, 0, 0))
        k.key("Shin_F" + s, f, rot=(96 * amt, 0, 0))
        k.key("Foot_F" + s, f, rot=(30 * amt, 0, 0))
        k.key("Leg_B" + s, f, rot=((48 + 14 * kick) * amt, 0, 0), loc=(0, 0, 0))
        k.key("Shin_B" + s, f, rot=((-24 - 10 * kick) * amt, 0, 0))
        k.key("Foot_B" + s, f, rot=((30 + 10 * kick) * amt, 0, 0))


def fly_pose(k, f, ph, legs=True):
    w = wing3.stroke(ph, top=38.0, bot=-8.0, down=0.42, sweep=12.0, twist=12.0, fold=30.0)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    k.key("Spine", f, rot=(PITCH - 3 * math.sin(2 * math.pi * (ph - 0.1)), 0, 0),
          loc=(0, 0, FLY_LIFT + 0.08 * math.cos(2 * math.pi * (ph - 0.45))))
    k.key("Chest", f, rot=(0, 0, 0))
    k.key("Neck", f, rot=(8 - 2 * math.sin(2 * math.pi * (ph - 0.25)), 0, 0))
    k.key("Neck2", f, rot=(-4, 0, 0))
    k.key("Head", f, rot=(-12 + 2 * math.sin(2 * math.pi * (ph - 0.32)), 0, 0))
    k.key("Jaw", f, rot=(2, 0, 0))
    for i, b in enumerate(TAIL):                                              # tail lashes as a counterweight
        k.key(b, f, rot=(3 + 3 * math.sin(2 * math.pi * (ph - 0.12 * (i + 1))),
                         (5 + 3 * i) * math.sin(2 * math.pi * (ph - 0.15 * i)), 0))
    anchors(k, f)
    if legs:
        fly_legs(k, f, ph)


def fly(k):
    n = FLY_N
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, f / n)
    k.finish()


def rest_keys(k, f, z=0.0, pitch=0.0):
    k.key("Spine", f, rot=(pitch, 0, 0), loc=(0, 0, z))
    for b in ("Chest", "Neck", "Neck2", "Head"):
        k.key(b, f, rot=(0, 0, 0))
    k.key("Jaw", f, rot=(2, 0, 0))
    folded(k, f)
    for b in TAIL:
        k.key(b, f, rot=(0, 0, 0))
    anchors(k, f)


def plant_frames(k, frames):
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


def takeoff(k):
    """crouch with the wings unfolding high (0-10), LAUNCH at 11 on a huge downstroke + leg push, into flight"""
    n = 27
    k.new_action("takeoff", n, False)
    rest_keys(k, 0)
    for f, z, p, w in ((6, -0.08, -5, (34, -8, -4, 64)), (10, -0.10, -7, (42, -4, -8, 0)),
                       (13, 0.22, 8, (-30, 12, 10, 4)), (17, 0.36, 12, (20, 0, 0, -6))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Neck", f, rot=(-6 - p * 0.4, 0, 0))
        k.key("Neck2", f, rot=(-3, 0, 0))
        k.key("Head", f, rot=(-6, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(8 - p * 0.6, 0, 0))
        anchors(k, f)
    fly_pose(k, 22, 0.0, legs=False)
    fly_pose(k, n, 0.3, legs=False)
    plant_frames(k, range(0, 13))
    for f, a in ((15, 0.45), (19, 0.85)):
        fly_legs(k, f, 0.0, a)
    fly_legs(k, 22, 0.0)
    fly_legs(k, n, 0.3)
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """flare upright with braking beats, legs reach, touch down at 16, absorb, fold the wings"""
    n = 27
    k.new_action("land", n, False)
    fly_pose(k, 0, 0.0)
    for f, z, p, w in ((7, 0.12, -14, (30, 16, -10, -6)), (12, 0.06, -8, (-12, 10, -6, 4)),
                       (16, -0.06, 4, (18, -6, 0, 40)), (21, 0.02, -1, (24, -6, 0, 96))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Neck", f, rot=(-4 - p * 0.4, 0, 0))
        k.key("Neck2", f, rot=(-2, 0, 0))
        k.key("Head", f, rot=(-5, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(6 - p * 0.6, 0, 0))
        anchors(k, f)
    rest_keys(k, n)
    for s in ("L", "R"):                                   # legs reach for the ground
        k.key("Leg_F" + s, 7, rot=(-20, 0, 0), loc=(0, 0, 0))
        k.key("Shin_F" + s, 7, rot=(10, 0, 0))
        k.key("Foot_F" + s, 7, rot=(20, 0, 0))
        k.key("Leg_B" + s, 7, rot=(-6, 0, 0), loc=(0, 0, 0))
        k.key("Shin_B" + s, 7, rot=(0, 0, 0))
        k.key("Foot_B" + s, 7, rot=(20, 0, 0))
    plant_frames(k, range(16, n + 1))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(16 / n, 3)}


def roar(k):
    """FIRE BREATH: inhales (chest swells, head back, wings half raised), then thrusts the neck forward and blasts
    (fire VFX from the Breath bone), holding ~1 s with ONE slow sweep left to right; the jaw closes; settles."""
    n = 64
    k.new_action("roar", n, False)
    P = [(0, 0, 0, 0, 0, 2, 0.0, 0), (10, -1.5, -10, -6, -20, 6, 1.0, 0), (14, -1.5, -11, -6, -22, 8, 1.0, 0),
         (19, 1.0, 12, 4, 4, 32, 0.4, 14), (48, 1.0, 12, 4, 4, 34, 0.4, -14), (54, 0.5, 2, 0, 0, 4, 0.1, -4),
         (64, 0, 0, 0, 0, 2, 0.0, 0)]
    for f, ch, n1, n2, hd, jw, wu, yaw in P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(n1, yaw * 0.45, 0))
        k.key("Neck2", f, rot=(n2, yaw * 0.25, 0))
        k.key("Head", f, rot=(hd, yaw * 0.3, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        folded(k, f, du=14 * wu, dfwd=-2 * wu)
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(4 * wu, 0, 0))
        anchors(k, f)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def emberdance(k):
    """SIGNATURE (Ivonrath only) - EMBER DANCE (alligator bellow): lowers its belly to the ground, lifts head and
    tail high so the body forms a U, wings spread low and flat, then RUMBLES - the back vibrates and the crest
    blades buzz (ember VFX dance off the back), throat pulsing, jaw shut - then a HEAD-SLAP: the head drops and
    claps its lower jaw against the ground; rises back onto its legs, settles with a tail curl."""
    n = 90
    k.new_action("act_emberdance", n, False)
    P = [(0, 0.0, 0, 0, 0, 0, 2, 0.0), (12, -0.26, -6, 0, 2, 16, 2, 0.3), (24, -0.26, -38, -12, 16, 30, 0, 1.0),
         (58, -0.26, -38, -12, 16, 30, 0, 1.0), (61, -0.26, -32, -10, 10, 24, 22, 0.8),
         (65, -0.26, 21.5, 7, 13, 10, 0, 0.5), (69, -0.26, 18, 5, 11, 8, 0, 0.4), (76, 0.0, 0, 0, 0, 2, 2, 0.0),
         (90, 0.0, 0, 0, 0, 0, 2, 0.0)]
    for f, z, n1, n2, hd, tl, jw, wl in P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Neck", f, rot=(n1, 0, 0))
        k.key("Neck2", f, rot=(n2, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        wings(k, f, FOLD["up"] * (1 - wl) - 10 * wl, FOLD["fwd"] * (1 - wl), 0, FOLD["tip"] * (1 - wl))
        tail_keys(k, f, (0, 0, 0, 0), (tl, tl * 0.4, tl * 0.1, 0))
        anchors(k, f)
    for f in range(27, 58, 3):                                                # RUMBLE: the back vibrates
        w = 1 if (f // 3) % 2 else -1
        k.key("Spine", f, rot=(1.5 * w, 0, 0), loc=(0, 0, -0.26))
        k.key("Chest", f, rot=(-1.5 * w, 0, 0))
        k.key("Neck2", f, rot=(-12 + 1.2 * w, 0, 0))                         # throat pulsing
    for f in (80, 85):                                                        # settle with a tail curl
        tail_keys(k, f, (-6, -12, -14, -10) if f == 80 else (0, 0, 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    emberdance(k)
    return stride


HEAD_XF = []
