# Bramble Badger (Wood/Grass egg, STARTER 40 %) - FIERCE style (2026-10-27, Glacier update batch 1).
# Plan: _review/BrambleBadger_plan.md (v2) + review _review/GLACIER_PLAN_REVIEW.md 2.7.
# A low, grumpy badger: pale grey back with a darker mantle over the shoulders, a short crest of amber bramble thorns
# down the spine, black belly / legs / side skirt, a white wedge face with the two black badger stripes running
# through narrow amber eyes, long black digging claws on the front paws, a stub tail.
import math
from mathutils import Vector

DISPLAY = "Bramble Badger"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 6.5                # total height (head top) in studs at x1; Mossback 7, Basilisk 8, Stag 11

GREY = (176, 172, 180)      # back / flanks (studded)
MANTLE = (110, 104, 116)    # darker mantle over shoulders + nape (review MUST 1)
BELLY_D = (72, 58, 54)      # belly, legs, side skirt
FACE = (240, 236, 226)      # face, cheeks, ear rims
AMBER = (236, 150, 60)      # THE accent: thorn crest + eye slits
AMBER_HOT = (255, 214, 140)
THORN_D = (120, 70, 36)     # thorn bases
BLACK = (14, 14, 22)
IVORY = (238, 234, 220)
MOUTH = (86, 18, 30)

PITCH = 0.024               # stud pitch: ~0.08 x torso height (TH ~0.30)

# leg joints (left side): shoulder/hip, elbow/knee, wrist/ankle, paw centre
LEGS = {"F": ((0.17, -0.36, 0.36), (0.185, -0.31, 0.20), (0.185, -0.36, 0.075), (0.185, -0.41, 0.032)),
        "B": ((0.165, 0.30, 0.37), (0.18, 0.21, 0.21), (0.18, 0.33, 0.085), (0.18, 0.29, 0.032))}
TAILP = [(0, 0.44, 0.44), (0, 0.535, 0.405)]
# thorn crest: (y, z, length, back-lean deg) from the nape to the tail base, shortest at the tail
THORNS = [(-0.47, 0.515, 0.060, 30), (-0.37, 0.535, 0.066, 34), (-0.26, 0.545, 0.070, 38), (-0.15, 0.548, 0.070, 42),
          (-0.04, 0.546, 0.068, 46), (0.07, 0.542, 0.064, 50), (0.18, 0.534, 0.058, 54), (0.29, 0.522, 0.052, 58),
          (0.39, 0.505, 0.044, 62)]


def X(p, s):
    return (s * p[0], p[1], p[2])


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=27, tier=2, plates=False)
    # ---------------- torso, built in two colour layers (no rails, no box): grey upper body over a dark lower body.
    # The split line runs along the flank at mid height, the real badger read (review ruling 4).
    # upper (grey): chest -> waist -> rump, with a low arch over the back
    B.add((0, -0.21, 0.435), (0.245, 0.27, 0.10), MANTLE, "Chest", top=(0.84, 0.84), rnd=0.38)
    B.seg((0, -0.02, 0.43), (0, 0.17, 0.432), 0.222, 0.098, GREY, "Spine", top=(0.95, 0.97), side=(1, 0, 0))
    B.add((0, 0.27, 0.425), (0.212, 0.19, 0.098), GREY, "Spine", top=(0.78, 0.70), rnd=0.42)
    B.add((0, 0.08, 0.515), (0.165, 0.27, 0.038), GREY, "Spine", top=(0.70, 0.86), rnd=0.5)       # back arch
    # lower (dark): the same outline, tapering under the belly; the belly line rises from chest to rump
    B.add((0, -0.21, 0.29), (0.245, 0.27, 0.07), BELLY_D, "Chest", bot=(0.70, 0.66), rnd=0.30)
    B.seg((0, -0.02, 0.30), (0, 0.17, 0.315), 0.222, 0.06, BELLY_D, "Spine", bot=(0.75, 0.75), side=(1, 0, 0))
    B.add((0, 0.27, 0.30), (0.212, 0.19, 0.055), BELLY_D, "Spine", bot=(0.72, 0.62), rnd=0.36)
    # (the mantle = the whole upper chest + neck in MANTLE grey, review MUST 1: no stuck-on pads)
    # ---------------- neck + head: short thick neck, a white wedge head carrying the two broad black badger stripes
    B.seg((0, -0.42, 0.42), (0, -0.58, 0.43), 0.15, 0.12, MANTLE, "Neck", ext=0.04)
    B.seg((0, -0.44, 0.31), (0, -0.60, 0.35), 0.11, 0.05, BELLY_D, "Neck", side=(1, 0, 0), ext=0.02)      # dark throat
    B.seg((0, -0.56, 0.43), (0, -0.79, 0.405), 0.150, 0.115, FACE, "Head", top=(0.76, 0.82), ext=0.02)     # skull
    B.seg((0, -0.77, 0.392), (0, -0.98, 0.362), 0.098, 0.074, FACE, "Head", top=(0.52, 0.58), ext=0.02)     # snout
    B.add((0, -0.995, 0.368), (0.040, 0.022, 0.028), BLACK, "Head", role="detail", bevel=0.008)             # nose
    for s in (1, -1):
        # stripes: the black band runs from beside the nose over the eye to the ear and wraps the upper SIDE of the
        # head (real badger); a white centre stripe stays between the bands, white cheeks below. Flush (+0.006-0.009)
        B.seg((s * 0.100, -0.575, 0.468), (s * 0.072, -0.80, 0.438), 0.058, 0.085, BLACK, "Head", top=(0.76, 0.82),
              studs=[])
        B.seg((s * 0.058, -0.78, 0.430), (s * 0.034, -0.962, 0.380), 0.040, 0.045, BLACK, "Head", top=(0.60, 0.70),
              studs=[])
        # narrow amber eye slit set into the band on the side-front of the head (front end low), heavy brow ridge above
        B.add((s * 0.1285, -0.735, 0.468), (0.006, 0.037, 0.0115), AMBER, "Head", rot=(15, 0, s * 10), studs=[],
              role="detail", bevel=0.002)
        B.add((s * 0.1315, -0.748, 0.465), (0.004, 0.013, 0.0055), AMBER_HOT, "Head", rot=(15, 0, s * 10), studs=[],
              role="detail", bevel=0.001)
        B.add((s * 0.133, -0.728, 0.492), (0.010, 0.046, 0.010), MANTLE, "Head", rot=(20, 0, s * 10), studs=[],
              role="detail", bevel=0.004)
        # white cheek ruff below the stripe
        B.add((s * 0.128, -0.66, 0.39), (0.04, 0.09, 0.05), FACE, "Head", rot=(0, 0, s * 8), rnd=0.4)
        # small round ears with pale rims, at the back end of the stripe
        side = "L" if s > 0 else "R"
        ear = B.add((s * 0.128, -0.545, 0.52), (0.040, 0.020, 0.034), BLACK, "Ear_" + side, rot=(-10, 0, -s * 18),
                    top=(0.7, 0.8), rnd=0.45)
        B.add(ear.world((0, -0.010, 0.024)), (0.036, 0.012, 0.010), FACE, "Ear_" + side, R=ear.R, studs=[],
              role="detail", bevel=0.004)
    # lower jaw (dark chin) + small ivory fangs + mouth line
    B.seg((0, -0.68, 0.345), (0, -0.94, 0.335), 0.075, 0.024, BELLY_D, "Jaw", top=(0.6, 0.8), ext=0.02)
    B.add((0, -0.83, 0.356), (0.050, 0.09, 0.006), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike((s * 0.040, -0.925, 0.350), (0, 0, -1), 0.040, 0.012, IVORY, "Head")
    # ---------------- amber bramble thorn crest (short, low, swept back; smooth) on dark thorn bases
    for i, (y, z, L, lean) in enumerate(THORNS):
        bone = "Neck" if y < -0.42 else ("Chest" if y < -0.08 else "Spine")
        B.add((0, y, z - 0.004), (0.034, 0.030, 0.012), THORN_D, bone, role="detail", bevel=0.005)
        d = Vector((0, math.sin(math.radians(lean)), math.cos(math.radians(lean))))
        B.spike((0, y - 0.004, z + 0.002), d, L, 0.042, AMBER, bone, top=(0.10, 0.34))
        if i % 2 == 0 and 0 < i < 8:                                     # little side thorns on every other knot
            for s in (1, -1):
                B.spike((s * 0.055, y + 0.01, z - 0.012), (s * 0.55, 0.45, 0.70), L * 0.62, 0.026, AMBER, bone,
                        top=(0.1, 0.3))
    # ---------------- legs: short, stout, dark; front paws with long black digging claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, -0.012)), K, 0.072, 0.082, BELLY_D, leg, ext=0.0, ext1=0.03, top=(0.88, 0.82))
                B.seg(K, A, 0.068, 0.070, BELLY_D, shin, top=(0.90, 0.90), ext=0.03, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.02, -0.012)), K, 0.078, 0.095, BELLY_D, leg, bot=(0.9, 1), top=(0.80, 0.74),
                      ext=0.0, ext1=0.03)
                B.seg(K, A, 0.064, 0.068, BELLY_D, shin, top=(0.86, 0.86), ext=0.03, ext1=0.02)
                B.seg(A, P + Vector((0, 0.02, 0.025)), 0.055, 0.055, BELLY_D, foot, ext=0.03)
            big = fb == "F"
            B.add(P, (0.078 if big else 0.070, 0.085 if big else 0.075, 0.034), BELLY_D, foot, top=(0.86, 0.80))
            for gx in (-0.048, -0.016, 0.016, 0.048):
                B.spike((P.x + gx * (1.05 if big else 0.95), P.y - (0.072 if big else 0.062), 0.026),
                        (0, -1, -0.35 if big else -0.55), 0.072 if big else 0.045, 0.014 if big else 0.012, BLACK,
                        foot)
    # ---------------- stub tail with a dark band
    T = [Vector(p) for p in TAILP]
    B.seg(T[0], T[1], 0.050, 0.044, GREY, "Tail1", top=(0.70, 0.70), ext=0.03)
    B.seg(T[0] + (T[1] - T[0]) * 0.60, T[1] + (T[1] - T[0]) * 0.22, 0.040, 0.034, BELLY_D, "Tail1", top=(0.4, 0.5))
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.16, 0.37), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.10, 0.37), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.40, 0.40), "Chest", tail=(0, -0.15, 0.03))
    k.joint("Head", (0, -0.56, 0.37), "Neck", tail=(0, -0.35, 0.0))           # throat pivot (low / back of the head)
    k.joint("Jaw", (0, -0.69, 0.345), "Head", tail=(0, -0.25, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.125, -0.555, 0.48), "Head", tail=(0, 0, 0.1))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.12, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
            k.joint("Dirt_" + fb + side, (s * P[0], P[1] - 0.07, 0.02), "Foot_" + fb + side, tail=(0, -0.1, 0))
    k.joint("Tail1", TAILP[0], "Spine", tail=(0, 0.13, -0.05))
    k.joint("Mouth", (0, -0.97, 0.35), "Head", tail=(0, -0.1, 0))              # growl dust puff
    k.joint("Crest", (0, -0.04, 0.60), "Spine", tail=(0, 0, 0.1))              # leaf-dust on the thorns (act)


def check_pairs():
    return [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
            ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"),
            ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Head", "Chest"), ("Jaw", "Chest"),
            ("Head", "Shin_FL"), ("Head", "Shin_FR"), ("Jaw", "Shin_FL"), ("Jaw", "Shin_FR"),
            ("Jaw", "Foot_FL"), ("Jaw", "Foot_FR"), ("Head", "Foot_FL"), ("Head", "Foot_FR"),
            ("Tail1", "Shin_BL"), ("Tail1", "Shin_BR")]


def joints():
    return [((0, -0.55, 0.36), (0, -0.60, 0.42), 0.17, "Head")]


# ------------------------------------------------------------------ animation (authored after the model gate)
import petkit as pk
import _common as cm


# anim(k) is added after the model gate (headless_pack uses the model-only path while it's missing)


HEAD_XF = []
