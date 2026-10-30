# Raiju (Thunder egg) - FIERCE style (2026-10-09, owner: the chibi pets look "for babies"; refs _refs/fierce/f_*):
# a real storm wolf built from tapered blocks and covered in Roblox studs (blockkit.stud_skin): real wolf anatomy
# (deep chest, tucked waist, long jointed legs, long snout, normal-size head), narrow yellow eyes under a heavy brow,
# bared fangs, swept cheek ruff + hackle spikes, yellow lightning stripes, a bushy tail ending in a bolt.
# Old chibi version: _tools/Raiju_chibi_backup_20261009.py
import math
from mathutils import Vector

DISPLAY = "Raijū"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.0

FUR = (80, 102, 182)        # storm blue (Roblox renders it ~0.6x darker -> dark storm navy in game)
FUR_D = (46, 54, 104)       # back / ruff / ear backs
PALE = (162, 182, 228)      # chest, belly, muzzle (lighter underside like a real wolf)
BOLT = (255, 202, 36)
EYE = (255, 206, 40)
EYE_HOT = (255, 246, 176)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
MOUTH = (86, 18, 30)

PITCH = 0.042               # stud pitch (Blender units)

# leg joints (left side): hip/shoulder, knee/elbow, ankle/wrist, paw centre
LEGS = {"F": ((0.145, -0.36, 0.76), (0.145, -0.27, 0.45), (0.145, -0.35, 0.11), (0.145, -0.40, 0.045)),
        "B": ((0.15, 0.36, 0.78), (0.15, 0.23, 0.47), (0.15, 0.44, 0.21), (0.15, 0.38, 0.045))}
TAILP = [(0, 0.50, 0.94), (0, 0.68, 0.84), (0, 0.83, 0.67), (0, 0.92, 0.46)]


def X(p, s):
    return (s * p[0], p[1], p[2])


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=11, tier=3, plates=False)
    # ---------------- torso: deep ribcage that tapers underneath, a sloped tuck up to a narrow waist, muscular rump
    # (owner 2026-10-09: "make the stomach look less like a BOX")
    B.add((0, -0.26, 0.76), (0.20, 0.34, 0.25), FUR, "Chest", bot=(0.66, 0.56), top=(0.90, 0.95), rnd=0.30)  # ribcage
    B.add((0, -0.37, 0.975), (0.17, 0.22, 0.07), FUR_D, "Chest", top=(0.70, 0.80))                    # withers
    B.seg((0, -0.16, 0.60), (0, 0.24, 0.715), 0.135, 0.085, FUR, "Spine", top=(0.82, 0.75), bot=(1, 1),
          side=(1, 0, 0))                                                                              # sloped tuck
    B.add((0, 0.10, 0.83), (0.15, 0.22, 0.15), FUR, "Spine", bot=(0.72, 0.70), top=(0.95, 1), rnd=0.30)  # waist
    B.add((0, 0.34, 0.81), (0.168, 0.19, 0.175), FUR, "Spine", rot=(-8, 0, 0), top=(0.84, 0.90), bot=(0.85, 0.9))
    B.add((0, 0.06, 0.968), (0.11, 0.28, 0.025), FUR_D, "Spine")                                       # dark saddle
    # pale underside: brisket -> sloped belly line (follows the tuck), pale chest front
    B.add((0, -0.27, 0.515), (0.12, 0.17, 0.025), PALE, "Chest", bot=(0.8, 0.9), studs=[])
    B.seg((0, -0.16, 0.523), (0, 0.22, 0.637), 0.095, 0.022, PALE, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    B.add((0, -0.538, 0.79), (0.15, 0.03, 0.15), PALE, "Chest", bot=(0.5, 1), top=(0.9, 1), rot=(15, 0, 0))  # chest front
    # (seated ON the ribcage's sloped front face: the face leans 15 deg, top forward)
    # ---------------- neck + hackles
    B.seg((0, -0.48, 0.84), (0, -0.76, 1.08), 0.145, 0.16, FUR, "Neck", ext=0.06)
    B.seg((0, -0.56, 0.78), (0, -0.80, 0.98), 0.12, 0.08, PALE, "Neck", side=(1, 0, 0), ext=0.02)  # pale throat
    # ---------------- head (pivot at the throat): skull, long tapered snout, heavy brow, narrow eyes
    head = B.add((0, -0.90, 1.17), (0.145, 0.13, 0.115), FUR, "Head", top=(0.82, 0.85))
    B.add((0, -0.86, 1.285), (0.11, 0.11, 0.03), FUR_D, "Head", top=(0.8, 0.8))                # dark crown
    B.seg((0, -0.99, 1.125), (0, -1.30, 1.10), 0.088, 0.072, FUR, "Head", top=(0.72, 0.80), ext=0.02)   # snout
    B.seg((0, -1.00, 1.065), (0, -1.28, 1.06), 0.082, 0.026, PALE, "Head", top=(0.75, 0.9))    # pale upper lip
    B.add((0, -1.305, 1.145), (0.042, 0.024, 0.030), BLACK, "Head", role="detail", bevel=0.01)  # nose
    # upper fangs + teeth along the lip
    for s in (1, -1):
        B.spike((s * 0.050, -1.235, 1.05), (0, 0, -1), 0.075, 0.016, TEETH, "Head")             # canine
        for y in (-1.17, -1.11, -1.05):
            B.spike((s * 0.062, y, 1.05), (0, 0, -1), 0.035, 0.012, TEETH, "Head")
    # lower jaw (opens in the roar) + lower fangs + dark mouth
    B.seg((0, -0.97, 1.02), (0, -1.25, 1.015), 0.072, 0.026, PALE, "Jaw", top=(0.8, 1), ext=0.02)
    B.add((0, -1.11, 1.048), (0.058, 0.12, 0.008), MOUTH, "Jaw", studs=[], role="detail", bevel=0.004)
    for s in (1, -1):
        B.spike((s * 0.042, -1.225, 1.04), (0, 0, 1), 0.05, 0.013, TEETH, "Jaw")
    # heavy angled brows + narrow glowing-yellow eyes (no Neon: bright solid colours)
    for s in (1, -1):
        B.add((s * 0.075, -1.002, 1.245), (0.07, 0.03, 0.028), FUR_D, "Head", rot=(0, -s * 20, 0), role="detail",
              bevel=0.01)
        B.add((s * 0.082, -1.028, 1.198), (0.055, 0.008, 0.026), BLACK, "Head", rot=(0, -s * 18, 0), studs=[],
              role="detail", bevel=0.004)
        B.add((s * 0.084, -1.035, 1.198), (0.046, 0.006, 0.014), EYE, "Head", rot=(0, -s * 18, 0), studs=[],
              role="detail", bevel=0.003)
        B.add((s * 0.090, -1.040, 1.200), (0.020, 0.004, 0.007), EYE_HOT, "Head", rot=(0, -s * 18, 0), studs=[],
              role="detail", bevel=0.002)
    # cheek ruff: swept-back fur spikes from the jaw line
    for s in (1, -1):
        for z, dz, L, w in ((1.07, -0.35, 0.13, 0.042), (1.14, -0.05, 0.15, 0.046), (1.21, 0.2, 0.12, 0.04)):
            root = Vector((s * 0.115, -0.90, z))
            B.spike(root, (s * 0.38, 0.92, dz), L, w, FUR_D, "Head", top=(0.12, 0.4))
    # ears: tall, pointed, pinned slightly back, pale inner
    for s, side in ((1, "L"), (-1, "R")):
        ear = B.add((s * 0.09, -0.82, 1.39), (0.055, 0.025, 0.11), FUR_D, "Ear_" + side, rot=(-18, s * 8, -s * 14),
                    top=(0.10, 0.5))
        B.add(ear.world((0, -0.027, -0.015)), (0.034, 0.006, 0.075), PALE, "Ear_" + side, R=ear.R, top=(0.12, 1),
              studs=[], role="detail", bevel=0.004)
    # neck ruff + hackle spikes down the back (dark, swept back)
    for y, z, L, ang, bone in ((-0.74, 1.22, 0.16, -50, "Neck"), (-0.64, 1.16, 0.18, -55, "Neck"),
                               (-0.52, 1.08, 0.18, -60, "Chest"), (-0.38, 1.05, 0.16, -65, "Chest"),
                               (-0.22, 1.02, 0.14, -68, "Chest"), (-0.06, 1.0, 0.12, -70, "Spine"),
                               (0.10, 0.99, 0.10, -72, "Spine")):
        d = Vector((0, math.sin(math.radians(-ang)), math.cos(math.radians(-ang))))
        B.spike((0, y, z - 0.04), d, L, 0.06, FUR_D, bone, top=(0.15, 0.25))
    for s in (1, -1):                                   # side ruff around the neck
        for y, z, L in ((-0.64, 0.97, 0.16), (-0.66, 1.08, 0.14)):
            B.spike((s * 0.11, y, z), (s * 0.35, 0.9, -0.1), L, 0.05, FUR_D, "Neck", top=(0.12, 0.35))
    # ---------------- legs: upper (in the body), lower, paw with black claws; yellow bolt stripes
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.08)), K, 0.066, 0.095, FUR, leg, ext=0.0, ext1=0.03, top=(0.85, 0.72))  # upper arm
                B.seg(K, A, 0.058, 0.064, FUR, shin, top=(0.85, 0.85), ext=0.03, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.03, 0.08)), K, 0.082, 0.14, FUR, leg, bot=(0.85, 1), top=(0.75, 0.62),
                      ext=0.0, ext1=0.03)                                                      # thigh
                B.seg(K, A, 0.06, 0.07, FUR, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02)
                B.seg(A, P + Vector((0, 0.03, 0.03)), 0.048, 0.052, FUR, foot, ext=0.03)          # hock -> paw
            B.add(P, (0.068, 0.085, 0.045), FUR_D, foot, top=(0.85, 0.80))                      # paw
            for gx in (-0.042, -0.014, 0.014, 0.042):
                B.spike((P.x + gx, P.y - 0.075, 0.035), (0, -1, -0.55), 0.06, 0.013, BLACK, foot)
            # bolt stripe on the outer side of the lower leg
            n = Vector((s, 0, 0))
            if fb == "F":
                zs = [(K + (A - K) * t) for t in (0.15, 0.45, 0.62, 0.90)]
                w = 0.058
            else:
                zs = [(K + (A - K) * t) for t in (0.10, 0.40, 0.58, 0.88)]
                w = 0.06
            pts = [Vector((z.x + s * (w + 0.004), z.y + dy, z.z)) for z, dy in zip(zs, (0.0, 0.03, -0.03, 0.0))]
            for i, (a, b) in enumerate(zip(pts, pts[1:])):
                B.bar(a, b, n, 0.032, 0.010, BOLT, shin, studs=[], bevel=0.004, top=(1, 0.15) if i == 2 else (1, 1))
    # ---------------- lightning stripes down the flanks (shoulder -> waist) and on the thighs
    for s in (1, -1):
        n = Vector((s, 0, 0))
        fl = [(-0.46, 0.92), (-0.30, 0.76), (-0.18, 0.84), (-0.02, 0.66)]
        P = [Vector((s * (0.213 if y < -0.05 else 0.172), y, z)) for y, z in fl]
        for i, (a, b) in enumerate(zip(P, P[1:])):
            B.bar(a, b, n, 0.055, 0.012, BOLT, "Chest", studs=[], bevel=0.005, top=(1, 0.12) if i == 2 else (1, 1))
        th = [(0.26, 0.92), (0.35, 0.81), (0.28, 0.73), (0.40, 0.62)]
        P = [Vector((s * 0.176, y, z)) for y, z in th]
        for i, (a, b) in enumerate(zip(P, P[1:])):
            B.bar(a, b, n, 0.05, 0.012, BOLT, "Spine", studs=[], bevel=0.005, top=(1, 0.12) if i == 2 else (1, 1))
    # ---------------- bushy tail hanging back, ending in a yellow bolt tip
    T = [Vector(p) for p in TAILP]
    for (a, b), (w, d), bn, tp in zip(zip(T, T[1:]), ((0.045, 0.05), (0.07, 0.075), (0.07, 0.075)),
                                      ("Tail1", "Tail2", "Tail3"), ((1.4, 1.4), (1.0, 1.0), (0.6, 0.6))):
        B.seg(a, b, w, d, FUR, bn, top=tp, ext=0.04)
    for t, L in ((0.3, 0.12), (0.7, 0.11)):                     # bushy fur flicks along the tail top
        p = T[1] + (T[2] - T[1]) * t
        B.spike(p + Vector((0, -0.01, 0.04)), (0, 0.8, 0.45), L, 0.045, FUR_D, "Tail2", top=(0.15, 0.3))
    tip = T[3]
    B.seg(tip + Vector((0, -0.03, 0.07)), tip + Vector((0, 0.04, -0.15)), 0.055, 0.028, BOLT, "Tail3",
          top=(0.1, 1), side=(1, 0, 0))
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.20, 0.80), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.10, 0.80), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.50, 0.88), "Chest", tail=(0, -0.2, 0.2))
    k.joint("Head", (0, -0.76, 1.06), "Neck", tail=(0, -0.35, 0.05))          # throat pivot
    k.joint("Jaw", (0, -0.97, 1.045), "Head", tail=(0, -0.3, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.09, -0.82, 1.29), "Head", tail=(0, 0, 0.2))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2", tail=(0, 0.05, -0.2))


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Head", "Chest"), ("Jaw", "Chest"), ("Ear_L", "Ear_R"),
         ("Head", "Shin_FL"), ("Head", "Shin_FR"), ("Jaw", "Shin_FL"), ("Jaw", "Shin_FR"),
         ("Tail2", "Shin_BL"), ("Tail2", "Shin_BR"), ("Tail3", "Shin_BL"), ("Tail3", "Shin_BR"),
         ("Tail3", "Foot_BL"), ("Tail3", "Foot_BR")]
    return P


def joints():
    return [((0, -0.72, 1.02), (0, -0.80, 1.10), 0.24, "Head"), ((0.09, -0.82, 1.29), (-0.09, -0.82, 1.29), 0.08, "Head")]


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm
TAIL = ["Tail1", "Tail2", "Tail3"]


def ears(k, f, l=0.0, r=None, splay=0.0):
    r = l if r is None else r
    k.key("Ear_L", f, rot=(l, 0, splay))
    k.key("Ear_R", f, rot=(r, 0, -splay))


def idle(k):
    """Alpha sentinel: scans left and right with snappy turns and holds, ear flicks, lips curl into a snarl, tail
    sways low, then lifts its chest and chin high before settling again."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.008 * b))
        k.key("Chest", f, rot=(-1.0 - 1.0 * b, 0, 0))
        cm.chain(k, f, n, TAIL, sway=6, pitch=0, cycles=2, lag=0.12, grow=0.5)
        k.key("Jaw", f, rot=(2 + 2 * pk.wave(f, n, 0, 10), 0, 0))
    for f, nk, hd, yaw, tilt in ((0, -2, -2, 0, 0), (22, -2, -2, 0, 0), (28, -4, 0, 26, 4), (48, -4, 0, 26, 4),
                                 (54, -2, -4, -22, -3), (74, -2, -4, -22, -3), (80, -2, -2, 0, 0),
                                 (86, -2, -2, 0, 0), (92, -10, -6, 0, 0), (106, -10, -6, 0, 0), (114, -2, -2, 0, 0),
                                 (120, -2, -2, 0, 0)):
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, tilt))
    for f, l, r in ((0, 0, 0), (26, 6, 6), (38, 6, 6), (40, 6, -22), (43, 6, 6), (46, 6, -16), (50, 6, 6),
                    (64, 4, 4), (66, -22, 4), (70, 4, 4), (82, 0, 0), (120, 0, 0)):
        ears(k, f, l, r)
    for f, ch in ((84, -1.0), (92, -6), (106, -6), (114, -1.0)):
        k.key("Chest", f, rot=(ch, 0, 0))
    cm.plant(k, n)
    k.finish()


def walk(k):
    n = 22

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 0, 2.0 * pk.wave(f, n)), loc=(0, 0, 0.015 * b))
        k.key("Chest", f, rot=(-1.0, 3.0 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n)))
        k.key("Neck", f, rot=(2 + 2.0 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(-1 - 2.0 * pk.wave(f, n, 0.2, 2), -2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(3 + 2 * pk.wave(f, n, 0, 2), 0, 0))
        ears(k, f, -8, -8)
        cm.chain(k, f, n, TAIL, sway=8, pitch=-3, cycles=1, lag=0.15)
    return cm.quad_walk(k, n, 0.17, 0.08, body, gait="trot")


def roar(k):
    """HOWL: leans back, chin to the sky, jaw wide open, ears pinned back, tail lifts and buzzes."""
    n = 66
    k.new_action("roar", n, False)
    P = [(0, 0, -2, -2, 2, 0), (10, -5, -12, -10, 6, 0.4), (20, -8, -24, -26, 26, 1), (48, -8, -26, -28, 28, 1),
         (56, -3, -10, -8, 8, 0.3), (66, 0, -2, -2, 2, 0)]
    for f, ch, nk, hd, jw, t in P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, -0.02 * t))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        ears(k, f, -30 * t, -30 * t)
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(-14 * t, 0, 0))
    for f in range(22, 48, 2):
        w = 1 if (f // 2) % 2 else -1
        k.key("Head", f, rot=(-27, 0, 2.5 * w))
        k.key("Tail3", f, rot=(-14, 7 * w, 0))
    cm.plant(k, n)
    k.finish(loop=False)


def thunderflip(k):
    """SIGNATURE (Raiju only): crouches low with ears pinned, EXPLODES upward into a full barrel roll with all four
    legs tucked, lands on all fours and holds a proud power pose (chest high, chin up, tail raised)."""
    import bpy
    n = 64
    k.new_action("act_thunderflip", n, False)
    Y = (0, 1, 0)
    P = [(0, 0.0, 0, 0, -2, -2, 0, 0), (8, -0.06, 0, 4, 2, -2, -20, 4), (14, -0.09, 0, 6, 4, 0, -30, 4),
         (18, 0.30, 0, -4, -6, -6, -30, -8), (21, 0.70, 90, -2, -6, -6, -30, -10), (24, 0.95, 180, 0, -4, -6, -30, -10),
         (27, 0.95, 270, 0, -4, -6, -30, -10), (30, 0.70, 360, -2, -6, -6, -26, -6), (34, 0.18, 360, -4, -12, -10, -10, 0),
         (38, -0.06, 360, 2, -6, -6, 0, 0), (44, 0.0, 360, -6, -10, -8, 10, -14), (56, 0.0, 360, -6, -10, -8, 10, -14),
         (64, 0.0, 360, 0, -2, -2, 0, 0)]
    for f, z, roll, ch, nk, hd, ear, tp in P:
        cm.key_axis(k, "Spine", f, Y, roll, loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(14 if 44 <= f <= 56 else 2, 0, 0))
        ears(k, f, ear, ear)
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(tp, 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in list(range(0, 17)) + list(range(36, n + 1)):
        sc.frame_set(f)
        for leg in cm.LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f, front, back, spl in ((18, 30, 34, 0), (22, 16, -16, 12), (30, 16, -16, 12), (34, 0, 4, 2)):
        for leg in cm.LEGS4:
            sx = 1 if leg.endswith("L") else -1
            k.key(leg, f, rot=(front if "_F" in leg else back, 0, -sx * spl), loc=(0, 0, 0))
            sh = leg.replace("Leg_", "Shin_")
            k.key(sh, f, rot=((-40 if "_F" in leg else 50) * (1 if f in (22, 30) else 0.4), 0, 0))
            k.key(leg.replace("Leg_", "Foot_"), f, rot=(0, 0, 0))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    thunderflip(k)
    return stride


HEAD_XF = []
