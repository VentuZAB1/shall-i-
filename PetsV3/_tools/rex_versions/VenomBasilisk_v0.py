# Venom Basilisk (Wood/Grass egg, NEW 5% pet, 2026-10-14) - FIERCE style "the little king": a thorny serpent-lizard
# built from tapered blocks under a Roblox stud skin, in the family of our quadrupeds (Ivonrath's sprawled legs, Raiju's
# face recipe): a long low jungle-green body with black bands, sprawled clawed legs, a long whip tail with a thorn
# tip, a royal CREST FRILL of spines with venom-purple membranes fanned behind the skull (hero feature), a spined back
# SAIL with purple membranes, narrow venom-purple eyes under heavy brows, long dripping venom fangs. No glow.
import math
from mathutils import Vector

DISPLAY = "Venom Basilisk"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 6.5

# Blender colours (Roblox renders ~0.6x darker)
GREEN = (66, 164, 88)        # jungle green
GREEN_D = (30, 86, 52)       # back, crest/sail spines, socks
BAND = (22, 50, 34)          # black-green bands
PALE = (206, 224, 150)       # belly, throat, jaw
VENOM = (192, 72, 255)       # accent: frill / sail membranes, eyes, fang drips
VENOM_D = (112, 34, 172)
VENOM_HOT = (240, 204, 255)
IVORY = (242, 234, 204)      # spine tips, teeth
BLACK = (14, 14, 22)
MOUTH = (90, 22, 50)

H_MODEL = 1.25
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

LEGS = {"F": ((0.18, -0.42, 0.50), (0.33, -0.33, 0.30), (0.29, -0.45, 0.09), (0.29, -0.51, 0.04)),
        "B": ((0.17, 0.36, 0.50), (0.33, 0.27, 0.32), (0.30, 0.47, 0.12), (0.30, 0.41, 0.04))}
TAILP = [(0, 0.52, 0.52), (0, 0.95, 0.43), (0, 1.38, 0.35), (0, 1.80, 0.29), (0, 2.16, 0.27)]
SKULL = Vector((0, -0.98, 0.76))


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def spine_fan(B, root, dirs, lengths, bone, w=0.03):
    """spines (dark -> ivory tip) from root along dirs, with venom membranes between neighbours (both faces)"""
    tips = []
    for d, L in zip(dirs, lengths):
        d = Vector(d).normalized()
        m = root + d * L * 0.7
        B.seg(root, m, w, w, GREEN_D, bone, side=(1, 0, 0), ext=0.02, top=(0.8, 0.8), role="limb")
        B.spike(m - d * 0.01, d, L * 0.32, w * 0.9, IVORY, bone, top=(0.12, 0.12), nostud=True)
        tips.append(root + d * L * 0.92)
    for a, b in zip(tips, tips[1:]):
        B.poly([root, a, a.lerp(b, 0.5) - (a.lerp(b, 0.5) - root).normalized() * 0.05, b], 0.018, VENOM, bone)
    return tips


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=503, tier=3, plates=False)
    # ---------------- torso: long low body, chest -> waist -> hips, tapered underside, pale belly, dark bands
    B.add((0, -0.30, 0.55), (0.20, 0.30, 0.17), GREEN, "Chest", bot=(0.66, 0.6), top=(0.86, 0.9), rnd=0.40)
    B.add((0, 0.05, 0.53), (0.17, 0.16, 0.15), GREEN, "Spine", bot=(0.7, 0.8), top=(0.9, 0.95), rnd=0.40)
    B.add((0, 0.32, 0.52), (0.18, 0.22, 0.16), GREEN, "Spine", bot=(0.7, 0.75), top=(0.86, 0.9), rnd=0.40)
    B.seg((0, -0.56, 0.40), (0, 0.46, 0.38), 0.12, 0.025, PALE, "Chest", side=(1, 0, 0), top=(0.8, 0.9), ext=0.02)
    for y, w, bone in ((-0.46, 0.17, "Chest"), (-0.22, 0.18, "Chest"), (0.04, 0.155, "Spine"), (0.26, 0.16, "Spine"),
                       (0.46, 0.14, "Spine")):
        B.add((0, y, 0.70), (w, 0.04, 0.03), BAND, bone, top=(0.75, 1), rnd=0.3)               # back bands
        for s in (1, -1):
            B.bar((s * (w + 0.02), y - 0.02, 0.66), (s * (w + 0.035), y + 0.02, 0.47), Vector((s, 0, 0)), 0.06,
                  0.012, BAND, bone, studs=[], bevel=0.004)                                    # band down the flank
    # ---------------- neck + head (throat pivot): long flat lizard skull, tapered snout, brows, slit eyes
    B.seg((0, -0.56, 0.60), (0, -0.84, 0.70), 0.13, 0.12, GREEN, "Neck", ext=0.05, ext1=0.03, top=(0.9, 0.9))
    B.seg((0, -0.58, 0.52), (0, -0.84, 0.62), 0.09, 0.03, PALE, "Neck", side=(1, 0, 0), ext=0.02)
    B.add(SKULL, (0.14, 0.15, 0.09), GREEN, "Head", top=(0.82, 0.86), rnd=0.3)
    B.add(SKULL + Vector((0, 0.02, 0.085)), (0.11, 0.12, 0.02), GREEN_D, "Head", top=(0.75, 0.8))
    B.seg(SKULL + Vector((0, -0.12, -0.01)), SKULL + Vector((0, -0.38, -0.05)), 0.10, 0.065, GREEN, "Head",
          top=(0.6, 0.7), ext=0.02)                                                                     # snout
    for s in (1, -1):
        B.add(SKULL + Vector((s * 0.045, -0.375, 0.0)), (0.012, 0.006, 0.008), BLACK, "Head", studs=[],
              role="detail", bevel=0.003)                                                               # nostril
    # mouth line, upper teeth, long venom fangs with purple drips; lower jaw opens
    B.seg(SKULL + Vector((0, -0.10, -0.075)), SKULL + Vector((0, -0.36, -0.095)), 0.085, 0.008, MOUTH, "Jaw",
          studs=[], role="detail")
    for s in (1, -1):
        for y in (-0.16, -0.22, -0.28):
            B.spike(SKULL + Vector((s * 0.07, y, -0.075)), (0, 0, -1), 0.03, 0.01, IVORY, "Head")
        f0 = SKULL + Vector((s * 0.06, -0.33, -0.08))
        B.spike(f0, (0, -0.15, -1), 0.09, 0.016, IVORY, "Head")                                     # venom fang
        B.add(f0 + Vector((0, -0.012, -0.10)), (0.009, 0.009, 0.016), VENOM, "Head", studs=[], role="detail",
              bevel=0.006, nostud=True)                                                        # venom drip
    B.seg(SKULL + Vector((0, -0.08, -0.10)), SKULL + Vector((0, -0.35, -0.12)), 0.08, 0.025, PALE, "Jaw",
          top=(0.7, 1), ext=0.02)
    for s in (1, -1):
        c = SKULL + Vector((s * 0.10, -0.115, 0.035))
        B.add(c, (0.05, 0.008, 0.022), BLACK, "Head", rot=(0, -s * 16, s * 24), studs=[], role="detail", bevel=0.004)
        B.add(c + Vector((s * 0.002, -0.006, 0)), (0.042, 0.006, 0.011), VENOM, "Head", rot=(0, -s * 16, s * 24),
              studs=[], role="detail", bevel=0.003)
        B.add(c + Vector((s * 0.014, -0.009, 0.002)), (0.016, 0.004, 0.005), VENOM_HOT, "Head",
              rot=(0, -s * 16, s * 24), studs=[], role="detail", bevel=0.002)
        B.add(c + Vector((s * 0.0, -0.002, 0.04)), (0.065, 0.03, 0.024), GREEN_D, "Head", rot=(0, -s * 20, s * 22),
              role="detail", bevel=0.01)                                                        # brow
        for z, dz, L in ((-0.04, -0.3, 0.10), (0.02, 0.0, 0.12)):                                   # cheek thorns
            B.spike(SKULL + Vector((s * 0.13, 0.04, z)), (s * 0.5, 0.85, dz), L, 0.03, GREEN_D, "Head",
                    top=(0.12, 0.35))
    # ---------------- ROYAL CREST FRILL: a fan of 7 spines behind the skull with venom membranes (hero feature)
    root = SKULL + Vector((0, 0.10, 0.06))
    dirs = [(-0.55, 0.55, 0.62), (-0.32, 0.55, 0.85), (-0.14, 0.5, 1.0), (0.0, 0.45, 1.05), (0.14, 0.5, 1.0),
            (0.32, 0.55, 0.85), (0.55, 0.55, 0.62)]
    spine_fan(B, root, dirs, (0.22, 0.30, 0.36, 0.40, 0.36, 0.30, 0.22), "Frill", w=0.026)
    # ---------------- BACK SAIL: spines from the withers to the hips with venom membranes (seen from the game cam)
    sail_root = [Vector((0, y, 0.70)) for y in (-0.44, -0.28, -0.10, 0.08, 0.26, 0.42)]
    sail_len = (0.20, 0.30, 0.36, 0.34, 0.26, 0.16)
    tips = []
    for p, L, bone in zip(sail_root, sail_len, ("Chest", "Chest", "Chest", "Spine", "Spine", "Spine")):
        d = Vector((0, 0.35, 1)).normalized()
        m = p + d * L * 0.72
        B.seg(p - d * 0.02, m, 0.026, 0.03, GREEN_D, bone, side=(1, 0, 0), top=(0.8, 0.8), role="limb")
        B.spike(m - d * 0.01, d, L * 0.3, 0.026, IVORY, bone, top=(0.12, 0.12), nostud=True)
        tips.append((p + d * L * 0.88, bone))
    for (a, ba), (b, bb), p0, p1 in zip(tips, tips[1:], sail_root, sail_root[1:]):
        bone = ba if ba == bb else "Spine"
        if ba != bb:
            continue
        B.poly([p0 + Vector((0, 0, 0.02)), a, a.lerp(b, 0.5) - Vector((0, 0, 0.05)), b, p1 + Vector((0, 0, 0.02))],
               0.016, VENOM, bone)
    # ---------------- sprawled legs: elbows / knees out, dark socks, 4 black claws, knee thorn (Ivonrath)
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.05)), K, 0.072, 0.085, GREEN, leg, ext1=0.04, top=(0.8, 0.8))
                B.seg(K, A, 0.058, 0.06, GREEN_D, shin, top=(0.85, 0.85), ext=0.04, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.02, 0.05)), K, 0.085, 0.12, GREEN, leg, ext1=0.04, top=(0.75, 0.7))
                B.seg(K, A, 0.058, 0.062, GREEN_D, shin, top=(0.85, 0.85), ext=0.04, ext1=0.02)
                B.seg(A, P + Vector((0, 0.03, 0.03)), 0.05, 0.05, GREEN_D, foot, ext=0.03)
            B.spike(K + Vector((s * 0.04, 0.03, 0.0)), (s * 0.7, 0.7, 0.1), 0.09, 0.026, GREEN_D,
                    shin if fb == "F" else leg)
            B.add(P, (0.07, 0.085, 0.04), GREEN_D, foot, top=(0.85, 0.80))
            for gx in (-0.045, -0.015, 0.015, 0.045):
                B.spike((P.x + gx, P.y - 0.075, 0.03), (gx * 1.5, -1, -0.5), 0.07, 0.014, BLACK, foot)
    # ---------------- long whip tail: green with bands, thorn pairs, a 3-thorn ivory tip
    T = [Vector(p) for p in TAILP]
    dims = ((0.13, 0.12), (0.10, 0.095), (0.075, 0.07), (0.05, 0.048))
    for i, ((a, b), (w, d)) in enumerate(zip(zip(T, T[1:]), dims)):
        bone = "Tail%d" % (i + 1)
        B.seg(a, b, w, d, GREEN, bone, ext=0.08 if i == 0 else 0.03, ext1=0.02, top=(0.82, 0.82))
        B.seg(a + Vector((0, 0, -d + 0.01)), b + Vector((0, 0, -dims[min(i + 1, 3)][1] * 0.82 + 0.01)), w * 0.7,
              0.014, PALE, bone, ext=0.02)
        mid = a.lerp(b, 0.5)
        B.add(mid + Vector((0, 0, d * 0.75)), (w * 0.9, 0.035, d * 0.35), BAND, bone, rnd=0.3)
        for s in (1, -1):
            B.spike(a.lerp(b, 0.7) + Vector((s * w * 0.8, 0, d * 0.4)), (s * 0.6, 0.6, 0.5), 0.07 - 0.01 * i, 0.022,
                    GREEN_D, bone, top=(0.12, 0.35))
    tip = T[4]
    for d in ((0, 1, 0.15), (0.45, 0.8, 0.3), (-0.45, 0.8, 0.3)):
        B.spike(tip - Vector((0, 0.03, 0)), d, 0.14, 0.03, IVORY, "Tail4", top=(0.12, 0.12), nostud=True)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.22, 0.54), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.10, 0.55), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.54, 0.60), "Chest", tail=(0, -0.25, 0.08))
    k.joint("Head", tuple(SKULL + Vector((0, 0.12, -0.06))), "Neck", tail=(0, -0.35, 0))      # throat pivot
    k.joint("Jaw", tuple(SKULL + Vector((0, -0.06, -0.08))), "Head", tail=(0, -0.3, 0))
    k.joint("Frill", tuple(SKULL + Vector((0, 0.10, 0.06))), "Head", tail=(0, 0.1, 0.2))
    for s, side in ((1, "L"), (-1, "R")):
        for fb, parent, knee in (("F", "Chest", (s * 0.8, 1, 0)), ("B", "Spine", (s * 0.8, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    for i in range(4):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=(Vector(TAILP[i + 1]) - Vector(TAILP[i])) if i == 3 else None)


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Head", "Chest"), ("Jaw", "Chest"), ("Frill", "Chest"),
         ("Frill", "Neck"), ("Head", "Shin_FL"), ("Head", "Shin_FR"), ("Jaw", "Shin_FL"), ("Jaw", "Shin_FR")]
    for t in ("Tail2", "Tail3", "Tail4"):
        for b in ("Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
            P.append((t, b))
    return P


HEAD_XF = []
