# Solar Lion (Celestial egg #1) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the black-maned sun king"): a real lion
# built from tapered blocks and covered in Roblox studs (blockkit.stud_skin): heavy forequarters, deep chest tapering to
# a rising belly line, long low body, big clawed paws, a broad head with a short heavy muzzle, bared fangs, narrow gold
# eyes with slit pupils under a heavy brow and a gold sun mark on the brow, a HUGE dark mane from the cheeks to the
# shoulders and chest, and behind it the Persian "Lion and Sun" emblem: 12 flat bronze sun-ray blades with gold tips
# (each on its own bone under the Rays wheel), a long tail ending in a dark tuft.
# Old chibi version: _tools/chibi_specs/SolarLion.py
import math
from mathutils import Vector, Euler, Matrix

DISPLAY = "Solar Lion"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 9.0

FUR = (206, 140, 66)          # tawny (Roblox renders ~0.6x darker -> deep tawny in game)
BACK = (164, 102, 46)         # back shade, brows, ear backs
PALE = (238, 208, 152)        # muzzle, chin, chest, belly
MANE = (98, 56, 36)           # the black-brown mane (outer)
MANE_I = (148, 80, 40)        # inner mane ring round the face
RAY = (186, 100, 34)          # sun-ray blades (bronze) ...
GOLD = (255, 196, 40)         # ... with gold tips = the accent (also eyes + brow sun mark)
EYE = (255, 196, 40)
EYE_HOT = (255, 236, 160)
NOSE = (70, 36, 30)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
MOUTH = (96, 26, 30)

PITCH = 0.042

# leg joints (left side): H shoulder/hip, K elbow/stifle, A wrist/hock, P paw centre
LEGS = {"F": ((0.155, -0.48, 0.70), (0.155, -0.39, 0.42), (0.155, -0.47, 0.115), (0.155, -0.52, 0.05)),
        "B": ((0.13, 0.48, 0.76), (0.13, 0.34, 0.47), (0.13, 0.58, 0.22), (0.13, 0.51, 0.05))}
HC = Vector((0, -0.93, 1.04))          # cranium centre
RC = Vector((0, -0.72, 1.04))          # centre of the sun-ray wheel (set into the mane bulk)
NR = 12
R0 = 0.31                              # ray root radius (hidden in the mane)
TILT = (22, 22, 22, 22, 10, 0, 0, 0, 10, 22, 22, 22)   # rays tilted back into a shallow cone (deg)
TAILP = [(0, 0.66, 0.83), (0, 0.90, 0.68), (0, 1.10, 0.40), (0, 1.26, 0.19)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def ray_flat(i):
    a = 2 * math.pi * i / NR
    return Vector((math.sin(a), 0, math.cos(a)))


def ray_R(i):
    """ray block frame: local z along the ray, tilted TILT[i] deg back (+y) about its own tangent axis"""
    a = 2 * math.pi * i / NR
    t = Vector((math.cos(a), 0, -math.sin(a)))
    return Matrix.Rotation(-math.radians(TILT[i]), 3, t) @ Euler((0, a, 0), "XYZ").to_matrix()


def ray_dir(i):
    return ray_R(i) @ Vector((0, 0, 1))


def ray_len(i):
    d = ray_flat(i)
    low = max(0.0, -d.z)
    return (0.36 if i % 2 == 0 else 0.25) * (1 - 0.45 * low)


def eye(B, c, s, yaw=20, bone="Head", sc=1.0):
    """FIERCE_PLAN eye recipe (Raiju): black socket -> gold slit (+ cat slit pupil) -> hot highlight -> heavy brow"""
    R = Euler((0, math.radians(-s * 18), math.radians(s * yaw)), "XYZ").to_matrix()
    Rb = Euler((0, math.radians(-s * 20), math.radians(s * yaw)), "XYZ").to_matrix()
    c = Vector(c)
    B.add(c + Rb @ Vector((-s * 0.006, 0.026, 0.047 * sc)), (0.072 * sc, 0.032, 0.028 * sc), BACK, bone, R=Rb,
          role="detail", bevel=0.01)
    B.add(c, (0.055 * sc, 0.008, 0.026 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + R @ Vector((0.002 * s, -0.007, 0.0)), (0.046 * sc, 0.006, 0.014 * sc), EYE, bone, R=R, studs=[],
          role="detail", bevel=0.003)
    B.add(c + R @ Vector((-s * 0.004, -0.010, 0.0)), (0.006 * sc, 0.004, 0.013 * sc), BLACK, bone, R=R, studs=[],
          role="detail", bevel=0.002)                                                              # slit pupil
    B.add(c + R @ Vector((s * 0.022 * sc, -0.011, 0.002)), (0.016 * sc, 0.004, 0.006 * sc), EYE_HOT, bone, R=R,
          studs=[], role="detail", bevel=0.002)


def tuft(B, root, d, L, w, color, bone, tip=None):
    """swept fur tuft (pointed block) with an optional lighter tip"""
    d = Vector(d).normalized()
    B.spike(root, d, L, w, color, bone, top=(0.12, 0.38))
    if tip:
        B.spike(root + d * L * 0.5, d, L * 0.5, w * 0.62, tip, bone, top=(0.12, 0.38))


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=163, tier=6, plates=False)
    # ---------------- torso: deep ribcage + heavy shoulders, sloped tuck to a narrow waist, hips
    B.add((0, -0.30, 0.71), (0.22, 0.36, 0.27), FUR, "Chest", bot=(0.66, 0.56), top=(0.90, 0.95), rnd=0.30)
    B.add((0, -0.40, 0.955), (0.18, 0.21, 0.06), BACK, "Chest", top=(0.72, 0.80))                     # shoulders
    B.seg((0, -0.05, 0.48), (0, 0.40, 0.575), 0.15, 0.08, FUR, "Spine", top=(0.82, 0.75), bot=(1, 1), side=(1, 0, 0))
    B.add((0, 0.16, 0.73), (0.165, 0.24, 0.165), FUR, "Spine", bot=(0.72, 0.70), top=(0.95, 1), rnd=0.30)  # waist
    B.add((0, 0.46, 0.74), (0.185, 0.21, 0.18), FUR, "Spine", rot=(-14, 0, 0), top=(0.84, 0.78), bot=(0.85, 0.9),
          rnd=0.32)                                                                                     # hips
    # pale underside: brisket -> sloped belly line, chest front
    B.add((0, -0.32, 0.445), (0.13, 0.19, 0.025), PALE, "Chest", bot=(0.8, 0.9), studs=[])
    B.seg((0, -0.05, 0.405), (0, 0.38, 0.515), 0.10, 0.022, PALE, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    # ---------------- short thick neck (under the mane)
    B.seg((0, -0.56, 0.80), (0, -0.82, 0.98), 0.17, 0.17, FUR, "Neck", ext=0.06)
    # ---------------- head (pivot at the throat): broad cranium, short heavy muzzle, whisker pads, nose, fangs
    B.add(HC, (0.15, 0.11, 0.115), FUR, "Head", top=(0.84, 0.85))                                     # cranium
    B.add(HC + Vector((0, 0.03, 0.125)), (0.11, 0.08, 0.025), BACK, "Head", top=(0.8, 0.8))           # dark crown
    B.seg((0, -1.00, 1.035), (0, -1.17, 1.015), 0.085, 0.06, FUR, "Head", top=(0.78, 0.85), ext=0.02)  # nose bridge
    for s in (1, -1):                                                                                   # whisker pads
        B.add((s * 0.058, -1.10, 0.965), (0.062, 0.075, 0.05), PALE, "Head", rnd=0.4)
    B.add((0, -1.185, 1.02), (0.05, 0.026, 0.033), NOSE, "Head", role="detail", bevel=0.01, top=(0.6, 1))  # nose
    for s in (1, -1):
        B.spike((s * 0.058, -1.14, 0.93), (0, -0.1, -1), 0.08, 0.017, TEETH, "Head")                  # canines
        for y in (-1.09, -1.05):
            B.spike((s * 0.07, y, 0.93), (0, 0, -1), 0.034, 0.012, TEETH, "Head")
    B.add((0, -1.08, 0.925), (0.075, 0.075, 0.006), MOUTH, "Head", studs=[], role="detail", bevel=0.004)
    # lower jaw (opens in the roar) + lower fangs + pale chin
    B.seg((0, -0.97, 0.895), (0, -1.15, 0.885), 0.08, 0.03, PALE, "Jaw", top=(0.8, 1), ext=0.02)
    B.add((0, -1.07, 0.921), (0.064, 0.075, 0.006), MOUTH, "Jaw", studs=[], role="detail", bevel=0.004)
    for s in (1, -1):
        B.spike((s * 0.048, -1.135, 0.91), (0, 0, 1), 0.05, 0.014, TEETH, "Jaw")
    # narrow gold eyes (slit pupils) under heavy brows + gold sun mark on the brow
    for s in (1, -1):
        eye(B, (s * 0.076, -1.044, 1.075), s, sc=1.1)
    B.add((0, -1.043, 1.138), (0.028, 0.006, 0.028), GOLD, "Head", rot=(0, 45, 0), studs=[], role="detail",
          bevel=0.004)
    for a in (0, 90, 180, 270):
        d = Vector((math.sin(math.radians(a)), 0, math.cos(math.radians(a))))
        B.add(Vector((0, -1.043, 1.138)) + d * 0.05, (0.009, 0.006, 0.016), GOLD, "Head",
              rot=(0, a, 0), top=(0.2, 1), studs=[], role="detail", bevel=0.003)
    # small round ears in the mane top
    for s, side in ((1, "L"), (-1, "R")):
        ear = B.add((s * 0.12, -0.88, 1.18), (0.045, 0.022, 0.05), BACK, "Ear_" + side, rot=(-10, s * 8, -s * 18),
                    top=(0.55, 0.7))
        B.add(ear.world((0, -0.022, -0.008)), (0.03, 0.005, 0.034), PALE, "Ear_" + side, R=ear.R, top=(0.6, 1),
              studs=[], role="detail", bevel=0.004)
    # ---------------- the mane: huge dark bulk round the neck + shoulders, an inner ring framing the face,
    # a chest bib hanging between the front legs, swept tufts over the shoulders
    B.add((0, -0.69, 0.95), (0.25, 0.20, 0.26), MANE, "Neck", rnd=0.36, top=(0.80, 0.8), bot=(0.8, 0.85))   # bulk
    B.add((0, -0.66, 1.18), (0.18, 0.16, 0.08), MANE, "Neck", rnd=0.36, top=(0.6, 0.7))                   # crest
    for i in range(14):                                   # face ring: tufts all round the face, swept back + out
        a = 2 * math.pi * (i + 0.5) / 14
        d = Vector((math.sin(a), 0, math.cos(a)))
        if d.z < -0.85:
            continue
        root = HC + Vector((d.x * 0.13, 0.06, d.z * 0.11 - 0.02))
        L = 0.17 if i % 2 == 0 else 0.13
        tuft(B, root, d * 1.0 + Vector((0, 0.55, 0)), L, 0.06, MANE, "Head")
    for s in (1, -1):                                     # cheek ruff under the jaw line
        for z, dz, L in ((0.92, -0.6, 0.15), (0.99, -0.2, 0.17)):
            tuft(B, Vector((s * 0.12, -0.92, z)), (s * 0.55, 0.6, dz), L, 0.055, MANE_I, "Head")
    for s in (1, -1):                                     # outer mane tufts: shoulders + sides of the bulk
        for y, z, L, d in ((-0.66, 1.10, 0.22, (s * 0.7, 0.55, 0.35)), (-0.62, 0.92, 0.24, (s * 0.85, 0.5, -0.1)),
                           (-0.66, 0.75, 0.20, (s * 0.7, 0.35, -0.6)), (-0.52, 1.04, 0.20, (s * 0.45, 0.85, 0.2))):
            tuft(B, Vector((s * 0.16, y, z)), d, L, 0.075, MANE, "Neck")
    # shoulder cape: the mane runs back over the shoulders and down the chest sides (on the Chest)
    B.add((0, -0.47, 0.86), (0.258, 0.17, 0.215), MANE, "Chest", rnd=0.36, top=(0.72, 0.8), bot=(0.85, 0.9))
    for s in (1, -1):
        for y, z, L, d in ((-0.36, 0.98, 0.20, (s * 0.45, 0.85, 0.15)), (-0.36, 0.80, 0.21, (s * 0.55, 0.8, -0.35)),
                           (-0.44, 0.66, 0.18, (s * 0.35, 0.5, -0.85))):
            tuft(B, Vector((s * 0.20, y, z)), d, L, 0.075, MANE, "Chest")
    for y, z, L in ((-0.62, 1.20, 0.22), (-0.50, 1.12, 0.20), (-0.38, 1.02, 0.17)):     # dorsal mane down the back
        tuft(B, Vector((0, y, z - 0.03)), (0, 0.75, 0.6), L, 0.08, MANE, "Neck" if y < -0.45 else "Chest")
    for x, L in ((0.0, 0.30), (0.10, 0.25), (-0.10, 0.25)):                              # chest bib
        tuft(B, Vector((x, -0.84, 0.78)), (x * 0.5, 0.15, -1), L, 0.075, MANE, "Neck")
    # ---------------- the sun: 12 flat bronze ray blades with gold tips radiating from behind the mane
    for i in range(NR):
        d = ray_dir(i)
        ln = ray_len(i)
        w = (0.095 if i % 2 == 0 else 0.078) * (1 - 0.3 * max(0.0, -d.z))
        base = RC + d * R0
        ray = B.add(base + d * (ln / 2), (w, 0.02, ln / 2), RAY, "Ray%d" % (i + 1), R=ray_R(i), top=(0.06, 1),
                    role="limb", bevel=0.008, studs=[])
        B.add(ray.world((0, 0, ln * 0.30)), (w * 0.615, 0.024, ln * 0.20), GOLD, "Ray%d" % (i + 1), R=ray.R,
              top=(0.10, 1), studs=[], role="detail", bevel=0.007)
    # ---------------- legs: heavy forearms, big paws with 4 black claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.08)), K, 0.095, 0.125, FUR, leg, ext=0.0, ext1=0.03, top=(0.85, 0.75))
                B.seg(K, A, 0.082, 0.082, FUR, shin, top=(0.85, 0.88), ext=0.03, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.03, 0.08)), K, 0.078, 0.15, FUR, leg, bot=(0.85, 1), top=(0.75, 0.62),
                      ext=0.0, ext1=0.03)
                B.seg(K, A, 0.065, 0.075, FUR, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02)
                B.seg(A, P + Vector((0, 0.03, 0.035)), 0.055, 0.058, FUR, foot, ext=0.03)
            B.add(P, (0.09, 0.10, 0.05), PALE if fb == "F" else FUR, foot, top=(0.85, 0.80))               # paw
            for gx in (-0.054, -0.018, 0.018, 0.054):
                B.spike((P.x + gx, P.y - 0.088, 0.04), (0, -1, -0.55), 0.065, 0.014, BLACK, foot)
    # ---------------- long tail ending in a dark tuft
    T = [Vector(p) for p in TAILP]
    for (a, b), (w, d), bn in zip(zip(T, T[1:]), ((0.05, 0.055), (0.042, 0.045), (0.036, 0.038)),
                                  ("Tail1", "Tail2", "Tail3")):
        B.seg(a, b, w, d, FUR, bn, ext=0.04, top=(0.9, 0.9))
    tip = T[3]
    B.add(tip + Vector((0, 0.03, -0.01)), (0.06, 0.07, 0.06), MANE, "Tail3", rnd=0.4)
    for d, L in (((0, 0.8, -0.3), 0.14), ((0.5, 0.6, -0.5), 0.11), ((-0.5, 0.6, -0.5), 0.11), ((0, 0.4, -0.9), 0.12)):
        tuft(B, tip + Vector((0, 0.03, -0.01)), d, L, 0.05, MANE, "Tail3")
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.44, 0.76), "Root", tail=(0, -0.4, 0))            # at the hips: sitting pivots here
    k.joint("Chest", (0, -0.04, 0.76), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.56, 0.86), "Chest", tail=(0, -0.3, 0.15))
    k.joint("Head", (0, -0.85, 0.94), "Neck", tail=(0, -0.35, 0))           # throat pivot
    k.joint("Jaw", (0, -0.97, 0.91), "Head", tail=(0, -0.2, 0))
    k.joint("Rays", tuple(RC), "Head", tail=(0, -0.3, 0))                  # the sun wheel is carried by the head
    for i in range(NR):
        d = ray_dir(i)
        k.joint("Ray%d" % (i + 1), tuple(RC + d * R0), "Rays", tail=tuple(d * 0.25))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.12, -0.88, 1.13), "Head", tail=(0, 0, 0.2))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    for i in range(3):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=tuple(Vector(TAILP[i + 1]) - Vector(TAILP[i])))


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    P += [("Head", "Chest"), ("Jaw", "Chest"), ("Jaw", "Neck"), ("Ear_L", "Ear_R")]
    for i in range(NR):
        P.append(("Ray%d" % (i + 1), "Chest"))
    for i in (3, 4, 5, 6, 7, 8, 9):                 # side + lower rays pass in front of the front legs
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append(("Ray%d" % (i + 1), b))
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
        P.append(("Tail2", b))
        P.append(("Tail3", b))
    return P


def joints():
    out = []
    for i in range(NR):
        p = RC + ray_dir(i) * R0
        out.append((p, p, 0.10, "Ray%d" % (i + 1)))
    return out


# ------------------------------------------------------------------ animation (FIERCE_PLAN SolarLion)
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]


def ease(u):
    u = max(0.0, min(1.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)


def wheel(k, f, spin=0.0, out=0.0, flat=0.0, low_in=0.0, fwd=0.0):
    """spin = degrees the ray wheel has turned (about the forward axis); out = rays pushed outward along their own
    direction; flat 0..1 = the cone tilt flattened into the head plane (< 0 = tilted further back, gathered);
    low_in = the lower rays retract into the mane (head-down poses)"""
    cm.key_axis(k, "Rays", f, (0, -1, 0), spin, loc=(0, -fwd, 0))
    for i in range(NR):
        a = 2 * math.pi * i / NR
        t = Vector((math.cos(a), 0, -math.sin(a)))
        low = max(0.0, -math.cos(a - math.radians(spin)))           # how far down this ray points right now
        o = out - low_in * min(0.30, 0.65 * low) - (min(0.30, 0.6 * low) if abs(spin) > 1 else 0.0)
        cm.key_axis(k, "Ray%d" % (i + 1), f, t, max(TILT[i], 10) * flat, loc=tuple(ray_dir(i) * o))


def ears(k, f, pin=0.0):
    k.key("Ear_L", f, rot=(-pin, 0, 0))
    k.key("Ear_R", f, rot=(-pin, 0, 0))


def plant(k, n, legs=LEGS4, skip=None):
    import bpy
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in legs:
            if skip and skip(leg, f):
                continue
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


def idle(k):
    """KING'S SIT: sits down on its haunches with the chest high, surveys its kingdom with long holds (left, right),
    the tail swishing along the ground, the sun wheel drifting, then stands back up."""
    n = 120
    k.new_action("idle", n, True)

    def sit(f):
        return ease((f - 6) / 22) * (1 - ease((f - 94) / 22))

    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        u = sit(f)
        k.key("Spine", f, rot=(-15 * u, 0, 0), loc=(0, 0, 0.006 * b - 0.225 * u))
        k.key("Chest", f, rot=(-0.8 * b - 3 * u, 0, 0))
        sw = 14 * pk.wave(f, n, 0, 3)
        k.key("Tail1", f, rot=(40 * u + 6 * (1 - u), -30 * u + sw * (1 - 0.5 * u), 0))
        k.key("Tail2", f, rot=(-10 * u + 4 * (1 - u), sw * 1.2 - 20 * u, 0))
        k.key("Tail3", f, rot=(-8 * u + 4 * (1 - u), sw * 1.5 - 10 * u, 0))
        wheel(k, f, spin=0.0, low_in=u, fwd=0.05 * u)
    for f, nk, hd, yaw in ((0, 0, 0, 0), (6, 0, 0, 0), (28, 7, 2, 0), (34, 7, 2, 0), (40, 7, 1, 18), (58, 7, 1, 18),
                           (64, 7, 1, -18), (84, 7, 1, -18), (90, 7, 2, 0), (96, 7, 2, 0), (116, 0, 0, 0),
                           (n, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
    for f, pin in ((0, 0), (44, 0), (47, -14), (52, 0), (70, 0), (73, -14), (78, 0), (n, 0)):
        ears(k, f, pin)
    plant(k, n)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    """majestic shoulder-rolling walk, head carried low and steady, the sun wheel rocking."""
    n = 34

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 1.5 * pk.wave(f, n, 0.0), 1.5 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.025 * b))
        k.key("Chest", f, rot=(0, -2 * pk.wave(f, n, 0.25), -3 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(3 + 2 * pk.wave(f, n, 0.2, 2), 0, 0))
        k.key("Head", f, rot=(-2 * pk.wave(f, n, 0.3, 2), 2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        ears(k, f, 0)
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(6 + 3 * i, 10 * pk.wave(f, n, 0.3 + 0.12 * i), 0))
        wheel(k, f, spin=8 * pk.wave(f, n, 0.2, 2))
    return cm.quad_walk(k, n, 0.15, 0.11, body, gait="walk")


def roar(k):
    """LION ROAR: lowers its head as the mouth opens, then the full roar rises (head to level, jaw wide, flanks
    pumping), ending in 3 grunts (jaw pops); the tail lashes."""
    n = 64
    k.new_action("roar", n, False)
    for f, ch, nk, hd, jw, z, li in ((0, 0, 0, 0, 0, 0, 0), (10, 3, 14, 8, 16, -0.03, 1), (14, 3, 14, 8, 18, -0.03, 1),
                                     (20, -4, -2, -6, 36, 0.01, 0.2), (40, -4, -2, -6, 36, 0.01, 0.2),
                                     (44, -2, 0, -2, 12, 0.0, 0), (58, 0, 0, 0, 4, 0, 0), (n, 0, 0, 0, 0, 0, 0)):
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        wheel(k, f, low_in=li, out=0.04 * (20 <= f <= 40))
        ears(k, f, 20 if 10 <= f <= 44 else 0)
    for f in range(22, 40, 3):                                   # the flanks pump through the roar
        k.key("Chest", f, rot=(-4 + (3 if (f // 3) % 2 else -2), 0, 0))
    for f, jw in ((46, 26), (48, 8), (50, 24), (52, 7), (54, 22), (57, 4)):         # 3 grunts
        k.key("Jaw", f, rot=(jw, 0, 0))
    for f in range(0, n + 1, 2):
        lash = 26 * math.sin(2 * math.pi * f / 16) * ease((f - 14) / 6) * (1 - ease((f - 50) / 8))
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(10 + 4 * i, lash * (0.5 + 0.35 * i), 0))
    plant(k, n)
    k.finish(loop=False)


def sunburst(k):
    """SIGNATURE - LION AND SUN: plants its paws and puffs the chest, chin up while the rays gather in; the rays SHOOT
    out and the sun wheel turns a full circle as it strikes the emblem pose (right forepaw raised high, head at 3/4);
    the rays snap back in, paw down, a proud huff."""
    n = 90
    k.new_action("act_sunburst", n, False)
    for f, ch, nk, hd, yaw, jw, z in ((0, 0, 0, 0, 0, 0, 0), (12, -6, 0, 0, 0, 0, 0.02), (24, -8, -12, -8, 0, 0, 0.02),
                                      (40, -6, -10, -6, 15, 4, 0.02), (60, -6, -10, -6, 15, 4, 0.02),
                                      (70, -2, -4, -2, 0, 0, 0.0), (76, 0, 0, 0, 0, 0, 0), (80, 3, 2, 3, 0, 10, -0.02),
                                      (84, 0, 0, 0, 0, 2, 0), (n, 0, 0, 0, 0, 0, 0)):
        k.key("Chest", f, rot=(ch, 0, 3 * (40 <= f <= 60)))
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        ears(k, f, 0)
    for f in range(0, n + 1):
        if f <= 12:
            out, flat, spin = 0.0, 0.0, 0.0
        elif f <= 24:
            u = ease((f - 12) / 12)
            out, flat, spin = -0.05 * u, -0.4 * u, 0.0
        elif f <= 34:
            u = ease((f - 24) / 10)
            out, flat, spin = -0.05 + 0.11 * u, -0.4 + 1.4 * u, 0.0
        elif f <= 64:
            u = ease((f - 34) / 30)
            out, flat, spin = 0.06 + 0.01 * math.sin(2 * math.pi * f / 6), 1.0, 360 * u
        elif f <= 72:
            u = ease((f - 64) / 8)
            out, flat, spin = 0.06 * (1 - u), 1.0 - u, 360.0
        else:
            out, flat, spin = 0.0, 0.0, 360.0
        g = ease((f - 22) / 10) * (1 - ease((f - 64) / 10))
        wheel(k, f, spin=spin, out=out, flat=flat, low_in=ease((f - 30) / 8) * (1 - ease((f - 64) / 8)), fwd=0.10 * g)
    for f in range(0, n + 1, 2):
        up = ease(f / 12) * (1 - ease((f - 64) / 12))
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(6 + 4 * i + 24 * up, 8 * pk.wave(f, n, 0.2 + 0.1 * i, 3), 0))
    import bpy
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            if leg == "Leg_FR" and 38 <= f <= 69:               # the emblem: right forepaw raised high
                u = ease((f - 36) / 6) * (1 - ease((f - 64) / 6))
                k.key(leg, f, rot=(-62 * u, 0, 0))
                k.key("Shin_FR", f, rot=(-10 * u, 0, 0))
                k.key("Foot_FR", f, rot=(55 * u, 0, 0))
            else:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    sunburst(k)
    return stride


HEAD_XF = []
