# Cvetibara (SECRET of the Celestial egg, wingquad, flies) - FIERCE style (2026-10-09, FIERCE_PLAN "the blossom
# capybara"; "tsvete" = flower): a real capybara turned into a regal armoured celestial beast, built from tapered
# blocks under a Roblox stud skin: a heavy barrel body with the rump set high and a pale underside that follows the
# tuck, short 2-bone legs (4 front toes, 3 hind, black claws), a big square deep head with the eyes / ears / nostrils
# set HIGH, narrow heavy-lidded magenta eyes, big incisors, the dark morillo on the snout, a ridge of coarse dark
# fur, a brass frontlet + chanfron carrying a 5-petal magenta star-lotus (Petal1-5 bones), a floating
# brass halo, and broad umber feather wings with magenta primary tips. No glow (sparkles = particle VFX).
# Chibi version: _tools/chibi_specs/Cvetibara.py
import math
from mathutils import Vector, Matrix, Euler
import wing3

DISPLAY = "Cvetibara"
MOTION = "Fly"
RIG = "wingquad"
HEIGHT = 7.5

FUR = (168, 108, 70)        # capybara brown (Roblox renders it ~0.6x darker)
BACK = (112, 70, 48)        # back, coarse fur ridge, ear backs, brows
UNDER = (214, 160, 114)     # cheeks, underside, inner ears
DARKF = (52, 36, 30)        # feet, nose, morillo
WING_A = (120, 80, 56)      # wing arm, secondaries (umber)
WING_C = (150, 104, 72)     # coverts
WING_P = (104, 68, 48)      # primaries
BRASS = (214, 172, 80)      # halo, frontlet, wing leading edge
BRASS_D = (168, 128, 56)
MAG = (255, 70, 170)        # ACCENT: lotus petals, feather tips, eyes
MAG_HOT = (255, 210, 236)
MAG_D = (214, 40, 132)
INCISOR = (226, 200, 150)
BLACK = (14, 14, 22)
MOUTH = (80, 30, 34)

LEGS = {"F": ((0.20, -0.44, 0.62), (0.215, -0.37, 0.31), (0.215, -0.47, 0.09), (0.215, -0.51, 0.04)),
        "B": ((0.21, 0.44, 0.66), (0.225, 0.29, 0.38), (0.225, 0.56, 0.14), (0.225, 0.49, 0.04))}
WING = wing3.Wing(S=(0.23, -0.40, 0.88), W=(0.80, -0.24, 1.30), H=(0.82, 0.42, 0.86), BB=(0.21, 0.18, 0.90))
TIP = (1.62, 0.02, 1.56)
HEAD_C = (0, -0.98, 0.95)
FLOWER_C = (0, -0.90, 1.155)
HALO_C = (0, -0.86, 1.46)


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


def eye(B, c, s, yaw=30.0, tilt=14.0, sc=1.0):
    """FIERCE_PLAN D, heavy-lidded: black socket (tilted, inner corner down) -> magenta slit -> hot highlight on the
    outer half; the heavy fur lid is a separate brow block above."""
    R = Euler((0, math.radians(-s * tilt), math.radians(s * yaw)), "XYZ").to_matrix()
    n = R @ Vector((0, -1, 0))
    c = Vector(c)
    B.add(c, (0.05 * sc, 0.008, 0.022 * sc), BLACK, "Head", R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + n * 0.006, (0.042 * sc, 0.006, 0.012 * sc), MAG, "Head", R=R, studs=[], role="detail", bevel=0.003)
    B.add(c + n * 0.011 + R @ Vector((s * 0.018 * sc, 0, 0.001)), (0.016 * sc, 0.004, 0.006 * sc), MAG_HOT, "Head",
          R=R, studs=[], role="detail", bevel=0.002)
    Rb = Euler((0, math.radians(-s * 18), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.034 * sc)) + n * 0.018, (0.066 * sc, 0.03, 0.022 * sc), BACK, "Head", R=Rb,
          role="detail", bevel=0.01)                                                            # heavy lid / brow
    return R, n


def feather_wing(B, s, side):
    """umber feather wing: arm + wrist, brass-edged coverts on the arm, secondaries hanging back to the hinge line
    (Wing bone), primaries fanned from the wrist with big magenta tips (WingTip bone, folds about wrist->hinge)."""
    S, W, H, BB = (X(p, s) for p in (WING.S, WING.W, WING.H, WING.BB))
    T = X(TIP, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    n = (W - S).cross(H - W).normalized()
    if n.z < 0:
        n = -n
    FT = 0.022
    B.seg(S, W, 0.05, 0.065, WING_A, wb, side=n, ext=0.10, role="limb")
    B.add(W, (0.07, 0.07, 0.07), WING_A, wb, role="limb")
    B.seg(W, W.lerp(T, 0.28), 0.042, 0.055, WING_A, tb, side=n, top=(0.8, 0.8), role="limb")
    B.seg(S.lerp(W, 0.2), W, 0.05, 0.026, BRASS, wb, side=n, ext1=0.02, studs=[], role="limb")       # brass edge
    NS = 6
    for i in range(NS):                                            # secondaries
        t = (i + 0.5) / NS
        a = S.lerp(W, 0.04 + 0.92 * t)
        e = BB.lerp(H, t)
        d = (e - a).normalized()
        L = (e - a).length + 0.10 * min(1.0, t * 1.4)            # inner feathers stop at the root line
        o = n * (0.006 if i % 2 else -0.006)
        B.bar(a + o, a + d * L + o, n, 0.20, FT, WING_A, wb, top=(1, 0.45))
    NC = 5
    for i in range(NC):                                            # coverts (lighter, on top)
        t = (i + 0.5) / NC
        a = S.lerp(W, 0.03 + 0.92 * t)
        e = BB.lerp(H, t)
        d = (e - a).normalized()
        o = n * (FT + 0.014)
        B.bar(a + o - d * 0.03, a + d * 0.30 + o, n, 0.19, FT, WING_C, wb, top=(1, 0.4))
    NP = 9                                                         # primaries with magenta tips (one band)
    hd, td = (H - W).normalized(), (T - W).normalized()
    for j in range(NP):
        u = j / (NP - 1)
        d = hd.lerp(td, 0.12 + 0.88 * u).normalized()
        L = (T - W).length * (0.60 + 0.40 * u)
        o = -n * (0.012 + 0.006 * (j % 2))
        a = W + d * 0.02 + o
        e = W + d * L + o
        B.bar(a, e, n, 0.22, FT, WING_P, tb, top=(1, 0.5))
        w70 = 0.22 * (1 - 0.5 * 0.68)
        B.bar(a.lerp(e, 0.68), e + d * 0.01, n, w70, FT + 0.004, MAG, tb, studs=[], top=(1, 0.6))


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=53, tier="S", plates=False)
    # ---------------- barrel body: ribcage tapering underneath, sloped tuck, high round rump (capybara back line)
    B.add((0, -0.25, 0.62), (0.27, 0.38, 0.27), FUR, "Spine", bot=(0.74, 0.62), top=(0.88, 0.92), rnd=0.32)
    B.seg((0, -0.10, 0.42), (0, 0.36, 0.50), 0.19, 0.09, FUR, "Spine", top=(0.85, 0.8), side=(1, 0, 0))   # tuck
    B.add((0, 0.40, 0.70), (0.265, 0.30, 0.27), FUR, "Spine", rot=(-10, 0, 0), top=(0.84, 0.78), bot=(0.86, 0.8),
          rnd=0.34)                                                                                # high rump
    B.add((0, 0.66, 0.66), (0.20, 0.08, 0.20), FUR, "Spine", top=(0.8, 0.6), bot=(0.8, 0.7), rnd=0.4)    # rump drop
    B.seg((0, -0.52, 0.89), (0, 0.62, 0.97), 0.15, 0.03, BACK, "Spine", side=(1, 0, 0), top=(0.8, 0.8))  # saddle
    # pale underside: brisket + strip along the tuck, pale chest front
    B.add((0, -0.30, 0.375), (0.16, 0.20, 0.025), UNDER, "Spine", bot=(0.8, 0.9), studs=[])
    B.seg((0, -0.10, 0.333), (0, 0.34, 0.415), 0.13, 0.022, UNDER, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    B.add((0, 0.10, 0.66), (0.25, 0.16, 0.22), FUR, "Spine", bot=(0.8, 0.7), rnd=0.30)          # waist (no hole)
    ribs = [blk for blk in B.items if blk.bone == "Spine"][:1]
    seat_plate(B, ribs, (0, -2, 0.60), (0, 1, 0), (0.18, 0.022, 0.17), UNDER, "Spine", proud=0.010, bot=(0.5, 1),
               top=(0.9, 1), rnd=0.25)                                                   # pale chest ON the chest
    # coarse dark fur ridge along the spine (short spikes laid back)
    for y, z, L, ang in ((-0.50, 0.91, 0.11, 62), (-0.34, 0.92, 0.12, 64), (-0.18, 0.93, 0.12, 66),
                         (-0.02, 0.94, 0.12, 68), (0.14, 0.96, 0.12, 70), (0.30, 0.98, 0.11, 72),
                         (0.46, 0.98, 0.10, 74)):
        d = Vector((0, math.sin(math.radians(ang)), math.cos(math.radians(ang))))
        B.spike((0, y, z - 0.03), d, L, 0.05, BACK, "Spine", top=(0.15, 0.3))
    # ---------------- short thick neck
    B.seg((0, -0.56, 0.70), (0, -0.80, 0.86), 0.19, 0.18, FUR, "Neck", ext=0.06, ext1=0.03)
    B.seg((0, -0.62, 0.58), (0, -0.84, 0.72), 0.14, 0.05, UNDER, "Neck", ext=0.02)
    # ---------------- head: big square deep capybara head, eyes / ears / nostrils high, blunt muzzle
    hc = Vector(HEAD_C)
    B.add(hc, (0.175, 0.20, 0.165), FUR, "Head", top=(0.88, 0.92), rnd=0.28)                      # skull
    B.add((0, -1.25, 0.905), (0.15, 0.115, 0.15), FUR, "Head", top=(0.82, 0.86), bot=(0.9, 0.9), rnd=0.28)  # muzzle
    B.add((0, -0.96, 1.105), (0.13, 0.17, 0.025), BACK, "Head", top=(0.85, 0.85))                  # dark crown
    for s in (1, -1):
        B.add((s * 0.158, -1.04, 0.85), (0.03, 0.12, 0.07), UNDER, "Head", rot=(0, s * 6, 0), top=(0.8, 0.9),
              rnd=0.35)                                                                         # pale jowls
        for z, dz, L, w in ((0.83, -0.45, 0.16, 0.05), (0.89, 0.30, 0.12, 0.044)):
            B.spike((s * 0.165, -0.93, z), (s * 0.40, 0.92, dz), L, w, BACK, "Head", top=(0.12, 0.4))  # cheek ruff
    B.add((0, -1.255, 1.055), (0.06, 0.06, 0.026), DARKF, "Head", top=(0.75, 0.8), rnd=0.35)       # morillo
    B.add((0, -1.352, 1.005), (0.085, 0.024, 0.03), DARKF, "Head", top=(0.9, 1), bot=(0.55, 1), rnd=0.35)  # nose
    muz = [blk for blk in B.items if blk.bone == "Head"][1]
    seat_plate(B, [muz], (0, -2, 0.885), (0, 1, 0), (0.105, 0.022, 0.045), UNDER, "Head", proud=0.008, rnd=0.2)
    for s in (1, -1):                                                         # pale upper-lip band wraps the sides
        seat_plate(B, [muz], (s * 1.0, -1.305, 0.885), (-s, 0, 0), (0.045, 0.022, 0.05), UNDER, "Head",
                   proud=0.008, rnd=0.2)
    B.add((0, -1.366, 0.906), (0.006, 0.006, 0.068), DARKF, "Head", role="detail", bevel=0.002)    # split lip
    for s in (1, -1):                                                         # stern mouth, ends 12 deg down
        B.add((s * 0.0425, -1.364, 0.836), (0.0425, 0.008, 0.008), MOUTH, "Head", rot=(0, s * 12, 0),
              role="detail", bevel=0.003)
        B.add((s * 0.018, -1.358, 0.812), (0.017, 0.008, 0.022), INCISOR, "Head", bot=(0.8, 1), role="detail",
              bevel=0.004)                                                                  # short incisors
    B.add((0, -1.20, 0.745), (0.11, 0.13, 0.04), UNDER, "Jaw", top=(0.95, 0.9), rnd=0.3)           # lower jaw
    for s in (1, -1):                                                                          # high narrow eyes
        B.add((s * 0.155, -1.14, 1.05), (0.042, 0.05, 0.036), FUR, "Head", rot=(0, 0, s * 22), role="detail",
              bevel=0.01)                                                                     # raised eye bump
        eye(B, (s * 0.1755, -1.19, 1.052), s, yaw=22, sc=1.12)
    # blink / heavy lids (own bones): fur plates hidden inside the head, they slide out over the eyes
    for s, side in ((1, "L"), (-1, "R")):
        R = Euler((0, math.radians(-s * 14), math.radians(s * 22)), "XYZ").to_matrix()
        nn = R @ Vector((0, -1, 0))
        c = Vector((s * 0.1755, -1.19, 1.052)) - nn * 0.055
        B.add(c, (0.059, 0.006, 0.028), BACK, "Lid_" + side, R=R, studs=[], role="detail", bevel=0.003)
        B.add(c + R @ Vector((0, -0.003, -0.025)), (0.059, 0.006, 0.006), BLACK, "Lid_" + side, R=R, studs=[],
              role="detail", bevel=0.002)
    # small round ears high on the head
    for s, side in ((1, "L"), (-1, "R")):
        ear = B.add((s * 0.15, -0.83, 1.15), (0.05, 0.028, 0.048), BACK, "Ear_" + side, rot=(-10, 0, -s * 18),
                    rnd=0.4)
        B.add(ear.world((0, -0.029, -0.006)), (0.03, 0.005, 0.028), UNDER, "Ear_" + side, R=ear.R, studs=[],
              role="detail", bevel=0.004)
    # brass frontlet (armour) on the forehead, carrying the star-lotus
    B.add((0, -1.0, 1.12), (0.09, 0.11, 0.018), BRASS, "Head", top=(0.8, 0.8), role="limb")
    B.seg((0, -1.07, 1.125), (0, -1.19, 1.085), 0.062, 0.016, BRASS, "Head", side=(1, 0, 0), top=(0.45, 1),
          role="limb")                                                                      # chanfron down the nose
    B.add((0, -1.115, 1.13), (0.022, 0.022, 0.008), MAG, "Head", rot=(0, 0, 45), studs=[], role="detail",
          bevel=0.004)                                                                      # gem
    B.add((0, -1.165, 1.10), (0.05, 0.012, 0.035), BRASS_D, "Head", bot=(0.4, 1), role="detail", bevel=0.006)
    # ---------------- 5-petal star-lotus (Flower + Petal1-5), magenta blades, brass centre
    fc = Vector(FLOWER_C)
    B.add(fc + Vector((0, 0, 0.02)), (0.05, 0.05, 0.03), BRASS, "Flower", rnd=0.35)
    for i in range(5):
        a = math.radians(90 + 72 * i)
        d = Vector((math.cos(a), math.sin(a), 0.8)).normalized()
        sd = Vector((-math.sin(a), math.cos(a), 0))
        root = fc + Vector((0.03 * math.cos(a), 0.03 * math.sin(a), 0.035))
        Rp = bk.frame_from(root, root + d, sd)
        pn = Rp @ Vector((0, 1, 0))
        if pn.z < 0:
            pn = -pn
        bone = "Petal%d" % (i + 1)
        B.add(root + d * 0.05, (0.075, 0.014, 0.05), MAG, bone, R=Rp, top=(1, 1), bot=(0.45, 1), role="limb",
              rnd=0.2)                                                                          # petal: widening
        B.add(root + d * 0.15, (0.075, 0.014, 0.05), MAG, bone, R=Rp, top=(0.1, 1), bot=(1, 1), role="limb",
              rnd=0.2)                                                                          # ... to a point
        B.add(root + d * 0.09 + pn * 0.015, (0.03, 0.006, 0.07), MAG_D, bone, R=Rp, top=(0.2, 1), bot=(0.6, 1),
              role="detail", bevel=0.004)                                                       # centre vein
    # ---------------- floating brass halo (Halo bone): ring of 10 segments, tilted back a little
    hcv = Vector(HALO_C)
    Rh = Euler((math.radians(-12), 0, 0), "XYZ").to_matrix()
    N = 10
    for i in range(N):
        a0, a1 = 2 * math.pi * i / N, 2 * math.pi * (i + 1) / N
        p0 = hcv + Rh @ Vector((0.21 * math.cos(a0), 0.21 * math.sin(a0), 0))
        p1 = hcv + Rh @ Vector((0.21 * math.cos(a1), 0.21 * math.sin(a1), 0))
        B.seg(p0, p1, 0.026, 0.022, BRASS, "Halo", side=Rh @ Vector((0, 0, 1)), ext=0.012, ext1=0.012, role="limb")
    # ---------------- short legs: dark feet, 4 front toes / 3 hind toes with black claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.06)), K, 0.095, 0.11, FUR, leg, ext1=0.04, top=(0.85, 0.75))
                B.seg(K, A, 0.068, 0.07, FUR, shin, top=(0.85, 0.85), ext=0.04, ext1=0.02)
                toes = (-0.048, -0.016, 0.016, 0.048)
            else:
                B.seg(H + Vector((0, 0.02, 0.06)), K, 0.11, 0.16, FUR, leg, bot=(0.85, 1), top=(0.75, 0.62),
                      ext1=0.04)
                B.seg(K, A, 0.066, 0.07, FUR, shin, top=(0.85, 0.85), ext=0.04, ext1=0.02)
                B.seg(A, P + Vector((0, 0.03, 0.03)), 0.056, 0.056, DARKF, foot, ext=0.03)
                toes = (-0.04, 0.0, 0.04)
            B.add(P, (0.078, 0.09, 0.042), DARKF, foot, top=(0.85, 0.80))
            for gx in toes:
                B.spike((P.x + gx, P.y - 0.08, 0.032), (0, -1, -0.5), 0.055, 0.014, BLACK, foot)
    # ---------------- wings
    for s, side in ((1, "L"), (-1, "R")):
        feather_wing(B, s, side)
    B.build()
    mn, mx = k.bounds()
    pitch = 0.2243 * (mx.z - mn.z) / HEIGHT
    bk.stud_skin(k, pitch)
    return {"TH": round(B.th, 3), "pitch": round(pitch, 4), "H": round(mx.z - mn.z, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.16, 0.64), "Root", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.56, 0.72), "Spine", tail=(0, -0.2, 0.12))
    k.joint("Head", (0, -0.80, 0.84), "Neck", tail=(0, -0.35, 0.05))          # throat pivot
    k.joint("Jaw", (0, -1.08, 0.78), "Head", tail=(0, -0.2, 0))
    k.joint("Flower", FLOWER_C, "Head", tail=(0, 0, 0.12))
    for i in range(5):
        a = math.radians(90 + 72 * i)
        k.joint("Petal%d" % (i + 1), Vector(FLOWER_C) + Vector((0.03 * math.cos(a), 0.03 * math.sin(a), 0.035)),
                "Flower", tail=Vector((math.cos(a), math.sin(a), 1.1)).normalized() * 0.15)
    k.joint("Halo", HALO_C, "Head", tail=(0, 0, 0.12))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.15, -0.83, 1.11), "Head", tail=(0, 0, 0.12))
        k.joint("Lid_" + side, (s * 0.1755, -1.14, 1.052), "Head", tail=(0, -0.1, 0))
        for fb, knee in (("F", (0, 1, 0)), ("B", (0, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, "Spine")
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
        k.joint("Wing_" + side, X(WING.S, s), "Spine")
        k.joint("WingTip_" + side, X(WING.W, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.1))


LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
PETALS = ["Petal%d" % (i + 1) for i in range(5)]


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    P = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
         ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ("Head", "Neck", "Halo", "Flower", "Ear_L", "Ear_R", "Spine", "Leg_FL", "Leg_FR", "Leg_BL",
                  "Leg_BR", "Shin_FL", "Shin_FR", "Shin_BL", "Shin_BR") + tuple(PETALS):
            P.append((w, b))
    for s in ("L", "R"):
        P += [("Leg_F" + s, "Leg_B" + s), ("Shin_F" + s, "Shin_B" + s), ("Foot_F" + s, "Foot_B" + s)]
    P += [("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR", "Leg_FL", "Leg_FR"):
            P.append((a, b))
    P += [("Jaw", "Neck"), ("Jaw", "Spine"), ("Head", "Spine"), ("Halo", "Head"), ("Halo", "Flower"),
          ("Halo", "Ear_L"), ("Halo", "Ear_R"), ("Flower", "Ear_L"), ("Flower", "Ear_R")]
    for p in PETALS:
        P += [(p, "Halo"), (p, "Ear_L"), (p, "Ear_R")]
    return P


def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.13, "Wing_" + sd))
    out.append(((0, -0.80, 0.84), (0, -0.86, 0.90), 0.26, "Head"))
    out.append(((0, -0.56, 0.72), (0, -0.56, 0.72), 0.26, "Neck"))
    return out


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm
FOLD = dict(up=-6, fwd=-6, twist=0, tip=120)          # ground pose: folded bird wing, magenta band down the flank
BUD = dict(up=-12, fwd=14, twist=8, tip=120)          # bloom act: wings wrapped forward round the body like petals
LID_N = {s: Euler((0, math.radians(-s * 14), math.radians(s * 22)), "XYZ").to_matrix() @ Vector((0, -1, 0))
         for s in (1, -1)}


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side=side)


def folded(k, f, du=0.0, dfwd=0.0, dtip=0.0, side=None):
    wings(k, f, FOLD["up"] + du, FOLD["fwd"] + dfwd, FOLD["twist"], FOLD["tip"] + dtip, side)


def blend_w(k, f, A, Bd, t, dtip=0.0):
    wings(k, f, *(A[x] + (Bd[x] - A[x]) * t for x in ("up", "fwd", "twist")), A["tip"] + (Bd["tip"] - A["tip"]) * t
          + dtip)


def lids(k, f, amt):
    """0 = open (plates hidden in the head), 0.5 = heavy half lid, 1 = shut"""
    for s, side in ((1, "L"), (-1, "R")):
        if amt <= 0:
            v = Vector((0, 0, 0))
        else:
            v = LID_N[s] * 0.061 + Vector((0, 0, 0.016 * min(1.0, (1 - amt) / 0.5)))
        k.key("Lid_" + side, f, rot=(0, 0, 0), loc=tuple(v))


def ears(k, f, l=0.0, r=None, fwd=0.0):
    r = l if r is None else r
    k.key("Ear_L", f, rot=(fwd, 0, l))
    k.key("Ear_R", f, rot=(fwd, 0, -r))


def petals(k, f, close=0.0):
    """close + folds the 5 lotus petals up toward a bud (deg), - opens them wider"""
    for i in range(5):
        a = math.radians(90 + 72 * i)
        d = Vector((math.cos(a), math.sin(a), 0.8)).normalized()
        cm.key_axis(k, "Petal%d" % (i + 1), f, d.cross(Vector((0, 0, 1))), close)


def halo(k, f, z=0.0, tilt=0.0, spin=0.0):
    cm.key_axis(k, "Halo", f, (0, 0, 1), spin, loc=(0, 0, z))


def idle(k):
    """ZEN EAR FLICK: stands calm with heavy half lids and a slow sway; 3 rapid ear flicks (left ear at f30, right
    at f75); little nose twitches; the halo bobs and the lotus sways."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        b = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(0, 0, 1.2 * pk.wave(f, n, 0.1)), loc=(0, 0, 0.008 * b))
        k.key("Neck", f, rot=(0, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        lids(k, f, 0.5)
        halo(k, f, z=0.03 * pk.wave(f, n, 0.2, 2))
        k.key("Flower", f, rot=(0, 0, 6 * pk.wave(f, n, 0.35, 2)))
        petals(k, f, 0)
        folded(k, f, du=1.5 * pk.wave(f, n, 0.15, 2))
    for f, p in ((0, 0), (12, 0), (14, 1.5), (16, 0), (18, 1.5), (20, 0), (52, 0), (54, 1.5), (56, 0), (96, 0),
                 (98, 1.5), (100, 0), (102, 1.5), (104, 0), (120, 0)):
        k.key("Head", f, rot=(p, 2 * pk.wave(f, n, 0.1), 0))                   # nose twitches
    for f, l, r in ((0, 0, 0), (29, 0, 0), (30, 26, 0), (32, -4, 0), (34, 26, 0), (36, -4, 0), (38, 24, 0),
                    (41, 0, 0), (74, 0, 0), (75, 0, 26), (77, 0, -4), (79, 0, 26), (81, 0, -4), (83, 0, 24),
                    (86, 0, 0), (120, 0, 0)):
        ears(k, f, l, r)
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 24

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.0 * pk.wave(f, n, 0, 2), 1.5 * pk.wave(f, n, 0.1), 2.0 * pk.wave(f, n)),
              loc=(0, 0, 0.02 * b))
        k.key("Neck", f, rot=(1 * pk.wave(f, n, 0.1, 2), 0, 0))
        k.key("Head", f, rot=(-1.5 * pk.wave(f, n, 0.15, 2), 2 * pk.wave(f, n, 0.1), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        folded(k, f, du=2 * pk.wave(f, n, 0.1, 2))
        ears(k, f, 4 * pk.wave(f, n, 0.2, 2), 4 * pk.wave(f, n, 0.2, 2))
        lids(k, f, 0.5)
        halo(k, f, z=0.025 * pk.wave(f, n, 0.3, 2))
        k.key("Flower", f, rot=(0, 0, 6 * pk.wave(f, n, 0.35, 2)))
        petals(k, f, 0)
    return cm.quad_walk(k, n, 0.13, 0.08, body, gait="trot")


# ---- flight: "swims" through the air - quick short wingbeats, all four legs paddle, head level
FLY_N = 18
PITCH = 6.0
FLY_LIFT = 0.30


def fly_legs(k, f, ph, amt=1.0):
    for leg, off in (("FL", 0.0), ("BR", 0.0), ("FR", 0.5), ("BL", 0.5)):
        w = math.sin(2 * math.pi * (ph + off))
        fr = leg[0] == "F"
        k.key("Leg_" + leg, f, rot=((-10 + 28 * w if fr else 22 + 26 * w) * amt, 0, 0), loc=(0, 0, 0))
        k.key("Shin_" + leg, f, rot=((30 - 20 * w if fr else -10 - 16 * w) * amt, 0, 0))
        k.key("Foot_" + leg, f, rot=((20 + 15 * w) * amt, 0, 0))


def fly_pose(k, f, ph, legs=True):
    w = wing3.stroke(ph, top=32.0, bot=-10.0, down=0.45, sweep=10.0, twist=10.0, fold=26.0)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    k.key("Spine", f, rot=(PITCH - 1.5 * math.sin(2 * math.pi * (ph - 0.1)), 0, 0),
          loc=(0, 0, FLY_LIFT + 0.05 * math.cos(2 * math.pi * (ph - 0.45))))
    k.key("Neck", f, rot=(-2, 0, 0))
    k.key("Head", f, rot=(-PITCH + 1.5 * math.sin(2 * math.pi * (ph - 0.1)), 0, 0))     # head stays level
    k.key("Jaw", f, rot=(0, 0, 0))
    lag = math.cos(2 * math.pi * (ph - 0.13))
    ears(k, f, 0, 0, fwd=-14 - 3 * lag)
    lids(k, f, 0.5)
    halo(k, f, z=-0.02 * lag)
    k.key("Flower", f, rot=(6 + 4 * lag, 0, 0))
    petals(k, f, 0)
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
    for b in ("Neck", "Head", "Jaw"):
        k.key(b, f, rot=(0, 0, 0))
    folded(k, f)
    ears(k, f, 0, 0)
    lids(k, f, 0.5)
    halo(k, f)
    k.key("Flower", f, rot=(0, 0, 0))
    petals(k, f, 0)


def plant_frames(k, frames):
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


def takeoff(k):
    """crouch with the wings lifting high (0-10), LAUNCH at 11 on a big downstroke + leg push, into flight"""
    n = 27
    k.new_action("takeoff", n, False)
    rest_keys(k, 0)
    for f, z, p, w in ((6, -0.07, 3, (34, -6, -4, 60)), (10, -0.09, 4, (40, -4, -6, 0)),
                       (13, 0.22, -4, (-20, 10, 8, 4)), (17, 0.34, 4, (22, 0, 0, -8))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(0, 0, 0))
        k.key("Head", f, rot=(-4 - p * 0.5, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        wings(k, f, *w)
        ears(k, f, 0, 0, fwd=-10 if f >= 13 else 0)
        lids(k, f, 0.5)
        halo(k, f, z=0.02)
        k.key("Flower", f, rot=(0, 0, 0))
        petals(k, f, 0)
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
    """flare (nose up, wings forward as an air brake, legs reach), touch down at 16, absorb, settle"""
    n = 27
    k.new_action("land", n, False)
    fly_pose(k, 0, 0.0)
    for f, z, p, w in ((7, 0.12, -10, (30, 16, -10, -8)), (12, 0.06, -6, (-8, 10, -6, 4)),
                       (16, -0.06, 3, (16, -4, 0, 40)), (21, 0.02, -1, (22, -6, 0, 96))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(0, 0, 0))
        k.key("Head", f, rot=(-4 - p * 0.3, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        wings(k, f, *w)
        ears(k, f, 0, 0, fwd=-10 if f < 16 else 0)
        lids(k, f, 0.5)
        halo(k, f, z=0.03 if f < 21 else 0.0)
        k.key("Flower", f, rot=(0, 0, 0))
        petals(k, f, 0)
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
    """ALARM BARK: 3 sharp barks - each one jolts the body forward, the jaw pops open, the wings snap half open,
    the ears snap forward - then she settles."""
    n = 54
    k.new_action("roar", n, False)
    rest_keys(k, 0)
    for i, b0 in enumerate((8, 20, 32)):
        for df, jolt, jw, wo, ef in ((0, 0.0, 0, 0.0, 0), (3, 0.03, 25, 1.0, 16), (7, 0.01, 6, 0.6, 10),
                                     (10, 0.0, 0, 0.3, 4)):
            f = b0 + df
            k.key("Spine", f, rot=(1.5 * jolt / 0.03, 0, 0), loc=(0, -jolt, 0))
            k.key("Neck", f, rot=(-2 * jolt / 0.03, 0, 0))
            k.key("Head", f, rot=(-4 * jolt / 0.03, 0, 0))
            k.key("Jaw", f, rot=(jw, 0, 0))
            blend_w(k, f, FOLD, dict(up=34, fwd=-2, twist=0, tip=40), wo)
            ears(k, f, 0, 0, fwd=ef)
            lids(k, f, 0.0 if wo > 0.5 else 0.3)
            halo(k, f, z=0.02 * wo)
            k.key("Flower", f, rot=(0, 0, 0))
            petals(k, f, -8 * wo)
    rest_keys(k, 50)
    rest_keys(k, n)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def bloom(k):
    """SIGNATURE (Cvetibara only) - HOT-SPRING BLOOM: sinks belly-down as into a hot spring (lids shut, one ear
    flick), curls into a BUD (wings wrap forward round the body like closing petals, head tucks, the lotus folds
    shut), holds it with a small quiver, then BLOOMS - springs up, wings burst open wide and up, petals snap open,
    head up - holds the bloom with a slow head turn and a wing shimmer, then folds and settles."""
    n = 100
    k.new_action("act_bloom", n, False)
    OPEN = dict(up=40, fwd=0, twist=0, tip=-8)
    P = [(0, 0.0, 0, 0, 0.5, 0, "F", 0.0, 0), (16, -0.22, 2, 4, 1.0, 0, "F", 0.0, 0),
         (30, -0.22, 10, 16, 1.0, 34, "B", 1.0, 0), (44, -0.22, 10, 16, 1.0, 34, "B", 1.0, 0),
         (50, 0.04, -8, -10, 0.0, -10, "O", 1.0, 0), (54, 0.0, -6, -8, 0.0, -10, "O", 1.0, 0),
         (64, 0.0, -6, -8, 0.0, -10, "O", 1.0, 14), (74, 0.0, -6, -8, 0.0, -10, "O", 1.0, -14),
         (88, 0.0, 0, 0, 0.5, 0, "F", 0.0, 0), (100, 0.0, 0, 0, 0.5, 0, "F", 0.0, 0)]
    for f, z, nk, hd, lid, pet, wmode, wt, yaw in P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        lids(k, f, lid)
        petals(k, f, pet)
        if wmode == "F":
            folded(k, f)
        elif wmode == "B":
            blend_w(k, f, FOLD, BUD, wt)
        else:
            wings(k, f, OPEN["up"], OPEN["fwd"], OPEN["twist"], OPEN["tip"])
        halo(k, f, z=0.06 if wmode == "O" else 0.0, spin=0.0)
        k.key("Flower", f, rot=(0, 0, 0))
        ears(k, f, 0, 0)
    for f, l in ((8, 0), (10, 24), (12, -4), (14, 0)):                        # one ear flick in the spa
        ears(k, f, l, 0)
    for f in range(34, 44, 2):                                                # the bud quivers
        w = 1 if (f // 2) % 2 else -1
        blend_w(k, f, FOLD, BUD, 1.0, dtip=2.5 * w)
    for f in range(56, 72, 4):                                                # the open wings shimmer
        w = 1 if (f // 4) % 2 else -1
        wings(k, f, OPEN["up"] + 3 * w, 0, 0, OPEN["tip"] - 4 * w)
    for f, a in ((44, 0), (52, 180), (60, 360), (100, 360)):                  # the halo spins once as she blooms
        halo(k, f, z=0.06 if 48 <= f <= 74 else 0.0, spin=a)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    bloom(k)
    return stride


HEAD_XF = []
