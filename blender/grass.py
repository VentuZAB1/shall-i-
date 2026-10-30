"""Grass area creatures (Wood egg): MossbackTortoise, ForestFawn, TreantSprout, VineSerpent.
Run: blender -b -P grass.py [-- Name]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import creature_kit as K
from creature_kit import box, ellipsoid, cone, mirror_x, join_as, pivot, eye_pair

EYES = {"white": "#ffffff", "pupil": "#1d1a24"}


def mossback_tortoise():
    K.new_scene("MossbackTortoise")
    K.palette({**EYES, "shell": "#5b7d32", "shell2": "#476a28", "rim": "#d8b477", "skin": "#9cc46a",
               "skin2": "#7fae4f", "moss": "#6cc04a", "petal": "#ff8fb8", "petal2": "#fff4d8",
               "yolk": "#ffd23f", "mouth": "#3a2a22", "belly": "#e8cf96"})
    shell = ellipsoid("_shell", (1.25, 1.45, 0.85), (0, 0.1, 0.95), "shell", segs=10, rings=6, smooth=False)
    plates = [ellipsoid("_plate", (0.42, 0.42, 0.14), (x, y, z), "shell2", segs=6, rings=3, smooth=False)
              for x, y, z in ((0, 0.1, 1.78), (0.62, -0.35, 1.45), (-0.62, -0.35, 1.45),
                              (0.62, 0.6, 1.45), (-0.62, 0.6, 1.45))]
    rim = cone("_rim", 1.34, 1.34, 0.22, (0, 0.1, 0.55), "rim", verts=12)
    belly = ellipsoid("_belly", (1.15, 1.35, 0.3), (0, 0.1, 0.6), "belly", segs=10, rings=4)
    moss = [ellipsoid("_moss", (r, r, r * 0.45), (x, y, z), "moss", segs=7, rings=4, smooth=False)
            for x, y, z, r in ((0.15, 0.25, 1.82, 0.5), (-0.35, -0.1, 1.74, 0.4), (0.4, 0.6, 1.62, 0.35))]
    flowers = []
    for x, y, z, col in ((0.2, 0.3, 2.0, "petal"), (-0.4, -0.15, 1.9, "petal2"), (0.5, 0.7, 1.78, "petal")):
        flowers.append(cone("_stem", 0.03, 0.03, 0.2, (x, y, z - 0.12), "moss", verts=4))
        for a in range(5):
            import math
            ang = a * 2 * math.pi / 5
            flowers.append(ellipsoid("_petal", (0.09, 0.09, 0.04),
                                     (x + 0.1 * math.cos(ang), y + 0.1 * math.sin(ang), z + 0.08), col, segs=6, rings=3))
        flowers.append(ellipsoid("_yolk", (0.06, 0.06, 0.05), (x, y, z + 0.1), "yolk", segs=6, rings=3))
    tail = cone("_tail", 0.16, 0.02, 0.45, (0, 1.4, 0.6), "skin", verts=6, rot=(-100, 0, 0))
    body = join_as("Body", [shell, rim, belly, tail] + plates + moss + flowers)
    pivot(body, (0, 0.1, 0.9))

    neck = cone("_neck", 0.3, 0.27, 0.6, (0, -1.05, 0.8), "skin", verts=8, rot=(80, 0, 0), smooth=True)
    head = ellipsoid("_head", (0.5, 0.55, 0.46), (0, -1.75, 1.05), "skin", segs=12, rings=8)
    cheek = ellipsoid("_jaw", (0.46, 0.45, 0.25), (0, -1.8, 0.85), "skin2", segs=10, rings=5)
    mouth = box("_mouth", (0.36, 0.05, 0.05), (0, -2.23, 0.92), "mouth", bevel=0.3)
    head = join_as("Head", [neck, head, cheek, mouth] + eye_pair(0.24, -2.1, 1.2, 0.14))
    pivot(head, (0, -1.0, 0.85))

    for name, x, y in (("LegFL", 0.78, -0.72), ("LegBL", 0.78, 0.9)):
        leg = cone("_leg", 0.3, 0.26, 0.6, (x, y, 0.1), "skin", verts=8, smooth=True)
        foot = ellipsoid("_foot", (0.34, 0.38, 0.16), (x, y - 0.06, 0.12), "skin2", segs=8, rings=4)
        claws = [ellipsoid("_claw", (0.06, 0.07, 0.05), (x + dx, y - 0.4, 0.1), "rim", segs=5, rings=3)
                 for dx in (-0.14, 0, 0.14)]
        left = join_as(name, [leg, foot] + claws)
        pivot(left, (x, y, 0.72))
        mirror_x(left, name[:-1] + "R")
    return K.finish("MossbackTortoise")


def forest_fawn():
    import math
    K.new_scene("ForestFawn")
    K.palette({**EYES, "fur": "#c9844a", "fur2": "#a86a38", "cream": "#f6e2c0", "spot": "#fff6e6",
               "nose": "#2a1f1c", "hoof": "#4a3326", "ear": "#f2a7a0", "antler": "#8a5a36",
               "leaf": "#6fcf4a", "leaf2": "#4fae3a"})
    body = ellipsoid("_body", (0.55, 1.05, 0.55), (0, 0, 1.55), "fur", segs=12, rings=8)
    belly = ellipsoid("_belly", (0.45, 0.85, 0.35), (0, 0, 1.3), "cream", segs=10, rings=6)
    spots = [ellipsoid("_spot", (0.1, 0.12, 0.05), (x, y, 2.07 - abs(x) * 0.5), "spot", segs=6, rings=3,
                       rot=(0, x * 60, 0))
             for x, y in ((0.2, -0.4), (-0.22, -0.1), (0.25, 0.25), (-0.18, 0.5), (0.05, 0.7), (0.0, 0.05))]
    tail = ellipsoid("_tail", (0.14, 0.12, 0.22), (0, 1.05, 1.85), "spot", segs=8, rings=5, rot=(-30, 0, 0))
    body = join_as("Body", [body, belly, tail] + spots)
    pivot(body, (0, 0, 1.55))

    neck = cone("_neck", 0.26, 0.2, 0.8, (0, -0.7, 1.7), "fur", verts=10, rot=(35, 0, 0), smooth=True)
    head = ellipsoid("_head", (0.4, 0.45, 0.4), (0, -1.2, 2.45), "fur", segs=12, rings=8)
    snout = ellipsoid("_snout", (0.26, 0.32, 0.22), (0, -1.55, 2.33), "cream", segs=10, rings=6)
    nose = ellipsoid("_nose", (0.1, 0.07, 0.07), (0, -1.86, 2.4), "nose", segs=8, rings=4)
    ears = []
    for s in (1, -1):
        ears.append(ellipsoid("_ear", (0.13, 0.08, 0.3), (0.42 * s, -1.1, 2.72), "fur", segs=8, rings=5, rot=(0, -50 * s, 0)))
        ears.append(ellipsoid("_earin", (0.08, 0.04, 0.2), (0.43 * s, -1.16, 2.72), "ear", segs=6, rings=4, rot=(0, -50 * s, 0)))
        # leaf-sprout antlers: a twig with two branches and leaves
        bx = 0.17 * s
        ears.append(cone("_ant", 0.05, 0.035, 0.45, (bx, -1.05, 2.78), "antler", verts=6, rot=(0, -15 * s, 0)))
        ears.append(cone("_ant2", 0.035, 0.025, 0.25, (bx + 0.08 * s, -1.05, 3.05), "antler", verts=5, rot=(0, -60 * s, 0)))
        for lx, lz, col in ((bx + 0.3 * s, 3.2, "leaf"), (bx + 0.1 * s, 3.3, "leaf2"), (bx - 0.02 * s, 3.2, "leaf")):
            ears.append(ellipsoid("_leaf", (0.1, 0.05, 0.17), (lx, -1.05, lz), col, segs=6, rings=4, rot=(0, -30 * s, 0)))
    head = join_as("Head", [neck, head, snout, nose] + ears + eye_pair(0.25, -1.48, 2.55, 0.14, look=0.2))
    pivot(head, (0, -0.65, 1.75))

    for name, x, y in (("LegFL", 0.28, -0.6), ("LegBL", 0.28, 0.62)):
        upper = cone("_leg", 0.14, 0.1, 1.15, (x, y, 0.2), "fur2", verts=8, smooth=True)
        hoof = box("_hoof", (0.2, 0.22, 0.2), (x, y - 0.02, 0.1), "hoof", bevel=0.25)
        leg = join_as(name, [upper, hoof])
        pivot(leg, (x, y, 1.4))
        mirror_x(leg, name[:-1] + "R")
    return K.finish("ForestFawn")


def treant_sprout():
    import math
    K.new_scene("TreantSprout")
    K.palette({**EYES, "bark": "#7a5230", "bark2": "#5e3d22", "wood": "#e0b680", "ring": "#b98a55",
               "leaf": "#5fbf45", "leaf2": "#43a236", "leaf3": "#8ada5a", "mouth": "#2b1b12",
               "moss": "#7ccf52", "berry": "#ff5d5d"})
    trunk = cone("_trunk", 0.72, 0.6, 1.5, (0, 0, 0.55), "bark", verts=9)
    top = cone("_top", 0.58, 0.58, 0.06, (0, 0, 2.05), "wood", verts=9)
    ring = cone("_ring", 0.35, 0.35, 0.07, (0, 0, 2.06), "ring", verts=9)
    grooves = [box("_groove", (0.08, 0.06, 0.9), (0.66 * math.cos(a), 0.66 * math.sin(a), 1.2), "bark2",
                   bevel=0.3, rot=(0, 0, math.degrees(a)))
               for a in (0.3, 1.2, 2.1, 3.0, 3.8, 5.8)]
    mouth = ellipsoid("_mouth", (0.18, 0.06, 0.1), (0, -0.66, 1.05), "mouth", segs=8, rings=4)
    moss = ellipsoid("_moss", (0.28, 0.3, 0.12), (0.62, 0.25, 0.8), "moss", segs=7, rings=4, smooth=False,
                     rot=(0, 70, 0))
    body = join_as("Body", [trunk, top, ring, mouth, moss] + grooves + eye_pair(0.24, -0.62, 1.45, 0.17))
    pivot(body, (0, 0, 0.6))

    crown = []
    for x, y, z, r, col in ((0, 0, 2.55, 0.62, "leaf"), (0.45, 0.1, 2.35, 0.45, "leaf2"), (-0.45, 0.15, 2.4, 0.48, "leaf2"),
                            (0.1, 0.35, 2.85, 0.42, "leaf3"), (-0.2, -0.3, 2.3, 0.38, "leaf3")):
        crown.append(ellipsoid("_crown", (r, r, r * 0.85), (x, y, z), col, segs=8, rings=5, smooth=False))
    for x, y, z in ((0.3, -0.45, 2.55), (-0.35, -0.3, 2.75), (0.55, 0.2, 2.7)):
        crown.append(ellipsoid("_berry", (0.08, 0.08, 0.08), (x, y, z), "berry", segs=6, rings=4))
    head = join_as("Head", crown)
    pivot(head, (0, 0, 2.08))

    arm = cone("_arm", 0.14, 0.07, 0.85, (0.62, 0, 1.55), "bark", verts=6, rot=(0, 115, 0))
    twig = cone("_twig", 0.05, 0.02, 0.3, (1.15, 0, 1.25), "bark", verts=5, rot=(0, 160, 0))
    leaf = ellipsoid("_leaf", (0.15, 0.08, 0.22), (1.38, 0, 1.18), "leaf", segs=6, rings=4, rot=(0, 40, 0))
    armL = join_as("ArmL", [arm, twig, leaf])
    pivot(armL, (0.6, 0, 1.6))
    mirror_x(armL, "ArmR")

    leg = cone("_leg", 0.26, 0.22, 0.55, (0.32, 0, 0.1), "bark2", verts=7)
    toes = [cone("_toe", 0.09, 0.02, 0.45, (0.32, 0, 0.12), "bark2", verts=5, rot=(-95, 0, a))
            for a in (-40, 0, 40)]
    legL = join_as("LegL", [leg] + toes)
    pivot(legL, (0.32, 0, 0.62))
    mirror_x(legL, "LegR")
    return K.finish("TreantSprout")


def vine_serpent():
    import math
    K.new_scene("VineSerpent")
    K.palette({**EYES, "scale": "#3f9e4d", "scale2": "#2f7f3c", "belly": "#d9ec8a", "leaf": "#7fd84f",
               "petal": "#ff7eb0", "yolk": "#ffd23f", "tongue": "#e0405a", "mouth": "#3b1e22"})
    head = ellipsoid("_head", (0.5, 0.62, 0.36), (0, -2.35, 0.6), "scale", segs=12, rings=8)
    brow = ellipsoid("_brow", (0.44, 0.35, 0.22), (0, -2.15, 0.82), "scale2", segs=10, rings=5)
    petals = []
    for a in range(6):
        ang = a * math.pi / 3
        petals.append(ellipsoid("_petal", (0.16, 0.16, 0.05),
                                (0.22 * math.cos(ang), -2.05 + 0.22 * math.sin(ang), 1.02), "petal", segs=7, rings=3))
    petals.append(ellipsoid("_yolk", (0.11, 0.11, 0.07), (0, -2.05, 1.05), "yolk", segs=7, rings=4))
    head = join_as("Head", [head, brow] + petals + eye_pair(0.26, -2.62, 0.78, 0.14))
    pivot(head, (0, -1.85, 0.5))

    jaw = ellipsoid("_jaw", (0.44, 0.55, 0.16), (0, -2.35, 0.34), "belly", segs=10, rings=5)
    tongue = box("_tongue", (0.08, 0.4, 0.03), (0, -2.95, 0.36), "tongue", bevel=0.3)
    jaw = join_as("Jaw", [jaw, tongue])
    pivot(jaw, (0, -1.95, 0.42))

    def seg(name, y, r, leaf=True):
        top = ellipsoid("_seg", (r, 0.42, r * 0.8), (0, y, r * 0.8 + 0.02), "scale", segs=10, rings=6)
        bel = ellipsoid("_bel", (r * 0.85, 0.36, r * 0.45), (0, y - 0.02, r * 0.5), "belly", segs=8, rings=4)
        parts = [top, bel]
        if leaf:
            parts.append(ellipsoid("_leaf", (0.09, 0.2, 0.14), (0, y + 0.05, r * 1.6 + 0.08), "leaf",
                                   segs=6, rings=4, rot=(-25, 0, 0)))
        ob = join_as(name, parts)
        pivot(ob, (0, y - 0.3, r * 0.8))
        return ob

    seg("Body", -1.55, 0.44)
    y = -1.55
    for i in range(1, 8):
        y += 0.55
        r = 0.44 * (1 - i * 0.085)
        ob = seg("Seg%d" % i, y, r, leaf=(i % 2 == 1))
        if i == 7:
            tip = cone("_tip", r * 0.8, 0.02, 0.6, (0, y + 0.3, r * 0.8), "scale2", verts=8, rot=(-90, 0, 0))
            join_as("Seg7", [ob, tip])
    return K.finish("VineSerpent")


ALL = {"MossbackTortoise": mossback_tortoise, "ForestFawn": forest_fawn,
       "TreantSprout": treant_sprout, "VineSerpent": vine_serpent}

if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else list(ALL)
    for n in args:
        ALL[n]()
