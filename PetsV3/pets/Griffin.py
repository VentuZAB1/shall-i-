# Griffin (Celestial egg #2) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the gold guardian"): a golden-eagle griffin
# built from tapered blocks and covered in Roblox studs (blockkit.stud_skin): a dark-brown eagle front (deep chest,
# shingle-feather neck ruff, golden nape, a fierce eagle head with a heavy brow ridge over narrow yellow eyes, a big
# hooked yellow beak, swept ear tufts), eagle forelegs (feathered trousers, scaly yellow shanks, 4 black talons), golden
# lion hindquarters with a rising belly line, a lion tail with a dark tuft, and huge 3-row feather wings (light coverts
# -> mid secondaries -> dark primaries) built with wing3 rules (root-axis flap, hinge fold).
# Old chibi version: _tools/chibi_specs/Griffin.py
import math
from mathutils import Vector, Euler, Matrix
import wing3

DISPLAY = "Griffin"
MOTION = "Fly"
RIG = "wingquad"
HEIGHT = 9.0

BODY = (150, 100, 68)         # golden-eagle brown (Roblox renders ~0.6x darker)
NAPE = (222, 158, 72)         # golden nape, crown, ear tufts
BROW = (84, 56, 40)           # dark brow ridges (V over the beak root)
LION = (206, 146, 78)         # lion hindquarters
UNDER = (236, 206, 160)       # lion belly, chest ruff tips
COVERT = (164, 112, 74)       # wing rows: 3 clear value steps
SECOND = (128, 86, 60)
PRIMARY = (98, 66, 50)
YELLOW = (255, 200, 40)       # accent: beak, cere, shanks, feet, eyes
YELLOW_D = (226, 160, 30)     # scale bands
EYE = (255, 200, 40)
EYE_HOT = (255, 240, 170)
TUFT = (90, 52, 36)           # tail tuft
BEAK_D = (62, 56, 70)         # dark hooked beak tip
BLACK = (14, 14, 22)
MOUTH = (96, 26, 30)

PITCH = 0.045

# leg joints (left side): H shoulder/hip, K elbow(ankle)/stifle, A foot/hock, P foot centre
LEGS = {"F": ((0.15, -0.40, 0.72), (0.15, -0.31, 0.42), (0.15, -0.38, 0.12), (0.15, -0.42, 0.045)),
        "B": ((0.125, 0.44, 0.78), (0.125, 0.31, 0.48), (0.125, 0.54, 0.22), (0.125, 0.47, 0.045))}
HC = Vector((0, -0.84, 1.26))                     # cranium centre
TAILP = [(0, 0.62, 0.90), (0, 0.82, 0.74), (0, 0.96, 0.46), (0, 1.04, 0.28)]

# wing: designed flat-ish, then raised ELEV deg about the root line (shoulder -> body attachment) for the bind pose
ELEV = 18.0
_S0, _BB0 = Vector((0.17, -0.30, 1.00)), Vector((0.15, 0.16, 0.96))
_ROT = Matrix.Rotation(math.radians(-ELEV), 3, (_BB0 - _S0).normalized())


def _raise(p):
    return _S0 + _ROT @ (Vector(p) - _S0)


_W, _H2, _T = _raise((0.80, -0.22, 1.18)), _raise((0.66, 0.46, 1.02)), _raise((1.58, 0.12, 1.30))
_N = (_T - _W).cross(_H2 - _W).normalized()
if _N.z < 0:
    _N = -_N
WING = wing3.Wing(S=tuple(_S0), W=tuple(_W), H=tuple(_W + _N * 0.30), BB=tuple(_BB0))
H2 = tuple(_H2)                                   # trailing point of the secondaries (geometry only)
TIP = tuple(_T)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def frame(z, n):
    """rotation: local z along z, local x = the plane normal n (orthogonalised)"""
    z = Vector(z).normalized()
    x = Vector(n)
    x = (x - z * x.dot(z)).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


def feather(B, root, tip, nrm, width, thick, color, bone, taper=0.22):
    """a flat tapered feather lying in the wing plane (thin along nrm), pointed at the tip"""
    root, tip = Vector(root), Vector(tip)
    R = frame(tip - root, nrm)
    L = (tip - root).length
    return B.add((root + tip) / 2, (thick / 2, width / 2, L / 2), color, bone, R=R, top=(1.0, taper),
                 role="limb", bevel=0.008)


def wing(B, s, side):
    """3-row feather wing in ONE plane, rows stacked along its normal: secondaries (mid) + coverts (light) on the arm
    bone; inner primaries on the arm bone; outer primaries (dark, long, spread like fingers) + hand coverts on the
    tip bone (they sweep back over the inner wing when folding)."""
    S0, W, H, bb = X(WING.S, s), X(WING.W, s), X(H2, s), X(WING.BB, s)
    T = X(TIP, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    nrm = (T - W).cross(H - W).normalized()
    if nrm.z < 0:
        nrm = -nrm

    def pl(p):                                     # project onto the wing plane through the wrist
        p = Vector(p)
        return p - nrm * (p - W).dot(nrm)

    S, H, bb = pl(S0), pl(H), pl(bb)
    # arm (leading edge, light) + wrist knuckle + hand bar
    B.seg(S0, W, 0.05, 0.085, COVERT, wb, side=nrm, ext=0.05, role="limb")
    B.add(W, (0.05, 0.065, 0.065), COVERT, wb, R=frame(W - S, nrm), role="limb")
    B.seg(W + nrm * 0.078, W.lerp(T, 0.28) + nrm * 0.078, 0.026, 0.05, COVERT, tb, side=nrm, role="limb")
    # secondaries (mid): 7 broad feathers along the arm reaching back past the trailing edge (saw edge)
    n_sec = 7
    for i in range(n_sec):
        t = (i + 0.5) / n_sec
        a = S.lerp(W, 0.04 + 0.92 * t)
        end = bb.lerp(H, t)
        d = end - a
        end = end + d.normalized() * (0.07 + 0.04 * ((i % 2) * 2 - 1))
        feather(B, a - nrm * 0.016, end - nrm * 0.016, nrm, 0.27, 0.034, SECOND, wb, taper=0.35)
    # coverts (light): 6 broad short feathers over the secondaries' roots
    for i in range(6):
        t = (i + 0.5) / 6
        a = S.lerp(W, 0.03 + 0.94 * t)
        end = a.lerp(bb.lerp(H, t), 0.50)
        feather(B, a + nrm * 0.02, end + nrm * 0.02, nrm, 0.22, 0.034, COVERT, wb, taper=0.5)
    # inner primaries on the ARM bone (fill between the secondaries and the hand)
    for i, (t, f) in enumerate(((0.12, 0.68), (0.32, 0.78), (0.50, 0.86))):
        dv = (H - W).normalized().lerp((T - W).normalized(), t).normalized()
        ln = (T - W).length * f
        feather(B, W + dv * 0.04 - nrm * 0.016, W + dv * ln - nrm * 0.016, nrm, 0.25, 0.034, PRIMARY, wb, taper=0.3)
    # outer primaries: 5 long dark "finger" feathers fanned from the wrist, one layer above the coverts (tip bone)
    n_pri = 5
    for i in range(n_pri):
        t = i / (n_pri - 1)
        dv = (H - W).normalized().lerp((T - W).normalized(), 0.66 + 0.34 * t).normalized()
        ln = (T - W).length * (0.92 + 0.10 * t) * (1.0 + 0.04 * ((i % 2) * 2 - 1))
        o = nrm * (0.065 + 0.004 * (n_pri - 1 - i))
        feather(B, W + dv * 0.04 + o, W + dv * ln + o, nrm, 0.23, 0.034, PRIMARY, tb, taper=0.28)
    # hand coverts (light) over the primaries' roots
    for i in range(4):
        t = (i + 0.5) / 4
        dv = (H - W).normalized().lerp((T - W).normalized(), 0.60 + 0.40 * t).normalized()
        o = nrm * 0.11
        feather(B, W + dv * 0.03 + o, W + dv * 0.36 + o, nrm, 0.20, 0.034, COVERT, tb, taper=0.5)


def eye(B, c, s, yaw=28, bone="Head", sc=1.0):
    """FIERCE_PLAN eye recipe: black socket -> yellow slit -> hot highlight on the outer half (brow = the ridge)"""
    R = Euler((0, math.radians(-s * 18), math.radians(s * yaw)), "XYZ").to_matrix()
    c = Vector(c)
    B.add(c, (0.05 * sc, 0.008, 0.026 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + R @ Vector((0.002 * s, -0.006, -0.002)), (0.042 * sc, 0.006, 0.014 * sc), EYE, bone, R=R, studs=[],
          role="detail", bevel=0.003)
    B.add(c + R @ Vector((s * 0.016 * sc, -0.010, 0.0)), (0.017 * sc, 0.004, 0.006 * sc), EYE_HOT, bone, R=R,
          studs=[], role="detail", bevel=0.002)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=157, tier=6, plates=False)
    # ---------------- torso: eagle ribcage (Chest) -> sloped tuck -> lion waist + hips (Spine)
    B.add((0, -0.28, 0.74), (0.21, 0.32, 0.26), BODY, "Chest", bot=(0.66, 0.56), top=(0.90, 0.95), rnd=0.30)
    B.add((0, -0.36, 0.985), (0.16, 0.18, 0.05), BODY, "Chest", top=(0.70, 0.8))                     # withers
    B.seg((0, -0.04, 0.50), (0, 0.36, 0.58), 0.14, 0.08, LION, "Spine", top=(0.82, 0.75), bot=(1, 1), side=(1, 0, 0))
    B.add((0, 0.16, 0.74), (0.155, 0.22, 0.16), LION, "Spine", bot=(0.72, 0.70), top=(0.95, 1), rnd=0.30)  # waist
    B.add((0, 0.42, 0.75), (0.172, 0.20, 0.175), LION, "Spine", rot=(-8, 0, 0), top=(0.84, 0.90), bot=(0.85, 0.9),
          rnd=0.32)                                                                                     # hips
    B.seg((0, -0.04, 0.425), (0, 0.34, 0.522), 0.09, 0.022, UNDER, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    # feather skirt: eagle feathers overlapping onto the lion waist (sides + underside)
    for s in (1, -1):
        for z, L in ((0.88, 0.17), (0.76, 0.19), (0.64, 0.17), (0.54, 0.13)):
            B.spike((s * 0.15, -0.02, z), (s * 0.25, 1, -0.25), L, 0.06, BODY, "Chest", side=(s, 0, 0), top=(0.2, 0.3))
    # shingle chest ruff: 3 brick rows of down-pointing feathers on the breast, lower edges proud
    for r, (z, xs) in enumerate(((0.92, (-0.15, -0.05, 0.05, 0.15)), (0.80, (-0.10, 0.0, 0.10)),
                                 (0.68, (-0.05, 0.05)))):
        for x in xs:
            B.add((x, -0.615 + 0.03 * r, z), (0.055, 0.02, 0.07), NAPE if r == 0 else BODY, "Chest", rot=(-18, 0, 0),
                  bot=(0.2, 1.0), role="detail", bevel=0.008)
    # ---------------- neck: golden nape on the back, ruff of swept feathers
    B.seg((0, -0.50, 0.86), (0, -0.74, 1.18), 0.15, 0.15, BODY, "Neck", ext=0.05, ext1=0.03, top=(0.9, 0.9))
    B.seg((0, -0.58, 1.19), (0, -0.66, 1.30), 0.13, 0.07, NAPE, "Neck", ext=0.0, ext1=0.02, top=(0.85, 1))
    # golden hackle cape: 2 staggered rows (3 + 2) of shingle feathers down the back of the neck, tips to the withers
    dn = Vector((0, -0.6, 0.8))
    nn = Vector((0, 0.8, 0.6))
    Rn = Matrix.Rotation(math.radians(-14), 3, Vector((1, 0, 0))) @ Matrix((Vector((1, 0, 0)), nn, dn)).transposed()
    for t, xs in ((0.46, (-0.085, 0.0, 0.085)), (0.24, (-0.045, 0.045)), (0.04, (0.0,))):
        c = Vector((0, -0.38 - 0.24 * t, 0.95 + 0.32 * t)) + nn * 0.012
        for x in xs:
            B.add(c + Vector((x, 0, 0)), (0.062, 0.02, 0.09), NAPE, "Neck" if t > 0.1 else "Chest", R=Rn,
                  bot=(0.2, 1.0), role="limb", bevel=0.008)
    for s in (1, -1):
        for y, z, L in ((-0.64, 1.18, 0.16), (-0.56, 1.06, 0.18), (-0.50, 0.94, 0.15)):
            B.spike((s * 0.12, y, z), (s * 0.45, 0.8, -0.35), L, 0.055, NAPE, "Neck", top=(0.12, 0.35))
    # ---------------- eagle head (pivot at the throat)
    B.add(HC, (0.135, 0.13, 0.115), BODY, "Head", top=(0.85, 0.85))                                   # cranium
    B.add(HC + Vector((0, 0.03, 0.10)), (0.115, 0.11, 0.035), NAPE, "Head", top=(0.75, 0.8))          # golden crown
    B.add(HC + Vector((0, -0.10, -0.045)), (0.10, 0.06, 0.075), BODY, "Head", top=(0.9, 1))           # face
    B.add(HC + Vector((0, -0.165, -0.015)), (0.072, 0.035, 0.036), YELLOW, "Head", top=(0.85, 1))     # cere band
    for s in (1, -1):
        B.add(HC + Vector((s * 0.073, -0.17, -0.005)), (0.004, 0.010, 0.007), BLACK, "Head", studs=[],
              role="detail", bevel=0.003)                                                             # nostrils
    # big hooked beak: upper bill tapering forward, hooked tip curving down
    B.seg(HC + Vector((0, -0.16, -0.012)), HC + Vector((0, -0.29, -0.035)), 0.062, 0.056, YELLOW, "Head",
          top=(0.6, 0.6), ext=0.0)
    B.seg(HC + Vector((0, -0.25, -0.005)), HC + Vector((0, -0.315, -0.05)), 0.036, 0.042, BEAK_D, "Head",
          top=(0.8, 0.8), ext=0.01)
    B.spike(HC + Vector((0, -0.305, -0.04)), (0, -0.25, -1), 0.10, 0.032, BEAK_D, "Head", top=(0.15, 0.2))
    B.add(HC + Vector((0, -0.22, -0.068)), (0.052, 0.07, 0.005), MOUTH, "Head", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):                                                                                   # gape line
        B.add(HC + Vector((s * 0.06, -0.20, -0.06)), (0.004, 0.06, 0.007), MOUTH, "Head", rot=(-8, 0, 0), studs=[],
              role="detail", bevel=0.002)
    # lower mandible (opens in the screech)
    B.seg(HC + Vector((0, -0.14, -0.088)), HC + Vector((0, -0.27, -0.09)), 0.05, 0.02, YELLOW, "Jaw", top=(0.7, 1),
          ext=0.02)
    # heavy brow ridges overhanging narrow yellow eyes (inner end low)
    for s in (1, -1):
        eye(B, HC + Vector((s * 0.10, -0.128, 0.022)), s, sc=1.05)
        B.add(HC + Vector((s * 0.080, -0.118, 0.07)), (0.085, 0.045, 0.03), BROW, "Head",
              rot=(0, -s * 20, s * 22), role="detail", bevel=0.012)
    # swept ear tufts (3 feathers per side) + cheek feathers
    for s in (1, -1):
        root = HC + Vector((s * 0.10, 0.07, 0.10))
        for dv, ln, w in (((s * 0.30, 0.75, 0.75), 0.22, 0.05), ((s * 0.55, 0.80, 0.40), 0.18, 0.045),
                          ((s * 0.15, 0.95, 0.30), 0.18, 0.045)):
            B.spike(root, dv, ln, w, NAPE, "Head", top=(0.12, 0.35))
        for z, dz, L in ((-0.08, -0.45, 0.15), (0.0, -0.1, 0.16)):
            B.spike(HC + Vector((s * 0.11, 0.0, z)), (s * 0.5, 0.85, dz), L, 0.05, BODY, "Head", top=(0.12, 0.35))
    # ---------------- feathered wings
    for s, side in ((1, "L"), (-1, "R")):
        wing(B, s, side)
    # ---------------- legs: eagle forelegs (trousers, scaly shanks, 4 talons), lion hind legs (paw + claws)
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.06)), K, 0.08, 0.10, BODY, leg, ext1=0.03, top=(0.8, 0.75))     # trousers
                for dx in (-0.05, 0.0, 0.05):                       # feather fringe over the shank top
                    B.spike(K + Vector((s * dx, -0.02, 0.05)), (s * dx * 0.8, -0.2, -1), 0.10, 0.04, BODY, leg,
                            top=(0.2, 0.4))
                B.seg(K, A, 0.045, 0.05, YELLOW, shin, ext=0.03, ext1=0.02, role="limb")                # shank
                for t in (0.30, 0.55, 0.80):                        # scale bands
                    c = K.lerp(A, t)
                    B.add(c, (0.048, 0.053, 0.008), YELLOW_D, shin, rot=(-12, 0, 0), studs=[], role="detail",
                          bevel=0.004)
                B.add(P + Vector((0, 0.01, 0.0)), (0.055, 0.055, 0.04), YELLOW, foot, role="limb")         # foot
                for dx, dy in ((-0.045, -0.07), (0.0, -0.085), (0.045, -0.07)):
                    tb = P + Vector((dx, dy, -0.012))
                    B.seg(P + Vector((dx * 0.5, -0.02, -0.01)), tb, 0.022, 0.024, YELLOW, foot, role="limb")
                    B.spike(tb + Vector((0, -0.01, 0.006)), (0, -1, -0.62), 0.08, 0.019, BLACK, foot)
                B.spike(P + Vector((0, 0.05, -0.006)), (0, 1, -0.6), 0.07, 0.018, BLACK, foot)
            else:
                B.seg(H + Vector((0, 0.03, 0.08)), K, 0.072, 0.14, LION, leg, bot=(0.85, 1), top=(0.75, 0.62),
                      ext1=0.03)
                B.seg(K, A, 0.06, 0.07, LION, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02)
                B.seg(A, P + Vector((0, 0.03, 0.03)), 0.05, 0.054, LION, foot, ext=0.03)
                B.add(P, (0.075, 0.09, 0.045), LION, foot, top=(0.85, 0.80))                                  # paw
                for gx in (-0.045, -0.015, 0.015, 0.045):
                    B.spike((P.x + gx, P.y - 0.08, 0.035), (0, -1, -0.55), 0.06, 0.013, BLACK, foot)
    # ---------------- lion tail with a dark tuft
    T = [Vector(p) for p in TAILP]
    for (a, b), (w, d), bn in zip(zip(T, T[1:]), ((0.045, 0.05), (0.038, 0.04), (0.032, 0.034)),
                                  ("Tail1", "Tail2", "Tail3")):
        B.seg(a, b, w, d, LION, bn, ext=0.04, top=(0.9, 0.9))
    tip = T[3] + Vector((0, 0.02, -0.02))
    B.add(tip, (0.05, 0.06, 0.05), TUFT, "Tail3", rnd=0.4)
    for d, L in (((0, 0.8, -0.3), 0.13), ((0.5, 0.6, -0.5), 0.10), ((-0.5, 0.6, -0.5), 0.10), ((0, 0.4, -0.9), 0.11)):
        d = Vector(d).normalized()
        B.spike(tip, d, L, 0.045, TUFT, "Tail3", top=(0.12, 0.38))
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.40, 0.78), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.04, 0.78), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.48, 0.90), "Chest", tail=(0, -0.24, 0.30))
    k.joint("Head", tuple(HC + Vector((0, 0.08, -0.12))), "Neck", tail=(0, -0.35, 0))       # throat pivot
    k.joint("Jaw", tuple(HC + Vector((0, -0.12, -0.08))), "Head", tail=(0, -0.2, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Wing_" + side, X(WING.S, s), "Chest")
        k.joint("WingTip_" + side, X(WING.W, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.1))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    for i in range(3):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=tuple(Vector(TAILP[i + 1]) - Vector(TAILP[i])))


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    P = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
         ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ("Head", "Neck", "Tail1", "Tail2", "Tail3", "Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Leg_FL", "Leg_FR",
                  "Chest", "Spine"):
            P.append((w, b))
    P += [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
          ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
          ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    P += [("Head", "Chest"), ("Jaw", "Chest"), ("Jaw", "Neck")]
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
        P.append(("Tail2", b))
        P.append(("Tail3", b))
    return P


def joints():
    """wrist knuckle + hinge (wing3) and the shoulder: the arm root turns about the root line inside the chest edge"""
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.12, "Wing_" + sd))
    return out


# ------------------------------------------------------------------ animation (FIERCE_PLAN Griffin)
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]
FOLD = (40.0, -4.0, 0.0, 100.0)     # fold-searched: heraldic raised V, primaries swept back over the inner wing


def ease(u):
    u = max(0.0, min(1.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side=side)


def folded(k, f, du=0.0, dfwd=0.0, dtip=0.0, side=None):
    wings(k, f, FOLD[0] + du, FOLD[1] + dfwd, FOLD[2], FOLD[3] + dtip, side)


def blend(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def tail(k, f, n, sway=8.0, lift=0.0, cycles=2):
    for i, bn in enumerate(TAIL):
        k.key(bn, f, rot=(lift + 3 * i, sway * (0.6 + 0.3 * i) * pk.wave(f, n, 0.15 * i, cycles), 0))


def rest_keys(k, f, z=0.0, pitch=0.0):
    k.key("Spine", f, rot=(pitch, 0, 0), loc=(0, 0, z))
    k.key("Chest", f, rot=(0, 0, 0))
    k.key("Neck", f, rot=(0, 0, 0), loc=(0, 0, 0))
    k.key("Head", f, rot=(0, 0, 0))
    k.key("Jaw", f, rot=(0, 0, 0))
    folded(k, f)
    for b in TAIL:
        k.key(b, f, rot=(0, 0, 0))


def solve(k, f, legs=LEGS4, offs=None):
    for leg in legs:
        o = (offs or {}).get(leg, (0, 0, 0))
        k.solve_leg(leg, f, Vector((k.J[leg].x + o[0], k.J[leg].y + o[1], o[2])))


def plant_frames(k, frames, legs=LEGS4):
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        solve(k, f, legs)


# ---- ground
def idle(k):
    """RAPTOR WATCH: snappy head-locked turns (6 f turn, long holds) while the body breathes under a still head, cocks
    its head to look up at the sky with ONE eye, a beak clack, re-tucks the raised wings, the tail tuft flicks."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.008 * b))
        k.key("Chest", f, rot=(-1.2 * b, 0, 0))
        fl = 0.0
        for c in (30, 76):
            if c <= f <= c + 8:
                fl = 22 * math.sin(math.pi * (f - c) / 8)
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(2 * i, 5 * pk.wave(f, n, 0.15 * i, 2) + (fl if bn == "Tail3" else 0), 0))
    # head-lock: quick turns, long holds (the neck counters the breathing chest so the head stays still)
    for f, nk, hd, yaw, roll in ((0, 0, 0, 0, 0), (10, 0, 0, 0, 0), (16, 0, -2, -32, 0), (36, 0, -2, -32, 0),
                                 (42, 0, -2, 28, 0), (56, 0, -2, 28, 0), (62, -4, -10, 10, 36), (78, -4, -10, 10, 38),
                                 (84, 0, 0, 0, 0), (n, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, yaw * 0.35, 0), loc=(0, 0, 0))
        k.key("Head", f, rot=(hd, yaw * 0.65, roll))
    for f, jw in ((0, 0), (84, 0), (86, 16), (88, 0), (90, 12), (92, 0), (n, 0)):        # beak clack
        k.key("Jaw", f, rot=(jw, 0, 0))
    for f, du, dt in ((0, 0, 0), (94, 0, 0), (100, 6, -10), (104, 6, -10), (110, 0, 0), (n, 0, 0)):   # re-tuck
        folded(k, f, du, 0, dt)
    plant_frames(k, range(0, n + 1))
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    """lateral walk with a pigeon-style HEAD BOB: the head thrusts forward and holds still against the body."""
    n = 30

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 1.2 * pk.wave(f, n, 0.0), 1.5 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.02 * b))
        k.key("Chest", f, rot=(0, -1.5 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n, 0.25)))
        u = (2 * f / n) % 1.0
        bob = (u / 0.3) if u < 0.3 else (1 - (u - 0.3) / 0.7)
        k.key("Neck", f, rot=(4 * bob, 0, 0), loc=(0, -0.06 * bob, 0))
        k.key("Head", f, rot=(-4 * bob, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        folded(k, f, du=2 * pk.wave(f, n, 0.3, 2))
        tail(k, f, n, sway=10, lift=0, cycles=1)
    return cm.quad_walk(k, n, 0.15, 0.11, body, gait="walk")


def roar(k):
    """SKY SCREECH: chest up, both wings flung UP into a tall V with the primaries spread, the head thrust FORWARD with
    the beak gaping, holds the screech, folds back."""
    n = 60
    k.new_action("roar", n, False)
    V = (44.0, 0.0, -6.0, -6.0)
    for f, p, z, nk, hd, jw, w in ((0, 0, 0, 0, 0, 0, 0.0), (8, 3, -0.03, 6, 6, 2, 0.15), (16, -10, 0.02, -10, 14, 32, 1.0),
                                   (42, -10, 0.02, -10, 14, 34, 1.0), (52, -2, 0, -2, 2, 4, 0.2), (n, 0, 0, 0, 0, 0, 0.0)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0), loc=(0, -0.06 * (16 <= f <= 42), 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        wings(k, f, *blend(FOLD, V, w))
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(12 * (16 <= f <= 42), 0, 0))
    for f in range(18, 42, 2):
        k.key("Jaw", f, rot=(33 + (2 if (f // 2) % 2 else -2), 0, 0))
    plant_frames(k, range(0, n + 1))
    k.finish(loop=False)


def mantle(k):
    """SIGNATURE - MANTLE THE KILL: spots prey and locks on, strikes it with the right talon, MANTLES (wings spread low
    and arched forward like a tent over the prey, head low glaring up), two tearing pulls with the shoulders heaving,
    the head snaps up with the beak open, folds the wings and steps back."""
    import bpy
    n = 95
    k.new_action("act_mantle", n, False)
    TENT = (-38.0, 31.0, -12.0, -6.0)
    for f, y, z, p, ch, nk, hd, jw in ((0, 0, 0, 0, 0, 0, 0, 0), (12, 0, -0.04, 4, 0, 14, 10, 0),
                                       (20, -0.08, -0.05, 6, 0, 16, 8, 6), (24, -0.12, -0.08, 8, 2, 18, 4, 0),
                                       (34, -0.12, -0.10, 10, 2, 22, -14, 4),
                                       (40, -0.12, -0.10, 10, 4, 28, 14, 24), (44, -0.12, -0.10, 10, 4, 28, 18, 4),
                                       (50, -0.12, -0.08, 8, -1, 12, -12, 6), (56, -0.12, -0.10, 10, 4, 28, 14, 24),
                                       (60, -0.12, -0.10, 10, 4, 28, 18, 4), (66, -0.12, -0.08, 8, -1, 12, -12, 6),
                                       (72, -0.10, -0.06, 4, -2, -3, -16, 30), (78, -0.10, -0.06, 4, -2, -3, -16, 30),
                                       (86, -0.03, -0.02, 2, 0, 0, 0, 2), (n, 0, 0, 0, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, y, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0), loc=(0, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    for f, w in ((0, 0.0), (14, 0.0), (24, 0.35), (32, 1.0), (88, 0.0), (n, 0.0)):
        wings(k, f, *blend(FOLD, TENT, w))
    for f in (68, 70, 72, 76):                                    # wings ease back as the head snaps up
        wings(k, f, TENT[0], 10.0, TENT[2], TENT[3])
    for f in range(36, 66, 2):                                    # the mantle heaves with the pulls
        h = math.sin(2 * math.pi * (f - 36) / 16)
        wings(k, f, *blend(FOLD, (TENT[0] + 3 + 3 * h, TENT[1], TENT[2], TENT[3]), 1.0))
    for f in range(0, n + 1, 2):
        tail(k, f, n, sway=6, lift=6 * ease((f - 20) / 10) * (1 - ease((f - 80) / 10)), cycles=3)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        # the right talon reaches forward and strikes down onto the prey 0.26 ahead (held there), steps back at 80-90
        if f < 12 or f > 92:
            o = (0, 0, 0)
        elif f <= 20:
            u = (f - 12) / 8
            o = (0, -0.26 * ease(u), 0.16 * math.sin(math.pi * u))
        elif f <= 80:
            o = (0, -0.26, 0)
        else:
            u = (f - 80) / 12
            o = (0, -0.26 * (1 - ease(u)), 0.10 * math.sin(math.pi * u))
        solve(k, f, offs={"Leg_FR": o})
    k.finish(loop=False)


# ---- flight
FLY_N = 44
PITCH = 8.0


def fly_legs(k, f, ph, amt=1.0, pump=0.0):
    """eagle talons tucked up under the chest; lion hind legs trailing back, pumping on each downstroke"""
    for leg in LEGS4:
        fr = leg[4] == "F"
        side = leg[4:]
        if fr:
            k.key(leg, f, rot=(amt * 25, 0, 0))
            k.key("Shin_" + side, f, rot=(amt * 95, 0, 0))
            k.key("Foot_" + side, f, rot=(amt * 60, 0, 0))
        else:
            k.key(leg, f, rot=(amt * (42 + 10 * pump), 0, 0))
            k.key("Shin_" + side, f, rot=(amt * (-6 + 12 * pump), 0, 0))
            k.key("Foot_" + side, f, rot=(amt * 50, 0, 0))


def body_fly(k, f, ph, glide=0.0):
    s = math.sin(2 * math.pi * (ph - 0.1))
    k.key("Spine", f, rot=(PITCH - 3 * s * (1 - glide), 0, 0),
          loc=(0, 0, 0.08 * math.cos(2 * math.pi * (ph - 0.45)) * (1 - glide)))
    k.key("Chest", f, rot=(-2 * s * (1 - glide), 0, 0))
    k.key("Neck", f, rot=(-6 + 3 * math.sin(2 * math.pi * (ph - 0.25)) * (1 - glide), 0, 0), loc=(0, 0, 0))
    k.key("Head", f, rot=(-6 - 3 * math.sin(2 * math.pi * (ph - 0.32)) * (1 - glide), 0, 0))
    k.key("Jaw", f, rot=(0, 0, 0))
    for i, b in enumerate(TAIL):
        k.key(b, f, rot=((36 if i == 0 else -2 if i == 1 else 14) + 5 * math.sin(2 * math.pi * (ph - 0.3 - 0.12 * i)),
                         3 * math.sin(2 * math.pi * (ph - 0.2 * i)), 0))


GLIDE = (-6.0, 2.0, 4.0, -6.0)


def fly_pose(k, f, legs=True, cf=None):
    """FLAP-FLAP-GLIDE (44 f): 2 powerful strokes (0-14, 14-28) with the primaries spread, then a glide hold (32-40),
    the wings rise back to the top of the stroke by 44. cf = cycle frame used for the pose (default f)."""
    c = f if cf is None else cf
    if c <= 28:
        ph = (c % 14) / 14 if c < 28 else 1.0
        w = wing3.stroke(ph, bot=-34)
        wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
        body_fly(k, f, ph)
        pump = max(0.0, math.sin(math.pi * min(1.0, ph / 0.45)))
        if legs:
            fly_legs(k, f, ph, pump=pump)
    else:
        top = wing3.stroke(0.0, bot=-34)
        T = (top["up"], top["fwd"], top["twist"], top["tip"])
        if c <= 32:
            g = ease((c - 28) / 4)
        elif c <= 40:
            g = 1.0
        else:
            g = 1 - ease((c - 40) / 4)
        wings(k, f, *blend(T, GLIDE, g))
        body_fly(k, f, 0.0, glide=g)
        if legs:
            fly_legs(k, f, 0.0, pump=0.0)


def fly(k):
    k.new_action("fly", FLY_N, True)
    for f in range(0, FLY_N + 1):
        fly_pose(k, f)
    k.finish()


def takeoff(k):
    """crouch with the wings opening high, LAUNCH (frame 11) on a huge downstroke, legs push then tuck"""
    n = 30
    k.new_action("takeoff", n, False)
    rest_keys(k, 0)
    for f, z, p, w in ((5, -0.10, 6, (30, -6, -6, 40)), (10, -0.18, 8, (34, -2, -8, -6)),
                       (13, 0.10, 10, (-10, 8, 12, -10)), (16, 0.18, 12, (-24, 6, 4, 6))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(2, 0, 0))
        k.key("Neck", f, rot=(-8, 0, 0), loc=(0, 0, 0))
        k.key("Head", f, rot=(-6, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(-4, 0, 0))
    for f in range(18, n + 1, 2):                                # glide out of the launch, rise to the stroke top
        fly_pose(k, f, legs=False, cf=round(31 + 13 * (f - 18) / (n - 18)))
    plant_frames(k, range(0, 13))
    for f, a in ((15, 0.5), (19, 0.9), (n, 1.0)):
        fly_legs(k, f, 0.0, a)
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """flares upright with braking beats, legs swing down and reach, touches (frame 17), absorbs, folds the wings"""
    n = 30
    k.new_action("land", n, False)
    fly_pose(k, 0)
    for f, p, z, w in ((6, 4, 0.06, (20, 18, -14, -4)), (10, -8, 0.10, (-18, 22, -14, 6)),
                       (13, -8, 0.08, (18, 16, -10, -6)), (15, -4, 0.04, (0, 8, -6, 10))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(-2, 0, 0))
        k.key("Neck", f, rot=(-4, 0, 0), loc=(0, 0, 0))
        k.key("Head", f, rot=(-4, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(8, 0, 0))
    for f, a in ((6, 0.6), (11, 0.2)):
        fly_legs(k, f, 0.0, a)
    for f, z, p, w in ((17, -0.16, 6, (12, -6, 0, 40)), (21, -0.08, 3, (30, -4, -2, 80)), (26, 0.0, 0, None)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(1, 0, 0))
        k.key("Neck", f, rot=(p * 0.5, 0, 0), loc=(0, 0, 0))
        k.key("Head", f, rot=(-p * 0.3, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
        for b in TAIL:
            k.key(b, f, rot=(-2, 0, 0))
    rest_keys(k, n)
    plant_frames(k, range(17, n + 1))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(17 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    mantle(k)
    return stride


HEAD_XF = []
