# Bramble Badger (Wood/Grass egg, STARTER 40 %) - FIERCE style (2026-10-27, Glacier update batch 1).
# Plan: _review/BrambleBadger_plan.md (v2) + review _review/GLACIER_PLAN_REVIEW.md 2.7.
# A low, grumpy badger: pale grey back with a darker mantle cape over the shoulders and nape, a short crest of amber
# bramble thorns down the spine, dark belly / legs / side skirt, a white wedge face with two bold black badger bands
# running from the snout over the narrow amber eyes to the ears, dark digging claws, a stub tail.
# v2 (builder A, model review 1 M1-M7 + N1-N4): narrow edge bands (white centre >= 0.12), lifted palette, grey/dark
# split at z 0.30 with a belly tuck, mantle = shoulder cape only, forward-facing eyes in the bands, shorter snout,
# flush ear rims, shorter claws/thorns, whole body 0.03 lower, tail stub seated in the rump.
import math
import os
from mathutils import Vector, Euler

DISPLAY = "Bramble Badger"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 6.5                # total height (thorn crest top) in studs at x1; Mossback 7, Basilisk 8, Stag 11

GREY = (176, 172, 180)      # back / flanks (studded)
MANTLE = (136, 130, 146)    # darker mantle cape over shoulders + nape (review 1 M2)
BELLY_D = (104, 88, 80)     # belly, legs, side skirt (review 1 M2: not near-black in game)
GREY_D = (150, 146, 156)       # final85 T1: flank band between the grey back and the dark skirt
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
THORNS = [(-0.47, 0.550, 0.064, 30), (-0.37, 0.570, 0.072, 34), (-0.26, 0.545, 0.072, 38), (-0.15, None, 0.072, 42),
          (-0.04, None, 0.072, 46), (0.07, None, 0.072, 50), (0.18, None, 0.064, 54), (0.29, None, 0.048, 58),
          (0.39, None, 0.042, 62)]                      # final85 T2 lengths; None = seated on the hull top (r2 T2)
MANTLE_TILT = float(os.environ.get("BADGER_TILT", "-10.0"))  # r4 N5: the mantle pitches nose-up, rear down
BREATH = float(os.environ.get("BADGER_BREATH", "1.0"))       # r4 M1 test switch (0 = breath off)
TWITCH_DEG = float(os.environ.get("BADGER_TWITCH", "8.0"))   # r4 N2 ear twitch (test switch: 0 = off)
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


HULL_P = 3.5                     # superellipse exponent of the upper body cross-section (rounded back, no seams)
HULL_PB = 6.0                    # lower half: squarer, so the flank stays full down to the skirt (legs stay covered)
HULL_ZB = 0.26                   # hull bottom (buried in the dark skirt)


def hull_top(y):
    """top line of the merged grey body (r2 T2): 0.540 at the shoulders, the old arch height 0.553 over the middle,
    0.535 over the rump, then the rump rounds off (y 0.40-0.465)"""
    def ss(a, b, t):
        u = max(0.0, min(1.0, (t - a) / (b - a)))
        return u * u * (3 - 2 * u)
    return 0.540 + 0.013 * ss(-0.22, -0.05, y) - 0.018 * ss(0.22, 0.40, y)


def hull_hx(y):
    return 0.222 - 0.010 * max(0.0, min(1.0, (y + 0.26) / 0.66))


def hull_x(y, z):
    """flank half-width of the hull at height z (superellipse)"""
    zt = hull_top(y)
    zc, hz = (zt + HULL_ZB) / 2, (zt - HULL_ZB) / 2
    u = min(1.0, abs((z - zc) / hz))
    pp = HULL_P if z >= zc else HULL_PB
    return hull_hx(y) * (1 - u ** pp) ** (1 / pp)


def body_hull(B):
    """ONE grey body from the shoulders (y -0.25, inside the shoulder blocks) to a rounded rump (y 0.465): a studded
    closed Tube of superellipse rings - replaces the spine seg, the rear block and the back arch (no seams)"""
    rings, n = [], 22
    ys = [-0.25 + 0.025 * i for i in range(27)] + [0.415, 0.43, 0.445, 0.455, 0.462]
    for y in ys:
        zt = hull_top(min(y, 0.40))
        zc, hz, hx = (zt + HULL_ZB) / 2, (zt - HULL_ZB) / 2, hull_hx(min(y, 0.40))
        f = math.sqrt(max(0.0, 1 - ((y - 0.40) / 0.068) ** 2)) if y > 0.40 else 1.0     # round the rump
        ring = []
        for i in range(n):
            a = 2 * math.pi * i / n
            c, sn = math.cos(a), math.sin(a)
            pp = HULL_P if sn >= 0 else HULL_PB
            x = hx * f * math.copysign(abs(c) ** (2 / pp), c)
            z = zc + hz * f * math.copysign(abs(sn) ** (2 / pp), sn)
            ring.append(Vector((x, y, z)))
        rings.append(ring)
    B.tube(rings, GREY, "Spine")


def flank_bands(B, z0=0.3085, z1=0.3565):
    """the GREY_D flank band as a thin open-arc strip that hugs the hull flank (0.003 proud), y -0.25..0.38"""
    zs = [z0 + (z1 - z0) * i / 4 for i in range(5)]
    for s in (1, -1):
        rings = []
        for i in range(26):
            y = -0.25 + 0.63 * i / 25
            outer = [Vector((s * (hull_x(y, z) + 0.003), y, z)) for z in zs]
            inner = [Vector((s * (hull_x(y, z) - 0.008), y, z)) for z in zs]
            rings.append((outer, inner))
        B.tube(rings, GREY_D, "Spine", closed=False, nostud=True)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=27, tier=2, plates=False)
    # ---------------- torso in two colour layers: grey upper body over a dark lower skirt, split at z 0.30 (M3).
    # MANTLE = a shoulder cape (y -0.48..-0.26, M4), slightly proud of the grey, with a sloped back edge.
    B.add((0, -0.364, 0.44), (0.245, 0.11, 0.135), MANTLE, "Chest", rot=(MANTLE_TILT, 0, 0), top=(0.86, 0.66),
          top_shift=(0, 0.050), rnd=0.50)       # r4 N5: rounder (capped 0.45) + tilted so the rear rolls into the back
    # (r3 T1: the shoulder hump is 0.035 higher - the badger's heavy shoulders)
    B.add((0, -0.30, 0.415), (0.226, 0.09, 0.115), GREY, "Chest", top=(0.90, 0.95), rnd=0.38)    # grey shoulder
    body_hull(B)                                        # r2 T2: ONE lofted grey body (spine + rear + arch merged)
    # lower (dark) skirt: the belly line rises from 0.22 at the chest to 0.26 at waist + rump (a 0.04 tuck)
    B.add((0, -0.21, 0.26), (0.245, 0.27, 0.04), BELLY_D, "Chest", bot=(0.70, 0.66), rnd=0.30)
    B.seg((0, -0.02, 0.28), (0, 0.17, 0.295), 0.222, 0.02, BELLY_D, "Spine", bot=(0.75, 0.75), side=(1, 0, 0))
    B.add((0, 0.27, 0.28), (0.212, 0.19, 0.02), BELLY_D, "Spine", bot=(0.72, 0.62), rnd=0.36)
    flank_bands(B)                                      # final85 T1 / r2 T1: GREY_D band hugging the hull flank
    # ---------------- neck (mantle) + head: a white wedge head with two narrow black edge bands
    B.seg((0, -0.42, 0.42), (0, -0.58, 0.41), 0.15, 0.12, MANTLE, "Neck", ext=0.04)
    B.seg((0, -0.44, 0.31), (0, -0.60, 0.33), 0.11, 0.05, BELLY_D, "Neck", side=(1, 0, 0), ext=0.02)      # dark throat
    skull = B.seg((0, -0.56, 0.41), (0, -0.79, 0.385), 0.150, 0.115, FACE, "Head", top=(0.66, 0.80), ext=0.02)
    snout = B.seg((0, -0.77, 0.372), (0, -0.92, 0.346), 0.096, 0.072, FACE, "Head", top=(0.58, 0.64), ext=0.02)
    B.add((0, -0.935, 0.354), (0.038, 0.022, 0.028), BLACK, "Head", role="detail", bevel=0.008)             # nose
    for s in (1, -1):
        # the badger bands: from the ear over the eye along the skull's top edge, then down the snout to the nose
        edge_band(B, skull, s, -skull.h.z + 0.012, skull.h.z, 0.035, 0.040, BLACK, k1=0.80)
        edge_band(B, snout, s, -snout.h.z - 0.010, snout.h.z - 0.024, 0.022, 0.022, BLACK, k1=0.70)
        # narrow amber eye slit in the band near the front of the skull, facing ~35 deg forward (M5), heavy brow
        lz = 0.070
        W, Hh = hdims(skull, lz)
        p = skull.world(Vector((s * (W - 0.002), Hh - 0.040, lz)))          # review 2 M-1: seated in the band
        alpha = math.atan2(hdims(skull, -skull.h.z)[0] - hdims(skull, skull.h.z)[0], 2 * skull.h.z)  # wedge wall
        Re = skull.R @ Euler((0, -s * (alpha + math.radians(22)), 0), "XYZ").to_matrix()   # ~33 deg forward
        nrm = Re @ Vector((s, 0, 0))
        B.add(p, (0.010, 0.024, 0.040), BLACK, "Head", R=Re, studs=[], role="detail", bevel=0.006)      # socket
        Rs = Re @ Euler((math.radians(14), 0, 0), "XYZ").to_matrix()                  # front end low
        B.add(p + nrm * 0.011, (0.004, 0.0115, 0.036), AMBER, "Head", R=Rs, studs=[], role="detail", bevel=0.002)
        B.add(p + nrm * 0.0135, (0.002, 0.0055, 0.013), AMBER_HOT, "Head", R=Rs, studs=[], role="detail",
              bevel=0.001)
        Rb = Re @ Euler((math.radians(22), 0, 0), "XYZ").to_matrix()
        B.add(p + skull.R @ Vector((0, 0.026, 0.004)), (0.012, 0.010, 0.050), MANTLE, "Head", R=Rb,
              studs=[], role="detail", bevel=0.004)                                         # heavy brow ridge
        # white cheek ruff below the band (M1: bigger)
        B.add((s * 0.125, -0.649, 0.352), (0.05, 0.136, 0.070), FACE, "Head", rot=(0, 0, s * 8), rnd=0.4)  # r4 M2: rear 0.018 shorter (mantle clearance)
        # small round ears at the back end of the band, a thin flush pale rim along the top (M7)
        side = "L" if s > 0 else "R"
        ear = B.add((s * 0.128, -0.545, 0.50), (0.040, 0.020, 0.034), BLACK, "Ear_" + side, rot=(-10, 0, -s * 18),
                    top=(0.7, 0.8), rnd=0.45)
        B.add(ear.world((0, -0.021, 0.020)), (0.030, 0.004, 0.009), FACE, "Ear_" + side, R=ear.R, studs=[],
              role="detail", bevel=0.003)
    # lower jaw (white chin) + small ivory fangs + mouth line (M6: 0.06 shorter)
    B.seg((0, -0.68, 0.325), (0, -0.88, 0.315), 0.085, 0.024, FACE, "Jaw", top=(0.6, 0.8), ext=0.02)
    B.add((0, -0.80, 0.336), (0.050, 0.07, 0.006), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike((s * 0.040, -0.865, 0.330), (0, 0, -1), 0.040, 0.012, IVORY, "Head")
    # ---------------- amber bramble thorn crest (short, low, swept back; smooth) on dark thorn bases
    for i, (y, z, L, lean) in enumerate(THORNS):
        z = hull_top(y) - 0.006 if z is None else z
        bone = "Neck" if y < -0.42 else ("Chest" if y < -0.08 else "Spine")
        B.add((0, y, z - 0.004), (0.034, 0.030, 0.012), THORN_D, bone, role="detail", bevel=0.005)
        d = Vector((0, math.sin(math.radians(lean)), math.cos(math.radians(lean))))
        tb = "Thorn_%d" % (i + 1)                                        # own bone: flatten / bristle (clips)
        B.spike((0, y - 0.004, z + 0.002), d, L, 0.064, AMBER, tb, top=(0.10, 0.34))     # final85 T2: width 0.064
        if i % 2 == 0 and 0 < i < 8:                                     # little side thorns on every other knot
            for s in (1, -1):
                B.spike((s * 0.058, y + 0.01, z - 0.012), (s * 0.55, 0.45, 0.70), L * 0.72, 0.034, AMBER, tb,
                        top=(0.1, 0.3))
    # ---------------- stub tail seated in the rump, short dark band (N4)
    T = [Vector(p) for p in TAILP]
    B.seg(T[0], T[1], 0.050, 0.044, GREY, "Tail1", top=(0.70, 0.70), ext=0.02)
    B.seg(T[0] + (T[1] - T[0]) * 0.72, T[1] + (T[1] - T[0]) * 0.16, 0.038, 0.032, BELLY_D, "Tail1", top=(0.4, 0.5))
    if os.environ.get("BADGER_NECKDBG"):                # r5 MUST 1 evidence: Neck-bone parts in magenta
        for blk in B.items:
            if blk.bone == "Neck":
                blk.color = bk.rgb((255, 0, 255))
    dz = Vector((0, 0, DZ))
    for blk in B.items:                                 # N3: the body group sits 0.03 lower
        if blk.bone in BODYB or blk.bone.startswith("Thorn_"):
            if isinstance(blk, bk.Tube):                # the tube mesh is built from rings (Lynx review 1 M1 lesson)
                blk.map(lambda q: q + dz)
                continue
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
                B.seg(H + Vector((0, 0.0, -0.045)), K, 0.048, 0.080, BELLY_D, leg, bot=(0.9, 1), top=(0.95, 0.95),
                      ext=0.0, ext1=0.03, rnd=0.45)     # final85 M1: no fin - narrower, starts under the body line
                B.add(H + Vector((0, 0.025, -0.035)), (0.050, 0.110, 0.075), GREY, "Spine", bot=(0.72, 0.75),
                      rnd=0.45)                     # haunch fur, flush with the rear block (final85 M2)
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
    k.joint("Head", bz((0, -0.56, 0.35)), "Neck", tail=(0, -0.30, 0.0))       # throat pivot (low / back of the head)
    k.joint("Jaw", bz((0, -0.69, 0.325)), "Head", tail=(0, -0.19, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, bz((s * 0.125, -0.555, 0.46)), "Head", tail=(0, 0, 0.1))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.12, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
            k.joint("FX_DirtPuff_" + fb + side, (s * P[0], P[1] - 0.07, 0.02), "Foot_" + fb + side, tail=(0, -0.1, 0))
    k.joint("Tail1", bz(TAILP[0]), "Spine", tail=tuple(Vector(TAILP[1]) - Vector(TAILP[0])))
    k.joint("FX_DustGrowl", bz((0, -0.91, 0.33)), "Head", tail=(0, -0.1, 0))   # growl dust puff at the mouth
    k.joint("FX_LeafDust", bz((0, -0.04, 0.60)), "Spine", tail=(0, 0, 0.1))    # leaf-dust on the thorns (act)
    for i, (y, z, L, lean) in enumerate(THORNS):                           # one bone per thorn, pivot at its base
        z = hull_top(y) - 0.006 if z is None else z
        bone = "Neck" if y < -0.42 else ("Chest" if y < -0.08 else "Spine")
        k.joint("Thorn_%d" % (i + 1), bz((0, y, z - 0.004)), bone, tail=(0, 0.02, 0.06))


def check_pairs():
    return [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
            ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"),
            ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Head", "Chest"), ("Jaw", "Chest"),
            ("Head", "Shin_FL"), ("Head", "Shin_FR"), ("Jaw", "Shin_FL"), ("Jaw", "Shin_FR"),
            ("Jaw", "Foot_FL"), ("Jaw", "Foot_FR"), ("Head", "Foot_FL"), ("Head", "Foot_FR"),
            ("Tail1", "Shin_BL"), ("Tail1", "Shin_BR")]


def joints():
    return [(bz((0, -0.55, 0.34)), bz((0, -0.60, 0.40)), 0.17, "Head")]


# ------------------------------------------------------------------ animation (BrambleBadger/ANIM_REFS.md)
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
THORNB = ["Thorn_%d" % (i + 1) for i in range(len(THORNS))]
H_U = 0.58                       # model height in units (HEIGHT 6.5 studs): 0.05H = 0.029


def tab(T, f):
    """eased (smoothstep) interpolation through [(frame, value | tuple)]"""
    if f <= T[0][0]:
        return T[0][1]
    for (f0, v0), (f1, v1) in zip(T, T[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / (f1 - f0) if f1 > f0 else 1.0
            u = u * u * (3 - 2 * u)
            if isinstance(v0, tuple):
                return tuple(a + (b - a) * u for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * u
    return T[-1][1]


def feet(k, f, T):
    """solve all four legs at frame f; T = {leg: (dx, dy, lift)} offsets from the rest ground spot"""
    import bpy
    bpy.context.scene.frame_set(f)
    for leg in LEGS4:
        dx, dy, lift = T.get(leg, (0.0, 0.0, 0.0))
        k.solve_leg(leg, f, Vector((k.J[leg].x + dx, k.J[leg].y + dy, lift)))


def thorns(k, f, pitch=0.0, wave=0.0, n=1, lag=0.06):
    """the bramble crest: all thorns pitch together (+ = forward / up, - = flatten back), optional travelling wave"""
    for i, b in enumerate(THORNB):
        w = wave * math.sin(2 * math.pi * (f / n - lag * i)) if wave else 0.0
        k.key(b, f, rot=(pitch + w, 0, 0))


def ears(k, f, p=0.0, splay=0.0):
    """p = pitch (+ forward), splay = outward roll (r4 N2: the twitch flicks the ears out, readable from behind)"""
    k.key("Ear_L", f, rot=(p, 0, splay))           # + roll = Ear_L tips out (+x); checked in a front render
    k.key("Ear_R", f, rot=(p, 0, -splay))


def idle(k):
    """NOSE-DOWN SNIFF (ref A): the head drops to the ground (front low, rump high), three nose sweeps along the
    ground with small lifts between them, the crest bristles once at f70, the head lifts back slower than it fell."""
    n = 120
    k.new_action("idle", n, True)
    DOWN = [(0, 0.0), (20, 1.0), (80, 1.0), (102, 0.0), (120, 0.0)]
    YAW = [(0, 0.0), (22, 0.0), (36, 8.0), (52, -8.0), (68, 5.0), (80, 0.0), (120, 0.0)]
    LIFT = [(0, 0.0), (28, 0.0), (34, 1.0), (40, 0.0), (48, 0.0), (52, 1.0), (58, 0.0), (66, 0.0), (70, 1.0),
            (76, 0.0), (120, 0.0)]
    BRIS = [(0, 0.0), (64, 0.0), (70, 1.0), (78, 1.0), (88, 0.0), (120, 0.0)]
    FLICK = [(0, 0.0), (40, 0.0), (46, 1.0), (52, 0.0), (96, 0.0), (102, 1.0), (108, 0.0), (120, 0.0)]   # r2 MC1: 12 f
    TWITCH = [(0, 0.0), (33, 0.0), (36, 1.0), (39, 0.0), (49, 0.0), (52, 1.0), (55, 0.0), (65, 0.0), (68, 1.0),
              (71, 0.0), (111, 0.0), (114, 1.0), (117, 0.0), (120, 0.0)]
    # r4 N2: a 6 f ear twitch at each sniff peak; r5: + one at f111-117 with the head back up (the ears clear the
    # mantle hump from the game camera only when the head is up)
    for f in range(0, n + 1):
        d, yw, lf, br = tab(DOWN, f), tab(YAW, f), tab(LIFT, f), tab(BRIS, f)
        b = BREATH * pk.wave(f, n, 0, 3)                                  # breathing all loop long (+1 at f10/50/90)
        k.key("Spine", f, rot=(4.0 * d, 0, 3.5 * yw / 8.0), loc=(0, 0, -0.010 * d + 0.014 * b))   # r4 N3 roll 3.5
        k.key("Chest", f, rot=(1.0 * d, 0, 0))                          # r4 M1: no breath pitch (it cancelled the lift)
        k.key("Neck", f, rot=(7.5 * d, 0.30 * yw, 0))                  # neck total <= 7.9 deg (limit 8)
        k.key("Head", f, rot=(15.5 * d - 10.0 * lf + 2.0 * b, 0.70 * yw, -0.3 * yw))   # r4 N1 lift 10, M1 nose held
        k.key("Jaw", f, rot=(1.5 + 1.5 * lf, 0, 0))
        fk = tab(FLICK, f)
        tw = tab(TWITCH, f)
        ears(k, f, -4.0 * d + 3.0 * lf + 16.0 * fk + TWITCH_DEG * tw, splay=3.5 * TWITCH_DEG * tw)   # r5: 8 fwd + 28 out
        thorns(k, f, 5.0 * br)                                            # r3 MC3: crest bristle 5 deg
        k.key("Tail1", f, rot=(4.0 * d + 14.0 * fk, 6.0 * pk.wave(f, n, 0.0, 2), 0))   # + a 14 deg tail flick
    cm.plant(k, n)
    k.finish()
    k.meta["planted"] = list(LEGS4)


def walk(k):
    """WADDLE-TROT (ref D): diagonal pairs, short stride, the stocky body rocks toward the planted front foot, the
    head dips on each front contact, the stub tail flicks late, the crest ripples a little."""
    n = 30

    def body(f):
        bob = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 2.0 * pk.wave(f, n), 4.0 * pk.wave(f, n)),
              loc=(0, 0, -0.020 * bob))                                  # final85 C3: bob 0.020, roll 4 deg
        k.key("Chest", f, rot=(0, -2.5 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(2.0 + 1.5 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(2.0 + 2.0 * pk.wave(f, n, 0.20, 2), -2.0 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(1.5, 0, 0))
        ears(k, f, -3.0)
        thorns(k, f, 0.0, wave=2.0, n=n)
        k.key("Tail1", f, rot=(3.0 * pk.wave(f, n, 0.3, 2), 10.0 * pk.wave(f, n, 0.25), 0))
    return cm.quad_walk(k, n, 0.075, 0.040, body, gait="trot")


def roar(k):
    """HUNKER GROWL (ref B): the shoulders drop first (the rump follows), thorns flatten back 22 deg, ears back; the
    head goes low and forward with the face level at the threat and the jaw opens to the fangs (a low growl with a
    small tremble); it rises slower than it dropped."""
    n = 60
    k.new_action("roar", n, False)
    SH = [(0, 0.0), (12, 1.0), (45, 1.0), (58, 0.0), (60, 0.0)]           # shoulders lead
    RP = [(0, 0.0), (3, 0.0), (15, 1.0), (45, 1.0), (60, 0.0)]            # rump lags 3 f
    HD = [(0, 0.0), (8, 0.3), (22, 1.0), (45, 1.0), (57, 0.0), (60, 0.0)]
    JW = [(0, 1.5), (18, 1.5), (28, 24.0), (42, 24.0), (52, 1.5), (60, 1.5)]
    TH = [(0, 0.0), (12, 1.0), (46, 1.0), (56, 0.0), (60, 0.0)]
    drop = 0.10 * H_U                                                   # review 3 M-1: 0.10H (was 0.05H)
    for f in range(0, n + 1):
        sh, rp, hd = tab(SH, f), tab(RP, f), tab(HD, f)
        tr = 2.5 * math.sin(2 * math.pi * f / 4) if 24 <= f <= 42 else 0.0          # final85 T3: 2.5 deg
        k.key("Spine", f, rot=(3.0 * (sh - rp) + 2.0 * sh, 0, 0), loc=(0, -0.012 * sh, -drop * (0.6 * sh + 0.4 * rp)))
        k.key("Chest", f, rot=(1.5 * sh, 0, 0))
        k.key("Neck", f, rot=(7.0 * hd, 0, 0))                           # low and thrust forward (ref B):
        k.key("Head", f, rot=(-4.0 * hd + 0.4 * tr, 0, 0))               # the face stays level at the threat
        k.key("Jaw", f, rot=(tab(JW, f) + tr, 0, 0))
        ears(k, f, -28.0 * tab(TH, f))
        thorns(k, f, -22.0 * tab(TH, f))
        k.key("Tail1", f, rot=(-8.0 * rp, 0, 0))
    cm.plant(k, n)
    k.finish(loop=False)
    k.events["roar"] = {"growl": round(30 / n, 3)}


def burrow(k):
    """SIGNATURE act_burrow - DIG THE BURROW (refs A + C): a quick nose-tap on the spot, then straight into three
    forepaw scoops L/R/L with the head low over the hole (each lifts <= 0.05H, sweeps back along the ground: dirt flies
    on the sweep); two hind kicks spray the dirt back; the head pops up and looks slowly right then left with the crest
    raised; back to the exact rest pose. (review 3: M-2 tap + scoop at f8, M-3 slow look, N-1..N-3 kicks)"""
    import bpy
    n = 100
    k.new_action("act_burrow", n, False)
    DN = [(0, 0.0), (4, 0.45), (8, 0.25), (14, 0.75), (52, 0.75), (56, 0.5), (61, -0.25), (88, -0.25), (96, 0.0),
          (100, 0.0)]                                                       # tap f0-8, low over the hole, pop up
    YW = [(0, 0.0), (60, 0.0), (68, 14.0), (72, 14.0), (86, -14.0), (90, -14.0), (98, 0.0), (100, 0.0)]  # slow look
    RK = [(0, 0.0), (8, 0.0), (12, 1.0), (20, -1.0), (30, 1.0), (38, 0.0), (41, 0.0), (45, 1.0), (50, 0.0),
          (54, -1.0), (59, 0.0), (100, 0.0)]                                # body rock toward the support side
    TH = [(0, 0.0), (56, 0.0), (61, 1.0), (88, 1.0), (95, 0.0), (100, 0.0)]
    for f in range(0, n + 1):
        d, yw, rk = tab(DN, f), tab(YW, f), tab(RK, f)
        kick = 1.0 if 41 <= f <= 59 else 0.0
        k.key("Spine", f, rot=(4.0 * max(d, 0.0) + 1.5 * kick, 0, 2.5 * rk), loc=(0, 0, -0.010 * max(d, 0.0)))
        k.key("Chest", f, rot=(1.0 * max(d, 0.0), 0, -1.0 * rk))
        k.key("Neck", f, rot=(8.0 * d, 0.40 * yw, 0))
        k.key("Head", f, rot=(17.0 * d, 0.60 * yw, 0))
        k.key("Jaw", f, rot=(1.5, 0, 0))
        ears(k, f, -6.0 * max(d, 0.0) + 6.0 * max(-d, 0.0) * 4)
        thorns(k, f, 3.0 * tab(TH, f), wave=(1.5 if 8 <= f <= 59 else 0.0), n=10)
        k.key("Tail1", f, rot=(6.0 * max(d, 0.0), 8.0 * rk, 0))
    k.bake_bezier_now()

    # forepaw scoop: (dy, lift) through the scoop, 10 f: reach forward + lift <= 0.05H, contact, sweep back, return
    SC = [(0, (0.0, 0.0)), (3, (-0.056, 0.026)), (5, (-0.064, 0.0)), (8, (0.032, 0.0)), (10, (0.0, 0.0))]  # T4
    # hind kick, 9 f: shove back 0.070 + lift 0.028 (N-2 / N-3), touch down, step home with a small lift
    KICK = [(0, (0.0, 0.0)), (3, (0.070, 0.028)), (5, (0.058, 0.0)), (7, (0.028, 0.012)), (9, (0.0, 0.0))]  # review 4 NICE
    KT = {"Leg_BL": 41, "Leg_BR": 50}

    def paw(f, f0, T):
        if f0 <= f <= f0 + T[-1][0]:
            return tab(T, f - f0)
        return (0.0, 0.0)

    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        fl = paw(f, 8, SC) if f < 18 else paw(f, 28, SC)
        T = {"Leg_FL": fl, "Leg_FR": paw(f, 18, SC), "Leg_BL": paw(f, KT["Leg_BL"], KICK),
             "Leg_BR": paw(f, KT["Leg_BR"], KICK)}
        for leg in LEGS4:
            dy, lift = T[leg]
            toe = (-7.0 * lift / 0.028) if leg in KT else None                # N-1: kick toe up, never into the grass
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y + dy, lift)), toe=toe)
    k.finish(loop=False)
    k.events["act_burrow"] = {"dig1": round(16 / n, 3), "dig2": round(26 / n, 3), "dig3": round(36 / n, 3),
                              "kick1": round(44 / n, 3), "kick2": round(53 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    burrow(k)
    return stride


HEAD_XF = []
