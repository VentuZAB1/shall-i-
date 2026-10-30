# Celestial Dragon (Celestial egg, wingquad, flies) - FIERCE style (2026-10-09, FIERCE_PLAN "the moon eater"):
# a midnight-indigo western dragon built from tapered blocks under a Roblox stud skin: deep keeled chest with pale
# scute bands, tucked waist, lizard front legs (elbows out) + digitigrade hind legs with black claws, an S-neck
# (Neck + Neck2), a wedge head with narrow moon-white eyes under heavy brows, fangs, a crown of 4 swept pearl horns
# with white tips, a row of dark back spines, broad membrane wings with moon-white constellation stars, a long tail
# (Tail1-4) ending in a flat CRESCENT-MOON blade, and 5 moon-white star shards floating on the Orbit bone.
# No glow (sparkles / star burst = particle VFX on the Breath / Flame anchors). Chibi version: _tools/chibi_specs/.
import math
from mathutils import Vector, Matrix
import wing3

DISPLAY = "Celestial Dragon"
MOTION = "Fly"
RIG = "wingquad"
HEIGHT = 10.0                # gate 2026-10-09: 7.5 made it 25 % smaller than the other tier-6 pets

BODY = (70, 76, 182)        # midnight indigo (Roblox renders ~0.6x darker)
DARK = (40, 42, 106)        # back, spines, socks, brows
PALE = (160, 166, 218)      # pearl-lavender underside + throat
PALE2 = (126, 132, 196)     # scute band gaps
MEM = (70, 64, 160)         # outer membrane
MEM_IN = (52, 47, 126)      # inner membrane
HORN = (184, 190, 232)      # pearl horns
MOON = (240, 244, 255)      # ACCENT: crescent, horn tips, eyes, constellations, star shards
EYE = (214, 240, 255)
EYE_HOT = (255, 255, 255)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
MOUTH = (70, 16, 40)

# leg joints (left side): hip/shoulder, knee/elbow, ankle/wrist, paw centre
LEGS = {"F": ((0.18, -0.40, 0.80), (0.25, -0.31, 0.45), (0.22, -0.42, 0.11), (0.22, -0.47, 0.045)),
        "B": ((0.19, 0.38, 0.80), (0.21, 0.22, 0.47), (0.21, 0.48, 0.21), (0.21, 0.41, 0.045))}
NECKP = [(0, -0.47, 0.90), (0, -0.83, 1.15), (0, -0.71, 1.47)]           # Neck, Neck2, Head (throat pivot)
HEAD_OFF = (0, 0.035, -0.02)     # the head group was built for a throat at (0, -0.745, 1.49): HEAD_XF moves it
TAILP = [(0, 0.54, 0.90), (0, 1.14, 0.74), (0, 1.74, 0.56), (0, 2.30, 0.46), (0, 2.70, 0.52)]   # 2.0 BL (plan)
CRES = (0.26, 0.21, 0.115)       # crescent outer R, inner r, inner-circle offset
WING = wing3.Wing(S=(0.18, -0.26, 1.03), W=(0.80, -0.08, 1.50), H=(0.82, 0.86, 0.94), BB=(0.14, 0.30, 1.03))
F1, F2 = (1.66, 0.20, 1.72), (1.54, 0.78, 1.26)
ORBIT_C = (0, 0.30, 1.86)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def plane_R(n, deg=0.0):
    """rotation whose local z is n (local x/y in the plane, turned by deg)"""
    n = Vector(n).normalized()
    u = Vector((1, 0, 0)) if abs(n.x) < 0.9 else Vector((0, 1, 0))
    u = (u - n * u.dot(n)).normalized()
    v = n.cross(u)
    return Matrix((u, v, n)).transposed() @ Matrix.Rotation(math.radians(deg), 3, "Z")


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


def fierce_eye(B, c, s, bone="Head", yaw=20.0, tilt=18.0, sc=1.0, brow_c=DARK):
    """FIERCE_PLAN D: black socket (tilted, inner corner down) -> accent slit -> hot highlight on the outer half,
    heavy dark brow above. c = socket centre on the face; yaw turns the eye out to the side."""
    from mathutils import Euler
    R = Euler((0, math.radians(-s * tilt), math.radians(s * yaw)), "XYZ").to_matrix()
    n = R @ Vector((0, -1, 0))
    c = Vector(c)
    B.add(c, (0.052 * sc, 0.008, 0.025 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0135 * sc), EYE, bone, R=R, studs=[], role="detail", bevel=0.003)
    B.add(c + n * 0.011 + R @ Vector((s * 0.014 * sc, 0, 0.001)), (0.019 * sc, 0.004, 0.0068 * sc), EYE_HOT, bone,
          R=R, studs=[], role="detail", bevel=0.002)
    Rb = Euler((0, math.radians(-s * 20), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.042 * sc)) + n * 0.022, (0.068 * sc, 0.03, 0.026 * sc), brow_c, bone, R=Rb,
          role="detail", bevel=0.01)


def spike_row(B, pts, color, top=(0.15, 0.25), w=0.055):
    """back spines laid back: (base, angle-from-vertical toward +y, length, bone)"""
    for base, ang, L, bone, ww in pts:
        d = Vector((0, math.sin(math.radians(ang)), math.cos(math.radians(ang))))
        B.spike(base, d, L, ww or w, color, bone, top=top, side=(1, 0, 0))


def membrane_wing(B, s, side):
    """dark arm + fingers, wrist knuckle + pearl thumb claw, 2-tone membrane (inner darker) with a dark scalloped
    trailing-edge trim, moon-white constellation stars on both faces of the panels."""
    S, W, f3, bb = (X(p, s) for p in (WING.S, WING.W, WING.H, WING.BB))
    f1, f2 = X(F1, s), X(F2, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    B.seg(S, W, 0.055, 0.06, DARK, wb, side=(0, 0, 1), ext=0.10, role="limb")
    B.add(W, (0.072, 0.072, 0.072), DARK, wb, role="limb")
    B.spike(W + Vector((s * 0.02, -0.03, 0.04)), (s * 0.5, -0.5, 0.7), 0.16, 0.032, HORN, wb, top=(0.12, 0.12))
    B.seg(W, f3, 0.036, 0.04, DARK, wb, side=(0, 0, 1), top=(0.45, 0.45), role="limb")
    for f, w in ((f1, 0.044), (f2, 0.04)):
        B.seg(W, f, w, w + 0.004, DARK, tb, side=(0, 0, 1), top=(0.4, 0.4), role="limb")
    e12 = f1.lerp(f2, 0.5).lerp(W, 0.17)
    e23 = f2.lerp(f3, 0.5).lerp(W, 0.17)
    q = f3.lerp(bb, 0.5).lerp(S, 0.14)
    B.poly([S, W, f3, q, bb], 0.03, MEM_IN, wb)
    B.poly([W, f1, e12, f2], 0.03, MEM, tb)
    B.poly([W, f2, e23, f3], 0.03, MEM, tb)
    nrm = (f1 - W).cross(f3 - W).normalized()
    for a, b, bone in ((f1, e12, tb), (e12, f2, tb), (f2, e23, tb), (e23, f3, tb), (f3, q, wb), (q, bb, wb)):
        B.bar(a, b, nrm, 0.045, 0.024, DARK, bone, studs=[], bevel=0.008)
    # constellations (gate: no confetti): outer panel = ONE 4-point star at its centre + 3 diamonds in a line toward
    # f1; rear panel = 2 diamonds; inner panel none. Both faces.
    for sg in (1, -1):
        n1 = (f1 - W).cross(f2 - W).normalized() * sg
        c = (W + f1 + f2) / 3
        u = (f1 - W).normalized()
        v = n1.cross(u).normalized()
        cc = c + n1 * 0.019
        for d in (u, -u, v, -v):
            B.bar(cc, cc + d * 0.065, n1, 0.032, 0.006, MOON, tb, studs=[], top=(1, 0.2), bevel=0.003)
        dl = (f1 - c).normalized()
        for i in range(3):
            p = c + dl * (0.13 + 0.10 * i) + n1 * 0.019
            B.add(p, (0.034, 0.034, 0.006), MOON, tb, R=plane_R(n1, 45), studs=[], bevel=0.003)
        n2 = (f2 - W).cross(f3 - W).normalized() * sg
        for a_, b_, c_ in ((0.42, 0.32, 0.26), (0.30, 0.40, 0.30)):
            p = W * a_ + f2 * b_ + f3 * c_ + n2 * 0.019
            B.add(p, (0.034, 0.034, 0.006), MOON, tb, R=plane_R(n2, 45), studs=[], bevel=0.003)

def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=83, tier=6, plates=False)
    # ---------------- torso: deep keeled ribcage, sloped tuck to a narrow waist, muscular hips (no box belly)
    B.add((0, -0.24, 0.78), (0.23, 0.34, 0.27), BODY, "Chest", bot=(0.66, 0.56), top=(0.90, 0.95), rnd=0.30)
    B.add((0, -0.36, 1.00), (0.185, 0.22, 0.07), DARK, "Chest", top=(0.70, 0.80))                     # withers
    B.seg((0, -0.14, 0.60), (0, 0.26, 0.715), 0.14, 0.085, BODY, "Spine", top=(0.82, 0.75), side=(1, 0, 0))
    B.add((0, 0.10, 0.83), (0.168, 0.22, 0.15), BODY, "Spine", bot=(0.72, 0.70), top=(0.95, 1), rnd=0.30)
    B.add((0, 0.36, 0.82), (0.19, 0.20, 0.18), BODY, "Spine", rot=(-8, 0, 0), top=(0.84, 0.90), bot=(0.85, 0.9))
    B.add((0, 0.06, 0.968), (0.10, 0.30, 0.025), DARK, "Spine")                                    # dark saddle
    # pale scute underside: brisket -> belly strip following the tuck, keel plate on the chest front with bands
    B.add((0, -0.27, 0.515), (0.12, 0.17, 0.025), PALE, "Chest", bot=(0.8, 0.9), studs=[])
    B.seg((0, -0.14, 0.523), (0, 0.24, 0.642), 0.095, 0.022, PALE, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    ribs = [blk for blk in B.items if blk.bone == "Chest"][:1]
    keel = seat_plate(B, ribs, (0, -2, 0.79), (0, 1, 0), (0.15, 0.022, 0.17), PALE, "Chest", proud=0.010,
                      bot=(0.62, 1), top=(0.92, 1), rnd=0.25)                                   # keel ON the chest
    for v in (-0.09, -0.01, 0.07):                                                           # scute band gaps
        B.add(keel.world((0, -0.023, v)), (0.13 * (0.75 + 0.25 * (v + 0.17) / 0.34), 0.004, 0.009), PALE2,
              "Chest", R=keel.R, studs=[], role="detail", bevel=0.003)
    # ---------------- S-neck: lower part leans forward, upper part rises; pale scute throat
    N0, N1, N2 = (Vector(p) for p in NECKP)
    B.seg(N0 + Vector((0, 0.03, -0.04)), N1, 0.135, 0.15, BODY, "Neck", ext=0.05, ext1=0.03)
    B.seg(N1, N2 + Vector((0, 0.0, 0.03)), 0.115, 0.125, BODY, "Neck2", ext=0.05, ext1=0.02)
    for a, b, bone, hw in ((N0 + Vector((0, 0.03, -0.04)), N1, "Neck", 0.10), (N1, N2, "Neck2", 0.085)):
        d = (b - a).normalized()
        fn = Vector((0, d.z, -d.y)) if d.z > 0 else Vector((0, -d.z, d.y))
        if fn.y > 0:
            fn = -fn
        off = 0.15 if bone == "Neck" else 0.125
        B.seg(a + fn * (off - 0.035), b + fn * (off - 0.035), hw, 0.05, PALE, bone, ext=0.02, ext1=0.0)
        for t in (0.3, 0.62, 0.92):                                                   # scute band gaps
            c = a.lerp(b, t) + fn * (off + 0.016)
            B.bar(c - Vector((hw * 0.85, 0, 0)), c + Vector((hw * 0.85, 0, 0)), fn, 0.016, 0.005, PALE2, bone,
                  studs=[], role="detail", bevel=0.002)
    # ---------------- head: skull (throat pivot), wedge snout, crown, jaw, fangs, narrow eyes, cheek blades
    B.add((0, -0.87, 1.64), (0.125, 0.12, 0.10), BODY, "Head", top=(0.80, 0.85))                  # skull
    B.add((0, -0.84, 1.745), (0.09, 0.10, 0.025), DARK, "Head", top=(0.8, 0.8))                   # dark crown
    B.seg((0, -0.95, 1.605), (0, -1.23, 1.56), 0.088, 0.062, BODY, "Head", top=(0.70, 0.74), ext=0.02)  # snout
    B.seg((0, -0.97, 1.663), (0, -1.17, 1.622), 0.032, 0.016, DARK, "Head", top=(0.5, 0.6))       # nose ridge
    for s in (1, -1):                                                                  # nostril slits on top
        B.add((s * 0.034, -1.19, 1.607), (0.012, 0.024, 0.008), BLACK, "Head", rot=(-9, 0, s * 20), role="detail",
              bevel=0.003)
    B.seg((0, -0.97, 1.528), (0, -1.22, 1.518), 0.08, 0.02, PALE, "Head", top=(0.75, 0.9))       # pale upper lip
    for s in (1, -1):
        B.spike((s * 0.050, -1.20, 1.515), (0, 0, -1), 0.07, 0.015, TEETH, "Head")                 # canine
        for y in (-1.13, -1.07, -1.01):
            B.spike((s * 0.062, y, 1.515), (0, 0, -1), 0.034, 0.011, TEETH, "Head")
    B.seg((0, -0.93, 1.485), (0, -1.21, 1.48), 0.068, 0.026, PALE, "Jaw", top=(0.8, 1), ext=0.02)      # lower jaw
    B.add((0, -1.07, 1.512), (0.054, 0.12, 0.008), MOUTH, "Jaw", studs=[], role="detail", bevel=0.004)
    for s in (1, -1):
        B.spike((s * 0.040, -1.19, 1.505), (0, 0, 1), 0.045, 0.012, TEETH, "Jaw")
    for s in (1, -1):
        B.add((s * 0.088, -0.952, 1.672), (0.034, 0.03, 0.05), BODY, "Head", rot=(0, 0, s * 26), role="detail",
              bevel=0.01)                                                           # cheek corner under the eye
        fierce_eye(B, (s * 0.074, -0.985, 1.684), s, yaw=24, sc=1.0)
    # cheek blades swept back from the jaw hinge (dark)
    for s in (1, -1):
        for z, dz, L, w in ((1.55, -0.30, 0.14, 0.04), (1.62, 0.0, 0.16, 0.044)):
            B.spike((s * 0.10, -0.86, z), (s * 0.40, 0.92, dz), L, w, DARK, "Head", top=(0.12, 0.4))
    # crown of 4 swept pearl horns with moon-white tips: 2 long upper horns (3 segments) + 2 lower side horns
    for s in (1, -1):
        P = [Vector((s * 0.075, -0.83, 1.73)), Vector((s * 0.11, -0.73, 1.86)), Vector((s * 0.14, -0.58, 1.95)),
             Vector((s * 0.16, -0.40, 1.99))]
        B.seg(P[0], P[1], 0.04, 0.042, HORN, "Head", side=(1, 0, 0), ext=0.06, top=(0.85, 0.85), role="limb")
        B.seg(P[1], P[2], 0.034, 0.036, HORN, "Head", side=(1, 0, 0), ext=0.02, top=(0.8, 0.8), role="limb")
        B.spike(P[2] - (P[3] - P[2]).normalized() * 0.02, P[3] - P[2], (P[3] - P[2]).length + 0.04, 0.03, MOON,
                "Head", top=(0.12, 0.12))
        Q = [Vector((s * 0.115, -0.84, 1.66)), Vector((s * 0.20, -0.72, 1.70)), Vector((s * 0.26, -0.56, 1.73))]
        B.seg(Q[0], Q[1], 0.032, 0.034, HORN, "Head", side=(0, 0, 1), ext=0.05, top=(0.8, 0.8), role="limb")
        B.spike(Q[1] - (Q[2] - Q[1]).normalized() * 0.02, Q[2] - Q[1], (Q[2] - Q[1]).length + 0.03, 0.026, MOON,
                "Head", top=(0.12, 0.12))
    # ---------------- back spines: neck -> withers -> back -> tail, laid back 50-72 deg, shrinking to the tail
    rows = []
    for t, L in ((0.25, 0.10), (0.75, 0.12)):
        p = N1.lerp(N2, 1 - t) + Vector((0, 0.115, 0.0))
        rows.append((p, 40, L, "Neck2", 0.045))
    for t, L in ((0.3, 0.14), (0.75, 0.15)):
        p = (N0 + Vector((0, 0.03, -0.04))).lerp(N1, t) + Vector((0, 0.13, 0.07))
        rows.append((p, 50, L, "Neck", 0.05))
    for y, z, L, ang, bone in ((-0.44, 1.03, 0.17, 58, "Chest"), (-0.26, 1.03, 0.16, 62, "Chest"),
                               (-0.08, 1.0, 0.14, 66, "Spine"), (0.10, 0.98, 0.13, 68, "Spine"),
                               (0.28, 0.98, 0.12, 70, "Spine"), (0.46, 0.96, 0.11, 72, "Spine")):
        rows.append((Vector((0, y, z - 0.04)), ang, L, bone, None))
    spike_row(B, rows, DARK)
    # ---------------- legs: lizard front legs (elbows out), digitigrade hind legs, dark socks, 4 black claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.08)), K, 0.082, 0.105, BODY, leg, ext1=0.03, top=(0.85, 0.72))
                B.seg(K, A, 0.066, 0.072, DARK, shin, top=(0.82, 0.82), ext=0.035, ext1=0.02)
                B.spike(K + Vector((s * 0.04, 0.05, 0.0)), (s * 0.5, 0.85, 0.1), 0.10, 0.03, DARK, shin)  # elbow spur
            else:
                thigh = B.seg(H + Vector((0, 0.03, 0.08)), K, 0.098, 0.15, BODY, leg, bot=(0.85, 1),
                              top=(0.75, 0.62), ext1=0.03)
                # moon crescent on the outer thigh (echoes the tail moon; reads from the side / back at 64 px)
                ax = thigh.R @ Vector((-s, 0, 0))
                org = []
                for th in (-105, -52.5, 0, 52.5, 105):
                    yl, zl = 0.095 * math.cos(math.radians(th)), 0.095 * math.sin(math.radians(th)) + 0.01
                    org.append(thigh.world((s * 0.5, yl, zl)))
                surf_strip(B, [thigh], org, ax, 0.05, 0.008, MOON, leg, proud=0.010, tip0=True, tip1=True)
                B.seg(K, A, 0.066, 0.076, DARK, shin, top=(0.80, 0.80), ext=0.035, ext1=0.02)
                B.seg(A, P + Vector((0, 0.03, 0.03)), 0.054, 0.058, DARK, foot, ext=0.03)
            B.add(P, (0.078, 0.092, 0.045), DARK, foot, top=(0.85, 0.80))
            for gx in (-0.05, -0.017, 0.017, 0.05):
                B.spike((P.x + gx, P.y - 0.08, 0.035), (0, -1, -0.55), 0.07, 0.015, BLACK, foot)
    # ---------------- long tail (4 bones) with a spine row, ending in a flat crescent-moon blade
    T = [Vector(p) for p in TAILP]
    dims = ((0.125, 0.13), (0.095, 0.10), (0.072, 0.075), (0.052, 0.055))
    for i, ((a, b), (w, d)) in enumerate(zip(zip(T, T[1:]), dims)):
        B.seg(a, b, w, d, BODY, "Tail%d" % (i + 1), ext=0.06 if i == 0 else 0.03, ext1=0.02, top=(0.85, 0.85))
        B.seg(a + Vector((0, 0, -d + 0.012)), b + Vector((0, 0, -dims[min(i + 1, 3)][1] * 0.8 + 0.012)), w * 0.72,
              0.014, PALE, "Tail%d" % (i + 1), ext=0.02)
        for t in (0.35, 0.8):
            p = a.lerp(b, t)
            rows2 = [(p + Vector((0, 0, d - 0.02)), 72, 0.10 - 0.02 * i, "Tail%d" % (i + 1), 0.045 - 0.006 * i)]
            spike_row(B, rows2, DARK)
    # crescent (0.35 SH): the convex middle grows out of the tail tip, the two horns sweep back-up and back-down;
    # a flat broad blade seen from the side (strip of quads between the outer and the inner arc, both meet at the tips)
    R, r, off = CRES
    ty = (R * R - r * r + off * off) / (2 * off)
    a_tip = math.degrees(math.acos(-ty / R))
    b_tip = math.degrees(math.acos(-(ty - off) / r))
    C = T[4] + Vector((0, R - 0.035, 0.0))
    N = 10
    outer, inner = [], []
    for j in range(N + 1):
        a = math.radians(-a_tip + 2 * a_tip * j / N)
        b = math.radians(-b_tip + 2 * b_tip * j / N)
        outer.append(C + Vector((0, -R * math.cos(a), R * math.sin(a))))
        inner.append(C + Vector((0, off - r * math.cos(b), r * math.sin(b))))
    for j in range(N):
        q = [outer[j], outer[j + 1], inner[j + 1], inner[j]]
        if j == 0:
            q = [outer[0], outer[1], inner[1]]
        elif j == N - 1:
            q = [outer[j], outer[j + 1], inner[j]]
        B.poly(q, 0.05, MOON, "Tail4")
    B.seg(T[3].lerp(T[4], 0.5), C + Vector((0, -R + 0.03, 0)), 0.045, 0.05, BODY, "Tail4", ext=0.0)
    # ---------------- 5 floating star shards on the Orbit bone
    oc = Vector(ORBIT_C)
    for i in range(5):
        a = math.radians(90 + 72 * i)
        p = oc + Vector((0.40 * math.cos(a), 0.40 * math.sin(a), 0.04 * math.sin(2 * a)))
        B.spike(p, (0, 0, 1), 0.075, 0.032, MOON, "Orbit", side=(math.cos(a), math.sin(a), 0), top=(0.1, 0.1))
        B.spike(p, (0, 0, -1), 0.06, 0.032, MOON, "Orbit", side=(math.cos(a), math.sin(a), 0), top=(0.1, 0.1))
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
    k.joint("Spine", (0, 0.20, 0.80), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.12, 0.80), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", NECKP[0], "Chest", tail=(0, -0.2, 0.28))
    k.joint("Neck2", NECKP[1], "Neck", tail=(0, -0.05, 0.28))
    k.joint("Head", Vector(NECKP[2]) - Vector(HEAD_OFF), "Neck2", tail=(0, -0.35, 0.05))   # throat (HEAD_XF)
    k.joint("Jaw", (0, -0.93, 1.50), "Head", tail=(0, -0.3, 0))
    k.joint("Breath", (0, -1.30, 1.56), "Head", tail=(0, -0.25, 0))    # VFX anchor (no mesh)
    for s, side in ((1, "L"), (-1, "R")):
        for fb, parent, knee in (("F", "Chest", (s * 0.35, 1, 0)), ("B", "Spine", (0, -1, 0))):
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
    k.joint("Flame", crescent_pts()[0], "Tail4", tail=(0, 0, 0.2))     # crescent centre: sparkle VFX anchor
    k.joint("Orbit", ORBIT_C, "Spine", tail=(0, 0, 0.2))


LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3", "Tail4"]


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    P = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
         ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ("Head", "Neck", "Neck2", "Chest", "Spine", "Tail1", "Tail2", "Tail3", "Tail4", "Orbit",
                  "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"):
            P.append((w, b))
    for s in ("L", "R"):
        P += [("Leg_F" + s, "Leg_B" + s), ("Shin_F" + s, "Shin_B" + s), ("Foot_F" + s, "Foot_B" + s)]
    P += [("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Chest", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR", "Leg_FL", "Leg_FR"):
            P.append((a, b))
    P += [("Jaw", "Neck"), ("Head", "Neck"), ("Orbit", "Head"), ("Orbit", "Neck2"), ("Orbit", "Spine"),
          ("Orbit", "Tail1"), ("Orbit", "Tail2"), ("Orbit", "Tail3"), ("Orbit", "Tail4")]
    for t in ("Tail2", "Tail3", "Tail4"):
        for b in ("Head", "Jaw", "Neck", "Neck2", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
            P.append((t, b))
    return P


def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.13, "Wing_" + sd))
    out.append((Vector(NECKP[2]) - Vector(HEAD_OFF), (0, -0.80, 1.58), 0.20, "Head"))
    out.append((NECKP[1], NECKP[1], 0.16, "Neck2"))
    out.append((NECKP[0], NECKP[0], 0.20, "Neck"))
    return out


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm
from mathutils import Quaternion
FOLD = dict(up=20, fwd=-8, twist=0, tip=130)          # ground pose: wrist high, outer wing tucked under (no sail)


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side=side)


def folded(k, f, du=0.0, dfwd=0.0, dtip=0.0, dtw=0.0, side=None):
    wings(k, f, FOLD["up"] + du, FOLD["fwd"] + dfwd, FOLD["twist"] + dtw, FOLD["tip"] + dtip, side)


def anchors(k, f):
    k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
    k.key("Flame", f, rot=(0, 0, 0))


def orbit(k, f, n, turns=1, lift=0.0, bob=0.03):
    """the 5 star shards circle (whole turns per clip so loops close) and bob"""
    cm.key_axis(k, "Orbit", f, (0, 0, 1), 360.0 * turns * f / n, loc=(0, 0, lift + bob * pk.wave(f, n, 0.0, 2)))


def keys_orbit(k, n, turns=1, step=5):
    for f in list(range(0, n + 1, step)) + [n]:
        orbit(k, f, n, turns)


def key_q(k, bone, f, q):
    pb = k.arm.pose.bones[bone]
    R0 = k.arm.data.bones[bone].matrix_local.to_quaternion()
    pb.rotation_quaternion = R0.inverted() @ q @ R0
    pb.keyframe_insert("rotation_quaternion", frame=f, group=bone)


def tail_aim(k, f, dirs):
    """key Tail1-4 so each segment points along the given armature-space direction (Spine level)"""
    T = [Vector(p) for p in TAILP]
    prev = Quaternion()
    for i, d in enumerate(dirs):
        rest = (T[i + 1] - T[i]).normalized()
        qw = rest.rotation_difference(Vector(d).normalized())
        key_q(k, TAIL[i], f, prev.inverted() @ qw)
        prev = qw


def rest_dirs():
    T = [Vector(p) for p in TAILP]
    return [(T[i + 1] - T[i]).normalized() for i in range(4)]


def idle(k):
    """STARGAZE: slow breathing; the head tilts up following the circling star shards, holds the gaze, comes back;
    the tail draws a slow S-curl along the ground; the wings tighten their fold before settling."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        b = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.008 * b))
        k.key("Chest", f, rot=(1.0 + 0.8 * b, 0, 0))
        cm.chain(k, f, n, TAIL, sway=6, pitch=0, cycles=1, lag=0.2, grow=0.55)
        k.key("Jaw", f, rot=(2, 0, 0))
        anchors(k, f)
    for f, n1, n2, hd, yaw in ((0, 0, 0, 0, 0), (10, -2, -3, -6, 4), (40, -6, -10, -26, 14), (55, -6, -10, -28, 0),
                               (70, -6, -10, -26, -14), (90, 0, 0, 0, -4), (120, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(n1, yaw * 0.25, 0))
        k.key("Neck2", f, rot=(n2, yaw * 0.3, 0))
        k.key("Head", f, rot=(hd, yaw * 0.45, 0))
    for f, du, df in ((0, 0, 0), (88, 0, 0), (98, 5, -2), (110, 5, -2), (118, 0, 0), (120, 0, 0)):
        folded(k, f, du=du, dfwd=df)
    keys_orbit(k, n, 1)
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 26

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 1.5 * pk.wave(f, n, 0.1), 1.8 * pk.wave(f, n)),
              loc=(0, 0, 0.02 * b))
        k.key("Chest", f, rot=(0.8, 1.2 * pk.wave(f, n, 0.25), -0.7 * pk.wave(f, n)))
        k.key("Neck", f, rot=(2 + 2 * pk.wave(f, n, 0.15, 2), -2 * pk.wave(f, n, 0.2), 0))
        k.key("Neck2", f, rot=(-1 - 1.5 * pk.wave(f, n, 0.2, 2), -1.5 * pk.wave(f, n, 0.25), 0))
        k.key("Head", f, rot=(-1 - 2 * pk.wave(f, n, 0.25, 2), -2 * pk.wave(f, n, 0.3), 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        folded(k, f, du=2 * pk.wave(f, n, 0.1, 2))
        cm.chain(k, f, n, TAIL, sway=9, pitch=1, cycles=1, lag=0.15, grow=0.5)
        anchors(k, f)
        orbit(k, f, n, 0)
    return cm.quad_walk(k, n, 0.16, 0.09, body, gait="walk")


# ---- flight: slow majestic strokes with a long glide hold
FLY_N = 33
PITCH = 12.0
FLY_LIFT = 0.30          # flight poses ride clear of the floor (ground check)


def stroke_slow(ph):
    """one slow stroke in the first 62 % of the cycle, then a glide with the wings near level, raised again"""
    ph %= 1.0
    if ph < 0.62:
        return wing3.stroke(ph / 0.62, top=34.0, bot=-20.0, down=0.48, sweep=10.0, twist=10.0, fold=26.0)
    e = math.sin(math.pi * (ph - 0.62) / 0.38)
    return dict(up=30 - 24 * e, fwd=-2 + 2 * e, twist=0.0, tip=-5 + e)


def fly_legs(k, f, ph, amt=1.0):
    """front legs tucked like a cat's, hind legs trailing and pumping gently"""
    w = math.sin(2 * math.pi * (ph - 0.25))
    for s in ("L", "R"):
        k.key("Leg_F" + s, f, rot=(-40 * amt, 0, 0), loc=(0, 0, 0))
        k.key("Shin_F" + s, f, rot=((100 + 4 * w) * amt, 0, 0))
        k.key("Foot_F" + s, f, rot=(30 * amt, 0, 0))
        k.key("Leg_B" + s, f, rot=((16 + 6 * w) * amt, 0, 0), loc=(0, 0, 0))
        k.key("Shin_B" + s, f, rot=((10 - 8 * w) * amt, 0, 0))
        k.key("Foot_B" + s, f, rot=((40 + 6 * w) * amt, 0, 0))


def fly_pose(k, f, ph, legs=True):
    w = stroke_slow(ph)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    u = min(ph % 1.0 / 0.62, 1.0)
    k.key("Spine", f, rot=(PITCH - 2.5 * math.sin(2 * math.pi * u), 0, 0),
          loc=(0, 0, FLY_LIFT + 0.06 * math.sin(2 * math.pi * u)))
    k.key("Chest", f, rot=(0, 0, 0))
    k.key("Neck", f, rot=(16 - 2 * math.sin(2 * math.pi * (ph - 0.2)), 0, 0))
    k.key("Neck2", f, rot=(-8, 0, 0))
    k.key("Head", f, rot=(-16 + 2 * math.sin(2 * math.pi * (ph - 0.3)), 0, 0))
    k.key("Jaw", f, rot=(2, 0, 0))
    for i, b in enumerate(TAIL):
        k.key(b, f, rot=(2 + 4 * math.sin(2 * math.pi * (ph - 0.12 * (i + 1))),
                         3 * math.sin(2 * math.pi * (ph - 0.2 * i)), 0))
    anchors(k, f)
    if legs:
        fly_legs(k, f, ph)


def fly(k):
    n = FLY_N
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, f / n)
    keys_orbit(k, n, 0, step=3)
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
    for f, z, p, w in ((6, -0.10, -6, (34, -10, -4, 70)), (10, -0.13, -8, (40, -4, -8, 0)),
                       (13, 0.22, 8, (-36, 10, 10, 4)), (17, 0.36, 12, (18, 0, 0, -6))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Neck", f, rot=(-6 - p * 0.4, 0, 0))
        k.key("Neck2", f, rot=(-4, 0, 0))
        k.key("Head", f, rot=(-6, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(10 - p * 0.6, 0, 0))
        anchors(k, f)
    fly_pose(k, 22, 0.0, legs=False)
    fly_pose(k, n, 0.18, legs=False)
    keys_orbit(k, n, 0, step=3)
    plant_frames(k, range(0, 12))
    for f, a in ((14, 0.45), (19, 0.85)):
        fly_legs(k, f, 0.0, a)
    fly_legs(k, 22, 0.0)
    fly_legs(k, n, 0.18)
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """flare upright with braking beats, legs reach, touch down at 16, absorb, fold the wings"""
    n = 27
    k.new_action("land", n, False)
    fly_pose(k, 0, 0.0)
    for f, z, p, w in ((7, 0.12, -14, (30, 16, -10, -6)), (12, 0.06, -8, (-14, 10, -6, 4)),
                       (16, -0.08, 4, (16, -6, 0, 40)), (21, 0.02, -1, (20, -8, 0, 100))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Neck", f, rot=(-4 - p * 0.4, 0, 0))
        k.key("Neck2", f, rot=(-3, 0, 0))
        k.key("Head", f, rot=(-5, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(6 - p * 0.6, 0, 0))
        anchors(k, f)
    rest_keys(k, n)
    keys_orbit(k, n, 0, step=3)
    for s in ("L", "R"):                                   # legs reach for the ground
        k.key("Leg_F" + s, 7, rot=(-24, 0, 0), loc=(0, 0, 0))
        k.key("Shin_F" + s, 7, rot=(10, 0, 0))
        k.key("Foot_F" + s, 7, rot=(20, 0, 0))
        k.key("Leg_B" + s, 7, rot=(-8, 0, 0), loc=(0, 0, 0))
        k.key("Shin_B" + s, 7, rot=(0, 0, 0))
        k.key("Foot_B" + s, 7, rot=(20, 0, 0))
    plant_frames(k, range(16, n + 1))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(16 / n, 3)}


def roar(k):
    """ROYAL ARCH: the S-neck rises into a high arch and the head bends DOWN at the viewer, jaw wide, horns forward,
    roaring downward; the tail lifts; the wings stay folded; settles."""
    n = 60
    k.new_action("roar", n, False)
    P = [(0, 0, 0, 0, 0, 2, 0.0), (12, 1, -10, -6, 6, 6, 0.3), (20, 1.5, -30, -12, 40, 34, 1.0),
         (46, 1.5, -30, -12, 42, 36, 1.0), (54, 0.5, -8, -3, 8, 6, 0.2), (60, 0, 0, 0, 0, 2, 0.0)]
    for f, ch, n1, n2, hd, jw, t in P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(n1, 0, 0))
        k.key("Neck2", f, rot=(n2, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        folded(k, f, du=5 * t)
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(10 * t * (1 - 0.2 * i), 0, 0))
        anchors(k, f)
    for f in range(22, 46, 3):                          # the roar rumbles in the jaw (no head shake)
        w = 1 if (f // 3) % 2 else -1
        k.key("Jaw", f, rot=(36 + 2 * w, 0, 0))
    for f, z in ((0, 0.0), (10, 0.0), (20, 0.40), (48, 0.40), (58, 0.0), (60, 0.0)):
        cm.key_axis(k, "Orbit", f, (0, 0, 1), 360.0 * f / n, loc=(0, 0.15 * z / 0.4, z))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


ECL_HEAD = [(0, 0, 0, 0, 2, 0), (12, 0, 0, 0, 2, 0), (26, -3, -8, -44, 30, 0.8), (40, -8, -18, -60, 42, 1.0),
            (48, -8, -18, -60, 42, 1.0), (53, -8, -18, -60, 42, 1.0), (54, -8, -18, -60, 26, 1.0),  # one-frame SNAP
            (70, -8, -18, -60, 26, 1.0),
            (74, -8, -18, -60, 40, 1.0), (80, -8, -18, -60, 40, 0.9), (88, -2, -3, -4, 6, 0.3), (100, 0, 0, 0, 2, 0)]
MOUTH_GAP = (0, -1.17, 1.425)          # rest point in the open front of the mouth (HEAD_XF applied)


def crescent_pts():
    """crescent centre, lower horn tip and the unit tangent toward that tip (rest)"""
    R, r, off = CRES
    C = Vector(TAILP[4]) + Vector((0, R - 0.035, 0))
    ty = (R * R - r * r + off * off) / (2 * off)
    a_tip = math.acos(-ty / R)
    tip = C + Vector((0, -R * math.cos(-a_tip), R * math.sin(-a_tip)))
    a2 = -a_tip + math.radians(14)
    back = C + Vector((0, -R * math.cos(a2), R * math.sin(a2)))
    return C, tip, (tip - back).normalized()


def tail_reach(k, f, target, tip_dir, tip_rest=None, tan_rest=None):
    """solve Tail1-4 (yz plane) so the crescent point tip_rest lands on `target` with its tangent along tip_dir;
    the chain arcs up over the back (elbow up). Keys the tail at frame f."""
    T = [Vector(p) for p in TAILP]
    if tip_rest is None:
        _, tip_rest, tan_rest = crescent_pts()
    Ls = [(T[i + 1] - T[i]).length for i in range(4)]
    d4 = Vector(tip_dir).normalized()
    q4 = Vector(tan_rest).normalized().rotation_difference(d4)
    P3 = Vector(target) - q4 @ (Vector(tip_rest) - T[3])           # Tail4 joint (world)
    root = T[0]
    reach = Ls[0] + Ls[1] + Ls[2] - 0.01
    if (P3 - root).length > reach:                                   # out of reach: closest pose on the line
        print("tail_reach clamp f%d %.3f" % (f, (P3 - root).length - reach))
        P3 = root + (P3 - root).normalized() * reach
    best = None
    for a in range(-40, 41, 2):                                       # Tail1 lean (deg from vertical, + = back)
        d1 = Vector((0, math.sin(math.radians(a)), math.cos(math.radians(a))))
        P1 = root + d1 * Ls[0]
        v = P3 - P1
        dist = v.length
        if dist > Ls[1] + Ls[2] - 1e-3 or dist < abs(Ls[1] - Ls[2]) + 1e-3:
            continue
        ca = (Ls[1] ** 2 + dist ** 2 - Ls[2] ** 2) / (2 * Ls[1] * dist)
        ang = math.acos(max(-1, min(1, ca)))
        base = math.atan2(v.z, v.y)
        for sg in (1, -1):
            th = base + sg * ang
            d2 = Vector((0, math.cos(th), math.sin(th)))
            P2 = P1 + d2 * Ls[1]
            d3 = (P3 - P2).normalized()
            d4w = q4 @ (T[4] - T[3]).normalized()
            th_ = [math.atan2(d.z, d.y) for d in (d1, d2, d3, d4w)]
            bends = [(th_[i + 1] - th_[i] + math.pi) % (2 * math.pi) - math.pi for i in range(3)]
            score = 0.25 * min(P1.z, P2.z) - 0.4 * abs(a) / 40 - (max(bends) - min(bends))   # an even arc, no peak
            if best is None or score > best[0]:
                best = (score, [d1, d2, d3, q4 @ (T[4] - T[3]).normalized()])
    if best is None:
        raise RuntimeError("tail_reach: target out of reach %s P3 %s dist %.3f" % (tuple(target), tuple(P3), (P3 - root).length))
    tail_aim(k, f, best[1])
    return best[1]


def eclipse(k):
    """SIGNATURE (CelestialDragon only) - SWALLOW THE MOON: the tail sweeps round along the ground, rises in a high
    arc over the back until the crescent hangs above the head like the moon, the head rises and gazes up at it with
    the wings half open as a frame, the jaws open wide and SNAP shut on the crescent's horn (the eclipse), hold
    it, release; the tail whips back down; settle and fold. The bite is solved: the tail chain is computed so the
    horn tip lands in the posed mouth gap."""
    import bpy
    n = 100
    k.new_action("act_eclipse", n, False)
    RD = rest_dirs()

    def yawed(dirs, degs):
        return [Quaternion((0, 0, 1), math.radians(d)) @ v for v, d in zip(dirs, degs)]
    for f, n1, n2, hd, jw, wo in ECL_HEAD:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        k.key("Chest", f, rot=(-3 * wo, 0, 0))
        k.key("Neck", f, rot=(n1, 0, 0))
        k.key("Neck2", f, rot=(n2, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        wings(k, f, FOLD["up"] + 14 * wo, FOLD["fwd"] + 6 * wo, 0, FOLD["tip"] * (1 - 0.75 * wo))   # half open
        anchors(k, f)
    for f, z in ((0, 0.0), (4, 0.0), (16, 0.90), (90, 0.90), (99, 0.0), (100, 0.0)):    # the stars rise out of
        cm.key_axis(k, "Orbit", f, (0, 0, 1), 360.0 * f / n, loc=(0, 1.0 * z / 0.9, z * 1.45))    # the moon's way
    sc = bpy.context.scene
    arm = k.arm
    UP = Vector((0, 0, 1))

    def mouth(f):
        """posed mouth point + the direction into the mouth (snout axis toward the throat) at frame f"""
        sc.frame_set(f)
        pb = arm.pose.bones["Head"]
        M = arm.matrix_world @ pb.matrix @ arm.data.bones["Head"].matrix_local.inverted()
        return M @ Vector(MOUTH_GAP), (M.to_3x3() @ Vector((0, 1, 0))).normalized()
    G, axis = mouth(54)
    tail_aim(k, 0, RD)
    tail_aim(k, 12, yawed(RD, (-12, -28, -42, -50)))
    tail_aim(k, 17, [(0.0, 0.55, 0.84), (0, 0.2, 0.98), (0, -0.5, 0.86), (0, -0.95, 0.1)])  # curls up
    tail_aim(k, 23, [(0, 0.15, 1.0), (0, -0.25, 0.97), (0, -0.6, 0.8), (0, -0.85, 0.5)])   # high arc over the back
    tail_reach(k, 32, G - axis * 0.07, axis)       # the moon hangs where the jaws will be; the head rises below it
    tail_reach(k, 41, G - axis * 0.07, axis)
    tail_reach(k, 48, G, axis)                     # the horn sinks straight into the wide-open jaws
    tail_reach(k, 54, G, axis)                     # SNAP: the jaws close on the moon (eclipse)
    tail_reach(k, 70, G, axis)
    tail_reach(k, 74, G, axis)
    tail_reach(k, 80, G - axis * 0.07, axis)       # release
    tail_aim(k, 86, yawed(RD, (8, 18, 26, 30)))                           # the tail whips back down and round
    tail_aim(k, 94, RD)
    tail_aim(k, 100, RD)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    eclipse(k)
    return stride


HEAD_XF = [((0, 0, 0), 1.0, ["Head", "Jaw", "Breath"], HEAD_OFF)]
