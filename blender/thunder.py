"""Thunder area creatures (Storm egg): SparkFox, Raiju, CloudRam, ThunderBull, Thunderbird, StormWyvern.
Run: blender -b -P thunder.py [-- Name]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import creature_kit as K
from creature_kit import box, ellipsoid, cone, limb, mirror_x, join_as, pivot, eye_pair

EYES = {"white": "#ffffff", "pupil": "#1d1a24"}


def legs4(xs, yf, yb, top, r, color, foot, foot_color, foot_size=None):
    """Four straight legs, left ones built and mirrored. Pivots at the hips/shoulders."""
    fs = foot_size or (r * 1.3, r * 1.5, r * 0.8)
    for name, y in (("LegFL", yf), ("LegBL", yb)):
        leg = limb("_leg", (xs, y, top), (xs, y, fs[2]), r, r * 0.8, color)
        f = ellipsoid("_foot", fs, (xs, y - r * 0.3, fs[2] * 0.9), foot_color, segs=8, rings=4) if foot == "paw" \
            else box("_hoof", (fs[0] * 1.6, fs[1] * 1.4, fs[2] * 1.6), (xs, y, fs[2] * 0.8), foot_color, bevel=0.25)
        ob = join_as(name, [leg, f])
        pivot(ob, (xs, y, top))
        mirror_x(ob, name[:-1] + "R")


def bolt(name, p, scale, color, rot=(0, 0, 0), thick=0.06):
    """Flat lightning-bolt made of three slanted boxes (in the XZ plane before rot)."""
    import bmesh
    from mathutils import Vector
    s = scale
    outline = [(0.12, 0.62), (-0.24, 0.02), (-0.02, 0.02), (-0.16, -0.62), (0.26, 0.1), (0.04, 0.1)]
    bm = bmesh.new()
    front = [bm.verts.new((x * s, -thick / 2, z * s)) for x, z in outline]
    face = bm.faces.new(front)
    ext = bmesh.ops.extrude_face_region(bm, geom=[face])
    bmesh.ops.translate(bm, vec=Vector((0, thick, 0)), verts=[v for v in ext["geom"] if isinstance(v, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    return [K._finish(bm, name, color, p, rot, smooth=False)]


def spark_fox():
    K.new_scene("SparkFox")
    K.palette({**EYES, "fur": "#ffc928", "fur2": "#f0a818", "cream": "#fff6dc", "dark": "#3a2a1a",
               "nose": "#241a14", "earin": "#ff9a5c", "zap": "#fff27a"})
    body = ellipsoid("_body", (0.5, 0.85, 0.5), (0, 0, 1.15), "fur", segs=12, rings=8)
    chest = ellipsoid("_chest", (0.38, 0.4, 0.42), (0, -0.55, 1.1), "cream", segs=10, rings=6)
    body = join_as("Body", [body, chest])
    pivot(body, (0, 0, 1.15))

    head = ellipsoid("_head", (0.52, 0.45, 0.45), (0, -0.95, 1.75), "fur", segs=12, rings=8)
    cheeks = [ellipsoid("_cheek", (0.22, 0.2, 0.18), (0.32 * s, -1.1, 1.58), "cream", segs=8, rings=5) for s in (1, -1)]
    snout = ellipsoid("_snout", (0.2, 0.3, 0.17), (0, -1.35, 1.62), "cream", segs=10, rings=6)
    nose = ellipsoid("_nose", (0.08, 0.06, 0.06), (0, -1.64, 1.68), "nose", segs=6, rings=4)
    ears = []
    for s in (1, -1):
        ears.append(cone("_ear", 0.22, 0.02, 0.6, (0.28 * s, -0.9, 2.05), "fur", verts=4, rot=(0, -18 * s, 0)))
        ears.append(cone("_earin", 0.12, 0.01, 0.4, (0.27 * s, -0.99, 2.08), "earin", verts=4, rot=(0, -18 * s, 0)))
    head = join_as("Head", [head, snout, nose] + cheeks + ears + eye_pair(0.24, -1.3, 1.85, 0.15, look=0.15))
    pivot(head, (0, -0.6, 1.4))

    legs4(0.28, -0.5, 0.5, 1.0, 0.12, "fur2", "paw", "cream")

    # zigzag lightning tail
    pts = [(0, 0.75, 1.3), (0.1, 1.2, 1.75), (-0.15, 1.45, 2.2), (0.12, 1.7, 2.75)]
    rs = [0.16, 0.22, 0.26, 0.05]
    for i in range(3):
        parts = [limb("_t", pts[i], pts[i + 1], rs[i], rs[i + 1], "fur" if i < 2 else "cream", verts=6, smooth=False)]
        t = join_as("Tail%d" % (i + 1), parts)
        pivot(t, pts[i])
    return K.finish("SparkFox")


def raiju():
    K.new_scene("Raiju")
    K.palette({**EYES, "pupil": "#10306a", "fur": "#e6f3ff", "fur2": "#c7ddf5", "stripe": "#3d7dff",
               "bolt": "#ffe04a", "nose": "#1c2a44", "paw": "#9fbde0", "mouth": "#1c2a44"})
    body = ellipsoid("_body", (0.55, 1.0, 0.55), (0, 0, 1.3), "fur", segs=12, rings=8)
    stripes = [ellipsoid("_stripe", (0.56 * k, 0.09, 0.56 * k), (0, y, 1.3), "stripe", segs=12, rings=8)
               for y, k in ((-0.25, 0.97), (0.15, 0.99), (0.5, 0.9))]
    mane = []
    for i, y in enumerate((-0.75, -0.45, -0.15, 0.15, 0.45)):
        mane += bolt("_mane", (0, y, 1.95 - i * 0.05), 0.55 - i * 0.05, "bolt", rot=(0, 0, 90))
    body = join_as("Body", [body] + stripes + mane)
    pivot(body, (0, 0, 1.3))

    head = ellipsoid("_head", (0.5, 0.5, 0.45), (0, -1.1, 1.85), "fur", segs=12, rings=8)
    snout = ellipsoid("_snout", (0.24, 0.35, 0.2), (0, -1.5, 1.72), "fur2", segs=10, rings=6)
    nose = ellipsoid("_nose", (0.09, 0.06, 0.07), (0, -1.84, 1.8), "nose", segs=6, rings=4)
    marks = [box("_mark", (0.05, 0.25, 0.08), (0.2 * s, -1.25, 2.2), "stripe", bevel=0.3, rot=(0, 0, 25 * s)) for s in (1, -1)]
    ears = []
    for s in (1, -1):
        ears.append(cone("_ear", 0.2, 0.02, 0.5, (0.3 * s, -1.0, 2.15), "fur", verts=4, rot=(0, -25 * s, 0)))
        ears += bolt("_earbolt", (0.5 * s, -1.0, 2.55), 0.35, "bolt", rot=(0, -20 * s, 0))
    head = join_as("Head", [head, snout, nose] + marks + ears + eye_pair(0.24, -1.45, 1.95, 0.14))
    pivot(head, (0, -0.75, 1.55))

    legs4(0.3, -0.62, 0.6, 1.1, 0.13, "fur2", "paw", "paw")

    pts = [(0, 0.95, 1.45), (0, 1.4, 1.9), (0, 1.55, 2.5)]
    t1 = join_as("Tail1", [limb("_t", pts[0], pts[1], 0.14, 0.12, "fur")])
    pivot(t1, pts[0])
    t2 = join_as("Tail2", bolt("_tb", (0, 1.5, 2.3), 0.9, "bolt", rot=(0, 0, 90), thick=0.12))
    pivot(t2, pts[1])
    return K.finish("Raiju")


def cloud_ram():
    K.new_scene("CloudRam")
    K.palette({**EYES, "wool": "#f7f9ff", "wool2": "#dfe6f5", "face": "#5b6a8e", "face2": "#7b8ab0",
               "horn": "#f2c14e", "horn2": "#d49a2a", "hoof": "#2d3550", "zap": "#ffe04a"})
    puffs = []
    for x, y, z, r in ((0, 0, 1.45, 0.7), (0.4, -0.4, 1.35, 0.5), (-0.4, -0.4, 1.35, 0.5), (0.4, 0.45, 1.35, 0.5),
                       (-0.4, 0.45, 1.35, 0.5), (0, -0.55, 1.75, 0.45), (0, 0.55, 1.75, 0.45), (0.3, 0, 1.95, 0.45),
                       (-0.3, 0, 1.95, 0.45), (0, 0.9, 1.4, 0.35)):
        puffs.append(ellipsoid("_puff", (r, r, r * 0.9), (x, y, z), "wool" if r > 0.4 else "wool2", segs=8, rings=6))
    zaps = bolt("_zap", (0.62, 0.1, 1.5), 0.45, "zap", rot=(0, 0, 90)) + bolt("_zap", (-0.62, 0.1, 1.5), 0.45, "zap", rot=(0, 0, 90))
    body = join_as("Body", puffs + zaps)
    pivot(body, (0, 0, 1.4))

    head = ellipsoid("_head", (0.36, 0.45, 0.4), (0, -1.0, 1.75), "face", segs=12, rings=8)
    muzzle = ellipsoid("_muzzle", (0.26, 0.25, 0.22), (0, -1.35, 1.6), "face2", segs=10, rings=6)
    tuft = [ellipsoid("_tuft", (0.2, 0.2, 0.16), (x, -0.95, 2.15), "wool", segs=8, rings=5) for x in (-0.15, 0.15, 0)]
    horns = []
    for s in (1, -1):
        for i in range(9):
            a = i * 0.75
            rad = 0.35 - i * 0.02
            horns.append(ellipsoid("_horn", (0.14 - i * 0.008,) * 3,
                                   (s * (0.35 + 0.1 * i / 8 + rad * 0.3), -0.85 + rad * math.sin(a), 1.95 - rad + rad * math.cos(a)),
                                   "horn" if i % 2 == 0 else "horn2", segs=6, rings=4))
    ears = [ellipsoid("_ear", (0.22, 0.08, 0.1), (0.42 * s, -0.95, 1.8), "face", segs=8, rings=4, rot=(0, 20 * s, 0)) for s in (1, -1)]
    head = join_as("Head", [head, muzzle] + tuft + horns + ears + eye_pair(0.2, -1.33, 1.85, 0.12))
    pivot(head, (0, -0.65, 1.6))

    legs4(0.3, -0.45, 0.5, 1.0, 0.12, "face", "hoof", "hoof", foot_size=(0.12, 0.12, 0.12))
    return K.finish("CloudRam")


def thunder_bull():
    K.new_scene("ThunderBull")
    K.palette({**EYES, "hide": "#3d4659", "hide2": "#2d3445", "muzzle": "#7c879e", "bolt": "#ffd21f",
               "horn": "#f3e7c9", "horn2": "#cdbb92", "ring": "#f2b632", "hoof": "#1a1e28", "brow": "#1a1e28"})
    body = box("_body", (1.4, 2.0, 1.2), (0, 0, 1.55), "hide", bevel=0.3, segs=2)
    hump = box("_hump", (1.3, 0.9, 0.5), (0, -0.5, 2.25), "hide2", bevel=0.35, segs=2)
    bolts = []
    for s in (1, -1):
        bolts += bolt("_bolt", (0.71 * s, 0, 1.6), 0.85, "bolt", rot=(0, 0, 90))
    tail = limb("_tail", (0, 1.0, 1.9), (0, 1.25, 1.1), 0.06, 0.04, "hide2", verts=5)
    tuft = ellipsoid("_tuft", (0.12, 0.12, 0.2), (0, 1.27, 1.0), "bolt", segs=6, rings=4)
    body = join_as("Body", [body, hump, tail, tuft] + bolts)
    pivot(body, (0, 0, 1.55))

    head = box("_head", (0.85, 0.75, 0.8), (0, -1.3, 1.8), "hide", bevel=0.3, segs=2)
    muzzle = box("_muzzle", (0.75, 0.4, 0.45), (0, -1.75, 1.55), "muzzle", bevel=0.35, segs=2)
    nostr = [ellipsoid("_nos", (0.07, 0.03, 0.05), (0.17 * s, -1.96, 1.6), "hoof", segs=6, rings=3) for s in (1, -1)]
    ring = cone("_ring", 0.16, 0.16, 0.04, (0, -2.0, 1.42), "ring", verts=10, rot=(90, 0, 0))
    brows = [box("_brow", (0.26, 0.06, 0.07), (0.2 * s, -1.69, 2.1), "brow", bevel=0.3, rot=(0, -15 * s, 0)) for s in (1, -1)]
    horns = []
    for s in (1, -1):
        horns.append(limb("_horn", (0.4 * s, -1.25, 2.05), (0.8 * s, -1.3, 2.2), 0.13, 0.1, "horn2", verts=7))
        horns.append(limb("_horn", (0.8 * s, -1.3, 2.2), (0.95 * s, -1.4, 2.6), 0.1, 0.02, "horn", verts=7))
    ears = [ellipsoid("_ear", (0.2, 0.07, 0.1), (0.5 * s, -1.1, 1.95), "hide2", segs=8, rings=4) for s in (1, -1)]
    head = join_as("Head", [head, muzzle, ring] + nostr + brows + horns + ears + eye_pair(0.24, -1.69, 1.95, 0.12))
    pivot(head, (0, -0.95, 1.8))

    legs4(0.45, -0.65, 0.65, 1.1, 0.2, "hide2", "hoof", "hoof", foot_size=(0.16, 0.16, 0.15))
    return K.finish("ThunderBull")


def wing(side_name, root, span, chord, colors, s=1):
    """Two-part bird/wyvern wing spread along X. Returns (inner, tip) joined objects."""
    x0, y0, z0 = root
    inner_parts = [box("_w", (span * 0.5, chord, 0.08), (x0 + s * span * 0.25, y0, z0), colors[0], bevel=0.3)]
    tip_parts = [box("_w", (span * 0.5, chord * 0.85, 0.07), (x0 + s * span * 0.75, y0 + chord * 0.05, z0), colors[0], bevel=0.3)]
    for i in range(3):
        fx = x0 + s * span * (0.12 + 0.16 * i)
        inner_parts.append(ellipsoid("_f", (0.11, chord * 0.45, 0.05), (fx, y0 + chord * 0.55, z0 - 0.01), colors[1], segs=6, rings=3))
    for i in range(4):
        fx = x0 + s * span * (0.58 + 0.13 * i)
        tip_parts.append(ellipsoid("_f", (0.1, chord * 0.5, 0.045), (fx, y0 + chord * 0.55, z0 - 0.01), colors[1], segs=6, rings=3))
    tip_parts.append(ellipsoid("_f", (span * 0.12, chord * 0.3, 0.05), (x0 + s * span * 1.02, y0 + chord * 0.1, z0), colors[1], segs=6, rings=3))
    inner = join_as(side_name, inner_parts)
    pivot(inner, root)
    tip = join_as(side_name + "2", tip_parts)
    pivot(tip, (x0 + s * span * 0.5, y0, z0))
    return inner, tip


def thunderbird():
    K.new_scene("Thunderbird")
    K.palette({**EYES, "feather": "#2d3f86", "feather2": "#1f2d66", "belly": "#9fd0ff", "gold": "#ffd23f",
               "beak": "#ffb42a", "talon": "#ffcf5a", "edge": "#ffe98a"})
    body = ellipsoid("_body", (0.6, 0.85, 0.65), (0, 0, 1.6), "feather", segs=12, rings=8, rot=(-15, 0, 0))
    belly = ellipsoid("_belly", (0.45, 0.55, 0.5), (0, -0.3, 1.45), "belly", segs=10, rings=6)
    chevrons = [box("_chev", (0.5, 0.05, 0.07), (0, -0.78, 1.55 - i * 0.2), "gold", bevel=0.3) for i in range(2)]
    tail = [ellipsoid("_tailf", (0.14, 0.55, 0.05), (x, 1.05, 1.35), c, segs=6, rings=3, rot=(15, 0, x * 40))
            for x, c in ((-0.22, "feather2"), (0, "gold"), (0.22, "feather2"))]
    body = join_as("Body", [body, belly] + chevrons + tail)
    pivot(body, (0, 0, 1.6))

    head = ellipsoid("_head", (0.42, 0.45, 0.42), (0, -0.85, 2.3), "feather", segs=12, rings=8)
    beak = cone("_beak", 0.16, 0.02, 0.4, (0, -1.2, 2.25), "beak", verts=8, rot=(100, 0, 0))
    crest = [cone("_crest", 0.07, 0.01, 0.45, (0, -0.75 + i * 0.15, 2.65), "gold", verts=4, rot=(-40 - i * 15, 0, 0)) for i in range(3)]
    head = join_as("Head", [head, beak] + crest + eye_pair(0.22, -1.12, 2.42, 0.12))
    pivot(head, (0, -0.55, 2.0))

    for s, n in ((1, "WingL"), (-1, "WingR")):
        wing(n, (0.5 * s, -0.1, 1.85), 2.2, 0.8, ("feather", "edge"), s)

    for s, n in ((1, "LegL"), (-1, "LegR")):
        leg = limb("_leg", (0.25 * s, 0.05, 1.1), (0.25 * s, 0.0, 0.15), 0.09, 0.07, "talon", verts=6)
        toes = [limb("_toe", (0.25 * s, 0.0, 0.1), (0.25 * s + dx, -0.3, 0.05), 0.05, 0.02, "talon", verts=5) for dx in (-0.12, 0, 0.12)]
        ob = join_as(n, [leg] + toes)
        pivot(ob, (0.25 * s, 0.05, 1.1))
    return K.finish("Thunderbird")


def storm_wyvern():
    K.new_scene("StormWyvern")
    K.palette({**EYES, "pupil": "#2a1450", "scale": "#3f3f9c", "scale2": "#2c2c78", "belly": "#ffd96a",
               "horn": "#f3e7c9", "memb": "#7d6cf0", "memb2": "#a79aff", "bolt": "#ffe04a", "claw": "#f3e7c9"})
    body = ellipsoid("_body", (0.6, 1.0, 0.6), (0, 0, 1.55), "scale", segs=12, rings=8)
    belly = ellipsoid("_belly", (0.45, 0.8, 0.4), (0, -0.05, 1.3), "belly", segs=10, rings=6)
    spikes = [cone("_spk", 0.1, 0.01, 0.3, (0, y, 2.1 - abs(y) * 0.1), "horn", verts=4) for y in (-0.5, -0.1, 0.3)]
    body = join_as("Body", [body, belly] + spikes)
    pivot(body, (0, 0, 1.55))

    neck = limb("_neck", (0, -0.7, 1.8), (0, -1.05, 2.4), 0.3, 0.25, "scale")
    head = ellipsoid("_head", (0.42, 0.55, 0.38), (0, -1.3, 2.55), "scale", segs=12, rings=8)
    snout = ellipsoid("_snout", (0.3, 0.35, 0.22), (0, -1.7, 2.45), "scale2", segs=10, rings=6)
    jawb = ellipsoid("_jawb", (0.28, 0.35, 0.12), (0, -1.65, 2.3), "belly", segs=8, rings=4)
    horns = []
    for s in (1, -1):
        horns.append(limb("_horn", (0.22 * s, -1.15, 2.8), (0.35 * s, -0.8, 3.2), 0.09, 0.01, "horn", verts=6))
        horns.append(limb("_horn2", (0.3 * s, -1.2, 2.65), (0.55 * s, -0.95, 2.85), 0.06, 0.01, "horn", verts=5))
    nos = [ellipsoid("_nos", (0.05, 0.03, 0.04), (0.1 * s, -2.02, 2.5), "scale2", segs=5, rings=3) for s in (1, -1)]
    head = join_as("Head", [neck, head, snout, jawb] + horns + nos + eye_pair(0.25, -1.62, 2.7, 0.13, look=0.2))
    pivot(head, (0, -0.65, 1.8))

    for s, n in ((1, "WingL"), (-1, "WingR")):
        root = (0.45 * s, -0.2, 1.95)
        elbow = (1.4 * s, 0.0, 2.35)
        tipp = (2.6 * s, 0.25, 2.2)
        inner = [limb("_bone", root, elbow, 0.1, 0.08, "scale2", verts=6),
                 box("_memb", (1.0, 1.0, 0.05), (0.95 * s, 0.35, 2.05), "memb", bevel=0.2, rot=(0, -18 * s, 0))]
        tipparts = [limb("_bone", elbow, tipp, 0.08, 0.03, "scale2", verts=6),
                    box("_memb", (1.2, 0.9, 0.05), (1.95 * s, 0.55, 2.2), "memb2", bevel=0.25, rot=(0, 5 * s, -10 * s)),
                    cone("_claw", 0.06, 0.01, 0.2, elbow, "claw", verts=4, rot=(0, 0, 0))]
        a = join_as(n, inner)
        pivot(a, root)
        b = join_as(n + "2", tipparts)
        pivot(b, elbow)

    for s, n in ((1, "LegL"), (-1, "LegR")):
        thigh = ellipsoid("_thigh", (0.25, 0.35, 0.4), (0.4 * s, 0.35, 1.2), "scale", segs=8, rings=6)
        shin = limb("_shin", (0.42 * s, 0.4, 0.95), (0.42 * s, 0.25, 0.15), 0.13, 0.1, "scale2", verts=7)
        claws = [limb("_claw", (0.42 * s, 0.2, 0.1), (0.42 * s + dx, -0.12, 0.05), 0.05, 0.01, "claw", verts=4) for dx in (-0.12, 0, 0.12)]
        ob = join_as(n, [thigh, shin] + claws)
        pivot(ob, (0.4 * s, 0.35, 1.35))

    pts = [(0, 0.85, 1.5), (0, 1.35, 1.3), (0, 1.8, 1.1), (0, 2.2, 0.95), (0, 2.55, 0.9), (0, 2.85, 0.95)]
    rs = [0.3, 0.24, 0.18, 0.13, 0.09, 0.05]
    for i in range(5):
        parts = [limb("_t", pts[i], pts[i + 1], rs[i], rs[i + 1], "scale" if i % 2 == 0 else "scale2", verts=8),
                 cone("_spk", 0.07, 0.01, 0.2, ((pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2,
                      (pts[i][2] + pts[i + 1][2]) / 2 + rs[i] * 0.85), "horn", verts=4)]
        if i == 4:
            parts += bolt("_tipbolt", (0, 3.05, 1.0), 0.8, "bolt", rot=(0, 0, 90), thick=0.1)
        t = join_as("Tail%d" % (i + 1), parts)
        pivot(t, pts[i])
    return K.finish("StormWyvern")


ALL = {"SparkFox": spark_fox, "Raiju": raiju, "CloudRam": cloud_ram, "ThunderBull": thunder_bull,
       "Thunderbird": thunderbird, "StormWyvern": storm_wyvern}

if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else list(ALL)
    for n in args:
        ALL[n]()
