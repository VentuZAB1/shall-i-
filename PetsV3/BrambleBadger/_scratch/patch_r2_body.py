p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\BrambleBadger.py"
s = open(p, encoding="utf-8").read()

# 1) one lofted grey body instead of spine seg + rear block + arch (r2 T2) and a band strip that hugs it (T1)
old_body = '''    B.seg((0, -0.26, 0.415), (0, 0.17, 0.417), 0.222, 0.115, GREY, "Spine", top=(0.95, 0.97), side=(1, 0, 0))
    B.add((0, 0.27, 0.415), (0.212, 0.19, 0.115), GREY, "Spine", top=(0.95, 0.95), rnd=0.50)   # final85 M3
    B.add((0, 0.10, 0.515), (0.165, 0.20, 0.038), GREY, "Spine", top=(0.70, 0.86), rnd=0.5)       # back arch (r2 MM2:
                                                                       # ends buried in the spine + rear blocks)'''
new_body = '''    body_hull(B)                                        # r2 T2: ONE lofted grey body (spine + rear + arch merged)'''
assert old_body in s
s = s.replace(old_body, new_body)

old_band = s[s.index("    for s in (1, -1):                                   # final85 T1: GREY_D flank band"):
             s.index("    # ---------------- neck (mantle) + head")]
new_band = '''    flank_bands(B)                                      # final85 T1 / r2 T1: GREY_D band hugging the hull flank
'''
s = s.replace(old_band, new_band)

# 2) Tubes are built from their rings: the DZ shift must move the rings too
old_dz = '''        if blk.bone in BODYB or blk.bone.startswith("Thorn_"):
            if hasattr(blk, "pts"):'''
new_dz = '''        if blk.bone in BODYB or blk.bone.startswith("Thorn_"):
            if isinstance(blk, bk.Tube):                # the tube mesh is built from rings (Lynx review 1 M1 lesson)
                blk.map(lambda q: q + dz)
                continue
            if hasattr(blk, "pts"):'''
assert old_dz in s
s = s.replace(old_dz, new_dz)

# 3) thorns on the hull top line
old_th = s[s.index("THORNS = ["):s.index("DZ = -0.030")]
new_th = '''THORNS = [(-0.47, 0.515, 0.064, 30), (-0.37, 0.535, 0.072, 34), (-0.26, 0.545, 0.072, 38), (-0.15, None, 0.072, 42),
          (-0.04, None, 0.072, 46), (0.07, None, 0.072, 50), (0.18, None, 0.064, 54), (0.29, None, 0.048, 58),
          (0.39, None, 0.042, 62)]                      # final85 T2 lengths; None = seated on the hull top (r2 T2)
'''
s = s.replace(old_th, new_th)
old_loop = '''    for i, (y, z, L, lean) in enumerate(THORNS):
        bone = "Neck" if y < -0.42 else ("Chest" if y < -0.08 else "Spine")'''
new_loop = '''    for i, (y, z, L, lean) in enumerate(THORNS):
        z = hull_top(y) - 0.006 if z is None else z
        bone = "Neck" if y < -0.42 else ("Chest" if y < -0.08 else "Spine")'''
assert old_loop in s
s = s.replace(old_loop, new_loop)

# 4) helpers before model()
helpers = '''HULL_P = 3.5                     # superellipse exponent of the body cross-section (rounded box, no seams)
HULL_ZB = 0.27                   # hull bottom (buried in the dark skirt)


def hull_top(y):
    """top line of the merged grey body (r2 T2): 0.540 at the shoulders, the old arch height 0.553 over the middle,
    0.535 over the rump, then the rump rounds off (y 0.40-0.465)"""
    def ss(a, b, t):
        u = max(0.0, min(1.0, (t - a) / (b - a)))
        return u * u * (3 - 2 * u)
    return 0.540 + 0.013 * ss(-0.22, -0.05, y) - 0.018 * ss(0.22, 0.40, y)


def hull_hx(y):
    return 0.222 - 0.010 * max(0.0, min(1.0, (y + 0.26) / 0.66))


def hull_x(y, z):
    """flank half-width of the hull at height z (superellipse)"""
    zt = hull_top(y)
    zc, hz = (zt + HULL_ZB) / 2, (zt - HULL_ZB) / 2
    u = min(1.0, abs((z - zc) / hz))
    return hull_hx(y) * (1 - u ** HULL_P) ** (1 / HULL_P)


def body_hull(B):
    """ONE grey body from the shoulders (y -0.25, inside the shoulder blocks) to a rounded rump (y 0.465): a studded
    closed Tube of superellipse rings - replaces the spine seg, the rear block and the back arch (no seams)"""
    rings, n = [], 22
    ys = [-0.25 + 0.025 * i for i in range(27)] + [0.415, 0.43, 0.445, 0.455, 0.462]
    for y in ys:
        zt = hull_top(min(y, 0.40))
        zc, hz, hx = (zt + HULL_ZB) / 2, (zt - HULL_ZB) / 2, hull_hx(min(y, 0.40))
        f = math.sqrt(max(0.0, 1 - ((y - 0.40) / 0.068) ** 2)) if y > 0.40 else 1.0     # round the rump
        ring = []
        for i in range(n):
            a = 2 * math.pi * i / n
            c, sn = math.cos(a), math.sin(a)
            x = hx * f * math.copysign(abs(c) ** (2 / HULL_P), c)
            z = zc + hz * f * math.copysign(abs(sn) ** (2 / HULL_P), sn)
            ring.append(Vector((x, y, z)))
        rings.append(ring)
    B.tube(rings, GREY, "Spine")


def flank_bands(B, z0=0.3085, z1=0.3565):
    """the GREY_D flank band as a thin open-arc strip that hugs the hull flank (0.003 proud), y -0.25..0.38"""
    zs = [z0 + (z1 - z0) * i / 4 for i in range(5)]
    for s in (1, -1):
        rings = []
        for i in range(26):
            y = -0.25 + 0.63 * i / 25
            outer = [Vector((s * (hull_x(y, z) + 0.003), y, z)) for z in zs]
            inner = [Vector((s * (hull_x(y, z) - 0.008), y, z)) for z in zs]
            rings.append((outer, inner))
        B.tube(rings, GREY_D, "Spine", closed=False, nostud=True)


def model(k):'''
assert s.count("\ndef model(k):") == 1
s = s.replace("\ndef model(k):", "\n" + helpers, 1)
open(p, "w", encoding="utf-8").write(s)
print("ok")
