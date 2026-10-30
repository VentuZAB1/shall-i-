# Pharaoh Asparuh (SECRET of the Void egg, quad, sphinx rest) - FIERCE style (2026-10-09, FIERCE_PLAN "the cat king"):
# a Persian cat lying like the Great Sphinx, built from tapered blocks under a Roblox stud skin: cobby cream body,
# chest raised on the elbows, forelegs stretched forward with gold anklets and black claws, round haunches with the
# hind paws tucked, a broad round head with a short muzzle, narrow kohl-lined turquoise slit eyes (vertical pupils)
# under heavy brows, small fangs, a deep cheek-and-chest ruff, the plume tail curled along his right side, and the
# hero costume: a striped lapis / gold NEMES (hood, flared side flaps, lappets, back queue), a gold URAEUS cobra
# with a turquoise gem, and a 3-band USEKH collar (gold / turquoise / gold) with lapis drops. No glow.
# 2-bone legs: he gets up and struts in the walk; lies regally in everything else. Chibi: _tools/chibi_specs/.
import math
from mathutils import Vector, Matrix, Euler

DISPLAY = "Pharaoh Asparuh"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.0

FUR = (228, 208, 174)       # cream (his real coat)
SHADE = (176, 156, 128)     # back saddle, brows, ear backs, tail top
PALE = (250, 247, 240)      # ruff, muzzle, paws, chest
LAPIS = (40, 66, 176)       # nemes stripes (Roblox darkens -> deep lapis)
GOLD = (230, 172, 52)
GOLD_D = (190, 132, 34)
TURQ = (40, 230, 210)       # ACCENT: uraeus gem, usekh middle band, eyes, anklet gems
TURQ_HOT = (200, 255, 248)
KOHL = (24, 20, 30)
NOSE = (178, 110, 120)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
MOUTH = (90, 22, 36)

# 2-bone legs (rest = sphinx): shoulder -> elbow (on the ground) -> wrist (forearm stretched forward) -> paw centre
FRONT = ((0.20, -0.34, 0.42), (0.21, -0.40, 0.10), (0.21, -0.84, 0.075), (0.21, -0.92, 0.05))
# hind: hip -> hock (back of the haunch, on the ground) -> paw (tucked forward beside the belly)
HIND = ((0.27, 0.44, 0.32), (0.31, 0.64, 0.075), (0.31, 0.14, 0.06), (0.31, 0.07, 0.05))
TAILP = [(-0.05, 0.76, 0.20), (-0.33, 1.00, 0.105), (-0.55, 0.64, 0.10), (-0.56, 0.24, 0.10), (-0.52, -0.06, 0.11)]
HEAD_C = (0, -0.47, 0.80)


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


def eye(B, c, s, yaw=18.0, tilt=18.0, sc=1.0):
    """FIERCE_PLAN D, regal cat version: kohl socket with an Egyptian kohl wing at the outer corner, turquoise slit,
    vertical pupil, hot highlight on the outer half."""
    R = Euler((0, math.radians(-s * tilt), math.radians(s * yaw)), "XYZ").to_matrix()
    n = R @ Vector((0, -1, 0))
    c = Vector(c)
    B.add(c, (0.052 * sc, 0.008, 0.026 * sc), KOHL, "Head", R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + n * 0.006, (0.043 * sc, 0.006, 0.0145 * sc), TURQ, "Head", R=R, studs=[], role="detail", bevel=0.003)
    B.add(c + n * 0.011 + R @ Vector((-s * 0.004, 0, 0)), (0.0065 * sc, 0.004, 0.0145 * sc), BLACK, "Head", R=R,
          studs=[], role="detail", bevel=0.002)
    B.add(c + n * 0.011 + R @ Vector((s * 0.022 * sc, 0, 0.003)), (0.012 * sc, 0.004, 0.0055 * sc), TURQ_HOT,
          "Head", R=R, studs=[], role="detail", bevel=0.002)
    # kohl wing: from the outer corner out and slightly up (Eye of Horus line)
    o = c + R @ Vector((s * 0.05 * sc, 0, -0.008 * sc))
    d = R @ Vector((s * 0.94, 0.25, 0.30)).normalized()
    B.bar(o, o + d * 0.06 * sc, n, 0.018 * sc, 0.006, KOHL, "Head", studs=[], top=(1, 0.3), bevel=0.003)
    return R, n


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=73, tier="S", plates=False)
    # ---------------- body (lying): raised chest propped on the elbows, long cobby rear body, round haunches
    chest = B.add((0, -0.22, 0.38), (0.23, 0.22, 0.30), FUR, "Spine", bot=(0.82, 0.78), top=(0.86, 0.92), rnd=0.32)
    B.seg((0, -0.10, 0.37), (0, 0.36, 0.27), 0.215, 0.215, FUR, "Spine", side=(1, 0, 0), top=(0.92, 0.95), rnd=0.38)
    B.add((0, 0.44, 0.235), (0.21, 0.23, 0.215), FUR, "Spine", bot=(0.85, 0.9), top=(0.70, 0.60), rnd=0.42)  # rump
    B.add((0, -0.18, 0.66), (0.17, 0.17, 0.05), FUR, "Spine", top=(0.8, 0.8))                      # shoulder blades
    B.seg((0, -0.12, 0.655), (0, 0.10, 0.575), 0.12, 0.03, FUR, "Spine", side=(1, 0, 0), top=(0.85, 1))  # back line
    B.seg((0, 0.08, 0.578), (0, 0.46, 0.44), 0.115, 0.03, FUR, "Spine", side=(1, 0, 0), top=(0.6, 1))
    plate = seat_plate(B, [chest], (0, -2, 0.30), (0, 1, 0), (0.17, 0.022, 0.20), PALE, "Spine", proud=0.010,
                       bot=(0.7, 1), top=(0.9, 1), rnd=0.3)                                    # pale chest ON the chest
    for s, side in ((1, "L"), (-1, "R")):
        B.add((s * 0.215, 0.48, 0.245), (0.14, 0.24, 0.21), FUR, "Leg_B" + side, rnd=0.50,
              top=(0.60, 0.52), bot=(0.95, 0.85))                                                 # round haunch
        # Persian fluff: 2 flat studded fur locks on the haunch's back-upper edge (laid back 65 deg, 15 deg out)
        for root in (Vector((s * 0.25, 0.63, 0.34)), Vector((s * 0.27, 0.66, 0.22))):
            d = Vector((s * math.sin(math.radians(15)), math.sin(math.radians(65)), math.cos(math.radians(65))))
            d.normalize()
            B.add(root + d * (0.09 - 0.04), (0.024, 0.055, 0.09), FUR, "Leg_B" + side,
                  R=bk.frame_from(root, root + d, (1, 0, 0)), top=(0.5, 0.15), role="limb")
    # ---------------- usekh collar seated on the chest front (U-bands: gold / turquoise / gold)
    cz = 0.47
    for r0, r1, col in ((0.075, 0.11, GOLD), (0.11, 0.145, TURQ), (0.145, 0.18, GOLD)):
        r = (r0 + r1) / 2
        org = [(r * math.sin(math.radians(-64 + 128 * i / 7)), -2, cz - r * math.cos(math.radians(-64 + 128 * i / 7)))
               for i in range(8)]
        surf_strip(B, [chest, plate], org, (0, 1, 0), r1 - r0 + 0.006, 0.010, col, "Spine",
                   proud=0.008 if col == TURQ else 0.012, bevel=0.005)
    # ---------------- front legs: upper arm, forearm lying forward, pale paw, 4 black claws, gold anklet + gem
    for s, side in ((1, "L"), (-1, "R")):
        S, E, W, P = (X(p, s) for p in FRONT)
        B.seg(S + Vector((0, 0, 0.06)), E, 0.088, 0.10, FUR, "Leg_F" + side, ext1=0.05, top=(0.9, 0.85))
        B.seg(E, W, 0.078, 0.068, FUR, "Shin_F" + side, side=(1, 0, 0), ext=0.06, ext1=0.0)
        B.add(P, (0.088, 0.095, 0.05), PALE, "Foot_F" + side, top=(0.85, 0.8), rnd=0.35)
        for gx in (-0.05, -0.017, 0.017, 0.05):
            B.spike((P.x + gx, P.y - 0.085, 0.035), (0, -1, -0.5), 0.045, 0.012, BLACK, "Foot_F" + side)
        an = W + Vector((0, 0.07, 0.0))
        B.add(an, (0.092, 0.03, 0.078), GOLD, "Shin_F" + side, role="limb", rnd=0.2)
        B.add(an + Vector((s * 0.093, 0, 0.0)), (0.008, 0.022, 0.022), TURQ, "Shin_F" + side, rot=(45, 0, 0),
              studs=[], role="detail", bevel=0.004)
    # ---------------- hind legs: lower leg lying forward beside the belly, pale paw, claws
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A, P = (X(p, s) for p in HIND)
        B.seg(K + Vector((0, 0.02, 0.0)), A, 0.07, 0.06, FUR, "Shin_B" + side, side=(1, 0, 0), ext=0.03)
        B.add(P, (0.08, 0.085, 0.048), PALE, "Foot_B" + side, top=(0.85, 0.8), rnd=0.35)
        for gx in (-0.045, -0.015, 0.015, 0.045):
            B.spike((P.x + gx, P.y - 0.078, 0.033), (0, -1, -0.5), 0.04, 0.011, BLACK, "Foot_B" + side)
    # ---------------- fat Persian plume tail curled along his right side, 2 big tufts on Tail2, gold ring
    T = [Vector(p) for p in TAILP]
    for i, (a, b, bone) in enumerate(((0, 1, "Tail1"), (1, 2, "Tail2"), (2, 3, "Tail3"), (3, 4, "Tail3"))):
        B.seg(T[a], T[b], 0.10, 0.09, FUR if i < 3 else PALE, bone, side=(0, 0, 1), ext=0.05, ext1=0.03,
              top=(0.95, 0.95) if i < 3 else (0.85, 0.85), rnd=0.42)
    p = T[1].lerp(T[2], 0.5) + Vector((0, 0, 0.05))                     # one flat fur lock on top of Tail2
    d = ((T[2] - T[1]).normalized() * 0.42 + Vector((0, 0, 0.91))).normalized()
    B.add(p + d * 0.05, (0.024, 0.055, 0.09), FUR, "Tail2", R=bk.frame_from(p, p + d, (T[2] - T[1]).cross(
        Vector((0, 0, 1))).normalized()), top=(0.5, 0.15), role="limb")
    p = T[2].lerp(T[3], 0.35)
    d = (T[3] - T[2]).normalized()
    B.add(p, (0.108, 0.098, 0.022), GOLD, "Tail3", R=bk.frame_from(p, p + d, (0, 0, 1)), role="limb")
    # ---------------- neck under the ruff; the ruff = 5 bold pale locks above the usekh
    B.add((0, -0.34, 0.60), (0.16, 0.13, 0.13), FUR, "Neck", rnd=0.4)
    for i in range(5):
        a = math.radians(-60 + 30 * i)
        d = Vector((math.sin(a) * 0.8, -0.55, -math.cos(a) * 0.9)).normalized()
        root = Vector((0.11 * math.sin(a), -0.44, 0.62 - 0.05 * math.cos(a)))
        B.spike(root, d, 0.18 if 1 <= i <= 3 else 0.15, 0.09, PALE, "Neck", side=(0, -1, 0), top=(0.15, 0.4))
    # ---------------- head (throat pivot): broad round Persian skull, short muzzle, nose, fangs, jaw
    hc = Vector(HEAD_C)
    B.add(hc, (0.165, 0.15, 0.15), FUR, "Head", top=(0.86, 0.88), bot=(0.92, 0.9), rnd=0.34)
    B.add((0, -0.64, 0.725), (0.088, 0.04, 0.055), PALE, "Head", top=(0.9, 0.8), rnd=0.35)          # muzzle
    for s in (1, -1):
        B.add((s * 0.042, -0.655, 0.712), (0.05, 0.035, 0.042), PALE, "Head", rnd=0.4)            # whisker pads
        B.spike((s * 0.036, -0.69, 0.686), (0, -0.1, -1), 0.05, 0.012, TEETH, "Head")              # fang
    B.add((0, -0.682, 0.76), (0.028, 0.016, 0.019), NOSE, "Head", bot=(0.45, 1), role="detail", bevel=0.006)
    B.add((0, -0.684, 0.728), (0.006, 0.006, 0.02), KOHL, "Head", role="detail", bevel=0.002)      # philtrum
    B.add((0, -0.688, 0.684), (0.055, 0.006, 0.006), KOHL, "Head", role="detail", bevel=0.002)     # stern lip
    for s in (1, -1):
        B.add((s * 0.066, -0.686, 0.680), (0.016, 0.006, 0.006), KOHL, "Head", rot=(0, s * 12, 0), role="detail",
              bevel=0.002)
    B.add((0, -0.57, 0.672), (0.05, 0.035, 0.012), MOUTH, "Head", studs=[], role="detail", bevel=0.004)  # (yawn)
    B.add((0, -0.615, 0.66), (0.06, 0.055, 0.022), PALE, "Jaw", top=(0.95, 0.9), rnd=0.3)           # lower jaw
    # cheek fluff (ruff on the cheeks, swept back)
    for s in (1, -1):
        for z, dz, L in ((0.70, -0.4, 0.14), (0.76, -0.1, 0.13)):
            B.spike((s * 0.15, -0.54, z), (s * 0.55, 0.7, dz), L, 0.05, PALE, "Head", top=(0.15, 0.4))
    # narrow kohl-lined regal eyes under heavy brows
    for s in (1, -1):
        B.add((s * 0.098, -0.592, 0.83), (0.052, 0.035, 0.045), FUR, "Head", rot=(0, 0, s * 22), role="detail",
              bevel=0.012)                                                                  # eye corner fill
        eye(B, (s * 0.074, -0.622, 0.832), s, yaw=20, sc=1.0)
        Rb = Euler((0, math.radians(-s * 16), math.radians(s * 20)), "XYZ").to_matrix()
        B.add((s * 0.074, -0.632, 0.872), (0.066, 0.026, 0.022), SHADE, "Head", R=Rb, role="detail", bevel=0.009)
    # ---------------- nemes: striped hood (lapis / gold), gold brow band, flared side flaps, lappets, back queue
    for j, (z0, z1, sx, sy, col) in enumerate(((0.88, 0.93, 0.195, 0.175, GOLD), (0.93, 0.97, 0.19, 0.17, LAPIS),
                                               (0.97, 1.0, 0.172, 0.156, GOLD), (1.0, 1.03, 0.148, 0.136, LAPIS))):
        B.add((0, -0.455 + 0.008 * j, (z0 + z1) / 2), (sx, sy, (z1 - z0) / 2 + 0.004), col, "Head",
              top=(0.93, 0.93), role="limb", rnd=0.12)
    B.add((0, -0.632, 0.90), (0.17, 0.018, 0.028), GOLD, "Head", top=(0.95, 1), role="limb", rnd=0.25)  # brow band
    for s in (1, -1):
        flap = B.add((s * 0.23, -0.37, 0.69), (0.036, 0.155, 0.21), LAPIS, "Head", top=(1, 0.62),
                     rot=(0, s * 12, 0), role="limb", rnd=0.2)                                  # flat nemes flap
        yh = lambda zl: 0.155 * (1 + (0.62 - 1) * (zl / 0.21 + 1) / 2)
        for zc in (-0.14, 0.0, 0.14):                                   # 3 flush gold stripes wrapping the flap
            y0, y1 = yh(zc - 0.035) + 0.006, yh(zc + 0.035) + 0.006
            ym = (y0 + y1) / 2
            B.add(flap.world((0, 0, zc)), (0.042, ym, 0.035), GOLD, "Head", R=flap.R, top=(1, y1 / ym),
                  bot=(1, y0 / ym), role="detail", bevel=0.004)
        for j, col in enumerate((GOLD, LAPIS, GOLD)):                   # lappet draped on the chest (Spine)
            zc = 0.50 - 0.10 * j
            p, n = surf_hit(B, [chest, plate], (s * 0.165, -2, zc), (0, 1, 0))
            B.add(p + n * (0.026 + 0.008), (0.05, 0.026, 0.05), col, "Spine", rot=(14, 0, 0), role="limb",
                  rnd=0.15)                                                       # clears the collar ends
        p, n = surf_hit(B, [chest, plate], (s * 0.165, -2, 0.24), (0, 1, 0))
        B.add(p + n * (0.028 + 0.008), (0.054, 0.028, 0.014), GOLD_D, "Spine", role="limb", rnd=0.2)
    B.seg((0, -0.32, 0.86), (0, -0.20, 0.68), 0.07, 0.04, LAPIS, "Head", side=(1, 0, 0), top=(0.8, 1))   # queue
    B.add((0, -0.208, 0.68), (0.075, 0.045, 0.025), GOLD, "Head", role="limb")
    # uraeus: gold cobra rising from the brow band, hood with a turquoise gem
    B.seg((0, -0.645, 0.90), (0, -0.66, 0.99), 0.026, 0.02, GOLD, "Head", side=(1, 0, 0))
    B.add((0, -0.664, 0.99), (0.05, 0.02, 0.05), GOLD_D, "Head", top=(0.55, 1), bot=(0.75, 1), role="limb",
          rnd=0.2)
    B.add((0, -0.689, 0.99), (0.018, 0.006, 0.024), TURQ, "Head", rot=(0, 45, 0), studs=[], role="detail",
          bevel=0.004)
    B.add((0, -0.668, 1.045), (0.02, 0.03, 0.016), GOLD, "Head", role="detail", bevel=0.006)
    # ears poking out of the nemes: small, shade backs, pale inner, gold cuff
    for s, side in ((1, "L"), (-1, "R")):
        ear = B.add((s * 0.115, -0.44, 1.065), (0.05, 0.026, 0.065), SHADE, "Ear_" + side, rot=(-8, 0, -s * 12),
                    top=(0.15, 0.45))
        B.add(ear.world((0, -0.027, -0.012)), (0.03, 0.005, 0.042), PALE, "Ear_" + side, R=ear.R, top=(0.15, 1),
              studs=[], role="detail", bevel=0.003)
        B.add(ear.world((0, 0, -0.058)), (0.055, 0.03, 0.014), GOLD, "Ear_" + side, R=ear.R, role="detail",
              bevel=0.006)
    # blink lids (own bones): fur plates hidden inside the head at rest, they slide forward over the eyes
    for s, side in ((1, "L"), (-1, "R")):
        R = Euler((0, math.radians(-s * 18), math.radians(s * 20)), "XYZ").to_matrix()
        c = Vector((s * 0.074, -0.622, 0.832)) - R @ Vector((0, -1, 0)) * 0.055
        B.add(c, (0.056, 0.006, 0.03), FUR, "Lid_" + side, R=R, studs=[], role="detail", bevel=0.003)
        B.add(c + R @ Vector((0, -0.003, -0.026)), (0.056, 0.006, 0.006), KOHL, "Lid_" + side, R=R, studs=[],
              role="detail", bevel=0.002)
    B.build()
    mn, mx = k.bounds()
    pitch = 0.2243 * (mx.z - mn.z) / HEIGHT
    bk.stud_skin(k, pitch)
    return {"TH": round(B.th, 3), "pitch": round(pitch, 4), "H": round(mx.z - mn.z, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.16, 0.36), "Root", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.30, 0.58), "Spine", tail=(0, -0.1, 0.25))
    k.joint("Head", (0, -0.37, 0.68), "Neck", tail=(0, -0.35, 0.1))          # throat pivot
    k.joint("Jaw", (0, -0.57, 0.665), "Head", tail=(0, -0.15, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.115, -0.44, 1.015), "Head", tail=(0, 0, 0.15))
        k.joint("Lid_" + side, (s * 0.074, -0.57, 0.832), "Head", tail=(0, -0.1, 0))
        S, E, W, P = (X(p, s) for p in FRONT)
        k.joint("Leg_F" + side, S, "Spine")
        k.joint("Shin_F" + side, E, "Leg_F" + side)
        k.joint("Foot_F" + side, W, "Shin_F" + side, tail=(0, -0.2, 0))
        k.add_leg2("Leg_F" + side, "Shin_F" + side, "Foot_F" + side, knee=(0, 1, 0))
        H, K, A, P = (X(p, s) for p in HIND)
        k.joint("Leg_B" + side, H, "Spine")
        k.joint("Shin_B" + side, K, "Leg_B" + side)
        k.joint("Foot_B" + side, A, "Shin_B" + side, tail=(0, -0.2, 0))
        k.add_leg2("Leg_B" + side, "Shin_B" + side, "Foot_B" + side, knee=(0, 1, 0))
    k.joint("Tail1", TAILP[0], "Spine", tail=Vector(TAILP[1]) - Vector(TAILP[0]))
    k.joint("Tail2", TAILP[1], "Tail1", tail=Vector(TAILP[2]) - Vector(TAILP[1]))
    k.joint("Tail3", TAILP[2], "Tail2", tail=Vector(TAILP[3]) - Vector(TAILP[2]))


LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]


def check_pairs():
    L = ["Leg_FL", "Shin_FL", "Foot_FL", "Leg_FR", "Shin_FR", "Foot_FR"]
    P = [("Shin_FL", "Shin_FR"), ("Foot_FL", "Foot_FR"), ("Shin_FL", "Foot_FR"), ("Foot_FL", "Shin_FR"),
         ("Leg_BL", "Shin_FL"), ("Leg_BR", "Shin_FR"), ("Shin_BL", "Shin_FL"), ("Shin_BR", "Shin_FR"),
         ("Foot_BL", "Foot_FL"), ("Foot_BR", "Foot_FR"), ("Foot_BL", "Shin_FL"), ("Foot_BR", "Shin_FR"),
         ("Shin_BL", "Shin_BR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in L:
            P.append((a, b))
    for t in ("Tail1", "Tail2", "Tail3"):
        for b in ("Leg_BR", "Shin_BR", "Foot_BR", "Leg_BL", "Shin_BL", "Foot_BL", "Shin_FR", "Foot_FR"):
            P.append((t, b))
    P += [("Ear_L", "Ear_R"), ("Jaw", "Spine"), ("Jaw", "Neck"), ("Head", "Spine")]
    return P


def joints():
    out = [((0, -0.32, 0.60), (0, -0.40, 0.70), 0.30, "Head"), (TAILP[0], TAILP[0], 0.18, "Tail1")]
    for s, side in ((1, "L"), (-1, "R")):
        S, E, W, P = (X(p, s) for p in FRONT)
        H, K, A, P2 = (X(p, s) for p in HIND)
        out += [(E, E, 0.14, "Shin_F" + side), (W, W, 0.14, "Foot_F" + side), (K, K, 0.12, "Shin_B" + side),
                (A, A, 0.12, "Foot_B" + side)]
    return out


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm
from mathutils import Quaternion

LID_N = {s: Vector((s * math.sin(math.radians(20)), -math.cos(math.radians(20)), 0.0)) for s in (1, -1)}


def key_q(k, bone, f, q):
    pb = k.arm.pose.bones[bone]
    R0 = k.arm.data.bones[bone].matrix_local.to_quaternion()
    pb.rotation_quaternion = R0.inverted() @ q @ R0
    pb.keyframe_insert("rotation_quaternion", frame=f, group=bone)


def lids(k, f, amt):
    """0 = open (lid plates hidden in the head), 0.5 = heavy half lid (upper half of the eye), 1 = shut"""
    for s, side in ((1, "L"), (-1, "R")):
        out = 0.0 if amt <= 0 else 0.061
        up = 0.0 if amt <= 0 else 0.018 * (1 - amt) / 0.5 if amt < 1 else 0.0
        v = LID_N[s] * out + Vector((0, 0, min(up, 0.018)))
        k.key("Lid_" + side, f, rot=(0, 0, 0), loc=tuple(v))


def ears(k, f, l=0.0, r=None, back=0.0, splay=0.0):
    r = l if r is None else r
    k.key("Ear_L", f, rot=(back, 0, l + splay))
    k.key("Ear_R", f, rot=(back, 0, -r - splay))


def tail_rest(k, f, flick=0.0, curl=0.0):
    """lying tail: stays on the ground along his right side, only the tip flicks (yaw) or curls up (curl)"""
    k.key("Tail1", f, rot=(0, 0, 0))
    k.key("Tail2", f, rot=(0, 0, 0))
    k.key("Tail3", f, rot=(-curl, flick, 0))


def tail_up(k, f, sway=0.0, curl=0.0):
    """walking tail: Tail1 swung back and up behind the rump, Tail2 up, Tail3 curling forward at the tip"""
    T = [Vector(p) for p in TAILP]
    dr = [(T[1] - T[0]).normalized(), (T[2] - T[1]).normalized(), (T[4] - T[2]).normalized()]
    sw = math.radians(sway)
    dt = [Vector((0.10 + 0.3 * math.sin(sw), 0.80, 0.60)).normalized(),        # a Persian carries the plume
          Vector((0.6 * math.sin(sw), 0.64, 0.77)).normalized(),               # low: a rising S behind him
          Vector((0.8 * math.sin(sw), 0.90, 0.42 + 0.15 * curl)).normalized()]
    qw = [dr[i].rotation_difference(dt[i]) for i in range(3)]
    key_q(k, "Tail1", f, qw[0])
    key_q(k, "Tail2", f, qw[0].inverted() @ qw[1])
    key_q(k, "Tail3", f, qw[1].inverted() @ qw[2])


def idle(k):
    """ROYAL GAZE: chin up, he looks down his nose to one side, then the other; the ears twitch independently;
    the tail tip flicks lazily on the ground."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        b = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(-0.6 * b, 0, 0), loc=(0, 0, 0.006 * (1 + b) / 2))
        k.key("Jaw", f, rot=(0, 0, 0))
        tail_rest(k, f, flick=-3 - 3 * pk.wave(f, n, 0.1, 3))
        lids(k, f, 0)
    for f, nk, hd, yaw, roll in ((0, 0, 0, 0, 0), (10, -3, -6, 0, 0), (24, -3, -2, 13, 2), (48, -3, -2, 13, 2),
                                 (60, -3, -6, 0, 0), (72, -3, -2, -13, -2), (96, -3, -2, -13, -2),
                                 (108, -3, -6, 0, 0), (120, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, yaw * 0.35, 0))
        k.key("Head", f, rot=(hd, yaw * 0.65, roll))
    for f, l, r in ((0, 0, 0), (30, 0, 0), (32, -18, 0), (35, 4, 0), (38, 0, 0), (78, 0, 0), (80, 0, -20),
                    (83, 0, 5), (86, 0, -14), (89, 0, 0), (120, 0, 0)):
        ears(k, f, l, r)
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = LEGS4


RAISE = 0.31          # he gets up for the walk: the sphinx pose unfolds into a standing strut
STAND_DY = {"F": -0.04, "B": 0.0}


def walk(k):
    """dainty proud strut: up on his legs, lateral-sequence cat walk, head held level and high, tail up in a curl."""
    import bpy
    n = 28
    SH, LIFT, duty = 0.13, 0.09, 0.62
    legs = [("Leg_BL", 0.0), ("Leg_FL", 0.25), ("Leg_BR", 0.5), ("Leg_FR", 0.75)]
    k.new_action("walk", n, True)
    for f in range(0, n + 1, 2):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.0 * pk.wave(f, n, 0.1, 2), 2.0 * pk.wave(f, n, 0.1), 2.5 * pk.wave(f, n)),
              loc=(0, 0, RAISE + 0.022 * b))
        k.key("Neck", f, rot=(-1.0 * pk.wave(f, n, 0.15, 2), -2.0 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(-3 + 1.5 * pk.wave(f, n, 0.2, 2), -1.5 * pk.wave(f, n, 0.1), -2.0 * pk.wave(f, n)))
        k.key("Jaw", f, rot=(0, 0, 0))
        tail_up(k, f, sway=5 * pk.wave(f, n, 0.2), curl=0.5 + 0.5 * pk.wave(f, n, 0.3, 2))
        lids(k, f, 0)
        ears(k, f, 0, 0)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg, off in legs:
            g = pk.gait_target(k, leg, f, n, off, SH, LIFT, duty)
            hip = k.J[leg]
            ank = k.J[k.legs2[leg]["foot"]]
            ty = 2 * hip.y - ank.y + (g.y - hip.y) + STAND_DY[leg[4]]
            k.solve_leg(leg, f, Vector((hip.x, ty, g.z)))
    k.finish()
    k.meta["legs"] = legs
    k.meta["duty"] = duty
    k.meta["walk_cycle"] = n
    return (2 * SH) / duty


def roar(k):
    """YAWN-SNARL: a huge yawn (eyes shut, chin up, jaw wide, every fang showing, ears back) that turns into a
    snarl at its peak (head forward, eyes open and glaring, ears flat), then the jaw closes slowly."""
    n = 60
    k.new_action("roar", n, False)
    P = [(0, 0, 0, 0, 0, 0, 0, 0), (12, 0, -4, -10, 8, 0.5, -8, 0), (22, 0, -9, -24, 34, 1.0, -22, 0),
         (28, 0, -9, -22, 34, 1.0, -24, 0), (33, 0, 2, 4, 24, 0.0, -34, 14), (44, 0, 2, 4, 26, 0.0, -34, 14),
         (54, 0, 1, 2, 3, 0.0, -6, 2), (60, 0, 0, 0, 0, 0.0, 0, 0)]
    for f, sp, nk, hd, jw, lid, eb, spl in P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        lids(k, f, lid)
        ears(k, f, 0, 0, back=eb, splay=spl)
        tail_rest(k, f, flick=0)
    for f in range(34, 44, 2):                               # the snarl trembles in the tail tip (no head shake)
        tail_rest(k, f, flick=-3 - 3 * (1 if (f // 2) % 2 else -1))
    cm.plant(k, n)
    k.finish(loop=False)


def knead(k):
    """SIGNATURE (Pharaoh only) - ROYAL BISCUITS: lids half close, chin lifts, then he KNEADS - the front paws
    alternately lift high and press down L-R-L-R-L-R, claws splaying on each press, shoulders rolling, a tiny purr
    vibration, the tail tip curling up - then gives the viewer a SLOW BLINK and settles."""
    import bpy
    n = 90
    k.new_action("act_knead", n, False)
    for f, nk, hd, lid in ((0, 0, 0, 0), (10, -3, -8, 0.5), (70, -3, -8, 0.5), (73, -3, -8, 1.0), (79, -3, -8, 1.0),
                           (84, -1, -3, 0), (90, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        lids(k, f, lid)
        k.key("Jaw", f, rot=(0, 0, 0))
    for f in range(0, n + 1, 2):
        knead_on = 10 <= f <= 70
        roll = 3 * math.sin(math.pi * (f - 10) / 10) if knead_on else 0.0
        purr = 0.003 * (1 if (f // 2) % 2 else -1) if knead_on else 0.0
        rise = 0.024 * min(1.0, max(0.0, (f - 4) / 6)) * (1 - min(1.0, max(0.0, (f - 70) / 8)))
        k.key("Spine", f, rot=(0, 0, roll), loc=(0, 0, rise + purr))
        curl = 22 * min(1.0, max(0.0, (f - 10) / 12)) * (1 - min(1.0, max(0.0, (f - 72) / 14)))
        tail_rest(k, f, flick=0, curl=curl)
        ears(k, f, 0, 0, back=-4 if knead_on else 0)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in ("Leg_BL", "Leg_BR"):
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
        for leg, ph0 in (("Leg_FL", 0), ("Leg_FR", 10)):
            lift, toe = 0.0, None
            t = f - 10 - ph0
            if 0 <= t < 60 and (t // 10) % 2 == 0 and f <= 70:
                u = (t % 10) / 10.0
                lift = 0.15 * math.sin(math.pi * u)
                toe = 30 * math.sin(math.pi * u) - 10 * max(0.0, math.sin(math.pi * (u - 0.6) / 0.4))
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, lift)), toe=toe if toe is not None else 0.0)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    knead(k)
    return stride


HEAD_XF = []
