# Permafrost Titan (Glacier egg SECRET 2.5 %, 2026-10-27) - plan _review/PermafrostTitan_plan.md v2, hero = OPTION A
# (owner decision): THE GOLD CHEST BEZEL. An upright mauve-stone ice giant in the FIERCE studded style: rounded studded
# stone masses split by dark slate joints, two rounded pauldrons per shoulder capped with white glacier ice, long arms
# ending in boulder fists with white ice knuckle crusts, pillar legs on blocky three-toed feet, a small bare head sunk
# between the shoulders (heavy slate brow, white ice slit eyes, black slit pupils, flat closed mouth) and THE HERO: a
# 12-facet house-gold bezel ring (gold-dark inner lining) set into the chest around a faceted ice-white core.
# No spikes, no crown, no cyan, no glow (the core pulse / frost drift / ice dust are Studio VFX on the anchor bones).
import math
from mathutils import Vector, Matrix, Euler

DISPLAY = "Permafrost Titan"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 10.0                # studs to the top of the head (option A: no head piece) - equal to Thunder Rex

# Blender colours (Roblox renders ~0.6x darker)
MAUVE = (184, 150, 200)      # body: stone masses, pauldron bodies, head, limbs (studded)
MAUVE_D = (150, 118, 170)    # shadowed stone (back plates, inner faces) - same family, one step darker
ICE_W = (226, 240, 250)      # pauldron caps, chest core, knuckle crusts, eye slits (smooth)
JOINT_D = (52, 60, 84)       # joints, gaps, brow ridge, eye sockets, toe blocks
GOLD = (255, 196, 50)        # THE hero: the chest bezel ring only
GOLD_D = (214, 150, 30)      # the bezel's inner lining
BLACK = (14, 14, 22)         # pupils, claws
MOUTH = (86, 18, 30)         # mouth slit

H_MODEL = 2.00               # head top in Blender units
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

HIP, KNEE, ANKLE = (0.215, 0.03, 0.95), (0.235, -0.04, 0.55), (0.235, 0.02, 0.175)
SHOULDER, ELBOW, WRIST = (0.47, 0.02, 1.60), (0.60, 0.07, 1.19), (0.635, -0.03, 0.84)
FIST = (0.635, -0.05, 0.70)
THROAT = (0.0, -0.08, 1.70)
CORE = (0, -0.30, 1.45)       # filled in by model(): chest core centre on the chest face (VFX anchor)
CORE_N = (0, -1, 0)
HERO = (0, -0.32, 1.67)       # filled in by model(): bezel top (glint anchor)
CAP = (0.53, 0.0, 1.88)       # filled in by model(): upper pauldron ice cap top (left)


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
    """slate socket (inner corner down) -> ice-white slit -> black slit pupil at the inner end, heavy slate V-brow"""
    R = face_R(n) @ Euler((0, math.radians(-s * tilt), 0), "XYZ").to_matrix()
    nn = Vector(n).normalized()
    c = Vector(c)
    kw = dict(R=R, studs=[], role="detail")
    B.add(c, (0.062 * sc, 0.008, 0.030 * sc), JOINT_D, bone, bevel=0.005, **kw)                    # socket
    B.add(c + nn * 0.006, (0.052 * sc, 0.006, 0.017 * sc), ICE_W, bone, bevel=0.004, **kw)         # ice slit
    B.add(c + nn * 0.011 + R @ Vector((-s * 0.012 * sc, 0, 0)), (0.007 * sc, 0.004, 0.016 * sc), BLACK, bone,
          bevel=0.002, **kw)                                                                     # slit pupil
    Rb = face_R(n) @ Euler((0, math.radians(-s * 22), 0), "XYZ").to_matrix()
    B.add(c + nn * 0.026 + Vector((0, 0, 0.040 * sc)), (0.080 * sc, 0.034, 0.026 * sc), JOINT_D, bone, R=Rb,
          role="detail", bevel=0.011)                                                            # heavy V-brow


def ice_chunk(B, base, d, L, w, bone, side=(1, 0, 0)):
    """blunt glacier ice chunk (no point): a short tapered faceted block standing on `base` along d"""
    import blockkit as bk
    base, d = Vector(base), Vector(d).normalized()
    tip = base + d * L
    return B.add((base + tip) / 2, (w, w * 0.85, L / 2), ICE_W, bone, R=bk.frame_from(base, tip, side),
                 top=(0.55, 0.50), nostud=True, role="limb", rnd=0.25)


def model(k):
    import blockkit as bk
    global CORE, CORE_N, HERO, CAP
    B = bk.Blocks(k, seed=2501, tier=4, plates=False)
    up = Vector((0, 0, 1))
    # ================= pelvis + waist (Spine): heavy hips, dark belt joint, tapered waist
    hips = B.add((0, 0.03, 0.985), (0.29, 0.20, 0.125), MAUVE, "Spine", bot=(0.80, 0.82), top=(1.0, 1.0), rnd=0.36)
    B.add((0, 0.02, 1.115), (0.255, 0.18, 0.04), JOINT_D, "Spine", rnd=0.4)                          # belt joint
    waist = B.add((0, 0.0, 1.19), (0.25, 0.175, 0.09), MAUVE, "Spine", bot=(0.95, 0.95), top=(1.08, 1.06),
                  rnd=0.36)
    # front tasset: a dark-edged stone plate hanging over the hip front
    B.add((0, -0.185, 0.93), (0.15, 0.035, 0.10), MAUVE_D, "Spine", rot=(-8, 0, 0), bot=(0.8, 1), rnd=0.3)
    # ================= chest (Chest): wide stone ribcage (inverted triangle), pecs, trapezius hump behind the head
    rib = B.add((0, -0.01, 1.48), (0.37, 0.25, 0.285), MAUVE, "Chest", rot=(5, 0, 0), bot=(0.68, 0.76),
                top=(1.0, 0.94), rnd=0.32)
    B.add((0, 0.035, 1.255), (0.27, 0.19, 0.035), JOINT_D, "Chest", rnd=0.4)                         # chest/waist gap
    trap = B.add((0, 0.12, 1.715), (0.27, 0.16, 0.10), MAUVE, "Chest", rot=(-10, 0, 0), top=(0.62, 0.70),
                 rnd=0.42)
    # back: two dark-gapped stone slabs on the upper back (the game camera sees the back)
    for z0, z1, w in ((1.70, 1.50, 0.25), (1.46, 1.27, 0.21)):
        a, na = surf_hit(B, [rib], (0, 1.0, z0), (0, -1, 0))
        b, nb = surf_hit(B, [rib], (0, 1.0, z1), (0, -1, 0))
        n = (na + nb).normalized()
        B.add((a + b) / 2 + n * 0.012, (0.03, w, (a - b).length / 2), MAUVE_D, "Chest",
              R=bk.frame_from(b, a, n), top=(1, 0.9), rnd=0.40)
        g = b - (a - b).normalized() * 0.02 + n * 0.006
        B.add(g, (0.012, w * 0.80, 0.022), JOINT_D, "Chest", R=bk.frame_from(b, a, n), studs=[], role="detail",
              bevel=0.004)
    # ================= THE HERO: gold chest bezel (12 facets, tilted 10 deg up) around a faceted ice core
    cp, cn = surf_hit(B, [rib], (0, -1.0, 1.455), (0, 1, 0))
    rn = (cn + up * math.tan(math.radians(10))).normalized()           # ring normal: the chest face tilted 10 up
    u = Vector((1, 0, 0))
    v = rn.cross(u).normalized()
    if v.z < 0:
        v = -v
    R_OUT, R_IN, DEPTH, PROUD = 0.225, 0.155, 0.10, 0.045
    rc = cp + rn * (PROUD - DEPTH / 2)                                 # ring centre plane (half sunk in the chest)
    CORE, CORE_N = tuple(cp + rn * 0.02), tuple(rn)
    rm = (R_OUT + R_IN) / 2
    for i in range(12):
        a0, a1 = 2 * math.pi * i / 12, 2 * math.pi * (i + 1) / 12
        p0 = rc + (u * math.cos(a0) + v * math.sin(a0)) * rm
        p1 = rc + (u * math.cos(a1) + v * math.sin(a1)) * rm
        am = (a0 + a1) / 2
        rad = u * math.cos(am) + v * math.sin(am)
        B.seg(p0, p1, (R_OUT - R_IN) / 2, DEPTH / 2, GOLD, "Chest", side=rad, ext=0.012, ext1=0.012,
              studs=[], nostud=True, role="limb", rnd=0.22)
        q0 = rc + (u * math.cos(a0) + v * math.sin(a0)) * (R_IN - 0.004) + rn * 0.006
        q1 = rc + (u * math.cos(a1) + v * math.sin(a1)) * (R_IN - 0.004) + rn * 0.006
        B.seg(q0, q1, 0.014, DEPTH / 2 - 0.012, GOLD_D, "Chest", side=rad, ext=0.006, ext1=0.006, studs=[],
              nostud=True, role="detail", bevel=0.004)
    # four gold settings clamping the ring to the chest (diagonals), low and blunt (no spikes)
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        rad = u * math.cos(a) + v * math.sin(a)
        p0 = rc + rad * (R_OUT - 0.01) + rn * 0.01
        p1 = rc + rad * (R_OUT + 0.055) - rn * 0.012
        B.seg(p0, p1, 0.030, 0.022, GOLD, "Chest", side=rn.cross(rad), studs=[], nostud=True, role="limb",
              top=(0.8, 0.6), rnd=0.3)
    HERO = tuple(rc + v * R_OUT + rn * 0.06)
    # the faceted ice core: octagon disc -> raised diamond -> raised centre facet (all ice-white, smooth)
    Rc = face_R(rn, up=v)
    for rot, hs, dz in ((0, 0.150, 0.000), (45, 0.150, 0.000), (45, 0.105, 0.018), (0, 0.062, 0.032)):
        Rr = Rc @ Euler((0, math.radians(rot), 0), "XYZ").to_matrix()
        B.add(rc + rn * (DEPTH / 2 - 0.01 + dz), (hs, 0.018, hs), ICE_W, "Chest", R=Rr, studs=[], nostud=True,
              role="limb", rnd=0.18)
    # pecs: two rounded stone plates above-outside the ring
    for s in (1, -1):
        pp, pn = surf_hit(B, [rib], (s * 0.255, -1.0, 1.63), (0, 1, 0))
        B.add(pp + pn * 0.03, (0.105, 0.04, 0.085), MAUVE, "Chest", R=face_R(pn) @ Euler(
            (0, math.radians(-s * 12), 0), "XYZ").to_matrix(), rnd=0.42, top=(0.9, 1.0))
        lp, ln = surf_hit(B, [rib], (s * 0.27, -1.0, 1.30), (0, 1, 0))
        B.add(lp + ln * 0.02, (0.075, 0.03, 0.065), MAUVE_D, "Chest", R=face_R(ln) @ Euler(
            (0, math.radians(s * 10), 0), "XYZ").to_matrix(), rnd=0.42)                            # lower rib plates
    # ================= neck + head (throat pivot): dark neck joint, small skull sunk between the pauldrons
    B.seg((0, 0.0, 1.62), (0, -0.12, 1.78), 0.115, 0.10, JOINT_D, "Head", ext=0.02, rnd=0.4)          # neck joint
    skull = B.add((0, -0.185, 1.875), (0.140, 0.140, 0.120), MAUVE, "Head", top=(0.84, 0.86), bot=(1.0, 1.0),
                  rnd=0.30)
    B.add((0, -0.14, 1.985), (0.11, 0.10, 0.025), MAUVE_D, "Head", top=(0.8, 0.8), rnd=0.4)            # crown cap
    for s in (1, -1):
        B.add((s * 0.128, -0.24, 1.82), (0.045, 0.085, 0.07), MAUVE, "Head", rot=(0, 0, s * 8), rnd=0.42)  # cheek
    B.seg((0, -0.27, 1.90), (0, -0.335, 1.80), 0.045, 0.03, MAUVE, "Head", top=(0.85, 1.0), rnd=0.4)  # nose ridge
    # jaw: heavy square chin (Jaw bone), mouth slit along its top
    B.add((0, -0.235, 1.755), (0.118, 0.11, 0.052), MAUVE, "Jaw", top=(1.0, 0.95), bot=(0.86, 0.88), rnd=0.34)
    B.add((0, -0.338, 1.792), (0.075, 0.008, 0.009), MOUTH, "Head", studs=[], role="detail", bevel=0.003)
    # eyes on the face plane under the brow
    for s in (1, -1):
        ep, en = surf_hit(B, [skull], (s * 0.07, -1.0, 1.885), (0, 1, 0))
        ice_eye(B, ep + en * 0.004, s, en, tilt=20, sc=1.0)
    # ================= arms: shoulder boulder, upper arm, slate elbow, flared forearm with a dark bracer,
    # boulder fist with curled finger blocks and ice knuckle crusts
    for s, side in ((1, "L"), (-1, "R")):
        arm, fore, hand = "Arm_" + side, "Fore_" + side, "Hand_" + side
        Sv, Ev, Wv, Fv = X(SHOULDER, s), X(ELBOW, s), X(WRIST, s), X(FIST, s)
        B.add(Sv + Vector((s * 0.03, 0.0, -0.01)), (0.155, 0.165, 0.15), MAUVE, arm, rnd=0.45)        # deltoid
        B.seg(Sv, Ev, 0.125, 0.135, MAUVE, arm, ext=0.0, ext1=0.03, top=(0.86, 0.86), rnd=0.38)       # upper arm
        de = (Wv - Ev).normalized()
        B.seg(Ev - de * 0.02, Ev + de * 0.05, 0.118, 0.128, JOINT_D, fore, rnd=0.35)                  # elbow joint
        B.seg(Ev, Wv, 0.13, 0.14, MAUVE, fore, ext=0.02, ext1=0.0, top=(1.14, 1.10), rnd=0.36)        # forearm
        B.seg(Wv - de * 0.16, Wv - de * 0.07, 0.152, 0.160, MAUVE_D, fore, rnd=0.32)                  # bracer
        B.seg(Wv - de * 0.05, Wv + de * 0.03, 0.128, 0.138, JOINT_D, fore, rnd=0.35)                  # wrist joint
        B.add(Fv, (0.150, 0.150, 0.135), MAUVE, hand, rnd=0.36)                                       # fist
        for i, gx in enumerate((-0.085, -0.028, 0.028, 0.085)):                                       # curled fingers
            B.add(Fv + Vector((gx * s, -0.145, -0.045)), (0.030, 0.035, 0.055), JOINT_D, hand, rnd=0.42,
                  role="detail")
        B.add(Fv + Vector((-s * 0.10, -0.10, 0.04)), (0.045, 0.05, 0.06), MAUVE_D, hand, rnd=0.42)    # thumb
        for gx, L in ((-0.075, 0.10), (0.0, 0.12), (0.075, 0.10)):                                    # ice knuckles
            base = Fv + Vector((gx * s, -0.115, 0.075))
            ice_chunk(B, base, (gx * s * 0.6, -0.8, 0.6), L, 0.034, hand)
        # ---- two rounded studded pauldrons per side, each capped with glacier ice
        p1 = B.add(Sv + Vector((s * 0.035, 0.0, 0.165)), (0.185, 0.20, 0.085), MAUVE, arm,
                   rot=(0, s * 16, 0), top=(0.84, 0.86), rnd=0.45)
        c1 = B.add(p1.world((0, 0, 0.095)), (0.135, 0.150, 0.045), ICE_W, arm, R=p1.R, top=(0.70, 0.72),
                   nostud=True, role="limb", rnd=0.40)
        for dx, dy, L in ((0.0, -0.06, 0.08), (0.06, 0.05, 0.065), (-0.06, 0.04, 0.06)):
            ice_chunk(B, p1.world((s * dx, dy, 0.12)), p1.R @ Vector((s * dx, dy * 0.6, 1.0)), L, 0.04, arm)
        p2 = B.add(Sv + Vector((s * 0.175, 0.0, 0.0)), (0.10, 0.175, 0.125), MAUVE, arm,
                   rot=(0, s * 38, 0), top=(0.80, 0.84), rnd=0.45)
        B.add(p2.world((0, 0, 0.115)), (0.07, 0.13, 0.04), ICE_W, arm, R=p2.R, top=(0.70, 0.72), nostud=True,
              role="limb", rnd=0.40)
        ice_chunk(B, p2.world((s * 0.0, -0.03, 0.14)), p2.R @ Vector((0, -0.1, 1.0)), 0.06, 0.035, arm)
        if s > 0:
            CAP = tuple(c1.world((0, 0, 0.06)))
    # ================= legs: pillar thighs + shins (flared), slate knee/ankle joints, blocky feet + 3 slate toes
    for s, side in ((1, "L"), (-1, "R")):
        leg, shin, foot = "Leg_" + side, "Shin_" + side, "Foot_" + side
        H, K, A = X(HIP, s), X(KNEE, s), X(ANKLE, s)
        B.seg(H + Vector((0, 0.0, 0.07)), K, 0.160, 0.175, MAUVE, leg, ext=0.0, ext1=0.02, top=(0.86, 0.84),
              rnd=0.40)                                                                                # thigh
        dk = (A - K).normalized()
        B.seg(K - dk * 0.035, K + dk * 0.05, 0.135, 0.148, JOINT_D, shin, rnd=0.38)                    # knee joint
        B.add(K + Vector((0, -0.14, 0.01)), (0.095, 0.05, 0.085), MAUVE_D, shin, rnd=0.42)            # knee cap
        B.seg(K, A, 0.140, 0.150, MAUVE, shin, ext=0.0, ext1=0.0, top=(1.14, 1.12), rnd=0.38)          # pillar shin
        B.seg(A - Vector((0, 0, 0.005)), A + Vector((0, 0, 0.045)), 0.150, 0.160, JOINT_D, foot, rnd=0.35)  # ankle
        F = Vector((A.x, A.y - 0.06, 0.075))
        B.add(F, (0.170, 0.215, 0.075), MAUVE, foot, top=(0.86, 0.84), rnd=0.36)                       # foot
        for gx in (-0.105, 0.0, 0.105):                                                                 # 3 toes
            B.add(Vector((A.x + gx, A.y - 0.285, 0.048)), (0.046, 0.055, 0.048), JOINT_D, foot, rnd=0.40)
            B.spike(Vector((A.x + gx, A.y - 0.335, 0.03)), (0, -1, -0.45), 0.04, 0.02, BLACK, foot)
    B.build()
    bk.stud_skin(k, PITCH)
    mn, mx = k.bounds()
    return {"TH": round(B.th, 3), "PITCH": PITCH, "H": round(mx.z, 3), "lowest": round(mn.z, 3),
            "size": [round(v, 3) for v in (mx - mn)], "CORE": [round(v, 3) for v in CORE],
            "HERO": [round(v, 3) for v in HERO]}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.02, 1.00), "Root", tail=(0, 0, 0.25))
    k.joint("Chest", (0, 0.0, 1.24), "Spine", tail=(0, -0.05, 0.40))
    k.joint("Head", THROAT, "Chest", tail=(0, -0.2, 0.18))                   # throat pivot
    k.joint("Jaw", (0, -0.13, 1.79), "Head", tail=(0, -0.2, -0.02))
    k.joint("Core", CORE, "Chest", tail=tuple(Vector(CORE_N) * 0.15))
    k.joint("Hero", HERO, "Chest", tail=(0, -0.1, 0.1))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Arm_" + side, X(SHOULDER, s), "Chest")
        k.joint("Fore_" + side, X(ELBOW, s), "Arm_" + side)
        k.joint("Hand_" + side, X(WRIST, s), "Fore_" + side, tail=(0, -0.05, -0.25))
        k.add_leg2("Arm_" + side, "Fore_" + side, "Hand_" + side, knee=(s * 0.3, 1.0, 0))      # elbows bend back
        k.joint("Pauldron_" + side, X(CAP, s), "Arm_" + side, tail=(0, 0, 0.12))
        k.joint("Fist_" + side, X(FIST, s) + Vector((0, -0.16, 0.06)), "Hand_" + side, tail=(0, -0.1, 0))
        k.joint("Leg_" + side, X(HIP, s), "Spine")
        k.joint("Shin_" + side, X(KNEE, s), "Leg_" + side)
        k.joint("Foot_" + side, X(ANKLE, s), "Shin_" + side, tail=(0, -0.2, -0.1))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
    k.joint("Knee_R", X(KNEE, -1) + Vector((0, -0.19, 0.0)), "Shin_R", tail=(0, -0.1, 0))


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
    out = [((0, -0.04, 1.66), (0, -0.10, 1.74), 0.13, "Head")]
    for s, side in ((1, "L"), (-1, "R")):
        out.append((X(WRIST, s), X(WRIST, s), 0.15, "Hand_" + side))
        out.append((X(ELBOW, s), X(ELBOW, s), 0.15, "Fore_" + side))
        out.append((X(KNEE, s), X(KNEE, s), 0.16, "Shin_" + side))
        out.append((X(ANKLE, s), X(ANKLE, s), 0.16, "Foot_" + side))
        out.append((X(HIP, s), X(HIP, s), 0.20, "Leg_" + side))
    return out


HEAD_XF = []
