# Nightmare Stallion (Void egg #2) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the dark Friesian"): a real horse
# built from tapered blocks and covered in Roblox studs (blockkit.stud_skin): deep chest tapering to a rising belly
# line, long legs with thin cannons, big dark hooves and flame feathering, a long arched neck, a long narrow horse head
# carried nose-down (cranium + round jowl + long face + soft muzzle with flared nostrils), narrow magenta eyes under a
# heavy brow, bared teeth, 2 short swept-back nightmare horns, a crest of violet flame blades with magenta tips and a
# flame tail falling to the hocks.  Old chibi version: _tools/chibi_specs/NightmareStallion.py
import math
from mathutils import Vector, Euler, Matrix

DISPLAY = "Nightmare Stallion"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 9.0

COAT = (74, 70, 92)           # charcoal-black coat (coordinator 2026-10-09: Void-tier separation from Panther/Dragon)
DARK = (42, 38, 56)           # brows, ear backs, back line
LEGD = (56, 52, 72)           # darker lower legs (Friesian)
UNDER = (122, 116, 144)       # muzzle, throat, chest, belly (lighter charcoal underside)
HOOF = (26, 24, 34)
MANE_D = (196, 30, 150)       # flame mane / tail: deep magenta -> hot pink -> pale-pink tips
MANE = (255, 64, 186)
ACCENT = (255, 168, 228)      # pale hot-pink flame tips, feathering tips
EYE = (255, 60, 200)
EYE_HOT = (255, 190, 238)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
MOUTH = (70, 16, 40)
HORN = (34, 30, 46)

PITCH = 0.041               # stud pitch: 0.042 x (U / U_raiju), U = model height / HEIGHT

# leg joints (left side): H hip/shoulder, K knee/stifle, A fetlock (front) / hock (hind), P hoof centre
LEGS = {"F": ((0.13, -0.36, 0.76), (0.13, -0.385, 0.35), (0.13, -0.36, 0.14), (0.13, -0.385, 0.042)),
        "B": ((0.105, 0.36, 0.84), (0.105, 0.24, 0.57), (0.105, 0.47, 0.37), (0.105, 0.42, 0.042))}
FETLOCK_B = (0.105, 0.455, 0.14)
NECK_A = (Vector((0, -0.42, 0.84)), Vector((0, -0.60, 1.22)))      # lower neck (steep)
NECK_B = (Vector((0, -0.56, 1.16)), Vector((0, -0.78, 1.42)))      # upper neck (arching forward)
HC = Vector((0, -0.90, 1.40))                                       # cranium centre
HR = Euler((math.radians(48), 0, 0), "XYZ").to_matrix()            # head carried 48 deg nose-down
CREST = [Vector((0, -0.30, 1.06)), Vector((0, -0.47, 1.28)), Vector((0, -0.70, 1.48)), Vector((0, -0.80, 1.52))]
TAILP = [(0, 0.60, 0.90), (0, 0.76, 0.92), (0, 0.87, 0.72), (0, 0.90, 0.42)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def hp(p):
    """point in the head's local frame (x side, -y along the face, z = forehead side) -> rest space"""
    return HC + HR @ Vector(p)


def hR(rx=0.0, ry=0.0, rz=0.0):
    return HR @ Euler((math.radians(rx), math.radians(ry), math.radians(rz)), "XYZ").to_matrix()


def flame(B, base, up, back, h, w, t, color, bone, tip_c=None, tip_frac=0.38):
    """flat flame blade standing on a surface (up = surface normal), base length along `back`, tip swept back;
    tip_c = the outer part in the accent colour"""
    up = Vector(up).normalized()
    back = Vector(back)
    back = (back - up * back.dot(up)).normalized()
    R = Matrix((up.cross(back), back, up)).transposed()      # local x = side (thin), y = back, z = up
    blk = B.add(base + up * (h / 2), (t, w, h / 2), color, bone, R=R, top=(0.5, 0.18), top_shift=(0, w * 0.95),
                role="limb")
    if tip_c:
        f = tip_frac
        z0 = h * (1 - f)
        wz = w * (1 - (1 - 0.18) * (1 - f))            # blade half width at the tip block's base
        B.add(base + up * (z0 + h * f / 2) + back * (w * 0.95 * (1 - f / 2)), (t * 1.08, wz, h * f / 2), tip_c, bone,
              R=R, top=(0.6, 0.18 * w / wz), top_shift=(0, w * 0.95 * f), role="limb", studs=[])
    return blk


def eye(B, orb, s, bone="Head", sc=1.0):
    """FIERCE_PLAN eye recipe on the front (-y) face of an orbit block: black socket -> magenta slit -> hot highlight
    on the outer half -> heavy dark brow overhanging slightly"""
    R = orb.R @ Euler((0, math.radians(-s * 18), 0), "XYZ").to_matrix()
    Rb = orb.R @ Euler((0, math.radians(-s * 20), 0), "XYZ").to_matrix()
    c = orb.world((0, -orb.h.y, -0.006))
    B.add(orb.world((-s * 0.004, -orb.h.y + 0.02, orb.h.z * 0.75)), (0.06 * sc, 0.03 * sc, 0.022 * sc), DARK, bone,
          R=Rb, role="detail", bevel=0.01)
    B.add(c, (0.048 * sc, 0.006, 0.023 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + R @ Vector((0.002 * s, -0.004, 0.0)), (0.041 * sc, 0.006, 0.012 * sc), EYE, bone, R=R, studs=[],
          role="detail", bevel=0.003)
    B.add(c + R @ Vector((s * 0.013 * sc, -0.008, 0.002)), (0.018 * sc, 0.004, 0.006 * sc), EYE_HOT, bone, R=R,
          studs=[], role="detail", bevel=0.002)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=139, tier=5, plates=False)
    # ---------------- torso: deep ribcage tapering underneath, sloped tuck up to the flank, rounded croup
    B.add((0, -0.20, 0.79), (0.19, 0.31, 0.235), COAT, "Chest", bot=(0.66, 0.56), top=(0.90, 0.95), rnd=0.30)
    B.add((0, -0.32, 0.99), (0.13, 0.17, 0.055), COAT, "Chest", top=(0.62, 0.75))                    # withers
    B.seg((0, -0.08, 0.60), (0, 0.30, 0.68), 0.14, 0.08, COAT, "Spine", top=(0.85, 0.80), bot=(1, 1), side=(1, 0, 0))
    B.add((0, 0.12, 0.84), (0.142, 0.20, 0.135), COAT, "Spine", bot=(0.75, 0.72), top=(0.95, 1), rnd=0.30)  # waist
    B.add((0, 0.40, 0.83), (0.168, 0.21, 0.175), COAT, "Spine", rot=(-15, 0, 0), top=(0.80, 0.72), bot=(0.82, 0.85),
          rnd=0.38)                                                                                     # sloped croup
    # pale underside: brisket -> sloped belly line (follows the tuck), chest front
    B.add((0, -0.25, 0.552), (0.11, 0.16, 0.022), UNDER, "Chest", bot=(0.8, 0.9), studs=[])
    B.seg((0, -0.09, 0.528), (0, 0.27, 0.622), 0.085, 0.022, UNDER, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    B.add((0, -0.525, 0.79), (0.14, 0.035, 0.15), UNDER, "Chest", rot=(-14, 0, 0), bot=(0.5, 1), top=(0.9, 1))
    # shoulder blades: sloped muscle ridges from the withers down to the point of the shoulder
    for s in (1, -1):
        B.seg((s * 0.150, -0.26, 0.98), (s * 0.165, -0.47, 0.70), 0.04, 0.085, COAT, "Chest", side=(1, 0, 0),
              top=(0.8, 0.9), bot=(0.7, 0.8))
    # ---------------- arched neck (lower steep, upper arching forward) + pale throat
    a, b = NECK_A
    B.seg(a, b, 0.125, 0.17, COAT, "Neck", ext=0.06, ext1=0.03, top=(0.88, 0.85))
    a2, b2 = NECK_B
    B.seg(a2, b2, 0.11, 0.12, COAT, "Neck", ext=0.0, ext1=0.04, top=(0.85, 0.85))
    B.seg((0, -0.54, 0.80), (0, -0.79, 1.27), 0.085, 0.07, UNDER, "Neck", ext=0.0, ext1=0.02, top=(0.85, 1))
    # ---------------- head (pivot at the throat): cranium, round jowl, long face, soft muzzle, closed mouth with
    # bared fangs
    B.add(hp((0, 0, 0)), (0.108, 0.105, 0.092), COAT, "Head", R=HR, top=(0.90, 0.88))               # cranium
    B.add(hp((0, 0.025, -0.105)), (0.115, 0.112, 0.08), COAT, "Head", R=HR, rnd=0.42)                # round jowl
    B.seg(hp((0, -0.05, 0.02)), hp((0, -0.41, -0.01)), 0.086, 0.07, COAT, "Head", top=(0.82, 0.85), ext=0.02)  # face
    B.seg(hp((0, -0.06, -0.075)), hp((0, -0.37, -0.085)), 0.08, 0.058, COAT, "Head", top=(0.92, 0.9), ext=0.02)
    B.add(hp((0, -0.43, -0.05)), (0.08, 0.07, 0.085), UNDER, "Head", R=HR, rnd=0.35, top=(0.9, 0.9))  # muzzle
    for s in (1, -1):                       # flared nostril slits on the muzzle front, outer end up
        B.add(hp((s * 0.044, -0.498, 0.004)), (0.013, 0.006, 0.03), BLACK, "Head", R=hR(0, s * 28, 0),
              studs=[], role="detail", bevel=0.004)
    # upper lip (Lip bone: curls back in the flehmen), mouth line, bared fangs over the lower lip
    B.add(hp((0, -0.475, -0.116)), (0.07, 0.035, 0.019), UNDER, "Lip", R=HR, rnd=0.3, studs=[])
    B.add(hp((0, -0.43, -0.142)), (0.077, 0.07, 0.006), MOUTH, "Head", R=HR, studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike(hp((s * 0.076, -0.43, -0.13)), HR @ Vector((0, -0.12, -1)), 0.06, 0.016, TEETH, "Head")  # fangs
        B.spike(hp((s * 0.07, -0.37, -0.13)), HR @ Vector((0, 0, -1)), 0.04, 0.012, TEETH, "Head")
    # lower jaw (opens in the squeal): pale chin + lower fangs
    B.seg(hp((0, -0.08, -0.165)), hp((0, -0.47, -0.18)), 0.07, 0.035, COAT, "Jaw", top=(0.86, 1), ext=0.02)
    B.add(hp((0, -0.41, -0.182)), (0.064, 0.062, 0.037), UNDER, "Jaw", R=HR, rnd=0.3)                # pale chin
    for s in (1, -1):
        B.spike(hp((s * 0.05, -0.385, -0.15)), HR @ Vector((0, -0.1, 1)), 0.04, 0.012, TEETH, "Jaw")
    # narrow magenta eyes facing FORWARD (counter-rotated against the nose-down head) on orbit wedges at the
    # top corners of the face, under heavy dark brows
    for s in (1, -1):
        Re = hR(-48, 0, s * 32)
        ec = hp((s * 0.088, -0.11, 0.072))
        orb = B.add(ec + Re @ Vector((0, 0.034, 0)), (0.06, 0.034, 0.036), COAT, "Head", R=Re, rnd=0.25)
        eye(B, orb, s, sc=1.15)
    # tall pricked ears (dark backs, deep inner)
    for s, side in ((1, "L"), (-1, "R")):
        root = hp((s * 0.06, 0.07, 0.085))
        ear = B.add(root + Vector((s * 0.012, -0.004, 0.075)), (0.036, 0.022, 0.08), COAT, "Ear_" + side,
                    rot=(6, s * 12, 0), top=(0.10, 0.45))
        B.add(ear.world((0, -0.022, -0.01)), (0.022, 0.005, 0.055), MOUTH, "Ear_" + side, R=ear.R, top=(0.12, 1),
              studs=[], role="detail", bevel=0.004)
    # 2 short swept-back nightmare horns (3 tapered segments) from the forehead, between the ears
    for s in (1, -1):
        h0 = hp((s * 0.05, -0.05, 0.085))
        h1 = h0 + Vector((s * 0.055, 0.045, 0.075))
        h2 = h1 + Vector((s * 0.045, 0.075, 0.06))
        B.seg(h0, h1, 0.032, 0.036, HORN, "Head", ext=0.03, top=(0.8, 0.8))
        B.seg(h1, h2, 0.025, 0.028, HORN, "Head", ext=0.015, top=(0.75, 0.75))
        B.spike(h2, (s * 0.15, 1, 0.55), 0.08, 0.019, HORN, "Head")
    # forelock: flame blades lying down the forehead between the ears
    for x, ln, w in ((0.0, 0.20, 0.05), (0.04, 0.15, 0.04), (-0.04, 0.15, 0.04)):
        p0 = hp((x, 0.07, 0.102))
        p1 = hp((x * 1.4, 0.07 - ln, 0.106))
        B.bar(p0, p1, HR @ Vector((0, 0, 1)), w * 2, 0.012, MANE_D, "Head", top=(1, 0.2))
    # ---------------- mane: flame blades standing on the crest from the poll to the withers, magenta tips
    def crest(t):                           # t 0 = withers .. 1 = poll -> point, forward tangent, up normal
        u = t * 3
        j = min(int(u), 2)
        p = CREST[j].lerp(CREST[j + 1], u - j)
        d = (CREST[j + 1] - CREST[j]).normalized()
        up = Vector((0, d.z, -d.y))
        return p, d, (up if up.z > 0 else -up)
    B.seg(crest(0.10)[0], crest(0.86)[0], 0.06, 0.035, MANE_D, "Mane", side=(1, 0, 0), ext=0.0, ext1=0.0)  # crest
    # standing flame blades, overlapping, swept back ~45 deg, in 2 staggered rows (volume from the front)
    pts = [(0.80, 0.22, 0.085, 0.0), (0.70, 0.32, 0.10, 0.022), (0.61, 0.36, 0.11, -0.022), (0.54, 0.37, 0.11, 0.022),
           (0.41, 0.34, 0.105, -0.022), (0.28, 0.30, 0.10, 0.022), (0.17, 0.24, 0.09, -0.022)]
    for i, (t, h, w, x) in enumerate(pts):
        p, d, up = crest(t)
        a = math.radians(42 if t > 0.35 else 26 if t > 0.22 else 14)
        dirv = up * math.cos(a) - d * math.sin(a)
        flame(B, p - up * 0.04 + Vector((x, 0, 0)), dirv, -d, h, w, 0.034, MANE if i % 2 == 0 else MANE_D, "Mane",
              tip_c=ACCENT)
    # broad flat locks lying down both sides of the neck (the mane reads from the front and the back)
    for s in (1, -1):
        for t, ln, w, ang in ((0.74, 0.22, 0.11, 34), (0.54, 0.30, 0.12, 52), (0.34, 0.26, 0.11, 70)):
            p, d, up = crest(t)
            root = p + Vector((s * 0.085, 0, -0.04))
            a = math.radians(ang)
            end = root + Vector((s * 0.07, math.sin(a), -math.cos(a))).normalized() * ln
            n = Vector((s, 0, 0.45)).normalized()
            B.bar(root, end, n, w, 0.016, MANE_D, "Mane", top=(1, 0.2))
            B.bar(root.lerp(end, 0.62), end + (end - root).normalized() * 0.01, n, w * 0.5, 0.02, ACCENT, "Mane",
                  top=(1, 0.2), studs=[])
    # ---------------- legs: forearm / thigh, thin cannon, fetlock feathering (flame), big dark hoof
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.06)), K, 0.07, 0.09, COAT, leg, ext1=0.03, top=(0.72, 0.62))       # forearm
                B.add(K + Vector((0, -0.005, 0.0)), (0.05, 0.055, 0.05), LEGD, shin, rnd=0.3)               # knee
                B.seg(K, A, 0.042, 0.048, LEGD, shin, ext=0.02, ext1=0.02)                                    # cannon
                F = A
                fb_bone = foot
            else:
                B.seg(H + Vector((0, 0.03, 0.08)), K, 0.068, 0.15, COAT, leg, bot=(0.85, 1), top=(0.75, 0.62),
                      ext1=0.03)                                                                        # thigh
                B.seg(K, A, 0.058, 0.075, COAT, shin, top=(0.80, 0.75), ext=0.03, ext1=0.02)              # gaskin
                B.add(A + Vector((0, 0.01, 0)), (0.05, 0.06, 0.05), COAT, foot, rnd=0.3)                  # hock
                F = Vector(X(FETLOCK_B, s))
                B.seg(A, F, 0.042, 0.048, LEGD, foot, ext=0.02, ext1=0.02)                                # cannon
                fb_bone = foot
            # pastern + fetlock knob + hoof
            B.seg(F + Vector((0, 0, 0.02)), P + Vector((0, 0.0, 0.03)), 0.044, 0.046, LEGD, fb_bone, ext=0.02)
            B.add(P, (0.062, 0.072, 0.042), HOOF, fb_bone, top=(0.80, 0.78), bot=(1, 1), role="limb")
            # feathering: long hair falling over the hoof - dark flame tufts with magenta tips (front, sides, back)
            for dv in ((s * 0.35, -0.35, -1), (s * 0.6, 0.1, -1), (s * 0.2, 0.5, -1)):
                dv = Vector(dv).normalized()
                rad = Vector((dv.x, dv.y, 0)).normalized()
                root = F + rad * 0.035 + Vector((0, 0, 0.03))
                tang = Vector((-rad.y, rad.x, 0))
                flame(B, root, dv, tang, 0.11, 0.03, 0.01, MANE_D, fb_bone, tip_c=ACCENT, tip_frac=0.35)
    # ---------------- flame tail: thick dock, then broad flat flame blades cascading to the hocks
    T = [Vector(p) for p in TAILP]
    B.seg(T[0] + Vector((0, -0.04, -0.02)), T[1], 0.05, 0.055, COAT, "Tail1", ext=0.02)               # dock
    for (a, b), bn, w, c in (((T[0], T[1]), "Tail1", 0.10, MANE_D), ((T[1], T[2]), "Tail2", 0.12, MANE),
                             ((T[2], T[3]), "Tail3", 0.11, MANE_D)):
        d = (b - a).normalized()
        B.seg(a, b, 0.035, w, c, bn, side=(1, 0, 0), ext=0.04, top=(1, 0.75) if bn != "Tail3" else (1, 0.2))
    for t, ln, ang, c in ((0.3, 0.22, 35, MANE), (0.7, 0.24, 15, MANE_D)):          # strands flicking back
        p = T[1].lerp(T[2], t)
        dv = Vector((0, math.cos(math.radians(ang)), -math.sin(math.radians(ang))))
        flame(B, p, Vector((0, 1, 0.2)), (0, 0, -1), ln, 0.07, 0.03, c, "Tail2", tip_c=ACCENT)
    tip = T[3]
    B.seg(tip + Vector((0, -0.01, 0.10)), tip + Vector((0, 0.04, -0.06)), 0.032, 0.07, ACCENT, "Tail3",
          side=(1, 0, 0), top=(1, 0.1), ext=0.0)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.36, 0.84), "Root", tail=(0, -0.4, 0))             # at the hind hips: rearing pivots here
    k.joint("Chest", (0, -0.06, 0.82), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", tuple(NECK_A[0] + Vector((0, 0.02, 0.04))), "Chest", tail=tuple(NECK_B[1] - NECK_A[0]))
    k.joint("Head", tuple(hp((0, 0.085, -0.13))), "Neck", tail=tuple(HR @ Vector((0, -0.35, 0))))   # throat pivot
    k.joint("Jaw", tuple(hp((0, -0.08, -0.15))), "Head", tail=tuple(HR @ Vector((0, -0.3, 0))))
    k.joint("Lip", tuple(hp((0, -0.44, -0.135))), "Head", tail=tuple(HR @ Vector((0, -0.1, 0))))
    k.joint("Mane", tuple(CREST[1] + Vector((0, 0.02, -0.06))), "Neck", tail=(0, -0.2, 0.2))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, tuple(hp((s * 0.06, 0.07, 0.085))), "Head", tail=(0, 0, 0.2))
        for fb, parent, knee in (("F", "Chest", (0, -1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2", tail=(0, 0.02, -0.2))


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR")]
    for a in ("Head", "Jaw", "Lip", "Neck"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    P += [("Head", "Chest"), ("Jaw", "Chest"), ("Lip", "Chest"), ("Jaw", "Neck"), ("Mane", "Chest"), ("Mane", "Head"),
          ("Ear_L", "Mane"), ("Ear_R", "Mane"), ("Ear_L", "Ear_R"), ("Lip", "Jaw")]
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
        P.append(("Tail3", b))
        P.append(("Tail2", b))
    return P


def joints():
    """the deep neck root overlaps the shoulders inside the chest; the jowl hides the throat hinge"""
    b = NECK_A[0]
    return [(b, b, 0.30, "Neck"), (hp((0, 0.085, -0.13)), hp((0, 0.085, -0.13)), 0.16, "Head"),
            (hp((0, -0.10, -0.16)), hp((0, 0.04, -0.15)), 0.09, "Head")]          # jaw root hidden in the jowl


# ------------------------------------------------------------------ animation (FIERCE_PLAN NightmareStallion)
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]


def ease(u):
    u = max(0.0, min(1.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)


def ears(k, f, pin=0.0, turn_l=0.0, turn_r=None):
    """pin + = ears pinned back; turn + = the ear opening turns outward/back"""
    turn_r = turn_l if turn_r is None else turn_r
    k.key("Ear_L", f, rot=(-pin, turn_l, 0))
    k.key("Ear_R", f, rot=(-pin, -turn_r, 0))


def solve_planted(k, f, legs=LEGS4):
    for leg in legs:
        k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


def idle(k):
    """HIP-SHOT FLEHMEN: rests the right hind hoof on its toe (hip dropped), swishes its tail, ears turn; 66-100 the
    flehmen: lifts its head 30 deg and curls the upper lip back, holds, relaxes."""
    import bpy
    n = 120
    k.new_action("idle", n, True)

    def rest(f):
        return ease((f - 2) / 14) * (1 - ease((f - 102) / 14))

    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        r = rest(f)
        k.key("Spine", f, rot=(0, 0, -2.5 * r), loc=(0, 0, 0.006 * b - 0.016 * r))
        k.key("Chest", f, rot=(-0.6 * b, 0, 2.0 * r))
        sw = 0.0
        for c in (18, 44):
            if c <= f <= c + 16:
                sw = 30 * math.sin(2 * math.pi * (f - c) / 16)
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(2 * i, sw * (0.5 + 0.35 * i) + 3 * pk.wave(f, n, 0.1 * i, 2), 0))
        fl = ease((f - 62) / 10) * (1 - ease((f - 98) / 10))
        k.key("Mane", f, rot=(0.8 * b + 3 * fl, 0, 1.2 * pk.wave(f, n, 0.2, 2)))
    for f, nk, hd, yaw, jw, lip in ((0, 0, 0, 0, 0, 0), (14, 0, 0, 0, 0, 0), (22, -2, 2, 16, 0, 0), (40, -2, 2, 16, 0, 0),
                                    (48, 0, 0, 0, 0, 0), (62, 0, 0, 0, 0, 0), (72, -13, -16, 0, 2, 0),
                                    (78, -14, -17, 0, 7, -38), (94, -14, -17, 0, 7, -40), (100, -11, -14, 0, 2, -6),
                                    (108, 0, 0, 0, 0, 0), (n, 0, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Lip", f, rot=(lip, 0, 0))
    for f, pin, l, r in ((0, 0, 0, 0), (24, 0, 0, 0), (27, 0, 34, 0), (36, 0, 34, 0), (39, 0, 0, 0), (52, 0, 0, 0),
                         (55, 0, 0, 30), (60, 0, 0, 30), (63, 0, 0, 0), (74, -8, 0, 0), (96, -8, 0, 0), (104, 0, 0, 0),
                         (n, 0, 0, 0)):
        ears(k, f, pin, l, r)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        r = rest(f)
        for leg in LEGS4:
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if leg == "Leg_BR" and r > 0:
                T = Vector((k.J[leg].x + 0.03 * r, k.J[leg].y - 0.07 * r, 0.05 * r))
                k.solve_leg(leg, f, T, toe=42 * r)
            else:
                k.solve_leg(leg, f, T)
    k.finish()
    k.meta["planted"] = ["Leg_FL", "Leg_FR", "Leg_BL"]


def walk(k):
    """high-stepping prance (trot with lifted knees), head carried high, mane and tail flowing."""
    n = 26

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 1.0 * pk.wave(f, n, 0.0), 1.5 * pk.wave(f, n, 0.0)),
              loc=(0, 0, 0.03 * b))
        k.key("Chest", f, rot=(-1.5 * pk.wave(f, n, 0.15, 2), 0, -1.2 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(-4 + 3 * pk.wave(f, n, 0.2, 2), 0, 0))
        k.key("Head", f, rot=(3 - 3 * pk.wave(f, n, 0.3, 2), 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        k.key("Lip", f, rot=(0, 0, 0))
        k.key("Mane", f, rot=(1 + 3 * pk.wave(f, n, 0.3, 2), 0, 2.5 * pk.wave(f, n, 0.2)))
        ears(k, f, -6)
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(12 - 3 * i + 4 * pk.wave(f, n, 0.2 + 0.1 * i, 2), 6 * pk.wave(f, n, 0.3 + 0.1 * i), 0))
    return cm.quad_walk(k, n, 0.16, 0.15, body, gait="trot")


def roar(k):
    """SQUEAL & BUCK: pins its ears and squeals with the neck arched and the jaw open, then drops its head and BUCKS,
    kicking both hind legs high behind (rump up 0.15), lands and settles."""
    import bpy
    n = 60
    k.new_action("roar", n, False)
    P = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (6, 0, -0.02, 0, -6, -4, 2, 0, 0, 10),
         (12, 0, 0.0, -2, -4, -14, 26, -5, 8, 40), (22, 0, 0.0, -2, -5, -15, 28, -5, 8, 40),
         (28, 5, -0.03, 2, 14, 4, 4, 2, 0, 40), (34, 12, 0.15, 0, 16, 4, 2, -8, 40, 40),
         (40, 10, 0.12, 0, 15, 4, 2, -6, 34, 30), (46, 0, -0.03, 0, 6, 2, 0, 3, 6, 10), (52, 0, 0.0, 0, 0, 0, 0, 0, 0, 0),
         (n, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
    for f, sp, z, ch, nk, hd, jw, mp, tl, pin in P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Lip", f, rot=(-jw * 0.4, 0, 0))
        k.key("Mane", f, rot=(mp, 0, 0))
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(tl * (1 - 0.3 * i), 0, 0))
        ears(k, f, pin)
    for f in range(13, 23, 2):
        k.key("Jaw", f, rot=(27 + (3 if (f // 2) % 2 else -3), 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        solve_planted(k, f, ["Leg_FL", "Leg_FR"])
        if 31 <= f <= 43:
            u = ease((f - 29) / 5) * (1 - ease((f - 39) / 5))
            for side in ("BL", "BR"):
                k.key("Leg_" + side, f, rot=(62 * u, 0, 0))
                k.key("Shin_" + side, f, rot=(-30 * u, 0, 0))
                k.key("Foot_" + side, f, rot=(26 * u, 0, 0))
        else:
            solve_planted(k, f, ["Leg_BL", "Leg_BR"])
    k.finish(loop=False)


def rear(k):
    """SIGNATURE - REAR & STRIKE: gathers its haunches, REARS up 50 deg on its hind legs with the mane streaming,
    strikes the air 3 times with alternating front hooves while whinnying, crashes down onto its front hooves."""
    import bpy
    n = 95
    k.new_action("act_rear", n, False)
    P = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (10, 4, -0.05, 2, 8, 4, 0, 0, -4, 10), (14, 4, -0.06, 2, 8, 4, 0, 0, -4, 10),
         (24, -44, -0.06, -4, 20, -6, 12, -14, 32, 30), (30, -52, -0.05, -4, 24, -8, 18, -18, 38, 35),
         (45, -50, -0.05, -4, 23, -9, 18, -16, 36, 35), (60, -51, -0.05, -4, 24, -8, 18, -18, 38, 35),
         (66, -14, -0.01, 0, 10, 2, 8, -6, 14, 20), (70, 5, -0.06, 4, 6, 4, 4, 0, 8, 10),
         (78, 0, -0.01, 0, 0, 0, 0, 2, 0, 0), (n, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
    for f, sp, z, ch, nk, hd, jw, mp, tl, pin in P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Lip", f, rot=(-jw * 0.4, 0, 0))
        k.key("Mane", f, rot=(mp, 0, 0))
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(tl * (1 - 0.25 * i), 0, 0))
        ears(k, f, pin)
    for f in range(32, 60, 2):                                   # whinny: the jaw quivers, the mane streams
        k.key("Jaw", f, rot=(18 + (3 if (f // 2) % 2 else -3), 0, 0))
        k.key("Mane", f, rot=(-17 + 3 * math.sin(2 * math.pi * f / 8), 3 * math.sin(2 * math.pi * f / 11), 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        solve_planted(k, f, ["Leg_BL", "Leg_BR"])
        if 17 <= f <= 65:
            if f <= 26 or f >= 60:                               # tuck while rising / reach down to land
                u = ease((f - 14) / 10) if f <= 26 else 1 - ease((f - 60) / 5)
                for side in ("FL", "FR"):
                    k.key("Leg_" + side, f, rot=(-30 * u, 0, 0))
                    k.key("Shin_" + side, f, rot=(105 * u, 0, 0))
                    k.key("Foot_" + side, f, rot=(30 * u, 0, 0))
            else:                                                # 3 strikes each, alternating hooves
                for side, ph in (("FL", 0.0), ("FR", 0.5)):
                    w = math.sin(2 * math.pi * ((f - 26) / 12 + ph))
                    st = max(0.0, w)
                    k.key("Leg_" + side, f, rot=(-30 - 34 * st, 0, 0))
                    k.key("Shin_" + side, f, rot=(105 - 75 * st, 0, 0))
                    k.key("Foot_" + side, f, rot=(30 - 20 * st, 0, 0))
        else:
            solve_planted(k, f, ["Leg_FL", "Leg_FR"])
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    rear(k)
    return stride


HEAD_XF = []
