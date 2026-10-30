"""Water area creatures (Tide egg): SeaTurtlePup, Kappa, Hippocampus, KrakenHatchling.
Run: blender -b -P water.py [-- Name]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import creature_kit as K
from creature_kit import box, ellipsoid, cone, limb, mirror_x, join_as, pivot, eye_pair

EYES = {"white": "#ffffff", "pupil": "#1d1a24"}


def sea_turtle_pup():
    K.new_scene("SeaTurtlePup")
    K.palette({**EYES, "shell": "#2bb3a3", "plate": "#5fd6c4", "rim": "#f2d9a0", "skin": "#8fd3b0",
               "skin2": "#6dbf98", "belly": "#fff0c4", "mouth": "#2a4a3e", "blush": "#ff9eb5"})
    shell = ellipsoid("_shell", (1.1, 1.25, 0.72), (0, 0.1, 0.9), "shell", segs=12, rings=7)
    plates = [ellipsoid("_plate", (0.34, 0.36, 0.1), (x, y, z), "plate", segs=6, rings=3, smooth=False,
                        rot=(rx, ry, 0))
              for x, y, z, rx, ry in ((0, 0.1, 1.6, 0, 0), (0.55, -0.3, 1.33, 25, 35), (-0.55, -0.3, 1.33, 25, -35),
                                      (0.55, 0.55, 1.33, -25, 35), (-0.55, 0.55, 1.33, -25, -35))]
    rim = cone("_rim", 1.16, 1.16, 0.18, (0, 0.1, 0.55), "rim", verts=14)
    belly = ellipsoid("_belly", (1.0, 1.15, 0.25), (0, 0.1, 0.58), "belly", segs=10, rings=4)
    tail = cone("_tail", 0.14, 0.02, 0.35, (0, 1.3, 0.62), "skin", verts=6, rot=(-100, 0, 0))
    body = join_as("Body", [shell, rim, belly, tail] + plates)
    pivot(body, (0, 0.1, 0.85))

    neck = limb("_neck", (0, -0.8, 0.8), (0, -1.3, 1.05), 0.3, 0.28, "skin")
    head = ellipsoid("_head", (0.6, 0.6, 0.55), (0, -1.65, 1.25), "skin", segs=12, rings=8)
    mouth = box("_mouth", (0.3, 0.04, 0.04), (0, -2.2, 1.02), "mouth", bevel=0.3)
    blush = [ellipsoid("_blush", (0.12, 0.04, 0.07), (0.38 * s, -2.1, 1.1), "blush", segs=6, rings=3) for s in (1, -1)]
    head = join_as("Head", [neck, head, mouth] + blush + eye_pair(0.27, -2.08, 1.35, 0.17))
    pivot(head, (0, -0.85, 0.85))

    for name, x, y, rz, sz in (("LegFL", 0.85, -0.55, -30, 1.0), ("LegBL", 0.75, 0.8, 30, 0.7)):
        fl = ellipsoid("_flip", (0.55 * sz, 0.22, 0.09), (x + 0.35 * sz, y, 0.55), "skin2", segs=10, rings=5, rot=(0, -15, rz))
        leg = join_as(name, [fl])
        pivot(leg, (x, y, 0.6))
        mirror_x(leg, name[:-1] + "R")
    return K.finish("SeaTurtlePup")


def kappa():
    K.new_scene("Kappa")
    K.palette({**EYES, "skin": "#5fb85a", "skin2": "#4a9a47", "belly": "#f3e39a", "beak": "#ffb638",
               "shell": "#6b5a2e", "shell2": "#8a7640", "hair": "#2f6b3a", "dish": "#f4f1e4",
               "water": "#5ec8ff", "foot": "#ff9c3a", "mouth": "#3a2418"})
    torso = ellipsoid("_torso", (0.6, 0.5, 0.7), (0, 0, 1.25), "skin", segs=12, rings=8)
    belly = ellipsoid("_belly", (0.45, 0.2, 0.55), (0, -0.33, 1.2), "belly", segs=10, rings=6)
    shell = ellipsoid("_shell", (0.62, 0.35, 0.72), (0, 0.33, 1.3), "shell", segs=10, rings=6, smooth=False)
    shellrim = ellipsoid("_shellrim", (0.66, 0.2, 0.76), (0, 0.22, 1.3), "shell2", segs=10, rings=6)
    body = join_as("Body", [torso, belly, shell, shellrim])
    pivot(body, (0, 0, 1.0))

    head = ellipsoid("_head", (0.62, 0.58, 0.55), (0, -0.05, 2.35), "skin", segs=14, rings=9)
    beak = cone("_beak", 0.25, 0.05, 0.4, (0, -0.5, 2.18), "beak", verts=8, rot=(90, 0, 0))
    beak2 = ellipsoid("_beak2", (0.26, 0.2, 0.1), (0, -0.55, 2.1), "beak", segs=8, rings=4)
    hair = []
    for i in range(14):
        a = i * 2 * math.pi / 14
        if math.sin(a) < -0.55:
            continue  # leave the face clear
        cx, cy = math.cos(a), math.sin(a)
        hair.append(limb("_hair", (0.5 * cx, -0.05 + 0.48 * cy, 2.7), (0.78 * cx, -0.05 + 0.75 * cy, 2.78),
                         0.12, 0.02, "hair", verts=5, smooth=False))
    dish = cone("_dish", 0.42, 0.5, 0.1, (0, -0.05, 2.82), "dish", verts=14)
    water = cone("_water", 0.4, 0.4, 0.02, (0, -0.05, 2.925), "water", verts=14)
    head = join_as("Head", [head, beak, beak2, dish, water] + hair + eye_pair(0.27, -0.5, 2.5, 0.15))
    pivot(head, (0, -0.05, 1.85))

    arm = limb("_arm", (0.55, 0, 1.55), (0.85, -0.15, 1.0), 0.12, 0.1, "skin")
    hand = ellipsoid("_hand", (0.16, 0.14, 0.12), (0.88, -0.18, 0.92), "skin2", segs=8, rings=5)
    armL = join_as("ArmL", [arm, hand])
    pivot(armL, (0.55, 0, 1.55))
    mirror_x(armL, "ArmR")

    leg = limb("_leg", (0.28, 0, 0.75), (0.3, 0, 0.15), 0.16, 0.13, "skin")
    foot = ellipsoid("_foot", (0.22, 0.34, 0.1), (0.3, -0.15, 0.1), "foot", segs=8, rings=4)
    legL = join_as("LegL", [leg, foot])
    pivot(legL, (0.28, 0, 0.75))
    mirror_x(legL, "LegR")
    return K.finish("Kappa")


def hippocampus():
    K.new_scene("Hippocampus")
    K.palette({**EYES, "hide": "#4fc3c9", "hide2": "#39a7b5", "belly": "#d4f5ef", "fin": "#6f7ff0",
               "fin2": "#9aa6ff", "hoof": "#2f5d80", "nose": "#23384a", "scale": "#2f93a8"})
    chest = ellipsoid("_chest", (0.55, 0.8, 0.65), (0, 0, 1.3), "hide", segs=12, rings=8)
    belly = ellipsoid("_belly", (0.45, 0.65, 0.4), (0, -0.05, 1.05), "belly", segs=10, rings=6)
    body = join_as("Body", [chest, belly])
    pivot(body, (0, 0, 1.3))

    neck = limb("_neck", (0, -0.4, 1.6), (0, -0.75, 2.25), 0.34, 0.26, "hide")
    head = ellipsoid("_head", (0.36, 0.55, 0.38), (0, -1.0, 2.45), "hide", segs=12, rings=8, rot=(-15, 0, 0))
    snout = ellipsoid("_snout", (0.28, 0.35, 0.26), (0, -1.45, 2.3), "belly", segs=10, rings=6)
    nostrils = [ellipsoid("_nos", (0.05, 0.03, 0.04), (0.1 * s, -1.78, 2.35), "nose", segs=5, rings=3) for s in (1, -1)]
    mane = [ellipsoid("_mane", (0.06, 0.28, 0.2), (0, -0.55 + i * 0.22, 2.75 - i * 0.28), "fin" if i % 2 else "fin2",
                      segs=6, rings=4, rot=(-35, 0, 0)) for i in range(4)]
    ears = [ellipsoid("_earfin", (0.05, 0.14, 0.26), (0.25 * s, -0.85, 2.8), "fin2", segs=6, rings=4, rot=(20, -25 * s, 0))
            for s in (1, -1)]
    head = join_as("Head", [neck, head, snout] + nostrils + mane + ears + eye_pair(0.28, -1.15, 2.6, 0.13))
    pivot(head, (0, -0.4, 1.6))

    leg = limb("_leg", (0.3, -0.45, 1.1), (0.35, -0.65, 0.5), 0.13, 0.1, "hide2")
    fin = ellipsoid("_legfin", (0.2, 0.28, 0.06), (0.37, -0.75, 0.42), "fin", segs=8, rings=4, rot=(30, 0, 0))
    legL = join_as("LegFL", [leg, fin])
    pivot(legL, (0.3, -0.45, 1.1))
    mirror_x(legL, "LegFR")

    pts = [(0, 0.55, 1.15), (0, 1.1, 0.85), (0, 1.6, 0.8), (0, 1.95, 1.05), (0, 2.1, 1.45)]
    rs = [0.42, 0.33, 0.25, 0.18, 0.12]
    for i in range(4):
        seg = limb("_t", pts[i], pts[i + 1], rs[i], rs[i + 1], "hide2" if i % 2 else "hide")
        parts = [seg, ellipsoid("_ridge", (0.05, 0.2, 0.12), ((pts[i][0] + pts[i + 1][0]) / 2,
                 (pts[i][1] + pts[i + 1][1]) / 2, (pts[i][2] + pts[i + 1][2]) / 2 + rs[i] * 0.9), "fin", segs=6, rings=3)]
        if i == 3:
            parts += [ellipsoid("_fluke", (0.12, 0.3, 0.42), (0.18 * s, 2.15, 1.75), "fin", segs=8, rings=5,
                                rot=(-20, 25 * s, 0)) for s in (1, -1)]
        t = join_as("Tail%d" % (i + 1), parts)
        pivot(t, pts[i])
    return K.finish("Hippocampus")


def kraken_hatchling():
    K.new_scene("KrakenHatchling")
    K.palette({**EYES, "skin": "#9b5de5", "skin2": "#7a3fc4", "spot": "#c89bff", "sucker": "#ffd0f0",
               "mouth": "#3a1650", "blush": "#ff8fc8"})
    mantle = ellipsoid("_mantle", (0.95, 0.9, 1.05), (0, 0, 1.55), "skin", segs=14, rings=9)
    tip = ellipsoid("_tip", (0.6, 0.55, 0.45), (0, 0.15, 2.5), "skin2", segs=10, rings=6)
    spots = [ellipsoid("_spot", (0.14, 0.1, 0.12), (x, y, z), "spot", segs=6, rings=4)
             for x, y, z in ((0.55, 0.45, 2.1), (-0.6, 0.3, 1.9), (0.2, 0.75, 1.75), (-0.25, 0.6, 2.45), (0.7, -0.1, 2.2))]
    blush = [ellipsoid("_blush", (0.14, 0.05, 0.08), (0.5 * s, -0.8, 1.3), "blush", segs=6, rings=3) for s in (1, -1)]
    mouth = ellipsoid("_mouth", (0.12, 0.05, 0.08), (0, -0.88, 1.2), "mouth", segs=6, rings=4)
    body = join_as("Body", [mantle, tip, mouth] + spots + blush + eye_pair(0.36, -0.78, 1.6, 0.24))
    pivot(body, (0, 0, 1.3))

    n = 6
    for t in range(n):
        a = (t + 0.5) * 2 * math.pi / n
        out = (math.cos(a), math.sin(a))
        p = [(0.55 * out[0], 0.55 * out[1], 0.75),
             (1.0 * out[0], 1.0 * out[1], 0.35),
             (1.45 * out[0], 1.45 * out[1], 0.2),
             (1.75 * out[0], 1.75 * out[1], 0.45)]
        r = [0.26, 0.19, 0.13, 0.05]
        for k in range(3):
            seg = limb("_s", p[k], p[k + 1], r[k], r[k + 1], "skin" if k % 2 == 0 else "skin2")
            mid = [(p[k][i] + p[k + 1][i]) / 2 for i in range(3)]
            suck = ellipsoid("_suck", (r[k] * 0.5, r[k] * 0.5, 0.04), (mid[0], mid[1], mid[2] - r[k] * 0.85), "sucker",
                             segs=6, rings=3)
            ob = join_as("Tentacle%d_%d" % (t + 1, k + 1), [seg, suck])
            pivot(ob, p[k])
    return K.finish("KrakenHatchling")


ALL = {"SeaTurtlePup": sea_turtle_pup, "Kappa": kappa, "Hippocampus": hippocampus, "KrakenHatchling": kraken_hatchling}

if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else list(ALL)
    for n in args:
        ALL[n]()
