# Permafrost Titan (Glacier egg SECRET 2.5 %, 2026-10-27) - plan _review/PermafrostTitan_plan.md v2, hero = OPTION A
# (owner decision): THE GOLD CHEST BEZEL. An upright, forward-hunched mauve-stone ice giant in the FIERCE studded
# style: rounded studded stone masses split by dark slate joints, darker plum armour plates (bracers, shin guards,
# thigh plates, back slabs), two rounded pauldrons per shoulder capped with crusts of white glacier ice, long arms
# ending in boulder fists with white ice knuckle crusts, pillar legs on wedge three-toed feet, a small bare head sunk
# between the shoulders (slate brow shelf, deep-set white ice slits, black slit pupils, flat closed mouth) and THE
# HERO: a 12-facet house-gold bezel ring (gold-dark inner lining, four gold settings) set into the chest around a
# faceted ice-white core, echoed by a small gold ring on the back hump for the game camera (round 2). No spikes, no
# crown, no cyan, no glow (core pulse / frost drift / ice dust = Studio VFX).
import math
from mathutils import Vector, Matrix, Euler

DISPLAY = "Permafrost Titan"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 10.0                # studs to the top of the head (option A: no head piece) - equal to Thunder Rex

# Blender colours (Roblox renders ~0.6x darker)
MAUVE = (146, 101, 178)     # body: stone masses, pauldron bodies, head, limbs (studded); plan (184,150,200)
                             # deepened 2026-10-27 (same hue 275-281): the plan value read pastel next to
                             # every approved pet in the 64 px strip; r2 (NICE 1) lifted from (136,94,166)
PLUM = (86, 56, 112)         # armour plates: bracers, shin guards, thigh plates, back slabs, trapezius, crown cap
ICE_W = (226, 240, 250)      # pauldron caps, chest core, knuckle crusts, eye slits (smooth)
JOINT_D = (52, 60, 84)       # joints, gaps, brow ridge, eye sockets, toe blocks
GOLD = (255, 196, 50)        # THE hero: the chest bezel ring + its settings, and the small back echo ring (r2)
GOLD_D = (214, 150, 30)      # the bezels' inner lining
BLACK = (14, 14, 22)         # pupils, toe claws
MOUTH = (86, 18, 30)         # mouth slit

H_MODEL = 2.03               # head top in Blender units (measured)
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

HIP, KNEE, ANKLE = (0.22, 0.04, 0.86), (0.25, -0.06, 0.50), (0.25, 0.02, 0.165)
SHOULDER, ELBOW, WRIST = (0.48, 0.05, 1.56), (0.645, 0.12, 1.15), (0.645, -0.10, 0.83)
FIST = (0.635, -0.155, 0.69)
THROAT = (0.0, -0.10, 1.66)
CORE = (0, -0.30, 1.45)       # filled in by model(): chest core centre on the chest face (VFX anchor)
CORE_N = (0, -1, 0)
HERO = (0, -0.32, 1.67)       # filled in by model(): bezel top (glint anchor)
CAP = (0.53, 0.0, 1.88)       # filled in by model(): upper pauldron ice cap top (left)
BACK = (0, 0.40, 1.70)        # filled in by model(): back echo ring centre (r2; glint VFX anchor, on Chest)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def surf_hit(B, blks, origin, direction):
    """first hit of a ray on the given parts (blocks or tubes) -> (point, outward normal) (AbyssWeaver)"""
    import blockkit as bk
    from mathutils.bvhtree import BVHTree
    B._resolve()
    best = None
    d = Vector(direction).normalized()
    for blk in blks:
        bm = bk.part_bm(blk)
        t = BVHTree.FromBMesh(bm)
        bm.free()
        loc, nrm, _, dist = t.ray_cast(Vector(origin), d)
        if loc is not None and (best is None or dist < best[2]):
            best = (loc, nrm.normalized(), dist)
    if best is None:
        raise RuntimeError("surf_hit: no surface from %s" % (tuple(origin),))
    return best[0], best[1]


def face_R(nn, up=(0, 0, 1)):
    """frame whose local -y is the outward normal nn and local z points as close to `up` as possible"""
    y = -Vector(nn).normalized()
    z = Vector(up) - y * y.dot(Vector(up))
    if z.length < 1e-3:
        z = Vector((0, 1, 0)) - y * y.y
    z.normalize()
    return Matrix((y.cross(z), y, z)).transposed()


def ice_eye(B, c, s, n, bone="Head", tilt=20.0, sc=1.0):
    """slate socket (inner corner down) -> ice-white slit -> black slit pupil at the inner end (no glint)"""
    R = face_R(n) @ Euler((0, math.radians(-s * tilt), 0), "XYZ").to_matrix()
    nn = Vector(n).normalized()
    c = Vector(c)
    kw = dict(R=R, studs=[], role="detail")
    B.add(c, (0.060 * sc, 0.008, 0.030 * sc), JOINT_D, bone, bevel=0.005, top=(0.78, 1.0), **kw)   # socket
    B.add(c + nn * 0.006 + R @ Vector((0, 0, -0.004)), (0.047 * sc, 0.006, 0.0105 * sc), ICE_W, bone,
          bevel=0.003, top=(0.55, 1.0), **kw)                                                    # ice slit (wedge)
    B.add(c + nn * 0.010 + R @ Vector((-s * 0.004 * sc, 0, -0.004)), (0.0036 * sc, 0.004, 0.0108 * sc), BLACK,
          bone, bevel=0.0015, **kw)                                                              # reptile pupil


def ice_chunk(B, base, d, L, w, bone, side=(1, 0, 0), color=None):
    """blunt glacier ice chunk (flat facetted top, never a point): a short tapered block standing on base along d"""
    import blockkit as bk
    base, d = Vector(base), Vector(d).normalized()
    tip = base + d * L
    return B.add((base + tip) / 2, (w, w * 0.80, L / 2), color or ICE_W, bone, R=bk.frame_from(base, tip, side),
                 top=(0.62, 0.48), nostud=True, role="limb", rnd=0.10)


def model(k):
    import blockkit as bk
    global CORE, CORE_N, HERO, CAP, BACK
    B = bk.Blocks(k, seed=2501, tier=4, plates=False)
    up = Vector((0, 0, 1))
    # ================= pelvis + waist (Spine): heavy hips, plum side plates, dark belt joint, tapered waist
    B.add((0, 0.04, 0.90), (0.30, 0.21, 0.13), MAUVE, "Spine", bot=(0.80, 0.82), top=(1.0, 1.0), rnd=0.36)
    B.mirror((0.272, 0.045, 0.885), (0.058, 0.17, 0.12), PLUM, "Spine", rot=(0, 10, 0), bot=(0.8, 0.85), rnd=0.38)
    B.add((0, 0.03, 1.03), (0.268, 0.19, 0.04), JOINT_D, "Spine", rnd=0.4)                           # belt joint
    B.add((0, 0.02, 1.10), (0.262, 0.19, 0.08), MAUVE, "Spine", bot=(0.95, 0.95), top=(1.08, 1.06), rnd=0.36)
    # ================= chest (Chest): deep stone ribcage leaning forward (inverted triangle), plum back hump
    rib = B.add((0, 0.0, 1.42), (0.38, 0.28, 0.29), MAUVE, "Chest", rot=(10, 0, 0), bot=(0.70, 0.74),
                top=(1.0, 0.92), rnd=0.32)
    B.add((0, 0.05, 1.165), (0.28, 0.20, 0.035), JOINT_D, "Chest", rnd=0.4)                          # chest/waist gap
    hump = B.add((0, 0.175, 1.675), (0.30, 0.19, 0.13), PLUM, "Chest", rot=(-14, 0, 0), top=(0.60, 0.66),
                 rnd=0.42)                                                                          # back hump
    # back: two dark-gapped plum stone slabs (the game camera sees the back)
    for z0, z1, w in ((1.58, 1.40, 0.27), (1.36, 1.20, 0.23)):
        a, na = surf_hit(B, [rib], (0, 1.0, z0), (0, -1, 0))
        b, nb = surf_hit(B, [rib], (0, 1.0, z1), (0, -1, 0))
        n = (na + nb).normalized()
        B.add((a + b) / 2 + n * 0.014, (0.034, w, (a - b).length / 2), PLUM, "Chest",
              R=bk.frame_from(b, a, n), top=(1, 0.9), rnd=0.40)
        g = b - (a - b).normalized() * 0.022 + n * 0.006
        B.add(g, (0.012, w * 0.80, 0.022), JOINT_D, "Chest", R=bk.frame_from(b, a, n), studs=[], role="detail",
              bevel=0.004)
    # glacier crust breaking out of the back hump (blunt, flat-topped ice blocks - never spikes)
    for x, y, L, w, lean in ((0.0, 0.10, 0.15, 0.065, (0, 0.45, 1)), (0.12, 0.05, 0.11, 0.055, (0.5, 0.35, 1)),
                             (-0.13, 0.07, 0.12, 0.055, (-0.5, 0.4, 1)), (0.05, 0.11, 0.08, 0.045, (0.2, 0.9, 1))):
        bp, bn = surf_hit(B, [hump], (x, y + 0.17, 2.5), (0, 0, -1))
        ice_chunk(B, bp - bn * 0.03, Vector(lean), L + 0.03, w, "Chest")
    # ================= back echo of the hero (r2 MUST 1): a small gold bezel on the back face of the hump (the game
    # camera sees the back) - 12 gold facets + gold-dark lining around a small ice disc; no settings, no crown
    bp_, bn_ = surf_hit(B, [hump], (0, 1.0, 1.685), (0, -1, 0))
    brn = (bn_ + up * math.tan(math.radians(8))).normalized()
    bu = Vector((1, 0, 0))
    bv = brn.cross(bu).normalized()
    if bv.z < 0:
        bv = -bv
    BR_OUT, BR_IN, BDEPTH, BPROUD = 0.105, 0.070, 0.06, 0.030
    brc = bp_ + brn * (BPROUD - BDEPTH / 2)
    brm = (BR_OUT + BR_IN) / 2
    for i in range(12):
        a0, a1 = 2 * math.pi * (i + 0.5) / 12, 2 * math.pi * (i + 1.5) / 12
        am = (a0 + a1) / 2
        rad = bu * math.cos(am) + bv * math.sin(am)
        B.seg(brc + (bu * math.cos(a0) + bv * math.sin(a0)) * brm, brc + (bu * math.cos(a1) + bv * math.sin(a1)) * brm,
              (BR_OUT - BR_IN) / 2, BDEPTH / 2, GOLD, "Chest", side=rad, ext=0.007, ext1=0.007, studs=[], nostud=True,
              role="limb", rnd=0.22)
        B.seg(brc + (bu * math.cos(a0) + bv * math.sin(a0)) * (BR_IN - 0.008) + brn * 0.003,
              brc + (bu * math.cos(a1) + bv * math.sin(a1)) * (BR_IN - 0.008) + brn * 0.003, 0.011,
              BDEPTH / 2 - 0.010, GOLD_D, "Chest", side=rad, ext=0.004, ext1=0.004, studs=[], nostud=True,
              role="detail", bevel=0.003)
    B.poly([brc + brn * (BDEPTH / 2 - 0.010) + (bu * math.cos(a) + bv * math.sin(a)) * 0.050
            for a in [2 * math.pi * (j + 0.5) / 8 for j in range(8)]], 0.016, ICE_W, "Chest")      # ice disc
    BACK = tuple(brc + brn * 0.04)
    # ================= THE HERO: gold chest bezel (12 facets, tilted 10 deg up) around a faceted ice core
    cp, cn = surf_hit(B, [rib], (0, -1.0, 1.40), (0, 1, 0))
    rn = (cn + up * math.tan(math.radians(10))).normalized()           # ring normal: the chest face tilted 10 up
    u = Vector((1, 0, 0))
    v = rn.cross(u).normalized()
    if v.z < 0:
        v = -v
    R_OUT, R_IN, DEPTH, PROUD = 0.240, 0.150, 0.10, 0.045              # r2 NICE 2: outer 0.225 -> 0.240
    rc = cp + rn * (PROUD - DEPTH / 2)                                 # ring centre plane (half sunk in the chest)
    CORE, CORE_N = tuple(cp + rn * 0.02), tuple(rn)
    rm = (R_OUT + R_IN) / 2
    for i in range(12):
        a0, a1 = 2 * math.pi * (i + 0.5) / 12, 2 * math.pi * (i + 1.5) / 12
        p0 = rc + (u * math.cos(a0) + v * math.sin(a0)) * rm
        p1 = rc + (u * math.cos(a1) + v * math.sin(a1)) * rm
        am = (a0 + a1) / 2
        rad = u * math.cos(am) + v * math.sin(am)
        B.seg(p0, p1, (R_OUT - R_IN) / 2, DEPTH / 2, GOLD, "Chest", side=rad, ext=0.013, ext1=0.013,
              studs=[], nostud=True, role="limb", rnd=0.22)
        q0 = rc + (u * math.cos(a0) + v * math.sin(a0)) * (R_IN - 0.012) + rn * 0.004
        q1 = rc + (u * math.cos(a1) + v * math.sin(a1)) * (R_IN - 0.012) + rn * 0.004
        B.seg(q0, q1, 0.018, DEPTH / 2 - 0.014, GOLD_D, "Chest", side=rad, ext=0.006, ext1=0.006, studs=[],
              nostud=True, role="detail", bevel=0.004)
    # four gold settings clamping the ring to the chest (diagonals), low and blunt (no spikes)
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        rad = u * math.cos(a) + v * math.sin(a)
        p0 = rc + rad * (R_OUT - 0.012) + rn * 0.012
        p1 = rc + rad * (R_OUT + 0.06) - rn * 0.012
        B.seg(p0, p1, 0.032, 0.022, GOLD, "Chest", side=rn.cross(rad), studs=[], nostud=True, role="limb",
              top=(0.8, 0.6), rnd=0.3)
    HERO = tuple(rc + v * R_OUT + rn * 0.06)
    # the faceted ice core: octagon disc -> raised diamond -> raised centre facet (all ice-white, smooth)
    Rc = face_R(rn, up=v)
    B.poly([rc + rn * (DEPTH / 2 - 0.012) + (u * math.cos(a) + v * math.sin(a)) * 0.119
            for a in [2 * math.pi * (j + 0.5) / 8 for j in range(8)]], 0.032, ICE_W, "Chest")      # octagon ice disc
    for rot, hs, dz in ((45, 0.066, 0.016), (45, 0.034, 0.030)):                     # raised diamond + top facet
        Rr = Rc @ Euler((0, math.radians(rot), 0), "XYZ").to_matrix()
        B.add(rc + rn * (DEPTH / 2 - 0.012 + dz), (hs, 0.016, hs), ICE_W, "Chest", R=Rr, studs=[], nostud=True,
              role="limb", rnd=0.16)
    # pecs: two rounded stone masses above-outside the ring
    for s in (1, -1):
        pp, pn = surf_hit(B, [rib], (s * 0.27, -1.0, 1.585), (0, 1, 0))
        B.add(pp + pn * 0.035, (0.11, 0.045, 0.092), MAUVE, "Chest", R=face_R(pn) @ Euler(
            (0, math.radians(-s * 14), 0), "XYZ").to_matrix(), rnd=0.44, top=(0.9, 1.0))
    # ================= neck + head (throat pivot): dark neck joint, small skull sunk low and forward
    B.add((0, -0.10, 1.66), (0.102, 0.098, 0.070), JOINT_D, "Head", rnd=0.50)                         # neck joint
    # (a rounded slate knuckle centred on the throat pivot: a head bow / lift turns it in place)
    skull = B.add((0, -0.235, 1.84), (0.145, 0.150, 0.128), MAUVE, "Head", top=(0.84, 0.86), rnd=0.30)
    B.add((0, -0.20, 1.962), (0.112, 0.112, 0.032), PLUM, "Head", top=(0.8, 0.8), rnd=0.42)            # crown cap
    for s in (1, -1):
        B.add((s * 0.134, -0.272, 1.795), (0.045, 0.085, 0.065), MAUVE, "Head", rot=(0, 0, s * 8), rnd=0.42)  # cheek
    fp, fn = surf_hit(B, [skull], (0, -1.0, 1.87), (0, 1, 0))
    # slate brow ridge: two chunky halves (20 deg inner-down) meeting over the nose, set into the forehead
    for s in (1, -1):
        Rb = face_R(fn) @ Euler((0, math.radians(-s * 28), 0), "XYZ").to_matrix()          # r2 MUST 2: slabs
        B.add(fp + fn * 0.010 + Vector((s * 0.070, 0, -0.001)), (0.076, 0.032, 0.028), JOINT_D, "Head", R=Rb,
              role="limb", rnd=0.06, studs=[], nostud=True)
    B.seg(fp + fn * 0.010 + Vector((0, 0, -0.025)), fp + fn * 0.040 + Vector((0, 0, -0.095)), 0.028, 0.024,
          MAUVE, "Head", top=(1.25, 1.0), rnd=0.4)                                                   # nasal ridge
    for s in (1, -1):                                                                               # deep-set eyes
        ep, en = surf_hit(B, [skull], (s * 0.072, -1.0, 1.838), (0, 1, 0))
        ice_eye(B, ep + en * 0.003, s, en, tilt=20, sc=0.95)
    # jaw: heavy square chin (Jaw bone) jutting forward; the mouth is the dark seam between skull and jaw
    B.add((0, -0.295, 1.732), (0.120, 0.105, 0.046), MAUVE, "Jaw", top=(1.0, 0.95), bot=(0.84, 0.86), rnd=0.34)
    B.add((0, -0.384, 1.762), (0.088, 0.008, 0.0045), MOUTH, "Head", studs=[], role="detail", bevel=0.002)
    # ================= arms: shoulder boulder, upper arm, slate elbow, flared forearm under a plum bracer,
    # boulder fist with curled fingers and ice knuckle crusts; two ice-capped pauldrons per shoulder
    for s, side in ((1, "L"), (-1, "R")):
        arm, fore, hand = "Arm_" + side, "Fore_" + side, "Hand_" + side
        Sv, Ev, Wv, Fv = X(SHOULDER, s), X(ELBOW, s), X(WRIST, s), X(FIST, s)
        B.add(Sv + Vector((s * 0.03, 0.0, -0.01)), (0.155, 0.165, 0.150), MAUVE, arm, rnd=0.45)        # deltoid
        B.seg(Sv, Ev, 0.128, 0.138, MAUVE, arm, ext=0.0, ext1=0.03, top=(0.88, 0.88), rnd=0.40)       # upper arm
        de = (Wv - Ev).normalized()
        B.seg(Ev - de * 0.025, Ev + de * 0.05, 0.120, 0.130, JOINT_D, fore, rnd=0.36)                 # elbow joint
        B.seg(Ev, Wv, 0.130, 0.140, MAUVE, fore, ext=0.02, ext1=0.0, top=(1.12, 1.10), rnd=0.38)      # forearm
        br = B.seg(Ev + de * 0.11, Wv - de * 0.06, 0.150, 0.158, PLUM, fore, top=(1.07, 1.05), rnd=0.40)  # bracer
        for t_, L, w, lean in ((0.35, 0.075, 0.042, 0.5), (0.70, 0.065, 0.038, 0.8)):                 # ice crusts
            q = (Ev + de * 0.11).lerp(Wv - de * 0.06, t_)
            ice_chunk(B, q + Vector((s * 0.135, 0.02, 0.0)), (s * 1.0, 0.25, lean), L, w, fore)
        B.seg(Wv - de * 0.05, Wv + de * 0.035, 0.130, 0.138, JOINT_D, fore, rnd=0.36)                 # wrist joint
        fist = B.add(Fv, (0.162, 0.162, 0.142), MAUVE, hand, rot=(-14, 0, 0), rnd=0.46)               # fist
        for gx in (-0.090, -0.030, 0.030, 0.090):                                                     # curled fingers
            B.add(fist.world((gx * s, -0.155, -0.042)), (0.027, 0.032, 0.058), MAUVE, hand, R=fist.R, rnd=0.55)
        B.add(fist.world((-s * 0.11, -0.10, 0.035)), (0.048, 0.055, 0.065), PLUM, hand, R=fist.R, rnd=0.42)  # thumb
        for gx, L, tw in ((-0.080, 0.090, 0.040), (0.0, 0.112, 0.044), (0.080, 0.090, 0.040)):        # ice knuckles
            base = fist.world((gx * s, -0.112, 0.112))
            ice_chunk(B, base, fist.R @ Vector((gx * s * 0.8, -0.75, 0.7)), L, tw, hand)
        # ---- pauldron 1 (upper, over the shoulder) + its glacier crust (one slab + 3 broken blocks)
        p1 = B.add(Sv + Vector((s * 0.04, 0.005, 0.17)), (0.188, 0.208, 0.088), MAUVE, arm,
                   rot=(0, s * 18, 0), top=(0.84, 0.86), bot=(0.80, 0.80), rnd=0.55)
        c1 = B.add(p1.world((0, 0, 0.088)), (0.120, 0.140, 0.030), ICE_W, arm, R=p1.R, top=(0.82, 0.84),
                   nostud=True, role="limb", rnd=0.30)
        for dx, dy, L, w, lean in ((0.05, -0.06, 0.13, 0.062, 0.45), (0.085, 0.085, 0.095, 0.052, 0.75),
                                   (-0.05, 0.05, 0.075, 0.048, -0.15)):
            ice_chunk(B, p1.world((s * dx, dy, 0.10)), p1.R @ Vector((s * lean, dy * 0.8, 1.0)), L, w, arm)
        # ---- pauldron 2 (lower, outer, on the upper arm) + its crust
        p2 = B.add(Sv + Vector((s * 0.19, 0.02, -0.03)), (0.090, 0.170, 0.115), MAUVE, arm,
                   rot=(0, s * 42, 0), top=(0.80, 0.84), rnd=0.45)
        B.add(p2.world((0, 0, 0.110)), (0.068, 0.135, 0.032), ICE_W, arm, R=p2.R, top=(0.80, 0.82), nostud=True,
              role="limb", rnd=0.22)
        ice_chunk(B, p2.world((0.0, -0.04, 0.12)), p2.R @ Vector((s * 0.35, -0.2, 1.0)), 0.085, 0.048, arm)
        if s > 0:
            CAP = tuple(c1.world((0, 0, 0.06)))
    # ================= legs: pillar thighs (plum outer plates) + shins (plum guards), slate knee/ankle joints,
    # blocky feet with 3 slate toes
    for s, side in ((1, "L"), (-1, "R")):
        leg, shin, foot = "Leg_" + side, "Shin_" + side, "Foot_" + side
        H, K, A = X(HIP, s), X(KNEE, s), X(ANKLE, s)
        B.seg(H + Vector((0, 0.0, 0.07)), K, 0.165, 0.180, MAUVE, leg, ext=0.0, ext1=0.02, top=(0.86, 0.84),
              rnd=0.40)                                                                                # thigh
        B.seg(H + Vector((s * 0.12, 0.01, 0.0)), K + Vector((s * 0.095, 0.0, 0.10)), 0.046, 0.155, PLUM, leg,
              top=(0.75, 0.70), rnd=0.42)                                                              # thigh plate
        dk = (A - K).normalized()
        B.seg(K - dk * 0.035, K + dk * 0.05, 0.138, 0.150, JOINT_D, shin, rnd=0.38)                    # knee joint
        B.add(K + Vector((0, -0.145, 0.0)), (0.10, 0.04, 0.088), PLUM, shin, rnd=0.55)                 # knee cap
        B.seg(K, A, 0.143, 0.152, MAUVE, shin, ext=0.0, ext1=0.0, top=(1.14, 1.12), rnd=0.38)          # pillar shin
        B.seg(K + Vector((0, -0.128, -0.085)), A + Vector((0, -0.152, 0.07)), 0.116, 0.034, PLUM, shin,
              top=(1.15, 1.0), rnd=0.40)                                                               # shin guard
        B.seg(A - Vector((0, 0, 0.005)), A + Vector((0, 0, 0.015)), 0.155, 0.164, JOINT_D, foot, rnd=0.35)  # ankle
        F = Vector((A.x, A.y - 0.06, 0.07))
        B.seg(F + Vector((0, 0.222, 0)), F - Vector((0, 0.222, 0)), 0.178, 0.07, MAUVE, foot, side=(1, 0, 0),
              top=(0.70, 0.86), rnd=0.45)                                                     # wedge foot (r2)
        for gx in (-0.11, 0.0, 0.11):                                                                   # 3 toes
            B.add(Vector((A.x + gx, A.y - 0.295, 0.05)), (0.048, 0.056, 0.05), JOINT_D, foot, rnd=0.40)
            B.spike(Vector((A.x + gx, A.y - 0.345, 0.03)), (0, -1, -0.45), 0.04, 0.02, BLACK, foot)
    B.build()
    bk.stud_skin(k, PITCH)
    mn, mx = k.bounds()
    return {"TH": round(B.th, 3), "PITCH": PITCH, "H": round(mx.z, 3), "lowest": round(mn.z, 3),
            "size": [round(v, 3) for v in (mx - mn)], "CORE": [round(v, 3) for v in CORE],
            "HERO": [round(v, 3) for v in HERO], "BACK": [round(v, 3) for v in BACK]}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.03, 0.92), "Root", tail=(0, 0, 0.22))
    k.joint("Chest", (0, 0.02, 1.15), "Spine", tail=(0, -0.05, 0.40))
    k.joint("Head", THROAT, "Chest", tail=(0, -0.2, 0.18))                   # throat pivot
    k.joint("Jaw", (0, -0.19, 1.755), "Head", tail=(0, -0.2, -0.02))
    k.joint("Core", CORE, "Chest", tail=tuple(Vector(CORE_N) * 0.15))
    k.joint("Hero", HERO, "Chest", tail=(0, -0.1, 0.1))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Arm_" + side, X(SHOULDER, s), "Chest")
        k.joint("Fore_" + side, X(ELBOW, s), "Arm_" + side)
        k.joint("Hand_" + side, X(WRIST, s), "Fore_" + side, tail=(0, -0.05, -0.25))
        k.add_leg2("Arm_" + side, "Fore_" + side, "Hand_" + side, knee=(s * 0.3, 1.0, 0))      # elbows bend back
        k.joint("Pauldron_" + side, X(CAP, s), "Arm_" + side, tail=(0, 0, 0.12))
        k.joint("Fist_" + side, X(FIST, s) + Vector((0, -0.17, 0.08)), "Hand_" + side, tail=(0, -0.1, 0))
        k.joint("Leg_" + side, X(HIP, s), "Spine")
        k.joint("Shin_" + side, X(KNEE, s), "Leg_" + side)
        k.joint("Foot_" + side, X(ANKLE, s), "Shin_" + side, tail=(0, -0.2, -0.1))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
    k.joint("Knee_R", X(KNEE, -1) + Vector((0, -0.20, 0.0)), "Shin_R", tail=(0, -0.1, 0))


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Head", "Chest"), ("Jaw", "Chest"),
         ("Head", "Arm_L"), ("Head", "Arm_R"), ("Jaw", "Arm_L"), ("Jaw", "Arm_R"), ("Hand_L", "Hand_R")]
    for s in ("L", "R"):
        for a in ("Fore_" + s, "Hand_" + s):
            for b in ("Spine", "Chest", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Foot_L", "Foot_R"):
                P.append((a, b))
        P.append(("Arm_" + s, "Spine"))
    return P


def joints():
    out = [((0, -0.02, 1.62), (0, -0.12, 1.70), 0.17, "Head")]
    for s, side in ((1, "L"), (-1, "R")):
        out.append((X(WRIST, s), X(WRIST, s), 0.15, "Hand_" + side))
        out.append((X(ELBOW, s), X(ELBOW, s), 0.15, "Fore_" + side))
        out.append((X(KNEE, s), X(KNEE, s), 0.16, "Shin_" + side))
        out.append((X(ANKLE, s), X(ANKLE, s), 0.16, "Foot_" + side))
        out.append((X(HIP, s), X(HIP, s), 0.20, "Leg_" + side))
    return out


HEAD_XF = [((0, -0.10, 1.66), 1.0, ["Head", "Jaw"], (0, -0.03, 0.035))]   # head group lifted / forward (chin
#   clears the chest top in the kneel bow and the bellow lift) - a pure translation, built at final size
