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
MAUVE = (164, 116, 200)     # f85 MUST 1 (was 146,101,178) body: stone masses, pauldron bodies, head, limbs (studded); plan (184,150,200)
                             # deepened 2026-10-27 (same hue 275-281): the plan value read pastel next to
                             # every approved pet in the 64 px strip; r2 (NICE 1) lifted from (136,94,166)
PLUM = (98, 66, 130)         # f85 MUST 1 (was 86,56,112) armour plates: bracers, shin guards, thigh plates, back slabs, trapezius, crown cap
ICE_W = (226, 240, 250)      # pauldron caps, chest core, knuckle crusts, eye slits (smooth)
JOINT_D = (52, 60, 84)       # joints, gaps, brow ridge, eye sockets, toe blocks
GOLD = (255, 196, 50)        # THE hero: the chest bezel ring + its settings, and the small back echo ring (r2)
GOLD_D = (214, 150, 30)      # the bezels' inner lining
BLACK = (14, 14, 22)         # pupils, toe claws
MOUTH = (86, 18, 30)         # mouth slit

H_MODEL = 2.057              # head top in Blender units (measured; f85: the bigger head 2.03 -> 2.057)
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


def ice_eye(B, c, s, n, bone="Head", tilt=20.0, sc=1.0, wx=1.0):
    """slate socket (inner corner down) -> ice-white slit -> black slit pupil at the inner end (no glint)"""
    R = face_R(n) @ Euler((0, math.radians(-s * tilt), 0), "XYZ").to_matrix()
    nn = Vector(n).normalized()
    c = Vector(c)
    kw = dict(R=R, studs=[], role="detail")
    B.add(c, (0.060 * sc * wx, 0.008, 0.030 * sc), JOINT_D, bone, bevel=0.005, top=(0.78, 1.0), **kw)   # socket
    B.add(c + nn * 0.006 + R @ Vector((0, 0, -0.004)), (0.047 * sc * wx, 0.006, 0.0105 * sc), ICE_W, bone,
          bevel=0.003, top=(0.55, 1.0), **kw)                                                    # ice slit (wedge)
    B.add(c + nn * 0.010 + R @ Vector((-s * 0.004 * sc, 0, -0.004)), (0.0036 * sc, 0.004, 0.0108 * sc), BLACK,
          bone, bevel=0.0015, **kw)                                                              # reptile pupil


def ice_chunk(B, base, d, L, w, bone, side=(1, 0, 0), color=None, top=(0.62, 0.48)):
    """blunt glacier ice chunk (flat facetted top, never a point): a short tapered block standing on base along d"""
    import blockkit as bk
    base, d = Vector(base), Vector(d).normalized()
    tip = base + d * L
    return B.add((base + tip) / 2, (w, w * 0.80, L / 2), color or ICE_W, bone, R=bk.frame_from(base, tip, side),
                 top=top, nostud=True, role="limb", rnd=0.10)


def model(k):
    import blockkit as bk
    global CORE, CORE_N, HERO, CAP, BACK
    B = bk.Blocks(k, seed=2501, tier=4, plates=False)
    up = Vector((0, 0, 1))
    # ================= pelvis + waist (Spine): heavy hips, plum side plates, dark belt joint, tapered waist
    B.add((0, 0.04, 0.90), (0.27, 0.21, 0.13), MAUVE, "Spine", bot=(0.78, 0.82), top=(1.0, 1.0), rnd=0.40)  # r2 M2
    B.mirror((0.238, 0.045, 0.905), (0.034, 0.16, 0.10), PLUM, "Spine", rot=(0, 10, 0), bot=(0.8, 0.85),
             rnd=0.45)                                                       # r2 M2: hip plates on the hip, thinner
    B.add((0, 0.03, 1.03), (0.262, 0.19, 0.02), JOINT_D, "Spine", rnd=0.5)              # belt seam (r3 M2: 0.04 -> 0.02)
    B.add((0, 0.02, 1.10), (0.262, 0.19, 0.08), MAUVE, "Spine", bot=(0.95, 0.95), top=(1.08, 1.06), rnd=0.36)
    B.add((0, -0.176, 1.098), (0.16, 0.012, 0.030), ICE_W, "Spine", top=(1.06, 1.0), nostud=True, role="limb",
          rnd=0.30)                                                         # f85 9+ 5: pale belly band
    # ================= chest (Chest): deep stone ribcage leaning forward (inverted triangle), plum back hump
    rib = B.add((0, 0.0, 1.42), (0.38, 0.28, 0.29), MAUVE, "Chest", rot=(10, 0, 0), bot=(0.62, 0.74),
                top=(1.0, 0.92), rnd=0.32)
    B.add((0, 0.05, 1.165), (0.26, 0.20, 0.035), JOINT_D, "Chest", rnd=0.5)                    # chest/waist gap (r2)
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
    BR_OUT, BR_IN, BDEPTH, BPROUD = 0.140, 0.088, 0.06, 0.030          # r2 MUST 1 0.27, review 4 NICE 4: 0.28 BU outer dia
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
    B.poly([brc + brn * (BDEPTH / 2 - 0.010) + (bu * math.cos(a) + bv * math.sin(a)) * 0.066
            for a in [2 * math.pi * (j + 0.5) / 8 for j in range(8)]], 0.016, ICE_W, "Chest")      # ice disc
    BACK = tuple(brc + brn * 0.04)
    # ================= THE HERO: gold chest bezel (12 facets, tilted 10 deg up) around a faceted ice core
    cp, cn = surf_hit(B, [rib], (0, -1.0, 1.40), (0, 1, 0))
    rn = (cn + up * math.tan(math.radians(10))).normalized()           # ring normal: the chest face tilted 10 up
    u = Vector((1, 0, 0))
    v = rn.cross(u).normalized()
    if v.z < 0:
        v = -v
    R_OUT, R_IN, DEPTH, PROUD = 0.272, 0.148, 0.10, 0.045              # f85 9+ 1: outer 0.240 -> 0.272 (0.265 gave 44 px)
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
        p1 = rc + rad * (R_OUT + 0.045) - rn * 0.012                   # f85: shorter settings (bigger ring)
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
    skull = B.add((0, -0.245, 1.86), (0.160, 0.160, 0.135), MAUVE, "Head", top=(0.84, 0.86), rnd=0.30)   # f85 9+ 2
    B.add((0, -0.21, 1.99), (0.122, 0.120, 0.032), PLUM, "Head", top=(0.8, 0.8), rnd=0.42)             # crown cap
    for s in (1, -1):
        B.add((s * 0.148, -0.284, 1.812), (0.048, 0.090, 0.068), MAUVE, "Head", rot=(0, 0, s * 8), rnd=0.42)  # cheek
    fp, fn = surf_hit(B, [skull], (0, -1.0, 1.89), (0, 1, 0))
    # slate brow ridge: two chunky halves (20 deg inner-down) meeting over the nose, set into the forehead
    for s in (1, -1):
        Rb = face_R(fn) @ Euler((0, math.radians(-s * 30), 0), "XYZ").to_matrix()          # r1 MUST 2: slabs
        B.add(fp + fn * 0.010 + Vector((s * 0.070, 0, -0.001)), (0.076, 0.032, 0.028), JOINT_D, "Head", R=Rb,
              role="limb", rnd=0.06, studs=[], nostud=True)
    B.seg(fp + fn * 0.010 + Vector((0, 0, -0.025)), fp + fn * 0.040 + Vector((0, 0, -0.095)), 0.028, 0.024,
          MAUVE, "Head", top=(1.25, 1.0), rnd=0.4)                                                   # nasal ridge
    for s in (1, -1):                                                                               # deep-set eyes
        ep, en = surf_hit(B, [skull], (s * 0.078, -1.0, 1.858), (0, 1, 0))
        ice_eye(B, ep + en * 0.003, s, en, tilt=20, sc=0.95, wx=1.15)
    # jaw: heavy square chin (Jaw bone) jutting forward; the mouth is the dark seam between skull and jaw
    B.add((0, -0.295, 1.732), (0.120, 0.105, 0.046), MAUVE, "Jaw", top=(1.0, 0.95), bot=(0.84, 0.86), rnd=0.34)
    # f85 MUST 3: the visible jaw hangs under the skull (seam z ~1.727); a dark cavity on Head fills the space the
    # jaw front drops away from, and the lip line rides the Jaw at the seam
    B.add((0, -0.335, 1.707), (0.086, 0.040, 0.018), JOINT_D, "Head", studs=[], nostud=True, role="detail",
          rnd=0.2)                                                          # mouth cavity
    B.add((0, -0.399, 1.727), (0.088, 0.008, 0.0045), MOUTH, "Jaw", studs=[], role="detail", bevel=0.002)  # lip
    # ================= arms: shoulder boulder, upper arm, slate elbow, flared forearm under a plum bracer,
    # boulder fist with curled fingers and ice knuckle crusts; two ice-capped pauldrons per shoulder
    for s, side in ((1, "L"), (-1, "R")):
        arm, fore, hand = "Arm_" + side, "Fore_" + side, "Hand_" + side
        Sv, Ev, Wv, Fv = X(SHOULDER, s), X(ELBOW, s), X(WRIST, s), X(FIST, s)
        B.add(Sv + Vector((s * 0.03, 0.0, -0.01)), (0.155, 0.165, 0.150), MAUVE, arm, rnd=0.55)        # deltoid
        B.seg(Sv, Ev, 0.134, 0.144, MAUVE, arm, ext=0.0, ext1=0.03, top=(0.80, 0.80), rnd=0.42)       # upper arm (f85)
        de = (Wv - Ev).normalized()
        B.seg(Ev - de * 0.025, Ev + de * 0.05, 0.120, 0.130, JOINT_D, fore, rnd=0.36)                 # elbow joint
        B.seg(Ev, Wv, 0.140, 0.148, MAUVE, fore, ext=0.02, ext1=0.0, top=(0.82, 0.82), rnd=0.40)      # forearm (f85)
        br = B.seg(Ev + de * 0.11, Wv - de * 0.06, 0.160, 0.168, PLUM, fore, top=(0.80, 0.80), rnd=0.42)  # bracer
        for t_, L, w, lean in ((0.35, 0.075, 0.042, 0.5), (0.70, 0.065, 0.038, 0.8)):                 # ice crusts
            q = (Ev + de * 0.11).lerp(Wv - de * 0.06, t_)
            ice_chunk(B, q + Vector((s * 0.135, 0.02, 0.0)), (s * 1.0, 0.25, lean), L, w, fore)
        B.seg(Wv - de * 0.05, Wv + de * 0.035, 0.130, 0.138, JOINT_D, fore, rnd=0.36)                 # wrist joint
        fist = B.add(Fv, (0.162, 0.162, 0.142), MAUVE, hand, rot=(-14, 0, 0), rnd=0.46)               # fist
        for gx in (-0.090, -0.030, 0.030, 0.090):                                                     # curled fingers
            B.add(fist.world((gx * s, -0.152, -0.030)), (0.027, 0.032, 0.035), MAUVE, hand, R=fist.R, rnd=0.55)
        B.add(fist.world((-s * 0.11, -0.10, 0.035)), (0.048, 0.055, 0.065), PLUM, hand, R=fist.R, rnd=0.42)  # thumb
        for gx, L, tw in ((-0.080, 0.060, 0.040), (0.0, 0.072, 0.044), (0.080, 0.060, 0.040)):        # ice knuckles
            base = fist.world((gx * s, -0.112, 0.112))
            ice_chunk(B, base, fist.R @ Vector((gx * s * 0.8, -0.75, 0.7)), L, tw, hand, top=(0.80, 0.72))
        # ---- pauldron 1 (upper, over the shoulder) + its glacier crust (one slab + 3 broken blocks)
        p1 = B.add(Sv + Vector((s * 0.04, 0.005, 0.17)), (0.188, 0.208, 0.088), MAUVE, arm,
                   rot=(0, s * 18, 0), top=(0.84, 0.86), bot=(0.80, 0.80), rnd=0.55)
        c1 = B.add(p1.world((0, 0, 0.090)), (0.150, 0.170, 0.036), ICE_W, arm, R=p1.R, top=(0.82, 0.84),   # r4 M3
                   nostud=True, role="limb", rnd=0.30)
        for dx, dy, L, w, lean in ((0.05, -0.06, 0.18, 0.070, 0.40), (0.085, 0.085, 0.12, 0.058, 0.70),
                                   (-0.05, 0.05, 0.09, 0.052, -0.15)):                          # f85 9+ 3
            ice_chunk(B, p1.world((s * dx, dy, 0.10)), p1.R @ Vector((s * lean, dy * 0.8, 1.0)), L, w, arm,
                      top=(0.86, 0.80))                                                        # flat tops
        # ---- pauldron 2 (lower, outer, on the upper arm) + its crust
        p2 = B.add(Sv + Vector((s * 0.19, 0.02, -0.03)), (0.090, 0.170, 0.115), MAUVE, arm,
                   rot=(0, s * 42, 0), top=(0.80, 0.84), rnd=0.45)
        B.add(p2.world((0, 0, 0.112)), (0.084, 0.152, 0.035), ICE_W, arm, R=p2.R, top=(0.80, 0.82), nostud=True,   # r4 M3
              role="limb", rnd=0.22)
        ice_chunk(B, p2.world((0.0, -0.04, 0.12)), p2.R @ Vector((s * 0.35, -0.2, 1.0)), 0.10, 0.050, arm,
                  top=(0.86, 0.80))
        if s > 0:
            CAP = tuple(c1.world((0, 0, 0.06)))
    # ================= legs: pillar thighs (plum outer plates) + shins (plum guards), slate knee/ankle joints,
    # blocky feet with 3 slate toes
    for s, side in ((1, "L"), (-1, "R")):
        leg, shin, foot = "Leg_" + side, "Shin_" + side, "Foot_" + side
        H, K, A = X(HIP, s), X(KNEE, s), X(ANKLE, s)
        # r2 MUST 1: ONE tapered tube per leg - thigh 0.182 -> 0.66 at the knee, the shin carries on from the same
        # width down to the ankle; the plum plate, knee cap and shin guard are flush (no steps); one thin ankle band
        TW, TD, TT = 0.182, 0.194, 0.66                       # thigh half-width / half-depth at the hip, knee taper
        SW, SD, ST = TW * TT, TD * TT, 0.84                   # r3 M1: the shin starts AT the thigh's knee width
        H2 = H + Vector((s * 0.02, 0.0, 0.07))                # r2 MUST 2: the thigh top 0.02 further out
        B.seg(H2, K, TW, TD, MAUVE, leg, ext=0.0, ext1=0.02, top=(TT, TT), rnd=0.40)                  # thigh
        f0, f1 = 0.10, 0.80                                   # the plum outer plate rides the thigh surface
        q0, q1 = H2.lerp(K, f0), H2.lerp(K, f1)
        w0, w1 = TW * (1 - (1 - TT) * f0), TW * (1 - (1 - TT) * f1)
        B.seg(q0 + Vector((s * (w0 - 0.012), 0.01, 0)), q1 + Vector((s * (w1 - 0.012), 0.0, 0)), 0.020, 0.125 * (w0 / TW),
              PLUM, leg, top=(1.0, w1 / w0), rnd=0.45)                                                 # thigh plate
        dk = (A - K).normalized()
        B.seg(K - dk * 0.030, K + dk * 0.040, SW * 0.86, SD * 0.86, JOINT_D, shin, rnd=0.45)        # knee joint (inside)
        B.add(K + Vector((0, -(SD - 0.012), 0.0)), (0.088, 0.020, 0.080), PLUM, shin, rnd=0.60)       # knee cap (r3: 0.008 proud)
        B.seg(K, A, SW, SD, MAUVE, shin, ext=0.02, ext1=0.0, top=(ST, ST), rnd=0.42)                  # shin
        g0, g1 = 0.18, 0.82                                   # the plum front guard rides the shin surface
        B.seg(K.lerp(A, g0) + Vector((0, -(SD * (1 - (1 - ST) * g0) - 0.010), 0)),
              A.lerp(K, 1 - g1) + Vector((0, -(SD * (1 - (1 - ST) * g1) - 0.010), 0)), 0.100, 0.018, PLUM, shin,
              top=(0.88, 1.0), rnd=0.45)                                                               # shin guard
        B.seg(A + Vector((0, 0, 0.012)), A + Vector((0, 0, 0.034)), SW * ST + 0.008, SD * ST + 0.008, JOINT_D, shin,
              rnd=0.35)                                                                                # one ankle band
        B.seg(A - Vector((0, 0, 0.005)), A + Vector((0, 0, 0.014)), SW * ST - 0.004, SD * ST - 0.004, JOINT_D, foot,
              rnd=0.35)                                                                                # ankle (inside)
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
    k.joint("Knee_L", X(KNEE, 1) + Vector((0, -0.17, 0.0)), "Shin_L", tail=(0, -0.1, 0))   # r2 MUST 4: kneel on the LEFT


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


# ------------------------------------------------------------------ animation (clips 2026-10-27, refs: ANIM_REFS.md)
# Heavy, slow, upright: the Titan never pounds or presses (the Frostcrown Dragon owns the press). The walk is the
# Plate-27 load walk; the act is the Plate-356 kneel and rise. Feet are IK-planted in every frame of idle / roar / act.
import petkit as pk
import _common as cm

LEGS = ("Leg_L", "Leg_R")


def curve(keys, f):
    """smoothstep through (frame, value) keys"""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            return v0 + (v1 - v0) * u * u * (3 - 2 * u)
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]


def vcurve(keys, f):
    """curve() for (frame, Vector) keys"""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            return Vector(v0).lerp(Vector(v1), u * u * (3 - 2 * u))
    return Vector(keys[-1][1] if f > keys[-1][0] else keys[0][1])


def sn(f, n, ph=0.0, cyc=1):
    return math.sin(2 * math.pi * (cyc * f / n + ph))


def ankle_to(k, leg, f, A, toe=0.0, yaw=0.0):
    """IK: put the ankle of `leg` at world point A; toe = foot pitch (deg, + = toes down); yaw = foot turn about Z
    (deg, + = toes toward +x)"""
    from mathutils import Quaternion
    foot = k.legs2[leg]["foot"]
    hipR, ankR = k.J[leg], k.J[foot]
    k.solve_leg(leg, f, Vector((A.x - (ankR.x - hipR.x), A.y - (ankR.y - hipR.y), A.z - ankR.z)), toe=toe)
    if yaw:
        k._aim(foot, f, Quaternion((0, 0, 1), math.radians(yaw)) @ Quaternion((1, 0, 0), math.radians(toe)))


def arms_fk(k, f, out=0.0, fwd=0.0, bend=0.0):
    """FK arms: out + = the arm swings away from the body, fwd + = swings forward, bend + = the elbow flexes"""
    for s, side in ((1, "L"), (-1, "R")):
        k.key("Arm_" + side, f, rot=(-fwd, 0, -s * out))
        k.key("Fore_" + side, f, rot=(-bend, 0, 0))
        k.key("Hand_" + side, f, rot=(0, 0, 0))


def idle(k):
    """WEIGHT SHIFT (plan, f85 MUST 5): hip yaw +/-4 deg over one cycle, two breaths (chest 2 deg, the body sinks
    0.015), the shoulders (pauldrons) settle 2 deg at f30 and f70, a slow +/-8 deg fist flex (60 f, the fists offset),
    core pulses f40 / f100. No head tilt (the head stays level and forward). Feet planted."""
    n = 120
    k.new_action("idle", n, True)
    settle = [(0, 0), (26, 0), (30, 2), (42, 0), (66, 0), (70, 2), (82, 0), (120, 0)]
    for f in range(0, n + 1, 2):
        yaw = 6 * sn(f, n)                                                   # r2 MUST 5: 4 -> 6 deg
        br = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0, yaw, 0), loc=(0, 0, -0.015 * br))         # breath sink 0.005 -> 0.015
        k.key("Chest", f, rot=(-1.8 * br, -0.75 * yaw, 0))                  # r3: breath 2.0 -> 1.8 (chest vs spine margin)
        k.key("Head", f, rot=(1.8 * br, -0.25 * yaw, 0))                    # the head stays level and forward
        k.key("Jaw", f, rot=(0, 0, 0))
        arms_fk(k, f, out=curve(settle, f), bend=2.0 * br)
        sway = 2.5 * sn(f, n)                                                # r3 M5: the shoulders turn with the hips -
        for s_, side in ((1, "L"), (-1, "R")):                               # opposite fwd / back arm swing on the
            k.key("Arm_" + side, f, rot=(-s_ * sway, 0, -s_ * curve(settle, f)))   # hip-yaw sine (the chest counter
                                                                             # does not cancel it)
        for s, side in ((1, "L"), (-1, "R")):                             # f85: slow +/-8 deg fist flex
            k.key("Hand_" + side, f, rot=(8 * sn(f, 60, 0.25 if s > 0 else 0.0), 0, 0))
    cm.plant(k, n, legs=LEGS)
    k.finish()
    k.meta["planted"] = list(LEGS)
    k.events["idle"] = {"frost1": round(30 / n, 3), "core1": round(40 / n, 3), "frost2": round(70 / n, 3),
                        "core2": round(100 / n, 3)}


def walk(k):
    """HEAVY LOAD WALK (Plate 27, W1-W5): flat-foot contacts, the body sinks just after each contact and rises at
    passing, low swing foot, upright torso, the weight rolls over the stance foot, arms swing only 4 deg."""
    n = 48
    half = n // 2
    dip = [(0, -0.012), (5, -0.035), (14, 0.004), (24, -0.012)]

    def body(f):
        t = f % half
        k.key("Spine", f, rot=(0.6, 3 * sn(f, n, 0.0), 2 * sn(f, n, 0.0)),
              loc=(0.022 * sn(f, n, 0.15), 0, curve(dip, t)))
        k.key("Chest", f, rot=(0, -2 * sn(f, n, 0.0), -1.5 * sn(f, n, 0.0)))
        k.key("Head", f, rot=(-0.6 - 0.8 * sn(f, n, 0.3, 2), -1 * sn(f, n, 0.0), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        for s, side in ((1, "L"), (-1, "R")):
            k.key("Arm_" + side, f, rot=(5.5 * s * sn(f, n, 0.0), 0, 0))         # opposite the same-side leg (r3: 4 -> 5.5)
            k.key("Fore_" + side, f, rot=(-3 - 2 * s * sn(f, n, 0.05), 0, 0))
            k.key("Hand_" + side, f, rot=(0, 0, 0))
    orig = k.solve_leg
    k.solve_leg = lambda leg, f, T, foot_z=0.0, toe=None: orig(leg, f, T, foot_z,
                                                               toe=10.0 * min(1.0, max(0.0, T.z) / 0.07))
    try:
        stride = cm.biped_walk(k, n, 0.20, 0.07, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.62)
    finally:
        del k.solve_leg
    return stride


def roar(k):
    """CORE BELLOW (plan; refs #3 + #9; f85 MUST 4): lean in and tuck (anticipation), then the body pushes forward
    (Spine -4, Chest -3 local = -7 world), the head lifts 15 deg and the arms go out 22 deg (24 at f34); the jaw opens
    late (24 deg at f27); the core pulses f22 / f34; hold to f50; a slower settle."""
    n = 66
    k.new_action("roar", n, False)
    K = [  # f, spine z, spine pitch, chest pitch, head pitch, jaw, arms out
        (0, 0.0, 0, 0, 0, 0, 0),
        (10, -0.012, 1, 3, 4, 0, -2),
        (22, 0.010, -4, -3, -15, 12, 22),                                    # f85 MUST 4 (jaw 16 -> 24: the gap shows)
        (27, 0.010, -4, -3, -15, 24, 22),
        (34, 0.014, -4, -3, -15, 22, 24),
        (50, 0.010, -3.5, -3, -14, 20, 22),
        (58, 0.0, -1, -1, -4, 6, 10),
        (66, 0.0, 0, 0, 0, 0, 0)]
    for f, z, sp, ch, hd, jw, ao in K:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        arms_fk(k, f, out=ao, bend=max(0.0, ao) * 0.6)
    cm.plant(k, n, legs=LEGS)
    k.finish(loop=False)
    k.events["roar"] = {"core1": round(22 / n, 3), "glint": round(22 / n, 3), "icedust": round(24 / n, 3),
                        "core2": round(34 / n, 3)}


DROP = 0.318         # pelvis drop of the kneel (left knee cap on the snow; r3: 0.312 -> 0.318 with the 0.008-proud cap; r2 0.272 -> 0.312)
SETTLE = 0.005      # r3 polish (was 0.008): the 3-frame settle after the knee lands (ref K8a)
# r4 (review 3 MUST 1): the kneel reads from the front / 3-4 / behind - the Spine rolls toward the kneeling (right)
# side, the Chest and Head counter-roll (chest vs spine <= 5 deg, head level)
# r2 MUST 4: MIRRORED - the LEFT knee goes down (the camera side), the RIGHT foot steps forward; rolls flip sign
ROLL_S = [(0, 0), (8, 0), (18, 9), (50, 9), (62, 4), (76, 0), (100, 0)]           # r3 M4: 7 -> 9 in the hold
ROLL_C = [(0, 0), (8, 0), (18, -3.5), (50, -3.5), (62, -2), (76, 0), (100, 0)]
ROLL_H = [(0, 0), (8, 0), (18, -5.5), (50, -5.5), (62, -2), (76, 0), (100, 0)]     # r3: the head stays level
STEP_R = Vector((-0.04, -0.30, 0.0))  # the right foot steps forward 0.30 and 0.04 out


def act_kneelrise(k):
    """KNEEL AND RISE (plan; Plate 356 K1-K4 + #9; final 8.5 r2 MIRRORED): the right foot steps forward, the body drops
    straight down and the LEFT knee lands (ice crack, `Knee_L`), the left toes tuck and turn out, the head bows 12 deg,
    the right fist rests on the raised right knee and the left fist on the left thigh;
    the kneel holds while the core pulses twice; the rise starts with a forward lean, then the front leg drives up,
    the right foot comes through and the left foot steps back; exact rest."""
    import bpy
    n = 100
    k.new_action("act_kneelrise", n, False)
    SP = [  # f, x, y, z, spine pitch, chest pitch, head pitch
        (0, 0.0, 0.0, 0.0, 0, 0, 0), (6, 0.03, 0.0, -0.01, 0, 0, 0),
        (18, 0.0, -0.04, -DROP, 4, 2, 12), (20, 0.0, -0.04, -DROP - SETTLE, 4, 2.5, 13), (23, 0.0, -0.04, -DROP, 4, 2, 12),
        (34, 0.0, -0.04, -DROP + 0.006, 4, 2, 12),
        (50, 0.0, -0.04, -DROP, 4, 2, 12),
        (58, 0.0, -0.09, -DROP + 0.01, 10, 4, 6), (70, 0.0, -0.05, -0.12, 6, 2, 3), (80, 0.0, -0.01, -0.02, 1, 0, 0),
        (84, 0.0, 0.0, 0.0, 0, 0, 0), (100, 0.0, 0.0, 0.0, 0, 0, 0)]
    # asymmetric hold (r2 MUST 4, r3 M3): the RIGHT fist rests forward on the raised right knee; the LEFT fist rests on
    # the top of the left (kneeling) thigh, above the knee, so the knee stays visible from the front / 3-4
    # (f, out, fwd, bend)
    ARM_R = [(0, 0, 0, 0), (18, 4, 18, 26), (30, 4, 20, 32), (50, 4, 20, 32), (62, 2, 8, 8), (80, 0, 0, 0), (100, 0, 0, 0)]
    # r3 M3: the review's (6, 22, 60) lifted the fist to z 1.04 (above the chest line). Probe sweep (_scratch/fist_probe.py,
    # surface distance + collide_where): closer than ~0.09 the thick forearm / bracer cuts into the thigh top, so the
    # hold is (-11, 14, 14): fist 0.094 from the thigh surface, fist centre z 0.51 (chest line 0.83), no collision
    ARM_L = [(0, 0, 0, 0), (18, -4, 12, 24), (30, -11, 14, 14), (46, -11, 14, 14), (53, 4, 8, 24), (62, 5, 4, 14), (80, 0, 0, 0),
             (100, 0, 0, 0)]                                     # f46-53: the arm comes off the thigh before the lean
    for f in range(0, n + 1, 2):
        x = curve([(a[0], a[1]) for a in SP], f)
        y = curve([(a[0], a[2]) for a in SP], f)
        z = curve([(a[0], a[3]) for a in SP], f)
        k.key("Spine", f, rot=(curve([(a[0], a[4]) for a in SP], f), 0, curve(ROLL_S, f)), loc=(x, y, z))
        k.key("Chest", f, rot=(curve([(a[0], a[5]) for a in SP], f), 0, curve(ROLL_C, f)))
        k.key("Head", f, rot=(curve([(a[0], a[6]) for a in SP], f), 0, curve(ROLL_H, f)))
        k.key("Jaw", f, rot=(0, 0, 0))
        for sgn, side, T in ((1, "L", ARM_L), (-1, "R", ARM_R)):
            k.key("Arm_" + side, f, rot=(-curve([(a[0], a[2]) for a in T], f), 0, -sgn * curve([(a[0], a[1]) for a in T], f)))
            k.key("Fore_" + side, f, rot=(-curve([(a[0], a[3]) for a in T], f), 0, 0))
            k.key("Hand_" + side, f, rot=(0, 0, 0))
    k.bake_bezier_now()
    aL, aR = k.J["Foot_L"].copy(), k.J["Foot_R"].copy()
    # r2 MUST 4 (mirrored): the RIGHT foot steps forward and back; the LEFT knee goes down, its foot tucks + turns out
    R = [(0, aR), (2, aR), (5, aR + STEP_R * 0.5 + Vector((0, 0, 0.06))), (9, aR + STEP_R),
         (70, aR + STEP_R), (74, aR + STEP_R * 0.5 + Vector((0, 0, 0.05))), (79, aR), (100, aR)]
    L = [(0, aL), (6, aL), (11, aL + Vector((0, 0.18, 0.10))), (15, aL + Vector((0, 0.31, 0.16))), (18, aL + Vector((0, 0.34, 0.155))),
         (52, aL + Vector((0, 0.34, 0.155))), (62, aL + Vector((0, 0.24, 0.11))), (70, aL + Vector((0, 0.08, 0.07))),
         (76, aL), (100, aL)]
    TL = [(0, 0), (6, 0), (18, 26), (52, 26), (62, 18), (70, 6), (76, 0), (100, 0)]
    YL = [(0, 0), (10, 0), (18, 10), (50, 10), (62, 4), (72, 0), (100, 0)]      # the left foot turns 10 deg out
    TR = [(0, 0), (2, 0), (5, 8), (9, 0), (70, 0), (74, 8), (79, 0), (100, 0)]
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        ankle_to(k, "Leg_R", f, vcurve(R, f), toe=curve(TR, f))
        ankle_to(k, "Leg_L", f, vcurve(L, f), toe=curve(TL, f), yaw=curve(YL, f))
    k.finish(loop=False)
    k.events["act_kneelrise"] = {"icecrack": round(18 / n, 3), "core1": round(30 / n, 3), "core2": round(44 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    act_kneelrise(k)
    return stride
