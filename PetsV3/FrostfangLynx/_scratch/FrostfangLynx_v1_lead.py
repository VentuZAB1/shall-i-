# Frostfang Lynx (Glacier egg, STARTER 50 %) - FIERCE style (2026-10-27, Glacier update batch 1).
# Plan: _review/FrostfangLynx_plan.md (v2) + review _review/GLACIER_PLAN_REVIEW.md 2.1.
# A lean ice lynx: compact body on long legs, big snowshoe paws with smooth icy claws, a sand-silver coat covered in
# dark rosette spots, a darker saddle, snow-white underside + flared cheek ruff (the lynx "beard"), tall ears with
# ice-tipped tufts, narrow ice-cyan slit eyes under heavy brows, a short bobtail with a black tip.
import math
from mathutils import Vector, Euler

DISPLAY = "Frostfang Lynx"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.0                  # total height (ear-tuft tips) in studs at x1

WARM_SILVER = (190, 172, 150)  # body / legs / head sides (studded)
BACK_SHADE = (126, 116, 110)   # saddle, brows, ear backs, rosette spots (>= 20 % of the side view)
SNOW = (240, 244, 250)         # underside, muzzle, cheek ruff, paw socks, ear fronts
ICE = (150, 236, 255)          # THE accent: eye slits, tuft tips
ICE_CLAW = (214, 244, 255)     # claws (smooth)
BLACK = (14, 14, 22)
MOUTH = (86, 18, 30)
TEETH = (238, 234, 220)

PITCH = 0.034                  # ~0.08 x torso height

# leg joints (left side): shoulder/hip, elbow/knee, wrist/ankle, paw centre (long cat legs, withers ~0.80)
LEGS = {"F": ((0.112, -0.30, 0.60), (0.115, -0.24, 0.345), (0.118, -0.29, 0.095), (0.118, -0.335, 0.040)),
        "B": ((0.108, 0.30, 0.62), (0.112, 0.18, 0.39), (0.115, 0.37, 0.16), (0.115, 0.32, 0.040))}
TAILP = [(0, 0.44, 0.74), (0, 0.55, 0.70), (0, 0.65, 0.635), (0, 0.72, 0.565)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def prof(b, lz):
    t = (lz / b.h.z + 1) / 2
    fx = b.bot[0] + (b.top[0] - b.bot[0]) * t
    fy = b.bot[1] + (b.top[1] - b.bot[1]) * t
    return b.h.x * fx, b.h.y * fy, b.ts[1] * t


def side_pt(b, s, ly, lz, off=0.006):
    """point on the +-x flank of tapered block b at local (ly, lz) + the flank normal"""
    hx, _, oy = prof(b, lz)
    p = b.world(Vector((s * (hx + off), ly + oy, lz)))
    dx = b.h.x * (b.top[0] - b.bot[0]) / (2 * b.h.z)
    return p, (b.R @ Vector((s, 0, -dx))).normalized()


def spot(B, b, s, ly, lz, r=0.030, ang=0.0, ring=False):
    """a dark lynx spot on a flank: a short fat flush bar (solid) or a broken ring (rosette)"""
    p, nrm = side_pt(b, s, ly, lz, off=0.004)
    up = Vector((0, 0, 1))
    u = (up - nrm * up.dot(nrm)).normalized()
    v = nrm.cross(u).normalized()
    if not ring:
        a = math.radians(ang)
        t = u * math.cos(a) + v * math.sin(a)
        B.bar(p - t * r * 0.6, p + t * r * 0.6, nrm, r * 1.15, 0.007, BACK_SHADE, b.bone, studs=[], bevel=0.003)
        return
    for i in range(4):
        a = math.radians(ang + 90 * i)
        c = p + (u * math.cos(a) + v * math.sin(a)) * r
        t = (-u * math.sin(a) + v * math.cos(a))
        B.bar(c - t * r * 0.55, c + t * r * 0.55, nrm, 0.026, 0.007, BACK_SHADE, b.bone, studs=[], bevel=0.003)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=271, tier=3, plates=False)
    # ---------------- torso: compact deep chest, strong tuck, narrow waist, high hips (lynx: hind legs longer)
    rib = B.add((0, -0.19, 0.615), (0.150, 0.235, 0.195), WARM_SILVER, "Chest", bot=(0.62, 0.52), top=(0.88, 0.92),
                rnd=0.30)
    B.seg((0, -0.06, 0.44), (0, 0.20, 0.545), 0.092, 0.055, WARM_SILVER, "Spine", top=(0.82, 0.75), side=(1, 0, 0))
    waist = B.add((0, 0.08, 0.668), (0.118, 0.16, 0.112), WARM_SILVER, "Spine", bot=(0.72, 0.70), top=(0.95, 1),
                  rnd=0.30)
    hips = B.add((0, 0.30, 0.672), (0.132, 0.155, 0.132), WARM_SILVER, "Spine", rot=(-6, 0, 0), top=(0.84, 0.90),
                 bot=(0.85, 0.9), rnd=0.30)
    # darker saddle along the top line: withers -> waist -> rump
    for a, b, bone in (((0, -0.30, 0.810), (0, -0.08, 0.800), "Chest"), ((0, -0.08, 0.800), (0, 0.10, 0.780), "Spine"),
                       ((0, 0.10, 0.780), (0, 0.33, 0.800), "Spine")):
        B.seg(a, b, 0.072, 0.014, BACK_SHADE, bone, side=(1, 0, 0), ext=0.012, ext1=0.012, top=(0.95, 1), rnd=0.3)
    # snow underside following the tuck + snow chest front / throat
    B.add((0, -0.20, 0.425), (0.078, 0.12, 0.02), SNOW, "Chest", bot=(0.8, 0.9), studs=[])
    B.seg((0, -0.06, 0.428), (0, 0.18, 0.528), 0.062, 0.018, SNOW, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    B.add((0, -0.415, 0.62), (0.098, 0.025, 0.12), SNOW, "Chest", bot=(0.5, 1), top=(0.9, 1), rot=(-12, 0, 0))
    # ---------------- neck (40 deg up) + round head with a short muzzle
    B.seg((0, -0.34, 0.69), (0, -0.53, 0.86), 0.090, 0.100, WARM_SILVER, "Neck", ext=0.05)
    B.seg((0, -0.39, 0.63), (0, -0.56, 0.80), 0.068, 0.055, SNOW, "Neck", side=(1, 0, 0), ext=0.02)    # snow throat
    B.add((0, -0.615, 0.935), (0.098, 0.085, 0.082), WARM_SILVER, "Head", top=(0.84, 0.86), bot=(0.9, 0.95), rnd=0.42)
    B.add((0, -0.60, 1.012), (0.068, 0.058, 0.012), BACK_SHADE, "Head", top=(0.8, 0.8))               # dark crown
    B.seg((0, -0.675, 0.905), (0, -0.765, 0.893), 0.068, 0.040, SNOW, "Head", top=(0.84, 0.84), ext=0.02)  # muzzle
    for sx in (1, -1):                                                                      # whisker pads
        B.add((sx * 0.030, -0.752, 0.872), (0.033, 0.022, 0.016), SNOW, "Head", rnd=0.2)
    B.add((0, -0.772, 0.916), (0.020, 0.010, 0.013), BLACK, "Head", bot=(0.45, 0.8), role="detail", bevel=0.004)
    for s in (1, -1):
        B.spike((s * 0.034, -0.760, 0.858), (0, -0.1, -1), 0.050, 0.011, TEETH, "Head")
    # lower jaw + mouth
    B.seg((0, -0.60, 0.830), (0, -0.752, 0.828), 0.056, 0.020, SNOW, "Jaw", top=(0.8, 1), ext=0.02)
    B.add((0, -0.69, 0.849), (0.038, 0.065, 0.005), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    # narrow ice-cyan slit eyes (black socket, vertical pupil), heavy brows
    for s in (1, -1):
        rot = (0, -s * 18, s * 20)
        B.add((s * 0.050, -0.703, 0.952), (0.036, 0.008, 0.017), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.003)
        B.add((s * 0.051, -0.709, 0.952), (0.030, 0.006, 0.0098), ICE, "Head", rot=rot, studs=[], role="detail",
              bevel=0.002)
        B.add((s * 0.049, -0.7155, 0.952), (0.0058, 0.0035, 0.0108), BLACK, "Head", rot=(0, 0, s * 20), studs=[],
              role="detail", bevel=0.0012)                                                  # vertical cat pupil
        B.add((s * 0.046, -0.688, 0.984), (0.050, 0.022, 0.017), BACK_SHADE, "Head", rot=(0, -s * 20, s * 22),
              role="detail", bevel=0.007)                                                   # heavy brow
    # the lynx beard: flared snow cheek ruff, blades sweeping down and back from the jaw line
    for s in (1, -1):
        for z, dz, L, w in ((0.845, -0.75, 0.105, 0.038), (0.885, -0.45, 0.115, 0.040), (0.925, -0.15, 0.090, 0.034)):
            B.spike((s * 0.082, -0.640, z), (s * 0.62, 0.40, dz), L, w, SNOW, "Head", top=(0.12, 0.40))
    # tall ears with snow fronts and ice tuft tips (blocks only, no strands)
    for s, side in ((1, "L"), (-1, "R")):
        R = Euler((math.radians(-10), math.radians(s * 6), math.radians(-s * 12)), "XYZ").to_matrix()
        root = Vector((s * 0.060, -0.585, 1.000))
        ear = B.add(root + R @ Vector((0, 0, 0.050)), (0.034, 0.014, 0.052), BACK_SHADE, "Ear_" + side, R=R,
                    top=(0.30, 0.6), rnd=0.25)
        B.add(ear.world((0, -0.014, -0.006)), (0.022, 0.004, 0.036), SNOW, "Ear_" + side, R=R, top=(0.35, 1),
              studs=[], role="detail", bevel=0.003)
        tip = root + R @ Vector((0, 0, 0.098))
        B.spike(tip, R @ Vector((0, 0.15, 1)), 0.050, 0.014, ICE, "Ear_" + side, top=(0.1, 0.3))
    # ---------------- legs: long; snowshoe paws (snow socks) with smooth icy claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, Pw = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.07)), K, 0.056, 0.080, WARM_SILVER, leg, ext=0.0, ext1=0.03, top=(0.85, 0.72))
                B.seg(K, A, 0.045, 0.050, WARM_SILVER, shin, top=(0.88, 0.88), ext=0.03, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.03, 0.07)), K, 0.070, 0.115, WARM_SILVER, leg, bot=(0.85, 1), top=(0.75, 0.62),
                      ext=0.0, ext1=0.03)
                B.seg(K, A, 0.047, 0.055, WARM_SILVER, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02)
                B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.040, 0.042, SNOW, foot, ext=0.03)
            B.add(Pw, (0.068, 0.082, 0.040), SNOW, foot, top=(0.86, 0.82))                   # snowshoe paw
            cb = ("Claw_" + fb + side) if fb == "F" else foot
            for gx in (-0.040, -0.014, 0.014, 0.040):
                B.spike((Pw.x + gx, Pw.y - 0.072, 0.032), (0, -1, -0.55), 0.052, 0.012, ICE_CLAW, cb)
    # ---------------- rosette spots on the flanks, shoulders and thighs (>= 20 % of the side view)
    for s in (1, -1):
        for ly, lz, r, a, ring in ((-0.14, 0.07, 0.030, 20, False), (-0.05, -0.04, 0.032, 60, True),
                                   (0.05, 0.08, 0.028, 0, False), (0.12, -0.02, 0.030, 35, False),
                                   (-0.16, -0.08, 0.026, 80, False), (0.16, 0.10, 0.024, 10, False)):
            spot(B, rib, s, ly, lz, r=r, ang=a, ring=ring)
        for ly, lz, r, a, ring in ((-0.08, 0.03, 0.028, 30, False), (0.05, -0.03, 0.030, 70, True),
                                   (0.10, 0.06, 0.024, 0, False)):
            spot(B, waist, s, ly, lz, r=r, ang=a, ring=ring)
        for ly, lz, r, a, ring in ((-0.07, 0.05, 0.028, 15, False), (0.06, -0.02, 0.032, 50, True),
                                   (0.0, -0.08, 0.026, 85, False), (0.09, 0.08, 0.022, 0, False)):
            spot(B, hips, s, ly, lz, r=r, ang=a, ring=ring)
    # ---------------- short bobtail with a black tip band
    P = [Vector(p) for p in TAILP]
    for i, ((a, b), (w, d)) in enumerate(zip(zip(P, P[1:]), ((0.040, 0.050), (0.040, 0.046), (0.036, 0.040)))):
        B.seg(a, b, w, d, BLACK if i == 2 else WARM_SILVER, "Tail%d" % (i + 1), ext=0.03, top=(0.92, 0.92))
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.16, 0.66), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.08, 0.66), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.34, 0.70), "Chest", tail=(0, -0.15, 0.14))
    k.joint("Head", (0, -0.535, 0.865), "Neck", tail=(0, -0.25, 0.0))         # throat pivot
    k.joint("Jaw", (0, -0.605, 0.838), "Head", tail=(0, -0.15, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.060, -0.585, 1.000), "Head", tail=(s * 0.02, 0, 0.1))
        k.joint("Tuft_" + side, (s * 0.066, -0.578, 1.10), "Ear_" + side, tail=(0, 0, 0.05))   # ice dust anchor
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, Pw = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.12, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
            if fb == "F":
                k.joint("Claw_F" + side, (s * Pw.x, Pw.y - 0.05, 0.035), "Foot_F" + side, tail=(0, -0.06, -0.02))
            k.joint("Snow_" + fb + side, (s * Pw.x, Pw.y, 0.02), "Foot_" + fb + side, tail=(0, 0, 0.05))
    for i in range(3):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=tuple(Vector(TAILP[i + 1]) - Vector(TAILP[i])))


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"),
         ("Claw_FL", "Claw_FR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    P += [("Head", "Chest"), ("Jaw", "Chest"), ("Ear_L", "Ear_R")]
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
        P.append(("Tail1", b))
    return P


def joints():
    return [((0, -0.52, 0.84), (0, -0.56, 0.90), 0.13, "Head")]


HEAD_XF = []
