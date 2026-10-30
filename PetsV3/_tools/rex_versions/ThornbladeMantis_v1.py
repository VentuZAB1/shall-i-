# Thornblade Mantis (Wood/Grass egg, NEW 2% SECRET, 2026-10-14) - FIERCE style "the jade executioner": a warrior
# praying mantis built from tapered blocks under a Roblox stud skin. A raised prothorax carries a triangular head with
# huge RUBY compound eyes (black pseudo-pupils), an angry brow, dark mandibles and a GOLD cone-crown (hero piece #1,
# reads at icon size). Two raptorial forelegs held in the prayer pose: jade coxa, a broad femur with a GOLD scythe edge
# lined with RUBY thorn crystals and a folded GOLD tibia hook (hero piece #2). Four long spidery walking legs, a
# segmented abdomen under folded leaf-wings (tegmina: dark rim, jade panel, dark veins, gold costal stripe) that hide
# the hindwings with RUBY eye-spots - revealed in the threat display (roar). 3-band colour: dark teal armour / jade
# hide / pale mint underside. No glow.
import math
from mathutils import Vector, Matrix

DISPLAY = "Thornblade Mantis"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 10.0       # total height (crown tip) in studs at x1 - the 2% secret stands over its egg (Treant 10, Stag 11)

# Blender colours (Roblox renders ~0.6x darker)
ARMOR = (18, 74, 70)         # dark teal armour: plates, rims, veins, brows, mandibles, tibiae
HIDE = (36, 182, 146)        # jade hide
HIDE_L = (88, 214, 170)      # light jade wing panels
BELLY = (198, 242, 216)      # pale mint underside
BELLY_D = (150, 206, 178)
GOLD = (255, 196, 50)        # HERO: crown, scythe edges, tibia hooks, costal stripes
GOLD_D = (204, 138, 24)
RUBY_D = (128, 10, 44)       # ACCENT crystal steps: deep -> ruby -> hot
RUBY = (240, 40, 76)
RUBY_HOT = (255, 192, 204)
BLACK = (14, 14, 22)
IVORY = (240, 234, 210)

# walking legs (left): hip, knee (high, out), ankle, toe;  F = middle pair, B = hind pair
LEGS = {"F": ((0.12, -0.06, 0.42), (0.40, -0.22, 0.66), (0.52, -0.42, 0.11), (0.56, -0.54, 0.02)),
        "B": ((0.12, 0.14, 0.42), (0.42, 0.30, 0.66), (0.54, 0.60, 0.11), (0.58, 0.72, 0.02))}
PRO = (Vector((0, -0.06, 0.52)), Vector((0, -0.38, 0.94)))        # prothorax (Chest) base -> top
NECK = Vector((0, -0.40, 0.96))
HEADP = Vector((0, -0.45, 1.02))                                  # head pivot
HC = Vector((0, -0.50, 1.10))                                     # head centre
# raptorial foreleg (left): coxa root, coxa-femur joint ("elbow", low), femur-tibia joint (high), tibia tip
ARM = (Vector((0.07, -0.30, 0.82)), Vector((0.15, -0.42, 0.58)), Vector((0.165, -0.60, 0.90)),
       Vector((0.16, -0.63, 0.62)))
ABD = [Vector(p) for p in ((0, 0.20, 0.44), (0, 0.52, 0.45), (0, 0.82, 0.48), (0, 1.06, 0.56))]
WROOT = Vector((0.03, 0.02, 0.58))     # wing hinge (left)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def ruby_gem(B, c, n, size, bone):
    """faceted ruby crystal: deep base -> ruby body -> hot tip along n"""
    n = Vector(n).normalized()
    c = Vector(c)
    B.spike(c - n * 0.01, n, size * 1.0, size * 0.55, RUBY_D, bone, top=(0.7, 0.7))
    B.spike(c + n * size * 0.25, n, size * 0.85, size * 0.42, RUBY, bone, top=(0.15, 0.15))
    B.spike(c + n * size * 0.75, n, size * 0.40, size * 0.18, RUBY_HOT, bone, top=(0.1, 0.1))


def leaf(s, t, w):
    """outline point of the folded tegmen at length t (0 hinge -> 1 tip), across w (0 midline -> 1 outer edge)"""
    y = WROOT.y + t * 1.00
    half = 0.17 * math.sin(math.pi * min(1.0, t * 1.08) ** 0.75) + 0.02
    x = s * (0.02 + w * half)
    z = 0.592 + 0.04 * t - 0.035 * w * w
    return Vector((x, y, z))


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=211, tier=3, plates=False)
    # ---------------- thorax (Spine): meso/metathorax block, dark dorsal plate, pale underside
    B.add((0, 0.04, 0.44), (0.13, 0.20, 0.10), HIDE, "Spine", bot=(0.8, 0.85), top=(0.85, 0.95), rnd=0.30)
    B.add((0, 0.04, 0.542), (0.10, 0.18, 0.018), ARMOR, "Spine", top=(0.85, 0.9))
    B.add((0, 0.04, 0.338), (0.09, 0.15, 0.014), BELLY, "Spine", studs=[])
    # ---------------- abdomen (Tail1-3): wide flat segments, pale ventral plates, dark tergite rings, rising tip
    dims = ((0.15, 0.085), (0.155, 0.085), (0.11, 0.07))
    for i, ((a, b), (w, d)) in enumerate(zip(zip(ABD, ABD[1:]), dims)):
        bone = "Tail%d" % (i + 1)
        B.seg(a, b, w, d, HIDE, bone, ext=0.06 if i == 0 else 0.02, ext1=0.02, top=(0.9 if i < 2 else 0.55, 0.85))
        B.seg(a + Vector((0, 0, -d + 0.01)), b + Vector((0, 0, -d * 0.8 + 0.01)), w * 0.75, 0.014, BELLY, bone,
              ext=0.01)
        for t in (0.3, 0.75):
            p = a.lerp(b, t)
            B.seg(p - (b - a).normalized() * 0.018, p + (b - a).normalized() * 0.018, w * (1.03 - 0.25 * t * (i == 2)),
                  d * 1.04, ARMOR, bone, top=(0.98, 0.98))                                    # tergite ring
    for s in (1, -1):                                                                       # cerci at the tip
        B.spike(ABD[3] + Vector((s * 0.03, -0.02, 0)), (s * 0.3, 1, 0.25), 0.10, 0.014, ARMOR, "Tail3")
    # ---------------- folded hindwings (hidden under the tegmina; RUBY eye-spot shown in the threat display)
    for s, side in ((1, "L"), (-1, "R")):
        hb = "Wing_" + side
        P = [leaf(s, t, w) - Vector((0, 0, 0.026)) for t, w in ((0.02, 0.1), (0.25, 0.85), (0.6, 0.85), (0.9, 0.5),
                                                                  (0.97, 0.05), (0.5, 0.0))]
        B.poly([P[5], P[0], P[1], P[2], P[3], P[4]], 0.014, ARMOR, hb)
        eye = leaf(s, 0.55, 0.45) - Vector((0, 0, 0.026))
        for r, c, dz in ((0.085, BLACK, 0.0), (0.062, RUBY_D, 0.004), (0.046, RUBY, 0.008), (0.018, RUBY_HOT, 0.012)):
            pts = [eye + Vector((r * 0.75 * math.cos(a), r * 1.15 * math.sin(a), dz)) for a in
                   [2 * math.pi * i / 12 for i in range(12)]]
            B.poly([eye + Vector((0, 0, dz))] + pts + [pts[0]], 0.012, c, hb)
    # ---------------- tegmina (folded leaf-wings, the main read from the game camera)
    for s, side in ((1, "L"), (-1, "R")):
        eb = "Elytra_" + side
        out = [leaf(s, t, 1.0) for t in (0.0, 0.12, 0.3, 0.5, 0.7, 0.86, 0.97)]
        mid = [leaf(s, t, 0.0) for t in (0.97, 0.7, 0.4, 0.1)]
        B.poly([leaf(s, 0.45, 0.5)] + out + mid + [out[0]], 0.024, ARMOR, eb)                   # dark rim
        inner = [leaf(s, t, 0.86) + Vector((0, 0, 0.006)) for t in (0.08, 0.3, 0.5, 0.7, 0.84)]
        inner += [leaf(s, t, 0.12) + Vector((0, 0, 0.006)) for t in (0.84, 0.6, 0.3, 0.08)]
        B.poly([leaf(s, 0.45, 0.5) + Vector((0, 0, 0.006))] + inner + [inner[0]], 0.022, HIDE_L, eb)  # jade panel
        # gold costal stripe along the outer edge + dark veins
        cs = [leaf(s, t, 0.93) + Vector((0, 0, 0.012)) for t in (0.06, 0.25, 0.45, 0.65, 0.82)]
        for a, b in zip(cs, cs[1:]):
            B.bar(a, b, Vector((s * 0.25, 0, 1)), 0.032, 0.008, GOLD, eb, studs=[], bevel=0.003)
        vm = [leaf(s, t, 0.5) + Vector((0, 0, 0.014)) for t in (0.06, 0.3, 0.55, 0.8, 0.93)]
        for a, b in zip(vm, vm[1:]):
            B.bar(a, b, Vector((0, 0, 1)), 0.016, 0.006, ARMOR, eb, studs=[], bevel=0.002)      # mid vein
        for t in (0.28, 0.48, 0.68):
            a = leaf(s, t, 0.5) + Vector((0, 0, 0.014))
            b = leaf(s, t + 0.1, 0.88) + Vector((0, 0, 0.014))
            B.bar(a, b, Vector((0, 0, 1)), 0.012, 0.006, ARMOR, eb, studs=[], bevel=0.002)      # side veins
    # ---------------- prothorax (Chest): long raised neck-shield, dark dorsal ridge, pale throat, pronotum flare
    B.seg(PRO[0] + Vector((0, 0.04, -0.04)), PRO[1], 0.085, 0.075, HIDE, "Chest", ext=0.05, ext1=0.03, top=(0.8, 0.9))
    B.seg(PRO[0].lerp(PRO[1], 0.08), PRO[1], 0.035, 0.085, ARMOR, "Chest", top=(0.7, 0.9))           # dorsal keel
    d = (PRO[1] - PRO[0]).normalized()
    nrm = Vector((0, 0.8, -0.6)).normalized()
    B.seg(PRO[0].lerp(PRO[1], 0.15) - nrm * 0.0 + Vector((0, -0.05, -0.04)),
          PRO[1] + Vector((0, -0.05, -0.05)), 0.06, 0.03, BELLY, "Chest", top=(0.8, 1))                # throat
    for t, w in ((0.55, 0.13), (0.78, 0.115)):                                               # pronotum flares
        p = PRO[0].lerp(PRO[1], t)
        B.seg(p - d * 0.05, p + d * 0.05, w, 0.05, ARMOR, "Chest", top=(0.9, 0.9))
        for s in (1, -1):
            B.spike(p + Vector((s * w, 0, 0)), (s, 0.25, 0.15), 0.07, 0.02, ARMOR, "Chest", top=(0.12, 0.3))
    B.seg(NECK + Vector((0, 0.02, -0.03)), HEADP + Vector((0, -0.02, 0.0)), 0.06, 0.05, HIDE, "Neck", ext=0.03)
    # ---------------- head: triangular face, huge RUBY compound eyes, black pseudo-pupils, angry brow
    B.add(HC, (0.115, 0.07, 0.085), HIDE, "Head", bot=(0.42, 0.85), top=(1.0, 0.95), rnd=0.25)
    B.add(HC + Vector((0, -0.015, -0.115)), (0.05, 0.05, 0.035), HIDE, "Head", bot=(0.6, 0.8))       # lower face
    B.add(HC + Vector((0, -0.068, 0.0)), (0.06, 0.01, 0.06), BELLY, "Head", bot=(0.5, 1), studs=[], role="detail",
          bevel=0.005)                                                                         # face plate
    for s in (1, -1):
        e = HC + Vector((s * 0.125, -0.015, 0.045))
        B.add(e, (0.058, 0.06, 0.066), RUBY_D, "Head", rnd=0.5, studs=[], nostud=True, bot=(0.75, 0.8),
              top=(0.75, 0.8))                                                                 # eye bulb
        B.add(e + Vector((s * 0.006, -0.014, 0.004)), (0.052, 0.05, 0.05), RUBY, "Head", rnd=0.5, studs=[],
              nostud=True, bot=(0.7, 0.8), top=(0.7, 0.8), role="detail")
        B.add(e + Vector((s * 0.012, -0.058, 0.02)), (0.016, 0.006, 0.016), RUBY_HOT, "Head", studs=[],
              role="detail", bevel=0.004)                                                     # highlight
        B.add(e + Vector((-s * 0.006, -0.061, -0.006)), (0.013, 0.006, 0.02), BLACK, "Head", studs=[],
              role="detail", bevel=0.004)                                                     # pseudo-pupil
        B.add(e + Vector((-s * 0.04, -0.05, 0.062)), (0.06, 0.026, 0.018), ARMOR, "Head", rot=(0, s * 24, 0),
              role="detail", bevel=0.008)                                                     # angry brow
        # mandibles (dark, ivory tips) + palps
        m0 = HC + Vector((s * 0.035, -0.04, -0.15))
        B.spike(m0, (-s * 0.55, -0.6, -0.55), 0.075, 0.018, ARMOR, "Jaw", top=(0.4, 0.4))
        B.spike(m0 + Vector((-s * 0.03, -0.035, -0.035)), (-s * 0.9, -0.3, -0.3), 0.035, 0.009, IVORY, "Jaw")
        B.spike(HC + Vector((s * 0.05, -0.03, -0.12)), (s * 0.4, -0.5, -1), 0.07, 0.01, ARMOR, "Jaw")
        # antennae: long thin whips from between the eyes, swept up-back
        a0 = HC + Vector((s * 0.028, -0.06, 0.07))
        a1 = a0 + Vector((s * 0.08, 0.02, 0.24))
        a2 = a1 + Vector((s * 0.12, 0.16, 0.16))
        B.seg(a0, a1, 0.012, 0.012, ARMOR, "Antenna_" + side, ext=0.01, role="limb")
        B.seg(a1, a2, 0.009, 0.009, ARMOR, "Antenna_" + side, ext=0.005, role="limb")
    # GOLD CONE-CROWN (hero #1): tall central cone + 2 side prongs on a gold band, ruby gem at the base
    cb = HC + Vector((0, 0.01, 0.10))
    B.add(cb, (0.07, 0.04, 0.022), GOLD, "Head", top=(0.85, 0.85), role="limb", bevel=0.008)
    B.spike(cb + Vector((0, 0.0, 0.01)), (0, 0.35, 1), 0.26, 0.045, GOLD, "Head", top=(0.12, 0.12))
    for s in (1, -1):
        B.spike(cb + Vector((s * 0.05, 0.0, 0.01)), (s * 0.45, 0.25, 1), 0.13, 0.03, GOLD, "Head", top=(0.12, 0.12))
    B.spike(cb + Vector((0, 0.02, 0.06)), (0, 0.35, 1), 0.12, 0.022, GOLD_D, "Head", top=(0.3, 0.3))   # cone keel
    ruby_gem(B, cb + Vector((0, -0.038, 0.0)), (0, -1, 0.15), 0.045, "Head")
    # ---------------- raptorial forelegs (hero #2): coxa -> femur scythe (gold edge, ruby thorns) -> gold tibia hook
    for s, side in ((1, "L"), (-1, "R")):
        C0, C1, F1, T1 = (X(p, s) for p in ARM)
        arm, fore, blade = "Arm_" + side, "Fore_" + side, "Blade_" + side
        B.seg(C0, C1, 0.045, 0.05, HIDE, arm, ext=0.04, ext1=0.03, top=(0.8, 0.8))                  # coxa
        B.add(C1, (0.05, 0.05, 0.05), ARMOR, arm, rnd=0.3)                                           # joint
        fem = B.seg(C1, F1, 0.055, 0.08, HIDE, fore, ext=0.03, ext1=0.04, top=(0.7, 0.8))            # femur
        fd = (F1 - C1).normalized()
        fwd = Vector((0, -1, 0))
        edge = (fwd - fd * fwd.dot(fd)).normalized()                                             # femur's front edge
        B.seg(C1 + edge * 0.07 + fd * 0.02, F1 + edge * 0.06, 0.03, 0.026, GOLD, fore, top=(0.6, 0.8), ext1=0.02)
        for t in (0.25, 0.45, 0.65, 0.85):
            ruby_gem(B, C1.lerp(F1, t) + edge * 0.085, edge + fd * 0.35, 0.05 if t in (0.45, 0.65) else 0.04, fore)
        B.add(F1, (0.045, 0.045, 0.045), ARMOR, fore, rnd=0.3)                                       # knee
        td = (T1 - F1).normalized()
        B.seg(F1, T1, 0.028, 0.034, GOLD, blade, ext=0.02, top=(0.7, 0.6))                           # tibia
        tedge = (fwd - td * fwd.dot(td)).normalized()
        for t in (0.3, 0.55, 0.78):
            B.spike(F1.lerp(T1, t) + tedge * 0.025, tedge * 0.8 - td * 0.6, 0.045, 0.012, GOLD_D, blade)
        B.spike(T1 - td * 0.01, td * 0.6 + tedge * 0.8 + Vector((0, 0, 0.3)), 0.07, 0.018, BLACK, blade)  # hook
    # ---------------- walking legs: jade femur up-out to a high knee, dark tibia down, black tarsus
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            B.seg(H, K, 0.042, 0.048, HIDE, leg, ext=0.03, ext1=0.03, top=(0.8, 0.8))
            B.add(K, (0.048, 0.048, 0.048), ARMOR, leg, rnd=0.3)
            B.seg(K, A, 0.032, 0.034, ARMOR, shin, ext=0.02, ext1=0.02, top=(0.7, 0.7))
            for t in (0.3, 0.55):
                B.spike(K.lerp(A, t), (s * 0.5, 0.0, -0.4) if fb == "F" else (s * 0.5, 0.3, -0.3), 0.04, 0.009,
                        GOLD_D, shin)
            B.seg(A, P, 0.02, 0.018, ARMOR, foot, ext=0.015)
            B.spike(P, P - A, 0.05, 0.012, BLACK, foot)
    B.build()
    mn, mx = k.bounds()
    pitch = 0.2243 * (mx.z - mn.z) / HEIGHT
    bk.stud_skin(k, pitch)
    return {"TH": round(B.th, 3), "pitch": round(pitch, 4), "H": round(mx.z - mn.z, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.04, 0.44), "Root", tail=(0, -0.3, 0))
    k.joint("Chest", tuple(PRO[0]), "Spine", tail=tuple(PRO[1] - PRO[0]))
    k.joint("Neck", tuple(NECK), "Chest", tail=(0, -0.05, 0.06))
    k.joint("Head", tuple(HEADP), "Neck", tail=(0, -0.1, 0.1))
    k.joint("Jaw", tuple(HC + Vector((0, -0.03, -0.12))), "Head", tail=(0, -0.05, -0.08))
    k.joint("Strike", tuple(HC + Vector((0, -0.45, -0.25))), "Chest", tail=(0, -0.2, 0))   # strike VFX anchor
    for s, side in ((1, "L"), (-1, "R")):
        C0, C1, F1, T1 = (X(p, s) for p in ARM)
        k.joint("Antenna_" + side, tuple(HC + Vector((s * 0.028, -0.06, 0.07))), "Head", tail=(s * 0.08, 0.02, 0.24))
        k.joint("Arm_" + side, tuple(C0), "Chest")
        k.joint("Fore_" + side, tuple(C1), "Arm_" + side)
        k.joint("Blade_" + side, tuple(F1), "Fore_" + side, tail=tuple(T1 - F1))
        k.joint("Elytra_" + side, tuple(X(WROOT, s)), "Spine", tail=(0, 0.5, 0.02))
        k.joint("Wing_" + side, tuple(X(WROOT, s) - Vector((0, 0, 0.02))), "Spine", tail=(0, 0.5, 0.02))
        for fb, knee in (("F", (s * 0.5, -0.2, 1)), ("B", (s * 0.5, 0.2, 1))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, "Spine")
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=tuple(P - A))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", tuple(ABD[0]), "Spine")
    k.joint("Tail2", tuple(ABD[1]), "Tail1")
    k.joint("Tail3", tuple(ABD[2]), "Tail2", tail=tuple(ABD[3] - ABD[2]))


LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]


def check_pairs():
    P = []
    for s in ("L", "R"):
        P += [("Leg_F" + s, "Leg_B" + s), ("Shin_F" + s, "Shin_B" + s), ("Foot_F" + s, "Foot_B" + s),
              ("Fore_" + s, "Head"), ("Blade_" + s, "Head"), ("Fore_" + s, "Jaw"), ("Blade_" + s, "Jaw"),
              ("Blade_" + s, "Chest"), ("Fore_" + s, "Shin_F" + s), ("Blade_" + s, "Shin_F" + s),
              ("Elytra_" + s, "Tail1"), ("Elytra_" + s, "Tail2"), ("Elytra_" + s, "Tail3"),
              ("Wing_" + s, "Elytra_" + s), ("Shin_B" + s, "Tail2"), ("Shin_B" + s, "Tail3")]
    P += [("Fore_L", "Fore_R"), ("Blade_L", "Blade_R"), ("Fore_L", "Blade_R"), ("Fore_R", "Blade_L"),
          ("Elytra_L", "Elytra_R"), ("Wing_L", "Wing_R")]
    return P


HEAD_XF = []
