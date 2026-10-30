# Bramble Badger (Wood/Grass egg, STARTER 40 %) - FIERCE style (2026-10-27, Glacier update batch 1).
# Plan: _review/BrambleBadger_plan.md (v2) + review _review/GLACIER_PLAN_REVIEW.md 2.7.
# A low, grumpy badger: pale grey back with a darker mantle cape over the shoulders and nape, a short crest of amber
# bramble thorns down the spine, dark belly / legs / side skirt, a white wedge face with two bold black badger bands
# running from the snout over the narrow amber eyes to the ears, dark digging claws, a stub tail.
# v2 (builder A, model review 1 M1-M7 + N1-N4): narrow edge bands (white centre >= 0.12), lifted palette, grey/dark
# split at z 0.30 with a belly tuck, mantle = shoulder cape only, forward-facing eyes in the bands, shorter snout,
# flush ear rims, shorter claws/thorns, whole body 0.03 lower, tail stub seated in the rump.
import math
from mathutils import Vector, Euler

DISPLAY = "Bramble Badger"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 6.5                # total height (thorn crest top) in studs at x1; Mossback 7, Basilisk 8, Stag 11

GREY = (176, 172, 180)      # back / flanks (studded)
MANTLE = (136, 130, 146)    # darker mantle cape over shoulders + nape (review 1 M2)
BELLY_D = (104, 88, 80)     # belly, legs, side skirt (review 1 M2: not near-black in game)
FACE = (255, 252, 244)      # face, cheeks, ear rims (review 1 M1)
AMBER = (255, 176, 64)      # THE accent: thorn crest + eye slits (review 1 M2)
AMBER_HOT = (255, 214, 140)
THORN_D = (96, 56, 28)      # thorn bases (review 1 M2)
BLACK = (14, 14, 22)
IVORY = (238, 234, 220)
MOUTH = (86, 18, 30)

PITCH = 0.024               # stud pitch: ~0.08 x torso height (TH ~0.30)

# leg joints (left side): shoulder/hip, elbow/knee, wrist/ankle, paw centre (review N3: 0.03 lower)
LEGS = {"F": ((0.17, -0.36, 0.33), (0.185, -0.31, 0.17), (0.185, -0.36, 0.064), (0.185, -0.41, 0.032)),
        "B": ((0.165, 0.30, 0.34), (0.18, 0.21, 0.18), (0.18, 0.33, 0.074), (0.18, 0.29, 0.032))}
TAILP = [(0, 0.43, 0.40), (0, 0.555, 0.372)]
# thorn crest: (y, z, length, back-lean deg) from the nape to the tail base, shortest at the tail (review N2: <= 0.058)
THORNS = [(-0.47, 0.515, 0.052, 30), (-0.37, 0.535, 0.056, 34), (-0.26, 0.545, 0.058, 38), (-0.15, 0.548, 0.058, 42),
          (-0.04, 0.546, 0.058, 46), (0.07, 0.542, 0.056, 50), (0.18, 0.534, 0.052, 54), (0.29, 0.522, 0.048, 58),
          (0.39, 0.505, 0.042, 62)]
DZ = -0.030                 # review N3: the body / head / tail sit this much lower than the coordinates below
BODYB = ("Chest", "Spine", "Neck", "Head", "Jaw", "Ear_L", "Ear_R", "Tail1")


def bz(p):
    return tuple(Vector(p) + Vector((0, 0, DZ)))


def X(p, s):
    return (s * p[0], p[1], p[2])


def hdims(b, lz):
    """half width / half height of seg block b at local z (its taper), in b's local frame"""
    t = (lz / b.h.z + 1) / 2
    return (b.h.x * (b.bot[0] + (b.top[0] - b.bot[0]) * t), b.h.y * (b.bot[1] + (b.top[1] - b.bot[1]) * t))


def edge_band(B, host, s, z0, z1, wx, wy, color, k1=1.0, proud=0.003, bone=None):
    """a flush band hugging the +-x TOP edge of seg block `host` from local z0 to z1 (z = along the seg, y = up):
    shows wx*2 wide on the top face and wy*2 tall on the side wall; k1 = taper of the band at the z1 end"""
    W0, H0 = hdims(host, z0)
    W1, H1 = hdims(host, z1)
    xb, yb = s * (W0 - wx + proud), H0 - wy + proud
    xt, yt = s * (W1 - wx * k1 + proud), H1 - wy * k1 + proud
    c = Vector((xb, yb, (z0 + z1) / 2))
    return B.add(host.world(c), (wx, wy, (z1 - z0) / 2), color, bone or host.bone, R=host.R, top=(k1, k1),
                 top_shift=(xt - xb, yt - yb), studs=[], nostud=True, rnd=0.45)       # rounded like the skull edge


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=27, tier=2, plates=False)
    # ---------------- torso in two colour layers: grey upper body over a dark lower skirt, split at z 0.30 (M3).
    # MANTLE = a shoulder cape (y -0.48..-0.26, M4), slightly proud of the grey, with a sloped back edge.
    B.add((0, -0.37, 0.42), (0.245, 0.11, 0.12), MANTLE, "Chest", top=(0.86, 0.80), top_shift=(0, 0.035), rnd=0.40)
    B.add((0, -0.30, 0.415), (0.226, 0.09, 0.115), GREY, "Chest", top=(0.90, 0.95), rnd=0.38)    # grey shoulder
    B.seg((0, -0.26, 0.415), (0, 0.17, 0.417), 0.222, 0.115, GREY, "Spine", top=(0.95, 0.97), side=(1, 0, 0))
    B.add((0, 0.27, 0.415), (0.212, 0.19, 0.115), GREY, "Spine", top=(0.78, 0.70), rnd=0.42)
    B.add((0, 0.08, 0.515), (0.165, 0.27, 0.038), GREY, "Spine", top=(0.70, 0.86), rnd=0.5)       # back arch
    # lower (dark) skirt: the belly line rises from 0.22 at the chest to 0.26 at waist + rump (a 0.04 tuck)
    B.add((0, -0.21, 0.26), (0.245, 0.27, 0.04), BELLY_D, "Chest", bot=(0.70, 0.66), rnd=0.30)
    B.seg((0, -0.02, 0.28), (0, 0.17, 0.295), 0.222, 0.02, BELLY_D, "Spine", bot=(0.75, 0.75), side=(1, 0, 0))
    B.add((0, 0.27, 0.28), (0.212, 0.19, 0.02), BELLY_D, "Spine", bot=(0.72, 0.62), rnd=0.36)
    # ---------------- neck (mantle) + head: a white wedge head with two narrow black edge bands
    B.seg((0, -0.42, 0.42), (0, -0.58, 0.43), 0.15, 0.12, MANTLE, "Neck", ext=0.04)
    B.seg((0, -0.44, 0.31), (0, -0.60, 0.35), 0.11, 0.05, BELLY_D, "Neck", side=(1, 0, 0), ext=0.02)      # dark throat
    skull = B.seg((0, -0.56, 0.43), (0, -0.79, 0.405), 0.150, 0.115, FACE, "Head", top=(0.66, 0.80), ext=0.02)
    snout = B.seg((0, -0.77, 0.392), (0, -0.92, 0.366), 0.096, 0.072, FACE, "Head", top=(0.58, 0.64), ext=0.02)
    B.add((0, -0.935, 0.374), (0.038, 0.022, 0.028), BLACK, "Head", role="detail", bevel=0.008)             # nose
    for s in (1, -1):
        # the badger bands: from the ear over the eye along the skull's top edge, then down the snout to the nose
        edge_band(B, skull, s, -skull.h.z + 0.012, skull.h.z, 0.035, 0.040, BLACK, k1=0.80)
        edge_band(B, snout, s, -snout.h.z - 0.010, snout.h.z - 0.024, 0.022, 0.022, BLACK, k1=0.70)
        # narrow amber eye slit in the band near the front of the skull, facing ~35 deg forward (M5), heavy brow
        lz = 0.070
        W, Hh = hdims(skull, lz)
        p = skull.world(Vector((s * (W + 0.010), Hh - 0.040, lz)))
        alpha = math.atan2(hdims(skull, -skull.h.z)[0] - hdims(skull, skull.h.z)[0], 2 * skull.h.z)  # wedge wall
        Re = skull.R @ Euler((0, -s * (alpha + math.radians(22)), 0), "XYZ").to_matrix()   # ~33 deg forward
        nrm = Re @ Vector((s, 0, 0))
        B.add(p, (0.010, 0.024, 0.040), BLACK, "Head", R=Re, studs=[], role="detail", bevel=0.006)      # socket
        Rs = Re @ Euler((math.radians(14), 0, 0), "XYZ").to_matrix()                  # front end low
        B.add(p + nrm * 0.011, (0.004, 0.0115, 0.036), AMBER, "Head", R=Rs, studs=[], role="detail", bevel=0.002)
        B.add(p + nrm * 0.0135, (0.002, 0.0055, 0.013), AMBER_HOT, "Head", R=Rs, studs=[], role="detail",
              bevel=0.001)
        Rb = Re @ Euler((math.radians(22), 0, 0), "XYZ").to_matrix()
        B.add(p + nrm * 0.010 + skull.R @ Vector((0, 0.026, 0.004)), (0.012, 0.010, 0.050), MANTLE, "Head", R=Rb,
              studs=[], role="detail", bevel=0.004)                                         # heavy brow ridge
        # white cheek ruff below the band (M1: bigger)
        B.add((s * 0.125, -0.64, 0.385), (0.05, 0.145, 0.06), FACE, "Head", rot=(0, 0, s * 8), rnd=0.4)
        # small round ears at the back end of the band, a thin flush pale rim along the top (M7)
        side = "L" if s > 0 else "R"
        ear = B.add((s * 0.128, -0.545, 0.52), (0.040, 0.020, 0.034), BLACK, "Ear_" + side, rot=(-10, 0, -s * 18),
                    top=(0.7, 0.8), rnd=0.45)
        B.add(ear.world((0, -0.021, 0.020)), (0.030, 0.004, 0.009), FACE, "Ear_" + side, R=ear.R, studs=[],
              role="detail", bevel=0.003)
    # lower jaw (white chin) + small ivory fangs + mouth line (M6: 0.06 shorter)
    B.seg((0, -0.68, 0.345), (0, -0.88, 0.335), 0.075, 0.024, FACE, "Jaw", top=(0.6, 0.8), ext=0.02)
    B.add((0, -0.80, 0.356), (0.050, 0.07, 0.006), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike((s * 0.040, -0.865, 0.350), (0, 0, -1), 0.040, 0.012, IVORY, "Head")
    # ---------------- amber bramble thorn crest (short, low, swept back; smooth) on dark thorn bases
    for i, (y, z, L, lean) in enumerate(THORNS):
        bone = "Neck" if y < -0.42 else ("Chest" if y < -0.08 else "Spine")
        B.add((0, y, z - 0.004), (0.034, 0.030, 0.012), THORN_D, bone, role="detail", bevel=0.005)
        d = Vector((0, math.sin(math.radians(lean)), math.cos(math.radians(lean))))
        B.spike((0, y - 0.004, z + 0.002), d, L, 0.056, AMBER, bone, top=(0.10, 0.34))
        if i % 2 == 0 and 0 < i < 8:                                     # little side thorns on every other knot
            for s in (1, -1):
                B.spike((s * 0.058, y + 0.01, z - 0.012), (s * 0.55, 0.45, 0.70), L * 0.72, 0.034, AMBER, bone,
                        top=(0.1, 0.3))
    # ---------------- stub tail seated in the rump, short dark band (N4)
    T = [Vector(p) for p in TAILP]
    B.seg(T[0], T[1], 0.050, 0.044, GREY, "Tail1", top=(0.70, 0.70), ext=0.02)
    B.seg(T[0] + (T[1] - T[0]) * 0.72, T[1] + (T[1] - T[0]) * 0.16, 0.038, 0.032, BELLY_D, "Tail1", top=(0.4, 0.5))
    dz = Vector((0, 0, DZ))
    for blk in B.items:                                 # N3: the body group sits 0.03 lower
        if blk.bone in BODYB:
            if hasattr(blk, "pts"):
                blk.pts = [q + dz for q in blk.pts]
            blk.c = blk.c + dz
    # ---------------- legs: short, stout, dark; front paws with black digging claws (N1: 0.050)
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, -0.045)), K, 0.066, 0.076, BELLY_D, leg, ext=0.0, ext1=0.03, top=(0.88, 0.82),
                      rnd=0.40)
                B.seg(K, A, 0.062, 0.064, BELLY_D, shin, top=(0.90, 0.90), ext=0.03, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.02, -0.012)), K, 0.072, 0.088, BELLY_D, leg, bot=(0.9, 1), top=(0.80, 0.74),
                      ext=0.0, ext1=0.03)
                B.add(H + Vector((s * 0.022, 0.025, -0.035)), (0.068, 0.110, 0.075), GREY, leg, bot=(0.72, 0.75),
                      rnd=0.45)                                    # grey body fur carried down over the haunch
                B.seg(K, A, 0.058, 0.062, BELLY_D, shin, top=(0.86, 0.86), ext=0.03, ext1=0.02)
                B.seg(A, P + Vector((0, 0.02, 0.025)), 0.050, 0.050, BELLY_D, foot, ext=0.03)
            big = fb == "F"
            B.add(P, (0.074 if big else 0.066, 0.082 if big else 0.072, 0.034), BELLY_D, foot, top=(0.86, 0.80))
            for gx in (-0.048, -0.016, 0.016, 0.048):
                B.spike((P.x + gx * (1.05 if big else 0.95), P.y - (0.072 if big else 0.062), 0.026),
                        (0, -1, -0.35 if big else -0.55), 0.050 if big else 0.045, 0.014 if big else 0.012, BLACK,
                        foot)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", bz((0, 0.16, 0.37)), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", bz((0, -0.10, 0.37)), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", bz((0, -0.40, 0.40)), "Chest", tail=(0, -0.15, 0.03))
    k.joint("Head", bz((0, -0.56, 0.37)), "Neck", tail=(0, -0.30, 0.0))       # throat pivot (low / back of the head)
    k.joint("Jaw", bz((0, -0.69, 0.345)), "Head", tail=(0, -0.19, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, bz((s * 0.125, -0.555, 0.48)), "Head", tail=(0, 0, 0.1))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.12, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
            k.joint("FX_DirtPuff_" + fb + side, (s * P[0], P[1] - 0.07, 0.02), "Foot_" + fb + side, tail=(0, -0.1, 0))
    k.joint("Tail1", bz(TAILP[0]), "Spine", tail=tuple(Vector(TAILP[1]) - Vector(TAILP[0])))
    k.joint("FX_DustGrowl", bz((0, -0.91, 0.35)), "Head", tail=(0, -0.1, 0))   # growl dust puff at the mouth
    k.joint("FX_LeafDust", bz((0, -0.04, 0.60)), "Spine", tail=(0, 0, 0.1))    # leaf-dust on the thorns (act)


def check_pairs():
    return [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
            ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"),
            ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Head", "Chest"), ("Jaw", "Chest"),
            ("Head", "Shin_FL"), ("Head", "Shin_FR"), ("Jaw", "Shin_FL"), ("Jaw", "Shin_FR"),
            ("Jaw", "Foot_FL"), ("Jaw", "Foot_FR"), ("Head", "Foot_FL"), ("Head", "Foot_FR"),
            ("Tail1", "Shin_BL"), ("Tail1", "Shin_BR")]


def joints():
    return [(bz((0, -0.55, 0.36)), bz((0, -0.60, 0.42)), 0.17, "Head")]


# ------------------------------------------------------------------ animation (authored after the model gate)
import petkit as pk
import _common as cm


# anim(k) is added after the model gate (headless_pack uses the model-only path while it's missing)


HEAD_XF = []
