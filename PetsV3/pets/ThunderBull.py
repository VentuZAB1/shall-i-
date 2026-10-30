# Thunder Bull (Thunder egg) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the storm bison"): an American bison x gaur
# bull built from tapered blocks and covered in Roblox studs: a massive shoulder hump, the back sloping down to lean
# hindquarters, a deep keel chest with a rising belly line, the broad head held LOW, horns curving out-up-forward in 3
# tapered segments, a dark shaggy cape (head, hump, shoulders, front-leg chaps) ending in a ragged shingle edge at
# mid-ribcage, a beard, split hooves, a thin tail with a tuft, and branching electric-blue Lichtenberg scars on the hump
# and both flanks. Narrow slanted blue eyes under a heavy brow. No glow (storm cloud + sparks = Studio VFX).
# Old chibi version: _tools/chibi_specs/ThunderBull.py
import math
from mathutils import Vector, Matrix

DISPLAY = "Thunder Bull"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 6.5                # hump/withers ~6.5 studs at x1 (coordinator HEIGHT rule 2026-10-09)

# FIERCE_PLAN palette is the in-game look; Roblox renders ~0.55-0.6x darker, so the Blender colours are ~1.8x brighter
BODY = (98, 108, 178)       # hindquarters (plan 52,58,92)
CAPE = (54, 58, 106)        # shaggy cape: head, hump, shoulders, chaps (plan 34,36,62)
CAPE_D = (38, 40, 74)       # brows, beard, topknot, tuft
PALE = (140, 150, 206)      # muzzle + belly (plan 96,104,140)
HORN = (228, 222, 202)
HORN_T = (40, 40, 54)
HOOF = (20, 20, 30)
SCAR = (70, 190, 255)       # accent: Lichtenberg scars + eyes
EYE = (70, 190, 255)
EYE_HOT = (190, 233, 255)
BLACK = (14, 14, 22)
NOSE = (30, 30, 46)
MOUTH = (86, 18, 30)
TEETH = (238, 234, 220)

H_MODEL = 1.07              # model height (hump top) in Blender units
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)   # same world stud size as the Raiju

# leg joints (left side): shoulder/hip, elbow/stifle, carpus/hock, hoof centre
LEGS = {"F": ((0.165, -0.34, 0.70), (0.165, -0.24, 0.42), (0.165, -0.335, 0.18), (0.165, -0.37, 0.04)),
        "B": ((0.150, 0.47, 0.70), (0.150, 0.35, 0.47), (0.150, 0.55, 0.27), (0.150, 0.48, 0.04))}
TAILP = [(0, 0.66, 0.80), (0, 0.72, 0.64), (0, 0.745, 0.48), (0, 0.75, 0.36)]
HEAD_O = Vector((0, -0.92, 0.63))     # head frame origin; the face looks forward-up (head held low, nose down)
HEAD_P = -42.0                        # head frame pitch (deg): local -y = face normal, local +z = up the face


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def Rx(d):
    return Matrix.Rotation(math.radians(d), 3, "X")


def Ry(d):
    return Matrix.Rotation(math.radians(d), 3, "Y")


def Rz(d):
    return Matrix.Rotation(math.radians(d), 3, "Z")


RH = Rx(HEAD_P)


def hp(p):
    """head-frame point -> world"""
    return HEAD_O + RH @ Vector(p)


def hadd(B, p, half, color, bone="Head", yaw=0.0, roll=0.0, pitch=0.0, **kw):
    """block in the head frame (yaw about the face's up axis, roll in the face plane)"""
    return B.add(hp(p), half, color, bone, R=RH @ Rx(pitch) @ Rz(yaw) @ Ry(roll), **kw)


def side_pt(blk, s, y, z, out=0.004):
    """point + outward normal on the +-x face of a (tapered, rotated) block at block-local (y, z)"""
    t = (z / blk.h.z + 1) / 2
    sx = blk.bot[0] + (blk.top[0] - blk.bot[0]) * t
    dxdz = blk.h.x * (blk.top[0] - blk.bot[0]) / (2 * blk.h.z)
    n = (blk.R @ Vector((s, 0, -dxdz))).normalized()
    return blk.world((s * blk.h.x * sx, y, z)) + n * out, n


def scar(B, blk, s, pts, width, bone, thick=0.012):
    """branch of flat bars along block-local (y, z) points on the +-x face; the last bar ends in a point"""
    P = [side_pt(blk, s, y, z) for y, z in pts]
    for i in range(len(P) - 1):
        (a, na), (b, nb) = P[i], P[i + 1]
        d = (b - a).normalized()
        a2 = a - d * (width * 0.35 if i else 0.0)
        B.bar(a2, b, (na + nb).normalized(), width, thick, SCAR, bone, studs=[], bevel=0.004,
              top=(1, 0.15) if i == len(P) - 2 else (1, 1))


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=31, tier=3, plates=False)
    # ---------------- torso: deep keel ribcage tapering underneath, sloped tuck up to a narrower waist, lean hips
    rib = B.add((0, -0.23, 0.70), (0.25, 0.33, 0.25), BODY, "Chest", bot=(0.66, 0.56), top=(0.90, 0.95), rnd=0.40)
    B.seg((0, -0.14, 0.555), (0, 0.30, 0.665), 0.17, 0.09, BODY, "Spine", top=(0.82, 0.75), side=(1, 0, 0))  # tuck
    waist = B.add((0, 0.19, 0.72), (0.19, 0.22, 0.15), BODY, "Spine", bot=(0.72, 0.70), top=(0.94, 1), rnd=0.30)
    hips = B.add((0, 0.50, 0.69), (0.175, 0.19, 0.13), BODY, "Spine", rot=(-8, 0, 0), top=(0.84, 0.90),
                 bot=(0.85, 0.9))
    # pale belly strip following the tuck
    B.seg((0, -0.12, 0.468), (0, 0.28, 0.578), 0.11, 0.022, PALE, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    # ---------------- shaggy cape over the forequarters + a rounded hump peaking over the shoulders, sloping back
    cape = B.add((0, -0.37, 0.72), (0.27, 0.22, 0.265), CAPE, "Chest", bot=(0.70, 0.62), top=(0.78, 0.86),
                 rnd=0.42)
    hump = B.add((0, -0.26, 0.935), (0.20, 0.28, 0.13), CAPE, "Chest", rot=(-4, 0, 0), top=(0.50, 0.56),
                 rnd=0.45)
    B.add((0, 0.02, 0.85), (0.165, 0.20, 0.075), CAPE, "Chest", rot=(-13, 0, 0), top=(0.80, 0.92), rnd=0.45)   # mane
    # ragged shingle edge of the cape: pointed fur locks lying flush on the ribcage flank, staggered lengths
    for s in (1, -1):
        edge = [(-0.24, 0.70), (-0.24, 0.90), (-0.04, 0.89), (-0.12, 0.81), (0.03, 0.74), (-0.09, 0.67),
                (-0.01, 0.58), (-0.12, 0.54), (-0.07, 0.48), (-0.24, 0.50)]
        B.poly([side_pt(rib, s, y - rib.c.y, z - rib.c.z, 0.016)[0] for y, z in edge], 0.032, CAPE, "Chest")
        for y in (-0.42, -0.30):                                                              # brisket hem
            B.spike((s * 0.10, y, 0.47), (s * 0.25, 0.8, -1), 0.08, 0.065, CAPE_D, "Chest", top=(0.2, 0.45))
    # ---------------- neck (short, thick, hanging forward-down) + throat
    B.seg((0, -0.48, 0.84), (0, -0.82, 0.68), 0.17, 0.17, CAPE, "Neck", ext=0.04)
    # ---------------- head (pivot at the throat), held low: skull, broad pale muzzle, heavy brow, slit eyes
    hadd(B, (0, 0.0, 0.06), (0.17, 0.14, 0.18), CAPE, top=(0.78, 0.80), rnd=0.38)                # skull
    hadd(B, (0, 0.04, 0.24), (0.14, 0.12, 0.06), CAPE, top=(0.75, 0.8), rnd=0.45)                 # woolly crown
    for x, dy, L in ((0.0, -0.25, 0.13), (0.075, 0.1, 0.11), (-0.075, 0.1, 0.11), (0.0, 0.45, 0.10)):   # wool tufts
        B.spike(hp((x, 0.02, 0.27)), RH @ Vector((x * 1.5, dy, 1)), L, 0.045, CAPE_D, "Head", top=(0.2, 0.4))
    hadd(B, (0, -0.045, -0.16), (0.125, 0.12, 0.095), PALE, bot=(0.74, 0.80), top=(0.95, 1), rnd=0.34)  # muzzle
    hadd(B, (0, -0.166, -0.125), (0.085, 0.008, 0.042), NOSE, bot=(0.8, 1), studs=[], role="detail",
         bevel=0.006)                                                                               # nose pad
    for s_ in (1, -1):
        hadd(B, (s_ * 0.055, -0.175, -0.128), (0.012, 0.004, 0.02), BLACK, roll=s_ * 25, studs=[], role="detail",
             bevel=0.003)                                                                           # nostril slits
    # lower jaw (opens in the bellow) + dark mouth + blunt lower teeth
    jaw = hadd(B, (0, 0.07, -0.215), (0.105, 0.085, 0.032), PALE, bone="Jaw", bot=(0.85, 0.9))
    hadd(B, (0, 0.02, -0.182), (0.085, 0.075, 0.006), MOUTH, bone="Jaw", studs=[], role="detail", bevel=0.003)
    for x in (-0.05, -0.017, 0.017, 0.05):
        hadd(B, (x, -0.045, -0.177), (0.012, 0.008, 0.012), TEETH, bone="Jaw", studs=[], role="detail", bevel=0.003)
    # heavy angled brow ridge + narrow slanted eyes (black socket, accent slit, hot centre on the outer half)
    for s in (1, -1):
        hadd(B, (s * 0.090, -0.150, 0.088), (0.082, 0.036, 0.030), CAPE_D, yaw=s * 18, roll=-s * 24,
             role="detail", bevel=0.012)                                                           # brow
        hadd(B, (s * 0.100, -0.133, 0.036), (0.060, 0.024, 0.024), BLACK, yaw=s * 24, roll=-s * 22, studs=[],
             role="detail", bevel=0.005)                                                           # socket
        hadd(B, (s * 0.102, -0.152, 0.036), (0.050, 0.007, 0.012), EYE, yaw=s * 24, roll=-s * 22, studs=[],
             role="detail", bevel=0.003)                                                           # slit
        hadd(B, (s * 0.118, -0.159, 0.039), (0.020, 0.004, 0.007), EYE_HOT, yaw=s * 24, roll=-s * 22, studs=[],
             role="detail", bevel=0.002)                                                           # hot centre
    # short beard rooted on the throat (continues the neck line)
    B.seg(hp((0, 0.12, -0.18)), hp((0, 0.15, -0.18)) + Vector((0, 0.04, -0.09)), 0.09, 0.05, CAPE_D, "Head",
          top=(0.5, 0.6), ext=0.03)
    # cheek tufts swept back from the skull sides
    for s in (1, -1):
        for z, dz, L in ((0.0, -0.4, 0.12), (0.10, 0.0, 0.13)):
            B.spike(hp((s * 0.13, 0.06, z)), (s * 0.45, 0.85, dz), L, 0.045, CAPE_D, "Head", top=(0.12, 0.4))
    # horns: 3 tapered segments, out -> up -> forward, ivory with a dark tip (span ~0.85 SH)
    for s in (1, -1):
        h0 = hp((s * 0.12, 0.04, 0.17))
        h1 = h0 + Vector((s * 0.16, 0.02, 0.01))
        h2 = h1 + Vector((s * 0.11, -0.01, 0.10))
        h3 = h2 + Vector((s * 0.025, -0.085, 0.10))
        B.seg(h0, h1, 0.045, 0.045, HORN, "Head", side=(0, 0, 1), ext=0.04, top=(0.85, 0.85), nostud=True)
        B.seg(h1, h2, 0.039, 0.039, HORN, "Head", side=(0, 0, 1), ext=0.02, top=(0.80, 0.80), nostud=True)
        d = h3 - h2
        B.spike(h2 - d.normalized() * 0.02, d, d.length * 0.62 + 0.02, 0.032, HORN, "Head", top=(0.55, 0.55),
                nostud=True)
        B.spike(h2 + d * 0.58, d, d.length * 0.45, 0.018, HORN_T, "Head", nostud=True)
    # small pointed ears sticking out sideways under the horns, pale inside
    for s_, side in ((1, "L"), (-1, "R")):
        root = hp((s_ * 0.15, 0.07, 0.10))
        d = Vector((s_ * 1.0, 0.25, -0.35))
        B.spike(root, d, 0.13, 0.035, CAPE, "Ear_" + side, side=(0, 0, 1), top=(0.25, 0.5), studs=None)
        B.spike(root + d.normalized() * 0.02 + Vector((0, -0.03, 0.0)), d, 0.09, 0.022, PALE, "Ear_" + side,
                side=(0, 0, 1), top=(0.25, 0.4))
    # ---------------- legs: short and thick; shaggy chaps on the front upper legs, split hooves, dew claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.06)), K, 0.08, 0.10, CAPE, leg, ext=0.0, ext1=0.03, top=(0.85, 0.72))
                for y, L in ((-0.05, 0.11), (0.0, 0.13), (0.05, 0.11)):                    # chaps fringe
                    B.spike(K + Vector((s * 0.055, y, 0.10)), (s * 0.3, 0.25, -1), L, 0.045, CAPE, leg,
                            top=(0.12, 0.4))
                B.seg(K, A, 0.068, 0.072, BODY, shin, top=(0.82, 0.85), ext=0.03, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.03, 0.06)), K, 0.08, 0.13, BODY, leg, bot=(0.85, 1), top=(0.72, 0.62),
                      ext=0.0, ext1=0.03)                                                       # lean thigh
                B.seg(K, A, 0.055, 0.065, BODY, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02)
            B.seg(A, P + Vector((0, 0.0, 0.05)), 0.047, 0.05, BODY, foot, ext=0.03, top=(0.9, 0.9))   # cannon
            B.add(P + Vector((0, 0.005, 0.035)), (0.06, 0.058, 0.024), CAPE_D, foot, studs=[])      # pastern
            for gx in (-1, 1):                                                                  # split hoof
                B.add(P + Vector((gx * 0.032, -0.014, -0.002)), (0.029, 0.062, 0.038), HOOF, foot,
                      top=(0.80, 0.70), role="limb", nostud=True)
            for gx in (-1, 1):                                                                  # dew claws
                B.spike(P + Vector((gx * 0.025, 0.045, 0.06)), (0, 1, -0.6), 0.035, 0.012, HOOF, foot)
    # ---------------- Lichtenberg scars: a trunk + 3 branches on each flank (waist) and down each side of the hump
    for s in (1, -1):
        scar(B, waist, s, [(-0.14, 0.09), (-0.04, 0.04), (0.02, -0.03), (0.12, -0.08), (0.18, -0.10)], 0.05, "Spine")
        scar(B, waist, s, [(-0.04, 0.04), (0.04, 0.09)], 0.036, "Spine")
        scar(B, waist, s, [(0.02, -0.03), (0.02, -0.10)], 0.036, "Spine")
        scar(B, waist, s, [(0.12, -0.08), (0.17, -0.01)], 0.032, "Spine")
        scar(B, cape, s, [(0.13, 0.19), (0.04, 0.15), (-0.05, 0.13), (-0.12, 0.09)], 0.046, "Chest")
        scar(B, cape, s, [(0.04, 0.15), (0.01, 0.07)], 0.032, "Chest")
        scar(B, hump, s, [(0.17, -0.06), (0.06, -0.02), (-0.04, -0.05), (-0.14, 0.0)], 0.046, "Chest")
        scar(B, hump, s, [(0.06, -0.02), (0.01, -0.10)], 0.032, "Chest")
        scar(B, hump, s, [(-0.04, -0.05), (-0.10, -0.10)], 0.032, "Chest")
    # ---------------- thin tail hanging down, ending in a dark tuft
    T = [Vector(p) for p in TAILP]
    for (a, b), w, bn in zip(zip(T, T[1:]), (0.034, 0.028, 0.024), ("Tail1", "Tail2", "Tail3")):
        B.seg(a, b, w, w, BODY, bn, ext=0.03, top=(0.85, 0.85))
    tip = T[3]
    B.seg(tip + Vector((0, 0, 0.05)), tip + Vector((0, 0.01, -0.09)), 0.04, 0.04, CAPE_D, "Tail3", top=(1.2, 1.2))
    for dx, dy, L in ((0, 0.0, 0.15), (0.6, 0.25, 0.11), (-0.6, 0.25, 0.11), (0, 0.6, 0.10)):   # tuft fan
        B.spike(tip + Vector((0, 0, -0.06)), (dx, dy, -1), L, 0.04, CAPE_D, "Tail3", top=(0.2, 0.3))
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.30, 0.72), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.02, 0.72), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.46, 0.80), "Chest", tail=(0, -0.25, -0.12))
    k.joint("Head", tuple(hp((0, 0.10, -0.10))), "Neck", tail=(0, -0.3, -0.1))         # throat pivot (low/back)
    k.joint("Jaw", tuple(hp((0, 0.13, -0.20))), "Head", tail=(0, -0.25, -0.05))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, tuple(hp((s * 0.14, 0.06, 0.08))), "Head", tail=(s * 0.15, 0, 0))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2", tail=(0, 0.01, -0.2))


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Head", "Chest"), ("Jaw", "Chest"), ("Ear_L", "Ear_R"),
         ("Head", "Leg_FL"), ("Head", "Leg_FR"), ("Head", "Shin_FL"), ("Head", "Shin_FR"), ("Jaw", "Shin_FL"),
         ("Jaw", "Shin_FR"), ("Tail2", "Shin_BL"), ("Tail2", "Shin_BR"), ("Tail3", "Shin_BL"), ("Tail3", "Shin_BR"),
         ("Tail3", "Foot_BL"), ("Tail3", "Foot_BR"), ("Tail2", "Leg_BL"), ("Tail2", "Leg_BR")]
    return P


def joints():
    return [(tuple(hp((0, 0.10, -0.10))), tuple(hp((0, 0.0, 0.0))), 0.20, "Head")]


# ------------------------------------------------------------------ animation (FIERCE_PLAN: cud & flies / broadside
# bellow / scrape & charge). Bull-only motifs: cud grinding, tail fly-swats, the broadside threat turn, the hoof scrape.
import petkit as pk
import _common as cm
from mathutils import Quaternion

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]
TURN_C = Vector((0, 0.10, 0))           # the broadside turn pivots between the front and hind hooves


def ears(k, f, l=0.0, r=None):
    """roll the sideways ears: - = flick up"""
    r = l if r is None else r
    k.key("Ear_L", f, rot=(0, 0, l))
    k.key("Ear_R", f, rot=(0, 0, -r))


def tail(k, f, pitch=0.0, roll=0.0, lag=(1.0, 0.8, 0.6)):
    """pitch + lifts the hanging tail backward, roll - swings it to the left flank"""
    for b, g in zip(TAIL, lag):
        k.key(b, f, rot=(pitch * g, 0, roll * g))


def plant_all(k, f, yaw=0.0, moves=None):
    """IK every hoof; yaw = body turn about TURN_C, moves = {leg: (T, foot_yaw)} overrides"""
    import bpy
    bpy.context.scene.frame_set(f)
    for leg in LEGS4:
        if moves and leg in moves:
            T, fy = moves[leg]
        else:
            T, fy = Vector((k.J[leg].x, k.J[leg].y, 0.0)), 0.0
        k.solve_leg(leg, f, T)
        if fy:
            k._aim("Foot" + leg[3:], f, Quaternion((0, 0, 1), math.radians(fy)))


def turned_T(k, leg, yaw):
    """hip-space IK target of a hoof whose ankle spot is rotated by `yaw` about TURN_C"""
    sh = k.J["Foot" + leg[3:]] - k.J[leg]
    A0 = Vector((k.J[leg].x + sh.x, k.J[leg].y + sh.y, 0.0))
    A = TURN_C + Quaternion((0, 0, 1), math.radians(yaw)) @ (A0 - TURN_C)
    return Vector((A.x - sh.x, A.y - sh.y, 0.0))


def idle(k):
    """CUD & FLIES: heavy breathing while the jaw grinds side to side (3 grinds), the tail swats a fly off the left
    flank (f45) and the right flank (f90), ear flicks, and at 62-88 a slow glare toward the viewer, held."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.007 * b))
        k.key("Chest", f, rot=(-0.8 - 0.8 * b, 0, 0))
        chew = 0.0 if 60 <= f <= 90 else 1.0
        k.key("Jaw", f, rot=(3 + 2.5 * chew * (0.5 + 0.5 * math.sin(2 * math.pi * 6 * f / n)), 6 * chew * math.sin(
            2 * math.pi * 3 * f / n), 0))
    for f, nk, ny, hd, hy in ((0, 0, 0, 0, 0), (58, 0, 0, 0, 0), (68, -3, 10, -6, 20), (86, -3, 10, -6, 20),
                              (98, 0, 0, 0, 0), (120, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, ny, 0))
        k.key("Head", f, rot=(hd, hy, 0))
    for f, p, r in ((0, 0, 0), (38, 0, 0), (42, 22, -38), (45, 30, -46), (48, 18, -30), (54, 4, -4), (60, 0, 0),
                    (83, 0, 0), (87, 22, 38), (90, 30, 46), (93, 18, 30), (99, 4, 4), (105, 0, 0), (120, 0, 0)):
        tail(k, f, p, r)
    for f, l, r in ((0, 0, 0), (20, 0, 0), (22, -24, 0), (25, 0, 0), (66, 0, 0), (70, 10, 10), (86, 10, 10),
                    (92, 0, 0), (104, 0, 0), (106, 0, -24), (109, 0, 0), (120, 0, 0)):
        ears(k, f, l, r)
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 32

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 1.5 * pk.wave(f, n, 0.0), 2.0 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.012 * b))
        k.key("Chest", f, rot=(0, -2 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(2 * pk.wave(f, n, 0.1, 2), 0, 0))
        k.key("Head", f, rot=(-2 * pk.wave(f, n, 0.2, 2), 2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(3, 0, 0))
        tail(k, f, 6, 8 * pk.wave(f, n, 0.3))
        ears(k, f, 4 * pk.wave(f, n, 0.2, 2), 4 * pk.wave(f, n, 0.7, 2))
    return cm.quad_walk(k, n, 0.12, 0.07, body, gait="walk")


def turn_keys(k, frames, yaw_f, step_plan):
    """re-plant every hoof while the body turns about TURN_C; step_plan = {leg: (f0, f1, yaw_from, yaw_to)} lifts
    the hoof in an arc between its old and new spot"""
    for f in frames:
        moves = {}
        for leg in LEGS4:
            f0, f1, y0, y1 = step_plan[leg]
            if f <= f0:
                y, lift = y0, 0.0
            elif f >= f1:
                y, lift = y1, 0.0
            else:
                u = (f - f0) / (f1 - f0)
                e = 0.5 - 0.5 * math.cos(math.pi * u)
                y, lift = y0 + (y1 - y0) * e, 0.07 * math.sin(math.pi * u)
            T = turned_T(k, leg, y)
            moves[leg] = (Vector((T.x, T.y, lift)), y)
        plant_all(k, f, yaw_f(f), moves)


def roar(k):
    """BROADSIDE BELLOW: steps round 35 deg to show its flank, tail raised stiff, head low, the mouth opens 25 deg and
    the bellow pumps the flanks twice; steps back."""
    n = 64
    YAW = -35.0                                          # left flank toward the viewer
    k.new_action("roar", n, False)

    def yaw_at(f):
        if f <= 2:
            return 0.0
        if f < 16:
            return YAW * (0.5 - 0.5 * math.cos(math.pi * (f - 2) / 14))
        if f <= 48:
            return YAW
        if f < 62:
            return YAW * (0.5 + 0.5 * math.cos(math.pi * (f - 48) / 14))
        return 0.0
    for f in range(0, n + 1, 2):
        y = yaw_at(f)
        q = Quaternion((0, 0, 1), math.radians(y))
        rel = k.J["Spine"] - TURN_C
        off = (TURN_C + q @ rel) - k.J["Spine"]
        k.key("Spine", f, rot=(0, y, 0), loc=(off.x, off.y, 0))
    P = [(0, 0, 0, 0, 3, 0, 0), (14, 4, 6, 6, 4, 50, 0.2), (22, 3, 10, 8, 26, 70, 1), (30, 1, 8, 6, 22, 70, 1),
         (36, 3, 10, 8, 27, 70, 1), (44, 1, 8, 6, 22, 70, 1), (50, 2, 4, 2, 6, 40, 0.3), (64, 0, 0, 0, 3, 0, 0)]
    for f, ch, nk, hd, jw, tp, t in P:
        k.key("Chest", f, rot=(ch, 0, 0), loc=(0, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 8 * t, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tail(k, f, tp, 0, lag=(1.0, -0.15, -0.1))
        ears(k, f, 18 * t, 18 * t)
    for f in (24, 38):                                   # the bellow pumps the flanks
        k.key("Chest", f, rot=(5, 0, 0), loc=(0, 0, 0.012))
    k.bake_bezier_now()
    # front hooves swing to -x (FR leads), hind hooves to +x (BL leads): the leading hoof steps away first
    plan_out = {"Leg_FR": (2, 8, 0, YAW), "Leg_BL": (5, 11, 0, YAW), "Leg_FL": (8, 14, 0, YAW), "Leg_BR": (11, 17, 0, YAW)}
    plan_back = {"Leg_FL": (48, 54, YAW, 0), "Leg_BR": (51, 57, YAW, 0), "Leg_FR": (54, 60, YAW, 0),
                 "Leg_BL": (57, 63, YAW, 0)}
    turn_keys(k, range(0, 33), yaw_at, plan_out)
    turn_keys(k, range(33, n + 1), yaw_at, plan_back)
    k.finish(loop=False)


def charge(k):
    """SIGNATURE - SCRAPE & CHARGE: paws the ground twice with the right fore-hoof flinging dirt back, head low; drops
    the horns as the tail goes stiff and the body rocks back onto its haunches; LUNGES forward over planted hooves;
    hooks the horns up and to the right; settles back with one snort."""
    n = 90
    k.new_action("act_charge", n, False)
    P = [  # f, spine (y, z, pitch), chest, neck, head (pitch, yaw, roll), jaw, tail pitch
        (0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 3, 0),
        (6, 0.02, -0.01, 0, 1, 6, 8, 0, 0, 4, 10),
        (28, 0.02, -0.01, 0, 1, 6, 8, 0, 0, 4, 10),
        (36, 0.07, -0.05, -4, 2, 10, 18, 0, 0, 6, 70),
        (40, 0.07, -0.05, -4, 2, 10, 18, 0, 0, 6, 72),
        (48, -0.15, -0.035, 4, 0, 6, 14, 0, 0, 10, 60),
        (52, -0.15, -0.035, 4, 0, 6, 14, 0, 0, 12, 60),
        (57, -0.12, -0.01, -2, -2, -2, -12, -32, 22, 22, 50),
        (62, -0.10, -0.01, -2, -2, -2, -12, -32, 22, 18, 40),
        (72, -0.02, 0.0, 0, 0, 0, 0, 0, 0, 4, 8),
        (76, -0.01, 0.0, 0, 0, -2, -6, 0, 0, 14, 4),
        (80, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 3, 0),
        (90, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 3, 0)]
    for f, y, z, p, ch, nk, hp_, hy, hr, jw, tp in P:
        k.key("Spine", f, rot=(p, hy * 0.3, 0), loc=(0, y, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, hy * 0.2, 0))
        k.key("Head", f, rot=(hp_, hy * 0.25, hr))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tail(k, f, tp, 0, lag=(1.0, -0.1, -0.1))
        pin = 1.0 if 30 <= f <= 64 else 0.0
        ears(k, f, 22 * pin, 22 * pin)
    k.bake_bezier_now()
    import bpy
    J = k.J
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        for leg in LEGS4:
            T = Vector((J[leg].x, J[leg].y, 0.0))
            if leg == "Leg_FR" and 4 <= f < 30:             # two scrapes: reach forward-up, drag the hoof back
                cyc = (f - 4) // 13
                u = ((f - 4) % 13) / 13
                y0 = 0.0 if cyc == 0 else 0.10
                if u < 0.4:
                    v = u / 0.4
                    y = y0 + (-0.13 - y0) * math.sin(math.pi * v * 0.5)
                    T = Vector((J[leg].x, J[leg].y + y, 0.09 * math.sin(math.pi * v)))
                else:
                    v = (u - 0.4) / 0.6
                    T = Vector((J[leg].x, J[leg].y - 0.13 + 0.23 * v, 0.0))
            elif leg == "Leg_FR" and 30 <= f <= 36:          # step the hoof back under the shoulder
                v = (f - 30) / 6
                T = Vector((J[leg].x, J[leg].y + 0.10 * (1 - v), 0.05 * math.sin(math.pi * v)))
            k.solve_leg(leg, f, T)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    charge(k)
    return stride


HEAD_XF = []
