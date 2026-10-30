# Lava Golem (Magma egg #2) - FIERCE style (2026-10-09, FIERCE_PLAN "the volcano silverback"): a basalt silverback
# gorilla built from tapered blocks under a Roblox stud skin. Inverted-triangle build (shoulders 0.55 H wide, chest
# barrel, narrow waist, short legs), a trapezius hump that sinks the head between the shoulders, a rock sagittal
# crest and a heavy brow shelf over narrow molten eyes, fangs, long arms (thicker forearms) ending in boulder fists
# below the knees with obsidian knuckle claws, rock armour on the shoulders / back / forearms / shins, a molten heart
# cluster in the chest with seams running to the shoulders and knees, and the golem's "emet" glyph (3 bars) on the
# forehead. No glow (embers = VFX). Old chibi version: _tools/chibi_specs/LavaGolem.py
import math
from mathutils import Vector, Euler

DISPLAY = "Lava Golem"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 7.0                   # hump/chest top ~1.40 of 1.52 model units = ~6.5 studs at x1 (HEIGHT rule 2026-10-09)

BASALT = (112, 98, 96)         # basalt body (Roblox renders ~0.6x darker -> near-black basalt in game)
TOPS = (152, 144, 140)        # rock armour tops: pauldrons, hump slabs, brow, forearm / shin guards, crest
DARK = (62, 56, 58)           # face, hands, feet
CLAW = (14, 14, 22)           # obsidian claws
MAGMA = (255, 170, 30)        # the ONE accent: heart, seams, eyes, glyph, mouth
MAGMA_HOT = (255, 236, 160)
TEETH = (236, 226, 206)
BLACK = (14, 14, 22)

PITCH = 0.049                 # stud pitch = 0.042 x (U / U_raiju), U = model height / HEIGHT (1.52 / 7.0 vs 1.498 / 8)

S0 = (0.38, -0.10, 1.22)      # shoulder in the UPRIGHT build frame (the upper body is then leaned LEAN deg)
LEAN = 18.0                   # extra forward lean of the whole upper body about the waist (chest 24 -> 42 deg)
PIV = (0.0, 0.04, 0.72)       # waist pivot of the lean
THROAT0 = (0.0, -0.24, 1.30)  # throat joint in the upright frame
HEAD_S = 1.18                 # head group scale about the throat
HEAD_UP = 0.03                # head group lift after the lean (face clears the pauldrons)
E = (0.58, -0.24, 0.75)       # elbow / wrist / fist (left side, world): bowed ")(" arms dropping to planted fists
W = (0.45, -0.33, 0.34)
FIST = (0.45, -0.36, 0.165)
LEG = ((0.15, 0.10, 0.58), (0.19, 0.00, 0.32), (0.18, 0.08, 0.10))


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def RL():
    return Euler((math.radians(LEAN), 0, 0), "XYZ").to_matrix()


def lean(p):
    """upright-frame point -> leaned world point"""
    P = Vector(PIV)
    return P + RL() @ (Vector(p) - P)


S = tuple(lean(S0))
THROAT = tuple(lean(THROAT0) + Vector((0, 0, HEAD_UP)))


def head_xf(p):
    """head-group build point (old upright head frame) -> world: follow the throat, stay level, scale"""
    T = Vector(THROAT)
    return T + (Vector(p) - Vector(THROAT0)) * HEAD_S


def fpt(b, lx, lz, off=0.006, back=False):
    """point on the FRONT (-y) (or BACK, +y) face of tapered / top-shifted block b at local (lx, lz) + its normal"""
    t = (lz / b.h.z + 1) / 2
    fy = b.bot[1] + (b.top[1] - b.bot[1]) * t
    sg = 1 if back else -1
    p = b.world(Vector((lx + b.ts[0] * t, b.ts[1] * t + sg * (b.h.y * fy + off), lz)))
    g = (b.ts[1] + sg * b.h.y * (b.top[1] - b.bot[1])) / (2 * b.h.z)
    return p, (b.R @ Vector((0, sg, -sg * g))).normalized()


def spt(b, s, ly, lz, off=0.006):
    """point on the +-x SIDE face of tapered block b at local (ly, lz) + the face normal"""
    t = (lz / b.h.z + 1) / 2
    fx = b.bot[0] + (b.top[0] - b.bot[0]) * t
    p = b.world(Vector((s * (b.h.x * fx + off), ly + b.ts[1] * t, lz)))
    g = b.h.x * (b.top[0] - b.bot[0]) / (2 * b.h.z)
    return p, (b.R @ Vector((s, 0, -g))).normalized()


def seam(B, Q, bone, w=0.05, tip=True):
    """magma seam: flat bars through [(point, normal)], the last one pointed"""
    for i, ((a, n), (c, _)) in enumerate(zip(Q, Q[1:])):
        last = tip and i == len(Q) - 2
        B.bar(a, c, n, w, 0.012, MAGMA, bone, studs=[], bevel=0.004, top=(1, 0.2) if last else (1, 1))


def band(B, p0, p1, hw, hd, bone, side=(1, 0, 0)):
    """flush magma joint band (0.045 tall) around a limb between p0 and p1"""
    B.seg(p0, p1, hw, hd, MAGMA, bone, side=side, studs=[], role="limb", rnd=0.25)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=113, tier=3, plates=False)
    # ================= upper body (Chest) built UPRIGHT, then leaned LEAN deg about the waist
    n_up = len(B.items)
    chest = B.add((0, -0.08, 1.08), (0.28, 0.225, 0.25), BASALT, "Chest", rot=(24, 0, 0), bot=(0.70, 0.78),
                  top=(1.0, 0.96), rnd=0.30)
    hump = B.add((0, 0.03, 1.36), (0.27, 0.18, 0.11), TOPS, "Chest", rot=(24, 0, 0), top=(0.52, 0.60), rnd=0.38)
    # pec armour plates + nape bridge from the hump to the skull
    for sx in (1, -1):
        pp, pn = fpt(chest, sx * 0.155, 0.16, off=0.012)
        B.add(pp, (0.03, 0.105, 0.075), TOPS, "Chest", R=bk.frame_from(pp - Vector((0, 0, 0.1)), pp, pn),
              top=(1, 0.85), rnd=0.40)
    B.seg((0, -0.02, 1.36), (0, -0.17, 1.36), 0.13, 0.10, BASALT, "Chest", top=(0.8, 0.85), rnd=0.40)
    # molten heart: dark broken-rock socket + magma core + hot centre
    hp, hn = fpt(chest, 0.0, 0.02, off=0.0)
    for ang, sz in ((45, (0.11, 0.11)), (20, (0.085, 0.08)), (70, (0.08, 0.09))):
        B.add(hp + hn * 0.006, (0.014, sz[0], sz[1]), DARK, "Chest", R=bk.frame_from(hp, hp + Vector(
            (math.cos(math.radians(ang)), 0, math.sin(math.radians(ang)))), hn), studs=[], role="detail", bevel=0.008)
    B.add(hp + hn * 0.016, (0.014, 0.07, 0.07), MAGMA, "Chest",
          R=bk.frame_from(hp, hp + Vector((0.7071, 0, 0.7071)), hn), studs=[], role="detail", bevel=0.008)
    B.add(hp + hn * 0.026, (0.010, 0.03, 0.03), MAGMA_HOT, "Chest",
          R=bk.frame_from(hp, hp + Vector((0.7071, 0, 0.7071)), hn), studs=[], role="detail", bevel=0.005)
    # seams from the heart: out under the pecs to each armpit, down to each hip
    for s in (1, -1):
        seam(B, [fpt(chest, s * x, z) for x, z in ((0.06, -0.04), (0.12, -0.01), (0.17, 0.02), (0.27, 0.06))],
             "Chest", tip=False)
        seam(B, [fpt(chest, s * x, z) for x, z in ((0.05, -0.13), (0.10, -0.16), (0.08, -0.20), (0.12, -0.25))],
             "Chest", tip=False)
    # silver back: 2 overlapping rock plates down the chest's back (jagged lower edges, magma gaps)
    plates = []
    for z0, z1, w in ((0.30, 0.06, 0.25), (0.02, -0.24, 0.23)):
        a, na = fpt(chest, 0.0, z0, off=0.03, back=True)
        b, nb = fpt(chest, 0.0, z1, off=0.03, back=True)
        n = (na + nb).normalized()
        plates.append((a, b, n, w, "Chest"))
    for blk in B.items[n_up:]:
        blk.c = lean(blk.c)
        blk.R = RL() @ blk.R
    plates = [(lean(a), lean(b), RL() @ n, w, bn) for a, b, n, w, bn in plates]
    # trapezius: rises from the hump into the back of the skull (the head sinks into the shoulders)
    tp = Vector(THROAT) + Vector((0, 0.055, 0.17))
    B.seg(tp + Vector((0, 0.24, -0.07)), tp, 0.18, 0.105, TOPS, "Chest", top=(0.72, 0.8), rnd=0.42)
    # ================= lower body (Spine): waist, pelvis, rump, lower back plate
    belly = B.add((0, 0.02, 0.82), (0.20, 0.165, 0.13), BASALT, "Spine", rot=(10, 0, 0), bot=(0.86, 0.90),
                  top=(1.0, 1.0), rnd=0.30)
    B.add((0, 0.06, 0.645), (0.18, 0.15, 0.10), DARK, "Spine", bot=(0.85, 0.85), rnd=0.30)          # pelvis
    B.add((0, 0.20, 0.70), (0.17, 0.13, 0.12), BASALT, "Spine", rot=(-12, 0, 0), top=(0.85, 0.8), rnd=0.38)  # rump
    a, na = fpt(belly, 0.0, 0.14, off=0.03, back=True)
    plates.append((a, Vector((0, 0.31, 0.74)), (na + Vector((0, 0.5, 0.8))).normalized(), 0.19, "Spine"))
    for s in (1, -1):
        seam(B, [fpt(belly, s * x, z) for x, z in ((0.09, 0.10), (0.12, 0.03), (0.09, -0.03), (0.12, -0.10))],
             "Spine")
    for i, (a, b, n, w, bn) in enumerate(plates):
        d = (b - a).normalized()
        L = (b - a).length
        B.add((a + b) / 2, (0.035, w, L / 2), TOPS, bn, R=bk.frame_from(a, b, n), top=(1, 0.9), rnd=0.40)
        # magma under the gap below this plate + jagged rock teeth hanging over it
        g = b + d * 0.03 - n * 0.02
        B.add(g, (0.012, w * 0.85, 0.05), MAGMA, bn, R=bk.frame_from(g - d, g, n), studs=[], role="detail",
              bevel=0.004)
        side = n.cross(d).normalized()
        for j, u in enumerate((-0.6, 0.0, 0.6)):
            t0 = b + side * (u * w) - d * 0.02
            t1 = t0 + d * (0.075 if j % 2 == 0 else 0.055)
            B.add((t0 + t1) / 2, (0.02, 0.045, (t1 - t0).length / 2), TOPS, bn, R=bk.frame_from(t0, t1, n),
                  top=(1, 0.12), role="detail", bevel=0.006)
    # ================= head: built in the old upright head frame, follows the throat level, scaled 1.18
    HY, HZ = -0.12, -0.06
    n0 = len(B.items)
    skull = B.add((0, -0.21, 1.445), (0.125, 0.115, 0.115), BASALT, "Head", top=(0.84, 0.80), rnd=0.30)
    B.add((0, -0.19, 1.575), (0.03, 0.085, 0.045), TOPS, "Head", top=(0.35, 0.45), top_shift=(0, 0.035),
          rnd=0.2)                                                                       # sagittal crest (peaks back)
    brow = B.add((0, -0.300, 1.505), (0.147, 0.05, 0.034), BASALT, "Head", rot=(-8, 0, 0), top=(0.96, 1.0),
                 role="limb", bevel=0.010)                                 # studded rock brow shelf (overhangs)
    for x in (-0.042, 0.0, 0.042):                                                       # emet glyph on the brow
        B.on_face(brow, "-y", x, 0.0, 0.011, 0.022, 0.008, MAGMA, role="detail", bevel=0.003)
    B.add((0, -0.338, 1.362), (0.105, 0.06, 0.060), DARK, "Head", top=(0.85, 0.75), bot=(0.9, 1), rnd=0.30)  # muzzle
    for s in (1, -1):
        B.add((s * 0.032, -0.388, 1.404), (0.013, 0.006, 0.009), BLACK, "Head", studs=[], role="detail",
              bevel=0.004)                                                                       # nostrils
        rot = (0, -s * 18, s * 20)
        B.add((s * 0.066, -0.322, 1.452), (0.046, 0.010, 0.020), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.004)
        B.add((s * 0.068, -0.329, 1.452), (0.037, 0.007, 0.011), MAGMA, "Head", rot=rot, studs=[], role="detail",
              bevel=0.003)
        B.add((s * 0.075, -0.333, 1.454), (0.016, 0.004, 0.005), MAGMA_HOT, "Head", rot=rot, studs=[],
              role="detail", bevel=0.002)
        B.spike((s * 0.062, -0.365, 1.312), (0, -0.15, -1), 0.065, 0.015, TEETH, "Head")      # upper fang
        B.spike((s * 0.026, -0.375, 1.310), (0, 0, -1), 0.03, 0.011, TEETH, "Head")
    B.add((0, -0.31, 1.295), (0.095, 0.075, 0.032), DARK, "Jaw", top=(0.95, 0.9), bot=(0.8, 0.85), rnd=0.3)
    B.add((0, -0.33, 1.329), (0.07, 0.05, 0.006), MAGMA, "Jaw", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike((s * 0.055, -0.372, 1.32), (0, -0.1, 1), 0.05, 0.013, TEETH, "Jaw")
    for blk in B.items[n0:]:
        blk.c = head_xf(blk.c + Vector((0, HY, HZ)))
        blk.h = blk.h * HEAD_S
    # ================= arms: deltoid boulders + pauldrons, bowed tapering arms, dark forearms, magma joint bands
    for s, side in ((1, "L"), (-1, "R")):
        arm, fore, hand = "Arm_" + side, "Fore_" + side, "Hand_" + side
        Sv, Ev, Wv, Fv = X(S, s), X(E, s), X(W, s), X(FIST, s)
        dl = B.add(Sv + Vector((s * 0.05, 0.0, -0.01)), (0.145, 0.15, 0.125), BASALT, arm, rot=(0, s * 14, 0),
                   rnd=0.45)
        pa = B.add(Sv + Vector((s * 0.08, 0.0, 0.07)), (0.14, 0.15, 0.06), TOPS, arm, rot=(0, s * 24, 0),
                   top=(0.75, 0.8), rnd=0.35)                                                             # pauldron
        for dy, L in ((-0.06, 0.13), (0.07, 0.11)):
            B.spike(pa.world((s * 0.02, dy, 0.03)), (s * 0.45, 0.25, 1), L, 0.04, TOPS, arm, top=(0.12, 0.3))
        up = B.seg(Sv, Ev, 0.11, 0.11, BASALT, arm, ext=0.0, ext1=0.04, top=(0.72, 0.75))
        da = (Wv - Ev).normalized()
        fo = B.seg(Ev, Wv, 0.13, 0.13, DARK, fore, ext=0.05, ext1=0.0, top=(0.62, 0.66))
        band(B, Ev + da * 0.005, Ev + da * 0.05, 0.135, 0.135, fore)                       # elbow band
        band(B, Wv - da * 0.075, Wv - da * 0.03, 0.093, 0.098, fore)                      # wrist band
        for t, L in ((0.25, 0.12), (0.55, 0.10)):                                          # rock shards (forearm)
            base = Ev + (Wv - Ev) * t + Vector((s * 0.10 * (1 - 0.35 * t), 0.02, 0))
            B.spike(base, (s * 0.55, 0.65, 0.55), L, 0.035, TOPS, fore, top=(0.12, 0.3))
        # seam down the deltoid + upper arm (continues the chest seam out of the armpit)
        seam(B, [spt(up, s, y, z) for y, z in ((0.0, 0.21), (-0.04, 0.11), (0.03, 0.0), (-0.02, -0.10),
                                                (0.03, -0.18))], arm, w=0.045)
        # boulder fist + knuckle plate + 4 obsidian knuckle claws
        B.add(Fv, (0.125, 0.13, 0.13), DARK, hand, rnd=0.32)
        B.add(Fv + Vector((0, -0.11, -0.03)), (0.115, 0.04, 0.07), BASALT, hand, rnd=0.35)
        for gx in (-0.075, -0.025, 0.025, 0.075):
            B.spike((Fv.x + gx, Fv.y - 0.14, Fv.z - 0.055), (0, -1, -0.45), 0.07, 0.017, CLAW, hand)
    # ================= legs: short, bowed; basalt thigh with a magma seam to the knee, dark shin + guard, dark feet
    for s, side in ((1, "L"), (-1, "R")):
        leg, shin, foot = "Leg_" + side, "Shin_" + side, "Foot_" + side
        H, K, A = (X(p, s) for p in LEG)
        th = B.seg(H + Vector((0, 0, 0.06)), K, 0.115, 0.13, BASALT, leg, ext=0.0, ext1=0.04, top=(0.85, 0.80))
        B.seg(K, A, 0.09, 0.10, DARK, shin, ext=0.04, ext1=0.02, top=(0.9, 0.9))
        dk = (A - K).normalized()
        band(B, K + dk * 0.0, K + dk * 0.045, 0.097, 0.107, shin)                           # knee band
        B.seg(K + Vector((0, -0.035, -0.06)), K + (A - K) * 0.8 + Vector((0, -0.045, 0)), 0.075, 0.03, TOPS, shin,
              top=(0.85, 1), rnd=0.3)                                                           # shin guard
        seam(B, [fpt(th, s * x, z) for x, z in ((0.03, 0.17), (-0.02, 0.09), (0.03, 0.0), (-0.01, -0.09),
                                                 (0.02, -0.17))], leg, w=0.045)
        B.add((A.x, A.y - 0.08, 0.05), (0.11, 0.165, 0.05), DARK, foot, top=(0.9, 0.85), rnd=0.3)
        for gx in (-0.07, -0.023, 0.023, 0.07):
            B.spike((A.x + gx, A.y - 0.235, 0.035), (0, -1, -0.5), 0.055, 0.016, CLAW, foot)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.04, 0.66), "Root", tail=(0, 0, 0.3))
    k.joint("Chest", (0, 0.02, 0.86), "Spine", tail=(0, -0.25, 0.4))
    T = Vector(THROAT)
    k.joint("Head", T, "Chest", tail=(0, -0.2, 0.15))                        # pivot low at the back of the throat
    k.joint("Jaw", head_xf((0, -0.36, 1.27)), "Head", tail=(0, -0.2, 0))
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        k.joint("Arm_" + side, Sv, "Chest")
        k.joint("Fore_" + side, Ev, "Arm_" + side)
        k.joint("Hand_" + side, Wv, "Fore_" + side, tail=(0, -0.05, -0.25))
        k.add_leg2("Arm_" + side, "Fore_" + side, "Hand_" + side, knee=(s * 1.0, 0.15, 0))   # arm IK (knuckles)
        H, K, A = (X(p, s) for p in LEG)
        k.joint("Leg_" + side, H, "Spine")
        k.joint("Shin_" + side, K, "Leg_" + side)
        k.joint("Foot_" + side, A, "Shin_" + side, tail=(0, -0.25, 0))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))


# ------------------------------------------------------------------ animation (FIERCE_PLAN 2026-10-09)
import petkit as pk
import _common as cm
from mathutils import Quaternion, Matrix

LEGS2 = ["Leg_L", "Leg_R"]
ARMS = ["Arm_L", "Arm_R"]


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


def wrist(k, side, f, P, toe=0.0, q=None):
    """2-bone arm IK: put the wrist at world point P (fist kept level, or world rotation q on the hand)"""
    s = 1 if side == "L" else -1
    Sv, Wv = X(S, s), X(W, s)
    P = Vector(P)
    k.solve_leg("Arm_" + side, f, Vector((Sv.x + P.x - Wv.x, Sv.y + P.y - Wv.y, P.z - Wv.z)), toe=toe)
    if q is not None:
        k._aim("Hand_" + side, f, q)


def rest_wrist(side):
    return X(W, 1 if side == "L" else -1)


def fist_off():
    return Vector(FIST) - Vector(W)          # fist centre below the wrist (left side; x part is 0)


def plant_feet(k, f, lift=0.0, dy=0.0):
    for leg in LEGS2:
        k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y + dy, lift)))


def chest_xf(k):
    """armature-space transform rest -> posed of the Chest bone at the current frame"""
    pb = k.arm.pose.bones["Chest"]
    return pb.matrix @ k.arm.data.bones["Chest"].matrix_local.inverted()


def idle(k):
    """KNUCKLE REST: leans on its planted knuckles with heavy breaths; lifts the right fist and turns it to inspect
    it (head follows), brings the left palm up and cracks its knuckles into it 3 times, then plants both back."""
    import bpy
    n = 120
    k.new_action("idle", n, True)
    HD = [(0, (0, 0)), (40, (0, 0)), (48, (10, -14)), (60, (10, -14)), (64, (8, -4)), (80, (8, -4)), (92, (0, 0)),
          (120, (0, 0))]
    JW = [(0, 3), (66, 3), (67, 10), (69, 3), (70, 10), (72, 3), (73, 10), (75, 3), (120, 3)]
    for f in range(0, n + 1):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.012 * b))
        k.key("Chest", f, rot=(-2.0 * b, 2 * tab([(0, 0), (44, 0), (52, -1), (80, -1), (92, 0), (120, 0)], f), 0))
        hp, hy = tab(HD, f)
        k.key("Head", f, rot=(hp, hy, 0))
        k.key("Jaw", f, rot=(tab(JW, f), 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    R0, L0 = rest_wrist("R"), rest_wrist("L")
    RI = Vector((-0.22, -0.70, 0.96))           # right fist held up in front of the face
    RC = Vector((-0.145, -0.68, 0.92))           # right fist cracking into the left palm
    LC = Vector((0.145, -0.68, 0.90))
    RT = [(0, R0), (40, R0), (50, RI), (60, RI), (64, RC), (80, RC), (92, R0), (120, R0)]
    LT = [(0, L0), (56, L0), (64, LC), (80, LC), (92, L0), (120, L0)]
    for f in range(0, n + 1):
        sc.frame_set(f)
        plant_feet(k, f)
        r = Vector(tab([(fr, tuple(v)) for fr, v in RT], f))
        l = Vector(tab([(fr, tuple(v)) for fr, v in LT], f))
        lr = 0.10 * math.sin(math.pi * min(1, max(0, (f - 40) / 10))) if 40 <= f <= 50 else 0.0
        lr += 0.08 * math.sin(math.pi * min(1, max(0, (f - 80) / 12))) if 80 <= f <= 92 else 0.0
        push = 0.012 * (math.sin(2 * math.pi * (f - 66) / 3.0) > 0.3) if 66 <= f <= 75 else 0.0
        turn = tab([(0, 0.0), (48, 0.0), (52, 40.0), (56, -30.0), (60, 20.0), (64, 0.0), (120, 0.0)], f)
        qr = Quaternion((0, 1, 0), math.radians(turn)) @ Quaternion((1, 0, 0), math.radians(
            -50 * tab([(0, 0.0), (44, 0.0), (50, 1.0), (60, 1.0), (64, 0.3), (80, 0.3), (92, 0.0), (120, 0.0)], f)))
        wrist(k, "R", f, r + Vector((push, 0, lr)), q=qr)
        ql = Quaternion((0, 1, 0), math.radians(-70 * tab([(0, 0.0), (58, 0.0), (64, 1.0), (80, 1.0), (90, 0.0),
                                                            (120, 0.0)], f)))
        wrist(k, "L", f, l + Vector((0, 0, 0.06 * math.sin(math.pi * min(1, max(0, (f - 56) / 8)))
                                     if 56 <= f <= 64 else 0.0)), q=ql)
    k.finish()
    k.meta["planted"] = LEGS2


def walk(k):
    """KNUCKLE-WALK: lateral-sequence gait on the fists and feet, heavy shoulder roll, head steady."""
    n = 32

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.0 * pk.wave(f, n, 0.1, 2), 3 * pk.wave(f, n, 0.0), 2.5 * pk.wave(f, n, 0.05)),
              loc=(0, 0, -0.02 * b))
        k.key("Chest", f, rot=(1.5 * pk.wave(f, n, 0.15, 2), -5 * pk.wave(f, n, 0.0), -3 * pk.wave(f, n, 0.05)))
        k.key("Head", f, rot=(-1.5 * pk.wave(f, n, 0.2, 2), 4 * pk.wave(f, n, 0.0), 0))
        k.key("Jaw", f, rot=(3, 0, 0))
    legs = [("Leg_L", 0.0), ("Arm_L", 0.25), ("Leg_R", 0.5), ("Arm_R", 0.75)]
    k.meta["legs"] = legs
    k.meta["duty"] = 0.62
    return pk.walk_cycle(k, n, legs, 0.12, 0.08, body, duty=0.62)


def roar(k):
    """CHEST BEAT: rises tall out of the lean, chest out, head back, then 6 rapid alternating chest beats with cupped
    fists (embers on each hit), jaw wide, a final hoot with the arms flung wide; drops back onto its knuckles."""
    import bpy
    n = 60
    k.new_action("roar", n, False)
    RISE = [(0, 0.0), (10, 1.0), (40, 1.0), (52, 0.0), (60, 0.0)]
    HOOT = [(0, 0.0), (34, 0.0), (38, 1.0), (44, 1.0), (50, 0.0), (60, 0.0)]
    for f in range(0, n + 1):
        r, h = tab(RISE, f), tab(HOOT, f)
        k.key("Spine", f, rot=(-4 * r, 0, 0), loc=(0, 0.02 * r, 0.05 * r))
        k.key("Chest", f, rot=(-22 * r - 4 * h, 0, 0))
        k.key("Head", f, rot=(-6 * r - 12 * h, 0, 0))
        jw = 3 + 14 * r + 18 * h + (3 * math.sin(2 * math.pi * f / 4) if 12 <= f <= 34 else 0)
        k.key("Jaw", f, rot=(jw, 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    up24 = Euler((math.radians(24), 0, 0), "XYZ").to_matrix()
    nrm0 = RL() @ up24 @ Vector((0, -1, 0))
    BEAT = {"R": (14, 22, 30), "L": (18, 26, 34)}
    for f in range(0, n + 1):
        sc.frame_set(f)
        plant_feet(k, f)
        M = chest_xf(k)
        r, h = tab(RISE, f), tab(HOOT, f)
        for side in ("L", "R"):
            s = 1 if side == "L" else -1
            pec = lean(Vector((s * 0.13, -0.08, 1.08)) + up24 @ Vector((0, -0.24, 0.10)))
            P = M @ pec
            nrm = (M.to_3x3() @ nrm0).normalized()
            hit = 0.0
            for fb in BEAT[side]:
                if fb - 2 <= f <= fb + 2:
                    hit = max(hit, 1.0 - abs(f - fb) / 2.0)
            away = 0.22 + 0.10 * (1 - hit)                          # fist centre distance in front of the pec
            beat_pt = P + nrm * away + Vector((s * 0.06, 0, -0.02)) - fist_off()
            wide = Vector((s * 0.72, -0.40, 1.02))                    # hoot: arms flung wide
            tgt = beat_pt.lerp(wide, h)
            wr = rest_wrist(side)
            P2 = wr.lerp(tgt, r) + Vector((0, 0, 0.10 * math.sin(math.pi * r)))
            wrist(k, side, f, P2)
    k.finish(loop=False)


def pound(k):
    """SIGNATURE - GROUND POUND: raises the right fist high and SMASHES it into the ground, then the left; clasps
    both fists overhead and crouches; JUMPS and lands with a double-fisted smash (shockwave); holds the impact
    crouch glaring; rises to rest."""
    import bpy
    n = 100
    k.new_action("act_pound", n, False)
    # body: (spine z, chest pitch, chest yaw, head pitch)
    BODY = [(0, (0.0, 0, 0, 0)), (10, (0.02, -10, -8, -4)), (16, (-0.03, 8, -10, 4)), (20, (-0.03, 8, -10, 4)),
            (26, (0.02, -10, 8, -4)), (32, (-0.03, 8, 10, 4)), (36, (-0.03, 8, 10, 4)), (42, (0.02, 4, 0, 22)),
            (50, (-0.12, 6, 0, 22)), (56, (0.32, 6, 0, 22)), (61, (0.04, 6, 0, 22)), (64, (-0.10, 8, 0, 14)),
            (70, (-0.13, 12, 0, -12)), (86, (-0.12, 12, 0, -12)), (100, (0.0, 0, 0, 0))]
    JW = [(0, 3), (12, 3), (16, 22), (22, 6), (28, 6), (32, 22), (38, 6), (62, 6), (65, 30), (72, 12), (86, 12),
          (100, 3)]
    for f in range(0, n + 1):
        z, cp, cy, hp = tab(BODY, f)
        k.key("Spine", f, rot=(0, cy * 0.4, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(cp, cy, 0))
        k.key("Head", f, rot=(hp - cp * 0.6, -cy * 0.4, 0))
        k.key("Jaw", f, rot=(tab(JW, f), 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    R0, L0 = rest_wrist("R"), rest_wrist("L")
    UPR, UPL = Vector((-0.52, -0.40, 1.58)), Vector((0.52, -0.40, 1.58))
    HITR, HITL = Vector((-0.40, -0.64, 0.36)), Vector((0.40, -0.64, 0.36))
    MIDR, MIDL = Vector((-0.66, -0.42, 0.95)), Vector((0.66, -0.42, 0.95))       # arms swing up OUTSIDE the body
    CLR, CLL = Vector((-0.145, -0.72, 1.84)), Vector((0.145, -0.72, 1.84))
    DBR, DBL = Vector((-0.15, -0.74, 0.36)), Vector((0.15, -0.74, 0.36))
    RT = [(0, R0), (3, R0), (8, MIDR), (12, UPR), (16, HITR), (20, HITR), (26, R0), (34, R0), (39, MIDR),
          (44, CLR), (50, CLR), (60, CLR), (63, DBR), (86, DBR), (100, R0)]
    LT = [(0, L0), (20, L0), (24, MIDL), (28, UPL), (32, HITL), (36, HITL), (40, L0), (41, L0), (44, MIDL),
          (48, CLL), (50, CLL), (60, CLL), (63, DBL), (86, DBL), (100, L0)]
    TOE = [(0, 0.0), (10, -40.0), (16, 0.0), (36, 0.0), (44, -60.0), (60, -60.0), (63, 0.0), (100, 0.0)]

    def air(f):
        z = tab(BODY, f)[0]
        return max(0.0, z - 0.08) if 51 <= f <= 61 else 0.0

    for f in range(0, n + 1):
        sc.frame_set(f)
        plant_feet(k, f, lift=air(f))
        wcl = tab([(0, 0.0), (40, 0.0), (44, 1.0), (60, 1.0), (63, 0.0), (100, 0.0)], f)
        bz = tab(BODY, f)[0] * wcl                      # the overhead clasp rides up and down with the jump
        for side, T in (("R", RT), ("L", LT)):
            P = Vector(tab([(fr, tuple(v)) for fr, v in T], f)) + Vector((0, 0, bz))
            wrist(k, side, f, P, toe=tab(TOE, f))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    pound(k)
    return stride


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Hand_L", "Hand_R"), ("Fore_L", "Fore_R"),
         ("Hand_L", "Fore_R"), ("Hand_R", "Fore_L"), ("Arm_L", "Head"), ("Arm_R", "Head")]
    for s in ("L", "R"):
        for a in ("Fore_" + s, "Hand_" + s):
            for b in ("Spine", "Chest", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Foot_L", "Foot_R", "Head", "Jaw"):
                P.append((a, b))
    return P


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        Wv = X(W, s)
        out.append((Wv, Wv, 0.14, "Hand_" + side))
    return out
