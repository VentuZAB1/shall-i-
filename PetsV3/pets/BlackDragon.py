# Black Eastern Dragon (Void egg #3) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the storm lung"): a long Chinese lung
# built from tapered blocks and covered in Roblox studs (blockkit.stud_skin): a thin ink-indigo serpent body (D tapering
# 1.0 -> 0.35) in 9 chain segments arched in a side-view S, a pale "clam" belly of transverse scutes, a violet flame
# mane from the poll to the tail fan, 4 short legs with elbow flames and gold eagle talons, a long camel-like head with
# an open jaw and 4 fangs, narrow gold eyes under heavy brows, a gold chimu bump on the brow, gold stag antlers with
# 2 tines, ox ears, 2 long drooping gold whiskers, a flame beard - and the flaming pearl it chases, by its cheek.
# FLIES WITHOUT WINGS (Motion = Fly).  Old chibi version: _tools/chibi_specs/BlackDragon.py
import math
from mathutils import Vector, Euler, Matrix

DISPLAY = "Black Eastern Dragon"
MOTION = "Fly"
RIG = "serpent"
HEIGHT = 9.0

INK = (78, 68, 158)           # ink-indigo body (Roblox renders ~0.6x darker -> near-black indigo in game)
DARK = (44, 36, 88)           # brows, back scales, claws' fingers
BELLY = (176, 164, 214)       # clam-belly scutes, lips, chin
MANE = (146, 84, 236)         # violet flame mane ...
MANE_L = (204, 158, 255)      # ... lighter tips
GOLD = (255, 196, 50)         # accent: antlers, talons, whiskers, chimu, eyes
GOLD_D = (214, 150, 30)
EYE = (255, 196, 50)
EYE_HOT = (255, 238, 170)
PEARL = (236, 232, 255)
PEARL_C = (196, 160, 255)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
MOUTH = (96, 22, 46)
TONGUE = (200, 70, 110)

PITCH = 0.043               # 0.042 x (U / U_raiju), U = model height / HEIGHT

D = 0.28                                            # tube diameter at the chest
# chain joints (side-view S): chest (front legs) -> hump -> hips (hind legs) -> tail curling up
CHAIN = ["Spine", "Body1", "Body2", "Body3", "Body4", "Body5", "Tail1", "Tail2", "Tail3"]
CP = [Vector(p) for p in ((0, -0.20, 0.52), (0, 0.10, 0.66), (0, 0.36, 0.90), (0, 0.66, 1.08), (0, 0.96, 0.90),
                          (0, 1.20, 0.58), (0, 1.48, 0.52), (0, 1.76, 0.57), (0, 1.98, 0.75), (0, 2.08, 1.08))]
RAD = [D / 2 * (1 - 0.62 * i / 9) for i in range(10)]
NECK = [Vector((0, -0.48, 0.55)), Vector((0, -0.70, 0.78)), Vector((0, -0.84, 1.02))]
HC = Vector((0, -1.02, 1.14))                      # cranium centre
PEARL_P = Vector((-0.50, -1.18, 1.30))
# leg joints (left side): H hip, K elbow (out), A wrist, P foot centre
LEGS = {"F": ((0.10, -0.22, 0.46), (0.24, -0.27, 0.30), (0.21, -0.20, 0.10), (0.21, -0.25, 0.04)),
        "B": ((0.075, 1.34, 0.52), (0.23, 1.41, 0.30), (0.20, 1.32, 0.10), (0.20, 1.27, 0.04))}


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def up_of(d):
    u = Vector((0, d.z, -d.y))
    return u.normalized() if u.z > 0 else -u.normalized()


def flame(B, base, up, back, h, w, t, color, bone, tip_c=None, tip_frac=0.40):
    """flat flame blade standing on a surface (up = blade direction), base along `back`, tip swept back"""
    up = Vector(up).normalized()
    back = Vector(back)
    back = (back - up * back.dot(up)).normalized()
    R = Matrix((up.cross(back), back, up)).transposed()
    B.add(base + up * (h / 2), (t, w, h / 2), color, bone, R=R, top=(0.5, 0.18), top_shift=(0, w * 0.95),
          role="limb")
    if tip_c:
        f = tip_frac
        z0 = h * (1 - f)
        wz = w * (1 - (1 - 0.18) * (1 - f))
        B.add(base + up * (z0 + h * f / 2) + back * (w * 0.95 * (1 - f / 2)), (t * 1.1, wz, h * f / 2), tip_c, bone,
              R=R, top=(0.6, 0.18 * w / wz), top_shift=(0, w * 0.95 * f), role="limb", studs=[])


def eye(B, c, s, yaw=24, bone="Head", sc=1.0):
    """FIERCE_PLAN eye recipe: black socket -> gold slit (+ reptile slit pupil) -> hot highlight -> heavy brow"""
    R = Euler((0, math.radians(-s * 18), math.radians(s * yaw)), "XYZ").to_matrix()
    Rb = Euler((0, math.radians(-s * 22), math.radians(s * yaw)), "XYZ").to_matrix()
    c = Vector(c)
    B.add(c + Rb @ Vector((-s * 0.006, 0.026, 0.048 * sc)), (0.075 * sc, 0.034, 0.03 * sc), DARK, bone, R=Rb,
          role="detail", bevel=0.01)
    B.add(c, (0.056 * sc, 0.008, 0.026 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + R @ Vector((0.002 * s, -0.007, 0.0)), (0.047 * sc, 0.006, 0.014 * sc), EYE, bone, R=R, studs=[],
          role="detail", bevel=0.003)
    B.add(c + R @ Vector((-s * 0.004, -0.010, 0.0)), (0.006 * sc, 0.004, 0.013 * sc), BLACK, bone, R=R, studs=[],
          role="detail", bevel=0.002)
    B.add(c + R @ Vector((s * 0.022 * sc, -0.011, 0.002)), (0.016 * sc, 0.004, 0.006 * sc), EYE_HOT, bone, R=R,
          studs=[], role="detail", bevel=0.002)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=149, tier=5, plates=False, th=0.40)
    # ---------------- the serpent body: 9 rounded tapering segments (one per chain bone), clam-belly scutes,
    # a violet flame blade on each segment's back
    for i in range(9):
        bone = CHAIN[i]
        a, b = CP[i], CP[i + 1]
        r0, r1 = RAD[i], RAD[i + 1]
        d = (b - a).normalized()
        B.seg(a, b, r0, r0, INK, bone, side=(1, 0, 0), ext=0.05 if i else 0.0, ext1=0.05,
              top=(r1 / r0, r1 / r0), rnd=0.42, role="mass" if i < 6 else "limb")
        up = up_of(d)
        for t in (0.28, 0.72):                                        # 2 transverse belly scutes per segment
            rm = r0 + (r1 - r0) * t
            c = a.lerp(b, t) - up * (rm * 0.80)
            B.add(c, (rm * 0.78, (b - a).length * 0.19, rm * 0.26), BELLY, bone, R=Matrix((Vector((1, 0, 0)),
                  d, Vector((1, 0, 0)).cross(d))).transposed(), rnd=0.3, studs=[])
        rm = (r0 + r1) / 2
        B.seg(a + up * (rm * 0.72), b + up * (r1 * 0.72), rm * 0.42, rm * 0.3, DARK, bone, side=(1, 0, 0), ext=0.02,
              ext1=0.02, top=(r1 / r0, r1 / r0))                              # dark back ridge under the mane
        flame(B, a.lerp(b, 0.42) + up * (rm * 0.75), up * 0.75 - d * 0.65, -d, rm * 2.0, rm * 1.1, rm * 0.26,
              MANE if i % 2 == 0 else MANE_L if i > 6 else MANE, bone, tip_c=MANE_L if i <= 6 else None)
    # chest front: the body runs on under the neck root
    B.seg(NECK[0] + Vector((0, 0.02, -0.02)), CP[0], RAD[0] * 1.02, RAD[0] * 1.02, INK, "Spine", side=(1, 0, 0),
          ext=0.06, rnd=0.42)
    B.add(NECK[0].lerp(CP[0], 0.5) - Vector((0, 0, RAD[0] * 0.78)), (RAD[0] * 0.78, 0.07, RAD[0] * 0.26), BELLY,
          "Spine", rot=(-8, 0, 0), rnd=0.3, studs=[])
    # tail fan: 3 flat flame blades ending in a point (side-view plane)
    tip = CP[9]
    dz = (CP[9] - CP[8]).normalized()
    for dv, ln, w, c in ((dz, 0.26, 0.09, MANE), (dz * 0.6 + Vector((0, 0.8, 0)), 0.20, 0.07, MANE_L),
                         (dz * 0.6 + Vector((0, -0.8, 0)), 0.18, 0.065, MANE_L)):
        dv = dv.normalized()
        B.seg(tip - dv * 0.03, tip + dv * ln, 0.02, w, c, "Tail3", side=(1, 0, 0), top=(1, 0.1), role="limb")
    # ---------------- neck: 2 rings from the chest up into the back of the head, belly scutes, mane blades
    for j in range(2):
        a, b = NECK[j], NECK[j + 1]
        d = (b - a).normalized()
        B.seg(a, b, 0.135, 0.135, INK, "Neck", side=(1, 0, 0), ext=0.03 if j else 0.0, ext1=0.06, rnd=0.42,
              top=(0.95, 0.95))
        up = up_of(d)
        for t in (0.3, 0.75):
            c = a.lerp(b, t) - up * 0.108
            B.add(c, (0.105, (b - a).length * 0.19, 0.036), BELLY, "Neck", R=Matrix((Vector((1, 0, 0)), d,
                  Vector((1, 0, 0)).cross(d))).transposed(), rnd=0.3, studs=[])
        flame(B, a.lerp(b, 0.5) + up * 0.08, up * 0.7 - d * 0.7, -d, 0.24, 0.13, 0.036, MANE, "Neck", tip_c=MANE_L)
    # ---------------- the head (2.2 D long, 1.4 D wide): long camel-like skull, broad snout, nostril knobs,
    # open jaw, fangs
    B.add(HC, (0.20, 0.16, 0.14), INK, "Head", top=(0.86, 0.85))                                    # cranium
    B.seg(HC + Vector((0, -0.13, -0.03)), HC + Vector((0, -0.55, -0.075)), 0.155, 0.10, INK, "Head", top=(0.80, 0.85),
          ext=0.0)                                                                                    # snout
    B.seg(HC + Vector((0, -0.15, 0.07)), HC + Vector((0, -0.48, 0.02)), 0.095, 0.03, DARK, "Head", top=(0.7, 1))  # ridge
    B.add(HC + Vector((0, -0.08, 0.165)), (0.07, 0.07, 0.04), GOLD, "Head", rnd=0.4)                # chimu bump
    for s in (1, -1):                                                                                 # nostril knobs
        knob = B.add(HC + Vector((s * 0.085, -0.555, -0.01)), (0.052, 0.048, 0.044), INK, "Head", rnd=0.4)
        B.add(knob.world((s * 0.006, -0.03, 0.036)), (0.02, 0.012, 0.006), DARK, "Head", rot=(-20, 0, s * 30),
              studs=[], role="detail", bevel=0.003)                                       # nostril on top
    B.seg(HC + Vector((0, -0.15, -0.125)), HC + Vector((0, -0.56, -0.15)), 0.145, 0.025, BELLY, "Head", top=(0.85, 1))
    B.add(HC + Vector((0, -0.35, -0.178)), (0.12, 0.20, 0.006), MOUTH, "Head", studs=[], role="detail", bevel=0.004)
    for s in (1, -1):
        B.spike(HC + Vector((s * 0.10, -0.50, -0.16)), (0, -0.1, -1), 0.10, 0.022, TEETH, "Head")       # fangs
        for y in (-0.42, -0.35, -0.28):
            B.spike(HC + Vector((s * 0.118, y, -0.16)), (0, 0, -1), 0.045, 0.015, TEETH, "Head")
    # lower jaw (Jaw bone), open 14 deg at rest: belly-pale chin, dark mouth, tongue, 2 lower fangs, flame beard
    JR = Euler((math.radians(14), 0, 0), "XYZ").to_matrix()
    JP = HC + Vector((0, -0.11, -0.17))

    def jp(p):
        return JP + JR @ Vector(p)
    B.add(jp((0, -0.21, -0.04)), (0.125, 0.22, 0.04), INK, "Jaw", R=JR, bot=(0.8, 0.85), role="limb")
    B.add(jp((0, -0.21, -0.077)), (0.10, 0.20, 0.006), BELLY, "Jaw", R=JR, studs=[], role="detail", bevel=0.004)
    B.add(jp((0, -0.20, 0.002)), (0.10, 0.19, 0.005), MOUTH, "Jaw", R=JR, studs=[], role="detail", bevel=0.003)
    B.add(jp((0, -0.18, 0.007)), (0.055, 0.14, 0.005), TONGUE, "Jaw", R=JR, studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike(jp((s * 0.085, -0.38, 0.0)), JR @ Vector((0, 0.1, 1)), 0.07, 0.018, TEETH, "Jaw")
    for x, L in ((0.0, 0.20), (0.06, 0.15), (-0.06, 0.15)):
        r0 = jp((x, -0.14, -0.07))
        B.spike(r0, (x * 2, 0.55, -1), L, 0.045, MANE, "Jaw", top=(0.12, 0.35))
    # narrow gold eyes (reptile slit pupils) under heavy brows at the skull-snout junction
    for s in (1, -1):
        eye(B, HC + Vector((s * 0.132, -0.162, 0.088)), s, sc=1.2)
    # gold stag antlers: a beam curving up and back in 3 segments, 2 forward tines, pointed tips
    for s in (1, -1):
        a0 = HC + Vector((s * 0.10, 0.04, 0.12))
        a1 = a0 + Vector((s * 0.065, 0.03, 0.19))
        a2 = a1 + Vector((s * 0.055, 0.13, 0.14))
        a3 = a2 + Vector((s * 0.02, 0.16, 0.05))
        for p, q, w in ((a0, a1, 0.034), (a1, a2, 0.030), (a2, a3, 0.026)):
            B.seg(p, q, w, w, GOLD, "Head", ext=0.02, role="limb")
        B.spike(a3, a3 - a2, 0.10, 0.024, GOLD, "Head")
        B.spike(a1 + (a2 - a1) * 0.15, (s * 0.2, -0.5, 0.85), 0.14, 0.024, GOLD, "Head")
        B.spike(a2 + (a3 - a2) * 0.2, (s * 0.15, -0.3, 0.95), 0.12, 0.022, GOLD, "Head")
    # ox ears: short, sticking out sideways behind the eyes
    for s in (1, -1):
        B.spike(HC + Vector((s * 0.18, 0.05, 0.07)), (s * 1, 0.35, 0.25), 0.15, 0.04, INK, "Head", top=(0.3, 0.6))
    # 2 long drooping gold whiskers (3 D) from beside the nostrils
    for s in (1, -1):
        w = [HC + Vector((s * 0.14, -0.52, -0.05)), HC + Vector((s * 0.24, -0.40, -0.12)),
             HC + Vector((s * 0.38, -0.20, -0.20)), HC + Vector((s * 0.50, 0.02, -0.34)),
             HC + Vector((s * 0.58, 0.20, -0.52))]
        for j, (p, q) in enumerate(zip(w, w[1:])):
            B.seg(p, q, 0.028 - 0.004 * j, 0.028 - 0.004 * j, GOLD, "Head", ext=0.02, role="limb")
        B.spike(w[4], w[4] - w[3], 0.08, 0.015, GOLD, "Head")
    # cheek frills: flame blades fanned back from the back corners of the jaw line
    for s in (1, -1):
        for z, dz, L, c in ((-0.11, -0.45, 0.22, MANE), (0.0, -0.05, 0.27, MANE_L), (0.10, 0.3, 0.20, MANE)):
            root = HC + Vector((s * 0.18, 0.09, z))
            d = Vector((s * 0.55, 0.75, dz)).normalized()
            B.seg(root, root + d * L, 0.065, 0.024, c, "Head", side=(0, 0, 1), ext=0.04, top=(0.12, 0.5), role="limb")
    # head mane: flame blades streaming back from the poll between the antlers
    for x, ln in ((0.0, 0.32), (-0.08, 0.25), (0.08, 0.25)):
        flame(B, HC + Vector((x, 0.13, 0.11)), Vector((x * 1.5, 0.75, 0.6)), (0, 1, -0.4), ln, 0.09, 0.032, MANE,
              "Head", tip_c=MANE_L)
    # ---------------- legs: upper leg out of the body side (elbow out), forearm, scaly foot, 4 gold talons,
    # an elbow flame
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            hw = 0.07 if fb == "F" else 0.066
            B.seg(H, K, hw, hw * 1.1, INK, leg, ext=0.0, ext1=0.04, side=(0, 1, 0))
            B.seg(K, A, hw * 0.85, hw * 0.9, INK, shin, ext=0.04, ext1=0.02, side=(0, 1, 0))
            B.add(K + Vector((s * 0.01, 0, 0)), (hw * 1.05, hw * 1.05, hw * 1.05), INK, leg, rnd=0.4)     # elbow
            flame(B, K + Vector((s * 0.02, 0.02, 0.0)), Vector((s * 0.5, 0.75, 0.25)), (0, 0, -1), 0.17, 0.05, 0.022,
                  MANE, leg, tip_c=MANE_L)
            B.add(P + Vector((0, 0.01, 0.0)), (0.06, 0.06, 0.04), DARK, foot, role="limb")                  # foot
            for dx, dy in ((-0.04, -0.06), (0.0, -0.07), (0.04, -0.06)):
                tb = P + Vector((dx, dy, -0.01))
                B.seg(P + Vector((dx * 0.5, -0.02, -0.005)), tb, 0.018, 0.02, DARK, foot, role="limb")
                B.spike(tb + Vector((0, -0.01, 0.006)), (0, -1, -0.62), 0.07, 0.016, GOLD, foot)
            B.spike(P + Vector((0, 0.05, -0.004)), (0, 1, -0.6), 0.06, 0.015, GOLD, foot)
    # ---------------- the flaming pearl (own bone): a round pearl with a violet core facet
    B.add(PEARL_P, (0.11, 0.11, 0.11), PEARL, "Pearl", rnd=0.45, role="limb")
    B.add(PEARL_P, (0.11, 0.11, 0.11), PEARL, "Pearl", rot=(0, 0, 45), rnd=0.45, role="limb")
    B.add(PEARL_P, (0.11, 0.11, 0.11), PEARL, "Pearl", rot=(45, 0, 0), rnd=0.45, role="limb")
    for j in range(8):                                  # gold equator band: an octagonal ring of 8 short bars
        ang = 2 * math.pi * j / 8
        c = PEARL_P + Vector((math.cos(ang), math.sin(ang), 0)) * 0.142
        B.add(c, (0.014, 0.06, 0.0125), GOLD, "Pearl", rot=(0, 0, math.degrees(ang)), role="limb", bevel=0.004,
              nostud=True)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", tuple(CP[0]), "Root", tail=tuple(CP[1] - CP[0]))
    for i in range(1, len(CHAIN)):
        k.joint(CHAIN[i], tuple(CP[i]), CHAIN[i - 1], tail=tuple(CP[i + 1] - CP[i]))
    k.joint("Neck", tuple(NECK[0]), "Spine", tail=tuple(NECK[2] - NECK[0]))
    k.joint("Head", tuple(HC + Vector((0, 0.14, -0.16))), "Neck", tail=(0, -0.4, 0))       # throat pivot
    k.joint("Jaw", tuple(HC + Vector((0, -0.11, -0.17))), "Head", tail=(0, -0.3, 0))
    k.joint("Pearl", tuple(PEARL_P), "Spine", tail=(0, 0, 0.2))
    for s, side in ((1, "L"), (-1, "R")):
        for fb, parent, knee in (("F", "Spine", (s * 0.6, -0.8, 0)), ("B", "Body5", (s * 0.6, 0.8, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)


def check_pairs():
    P = [("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"), ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw", "Neck"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Body2", "Body3", "Body4", "Tail1", "Tail2", "Tail3"):
            P.append((a, b))
    for a in ("Tail1", "Tail2", "Tail3"):
        for b in ("Spine", "Body1", "Body2", "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR"):
            P.append((a, b))
    for a, b in (("Body3", "Spine"), ("Body4", "Spine"), ("Body4", "Body1"), ("Body5", "Body1"), ("Body5", "Spine"),
                 ("Body5", "Body2"), ("Tail2", "Body4"), ("Tail3", "Body4"), ("Tail3", "Body5")):
        P.append((a, b))
    P += [("Pearl", "Head"), ("Pearl", "Jaw"), ("Pearl", "Neck"), ("Pearl", "Tail2"), ("Pearl", "Tail3"),
          ("Pearl", "Body2"), ("Pearl", "Tail1"), ("Pearl", "Leg_FL"), ("Pearl", "Leg_FR")]
    return P


def joints():
    """neck root inside the chest ring, and the overlapping ring ends at every chain joint (hidden hinges)"""
    out = [(NECK[0], NECK[0], 0.24, "Neck")]
    for i in range(1, len(CHAIN)):
        out.append((CP[i], CP[i], RAD[i - 1] * 1.4, CHAIN[i]))
    return out


# ------------------------------------------------------------------ animation (FIERCE_PLAN BlackDragon)
import petkit as pk
import _common as cm
from mathutils import Quaternion

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
FRONT = ["Leg_FL", "Leg_FR"]
HIND = ["Leg_BL", "Leg_BR"]
LIFT = 0.32                                  # flight height of the swimming clips (the body stays clear of the ground)


def ease(u):
    u = max(0.0, min(1.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)


def waves(k, f, n, pitch=0.0, yaw=0.0, phase=0.0, cycles=1, lag=0.11, base=None, start=0):
    """travelling wave down the body chain (pitch = vertical swim waves, yaw = side-to-side snaking)"""
    for i, bn in enumerate(CHAIN[start:], start):
        ph = phase - lag * i
        b = base[i] if base else (0, 0)
        s = math.sin(2 * math.pi * (cycles * f / n + ph))
        k.key(bn, f, rot=(b[0] + pitch * s, b[1] + yaw * s, 0))


def pearl(k, f, p=(0, 0, 0)):
    k.key("Pearl", f, rot=(0, 0, 0), loc=p)


def legs_fk(k, f, front=0.0, hind=0.0, paddle=0.0, ph=0.0):
    """airborne legs swept back along the body, making small grasping strokes"""
    for leg in LEGS4:
        fr = leg[4] == "F"
        side = leg[4:]
        s = 1 if side.endswith("L") else -1
        w = math.sin(2 * math.pi * (ph + (0.0 if fr else 0.5) + (0.0 if s > 0 else 0.25)))
        base = front if fr else hind
        k.key(leg, f, rot=(base + paddle * w, 0, -s * 8))
        k.key("Shin_" + side, f, rot=(28 + 0.6 * paddle * w, 0, 0))
        k.key("Foot_" + side, f, rot=(26, 0, 0))


def solve(k, f, legs=LEGS4):
    for leg in legs:
        k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


def idle(k):
    """PEARL NUDGE: a lazy side-wave rolls down the body, the pearl drifts away from the cheek and the dragon nudges it
    back with its snout - twice; the tail tip curls."""
    import bpy
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        waves(k, f, n, pitch=0.8, yaw=1.4, cycles=2, lag=0.10, start=1)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0, 2), 1.5 * pk.wave(f, n, 0, 2), 0), loc=(0, 0, 0.01 * b))
        curl = 18 * ease((f - 20) / 14) * (1 - ease((f - 96) / 14))
        k.key("Tail3", f, rot=(curl + 4 * pk.wave(f, n, 0.3, 4), 6 * pk.wave(f, n, 0.1, 2), 0))
    # the pearl drifts out to the right-front and up; the head turns to it and nudges it back (twice)
    for f, px, py, pz, nk, hy, h, jw in ((0, 0, 0, 0, 0, 0, 0, 0), (16, -0.06, -0.04, 0.04, 0, -6, 0, 0),
                                         (34, -0.18, -0.12, 0.08, 0, -22, -4, 0), (42, -0.18, -0.12, 0.08, 4, -30, 4, 6),
                                         (47, -0.04, -0.02, 0.02, 2, -14, 0, 0), (66, 0.0, 0.0, 0.0, 0, -4, 0, 0),
                                         (82, -0.14, -0.18, 0.12, 0, -18, -6, 0), (90, -0.14, -0.18, 0.12, 6, -26, 4, 6),
                                         (95, -0.02, -0.03, 0.02, 2, -10, 0, 0), (108, 0, 0, 0, 0, 0, 0, 0), (n, 0, 0, 0, 0, 0, 0, 0)):
        pearl(k, f, (px, py, pz + 0.025 * math.sin(2 * math.pi * f / 30)))
        k.key("Neck", f, rot=(nk, hy * 0.4, 0))
        k.key("Head", f, rot=(h, hy * 0.6, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        solve(k, f)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    """lizard trot: diagonal pairs, the long body snakes side to side, head steady, tail swinging."""
    n = 28

    def body(f):
        waves(k, f, n, pitch=0.5, yaw=2.5, cycles=1, lag=0.12, start=1)
        k.key("Spine", f, rot=(0, 3 * pk.wave(f, n, 0.0), 1.5 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.015 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        k.key("Neck", f, rot=(0, -4 * pk.wave(f, n, 0.0), 0))
        k.key("Head", f, rot=(0, -2 * pk.wave(f, n, 0.0), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        pearl(k, f, (0, 0, 0.03 * pk.wave(f, n, 0, 2)))
    return cm.quad_walk(k, n, 0.14, 0.09, body, gait="trot")


FLY_N = 36


def fly_pose(k, f, n=FLY_N):
    """wingless swimming flight: vertical waves travel from the chest to the tail tip, the head stays level, the legs
    make small grasping strokes, the pearl rides along by the cheek"""
    u = f / n
    waves(k, f, n, pitch=5.0, yaw=2.5, cycles=1, lag=0.12, base=[(0, 0)] + [(1.5, 0)] * 8, start=1)
    k.key("Spine", f, rot=(-3 + 4 * math.sin(2 * math.pi * u), 0, 0),
          loc=(0, 0, LIFT + 0.05 * math.sin(2 * math.pi * (u - 0.1))))
    k.key("Neck", f, rot=(6 - 4 * math.sin(2 * math.pi * (u - 0.08)), 0, 0))
    k.key("Head", f, rot=(-2 + 2 * math.sin(2 * math.pi * (u - 0.16)), 0, 0))
    k.key("Jaw", f, rot=(4, 0, 0))
    legs_fk(k, f, front=40, hind=55, paddle=18, ph=u)
    pearl(k, f, (0.02, -0.04, 0.04 * math.sin(2 * math.pi * u)))


def fly(k):
    k.new_action("fly", FLY_N, True)
    for f in range(0, FLY_N + 1):
        fly_pose(k, f)
    k.finish()


def takeoff(k):
    """crouches low, springs up off all four legs (launch at frame 11), the body whips into the swimming wave."""
    import bpy
    n = 27
    k.new_action("takeoff", n, False)
    for f, z, p in ((0, 0, 0), (6, -0.08, 4), (10, -0.10, 6), (13, 0.18, -3), (18, LIFT + 0.05, -3)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        waves(k, f, n, pitch=5 if f >= 13 else 0, cycles=1, lag=0.12, start=1)
        k.key("Neck", f, rot=(6 if f < 11 else 12, 0, 0))
        k.key("Head", f, rot=(0, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        pearl(k, f, (0, 0, 0))
    fly_pose(k, n)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, 13):
        sc.frame_set(f)
        solve(k, f)
    for f, t in ((15, 0.5), (21, 0.85)):
        legs_fk(k, f, front=40 * t, hind=55 * t, paddle=0)
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """glides in on the wave, the front swings up and the legs reach down, touches (frame 16), absorbs, settles."""
    import bpy
    n = 27
    k.new_action("land", n, False)
    fly_pose(k, 0)
    for f, z, p in ((8, LIFT * 0.7, -3), (13, 0.10, -2), (16, -0.05, 2), (20, -0.07, 2), (27, 0, 0)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        waves(k, f, n, pitch=3 if f <= 13 else 0, cycles=1, lag=0.12, start=1)
        k.key("Neck", f, rot=(8 if f < 16 else 0, 0, 0))
        k.key("Head", f, rot=(0, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        pearl(k, f, (0, 0, 0))
    legs_fk(k, 8, front=-4, hind=0, paddle=0)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(16, n + 1):
        sc.frame_set(f)
        solve(k, f)
    k.finish(loop=False)
    k.events["land"] = {"touch": round(16 / n, 3)}


def roar(k):
    """S-COIL STRIKE: draws the neck and chest back into a tight S, claws raised, mane bristling; then STRIKES forward
    and up with the jaw wide, holds the roar, settles."""
    import bpy
    n = 60
    k.new_action("roar", n, False)
    for f, sp, z, y, b1, nk, hd, jw, pz in ((0, 0, 0, 0, 0, 0, 0, 0, 0), (8, -6, 0.04, 0.03, 4, -14, 12, 0, 0.0),
                                           (18, -14, 0.10, 0.06, 10, -34, 34, 0, 0.06),
                                           (24, 2, 0.06, -0.10, -4, 14, -10, 36, 0.12),
                                           (42, 2, 0.06, -0.10, -4, 16, -12, 38, 0.12), (52, 0, 0.0, 0, 0, 2, 0, 4, 0.02),
                                           (n, 0, 0, 0, 0, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, y, z))
        k.key("Body1", f, rot=(b1, 0, 0))
        k.key("Body2", f, rot=(-b1 * 0.6, 0, 0))
        for bn in ("Body3", "Body4", "Body5"):
            k.key(bn, f, rot=(0, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        pearl(k, f, (0.0, 0.0, pz))
    for f in range(0, n + 1, 2):                             # the tail lashes through the strike
        lash = 14 * math.sin(2 * math.pi * f / 20) * ease((f - 10) / 8) * (1 - ease((f - 46) / 8))
        for i, bn in enumerate(("Tail1", "Tail2", "Tail3")):
            k.key(bn, f, rot=(0, lash * (0.6 + 0.4 * i), 0))
    for f in range(26, 42, 2):
        k.key("Jaw", f, rot=(36 + (3 if (f // 2) % 2 else -3), 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        solve(k, f, HIND)
        if 6 <= f <= 54:                                     # claws raised while coiled, reaching on the strike
            u = ease((f - 6) / 8) * (1 - ease((f - 46) / 8))
            for leg in FRONT:
                side = leg[4:]
                s = 1 if side.endswith("L") else -1
                k.key(leg, f, rot=(-34 * u, 0, -s * 10 * u))
                k.key("Shin_" + side, f, rot=(40 * u, 0, 0))
                k.key("Foot_" + side, f, rot=(30 * u, 0, 0))
        else:
            solve(k, f, FRONT)
    k.finish(loop=False)


def pearlchase(k):
    """SIGNATURE - CHASE THE PEARL: the pearl darts up and away; the dragon rises after it into the air, its long body
    curving as it whirls one full corkscrew turn chasing the pearl round and round, the head stretched after it; the
    front claw SNATCHES the pearl and the jaws snap beside it; it sinks back down with a wave rolling to the tail tip,
    the pearl back at its cheek."""
    import bpy
    n = 100
    k.new_action("act_pearlchase", n, False)

    def air(f):
        return ease((f - 8) / 16) * (1 - ease((f - 72) / 16))

    def spin(f):
        return 360.0 * ease((f - 24) / 38)

    for f in range(0, n + 1, 2):
        a = air(f)
        sp = spin(f)
        q = Quaternion((0, 0, 1), math.radians(sp))
        cm.key_axis(k, "Spine", f, (1, 0, 0), -6 * a, loc=(0, 0, 0.32 * a), extra=q)
        whirl = math.sin(math.pi * min(1.0, max(0.0, (f - 24) / 38)))           # the body trails the turn
        for i, bn in enumerate(CHAIN[1:], 1):
            wv = 5 * math.sin(2 * math.pi * (f / 24 - 0.1 * i)) * a
            k.key(bn, f, rot=((2 if i <= 3 else 0) * a + wv * 0.4, -16 * whirl + wv, 0))
        k.key("Neck", f, rot=(-14 * a, 10 * whirl, 0))
        k.key("Head", f, rot=(10 * a, 14 * whirl, 0))
    for f in range(74, n + 1, 2):                                # the wave rolling out to the tail tip
        w = (1 - ease((f - 76) / 22))
        for i, bn in enumerate(CHAIN[1:], 1):
            k.key(bn, f, rot=(2 * w * math.sin(2 * math.pi * ((f - 74) / 16 - 0.12 * i)) + 1.0 * w, 0, 0))
    for f, jw in ((0, 0), (24, 8), (58, 8), (61, 30), (64, 0), (67, 26), (70, 0), (n, 0)):
        k.key("Jaw", f, rot=(jw, 0, 0))
    # the pearl: darts up and away to the left, leads the head round the turn (it is carried by the Spine, so it
    # turns with the dragon, kept ahead and to the left), dips down to the right claw (snatched), back to the cheek
    LEAD = Vector((0.95, -0.25, 0.30))
    CLAW = Vector((0.23, 0.56, -1.10))
    WB, WC = Vector((-0.30, 0.48, -1.05)), Vector((-0.45, 0.13, -0.35))
    for f in range(0, n + 1, 2):
        if f <= 12:                                          # darts across in front of the snout, then up-left
            W0, W0b = Vector((0.05, -0.67, -0.05)), Vector((0.95, -0.67, 0.05))
            p = W0 * ease(f / 4) if f <= 4 else W0.lerp(W0b, ease((f - 4) / 4)) if f <= 8 else                 W0b.lerp(LEAD, ease((f - 8) / 4))
        elif f <= 56:
            p = LEAD + Vector((0, 0, 0.06 * math.sin(2 * math.pi * (f - 12) / 22)))
        elif f <= 63:                                        # down the left side, under the jaw, into the claw
            W1, MID = Vector((1.00, -0.12, -0.62)), Vector((0.60, 0.08, -0.82))
            u = (f - 56) / 7
            if u < 0.34:
                p = LEAD.lerp(W1, ease(u / 0.34))
            elif u < 0.67:
                p = W1.lerp(MID, ease((u - 0.34) / 0.33))
            else:
                p = MID.lerp(CLAW, ease((u - 0.67) / 0.33))
        elif f <= 76:
            p = CLAW
        elif f <= 81:                                        # out to the right under the whisker, round its tip,
            p = CLAW.lerp(WB, ease((f - 76) / 5))           # then up the outside back to the cheek
        elif f <= 87:
            p = WB.lerp(WC, ease((f - 81) / 6))
        else:
            p = WC * (1 - ease((f - 87) / 7))
        pearl(k, f, tuple(p))
    for f in (1, 3, 5, 7, 9, 11):
        W0, W0b = Vector((0.05, -0.67, -0.05)), Vector((0.95, -0.67, 0.05))
        p = W0 * ease(f / 4) if f <= 4 else W0.lerp(W0b, ease((f - 4) / 4)) if f <= 8 else W0b.lerp(LEAD, ease((f - 8) / 4))
        pearl(k, f, tuple(p))
    for f in (77, 79, 83, 85, 89, 91):
        p = CLAW.lerp(WB, ease((f - 76) / 5)) if f <= 81 else WB.lerp(WC, ease((f - 81) / 6)) if f <= 87 else             WC * (1 - ease((f - 87) / 7))
        pearl(k, f, tuple(p))
    for f in (57, 59, 61):
        u = (f - 56) / 7
        W1, MID = Vector((1.00, -0.12, -0.62)), Vector((0.60, 0.08, -0.82))
        p = LEAD.lerp(W1, ease(u / 0.34)) if u < 0.34 else W1.lerp(MID, ease((u - 0.34) / 0.33)) if u < 0.67 else             MID.lerp(CLAW, ease((u - 0.67) / 0.33))
        pearl(k, f, tuple(p))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        a = air(f)
        if a < 0.03:
            solve(k, f)
            continue
        for leg in LEGS4:                                    # airborne: legs drawn up and paddling; the right claw snatches
            side = leg[4:]
            s = 1 if side.endswith("L") else -1
            fr = leg[4] == "F"
            b = min(1.0, a * 1.5)
            if leg == "Leg_FR" and 54 <= f <= 80:
                g = ease((f - 54) / 6) * (1 - ease((f - 74) / 6))
                k.key(leg, f, rot=(b * 30 - 75 * g, 0, -s * 8 * b))
                k.key("Shin_FR", f, rot=(b * 30 + 10 * g, 0, 0))
                k.key("Foot_FR", f, rot=(b * 26 + 20 * g, 0, 0))
                continue
            w = math.sin(2 * math.pi * (f / 20 + (0.0 if fr else 0.5) + (0.0 if s > 0 else 0.25)))
            k.key(leg, f, rot=(b * ((30 if fr else 45) + 12 * w), 0, -s * 8 * b))
            k.key("Shin_" + side, f, rot=(b * (30 + 8 * w), 0, 0))
            k.key("Foot_" + side, f, rot=(b * 26, 0, 0))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    pearlchase(k)
    return stride


HEAD_XF = []
