# Thunder Rex (Storm egg SECRET, 2026-10-14, owner lineup "T-rex, crackling back spines") - FIERCE style: a real
# tyrannosaur built from tapered blocks and covered in Roblox studs (blockkit.stud_skin), modelled on the owner's
# reference f_71 (a dark studded secret dino with bright accents): horizontal body balanced over two huge drumstick
# legs, a massive boxy skull with a heavy brow, small slit eyes, rows of fangs, tiny two-claw arms, a long thick tail.
# Storm look: dark slate body, pale belly, electric-cyan lightning scars on the flanks/thighs/tail and two-tone back
# spines (dark base, cyan tip) from the skull to the tail. No glow (sparks = Studio VFX).
import math
from mathutils import Vector

DISPLAY = "Thunder Rex"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 9.0

# Roblox renders colours ~0.6x darker -> pick them brighter than the in-game look
BODY = (98, 106, 140)        # storm slate (reads dark charcoal-blue in game)
BODY_D = (54, 58, 84)        # back saddle, brows, spine bases, toes
BELLY = (182, 188, 208)      # throat, belly, tail underside
BELLY_D = (146, 152, 178)    # belly grooves
BOLT = (60, 222, 255)        # electric cyan accent
BOLT_HOT = (200, 250, 255)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
MOUTH = (86, 18, 30)
CLAW = (26, 26, 36)

H_MODEL = 1.62
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

# leg joints (left side): hip, knee (forward), ankle (back), toe
HIP, KNEE, ANKLE, TOE = (0.22, 0.30, 0.90), (0.25, 0.04, 0.55), (0.23, 0.30, 0.22), (0.23, 0.12, 0.035)
SHOULDER, ELBOW, HAND = (0.21, -0.40, 0.90), (0.26, -0.47, 0.76), (0.23, -0.58, 0.79)
TAILP = [(0, 0.52, 1.02), (0, 0.92, 0.99), (0, 1.32, 0.92), (0, 1.70, 0.83), (0, 2.06, 0.74)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def zig(B, pts, n, width, bone, thick=0.012):
    """flat cyan lightning scar along pts on a surface with normal n, last segment pointed"""
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        B.bar(a, b, n, width, thick, BOLT, bone, studs=[], bevel=0.005,
              top=(1, 0.12) if i == len(pts) - 2 else (1, 1))


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=31, tier=4, plates=False)
    # ---------------- torso: deep barrel ribcage (front a bit higher), tucked belly line rising to the hips
    B.add((0, -0.16, 1.01), (0.25, 0.31, 0.27), BODY, "Chest", rot=(-6, 0, 0), bot=(0.64, 0.58), top=(0.86, 0.90),
          rnd=0.32)                                                                                  # ribcage
    B.add((0, 0.24, 1.01), (0.215, 0.25, 0.235), BODY, "Spine", rot=(5, 0, 0), bot=(0.72, 0.70), top=(0.86, 0.9),
          rnd=0.32)                                                                                  # hips
    B.add((0, 0.02, 1.27), (0.15, 0.42, 0.03), BODY_D, "Chest", rot=(-3, 0, 0), top=(0.7, 0.9))           # dark saddle
    B.seg((0, -0.30, 0.765), (0, 0.24, 0.80), 0.15, 0.03, BELLY, "Chest", side=(1, 0, 0), top=(0.7, 0.9), ext=0.03)
    for t, w in ((0.15, 0.13), (0.42, 0.12), (0.70, 0.10)):                                          # belly grooves
        p = Vector((0, -0.30, 0.735)).lerp(Vector((0, 0.24, 0.77)), t)
        B.bar(p + Vector((-w, 0, 0)), p + Vector((w, 0, 0)), Vector((0, 0, -1)), 0.022, 0.008, BELLY_D, "Chest",
              studs=[], bevel=0.003)
    B.add((0, -0.455, 0.93), (0.13, 0.03, 0.12), BELLY, "Chest", rot=(18, 0, 0), bot=(0.6, 1), top=(0.9, 1))  # chest
    # ---------------- thick short neck + pale throat
    B.seg((0, -0.38, 1.10), (0, -0.64, 1.30), 0.165, 0.175, BODY, "Neck", ext=0.06, top=(0.92, 0.9))
    B.seg((0, -0.46, 0.97), (0, -0.70, 1.17), 0.12, 0.06, BELLY, "Neck", side=(1, 0, 0), ext=0.02)
    # ---------------- head (throat pivot): massive boxy skull, deep snout, heavy brow, small slit eyes, fangs
    B.add((0, -0.80, 1.40), (0.185, 0.18, 0.16), BODY, "Head", top=(0.80, 0.84), rnd=0.25)                 # skull
    B.add((0, -0.78, 1.565), (0.13, 0.14, 0.025), BODY_D, "Head", top=(0.75, 0.8))                        # dark crown
    for s in (1, -1):                                                                                   # jaw muscles
        B.add((s * 0.165, -0.72, 1.33), (0.05, 0.10, 0.11), BODY, "Head", top=(0.7, 0.8), rnd=0.4)
    B.seg((0, -0.92, 1.37), (0, -1.38, 1.30), 0.145, 0.125, BODY, "Head", top=(0.80, 0.76), ext=0.03)      # snout
    B.seg((0, -0.94, 1.225), (0, -1.36, 1.20), 0.138, 0.032, BODY_D, "Head", top=(0.82, 0.9))             # upper lip
    for s in (1, -1):                                                                                   # nostrils
        B.add((s * 0.05, -1.35, 1.405), (0.018, 0.03, 0.008), BLACK, "Head", rot=(-8, 0, -s * 20), studs=[],
              role="detail", bevel=0.004)
    # upper teeth along the lip, the big fangs in front
    for s in (1, -1):
        B.spike((s * 0.10, -1.29, 1.20), (0, -0.1, -1), 0.095, 0.02, TEETH, "Head")
        for y, L in ((-1.22, 0.065), (-1.15, 0.07), (-1.08, 0.065), (-1.01, 0.06), (-0.95, 0.05)):
            B.spike((s * 0.118, y, 1.20), (0, 0, -1), L, 0.015, TEETH, "Head")
    # lower jaw (opens in the roar): heavy, pale underneath, dark mouth, teeth pointing up
    B.seg((0, -0.74, 1.15), (0, -1.32, 1.15), 0.13, 0.065, BODY, "Jaw", top=(0.80, 1), ext=0.03)
    B.seg((0, -0.76, 1.08), (0, -1.28, 1.10), 0.10, 0.025, BELLY, "Jaw", top=(0.8, 1), ext=0.02)
    B.add((0, -1.04, 1.218), (0.10, 0.24, 0.008), MOUTH, "Jaw", studs=[], role="detail", bevel=0.004)
    for s in (1, -1):
        for y, L in ((-1.26, 0.065), (-1.18, 0.055), (-1.10, 0.055), (-1.02, 0.05), (-0.94, 0.045)):
            B.spike((s * 0.105, y, 1.205), (0, 0, 1), L, 0.014, TEETH, "Jaw")
    # heavy brow ridges + small slanted cyan eye slits + hornlets
    for s in (1, -1):
        B.add((s * 0.125, -0.955, 1.515), (0.08, 0.055, 0.036), BODY_D, "Head", rot=(0, -s * 16, 0), role="detail",
              bevel=0.012)                                                                           # brow
        B.add((s * 0.140, -0.985, 1.462), (0.056, 0.010, 0.026), BLACK, "Head", rot=(0, -s * 16, s * 6), studs=[],
              role="detail", bevel=0.004)                                                            # socket
        B.add((s * 0.142, -0.992, 1.462), (0.047, 0.006, 0.013), BOLT, "Head", rot=(0, -s * 16, s * 6), studs=[],
              role="detail", bevel=0.003)                                                            # slit
        B.add((s * 0.150, -0.996, 1.465), (0.019, 0.004, 0.0065), BOLT_HOT, "Head", rot=(0, -s * 16, s * 6),
              studs=[], role="detail", bevel=0.002)                                                  # hot centre
        B.spike((s * 0.13, -0.92, 1.545), (s * 0.2, 0.5, 1), 0.09, 0.032, BODY_D, "Head", top=(0.15, 0.3))  # hornlet
        for dz, L in ((0.0, 0.10), (-0.06, 0.08)):                                                    # cheek spikes
            B.spike((s * 0.205, -0.70, 1.36 + dz), (s * 0.5, 0.86, -0.1), L, 0.032, BODY_D, "Head", top=(0.15, 0.35))
    # ---------------- tiny two-claw arms
    for s, side in ((1, "L"), (-1, "R")):
        Sh, El, Ha = X(SHOULDER, s), X(ELBOW, s), X(HAND, s)
        B.seg(Sh, El, 0.042, 0.048, BODY, "Arm_" + side, ext=0.03, ext1=0.02, top=(0.85, 0.85))
        B.seg(El, Ha, 0.034, 0.038, BODY, "Hand_" + side, ext=0.02, ext1=0.01, top=(0.9, 0.9))
        for gx in (-0.014, 0.014):
            B.spike(Ha + Vector((s * 0.005 + gx, -0.01, -0.01)), (0, -0.6, -0.8), 0.05, 0.011, CLAW, "Hand_" + side)
    # ---------------- huge drumstick legs: thigh, shin, metatarsus, 3 clawed toes forward + 1 back
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A, T = X(HIP, s), X(KNEE, s), X(ANKLE, s), X(TOE, s)
        B.seg(H + Vector((0, 0.04, 0.12)), K, 0.165, 0.245, BODY, "Leg_" + side, ext=0.0, ext1=0.05,
              top=(0.52, 0.42), rnd=0.50)                                                            # thigh
        B.seg(K, A, 0.085, 0.10, BODY, "Shin_" + side, ext=0.04, ext1=0.03, top=(0.75, 0.75))
        B.seg(A, T + Vector((0, 0, 0.04)), 0.07, 0.07, BODY_D, "Foot_" + side, ext=0.03, top=(0.9, 0.9))
        B.add(T + Vector((0, 0.0, 0.0)), (0.095, 0.09, 0.035), BODY_D, "Foot_" + side)
        for gx, L in ((-0.06, 0.13), (0.0, 0.15), (0.06, 0.13)):
            B.seg(T + Vector((gx, -0.04, 0.03)), T + Vector((gx * 1.4, -0.16, 0.02)), 0.026, 0.024, BODY_D,
                  "Foot_" + side, ext=0.0, top=(0.8, 0.8))                                           # toe
            B.spike(T + Vector((gx * 1.45, -0.165, 0.025)), (gx * 2, -1, -0.45), L * 0.55, 0.02, CLAW, "Foot_" + side)
        B.spike(T + Vector((0, 0.07, 0.03)), (0, 1, -0.4), 0.07, 0.017, CLAW, "Foot_" + side)
        # lightning scar down the outer thigh
        n = Vector((s, 0, 0))
        pts = [H + Vector((s * 0.155, -0.02, 0.06)), H.lerp(K, 0.35) + Vector((s * 0.165, -0.06, 0)),
               H.lerp(K, 0.55) + Vector((s * 0.17, 0.05, 0)), H.lerp(K, 0.85) + Vector((s * 0.15, -0.01, 0))]
        zig(B, pts, n, 0.05, "Leg_" + side)
    # ---------------- lightning scars along the flanks (shoulder -> hip)
    for s in (1, -1):
        n = Vector((s, 0, 0))
        pts = [Vector((s * 0.235, y, z)) for y, z in ((-0.40, 1.12), (-0.24, 0.98), (-0.12, 1.08), (0.06, 0.92))]
        zig(B, pts, n, 0.06, "Chest")
    # ---------------- back spines: dark base + cyan tip, skull -> neck -> back -> tail
    rows = [((0, -0.74, 1.585), 0.13, 64, "Head"), ((0, -0.58, 1.44), 0.16, 66, "Neck"), ((0, -0.46, 1.36), 0.18, 68, "Neck"),
            ((0, -0.32, 1.30), 0.20, 70, "Chest"), ((0, -0.16, 1.29), 0.21, 72, "Chest"), ((0, 0.00, 1.28), 0.20, 74, "Chest"),
            ((0, 0.16, 1.26), 0.19, 76, "Spine"), ((0, 0.32, 1.24), 0.17, 78, "Spine"), ((0, 0.48, 1.18), 0.15, 80, "Spine")]
    for p, L, ang, bone in rows:
        d = Vector((0, math.sin(math.radians(90 - ang)), math.cos(math.radians(90 - ang))))
        base = Vector(p) - d * 0.03
        B.spike(base, d, L * 0.62, 0.065, BODY_D, bone, side=(1, 0, 0), top=(0.55, 0.55))
        B.spike(base + d * L * 0.58, d, L * 0.45, 0.065 * 0.55, BOLT, bone, side=(1, 0, 0), top=(0.12, 0.3),
                nostud=True)
    # ---------------- long thick tail (4 bones), pale underside, spines, cyan scars
    T = [Vector(p) for p in TAILP]
    for i, (hw, tp) in enumerate(((0.19, 0.78), (0.15, 0.74), (0.115, 0.70), (0.08, 0.55))):
        B.seg(T[i], T[i + 1], hw, hw * 0.95, BODY, "Tail%d" % (i + 1), ext=0.12 if i == 0 else 0.05, top=(tp, tp))
        dv = (T[i + 1] - T[i]).normalized()
        dn = dv.cross(Vector((1, 0, 0))).normalized()
        dn = dn if dn.z < 0 else -dn
        B.seg(T[i] + dn * hw * 0.82, T[i + 1] + dn * hw * tp * 0.82, hw * 0.6, hw * 0.22, BELLY, "Tail%d" % (i + 1),
              ext=0.0 if i == 0 else 0.03, top=(tp, tp))                                             # pale underside
        up = -dn
        mid = T[i].lerp(T[i + 1], 0.5) + up * hw * 0.85
        d = (dv * 0.5 + up).normalized()
        L = (0.14, 0.12, 0.10, 0.08)[i]
        B.spike(mid - d * 0.02, d, L * 0.62, hw * 0.34, BODY_D, "Tail%d" % (i + 1), side=(1, 0, 0), top=(0.55, 0.55))
        B.spike(mid + d * L * 0.58, d, L * 0.45, hw * 0.19, BOLT, "Tail%d" % (i + 1), side=(1, 0, 0),
                top=(0.12, 0.3), nostud=True)
        if i < 3:                                                                                   # side scars
            for s in (1, -1):
                n = Vector((s, 0, 0))
                a = T[i].lerp(T[i + 1], 0.2) + Vector((s * hw * 0.98, 0, hw * 0.25))
                b = T[i].lerp(T[i + 1], 0.55) + Vector((s * hw * 0.95, 0, -hw * 0.2))
                c = T[i].lerp(T[i + 1], 0.85) + Vector((s * hw * tp * 0.95, 0, hw * 0.1))
                zig(B, [a, b, c], n, 0.045 * (1 - 0.18 * i), "Tail%d" % (i + 1))
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.24, 1.00), "Root", tail=(0, -0.4, 0.02))
    k.joint("Chest", (0, -0.06, 1.02), "Spine", tail=(0, -0.4, 0.05))
    k.joint("Neck", (0, -0.40, 1.12), "Chest", tail=(0, -0.2, 0.15))
    k.joint("Head", (0, -0.64, 1.24), "Neck", tail=(0, -0.4, 0.0))           # throat pivot
    k.joint("Jaw", (0, -0.76, 1.20), "Head", tail=(0, -0.4, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Arm_" + side, X(SHOULDER, s), "Chest")
        k.joint("Hand_" + side, X(ELBOW, s), "Arm_" + side, tail=(0, -0.1, 0.02))
        k.joint("Leg_" + side, X(HIP, s), "Spine")
        k.joint("Shin_" + side, X(KNEE, s), "Leg_" + side)
        k.joint("Foot_" + side, X(ANKLE, s), "Shin_" + side, tail=(0, -0.15, -0.1))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
    for i in range(4):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=(Vector(TAILP[i + 1]) - Vector(TAILP[i])) if i == 3 else None)


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Head", "Chest"), ("Jaw", "Chest"),
         ("Jaw", "Neck"), ("Head", "Arm_L"), ("Head", "Arm_R"), ("Jaw", "Arm_L"), ("Jaw", "Arm_R"),
         ("Jaw", "Hand_L"), ("Jaw", "Hand_R"), ("Arm_L", "Leg_L"), ("Arm_R", "Leg_R"), ("Hand_L", "Leg_L"),
         ("Hand_R", "Leg_R"), ("Hand_L", "Hand_R")]
    for t in ("Tail2", "Tail3", "Tail4"):
        for b in ("Shin_L", "Shin_R", "Foot_L", "Foot_R"):
            P.append((t, b))
    return P


HEAD_XF = []
