p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\WraithHound.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a[:70], s.count(a))
    s = s.replace(a, b)


i0 = s.index("def column(")
i1 = s.index("def model(k):")
s = s[:i0] + '''def wisp(B, root, d0, d1, L0, L1, w, d, bone, side=(1, 0, 0), tipfrac=0.42):
    """one smoke wisp of the mane: a fat rounded root rising steeply (d0, L0), bending back into a long tapering
    tail (d1, L1) that ends in an indigo point. Returns the tip."""
    root = Vector(root)
    m = root + Vector(d0).normalized() * L0
    q = m + Vector(d1).normalized() * L1
    j = m + (q - m) * (1 - tipfrac)
    B.seg(root, m, w, d, SOOT, bone, side=side, top=(0.70, 0.70), ext=0.04, ext1=0.0, rnd=0.42)
    B.seg(m, j, w * 0.70, d * 0.70, SOOT, bone, side=side, top=(0.62, 0.62), ext=0.035, ext1=0.0, rnd=0.42)
    B.seg(j, q, w * 0.70 * 0.62, d * 0.70 * 0.62, INDIGO, bone, side=side, top=(0.10, 0.22), ext=0.01,
          studs=[], nostud=True, rnd=0.35)
    return q


def mane_row(B, bone, root, sc):
    """one mane row: a tall centre wisp (bone) + two side wisps splayed out (bone_L / bone_R, for the fan-out)"""
    out = {"C": wisp(B, root, (0, 0.28, 1.0), (0, 1.0, 0.50), 0.22 * sc, 0.21 * sc, 0.068 * sc, 0.085 * sc, bone)}
    for s_, sd in ((1, "L"), (-1, "R")):
        r = root + Vector((s_ * 0.052, 0.035, -0.020))
        out[sd] = wisp(B, r, (s_ * 0.40, 0.38, 1.0), (s_ * 0.30, 1.0, 0.30), 0.16 * sc, 0.17 * sc, 0.055 * sc,
                       0.070 * sc, bone + "_" + sd)
    return out


''' + s[i1:]
rep('''MANE = [("Mane1", "Neck", Vector((0, -0.64, 0.995)), 0.95),
        ("Mane2", "Chest", Vector((0, -0.40, 0.915)), 1.20),
        ("Mane3", "Spine", Vector((0, -0.13, 0.885)), 0.95)]''',
    '''MANE = [("Mane1", "Neck", Vector((0, -0.635, 0.985)), 0.95),
        ("Mane2", "Chest", Vector((0, -0.40, 0.905)), 1.22),
        ("Mane3", "Spine", Vector((0, -0.13, 0.875)), 0.95)]''')
# saddle a little shallower (the mane adds soot)
rep('''    upper(B, rib, 0.035, SOOT, ky=0.80, cy=0.05)
    upper(B, waist, -0.015, SOOT)
    upper(B, hips, 0.010, SOOT, ky=0.92, cy=-0.01)''', '''    upper(B, rib, 0.060, SOOT, ky=0.80, cy=0.05)
    upper(B, waist, 0.000, SOOT)
    upper(B, hips, 0.030, SOOT, ky=0.92, cy=-0.01)''')
# mist belly: the lower layer of the chest (follows its own taper) + a wider tuck strip
rep('''    B.add((0, -0.29, 0.478), (0.090, 0.15, 0.022), MIST, "Chest", bot=(0.8, 0.9), studs=[])''',
    '''    lower(B, rib, -0.125, MIST, ky=0.86, cy=0.02)''')
rep('''    B.seg((0, -0.10, 0.500), (0, 0.24, 0.628), 0.090, 0.024, MIST, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)''',
    '''    B.seg((0, -0.10, 0.498), (0, 0.24, 0.626), 0.100, 0.030, MIST, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)''')
rep('''def model(k):''', '''def lower(B, T, lz1, color, p=0.006, ky=1.0, cy=0.0, rnd_t=0.30):
    """the slab of block T below its local z = lz1, grown by p (a colour layer following T's shape: the mist belly)"""
    x0, y0, ox0, oy0 = tdims(T, -T.h.z)
    x1, y1, ox1, oy1 = tdims(T, lz1)
    hz = (lz1 - (-T.h.z - p)) / 2
    hx, hy = x0 + p, y0 * ky + p
    c = Vector((ox0, oy0 + cy, -T.h.z - p + hz))
    mnT = min(T.h.x * min(T.top[0], T.bot[0]), T.h.y * min(T.top[1], T.bot[1]), T.h.z)
    mnS = min(min(hx, x1 + p), min(hy, y1 * ky + p), hz)
    rnd = min(0.45, rnd_t * mnT / mnS)
    return B.add(T.world(c), (hx, hy, hz), color, T.bone, R=T.R, top=((x1 + p) / hx, (y1 * ky + p) / hy),
                 top_shift=(ox1 - ox0, oy1 - oy0), rnd=rnd)


def model(k):''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
